import requests
import json
import pandas as pd
import pickle

block_list = {
              '1' : ['Altstadt', 'Lehel'],
              '2' : ['Ludwigsvorstadt', 'Isarvorstadt'], 
              '3' : ['Maxvorstadt'], 
              '4' : ['Schwabing-West'], 
              '5' : ['Au', 'Haidhausen'], 
              '6' : ['Sendling-Westpark'], 
              '7' : ['Sendling'], 
              '8' : ['Schwanthalerhöhe'], 
              '9' : ['Neuhausen', 'Nymphenburg'], 
              '10' : ['Moosach'], 
              '11' : ['Milbertshofen', 'Am Hart'], 
              '12' : ['Schwabing', 'Freimann'], 
              '13' : ['Bogenhausen'], 
              '14' : ['Berg am Laim'], 
              '15' : ['Trudering', 'Riem'], 
              '16' : ['Ramersdorf', 'Perlach'],
              '17' : ['Obergiesing', 'Fasangarten'], 
              '18' : ['Untergiesing', 'Harlaching'],
              '19' : ['Thalkirchen', 'Obersendling', 'Forstenried', 'Fürstenried', 'Solln'],
              '20' : ['Hadern'], 
              '21' : ['Pasing', 'Obermenzing'], 
              '22' : ['Aubing', 'Lochhausen', 'Langwied'], 
              '23' : ['Allach', 'Untermenzing'], 
              '24' : ['Feldmoching', 'Hasenbergl'], 
              '25' : ['Laim']
}
gebiet_num_dict = {}

for (num, s) in block_list.items():
    for s1 in s:
        gebiet_num_dict[s1] = num




def get_links(start_date: str, end_date: str):
    """
    Retrieves links from the Polizeipräsidium München website based on the specified date range.

    Args:
        start_date (str): The start date of the range in the format 'DD-MM-YYYY'.
        end_date (str): The end date of the range in the format 'DD-MM-YYYY'.

    Returns:
        list: A list of links to the press releases from the Polizeipräsidium München website.
    """

    json_data = {
        'params': {
            'type': 'presse',
            'q': '{{"queryStr":false,"datefr":"{0}","dateto":"{1}","author":"Polizeipräsidium München"}}'.format(start_date, end_date),
        },
    }

    response = requests.post('https://www.polizei.bayern.de/es/search', json=json_data)
    json_data = json.loads(response.text)

    links = []
    for i in json_data['hits']['hits']:
        links.append(i['_source']['directory'])

    return links


def split_into_lists(text, link):
    """
    Splits the given text into lists based on the numeric pattern at the beginning of each line.

    Args:
    text (list): List of strings representing the text.

    Returns:
    list: List of lists, where each inner list represents a separate group of lines.
    """
    lists = []
    current_new = []

    for line in text:
        if line[0].isdigit(): # an old new ends -> save it 
            if not current_new:
                current_new = [line]
                continue

            title = current_new[0]
            for k in title.split():
                if k in gebiet_num_dict.keys(): # search for the district number 
                    gebiet = gebiet_num_dict[k]
                    news_list.append(' '.join(current_new))
                    gebiet_nums_list.append(gebiet)
                    all_links.append(link)
                    print(link)
                    break

            current_new = [line]
        else:
            current_new.append(line)

    if current_new: # if the new is not empty -> find its district numbers
        title = current_new[0]
        for k in title.split():
            if k in gebiet_num_dict.keys():
                gebiet = gebiet_num_dict[k]
                news_list.append(' '.join(current_new))
                gebiet_nums_list.append(gebiet)
                all_links.append(link)
                print(link)
                break


def get_news_lists(url):
    """
    Retrieves the news lists from the given URL.

    Args:
    url (str): The URL to retrieve the news lists from.

    Returns:
    list: List of lists, where each inner list represents a separate group of news.
    """
    from newspaper import Article

    d1 = Article(url)
    d1.download()
    d1.parse()

    return split_into_lists(d1.text.split('\n\n'), url)


news_list = []
gebiet_nums_list = []
all_links = []

import concurrent.futures

def get_dataset(start_date : str, end_date : str):
    
    links = get_links(start_date, end_date)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(get_news_lists, 'https://www.polizei.bayern.de' + link) for link in links]

    # Constructing a dataset of news and corresponding district numbers 
    p = pd.DataFrame({'new' : news_list, 'num' : gebiet_nums_list})
    return p

def get_predictions(df : pd.DataFrame, model):
    df['pred'] = model.predict(df.new)
    # saving the predictions
    df.to_csv('pred.csv', index=False)


def solve(start_date: str, end_date: str):
    """
    Process the data within the specified date range.

    Args:
        start_date (str): The start date of the data range.
        end_date (str): The end date of the data range.
    """
    
    with open('model.pkl', 'rb') as file:
        m = pickle.load(file)
    df = get_dataset(start_date, end_date)
    get_predictions(df, m)

print(solve("28.03.2022", "27.03.2024")) 
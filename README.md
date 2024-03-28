# crime-news-analyser

# **I. Introduction**
In the modern world, crime presents significant challenges for both law enforcement agencies and communities. Understanding the nature of these crimes and categorizing them effectively is crucial for implementing targeted intervention strategies. With this in mind, this project addresses the pressing need for accurate classification of crime acts into distinct categories based on their potential for human harm. Using advanced machine learning techniques, particularly Stochastic Gradient Descent and Naive Bayes Classifier, my model classifies crimes into three main categories: those unlikely to cause harm, those indirectly harming individuals, and those directly inflicting harm. The acts of vandalism would therefore be categorized into the first category, the act of burglary would fall into second category, a murder would be classified as a third category crime act

# **II. Materials and methods**
Data preprocessing
The crime news was collected from the [German police portal](https://www.polizei.bayern.de/aktuelles/pressemitteilungen/index.html) with a filter on Munich news via POST request and parsing of the resulting JSON file. Each website contains 3 to 6 news articles, which are being segmented into independent news. The data about the district of crime act is also being collected and analyzed. 

## Algorithms
Independent news is then being splitted into words, which are also being split using a custom composite word splitter (Kompositazerlegung) for German words (compound_splitter.py) using Aho-Corasick algorithm. The examples of the splitter can be seen below *(compound_splitter.py)*: 

<img width="515" alt="image" src="https://github.com/ol1g3/crime-news-analyser/assets/67047059/e9ca523e-804c-4344-bfaa-8bda7213d1c0">


Each word is then lemmatized using the Spacy lemmatizer to ensure consistency in word representation and avoid treating words of the same form as different entities. TF-IDF statistics are subsequently calculated for each word, providing insight into their significance within the document corpus. 

### Naive Bayes
The first algorithm I used was Naive Bayes Classifier (MultinomialNB) from scikit-learn library. Naive Bayes is a supervised learning classification model based on applying Bayes' theorem. The features are the results of TF-IDF statistic calculation. After hyperparameter tuning I decided to keep the default parameters of the model, as the hyperparameters did not change the training performance. The Naive Bayes Classifier got an accuracy over 92%

### Stochastic Gradient Descent
The second algorithm I used was Stochastic Gradient Descent (SGD) from scikit-learn. The reason I chose it is that the single word can classify the new. For instance, the word “Einbruch” is almost an indicator of the new being classified as the second type. Therefore, the task can be seen as a classification problem with 3 classes and not as an NLP problem. The hyperparameter tuning also showed the well performance of default parameters with an accuracy over 95%. 

# **III. Results**
In the time range from 28.03.2022 to 27.03.2024 an amount of 1631 news was collected, transformed and analyzed. These are the standings, different colors indicating different types of crime acts *(data-plotting.ipynb)*:

![image](https://github.com/ol1g3/crime-news-analyser/assets/67047059/bede269e-e39f-4da5-b27f-0234244e9b19)

Two districts in Munich stand out at the top of the crime table: Schwabing and Freimann, with a total of 176 reported acts, and Altstadt and Lehel, with 173 acts. Notably, Altstadt significantly leads in the third category of crime, while the second category does not have a distinct association with any city district. This information can also be obtained from the map chart of each of the three crime categories *(data-plotting.ipynb)*:

![image](https://github.com/ol1g3/crime-news-analyser/assets/67047059/b60ebf3b-c57a-4aaa-95cb-81025fb9d945)

# **IV. Closing thoughts**
I believe my project would be interesting for people who are considering relocating and seeking insights into the safety and crime trends of specific areas. A further objective is to develop a web interface containing all the collected information for easy access and exploration.

In conclusion, this project was incredibly interesting for me. I had the chance to go through essentially the whole data science workflow, from finding a unique problem statement, gathering data, training models and presenting, as well as somewhat accomplish my goal to create something useful. As undergraduate students, it was a tremendous learning experience and I am looking forward to creating more exciting projects like this one.

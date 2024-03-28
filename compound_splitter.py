import ahocorasick
from sympy import comp

german_plural_endings = [
    "e", "en", "n", "er", "s"
]

def make_auto(dictionary_path):
    """
    Create an Aho-Corasick automaton from a dictionary file.

    Args:
        dictionary_path (str): Path to the dictionary file.

    Returns:
        ahocorasick.Automaton: The Aho-Corasick automaton.
    """
    automaton = ahocorasick.Automaton()

    with open(dictionary_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()

    for i, word in enumerate(words):
        automaton.add_word(word.lower(), (word, word[0].isupper()))

    automaton.make_automaton()

    return automaton


def recursive_search(s: str, words: list[list], cur_pos: int = 0, cur_ind=0, cur_result: list[str] = []):
    """
    Recursively search for compound words in a string.

    Args:
        s (str): The input string.
        words (list[list]): List of found compound words in s with their start and end indices.
        cur_pos (int): Current position in the string.
        cur_ind (int): Current index in the words list.
        cur_result (list[str]): Current result list.

    Returns:
        list[str]: List of compound words found in the string.
    """
    # Check if the end of the string is reached
    if cur_pos == len(s):
        return cur_result

    # Check if the remaining string matches a German plural ending
    if s[cur_pos:] in german_plural_endings:
        return cur_result

    # Check if all words have been processed
    if cur_ind == len(words):
        return []

    while cur_ind < len(words):
        # Skip words that occur before the current position
        if words[cur_ind][0] < cur_pos:
            cur_ind += 1
            continue

        # Check if the word starts at the current position
        if words[cur_ind][0] == cur_pos:
            # Recursively search for compound words after the current word
            post_results = recursive_search(s, words, cur_pos=words[cur_ind][1]+1, cur_ind=cur_ind, cur_result=cur_result + [words[cur_ind][2]])
            if post_results:
                return post_results

        # Check if the word starts one position after the current position and the current character is 's'
        # 's' - the letter that can stay between compounds
        elif words[cur_ind][0] == cur_pos + 1 and s[cur_pos] == 's':
            # Recursively search for compound words after the current word
            post_results = recursive_search(s, words, cur_pos=words[cur_ind][1]+1, cur_ind=cur_ind, cur_result=cur_result + [words[cur_ind][2]])
            if post_results:
                return post_results

        cur_ind += 1

    # No compound words found
    return []

def get_compounds(text : str, automaton):
    """
    Extracts compound words from the given text using an automaton.

    Args:
        text (str): The input text from which to extract compound words.
        automaton: The automaton used for extracting compound words.

    Returns:
        list: A list of compound words found in the text. Each compound word is represented as a list
              containing the start index, end index, and lowercase word.

    """
    result = []
    for end_index, (word, is_noun) in automaton.iter(text):
        start_index = end_index - len(word) + 1
        # Skip words that are not nouns, abbreviations, or have less than 3 characters
        if not is_noun or word.isupper() or len(word) < 4:
            continue
        # Add the compound word to the result list
        result.append([start_index, end_index, word.lower()])

    # Sort the result list based on the start index
    result = sorted(result)
    return result

def solve(text: str, automaton):
    """
    Solve the compound splitting problem.

    Args:
        text (str): The input text.
        automaton (ahocorasick.Automaton): The Aho-Corasick automaton.

    Returns:
        list[list]: List of compound words found in the text.
    """
    # Iterate over the matches found by the automaton
    compounds = get_compounds(text, automaton)

    # Call the recursive_search function to find compound words in the text
    ans = recursive_search(text, compounds)

    # If no compound words are found, return an empty list
    if ans == None:
        return []

    # Filter out empty lists from the result and return the final list of compound words
    return list(filter(lambda x: x != [], ans))

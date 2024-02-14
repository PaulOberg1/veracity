import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance



# NOTE: I did not use tokenize library from nltk because it gives me sentences with each word character separated by a space.
def read_description(description):
    """
    Processes a given description into a list of sentences, where each sentence is represented as a list of words.

    Input:
    - STRING: The input description to be processed.

    Returns:
    - LIST: A list of sentences, where each sentence is represented as a list of words.
    """
    article = description.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    """
    Calculates the cosine similarity between two input sentences.

    Input:
    - LIST: First sentence represented as a list of words.
    - LIST: Second sentence represented as a list of words.
    - LIST (optional): Contains a list of stopwords to be ignored in similarity calculation.

    Returns:
    - FLOAT: Cosine similarity score between the two sentences.
    """
    if stopwords is None:
        stopwords = []
    sent1 = [i.lower() for i in sent1]
    sent2 = [i.lower() for i in sent2]
    all_words = list(set(sent1 + sent2))

    vect1 = [0] * len(all_words)
    vect2 = [0] * len(all_words)

    for i in sent1:
        if i in stopwords:
            continue
        vect1[all_words.index(i)] += 1
    for i in sent2:
        if i in stopwords:
            continue
        vect2[all_words.index(i)] += 1

    # Check if either of the vectors is a zero vector
    if sum(vect1) == 0 or sum(vect2) == 0:
        return "didn't work"
    else:
        return 1 - cosine_distance(vect1, vect2)


def gen_sim_matrix(sentences, stop_words):
    """
    Calculates sentence similarity matrix using cosine similarity measure.

    Input:
    - LIST: Contains list of sentences to compute similarity.
    - LIST: Contains list of stopwords to be ignored in similarity.

    Returns:
    - numpy.ndarray: Sentence similarity matrix.
    """
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)

    return similarity_matrix


def generate_summary(description, lines=5):
    """
    Processes and generates summary using google's PageRank algorithm.

    Input:
    - STRING: A string containing the description which needs to be summarised.
    - INT: An integer to determine the size of the summary. (Default = 5)

    Returns:
    - STRING: A string containing the summary of the description.
    """
    stop_words = stopwords.words("english")
    summarise_text = []
    sentences = read_description(description)
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    for i in range(lines):
        summarise_text.append(" ".join(ranked_sentence[i][1]))
    summary_of_description = (". ".join(summarise_text))

    return summary_of_description

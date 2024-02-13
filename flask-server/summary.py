import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from server import youtube, Flask, request, jsonify

app = Flask(__name__)


@app.route('/summarise', methods=['POST'])
def summarise():
    try:
        # write code to get YouTube description.
        """
        videoID = request.json
        
        # Make sure to import the 'YouTube' object from server.py
        response = youtube.captions().list(
            part="snippet",
            videoId=videoID
        ).execute()

        descriptions = []
        for item in response['items']:
            caption_id = item['id']
            description_response = youtube.captions().download(
                id=caption_id,
                tfmt="ttml"
            ).execute()
            # Decode the content directly without using .decode("utf-8")
            description = description_response["content"]
            descriptions.append(description)

        # Summarising descriptions array.
        youtuber_name = "__PLACEHOLDER__"
        pronouns = set(["he", "him", "his", "she", "her", "it", "its", "they", "them", "their"])

        # Removing pronoun component from description.
        for word in words:
            if word in pronouns:
                word = youtuber_name
        """

        # Mock description for testing.
        descriptions = "Soft house + beta wave isochronic tones (+ cool koala) for a high focus mental state while studying or working. Part of my peak focus for complex tasks series. ▶️ [1](https://www.youtube.com/watch?v=H1ZFro8_ZRQ&list=PLvge0IEcZWN7eQVidOQRkxiBxHoSkewww) ➡️ Subscribe to my channel and be updated with my latest tracks: [2](http://www.youtube.com/user/MindAmend?sub_confirmation=1) Use this track when working on advanced and complicated topics like coding/programming, mathematics, scientific formulas, financial analysis or any complex mental activity. Isochronic tones produce a stronger and more powerful brainwave entrainment effect when compared to binaural beats or standard music. What is this? This is a high-intensity audio brainwave entrainment session, using isochronic tones. Listen to this when you need a strong burst of intense focus to concentrate and study things like advanced mathematics, scientific formulas, financial analysis or any other complex mental activity. How is this session constructed? The session starts off beating at 10Hz and ramps up to 18Hz by the 6-minute mark. It stays at 18Hz until the final 5 minutes where it ramps back down again. How to use it? Listen to this track with your eyes open while doing the task/activity you want to focus on. Headphones are NOT required Although headphones are not required you may find they produce a more intense effect, because they help to block out distracting external sounds. When to listen? Because this track increases your beta brainwave activity, it's best to listen to this during the daytime and early evening. If you listen to this too close to bedtime, it might disrupt your sleep, in a similar way to how you might respond if you drank coffee just before going to bed. How loud should the volume be? The main thing to consider is that it should be loud enough to hear the repetitive isochronic tones so you don't so quiet you can hardly hear them but also don't want it so loud that uncomfortable for you hurts your ears gives headache recommend starting with volume around halfway adjust level feel comfortable there #upbeatsstudymusic #housestudymusic #focusmusic Artist credit: Jones Meadow Tracks: Jet Stream Familiar Lights Flares Sound Off Bet"

        # 2nd parameter in this function determines the size of summary.
        summary = generate_summary(descriptions, 2)

        return jsonify({"message": "successfully summarised", "data": summary}), 200

    except Exception as e:
        return jsonify({"message": f"error: {e}"}), 500


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
        return jsonify({"message": "It didn't work."}), 200
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


if __name__ == "__main__":
    app.run(debug=True)

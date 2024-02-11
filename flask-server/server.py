from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)
youtube = build("youtube","v3",developerKey="AIzaSyAO7SrY7EwY2JHv28qksxr2xmOSwbA96PU")

@app.route("/getComments", methods=["POST"])
def getComments():
    """
    Fetch YouTube comments given a video ID

    Input:
    - JSON: A JSON object containing the video ID

    Returns:
    - JSON: A JSON object containing array of comments
    """
    try:
        videoID = request.json

        #Fetch comments via YouTube API
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=videoID,
            maxResults=10
        ).execute()

        #Store comments in array
        comments = []
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        
        return jsonify({"message":"succesfully fetched comments","data":comments}),200
    except Exception as e:
        return jsonify({"message":f"error: {e}"}),500


@app.route("/rate",methods=["POST"])
def rate():
    """
    Perform sentiment analysis on a set of comments and return a score

    Input:
    - JSON: A JSON object containing an array of YouTube comments

    Returns:
    - JSON: A JSON object containing sentiment analysis score as a string
    """
    try:
        comments = request.json
        analyzer = SentimentIntensityAnalyzer()
        text = sum(comments) #Concatenate all the comments into a single block of text
        scores = analyzer.polarity_scores(text) #Compute the sentiment analysis scores of the text
        codeToWord = {"neg":"Negative","neu":"Neutral","pos":"Positive","compound":"Compound"} #Maps keys in 'scores' variable to readable form
        result = codeToWord[max([(key,value) for key,value in scores.items()],lambda pair: pair[1])[0]] #Obtains final rating as adjective

        return jsonify({"message":"success","data":result}),200
    except Exception as e:
        return jsonify({"message":f"error: {e}"}),500
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)
youtube = build("youtube","v3",developerKey="AIzaSyDk0We7u9xaFhJuJnJKIPJRbox0Km6X3n0")

#Configure logger
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)


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
        app.logger.debug("Request received at /getComments")
        videoID = request.json.get("videoID") #Fetch video ID from request data
        app.logger.debug(f"Video ID: {videoID}")

        #Fetch comments via YouTube API
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=videoID,
            maxResults=100
        ).execute()

        #Store comments in array
        comments = []
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        
        return jsonify({"message":"succesfully fetched comments","data":comments}),200
    except Exception as e:
        app.logger.error(f"Error with /getComments route: {e}")
        return jsonify({"message":f"error: {e}"}),500

@app.route("/getDescription",methods=["POST"])
def getDescription():
    """
    Fetch transcript of a YouTube video given a video ID

    Input:
    - JSON: A JSON object containing the video ID

    ReturnsL
    - JSON: A JSON object containing the transcript if function successful
    """
    try:
        app.logger.debug("Request received at /getDescription")
        videoID = request.json.get("videoID") #Fetch video ID from request data
        app.logger.debug(videoID)
        response = youtube.videos().list( #
            part="snippet",
            id = videoID
        ).execute()
        if response:
            app.logger.debug(response)
            app.logger.debug("response successful")
        video_description = response["items"][0]["snippet"]["description"]
        app.logger.debug(f"\n\n\nDESCRIPTION = {video_description}")
        
        return jsonify({"message":"description successfully retrieved from YouTube API", "data":video_description}),200
    except Exception as e:
        app.logger.error(f"Error with /getDescription route: {e}")
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
        app.logger.debug("Received request at /rate")
        comments = request.json
        analyzer = SentimentIntensityAnalyzer()
        text = "".join(list(comments)) #Concatenate all the comments into a single block of text
        scores = analyzer.polarity_scores(text) #Compute the sentiment analysis scores of the text
        result = str(scores["compound"])

        return jsonify({"message":"success","data":result}),200
    except Exception as e:
        app.logger.error(f"Error with /rate route: {e}")
        return jsonify({"message":f"error: {e}"}),500

@app.route('/') #Root of application
def index():
    return "Hello, this is the root of the Flask application!"

if __name__=="__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask_cors import CORS
import logging
import requests
from summary import generate_summary


app = Flask(__name__)
CORS(app)
app.config["PREFERRED_URL_SCHEME"]="https"
youtube = build("youtube","v3",developerKey="AIzaSyDk0We7u9xaFhJuJnJKIPJRbox0Km6X3n0")

#Configure logger
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

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
        data = request.json.get("metadata")
        comments = data.get("comments")
        analyzer = SentimentIntensityAnalyzer()
        text = "".join(list(comments)) #Concatenate all the comments into a single block of text
        scores = analyzer.polarity_scores(text) #Compute the sentiment analysis scores of the text
        result = str(scores["compound"])
        app.logger.debug("success rating")
        return jsonify({"message":"success","data":result}),200
    except Exception as e:
        app.logger.error(f"Error with /rate route: {e}")
        return jsonify({"message":f"error: {e}"}),500

@app.route('/summarise', methods=['POST'])
def summarise():
    """
    Summarise given description and return to frontend

    Input:
    - JSON: A JSON object containing a YouTube description as a string

    Returns:
    - A JSON object containing the summarised text as a string
    """
    try:
        app.logger.debug("Request received at metadata endpoint")
        #Access video metadata
        metadata = request.json.get("metadata")
        description = metadata.get("description")
        title = metadata.get("title")#request.json.get("title")
        category = metadata.get("category")#request.json.get("topic")
        app.logger.debug(description,title,category)
        # 2nd parameter in this function determines the size of summary.
        summary = generate_summary(description, 1)

        return jsonify({"message":"text successfully summarised","data":summary}),200
    except Exception as e:
        app.logger.debug(f"text summarisation unsuccessful: {e}")
        return jsonify({"message":"text summarisation unsuccessful"}),500   

@app.route("/getMetadata", methods=["POST"])
def getMetadata():
    """
    Fetch metadata of video given its ID
    Request video's title, description, comments and category from YouTube Data API

    Input:
    - JSON: A JSON object containing the video ID

    Returns
    - JSON: A JSON object containing video's metadata
    """
    try:
        app.logger.debug("successfully accessed /getMetadata endpoint")
        videoID = request.json.get("videoID") #Fetch video ID from request data

        #Accessing video description, title and category
        params = { #Parameters to be sent with request to YouTube Data API
            "part":"snippet",
            "id":videoID,
            "maxResults":100, 
            "key":"AIzaSyDk0We7u9xaFhJuJnJKIPJRbox0Km6X3n0" #API key
        }
        url = "https://www.googleapis.com/youtube/v3/videos" #URL to request data from
        data = requests.get(url,params=params).json()

        description = data["items"][0]["snippet"]["description"]
        title = data["items"][0]["snippet"]["title"]
        category = data["items"][0]["snippet"].get("categoryID")

        #Accessing comments section
        params = {
            "part":"snippet",
            "videoId":videoID,
            "key":"AIzaSyDk0We7u9xaFhJuJnJKIPJRbox0Km6X3n0"
        }
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        data = requests.get(url,params=params).json()

        comments = []
        for item in data["items"]: #Store comments in array
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        
        #Accesing channel name
        channel_id = data["items"][0]["snippet"]["channelId"]
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part":"snippet",
            "id":channel_id,
            "key":"AIzaSyDk0We7u9xaFhJuJnJKIPJRbox0Km6X3n0"
        }
        data = requests.get(url,params=params).json()
        
        channel_title = data["items"][0]["snippet"]["title"]
        channel_description = data["items"][0]["snippet"]["description"]
        channel_creation_date = data["items"][0]["snippet"]["publishedAt"]
        channel_thumbnail = data["items"][0]["snippet"]["thumbnails"].get("default",{}).get("url")
        
        return jsonify({"message":"successfully retrieved metadata",
                        "data": {
                            "comments":comments,
                            "description":description,
                            "title":title,
                            "category":category,
                            "channel_title":channel_title,
                            "channel_description":channel_description,
                            "channel_creation_date":channel_creation_date,
                            "channel_thumbnail":channel_thumbnail
                        }
                        })
    except Exception as e:
        app.logger.error(f"failure at /getMetadata endpoint: {e}")
        return jsonify({"message":f"unsuccessful retrieving metadata: {e}"}),500


@app.route('/') #Root of application
def index():
    return "Hello, this is the root of the Flask application!"

if __name__=="__main__":
    app.run(debug=True)
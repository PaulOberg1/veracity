from flask import Flask, request, jsonify
from googleapiclient.discovery import build

app = Flask(__name__)
youtube = build("youtube","v3",developerKey="AIzaSyAO7SrY7EwY2JHv28qksxr2xmOSwbA96PU")

@app.route("/getComments", methods=["POST"])
def getComments():
    """
    Fetch YouTube comments given a video ID

    Returns:
    - JSON: Data field contains array of comments
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


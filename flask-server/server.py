from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

@app.route("/getTranscript",methods=["POST"])
def getTranscript():
    """
    Fetch transcript of a YouTube video given a video ID

    Input:
    - JSON: A JSON object containing the video ID

    ReturnsL
    - JSON: A JSON object containing the transcript if function successful
    """
    try:
        videoID = request.json #Fetch video ID from request data
        response = youtube.captions().list( #
            part="snippet",
            videoId = videoID
        )
        transcripts=[]
        for item in response["items"]:
            caption_id=item["id"] #Get ID of given caption track
            transcript_response=youtube.captions.download( #Get caption track matching video ID
                id=caption_id,
                tfmt="ttml" #Convert caption track to Timed Text Markup Language format
            ).execute()
            transcript=transcript_response.decode("utf-8")
            transcripts.append(transcript)
        
        return jsonify({"message":"transcript successfully retrieved from YouTube API", "data":transcripts}),200
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

if __name__=="__main__":
    app.run(debug=True)
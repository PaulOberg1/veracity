/*
    File: ratingPage.js
    Description: This file implements the veracity rating feature of the program.
    Dependencies: react, axios
*/

import React, {useState} from "react";
import axios from "axios";


/**
 * Decodes a given video URL into video ID
 * @param {string} url The video URL
 * @returns {string | null} The video ID
 */
const getVideoID = (url) => {
    const string = "/^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/"; //String to compare against
    const id = url.match(string); //Matches string with given url
    
    if (match && match[2].length === 11) { //If output valid, ID of expected length
        return match[2];
    } else {
        return null;
    }
}


const ratingPage = () => {
    const [comments,setComments] = useState("");
    const [rating, setRating] = useState(null);

    
    /**
     * Makes POST request to backend to send current video id
     * Receives comment section of given video
     *  Updates 'comments' state
     */
    const getComments = () => {
        const videoID = getVideoID(window.location.href);
        axios.post("/getComments",videoID)
        .then(response => response.json)
        .then(result => {
            console.log(`success : ${result.message}`);
            setComments(result.data);
        })
        .catch((error) => {
            console.error(`error: ${error}`);
        })
    }


    /**
     * Makes POST request to backend to send comment data
     * Receive sentiment analysis scores of comments
     * Handles error checking
     */        
    const getRating = () => {
        axios.post("/rate",comments)
        .then(response => response.json)
        .then(result => {
            console.log("response: " + result.message);
            setRating(result.data);
        })
        .catch((error) => {
            console.error("error : " + error.message);
        })
    }

    return (
        <div>
            <button onClick={() => {getRating}}>Veracity Rating</button>
            {rating &&
            <p>Rating = {rating}</p>
            }
        </div>
    )
}

export default ratingPage;
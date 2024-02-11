/*
    File: RatingPage.js
    Description: This file implements the veracity rating feature of the program.
    Dependencies: react, axios
*/

import React, {useState,useEffect} from "react";
import axios from "axios";



/**
 * Display rating page with rate button and rating
 * @returns {HTML} The rating page as HMTL
 */
const RatingPage = (videoID) => {
    const [comments,setComments] = useState("");
    const [rating, setRating] = useState(null);

    useEffect(() => { //Call once video ID available
        /**
         * Makes POST request to backend to send current video id
         * Receives comment section of given video
         *  Updates 'comments' state
         */
        const getComments = () => {
            axios.post("/getComments",videoID) //Post video ID to backend
            .then(response => response.json) //Convert response to json
            .then(result => {
                console.log(`success : ${result.message}`);
                setComments(result.data); //Update 'comments' state
            })
            .catch((error) => {
                console.error(`error: ${error}`);
            })
        };
        getComments();
    },[videoID]);


    /**
     * Makes POST request to backend to send comment data
     * Receive sentiment analysis scores of comments
     * Handles error checking
     */        
    const getRating = () => {
        axios.post("/rate",comments) //Post comments to backend
        .then(response => response.json) //Recieve backend response, convert to JSON
        .then(result => {
            console.log("response: " + result.message); //Log success
            setRating(result.data); //Acccess rating from backend response, update 'rating' state
        })
        .catch((error) => {
            console.error("error : " + error.message);
        })
    }

    return (
        <div>
            <button onClick={getRating()}>Veracity Rating</button>

            {/* Rating Display if available */}
            {rating &&
            <p>Rating = {rating}</p>
            }
        </div>
    )
}

export default RatingPage;
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
const RatingPage = ({metadata}) => {
    const [rating, setRating] = useState("");

    useEffect(() => {
        /**
         * Makes POST request to backend to send comment data
         * Receive sentiment analysis scores of comments
         * Handles error checking
         */        
        const getRating = () => {
            console.log("rate metadata = " + metadata);
            axios.post("/rate",{metadata:metadata}, {headers: {"Content-Type":"application/json"}}) //Post metadata to backend
            .then(response => response.data)
            .then(result => {
                console.log("response: " + result.message); //Log success
                setRating(result.data); //Acccess rating from backend response, update 'rating' state
            })
            .catch((error) => {
                console.error("error : " + error);
            })
        }
        if (metadata) {
            console.log("Metadata available for rate");
            getRating();
        }
    },[metadata]);

    return (
        <div>

            {/* Rating Display if available */}
            {rating &&
            <p>Rating = {rating}</p>
            }
        </div>
    )
}

export default RatingPage;
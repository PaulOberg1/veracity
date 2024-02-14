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

    // useEffect(() => { //Call once video ID available
    //     /**
    //      * Makes POST request to backend to send current video id
    //      * Receives comment section of given video
    //      *  Updates 'comments' state
    //      */
    //     const getComments = () => {
    //         axios.post("/getComments",videoID, {headers: {"Content-Type":"application/json"}}) //Post video ID to backend
    //         .then(response => response.data)
    //         .then(result => { //Receive comments array from backend
    //             console.log(`success : ${result.message}`);
    //             setComments(result.data); //Update 'comments' state
    //         })
    //         .catch((error) => {
    //             console.error(`error: ${error}`);
    //         })
    //     };
    //     if (videoID) {
    //         console.log(`Video ID available for post request`);
    //         getComments();
    //     }
    // },[videoID]);


    useEffect(() => {
        /**
         * Makes POST request to backend to send comment data
         * Receive sentiment analysis scores of comments
         * Handles error checking
         */        
        const getRating = () => {
            console.log(metadata);
            axios.post("/rate",{metadata:metadata}, {headers: {"Content-Type":"application/json"}}) //Post comments to backend
            .then(response => response.data)
            .then(result => {
                console.log("response: " + result.data); //Log success
                setRating(result.data); //Acccess rating from backend response, update 'rating' state
            })
            .catch((error) => {
                console.error("error : " + error);
            })
        }
        if (metadata) {
            console.log("Comments available for post request");
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
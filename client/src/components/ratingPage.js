/*
    File: ratingPage.js
    Description: This file implements the veracity rating feature of the program.
    Dependencies: react, axios
*/

import react, {useState} from "react";
import axios from "axios";



const ratingPage = () => {
    const [comments,setComments] = useState("");
    const [rating, setRating] = useState(null);

    /*
        Makes POST request to backend to send comment data
        Receive sentiment analysis scores of comments
        Handles error checking
    */
    const getRating = () => {
        axios.post("/rate",comments)
        .then(response => response.json)
        .then(result => {
            console.log("response: " + result.message);
            setRating(result.data);
        })
        .catch((error) => {
            console.error("error : " + error.message)
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
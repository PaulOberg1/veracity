/*
    File: summaryPage.js
    Description: Implement transcript summary feature.
    Dependencies: react, axios 
*/

import React, {useState} from "react";
import axios from "axios";



const summaryPage = () => {
    const [transcript,setTranscript] = useState("");
    const [summaryHTML,setSummaryHTML] = useState(null);

    /**
     * Makes POST request to backend sending transcript data
     * Receives summary HTML data from backend and stores data
     * Handles error checking
     */
    const sendTranscript = () => {
        axios.post("/summarise",transcript)
        .then(response => response.json)
        .then(result => {
            console.log("response : " + result.message);
            setSummaryHTML(result.text); //Store summary data as html on frontend
        })
        .catch((error) => {
            console.error("error: " + e);
        })
    }

    return (
        <div>
            {transcript && (
                <button onClick={sendTranscript}>Summarise Video</button>
            )}
            {summaryHTML && (
                <div dangerouslySetInnerHTML={{__html: summaryHTML}} /> 
            )}
            
        </div>
    )
}

export default summaryPage;
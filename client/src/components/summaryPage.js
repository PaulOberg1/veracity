/*
    File: SummaryPage.js
    Description: Implement transcript summary feature.
    Dependencies: react, axios 
*/

import React, {useState,useEffect} from "react";
import axios from "axios";


/**
 * Display summary page with summarise button and summarised transcript
 * @returns {HTML} The summary page as HTML
 */
const SummaryPage = (videoID) => {
    const [transcript,setTranscript] = useState("");
    const [summaryHTML,setSummaryHTML] = useState(null);


    useEffect(() => { //Call once video ID available
        /**
         * Fetch transcript from backend given video ID
         */
        const getTranscript = () => {
            axios.post("/getTranscript",videoID) //Post video ID to backend
            .then(response => response.json) //Receive transcript from backend
            .then(result => {
                console.log(result.message);
                setTranscript(result.data); //Update transcript state
            })
            .catch((error) => {
                console.log(error.message);
            })
        };
        getTranscript();
    },[videoID]);

    /**
     * Makes POST request to backend sending transcript data
     * Receives summary HTML data from backend and stores data
     * Handles error checking
     */
    const sendTranscript = () => {
        axios.post("/summarise",transcript) //Send transcript to backend
        .then(response => response.json) //Receive summary data from backend, convert to JSON
        .then(result => {
            console.log("response : " + result.message);
            setSummaryHTML(result.text); //Store summary data as html on frontend
        })
        .catch((error) => {
            console.error("error: " + error);
        })
    }

    return (
        <div>
            {/* Summary Button if transcript available */}
            {transcript && (
                <button onClick={sendTranscript()}>Summarise Video</button>
            )}
            {/* Summary Display if available */}
            {summaryHTML && (
                <div dangerouslySetInnerHTML={{__html: summaryHTML}} /> 
            )}
            
        </div>
    )
}

export default SummaryPage;
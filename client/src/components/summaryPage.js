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
            axios.post("/getTranscript",videoID, {headers: {"Content-Type":"application/json"}}) //Post video ID to backend
            .then(response => response.json)
            .then(result => { //Receive transcript from backend
                console.log(result.message);
                setTranscript(result.data); //Update transcript state
            })
            .catch((error) => {
                console.log(error.message);
            })
        };
        getTranscript();
    },[videoID]);

    useEffect(() => { //Call each time transcript updated
        /**
         * Makes POST request to backend sending transcript data
         * Receives summary HTML data from backend and stores data
         * Handles error checking
         */
        const sendTranscript = () => {
            axios.post("/summarise",{transcript:transcript}, {headers: {"Content-Type":"application/json"}}) //Send transcript to backend
            .then(response => response.data)
            .then(result => { //Receive summary data from backend
                console.log("response : " + result.message);
                setSummary(result.text); //Store summary data as html on frontend
            })
            .catch((error) => {
                console.error("error: " + error);
            })
        };
        if (transcript)
            sendTranscript();
    },[transcript]);

    return (
        <div>

            {/* Summary Display if available */}
            {summaryHTML && (
                <div dangerouslySetInnerHTML={{__html: summaryHTML}} /> 
            )}
            
        </div>
    )
}

export default SummaryPage;
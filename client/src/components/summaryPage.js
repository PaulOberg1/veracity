/*
    File: SummaryPage.js
    Description: Implement description summary feature.
    Dependencies: react, axios 
*/

import React, {useState,useEffect} from "react";
import axios from "axios";


/**
 * Display summary page with summarise button and summarised description
 * @returns {HTML} The summary page as HTML
 */
const SummaryPage = (videoID) => {
    const [description,setDescription] = useState("");
    const [summary,setSummary] = useState("");


    useEffect(() => { //Call each time video ID updated
        /**
         * Fetch description from backend given video ID
         */
        const getDescription = () => {
            axios.post("/getDescription",videoID, {headers: {"Content-Type":"application/json"}}) //Post video ID to backend
            .then(response => response.data)
            .then(result => { //Receive description from backend
                console.log(result.message);
                setDescription(result.data); //Update description state
            })
            .catch((error) => {
                console.log(error.message);
            })
        };
        if (videoID)
            getDescription();
    },[videoID]);

    useEffect(() => { //Call each time description updated
        /**
         * Makes POST request to backend sending description data
         * Receives summary HTML data from backend and stores data
         * Handles error checking
         */
        const sendDescription = () => {
            axios.post("/summarise",{description:description}, {headers: {"Content-Type":"application/json"}}) //Send description to backend
            .then(response => response.data)
            .then(result => { //Receive summary data from backend
                console.log("response : " + result.message);
                setSummary(result.text); //Store summary data as html on frontend
            })
            .catch((error) => {
                console.error("error: " + error);
            })
        };
        if (description)
            sendDescription();
    },[description]);

    return (
        <div>
            {/* Summary Display if available */}
            {summary && (
                <p>{summary}</p>
            )}
            
        </div>
    )
}

export default SummaryPage;
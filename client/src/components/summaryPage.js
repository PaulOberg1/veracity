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
const SummaryPage = ({metadata}) => {
    const [summary,setSummary] = useState("");

    useEffect(() => { //Call each time description updated
        /**
         * Makes POST request to backend sending description data
         * Receives summary HTML data from backend and stores data
         * Handles error checking
         */
        const sendMetadata = () => {
            console.log("metadata = " + metadata);
            axios.post("/summarise",{metadata:metadata}, {headers: {"Content-Type":"application/json"}}) //Post metadata to backend
            .then(response => response.data)
            .then(result => { //Receive summary data from backend
                console.log("response : " + result.message);
                setSummary(result.data); //Store summary data as html on frontend
            })
            .catch((error) => {
                console.error("error: " + error);
            })
        };
        if (metadata) {
            console.log("metadata available for summary")
            sendMetadata();
        }
    },[metadata]);

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
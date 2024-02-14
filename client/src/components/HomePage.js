/**
 * File: Home.js
 * Description: This file displays a home page with a summary tab and rating tab, displaying SummaryPage.js and RatingPage.js respectively.
 * Dependencies: react
 */

import React, {useState, useEffect} from "react";
import axios from "axios";
import SummaryPage from "./SummaryPage";
import RatingPage from "./RatingPage";

/**
 * Decodes a given video URL into video ID
 * @param {string} url The video URL
 * @returns {string | null} The video ID
 */
const getVideoID = (url) => {
    const string = /^(?:.*(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=))([^#\&\?]*).*/;
    const id = url.match(string); //Matches string with given url
    if (id && id[1].length === 11) { //If output valid, ID of expected length
        return id[1];
    } else {
        return null;
    }
}



/**
 * Displays the home page
 * @returns {HTML} The home page HTML containing 2 buttons and corresponding tabs
 */
const HomePage = () => {
    const [activeTab, setActiveTab] = useState("ratingTab"); //Either rating tab or summary tab

    const [URL, setURL] = useState("https://www.youtube.com/watch?v=MJiBpHVdzAg");
    
    const [metadata, setMetadata] = useState({});


    useEffect(() => { //Run once at start of program
        /**
         * Retrieves title, description, topic and commments of video given its ID
         */
        const getMetadata = () => {
            const videoID = getVideoID(URL);
            axios.post("/getMetadata",{videoID:videoID}, {headers: {"Content-Type":"application/json"}})
            .then(response => response.data)
            .then(result => {
                console.log(result.message);
                setMetadata(result.data);              
            })
            .catch((error) => {console.error(`error occured fetching metadata: ${error}`)})
        };
        if (URL)
            getMetadata();
    },[URL]);


    return (
        <div>

            <form>
                <label>URL</label>
                <input type="text" value={URL} onChange={(e) => {setURL(e.target.value)}}/>
            </form>

            {/* Tab Section*/}
            <div id="tabs">

                {/* Button to switch to rating tab */}
                <button className={activeTab==="ratingTab" ? "active" : "inactive"}
                onClick={() => {setActiveTab("ratingTab")}}>
                    Rating
                </button>

                {/* Button to switch to summary tab */}
                <button className={activeTab==="summaryTab" ? "active" : "inactive"}
                onClick={() => {setActiveTab("summaryTab")}}>
                    Summary
                </button>
            </div>

            {/* Display contents of either tab */}
            {activeTab==="ratingTab" && <RatingPage comments={metadata} />}
            {activeTab==="summaryTab" && <SummaryPage metadata={metadata} />}
        </div>
    )
}

export default HomePage;
/**
 * File: Home.js
 * Description: This file displays a home page with a summary tab and rating tab, displaying SummaryPage.js and RatingPage.js respectively.
 * Dependencies: react
 */

import React, {useState} from "react";
import SummaryPage from "./SummaryPage";
import RatingPage from "./RatingPage";

/**
 * Displays the home page
 * @returns {HTML} The home page HTML containing 2 buttons and corresponding tabs
 */
const HomePage = () => {
    const [activeTab, setActiveTab] = useState("ratingTab"); //Either rating tab or summary tab

    return (
        <div>

            {/* Tab Section*/}
            <div id="tabs">

                {/* Button to switch to rating tab */}
                <button className={activeTab=="ratingTab" ? "active" : "inactive"}
                onClick={() => {setActiveTab("ratingTab")}}>
                    Rating
                </button>

                {/* Button to switch to summary tab */}
                <button className={activeTab=="summaryTab" ? "active" : "inactive"}
                onClick={() => {setActiveTab("summaryTab")}}>
                    Summary
                </button>
            </div>

            {/* Display contents of either tab */}
            {activeTab==="ratingTab" && <RatingPage />}
            {activeTab==="summaryTab" && <SummaryPage />}
        </div>
    )
}

export default HomePage;
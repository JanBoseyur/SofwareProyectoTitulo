
import { useState } from "react";

import "../styles/dashboard.css";

import VoiceChart from "../components/charts/VoiceCharts";
import Button from "../components/buttonNavbar";

function Dashboard() {
    return (

        <div className = "body">
            
            <div className = "chartContainer">
                <VoiceChart/>
            </div>

        </div>
    );
}

export default Dashboard;
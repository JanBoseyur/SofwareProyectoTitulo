
import "../styles/dashboard.css";

import VoiceChart from "../components/charts/VoiceCharts";

function Dashboard() {
    return (

        <div className = "bodyDashboard">
            
            <div className = "textContainer">
                <div className = "titulo">
                    Vochice
                </div>

                <div className = "descripcion">
                    Software de orientación a posible riesgo suicida
                    mediante análisis sonoro
                </div>
            </div>

            <div className = "chartContainer">
                <VoiceChart/>
            </div>

        </div>
    );
}

export default Dashboard;
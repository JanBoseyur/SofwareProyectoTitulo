
import { Outlet } from "react-router-dom";

import Navbar from "../components/navbar";
import "../styles/home.css";

function Home() {
    return (
        <div className = "body">

            <Navbar />

            <main className = "homeContainer">
                <Outlet />
            </main>

        </div>
    );
}

export default Home;

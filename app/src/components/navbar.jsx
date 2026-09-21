
import { Archive, ChartLine, Library, Bug, ChartPie, Package } from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

import "../styles/navbar.css";
import Button from "../components/buttonNavbar";

function Navbar() {
    return (

        <nav className = "body">

            <div className = "contentContainer">

                <NavLink to="/">
                    <Button icon = {ChartLine} className = "buttonNav">
                    </Button>
                </NavLink>

                <NavLink to="/library">
                    <Button icon = {Library} className = "buttonNav">
                    </Button>
                </NavLink>

                <Button icon = {Archive} className = "buttonNav">
                </Button>

                <Button icon = {Bug} className = "buttonNav">
                </Button>

                <Button icon = {ChartPie} className = "buttonNav">
                </Button>

                <Button icon = {Package} className = "buttonNav">
                </Button>

            </div>

        </nav>
        
    );
}

export default Navbar;

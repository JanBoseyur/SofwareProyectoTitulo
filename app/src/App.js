
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import Dashboard from "./pages/dashboard";
import Library from "./pages/library";
import Data from "./pages/data"
import Bug from "./pages/bug"

function App() {
    return (

        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}>
                    <Route index element={<Dashboard />} />
                    <Route path="library" element={<Library />}/>
                    <Route path="data" element={<Data />}/>
                    <Route path="bug" element={<Bug />}/>
                </Route>
            </Routes>
        </BrowserRouter>
        
    );
}

export default App;
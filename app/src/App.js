
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/home";
import Dashboard from "./pages/dashboard";
import Library from "./pages/library";

function App() {
    return (

        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}>
                    <Route index element={<Dashboard />} />
                    <Route path="library" element={<Library />}/>
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
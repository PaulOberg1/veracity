import './App.css';
import {BrowserRouter as Router,Routes,Route,Navigate} from "react-router-dom";
import HomePage from "./components/HomePage.js";
import RatingPage from "./components/RatingPage.js";
import SummaryPage from "./components/SummaryPage.js";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/rate" element={<RatingPage />}/>
          <Route path="/summarise" element={<SummaryPage />}/>
          <Route path="/home" element={<HomePage />}/>
          <Route path="/" element={<Navigate to="/home"/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

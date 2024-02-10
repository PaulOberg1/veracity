import './App.css';
import {Router,Routes,Route,Navigate} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/rate" element={{ratingPage}}/>
          <Route path="/summarise" element={{summaryPage}}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

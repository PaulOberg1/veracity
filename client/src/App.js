import './App.css';
import {Router,Routes,Route,Navigate} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/rate" element={{RatingPage}}/>
          <Route path="/summarise" element={{SummaryPage}}/>
          <Route path="/home" element={{HomePage}}/>
          <Route path="/" element={
            <>
              <Navigate to="/home"/>
            </>
          }/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

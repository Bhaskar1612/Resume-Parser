import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import UploadForm from "./UploadForm";
import SearchPage from "./SearchPage";
import SearchResult from "./SearchResult";
import ThankYouPage from "./ThankYouPage";
import "./index.css";

function App() {
  return (
    <Router>
      <div className="homepage-container">
        <h1 className="homepage-title">Resume Extractor</h1>
        <div className="homepage-buttons">
          <Link to="/upload" className="homepage-button">Extract Resume</Link>
          <Link to="/search" className="homepage-button">Search Resume</Link>
        </div>
      </div>
      <Routes>
        <Route path="/upload" element={<UploadForm />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/search-result" element={<SearchResult />} />
        <Route path="/thank-you" element={<ThankYouPage />} />
      </Routes>
    </Router>
  );
}

export default App;

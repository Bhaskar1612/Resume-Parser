import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadForm from "./UploadForm";
import ThankYouPage from "./ThankYouPage";

function App() {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<UploadForm />} />
        <Route path="/thank-you" element={<ThankYouPage />} />
      </Routes>
    </Router>
  );
}

export default App;

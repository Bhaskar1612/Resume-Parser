import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./index.css";

function SearchPage() {
  const [userPrompt, setUserPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/v1/search-resume/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_prompt: userPrompt }),
      });
      const data = await response.json();
      navigate("/search-result", { state: { resume: data } });
    } catch (error) {
      console.error("Error searching resume:", error);
    }
  };

  return (
    <div className="search-container">
      <h2>Search Resume</h2>
      <input
        type="text"
        placeholder="Enter search prompt"
        value={userPrompt}
        onChange={(e) => setUserPrompt(e.target.value)}
        className="search-input"
      />
      <button onClick={handleSearch} className="search-button" disabled={loading}>
        {loading ? "We are processing. Plz wait" : "Search"}
      </button>
    </div>
  );
}

export default SearchPage;
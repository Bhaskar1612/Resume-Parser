import { useNavigate } from "react-router-dom";

function ThankYouPage() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h2>Thank You! 🎉</h2>
      <p>Your resume has been submitted successfully.</p>
      <button onClick={() => navigate("/")}>Back</button>
    </div>
  );
}

export default ThankYouPage;

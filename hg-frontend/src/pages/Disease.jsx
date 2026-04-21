import BackgroundAnimation from "../components/BackgroundAnimation";
import { useState } from "react";

export default function Disease() {
  const [symptoms, setSymptoms] = useState("");
  const [result, setResult] = useState("");

  const handleAnalyze = () => {
    setResult("Analyzing symptoms... (backend coming next)");
  };

  return (
    <div className="page">
      <BackgroundAnimation src="https://lottie.host/49f15b81-8d4b-474f-843a-efb9deea97ad/0e1xN0W7Bl.lottie" />

      <h1>Disease Prediction</h1>

      <input
        className="input"
        placeholder="Enter symptoms..."
        value={symptoms}
        onChange={(e) => setSymptoms(e.target.value)}
      />

      <button className="btn" onClick={handleAnalyze}>
        Analyze
      </button>

      {result && <div className="result-box">{result}</div>}
    </div>
  );
}
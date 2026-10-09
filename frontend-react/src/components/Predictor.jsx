import { useState } from "react";

function Predictor() {

  const [message, setMessage] = useState("");
  const [result, setResult] = useState("");

  const detectScam = async () => {

    if (!message.trim()) {
      setResult("Please enter a message");
      return;
    }

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
          }),
        }
      );

      const data = await response.json();

      if (data.prediction.includes("Scam")) {
         setResult("🚨 THREAT DETECTED. It's a Scam");
      } else {
          setResult("✅ MESSAGE IS SAFE");
      }

    } catch (error) {
      console.error(error);
      setResult("❌ Backend connection failed");
    }
  };

  return (
    <section className="Predictor">

     <h2>Try the Detector</h2>

<label className="message-label">
  Enter SMS / Email / UPI Fraud Message
</label>

<textarea
  placeholder="Paste suspicious message here for AI analysis..."
  value={message}
  onChange={(e) => setMessage(e.target.value)}
/>
      <button onClick={detectScam}>
        Predict🔍
      </button>

     {result && (
  <div
    className="result"
    style={{
      color:
        result.includes("THREAT")
          ? "#ff4d4d"
          : "#22c55e",
    }}
  >
    {result}
  </div>
)}
    </section>
  );
}

export default Predictor;
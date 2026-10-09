import { useState } from "react";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

const examples = [
  {
    label: "Suspicious",
    text: "URGENT: Your bank account will be blocked today. Verify your details at http://secure-bank-check.example and share your OTP.",
  },
  {
    label: "Routine",
    text: "Hi, the team meeting has been moved to 3:30 PM tomorrow. Please confirm if you can attend.",
  },
];

function Predictor() {
  const [message, setMessage] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const detectScam = async (event) => {
    event.preventDefault();
    if (!message.trim()) {
      setError("Enter a message to start the analysis.");
      setAnalysis(null);
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);
    try {
      const response = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message.trim() }),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || `The analysis service returned HTTP ${response.status}.`);
      }
      setAnalysis(data);
    } catch (requestError) {
      setError(
        requestError instanceof TypeError
          ? "Could not connect to the analysis API. Start the backend and check VITE_API_BASE_URL."
          : requestError.message || "Analysis failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const isScam = analysis?.label === "scam";

  return (
    <section className="workspace" id="analyze">
      <div className="section-heading">
        <div>
          <p className="eyebrow">MESSAGE INSPECTION</p>
          <h2>Analyze a suspicious message</h2>
          <p className="muted">Paste an SMS, email snippet, or payment-related message. Analysis runs against the configured NLP model.</p>
        </div>
        <span className="local-badge"><span className="status-dot" /> On-demand scan</span>
      </div>

      <div className="analysis-grid">
        <form className="input-panel" onSubmit={detectScam}>
          <label className="message-label" htmlFor="message-input">Message content</label>
          <textarea
            id="message-input"
            maxLength={10000}
            placeholder="Paste the complete message here. Remove personal information first."
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            aria-describedby="message-hint"
          />
          <div className="input-meta">
            <span id="message-hint">Do not include real passwords, OTPs, or account numbers.</span>
            <span>{message.length.toLocaleString()} / 10,000</span>
          </div>
          <div className="examples">
            <span className="examples-label">Try an example</span>
            {examples.map((example) => (
              <button
                className="example-button"
                key={example.label}
                type="button"
                onClick={() => { setMessage(example.text); setAnalysis(null); setError(""); }}
              >
                {example.label}
              </button>
            ))}
            <button className="example-button clear-button" type="button" onClick={() => { setMessage(""); setAnalysis(null); setError(""); }}>
              Clear
            </button>
          </div>
          <button className="analyze-button" type="submit" disabled={loading || !message.trim()}>
            {loading ? <><span className="spinner" /> Analyzing message…</> : <>Run threat analysis <span aria-hidden="true">→</span></>}
          </button>
          {error && <p className="error-message" role="alert">{error}</p>}
        </form>

        <aside className="result-panel" aria-live="polite">
          {!analysis && !loading && !error && (
            <div className="empty-state">
              <div className="scan-mark" aria-hidden="true">⌁</div>
              <p className="eyebrow">ANALYSIS REPORT</p>
              <h3>Waiting for a message</h3>
              <p className="muted">Your classification and explainable warning signals will appear here.</p>
              <div className="report-placeholder"><span /> <span /> <span /></div>
            </div>
          )}
          {loading && (
            <div className="empty-state">
              <div className="spinner large-spinner" />
              <h3>Inspecting message</h3>
              <p className="muted">Running text classification and checking common social-engineering signals.</p>
            </div>
          )}
          {analysis && (
            <div className="report">
              <div className={`verdict-icon ${isScam ? "danger" : "caution"}`} aria-hidden="true">{isScam ? "!" : "✓"}</div>
              <p className="eyebrow">MODEL CLASSIFICATION</p>
              <h3 className={isScam ? "verdict-danger" : "verdict-caution"}>{isScam ? "Scam pattern detected" : "No scam pattern detected"}</h3>
              <p className="muted verdict-copy">
                {isScam
                  ? "This message resembles examples labelled as scams by the trained model. Avoid clicking links or sending money until verified."
                  : "The model did not classify this message as a scam. This is not proof that the sender or message is legitimate."}
              </p>
              <div className="report-divider" />
              <div className="signals-heading">
                <h4>Risk indicators</h4>
                <span>{analysis.indicator_count ?? analysis.risk_indicators?.length ?? 0} found</span>
              </div>
              {analysis.risk_indicators?.length ? (
                <div className="signals-list">
                  {analysis.risk_indicators.map((signal, index) => (
                    <div className="signal" key={`${signal.title}-${index}`}>
                      <span className={`signal-dot severity-${signal.severity}`} />
                      <div><strong>{signal.title}</strong><p>{signal.detail}</p></div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-signals">No configured keyword signals were found. The model can still make mistakes.</p>
              )}
              <div className="safety-note"><strong>Next step</strong><p>Verify the sender through an official app or number you already trust. Never share OTPs, UPI PINs, or passwords.</p></div>
            </div>
          )}
          {error && !analysis && !loading && (
            <div className="empty-state error-state">
              <div className="verdict-icon danger" aria-hidden="true">×</div>
              <h3>Analysis unavailable</h3>
              <p className="muted">{error}</p>
            </div>
          )}
        </aside>
      </div>
    </section>
  );
}

export default Predictor;

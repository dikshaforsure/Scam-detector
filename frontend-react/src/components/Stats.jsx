function Stats() {
  const workflow = [
    { number: "01", title: "Normalize the text", detail: "The message is transformed into text features using a TF-IDF vectorizer." },
    { number: "02", title: "Classify the message", detail: "A supervised linear classifier predicts whether the text resembles scam examples." },
    { number: "03", title: "Explain warning signals", detail: "Readable checks highlight urgency, credential requests, links, and payment pressure." },
  ];

  return (
    <section className="method-section" id="method">
      <div className="section-heading">
        <div>
          <p className="eyebrow">UNDER THE HOOD</p>
          <h2>A transparent detection workflow</h2>
          <p className="muted">NLP classification is combined with rule-based indicators to support—not replace—your judgement.</p>
        </div>
        <span className="method-chip">TF-IDF + Linear classifier</span>
      </div>
      <div className="workflow-grid">
        {workflow.map((item) => (
          <article className="workflow-card" key={item.number}>
            <span className="workflow-number">{item.number}</span>
            <h3>{item.title}</h3>
            <p>{item.detail}</p>
          </article>
        ))}
      </div>
      <div className="dataset-note">
        <div className="dataset-icon" aria-hidden="true">⌘</div>
        <div>
          <h3>Measure quality, don't guess it</h3>
          <p>The training utility writes a held-out evaluation report with scam precision, recall, F1, and a confusion matrix. Report results for your actual split; no fixed accuracy is displayed here.</p>
        </div>
      </div>
      <div className="category-section">
        <p className="eyebrow">COMMON SOCIAL-ENGINEERING THEMES</p>
        <div className="category-chips">
          {["Credential harvesting", "Urgency & threats", "Prize / reward bait", "Payment pressure", "Suspicious links", "Impersonation"].map((category) => (
            <span key={category}>{category}</span>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Stats;

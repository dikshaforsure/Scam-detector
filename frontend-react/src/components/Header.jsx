function Header() {
  return (
    <header className="hero" id="top">
      <nav className="topbar" aria-label="Main navigation">
        <a className="brand" href="#top" aria-label="Scam Detector home">
          <span className="brand-mark" aria-hidden="true">S</span>
          <span>Scam<span className="brand-accent">Detector</span></span>
        </a>
        <div className="nav-links">
          <a href="#analyze">Analyze</a>
          <a href="#method">How it works</a>
          <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer">API docs ↗</a>
        </div>
        <span className="system-status"><span className="status-dot" /> NLP screening</span>
      </nav>

      <div className="hero-content">
        <div className="hero-copy">
          <p className="eyebrow"><span className="status-dot" /> MESSAGE THREAT INTELLIGENCE</p>
          <h1>Spot the signal.<br /><span>Stop the scam.</span></h1>
          <p className="hero-description">
            Inspect suspicious SMS, email, and payment messages with NLP-based classification and clear, human-readable risk indicators.
          </p>
          <a className="hero-cta" href="#analyze">Analyze a message <span aria-hidden="true">↓</span></a>
          <p className="hero-footnote">Built for awareness and defensive screening. Always verify high-stakes messages independently.</p>
        </div>
        <div className="hero-visual" aria-label="Illustration of message security signals">
          <div className="orb orb-one" />
          <div className="orb orb-two" />
          <div className="security-card">
            <div className="security-card-top"><span className="mini-shield">⌑</span><span>THREAT MONITOR</span><span className="live-indicator">ACTIVE</span></div>
            <div className="security-score"><span className="score-ring">NLP</span><div><strong>Message analysis</strong><p>Text features + risk signals</p></div></div>
            <div className="signal-bars"><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /><span /></div>
            <div className="security-row"><span className="row-dot" /> TF-IDF text features <strong>READY</strong></div>
            <div className="security-row"><span className="row-dot teal" /> Social-engineering checks <strong>READY</strong></div>
            <div className="security-card-bottom"><span>SCAM DETECTOR</span><span>DEFENSIVE MODE / 01</span></div>
          </div>
        </div>
      </div>
      <div className="trust-strip">
        <div><strong>01</strong><span>Text classification</span></div>
        <div><strong>02</strong><span>Explainable indicators</span></div>
        <div><strong>03</strong><span>Privacy-first workflow</span></div>
      </div>
    </header>
  );
}

export default Header;

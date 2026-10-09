function Stats() {
  return (
    <div className="stats">

      <h2>Model Performance</h2>

      <div className="cards">

        <div className="card">
          <h3>Naive Bayes</h3>
          <p>98.33%</p>
        </div>

        <div className="card">
          <h3>Logistic Regression</h3>
          <p>98.15%</p>
        </div>

        <div className="card best">
          <h3>SVM</h3>
          <p>98.36%</p>
        </div>

      </div>

      <h2>Scam Categories</h2>

      <ul>
        <li>UPI Fraud</li>
        <li>OTP Scam</li>
        <li>Lottery Scam</li>
        <li>Reward Scam</li>
        <li>Bank KYC Fraud</li>
        <li>Payment Request Scam</li>
        <li>Fake Job Offers</li>
      </ul>

    </div>
  );
}

export default Stats;
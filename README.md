# 🛡️ Scam-Detector : Scam Message Detection System

An AI-powered cybersecurity application that detects fraudulent SMS, phishing messages, OTP scams, UPI frauds, lottery scams, and other malicious text messages using Machine Learning and Natural Language Processing (NLP).

The system combines a React frontend, FastAPI backend, and an SVM machine learning model trained on scam message data to classify messages as **Safe** or **Scam**.

---

## 🚀 Features

* Detects scam and phishing messages
* Machine Learning based classification
* Natural Language Processing (NLP)
* TF-IDF text vectorization
* Support Vector Machine (SVM) classifier
* Interactive React user interface
* FastAPI backend API
* Real-time prediction results
* Cybersecurity-themed dashboard

---

## 🏗️ Project Architecture

User Input
↓
React Frontend
↓
FastAPI Backend
↓
TF-IDF Vectorizer
↓
SVM Machine Learning Model
↓
Prediction Result

---

## 🧠 Machine Learning Pipeline

### Data Preprocessing

* Text cleaning
* Lowercase conversion
* Removal of punctuation
* Tokenization
* Stopword removal

### Feature Extraction

TF-IDF (Term Frequency – Inverse Document Frequency)

### Models Evaluated

| Model               | Accuracy |
| ------------------- | -------- |
| Naive Bayes         | 98.33%   |
| Logistic Regression | 98.15%   |
| SVM                 | 98.36%   |

### Best Performing Model

Support Vector Machine (SVM)

Accuracy: **98.36%**

---

## 🛠️ Technology Stack

### Frontend

* React.js
* JavaScript
* HTML5
* CSS3
* Fetch API

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Machine Learning

* Python
* Scikit-Learn
* Pandas
* NumPy
* TF-IDF Vectorizer
* Support Vector Machine (SVM)

---

## 📂 Project Structure

project/

├── backend/

│ ├── main.py

│ ├── model.pkl

│ └── vectorizer.pkl

│

├── frontend-react/

│ ├── src/

│ │ ├── components/

│ │ │ ├── Header.jsx

│ │ │ ├── Predictor.jsx

│ │ │ ├── Stats.jsx

│ │ │ └── Footer.jsx

│ │

│ ├── App.jsx

│ ├── App.css

│ └── main.jsx

│

└── README.md

---

## ⚙️ Installation

### Clone Repository

```bash
git clone <repository-link>
cd project
```

### Backend Setup

```bash
conda activate ml_env

cd backend

uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend Setup

```bash
cd frontend-react

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 🎯 Scam Categories Detected

* OTP Fraud
* UPI Fraud
* Lottery Scam
* Reward Scam
* Bank KYC Fraud
* Fake Payment Requests
* Phishing Messages
* Fake Job Offers

---

## 🔮 Future Enhancements

* BERT Fine-Tuning
* Explainable AI (XAI)
* Confidence Score Display
* Multilingual Scam Detection
* Android Application
* Real-Time SMS Monitoring
* Email Scam Detection
* Cyber Threat Intelligence Dashboard

---

## 📊 Results

The Support Vector Machine (SVM) model achieved an accuracy of **98.36%**, outperforming Naive Bayes and Logistic Regression models on the scam message classification dataset.

---

## 👩‍💻 Author

Diksha Anand

Computer Engineering Student

Machine Learning • NLP • Cybersecurity • Web Development

---

## 📜 License

This project is developed for educational and research purposes.

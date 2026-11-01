📂 Project Overview:

This project implements an advanced fraud detection system for financial transactions by combining deep learning techniques and machine learning models. It follows a structured pipeline to identify anomalies, analyze sequential patterns, and accurately classify fraudulent behavior.

⚙️ Technologies Used:

Python 🐍
TensorFlow / Keras 🤖 (Neural Networks: Autoencoder & LSTM)
Scikit-learn 📊 (Random Forest & Evaluation Metrics)
Pandas & NumPy 📁 (Data Manipulation)
Matplotlib & Seaborn 📈 (Data Visualization)

🧪 Testing Process:

New transactions pass through:

Autoencoder → Detects anomalies.
LSTM → Evaluates sequential behavior.
Random Forest → Final classification decision.
Reconstruction Error serves as a key indicator for anomaly detection.

Transactions flagged as high-risk undergo deeper analysis through the LSTM and Random Forest layers.

✅ Key Takeaways:

Layered AI Strategy: Autoencoder → LSTM → Random Forest for comprehensive fraud detection.
Anomaly Detection: Captures outliers and new fraud patterns.
Sequential Analysis: LSTM captures evolving transaction behaviors.
Robust Classification: Random Forest reduces false positives and improves accuracy.

Dataset from:https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

# **Stock Price Prediction with MLOps & Data Drift Detection**

This project implements a complete MLOps workflow to predict stock prices and monitor data drift over time. It uses LSTM models, DVC for data versioning, BentoML for serving, and GKE for deployment. Weekly drift detection is integrated using Evidently.

This project is based on the code from [A guide to MLOps](https://mlops.swiss-ai-center.ch/).

---

## 🚀 Overview

- Predicts **next 5 days** of stock prices using **LSTM**
- Uses **5 years** of NASDAQ stock data (20 tech companies)
- Full MLOps workflow: data prep → training → evaluation → deployment
- Weekly model updates and drift reports generated via CI/CD

---

## 📂 Main Features

### **Data Pipeline**

- Raw data collected from nasdaq.com
- Cleaning, normalization, sliding-window sequences
- Versioned with **DVC** and stored in **S3**

### **Model**

- LSTM sequence model
- Enhanced features: SMA/EMA, volatility proxy, volume change, ratios
- Metrics: MAE, RMSE, R²

### **Performance**

- Initial MAE: **1.87** → Improved to **0.66**
- R² remains low due to stock market volatility

---

## 🔍 Data Drift Detection

Integrated using **Evidently**:

- Compares _current_ vs. _candidate_ datasets weekly
- Statistical tests (KS, Chi-square)
- Generates HTML & JSON drift reports
- Pipeline posts drift summary + model comparison
- Artificial drift branch included for testing

---

## ⚙️ CI/CD Workflow

Powered by GitHub Actions + Kubernetes runner:

### **train-and-report**

- Runs DVC pipeline
- Trains model and compares metrics with main
- Generates CML report in PR comments
- Runs drift analysis

### **publish-and-deploy**

- Builds BentoML service
- Builds/pushes Docker image
- Updates GKE deployment via rolling update

---

## ☁️ Deployment

- BentoML for model serving
- Docker container
- Hosted on **Google Kubernetes Engine**
- Supports horizontal scaling

---

## Useful commands

```bash
python3.12 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip freeze --local --all > requirements-freeze.txt

dvc pull
dvc repro

docker run --rm -p 3000:3000 celestial-bodies-classifier:latest

kubectl apply -f kubernetes/runner.yaml
kubectl get pods
kubectl delete -f kubernetes/runner.yaml
```

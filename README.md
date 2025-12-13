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

# Serve the model locally
bentoml serve --working-dir ./src serve:FinancialForecastService

# Build and run Docker container locally
bentoml build src
bentoml containerize stock-ml:latest --image-tag stock-ml:latest
docker run --rm -p 3000:3000 stock-ml:latest

gcloud container clusters create \
    --machine-type=e2-standard-2 \
    --num-nodes=1 \
    --zone=$GCP_K8S_CLUSTER_ZONE \
    $GCP_K8S_CLUSTER_NAME

kubectl get namespaces
kubectl get nodes

kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml

kubectl create secret generic github-runner-pat --from-literal=token=$GH_RUNNER_PAT
kubectl apply -f kubernetes/runner.yaml
kubectl get pods
kubectl delete -f kubernetes/runner.yaml

# Delete cluster after use
gcloud container clusters delete $GCP_K8S_CLUSTER_NAME --zone=$GCP_K8S_CLUSTER_ZONE
```


Predict stock request:

```json
{
  "stock_data": [
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05},
    {"Return": 0.12, "SMA_5": 0.10, "SMA_10": 0.08, "EMA_5": 0.11, "High_Low_Spread": 1.5, "Open_Close_Ratio": 1.002, "Volume_Change": 0.05}
  ]
}
```
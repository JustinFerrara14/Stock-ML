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

## 📦 Usage

To get a prediction from the deployed model, you can download a CSV file of stock data (e.g., from [nasdaq.com](https://www.nasdaq.com)) and convert it to JSON input format using the [./src/generateInput.py](./src/generateInput.py) script. An example of CSV file is provided at [./doc/samplePrediction/stock_data.csv](./doc/samplePrediction/stock_data.csv) which as been downloaded [nasdaq.com](https://www.nasdaq.com) for NVIDIA Corporation (NVDA) on December 13, 2025.

```bash
python3 src/generateInput.py
```

This will create a JSON file at [./doc/samplePrediction/stock_data.json](./doc/samplePrediction/stock_data.json). You can then send this JSON content to the deployed model's REST API endpoint using a tool like `curl` or using the FastAPI Swagger UI.

After submitting the JSON input to the model, the model responded with the following JSON output containing the predicted stock prices for the next 5 days:

```json
{
  "predicted_return_next5": [
    0.37401431798934937,
    -0.4399341940879822,
    -0.09452365338802338,
    -0.5075818300247192,
    -0.22593094408512115
  ]
}
```

The predicted returns can be converted back to stock prices using the last known stock price from the input data and the formula:
- Predicted Price for `15.12.2025`: 175.02 * (1 + 0.3740/100) = **175.65**
- Predicted Price for `16.12.2025`: 175.65 * (1 - 0.4399/100) = **174.88**
- Predicted Price for `17.12.2025`: 174.88 * (1 - 0.0945/100) = **174.71**
- Predicted Price for `18.12.2025`: 174.71 * (1 - 0.5076/100) = **173.84**
- Predicted Price for `19.12.2025`: 173.84 * (1 - 0.2259/100) = **173.45**

---

## 🛠️ Useful commands

The following commands can be used to set up the environment, run the DVC pipeline, serve the model locally, build and run the Docker container, and deploy to GKE.

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

# Get external IP in "LoadBalancer Ingress" field
kubectl describe services stock-ml

kubectl create secret generic github-runner-pat --from-literal=token=$GH_RUNNER_PAT
kubectl apply -f kubernetes/runner.yaml
kubectl get pods
kubectl delete -f kubernetes/runner.yaml

# Delete cluster after use
gcloud container clusters delete $GCP_K8S_CLUSTER_NAME --zone=$GCP_K8S_CLUSTER_ZONE
```
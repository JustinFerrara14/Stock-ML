# Stock-ML

This repository contains the code and documentation for the project "Stock-ML", in the context of the "TSM-MachLeData" course.

This repository is based on the code from [A guide to MLOps](https://mlops.swiss-ai-center.ch/).

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
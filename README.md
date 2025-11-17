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

bentoml containerize stock_ml:latest --image-tag stock-ml:latest
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
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000},
    {"Open": 260.1, "High": 264.0, "Low": 259.0, "Volume": 38200000}
  ]
}
```
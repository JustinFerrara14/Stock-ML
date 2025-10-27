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

kubectl apply -f kubernetes/runner.yaml
kubectl get pods
kubectl delete -f kubernetes/runner.yaml
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
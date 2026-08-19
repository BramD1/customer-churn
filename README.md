# customer-churn

Telco customer churn prediction: an XGBoost model (tracked with MLflow) served through a
combined FastAPI + Gradio app. 

All credits to this repository to learn how to deploy ML model:
https://github.com/anesriad/Telco-Customer-Churn-ML/blob/main/dockerfile

## Project layout

- `src/data/`, `src/features/` — data loading and feature engineering used at training time
- `src/models/train.py` — trains the XGBoost model and logs it (+ its feature schema) to MLflow
- `src/serving/inference.py` — loads the bundled model and reproduces training-time feature
  engineering for incoming requests
- `src/app/main.py` — FastAPI app (`/predict`) with a Gradio UI mounted at `/ui`
- `src/serving/model/` — the model artifacts actually bundled into the Docker image
- `scripts/export_model.py` — copies the latest MLflow training run into `src/serving/model/`

## Run locally without Docker

```bash
pip install -r requirements-serving.txt
uvicorn src.app.main:app --reload --port 8000
```

Then visit `http://localhost:8000/ui` for the Gradio form, or `http://localhost:8000/docs`
for the FastAPI OpenAPI docs.

## Run with Docker

```bash
docker build -t customer-churn .
docker run -p 8000:8000 customer-churn
```

Visit `http://localhost:8000/ui` or `http://localhost:8000/docs`.

## Retraining and redeploying the model

1. Train: `python -m src.models.train` (however you currently invoke it), which now also logs
   `feature_columns.txt` alongside the model.
2. Export the new run into the serving directory: `python scripts/export_model.py`
3. Rebuild the Docker image so the new model is bundled: `docker build -t customer-churn .`

## CI / publishing the image

[.github/workflows/ci.yml](.github/workflows/ci.yml) builds the image and pushes it to Docker
Hub on every push to `main`. Update the `tags:` value to your own Docker Hub repo, and add
`DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` secrets under this repo's Settings > Secrets and
variables > Actions before it will run successfully.

## Deploying the built image

Once the image builds and pushes successfully, any container host that can pull from Docker
Hub works: point it at your image, map port 8000, and it serves both the API and the UI.

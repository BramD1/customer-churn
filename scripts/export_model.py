"""
Copy the most recently trained MLflow model into src/serving/model/, the
directory bundled into the Docker image for serving.

Run after training:
    python scripts/export_model.py
"""

import glob
import os
import shutil

SOURCE_GLOB = "mlruns/*/models/*/artifacts"
DEST_DIR = os.path.join("src", "serving", "model")
FILES_TO_COPY = [
    "MLmodel",
    "model.ubj",
    "conda.yaml",
    "python_env.yaml",
    "requirements.txt",
    "feature_columns.txt",
]


def main():
    candidates = glob.glob(SOURCE_GLOB)
    if not candidates:
        raise SystemExit(f"No trained model found matching {SOURCE_GLOB!r}. Run training first.")

    latest = max(candidates, key=os.path.getmtime)
    print(f"Exporting model from: {latest}")

    os.makedirs(DEST_DIR, exist_ok=True)
    for name in FILES_TO_COPY:
        src = os.path.join(latest, name)
        if not os.path.exists(src):
            raise SystemExit(
                f"Missing expected artifact {name!r} in {latest}. "
                "Was the model trained with the current src/models/train.py?"
            )
        shutil.copy(src, os.path.join(DEST_DIR, name))
        print(f"  copied {name}")

    print(f"Done. Model ready for the Docker image at {DEST_DIR}/")


if __name__ == "__main__":
    main()

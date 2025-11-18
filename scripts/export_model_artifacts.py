"""
Utility script to convert the trained scikit-learn artifacts into lightweight
JSON representations that can be used in environments where large binary
dependencies (numpy, scipy, scikit-learn) would exceed platform limits.

Usage:
    python scripts/export_model_artifacts.py

The script writes the following files inside `models/`:
    - random_forest_compact.json
    - scaler_params.json

These JSON files contain everything needed for runtime inference without
pulling in the original heavy dependencies.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def export_random_forest() -> None:
    model_path = MODELS_DIR / "random_forest_model.pkl"
    with model_path.open("rb") as f:
        model = pickle.load(f)

    trees = []
    for estimator in model.estimators_:
        tree = estimator.tree_
        trees.append(
            {
                "children_left": tree.children_left.tolist(),
                "children_right": tree.children_right.tolist(),
                "feature": tree.feature.tolist(),
                "threshold": tree.threshold.tolist(),
                "value": tree.value[:, 0, :].tolist(),
            }
        )

    payload = {
        "trees": trees,
        "classes": model.classes_.tolist(),
        "n_features": int(model.n_features_in_),
        "feature_names": model.feature_names_in_.tolist(),
    }

    output_path = MODELS_DIR / "random_forest_compact.json"
    output_path.write_text(json.dumps(payload))
    print(f"Saved compact random forest to {output_path.relative_to(ROOT)}")


def export_scaler() -> None:
    scaler_path = MODELS_DIR / "standard_scaler.pkl"
    with scaler_path.open("rb") as f:
        scaler = pickle.load(f)

    payload = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist(),
        "n_features": int(scaler.n_features_in_),
    }
    output_path = MODELS_DIR / "scaler_params.json"
    output_path.write_text(json.dumps(payload))
    print(f"Saved scaler parameters to {output_path.relative_to(ROOT)}")


def main() -> None:
    export_random_forest()
    export_scaler()


if __name__ == "__main__":
    main()


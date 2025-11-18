from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"

NUMERICAL_COLUMNS: Sequence[str] = (
    "Account length",
    "Number vmail messages",
    "Total day minutes",
    "Total day calls",
    "Total eve minutes",
    "Total eve calls",
    "Total night minutes",
    "Total night calls",
    "Total intl minutes",
    "Total intl calls",
    "Customer service calls",
)

FEATURE_ORDER: Sequence[str] = (
    "International plan",
    "Voice mail plan",
    *NUMERICAL_COLUMNS,
)


def _normalize_bool(value: str) -> int:
    normalized = value.strip().lower()
    if normalized in {"yes", "true", "1", "y"}:
        return 1
    if normalized in {"no", "false", "0", "n"}:
        return 0
    raise ValueError(f"Unsupported boolean-like value: {value!r}")


class RandomForestPredictor:
    def __init__(self) -> None:
        model_payload = json.loads((MODELS_DIR / "random_forest_compact.json").read_text())
        scaler_payload = json.loads((MODELS_DIR / "scaler_params.json").read_text())

        if model_payload["feature_names"] != list(FEATURE_ORDER):
            raise ValueError("Model feature order does not match expected schema.")

        self._trees = model_payload["trees"]
        self._classes = model_payload["classes"]

        self._scaler_mean = scaler_payload["mean"]
        self._scaler_scale = scaler_payload["scale"]

    def predict_from_form(self, form_data: Dict[str, str]) -> int:
        features = self._build_feature_vector(form_data)
        return self._predict(features)

    def _build_feature_vector(self, form_data: Dict[str, str]) -> List[float]:
        categorical = [
            _normalize_bool(form_data["international_plan"]),
            _normalize_bool(form_data["voice_mail_plan"]),
        ]

        numerical_values = [
            float(form_data["account_length"]),
            float(form_data["number_vmail_messages"]),
            float(form_data["total_day_minutes"]),
            float(form_data["total_day_calls"]),
            float(form_data["total_eve_minutes"]),
            float(form_data["total_eve_calls"]),
            float(form_data["total_night_minutes"]),
            float(form_data["total_night_calls"]),
            float(form_data["total_intl_minutes"]),
            float(form_data["total_intl_calls"]),
            float(form_data["customer_service_calls"]),
        ]

        scaled = self._scale_values(numerical_values)
        return categorical + scaled

    def _scale_values(self, values: Iterable[float]) -> List[float]:
        return [
            (val - mean) / scale
            for val, mean, scale in zip(values, self._scaler_mean, self._scaler_scale)
        ]

    def _predict(self, features: Sequence[float]) -> int:
        votes = [0.0 for _ in self._classes]
        for tree in self._trees:
            tree_vote = self._traverse_tree(tree, features)
            for idx, value in enumerate(tree_vote):
                votes[idx] += value
        return self._classes[votes.index(max(votes))]

    @staticmethod
    def _traverse_tree(tree: Dict[str, List[Any]], features: Sequence[float]) -> Sequence[float]:
        node = 0
        children_left = tree["children_left"]
        children_right = tree["children_right"]
        feature_index = tree["feature"]
        thresholds = tree["threshold"]
        values = tree["value"]

        while children_left[node] != -1:
            idx = feature_index[node]
            threshold = thresholds[node]
            if features[idx] <= threshold:
                node = children_left[node]
            else:
                node = children_right[node]
        return values[node]


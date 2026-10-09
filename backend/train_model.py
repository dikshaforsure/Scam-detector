"""Reproducible baseline training and evaluation for Scam Detector."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pickle
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dataset"
ARTIFACT_DIR = Path(__file__).resolve().parent


def normalise_columns(frame: pd.DataFrame) -> pd.DataFrame:
    names = {str(column).strip().lower(): column for column in frame.columns}
    text_col = next((names[key] for key in ("text", "message", "sms", "content") if key in names), None)
    label_col = next((names[key] for key in ("scam", "label", "target", "is_scam") if key in names), None)
    if text_col is None or label_col is None:
        raise ValueError(f"Could not find text and label columns. Found: {list(frame.columns)}")
    result = frame[[text_col, label_col]].copy()
    result.columns = ["text", "label"]
    result["text"] = result["text"].fillna("").astype(str).str.strip()
    label_map = {"0": 0, "1": 1, "safe": 0, "ham": 0, "legitimate": 0, "legit": 0,
                 "scam": 1, "spam": 1, "fraud": 1, "phishing": 1}
    result["label"] = result["label"].map(lambda value: label_map.get(str(value).strip().lower(), value))
    result["label"] = pd.to_numeric(result["label"], errors="coerce")
    result = result[result["text"].ne("") & result["label"].isin([0, 1])]
    result["label"] = result["label"].astype(int)
    return result.drop_duplicates(subset=["text", "label"]).reset_index(drop=True)


def load_datasets(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        if not path.exists():
            print(f"Skipping missing dataset: {path}", file=sys.stderr)
            continue
        try:
            frames.append(normalise_columns(pd.read_csv(path, encoding_errors="replace")))
        except Exception as exc:
            print(f"Skipping {path}: {exc}", file=sys.stderr)
    if not frames:
        raise FileNotFoundError("No usable CSV datasets found. Provide --data paths with text and scam/label columns.")
    merged = pd.concat(frames, ignore_index=True)
    label_counts = merged.groupby("text")["label"].nunique()
    conflicting = set(label_counts[label_counts > 1].index)
    if conflicting:
        print(f"Excluding {len(conflicting)} texts with conflicting labels.", file=sys.stderr)
        merged = merged[~merged["text"].isin(conflicting)]
    return merged.drop_duplicates(subset=["text"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", nargs="*", type=Path, help="CSV paths; defaults to CSV files in ../dataset")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--model", choices=["svm", "logistic"], default="svm")
    args = parser.parse_args()
    if not 0.1 <= args.test_size <= 0.4:
        parser.error("--test-size should be between 0.1 and 0.4")
    paths = args.data if args.data else sorted(DATA_DIR.glob("*.csv"))
    data = load_datasets(paths)
    if data["label"].nunique() != 2 or data["label"].value_counts().min() < 2:
        raise ValueError("Need at least two examples of each class for a stratified split.")
    train_x, test_x, train_y, test_y = train_test_split(
        data["text"], data["label"], test_size=args.test_size, random_state=args.seed, stratify=data["label"])
    classifier = LinearSVC(class_weight="balanced") if args.model == "svm" else LogisticRegression(max_iter=2000, class_weight="balanced")
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, strip_accents="unicode", sublinear_tf=True,
                                  ngram_range=(1, 2), min_df=1, max_features=250_000)),
        ("classifier", classifier),
    ])
    pipeline.fit(train_x, train_y)
    predicted = pipeline.predict(test_x)
    report = classification_report(test_y, predicted, labels=[0, 1], target_names=["legitimate", "scam"],
                                   output_dict=True, zero_division=0)
    metrics = {
        "model": args.model, "seed": args.seed, "rows_after_deduplication": int(len(data)),
        "train_rows": int(len(train_x)), "test_rows": int(len(test_x)),
        "class_counts": {str(k): int(v) for k, v in data["label"].value_counts().sort_index().items()},
        "accuracy": float(accuracy_score(test_y, predicted)),
        "scam_precision": float(precision_score(test_y, predicted, pos_label=1, zero_division=0)),
        "scam_recall": float(recall_score(test_y, predicted, pos_label=1, zero_division=0)),
        "scam_f1": float(f1_score(test_y, predicted, pos_label=1, zero_division=0)),
        "confusion_matrix_labels_0_then_1": confusion_matrix(test_y, predicted, labels=[0, 1]).tolist(),
        "classification_report": report,
        "note": "Metrics are for this held-out split only; dataset leakage, source bias, and real-world drift may affect production results.",
    }
    ARTIFACT_DIR.mkdir(exist_ok=True)
    fitted = pipeline.named_steps
    with (ARTIFACT_DIR / "model.pkl").open("wb") as handle:
        pickle.dump(fitted["classifier"], handle)
    with (ARTIFACT_DIR / "vectorizer.pkl").open("wb") as handle:
        pickle.dump(fitted["tfidf"], handle)
    with (ARTIFACT_DIR / "evaluation.json").open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import math
from pathlib import Path


def euclidean_distance(vec1: list[float], vec2: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def distance_to_similarity(distance: float) -> float:
    """
    По условию:
    нулевое расстояние -> единичная мера близости
    """
    return 1.0 / (1.0 + distance)


def classify_symbol(
    unknown_features: dict[str, float],
    reference_db: dict[str, dict[str, float]],
    feature_columns: list[str],
) -> list[tuple[str, float]]:
    unknown_vec = [float(unknown_features[col]) for col in feature_columns]

    hypotheses: list[tuple[str, float]] = []

    for symbol, ref_features in reference_db.items():
        ref_vec = [float(ref_features[col]) for col in feature_columns]
        dist = euclidean_distance(unknown_vec, ref_vec)
        sim = distance_to_similarity(dist)
        hypotheses.append((symbol, sim))

    hypotheses.sort(key=lambda item: item[1], reverse=True)
    return hypotheses


def build_recognized_string(all_hypotheses: list[list[tuple[str, float]]]) -> str:
    return "".join(h[0][0] for h in all_hypotheses if h)


def evaluate_recognition(recognized: str, truth: str) -> dict[str, float | int]:
    if len(recognized) != len(truth):
        raise ValueError(
            f"Длины строк не совпадают: recognized={len(recognized)}, truth={len(truth)}"
        )

    correct = sum(1 for a, b in zip(recognized, truth) if a == b)
    total = len(truth)
    errors = total - correct
    accuracy_percent = (correct / total * 100.0) if total > 0 else 0.0

    return {
        "total": total,
        "correct": correct,
        "errors": errors,
        "accuracy_percent": accuracy_percent,
    }


def save_hypotheses_text(
    all_hypotheses: list[list[tuple[str, float]]],
    output_path: Path,
) -> None:
    lines = []
    for i, hypotheses in enumerate(all_hypotheses, start=1):
        parts = [f'("{symbol}", {score:.6f})' for symbol, score in hypotheses]
        lines.append(f"{i}: [{', '.join(parts)}]")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def save_recognition_report(
    recognized: str,
    truth: str,
    metrics: dict[str, float | int],
    output_path: Path,
) -> None:
    text = (
        f"Ground truth: {truth}\n"
        f"Recognized:   {recognized}\n"
        f"Total:        {metrics['total']}\n"
        f"Correct:      {metrics['correct']}\n"
        f"Errors:       {metrics['errors']}\n"
        f"Accuracy, %:  {metrics['accuracy_percent']:.2f}\n"
    )
    output_path.write_text(text, encoding="utf-8")


def save_experiment_summary_csv(
    rows: list[dict[str, object]],
    output_path: Path,
) -> None:
    if not rows:
        raise ValueError("Нет строк для experiment summary.")

    columns = list(rows[0].keys())

    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(columns)
        for row in rows:
            writer.writerow([row[col] for col in columns])
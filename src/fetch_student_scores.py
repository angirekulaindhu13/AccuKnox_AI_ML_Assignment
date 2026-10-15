import math
from pathlib import Path

import matplotlib.pyplot as plt
import requests


API_URL = "http://127.0.0.1:8000/students"


def fetch_students():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    media_type = content_type.split(";", maxsplit=1)[0].strip().lower()
    if media_type != "application/json":
        raise ValueError(f"Expected a JSON response, received {content_type!r}")

    students = response.json()
    if not isinstance(students, list) or not students:
        raise ValueError("Expected a non-empty JSON list of students")

    validated_students = []
    for index, student in enumerate(students):
        if not isinstance(student, dict):
            raise ValueError(f"Student record {index} must be a JSON object")

        name = student.get("student_name")
        score = student.get("test_score")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Student record {index} has no valid student_name")
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"Student record {index} has a non-numeric test_score")
        if not math.isfinite(score):
            raise ValueError(f"Student record {index} has a non-finite test_score")

        validated_students.append((name.strip(), score))

    return validated_students


def main():
    students = fetch_students()
    names = [name for name, _ in students]
    scores = [score for _, score in students]
    average_score = sum(scores) / len(scores)

    print(f"Number of students: {len(students)}")
    print(f"Average test score: {average_score:.2f}")

    figure, axis = plt.subplots(figsize=(10, 6))
    axis.bar(names, scores, color="steelblue")
    axis.set_title("Synthetic Student Test Scores")
    axis.set_xlabel("Student")
    axis.set_ylabel("Test score")
    axis.set_ylim(bottom=0)
    axis.tick_params(axis="x", labelrotation=20)
    figure.tight_layout()

    output_path = Path(__file__).resolve().parent.parent / "data" / "output" / "student_scores.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    plt.close(figure)
    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    main()
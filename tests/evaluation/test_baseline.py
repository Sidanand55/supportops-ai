import json
from pathlib import Path

DATASET_PATH = (
    Path(__file__).parents[2]
    / "app"
    / "evaluation"
    / "datasets"
    / "baseline.json"
)


def test_baseline_dataset_exists():

    assert DATASET_PATH.exists()


def test_baseline_dataset_is_valid():

    with open(DATASET_PATH, encoding="utf-8") as file:
        dataset = json.load(file)

    assert len(dataset) >= 15

    for case in dataset:

        assert "id" in case
        assert "category" in case
        assert "input" in case
        assert "expected_behavior" in case
        assert "must_not_contain" in case


def test_baseline_ids_are_unique():

    with open(DATASET_PATH, encoding="utf-8") as file:
        dataset = json.load(file)

    ids = [case["id"] for case in dataset]

    assert len(ids) == len(set(ids))
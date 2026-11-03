import asyncio
import json
from pathlib import Path

from app.services.llm.service import generate_response

DATASET_PATH = Path(__file__).parent / "datasets" / "baseline.json"


async def run_evaluations():
    with open(DATASET_PATH, "r") as file:
        test_cases = json.load(file)

    results = []

    for test_case in test_cases:
        response = await generate_response(test_case["input"])

        violations = []

        for phrase in test_case["must_not_contain"]:
            if phrase.lower() in response.lower():
                violations.append(phrase)

        passed = len(violations) == 0

        results.append(
            {
                "id": test_case["id"],
                "category": test_case["category"],
                "response": response,
                "passed": passed,
                "violations": violations,
            }
        )

        print(f"{test_case['id']}: {'PASS' if passed else 'FAIL'}")

    total = len(results)
    passed = sum(r["passed"] for r in results)

    print("\nEvaluation Summary")
    print("------------------")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Pass Rate: {passed / total * 100:.2f}%")

    return results


if __name__ == "__main__":
    asyncio.run(run_evaluations())

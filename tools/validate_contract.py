#!/usr/bin/env python3
"""Validate EG-Architecture exchange contract and synthetic fixtures.

Install: python -m pip install -r requirements-dev.txt
Run:     python tools/validate_contract.py
"""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "v1" / "contract.schema.json"
EXAMPLES_PATH = ROOT / "contracts" / "v1" / "examples.json"

def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    examples = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert len(examples) == 5, "Expected all five message types"
    kinds = {item["messageType"] for item in examples}
    assert kinds == {
        "price.observation", "product.match", "receipt.line",
        "comparison.result", "recipe.draft"
    }
    for i, item in enumerate(examples):
        errors = sorted(validator.iter_errors(item), key=lambda e: str(e.path))
        assert not errors, f"Valid fixture {i} failed: {[e.message for e in errors]}"

    negatives = {}
    item = copy.deepcopy(examples[0])
    item["payload"]["priceCents"] = -1
    negatives["negative cents"] = item

    item = copy.deepcopy(examples[0])
    item["payload"]["scope"]["storeId"] = None
    negatives["store confirmed without ID"] = item

    item = copy.deepcopy(examples[0])
    item["payload"]["article"]["organic"] = "maybe"
    negatives["invalid organic status"] = item

    item = copy.deepcopy(examples[0])
    item["payload"]["source"]["rightsStatus"] = "KNOWN_LICENCED_BY_GUESS"
    negatives["invented rights status"] = item

    item = copy.deepcopy(examples[2])
    del item["payload"]["rawText"]
    negatives["missing receipt raw text"] = item

    item = copy.deepcopy(examples[4])
    item["payload"]["flags"]["considerOffers"] = "false"
    negatives["nonboolean recipe flag"] = item

    item = copy.deepcopy(examples[4])
    item["payload"]["portionCount"] = 0
    negatives["zero recipe portions"] = item

    for case, item in negatives.items():
        assert list(validator.iter_errors(item)), f"Invalid case incorrectly accepted: {case}"
    print(f"PASS: schema valid; {len(examples)} positive and {len(negatives)} negative cases")

if __name__ == "__main__":
    main()

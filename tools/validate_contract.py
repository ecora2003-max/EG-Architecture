#!/usr/bin/env python3
"""Validate both independent EG interchange schema versions, synthetic fixtures,
and deliberately invalid cases. Run: python tools/validate_contract.py
"""
import copy
import json
from datetime import datetime
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
EXPECTED = {
    "v1": {"price.observation", "product.match", "receipt.line",
           "comparison.result", "recipe.draft"},
    "v1.1": {"price.observation", "product.match", "receipt.line",
             "comparison.result", "recipe.draft",
             "shopping.need.projection", "shopping.purchase.suggestion",
             "shopping.offer.interest", "shopping.past.comparison"},
}

def semantic_errors(message):
    """Cross-field invariants not expressible by our structural draft schema."""
    payload = message["payload"]
    kind = message["messageType"]
    errors = []
    if kind == "shopping.past.comparison":
        purchase = datetime.fromisoformat(payload["purchaseAt"])
        cutoff = datetime.fromisoformat(payload["evidenceCutoff"])
        if purchase.utcoffset() is None or cutoff.utcoffset() is None:
            errors.append("timestamps require time-zone offsets")
        elif cutoff > purchase:
            errors.append("historical evidence cannot be observed after purchase")
        if payload.get("status") == "PROVEN":
            if not payload["matchedHistoricalOfferIds"] or payload["savingsProvenCents"] is None:
                errors.append("PROVEN needs price evidence and known savings")
    elif kind == "shopping.need.projection":
        snap = datetime.fromisoformat(payload["snapshotAt"])
        as_of = datetime.fromisoformat(payload["asOf"])
        if snap.utcoffset() is None or as_of.utcoffset() is None:
            errors.append("timestamps require time-zone offsets")
        elif as_of < snap:
            errors.append("decision cutoff predates snapshot")
    return errors

def negative_cases(examples):
    by_type = {x["messageType"]: x for x in examples}
    p = by_type["price.observation"]
    m = by_type["receipt.line"]
    recipe = by_type["recipe.draft"]
    negatives = {}

    def add(name, source, path, wrong):
        item = copy.deepcopy(source)
        obj = item
        for key in path[:-1]:
            obj = obj[key]
        if wrong is Ellipsis:
            del obj[path[-1]]
        else:
            obj[path[-1]] = wrong
        negatives[name] = item

    add("negative cents", p, ["payload", "priceCents"], -1)
    add("store confirmed without ID", p, ["payload", "scope", "storeId"], None)
    add("invalid organic status", p, ["payload", "article", "organic"], "maybe")
    add("invented rights status", p, ["payload", "source", "rightsStatus"], "GUESSED")
    add("missing receipt raw text", m, ["payload", "rawText"], Ellipsis)
    add("nonboolean recipe flag", recipe, ["payload", "flags", "considerOffers"], "false")
    add("zero recipe portions", recipe, ["payload", "portionCount"], 0)
    if "shopping.need.projection" in by_type:
        need = by_type["shopping.need.projection"]
        suggestion = by_type["shopping.purchase.suggestion"]
        interest = by_type["shopping.offer.interest"]
        past = by_type["shopping.past.comparison"]
        add("negative shopping horizon", need, ["payload", "horizonDays"], -2)
        add("missing need id", need, ["payload", "needs", 0, "needId"], "")
        add("unknown amount is not a float", suggestion, ["payload", "expectedCents"], 12.5)
        add("unrecognized suggestion state", suggestion, ["payload", "status"], "BOUGHT")
        add("interest cannot confirm a purchase", interest, ["payload", "confirmed"], True)
        add("unknown interest action", interest, ["payload", "action"], "PURCHASED")
        add("historical evidence must be dated", past, ["payload", "evidenceCutoff"], "tomorrow")
        add("historical savings cannot be negative", past, ["payload", "savingsProvenCents"], -1)
        add("historical hindsight forbidden", past, ["payload", "evidenceCutoff"],
            "2026-11-01T18:00:00+01:00")
        add("proven savings require matched prices", past, ["payload", "status"], "PROVEN")
    return negatives

def check(version):
    folder = CONTRACTS / version
    schema = json.loads((folder / "contract.schema.json").read_text(encoding="utf-8"))
    examples = json.loads((folder / "examples.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    assert isinstance(examples, list)
    assert len(examples) == len(EXPECTED[version]), "One sample per message type required"
    assert {x["messageType"] for x in examples} == EXPECTED[version]
    for i, item in enumerate(examples):
        errors = list(validator.iter_errors(item))
        assert not errors, f"{version}: valid example {i}: {[e.message for e in errors]}"
        assert not semantic_errors(item), f"{version}: semantic failure in example {i}"

    negatives = negative_cases(examples)
    for case, item in negatives.items():
        errors = list(validator.iter_errors(item))
        # Semantic checks apply only after schema validation passes.
        semantics = [] if errors else semantic_errors(item)
        assert errors or semantics, f"{version}: invalid example accepted: {case}"
    return len(examples), len(negatives)

def main():
    count = [0, 0]
    for version in ("v1", "v1.1"):
        p, n = check(version)
        count[0] += p
        count[1] += n
        print(f"PASS {version}: {p} positive, {n} negative; schema + semantic gates")
    print(f"PASS all versions: {count[0]} positive, {count[1]} negative")

if __name__ == "__main__":
    main()

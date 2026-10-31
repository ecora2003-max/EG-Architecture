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
            if not payload["matchedHistoricalOfferIds"] or payload["savingsProvenCents"] is None or payload["savingsProvenCents"] <= 0:
                errors.append("PROVEN needs matched prices and strictly positive proven merchandise savings")
    elif kind == "shopping.purchase.suggestion":
        lines = payload.get("packageLines", [])
        if lines:
            refs = set(payload["observationRefs"])
            products = {line["productId"] for line in lines}
            if len(lines) == 1 and payload["productId"] is not None and payload["productId"] != lines[0]["productId"]:
                errors.append("single row product must match header")
            if len(lines) == 1 and payload["packageCount"] is not None and payload["packageCount"] != lines[0]["packageCount"]:
                errors.append("single row pack count must match header")
            if len(lines) > 1 and (payload["productId"] is not None or payload["packageCount"] is not None):
                errors.append("mixed package selection must not masquerade as a single product/package count")
            if len(products) > 1 and payload["productId"] is not None:
                errors.append("multi-product selection cannot have one top-level productId")
            if any(line["observationId"] is not None and line["observationId"] not in refs for line in lines):
                errors.append("package evidence ID missing from observationRefs")
            if any(line["storeId"] is not None and line["retailerId"] is None for line in lines):
                errors.append("store cannot exist without retailer")
            if any(line["observationId"] is None for line in lines):
                if payload["expectedCents"] is not None or payload["checkoutCents"] is not None:
                    errors.append("unverified package line cannot certify aggregate prices")
                if payload["status"] == "FEASIBLE_NOT_PURCHASED":
                    errors.append("unverified package evidence cannot prove feasible purchase")
            merch = [line["merchandiseCents"] for line in lines]
            checkouts = [line["checkoutCents"] for line in lines]
            if payload["expectedCents"] is not None and (any(x is None for x in merch) or sum(merch) != payload["expectedCents"]):
                errors.append("aggregate merchandise price must equal fully known package lines")
            if payload["checkoutCents"] is not None and (any(x is None for x in checkouts) or sum(checkouts) != payload["checkoutCents"]):
                errors.append("aggregate checkout must equal fully known package lines")
            for line in lines:
                merchandise, deposit, checkout = (line[k] for k in ("merchandiseCents", "depositCents", "checkoutCents"))
                if checkout is not None and (merchandise is None or deposit is None or checkout != merchandise + deposit):
                    errors.append("line checkout needs known merchandise, deposit and exact sum")
    elif kind == "shopping.need.projection":
        snap = datetime.fromisoformat(payload["snapshotAt"])
        as_of = datetime.fromisoformat(payload["asOf"])
        if snap.utcoffset() is None or as_of.utcoffset() is None:
            errors.append("timestamps require time-zone offsets")
        elif as_of < snap:
            errors.append("decision cutoff predates snapshot")
        known = [need["needId"] for need in payload["needs"]]
        unknown = [need["needId"] for need in payload.get("unknownNeeds", [])]
        if len(set(known + unknown)) != len(known + unknown):
            errors.append("duplicate need IDs across typed and unknown need rows")
        if unknown and payload["completeness"] == "COMPLETE":
            errors.append("unresolved needs forbid COMPLETE projection")
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
        add("unknown quantity must stay null", need, ["payload", "unknownNeeds", 0, "quantityToBuy"], 0)
        add("unknown need requires nonempty reason", need, ["payload", "unknownNeeds", 0, "reason"], "")
        add("unknown need must be dated", need, ["payload", "unknownNeeds", 0, "dueDate"], 42)
        add("duplicate need in typed and unknown", need, ["payload", "unknownNeeds", 0, "needId"], need["payload"]["needs"][0]["needId"])
        add("unknown need forbids complete projection", need, ["payload", "completeness"], "COMPLETE")
        add("package line needs valid count", suggestion, ["payload", "packageLines", 0, "packageCount"], 0)
        add("package line without observation cannot prove totals", suggestion, ["payload", "packageLines", 0, "observationId"], None)
        add("package line with wrong merchandise total", suggestion, ["payload", "expectedCents"], 198)
        add("package line checkout must reconcile", suggestion, ["payload", "packageLines", 0, "checkoutCents"], 198)
        add("package line store requires retailer", suggestion, ["payload", "packageLines", 0, "retailerId"], None)
        add("historical savings is merchandise only", past, ["payload", "savingsBasis"], "CHECKOUT")
        add("historical savings requires explicit basis", past, ["payload", "savingsBasis"], Ellipsis)
        proven_zero = copy.deepcopy(past)
        proven_zero["payload"]["matchedHistoricalOfferIds"] = ["OBS-COMPARED-001"]
        proven_zero["payload"]["status"] = "PROVEN"
        proven_zero["payload"]["savingsProvenCents"] = 0
        negatives["proven zero is not a saving"] = proven_zero
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

    additional = []
    if version == "v1.1":
        by_type = {x["messageType"]: x for x in examples}
        mixed = copy.deepcopy(by_type["shopping.purchase.suggestion"])
        mp = mixed["payload"]
        mp["packageLines"].append({
            "productId": "PRODUCT-FAKE-002", "observationId": "OBS-EXAMPLE-002",
            "packageCount": 1, "quantity": {"amount": 250, "unit": "g", "basis": "NET", "confirmed": True},
            "merchandiseCents": 100, "depositCents": 0, "checkoutCents": 100,
            "retailerId": "EXAMPLE_RETAILER", "storeId": "EXAMPLE_STORE"
        })
        mp["productId"] = None
        mp["packageCount"] = None
        mp["observationRefs"].append("OBS-EXAMPLE-002")
        mp["expectedCents"] = 299
        mp["checkoutCents"] = 299
        additional.append(mixed)
        not_proven = copy.deepcopy(by_type["shopping.purchase.suggestion"])
        np = not_proven["payload"]
        np["packageLines"][0]["observationId"] = None
        np["packageLines"][0]["merchandiseCents"] = None
        np["packageLines"][0]["depositCents"] = None
        np["packageLines"][0]["checkoutCents"] = None
        np["observationRefs"] = []
        np["expectedCents"] = None
        np["checkoutCents"] = None
        additional.append(not_proven)
    for i, item in enumerate(additional):
        errors = list(validator.iter_errors(item))
        assert not errors, f"{version}: extra valid example {i}: {[e.message for e in errors]}"
        assert not semantic_errors(item), f"{version}: semantic failure in extra example {i}"
    negatives = negative_cases(examples)
    for case, item in negatives.items():
        errors = list(validator.iter_errors(item))
        # Semantic checks apply only after schema validation passes.
        semantics = [] if errors else semantic_errors(item)
        assert errors or semantics, f"{version}: invalid example accepted: {case}"
    return len(examples) + len(additional), len(negatives)

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

#!/usr/bin/env python3
"""Offline consistency gate for the architecture's *evidence ledger*.

This does NOT execute Kotlin, Python compare_prices, Android instrumentation or
external source access. Those results must be checked in their owning CI.
"""
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "policies" / "shopping-compare-acceptance.v1.json"
SCENARIOS = {f"{n:02d}" for n in range(1, 13)}
CASES = {
    "same_bio", "different_bio", "both_signals", "exact_rate_tie",
    "fractional_delta", "unknown_organic", "unknown_deposit",
    "no_cheaper", "targeted_sale",
}
STATES = {"PARTIAL_FULL_CALL", "HOST_JVM_ONLY", "OPEN", "FULL_CALL_VERIFIED"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(data):
    require(data.get("manifestVersion") == "1.0.0", "manifest version")
    require(data.get("scope") == "SYNTHETIC_FULL_COMPARE_PARITY_AND_INTEGRATION", "scope")
    require(data.get("status") == "PARTIAL_HOST_JVM_VERIFIED_NOT_INTEGRATED", "premature release status")
    ref = data["reference"]
    require(ref["architecturePolicyVersion"] == "1.0.3", "canonical policy version")
    require(ref["preisdatenPolicyVersion"] == "1.0.1", "preisdaten observed version")
    require(ref["einkaufsintelligenzPolicyVersion"] == "1.0.1", "shopping observed version")
    require(ref["policyParityVerified"] is False, "policy drift must remain open")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", ref["pythonReferenceCommit"])), "reference SHA")
    ev = data["hostEvidence"]
    require(ev["repo"] == "ecora2003-max/Ernaerungsgedaechnis", "host repo")
    for key in ("codeTestCommit", "reviewedHead", "fixtureBlobSha"):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", ev[key])), key)
    require(re.fullmatch(
        r"https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/[0-9]+",
        ev["ciRunUrl"]) is not None, "CI URL")
    require(ev["fixturePath"].endswith("/shopping_full_compare_v1.tsv"), "fixture path")
    require(ev["jvmTests"] == 249 and ev["roomMigrationTests"] == 7, "verified host XML totals")
    require(all(ev[k] == 0 for k in ("failures", "errors", "skipped")), "host XML failure")
    require(ev["pythonFullCompareCalls"] == 9, "verified full-call total")
    require(len(ev["fullCallCaseIds"]) == len(CASES) and
            set(ev["fullCallCaseIds"]) == CASES, "full-call fixture case inventory")
    require(all(value is False for value in data["releaseGates"].values()),
            "unproven release gate asserted")
    scenarios = data["scenarios"]
    require(len(scenarios) == 12 and {s["id"] for s in scenarios} == SCENARIOS,
            "missing or duplicate acceptance scenario")
    referenced = set()
    for s in scenarios:
        require(s["state"] in STATES, "unknown scenario state: " + s["id"])
        require(bool(s["title"].strip()), "empty scenario title")
        require(isinstance(s["sharedCases"], list) and
                set(s["sharedCases"]).issubset(CASES), "unrecognized shared case")
        require(len(s["sharedCases"]) == len(set(s["sharedCases"])), "duplicate shared case")
        require(bool(s["missing"]) and all(isinstance(x, str) and x.strip()
                                         for x in s["missing"]), "unjustified completion")
        if s["state"] in ("HOST_JVM_ONLY", "OPEN"):
            require(not s["sharedCases"], "non-full-call state claims full-call evidence")
        if s["state"] == "PARTIAL_FULL_CALL":
            require(bool(s["sharedCases"]), "partial full-call state without fixture")
        require(s["state"] != "FULL_CALL_VERIFIED", "full scenario coverage not evidenced")
        referenced.update(s["sharedCases"])
    require(referenced == CASES, "full-call evidence not mapped to scenario inventory")
    return len(scenarios), len(referenced)


def self_test(original):
    mutations = [
        lambda x: x["scenarios"].append(copy.deepcopy(x["scenarios"][0])),
        lambda x: x["hostEvidence"]["fullCallCaseIds"].append("fabricated"),
        lambda x: x["releaseGates"].__setitem__("integrated", True),
        lambda x: x["reference"].__setitem__("policyParityVerified", True),
        lambda x: x["scenarios"][11].__setitem__("state", "FULL_CALL_VERIFIED"),
        lambda x: x["scenarios"][0].__setitem__("sharedCases", ["invented_case"]),
    ]
    for i, mutation in enumerate(mutations, 1):
        test = copy.deepcopy(original)
        mutation(test)
        try:
            check(test)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError(f"negative ledger test {i} unexpectedly passed")
    return len(mutations)


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenarios, cases = check(data)
    negatives = self_test(data)
    print(f"PASS evidence-ledger consistency: {scenarios} scenarios, "
          f"{cases} pinned full-call cases, {negatives} negative mutations")
    print("NOT A LIVE OR CROSS-LANGUAGE TEST: full parity, device, rights and policy drift remain open.")


if __name__ == "__main__":
    main()

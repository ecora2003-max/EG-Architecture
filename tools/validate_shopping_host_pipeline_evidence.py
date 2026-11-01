#!/usr/bin/env python3
"""Offline consistency checks for the synthetic host pipeline evidence ledger.

This script does NOT run Android, Kotlin, Python module reference functions,
read GitHub CI logs or verify external sources. It prevents accidental release
claims and inconsistent pinned evidence; owning CI remains the test authority.
"""
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "policies" / "shopping-host-pipeline-evidence.v1.json"
EXPECTED = {
    "compare_prices": ("shopping_full_compare_v1.tsv",
                       "27f9a23679727ed793ad20a9c089ce04ea99ba67", 9),
    "project_needs": ("shopping_needs_v1.tsv",
                      "8ada95b1a614d937a3c6afe83f6a56ece316e4fb", 12),
    "optimize_package_mix": ("shopping_pack_mix_v1.tsv",
                             "360e06b5d821e484aa6242737566b6dafdb66d9d", 7),
}
EXPECTED_FIELDS = {
    "compare_prices": {"selected alternatives", "price signals", "synthetic expected outputs"},
    "project_needs": {"horizon totals 1/7/28/56", "unknown event IDs",
                      "snapshot completeness"},
    "optimize_package_mix": {"status", "cost", "selected product IDs and pack counts",
                             "warning strings"},
}
RELEASE_GATES = {
    "fullCompareParityVerified", "fullNeedsParityVerified",
    "fullPurchaseSuggestionParityVerified", "productionRegistriesVerified",
    "androidDeviceVerified", "integrated",
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(s):
    return isinstance(s, str) and re.fullmatch(r"[0-9a-f]{40}", s) is not None

def check(d):
    require(d.get("manifestVersion") == "1.0.0", "manifestVersion")
    require(d.get("scope") == "SYNTHETIC_HOST_PRICE_NEEDS_PACK_PARITY_EVIDENCE", "scope")
    require(d.get("status") == "PARTIAL_OFFLINE_HOST_JVM_VERIFIED_NOT_INTEGRATED",
            "premature release claim")
    host = d["hostEvidence"]
    require(host["repo"] == "ecora2003-max/Ernaerungsgedaechnis", "host repo")
    require(sha(host["ciCommit"]), "CI commit SHA")
    require(host["ciRunUrl"] ==
            "https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41263550103",
            "pinned CI URL")
    require(host["ciCommit"] == "c32945c347027b14903299dd0d67c1c42e749d5a",
            "CI SHA does not match reviewed run")
    require(host["ciJobId"] == 124721530890, "CI job")
    require(host["jvmTests"] == 260 and host["roomMigrationTests"] == 7,
            "verified JUnit totals")
    require(all(host[k] == 0 for k in ("jvmFailures", "jvmErrors", "jvmSkipped")),
            "failed or skipped tests")
    require(host["androidInstrumentationExecuted"] is False and host["apkBuilt"] is False,
            "device or APK execution not evidenced")
    ref = d["pythonReference"]
    require(ref["repo"] == "ecora2003-max/EG-Einkaufsintelligenz", "reference repo")
    require(ref["commit"] == "a3e13b147124ad7c25698a695e2ab42d7299a58a",
            "reference must remain pinned")
    require(set(d["releaseGates"]) == RELEASE_GATES and
            all(v is False for v in d["releaseGates"].values()),
            "unsupported release gate")
    rows = d["pipelines"]
    require(isinstance(rows, list) and len(rows) == 3, "three pipelines required")
    require({x["id"] for x in rows} == set(EXPECTED), "missing/duplicate pipeline")
    for p in rows:
        name = p["id"]
        file_name, blob, count = EXPECTED[name]
        require(p["fixturePath"] ==
                "app/src/test/resources/integration/" + file_name, "fixture path: " + name)
        require(sha(p["fixtureBlobSha"]) and p["fixtureBlobSha"] == blob,
                "fixture blob: " + name)
        require(p["sharedFullFunctionCalls"] == count, "shared calls: " + name)
        require(p["status"] == "PARTIAL_SHARED_FULL_CALL", "premature parity claim: " + name)
        fields = p["verifiedFields"]
        require(isinstance(fields, list) and len(fields) == len(set(fields)) and
                set(fields) == EXPECTED_FIELDS[name], "claimed fields: " + name)
        missing = p["notVerified"]
        require(isinstance(missing, list) and len(missing) >= 3 and
                all(isinstance(s, str) and s.strip() for s in missing),
                "missing gates: " + name)
    return len(rows), sum(x["sharedFullFunctionCalls"] for x in rows)

def negative_tests(d):
    mutations = [
        lambda x: x["hostEvidence"].__setitem__("jvmTests", 261),
        lambda x: x["hostEvidence"].__setitem__("androidInstrumentationExecuted", True),
        lambda x: x["releaseGates"].__setitem__("integrated", True),
        lambda x: x["pipelines"][0].__setitem__("sharedFullFunctionCalls", 10),
        lambda x: x["pipelines"][1].__setitem__("status", "FULL_PARITY_VERIFIED"),
        lambda x: x["pipelines"][2]["verifiedFields"].append("optimalityProven"),
        lambda x: x["pipelines"][2].__setitem__("notVerified", []),
        lambda x: x["pythonReference"].__setitem__("commit", "0" * 40),
    ]
    for i, mutate in enumerate(mutations, 1):
        bad = copy.deepcopy(d)
        mutate(bad)
        try:
            check(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError(f"negative ledger mutation {i} unexpectedly passed")
    return len(mutations)

if __name__ == "__main__":
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pipelines, cases = check(manifest)
    negatives = negative_tests(manifest)
    print(f"PASS host-pipeline evidence ledger: {pipelines} partial pipelines, "
          f"{cases} shared full-function calls, {negatives} negative mutations")
    print("NOT A TEST RUN: Android, Python/Kotlin execution, rights and integration "
          "must be independently verified in their owning CI.")

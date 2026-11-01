#!/usr/bin/env python3
"""Validate only the internal consistency of pinned synthetic recipe evidence.

Does NOT run GitHub Actions, Android, Kotlin, Room or external module tests.
"""
import copy
import json
import re
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1] / "policies" / "recipe-host-evidence.v1.json"
HOST = "ecora2003-max/Ernaerungsgedaechnis"
HOST_SHA = "3fb4b75f86c2d3b4680e19bc1eb16192633dabe4"
MODULE_SHA = "5b6320d5b93a2011613b6dbb310865ed22fc39bc"
RELEASE_KEYS = {
    "recipeJsonImportVerified", "recipeGeneratorHostParityVerified",
    "productionRegistriesVerified", "androidDeviceVerified", "integrated",
}
GATES = {
    "context_and_review": {
        "count": 1, "scope": "HOST_JVM_REVIEW_ONLY",
        "verified": {
            "eight flag combinations from prior host CI",
            "missing or unauthorized selected context fails closed",
            "independent product version, quantity basis and allergen checks",
        },
    },
    "synthetic_foodstore_chain": {
        "count": 3, "scope": "ROBOLECTRIC_IN_MEMORY_ROOM_ONLY",
        "verified": {
            "draft has no transaction",
            "separate confirmed save, production and consumption",
            "idempotent retries, rollback and ordered reversals",
        },
    },
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def is_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def check(d):
    require(d["manifestVersion"] == "1.0.0", "manifest version")
    require(d["scope"] == "SYNTHETIC_HOST_RECIPE_REVIEW_FOODSTORE_EVIDENCE", "scope")
    require(d["status"] == "PARTIAL_RECIPE_HOST_JVM_VERIFIED_NOT_INTEGRATED",
            "premature status")
    require(d["observedAt"] == "2026-11-01T04:14:10Z", "observation timestamp")
    host = d["hostEvidence"]
    require(host["repo"] == HOST, "host repository")
    require(host["ciCommit"] == HOST_SHA and is_sha(host["ciCommit"]), "host SHA")
    require(host["ciRunUrl"] == "https://github.com/" + HOST +
            "/actions/runs/41271956493", "host CI URL")
    require(host["ciJobId"] == 124746372731, "host CI job")
    require(host["junitXmlFiles"] == 40 and host["jvmTests"] == 290 and
            host["roomMigrationTests"] == 7, "host JUnit evidence")
    require(all(type(host[k]) is int and host[k] == 0 for k in
                ("jvmFailures", "jvmErrors", "jvmSkipped")), "host test failures")
    require(host["androidInstrumentationExecuted"] is False and
            host["apkBuilt"] is False, "unproven Android/APK")
    require(host["recipeHostCodeBlob"] ==
            "ccc4d29616b2e0150a97939c824d1229176efd5d", "host code blob")
    require(host["recipeE2ETestBlob"] ==
            "8bd7ef91dd0b561aed9644bbe6928be5d7e9e315", "E2E test blob")

    prior = d["priorHostEvidence"]
    require(prior["ciCommit"] == "760acb8a3a69c61ee2eac9f0e8aa90260514e95c",
            "prior CI SHA")
    require(prior["ciRunUrl"] == "https://github.com/" + HOST +
            "/actions/runs/41270443755", "prior CI URL")
    require(prior["jvmTests"] == 286 and prior["newRecipeHostGateTests"] == 9,
            "prior CI test counts")
    require(host["jvmTests"] - prior["jvmTests"] == 4, "new host test delta")

    module = d["recipeModuleReference"]
    require(module["repo"] == "ecora2003-max/EG-Rezept-KI", "module repo")
    require(module["ciCommit"] == MODULE_SHA and is_sha(module["ciCommit"]),
            "module SHA")
    require(module["ciRunUrl"] ==
            "https://github.com/ecora2003-max/EG-Rezept-KI/actions/runs/41233688107",
            "module CI URL")
    require(module["kotlinJvmTests"] == 220 and module["schemaCases"] == 74,
            "module test counts")
    contract = d["contractReference"]
    require(contract["version"] == "1.0.0-draft", "contract version")
    require(contract["schemaBlobSha"] ==
            "bedde4677342817fe6b883962c8dfbbd60100072", "contract blob")
    gates = d["hostGates"]
    require(isinstance(gates, list) and len(gates) == 2, "host gates count")
    require({x["id"] for x in gates} == set(GATES), "missing/duplicate gate")
    for gate in gates:
        spec = GATES[gate["id"]]
        require(type(gate["newTestsOnLatestHostCi"]) is int and
                gate["newTestsOnLatestHostCi"] == spec["count"], "new tests count")
        require(gate["scope"] == spec["scope"], "scope")
        verified = gate["verified"]
        require(isinstance(verified, list) and
                len(verified) == len(set(verified)) and
                set(verified) == spec["verified"], "verified claims")
        missing = gate["notVerified"]
        require(isinstance(missing, list) and len(missing) >= 3 and
                len(missing) == len(set(missing)) and
                all(isinstance(s, str) and s.strip() for s in missing),
                "missing gates")
    require(sum(x["newTestsOnLatestHostCi"] for x in gates) == 4,
            "new test count not reconciled")
    release = d["releaseGates"]
    require(set(release) == RELEASE_KEYS and
            all(value is False for value in release.values()),
            "unsupported release claim")
    return len(gates)


def negative_tests(data):
    mutations = [
        lambda d: d["hostEvidence"].__setitem__("jvmTests", 291),
        lambda d: d["hostEvidence"].__setitem__("androidInstrumentationExecuted", True),
        lambda d: d["hostEvidence"].__setitem__("jvmFailures", 1),
        lambda d: d["priorHostEvidence"].__setitem__("jvmTests", 285),
        lambda d: d["hostGates"][0].__setitem__("newTestsOnLatestHostCi", 2),
        lambda d: d["hostGates"][1].__setitem__("scope", "ANDROID_DEVICE"),
        lambda d: d["hostGates"][1]["verified"].append("full schema import"),
        lambda d: d["hostGates"][0].__setitem__("notVerified", []),
        lambda d: d["recipeModuleReference"].__setitem__("schemaCases", 75),
        lambda d: d["releaseGates"].__setitem__("integrated", True),
        lambda d: d["contractReference"].__setitem__("version", "1.1.0-draft"),
    ]
    for index, mutate in enumerate(mutations, 1):
        changed = copy.deepcopy(data)
        mutate(changed)
        try:
            check(changed)
        except (KeyError, TypeError, ValueError):
            continue
        raise AssertionError(f"negative mutation {index} unexpectedly accepted")
    return len(mutations)


if __name__ == "__main__":
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    gates = check(manifest)
    negatives = negative_tests(manifest)
    print(f"PASS recipe-host evidence ledger: {gates} partial gates, "
          f"4 new JVM tests, {negatives} negative mutations")
    print("NOT A TEST RUN: External host/module CI, Android hardware and "
          "complete recipe import must be verified independently.")

#!/usr/bin/env python3
"""Static evidence consistency only. Does not run Kotlin, Android, Room or GitHub CI."""
import copy
import json
import re
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "policies" / "recipe-v1-import-evidence.v1.json"
HOST = "ecora2003-max/Ernaerungsgedaechnis"
MILESTONES = (
    ("review_foodstore", "3fb4b75f86c2d3b4680e19bc1eb16192633dabe4", 41271956493, 290, 4),
    ("bounded_json_import", "7bf45400d10a6cdbd5e6e50f6f8346367bea6805", 41273875502, 303, 13),
    ("trusted_context_timestamp", "de6842a3dcc25dd8f02d3db34d7b39ca8aab90a8", 41274938362, 304, 1),
    ("room_catalog_preview", "d94f4a93b7e6f63a8ecfa3c620974e39e7d97609", 41275499465, 307, 3),
)
EXPECTED_BLOBS = {
    "boundedJson": "a926090d309c8002edcbad43564212e0dcdab967",
    "v1Import": "666c5b3ebbe1efd4f533fb1ce5de4c1827985a45",
    "catalogEvidence": "ec60ad63278e3c2b3d9f59af552665de10fefb62",
    "catalogTest": "09e6c143cd82896aef32d78d396df4fbfb7b51a8",
    "schemaChecker": "373a6ef05437f45d005aa8d73f9b3a96c1ff8911",
}
TRUE_GATES = {"boundedJsonImportJvmVerified", "pinnedSchemaFixtureCiVerified",
              "trustedContextTimeJvmVerified", "roomCatalogPreviewJvmVerified"}
FALSE_GATES = {"fullRuntimeSchemaVerified", "recipeModuleParityVerified",
               "productionConfirmationRegistryVerified", "saveTimeRevalidationVerified",
               "androidDeviceVerified", "integrated"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None

def check(data):
    require(data["manifestVersion"] == "1.0.0", "manifest version")
    require(data["scope"] == "SYNTHETIC_HOST_RECIPE_V1_IMPORT_AND_ROOM_CATALOG", "scope")
    require(data["status"] == "PARTIAL_JVM_AND_SCHEMA_FIXTURE_VERIFIED_NOT_INTEGRATED", "status")
    require(data["observedAt"] == "2026-11-01T05:09:33Z", "observed timestamp")
    c = data["contract"]
    require(c == {"version": "1.0.0-draft",
                  "schemaBlobSha": "bedde4677342817fe6b883962c8dfbbd60100072",
                  "runtimeSchemaValidation": False}, "contract or runtime claim")
    h = data["host"]
    require(h["repo"] == HOST and h["commit"] == MILESTONES[-1][1] and sha(h["commit"]), "host pin")
    require(h["runUrl"] == "https://github.com/" + HOST + "/actions/runs/41275499465", "run URL")
    require(type(h["jobId"]) is int and h["jobId"] == 124756745519, "job ID")
    for key, value in {"junitXmlFiles": 42, "jvmTests": 307, "jvmFailures": 0,
                       "jvmErrors": 0, "jvmSkipped": 0, "roomMigrationTests": 7,
                       "recipeSchemaPositive": 9, "recipeSchemaNegative": 14}.items():
        require(type(h[key]) is int and h[key] == value, "host evidence: " + key)
    require(h["fullPythonCalls"] == {"comparePrices": 9, "projectNeeds": 12,
                                    "optimizePackageMix": 7, "suggestPurchases": 7},
            "full Python call counts")
    require(h["androidInstrumentationExecuted"] is False and h["apkBuilt"] is False,
            "unsupported Android/APK")
    milestones = data["milestones"]
    require(isinstance(milestones, list) and len(milestones) == 4, "milestones count")
    for index, (entry, expected) in enumerate(zip(milestones, MILESTONES)):
        keys = ("id", "commit", "runId", "jvmTests", "increment")
        require(tuple(entry[k] for k in keys) == expected and sha(entry["commit"]),
                "milestone " + str(index))
        if index > 0:
            require(entry["jvmTests"] - milestones[index-1]["jvmTests"] == entry["increment"],
                    "test increment")
    require(data["codeBlobs"] == EXPECTED_BLOBS and all(sha(x) for x in EXPECTED_BLOBS.values()),
            "source blobs")
    for key, minimum in (("verifiedScopes", 5), ("notVerified", 7)):
        values = data[key]
        require(isinstance(values, list) and len(values) >= minimum and
                len(values) == len(set(values)) and
                all(isinstance(v, str) and v.strip() for v in values), key)
    release = data["releaseGates"]
    require(set(release) == TRUE_GATES | FALSE_GATES, "release gate keys")
    require(all(release[k] is True for k in TRUE_GATES) and
            all(release[k] is False for k in FALSE_GATES), "premature release")
    return len(milestones)

def negative_tests(original):
    changes = [
        lambda d: d["host"].__setitem__("jvmTests", 308),
        lambda d: d["host"].__setitem__("jvmFailures", 1),
        lambda d: d["host"].__setitem__("androidInstrumentationExecuted", True),
        lambda d: d["host"].__setitem__("recipeSchemaNegative", 13),
        lambda d: d["host"]["fullPythonCalls"].__setitem__("suggestPurchases", 8),
        lambda d: d["milestones"][1].__setitem__("increment", 12),
        lambda d: d["milestones"][3].__setitem__("commit", "0"*40),
        lambda d: d["codeBlobs"].__setitem__("v1Import", "0"*40),
        lambda d: d["contract"].__setitem__("runtimeSchemaValidation", True),
        lambda d: d["releaseGates"].__setitem__("integrated", True),
        lambda d: d["releaseGates"].__setitem__("productionConfirmationRegistryVerified", True),
        lambda d: d["notVerified"].__setitem__(slice(None), []),
    ]
    for i, change in enumerate(changes, 1):
        modified = copy.deepcopy(original)
        change(modified)
        try:
            check(modified)
        except (KeyError, TypeError, ValueError):
            continue
        raise AssertionError("negative mutation " + str(i) + " was accepted")
    return len(changes)

if __name__ == "__main__":
    evidence = json.loads(FILE.read_text(encoding="utf-8"))
    count = check(evidence)
    negative = negative_tests(evidence)
    print(f"PASS recipe v1 import evidence: {count} milestones, 307 JVM tests, "
          f"9/14 schema fixtures, {negative} negative mutations")
    print("NOT A TEST RUN: Host CI, Kotlin/Room, Android and module parity are external.")

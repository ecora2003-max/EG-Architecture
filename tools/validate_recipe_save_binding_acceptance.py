#!/usr/bin/env python3
"""Validate the static recipe save-binding acceptance register, not external CI."""
import copy
import json
import re
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "policies" / "recipe-save-binding-acceptance.v1.json"
HOST = "ecora2003-max/Ernaerungsgedaechtnis"
VERIFIED = {
    "SAVE_IDEMPOTENT": "RecipeDraftCatalogSaveTest.exactReviewedInputSavesOnceAndNeverBooksStockOrConsumption",
    "MISSING_CONFIRMATION": "RecipeDraftCatalogSaveTest.missingSeparateConfirmationCannotWriteAnything",
    "DRAFT_CONTENT_CHANGE": "RecipeDraftCatalogSaveTest.changedDraftOrChangedHostAllergenEvidenceCannotReusePreview",
    "ALLERGEN_FACT_CHANGE": "RecipeDraftCatalogSaveTest.changedDraftOrChangedHostAllergenEvidenceCannotReusePreview",
    "CATALOG_REVISION_RACE": "RecipeDraftCatalogSaveTest.interveningCatalogRevisionInvalidatesPreviouslyReadyPreview",
    "OPERATION_KEY_COLLISION": "RecipeDraftCatalogSaveTest.reusedOperationKeyWithDifferentReviewedRecipeCannotOverwriteHistory",
    "NESTED_BOOKING_CLAIM": "RecipeDraftV1ImportTest.bookingClaimsInNestedAndUnknownExtensionsNeverBecomeHostEvents",
    "FUTURE_TRUSTED_CONTEXT": "RecipeDraftV1ImportTest.futureDatedHostContextCannotAttestARecipeEvenWithinProducerClockSkew",
}
PENDING = {
    "DRAFT_ID_SWAP_SAME_RECIPE_INPUT",
    "TRACE_OR_META_SWAP_SAME_INPUT",
    "WARNINGS_OR_EXTENSION_SWAP_SAME_INPUT",
    "CONSENT_FLAGS_OR_RESTRICTIONS_CHANGE",
    "CONTEXT_SNAPSHOT_REVOCATION",
    "CONFIRMATION_PROVENANCE",
    "CONFIRMATION_REPLAY_OTHER_DRAFT",
    "PARALLEL_CATALOG_UPDATE",
    "RESTART_AND_REPLAY",
    "ALLERGEN_EVIDENCE_REVOCATION",
    "RUNTIME_DRAFT202012_SCHEMA",
    "MODULE_REVALIDATOR_PARITY",
    "ANDROID_USER_ACTION_E2E",
    "PRODUCTION_HOST_FACTS",
}
GATES = {
    "saveTimeRoomRevalidationJvmVerified": True,
    "fullDraftIdentityBoundToApproval": False,
    "durableUserConfirmationRegistryVerified": False,
    "fullRuntimeSchemaVerified": False,
    "moduleRevalidatorParityVerified": False,
    "androidDeviceVerified": False,
    "integrated": False,
}
EXPECTED_HOST = {
    "repository": HOST,
    "testedCommit": "786271e840b1495e5f2eacf11595f552c72ce355",
    "runId": 41279640831,
    "jobId": 124768754231,
    "jvmTests": 315,
    "jvmFailures": 0,
    "jvmErrors": 0,
    "jvmSkipped": 0,
    "roomMigrations": 7,
    "recipeSchemaPositive": 9,
    "recipeSchemaNegative": 14,
    "androidInstrumentationExecuted": False,
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def check(d):
    require(d["manifestVersion"] == "1.0.0", "manifest version")
    require(d["scope"] == "RECIPE_SAVE_APPROVAL_BINDING", "scope")
    require(d["observedAt"] == "2026-11-01T06:13:00Z", "observedAt")
    require(d["contract"] == {
        "version": "1.0.0-draft",
        "schemaBlobSha": "bedde4677342817fe6b883962c8dfbbd60100072",
        "fullRuntimeValidationVerified": False,
    }, "contract")
    require(d["host"] == EXPECTED_HOST, "host evidence or unsupported claim")
    require(re.fullmatch(r"[0-9a-f]{40}", d["host"]["testedCommit"]) is not None,
            "host SHA")
    require("Caller-provided confirmation" in d["evidenceScope"], "evidence limitation")
    require(d["releaseGates"] == GATES, "premature release claim")
    scenarios = d["scenarios"]
    require(isinstance(scenarios, list) and len(scenarios) == len(VERIFIED) + len(PENDING),
            "scenario count")
    ids = [x["id"] for x in scenarios]
    require(len(ids) == len(set(ids)) and set(ids) == set(VERIFIED) | PENDING,
            "missing/duplicate/unknown scenario")
    for s in scenarios:
        require(set(s) == {"id", "status", "expectedWrite", "testRef", "acceptance"},
                "scenario fields")
        require(s["expectedWrite"] in {"NONE", "RECIPE_ONLY"}, "side-effect scope")
        require(isinstance(s["acceptance"], str) and len(s["acceptance"].strip()) >= 30,
                "acceptance detail")
        if s["id"] in VERIFIED:
            require(s["status"] == "JVM_SYNTHETIC_VERIFIED" and
                    s["testRef"] == VERIFIED[s["id"]] and
                    s["acceptance"].startswith("Verified only within"),
                    "verified fixture evidence")
        else:
            require(s["status"] == "PENDING" and s["testRef"] is None,
                    "unproven case cannot claim success")
    return len(VERIFIED), len(PENDING)

def negative_tests(original):
    changes = [
        lambda d: d["host"].__setitem__("jvmTests", 316),
        lambda d: d["host"].__setitem__("jvmFailures", 1),
        lambda d: d["host"].__setitem__("androidInstrumentationExecuted", True),
        lambda d: d["host"].__setitem__("testedCommit", "0" * 40),
        lambda d: d["contract"].__setitem__("fullRuntimeValidationVerified", True),
        lambda d: d["releaseGates"].__setitem__("integrated", True),
        lambda d: d["releaseGates"].__setitem__("fullDraftIdentityBoundToApproval", True),
        lambda d: d["scenarios"][0].__setitem__("testRef", "ImaginaryTest.passes"),
        lambda d: d["scenarios"][0].__setitem__("status", "PENDING"),
        lambda d: d["scenarios"][-1].__setitem__("status", "JVM_SYNTHETIC_VERIFIED"),
        lambda d: d["scenarios"][-1].__setitem__("testRef", "ImaginaryTest.passes"),
        lambda d: d["scenarios"].append(copy.deepcopy(d["scenarios"][0])),
        lambda d: d["scenarios"].pop(),
        lambda d: d["scenarios"][-1].__setitem__("expectedWrite", "STOCK_AND_RECIPE"),
        lambda d: d.__setitem__("evidenceScope", "All integration complete"),
        lambda d: d["scenarios"][-1].__setitem__("acceptance", ""),
    ]
    for index, mutate in enumerate(changes, 1):
        candidate = copy.deepcopy(original)
        mutate(candidate)
        try:
            check(candidate)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError(f"negative mutation {index} was accepted")
    return len(changes)

if __name__ == "__main__":
    manifest = json.loads(FILE.read_text(encoding="utf-8"))
    verified, pending = check(manifest)
    mutations = negative_tests(manifest)
    print(f"PASS recipe save binding ledger: {verified} synthetic JVM scenarios, "
          f"{pending} pending gates, {mutations} negative mutations")
    print("STATIC ONLY: no external GitHub CI, Android runtime, Room or user-action tests run here.")

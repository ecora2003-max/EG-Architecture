#!/usr/bin/env python3
"""Contract-level retailer capability checks: not a production source permission test.

This validates the architecture's user-selected functional matrix only.
The actual retailer adapters must independently enforce source legality,
access scope, rate limits and APP_DISPLAY use.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "policies" / "retailer-source-capabilities.v1.json"
YES_PRICE = {"ALDI_NORD", "ALDI_SUED", "REWE", "LIDL"}
NO_PRICE = {"PENNY", "KAUFLAND", "EDEKA", "NETTO_MD"}
UNKNOWN = set()
ALL = YES_PRICE | NO_PRICE | UNKNOWN

def main():
    data = json.loads(POLICY.read_text(encoding="utf-8"))
    assert data["policyVersion"] == "1.0.2"
    assert data["category"] == "PROJECT_FUNCTIONAL_CAPABILITY_NOT_LEGAL_PERMISSION"
    cap = data["retailerCapabilities"]
    assert set(cap) == ALL, "Retailer names missing or unexpected"
    checks = 0
    for retailer, spec in cap.items():
        assert set(spec) == {"targetedProductPriceQuery", "publishedOfferCollection", "publishedOfferCatalogDiscovery"}
        q = spec["targetedProductPriceQuery"]
        offers = spec["publishedOfferCollection"]
        catalog = spec["publishedOfferCatalogDiscovery"]
        assert type(q) is bool or q is None
        assert type(offers) is bool or offers is None
        assert type(catalog) is bool or catalog is None
        if retailer in YES_PRICE:
            assert q is True and offers is True and catalog is True
        elif retailer in NO_PRICE:
            assert q is False and offers is True and catalog is False
        else:
            assert q is None and offers is None and catalog is None
        checks += 3
    gate = data["executionGates"]
    required = (
        "lawfulAccessRequired", "sourceTermsAndDatabaseRightsPerSource",
        "noLoginOrTechnicalProtectionBypass", "noMassCatalogExtraction",
        "noUncontrolledPolling", "rateLimitAndTimeoutRequired",
        "rawSourceProvenanceAndDateRequired", "storeOrRegionalScopeMustBeReported",
        "externalAppDisplayMustBeSeparatelyLawfullyGrounded",
        "unknownSourceRightsMustNeverBePromotedToPermitted",
        "userConfirmedReceiptHistoryRemainsSeparate",
    )
    assert all(gate.get(k) is True for k in required), "Source safety gate missing"
    checks += len(required)
    assert "DEVELOPMENT_ONLY" in data["staging"]
    print(f"PASS: {checks} retailer capability / safety gate assertions; 4 price+offer+catalog, 4 offer-only.")
    print("NOTE: this is policy configuration validation, not proof of a retailer API or legal permission.")

if __name__ == "__main__":
    main()

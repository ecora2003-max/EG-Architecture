# EG-Architecture – verbindliche Fachverträge
**Rolle:** Chat 1 / Architektursteuerung. **Status:** erste Vertragsbasis `1.0.0-draft`, 31.10.2026; **keine Freigabe zur produktiven Integration**.

Dieses öffentliche Repository ist die gemeinsame, versionierte Vertragsquelle für unabhängige Zuliefermodule der Android-App „Ernährungsgedächtnis“. **Es ist weder die App noch die produktive Ernährungs- oder Vorratsdatenbank.**

## Einstieg für alle Entwicklungs-Chats
1. [Master-Architektur](docs/MASTER_ARCHITECTURE.md): Ziele, Systemgrenzen, Verantwortlichkeiten und Datenflüsse.
2. [Fachliches Datenmodell](docs/DOMAIN_MODEL.md): Begriffe, Identitäten, Mengen, Preise, Bon, Quellen, Qualität, Vergleiche.
3. [Integration und Governance](docs/INTEGRATION_AND_GOVERNANCE.md): Versionierung, Freigabe, Tests, Übergabe, Änderungen.
4. [Maschinenlesbarer Vertragskern](contracts/v1/contract.schema.json) und [Beispielnachrichten](contracts/v1/examples.json).
5. [Architekturentscheidungen](docs/DECISIONS.md); [Anweisung für Architektur-Chat](AGENTS.md).

## Repository- und Rollenübersicht
| Repository | Rolle / Besitz | Darf bearbeiten |
| --- | --- | --- |
| [EG-Architecture](https://github.com/ecora2003-max/EG-Architecture) | gemeinsame Verträge, Chat 1 | Architektursteuerung |
| [EG-Preisdaten](https://github.com/ecora2003-max/EG-Preisdaten) | Händleradapter, Preise, Angebote | Preisdaten-Chat |
| [EG-Produktdaten](https://github.com/ecora2003-max/EG-Produktdaten) | Produktidentifikation, Bon-Aliase, Preisgedächtnis | Produktdaten-Chat |
| [EG-Einkaufsintelligenz](https://github.com/ecora2003-max/EG-Einkaufsintelligenz) | Preisvergleich, Kaufentscheidung, Nachfrageprognose | Einkaufs-Chat |
| [EG-Rezept-KI](https://github.com/ecora2003-max/EG-Rezept-KI) | Rezeptentwürfe und optionale Kontextnutzung | Rezept-Chat |
| `Ernaerungsgedaechtnis` (GitHub-Sichtbarkeit derzeit public) | bestehende Android-App, ausschließlich Codex | **Nur App-Integration/Codex** |

**Schreibregel:** Entwicklungs-Chats verändern ausschließlich ihr eigenes Repository. Andere Module und die Architektur dürfen gelesen werden; Vorschläge zu Fremdänderungen werden als dokumentierte Änderungsanträge gestellt. Das App-Repository ist für Module nur lesend relevant; seine GitHub-Sichtbarkeit ist derzeit public und kein Schutz für personenbezogene Daten. Projektanweisungen sind **keine technische GitHub-Rechtesperre**.

## Architektur-Grundsatz
Die Module sind **Lieferanten eigenständiger, testbarer Produkte**, keine Parallelentwickler der Gesamt-App. Sie erhalten und liefern dokumentierte Daten; sie verwenden intern frei gewählte Modelle. Codex adaptiert diese an die bestehende lokale Room-Architektur. Kein Modul greift direkt auf Room-DAOs, produktive Google Sheets, reale Bestände oder private Nutzerkonten zu.

## Unverhandelbare Sicherheits- und Datenregeln
- **Preisbeobachtung ≠ bezahlter Kauf ≠ Bestandsbewegung; Rezeptentwurf ≠ Kochen ≠ Verzehr.**
- Unbekannt `null`/fehlend ≠ bekannte Null. Keine erratenen Barcodezuordnungen, Mengen, Haltbarkeiten oder Preise.
- Identitäten, zeitlicher Bezug, Quelle, Filial-/Regionsgeltung, Datenqualität und rechtliche Nutzbarkeit sichtbar erhalten.
- Geld als ganzzahlige Euro-Cents; g/ml/Portion für Fachmengen; Stück-/Packungspreise nur nach belegbarer Umrechnung in Grundpreise.
- Keine Secrets, personenbezogenen Daten oder echten Belege in öffentliche Repositories; ausschließlich synthetische Fixtures.
- Kein kostenpflichtiger API-, Server- oder Hintergrunddienst als Pflichtvoraussetzung. Externe Datenquellen nur im zulässigen Nutzungsrahmen.
- Jede Modul-Lieferung mit reproduzierbarem Test, Fehlerfällen und nachvollziehbarer Dokumentation.

## Freigabegrad
`1.0.0-draft` definiert zunächst den gemeinsamen Arbeitsrahmen. Feldnamen, Pflichtfelder und JSON-Schemas werden vor stabiler `1.0.0` anhand von Beispielen aller vier Module validiert. Keine fertige Haupt-App-Integration oder vollständige Händler-API-Abdeckung wird hier behauptet.

## Vertragsweiterentwicklung und Übergabe (31.10.2026)
- **Aktuell von den Fachmodulen verwendet:** [`contracts/v1` – 1.0.0-draft](contracts/v1/contract.schema.json) (unverändert).
- **Neue, noch nicht stabil freigegebene Erweiterung:** [`contracts/v1.1` – 1.1.0-draft](contracts/v1.1/README.md), vier Shopping-Nachrichtentypen mit synthetischen Fixtures. Module müssen weiterhin ihre unterstützte Version ausdrücklich nennen.
- [Verbindliche Rechte- und Datenanzeige-Schranken](docs/PRICE_RIGHTS_AND_DISPLAY.md) einschließlich privater Bonhistorie und gesperrter externer Quellen.
- [Integrations-Testplan für Codex](docs/CODEX_INTEGRATION_PLAN.md). **Dies ist eine Auftragsbeschreibung, keine fertige Android-Integration.**
- Test: `python -m pip install -r requirements-dev.txt && python tools/validate_contract.py`; GitHub Actions `contract-validation` bei Vertragsänderungen.

- **Aktueller Händler-Funktionsumfang:** [Preisabfrage und Angebots-Erfassung pro Händler](docs/RETAILER_SOURCE_POLICY.md) (ADR-016); separate [JSON-Policy](policies/retailer-source-capabilities.v1.json). Technische Funktionsentscheidung ≠ bestätigte Quellenrechte.

## Chat-1-Übergabe und aktueller Stand
- [Aktueller Architektur- und Modulstatus](docs/STATUS.md), inklusive letzter CI-Nachweise und noch offener Freigabe-Gates.
- [Abnehmer-Kompatibilitätsaudit](docs/CONSUMER_COMPATIBILITY_AUDIT.md) mit konkreten Modul-Schema-SHAs, gültigen CI-Nachweisen und offenen Codex-Testgates.
- [ADR-017](docs/ADR_017_SHOPPING_RESOLUTION.md): unbekannte Bedarfe, typisierte gemischte Packungen und Warenpreis-Basis historischer Ersparnisse im `1.1.0-draft`. Die vorherige v1.1-Testkopie ist nach dieser Draft-Revision **nicht** mehr schema-identisch; betroffene Module müssen erneut prüfen.
- [GitHub Actions Run 41226969317](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41226969317): 16 positive + 37 negative Schema-/Semantiktests, 27 Händler-Policy-Prüfungen erfolgreich. Keine Android-, Live-Händler- oder Rechtsfreigabe.

- [Aktueller Integrationsaudit 01.11.2026](docs/INTEGRATION_EVIDENCE_2026-11-01.md): überprüfte Fachmodul-/Host-CI, Room-8-Teilports, festgestellter Policy-Drift 1.0.1↔1.0.3 und noch offene Host-Orchestrierung; keine produktive Freigabe.
- [Python–Kotlin-Preisvergleichsparität – Integrationsgate](docs/SHOPPING_COMPARE_PARITY_GATE.md): aktueller 240-JVM-Test-/7-Migrationsnachweis, 12 verbindliche E2E-Szenarien und bewusst strengere Host-Gates; vollständige `compare_prices`-Parität weiterhin offen.

- [Preisvergleichs-Abnahmeregister](policies/shopping-compare-acceptance.v1.json) mit 12 Szenarien und 9 geprüften synthetischen Python–Kotlin-Gesamtfällen; [Konsistenzvalidator](tools/validate_shopping_parity_evidence.py) (keine eigenständige End-to-End-Ausführung). [Neueste Architektur-CI 41260847763](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41260847763) erfolgreich.
- [FEFO-/Bedarfs- und Gebindemix-Paritätsgate](docs/SHOPPING_NEEDS_PACK_PARITY_GATE.md): verifizierte Host-CI **260 JVM-Tests**, **9+12+7** synthetische Python-/Kotlin-Vollfunktionsvektoren; [neues Evidenzregister](policies/shopping-host-pipeline-evidence.v1.json) mit [Offline-Validator](tools/validate_shopping_host_pipeline_evidence.py). [Architektur-CI 41264947842](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41264947842) erfolgreich; vollständige Ergebnis-/Geräte-/Transaktionsparität weiterhin offen.

- [Begrenzte `suggest_purchases`-Python–Kotlin-Parität und Sicherheitsgate](docs/SHOPPING_SUGGEST_PARITY_GATE.md): 272 bereits nachgewiesene Host-JVM-Tests, sieben neu eingereichte gemeinsame Gesamtfunktions-Fälle mit zunächst ausstehender CI, ausdrückliche Grenzen für `RESEARCH_ONLY` vs. `APP_DISPLAY` und vollständige Restabnahme.

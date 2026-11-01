# Vertragstests – 31.10.2026

## Neuester nachgeprüfter CI-Nachweis – ADR-017
**GitHub Actions [Run 41226969317](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41226969317)**, Job `validate` (ID `124613037294`), Commit `c1b08f0e062fb9d2cdacf4853296c5529f85f17b`, `completed/success`. Vollständiges Joblog direkt eingesehen:

```text
PASS v1: 5 positive, 7 negative; schema + semantic gates
PASS v1.1: 11 positive, 30 negative; schema + semantic gates
PASS all versions: 16 positive, 37 negative
PASS: 27 retailer capability / safety gate assertions; 4 price+offer, 4 offer-only.
```

**Neu geprüft:** strenges `unknownNeeds[]`-Format und Duplikatsperre, unvollständige Bedarfsprojektionen, typisierte `packageLines[]` mit Quellen-/Preis-/Pfandsummen, zwei zusätzliche gültige gemischte/unsichere Beispiel-DTOs, `savingsBasis=MERCHANDISE_ONLY` und verbotene Scheinersparnis. Vollständiges JSON Schema Draft 2020-12 und zusätzliche Cross-Field-Semantik. **Keine** neue v1-Fachregel.

**Grenze:** Dies belegt Architektur-DTOs und die Händlerkonfigurationsmatrix, **nicht** die bereits vendorten Vertragskopien der Module, nutzbare Live-Quellen, App-Runtime oder Kotlin-Integration. Weitere Abnehmer-/Android-Abnahmetests offen.

## Vorheriger CI-Nachweis (vor ADR-017)
**GitHub Actions [Run 41224097675](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41224097675)**, Job `validate` (Job-ID `124604509848`), Status `completed/success`. Das vollständige Joblog wurde direkt gelesen; exakte Ausgabe des Python-Programms:

```text
PASS v1: 5 positive, 7 negative; schema + semantic gates
PASS v1.1: 9 positive, 17 negative; schema + semantic gates
PASS all versions: 14 positive, 24 negative
```

Ausführung über `.github/workflows/contract-validation.yml` mit gepinntem `jsonschema[format]==4.23.0`, `Draft202012Validator.check_schema`, `FormatChecker`, `tools/validate_contract.py`. Es handelt sich um **tatsächlich ausgeführte** automatische Vertragsprüfungen und Negativtests, nicht nur um eine manuelle Teilkontrolle.

## Vertragliche Bedeutung
- **Version `1.0.0-draft`**: ursprüngliche fünf Nachrichtentypen und 5+7 Tests; Nachrichten und Schema wurden nicht geändert.
- **Version `1.1.0-draft`**: neun Typen inklusive vier neuer Shopping-DTOs und 9+17 Tests. Externe Quellen- und Nutzerrechtsregeln sind fachlich in `docs/PRICE_RIGHTS_AND_DISPLAY.md` definiert.
- Cross-field-Gates der Testsoftware: datierte Entscheidungen dürfen nicht vor ihrem Snapshot liegen; historische Preisdaten dürfen nicht nach dem Kauf beobachtet sein; Status `PROVEN` setzt passend belegte Alternativen und bekannte Ersparnis voraus.
- Zusätzliche lokale Schema-Kontrolle direkt nach dem Anlegen: 9/9 Beispiele akzeptiert, 10/10 syntaktisch/strukturell absichtlich falsche Nachrichten abgewiesen. Diese Kontrolle war **nur teilweise** schemaäquivalent und wird **nicht** statt des obigen Python-Validators als vollständiger Testnachweis zitiert.

## Offen vor stabiler Freigabe
1. Die vier Modul-Chats und Codex haben die neuen `v1.1`-Nachrichten **noch nicht verbindlich als Adapter-API integriert und abgenommen**; darum bleibt `1.1.0-draft` unfrei.
2. Die Schema-Tests beweisen das Nachrichtenformat und selektierte Invarianten, **nicht** die Korrektheit vollständiger App-/Room-Adapter, realer Daten oder des Android-Gerätes.
3. Nutzungsrechte externer Händlerdaten sind weiterhin ungesichert; die vollständige `APP_DISPLAY`-Schranke muss durch Preisdaten, Einkaufsintelligenz und Codex mit eigenen Negativtests belegt werden.
4. Der letzte produktive Haupt-App-Stand wurde hier **nicht verändert oder integriert**; die fertige Offline-Engine erfordert weiterhin Kotlin-Integration durch Codex.

**Freigabestatus:** `DRAFT_CI_VERIFIED`. Keine Behauptung `STABLE`, `APP_INTEGRATED` oder `LIVE_SOURCE_VERIFIED`.

## Reproduktion
```sh
python -m pip install -r requirements-dev.txt
python tools/validate_contract.py
```

## Ergänzung – strengere Shopping-Prüfungen (31.10.2026, 18:03 UTC)
[GitHub Actions 41227460264](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227460264), Job `124614481930`, Commit `02eb9f034256a98339b9fdf37618bb53f818c362`, completed/success. Original-Log geprüft:

```text
PASS v1: 5 positive, 7 negative; schema + semantic gates
PASS v1.1: 11 positive, 34 negative; schema + semantic gates
PASS all versions: 16 positive, 41 negative
PASS: 27 retailer capability / safety gate assertions; 4 price+offer, 4 offer-only.
```

Neuer zusätzlicher Quervergleich: Produkt-/Packungs-Kopffeld muss zur einzigen Packungszeile passen, ein `FEASIBLE_NOT_PURCHASED`-Vorschlag benötigt bekannte Menge/Warenpreis/Cashbetrag/Kapazität; Budgetperioden dürfen nicht rückwärts laufen. **Wichtig:** Das v1.1-Beispiel-Array enthält weiterhin exakt **9** kanonische Nachrichtentyp-Beispiele; die CI zählt **11** positive Fälle, weil **2 gültige Zusatzfälle programmgeneriert** werden. Eine Modulprüfung, die `examples.json` selbst mit 11 Beispielen erwartet, hat ein falsches Testziel. Ein zunächst roter Architektur-CI-Lauf `41227411420` lag an einem falsch konstruierten Negativtest (als `FEASIBLE` gewertet, obwohl genügend Kapazitätsnachweise vorhanden waren); das Fixture wurde korrigiert, spätere CI grün.

Keine Änderung am Schema-Blob `dca777d219307a90bf3d4dff6189fbf12476c508` durch diesen zusätzlichen Validator-Test. Kein Nachweis der Android- oder Händler-Live-Inbetriebnahme.

## Jüngster Vertragstest – externe Preisrechte (31.10.2026, 18:07 UTC)
[Run 41227803811](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227803811), geprüfter Code-Commit `ece096e5b636e25c0c83609095e640adc0a8910a`, `completed/success`: **v1 5 positive/7 negative; v1.1 11 positive/35 negative; zusammen 16 positive/42 negative**. Zusätzlich **27/27** Händlerfunktionsprüfungen. Direkter GitHub-Actions-Joblog-Nachweis.

Neuer testbarer Cross-Field-Sperrfall: `price.observation` mit `meta.usageContext=APP_DISPLAY` und `source.rightsStatus=UNVERIFIED` muss abgewiesen werden (`RESTRICTED` gleicher Gate-Zweig). `PERMITTED` allein ist weiterhin **keine** belegte Nutzungsberechtigung; Lizenz-/Umfangs-/Quellenbeleg und Host-Freigabe bleiben außerhalb des rein lokalen Schema-Validators erforderlich. Das JSON-Schema wurde in dieser Ergänzung nicht verändert.

## ADR-018: getrennte Angebots- und Katalog-Kapazitäten, 31.10.2026, 21:02 UTC
[Run 41241651613](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41241651613) auf Codecommit `4943ea4f9b6496269bb77ac8a81d67b8d87f7528`: **success**, direkter Joblogbefund: `PASS v1: 5 positive, 7 negative`; `PASS v1.1: 11 positive, 35 negative`; `PASS all versions: 16 positive, 42 negative`; `PASS: 35 retailer capability / safety gate assertions; 4 price+offer+catalog, 4 offer-only.`. Drei unabhängig testbare Händlerfähigkeiten in Policy-Version `1.0.2`: gezielte reguläre Produktpreisabfrage, veröffentlichte Einzelangebotspreise und Angebotskatalog-Erfassung der vier gewählten Händler. Keine Änderung an Vertrags-JSON-Schemas, keine rechtliche Quellenfreigabe oder Android-Integration impliziert.

## Jüngster Workflow-/Händlerpolicy-Test – ADR-019, 31.10.2026, 21:09 UTC

[GitHub Actions 41242200776](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41242200776), Job `124658221832`, Codecommit `53c86a32a07a9254629ece92d20edd855226d167`, **completed/success**, Joblog in der Architekturfortsetzung erneut gelesen. Exakte Ausgaben: `PASS v1: 5 positive, 7 negative`; `PASS v1.1: 11 positive, 35 negative`; `PASS all versions: 16 positive, 42 negative`; `PASS: 42 retailer capability / safety gate assertions; 4 price+offer+catalog, 4 offer-only`. Policy **1.0.3** testet zusätzlich ADR-019-Workflow-Direktiven; v1/v1.1-Vertrags-Schema-Blobs unverändert. Sieben nachfolgende Architektur-Commits bis `18794be9` betreffen ausschließlich Dokumente. **Kein** Kotlin-/App-/Geräte-/Livequellenbeweis. Neuer Abnehmer-/Host-Audit: [01.11.2026](INTEGRATION_EVIDENCE_2026-11-01.md).

## Architektur-CI mit maschinenlesbarem Shopping-Abnahmeregister, 01.11.2026, ca. 02:23 MEZ

[Run 41260847763](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41260847763), Job `124713617228`, Code-/Workflow-Commit `0230477a299f05cab700692eae4dc674079f068f`, **completed/success**. Direktes Joblog:

```text
PASS v1: 5 positive, 7 negative; schema + semantic gates
PASS v1.1: 11 positive, 35 negative; schema + semantic gates
PASS all versions: 16 positive, 42 negative
PASS: 42 retailer capability / safety gate assertions; 4 price+offer+catalog, 4 offer-only.
PASS evidence-ledger consistency: 12 scenarios, 9 pinned full-call cases, 6 negative mutations
```

**Reproduktion:** `python -m pip install -r requirements-dev.txt && python tools/validate_contract.py && python tools/validate_retailer_source_policy.py && python tools/validate_shopping_parity_evidence.py`. Das neue Ledger validiert nur Nachweis-Kohärenz (12 Szenarien, neun referenzierte Test-IDs, offene Gates und sechs absichtlich falsche Manifestmutationen). **Es führt keine Python-`compare_prices`-Aufrufe, keine Kotlin-/Room-/Gerätetests und keine externen Quellenprüfungen aus.** Der unabhängige Host-CI-Nachweis der neun echten Full-call-Vektoren steht in [Shopping-Paritätsgate](SHOPPING_COMPARE_PARITY_GATE.md). Vertrags-Schema-Blobs unverändert, `1.1.0-draft` nicht freigegeben.

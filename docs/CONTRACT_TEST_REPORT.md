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

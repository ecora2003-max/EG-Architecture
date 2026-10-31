# Vertragsprüfung – Stand 31.10.2026
**Geprüfter Vertrag:** `contracts/v1/contract.schema.json` mit `contractVersion=1.0.0-draft`.

## Tatsächlich ausgeführte Prüfung
In einer isolierten JavaScript-Prüfroutine wurden die **direkt aus GitHub gelesenen aktuellen** `contract.schema.json` und `examples.json` geparst. Geprüft wurden tatsächlich vorhandene JSON-Schema-Elemente: `$ref`, `type`, `required`, `enum`, `const`, `minimum/maximum`, `properties`, `additionalProperties`, `anyOf`, `allOf`, `if/then`, `format` (grundlegende Syntax) und Arrays.

**Ergebnis:** 5/5 positive Beispiele akzeptiert, 6/6 bewusst beschädigte Nachrichten abgewiesen:
1. negative Preis-Cents,
2. Filialpreis ohne bestätigte `storeId`,
3. unzulässiger Bio-String,
4. Bonposition ohne `rawText`,
5. Rezept-Flag als String statt boolesch,
6. Rezept mit null Portionen.

**Wichtig:** Die ausgeführte JS-Routine ist eine **teilweise Schema-Kontrolle**, **keine vollständige JSON-Schema-2020-12-Implementierung**. Sie beweist strukturelle Plausibilität, nicht die Konformität sämtlicher noch nicht getesteter JSON-Schema-Sonderfälle.

## Reproduzierbarer Vollvalidator
Im Repository sind `requirements-dev.txt` und `tools/validate_contract.py` abgelegt. Zur **separaten vollen Prüfung** auf einem Rechner mit Python:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_contract.py
```

Das Skript benutzt `jsonschema.Draft202012Validator` und kontrolliert 5 positive und 7 negative Fälle. **Dieser Python-Befehl wurde bei der Erstellung dieser Dokumentation noch nicht ausgeführt**; daher kein erfundener Pass-Nachweis. Eine Ausführung/CI-Prüfung samt Commit-SHA ist vor stabiler Vertragsfreigabe nachzuholen.

## Vertragsfreigabe
**Status: `DRAFT_STRUCTURALLY_CHECKED`, nicht `STABLE` / `INTEGRATED`.**
Noch offen: Standardvalidierung per Python gegen vollständiges Repo-Checkout, alle modulindividuellen Abnehmerprüfungen, Semantiktests für Kurs-/Mengen-/Rabattkonstellationen und Integrationsprüfung durch Codex.

## Fehlerkriterien für kommende Releases
Negativer Preis darf nicht als gültige Beobachtung durchgehen; unbekannter Preis darf nicht als null Euro gelten; fehlender Bio-Status darf nicht in „konventionell“ umgewandelt werden; Marktscope darf ohne Markt-ID nicht `STORE_CONFIRMED` heißen; Rezeptvorschlag darf keinen Ist-Vorgang auslösen; Kaufzeitpunkt muss für historische Sparvergleiche belegt sein.

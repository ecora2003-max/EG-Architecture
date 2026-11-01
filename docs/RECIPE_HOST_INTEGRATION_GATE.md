# Rezept-KI: Host-Sicherheitsgate, synthetische FoodStore-Kette und Restabnahme

**Stand:** 01.11.2026, 05:20 MEZ. **Rolle:** Architektursteuerung (nur lesende App-/Modulprüfung). **Status:** `PARTIAL_RECIPE_HOST_JVM_VERIFIED / FULL_RECIPE_IMPORT_PENDING / ANDROID_DEVICE_PENDING / NOT_INTEGRATED`.

## Direkt verifizierte Evidenz

- **Haupt-App:** [CI 41271956493](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41271956493), Code-/Test-SHA `3fb4b75f86c2d3b4680e19bc1eb16192633dabe4`, Job `124746372731`, `completed/success`. Direktes Joblog: `JUNIT_XML: files=40 tests=290 failures=0 errors=0 skipped=0 migrations=7`, `BUILD SUCCESSFUL in 3m 53s`; Lint, Room-8-Schema, Android-Test**kompilierung**, sechs gepinnte Python-Teilprüfungen und 9/12/7/7 Shopping-Full-call-Referenzen erfolgreich. **APK-Erzeugung übersprungen; kein Emulator-/Gerätetest ausgeführt.**
- **Vorherige Host-Stufe:** [CI 41270443755](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41270443755) auf `760acb8a3a69c61ee2eac9f0e8aa90260514e95c`: 286/286 JVM, 7 Migrationen, darunter neun neue `RecipeDraftHostGateTest`-Methoden. Der neueste Lauf umfasst zusätzlich vier Tests (ein Kontext-Negativtest, drei `RecipeDraftHostEndToEndTest`-Fälle).
- **Referenzmodul:** [EG-Rezept-KI CI 41233688107](https://github.com/ecora2003-max/EG-Rezept-KI/actions/runs/41233688107), SHA `5b6320d5b93a2011613b6dbb310865ed22fc39bc`: laut Modulstatus 220 Kotlin-JVM-Prüfungen, 74 Draft-2020-12-Schemafälle; **separate Modul-CI**, nicht mit dem Host-Kotlin-Code gleichzusetzen.
- **Vertrag:** `contracts/v1` = `1.0.0-draft`, Schema-Blob `bedde4677342817fe6b883962c8dfbbd60100072`. `v1.1` bleibt ein nicht freigegebener Shopping-Entwurf. Keine Schemaänderung durch dieses Gate.

## Was der Host wirklich prüft

Der Code [RecipeDraftHostGate.kt](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/3fb4b75f86c2d3b4680e19bc1eb16192633dabe4/app/src/main/java/de/ernaehrung/demo/data/integration/RecipeDraftHostGate.kt) ist ein **rein lesender** Port für bereits extern validierte DTOs, kein JSON-Decoder, Generator oder Datenbankautor. Er verlangt explizite Freigabe der jeweils ausgewählten Vorrats-, Einkaufs- und Angebotskontexte, unabhängige Produktversionsidentität, passende Mengenbasis und Roh-/Gargewicht sowie bekannte Allergenbelege. Nicht gewählte Snapshots dürfen nicht weitergereicht werden. Unbekannte Mengen/Allergene/Produktversionen bleiben `REVIEW_REQUIRED`, bestätigte Konflikte `BLOCKED`; nur gesonderte Rezeptbestätigung kann `RecipeInput` ermöglichen.

Die drei [synthetischen Room-/FoodStore-Tests](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/3fb4b75f86c2d3b4680e19bc1eb16192633dabe4/app/src/test/java/de/ernaehrung/demo/RecipeDraftHostEndToEndTest.kt) prüfen: Entwurf ohne Ist-Buchung; separaten Rezeptsave; ausdrücklich bestätigte, idempotente Herstellung; gesonderten Verzehr; Rollback einer gescheiterten Produktion; korrekte Reihenfolge der Stornos. **Das ist ein begrenzter Robolectric-/In-Memory-Room-Nachweis, kein produktiver App-/Geräte-End-to-End-Test.**

## Verbindliche Restabnahme für Codex

1. **Vollständigen `recipe.draft`-Import**: JSON-Decoder, Draft-2020-12-Schema mit negativem Input, typgetreue Felder/Integer-Mengen, Version/Offset/Quelle, erneute Modul-`RecipeDraftRevalidation` und Host-Identitäts-/Allergen-/Nährwertbelege auf demselben App-SHA prüfen. Der Host akzeptiert derzeit bereits konstruierte `Draft`-Objekte; das ist keine Schema-Parität.
2. **Reale Generator- und Kontextpipeline**: gepinnten deterministischen Offline-Kandidatenkern anbinden; alle acht Flagkombinationen, unbekannte/verspätete Snapshots, bestätigte Restriktionen, Mengen-/Zubereitungsbasis und unvollständige Nährwerte auf vollständiger Input→JSON→Review→UI-Kette nachweisen. Optionales lokales Modell bleibt bis zu echter Android-Privacy-/Runtime-Prüfung deaktiviert.
3. **Transaktionale Integration erweitern**: produktive Host-Datenadapter, aktuelle Produktversionsbelege, negative Storno-/Retry-/Konkurrenz-/Neustart- und Migrationstests. Vorschlag, Plan und Rezeptsave dürfen nie implizit Herstellung, Einkauf oder Verzehr buchen.
4. **Android-Instrumentation tatsächlich ausführen**: UI-/Bestätigungsgrenzen, Kamera/OCR nur soweit betroffen, Offline-/Datenschutz-/Geräte-/optional Modellverfügbarkeit. `compileDebugAndroidTestKotlin` ist kein ausgeführter Gerätetest.

**Freigabegrenze:** `RECIPE_JSON_IMPORT_VERIFIED=false`, `RECIPE_GENERATOR_HOST_PARITY_VERIFIED=false`, `PRODUCTION_REGISTRIES_VERIFIED=false`, `ANDROID_DEVICE_VERIFIED=false`, `INTEGRATED=false`. Maschinenlesbarer statischer Nachweis: [recipe-host-evidence.v1.json](../policies/recipe-host-evidence.v1.json). Der lokale Validator verifiziert ausschließlich Konsistenz der dokumentierten Pins und Freigabegates, **nicht** die externen CI-Läufe selbst. Keine fremden Repositories beschrieben.

## Eigener Architektur-Konsistenztest

[GitHub Actions 41272823110](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41272823110), Code-/Workflow-SHA `4b708914840933b441f206729196428692d58051`, Job `124748912712`, `completed/success`. Tatsächliche Ausgabe: `PASS recipe-host evidence ledger: 2 partial gates, 4 new JVM tests, 11 negative mutations`; parallel 16 positive/42 negative Vertragsfälle und 42 Händler-Policy-Gates. **Die vier JVM-Tests wurden in der Host-CI 41271956493 ausgeführt, nicht im Architekturvalidator.** Das eigene Skript prüft lediglich die statischen Belege, inklusive elf bewusst fehlerhafter Varianten.

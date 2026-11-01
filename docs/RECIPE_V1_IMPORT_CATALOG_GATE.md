# Rezept-v1-JSON-Import und Room-Katalogbelege – Integrationsgate

**Belegzeit:** 01.11.2026, 05:09 UTC (06:09 MEZ). **Rolle:** ausschließlich read-only Host-Audit und Architekturabnahme. **Status:** `PARTIAL_JVM_AND_SCHEMA_FIXTURE_VERIFIED_NOT_INTEGRATED`.

## Nachgewiesener Hoststand

Der vollständige [Host-CI-Lauf 41275499465](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41275499465) auf dem Codecommit [`d94f4a93`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/commit/d94f4a93b7e6f63a8ecfa3c620974e39e7d97609), Job `124756745519`, ist `completed/success`. Das tatsächliche Joblog meldet `BUILD SUCCESSFUL in 4m 8s` und **42 frische JUnit-XML, 307 JVM-Tests, 0 Failures, 0 Errors, 0 Skips, 7 befüllte Room-Migrationen**. Im selben CI-Job bestanden Lint, Android-Test**kompilierung**, Room-8-Schemaabgleich, **9 positive/14 negative** gepinnte `recipe.draft`-v1-Schema-Fälle und Python-Referenzaufrufe **9/9 compare_prices, 12/12 project_needs, 7/7 optimize_package_mix, 7/7 suggest_purchases**. Die sechs übrigen Python-Teilreferenzen bestanden ebenfalls. APK-Build und -Upload waren ausdrücklich **skipped**; **kein** Android-Geräte-/Emulatortest wurde ausgeführt.

| Belegter Meilenstein | Codecommit | Host-CI | JVM gesamt | Veränderung |
| --- | --- | --- | ---: | --- |
| Review und synthetische FoodStore-Kette | `3fb4b75f` | [41271956493](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41271956493) | 290 | +4 Rezepttests gegenüber 286 |
| Begrenzter v1-JSON-Import | `7bf45400` | [41273875502](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41273875502) | 303 | +13 Importtests |
| Unabhängiger Kontext-Zeitbeleg | `de6842a3` | [41274938362](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41274938362) | 304 | +1 Test |
| Room-gebundener Produktversionsbeleg | `d94f4a93` | [41275499465](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41275499465) | 307 | +3 Tests |

Die fehlgeschlagenen Zwischenläufe [41273621020](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41273621020) (API-26-Kompatibilität und Reviewstatus) und [41274210865](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41274210865) (fehlende `date-time`-Formatabhängigkeit im Python-Schema-Gate) wurden durch die nachfolgenden grünen Codecommits korrigiert; **die roten SHAs sind keine Freigabenachweise**.

## Was der Code tatsächlich schützt

- [`RecipeDraftBoundedJson.kt`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/d94f4a93b7e6f63a8ecfa3c620974e39e7d97609/app/src/main/java/de/ernaehrung/demo/data/integration/RecipeDraftBoundedJson.kt) begrenzt Zeichen, Tiefe und Knoten und weist doppelte JSON-Schlüssel, beschädigte Unicode-Sequenzen und ungültige Zahlen zurück.
- [`RecipeDraftV1Import.kt`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/d94f4a93b7e6f63a8ecfa3c620974e39e7d97609/app/src/main/java/de/ernaehrung/demo/data/integration/RecipeDraftV1Import.kt) akzeptiert nur `1.0.0-draft / recipe.draft`, überprüft konsumierte Felder, Offset-Zeit und Frische; modellbehauptete Bestätigungen, Nährwerte und Allergenfreiheit sind **keine** Hostbelege. Die acht Kontextflagkombinationen, fehlende oder zeitlich abweichende Host-Snapshots und negative Eingaben werden JVM-seitig geprüft.
- [`RecipeCatalogEvidence.kt`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/d94f4a93b7e6f63a8ecfa3c620974e39e7d97609/app/src/main/java/de/ernaehrung/demo/data/integration/RecipeCatalogEvidence.kt) löst `foodTypeId` nicht als Produktversion auf, sondern verlangt eine separate Bestätigung zur aktuellen Room-Produktversion, Revision, Versionzeit, Einheit und Quellenqualität. Unbekannte Allergene bleiben unbekannt.
- `FoodStore.previewRecipeDraftV1` liest die Room-Versionen in einem Transaktionssnapshot und ruft **keine** Rezept-/Herstellungs-/Verzehrbuchung auf. Die drei neuen [synthetischen Robolectric-Tests](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/d94f4a93b7e6f63a8ecfa3c620974e39e7d97609/app/src/test/java/de/ernaehrung/demo/RecipeCatalogEvidenceTest.kt) belegen diesen begrenzten Preview-Pfad.

## Offene, für Codex verbindliche Abnahme

1. **Runtime-Vertrag:** vollständige gepinnte Draft-2020-12-Schema-Validierung **jeder** eingehenden Rezeptnachricht, inklusive Format-/Negativfällen. Die neun/14 Schema-Fixtures laufen in **Python-CI**, nicht als Android-Laufzeitvalidator. Ein enger Kotlin-Decoder ist kein Ersatz.
2. **Modulparität:** echte `EG-Rezept-KI`-Generator- und `RecipeDraftRevalidation`-Referenz auf identischen synthetischen Inputs und vollständigen Ausgaben mit dem Host vergleichen; bekannte Unterschiede dokumentieren, nicht durch Reduktion der Testdaten kaschieren.
3. **Unabhängige Bestätigungen:** Nutzeraktion, Produktversionsrevision, Menge/Basis, RAW/COOKED, Allergen und Snapshotzeit mit einer hostseitigen, auditierbaren Registry verbinden. Die bisherige `ConfirmedLine`-Map wird vom Aufrufer übergeben; sie ist **noch kein** attestierter produktiver Bestätigungsdatensatz.
4. **Save-Time-TOCTOU:** beim **tatsächlichen** Rezeptsave Produktrevision, Zustimmung und Kontext erneut atomar prüfen. Test: Änderung der Produktversion **zwischen Preview und Save**, Storno, Neustart, parallele Änderungen und fehlende Fakten dürfen keine veraltete `RecipeInput`-Freigabe übernehmen. Keine automatische Herstellung oder Verbrauchsbuchung.
5. **Gerät und UI:** tatsächliche Android-Instrumentation für Nutzerbestätigung, Offline-/Privacy-Gates, Migration und gegebenenfalls lokales Modell ausführen. `compileDebugAndroidTestKotlin` genügt nicht. Keine produktive Livequelle ohne bestehende technische Rechtegates; keine neue separate Rechtsrecherche gemäß ADR-019.

**Vertrag:** `contracts/v1` bleibt `1.0.0-draft`, Blob `bedde4677342817fe6b883962c8dfbbd60100072`. `contracts/v1.1` bleibt ein separater Shopping-Draft. Keine Schema- oder Händler-Policy-Änderung und **keine** Modul-/Gesamtfreigabe. Das neue [statische Evidenzregister](../policies/recipe-v1-import-evidence.v1.json) und sein [Offline-Validator](../tools/validate_recipe_v1_import_evidence.py) prüfen ausschließlich dokumentierte Konsistenz, **nicht** die externen CI-/Kotlin-/Android-Ausführungen.

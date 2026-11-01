# `suggest_purchases` – begrenzte Python–Kotlin-Parität und Host-Freigabegate

**Stand:** 01.11.2026, 04:14 MEZ. **Zuständigkeit:** EG-Architecture (nur Vertrags-/Integrationsaudit; App-Code ausschließlich Codex). **Freigabe:** `PARTIAL_HOST_JVM_VERIFIED / FULL_SUGGEST_PARITY_PENDING / NOT_INTEGRATED`.

## Nachweise und exakt getrennte Teststände

- Letzter **abgeschlossener** Host-CI-Lauf vor der neuen Gesamtfunktions-Fixture: [41267961744](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41267961744), SHA `af309c38a880adb455050cd8c83d7b8552cba152`, Job `124734630660`, `completed/success`. Direkt aus dem Joblog: `JUNIT_XML: files=38 tests=272 failures=0 errors=0 skipped=0 migrations=7`, `BUILD SUCCESSFUL in 2m 57s`; Python-Vollaufrufe `compare_prices` 9/9, `project_needs` 12/12 und `optimize_package_mix` 7/7. Dieser Lauf **enthält noch nicht** die sieben `suggest_purchases`-Gesamtfunktionsaufrufe.
- Der **neuere** App-Commit [`cf8b25462ad24eb4528576e5d2a45d5ce0910937`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/commit/cf8b25462ad24eb4528576e5d2a45d5ce0910937) ergänzt `shopping_suggest_v1.tsv`, Kotlin-Test `sharedPinnedPythonSuggestPurchasesMoneyAndMixVectors`, `tools/check_shopping_suggest_reference.py` und den eigenen GitHub-Actions-Schritt. **Zum Erhebungszeitpunkt** ist [CI 41268235532](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41268235532) auf genau diesem Commit noch `in_progress`. Keine sieben Tests vor dem vollständigen CI-Nachweis als bestanden ausgeben.
- Gepinnte Python-Referenz: `EG-Einkaufsintelligenz@a3e13b147124ad7c25698a695e2ab42d7299a58a`, `eg_shopping.engine.suggest_purchases`. Host-Fixture `app/src/test/resources/integration/shopping_suggest_v1.tsv` Blob `8d3c5e636cc1af88f0748d4f7eefaa991d9aeb89`; Python-Checker Blob `10db7e7068bf813db35a9643dd1ca6af7ed82d0e`.

## Sieben gemeinsame synthetische Szenarien (noch nicht freigegeben)

| Fixture-ID | Zweck | Vergleichbare Ausgaben |
| --- | --- | --- |
| `single` | Ein FoodType, 25 Cent Pfand | Status, Mix, Waren-/Checkout-Cents, Restbudget |
| `two-foodtypes` | Sequenzielle zwei Bedarfszeilen | Beide Status, Mix, Summen, Restbudget |
| `cheaper-mix` | Zwei kleine Packungen günstiger als eine große | Optimierter Mix, Kosten |
| `verified-multibuy` | Zwei Packungen nur bei Host-bestätigter Mindestabnahme | Mix, Kosten |
| `zero-merchandise` | Bekannter Nullpreis statt unbekannter Preis | `0` in Waren-/Checkoutsumme |
| `zero-budget-free` | Bekannter Nullpreis bei Nullbudget | Zulässiger Nullkostenfall |
| `budget-unknown` | Budget unbekannt, nicht `0` | `REVIEW`, unbekanntes Restbudget |

**Wichtig:** Die Fixture liefert gemeinsame erwartete **Ergebnisfelder**, nicht identische Autorisierungseingaben. Die Python-Referenz läuft explizit mit `usage_context="RESEARCH_ONLY"` und synthetischen `UNVERIFIED`-Quellrechten; Kotlin läuft mit **separat bestätigten** Host-Registries für `APP_DISPLAY`. Deshalb darf selbst ein grüner 7/7-Lauf nur als **begrenzte fachliche Geld-/Mix-Parität**, nicht als identische Rechte-/Fehler-/Vollausgabeparität gelten. `sideEffects=[]` ist in beiden Testpfaden Pflicht.

## Bereits separat getestete Host-Schutzfälle

- Keine `FEASIBLE_NOT_PURCHASED`-Behauptung bei unbestätigten Rechten, Filiale, Artikelversion, Multibuy-Bedingung, unbekanntem Pfand, Budget, Lagerkapazität oder Haltbarkeit.
- Unterschiedliche **bestätigte** Mengenbasen (`NET` vs. `DRAINED`) dürfen sich bei der Abdeckungsprüfung nicht gegenseitig kontaminieren; der Host-Regressionstest war im [269-JVM-Lauf 41266557275](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41266557275) grün.
- Neue konservative Host-Regressionen zu Evidenz nach dem Einkaufstag, späterem Beobachtungstag trotz UTC-Offset und hypothetischem sequenziellem Restbudget waren im **272-JVM-Lauf 41267961744** grün. Das sind absichtliche Host-Verschärfungen, **keine** behauptete Python-Vollparität.
- Kaufvorschläge bleiben Vorschläge: keine automatische Zahlung, keine Bestandsbewegung, kein Schreiben eines Preisgedächtnisses.

## Verbindliche Restabnahme für Codex

1. Den neueren `cf8b2546`-CI-Lauf vollständig abschließen lassen und **auf demselben SHA** JUnit-XML, 7/7 echte Python-`suggest_purchases`-Funktionsaufrufe, Kotlin-Fixture-Test, sechs Teilreferenzen, 9+12+7 bisherige Vollaufrufe, Lint, Room-8-Schema und Android-Testkompilierung nachweisen; bei Fehlern **kein** Erfolgseintrag.
2. Vollständige strukturierte `suggest_purchases`-Ausgaben abgleichen: `items[].reasons`, `rejected[]`, `warnings[]`, `unknownNeeds[]`, `packageLines[]`, `snapshotComplete`, `optimalityProven`, `usedCapacityMl`, `savingsBasis`, Budget-/Pfand- und Rechtefelder. Unterschiedliche Python-`RESEARCH_ONLY`-/Kotlin-`APP_DISPLAY`-Entscheidungen ausdrücklich als Host-Delta erfassen.
3. Gemeinsame **negative** Funktionsaufrufe mit ungültigen/fehlenden Mengenbasen, anderem Store, Zukunfts-/Ablaufaktionen, beschädigten Zahlen, unbekanntem Pfand, mehrdeutigen Artikeln, gemischten Warenkörben, Filial-/Quellenrechtslücken, unvollständigen Bedarfssnapshots und Null-vs.-Unbekannt hinzufügen. Keine Testfixtures durch Weglassen von Sperrfällen „grün“ machen.
4. Echte **bestätigte** Host-Registry-Befüllung und durchgängige Bon→historischer Preis→Bedarf→Gebindemix→Kaufvorschlag-Kette mit idempotenter Bestätigung/Room-Migration testen. Ohne nachgewiesene Rechte keine produktive Fremdpreisanzeige. Keine zusätzliche eigenständige Rechtsrecherche gemäß ADR-019.
5. Android-Instrumentation auf Gerät/Emulator einschließlich Offline-/UI-/Kamera-/OCR-Grenzen tatsächlich **ausführen**. `compileDebugAndroidTestKotlin` allein reicht nicht; keine APK-Behauptung aus übersprungenem Milestone.

**Statusregel:** Bis zu den obigen Belegen `FULL_SUGGEST_PURCHASES_PARITY=false`, `ANDROID_DEVICE_VERIFIED=false`, `INTEGRATED=false`, `STABLE=false`. Die bestehenden v1/v1.1-Schemas und Händler-Policy 1.0.3 werden durch dieses Audit **nicht** verändert.

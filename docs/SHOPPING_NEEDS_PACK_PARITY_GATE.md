# Shopping-Host: FEFO-Bedarf und Gebindemix – Paritäts- und Integrationsgate

**Erhebung:** 01.11.2026, 03:21–03:30 MEZ. **Schreibzuständigkeit:** ausschließlich EG-Architecture. **Belegart:** aktuelle GitHub-Actions-Logs und read-only Code-/Fixture-Prüfung der Haupt-App sowie der gepinnten Python-Referenz. **Keine Freigabe** der Gesamtintegration.

## 1. Tatsächlich geprüfter Stand

- Haupt-App: [GitHub Actions 41263550103](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41263550103), Job `124721530890`, Commit `c32945c347027b14903299dd0d67c1c42e749d5a`, **completed/success** am 01.11.2026, 02:07 UTC. Direktes Joblog: `BUILD SUCCESSFUL in 3m 49s`; `JUNIT_XML: files=37 tests=260 failures=0 errors=0 skipped=0 migrations=7`; `JUNIT_XML_PASS`.
- Im **selben** Job wurden gegen `EG-Einkaufsintelligenz@a3e13b147124ad7c25698a695e2ab42d7299a58a` die tatsächlichen Python-Funktionen aufgerufen: `compare_prices` **9/9**, `project_needs` **12/12**, `optimize_package_mix` **7/7**. Die entsprechenden Kotlin-JVM-Tests lesen dieselben synthetischen TSV-Fixtures und vergleichen ausgewählte Resultatfelder mit denselben Erwartungen. Das ist **Teilparität auf 28 Testvektoren**, nicht vollständige Ausgabe-/Fehlerparität für alle Eingaben.
- `ShoppingNeedsKernel.kt` Blob `5f89f17661e82116ecde85e135d97ed28778a51f`; `ShoppingPackMixKernel.kt` Blob `3ee6489ab24b76323cfadec50e4dfd740e3fef63`. Python `pack_optimizer.py` Blob `e565b112adaee7adbc8d116a4575a60f71c6a654`.
- Fixierte Fixtures: `shopping_full_compare_v1.tsv` Blob `27f9a23679727ed793ad20a9c089ce04ea99ba67`; `shopping_needs_v1.tsv` Blob `8ada95b1a614d937a3c6afe83f6a56ece316e4fb`; `shopping_pack_mix_v1.tsv` Blob `360e06b5d821e484aa6242737566b6dafdb66d9d`.
- **Keine** Android-Geräte-/Emulatorausführung; `Build milestone APK` im CI explizit **skipped**. `compileDebugAndroidTestKotlin` ist nur Kompilierung, keine Instrumentation.

Der maschinenlesbare [Evidenzstand](../policies/shopping-host-pipeline-evidence.v1.json) wird von [Offline-Validator](../tools/validate_shopping_host_pipeline_evidence.py) geprüft. Der Validator prüft **nur Konsistenz und nicht selbst CI-Logs, Kotlin, Python oder Android**. Das frühere [Preisvergleichsregister](../policies/shopping-compare-acceptance.v1.json) bleibt als **historisch auf 249 JVM-Tests und 9 Full-call-Fälle gepinnter Nachweis** bestehen; seine älteren Zahlen sind nicht der aktuelle Host-Gesamtstand.

## 2. Was die gemeinsamen Vektoren tatsächlich vergleichen

| Pipeline | Gemeinsame echte Python-Funktionsaufrufe | Überprüfte Felder | Nicht abgedeckte Felder/Wege |
| --- | ---: | --- | --- |
| `compare_prices` | 9 | synthetische erwartete Vergleichsausgaben/Signale | große Negativmatrix, vollständige Host-Registries, acht Händler, historische Gesamttransaktion; siehe separates Preisvergleichsgate |
| `project_needs` | 12 | Bedarfssummen je **1/7/28/56 Tage**, unbekannte Event-IDs, `snapshotComplete` | vollständige eventweise `allocations[]`-/`unknownNeeds[]`-Details, Warning-Texte, gemeinsame Invalid-/Grenzfallparität, Room-Snapshot |
| `optimize_package_mix` | 7 | `status`, `costCents`, Produkt-/Packungs-Mix, `warnings[]` | `optimalityProven`, `rejected[]`, `usedCapacityMl`, Mengen- und Fehlerdetails, `minPacks/maxPacks`, bedingte Preise, Pfand, vollständige `suggest_purchases` |

Die sieben Gebindefälle decken einen exakten Mix, unbekanntes Budget, unbekannte Lagerkapazität, kurze Haltbarkeit, Budgetüberschreitung, Suchlimit und einen Einzelmix ab. Sie **belegen keine** vollständige Prüfung von Nullpreis-Ties, Obergrenzen, ungültigen Konditionen oder produktiver Checkout-Summe. Die zwölf Bedarfsfälle prüfen unter anderem FEFO-Einmalverbrauch, unbrauchbare Chargen, unbekannte Daten, Portionen-Doppelzählung, historische Baseline und Mengenbasis-Isolation.

## 3. Verbindliche nächste Abnahmeszenarien für Codex (nur Haupt-App)

1. **Bedarf: Vollresultat-Parität.** Gemeinsame Python-/Kotlin-Fixtures müssen für jede Allokation `eventId`, `foodTypeId`, `dueDate`, `quantityRequired`, `quantityToBuy`, `unit`, `basis`, `origin` vergleichen; ebenso `unknownNeeds[]`, `warnings[]`, `snapshotComplete` und keine Seiteneffekte. Nur Horizon-Totals genügen nicht.
2. **Bedarf: negative und zeitliche Grenzen.** Doppelte Lot-/Event-IDs, ungültige Datumswerte, 0/366/367-Tage-Horizonte, historische Ereignisse außerhalb des Beobachtungsfensters, fehlende Menge/Einheit, MHD unbekannt, unterschiedliche Mengenbasis, Plan am Rand des Horizonts. Bewusst strengere Kotlin-Grenze 366 Tage explizit als Host-Abweichung behandeln, nicht die Python-Referenz unbemerkt beschneiden.
3. **Gebindemix: vollständiges Ergebnis.** Gleiche Testeingaben müssen `status`, `items[]` (Menge/Kosten), `costCents`, `quantityBought`, `optimalityProven`, `rejected[]`, `warnings[]`, `usedCapacityMl` und `scope` prüfen; eine `SEARCH_LIMIT`-Antwort darf nie als optimaler Kaufvorschlag erscheinen.
4. **Gebindemix: Sperren und Randfälle.** `minPacks/maxPacks`, mehr als acht Varianten, genau 250.000/250.001 Suchknoten, Preis 0, Gleichstand/Sortierung, Kapazität exakt erreicht/überschritten, unbestätigter Coupon, abgelaufene `SALE`, `REFERENCE_OLD`, `HISTORICAL_PAID`, `ONLINE_LISTED` mit/ohne Versand, Pfand unbekannt und sehr große Ganzzahlen. Fehler oder konservative Ablehnung explizit abgleichen; kein impliziter Checkout-Preis.
5. **Host-Orchestrierung: `suggest_purchases` vollständig.** Erst nach bestätigten FoodType-/Produktversions-/Store-/Mengen-/Quellen- und `APP_DISPLAY`-Gates; alle Bedarfe, Preis-/Gebindevarianten, Budgetperioden, Lagerkapazität, Haltbarkeit, Pfand und unvollständige Coverage berücksichtigen. Der isolierte `optimize_package_mix`-Port ist **nicht** diese Gesamtfunktion.
6. **Transaktionskette und Geräte.** Synthetischer Bonentwurf → ausdrückliche Kaufbestätigung → genau eine historische Preisbeobachtung (Retry idempotent) → Preisvergleich zum korrekten `as_of` → FEFO-Bedarf → Gebindevorschlag, **ohne** implizite Lager-/Kauf-/Verzehrbuchung. Danach Room-/Compose-/OCR-/Offline- und Android-Geräte-/Emulatorausführung nachweisen.

**Freigabe:** `PARTIAL_OFFLINE_HOST_JVM_VERIFIED`; `FULL_COMPARE_PARITY`, `FULL_NEEDS_PARITY`, `FULL_SUGGEST_PURCHASES_PARITY`, `ANDROID_DEVICE_VERIFIED`, `INTEGRATED` bleiben **false**. Die Händler-Policy-Abweichung 1.0.1 (Preisdaten/Einkaufsintelligenz) zu 1.0.3 (Architektur) bleibt separat offen. Keine eigenständige juristische Recherche gemäß ADR-019.

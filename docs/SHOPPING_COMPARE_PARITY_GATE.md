# Python–Kotlin-Gesamtparität für Preisvergleiche – Integrationsgate

**Erhebung:** 01.11.2026, ca. 01:19 MEZ. **Eigentümer:** Architektursteuerung; dieses Dokument ist eine read-only Übergabe an Codex und die Fachmodule, **kein** Android-Code und keine behauptete Freigabe.

## 1. Reproduzierbar belegter Ausgangspunkt

| Komponente | Geprüfte Referenz | Was tatsächlich belegt ist |
| --- | --- | --- |
| Python Einkaufsintelligenz | `EG-Einkaufsintelligenz@a3e13b147124ad7c25698a695e2ab42d7299a58a`, `eg_shopping/engine.py` Blob `be47af89bd15d9129f9cedfb14bb7f6954032b99`; [CI 41232038282](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41232038282) | 134 synthetische Offline-Tests; vollständige Python-Funktion `compare_prices` vorhanden, aber nicht vollständig mit Kotlin verglichen |
| Android-Host | `Ernaerungsgedaechtnis@270c6144c84e44b00268fb40aa0830173fe42148`, nachfolgend nur Statuscommit `98ba72bce011689f23370f6e4bdcfe0b0e5fb118`; `ShoppingPriceComparisonGate.kt` Blob `d22b370f2cc81e84d2b42dcf1e42d4413a6c7c68` | [CI 41255825754](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41255825754), Job `124698655449`, **completed/success**. Direktes Joblog: `JUNIT_XML: files=33 tests=240 failures=0 errors=0 skipped=0 migrations=7`, `JUNIT_XML_PASS`, Gradle `BUILD SUCCESSFUL in 3m 48s`. |
| Gepinnte Referenzvektoren im selben Host-Run | Python-Originale aus Produktdaten/Einkaufsintelligenz | **35/35** historische Bonpreise, **17/17** Bonzuordnung, **18/18** Mengen/Grundpreis, **37/37** Gültigkeit/Store, **40/40** Vergleichbarkeit, **24/24** Coverage. **Sechs Teilfunktionen**, kein kompletter `compare_prices`-Aufruf mit identischem Gesamtinput. |
| Architektur-Policy | `EG-Architecture` Policy **1.0.3**, Blob `7ed2ef6918c8fdcdb9c482cb0a38eb38e5f6852c` | Host `RetailerPolicy` hat die drei Fähigkeiten implementiert. Preisdaten und Einkaufsintelligenz vendoren noch **1.0.1**, Blob `06a05d5c47be8d67fb75dfca11821d8793be86fb`; die dritte Katalogfähigkeit und ADR-019-Workflow-Direktiven fehlen dort. |

**Wichtig:** Die erfolgreiche CI bestätigt die **synthetische Host-Komposition** mit 240 JVM-Tests und sieben Room-Migrationsfällen, **nicht** die vollständige Fachparität, reale Host-Registries, Android-Gerätetests, externe Datenrechte oder Händlerabdeckung. Der aktuelle Host-Port schreibt weder Kauf noch Lager.

## 2. Tatsächliche öffentliche Funktionen und Ergebnismengen

**Python:** `compare_prices(target, observations, shopping_date, *, as_of, coverage, matches, allowed_stores, allow_online, historical, usage_context, rights_grants)` aus `eg_shopping/engine.py`. Rückgabe: `alternatives[]` (exakte Grundpreisrate, Zielmengen-Differenz, Bio-/Vergleichbarkeitsstatus), `signals[]`, `incomplete`, `gaps[]`, `otherDayOffers[]`, `rejected[]`, `bestPriceClaim`; bei ungültigem Ziel auch `DomainError`.

**Kotlin:** `ShoppingPriceComparisonGate.compare(target, candidates, coverage, matches, permissions, stores, articles, substitutions)`. Rückgabe: `targetEligible`, `cheaper[]`, `excluded`, `signals` und stets `marketWideBestPriceProven=false`. Vor dem Vergleich prüft der Host unabhängige Rechte-, Store-, Produktversions-/Bio-, Angebots-, Datums-, Mengen- und Mengenbasis-Gates. Host-Registries sind im Test künstliche Trust-Anker, noch nicht mit echten bestätigten Stammdaten verbunden.

Die zwei Funktionen haben **nicht denselben Transportvertrag**. Ein belastbarer Paritätstest benötigt einen expliziten, versionierten Normalisierungsadapter: identische synthetische fachliche Beobachtungen auf beiden Seiten, dokumentierte Abbildung von Rechten/Produktversion/Store und dann Vergleich **fachlich gleichwertiger Ergebnisfelder**. Nicht durch Weglassen eines strengeren Host-Gates künstlich Gleichheit herstellen.

## 3. Bekannte semantische Unterschiede – ausdrücklich zu testen

| Fall | Python-Referenz | Aktueller Kotlin-Host | Abnahmeregel |
| --- | --- | --- | --- |
| `RESEARCH_ONLY` / `UNVERIFIED` | Kann synthetische Beobachtungen zu Forschungszwecken vergleichen | Preis-Host-Port nur `APP_DISPLAY`, externe Anzeige ohne Host-Rechtegrant gesperrt | **Beabsichtigte Sicherheitsschranke**, kein Paritätsfehler; getrennte Vergleichsmodi |
| Store nur `CHAIN_REGION` | In nicht-historischen Vergleichen teils mit Warnung akzeptiert | `STORE_CONFIRMED` plus unabhängige Registry zwingend | Konservative Host-Abweichung dokumentieren; keine künstliche Store-Bestätigung |
| `SALE` aus gezielter Produktabfrage | `source_policy.source_gate` trennt `acquisitionMode` vom `priceKind`; ein gezielter Abruf kann einen Aktionspreis liefern | `ShoppingOfferGate` erlaubt `SALE` derzeit nur für `PUBLISHED_OFFER_COLLECTION`, nicht für `TARGETED_PRODUCT_PRICE_QUERY` | **Funktions-/Paritätslücke zur Entscheidung**, ob nach belegter Provenienz und Sale-Gültigkeit ein gezielter Sale-Preis zulässig sein soll; keine automatische Umdeklaration als Angebotsfeed |
| `CONFIRMED_BY_USER`-Substitution | Match-Eingabe allein kann funktionale Ersetzung erlauben | Zusätzlich unabhängige `ConfirmedSubstitutionRegistry` mit Versionspaar und Cutoff; Default DENY | Strengeres Host-Gate beibehalten, gefälschte Match-Texte müssen scheitern |
| Zielbeobachtung in `observations[]` | Ein identischer Ziel-Eintrag wird einmal ignoriert | Alle Observation-IDs einschließlich Ziel müssen eindeutig sein | Normalisierungsregel festlegen: Ziel beim Kotlin-Aufruf aus Kandidaten entfernen; weitere Duplikate ablehnen |
| Nicht am Einkaufstag gültiges Angebot | `otherDayOffers[]` als gesonderte Information | `excluded`/Gaps, derzeit kein gleichwertiges `otherDayOffers[]`-Feld | Ausgabe-/DTO-Parität offen; nie als aktuell günstiger behandeln |
| Zielpreis nicht anzeigefähig | `DomainError` bei ungültigem Ziel | `targetEligible=false` und Grausignal | Fehlerklassen semantisch abgleichen; nicht einfach `[]` als gültigen Vergleich interpretieren |
| Unbekannter Pfand-/Checkoutbetrag | Merchandise-Grundpreis kann vergleichbar sein; Checkout bleibt unbekannt, Gap | Gleiches konservatives Grundprinzip | `MERCHANDISE_ONLY`; kein belegter Gesamtbetrag oder Sparbetrag aus unbekanntem Pfand |
| Katalog-Fähigkeit | Python-Policy 1.0.1 kennt sie nicht | Kotlin-Policy 1.0.3 kennt sie, `ExternalPriceBridge` blockiert Katalog als direkte Preisbeobachtung | Katalogposition erst über geprüfte Angebotsbeobachtung; kein direkter Katalog→Anzeige-Bypass |

## 4. Verbindliche synthetische Gesamt-Testmatrix für Codex

Die **gleichen** kanonischen Fachfälle mit vollständig belegtem Zielpreis, Produktversion, Markt, Zeitpunkt, Mengenbasis, `APP_DISPLAY`-Rechtegrant und Host-Registries auf beiden Seiten abbilden; für absichtlich abweichende Modi explizite `expectedDivergence`-Kennzeichnung statt heimlichem Überspringen:

1. Gleiche funktionale Ware, gleicher belegter Bio-Status, günstiger → **RED**, exakte rational berechnete Zielmengen-Differenz.
2. Belegter anderer Bio-Status, günstiger → **ORANGE**; Rot und Orange dürfen zusammen auftreten.
3. Unbekannter Bio-Status oder unvollständige Coverage → **GREY** ohne erfundene Rot-/Orange-Einstufung; Grau kann zusätzlich zu Rot erscheinen.
4. Zwei gleich günstige Alternativen → deterministische Sortierung nach exakter Grundpreisrate, dann Observation-ID; kein nominaler Packungspreis als Sortierbasis.
5. Falsche Menge/Einheit/Basis, fehlende Artikelversion oder kritisches Produktattribut → Ausschluss und Coverage-Gap.
6. `UNVERIFIED`/`RESTRICTED`, fehlender Rechtegrant, falscher Store/Region, unbestätigte Produktversion → **keine APP_DISPLAY-Freigabe**.
7. Beobachtung nach `as_of`, abgelaufene/nicht veröffentlichte Aktion, `HISTORICAL_PAID` als aktuelles Angebot → ausgeschlossen; keine rückwirkende Zukunftskenntnis.
8. Coupon/App-/Mehrfachkaufbedingungen nicht nachgewiesen → nicht als uneingeschränkter Kassenpreis; Pfand `null` bleibt unbekannt.
9. Gefälschter Substitutionsmatch, falsches Produktversionspaar, falscher Cutoff, Registry-Ausfall → keine automatische Substitution; positiv nur mit hostbestätigter Entscheidung.
10. Identische Observation-ID, fehlerhafte Zielbeobachtung, über 256 Kandidaten → explizite, reproduzierbare Fehler-/Grenzbehandlung.
11. Vier erlaubte reguläre Preisabfrage-Händler und vier **nur Angebot**-Händler, jeweils positive/negative Fähigkeiten; Katalogerfassung ausschließlich vier Händler, ohne direkten Preis-Display-Bypass.
12. Bon-Scan→Entwurf→explizite Kaufbestätigung→genau eine historische Preisbeobachtung→Vergleich→Bedarfsprojektion; Retry/Storno/zweiter echter Kauf, keine ungefragte Lager-/Kauf-/Verzehrbuchung.

**Ergebnisabgleich:** Für gemeinsame zulässige Fälle `targetEligible`/Zielvalidität, sortierte Alternativen-IDs, exakte Rate als Zähler/Nenner, Zielmengen-Delta nur bei ganzzahligem Cent, Vergleichbarkeits- und Bio-Status, RED/ORANGE/GREY, Unvollständigkeit und `CHEAPEST_KNOWN_MATCHING_ONLY` prüfen. Abweichende Ablehnungsgründe und zusätzliche Host-Sperren als bewusstes Delta dokumentieren. Test darf nicht allein aus sechs separaten Python-Teilfunktionschecks bestehen; mindestens **ein vollständiger Python-`compare_prices`-Aufruf pro gemeinsamem Testfall** und die entsprechende Kotlin-Host-Komposition sind nötig.

## 5. Eigentümer, Reihenfolge, Freigabe

1. **Codex (nur Haupt-App):** Gemeinsame synthetische E2E-Vektoren und Normalisierungsadapter implementieren, tatsächliche Python-`compare_prices`-Ausgaben gegen Kotlin-Ergebnisse prüfen, alle bewusst strengeren Host-Gates erhalten; echte lokale Store-/Artikel-/Substitutions-Registries und No-Side-Effects nachweisen. Zuerst die `SALE`-bei-gezielter-Abfrage-Abweichung fachlich entscheiden, ohne Rechte-/Quellen-Gates zu schwächen.
2. **Preisdaten/Einkaufsintelligenz (je nur eigenes Repo):** Policy 1.0.3 mit drei Fähigkeiten und ADR-019-Workflowregel bewusst übernehmen, danach echte Tests und dokumentierte SHA-Parität; kein Livezugriff allein wegen Policy-Version. Rezept-KI und Produktdaten nur bei konkreter Adapterbetroffenheit.
3. **Architektursteuerung (nur EG-Architecture):** CI/Schema-/Policy-/Adapterbelege erneut lesen, Abweichungen dokumentieren, keine automatische `1.1.0-draft`-Freigabe.

**Freigabestatus:** `DRAFT_CI_VERIFIED / ISOLATED_HOST_COMPOSITION_JVM_VERIFIED / FULL_COMPARE_PARITY_PENDING / DEVICE_PENDING`. Keine gesonderte neue juristische Recherche gemäß ADR-019; bestehende technische Rights-/Access-Gates bleiben bestehen.

# Codex – Integrationsplan der vier Fachmodule (nur lesender Übergabeauftrag)

> **Neueste verbindliche Arbeitsanweisung (ADR-019, 31.10.2026):** Codex soll **keine separaten rechtlichen Recherchen/Prüfprojekte** zu öffentlich beworbenen Händlerpreisen oder Katalogen mehr durchführen, keine neuen Lizenzanfragen anstoßen und die Diskussion nicht ohne ausdrückliche Nutzerinitiative wieder öffnen. Stattdessen Integration und technische Tests fortsetzen. Der bestehende Rights-/Source-Status bleibt wahrheitsgemäß und die technischen Zugriffsgrenzen gelten weiter; dies ist **keine** neue Aufgabe, alle Nutzungsrechte einzeln zu untersuchen. Nicht aktivierte externe Livefeeds dürfen die Offlineintegration nicht blockieren. Details: [ADR-019](ADR_019_NO_SEPARATE_LEGAL_REVIEWS.md).

**Stand der ursprünglichen Planung: 31.10.2026.** **Aktueller belegter Host-/Abnehmerstand: [Integrationsaudit 01.11.2026](INTEGRATION_EVIDENCE_2026-11-01.md).** Die untenstehenden Ausgangszahlen sind historische Planungswerte; die Haupt-App hat inzwischen Room 8 und isolierte JVM-geprüfte Ports. **Dieses Dokument selbst ist keine ausgeführte App-Integration.** `Ernaerungsgedaechtnis` ist ausschließlich das Schreibrepository von Codex. Architektur- und Fach-Chats **ändern die Haupt-App nicht**.

## A. Ausgangslage
- Haupt-App letztes erfasstes Release `0.9.0-recognition`, Room 7, 35 Tabellen, APK/183 JVM-Tests aus Phase 5; keine aktuelle native Geräte-OCR-Abnahme.
- Produktdaten: 105 Offline-Tests, Referenzengine Python, mit Alias-/Filialkontext und bestätigten historischen Preiserfassungen.
- Preisdaten: 77 Offline-Tests, acht Händler als Quellen-Adapter, **produktive Drittquellenrechte und mehrere Livepfade ungeklärt**.
- Einkaufsintelligenz: 82 nachgewiesene Tests beim dokumentierten Meilenstein, danach Codeänderung für Preisbeleg-/Pfand-/Budgetprüfung → neueste Version **erneut vollständig** mit CI belegen.
- Rezept-KI: 78 Kotlin-/Schema-Tests, Offline-Generator/Validator und getesteter Modellport, **kein echter on-device LLM-/Gerätetest**.
- EG-Architecture: `v1/1.0.0-draft` bleibt unverändert. `v1.1/1.1.0-draft` ist nur eine zusätzliche, **noch nicht produktiv freigegebene** Version für Shopping-DTOs. Nicht still aktualisieren.

## B. Arbeitsreihenfolge – Integrationsgates
1. **Read-only Inventur**: HEAD-SHAs, AGENTS.md/STATUS.md/ACCEPTANCE.md/INTEGRATION.md aller fünf Repos, bestehende FoodStore-Methoden und Room-Schema lesen; eingefrorene Versionen dokumentieren. Keine privaten Daten zu Testzwecken exportieren.
2. **Vertrags-/DTO-Matrix**: Eingabe-/Ausgabeports, betroffene App-Datenklassen, Haupt-Schreibtransaktionen, Nullable-/Null-/Cent-/Mengen-/Bio-/Händler-/Store-/Datum-Felder und erlaubte Datenrechte pro Modul mappen. Erweiterungen v1.1 nur nach Freigabe, bis dahin private DTO-Adapter.
3. **Produktdaten zuerst**: bestehenden Barcode-/Bon-OCR-Zweig über reine Matchfunktionen und Händler-/Filial-/Versionsaliase erweitern. App bleibt einzige Stelle, die Käufe bestätigt, Zahlung bucht oder Lagerzugänge erzeugt. Synthetische End-to-End-Testfälle: unbestätigter Bon → KEINE Buchung; bestätigter Kauf → genau EINE `HISTORICAL_PAID`-Preisbeobachtung; identischer Scan/Retry → keine zweite; getrennte identische Käufe → beide erhalten.
4. **Einkaufsintelligenz danach**: Kotlin-Port der deterministischen Preis-/Grundpreis-/Warn-/Bedarf-/Budget-/Haltbarkeitshandhabung anhand genau der veröffentlichten Python-Fixures. End-to-End-Szenario mit roten/orangen/grauen Signalen, bekannten/unbekannten Warenpreise, Pfand und Filialdatum.
5. **Preisdatenadapter**: nur synthetische/offline und nachweislich genehmigte externe Quellen. Bei App-Anzeige `APP_DISPLAY` den **doppelten Rechtefilter** implementieren (Preisdaten + Einkaufsvergleich/App-UI). Unverifizierte Quellen dürfen nicht durch einen Direktimport aus `Try` den Filter umgehen. Bei nicht nutzbaren Quellen Coverage-Warnungen statt falscher Bestpreise.
6. **Rezept-KI**: bereits real testbaren Kotlin-Kern in eine eigenständige Modulschicht integrieren; Offline-Fallback ohne Cloudkosten, separate Nutzerflags `considerStock`, `considerShopping`, `considerOffers` (8 Kombinationen), Allergene, portionsbezogene Nährwerte, keinerlei Buchung. Optionales Android-Modell erst mit Geräteverfügbarkeit, Datenschutz und Instrumentation-Test.
7. **Migration/Regression**: bestehende Room-1..7-Migrationspfade, Versions-/ID- und Kauf-/Bestandsvorgänge, Bild-/OCR-/Barcodes, Nutzerinteraktion und Offline-Verhalten vollständig testen. Keine tatsächliche Datensicherung/Migration aus dem Google Sheet ohne ausdrückliche Freigabe; keine Tests mit realen Bons.
8. **Integrationsstatus:** Ein Modul darf `INTEGRATED` erst nach erfolgreicher App-JVM-/CI-/Migration-/Gerätetestprüfung erhalten. Bei fehlendem physischem Gerät ausdrücklich nur `JVM_INTEGRATION_VERIFIED`, nicht Hardwarefreigabe.

## C. Erforderliche synthetische End-to-End-Testkette
**Bonbild- oder OCR-Testfixture → Bonentwurf → Produkterkennung (GTIN/SKU/Bonalias) → ausdrückliche Bestätigung → idempotente Kauf-/Positionsbuchung → datierte historische Preisbeobachtung → Artikel-/Grundpreisvergleich zum damaligen Zeitpunkt → retrospektive Auswertung ohne Hindsight → Einkaufsbedarfsvorschlag ohne Lager-/Verzehrbuchung**.

Varianten: mehrere plausible Produkte, Händlerwechsel und Filiale, falscher Barcode, verlorenes Dezimalkomma, Bonrabatt/Pfand, unbekanntes Abtropfgewicht, alte Produktversion, negative Retourenposition, gleiche Bonaufnahme zweimal, identischer zweiter realer Kauf, Filial-/regionale Preisabweichung, unterstellter Coupon, unbekannte Quelle/rechtlich gesperrte Quelle.

## D. Integrations-Prüfmatrix (Gate)
| System | Positive Tests | Zwingende Sperrtests |
| --- | --- | --- |
| Datenmodelle | Fachmessages validieren, IDs/Versionen erhalten | Null≠0, float→cent Rundung, fehlende Herkunft |
| OCR+Produktdaten | eindeutiger bestätigter Alias → historische Beobachtung | mehrdeutiger/stale Alias, fehlender Händler, unbestätigter Entwurf |
| Kauf/Bestand | atomare Buchung einmalig | Doppelbuchung bei Retry, Scan bucht nicht |
| Preisvergleich | faire g/ml-/kg/l-Raten und Bio/Warnsignale | falsche Menge, Coupon, alte Aktion, fehlende aktuelle Quellenrechte |
| Historie | damals bereits beobachtete und gültige Alternativen | künftige Preisbeobachtung, anderer Markt, Versand/Pfand unklar |
| Einkaufen | korrekte Packungszahl, Cash-Budget inklusive Pfand | unterstellte Lagerkapazität, mehrere offene kumulative Horizonte |
| Rezepte | Generator/Validator und 8 Flags | ungeprüfte Allergie, nicht belegte Ernährung/Werte, Plan≠Ist |
| Persistenz | alle alten Tabellen/Versionen unverändert | geänderte Room-Migration, verlorene Zahlungs-/Beleg-ID |
| Geräte | OCR, Kamera, Barcode, optional lokales LLM | nicht unterstützte Hardware oder Offlinefehler |

## E. Explizit nicht beauftragt
Keine Änderung an fremden Fachrepos oder Architektur durch Codex. Bei fehlender Vertragsschnittstelle schriftlicher Änderungsantrag an Chat 1. Keine ungefragte produktive Sheet-Migration, keine verdeckte Datenübertragung in Cloud-AI, keine gebührenpflichtige API, keine ungeklärte Live-Quelle in die Nutzungsoberfläche. Der bereits angekündigte Phase-6-Datenaustausch der Haupt-App bleibt **separater eigener Entwicklungsmeilenstein**; er darf nicht still als erledigt oder automatisch durch die Module ersetzt werden.

## F. Statusführung für Codex
Bei jedem App-Merge/Integrationsabschnitt: geprüftes Modul-SHA, Vertrag, geänderte Dateien, Adaptermapping, ausgeführte Befehle/Pass/Fail/Skip, unveränderte Bestands-/Kaufsicherung, Geräteteststatus, aktueller APK-Teststand in der **privaten Haupt-App** dokumentieren. Commit-/Workflow-Ergebnis ist nicht gleich Hardwarefreigabe.


## G. Aktuelle Händler-Funktionsmatrix für Android/Codex
Beim Android-Port **ADR-016** und [RETAILER_SOURCE_POLICY.md](RETAILER_SOURCE_POLICY.md) zwingend berücksichtigen. Gezielte Produktpreisabfrage nur für ALDI Nord/Süd, REWE und Lidl; veröffentlichte Angebotsdaten auch für Penny, Kaufland, EDEKA und Netto Marken-Discount; bei diesen vier Händlern keine gezielte reguläre Produktpreisabfrage. Händlerpreis- und Angebotsdaten sind separate Fähigkeiten. Produktivnutzung nur nach Rechts-/Quellenprüfung, nicht durch die Nutzerfunktionsentscheidung selbst; keine Umbuchungen oder pauschal unterstellte Filialabdeckung. Negative Kotlin-Tests für die vier ausgeschlossenen Normalpreis-Abfrage-Händler und für `UNVERIFIED`/`RESTRICTED` bei `APP_DISPLAY` ergänzen. Diese Dokumentation ist nur Übergabe, keine erfolgte App-Änderung.


### Präzisierung ADR-018 – Angebotspreise und Katalogquellen (31.10.2026)
**Die veröffentlichten Angebotspreise sämtlicher acht Händler** sind als projektseitig zu erschließende Daten vorgesehen. Zusätzlich soll der Host **Angebotskatalog-Listen für ALDI Nord, ALDI Süd, Lidl und REWE** als getrennte Fähigkeit nutzen können (einzelne Aktionspositionen mit Gültigkeit, Quelle und Regionsbezug). Für Penny, Kaufland, EDEKA und Netto Marken-Discount **nur Einzel-Angebotspreise**, **keine** Katalog-Erschließung im aktuellen Projektumfang; weiterhin keine gezielte reguläre Produktpreisabfrage.

Kotlin-Gates am `policies/retailer-source-capabilities.v1.json` **aktuelle kanonische Policy-Version 1.0.3** (drei getrennte Händlerfähigkeiten; zusätzliche ADR-019-Arbeitsdirektiven) nachweisen; positive und negative Tests pro Händler. Das ändert weder `contracts/v1` noch das noch experimentelle `contracts/v1.1`. **Keine fremden Vollprospektbilder/kompletten Datenbankbestände spiegeln** und APP_DISPLAY-/Nutzungsrechte unabhängig bestätigen. Bei ungeprüften Quellen Deaktivierung einzelner Connectoren, aber kein Stopp der Offlineintegration. Kein selbstständiges Schreiben in Architektur/Modul-Repos.


## H. ADR-017: nachgeschärfte Shopping-v1.1-Draft-Adapter (offen)
Beim späteren v1.1-Kotlin-Port [ADR-017](ADR_017_SHOPPING_RESOLUTION.md) und den aktuellen `contracts/v1.1`-Schema-Blob **neu** einlesen: `unknownNeeds[]` enthält unbekannte Einheiten ohne fiktive `Quantity.unit`; `packageLines[]` enthält einzeln belegte Produkt-/Gebinde-/Preis-/Pfandzeilen; `savingsBasis=MERCHANDISE_ONLY` ist Pflicht für historische Vergleiche. Kein automatisches Durchreichen der alten, nur untypisierten `mix[]`-Extension. Negative Host-Tests: doppelte IDs, `COMPLETE` mit unbekanntem Bedarf, fehlender Preisbeleg bei behaupteter Gesamtsumme, Produkt-Mix mit angeblichem Einzelprodukt, unbekanntes Pfand mit Checkout-Zahl, historische Checkout- statt Warenpreisersparnis. Der bestehende v1-Adapter bleibt unverändert; Freigabe nach Modulparität und Codex-JVM-/App-Regression.

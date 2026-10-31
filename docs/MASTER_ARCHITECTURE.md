# Gesamtarchitektur – unabhängige Zuliefermodule
**Vertragsstand:** 1.0.0-draft · 31.10.2026 · Eigentümer: Architektursteuerung (Chat 1)

## 1. Ziel und Schnitt des Systems
„Ernährungsgedächtnis“ ist eine Android-Anwendung für Vorräte, Ernährung, Meal-Prep, Rezepte, Planungen und Einkauf. Die spezialisierten Chats entwickeln **unabhängige, integrierbare Produkte**, keine konkurrierenden Gesamtsysteme. Sie sollen End-to-End-Funktionalität im jeweiligen Fachgebiet liefern und diese nachweisen.

Die fachlichen Verträge legen Bedeutung und Grenzen der Daten fest. Sie **verlangen keine Übernahme des internen Room-Schemas**. Jedes Modul besitzt eigene interne Modelle und einen klaren Ein-/Ausgabe-Adapter. Die eigentliche App-Datenhaltung, UI, Transaktionen und Datenmigration bleiben bei Codex.

## 2. Ausgangsbasis und Grenzen (Stand 30./31.10.2026)
- Privates Android-Hauptrepository `ecora2003-max/Ernaerungsgedaechnis` – **für alle Fach-Chats lesbar, niemals schreibbar**; Codex integriert.
- Letzte eingesehene Übergabe: `docs/UEBERGABE_2026-10-30_PHASE5.md`, Demo `0.9.0-recognition`, Room-Schema **7** mit **35 Tabellen**, 183 ausgeführte JVM-Tests ohne Fehler. Keine reale Produktivmigration, Hardwaretests der nativen OCR/Kamera noch offen.
- Vorhanden: produktversionierte Artikel, Chargen, Ereignisse, Herstellung und Verzehr, Planung/Restbedarf, Einkaufslisten-/Preis-/Budgetgrundlagen, Barcode- und Bon-OCR, bestätigbare Händler-/Bon-Aliase.
- Lokale App-Datenbank `food-local-sandbox.db` ist Testbereich. Produktives Google Sheet (Schema **1.1.0** bei Planungserstellung) bleibt separate, einzige produktive Quelle für tatsächlich berichtete Ernährungs-/Vorratsereignisse. **Keine Entwicklungsgruppe liest, schreibt oder importiert produktive personenbezogene Daten für Tests.**
- `EG-Preisdaten` (vormals `Try`) enthält Python-Referenzadapter und Live-Berichte; diese sind keine freigegebene, vollständige oder lizenzierte Händlerplattform.
- Ältere Standangaben sind **Momentaufnahmen**, keine Nachweise über den momentanen neuesten Commit; vor jeder Integrationsplanung Status frisch lesen.

## 3. Repository-Lese- und Schreibgrenzen
| Rolle | Leserechte (Arbeitsregel) | Einzige zulässige Schreibziele |
| --- | --- | --- |
| Architektur-Chat | Architektur, Module, ggf. privates Hauptrepo | `EG-Architecture` |
| Preisdaten-Chat | Architektur, alle Module, Hauptrepo | `EG-Preisdaten` |
| Produktdaten-Chat | Architektur, alle Module, Hauptrepo | `EG-Produktdaten` |
| Einkaufs-Chat | Architektur, alle Module, Hauptrepo | `EG-Einkaufsintelligenz` |
| Rezept-Chat | Architektur, alle Module, Hauptrepo | `EG-Rezept-KI` |
| Codex | alle | nur das ausdrücklich beauftragte Integrations-Repository |

**Wichtig:** „Hauptrepo nur lesen“ und „Architektur nur lesen“ sind Anweisungen. Für technisch erzwungene Zugriffstrennung sind GitHub-Berechtigungen separat einzuschränken. Ein Chat darf auch bei technisch vorhandenen Schreibrechten die Grenze nicht überschreiten. Änderungen an Fremdrepos nur über Vorschlagsdokument/Issue im eigenen Repo, niemals über direkten Commit oder PR aus fremder Schreibsitzung.

## 4. Verantwortung je Modul
| Modul | Eigentum / Eingabe | Liefert | Ausdrücklich **nicht** |
| --- | --- | --- | --- |
| **Preisdaten** | Händler-Adapter, Filialreferenz, Zeitraum, Suchbegriff, öffentliche Katalog-/Aktionsquellen | datierte rohe/normalisierte Produkt- und Preisbeobachtungen, Angebotsgültigkeit, Abdeckung, Lizenz-/Zugriffshinweise | Rankings, persönliche Einkaufsvorschläge, Buchungen |
| **Produktdaten** | Produktmetadaten, Bon-/Barcode-Hinweise, bestätigte Transaktionsauszüge | Produktzuordnungen, Aliasentscheidungs-Vorschläge, qualifizierte Preisbeobachtungen | eigenständige Bon-OCR- oder Bestandsdatenbank; ungeprüfte Auto-Buchung |
| **Einkaufsintelligenz** | bestätigte/angezeigte Preise, Zuordnung und verfügbare zeitgebundene Planungssnapshots | Preisvergleiche/Signale, Kauf- und Budgetvorschläge, Abdeckung/Fallstricke | Live-Scraping, direktes Lager-Schreiben, Rezeptgenerierung |
| **Rezept-KI** | optionale Ernährungskontexte, verfügbare Angebote, Planungs-/Bedarfs-Snapshots | strukturierte **Rezeptentwürfe** mit Kandidaten, Zutaten, Portionen, Hinweisen und Lücken | tatsächliches Kochen, Buchen, Erfinden von Nährwerten oder Verträglichkeitsgarantien |
| **Codex** | Modul-Ausgaben und Fachverträge | Adapter auf Room/Compose, Gesamtintegration, reale App-Tests, Migrationen | stilles Übergehen von Warnungen/Datenherkunft |

## 5. Datenfluss, Daten-Eigentum
`Preisdaten → (Produktdaten/Identität) → Einkaufsintelligenz`; `Rezept-KI` kann optional auf **standardisierte, explizit bereitgestellte Snapshots** von Preisen, Vorräten und Einkaufsbedarf zugreifen. Die Produktdaten-Engine kann bestätigte Bonpositionen in historische Beobachtungen umwandeln; diese werden wieder als Preisdatenquelle für Vergleiche bereitgestellt. Dieser logische Kreis ist **kein** gegenseitiger Laufzeit-Import. Abhängigkeiten werden über unveränderliche Nachrichten, Mock-Fixtures und Adapter getrennt.

**Datenhoheit:** Nur die Haupt-App bestätigt tatsächliche Käufe, Kassenbonauflösungen, Preisbeobachtungen aus bestätigten Käufen, Bestandszugänge, Herstellung und Verzehr. Externe Module liefern Vorschläge/Snapshots, keinen direkten Schreibbefehl. Die Vergleichs-Engine erhält einen freigegebenen Preis-Snapshot und schreibt nichts.

## 6. Preisvergleich und Anzeigenlogik
Vergleichsschichten: **alle acht Händlerangebote untereinander** plus **verfügbare reguläre Preiskatalog-/Suchergebnisse** (insbesondere Lidl, ALDI Nord/Süd und REWE, aber ohne unbegründete Vollständigkeitsgarantie) plus bestätigte historische Bonpreise. Gleiches Produkt, Produkte derselben funktionalen Kategorie, Marke/Eigenmarke und Bio-Status bleiben verschiedene Dimensionen.

- **Rot:** Ein **nachweislich aktuell/zeitgerecht** günstigeres, funktional vergleichbares Produkt mit **gleichem Bio-Status** ist gefunden. Marken-/Eigenmarkenwechsel darf rot sein, wenn Merkmale zum Vergleich passen.
- **Orange:** Eine günstigere funktionale Alternative mit **anderem Bio-Status** ist gefunden; Unterschied explizit benennen.
- **Grau:** `Könnte es günstiger geben`, wenn relevante Vergleichsdaten fehlen, veraltet oder unklar sind. **Kein Beweis**, dass tatsächlich ein besserer Preis existiert.
- **Keine Warnung** ist **kein** Vollständigkeits- oder Bestpreisnachweis. Rot/Orange/Grau können zusammen auftreten; die Engine gibt **mehrere Fakten/Signale**, keine exklusive Ampel zurück.
- Grundpreis nur bei nachweislich kompatibler nutzbarer Masse/Volumenmenge in €/kg bzw. €/l; Stückware bleibt Stückware. Kaufpreis, Gebindeanzahl, Pfand, Coupons, App-Bedingungen, regionale Gültigkeit und Verfügbarkeit separat halten.
- Eine reguläre Vergleichspreisangabe, UVP, `oldPrice`, historische Preisbeobachtung und tatsächlich beobachteter Kaufpreis sind **nicht austauschbar**. Keine pauschale Behauptung, Markenprodukte seien filialübergreifend gleich teuer.
- „Günstigste bekannte passende Alternative“ ist zulässig, **„günstigstes Produkt am Markt“** ohne beweisbar umfassende Quelle nicht.

## 7. Zeitliche Korrektheit
Ein Preis besitzt Abruf-/Beobachtungszeit, ggf. `valid_from`/`valid_until`, Quelle und (bestenfalls) Markt. „Am Einkaufstag günstiger“ darf nur anhand zum **damaligen Zeitpunkt gültiger, passend belegter Preise** festgestellt werden. Ein aktueller Preis darf nicht rückwirkend zur historischen Einkaufsauswertung verwendet werden. Bei geplanten zukünftigen Einkäufen nur tatsächlich veröffentlichte Zukunftsaktionen verwenden. Preisgedächtnis wird lokal aus bestätigten Beobachtungen aufgebaut; ein alter Preis ist kein heutiger Kassenpreis.

## 8. Fachliche Kernregeln
- Produktfamilie/food type, konkrete SKU/GTIN, Händlerartikelnummer, Bontext und Rezeptzutat sind unterschiedliche Identitäten; eine EAN ist nicht automatisch die Händlerartikelnummer.
- Bio `true/false/null` ist bekannt bio / bekannt nicht bio / unbekannt; Marke/Eigenmarke getrennt. Funktionale Vergleichbarkeit durch Attribute/Kategorien, nicht bloße Textähnlichkeit.
- Fehlende Mengen, Nährwerte, Preisbestandteile, Herkunft oder Zeitangaben bleiben unbekannt; niemals still als `0` oder „nicht bio“ deklarieren.
- Geld in ganzzahligen EUR-Cents, keine Float-Rundungsfehler. Mengen in eindeutig belegter Basis; Rohgewicht, Gesamtfüllmenge, Abtropfgewicht, Stück und Portion nicht still gleichsetzen.
- Quellen-/Qualitätsstatus erhalten. Nutzerbestätigungen sind datierte Entscheidungen; Modelle dürfen sie nicht selbst erfinden.
- Lebensmittel- und Allergensicherheit hat Vorrang. Kein MHD als automatisches Verderbdatum. Keine nicht bestätigte Lagerkapazität oder Budgethöhe behaupten.
- Abgleich von Bedarf aus Kochen und Verzehr ohne Doppelzählung: Kochen braucht Rohzutaten; späterer Verzehr der daraus erzeugten Portionen erzeugt nicht nochmals dieselben Rohwaren.
- Die App ist lokal/ohne kostenpflichtige Cloud-/API-Pflicht nutzbar; Online-Daten/AI-Fähigkeiten sind optional, Fehlermeldungen müssen offline sinnvoll bleiben.

## 9. Austausch und Versionierung
Die verbindlichen öffentlichen Nachrichten-Objekte und Beispiel-Payloads liegen unter `contracts/v1/`. Sie sind **Transport- und Fachverträge**, keine Speicheranweisung, keine Gewähr für Produktionsreife. JSON-Schema `1.0.0-draft` kennzeichnet die laufende Abstimmung. Fachmodul-Code darf Kotlin, Python oder eine plattformneutrale Bibliothek sein, **muss aber dokumentieren**, wie auf Android ohne dauerhaften Server und ohne Bezahlpflicht integriert werden kann. Ein Modul darf keine nicht vereinbarte umfangreiche Runtime als Pflicht voraussetzen.

## 10. Fertigstellung
Jeder Modul-Chat muss über die Fertigstellungskriterien in seinem `AGENTS.md` und `docs/DEVELOPMENT_MANDATE.md` berichten. Ohne automatisierte Offline-Tests, reproduzierbare positive und negative Testfälle, demonstrierte Ein-/Ausgaben, Rechts-/Quellenstatus, Abdeckungsgrenzen und Integrationsleitfaden **kein „fertig“**. Externe Live-Abfragen sind nur dort erforderlich, wo die reale Quellenfunktion Gegenstand des Nachweises ist und zulässig getestet werden kann. Grün bestandene Unit-Tests beweisen keine Live-API.

## 11. Gültigkeitsbereich
Diese Dokumente werden erst nach Prüfung durch alle Modul-Teams und Codex als stabile Version 1.0.0 freigegeben. Bis dahin gilt `1.0.0-draft` als **gemeinsame Arbeitsannahme**, nicht als unveränderlicher Produktionsvertrag. Jeder fachliche Änderungsvorschlag erhält Ursache, Auswirkungen, Migrations-/Kompatibilitätsbedarf und Tests. Keine stille Vertragsänderung durch ein Fachmodul.

# Preisquellen: Forschungsnutzung, App-Anzeige und private Historie
**Integrationsregel, 31.10.2026.** Diese Seite ist eine technische Sicherheits-Gate-Definition, **keine Rechtsberatung oder Nutzungslizenz**.

## Drei strikt getrennte Verwendungen
1. `RESEARCH_ONLY`: Einzeltests/Quellenbewertung mit belegter technischer und rechtlicher Zulässigkeit, keine Verwertung als öffentlich sichtbare Produkt-/Regalpreise. Datensätze als `SOURCED`, Quellenrechte ggf. `UNVERIFIED`. Keine dauerhafte App-Nutzung aus dem bloßen Abrufrecht ableiten.
2. `APP_DISPLAY`: fremde Preis- oder Produktdaten werden Endnutzern in der App als aktuelle/kommende Alternative angezeigt. Vorher für **jede Herkunft und vorgesehene Verwendungsart** dokumentierte Nutzungs-/Speicher-/Anzeigeerlaubnis erforderlich. `source.rightsStatus=PERMITTED` allein reicht nicht, wenn Beleg/Geltungsumfang fehlt; `UNVERIFIED` oder `RESTRICTED` sind ein No-Go für den betreffenden Datensatz.
3. `PRIVATE_USER_HISTORY`: ausdrücklich vom Nutzer bestätigte eigene Einkäufe/Kassenbons werden im privaten, lokalen Preisgedächtnis verarbeitet und dem betreffenden Nutzer als historische Zahlungen angezeigt. Das ist **keine Erlaubnis**, Händler-Websites oder dritte Bons öffentlich zu verteilen. Persönliche Bonbilder dürfen nie in öffentliche Repositories/Actions/Testfixtures exportiert werden.

## Pflichten für Adapter
- **Eingang:** `observation.source.origin`, `rightsStatus`, `evidenceKind`, `observedAt`, Händler-/Markt-/Regionskontext, ggf. bestätigte Genehmigungsreferenz.
- **Preisvergleich:** interne, eindeutig als Forschungs-/Synthetikdaten erkennbare Vergleiche dürfen mit nicht freigegebenen Beobachtungen getestet werden. Für `APP_DISPLAY` darf die Engine keine unverifiziert-rechtebehaftete **externen** Preisbeobachtung als sichtbare Alternative oder Ersparnis nach außen geben. Ein upstream-Filter allein genügt nicht; auch App-Adapter prüfen.
- **Quelle:** User-confirmed Receipt = `PRIVATE_USER_HISTORY`, `HISTORICAL_PAID` und Zeit-/Identitätsbeleg, **kein aktueller Preis**. Eigene Daten können privat gezeigt werden, aber fremde Preisalternativen benötigen weiterhin eigene Berechtigung.
- **Vollständigkeit:** Durch fehlende Rechte herausgefilterte Angebote gelten als fehlende Vergleichsabdeckung. Das Ergebnis muss passende `gaps` und ggf. **grauen Hinweis** `Könnte es günstiger geben` zeigen, statt „bester Marktpreis“.
- **Zulässigkeit:** Offizielle Website/API, technisch lesbarer Preis oder statisch gefundener Endpunkt allein = **keine** bestätigte Wiederverwendungs-/Speicher-/Anzeigefreigabe. Consent des eigenen App-Nutzers ersetzt nicht automatisch Rechte Dritter.
- **Zeit:** historische Preise nur für den belegten Einkaufstag; Angebote nur im realen Gültigkeitszeitraum, Filial-/Online-/Couponbedingungen getrennt.
- **Rechte-Registry:** Preisdatenmodul liefert explizit `PERMITTED`/`UNVERIFIED`/`RESTRICTED`, Quellen-/Versionstest- und Lizenzhinweis. Bei ungeklärten Rechten im produktiven Handler fail-closed, kein heimlicher Experimental-Modus.

## Drei verbindliche Ende-zu-Ende-Tests vor App-Freigabe
1. Fremde `UNVERIFIED` und `RESTRICTED` Quelle in einer `APP_DISPLAY`-Preisvergleichsanfrage → kein nach außen sichtbarer Preis/Alternativlink/Ersparnis; `incomplete=true` und zutreffende Coverage-Warnung. `RESEARCH_ONLY` kann separat synthetisch/rechtmäßig laufen.
2. Eigener bestätigter Bon → privater historischer Preis mit Händler und Datum; **keine** ungefragte Netzupload- oder Bestandsbuchung; keine irreführende Aussage über heutigen Preis.
3. Gleicher Bon, nicht bestätigter OCR-Entwurf → **keine** Preisbeobachtung, Zahlung oder Bestandsbewegung; erneute Verarbeitung derselben bestätigten Position idempotent.

## Umsetzung
Die Android-Haupt-App/Codex verantwortet die Darstellung und private Historie. Das Preisdatenmodul ist bereits konservativ bei `APP_DISPLAY`. Einkaufsintelligenz muss eine explizite `usageContext`- bzw. vertrauenswürdige, vom Host geprüfte Quellenfreigabe-Grenze und passende Negativtests liefern. Ein Modul-Chat schreibt hierfür ausschließlich in sein eigenes Repository; Änderungen am Architektur-Repo nur durch die Architektursteuerung.

## Konkretisierte Händlerauswahl (ADR-016)
Fachliche Auswahl: ALDI Nord, ALDI Süd, REWE und Lidl – gezielte Preisabfragen und veröffentlichte Angebote. Penny, Kaufland und EDEKA – ausschließlich veröffentlichte Angebote. Netto Marken-Discount – keine neue Entscheidung. Maßgeblich ist `docs/RETAILER_SOURCE_POLICY.md` samt JSON-Matrix. Die fachliche Auswahl ist keine Aussage über individuelle Nutzungsrechte. Der quellen- und verwendungsbezogene Rechtsstatus bleibt getrennt zu prüfen. Einzelne öffentlich sichtbare Preisfakten erfordern nicht allein aufgrund ihrer Herkunft zwingend einen Lizenzvertrag; ob ein konkretes Verfahren zulässig ist, hängt u. a. vom Abrufumfang, Datenbankrechten, Nutzungsbedingungen und der Wiederverwendung ab. Ungeklärte Produktivquellen werden nicht automatisch als freigegeben gekennzeichnet.

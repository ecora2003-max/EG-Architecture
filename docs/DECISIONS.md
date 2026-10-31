# Architekturentscheidungen (ADR-Register)
**Verwalter: Architektursteuerung / Chat 1.** Änderungen nur nach dokumentiertem Architekturentscheid.

| ID | Status | Entscheidung | Begründung / Folge |
| --- | --- | --- | --- |
| ADR-001 | ANGENOMMEN 31.10.2026 | Fachmodule als unabhängige Zulieferer; Codex integriert in Haupt-App | Teams liefern getestete austauschbare Kernfunktionen, keine DB-/UI-Konkurrenz |
| ADR-002 | ANGENOMMEN | Gemeinsames kanonisches **fachliches** Datenmodell; interne Modulmodelle frei | Adapterfähigkeit bei Android-/Room-Änderungen |
| ADR-003 | ANGENOMMEN | Architektur-Repo für Fachmodule nur **lesbar**; Haupt-App nur **lesbar** | Einziger Schreibbesitzer pro Repository; Schutzgrenze ist zunächst organisatorisch |
| ADR-004 | ANGENOMMEN | Unbekannt ≠ nullwertig; Preise/Cents, genaue Mengenbasis, Zeitbezug und Quellenpflicht | Keine Scheingenauigkeit |
| ADR-005 | ANGENOMMEN | Keine Buchung durch Vorschlag/Scan/Angebot/Rezepte/Listenhäkchen | Ist-Vorgänge nur nach Nutzerbestätigung und über App-Schreibgrenze |
| ADR-006 | ANGENOMMEN | Aktionsdaten aller acht Händler + verfügbare reguläre Preise + datierte Bonhistorie; Abdeckung sichtbar | Vergleich auch bei unvollständigen Katalogen sinnvoll |
| ADR-007 | ANGENOMMEN | Rot: vergleichbar gleicher Bio-Status günstiger; Orange: anderer Bio-Status günstiger; Grau: eventuell günstiger wegen Datenlücken | Evidenzgetriebene, mehrwertige Signale |
| ADR-008 | ANGENOMMEN | Barcode/Bon-OCR der Haupt-App wiederverwenden; Produktdaten-Modul ergänzt Identität/Aliase/Preisgedächtnis | Keine zweite OCR-/Kassenbuchungslogik |
| ADR-009 | ANGENOMMEN | Tests nach jeder Funktionsänderung; nur reproduzierbar nachgewiesener Code „bereit zur Integration“ | Fachmodule keine bloßen Projektberichte |
| ADR-010 | ANGENOMMEN | Keine kostenpflichtigen Pflichtdienste/Server oder Übernahme privater Daten in öffentliche Repos | Kosten- und Datenschutzrahmen |
| ADR-011 | VORLÄUFIG | Austauschvertrag 1.0.0-draft mit JSON-Schema, Beispielen und optionalen Extensions | Schema vor stabilem Release durch alle Teams und Codex prüfen |
| ADR-012 | OFFEN | Ziel-Runtime von AI-Rezepten und Lizenz/Persistenz externer Supermarktdaten | Technische Machbarkeit und Rechtslage müssen belegt werden |


| ADR-013 | ENTWURF 31.10.2026 | Shopping-Nachrichten `shopping.need.projection`, `shopping.purchase.suggestion`, `shopping.offer.interest` und `shopping.past.comparison` in separatem `contracts/v1.1` | Ergänzung auf Antrag von Einkaufsintelligenz; `v1.0` bleibt unverändert, Stabilisierung nach Abnehmer- und CI-Tests |
| ADR-014 | ANGENOMMEN 31.10.2026 | Nutzeranzeige fremder Preisbeobachtungen nur mit nachgewiesenen, zweckbezogenen Rechten; private bestätigte Bonpreise getrennt | `UNVERIFIED`/`RESTRICTED` niemals still als `APP_DISPLAY`-geeignet umdeuten; zwei technische Gates; siehe [Preisquellenrichtlinie](PRICE_RIGHTS_AND_DISPLAY.md) |
| ADR-015 | ANGENOMMEN 31.10.2026 | Fachmodule werden nicht von Architektur-Chats in fremden Repos geändert; Integration ausschließlich über Codex | Integrationsplan [Codex](CODEX_INTEGRATION_PLAN.md), Abnahme erst mit End-to-End-JVM/Migrations-/Gerätenachweisen |


| ADR-016 | ANGENOMMEN 31.10.2026 | **Händlerspezifischer Funktionsumfang:** gezielte Produktpreisabfrage + Angebotserfassung nur für ALDI Nord/Süd, REWE, Lidl; Angebotserfassung ohne gezielte Produktpreisabfrage für Penny, Kaufland, EDEKA; Netto Marken-Discount ohne neue Entscheidung | Nutzerentscheidung, konkretisiert ADR-006 hinsichtlich **Datenabruf-Funktionen**; siehe [Händlermatrix](RETAILER_SOURCE_POLICY.md) und [Policy JSON](../policies/retailer-source-capabilities.v1.json). Keine rechtliche Lizenz durch Funktionsfreigabe; rechtskonforme Quellenprüfung/APP_DISPLAY-Gate bleiben unabhängig. |

## Änderungsverfahren
Im **eigenen Modul-Repo** einen fachlichen Änderungsantrag mit Problem, Beispiel, betroffenen Verträgen, Kompatibilitätsbedarf und Tests dokumentieren. Architektursteuerung entscheidet in diesem Register und versioniert das Vertragsschema. **Kein Fachmodul schreibt direkt hier.**

## Verwechslungen ausdrücklich vermeiden
- „Gibt einen API-Endpunkt“ ≠ „darf dauerhaft systematisch genutzt werden“.
- „Preisfeld in Antwort“ ≠ „alle regulären Filialpreise vollständig“.
- „Markenprodukt“ ≠ „filialübergreifend immer gleicher Preis“.
- „Bio nicht erwähnt“ ≠ „nachgewiesen konventionell“.
- „Kauf bestätigt“ ≠ „gekaufte Lebensmittel sicher gelagert oder gegessen“.
- „Alle Tests grün“ ≠ „Quellenrechte, Hardware und Haupt-App-Integration geprüft“.

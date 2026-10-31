# Erweiterung für Einkaufsprozesse: 1.1.0-draft
**Stand:** 31.10.2026. **Status:** Architekturentwurf, **nicht produktiv freigegeben**, alte Version `1.0.0-draft` bleibt unverändert.

Anlass: <https://github.com/ecora2003-max/EG-Einkaufsintelligenz/blob/main/docs/CONTRACT_CHANGE_REQUEST.md>.

## Entscheidung
Vier neue Nachrichtentypen sind **additiv** in einer eigenen Vertragsfassung modelliert:
- `shopping.need.projection`: datierte, kumulative Einkaufsbedarfe; keine Buchung.
- `shopping.purchase.suggestion`: Produkt-/Gebinde-/Budget-/Pfand-Vorschlag; Status `FEASIBLE_NOT_PURCHASED` bedeutet **nicht** bezahlt.
- `shopping.offer.interest`: reine Interessen- und Listen-Statusvorschläge.
- `shopping.past.comparison`: historischer Einkauf, ausschließlich damals zugängliche Preisbelege; belegte Ersparnis nullable.

Die fünf bisherigen Nachrichtentypen sind strukturell unverändert, aber für diese Fassung mit `contractVersion: "1.1.0-draft"` zu versehen. **Nicht** in einer bestehenden 1.0-Nachricht still neue Typen verwenden. Bestehende Module können weiterhin v1.0 implementieren und müssen v1.1 erst nach ausdrücklicher Freigabe unterstützen.

## Kanonische Form
Jede Nachricht: `contractVersion`, `messageType`, `meta` und `payload`. `meta.usageContext` ist optional: `RESEARCH_ONLY`, `APP_DISPLAY`, `PRIVATE_USER_HISTORY`; es **beweist keinerlei Nutzungsrechte**. Der Host muss den Kontext durchsetzen, insbesondere externe Daten vor der Darstellung prüfen.

Neu:
- Identitäten: `needId`, `productId`, `observationRefs[]`, `confirmedPurchaseRef`, stabile Snapshot-Referenzen.
- Mengen: `Quantity` mit integer `amount` und dokumentierter `unit`/`basis`/`confirmed`.
- Geld: `expectedCents` **Warenpreis** und `checkoutCents` **bekannter Kassen-Cashbetrag inklusive belegtem Pfand**. Unbekannte Posten `null`, niemals 0.
- Zeit: `snapshotAt`, `asOf`, `effectiveAt`, `purchaseAt`, `evidenceCutoff` ISO-8601 mit UTC-Offset; `dueDate` und Periodengrenzen ISO-Datum.
- Vollständigkeit: `COMPLETE`/`PARTIAL`/`UNKNOWN`; Umfang und Abdeckung müssen belegt sein.
- Kein Vertragstyp stellt einen Kauf-, Lager-, Rechnungs-, Koch- oder Verzehrbefehl dar.

## Semantische Gates (durch Adapter prüfen; JSON Schema allein reicht nicht)
1. `shopping.need.projection.asOf >= snapshotAt`; Horizonte aus demselben Snapshot kumulativ und nicht summierbar.
2. `shopping.past.comparison.evidenceCutoff <= purchaseAt`; jede verwendete externe Preisbeobachtung wurde vor Kaufzeitpunkt veröffentlicht/beobachtet und war am Kaufdatum gültig.
3. `status=PROVEN` nur mit ausreichenden historischen konkreten Preis- und Mengennachweisen; sonst `savingsProvenCents=null`.
4. `FEASIBLE_NOT_PURCHASED` nur bei hinreichenden Mengen-, Markt-, Zeit-, Preis-, Depot-/Pfand-, Budget- und Kapazitätsbelegen. Insbesondere kein Kaufstatus.
5. `source.rightsStatus` ist Quellrecht, `meta.usageContext` ist Verwendungszweck. **Nur APP_DISPLAY mit belegter Nutzungsfreigabe für die konkrete Quelle**; private eigene bestätigte Bonbeobachtungen können lokal im Modus `PRIVATE_USER_HISTORY` angezeigt werden. Ein ausdrücklich fehlender Händlerlizenznachweis darf nicht durch Neulabeln einer Quelle umgangen werden.
6. Produkt-/Bonidentität und Kettenscope müssen mit den aktuellen konkreten Versionen kompatibel sein; Händler-SKU niemals als GTIN schätzen.
7. Bei einem source-/budget-/quantity-bezogenen unbekannten oder widersprüchlichen Feld konservativ `REVIEW`/unknown, niemals Zahl behaupten.
8. Zwei echte Käufe sind nicht automatisch ein Duplikat, dieselbe bestätigte Belegposition darf durch Retry nicht doppelt in Preisgedächtnis/Buchung gelangen.

## Dateien und Prüflauf
- `contract.schema.json`: JSON Schema Draft 2020-12.
- `examples.json`: 9 vollständig synthetische Nachrichten.
- `tools/validate_contract.py`: prüft v1.0 und v1.1, Positiv-/Negativfälle und zeitliche Semantik.
- `.github/workflows/contract-validation.yml`: prüft diese bei den relevanten Änderungen mit Python und fixierter jsonschema-Version.

## Freigabebedingung
`1.1.0-draft` wird **nicht automatisch stabil**. Vor Freigabe müssen der Einkaufs-Chat, Produktdaten-/Preisdatenchat und Codex gegen echte Modul-/App-DTOs prüfen, dass IDs/Mengen/Gültigkeit/Snapshots verlustfrei abgebildet werden. Ungeklärte Felder als Änderungsantrag, keine stillen Implementierungsänderungen. Nach CI-grüner Schema- und Modulprüfung neues ADR-/Versionsprotokoll erstellen und erst dann `1.1.0` freigeben.

## ADR-017: nachgeschärfte v1.1-Draft-Semantik (31.10.2026)
- `shopping.need.projection.payload.unknownNeeds[]` ist nun explizit typisiert: `needId`, `foodTypeId`, `dueDate|null`, `quantityToBuy=null`, `reason`. Das generische `Quantity.unit` bleibt **unverändert**; unbekannte Einheiten werden nicht als `g` o. Ä. erfunden. Ein offener Bedarf erzwingt `PARTIAL` oder `UNKNOWN`, eindeutige IDs sind auch mit `needs[]` zu gewährleisten.
- `shopping.purchase.suggestion.payload.packageLines[]` ist für gemischte Gebinde strukturiert. Je Packung werden Produkt-ID, Preisbeleg, Anzahl, Menge, Warenpreis, Pfand, Gesamtpreis und Händler-/Filialzuordnung getrennt übertragen. Gesamtwerte sind nur bei vollständig belegter Zusammensetzung beweisbar. Ein Mix darf keinen vermeintlichen Einzelartikel vorspiegeln.
- `shopping.past.comparison.payload.savingsBasis` ist ab **dieser Draft-Revision Pflicht** und ausschließlich `MERCHANDISE_ONLY`. `savingsProvenCents` ist keine hypothetische Checkout-/Pfand- oder bloße Grundpreisersparnis.
- **Kompatibilität:** `contracts/v1` und dessen Nachrichten bleiben unverändert. Der frühere `v1.1`-Entwurf wird durch die neue Pflichtangabe `savingsBasis` nicht vollständig rückwärtskompatibel fortgeschrieben. Es bleibt ausdrücklich `1.1.0-draft`, **nicht** freigegeben; zur Migration den aktuellen Schema-Blob lesen, nicht eine alte Kopie verwenden.
- Formaler Beschluss und Nachweise: [ADR-017](../../docs/ADR_017_SHOPPING_RESOLUTION.md), [Vertragstestbericht](../../docs/CONTRACT_TEST_REPORT.md); GitHub Actions [41226969317](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41226969317) 11 positive + 30 negative v1.1-Fälle.

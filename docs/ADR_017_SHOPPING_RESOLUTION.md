# ADR-017 – Shopping-DTOs: unbekannte Bedarfe, Mischgebinde und historische Ersparnisse

**Entscheidung:** 31.10.2026 · **Status:** im `1.1.0-draft` umgesetzt und per Architektur-CI geprüft; **keine stabile Vertrags- oder Integrationsfreigabe**.  
**Anlass:** `EG-Einkaufsintelligenz/docs/CONTRACT_CHANGE_REQUEST.md` und `docs/V11_DRAFT_COMPATIBILITY.md`.  
**Geltung:** ausschließlich `contracts/v1.1/`; `contracts/v1/` bleibt unverändert.

## 1. Noch unbekannter Einkaufsbedarf
Das mengen-/einheitenbezogene `Quantity`-Schema wird **nicht** global aufgeweicht: `unit` bleibt `g|ml|portion|piece`. Für Fälle ohne bekannte Einheit existiert jetzt ein **typisiertes** `shopping.need.projection.payload.unknownNeeds[]` mit:
- `needId` und `foodTypeId` als nichtleere Zeichenfolgen,
- `dueDate` als ISO-Datum oder `null`,
- `quantityToBuy=null` (kein numerischer Nullbedarf),
- `reason` als nichtleere Zeichenfolge.

Derselbe `needId` darf nicht gleichzeitig in `needs[]` und `unknownNeeds[]` oder innerhalb einer Liste mehrfach auftreten. Sobald `unknownNeeds[]` Einträge enthält, ist die gesamte `completeness` **nicht** `COMPLETE`. Der Host darf den unbekannten Bedarf nicht still ausblenden; Warnung und offener Klärungsbedarf müssen sichtbar bleiben. Die derzeitige Experimentalschnittstelle der Einkaufsintelligenz übermittelt diese Daten bereits als Extension, aber **die neue strenge Schemafassung ist dort noch nicht nachgetestet**.

## 2. Gemischte Packungen
Optionales, nun typisiertes `shopping.purchase.suggestion.payload.packageLines[]` mit pro Zeile: `productId`, `observationId|null`, `packageCount`, `quantity`, `merchandiseCents|null`, `depositCents|null`, `checkoutCents|null`, `retailerId|null`, `storeId|null`.

Regeln:
- Bei mehreren Zeilen darf die aggregierte Einzelangabe `productId`/`packageCount` keinen einzelnen Artikel vortäuschen (beide `null`).
- Eine konkrete `observationId` muss in `observationRefs[]` referenziert sein; eine unbekannte `observationId` bleibt `null` und kann keine nachgewiesenen aggregierten `expectedCents`/`checkoutCents` rechtfertigen.
- Der Warenwert ist die Summe **sämtlicher belegter** `merchandiseCents`; der Cash-Betrag entspricht der Summe aller `checkoutCents`. Pro Zeile müssen `checkoutCents = merchandiseCents + depositCents` gelten, wenn bekannt. Unbekanntes Pfand/fehlende Belege untersagen eine bestätigte Cash-Summe; `null` bedeutet nicht 0.
- `storeId` darf nicht ohne `retailerId` auftreten. `FEASIBLE_NOT_PURCHASED` ist ohne jede erforderliche Preisbeobachtung unzulässig und **niemals** gleichbedeutend mit gekauft.
- Bei `packageLines[]` wird nur innerhalb des explizit belegten Geltungsbereichs verglichen; Coupons, Lagerkapazität und zeitliche Gültigkeit sind **zusätzliche** Host-/Adapter-Gates.

Bis zur Übernahme durch den Einkaufs-Adapter ist dessen untypisierte `mix[]`-Extension **keine freigegebene Ersatzschnittstelle**.

## 3. Historisch belegte Ersparnis
`shopping.past.comparison.payload.savingsBasis` ist in `1.1.0-draft` **verpflichtend** und ausschließlich `MERCHANDISE_ONLY`. `savingsProvenCents` bezeichnet nachgewiesene Reduktion des Gesamtwarenpreises für einen tatsächlich vergleichbaren damaligen Kaufumfang; **keine** Kassen-/Pfand-/Versand- oder reine Grundpreisersparnis. `status=PROVEN` erfordert passende konkrete historische Preisreferenzen und positive belegte Warenpreisersparnis. Andernfalls bleibt `savingsProvenCents=null` bzw. ein nicht-`PROVEN`-Status. Beobachtungs-/Gültigkeitszeit, Filialvergleich und frühere Kaufmengen sind zusätzlich fachlich zu verifizieren.

Die Pflichtangabe `savingsBasis` ist gegenüber dem **vorherigen v1.1-Draft** eine inkompatible Nachschärfung, **nicht** gegenüber `v1`. Kein stilles Upgrade: Moduladapter und Codex müssen die neue Schema-Blob-Version explizit prüfen.

## 4. Test- und Integrationsgate
GitHub Actions `contract-validation` [Run 41226969317](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41226969317), Commit `c1b08f0e062fb9d2cdacf4853296c5529f85f17b`:
- `v1`: 5 positive / 7 negative, unverändert.
- `v1.1`: 11 positive / 30 negative inkl. zwei zusätzlichen gültigen Misch-/Unbekanntfällen und neuer semantischer Gates.
- Insgesamt **16 positive / 37 negative** Schema-/Semantiktests bestanden; Händlerfunktionsmatrix zusätzlich **27/27** Policy-Prüfungen. Alle genannten Zahlen aus tatsächlich ausgelesenem CI-Joblog.

**Offen:** experimenteller Einkaufsadapter gegen *neue* Blob-SHA testen/portieren; vollständige Versions-/Negativtests der betroffenen anderen Modul-Adapter; Kotlin-DTOs, Host-Rechtefilter, alte Bestands-/Kaufsemantik, App-JVM-/Room-/Gerätetests durch Codex; Quellenrechte. Bei Konflikt neue Änderungsanträge, keine Implementierung in fremden Repositories durch Chat 1. Bis dahin `DRAFT_CI_VERIFIED`, nicht `STABLE` oder `INTEGRATED`.

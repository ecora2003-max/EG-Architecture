# Abnehmer-Kompatibilitätsprüfung – Vertrag 1.1.0-draft
**Momentaufnahme:** 31.10.2026, 18:03 UTC. **Erstellt durch Chat 1, Architektursteuerung.**

## Neuere Abnehmerbeobachtung – 31.10.2026, ab 18:04 UTC
**Die Einkaufsintelligenz hat die veraltete v1.1-Testkopie inzwischen ersetzt:** Die aktuelle `contracts/v1.1/contract.schema.json` hat jetzt ebenfalls Blob-SHA `dca777d219307a90bf3d4dff6189fbf12476c508`. Damit ist der reine **Schema-Datei-Gleichstand** hergestellt. Der Draft-Adapter wurde ebenfalls von der vorherigen `mix[]`-Extension auf typisierte `packageLines[]` umgestellt.

**Die Abnehmer-Implementierungsfreigabe ist weiterhin offen:** Der grüne [Run 41227548850](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227548850) mit 107/107 Tests gehört zu einem Commit mit neuer Schema-Kopie, aber **ohne die spätere vollständig typisierte `packageLines[]`-Implementierung**. Folgende Erweiterungs-Commits hatten zunächst rote CI. Beispielsweise beanstandete [Run 41227606242](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227606242) die Annahme, `examples.json` müsse 11 Kanonbeispiele enthalten. Korrekt sind **9 kanonische Envelopes + 2 programmgenerierte Positivfälle im Architekturvalidator = 11 positive v1.1-Tests**. Vor einer v1.1-Abnahme **neuesten Modul-Head und erfolgreiche zugehörige vollständige CI erneut prüfen**; einen früheren grünen Test nicht als Nachweis für neueren Code verwenden.

Die nachfolgende Tabelle bewahrt den **datierten ursprünglichen** SHA-Audit-Befund, einschließlich der damals tatsächlich noch veralteten Schema-Kopie. Bei der Integrationsentscheidung gilt diese neuere Beobachtung vorrangig.

## Maßstab
- Ursprüngliches `contracts/v1/contract.schema.json`: Blob-SHA `bedde4677342817fe6b883962c8dfbbd60100072` (`1.0.0-draft`).
- Aktuelles, nach ADR-017 nachgeschärftes `contracts/v1.1/contract.schema.json`: Blob-SHA `dca777d219307a90bf3d4dff6189fbf12476c508` (`1.1.0-draft`, **nicht stabil freigegeben**).
- Schema-Parität, erfolgreich ausgeführter Unit-Test und tatsächlich getesteter Haupt-App-Adapter sind **drei getrennte Nachweisstufen**. `github actions success` beweist zunächst nur das konkrete Workflow-Programm und seinen Commit, **keine** Vertragskompatibilität, wenn eine veraltete Schema-Kopie geprüft wird.
- Nur aus echten GitHub-Repository-Dateien und GitHub-Actions-Logs abgeleitet. Keine Fremd-Repositories geändert.

## Reproduzierbarer Befund je Modul

| Fachmodul / Stand | Nachgewiesene Tests | Vertragsevidenz und Gate |
| --- | --- | --- |
| **EG-Preisdaten**, `main@affc8cdf58f2d5d3c793857bd5ab43b4a8639046` | [Run 41224039268](https://github.com/ecora2003-max/EG-Preisdaten/actions/runs/41224039268), **89/89** Python-Unit-Tests, keine Fehler | Liefert alte v1-Fachmessages. Kein lokaler Standardpfad `contracts/v1/contract.schema.json` gefunden; maßgebliche API/Fixture-Version im Code-/Testlauf pinnen und gesondert gegen v1.1 bei Bedarf validieren. Live-Rechte/Filialabdeckung weiterhin offen. |
| **EG-Produktdaten**, `main@5f37e9ba4a468dbfbe7336f91f680ebda636ec47` | [Run 41220106489](https://github.com/ecora2003-max/EG-Produktdaten/actions/runs/41220106489), **105/105** Python-Tests laut dokumentiertem Fachcode-Stand | Vendorte `contracts/v1/contract.schema.json` ist Blob-`bedde467...` (kanonische v1-Parität). v1.1-Einkaufs-DTOs und Android-Adapter nicht nachgewiesen; Produktdatenmodul ist für seine **v1-Offline-Abnahme** bereit, nicht für App-Integration. |
| **EG-Einkaufsintelligenz**, `main@ed6ef5013323fbe8ff5e015d584fee2ec1a01254` | [Run 41227197394](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227197394), **119/119** Python-Tests, keine Fehler (vollständiges Log geprüft) | Vendorte `contracts/v1/contract.schema.json` stimmt mit kanonischem v1 überein; **vendorte v1.1-Kopie ist `f4755a0a2dfbd8c4f58f2778fa21800b9e3ffbdc` und damit *NICHT* gleich aktuellem kanonischem `dca777...`**. `1.1.0-draft`-Kompatibilität daher **OFFEN**; kein CLI-/App-Upgrade. |
| **EG-Rezept-KI**, `main@029b0337a3064109f320230c1f4ea83d305395eb` | [Run 41226586359](https://github.com/ecora2003-max/EG-Rezept-KI/actions/runs/41226586359) completed/success. STATUS berichtet **145 JVM-Tests + 74 Schemafälle** | Vertrag `v1` wird in CI über ausdrücklich gepinnte Architektur-Revision bezogen; kein direkt vendortes `contracts/v1/contract.schema.json` am Standardpfad. v1.1-Shopping-DTO nicht Teil der Rezept-KI-Fachabnahme, Android-On-Device-/Privacy-Beweis offen. |
| **Android-Haupt-App** | Kein aktueller erfolgreicher Code-/Geräte-Integrationsnachweis in dieser Prüfung | Privates App-Repository kann durch Chat 1 nicht als vollständige aktuelle Integrationsquelle verifiziert werden. **Codex-only**; `INTEGRATED` bleibt gesperrt. |

`main@` bezeichnet den bei der Prüfung mit GitHub `git/ref/heads/main` gelesenen Stand; Module können sich danach bereits weiterentwickelt haben. Bei jeder neuen Entscheidung Head/CI erneut lesen.

## Zwingende Übergabe an das Einkaufsintelligenz-Modul
1. Im **eigenen** Repo den aktuellen kanonischen Schema-Blob `dca777...` übernehmen oder in CI ausdrücklich gegen den kanonischen Architektur-Commit validieren, ohne v1-CLI-Produktion umzuschalten. Für Testkopien Snapshot-SHA dokumentieren.
2. `unknownNeeds[]`: `quantityToBuy=null`; nicht implizit `0 g`; IDs auch quer zu `needs[]` eindeutig; `completeness` korrekt.
3. `packageLines[]`: pro ausgewähltem Gebinde belegte Einzelposition, `productId`, `observationId`, `packageCount`, `quantity`, Preise, Pfand und Händler-/Filiale; top-level Produkt-/Packungsangaben müssen ggf. mit einer Einzelzeile übereinstimmen. Nicht belegte Zeilen blockieren beweisbare Summen und Feasible-Status. Budgetzeitraum `from<=until`.
4. `shopping.past.comparison`: `savingsBasis=MERCHANDISE_ONLY` Pflicht; `PROVEN` nur positive dokumentierte Ersparnis auf damals belegtem **Warenpreis-Gesamtbetrag**, kein nachträglich bekannter Preis. Bericht darf nicht vor dem bestätigten Kauf erstellt sein.
5. Neue Positiv-/Negativtests und `test_draft_v11.py` gegen **exakt** den neuen Schema-Blob; `1.0.0-draft`-Abnahmesuite weiterhin vollständig grün. Zusätzlich Host-/APP_DISPLAY-Rechte-Filter und ausschließliche Vorschlagssemantik nachweisen.

## Übergabe an Preisdaten und Produktdaten
- **Preisdaten:** Jede `observationId` ist in Händler/Filiale/Zeit/Quelle eindeutig, Cents/Pfand einzeln, `null` sichtbar; veraltete oder nicht zum Kauf gültige Quellen nicht für historische Ersparnisse nutzen. Nur dokumentierte zulässige Quellen bei `APP_DISPLAY`; ALDI Nord/Süd/REWE/Lidl gezielter Preis+Angebote, andere vier nur Angebote.
- **Produktdaten:** Identitäts- und Aliasauflösung bleibt getrennt von Packungs-/Preis-Beobachtung; konkrete Produkt-/Gebinde-Version muss vor Kaufvorschlag bestätigt sein. Verknüpfung `needIds[]`, `observationRefs[]`, `packageLines[]` nur über belegte IDs. Bonentwurf darf keinen Kauf oder historischen Preis buchen.
- **Beide:** v1-Kern bleibt zunächst unverändert. Die v1.1-Erweiterung ist *keine* Aufforderung zu ungetestetem Runtime-Upgrade. Auffälligkeiten als Änderungsantrag an Chat 1.

## Codex: verbindliche End-to-End-Abnahme, derzeit offen
1. Produkt-/Packungs-/Beleg-ID → explizit bestätigter Kauf → genau eine Kauf-/Preisgedächtnis-Buchung trotz Retry; zweiter realer Kauf nicht dedupliziert.
2. Projektions-Snapshot → kumulative 1/7/56-Tages-Bedarfsansichten ohne Summierung von überlappenden Horizonten; `unknownNeeds[]` sichtbar, nicht als null Menge gekauft.
3. Gemischter Warenkorb → Kostenwahrheit bei fehlender Beleg-ID, unbekanntem Pfand, Coupon, Markt/Datum und fehlender Kapazität; `FEASIBLE_NOT_PURCHASED` kein realer Kauf.
4. Historischer Vergleich → nur am damaligen Kaufdatum verfügbare Preisbelege, positive beweisbare Warenpreisersparnis, `unitOnlyAlternatives` getrennt; kein Hindsight.
5. `APP_DISPLAY` → `UNVERIFIED`/`RESTRICTED` externer Ursprung niemals sichtbarer Preis/Links/Sparvorschlag, mit Coverage-Hinweis. Private bestätigte Bonhistorie nur lokal, mit Datum.
6. Vollständige Kotlin-/JVM-/Room-Migrationstests einschließlich Bestandsschutz und Idempotenz, Compose-UI, Offline-/Gerätetests. Bei fehlender Hardware ausdrücklich nur JVM-Abnahme.

## Architektureigene CI
[Run 41227460264](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227460264), Code-SHA `02eb9f034256a98339b9fdf37618bb53f818c362`, **completed/success**:
- v1: **5 positive + 7 negative**.
- v1.1: **11 positive + 34 negative**.
- Summe: **16 positive + 41 negative** Schema-/Semantikprüfungen; Händler-Policy **27/27**.
- Prüft neu Einzelzeilen-/Top-Level-Produkt- und Packungsparität sowie Fehlklassifizierung `FEASIBLE` bei unbekannter Menge/Preis/Kapazität; verkehrte Budgetdaten. Eine vorherige CI ([41227411420](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227411420)) war wegen **fehlerhaft konstruiertem Negativfixture** rot und wurde durch ein tatsächlich ungültiges Testfixture korrigiert. Kein produktiver Integrationsnachweis.

**Gesamtbewertung:** `DRAFT_CI_VERIFIED / CONSUMER_PARITY_PENDING / CODEX_INTEGRATION_PENDING`. Keine stabile v1.1-Freigabe, keine Android- oder Live-Quellenfreigabe.

## Aktualisierung – erste grüne Adapter-Abnahme nach Schema-Übernahme (18:07 UTC)

Nach der oben dokumentierten kurzzeitigen roten CI hat Einkaufsintelligenz einen tatsächlich **erfolgreichen** Lauf mit dem neuen Schema und den typisierten `packageLines[]` erreicht: [Run 41227774941](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227774941), Codecommit `ec910c1ad9ea479330f7a592567c03fbadc01ad6`, **124/124 Python-Tests**, keine Fehler; vollständiges Joblog gelesen. Für genau diesen Commit beträgt die vendorte Schema-Blob-SHA `dca777d219307a90bf3d4dff6189fbf12476c508`, die Adapter-Datei enthält `packageLines` und `unknownNeeds`. **Schema-Parität + Offline-Testlauf dieses Draft-Adapters nachgewiesen**, aber noch **nicht** Codex-/Host-/Rechte-/Android-Integration oder stabile Freigabe.

Architektur-CI hat ergänzend [Run 41227803811](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227803811) mit **16 positiven / 42 negativen** Schema-/Semantiktests (inkl. `APP_DISPLAY`-Rechtesperre) und **27 Händler-Policy-Checks** erfolgreich abgeschlossen. Für spätere Abnahme verbleibt die APP_DISPLAY-Registry-Rechtsbelegprüfung, die modulübergreifende Kotlin-Parität und der historische Kauf-/Preis-/Bestands-E2E-Pfad. Die ursprünglichen SHA-/CI-Befunde oben sind datierte historische Momentaufnahmen, **keine** noch aktuelle Aussage, dass die v1.1-Schema-Kopie weiterhin veraltet sei.

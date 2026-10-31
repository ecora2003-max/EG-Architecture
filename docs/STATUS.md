# Projektstatus – Architektursteuerung / Chat 1
**Stand:** 31.10.2026 · **Zuständiges Schreibrepository:** ausschließlich `ecora2003-max/EG-Architecture`.

## Aktueller Vertragsstand
- `contracts/v1`: `1.0.0-draft`, unverändert, 5 positive + 7 negative Schema-/Semantiktests.
- `contracts/v1.1`: `1.1.0-draft`, nicht stabil freigegeben. Vier additive Shopping-Nachrichten, zusätzlich ADR-017 für typisierte `unknownNeeds[]`, `packageLines[]` und `savingsBasis=MERCHANDISE_ONLY`.
- Aktuelle Schema-Blob-SHA von `contracts/v1.1/contract.schema.json`: `dca777d219307a90bf3d4dff6189fbf12476c508`. Ältere Modul-Testkopie `f4755a0a2dfbd8c4f58f2778fa21800b9e3ffbdc` **nicht mehr gleichwertig**.
- Geprüfter Code-/Schema-/Testcommit `c1b08f0e062fb9d2cdacf4853296c5529f85f17b`: [CI 41226969317](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41226969317), `completed/success` – **16 positive, 37 negative** Vertragstests und **27** Händler-Policy-Prüfungen bestanden. Vollständiges Joblog direkt eingesehen. Spätere Dokumentationscommits ändern die geprüfte Fachlogik nicht.

## Module – zuletzt aus eigenem STATUS gelesen (Momentaufnahme)
| Modul | Gesicherter gemeldeter Offline-Stand | Nicht als erledigt behandeln |
| --- | --- | --- |
| [EG-Preisdaten](https://github.com/ecora2003-max/EG-Preisdaten) | `PARTIAL_READY`; 77 bestandene CI-Tests (letzter in Status belegter Code-Testlauf) | Quellen-/Datenrechte, echte Händlerabdeckung und Feed-Lücken; Android-Kotlin-Port |
| [EG-Produktdaten](https://github.com/ecora2003-max/EG-Produktdaten) | `READY_FOR_INTEGRATION`, offline; 105 bestandene CI-Tests | Kotlin/Room/Bon-End-to-End-Integration durch Codex |
| [EG-Einkaufsintelligenz](https://github.com/ecora2003-max/EG-Einkaufsintelligenz) | v1.0 offline `READY_FOR_INTEGRATION`; neuer v1.1 Adapter `EXPERIMENTAL/SCHEMA_TESTED`, 107 bestandene CI-Tests beim letzten Code-Meilenstein | experimentelle vendorte v1.1 Schema-Kopie nach ADR-017 veraltet; neue Felder und Adaptertests; Android-Integration; APP_DISPLAY-Rechtefilter |
| [EG-Rezept-KI](https://github.com/ecora2003-max/EG-Rezept-KI) | `PARTIAL_READY/OFFLINE_VERIFIED`; 129 JVM- und 74 Schema-Fallprüfungen in dokumentierter CI | echtes Android-On-Device-Modell, Hardware- und App-Tests; Host-JSON-Parser/Privatsphäre |

Testzahlen der Module wurden **aus deren Statusdateien** übernommen, nicht in diesem Architekturschritt neu ausgeführt; nach weiteren Modulcommits neu lesen.

## Verbindliche Grenzen
- Nur [EG-Architecture](https://github.com/ecora2003-max/EG-Architecture) darf Chat 1 beschreiben. Vier Fachmodule schreiben je eigenes Repo; `Ernaerungsgedaechnis` darf nur Codex integrieren.
- Die produktive Google-Sheets-Ernährungs-/Vorratsquelle bleibt bis ausdrücklicher Migration maßgeblich und getrennt; keine echten privaten Belege/Snapshots in öffentliche Repos oder CI.
- ADR-016: ALDI Nord/Süd, REWE und Lidl – **gezielte Preisabfrage + Angebote**; Penny, Kaufland, EDEKA und Netto Marken-Discount – **nur Angebote**. Funktionswunsch ist keine rechtliche Abruf-/Anzeigefreigabe.
- Unklare fremde Datenrechte sperren `APP_DISPLAY`; bestätigte private Bonpreise sind historische, keine aktuellen Händlerpreise. Preisvorschläge/Rezepte/Listeninteressen erzeugen **keine** Käufe oder Vorratsbewegungen.
- Kein `STABLE` oder `INTEGRATED` allein aufgrund von Offline-Tests.

## Unmittelbare nächste Schritte Chat 1
1. [ADR-017](ADR_017_SHOPPING_RESOLUTION.md) als **Draft-Vertragsänderung** an Einkaufsintelligenz, Preisdaten, Produktdaten und Codex zur expliziten SHA-/Adapter-/Semantikprüfung übergeben. **Keine Änderungen in deren Repos durch Chat 1.**
2. Einkaufsintelligenz: `dca777…` statt `f4755…` validieren; typisierte `packageLines[]` übernehmen, `unknownNeeds[]` gemäß Schema überprüfen, historische `savingsBasis` testen; neue Negativfälle einschließlich Rechtefilter nachweisen.
3. Preisdaten/Produktdaten: Impact auf IDs, Einzelbeobachtungen, Menge, Sortiment, Quellenrecht und Bonhistorie dokumentieren; kein stilles v1.1-Upgrade. Rezept-KI: v1 unverändert, Änderungen nur bei nachweisbarer Abhängigkeit.
4. Codex: Android-E2E-Bon→Kauf→Preisgedächtnis→Vergleich→Bedarfsprojektions-Szenario und Kotlin-Adapter inklusive Room-Migration, APP_DISPLAY-Rechtegate, No-Side-Effects und Hardwaretests. Vertrag erst nach Abnehmernachweisen stabilisieren.
5. Vor nächstem Statusbericht neue Modul-/Architektur-Commits und CI-Logs abrufen; Abnahme nur aus reproduzierbaren Logs/Fixtures ableiten. Keine ungestützte Händler-, Quellenrecht- oder Gerätefreigabe.

## Chat-1-Fortsetzung – 31.10.2026, 18:03–18:06 UTC

**Strengere Architekturabnahme:** [Run 41227460264](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227460264) am Codecommit `02eb9f0` nach echter Negativfixture-Korrektur **success**: 5/7 (v1) + 11/34 (v1.1) = **16 Positivfälle, 41 Negativfälle**, zusätzlich **27 Händlerfunktions-Gates**, 0 fehlgeschlagen. Bereits bestehende v1-Fachvertragsversion und v1.1-Schema-SHA `dca777d219307a90bf3d4dff6189fbf12476c508` unverändert.

**Abnehmer-Klärung:** [Kompatibilitäts-Audit](CONSUMER_COMPATIBILITY_AUDIT.md) erstellt, anhand echter GitHub-Daten geprüft: Preisdaten neueste dokumentierte vollständige CI **89/89**, Produktdaten **105/105**, Rezept-KI neuester dokumentierter Lauf **145 JVM / 74 Schemafälle**, Einkaufsintelligenz v1 CI über 100 Offline-Tests. Diese Zahlen beziehen sich auf verschiedene Modul-Commits und ersetzen weder die Gesamtintegration noch Quellrechts-Gates.

**Laufende Änderung bei Einkaufsintelligenz:** Die neue v1.1-Testkopie wurde während dieser Prüfung von `f4755a...` auf den kanonischen Schema-Blob `dca777...` aktualisiert, und der opt-in Draft-Adapter führt jetzt `packageLines`. Der 107-Tests-Lauf [41227548850](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227548850) war grün **vor** der Adapter-Erweiterung; unmittelbar anschließende CI bei Adapter-Umstellung zunächst rot. Unter anderem wurde irrtümlich `examples.json` mit 11 statt den kanonischen 9 Beispielen erwartet (11 bezeichnet die **gesamten positiven v1.1-Vertragstests inklusive zwei generierter Fälle**). Dieser Punkt ist eine **Adaptertest-Frage im Modulrepo**, kein Anlass, willkürlich zwei Kanonbeispiele einzufügen. Neuere Modul-Commits/CI danach frisch prüfen und vor Freigabe einen tatsächlich grünen **aktuellen** Adapter-Stand verlangen. Keine Änderungen an diesem Modul durch Chat 1.

**Freigabegrad bleibt** `DRAFT_CI_VERIFIED / CONSUMER_PARITY_PENDING / CODEX_INTEGRATION_PENDING`. Nächster Architekturarbeitsschritt: externes neuestes CI prüfen, Abnehmer-Gates in [Audit](CONSUMER_COMPATIBILITY_AUDIT.md) aktualisieren, dann erst nach Codex- und Modul-Abnahme über stabile Version befinden.

## Update – tatsächlich neu verifizierte CI und Abnehmerparität, 31.10.2026, 18:07 UTC

- Architektur-Run [41227803811](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41227803811) auf `ece096e5` **PASS: 16 positive + 42 negative Schema-/Semantiktests, 27 Händler-Policy-Gates**. Neuer `APP_DISPLAY`-Negativfall für unbestätigte externe Preisrechte. Schema-Blob `dca777...` unverändert; keine Rechts-/Produktivfreigabe.
- Einkaufsintelligenz hat die vendorte `contracts/v1.1/contract.schema.json` nun nachweislich auf `dca777d219307a90bf3d4dff6189fbf12476c508` aktualisiert. Der überprüfte Test-Commit `ec910c1ad9ea479330f7a592567c03fbadc01ad6` enthält bereits die typisierten `packageLines` und `unknownNeeds`; [CI 41227774941](https://github.com/ecora2003-max/EG-Einkaufsintelligenz/actions/runs/41227774941) **PASS 124/124 Tests**, 0 Fehler. Frühere fehlgeschlagene PR-/Push-Testläufe wurden dadurch **für diesen geprüften Code-Commit** behoben. Ein späterer Modul-Head ist erneut zu verifizieren.
- Dadurch ist die **syntaktische Schema-Kopie-Parität und lokale Testfähigkeit des Shopping-Draft-Adapters** belegt, nicht jedoch vollständige End-to-End-Fachsemantik, APP_DISPLAY-Rechteprüfung bei realen Quellen, Codex-Adapter, Kotlin/Room/Compose/Migration/Android-Gerät. Status: `DRAFT_CI_VERIFIED / SHOPPING_DRAFT_ADAPTER_OFFLINE_VERIFIED / ANDROID_INTEGRATION_PENDING`. `1.1.0-draft` bleibt **nicht STABLE**.

## ADR-018 – Angebotspreise und Katalogquellen, 31.10.2026, 21:02 UTC
Nutzer bekräftigt funktionale Datenwünsche: **Angebotspreise aller 8 Händler** sowie zusätzlich **Angebotskatalog-Listen für ALDI Nord, ALDI Süd, Lidl, REWE**. Die vier anderen Händler (Penny, Kaufland, EDEKA, Netto Marken-Discount) erhalten veröffentlichte Einzel-Angebotspreise, aber keine Katalog-Erschließung im aktuellen Projektumfang und keine gezielte reguläre Produktpreissuche. ADR-016 um die Katalogdimension als [ADR-018](DECISIONS.md) präzisiert. Neue Maschinenmatrix `policies/retailer-source-capabilities.v1.json` Policy-Version **1.0.2** mit den drei getrennten Fähigkeiten `targetedProductPriceQuery`, `publishedOfferCollection`, `publishedOfferCatalogDiscovery`; **kein** Änderungen des fachlichen v1-/v1.1-Schemas.

**Ausgeführte Architektur-CI:** [Run 41241651613](https://github.com/ecora2003-max/EG-Architecture/actions/runs/41241651613), Commit `4943ea4f9b6496269bb77ac8a81d67b8d87f7528`, `success`, direktes Log geprüft: **16/16 positive, 42/42 negative Vertragsfälle; 35/35 Händler-Fähigkeits-/Sicherheitschecks**. Vorgängerrun `41241639706` ist wegen noch nicht gleichzeitig angepasstem Policy-Validator rot; der nachfolgende Run ist grün. Spätere Änderungen an ADR-/Policy-/Übergabedokumenten ändern den getesteten Policy-Code nicht.

**Rechtegrenze:** Der Nutzerbegriff „frei“ wird als öffentlich bekannt gemachte/zugängliche Angebote **nicht automatisch** mit einer bestätigten Wiederverwendungs-/Redistributionsberechtigung gleichgesetzt. Code und Host müssen tatsächliche Quellen-/Verwendungsrechte weiterhin separat prüfen. Im Zweifel nur nichtproduktive Quellenanalyse und sichere Offline-Funktionen aktiv; keine Blockade der gesamten Integrationsarbeit.

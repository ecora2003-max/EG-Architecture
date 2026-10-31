# Integration, Vertragsverwaltung und Qualitäts-Gates
**Version 1.0.0-draft – Arbeitsregel für alle Chats und Codex**

## A. Technische und organisatorische Rollen
Alle spezialisierten Chats dürfen die Architektur, andere Modul-Repositories und das private Hauptrepo **lesen**, soweit GitHub den Zugang anbietet. **Nur das eigene Modul-Repository darf verändert werden.** Das Architektur-Repository schreiben ausschließlich Chat 1 bzw. die ausdrücklich beauftragte Architektursteuerung; das private `Ernaerungsgedaechnis` schreiben ausschließlich Codex/der beauftragte Haupt-App-Integrator. Auch wenn ein GitHub-Token breitere Rechte gewährt, gilt diese Schranke. Niemals Fremdbranches, Fremd-Dateien, Issues/PRs oder Workflows ändern, sofern dies als Schreibaktion in fremdes Repository erfolgt. Änderungen als Vorschlag `docs/CONTRACT_CHANGE_REQUEST.md` **im eigenen Repo** hinterlegen.

## B. Fachvertrag vs. interne Implementierung
Das kanonische Modell bestimmt Semantik, nicht SQL-Tabellen, Klassennamen oder Programmiersprache. Ein Modul darf seine internen Klassen/DB/Mappings verändern, solange Input-/Output-Vertrag und Invarianten erhalten bleiben. Keine direkten Imports aus der Haupt-App; keine neue zweite Bestands-, Zahlungs- oder Ernährungswahrheit.

Die Sprache/Runtime ist frei, aber es ist ein **realistischer Android-Integrationsweg** zu dokumentieren: reiner Kotlin-Kern, portierbare Python-Referenz mit exakter Kotlin-Migrationsspezifikation, optionaler on-device AI-Adapter oder bewusst rein analytisches Modulergebnis. Keine verpflichtende Bezahl-API/Server/Apps-Script-Lösung. Bei Kotlin: Tests ohne Android-Hardware für Fachkern, UI und Betriebssystemintegration bleiben Aufgabe Codex.

## C. Versionierte Nachrichten
- Kontraktdateien unter `contracts/v1`; Entwürfe mit `contractVersion: "1.0.0-draft"`.
- **Patch**: redaktionell/nicht semantisch; **Minor**: kompatible neue optionale Felder/Typsets nur nach Tests; **Major**: anderes Verhalten, Pflichtfelder, geänderte Interpretation von Preisen/Mengen/Status.
- Keine stillen Versionssprünge oder neuen Pflichtfelder. Input-Parser dürfen unbekannte optionale **namespaced** Extensions ignorieren, dürfen aber widersprüchliche Pflichtwerte nicht still „korrigieren“.
- Für inkompatible Änderungen eine neue `v2`-Struktur, Kompatibilitätsmatrix und migrationsfeste Beispieltests.
- Jede Modul-Lieferung benennt exakt unterstützte Vertragsversion(en) und zuletzt gelesene Git-Commit-SHA.

## D. Prüfmatrix – für **jede** Entwicklung / Änderung
1. Reproduzierbare Tests für eigene Domänenlogik ausführen: positive, negative, Rand- und Fehlerfälle. **Nach jeder verhaltensändernden Implementierung**, nicht nur beim Phasenabschluss.
2. Testfixture für eine gültige und mehrere ungültige/teilweise unbekannte Nachrichten. Contract-Schema lokal prüfen; bei fehlendem Validator minimaler Format-/Semantiktest plus sichtbarer Hinweis auf fehlende formale Validierung.
3. Tests nach Integration von Änderungen an Parser-/Anbieterschemas. Offline-Fixtures im Git; Live-Quelle nur kontrolliert, zulässig, ohne Zugangsschutz/Geheimnisse zu umgehen. Live-Tests vor Abschluss jedes liveabhängigen Adapters und erneut, wenn Quelle/Anfrage verändert wird.
4. Eigene Vergleiche vollständig deterministisch ohne Preis-Float; Grundpreis-, Rabatt-/Pfand-, Mengen- und Datumsfälle.
5. Testen, dass `suggest`, `parse`, `compare` und `generate` **keine realen Bestände, Zahlungen oder Ernährungseinträge** verändern.
6. Testbericht nach jedem Meilenstein: Kommando, Datum, Commit, Anzahl bestanden/nicht bestanden/übersprungen, Datenumfang, behauptetes Ziel, offene Einschränkungen.
7. Negative Testfälle nicht durch Auslassen, Abschwächen oder Stub-Pass kaschieren; falsche Live-Ergebnisse nicht mit Mock-Erfolgen verwechseln.

## E. Definition of Done – Stufen
- `RESEARCHED`: Idee/Endpoint/Algorithmus gefunden, Nachweise, Grenzen dokumentiert; **nicht fertig**.
- `PROTOTYPE`: Beispielpfad funktioniert, noch keine garantierte Fehler-/Testabdeckung; **nicht fertig**.
- `OFFLINE_VERIFIED`: deterministischer Fachkern mit synthetischen Tests, Schema-Beispielen, Fehlerpfaden, keine Abhängigkeit von unerprobter Live-Quelle im Test; noch nicht komplett.
- `SOURCE_VERIFIED`: alle beanspruchten externen Quelleinbindungen mit aktuellen begrenzten und zulässigen End-to-End-Nachweisen und klarer Abdeckung; Lizenzstatus bleibt gesonderte Prüfung.
- `READY_FOR_INTEGRATION`: **alle** modulindividuellen Abnahmekriterien bestanden; alle Dokumente und Beispiele vollständig; Kompatibilität/Android-Weg angegeben; Sicherheits- und Rechtefragen als Freigabe-Gate transparent. Bei unzulässiger/ungeklärter Live-Nutzung kann nur der Offline-Adapter als integrationsreif gelten, nicht die produktive Live-Quelle.
- `INTEGRATED`: Nur Codex darf nach echter Haupt-App-Integration, Migrationen, Regression und Geräteprüfungen setzen; niemals von Fach-Chat behaupten.

## F. Lieferartefakte je Modul
`AGENTS.md` (bindende Anweisung), `README.md` (Einstieg), `docs/DEVELOPMENT_MANDATE.md` (fachliche Zielsetzung/Grenzen), `docs/ACCEPTANCE.md` (Tests/DoD), `docs/INTEGRATION.md` (API/Beispiele, Android-Anbindung), `docs/STATUS.md` (gemessener Status/Offenes), `tests/` und `examples/` oder äquivalent. Ein bestehendes Forschungsrepo behält alle historischen Berichte; neue Erkenntnisse kennzeichnen veraltete Testzahlen ohne Originaldaten zu löschen.

Übergabe-Checkliste: 
- [ ] Vertragsversion/Commit fixiert; Quellen, Lizenzen, Dritt-Abhängigkeiten dokumentiert
- [ ] Öffentliche Ein-/Ausgaben und Fehlermodell implementiert und mit Samples belegt
- [ ] Keine reale Nutzer-/Produktivdaten in Repo/CI/Logs; Secrets geprüft
- [ ] Onlineausfall, Teilabdeckung, unbekannter Wert, dubiose Mengen, Fehlzuordnung und widersprüchliche Datumsintervalle behandelt
- [ ] Tests **tatsächlich** gelaufen; Befehl, SHA und Ergebnis nachvollziehbar
- [ ] Kein direkter Schreibzugriff in anderen Repos/Haupt-App/produktives Sheet
- [ ] Integrationsskizze zeigt pure Funktionen, Adaptergrenze, deterministische Tests und Migrationsbedarf
- [ ] Limitierungen mit Auswirkung für Nutzer aufgeführt

## G. Änderungsprotokoll und Konfliktmanagement
Anfrage im eigenen Repo: `CR-YYYYMMDD-<slug>`; Situation, Reproduktionsbeleg, derzeitiger Vertrag, gewünschte neue Felder/Semantik, vorhandene Abnehmer, Migration, Testmatrix, Kompatibilitätsrisiko. Architektursteuerung bewertet und veröffentlicht `docs/DECISIONS.md` / neue Vertragsdatei. Fach-Chat implementiert erst nach Versionsfreigabe verbindliche Änderungen; interne Lösungsversuche sind weiter erlaubt. Keine stille Neudefinition von `priceCents`, `bio`, `storeId` oder `confirmed`.

## H. Tests/CI und Kosten
GitHub Actions im Free-Kontingent nach Bedarf; kein Dauerpolling, kein unnötiger Voll-Katalog-Massendownload, keine automatisierten Monitoring- oder Background-Jobs ohne gesonderten Auftrag. CI-Ausgaben kompakt halten, personenbezogene Daten und Tokens vermeiden. Saubere Timeouts, Request-Limits, Caching, Retry mit Backoff nur im zulässigen Quellenrahmen und Provider-Ausfälle transparent machen. Lizenz- und robots-/Nutzungsregeln dokumentieren.

## I. Test-/Betriebsdaten und Datenschutz
Synthetische Daten standardmäßig. Echte Kassenbons/Filialidentitäten/Beobachtungen aus Nutzerbestätigung bleiben in freigegebenem privaten Kontext; nicht in GitHub-Code, Issues, Actions-Artefakten oder öffentlichen Fixtures. Keine automatisierte Synchronisierung des produktiven Google Sheets. Die Schema-Version des Sheets 1.1.0 und die App-Demo Room 7 sind **verschiedene Systeme**. Datenmigration nur bei ausdrücklichem Auftrag durch Codex, mit Datenerhalt und Rückprüfung.

## J. App-Integrations-Gate (Codex)
Keine 1:1-Festschreibung von Zulieferer-DTOs in Room. Codex validiert, normalisiert und schreibt nur über bestehende transaktionale `FoodStore`-Grenze. Vorher/nachher gleiche Testfälle auf echtem App-Modell; Versionshistorizität, unveränderte IDs/Chargen/Buchungen, Idempotenz, Race Conditions, Migration über alle Altschemas, offline/randlastige Geräteszenarien. No-Go bei stillen Änderungen produktiver Bestände, doppelt bezahlten Belegen, fehlerhaftem Vergleich oder Daten-/Lizenzrisiken.

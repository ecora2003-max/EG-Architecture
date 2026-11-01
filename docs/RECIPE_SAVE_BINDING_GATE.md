# Rezeptfreigabe an konkreten Entwurf binden – Save-Time-Abnahme

**Stand:** 01.11.2026, 06:13 UTC · **Status:** `SYNTHETIC_SAVE_REVALIDATION_JVM_VERIFIED / APPROVAL_BINDING_PENDING / NOT_INTEGRATED`. Dies ist ein Architektur- und Abnahmeauftrag für Codex; **kein** Fremdrepo wurde beschrieben.

## Verifizierter Host-Stand

[GitHub Actions 41279640831](https://github.com/ecora2003-max/Ernaerungsgedaechnis/actions/runs/41279640831), Job `124768754231`, Code-/Test-SHA [`786271e8`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/commit/786271e840b1495e5f2eacf11595f552c72ce355): `completed/success`. Originaljoblog: `BUILD SUCCESSFUL in 3m 10s`, frische `JUNIT_XML: files=43 tests=315 failures=0 errors=0 skipped=0 migrations=7`; gepinnte Rezept-v1-Schemafixtures **9 positiv / 14 negativ**, Python-Vollaufrufe **9/12/7/7**, Lint, Room-8-Schema und Android-Testkompilierung bestanden. APK übersprungen, **0 Geräte-/Emulatortests**. Nachfolgender Hauptrepo-HEAD `b136cba1` ändert laut Commit-Dateiliste nur `docs/STATUS.md`.

Die [Host-Transaktion `FoodStore.saveReviewedRecipeDraftV1`](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/786271e840b1495e5f2eacf11595f552c72ce355/app/src/main/java/de/ernaehrung/demo/data/local/FoodStore.kt) liest vor `kitchen.saveRecipe` die aktuelle Room-Produktversion erneut und vergleicht das neu berechnete `RecipeInput` mit dem übergebenen `expectedPreview`. Fünf synthetische [Room-Tests](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/786271e840b1495e5f2eacf11595f552c72ce355/app/src/test/java/de/ernaehrung/demo/RecipeDraftCatalogSaveTest.kt) prüfen Wiederholung, fehlende Bool-Bestätigung, Änderung von Titel/Menge/Allergen, zwischenzeitliche Produktrevision und Operation-Key-Kollision. Zwei neue [Importtests](https://github.com/ecora2003-max/Ernaerungsgedaechnis/blob/786271e840b1495e5f2eacf11595f552c72ce355/app/src/test/java/de/ernaehrung/demo/RecipeDraftV1ImportTest.kt) decken verschachtelte Buchungsbehauptungen und einen zukünftigen Host-Kontextzeitpunkt ab. Diese Tests beweisen **keine** produktive Benutzerbestätigung.

## Konkrete Bindungslücke vor einer Freigabe

Der aktuelle Save-Einstieg erhält `expectedPreview: RecipeInput`, `confirmed: Boolean`, `request.userConfirmedRecipeSave`, `confirmations` und `reviewedStates` **als Aufruferparameter**. Das `RecipeInput` enthält nicht die vollständige `recipe.draft`-Nachricht: insbesondere wird `draftId` beim JSON-Import zwar gelesen, aber nicht in das zurückgegebene `RecipeInput` aufgenommen. Ebenso sind Trace-/Quellmetadaten, Warnungen, die Einwilligungskonfiguration und die Provenienz der unabhängigen Hostbelege nicht vollständig in dieser Gleichheitsprüfung gebunden. Daher ist eine **Bindung der ausdrücklichen Zustimmung an genau den geprüften Entwurf** bislang nicht nachgewiesen. Ein tatsächlich erfolgreiches Austauschszenario wird hier **nicht** behauptet; es muss durch Negativtests geprüft werden.

### Verbindliche Soll-Invariante für Codex

Eine Rezeptübernahme ist nur zulässig, wenn die tatsächliche, auditierbare Nutzeraktion exakt zur **erneut validierten** Freigabebasis passt:

- Versioniertes, kanonisches Digest des **gesamten** eingehenden `recipe.draft` (inkl. `draftId`, Metadaten, Warnungen und Erweiterungen), Vertragsversion und vollständige Draft-2020-12-Laufzeitvalidierung; keine Modell-Behauptung ist Bestätigungsbeleg.
- Unveränderliche Referenz auf den geprüften Request: drei Kontextflags, bestätigte Einschränkungen, Portionen, datierte Host-Kontextsnapshots und getrennt belegte Quellen-/Rechteentscheidungen. Entzogene Einwilligung sperrt Save.
- Jede Zutatenzeile: explizit bestätigte `foodTypeId`→Produktversionsidentität, aktuelle Revision, Menge, Basis, RAW/COOKED, Allergene und Zeit/Quelle des Hostbelegs; unbekannt bleibt unbekannt.
- Bestätigungsereignis mit eigener eindeutiger ID, Nutzeraktionszeit und Bezug auf Freigabedigest, Hostbelegrevision und Operation-Key. **Ein vom Aufrufer gesetztes Boolean oder ein KI-generiertes Feld reicht nicht.**
- Erneute Prüfung dieser Bindung **innerhalb derselben Room-Transaktion** wie die Rezeptversionserstellung; Replay mit identischem Key und identischem Beleg ist idempotent, abweichender Key-/Digest-Inhalt wird abgewiesen. Weder Vorschau noch Save erzeugen Kauf-, Lager-, Herstellungs- oder Verzehrereignisse.
- Eine künftige Persistenz- oder Schemaänderung erfordert neue versionierte Room-Exports, nichtdestruktive Migrationen und befüllte Erhaltungstests. Keine echte Nutzer-/Sheets-Datenübernahme.

## Ausführbare Abnahmematrix

[Maschinenlesbares Register](../policies/recipe-save-binding-acceptance.v1.json): **8 eng begrenzte, bereits durch konkrete JVM-Testmethoden belegte Szenarien** und **14 explizit ausstehende Fälle**. Dazu zählen Entwurfs-ID-Wechsel bei gleichem `RecipeInput`, Metadaten-/Warnungsänderung, Kontextentzug, Provenienz, Cross-Draft-Replay, parallele Produktänderung, Prozessneustart, vollständige Runtime-Schemavalidierung, gepinnte Rezept-Revalidator-Parität und Android-UI-Instrumentation. [Offline-Validator](../tools/validate_recipe_save_binding_acceptance.py) prüft die Registerkonsistenz und Negativmutationen, **führt aber keine Host-Tests aus**.

**Freigaberegel:** Die bisherige synthetische Save-Time-Room-Prüfung ist bestanden; `fullDraftIdentityBoundToApproval=false`, `durableUserConfirmationRegistryVerified=false`, `fullRuntimeSchemaVerified=false`, `moduleRevalidatorParityVerified=false`, `androidDeviceVerified=false`, `integrated=false`. Vor einer Umstellung dieser Werte sind echte aktuelle Host-Code-/Test-SHAs, vollständige Ergebnisprüfung und ein neuer belegter Abnahmeentscheid nötig. Verträge `1.0.0-draft` und `1.1.0-draft` bleiben unverändert; keine separaten juristischen Prüfaufträge gemäß ADR-019.

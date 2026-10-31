# Kanonisches fachliches Datenmodell – Begriffe und Invarianten
**Status**: 1.0.0-draft, fachliche Bedeutung verbindliche Arbeitsannahme; keine feste Room-/SQL-Struktur.

## 1. Trennung der Identitäten
| Entität | Wofür steht sie? | Referenz / Beispiel |
| --- | --- | --- |
| `FoodType` | allgemeiner Lebensmitteltyp, vergleichbare Nutzung; hierarchisch, editierbar | „zarte Haferflocken“, „Tofu natur“ |
| `Product` | konkrete Hersteller-/Handelsware und ggf. Variantenidentität | Marke, Geschmacksrichtung, Bio-Kennzeichen |
| `RetailerArticle` | Zuordnung einer Ware zu Händlerartikelnummer/Verkaufskontext | händlergebundene `sku`, `storeId` |
| `Package` | verkäufliches Gebinde und nutzbare Menge | „2×500 g“, „1 Stück“ |
| `GTIN` | standardisierte Barcodekennung von Handels-/Verpackungsebene | 8/12/13/14 gültige Ziffern; keine automatische Identität mit Boncode |
| `ReceiptAlias` | händlergebundener, originalgetreuer Bonzeilentext → *Kandidat* | `HAFERFL ZART`; Bestätigung separat |
| `PriceObservation` | konkreter Preis zu Produkt/Gebinde/Ort/Zeit/Quelle | Aktion, aktueller Webpreis, historischer bezahlter Bonpreis |
| `Offer` | zeitlich begrenzte Kondition, häufig Aktionspreis | `validFrom`, `validUntil`, Couponbedingungen |
| `ReceiptLine` | Originaltext und Positionsbetrag auf einem Beleg | kann Pfand, Rabatt, Non-Food sein |
| `ProductMatch` | *nachvollziehbare Zuordnung* zwischen zwei Identitäten | Score, Beweise, Zustand, Nutzervotum |
| `ComparisonResult` | fachlich begründete Preisaussage für Zieltermin | günstigere Kandidaten + Warnsignale + Datenlücken |
| `RecipeDraft` | nicht bestätigte, möglicherweise KI-generierte Rezeptversion | Zutaten, Mengen, Schritte, offene Punkte |
| `StockSnapshot` | ausdrücklich bereitgestellter lesender Blick auf physischen Stand | zeitgestempelt, ggf. unvollständig |
| `ShoppingNeed` | berechneter zukünftiger Bedarf/Restbedarf | kein Kauf und keine Reservierungsbewegung |

**Keine scheinbaren Eins-zu-eins-Beziehungen:** Mehrere SKUs können zu einem FoodType gehören, eine GTIN kann eine andere Gebindeebene beschreiben, ein Händler kann seinen Artikelcode umstellen; derselbe Bontext kann mehrere Artikel meinen. Identitätszuordnung benötigt eigene Beweiskette. Echte produktive App-IDs werden nie von Zulieferern erfunden.

## 2. Produktmerkmale und Vergleichbarkeit
`brandName` (falls vorhanden) und `brandKind` (`MANUFACTURER`, `PRIVATE_LABEL`, `UNKNOWN`) sind von `organic` (`true`, `false`, `null`) getrennt. `false` nur bei begründetem Nicht-Bio; fehlender Öko-Hinweis beweist nicht automatisch „nicht bio“. Eigenschaften wie Tierart, Fettgehalt, Verarbeitung, gezuckert/ungesüßt, frisch/TK, Sorte, Verwendungszweck und Allergeninformationen müssen als vergleichsrelevante Attribute übermittelbar sein. Keine Gleichsetzung durch Schlagwort allein.

Produktvergleich in fachlichen Stufen: `EXACT_SKU` (Identität/GTIN/Gebinde geprüft), `SAME_FOOD_VARIANT` (gleiche Funktion/Variante, ggf. andere Marke), `FUNCTIONAL_SUBSTITUTE` (echte Alternative mit offengelegtem Unterschied), `NOT_COMPARABLE`, `UNKNOWN`. Ein Vergleich darf mehrere Alternativen und Kontraindikationen enthalten.

## 3. Händler, Märkte und Herkunft
`retailerId`: stabile kettenbezogene ID, `storeId`: Händler-intern und **nur innerhalb retailerId** eindeutig. `scopeType`: `STORE_CONFIRMED`, `REGION_CONFIRMED`, `CHAIN_WIDE_REPORTED`, `ONLINE`, `UNKNOWN`. Nie einen Kettenpreis als bestätigten Preis jeder Filiale ausgeben. **Netto Marken-Discount** ist nicht „Netto mit Scottie-Hund“; Händleridentität strikt bewahren.

Quelle: ursprünglicher Anbieter, offizieller Link/Quellbeleg (wenn vorhanden), Abrufzeit, Nutzungsstatus, Qualität/Ausschnitt, ggf. parserVersion. `rightsStatus=UNVERIFIED` ist Standard, kein `PERMITTED` ohne belegte Rechte. Live-Abruf vs. statische App-Analyse vs. Dritt-Dokumentation separat dokumentieren. Öffentlich erreichbarer Endpunkt ≠ Datennutzungserlaubnis.

## 4. Mengen und Geld
- Geld: `priceCents` als nichtnegative ganze Zahl, `currency=EUR`; null/fehlend bleibt unbekannt, `0` ist nur bestätigter Nullpreis. Bei Pfand, Rabatten und Coupons getrennte Felder; beworbene `oldPrice` nicht als tatsächlich erhobenen früheren Normalpreis umdeuten.
- Gebindemenge: Menge und Einheit (`g`, `ml`, `portion`, `piece`) **plus Mengenbasis** (`NET`, `DRAINED`, `GROSS`, `PIECE`, `UNKNOWN`) und Beleg-/Bestätigungsstatus. Vergleichs-Grundpreis nur mit **gleicher** physikalischer Einheit und verträglicher Mengenbasis; kg = 1000 g, l = 1000 ml. Bei `piece` keine automatische kg/l-Umrechnung.
- Mehrfachgebinde als `packageCount` und `quantityPerPackage` führen, nicht „5 kg“ als 500 g markieren. Keine Dichte-, Stückgewicht- oder Abtropfgewichtsannahmen ohne expliziten Nachweis.
- Preise für den zu kaufenden Packungsinhalt, für den Nutzer tatsächlich nutzbare Menge, Pfand und Endkosten getrennt, damit Budget-/Vergleichslogik korrekt ist.
- In der Ziel-App existieren ganzzahlige 1/1000-Basiseinheiten. Zulieferer dürfen präzise andere interne Repräsentationen verwenden; **Adapter konvertiert nach Prüfung und ggf. sicherem Aufrunden**.

## 5. Zeit, Lebenszyklus und Qualität
`observedAt`: wann Preis/Information tatsächlich beobachtet/ausgelesen wurde. `validFrom`/`validUntil`: zu welchem Kaufzeitpunkt beworbene Kondition gilt, wenn bekannt. `purchaseAt`: bestätigter Kaufzeitpunkt. `sourceUpdatedAt`: eigener Händler-Zeitstempel nur wenn vorhanden. `checkedAt`: aktueller Prüflauf. Kein HTTP-Date als Produkt-Update-Zeitstempel deklarieren. Alle absoluten Zeitstempel ISO-8601 mit Zone/Offset; Tagesgültigkeiten explizit lokale Händlerzone, standardmäßig Europe/Berlin.

`dataQuality`: `CONFIRMED` (spezifisch verifiziert), `SOURCED` (aus Quelle übernommen, Nutzer noch nicht bestätigt), `ESTIMATED`, `UNKNOWN`. `coverage`: welche Filialen, Kategorien, Suchanfragen, Datumsintervalle und Anteil tatsächlich geprüft wurden; ein `totalCount` ist kein bewiesener Gesamtbestand.

## 6. Preise nach Bedeutung – niemals vermischen
`SALE`: beworbene Aktion; `CURRENT_DISPLAYED`: momentan angezeigter Kaufpreis; `LISTED_REGULAR`: ausdrücklich als regulär bezeichneter Preis, unverifizierte historische Geltung; `REFERENCE_OLD`: durchgestrichene Händlerreferenz; `HISTORICAL_PAID`: anhand bestätigtem Kauf gezahlt, datiert; `ONLINE_LISTED`: Shoppreis, nicht notwendigerweise Marktpreis. Auch „aktueller Preis“ kann bereits Aktion enthalten. Preisbeobachtung ist kein Stockevent.

## 7. Bon-Fakten, Zuordnung und Preisgedächtnis
Bon-OCR erzeugt **unveränderlichen Rohtext und überprüfbare Vorschläge**. Die Haupt-App verfügt bereits über OCR, GTIN-Prüfung, Händleraliase, Belegentwürfe und explizite Kaufannahme. Ein Modul übernimmt diese Systeme **nicht** als zweite Wahrheit.

- Pro Bonposition: Originaltext, erkannter Text, gedruckter Positions-/Einzelpreis, Menge soweit belegt, Kategorie `FOOD`, `NON_FOOD`, `DEPOSIT`, `DISCOUNT`, `RETURN`, `UNKNOWN`; separater Beleg-Gesamtzahlbetrag.
- Produktkandidaten aus EAN/GTIN, Händlerartikelnummer, Alias, Text/Packungs- und Händlerkontext ableiten. `suggested`/mehrdeutig/konfliktbehaftet nicht als bestätigte Zuordnung ausgeben.
- Lernen nur auf Grundlage **ausdrücklich bestätigter** Zuordnungen und ihrer Händler-/Variantenbindung. Bonpositionen mit Rabatten können einen gewichteten effektiven Stück-/Gebindepreis nur ergeben, wenn Rabatt tatsächlich eindeutig einer Position zugeordnet ist. Sonst Preis offen, aber Belegsumme erhalten.
- Deduplizierung: Belegbild-Fingerprint, Transaktions-ID, Position-ID und Wiederholungs-/Storno-Beziehungen; gleicher Händler/Tag/Summe ist Hinweis, **kein** Duplikatbeweis.
- Zeitgebundene belegte Preise mit Herkunft als Preisgedächtnis; keine still aktualisierten „Normalpreise“. Persönliche Bons gehören **nicht** in öffentliche Repositories oder geteilte APIs.

## 8. Preisvergleichssignale
Preise aus allen 8 Aktionsquellen plus erreichbare aktuelle reguläre Händlerpreise (Lidl, ALDI Nord/Süd, REWE als gegenwärtige Kandidaten, Vollständigkeit unbewiesen) plus passende historische, als solche gekennzeichnete Beobachtungen. **Rot** = belegte aktuell günstigere **funktional gleiche** Option mit identischem Bio-Status; **Orange** = günstigere funktionale Alternative mit abweichendem Bio-Status; **Grau** = relevanter fehlender/unklarer/alter Datenausschnitt, Wortlaut „Könnte es günstiger geben“. Die Signale sind **nicht exklusiv**. Preisvergleich pro kg/l nur bei kompatiblen nachgewiesenen Mengen, Preisdatum und Zugangsvoraussetzungen; bei Bio unbekannt keine rote/gelbe Gewissheit.

Produktidentität und Vergleich werden **separat** bewertet. Es ist möglich, exakt identische Markenprodukte nach Händler preislich zu vergleichen. Marke/Eigenmarke ist kein Grund, vergleichbare Alternativen auszublenden.

## 9. Rezept-KI und Planungsdaten
Input: unabhängige boolesche Kontextwahlen `considerStock`, `considerShopping`, `considerOffers`; nur bereitgestellte Snapshots werden verwendet, keine implizite Nutzerdatenabfrage. Rezept-Output: Name, Rohzutaten mit geprüften Einheiten, Portionen, Zeiten, Methoden, Quelle/Unsicherheit und offene Datenfelder; separat berechnete Nährwerte nur anhand belegter Zutatendaten. Rezeptentwurf bucht **nichts**. Nicht bestätigte Allergie- oder Gesundheitsinformationen werden nicht als ausgeschlossen angenommen. Fehlende Lagerkapazität, Kühlkette, Haltbarkeitsbelege und Budget bedeuten „nicht geprüft“, nicht „sicher“. Kochen erzeugt später echte Chargen, Verzehr separat und nur bei Nutzerbestätigung.

## 10. Geplante Informationspakete
Maschinenlesbarer Nachrichtenumschlag: `contractVersion`, `messageType`, `meta`, `payload`. Zieltypen: `price.observation`, `product.match`, `receipt.line`, `comparison.result`, `recipe.draft`. Der Adapter prüft Schema, Version, Identitäten, Mengen, Status, Datumsbezug, Quellen. Module dürfen eigene Zusatzfelder als namespaced Extensions ergänzen; **niemals** Pflichtbedeutungen ändern. Siehe `contracts/v1/`.

## 11. Tests und Abnahme
Pflicht-Tests für Null/0, Preis- und Mengenrundung, mehrere Filialen, veraltete Preise, Bio/unbekannt, Produktverwechslung, Rabatt/Pfand, doppelte Belege, Eventvorschlag ohne Seitenwirkung, fehlende externe Quelle und Vertragsschema. Jeder Test mit synthetischen Produkten und erfundenen IDs – keine personenbezogenen Daten. Nachweisbar prüfbare Modulfunktionen können `READY_FOR_INTEGRATION` melden; `INTEGRATED` darf nur Codex nach App-Gesamttest setzen.

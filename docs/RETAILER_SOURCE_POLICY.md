# Verbindlicher fachlicher Händlerumfang – 31.10.2026

**Architekturentscheidung zur gewünschten Funktionalität, keine Feststellung einer Nutzungslizenz.** Maschinenlesbare Matrix: [retailer-source-capabilities.v1.json](../policies/retailer-source-capabilities.v1.json).

## Gewünschter Funktionsumfang

| Händler | Gezielte Produktpreisabfragen | Erfassung veröffentlichter Angebote |
| --- | --- | --- |
| ALDI Nord | **Ja** | **Ja** |
| ALDI Süd | **Ja** | **Ja** |
| REWE | **Ja** | **Ja** |
| Lidl | **Ja** | **Ja** |
| Penny | **Nein** | **Ja** |
| Kaufland | **Nein** | **Ja** |
| EDEKA | **Nein** | **Ja** |
| Netto Marken-Discount | **Nein** | **Ja** |

**Geltungsbereich:** „Ja“ bedeutet *fachlich zur Implementierung vorgesehen* und *bei zulässiger Quelle nutzbar*, nicht automatisch „Datenabruf rechtlich freigegeben“. „Nein“ schließt diese Funktion für den genannten Händler im neuen Projektumfang aus, auch wenn ein früherer Forschungsadapter technisch Preise abrufen konnte. Netto Marken-Discount ist jetzt ebenfalls **nur für die Angebotserfassung**, nicht für gezielte reguläre Preisabfragen vorgesehen. Bestehende Forschungsergebnisse bleiben erhalten; eine Produktivfreigabe folgt daraus nicht.

## Präzise Trennung

**Gezielte Produktpreisabfrage:** Einzelne Produkte, GTINs oder bekannte FoodType-Suchbegriffe auf konkreten Nutzerwunsch bzw. klar begrenzten Einkaufsbedarf hin, mit begrenzter Anzahl Treffer, Kontrolle von Filiale/Region/Zeitpunkt und Rate-Limits. Kein automatisierter Vollsortiments-/Bulk-Katalogdownload. Ein gefundenes Produkt ohne verlässlichen Regalpreis bleibt im Ergebnis *Preis unbekannt*.

**Angebotserfassung:** Ausdrücklich veröffentlichte, datierte Werbe-/Aktionsangebote als strukturierte Preisbeobachtungen; vorzugsweise quellenminimal ohne fremde Bilder, vollständige Prospekte oder urheberrechtlich geschützte Werbetexte zu kopieren. Aktionen für Zukunftstermine nur bei tatsächlicher Veröffentlichung. Coupons, Kundenkarte, Mindesteinkauf, Gültigkeitsfenster, Filial-/Regionstyp und unbekannte Bedingungen getrennt; keine Behauptung des heutigen Kassenpreises. Anbieter ohne nachweisbare aktuelle Angebote bleiben `UNKNOWN`, keine erfundene Vollständigkeit.

**Nicht neu erlaubt:** Regelmäßiges massenhaftes Abfragen von Einzelpreisen als verdeckter Gesamt-Katalog; Umgehung von Login, Bot-Sperren, 403/429, Captchas oder vertraglichen Zugangsbeschränkungen; ungefragte Weiterveröffentlichung fremder Datenbankinhalte; ungeprüfte Händler-/Quellenrechte; Produktivdaten, Kundenzugänge oder fremde Test-Repositories. Bestehende Datenschutz-, Free-Plan- und Offline-Grenzen gelten unverändert.

## Rechtlich-technisches Gate je Quelle, unabhängig von Händlernamen

1. **Nutzungsart prüfen:** Technischer Zugriff, Umfang/Regelmäßigkeit, Datenbankherstellerrechte (§§ 87a ff. UrhG), wirksame Nutzungsbedingungen, Nutzung eigener Texte/Bilder, Zweck und mögliche Ausnahmen sind quell- und verfahrensbezogen zu beurteilen. Einzelne Preisfakten sind nicht schon deshalb lizenzpflichtig, weil sie von einem Händler stammen; umgekehrt bedeutet öffentlich abrufbar nicht frei für systematische Übernahme.
2. **Quelle beurteilen:** `source.rightsStatus` beschreibt den geprüften Rechts-/Freigabestand. `UNVERIFIED` ist *ungeprüft*, **nicht nachgewiesenermaßen verboten**; `RESTRICTED` kennzeichnet eine bestimmte bekannte Einschränkung. Ein `PERMITTED`-Status muss auf dokumentierter geltender Rechtsgrundlage (z. B. einschlägiger gesetzlicher Erlaubnis oder Lizenz) mit konkretem Umfang beruhen und darf nicht bloß aus einem erfolgreichen HTTP-Aufruf entstehen.
3. **Vor produktivem Abruf/Anzeige:** Für jeden Händler und *jede konkrete Datenquelle/Technik* muss die Erhebung und anschließende Anzeige rechtlich hinreichend beurteilt, dokumentiert und technisch begrenzt werden. Solange ungeklärt: Forschung/Synthetik nach zulässigen Grenzen, aber keine ungeprüfte Produktiv-Freischaltung externer Daten.
4. **Einkaufsintelligenz und Codex:** Prüfen in `APP_DISPLAY` die Rechte *und* diese Händlermatrix. Nicht erlaubte **Produktpreis-Abfragen** für Penny/Kaufland/EDEKA dürfen auch nicht durch direkte Nutzung eines existierenden Preisadapters umgangen werden. Deren veröffentlichte Angebote sind funktional vorgesehen, unterliegen aber denselben Quellenrechten wie alle anderen externen Daten. Fehlende Abdeckung führt zu Datenlücke/Grau statt spekulativem Bestpreis.
5. **Eigene Bons separat:** Bestätigte persönliche Kassenbonpreise aller Händler bleiben als datierte historische Einzelbeobachtungen im privaten Preisgedächtnis möglich; dies ist keine externe gezielte Live-Abfrage und keine aktuelle Regalpreisaussage.

## Pflicht-Tests

- **Vier positive Zielhändler:** Gezielte, exakt begrenzte Produktpreisanfragen und Angebotserfassung für ALDI Nord/Süd, REWE, Lidl im Policy-Gate erlaubt; Rechts-/Quellprüfung für Produktivabruf separat nachweisen.
- **Vier Negativhändler:** Gezielte Produktpreisabfragen Penny, Kaufland, EDEKA und Netto Marken-Discount werden vom Funktions-Policy-Gate zurückgewiesen – auch wenn ein Preis-HTTP-Endpoint zufällig existiert. Ihre veröffentlichten Angebote werden funktional akzeptiert, falls Datums-/Quellen-/Rechtsbelege vorhanden.
- **Netto:** Nur veröffentlichte Angebote sind funktional vorgesehen; keine gezielte reguläre Einzelpreisabfrage. Das gilt auch für bereits vorhandene experimentelle Preisparser. Vor produktiver Nutzung sind Rechts- und Quellenprüfungen erforderlich.
- **Rechte:** Jeder Funktionsfall mit `UNVERIFIED`/`RESTRICTED` Quelle darf nicht ohne dokumentierte Klärung als produktive App-Anzeige/Live-Nutzung durchgehen; kein Datenverlust, kein stilles Umschreiben in `PERMITTED`.
- **Vergleiche:** Gemischte Händler, fehlende Normalpreisquellen, unbekannter Bio-Status, unbekannte Menge, alte Angebote, nur eine Filiale, Coupon-/App-Bedingungen, getrennte historische Bons, doppelte OCR-Scans und No-Side-Effects.
- **Echte Abnahme:** Ausführbarer Testcode, synthetische Fixtures und CI-Nachweise je geänderter Modulimplementierung. Keine Freigabe aufgrund dieser Dokumentation allein.

## Umsetzung und Repository-Grenzen

Die Architektursteuerung darf **nur** `EG-Architecture` schreiben. Der **Preisdaten-Chat** baut die Matrix und Quell-Gates in `EG-Preisdaten` ein. **Einkaufsintelligenz** prüft sie bei Produktpreis- und Angebotsvergleich/Vorschlägen. **Codex** integriert die Grenzen in die private Android-App. Die anderen Modul-Chats lesen diese Vorgabe, ändern sie nicht. Änderungen an bestehenden Verträgen nur versioniert, mit Tests und expliziter Freigabe.

**Status:** `FUNCTIONAL_SCOPE_DECIDED / IMPLEMENTATION_PENDING`. Kein Nachweis neuer Händler-Live-Rechte oder produktiver Android-Durchsetzung.

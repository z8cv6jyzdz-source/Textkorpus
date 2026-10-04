# Durchsichtsprotokoll Phase 6.2 — Code-Durchsicht über Kreuz

**Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 6.2 · Stand 25.09.2026**

Voraussetzung erfüllt: Der Abgleich 6.1 ist bestanden (Abgleichprotokoll_2026-09-25). Die Durchsicht prüft die Skripte beider Implementierungen gegen die Spezifikation (Stand Nachtrag 2), gegen die Festlegungen des Rückfragenprotokolls vom 25.09. und gegen die Code-Regeln des Auswertungsverfahrens (3.2 Skriptkopf, 3.3 keine eingetippten Zwischenwerte, keine nachbearbeiteten Ausgaben, fester Startwert, Abbruch mit Meldung). Sie nennt keine Ergebniszahlen.

## Teil A · R-Skripte der zweiten Instanz, durchgesehen von der ersten Instanz

**Gelesen:** `Funktionen_2026-09-25.R` (Bibliothek), `S01` bis `S19`, `Gesamtlauf_2026-09-25.R` (Auszug), `Referenztests_2026-09-25.R` (über das Validierungsprotokoll), `Abgleich_2026-09-25.R`, `Pruefsummen_Abgabe_2026-09-25.R`.

### A.1 Code-Regeln (Auswertungsverfahren 3.2 bis 3.4)

| Regel | Befund |
|---|---|
| 3.2 Skriptkopf mit Zweck, Spezifikationsbezug, Eingang mit Prüfsumme, Fassung, Aufruf | In allen 24 Skripten vorhanden. Die Prüfsummen des Datenstands stehen im Kopf von S01 und werden von jedem Folgeskript über die Zwischendatei in die Ausgabe geschrieben, die Sollprüfsummen der Anlagen in der Bibliothek (`ANLAGEN`) und werden vor jeder Verwendung geprüft (`lies_anlage`) |
| 3.3 keine eingetippten Zwischenwerte | Erfüllt. Alle Schwellen, Faktoren, Wochengrenzen, Sitzungsdauern, Koeffizienten und Codebuchlabels werden aus den Anlagen gelesen. Selbst die Listenlabels HL-01 bis BW-14 werden aus dem Codebuch gebildet und gegen die Regel geprüft. Die Konstanten PP 5, 6, 7 und AK 9 werden gegen die Kennungen abgeglichen (S08) |
| 3.3 keine nachbearbeiteten Ausgaben | Erfüllt. Die Ergebnisdatei entsteht aus den Registern der Schritte, formatiert mit `%#.17g`, Anzahlen und Merkmale werden auf Ganzzahligkeit geprüft |
| 3.3 fester Startwert | Erfüllt. `RNGkind("Mersenne-Twister", "Inversion", "Rejection")` und `set.seed(20260924)` vor jeder Zielgröße in S19 |
| 3.3 Abbruch mit Meldung | Erfüllt. `pruefe` und `abbruch` in allen Schritten, Warnungen werden über `withCallingHandlers` gesammelt und im Laufprotokoll gezählt (0 Warnungen) |
| 3.4 Fassungen | Alle Skripte tragen die Fassung 2026-09-25, erste Fassung, das Referenztestskript den Nachtrag Toleranz R08 |
| Lesarten | R1 und R4 als Schalter mit Abbruch bei fehlender Festlegung, R2 als benannte Konstanten, R3 in `paare_zaehlen`, A1 bis A13 im Rückfragenprotokoll |

### A.2 Regeln je Schritt

| Schritt | Geprüfte Regeln | Befund |
|---|---|---|
| S01 | Prüfsummen, Wertebereiche aller drei Eingänge, Schlüssel, Codes, Zusatzprüfungen A9, Ausgaben | ohne Abweichung. Strenger als A9: IG-Spieler mit Listenplatz müssen in der Zuordnung stehen (sinnvoll) |
| S02 | gültig_roh, Lauf über gleiche Versuchsnummer, Abschnitte ab 0 m, Δt ≤ 0 und v > 10 m/s, alle Teilzeiten des Laufs ungültig | ohne Abweichung. `lauf_gestoert` bricht bei doppelter Distanz ab |
| S03 | Reihenfolge NANG, AUSL, Vokabular, K5-Abbruch, Widerspruchsprüfung über alle Post-Zeilen nicht angetretener Spieler | ohne Abweichung |
| S04 | k, BEST, MEAN, CM aus Seiten-Bestwerten nur bei beiden Seiten, Gründe | ohne Abweichung. Zusatzprüfung „höchstens drei gültige Versuche“ |
| S05 | Umrechnung, MP, Gültigkeitsbereich, Interpolation, PAS, %PAH, K2 | ohne Abweichung. Vorrang „Eingang fehlt“ vor „außerhalb Gültigkeitsbereich“, siehe C.1 |
| S06 | Label, Fallkorrekturen aus der Anlage, Zuordnung mit Abbrüchen, Status, CR-10, Kalenderregel, K8, Paare | ohne Abweichung. Zusätzliche Prüfung, dass die Wochengrenzen der Konstanten sechs Wochen umfassen |
| S07 | GANZ, GT, WOCAP, DIST, nicht erhebbar mit 0 in Summe und Verteilung, Rate, V00 bis V12 mit Hinweis A6, GE, Median und Mittel über die zugeteilten Spieler, Wochenanteil, CR-10 und Load, UE | ohne Abweichung. Median und Mittel über alle Zugeteilten, wie die Kennungsanlage („je zugeteiltem Spieler“) und S07 Regel 6 verlangen, siehe C.2 |
| S08 | ITT, PP5 bis PP7, AK9, FAMS, INF, Mitgliedschaften, Fluss mit A7, Box 6, Anteile, ANA | ohne Abweichung |
| S09 | Bezugsmenge je Zeitpunkt, post ohne nicht angetretene | ohne Abweichung |
| S10 | TE über k ≥ 2, K15 für CM, χ²-KI, CV mit Mittel der TE-Menge, S und SESOI nur prä, RTS, FLEINZ, Vereine | ohne Abweichung |
| S11 | Δ aus Spielern mit gültigen Versuchen 1 bis 3, Lesart R1 a | ohne Abweichung |
| S12 | ANA, Familiarisierung, d ohne J in BASE und ITT, n, M, SD | ohne Abweichung |
| S13 | QR mit Spaltenskalierung, df, SE aus V, t, p, KI, adjustierte Mittelwerte am Setmittel, PREM, PAHM, SIG, H0REJ, NTEST, A10 | ohne Abweichung. Pivotierung der QR-Zerlegung wird abgefangen (Abbruch statt Fehlzuordnung) |
| S14 | Shapiro-Wilk (`shapiro.test`, AS R94), Q-Q mit `qqline`, Brown-Forsythe, Residuen-SD und Quotient, zwei Steigungsmodelle, Linearitätsgrafik, Überlappung, Vorab-Prüfung mit Lesart R4 a | ohne Abweichung. Q-Q-Linie durch die Quartile (`qqline`), in der Gegenprobe Mittel und SD, ohne Kennung |
| S15 | SD_prä gepoolt, df_g = n − 2, J, g, KI aus KI(b1), unadjustierte Differenz mit gepoolter Varianz | ohne Abweichung |
| S16 | PP6 mit Fallzahlregel und A10, Deskription unabhängig von INF, AK9-Einzelwerte | ohne Abweichung |
| S17 | MW, PP5, PP7, AEND (df n − 3), OPAH (df n − 3), FAMB (df n − 5), Variante a, Deskription | ohne Abweichung |
| S18 | df2 = N − 4, λ, F_crit, Power über `pf(ncp)`, `uniroot` mit tol 1e-10 und Konvergenzprüfung, keine Nullstelle, Kombinationen nach N4.15 | ohne Abweichung |
| S19 | Startwert je Zielgröße, Schichtung, Rangverwurf gezählt, Quantil Typ 7, SD, MC-SE aus 20 Blöcken, b1* als Zwischendatei | ohne Abweichung |
| G.1, G.2 | Ergebnisdatei, Vollständigkeitsprüfung je Schritt, Referenztests vor der Studienrechnung, Validierungsprotokoll | ohne Abweichung |

### A.3 Beobachtungen ohne Regelabweichung

1. Die Bibliothek rechnet SHA-256 in reinem R (FIPS 180-4) und ist im Validierungsprotokoll gegen `sha256sum` bestätigt. Im Container der ersten Instanz liefert sie für die PNG-Dateien dieselben Werte wie `sha256sum`, die Abweichung der PNG-Prüfsummen liegt am Metadatenblock der Dateiübertragung (Abgleichprotokoll § 2), nicht an der Bibliothek.
2. Rangkriterium: `qr()` mit der R-Voreinstellung (Toleranz 1e-7) auf der spaltenskalierten Matrix. Die Gegenprobe prüft den Rang über die Singulärwertzerlegung. Bei exakter Kollinearität stimmen beide überein, bei fast kollinearen Matrizen könnten sie auseinanderfallen. Im Datenstand ohne Wirkung (S19: 0 verworfene Ziehungen auf beiden Seiten).
3. Die Umgebungsdatei und das Laufprotokoll dokumentieren Aufruf, Umgebungsvariablen (LC_ALL, TZ), Paketstände und Prüfsummen vollständig. Ein Reproduktionstest (8.4) ist damit vorbereitet.

## Teil B · Python-Skript der ersten Instanz, durchgesehen von einer unabhängigen Prüfinstanz

Die zweite Instanz bleibt blind (Aufgabenstellung Phase 6), deshalb hat eine getrennte Prüfinstanz (Claude-Unteragent ohne Kenntnis der Rechnung, ohne Zugriff auf die R-Skripte und die Ergebnisdatei) `Gegenprobe_Python_2026-09-25.py` (Fassung 1) Regel für Regel gegen die Spezifikation, die Kennungsanlage und das Rückfragenprotokoll gelesen, ohne das Skript auszuführen. Bericht in Kurzform:

**Kritisch (Ergebnis falsch): keine.**

*Tab. 3.* Befunde der Prüfinstanz und Umsetzung in Fassung 2

| Nr. | Schwere | Befund | Umsetzung |
|---|---|---|---|
| 1 | mittel | S03 Regel 1: Widerspruchsprüfung (Wert in Post-Zeile eines nicht angetretenen Spielers) griff nur bei ungültigen Zeilen | behoben: Prüfung über alle Post-Zeilen solcher Spieler vor der Gültigkeitsabfrage |
| 2 | mittel | S05: Vorrang der Gründe bei Alter außerhalb und fehlendem Eingang nicht festgelegt, Skript gab „außerhalb Gültigkeitsbereich“ | angeglichen an die berichtete Rechnung („Eingang fehlt“ zuerst), Nachtragsvorschlag C.1 |
| 3 | mittel | Rangkriterium SVD statt QR-Toleranz, keine Spaltenskalierung | belassen, R05 (Longley) prüft die Stabilität auf 9 Stellen, Beobachtung A.3 Nr. 2 |
| 4 | mittel | S19: `continue` im Fehlerpfad bei weniger als zwei gültigen Ziehungen fehlplatziert (hätte mit „Kennung doppelt“ abgebrochen) | behoben |
| 5 | gering | R03 nicht über den S15-Rechenweg geprüft | behoben: zwei Zusatzprüfungen (gepoolte SD, t² = F) auf 9 Stellen |
| 6 | gering | Grafikdateien mit Zusatz `_Python`, kein Abbruch ohne matplotlib | belassen, bewusst, im Skriptkopf vermerkt |
| 7 | gering | S01: Seite außerhalb 505 nicht auf leer oder „–“ geprüft | behoben |
| 8 | gering | Anlagen in Dictionaries ohne Abbruch bei doppelten Schlüsseln | behoben (`dict_eindeutig`) |
| 9 | gering | Schwellen 5, 6, 7, 9 und Verteilung 0 bis 12 als Literale neben den gelesenen Konstanten | belassen, Werte identisch mit der Anlage, die Kennungen legen sie fest |
| 10 | gering | Referenztestausgabe ja/NEIN statt 0/1 | belassen (Protokollform) |
| 11 | gering | A9 strenger als vereinbart (Reihenfolge der Codes) | belassen, Datenwörterbuch garantiert die Reihenfolge |
| 12 | gering | Robustheit ohne Grund aus G.1 in Fällen, die der Datenstand ausschließt (SD post = 0, leere IG, leeres Alter) | belassen, Abbruch mit Meldung statt Grund ist nach 0.5 Nr. 10 zulässig |
| 13 | gering | Funktionsname, doppelter Zweig in `fmt`, feste Zahl 3 559 im Kopf | behoben |
| 14 | gering | Paare werden gezählt, nicht je Meldung gekennzeichnet | belassen, keine Kennung braucht die Kennzeichnung |

Gesamtbewertung der Prüfinstanz: regelgetreue Umsetzung in jedem Rechenschritt, kein Fehler mit Wirkung auf die Ergebnisdatei, als Gegenprobe geeignet. Fassung 2 mit den Behebungen lief erneut (Ergebnisdatei byteidentisch mit Fassung 1, SHA-256 `2d4ce431…`) und bestand den Abgleich 6.1 erneut.

## Teil C · Vorschläge für einen Nachtrag 3 zur Spezifikation (Entscheidung des Verfassers)

| Nr. | Stelle | Lücke | Vorschlag |
|---|---|---|---|
| C.1 | S05 Regel 4 und 9, G.1 Nr. 4 | Vorrang der Gründe bei Alter außerhalb und zugleich fehlendem Eingang nicht festgelegt | „Fehlt ein Eingang, gilt Eingang fehlt, auch bei Alter außerhalb des Gültigkeitsbereichs“ (wie in beiden Implementierungen umgesetzt) |
| C.2 | S07 Regel 7 gegen F.7 N4.3 | N4.3 sagt „Median und Mittel über Spieler mit Meldung“, S07 Regel 6 und 7 und die Kennungsanlage sagen „je zugeteiltem Spieler“, Spieler ohne Listenplatz mit 0 | N4.3 an Regel 7 und die Anlage angleichen. Beide Implementierungen rechnen über die zugeteilten Spieler |
| C.3 | 0.5 Nr. 11 | Rangkriterium nicht beziffert | „Rang nach QR-Zerlegung mit Toleranz 1e-7 auf der spaltenskalierten Designmatrix oder gleichwertig“, nur als Klarstellung |
| C.4 | G.1 Nr. 6 | Dateinamen der Grafiken nur für eine Implementierung eindeutig | Zusatz für die Gegenprobe erlauben (`_Python`) |

Keiner der Punkte ändert einen Wert der Ergebnisdatei im vorliegenden Datenstand. Bis zur Entscheidung gilt die Spezifikation im Stand Nachtrag 2.

## Ergebnis der Durchsicht

Beide Implementierungen setzen die Spezifikation regelgetreu um. Die R-Skripte der zweiten Instanz erfüllen die Code-Regeln 3.2 bis 3.4 vollständig. Das Python-Skript ist nach den Befunden der unabhängigen Prüfinstanz als Fassung 2 bereinigt, ergebnisneutral. Die Durchsicht 6.2 ist bestanden, es bleibt kein offener Punkt, der die Freigabe F2 hindert.

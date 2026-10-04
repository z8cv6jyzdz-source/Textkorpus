# Abgleichprotokoll Phase 6.1

**Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Phase 6 · Stand 25.09.2026**

Verfasser: Luca Klier · erste Instanz (Projekt): Claude Cowork, Sitzung vom 25.09.2026 · zweite Instanz (blind): Claude-Sitzung ohne Projektzugriff, Abgabe `Blindrechnung_R_2026-09-24\Abgabe_R_2026-09-25`

## 1 Gegenstand und Ergebnis

Phase 6.1 vergleicht die berichtete Rechnung (R 4.3.3, blinde zweite Instanz, Spezifikation vom 24.09.2026 im Stand Nachtrag 2) je Kennung mit der Gegenprobe (Python) über denselben eingefrorenen Datenstand `Datenstand_2026-09-24`. Der Abgleich lief mit dem neutralen Skript `Abgleich_2026-09-25.R` der zweiten Instanz und den Toleranzen der Spezifikation Teil G.3.

**Ergebnis: bestanden.** Alle 3 559 ausgeschriebenen Kennungen (1 535 Muster der Anlage) stimmen innerhalb der Toleranzen überein, keine Kennung steht nur in einer Datei, alle 134 fehlenden Werte fehlen beidseitig mit demselben Grund. Die Ergebnisdatei der zweiten Instanz kann in Phase 7 als Zahlenquelle des Manuskripts dienen, sobald der Verfasser die Freigabe F2 nach 6.2 bis 6.4 gibt.

*Tab. 1.* Urteile je Toleranzklasse (Abgleich_2026-09-25_Protokoll.txt)

| Klasse | Kennungen | bestanden | Abweichung | nachrichtlich | Toleranz (G.3) |
|---|---:|---:|---:|---:|---|
| EXAKT (Anzahlen, Merkmale, Setzugehörigkeiten) | 1 801 | 1 801 | 0 | 0 | exakt gleich |
| DETERM (deterministische Rechnungen) | 1 714 | 1 714 | 0 | 0 | \|a − b\| ≤ 1e-9 · max(1, \|a\|) |
| ITERATIV (S18 MDES, MDESR, POW, S14 SWP) | 23 | 23 | 0 | 0 | relativ 1e-6 |
| ZUFALL (S19 BKIU, BKIO) | 6 | 6 | 0 | 0 | 3 · √(MC-SE_1² + MC-SE_2²) |
| NACHRICHT (S19 BSD, BMCU, BMCO, BNGUELT, BNVERW) | 15 | – | – | 15 | nur berichtet |
| **Summe** | **3 559** | **3 544** | **0** | **15** | |

Je Schritt S01 bis S19: 0 Abweichungen. Größte relative Abweichung einer bestandenen deterministischen Kennung: 2,7e-10 (S14.SWW.CM.PRE.BPAHIG.X, Shapiro-Wilk-W aus zwei Implementierungen des Algorithmus AS R94). Iterative Größen: Shapiro-Wilk-p bis 9,5e-9 relativ, MDES und Power bis 8e-10 relativ, also auch unter der deterministischen Toleranz. Bootstrap-Grenzen: Abweichung zwischen 2 und 81 Prozent der zulässigen Toleranz (Generatoren Mersenne-Twister in R und PCG64 in numpy, nach S19 Regel 6 zulässig). Nachrichtlich: Bootstrap-SD der b1* auf 0,4 bis 1,7 Prozent gleich, Monte-Carlo-Fehler der Grenzen um 9 bis 38 Prozent verschieden (Schätzungen aus je 20 Blöcken, erwartbar), 10 000 gültige und 0 verworfene Ziehungen auf beiden Seiten.

## 2 Unversehrtheit der Abgabe

Prüfung mit `sha256sum` im Container gegen `Pruefsummen_Abgabe_2026-09-25.txt` (100 Dateien) und gegen `Datenstand_2026-09-24\Pruefsummen.txt` (6 Dateien).

- Datenstand: 6 von 6 Prüfsummen stimmen. Die Anlagen der Spezifikation und die Sollprüfsummen in `Funktionen_2026-09-25.R` stimmen mit dem Projektordner `02_Befunde` überein (Kennungsanlage und Spezifikation byteidentisch).
- Abgabe: 94 von 100 Prüfsummen stimmen exakt, darunter die Ergebnisdatei (`3194a805…`), das Laufprotokoll (`f25d57b3…`), alle Skripte, alle Textausgaben und alle Zwischendateien.
- Die sechs PNG-Grafiken (`S14_QQ_*`, `S14_Linearitaet_*`) weichen ab. Ursache: Beim Übertragen aus dem Container der zweiten Instanz auf den Rechner hat die Dateiablage („Anthropic Files“, Content Credentials nach C2PA) in jede PNG einen Metadatenblock `caBX` von 5 770 Bytes eingefügt. Nach Entfernen dieses Blocks stimmen alle sechs Prüfsummen mit der Liste überein. Die Bilddaten (IHDR, IDAT) sind unverändert. Die Grafiken tragen keine Kennung (G.1 Nr. 6), der Befund berührt keinen Wert.

## 3 Die Gegenprobe: Python-Kette in neuer Fassung

Der Code-Stand vom 12.09.2026 (`Auswertung_B0` bis `B9`, `F1`) liest das Workbook statt des Datenstands, kennt weder die Schrittfolge S01 bis S19 noch die Kennungen, rechnet Größen, die mit Nachtrag 2 entfallen sind, und weicht in Einzelregeln von den Festlegungen vom 24.09. ab (J mit df = n − 4, zentrierte Kovariaten, Poweranalyse mit R²). Umfang und Kennungen waren also nicht angepasst. Die Gegenprobe wurde deshalb als neue, datierte Fassung geschrieben (Auswertungsverfahren 3.4): `03_Skripte\Gegenprobe_Python_2026-09-25.py`. Sie übernimmt die Rechenlogik der Kette (numpy, scipy: Kleinste Quadrate, Shapiro-Wilk, Brown-Forsythe, χ²-Intervall des TE, Fragebogenregeln) und setzt die Spezifikation Schritt für Schritt um, einschließlich der Festlegungen aus der Blindrechnung vom 25.09. (Antworten R1 bis R5, Anmerkungen A1 bis A13 des Rückfragenprotokolls), der Referenztests R01 bis R13 mit dem Nachtrag Toleranz R08 und der Ausgabe nach G.1.

*Tab. 2.* Läufe und Prüfsummen

| Datei | Fassung | SHA-256 | Inhalt |
|---|---|---|---|
| Gegenprobe_Python_2026-09-25.py | 1 (25.09., 10:07 UTC) | 943a4553fd7dfea4a3ce902a27d9e0f3754c308676d7bceed3e1eb5306e841ea | erste Fassung, Abgleich bestanden |
| Gegenprobe_Python_2026-09-25.py | 2 (25.09., 10:27 UTC) | 2959ab0c30087bd0a19bfdf4df96ef76877c964cd2473ed42e1e2fb65f2bc189 | nach der Durchsicht 6.2 (Befunde 1, 2, 4, 5, 7, 8, 13), ergebnisneutral, Abgleich wiederholt |
| Ergebnisse_Python_2026-09-25.csv | aus Fassung 1 und 2 | 2d4ce431b64bc209fa71a5f4615dbf828dce4b1eda7967952f75cfb26ec35099 | 3 559 Zeilen, 3 425 mit Wert, 134 fehlend (Eingang fehlt 22, Fallzahlregel 14, nicht erhebbar 3, zu wenige Werte 95), byteidentisch aus beiden Fassungen |
| Ergebnisse_R_2026-09-25.csv | zweite Instanz | 3194a805dc3e2c4bf0142ecab5f091d9e201449f3f2811b78073b406c74392a8 | 3 559 Zeilen, dieselben Anzahlen fehlender Werte je Grund |
| Abgleich_2026-09-25.R | zweite Instanz | eaa40e7f05ce7b1f7870f00144c7f112af16d1dfa4a69ea1c4f8b8a4beb63858 | neutrales Abgleichskript |
| Abgleich_2026-09-25.csv | Lauf 2 (Fassung 2) | a49a9e8cb2fa213a50425c7d8f8ae7c7bea21bee52a23df08f0d60e08bda51ea | Urteil je Kennung |
| Abgleich_2026-09-25_Protokoll.txt | Lauf 2 (Fassung 2) | 76452204c5500987c8599feb1ddea13b36b467cf3ad3cfc9a13ac537d9e16c70 | Zusammenfassung je Klasse und Schritt |

Rechenumgebung der Gegenprobe: Python 3.11.15, numpy 2.4.4, scipy 1.17.1, matplotlib 3.10.9 (Ubuntu 24.04, Container). Abgleichskript ausgeführt mit R 4.3.3 (r-base-core 4.3.3-2build2 aus den Ubuntu-Paketquellen), derselben Fassung wie bei der zweiten Instanz. Einzelheiten in `03_Skripte\Umgebung_2026-09-25.txt`.

Validierung der Gegenprobe vor der Studienrechnung (Phase 4): Referenztests 83 von 83 Sollwerten bestanden (R08 mit dem Nachtrag Toleranz vom 25.09., W 1e-5 und F 1e-4), in Fassung 2 zusätzlich R03 über den S15-Rechenweg (gepoolte SD, t²), Grenzfälle 39 von 39 bestanden (Quantil Typ 7, Auslöseprüfung, Interpolation, Kalenderregel, Paarbildung, Wochendeckel, Fallzahlregel, Rangdefekt, TE, Überlappung, Brown-Forsythe von Hand). Für die Stellengenauigkeit von R03 (AtmWtAg, 9 Stellen) rechnen Mittel und Quadratsummen um den ersten Wert verschoben, wie bei der zweiten Instanz (Anmerkung A12).

## 4 Festlegungen aus der Blindrechnung, auf beiden Seiten gleich umgesetzt

| Nr. | Festlegung (25.09.2026) | Umsetzung R | Umsetzung Python |
|---|---|---|---|
| 1 | R1: SESOI post intern aus den BEST post für S11 (Lesart a) | Schalter LESART_R1 in S11 | Dictionary SESOI_POST ohne Kennung |
| 2 | R2: Zuordnung der acht Gründe | Konstanten GRUND_* | Konstanten G_* mit Prüfung in `setze` |
| 3 | R3: Sammelmeldungspaar = Komplement des Dublettenpaars, jedes Paar gezählt | `paare_zaehlen` | Funktion `paare`, Grenzfall geprüft |
| 4 | R4: Fallzahlregel in BPAH für beide Vorab-Prüfungen (Lesart a) | Schalter LESART_R4 | `inf(bpah)` vor Prä-Modell und Shapiro-Wilk |
| 5 | R5: Toleranz R08 W 1e-5, F 1e-4 | NACHTRAEGE_TOLERANZ | Tabelle NACHTRAG in `referenztests` |
| 6 | A1, A5, A7, A8, A9, A10, A11 | Skripte S01, S06, S07, S08, S13 bis S17 | S01 (A9), S06 (A5, A8), S08 (A7), `b1_ausgabe` (A10), S14 (A1, A11) |

## 5 Abweichungen und Klärungen

Es gab keine Abweichung außerhalb der Toleranzen, also keinen Austausch mit der zweiten Instanz über einzelne Kennungen und keine Korrektur einer Rechnung. Die Blindheit der zweiten Instanz bleibt gewahrt. Zwei Lesartenunterschiede ohne Wirkung im Datenstand hat die Durchsicht 6.2 gefunden (Vorrang der Gründe in S05, Rangkriterium der QR-Zerlegung), sie stehen im Durchsichtsprotokoll mit dem Vorschlag eines Nachtrags 3.

## 6 Unabhängigkeit, Grenzen

- Die Gegenprobe wurde geschrieben, bevor die R-Skripte S01 bis S19 und die Werte der R-Ergebnisdatei gelesen wurden. Vorher gelesen: Spezifikation und Anlagen, Rückfragenprotokoll, Laufprotokoll (Prüfsummen, Zahl der fehlenden Werte je Grund), Abgleichskript, Prüfsummenskript und der SHA-256-Teil der Funktionsbibliothek (zur Klärung der PNG-Abweichung). Die R-Rechenskripte und die Werte wurden erst nach dem bestandenen Abgleich für die Durchsicht 6.2 geöffnet.
- Beide Implementierungen stammen von Claude-Instanzen, die Unabhängigkeit betrifft den Informationszugang (Blindheit der zweiten Instanz), nicht die Autorenschaft. Eine gemeinsame Fehllesung der Spezifikation würde der Abgleich nicht aufdecken. Dagegen stehen die Referenztests mit veröffentlichten Sollwerten, die Grenzfälle mit Sollwerten von Hand, die Handprobe des Verfassers (6.3) und die Plausibilitätsprüfung (6.4). Die unabhängige Durchsicht des Python-Skripts (6.2) fand keinen kritischen Befund.
- Das Abgleichskript ordnet S18 POW der iterativen Klasse zu (Skriptkopf). Die Werte stimmen so genau überein, dass sie auch die deterministische Toleranz einhalten. Eine Änderung der Zuordnung ist nicht nötig.

## 7 Dateien dieser Phase

- `02_Befunde\Abgleich_2026-09-25.csv`, `Abgleich_2026-09-25_Protokoll.txt` (Ausgabe des neutralen Skripts, Lauf 2), dieses Protokoll (.md, .docx, .pdf)
- `03_Skripte\Gegenprobe_Python_2026-09-25.py` (Fassung 2), `Gegenprobe_Python_2026-09-25.txt` (Laufprotokoll mit Referenztests, Grenzfällen, Prüfsummen), `Ergebnisse_Python_2026-09-25.csv`, `S14_QQ_<ZIEL>_Python.png`, `S14_Linearitaet_<ZIEL>_Python.png`
- `03_Skripte\Umgebung_2026-09-25.txt` (L4)
- `_Archiv\Gegenprobe_Python_2026-09-25_Fassung1.py` (Fassung 1, nur zur Nachvollziehbarkeit)

## 8 Nächste Schritte

6.2 Durchsichtsprotokoll (liegt vor) · 6.3 Handprobe durch den Verfasser (`04_Uebergaben\Handprobe_2026-09-25.xlsx`) · 6.4 Plausibilitätsprotokoll (liegt vor, mit dem Befund zur %PAH-Regel) · Freigabe F2 durch den Verfasser · danach Phase 7 (Kennzahlenblatt aus der Ergebnisdatei, Objekte per R-Skript, Endabgleich Manuskript).

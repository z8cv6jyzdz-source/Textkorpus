# Kennzahlenblatt — Bachelorarbeit U15-Plyometrie

**Erzeugt am 25.09.2026 aus der Ergebnisdatei der berichteten Rechnung (Phase 7.1) · Datenstand 2026-09-24 (eingefroren) · Freigabe F2: Verfasser, 25.09.2026 · Rev. 2 vom 25.09.2026: K-01.24 (Clusterebene, angefragte Vereine) ergänzt**

Einzige Zahlenquelle für den Manuskripttext. Jede Zahl im Manuskript trägt eine Kennung K-xx.y aus diesem Blatt. Jede Zeile nennt daneben die Kennung der Ergebnisdatei (Spezifikation 0.3), aus der der Wert stammt. Zahlen aus Projektanweisungen, Sitzungsnotizen, Befund- oder Übergabedokumenten und aus dem Kennzahlenblatt vom 22.09.2026 werden nicht verwendet, das sind Abschriften oder überholte Stände (Register R11).

Quelle: `Blindrechnung_R_2026-09-24\Abgabe_R_2026-09-25\Ergebnisse_R_2026-09-25.csv` (R 4.3.3, blinde zweite Instanz, SHA-256 `3194a805dc3e2c4bf0142ecab5f091d9e201449f3f2811b78073b406c74392a8`), Kopie in `Claude\03_Skripte\Abgabe_R_2026-09-25`. Abgleich mit der Gegenprobe (Python) je Kennung bestanden (Abgleichprotokoll_2026-09-25). Erzeuger: `Claude\03_Skripte\Kennzahlen_2026-09-25.py`. Bei neuem Datenstand oder neuem Lauf beider Ketten das Skript erneut laufen lassen, nie eine Zahl hier von Hand ändern. Anlage `Kennzahlen_2026-09-25_Werte.csv`: jede Zeile dieses Blatts mit ungerundetem Wert und Berichtsort (T Text, A Anhang, I intern nach dem Umfangsdokument).

**Darstellungsregeln (Umfangsdokument § 3.7):** Zeiten M ± SD mit zwei Nachkommastellen, Differenzen, Konfidenzgrenzen, TE und SESOI mit drei · Standweitsprung M ± SD ganzzahlig, Differenzen und Grenzen mit einer Nachkommastelle · d und g mit zwei, p mit drei Nachkommastellen, darunter „< 0,001“, CV mit einer · Konfidenzintervalle als Spanne mit „bis“ · Vorzeichen bei Differenzen und Grenzen immer, Differenz IG minus KG, bei Zeiten bedeuten negative Werte eine schnellere IG.

**Bezugsmengen-Regel (Verfasser 22.09.2026, unverändert):** (1) *Zur Eingangstestung angetreten* (K-01.1 bis K-01.8) steht nur im Teilnehmerfluss (Abb. 1) und in genau einem Satz daneben in 5.1. Die Methodik nennt keine Spielerzahlen dieser Menge, 4.1 nennt die Zuteilung auf Vereinsebene. (2) *Analysepopulation* (K-01.14, K-01.16, Menge ANA der Spezifikation: im ITT-Set mindestens einer Zielgröße) ist die Stichprobe des Manuskripts: 4.2, Tab. 2 oben (K-02), Nenner je Zielgröße in Tab. 2 unten und Tab. 3 (K-04, K-06). (3) *Status ausgewertet* (K-01.10, zur Post-Testung angetreten) ist nur ein Zwischenschritt von Abb. 1. Jede Zahl im Text nennt ihre Bezugsmenge, K-02 gilt nur für die Analysepopulation.

**Programmzahlen** (Kontakte, Anteile, Wochen) stehen nicht hier, sondern in `Claude\03_Skripte\Programmkennzahlen_2026-09-23.txt` (P-01 bis P-12).

## K-01 Teilnehmerfluss und Fallzahlen (Abb. 1, ein Satz in 5.1, Box 6 in 4.7)

| Kennung | Größe | Wert | Bezugsmenge | Kennung der Ergebnisdatei |
|---|---|---|---|---|
| K-01.1 | N zugeteilt und eingangsgetestet | 31 | alle Spieler der Personendaten (jeder mit Prätestdaten, K-01.8) | S01.N.X.X.ALL.X |
| K-01.2 | n Interventionsgruppe | 18 | zugeteilt (S01 und Teilnehmerfluss S08 gleich) | S01.N.X.X.IG.X, S08.FLZUG.X.X.IG.X |
| K-01.3 | n Kontrollgruppe | 13 | zugeteilt (S01 und Teilnehmerfluss S08 gleich) | S01.N.X.X.KG.X, S08.FLZUG.X.X.KG.X |
| K-01.4 | n Verein A (Hohenlind) | 7 | zugeteilt (S01 und Teilnehmerfluss S08 gleich) | S01.N.X.X.VA.X, S08.FLZUG.X.X.VA.X |
| K-01.5 | n Verein B (Blau-Weiß) | 11 | zugeteilt (S01 und Teilnehmerfluss S08 gleich) | S01.N.X.X.VB.X, S08.FLZUG.X.X.VB.X |
| K-01.6 | n Verein C (Vorwärts Spoho) | 13 | zugeteilt (S01 und Teilnehmerfluss S08 gleich) | S01.N.X.X.VC.X, S08.FLZUG.X.X.VC.X |
| K-01.7 | Zuteilungsverhältnis IG : KG (Spielerebene, abgeleitet) | 1,38 : 1 | keine Textverwendung (Verfasser 22.09.), auf Vereinsebene 2 : 1 | S01.N.X.X.IG.X, S01.N.X.X.KG.X |
| K-01.8 | mit Prätestdaten (mindestens ein gültiger Prä-Versuch) | IG 18 · KG 13 (A 7 · B 11 · C 13) | zugeteilt | S08.FLPRE.X.X.IG.X, S08.FLPRE.X.X.KG.X, S08.FLPRE.X.X.VA.X, S08.FLPRE.X.X.VB.X, S08.FLPRE.X.X.VC.X |
| K-01.9 | Post-Testung nicht angetreten | IG 2 · KG 2 (A 0 · B 2 · C 2) | zugeteilt (Codes in K-12) | S08.FLNANG.X.X.IG.X, S08.FLNANG.X.X.KG.X, S08.FLNANG.X.X.VA.X, S08.FLNANG.X.X.VB.X, S08.FLNANG.X.X.VC.X |
| K-01.10 | Status ausgewertet (zur Post-Testung angetreten) | IG 16 · KG 11 (A 7 · B 9 · C 11) | zugeteilt | S08.FLAUSG.X.X.IG.X, S08.FLAUSG.X.X.KG.X, S08.FLAUSG.X.X.VA.X, S08.FLAUSG.X.X.VB.X, S08.FLAUSG.X.X.VC.X |
| K-01.11 | ohne %PAH (fehlende Anthropometrie, K2) | IG 0 · KG 1 | zugeteilt (Codes in K-12) | S08.FLOPAH.PAH.X.IG.X, S08.FLOPAH.PAH.X.KG.X |
| K-01.12 | Familiarisierung IG | 10× ein Termin, 8× zwei, 0 ohne Angabe | zugeteilt | S12.NFAM1.FAM.PRE.IG.X, S12.NFAM2.FAM.PRE.IG.X, S12.NFAMNA.FAM.PRE.IG.X |
| K-01.13 | Familiarisierung KG | 0× ein Termin, 13× zwei, 0 ohne Angabe | zugeteilt | S12.NFAM1.FAM.PRE.KG.X, S12.NFAM2.FAM.PRE.KG.X, S12.NFAMNA.FAM.PRE.KG.X |
| K-01.14 | Analysepopulation ANA (im ITT-Set mindestens einer Zielgröße) | IG 16 · KG 10 = 26 | Stichprobe des Manuskripts, Nenner je Zielgröße in K-04 und K-06 | S12.N.AGE.PRE.ANAIG.X, S12.N.AGE.PRE.ANAKG.X |
| K-01.15 | nicht in der Analysepopulation (abgeleitet aus den ITT-Mitgliedschaften) | 5: BW-07, BW-21, VS-07, VS-16, VS-18 | Post-Testung nicht angetreten oder ohne %PAH (Gründe je Spieler in K-12) | S08.MITGL.{Ziel}.X.P<Code>.ITT |
| K-01.16 | Analysepopulation je Verein (abgeleitet, Codepräfix HL = A, BW = B, VS = C) | A 7 · B 9 · C 10 | Bezugsmenge K-01.14, für 4.2 | S08.MITGL.{Ziel}.X.P<Code>.ITT |
| K-01.17 | Intervention erhalten (IG, mindestens eine vollständig gemeldete Einheit, CONSORT 13a) | 14 | zugeteilte IG-Spieler | S07.GE01.ADH.X.IG.GANZ |
| K-01.24 | Vereine (Clusterebene von Abb. 1, Angabe des Verfassers 25.09.2026, Zuteilung auf Vereinsebene vor der Eingangstestung) | angefragt 4 · zugesagt 3 (A, B, C) · ohne Zusage 1 | angefragte Vereine | nicht aus der Ergebnisdatei |

**Box 6 nach CONSORT (K-01.18 bis K-01.22, je Gruppe gezählt, nicht exklusiv, 4.7):**

| Kennung | Klasse | Wert | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-01.18 | Nichteinhaltung (IG mit GANZ < 6, einschließlich 0) | IG 7 | S08.B6NE.X.X.IG.X |
| K-01.19 | davon ohne jede Meldung | IG 2 | S08.B6NEKM.X.X.IG.X |
| K-01.20 | Instrumentenfehler (kein Listenplatz) | IG 1 | S08.B6IF.X.X.IG.X |
| K-01.21 | fehlende Kovariate %PAH | IG 0 · KG 1 | S08.B6FK.X.X.IG.X, S08.B6FK.X.X.KG.X |
| K-01.22 | nicht angetreten | IG 2 · KG 2 | S08.B6NA.X.X.IG.X, S08.B6NA.X.X.KG.X |

**Erhebungs- und Attritionsanteile (K-01.23, Spieler mit BEST prä und post je zugeteiltem Spieler, 6.3 TESTEX 6):**

| Kennung | Zielgröße | IG | KG | gesamt | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|
| K-01.23 | Sprint 5 m | 88,9 % | 53,8 % | 74,2 % | S08.ANT.Z05.X.IG.X, S08.ANT.Z05.X.KG.X, S08.ANT.Z05.X.ALL.X |
| K-01.23 | Sprint 10 m | 38,9 % | 84,6 % | 58,1 % | S08.ANT.Z10.X.IG.X, S08.ANT.Z10.X.KG.X, S08.ANT.Z10.X.ALL.X |
| K-01.23 | Sprint 30 m | 88,9 % | 84,6 % | 87,1 % | S08.ANT.Z30.X.IG.X, S08.ANT.Z30.X.KG.X, S08.ANT.Z30.X.ALL.X |
| K-01.23 | 505 links | 83,3 % | 84,6 % | 83,9 % | S08.ANT.CL.X.IG.X, S08.ANT.CL.X.KG.X, S08.ANT.CL.X.ALL.X |
| K-01.23 | 505 rechts | 77,8 % | 76,9 % | 77,4 % | S08.ANT.CR.X.IG.X, S08.ANT.CR.X.KG.X, S08.ANT.CR.X.ALL.X |
| K-01.23 | 505-Seitenmittel | 72,2 % | 76,9 % | 74,2 % | S08.ANT.CM.X.IG.X, S08.ANT.CM.X.KG.X, S08.ANT.CM.X.ALL.X |
| K-01.23 | Standweitsprung | 88,9 % | 84,6 % | 87,1 % | S08.ANT.SBJ.X.IG.X, S08.ANT.SBJ.X.KG.X, S08.ANT.SBJ.X.ALL.X |
| K-01.23 | Teilnehmerebene (Status ausgewertet je zugeteilt) | 88,9 % | 84,6 % | 87,1 % | S08.ANTTN.X.X.IG.X, S08.ANTTN.X.X.KG.X, S08.ANTTN.X.X.ALL.X |

## K-02 Stichprobe der Analysepopulation (Tab. 2 oben, 4.2)

Bezugsmenge K-01.14 (Menge ANA). Prä-Werte. Keine Signifikanztests (CONSORT Item 15).

| Kennung | Merkmal | Interventionsgruppe | Kontrollgruppe | Kennung der Ergebnisdatei |
|---|---|---|---|---|
| K-02.1 | Alter (Jahre) | 15,10 ± 0,26 (n = 16) | 14,08 ± 0,31 (n = 10) | S12.N.AGE.PRE.ANAIG.X, S12.M.AGE.PRE.ANAIG.X, S12.SD.AGE.PRE.ANAIG.X, S12.N.AGE.PRE.ANAKG.X, S12.M.AGE.PRE.ANAKG.X, S12.SD.AGE.PRE.ANAKG.X |
| K-02.2 | Körperhöhe (cm) | 173,9 ± 10,7 (n = 16) | 168,7 ± 6,6 (n = 10) | S12.N.HGT.PRE.ANAIG.X, S12.M.HGT.PRE.ANAIG.X, S12.SD.HGT.PRE.ANAIG.X, S12.N.HGT.PRE.ANAKG.X, S12.M.HGT.PRE.ANAKG.X, S12.SD.HGT.PRE.ANAKG.X |
| K-02.3 | Körpermasse (kg) | 60,8 ± 10,1 (n = 16) | 53,3 ± 7,5 (n = 10) | S12.N.MASS.PRE.ANAIG.X, S12.M.MASS.PRE.ANAIG.X, S12.SD.MASS.PRE.ANAIG.X, S12.N.MASS.PRE.ANAKG.X, S12.M.MASS.PRE.ANAKG.X, S12.SD.MASS.PRE.ANAKG.X |
| K-02.4 | %PAH | 94,74 ± 2,77 (n = 16) | 90,50 ± 2,73 (n = 10) | S12.N.PAH.PRE.ANAIG.X, S12.M.PAH.PRE.ANAIG.X, S12.SD.PAH.PRE.ANAIG.X, S12.N.PAH.PRE.ANAKG.X, S12.M.PAH.PRE.ANAKG.X, S12.SD.PAH.PRE.ANAKG.X |
| K-02.5 | Geburtsjahrgang (Studienmerkmal, nicht in der Ergebnisdatei) | 2011 | 2012 | Studiensteckbrief, Mannschaftsjahrgang |

Alters- und Wertespannen (Minimum, Maximum) werden nicht mehr berichtet (Nachtrag 2, N4.11). Die Überlappung der Kovariaten je Analyseset steht in K-04.

## K-03 Termine und Prä-Post-Intervalle (4.3, Abb. H7)

Nicht Teil der Ergebnisdatei (der Datenstand enthält keine Testdaten). Übernommen aus dem Workbook `Statistik\Studiendaten_U15_gesamt.xlsx`, Blatt `01_Personen`, wie im Kennzahlenblatt vom 22.09.2026 (K-03). Intervalle im Skript aus den Daten berechnet.

| Kennung | Verein | Prä | Post | Intervall |
|---|---|---|---|---|
| K-03.1 | Verein A (Hohenlind) | 02.07.2026 | 10.09.2026 | 70 Tage = 10,0 Wochen |
| K-03.2 | Verein B (Blau-Weiß Köln) | 14.07.2026 | 01.09.2026 | 49 Tage = 7,0 Wochen |
| K-03.3 | Verein C (Vorwärts Spoho) | 13.07.2026 | 14.09.2026 | 63 Tage = 9,0 Wochen |

Spanne der Intervalle über die drei Vereine (K-03.4): 7,0 bis 10,0 Wochen. Intervention 20.07. bis 30.08.2026 (Programmwochen W1 bis W6, Konstanten der Spezifikation).

## K-04 Ausgangswerte je Zielgröße (Tab. 2 unten, Tab. H3)

**K-04.1 bis K-04.7 im Analyseset je Zielgröße (ITT: BEST prä, BEST post und %PAH vorhanden). d = (M_IG − M_KG) / SD_pool ohne J, nur deskriptiv. Überlappung nach S12 Regel 2 (Zahl der Spieler im gemeinsamen Bereich von Ausgangswert und %PAH, nur konfirmatorische Zielgrößen).**

| Kennung | Zielgröße | n IG | M ± SD IG | n KG | M ± SD KG | d | Überlappung | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|
| K-04.1 | Sprint 5 m (s) | 16 | 1,05 ± 0,08 | 7 | 1,13 ± 0,04 | −1,15 | – | S08.N.Z05.X.ITTIG.X, S12.N.Z05.PRE.ITTIG.HAUPT, S12.M.Z05.PRE.ITTIG.HAUPT, S12.SD.Z05.PRE.ITTIG.HAUPT, S08.N.Z05.X.ITTKG.X, S12.N.Z05.PRE.ITTKG.HAUPT, S12.M.Z05.PRE.ITTKG.HAUPT, S12.SD.Z05.PRE.ITTKG.HAUPT, S12.D.Z05.PRE.ITT.HAUPT |
| K-04.2 | Sprint 10 m (s) | 7 | 1,77 ± 0,08 | 10 | 1,95 ± 0,08 | −2,23 | – | S08.N.Z10.X.ITTIG.X, S12.N.Z10.PRE.ITTIG.HAUPT, S12.M.Z10.PRE.ITTIG.HAUPT, S12.SD.Z10.PRE.ITTIG.HAUPT, S08.N.Z10.X.ITTKG.X, S12.N.Z10.PRE.ITTKG.HAUPT, S12.M.Z10.PRE.ITTKG.HAUPT, S12.SD.Z10.PRE.ITTKG.HAUPT, S12.D.Z10.PRE.ITT.HAUPT |
| K-04.3 | Sprint 30 m (s) | 16 | 4,51 ± 0,21 | 10 | 4,89 ± 0,27 | −1,64 | Prä IG 12, KG 4 · %PAH IG 7, KG 9 | S08.N.Z30.X.ITTIG.X, S12.N.Z30.PRE.ITTIG.HAUPT, S12.M.Z30.PRE.ITTIG.HAUPT, S12.SD.Z30.PRE.ITTIG.HAUPT, S08.N.Z30.X.ITTKG.X, S12.N.Z30.PRE.ITTKG.HAUPT, S12.M.Z30.PRE.ITTKG.HAUPT, S12.SD.Z30.PRE.ITTKG.HAUPT, S12.D.Z30.PRE.ITT.HAUPT, S14.OVPREIG.Z30.X.ITT.HAUPT, S14.OVPREKG.Z30.X.ITT.HAUPT, S14.OVPAHIG.Z30.X.ITT.HAUPT, S14.OVPAHKG.Z30.X.ITT.HAUPT |
| K-04.4 | 505 links (s) | 15 | 2,45 ± 0,09 | 10 | 2,54 ± 0,12 | −0,83 | – | S08.N.CL.X.ITTIG.X, S12.N.CL.PRE.ITTIG.HAUPT, S12.M.CL.PRE.ITTIG.HAUPT, S12.SD.CL.PRE.ITTIG.HAUPT, S08.N.CL.X.ITTKG.X, S12.N.CL.PRE.ITTKG.HAUPT, S12.M.CL.PRE.ITTKG.HAUPT, S12.SD.CL.PRE.ITTKG.HAUPT, S12.D.CL.PRE.ITT.HAUPT |
| K-04.5 | 505 rechts (s) | 14 | 2,47 ± 0,12 | 10 | 2,51 ± 0,13 | −0,30 | – | S08.N.CR.X.ITTIG.X, S12.N.CR.PRE.ITTIG.HAUPT, S12.M.CR.PRE.ITTIG.HAUPT, S12.SD.CR.PRE.ITTIG.HAUPT, S08.N.CR.X.ITTKG.X, S12.N.CR.PRE.ITTKG.HAUPT, S12.M.CR.PRE.ITTKG.HAUPT, S12.SD.CR.PRE.ITTKG.HAUPT, S12.D.CR.PRE.ITT.HAUPT |
| K-04.6 | 505-Seitenmittel (s) | 13 | 2,46 ± 0,09 | 10 | 2,53 ± 0,11 | −0,69 | Prä IG 12, KG 6 · %PAH IG 5, KG 9 | S08.N.CM.X.ITTIG.X, S12.N.CM.PRE.ITTIG.HAUPT, S12.M.CM.PRE.ITTIG.HAUPT, S12.SD.CM.PRE.ITTIG.HAUPT, S08.N.CM.X.ITTKG.X, S12.N.CM.PRE.ITTKG.HAUPT, S12.M.CM.PRE.ITTKG.HAUPT, S12.SD.CM.PRE.ITTKG.HAUPT, S12.D.CM.PRE.ITT.HAUPT, S14.OVPREIG.CM.X.ITT.HAUPT, S14.OVPREKG.CM.X.ITT.HAUPT, S14.OVPAHIG.CM.X.ITT.HAUPT, S14.OVPAHKG.CM.X.ITT.HAUPT |
| K-04.7 | Standweitsprung (cm) | 16 | 238 ± 13 | 10 | 226 ± 21 | +0,70 | Prä IG 16, KG 6 · %PAH IG 7, KG 9 | S08.N.SBJ.X.ITTIG.X, S12.N.SBJ.PRE.ITTIG.HAUPT, S12.M.SBJ.PRE.ITTIG.HAUPT, S12.SD.SBJ.PRE.ITTIG.HAUPT, S08.N.SBJ.X.ITTKG.X, S12.N.SBJ.PRE.ITTKG.HAUPT, S12.M.SBJ.PRE.ITTKG.HAUPT, S12.SD.SBJ.PRE.ITTKG.HAUPT, S12.D.SBJ.PRE.ITT.HAUPT, S14.OVPREIG.SBJ.X.ITT.HAUPT, S14.OVPREKG.SBJ.X.ITT.HAUPT, S14.OVPAHIG.SBJ.X.ITT.HAUPT, S14.OVPAHKG.SBJ.X.ITT.HAUPT |

Gemeinsamer Bereich der Kovariaten (K-04.8, untere und obere Grenze, konfirmatorische Zielgrößen):

| Kennung | Zielgröße | gemeinsamer Bereich | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-04.8 | Sprint 30 m | Prä 4,450 bis 4,890 s · %PAH 87,07 bis 94,92 | S14.OVPRL.Z30.X.ITT.HAUPT, S14.OVPRU.Z30.X.ITT.HAUPT, S14.OVPAL.Z30.X.ITT.HAUPT, S14.OVPAU.Z30.X.ITT.HAUPT |
| K-04.8 | 505-Seitenmittel | Prä 2,320 bis 2,575 s · %PAH 87,07 bis 94,92 | S14.OVPRL.CM.X.ITT.HAUPT, S14.OVPRU.CM.X.ITT.HAUPT, S14.OVPAL.CM.X.ITT.HAUPT, S14.OVPAU.CM.X.ITT.HAUPT |
| K-04.8 | Standweitsprung | Prä 207,0 bis 255,0 cm · %PAH 87,07 bis 94,92 | S14.OVPRL.SBJ.X.ITT.HAUPT, S14.OVPRU.SBJ.X.ITT.HAUPT, S14.OVPAL.SBJ.X.ITT.HAUPT, S14.OVPAU.SBJ.X.ITT.HAUPT |

**K-04.9 bis K-04.15 alle eingangsgetesteten Spieler mit Bestwert prä (Menge BASE, Tab. H3, Ausfallvergleich zu Tab. 2):**

| Kennung | Zielgröße | n IG | M ± SD IG | n KG | M ± SD KG | d | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|
| K-04.9 | Sprint 5 m (s) | 18 | 1,05 ± 0,08 | 8 | 1,14 ± 0,04 | −1,22 | S12.N.Z05.PRE.IG.HAUPT, S12.M.Z05.PRE.IG.HAUPT, S12.SD.Z05.PRE.IG.HAUPT, S12.N.Z05.PRE.KG.HAUPT, S12.M.Z05.PRE.KG.HAUPT, S12.SD.Z05.PRE.KG.HAUPT, S12.D.Z05.PRE.BASE.HAUPT |
| K-04.10 | Sprint 10 m (s) | 18 | 1,85 ± 0,10 | 13 | 1,97 ± 0,08 | −1,29 | S12.N.Z10.PRE.IG.HAUPT, S12.M.Z10.PRE.IG.HAUPT, S12.SD.Z10.PRE.IG.HAUPT, S12.N.Z10.PRE.KG.HAUPT, S12.M.Z10.PRE.KG.HAUPT, S12.SD.Z10.PRE.KG.HAUPT, S12.D.Z10.PRE.BASE.HAUPT |
| K-04.11 | Sprint 30 m (s) | 18 | 4,53 ± 0,23 | 13 | 4,93 ± 0,25 | −1,68 | S12.N.Z30.PRE.IG.HAUPT, S12.M.Z30.PRE.IG.HAUPT, S12.SD.Z30.PRE.IG.HAUPT, S12.N.Z30.PRE.KG.HAUPT, S12.M.Z30.PRE.KG.HAUPT, S12.SD.Z30.PRE.KG.HAUPT, S12.D.Z30.PRE.BASE.HAUPT |
| K-04.12 | 505 links (s) | 17 | 2,47 ± 0,11 | 12 | 2,54 ± 0,11 | −0,70 | S12.N.CL.PRE.IG.HAUPT, S12.M.CL.PRE.IG.HAUPT, S12.SD.CL.PRE.IG.HAUPT, S12.N.CL.PRE.KG.HAUPT, S12.M.CL.PRE.KG.HAUPT, S12.SD.CL.PRE.KG.HAUPT, S12.D.CL.PRE.BASE.HAUPT |
| K-04.13 | 505 rechts (s) | 17 | 2,48 ± 0,11 | 12 | 2,50 ± 0,13 | −0,17 | S12.N.CR.PRE.IG.HAUPT, S12.M.CR.PRE.IG.HAUPT, S12.SD.CR.PRE.IG.HAUPT, S12.N.CR.PRE.KG.HAUPT, S12.M.CR.PRE.KG.HAUPT, S12.SD.CR.PRE.KG.HAUPT, S12.D.CR.PRE.BASE.HAUPT |
| K-04.14 | 505-Seitenmittel (s) | 16 | 2,47 ± 0,09 | 11 | 2,52 ± 0,11 | −0,60 | S12.N.CM.PRE.IG.HAUPT, S12.M.CM.PRE.IG.HAUPT, S12.SD.CM.PRE.IG.HAUPT, S12.N.CM.PRE.KG.HAUPT, S12.M.CM.PRE.KG.HAUPT, S12.SD.CM.PRE.KG.HAUPT, S12.D.CM.PRE.BASE.HAUPT |
| K-04.15 | Standweitsprung (cm) | 18 | 237 ± 13 | 13 | 224 ± 19 | +0,84 | S12.N.SBJ.PRE.IG.HAUPT, S12.M.SBJ.PRE.IG.HAUPT, S12.SD.SBJ.PRE.IG.HAUPT, S12.N.SBJ.PRE.KG.HAUPT, S12.M.SBJ.PRE.KG.HAUPT, S12.SD.SBJ.PRE.KG.HAUPT, S12.D.SBJ.PRE.BASE.HAUPT |

**K-04.16 bis K-04.19 deskriptive Zielgrößen prä und post im Analyseset (Tab. H3, nur Deskription, R5):**

| Kennung | Zielgröße | prä IG | prä KG | post IG | post KG | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|
| K-04.16 | Sprint 5 m (s) | 1,05 ± 0,08 (n = 16) | 1,13 ± 0,04 (n = 7) | 1,08 ± 0,04 (n = 16) | 1,17 ± 0,04 (n = 7) | S12.N.Z05.PRE.ITTIG.HAUPT, S12.M.Z05.PRE.ITTIG.HAUPT, S12.SD.Z05.PRE.ITTIG.HAUPT, S12.N.Z05.PRE.ITTKG.HAUPT, S12.M.Z05.PRE.ITTKG.HAUPT, S12.SD.Z05.PRE.ITTKG.HAUPT, S12.N.Z05.POST.ITTIG.HAUPT, S12.M.Z05.POST.ITTIG.HAUPT, S12.SD.Z05.POST.ITTIG.HAUPT, S12.N.Z05.POST.ITTKG.HAUPT, S12.M.Z05.POST.ITTKG.HAUPT, S12.SD.Z05.POST.ITTKG.HAUPT |
| K-04.17 | Sprint 10 m (s) | 1,77 ± 0,08 (n = 7) | 1,95 ± 0,08 (n = 10) | 1,87 ± 0,07 (n = 7) | 1,98 ± 0,08 (n = 10) | S12.N.Z10.PRE.ITTIG.HAUPT, S12.M.Z10.PRE.ITTIG.HAUPT, S12.SD.Z10.PRE.ITTIG.HAUPT, S12.N.Z10.PRE.ITTKG.HAUPT, S12.M.Z10.PRE.ITTKG.HAUPT, S12.SD.Z10.PRE.ITTKG.HAUPT, S12.N.Z10.POST.ITTIG.HAUPT, S12.M.Z10.POST.ITTIG.HAUPT, S12.SD.Z10.POST.ITTIG.HAUPT, S12.N.Z10.POST.ITTKG.HAUPT, S12.M.Z10.POST.ITTKG.HAUPT, S12.SD.Z10.POST.ITTKG.HAUPT |
| K-04.18 | 505 links (s) | 2,45 ± 0,09 (n = 15) | 2,54 ± 0,12 (n = 10) | 2,45 ± 0,08 (n = 15) | 2,51 ± 0,13 (n = 10) | S12.N.CL.PRE.ITTIG.HAUPT, S12.M.CL.PRE.ITTIG.HAUPT, S12.SD.CL.PRE.ITTIG.HAUPT, S12.N.CL.PRE.ITTKG.HAUPT, S12.M.CL.PRE.ITTKG.HAUPT, S12.SD.CL.PRE.ITTKG.HAUPT, S12.N.CL.POST.ITTIG.HAUPT, S12.M.CL.POST.ITTIG.HAUPT, S12.SD.CL.POST.ITTIG.HAUPT, S12.N.CL.POST.ITTKG.HAUPT, S12.M.CL.POST.ITTKG.HAUPT, S12.SD.CL.POST.ITTKG.HAUPT |
| K-04.19 | 505 rechts (s) | 2,47 ± 0,12 (n = 14) | 2,51 ± 0,13 (n = 10) | 2,48 ± 0,11 (n = 14) | 2,56 ± 0,12 (n = 10) | S12.N.CR.PRE.ITTIG.HAUPT, S12.M.CR.PRE.ITTIG.HAUPT, S12.SD.CR.PRE.ITTIG.HAUPT, S12.N.CR.PRE.ITTKG.HAUPT, S12.M.CR.PRE.ITTKG.HAUPT, S12.SD.CR.PRE.ITTKG.HAUPT, S12.N.CR.POST.ITTIG.HAUPT, S12.M.CR.POST.ITTIG.HAUPT, S12.SD.CR.POST.ITTIG.HAUPT, S12.N.CR.POST.ITTKG.HAUPT, S12.M.CR.POST.ITTKG.HAUPT, S12.SD.CR.POST.ITTKG.HAUPT |

## K-05 Messgüte (Tab. 1 in 4.4, Tab. H1)

TE = gepoolte Innerspieler-SD der gültigen Wiederholungsversuche der Spieler mit k ≥ 2 (O5), 95-%-KI aus χ² (K12), CV = 100 · TE / Mittel der Versuche der TE-Menge (K13), S = SD der Bestwerte prä aller Spieler (O6), SESOI = 0,2 · S, RTS = TE/SESOI, FLEINZ = 1 wenn TE > SESOI. Seitenmittel aus beidseitig gültigen Versuchsnummern (K15). Ohne MDC und ohne TE/√n (Nachtrag 2).

| Kennung | Zielgröße | n prä | TE prä [95-%-KI] | df | CV (%) | S (Zwischen-SD der Bestwerte) | SESOI | TE/SESOI | TE > SESOI | TE post [95-%-KI] | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K-05.1 | Sprint 5 m (s) | 21 | 0,046 [0,037 bis 0,063] | 27 | 4,2 | 0,079 (n = 26) | 0,016 | 2,92 | 1 | 0,040 [0,032 bis 0,051] (n = 25) | S10.NTE.Z05.PRE.ALL.X, S10.TE.Z05.PRE.ALL.X, S10.TELO.Z05.PRE.ALL.X, S10.TEHI.Z05.PRE.ALL.X, S10.DFTE.Z05.PRE.ALL.X, S10.CV.Z05.PRE.ALL.X, S10.NSB.Z05.PRE.ALL.X, S10.SB.Z05.PRE.ALL.X, S10.SESOI.Z05.PRE.ALL.X, S10.RTS.Z05.PRE.ALL.X, S10.FLEINZ.Z05.PRE.ALL.X, S10.NTE.Z05.POST.ALL.X, S10.TE.Z05.POST.ALL.X, S10.TELO.Z05.POST.ALL.X, S10.TEHI.Z05.POST.ALL.X, S10.DFTE.Z05.POST.ALL.X |
| K-05.2 | Sprint 10 m (s) | 26 | 0,037 [0,030 bis 0,048] | 36 | 1,9 | 0,107 (n = 31) | 0,021 | 1,72 | 1 | 0,050 [0,038 bis 0,073] (n = 13) | S10.NTE.Z10.PRE.ALL.X, S10.TE.Z10.PRE.ALL.X, S10.TELO.Z10.PRE.ALL.X, S10.TEHI.Z10.PRE.ALL.X, S10.DFTE.Z10.PRE.ALL.X, S10.CV.Z10.PRE.ALL.X, S10.NSB.Z10.PRE.ALL.X, S10.SB.Z10.PRE.ALL.X, S10.SESOI.Z10.PRE.ALL.X, S10.RTS.Z10.PRE.ALL.X, S10.FLEINZ.Z10.PRE.ALL.X, S10.NTE.Z10.POST.ALL.X, S10.TE.Z10.POST.ALL.X, S10.TELO.Z10.POST.ALL.X, S10.TEHI.Z10.POST.ALL.X, S10.DFTE.Z10.POST.ALL.X |
| K-05.3 | Sprint 30 m (s) | 30 | 0,077 [0,065 bis 0,097] | 47 | 1,6 | 0,313 (n = 31) | 0,063 | 1,24 | 1 | 0,090 [0,074 bis 0,116] (n = 26) | S10.NTE.Z30.PRE.ALL.X, S10.TE.Z30.PRE.ALL.X, S10.TELO.Z30.PRE.ALL.X, S10.TEHI.Z30.PRE.ALL.X, S10.DFTE.Z30.PRE.ALL.X, S10.CV.Z30.PRE.ALL.X, S10.NSB.Z30.PRE.ALL.X, S10.SB.Z30.PRE.ALL.X, S10.SESOI.Z30.PRE.ALL.X, S10.RTS.Z30.PRE.ALL.X, S10.FLEINZ.Z30.PRE.ALL.X, S10.NTE.Z30.POST.ALL.X, S10.TE.Z30.POST.ALL.X, S10.TELO.Z30.POST.ALL.X, S10.TEHI.Z30.POST.ALL.X, S10.DFTE.Z30.POST.ALL.X |
| K-05.4 | 505 links (s) | 22 | 0,089 [0,070 bis 0,122] | 26 | 3,5 | 0,114 (n = 29) | 0,023 | 3,89 | 1 | 0,053 [0,041 bis 0,076] (n = 21) | S10.NTE.CL.PRE.ALL.X, S10.TE.CL.PRE.ALL.X, S10.TELO.CL.PRE.ALL.X, S10.TEHI.CL.PRE.ALL.X, S10.DFTE.CL.PRE.ALL.X, S10.CV.CL.PRE.ALL.X, S10.NSB.CL.PRE.ALL.X, S10.SB.CL.PRE.ALL.X, S10.SESOI.CL.PRE.ALL.X, S10.RTS.CL.PRE.ALL.X, S10.FLEINZ.CL.PRE.ALL.X, S10.NTE.CL.POST.ALL.X, S10.TE.CL.POST.ALL.X, S10.TELO.CL.POST.ALL.X, S10.TEHI.CL.POST.ALL.X, S10.DFTE.CL.POST.ALL.X |
| K-05.5 | 505 rechts (s) | 26 | 0,083 [0,066 bis 0,111] | 30 | 3,3 | 0,117 (n = 29) | 0,023 | 3,55 | 1 | 0,072 [0,053 bis 0,113] (n = 14) | S10.NTE.CR.PRE.ALL.X, S10.TE.CR.PRE.ALL.X, S10.TELO.CR.PRE.ALL.X, S10.TEHI.CR.PRE.ALL.X, S10.DFTE.CR.PRE.ALL.X, S10.CV.CR.PRE.ALL.X, S10.NSB.CR.PRE.ALL.X, S10.SB.CR.PRE.ALL.X, S10.SESOI.CR.PRE.ALL.X, S10.RTS.CR.PRE.ALL.X, S10.FLEINZ.CR.PRE.ALL.X, S10.NTE.CR.POST.ALL.X, S10.TE.CR.POST.ALL.X, S10.TELO.CR.POST.ALL.X, S10.TEHI.CR.POST.ALL.X, S10.DFTE.CR.POST.ALL.X |
| K-05.6 | 505-Seitenmittel (s) | 19 | 0,055 [0,042 bis 0,078] | 21 | 2,2 | 0,100 (n = 27) | 0,020 | 2,73 | 1 | 0,041 [0,029 bis 0,067] (n = 12) | S10.NTE.CM.PRE.ALL.X, S10.TE.CM.PRE.ALL.X, S10.TELO.CM.PRE.ALL.X, S10.TEHI.CM.PRE.ALL.X, S10.DFTE.CM.PRE.ALL.X, S10.CV.CM.PRE.ALL.X, S10.NSB.CM.PRE.ALL.X, S10.SB.CM.PRE.ALL.X, S10.SESOI.CM.PRE.ALL.X, S10.RTS.CM.PRE.ALL.X, S10.FLEINZ.CM.PRE.ALL.X, S10.NTE.CM.POST.ALL.X, S10.TE.CM.POST.ALL.X, S10.TELO.CM.POST.ALL.X, S10.TEHI.CM.POST.ALL.X, S10.DFTE.CM.POST.ALL.X |
| K-05.7 | Standweitsprung (cm) | 29 | 6,1 [5,1 bis 7,8] | 41 | 2,7 | 16,6 (n = 31) | 3,3 | 1,85 | 1 | 6,7 [5,3 bis 9,2] (n = 23) | S10.NTE.SBJ.PRE.ALL.X, S10.TE.SBJ.PRE.ALL.X, S10.TELO.SBJ.PRE.ALL.X, S10.TEHI.SBJ.PRE.ALL.X, S10.DFTE.SBJ.PRE.ALL.X, S10.CV.SBJ.PRE.ALL.X, S10.NSB.SBJ.PRE.ALL.X, S10.SB.SBJ.PRE.ALL.X, S10.SESOI.SBJ.PRE.ALL.X, S10.RTS.SBJ.PRE.ALL.X, S10.FLEINZ.SBJ.PRE.ALL.X, S10.NTE.SBJ.POST.ALL.X, S10.TE.SBJ.POST.ALL.X, S10.TELO.SBJ.POST.ALL.X, S10.TEHI.SBJ.POST.ALL.X, S10.DFTE.SBJ.POST.ALL.X |

**K-05.8 TE je Verein (Tab. H1), prä und post, mit df und Zahl der Spieler der TE-Menge:**

| Kennung | Zielgröße | prä A | prä B | prä C | post A | post B | post C | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|
| K-05.8 | Sprint 5 m (s) | 0,049 (df 11, n 7) | 0,034 (df 11, n 10) | 0,061 (df 5, n 4) | 0,038 (df 13, n 7) | 0,018 (df 14, n 9) | 0,059 (df 10, n 9) | S10.TE.Z05.PRE.VA.X, S10.DFTE.Z05.PRE.VA.X, S10.NTE.Z05.PRE.VA.X, S10.TE.Z05.PRE.VB.X, S10.DFTE.Z05.PRE.VB.X, S10.NTE.Z05.PRE.VB.X, S10.TE.Z05.PRE.VC.X, S10.DFTE.Z05.PRE.VC.X, S10.NTE.Z05.PRE.VC.X, S10.TE.Z05.POST.VA.X, S10.DFTE.Z05.POST.VA.X, S10.NTE.Z05.POST.VA.X, S10.TE.Z05.POST.VB.X, S10.DFTE.Z05.POST.VB.X, S10.NTE.Z05.POST.VB.X, S10.TE.Z05.POST.VC.X, S10.DFTE.Z05.POST.VC.X, S10.NTE.Z05.POST.VC.X |
| K-05.8 | Sprint 10 m (s) | 0,038 (df 11, n 7) | 0,028 (df 17, n 11) | 0,050 (df 8, n 8) | 0,029 (df 13, n 7) | fehlend (zu wenige Werte) | 0,075 (df 7, n 6) | S10.TE.Z10.PRE.VA.X, S10.DFTE.Z10.PRE.VA.X, S10.NTE.Z10.PRE.VA.X, S10.TE.Z10.PRE.VB.X, S10.DFTE.Z10.PRE.VB.X, S10.NTE.Z10.PRE.VB.X, S10.TE.Z10.PRE.VC.X, S10.DFTE.Z10.PRE.VC.X, S10.NTE.Z10.PRE.VC.X, S10.TE.Z10.POST.VA.X, S10.DFTE.Z10.POST.VA.X, S10.NTE.Z10.POST.VA.X, S10.TE.Z10.POST.VB.X, S10.DFTE.Z10.POST.VB.X, S10.NTE.Z10.POST.VB.X, S10.TE.Z10.POST.VC.X, S10.DFTE.Z10.POST.VC.X, S10.NTE.Z10.POST.VC.X |
| K-05.8 | Sprint 30 m (s) | 0,047 (df 12, n 7) | 0,051 (df 17, n 11) | 0,108 (df 18, n 12) | 0,121 (df 11, n 7) | 0,034 (df 14, n 9) | 0,101 (df 13, n 10) | S10.TE.Z30.PRE.VA.X, S10.DFTE.Z30.PRE.VA.X, S10.NTE.Z30.PRE.VA.X, S10.TE.Z30.PRE.VB.X, S10.DFTE.Z30.PRE.VB.X, S10.NTE.Z30.PRE.VB.X, S10.TE.Z30.PRE.VC.X, S10.DFTE.Z30.PRE.VC.X, S10.NTE.Z30.PRE.VC.X, S10.TE.Z30.POST.VA.X, S10.DFTE.Z30.POST.VA.X, S10.NTE.Z30.POST.VA.X, S10.TE.Z30.POST.VB.X, S10.DFTE.Z30.POST.VB.X, S10.NTE.Z30.POST.VB.X, S10.TE.Z30.POST.VC.X, S10.DFTE.Z30.POST.VC.X, S10.NTE.Z30.POST.VC.X |
| K-05.8 | 505 links (s) | 0,106 (df 7, n 4) | 0,067 (df 9, n 9) | 0,093 (df 10, n 9) | 0,077 (df 4, n 4) | 0,056 (df 6, n 6) | 0,039 (df 11, n 11) | S10.TE.CL.PRE.VA.X, S10.DFTE.CL.PRE.VA.X, S10.NTE.CL.PRE.VA.X, S10.TE.CL.PRE.VB.X, S10.DFTE.CL.PRE.VB.X, S10.NTE.CL.PRE.VB.X, S10.TE.CL.PRE.VC.X, S10.DFTE.CL.PRE.VC.X, S10.NTE.CL.PRE.VC.X, S10.TE.CL.POST.VA.X, S10.DFTE.CL.POST.VA.X, S10.NTE.CL.POST.VA.X, S10.TE.CL.POST.VB.X, S10.DFTE.CL.POST.VB.X, S10.NTE.CL.POST.VB.X, S10.TE.CL.POST.VC.X, S10.DFTE.CL.POST.VC.X, S10.NTE.CL.POST.VC.X |
| K-05.8 | 505 rechts (s) | 0,090 (df 9, n 7) | 0,071 (df 8, n 8) | 0,084 (df 13, n 11) | 0,102 (df 3, n 3) | 0,067 (df 5, n 5) | 0,057 (df 6, n 6) | S10.TE.CR.PRE.VA.X, S10.DFTE.CR.PRE.VA.X, S10.NTE.CR.PRE.VA.X, S10.TE.CR.PRE.VB.X, S10.DFTE.CR.PRE.VB.X, S10.NTE.CR.PRE.VB.X, S10.TE.CR.PRE.VC.X, S10.DFTE.CR.PRE.VC.X, S10.NTE.CR.PRE.VC.X, S10.TE.CR.POST.VA.X, S10.DFTE.CR.POST.VA.X, S10.NTE.CR.POST.VA.X, S10.TE.CR.POST.VB.X, S10.DFTE.CR.POST.VB.X, S10.NTE.CR.POST.VB.X, S10.TE.CR.POST.VC.X, S10.DFTE.CR.POST.VC.X, S10.NTE.CR.POST.VC.X |
| K-05.8 | 505-Seitenmittel (s) | 0,047 (df 4, n 3) | 0,042 (df 8, n 8) | 0,067 (df 9, n 8) | 0,081 (df 1, n 1) | 0,028 (df 5, n 5) | 0,040 (df 6, n 6) | S10.TE.CM.PRE.VA.X, S10.DFTE.CM.PRE.VA.X, S10.NTE.CM.PRE.VA.X, S10.TE.CM.PRE.VB.X, S10.DFTE.CM.PRE.VB.X, S10.NTE.CM.PRE.VB.X, S10.TE.CM.PRE.VC.X, S10.DFTE.CM.PRE.VC.X, S10.NTE.CM.PRE.VC.X, S10.TE.CM.POST.VA.X, S10.DFTE.CM.POST.VA.X, S10.NTE.CM.POST.VA.X, S10.TE.CM.POST.VB.X, S10.DFTE.CM.POST.VB.X, S10.NTE.CM.POST.VB.X, S10.TE.CM.POST.VC.X, S10.DFTE.CM.POST.VC.X, S10.NTE.CM.POST.VC.X |
| K-05.8 | Standweitsprung (cm) | 7,1 (df 12, n 7) | 5,1 (df 15, n 11) | 6,4 (df 14, n 11) | 7,5 (df 5, n 5) | 8,1 (df 11, n 8) | 4,1 (df 10, n 10) | S10.TE.SBJ.PRE.VA.X, S10.DFTE.SBJ.PRE.VA.X, S10.NTE.SBJ.PRE.VA.X, S10.TE.SBJ.PRE.VB.X, S10.DFTE.SBJ.PRE.VB.X, S10.NTE.SBJ.PRE.VB.X, S10.TE.SBJ.PRE.VC.X, S10.DFTE.SBJ.PRE.VC.X, S10.NTE.SBJ.PRE.VC.X, S10.TE.SBJ.POST.VA.X, S10.DFTE.SBJ.POST.VA.X, S10.NTE.SBJ.POST.VA.X, S10.TE.SBJ.POST.VB.X, S10.DFTE.SBJ.POST.VB.X, S10.NTE.SBJ.POST.VB.X, S10.TE.SBJ.POST.VC.X, S10.DFTE.SBJ.POST.VC.X, S10.NTE.SBJ.POST.VC.X |

## K-06 Hauptanalyse: ANCOVA im ITT-Set (Tab. 3, 5.2, 6.1, Tab. H4)

Modell Post = b0 + b1·G + b2·Prä + b3·%PAH, G = 1 für die IG. b1 = adjustierte Gruppendifferenz im Post-Wert (IG minus KG). Unadjustierte Differenz = Differenz der Post-Mittel im selben Set (O4). g = b1 / gepoolte Prä-SD × J, KI aus dem KI von b1 (O3). Einordnung nach der Schlusslogik (Umfangsdokument § 5.1): Differenz so gepolt, dass positive Werte einen Vorteil der IG bedeuten, gegen null und SESOI (K-05) gelegt.

| Kennung | Zielgröße | n IG / KG | Post M ± SD IG | Post M ± SD KG | Differenz unadjustiert [95-%-KI] | Differenz adjustiert b1 [95-%-KI] | p | g [95-%-KI] | SESOI | Fall (Schlusslogik) | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K-06.1 | Sprint 30 m (s) | 16 / 10 | 4,57 ± 0,18 | 4,89 ± 0,23 | −0,327 [−0,497 bis −0,156] | −0,045 [−0,199 bis +0,110] | 0,557 | −0,18 [−0,83 bis +0,46] | 0,063 | C1 (kein Unterschied nachweisbar, relevante Effekte in beide Richtungen vereinbar, unschlüssig) | S13.NIG.Z30.X.ITT.HAUPT, S13.NKG.Z30.X.ITT.HAUPT, S15.MPOSTIG.Z30.X.ITT.HAUPT, S15.MPOSTKG.Z30.X.ITT.HAUPT, S15.SDPOST.Z30.X.ITT.HAUPT, S15.UD.Z30.X.ITT.HAUPT, S15.UDKIU.Z30.X.ITT.HAUPT, S15.UDKIO.Z30.X.ITT.HAUPT, S15.UDP.Z30.X.ITT.HAUPT, S13.B1.Z30.X.ITT.HAUPT, S13.KIU.Z30.X.ITT.HAUPT, S13.KIO.Z30.X.ITT.HAUPT, S13.P.Z30.X.ITT.HAUPT, S15.G.Z30.X.ITT.HAUPT, S15.GKIU.Z30.X.ITT.HAUPT, S15.GKIO.Z30.X.ITT.HAUPT, S13.SIG.Z30.X.ITT.HAUPT, S10.SESOI.Z30.PRE.ALL.X, S12.SD.Z30.POST.ITTIG.HAUPT, S12.SD.Z30.POST.ITTKG.HAUPT, S12.N.Z30.POST.ITTIG.HAUPT, S12.M.Z30.POST.ITTIG.HAUPT, S12.N.Z30.POST.ITTKG.HAUPT, S12.M.Z30.POST.ITTKG.HAUPT |
| K-06.2 | 505-Seitenmittel (s) | 13 / 10 | 2,47 ± 0,08 | 2,53 ± 0,12 | −0,060 [−0,147 bis +0,026] | −0,012 [−0,085 bis +0,061] | 0,734 | −0,11 [−0,81 bis +0,58] | 0,020 | C1 (kein Unterschied nachweisbar, relevante Effekte in beide Richtungen vereinbar, unschlüssig) | S13.NIG.CM.X.ITT.HAUPT, S13.NKG.CM.X.ITT.HAUPT, S15.MPOSTIG.CM.X.ITT.HAUPT, S15.MPOSTKG.CM.X.ITT.HAUPT, S15.SDPOST.CM.X.ITT.HAUPT, S15.UD.CM.X.ITT.HAUPT, S15.UDKIU.CM.X.ITT.HAUPT, S15.UDKIO.CM.X.ITT.HAUPT, S15.UDP.CM.X.ITT.HAUPT, S13.B1.CM.X.ITT.HAUPT, S13.KIU.CM.X.ITT.HAUPT, S13.KIO.CM.X.ITT.HAUPT, S13.P.CM.X.ITT.HAUPT, S15.G.CM.X.ITT.HAUPT, S15.GKIU.CM.X.ITT.HAUPT, S15.GKIO.CM.X.ITT.HAUPT, S13.SIG.CM.X.ITT.HAUPT, S10.SESOI.CM.PRE.ALL.X, S12.SD.CM.POST.ITTIG.HAUPT, S12.SD.CM.POST.ITTKG.HAUPT, S12.N.CM.POST.ITTIG.HAUPT, S12.M.CM.POST.ITTIG.HAUPT, S12.N.CM.POST.ITTKG.HAUPT, S12.M.CM.POST.ITTKG.HAUPT |
| K-06.3 | Standweitsprung (cm) | 16 / 10 | 233 ± 14 | 223 ± 17 | +10,1 [−2,5 bis +22,7] | −0,1 [−8,7 bis +8,6] | 0,987 | −0,00 [−0,52 bis +0,51] | 3,3 | C1 (kein Unterschied nachweisbar, relevante Effekte in beide Richtungen vereinbar, unschlüssig) | S13.NIG.SBJ.X.ITT.HAUPT, S13.NKG.SBJ.X.ITT.HAUPT, S15.MPOSTIG.SBJ.X.ITT.HAUPT, S15.MPOSTKG.SBJ.X.ITT.HAUPT, S15.SDPOST.SBJ.X.ITT.HAUPT, S15.UD.SBJ.X.ITT.HAUPT, S15.UDKIU.SBJ.X.ITT.HAUPT, S15.UDKIO.SBJ.X.ITT.HAUPT, S15.UDP.SBJ.X.ITT.HAUPT, S13.B1.SBJ.X.ITT.HAUPT, S13.KIU.SBJ.X.ITT.HAUPT, S13.KIO.SBJ.X.ITT.HAUPT, S13.P.SBJ.X.ITT.HAUPT, S15.G.SBJ.X.ITT.HAUPT, S15.GKIU.SBJ.X.ITT.HAUPT, S15.GKIO.SBJ.X.ITT.HAUPT, S13.SIG.SBJ.X.ITT.HAUPT, S10.SESOI.SBJ.PRE.ALL.X, S12.SD.SBJ.POST.ITTIG.HAUPT, S12.SD.SBJ.POST.ITTKG.HAUPT, S12.N.SBJ.POST.ITTIG.HAUPT, S12.M.SBJ.POST.ITTIG.HAUPT, S12.N.SBJ.POST.ITTKG.HAUPT, S12.M.SBJ.POST.ITTKG.HAUPT |

**K-06.4 Entscheidung nach dem Antrag (K23, P6):** H0 nicht abgelehnt (H0REJ = 0), 3 konfirmatorische Tests, SIG je Zielgröße Z30 0, CM 0, SBJ 0. Keine Adjustierung für Mehrfachtestung.

**K-06.5 Modellkennwerte und adjustierte Mittelwerte (Tab. H4):**

| Kennung | Zielgröße | b0 | b2 (Prä) | b3 (%PAH) | SE(b1) | t | df | Residuen-SD | R² | adj. Mittel IG [95-%-KI] | adj. Mittel KG [95-%-KI] | Prä-Mittel · %PAH-Mittel des Sets | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-06.5 | Sprint 30 m | 2,059 (SE 1,188) | 0,677 (SE 0,117) | −0,005 (SE 0,010) | 0,075 | −0,60 | 22 | 0,130 | 0,78 | 4,675 [4,595 bis 4,754] | 4,719 [4,610 bis 4,828] | 4,658 · 93,11 | S13.B0.Z30.X.ITT.HAUPT, S13.SEB0.Z30.X.ITT.HAUPT, S13.B2.Z30.X.ITT.HAUPT, S13.SEB2.Z30.X.ITT.HAUPT, S13.B3.Z30.X.ITT.HAUPT, S13.SEB3.Z30.X.ITT.HAUPT, S13.SEB1.Z30.X.ITT.HAUPT, S13.T.Z30.X.ITT.HAUPT, S13.DF.Z30.X.ITT.HAUPT, S13.SIGMA.Z30.X.ITT.HAUPT, S13.R2.Z30.X.ITT.HAUPT, S13.AMIG.Z30.X.ITT.HAUPT, S13.AMIGU.Z30.X.ITT.HAUPT, S13.AMIGO.Z30.X.ITT.HAUPT, S13.AMKG.Z30.X.ITT.HAUPT, S13.AMKGU.Z30.X.ITT.HAUPT, S13.AMKGO.Z30.X.ITT.HAUPT, S13.PREM.Z30.X.ITT.HAUPT, S13.PAHM.Z30.X.ITT.HAUPT |
| K-06.5 | 505-Seitenmittel | 0,529 (SE 0,724) | 0,757 (SE 0,152) | 0,001 (SE 0,005) | 0,035 | −0,34 | 19 | 0,066 | 0,63 | 2,493 [2,450 bis 2,535] | 2,505 [2,454 bis 2,555] | 2,486 · 92,93 | S13.B0.CM.X.ITT.HAUPT, S13.SEB0.CM.X.ITT.HAUPT, S13.B2.CM.X.ITT.HAUPT, S13.SEB2.CM.X.ITT.HAUPT, S13.B3.CM.X.ITT.HAUPT, S13.SEB3.CM.X.ITT.HAUPT, S13.SEB1.CM.X.ITT.HAUPT, S13.T.CM.X.ITT.HAUPT, S13.DF.CM.X.ITT.HAUPT, S13.SIGMA.CM.X.ITT.HAUPT, S13.R2.CM.X.ITT.HAUPT, S13.AMIG.CM.X.ITT.HAUPT, S13.AMIGU.CM.X.ITT.HAUPT, S13.AMIGO.CM.X.ITT.HAUPT, S13.AMKG.CM.X.ITT.HAUPT, S13.AMKGU.CM.X.ITT.HAUPT, S13.AMKGO.CM.X.ITT.HAUPT, S13.PREM.CM.X.ITT.HAUPT, S13.PAHM.CM.X.ITT.HAUPT |
| K-06.5 | Standweitsprung | 18,25 (SE 54,81) | 0,778 (SE 0,109) | 0,32 (SE 0,64) | 4,2 | −0,02 | 22 | 8,1 | 0,76 | 229 [225 bis 234] | 229 [223 bis 236] | 233,4 · 93,11 | S13.B0.SBJ.X.ITT.HAUPT, S13.SEB0.SBJ.X.ITT.HAUPT, S13.B2.SBJ.X.ITT.HAUPT, S13.SEB2.SBJ.X.ITT.HAUPT, S13.B3.SBJ.X.ITT.HAUPT, S13.SEB3.SBJ.X.ITT.HAUPT, S13.SEB1.SBJ.X.ITT.HAUPT, S13.T.SBJ.X.ITT.HAUPT, S13.DF.SBJ.X.ITT.HAUPT, S13.SIGMA.SBJ.X.ITT.HAUPT, S13.R2.SBJ.X.ITT.HAUPT, S13.AMIG.SBJ.X.ITT.HAUPT, S13.AMIGU.SBJ.X.ITT.HAUPT, S13.AMIGO.SBJ.X.ITT.HAUPT, S13.AMKG.SBJ.X.ITT.HAUPT, S13.AMKGU.SBJ.X.ITT.HAUPT, S13.AMKGO.SBJ.X.ITT.HAUPT, S13.PREM.SBJ.X.ITT.HAUPT, S13.PAHM.SBJ.X.ITT.HAUPT |

## K-07 Voraussetzungsprüfungen (5.2 Satz nach R2, Tab. H4, Anhang G)

Regel O7: Eine verworfene Prüfung (p < 0,05) ändert das Verfahren nicht, sie wird mit Prüfgröße und p berichtet. Nicht verworfene Prüfungen heißen „geprüft und nicht verworfen“.

| Kennung | Zielgröße | Shapiro-Wilk der Residuen | Brown-Forsythe | Residuen-SD je Gruppe | Steigung Gruppe × Prä | Steigung Gruppe × %PAH | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|
| K-07.1 | Sprint 30 m | W = 0,915, p = 0,034, verworfen | F(1, 24) = 2,24, p = 0,148, nicht verworfen | IG 0,087, KG 0,169, Verhältnis KG/IG 1,94 | b = +0,197 (SE 0,228), t(21) = 0,86, p = 0,398 | b = +0,0281 (SE 0,0195), t(21) = 1,44, p = 0,165 | S14.SWW.Z30.X.ITT.HAUPT, S14.SWP.Z30.X.ITT.HAUPT, S14.SWVERW.Z30.X.ITT.HAUPT, S14.BFF.Z30.X.ITT.HAUPT, S14.BFDF1.Z30.X.ITT.HAUPT, S14.BFDF2.Z30.X.ITT.HAUPT, S14.BFP.Z30.X.ITT.HAUPT, S14.BFVERW.Z30.X.ITT.HAUPT, S14.SDRIG.Z30.X.ITT.HAUPT, S14.SDRKG.Z30.X.ITT.HAUPT, S14.SDRQ.Z30.X.ITT.HAUPT, S14.BINT.Z30.X.ITT.SLPRE, S14.SEINT.Z30.X.ITT.SLPRE, S14.TINT.Z30.X.ITT.SLPRE, S14.DFINT.Z30.X.ITT.SLPRE, S14.PINT.Z30.X.ITT.SLPRE, S14.VERW.Z30.X.ITT.SLPRE, S14.BINT.Z30.X.ITT.SLPAH, S14.SEINT.Z30.X.ITT.SLPAH, S14.TINT.Z30.X.ITT.SLPAH, S14.DFINT.Z30.X.ITT.SLPAH, S14.PINT.Z30.X.ITT.SLPAH, S14.VERW.Z30.X.ITT.SLPAH |
| K-07.1 | 505-Seitenmittel | W = 0,934, p = 0,136, nicht verworfen | F(1, 21) = 1,12, p = 0,301, nicht verworfen | IG 0,057, KG 0,069, Verhältnis KG/IG 1,20 | b = −0,270 (SE 0,300), t(18) = −0,90, p = 0,380 | b = +0,0011 (SE 0,0108), t(18) = 0,10, p = 0,922 | S14.SWW.CM.X.ITT.HAUPT, S14.SWP.CM.X.ITT.HAUPT, S14.SWVERW.CM.X.ITT.HAUPT, S14.BFF.CM.X.ITT.HAUPT, S14.BFDF1.CM.X.ITT.HAUPT, S14.BFDF2.CM.X.ITT.HAUPT, S14.BFP.CM.X.ITT.HAUPT, S14.BFVERW.CM.X.ITT.HAUPT, S14.SDRIG.CM.X.ITT.HAUPT, S14.SDRKG.CM.X.ITT.HAUPT, S14.SDRQ.CM.X.ITT.HAUPT, S14.BINT.CM.X.ITT.SLPRE, S14.SEINT.CM.X.ITT.SLPRE, S14.TINT.CM.X.ITT.SLPRE, S14.DFINT.CM.X.ITT.SLPRE, S14.PINT.CM.X.ITT.SLPRE, S14.VERW.CM.X.ITT.SLPRE, S14.BINT.CM.X.ITT.SLPAH, S14.SEINT.CM.X.ITT.SLPAH, S14.TINT.CM.X.ITT.SLPAH, S14.DFINT.CM.X.ITT.SLPAH, S14.PINT.CM.X.ITT.SLPAH, S14.VERW.CM.X.ITT.SLPAH |
| K-07.1 | Standweitsprung | W = 0,968, p = 0,580, nicht verworfen | F(1, 24) = 0,77, p = 0,390, nicht verworfen | IG 6,8, KG 9,2, Verhältnis KG/IG 1,34 | b = +0,272 (SE 0,205), t(21) = 1,33, p = 0,198 | b = −1,0264 (SE 1,2907), t(21) = −0,80, p = 0,435 | S14.SWW.SBJ.X.ITT.HAUPT, S14.SWP.SBJ.X.ITT.HAUPT, S14.SWVERW.SBJ.X.ITT.HAUPT, S14.BFF.SBJ.X.ITT.HAUPT, S14.BFDF1.SBJ.X.ITT.HAUPT, S14.BFDF2.SBJ.X.ITT.HAUPT, S14.BFP.SBJ.X.ITT.HAUPT, S14.BFVERW.SBJ.X.ITT.HAUPT, S14.SDRIG.SBJ.X.ITT.HAUPT, S14.SDRKG.SBJ.X.ITT.HAUPT, S14.SDRQ.SBJ.X.ITT.HAUPT, S14.BINT.SBJ.X.ITT.SLPRE, S14.SEINT.SBJ.X.ITT.SLPRE, S14.TINT.SBJ.X.ITT.SLPRE, S14.DFINT.SBJ.X.ITT.SLPRE, S14.PINT.SBJ.X.ITT.SLPRE, S14.VERW.SBJ.X.ITT.SLPRE, S14.BINT.SBJ.X.ITT.SLPAH, S14.SEINT.SBJ.X.ITT.SLPAH, S14.TINT.SBJ.X.ITT.SLPAH, S14.DFINT.SBJ.X.ITT.SLPAH, S14.PINT.SBJ.X.ITT.SLPAH, S14.VERW.SBJ.X.ITT.SLPAH |

**K-07.2 Vorab-Prüfung an den Prä-Werten (Menge BPAH, beschreibt die Ausgangslage, keine ANCOVA-Voraussetzung):**

| Kennung | Zielgröße | Interaktion Gruppe × %PAH im Prä-Modell | Shapiro-Wilk Prä IG | Shapiro-Wilk Prä KG | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|
| K-07.2 | Sprint 30 m | c3 = +0,0006 (SE 0,0342), t(26) = 0,02, p = 0,987 | W = 0,977, p = 0,915 | W = 0,955, p = 0,713 | S14.CINT.Z30.PRE.BPAH.SLPAH, S14.SECINT.Z30.PRE.BPAH.SLPAH, S14.TCINT.Z30.PRE.BPAH.SLPAH, S14.DFCINT.Z30.PRE.BPAH.SLPAH, S14.PCINT.Z30.PRE.BPAH.SLPAH, S14.SWW.Z30.PRE.BPAHIG.X, S14.SWP.Z30.PRE.BPAHIG.X, S14.SWW.Z30.PRE.BPAHKG.X, S14.SWP.Z30.PRE.BPAHKG.X |
| K-07.2 | 505-Seitenmittel | c3 = −0,0178 (SE 0,0132), t(23) = −1,35, p = 0,191 | W = 0,871, p = 0,029 | W = 0,974, p = 0,922 | S14.CINT.CM.PRE.BPAH.SLPAH, S14.SECINT.CM.PRE.BPAH.SLPAH, S14.TCINT.CM.PRE.BPAH.SLPAH, S14.DFCINT.CM.PRE.BPAH.SLPAH, S14.PCINT.CM.PRE.BPAH.SLPAH, S14.SWW.CM.PRE.BPAHIG.X, S14.SWP.CM.PRE.BPAHIG.X, S14.SWW.CM.PRE.BPAHKG.X, S14.SWP.CM.PRE.BPAHKG.X |
| K-07.2 | Standweitsprung | c3 = −1,9781 (SE 2,0974), t(26) = −0,94, p = 0,354 | W = 0,934, p = 0,226 | W = 0,913, p = 0,235 | S14.CINT.SBJ.PRE.BPAH.SLPAH, S14.SECINT.SBJ.PRE.BPAH.SLPAH, S14.TCINT.SBJ.PRE.BPAH.SLPAH, S14.DFCINT.SBJ.PRE.BPAH.SLPAH, S14.PCINT.SBJ.PRE.BPAH.SLPAH, S14.SWW.SBJ.PRE.BPAHIG.X, S14.SWP.SBJ.PRE.BPAHIG.X, S14.SWW.SBJ.PRE.BPAHKG.X, S14.SWP.SBJ.PRE.BPAHKG.X |

## K-08 Per-Protokoll-Vergleich, Sensitivitätsanalysen und Bootstrap (Tab. H4, 5.2 Sammelsatz, 6.2)

Je Variante adjustierte Differenz b1 mit 95-%-KI, p und n je Gruppe. Bei INF = 0 (unter acht Spielern je Gruppe) nur Deskription (R4, R5). Änderungswertmodell (AEND) mit Δ = Post − Prä und %PAH, Modell ohne %PAH (OPAH), Familiarisierung als dritte Kovariate (FAMB, Set FAMS).

| Kennung | Variante | Zielgröße | n IG / KG | b1 [95-%-KI] | p | Fall | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|
| K-08.1 | PP6 (Per-Protokoll ≥ 6, Hauptschwelle) | Sprint 30 m | 9 / 10 | +0,033 [−0,201 bis +0,267] | 0,769 | C1 | S16.B1.Z30.X.PP6.HAUPT, S16.KIU.Z30.X.PP6.HAUPT, S16.KIO.Z30.X.PP6.HAUPT, S16.P.Z30.X.PP6.HAUPT, S16.NIG.Z30.X.PP6.HAUPT, S16.NKG.Z30.X.PP6.HAUPT, S16.DF.Z30.X.PP6.HAUPT |
| K-08.1 | PP6 (Per-Protokoll ≥ 6, Hauptschwelle) | 505-Seitenmittel | 7 / 10 | fehlend (Fallzahlregel) | – | – | S16.B1.CM.X.PP6.HAUPT, S16.KIU.CM.X.PP6.HAUPT, S16.KIO.CM.X.PP6.HAUPT, S16.P.CM.X.PP6.HAUPT, S16.NIG.CM.X.PP6.HAUPT, S16.NKG.CM.X.PP6.HAUPT, S16.DF.CM.X.PP6.HAUPT |
| K-08.1 | PP6 (Per-Protokoll ≥ 6, Hauptschwelle) | Standweitsprung | 9 / 10 | +0,5 [−10,9 bis +12,0] | 0,925 | C1 | S16.B1.SBJ.X.PP6.HAUPT, S16.KIU.SBJ.X.PP6.HAUPT, S16.KIO.SBJ.X.PP6.HAUPT, S16.P.SBJ.X.PP6.HAUPT, S16.NIG.SBJ.X.PP6.HAUPT, S16.NKG.SBJ.X.PP6.HAUPT, S16.DF.SBJ.X.PP6.HAUPT |
| K-08.2 | Mittelwert statt Bestwert (MW) | Sprint 30 m | 16 / 10 | −0,062 [−0,221 bis +0,098] | 0,432 | C1 | S17.B1.Z30.X.ITT.MW, S17.KIU.Z30.X.ITT.MW, S17.KIO.Z30.X.ITT.MW, S17.P.Z30.X.ITT.MW, S17.NIG.Z30.X.ITT.MW, S17.NKG.Z30.X.ITT.MW, S17.DF.Z30.X.ITT.MW |
| K-08.2 | Mittelwert statt Bestwert (MW) | 505-Seitenmittel | 13 / 10 | +0,006 [−0,077 bis +0,089] | 0,882 | C1 | S17.B1.CM.X.ITT.MW, S17.KIU.CM.X.ITT.MW, S17.KIO.CM.X.ITT.MW, S17.P.CM.X.ITT.MW, S17.NIG.CM.X.ITT.MW, S17.NKG.CM.X.ITT.MW, S17.DF.CM.X.ITT.MW |
| K-08.2 | Mittelwert statt Bestwert (MW) | Standweitsprung | 16 / 10 | −2,4 [−10,4 bis +5,6] | 0,538 | C1 | S17.B1.SBJ.X.ITT.MW, S17.KIU.SBJ.X.ITT.MW, S17.KIO.SBJ.X.ITT.MW, S17.P.SBJ.X.ITT.MW, S17.NIG.SBJ.X.ITT.MW, S17.NKG.SBJ.X.ITT.MW, S17.DF.SBJ.X.ITT.MW |
| K-08.3 | PP5 (≥ 5) | Sprint 30 m | 10 / 10 | +0,006 [−0,217 bis +0,229] | 0,956 | C1 | S17.B1.Z30.X.PP5.HAUPT, S17.KIU.Z30.X.PP5.HAUPT, S17.KIO.Z30.X.PP5.HAUPT, S17.P.Z30.X.PP5.HAUPT, S17.NIG.Z30.X.PP5.HAUPT, S17.NKG.Z30.X.PP5.HAUPT, S17.DF.Z30.X.PP5.HAUPT |
| K-08.3 | PP5 (≥ 5) | 505-Seitenmittel | 8 / 10 | −0,014 [−0,119 bis +0,091] | 0,782 | C1 | S17.B1.CM.X.PP5.HAUPT, S17.KIU.CM.X.PP5.HAUPT, S17.KIO.CM.X.PP5.HAUPT, S17.P.CM.X.PP5.HAUPT, S17.NIG.CM.X.PP5.HAUPT, S17.NKG.CM.X.PP5.HAUPT, S17.DF.CM.X.PP5.HAUPT |
| K-08.3 | PP5 (≥ 5) | Standweitsprung | 10 / 10 | −1,9 [−13,4 bis +9,6] | 0,730 | C1 | S17.B1.SBJ.X.PP5.HAUPT, S17.KIU.SBJ.X.PP5.HAUPT, S17.KIO.SBJ.X.PP5.HAUPT, S17.P.SBJ.X.PP5.HAUPT, S17.NIG.SBJ.X.PP5.HAUPT, S17.NKG.SBJ.X.PP5.HAUPT, S17.DF.SBJ.X.PP5.HAUPT |
| K-08.4 | PP7 (≥ 7) | Sprint 30 m | 8 / 10 | +0,033 [−0,219 bis +0,286] | 0,781 | C1 | S17.B1.Z30.X.PP7.HAUPT, S17.KIU.Z30.X.PP7.HAUPT, S17.KIO.Z30.X.PP7.HAUPT, S17.P.Z30.X.PP7.HAUPT, S17.NIG.Z30.X.PP7.HAUPT, S17.NKG.Z30.X.PP7.HAUPT, S17.DF.Z30.X.PP7.HAUPT |
| K-08.4 | PP7 (≥ 7) | 505-Seitenmittel | 6 / 10 | fehlend (Fallzahlregel) | – | – | S17.B1.CM.X.PP7.HAUPT, S17.KIU.CM.X.PP7.HAUPT, S17.KIO.CM.X.PP7.HAUPT, S17.P.CM.X.PP7.HAUPT, S17.NIG.CM.X.PP7.HAUPT, S17.NKG.CM.X.PP7.HAUPT, S17.DF.CM.X.PP7.HAUPT |
| K-08.4 | PP7 (≥ 7) | Standweitsprung | 8 / 10 | −0,9 [−12,7 bis +11,0] | 0,879 | C1 | S17.B1.SBJ.X.PP7.HAUPT, S17.KIU.SBJ.X.PP7.HAUPT, S17.KIO.SBJ.X.PP7.HAUPT, S17.P.SBJ.X.PP7.HAUPT, S17.NIG.SBJ.X.PP7.HAUPT, S17.NKG.SBJ.X.PP7.HAUPT, S17.DF.SBJ.X.PP7.HAUPT |
| K-08.5 | Änderungswertmodell (AEND) | Sprint 30 m | 16 / 10 | +0,049 [−0,106 bis +0,205] | 0,519 | C1 | S17.B1.Z30.X.ITT.AEND, S17.KIU.Z30.X.ITT.AEND, S17.KIO.Z30.X.ITT.AEND, S17.P.Z30.X.ITT.AEND, S17.NIG.Z30.X.ITT.AEND, S17.NKG.Z30.X.ITT.AEND, S17.DF.Z30.X.ITT.AEND |
| K-08.5 | Änderungswertmodell (AEND) | 505-Seitenmittel | 13 / 10 | −0,009 [−0,085 bis +0,067] | 0,807 | C1 | S17.B1.CM.X.ITT.AEND, S17.KIU.CM.X.ITT.AEND, S17.KIO.CM.X.ITT.AEND, S17.P.CM.X.ITT.AEND, S17.NIG.CM.X.ITT.AEND, S17.NKG.CM.X.ITT.AEND, S17.DF.CM.X.ITT.AEND |
| K-08.5 | Änderungswertmodell (AEND) | Standweitsprung | 16 / 10 | −0,6 [−9,8 bis +8,5] | 0,887 | C1 | S17.B1.SBJ.X.ITT.AEND, S17.KIU.SBJ.X.ITT.AEND, S17.KIO.SBJ.X.ITT.AEND, S17.P.SBJ.X.ITT.AEND, S17.NIG.SBJ.X.ITT.AEND, S17.NKG.SBJ.X.ITT.AEND, S17.DF.SBJ.X.ITT.AEND |
| K-08.6 | ohne %PAH (OPAH) | Sprint 30 m | 16 / 10 | −0,061 [−0,199 bis +0,078] | 0,372 | C1 | S17.B1.Z30.X.ITT.OPAH, S17.KIU.Z30.X.ITT.OPAH, S17.KIO.Z30.X.ITT.OPAH, S17.P.Z30.X.ITT.OPAH, S17.NIG.Z30.X.ITT.OPAH, S17.NKG.Z30.X.ITT.OPAH, S17.DF.Z30.X.ITT.OPAH |
| K-08.6 | ohne %PAH (OPAH) | 505-Seitenmittel | 13 / 10 | −0,008 [−0,068 bis +0,051] | 0,771 | C1 | S17.B1.CM.X.ITT.OPAH, S17.KIU.CM.X.ITT.OPAH, S17.KIO.CM.X.ITT.OPAH, S17.P.CM.X.ITT.OPAH, S17.NIG.CM.X.ITT.OPAH, S17.NKG.CM.X.ITT.OPAH, S17.DF.CM.X.ITT.OPAH |
| K-08.6 | ohne %PAH (OPAH) | Standweitsprung | 16 / 10 | +1,1 [−6,0 bis +8,1] | 0,757 | C1 | S17.B1.SBJ.X.ITT.OPAH, S17.KIU.SBJ.X.ITT.OPAH, S17.KIO.SBJ.X.ITT.OPAH, S17.P.SBJ.X.ITT.OPAH, S17.NIG.SBJ.X.ITT.OPAH, S17.NKG.SBJ.X.ITT.OPAH, S17.DF.SBJ.X.ITT.OPAH |
| K-08.7 | Familiarisierung als Kovariate (FAMB) | Sprint 30 m | 16 / 10 | −0,053 [−0,214 bis +0,107] | 0,498 | C1 | S17.B1.Z30.X.FAMS.FAMB, S17.KIU.Z30.X.FAMS.FAMB, S17.KIO.Z30.X.FAMS.FAMB, S17.P.Z30.X.FAMS.FAMB, S17.NIG.Z30.X.FAMS.FAMB, S17.NKG.Z30.X.FAMS.FAMB, S17.DF.Z30.X.FAMS.FAMB |
| K-08.7 | Familiarisierung als Kovariate (FAMB) | 505-Seitenmittel | 13 / 10 | −0,009 [−0,092 bis +0,074] | 0,827 | C1 | S17.B1.CM.X.FAMS.FAMB, S17.KIU.CM.X.FAMS.FAMB, S17.KIO.CM.X.FAMS.FAMB, S17.P.CM.X.FAMS.FAMB, S17.NIG.CM.X.FAMS.FAMB, S17.NKG.CM.X.FAMS.FAMB, S17.DF.CM.X.FAMS.FAMB |
| K-08.7 | Familiarisierung als Kovariate (FAMB) | Standweitsprung | 16 / 10 | +0,3 [−9,0 bis +9,6] | 0,945 | C1 | S17.B1.SBJ.X.FAMS.FAMB, S17.KIU.SBJ.X.FAMS.FAMB, S17.KIO.SBJ.X.FAMS.FAMB, S17.P.SBJ.X.FAMS.FAMB, S17.NIG.SBJ.X.FAMS.FAMB, S17.NKG.SBJ.X.FAMS.FAMB, S17.DF.SBJ.X.FAMS.FAMB |

**K-08.8 Bootstrap-KI der adjustierten Differenz (Perzentil, B = 10 000, Startwert 20260924, nachträglich O8, N3):**

| Kennung | Zielgröße | Bootstrap-KI | SD der b1* | MC-SE untere · obere Grenze | gültige · verworfene Ziehungen | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|
| K-08.8 | Sprint 30 m | −0,177 bis +0,107 | 0,072 | 0,0021 · 0,0026 | 10000 · 0 | S19.BKIU.Z30.X.ITT.BOOT, S19.BKIO.Z30.X.ITT.BOOT, S19.BSD.Z30.X.ITT.BOOT, S19.BMCU.Z30.X.ITT.BOOT, S19.BMCO.Z30.X.ITT.BOOT, S19.BNGUELT.Z30.X.ITT.BOOT, S19.BNVERW.Z30.X.ITT.BOOT |
| K-08.8 | 505-Seitenmittel | −0,105 bis +0,053 | 0,040 | 0,0011 · 0,0010 | 10000 · 0 | S19.BKIU.CM.X.ITT.BOOT, S19.BKIO.CM.X.ITT.BOOT, S19.BSD.CM.X.ITT.BOOT, S19.BMCU.CM.X.ITT.BOOT, S19.BMCO.CM.X.ITT.BOOT, S19.BNGUELT.CM.X.ITT.BOOT, S19.BNVERW.CM.X.ITT.BOOT |
| K-08.8 | Standweitsprung | −13,1 bis +9,7 | 5,8 | 0,15 · 0,14 | 10000 · 0 | S19.BKIU.SBJ.X.ITT.BOOT, S19.BKIO.SBJ.X.ITT.BOOT, S19.BSD.SBJ.X.ITT.BOOT, S19.BMCU.SBJ.X.ITT.BOOT, S19.BMCO.SBJ.X.ITT.BOOT, S19.BNGUELT.SBJ.X.ITT.BOOT, S19.BNVERW.SBJ.X.ITT.BOOT |

**K-08.9 Deskription der Per-Protokoll-Mengen und des Familiarisierungssets (R5, Tab. H4), M ± SD der Bestwerte:**

| Kennung | Zielgröße | PP6 IG prä | PP6 IG post | PP5 IG prä | PP5 IG post | PP7 IG prä | PP7 IG post | FAMS IG prä | FAMS IG post | FAMS KG prä | FAMS KG post | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-08.9 | Sprint 30 m | 4,50 ± 0,23 | 4,58 ± 0,20 | 4,50 ± 0,22 | 4,58 ± 0,19 | 4,48 ± 0,24 | 4,57 ± 0,21 | 4,51 ± 0,21 | 4,57 ± 0,18 | 4,89 ± 0,27 | 4,89 ± 0,23 | S16.M.Z30.PRE.PP6IG.HAUPT, S16.SD.Z30.PRE.PP6IG.HAUPT, S16.M.Z30.POST.PP6IG.HAUPT, S16.SD.Z30.POST.PP6IG.HAUPT, S17.M.Z30.PRE.PP5IG.HAUPT, S17.SD.Z30.PRE.PP5IG.HAUPT, S17.M.Z30.POST.PP5IG.HAUPT, S17.SD.Z30.POST.PP5IG.HAUPT, S17.M.Z30.PRE.PP7IG.HAUPT, S17.SD.Z30.PRE.PP7IG.HAUPT, S17.M.Z30.POST.PP7IG.HAUPT, S17.SD.Z30.POST.PP7IG.HAUPT, S17.M.Z30.PRE.FAMSIG.FAMB, S17.SD.Z30.PRE.FAMSIG.FAMB, S17.M.Z30.POST.FAMSIG.FAMB, S17.SD.Z30.POST.FAMSIG.FAMB, S17.M.Z30.PRE.FAMSKG.FAMB, S17.SD.Z30.PRE.FAMSKG.FAMB, S17.M.Z30.POST.FAMSKG.FAMB, S17.SD.Z30.POST.FAMSKG.FAMB |
| K-08.9 | 505-Seitenmittel | 2,42 ± 0,11 | 2,47 ± 0,09 | 2,43 ± 0,10 | 2,46 ± 0,08 | 2,42 ± 0,12 | 2,47 ± 0,09 | 2,46 ± 0,09 | 2,47 ± 0,08 | 2,53 ± 0,11 | 2,53 ± 0,12 | S16.M.CM.PRE.PP6IG.HAUPT, S16.SD.CM.PRE.PP6IG.HAUPT, S16.M.CM.POST.PP6IG.HAUPT, S16.SD.CM.POST.PP6IG.HAUPT, S17.M.CM.PRE.PP5IG.HAUPT, S17.SD.CM.PRE.PP5IG.HAUPT, S17.M.CM.POST.PP5IG.HAUPT, S17.SD.CM.POST.PP5IG.HAUPT, S17.M.CM.PRE.PP7IG.HAUPT, S17.SD.CM.PRE.PP7IG.HAUPT, S17.M.CM.POST.PP7IG.HAUPT, S17.SD.CM.POST.PP7IG.HAUPT, S17.M.CM.PRE.FAMSIG.FAMB, S17.SD.CM.PRE.FAMSIG.FAMB, S17.M.CM.POST.FAMSIG.FAMB, S17.SD.CM.POST.FAMSIG.FAMB, S17.M.CM.PRE.FAMSKG.FAMB, S17.SD.CM.PRE.FAMSKG.FAMB, S17.M.CM.POST.FAMSKG.FAMB, S17.SD.CM.POST.FAMSKG.FAMB |
| K-08.9 | Standweitsprung | 243 ± 9 | 239 ± 5 | 240 ± 14 | 236 ± 13 | 242 ± 9 | 238 ± 3 | 238 ± 13 | 233 ± 14 | 226 ± 21 | 223 ± 17 | S16.M.SBJ.PRE.PP6IG.HAUPT, S16.SD.SBJ.PRE.PP6IG.HAUPT, S16.M.SBJ.POST.PP6IG.HAUPT, S16.SD.SBJ.POST.PP6IG.HAUPT, S17.M.SBJ.PRE.PP5IG.HAUPT, S17.SD.SBJ.PRE.PP5IG.HAUPT, S17.M.SBJ.POST.PP5IG.HAUPT, S17.SD.SBJ.POST.PP5IG.HAUPT, S17.M.SBJ.PRE.PP7IG.HAUPT, S17.SD.SBJ.PRE.PP7IG.HAUPT, S17.M.SBJ.POST.PP7IG.HAUPT, S17.SD.SBJ.POST.PP7IG.HAUPT, S17.M.SBJ.PRE.FAMSIG.FAMB, S17.SD.SBJ.PRE.FAMSIG.FAMB, S17.M.SBJ.POST.FAMSIG.FAMB, S17.SD.SBJ.POST.FAMSIG.FAMB, S17.M.SBJ.PRE.FAMSKG.FAMB, S17.SD.SBJ.PRE.FAMSKG.FAMB, S17.M.SBJ.POST.FAMSKG.FAMB, S17.SD.SBJ.POST.FAMSKG.FAMB |

n der Per-Protokoll- und Familiarisierungssets (K-08.10, IG, KG-Teil gleich dem ITT-KG):

| Kennung | Zielgröße | n je Set und Merkmal INF | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-08.10 | Sprint 30 m | PP5 10 · PP6 9 · PP7 8 · AK9 3 · FAMS IG 16, KG 10 · inferenzfähig (ITT, PP5, PP6, PP7, FAMS): 1, 1, 1, 1, 1 | S08.N.Z30.X.PP5IG.X, S08.N.Z30.X.PP6IG.X, S08.N.Z30.X.PP7IG.X, S08.N.Z30.X.AK9IG.X, S08.N.Z30.X.FAMSIG.X, S08.N.Z30.X.FAMSKG.X, S08.INF.Z30.X.ITT.X, S08.INF.Z30.X.PP5.X, S08.INF.Z30.X.PP6.X, S08.INF.Z30.X.PP7.X, S08.INF.Z30.X.FAMS.X |
| K-08.10 | 505-Seitenmittel | PP5 8 · PP6 7 · PP7 6 · AK9 3 · FAMS IG 13, KG 10 · inferenzfähig (ITT, PP5, PP6, PP7, FAMS): 1, 1, 0, 0, 1 | S08.N.CM.X.PP5IG.X, S08.N.CM.X.PP6IG.X, S08.N.CM.X.PP7IG.X, S08.N.CM.X.AK9IG.X, S08.N.CM.X.FAMSIG.X, S08.N.CM.X.FAMSKG.X, S08.INF.CM.X.ITT.X, S08.INF.CM.X.PP5.X, S08.INF.CM.X.PP6.X, S08.INF.CM.X.PP7.X, S08.INF.CM.X.FAMS.X |
| K-08.10 | Standweitsprung | PP5 10 · PP6 9 · PP7 8 · AK9 3 · FAMS IG 16, KG 10 · inferenzfähig (ITT, PP5, PP6, PP7, FAMS): 1, 1, 1, 1, 1 | S08.N.SBJ.X.PP5IG.X, S08.N.SBJ.X.PP6IG.X, S08.N.SBJ.X.PP7IG.X, S08.N.SBJ.X.AK9IG.X, S08.N.SBJ.X.FAMSIG.X, S08.N.SBJ.X.FAMSKG.X, S08.INF.SBJ.X.ITT.X, S08.INF.SBJ.X.PP5.X, S08.INF.SBJ.X.PP6.X, S08.INF.SBJ.X.PP7.X, S08.INF.SBJ.X.FAMS.X |

**K-08.11 Familiarisierung Variante a, nur deskriptiv: Δ = Post − Prä (Bestwert) je Gruppe und Zahl der Termine (Tab. H4):**

| Kennung | Zielgröße | IG ein Termin | IG zwei Termine | KG ein Termin | KG zwei Termine | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|
| K-08.11 | Sprint 30 m | n = 9: +0,089 ± 0,101 | n = 7: +0,013 ± 0,056 | n = 0: fehlend (zu wenige Werte) | n = 10: −0,001 ± 0,204 | S17.N.Z30.DIFF.ITTIG.F1, S17.M.Z30.DIFF.ITTIG.F1, S17.SD.Z30.DIFF.ITTIG.F1, S17.N.Z30.DIFF.ITTIG.F2, S17.M.Z30.DIFF.ITTIG.F2, S17.SD.Z30.DIFF.ITTIG.F2, S17.N.Z30.DIFF.ITTKG.F1, S17.M.Z30.DIFF.ITTKG.F1, S17.SD.Z30.DIFF.ITTKG.F1, S17.N.Z30.DIFF.ITTKG.F2, S17.M.Z30.DIFF.ITTKG.F2, S17.SD.Z30.DIFF.ITTKG.F2 |
| K-08.11 | 505-Seitenmittel | n = 8: +0,019 ± 0,077 | n = 5: +0,010 ± 0,054 | n = 0: fehlend (zu wenige Werte) | n = 10: +0,006 ± 0,069 | S17.N.CM.DIFF.ITTIG.F1, S17.M.CM.DIFF.ITTIG.F1, S17.SD.CM.DIFF.ITTIG.F1, S17.N.CM.DIFF.ITTIG.F2, S17.M.CM.DIFF.ITTIG.F2, S17.SD.CM.DIFF.ITTIG.F2, S17.N.CM.DIFF.ITTKG.F1, S17.M.CM.DIFF.ITTKG.F1, S17.SD.CM.DIFF.ITTKG.F1, S17.N.CM.DIFF.ITTKG.F2, S17.M.CM.DIFF.ITTKG.F2, S17.SD.CM.DIFF.ITTKG.F2 |
| K-08.11 | Standweitsprung | n = 9: −5,0 ± 7,7 | n = 7: −3,7 ± 4,6 | n = 0: fehlend (zu wenige Werte) | n = 10: −3,2 ± 11,2 | S17.N.SBJ.DIFF.ITTIG.F1, S17.M.SBJ.DIFF.ITTIG.F1, S17.SD.SBJ.DIFF.ITTIG.F1, S17.N.SBJ.DIFF.ITTIG.F2, S17.M.SBJ.DIFF.ITTIG.F2, S17.SD.SBJ.DIFF.ITTIG.F2, S17.N.SBJ.DIFF.ITTKG.F1, S17.M.SBJ.DIFF.ITTKG.F1, S17.SD.SBJ.DIFF.ITTKG.F1, S17.N.SBJ.DIFF.ITTKG.F2, S17.M.SBJ.DIFF.ITTKG.F2, S17.SD.SBJ.DIFF.ITTKG.F2 |

## K-09 Sensitivitäts-Poweranalyse, Standardweg (4.7, 6.2, Anhang G)

F-Test des Gruppenterms, df1 = 1, df2 = N − 4, λ = d²·n_IG·n_KG/N, α = 0,05, ohne Kovariatengewinn (O9). MDES = kleinster Effekt d mit Power 0,80, MDES/0,2 = Vielfaches des SESOI. Power bei den im Plan genannten Vorab-Erwartungen (D006 und D011 nur 10 m, D037 und D093 für die konfirmatorischen Zielgrößen).

| Kennung | Zielgröße | N | df1, df2 | F_krit | MDES (Power 0,80) | Power bei Vorab-Erwartung | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|
| K-09.1 | Sprint 10 m | 17 | 1, 13 | 4,67 | – | d = 0,06: 0,051 · d = 0,11: 0,055 | S18.NTOT.Z10.X.ITT.X, S18.DF1.Z10.X.ITT.X, S18.DF2.Z10.X.ITT.X, S18.FCRIT.Z10.X.ITT.X, S18.POW.Z10.X.ITT.D006, S18.POW.Z10.X.ITT.D011 |
| K-09.2 | Sprint 30 m | 26 | 1, 22 | 4,30 | 1,18 (5,9 × SESOI) | d = 0,37: 0,14 · d = 0,93: 0,60 | S18.NTOT.Z30.X.ITT.X, S18.DF1.Z30.X.ITT.X, S18.DF2.Z30.X.ITT.X, S18.FCRIT.Z30.X.ITT.X, S18.MDES.Z30.X.ITT.X, S18.MDESR.Z30.X.ITT.X, S18.POW.Z30.X.ITT.D037, S18.POW.Z30.X.ITT.D093 |
| K-09.3 | 505-Seitenmittel | 23 | 1, 19 | 4,38 | 1,24 (6,2 × SESOI) | d = 0,37: 0,13 · d = 0,93: 0,56 | S18.NTOT.CM.X.ITT.X, S18.DF1.CM.X.ITT.X, S18.DF2.CM.X.ITT.X, S18.FCRIT.CM.X.ITT.X, S18.MDES.CM.X.ITT.X, S18.MDESR.CM.X.ITT.X, S18.POW.CM.X.ITT.D037, S18.POW.CM.X.ITT.D093 |
| K-09.4 | Standweitsprung | 26 | 1, 22 | 4,30 | 1,18 (5,9 × SESOI) | d = 0,37: 0,14 · d = 0,93: 0,60 | S18.NTOT.SBJ.X.ITT.X, S18.DF1.SBJ.X.ITT.X, S18.DF2.SBJ.X.ITT.X, S18.FCRIT.SBJ.X.ITT.X, S18.MDES.SBJ.X.ITT.X, S18.MDESR.SBJ.X.ITT.X, S18.POW.SBJ.X.ITT.D037, S18.POW.SBJ.X.ITT.D093 |

## K-10 Adhärenz, Belastung, unerwünschte Ereignisse (4.6, 4.7, 5.1, Tab. H2, Tab. H5)

| Kennung | Größe | Wert | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-10.1 | Meldungen des Fragebogens A gesamt | 111 | S06.NMELD.FB.X.ALL.X |
| K-10.2 | korrigierte Meldungen (Fallkorrekturen) · Dublettenpaare · Sammelmeldungspaare | 7 · 1 · 7 | S06.NKORR.FB.X.ALL.X, S06.NDUBL.FB.X.ALL.X, S06.NSAMM.FB.X.ALL.X |
| K-10.3 | Meldungen je Status: ganz · teilweise · gar nicht | 92 · 6 · 13 | S06.NSTAT.FB.X.IG.GANZ, S06.NSTAT.FB.X.IG.TEILW, S06.NSTAT.FB.X.IG.GARN |
| K-10.4 | zugeteilte IG-Spieler (Nenner 12 Einheiten je Spieler) | 18 | S07.NZUG.ADH.X.IG.X |
| K-10.5 | Summe und Umsetzungsrate GANZ | 92 Einheiten, 42,6 % | S07.SUMME.ADH.X.IG.GANZ, S07.RATE.ADH.X.IG.GANZ |
| K-10.6 | Summe und Beteiligungsrate GT (ganz oder teilweise) | 98 Einheiten, 45,4 % | S07.SUMME.ADH.X.IG.GT, S07.RATE.ADH.X.IG.GT |
| K-10.7 | Untergrenzen: Summe und Rate wochengedeckelt (WOCAP) · nach distinkten Nummern (DIST) | 90, 41,7 % · 86, 39,8 % | S07.SUMME.ADH.X.IG.WOCAP, S07.RATE.ADH.X.IG.WOCAP, S07.SUMME.ADH.X.IG.DIST, S07.RATE.ADH.X.IG.DIST |
| K-10.8 | Median und Mittel der Zählung GANZ je zugeteiltem Spieler | Median 6,0, Mittel 5,11 | S07.MED.ADH.X.IG.GANZ, S07.MITT.ADH.X.IG.GANZ |
| K-10.9 | Spieler mit mindestens einer Meldung (gleich welchen Status) | 15 | S07.NMELDSP.ADH.X.IG.X |
| K-10.10 | Spieler mit GANZ ≥ 6 · ≥ 9 (Hauptzählung) | 10 · 3 | S07.GE06.ADH.X.IG.GANZ, S07.GE09.ADH.X.IG.GANZ |
| K-10.11 | Spieler mit ≥ 6 · ≥ 9 nach WOCAP und nach DIST | WOCAP 9 · 2, DIST 9 · 1 | S07.GE06.ADH.X.IG.WOCAP, S07.GE09.ADH.X.IG.WOCAP, S07.GE06.ADH.X.IG.DIST, S07.GE09.ADH.X.IG.DIST |
| K-10.12 | unerwünschte Ereignisse (H007 = 1): Meldungen gesamt · ganz · teilweise · gar nicht · Spieler | 12 · 8 · 2 · 2 · 9 Spieler | S07.UE.FB.X.IG.X, S07.UE.FB.X.IG.GANZ, S07.UE.FB.X.IG.TEILW, S07.UE.FB.X.IG.GARN, S07.UESP.FB.X.IG.X |
| K-10.13 | CR-10 der Meldungen „ganz“ | n = 92, 2,9 ± 0,9, Median 3,0, Min 0,0, Max 5,0 | S07.N.CR10.X.IG.GANZ, S07.M.CR10.X.IG.GANZ, S07.SD.CR10.X.IG.GANZ, S07.MED.CR10.X.IG.GANZ, S07.MIN.CR10.X.IG.GANZ, S07.MAX.CR10.X.IG.GANZ |
| K-10.14 | sRPE-Load der Meldungen „ganz“ (AU, CR-10 mal Solldauer der Woche) | n = 92, 106,7 ± 35,9, Median 110,8, Min 0,0, Max 199,7 | S07.N.LOAD.X.IG.GANZ, S07.M.LOAD.X.IG.GANZ, S07.SD.LOAD.X.IG.GANZ, S07.MED.LOAD.X.IG.GANZ, S07.MIN.LOAD.X.IG.GANZ, S07.MAX.LOAD.X.IG.GANZ |

**K-10.15 Verteilung der Zählung GANZ und Schwellenlandschaft (Tab. H2, Tab. H5):**

| Einheiten „ganz“ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Spieler mit genau | 4 | 0 | 2 | 0 | 1 | 1 | 2 | 3 | 2 | 2 | 0 | 0 | 1 |
| Spieler mit mindestens | – | 14 | 14 | 12 | 12 | 11 | 10 | 8 | 5 | 3 | 1 | 1 | 1 |

**K-10.16 Wochenverlauf (Tab. H2): Wochenanteil der Meldungen „ganz“ (Meldungen / (2 · zugeteilte Spieler)), CR-10 und sRPE-Load je Programmwoche:**

| Kennung | Woche | Wochenanteil ganz | CR-10 (n, M ± SD) | sRPE-Load (n, M ± SD) | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|
| K-10.16 | W1 | 44,4 % | n = 16, 2,8 ± 0,7 | n = 16, 104,5 ± 24,3 | S07.ANTW.ADH.W1.IG.GANZ, S07.N.CR10.W1.IG.GANZ, S07.M.CR10.W1.IG.GANZ, S07.SD.CR10.W1.IG.GANZ, S07.N.LOAD.W1.IG.GANZ, S07.M.LOAD.W1.IG.GANZ, S07.SD.LOAD.W1.IG.GANZ |
| K-10.16 | W2 | 55,6 % | n = 20, 3,0 ± 0,6 | n = 20, 110,8 ± 24,0 | S07.ANTW.ADH.W2.IG.GANZ, S07.N.CR10.W2.IG.GANZ, S07.M.CR10.W2.IG.GANZ, S07.SD.CR10.W2.IG.GANZ, S07.N.LOAD.W2.IG.GANZ, S07.M.LOAD.W2.IG.GANZ, S07.SD.LOAD.W2.IG.GANZ |
| K-10.16 | W3 | 44,4 % | n = 16, 2,6 ± 0,5 | n = 16, 87,1 ± 16,6 | S07.ANTW.ADH.W3.IG.GANZ, S07.N.CR10.W3.IG.GANZ, S07.M.CR10.W3.IG.GANZ, S07.SD.CR10.W3.IG.GANZ, S07.N.LOAD.W3.IG.GANZ, S07.M.LOAD.W3.IG.GANZ, S07.SD.LOAD.W3.IG.GANZ |
| K-10.16 | W4 | 50,0 % | n = 18, 2,8 ± 1,2 | n = 18, 98,6 ± 43,4 | S07.ANTW.ADH.W4.IG.GANZ, S07.N.CR10.W4.IG.GANZ, S07.M.CR10.W4.IG.GANZ, S07.SD.CR10.W4.IG.GANZ, S07.N.LOAD.W4.IG.GANZ, S07.M.LOAD.W4.IG.GANZ, S07.SD.LOAD.W4.IG.GANZ |
| K-10.16 | W5 | 41,7 % | n = 15, 3,3 ± 1,2 | n = 15, 130,4 ± 46,4 | S07.ANTW.ADH.W5.IG.GANZ, S07.N.CR10.W5.IG.GANZ, S07.M.CR10.W5.IG.GANZ, S07.SD.CR10.W5.IG.GANZ, S07.N.LOAD.W5.IG.GANZ, S07.M.LOAD.W5.IG.GANZ, S07.SD.LOAD.W5.IG.GANZ |
| K-10.16 | W6 | 19,4 % | n = 7, 2,9 ± 1,2 | n = 7, 114,6 ± 48,7 | S07.ANTW.ADH.W6.IG.GANZ, S07.N.CR10.W6.IG.GANZ, S07.M.CR10.W6.IG.GANZ, S07.SD.CR10.W6.IG.GANZ, S07.N.LOAD.W6.IG.GANZ, S07.M.LOAD.W6.IG.GANZ, S07.SD.LOAD.W6.IG.GANZ |

**K-10.17 Antragskriterium (AK9, ≥ 9 von 12 Einheiten „ganz“): Einzelwerte Δ = BEST post − BEST prä je Spieler (Tab. H2), keine Inferenz:**

| Kennung | Code | Δ 30 m | Δ 505-Seitenmittel | Δ Standweitsprung | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|
| K-10.17 | BW-02 | +0,010 s | −0,050 s | +7,0 cm | S16.DIFF.Z30.DIFF.PBW-02.AK9, S16.DIFF.CM.DIFF.PBW-02.AK9, S16.DIFF.SBJ.DIFF.PBW-02.AK9 |
| K-10.17 | BW-08 | −0,010 s | +0,065 s | −7,0 cm | S16.DIFF.Z30.DIFF.PBW-08.AK9, S16.DIFF.CM.DIFF.PBW-08.AK9, S16.DIFF.SBJ.DIFF.PBW-08.AK9 |
| K-10.17 | HL-03 | +0,130 s | +0,075 s | −8,0 cm | S16.DIFF.Z30.DIFF.PHL-03.AK9, S16.DIFF.CM.DIFF.PHL-03.AK9, S16.DIFF.SBJ.DIFF.PHL-03.AK9 |

## K-11 Versuche, Ausfälle, Bestwert-Bias (4.4, Tab. H1)

| Kennung | Größe | Wert | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-11.1 | Zeilen der Versuchsdaten (Raster) | 1116 | S01.NZEIL.X.X.ALL.X |
| K-11.2 | auslösegestörte Sprintläufe prä · post | 0 · 0 | S02.NAUSL.X.PRE.ALL.X, S02.NAUSL.X.POST.ALL.X |

**K-11.3 gültige Versuche je Zielgröße und Zeitpunkt (alle Spieler) und mittlere Zahl gültiger Versuche je Spieler und Gruppe (S09, Bezugsmenge: Spieler mit Zeilen zum Zeitpunkt, post ohne nicht angetretene):**

| Kennung | Zielgröße | gültig prä | gültig post | k̄ prä IG | k̄ prä KG | k̄ post IG | k̄ post KG | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|
| K-11.3 | Sprint 5 m | 53 | 64 | 2,22 | 1,00 | 2,69 | 1,91 | S02.NGUELT.Z05.PRE.ALL.X, S02.NGUELT.Z05.POST.ALL.X, S09.KMEAN.Z05.PRE.IG.X, S09.KMEAN.Z05.PRE.KG.X, S09.KMEAN.Z05.POST.IG.X, S09.KMEAN.Z05.POST.KG.X |
| K-11.3 | Sprint 10 m | 67 | 38 | 2,56 | 1,62 | 1,25 | 1,64 | S02.NGUELT.Z10.PRE.ALL.X, S02.NGUELT.Z10.POST.ALL.X, S09.KMEAN.Z10.PRE.IG.X, S09.KMEAN.Z10.PRE.KG.X, S09.KMEAN.Z10.POST.IG.X, S09.KMEAN.Z10.POST.KG.X |
| K-11.3 | Sprint 30 m | 78 | 65 | 2,61 | 2,38 | 2,56 | 2,18 | S02.NGUELT.Z30.PRE.ALL.X, S02.NGUELT.Z30.POST.ALL.X, S09.KMEAN.Z30.PRE.IG.X, S09.KMEAN.Z30.PRE.KG.X, S09.KMEAN.Z30.POST.IG.X, S09.KMEAN.Z30.POST.KG.X |
| K-11.3 | 505 links | 55 | 48 | 1,83 | 1,69 | 1,62 | 2,00 | S02.NGUELT.CL.PRE.ALL.X, S02.NGUELT.CL.POST.ALL.X, S09.KMEAN.CL.PRE.IG.X, S09.KMEAN.CL.PRE.KG.X, S09.KMEAN.CL.POST.IG.X, S09.KMEAN.CL.POST.KG.X |
| K-11.3 | 505 rechts | 59 | 40 | 1,89 | 1,92 | 1,44 | 1,55 | S02.NGUELT.CR.PRE.ALL.X, S02.NGUELT.CR.POST.ALL.X, S09.KMEAN.CR.PRE.IG.X, S09.KMEAN.CR.PRE.KG.X, S09.KMEAN.CR.POST.IG.X, S09.KMEAN.CR.POST.KG.X |
| K-11.3 | Standweitsprung | 72 | 53 | 2,50 | 2,08 | 2,00 | 1,91 | S02.NGUELT.SBJ.PRE.ALL.X, S02.NGUELT.SBJ.POST.ALL.X, S09.KMEAN.SBJ.PRE.IG.X, S09.KMEAN.SBJ.PRE.KG.X, S09.KMEAN.SBJ.POST.IG.X, S09.KMEAN.SBJ.POST.KG.X |

**K-11.4 ungültige Zeilen je Ausfallkategorie (S03: TECH technischer Ausfall, ZEIT dritter Versuch aus Zeitmangel, FEHL nicht wiederholbarer Fehlversuch, FALSCH falsch aufgenommen, NANG nicht angetreten (nur post), AUSL auslösegestört):**

| Kennung | Zielgröße | Zeit | IG TECH | IG ZEIT | IG FEHL | IG FALSCH | IG NANG | IG AUSL | KG TECH | KG ZEIT | KG FEHL | KG FALSCH | KG NANG | KG AUSL | Kennung der Ergebnisdatei |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-11.4 | Sprint 5 m | prä | 9 | 5 | 0 | 0 | – | 0 | 26 | 0 | 0 | 0 | – | 0 | S03.NKAT.Z05.PRE.IG.TECH, S03.NKAT.Z05.PRE.IG.ZEIT, S03.NKAT.Z05.PRE.IG.FEHL, S03.NKAT.Z05.PRE.IG.FALSCH, S03.NKAT.Z05.PRE.IG.AUSL, S03.NKAT.Z05.PRE.KG.TECH, S03.NKAT.Z05.PRE.KG.ZEIT, S03.NKAT.Z05.PRE.KG.FEHL, S03.NKAT.Z05.PRE.KG.FALSCH, S03.NKAT.Z05.PRE.KG.AUSL |
| K-11.4 | Sprint 5 m | post | 1 | 4 | 0 | 0 | 6 | 0 | 5 | 7 | 0 | 0 | 6 | 0 | S03.NKAT.Z05.POST.IG.TECH, S03.NKAT.Z05.POST.IG.ZEIT, S03.NKAT.Z05.POST.IG.FEHL, S03.NKAT.Z05.POST.IG.FALSCH, S03.NKAT.Z05.POST.IG.NANG, S03.NKAT.Z05.POST.IG.AUSL, S03.NKAT.Z05.POST.KG.TECH, S03.NKAT.Z05.POST.KG.ZEIT, S03.NKAT.Z05.POST.KG.FEHL, S03.NKAT.Z05.POST.KG.FALSCH, S03.NKAT.Z05.POST.KG.NANG, S03.NKAT.Z05.POST.KG.AUSL |
| K-11.4 | Sprint 10 m | prä | 3 | 5 | 0 | 0 | – | 0 | 18 | 0 | 0 | 0 | – | 0 | S03.NKAT.Z10.PRE.IG.TECH, S03.NKAT.Z10.PRE.IG.ZEIT, S03.NKAT.Z10.PRE.IG.FEHL, S03.NKAT.Z10.PRE.IG.FALSCH, S03.NKAT.Z10.PRE.IG.AUSL, S03.NKAT.Z10.PRE.KG.TECH, S03.NKAT.Z10.PRE.KG.ZEIT, S03.NKAT.Z10.PRE.KG.FEHL, S03.NKAT.Z10.PRE.KG.FALSCH, S03.NKAT.Z10.PRE.KG.AUSL |
| K-11.4 | Sprint 10 m | post | 1 | 0 | 0 | 27 | 6 | 0 | 7 | 8 | 0 | 0 | 6 | 0 | S03.NKAT.Z10.POST.IG.TECH, S03.NKAT.Z10.POST.IG.ZEIT, S03.NKAT.Z10.POST.IG.FEHL, S03.NKAT.Z10.POST.IG.FALSCH, S03.NKAT.Z10.POST.IG.NANG, S03.NKAT.Z10.POST.IG.AUSL, S03.NKAT.Z10.POST.KG.TECH, S03.NKAT.Z10.POST.KG.ZEIT, S03.NKAT.Z10.POST.KG.FEHL, S03.NKAT.Z10.POST.KG.FALSCH, S03.NKAT.Z10.POST.KG.NANG, S03.NKAT.Z10.POST.KG.AUSL |
| K-11.4 | Sprint 30 m | prä | 2 | 5 | 0 | 0 | – | 0 | 8 | 0 | 0 | 0 | – | 0 | S03.NKAT.Z30.PRE.IG.TECH, S03.NKAT.Z30.PRE.IG.ZEIT, S03.NKAT.Z30.PRE.IG.FEHL, S03.NKAT.Z30.PRE.IG.FALSCH, S03.NKAT.Z30.PRE.IG.AUSL, S03.NKAT.Z30.PRE.KG.TECH, S03.NKAT.Z30.PRE.KG.ZEIT, S03.NKAT.Z30.PRE.KG.FEHL, S03.NKAT.Z30.PRE.KG.FALSCH, S03.NKAT.Z30.PRE.KG.AUSL |
| K-11.4 | Sprint 30 m | post | 3 | 4 | 0 | 0 | 6 | 0 | 2 | 7 | 0 | 0 | 6 | 0 | S03.NKAT.Z30.POST.IG.TECH, S03.NKAT.Z30.POST.IG.ZEIT, S03.NKAT.Z30.POST.IG.FEHL, S03.NKAT.Z30.POST.IG.FALSCH, S03.NKAT.Z30.POST.IG.NANG, S03.NKAT.Z30.POST.IG.AUSL, S03.NKAT.Z30.POST.KG.TECH, S03.NKAT.Z30.POST.KG.ZEIT, S03.NKAT.Z30.POST.KG.FEHL, S03.NKAT.Z30.POST.KG.FALSCH, S03.NKAT.Z30.POST.KG.NANG, S03.NKAT.Z30.POST.KG.AUSL |
| K-11.4 | 505 links | prä | 8 | 11 | 2 | 0 | – | 0 | 7 | 7 | 3 | 0 | – | 0 | S03.NKAT.CL.PRE.IG.TECH, S03.NKAT.CL.PRE.IG.ZEIT, S03.NKAT.CL.PRE.IG.FEHL, S03.NKAT.CL.PRE.IG.FALSCH, S03.NKAT.CL.PRE.IG.AUSL, S03.NKAT.CL.PRE.KG.TECH, S03.NKAT.CL.PRE.KG.ZEIT, S03.NKAT.CL.PRE.KG.FEHL, S03.NKAT.CL.PRE.KG.FALSCH, S03.NKAT.CL.PRE.KG.AUSL |
| K-11.4 | 505 links | post | 0 | 16 | 6 | 0 | 6 | 0 | 0 | 11 | 0 | 0 | 6 | 0 | S03.NKAT.CL.POST.IG.TECH, S03.NKAT.CL.POST.IG.ZEIT, S03.NKAT.CL.POST.IG.FEHL, S03.NKAT.CL.POST.IG.FALSCH, S03.NKAT.CL.POST.IG.NANG, S03.NKAT.CL.POST.IG.AUSL, S03.NKAT.CL.POST.KG.TECH, S03.NKAT.CL.POST.KG.ZEIT, S03.NKAT.CL.POST.KG.FEHL, S03.NKAT.CL.POST.KG.FALSCH, S03.NKAT.CL.POST.KG.NANG, S03.NKAT.CL.POST.KG.AUSL |
| K-11.4 | 505 rechts | prä | 5 | 11 | 4 | 0 | – | 0 | 3 | 8 | 3 | 0 | – | 0 | S03.NKAT.CR.PRE.IG.TECH, S03.NKAT.CR.PRE.IG.ZEIT, S03.NKAT.CR.PRE.IG.FEHL, S03.NKAT.CR.PRE.IG.FALSCH, S03.NKAT.CR.PRE.IG.AUSL, S03.NKAT.CR.PRE.KG.TECH, S03.NKAT.CR.PRE.KG.ZEIT, S03.NKAT.CR.PRE.KG.FEHL, S03.NKAT.CR.PRE.KG.FALSCH, S03.NKAT.CR.PRE.KG.AUSL |
| K-11.4 | 505 rechts | post | 0 | 16 | 9 | 0 | 6 | 0 | 0 | 11 | 5 | 0 | 6 | 0 | S03.NKAT.CR.POST.IG.TECH, S03.NKAT.CR.POST.IG.ZEIT, S03.NKAT.CR.POST.IG.FEHL, S03.NKAT.CR.POST.IG.FALSCH, S03.NKAT.CR.POST.IG.NANG, S03.NKAT.CR.POST.IG.AUSL, S03.NKAT.CR.POST.KG.TECH, S03.NKAT.CR.POST.KG.ZEIT, S03.NKAT.CR.POST.KG.FEHL, S03.NKAT.CR.POST.KG.FALSCH, S03.NKAT.CR.POST.KG.NANG, S03.NKAT.CR.POST.KG.AUSL |
| K-11.4 | Standweitsprung | prä | 2 | 5 | 2 | 0 | – | 0 | 3 | 7 | 2 | 0 | – | 0 | S03.NKAT.SBJ.PRE.IG.TECH, S03.NKAT.SBJ.PRE.IG.ZEIT, S03.NKAT.SBJ.PRE.IG.FEHL, S03.NKAT.SBJ.PRE.IG.FALSCH, S03.NKAT.SBJ.PRE.IG.AUSL, S03.NKAT.SBJ.PRE.KG.TECH, S03.NKAT.SBJ.PRE.KG.ZEIT, S03.NKAT.SBJ.PRE.KG.FEHL, S03.NKAT.SBJ.PRE.KG.FALSCH, S03.NKAT.SBJ.PRE.KG.AUSL |
| K-11.4 | Standweitsprung | post | 0 | 11 | 5 | 0 | 6 | 0 | 0 | 11 | 1 | 0 | 6 | 0 | S03.NKAT.SBJ.POST.IG.TECH, S03.NKAT.SBJ.POST.IG.ZEIT, S03.NKAT.SBJ.POST.IG.FEHL, S03.NKAT.SBJ.POST.IG.FALSCH, S03.NKAT.SBJ.POST.IG.NANG, S03.NKAT.SBJ.POST.IG.AUSL, S03.NKAT.SBJ.POST.KG.TECH, S03.NKAT.SBJ.POST.KG.ZEIT, S03.NKAT.SBJ.POST.KG.FEHL, S03.NKAT.SBJ.POST.KG.FALSCH, S03.NKAT.SBJ.POST.KG.NANG, S03.NKAT.SBJ.POST.KG.AUSL |
| K-11.4 | Summe über die sechs Zielgrößen (abgeleitet) | prä | 29 | 42 | 8 | 0 | – | 0 | 65 | 22 | 8 | 0 | – | 0 | Summe der Zeilen oben |
| K-11.4 | Summe über die sechs Zielgrößen (abgeleitet) | post | 5 | 51 | 20 | 27 | 36 | 0 | 14 | 55 | 6 | 0 | 36 | 0 | Summe der Zeilen oben |

**K-11.5 fehlende Werte je Zielgröße (Teilnehmerfluss S08 Regel 8): Spieler ohne BEST prä · ohne BEST post, je Gruppe:**

| Kennung | Zielgröße | Wert | Kennung der Ergebnisdatei |
|---|---|---|---|
| K-11.5 | Sprint 5 m | ohne Prä: IG 0, KG 5 · ohne Post: IG 2, KG 2 | S08.FLOPRE.Z05.X.IG.X, S08.FLOPRE.Z05.X.KG.X, S08.FLOPOST.Z05.X.IG.X, S08.FLOPOST.Z05.X.KG.X |
| K-11.5 | Sprint 10 m | ohne Prä: IG 0, KG 0 · ohne Post: IG 11, KG 2 | S08.FLOPRE.Z10.X.IG.X, S08.FLOPRE.Z10.X.KG.X, S08.FLOPOST.Z10.X.IG.X, S08.FLOPOST.Z10.X.KG.X |
| K-11.5 | Sprint 30 m | ohne Prä: IG 0, KG 0 · ohne Post: IG 2, KG 2 | S08.FLOPRE.Z30.X.IG.X, S08.FLOPRE.Z30.X.KG.X, S08.FLOPOST.Z30.X.IG.X, S08.FLOPOST.Z30.X.KG.X |
| K-11.5 | 505 links | ohne Prä: IG 1, KG 1 · ohne Post: IG 2, KG 2 | S08.FLOPRE.CL.X.IG.X, S08.FLOPRE.CL.X.KG.X, S08.FLOPOST.CL.X.IG.X, S08.FLOPOST.CL.X.KG.X |
| K-11.5 | 505 rechts | ohne Prä: IG 1, KG 1 · ohne Post: IG 3, KG 2 | S08.FLOPRE.CR.X.IG.X, S08.FLOPRE.CR.X.KG.X, S08.FLOPOST.CR.X.IG.X, S08.FLOPOST.CR.X.KG.X |
| K-11.5 | 505-Seitenmittel | ohne Prä: IG 2, KG 2 · ohne Post: IG 3, KG 2 | S08.FLOPRE.CM.X.IG.X, S08.FLOPRE.CM.X.KG.X, S08.FLOPOST.CM.X.IG.X, S08.FLOPOST.CM.X.KG.X |
| K-11.5 | Standweitsprung | ohne Prä: IG 0, KG 0 · ohne Post: IG 2, KG 2 | S08.FLOPRE.SBJ.X.IG.X, S08.FLOPRE.SBJ.X.KG.X, S08.FLOPOST.SBJ.X.IG.X, S08.FLOPOST.SBJ.X.KG.X |

**K-11.6 Bestwert-Bias, gemessen (S11): Δ = best(V1, V2, V3) − best(V1, V2) über Spieler mit drei gültigen Versuchen, Mittel und Mittel/SESOI, nur deskriptiv:**

| Kennung | Zielgröße | prä | post | Kennung der Ergebnisdatei |
|---|---|---|---|---|
| K-11.6 | Sprint 5 m | n = 6, −0,0283 s (−1,79 × SESOI) | n = 12, −0,0058 s (−0,45 × SESOI) | S11.N.Z05.PRE.ALL.X, S11.DMEAN.Z05.PRE.ALL.X, S11.DSESOI.Z05.PRE.ALL.X, S11.N.Z05.POST.ALL.X, S11.DMEAN.Z05.POST.ALL.X, S11.DSESOI.Z05.POST.ALL.X |
| K-11.6 | Sprint 10 m | n = 10, −0,0050 s (−0,23 × SESOI) | n = 7, −0,0186 s (−0,97 × SESOI) | S11.N.Z10.PRE.ALL.X, S11.DMEAN.Z10.PRE.ALL.X, S11.DSESOI.Z10.PRE.ALL.X, S11.N.Z10.POST.ALL.X, S11.DMEAN.Z10.POST.ALL.X, S11.DSESOI.Z10.POST.ALL.X |
| K-11.6 | Sprint 30 m | n = 17, −0,0159 s (−0,25 × SESOI) | n = 12, −0,0075 s (−0,14 × SESOI) | S11.N.Z30.PRE.ALL.X, S11.DMEAN.Z30.PRE.ALL.X, S11.DSESOI.Z30.PRE.ALL.X, S11.N.Z30.POST.ALL.X, S11.DMEAN.Z30.POST.ALL.X, S11.DSESOI.Z30.POST.ALL.X |
| K-11.6 | 505 links | n = 4, −0,0325 s (−1,43 × SESOI) | n = 0, fehlend (zu wenige Werte) | S11.N.CL.PRE.ALL.X, S11.DMEAN.CL.PRE.ALL.X, S11.DSESOI.CL.PRE.ALL.X, S11.N.CL.POST.ALL.X, S11.DMEAN.CL.POST.ALL.X, S11.DSESOI.CL.POST.ALL.X |
| K-11.6 | 505 rechts | n = 4, −0,0750 s (−3,22 × SESOI) | n = 0, fehlend (zu wenige Werte) | S11.N.CR.PRE.ALL.X, S11.DMEAN.CR.PRE.ALL.X, S11.DSESOI.CR.PRE.ALL.X, S11.N.CR.POST.ALL.X, S11.DMEAN.CR.POST.ALL.X, S11.DSESOI.CR.POST.ALL.X |
| K-11.6 | Standweitsprung | n = 12, +0,75 cm (+0,23 × SESOI) | n = 3, +0,33 cm (+0,11 × SESOI) | S11.N.SBJ.PRE.ALL.X, S11.DMEAN.SBJ.PRE.ALL.X, S11.DSESOI.SBJ.PRE.ALL.X, S11.N.SBJ.POST.ALL.X, S11.DMEAN.SBJ.POST.ALL.X, S11.DSESOI.SBJ.POST.ALL.X |

## K-12 Einschluss je Spieler, Reifestatus, Bestwerte und Adhärenz (Abb. 1, Abb. 2, Tab. H2)

Eingeschlossen ist jeder zugeteilte Spieler (ITT, CONSORT Box 6). Ein fehlender Wert schließt den Spieler nur aus der Zielgröße aus, in der er fehlt, keine Fortschreibung. ✓ = im ITT-Set der Zielgröße (BEST prä, BEST post und %PAH vorhanden). Die Zählung je Spalte ergibt die Nenner in K-04 und K-06. Bestwerte prä und post der konfirmatorischen Zielgrößen und %PAH je Spieler sind die Einzelpunkte von Abb. 2 (Post dort auf den mittleren %PAH des Sets adjustiert, K-06.5). Adhärenz GANZ je IG-Spieler für Tab. H2.

| Kennung | Code | Gruppe | Verein | %PAH | 5 m | 10 m | 30 m | 505 L | 505 R | 505 M | SBJ | BEST 30 m prä | BEST 30 m post | BEST 505 M prä | BEST 505 M post | BEST SBJ prä | BEST SBJ post | GANZ | Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K-12 | BW-01 | IG | B | 91,85 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,530 | 4,540 | 2,555 | 2,545 | 222 | 218 | 0 | — |
| K-12 | BW-02 | IG | B | 97,15 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,690 | 4,700 | 2,470 | 2,420 | 228 | 235 | 12 | — |
| K-12 | BW-04 | IG | B | 94,99 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,630 | 4,680 | 2,425 | 2,455 | 251 | 250 | 6 | — |
| K-12 | BW-05 | IG | B | 94,21 | ✓ | – | ✓ | ✓ | – | – | ✓ | 4,420 | 4,540 | 2,475 | – | 238 | 237 | 7 | — |
| K-12 | BW-06 | IG | B | 87,07 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,500 | 4,510 | 2,575 | 2,590 | 243 | 244 | 2 | — |
| K-12 | BW-07 | IG | B | 92,49 | – | – | – | – | – | – | – | 4,290 | – | 2,455 | – | 247 | – | 6 | Post nicht angetreten |
| K-12 | BW-08 | IG | B | 96,75 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,450 | 4,440 | 2,415 | 2,480 | 246 | 239 | 9 | — |
| K-12 | BW-09 | IG | B | 92,25 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,820 | 4,780 | 2,530 | 2,550 | 237 | 236 | 7 | — |
| K-12 | BW-10 | IG | B | 94,09 | ✓ | – | ✓ | ✓ | ✓ | ✓ | ✓ | 4,550 | 4,510 | 2,505 | 2,425 | 207 | 202 | 5 | — |
| K-12 | BW-11 | IG | B | 92,73 | ✓ | – | ✓ | ✓ | – | – | ✓ | 4,890 | 4,890 | – | 2,530 | 222 | 210 | 2 | — |
| K-12 | BW-21 | IG | B | 90,74 | – | – | – | – | – | – | – | 5,000 | – | 2,610 | – | 223 | – | nicht erhebbar | Post nicht angetreten |
| K-12 | HL-01 | IG | A | 98,24 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,660 | 4,720 | 2,485 | 2,550 | 236 | 237 | 8 | — |
| K-12 | HL-02 | IG | A | 97,00 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,090 | 4,240 | 2,195 | 2,305 | 251 | 238 | 8 | — |
| K-12 | HL-03 | IG | A | 96,79 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,220 | 4,350 | 2,430 | 2,505 | 248 | 240 | 9 | — |
| K-12 | HL-05 | IG | A | 95,26 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,250 | 4,300 | 2,450 | 2,420 | 232 | 216 | 0 | — |
| K-12 | HL-06 | IG | A | 96,13 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,510 | 4,490 | 2,410 | 2,505 | 243 | 243 | 0 | — |
| K-12 | HL-07 | IG | A | 96,48 | ✓ | ✓ | ✓ | – | ✓ | – | ✓ | 4,480 | 4,790 | – | 2,365 | 255 | 243 | 7 | — |
| K-12 | HL-08 | IG | A | 94,85 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,480 | 4,580 | 2,480 | 2,380 | 245 | 245 | 4 | — |
| K-12 | VS-01 | KG | C | 90,04 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,910 | 4,790 | 2,460 | 2,445 | 228 | 224 | – | — |
| K-12 | VS-02 | KG | C | 86,45 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,890 | 4,910 | 2,505 | 2,560 | 208 | 197 | – | — |
| K-12 | VS-03 | KG | C | 90,21 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,940 | 5,230 | 2,605 | 2,625 | 235 | 226 | – | — |
| K-12 | VS-04 | KG | C | 88,04 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5,020 | 4,990 | 2,615 | 2,530 | 210 | 212 | – | — |
| K-12 | VS-05 | KG | C | 87,23 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,950 | 5,030 | 2,540 | 2,575 | 228 | 225 | – | — |
| K-12 | VS-06 | KG | C | 92,99 | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,450 | 4,500 | 2,320 | 2,290 | 259 | 262 | – | — |
| K-12 | VS-07 | KG | C | 88,13 | – | – | – | – | – | – | – | 5,190 | – | 2,520 | – | 219 | – | – | Post nicht angetreten |
| K-12 | VS-08 | KG | C | 91,66 | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5,440 | 5,220 | 2,600 | 2,685 | 202 | 213 | – | — |
| K-12 | VS-10 | KG | C | 90,39 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,640 | 4,860 | 2,405 | 2,410 | 232 | 220 | – | — |
| K-12 | VS-16 | KG | C | 87,53 | – | – | – | – | – | – | – | 4,920 | – | – | – | 226 | – | – | Post nicht angetreten |
| K-12 | VS-17 | KG | C | 94,92 | – | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 4,660 | 4,760 | 2,510 | 2,615 | 258 | 235 | – | — |
| K-12 | VS-18 | KG | C | fehlend | – | – | – | – | – | – | – | 5,070 | 5,180 | – | 2,540 | 209 | 227 | – | ohne %PAH |
| K-12 | VS-11 | KG | C | 93,03 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 5,040 | 4,640 | 2,695 | 2,585 | 204 | 218 | – | — |

Zahl der Spieler mit %PAH (K-12.1): IG 18 · KG 12 (S05.NPAH.PAH.PRE.IG.X, S05.NPAH.PAH.PRE.KG.X).

## Abdeckung

Kennungen der Ergebnisdatei: 3559, davon in diesem Blatt verwendet: 1843. Kennungen mit Berichtsort Text (T) nach dem Umfangsdokument: 581, davon hier ohne Zeile: 0. Nicht verwendete Kennungen sind Zwischenwerte (I), Mittelwerte der Versuche und Bestwerte der deskriptiven Zielgrößen je Spieler, Setmitgliedschaften der Per-Protokoll-Mengen und Steuergrößen. Sie bleiben in der Ergebnisdatei abrufbar.

Werte mit fehlendem Eintrag in der Ergebnisdatei erscheinen als „fehlend (Grund)“ nach Spezifikation G.1 Nr. 4. Semikolons kommen in diesem Blatt nicht vor.

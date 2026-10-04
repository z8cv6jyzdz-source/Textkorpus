# Spezifikation der Rechenschritte

**Bachelorarbeit U15-Plyometrie · DSHS Köln · Stand 24.09.2026 · freigegeben (F1), Nachtrag 1 und Nachtrag 2 (24.09.2026), Nachtrag 3 (25.09.2026)**
Gehört zu `01_Verfahren\Auswertungsverfahren_2026-09-24` (Phase 2, Schritte 2.1 bis 2.3) und zur Maßnahme L6. Anlagen unter gleichem Namensstamm: `_Kennungen.csv`, `_Konstanten.csv`, `_Koeffizienten_KR.csv`, `_Vokabular.csv`, `_Fragebogen.csv`, `_Referenzdaten.csv`, `_Referenzdaten_Daten.csv`, `_Zahlenliste.csv`.

---

## Deckblatt (Freigabe F1, Nachtrag 1 und Nachtrag 2 am 24.09.2026, Nachtrag 3 am 25.09.2026)

**Grundlage: Ethikantrag vom 16.06.2026 und Auswertungsplan vom 12.09.2026.** Die Spezifikation beschreibt jede Rechnung so, dass eine zweite Instanz sie ohne Projektzugriff in R umsetzen kann. Sie enthält keine Ergebnisse und keine Zahl aus den Studiendaten (Nachweis Teil H).

**Methodische Kernfestlegungen**

| Bereich | Festlegung | Status |
|---|---|---|
| Aggregation | Bestwert der gültigen Versuche, Mittelwert der Versuche als Sensitivität. 505 als Mittel der beiden Seiten-Bestwerte, nur wenn beide Seiten gültig sind | Antrag, Plan |
| Reifestatus | %PAH nach Khamis & Roche (1994), Tab. 1 unverändert, Erratum nicht verwendet (O1), lineare Interpolation (O2), fehlende Elterngröße → %PAH fehlend (K2) | Antrag, nachträglich |
| Analysesets | ITT = Prä, Post und %PAH vorhanden. Per-Protokoll ab 6 von 12 Einheiten „ganz“ (5 und 7 als Sensitivität), Antragskriterium ab 9 nur als Einzelwerte. Inferenz nur ab 8 Spielern je Gruppe | Antrag, Plan |
| Hauptanalyse | ANCOVA Post ~ Gruppe + Prä + %PAH für 30 m, 505-Seitenmittel und Standweitsprung. H0 abgelehnt, wenn mindestens eine Zielgröße p < 0,05 in günstiger Richtung zeigt, ohne Adjustierung | Antrag, K23, P6 |
| Effektstärke | g = b1 / gepoolte Prä-SD × J, J = 1 − 3/(4·df − 1), df = n − 2, KI aus dem KI von b1 (O3). Unadjustiert: Differenz der Post-Mittel (O4) | Antrag, Plan, O3, O4 |
| Voraussetzungen | Shapiro-Wilk und Q-Q-Diagramm, Brown-Forsythe mit Residuen-SD je Gruppe, zwei Steigungsmodelle, Linearität grafisch. Nur berichten, kein Wechsel (O7) | Plan, nachträglich |
| Messgüte | TE = gepoolte Innerspieler-SD (O5), S = SD der Bestwerte aller Spieler (O6), SESOI = 0,2 · S, TE-KI aus χ² (K12), CV | Plan, nachträglich |
| Sensitivität | Mittelwert, PP5, PP7, Änderungswert, ohne %PAH, Familiarisierung als Kovariate, Variante a deskriptiv. Bootstrap-KI für alle drei, nachträglich (O8, N3) | Plan, O8, N3 |
| Poweranalyse | Standardweg: df2 = N − 4, λ = d²·n_IG·n_KG/N, MDES bei Power 0,80, ohne R² und ohne Faktor SE (O9) | Plan, O9 |
| Adhärenz | Hauptzählung = Meldungen „ganz“, Nenner 12 × zugeteilte Spieler. Fallkorrekturen CASE 59 und 70 → BW-06, CASE 140, 158, 165, 190, 206 → BW-04. Untergrenzen wochengedeckelt und nach distinkten Nummern | Plan, K9 |
| Umfang | Nur Größen, die berichtet werden oder die eine Prüfung oder die Darstellung braucht, 1.535 Kennungen. Stichprobenbeschreibung in der Analysepopulation ANA | nachträglich, Nachtrag 2 |

**Am 24.09.2026 entschieden (Teil F.2):** O1 bis O9 wie oben, O10 entfällt. K1 bis K3 Alter, Elterngröße, Einheiten · K4, K5, K8 Auslöse- und Abbruchregeln · K6, K7 Meldezeitpunkt, Dubletten · K9, K10 Umsetzungsrate, sRPE-Load · K12 bis K16 Messgüte · K17 bis K24 Modelle und Prüfverfahren · K26 bis K30 Deskription und Anteile · K11 Reifebänder offen · K25 entfällt mit O9.

**Mit F1 bestätigt (bei der Ausarbeitung präzisiert, Teil F.3):** P1 Fisher-KI mit ungerundetem Quantil · P2 „durchgeführt“ = ganz oder teilweise · P3 Veröffentlichungsabstand nach Kalenderwoche · P4 Wochen- und Blockanteile ohne Deckel · P5 Vorab-Prüfung in der Menge mit %PAH · P6 H0-Entscheidung bei fehlenden Tests · P7 Poweranalyse für alle Zielgrößen und unabhängig von der Fallzahlregel.

**Nachtrag 2 (Teil F.7):** Ausgabe auf die berichteten und für Prüfungen gebrauchten Größen beschränkt · Menge ANA für die Stichprobenbeschreibung · Mittel der Kovariaten im ITT-Set als Ausgabe · P7 eingeschränkt, P1 und P3 ohne Anwendung.

**Nachtrag 3 (Teil F.8):** vier Klarstellungen aus der Code-Durchsicht der Phase 6.2, nach bestandenem Abgleich beider Implementierungen: Vorrang des Grunds „Eingang fehlt“ in S05 · Bezugsmenge von Median und Mittel der Adhärenz in N4.3 · Rangkriterium der Designmatrix · Dateinamen der Grafiken der Gegenprobe. Keine Regel der Hauptanalyse, keine Kennung und kein Referenztest ändert sich.

**Entfallen:** R²max, Faktor SE und R²-Spanne der Poweranalyse, partielles η², mit Nachtrag 2 die Größen nach Teil F.7. **Offen:** Reifebänder. **Nicht aufgenommen:** zeitgleiche Meldungen verschiedener Spieler, Modalwert des Untergrunds, Freitextkategorien. **Prüfhinweis:** R ist berichtete Rechenumgebung nach Entscheidung des Verfassers (antragskonform, ohne Betreuerfreigabe). F1: Verfasser, 24.09.2026. Nachtrag 2: Verfasser, 24.09.2026. Nachtrag 3: Verfasser, 25.09.2026. Referenztests R01 bis R13 vor der Studienrechnung (Teil G).

---

## 0 Kopf

### 0.1 Zweck und Geltung

Die Spezifikation übersetzt den Auswertungsplan vom 12.09.2026 in Rechenregeln. Eine zweite Instanz soll allein nach diesem Dokument und seinen Anlagen die gesamte Auswertung in R umsetzen können. Das Dokument setzt den Plan um und trifft keine eigenen methodischen Entscheidungen. Wo der Plan eine Größe offen ließ, hat der Verfasser am 24.09.2026 entschieden (O1 bis O10, K1 bis K30). Wo bei der Ausarbeitung eine Regel nur präzisiert werden musste, steht sie als P1 bis P7 zur Bestätigung mit der Freigabe F1. Alle diese Punkte sind als „nachträglich“ gekennzeichnet und in Teil F gesammelt.

Die Spezifikation enthält keine Ergebnisse und keine Zahlen aus den Studiendaten. Alle Zahlen im Text sind Regeln, Schwellen, Formelkonstanten oder Werte aus Originalquellen mit Fundstelle (Nachweis in Teil H).

Bei Widerspruch zwischen diesem Dokument und einer anderen Datei gilt dieses Dokument. Ist eine Regel unklar oder fehlt sie, wird angehalten und rückgefragt. Die Antwort kommt als datierter Nachtrag zur Spezifikation.

### 0.2 Quellen und Statuslegende

Grundlage sind ausschließlich: Ethikantrag vom 16.06.2026 (Studienprotokoll) · Auswertungsplan vom 12.09.2026 · Projektanweisungen Fassung 12, § 3.1 und § 11 (im Folgenden PA) · Fragebogenauswertung vom 12.09.2026 (im Folgenden FA) · Codebuch Fragebogen A (SoSci test546007, Stand 24.08.2026) · Versuchszahl-Protokollbefund vom 09.09.2026 · Originalquellen mit Seiten- oder Tabellenangabe (Literatur in Teil I).

| Status | Bedeutung |
|---|---|
| Antrag | im Ethikantrag festgelegt |
| Plan 12.09. | im Auswertungsplan, in der Fragebogenauswertung oder in PA § 3.1 und § 11 festgelegt, vor Kenntnis der Kontrollgruppenwerte |
| nachträglich | nach dem Sperrdatum 15.09.2026 festgelegt (Verfasser 24.09.2026) oder bei der Ausarbeitung präzisiert (P1 bis P7). Im Bericht als nachträglich zu kennzeichnen |
| offen | nicht entschieden. Wird nicht gerechnet |

### 0.3 Kennungsschema

Jede Ausgabe trägt genau eine Kennung aus sechs Feldern, getrennt durch Punkte:

`S<nn>.<GRÖSSE>.<ZIEL>.<ZEIT>.<MENGE>.<VARIANTE>`

Nicht zutreffende Felder stehen als `X`. Zeichenvorrat: Großbuchstaben A–Z, Ziffern 0–9, Bindestrich nur innerhalb von Spielercodes.

| Feld | Werte |
|---|---|
| S<nn> | Rechenschritt S01 bis S19 |
| GRÖSSE | Kurzname der Größe. Bedeutung und Einheit je Kennung in Anlage `_Kennungen.csv`, Spalten `beschreibung` und `einheit` |
| ZIEL | `Z05` Sprint 5 m · `Z10` Sprint 10 m · `Z30` Sprint 30 m · `SBJ` Standweitsprung · `CL` 505 links · `CR` 505 rechts · `CM` 505 Seitenmittel · `AGE` Alter · `HGT` Körperhöhe · `MASS` Körpermasse · `PAH` %PAH · `FAM` Familiarisierung · `ADH` Adhärenz · `CR10` Anstrengung CR-10 · `LOAD` sRPE-Load · `FB` Fragebogen allgemein |
| ZEIT | `PRE` · `POST` · `DIFF` (Post minus Prä) · Programmwoche `W1` bis `W6` |
| MENGE | `ALL` alle Spieler · `IG` · `KG` · `VA` `VB` `VC` Verein A, B, C · Analysesets `ITT` `PP5` `PP6` `PP7` `AK9` `FAMS` für Analysen über beide Gruppen, mit angehängtem `IG` oder `KG` für einen Gruppenteil (Beispiel `ITTIG`) · `BASE` Spieler mit Prä-Bestwert der Zielgröße, mit Gruppenanhang (`BASEIG`) · `BPAH` Spieler mit Prä-Bestwert der Zielgröße und %PAH, ohne oder mit Gruppenanhang · `ANA` Analysepopulation nach S08 Regel 11, mit Gruppenanhang (`ANAIG`) · je Spieler `P` gefolgt vom Code (`P<Code>`) |
| VARIANTE | `HAUPT` Bestwert und Hauptmodell · `MW` Mittelwert der Versuche · `AEND` Änderungswertmodell · `OPAH` ohne %PAH · `FAMB` mit Familiarisierung · `F1` `F2` Familiarisierung mit einem oder zwei Terminen · Status einer Meldung `GANZ` `TEILW` `GARN` · Adhärenzzählungen `GANZ` `GT` (ganz oder teilweise) `WOCAP` `DIST` · Ausfallkategorien `TECH` `ZEIT` `FEHL` `FALSCH` `NANG` `AUSL` · Prüfmodelle `SLPRE` `SLPAH` · `BOOT` · Erwartungswerte `D006` `D011` `D037` `D093` · in S08 bei Mitgliedschaften der Setname |

Beispiele: `S04.BEST.Z30.PRE.P<Code>.X` Bestwert 30 m prä je Spieler · `S05.PAH.PAH.PRE.P<Code>.X` %PAH je Spieler · `S10.TE.CM.PRE.ALL.X` typischer Messfehler des Seitenmittels prä · `S13.B1.Z30.X.ITT.HAUPT` adjustierte Differenz 30 m.

Spielerkennungen sind Muster. In der Anlage steht `P<Code>`, die Instanz ersetzt `<Code>` durch den Analysecode jedes Spielers der Menge in Spalte `spielermenge`: `ALLE` alle Spieler der Personendaten · `IG` alle IG-Spieler der Personendaten · `AK9` Spieler im Set AK9 der jeweiligen Zielgröße. So wird in der Spezifikation keine Fallzahl sichtbar. Jede Kennung erscheint in der Ergebnisdatei genau einmal. Die vollständige Liste mit Einheit und Beschreibung steht in `_Kennungen.csv`, sie ist maßgeblich. In den Schritten unten sind Kennungsfamilien mit geschweiften Klammern zusammengefasst: `{A,B}` steht für beide Werte, `{…}` für die in der Anlage genannten Werte.

### 0.4 Eingang

Maßgeblich ist das Datenwörterbuch des eingefrorenen Datenstands (Phase 1). Die Variablennamen hier sind vorläufig und werden in Phase 1 abgeglichen.

1. **Versuchsdaten**, eine Zeile je Spieler × Zeitpunkt × Test × Seite × Versuch: `Code` · `Zeitpunkt` (prä, post) · `Test` (Sprint_5m, Sprint_10m, Sprint_30m, COD_505, Standweitsprung) · `Seite` (L oder R beim 505, sonst leer oder „–“) · `Versuch` (1, 2, 3) · `Wert` (Zeiten in s, Sprungweite in cm) · `ungültig` (leer oder Eintrag) · `Bemerkung` (festes Vokabular). Eine im Datenstand etwa vorhandene berechnete Spalte `gilt` wird nicht verwendet.
2. **Personendaten**, eine Zeile je Spieler: `Code` · `Verein` (A, B, C) · `Gruppe` (IG, KG) · `Alter_prae` (Dezimaljahre am Prätesttag, Definition in S05) · `Koerperhoehe_prae` (cm) · `Koerpermasse_prae` (kg) · `Groesse_Mutter` und `Groesse_Vater` (cm) · `Familiarisierung` (1, 2 oder leer) · `Status` (ausgewertet, nicht angetreten). Eine etwa vorhandene berechnete Spalte %PAH wird nicht verwendet.
3. **Fragebogen-Rohexport A** ohne Freitexte: `CASE` · `STARTED` (Zeitstempel JJJJ-MM-TT hh:mm:ss) · `H010` · `H002` · `H003` · `H004` · `H005` · `H006` · `H007` · `H008` · `H009`. Weitere Metadatenspalten dürfen vorhanden sein und werden nicht verwendet.
4. **Zuordnungstabelle Fragebogen** aus Phase 1 (Schritt 1.2): Listenlabel (HL-01 bis HL-08, BW-01 bis BW-14) → Analysecode sowie für jeden IG-Spieler das Merkmal `kein_Listenplatz` (ja, nein).

### 0.5 Rechenkonventionen

1. Keine Rundung in Zwischen- und Endwerten. Ausgabe ungerundet mit mindestens zwölf signifikanten Stellen.
2. Standardabweichung mit Nenner n − 1. Gepoolte SD zweier Gruppen: SD_pool = √( ((n_IG − 1)·s_IG² + (n_KG − 1)·s_KG²) / (n_IG + n_KG − 2) ).
3. Fehlende Werte werden nie ersetzt und nie fortgeschrieben (keine LOCF, PA § 11.7). Eine Größe, deren Eingang fehlt, ist fehlend und wird mit Grund ausgegeben.
4. Gruppenvariable G: IG = 1, KG = 0. Differenzen immer IG minus KG.
5. Richtung: Günstig für die IG ist bei Zeiten (Z05, Z10, Z30, CL, CR, CM) ein negativer Wert, beim Standweitsprung ein positiver.
6. Konfidenzintervalle 95 %, zweiseitig. α = 0,05 (Antrag § 1).
7. Quantile (Median, Quartile, Bootstrap-Grenzen) nach Typ 7: Für sortierte Werte x(1) ≤ … ≤ x(n) und Anteil p ist h = (n − 1)·p + 1, das Quantil x(⌊h⌋) + (h − ⌊h⌋)·(x(⌊h⌋+1) − x(⌊h⌋)). Bei h = n gilt x(n).
8. p-Werte exakt aus der jeweiligen Verteilung, zweiseitig, ohne Schwellenangabe.
9. Nullstellensuche mit absoluter Toleranz 1e-10.
10. Abbruch mit Meldung statt stiller Korrektur bei unbekannten Kategorien, doppelten Schlüsseln, Werten außerhalb des zulässigen Formats und jedem Widerspruch zu einer Regel dieses Dokuments.
11. Eine Analyse, deren Designmatrix nicht vollen Rang hat, wird nicht gerechnet. Ihre Kennungen werden als fehlend mit Grund ausgegeben. Der Rang wird nach einer QR-Zerlegung mit der Toleranz 1e-7 auf der spaltenskalierten Designmatrix bestimmt oder mit einem gleichwertigen Kriterium (Nachtrag 3, N5.3, Klarstellung).
12. Verteilungsquantile werden ungerundet aus der Verteilung berechnet: t_df(p) für die t-Verteilung, F_df1,df2(p) für die zentrale F-Verteilung, χ²_df(p) für die χ²-Verteilung, z_p für die Standardnormalverteilung, jeweils das p-Quantil.
13. Eine Statistik, die mehr Werte verlangt, als vorhanden sind (etwa eine SD bei n < 2 oder ein Mittel bei n = 0), ist fehlend mit Grund. Zahlen (n, Anzahlen) werden immer ausgegeben, auch wenn sie 0 sind.

---

## Teil A · Aufbereitung

### S01 Einlesen und Strukturprüfung

**Status:** Plan 12.09. (Auswertungsverfahren 1.3). Regeln hier ausgeschrieben.
**Zweck:** Eingang auf Form und Vollständigkeit prüfen, bevor gerechnet wird.
**Eingang:** alle Dateien aus 0.4.
**Regel:**
1. SHA-256-Prüfsummen aller Eingangsdateien gegen die Liste des Datenstands.
2. Versuchsdaten: Zeitpunkt ∈ {prä, post} · Test ∈ {Sprint_5m, Sprint_10m, Sprint_30m, COD_505, Standweitsprung} · Seite ∈ {L, R} genau dann, wenn Test = COD_505 · Versuch ∈ {1, 2, 3} · Schlüssel (Code, Zeitpunkt, Test, Seite, Versuch) eindeutig · Wert leer oder eine Zahl größer 0 · jeder Code steht in den Personendaten.
3. Personendaten: Code eindeutig · Verein ∈ {A, B, C} · Gruppe IG genau dann, wenn Verein ∈ {A, B}, sonst KG (Auswertungsplan § 5.4 Nr. 3) · Familiarisierung ∈ {1, 2, leer} · Status ∈ {ausgewertet, nicht angetreten}.
4. Fragebogen: CASE eindeutig · H010 ∈ {1, …, 22} · H002 = 1 · H003 ∈ {1, …, 12} · H004 ∈ {1, 2, 3} · H005 ∈ {1, …, 11} · H006 ∈ {1, …, 5} · H007, H008, H009 ∈ {1, 2} (Codebuch, Anlage `_Fragebogen.csv`). Jeder andere Wert, auch ein leerer Wert oder ein Fehlkode, ist ein Verstoß. Der Export enthält nach FA § 1 nur vollständig bearbeitete Fragebögen.
**Ausgabe:** `S01.N.X.X.{ALL,IG,KG,VA,VB,VC}.X` Zahl der Spieler in den Personendaten · `S01.NZEIL.X.X.ALL.X` Zeilen der Versuchsdaten · `S01.NMELD.FB.X.ALL.X` Zeilen des Fragebogens.
**Entscheidungsregel:** Jede Verletzung führt zum Abbruch mit Meldung.

### S02 Gültigkeit der Versuche

**Status:** Plan 12.09. (Auswertungsplan § 2 B0.2, PA § 11.8). Abschnittsregel nachträglich (K4).
**Zweck:** Festlegen, welcher Versuch in die Auswertung eingeht.
**Eingang:** Versuchsdaten.
**Regel:**
1. gültig_roh = 1, wenn `Wert` vorhanden und `ungültig` leer ist, sonst 0.
2. Auslöseprüfung Sprint. Ein Lauf ist die Menge der Zeilen mit gleichem Code, Zeitpunkt und Versuch über Sprint_5m, Sprint_10m und Sprint_30m. Die Distanzen sind 5, 10 und 30 m. Für jeden Lauf werden die Teilzeiten mit gültig_roh = 1 nach Distanz geordnet. Abschnitte liegen zwischen aufeinanderfolgenden vorhandenen Teilzeiten, der erste beginnt bei 0 m mit t = 0. Abschnittszeit Δt = t_j − t_(j−1), Abschnittsgeschwindigkeit v = Δd/Δt in m/s. Ist ein Δt ≤ 0 s oder ein v > 10,0 m/s, gilt der Lauf als auslösegestört, und alle seine Teilzeiten sind ungültig.
3. gültig = 1, wenn gültig_roh = 1 und der Versuch nicht zu einem auslösegestörten Lauf gehört, sonst 0.
**Ausgabe:** `S02.NAUSL.X.{PRE,POST}.ALL.X` Zahl auslösegestörter Läufe · `S02.NGUELT.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.ALL.X` Zahl gültiger Versuche.
**Hinweis:** Dass ein Lauf über die gleiche Versuchsnummer in den drei Sprinttests gebildet wird, ist im Datenwörterbuch zu bestätigen.

### S03 Ausfallkategorien

**Status:** Plan 12.09. (Auswertungsplan § 2 B0.4, PA § 3.1, Versuchszahl-Protokollbefund § 3). K5 nachträglich.
**Zweck:** Jeden ungültigen Versuch einem Ausfallmechanismus zuordnen.
**Eingang:** Versuchsdaten, S02, Status.
**Regel:** Jede Zeile mit gültig = 0 erhält genau eine Kategorie, in dieser Reihenfolge geprüft:
1. `NANG` nicht angetreten: Zeitpunkt post und Status des Spielers „nicht angetreten“. Steht in einer solchen Zeile ein Wert, ist das ein Widerspruch (Abbruch).
2. `AUSL` auslösegestört: Zeile ungültig allein durch S02 Regel 2.
3. Sonst nach dem Text in `Bemerkung` gemäß Anlage `_Vokabular.csv`: `TECH` technischer Ausfall der Lichtschranke · `ZEIT` dritter Versuch aus Zeitmangel nicht durchgeführt · `FEHL` nicht wiederholbarer Fehlversuch · `FALSCH` Lichtschranke falsch aufgenommen.
Ein Bemerkungstext, der nicht in der Anlage steht, und eine ungültige Zeile ohne Bemerkung führen zum Abbruch (K5). Schreibvarianten gelten nur, soweit die Anlage sie listet. Das Vokabular wird in Phase 1 vereinheitlicht.
**Ausgabe:** `S03.NKAT.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.{IG,KG}.{TECH,ZEIT,FEHL,FALSCH,NANG,AUSL}` Zahl der Zeilen je Kategorie, `NANG` nur für POST.

### S04 Aggregation je Spieler

**Status:** Antrag § 3 (Standweitsprung „bester von drei Versuchen“, 505 „Mittelwert beider Beinseiten“) · Plan 12.09. (Bestwert auch für Sprint und 505, Mittelwert der Versuche als Sensitivität, Auswertungsplan § 5.9, PA § 11.8).
**Zweck:** Je Spieler, Zeitpunkt und Zielgröße einen Wert bilden.
**Eingang:** gültige Versuche aus S02.
**Regel** je Spieler × Zeitpunkt × Test, beim 505 zusätzlich je Seite:
1. k = Zahl der gültigen Versuche (0 bis 3).
2. Bestwert BEST: Minimum der gültigen Werte bei Zeiten, Maximum beim Standweitsprung. Bei k = 0 fehlend.
3. Mittelwert MEAN: arithmetisches Mittel der gültigen Werte. Bei k = 0 fehlend.
4. 505-Seitenmittel (zwei getrennte Operationen, Auswertungsplan § 5.9): zuerst Versuche einer Seite zum Bestwert, dann Mittel der Seiten. CM_BEST = (CL_BEST + CR_BEST)/2 und CM_MEAN = (CL_MEAN + CR_MEAN)/2, nur wenn beide Seiten k ≥ 1 haben, sonst fehlend. Eine fehlende Seite wird nie durch die andere ersetzt. Vorbild der Regel: Dugdale et al. (2019, Methods, 505COD).
5. Gleichstände: Kein Schritt verwendet den Index des besten Versuchs. Bei Gleichstand ist der Bestwert derselbe Wert. Eine Festlegung ist daher nicht nötig.
**Ausgabe** je Spieler: `S04.K.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.P<Code>.X` · `S04.BEST.{Z05,Z10,Z30,SBJ,CL,CR,CM}.{PRE,POST}.P<Code>.X` · `S04.MEAN.{Z05,Z10,Z30,SBJ,CL,CR,CM}.{PRE,POST}.P<Code>.X`. Einheiten s oder cm.

### S05 Reifestatus %PAH nach Khamis und Roche

**Status:** Antrag § 1 und § 3 (%PAH nach Khamis & Roche, 1994, aus Körperhöhe und Körpermasse des Spielers und Körperhöhe beider Erziehungsberechtigter, kontinuierlich) · Tabellenwahl, Interpolation, Altersdefinition, Einheiten und fehlende Elterngröße nachträglich (O1, O2, K1 bis K3).
**Zweck:** Prozentsatz der prognostizierten Erwachsenengröße je Spieler aus den Rohgrößen.
**Eingang:** `Alter_prae`, `Koerperhoehe_prae`, `Koerpermasse_prae`, `Groesse_Mutter`, `Groesse_Vater`.
**Regel:**
1. Alter (K1): Alter_prae = (Datum der Prätestung − Geburtsdatum) in Tagen / 365,25. Die Berechnung erfolgt in Phase 1 vor dem Einfrieren, das Geburtsdatum ist nicht Teil des Datenstands.
2. Einheiten (K3): Die Koeffizienten gelten für Zoll und Pfund (Khamis & Roche, 1994, S. 505). S_in = Körperhöhe / 2,54 · W_lb = Körpermasse / 0,45359237 · Elterngrößen ebenfalls / 2,54. Konstanten nach NIST SP 811 (2008), Anhang B.8 und Fußnote 22.
3. Elterngröße (Khamis & Roche, 1994, S. 504): MP_in = (Mutter_in + Vater_in) / 2.
4. Gültigkeitsbereich: 4,0 ≤ Alter ≤ 17,5 Jahre (Khamis & Roche, 1994, S. 506). Außerhalb ist %PAH fehlend. Keine Extrapolation.
5. Koeffizienten (O1): Tab. 1 „White Males“ (Khamis & Roche, 1994, S. 505) unverändert, Anlage `_Koeffizienten_KR.csv`. Das Erratum (Pediatrics 95(3), 457, 1995, doi 10.1542/peds.95.3.457) korrigiert nach seinem Crossref-Eintrag Fehler in Tab. 1 und 2. Es liegt nicht vor und wird nicht verwendet.
6. Alter zwischen zwei Zeilen (O2): a_lo = ⌊2·Alter⌋/2 (größte Tabellenzeile ≤ Alter), a_hi = a_lo + 0,5, w = (Alter − a_lo)/0,5. Jeder der vier Koeffizienten c ∈ {β0, β1, β2, β3} wird linear interpoliert: c = (1 − w)·c(a_lo) + w·c(a_hi). Bei w = 0, auch bei Alter = 17,5, gilt die Zeile a_lo allein.
7. Vorhersage (Khamis & Roche, 1994, S. 505): PAS_in = β0 + β1·S_in + β2·W_lb + β3·MP_in.
8. %PAH = 100 · S_in / PAS_in (Antrag § 1: Prozentsatz des prognostizierten Erwachsenenwuchses).
9. Fehlt ein Eingang, auch nur eine Elterngröße, ist %PAH fehlend (K2). Der Grund lautet dann „Eingang fehlt“, auch wenn zugleich das Alter außerhalb des Gültigkeitsbereichs der Regel 4 liegt (Nachtrag 3, N5.1). Die im Original genannten Ersatzwege für eine fehlende Elterngröße (S. 506: Schätzung der fehlenden Größe durch den anwesenden Elternteil, als weniger geeignete Alternative ein veröffentlichter Mittelwert) werden nicht verwendet.
10. Die Anthropometrie der Prätestung ist die einzige Quelle. Post-Anthropometrie gibt es nicht (PA § 11.2).
**Ausgabe** je Spieler: `S05.MP.PAH.PRE.P<Code>.X` (in) · `S05.PAS.PAH.PRE.P<Code>.X` (in) · `S05.PAH.PAH.PRE.P<Code>.X` (%). Zusammenfassung: `S05.NPAH.PAH.PRE.{IG,KG}.X` Zahl der Spieler mit %PAH.
**Referenztest:** Rechenbeispiel Khamis & Roche (1994, S. 507), Anlage `_Referenzdaten.csv` R10.

### S06 Fragebogen A: Dekodierung, Fallkorrekturen, Zuordnung

**Status:** Plan 12.09. (FA § 1 und § 2, PA § 3.1) · K6 bis K8 nachträglich · Regel 8 und Ausgabe nach Nachtrag 2 (F.7).
**Zweck:** Jede Meldung einem Spieler, einem Status, einer Programmwoche und einer CR-10-Stufe zuordnen.
**Eingang:** Rohexport, Anlage `_Fragebogen.csv`, Zuordnungstabelle.
**Regel:**
1. Listenlabel = Label des Werts von H010 laut Codebuch: 1 bis 8 → HL-01 bis HL-08, 9 bis 22 → BW-01 bis BW-14.
2. Fallkorrekturen (FA § 1, PA § 3.1): CASE 59 und 70 erhalten das Listenlabel BW-06. CASE 140, 158, 165, 190 und 206 erhalten das Listenlabel BW-04. Weitere Korrekturen einzelner Meldungen gibt es nicht. Meldungspaare mit abweichendem Inhalt bleiben zwei Meldungen (Verfasser 12.09.).
3. Analysecode = Zuordnungstabelle(Listenlabel). Ein Listenlabel ohne Analysecode, an dem eine Meldung hängt, führt zum Abbruch. Ein Analysecode der KG führt zum Abbruch.
4. Status aus H004: 1 ganz · 2 teilweise · 3 gar nicht.
5. CR-10 = H005 − 1 (Codebuch: Stufen 0 bis 10 auf die Codes 1 bis 11).
6. Meldezeitpunkt = STARTED, als exportierte Ortszeit (K6). Meldedatum = Kalenderdatum von STARTED.
7. Programmwoche nach Kalenderregel, Montag 00:00 bis Sonntag 23:59:59 (FA § 2): W1 20.07. bis 26.07.2026 · W2 27.07. bis 02.08. · W3 03.08. bis 09.08. · W4 10.08. bis 16.08. · W5 17.08. bis 23.08. · W6 24.08. bis 30.08.2026. Eine Meldung außerhalb von W1 bis W6 führt zum Abbruch (K8).
8. entfällt (Nachtrag 2). Keine Ausgabe verwendet die Fensterregel.
9. Dubletten (FA § 1): Zwei Meldungen desselben Analysecodes mit Abstand von höchstens 5 Minuten (STARTED) und identischen Werten in H003 bis H009 bilden ein Dublettenpaar. Jedes solche Paar wird gezählt, auch wenn eine Meldung zu mehreren Paaren gehört. Das Paar wird gekennzeichnet, nicht gelöscht. Jede Meldung zählt (K7, Verfasserregel 12.09.: jede abgegebene Meldung zählt). Zwei Meldungen desselben Codes mit höchstens 5 Minuten Abstand und abweichendem Inhalt bilden ein Sammelmeldungspaar.
**Ausgabe:** `S06.NMELD.FB.X.ALL.X` · `S06.NMELD.FB.X.P<Code>.X` Zahl der zugeordneten Meldungen je IG-Spieler, 0 für Spieler ohne Meldung und ohne Listenplatz · `S06.NKORR.FB.X.ALL.X` korrigierte Meldungen · `S06.NDUBL.FB.X.ALL.X` Dublettenpaare · `S06.NSAMM.FB.X.ALL.X` Sammelmeldungspaare · `S06.NSTAT.FB.X.IG.{GANZ,TEILW,GARN}` Meldungen je Status.

### S07 Adhärenz, Belastung, unerwünschte Ereignisse

**Status:** Antrag § 3 (Anzahl durchgeführter Einheiten, Session-RPE auf der CR-10-Skala) · Plan 12.09. (Zählregeln, Untergrenzen, sRPE-Load, deskriptive Kennwerte, FA § 2 bis § 5 und § 7, PA § 3.1) · K9, K10, P2 und P4 nachträglich · Umfang nach Nachtrag 2 (F.7).
**Zweck:** Adhärenz je IG-Spieler und deskriptive Kennwerte des Monitorings.
**Eingang:** S06, Personendaten, Zuordnungstabelle.
**Mengen:** Meldungen sind alle nach S06 zugeordneten Meldungen. Zugeteilte Spieler sind die IG-Spieler der Personendaten (Menge IG). Status-Mengen: ganz (H004 = 1), teilweise (2), gar nicht (3), ganz oder teilweise (1 oder 2, in der FA „durchgeführt“, P2).
**Regel, Adhärenz** je IG-Spieler der Personendaten:
1. `GANZ` Hauptzählung: Zahl der Meldungen mit Status ganz (PA § 3.1).
2. `GT` Beteiligung: Zahl der Meldungen mit Status ganz oder teilweise.
3. `WOCAP` wochengedeckelt: Summe über W1 bis W6 (Kalenderregel) von min(2, Zahl der Meldungen „ganz“ in der Woche).
4. `DIST` distinkte Einheitennummern: Zahl verschiedener Werte von H003 unter den Meldungen „ganz“.
5. IG-Spieler ohne Meldung erhalten in allen Zählungen 0 (Nichteinhaltung). IG-Spieler mit `kein_Listenplatz` = ja erhalten fehlende Einzelwerte mit Grund „nicht erhebbar“ (K9).
6. Nenner: 12 angebotene Einheiten je Spieler. Umsetzungsrate je Zählung = Summe der Zählung / (12 · n_zugeteilt), mit n_zugeteilt = Zahl der zugeteilten Spieler. Spieler ohne Listenplatz zählen in Summe, Rate, Verteilung, Median und Mittel mit 0 (K9, FA § 4).
7. Verteilung der Zählung `GANZ` über die zugeteilten Spieler: Zahl der Spieler je Wert 0 bis 12 · Schwellenlandschaft = Zahl der Spieler mit Zählung ≥ s für s = 1 bis 12 · Median und Mittel. Für `WOCAP` und `DIST` nur die Zahl der Spieler mit Zählung ≥ 6 und ≥ 9. Dazu die Zahl der Spieler mit mindestens einer Meldung, gleich welchen Status.
**Regel, Zeitstruktur** (FA § 2 und § 4.4):
8. Je Programmwoche (Kalenderregel): Wochenanteil = Meldungen „ganz“ der Woche / (2 · n_zugeteilt) (P4).
9. entfällt (Nachtrag 2).
10. entfällt (Nachtrag 2).
**Regel, Belastung** (Antrag § 3, FA § 5):
11. CR-10 der Meldungen „ganz“: n, M, SD, Median, Min, Max über alle Meldungen der IG, dazu n, M und SD je Programmwoche.
12. sRPE-Load (Foster et al., 2001, im Antrag genannt) nur für Meldungen „ganz“ (K10): Load = CR-10 · Dauer_w mit der Sitzungsdauer der Programmwoche w nach Kalenderregel (Wochenvideo plus Aufwärmvideo, FA § 5): W1 37:09 · W2 36:55 · W3 33:10 · W4 34:48 · W5 39:56 · W6 40:07 (min:s). Dauer in Minuten = Minuten + Sekunden/60. Einheit AU. n, M, SD, Median, Min, Max über alle Meldungen der IG, dazu n, M und SD je Programmwoche.
**Regel, unerwünschte Ereignisse:**
13. Unerwünschte Ereignisse (CONSORT Item 19, Moher et al., 2010, FA § 7): Meldungen mit H007 = 1. Zahl gesamt und je Status sowie Zahl der Spieler mit mindestens einer solchen Meldung. Nur IG, die KG hatte kein Instrument (Antrag § 3).
14. bis 22. entfallen (Nachtrag 2).
**Ausgabe** (vollständig in `_Kennungen.csv`): Adhärenz je Spieler `S07.ADH.ADH.X.P<Code>.{GANZ,WOCAP,DIST}` · Rate `S07.NZUG.ADH.X.IG.X`, `S07.{SUMME,RATE}.ADH.X.IG.{GANZ,GT,WOCAP,DIST}` · Verteilung `S07.{V00,…,V12,GE01,…,GE12,MED,MITT}.ADH.X.IG.GANZ`, `S07.{GE06,GE09}.ADH.X.IG.{WOCAP,DIST}` und `S07.NMELDSP.ADH.X.IG.X` · Zeitstruktur `S07.ANTW.ADH.{W1,…,W6}.IG.GANZ` · Belastung `S07.{N,M,SD,MED,MIN,MAX}.{CR10,LOAD}.X.IG.GANZ` und `S07.{N,M,SD}.{CR10,LOAD}.{W1,…,W6}.IG.GANZ` · unerwünschte Ereignisse `S07.UE.FB.X.IG.{X,GANZ,TEILW,GARN}` und `S07.UESP.FB.X.IG.X`.

---

## Teil B · Populationen und Datenverluste

### S08 Analysesets, Nenner, Teilnehmerfluss

**Status:** Plan 12.09. (Auswertungsplan § 2 B4 und B9, § 5.3, PA § 11.7 und § 11.9) · K27 nachträglich · Regeln 8 und 11 nach Nachtrag 2 (F.7).
**Zweck:** Für jede Analyse festlegen, welche Spieler eingehen, und den Teilnehmerfluss zählen.
**Eingang:** S04, S05, S07, Personendaten.
**Regel:**
1. ITT-Set je Zielgröße Z ∈ {Z05, Z10, Z30, SBJ, CL, CR, CM}: alle Spieler beider Gruppen, bei denen BEST prä, BEST post und %PAH vorhanden sind. Das Set gilt für BEST und für MEAN, weil MEAN genau dann vorhanden ist, wenn BEST vorhanden ist.
2. Rolle der Zielgrößen (Auswertungsplan § 2, PA § 11.9): konfirmatorisch Z30, CM, SBJ · deskriptiv Z05, Z10, CL, CR. Für die deskriptiven Zielgrößen wird kein Modell gerechnet. Die Sets der Regeln 4 bis 6 werden nur für die konfirmatorischen Zielgrößen gebildet.
3. Fallzahlregel (PA § 11.9): Eine Analyse ist inferenzfähig, wenn in ihrem Set n_IG ≥ 8 und n_KG ≥ 8 gilt. Sonst werden für sie nur n, M, SD und Einzelwerte ausgegeben, ohne p-Wert, ohne Konfidenzintervall und ohne Effektstärke. Die Regel gilt für jede Analyse aus S13 bis S17 und für S19. Ausgabe als Merkmal INF (1 inferenzfähig, 0 nicht). Die Analysen `MW`, `AEND` und `OPAH` haben das Merkmal INF des ITT-Sets.
4. Per-Protokoll-Sets (PA § 11.7, Schwelle ≥ 6 festgelegt am 11.09.2026, ≥ 5 und ≥ 7 als Sensitivität): PP_s = ITT-Set ∩ (alle KG-Spieler ∪ IG-Spieler mit GANZ ≥ s), s ∈ {5, 6, 7}. IG-Spieler mit fehlender Adhärenz gehören zu keinem PP-Set. Der KG-Teil jedes PP-Sets ist der KG-Teil des ITT-Sets und wird nicht gesondert ausgegeben.
5. Antragskriterium (Antrag § 8: Adherence unter 75 % der vorgesehenen Einheiten): AK9 = IG-Spieler des ITT-Sets mit GANZ ≥ 9. Nur Einzelwerte, keine Inferenz (Auswertungsplan § 5.3).
6. Familiarisierungsset FAMS je Zielgröße: ITT-Set ohne Spieler mit fehlender Familiarisierung.
7. Mitgliedschaft je Spieler als Merkmal 0 oder 1: ITT für alle sieben Zielgrößen, PP5, PP6, PP7, AK9 und FAMS für die konfirmatorischen Zielgrößen.
8. Teilnehmerfluss je Gruppe und je Verein: zugeteilt (Personendaten) · mit Prätestdaten (mindestens ein gültiger Prä-Versuch in irgendeinem Test) · Status ausgewertet · Status nicht angetreten. Nur je Gruppe: je Zielgröße im ITT-Set · je Zielgröße Zahl der Spieler ohne BEST prä und ohne BEST post · Zahl der Spieler ohne %PAH. Die Gründe werden unabhängig gezählt, ein Spieler kann mehrere haben.
9. Klassen nach CONSORT Box 6 (PA § 11.7), je Gruppe gezählt, nicht exklusiv: Nichteinhaltung = IG-Spieler mit GANZ < 6, einschließlich GANZ = 0, Spieler mit fehlender Adhärenz zählen hier nicht · davon ohne jede Meldung · Instrumentenfehler = IG-Spieler mit `kein_Listenplatz` = ja · fehlende Kovariate = %PAH fehlend · nicht angetreten = Status „nicht angetreten“.
10. Erhebungs- und Attritionsanteile (K27): je Zielgröße und Gruppe sowie gesamt Zahl der Spieler mit BEST prä und BEST post geteilt durch Zahl der zugeteilten Spieler. Auf Teilnehmerebene: Status ausgewertet geteilt durch zugeteilt.
11. Analysepopulation ANA (Nachtrag 2): alle Spieler, die im ITT-Set mindestens einer der sieben Zielgrößen stehen, je Gruppe. Sie dient nur der Stichprobenbeschreibung in S12 Regel 1.
**Ausgabe:** Setgrößen `S08.N.{Z05,Z10,Z30,SBJ,CL,CR,CM}.X.{ITTIG,ITTKG}.X` und `S08.N.{Z30,CM,SBJ}.X.{PP5IG,PP6IG,PP7IG,AK9IG,FAMSIG,FAMSKG}.X` · `S08.INF.{Z30,CM,SBJ}.X.{ITT,PP5,PP6,PP7,FAMS}.X` · Mitgliedschaften `S08.MITGL.{Z05,…,CM}.X.P<Code>.ITT` und `S08.MITGL.{Z30,CM,SBJ}.X.P<Code>.{PP5,PP6,PP7,AK9,FAMS}` (hier trägt das Feld VARIANTE den Setnamen) · Fluss `S08.{FLZUG,FLPRE,FLAUSG,FLNANG}.X.X.{IG,KG,VA,VB,VC}.X`, `S08.{FLITT,FLOPRE,FLOPOST}.{Z05,…,CM}.X.{IG,KG}.X`, `S08.FLOPAH.PAH.X.{IG,KG}.X` · Box 6 `S08.{B6NE,B6NEKM,B6IF}.X.X.IG.X`, `S08.{B6FK,B6NA}.X.X.{IG,KG}.X` · Anteile `S08.ANT.{Z05,…,CM}.X.{IG,KG,ALL}.X`, `S08.ANTTN.X.X.{IG,KG,ALL}.X`.

### S09 Versuchszahlen

**Status:** Plan 12.09. (Auswertungsplan § 2 B1 und B2, PA § 3.1, Versuchszahl-Protokollbefund § 2 und § 3) · Umfang nach Nachtrag 2 (F.7).
**Zweck:** Zahl der gültigen Versuche je Gruppe beschreiben.
**Eingang:** Versuchsdaten, S04, Personendaten.
**Regel:**
1. Bezugsmenge je Zeitpunkt: Spieler mit Zeilen zu diesem Zeitpunkt, post ohne Spieler mit Status „nicht angetreten“.
2. Mittlere Zahl gültiger Versuche k je Zielgröße (Z05, Z10, Z30, SBJ, CL, CR), Zeitpunkt und Gruppe über die Bezugsmenge.
3. entfällt (Nachtrag 2).
4. entfällt (Nachtrag 2).
**Ausgabe:** `S09.KMEAN.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.{IG,KG}.X`.

---

## Teil C · Messgüte

### S10 Typischer Messfehler, SESOI und abgeleitete Größen

**Status:** Plan 12.09. (Auswertungsplan § 2 B3, PA § 11.3, Hopkins, 2000) · Definitionen von TE und S, KI-Form und CV-Nenner nachträglich (O5, O6, K12, K13, K15) · Umfang nach Nachtrag 2 (F.7).
**Zweck:** Messgüte je Zielgröße und Zeitpunkt aus den Wiederholungsversuchen der eigenen Daten.
**Eingang:** gültige Versuche (S02), S04.
**Mengen:** je Zielgröße Z ∈ {Z05, Z10, Z30, SBJ, CL, CR, CM} und Zeitpunkt prä und post getrennt, alle Spieler beider Gruppen gemeinsam (ALL). Zusätzlich TE je Verein, nur deskriptiv (PA § 11.3).
**Regel:**
1. TE-Menge: Spieler mit k ≥ 2. TE = √( Σ_i Σ_j (x_ij − x̄_i)² / Σ_i (k_i − 1) ), x̄_i Mittel der gültigen Versuche von Spieler i (gepoolte Innerspieler-SD, O5). df_TE = Σ_i (k_i − 1).
2. Seitenmittel CM (K15): Je Spieler zählen nur Versuchsnummern j, die auf beiden Seiten gültig sind. m_ij = (L_ij + R_ij)/2. TE_CM nach Regel 1 aus den m_ij, TE-Menge = Spieler mit mindestens zwei solchen Paaren.
3. 95-%-KI des TE, gleichendig aus der χ²-Verteilung (Hopkins, 2000, S. 13, K12): untere Grenze TE·√(df_TE / χ²_df(0,975)), obere Grenze TE·√(df_TE / χ²_df(0,025)) mit df = df_TE.
4. CV, nur prä (Hopkins, 2000, S. 12, K13): CV = 100 · TE / x̄_TE mit x̄_TE = Mittel aller gültigen Versuche der TE-Menge. Für CM das Mittel aller m_ij der TE-Menge.
5. Zwischen-Athleten-SD (O6), nur prä: S = SD der BEST-Werte prä aller Spieler mit vorhandenem BEST prä, beide Gruppen zusammen. n_S = Zahl dieser Spieler.
6. SESOI = 0,2 · S (PA § 11.3, Hopkins, 2000, S. 8, dort nach Cohen, 1988, S. 25), nur prä.
7. entfällt (Nachtrag 2).
8. Verhältnis RTS = TE / SESOI, nur prä.
9. Merkmal (PA § 11.3), nur prä: FLEINZ = 1, wenn TE > SESOI (dann keine Aussagen auf Einzelspielerebene).
10. Je Verein (VA, VB, VC) und Zeitpunkt: TE, df_TE und Zahl der Spieler der TE-Menge nach Regel 1 und 2.
Ist eine TE-Menge leer, ist TE fehlend mit Grund, ebenso alle davon abgeleiteten Größen.
**Ausgabe:** `S10.{TE,TELO,TEHI,DFTE,NTE}.{Z05,Z10,Z30,SBJ,CL,CR,CM}.{PRE,POST}.ALL.X` · `S10.{CV,SB,NSB,SESOI,RTS,FLEINZ}.{Z05,Z10,Z30,SBJ,CL,CR,CM}.PRE.ALL.X` · `S10.{TE,DFTE,NTE}.{Z05,Z10,Z30,SBJ,CL,CR,CM}.{PRE,POST}.{VA,VB,VC}.X`.
**Referenztests:** R07 und R13 (χ²-Quantile), R01 (Standardabweichung).

### S11 Bestwert-Bias, gemessen

**Status:** Plan 12.09. (PA § 11.8, Versuchszahl-Protokollbefund § 4).
**Zweck:** Ausmaß, um das ein dritter Versuch den Bestwert verschiebt, direkt an den eigenen Daten.
**Eingang:** gültige Versuche, S10.
**Regel:** je Zielgröße (Z05, Z10, Z30, SBJ, CL, CR) und Zeitpunkt, alle Spieler mit gültigen Versuchen 1, 2 und 3: Δ_i = best(x_i1, x_i2, x_i3) − best(x_i1, x_i2), best wie in S04. Ausgabe n, Mittel von Δ und Mittel von Δ geteilt durch SESOI desselben Ziels und Zeitpunkts. Nur deskriptiv.
**Ausgabe:** `S11.{N,DMEAN,DSESOI}.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.ALL.X`.

---

## Teil D · Deskription

### S12 Stichprobe, Ausgangswerte, Prä und Post

**Status:** Plan 12.09. (Auswertungsplan § 2 B5 und B6, Tab. 1 „Baseline-Vergleich: kein Test“, PA § 11.9) · K26 und K29 nachträglich · Menge ANA statt K30 und Umfang nach Nachtrag 2 (F.7).
**Zweck:** Beschreibung ohne Signifikanztests.
**Eingang:** Personendaten, S04, S05, S08.
**Regel:**
1. Stichprobe je Gruppe in der Analysepopulation (S08 Regel 11, Feld MENGE `ANAIG`, `ANAKG`): n, M, SD für AGE, HGT, MASS, PAH. Familiarisierung: Zahl der Spieler mit 1, mit 2 und mit fehlender Angabe je Gruppe über alle Zugeteilten (`IG`, `KG`).
2. Überlappung (K26): Für eine Größe mit Werten in beiden Gruppen ist der gemeinsame Bereich [L, U] mit L = max(min_IG, min_KG) und U = min(max_IG, max_KG). Gezählt wird je Gruppe die Zahl der Werte mit L ≤ x ≤ U. Ist L > U, sind beide Zahlen 0. Angewandt wird die Regel in S14 Regel 5, in den Analysesets.
3. Ausgangswerte je Zielgröße (alle sieben), keine Signifikanztests: d = (M_IG − M_KG) / SD_pool der BEST-Werte prä, ohne Korrektur J (K26), in zwei Mengen: alle Fälle mit BEST prä (`BASE`) und ITT-Set (Auswertungsplan § 2 B5). n, M und SD liefert Regel 4.
4. Prä und Post je Zielgröße und Gruppe (K29): n, M, SD von BEST prä über alle Fälle mit Wert (Menge `IG`, `KG`). Im ITT-Set n, M, SD von BEST prä und BEST post (`HAUPT`).
**Ausgabe:** `S12.{N,M,SD}.{AGE,HGT,MASS,PAH}.PRE.{ANAIG,ANAKG}.X` · `S12.{NFAM1,NFAM2,NFAMNA}.FAM.PRE.{IG,KG}.X` · `S12.D.{Z05,Z10,Z30,SBJ,CL,CR,CM}.PRE.{BASE,ITT}.HAUPT` · `S12.{N,M,SD}.{Z05,…,CM}.PRE.{IG,KG}.HAUPT` · `S12.{N,M,SD}.{Z05,…,CM}.{PRE,POST}.{ITTIG,ITTKG}.HAUPT`.

---

## Teil E · Inferenz

Notation: X ist die Designmatrix mit einer Spalte je Modellparameter, V = σ̂²·(XᵀX)⁻¹ die geschätzte Kovarianzmatrix der Koeffizienten. T_df ist die Verteilungsfunktion der t-Verteilung mit df Freiheitsgraden. Die Schätzung soll numerisch stabil erfolgen (etwa über eine QR-Zerlegung). Die Referenztests R04 und R05 prüfen das.

Für alle Analysen aus S13 bis S17 und S19 gilt die Fallzahlregel (S08 Regel 3). Bei INF = 0 werden die Kennungen der Analyse als fehlend mit Grund „Fallzahlregel“ ausgegeben. n, M und SD der Sets stehen in S08, S12, S16 und S17.

### S13 Hauptanalyse: ANCOVA im ITT-Set

**Status:** Antrag § 1 (ANCOVA mit dem Prä-Wert und %PAH als Kovariaten, α = 0,05, Hypothesen H0 und H1) · Plan 12.09. (PA § 11.2, § 11.4) · K17, K23 und P6 nachträglich · Ausgabe von P̄ und Ā nach Nachtrag 2 (F.7).
**Zweck:** Adjustierte Gruppendifferenz im Post-Wert je konfirmatorischer Zielgröße.
**Eingang:** ITT-Set je Zielgröße Z ∈ {Z30, CM, SBJ}, BEST prä und post, %PAH, Merkmal INF aus S08.
**Modell:** Post_i = b0 + b1·G_i + b2·Prä_i + b3·PAH_i + e_i, Schätzung nach der Methode der kleinsten Quadrate. Prä und Post sind BEST derselben Zielgröße.
**Regel** (nur bei INF = 1):
1. Koeffizienten b0 bis b3 mit Standardfehlern aus V. Residuen-SD σ̂ = √(Σe_i² / df), df = n − 4. R² des Modells.
2. Adjustierte Differenz b1 (IG minus KG) mit SE(b1), t = b1/SE(b1), p = 2·(1 − T_df(|t|)), 95-%-KI b1 ± t_df(0,975)·SE(b1).
3. Adjustierte Mittelwerte (K17): AM_g = b0 + b1·g + b2·P̄ + b3·Ā für g ∈ {0, 1}, mit P̄ und Ā gleich dem Mittel von Prä und %PAH über das Analyseset. SE(AM_g) = √(cᵀVc) mit c = (1, g, P̄, Ā)ᵀ. KI AM_g ± t_df(0,975)·SE(AM_g). P̄ und Ā werden mit ausgegeben.
4. Kein partielles η² (K24).
**Entscheidungsregel** (Antrag, K23, P6): Je Zielgröße ist SIG = 1, wenn p < 0,05 und b1 in günstiger Richtung liegt (Zeiten b1 < 0, Standweitsprung b1 > 0), sonst SIG = 0. Bei INF = 0 fehlt SIG. H0 ist abgelehnt (H0REJ = 1), wenn SIG = 1 für mindestens eine konfirmatorische Zielgröße gilt, sonst H0REJ = 0. NTEST ist die Zahl der konfirmatorischen Zielgrößen mit INF = 1. Keine Adjustierung für Mehrfachtestung (PA § 11.4).
**Ausgabe:** `S13.{B0,B1,B2,B3,SEB0,SEB1,SEB2,SEB3,SIGMA,DF,R2,T,P,KIU,KIO,AMIG,AMKG,SEAMIG,SEAMKG,AMIGU,AMIGO,AMKGU,AMKGO,NIG,NKG,SIG}.{Z30,CM,SBJ}.X.ITT.HAUPT` · `S13.{H0REJ,NTEST}.X.X.ITT.HAUPT` · `S13.{PREM,PAHM}.{Z30,CM,SBJ}.X.ITT.HAUPT` (P̄ und Ā aus Regel 3).
**Referenztests:** R04, R05 (Kleinste-Quadrate-Schätzung), R06 (t-Quantile).

### S14 Voraussetzungen

**Status:** Plan 12.09. (PA § 11.2 „zu prüfen und zu berichten“, § 11.9, Auswertungsplan § 2 B6 und Tab. 1 „Residuen, Brown-Forsythe, Gruppe × Prä, Gruppe × %PAH, Linearität, Überlappung“) · Folge verworfener Prüfungen, Prüfgrößen und Modelle nachträglich (O7, K18 bis K21) · Menge der Vorab-Prüfung nachträglich (P5) · Q-Q-Diagramm und Residuen-SD je Gruppe nachträglich (Nachtrag N1 und N2, Teil F.6).
**Zweck:** Voraussetzungen jedes Modells aus S13 prüfen und berichten.
**Eingang:** Modelle und Residuen aus S13, ITT-Sets, S04, S05.
**Regel** je Zielgröße Z ∈ {Z30, CM, SBJ}, Regeln 1 bis 5 bei INF = 1 des ITT-Sets:
1. Normalverteilung der Residuen (K18): Shapiro-Wilk-Test auf allen Residuen e_i des Modells gemeinsam, in der Approximation nach Royston (1995, Remark AS R94). Ausgabe W und p. Dazu ein Normal-Q-Q-Diagramm aller Residuen, Gruppen unterscheidbar markiert, eine Datei je Zielgröße (Nachtrag N1). Keine Kennzahl.
2. Varianzhomogenität (K19): Brown-Forsythe-Test, das ist der Levene-Test mit dem Median als Zentrum (NIST/SEMATECH e-Handbook, Abschn. 1.3.5.10). z_i = |e_i − Median der Residuen der Gruppe von i|. Einfaktorielle Varianzanalyse von z über die Gruppen, bei k Gruppen mit df1 = k − 1 und df2 = n − k, hier k = 2. Ausgabe F, df1, df2 und p. Zusätzlich die SD der Residuen e_i je Gruppe nach 0.5 Nr. 2 (SD_IG und SD_KG, Nenner n_Gruppe − 1) und das Verhältnis SD_KG / SD_IG (Nachtrag N2).
3. Homogenität der Regressionssteigungen (K20), zwei getrennte Modelle: Modell SLPRE = Modell S13 plus Term G·Prä, Modell SLPAH = Modell S13 plus Term G·PAH. Je Modell Koeffizient des Interaktionsterms, SE, t, df = n − 5, p.
4. Linearität (K21): Grafiken der Residuen gegen die Vorhersage, gegen Prä und gegen %PAH, Gruppen unterscheidbar markiert, eine Datei je Zielgröße. Keine Kennzahl.
5. Überlappung der Kovariaten im Analyseset (PA § 11.9): für Prä und für %PAH gemeinsamer Bereich nach S12 Regel 2, Zahl der IG- und KG-Spieler darin.
6. Vorab-Prüfung an den Prä-Werten (Auswertungsplan § 2 B6) in der Menge BPAH, das sind die Spieler mit BEST prä und %PAH (P5), mit der Fallzahlregel S08 Regel 3 für diese Menge: Modell Prä = c0 + c1·G + c2·PAH + c3·G·PAH mit c3, SE, t, df = n − 4, p. Shapiro-Wilk der BEST-Werte prä je Gruppe in derselben Menge mit W und p.
**Entscheidungsregel** (O7): Eine verworfene Prüfung (p < 0,05) ändert das Verfahren nicht. Sie wird mit Prüfgröße und p-Wert berichtet. Ausgabe je Prüfung ein Merkmal VERW (1 bei p < 0,05). Im Bericht gilt die Formulierung „geprüft und nicht verworfen“, nicht „erfüllt“ (PA § 11.9).
**Ausgabe:** `S14.{SWW,SWP,SWVERW}.{Z30,CM,SBJ}.X.ITT.HAUPT` · `S14.{BFF,BFDF1,BFDF2,BFP,BFVERW}.{Z30,CM,SBJ}.X.ITT.HAUPT` · `S14.{SDRIG,SDRKG,SDRQ}.{Z30,CM,SBJ}.X.ITT.HAUPT` · `S14.{BINT,SEINT,TINT,DFINT,PINT,VERW}.{Z30,CM,SBJ}.X.ITT.{SLPRE,SLPAH}` · `S14.{OVPREIG,OVPREKG,OVPRL,OVPRU,OVPAHIG,OVPAHKG,OVPAL,OVPAU}.{Z30,CM,SBJ}.X.ITT.HAUPT` · `S14.{CINT,SECINT,TCINT,DFCINT,PCINT}.{Z30,CM,SBJ}.PRE.BPAH.SLPAH` · `S14.{SWW,SWP}.{Z30,CM,SBJ}.PRE.{BPAHIG,BPAHKG}.X`.
**Referenztests:** R08 (Brown-Forsythe), R09 (Shapiro-Wilk), R05.

### S15 Effektstärke und unadjustierte Differenz

**Status:** Antrag § 1 („Effektstärken (Cohens d bzw. Hedges' g)“) · Plan 12.09. (PA § 11.2, Auswertungsplan § 6 Nr. 3: g = adjustierte Differenz / gepoolte Prä-SD × J, KI aus dem KI der adjustierten Differenz) · Standardisierer, Freiheitsgrade und Form der unadjustierten Differenz nachträglich (O3, O4) · auf die Hauptanalyse beschränkt (Nachtrag 2, F.7).
**Zweck:** Standardisierte adjustierte Differenz und unadjustierte Differenz (CONSORT Item 18: „both unadjusted and adjusted analyses should be reported“, Moher et al., 2010, S. 19).
**Eingang:** S13 mit dem ITT-Set und den BEST-Werten.
**Regel** für die Hauptanalyse (Set `ITT`, Variante `HAUPT`) je konfirmatorischer Zielgröße, nur bei INF = 1:
1. SD_prä = gepoolte SD der BEST-Werte prä der Spieler des ITT-Sets.
2. df_g = n_IG + n_KG − 2. J = 1 − 3/(4·df_g − 1) (O3). Das ist dieselbe Korrektur wie Lakens (2013, Formel 4): 1 − 3/(4(n1 + n2) − 9).
3. g = b1 / SD_prä · J. KI: KIU(b1) / SD_prä · J und KIO(b1) / SD_prä · J. b1 und seine KI-Grenzen stammen aus S13.
4. Unadjustierte Differenz (O4): D_u = M_post,IG − M_post,KG der BEST-Werte im ITT-Set. SD_post,pool = gepoolte SD der Post-Werte. SE = SD_post,pool·√(1/n_IG + 1/n_KG), t = D_u/SE, df = n − 2, p zweiseitig, KI D_u ± t_df(0,975)·SE. Das entspricht dem Modell Post = a0 + a1·G + e.
**Ausgabe:** `S15.{SDPRE,DFG,J,G,GKIU,GKIO,UD,UDSE,UDT,UDDF,UDP,UDKIU,UDKIO,MPOSTIG,MPOSTKG,SDPOST}.{Z30,CM,SBJ}.X.ITT.HAUPT`.
**Referenztests:** R11 (Hedges' g), R03 (Zwei-Gruppen-Vergleich mit gepoolter Varianz).

### S16 Per-Protokoll-Vergleich und Antragskriterium

**Status:** Antrag § 8 (Ausschluss bei Adherence unter 75 % aus der Hauptanalyse, Berücksichtigung in Sensitivitätsanalyse) · Plan 12.09. (Auswertungsplan § 5.3, PA § 11.7: Hauptanalyse ITT, Antragskriterium deskriptiv, Per-Protokoll ≥ 6 als beobachtender Vergleich) · Umfang nach Nachtrag 2 (F.7).
**Zweck:** Effekt der Durchführung unter der Voraussetzung ausreichender Umsetzung, ausdrücklich als nicht randomisierter, beobachtender Vergleich.
**Regel:**
1. PP6: Modell S13 im Set PP6 je konfirmatorischer Zielgröße, mit Fallzahlregel. Ausgaben: b1 mit SE, df, t, p und 95-%-KI sowie n_IG und n_KG. SIG und die Entscheidung über H0 gelten nur für die Hauptanalyse S13.
2. Deskriptiv, unabhängig von INF: M und SD von BEST prä und BEST post im IG-Teil des Sets PP6. Der KG-Teil ist der KG-Teil des ITT-Sets (S12).
3. Antragskriterium AK9: je konfirmatorischer Zielgröße für jeden Spieler des Sets AK9 Δ = BEST post − BEST prä als Einzelwert. BEST prä und post stehen in S04, die Zahl der Spieler in S08. Kein Test, keine Effektstärke.
**Ausgabe:** `S16.{B1,SEB1,DF,T,P,KIU,KIO,NIG,NKG}.{Z30,CM,SBJ}.X.PP6.HAUPT` · `S16.{M,SD}.{Z30,CM,SBJ}.{PRE,POST}.PP6IG.HAUPT` · `S16.DIFF.{Z30,CM,SBJ}.DIFF.P<Code>.AK9`.

### S17 Vorab festgelegte Sensitivitätsanalysen

**Status:** Plan 12.09. (PA § 11.5, § 11.8, Auswertungsplan § 2 B7 Blöcke C bis F) · Menge des Modells ohne %PAH nachträglich (K22) · R²-Spanne entfallen (O9, Teil F) · Umfang nach Nachtrag 2 (F.7).
**Zweck:** Robustheit der Hauptanalyse gegenüber Aggregat, Mindestdosis, Modellform und Familiarisierung.
**Regel** je konfirmatorischer Zielgröße, jeweils mit Fallzahlregel. Ausgaben: b1 mit SE, df, t, p und 95-%-KI sowie n_IG und n_KG:
1. `MW`: Modell S13 mit MEAN statt BEST für Prä und Post (CM: CM_MEAN), ITT-Set.
2. `PP5`, `PP7`: Modell S13 in den Sets PP5 und PP7.
3. `AEND` Änderungswertmodell: Δ_i = Post_i − Prä_i (BEST), Modell Δ_i = b0 + b1·G_i + b3·PAH_i + e_i im ITT-Set, df = n − 3.
4. `OPAH` ohne %PAH: Post_i = b0 + b1·G_i + b2·Prä_i + e_i im ITT-Set (K22), df = n − 3.
5. `FAMB` Familiarisierung als dritte Kovariate: Post_i = b0 + b1·G_i + b2·Prä_i + b3·PAH_i + b4·F_i + e_i, F = Zahl der Familiarisierungstermine (1 oder 2, numerisch), Set FAMS, df = n − 5. Hinweis im Bericht: In der IG ist F mit Verein A konfundiert (Auswertungsplan § 5.5).
6. Familiarisierung Variante a, nur deskriptiv (Auswertungsplan § 5.5): je Gruppe und F ∈ {1, 2} n, M, SD von Δ = BEST post − BEST prä im ITT-Set.
7. Deskriptiv, unabhängig von INF: M und SD von BEST prä und BEST post im IG-Teil der Sets PP5 und PP7 sowie in beiden Gruppen des Sets FAMS.
**Ausgabe** (Familien gemäß `_Kennungen.csv`): `S17.{B1,SEB1,DF,T,P,KIU,KIO,NIG,NKG}.{Z30,CM,SBJ}.X.ITT.{MW,AEND,OPAH}` · `S17.{…}.{Z30,CM,SBJ}.X.{PP5,PP7}.HAUPT` · `S17.{…}.{Z30,CM,SBJ}.X.FAMS.FAMB` · `S17.{M,SD}.{Z30,CM,SBJ}.{PRE,POST}.{PP5IG,PP7IG}.HAUPT` · `S17.{M,SD}.{Z30,CM,SBJ}.{PRE,POST}.{FAMSIG,FAMSKG}.FAMB` · `S17.{N,M,SD}.{Z30,CM,SBJ}.DIFF.{ITTIG,ITTKG}.{F1,F2}`.

### S18 Sensitivitäts-Poweranalyse, Standardweg

**Status:** Plan 12.09. (PA § 11.1: Sensitivitäts- statt A-priori-Poweranalyse je Zielgröße, α = 0,05, Power 0,80, MDES als Ergebnis, Einordnung gegen den SESOI, Power bei den dokumentierten Vorab-Erwartungen) · Rechenweg nachträglich (O9: ohne Kovariatengewinn R² und ohne Imbalance-Faktor, Teil F) · P7 nachträglich · Kombinationen nach Nachtrag 2 (F.7).
**Zweck:** Welche Effekte die erreichte Stichprobe mit ausreichender Power hätte entdecken können (Lakens, 2022, S. 5, Tab. 3).
**Eingang:** n_IG und n_KG der ITT-Sets von Z10, Z30, CM und SBJ. Keine Werte der Zielgrößen.
**Regel** je Zielgröße Z ∈ {Z10, Z30, CM, SBJ}, N = n_IG + n_KG. S18 wird unabhängig vom Merkmal INF gerechnet (P7, eingeschränkt durch Nachtrag 2):
1. Test: F-Test des Gruppenterms im Modell S13. df1 = 1, df2 = N − 4. Je Kovariate ein Nennerfreiheitsgrad weniger (Cohen, 1988, S. 380).
2. Nichtzentralität λ = f²·N mit f = σ_m/σ (G*Power-3.1-Handbuch, S. 26 und S. 30). Mit den Gruppenanteilen p_g = n_g/N ist σ_m² = Σ p_g·(μ_g − μ̄)² und μ̄ = Σ p_g·μ_g, für zwei Gruppen also f = d·√(p_IG·p_KG) und λ = d²·n_IG·n_KG/N. Bei gleichen Gruppen ist f = d/2 (Cohen, 1988, S. 276, Formel 8.2.6). d ist in Einheiten der Innergruppen-SD angegeben, ohne Minderung durch Kovariaten.
3. Power(d) = 1 − G(F_crit), G = Verteilungsfunktion der nichtzentralen F-Verteilung mit df1, df2 und λ, F_crit = F_df1,df2(0,95).
4. MDES, nur für Z30, CM und SBJ: d* = Lösung von Power(d) = 0,80 durch Nullstellensuche im Intervall [0, 10] mit Toleranz 1e-10. Liegt Power(10) unter 0,80, ist d* fehlend mit Grund. Ausgabe d* und das Vielfache d*/0,2 (SESOI = 0,2 SD-Einheiten, S10).
5. Power bei den dokumentierten Vorab-Erwartungen (PA § 11.1) mit denselben df und λ, nur für die im Plan genannten Kombinationen: Z10 mit D006 und D011, Z30, CM und SBJ mit D037 und D093.

| Variante | d | Fundstelle |
|---|---|---|
| D006 | 0,06 | Lloyd et al. (2016), Tab. 4, S. 1243 (10-m-Beschleunigung, plyometrische Gruppe nach PHV, Veränderung innerhalb der Gruppe) |
| D011 | 0,11 | Ramirez-Campillo et al. (2020), Abschn. 3.5 (10 m, höchstens 14 Einheiten bzw. höchstens 7 Wochen) |
| D037 | 0,37 | Moran et al. (2016), Tab. 4 (Countermovement Jump, weniger als 14,5 Einheiten) |
| D093 | 0,93 | Ramirez-Campillo et al. (2020), Abschn. 3.5 (10 m, mehr als 14 Einheiten bzw. mehr als 7 Wochen) |

**Ausgabe:** `S18.{NTOT,DF1,DF2,FCRIT}.{Z10,Z30,CM,SBJ}.X.ITT.X` · `S18.{MDES,MDESR}.{Z30,CM,SBJ}.X.ITT.X` · `S18.POW.Z10.X.ITT.{D006,D011}` · `S18.POW.{Z30,CM,SBJ}.X.ITT.{D037,D093}`.
**Referenztests:** R12 (nichtzentrale F-Verteilung und Fallzahlsuche).

### S19 Bootstrap-Konfidenzintervall der adjustierten Differenz

**Status:** nachträglich (Festlegung Verfasser 24.09.2026, O8 und Nachtrag N3, Teil F.6). Zusatzsensitivität, im Bericht als nachträglich festgelegt zu kennzeichnen.
**Zweck:** Konfidenzintervall der adjustierten Differenz ohne Normalverteilungsannahme für die Residuen.
**Eingang:** ITT-Set je Zielgröße Z ∈ {Z30, CM, SBJ}, BEST prä und post, %PAH. Je Zielgröße nur bei INF = 1 (S08 Regel 3).
**Regel:**
1. Zufallszahlengenerator vor jeder Zielgröße neu mit dem Startwert 20260924 setzen. Reihenfolge Z30, CM, SBJ. Regeln 2 bis 6 gelten je Zielgröße.
2. B = 10 000 Ziehungen. In jeder Ziehung werden n_IG Spieler aus der IG und n_KG Spieler aus der KG des ITT-Sets mit Zurücklegen gezogen (Schichtung nach Gruppe). Das Modell S13 wird geschätzt und b1* gespeichert.
3. Hat die Designmatrix einer Ziehung nicht vollen Rang, wird die Ziehung verworfen und gezählt, nicht ersetzt.
4. Perzentil-KI: Quantile 0,025 und 0,975 (Typ 7) der gültigen b1*. Zusätzlich SD der gültigen b1*.
5. Monte-Carlo-Fehler je KI-Grenze: Die ersten 20·⌊B_gültig/20⌋ gültigen b1* werden in Ziehungsreihenfolge in 20 gleich große Blöcke geteilt. Je Block das Quantil wie in Regel 4. MC-SE = SD der 20 Blockquantile / √20.
6. Abgleich zweier Implementierungen (Phase 6.1): Die Grenzen gelten als übereinstimmend, wenn die Differenz höchstens 3·√(MC-SE_1² + MC-SE_2²) beträgt. Unterschiedliche Generatoren sind zulässig.
**Ausgabe:** `S19.{BKIU,BKIO,BSD,BMCU,BMCO,BNGUELT,BNVERW}.{Z30,CM,SBJ}.X.ITT.BOOT`. Einheit der Grenzen, der SD und der MC-SE wie die Zielgröße.
**Referenztest:** keiner mit veröffentlichtem Sollwert. Prüfung über Grenzfälle (Phase 4.2) und den Monte-Carlo-Abgleich.

---

## Teil F · Nachträglich, entfallen und offen

### F.1 Rechenumgebung

R ist berichtete Rechenumgebung (Verfasserentscheidung 24.09.2026). Eine Freigabe durch den Betreuer wird nicht eingeholt (Verfasser 24.09.2026). Die Freigabe F1 der Spezifikation hat der Verfasser am 24.09.2026 selbst gegeben, ohne unabhängige Methodenprüfung. Der Antrag nennt „SPSS und/oder R“ (Antrag § 1), der Wechsel ist antragskonform und steht im Register des Auswertungsplans. Folge: Das partielle η², das nur als SPSS-Nebenausgabe vorgesehen war (PA § 11.2), entfällt (K24).

### F.2 Am 24.09.2026 entschiedene Punkte (nach dem Sperrdatum)

| Nr. | Festlegung | Schritt |
|---|---|---|
| O1 | Khamis-Roche-Koeffizienten aus Tab. 1 (1994) unverändert, Erratum (1995) bekannt, nicht eingesehen, nicht verwendet | S05 |
| O2 | Lineare Interpolation der Koeffizienten zwischen benachbarten Halbjahreszeilen | S05 |
| O3 | g mit gepoolter Prä-SD des Analysesets, J mit df = n_IG + n_KG − 2 | S15 |
| O4 | Unadjustierte Differenz = Differenz der Post-Mittel im Analyseset, gepoolte Varianz | S15 |
| O5 | TE = gepoolte Innerspieler-SD der Spieler mit k ≥ 2 | S10 |
| O6 | S = SD der Bestwerte aller Spieler, beide Gruppen zusammen | S10 |
| O7 | Verworfene Voraussetzungsprüfungen werden berichtet, das Verfahren bleibt | S14 |
| O8 | Bootstrap-KI mit B = 10 000, Startwert 20260924, Schichtung nach Gruppe. Zielgrößen nach Nachtrag N3 | S19 |
| O9 | Sensitivitäts-Poweranalyse nach dem Standardweg, ohne R² und ohne Faktor SE | S18 |
| O10 | entfällt mit O9 (kein R² im Rechenweg) | – |
| K1 | Alter in Tagen / 365,25 am Prätesttag, berechnet in Phase 1 | S05 |
| K2 | Fehlende Elterngröße → %PAH fehlend, keine Ersatzgröße | S05 |
| K3 | Umrechnung mit 2,54 cm je Zoll und 0,45359237 kg je Pfund | S05 |
| K4 | Auslöseprüfung über Abschnitte zwischen vorhandenen Teilzeiten, Lauf = gleiche Versuchsnummer | S02 |
| K5 | Unbekannter Bemerkungstext oder ungültige Zeile ohne Bemerkung → Abbruch | S03 |
| K6 | Meldezeitpunkt = STARTED | S06 |
| K7 | Dubletten gekennzeichnet, jede Meldung zählt | S06 |
| K8 | Meldung außerhalb W1 bis W6 → Abbruch | S06 |
| K9 | Umsetzungsrate mit Nenner 12 × zugeteilte IG-Spieler, ohne Listenplatz Einzelwert fehlend, in Rate und Verteilung 0 | S07 |
| K10 | sRPE-Load nur für „ganz“, mit wochenspezifischer Sitzungsdauer | S07 |
| K11 | Reifebänder nicht aufgenommen | F.5 |
| K12 | TE-KI gleichendig aus χ² | S10 |
| K13 | CV mit dem Mittel aller gültigen Versuche der TE-Menge | S10 |
| K14 | MDC mit der Konstante 1,96. Entfällt mit Nachtrag 2 | S10 |
| K15 | TE des Seitenmittels aus beidseitig gültigen Versuchsnummern | S10 |
| K16 | TE/√n mit n = Spieler der S-Menge. Entfällt mit Nachtrag 2 | S10 |
| K17 | Adjustierte Mittelwerte bei Kovariaten am Mittel des Analysesets | S13 |
| K18 | Shapiro-Wilk auf den Modellresiduen, vorab auf den Prä-Werten je Gruppe | S14 |
| K19 | Brown-Forsythe auf den Residuen nach Gruppe | S14 |
| K20 | Steigungshomogenität in zwei getrennten Modellen | S14 |
| K21 | Linearität nur grafisch | S14 |
| K22 | Modell ohne %PAH in derselben Menge wie die Hauptanalyse | S17 |
| K23 | Richtungsregel und globale Entscheidung über H0 | S13 |
| K24 | Partielles η² entfällt | S13 |
| K25 | entfällt mit O9 (keine R²-Spanne) | – |
| K26 | Baseline-d ohne J, Überlappung mit eingeschlossenen Grenzen | S12, S14 |
| K27 | Erhebungs- und Attritionsanteile mit gültigem Prä- und Post-Wert je Zugeteiltem | S08 |
| K28 | Leistungsunabhängigkeit über Pearson r, roh und je Verein. Entfällt mit Nachtrag 2 | S09 |
| K29 | Deskriptive Prä-Post-Werte über alle Fälle je Zelle, zusätzlich im ITT-Set. Mit Nachtrag 2 eingeschränkt | S12 |
| K30 | Stichprobe zusätzlich für Spieler mit Status ausgewertet. Mit Nachtrag 2 ersetzt durch die Menge ANA | S12 |

### F.3 Bei der Ausarbeitung präzisiert (mit F1 am 24.09.2026 bestätigt)

Die Quellen legen diese Punkte nicht wörtlich fest. Die Spezifikation wählt jeweils die nächstliegende Lesart. Keiner der Punkte berührt die Hauptanalyse, die Effektstärke oder die Analysesets.

| Nr. | Präzisierung | Lesart und Grund | Schritt |
|---|---|---|---|
| P1 | Fisher-KI der explorativen Korrelationen mit dem ungerundeten Quantil z_0,975. Ohne Anwendung seit Nachtrag 2 | FA § 9 nennt nur „95-%-KI (Fisher-z)“. Das ungerundete Quantil ist die Voreinstellung üblicher Software | S07 |
| P2 | „durchgeführt“ = Status ganz oder teilweise | So verwendet die FA den Begriff (§ 2, § 3, § 6), ohne ihn zu definieren | S07 |
| P3 | Abstand zur Veröffentlichung bezogen auf das Video der Programmwoche nach Kalenderregel. Ohne Anwendung seit Nachtrag 2 | Die Kalenderregel ist nach FA § 2 die Hauptzuordnung | S07 |
| P4 | Wochen- und Blockanteile zählen die Meldungen „ganz“ ohne Wochendeckel | Entspricht der Hauptzählung (PA § 3.1). Die FA nennt den Zähler nur „vollständige Einheiten“ | S07 |
| P5 | Vorab-Prüfung an den Prä-Werten in der Menge mit BEST prä und %PAH, auch für Shapiro-Wilk | Das Prüfmodell braucht %PAH. Beide Vorab-Prüfungen laufen so auf denselben Spielern | S14 |
| P6 | Nicht inferenzfähige Zielgrößen haben kein SIG. H0REJ = 1, sobald ein SIG = 1 ist, sonst 0. NTEST wird mit ausgegeben | Wörtliche Anwendung von K23 bei fehlenden Tests | S13 |
| P7 | Poweranalyse unabhängig von INF. Mit Nachtrag 2 nur für die im Plan genannten Kombinationen | Die Tabelle in PA § 11.1 enthält alle Zielgrößen, auch Sets unter acht Spielern je Gruppe | S18 |

### F.4 Gegenüber dem Plan entfallen

1. R²max = rel², Faktor SE und die R²-Spanne der Sensitivitäts-Poweranalyse (PA § 11.1, § 11.5), entfallen mit O9.
2. Partielles η² (K24).
3. Die Größen, die mit Nachtrag 2 entfallen (F.7).
Alle drei Punkte gehören als nachträgliche Änderung in das Register des Auswertungsplans.

### F.5 Offen oder nicht aufgenommen, wird nicht gerechnet

1. Reifebänder (%PAH-Klassen). Im Plan nicht festgelegt, Entscheidung offen (K11). Aufnahme nur per datiertem Nachtrag.
2. Zeitgleiche Meldungen verschiedener Spieler (FA § 1). Die FA beschreibt den Befund, legt aber keine Regel zur Bildung der Zeitfenster fest.
3. Modalwert des Untergrunds je Spieler (FA § 6). Keine Regel für Gleichstände.
4. Kategorien aus Freitexten (Gründe, Lokalisation von Beschwerden, Art des Fremdtrainings, FA § 6 und § 7). Freitexte sind nicht Teil des Eingangs.

### F.6 Nachtrag 1 nach der Freigabe F1 (24.09.2026)

Grundlage: Literaturabgleich der Voraussetzungsprüfungen, Entscheidung des Verfassers am 24.09.2026. Die Nachträge ergänzen Ausgaben. Sie ändern keine Regel der Hauptanalyse und keine bereits festgelegte Kennung.

| Nr. | Nachtrag | Grund | Schritt |
|---|---|---|---|
| N1 | Normal-Q-Q-Diagramm der Residuen je Zielgröße | Grafische Prüfung neben dem Shapiro-Wilk-Test | S14 Regel 1, G.1 |
| N2 | SD der Residuen je Gruppe und Verhältnis SD_KG / SD_IG | Richtung einer möglichen Verzerrung bei ungleich großen Gruppen erkennbar machen | S14 Regel 2 |
| N3 | Bootstrap-KI für Z30, CM und SBJ, Startwert vor jeder Zielgröße neu | Einheitliche Zusatzsensitivität für alle konfirmatorischen Zielgrößen | S19 |

### F.7 Nachtrag 2 nach der Freigabe F1 (24.09.2026)

Grundlage: Entscheidung des Verfassers vom 24.09.2026 zum Berichtsumfang. Der Nachtrag beschränkt die Ausgabe auf die Größen, die berichtet werden oder die eine Prüfung oder die Darstellung braucht. Er ändert keine Regel der Hauptanalyse, kein Analyseset der Inferenz und keinen Referenztest. Die Anlage `_Kennungen.csv` enthält danach 1.535 Kennungen. Entfallene Regeln behalten ihre Nummer mit dem Vermerk „entfällt“. P1 und P3 sind ohne Anwendung, weil ihre Regeln entfallen.

| Nr. | Änderung | Stelle |
|---|---|---|
| N4.1 | Meldungen je Status nur für die IG gesamt | S06, Ausgabe |
| N4.2 | Fensterregel entfällt, keine Ausgabe verwendet sie | S06 Regel 8 |
| N4.3 | Adhärenz: Einzelwerte für GANZ, WOCAP und DIST · Summe und Rate für GANZ, GT, WOCAP und DIST, nur IG · Verteilung für GANZ, für WOCAP und DIST nur die Schwellen 6 und 9 · Median und Mittel über die zugeteilten Spieler, Spieler ohne Listenplatz mit 0 (so Regel 7 und die Kennungsanlage, Nachtrag 3, N5.2), GTWOCAP und GTDIST entfallen | S07 Regeln 3 bis 7 |
| N4.4 | Zeitstruktur: nur der Wochenanteil der IG. Blockanteile und Zählungen je Woche entfallen | S07 Regeln 8 bis 10 |
| N4.5 | Belastung: CR-10 und sRPE-Load für die IG mit n, M, SD, Median, Min und Max, je Woche mit n, M und SD. Werte je Verein, je Spieler, bei „teilweise“, Stufenverteilung und Summen des Load entfallen | S07 Regeln 11 und 12 |
| N4.6 | Unerwünschte Ereignisse ohne Aufschlüsselung je Woche und Verein | S07 Regel 13 |
| N4.7 | Untergrund, Videopausen, Fremdtraining, Instrumentkennwerte und explorative Beschreibung entfallen. `TIME_SUM` ist kein Eingang mehr | S07 Regeln 14 bis 22, 0.4 |
| N4.8 | Teilnehmerfluss je Zielgröße und ohne %PAH nur je Gruppe. Neue Menge ANA | S08 Regeln 8 und 11 |
| N4.9 | Versuchszahl nur als Mittel je Gruppe. Verteilung von k, Ausfallraten und Leistungsunabhängigkeit (K28) entfallen | S09 |
| N4.10 | Messgüte: Modellwert des TE des Seitenmittels, M_S, SESOI_T, MDC (K14) sowie TE/√n mit Merkmal (K16) entfallen. CV, S, SESOI, RTS und FLEINZ nur prä | S10 |
| N4.11 | Stichprobe in der Menge ANA statt der Menge „ausgewertet“ (ersetzt K30). Min und Max, Werte je Verein, Überlappung außerhalb der Analysesets, Post-Werte aller Fälle und Mittelwert-Deskription entfallen (K29 eingeschränkt) | S12 |
| N4.12 | Mittel von Prä-Wert und %PAH im ITT-Set als Ausgabe | S13 Regel 3 |
| N4.13 | g und unadjustierte Differenz nur für die Hauptanalyse | S15 |
| N4.14 | Per-Protokoll-Vergleich und Sensitivitätsanalysen: je Analyse b1 mit SE, df, t, p, KI und n je Gruppe. Übrige Koeffizienten, σ̂, R², adjustierte Mittelwerte und g entfallen | S16, S17 |
| N4.15 | Poweranalyse nur für die im Plan genannten Kombinationen: Z10 mit D006 und D011, Z30, CM und SBJ mit D037 und D093. MDES nur für Z30, CM und SBJ. Schränkt P7 ein | S18 |
| N4.16 | Kennungsschema ohne `W7`, `VOR`, `AB`, `AUSG`, `LT6`, `GE6`, `ALLE`, `GTWOCAP`, `GTDIST`, `EXP1` und `EXP2`, mit `ANA` | 0.3 |

Unverändert bleiben S01 bis S05, S11, S14, S19, Teil G und die Referenztests R01 bis R13.

### F.8 Nachtrag 3 nach der Freigabe F1 (25.09.2026)

Grundlage: Code-Durchsicht über Kreuz der Phase 6.2 (`02_Befunde\Durchsichtsprotokoll_2026-09-25`, Teil C), Entscheidung des Verfassers am 25.09.2026 nach bestandenem Abgleich 6.1. Beide Implementierungen hatten die vier Stellen bereits gleich gelesen. Der Nachtrag hält die Lesart schriftlich fest. Er ändert keine Regel der Hauptanalyse, keine Kennung und keinen Referenztest. Dass er keinen Wert der Ergebnisdatei berührt, hält das Durchsichtsprotokoll fest.

| Nr. | Klarstellung | Stelle | Grund |
|---|---|---|---|
| N5.1 | Fehlt ein Eingang, gilt der Grund „Eingang fehlt“, auch bei Alter außerhalb des Gültigkeitsbereichs | S05 Regel 9, G.1 Nr. 4 | Der Vorrang der Gründe war nicht festgelegt. Beide Implementierungen prüfen den fehlenden Eingang zuerst |
| N5.2 | Median und Mittel der Adhärenz GANZ über die zugeteilten Spieler, Spieler ohne Listenplatz mit 0 | F.7 N4.3, S07 Regel 7 | N4.3 sagte „über Spieler mit Meldung“, Regel 7 und die Kennungsanlage („je zugeteiltem Spieler“) nennen die zugeteilten Spieler. Beide Implementierungen rechnen so |
| N5.3 | Rang der Designmatrix nach QR-Zerlegung mit Toleranz 1e-7 auf der spaltenskalierten Matrix oder gleichwertig | 0.5 Nr. 11 | Das Rangkriterium war nicht beziffert. Klarstellung, keine neue Regel |
| N5.4 | Die Gegenprobe darf den Dateinamen der Grafiken den Zusatz `_Python` anhängen | G.1 Nr. 6 | Die Dateinamen waren nur für eine Implementierung eindeutig |

---

## Teil G · Ausgabe, Referenztests, Abgleich

### G.1 Ergebnisdatei

1. Eine CSV-Datei, Kodierung UTF-8, Komma als Trennzeichen, Punkt als Dezimalzeichen, eine Kopfzeile, Spalten `Kennung`, `Wert`, `Einheit`, `Grund`, `Skript`. Texte mit Komma stehen in doppelten Anführungszeichen.
2. Jede Kennung aus `_Kennungen.csv` erscheint genau einmal, Spielerkennungen für jeden Spieler der Menge in Spalte `spielermenge`. Keine weiteren Kennungen.
3. Werte ungerundet mit mindestens zwölf signifikanten Stellen, in fester oder wissenschaftlicher Schreibweise. Merkmale als 0 oder 1. Anzahlen als ganze Zahlen.
4. Ein fehlender Wert steht mit leerem Feld `Wert` und einem Grund aus dieser Liste: „Eingang fehlt“ · „Fallzahlregel“ · „Rang“ · „zu wenige Werte“ · „konstant“ · „außerhalb Gültigkeitsbereich“ · „nicht erhebbar“ · „keine Nullstelle“. Weitere Gründe nur mit Rückfrage. Treffen mehrere Gründe zu, gilt der in der Regel zuerst geprüfte, in S05 „Eingang fehlt“ vor „außerhalb Gültigkeitsbereich“ (Nachtrag 3, N5.1).
5. Einheit je Kennung wie in `_Kennungen.csv`.
6. Grafiken aus S14 Regel 1 und Regel 4 als Dateien `S14_QQ_<ZIEL>` und `S14_Linearitaet_<ZIEL>` im Format PNG oder PDF, ohne Kennung. Die Gegenprobe darf ihren Dateinamen den Zusatz `_Python` anhängen (Nachtrag 3, N5.4).
7. Zwischendateien je Schritt (etwa die Gültigkeit je Versuchszeile) dürfen zusätzlich abgelegt werden. Sie tragen keine Kennung.
8. Die Anlagen dieser Spezifikation folgen derselben Form wie Nr. 1.

### G.2 Referenztests (Phase 4)

Vor der Studienrechnung rechnet die Instanz jeden Referenztest der Anlage `_Referenzdaten.csv` mit den Daten der Anlage `_Referenzdaten_Daten.csv` und demselben Code, der später die Studiendaten rechnet. Ausgabe je Sollwert: Test, Größe, Sollwert, eigener Wert, Abweichung, bestanden (0 oder 1). Die Sollwerte sind wörtlich aus den Quellen übernommen, nicht gerechnet. Ein nicht bestandener Test hält die Auswertung an.

| Nr. | Datensatz und Quelle | prüft | Schritt |
|---|---|---|---|
| R01 | NIST StRD NumAcc1 | Mittel und SD mit Nenner n − 1, Stellengenauigkeit | S04, S10, S12 |
| R02 | NIST StRD SiRstv | einfaktorielle Varianzanalyse, Residuen-SD | S14 |
| R03 | NIST StRD AtmWtAg | Zwei-Gruppen-Vergleich mit gepoolter Varianz bei schlecht konditionierten Daten | S15, 0.5 Nr. 2 |
| R04 | NIST StRD Norris | einfache lineare Regression mit Standardfehlern | S13 |
| R05 | NIST StRD Longley | multiple Regression, numerische Stabilität | S13, S14, S17 |
| R06 | NIST/SEMATECH e-Handbook 1.3.6.7.2 | t-Quantile | S13, S15 |
| R07 | NIST/SEMATECH e-Handbook 1.3.6.7.4 | χ²-Quantile | S10 |
| R08 | NIST/SEMATECH e-Handbook 1.3.5.10, GEAR | Brown-Forsythe (Levene mit Median) | S14 |
| R09 | NIST Dataplot, ZARR13 | Shapiro-Wilk nach AS R94 | S14 |
| R10 | Khamis & Roche (1994), S. 507 | Vorhersagegleichung | S05 |
| R11 | Lakens (2013), Tab. 3 und Beispiel | Cohens d, Hedges' g, t-Test mit gepoolter Varianz | S15 |
| R12 | G*Power-3.1-Handbuch S. 29 · Cohen (1988), Tab. 8.3.12, 8.4.4, 2.4.1 | nichtzentrale F-Verteilung, Power, Fallzahlsuche | S18 |
| R13 | NIST/SEMATECH e-Handbook 1.3.5.8, GEAR | χ²-Test der Varianz, χ²-Quantile | S10 |

Die Fundstellen, Sollwerte und Toleranzen stehen je Zeile in `_Referenzdaten.csv`. Bei R12 wird df2 = N − k der Quelle verwendet, nicht df2 = N − 4 aus S18. Die Power-Funktion nimmt df1, df2 und λ deshalb als Argumente.

### G.3 Toleranzen für den Abgleich (Phase 6.1)

| Art der Größe | Toleranz |
|---|---|
| Anzahlen, Merkmale, Setzugehörigkeiten | exakt gleich |
| deterministische Rechnungen (alle Schritte außer den folgenden) | \|a − b\| ≤ 1e-9 · max(1, \|a\|) |
| iterative Rechnungen (Nullstellensuche S18, Shapiro-Wilk-p, Quantile nichtzentraler Verteilungen) | relative Abweichung ≤ 1e-6 |
| Zufallsverfahren (S19) | Differenz ≤ 3 · √(MC-SE_1² + MC-SE_2²) |
| Referenztests mit gedruckten Sollwerten | Übereinstimmung bis zur letzten gedruckten Stelle, das heißt Abweichung höchstens eine halbe Einheit dieser Stelle |
| Referenztests mit NIST-Zertifikatswerten | Übereinstimmung auf mindestens 9 signifikante Stellen |

Liegt eine Abweichung außerhalb der Toleranz, wird sie in Phase 6 geklärt, nicht durch Anpassen der Toleranz.

---

## Teil H · Zahlen im Dokument und ihre Herkunft

### H.1 Vorgehen und Ergebnis

Alle Ziffernfolgen des Dokuments wurden maschinell ausgelesen und je Vorkommen einer Herkunft zugeordnet: Regel, Formelkonstante, Code, Fundstelle oder Wert aus einer Originalquelle. Die vollständige Liste mit Zeile, Abschnitt, Zahl, Art, Herkunft und Textumgebung steht in der Anlage `_Zahlenliste.csv`. Die übrigen Anlagen nennen ihre Herkunft je Zeile selbst (Spalten `quelle`, `fundstelle`, `status` oder `url`).

Ergebnis: Das Dokument enthält keine Zahl aus den Studiendaten, keine Fallzahl, keinen Mittelwert, keine Streuung, keinen Messgüte-, p- oder Effektwert und kein Ergebnis vom 15.09.2026. Bei der Prüfung entfernt wurden die beiden Grenzen der R²-Spanne aus PA § 11.5, weil sie aus den eigenen Messgütewerten abgeleitet sein können. Die Spanne entfällt ohnehin mit O9.

### H.2 Arten von Zahlen

| Art | Umfang | Herkunft |
|---|---|---|
| Kennungen und Bezeichner | S01 bis S19, Z05, Z10, Z30, W1 bis W6, D006 bis D093, R01 bis R13, O1 bis O10, K1 bis K30, P1 bis P7, N1 bis N4, F0, F1, H002 bis H010, HL-01 bis HL-08, BW-01 bis BW-14 und weitere Größenkürzel | Kennungsschema 0.3, Codebuch, Projektquellen |
| Gliederung und Verweise | Nummern von Abschnitten, Regeln, Listenpunkten, Schritten und Phasen, Fassung 12 der PA | Aufbau dieses Dokuments und des Auswertungsverfahrens |
| Fundstellen | Paragraphen der Projektquellen (etwa § 3.1, § 11.9, B0.2, B7), Seiten, Tabellen, Abschnitte, Formeln und Items der Originalquellen, Erscheinungsjahre, Band, Heft, Seitenbereich, DOI | Teil I |
| Dokumentdaten | 16.06.2026 Ethikantrag · 24.08.2026 Codebuch · 09.09.2026 Versuchszahl-Protokollbefund · 11.09.2026 Festlegung der Per-Protokoll-Schwelle · 12.09.2026 Auswertungsplan und FA · 13.09.2026 PA Fassung 12 · 15.09.2026 Sperrdatum · 24.09.2026 Festlegungen und Spezifikation · 01.06.2023 G*Power-Handbuch | jeweilige Quelle |
| Namen von Tests und Zielgrößen | 5, 10 und 30 als Sprintdistanzen in m · 505 als Name des Richtungswechseltests · U15 | Antrag § 3 |
| Codes und Wertebereiche | Versuch 1 bis 3 · Familiarisierung 1, 2 · G = 1 und 0 · Merkmale 0 und 1 · H010 1 bis 22 · H002 = 1 · H003 1 bis 12 · H004 1 bis 3 · H005 1 bis 11 · H006 1 bis 5 · H007 bis H009 1 und 2 · CR-10-Stufen 0 bis 10 · k = 0 bis 3 · Zählwerte 0 bis 12 · CASE 59, 70, 140, 158, 165, 190, 206 | Datenformat 0.4, Codebuch, FA § 1, PA § 3.1 |
| Formelkonstanten | Freiheitsgrade n − 1 bis n − 5 und N − 4 · 2 im Mittel zweier Werte und im zweiseitigen p-Wert · 1, 3 und 4 in J · 100 für Prozent · 60 Sekunden je Minute · Quantilpunkte 0,025, 0,95 und 0,975 · Quantiltyp 7 · 20 als Blockzahl im Monte-Carlo-Fehler | Formeln der Schritte mit den dort genannten Quellen |

### H.3 Regeln, Schwellen und Quellwerte

| Wert | Bedeutung | Herkunft | Status |
|---|---|---|---|
| 10,0 m/s und 0 s | Grenzen der Auslöseprüfung | Auswertungsplan § 2 B0.2, PA § 11.8 | Plan 12.09. |
| 5, 10, 30 m | Distanzen der Teilzeiten | Antrag § 3 | Antrag |
| 3 | Versuche je Spieler, Zeitpunkt und Test | Antrag § 3, PA § 3.1 | Antrag |
| 2,54 und 0,45359237 | Zoll in cm, Pfund in kg, exakt | NIST SP 811 (2008), Anhang B.8 und Fußnote 22 | nachträglich (K3) |
| 365,25 | Tage je Jahr im Dezimalalter | Festlegung K1 | nachträglich |
| 4,0 und 17,5 | Gültigkeitsbereich in Jahren | Khamis & Roche (1994), S. 506 | Antrag |
| 0,5 | Raster der Tabellenzeilen in Jahren | Khamis & Roche (1994), Tab. 1 | nachträglich (O2) |
| 5 min | Abstand eines Dubletten- oder Sammelmeldungspaars | FA § 1 | Plan 12.09. |
| 20.07. bis 30.08.2026, 00:00, 23:59:59 | Grenzen der Programmwochen W1 bis W6 | FA § 2 | Plan 12.09. |
| 12 | angebotene Einheiten je Spieler | PA § 3.1, FA § 4 | Plan 12.09. |
| 2 | Wochendeckel und Soll je Woche | FA § 3, PA § 3.1 | Plan 12.09. |
| 37:09, 36:55, 33:10, 34:48, 39:56, 40:07 | Sitzungsdauer der Wochen W1 bis W6 in min:s | FA § 5, Tab. 12 | Plan 12.09., K10 |
| 5, 6, 7 | Per-Protokoll-Schwellen, 6 als Hauptschwelle, 6 auch als Schwelle der Untergrenzen in S07 Regel 7 | PA § 11.5, § 11.7 | Plan 12.09. |
| 9 und 75 % | Antragskriterium, 9 auch als Schwelle der Untergrenzen in S07 Regel 7 | Antrag § 8, PA § 11.7 | Antrag |
| 8 | kleinste Gruppengröße für Inferenz | PA § 11.9 | Plan 12.09. |
| 0,05 | Signifikanzniveau | Antrag § 1 | Antrag |
| 95 % | Niveau der Konfidenzintervalle | PA § 11.2, § 11.4 | Plan 12.09. |
| 0,80 | Zielpower | PA § 11.1 | Plan 12.09. |
| 0,2 | SESOI-Faktor | PA § 11.3, Hopkins (2000), S. 8, Cohen (1988), S. 25 | Plan 12.09. |
| 0,06 · 0,11 · 0,37 · 0,93 | Vorab-Erwartungen der Poweranalyse | Lloyd et al. (2016), Tab. 4 · Ramirez-Campillo et al. (2020), Abschn. 3.5 · Moran et al. (2016), Tab. 4 | Plan 12.09. |
| 14 Einheiten, 7 Wochen, 14,5 Einheiten | Teilungsgrenzen der Quellen zu den Vorab-Erwartungen | Ramirez-Campillo et al. (2020), Abschn. 3.5 · Moran et al. (2016), Tab. 4 | Quelle |
| [0, 10] und 1e-10 | Suchintervall und Toleranz der Nullstellensuche | O9, 0.5 Nr. 9 | nachträglich |
| 10 000, 20260924, 20, 3 | Ziehungen, Startwert, Blockzahl und Abgleichfaktor des Bootstraps | O8, Toleranzvorschlag | nachträglich |
| 12 Stellen, 1e-9, 1e-6, 9 Stellen | Ausgabegenauigkeit und Toleranzen | 0.5 Nr. 1, G.3 | nachträglich |

---

## Teil I · Quellen

**Projektquellen:** Ethikantrag „Auswirkung eines videogestützten plyometrischen Heimtrainingsprogramms …“ vom 16.06.2026 · Auswertungsplan vom 12.09.2026 · Projektanweisungen Fassung 12 vom 13.09.2026, § 3.1 und § 11 · Fragebogenauswertung vom 12.09.2026 · Codebuch Fragebogen A, SoSci test546007, Stand 24.08.2026 · Versuchszahl-Protokollbefund vom 09.09.2026 · Auswertungsverfahren vom 24.09.2026.

**Originalquellen:**

- Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2. Aufl.). Lawrence Erlbaum. Verwendet: S. 25, S. 55 (Tab. 2.4.1), S. 276 (Formel 8.2.6), S. 311 (Tab. 8.3.12), S. 356, S. 380, S. 384 (Tab. 8.4.4).
- Dugdale, J. H., Arthur, C. A., Sanders, D., & Hunter, A. M. (2019). Reliability and validity of field-based fitness tests in youth soccer players. *European Journal of Sport Science, 19*(6), 745–756. https://doi.org/10.1080/17461391.2018.1556739
- Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2023). *G\*Power 3.1 manual* (Stand 01.06.2023). Heinrich-Heine-Universität Düsseldorf. Verwendet: S. 26, S. 29 bis 30.
- Foster, C., Florhaug, J. A., Franklin, J., Gottschall, L., Hrovatin, L. A., Parker, S., Doleshal, P., & Dodge, C. (2001). A new approach to monitoring exercise training. *Journal of Strength and Conditioning Research, 15*(1), 109–115. Im Antrag genannt.
- Hopkins, W. G. (2000). Measures of reliability in sports medicine and science. *Sports Medicine, 30*(1), 1–15. https://doi.org/10.2165/00007256-200030010-00001 · Verwendet: S. 2 bis 3 (Tab. I), S. 8, S. 10 (Tab. II), S. 12, S. 13.
- Khamis, H. J., & Roche, A. F. (1994). Predicting adult stature without using skeletal age: The Khamis-Roche method. *Pediatrics, 94*(4), 504–507. https://doi.org/10.1542/peds.94.4.504 · Verwendet: S. 504, S. 505 (Tab. 1), S. 506, S. 507.
- Erratum zu Khamis & Roche (1994). (1995). *Pediatrics, 95*(3), 457. https://doi.org/10.1542/peds.95.3.457 · Nicht eingesehen, nicht verwendet (O1).
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs. *Frontiers in Psychology, 4*, 863. https://doi.org/10.3389/fpsyg.2013.00863 · Verwendet: Formel 4, Tab. 3.
- Lakens, D. (2022). Sample size justification. *Collabra: Psychology, 8*(1), 33267. https://doi.org/10.1525/collabra.33267 · Verwendet: S. 5, Tab. 3.
- Lloyd, R. S., Radnor, J. M., De Ste Croix, M. B. A., Cronin, J. B., & Oliver, J. L. (2016). Changes in sprint and jump performances after traditional, plyometric, and combined resistance training in male youth pre- and post-peak height velocity. *Journal of Strength and Conditioning Research, 30*(5), 1239–1247. Verwendet: Tab. 4, S. 1243.
- Moher, D., Hopewell, S., Schulz, K. F., Montori, V., Gøtzsche, P. C., Devereaux, P. J., Elbourne, D., Egger, M., & Altman, D. G. (2010). CONSORT 2010 explanation and elaboration: Updated guidelines for reporting parallel group randomised trials. *BMJ, 340*, c869. https://doi.org/10.1136/bmj.c869 · Verwendet: Item 18 (S. 19), Item 19, Box 6.
- Moran, J., Sandercock, G. R. H., Ramírez-Campillo, R., Meylan, C., Collison, J., & Parry, D. A. (2016). Age-related variation in male youth athletes' countermovement jump following plyometric training: A meta-analysis of controlled trials. *Journal of Strength and Conditioning Research*, Publish Ahead of Print. https://doi.org/10.1519/JSC.0000000000001444 · Verwendet: Tab. 4. Endgültige Jahrgangs- und Seitenangaben sind vor der Zitation im Manuskript zu prüfen.
- National Institute of Standards and Technology. (2008). *Guide for the use of the International System of Units (SI)* (NIST Special Publication 811, 2008 ed.), Anhang B.2, B.3, B.8 und Fußnote 22. https://www.nist.gov/pml/special-publication-811
- National Institute of Standards and Technology. *Statistical Reference Datasets (StRD)*: ANOVA (SiRstv, AtmWtAg), Linear Least Squares Regression (Norris, Longley), Univariate Summary Statistics (NumAcc1). https://www.itl.nist.gov/div898/strd/
- NIST/SEMATECH. *e-Handbook of Statistical Methods*, Abschn. 1.3.5.8, 1.3.5.10, 1.3.6.7.2, 1.3.6.7.4. https://www.itl.nist.gov/div898/handbook/
- National Institute of Standards and Technology. *Dataplot Reference Manual*, „Wilk-Shapiro Normal Test“. https://www.itl.nist.gov/div898/software/dataplot/refman1/auxillar/wilkshap.htm
- Ramirez-Campillo, R., Castillo, D., Raya-González, J., Moran, J., Sáez de Villarreal, E., & Lloyd, R. S. (2020). Effects of plyometric jump training on jump and sprint performance in young male soccer players: A systematic review and meta-analysis. *Sports Medicine*. Akzeptiertes Manuskript, im Druck. Verwendet: Abschn. 3.5 und Abb. 2. Band, Seiten und DOI sind vor der Zitation im Manuskript zu prüfen.
- Royston, P. (1995). Remark AS R94: A remark on algorithm AS 181: The W-test for normality. *Applied Statistics, 44*(4), 547. https://doi.org/10.2307/2986146

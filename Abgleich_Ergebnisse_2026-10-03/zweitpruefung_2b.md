# Zweitprüfung der Teiltabelle 2b — Abgleich von Kapitel 5 mit dem Befund zu den Ergebnisteilen

Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext · Datum 03.10.2026

Prüfer: unabhängiger Subagent, an Kapitel 5, an den Teiltabellen 2a und 2b und an ihren Skripten nicht beteiligt. Auf allen Eingängen nur lesend. Geschrieben wurden nur dieser Bericht in W, eine Kopie von W für den Reproduktionslauf (`scratchpad/zp2b_lauf`) und ein eigenes Nachrechnungsskript (`scratchpad/zp2b_check/nachrechnung.py` mit `nachrechnung.txt`, ohne Semikolon).

W = `/tmp/claude-0/-home-claude/f97847bf-da5e-52e7-9eb7-7bf2fca9ddac/scratchpad/w2b` · C = `/mnt/user-data/uploads/Bachelorarbeit/Claude`

## 0 Verfahren

1. Jede der 47 Zeilen gegen den Wortlaut von Kapitel 5 (`textstand_saetze.md`), die Codes nach dem Codebuch und nach den Hinweisen (`konsens_2a.csv`, Spalten K und KH), die Merkmale (`eigen.txt`), die Belege (`pruef_2b.txt` § 0 bis § 17) und jede angeführte Fundstelle gelesen.
2. Jede Korpuszahl, die eine Zeile neu einführt, mit eigenem Skript an der Anlage `…_Saetze.csv` nachgerechnet: Befundanteil mit und ohne B2, Sätze und Wörter vor dem ersten Befund, Z2 vor dem ersten Befund, letzter Satz je Studie, Stellung von O2, V1, V2, Z1 und Z2, „respectively“. Erstnennung der Objekte an `textbausteine.txt` § 12 und § 14, zweite Lesart der Zielgrößenfolge an `zielgroessenfolge_text.py`.
3. Status gegen die Zählregel (Befund § 6.5) und gegen die Definition „bewusst anders (mit Entscheidung und Fundstelle)“, Registerzeilen gegen `register_pruefung.md` und Abgleichbefund § 2.
4. Vollständigkeit gegen Befund § 6.5 Nr. 1 bis 10, K1 bis K10, P1 bis P12, § 0, § 1, § 3, § 4, § 6, § 7 und Fortsetzungsübergabe § 5 Nr. 4.
5. Widersprüche zwischen den Zeilen, zu Teiltabelle 2a (Abgleichbefund § 3.1) und zu § 2 des Abgleichbefunds.
6. Reproduktion: W ohne `__pycache__` nach `scratchpad/zp2b_lauf` kopiert, dort `python3 pruef_2b.py /mnt/user-data/uploads/Bachelorarbeit/Claude zp2b_lauf/aus` (Python 3.13.16), die drei Ausgaben per MD5 gegen W verglichen, Semikola gezählt.

## 1 Gelesene Dateien (MD5)

| Datei | MD5 |
|---|---|
| W/teiltabelle_2b.md | 8976eb96ee5e7edc296e5f7a888b1532 |
| W/teiltabelle_2b.csv | 219d2871d69341d574f429e9ffa7c5dc |
| W/pruef_2b.py | 55c545b142731d7878b9ef0eb004b52a |
| W/pruef_2b.txt | 6bef2dea1ed75d100eb57568f4d9f2ee |
| W/textstand_saetze.md | 5658c9cda70cd90f3badea4791007390 |
| W/textstand.json | bb86ed78a6ba45038d57b8cb4f763fb4 |
| W/konsens_2a.csv | 39aa513a4a0b44d83905d738778124c1 |
| W/eigen.txt | dee8cc39be0f4dd9960216a123510739 |
| W/abgleich_2a.txt | 4f2e0d0b54caa8d7ba362572ba0a9326 |
| W/register_pruefung.md | d1de8266e4267d88c94366eb6963a397 |
| W/blind/memo_B.md | cd1759f79a739529ffe219ef367357c9 |
| W/master_saetze.md | 31d55bef07e17f200b26f3711521c767 |
| W/master_saetze.json | 4d06c614536fc21c2a2b57b284d9d925 |
| W/LIESMICH.md | 7ebe413130f892d2f29c1450544adb36 |
| C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md | c474dbf0f14b89fe581b67f4249d3387 |
| C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv | db2501d4b66838c9f15a6249514f4c88 |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/codebook.md | d69930967134fe8238aa20bb3fc033a1 |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.txt | 44dc8b4477a3eea4c958ac6b6ad7e4fd |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.py (Ausdruck B_RESPECTIVELY) | 49da188c7d3a0d38a3aac57f98726b5c |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/zielgroessenfolge_text.py | 079b185316d919160eaca3b8f7e6da72 |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/zielgroessenfolge_text.txt | 8880b76dcb21deaa5939a89550eaf7f8 |
| C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/analyse.txt | f649f1cf114ea08d60fd72327c07db71 |
| C/02_Befunde/Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md | a9b0ce2f765a8a9595cca2c7a47b7803 |
| C/04_Uebergaben/Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md | fc1e1d52b1c427b77f8501a691c9c735 |
| C/04_Uebergaben/Uebergabe_Abgleich_Ergebnisse_Fortsetzung1_2026-10-03.md | 7d8a86e1aca7ed18c2cfa4261545f927 |
| C/04_Uebergaben/Textvorschlag_5_2026-09-30.md | 835c3a45dd3a4e702684d05838bc38a1 |
| C/04_Uebergaben/Textvorschlag_6.1_2026-10-02.md (nur § 9, Vormerkung G6) | c3de94d3bbfaa82f32f98fff09ea8364 |
| C/04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md (Task 11, Nachträge) | 89fdd838993f66611b5b2fbe238d06eb |
| C/00_Steuerung/Projektanweisungen_Fassung17.md (§ 3, § 5.1, § 5a, § 10, § 11.9) | 0bd441fc265f08a6280d2ad582008f60 |
| C/01_Verfahren/Stilprofil_2026-09-13.md | de1a8fa4e639735b7999193a0870096c |
| C/01_Verfahren/Gliederung_2026-09-28.md (v6, Zeile Ergebnisse, Ä16) | e50ad22049affdae0d54832a72d2b429 |
| C/02_Befunde/Berichtsraster_2026-09-23.md (§ 3.12, § 3.13) | 527009f05fb25ea0b64abac4aa49bf55 |
| C/02_Befunde/Kennzahlen_2026-09-25_Werte.csv (K-01, K-10) | 25bca501fb60680c584fc6e7796dc31e |
| C/03_Skripte/Abgleich_Ergebnisse_2026-10-03/quellen/Auswertungs_und_Berichtsumfang_2026-09-24.md (§ 5) | 521f22ec2656a63dd3409b2633db20f7 |

Die lokalen Eingänge von `pruef_2b.py` in W (`textstand.json`, `eigen.json`, `abgleich_2a.json`, `master_saetze.json`, `konsens_2a.py`) sind bytegleich mit `C/03_Skripte/Abgleich_Ergebnisse_2026-10-03`, ebenso `konsens_2a.csv`, `register_pruefung.md` und `blind/memo_B.md`.

## 2 Zählung

**A 2 · B 9 · C 10**

## 3 Befunde

### Nr. 1 · A · Zeile 2b.27

**Befund.** Falsche Korpusaussage zur Stellung der Umsetzung: „… vor dem ersten Befund wie im Kern (4 von 5, Lloyd im Befundteil) und bei Klusemann, Veith und Rogers danach“. Bei Klusemann stehen alle fünf O2-Sätze (1.2 bis 1.6) vor dem ersten Befund (2.1). So zeigt es der eigene Beleg (`pruef_2b.txt` § 10: „Klusemann2012 Setting O2 15,6 % · vor“) und so steht es in Befund § 3.1 („Bei Veith, Rogers und Hilska steht ein Teil davon nach den Befunden“). Nachgerechnet: Veith 3.2 bis 3.4 nach den Befunden, Rogers 2.5 bis 2.7 danach (O2 sekundär in 1.4 und 1.9 davor), Hilska 2.1 und 2.2 davor, 7.1 bis 7.5 danach. Der Status ändert sich nicht.

**Vorschlag.** „… vor dem ersten Befund wie im Kern (4 von 5, Lloyd im Befundteil) und wie bei Klusemann, bei Veith und Rogers danach, bei Hilska vor und nach den Befunden.“

### Nr. 2 · A · Zeile 2b.6

**Befund.** Der Status „bewusst anders“ wird von der Zeile selbst widerlegt. Befund § 6.5 verlangt für „bewusst anders“ eine Entscheidung mit Fundstelle, die Zeile stellt fest „eigens begründet ist sie nicht“. P4 verlangt unadjustiert „neben“ adjustiert, nicht davor. Raster 5.2.1 und 5.2.2 regeln die Spalten von Tab. 3, nicht die Satzfolge. Zeile 9 Nr. 1 ist die allgemeine Freigabe, und genau sie reicht in 2b.9 nicht für „bewusst anders“ („freigegebener Wortlaut, Ordnung nicht eigens begründet“, dort „teilweise“). K4 ist Korpusregel (§ 6.2), kein Projektteil von § 6.1, den Textvorschlag 5 entscheidet. Die Frage des Prüfkatalogs („Steht je Zielgröße das Modellergebnis vor allem anderen?“) ist für jede Zielgröße mit Nein zu beantworten, weil A5 S3 (unadjustiert, alle drei) vor A5 S4 und S5 steht. Der Satz „Innerhalb jeder Zielgröße beginnt der Befund mit der adjustierten Differenz“ widerspricht dem ersten Satz der Zeile, gemeint sind die zielgrößenbezogenen Sätze.

**Vorschlag.** Status „teilweise (in den zielgrößenbezogenen Sätzen A5 S4, S5 steht die adjustierte Differenz vorn, davor A5 S3 über alle drei, ohne Entscheidung)“, nach strengem Wortlaut „nicht erfüllt“. Folge als Punkt für Schritt 3 vormerken (Grund nachtragen oder umstellen). Den zweiten Satz fassen als „In den zielgrößenbezogenen Sätzen (A5 S4, S5) steht die adjustierte Differenz vorn.“

### Nr. 3 · B · Zeile 2b.1

**Befund.** Die Nachrechnung ohne B2 ist an der CSV bestätigt (Median 56,83 %, Spanne 0,0 bis 100,0, Werte je Studie wie `pruef_2b.txt` § 1). Der Schluss „Kapitel 5 damit in der Spanne“ hängt aber allein an Moran: Dort sind alle Befundsätze B2, ohne sie bleiben vier X1-Sätze und ein Befundanteil von 0 %. Ohne diesen Grenzfall liegt das Minimum bei Beato (26,4 %), Kapitel 5 (22,4 %) liegt also auch nach der Nachrechnung unter allen neun übrigen Kernstudien. Die Nachrechnung ist eine abgeleitete Größe außerhalb von § 2 bis § 4 und zählt nach der Zählregel nicht als Übereinstimmung.

**Vorschlag.** „… Kapitel 5 liegt auch ohne B2 unter neun von zehn Kernstudien (nächste Beato 26,4 %), gleichauf nur mit Moran, dessen Befunde ohne B2 ganz entfallen (0 %). Die Nachrechnung ist keine Größe des Befunds und zählt nicht als Übereinstimmung (§ 6.5).“ Status „bewusst anders“ bleibt.

### Nr. 4 · B · Zeile 2b.2

**Befund.** „erfüllt (Form wie Korpus …)“ ist milder, als K1 trägt. K1 lautet „Rahmen vor dem ersten Befund: Orientierung oder Objektsätze“. Vor dem ersten Befund stehen zwei Z2-Sätze (A3 S3, S4, 27 Wörter), nach dem Codebuch weder Orientierung noch Objektsatz, und nach der Zählregel zählt dieser Code. Z2 ist im ganzen Korpus nie Primärcode, vor dem ersten Befund nur sekundär bei Klusemann. Die Satzzahl des Rahmens (16) liegt weit über der Spanne (0 bis 6). Die Stellung der unerwünschten Ereignisse ist Projektentscheidung (Raster 5.1.8, P in § 3.12, Plan § 3 Task 11 „Aufbau“). Registerzeile U9 betrifft die Folge Ausgangswerte vor Umsetzung, nicht K1. Die Klammer zu Klusemann ist unvollständig: 1.1 ist eine Verletzung als Ausschlussgrund (O1 mit Z2), nur 1.3 und 1.6 nennen Krankheit bei verpassten Einheiten.

**Vorschlag.** Status „erfüllt (Rahmen vorhanden, Wortanteil in der Spanne), bewusst anders für Z2 im Rahmen (Raster 5.1.8, Plan § 3 Task 11), Satzzahl über der Spanne (P12)“. Registerspalte „Zeile 7b, Zeile 9 Nr. 1“ statt U9. Klammer „(Klusemann 1.1 Verletzung als Ausschlussgrund, 1.3 und 1.6 Krankheit als Grund verpasster Einheiten)“.

### Nr. 5 · B · Zeile 2b.4

**Befund.** Die Vergleichszahl wechselt die Zählbasis. Kapitel 5 wird nach der ersten Nennung im Manuskript gezählt (fünf von sieben per Objektsatz), die Kernzahl „11 von 14“ nach der ersten Nennung im Ergebnisteil (`textbausteine.txt` § 12). Darin stehen drei Kernobjekte, die der Ergebnisteil zuerst in einer Klammer vor dem ersten Befund nennt, jeweils Tab. 1 in einem O4-Satz (Negra 2019 1.5, Negra 2020 1.1, Sammoud 1.4), gleich ob die Methodik sie schon nannte. Gleich gezählt (2a.25) sind es in Kapitel 5 fünf von neun Objekten, weil Tab. 1 und Tab. H1 vor dem ersten Befund in der Klammer stehen. Der Status trägt trotzdem, weil K3 auch „mindestens ein Objektsatz vor dem ersten Befund 8 von 10, alle Objekte 0 von 10“ zählt.

**Vorschlag.** „… fünf von neun Objekten, die der Ergebnisteil vor dem ersten Befund zuerst nennt, per Objektsatz (Zählweise des Korpus, 2a.25, Kern 11 von 14), fünf von sieben, wenn Tab. 1 und Tab. H1 als Wiederaufrufe aus 4.4 gelten (Projektsicht, Zeile 1d)“.

### Nr. 6 · B · Zeile 2b.11

**Befund.** „teilweise“ stützt sich auf die Lesart des Codierers B („nach Wortlaut alle Zielgrößen der Studie“), die der Konsens verworfen hat (A5 S6 = B1 mit zg X, „damit“ bindet an die drei geprüften). Nach der Zählregel zählt gegen K8 der Code nach dem Codebuch. Danach enthält Kapitel 5 keinen Sammelbefund mit Quantor über alle Zielgrößen, und K8 („wo er über alle Zielgrößen gilt“) ist gegenstandslos, weil kein Befund für alle sieben Zielgrößen gilt. Die Ausnahmen nennt A5 S11. Die Mehrdeutigkeit von A5 S6 ist ein Punkt der Leseführung (Befund § 3.6), kein Mangel nach K8. Dazu: „O-Codes nach Regel 2“ trifft nur A1 S4 (Ausgangsvergleich). A4 S1 ist O5 nach der Definition (Messgüte), den Vorrang vor dem Quantor regelt Hinweis H3.

**Vorschlag.** Status „erfüllt (nach dem Codebuch gegenstandslos, Ausnahmen in A5 S11)“, die Mehrdeutigkeit von A5 S6 als Potenzial der Leseführung für Schritt 3. „O-Codes (A1 S4 nach Regel 2, A4 S1 als Messgüte nach O5)“.

### Nr. 7 · B · Zeile 2b.13, dazu 2b.30 und 2b.31

**Befund.** Es fehlt die Registerzeile, die den Schluss trägt: Zeile 10, Teilentscheidung 10g („kein Resümee“, Textvorschlag 5 § 3: „letzter Satz ist ein Befundsatz mit (Tab. H4)“). Die Registerprüfung bewertet 10g als „erfüllt: letzter Satz Befund mit Klammer“, Abgleichbefund § 2.1 übernimmt das. 2b.13 kommt nach dem Codebuch (A6 S4 = Z1) zu „teilweise“. In der Sache ist das kein Registerverstoß, weil 10g das Resümee regelt, aber die Prämisse von Textvorschlag 5 § 2 und § 3 trägt nach dem Codebuch nicht. Ohne diesen Satz widersprechen sich § 2 und § 3.2 des Abgleichbefunds scheinbar. Plan § 3 Task 11 („letzter Satz mit Objektverweis, kein Resümee“) ist unabhängig von der Lesart erfüllt, nur Raster § 3.13 und Textvorschlag 5 § 2 hängen am Befundsatz, die Zeile knüpft beide an dieselbe Bedingung. „nach den Hinweisen Z1 mit B4“ ist unvollständig (Z1 mit B4 und V2). 2b.31 fasst den Schluss ohne Befundsatz unter „bewusst anders, wo Textvorschlag 5 entscheidet“, Textvorschlag 5 hat aber keinen Schluss ohne Befundsatz entschieden, sondern A6 S4 für einen Befundsatz gehalten.

**Vorschlag.** Registerspalte „Zeile 9 Nr. 1, Zeile 10g (Textvorschlag 5 liest A6 S4 als Befundsatz, nach dem Codebuch Z1)“. Satz neu: „Plan § 3 Task 11 ist erfüllt (Objektverweis, kein Resümee), Raster § 3.13 und Textvorschlag 5 § 2 nur in deren Lesart von A6 S4.“ In 2b.30 und 2b.31 für den Schluss auf 2b.13 verweisen, in 2b.31 den Schluss aus „bewusst anders“ herausnehmen.

### Nr. 8 · B · Zeile 2b.40

**Befund.** „A6 S4 ist nach den Hinweisen ein Sammelbefund mit Klammer am Schluss wie Negra 2019 2.8“ trifft weder nach dem Codebuch (Z1 mit B1 und V2) noch nach den Hinweisen zu (Z1 mit B4 und V2, B4 nur sekundär). Negra 2019 2.8 ist primär B4. Die Gleichsetzung stützt eine Übereinstimmung mit dem Korpus auf die Projektauslegung H2, gegen den letzten Satz der Zählregel, und widerspricht 2b.13, das nach dem Codebuch „kein Befundsatz am Schluss“ feststellt.

**Vorschlag.** „Kein Resümee über die Studie. A6 S4 ist nach dem Codebuch Z1 (Sammelsatz der Absicherung), kein Sammelbefund wie Negra 2019 2.8 (2b.13).“ Status „erfüllt“ für „keine Deutung, kein Resümee“ bleibt.

### Nr. 9 · B · Zeile 2b.28

**Befund.** Die Stellung von V2 und Z1 ist unvollständig oder ungenau beschrieben. (a) A5 S11 ist V2 und steht nach dem letzten Befundsatz (A5 S10). Primäres V2 steht im Korpus nur vorn (Rogers 1.2, 1.9) oder im Befundteil (Hilska 6.1, Veith 2.3), im Kern nur sekundär (Sammoud 1.1 vorn, Lloyd 1.3 im Befundteil), nie nach den Befunden. Die Zeile prüft die Stellung von A5 S11 nicht gegen den Korpus. (b) „Rogers 2.1 bis 2.4“: 2.2 trägt kein Z1, der eigene Beleg nennt 2.1, 2.3 und 2.4. (c) Z1 vor dem ersten Befund fehlt (Rogers 1.3 und 1.8 als X1 mit Z1, Moran 1.1 bis 1.3). (d) Die Stellung als letzter Teil des Kapitels verursacht die Abweichung in 2b.13, ein Querverweis fehlt, der nicht dokumentierte Grund ist ein Punkt für Schritt 3.

**Vorschlag.** „… Zusatzanalysen vorn als Objektsatz (Rogers 1.3, 1.8), im Befundteil (Hilska 4.2, Rogers 2.1, 2.3, 2.4) oder danach (Asimakidis 1.6). Analyseregeln (V2) vorn (Rogers 1.2, 1.9) oder im Befundteil (Hilska 6.1, Veith 2.3), nie nach den Befunden, A5 S11 steht danach (Plan § 3 Task 11). Folge der Stellung für den Schluss in 2b.13.“ Status „erfüllt (Stellung nach Plan)“ bleibt.

### Nr. 10 · B · Zeilen 2b.33 und 2b.35

**Befund.** Beide Zeilen tragen „erfüllt“, obwohl sie Abweichungen vom Korpus nach Projektregeln aufzählen. 2b.35 nennt fünf (Hypothesenentscheidung P7, unerwünschte Ereignisse P10, Datenprüfung P8, Sensitivität P9, unadjustiert neben adjustiert P4), 2b.33 den Ausgangsvergleich ohne Test (Kern 4 von 5 mit Test, P1) und die Messgüte gegen den SESOI (im Kern ohne Vorbild). 2b.37 stuft gleichartige Punkte als „bewusst anders“ ein. Nach der Zählregel zählt Übereinstimmung nur, wo der Text dem Korpus folgt. In 2b.33 steht zudem „erweitert Rogers und Asimakidis gegen die SWC“ unter „vor den Befunden“, Asimakidis 1.7 ist aber der letzte Satz nach den Befunden, vorn steht nur Rogers 1.1.

**Vorschlag.** 2b.35: „erfüllt für Belege, Deutung und Analysezahl, bewusst anders für fünf Punkte (P4, P7 bis P10)“. 2b.33: „erfüllt, bewusst anders beim Ausgangsvergleich ohne Test (P1) und beim Flussdiagramm im Ergebnisteil“ und „(… erweitert Rogers 1.1 vorn, Asimakidis 1.7 am Schluss, beide gegen die SWC)“.

### Nr. 11 · B · ganze Tabelle, dazu 2b.5

**Befund.** Die Tabelle trennt nicht, welche Zeilen die Übereinstimmung mit dem Korpus nach der Zählregel prüfen und welche die Treue zu einer Fundstelle (P1 bis P12, Plan, Projektteile von § 6.1, Budgetabsatz von § 4, § 7). Die Zählung „erfüllt 33 · teilweise 9 · bewusst 5“ (`pruef_2b.txt` § 17) mischt beides und lässt sich als Korpusübereinstimmung lesen. Nach meiner Zuordnung prüfen 19 Zeilen gegen den Korpus (2b.1 bis 2b.7, 2b.9 bis 2b.14, 2b.27, 2b.30, 2b.32 bis 2b.35: erfüllt 13, teilweise 4, bewusst anders 2) und 28 gegen eine Fundstelle (erfüllt 20, teilweise 5, bewusst anders 3). 2b.5 zählt K4 als „erfüllt“, obwohl K4 mangels Vergleichen einzelner Gruppen gegenstandslos ist, und 2b.6 führt dieselbe Prüfkatalogfrage Nr. 3 als „bewusst anders“.

**Vorschlag.** Spalte „Maßstab“ (Korpus nach § 6.5 oder Fundstelle) und getrennte Zählung in § 3.2. 2b.5 als „erfüllt (gegenstandslos)“ kennzeichnen und auf 2b.6 verweisen.

### Nr. 12 · C · Zeile 2b.27

**Befund.** „Kern 4 bis 12 % in fünf Studien“: Die Spanne 4,1 bis 11,8 % gilt für die vier Kernstudien mit O2 als Primärcode (Lloyd, Beato, Negra 2019, Sammoud), Negra 2020 hat O2 nur sekundär (1.2, O1). Die Settingstudien berichten Spanne, Gründe und Schwellen (§ 0 Nr. 5), Kapitel 5 nennt im Text Schwellen und Median, die Verteilung steht in Tab. H2, die Gründe sind nicht erfasst. Die fehlende Spanne im Text nennt die Zeile nicht ausdrücklich.

**Vorschlag.** „Kern 4 bis 12 % in vier Studien, in einer fünften nur als Sekundärcode“ und „Spanne je Spieler nicht im Text (Verteilung in Tab. H2)“.

### Nr. 13 · C · Zeile 2b.19

**Befund.** Die einschlägige Registerzeile 3 fehlt (Teilentscheidung 3c, Schlusslogik mit Musterformulierungen, in der Registerprüfung „erfüllt … mit „Unterschieden“ statt „Effekten““). Die Musterformulierung ist unvollständig zitiert, ihr erster Satz („Ein Gruppenunterschied ist nicht nachweisbar.“) steht in A5 S6. Plan § 3 Task 11 verlangt den Fall „je Zielgröße … im Wortlaut der Musterformulierung“. Die Abweichungen (Präteritum nach F17 § 10, Plural und ein Satz für alle drei wegen der Ordnung in 2b.9, „Unterschieden“ wegen der Wortprüfung „Effekt“) gehören mit Grund in die Zeile.

**Vorschlag.** Registerspalte „Zeile 3c, Zeile 6i, Zeile 10b“, Musterformulierung vollständig, ein Halbsatz zu den Gründen.

### Nr. 14 · C · Zeilen 2b.22 und 2b.23

**Befund.** In 2b.22 fehlt Registerzeile 16 (Voraussetzungen als ein Satz zur verworfenen Prüfung und ein Sammelsatz, Raster 5.2.3 „je Zielgröße in einem Satz“ für Kapitel 5 überholt), in 2b.22 und 2b.23 Zeile 3d (R1, R2, R4).

**Vorschlag.** Ergänzen.

### Nr. 15 · C · Zeile 2b.47

**Befund.** „nach Teil 3 zulässig“ verallgemeinert. Stilprofil Teil 3 lässt nur „ein Komma zwischen zwei Hauptsätzen ohne Konjunktion“ zu, „aber die Teilung in zwei Sätze ist die Regel“. Das trifft die elliptischen Sätze A1 S3, A2 S3, A2 S4, A4 S2 und A5 S5, nicht oder nur bedingt A2 S1 (angehängte Medianangabe), A3 S3 („davon“-Anschluss) und A5 S3 (mit „und“ verbundene Prädikate). Die Handregel wird uneinheitlich angewandt: A2 S2 mit eigener Zahl in der Klammer (45,4 %) gilt als eine Aussage, die angehängte Medianangabe in A2 S1 als zweite. Der Zielwert „Etwa jeder sechste Satz trägt einen Klammerverweis“ bleibt unbewertet, 7 von 29 ist etwa jeder vierte.

**Vorschlag.** „zulässig nach der Komma-Ausnahme: A1 S3, A2 S3, A2 S4, A4 S2, A5 S5 · nicht gedeckt: A2 S1, A3 S3, A5 S3 (Teilung ist die Regel)“, A2 S2 einheitlich einordnen, „7 von 29, über dem Zielwert, alle Klammern sind Objektverweise“.

### Nr. 16 · C · Zeile 2b.9

**Befund.** Neben dem Plan fehlt die Fundstelle F17 § 5a („dann je Zielgröße in fester Reihenfolge“). „alle Formen im Kern belegt“ ist zu pauschal: Der Quantor als Blockbeginn (A5 S3, S6, nach dem Codebuch B1) hat im Kern ein einziges Gegenstück (Hammami 1.3, Quantor über die Tests einer Zielgröße, 1 von 38 Blöcken), die sechs Anfänge mit Sammelbefund gelten nur nach H2.

**Vorschlag.** F17 § 5a ergänzen, „alle Formen im Kern belegt“ durch die Häufigkeiten ersetzen.

### Nr. 17 · C · Zeile 2b.12

**Befund.** 2a.35 beschreibt den Kontrast unadjustiert gegen adjustiert „über zwei Sätze ohne Konnektor (A5 S3, S4)“, 2b.12 „im selben Satz“ (A5 S3). Beides ist vertretbar, die Teiltabellen sollten gleich lesen. Nicht erörtert ist, dass die Einschränkung des 30-m-Befunds (A6 S1, S2) sieben Sätze nach A5 S4 steht. Nach der Zählregel betrifft K9 nur Befundsätze (V1 und Z1 sind keine), der Status ändert sich nicht, als Hinweis für Schritt 3 lohnt der Punkt.

**Vorschlag.** Lesart an 2a.35 angleichen und einen Halbsatz zum Ort der Einschränkung ergänzen.

### Nr. 18 · C · Zeilen 2b.24 und 2b.29

**Befund.** Die acht Meldungen mit Schmerzangabe zu vollständigen Einheiten stehen nur als Differenz (12 − 2 − 2). Das Kennzahlenblatt führt K-10.12 mit allen Teilwerten („12 · 8 · 2 · 2 · 9 Spieler“) unter Berichtsort „T · 5.1 unerwünschte Ereignisse (CONSORT 19)“. 6.1 A6 S2 baut auf diese Differenz („überwiegend zu vollständig durchgeführten Einheiten“), 2b.29 nennt für A6 S2 nur die Bezugsmenge 15.

**Vorschlag.** In 2b.24 den Berichtsort nennen. In 2b.29: „6.1 A6 S2: Bezugsmenge 15 nur in Tab. H2, „überwiegend“ nur per Rechnung aus A3 S3“.

### Nr. 19 · C · Zeilen 2b.7 und 2b.8

**Befund.** „Titel“ ist das Thema aus F17 § 2, das Titelblatt steht nicht in `master_saetze.json`, die Zeile nennt die Quelle nicht (`pruef_2b.txt` § 4 schon). Den Prüfpunkt der Fortsetzungsübergabe „A4 S2 gegen K5 („bei Wiederkehr dieselbe“)“ beantwortet 2b.7 nur mittelbar. 6.1 A3 S7 nennt „Sprung, Beschleunigung und Richtungswechsel“ in anderer Folge (Erklärungssatz, kein Zielgrößenblock), das gehört nach 2 (e).

**Vorschlag.** „Titel (F17 § 2)“. In 2b.7: „A4 S2 (O5) ist kein Befundblock und fällt nicht unter K5, die Folge gegen F17 § 5.1 in 2b.8“. 6.1 A3 S7 für 2 (e) vormerken.

### Nr. 20 · C · Vollständigkeit, Notation

**Befund.** Ohne eigene Zeile bleiben Befund § 7 Nr. 3, Nr. 6 und Nr. 10, § 3.3 „Moderatoren und Untergruppen“ und § 3.4 als Ganzes. § 7 Nr. 6 berührt den „Korpus Ø 336“ für Kapitel 5 in F17 § 5.2 (an denselben acht Studien 347), § 7 Nr. 10 die Vormerkungen G37, auf die mehrere Zeilen verweisen. Kapitel 5 hat keine Moderatoranalyse (B3 fehlt, Gruppe × %PAH nur als Voraussetzung in Tab. H4), § 3.4 ist auf 2a.31, 2b.39 und 2b.43 verteilt. Die Registerspalte mischt „Zeile 9 Nr. 1, 2, 3“ mit den Buchstaben der Registerprüfung (9a, 9c, 9d). Der Kopf von `pruef_2b.py` nennt „Abschnittsnummern 0 bis 16“, die Ausgabe hat § 17.

**Vorschlag.** In § 3.2 ein Satz, dass diese Aussagen Kapitel 5 nicht berühren oder in 2a erledigt sind (für § 7 Nr. 6 mit dem Hinweis auf F17 § 5.2). Registerspalte einheitlich („9a (Nr. 1)“ usw.), Kopf auf „0 bis 17“.

## 4 Reproduktion

| Ausgabe | MD5 in W | MD5 im eigenen Lauf | Ergebnis |
|---|---|---|---|
| pruef_2b.txt | 6bef2dea1ed75d100eb57568f4d9f2ee | 6bef2dea1ed75d100eb57568f4d9f2ee | bytegleich |
| teiltabelle_2b.csv | 219d2871d69341d574f429e9ffa7c5dc | 219d2871d69341d574f429e9ffa7c5dc | bytegleich |
| teiltabelle_2b.md | 8976eb96ee5e7edc296e5f7a888b1532 | 8976eb96ee5e7edc296e5f7a888b1532 | bytegleich |

Lauf ohne Abbruch (alle PRUEF-Bedingungen erfüllt, 68 von 68 Zitaten gefunden), Ausgabe „Teiltabelle 2b: 47 Zeilen · bewusst 5, erfüllt 33, teilweise 9“. `pruef_2b.py` enthält kein Semikolon (chr(59) 0-mal), ebenso `pruef_2b.txt` und `teiltabelle_2b.md`, in der CSV steht es nur als Trennzeichen, in keiner Zelle.

## 5 Nachrechnung an der CSV (Auszug, `zp2b_check/nachrechnung.txt`)

- Befundanteil im Kern: Median 72,48 %, Spanne 26,4 bis 100,0. Ohne B2: Lloyd 69,9 · Hammami 100,0 · Beato 26,4 · Negra 2019 36,8 · Negra 2020 38,8 · Aloui 91,1 · Liu 69,4 · Moran 0,0 · Sammoud 44,3 · Bouafif 100,0, Median 56,83, Spanne 0,0 bis 100,0.
- Vor dem ersten Befund: Kern Sätze Median 3 (0 bis 6), Wortanteil höchstens Beato 67,2 %, danach Moran 41,8, Negra 2020 40,4, Negra 2019 39,8. Z2 nie primär, sekundär davor nur Klusemann 1.1 (O1), 1.3 und 1.6 (O2), danach Veith 3.3.
- Letzter Satz: Kern B 8 (Lloyd B3, Hammami B2, Negra 2019 B4, Aloui B1, Liu B2, Moran B2, Sammoud B2, Bouafif B3), X 2 (Beato, Negra 2020), Klammer am Satzende 5. Erweitert O 4 (Hilska, Klusemann, Rogers, Asimakidis), X 1 (Veith), B 1 (Padrón-Cabo). Kein Ergebnisteil endet mit Z.
- O2 primär: Kern Lloyd 11,8 (im Befundteil), Beato 10,9, Negra 2019 4,1, Sammoud 8,0 (alle vorn), Negra 2020 nur sekundär (1.2 vorn). Setting Klusemann 15,6 (vorn), Veith 15,0 (danach), Rogers 15,5 (danach), Hilska 21,2 (vorn und danach).
- V1: Veith 1.1 und Asimakidis 1.1 vorn, sekundär Hilska 6.1 und Veith 2.3 im Befundteil. V2 primär: Rogers 1.2, 1.9 vorn, Hilska 6.1, Veith 2.3 im Befundteil, sekundär Sammoud 1.1 und Klusemann 1.5 vorn, Lloyd 1.3 im Befundteil. Z1 primär nur Asimakidis 1.6 danach, sekundär Moran 1.1 bis 1.3 und Rogers 1.3, 1.8 vorn, Liu 2.5, Hilska 4.2, Rogers 2.1, 2.3, 2.4 im Befundteil.
- „respectively“ im Kern 8 Sätze in 5 Studien, einschließlich „respectfully“ bei Beato 1.1, wie der Ausdruck B_RESPECTIVELY.

## 6 Als richtig bestätigt

- Wortlaut, Satzkennungen und Codes in allen 47 Zeilen stimmen mit `textstand_saetze.md` und `konsens_2a.csv` überein, mit den oben genannten Ausnahmen bei der Lesart von A6 S4 (2b.40) und A4 S1 (2b.11).
- Korpuszahlen der Zeilen 2b.1, 2b.2, 2b.13, 2b.27 (bis auf Nr. 1 und Nr. 12), 2b.28 (bis auf Nr. 9), 2b.34, 2b.36, 2b.41 und 2b.44 an der CSV und an `textbausteine.txt` nachgerechnet, die Befundzahlen aus § 0 bis § 7 richtig übernommen (K1 bis K10 mit Häufigkeit, Kern 11 von 14, 10 Sätze in 7 Studien, 5 von 38 Blöcken, 4 von 5 mit Test).
- Kennzahlen: K-10.4 = 18, K-10.9 = 15 (Berichtsort A · Tab. H2 Anmerkung), K-10.12 = 12 · 8 · 2 · 2 · 9 Spieler, daraus 50,0 % und 60,0 % in 2b.45 richtig.
- Zielgrößenfolge: Befundblöcke S → C → J in beiden Lesarten (zweite Lesart nur B-Sätze, wie `zielgroessenfolge_text.py`), A4 S2 S, J, C, A5 S11 S, C, B5 S1, S3, 4.1 A4 S2, 4.4.1 bis 4.4.3, 4.7 A3 S1 und 6.1 A3 bis A5 S → C → J, B5 S4 ohne Folge.
- Zuordnung der 24 Sätze von 6.1 in 2b.29 gleich Abgleichbefund § 1.4, alle Objekte, auf die 6.1 baut, sind in Kapitel 5 verwiesen, A4 ohne Bezug in 6.1.
- Projektregeln P1 bis P12 am Satz (2b.15 bis 2b.26) inhaltlich richtig geprüft, Stellen und Vorzeichen in A5 S4, S5 und A6 S2 nach F17 § 5.3, kein Semikolon, kein adverbialer Konnektor, Median 15,0, längster Satz 28.
- Status richtig eingestuft in allen Zeilen außer 2b.2, 2b.6, 2b.11, 2b.33 und 2b.35 (Nr. 2, 4, 6, 10), dazu 2b.5 als gegenstandslos kennzeichnen (Nr. 11) und in 2b.31 den Schluss nicht unter „bewusst anders“ fassen (Nr. 7). Ausdrücklich bestätigt: „teilweise“ in 2b.8, 2b.9, 2b.13, 2b.22, 2b.30, 2b.45, 2b.46 und 2b.47, „bewusst anders“ in 2b.1, 2b.37 und 2b.42.
- Registerzeilen und Teilentscheidungen (1b, 1d bis 1f, 2a, 2c, 6g, 6i, 10d, 10m, V1, U1, U3, U9, c4, c7 bis c9, r1, r2, Zeilen 14 bis 16) existieren und passen zu ihren Zeilen, keine Zeile widerspricht § 2.2 des Abgleichbefunds (2b.22 Schwere C, 2b.45 Schwere B wie dort).
- Vollständigkeit: Prüfkatalog Nr. 1 bis 10, K1 bis K10, P1 bis P12 und alle Prüfpunkte aus Fortsetzungsübergabe § 5 Nr. 4 haben eine Zeile. Die Textbausteine (§ 5.1, § 5.2) sind zu Recht für 2 (c) ausgespart.
- Zitatprüfung des Skripts (68 von 68) an Stichproben selbst nachgelesen: F17 § 5a und § 11.9, Plan § 3 Task 11, Stilprofil Teil 2, 3, 4 und 7, Raster § 3.13, Umfangsdokument § 5.1 (C1), R1, R4, Gliederung v6 Ä16, Textvorschlag 5 § 0 und § 3, Textvorschlag 6.1 § 9.

# Fortsetzungsübergabe 4 — Task „Diskussion: Anwendung der Argumentationsstruktur“ — 03.10.2026

Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext · Stand 03.10.2026, nach der Klickfreigabe des Nachtrags zu 6.1 (Sitzungsuhr)

Anlass: Der Verlauf wurde während des Nachtrags zum Textvorschlag 6.1 automatisch zusammengefasst. Nach der Taskwechselregel des Startprompts (Ausgangsübergabe § 0) ist der laufende Teilschritt, der Nachtrag bis zur Klickfreigabe, abgeschlossen und gesichert: Nachtrag Fassung 3 mit dem Klickergebnis, Teil 0 Rev. 162. Gewechselt wird am Checkpoint nach der Freigabe, vor der Nachführung des Textvorschlags 6.1 und vor dem angewiesenen Einbau. Ausgangsübergabe: `04_Uebergaben\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` (Startprompt § 0, Register § 4, Eingänge für 12b § 5, Sicherung § 7, Taskwechsel § 8). Vorige Fortsetzungsübergaben: Fortsetzung 1 (Schritt 1 und 2a, Dateien § 1.3), Fortsetzung 2 (2b bis 2d mit Zweitprüfung, Dateien § 1.3), Fortsetzung 3 (Schritt 3, Dateien § 1.2, Entwurf des Nachtrags § 5 Nr. 1). Teil 0: Rev. 159, Rev. 160 und Rev. 162.

## 0 Neuer Startprompt (in einen neuen Task einfügen)

```
Task „Diskussion: Anwendung der Argumentationsstruktur“ — Fortsetzung 4 ab der Nachführung des Textvorschlags 6.1 und dem Einbau des Nachtrags

Lies zuerst vollständig: (1) Claude\04_Uebergaben\Uebergabe_Diskussion_Anwendung_Fortsetzung4_2026-10-03.md, (2) die Ausgangsübergabe Claude\04_Uebergaben\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md mit Startprompt § 0 und § 3 bis § 8, (3) Teil 0 der Sitzungsnotizen ab Rev. 159, (4) den freigegebenen Nachtrag Claude\04_Uebergaben\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md (Fassung 3, vor allem § 1, § 4 bis § 8, § 10 und § 11) und den Textvorschlag Claude\04_Uebergaben\Textvorschlag_6.1_2026-10-02.md (§ 0 bis § 7, § 9 und § 11). Führe zuerst den Textvorschlag 6.1 nach § 8 des Nachtrags nach (Markdown, JSON und Erzeuger als Fassung 3, Projektkopie). Baue danach den Nachtrag per Skript in den Master ein, wie ich es mit der Freigabe angewiesen habe: die drei Absätze A3 bis A5 von 6.1 ersetzen, Abgleich, Messskript, Endabgleich, MD5-Prüfung. Word halte ich dabei geschlossen. Danach Schritt 4 (Task 12b). Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.
```

## 1 Erledigt

### 1.1 Nachtrag zum Textvorschlag 6.1 (03.10., Fassung 1 um 14:36 im Ordner, Klick gegen 15:52, Fassung 3 gesichert nach 16:00 Sitzungsuhr)

- **Wortlaut** der in Schritt 3 freigegebenen Potenziale, finanziert mit Stufe 3 der Kürzungsleiter, ausgehend vom Entwurf der Fortsetzungsübergabe 3 § 5 Nr. 1. Geändert sind nur A3, A4 und A5, A1, A2 und A6 bleiben zeichengleich. Der Wortlaut steht in Nachtrag § 1 und in `S3_Nachtrag.json`. Die Tabelle nennt nur die geänderten Sätze, Satznummern alt (neu):

| Satz | Potenzial | Wortlaut | Wörter |
|---|---|---|---|
| A3 S5 | Stufe 3 (⚑ K1) | entfällt (Ramirez-Campillo et al., 2020, die Einleitung trägt die Aussage) | 14 → 0 |
| A3 S7 (neu S6) | P6 | „Beim Sprint war am wenigsten zu erwarten: Programme mit vertikalen Sprüngen und langen Bodenkontakten dürften eher Sprung, Beschleunigung und Richtungswechsel ansprechen (Oliver et al., 2024), Sprintinhalte fehlten.“ | 28 → 27 |
| A4 S4 | P1 | „Eine Metaanalyse fand die Richtungswechselleistung, überwiegend von Mädchen, in keiner Reifegruppe nachweisbar verbessert (Ramirez-Campillo et al., 2023).“ | 20 → 17 |
| A4 S5a (neu S6) | P1 | „Mit beiden ist der eigene Befund vereinbar.“ | 0 → 7 |
| A4 S8 (neu S9) | P2 mit P5 | „Den Abstand könnte weniger die Übungsauswahl als die eigene Umsetzung erklären, auch das Vergleichsprogramm kam ohne Wende aus.“ | 13 → 18 |
| A5 S6 | P1 | „Die Sprunghöhe von Schülern nach dem Wachstumsgipfel blieb in einer älteren kontrollierten Studie nach sechs Wochen ohne nachweisbare Veränderung (Lloyd et al., 2016), was mit dem eigenen Befund vereinbar ist.“ | 24 → 30 |

- **Messung per Skript** (Leerraum-Token und Satzteilung wie Messskript Fassung 4): A1 99 · A2 116 · A3 116 · A4 142 · A5 159 · A6 68 = **700** gegen 700 (im Master bisher 99 · 116 · 131 · 133 · 153 · 68 = 700). 40 Sätze, Median 16,5, längster Satz 31 (A1 S1, unverändert), 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, Belegklammern 14 → 13, Belegstellen 16 → 15, Quellen 9 → 8, Konnektorpaare in Folge 4 → 2. Keine neue Ziffer, kein Name als Satzsubjekt, keine neue Quelle. Ramirez-Campillo et al. (2020) steht danach nur noch in der Einleitung.
- **Markierung nach der Lage im eigenen Intervall** (K-06.2 und K-06.3, im Text keine Zahl): Ramirez-Campillo et al. (2023) und Zheng et al. (2025) „vereinbar“ (A4 S6), Oliver et al. (2024) und Sammoud et al. (2024) Widerspruch, Lloyd et al. (2016) „vereinbar“ mit Lage näherungsweise im Intervall (Modellrechnung aus Tab. 4, g ≈ +0,07, mit angenommener Steigung 0,8 etwa 0,00, keine Messung).
- **Probelauf** an einer Kopie des Masters (`S3_Nachtrag_Probelauf_2026-10-03.py`, Messskript Fassung 4): A3 bis A5 sind die Absätze 3 bis 5 nach der Überschrift „6.1 Einordnung der Ergebnisse“ (w:p-Index 139 bis 141), übrige Absätze zeichengleich, 188 → 188 Absätze, Kopie 40.337 Byte, MD5 `6c1db4554cba8d5b791c7884a28b6169`, bytegleich in Fassung 2 und 3. Messskript an der Kopie: 6.1 700 gegen 700, Absatztext 4.496 gegen 6.350, Prognose 27,8 Seiten (Modellrechnung). Der Master blieb unverändert.
- **Zweitprüfung** durch einen unabhängigen Subagenten (Gegenstand Fassung 1): 15 Befunde, 1 × A, 5 × B, 9 × C, alle eingearbeitet bis auf Nr. 14 (vorgemerkt, Nachtrag § 11 Nr. 7). A: „(1:3)“ in Tab. 5 von Ramirez-Campillo et al. (2023) zählt laut Fußnote ¥ Studien „males:females“, nicht Reifegruppen. Der Richtungswechsel-Befund beruht auf einer Studie mit Jungen und drei mit Mädchen, die Kontrollen waren dreimal Schulsport und einmal Fußball, Distanz Population 2. Derselbe Lesefehler steht in TV 6.1 § 5. B: Lage bei Lloyd et al. (2016) als Modellrechnung prüfbar · „vereinbar“ ist nach Codebuch Regel 9 V1, Kennwert umbenannt · Reifung beim Richtungswechsel nicht ohne Richtung (kleiner Vorteil vor PHV, Gewissheit niedrig) · Liste der Nachführungen in § 8 vollständig gemacht · Vormerkung für die Einleitung (Satz zu Programmen bis sieben Wochen halten). Bericht unverändert im Arbeitsordner, Einarbeitung je Befund in Nachtrag § 9.
- **Fassung 2:** A4 S4 nennt die Population („überwiegend von Mädchen“, +3, 6.1 genau 700), A4 S9 beginnt mit „Den Abstand“, Lage bei Lloyd et al. (2016) als Modellrechnung. T1 und T4 nachgetragen per `S3_T1_T4_Nachtrag_2026-10-03.py`: T1 `RC2023` Feld `population` mit Vermerk zum Richtungswechsel (76 Steckbriefe), T4 neue Zeile `RC2023` „Studienverhältnis (1:3) beim Richtungswechsel“ (170 → 171 Zitierfallen). Das Skript bricht bei einem zweiten Lauf ab.
- **Klickfreigabe** (§ 2) und **Fassung 3** mit dem Klickergebnis in Kopf, § 0, „In Kürze“, § 1, § 3, § 8, § 10 bis § 12 und im JSON-Feld `fassung`. Wortlaut, Satz-CSV, Protokoll des Laufs und Probelauf bytegleich mit Fassung 2, Läufe unter wechselndem `PYTHONHASHSEED` bytegleich.

### 1.2 Dateien (nach Rückschreibung neu gestagt und per MD5 bestätigt)

Ordner `Claude\03_Skripte\Diskussion_Anwendung_2026-10-03\`, neu oder geändert seit Fortsetzungsübergabe 3. Alle übrigen Dateien stehen unverändert in den Fortsetzungsübergaben 1 bis 3.

| Datei | Byte | MD5 |
|---|---:|---|
| `S3_Nachtrag_6_1_2026-10-03.py` (Fassung 3) | 102.016 | `98d6b93b34a22357395a401acc074127` |
| `S3_Nachtrag.json` | 6.840 | `47a682dce7446566f67772ac793cf036` |
| `S3_Nachtrag_Saetze.csv` | 13.041 | `e21b9b06bf21b3a2b54a720da609ab04` |
| `S3_Nachtrag.txt` | 2.915 | `987beee7ac1eacbb4a95258f64781690` |
| `S3_Nachtrag_Probelauf_2026-10-03.py` (Fassung 2) | 5.595 | `fecaac1e73359ae68d155f20fdb87b82` |
| `S3_Nachtrag_Probelauf.txt` | 1.615 | `e226b86200074f0618fe6126f4d7ffea` |
| `S3_Nachtrag_Zweitpruefung_Bericht.md` (neu) | 27.607 | `db8bdafe489e84ae6d22b805663c9689` |
| `S3_T1_T4_Nachtrag_2026-10-03.py` (neu) | 6.566 | `371fb49add71d5a7593d9c4c570ebf9c` |
| `S3_T1_T4_Nachtrag.txt` (neu) | 2.470 | `87df41c9f68f52fc93914abb919cd4ee` |
| `LIESMICH.md` (Abschnitt „Nachtrag 6.1“) | 25.513 | `4625967ba8209d3eb29b95b25eff486f` |

Außerhalb des Arbeitsordners:

| Datei | Byte | MD5 |
|---|---:|---|
| `04_Uebergaben\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md` (Fassung 3) | 75.397 | `4b35973e6770f93234057789fcd87def` |
| `Schreiben\ev3_daten\T1_steckbriefe.csv` (vorher 103.438 Byte, `9f9dd85b…`) | 103.653 | `ae847c32ade026e2903d5f325a312b1f` |
| `Schreiben\ev3_daten\T4_zitierfallen.csv` (vorher 85.384 Byte, `074e70a6…`) | 86.825 | `0d44eae00f7a5b726a68f370abc956d5` |

Projektkopie des Nachtrags `claude/Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md` mit Fassung 3 ersetzt. Teil 0 Rev. 162 mit `03_Skripte\Steuerung_Rev162_2026-10-03.py` und `.txt`. Aufrufe und Reihenfolge der Skripte in `LIESMICH.md`. Unverändert: Master (40.331 Byte, MD5 `2fda214483ffe46d652cb7b7a8882df9`), Textvorschlag 6.1 mit JSON (MD5 `627f6b1504fcdc3ac7ccc5789b06ed41`, 6.210 Byte) und Erzeuger, Ergebnisdokument Fassung 7, Kennzahlenblatt, Zahlenliste des Endabgleichs, Maßnahmenliste.

## 2 Klickergebnisse

Klick 03.10., gegen 15:52 Sitzungsuhr, vier Fragen, alle Antworten wie empfohlen (Nachtrag § 10):

- **A3 (Sprint):** „Freigeben“, mit Stufe 3 (A3 S5 entfällt, ⚑ K1) und P6.
- **A4 (Richtungswechsel):** „Empfehlung freigeben“: A4 S4 mit „überwiegend von Mädchen“, der Grund der Fremdpopulation nur im Begleitteil (Abweichung vom Wortlaut der Populationsregel, nach K2 das zweite Mal so entschieden), A4 S9 „Den Abstand könnte …“. Nicht gewählt: (a) „dürfte“ oder Variante „Da …“, (b) Ramirez-Campillo et al. (2023) aus A4 entfernen (6.1 dann 684).
- **A5 (Sprung):** „Freigeben“.
- **Einbau:** „Per Skript einbauen“ mit dem Ablauf „Nach der Nachführung des Textvorschlags 6.1, sobald der Rechner erreichbar ist: drei Absätze ersetzen, Abgleich, Messskript, Endabgleich, MD5-Prüfung.“ Das ist die ausdrückliche Anweisung zum Einbau. Ausgeführt wird sie in Fortsetzung 4.

## 3 Offene Klicks (in der Reihenfolge, in der sie anfallen)

1. **Nachführung und Einbau:** keine Klickfrage, beides ist angewiesen. Rückfrage nur, wenn der Master vom Referenzstand abweicht und die Abweichung nicht aus einem dokumentierten Rev.-Block stammt, oder wenn der alte Wortlaut von A3 bis A5 nicht zeichengleich gefunden wird (§ 4 B Nr. 1). Dann nicht einbauen, melden.
2. **Schritt 4 (a):** Bauform von 6.2 und 6.3 mit Empfehlung (Gliederung v6, Bauform Sammoud).
3. **Schritt 4 (b):** fehlende Quellen (Stuart, 2010, und H8-Verfahrensquellen) warten oder ohne Beleg schreiben (Übergabe § 5 Nr. 8, Plan § 7.2) · Ort von Hilska et al. (2021), G3 oder G5 · weitere offene Entscheidungen aus dem Gerüst.
4. **Schritt 4 (e):** Freigabe des Textvorschlags 6.2 und 6.3, Einbau per Skript oder Übertragung durch den Verfasser.

## 4 Nächster Schritt mit erstem Arbeitsgang

**A. Nachführung des Textvorschlags 6.1** nach Nachtrag § 8:

1. Rechner verbunden prüfen. Stagen und lesen: `04_Uebergaben\Textvorschlag_6.1_2026-10-02.md`, `03_Skripte\Textvorschlag_6.1_2026-10-02.py` (Erzeuger Fassung 2) und `03_Skripte\Textvorschlag_6.1_2026-10-02.json` (6.210 Byte, MD5 `627f6b1504fcdc3ac7ccc5789b06ed41`), den Nachtrag Fassung 3 mit `S3_Nachtrag.json` und `S3_Nachtrag_Saetze.csv`. Die JSON Fassung 2 vor dem Überschreiben im Container sichern. Sie ist der Maßstab für den alten Wortlaut beim Einbau (B Nr. 2). Eine Kopie nach `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\` ist nach F17 § 1.4 möglich.
2. Erzeuger auf Fassung 3 bringen: A3 bis A5 zeichengleich aus `S3_Nachtrag.json`, A1, A2 und A6 unverändert, dazu jede Zeile der Liste in Nachtrag § 8 (§ 0 Kopf, § 1, § 2 Zug-Tabelle, § 3 Verzichtstabelle mit der neuen Zeile, § 4 Rasterzuordnung, § 5 Belegtabelle mit der Lesart „(1:3)“, § 6 Begleitteil, § 7 Kürzungsleiter, § 9.3 Nr. 1 und Nr. 3, § 9.4, § 11.4). Der Erzeuger trägt A3 bis A5 fest im Quelltext, ein Neulauf ohne Ersetzung erzeugte den alten Wortlaut (Zweitprüfung Nr. 13). Lauf in einen frischen Ausgabepfad, Absätze der neuen JSON per Skript gegen `S3_Nachtrag.json` prüfen (zeichengleich), Erledigung jeder Zeile von § 8 im Lauf protokollieren.
3. Markdown, JSON und Erzeuger zurückschreiben (frischer Ausgabepfad, `expectedMtimeMs`), neu stagen, MD5 vergleichen. Projektkopie `claude/Textvorschlag_6.1_2026-10-02.md` ersetzen (Projektspeicher § 5 Nr. 3).

**B. Einbau per Skript** (angewiesen, Nachtrag § 10 Nr. 4):

1. Word ist geschlossen. Master stagen und gegen den Referenzstand prüfen: 40.331 Byte, MD5 `2fda214483ffe46d652cb7b7a8882df9`, 188 Absätze, keine `word/comments.xml`. Weicht er ab, die Abweichung bestimmen. Nur wenn 6.1 unverändert ist (A1 bis A6 zeichengleich mit der JSON Fassung 2) und die Änderung aus einem dokumentierten Rev.-Block stammt, etwa aus dem parallelen Task, auf dem neuen Stand einbauen. Die Probekopie gilt dann nicht als Erwartungswert. Sonst nicht einbauen, melden.
2. Einbauskript im Arbeitsordner, Vorschlag `S4_Einbau_6_1_2026-10-03.py`, abgeleitet aus `S3_Nachtrag_Probelauf_2026-10-03.py`: alter Wortlaut aus der JSON Fassung 2 zeichengleich gefordert in den Absätzen 3 bis 5 nach der Überschrift „6.1 Einordnung der Ergebnisse“, neuer Wortlaut aus der JSON Fassung 3, übrige Absätze zeichengleich, 188 Absätze. Erwartet bei unverändertem Master: Ausgabe bytegleich mit der Probekopie (40.337 Byte, MD5 `6c1db4554cba8d5b791c7884a28b6169`), sonst den Unterschied vor der Rückschreibung erklären. Danach `validate.py` des docx-Skills wie in Task 12a.
3. Rückschreibung aus frischem Ausgabepfad mit `expectedMtimeMs` des Masters (Word geschlossen), Wartezeit, neu stagen, MD5 gleich der Ausgabe.
4. Abgleich mit `03_Skripte\Abgleich_Kapitel6_1_Master_2026-10-02.py <Master> <Ausgabe> <JSON Fassung 3> <Protokoll>`. Das Skript ist über JSON und Referenz parametrisiert (keine festen Wortzahlen gefunden). Das Protokoll unter eigenem Namen in den Arbeitsordner schreiben, das Protokoll vom 02.10. bleibt.
5. Messskript Fassung 4 am Master (`03_Skripte\Manuskriptstand_2026-09-25.py`, Ausgaben `.txt` und `.csv` wie beim Einbau in Task 12a). Erwartet: 6.1 700 gegen 700, Absatztext 4.496 gegen 6.350, Prognose 27,8 Seiten (Modellrechnung).
6. Endabgleich Fassung 3 in eigenem Unterordner (Vorschlag `03_Skripte\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\`), Zahlenliste `03_Skripte\Endabgleich_Manuskript_2026-09-25_Zahlen.csv` bis Task 18 unverändert. Der Nachtrag führt keine Ziffer ein, Abweichungen gegenüber dem Lauf vom 02.10. sind nur bei den Zitatjahren zu erwarten (Ramirez-Campillo et al., 2020, entfällt in 6.1).
7. TV 6.1 § 11.4 „Einbau des Nachtrags“ mit dem Ergebnis nachtragen, Projektkopie, Rev.-Block in Teil 0, Meldung.

**C. Danach Schritt 4 (Task 12b)** nach Startprompt § 0 und Eingängen § 5 der Ausgangsübergabe, mit den Vormerkungen in § 5 Nr. 5.

## 5 Besonderheiten, die nicht in den Dateien stehen

1. **Umgebung:** Rechner `C:\Users\acul2\OneDrive\Desktop\Bachelorarbeit` (Windows). Eine Shell auf dem Rechner steht nicht zur Verfügung. Gearbeitet wird im Cloud-Container, Zugriff über Verzeichnisliste, Stagen und Rückschreibung. Gestagte Dateien unter `/mnt/user-data/uploads/Bachelorarbeit/…`, Rückschreibung aus einem frischen Ordner unter `/mnt/user-data/outputs/`, bei bestehenden Dateien mit `expectedMtimeMs` aus einer frischen Verzeichnisliste, danach neu stagen und per MD5 vergleichen. Vergeben sind `s3_2026-10-03_a`, `rev159_2026-10-03_a`, `ue3_2026-10-03_a`, `rev160_2026-10-03_a`, `n61_2026-10-03_a`, `n61_2026-10-03_b`, `ue4_2026-10-03_a` und `rev162_2026-10-03_a`. Die Sitzungsuhr ist die Ortszeit des Containers (UTC+1). Jeden Lauf mit `PYTHONDONTWRITEBYTECODE=1` starten, Skripte ohne Semikolon (`SEMI = chr(59)`, Selbstprüfung am Ende). Die Skripte des Arbeitsordners importieren `basis.py` und `absatzfunktion.py` aus `03_Skripte\Argumentationsstruktur_Diskussion_2026-10-02`. Das Nachtragsskript braucht `pdftotext` und die fünf PDFs aus `Ideen und Studien` (Ramirez-Campillo 2023, Zheng 2025, Lloyd 2016, Sammoud 2024, Oliver 2024).
2. **Paralleler Task:** „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (Fortsetzung ab Teilschritt 2 d, Teil 0 Rev. 161) schreibt in dieselben Steuerdokumente und kann später auch den Master ändern. Teil 0 vor jedem Schreiben neu stagen, die Rev.-Nummer ist die nächste freie, Rückschreibung mit `expectedMtimeMs`. Vor dem Einbau den Master neu stagen (§ 4 B Nr. 1).
3. **Projektspeicher:** 1.869.747 von 2.000.000 Byte vor dieser Ablage (der Stand ist seit Fortsetzung 3 gesunken). Ergebnisdokument und Textvorschlag 6.2 und 6.3 passen voraussichtlich nicht hinein, dann gilt die Ordnerfassung. Die Projektkopie der Sitzungsnotizen steht weiter auf Rev. 154. Andere Projektkopien nur nach Rückfrage löschen (Übergabe § 7 Nr. 4).
4. **Budget:** 6.1 bleibt mit dem Nachtrag bei 700 Wörtern, ohne Reserve. Von der Kürzungsleiter sind Stufe 1 und Stufe 3 verbraucht. Es bleiben Stufe 2 (A5 S8, −24, ⚑ F17 § 5.3) und Stufe 4 (A2 S6, −18, nur mit erneuter Prüfung von A4 S9, der sich auf ihre Grenze stützt). Stufe 5 entfällt, weil P1 den Satz A5 S6 braucht.
5. **Vormerkungen für Schritt 4 (12b)** aus Nachtrag § 11 Nr. 3: G3 nennt die Verdünnung als Limitation, A4 S9 nutzt die Umsetzung jetzt als Erklärungsangebot beim Richtungswechsel. G3 wiederholt den Wortlaut nicht und deutet die Umsetzung nicht als Ursache (F17 § 11.2b) · Aufsicht einmal als Korpuseigenschaft (F17 § 6.4), dort auch der Vergleich der Umsetzung mit der betreuten Vergleichsstudie, falls 12b ihn braucht (Sammoud et al., 2024, Adhärenz > 85 % nach T1, nicht in 6.1) · G8 ohne erneute Normwerte · Ramirez-Campillo et al. (2020) für 6.2.1 weiter verfügbar · 6.2: Die Trennung zwischen „vereinbar“ (Zheng et al., 2025) und Widerspruch (Oliver et al., 2024) hängt an 0,05 Abstand zur unteren Grenze des eigenen Intervalls, dazu der Vorbehalt der g-Skala gegenüber Effektstärken der Literatur (TV 4.7 Nr. 44) · Lloyd et al. (2016) als Literaturerwartung in 6.2.1 mit der Modellrechnung, nicht als gemessener Gruppenvergleich.
6. **Vormerkungen für Steuerdokumente** (am Ende des Tasks in die Maßnahmenliste, Taskzeile 12, G37): die Liste aus Fortsetzungsübergabe 2 § 5 Nr. 7 · aus Schritt 3 die Vormerkungen 1 bis 3 am Ende von § 4 des Ergebnisdokuments · aus dem Nachtrag § 11 Nr. 2 (Berichtigungen zum Ergebnisdokument, das nicht neu erzeugt wird), Nr. 4 (T1-Distanzfelder `RC2023`, `Sammoud2024` und `Zheng2025` angleichen, Abweichung P3 an Berichtsraster Rev. 4 und Fassung 18 § 5a, Fassung 18 § 6.4: Grund der Fremdpopulation nur im Begleitteil als Regel aufnehmen, jetzt zweimal entschieden), Nr. 6 (Einleitung, Nr. 7 hier) und Nr. 7 (A5 S6 „nach sechs Wochen plyometrischen Trainings“, +2, nur falls in 6.1 Wörter frei werden).
7. **Schlussfassung der Einleitung (G35):** (a) Den Satz zu Programmen bis sieben Wochen (Absatz 1, Satz 5, Ramirez-Campillo et al., 2020) halten, 6.1 setzt ihn seit Stufe 3 voraus. (b) Im Satz zu Ramirez-Campillo et al. (2023) (Absatz 5, Satz 5) die Population der Richtungswechsel-Evidenz nennen wie in A4 S4.
8. **Keine erneuten Läufe** von `S3_T1_T4_Nachtrag_2026-10-03.py` (bricht ab) und von `T1_T4_Nachtrag_Boumparis_2026-10-02.py` (setzt das Feld `fassung` von `Boumparis2026` zurück, TV 6.1 § 11.3). T1 hat 76 Steckbriefe, T4 171 Zitierfallen.

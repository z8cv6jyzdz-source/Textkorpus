# Fortsetzungsübergabe 5 — Task „Diskussion: Anwendung der Argumentationsstruktur“ — 03.10.2026

Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext · Stand 03.10.2026, nach dem Einbau des Nachtrags zu 6.1 (Sitzungsuhr)

Anlass: Der Verlauf wurde nach dem Einbau des Nachtrags, vor dem Rev.-Block, automatisch zusammengefasst. Nach der Taskwechselregel des Startprompts (Ausgangsübergabe § 0) ist der laufende Arbeitsgang abgeschlossen und gesichert: Textvorschlag 6.1 als Fassung 3 nachgeführt, Nachtrag per Skript in den Master eingebaut, Abgleich, Messskript und Endabgleich ohne neuen Befund, Textvorschlag 6.1 § 11.4 mit dem Ergebnis, Teil 0 Rev. 163. Gewechselt wird am Checkpoint nach der Freigabe und dem angewiesenen Einbau, vor Schritt 4 (a). Ausgangsübergabe: `04_Uebergaben\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` (Startprompt § 0, Register § 4, Eingänge für 12b § 5, Hinweise § 6, Sicherung § 7, Taskwechsel § 8). Vorige Fortsetzungsübergaben: Fortsetzung 1 (Schritt 1 und 2a, Dateien § 1.3), Fortsetzung 2 (2b bis 2d mit Zweitprüfung, Dateien § 1.3), Fortsetzung 3 (Schritt 3, Dateien § 1.2), Fortsetzung 4 (Nachtrag mit Zweitprüfung und Klick, Dateien § 1.2). Teil 0: Rev. 159, Rev. 160, Rev. 162 und Rev. 163.

## 0 Neuer Startprompt (in einen neuen Task einfügen)

```
Task „Diskussion: Anwendung der Argumentationsstruktur“ — Fortsetzung 5 ab Schritt 4 (a) (Task 12b: Zuordnung der Rasterzeilen und Bauform)

Lies zuerst vollständig: (1) Claude\04_Uebergaben\Uebergabe_Diskussion_Anwendung_Fortsetzung5_2026-10-03.md, (2) die Ausgangsübergabe Claude\04_Uebergaben\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md mit Startprompt § 0 und § 3 bis § 8, (3) Teil 0 der Sitzungsnotizen ab Rev. 159, (4) den Befund Claude\02_Befunde\Argumentationsstruktur_Diskussion_RCT_2026-10-02.md (vor allem § 8, § 9, § 12 und § 13), den Kapitelstruktur-Abgleich Claude\02_Befunde\Kapitelstruktur_Abgleich_2026-09-28.md (§ 5 B5, § 6.1, § 7 Nr. 4) und den Textvorschlag Claude\04_Uebergaben\Textvorschlag_6.1_2026-10-02.md (Fassung 3, § 1 und § 9.1), dazu die Arbeitsdateien aus der Fortsetzungsübergabe. Lade den Skill kapiteltext-bachelorarbeit. Setze mit Schritt 4 (a) fort: Master gegen den Stand nach dem Einbau prüfen, dann jede Rasterzeile 6.2.1 bis 6.2.12 und 6.3.1 bis 6.3.5 den Methodenbegründungen, den Stärken oder G1 bis G8 zuordnen (G37 a) und die Bauform als Klickfrage mit Empfehlung vorlegen. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.
```

## 1 Erledigt

### 1.1 Nachführung des Textvorschlags 6.1 (03.10., Fassung 3, erste Rückschreibung 16:29 Sitzungsuhr)

- **Erzeuger** `03_Skripte\Textvorschlag_6.1_2026-10-02.py` auf Fassung 3: A3 bis A5 zeichengleich aus `S3_Nachtrag.json`, A1, A2 und A6 wie Fassung 2, neues JSON-Feld `fassung` mit dem Klick vom 03.10. gegen 15:52 (Schlüsselfolge `abschnitt`, `titel`, `budget`, `fassung`, `absaetze`). **Markdown-Erzeuger** `03_Skripte\tv61_md.py` mit jeder Zeile der Liste in Nachtrag § 8: Kopf (Fassung 3, T4 171), § 0, „In Kürze“, § 1, § 2 Zug-Tabelle, § 3 Verzichtstabelle mit der neuen Zeile zur Fremdpopulation von Ramirez-Campillo et al. (2023), § 4 Rasterzuordnung neu für A3 S1 bis S6, A4 S1 bis S9 und A5 S6, § 5 Belegtabelle mit der Lesart „(1:3)“ (Studien mit Jungen zu Studien mit Mädchen, Distanz Population 2), § 6 Begleitteil, § 7 Kürzungsleiter, § 8 Nr. 5 (Klicks des Nachtrags), § 9.1 Nr. 10, § 9.3 Nr. 1, 3 und 6, § 9.4 Nr. 1 und 2, § 9.5 Nr. 5, § 10, § 11.4.
- **Prüfung** per `S4_Nachfuehrung_TV61_2026-10-03.py`: 10 von 10 Zeilen der Tabelle in Nachtrag § 8 erledigt, A1 bis A6 der JSON zeichengleich mit `S3_Nachtrag.json`, A1, A2 und A6 gleich und A3 bis A5 verschieden gegenüber Fassung 2, zwei Läufe unter `PYTHONHASHSEED` 0 und 4711 bytegleich, kein Semikolon in den drei Skripten, ohne Befund.
- **Messung Fassung 3** (wie Messskript Fassung 4): A1 99 · A2 116 · A3 116 · A4 142 · A5 159 · A6 68 = **700** gegen 700, 40 Sätze, Median 16,5, längster Satz 31 (A1 S1), 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, 13 Belegklammern, acht Quellen. Satzzahl je Absatz: A1 6, A2 6, A3 6, A4 9, A5 8, A6 5.
- **Berichtigungen über § 8 hinaus** (Fehler, die schon in Fassung 2 standen): „Bauplan 11/11“ in § 0, § 2, § 4 und § 7 durch die Häufigkeiten aus Befund § 13 Nr. 1 ersetzt · die Satznummern in A2 haben sich mit Variante A verschoben, in § 3 „A2 S4 … S5“ zu „A2 S5 … S6“ und „(A1 S5, A2 S1, S3)“ zu „S4“, im Schlusssatz von § 4 „(und A2 S4)“ zu „A2 S5“ · „U19“ in § 0 (stand im entfallenen Liu-Satz) zu „U15“ · Verweise in „In Kürze“ und in § 4 angepasst (A5 S5: die Dosis von Sammoud et al., 2024, steht jetzt in A4 S8).
- **Sicherung:** Fassung 2 von Markdown, JSON, Messprotokoll und beiden Erzeugern liegt in `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\`. Die JSON der Fassung 2 war der Maßstab des alten Wortlauts beim Einbau. Projektkopie `claude/Textvorschlag_6.1_2026-10-02.md` mit Fassung 3 und § 11.4 ersetzt.

### 1.2 Einbau des Nachtrags (03.10., 16:31 bis 16:34 Sitzungsuhr, angewiesen per Klick gegen 15:52, Word geschlossen)

- **Eingang:** Master frisch gestagt, Referenzstand `2fda214483ffe46d652cb7b7a8882df9`, 40.331 Byte, 188 Absätze, keine `word/comments.xml`, Dateizeit seit dem Einbau vom 02.10. unverändert. Keine Rückfrage nötig (Fortsetzungsübergabe 4 § 3 Nr. 1).
- **Einbau** per `S4_Einbau_6_1_2026-10-03.py`: A3, A4 und A5 ersetzt (Absätze 3 bis 5 nach der Überschrift „6.1 Einordnung der Ergebnisse“, w:p-Index 139 bis 141), alter Wortlaut zeichengleich mit der JSON der Fassung 2, alle übrigen Absätze zeichengleich, 188 → 188 Absätze, Formatvorlage Standard ohne Direktformatierung. Ausgabe 40.337 Byte, MD5 `6c1db4554cba8d5b791c7884a28b6169`, bytegleich mit der Probekopie des Probelaufs. `validate.py` des docx-Skills mit `--original` bestanden.
- **Rückschreibung** aus `einbau61n_2026-10-03_a` mit `expectedMtimeMs`, 10 s Wartezeit, neu gestagt: MD5 gleich der Ausgabe. Neue Dateizeit des Masters 1791041534066.
- **Abgleich** (`03_Skripte\Abgleich_Kapitel6_1_Master_2026-10-02.py`, Master gegen Ausgabe und JSON der Fassung 3): ohne Befund. A1 bis A6 zeichengleich, 99 · 116 · 116 · 142 · 159 · 68 = 700 Wörter, Überschriften 6 bis 7 an den Positionen 135, 136, 143, 144, 145, 6.2 und 6.3 ohne Text, 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, kein Satz über 32.
- **Messskript Fassung 4** am Master: 6.1 700 gegen 700, Kapitel 6 700 gegen 1.600, Absatztext 4.496 gegen 6.350, 0 Semikola, 0 Abschnittsverweise, 7 Platzhalter (Anhang H), 47 Autor-Jahr-Belege, Prognose 27,8 Seiten (Modellrechnung). Die Ausgabe ist bytegleich mit `03_Skripte\Manuskriptstand_2026-09-25.txt` und `.csv` vom 02.10., dort deshalb nicht neu geschrieben, Kopie als `S4_Manuskriptstand.txt` und `.csv`.
- **Endabgleich Fassung 3** in `03_Skripte\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\`: 382 Zahlen statt 383, weil in 6.1 das Zitatjahr 2020 mit Ramirez-Campillo et al. (2020) entfällt (Zitatjahre 90 → 89). In 6.1 stehen 25 Zahlen: 15 Zitatjahre, 7 Testnamen und Messstrecken, 3 Klassifikationsartefakte („15“ in U15 und in „15 bis 40 m“, „90“ im 90. Perzentil), keine Ergebniszahl. Satzprüfungen 23, Abweichungen 2 wie am 02.10. (Tab. 1 bis Task 18 nicht im Master, P-09), Vorschläge 0. Zahlenliste `03_Skripte\Endabgleich_Manuskript_2026-09-25_Zahlen.csv` bis Task 18 unverändert.
- **Textvorschlag 6.1 § 11.4** mit dem Ergebnis des Einbaus, zweite Rückschreibung, Projektkopie erneut ersetzt.

### 1.3 Dateien (nach Rückschreibung neu gestagt und per MD5 bestätigt, erneut gestagt gegen 16:43 Sitzungsuhr)

Ordner `Claude\03_Skripte\Diskussion_Anwendung_2026-10-03\`, neu oder geändert seit Fortsetzungsübergabe 4. Alle übrigen Dateien stehen unverändert in den Fortsetzungsübergaben 1 bis 4.

| Datei | Byte | MD5 |
|---|---:|---|
| `S4_Nachfuehrung_TV61_2026-10-03.py` (neu) | 16.593 | `b053bb01025914f462c3836d2edf0e7f` |
| `S4_Nachfuehrung_TV61.txt` (neu, Endstand mit § 11.4) | 7.054 | `4741d737f1f8af9050c076b51b0d0b80` |
| `S4_Einbau_6_1_2026-10-03.py` (neu) | 7.544 | `a7e5fda98227eaf688e4a018bfc96bb4` |
| `S4_Einbau_6_1_Protokoll.txt` (neu) | 4.087 | `20684d14d2a1103962a37fe546d6207e` |
| `S4_Abgleich_Kapitel6_1_Master.txt` (neu) | 1.776 | `0b810abd3a028b12137c8e942ef86c75` |
| `S4_Manuskriptstand.txt` (neu) | 8.057 | `732e94b03643c7dbaecfb7200daaae64` |
| `S4_Manuskriptstand.csv` (neu) | 3.219 | `718b6e2103fb01971ceeaca8298f2b7c` |
| `LIESMICH.md` (Abschnitt „Fortsetzung 4“) | 32.407 | `49b1541c93fa5d877b92e12c452e3e5a` |

Außerhalb des Arbeitsordners:

| Datei | Byte | MD5 |
|---|---:|---|
| `Schreiben\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (vorher 40.331 Byte, `2fda2144…`) | 40.337 | `6c1db4554cba8d5b791c7884a28b6169` |
| `04_Uebergaben\Textvorschlag_6.1_2026-10-02.md` (Fassung 3 mit § 11.4) | 123.351 | `02d7e09c12f655476ca202352611071e` |
| `03_Skripte\Textvorschlag_6.1_2026-10-02.json` (Fassung 3) | 6.460 | `30913b2113b3de33bfc763bdf547eb08` |
| `03_Skripte\Textvorschlag_6.1_2026-10-02.txt` (Fassung 3) | 1.059 | `25f83ed1b90bd9bfbbbeffdd67ecdbcd` |
| `03_Skripte\Textvorschlag_6.1_2026-10-02.py` (Fassung 3) | 14.375 | `f2e03ccfb164be990783a6c1549b83d1` |
| `03_Skripte\tv61_md.py` (Fassung 3) | 125.812 | `28640ccbd5595de4789dc6d10c2543ba` |
| `03_Skripte\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\Endabgleich_Manuskript_2026-09-25.txt` | 8.680 | `0ad2fcd315d8a941815a16a32682bfe7` |
| `03_Skripte\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\Endabgleich_Manuskript_2026-09-25_Zahlen.csv` | 54.610 | `8417969f78bc4e60163f4232c65434b2` |
| `03_Skripte\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\Abgleichprotokoll_Manuskript_2026-09-25.md` | 9.936 | `78445b19e75bcb098d8acde7cc9571dc` |
| `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\Textvorschlag_6.1_2026-10-02.md` (Fassung 2) | 98.346 | `c3de94d3bbfaa82f32f98fff09ea8364` |
| `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\Textvorschlag_6.1_2026-10-02.json` (Fassung 2) | 6.210 | `627f6b1504fcdc3ac7ccc5789b06ed41` |
| `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\Textvorschlag_6.1_2026-10-02.py` (Fassung 2) | 13.379 | `c7ee7f7955088996db797830fa4af013` |
| `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\Textvorschlag_6.1_2026-10-02.txt` (Fassung 2) | 982 | `8a0d0ffd6b0fb491ba8901b939908413` |
| `_Archiv\_ersetzt_2026-10-03_Nachtrag_6_1\tv61_md.py` (Fassung 2) | 96.723 | `6ee0a45893aad489ad6c2abee06deedf` |

Dazu diese Übergabe mit Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung5_2026-10-03.md` und Teil 0 Rev. 163 mit `03_Skripte\Steuerung_Rev163_2026-10-03.py` und `.txt`. Aufrufe und Reihenfolge der Skripte in `LIESMICH.md`, Abschnitt „Fortsetzung 4“. Unverändert: Ergebnisdokument `02_Befunde\Abgleich_Diskussion_6.1_Argumentationsstruktur_2026-10-03.md` (Fassung 7), Nachtrag `04_Uebergaben\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md` (Fassung 3, MD5 `4b35973e…`), `S3_Nachtrag.json` (MD5 `47a682dc…`), T1 (76 Steckbriefe) und T4 (171 Zitierfallen), Kennzahlenblatt, Zahlenliste des Endabgleichs, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste.

## 2 Klickergebnisse

Keine neuen Klicks in dieser Sitzung. Nachführung und Einbau folgten dem Klick vom 03.10. gegen 15:52 Sitzungsuhr (Fortsetzungsübergabe 4 § 2, Einbau „Per Skript einbauen“ nach der Nachführung). Eine Rückfrage war nicht nötig: Der Master entsprach dem Referenzstand, der alte Wortlaut von A3 bis A5 stand zeichengleich, die Ausgabe war bytegleich mit der Probekopie.

## 3 Offene Klicks (in der Reihenfolge, in der sie anfallen)

1. **Schritt 4 (a):** Bauform von 6.2 und 6.3 mit Empfehlung. Ausgangspunkt ist die festgelegte Bauform aus dem Kapitelstruktur-Abgleich (Methodenbegründungen → Stärken → Scharniersatz → G1 bis G8 → Ausblick mit der letzten Limitation verschmolzen). Zu entscheiden ist vor allem der vorgeschaltete Methodenabsatz, der im Korpus kein Vorbild hat: Befund § 12.4 Nr. 2 empfiehlt 6.2.8 und 6.2.11 im Dreischritt nach Sammoud et al. (2024, Sätze 5 bis 7) am Anfang des Stärkenzugs und 6.2.9 als K-Zeile nur bei freiem Budget.
2. **Schritt 4 (b):** fehlende Quellen (Stuart, 2010, und die H8-Verfahrensquellen) warten oder ohne Beleg schreiben (Ausgangsübergabe § 5 Nr. 8, Plan § 7.2) · Ort von Hilska et al. (2021), G3 oder G5 · weitere offene Entscheidungen aus dem Gerüst.
3. **Schritt 4 (e):** Freigabe des Textvorschlags 6.2 und 6.3, Einbau per Skript oder Übertragung durch den Verfasser.

## 4 Nächster Schritt mit erstem Arbeitsgang

**Schritt 4 (a) (Task 12b): Zuordnung der Rasterzeilen und Bauform**

1. Rechner verbunden prüfen. Master frisch stagen und gegen den Stand nach dem Einbau prüfen: 40.337 Byte, MD5 `6c1db4554cba8d5b791c7884a28b6169`, 188 Absätze, keine `word/comments.xml`, 6.1 zeichengleich mit `03_Skripte\Textvorschlag_6.1_2026-10-02.json` (Fassung 3), 6.2 und 6.3 ohne Text. Am schnellsten mit `Abgleich_Kapitel6_1_Master_2026-10-02.py <Master> <Master> <JSON Fassung 3> <Protokoll>`. Weicht die MD5 ab, die Abweichung bestimmen: F9 durch den Verfasser (dann muss das Messskript Fassung 4 dieselben Werte liefern, 6.1 700, Absatztext 4.496) oder ein dokumentierter Rev.-Block des parallelen Tasks „Ergebnisse“ (Kapitel 5 darf sich geändert haben, 6.1 nicht). Jede andere Abweichung vor dem Weiterarbeiten melden.
2. Eingänge lesen: Ausgangsübergabe § 5 Nr. 1 bis 8, darin Textvorschlag 6.1 § 9.1 Nr. 1 bis 10 (Nr. 10 neu aus dem Nachtrag, § 5 Nr. 6 hier), Befund § 12.4 (Absatz „6.2 und 6.3“ mit dem Zuordnungsvorschlag), Kapitelstruktur-Abgleich § 5 B5, § 6.1 Zeile 4.2, Ä17 und § 7 Nr. 4, Berichtsraster § 3.14 (Zeilen 6.2.1 bis 6.2.12 und 6.3.1 bis 6.3.5 mit Etikett P, P°, K, E), Fassung 17 § 12 G1 bis G8. Voraussetzungsprüfungen und Umfangsdokument liegen nur als `.docx` und `.pdf` vor.
3. Zuordnungstabelle als Datei, Vorschlag `03_Skripte\Diskussion_Anwendung_2026-10-03\S4a_Rasterzuordnung_12b.md`, Prüfungen per Skript: je Rasterzeile Etikett, Inhalt, Ort (Methodenbegründung, Stärke, G1 bis G8, Vormerkung für Kapitel 7), Teilung einer Zeile auf mehrere Orte (6.2.7, 6.2.9 und 6.2.10 nach dem Vorschlag in Befund § 12.4), Grundlage, Kennungen, Quellen mit Volltextstatus und T4-Prüfung, Richtwert der Wörter je Ort (nur die Summe 900 ist verbindlich, E4). Zu prüfen: Jede P- und P°-Zeile hat einen Ort, 6.2.1 (Präzision) und 6.2.2 (Multiplizität) bleiben in G1 erkennbar, keine Aussage aus 6.1 wird wörtlich wiederholt.
4. Bauform als Klickfrage mit Empfehlung (§ 3 Nr. 1), Anteile nach Sammoud et al. (2024) auf 900 umgerechnet als Orientierung (Befund § 12.4). Danach Rückschreibung, MD5, Meldung. Checkpoint nach (a).

**Danach** Schritt 4 (b) bis (e) und Schritt 5 nach Startprompt § 0 der Ausgangsübergabe, am Ende des Tasks Maßnahmenliste (Taskzeile 12, G37) und Rev.-Block.

## 5 Besonderheiten, die nicht in den Dateien stehen

1. **Umgebung:** Rechner `C:\Users\acul2\OneDrive\Desktop\Bachelorarbeit` (Windows). Eine Shell auf dem Rechner steht nicht zur Verfügung. Gearbeitet wird im Cloud-Container, Zugriff über Verzeichnisliste, Stagen und Rückschreibung. Gestagte Dateien unter `/mnt/user-data/uploads/Bachelorarbeit/…`, Rückschreibung aus einem frischen Ordner unter `/mnt/user-data/outputs/`, bei bestehenden Dateien mit `expectedMtimeMs` aus einer frischen Verzeichnisliste, danach neu stagen und per MD5 vergleichen. Vergeben sind `s3_2026-10-03_a`, `rev159_2026-10-03_a`, `ue3_2026-10-03_a`, `rev160_2026-10-03_a`, `n61_2026-10-03_a`, `n61_2026-10-03_b`, `ue4_2026-10-03_a`, `rev162_2026-10-03_a`, `n61_2026-10-03_c`, `n61_2026-10-03_d`, `einbau61n_2026-10-03_a`, `einbau61n_2026-10-03_b`, `ue5_2026-10-03_a` und `rev163_2026-10-03_a`. Die Sitzungsuhr ist die Ortszeit des Containers (UTC+1). Jeden Lauf mit `PYTHONDONTWRITEBYTECODE=1` starten, Skripte ohne Semikolon (`SEMI = chr(59)`, Selbstprüfung am Ende). Die Skripte des Arbeitsordners importieren `basis.py` und `absatzfunktion.py` aus `03_Skripte\Argumentationsstruktur_Diskussion_2026-10-02`. Validator des docx-Skills: `/mnt/skills/public/docx/scripts/office/validate.py <docx> --original <orig>`.
2. **Präfixe im Arbeitsordner:** `S4_` ohne Buchstaben steht für die Nachführung und den Einbau aus Fortsetzung 4, nicht für Schritt 4. Für Schritt 4 die Präfixe `S4a_` bis `S4e_` nach Teilschritt verwenden, für Schritt 5 `S5_`, und `LIESMICH.md` je Teilschritt fortschreiben.
3. **Paralleler Task:** „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (zuletzt Teil 0 Rev. 161, Fortsetzung ab Teilschritt 2 d) schreibt in dieselben Steuerdokumente und kann den Master ändern (Kapitel 5). Teil 0 vor jedem Schreiben neu stagen, die Rev.-Nummer ist die nächste freie, Rückschreibung mit `expectedMtimeMs`. Vor jedem Einbau den Master neu stagen.
4. **Projektspeicher:** 1.890.519 von 2.000.000 Byte vor der Projektkopie dieser Übergabe. Ein Textvorschlag 6.2 und 6.3 im Umfang von Textvorschlag 6.1 passt nicht mehr hinein, dann gilt die Ordnerfassung, das steht im Rev.-Block. Die Projektkopie der Sitzungsnotizen steht weiter auf Rev. 154. Andere Projektkopien nur nach Rückfrage löschen (Ausgangsübergabe § 7 Nr. 4).
5. **6.1 im Master (Fassung 3):** 700 Wörter ohne Reserve. Von der Kürzungsleiter sind Stufe 1 und Stufe 3 verbraucht. Es bleiben Stufe 2 (A5 S8, −24, ⚑ F17 § 5.3) und Stufe 4 (A2 S6, −18, nur mit erneuter Prüfung von A4 S9, der sich auf ihre Grenze stützt). Stufe 5 entfällt, weil P1 den Satz A5 S6 braucht. 6.2 und 6.3 wiederholen keine Aussage aus 6.1 wörtlich (Bauplan § 8).
6. **Vormerkungen für Schritt 4 (12b)**, alle in Textvorschlag 6.1 § 9.1 Nr. 1 bis 10, aus dem Nachtrag (§ 11 Nr. 3, dort § 9.1 Nr. 10): G3 nennt die Verdünnung als Limitation, A4 S9 nutzt die Umsetzung als Erklärungsangebot beim Richtungswechsel. G3 wiederholt den Wortlaut nicht und deutet die Umsetzung nicht als Ursache (F17 § 11.2b) · Aufsicht einmal als Korpuseigenschaft (F17 § 6.4), dort auch der Vergleich der Umsetzung mit der betreuten Vergleichsstudie, falls 12b ihn braucht (Sammoud et al., 2024, Adhärenz über 85 % nach T1, nicht in 6.1) · G8 ohne erneute Normwerte · Ramirez-Campillo et al. (2020) für 6.2.1 weiter verfügbar, in 6.1 nicht mehr zitiert · 6.2: Die Trennung zwischen „vereinbar“ (Zheng et al., 2025) und Widerspruch (Oliver et al., 2024) hängt an 0,05 Abstand zur unteren Grenze des eigenen Intervalls, dazu der Vorbehalt der g-Skala gegenüber Effektstärken der Literatur (Textvorschlag 4.7 Nr. 44) · Lloyd et al. (2016) als Literaturerwartung in 6.2.1 mit der Modellrechnung, nicht als gemessener Gruppenvergleich · vor 12b T1 `Liu2024` angleichen (Distanz 2 · 1 · 2 gegen 1 · 1 · 0 der Belegtabelle, § 9.1 Nr. 4, am 03.10. gegen 16:45 in T1 noch offen).
7. **Vormerkungen für Steuerdokumente** (am Ende des Tasks in die Maßnahmenliste, Taskzeile 12, G37): unverändert die Liste aus Fortsetzungsübergabe 4 § 5 Nr. 6 · dazu Taskzeile 12 (12a): Nachtrag Argumentationsstruktur eingebaut am 03.10., 16:31 bis 16:34, Textvorschlag 6.1 Fassung 3, Abgleich, Messskript und Endabgleich ohne neuen Befund · Textvorschlag 6.1 § 9.5 Nr. 4 und 5 (Berichtsraster § 3.14 Ist-Spalte 6.1.1 bis 6.1.4, Fassung 18, T1-Distanzfelder) gelten unverändert.
8. **Schlussfassung der Einleitung (G35):** (a) Den Satz zu Programmen bis sieben Wochen (Absatz 1, Satz 5, Ramirez-Campillo et al., 2020) halten, 6.1 setzt ihn seit Stufe 3 voraus, die Einleitung ist jetzt die einzige Stelle der Dosisaussage dieser Metaanalyse (Textvorschlag 6.1 § 9.3 Nr. 3). (b) Im Satz zu Ramirez-Campillo et al. (2023) (Absatz 5, Satz 5) die Population der Richtungswechsel-Evidenz nennen wie in A4 S4 (§ 9.3 Nr. 6).
9. **Keine erneuten Läufe** von `S3_T1_T4_Nachtrag_2026-10-03.py` (bricht ab), `T1_T4_Nachtrag_Boumparis_2026-10-02.py` (setzt das Feld `fassung` von `Boumparis2026` zurück, Textvorschlag 6.1 § 11.3) und `S4_Einbau_6_1_2026-10-03.py` (fordert 6.1 in Fassung 2 und bricht am heutigen Master ab, so gewollt). Das Einbauskript vom 02.10. (`03_Skripte\Master_6_1_2026-10-02.py`) gilt für den Stand vor dem ersten Einbau und wird nicht wieder verwendet. `S4_Nachfuehrung_TV61_2026-10-03.py` ist wiederholbar (Aufruf in `LIESMICH.md`, braucht JSON und Markdown der Fassung 2 aus dem Archiv). T1 hat 76 Steckbriefe, T4 171 Zitierfallen.

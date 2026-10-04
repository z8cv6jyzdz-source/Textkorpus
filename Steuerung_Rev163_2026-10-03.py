# -*- coding: utf-8 -*-
"""Steuerung_Rev163_2026-10-03.py — Rev.-Block 163 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Fortsetzung 4: Nachführung des Textvorschlags 6.1 (Fassung 3) und
Einbau des Nachtrags in den Master, Taskwechsel nach automatischer Zusammenfassung des Verlaufs (Fortsetzungsübergabe 5).
Setzt den Block vor den jüngsten Block (Rev. 162) und ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev163_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == 'c8dba91fa1d4f71ace519afd3860baa6', MD5_VORHER  # gestagt 03.10. gegen 16:40 Sitzungsuhr, Stand Rev. 162
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 162 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 163 — siehe Block oben.) Zuvor: (Rev. 162 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 163' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 163, 03.10.2026, 16:50 Sitzungsuhr, Auftrag 03.10., 16:11 mit dem Startprompt aus Fortsetzungsübergabe 4 § 0): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Textvorschlag 6.1 als Fassung 3 nachgeführt, Nachtrag per Skript in den '
    'Master eingebaut (A3 bis A5 von 6.1), Abgleich, Messskript und Endabgleich ohne neuen Befund, Taskwechsel nach automatischer '
    'Zusammenfassung des Verlaufs, Fortsetzungsübergabe 5, Fortsetzung ab Schritt 4 (a) (Task 12b)',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung4_2026-10-03.md` § 0: zuerst den Textvorschlag '
    '6.1 nach § 8 des Nachtrags nachführen (Markdown, JSON und Erzeuger als Fassung 3, Projektkopie), danach den Nachtrag per Skript in den '
    'Master einbauen, wie mit der Freigabe angewiesen (A3 bis A5 von 6.1 ersetzen, Abgleich, Messskript, Endabgleich, MD5-Prüfung, Word '
    'geschlossen), danach Schritt 4 (Task 12b). Dazu Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.',
    '',
    '**Ergebnis:** (1) **Nachführung des Textvorschlags 6.1 (Fassung 3):** Erzeuger `03_Skripte\\Textvorschlag_6.1_2026-10-02.py` mit A3 '
    'bis A5 zeichengleich aus `S3_Nachtrag.json` und dem neuen Feld `fassung`, Markdown-Erzeuger `03_Skripte\\tv61_md.py` mit jeder Zeile '
    'der Liste in Nachtrag § 8. Prüfung per `S4_Nachfuehrung_TV61_2026-10-03.py`: 10 von 10 Zeilen erledigt, A1 bis A6 zeichengleich mit '
    '`S3_Nachtrag.json`, zwei Läufe unter verschiedenem `PYTHONHASHSEED` bytegleich, ohne Befund. 6.1 misst 700 gegen 700 (99 · 116 · 116 · '
    '142 · 159 · 68), 40 Sätze, Median 16,5, längster Satz 31, 13 Belegklammern, acht Quellen. Fassung 2 von Markdown, JSON, Messprotokoll '
    'und beiden Erzeugern in `_Archiv\\_ersetzt_2026-10-03_Nachtrag_6_1\\`. (2) **Einbau** 16:31 bis 16:34 per '
    '`S4_Einbau_6_1_2026-10-03.py`: Master im Referenzstand (`2fda2144…`, 40.331 Byte, 188 Absätze, keine comments.xml), A3 bis A5 ersetzt '
    '(Absätze 3 bis 5 nach „6.1 Einordnung der Ergebnisse“, w:p-Index 139 bis 141), alter Wortlaut zeichengleich mit der JSON der Fassung 2, '
    'übrige Absätze zeichengleich, 188 → 188, Ausgabe bytegleich mit der Probekopie des Probelaufs (`6c1db455…`, 40.337 Byte), `validate.py` '
    'bestanden, Rückschreibung mit mtime-Prüfung, neu gestagt, MD5 gleich. (3) **Abgleich** Master gegen Ausgabe und JSON der Fassung 3 ohne '
    'Befund. **Messskript Fassung 4:** 6.1 700 gegen 700, Absatztext 4.496 gegen 6.350, 0 Semikola, 0 Abschnittsverweise, Prognose 27,8 '
    'Seiten (Modellrechnung), bytegleich mit der Messung vom 02.10. **Endabgleich Fassung 3** in '
    '`03_Skripte\\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\\`: 382 Zahlen statt 383 (in 6.1 entfällt das Zitatjahr 2020), Satzprüfungen 23, '
    'Abweichungen 2 wie am 02.10., Vorschläge 0. (4) **Textvorschlag 6.1 § 11.4** mit dem Ergebnis des Einbaus, Projektkopie ersetzt. '
    '(5) **Taskwechsel** nach automatischer Zusammenfassung des Verlaufs am Checkpoint nach Freigabe und Einbau: Fortsetzungsübergabe 5 mit '
    'neuem Startprompt (§ 0), Arbeitsgängen und Dateien (§ 1), offenen Klicks (§ 3), Schritt 4 (a) als erstem Arbeitsgang (§ 4) und den '
    'Besonderheiten (§ 5). Keine neuen Klicks.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Textvorschlag 6.1 trug schon in Fassung 2 „Bauplan 11/11“ (§ 0, § 2, § 4, § 7), '
    'berichtigt nach Befund § 13 Nr. 1. (2) Die Satznummern in A2 hatten sich mit Variante A verschoben, in § 3 und im Schlusssatz von § 4 '
    'berichtigt (A2 S5 und S6 statt S4 und S5). (3) § 0 nannte „U19“ aus dem entfallenen Liu-Satz, berichtigt auf U15. (4) Die erste Fassung '
    'der Prüfung im Nachführungsskript verlangte, dass „11/11“ im Markdown gar nicht mehr vorkommt. § 9.5 Nr. 5 zitiert die Angabe aber als '
    '„Bauplan (11/11)“. Die Bedingung prüft jetzt § 0, § 2, § 4 und § 7 und genau dieses eine Zitat.',
    '',
    '**Stand der Dateien:** Neu: im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` die Dateien '
    '`S4_Nachfuehrung_TV61_2026-10-03.py` mit `.txt`, `S4_Einbau_6_1_2026-10-03.py` mit `S4_Einbau_6_1_Protokoll.txt`, '
    '`S4_Abgleich_Kapitel6_1_Master.txt`, `S4_Manuskriptstand.txt` und `.csv` · `03_Skripte\\Endabgleich_2026-10-03_Kapitel6_1_Nachtrag\\` '
    '(drei Dateien) · `_Archiv\\_ersetzt_2026-10-03_Nachtrag_6_1\\` (Fassung 2, fünf Dateien) · '
    '`04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung5_2026-10-03.md` (20.656 Byte, MD5 `972f7e54…`) mit dem neuen Startprompt '
    '(§ 0) und Projektkopie · `03_Skripte\\Steuerung_Rev163_2026-10-03.py` mit `.txt`. Geändert: Master '
    '`Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (40.337 Byte, MD5 `6c1db455…`, vorher `2fda2144…`) · '
    '`04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` Fassung 3 mit § 11.4 (123.351 Byte, MD5 `02d7e09c…`, Projektkopie ersetzt) · '
    '`03_Skripte\\Textvorschlag_6.1_2026-10-02.json` (6.460 Byte, MD5 `30913b21…`), `.txt`, `.py` und `03_Skripte\\tv61_md.py` (Fassung 3) · '
    '`LIESMICH.md` (Abschnitt „Fortsetzung 4“, 32.407 Byte) · diese Notizen (Rev. 163 auf Rev. 162), nur im Ordner, die Projektkopie bleibt '
    'auf Rev. 154. Projektspeicher 1.890.519 Byte vor der Ablage der Übergabe, danach rechnerisch 1.911.175 von 2.000.000. Unverändert: '
    'Ergebnisdokument Fassung 7, Nachtrag Fassung 3, `S3_Nachtrag.json`, T1 (76 Steckbriefe) und T4 (171 Zitierfallen), Kennzahlenblatt, '
    'Zahlenliste des Endabgleichs, `03_Skripte\\Manuskriptstand_2026-09-25.txt` und `.csv` (Messung bytegleich), Fassung 17, Bauplan, '
    'Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Fortsetzungsübergabe 5 § 5 Nr. 7). Rückschreibung '
    'aus eigenen Ausgabepfaden (`n61_2026-10-03_c` 12 Dateien, `einbau61n_2026-10-03_a` Master, `einbau61n_2026-10-03_b` 12 Dateien), danach '
    'neu gestagt und per MD5 verglichen, 25 von 25 gleich, gegen 16:43 alle 22 Dateien der Übergabe § 1.3 erneut bestätigt.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus '
    '`04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung5_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) dort in Schritt 4 '
    'die Klicks zur Bauform von 6.2 und 6.3, zu den fehlenden Quellen und zum Ort von Hilska et al. (2021), danach Freigabe und Einbau von '
    '6.2 und 6.3 · (3) aus Rev. 152 bis 162 weiter offen: Fortsetzung des Tasks „Ergebnisse“ (Rev. 161), F9 im Master, Vormerkungen G37 (o) '
    'und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 5 ab Schritt 4 (a) (Task 12b): Master gegen den Stand nach dem Einbau prüfen (`6c1db455…`, 40.337 '
    'Byte), dann jede Rasterzeile 6.2.1 bis 6.2.12 und 6.3.1 bis 6.3.5 den Methodenbegründungen, den Stärken oder G1 bis G8 zuordnen (G37 a), '
    'ausgehend vom Kapitelstruktur-Abgleich und Befund § 12.4, Bauform als Klickfrage mit Empfehlung. Danach Schritt 4 (b) bis (e), Schritt 5, '
    'am Ende des Tasks Maßnahmenliste und Rev.-Block.',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 162'
pos = [i for i, z in enumerate(zeilen) if z.startswith(ANKER)]
assert len(pos) == 1, pos
neu = zeilen[:pos[0]] + BLOCK + zeilen[pos[0]:]
neu[1] = STAND_NEU + zeilen[1][len(STAND_ALT):]
# Prüfung: außer Zeile 2 und dem eingefügten Block ist alles gleich
assert neu[:1] == zeilen[:1] and neu[2:pos[0]] == zeilen[2:pos[0]]
assert neu[pos[0] + len(BLOCK):] == zeilen[pos[0]:]
ausgabe = '\n'.join(neu).encode('utf-8')
open(AUS, 'wb').write(ausgabe)
MD5_NACHHER = hashlib.md5(ausgabe).hexdigest()
prot = [
    f'Eingabe: {len(roh)} Byte, MD5 {MD5_VORHER}',
    f'Ausgabe: {len(ausgabe)} Byte, MD5 {MD5_NACHHER}',
    f'Block vor Zeile {pos[0] + 1} (Rev. 162) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

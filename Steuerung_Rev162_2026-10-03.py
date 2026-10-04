# -*- coding: utf-8 -*-
"""Steuerung_Rev162_2026-10-03.py — Rev.-Block 162 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Nachtrag zum Textvorschlag 6.1 mit Zweitprüfung und Klickfreigabe,
Taskwechsel nach der Freigabe (Fortsetzungsübergabe 4). Setzt den Block vor den jüngsten Block (Rev. 161, paralleler Task) und
ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev162_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == 'aadd858046ead27e93f9ed0555d85e90', MD5_VORHER  # gestagt 03.10., 16:08 Sitzungsuhr, Stand Rev. 161 (paralleler Task)
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 161 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 162 — siehe Block oben.) Zuvor: (Rev. 161 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 162' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 162, 03.10.2026, 16:10 Sitzungsuhr, Auftrag 03.10., 14:15 mit dem Startprompt aus Fortsetzungsübergabe 3 § 0): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Nachtrag zum Textvorschlag 6.1 mit Zweitprüfung und Klickfreigabe (A3, A4, A5 '
    'wie empfohlen, Einbau per Skript angewiesen), Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzungsübergabe 4, '
    'Fortsetzung ab der Nachführung des Textvorschlags 6.1 und dem Einbau, kein Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung3_2026-10-03.md` § 0: Nachtrag zum Textvorschlag '
    '6.1 mit den in Schritt 3 freigegebenen Potenzialen P1, P2 mit P5 und P6, finanziert mit Stufe 3 der Kürzungsleiter, ausgehend vom Entwurf '
    'in § 5 Nr. 1, mit Wortlaut, Messung per Skript, Änderungs- und Belegtabelle, Zweitprüfung durch einen unabhängigen Subagenten und '
    'Klickfreigabe je Absatz, Einbau nur auf ausdrückliche Anweisung, danach Schritt 4 (Task 12b). Dazu die Taskwechselregel der '
    'Ausgangsübergabe (§ 0 und § 8).',
    '',
    '**Ergebnis:** (1) **Nachtrag Fassung 1** (14:36 im Ordner): Wortlaut nach dem Entwurf, Messung, Belegtabelle mit 22 Fundstellen per '
    '`pdftotext`, Probelauf an einer Kopie des Masters. (2) **Zweitprüfung** durch einen unabhängigen Subagenten: 15 Befunde (1 × A, 5 × B, '
    '9 × C), alle eingearbeitet bis auf einen vorgemerkten C-Befund. A: „(1:3)“ in Tab. 5 von Ramirez-Campillo et al. (2023) zählt Studien '
    'mit Jungen zu Studien mit Mädchen, nicht Reifegruppen. Der Richtungswechsel-Befund stammt überwiegend von Mädchen (Distanz Population 2), '
    'derselbe Lesefehler steht in Textvorschlag 6.1 § 5. B: Lage bei Lloyd et al. (2016) als Modellrechnung aus Tab. 4 prüfbar, „vereinbar“ '
    'nach Codebuch V1, Reifung beim Richtungswechsel nicht ohne Richtung, Liste der Nachführungen vollständig, Vormerkung für die Einleitung. '
    '(3) **Fassung 2:** A4 S4 nennt die Population („überwiegend von Mädchen“), A4 S9 lautet „Den Abstand könnte weniger die Übungsauswahl '
    'als die eigene Umsetzung erklären, auch das Vergleichsprogramm kam ohne Wende aus.“ 6.1 misst 700 gegen 700 (A3 116, A4 142, A5 159), '
    '40 Sätze, längster Satz 31, 0 Semikola, 0 Abschnittsverweise, Quellen 9 auf 8. Probelauf an der Masterkopie: 6.1 700, Absatztext 4.496, '
    'Prognose 27,8 Seiten (Modellrechnung), Kopie MD5 `6c1db455…`. T1 (`RC2023`, Feld `population`) und T4 (+1 Zeile `RC2023`, 171 '
    'Zitierfallen) nachgetragen. (4) **Klick** des Verfassers gegen 15:52, alle Antworten wie empfohlen: A3 „Freigeben“ mit Stufe 3, A4 '
    '„Empfehlung freigeben“ (Grund der Fremdpopulation nur im Begleitteil, nach K2 das zweite Mal so entschieden), A5 „Freigeben“, Einbau '
    '„Per Skript einbauen“ nach der Nachführung des Textvorschlags 6.1. Das ist die ausdrückliche Anweisung zum Einbau. (5) **Fassung 3** '
    'mit dem Klickergebnis, Wortlaut gleich Fassung 2. (6) **Fortsetzungsübergabe 4** mit neuem Startprompt (§ 0), den geänderten Sätzen '
    'und Dateien (§ 1), dem Klick (§ 2), den offenen Klicks (§ 3) und den Arbeitsgängen Nachführung und Einbau (§ 4). Ausgeführt wird der '
    'Einbau nach dem Taskwechsel.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Die Begründung zu A4 S5a verwies auf die alte Satznummer von A3 S6, berichtigt auf „A3 S6 '
    '(neu S5)“. (2) Der Entwurf von `LIESMICH.md` nannte das Protokoll des Laufs bei beiden Läufen bytegleich. Es nennt aber die Größe des '
    'Markdowns, berichtigt. (3) Den Lesefehler „(1:3)“ hatte Fassung 1 aus Textvorschlag 6.1 § 5 übernommen. Die Fundstelle war am PDF '
    'geprüft, die Fußnote ¥ nicht gelesen. Gefunden hat ihn die Zweitprüfung.',
    '',
    '**Stand der Dateien:** Neu: im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` die Dateien '
    '`S3_Nachtrag_Zweitpruefung_Bericht.md` (27.607 Byte, MD5 `db8bdafe…`) und `S3_T1_T4_Nachtrag_2026-10-03.py` mit `.txt` · '
    '`04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung4_2026-10-03.md` (19.915 Byte, MD5 `5f5ed04e…`) mit dem neuen Startprompt (§ 0) '
    'und Projektkopie · `03_Skripte\\Steuerung_Rev162_2026-10-03.py` mit `.txt`. Geändert: '
    '`04_Uebergaben\\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md` Fassung 3 (75.397 Byte, MD5 `4b35973e…`, Projektkopie '
    'ersetzt) · im Arbeitsordner `S3_Nachtrag_6_1_2026-10-03.py` (Fassung 3, 102.016 Byte, MD5 `98d6b93b…`), `S3_Nachtrag.json` (MD5 '
    '`47a682dc…`), `S3_Nachtrag_Saetze.csv`, `S3_Nachtrag.txt`, `S3_Nachtrag_Probelauf_2026-10-03.py` (Fassung 2) mit `.txt` und '
    '`LIESMICH.md` (Abschnitt „Nachtrag 6.1“, 25.513 Byte) · `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (103.653 Byte, MD5 `ae847c32…`) und '
    '`T4_zitierfallen.csv` (86.825 Byte, MD5 `0d44eae0…`) · diese Notizen (Rev. 162 auf Rev. 161), nur im Ordner, die Projektkopie bleibt auf '
    'Rev. 154. Projektspeicher 1.869.747 Byte vor der Ablage, danach rechnerisch 1.891.938 von 2.000.000. Unverändert: Master (40.331 Byte, '
    'MD5 `2fda2144…`), Textvorschlag 6.1 mit JSON (MD5 `627f6b15…`) und Erzeuger, Ergebnisdokument Fassung 7, Kennzahlenblatt, Zahlenliste '
    'des Endabgleichs, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, '
    'Übergabe § 7 Nr. 3). Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen, 14 von 14 gleich.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung4_2026-10-03.md` '
    '§ 0 in einem neuen Task fortsetzen und Word während des Einbaus geschlossen halten · (2) danach in Schritt 4 die Klicks zur Bauform von '
    '6.2 und 6.3, zu den fehlenden Quellen und zum Ort von Hilska et al. (2021) · (3) aus Rev. 152 bis 161 weiter offen: Fortsetzung des '
    'Tasks „Ergebnisse“ (Rev. 161), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 4 ab der Nachführung des Textvorschlags 6.1 nach Nachtrag § 8 (Markdown, JSON und Erzeuger als '
    'Fassung 3, Projektkopie), dann Einbau per Skript wie angewiesen: Master gegen den Referenzstand prüfen, A3 bis A5 von 6.1 ersetzen, '
    'Rückschreibung mit MD5-Prüfung, Abgleich, Messskript Fassung 4, Endabgleich Fassung 3 in eigenem Unterordner, TV 6.1 § 11.4, '
    'Rev.-Block. Danach Schritt 4 (Task 12b).',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 161'
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
    'Steuerung_Rev162_2026-10-03.py — Rev.-Block 162 in Teil 0',
    f'Eingabe: {len(roh)} Byte, MD5 {MD5_VORHER}',
    f'Ausgabe: {len(ausgabe)} Byte, MD5 {MD5_NACHHER}',
    f'Block vor Zeile {pos[0] + 1} (Rev. 161) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

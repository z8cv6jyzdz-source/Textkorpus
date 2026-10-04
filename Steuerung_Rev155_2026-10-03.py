# -*- coding: utf-8 -*-
"""Steuerung_Rev155_2026-10-03.py — Rev. 155 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Taskwechsel nach Teilschritt 2a (Übergabe vom 02.10., § 8).
Setzt den Rev.-Block über den jüngsten Block von Teil 0 und ergänzt die Stand-Zeile. Bricht ab, wenn der jüngste Block nicht
Rev. 154 ist (parallele Sitzung), dann neu stagen und die nächste freie Nummer nehmen.

Aufruf: python3 Steuerung_Rev155_2026-10-03.py <Cowork_Sitzungsnotizen.md> <Ausgabe.md> <Protokoll.txt>
Ohne Semikolon (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import re
import sys

EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
text = roh.decode('utf-8')
L = [f'Eingabe: {EIN}, {len(roh)} Byte, MD5 {hashlib.md5(roh).hexdigest()}']

revs = [int(x) for x in re.findall(r'^### ⭐⭐ NEU \(Rev\. (\d+),', text, flags=re.M)]
assert revs and max(revs) == 154 and 155 not in revs, f'jüngste Rev. {max(revs) if revs else None}, nicht 154'
L.append(f'Jüngste Rev. vor dem Lauf: {max(revs)}')

ANKER = '**Neu geschrieben 09.09.2026 (Rev. 26). Steht ab dieser Fassung ganz oben. Alles darunter ist historisch gewachsen und teilweise auf v2-Kapitelnummern — im Zweifel gilt Teil 0.**\n'
assert text.count(ANKER) == 1
STAND_ALT = '**Stand: (Rev. 154 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 155 — siehe Block oben.) Zuvor: (Rev. 154 — siehe Block oben.) Zuvor: '
assert text.count(STAND_ALT) == 1

BLOCK = """
### ⭐⭐ NEU (Rev. 155, 03.10.2026, 09:05 Sitzungsuhr, Auftrag 03.10., 08:04 mit dem Startprompt aus Übergabe § 0 vom 02.10.): Task „Diskussion: Anwendung der Argumentationsstruktur“ — Schritt 1 und Teilschritt 2a abgeschlossen und gesichert, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Teilschritt 2b, kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` § 0: 6.1 gegen den Befund `02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02` abgleichen und gegenprüfen, die Unterschiede als Potenziale per Klick freigeben lassen und nur Freigegebenes umsetzen, dann Task 12b (6.2 und 6.3 als ein Abschnitt „Methodendiskussion, Stärken und Limitationen“, 900 Wörter), zuletzt die Vormerkungen für Task 13a. Streng schrittweise, jeder Schritt mit gesicherter Datei und Meldung.

**Ergebnis:** (1) **Schritt 1 (Stand):** Master unverändert seit Rev. 152 (40.331 Byte, MD5 `2fda2144…`, 188 Absätze, keine comments.xml), 6.1 zeichengleich mit `03_Skripte\\Textvorschlag_6.1_2026-10-02.json` (Fassung 2), Messskript Fassung 4 reproduziert (6.1 700, Absatztext 4.496, 27,8 Seiten). Volltextstatus der 61 für 12b vorgemerkten Quellen: 34 zitierfähig, 5 im Ordner ohne T1-Steckbrief (Moher 2010, Smart 2015, Khamis & Roche 1994, Malina & Kozieł 2014, Fröhlich 2020), 22 nicht im Ordner (darunter Stuart 2010 und die H8-Verfahrensquellen). Skill-Nachtrag zu Schritt 4a (Rev. 115) gespeichert, Skill auf Stand v5. Register der Übergabe § 4 an den Fundstellen: 15 Zeilen bestätigt, 3 präzisiert (Halbsatz zum Restrisiko ohne Zweiterfassung in G4 oder G5, zwei quellenlose Satzteile in Kapitel 7, Ort von Hilska et al. 2021 in G3 oder G5 offen für Schritt 4). T1 `Liu2024` vor dem ersten Zitat in 12b auf die Distanz 1·1·0 nachführen. (2) **Teilschritt 2a (Codierung und Kennwerte):** 40 Sätze von 6.1 nach dem Codebuch des Befunds codiert, ein blinder Subagent als Zweitcodierer: Primärcode 37 von 40 übereinstimmend (κ 0,92), drei Abweichungen nach K17, K12 und K16 entschieden, Absatzfunktion A6 nach der Korpuskonvention QS:Sicherheit. Kennwerte per Skript gegen Befund § 3 bis § 7, Korpuswerte aus der Anlage nachgezählt (Blockkennwerte 15 von 15 gleich), dazu der Befundteil der Kernstudien als Vergleich auf gleicher Grundlage. Teiltabelle 2a mit 25 Zeilen: 12 entspricht, 5 bewusst abweichend, 3 teilweise, 3 außerhalb, 2 Hinweis. Vorgemerkt für 2b bis Schritt 3: Erklärungsanteil unter der Spanne aller Kernstudien (19,4 % der Wörter gegen 27,3 bis 58,5 % im Befundteil) · „Relevanz zuerst in jedem Block“ nach dem Codebuch nur in A4 umgesetzt (A3 S1 Prämisse der Erklärung, A5 S1 Programmbeschreibung) · Übereinstimmung mit Lloyd et al. (2016) in A5 nicht markiert · A4 S8 und A5 S7 ohne Modalverb · A5 endet mit dem Normwert.

**Eigene Korrekturen in dieser Sitzung:** (1) Skript S1: Die Belegzählung traf zunächst Regex-Artefakte und scheiterte an einem Namenskonflikt, vor der Ablage auf die Zählweise des Messskripts umgestellt (47 Belege wie dort). (2) Skript S2a: Kapitel 5 hat im Master keine Unterabschnitte, die Reihenfolge der Zielgrößen wird am Absatz der Gruppenvergleiche gelesen. Das Muster für den eigenen Befund in Vergleichssätzen traf die Kontrollgruppe einer Vorstudie (A4 S7) und ist berichtigt.

**Stand der Dateien:** Neu: `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` (24 Dateien, Schritt 1 und Teilschritt 2a, mit `LIESMICH.md`) · `02_Befunde\\Abgleich_Diskussion_6.1_Argumentationsstruktur_2026-10-03.md` (57.677 Byte, MD5 `1bf07061…`, § 1 bis § 3.1) · `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung1_2026-10-03.md` mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev155_2026-10-03.py` mit `.txt` · Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung1_2026-10-03.md`. Das Ergebnisdokument hat keine Projektkopie: Der Projektspeicher stand vor dieser Ablage bei 1,96 von 2,00 MB, es gilt die Ordnerfassung. Geändert: diese Notizen (Rev. 155 auf Rev. 154), nur im Ordner: Die Projektkopie `claude/Cowork_Sitzungsnotizen.md` ließ sich nicht aktualisieren, der Schreibversuch lag über der Speichergrenze des Projekts. Sie bleibt auf Rev. 154, es gilt die Ordnerfassung. Unverändert: Master, Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung1_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 154 weiter offen: Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 1 ab Teilschritt 2b: die neun Bauregeln aus Befund § 12.2 und die Projektregeln aus § 12.3 einzeln an 6.1 prüfen (Teiltabelle 2b, Ergebnisdokument § 3.2), dann 2c (Prüfliste § 12.5 Nr. 1 bis 6, 11 und 12) und 2d (Nachzählung der Korpusaussagen, auf die sich Potenziale stützen sollen), danach Schritt 3 mit der Klickfrage zu den Potenzialen.
"""

neu = text.replace(ANKER, ANKER + BLOCK, 1).replace(STAND_ALT, STAND_NEU, 1)
assert neu.count('### ⭐⭐ NEU (Rev. 155,') == 1
assert neu.index('### ⭐⭐ NEU (Rev. 155,') < neu.index('### ⭐⭐ NEU (Rev. 154,')
assert chr(59) not in BLOCK
aus = neu.encode('utf-8')
open(AUS, 'wb').write(aus)
L.append(f'Ausgabe: {AUS}, {len(aus)} Byte, MD5 {hashlib.md5(aus).hexdigest()}')
L.append(f'Block Rev. 155: {len(BLOCK.encode("utf-8"))} Byte, eingefügt über Rev. 154, Stand-Zeile ergänzt')
L.append('Unverändert außer Block und Stand-Zeile: ' + str(neu.replace(BLOCK, '', 1).replace(STAND_NEU, STAND_ALT, 1) == text))
open(PROT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))

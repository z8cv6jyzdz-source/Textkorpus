# -*- coding: utf-8 -*-
"""Steuerung_Rev164_2026-10-03.py — Rev.-Block 164 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Fortsetzung 5: Schritt 4 (a) des Tasks 12b (Zuordnung der Rasterzeilen
6.2 und 6.3, Bauform per Klick), Taskwechsel nach automatischer Zusammenfassung des Verlaufs (Fortsetzungsübergabe 6).
Setzt den Block vor den jüngsten Block (Rev. 163) und ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev164_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == '9cc5ef30e7b7bf39cda3fc884e48133b', MD5_VORHER  # gestagt 03.10. gegen 18:08 Sitzungsuhr, Stand Rev. 163
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 163 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 164 — siehe Block oben.) Zuvor: (Rev. 163 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 164' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 164, 03.10.2026, 18:10 Sitzungsuhr, Auftrag 03.10., 16:51 mit dem Startprompt aus Fortsetzungsübergabe 5 § 0): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Schritt 4 (a) des Tasks 12b: Master ohne Befund, Rasterzeilen 6.2 und 6.3 '
    'per Skript zugeordnet und geprüft, Bauform per Klick (Option A, Dreischritt im Stärkenzug), Taskwechsel nach automatischer '
    'Zusammenfassung des Verlaufs, Fortsetzungsübergabe 6, Fortsetzung ab Schritt 4 (b)',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung5_2026-10-03.md` § 0: Schritt 4 (a) des '
    'Tasks 12b, also den Master gegen den Stand nach dem Einbau prüfen, jede Rasterzeile 6.2.1 bis 6.2.12 und 6.3.1 bis 6.3.5 den '
    'Methodenbegründungen, den Stärken oder G1 bis G8 zuordnen (G37 a) und die Bauform als Klickfrage mit Empfehlung vorlegen. Dazu Schritte, '
    'Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.',
    '',
    '**Ergebnis:** (1) **Master** gegen 17:13 neu gestagt: 40.337 Byte, MD5 `6c1db455…` wie nach dem Einbau (Rev. 163), 188 Absätze, keine '
    'comments.xml, 6.1 zeichengleich mit der JSON der Fassung 3 (700 Wörter), 6.2 und 6.3 nur mit Überschriften, '
    '`Abgleich_Kapitel6_1_Master_2026-10-02.py` ohne Befund. (2) **Zuordnung** per '
    '`03_Skripte\\Diskussion_Anwendung_2026-10-03\\S4a_Rasterzuordnung_2026-10-03.py`, Ergebnis `S4a_Rasterzuordnung_12b.md`: 101 Teilzeilen '
    '(66 Kern, 26 Reserve, 6 Verzicht, 3 Vormerkungen für Kapitel 7) mit Ort, Grundlage, Kennungen und Quellenstatus nach S1, T1 und T4. '
    '6.2.1 und 6.2.2 vollständig in G1, Freigabe ohne unabhängige Methodenprüfung genau einmal in G3, Restrisiko ohne Zweiterfassung in G5, '
    'Bootstrap als streichbarer Halbsatz in G1, Aufsicht als Korpuseigenschaft einmal in G8, kein Erratum. 88 Vormerkungen der Eingänge mit '
    'Ziel oder Grund, Befunde B1 bis B17, acht Klicks K-b1 bis K-b8 für 4 (b). Zwölf Prüfungen per Skript ohne Befund (erwartet und vorgemerkt: '
    'Satzkern Nr. 4 des Nachtrags K2 teilt sechs Wörter mit 6.1 A2 S3, der eigene Anschluss in 4 (c) behebt das), zwei Läufe unter '
    'verschiedenem `PYTHONHASHSEED` bytegleich. Richtwerte 880 gegen 900, verbindlich ist nur die Summe. (3) **Klick Bauform** um 18:02: '
    'Option A, 6.2.11 (Reifestatus) und 6.2.8 (Messgüte) als Stärken im Dreischritt Problem → Vorgehen → Folge nach Sammoud et al. (2024) am '
    'Anfang des Stärkenzugs, danach übrige Stärken, Scharnier, G1 bis G8, Ausblick mit G8 verschmolzen, 6.2.9 nur bei freiem Budget. '
    '(4) **Taskwechsel** nach automatischer Zusammenfassung des Verlaufs am Checkpoint nach Schritt 4 (a): Fortsetzungsübergabe 6 mit neuem '
    'Startprompt (§ 0), Ergebnis und Dateien (§ 1), Klickergebnis (§ 2), offenen Klicks (§ 3), Schritt 4 (b) als erstem Arbeitsgang (§ 4) und '
    'den Besonderheiten (§ 5).',
    '',
    '**Befunde, die das Gerüst bestimmen (S4a § 5):** B13 die Stärke „Rechenkette vor Kenntnis der KG-Werte“ aus Raster 6.3.1 trägt nicht, '
    'die Spezifikation der berichteten Rechnung entstand nach der ersten Rechnung vom 15.09. (F17 § 1.5), tragfähig sind nur die Schwellen '
    'vor der Abschlusstestung der Kontrollgruppe · B5 die Ausfälle zur Abschlusstestung sind nicht leistungsneutral, aber ohne einheitliche '
    'Richtung · B9 die Power-Eingaben 0,37 (Countermovement Jump, Moran et al.) und 0,93 (10-m-Sprint bei mehr als 14 Einheiten, '
    'Ramirez-Campillo et al., 2020) sind keine Erwartungen für die eigenen Zielgrößen bei eigener Dosis · B1 die Steuerdokumente tragen für '
    'den 30-m-Sprint von Verein A Werte der ersten Rechnung, maßgeblich ist K-05.8 · B2, B11, B12 und B14 (Korpusbasis, Fallzahlempfehlung, '
    'Form der Korpuszahlen, Spielklasse) sind in 4 (b) zu entscheiden.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Die erste Fassung der Zuordnung prüfte ausgeschlossene Wendungen ohne Verneinung und '
    'meldete „keine Responder- und Einzelwertdarstellungen“ als Verstoß. Die Prüfung erkennt jetzt Verneinungen und nimmt die Beschreibung '
    'fremder Lesarten (6.2.1 e) ausdrücklich aus. (2) Zitate aus dem Berichtsraster brachten fünf Semikola ins Markdown, sie stehen jetzt als '
    '„·“ mit Vermerk. (3) Die Zahl der Zeilen 6.2.x, die in G1 bis G8 aufgehen, stand im Entwurf als „neun“, das Skript rechnet sie jetzt '
    '(elf). (4) Der Entwurf des LIESMICH-Abschnitts nannte für die erste Rückschreibung 17:57, berichtigt nach der mtime auf 17:35.',
    '',
    '**Stand der Dateien:** Neu: im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` die Dateien '
    '`S4a_Rasterzuordnung_2026-10-03.py` (91.167 Byte, MD5 `01d92ca5…`), `S4a_Rasterzuordnung_12b.md` (76.934 Byte, `2c13ac3a…`), '
    '`S4a_Rasterzuordnung.csv` (33.390 Byte, `fc1471f3…`), `S4a_Vormerkungen.csv` (9.158 Byte, `cf901a36…`), `S4a_Rasterzuordnung.txt` '
    '(5.909 Byte, `24badda7…`) und `S4a_Abgleich_Kapitel6_1_Master.txt` (1.889 Byte, `c695bdd3…`) · '
    '`04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung6_2026-10-03.md` (19.175 Byte, MD5 `494faa8e…`) mit dem neuen Startprompt '
    '(§ 0) und Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung6_2026-10-03.md` · `03_Skripte\\Steuerung_Rev164_2026-10-03.py` '
    'mit `.txt`. Geändert: `03_Skripte\\Diskussion_Anwendung_2026-10-03\\LIESMICH.md` (Abschnitt „Schritt 4 (a)“, 37.037 Byte, `446e22d3…`) · '
    'diese Notizen (Rev. 164 auf Rev. 163), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Projektspeicher nach der Projektkopie '
    'rechnerisch 1.930.350 von 2.000.000 Byte, die S4a-Dateien liegen nur im Ordner. Unverändert: Master (`6c1db455…`), Textvorschlag 6.1 '
    'Fassung 3, T1 (76 Steckbriefe) und T4 (171 Zitierfallen), Kennzahlenblatt, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, '
    'Maßnahmenliste (Nachführung am Ende des Tasks, Fortsetzungsübergabe 6 § 5 Nr. 7). Rückschreibung aus eigenen Ausgabepfaden '
    '(`s4a_2026-10-03_a` sechs Dateien um 17:35, `s4a_2026-10-03_b` vier Dateien um 18:05, `ue6_2026-10-03_a` Übergabe, '
    '`rev164_2026-10-03_a` diese Notizen mit Skript und Protokoll), danach neu gestagt und per MD5 verglichen.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung6_2026-10-03.md` '
    '§ 0 in einem neuen Task fortsetzen · (2) dort in Schritt 4 (b) die Klicks K-b1 bis K-b8 (fehlende Quellen, Ort von Hilska et al., 2021, '
    'TESTEX 7, Korpusbasis und Form der Korpuszahlen, Fallzahlempfehlung, Spielklasse der drei Mannschaften, Stärken ohne „Rechenkette“ und '
    'Ethikvotum, 30-m-Sprint je Verein), danach Freigabe des Gerüsts, Textvorschlag, Freigabe und Einbau von 6.2 und 6.3 · (3) aus Rev. 152 '
    'bis 163 weiter offen: Fortsetzung des Tasks „Ergebnisse“ (Rev. 161), F9 im Master, Vormerkungen G37 (o) und (p) für den '
    'Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 6 ab Schritt 4 (b) (Task 12b): Master und Teil 0 frisch stagen, die Klicks K-b1 bis K-b8 aus '
    '`S4a_Rasterzuordnung_12b.md` § 6 mit Empfehlung, T1 `Liu2024` angleichen und die fehlenden T1-Steckbriefe der Kern-Quellen anlegen, '
    'dann Zug-Tabelle, Verzichtstabelle und Stichpunktgerüst nach Bauform A mit Zielwörtern je Punkt und Kürzungsleiter bis 900, Freigabe '
    'abwarten. Danach Schritt 4 (c) bis (e), Schritt 5, am Ende des Tasks Maßnahmenliste und Rev.-Block.',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 163'
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
    f'Block vor Zeile {pos[0] + 1} (Rev. 163) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

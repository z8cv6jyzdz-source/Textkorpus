# -*- coding: utf-8 -*-
"""
Steuerung_Rev116_2026-09-28.py — Teil 0 Rev. 116, Maßnahmenliste und README nach dem Task Kapitelstruktur 28.09.
Bachelorarbeit U15-Plyometrie · DSHS Köln · Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`, Gliederung v6

Schreibt den Block Rev. 116 in Teil 0 der Sitzungsnotizen (vor Rev. 115) und die Stand-Zeile, schreibt die Maßnahmenliste fort
(Stand, A8 erledigt, G31 (a), G35 (d), G37 neu, Zusammenfassung Zeilen 11, 12, 18 und neue Zeile, Summe mit gemessener
Kästchenzählung) und den README (Gliederung v6, Befund). Zahlen aus der Zählung `Kapitelstruktur_Zaehlung_2026-09-28.txt`
(Überschriften v5 und v6). Jede Ersetzung genau einmal, sonst Abbruch. Ohne Semikolon im Skript (chr(59)).
Aufruf: python Steuerung_Rev116_2026-09-28.py <Quelle Claude-Ordner (gestagte Originale)> <Ausgabeordner> <Zaehlung.txt> <Uhrzeit Sitzungsuhr HH:MM>
"""
import os
import re
import sys

QUELLE, AUS, ZAEHL, UHR = sys.argv[1:5]
SEMI = chr(59)
PROT = []
h, mi = UHR.split(':')
UHR_MESZ = '%02d:%s' % ((int(h) + 1) % 24, mi)


def ersetze(text, alt, neu, was):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('ABBRUCH %s: Suchtext %d-mal gefunden: %s' % (was, n, alt[:90]))
    PROT.append('ersetzt: ' + was)
    return text.replace(alt, neu, 1)


def zeile(text, praefix, neu, was):
    zl = text.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('ABBRUCH %s: %d Zeilen beginnen mit %s' % (was, len(idx), praefix[:60]))
    zl[idx[0]] = neu
    PROT.append('Zeile ersetzt: ' + was)
    return '\n'.join(zl)


# Zahlen aus der Zählung
z = open(ZAEHL, encoding='utf-8').read()
m5 = re.search(r'Überschriften gesamt \(v5, Kapitel 1 bis 7 in Arbeitsnummern\): (\d+)', z)
m6 = re.search(r'Überschriften v6: Ebene 1 (\d+) · Ebene 2 (\d+) · Ebene 3 0 · gesamt (\d+) \(v5: (\d+)\) · Wörter je Überschrift (\d+)', z)
mk = re.search(r'Wörter je Überschrift \(ohne Absatztitel\): Median (\d+), Spanne (\d+) bis (\d+)', z)
mm = re.search(r'Unterabschnitte 2\. Ebene in der Methodik: Median (\d+), Spanne (\d+) bis (\d+)', z)
if not (m5 and m6 and mk and mm) or m5.group(1) != m6.group(4):
    raise SystemExit('ABBRUCH: Zählung nicht lesbar')
U5, E1, E2, U6, WJU = int(m5.group(1)), int(m6.group(1)), int(m6.group(2)), int(m6.group(3)), int(m6.group(5))
KMED, KMIN, KMAX = mk.group(1), mk.group(2), mk.group(3)
MMED, MMIN, MMAX = mm.group(1), mm.group(2), mm.group(3)

t = open(os.path.join(QUELLE, '00_Steuerung', 'Cowork_Sitzungsnotizen.md'), encoding='utf-8').read()
m = open(os.path.join(QUELLE, '00_Steuerung', 'Massnahmenliste_Datenverarbeitung.md'), encoding='utf-8').read()
r = open(os.path.join(QUELLE, 'README_Ordnerstruktur.md'), encoding='utf-8').read()

# ---------------------------------------------------------------------------------------------------------------- Teil 0
block = '''### ⭐⭐ NEU (Rev. 116, 28.09.2026, %s Sitzungsuhr, entspricht %s MESZ): Task Kapitelstruktur — Abgleich der Gliederung v5 mit Korpus und Leitfäden, Gliederung v6 mit %d statt %d Überschriften, Entscheidungen ohne Nachfrage

**Auftrag (Verfasser, 28.09., 21:00):** Die Gliederung v5 hat gegenüber RCTs eine „Übermenge von Unterkapiteln“. Die übliche Struktur von RCTs mit der Struktur der Leitfäden zum wissenschaftlichen Schreiben abgleichen, ausdrücklich ohne den SMK-Leitfaden, die medizinischen und naturwissenschaftlichen Leitfäden aus den Projektdateien nutzen, besonders die Kapitelstruktur prüfen, eine deutliche Verschlankung realisieren. **21:43: „aufgaben abschließen ohne nachfrage“**, die fünf Klickfragen der ersten Fassung des Befunds sind deshalb nach der jeweiligen Empfehlung als Entscheidungen E1 bis E5 ausgeführt (Befund § 8), jede mit einem Satz revidierbar. Master unverändert (48.791 Byte, MD5 e35315d6…), Fassung 17 ist in den Projekteinstellungen sichtbar (A8 erledigt).

**Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28` (.md, .docx, .pdf):** Maßstäbe waren der Vergleichskorpus (elf Studien, Überschriften am extrahierten Volltext neu gezählt, `03_Skripte\\Kapitelstruktur_Zaehlung_2026-09-28`, Fassung 2), CONSORT 2010 (Schulz et al., 2010, Checkliste S. 699 und Struktur S. 700), der Leitfaden Sportmedizin (Universitätsklinikum Münster, Kap. 2), der TUM-Leitfaden (02/2024, Kap. 3), dvs 2020 (S. 2) und Fröhlich et al. (2020, S. 101). Ergebnis: v5 trug %d Überschriften (5 Kapitel, 12 Unterabschnitte, 5 Unterunterabschnitte, 289 Wörter je Überschrift). Korpus: Methodik im Median %s Unterabschnitte (%s bis %s), Ergebnisse und Diskussion in 8 von 11 ohne Unterabschnitte, dritte Ebene in 3 von 11, Limitationen mit Überschrift 1 von 11, Wörter je Überschrift Median %s (%s bis %s). Die Abweichung der v5 lag in der Tiefe (4.4.1 bis 4.4.3 mit 62 bis 103 Wörtern, Elternüberschrift 4.5 ohne Text), im Monitoring-Abschnitt ohne Vorbild und in der Unterteilung von Ergebnissen und Diskussion, nicht in der Dichte. Gegenstimmen benannt: CONSORT S. 700 („frequent subheadings … especially the methods and results sections“, zugleich Verweis auf „the traditions of the research field“) und Sportmedizin S. 10 („streng hierarchisch“, „Fließtext … vermeiden“). Zweitprüfung durch einen unabhängigen Subagenten, 17 Befunde, alle eingearbeitet (Befund § 9), darunter: Ablauf und Tests im Korpus 4 zu 4 geteilt, Hammami ohne Limitationsblock (Bauplan § 1 nennt zwei Studien ohne Block, es sind drei, Nachtragsvermerk), Zählung um sechs Überschriften korrigiert.

**Gliederung v6 `01_Verfahren\\Gliederung_2026-09-28` (.md, .docx, .pdf, Erzeuger `03_Skripte\\Gliederung_v6_2026-09-28.py` aus der v5, Kopie der v5 in `_Archiv\\_ersetzt_2026-09-28_Gliederung_v5`):** %d Überschriften (%d + %d), keine dritte Ebene, %d Wörter je Überschrift. 1 Einleitung · 2 Methodik mit 2.1 Studiendesign, 2.2 Stichprobe, 2.3 Untersuchungsablauf, 2.4 Leistungsdiagnostik (Tests als Absätze), 2.5 Trainingsintervention und Begleitbedingungen (4.5.1, 4.5.2, 4.6), 2.6 Statistische Auswertung · 3 Ergebnisse ohne Unterabschnitte · 4 Diskussion mit 4.1 Einordnung der Ergebnisse und 4.2 Methodendiskussion, Stärken und Limitationen (6.2 und 6.3) · 5 Fazit und Ausblick. Änderungen Ä14 bis Ä19, Master-Punkte M27 (Task 18) und M28 (Tasks 11 und 12). Budgets je Abschnitt der v6 verbindlich (2.5 725, 3 450, 4.2 900), die Blockwerte bleiben Richtwerte, Summe 6.350.

**Entscheidungen (E1 bis E5, Befund § 8):** E1 Methodik mit sechs Unterabschnitten, 4.3 und 4.4 bleiben getrennt (die erste Fassung empfahl fünf, die Zweitprüfung zeigte den Korpus 4 zu 4 geteilt) · E2 Diskussion mit zwei Unterabschnitten · E3 Ergebnisse ohne Unterabschnitte, in Task 11 am Textvorschlag geprüft, 3.1 und 3.2 kommen zurück, wenn der Orientierungszug ohne Überschrift nicht trägt · E4 Budgets je Abschnitt verbindlich, Blockwerte als Richtwerte · E5 Kapitel 4 in Task 18 (M25 mit M27), Kapitel 5 und 6 mit den Tasks 11 und 12 (M28), Messskript Fassung 4 mit Task 11, Berichtsraster Rev. 4, Plan Rev. 6 und Fassung 18 im Steuerdokumente-Task nach dem Abgleich der Einleitung (G37).

**Nicht geändert:** Master, Berichtsraster (Rev. 3), Plan (Rev. 5), Messskript (Fassung 3), Fassung 17, Textvorschläge. Bis zum Steuerdokumente-Task gilt: Gliederung v6 und der Befund gehen den Angaben zur Kapitelstruktur in Fassung 17 § 5.1 bis § 5.3 und § 5a vor, die Arbeitsnummern und Zeilenkennungen bleiben.

**Stand der Dateien:** Neu: Befund (.md, .docx, .pdf), `03_Skripte\\Kapitelstruktur_Zaehlung_2026-09-28` (.py, .txt), `03_Skripte\\Gliederung_v6_2026-09-28.py`, `03_Skripte\\Steuerung_Rev116_2026-09-28` (.py, .txt), Archivordner `_ersetzt_2026-09-28_Gliederung_v5`. Ersetzt: Gliederung (.md, .docx, .pdf, jetzt v6), README, Maßnahmenliste, diese Notizen. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen. Projektkopien: Befund, Gliederung v6, Maßnahmenliste, Sitzungsnotizen.

**Offen beim Verfasser:** (1) `Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt (unverändert aus Rev. 115) · (2) Skill-Vorschlag speichern (G26g) · (3) die Einleitung in den Master übertragen (Task 7 neu, Rev. 114) · (4) die Gliederung v5 ist in Word geöffnet, die neue `.docx` konnte nur geschrieben werden, wenn Word sie freigegeben hat (siehe Protokoll `Steuerung_Rev116_2026-09-28.txt`).

**Nächster Schritt:** Nach der Übertragung der Einleitung die Übergabe Einleitung § 8 Nr. 6 (Abgleich Satz für Satz, Messskript, Endabgleich, Rev. 117, Maßnahmenliste mit G35 i, T1, T4, Plan, Projektkopien). Danach der Steuerdokumente-Task zur Kapitelstruktur (G37: Berichtsraster Rev. 4, Plan Rev. 6, Fassung 18, Messskript Fassung 4, Nachtragsvermerk Bauplan § 1), danach Task 11 (Kapitel 5 als ein Kapitel ohne Unterabschnitte) mit dem Startsatz aus Plan § 8, Nr. 23 per Klick zu Beginn.

''' % (UHR, UHR_MESZ, U6, U5, U5, MMED, MMIN, MMAX, KMED, KMIN, KMAX, U6, E1, E2, WJU)
t = ersetze(t, '### ⭐⭐ NEU (Rev. 115, 28.09.2026, 20:04 Sitzungsuhr', block + '### ⭐⭐ NEU (Rev. 115, 28.09.2026, 20:04 Sitzungsuhr', 'Teil 0 Block Rev. 116')
t = ersetze(t, '**Stand: (Rev. 115 — siehe Block oben.) Zuvor: (Rev. 114 — siehe Block oben.)',
            '**Stand: (Rev. 116 — siehe Block oben.) Zuvor: (Rev. 115 — siehe Block oben.) Zuvor: (Rev. 114 — siehe Block oben.)', 'Teil 0 Stand')

# ---------------------------------------------------------------------------------------------------------------- Maßnahmenliste
m = ersetze(m, '**Stand 28.09.2026, 20:04 Sitzungsuhr, entspricht 21:04 MESZ (Rev. 115 — Task Steuerdokumente 28.09.:',
            '**Stand 28.09.2026, %s Sitzungsuhr, entspricht %s MESZ (Rev. 116 — Task Kapitelstruktur: Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`, '
            'Gliederung v6 mit %d statt %d Überschriften, Entscheidungen E1 bis E5 ohne Nachfrage (Verfasser 21:43). A8 erledigt, G31 (a) und G35 (d) fortgeschrieben, '
            'G37 neu, Zusammenfassung um die Zeile Kapitelstruktur ergänzt). Zuvor 28.09.2026, 20:04 Sitzungsuhr, entspricht 21:04 MESZ (Rev. 115 — Task Steuerdokumente 28.09.:'
            % (UHR, UHR_MESZ, U6, U5), 'ML Stand')
m = ersetze(m, '- [ ] **A8 · ⭐ Projektanweisungen Fassung 17 in die claude.ai-Projekteinstellungen einsetzen** — ',
            '- [x] **A8 · ⭐ Projektanweisungen Fassung 17 in die claude.ai-Projekteinstellungen einsetzen** — **erledigt (Rev. 116, 28.09.: Fassung 17 ist in der Sitzung von 21:00 als Projektanweisung sichtbar).** ',
            'ML A8')
m = ersetze(m, '(a) Verfasser: Punkt nach „berechnet“ in 4.4.2, Überschrift 4.4.2 ohne „(bilateral)“, Platzhalter',
            '(a) Verfasser: Punkt nach „berechnet“ in 4.4.2, Überschrift 4.4.2 ohne „(bilateral)“ *(Rev. 116: die Überschrift entfällt mit Gliederung v6 in Task 18, M27)*, Platzhalter',
            'ML G31 a')
m = ersetze(m, '(d) Gliederung 1 Einleitung · 2 Methodik · 3 Ergebnisse · 4 Diskussion · 5 Fazit und Ausblick, Arbeitsnummern 4 bis 7 bis Task 18, Umnummerierung dort per Skript (Master, Steuerdokumente, Skripte, Textvorschläge)',
            '(d) Gliederung 1 Einleitung · 2 Methodik · 3 Ergebnisse · 4 Diskussion · 5 Fazit und Ausblick, Arbeitsnummern 4 bis 7 bis Task 18, Umnummerierung dort per Skript (Master, Steuerdokumente, Skripte, Textvorschläge) '
            '*(Rev. 116: nach Gliederung v6 mit der Zusammenlegung M27 und M28, Zuordnung 4.1 → 2.1 · 4.2 → 2.2 · 4.3 → 2.3 · 4.4 → 2.4 · 4.5.1, 4.5.2, 4.6 → 2.5 · 4.7 → 2.6 · 5 → 3 · 6.1 → 4.1 · 6.2, 6.3 → 4.2 · 7 → 5, G37)*',
            'ML G35 d')
g37 = ('- [ ] **G37 · Kapitelstruktur: Gliederung v6 (28.09., Rev. 116, Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`, Entscheidungen E1 bis E5 ohne Nachfrage):** '
       '%d statt %d Überschriften, keine dritte Ebene: 2.1 Studiendesign · 2.2 Stichprobe · 2.3 Untersuchungsablauf · 2.4 Leistungsdiagnostik (Tests als Absätze) · 2.5 Trainingsintervention und Begleitbedingungen (4.5.1, 4.5.2, 4.6) · 2.6 Statistische Auswertung · 3 Ergebnisse ohne Unterabschnitte · 4.1 Einordnung der Ergebnisse · 4.2 Methodendiskussion, Stärken und Limitationen (6.2, 6.3) · 5 Fazit und Ausblick. '
       'Folgeänderungen (Befund § 7), in einem Steuerdokumente-Task nach dem Abgleich der Einleitung: (a) Berichtsraster Rev. 4: Kopfblöcke mit Endnummer und Zusammenlegung, § 3.14 mit Kopfblock 4.2 und Zuordnung der Zeilen 6.2.x zu G1 bis G8 oder zum Eröffnungsabsatz (6.2.8, 6.2.9, 6.2.11 als Methodenbegründungen), Zeilenkennungen bleiben Arbeitsnummern, Präfix E und R in Task 18 · '
       '(b) Plan Rev. 6: Task 11 ein Kapitel ohne Unterabschnitte, Task 12 mit 6.1 und dem Abschnitt 6.2 + 6.3 nach Bauform Sammoud, Task 18 mit M27 · (c) Fassung 18: § 5.1 Gliederung und Zuordnungstabelle, § 5.2 Budgets je Abschnitt (2.5 725, 3 450, 4.2 900), § 5.3 Objektzuordnung in Endnummern, § 5a, § 12 („in 6.2“ → „in 4.2“), § 13 (E1 bis E5), § 15 (Sportmedizin als Maßstab der Kapitelstruktur), § 1.3 Nachtragsvermerk Bauplan § 1 (drei Studien ohne Limitationsblock: Lloyd, Hammami, Negra 2020) · '
       '(d) Messskript Fassung 4 mit Task 11 (Budget je Abschnitt der v6 neben den Blockrichtwerten, ELTERN der zusammengelegten Blöcke) · (e) Master: Kapitel 4 in Task 18 (M27 mit M25, Nahtstellen 4.4 Vorspann und Testabsätze, 4.5.1 mit 4.5.2 und 4.6, kein Wort hinzufügen), Kapitel 5 und 6 mit den Tasks 11 und 12 (M28) · '
       '(f) E3 in Task 11 am Textvorschlag prüfen (3.1 und 3.2 zurück, wenn der Orientierungszug ohne Überschrift nicht trägt) · (g) T4-Nachtrag: Bouafif et al. (2026) nennen in den Limitationen keine Belastungserfassung, beschreiben im Methodenteil aber sRPE (Zweitprüfung des Befunds) · (h) Skill-Vorschlag beim nächsten Stand auf Gliederung v6 (G26g). *(28.09., Rev. 116)*'
       % (U6, U5))
m = ersetze(m, '(c) erledigt · (d) bleibt.)*\n', '(c) erledigt · (d) bleibt.)*\n' + g37 + '\n', 'ML G37')
m = ersetze(m, '| 11 Kapitel 5 | B5 (Rest) · G28g · G29 (d), (e) · G32 (b) mit Nr. 23 per Klick zu Beginn · G32 (j) Rest (Umfangsdokument R5, F17 § 11.9) · G26g (Skill-Stand prüfen) |',
            '| 11 Kapitel 5 (nach Gliederung v6 ein Kapitel ohne Unterabschnitte, Blöcke 5.1 und 5.2 als Absatzgruppen) | B5 (Rest) · G28g · G29 (d), (e) · G32 (b) mit Nr. 23 per Klick zu Beginn · G32 (j) Rest (Umfangsdokument R5, F17 § 11.9) · G26g (Skill-Stand prüfen) · G37 (d), (e) Kapitel 5, (f) |',
            'ML Zeile 11')
m = ersetze(m, '| 12 Kapitel 6 | G17d · G17f · G26l · J6 · K23 · L14 (a), (b) · L16 · G29 (f) · G32 (c) · G34 (c) (Hilska 2021 in 6.3) · G33 (d), (f) · G35 (j) (Textvorschlag Einleitung § 6 Nr. 7) · H10 (optional) |',
            '| 12 Kapitel 6 (nach Gliederung v6: 6.1 und der Abschnitt 6.2 + 6.3 „Methodendiskussion, Stärken und Limitationen“) | G17d · G17f · G26l · J6 · K23 · L14 (a), (b) · L16 · G29 (f) · G32 (c) · G34 (c) (Hilska 2021 in 6.3) · G33 (d), (f) · G35 (j) (Textvorschlag Einleitung § 6 Nr. 7) · H10 (optional) · G37 (e) Kapitel 6 |',
            'ML Zeile 12')
m = ersetze(m, '· G35 (d) (Umnummerierung, vorher Präfix E im Berichtsraster) |',
            '· G35 (d) (Umnummerierung nach Gliederung v6 mit M27, vorher Präfix E und R im Berichtsraster) · G37 (e) Kapitel 4 · G31 (a) Überschrift 4.4.2 entfällt mit M27 |',
            'ML Zeile 18')
m = ersetze(m, '| 7 neu: Einleitung (Kapitel 1 bis 3 zusammengelegt, höchstens 1.500 Wörter, ersetzt 7 bis 10 und den Einleitungsteil von 14) |',
            '| Kapitelstruktur 28.09. (erledigt 28.09., Rev. 116: Befund und Gliederung v6) | G37 angelegt · offen: G37 (a) bis (d) im Steuerdokumente-Task nach dem Abgleich der Einleitung, (g), (h) |\n'
            '| 7 neu: Einleitung (Kapitel 1 bis 3 zusammengelegt, höchstens 1.500 Wörter, ersetzt 7 bis 10 und den Einleitungsteil von 14) |', 'ML Zeile Kapitelstruktur')
HO = len(re.findall(r'^- \[ \] \*\*', m, re.M))
TO = len(re.findall(r'^    - \[ \] \*\*', m, re.M))
m = ersetze(m, '| **Summe** | **Rev. 115 (28.09.), per Skript an den Kästchen gezählt: 38 Hauptpunkte und 9 Unterpunkte mit offenem Kästchen** (die Buchstabenpunkte innerhalb eines Eintrags nicht gezählt, darum nicht vergleichbar mit der Zählung darunter). A8 wieder offen, G35 (i) und (j) neu. Zuvor:',
            '| **Summe** | **Rev. 116 (28.09.), per Skript an den Kästchen gezählt: %d Hauptpunkte und %d Unterpunkte mit offenem Kästchen** (die Buchstabenpunkte innerhalb eines Eintrags nicht gezählt). A8 erledigt, G37 neu. Zuvor: **Rev. 115 (28.09.): 38 Hauptpunkte und 9 Unterpunkte mit offenem Kästchen** (A8 wieder offen, G35 (i) und (j) neu). Zuvor:' % (HO, TO),
            'ML Summe')

# ---------------------------------------------------------------------------------------------------------------- README
r = ersetze(r, '`Gliederung_2026-09-28` (v5: fünf Kapitel, Einleitung ohne Unterabschnitte, Budget und Seitenmodell)',
            '`Gliederung_2026-09-28` (v6 vom 28.09. abends: fünf Kapitel, zwei Ebenen, %d Überschriften, Einleitung ohne Unterabschnitte, Budget und Seitenmodell, v5 in `_Archiv\\_ersetzt_2026-09-28_Gliederung_v5`)' % U6,
            'README Zeile 01_Verfahren')
r = ersetze(r, 'Gliederung, Wortbudget und Seitenmodell stehen in `01_Verfahren\\Gliederung_2026-09-28` (v5).',
            'Gliederung, Wortbudget und Seitenmodell stehen in `01_Verfahren\\Gliederung_2026-09-28` (v6, Kapitelstruktur mit %d Überschriften, Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`).' % U6,
            'README Was wo gilt')
r = ersetze(r, '· `Argumentation_Relevanz_Breitensport_2026-09-28` (Rev. 2, Relevanz und Prävention) ·',
            '· `Kapitelstruktur_Abgleich_2026-09-28` (Korpus und Leitfäden zur Kapitelstruktur, Grundlage der Gliederung v6) · `Argumentation_Relevanz_Breitensport_2026-09-28` (Rev. 2, Relevanz und Prävention) ·',
            'README Zeile 02_Befunde')

os.makedirs(os.path.join(AUS, '00_Steuerung'), exist_ok=True)
for pfad, text in [(os.path.join('00_Steuerung', 'Cowork_Sitzungsnotizen.md'), t),
                   (os.path.join('00_Steuerung', 'Massnahmenliste_Datenverarbeitung.md'), m),
                   ('README_Ordnerstruktur.md', r)]:
    with open(os.path.join(AUS, pfad), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    PROT.append('geschrieben %s: %d Byte' % (pfad, len(text.encode('utf-8'))))
aus = ['Steuerung_Rev116_2026-09-28.py — Teil 0 Rev. 116, Maßnahmenliste und README (Task Kapitelstruktur 28.09.)',
       'Uhrzeit Sitzungsuhr %s (MESZ %s) · Überschriften v5 %d, v6 %d (%d + %d), Wörter je Überschrift v6 %d · Korpus Methodik Median %s (%s bis %s), Wörter je Überschrift Median %s (%s bis %s)'
       % (UHR, UHR_MESZ, U5, U6, E1, E2, WJU, MMED, MMIN, MMAX, KMED, KMIN, KMAX),
       'Kästchen offen nach Rev. 116: %d Hauptpunkte, %d Unterpunkte' % (HO, TO), ''] + PROT
os.makedirs(os.path.join(AUS, '03_Skripte'), exist_ok=True)
open(os.path.join(AUS, '03_Skripte', 'Steuerung_Rev116_2026-09-28.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(aus) + '\n')
print('\n'.join(aus))

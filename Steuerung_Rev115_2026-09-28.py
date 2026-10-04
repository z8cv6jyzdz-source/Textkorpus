# -*- coding: utf-8 -*-
"""
Steuerung_Rev115_2026-09-28.py — Teil 0 Rev. 115 und Maßnahmenliste nach dem Task Steuerdokumente 28.09.
Bachelorarbeit U15-Plyometrie · DSHS Köln · Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 7

Schreibt den Block Rev. 115 in Teil 0 der Sitzungsnotizen (vor Rev. 114) und die Stand-Zeile, schreibt die Maßnahmenliste fort
(Stand, A8, G25d, G26g, G29 bis G36, H6, H9, H10, I19, L9, L12, L14, Zusammenfassung mit gemessener Kästchenzählung).
Werte aus Seitenmodell, Messskript und Textvorschlag Einleitung, keine Zahl von Hand. Jede Ersetzung genau einmal, sonst Abbruch.
Aufruf: python Steuerung_Rev115_2026-09-28.py <Quelle Claude-Ordner (gestagte Originale)> <Arbeitsordner> <Ausgabeordner>
        <Uhrzeit Sitzungsuhr HH:MM>
Ohne Semikolon im Skript (chr(59)).
"""
import csv
import os
import re
import sys

QUELLE, ARBEIT, AUS, UHR = sys.argv[1:5]
SEMI = chr(59)
os.makedirs(AUS, exist_ok=True)
PROT = []


def de(x, nk=0):
    s = ('%.' + str(nk) + 'f') % x
    ganz, _, dez = s.partition('.')
    g = []
    while len(ganz) > 3:
        g.insert(0, ganz[-3:])
        ganz = ganz[:-3]
    g.insert(0, ganz)
    return '.'.join(g) + (',' + dez if dez else '')


def ersetze(text, alt, neu, was):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('ABBRUCH %s: Suchtext %d-mal gefunden: %s' % (was, n, alt[:90]))
    PROT.append('ersetzt: ' + was)
    return text.replace(alt, neu, 1)


def anhaengen(text, praefix, zusatz, was):
    zl = text.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('ABBRUCH %s: %d Zeilen beginnen mit %s' % (was, len(idx), praefix[:60]))
    zl[idx[0]] = zl[idx[0]].rstrip() + zusatz
    PROT.append('ergänzt: ' + was)
    return '\n'.join(zl)


def zeile(text, praefix, neu, was):
    zl = text.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('ABBRUCH %s: %d Zeilen beginnen mit %s' % (was, len(idx), praefix[:60]))
    zl[idx[0]] = neu
    PROT.append('Zeile ersetzt: ' + was)
    return '\n'.join(zl)


# ------------------------------------------------------------------ Werte aus den Dateien
h, mi = [int(x) for x in UHR.split(':')]
UHR_MESZ = '%02d:%02d' % ((h + 1) % 24, mi)
P = {r['parameter']: float(r['wert']) for r in csv.DictReader(open(os.path.join(ARBEIT, '03_Skripte', 'Seitenmodell_2026-09-28.csv'),
                                                                     encoding='utf-8'), delimiter=SEMI)}
GB, GO, TT = de(P['prognose_gesamt_basis'], 1), de(P['prognose_gesamt_obere'], 1), de(P['prognose_textteil'], 1)
NEIN = int(P['eintraege_basis'])
mess = open(os.path.join(ARBEIT, '03_Skripte', 'Manuskriptstand_2026-09-25.txt'), encoding='utf-8').read()
MP = re.findall(r'Prognose Einleitung bis Ende Literaturverzeichnis: (\d+,\d) Seiten', mess)
if len(MP) != 1:
    raise SystemExit('ABBRUCH: Prognose des Messskripts nicht eindeutig')
MP = MP[0]
w = {r['arbeitsnummer']: int(r['woerter']) for r in csv.DictReader(open(os.path.join(ARBEIT, '03_Skripte', 'Manuskriptstand_2026-09-25.csv'),
                                                                        encoding='utf-8'))}
K4 = sum(w[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.6', '4.7'])
W47 = w['4.7']
tv = open(os.path.join(QUELLE, '04_Uebergaben', 'Textvorschlag_Einleitung_2026-09-28.md'), encoding='utf-8').read()
TVW = re.findall(r'\| Wörter gesamt \| \*\*(\d{1,2}\.\d{3}|\d{3,4})\*\*', tv)[0]
pruef = open(os.path.join(ARBEIT, '03_Skripte', 'Steuerdokumente_Pruefung_2026-09-28.txt'), encoding='utf-8').read()
verg = open(os.path.join(ARBEIT, '03_Skripte', 'Projektanweisungen_Vergleich_F16_F17_2026-09-28.txt'), encoding='utf-8').read()
if 'GESAMT: alle Prüfungen bestanden' not in pruef or 'alle elf Prüfungen bestanden' not in verg:
    raise SystemExit('ABBRUCH: Prüfskript oder Vergleich nicht bestanden')
GELOESCHT = ['Projektanweisungen_Fassung14.md', 'Projektanweisungen_Fassung15.md', 'Textvorschlag_2.4_2026-09-26.md',
             'Textvorschlag_2.4_2026-09-27.md', 'Textvorschlag_2.4_2026-09-27_Fassung5.md', 'Uebergabe_Kapitel2_2026-09-26.md',
             'Uebergabe_2.4_Fassung6_2026-09-28.md', 'Uebergabe_Steuerdokumente_2026-09-25.md', 'Uebergabe_Datensicherung_2026-09-24.md',
             'Uebergabe_Blindrechnung_R_2026-09-24.md', 'Uebergabe_4.1_Studiendesign_2026-09-22.md',
             'Uebergabe_4.3_Untersuchungsablauf_2026-09-12.md', 'Uebergabe_4.4_Leistungsdiagnostik_2026-09-12.md',
             'Uebergabe_4.5.1_Heimtrainingsprogramm_2026-09-23.md', 'Uebergabe_4.6_Monitoring_2026-09-14.md',
             'Textvorschlag_4.1_2026-09-23.md', 'Textvorschlag_4.2_2026-09-22.md', 'Textvorschlag_4.5.1_2026-09-23.md',
             'Textvorschlag_4.7_2026-09-25.md', 'Befunde_Sofortblock_2026-09-13.md', 'Uebergabe_2.4_Zielgroessen_Diagnostik.md',
             'Manuskriptstand_und_Vollstaendigkeit_2026-09-13.md', 'Gliederung_2026-09-23.md', 'Uebergabe_Steuerdokumente_2026-09-28.md']
BEHALTEN = ['Textvorschlag_4.1_2026-09-12.md', 'Textvorschlag_4.2_2026-09-14.md', 'Textvorschlag_4.4_2026-09-13.md',
            'Textvorschlag_4.6_2026-09-14.md', 'Vollstaendigkeitspruefung_Methodik_2026-08-28.md']
NG = len(GELOESCHT)
V = dict(uhr=UHR, mesz=UHR_MESZ, gb=GB, go=GO, tt=TT, mp=MP, nein=NEIN, k4=de(K4), w47=W47, tvw=TVW, ng=NG, nb=len(BEHALTEN))

# ------------------------------------------------------------------ Sitzungsnotizen, Teil 0 Rev. 115
t = open(os.path.join(QUELLE, '00_Steuerung', 'Cowork_Sitzungsnotizen.md'), encoding='utf-8').read()
t = ersetze(t, '**Stand: (Rev. 114 — siehe Block oben.)', '**Stand: (Rev. 115 — siehe Block oben.) Zuvor: (Rev. 114 — siehe Block oben.)', 'SN Stand')
REV115 = '''### ⭐⭐ NEU (Rev. 115, 28.09.2026, %(uhr)s Sitzungsuhr, entspricht %(mesz)s MESZ): Task Steuerdokumente 28.09. — Projektanweisungen Fassung 17 per Klick freigegeben, Gliederung v5, Berichtsraster Rev. 3, Plan Rev. 5, Messskript Fassung 3 mit Seitenmodell, Übergabe Einleitung, README, Aufräumskript, Archiv, Skill-Vorschlag, Projektdokumente bereinigt

**Auftrag (Verfasser, 28.09., Startsatz der Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md`):** Schritte 1 bis 5 in der festgelegten Reihenfolge, kein Manuskripttext, keine Änderung am Master, Rücksprache nur per Klick. Parallel lief Task 7 neu (Rev. 114), dieser Task baut auf dessen Textvorschlag Einleitung auf (%(tvw)s Wörter). Master unverändert (48.791 Byte, MD5 e35315d6…, keine `comments.xml`).

**Klicks:** K1 ohne Vorspann (gezählt von der Einleitung bis zum Ende des Literaturverzeichnisses), K2 Regel R6 entfällt, K3 Tauschregel ab 32 Seiten, K6 Ankersatz in 6.1 und in der Zusammenfassung, 4.1 ohne Zwecksatz (16:27) · Fassung 17 § 6.6 „kein nachweisbarer Moderator“ · Vor-2020-Halbsatz nur bei Wirksamkeitsevidenz (17:54) · Erratum Khamis und Roche: kein Hinweis in der Arbeit, weder im Fließtext noch in Anhang G noch in Tab. H6 („Hinweis soll nicht mehr vorhanden sein … streichen ohne Widerworte“) · Verdünnungslogik in 6.1, als Limitation in 6.3 G3, 6.2 ohne eigenen Absatz (19:25) · K4 Bereinigung der Projektdokumente · K5 Fassung 17 freigegeben (19:58).

**Erledigt, alles per Skript mit Abbruch bei nicht eindeutiger Fundstelle:**
- Messskript `03_Skripte\\Manuskriptstand_2026-09-25.py` Fassung 3 (Einleitung mit dem Altbestand 2, 2.x und 3, Summen gegen 6.350, Block „Seitenschätzung“) und Seitenmodell `03_Skripte\\Seitenmodell_2026-09-28` (.py, .txt, .csv, Fassung 2 mit den Quellen des Textvorschlags Einleitung, %(nein)d Einträge). Modellrechnung: Textteil %(tt)s Seiten, Einleitung bis Ende des Literaturverzeichnisses %(gb)s Seiten mit vollen Budgets, %(go)s in der oberen Variante, %(mp)s mit den gemessenen Wörtern. Kapitel 4 %(k4)s gegen 2.550, 4.7 %(w47)s gegen 550.
- Projektanweisungen Fassung 17 `00_Steuerung\\Projektanweisungen_Fassung17.md`, Erzeuger `03_Skripte\\Projektanweisungen_Fassung17_2026-09-28.py` (Fassung 3), Vergleich mit Fassung 16 `03_Skripte\\Projektanweisungen_Vergleich_F16_F17_2026-09-28` (.py, .txt, Ordnerliste aus dem Gerät): alle elf Prüfungen bestanden. Neue Entscheidungen in § 13 Nr. 23 bis 41, darunter Nr. 40 (Erratum) und Nr. 41 (Verdünnungslogik).
- Gliederung v5 `01_Verfahren\\Gliederung_2026-09-28` (.md, .docx, .pdf, Erzeuger Fassung 2): fünf Kapitel mit Arbeits- und Endnummern, Urteil der Anwendbarkeitsprüfung, Ä2 bis Ä13, M24 bis M26, Wortlaut der offenen M-Punkte, v4 nur noch Herkunft. Berichtsraster Rev. 3 (.md, .docx, .pdf, Erzeuger Fassung 3): Kopfblock Einleitung, Kennzahlenblatt 25.09., 6.2.11, 6.2.12 und 5.1.11 neu. Plan Rev. 5 (Erzeuger Fassung 3). Übergabe Einleitung nachgezogen (offen nur § 8 Nr. 6). README und Aufräumskript auf Fassung 17 mit Fassung 16 in der Papierkorbliste (nach K5).
- Archiv: `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` (Vorstände von Berichtsraster Rev. 2, Plan Rev. 4, Messskript Fassung 2, Gliederung v4, README, Aufräumskript, Fassung 16) und `_Archiv\\_ersetzt_2026-09-28_Uebergaben` (erledigte Übergaben und Textvorschläge zu Kapitel 2 und 2.4, Übergaben Steuerdokumente 25.09. und 28.09., Textvorschlag 4.7 vom 25.09., Übergabe Textrevision, Vorstand der Übergabe Einleitung), je MD5 gegen das Original geprüft.
- Prüfskript `03_Skripte\\Steuerdokumente_Pruefung_2026-09-28` (a) bis (l): alle bestanden. T4 um `dV2009` ergänzt (`03_Skripte\\T4_Nachtrag_dV2009_2026-09-28.py`).
- Skill `kapiteltext-bachelorarbeit`: vollständiger Vorschlag auf dem Stand von Fassung 17, Gliederung v5 und Berichtsraster Rev. 3 zur Speicherung vorgelegt (G26g).
- Projektdokumente (K4): %(ng)d überholte Kopien gelöscht, je mit Original im Ordner oder im Archiv. Behalten, weil kein Original auffindbar ist: %(nb)d (Textvorschläge 4.1 vom 12.09., 4.2 vom 14.09., 4.4 vom 13.09., 4.6 vom 14.09., Vollständigkeitsprüfung Methodik vom 28.08.).

**Übergreifende Zweitprüfung** (unabhängiger Subagent, alle Steuerdokumente gegeneinander, 42 Befunde, jeder eingearbeitet oder per Klick entschieden): Objekte erst in Task 18, im Text keine Platzhalter (Fassung 17 § 13 Nr. 16, Plan Task 11 und 18, Gliederung v5 M11, M12, M26) · Ramirez-Campillo et al. (2023) und Zheng et al. (2025) nur nicht als Beleg einer Mindestdosis (§ 6.6) · Berichtsraster auf das Kennzahlenblatt 25.09. (K-05, K-11, K-10.5), 5.1.5 ohne Kennwerte, 20-m-Zwischenzeit in Tab. H6 und G7, 48 h als Tatsache in 4.3, G8-Wortlaut, § 4 Nr. 2 historisch, Semikola der geänderten Kopfblöcke ersetzt · „vorgemerkt für“ an leeren Zielorten · Übergabe Einleitung Zeile 1.3 nach Raster Rev. 3, G31 (c) in § 8 Nr. 6 · Plan: Musterdatei Textvorschlag 4.7 vom 26.09., F17 § 1.2, § 4 Nr. 1, Klickpunkt Nr. 23 in Task 11, Eingang Task 12, Streichpaket Bootstrap, Nr. 57a und Tab. H6 ohne R1, R9, R10, R12, R13 und R14 in Task 18, Präfix E vor der Umnummerierung, Folge der Klickfrage 12, § 7.1 Nr. 5 bis 9 als beantwortet · Gliederung v5 ohne Grundlage im Archiv · Seitenmodell mit den Quellen des Textvorschlags · Ordnerliste aus dem Gerät · Lesefassungen erzeugt · Vorstände archiviert · Skill-Entwurf korrigiert. Zwei Befunde führten zu Klicks (Erratum, Verdünnungslogik, 19:25).

**Zur Kenntnis:** Die Spielklasse der drei Mannschaften ist gegen das Einschlusskriterium von Oliver et al. (2024) zu prüfen (G35 i, mit Task 7 neu). `Verletzungsprävention_Vereinssport.pptx` liegt zweimal im Projekt, der Verfasser entfernt eine Kopie selbst in claude.ai.

**Stand der Dateien:** Geändert oder neu: Fassung 17, Gliederung v5 (.md, .docx, .pdf), Berichtsraster (.md, .docx, .pdf), Plan, Übergabe Einleitung, README, Aufräumskript, Messskript-Ausgaben, Seitenmodell, T4, Maßnahmenliste, diese Notizen, die Skripte des Tasks und die Archivordner. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen, Protokoll in `03_Skripte\\Steuerung_Rev115_2026-09-28.txt`. Der Arbeitsordner `archiv` des Containers wird nicht zurückgeschrieben. Projektkopien: Fassung 17, Gliederung v5, Berichtsraster, Plan, Maßnahmenliste, Übergabe Einleitung, Sitzungsnotizen (nach K4 wieder möglich).

**Offen beim Verfasser:** (1) Fassung 17 in die Projekteinstellungen einsetzen (A8) · (2) danach `Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt (Fassung 16, Gliederung v4, erledigte Übergaben und Textvorschläge) · (3) Skill-Vorschlag speichern · (4) die Einleitung in den Master übertragen (Task 7 neu, Rev. 114).

**Nächster Schritt:** Nach der Übertragung der Einleitung die Übergabe Einleitung § 8 Nr. 6 (Abgleich Satz für Satz, Messskript, Endabgleich, Rev. 116, Maßnahmenliste mit G35 i, T1, T4, Plan, Projektkopien). Danach Task 11 (Kapitel 5) mit dem Startsatz aus Plan § 8, Nr. 23 per Klick zu Beginn. Nach dem Einsetzen von Fassung 17 die Projektkopie `claude/Projektanweisungen_Fassung16.md` löschen.

''' % V
t = ersetze(t, '### ⭐⭐ NEU (Rev. 114, 28.09.2026, 16:40 Sitzungsuhr', REV115 + '### ⭐⭐ NEU (Rev. 114, 28.09.2026, 16:40 Sitzungsuhr', 'SN Rev. 115')

# ------------------------------------------------------------------ Maßnahmenliste
m = open(os.path.join(QUELLE, '00_Steuerung', 'Massnahmenliste_Datenverarbeitung.md'), encoding='utf-8').read()
m = ersetze(m, '**Stand 28.09.2026, 15:45 Sitzungsuhr, entspricht 16:45 MESZ (Rev. 113 —',
            '**Stand 28.09.2026, %(uhr)s Sitzungsuhr, entspricht %(mesz)s MESZ (Rev. 115 — Task Steuerdokumente 28.09.: Projektanweisungen '
            'Fassung 17 per Klick freigegeben (A8 wieder offen: einsetzen), Gliederung v5, Berichtsraster Rev. 3, Plan Rev. 5, Messskript Fassung 3, '
            'Seitenmodell, README, Aufräumskript, Archiv, Skill-Vorschlag, %(ng)d Projektkopien bereinigt. A8, G25d, G26g, G29 bis G36, H6, H9, H10, '
            'I19, L9, L12, L14 und die Zusammenfassung fortgeschrieben, G35 (i) und (j) neu). Zuvor 28.09.2026, 15:45 Sitzungsuhr, entspricht '
            '16:45 MESZ (Rev. 113 —' % V, 'ML Stand')
m = ersetze(m, '- [x] **A8 · ⭐ Projektanweisungen Fassung 15 in die claude.ai-Projekteinstellungen einsetzen** — ',
            '- [ ] **A8 · ⭐ Projektanweisungen Fassung 17 in die claude.ai-Projekteinstellungen einsetzen** — **Rev. 115 (28.09., 19:58 '
            'Sitzungsuhr, Klick K5): Fassung 17 freigegeben. Offen beim Verfasser, in dieser Folge: (1) den Text aus '
            '`00_Steuerung\\Projektanweisungen_Fassung17.md` (oder der Projektkopie) vollständig in die Projekteinstellungen kopieren · (2) Fassung 16 '
            'liegt schon als Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` (MD5 gleich) und steht in der Papierkorbliste · (3) '
            '`Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt (Fassung 16, Gliederung v4, erledigte Übergaben und Textvorschläge) · (4) danach die '
            'Projektkopie `claude/Projektanweisungen_Fassung16.md` löschen (nächster Task).** Zuvor zu Fassung 15 und 16: ', 'ML A8')
m = ersetze(m, 'Übergaben 5/6/7 mit § 3.1 und G16c bestücken.',
            'Übergaben 5/6/7 mit § 3.1 und G16c bestücken. *(Rev. 115, 28.09.: M11 und M12 in Task 18, vorher keine Platzhalter (Fassung 17 '
            '§ 5.3, Wortlaut in Gliederung v5 § 5), M16 Task 13, M23 optional, Tab. 1 als M26 in Task 18.)*', 'ML G25d')
m = ersetze(m, 'Speichern und in der nächsten Sitzung prüfen (analog G16a/G18d).',
            'Speichern und in der nächsten Sitzung prüfen (analog G16a/G18d). *(Rev. 115, 28.09.: neuer vollständiger Vorschlag auf dem Stand von '
            'Fassung 17, Gliederung v5 und Berichtsraster Rev. 3 zur Speicherung vorgelegt. Speichern beim Verfasser, Stand zu Beginn von Task 11 '
            'prüfen.)*', 'ML G26g')
m = ersetze(m, '(i) und (j) Task 15, Einzelheiten in G32.)*',
            '(i) und (j) Task 15, Einzelheiten in G32.)* *(Rev. 115, 28.09.: (a) Erratum seit dem Klick 19:25 überhaupt nicht in der Arbeit '
            '(Fassung 17 § 13 Nr. 40) · (f) Verdünnung in 6.1 und als Limitation in G3 (Klick 19:25, § 13 Nr. 41) · (g) überholt, Anhang G ohne '
            'Prüfprotokolle (Textvorschlag 4.7 Nr. 57, G32 g).)*', 'ML G29')
m = ersetze(m, '*(Rev. 113: Plan Rev. 5 im Task Steuerdokumente 28.09., Übergabe § 5.3)*',
            '*(Rev. 113: Plan Rev. 5 im Task Steuerdokumente 28.09., Übergabe § 5.3)* *(Rev. 115: Plan Rev. 5 erstellt per '
            '`03_Skripte\\Plan_Rev5_2026-09-28.py` (Fassung 3), Rev. 4 im Archiv.)*', 'ML G30')
m = ersetze(m, '(c) läuft in Task 7.)*',
            '(c) läuft in Task 7.)* *(Rev. 115, 28.09.: Der Platzhalter ⟨Tab. 1⟩ aus (a) entfällt, Tab. 1 setzt Task 18 direkt nach (b) '
            '(Gliederung v5 M26, Fassung 17 § 5.3). Offen aus (a) nur die Überschrift 4.4.2 ohne „(bilateral)“ (Task 18). (c) mit Task 7 neu.)*',
            'ML G31')
m = ersetze(m, '(h) Task 18: Tab. H6 aus Auswertungsplan § 5.10 mit Spalte Grund',
            '(h) Task 18: Tab. H6 aus Auswertungsplan § 5.10 ohne R1, R9, R10, R12, R13 und R14 (Fassung 17 § 13 Nr. 40), mit Spalte Grund',
            'ML G32 h')
m = ersetze(m, 'in § 7. *(26.09., Rev. 108)*',
            'in § 7. *(26.09., Rev. 108)* *(Rev. 115, 28.09.: (e) mit Task 7 neu (Textvorschlag Einleitung A9) · (g) Anhang G ohne '
            'Prüfprotokolle, Folge der Klickfrage 12 für 4.7 im Plan Task 16 · (j) erledigt bis auf Umfangsdokument R5 und Fassung 17 § 11.9, '
            'beide offen bis zur Entscheidung über Nr. 23 zu Beginn von Task 11.)*', 'ML G32')
m = ersetze(m, '(auch 2.2 und 2.3). *(28.09., Rev. 110)*',
            '(auch 2.2 und 2.3). *(28.09., Rev. 110)* *(Rev. 115: (c) erledigt in Fassung 17 § 6.5 (Nimphius mit den gedruckten Seiten, Korpus '
            '2.4 auf den Quellenpool der Vorarbeit) · (d) und (f) Task 12.)*', 'ML G33')
m = ersetze(m, '*(28.09., Rev. 111, neu gefasst Rev. 112)*',
            '*(28.09., Rev. 111, neu gefasst Rev. 112)* *(Rev. 115: (e) erledigt in Fassung 17 § 2, § 6.5, § 6.6, § 12 G8 und § 13 · (b) mit '
            'Task 7 neu · (c) Hilska 2021 für Task 12.)*', 'ML G34')
m = ersetze(m, '*(28.09., Rev. 112, ergänzt Rev. 113)*',
            '*(28.09., Rev. 112, ergänzt Rev. 113)* *(Rev. 115, 28.09.: (b) Seitenzahlen überholt, Modellrechnung nach dem Seitenmodell %(gb)s '
            'Seiten mit vollen Budgets, %(mp)s mit den gemessenen Wörtern (Gliederung v5 § 3.4), R6 entfällt (K2) · (f) erledigt (Fassung 17, '
            'Gliederung v5, Berichtsraster Rev. 3, Plan Rev. 5) · (h) erledigt mit K6 (16:27): Ankersatz in 6.1 und in der Zusammenfassung, 4.1 '
            'ohne Zwecksatz · (i) neu: Spielklasse der drei Mannschaften gegen das Einschlusskriterium von Oliver et al. (2024) prüfen (Fassung 17 '
            '§ 2, Zeile Leistungsniveau), mit Task 7 neu nach Übergabe Einleitung § 8 Nr. 6 · (j) neu: Vormerkungen für Task 12 aus Textvorschlag '
            'Einleitung § 6 Nr. 7 (Ankersatz A9 S1, Zheng und Ramirez-Campillo 2023 beim 505, Flores 2025 für 6.2, Bouafif 2026 für 6.1, Behm 2017 '
            'und de Villarreal 2009 für G8, Hilska 2021 für G5, Lloyd 2016 nach L14 b).)*' % V, 'ML G35')
m = ersetze(m, 'Die Grenze 33 ist strenger als die Betreuervorgabe 37 und gilt vor ihr. *(28.09., Rev. 113)*',
            'Die Grenze 33 ist strenger als die Betreuervorgabe 37 und gilt vor ihr. *(28.09., Rev. 113)* *(Rev. 115: (a) erledigt: K1 ohne '
            'Vorspann, K2 R6 entfällt, K3 Tauschregel ab 32 Seiten (16:27) · (b) ersetzt durch das Seitenmodell `03_Skripte\\Seitenmodell_2026-09-28` '
            '(Modellrechnung): Textteil %(tt)s, Einleitung bis Ende des Literaturverzeichnisses %(gb)s Seiten, obere Variante %(go)s, mit den '
            'gemessenen Wörtern %(mp)s · (c) erledigt · (d) bleibt.)*' % V, 'ML G36')
m = ersetze(m, '**Hoffmann et al. (2014)** über EQUATOR. *(PA § 7.1)*',
            '**Hoffmann et al. (2014)** über EQUATOR. *(PA § 7.1)* *(Rev. 115, 28.09.: Hoffmann et al. (2014) erledigt, der Volltext liegt im '
            'Ordner, T1-Steckbrief mit Task 15. Clemente et al. (2022) nur noch bei Bedarf für 6.1, in der Einleitung entfallen.)*', 'ML H6')
m = ersetze(m, '4.7 nennt den Faktor ohne Beleg, weil der Volltext fehlt (F14 § 7.1).',
            '4.7 nennt Hedges\' g ohne Beleg, weil der Volltext fehlt (F14 § 7.1, Wortlaut nach Rev. 115).', 'ML H9')
m = ersetze(m, 'gebraucht für 2.4 Fassung 6 (Güteaussagen) und 6.2.',
            'gebraucht nur noch optional für 6.2 (2.4 Fassung 6 wird nicht übertragen, Rev. 115).', 'ML H10')
m = anhaengen(m, '- [x] **I19 ·', ' *(Rev. 115: Berichtsraster-Teil erledigt mit Rev. 3 (4.2.5, Kopfblock 3.11, 4.7.13), die übrigen '
              'Nachtragsvermerke stehen in Fassung 17 § 1.3.)*', 'ML I19')
m = ersetze(m, '*(Rev. 96, 25.09.: als Task 15 im Plan der weiteren Schritte, Umfang von Anhang G ist Klickfrage 11)*',
            '*(Rev. 96, 25.09.: als Task 15 im Plan der weiteren Schritte, Umfang von Anhang G ist Klickfrage 11)* *(Rev. 115, 28.09.: Task 16 '
            'des Plans, Umfang von Anhang G ist Klickfrage 12. Der Methodenteil 4.7 ist mit Task 6 erledigt (%(w47)s Wörter), nach Nr. 57 ohne '
            'KI-Sammelsatz und ohne Prüfprotokolle. Anhang G ohne Prüfprotokolle und ohne Erratum (Fassung 17 § 13 Nr. 40). Offen: '
            'KI-Deklaration mit Mindestinhalt, Nutzungsprotokoll, Anhang G mit Poweranalyse-Eingaben, R-Skripten und Diagrammen, '
            'Reproduktionstest.)*' % V, 'ML L9')
m = anhaengen(m, '- [x] **L12 ·', ' *(Rev. 115, 28.09., Klick 19:25: kein Hinweis auf das Erratum in der Arbeit, weder im Fließtext noch in '
              'Anhang G noch in Tab. H6. Rechercheprotokoll und Registereintrag R14 bleiben Projektdokumentation, Fassung 17 § 13 Nr. 40.)*',
              'ML L12')
m = ersetze(m, '(c) und (d) Task 15.)*',
            '(c) und (d) Task 15.)* *(Rev. 115, 28.09.: (a) Hinweis auf das Planungsmodell für 6.2 vorgemerkt (Fassung 17 § 11.1) · (c) '
            'erledigt, Moran et al. (2017) nach der Version of Record (Rev. 114) · (d) Band und Seiten bei Crossref geprüft (Fassung 17 § 8), offen '
            'nur der Volltext der Verlagsfassung.)*', 'ML L14')
# Zusammenfassung
m = ersetze(m, 'Rev. 2 vom 25.09., Kürzung zuerst):**', 'Rev. 5 vom 28.09.):**', 'ML Zusammenfassung Kopf')
m = ersetze(m, 'A8 erledigt (Rev. 106) |', 'A8 für Fassung 16 erledigt (Rev. 106), für Fassung 17 wieder offen (Rev. 115) |', 'ML Zeile 1')
m = zeile(m, '| 1b Steuerdokumente 28.09.',
          '| 1b Steuerdokumente 28.09. (erledigt 28.09., Rev. 115) | G36 (a), (c) · G35 (f), (h) · G34 (e) · G33 (c) · G32 (j) bis auf R5 und '
          'F17 § 11.9 · G29 (g) (überholt) · I19 · G30 · offen beim Verfasser: A8 (Fassung 17 einsetzen, dann Aufräumskript), G26g (Skill speichern) |',
          'ML Zeile 1b')
m = ersetze(m, '| G35 (a), (e), (g) · G34 (b), (c) ·', '| G35 (a), (e), (g), (i) · G34 (b), (c) ·', 'ML Zeile 7 neu')
m = ersetze(m, '· K19 und G31 (c) · H10 · G18c · G19c |', '· K19 und G31 (c) · G18c · G19c |', 'ML Zeile 7 neu H10')
m = zeile(m, '| 11 Kapitel 5 |', '| 11 Kapitel 5 | B5 (Rest) · G28g · G29 (d), (e) · G32 (b) mit Nr. 23 per Klick zu Beginn · G32 (j) Rest '
          '(Umfangsdokument R5, F17 § 11.9) · G26g (Skill-Stand prüfen) |', 'ML Zeile 11')
m = ersetze(m, '(Hilska 2021 in 6.3) · G33 (d), (f) |', '(Hilska 2021 in 6.3) · G33 (d), (f) · G35 (j) (Textvorschlag Einleitung § 6 Nr. 7) · '
            'H10 (optional) |', 'ML Zeile 12')
m = ersetze(m, '· L14 (c), (d) ·', '· L14 (d) (Volltext der Verlagsfassung) · H6 (T1 Hoffmann 2014) ·', 'ML Zeile 15')
m = zeile(m, '| 16 Phase 8 |', '| 16 Phase 8 | L9 · G32 (g) |', 'ML Zeile 16')
m = zeile(m, '| 18 Endredaktion |', '| 18 Endredaktion | G29 (h) · G22 (Rest) · G18, G19 (Nullstand) · G13 (Rest) · G31 (a) Überschrift 4.4.2, (b) '
          'Tab. 1 (M26) · G25d (M11, M12) · G17g (Tab.-2-Feld) · G32 (h) mit Streichpaket Bootstrap und Nr. 57a · G35 (d) (Umnummerierung, '
          'vorher Präfix E im Berichtsraster) |', 'ML Zeile 18')
HO = len(re.findall(r'^- \[ \] \*\*', m, re.M))
TO = len(re.findall(r'^    - \[ \] \*\*', m, re.M))
m = ersetze(m, '| **Summe** | **33 Hauptpunkte und 35 Teilpunkte offen** (',
            '| **Summe** | **Rev. 115 (28.09.), per Skript an den Kästchen gezählt: %d Hauptpunkte und %d Unterpunkte mit offenem Kästchen** (die '
            'Buchstabenpunkte innerhalb eines Eintrags nicht gezählt, darum nicht vergleichbar mit der Zählung darunter). A8 wieder offen, G35 (i) '
            'und (j) neu. Zuvor: **33 Hauptpunkte und 35 Teilpunkte offen** (' % (HO, TO), 'ML Summe')

for name, text in [('Cowork_Sitzungsnotizen.md', t), ('Massnahmenliste_Datenverarbeitung.md', m)]:
    with open(os.path.join(AUS, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    PROT.append('geschrieben %s: %d Byte' % (name, len(text.encode('utf-8'))))
aus = ['Steuerung_Rev115_2026-09-28.py — Teil 0 Rev. 115 und Maßnahmenliste (Task Steuerdokumente 28.09.)',
       'Uhrzeit Sitzungsuhr %s (MESZ %s) · Seitenmodell %s / %s / Textteil %s · Messskript %s · Kapitel 4 %s · 4.7 %d · Textvorschlag %s'
       % (UHR, UHR_MESZ, GB, GO, TT, MP, de(K4), W47, TVW),
       'Projektkopien gelöscht (K4): %d · behalten ohne Original: %d' % (NG, len(BEHALTEN)),
       'Kästchen offen nach Rev. 115: %d Hauptpunkte, %d Unterpunkte' % (HO, TO), ''] + PROT
open(os.path.join(ARBEIT, '03_Skripte', 'Steuerung_Rev115_2026-09-28.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(aus) + '\n')
print('\n'.join(aus))

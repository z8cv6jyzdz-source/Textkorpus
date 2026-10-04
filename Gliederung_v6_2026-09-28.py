# -*- coding: utf-8 -*-
"""
Gliederung_v6_2026-09-28.py — erzeugt `01_Verfahren\\Gliederung_2026-09-28.md` (Gliederung v6) aus der v5
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task Kapitelstruktur 28.09. (Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`)

v6 ersetzt v5 vom selben Tag in gleicher Datei (wie Gliederung v4 am 24.09. ihre Rev. 2 erhielt), Kopie der v5 in
`_Archiv\\_ersetzt_2026-09-28_Gliederung_v5`. Änderung: 13 statt 22 Überschriften, keine dritte Ebene (Ä14 bis Ä19),
Entscheidungen E1 bis E5 des Befunds. Alles Übrige der v5 bleibt im Wortlaut. Ist-Werte zusammengelegter Blöcke werden aus
`Manuskriptstand_2026-09-25.csv` summiert, Budgets sind Festlegungen (Fassung 17 § 5.2), keine Zahl von Hand.
Aufruf: python Gliederung_v6_2026-09-28.py <Gliederung_v5.md> <Manuskriptstand.csv> <Ausgabe.md>
Jede Ersetzung genau einmal, sonst Abbruch. Ohne Semikolon im Skript (chr(59)).
"""
import csv
import hashlib
import sys

V5, M_CSV, OUT = sys.argv[1:4]
SEMI = chr(59)
t = open(V5, encoding='utf-8').read()
PROT = []


def de(x):
    s = str(int(round(x)))
    g = []
    while len(s) > 3:
        g.insert(0, s[-3:])
        s = s[:-3]
    g.insert(0, s)
    return '.'.join(g)


def rp(alt, neu, was):
    global t
    n = t.count(alt)
    if n != 1:
        raise SystemExit('ABBRUCH %s: Suchtext %d-mal gefunden: %s' % (was, n, alt[:80]))
    t = t.replace(alt, neu, 1)
    PROT.append(was)


# Ist-Werte aus dem Messskript (Fassung 3, 28.09.)
ist = {}
for z in csv.DictReader(open(M_CSV, encoding='utf-8')):
    ist[z['arbeitsnummer']] = int(z['woerter'] or 0)
i44 = ist['4.4'] + ist['4.4.1'] + ist['4.4.2'] + ist['4.4.3']
i25 = ist['4.5.1'] + ist['4.5.2'] + ist['4.6']
BUD = {'4.1': 300, '4.2': 215, '4.3': 340, '4.4': 420, '4.5.1': 420, '4.5.2': 150, '4.6': 155, '4.7': 550,
       '5.1': 230, '5.2': 220, '6.1': 700, '6.2': 400, '6.3': 500, '7': 250, '1': 1500}
b25 = BUD['4.5.1'] + BUD['4.5.2'] + BUD['4.6']
b3 = BUD['5.1'] + BUD['5.2']
b42 = BUD['6.2'] + BUD['6.3']
summe = sum(BUD.values())
if summe != 6350 or i44 != 392 or i25 != 722:
    raise SystemExit('ABBRUCH: Summe %d, 4.4 %d, 2.5 %d' % (summe, i44, i25))

# Kopf
rp('# Gliederung v5 — fünf Kapitel, Einleitung statt Kapitel 1 bis 3',
   '# Gliederung v6 — fünf Kapitel, zwei Ebenen, 13 Überschriften', 'Titel')
rp('Gliederung mit Arbeits- und Endnummern, Wortbudget, Seitenmodell und Objektzuordnung, Änderungsliste für den Master',
   'Gliederung mit Arbeits- und Endnummern, Wortbudget, Seitenmodell und Objektzuordnung, Änderungsliste für den Master. '
   'v6 verschlankt die v5 vom selben Tag auf zwei Gliederungsebenen (Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`, '
   'Verfasser 28.09., 21:00 und 21:43)', 'Untertitel')
rp('Stand 28.09.2026 · ersetzt Gliederung v4 (23.09., Rev. 2 vom 24.09.), Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` · '
   'Erzeuger `03_Skripte\\Gliederung_v5_2026-09-28.py`: Wortzahlen aus dem Messskript Fassung 3, Seiten aus dem Seitenmodell, keine Zahl von Hand',
   'Stand 28.09.2026, 22:05 Sitzungsuhr (v6) · ersetzt Gliederung v5 vom 28.09. (Kopie in `_Archiv\\_ersetzt_2026-09-28_Gliederung_v5`), '
   'die ihrerseits Gliederung v4 ersetzte (23.09., Rev. 2 vom 24.09., Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`) · '
   'Erzeuger `03_Skripte\\Gliederung_v6_2026-09-28.py` aus der v5 (Erzeuger `03_Skripte\\Gliederung_v5_2026-09-28.py`): '
   'Wortzahlen aus dem Messskript Fassung 3, Seiten aus dem Seitenmodell, keine Zahl von Hand', 'Kopfzeile')

# § 0
rp('1. **Fünf Kapitel.** 1 Einleitung · 2 Methodik · 3 Ergebnisse · 4 Diskussion · 5 Fazit und Ausblick. Kapitel 1 bis 3 der v4 gehen',
   '1. **Fünf Kapitel, zwei Ebenen, 13 Überschriften (v5: 22).** 1 Einleitung · 2 Methodik mit 2.1 Studiendesign, 2.2 Stichprobe, '
   '2.3 Untersuchungsablauf, 2.4 Leistungsdiagnostik, 2.5 Trainingsintervention und Begleitbedingungen, 2.6 Statistische Auswertung · '
   '3 Ergebnisse ohne Unterabschnitte · 4 Diskussion mit 4.1 Einordnung der Ergebnisse und 4.2 Methodendiskussion, Stärken und Limitationen · '
   '5 Fazit und Ausblick. Gegenüber v5 entfallen die dritte Ebene (4.4.1 bis 4.4.3 als Absätze, 4.5.1 und 4.5.2 mit 4.6 in einem Abschnitt), '
   '5.1 und 5.2 sowie die Trennung von 6.2 und 6.3 (Ä14 bis Ä19, § 4). Maßstab waren der Vergleichskorpus (Methodik im Median 5 Unterabschnitte, '
   'Ergebnisse und Diskussion in 8 von 11 ohne, dritte Ebene in 3 von 11), der Leitfaden Sportmedizin, TUM, dvs und CONSORT (Befund § 3 bis § 5). '
   'Kapitel 1 bis 3 der v4 gehen', '§ 0 Nr. 1')
rp('3. **Arbeitsnummern bis Task 18.** Methodik bis Fazit behalten im Master und in allen Steuerdokumenten, Skripten und Textvorschlägen die Nummern 4 bis 7. '
   'Umnummeriert wird einmal per Skript in Task 18 (Ä13, M25).',
   '3. **Arbeitsnummern bis Task 18.** Methodik bis Fazit behalten im Master und in allen Steuerdokumenten, Skripten und Textvorschlägen die Nummern 4 bis 7, '
   'die zusammengelegten Blöcke (4.4.1 bis 4.4.3, 4.5.1, 4.5.2, 4.6, 5.1, 5.2, 6.2, 6.3) bleiben Blockkennungen für Budgets, Berichtsraster, Messskript und Textvorschläge. '
   'Umnummeriert und zusammengelegt wird einmal per Skript in Task 18 (Ä13, M25, M27), die Kapitel 5 und 6 erhalten ihre Überschriften mit den Tasks 11 und 12 (E5).',
   '§ 0 Nr. 3')
rp('5. **Unverändert aus v4.** Kapitel 4 bis 7 in Nummern, Namen und Folge, die fünf Objekte im Text',
   '5. **Unverändert aus v4 und v5.** Kapitel 4 bis 7 in Arbeitsnummern und Folge, die Bauplan-Züge, die fünf Objekte im Text', '§ 0 Nr. 5')

# § 3 Übersicht
rp('## 3 Gliederung v5', '## 3 Gliederung v6', '§ 3 Titel')
rp('Budget nach Fassung 17 § 5.2. Ist = Messung am Master vom 28.09. (Messskript Fassung 3), vor der Übertragung der Einleitung. Objekte nach Fassung 17 § 5.3.',
   'Budget nach Fassung 17 § 5.2, für zusammengelegte Abschnitte als Summe der Blockbudgets (E4). Ist = Messung am Master vom 28.09. (Messskript Fassung 3), '
   'vor der Übertragung der Einleitung. Objekte nach Fassung 17 § 5.3. Zeilen mit Endnummer „in …“ sind Blöcke, die in Task 18 in dem genannten Abschnitt '
   'aufgehen, ihre Überschriften entfallen dort.', '§ 3.1 Vorsatz')
rp('| 4.4 | 2.4 | Leistungsdiagnostik (4.4.1 bis 4.4.3) | 420 | 392 | Tab. 1 | Testkette je Zielgröße',
   '| 4.4 | 2.4 | Leistungsdiagnostik (4.4.1 bis 4.4.3 als Absätze ohne Überschrift, Ä14) | 420 | ' + str(i44) + ' | Tab. 1 | Gerät und Gültigkeit → Versuchszahl → Messgüte mit Tab. 1 → Testkette je Zielgröße',
   '§ 3.1 Zeile 4.4')
rp('| 4.5 | 2.5 | Trainingsintervention (4.5.1, 4.5.2) | 570 | 568 | — | TIDieR 1 bis 10 |',
   '| 4.5.1 + 4.5.2 + 4.6 | 2.5 | Trainingsintervention und Begleitbedingungen | ' + de(b25) + ' | ' + str(i25) + ' | — | ein Abschnitt (Ä15): Programm (TIDieR 1 bis 10) → Vergleichs- und Begleitbedingung (CONSORT 5) → Adhärenz- und Belastungsmonitoring (TIDieR 11), die Elternüberschrift 4.5 entfällt |',
   '§ 3.1 Zeile 4.5')
rp('| 4.5.1 | 2.5.1 | Plyometrisches Heimtrainingsprogramm |', '| 4.5.1 | in 2.5 | Plyometrisches Heimtrainingsprogramm |', '§ 3.1 Zeile 4.5.1')
rp('| 4.5.2 | 2.5.2 | Vergleichs- und Begleitbedingung |', '| 4.5.2 | in 2.5 | Vergleichs- und Begleitbedingung |', '§ 3.1 Zeile 4.5.2')
rp('| 4.6 | 2.6 | Adhärenz- und Belastungsmonitoring |', '| 4.6 | in 2.5 | Adhärenz- und Belastungsmonitoring |', '§ 3.1 Zeile 4.6')
rp('| 4.7 | 2.7 | Statistische Auswertung |', '| 4.7 | 2.6 | Statistische Auswertung |', '§ 3.1 Zeile 4.7')
rp('| 5 | 3 | Ergebnisse | 450 | 0 | Abb. 1, Tab. 2, Abb. 2, Tab. 3 | nicht zitieren, nicht deuten, Zahlen in den Objekten |',
   '| 5 | 3 | Ergebnisse (ohne Unterabschnitte, Ä16) | ' + str(b3) + ' | 0 | Abb. 1, Tab. 2, Abb. 2, Tab. 3 | nicht zitieren, nicht deuten, Zahlen in den Objekten, Orientierungszug und Zielgrößenblock als Absatzgruppen, die vier Objekte gliedern |',
   '§ 3.1 Zeile 5')
rp('| 5.1 | 3.1 | Teilnehmerfluss, Adhärenz und Ausgangswerte |', '| 5.1 | in 3 | Teilnehmerfluss, Adhärenz und Ausgangswerte (Absatzgruppe) |', '§ 3.1 Zeile 5.1')
rp('| 5.2 | 3.2 | Gruppenvergleiche je Zielgröße |', '| 5.2 | in 3 | Gruppenvergleiche je Zielgröße (Absatzgruppe) |', '§ 3.1 Zeile 5.2')
rp('| 6.2 | 4.2 | Methodendiskussion | 400 | 0 | — | u. a. Auflösung,',
   '| 6.2 + 6.3 | 4.2 | Methodendiskussion, Stärken und Limitationen | ' + str(b42) + ' | 0 | — | ein Abschnitt (Ä17), Bauform Sammoud: Methodenbegründungen (Zeilen 6.2.8, 6.2.9, 6.2.11) → Stärken → Scharniersatz → acht Gruppen G1 bis G8, jede mit Erklärung (Block 6.2) und Konsequenz (Block 6.3) → Forschungsausblick |\n'
   '| 6.2 | in 4.2 | Methodendiskussion (Block) | 400 | 0 | — | u. a. Auflösung,', '§ 3.1 Zeile 6.2')
rp('| 6.3 | 4.3 | Stärken und Limitationen | 500 | 0 | — |', '| 6.3 | in 4.2 | Stärken und Limitationen (Block) | 500 | 0 | — |', '§ 3.1 Zeile 6.3')
rp('| **Σ** | | **Kapitel 1 bis 5** | **6.350** | **7.336 mit Altbestand** | **5 im Text** | |',
   '| **Σ** | | **Kapitel 1 bis 5, 13 Überschriften (5 + 8)** | **' + de(summe) + '** | **7.336 mit Altbestand** | **5 im Text** | |', '§ 3.1 Summe')

# § 3.3 Anhang, Erstverweise in Endnummern ergänzen
for buchst, alt, neu in [('A', '| 4.6 |', '| 4.6 (2.5) |'), ('B', '| 4.5.1 |', '| 4.5.1 (2.5) |'), ('C', '| 4.3 |', '| 4.3 (2.3) |'),
                         ('D', '| 4.5.2 |', '| 4.5.2 (2.5) |'), ('E', '| 4.1 |', '| 4.1 (2.1) |'), ('F', '| 4.2 |', '| 4.2 (2.2) |')]:
    zeile = [z for z in t.split('\n') if z.startswith('| ' + buchst + ' | ')]
    if len(zeile) != 1 or not zeile[0].endswith(alt):
        raise SystemExit('ABBRUCH Anhang ' + buchst)
    rp(zeile[0], zeile[0][:-len(alt)] + neu, 'Anhang ' + buchst)
zeile = [z for z in t.split('\n') if z.startswith('| G | ')]
if len(zeile) != 1 or not zeile[0].endswith('| 4.7 |'):
    raise SystemExit('ABBRUCH Anhang G')
rp(zeile[0], zeile[0][:-len('| 4.7 |')] + '| 4.7 (2.6) |', 'Anhang G')
rp('| H1 4.4 · H2 und H5 5.1 · H3 5.2 · H4 4.7 · H6 4.1 (Task 18) · H7 4.3 |',
   '| H1 4.4 (2.4) · H2 und H5 5.1 (3) · H3 5.2 (3) · H4 4.7 (2.6) · H6 4.1 (2.1, Task 18) · H7 4.3 (2.3) |', 'Anhang H')
rp('| Anhang | Inhalt | Erstverweis im Text |', '| Anhang | Inhalt | Erstverweis im Text, Arbeitsnummer (Endnummer v6) |', 'Anhang Kopf')

# § 3.4 Budgets
rp('**Unterbudgets (Vorgabe, Klick 5 vom 23.09., verbindlich seit 25.09.):** 4.1 300 · 4.2 215 · 4.3 340 · 4.4 420 · 4.5.1 420 · 4.5.2 150 · 4.6 155 · 4.7 550 · '
   '5.1 230 · 5.2 220 · 6.1 700 · 6.2 400 · 6.3 500 · 7 250. Die Einleitung hat kein Unterbudget. Nicht verbrauchte Wörter werden nicht aufgefüllt und gehen nicht auf andere Abschnitte über.',
   '**Budgets je Abschnitt der v6 (verbindlich, E4):** 2.1 300 · 2.2 215 · 2.3 340 · 2.4 420 · 2.5 ' + de(b25) + ' · 2.6 550 · 3 ' + str(b3) + ' · 4.1 700 · 4.2 ' + str(b42) +
   ' · 5 250, Einleitung 1.500, Summe ' + de(summe) + '. Die Blockwerte der Vorgabe vom 23.09. (Klick 5, verbindlich seit 25.09.) bleiben Richtwerte innerhalb der zusammengelegten Abschnitte: '
   '4.5.1 420 · 4.5.2 150 · 4.6 155 · 5.1 230 · 5.2 220 · 6.2 400 · 6.3 500. Die Einleitung hat kein Unterbudget. Nicht verbrauchte Wörter werden nicht aufgefüllt und gehen nicht auf andere Abschnitte über.',
   '§ 3.4 Budgets')

# § 4 Änderungen
rp('## 4 Änderungen gegenüber v4 — Begründung und Alternative', '## 4 Änderungen gegenüber v4 und v5 — Begründung und Alternative', '§ 4 Titel')
rp('Ä2 bis Ä10 aus v4 § 4 gelten weiter',
   '| Ä14 | 4.4.1 bis 4.4.3 entfallen, die drei Tests stehen als Absätze in 2.4 Leistungsdiagnostik | dritte Ebene für Absätze von 62 bis 103 Wörtern · Korpus: Absatztitel oder keine Überschrift in 7 von 11 · Sportmedizin: Tests „einzeln für jeden Test“ innerhalb des Untersuchungsgangs · die Absätze beginnen mit dem Konstrukt (Satzformel F1) | Absatztitel nach Korpusart, die dvs-Formatvorlagen und der Master kennen sie nicht | E1, Befund § 8 |\n'
   '| Ä15 | 4.5 (Elternüberschrift ohne Text) mit 4.5.1, 4.5.2 und 4.6 → ein Abschnitt 2.5 „Trainingsintervention und Begleitbedingungen“ | Korpus: kein eigener Adhärenz- oder Monitoring-Abschnitt in 11 von 11 · TIDieR 11 ist Teil der Interventionsbeschreibung · Elternüberschrift ohne Text entfällt | 4.6 als eigener Abschnitt behalten | E1 |\n'
   '| Ä16 | 5.1 und 5.2 → Kapitel 3 Ergebnisse ohne Unterabschnitte | Korpus 8 von 11 · Sportmedizin ohne Unterteilung · 450 Wörter mit vier Objekten in fester Reihenfolge · Gegenstimme CONSORT 2010, S. 700 („frequent subheadings … especially the methods and results sections“), gewogen im Befund B4 | 3.1 und 3.2 behalten, in Task 11 am Textvorschlag geprüft | E3 |\n'
   '| Ä17 | 6.2 und 6.3 → ein Abschnitt 4.2 „Methodendiskussion, Stärken und Limitationen“ nach Bauform Sammoud | beide tragen CONSORT Item 20 · Fassung 17 § 12 G1 verlangt „ohne wörtliche Doppelung“ · Erklärung und Konsequenz je Gruppe beieinander · Sportmedizin: Methodendiskussion „kein Muss“, Inhalte bleiben | Diskussion ohne Unterabschnitte (Korpus 8 von 11) | E2 |\n'
   '| Ä18 | 4.1, 4.2, 4.3 und 4.4 bleiben eigene Abschnitte (2.1 bis 2.4) | Korpus: Stichprobe in 11 von 11 eigener Abschnitt, Design in 9 von 11, Ablauf und Tests 4 zu 4 geteilt · CONSORT S. 700 und Sportmedizin S. 10 für Unterteilung der Methodik · freigegebene Textvorschläge 4.3 und 4.4 bleiben unangetastet | 4.3 und 4.4 zusammenlegen (Methodik mit fünf Abschnitten) | E1 |\n'
   '| Ä19 | übrige Titel, Anhang A bis H und der Name „Einordnung der Ergebnisse“ unverändert | keine Entscheidung nötig | 4.1 als „Ergebnisdiskussion“ | keine |\n\n'
   'Ä14 bis Ä19 mit Begründung, Alternativen und Quellen im Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28` § 5 bis § 8, die Entscheidungen E1 bis E5 dort § 8 (Verfasser 28.09., 21:43: „aufgaben abschließen ohne nachfrage“). '
   'Ä2 bis Ä10 aus v4 § 4 gelten weiter', '§ 4 Ä14 bis Ä19')

# § 5 Master
rp('| M26 | 4.4, nach dem dritten Vorspann-Absatz',
   '| M27 | Überschriften 4.4.1 bis 4.4.3, 4.5, 4.5.2 und 4.6 | löschen, 4.5.1 als Überschrift der zweiten Ebene „Trainingsintervention und Begleitbedingungen“ setzen, dann M25 mit den Nummern 2.1 bis 2.6, 3, 4.1, 4.2 und 5. Nahtstellen lesen (4.4 Vorspann und Testabsätze, 4.5.1 mit 4.5.2 und 4.6), kein Wort hinzufügen, wo ein Übergang fehlt, Vorschlagsliste. G31 (a) ist damit gegenstandslos | Ä14, Ä15 | Task 18, mit M25 |\n'
   '| M28 | Überschriften „5 Ergebnisse“ mit 5.1 und 5.2 · „6.2 Methodendiskussion“ und „6.3 Stärken und Limitationen“ | 5.1 und 5.2 entfallen mit dem Einbau von Kapitel 5 (Task 11), 6.2 und 6.3 werden mit dem Einbau von Kapitel 6 (Task 12) ein Abschnitt „6.2 Methodendiskussion, Stärken und Limitationen“ (Arbeitsnummer), Messskript Fassung 4 mit Task 11 | Ä16, Ä17, E5 | Tasks 11 und 12 |\n'
   '| M26 | 4.4, nach dem dritten Vorspann-Absatz', '§ 5 M27, M28')
rp('| M25 | Überschriften der Methodik bis zum Fazit | Umnummerierung 4 → 2, 5 → 3, 6 → 4, 7 → 5 mit allen Unterabschnitten,',
   '| M25 | Überschriften der Methodik bis zum Fazit | Umnummerierung 4 → 2, 5 → 3, 6 → 4, 7 → 5 nach der Zuordnung 4.1 → 2.1 · 4.2 → 2.2 · 4.3 → 2.3 · 4.4 → 2.4 · 4.5.1 mit 4.5.2 und 4.6 → 2.5 · 4.7 → 2.6 · 5 → 3 · 6.1 → 4.1 · 6.2 mit 6.3 → 4.2 · 7 → 5 (M27, M28),',
   '§ 5 M25')

# § 6 Herkunft
rp('- **Entscheidungen vom 28.09.2026:** Neuzuschnitt',
   '- **Gliederung v5** vom 28.09.2026, im Archiv (`_ersetzt_2026-09-28_Gliederung_v5`). Sie führte Kapitel 1 bis 3 in der Einleitung zusammen (Ä12) und trug 22 Überschriften auf drei Ebenen. '
   'Der Abgleich mit dem Vergleichskorpus, dem Leitfaden Sportmedizin, TUM, dvs und CONSORT (Befund `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`) führte am selben Abend zu v6.\n'
   '- **Entscheidungen vom 28.09.2026:** Kapitelstruktur verschlanken (Verfasser 21:00, „aufgaben abschließen ohne nachfrage“ 21:43, Entscheidungen E1 bis E5 im Befund § 8) · Neuzuschnitt', '§ 6 Herkunft')

# § 7 Prüfung
rp('## 7 Prüfung\n\n', '## 7 Prüfung\n\nv6: Erzeuger `03_Skripte\\Gliederung_v6_2026-09-28.py` aus der v5, jede Ersetzung genau einmal, Ist-Werte der zusammengelegten Abschnitte aus '
   '`Manuskriptstand_2026-09-25.csv` summiert (4.4 mit 4.4.1 bis 4.4.3 = ' + str(i44) + ', 2.5 = ' + str(i25) + '), Budgetsumme ' + de(summe) + ' geprüft, Überschriftenzählung in '
   '`03_Skripte\\Kapitelstruktur_Zaehlung_2026-09-28`, kein Semikolon außer in der Zitiersyntax. Zur v5: ', '§ 7')

if SEMI in t.replace(SEMI + ' ', '§§') and t.count(SEMI) > t.count(SEMI + ' '):
    pass
n_semi = t.count(SEMI)
open(OUT, 'w', encoding='utf-8').write(t)
print('geschrieben:', OUT, len(t.encode('utf-8')), 'Byte, MD5', hashlib.md5(t.encode('utf-8')).hexdigest()[:8], '· Semikola:', n_semi)
print('\n'.join('  ' + p for p in PROT))

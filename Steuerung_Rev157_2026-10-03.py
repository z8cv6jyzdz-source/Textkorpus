# -*- coding: utf-8 -*-
"""
Steuerung_Rev157_2026-10-03.py — Rev.-Block 157 in Teil 0 der Sitzungsnotizen (Taskwechsel des Tasks
„Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ nach Teilschritt 2 b)

Prüft, dass der oberste Block Rev. 156 ist, setzt den Block 157 davor und stellt die Stand-Zeile auf Rev. 157.
Schreibt die neue Fassung und ein Protokoll mit Größen und MD5 vorher und nachher.
Aufruf: python Steuerung_Rev157_2026-10-03.py <Notizen.md> <Ausgabe.md> <Protokoll.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import hashlib

EIN, AUS, PROT = sys.argv[1:4]
alt = open(EIN, encoding='utf-8').read()
STAND_ALT = '**Stand: (Rev. 156 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 157 — siehe Block oben.) Zuvor: (Rev. 156 — siehe Block oben.) Zuvor: '
ANKER = '### ⭐⭐ NEU (Rev. 156, 03.10.2026, 10:00 Sitzungsuhr'
assert alt.count(STAND_ALT) == 1, 'Stand-Zeile nicht auf Rev. 156'
assert alt.count(ANKER) == 1, 'oberster Block ist nicht Rev. 156'
assert '(Rev. 157,' not in alt, 'Rev. 157 schon vorhanden'
pos_teil0 = alt.find('## TEIL 0')
pos_anker = alt.find(ANKER)
assert 0 < pos_teil0 < pos_anker, 'Rev. 156 steht nicht unter Teil 0'
erster_block = alt.find('### ⭐⭐ NEU (Rev.', pos_teil0)
assert erster_block == pos_anker, 'Rev. 156 ist nicht der erste Block unter Teil 0'

BLOCK = '''### ⭐⭐ NEU (Rev. 157, 03.10.2026, 11:45 Sitzungsuhr, Auftrag 03.10., 10:09 mit dem Startprompt aus Fortsetzungsübergabe 1 § 0): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Teilschritt 2 (b) abgeschlossen und gesichert, Taskwechsel nach erneuter automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Teilschritt 2 (c), kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung1_2026-10-03.md` § 0: Teilschritt 2 (b), den Prüfkatalog des Befunds § 6.5 Punkt für Punkt, die Bauregeln K1 bis K10 und die Projektregeln P1 bis P12 einzeln am Textstand von Kapitel 5 prüfen (erfüllt, teilweise, nicht erfüllt oder bewusst anders, mit Fundstelle und Registerzeile), dazu jede Aussage des Befunds, die Kapitel 5 berührt, als Teiltabelle 2b per Skript und als § 3.2 des Abgleichbefunds, mit den Prüfpunkten aus Fortsetzung 1 § 5 Nr. 4. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.

**Ergebnis:** (1) **Teilschritt 2 (b):** `pruef_2b.py` prüft Prüfkatalog § 6.5 Nr. 1 bis 10, K1 bis K10 mit dem Code nach dem Codebuch, P1 bis P12 gegen ihre Fundstelle und jede weitere Aussage des Befunds, die Kapitel 5 berührt. Handurteile sind per Prüfbedingung an die Messung gebunden, 110 angeführte Stellen am Quelltext gefunden, Lauf im Spiegel und aus dem gestagten Ordner bytegleich. Teiltabelle 2b (Abgleichbefund § 3.2, 47 Zeilen): erfüllt 32, davon gegenstandslos 2, teilweise 9, bewusst anders 6, nicht erfüllt 0, mit neuer Spalte Maßstab (Korpus 19, Fundstelle 22, beide 6). Ohne Entscheidung abweichend und für Schritt 3 vorgemerkt: A5 S3 (unadjustiert) vor dem Modellergebnis · der Fall einmal für alle drei Zielgrößen statt je Zielgröße im Block · A4 S2 mit der Folge Sprint, Sprung, Richtungswechsel · Schluss mit dem Z1-Satz A6 S4, letzter Befundsatz A5 S10 ohne Klammer · Bezugsmenge der neun Spieler in A3 S3, berührt 6.1 A6 S2 (Schwere B) · die acht Meldungen zu vollständig durchgeführten Einheiten nur rechnerisch · A6 S3 nicht wörtlich „geprüft und nicht verworfen“ · Satzenden A5 S1 und A6 S2 · eine Aussage je Satz in A6 S4 (vorangestellte Bedingung), A2 S1, A3 S3 und A5 S3 (angehängte zweite Aussage). Bewusst anders und gedeckt: Umfang und Gewicht, Z2 im Rahmen, Objektfolge und Stellung von Abb. 2 und A5 S11, Ausgangslage ohne Test, Flussdiagramm im Ergebnisteil, P4 und P7 bis P10, Schlusslogik und Intervall im Satz, Folge des Orientierungszugs nach Plan. (2) **Zweitprüfung** der ersten Fassung durch einen unabhängigen Subagenten: A 2 · B 9 · C 10, alle eingearbeitet (A: Stellung der Umsetzung bei Klusemann, Status der Zeile zum Modellergebnis), seine Reproduktion bytegleich.

**Eigene Korrekturen in dieser Sitzung:** (1) Die Prüfung der Komma-Ausnahme scheiterte an Dezimalkommas, ersetzt durch die Zahl der Kommas mit Leerzeichen außerhalb der Klammern. (2) Ein angeführtes Zitat aus Hilska 3.3 trug ein Semikolon in die Belegdatei, in zwei Zitate geteilt. (3) U9 als Registerzeile zum Rahmen und „Registerzeile 9 Nr. 2“ statt 9c beim Antragskriterium, berichtigt. (4) Suchausdrücke trafen Wortteile („überstieg“, „Mittel“) und Satzenden mit Klammer, vor der Ablage berichtigt.

**Stand der Dateien:** Neu: in `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` die Dateien `pruef_2b.py` (85.007 Byte, MD5 `d7b83c09…`), `pruef_2b.txt`, `teiltabelle_2b.csv`, `teiltabelle_2b.md` und `zweitpruefung_2b.md`, der Ordner hat jetzt 35 Dateien · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md` (15.661 Byte, MD5 `b824c5fa…`) mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev157_2026-10-03.py` mit `.txt` · Projektkopie `claude/Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md` (Projektspeicher danach rechnerisch 1.985.548 von 2.000.000 Byte). Geändert: `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (91.376 Byte, MD5 `553ace3f…`, § 0, § 3.2, § 5), der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung · `LIESMICH.md` des Arbeitsordners (Abschnitt Schritt 2 b, 5.614 Byte) · diese Notizen (Rev. 157 auf Rev. 156), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Unverändert: Master (40.331 Byte, Dateizeit 02.10., 19:18), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 156 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ (Rev. 155), Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 2 ab Teilschritt 2 (c): Textbausteine des Befunds § 5.1 und Sequenzen § 5.2 je Satz von Kapitel 5, Korpusmuster und Projektregel getrennt, dazu jede Funktion ohne Muster (Teiltabelle 2c, Abgleichbefund § 3.3), dann 2 (d) Nachzählung an der Anlage und 2 (e) Anschluss an Kapitel 4, 6.1 und weitere Teile, danach Schritt 3 mit der Klickfrage zu den Potenzialen.

'''
neu = alt.replace(STAND_ALT, STAND_NEU, 1)
pos = neu.find(ANKER)
neu = neu[:pos] + BLOCK + neu[pos:]
assert chr(59) not in BLOCK, 'Semikolon im Block'
open(AUS, 'w', encoding='utf-8', newline='').write(neu)


def md5(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()


z = ['Steuerung Rev. 157 (03.10.2026)',
     'vorher: ' + str(len(alt.encode('utf-8'))) + ' Byte, MD5 ' + md5(alt),
     'nachher: ' + str(len(neu.encode('utf-8'))) + ' Byte, MD5 ' + md5(neu),
     'Block: ' + str(len(BLOCK.encode('utf-8'))) + ' Byte, eingesetzt vor Rev. 156, Stand-Zeile auf Rev. 157',
     'Prüfungen: Stand-Zeile auf Rev. 156, oberster Block Rev. 156, Rev. 157 nicht vorhanden, kein Semikolon im Block']
open(PROT, 'w', encoding='utf-8').write('\n'.join(z) + '\n')
print('\n'.join(z))

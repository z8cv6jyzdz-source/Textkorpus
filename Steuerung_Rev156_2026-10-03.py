# -*- coding: utf-8 -*-
"""
Steuerung_Rev156_2026-10-03.py — Rev.-Block 156 in Teil 0 der Sitzungsnotizen (Taskwechsel des Tasks
„Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ nach Teilschritt 2 a)

Prüft, dass der oberste Block Rev. 155 ist, setzt den Block 156 davor und stellt die Stand-Zeile auf Rev. 156.
Schreibt die neue Fassung und ein Protokoll mit Größen und MD5 vorher und nachher.
Aufruf: python Steuerung_Rev156_2026-10-03.py <Notizen.md> <Ausgabe.md> <Protokoll.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import hashlib

EIN, AUS, PROT = sys.argv[1:4]
alt = open(EIN, encoding='utf-8').read()
STAND_ALT = '**Stand: (Rev. 155 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 156 — siehe Block oben.) Zuvor: (Rev. 155 — siehe Block oben.) Zuvor: '
ANKER = '### ⭐⭐ NEU (Rev. 155, 03.10.2026, 09:05 Sitzungsuhr'
assert alt.count(STAND_ALT) == 1, 'Stand-Zeile nicht auf Rev. 155'
assert alt.count(ANKER) == 1, 'oberster Block ist nicht Rev. 155'
assert '(Rev. 156,' not in alt, 'Rev. 156 schon vorhanden'
pos_teil0 = alt.find('## TEIL 0')
pos_anker = alt.find(ANKER)
assert 0 < pos_teil0 < pos_anker, 'Rev. 155 steht nicht unter Teil 0'

BLOCK = '''### ⭐⭐ NEU (Rev. 156, 03.10.2026, 10:00 Sitzungsuhr, Auftrag 03.10., 08:04 mit dem Startprompt aus Übergabe § 0 vom 02.10.): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Schritt 1 und Teilschritt 2 (a) abgeschlossen und gesichert, Klick zum Register, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Teilschritt 2 (b), kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md` § 0: Kapitel 5 im Master gründlich mit allen Inhalten des Befunds `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02` abgleichen und gegenprüfen, die Unterschiede kompakt als Potenziale herausarbeiten und per Klick freigeben lassen, dann Absatz für Absatz überarbeiten. Streng schrittweise, jeder Schritt mit gesicherter Datei und Meldung, Budget 450 Wörter, Einbau nur auf ausdrückliche Anweisung.

**Ergebnis:** (1) **Schritt 1 (Textstand):** Master unverändert seit Rev. 152 (40.331 Byte, MD5 `2fda2144…`, keine comments.xml), Kapitel 5 zeichengleich mit `03_Skripte\\Textvorschlag_5_2026-09-30.json`, 450 Wörter in 29 Sätzen (Median 15,0, längster Satz 28), Messskript Fassung 4 reproduziert. Das Register der Übergabe (§ 4) hat ein unabhängiger Subagent an den Fundstellen und am Textstand geprüft: keine Verletzung, Kurzfassungen berichtigt, neun fehlende Entscheidungen und vier Präzisierungen als dokumentiert aufgenommen. 24 Sätze von 6.1 und die Platzhalter H2 bis H5 nehmen Kapitel 5 auf (Abgleichbefund § 1.4). Klick zu U8 und U10 „Plan und Freigabe (Empfehlung)“, geführt als Registerzeile 16: im Gruppenvergleich kein t- oder F-Wert im Satz, Voraussetzungen als ein Satz zur verworfenen Prüfung und ein Sammelsatz, F17 § 5a Nr. 3 und Raster 5.2.3 für Kapitel 5 überholt, Vormerkung G37 (p). (2) **Teilschritt 2 (a):** Ersteller und ein blinder Subagent codierten die 29 Sätze nach Codebuch Fassung 2 ohne die Anwendungshinweise: Primärcode 27 von 29 (κ 0,922), von den Hinweisen erfasste Sätze 14 von 16, übrige 13 von 13, zg und Deutung 29 von 29. Konsens nach dem Codebuch (A5 S6 und S8 beide B1), die Fassung nach den Hinweisen weicht nur über H2 ab (sechs Sätze). Messung gegen Befund § 2 bis § 4 (Teiltabelle 2a, 42 Zeilen): wie Korpus Rahmen vor dem ersten Befund, Objektsatz am Anfang, Tempus, keine Belege, keine Deutung, Nullbefunde ausdrücklich, Zielgrößenfolge der Befundsätze. Vorgemerkt für 2b: Wortanteil der Befunde 22,4 % unter der Spanne des Kerns (26,4 bis 100 %) bei einem Rahmen von 62,2 % (höher nur Beato) · letzter Satz kein Befundsatz · A4 S2 mit der Folge Sprint, Sprung, Richtungswechsel · Tab. H3 als Subjekt in A1 S3.

**Eigene Korrekturen in dieser Sitzung:** (1) Die Prüfung der Satzenden in `textstand.py` meldete zunächst 14 Sätze, weil sie die schließende Klammer abschnitt, vor der Ablage berichtigt (zwei Sätze, A5 S1 und A6 S2). (2) Codierer A war bei A5 S6 und A5 S8 uneinheitlich, der Konsens entscheidet beide nach der Klarstellung B4. (3) Der Kernmedian „vor dem ersten Befund“ wird wie in `textbausteine.py` aus je Studie gerundeten Werten gerechnet (22,3 statt 22,4 %). (4) Eine Rückschreibung der Fortsetzungsübergabe aus einem schon benutzten Ausgabepfad meldete „written“ und hatte die Vorfassung geschrieben (16.433 statt 16.464 Byte), wie am 28.09. (F17 Abschnitt F). Erkannt am MD5-Vergleich, aus einem frischen Pfad wiederholt und bestätigt.

**Stand der Dateien:** Neu: `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` (30 Dateien, davon 4 in `blind\\` und 2 in `quellen\\`, mit `LIESMICH.md`) · `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (51.248 Byte, MD5 `a9b0ce2f…`, § 0 bis § 3.1, § 5, Anhang A) · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung1_2026-10-03.md` (16.464 Byte, MD5 `7d8a86e1…`) mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev156_2026-10-03.py` mit `.txt` · Projektkopie `claude/Uebergabe_Abgleich_Ergebnisse_Fortsetzung1_2026-10-03.md` (Projektspeicher danach 1.969.887 von 2.000.000 Byte). Der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung. Geändert: diese Notizen (Rev. 156 auf Rev. 155), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Unverändert: Master, Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung1_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 155 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ (Rev. 155), Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 1 ab Teilschritt 2 (b): Prüfkatalog des Befunds § 6.5, Bauregeln K1 bis K10 und Projektregeln P1 bis P12 einzeln am Textstand (Teiltabelle 2b, Abgleichbefund § 3.2), dann 2 (c) Textbausteine und Sequenzen, 2 (d) Nachzählung an der Anlage, 2 (e) Anschluss an Kapitel 4, 6.1 und weitere Teile, danach Schritt 3 mit der Klickfrage zu den Potenzialen.

'''
neu = alt.replace(STAND_ALT, STAND_NEU, 1)
pos = neu.find(ANKER)
neu = neu[:pos] + BLOCK + neu[pos:]
assert chr(59) not in BLOCK, 'Semikolon im Block'
open(AUS, 'w', encoding='utf-8', newline='').write(neu)
md5 = lambda t: hashlib.md5(t.encode('utf-8')).hexdigest()
z = ['Steuerung Rev. 156 (03.10.2026)',
     f'vorher: {len(alt.encode("utf-8"))} Byte, MD5 {md5(alt)}',
     f'nachher: {len(neu.encode("utf-8"))} Byte, MD5 {md5(neu)}',
     f'Block: {len(BLOCK.encode("utf-8"))} Byte, eingesetzt vor Rev. 155, Stand-Zeile auf Rev. 156',
     'Prüfungen: Stand-Zeile auf Rev. 155, oberster Block Rev. 155, Rev. 156 nicht vorhanden, kein Semikolon im Block']
open(PROT, 'w', encoding='utf-8').write('\n'.join(z) + '\n')
print('\n'.join(z))

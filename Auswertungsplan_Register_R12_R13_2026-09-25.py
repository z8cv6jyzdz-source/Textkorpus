# -*- coding: utf-8 -*-
"""
Auswertungsplan_Register_R12_R13_2026-09-25.py — Register § 5.10 des Auswertungsplans um R12 und R13 ergänzen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Schritt 2.3 (Register)

Zweck: Zwei Verfasserentscheidungen vom 25.09.2026 als nachträgliche Festlegungen in
02_Befunde\\Auswertungsplan_2026-09-12.md eintragen: R12 (Handprobe 6.3 als Excel-Formelprobe) und
R13 (Nachtrag 3 zur Spezifikation), Kopfkasten und Einleitung von § 5.10 nachziehen. Jede Textstelle
wird genau einmal ersetzt, sonst bricht das Skript ab. Die Zahlen von R12 stammen aus der Rechenprobe
Handprobe_Pruefung_2026-09-25.txt und werden von dort gelesen.
Aufruf: python Auswertungsplan_Register_R12_R13_2026-09-25.py <Auswertungsplan.md> <Handprobe_Pruefung.txt>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

MD, PRUEF = sys.argv[1], sys.argv[2]
s = open(MD, encoding='utf-8').read()
pr = open(PRUEF, encoding='utf-8').read()
n_stimmt = re.search(r'Kennwerte mit Urteil „stimmt“: (\d+) von (\d+)', pr)
n_zusatz = re.search(r'Zusatzprüfungen bestanden: (\d+) von (\d+)', pr)
maxrel = re.search(r'Größte relative Abweichung einer Formel gegen die berichtete Rechnung: (\S+)', pr).group(1)
urteil = re.search(r'Gesamturteil der Rechenprobe: (\w+)', pr).group(1)
if urteil != 'bestanden':
    raise SystemExit('Rechenprobe nicht bestanden, Register nicht ergänzt')


def ersetze(alt, neu):
    global s
    if s.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:70])
    s = s.replace(alt, neu)


ersetze('> **Nachtrag 25.09.2026 (Phase 6):** Das Register § 5.10 trägt die Zeilen R9 bis R11: Festlegungen aus der Blindrechnung (R9), Gegenprobe als neue Fassung der Python-Kette mit bestandenem Abgleich je Kennung (R10) und eine Korrektur mit altem und neuem Ergebnis zur Berechnung des Reifestatus (R11). Nachweise: `02_Befunde\\Abgleichprotokoll_2026-09-25`, `Durchsichtsprotokoll_2026-09-25`, `Plausibilitaetsprotokoll_2026-09-25`.',
        '> **Nachtrag 25.09.2026 (Phase 6):** Das Register § 5.10 trägt die Zeilen R9 bis R13: Festlegungen aus der Blindrechnung (R9), Gegenprobe als neue Fassung der Python-Kette mit bestandenem Abgleich je Kennung (R10), eine Korrektur mit altem und neuem Ergebnis zur Berechnung des Reifestatus (R11), die Handprobe 6.3 als Excel-Formelprobe (R12) und Nachtrag 3 zur Spezifikation (R13). Nachweise: `02_Befunde\\Abgleichprotokoll_2026-09-25`, `Durchsichtsprotokoll_2026-09-25`, `Plausibilitaetsprotokoll_2026-09-25`, `03_Skripte\\Handprobe_Pruefung_2026-09-25.txt`, `02_Befunde\\Blindpruefung_Spezifikation_2026-09-24` (dritter Lauf).')
ersetze('Die Einträge R1 bis R8 hat der Verfasser am 24.09.2026 entschieden, R9 bis R11 kamen am 25.09.2026 aus der Blindrechnung und dem Abgleich (Phase 6), alle ohne Rücksprache mit dem Betreuer.',
        'Die Einträge R1 bis R8 hat der Verfasser am 24.09.2026 entschieden, R9 bis R13 kamen am 25.09.2026 aus der Blindrechnung, dem Abgleich, der Handprobe und der Code-Durchsicht (Phase 6), alle ohne Rücksprache mit dem Betreuer.')
R12 = ('| R12 | Handprobe 6.3 als Excel-Formelprobe (Verfasser 25.09.2026): Die 34 vorab bestimmten Kennwerte werden nicht von Hand nachgerechnet, sondern in `04_Uebergaben\\Handprobe_2026-09-25.xlsx` (Fassung 2, Erzeuger `03_Skripte\\Handprobe_2026-09-25.py`) mit Excel-Formeln allein aus den Eingangsblättern des Datenstands und der Anlagen berechnet, mit Auslöseprüfung, Ausfallkategorien, Interpolation der Koeffizienten, Analysesets und LINEST für die ANCOVA. Excel ist damit eine dritte Implementierung der 34 Kennwerte neben R und Python. Dazu der Vergleich von elf Zwischengrößen je Spieler mit der berichteten Rechnung und vier Zusatzprüfungen. Rechenprobe mit LibreOffice Calc (`03_Skripte\\Handprobe_Pruefung_2026-09-25.py` und `.txt`): %s von %s Kennwerte stimmen, Zusatzprüfungen %s von %s, größte relative Abweichung %s. Der Verfasser prüft Formeln und Urteile in Excel und trägt das Ergebnis in Zelle B4 ein | ergänzt Auswertungsverfahren 6.3 (Handprobe des Verfassers in Excel) | Eine Formelprobe ist nachvollziehbar und wiederholbar und prüft die Regeln der Spezifikation unabhängig von beiden Skriptsprachen. Von Hand eingetippte Werte wären weder prüfbar noch von der Rechnung unabhängig | 4.7 (Daten- und Rechenprüfung) |'
       % (n_stimmt.group(1), n_stimmt.group(2), n_zusatz.group(1), n_zusatz.group(2), maxrel))
R13 = ('| R13 | Nachtrag 3 zur Spezifikation (Teil F.8, 25.09.2026, N5.1 bis N5.4): Vorrang des Grunds „Eingang fehlt“ in S05 · Median und Mittel der Adhärenz über die zugeteilten Spieler, N4.3 an Regel 7 und die Kennungsanlage angeglichen · Rangkriterium der Designmatrix (QR-Zerlegung, Toleranz 1e-7, spaltenskaliert, oder gleichwertig) · Zusatz `_Python` in den Grafiknamen der Gegenprobe. Blindprüfung 2.2 im dritten Lauf bestanden | ergänzt R9 (Klarstellungen der Spezifikation nach dem Blindlauf) | Code-Durchsicht 6.2 (`Durchsichtsprotokoll_2026-09-25`, Teil C). Beide Implementierungen hatten die vier Stellen gleich gelesen, kein Wert der Ergebnisdatei ändert sich | 4.7, Anhang G |')
marker = '\n\n*Tab. 6.* In der ersten Rechnung enthalten, künftig nicht gerechnet und nicht berichtet'
ersetze(marker, '\n' + R12 + '\n' + R13 + marker)
with open(MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('Register ergänzt: R12 und R13, Kopfkasten und § 5.10 nachgezogen')

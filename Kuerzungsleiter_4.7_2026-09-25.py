# -*- coding: utf-8 -*-
"""
Kuerzungsleiter_4.7_2026-09-25.py — Stufen des Textvorschlags 4.7 aus der Fassung A erzeugen und messen
Jede K-Stelle wird genau einmal ersetzt, sonst Abbruch. Ohne Semikolon.
Aufruf: python Kuerzungsleiter_4.7_2026-09-25.py   (liest Textvorschlag_4.7_2026-09-25_A.txt, schreibt Textvorschlag_4.7_2026-09-25_Empf.txt und Textvorschlag_4.7_2026-09-25_Kurz.txt
und Kuerzungsleiter_4.7_2026-09-25.txt mit den gemessenen Ersparnissen)
Fassung: 2026-09-25, zweite Fassung (nach der Zweitprüfung).
"""
import re

src = open('Textvorschlag_4.7_2026-09-25_A.txt', encoding='utf-8').read()
ABS7_ALT = ('Der eingefrorene Datenstand war die einzige Datenquelle. Die Koeffizienten des Reifestatus stammen aus der Originalpublikation (Khamis & Roche, 1994), das Erratum von 1995 wurde nicht eingesehen. Der Reifestatus wurde nach der Spezifikation mit interpolierten Koeffizienten neu berechnet, nachdem die erste Auswertung gerundete Werte einer Tabellenspalte verwendet hatte. Alle Rechenschritte standen vor der berichteten Rechnung in einer Spezifikation fest, die die Untersuchungsleitung ohne unabhängige Methodenprüfung freigab. Rückfragen wurden vor der Rechnung dokumentiert beantwortet, spätere Klarstellungen änderten keinen Wert. Die Skripte der berichteten Rechnung erstellte ein KI-Sprachmodell (Claude, Anthropic) allein nach der Spezifikation und ohne Kenntnis der ersten Auswertung. Eine zweite, ebenfalls KI-gestützt erstellte Implementierung in Python diente als Gegenprobe, der Abgleich je Kennwert blieb innerhalb der vorab festgelegten Toleranzen. Vorab bestimmte Kennwerte wurden zusätzlich in Excel per Formel nachgerechnet. Poweranalyse, Skripte und Diagramme der Voraussetzungsprüfung stehen in Anhang G.')
ABS7_NEU = ('Der eingefrorene Datenstand war die einzige Datenquelle. Alle Rechenschritte standen vor der berichteten Rechnung in einer Spezifikation fest, die die Untersuchungsleitung ohne unabhängige Methodenprüfung freigab. Die Skripte erstellte ein KI-Sprachmodell (Claude, Anthropic) allein nach der Spezifikation und ohne Kenntnis der ersten Auswertung. Eine zweite KI-gestützte Implementierung in Python und eine Formelprobe in Excel dienten als Gegenproben, der Abgleich je Kennwert blieb innerhalb der vorab festgelegten Toleranzen. Prüfprotokolle, Poweranalyse, Skripte und Diagramme der Voraussetzungsprüfung stehen in Anhang G.')
K = {
 'K1': ('Zugeteilt wurde auf Vereinsebene, analysiert auf Spielerebene, eine Varianzkomponente für den Verein wurde bei drei Vereinen nicht modelliert.', '', 'Analyseeinheit (F14 § 4, TREND-Satz) nach 6.2 G2'),
 'K2': ('Die Hauptanalyse schätzt damit die Wirkung des Programmangebots.', '', 'Sprachregelung, trägt 6.1 Eröffnung'),
 'K3': ('Nicht enthalten waren Spieler ohne Abschlusstestung und ein Spieler ohne Reifestatus. Geringe Adhärenz und die fehlende Auswählbarkeit eines Spielers im Fragebogen führten nicht zum Ausschluss aus der Hauptanalyse.', '', 'Box-6-Klassen (4.7.3 P/E), stehen in Abb. 1'),
 'K4': ('Die Nenner werden je Zielgröße und Gruppe berichtet.', '', 'CONSORT 16 Regel, Nenner in Tab. 3'),
 'K5': ('Die Koeffizienten des Reifestatus stammen aus der Originalpublikation (Khamis & Roche, 1994), das Erratum von 1995 wurde nicht eingesehen.', '', 'R14 nach 4.3 (Methode des Reifestatus), Vormerkung'),
 'K6': ('Vorab bestimmte Kennwerte wurden zusätzlich in Excel per Formel nachgerechnet.', '', 'R12 Handprobe, in K12 als Halbsatz erhalten'),
 'K7': ('Es beruht auf der Perzentilmethode mit 10 000 Ziehungen ganzer Spieler, geschichtet nach Gruppe.', '', 'Bootstrap-Einzelheiten nach Anhang G'),
 'K8': ('Ergebnis ist die kleinste nachweisbare Effektstärke je Zielgröße als standardisierte Differenz d.', '', 'MDES-Definition, steht in 6.2 G1 und Anhang G'),
 'K9': ('Letztere fallen in der Interventionsgruppe weitgehend mit der Vereinszugehörigkeit zusammen.', '', 'Konfundierung der Familiarisierung nach 6.3 G7'),
 'K10': ('Die Zahl der Spieler je Mindestdosis zeigt Tab. H5.', '', 'Tab. H5 in 5.1 einführen (Adhärenz), Vormerkung'),
 'K11': ('Eingaben waren der F-Test des Gruppenterms bei zwei Gruppen und zwei Kovariaten (Freiheitsgrade 1 und N − 4), das n des Analysesets, α = 0,05 und Power 0,80, ohne Kovariatengewinn.', 'Eingaben waren das n des Analysesets, α = 0,05 und Power 0,80, ohne Kovariatengewinn, die Einzelheiten stehen in Anhang G.', 'Berichtsangaben der Poweranalyse (4.7.8) nach Anhang G'),
 'K12': (ABS7_ALT, ABS7_NEU, 'Daten- und Rechenprüfung ausgelagert: R9, R11, R13 und R14 nach Anhang G, Tab. H6 und 4.3'),
 'K13': ('Zusätzlich wurden die Prä-Werte vorab auf einen gruppengleichen Zusammenhang mit dem Reifestatus geprüft und die Veränderungen je Zahl der Familiarisierungstermine beschreibend verglichen.', '', 'Vorab-Prüfung (K-07.2) und Familiarisierung Variante a (K-08.11) in die Anmerkung zu Tab. H4'),
 'K14': ('Dazu wurde die Power bei den vorab aus der Literatur entnommenen Effektstärken berechnet, für den 10-m-Sprint nur diese.', '', 'Power bei Vorab-Erwartungen (K-09), Methode für 6.2 G1'),
}
EMPF = ['K5', 'K7', 'K8', 'K10', 'K12', 'K13']


def wc(t):
    t = '\n'.join(z for z in t.split('\n') if not z.startswith('#'))
    return len(t.split())


def stufe(keys):
    t = src
    reihe = (['K12'] if 'K12' in keys else []) + [k for k in keys if k != 'K12']
    for k in reihe:
        if k in ('K5', 'K6') and 'K12' in keys:
            continue
        a, b, _ = K[k]
        if t.count(a) != 1:
            raise SystemExit('K-Stelle nicht genau einmal: ' + k)
        t = t.replace(a, b)
    t = re.sub(r'  +', ' ', t)
    t = re.sub(r' \n', '\n', t)
    return t


base = wc(src)
zeilen = ['Fassung A: %d Wörter' % base]
for k, (a, b, grund) in K.items():
    zeilen.append('%s: −%d · %s' % (k, base - wc(stufe([k])), grund))
e = stufe(EMPF)
alle = [k for k in K if k != 'K6']
v = stufe(alle)
open('Textvorschlag_4.7_2026-09-25_Empf.txt', 'w', encoding='utf-8').write(e)
open('Textvorschlag_4.7_2026-09-25_Kurz.txt', 'w', encoding='utf-8').write(v)
zeilen.append('Empfehlung (A ohne %s): %d' % (', '.join(EMPF), wc(e)))
zeilen.append('Kurz (A ohne K1 bis K14, K6 in K12 enthalten): %d' % wc(v))
open('Kuerzungsleiter_4.7_2026-09-25.txt', 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
print('\n'.join(zeilen))

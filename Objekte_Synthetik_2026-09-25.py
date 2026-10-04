# -*- coding: utf-8 -*-
"""
Objekte_Synthetik_2026-09-25.py — synthetische Ergebnisdatei im Format der Spezifikation G.1 für die Probe der Objektskripte
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Schritt 7.2 (Objektskripte vorab mit synthetischen Daten prüfen), Maßnahme L19

Zweck: Aus der Kennungsliste und dem Muster fehlender Werte einer Ergebnisdatei eine Datei mit
denselben Kennungen, Einheiten, Gründen und Skriptnamen erzeugen, deren Werte zufällig sind
(fester Startwert). Anzahlen und Merkmale bleiben ganzzahlig, p-Werte liegen zwischen 0 und 1,
Messgrößen in plausiblen Spannen. Die Datei enthält kein Studienergebnis und dient nur der
Probe, ob Objekte_2026-09-25.R alle Zellen, Fehlpfade und Grafiken erzeugt.
Aufruf: python Objekte_Synthetik_2026-09-25.py <Ergebnisdatei.csv> <Ziel_synthetisch.csv>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import csv
import random

QUELLE, ZIEL = sys.argv[1], sys.argv[2]
rng = random.Random(20260925)
ZAEHL = {'N', 'NIG', 'NKG', 'NTE', 'NSB', 'DFTE', 'DF', 'DF1', 'DF2', 'DFG', 'NZEIL', 'NMELD', 'NKORR', 'NDUBL', 'NSAMM', 'NSTAT', 'NZUG', 'SUMME',
         'NMELDSP', 'UE', 'UESP', 'FLZUG', 'FLPRE', 'FLAUSG', 'FLNANG', 'FLITT', 'FLOPRE', 'FLOPOST', 'FLOPAH', 'B6NE', 'B6NEKM', 'B6IF', 'B6FK', 'B6NA',
         'K', 'NTOT', 'BNGUELT', 'BNVERW', 'NPAH', 'NFAM1', 'NFAM2', 'NFAMNA', 'NKAT', 'NGUELT', 'NAUSL', 'OVPREIG', 'OVPREKG', 'OVPAHIG', 'OVPAHKG',
         'DFINT', 'DFCINT', 'UDDF', 'BFDF1', 'BFDF2', 'ADH', 'DIST', 'WOCAP', 'MED', 'MITT'}
ZAEHL |= {'V%02d' % i for i in range(13)} | {'GE%02d' % i for i in range(1, 13)}
MERKMAL = {'MITGL', 'INF', 'SIG', 'H0REJ', 'NTEST', 'FLEINZ', 'SWVERW', 'BFVERW', 'VERW'}
PWERT = {'P', 'SWP', 'BFP', 'PINT', 'PCINT', 'UDP', 'POW', 'RATE', 'ANT', 'ANTTN', 'ANTW', 'R2'}

with open(QUELLE, encoding='utf-8', newline='') as f:
    zeilen = list(csv.DictReader(f))
aus = []
for r in zeilen:
    k = r['Kennung']
    schritt, groesse, ziel, zeit, menge, variante = k.split('.')
    if r['Wert'] == '':
        v = ''
    elif groesse in MERKMAL:
        v = str(rng.randint(0, 1)) if groesse != 'NTEST' else '3'
    elif groesse in ZAEHL:
        v = str(rng.randint(0, 30)) if groesse not in ('MED', 'MITT') else '%.6f' % rng.uniform(0, 12)
    elif groesse in PWERT:
        v = '%.12g' % rng.uniform(0.0005, 0.999)
    elif r['Einheit'] == 's':
        v = '%.12g' % rng.uniform(-0.3 if groesse in ('B1', 'KIU', 'KIO', 'UD', 'UDKIU', 'UDKIO', 'BKIU', 'BKIO', 'DMEAN', 'DIFF', 'M') and zeit == 'DIFF' or groesse in ('B1', 'KIU', 'KIO', 'UD', 'UDKIU', 'UDKIO', 'BKIU', 'BKIO', 'DMEAN', 'DIFF', 'B0', 'B3', 'BINT', 'CINT') else 0.5, 5.5)
    elif r['Einheit'] == 'cm':
        v = '%.12g' % rng.uniform(-15 if groesse in ('B1', 'KIU', 'KIO', 'UD', 'UDKIU', 'UDKIO', 'BKIU', 'BKIO', 'DMEAN', 'DIFF', 'B0', 'B3', 'BINT', 'CINT') or zeit == 'DIFF' else 150, 260)
    elif r['Einheit'] == '%':
        v = '%.12g' % rng.uniform(85, 98)
    elif r['Einheit'] == 'AU':
        v = '%.12g' % rng.uniform(40, 320)
    elif r['Einheit'] == 'Jahre':
        v = '%.12g' % rng.uniform(13.5, 15.5)
    elif r['Einheit'] == 'kg':
        v = '%.12g' % rng.uniform(40, 80)
    elif r['Einheit'] == 'in':
        v = '%.12g' % rng.uniform(60, 80)
    else:
        v = '%.12g' % rng.uniform(-2, 2)
    aus.append({'Kennung': k, 'Wert': v, 'Einheit': r['Einheit'], 'Grund': r['Grund'], 'Skript': r['Skript']})
with open(ZIEL, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['Kennung', 'Wert', 'Einheit', 'Grund', 'Skript'])
    w.writeheader()
    for r in aus:
        w.writerow(r)
print('geschrieben:', ZIEL, '· Kennungen:', len(aus), '· fehlend wie in der Vorlage:', sum(1 for r in aus if r['Wert'] == ''))

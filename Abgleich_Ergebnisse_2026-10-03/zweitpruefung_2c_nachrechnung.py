# -*- coding: utf-8 -*-
"""
nachrechnung.py — unabhängige Nachrechnung zur Zweitprüfung der Teiltabelle 2c (03.10.2026).

Liest nur: W (Teiltabelle 2c, Teiltabelle 2b, Codes, Merkmale, Textstand, Master-Sätze, Register) und C (Anlage
…_Saetze.csv, textbausteine.json, Befund, Fassung 17, Stilprofil, Raster, Plan, Textvorschlag 5, Umfangsdokument).
Schreibt nur nachrechnung.txt in den Ordner dieses Skripts. Ohne Semikolon im Skript (chr(59)), in der Ausgabe wird
chr(59) aus Korpustexten als ‹SK› wiedergegeben.
"""
import os
import re
import csv
import json
import hashlib
from collections import Counter, OrderedDict

SK = chr(59)
HIER = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.dirname(HIER), 'w2c')
C = '/mnt/user-data/uploads/Bachelorarbeit/Claude'
OUT = []


def aus(*t):
    OUT.append(' '.join(str(x) for x in t).replace(SK, ' ‹SK› '))


def lies(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def md5(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


P = OrderedDict([
    ('W/teiltabelle_2c.md', os.path.join(W, 'teiltabelle_2c.md')),
    ('W/teiltabelle_2c.csv', os.path.join(W, 'teiltabelle_2c.csv')),
    ('W/bausteine_2c.py', os.path.join(W, 'bausteine_2c.py')),
    ('W/bausteine_2c.txt', os.path.join(W, 'bausteine_2c.txt')),
    ('W/textstand.json', os.path.join(W, 'textstand.json')),
    ('W/textstand_saetze.md', os.path.join(W, 'textstand_saetze.md')),
    ('W/konsens_2a.csv', os.path.join(W, 'konsens_2a.csv')),
    ('W/eigen.json', os.path.join(W, 'eigen.json')),
    ('W/eigen.txt', os.path.join(W, 'eigen.txt')),
    ('W/abgleich_2a.json', os.path.join(W, 'abgleich_2a.json')),
    ('W/master_saetze.json', os.path.join(W, 'master_saetze.json')),
    ('W/master_saetze.md', os.path.join(W, 'master_saetze.md')),
    ('W/teiltabelle_2b.csv', os.path.join(W, 'teiltabelle_2b.csv')),
    ('W/teiltabelle_2b.md', os.path.join(W, 'teiltabelle_2b.md')),
    ('W/register_pruefung.md', os.path.join(W, 'register_pruefung.md')),
    ('W/zweitpruefung_2b.md', os.path.join(W, 'zweitpruefung_2b.md')),
    ('C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md', os.path.join(C, '02_Befunde', 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md')),
    ('C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv', os.path.join(C, '02_Befunde', 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv')),
    ('C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.json', os.path.join(C, '03_Skripte', 'Argumentationsstruktur_Ergebnisteile_2026-10-02', 'textbausteine.json')),
    ('C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.txt', os.path.join(C, '03_Skripte', 'Argumentationsstruktur_Ergebnisteile_2026-10-02', 'textbausteine.txt')),
    ('C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/codebook.md', os.path.join(C, '03_Skripte', 'Argumentationsstruktur_Ergebnisteile_2026-10-02', 'codebook.md')),
    ('C/02_Befunde/Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md', os.path.join(C, '02_Befunde', 'Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md')),
    ('C/00_Steuerung/Projektanweisungen_Fassung17.md', os.path.join(C, '00_Steuerung', 'Projektanweisungen_Fassung17.md')),
    ('C/01_Verfahren/Stilprofil_2026-09-13.md', os.path.join(C, '01_Verfahren', 'Stilprofil_2026-09-13.md')),
    ('C/02_Befunde/Berichtsraster_2026-09-23.md', os.path.join(C, '02_Befunde', 'Berichtsraster_2026-09-23.md')),
    ('C/04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md', os.path.join(C, '04_Uebergaben', 'Plan_Weitere_Schritte_2026-09-25.md')),
    ('C/04_Uebergaben/Textvorschlag_5_2026-09-30.md', os.path.join(C, '04_Uebergaben', 'Textvorschlag_5_2026-09-30.md')),
    ('C/03_Skripte/Abgleich_Ergebnisse_2026-10-03/quellen/Auswertungs_und_Berichtsumfang_2026-09-24.md', os.path.join(C, '03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'quellen', 'Auswertungs_und_Berichtsumfang_2026-09-24.md')),
    ('C/04_Uebergaben/Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md', os.path.join(C, '04_Uebergaben', 'Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md')),
])

aus('Nachrechnung zur Zweitprüfung der Teiltabelle 2c (nachrechnung.py, 03.10.2026)')
aus('')
aus('0 Eingänge (MD5)')
for k, p in P.items():
    aus('  ' + k.ljust(100), md5(p))
# lokale Eingänge in W gegen die Ordnerfassung in C
CORD = os.path.join(C, '03_Skripte', 'Abgleich_Ergebnisse_2026-10-03')
gleich = []
for f in ['textstand.json', 'eigen.json', 'abgleich_2a.json', 'master_saetze.json', 'konsens_2a.py', 'konsens_2a.csv', 'teiltabelle_2b.csv',
          'teiltabelle_2b.md', 'register_pruefung.md', 'textstand_saetze.md', 'eigen.txt', 'zweitpruefung_2b.md']:
    gleich.append(f + (' gleich' if md5(os.path.join(W, f)) == md5(os.path.join(CORD, f)) else ' VERSCHIEDEN'))
aus('  W gegen C/03_Skripte/Abgleich_Ergebnisse_2026-10-03:', ', '.join(gleich))
aus('')

# ------------------------------------------------------------------ Korpus
KORPUS = list(csv.DictReader(open(P['C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv'], encoding='utf-8'), delimiter=SK))
TB = json.load(open(P['C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.json'], encoding='utf-8'))
STUD = OrderedDict()
for r in KORPUS:
    STUD.setdefault(r['studie'], []).append(r)
KERN = [s for s in STUD if STUD[s][0]['gruppe'] == 'Kern']
ERW = [s for s in STUD if STUD[s][0]['gruppe'] != 'Kern']
SID = {r['studie'] + ' ' + r['satz']: r for r in KORPUS}


def sek(r):
    return [c for c in r['sekundaer'].split(SK) if c]


def hat(r, code):
    return r['primaer'] == code or code in sek(r)


def ids(menge, bed):
    return [r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in menge and bed(r)]


def rx(muster, menge=None):
    menge = menge or list(STUD)
    return [r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in menge and re.search(muster, r['text'])]


def erster_befund(studie):
    for r in STUD[studie]:
        if r['primaer'].startswith('B'):
            return r['satz']
    return None


def letzter_befund(studie):
    b = [r['satz'] for r in STUD[studie] if r['primaer'].startswith('B')]
    return b[-1] if b else None


def pos(sid):
    st, nr = sid.rsplit(' ', 1)
    sae = [r['satz'] for r in STUD[st]]
    i = sae.index(nr)
    eb, lb = erster_befund(st), letzter_befund(st)
    if eb is None:
        return 'ohne Befund'
    if i < sae.index(eb):
        return 'vor dem ersten Befund'
    if i > sae.index(lb):
        return 'nach dem letzten Befund'
    return 'im Befundteil'


def kurz(sid, n=150):
    return sid + ' ' + SID[sid]['primaer'] + ('(' + '+'.join(sek(SID[sid])) + ')' if sek(SID[sid]) else '') + ': ' + SID[sid]['text'][:n]


aus('1 Korpus')
aus('  Kern', len(KERN), 'Studien', sum(len(STUD[s]) for s in KERN), 'Sätze · erweitert', len(ERW), 'Studien', sum(len(STUD[s]) for s in ERW), 'Sätze')
aus('  Gruppen der Anlage:', dict(Counter(STUD[s][0]['gruppe'] for s in STUD)))
aus('')

# ------------------------------------------------------------------ Kapitel 5, Codes
KON = OrderedDict()
for r in csv.DictReader(open(P['W/konsens_2a.csv'], encoding='utf-8'), delimiter=SK):
    KON[r['satz']] = r
TS = json.load(open(P['W/textstand.json'], encoding='utf-8'))
SATZ = OrderedDict()
for a in TS['absaetze']:
    for s in a['saetze']:
        SATZ[s['id']] = s
MS = json.load(open(P['W/master_saetze.json'], encoding='utf-8'))['saetze']

# ------------------------------------------------------------------ 2 Nachrechnung je Zeile
aus('2 Nachrechnung der Korpuszahlen und Satzlisten der Zeilen (erwartet laut Zeile → gerechnet)')
CHK = []


def chk(zeile, text, erwartet, gerechnet):
    ok = erwartet == gerechnet
    CHK.append(ok)
    aus('  ' + ('ok    ' if ok else 'ABWEICHUNG ') + zeile.ljust(7), text, '| erwartet', erwartet, '| gerechnet', gerechnet)


fam = TB['familien']
chk('2c.1', 'OBJ_SUBJEKT Kern Sätze, Studien', (5, 3), (fam['OBJ_SUBJEKT']['kern_saetze'], len(fam['OBJ_SUBJEKT']['kern_studien'])))
chk('2c.1', 'X1 mit O1 im Kern', [], ids(KERN, lambda r: r['primaer'] == 'X1' and 'O1' in sek(r)))
chk('2c.1', 'X1 mit O1 im ganzen Korpus', [], ids(list(STUD), lambda r: r['primaer'] == 'X1' and 'O1' in sek(r)))
chk('2c.1', 'Flussdiagramm im Korpustext', [], rx(r'(?i)flow ?(chart|diagram)|CONSORT'))
chk('2c.1', 'planmäßiges Ende im Korpustext', [], rx(r'(?i)as planned|\bterminat|\bstopped\b|\bended\b|prematur|according to (the )?protocol'))
chk('2c.2', 'O1 im Kern, Studien', ['Negra2019', 'Negra2020', 'Sammoud2024'], sorted({x.split(' ')[0] for x in ids(KERN, lambda r: hat(r, 'O1'))}))
aus('         O1-Sätze im Kern:', ids(KERN, lambda r: hat(r, 'O1')))
for s in ids(KERN, lambda r: hat(r, 'O1')):
    aus('           ' + kurz(s))
aus('         Analysezahl im Korpus (n = …, „of the N participants“, „included“ mit Zahl):', rx(r'(?i)\bn ?= ?\d|of the \d+ participants|included a total|\(\s*n\s*=\s*\d'))
for s in rx(r'(?i)\bn ?= ?\d|of the \d+ participants|included a total'):
    aus('           ' + kurz(s, 170) + ' · ' + pos(s))
chk('2c.3', 'X1 mit O4 im ganzen Korpus', ['Hilska2021 1.1'], ids(list(STUD), lambda r: r['primaer'] == 'X1' and 'O4' in sek(r)))
chk('2c.3', 'OBJ_ORT Kern', (10, 7), (fam['OBJ_ORT']['kern_saetze'], len(fam['OBJ_ORT']['kern_studien'])))
aus('         Objektsätze mit zwei oder mehr Objekten (Tables/Figures n and m, n–m):', rx(r'(?i)(tables?|figures?|figs?)\s+\d+\s*(and|–|-|to)\s*\d+'))
for s in rx(r'(?i)(tables?|figures?|figs?)\s+\d+\s*(and|–|-|to)\s*\d+'):
    if SID[s]['primaer'] == 'X1':
        aus('           ' + kurz(s, 170) + ' · Subjekt ' + SID[s]['objekt_subjekt'] + ' Ort ' + SID[s]['objekt_ort'])
aus('         Moran 1.3:', SID['Moran2024 1.3']['text'])
chk('2c.4', 'Ausgangsvergleich mit Signifikanzaussage Kern (Sätze, Studien)', (5, 4), (fam['O_BASELINE_TEST']['kern_saetze'], len(fam['O_BASELINE_TEST']['kern_studien'])))
aus('         O4-Sätze mit vorhandenem Unterschied (significant … differences were detected, except for, difference … of):')
for s in rx(r'(?i)differences were detected|except for the inter-limb|between group difference at baseline of'):
    aus('           ' + kurz(s, 200) + ' · ' + SID[s]['gruppe'])
aus('         Richtung eines Ausgangsunterschieds („in favour“, „favor“, „higher/lower at baseline“) in O4-Sätzen:',
    ids(list(STUD), lambda r: hat(r, 'O4') and re.search(r'(?i)favou?r|higher at baseline|lower at baseline|better at baseline', r['text'])))
chk('2c.5', '„median“ im Korpus', ['Moran2024 1.2'], rx(r'(?i)\bmedian\b'))
aus('         Mittel der Einheiten oder je Woche (erweitert):', rx(r'(?i)\bmean of\b|\baverage number\b|×/week|per week|dose exposures', ERW))
aus('         Zählungen nach Status oder Anteil vollständiger Durchführung (erweitert):', rx(r'(?i)missed \d|missed sessions|performed \d+% of the time|completed all|not fully completing', ERW))
chk('2c.5', 'Objekte im Kern, Erstnennung nach Form und Stellung', {('Objektsatz', 'vor dem ersten Befund'): 11, ('Klammer oder Nebenstellung', 'ab dem ersten Befund'): 9,
                                                                   ('Objektsatz', 'ab dem ersten Befund'): 3, ('Klammer oder Nebenstellung', 'vor dem ersten Befund'): 3},
    dict(Counter((v[2], v[3]) for s in KERN for v in TB['objekt_erstnennung'].get(s, {}).values())))
chk('2c.6', 'Raten (O_RATE) im Kern, Studien', ['Beato2018', 'Lloyd2016', 'Negra2019'], sorted({b[0] for b in fam['O_RATE']['belege'] if b[0] in KERN}))
aus('         niedrige Umsetzung mit Einstufung (erweitert):', rx(r'(?i)poor|low compliance|lower compliance', ERW))
chk('2c.7', 'Schwelle der Umsetzung im Kern', ['Lloyd2016 1.3', 'Sammoud2024 1.1'], sorted(rx(r'(?i)threshold|more than 85%', KERN)))
aus('         Schwellen und Anteile an Schwellen in O2-Sätzen (erweitert):', ids(ERW, lambda r: hat(r, 'O2') and re.search(r'(?i)at least|or more|more than|all \d+ sessions|<\s*75', r['text'])))
chk('2c.8', '„respectively“ im Kern (Sätze, Studien), wie B_RESPECTIVELY', (8, 5), (fam['B_RESPECTIVELY']['kern_saetze'], len(fam['B_RESPECTIVELY']['kern_studien'])))
chk('2c.8', '„lower bound“ oder Untergrenze im Korpus', [], rx(r'(?i)lower bound|at minimum|conservative estimate'))
aus('         parallele Werte ohne „respectively“ (Klammer mit „x and y“ oder Paarliste ohne Zuordnungswort):')
for s in rx(r'\(\s*[−\-]?\d[^()]*\band\b\s*[−\-]?\d[^()]*\)'):
    if not re.search(r'(?i)respectiv|respectful', SID[s]['text']):
        aus('           ' + kurz(s, 200) + ' · ' + SID[s]['gruppe'])
chk('2c.9', 'O3 im Kern', ['Beato2018'], sorted({x.split(' ')[0] for x in ids(KERN, lambda r: hat(r, 'O3'))}))
aus('         „±“ in Befundsätzen, Kern und erweitert:', 'Kern', ids(KERN, lambda r: r['primaer'].startswith('B') and '±' in r['text']), '· erweitert', ids(ERW, lambda r: r['primaer'].startswith('B') and '±' in r['text']))
aus('         Mittelwert mit Spanne in Klammer (erweitert):', rx(r'(?i)\(range,|varied from \d', ERW))
chk('2c.10', '„load“ im Korpus', [], rx(r'(?i)\bload\b'))
chk('2c.10', 'Lloyd 1.3 mit V2', True, 'V2' in sek(SID['Lloyd2016 1.3']))
chk('2c.11', 'Z2 im Kern', [], ids(KERN, lambda r: hat(r, 'Z2')))
chk('2c.11', 'Z2 erweitert (alle sekundär)', ['Klusemann2012 1.1', 'Klusemann2012 1.3', 'Klusemann2012 1.6', 'Veith2021 3.3'], ids(ERW, lambda r: hat(r, 'Z2')))
chk('2c.11', 'Z2 erweitert primär', [], ids(ERW, lambda r: r['primaer'] == 'Z2'))
chk('2c.12', 'Aussage über nicht erhobene Daten im Korpus', [], rx(r'(?i)\bnot (collected|recorded|assessed|monitored|measured|available|obtained)\b|\bno data\b|were not (asked|surveyed)'))
aus('         Erhebung oder Rücklauf bei der Kontrollgruppe (O-Sätze):', ids(list(STUD), lambda r: r['primaer'].startswith('O') and re.search(r'(?i)control', r['text'])))
for s in ids(list(STUD), lambda r: r['primaer'].startswith('O') and re.search(r'(?i)control', r['text'])):
    aus('           ' + kurz(s, 170))
chk('2c.13', 'O5 im Kern', ['Aloui2022'], sorted({x.split(' ')[0] for x in ids(KERN, lambda r: hat(r, 'O5'))}))
chk('2c.13', 'Messfehler gegen SWC im Korpus', [], [s for s in rx(r'(?i)\bSWC\b|smallest worthwhile') if re.search(r'(?i)typical error|reliab|\bICC|\bCV\b', SID[s]['text'])])
chk('2c.14', '„trials“, „attempts“, „valid“ im Korpus (ohne „trial“ für die Studie)', [], rx(r'(?i)\btrials\b|\battempts?\b|\bvalid\b'))
aus('         „trial“ im Korpus (nur als Studie):', [s + ': ' + re.search(r'.{0,30}\btrial\b.{0,10}', SID[s]['text']).group(0) for s in rx(r'(?i)\btrial\b')])
chk('2c.17', '„unadjusted“ im Kern', [], rx(r'(?i)unadjusted', KERN))
chk('2c.17', '„unadjusted“ erweitert', ['Hilska2021 3.3', 'Hilska2021 4.1', 'Hilska2021 4.2', 'Hilska2021 6.4'], rx(r'(?i)unadjusted', ERW))
chk('2c.17', 'B_RICHTUNG Kern (Sätze, Studien)', (9, 5), (fam['B_RICHTUNG']['kern_saetze'], len(fam['B_RICHTUNG']['kern_studien'])))
chk('2c.17', 'Blockbeginn Quantor als Einzelbefund im Kern', 1, TB['blockstart']['Quantor ueber die Tests einer Zielgroesse (Einzelbefund)'])
chk('2c.18', 'B_POSTWERT Kern Studien', ['Bouafif2026', 'Sammoud2024'], sorted(fam['B_POSTWERT']['kern_studien']))
aus('         Rohdifferenz zwischen Gruppen mit Einheit und p (mean difference) im Kern:', ids(KERN, lambda r: r['primaer'] == 'B1' and re.search('mean difference: ' + chr(0xf02d) + '?[\\d.]+ ?(cm|s|m)\\b', r['text'])))
aus('         Intervall in Befundsätzen (CI, CL, confidence) Kern / erweitert:', [s for s in rx(r'(?i)\bCI\b|CL90|confidence') if SID[s]['primaer'].startswith('B')])
chk('2c.19', 'Sammoud 3.1 Blockbeginn Themenanker', True, any(b[0] == 'Sammoud2024' and b[1] == '3.1' for b in TB['blockstart_belege']['Themenanker']) if 'blockstart_belege' in TB else 'Sammoud2024 3.1' in lies(P['C/03_Skripte/Argumentationsstruktur_Ergebnisteile_2026-10-02/textbausteine.txt']))
chk('2c.20', 'B_NULL Kern Studien', 9, len(fam['B_NULL']['kern_studien']))
chk('2c.21', 'Nullformel (Spalte null) und Intervall (Spalte ki) zugleich', ['Klusemann2012 2.2'], [r['studie'] + ' ' + r['satz'] for r in KORPUS if r['null'] == '1' and int(r['ki'] or 0) > 0])
aus('         Spalte msd (±) in Befundsätzen mit Null- oder Unklarheitsurteil (trivial, unclear, little difference, no clear, remained):')
for s in ids(list(STUD), lambda r: r['primaer'].startswith('B') and '±' in r['text'] and re.search(r'(?i)\btrivial\b|unclear|little difference|no clear|remained', r['text'])):
    aus('           ' + kurz(s, 260) + ' · ' + SID[s]['gruppe'] + ' · null ' + SID[s]['null'] + ' ki ' + SID[s]['ki'] + ' msd ' + SID[s]['msd'])
aus('         Klusemann 2.2 (Erklärung der ±-Angaben):', SID['Klusemann2012 2.2']['text'])
aus('         Urteil „unclear“ im Korpus:', rx(r'(?i)unclear'), '· im Kern:', rx(r'(?i)unclear', KERN))
for s in rx(r'(?i)unclear'):
    aus('           ' + kurz(s, 260))
aus('         Nullurteil gegen eine Schwelle im Kern („trivial“, „substantial“):', ids(KERN, lambda r: r['primaer'].startswith('B') and re.search(r'(?i)\btrivial\b|substantial', r['text'])))
for s in ids(KERN, lambda r: r['primaer'].startswith('B') and re.search(r'(?i)\btrivial\b|substantial', r['text'])):
    aus('           ' + kurz(s, 220))
aus('         Einordnung nach vorab genannter Schwelle (acceptable, poor, notably):', rx(r'(?i)acceptable|poor|notably'))
chk('2c.23', '„hypothes“ in der Anlage', [], rx(r'(?i)hypothes'))
aus('         Regeln mit Entscheidung im Ergebnisteil (V2 primär oder sekundär):', ids(list(STUD), lambda r: hat(r, 'V2')))
aus('         Quantor mit Nullbefund als Einzelbefund (none of, no …) in B1/B2-Sätzen des Kerns:', ids(KERN, lambda r: r['primaer'] in ('B1', 'B2') and re.search(r'(?i)^(none of|no )', r['text'])))
aus('         Hammami 1.3:', SID['Hammami2016 1.3']['text'])
chk('2c.25', 'V2 im Kern primär', [], ids(KERN, lambda r: r['primaer'] == 'V2'))
chk('2c.25', 'V2 im Kern sekundär', ['Lloyd2016 1.3', 'Sammoud2024 1.1'], ids(KERN, lambda r: 'V2' in sek(r)))
chk('2c.25', 'V2 erweitert primär', ['Hilska2021 6.1', 'Veith2021 2.3', 'Rogers2020 1.2', 'Rogers2020 1.9'], ids(ERW, lambda r: r['primaer'] == 'V2'))
aus('         Stellung aller V2-Sätze:', [(s, pos(s)) for s in ids(list(STUD), lambda r: hat(r, 'V2'))])
m45 = [s for s in MS if s['id'].startswith('4.7 A1 S5')]
aus('         Master 4.7 A1 S5:', m45[0]['text'] if m45 else '—')
chk('2c.26', 'V1 im Korpus (primär oder sekundär)', ['Hilska2021 6.1', 'Veith2021 1.1', 'Veith2021 2.3', 'Asimakidis2022 1.1'], ids(list(STUD), lambda r: hat(r, 'V1')))
aus('         Stellung V1:', [(s, pos(s)) for s in ids(list(STUD), lambda r: hat(r, 'V1'))])
aus('         Themenanker und Verfahren als Subjekt (Regarding/For …, the … analysis indicated/revealed):', rx(r'(?i)^(regarding|for|in terms of|in reference to)[^,]*, the [^,]*?(analysis|test)\b'))
chk('2c.27', 'Z1 Kern primär', [], ids(KERN, lambda r: r['primaer'] == 'Z1'))
chk('2c.27', 'Z1 Kern sekundär', ['Liu2024 2.5', 'Moran2024 1.1', 'Moran2024 1.2', 'Moran2024 1.3'], ids(KERN, lambda r: 'Z1' in sek(r)))
aus('         Stellung Z1 erweitert:', [(s, pos(s)) for s in ids(ERW, lambda r: hat(r, 'Z1'))])
chk('2c.27', 'Sensitivität, Per-Protokoll, Bootstrap im Kern', [], rx(r'(?i)sensitivity|per[- ]protocol|bootstrap', KERN))
aus('         Per-Protokoll-ähnliche Regeln im Korpus (compliance-Ausschluss, regardless of compliance):', rx(r'(?i)excluded from the final analysis for low compliance|regardless of compliance'))
chk('2c.28', '„remaining“, „other tests“ im Kern', ['Beato2018 4.2', 'Negra2019 2.8'], sorted(rx(r'(?i)\bremaining\b|\bother tests\b|all the other', KERN)))
chk('2c.29', 'letzter Satz mit Klammer am Satzende (Kern)', 5, sum(1 for s in KERN if TB['ende'][s]['letzter_klammer']))
chk('2c.29', 'letzter Satz mit Z (Kern und erweitert)', [], [s for s in STUD if STUD[s][-1]['primaer'].startswith('Z')])
chk('2c.31', 'mehrsätzige O2-Folgen (zwei O2-Sätze nacheinander) im Kern', [], [s for s in KERN if any(STUD[s][i]['primaer'] == 'O2' and STUD[s][i + 1]['primaer'] == 'O2' for i in range(len(STUD[s]) - 1))])
chk('2c.36', 'V1 erweitert, Studien', ['Asimakidis2022', 'Hilska2021', 'Veith2021'], sorted({x.split(' ')[0] for x in ids(ERW, lambda r: hat(r, 'V1'))}))
chk('2c.42', 'unadjustiert und adjustiert im selben Satz', ['Hilska2021 3.3', 'Hilska2021 4.1', 'Hilska2021 6.4'], rx(r'(?i)unadjusted IRR.*adjusted IRR'))
chk('2c.44', 'Objektformen erweitert Subjekt / Ort', (5, 5), (len(ids(ERW, lambda r: r['objekt_subjekt'] != '0')), len(ids(ERW, lambda r: r['objekt_ort'] != '0'))))
chk('2c.45', 'Blockanfänge Kern gesamt', 38, sum(TB['blockstart'].values()))
chk('2c.46', '„respectively“ erweitert, Studien', 6, len(fam['B_RESPECTIVELY']['ext_studien']))
chk('2c.47', '„except“ im Kern', ['Bouafif2026 1.1', 'Negra2020 1.4', 'Negra2020 1.5', 'Sammoud2024 1.5'], sorted(rx(r'\bexcept\b', KERN)))
aus('         „except“ erweitert:', rx(r'\bexcept\b', ERW))
aus('         Ausnahme zu einem Sammelbefund in eigenem Folgesatz (B4 gefolgt von „However“ oder B-Satz mit Ausnahme), Kern:')
for s in KERN:
    rs = STUD[s]
    for i in range(1, len(rs)):
        if rs[i - 1]['primaer'] == 'B4' and re.match(r'(?i)however', rs[i]['text']):
            aus('           ' + kurz(s + ' ' + rs[i - 1]['satz'], 130))
            aus('           → ' + kurz(s + ' ' + rs[i]['satz'], 200))
aus('         Sätze über die übrigen Tests (Kern) mit den Sätzen davor im selben Absatz:')
for s in sorted(rx(r'(?i)\bremaining\b|\bother tests\b|all the other', KERN)):
    st, nr = s.split(' ')
    ab = nr.split('.')[0]
    davor = [st + ' ' + r['satz'] for r in STUD[st] if r['satz'].split('.')[0] == ab and int(r['satz'].split('.')[1]) < int(nr.split('.')[1])]
    for d in davor[-3:]:
        aus('           ' + kurz(d, 160))
    aus('           → ' + kurz(s, 160))
bnull = set(b[0] + ' ' + b[1] for b in fam['B_NULL']['belege'])
aus('         Familie B_NULL (maßgeblich nach Befund Anhang B):', len(bnull), 'Belege · davon mit Intervall (Spalte ki oder ± in der Spalte msd):',
    [s for s in sorted(bnull) if int(SID[s]['ki'] or 0) > 0 or int(SID[s]['msd'] or 0) > 0])
aus('         Gruppenvergleich (B1) mit dem Urteil „unclear“:', ids(list(STUD), lambda r: r['primaer'] == 'B1' and 'unclear' in r['text']))
aus('  Prüfungen:', sum(CHK), 'von', len(CHK), 'wie in der Zeile')
aus('')

# ------------------------------------------------------------------ 3 Sequenzen
aus('3 Sequenzen § 5.2 gegen A1 bis A6 (längste gemeinsame Teilfolge der Primärcodes, wie bausteine_2c.py § 2)')


def lcs(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for x in range(len(a)):
        for y in range(len(b)):
            t[x + 1][y + 1] = t[x][y] + 1 if a[x] == b[y] else max(t[x][y + 1], t[x + 1][y])
    return t[len(a)][len(b)]


SEQ = OrderedDict([(1, ('Negra2019', [1])), (2, ('Sammoud2024', [2, 3])), (3, ('Liu2024', [2, 3, 4])), (4, ('Aloui2022', [2, 3, 4, 5, 6])), (5, ('Negra2019', [2])), (6, ('Moran2024', [1]))])
SC = {n: [r['primaer'] for r in STUD[s] if int(r['absatz']) in a] for n, (s, a) in SEQ.items()}
for a in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']:
    k = [KON[i]['primaer'] for i in SATZ if i.startswith(a + ' ')]
    aus('  ' + a, ' '.join(k).ljust(36), ' · '.join('S' + str(n) + ' ' + str(lcs(k, SC[n])) + '/' + str(lcs(k, [c for c in SC[n] if c != 'B2'])) for n in SC))
aus('')

# ------------------------------------------------------------------ 4 Zitate am angegebenen Ort
aus('4 Zitate der Spalte Ergebnis: Fundorte (Anlage-Satz, Abschnitt des Befunds, Quelle, Kapitel-5-Satz, Master-Satz)')
TAB = list(csv.DictReader(open(P['W/teiltabelle_2c.csv'], encoding='utf-8'), delimiter=SK))
BEF = lies(P['C/02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md'])
BABS = OrderedDict()
akt = 'Kopf'
for z in BEF.split('\n'):
    m = re.match(r'^#{2,3} (\d+(?:\.\d+)?|Anhang [AB])\b', z)
    if m:
        akt = m.group(1)
    BABS[akt] = BABS.get(akt, '') + ' ' + z
QUELL = OrderedDict([('f17', P['C/00_Steuerung/Projektanweisungen_Fassung17.md']), ('stil', P['C/01_Verfahren/Stilprofil_2026-09-13.md']),
                     ('raster', P['C/02_Befunde/Berichtsraster_2026-09-23.md']), ('plan', P['C/04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md']),
                     ('tv5', P['C/04_Uebergaben/Textvorschlag_5_2026-09-30.md']),
                     ('umfang', P['C/03_Skripte/Abgleich_Ergebnisse_2026-10-03/quellen/Auswertungs_und_Berichtsumfang_2026-09-24.md']),
                     ('register', P['W/register_pruefung.md'])])
QT = {k: norm(lies(p)) for k, p in QUELL.items()}
NB = {k: norm(v) for k, v in BABS.items()}
kurzwort = 0
fundliste = []
for z in TAB:
    for q in re.findall(r'„([^“]+)“', z['Ergebnis']):
        teile = [norm(t) for t in re.split(r'…', q) if len(norm(t)) >= 4]
        if not teile or len(q) <= 7:
            kurzwort += 1
            continue
        orte = []
        orte += ['Anlage ' + r['studie'] + ' ' + r['satz'] for r in KORPUS if all(t in norm(r['text']) for t in teile)]
        orte += ['Befund § ' + k for k, v in NB.items() if all(t in v for t in teile)]
        orte += [k for k, v in QT.items() if all(t in v for t in teile)]
        orte += ['Kap5 ' + i for i in SATZ if all(t in norm(SATZ[i]['text']) for t in teile)]
        orte += ['Master ' + s['id'] for s in MS if all(t in norm(s['text']) for t in teile)]
        fundliste.append((z['Nr.'], q, orte))
for nr, q, orte in fundliste:
    aus('  ' + nr.ljust(7), q[:70].ljust(72), '→', ', '.join(orte[:6]) + (' …' if len(orte) > 6 else '') if orte else 'NICHT GEFUNDEN')
aus('  Zitate geprüft:', len(fundliste), '· kurze Einzelwörter ohne Ortsprüfung:', kurzwort, '· nicht gefunden:', sum(1 for _, _, o in fundliste if not o))
# Platzhalterformen gegen ihre angegebene Quelle
for q, quelle in [('Tab. ⟨n⟩ zeigt', 'stil'), ('stehen in Tab. ⟨n⟩', 'stil'), ('zugunsten der ⟨Gruppe⟩', 'f17')]:
    aus('  Platzhalter „' + q + '“ in', quelle + ':', q in QT[quelle], '· in Befund § 5.1:', q in NB['5.1'])
aus('  Stilprofil Teil 4 wörtlich: „Tab. 3 zeigt …“', 'Tab. 3 zeigt' in QT['stil'], '· „… stehen in Tab. 2.“', 'stehen in Tab. 2.' in QT['stil'])
aus('  „mit Tests“ in F17 nur als Wortanfang von „mit Testspielen“:', re.findall(r'mit Tests\w*', QT['f17']))
aus('')

# ------------------------------------------------------------------ 5 Status
aus('5 Status der Teiltabelle 2c und Verweise auf Teiltabelle 2b')
Z2B = OrderedDict((r['Nr.'], r) for r in csv.DictReader(open(P['W/teiltabelle_2b.csv'], encoding='utf-8'), delimiter=SK))
kz, fz = Counter(), Counter()
for z in TAB:
    m = re.match(r'^Korpus: (.+?) · Fundstelle: (.+)$', z['Status'])
    kz[m.group(1)] += 1
    fz[re.match(r'^(erfüllt|teilweise|nicht erfüllt|bewusst anders|keine Regel)', m.group(2)).group(1)] += 1
aus('  Korpus:', dict(kz), '· Fundstelle:', dict(fz))
for z in TAB:
    refs = re.findall(r'2b\.(\d+)', z['Status'])
    for ref in refs:
        r2 = Z2B['2b.' + ref]
        mass = r2['Befundstelle'].split(' · ')[0]
        st = r2['Status'].split(' · ')[0]
        if mass == 'Korpus':
            aus('  ' + z['Nr.'].ljust(7), 'Fundstellenstatus', re.search(r'Fundstelle: (.+)$', z['Status']).group(1), 'stützt sich auf 2b.' + ref, '(Maßstab', mass + ', Status', st + ')')
aus('')

# ------------------------------------------------------------------ 6 Semikola
aus('6 Semikola')
for f in ['bausteine_2c.py', 'bausteine_2c.txt', 'teiltabelle_2c.md', 'teiltabelle_2c.csv']:
    aus('  ' + f.ljust(22), lies(os.path.join(W, f)).count(SK))
rows = list(csv.reader(open(os.path.join(W, 'teiltabelle_2c.csv'), encoding='utf-8'), delimiter=SK))
aus('  CSV: Zeilen', len(rows), '· Felder je Zeile', sorted({len(r) for r in rows}), '· Zellen mit Semikolon', sum(1 for r in rows for c in r if SK in c))
aus('  dieses Skript:', lies(os.path.abspath(__file__)).count(SK))

with open(os.path.join(HIER, 'nachrechnung.txt'), 'w', encoding='utf-8') as fo:
    fo.write('\n'.join(OUT) + '\n')
print('nachrechnung.txt geschrieben,', len(OUT), 'Zeilen, Prüfungen', sum(CHK), 'von', len(CHK))

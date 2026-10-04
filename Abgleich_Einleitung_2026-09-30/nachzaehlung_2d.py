# -*- coding: utf-8 -*-
"""
nachzaehlung_2d.py — Schritt 2 (d): Korpusaussagen, auf die sich Potenziale stützen sollen, am Satzkorpus nachgezählt.

Grundlage: Anlage `02_Befunde\\Argumentationsstruktur_Einleitungen_RCT_2026-09-30_Saetze.csv` (Konsens),
`03_Skripte\\Argumentationsstruktur_Einleitungen_2026-09-30\\codes_B.json` (Codierer B) und Anhang C des Befunds
`02_Befunde\\Argumentationsstruktur_Einleitungen_RCT_2026-09-30.md`. Kernkorpus 10 Studien.
Pfade relativ zum Ordner des Skripts (`03_Skripte\\Abgleich_Einleitung_2026-09-30`), sonst Staging-Pfade oder Argumente.
Ohne Semikolon außerhalb von Zeichenketten (chr(59) als Trennzeichen der CSV).
Ausgabe: nachzaehlung_2d.txt neben dem Skript.
"""
import csv, json, os, re, sys, collections, statistics

SEMI = chr(59)
HIER = os.path.dirname(os.path.abspath(__file__))
STAGE = '/mnt/user-data/uploads/Bachelorarbeit/Claude'


def pfad(teile, ersatz):
    p = os.path.normpath(os.path.join(HIER, *teile))
    return p if os.path.exists(p) else ersatz


ANL = sys.argv[1] if len(sys.argv) > 1 else pfad(['..', 'Argumentationsstruktur_Einleitungen_2026-09-30'],
                                                  STAGE + '/03_Skripte/Argumentationsstruktur_Einleitungen_2026-09-30')
CSVP = sys.argv[2] if len(sys.argv) > 2 else pfad(['..', '..', '02_Befunde', 'Argumentationsstruktur_Einleitungen_RCT_2026-09-30_Saetze.csv'],
                                                   STAGE + '/02_Befunde/Argumentationsstruktur_Einleitungen_RCT_2026-09-30_Saetze.csv')
BEF = sys.argv[3] if len(sys.argv) > 3 else pfad(['..', '..', '02_Befunde', 'Argumentationsstruktur_Einleitungen_RCT_2026-09-30.md'],
                                                  STAGE + '/02_Befunde/Argumentationsstruktur_Einleitungen_RCT_2026-09-30.md')

rows = list(csv.DictReader(open(CSVP, encoding='utf-8'), delimiter=SEMI))
Bc = json.load(open(os.path.join(ANL, 'codes_B.json'), encoding='utf-8'))
CORE = ['Lloyd2016', 'Hammami2016', 'Beato2018', 'Negra2019', 'Negra2020', 'Aloui2022', 'Liu2024', 'Moran2024', 'Sammoud2024', 'Bouafif2026']
by = collections.defaultdict(list)
for r in rows:
    by[r['studie']].append(r)
Bmap = {s: {x[0]: (x[1], x[2]) for x in Bc[s]} for s in Bc}
# Einführung des plyometrischen Arms oder des Oberbegriffs, unter den er fällt (Befund § 3.2: „Hammami im vierten“ Absatz)
EINF = {'Lloyd2016': '1.1', 'Hammami2016': '4.1', 'Beato2018': '2.1', 'Negra2019': '2.1', 'Negra2020': '2.1',
        'Aloui2022': '2.1', 'Liu2024': '3.2', 'Moran2024': '1.2', 'Sammoud2024': '3.1', 'Bouafif2026': '2.1'}


def sek(s):
    return set(x for x in s.split(SEMI) if x)


def codes(r, wer):
    if wer == 'K':
        return r['primaer'], sek(r['sekundaer'])
    p, s = Bmap[r['studie']][r['satz']]
    return p, sek(s)


def hat(r, wer, c):
    p, s = codes(r, wer)
    return p == c or c in s


def satz(s, nr):
    return next(r for r in by[s] if r['satz'] == nr)


out = []
w = out.append
for wer, name in [('K', 'Konsens'), ('B', 'Codierer B')]:
    w('=== %s ===' % name)
    # d1 Vorzüge
    t3 = [s for s in CORE if any(hat(r, wer, 'T3') for r in by[s])]
    w('d1 Vorzüge (T3 primär oder sekundär) vorhanden: %d von 10: %s' % (len(t3), ', '.join(t3)))
    for lesart, wahl in [('Lesart i: erster Satz mit T1', lambda s: next(r for r in by[s] if hat(r, wer, 'T1'))),
                         ('Lesart ii: Einführung des plyometrischen Arms (Befund § 3.2)', lambda s: satz(s, EINF[s]))]:
        ein, beide, nurV, nurW, andere = [], [], [], [], []
        for s in CORE:
            t1 = wahl(s)
            p, sc = codes(t1, wer)
            alle = {p} | sc
            hatV, hatW = 'T3' in alle, 'E1' in alle
            if hatV:
                ein.append(s)
            if hatV and hatW:
                beide.append(s)
            elif hatV:
                nurV.append(s)
            elif hatW:
                nurW.append(s)
            else:
                andere.append('%s %s (%s)' % (s, t1['satz'], '+'.join(sorted(alle))))
        w('d1 %s — Vorzüge im Einführungssatz %d: %s' % (lesart, len(ein), ', '.join(ein)))
        w('   Wirksamkeit und Vorzüge %d: %s · nur Vorzüge %d: %s · nur Wirksamkeit %d: %s · anders: %s' % (
            len(beide), ', '.join(beide), len(nurV), ', '.join(nurV), len(nurW), ', '.join(nurW), ', '.join(andere) or '—'))
    # d5 Bedeutung der Lücke
    l2 = [s for s in CORE if any(hat(r, wer, 'L2') for r in by[s])]
    w('d5 Bedeutung der Lücke (L2 primär oder sekundär): %d: %s' % (len(l2), ', '.join(l2)))
    l2p = [s for s in CORE if any(codes(r, wer)[0] == 'L2' for r in by[s])]
    w('d5 L2 als Primärcode: %d: %s' % (len(l2p), ', '.join(l2p)))
    nach = []
    for s in CORE:
        R = by[s]
        zi = next(i for i, r in enumerate(R) if codes(r, wer)[0] == 'Z1')
        lastL = max(i for i, r in enumerate(R[:zi]) if hat(r, wer, 'L1'))
        l2i = [i for i, r in enumerate(R[:zi]) if hat(r, wer, 'L2')]
        if l2i:
            pos = ['nach' if i > lastL else ('gleich' if i == lastL else 'vor') for i in l2i]
            nach.append('%s: %s (letzter L1 %s)' % (s, ', '.join('%s %s' % (R[i]['satz'], p) for i, p in zip(l2i, pos)), R[lastL]['satz']))
    w('d5 Stellung der L2-Sätze zum schließenden Lückensatz: ' + ' | '.join(nach))
    zb = [s for s in CORE if codes(by[s][next(i for i, r in enumerate(by[s]) if codes(r, wer)[0] == 'Z1') - 1], wer)[0] == 'L2']
    w('d5 Satz vor dem Zweck ist ein Bedeutungssatz (L2 primär): %d: %s' % (len(zb), ', '.join(zb)))
    # d7 Dosis
    k3 = []
    for s in CORE:
        S = [r for r in by[s] if hat(r, wer, 'K3')]
        if S:
            k3.append('%s %s' % (s, ', '.join('%s %s(%s)' % (r['satz'], codes(r, wer)[0], SEMI.join(sorted(codes(r, wer)[1]))) for r in S)))
    w('d7 Dosis (K3 primär oder sekundär): %d: %s' % (len(k3), ' | '.join(k3)))
    # d10 Lücke und Zweck im selben Absatz
    gleich = []
    for s in CORE:
        R = by[s]
        zi = next(i for i, r in enumerate(R) if codes(r, wer)[0] == 'Z1')
        lastL = max(i for i, r in enumerate(R[:zi]) if hat(r, wer, 'L1'))
        if R[lastL]['absatz'] == R[zi]['absatz']:
            gleich.append(s)
    w('d10 Schließender Lückensatz und Zweck im selben Absatz: %d: %s · getrennt: %s' % (
        len(gleich), ', '.join(gleich), ', '.join(s for s in CORE if s not in gleich)))
    w('')

w('=== ohne Codierung oder nur Konsens ===')
# d2 Brückensatz
w('d2 Erster Absatz (Konsens), Primärcodes und letzter Satz:')
rein = []
for s in CORE:
    P1 = [r for r in by[s] if r['absatz'] == '1']
    pc = [r['primaer'] for r in P1]
    ist_rein = all(c.startswith('R') for c in pc)
    if ist_rein:
        rein.append(s)
    w('  %-12s %s %s | letzter Satz %s: %s' % (s, ' '.join(pc), '(rein R)' if ist_rein else '', P1[-1]['primaer'], P1[-1]['text'][:120]))
w('d2 Erster Absatz rein Relevanz: %d: %s' % (len(rein), ', '.join(rein)))
# d3 Mechanismus
w('d3 Mechanismus (T2 primär oder sekundär): Einführung (Lesart ii), erstes T2, erste Detailevidenz (E2, E3, K3 primär oder sekundär), T2-Sätze')
for s in CORE:
    R = by[s]
    iT1 = next(i for i, r in enumerate(R) if r['satz'] == EINF[s])
    iT2 = next((i for i, r in enumerate(R) if hat(r, 'K', 'T2')), None)
    iD = next((i for i, r in enumerate(R) if r['primaer'] in ('E2', 'E3', 'K3') or sek(r['sekundaer']) & {'E2', 'E3', 'K3'}), None)
    nT2p = sum(1 for r in R if r['primaer'] == 'T2')
    nT2 = sum(1 for r in R if hat(r, 'K', 'T2'))
    wT2 = sum(int(r['woerter']) for r in R if r['primaer'] == 'T2')
    if iT2 is None:
        w('  %-12s kein T2' % s)
        continue
    lage = 'nach der Einführung' if iT2 > iT1 else ('im Einführungssatz' if iT2 == iT1 else 'vor der Einführung')
    lage2 = '—' if iD is None else ('vor der Detailevidenz' if iT2 < iD else ('im selben Satz' if iT2 == iD else 'nach der Detailevidenz'))
    w('  %-12s Einführung %s · T2 %s (%s, %s) · Detailevidenz %s · T2-Sätze primär %d (%d Wörter), mit Sekundärcode %d' % (
        s, R[iT1]['satz'], R[iT2]['satz'], lage, lage2, R[iD]['satz'] if iD is not None else '—', nT2p, wT2, nT2))
N3 = [r for r in by['Negra2019'] if r['absatz'] == '3']
w('d3 Negra 2019 Absatz 3: %d Sätze, %d Wörter, Primärcodes %s' % (len(N3), sum(int(r['woerter']) for r in N3), ' '.join(r['primaer'] for r in N3)))
# d4 Reife
w('d4 Reife (K1 primär oder sekundär): Sätze, Wörter der K1-Primärsätze, Hypothese zur Reife')
for s in CORE:
    R = [r for r in by[s] if hat(r, 'K', 'K1')]
    if not R:
        w('  %-12s keine' % s)
        continue
    wp = sum(int(r['woerter']) for r in R if r['primaer'] == 'K1')
    zk = [r['satz'] for r in R if r['primaer'].startswith('Z')]
    nxt = []
    for r in R:
        i = by[s].index(r)
        if i + 1 < len(by[s]) and hat(by[s][i + 1], 'K', 'L1') and not hat(r, 'K', 'L1'):
            nxt.append(r['satz'])
    w('  %-12s %d Sätze (%d primär, %d Wörter primär) · Zweck- oder Hypothesensatz mit K1: %s · K1-Satz direkt vor einem Lückensatz: %s · %s' % (
        s, len(R), sum(r['primaer'] == 'K1' for r in R), wp, ', '.join(zk) or '—', ', '.join(nxt) or '—',
        ' | '.join('%s %s(%s) %s' % (r['satz'], r['primaer'], r['sekundaer'], r['text'][:60]) for r in R)))
# d6 Prävention
w('d6 Prävention und Verletzung im Kernkorpus (injur, prevent):')
for s in CORE:
    for r in by[s]:
        if re.search(r'injur|prevent', r['text'], re.I):
            w('  %-12s %s %s(%s), Einführung %s: %s' % (s, r['satz'], r['primaer'], r['sekundaer'], EINF[s], r['text'][:130]))
# d1 Gerät und Setting
w('d1 Gerät, Ausrüstung (equipment, apparatus, device, gear) im Kernkorpus:')
for s in CORE:
    for r in by[s]:
        if re.search(r'equipment|apparatus|device|gear\b', r['text'], re.I):
            w('  %-12s %s: %s' % (s, r['satz'], r['text'][:130]))
w('  (Ende der Liste)')
w('d1 Setting und Aufwand (supervis, home, video, online, remote, body mass, body weight, unloaded, cost, time, feasib, easy):')
for s in CORE:
    for r in by[s]:
        m = re.findall(r'unsupervis\w*|supervis\w*|\bhome\b|video\w*|online|remote\w*|own body mass|body ?weight|unloaded|cost\w*|training time|time[- ]efficient|feasib\w*|easy[\w-]*|easily', r['text'], re.I)
        if m:
            w('  %-12s %s %s(%s) [%s]: %s' % (s, r['satz'], r['primaer'], r['sekundaer'], ', '.join(sorted(set(x.lower() for x in m))), r['text'][:110]))
# d8 Lückendimensionen nach Anhang C
w('d8 Dimensionen der Lücke nach Anhang C des Befunds, Satzbezüge gegen die Konsenscodierung geprüft:')
bef = open(BEF, encoding='utf-8').read()
anhc = bef.split('## Anhang C')[1]
KAT = [('Uneinheitlichkeit', 'Uneinheitlichkeit'), ('Messinstrument', 'Messinstrumente'), ('Zielgröße', 'Zielgröße'),
       ('Reife', 'Reife'), ('Saisonphase', 'Saisonphase'), ('Dosis', 'Dosis oder Zeitverlauf'), ('Zeitverlauf', 'Dosis oder Zeitverlauf'),
       ('Design', 'Studiendesign'), ('Niveau', 'Population oder Niveau'), ('Population', 'Population oder Niveau'),
       ('Vergleich', 'Trainingsform'), ('Trainingsform', 'Trainingsform')]
NAME = {'Lloyd 2016': 'Lloyd2016', 'Hammami 2016': 'Hammami2016', 'Beato 2018': 'Beato2018', 'Negra 2019': 'Negra2019',
        'Negra 2020': 'Negra2020', 'Aloui 2022': 'Aloui2022', 'Liu 2024': 'Liu2024', 'Moran 2024': 'Moran2024',
        'Sammoud 2024': 'Sammoud2024', 'Bouafif 2026': 'Bouafif2026'}
kat_studien = collections.defaultdict(list)
anz = {}
for zeile in anhc.splitlines():
    teile = [t.strip() for t in zeile.strip().strip('|').split('|')]
    if len(teile) < 3 or teile[0] not in NAME:
        continue
    s = NAME[teile[0]]
    dims = [d.strip() for d in teile[2].split(' · ')]
    anz[s] = len(dims)
    nicht_l = []
    for d in dims:
        kat = next(k for key, k in KAT if key in d)
        if s not in kat_studien[kat]:
            kat_studien[kat].append(s)
        for bez in re.findall(r'(\d+\.\d+)(?:–(\d+\.\d+))?', d):
            a, b = bez
            nrs = [x['satz'] for x in by[s]]
            if b and a in nrs and b in nrs:
                spanne = nrs[nrs.index(a):nrs.index(b) + 1]
            else:
                spanne = [a]
            for nr in spanne:
                r = satz(s, nr)
                if not (hat(r, 'K', 'L1') or hat(r, 'K', 'L2')):
                    nicht_l.append('%s %s(%s)' % (nr, r['primaer'], r['sekundaer']))
    w('  %-12s %d Dimensionen · zitierte Sätze ohne Lückencode: %s' % (s, len(dims), ', '.join(sorted(set(nicht_l))) or '—'))
zwei_drei = [s for s in CORE if anz.get(s) in (2, 3)]
w('d8 Zwei oder drei Dimensionen: %d: %s · vier: %s · fünf: %s' % (
    len(zwei_drei), ', '.join(zwei_drei), ', '.join(s for s in CORE if anz.get(s) == 4) or '—', ', '.join(s for s in CORE if anz.get(s) == 5) or '—'))
w('d8 Studien je Dimension: ' + ' · '.join('%s %d (%s)' % (k, len(v), ', '.join(v)) for k, v in sorted(kat_studien.items(), key=lambda x: -len(x[1]))))
# d9 Anteile nach Wörtern und Primärcode
w('d9 Anteile je Gruppe am Kernkorpus (Wörter der Sätze nach Primärcode, Median und Spanne über 10 Studien):')
anteile = collections.defaultdict(dict)
for s in CORE:
    ges = sum(int(r['woerter']) for r in by[s])
    for g in 'RTEKDLZ':
        anteile[g][s] = 100.0 * sum(int(r['woerter']) for r in by[s] if r['primaer'][0] == g) / ges
for g in 'RTEKDLZ':
    v = list(anteile[g].values())
    w('  %s Median %.1f %% (%.1f bis %.1f) · %s' % (g, statistics.median(v), min(v), max(v),
                                                    ', '.join('%s %.1f' % (s, anteile[g][s]) for s in CORE)))
# d7 Einführungssätze im Wortlaut
w('d7 Einführungssätze (Lesart ii, Konsens):')
for s in CORE:
    t1 = satz(s, EINF[s])
    w('  %-12s %s %s(%s): %s' % (s, t1['satz'], t1['primaer'], t1['sekundaer'], t1['text'][:200]))
open(os.path.join(HIER, 'nachzaehlung_2d.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))

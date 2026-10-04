# -*- coding: utf-8 -*-
"""
schritt4_abschluss.py — Schritt 4, Abschluss: die ganze Einleitung im freigegebenen Wortlaut neu codieren und messen (30.09.2026)

Freigegebener Stand aus schritt4_stand.json (B1b Klick 18:02, B3 Klick 18:46, B4 Klick 19:45, B1a, B2 und B5 wortgleich mit dem
Textstand T). Codierung nach codebook.md (Fassung 1): unveränderte Sätze mit dem Konsens aus konsens_T.py (Befund Anhang A),
geänderte Sätze nach den Zug-Tabellen des Textvorschlags (§ 1.3, § 2.3, § 3.3), dort je vom unabhängigen Zweitprüfer geprüft.
B4 hat nach der Teilung von T S1 sieben statt sechs Sätze: S1 K1 (aus T S1), S2 K1 (E2) neu, S3 bis S7 mit den Codes von T S2 bis S6.
Profil, Anteile, Zugfolge, Grundfigur und erstes Auftreten wie abgleich_2a.py (Wörter als Leerraum-Token mit Belegklammern,
Anteile als Wortanteil der Primärcodes), für T und für den freigegebenen Stand nebeneinander, dazu der Korpus der zehn Kern-RCTs.
Aufruf im Ordner: python schritt4_abschluss.py [<Anlage Argumentationsstruktur_Einleitungen_2026-09-30>]
Schreibt schritt4_abschluss.txt und schritt4_abschluss.json. Ohne Semikolon (chr(59)).
"""
import json, os, re, sys, collections, statistics as st

HIER = os.path.dirname(os.path.abspath(__file__))
STAGING = '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Abgleich_Einleitung_2026-09-30'
for ort in (HIER, STAGING):
    if os.path.isfile(os.path.join(ort, 'konsens_T.py')):
        sys.path.insert(0, ort)
        break
from konsens_T import K  # Konsens des Textstands T (Befund Anhang A)

_ANL = os.path.normpath(os.path.join(HIER, '..', 'Argumentationsstruktur_Einleitungen_2026-09-30'))
ANL = sys.argv[1] if len(sys.argv) > 1 else (_ANL if os.path.isdir(_ANL) else
                                             '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Argumentationsstruktur_Einleitungen_2026-09-30')
SEMI = chr(59)
ORDER = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']


def lade(name):
    for ort in (HIER, STAGING):
        p = os.path.join(ort, name)
        if os.path.exists(p):
            return json.load(open(p, encoding='utf-8'))['absaetze']
    raise FileNotFoundError(name)


def saetze(text):  # unverändert aus Manuskriptstand_2026-09-25.py (Fassung 3)
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', text)
    t = re.sub(r'\b(et al|Abschn|Tab|Abb|vgl|bzw|ca|Nr|Aufl|Hrsg|Jg)\.', r'\1<P>', t)
    t = re.sub(r'\b([A-Z])\.\s', r'\1<P> ', t)
    t = re.sub(r'\bS\.\s', 'S<P> ', t)
    t = re.sub(r'\b(u|z|d)\.\s?(a|B|h)\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})', r'\1<P>\2<P>\3', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d)\.\s', r'\1<P> ', t)
    teile = [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(⟨])', t) if s.strip()]
    return [s.replace('<P>', '.') for s in teile]


KL = re.compile(r'\([^()]*\d{4}[^()]*\)')
T = {k: saetze(v) for k, v in lade('textstand_T.json').items()}
V = {k: saetze(v) for k, v in lade('textstand_V.json').items()}
N = {k: saetze(v) for k, v in lade('schritt4_stand.json').items()}

# Prüfungen des freigegebenen Stands gegen die Freigaben
for k in ('B1a', 'B2', 'B5'):
    assert N[k] == T[k], k + ' ist nicht wortgleich mit dem Textstand'
assert N['B1b'] == V['B1b'], 'B1b weicht von der Freigabe ab (Textvorschlag B1 § 1.2)'
assert N['B3'][:4] == T['B3'][:4] and 'und valide' not in N['B3'][4] and 'Ferguson' not in N['B3'][4], 'B3'
assert N['B4'][:2] == V['B4'][:2] and N['B4'][3:] == T['B4'][2:] and 'wozu eine verbesserte Funktion des DVZ' in N['B4'][2], 'B4'
for k in ORDER:
    assert len(T[k]) == len(K[k]), k

# Codierung des freigegebenen Stands
KN = {k: list(K[k]) for k in ORDER}
KN['B4'] = [K['B4'][0], ('K1', 'E2'), K['B4'][1]] + K['B4'][2:]  # T S1 geteilt, S2 neu (Zug-Tabelle § 3.3)
for k in ORDER:
    assert len(KN[k]) == len(N[k]), k
assert KN['B4'][2] == ('K1', 'T2') and KN['B4'][6][0] == 'L1'


def sek(s):
    return set(x for x in s.split(SEMI) if x)


def profil(S, C):
    R = []
    for p_i, k in enumerate(ORDER, 1):
        for i, s in enumerate(S[k]):
            R.append(dict(absatz=p_i, blk=k, satz=i + 1, w=len(s.split()), beleg=int(bool(KL.search(s))), p=C[k][i][0], sec=C[k][i][1], text=s))
    W = sum(r['w'] for r in R)
    gw = collections.Counter()
    for r in R:
        gw[r['p'][0]] += r['w']
    seq = []
    for r in R:
        if not seq or seq[-1] != r['p'][0]:
            seq.append(r['p'][0])
    cum, first, firstsent = 0, {}, {}
    for r in R:
        for c in [r['p']] + sorted(sek(r['sec'])):
            if c not in first:
                first[c] = cum / W
                firstsent[c] = '%s S%d' % (r['blk'], r['satz'])
        cum += r['w']
    pdom = []
    for a in range(1, len(ORDER) + 1):
        c = collections.Counter()
        for r in R:
            if r['absatz'] == a:
                c[r['p'][0]] += r['w']
        pdom.append(c.most_common(1)[0][0])
    pres = set()
    for r in R:
        pres.add(r['p'])
        pres.update(sek(r['sec']))
    return dict(R=R, W=W, P=len(ORDER), S=len(R), med=st.median([r['w'] for r in R]), beleg=sum(r['beleg'] for r in R) / len(R),
                anteil={g: gw[g] / W for g in 'RTEKDLZ'}, seq=' '.join(seq), pdom=' '.join(pdom), first=first, firstsent=firstsent, pres=pres)


def grundfigur(P):
    R_ = P['R']
    zi = next(i for i, r in enumerate(R_) if r['p'] == 'Z1')
    z1, vor = R_[zi], R_[zi - 1]
    folg = bool(re.match(r'^(Ziel der Studie war es deshalb|Deshalb|Daher|Somit|Folglich)', z1['text'])) or ' deshalb ' in z1['text'][:40]
    fL = next(i for i, r in enumerate(R_) if r['p'][0] == 'L' or any(c.startswith('L') for c in sek(r['sec'])))
    fLp = next(i for i, r in enumerate(R_) if r['p'][0] == 'L')
    fT = next(i for i, r in enumerate(R_) if r['p'][0] == 'T' or any(c.startswith('T') for c in sek(r['sec'])))
    fR = next(i for i, r in enumerate(R_) if r['p'][0] == 'R' or any(c.startswith('R') for c in sek(r['sec'])))
    fK = next(i for i, r in enumerate(R_) if r['p'][0] == 'K' or any(c.startswith('K') for c in sek(r['sec'])))
    t1 = next(r for r in R_ if r['p'] == 'T1' or 'T1' in sek(r['sec']))
    lastL = [i for i, r in enumerate(R_[:zi]) if r['p'] == 'L1' or 'L1' in sek(r['sec'])][-1]
    ort = lambda i: '%s S%d' % (R_[i]['blk'], R_[i]['satz'])
    return [
        ('Einleitung endet mit Lücke → Zweck', '10 von 10', 'ja' if P['seq'].endswith('L Z') else 'nein'),
        ('Zwecksatz als Folgerung markiert', '10 von 10', 'ja' if folg else 'nein'),
        ('Satz vor dem Zwecksatz ist Lücken- oder Bedeutungssatz', '10 von 10', 'ja (%s, %s)' % (ort(zi - 1), vor['p']) if vor['p'] in ('L1', 'L2') else 'nein'),
        ('Eröffnung mit Relevanz oder Problem', '9 von 10', 'ja (%s)' % R_[0]['p'] if R_[0]['p'][0] == 'R' else 'nein'),
        ('Lücke und Zweck im selben Absatz', '8 von 10', 'ja' if R_[lastL]['absatz'] == z1['absatz'] else 'nein (letzter Lückensatz %s, Zweck %s)' % (ort(lastL), ort(zi))),
        ('Relevanz → Trainingsmittel → Lücke → Zweck nach erstem Auftreten', '7 von 10', 'ja' if fR < fT < fL < zi else 'nein'),
        ('Kontext zwischen Trainingsmittel und Lücke (erstes Auftreten)', '4 von 10', 'ja (erstes K %s, erstes L %s)' % (ort(fK), ort(fL)) if fT < fK < fL else 'nein'),
        ('Kontext zwischen Trainingsmittel und Lücke (erster L-Primärsatz)', 'Lesart zu § 2.1', 'ja (%s)' % ort(fLp) if fT < fK < fLp else 'nein'),
        ('Trainingsmittel im ersten oder zweiten Absatz eingeführt', '7 von 10', 'ja (%s S%d)' % (t1['blk'], t1['satz']) if t1['absatz'] <= 2 else 'nein'),
        ('Einführung im selben Satz begründet', '10 von 10', 'ja (%s mit %s)' % (t1['p'], t1['sec']) if sek(t1['sec']) & {'E1', 'T3', 'T2'} else 'nein'),
        ('Schluss mit Hypothese', '7 von 10', 'ja' if R_[-1]['p'] == 'Z3' else 'nein'),
    ]


PT, PN = profil(T, K), profil(N, KN)
summ = json.load(open(os.path.join(ANL, 'summary.json'), encoding='utf-8'))
CORE = ['Lloyd2016', 'Hammami2016', 'Beato2018', 'Negra2019', 'Negra2020', 'Aloui2022', 'Liu2024', 'Moran2024', 'Sammoud2024', 'Bouafif2026']
C = [summ[s] for s in CORE]
de = lambda x, n=1: ('%.*f' % (n, x)).replace('.', ',')


def spanne(xs):
    return min(xs), st.median(xs), max(xs)


def lage(x, lo, hi):
    return 'in der Spanne' if lo - 1e-9 <= x <= hi + 1e-9 else ('über' if x > hi else 'unter') + ' der Spanne'


out = []
w = out.append
w('Schritt 4, Abschluss (30.09.2026): Einleitung im freigegebenen Wortlaut, neu codiert und gemessen')
w('Freigaben: B1b 18:02 (P1, P9) · B3 18:46 (P2, S5 ohne Ferguson et al., 2024) · B4 19:45 (P3b, P4c) · B1a, B2, B5 wortgleich (Assertionen)')
w('')
w('Umfang: T (Textstand) · freigegebener Stand · Korpus 10 Kern-RCTs Minimum, Median, Maximum · Lage des freigegebenen Stands')
for name, key, fmt in [('Wörter', 'W', 0), ('Absätze', 'P', 0), ('Sätze', 'S', 0), ('Satzlänge Median', 'med', 1)]:
    lo, me, hi = spanne([v[key] for v in C])
    w('  %-18s T %s · neu %s · Korpus %s, %s, %s · %s' % (name, de(PT[key], fmt), de(PN[key], fmt), de(lo, fmt), de(me, fmt), de(hi, fmt), lage(PN[key], lo, hi)))
lo, me, hi = spanne([v['beleg'] for v in C])
w('  %-18s T %s %% · neu %s %% · Korpus %s, %s, %s %% · %s' % ('Sätze mit Beleg', de(PT['beleg'] * 100), de(PN['beleg'] * 100), de(lo * 100), de(me * 100), de(hi * 100), lage(PN['beleg'], lo, hi)))
w('')
w('Anteile nach Primärcode (Wortanteil in %): T · neu · Korpus Minimum, Median, Maximum · Lage neu')
for g in 'RTEKDLZ':
    lo, me, hi = spanne([v['anteil'][g] for v in C])
    w('  %s  %5s %5s · %5s %5s %5s · %s' % (g, de(PT['anteil'][g] * 100), de(PN['anteil'][g] * 100), de(lo * 100), de(me * 100), de(hi * 100), lage(PN['anteil'][g], lo, hi)))
w('')
w('Zugfolge T:   ' + PT['seq'])
w('Zugfolge neu: ' + PN['seq'])
w('Absatzdominanz T: ' + PT['pdom'] + ' · neu: ' + PN['pdom'] + ' (B1a B1b B2 B3 B4 B5)')
w('')
w('Grundfigur (Befund Argumentationsstruktur § 2.1, § 3, § 5.3): Korpus · T · neu')
for (a, b, c), (_, _, d) in zip(grundfigur(PT), grundfigur(PN)):
    w('  %-66s Korpus %-16s T: %-44s neu: %s' % (a, b, c, d))
w('')
w('Erstes Auftreten (relative Wortposition und Satz): T · neu · Korpusmedian der Studien mit dem Code')
for c in ['R1', 'R2', 'R3', 'T1', 'T2', 'T3', 'T4', 'E1', 'E2', 'E3', 'K1', 'K2', 'K3', 'K4', 'D1', 'L1', 'L2', 'Z1', 'Z2', 'Z3']:
    pos = [summ[s]['first'][c] for s in CORE if c in summ[s]['first']]
    f = lambda P: ('%s (%s)' % (de(P['first'][c], 2), P['firstsent'][c])) if c in P['first'] else '—'
    w('  %-3s T %-16s · neu %-16s · Korpus n=%2d, Median %s' % (c, f(PT), f(PN), len(pos), de(st.median(pos), 2) if pos else '—'))
w('')
w('Vorkommen (Primär oder Sekundär): Funktionen, die zwischen T und neu wechseln: ' + (', '.join(sorted(PT['pres'] ^ PN['pres'])) or 'keine'))
w('')
w('Satz | Wörter | Beleg | Code (neu) | geändert gegenüber T')
geaendert = {('B1b', 1): 'P1', ('B1b', 7): 'P9', ('B3', 5): 'P2 und Klick § 2.7 a', ('B4', 1): 'P3b (ersetzt T S1)',
             ('B4', 2): 'P3b (neu, Beleg aus T S1)', ('B4', 3): 'P4c (T S2)'}
for r in PN['R']:
    key = (r['blk'], r['satz'])
    w('%s S%d | %d | %d | %s%s | %s' % (r['blk'], r['satz'], r['w'], r['beleg'], r['p'], (' (' + r['sec'].replace(SEMI, ', ') + ')') if r['sec'] else '',
                                        geaendert.get(key, '—')))
open(os.path.join(HIER, 'schritt4_abschluss.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump({'codes_neu': {k: KN[k] for k in ORDER}, 'anteile_T': PT['anteil'], 'anteile_neu': PN['anteil'], 'seq_T': PT['seq'], 'seq_neu': PN['seq'],
           'pdom_T': PT['pdom'], 'pdom_neu': PN['pdom'], 'W_T': PT['W'], 'W_neu': PN['W'], 'S_neu': PN['S'], 'beleg_neu': PN['beleg'],
           'first_neu': PN['first'], 'firstsent_neu': PN['firstsent']},
          open(os.path.join(HIER, 'schritt4_abschluss.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(out))

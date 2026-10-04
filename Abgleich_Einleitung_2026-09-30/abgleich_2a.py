# -*- coding: utf-8 -*-
"""
abgleich_2a.py — Schritt 2 (a): Codierung des Textstands T, Übereinstimmung A/B, Konsens, Zugfolge, Anteile und
Reihenfolge gegen den Korpus (Befund Argumentationsstruktur § 2 und § 5). Zählweise wie analyse.py und eigen.py der
Anlage zum Befund: Wörter als Leerraum-Token mit Belegklammern, Anteile als Wortanteil der Primärcodes, Vorkommen mit
Primär- oder Sekundärcode, Erstauftreten als relative Wortposition. Ohne Semikolon außerhalb von Zeichenketten.
Aufruf im Ordner: python abgleich_2a.py <Pfad zur Anlage Argumentationsstruktur_Einleitungen_2026-09-30>
"""
import json, os, re, sys, collections, statistics as st
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from codes_A_T import A
from konsens_T import K, ENTSCHEID
_ANL = os.path.normpath(os.path.join(HIER, '..', 'Argumentationsstruktur_Einleitungen_2026-09-30'))
ANL = sys.argv[1] if len(sys.argv) > 1 else (_ANL if os.path.isdir(_ANL) else '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Argumentationsstruktur_Einleitungen_2026-09-30')
TPFAD = os.path.join(HIER, 'textstand_T.json')
if not os.path.isfile(TPFAD):
    TPFAD = '/home/claude/abgleich/s1/textstand_T.json'
SEMI = chr(59)
B_raw = json.load(open(os.path.join(HIER, 'codes_B_T.json'), encoding='utf-8'))
B = {k: [(p, s) for _, p, s in v] for k, v in B_raw.items()}
T = json.load(open(TPFAD, encoding='utf-8'))['absaetze']
ORDER = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']


def saetze(text):  # wie Manuskriptstand_2026-09-25.py
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
S = {k: saetze(T[k]) for k in ORDER}
for k in ORDER:
    assert len(S[k]) == len(A[k]) == len(B[k]) == len(K[k]), k


def sek(s):
    return set(x for x in s.split(SEMI) if x)


# 1 Übereinstimmung
def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / n / n
    return po, (po - pe) / (1 - pe)


pairs = [(A[k][i][0], B[k][i][0]) for k in ORDER for i in range(len(A[k]))]
po, ka = kappa(pairs)
pg, kg = kappa([(a[0], b[0]) for a, b in pairs])
sek_gleich = sum(sek(A[k][i][1]) == sek(B[k][i][1]) for k in ORDER for i in range(len(A[k])))
abw = [(k, i + 1) for k in ORDER for i in range(len(A[k])) if A[k][i][0] != B[k][i][0] or sek(A[k][i][1]) != sek(B[k][i][1])]
assert set(abw) == set(ENTSCHEID), (sorted(set(abw) ^ set(ENTSCHEID)))
out = []
w = out.append
n = len(pairs)
w('Übereinstimmung A/B (39 Sätze): Primärcode %d von %d (%s %%), kappa %s · Gruppe %d von %d (%s %%), kappa %s · Sekundärcodes gleich %d von %d (%s %%)' % (
    sum(a == b for a, b in pairs), n, round(po * 100, 1), round(ka, 2), sum(a[0] == b[0] for a, b in pairs), n,
    round(pg * 100, 1), round(kg, 2), sek_gleich, n, round(sek_gleich / n * 100, 1)))
w('Abweichungen: %d Sätze, davon Primärcode %d, nur Sekundärcode %d, entschieden nach A %d, nach B %d' % (
    len(abw), sum(A[k][i - 1][0] != B[k][i - 1][0] for k, i in abw), sum(A[k][i - 1][0] == B[k][i - 1][0] for k, i in abw),
    sum(ENTSCHEID[x][2].startswith('A') for x in abw), sum(ENTSCHEID[x][2].startswith('B') for x in abw)))
w('')


# 2 Profil wie analyse.py
def profil(C):
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


PK, PA, PB = profil(K), profil(A), profil(B)
summ = json.load(open(os.path.join(ANL, 'summary.json'), encoding='utf-8'))
CORE = ['Lloyd2016', 'Hammami2016', 'Beato2018', 'Negra2019', 'Negra2020', 'Aloui2022', 'Liu2024', 'Moran2024', 'Sammoud2024', 'Bouafif2026']
C = [summ[s] for s in CORE]
de = lambda x, n=1: ('%.*f' % (n, x)).replace('.', ',')


def spanne(xs):
    return min(xs), st.median(xs), max(xs)


w('Umfang (Korpus 10 Kern-RCTs: Minimum, Median, Maximum):')
for name, key, fmt in [('Wörter', 'W', 0), ('Absätze', 'P', 0), ('Sätze', 'S', 1), ('Satzlänge Median', 'med', 1)]:
    lo, me, hi = spanne([v[key] for v in C])
    w('  %-18s T %s · Korpus %s, %s, %s · %s' % (name, de(PK[key], fmt), de(lo, fmt), de(me, fmt), de(hi, fmt),
                                                 'in der Spanne' if lo <= PK[key] <= hi else ('über' if PK[key] > hi else 'unter') + ' der Spanne'))
lo, me, hi = spanne([v['beleg'] for v in C])
w('  %-18s T %s %% · Korpus %s, %s, %s %% · %s' % ('Sätze mit Beleg', de(PK['beleg'] * 100), de(lo * 100), de(me * 100), de(hi * 100),
                                                   'in der Spanne' if lo <= PK['beleg'] <= hi else 'außerhalb'))
w('')
w('Anteile nach Primärcode (Wortanteil in %): T Konsens · T nur A · T nur B · Korpus Minimum, Median, Maximum · Lage · Befund § 5.2 (Stand B2 Fassung 2)')
BEF = {'R': '10', 'T': '28', 'E': '6,8', 'K': '24', 'D': '14', 'L': '6', 'Z': '11'}
for g in 'RTEKDLZ':
    xs = [v['anteil'][g] for v in C]
    lo, me, hi = spanne(xs)
    x = PK['anteil'][g]
    lage = 'in der Spanne' if lo - 1e-9 <= x <= hi + 1e-9 else ('über' if x > hi else 'unter') + ' der Spanne'
    w('  %s  %5s %5s %5s · %5s %5s %5s · %-16s · %s' % (g, de(x * 100), de(PA['anteil'][g] * 100), de(PB['anteil'][g] * 100),
                                                  de(lo * 100), de(me * 100), de(hi * 100), lage, BEF[g]))
w('')
w('Zugfolge (Primärgruppen zusammengefasst): ' + PK['seq'])
w('Absatzdominanz: ' + PK['pdom'] + ' (B1a B1b B2 B3 B4 B5)')
w('Zugfolgen im Korpus (Befund § 2.1): ' + ' | '.join('%s %s' % (s[:-4], summ[s]['seq']) for s in CORE))
w('')


# 3 Prüfungen der Grundfigur (Befund § 2.1, § 3, § 5.3)
R_ = PK['R']
zi = next(i for i, r in enumerate(R_) if r['p'] == 'Z1')
z1 = R_[zi]
vor = R_[zi - 1]
folg = bool(re.match(r'^(Ziel der Studie war es deshalb|Deshalb|Daher|Somit|Folglich)', z1['text'])) or ' deshalb ' in z1['text'][:40]
firstL_i = next(i for i, r in enumerate(R_) if r['p'][0] == 'L' or any(c.startswith('L') for c in sek(r['sec'])))
firstLprim_i = next(i for i, r in enumerate(R_) if r['p'][0] == 'L')
firstT_i = next(i for i, r in enumerate(R_) if r['p'][0] == 'T' or any(c.startswith('T') for c in sek(r['sec'])))
firstR_i = next(i for i, r in enumerate(R_) if r['p'][0] == 'R' or any(c.startswith('R') for c in sek(r['sec'])))
firstZ_i = zi
firstK_i = next(i for i, r in enumerate(R_) if r['p'][0] == 'K' or any(c.startswith('K') for c in sek(r['sec'])))
t1 = next(r for r in R_ if r['p'] == 'T1' or 'T1' in sek(r['sec']))
last_L = [i for i, r in enumerate(R_[:zi]) if r['p'] == 'L1' or 'L1' in sek(r['sec'])][-1]
checks = [
    ('Einleitung endet mit Lücke → Zweck', '10 von 10', 'ja' if PK['seq'].endswith('L Z') else 'nein (Folge endet ' + PK['seq'][-5:] + ')'),
    ('Zwecksatz als Folgerung markiert', '10 von 10', 'ja („deshalb“, B5 S1)' if folg else 'nein'),
    ('Satz vor dem Zwecksatz ist Lücken- oder Bedeutungssatz', '10 von 10 (8 L, 2 L2)', 'ja (%s S%d, %s)' % (vor['blk'], vor['satz'], vor['p']) if vor['p'] in ('L1', 'L2') else 'nein (%s)' % vor['p']),
    ('Eröffnung mit Relevanz oder Problem', '9 von 10', 'ja (%s)' % R_[0]['p'] if R_[0]['p'][0] == 'R' else 'nein (%s)' % R_[0]['p']),
    ('Lücke und Zweck im selben Absatz', '8 von 10', 'ja' if R_[last_L]['absatz'] == z1['absatz'] else 'nein (letzter Lückensatz %s S%d, Zweck %s S%d)' % (R_[last_L]['blk'], R_[last_L]['satz'], z1['blk'], z1['satz'])),
    ('Relevanz → Trainingsmittel → Lücke → Zweck nach erstem Auftreten', '7 von 10 (beide Codierungen)', 'ja' if firstR_i < firstT_i < firstL_i < firstZ_i else 'nein'),
    ('Kontext zwischen Trainingsmittel und Lücke (erstes Auftreten)', '4 von 10 (B: 3)', 'ja (erstes K %s S%d, erstes L %s S%d)' % (R_[firstK_i]['blk'], R_[firstK_i]['satz'], R_[firstL_i]['blk'], R_[firstL_i]['satz']) if firstT_i < firstK_i < firstL_i else 'nein (erstes K %s S%d, erstes L %s S%d)' % (R_[firstK_i]['blk'], R_[firstK_i]['satz'], R_[firstL_i]['blk'], R_[firstL_i]['satz'])),
    ('Kontext zwischen Trainingsmittel und Lücke (erster Lückensatz mit Primärcode)', 'Lesart zu § 2.1', 'ja (erster L-Primärsatz %s S%d)' % (R_[firstLprim_i]['blk'], R_[firstLprim_i]['satz']) if firstT_i < firstK_i < firstLprim_i else 'nein'),
    ('Trainingsmittel im ersten oder zweiten Absatz eingeführt', '7 von 10', 'ja (%s S%d, Absatz %d)' % (t1['blk'], t1['satz'], t1['absatz']) if t1['absatz'] <= 2 else 'nein'),
    ('Einführung im selben Satz begründet', '10 von 10', 'ja (%s mit %s)' % (t1['p'], t1['sec']) if sek(t1['sec']) & {'E1', 'T3', 'T2'} else 'nein'),
    ('Schluss mit Hypothese', '7 von 10', 'ja' if R_[-1]['p'] == 'Z3' else 'nein'),
]
w('Grundfigur (Befund § 2.1, § 3, § 5.3), Konsens:')
for a, b, c in checks:
    w('  %-78s Korpus %-26s T: %s' % (a, b, c))
w('')
w('Erstes Auftreten (Konsens), relative Wortposition und Satz, Korpusmedian der Studien mit dem Code:')
for c in ['R1', 'R2', 'R3', 'T1', 'T2', 'T3', 'T4', 'E1', 'E2', 'E3', 'K1', 'K2', 'K3', 'K4', 'D1', 'L1', 'L2', 'Z1', 'Z2', 'Z3']:
    pos = [summ[s]['first'][c] for s in CORE if c in summ[s]['first']]
    t = ('%s (%s)' % (de(PK['first'][c], 2), PK['firstsent'][c])) if c in PK['first'] else '—'
    w('  %-3s T %-18s · Korpus n=%2d, Median %s' % (c, t, len(pos), de(st.median(pos), 2) if pos else '—'))
w('')
w('Vorkommen je Funktion (Primär oder Sekundär) im Textstand, Konsens · A · B · Korpus (Studien, Befund § 2.2):')
KV = {c: sum(1 for s in CORE if c in summ[s]['pres']) for c in ['R1', 'R2', 'R3', 'T1', 'T2', 'T3', 'T4', 'E1', 'E2', 'E3', 'K1', 'K2', 'K3', 'K4', 'D1', 'L1', 'L2', 'Z1', 'Z2', 'Z3']}
for c in KV:
    satzK = [('%s S%d' % (r['blk'], r['satz'])) for r in PK['R'] if r['p'] == c or c in sek(r['sec'])]
    w('  %-3s %s · %s · %s · Korpus %d von 10 · %s' % (c, 'ja' if c in PK['pres'] else 'nein', 'ja' if c in PA['pres'] else 'nein',
                                                   'ja' if c in PB['pres'] else 'nein', KV[c], ', '.join(satzK) if satzK else '—'))
w('')
# Lesarten
LES = {}
for name, aend in [('B2 S2 als K2 (Codierung A)', {('B2', 2): 'K2'}), ('B2 S9 als E2', {('B2', 9): 'E2'}), ('B4 S4 als E1', {('B4', 4): 'E1'})]:
    C2 = {k: list(v) for k, v in K.items()}
    for (blk, nn), p in aend.items():
        C2[blk][nn - 1] = (p, C2[blk][nn - 1][1])
    LES[name] = profil(C2)['anteil']
w('Lesarten (Anteile in %, R T E K D L Z):')
for name, an in LES.items():
    w('  %-28s ' % name + ' · '.join('%s %s' % (g, de(an[g] * 100)) for g in 'RTEKDLZ'))
w('')
# Tabelle je Satz
w('Satz | Wörter | Beleg | A | B | Konsens | Entscheidung')
for r in PK['R']:
    key = (r['blk'], r['satz'])
    a = A[r['blk']][r['satz'] - 1]
    b = B[r['blk']][r['satz'] - 1]
    ent = ENTSCHEID.get(key, (None, None, 'übereinstimmend'))[2]
    w('%s S%d | %d | %d | %s%s | %s%s | %s%s | %s' % (r['blk'], r['satz'], r['w'], r['beleg'], a[0], (' (' + a[1] + ')') if a[1] else '',
                                                    b[0], (' (' + b[1] + ')') if b[1] else '', r['p'], (' (' + r['sec'] + ')') if r['sec'] else '', ent))
open(os.path.join(HIER, 'abgleich_2a.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump({'konsens': {k: K[k] for k in ORDER}, 'A': {k: A[k] for k in ORDER}, 'B': {k: B[k] for k in ORDER},
           'anteile_konsens': PK['anteil'], 'seq': PK['seq'], 'pdom': PK['pdom'], 'first': PK['first'], 'firstsent': PK['firstsent'],
           'W': PK['W'], 'S': PK['S'], 'beleg': PK['beleg']}, open(os.path.join(HIER, 'abgleich_2a.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(out))

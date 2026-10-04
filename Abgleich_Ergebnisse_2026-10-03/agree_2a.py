# -*- coding: utf-8 -*-
"""
agree_2a.py — Übereinstimmung der Codierungen A und B des Textstands von Kapitel 5, Schritt 2 (a), 03.10.2026

Primärcode (Anteil und Cohens Kappa wie agree.py des Korpus), Codegruppe (O, V, X, B, Z), Sekundärcodes (gleiche Menge),
zg und deutung, für alle 29 Sätze und getrennt für die Sätze, die ein Anwendungshinweis der Übergabe § 5 Nr. 3 erfasst
(HINWEIS in konsens_2a.py), und die übrigen. Dazu Konsens gegen A und B und Konsens gegen die Fassung nach den Hinweisen.
Aufruf: python agree_2a.py [<Ausgabe.txt>]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import json
import pathlib
import collections

B_ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(B_))
from codes_A import A
from konsens_2a import K, KH, HINWEIS, HINWEISTEXT, ORDNUNG

BJ = json.load(open(B_ / 'blind' / 'codes_B.json', encoding='utf-8'))
B = {s: (v['primaer'], v['sekundaer'], v['zg'], v['deutung']) for s, v in BJ.items()}
assert set(A) == set(B) == set(K), 'Satzlisten verschieden'


def kappa(pairs):
    """wie agree.py des Korpus"""
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = collections.Counter(a for a, _ in pairs)
    cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in set(ca) | set(cb)) / n / n
    return po, ((po - pe) / (1 - pe) if pe < 1 else float('nan'))


def zeile(name, X, Y, saetze):
    pr = [(X[s][0], Y[s][0]) for s in saetze]
    po, k = kappa(pr)
    gr = sum(X[s][0][0] == Y[s][0][0] for s in saetze)
    sek = sum(set(X[s][1]) == set(Y[s][1]) for s in saetze)
    zg = sum(X[s][2] == Y[s][2] for s in saetze)
    de = sum(X[s][3] == Y[s][3] for s in saetze)
    n = len(saetze)
    return (f'{name:44} n {n:>2} | Primär {sum(a == b for a, b in pr):>2} ({po * 100:5.1f} %, κ {k:5.3f}) | '
            f'Gruppe {gr:>2} | Sekundär {sek:>2} ({sek / n * 100:5.1f} %) | zg {zg:>2} | deutung {de:>2}')


ALLE = ORDNUNG
HIN = [s for s in ALLE if s in HINWEIS]
UEB = [s for s in ALLE if s not in HINWEIS]
out = []
P = out.append
P('Übereinstimmung A gegen B, Textstand Kapitel 5 (29 Sätze), Codebuch Fassung 2 ohne Anwendungshinweise')
P('A: codes_A.py (Ersteller, vor Kenntnis von B festgelegt) · B: blind/codes_B.json (unabhängiger Subagent, nur Codebuch und Textstand)')
P('')
P(zeile('alle Sätze', A, B, ALLE))
P(zeile('von einem Hinweis erfasst', A, B, HIN))
P(zeile('von keinem Hinweis erfasst', A, B, UEB))
P('')
P('Abweichungen beim Primärcode:')
for s in ALLE:
    if A[s][0] != B[s][0]:
        P(f'  {s}: A {A[s][0]} {"+".join(A[s][1]) or "—"} | B {B[s][0]} {"+".join(B[s][1]) or "—"} | Konsens {K[s][0]} {"+".join(K[s][1]) or "—"} | Hinweise {"+".join(HINWEIS.get(s, [])) or "—"}')
P('Abweichungen nur bei den Sekundärcodes:')
for s in ALLE:
    if A[s][0] == B[s][0] and set(A[s][1]) != set(B[s][1]):
        P(f'  {s}: A {"+".join(A[s][1]) or "—"} | B {"+".join(B[s][1]) or "—"} | Konsens {"+".join(K[s][1]) or "—"}')
P('')
P('Konsens (nach Codebuch) gegen die Codierer:')
P(zeile('Konsens gegen A', K, A, ALLE))
P(zeile('Konsens gegen B', K, B, ALLE))
P('')
P('Fassung nach den Hinweisen gegen den Konsens nach Codebuch:')
P(zeile('Hinweis gegen Konsens, alle', KH, K, ALLE))
P(zeile('Hinweis gegen Konsens, erfasste Sätze', KH, K, HIN))
P(zeile('A gegen Fassung nach Hinweisen', A, KH, ALLE))
P(zeile('B gegen Fassung nach Hinweisen', B, KH, ALLE))
P('')
P('Von den Hinweisen erfasste Sätze und Code nach Codebuch gegen Code nach Hinweis:')
for s in HIN:
    kh = KH[s]
    k = K[s]
    mark = '' if (kh[0], kh[1]) == (k[0], k[1]) else '  ← anders'
    P(f'  {s:6} {"+".join(HINWEIS[s]):9} Codebuch {k[0]} {"+".join(k[1]) or "—":7} | Hinweis {kh[0]} {"+".join(kh[1]) or "—":7}{mark}')
P('')
P('Wortlaut der Hinweise (Übergabe § 5 Nr. 3):')
for h, t in HINWEISTEXT.items():
    P(f'  {h}: {t}')
aus = sys.argv[1] if len(sys.argv) > 1 else str(B_ / 'agree_2a.txt')
open(aus, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))

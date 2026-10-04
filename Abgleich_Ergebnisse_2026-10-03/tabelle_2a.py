# -*- coding: utf-8 -*-
"""
tabelle_2a.py — Anhang A des Abgleichbefunds (Codierung des Textstands) als Markdown-Tabelle, Schritt 2 (a), 03.10.2026

Liest codes_A.py, blind/codes_B.json, konsens_2a.py und textstand.json und schreibt anhang_a_2a.md. Der Befund übernimmt
die Tabelle unverändert in Anhang A. Codes als „Primär (Sekundär)“, „—“ ohne Sekundärcode.
Aufruf: python tabelle_2a.py [<textstand.json> <Ausgabe.md>]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import json
import pathlib

B_ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(B_))
from codes_A import A
from konsens_2a import K, KH, HINWEIS, ORDNUNG, KH_ABW

TS = sys.argv[1] if len(sys.argv) > 1 else str(B_ / 'textstand.json')
AUS = sys.argv[2] if len(sys.argv) > 2 else str(B_ / 'anhang_a_2a.md')
BJ = json.load(open(B_ / 'blind' / 'codes_B.json', encoding='utf-8'))
ts = json.load(open(TS, encoding='utf-8'))
W = {s['id']: s['woerter'] for a in ts['absaetze'] for s in a['saetze']}


def c(p, sec):
    return p + (' (' + ', '.join(sec) + ')' if sec else '')


Z = ['| Satz | W | A | B | Konsens nach Codebuch | nach Hinweis | Hinweise | zg | Deutung | Entscheidung |',
     '|---|---:|---|---|---|---|---|---|---:|---|']
for s in ORDNUNG:
    a = A[s]
    b = BJ[s]
    k = K[s]
    kh = KH[s]
    gleich = (a[0], set(a[1])) == (b['primaer'], set(b['sekundaer']))
    if gleich:
        ent = 'A = B'
    elif a[0] != b['primaer']:
        ent = 'Primärcode nach ' + ('A' if k[0] == a[0] else 'B') + ', Grund in konsens_2a.csv'
    else:
        ent = 'Sekundärcodes nach ' + ('A' if set(k[1]) == set(a[1]) else ('B' if set(k[1]) == set(b['sekundaer']) else 'Konsens')) + ', Grund in konsens_2a.csv'
    hin = ', '.join(HINWEIS.get(s, [])) or '—'
    khs = c(kh[0], kh[1]) if s in KH_ABW else 'gleich'
    Z.append(f"| {s} | {W[s]} | {c(a[0], a[1])} | {c(b['primaer'], b['sekundaer'])} | {c(k[0], k[1])} | {khs} | {hin} | "
             f"{k[2] or '—'} | {k[3]} | {ent} |")
open(AUS, 'w', encoding='utf-8').write('\n'.join(Z) + '\n')
print('\n'.join(Z))

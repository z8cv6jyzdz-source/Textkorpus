# -*- coding: utf-8 -*-
"""
abgleich_2a.py — Textstand von Kapitel 5 gegen Befund § 2 bis § 4 (Umfang, Wortanteile, Rahmen vor dem ersten Befund,
Zugfolge, Statistik im Satz, Objektführung, Leseführung, Was der Ergebnisteil nicht tut), Schritt 2 (a), 03.10.2026

Codes aus konsens_2a.py (K nach Codebuch, KH nach den Hinweisen), Merkmale aus eigen.json, Wörter und Sätze aus
textstand.json. Korpuswerte des Kerns (zehn Studien) aus summary.json und saetze_codiert.csv des Korpusordners, gerechnet
wie analyse.py und textbausteine.py (§ 9, § 10) dort. Kapitel 5 ist eine Studie: Lage gegen Median und Spanne des Kerns.
Die Einordnung des eigenen Budgets (Befund § 4, letzter Absatz) ist kein Vergleichsmaßstab (Befund § 6.5).
Aufruf: python abgleich_2a.py <Korpusordner> [<textstand.json> <eigen.json> <Ausgabe.txt> <Ausgabe.json>]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import csv
import json
import pathlib
import statistics as st
import collections

B_ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(B_))
from konsens_2a import K, KH

KORP = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else B_.parent / 'Argumentationsstruktur_Ergebnisteile_2026-10-02'
TS = sys.argv[2] if len(sys.argv) > 2 else str(B_ / 'textstand.json')
EJ = sys.argv[3] if len(sys.argv) > 3 else str(B_ / 'eigen.json')
AUST = sys.argv[4] if len(sys.argv) > 4 else str(B_ / 'abgleich_2a.txt')
AUSJ = sys.argv[5] if len(sys.argv) > 5 else str(B_ / 'abgleich_2a.json')

CORE = ['Lloyd2016', 'Hammami2016', 'Beato2018', 'Negra2019', 'Negra2020', 'Aloui2022', 'Liu2024', 'Moran2024',
        'Sammoud2024', 'Bouafif2026']
SUM = json.load(open(KORP / 'summary.json', encoding='utf-8'))
ROWS = list(csv.DictReader(open(KORP / 'saetze_codiert.csv', encoding='utf-8'), delimiter=chr(59)))
for r in ROWS:
    r['woerter'] = int(r['woerter'])
ts = json.load(open(TS, encoding='utf-8'))
EIG = {r['id']: r for r in json.load(open(EJ, encoding='utf-8'))['saetze']}
SAETZE = [s for a in ts['absaetze'] for s in a['saetze']]
IDS = [s['id'] for s in SAETZE]
W = {s['id']: s['woerter'] for s in SAETZE}
ABS = {s['id']: s['absatz'] for s in SAETZE}
WG = sum(W.values())
G = 'OVXBZ'
CODES = ['O1', 'O2', 'O3', 'O4', 'O5', 'V1', 'V2', 'X1', 'X2', 'B1', 'B2', 'B3', 'B4', 'B5', 'Z1', 'Z2']
out = []
P = out.append
J = {}


def lage(x, xs):
    lo, hi, md = min(xs), max(xs), round(st.median(xs), 1)
    pos = 'unter der Spanne' if x < lo else ('über der Spanne' if x > hi else 'in der Spanne')
    rel = 'über dem Median' if x > md else ('unter dem Median' if x < md else 'gleich dem Median')
    return f'{pos}, {rel} (Kern Median {fmt(md)}, Spanne {fmt(lo)} bis {fmt(hi)})'


def fmt(x):
    if isinstance(x, float):
        return f'{x:.1f}'.replace('.', ',')
    return str(x)


def collapse(seq):
    o = []
    for x in seq:
        if not o or o[-1] != x:
            o.append(x)
    return o


def cats(zg):
    return [c for c in zg.split('+') if c] if zg else []


# ---------- 1 Umfang (Befund § 2.1, § 4, Anhang A) ----------
P('1 Umfang (Befund § 0 Nr. 3, § 2.1, § 4)')
saetze_je_absatz = collections.Counter(ABS[i] for i in IDS)
w_abs = collections.Counter()
for i in IDS:
    w_abs[ABS[i]] += W[i]
um = dict(W=WG, P=len(saetze_je_absatz), S=len(IDS), med=st.median(W.values()), maxsatz=max(W.values()),
          w_je_absatz=round(WG / len(saetze_je_absatz), 1))
for key, name in (('W', 'Wörter'), ('P', 'Absätze'), ('S', 'Sätze'), ('med', 'Satzlänge Median'),
                  ('maxsatz', 'längster Satz'), ('w_je_absatz', 'Wörter je Absatz')):
    xs = [SUM[k][key] for k in CORE]
    P(f'  {name:18} {fmt(um[key]):>6} | {lage(um[key], xs)}')
J['umfang'] = um

# ---------- 2 Wortanteile je Codegruppe und je Code (Befund § 0 Nr. 3, § 2.2, § 4) ----------
P('\n2 Wortanteile (Wortanteil der Primärcodes, Befund § 2.2 und § 4 „Gewicht der Funktionen“)')
J['anteile'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    gw = collections.Counter()
    cw = collections.Counter()
    for i in IDS:
        gw[C[i][0][0]] += W[i]
        cw[C[i][0]] += W[i]
    J['anteile'][name] = {'gruppe': {g: gw[g] for g in G}, 'code': dict(cw)}
    P(f'  Gruppen nach {name}:')
    for g in G:
        xs = [SUM[k]['anteil'][g] * 100 for k in CORE]
        P(f'    {g}: {gw[g]:>3} Wörter = {fmt(gw[g] / WG * 100):>5} % | Kern Mittel {fmt(st.mean(xs))} %, '
          f'Median {fmt(st.median(xs))} %, Spanne {fmt(min(xs))} bis {fmt(max(xs))} %')
    P(f'  Codes nach {name} (Kern: Mittel der Wortanteile über die zehn Studien, Befund § 2.2):')
    for c in CODES:
        xs = [SUM[k]['anteil_code'].get(c, 0) * 100 for k in CORE]
        if cw[c] or any(xs):
            P(f'    {c}: {cw[c]:>3} Wörter = {fmt(cw[c] / WG * 100):>5} % | Kern Mittel {fmt(st.mean(xs))} %, '
              f'in {sum(1 for x in xs if x > 0)} Studien tragend')

# ---------- 3 Vorkommen je Funktion (Befund § 2.2) ----------
P('\n3 Vorkommen je Funktion (primär oder sekundär), Kapitel 5 gegen Zahl der Kernstudien')
J['vorkommen'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    pres = set()
    prim = set()
    for i in IDS:
        pres.add(C[i][0])
        prim.add(C[i][0])
        pres.update(C[i][1])
    J['vorkommen'][name] = sorted(pres)
    zeile = []
    for c in CODES:
        n = sum(1 for k in CORE if c in SUM[k]['pres'])
        zeile.append(f'{c} {"T" if c in prim else ("s" if c in pres else "–")} ({n}/10)')
    P(f'  {name}: ' + ' · '.join(zeile))
P('  T tragend (Primärcode), s nur Sekundärcode, – fehlt · in Klammern Kernstudien mit dem Code (primär oder sekundär)')

# ---------- 4 Rahmen und Text vor dem ersten Befund (Befund § 2.1, § 4, textbausteine.txt § 10) ----------
P('\n4 Rahmen (Wörter in O-, V- und X-Sätzen) und Text vor dem ersten Befund (Sätze vor dem ersten B-Code)')
kern_r = {}
for k in CORE:
    rr = [r for r in ROWS if r['studie'] == k]
    wk = sum(r['woerter'] for r in rr)
    ovx = sum(r['woerter'] for r in rr if r['primaer'][0] in 'OVX')
    fb = next((n for n, r in enumerate(rr) if r['primaer'][0] == 'B'), len(rr))
    kern_r[k] = (round(ovx / wk * 100, 1), round(sum(r['woerter'] for r in rr[:fb]) / wk * 100, 1), fb)  # je Studie gerundet wie textbausteine.py § 10
J['rahmen'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    ovx = sum(W[i] for i in IDS if C[i][0][0] in 'OVX')
    ox = sum(W[i] for i in IDS if C[i][0][0] in 'OX')
    fb = next((n for n, i in enumerate(IDS) if C[i][0][0] == 'B'), len(IDS))
    vor = sum(W[i] for i in IDS[:fb])
    zvor = sum(W[i] for i in IDS[:fb] if C[i][0][0] == 'Z')
    J['rahmen'][name] = dict(ovx=ovx, ox=ox, vor=vor, saetze_vor=fb, erster_befund=IDS[fb], z_vor=zvor)
    P(f'  {name}: Rahmen O+V+X {ovx} Wörter = {fmt(ovx / WG * 100)} % | {lage(ovx / WG * 100, [v[0] for v in kern_r.values()])}')
    P(f'  {name}: ohne V (O+X) {ox} Wörter = {fmt(ox / WG * 100)} %')
    P(f'  {name}: vor dem ersten Befund ({IDS[fb]}) {vor} Wörter = {fmt(vor / WG * 100)} % in {fb} Sätzen, '
      f'davon Z {zvor} Wörter | {lage(vor / WG * 100, [v[1] for v in kern_r.values()])}')
P(f"  Kern: Sätze vor dem ersten Befund Median {fmt(st.median([v[2] for v in kern_r.values()]))}, "
  f"Spanne {min(v[2] for v in kern_r.values())} bis {max(v[2] for v in kern_r.values())}")

# ---------- 5 Zugfolge (Befund § 2.1, § 0 Nr. 4) ----------
P('\n5 Zugfolge nach Primärcodes, aufeinanderfolgende gleiche zusammengefasst')
J['zugfolge'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    seqc = collapse([C[i][0] for i in IDS])
    seq = collapse([C[i][0][0] for i in IDS])
    fb = next((n for n, i in enumerate(IDS) if C[i][0][0] == 'B'), len(IDS))
    vorb = [C[i][0] for i in IDS[:fb]]
    nachov = [C[i][0] for i in IDS[fb:] if C[i][0][0] in 'OV']
    nachz = [C[i][0] for i in IDS[fb:] if C[i][0][0] == 'Z']
    lb = max(n for n, i in enumerate(IDS) if C[i][0][0] == 'B')
    J['zugfolge'][name] = dict(seqc=' '.join(seqc), seq=' '.join(seq), erster=C[IDS[0]][0], letzter=C[IDS[-1]][0],
                               letzter_befund=IDS[lb], vor=vorb, nach_ov=nachov, nach_z=nachz)
    P(f'  {name}: Codes {" ".join(seqc)}')
    P(f'  {name}: Gruppen {" ".join(seq)} | erster {C[IDS[0]][0]} | letzter {C[IDS[-1]][0]} ({IDS[-1]}) | letzter Befundsatz {IDS[lb]}')
    P(f'  {name}: vor dem ersten Befund {" ".join(vorb)} | danach O/V {" ".join(nachov) or "—"} | danach Z {" ".join(nachz) or "—"}')
erst = collections.Counter(SUM[k]['erster'] for k in CORE)
letzt = collections.Counter(SUM[k]['letzter'][0] for k in CORE)
P(f'  Kern: erster Primärcode {dict(erst)} | letzter nach Gruppe {dict(letzt)}')

# ---------- 6 Befundordnung und Zielgrößenfolge (Befund § 3.3) ----------
P('\n6 Befundordnung: Blöcke je Zielgröße (aufeinanderfolgende B-Sätze mit gleicher erster Kategorie im Absatz), Folge der Zielgrößen')
J['bloecke'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    blocks = []
    for i in IDS:
        if C[i][0][0] != 'B':
            continue
        c = cats(C[i][2])[0] if cats(C[i][2]) else 'X'
        if blocks and blocks[-1][0] == c and blocks[-1][2] == ABS[i]:
            blocks[-1][1].append(i)
        else:
            blocks.append([c, [i], ABS[i]])
    zseq = collapse([c for i in IDS if C[i][0][0] == 'B' for c in cats(C[i][2]) if c != 'X'])
    zf = []
    for c in zseq:
        if c not in zf:
            zf.append(c)
    J['bloecke'][name] = dict(bloecke=[(c, b) for c, b, _ in blocks], zfolge=' '.join(zf))
    P(f'  {name}: ' + ' · '.join(f'{c}:{b[0]}' + (f'–{b[-1].split()[1]}' if len(b) > 1 else '') for c, b, _ in blocks)
      + f' | Folge der Zielgrößen {" ".join(zf)}')
P('  Methodik (4.4.1 Sprint, 4.4.2 505, 4.4.3 Standweitsprung) S C J · Titel „Sprint-, Richtungswechsel- und Sprungleistung“ S C J')
B2 = sum(1 for k in CORE if 'B2' in SUM[k]['pres'])
P(f'  Kern: Veränderung je Gruppe (B2) in {B2} von 10 · nach Zielgröße geordnet 6 von 10 (Befund § 3.3)')

# ---------- 7 Statistik im Satz (Befund § 3.4, textbausteine.txt § 9) ----------
P('\n7 Statistik im Befundsatz (Primärcode B): statistischer Wert, p, Teststatistik, Effektstärke als Wert, Intervall, Prozent, M±SD, Größenklasse')
J['statistik'] = {}
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    Bs = [i for i in IDS if C[i][0][0] == 'B']
    m = lambda key: sum(1 for i in Bs if EIG[i]['merkmale'][key] > 0)
    d = dict(n=len(Bs), statwert=m('statwert'), p=m('p'), stat=m('stat'), es=m('es'), ki=m('ki'), prozent=m('prozent'),
             msd=m('msd'), klasse=m('klasse'), differenz=m('differenz'), saetze=Bs)
    J['statistik'][name] = d
    P(f"  {name}: B-Sätze {d['n']} | mit Wert {d['statwert']} ({fmt(d['statwert'] / d['n'] * 100)} %) | p {d['p']} | "
      f"F/t {d['stat']} | ES {d['es']} | KI {d['ki']} | Prozent {d['prozent']} | M±SD {d['msd']} | Klasse {d['klasse']} | Differenz {d['differenz']}")
kb = [r for r in ROWS if r['studie'] in CORE and r['primaer'][0] == 'B']
P(f"  Kern: B-Sätze {len(kb)} | mit Wert {sum(int(r['statwert']) > 0 for r in kb)} "
  f"({fmt(sum(int(r['statwert']) > 0 for r in kb) / len(kb) * 100)} %) | Studien mit p {sum(1 for k in CORE if SUM[k]['befund_mit_p'])} | "
  f"mit KI {sum(1 for k in CORE if SUM[k]['befund_mit_ki'])} | mit ES-Wert {sum(1 for k in CORE if SUM[k]['befund_mit_es'])} | "
  f"mit Klasse {sum(1 for k in CORE if SUM[k]['befund_mit_klasse'])}")
alle_p = [i for i in IDS if EIG[i]['merkmale']['p']]
alle_ki = [i for i in IDS if EIG[i]['merkmale']['ki']]
alle_msd = [i for i in IDS if EIG[i]['merkmale']['msd']]
alle_stat = [i for i in IDS if EIG[i]['merkmale']['stat']]
P(f"  alle Sätze: p in {', '.join(alle_p)} | Intervall in {', '.join(alle_ki)} | ± in {', '.join(alle_msd)} | Teststatistik in {', '.join(alle_stat)}")
J['statistik']['alle'] = dict(p=alle_p, ki=alle_ki, msd=alle_msd, stat=alle_stat)

# ---------- 8 Nullbefunde, Sammelbefunde, Gegenbefunde (Befund § 3.5) ----------
P('\n8 Nullbefunde (Handprüfung in eigen.py), Sammelbefunde, Kontraste')
nulls = [(i, EIG[i]['nullform']) for i in IDS if EIG[i]['nullform']]
for i, f in nulls:
    P(f'  {i} ({K[i][0]}): {f}')
for name, C in (('Codebuch', K), ('Hinweis', KH)):
    b4 = [i for i in IDS if C[i][0] == 'B4' or 'B4' in C[i][1]]
    P(f'  B4 primär oder sekundär nach {name}: {", ".join(b4)}')
J['null'] = nulls
P('  Kontraste mit „jedoch“, „aber“, „während“, „dagegen“: ' + (', '.join(i for i in IDS if re.search(r'\b(?:jedoch|aber|während|dagegen|hingegen|wohingegen)\b', EIG[i]['text'], re.I)) or 'keine'))

# ---------- 9 Objektführung (Befund § 3.2, textbausteine.txt § 12 bis § 14) ----------
P('\n9 Objektführung: Verweise, Formen, Erstnennung, Wiederaufruf, Präsens')
fb = next((n for n, i in enumerate(IDS) if K[i][0][0] == 'B'), len(IDS))
seen = collections.OrderedDict()
wieder = []
for n, i in enumerate(IDS):
    e = EIG[i]
    subj = re.findall(r'^(?:Tab|Abb)\.\s[A-H]?\d+|(?<=,\s)(?:Tab|Abb)\.\s[A-H]?\d+(?=\s+(?:die|den|das)\b)', e['text'])
    for o in e['merkmale']['objekte']:
        form = 'Objektsatz' if o in subj else ('Klammer am Satzende' if e['merkmale']['objekt_klammer_ende'] else 'im Satz')
        if o in seen:
            wieder.append((i, o, form))
        else:
            seen[o] = (i, form, 'vor dem ersten Befund' if n < fb else 'ab dem ersten Befund')
nverw = sum(len(EIG[i]['merkmale']['objekte']) for i in IDS)
P(f'  Verweise {nverw} in {sum(1 for i in IDS if EIG[i]["merkmale"]["objekte"])} Sätzen, Objekte {len(seen)} (Kern: 38 Verweise, 26 Objekte in zehn Studien)')
P(f'  Objekt als Subjekt: {sum(EIG[i]["merkmale"]["objekt_subjekt"] for i in IDS)} Verweise in '
  f'{sum(1 for i in IDS if EIG[i]["merkmale"]["objekt_subjekt"])} Sätzen (Kern 5 Sätze in 3 Studien) · Ort-Form: '
  f'{sum(EIG[i]["merkmale"]["objekt_ort"] for i in IDS)} (Kern 10 Sätze in 7 Studien) · Klammer am Satzende: '
  f'{sum(EIG[i]["merkmale"]["objekt_klammer_ende"] for i in IDS)} Sätze (Kern 22 Sätze in 7 Studien)')
kl_b = [i for i in IDS if EIG[i]['merkmale']['objekt_klammer_ende'] and K[i][0][0] == 'B']
P(f'  Klammer am Satzende in Befundsätzen: {len(kl_b)} (Kern 18 Befundsätze in 5 Studien) · in Sätzen nach Code: '
  + ', '.join(f'{i} {K[i][0]}' for i in IDS if EIG[i]['merkmale']['objekt_klammer_ende']))
zaehl = collections.Counter((f, s) for (_, f, s) in seen.values())
P('  Erstnennung: ' + ' · '.join(f'{o} {i} {f} {s}' for o, (i, f, s) in seen.items()))
P('  Erstnennung gezählt: ' + ', '.join(f'{f} {s}: {n}' for (f, s), n in zaehl.items())
  + ' (Kern: Objektsatz vor 11, Objektsatz ab 3, Klammer vor 3, Klammer ab 9)')
P('  Wiederaufrufe: ' + (' · '.join(f'{o} {i} {f}' for i, o, f in wieder) or 'keine') + ' (Kern 14, davon Klammer am Satzende 11)')
praes = [i for i in IDS if EIG[i]['merkmale']['objekt_subjekt']]
P('  Objektsätze im Präsens: ' + ', '.join(f'{i} {EIG[i]["verb"]}' for i in praes) + ' (Kern 15 von 15)')
J['objekte'] = dict(verweise=nverw, erstnennung={o: list(v) for o, v in seen.items()}, wiederaufruf=wieder,
                    klammer_befund=kl_b)

# ---------- 10 Leseführung und Tempus (Befund § 3.6) ----------
P('\n10 Leseführung und Tempus')
P('  Adverbiale Konnektoren am Satzanfang: ' + (', '.join(f'{i} {EIG[i]["merkmale"]["konnektor"]}' for i in IDS if EIG[i]['merkmale']['konnektor']) or '0 von 29')
  + ' (Kern 14 von 108, 13 %, „However“ 7)')
anf = collections.Counter(EIG[i]['satzanfang'].split(' (')[0] for i in IDS)
P('  Satzanfänge (Handprüfung): ' + ', '.join(f'{a} {n}' for a, n in anf.most_common()))
bt = [i for i in IDS if K[i][0][0] == 'B']
prt = [i for i in bt if 'Präteritum' in EIG[i]['verb']]
P(f'  Befundsätze im Präteritum {len(prt)} von {len(bt)} (Kern 73 von 74) · alle Sätze außerhalb der Objektsätze im Präteritum: '
  f'{sum(1 for i in IDS if "Präteritum" in EIG[i]["verb"])} von {len(IDS) - len(praes)}')
pas = [i for i in IDS if 'Passiv' in EIG[i]['verb']]
P('  Passiv: ' + ', '.join(pas) + ' · Wir-Form: ' + str(sum(EIG[i]['merkmale']['wir'] for i in IDS)))

# ---------- 11 Was der Ergebnisteil nicht tut (Befund § 3.7) ----------
P('\n11 Was der Ergebnisteil des Kerns nicht tut, Kapitel 5 dagegen')
belege = sum(EIG[i]['merkmale']['beleg'] for i in IDS)
deut = sum(K[i][3] for i in IDS)
P(f'  Belege {belege} (Kern 0 in 10) · Deutung {deut} Sätze (Kern 4 Sätze in 4 Studien)')
P(f'  Entscheidung über eine Hypothese: {", ".join(i for i in IDS if "Nullhypothese" in EIG[i]["text"])} (Kern 0)')
P(f'  Unerwünschte Ereignisse (Z2): {", ".join(i for i in IDS if K[i][0] == "Z2")} (Kern 0, erweitert 2)')
P(f'  Datenprüfung und Voraussetzungen (V1): {", ".join(i for i in IDS if K[i][0] == "V1")} (Kern 0)')
P(f'  Zusatz- und Sensitivitätsanalysen (Z1 primär): {", ".join(i for i in IDS if K[i][0] == "Z1")} (Kern 0, Einzelwerte sekundär bei Liu und Moran)')
P('  Analysezahl je Gruppe im Text: keine (A1 S2 nennt 26 gesamt, je Gruppe nur Abb. 1, Tab. 2, Tab. 3) (Kern 0)')
P('  Unadjustierter neben adjustiertem Schätzer: A5 S3 (unadjustiert, ohne Zahl) neben A5 S4 und S5 (adjustiert mit Intervall) (Kern 0, erweitert Hilska)')
J['nicht'] = dict(belege=belege, deutung=deut)

open(AUST, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(J, open(AUSJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(out))

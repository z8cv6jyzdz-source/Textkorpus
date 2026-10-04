# -*- coding: utf-8 -*-
"""
bausteine_2c.py — Teilschritt 2 (c), 03.10.2026: Textbausteine des Befunds § 5.1 und Formulierungssequenzen § 5.2
Satz für Satz an Kapitel 5. Je Satz das Korpusmuster (linke Spalte von § 5.1, § 5.2, dazu § 2 und § 3, gezählt nach der
Zählregel des Befunds § 6.5 mit dem Code nach dem Codebuch) und die Projektregel (rechte Spalte von § 5.1 oder ihre
Fundstelle) getrennt, je Absatz die Zugfolge gegen die sechs Sequenzen, dazu jede Funktion ohne Muster und die Prüfpunkte
aus Fortsetzungsübergabe 2 § 5 Nr. 4.

Verglichen werden Satzfunktion und Bauform, nicht der Wortlaut: Die Bausteine des Korpus sind englische Marker und werden
nicht übersetzt (Stilprofil Teil 0), übertragbar sind Zugfolge und Satzfunktion, nicht die Statistik im Satz (Befund § 5.2),
die rechte Spalte von § 5.1 ist Projektableitung und kein Wortlaut für den Text (Befund § 5.1).

Eingänge im Ordner des Skripts: textstand.json, eigen.json, abgleich_2a.json, master_saetze.json, konsens_2a.py,
teiltabelle_2b.csv. Eingänge im Claude-Ordner (Pfade in QUELLEN): Befund, Anlage …_Saetze.csv, textbausteine.json des
Korpusordners, Stilprofil, Fassung 17, Berichtsraster, Plan, Textvorschlag 5, Umfangsdokument (Umwandlung in quellen),
Fortsetzungsübergabe 2.

Ausgaben: bausteine_2c.txt (Belege, Abschnitte 0 bis 8), teiltabelle_2c.csv (Trennzeichen chr(59), alle Felder in
Anführungszeichen), teiltabelle_2c.md (Tabelle für § 3.3 des Abgleichbefunds).

Statusspalte zweiteilig: „Korpus: …“ (wie Muster, abgewandelt, nur erweitert, kein Muster) und „Fundstelle: …“ (erfüllt,
teilweise, nicht erfüllt, bewusst anders, keine Regel), Regeln in STATUSREGELN (Ausgabe Abschnitt 8). Funktion ist der
Baustein von § 5.1, dem der Satz dient, ohne passende Zeile der Code nach dem Codebuch. Handurteile sind durch
Prüfbedingungen (PRUEF) an die Messung, die Codes, die Anlage und die Zählungen des Korpusordners gebunden. Ein 2b-Verweis
in der Statusspalte steht hinter dem Statuswort, das er belegt, und zeigt auf eine 2b-Zeile mit Maßstab Fundstelle und
demselben Statuswort. Jedes Zitat in „…“ der Spalte Ergebnis wird am genannten Ort gesucht (Studie mit Satz, Befund,
Steuerdokument), ohne Ortsangabe in allen Quelltexten, an Wortgrenzen (Abschnitt 7). Weicht etwas ab, bricht das Skript ab.
Fassung 2 nach der Zweitprüfung (zweitpruefung_2c.md), 48 Zeilen.

Aufruf: python bausteine_2c.py [<Claude-Ordner>] [<Ausgabeordner>]
  <Claude-Ordner>  Ordner mit 00_Steuerung bis 04_Uebergaben (Standard: zwei Ebenen über diesem Skript)
  <Ausgabeordner>  Standard: Ordner des Skripts
Nur lesend. Ohne Semikolon im Skript (chr(59)).
"""
import sys
import os
import re
import csv
import json
import hashlib
from collections import OrderedDict, Counter

HIER = os.path.dirname(os.path.abspath(__file__))
CLAUDE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(HIER))
AUS = sys.argv[2] if len(sys.argv) > 2 else HIER
SK = chr(59)
sys.path.insert(0, HIER)
import konsens_2a  # noqa: E402

QUELLEN = OrderedDict([
    ('befund', ['02_Befunde', 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md']),
    ('anlage', ['02_Befunde', 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv']),
    ('tb', ['03_Skripte', 'Argumentationsstruktur_Ergebnisteile_2026-10-02', 'textbausteine.json']),
    ('stil', ['01_Verfahren', 'Stilprofil_2026-09-13.md']),
    ('f17', ['00_Steuerung', 'Projektanweisungen_Fassung17.md']),
    ('raster', ['02_Befunde', 'Berichtsraster_2026-09-23.md']),
    ('plan', ['04_Uebergaben', 'Plan_Weitere_Schritte_2026-09-25.md']),
    ('tv5', ['04_Uebergaben', 'Textvorschlag_5_2026-09-30.md']),
    ('umfang', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'quellen', 'Auswertungs_und_Berichtsumfang_2026-09-24.md']),
    ('fort2', ['04_Uebergaben', 'Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md']),
])
LOKAL = ['textstand.json', 'eigen.json', 'abgleich_2a.json', 'master_saetze.json', 'konsens_2a.py', 'teiltabelle_2b.csv']


def pfad(k):
    return os.path.join(CLAUDE, *QUELLEN[k])


def lies(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def md5(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


AUSGABE = []


def aus(*t):
    AUSGABE.append(' '.join(str(x) for x in t))


def PRUEF(bed, text):
    if not bed:
        raise SystemExit('PRUEF verletzt: ' + text)


# ---------------------------------------------------------------- Eingänge
TS = json.load(open(os.path.join(HIER, 'textstand.json'), encoding='utf-8'))
EI = json.load(open(os.path.join(HIER, 'eigen.json'), encoding='utf-8'))
A2 = json.load(open(os.path.join(HIER, 'abgleich_2a.json'), encoding='utf-8'))
MS = json.load(open(os.path.join(HIER, 'master_saetze.json'), encoding='utf-8'))['saetze']
TB = json.load(open(pfad('tb'), encoding='utf-8'))
TXT = {k: lies(pfad(k)) for k in QUELLEN if k not in ('anlage', 'tb')}
Z2B = OrderedDict()
for r in csv.DictReader(open(os.path.join(HIER, 'teiltabelle_2b.csv'), encoding='utf-8'), delimiter=SK):
    Z2B[r['Nr.']] = r
PRUEF(len(Z2B) == 47, 'Teiltabelle 2b mit 47 Zeilen')

SATZ = OrderedDict()
ABS = OrderedDict()
for a in TS['absaetze']:
    ABS[a['kennung']] = [s['id'] for s in a['saetze']]
    for s in a['saetze']:
        SATZ[s['id']] = s
IDS = list(SATZ.keys())
MERK = {s['id']: s for s in EI['saetze']}
K = konsens_2a.K
KH = konsens_2a.KH
PRUEF(IDS == list(K.keys()), 'Satzfolge textstand.json gleich konsens_2a.K')
PRUEF(len(IDS) == 29 and list(ABS) == ['A1', 'A2', 'A3', 'A4', 'A5', 'A6'], '29 Sätze in sechs Absätzen')
ALLE = ' '.join(SATZ[i]['text'] for i in IDS)


def T(i):
    return SATZ[i]['text']


def M(i):
    return MERK[i]['merkmale']


def C(i):
    return K[i][0]


KORPUS = list(csv.DictReader(open(pfad('anlage'), encoding='utf-8'), delimiter=SK))
STUD = OrderedDict()
for r in KORPUS:
    STUD.setdefault(r['studie'], []).append(r)
KERN = [s for s in STUD if STUD[s][0]['gruppe'] == 'Kern']
ERW = [s for s in STUD if STUD[s][0]['gruppe'] != 'Kern']
PRUEF(len(KERN) == 10 and len(ERW) == 6, 'Kern 10, erweitert 6')
SID = {(r['studie'], r['satz']): r for r in KORPUS}


def sek(r):
    return [c for c in r['sekundaer'].split(SK) if c]


def hat(r, code):
    return r['primaer'] == code or code in sek(r)


def stud_code(code, gruppe, prim=False):
    menge = KERN if gruppe == 'Kern' else ERW
    return sorted({r['studie'] for r in KORPUS if r['studie'] in menge and (r['primaer'] == code if prim else hat(r, code))})


def saetze_rx(rx, gruppe=None):
    menge = KERN if gruppe == 'Kern' else (ERW if gruppe == 'erw' else list(STUD))
    return [r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in menge and re.search(rx, r['text'])]


def fam(name):
    f = TB['familien'][name]
    return f['kern_saetze'], len(f['kern_studien'])


def text(sid):
    st, nr = sid.rsplit(' ', 1)
    return SID[(st, nr)]['text']


def codefolge(studie, absaetze):
    return [r['primaer'] for r in STUD[studie] if int(r['absatz']) in absaetze]


# ---------------------------------------------------------------- § 0 Eingänge
aus('Teilschritt 2 (c), bausteine_2c.py — Belege der Teiltabelle 2c (Abgleichbefund § 3.3)')
aus('')
aus('0 Eingänge (MD5)')
for f in LOKAL:
    aus('  ' + f.ljust(64), md5(os.path.join(HIER, f)))
for k in QUELLEN:
    aus('  ' + '/'.join(QUELLEN[k]).ljust(64), md5(pfad(k)))
aus('')

# ---------------------------------------------------------------- § 1 Bausteine § 5.1
bef = TXT['befund']
s51 = bef.split('### 5.1 Bausteine je Funktion')[1].split('### 5.2 ')[0]
B51 = OrderedDict()
for z in s51.split('\n'):
    if z.startswith('| ') and not z.startswith('| Funktion') and not z.startswith('|---'):
        c = [x.strip() for x in z.strip().strip('|').split(' | ')]
        PRUEF(len(c) == 4, 'Zeile § 5.1 mit vier Zellen: ' + z[:60])
        B51[c[0]] = dict(muster=c[1], kern=c[2], regel=c[3])
PRUEF(len(B51) == 19, '§ 5.1 mit 19 Bausteinen')
# Kernhäufigkeiten der linken Spalte gegen textbausteine.json und die Anlage
KERNPRUEF = [
    ('Objekt einführen, Subjekt', fam('OBJ_SUBJEKT') == (5, 3), 'OBJ_SUBJEKT 5 Sätze, 3 Studien'),
    ('Objekt einführen, Ort', fam('OBJ_ORT') == (10, 7), 'OBJ_ORT 10 Sätze, 7 Studien'),
    ('Objekt wieder aufrufen', TB['wiederaufruf']['Klammer am Satzende']['saetze'] == 11 and sum(v['saetze'] for v in TB['wiederaufruf'].values()) == 14
     and fam('OBJ_KLAMMER') == (22, 7) and TB['klammer_satzende_erstnennung']['mit Erstnennung']['saetze'] == 11,
     'Wiederaufruf als Klammer 11 von 14, Klammer am Satzende 22 in 7, davon 11 mit Erstnennung'),
    ('Zuteilung, Fluss', len(stud_code('O1', 'Kern')) == 3, 'O1 in 3 Kernstudien'),
    ('Umsetzung', len(stud_code('O2', 'Kern')) == 5, 'O2 in 5 Kernstudien'),
    ('Ausgangslage', len(stud_code('O4', 'Kern')) == 7 and fam('O_BASELINE_TEST')[1] == 4, 'O4 in 7, Test in 4 Studien'),
    ('Messgüte', len(stud_code('O5', 'Kern')) == 1, 'O5 in 1 Kernstudie'),
    ('Gruppenvergleich im Post-Wert', fam('B_POSTWERT')[1] == 2, 'Post-Wert in 2 Studien'),
    ('Wechselwirkung mit Richtung', fam('B_INTERAKTION')[1] == 4, 'Wechselwirkung in 4 Studien'),
    ('Analyse als Subjekt', fam('B_ANALYSE_SUBJEKT') == (9, 5), 'Analyse als Subjekt 9 Sätze, 5 Studien'),
    ('Themenanker', fam('B_THEMA') == (14, 6) and TB['blockstart']['Themenanker'] == 5 and sum(TB['blockstart'].values()) == 38,
     'Themenanker 14 Sätze, 6 Studien, Blockbeginn 5 von 38'),
    ('Gegenbefund', fam('B_KONTRAST') == (7, 5), 'Kontrastmarker 7 Sätze in 5 Studien, davon als Kontrast 5 in 5 (Liu 3.2 und 4.2 formelhaft, Befund § 3.5)'),
    ('Sammelbefund', len(stud_code('B4', 'Kern')) == 6, 'B4 in 6 Kernstudien'),
    ('Sammelbefund mit Ausnahme', sorted(saetze_rx(r'\bexcept\b', 'Kern')) == ['Bouafif2026 1.1', 'Negra2020 1.4', 'Negra2020 1.5', 'Sammoud2024 1.5'],
     '„except“ in 4 Kernsätzen, in Sammelbefunden 3 in 2 Studien (Negra 2020 1.4, 1.5, Bouafif 1.1), dazu Sammoud 1.5 (O4)'),
    ('Nullbefund', len(TB['familien']['B_NULL']['kern_studien']) == 9, 'Nullformeln in 9 Kernstudien'),
    ('Datenprüfung', stud_code('V1', 'Kern') == [], 'V1 Kern 0'),
    ('Ereignisse, Gründe', stud_code('Z2', 'Kern') == [], 'Z2 Kern 0'),
    ('unadjustiert neben adjustiert', saetze_rx(r'(?i)unadjusted', 'Kern') == [], '„unadjusted“ im Kern 0'),
    ('Intervall im Satz', sorted({s.split(' ')[0] for s in saetze_rx(r'(?i)\bCI\b|CL90|confidence', 'Kern') if SID[tuple(s.split(' '))]['primaer'].startswith('B')}) == ['Beato2018'],
     'Intervall in einem Kern-Befundsatz nur Beato'),
]
PRUEF([k for k, _, _ in KERNPRUEF] == list(B51.keys()), 'Kernprüfung deckt alle 19 Bausteine in der Folge von § 5.1')
aus('1 Bausteine des Befunds § 5.1 (19 Zeilen), Kernhäufigkeit gegen textbausteine.json und Anlage')
for k, ok, txt in KERNPRUEF:
    PRUEF(ok, 'Kern ' + k + ': ' + txt)
    aus('  ' + k.ljust(32), '| Kern laut § 5.1:', B51[k]['kern'][:70], '| geprüft:', txt)
aus('')

# ---------------------------------------------------------------- § 2 Sequenzen § 5.2
s52 = bef.split('### 5.2 Formulierungssequenzen')[1].split('## 6 ')[0]
SEQ = OrderedDict()
for z in s52.split('\n'):
    m = re.match(r'^(\d)\. \*\*(.+?)\*\* \((.+?)\): (.*)$', z)
    if m:
        SEQ[int(m.group(1))] = dict(name=m.group(2), quelle=m.group(3), text=m.group(4))
PRUEF(list(SEQ) == [1, 2, 3, 4, 5, 6], '§ 5.2 mit sechs Sequenzen')
SEQ_ABS = OrderedDict([(1, ('Negra2019', [1])), (2, ('Sammoud2024', [2, 3])), (3, ('Liu2024', [2, 3, 4])),
                       (4, ('Aloui2022', [2, 3, 4, 5, 6])), (5, ('Negra2019', [2])), (6, ('Moran2024', [1]))])
SEQ_CODES = {n: codefolge(*SEQ_ABS[n]) for n in SEQ_ABS}
PRUEF(SEQ_CODES[1] == ['O1', 'O1', 'O2', 'X1', 'O4', 'O4'], 'Sequenz 1 O1 O1 O2 X1 O4 O4')
PRUEF(SEQ_CODES[2] == ['B1', 'B2', 'B2', 'B1', 'B2'], 'Sequenz 2 B1 B2 B2 B1 B2')
PRUEF(SEQ_CODES[3].count('B2') == 6 and SEQ_CODES[3].count('B1') == 6, 'Sequenz 3 je Zielgröße B2 B1 B1 B2')
PRUEF(SEQ_CODES[4] == ['B1'] * 6, 'Sequenz 4 nur B1')
PRUEF(SEQ_CODES[5] == ['B2'] * 5 + ['B1', 'B1', 'B4'], 'Sequenz 5 B2 ×5, B1 B1 B4')
PRUEF(SEQ_CODES[6] == ['X1'] * 4 + ['B2'] * 5, 'Sequenz 6 X1 ×4, B2 ×5')
PRUEF('Übertragbar sind Zugfolge und Satzfunktion, nicht die Statistik im Satz' in s52, 'Übertragungsregel § 5.2')


def lcs(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for x in range(len(a)):
        for y in range(len(b)):
            t[x + 1][y + 1] = t[x][y] + 1 if a[x] == b[y] else max(t[x][y + 1], t[x + 1][y])
    out, x, y = [], len(a), len(b)
    while x and y:
        if a[x - 1] == b[y - 1]:
            out.append(a[x - 1])
            x, y = x - 1, y - 1
        elif t[x - 1][y] >= t[x][y - 1]:
            x -= 1
        else:
            y -= 1
    return out[::-1]


KAP = {a: [C(i) for i in ABS[a]] for a in ABS}
aus('2 Sequenzen des Befunds § 5.2 (Codefolge nach der Anlage) gegen die Absätze von Kapitel 5 (Code nach dem Codebuch)')
for n, sq in SEQ.items():
    aus('  Sequenz', n, sq['name'], '(' + sq['quelle'] + '):', ' '.join(SEQ_CODES[n]), '· ohne B2 (P2):', ' '.join(c for c in SEQ_CODES[n] if c != 'B2') or '—')
for a in ABS:
    best = []
    for n in SEQ:
        g1 = lcs(KAP[a], SEQ_CODES[n])
        g2 = lcs(KAP[a], [c for c in SEQ_CODES[n] if c != 'B2'])
        best.append('S' + str(n) + ' ' + str(len(g1)) + '/' + str(len(g2)))
    aus('  ' + a, ' '.join(KAP[a]).ljust(40), '| gemeinsame Teilfolge (Länge mit und ohne B2):', ' · '.join(best))
LCS_A1_S1 = lcs(KAP['A1'], SEQ_CODES[1])
PRUEF(LCS_A1_S1 == ['O1', 'X1', 'O4'], 'A1 und Sequenz 1: gemeinsame Folge O1 X1 O4')
PRUEF(KAP['A5'][:2] == ['X1', 'X1'] and KAP['A5'][2:9] == ['B1'] * 7 and KAP['A5'][9:] == ['B4', 'V2'], 'A5 X1 X1 B1 ×7 B4 V2')
PRUEF(KAP['A6'] == ['V1', 'Z1', 'V1', 'Z1'] and KAP['A2'] == ['O2'] * 4 and KAP['A3'] == ['O3', 'O3', 'Z2', 'Z2'] and KAP['A4'] == ['O5', 'O5'],
      'Codefolgen A2, A3, A4, A6')
aus('  Beato Absatz 2 (Umsetzung → Beanspruchung):', ' '.join(codefolge('Beato2018', [2])), '· Aloui Absatz 1:', ' '.join(codefolge('Aloui2022', [1])),
    '· Klusemann Absatz 1:', ' '.join(codefolge('Klusemann2012', [1])), '· Rogers 2.5 bis 2.7:', ' '.join(r['primaer'] for r in STUD['Rogers2020'] if r['satz'] in ('2.5', '2.6', '2.7')))
PRUEF(codefolge('Beato2018', [2]) == ['O2', 'O3'], 'Beato Absatz 2 O2 O3')
PRUEF(codefolge('Aloui2022', [1])[:2] == ['X1', 'O5'], 'Aloui 1.1 X1, 1.2 O5')
aus('')

# ---------------------------------------------------------------- § 3 Kapitel 5 je Satz
aus('3 Kapitel 5 je Satz: Code nach dem Codebuch (nach dem Hinweis, wo anders), Satzanfang, Verb, Objektformen')
for i in IDS:
    kh = '' if KH[i][:2] == K[i][:2] else ' · nach Hinweis ' + KH[i][0] + (' (' + ', '.join(KH[i][1]) + ')' if KH[i][1] else '')
    aus('  ' + i.ljust(7), (C(i) + (' (' + ', '.join(K[i][1]) + ')' if K[i][1] else '')).ljust(14), kh.ljust(22), '|', MERK[i]['satzanfang'], '|', MERK[i]['verb'],
        '| Subjekt', M(i)['objekt_subjekt'], 'Ort', M(i)['objekt_ort'], 'Klammer', M(i)['objekt_klammer_ende'])
aus('')

# ---------------------------------------------------------------- Prüfbedingungen der Handurteile
ERST = A2['objekte']['erstnennung']
OE_KERN = Counter((v[2], v[3]) for s in KERN for v in TB['objekt_erstnennung'].get(s, {}).values())
MEHRFACH = sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['primaer'] == 'X1' and re.search(r'Tables? \d+ and \d+|Figures? \d+ ?[–-] ?\d+|Figures? \d+ and \d+', r['text']))
UNCLEAR = sorted(saetze_rx(r'(?i)\bunclear\b'))
FOLGE_AUSN = ([SID[('Beato2018', n)]['primaer'] for n in ('4.1', '4.2')] == ['B1', 'B4']
              and [SID[('Negra2019', n)]['primaer'] for n in ('2.6', '2.7', '2.8')] == ['B1', 'B1', 'B4']
              and [SID[('Lloyd2016', n)]['primaer'] for n in ('4.2', '4.3')] == ['B4', 'B3'] and text('Lloyd2016 4.3').startswith('However'))
KERN_SCHWELLE = sorted(saetze_rx(r'(?i)threshold|more than 85%', 'Kern'))
PB = OrderedDict()
PB['A1 S1'] = [(C('A1 S1') == 'X1' and M('A1 S1')['objekt_subjekt'] == 1 and M('A1 S1')['praesens_objekt'] == 1, 'Objekt als Subjekt im Präsens'),
               (saetze_rx(r'(?i)flow ?(chart|diagram)|CONSORT') == [], 'kein Korpussatz verweist auf ein Flussdiagramm'),
               ([r for r in KORPUS if r['studie'] in KERN and r['primaer'] == 'X1' and 'O1' in sek(r)] == [], 'kein Objektsatz des Kerns mit O1'),
               (saetze_rx(r'(?i)as planned|\bterminat|\bstopped\b|\bended\b|prematur') == [], 'kein Satz der Anlage zum planmäßigen Ende'),
               (text('Negra2019 1.1') == 'All subjects received treatment conditions as allocated.' and SID[('Negra2019', '1.1')]['primaer'] == 'O1', 'Negra 2019 1.1 O1'),
               ('planmäßigen' in T('A1 S1'), '„planmäßig“ im Satz')]
PB['A1 S2'] = [(C('A1 S2') == 'O1', 'O1'),
               (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if hat(r, 'O1') and re.search(r'\bn ?= ?\d', r['text'])) == ['Klusemann2012 1.7']
                and not any(re.search(r'\bn ?= ?\d', r['text']) for r in KORPUS if r['studie'] in KERN),
                'Analysezahl je Gruppe in einem O1-Satz nur Klusemann 1.7 (erweitert), „n =“ im Kern 0'),
               (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in KERN and hat(r, 'O1')) == ['Negra2019 1.1', 'Negra2019 1.2', 'Negra2020 1.2', 'Sammoud2024 1.1'],
                'O1 im Kern: Negra 2019 1.1, 1.2, Negra 2020 1.2, Sammoud 1.1'),
               (text('Sammoud2024 1.1').endswith('were consequently fully included in the final analyses.') and text('Negra2020 1.2') == 'All participants completed the aforementioned training programs.',
                'Sammoud 1.1 Aufnahme in die Analyse, Negra 2020 1.2 Abschluss'),
               ('Nine of the 22 participants who completed pre- and post-testing' in text('Rogers2020 2.1') and '(n = 8)' in text('Rogers2020 2.7'), 'Rogers 2.1 und 2.7 mit Bezugsmenge'),
               (re.findall(r'\d+', T('A1 S2')) == ['31', '26'], 'Zahlen 31 und 26, keine Gruppen')]
PB['A1 S3'] = [(C('A1 S3') == 'X1' and M('A1 S3')['objekt_subjekt'] == 2 and M('A1 S3')['objekt_ort'] == 0, 'zwei Objekte als Subjekt, keine Ort-Form'),
               (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['primaer'] == 'X1' and 'O4' in sek(r)) == ['Hilska2021 1.1'] and SID[('Hilska2021', '1.1')]['objekt_ort'] != '0',
                'X1 mit O4 nur Hilska 1.1, Ort-Form'),
               (MEHRFACH == ['Asimakidis2022 1.2', 'Beato2018 3.2', 'Rogers2020 1.3', 'Rogers2020 1.7', 'Rogers2020 1.8'] and SID[('Beato2018', '3.2')]['objekt_ort'] != '0'
                and SID[('Asimakidis2022', '1.2')]['objekt_subjekt'] != '0', 'mehrere Objekte in einem Objektsatz: Kern nur Beato 3.2 (Ort), als Subjekt nur Asimakidis 1.2'),
               (text('Negra2019 1.4').endswith('assessed at baseline and follow-up.') and SID[('Negra2019', '1.4')]['objekt_subjekt'] != '0', 'Negra 2019 1.4 Ausgangswerte, Subjekt'),
               (text('Negra2020 1.3').startswith('The baseline and post-intervention values') and SID[('Negra2020', '1.3')]['objekt_ort'] != '0', 'Negra 2020 1.3 Ausgangswerte, Ort')]
PB['A1 S4'] = [(C('A1 S4') == 'O4' and M('A1 S4')['sig'] == 0 and M('A1 S4')['p'] == 0, 'O4 ohne Test'),
               (fam('O_BASELINE_TEST') == (5, 4), 'Ausgangsvergleich mit Signifikanzaussage 5 Sätze in 4 Studien'),
               (sorted(r[0] + ' ' + r[1] for r in TB['familien']['O_BASELINE_OHNE']['belege'] if r[0] in KERN) == ['Aloui2022 1.3', 'Negra2019 1.6'], 'ohne Signifikanzwort Aloui 1.3 und Negra 2019 1.6'),
               (len(set(TB['familien']['O_BASELINE_TEST']['kern_studien']) | set(TB['familien']['O_BASELINE_OHNE']['kern_studien'])) == 5, 'Ausgangsvergleich in 5 Kernstudien'),
               (text('Sammoud2024 1.3').startswith('Significant between groups differences were detected') and 'except for the inter-limb asymmetry score' in text('Sammoud2024 1.5')
                and 'between group difference at baseline of only 0.9 points' in text('Rogers2020 1.1'), 'vorhandene Unterschiede Sammoud 1.3, 1.5, Rogers 1.1'),
               ([r for r in KORPUS if (r['primaer'] == 'O4' or 'O4' in sek(r)) and re.search(r'(?i)favou?r|higher|greater|better|faster|superior|advantage|lower|taller|heavier|older|younger', r['text'])] == [],
                'keine Richtung in einem Satz mit O4'),
               ('zugunsten' in T('A1 S4') and MERK['A1 S4']['satzanfang'] == 'Quantor', 'Quantor und „zugunsten“')]
PB['A2 S1'] = [(C('A2 S1') == 'O2', 'O2'), (saetze_rx(r'(?i)\bmedian\b') == ['Moran2024 1.2'], '„median“ nur in Moran 1.2 (Objektsatz)'),
               (sorted(saetze_rx(r'(?i)\bmean of\b|\baverage number\b|×/week', 'erw')) == ['Hilska2021 7.1', 'Rogers2020 2.5', 'Rogers2020 2.7', 'Veith2021 3.2'], 'Mittel und Häufigkeit der Einheiten erweitert'),
               ('missed 1 session' in text('Klusemann2012 1.3') and 'all exercises performed 87% of the time' in text('Veith2021 3.2'), 'Klusemann 1.3 verpasste Einheiten, Veith 3.2 Anteil'),
               (ERST['Tab. H2'][0] == 'A2 S1' and ERST['Tab. H2'][1] != 'Objektsatz', 'Erstnennung Tab. H2 in der Klammer'),
               (OE_KERN == Counter({('Objektsatz', 'vor dem ersten Befund'): 11, ('Klammer oder Nebenstellung', 'ab dem ersten Befund'): 9,
                                    ('Objektsatz', 'ab dem ersten Befund'): 3, ('Klammer oder Nebenstellung', 'vor dem ersten Befund'): 3}),
                'Kern 26 Objekte, 12 zuerst in der Klammer, davon 3 vor dem ersten Befund')]
PB['A2 S2'] = [(C('A2 S2') == 'O2' and M('A2 S2')['prozent'] == 2, 'Rate in Prozent'),
               (sorted(r[0] for r in TB['familien']['O_RATE']['belege'] if r[0] in KERN) == ['Beato2018', 'Lloyd2016', 'Negra2019'], 'Raten Lloyd, Beato, Negra 2019'),
               ('Themenanker' in MERK['A2 S2']['satzanfang'], 'Themenanker'), ('notably poor' in text('Rogers2020 2.6'), 'Rogers 2.6 „notably poor“'),
               ('low compliance (<75%)' in text('Klusemann2012 1.5'), 'Klusemann 1.5 Schwelle niedriger Umsetzung je Spieler')]
PB['A2 S3'] = [(C('A2 S3') == 'O2', 'O2'), (KERN_SCHWELLE == ['Lloyd2016 1.3', 'Sammoud2024 1.1'], 'Schwelle der Umsetzung im Kern Lloyd 1.3 und Sammoud 1.1'),
               (SID[('Klusemann2012', '1.5')]['primaer'] == 'O2', 'Klusemann 1.5 O2'),
               ('at least twice' in text('Hilska2021 7.2') and 'more than 75% of the weeks' in text('Hilska2021 7.4'), 'Hilska 7.2, 7.4 Anteile an Schwellen (Teams)'),
               (ERST['Tab. H5'][0] == 'A2 S3', 'Erstnennung Tab. H5 in A2 S3')]
PB['A2 S4'] = [(C('A2 S4') == 'O2' and K['A2 S4'][1] == ['Z1', 'V2'], 'O2 mit Z1 und V2'),
               (saetze_rx(r'(?i)lower bound') == [], 'Untergrenzen im Korpus 0'),
               (fam('B_RESPECTIVELY') == (8, 5), '„respectively“ 8 Sätze in 5 Kernstudien'),
               ('plyometric training = 91%' in text('Lloyd2016 1.3') and '10 m sprint:' in text('Aloui2022 3.1') and 'SBF:' in text('Aloui2022 4.1'),
                'Zuordnung mit „=“ (Lloyd 1.3) und Bezeichnungen in der Klammer (Aloui 3.1, 4.1)'),
               ('respectively' not in text('Klusemann2012 2.5') and 'respectively' not in text('Klusemann2012 4.1') and text('Klusemann2012 2.3').count('respectively') == 1
                and 'and agility (' in text('Klusemann2012 2.3') and text('Klusemann2012 2.5').endswith('for the supervised and video groups.'), 'Klusemann 2.3, 2.5, 4.1 Zuordnung über die Folge'),
               (not re.search(r'jeweils|bzw\.|beziehungsweise|entsprechend', T('A2 S4')), 'A2 S4 ohne Zuordnungswort')]
PB['A3 S1'] = [(C('A3 S1') == 'O3' and stud_code('O3', 'Kern') == ['Beato2018'] and M('A3 S1')['msd'] == 1, 'O3 im Kern nur Beato, M ± SD im Satz'),
               (not any('Beanspruchung' in k for k in B51), 'keine Zeile zur Beanspruchung in § 5.1'),
               (Counter(r['studie'] for r in KORPUS if r['primaer'].startswith('B') and r['msd'] != '0') == Counter({'Klusemann2012': 12, 'Asimakidis2022': 3}),
                '± in Befundsätzen nur erweitert: Klusemann 12, Asimakidis 3')]
PB['A3 S2'] = [(C('A3 S2') == 'O3' and 'V2' in K['A3 S2'][1] and 'Solldauer' in T('A3 S2'), 'O3 mit V2, Solldauer genannt'),
               (saetze_rx(r'(?i)\bload\b') == [], 'Load im Korpus 0'), ('V2' in sek(SID[('Lloyd2016', '1.3')]), 'Lloyd 1.3 mit V2')]
PB['A3 S3'] = [(C('A3 S3') == 'Z2' and stud_code('Z2', 'Kern') == [], 'Z2, Kern 0'),
               (stud_code('Z2', 'erw') == ['Klusemann2012', 'Veith2021'] and stud_code('Z2', 'erw', prim=True) == [], 'erweitert nur sekundär (Klusemann, Veith)')]
PB['A3 S4'] = [(C('A3 S4') == 'Z2' and MERK['A3 S4']['satzanfang'].startswith('Themenanker'), 'Z2 mit Gruppe als Themenanker'),
               (saetze_rx(r'(?i)\bnot (?:collected|recorded|assessed|monitored|measured|available)\b|\bno data\b') == [], 'keine Aussage über nicht erhobene Daten in der Anlage'),
               (text('Klusemann2012 1.4').startswith('The training logs did not reveal all causes') and SID[('Klusemann2012', '1.4')]['primaer'] == 'O2', 'Klusemann 1.4 Erhebungslücke, O2'),
               ('in the intervention and control groups, respectively' in text('Hilska2021 2.1') and SID[('Hilska2021', '1.2')]['primaer'] == 'O3'
                and [SID[('Hilska2021', n)]['primaer'] for n in ('8.1', '8.2', '8.3')] == ['O3'] * 3 and 'control group' in text('Hilska2021 8.1'), 'Hilska 2.1, 1.2, 8.1 bis 8.3')]
PB['A4 S1'] = [(C('A4 S1') == 'O5' and stud_code('O5', 'Kern') == ['Aloui2022'] and M('A4 S1')['objekt_klammer_ende'] == 1, 'O5 im Kern nur Aloui, Klammer'),
               ('Präteritum' in MERK['A4 S1']['verb'], 'Präteritum'), (fam('O_RELIAB') == (1, 1), 'Messgüte im Kern 1 Satz'),
               ([s for s in saetze_rx(r'(?i)\bSWC\b|smallest worthwhile') if re.search(r'(?i)typical error|reliab|\bICC|\bCV\b', text(s))] == [],
                'kein Satz der Anlage legt den Messfehler gegen eine Relevanzschwelle'),
               (SID[('Klusemann2012', '4.6')]['primaer'] == 'O5' and SID[('PadronCabo2025', '1.2')]['primaer'] == 'O5' and SID[('Asimakidis2022', '1.7')]['primaer'] == 'O5',
                'Klusemann 4.6, Padrón-Cabo 1.2, Asimakidis 1.7 O5')]
PB['A4 S2'] = [(C('A4 S2') == 'O5' and saetze_rx(r'(?i)\btrials\b|\battempts?\b') == [], 'gültige Versuche im Korpus 0'),
               (', beim 505-Test' in T('A4 S2'), 'Kontrast im selben Satz')]
PB['A5 S1'] = [(C('A5 S1') == 'X1' and M('A5 S1')['objekt_subjekt'] == 1 and M('A5 S1')['praesens_objekt'] == 1, 'Objektsatz Subjekt Präsens'),
               (T('A5 S1').endswith(" g."), 'Satzende „g.“')]
PB['A5 S2'] = [(C('A5 S2') == 'X1' and 'Z1' in K['A5 S2'][1] and M('A5 S2')['objekt_subjekt'] == 1, 'X1 mit Z1, Subjekt'),
               (SID[('Moran2024', '1.1')]['primaer'] == 'X1' and 'Z1' in sek(SID[('Moran2024', '1.1')]), 'Moran 1.1 X1 mit Z1')]
PB['A5 S3'] = [(C('A5 S3') == 'B1' and KH['A5 S3'][0] == 'B4', 'B1, nach Hinweis B4'),
               (saetze_rx(r'(?i)unadjusted', 'Kern') == [] and 'Hilska2021 3.3' in saetze_rx(r'(?i)unadjusted', 'erw'), 'unadjustiert im Kern 0, erweitert Hilska 3.3'),
               (fam('B_RICHTUNG') == (9, 5), 'Richtungsformeln 9 Sätze in 5 Kernstudien'),
               ('zugunsten' in T('A5 S3') and MERK['A5 S3']['satzanfang'] == 'Quantor', 'Quantor und „zugunsten“'),
               (TB['blockstart']['Quantor ueber die Tests einer Zielgroesse (Einzelbefund)'] == 1, 'Quantor als Blockbeginn 1 von 38')]
PB['A5 S4'] = [(C('A5 S4') == 'B1' and M('A5 S4')['ki'] >= 1 and M('A5 S4')['p'] == 1 and M('A5 S4')['stat'] == 0, 'Intervall und p, keine Teststatistik'),
               (sorted(TB['familien']['B_POSTWERT']['kern_studien']) == ['Bouafif2026', 'Sammoud2024'], 'Post-Wert Sammoud und Bouafif'),
               (all('mean difference:' in text('Liu2024 ' + n) and SID[('Liu2024', n)]['primaer'] == 'B1' for n in ('2.3', '3.3', '4.3')) and 'mean difference: 0.031s' in text('Liu2024 4.3'),
                'Liu 2.3, 3.3, 4.3 Rohdifferenz mit Einheit und p'),
               ('CI 0.1 to 3.2' in text('Veith2021 2.5'), 'Veith 2.5 Intervall'), (MERK['A5 S4']['satzanfang'].startswith('Modell'), 'Modell als Partizip')]
PB['A5 S5'] = [(C('A5 S5') == 'B1' and K['A5 S5'][2] == 'C+J' and MERK['A5 S5']['satzanfang'].startswith('Themenanker'), 'zwei Zielgrößen, Themenanker'),
               (M('A5 S5')['ki'] == 2 and M('A5 S5')['p'] == 2, 'zwei Intervalle, zwei p'),
               (text('Aloui2022 4.1').startswith('There was a training effect for') and 'SBF' in text('Aloui2022 4.1') and SID[('Aloui2022', '4.1')]['primaer'] == 'B1', 'Aloui 4.1 zwei Tests, Wechselwirkung')]
PB['A5 S6'] = [(C('A5 S6') == 'B1' and KH['A5 S6'][0] == 'B4' and 'fehlender Nachweis' in MERK['A5 S6']['nullform'], 'fehlender Nachweis, B1, nach Hinweis B4'),
               (' damit ' in T('A5 S6'), '„damit“ im Satz'),
               (text('Hammami2016 1.3').startswith('None of the 3 agility tests showed any significant gains for the experimental group') and SID[('Hammami2016', '1.3')]['primaer'] == 'B2',
                'Hammami 1.3 Einzelbefund mit Quantor'),
               (text('Klusemann2012 4.4').startswith('No clear changes were found') and SID[('Klusemann2012', '4.4')]['primaer'] == 'B2', 'Klusemann 4.4 „No clear changes“, B2')]
PB['A5 S7'] = [(C('A5 S7') == 'B1' and 'Intervall' in MERK['A5 S7']['nullform'], 'Intervall gegen den SESOI'),
               (UNCLEAR == ['Klusemann2012 2.5', 'Klusemann2012 2.7', 'Klusemann2012 3.2', 'Klusemann2012 3.3', 'Klusemann2012 4.3'], '„unclear“ nur Klusemann (erweitert), Kern 0'),
               ('mean ± 90% confidence limits' in text('Klusemann2012 2.2') and 'but with little difference compared with the video group' in text('Klusemann2012 3.3')
                and text('Klusemann2012 3.3').endswith('unclear).'), 'Klusemann 2.2 Grenzen, 3.3 Urteil in der Klammer'),
               (sorted(b[0] + ' ' + b[1] for b in TB['familien']['B_NULL']['belege'] if SID[(b[0], b[1])]['msd'] != '0' or SID[(b[0], b[1])]['ki'] != '0')
                == ['Klusemann2012 2.2', 'Klusemann2012 2.5', 'Klusemann2012 2.6', 'Klusemann2012 4.4']
                and all(SID[('Klusemann2012', n)]['primaer'] in ('B2', 'B4') for n in ('2.2', '2.5', '2.6', '4.4')), 'Nullformel mit Grenzen nur Klusemann 2.2, 2.5, 2.6, 4.4, je Gruppe'),
               ('with chances for beneficial, trivial, detrimental performance of 71/27/2%' in text('Beato2018 4.1'), 'Beato 4.1 Schwellen in beide Richtungen')]
PB['A5 S8'] = [(C('A5 S8') == 'B1' and SATZ['A5 S8']['woerter'] == 4, 'B1, vier Wörter'),
               (all(SID[('Klusemann2012', n)]['primaer'] == 'B1' and 'unclear' in text('Klusemann2012 ' + n) for n in ('2.7', '4.3'))
                and text('Klusemann2012 2.7').startswith('Differences between the supervised and video groups were'), 'Klusemann 2.7, 4.3 Vergleich als Subjekt mit „unclear“')]
PB['A5 S9'] = [(C('A5 S9') == 'B1' and M('A5 S9')['p'] == 1 and M('A5 S9')['ki'] == 0, 'Schwelle p, kein Intervall'),
               (saetze_rx(r'(?i)hypothes') == [], 'Hypothese im Korpus 0'),
               (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['primaer'] == 'V2') == ['Hilska2021 6.1', 'Rogers2020 1.2', 'Rogers2020 1.9', 'Veith2021 2.3']
                and 'We deemed acceptable compliance as 75%' in text('Rogers2020 1.9') and 'was therefore included as a covariate' in text('Veith2021 2.3'),
                'Regeln mit Entscheidung nur als V2 (Rogers 1.9, Veith 2.3)')]
PB['A5 S10'] = [(C('A5 S10') == 'B4' and 'Hypothesenentscheidung' in MERK['A5 S10']['nullform'], 'B4 als Hypothesenentscheidung')]
PB['A5 S11'] = [(C('A5 S11') == 'V2' and stud_code('V2', 'Kern', prim=True) == [] and stud_code('V2', 'Kern') == ['Lloyd2016', 'Sammoud2024'], 'V2 Kern nur sekundär (Lloyd, Sammoud)'),
                (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in ERW and r['primaer'] == 'V2') == ['Hilska2021 6.1', 'Rogers2020 1.2', 'Rogers2020 1.9', 'Veith2021 2.3'],
                 'V2 erweitert primär 4 Sätze in 3 Studien'), (M('A5 S11')['objekt_klammer_ende'] == 1, 'Klammer am Satzende')]
PB['A6 S1'] = [(C('A6 S1') == 'V1' and stud_code('V1', 'Kern') == [] and M('A6 S1')['stat'] == 1 and M('A6 S1')['p'] == 1, 'V1, Kern 0, W und p'),
               (sorted(saetze_rx(r'(?i)normal(ly)? distribut')) == ['Asimakidis2022 1.1', 'Veith2021 1.1'], 'Verteilungsprüfung nur Asimakidis 1.1 und Veith 1.1'),
               ('(p = 0.016)' in text('Veith2021 2.3') and 'V1' in sek(SID[('Veith2021', '2.3')]), 'Veith 2.3 einzelnes Prüfergebnis mit p, V2 mit V1'),
               (text('Sammoud2024 3.1').startswith('Regarding the asymmetry scores, the ANCOVA analysis indicated') and MERK['A6 S1']['satzanfang'].startswith('Themenanker'), 'Bauform wie Sammoud 3.1')]
PB['A6 S2'] = [(C('A6 S2') == 'Z1' and stud_code('Z1', 'Kern', prim=True) == [] and M('A6 S2')['ki'] >= 1, 'Z1, Kern primär 0, Intervall'),
               (T('A6 S2').endswith(' s.'), 'Satzende „s.“')]
PB['A6 S3'] = [(C('A6 S3') == 'V1' and M('A6 S3')['objekt_klammer_ende'] == 1 and 'übrigen' in T('A6 S3'), 'V1, „übrigen“, Klammer'),
               (sorted(saetze_rx(r'(?i)\bremaining\b|\bother tests\b|all the other', 'Kern')) == ['Beato2018 4.2', 'Negra2019 2.8'], '„remaining“ und „other tests“ im Kern Beato 4.2, Negra 2019 2.8'),
               (all(SID[tuple(s.split(' '))]['primaer'] == 'B4' for s in ['Beato2018 4.2', 'Negra2019 2.8']), 'beide B4'),
               (FOLGE_AUSN, 'Ausnahme vor den übrigen: Beato 4.1 → 4.2, Negra 2019 2.6, 2.7 → 2.8, umgekehrt Lloyd 4.2 → 4.3')]
PB['A6 S4'] = [(C('A6 S4') == 'Z1' and T('A6 S4').startswith('Soweit') and M('A6 S4')['objekt_klammer_ende'] == 1, 'Z1, „Soweit …“, Klammer'),
               (text('Lloyd2016 1.2').startswith('Irrespective of maturation, none of') and SID[('Lloyd2016', '1.2')]['primaer'] == 'B4', 'Lloyd 1.2 B4 mit vorangestellter Einschränkung'),
               (sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if r['studie'] in ERW and hat(r, 'Z1')) == ['Asimakidis2022 1.6', 'Hilska2021 4.2', 'Rogers2020 1.3', 'Rogers2020 1.8', 'Rogers2020 2.1', 'Rogers2020 2.3', 'Rogers2020 2.4'],
                'Z1 erweitert: Asimakidis 1.6, Hilska 4.2, Rogers'),
               (TB['ende']['Lloyd2016']['letzter'].startswith('B') and sum(1 for s in KERN if TB['ende'][s]['letzter'].startswith('Z')) == 0, 'kein Kern-Ergebnisteil endet mit Z'),
               (sum(1 for s in KERN if TB['ende'][s]['letzter_klammer']) == 5, 'letzter Satz mit Klammer in 5 von 10 Kernstudien')]
PRUEF(list(PB) == IDS, 'Prüfbedingungen für alle 29 Sätze')

# ---------------------------------------------------------------- Zeilen der Teiltabelle 2c
# (Prüfgegenstand, Maßstab, Befundstelle, Fundstelle im Text, Ergebnis, Status, Beleg)
# Teil A: je Satz
RA = OrderedDict()
RA['A1 S1'] = ('Objekt einführen, Teilnehmerfluss', 'Korpus und Fundstelle', '§ 5.1 „Objekt einführen, Subjekt“ (Kern 5 · 3), „Zuteilung, Fluss“ (Kern O1 in 3), § 3.1 · rechts: Stilprofil Teil 4, F17 § 10, CONSORT 13a, Raster 5.1.4, Register 1e', 'Korpusmuster: Objekt als Subjekt im Präsens wie „Fig 1 shows …“ (Moran 1.1) und „Table 3 displays …“ (Negra 2019 1.4). Abgewandelt: Der Satz trägt mit dem Fluss bis zum planmäßigen Ende eine zweite Funktion (O1), die kein Objektsatz des Kerns trägt (X1 mit O1 im Kern 0). Auf ein Flussdiagramm verweist kein Kern-Ergebnistext („Kein Kern-Ergebnistext verweist auf ein Flussdiagramm.“, § 3.1), den Fluss tragen dort O1-Sätze ohne Objekt („All subjects received treatment conditions as allocated.“, Negra 2019 1.1). Ein planmäßiges Studienende nennt kein Satz der Anlage. Projektregel: Erstverweis als Subjekt im Präsens („Tab. 3 zeigt …“, F17 § 10, dazu Stilprofil Teil 4 und Register 1e), Flussdiagramm im Ergebnisteil nach CONSORT 13a („Flussdiagramm im Methodikteil – es gehört nach 5.1 (CONSORT 13a).“, F17 § 5a), „planmäßig“ nach dem Klick zu Rasterzeile 5.1.4 (CONSORT 14b, Register 8a), gegen den Korpus bewusst anders (2b.33).', 'Korpus: abgewandelt · Fundstelle: erfüllt (Register 1e)', 'bausteine_2c.txt § 3, Moran2024 1.1, Negra2019 1.4, 1.1')
RA['A1 S2'] = ('Teilnehmerfluss, Menge zur Eingangstestung angetreten', 'Korpus und Fundstelle', '§ 5.1 „Zuteilung, Fluss“ (Kern O1 in 3), § 3.1 · rechts: F17 § 3 (Bezugsmengen-Regel), Raster 5.1.2, P11', 'Korpusmuster: O1 in 3 Kernstudien als Zuteilung wie geplant („All subjects received treatment conditions as allocated.“, Negra 2019 1.1), Ausfall mit Grund („Three participants … withdrew …“, Negra 2019 1.2), Abschluss („All participants completed the aforementioned training programs.“, Negra 2020 1.2) oder Aufnahme in die Analyse mit Quantor („… were consequently fully included in the final analyses.“, Sammoud 1.1, O1 sekundär). Abgewandelt: Sammoud 1.1 ist das nächste Kernvorbild für die Analysemenge, eine Zahl nennt kein Kernsatz („n =“ im Kern 0). Eine Analysezahl nennt erweitert als O1 nur Klusemann 1.7 („Final data analysis included a total number of 36 subjects“, mit Zahl je Gruppe), als Bezugsmenge auch Rogers 2.1 und 2.7. A1 S2 nennt Eingangsgetestete und Analysierte ohne Gruppen und ohne Grund, beides steht in Abb. 1 (KF17, Register 11h). Projektregel: genau ein Satz zur Menge „zur Eingangstestung angetreten“ (F17 § 3, Raster 5.1.2, Register 2b, 2f), Spieler je Gruppe und Nenner im Objekt (P11).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.25)', 'bausteine_2c.txt § 3, Negra2019 1.1, 1.2, Negra2020 1.2, Sammoud2024 1.1, Klusemann2012 1.7, Rogers2020 2.1, 2.7')
RA['A1 S3'] = ('Objekte der Ausgangslage einführen', 'Korpus und Fundstelle', '§ 5.1 „Objekt einführen, Subjekt“ (Kern 5 · 3) und „Objekt einführen, Ort“ (Kern 10 · 7), „Ausgangslage“ (Kern O4 in 7) · rechts: Stilprofil Teil 4, P1, Raster § 3.12, Register 1e, 1f', 'Korpusmuster: Objekt als Subjekt im Präsens wie Negra 2019 1.4 („Table 3 displays test data for all components of physical fitness assessed at baseline and follow-up.“). Abgewandelt: Der Satz trägt mit der Ausgangslage eine zweite Funktion (O4), die kein Objektsatz des Kerns trägt (X1 mit O4 nur Hilska 1.1, erweitert, in der Ort-Form: „The player characteristics for the intervention and study groups are provided in Table 1.“), und führt zwei Objekte ein, das zweite elliptisch. Zwei Objekte in einem Objektsatz hat der Kern nur in der Ort-Form („Within-group changes for CODJ-G and COD-G are reported in Tables 1 and 2, respectively.“, Beato 3.2), die Subjektform nur erweitert (Asimakidis 1.2). Ausgangswerte führt der Kern in beiden Formen ein, als Subjekt (Negra 2019 1.4) und als Ort (Negra 2020 1.3), die Ort-Form ist im Kern insgesamt die häufigere (10 Sätze in 7 Studien gegen 5 in 3). Projektregel: Erstverweis als Subjekt im Präsens (Register 1e), Größe und Überlappung im Objekt, keine Zahl aus Tab. 2 im Satz (P1, Raster § 3.12). Tab. H3 als Subjekt (elliptisch) nach Stilprofil Teil 4, die Auslegung für Anhangsobjekte lässt die Klammer zu, verlangt sie nicht (Register 1f, dazu 2b.4).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.15, Register 1e)', 'bausteine_2c.txt § 3, Negra2019 1.4, Negra2020 1.3, Hilska2021 1.1, Beato2018 3.2, Asimakidis2022 1.2')
RA['A1 S4'] = ('Richtung der Ausgangsunterschiede', 'Korpus und Fundstelle', '§ 5.1 „Ausgangslage“ (Kern O4 in 7, Test in 4), § 3.1 · rechts: P1 (CONSORT 15, F17 § 4), Textvorschlag 5 § 3, F17 § 11.2b', 'Korpusmuster: Ausgangsvergleich der Gruppen vor den Befunden in 5 Kernstudien, davon 4 mit Signifikanzaussage („Baseline comparisons revealed no significant differences between groups …“, Liu 1.1). Ohne Signifikanzwort und mit Quantor über die Tests stehen Aloui 1.3 („No parameter showed between-group differences at baseline.“) und Negra 2019 1.6 (Anlage). Abgewandelt: A1 S4 hat diese Form (Quantor, kein Test) und berichtet die Richtung der Unterschiede. Vorhandene Unterschiede nennt der Kern ohne Richtung („Significant between groups differences were detected for the chronological age, height, body mass, and maturity offset.“, Sammoud 1.3, dazu 1.5), erweitert Rogers 1.1 (Ausgangsunterschied unter der SWC), eine Richtung nennt kein Satz der Anlage. Projektregel: ohne Test, im Satz nur die Richtung (P1, Textvorschlag 5 § 3), die Richtung als „zugunsten der ⟨Gruppe⟩“ (Befund § 5.1 rechts) wie in der Schlusslogik („zugunsten der IG“, F17 § 11.2b), Register 10e.', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.15)', 'bausteine_2c.txt § 3, Liu2024 1.1, Aloui2022 1.3, Negra2019 1.6, Sammoud2024 1.3, 1.5, Rogers2020 1.1')
RA['A2 S1'] = ('Umsetzung: Meldungen nach Status, Median', 'Korpus und Fundstelle', '§ 5.1 „Umsetzung“ (Kern O2 in 5), „Objekt wieder aufrufen“ (Klammer am Satzende 22 · 7), § 3.1 · rechts: F17 § 3.2, Raster 5.1.6, Register 1f, 2g', 'Korpusmuster: Umsetzung im Kern als Rate je Gruppe, für beide Gruppen oder als „alle“ („The training compliance rate was 95% for the two groups.“, Negra 2019 1.3), immer hoch (§ 3.1). Abgewandelt: Zählungen nach Status und ein Median je Spieler, ohne Kernvorbild. „median“ steht im Korpus nur in einem Objektsatz (Moran 1.2). Erweitert am nächsten sind Spanne und Mittel je Teilnehmer (Rogers 2.5, 2.7, Hilska 7.1), der Anteil vollständiger Durchführung (Veith 3.2) und gezählte verpasste Einheiten (Klusemann 1.3). Erstverweis Tab. H2 als Klammer am Satzende, im Kern stehen 12 von 26 Objekten zuerst in einer Klammer, 3 davon vor dem ersten Befund. Projektregel: Meldungen nach Status und Median mit Nenner (F17 § 3.2, Raster 5.1.6), Nenner die 18 Zugeteilten (Register 2g), Anhangsobjekt in der Klammer (Register 1f). Stil: zweite Aussage nach dem Komma (2b.47), „6,0 vollständige je Spieler“ als offene Begriffsbrücke (Register 10u).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.27)', 'bausteine_2c.txt § 3, Negra2019 1.3, Moran2024 1.2, Rogers2020 2.5, 2.7, Hilska2021 7.1, Veith2021 3.2, Klusemann2012 1.3')
RA['A2 S2'] = ('Umsetzungsrate', 'Korpus und Fundstelle', '§ 5.1 „Umsetzung“ (Kern O2 in 5), § 3.1, § 6.4 · rechts: F17 § 3.2, Raster 5.1.6, Register 10s', 'Korpusmuster: Rate in Prozent wie Negra 2019 1.3, Lloyd 1.3 und Beato 2.1 (Raten in drei Kernstudien, § 3.1), hier mit der Bezugsgröße als Themenanker („Bei zwölf angebotenen Einheiten je Spieler“). Die Höhe hat kein Kernvorbild, im Kern berichten alle fünf hohe Werte. Eine Gruppe als niedrig stuft erweitert nur Rogers ein („notably poor“, 2.6), eine Schwelle niedriger Umsetzung je Spieler nennt Klusemann 1.5 („low compliance (<75%)“), A2 S2 ohne Etikett. Projektregel: Rate mit Nenner (F17 § 3.2, Raster 5.1.6), Anteil mit den teilweise durchgeführten ohne das Wort „Beteiligungsrate“ (Register 10s).', 'Korpus: wie Muster · Fundstelle: erfüllt (2b.27)', 'bausteine_2c.txt § 3, Negra2019 1.3, Lloyd2016 1.3, Beato2018 2.1, Rogers2020 2.6, Klusemann2012 1.5')
RA['A2 S3'] = ('Umsetzung an den Schwellen sechs und neun', 'Korpus und Fundstelle', '§ 5.1 „Umsetzung“ (Kern O2 in 5), „Objekt wieder aufrufen“ (Kern 11 von 14 Wiederaufrufen als Klammer), § 3.1 · rechts: F17 § 3.2, Raster 5.1.6, 5.1.11, Register 9c', 'Korpusmuster: Eine Schwelle der Umsetzung nennen im Kern Lloyd 1.3 („above the predetermined attendance threshold“) und Sammoud 1.1 („more than 85% of the training sessions“), beide für alle Teilnehmer über der Schwelle. Abgewandelt: Spielerzahlen an Schwellen hat nur die Erweiterung, für Spieler Klusemann 1.5 („Only 5 subjects from the video group completed all 12 sessions“), für Teams Hilska 7.2 und 7.4. A2 S3 nennt die Zahl der Spieler an zwei Schwellen, zwei Hauptsätze mit Komma, der zweite elliptisch (Komma-Ausnahme, 2b.47), am Satzende Wiederaufruf (Tab. H2) und Erstverweis (Tab. H5) in einer Klammer. Projektregel: Schwellen ≥ 6 und ≥ 9 (F17 § 3.2, Raster 5.1.6), Schwellenlandschaft mit Erstverweis Tab. H5 (Raster 5.1.11), Antragskriterium bei der Umsetzung, Ort bewusst anders nach Textvorschlag 5 (Register 9c, dazu 2b.31).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.27), Ort bewusst anders (2b.31)', 'bausteine_2c.txt § 3, Lloyd2016 1.3, Sammoud2024 1.1, Klusemann2012 1.5, Hilska2021 7.2, 7.4')
RA['A2 S4'] = ('Untergrenzen der Umsetzung', 'Korpus und Fundstelle', '§ 5.1 „Umsetzung“ (Kern O2 in 5), § 3.6 („respectively“ in 8 Sätzen aus 5 Studien) · rechts: F17 § 3.2', 'Korpusmuster: Baustein Umsetzung (Kern O2 in 5), abgewandelt zu Untergrenzen nach zwei Zählregeln, die weder der Kern noch die Erweiterung hat. Parallele Werte ordnet der Kern mit „respectively“ zu (8 Sätze in 5 Kernstudien, in Umsetzungssätzen Beato 2.1, erweitert Hilska 2.1 und Veith 3.4), mit „=“ (Lloyd 1.3) oder mit Bezeichnungen in der Klammer (Aloui 3.1, 4.1). Erweitert ordnet Klusemann über die Folge ohne Zuordnungswort zu, die Bezugsfolge steht dort im selben Satz („Both the supervised and video groups had small increases in the number of push-ups performed“, 4.1, dazu 2.3 und 2.5). A2 S4 ordnet „neun und zwei“ und „neun und einer“ ebenso über die Folge zu, die Bezugsfolge der Schwellen steht aber im vorigen Satz (A2 S3), dafür hat der Korpus kein Vorbild. Die Zählregeln stehen als Themenanker und Präpositionalgruppe im Satz (V2 sekundär). Projektregel: Untergrenzen wochengedeckelt und nach distinkten Nummern an den Schwellen ≥ 6 und ≥ 9, „in 5.1 als Sensitivität“ (F17 § 3.2), als Untergrenzen benannt (Textvorschlag 5 § 10 Nr. 18), Raten der Untergrenzen in Tab. H2 (Register 10p).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.27)', 'bausteine_2c.txt § 3 und § 6, Beato2018 2.1, Lloyd2016 1.3, Aloui2022 3.1, 4.1, Klusemann2012 2.3, 2.5, 4.1')
RA['A3 S1'] = ('Beanspruchung CR-10', 'Korpus und Fundstelle',
               'keine Zeile in § 5.1 · § 2.2 (O3 in 1), § 3.1, § 3.4 · Raster 5.1.7',
               'Korpusmuster: § 5.1 hat keine Zeile. Im Kern einmal, als RPE je Gruppe mit Mittelwert und Streuung („The average RPE was 5.5 ± 0.99 and 5.50 ± 1 for CODJ-G and COD-G, respectively.“, Beato 2.2), Mittelwert ± SD steht im Kern „nur in Orientierungssätzen (Beato)“ (§ 3.4), erweitert ± auch in 15 Befundsätzen (Klusemann 12 als 90-%-Grenzen, Asimakidis 3). A3 S1 hat diese Bauform (Größe als Subjekt, M ± SD, Präteritum) für eine Gruppe, mit Median und Spanne in der Klammer, und folgt auf die Umsetzung wie Beato 2.2 auf 2.1. Projektregel: CR-10 der Interventionsgruppe mit n, M, SD, Median, Minimum und Maximum im Satz (Raster 5.1.7), „als vollständig gemeldet“ als Selbstauskunft (Textvorschlag 5 § 10 Nr. 3).',
               'Korpus: wie Muster · Fundstelle: erfüllt', 'bausteine_2c.txt § 3 und § 5, Beato2018 2.1, 2.2')
RA['A3 S2'] = ('Beanspruchung sRPE-Load', 'Korpus und Fundstelle',
               'keine Zeile in § 5.1 · § 2.2 (O3 in 1) · Raster 5.1.7, F17 § 10, Register 3f',
               'Korpusmuster: Bauform wie A3 S1 (Beato 2.2), dazu die Definition der Größe im Satz („Der mit der Solldauer berechnete …“, V2 sekundär), wie Lloyd 1.3 die Anwesenheit an eine vorab festgelegte Schwelle bindet (O2 mit V2). Einen Load berichtet der Korpus nicht. Projektregel: sRPE-Load mit denselben Kennwerten (Raster 5.1.7), Load-Sprachregelung („Der sRPE-Load ist CR-10 mal Solldauer.“, F17 § 10), Klickentscheidung vom 24.09. Nr. 3 (Register 3f).',
               'Korpus: wie Muster · Fundstelle: erfüllt', 'bausteine_2c.txt § 3 und § 5, Beato2018 2.2, Lloyd2016 1.3')
RA['A3 S3'] = ('Meldungen mit Schmerzangabe je Status', 'Korpus und Fundstelle',
               '§ 5.1 „Ereignisse, Gründe“ (Kern 0) · rechts: CONSORT 19, P10, Raster 5.1.8, Register 9d',
               'Korpusmuster: Kern 0. Erweitert stehen Beschwerden nur als Grund von Ausfällen oder verpassten Einheiten („Having no partner (48.9%) and injury/soreness/sickness (44.7%) were reported as the main reasons for not fully completing the programme.“, Veith 3.3, dazu Klusemann 1.1, 1.3, 1.6, alle als Sekundärcode). A3 S3 zählt Meldungen und Spieler je Status, ohne Grund und ohne Kausalzuschreibung. Projektregel: Meldungen und Spieler je Status, ohne Kausalzuschreibung (CONSORT 19, P10), ohne Lokalisation (Register 9d). Der Status „ganz“ ergibt sich nur rechnerisch (2b.24), die Menge der neun Spieler steht nicht im Satz (2b.45, Schwere B).',
               'Korpus: nur erweitert · Fundstelle: teilweise (2b.45)', 'bausteine_2c.txt § 3 und § 5, Veith2021 3.3, Klusemann2012 1.1, 1.3, 1.6')
RA['A3 S4'] = ('Kontrollgruppe ohne Instrument', 'Korpus und Fundstelle', '§ 5.1 „Ereignisse, Gründe“ (Kern 0) · rechts: CONSORT 19, Raster 5.1.8, Register c8', 'Korpusmuster: Funktion Z2 im Kern 0, erweitert nur als Sekundärcode (§ 5.1 mit Veith 3.3). Dass für eine Gruppe nichts erhoben wurde, sagt kein Satz der Anlage. Eine Lücke der Erhebung benennt nur Klusemann 1.4 (erweitert, O2: „The training logs did not reveal all causes for the lower compliance in the video group.“). Eine Erhebung je Gruppe berichtet erweitert nur Hilska: den Rücklauf des Instruments je Gruppe („96% and 95% in the intervention and control groups, respectively“, 2.1, am nächsten an A3 S4), die Exposition je Gruppe (1.2) und Begleitbedingungen der Kontrollgruppe am Schluss (8.1 bis 8.3, O3). A3 S4 beginnt mit der Gruppe als Themenanker. Projektregel: Kontrollgruppe ohne Erfassungsinstrument (CONSORT 19, Raster 5.1.8), wörtliche Doppelung in 6.1 A6 S4 vermieden (Register c8).', 'Korpus: nur erweitert · Fundstelle: erfüllt (2b.24)', 'bausteine_2c.txt § 3, Klusemann2012 1.4, Hilska2021 1.2, 2.1, 8.1 bis 8.3')
RA['A4 S1'] = ('Messgüte post gegen SESOI', 'Korpus und Fundstelle',
               '§ 5.1 „Messgüte“ (Kern O5 in 1), „Objekt wieder aufrufen“ · rechts: F17 § 11.3, Raster 5.1.9',
               'Korpusmuster: Messgüte im Kern einmal, als Urteil über alle Zielgrößen im Präsens nach einem Objektsatz in der Ort-Form („Reliability is summarized in Table 3.“, „ICC and CV, including 95% CI, show acceptable reliability for all variables.“, Aloui 1.1, 1.2), erweitert als Kennwert (Klusemann 4.6) oder Urteil über alle Tests (Padrón-Cabo 1.2). Eine kleinste bedeutsame Veränderung nennt erweitert Asimakidis 1.7 als eigenen Wert, den Messfehler legt kein Satz der Anlage gegen sie. A4 S1 trägt Urteil und Quantor wie Aloui 1.2, misst den Fehler gegen den SESOI (ohne Vorbild), steht im Präteritum (F17 § 10) und ruft Tab. 1 aus 4.4 als Klammer am Satzende auf. Projektregel: Messfehler gegen den SESOI, Kennwerte im Objekt (F17 § 11.3, Raster 5.1.9), „auch“ knüpft an 4.4 an („Der TE überstieg bei allen Zielgrößen den SESOI“).',
               'Korpus: abgewandelt · Fundstelle: erfüllt', 'bausteine_2c.txt § 3, Aloui2022 1.1, 1.2, Klusemann2012 4.6, PadronCabo2025 1.2, Asimakidis2022 1.7')
RA['A4 S2'] = ('Gültige Versuche je Gruppe', 'Korpus und Fundstelle', '§ 5.1 „Messgüte“ (Kern O5 in 1), „Gegenbefund“ (Kern als Kontrast 5 · 5), § 3.5 · rechts: Raster 5.1.9, F17 § 5.1', 'Korpusmuster: Baustein Messgüte (Kern O5 in 1, Aloui 1.2), abgewandelt zu gültigen Versuchen je Gruppe, die weder der Kern noch die Erweiterung berichtet (trials und attempts in der Anlage 0). Den Kontrast der Gruppen trägt der Satz im selben Satz ohne Konnektor, wie der Korpus Kontraste im selben Satz mit „whereas“, „while“ oder „but“ führt (Hammami 1.4, Liu 2.4, Bouafif 1.4, § 3.5). Projektregel: gültige Versuche je Gruppe und Zeitpunkt in einem Satz (Raster 5.1.9), Wiederaufruf Tab. H1 aus 4.4 in der Klammer. Die Folge Sprint, Sprung, Richtungswechsel folgt der Gruppe mit mehr Versuchen, nicht der festen Reihenfolge (F17 § 5.1, 2b.8).', 'Korpus: abgewandelt · Fundstelle: teilweise (2b.8)', 'bausteine_2c.txt § 3, Aloui2022 1.2, Hammami2016 1.4, Liu2024 2.4, Bouafif2026 1.4')
RA['A5 S1'] = ('Tab. 3 einführen', 'Korpus und Fundstelle',
               '§ 5.1 „Objekt einführen, Subjekt“ (Kern 5 · 3), „unadjustiert neben adjustiert“ (Kern 0) · rechts: Stilprofil Teil 4, CONSORT 18, P3, P4',
               "Korpusmuster: Objekt als Subjekt im Präsens wie „Table 3 displays test data …“ (Negra 2019 1.4), der Befundteil setzt mit Objektsätzen ein wie bei Moran (1.1 bis 1.4, Sequenz 6). Projektregel: Erstverweis als Subjekt im Präsens (Stilprofil Teil 4), unadjustiert und adjustiert beide im Objekt (P4, CONSORT 18), g im Objekt (P3, Register 10c). Satzende auf einen Einzelbuchstaben („… sowie Hedges' g.“, 2b.46, Schwere C).",
               'Korpus: wie Muster · Fundstelle: erfüllt (2b.17, 2b.18, Register 1e)', 'bausteine_2c.txt § 3, Negra2019 1.4, Moran2024 1.1 bis 1.4')
RA['A5 S2'] = ('Abb. 2 einführen', 'Korpus und Fundstelle',
               '§ 5.1 „Objekt einführen, Subjekt“ (Kern 5 · 3), § 2.2 (Z1 sekundär) · rechts: Stilprofil Teil 4, Raster 5.2.8, Register 12a',
               'Korpusmuster: Objekt als Subjekt im Präsens wie „Fig 1 shows pre- and post-training measures for each participant …“ (Moran 1.1), dort wie hier mit einem Wert je Teilnehmer, bei Moran als Einzelwertdarstellung (Z1 sekundär wie Moran 1.1 bis 1.3 und Liu 2.5). Projektregel: Abb. 2 mit einem einführenden Satz (Raster 5.2.8), Modellgrafik, keine Einzelwertgrafik im Sinn von F17 § 11.6 (Register 10f, 12a).',
               'Korpus: wie Muster · Fundstelle: erfüllt (Register 1e, 12a)', 'bausteine_2c.txt § 3, Moran2024 1.1, Liu2024 2.5')
RA['A5 S3'] = ('Richtung unadjustiert gegen adjustiert', 'Korpus und Fundstelle',
               '§ 5.1 „unadjustiert neben adjustiert“ (Kern 0), „Wechselwirkung mit Richtung“ (Kern 4 Studien mit Wechselwirkung), „Sammelbefund“ (Kern B4 in 6), § 3.3 · rechts: CONSORT 18, F17 § 11.2b, K8, Raster 5.2.2',
               'Korpusmuster: Unadjustiert neben adjustiert hat der Kern nicht, erweitert Hilska 3.3 mit beiden Schätzern in einer Klammer („unadjusted IRR, 0.81 [95% CI, 0.63-1.03]“). Die Richtung tragen im Kern Richtungsformeln („with the EG improving more than CG“, Aloui 3.1, „favored the LPJT group“, Negra 2019 2.6, 9 Sätze in 5 Studien, Anlage), A5 S3 „zugunsten der Interventionsgruppe“ und „weiter von null entfernt als“. Der Quantor am Satzanfang macht den Satz nach dem Codebuch nicht zum Sammelbefund (B1, nach dem Hinweis H2 B4, das zählt nicht), als Blockbeginn hat ein Quantor über Einzelbefunde im Kern nur Hammami 1.3. Projektregel: beide Schätzer im Objekt, im Satz die Richtung beider (CONSORT 18), die adjustierte über das Vorzeichen bei genannter Subtraktionsrichtung (2b.39), Richtung als „zugunsten der IG“ (F17 § 11.2b), Quantor gilt für alle Zielgrößen der Aussage (K8). Stellung vor dem Modellergebnis ohne Entscheidung (2b.6), zweite Angabe mit „und“ (2b.47).',
               'Korpus: nur erweitert · Fundstelle: erfüllt (2b.18)', 'bausteine_2c.txt § 3 und § 6, Hilska2021 3.3, Aloui2022 3.1, Negra2019 2.6, Hammami2016 1.3')
RA['A5 S4'] = ('Adjustierte Differenz 30-m-Sprint', 'Korpus und Fundstelle', '§ 5.1 „Gruppenvergleich im Post-Wert“ (Kern 2 Studien), „Intervall im Satz“ (Kern 1), „Analyse als Subjekt“ (Kern 9 · 5) · rechts: P3, P5, CONSORT 18, F17 § 5.3, Zeile 16', 'Korpusmuster: Den Gruppenvergleich im Post-Wert nennen im Kern Sammoud und Bouafif, Sammoud alle Zielgrößen in einem Satz mit p und d, ohne Schätzer und Intervall und mit Größenklasse („A significant large between-group difference at post-test was observed for CMJ height“, 2.1). Abgewandelt: Rohdifferenz mit 95-%-Intervall und p. Eine Rohdifferenz zwischen den Gruppen mit Einheit und p, ohne Intervall, hat im Kern Liu („mean difference: 0.031s“, 4.3, dazu 2.3 und 3.3), ein Intervall im Befundsatz steht im Kern nur bei Beato 4.1 (90-%-Grenzen einer standardisierten Effektstärke), das nächste Vorbild für eine Rohdifferenz mit 95-%-Intervall und p ist erweitert Veith 2.5 („(1.6 kg, CI 0.1 to 3.2, p = 0.036)“, wachstumsadjustiertes Modell). Das Verfahren steht als Partizip am Satzanfang („Adjustiert für …“), nicht als Subjekt wie „the ANCOVA analysis indicated …“ (Sammoud 3.1). Projektregel: adjustierte Differenz mit Richtung, 95-%-KI und p, g im Objekt, ohne „signifikant“ und ohne Größenklasse (P3, P5), das Verfahren nur zur Unterscheidung der Schätzer (CONSORT 18), Spanne mit „bis“ (F17 § 5.3), keine Teststatistik (Zeile 16). Den Fall je Zielgröße im Block bewertet 2c.34 (2b.9).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.17, 2b.19)', 'bausteine_2c.txt § 3, Sammoud2024 2.1, 3.1, Liu2024 2.3, 3.3, 4.3, Beato2018 4.1, Veith2021 2.5')
RA['A5 S5'] = ('Adjustierte Differenzen 505 und Standweitsprung', 'Korpus und Fundstelle', '§ 5.1 „Themenanker“ (Kern 14 · 6, als Blockbeginn 5 von 38), „Gruppenvergleich im Post-Wert“, „Intervall im Satz“ · rechts: F17 § 5a, Plan § 3 Task 11, Stilprofil Teil 7, P3', 'Korpusmuster: Themenanker am Blockbeginn wie „Regarding the asymmetry scores, the ANCOVA analysis indicated …“ (Sammoud 3.1), das zweite Glied „beim Standweitsprung“ elliptisch im selben Satz. Zwei Tests in einem Satz wie Sammoud 2.1 (alle, Post-Wert) und Aloui 4.1 (zwei Tests als Wechselwirkung). Abgewandelt wie A5 S4: Rohdifferenz mit Intervall und p ohne Kernvorbild (2c.18). Projektregel: Folge der Zielgrößen erfüllt (F17 § 5a, Plan § 3 Task 11), den Fall je Zielgröße im Block bewertet 2c.34 (2b.9). Je Zielgröße derselbe Satzkern mit „betrug“ und einer Klammer aus Intervall und p (Stilprofil Teil 7: „Kap. 5: je Zielgröße derselbe Satzbau“), zwei Hauptsätze mit Komma (Komma-Ausnahme, 2b.47).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.17, 2b.19)', 'bausteine_2c.txt § 3, Sammoud2024 2.1, 3.1, Aloui2022 4.1')
RA['A5 S6'] = ('Nullbefund', 'Korpus und Fundstelle', '§ 5.1 „Nullbefund“ (Kern 9 Studien), „Sammelbefund“ (Kern B4 in 6), § 3.5 · rechts: F17 § 10, § 11.2b, P6, Umfangsdokument § 5.1, K8', 'Korpusmuster: Nullbefunde ausdrücklich in 9 von 10, als fehlende Signifikanz („No significant changes of RSSA performance were seen (Table 5).“, Hammami 1.5), fehlender Unterschied („No differences were found in the improvements between experimental groups“, Negra 2020 1.5) oder Größenklasse („trivial between-group differences“, Negra 2019 2.8). Abgewandelt: A5 S6 nennt den fehlenden Nachweis, diese Form hat der Kern nicht, erweitert am nächsten „No clear changes were found …“ (Klusemann 4.4, Veränderung je Gruppe). Den Quantor über die Tests trägt im Kern Hammami 1.3 als Einzelbefund („None of the 3 agility tests showed any significant gains for the experimental group“), nach dem Codebuch ist A5 S6 ebenso kein Sammelbefund (B1). Projektregel: „kein Gruppenunterschied nachweisbar“ mit Schätzer, Intervall und Fall (F17 § 10, P6), erster Satz der Musterformulierung C1 („Ein Gruppenunterschied ist nicht nachweisbar.“, Umfangsdokument § 5.1) im Präteritum mit Quantor. Der Quantor bindet nur über „damit“ an die drei geprüften Zielgrößen (2b.11).', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.20)', 'bausteine_2c.txt § 3, Hammami2016 1.3, 1.5, Negra2020 1.5, Negra2019 2.8, Klusemann2012 4.4')
RA['A5 S7'] = ('Intervall gegen den SESOI (Fall C1)', 'Korpus und Fundstelle', '§ 3.4, § 3.5, § 6.4 · Umfangsdokument § 5.1, F17 § 11.2b, Register 3c', 'Korpusmuster: Kern 0. Ein Intervall gegen Relevanzschwellen in beide Richtungen liest erweitert Klusemann über die qualitative Inferenz (Schätzer ± 90-%-Grenzen, „mean ± 90% confidence limits“, 2.2), am Gruppenvergleich mit dem Urteil in der Klammer („but with little difference compared with the video group“, 3.3, darauf „unclear“). Dass „unclear“ dort ein Intervall über beide Relevanzschwellen bezeichnet, steht nicht in der Anlage und ist an der Methodik zu bestätigen (2 d). Im Kern liest Beato eine Effektstärke mit 90-%-Grenzen gegen Schwellen in beide Richtungen („with chances for beneficial, trivial, detrimental performance of 71/27/2%“, 4.1), dort bei einem Befund mit Unterschied. Befund § 3.5 („Keine Studie liest einen Nullbefund über ein Intervall oder gegen eine Relevanzschwelle.“) und § 6.4 sind in 2 (d) nachzuzählen. Projektregel: Fall C1 nach der Musterformulierung („Das Intervall ist mit relevanten Effekten in beide Richtungen vereinbar.“, Umfangsdokument § 5.1), abgewandelt im Präteritum, mit Quantor über die drei Intervalle und „Unterschieden“ statt „Effekten“ (Wortliste Plan § 3 Task 11, 2b.19).', 'Korpus: nur erweitert · Fundstelle: erfüllt (2b.19)', 'bausteine_2c.txt § 3 und § 5, Klusemann2012 2.2, 3.3, Beato2018 4.1')
RA['A5 S8'] = ('Fall der Schlusslogik', 'Korpus und Fundstelle', '§ 3.5, § 6.4 · Umfangsdokument § 5.1, Register 3c, 6i', 'Korpusmuster: Kern 0. Erweitert urteilt Klusemann über Gruppenunterschiede mit „unclear“, den Vergleich als Subjekt und mit Kopula wie A5 S8 („Differences between the supervised and video groups were trivial or unclear in vertical jump, sit and reach, and 20-m sprint performance.“, 2.7, dazu 4.3). Projektregel: dritter Satz der Musterformulierung C1 („Der Befund ist unschlüssig.“, Umfangsdokument § 5.1), im Präteritum und im Plural für drei Zielgrößen, „waren“ statt „blieben“ (Textvorschlag 5 § 10 Nr. 17), der Fall statt einer Größenklasse (Register 6i).', 'Korpus: nur erweitert · Fundstelle: erfüllt (2b.19)', 'bausteine_2c.txt § 3 und § 5, Klusemann2012 2.7, 4.3')
RA['A5 S9'] = ('Entscheidungsregel', 'Korpus und Fundstelle', '§ 3.7 · rechts: 4.7 A3 S8, Register 4a, 6f, Textvorschlag 5 § 7.2', 'Korpusmuster: Kern 0, erweitert 0. Eine Regel für die Entscheidung über eine Hypothese nennt kein Ergebnisteil („Entscheidung über eine Hypothese 0“, § 3.7, „hypothes…“ kommt in der Anlage nicht vor), Regeln mit Entscheidung stehen nur als Analyseregeln mit V2 (Rogers 1.9, Veith 2.3). Die Bauform gleicht dem Einzelbefund mit Quantor über die Tests („None of the 3 agility tests showed any significant gains for the experimental group“, Hammami 1.3). Projektregel: Entscheidungsregel an der adjustierten Differenz in der Sprache von 4.7 („H0 gilt als verworfen, wenn mindestens eine davon einen Vorteil der Interventionsgruppe mit p < 0,05 (zweiseitig) zeigt“, 4.7 A3 S8, Register 4a, 6f), Satzende ohne Ziffer (Textvorschlag 5 § 7.2).', 'Korpus: kein Muster · Fundstelle: erfüllt (2b.21)', 'bausteine_2c.txt § 3, Hammami2016 1.3, Rogers2020 1.9, Veith2021 2.3')
RA['A5 S10'] = ('Entscheidung über H0', 'Korpus und Fundstelle',
                '§ 5.1 „Sammelbefund“ (Kern B4 in 6), § 2.1, § 3.7 · rechts: P7, Register 4a, 6k',
                'Korpusmuster: B4 steht im Kern nur als Sammelbefund mit Quantor („Irrespective of maturation, none of the control groups made any significant changes in performance“, Lloyd 1.2), eine Entscheidung über eine Hypothese trifft kein Ergebnisteil („Kein Ergebnisteil endet mit einem Resümee, keiner entscheidet über eine Hypothese.“, § 0 Nr. 4). Projektregel: Entscheidung über H0 im Ergebnisteil (P7, F17 § 11.2b, Umfangsdokument § 5.1, Textvorschlag 4.7 § 7), weder „Studienprotokoll“ noch „Ethikantrag“ im Kapitel (Register 6k).',
                'Korpus: kein Muster · Fundstelle: erfüllt (2b.21)', 'bausteine_2c.txt § 3, Lloyd2016 1.2')
RA['A5 S11'] = ('Deskriptive Zielgrößen', 'Korpus und Fundstelle',
                'keine Zeile in § 5.1 für V2 · § 2.2 (V2 Kern 2, tragend 0), „Objekt wieder aufrufen“ (Kern 11 von 14 Wiederaufrufen als Klammer) · rechts: Raster 5.2.5, Stilprofil Teil 4',
                'Korpusmuster: V2 steht im Kern nur als Sekundärcode (Lloyd 1.3, Sammoud 1.1), erweitert als eigener Satz vorn (Rogers 1.2, 1.9) oder im Befundteil mit Grund („The number of injuries was too small for analyzing each severity group separately.“, Hilska 6.1, dazu Veith 2.3), nie nach dem letzten Befund (2b.28). A5 S11 nennt die Behandlung ohne Grund, der Grund steht in 4.7 (die 505-Seitenwerte „laut Studienprotokoll“, die Sprintzeiten als „alle Teilmengen unter acht Spielern je Gruppe“, 4.7 A1 S5). Wiederaufruf Tab. H3 als Klammer am Satzende wie im Kern. Projektregel: deskriptive Zielgrößen in einem Satz ohne p und Effektstärke (Raster 5.2.5: „ein Satz im Text. Ohne p und ohne Effektstärke, Grund in 4.7“), danach höchstens die Klammer am Satzende (Stilprofil Teil 4).',
                'Korpus: nur erweitert · Fundstelle: erfüllt (2b.28)', 'bausteine_2c.txt § 3 und § 5, Hilska2021 6.1, Rogers2020 1.2, 1.9, Veith2021 2.3')
RA['A6 S1'] = ('Verworfene Normalverteilung 30-m-Sprint', 'Korpus und Fundstelle', '§ 5.1 „Datenprüfung“ (Kern 0), „Themenanker“ (Kern 14 · 6), „Analyse als Subjekt“ (Kern 9 · 5) · rechts: P8 (R2), F17 § 11.9, Raster 5.2.3, Zeile 16', 'Korpusmuster: Datenprüfung im Kern 0, erweitert als erster Satz des Ergebnisteils mit Sammelurteil („A normal distribution was observed for all data (p > 0.05).“, Asimakidis 1.1) oder mit der Ausnahme im selben Satz („All data except age were normally distributed.“, Veith 1.1). Ein einzelnes Prüfergebnis mit p im Befundteil hat erweitert Veith 2.3 („ROG impacted upon the statistical model assessing EH-S (p = 0.016)“, V2 mit V1). A6 S1 nennt die verworfene Prüfung mit Prüfgröße und p in eigenem Satz, in der Bauform der Kernbausteine Themenanker und Analyse als Subjekt („Regarding the asymmetry scores, the ANCOVA analysis indicated …“, Sammoud 3.1). Die Projektregel zur Analyse als Subjekt („das Verfahren nur, wo es den Schätzer unterscheidet“) gilt für Befundsätze, nicht für eine Datenprüfung. Projektregel: verworfene Prüfung mit Prüfgröße und p (P8, R2, O7, Raster 5.2.3), ein Satz zur verworfenen Prüfung (Zeile 16), Stellung nach dem Gruppenvergleich nach Plan (2b.28). Die übrigen Prüfungen folgen in A6 S3 (2b.22).', 'Korpus: nur erweitert · Fundstelle: erfüllt', 'bausteine_2c.txt § 3, Asimakidis2022 1.1, Veith2021 1.1, 2.3, Sammoud2024 3.1')
RA['A6 S2'] = ('Bootstrap-Intervall', 'Korpus und Fundstelle',
               'keine Zeile in § 5.1 für Z1 · § 2.2 (Z1 Kern 2, tragend 0), § 3.7, „Intervall im Satz“ (Kern 1) · rechts: P8 (R2), Raster 5.2.4, Register 6a, 6b, c4',
               'Korpusmuster: Z1 steht im Kern nur sekundär in Objektsätzen zu Einzelwerten (Moran 1.1 bis 1.3, Liu 2.5), Sensitivitätsanalysen berichtet kein Kern-Ergebnisteil („Sensitivitätsanalysen 0“, § 3.7), erweitert stehen Zusatzanalysen vorn als Objektsatz (Rogers 1.3, 1.8), im Befundteil (Hilska 4.2, Rogers 2.1, 2.3, 2.4) oder danach (Asimakidis 1.6). Die Form des Intervalls (Spanne mit Einheit, „von … bis“) entspricht erweitert Veith 2.5 („CI 0.1 to 3.2“). Projektregel: Bootstrap-KI neben der verworfenen Prüfung in genau einem Satz, als nachträglich festgelegt gekennzeichnet (P8, R2, Raster 5.2.4, Register 6a, c4), streichbar nur mit dem Streichpaket aus acht Punkten (Register 6b, Textvorschlag 4.7 § 7). Satzende auf einen Einzelbuchstaben („… bis +0,107 s.“, 2b.46, Schwere C).',
               'Korpus: nur erweitert · Fundstelle: erfüllt', 'bausteine_2c.txt § 3 und § 5, Moran2024 1.1, Liu2024 2.5, Rogers2020 1.3, 1.8, Veith2021 2.5')
RA['A6 S3'] = ('Übrige Voraussetzungen', 'Korpus und Fundstelle', '§ 5.1 „Datenprüfung“ (Kern 0), „Sammelbefund mit Ausnahme“ (Kern in Sammelbefunden 3 · 2) · rechts: P8, F17 § 11.9, Register 6g', 'Korpusmuster: Datenprüfung im Kern 0, erweitert Asimakidis 1.1 (Sammelurteil über alle Daten). Die Bauform „Die übrigen … wurden nicht verworfen (Tab. H4)“ gleicht den Kern-Sammelbefunden über die übrigen Tests („For the remaining tests (ICoD, 10-m, 20-m, and CMJ), trivial between-group differences were demonstrated (Table 4).“, Negra 2019 2.8, „All the other tests did not report any substantial variation between groups after the protocol.“, Beato 4.2), die dort Befunde sind (B4) und wie A6 S3 auf A6 S1 dem Einzelbefund in eigenem Satz folgen (Negra 2019 2.6, 2.7, Beato 4.1). Bei der Datenprüfung nennt nur Veith 1.1 eine Ausnahme, mit „except“ im selben Satz. Projektregel: übrige „geprüft und nicht verworfen“ (F17 § 11.9, P8, Register 6g), sinngleich, nicht wörtlich (2b.22, Schwere C), „mit Tests“ grenzt die grafisch geprüfte Linearität aus (Textvorschlag 5 § 3), Wiederaufruf Tab. H4 aus 4.7.', 'Korpus: nur erweitert · Fundstelle: teilweise (2b.22)', 'bausteine_2c.txt § 3, Asimakidis2022 1.1, Negra2019 2.6 bis 2.8, Beato2018 4.1, 4.2, Veith2021 1.1')
RA['A6 S4'] = ('Sammelsatz Per-Protokoll und Sensitivität', 'Korpus und Fundstelle',
               'keine Zeile in § 5.1 für Z1 · § 2.1 (Schluss), § 3.7, „Sammelbefund“ (Bauform) · rechts: P9 (R1, R4), Stilprofil Teil 3, Register 10h, 10t, c4',
               'Korpusmuster: Kern 0, Sensitivitäts- und Per-Protokoll-Analysen berichtet kein Kern-Ergebnisteil, keiner endet mit einem Z-Satz (2b.13), erweitert nennt Hilska Unteranalysen im Befundteil („Significant reductions in the incidence rates were also seen in the subanalyses of acute noncontact injuries“, 4.2). Die Bauform, eine vorangestellte Einschränkung mit verneintem Quantor, gleicht Lloyd 1.2 („Irrespective of maturation, none of the control groups made any significant changes in performance“), dort ein Sammelbefund (B4). A6 S4 ist nach dem Codebuch Z1 und zählt nicht als Sammelbefund. Klammer am Satzende im letzten Satz wie 5 von 10 Kernstudien. Projektregel: Sensitivität und Per-Protokoll in einem Sammelsatz (P9, R1) in der Zählung von 4.7 (Register 10t), Inferenz nur, soweit die Fallzahl reicht (R4), Per-Protokoll als beobachtend (Register c4). Gegen Stilprofil Teil 3 steht die Bedingung als Nebensatz vorn und „und keine davon …“ hängt eine zweite Aussage an (2b.47).',
               'Korpus: nur erweitert · Fundstelle: erfüllt (2b.23)', 'bausteine_2c.txt § 3, Hilska2021 4.2, Lloyd2016 1.2')

# Teil B: je Absatz gegen die Sequenzen § 5.2
RB = OrderedDict()
RB['A1'] = ('Zugfolge A1 gegen Sequenz 1', 'Korpus und Fundstelle',
            '§ 5.2 Sequenz 1 (Negra 2019, Absatz 1), § 3.1 · Plan § 3 Task 11, F17 § 5a',
            'Sequenz 1: Fluss → Ausfall mit Grund → Umsetzung → Objekt → Merkmale → Zielgrößen (O1 O1 O2 X1 O4 O4). A1: Objekt (Abb. 1) → Fluss → Objekt (Tab. 2, Tab. H3) → Ausgangslage (X1 O1 X1 O4). Gemeinsam ist die Folge Fluss → Objekt → Ausgangslage, das Objekt vor dem Ausgangsvergleich wie Negra 2019 1.4 vor 1.5 und 1.6. Anders: Ein Objektsatz zum Flussdiagramm eröffnet (im Kern ohne Vorbild), der Ausfall mit Grund steht in Abb. 1 (KF17), die Stichprobenmerkmale stehen in 4.2 (Register 5b), die Umsetzung folgt erst in A2. „Eine feste Folge innerhalb der Orientierung zeigt der Korpus nicht.“ (§ 3.1). Projektseite: Folge nach Plan § 3 Task 11, gegen F17 § 5a bewusst anders und gedeckt (2b.42).',
            'Korpus: abgewandelt · Fundstelle: bewusst anders (2b.42)', 'bausteine_2c.txt § 2, Negra2019 1.1 bis 1.6')
RB['A2'] = ('Zugfolge A2 (Umsetzung)', 'Korpus und Fundstelle',
            '§ 5.2 (keine Sequenz zur Umsetzung), § 3.1 („Umsetzung im Setting“) · F17 § 3.2, Raster 5.1.6',
            'Keine der sechs Sequenzen hat eine mehrsätzige Umsetzung, Sequenz 1 trägt sie in einem Satz (Negra 2019 1.3). Mehrsätzig berichten nur die Settingstudien: Klusemann 1.2 bis 1.6 (Rate je Gruppe → verpasste Einheiten mit Grund → unbekannte Gründe → Spieler an Schwellen mit Ausschluss → Krankheit), Rogers 2.5 bis 2.7 (Spanne und Mittel → Einstufung → Spanne und Mittel), Hilska 7.1 bis 7.5, Veith 3.2 bis 3.5. A2: Status und Median → Rate → Spieler an Schwellen → Untergrenzen (O2 O2 O2 O2), die Folge Rate → Schwelle wie Klusemann 1.2 → 1.5, ohne Gründe. Projektseite: Inhalt nach F17 § 3.2 und Raster 5.1.6, Umfang wie die Settingstudien (2b.27).',
            'Korpus: nur erweitert · Fundstelle: erfüllt (2b.27)', 'bausteine_2c.txt § 2, Klusemann2012 1.2 bis 1.6, Rogers2020 2.5 bis 2.7')
RB['A3'] = ('Zugfolge A3 (Beanspruchung, Schäden)', 'Korpus und Fundstelle', '§ 5.2 (keine Sequenz), § 2.1 (Beato), § 3.1 · Raster 5.1.7, 5.1.8, Plan § 3 Task 11, F17 § 5a', 'Keine Sequenz in § 5.2. Die Folge Umsetzung → Beanspruchung (A2 → A3 S1) hat im Kern Beato (2.1 Compliance → 2.2 RPE, Zugfolge O4 O2 O3 … in § 2.1). Schäden nach der Beanspruchung (Z2) haben kein Kernvorbild, erweitert stehen sie bei der Umsetzung (Klusemann 1.3, 1.6, Veith 3.3), Z2 im Rahmen ist gegen K1 bewusst anders (2b.2). Projektseite: Beanspruchung und unerwünschte Ereignisse im Orientierungszug erfüllt (Raster 5.1.7, 5.1.8, Plan § 3 Task 11), die Folge des Orientierungszugs gegen F17 § 5a bewusst anders und gedeckt (2b.42).', 'Korpus: abgewandelt · Fundstelle: bewusst anders (2b.42)', 'bausteine_2c.txt § 2, Beato2018 2.1, 2.2, Klusemann2012 1.3, 1.6, Veith2021 3.3')
RB['A4'] = ('Zugfolge A4 (Messgüte)', 'Korpus und Fundstelle',
            '§ 5.2 (keine Sequenz), § 3.1 · Raster 5.1.9, Plan § 3 Task 11',
            'Keine Sequenz in § 5.2. Messgüte steht im Kern einmal, am Anfang (Aloui 1.1 Objektsatz → 1.2 Urteil), erweitert am Anfang (Padrón-Cabo 1.1 → 1.2, Objektsatz → Urteil, dazu Rogers 1.1 mit dem Ausgangsunterschied gegen die SWC) oder am Schluss (Klusemann 4.6, Asimakidis 1.7). A4 steht am Ende der Orientierung vor den Befunden, ohne eigenen Objektsatz, weil Tab. 1 aus 4.4 eingeführt ist. Eine Folge innerhalb der Orientierung gibt der Korpus nicht vor (§ 3.1). Projektseite: TE post vor den gültigen Versuchen, der Plan nennt „unerwünschte Ereignisse, gültige Versuche und TE post“, Teil der gedeckten Folge des Orientierungszugs (2b.42).',
            'Korpus: abgewandelt · Fundstelle: bewusst anders (2b.42)', 'bausteine_2c.txt § 2, Aloui2022 1.1, 1.2, PadronCabo2025 1.1, 1.2, Rogers2020 1.1')
RB['A5'] = ('Zugfolge A5 gegen die Sequenzen 2 bis 6', 'Korpus und Fundstelle', '§ 5.2 Sequenz 2 (Sammoud), 4 (Aloui), 6 (Moran), 3 und 5 · § 6.4, § 7 Nr. 7 · P2, P3, P12, Plan § 3 Task 11, Register 7a', 'Sequenz 6 (Objekte zuerst, Befunde kurz): Wie dort führen Objektsätze den Befundteil ein (hier zwei, Moran vier), die Befundsätze folgen ohne Objektsatz (Moran mit einer Klammer in 1.5). Sequenz 2 (a priori geplante ANCOVA): Sammoud stellt den Gruppenvergleich im Post-Wert über alle Zielgrößen in einen Satz (2.1, 49 Wörter, p und d), dann die Veränderungen je Gruppe (2.2, 2.3, nach P2 ausgeschlossen), dann die nächste Zielgröße mit Themenanker (3.1). Ohne die B2-Sätze bleibt die Folge Post-Wert-Vergleich → Themenanker, A5 S4 und S5 folgen ihr mit einem Satz für den 30-m-Sprint und einem für 505 und Standweitsprung, mit Intervall statt d (P3, P12 mit höchstens 32 Wörtern). Vor ihnen steht A5 S3 (unadjustiert, in der Sequenz ohne Vorbild), danach die Schlusslogik (A5 S6 bis S10) und A5 S11 ohne Sequenz. Sequenz 4 (ein Satz je Zielgröße, eigener Absatz mit Unterüberschrift) trifft nur A5 S4 und ohne Absatz (Register 7a). Die Sequenzen 3 und 5 beruhen auf Veränderungen je Gruppe (P2), sie sind nicht übertragbar. Nächstes Vorbild für A5 ist nach der Funktion Sequenz 2 (§ 7 Nr. 7, Post-Wert-Vergleich zuerst). Nach der Codefolge lägen die Sequenzen 3 und 4 vorn (gemeinsame Teilfolge je 6 gegen 2), ihre gleichförmigen B1-Folgen beruhen aber auf Veränderungen je Gruppe oder tragen nur einen Satz je Zielgröße. Projektseite: P2, P3 und P12 erfüllt, der Fall steht einmal für alle drei Zielgrößen statt je Zielgröße im Block (2b.9), Abb. 2 vor den Befunden, Tab. 3 vor Abb. 2 und A5 S11 vor der Absicherung sind nach Textvorschlag 5 bewusst anders (2b.31).', 'Korpus: abgewandelt · Fundstelle: teilweise (2b.9), bewusst anders bei Abb. 2, Objektfolge und A5 S11 (2b.31)', 'bausteine_2c.txt § 2, Sammoud2024 2.1 bis 3.2, Moran2024 1.1 bis 1.9, Aloui2022 2.1 bis 6.2')
RB['A6'] = ('Zugfolge A6 (Absicherung)', 'Korpus und Fundstelle', '§ 5.2 (keine Sequenz), § 3.1, § 3.5, § 3.7, § 6.4 · Plan § 3 Task 11, Textvorschlag 5 § 2, Raster § 3.13', 'Keine Sequenz in § 5.2 und keine Stellungsregel (§ 6.4). Der Kern berichtet weder Datenprüfung noch Sensitivität (§ 3.7), erweitert steht die Datenprüfung als erster Satz (Veith 1.1, Asimakidis 1.1) oder als Analyseregel im Befundteil (Hilska 6.1, Veith 2.3), Zusatzanalysen stehen vorn als Objektsatz (Rogers 1.3, 1.8), im Befundteil (Hilska 4.2, Rogers 2.1) oder danach (Asimakidis 1.6). A6: verworfene Prüfung → Bootstrap → übrige Prüfungen → Sammelsatz (V1 Z1 V1 Z1). Die Ausnahme steht vor den übrigen wie bei Befunden im Kern (Beato 4.1 → 4.2, Negra 2019 2.6, 2.7 → 2.8), die umgekehrte Folge hat Lloyd 4.2 → 4.3, Veith 1.1 nennt die Ausnahme mit „except“ im selben Satz. Projektseite: Stellung nach Plan § 3 Task 11 und Textvorschlag 5 erfüllt (2b.28). Schluss mit dem Z1-Satz A6 S4, nach dem Codebuch kein Befundsatz, damit gegen Raster § 3.13 („Schluss = letzter Befundsatz mit Objektverweis“) teilweise, Textvorschlag 5 und Registerprüfung 10g lesen A6 S4 als Befundsatz (2b.13).', 'Korpus: nur erweitert · Fundstelle: teilweise (Raster § 3.13 nach dem Codebuch), Stellung erfüllt (2b.28)', 'bausteine_2c.txt § 2, Veith2021 1.1, 2.3, Asimakidis2022 1.1, 1.6, Hilska2021 4.2, 6.1, Rogers2020 1.3, 1.8, 2.1, Beato2018 4.1, 4.2, Negra2019 2.6 bis 2.8, Lloyd2016 4.2, 4.3')

PRUEF([r['primaer'] for r in STUD['Klusemann2012'] if r['satz'] in ('1.2', '1.3', '1.4', '1.5', '1.6')] == ['O2'] * 5
      and [r['primaer'] for r in STUD['Hilska2021'] if r['absatz'] == '7'] == ['O2'] * 5
      and [r['primaer'] for r in STUD['Veith2021'] if r['satz'] in ('3.2', '3.3', '3.4', '3.5')] == ['O2', 'O2', 'O2', 'X1']
      and [r['primaer'] for r in STUD['Rogers2020'] if r['satz'] in ('2.5', '2.6', '2.7')] == ['O2'] * 3, 'Teil B A2: mehrsätzige Umsetzung nur erweitert')
PRUEF('O4 O2 O3 X2 X1 B1 B4 X1' in bef, 'Teil B A3: Zugfolge Beato im Befund § 2.1')
PRUEF(SID[('PadronCabo2025', '1.1')]['primaer'] == 'X1' and 'O5' in sek(SID[('PadronCabo2025', '1.1')]) and SID[('PadronCabo2025', '1.2')]['primaer'] == 'O5'
      and STUD['Klusemann2012'][-1]['satz'] == '4.6' and STUD['Asimakidis2022'][-1]['satz'] == '1.7', 'Teil B A4: Messgüte erweitert vorn und am Schluss')
PRUEF(SID[('Sammoud2024', '2.1')]['woerter'] == '49' and text('Sammoud2024 2.1').count('d = ') == 5, 'Teil B A5: Sammoud 2.1 mit 49 Wörtern, fünf Tests mit d')

# Teil C: Funktionen ohne Muster
CODEZ = OrderedDict()
for code in ['V1', 'V2', 'Z1', 'Z2', 'O3']:
    CODEZ[code] = dict(kern=stud_code(code, 'Kern'), kern_prim=stud_code(code, 'Kern', prim=True), erw=stud_code(code, 'erw'),
                       erw_prim=stud_code(code, 'erw', prim=True), kap=[i for i in IDS if C(i) == code], kap_sek=[i for i in IDS if code in K[i][1]])
PRUEF(CODEZ['V1']['kern'] == [] and CODEZ['V1']['erw'] == ['Asimakidis2022', 'Hilska2021', 'Veith2021'], 'V1 Kern 0, erweitert 3')
PRUEF(CODEZ['V2']['kern_prim'] == [] and CODEZ['V2']['kern'] == ['Lloyd2016', 'Sammoud2024'] and len(CODEZ['V2']['erw']) == 4, 'V2 Kern sekundär 2, erweitert 4')
PRUEF(CODEZ['Z1']['kern_prim'] == [] and CODEZ['Z1']['kern'] == ['Liu2024', 'Moran2024'] and CODEZ['Z1']['erw_prim'] == ['Asimakidis2022'], 'Z1 Kern sekundär 2, erweitert primär Asimakidis')
PRUEF(CODEZ['Z2']['kern'] == [] and CODEZ['Z2']['erw'] == ['Klusemann2012', 'Veith2021'], 'Z2 Kern 0, erweitert 2')
PRUEF(CODEZ['O3']['kern'] == ['Beato2018'] and CODEZ['O3']['erw'] == ['Hilska2021'], 'O3 Kern Beato, erweitert Hilska')
PRUEF(CODEZ['V1']['kap'] == ['A6 S1', 'A6 S3'] and CODEZ['V2']['kap'] == ['A5 S11'] and CODEZ['V2']['kap_sek'] == ['A2 S4', 'A3 S2', 'A6 S4']
      and CODEZ['Z1']['kap'] == ['A6 S2', 'A6 S4'] and CODEZ['Z1']['kap_sek'] == ['A2 S4', 'A5 S2'] and CODEZ['Z2']['kap'] == ['A3 S3', 'A3 S4']
      and CODEZ['O3']['kap'] == ['A3 S1', 'A3 S2'], 'Sätze je Code in Kapitel 5')
RC = OrderedDict()
RC['V1'] = ('Funktion ohne Muster: V1 Datenprüfung', 'Korpus und Fundstelle',
            '§ 5.1 „Datenprüfung“ (Kern 0), § 2.2, § 3.1 · P8, F17 § 11.9, Zeile 16',
            'A6 S1 und A6 S3. Kern 0 als Primär- und Sekundärcode, erweitert in 3 Studien (Veith 1.1 und Asimakidis 1.1 primär, Hilska 6.1 und Veith 2.3 sekundär), jeweils am Anfang oder im Befundteil. In Kapitel 5 zwei Sätze nach den Befunden. Projektform: verworfene Prüfung mit Prüfgröße und p, übrige „geprüft und nicht verworfen“ (P8, F17 § 11.9, R2, O7), ein Satz zur verworfenen und ein Sammelsatz zu den übrigen (Zeile 16).',
            'Korpus: nur erweitert · Fundstelle: teilweise (2b.22)', 'bausteine_2c.txt § 5')
RC['V2'] = ('Funktion ohne Muster: V2 Analyseregel', 'Korpus und Fundstelle',
            'keine Zeile in § 5.1 · § 2.2 (V2 Kern 2, tragend 0, erweitert 4) · Raster 5.2.5, F17 § 3.2, § 10, R4',
            'A5 S11 primär, A2 S4, A3 S2 und A6 S4 sekundär. Kern primär 0, sekundär 2 Studien (Lloyd 1.3, Sammoud 1.1), erweitert primär 4 Sätze in 3 Studien (Rogers 1.2, 1.9, Hilska 6.1, Veith 2.3), im Korpus nie nach dem letzten Befund (2b.28), in Kapitel 5 A5 S11 nach der Entscheidung über H0. Projektform: Raster 5.2.5 (A5 S11), Zählregeln der Untergrenzen nach F17 § 3.2 (A2 S4), Load-Sprachregelung F17 § 10 (A3 S2), R4 (A6 S4).',
            'Korpus: nur erweitert · Fundstelle: erfüllt (2b.28)', 'bausteine_2c.txt § 5')
RC['Z1'] = ('Funktion ohne Muster: Z1 Zusatz- und Sensitivitätsanalysen', 'Korpus und Fundstelle',
            'keine Zeile in § 5.1 · § 2.2 (Z1 Kern 2, tragend 0, erweitert 3), § 3.7 · P8, P9, F17 § 3.2, § 11.6',
            'A6 S2 und A6 S4 primär, A2 S4 und A5 S2 sekundär. Kern primär 0, sekundär 2 Studien (Moran 1.1 bis 1.3, Liu 2.5, Objektsätze zu Einzelwerten), keine Sensitivitätsanalyse im Kern (§ 3.7). Erweitert primär Asimakidis 1.6 (individuelle Antworten nach den Befunden), sekundär Hilska 4.2 (Unteranalysen im Befundteil) und Rogers 1.3, 1.8, 2.1, 2.3, 2.4 (Responder). Projektform: Bootstrap-KI neben der verworfenen Prüfung (P8, R2), Sammelsatz aus Per-Protokoll und Sensitivität (P9, R1, R4), Untergrenzen „in 5.1 als Sensitivität“ (F17 § 3.2), Abb. 2 als Modellgrafik ohne Einzelwertdarstellung (F17 § 11.6).',
            'Korpus: nur erweitert · Fundstelle: erfüllt (2b.23)', 'bausteine_2c.txt § 5')
RC['Z2'] = ('Funktion ohne Muster: Z2 Schäden', 'Korpus und Fundstelle',
            '§ 5.1 „Ereignisse, Gründe“ (Kern 0), § 2.2, § 3.7 · P10, CONSORT 19, Raster 5.1.8',
            'A3 S3 und A3 S4. Kern 0, erweitert nur sekundär als Grund von Ausfällen oder verpassten Einheiten (Klusemann 1.1, 1.3, 1.6, Veith 3.3). In Kapitel 5 eigene Sätze im Orientierungszug, ohne Grund und ohne Kausalzuschreibung. Projektform: Meldungen und Spieler je Status, Kontrollgruppe ohne Instrument (P10, CONSORT 19, Raster 5.1.8), ohne Lokalisation (Register 9d), Bezugsmenge der neun Spieler offen (2b.45).',
            'Korpus: nur erweitert · Fundstelle: teilweise (2b.45)', 'bausteine_2c.txt § 5')
RC['O3'] = ('Funktion ohne Zeile in § 5.1: O3 Beanspruchung', 'Korpus und Fundstelle',
            'keine Zeile in § 5.1 · § 2.2 (O3 in 1), § 3.1, § 3.4 · Raster 5.1.7, F17 § 10, Register 3f',
            'A3 S1 und A3 S2. § 5.1 hat keine Zeile, § 2.2 nennt Beato als Beispiel: Kern O3 in 1 Studie (Beato 2.2, RPE je Gruppe mit M ± SD), erweitert Hilska 1.2 (Exposition je Gruppe) und 8.1 bis 8.3 (Begleitbedingungen der Kontrollgruppe). Projektform: CR-10 und sRPE-Load mit sechs Kennwerten im Satz (Raster 5.1.7), Load-Sprachregelung (F17 § 10), Klickentscheidung vom 24.09. Nr. 3 (Register 3f).',
            'Korpus: wie Muster · Fundstelle: erfüllt', 'bausteine_2c.txt § 5, Beato2018 2.2')
RC['SL'] = ('Funktion ohne Kernmuster: Fall C1 der Schlusslogik', 'Korpus und Fundstelle', '§ 3.4, § 3.5, § 6.4 · Umfangsdokument § 5.1 (C1), P5, P6, Register 3c', 'A5 S6 bis A5 S8. Nur der fehlende Nachweis (A5 S6) hat als Nullbefund ein Kernmuster in anderer Form (9 von 10). Lesart des Intervalls und Urteil haben im Kern kein Vorbild. Erweitert liest Klusemann Gruppenvergleiche über Schätzer ± 90-%-Grenzen mit dem Urteil „unclear“ (3.3, ohne Intervall im Satz 2.7 und 4.3), Nullformel und Intervall zugleich tragen dort nur Veränderungen je Gruppe (2.2, 2.5, 2.6, 4.4). Dass „unclear“ ein Intervall über beide Relevanzschwellen bezeichnet, ist an der Methodik zu bestätigen (2 d). Projektform: Musterformulierung C1 des Umfangsdokuments in drei Sätzen, abgewandelt im Präteritum, mit Quantor über drei Zielgrößen, „Unterschieden“ statt „Effekten“ und Plural (P6, Register 3c). Der Fall steht einmal für alle drei Zielgrößen, nicht je Zielgröße im Block, bewertet in 2c.34 (2b.9). Ein Vorbild für den Fall je Vergleich in der Klammer ist Klusemann 3.3.', 'Korpus: nur erweitert · Fundstelle: erfüllt (2b.19, 2b.20)', 'bausteine_2c.txt § 3 und § 5, Klusemann2012 2.2, 2.5, 2.6, 2.7, 3.3, 4.3, 4.4')
RC['SE'] = ('Funktion ohne Muster: Entscheidungsregel und Entscheidung über H0', 'Korpus und Fundstelle', '§ 3.7, § 0 Nr. 4 · 4.7 A3 S8, P7, Register 4a, 6f, 6k', 'A5 S9 und A5 S10. Kern 0 und erweitert 0: Kein Ergebnisteil entscheidet über eine Hypothese („Kein Ergebnisteil endet mit einem Resümee, keiner entscheidet über eine Hypothese.“, § 0 Nr. 4), Regeln mit Entscheidung stehen nur als Analyseregeln mit V2 (Rogers 1.9, Veith 2.3). Projektform: Entscheidungsregel in der Sprache von 4.7 (A5 S9, 4.7 A3 S8) und Entscheidung über H0 (A5 S10, P7), weder „Studienprotokoll“ noch „Ethikantrag“ im Kapitel (Register 6k).', 'Korpus: kein Muster · Fundstelle: erfüllt (2b.21)', 'bausteine_2c.txt § 3 und § 5, Rogers2020 1.9, Veith2021 2.3')
RC['UA'] = ('Funktion ohne Kernmuster: unadjustiert neben adjustiert', 'Korpus und Fundstelle',
            '§ 5.1 „unadjustiert neben adjustiert“ (Kern 0), § 3.7 · CONSORT 18, P4, Raster 5.2.2, Register 10n',
            'A5 S1 und A5 S3. Kern 0, erweitert Hilska 3.3, 4.1 und 6.4 (beide Schätzer mit 95-%-KI in einer Klammer, nach den Inzidenzen je Gruppe). Kapitel 5 setzt beide Werte in Tab. 3 (A5 S1) und nennt im Satz Richtung und Abstand der unadjustierten (A5 S3), vor dem Modellergebnis, Hilska nennt beide Schätzer im selben Satz nach dem Rohbefund. Projektform: CONSORT 18, P4, Raster 5.2.2 („der Abstand ist der Befund, nicht die Deutung“), kein unadjustierter p-Wert (Register 10n). Stellung von A5 S3 vor dem Modellergebnis ohne Entscheidung (2b.6).',
            'Korpus: nur erweitert · Fundstelle: erfüllt (2b.18)', 'bausteine_2c.txt § 3, Hilska2021 3.3, 4.1, 6.4')
RC['UM'] = ('Umsetzung jenseits der Rate (Teile ohne Kernvorbild)', 'Korpus und Fundstelle', '§ 5.1 „Umsetzung“ (Kern O2 in 5), § 3.1, § 6.4 · F17 § 3.2, Raster 5.1.6, 5.1.11', 'A2 S1, A2 S3 und A2 S4. Der Kern berichtet Raten (Lloyd 1.3, Beato 2.1, Negra 2019 1.3) oder dass alle Teilnehmer das Programm absolvierten (Negra 2020 1.2, Sammoud 1.1), Schwellen nur mit allen Teilnehmern darüber (Lloyd 1.3, Sammoud 1.1), alle Werte hoch (§ 3.1, § 6.4). Abgewandelt sind Meldungen nach Status, Median je Spieler, Spielerzahlen an Schwellen und Untergrenzen, die der Kern nicht hat. Erweitert stehen Spanne, Mittel, Schwellen mit Beleg und Einstufung (Rogers 1.9, 2.5 bis 2.7), Spieler an Schwellen (Klusemann 1.5), Anteile an Schwellen für Teams (Hilska 7.2, 7.4) und der Anteil vollständiger Durchführung (Veith 3.2). Untergrenzen nach zwei Zählregeln hat auch die Erweiterung nicht. Projektform: F17 § 3.2 (Zählregel, Untergrenzen „in 5.1 als Sensitivität“), Raster 5.1.6 und 5.1.11.', 'Korpus: abgewandelt · Fundstelle: erfüllt (2b.27)', 'bausteine_2c.txt § 3, Rogers2020 1.9, 2.5 bis 2.7, Klusemann2012 1.5, Hilska2021 7.2, 7.4, Veith2021 3.2')

# Teil D: Prüfpunkte aus Fortsetzungsübergabe 2 § 5 Nr. 4
OBJSAETZE = [i for i in IDS if M(i)['objekt_subjekt'] or M(i)['objekt_ort']]
PRUEF(OBJSAETZE == ['A1 S1', 'A1 S3', 'A5 S1', 'A5 S2'] and sum(M(i)['objekt_subjekt'] for i in OBJSAETZE) == 5 and sum(M(i)['objekt_ort'] for i in IDS) == 0,
      'vier Objektsätze, fünf Verweise als Subjekt, keine Ort-Form')
OBJFORM = {(g, f): sorted(r['studie'] + ' ' + r['satz'] for r in KORPUS if (r['studie'] in KERN) == (g == 'Kern') and r['objekt_' + f] != '0')
           for g in ('Kern', 'erw') for f in ('subjekt', 'ort')}
PRUEF([len(OBJFORM[('Kern', 'subjekt')]), len(OBJFORM[('Kern', 'ort')]), len(OBJFORM[('erw', 'subjekt')]), len(OBJFORM[('erw', 'ort')])] == [5, 10, 5, 5]
      and sorted({s.split(' ')[0] for s in OBJFORM[('erw', 'ort')]}) == ['Hilska2021', 'Rogers2020', 'Veith2021']
      and sorted({s.split(' ')[0] for s in OBJFORM[('erw', 'subjekt')]}) == ['Asimakidis2022', 'PadronCabo2025', 'Rogers2020'],
      'Objektformen: Kern Subjekt 5, Ort 10, erweitert je 5 in 3 Studien')
BLOCK = [('A5 S3', 'Quantor'), ('A5 S4', 'Modell'), ('A5 S5', 'Themenanker'), ('A5 S6', 'Quantor')]
PRUEF(all(MERK[i]['satzanfang'].startswith(a) for i, a in BLOCK), 'Blockanfänge A5 S3 bis S6')
PRUEF(TB['blockstart']['Modellterm'] == 9 and TB['blockstart']['Sammelbefund (B4)'] == 6 and TB['blockstart']['Konnektor'] == 4
      and TB['blockstart']['Zielgroesse, Befund oder Analyse als Subjekt'] == 11, 'Blockanfänge im Kern 9, 6, 4, 11')
ZUORD = OrderedDict([('A2 S1', 'als …'), ('A2 S3', 'direkte Paarung'), ('A3 S3', 'je'), ('A5 S5', 'Themenanker je Glied'), ('A2 S4', 'ohne Zuordnungswort')])
PRUEF(' als ' in T('A2 S1') and 'je zwei' in T('A3 S3') and 'beim Standweitsprung' in T('A5 S5'), 'Zuordnungsformen im Text')
PRUEF(len(TB['familien']['B_RESPECTIVELY']['ext_studien']) == 6 and [b[0] + ' ' + b[1] for b in TB['familien']['B_RESPECTIVELY']['belege'] if b[0] == 'Beato2018'][:3] == ['Beato2018 1.1', 'Beato2018 2.1', 'Beato2018 2.2'],
      '„respectively“ erweitert in 6 Studien, Beato 2.1 und 2.2 (Beato 1.1 als „respectfully“)')
RD = OrderedDict()
RD['OBJ'] = ('Prüfpunkt Objektsätze: Formen', 'Korpus und Fundstelle', '§ 5.1 „Objekt einführen, Subjekt“ (Kern 5 · 3) und „Objekt einführen, Ort“ (Kern 10 · 7), K3 · Stilprofil Teil 4, Plan § 3 Task 11, Raster § 3.12, Textvorschlag 5 § 0, Register 1e, U2', 'Kapitel 5 führt fünf Objekte in vier Objektsätzen ein (A1 S1, A1 S3, A5 S1, A5 S2), alle in der Subjektform im Präsens („zeigt“, „enthält“), die Ort-Form („… stehen in Tab. ⟨n⟩.“, Befund § 5.1 rechts) bleibt ungenutzt. Im Kern ist die Ort-Form die häufigere (10 Sätze in 7 Studien gegen 5 in 3), erweitert stehen beide gleich oft (je 5 Sätze in 3 Studien, Ort bei Hilska, Veith und Rogers, Subjekt bei Rogers, Padrón-Cabo und Asimakidis). Stilprofil Teil 4 und Register 1e lassen beide Formen zu, Plan § 3 Task 11, Raster § 3.12 und Textvorschlag 5 § 0 verlangen die Subjektform (Register 1e, U2). Die Ort-Form wiche vom freigegebenen Wortlaut ab.', 'Korpus: wie Muster · Fundstelle: erfüllt (Register 1e, U2)', 'bausteine_2c.txt § 6')
RD['BLOCK'] = ('Prüfpunkt Blockanfänge im Gruppenvergleich', 'Korpus und Fundstelle',
               '§ 3.3, K6, § 5.1 „Themenanker“ (als Blockbeginn 5 von 38) · F17 § 5a, Plan § 3 Task 11',
               'Vier Blöcke (2a.29): A5 S3 Quantor (nach dem Codebuch Einzelbefund), A5 S4 Modell als Partizip, A5 S5 Themenanker, A5 S6 Quantor. Kern 38 Blöcke: Zielgröße, Befund, Modellterm oder Analyse als Satzanfang 20 (davon Modellterm 9), Sammelbefund 6, Themenanker 5, Konnektor 4, Quantor über die Tests einer Zielgröße als Einzelbefund 1 (Hammami 1.3), Zeitangabe 1, Gruppe 1. Zwei der vier Blockanfänge (A5 S3, S6) haben die nächste Form, im Kern einmal (Hammami 1.3, Quantor über die Tests einer Zielgröße), A5 S3 und S6 quantifizieren über die drei konfirmatorischen Zielgrößen. A5 S4 entspricht dem Modellterm, A5 S5 dem Themenanker. Nach dem Hinweis H2 wären A5 S3 und S6 Sammelbefunde (Kern 6 von 38), das zählt nach der Zählregel nicht. Projektseite: je Zielgröße ein Block in fester Reihenfolge (F17 § 5a, Plan § 3 Task 11), teilweise erfüllt (2b.9).',
               'Korpus: abgewandelt · Fundstelle: teilweise (2b.9)', 'bausteine_2c.txt § 6, 2a.29')
RD['ZUORD'] = ('Prüfpunkt Zuordnung paralleler Werte', 'Korpus und Fundstelle', '§ 3.6 („respectively“ in 8 Sätzen aus 5 Studien) · Stilprofil Teil 3, Register r1', 'Parallele Werte ordnet der Kern mit „respectively“ zu (8 Sätze in 5 Kernstudien, erweitert in 6 Studien), darunter Umsetzung und Beanspruchung bei Beato (2.1, 2.2), mit „=“ (Lloyd 1.3) oder mit Bezeichnungen in der Klammer (Aloui 3.1, 4.1). Erweitert ordnet Klusemann auch über die Folge ohne Zuordnungswort zu, die Bezugsfolge im selben Satz (2.3, 2.5, 4.1). Kapitel 5 ordnet zu über „als …“ (A2 S1), direkte Paarung (A2 S3), „je“ (A3 S3) und einen Themenanker je Glied (A5 S5). Nur A2 S4 ordnet die Paare „neun und zwei“ und „neun und einer“ über die Folge der Schwellen zu, deren Bezugsfolge im vorigen Satz steht (A2 S3), dafür hat der Korpus kein Vorbild. Für Schritt 3 vorgemerkt: neben einem Zuordnungswort die Bezugsfolge im Satz. Projektseite: keine Regel in § 5.1, Stilprofil Teil 3 (eine Aussage je Satz, Komma-Ausnahme, 2b.47), Leseführung (2b.34).', 'Korpus: abgewandelt · Fundstelle: keine Regel', 'bausteine_2c.txt § 6, Beato2018 2.1, 2.2, Lloyd2016 1.3, Aloui2022 3.1, 4.1, Klusemann2012 2.3, 2.5, 4.1')
RD['AUSN'] = ('Prüfpunkt Ausnahmen in eigenem Satz', 'Korpus und Fundstelle', '§ 5.1 „Sammelbefund mit Ausnahme“ (Kern in Sammelbefunden 3 · 2), § 3.5, § 7 Nr. 5 · Stilprofil Teil 3', 'Der Kern nennt Ausnahmen im selben Satz mit „except“ (in Sammelbefunden 3 Sätze in 2 Studien: Negra 2020 1.4, 1.5, Bouafif 1.1, dazu Sammoud 1.5 beim Ausgangsvergleich) oder in eigenem Satz, davor (Beato 4.1 → 4.2, Negra 2019 2.6, 2.7 → 2.8) oder danach (Lloyd 4.2 → 4.3, § 7 Nr. 5), erweitert mit „except“ bei einem Sammelbefund (Klusemann 2.2) und bei der Datenprüfung („All data except age were normally distributed.“, Veith 1.1). Kapitel 5 stellt Ausnahmen in eigene Sätze, A5 S11 hinter die drei konfirmatorischen Zielgrößen, A6 S1 vor die übrigen Prüfungen (A6 S3), beide Folgen haben Kernvorbilder. Stilprofil Teil 3 verlangt den eigenen Satz („Eine Aussage je Satz, Ausnahmen in einen eigenen Satz.“), die Folge „erst die Regel …, dann die Einschränkung“ gilt dort für Bedingungen. § 5.1 nennt für Ausnahmen keine Projektregel („keine eigene Projektregel (K8)“).', 'Korpus: wie Muster · Fundstelle: keine Regel', 'bausteine_2c.txt § 6, Negra2020 1.4, 1.5, Bouafif2026 1.1, Beato2018 4.1, 4.2, Negra2019 2.6 bis 2.8, Lloyd2016 4.2, 4.3, Klusemann2012 2.2, Veith2021 1.1')

# ---------------------------------------------------------------- § 4 Prüfbedingungen
aus('4 Prüfbedingungen der Handurteile je Satz (alle bestanden)')
for i in IDS:
    for ok, txt in PB[i]:
        PRUEF(ok, i + ': ' + txt)
    aus('  ' + i.ljust(7), ' · '.join(txt for _, txt in PB[i]))
aus('')

# ---------------------------------------------------------------- § 5 Funktionen ohne Muster
aus('5 Funktionen ohne Muster: Studien mit dem Code (primär oder sekundär), Kern und erweitert, Sätze in Kapitel 5')
for code, d in CODEZ.items():
    aus('  ' + code, '| Kern', len(d['kern']), d['kern'], '(primär', len(d['kern_prim']), ') | erweitert', len(d['erw']), d['erw'], '(primär', len(d['erw_prim']),
        ') | Kapitel 5 primär', d['kap'], '· sekundär', d['kap_sek'])
aus('  Schlusslogik: Nullformel und Intervall zugleich nur Klusemann 2.2, Intervall der Ausnahme (PB A5 S7) · „hypothes…“ in der Anlage 0 (PB A5 S9)')
aus('  Umsetzung: Schwellen im Kern', KERN_SCHWELLE, '· „lower bound“ in der Anlage 0 · „median“ nur Moran 1.2 (Objektsatz)')
aus('')

# ---------------------------------------------------------------- § 6 Prüfpunkte Fortsetzung 2 § 5 Nr. 4
aus('6 Prüfpunkte aus Fortsetzungsübergabe 2 § 5 Nr. 4')
aus('  Objektsätze:', OBJSAETZE, '· Subjekt-Verweise', sum(M(i)['objekt_subjekt'] for i in OBJSAETZE), '· Ort-Form', sum(M(i)['objekt_ort'] for i in IDS),
    '· Kern Subjekt', fam('OBJ_SUBJEKT'), 'Ort', fam('OBJ_ORT'), '· erweitert Subjekt', OBJFORM[('erw', 'subjekt')], 'Ort', OBJFORM[('erw', 'ort')])
aus('  Blockanfänge A5:', ' · '.join(i + ' ' + MERK[i]['satzanfang'] for i, _ in BLOCK))
aus('  Blockanfänge Kern:', dict(TB['blockstart']))
aus('  Zuordnung paralleler Werte:', ' · '.join(i + ' ' + v for i, v in ZUORD.items()), '· Kern „respectively“', fam('B_RESPECTIVELY'))
aus('  Ausnahmen: Kern „except“', saetze_rx(r'\bexcept\b', 'Kern'), '· erweitert', saetze_rx(r'\bexcept\b', 'erw'))
aus('  unadjustiert vor adjustiert: A5 S3 vor A5 S4 (2b.6) · Fall C1 in A5 S6 bis S8 · Schlusssatz A6 S4 (2c.29, 2b.13) · Sequenz 2 für A5 (2c.34)')
aus('')

# ---------------------------------------------------------------- Teiltabelle 2c zusammenstellen
ZEILEN = []
for i, r in RA.items():
    w = SATZ[i]['text'].split(' ')
    anf = ' '.join(w[:6]) + (' …' if len(w) > 6 else '')
    code = C(i) + (' (' + ', '.join(K[i][1]) + ')' if K[i][1] else '')
    ZEILEN.append([i + ' · ' + code + ' · ' + r[0], r[1], r[2], i + ' „' + anf + '“', r[3], r[4], r[5]])
for a, r in RB.items():
    ZEILEN.append([r[0], r[1], r[2], a + ' (' + ' '.join(KAP[a]) + ')', r[3], r[4], r[5]])
for k, r in RC.items():
    stellen = {'V1': 'A6 S1, S3', 'V2': 'A5 S11, sekundär A2 S4, A3 S2, A6 S4', 'Z1': 'A6 S2, S4, sekundär A2 S4, A5 S2', 'Z2': 'A3 S3, S4',
               'O3': 'A3 S1, S2', 'SL': 'A5 S6 bis S8', 'SE': 'A5 S9, S10', 'UA': 'A5 S1, S3', 'UM': 'A2 S1, S3, S4'}[k]
    ZEILEN.append([r[0], r[1], r[2], stellen, r[3], r[4], r[5]])
for k, r in RD.items():
    stellen = {'OBJ': 'A1 S1, S3, A5 S1, S2', 'BLOCK': 'A5 S3 bis S6', 'ZUORD': 'A2 S1, S3, S4, A3 S3, A5 S5', 'AUSN': 'A5 S11, A6 S1, S3'}[k]
    ZEILEN.append([r[0], r[1], r[2], stellen, r[3], r[4], r[5]])
PRUEF(len(ZEILEN) == 48, '48 Zeilen')

KSTAT = ('wie Muster', 'abgewandelt', 'nur erweitert', 'kein Muster')
STATUSREGELN = ['Funktion ist der Baustein von § 5.1, dem der Satz dient, ohne passende Zeile der Code nach dem Codebuch (§ 2.2, Zählregel § 6.5). Lesart des Intervalls, Urteil und Entscheidung der Schlusslogik (A5 S7 bis S10) zählen als eigene Funktionen, der Befund führt sie gesondert (§ 3.5, § 3.7, § 6.4).',
                'Korpus wie Muster: Kernbaustein der Funktion in derselben Bauform, Gegenstand und Statistik im Satz zählen nicht (§ 5.2). Abgewandelt: Kernbaustein der Funktion, Bauform verändert oder um einen Teil ohne Kernvorbild ergänzt. Nur erweitert: Die Funktion hat im Kern keinen Baustein (Kern 0 oder nur als Sekundärcode), die erweiterte Gruppe hat einen. Kein Muster: weder Kern noch erweiterte Gruppe. Teil B entsprechend für die Zugfolge.',
                'Fundstelle gilt der Projektregel der Funktion (rechte Spalte von § 5.1 oder ihre Fundstelle), Stilbefunde (2b.46, 2b.47) stehen im Ergebnis. Bewusst anders nur mit Entscheidung und Fundstelle. Ein 2b-Verweis steht hinter dem Statuswort, das er belegt, und zeigt auf eine 2b-Zeile mit Maßstab Fundstelle, die dasselbe Statuswort trägt.']
FSTAT = ('erfüllt', 'teilweise', 'nicht erfüllt', 'bewusst anders', 'keine Regel')
TAB = []
for n, z in enumerate(ZEILEN, 1):
    nr = '2c.' + str(n)
    PRUEF(z[1] in ('Korpus', 'Fundstelle', 'Korpus und Fundstelle'), 'Maßstab ' + nr)
    m = re.match(r'^Korpus: (.+?) · Fundstelle: (.+)$', z[5])
    PRUEF(bool(m), 'Statusform ' + nr)
    ks, fs = m.group(1), m.group(2)
    PRUEF(ks in KSTAT, 'Korpusstatus ' + nr + ': ' + ks)
    fs0 = next((s for s in FSTAT if fs.startswith(s)), None)
    PRUEF(fs0 is not None, 'Fundstellenstatus ' + nr + ': ' + fs)
    segs = re.findall(r'(nicht erfüllt|erfüllt|teilweise|bewusst anders|keine Regel)[^()]*\(([^)]*)\)', fs)
    PRUEF(sorted(re.findall(r'2b\.\d+', fs)) == sorted(x for _, inner in segs for x in re.findall(r'2b\.\d+', inner)), nr + ': jeder 2b-Verweis der Statusspalte steht hinter einem Statuswort')
    for wort, inner in segs:
        for ref in re.findall(r'2b\.(\d+)', inner):
            st2b = Z2B['2b.' + ref]['Status'].split(' · ')[0]
            PRUEF(wort in st2b, nr + ': Status von 2b.' + ref + ' trägt „' + wort + '“ (' + st2b + ')')
            PRUEF(Z2B['2b.' + ref]['Befundstelle'].startswith(('Fundstelle', 'Korpus und Fundstelle')), nr + ': 2b.' + ref + ' mit Maßstab Fundstelle')
    for ref in re.findall(r'2b\.(\d+)', z[4]):
        PRUEF('2b.' + ref in Z2B, nr + ': Verweis 2b.' + ref)
    for ref in re.findall(r'2c\.(\d+)', z[4]):
        PRUEF(1 <= int(ref) <= len(ZEILEN), nr + ': Verweis 2c.' + ref)
    for ref in re.findall(r'2a\.(\d+)', z[4] + z[6]):
        PRUEF(1 <= int(ref) <= 42, nr + ': Verweis 2a.' + ref)
    PRUEF(SK not in ''.join(z), 'kein Semikolon in ' + nr)
    TAB.append([nr, z[0], z[1] + ' · ' + z[2], z[3], z[4], z[5], z[6], ks, fs0])

# Registerkennungen der Spalten Befundstelle, Ergebnis und Status
REGTXT = lies(os.path.join(HIER, 'register_pruefung.md'))
REG = set(re.findall(r'^\| ([0-9]{1,2}[a-z]|[UVO][0-9]+) \|', REGTXT, re.M)) | {'c' + str(n) for n in range(1, 10)} | {'r' + str(n) for n in range(1, 5)}
reg_verwendet = sorted({m for z in TAB for m in re.findall(r'Register ((?:\d{1,2}[a-z]|[UVOcr]\d+)(?:, (?:\d{1,2}[a-z]|[UVOcr]\d+))*)', z[2] + ' ' + z[4] + ' ' + z[5])
                        for m in m.split(', ')})
PRUEF(all(m in REG for m in reg_verwendet), 'Registerkennungen vorhanden: ' + ', '.join(m for m in reg_verwendet if m not in REG))

# ---------------------------------------------------------------- § 7 Zitatprüfung am genannten Ort
NT = {k: norm(v) for k, v in TXT.items()}
NT['anlage'] = norm(' '.join(r['text'] for r in KORPUS))
NT['kap5'] = norm(ALLE)
NT['master'] = norm(' '.join(s['text'] for s in MS))
NT['register'] = norm(REGTXT)
NTF = {k: v.casefold() for k, v in NT.items()}
STUDNAME = OrderedDict([('Negra 2019', 'Negra2019'), ('Negra 2020', 'Negra2020'), ('Padrón-Cabo', 'PadronCabo2025'), ('Lloyd', 'Lloyd2016'),
                        ('Hammami', 'Hammami2016'), ('Beato', 'Beato2018'), ('Aloui', 'Aloui2022'), ('Liu', 'Liu2024'), ('Moran', 'Moran2024'),
                        ('Sammoud', 'Sammoud2024'), ('Bouafif', 'Bouafif2026'), ('Hilska', 'Hilska2021'), ('Klusemann', 'Klusemann2012'),
                        ('Veith', 'Veith2021'), ('Rogers', 'Rogers2020'), ('Asimakidis', 'Asimakidis2022')])
PRUEF(sorted(STUDNAME.values()) == sorted(STUD), 'Studiennamen der Ortsprüfung')
NUMRX = r'\d+\.\d+'
RX_STUD = re.compile('(' + '|'.join(re.escape(k) for k in STUDNAME) + ')((?: ' + NUMRX + '(?:(?:, | und | bis )' + NUMRX + ')*)?)')
MARKER = [(r'Stilprofil\b', 'stil'), (r'F17\b', 'f17'), (r'Textvorschlag 5\b', 'tv5'), (r'Umfangsdokument\b', 'umfang'), (r'Raster\b', 'raster'),
          (r'Plan\b', 'plan'), (r'4\.\d A\d S\d+', 'master'), (r'Register\b', 'register'), (r'Befund\b', 'befund'), (r'§ \d', 'befund')]


def satzliste(studie, nums):
    alle = [r['satz'] for r in STUD[studie]]
    if not nums.strip():
        return alle
    out = []
    for t in re.split(r', | und ', nums.strip()):
        if ' bis ' in t:
            a, b = t.split(' bis ')
            out += alle[alle.index(a):alle.index(b) + 1]
        else:
            out.append(t)
    return out


def ort(rest):
    # Ortsangabe unmittelbar hinter dem Zitat: „…“ (Ort) oder „…“, Ort
    s = rest[re.match(r'[,:]? ?\(?', rest).end():]
    m = RX_STUD.match(s)
    if m:
        st = STUDNAME[m.group(1)]
        nums = satzliste(st, m.group(2))
        PRUEF(all((st, n) in SID for n in nums), 'Satzangabe ' + m.group(0))
        return m.group(1) + m.group(2), norm(' '.join(SID[(st, n)]['text'] for n in nums)).casefold()
    for rx, k in MARKER:
        if re.match(rx, s):
            return k, NTF[k]
    return None, None


def stuecke(q):
    # Bruchstücke ab vier Zeichen, an Wortgrenzen, offen nur an der Seite einer Auslassung
    teile_q = q.split('…')
    out = []
    for j, t in enumerate(teile_q):
        f = norm(t)
        if len(f) < 4:
            continue
        links = '' if j > 0 or not f[0].isalnum() else r'(?<!\w)'
        rechts = '' if j < len(teile_q) - 1 or not f[-1].isalnum() else r'(?!\w)'
        out.append(links + re.escape(f.casefold()) + rechts)
    return out


aus('7 Zitatprüfung: jedes Zitat in „…“ der Spalte Ergebnis am genannten Ort (Studie mit Satz, Befund oder Paragraf, Steuerdokument, Registerbericht),',
    'ohne Ortsangabe in allen Quelltexten, Groß- und Kleinschreibung gleichgesetzt, an Wortgrenzen, Auslassung „…“ teilt in Bruchstücke')
fehlt = []
zahl = Counter()
for z in TAB:
    for mq in re.finditer(r'„([^“]+)“', z[4]):
        q = mq.group(1)
        rx = stuecke(q)
        if not rx:
            zahl['kurz'] += 1
            aus('  kurz      ' + z[0].ljust(7), q)
            continue
        name, hay = ort(z[4][mq.end():])
        if name:
            ok = all(re.search(x, hay) for x in rx)
            wo = 'am Ort ' + name
            zahl['am Ort'] += 1
        else:
            orte = [k for k in NTF if all(re.search(x, NTF[k]) for x in rx)]
            ok = bool(orte)
            wo = 'frei, ' + (orte[0] if orte else '—')
            zahl['ohne Ort'] += 1
        if not ok:
            fehlt.append((z[0], q, wo))
        aus('  ' + ('gefunden' if ok else 'FEHLT').ljust(9), z[0].ljust(7), wo[:30].ljust(31), q[:90])
PRUEF(fehlt == [], 'alle Zitate gefunden: ' + str(fehlt))
aus('  ' + str(sum(zahl.values())), 'Zitate:', zahl['am Ort'], 'am genannten Ort gefunden,', zahl['ohne Ort'], 'ohne Ortsangabe in den Quelltexten gefunden,', zahl['kurz'], 'unter vier Zeichen')
aus('')

# ---------------------------------------------------------------- § 8 Zählung und Ausgaben
kz = Counter(z[7] for z in TAB)
fz = Counter(z[8] for z in TAB)
teile = OrderedDict([('A je Satz', TAB[:29]), ('B je Absatz', TAB[29:35]), ('C Funktionen ohne Muster', TAB[35:44]), ('D Prüfpunkte', TAB[44:])])
aus('8 Teiltabelle 2c (Registerkennungen verwendet, alle vorhanden:', ', '.join(reg_verwendet) + ')')
for t in STATUSREGELN:
    aus('  Regel: ' + t)
aus('  ', len(TAB), 'Zeilen · Korpus:', ' · '.join(k + ' ' + str(kz[k]) for k in KSTAT), '· Fundstelle:', ' · '.join(k + ' ' + str(fz[k]) for k in FSTAT))
for t, zz in teile.items():
    aus('  Teil ' + t + ':', len(zz), 'Zeilen · Korpus', dict(Counter(z[7] for z in zz)), '· Fundstelle', dict(Counter(z[8] for z in zz)))
wort_k = Counter()
for i, z in zip(IDS, TAB[:29]):
    wort_k[z[7]] += SATZ[i]['woerter']
PRUEF(sum(wort_k.values()) == 450, 'Wörter der 29 Sätze 450')
aus('  Teil A nach Wörtern (450):', ' · '.join(k + ' ' + str(wort_k[k]) for k in KSTAT))
aus('  Teil A je Absatz:', ' · '.join(a + ' ' + '/'.join(TAB[IDS.index(i)][7].replace('wie Muster', 'W').replace('abgewandelt', 'A').replace('nur erweitert', 'E').replace('kein Muster', 'K') for i in ABS[a]) for a in ABS),
    '(W wie Muster, A abgewandelt, E nur erweitert, K kein Muster)')
aus('  je Satz nach Primärcode:', ' · '.join(c + ' ' + str(n) for c, n in Counter(C(i) for i in IDS).most_common()))
with open(os.path.join(AUS, 'teiltabelle_2c.csv'), 'w', newline='', encoding='utf-8') as fo:
    w = csv.writer(fo, delimiter=SK, quoting=csv.QUOTE_ALL)
    w.writerow(['Nr.', 'Prüfgegenstand', 'Befundstelle', 'Fundstelle im Text', 'Ergebnis', 'Status', 'Beleg'])
    for z in TAB:
        w.writerow(z[:7])
with open(os.path.join(AUS, 'teiltabelle_2c.md'), 'w', encoding='utf-8') as fo:
    fo.write('| Nr. | Prüfgegenstand | Befundstelle | Fundstelle im Text | Ergebnis | Status | Beleg |\n')
    fo.write('|---|---|---|---|---|---|---|\n')
    for z in TAB:
        fo.write('| ' + ' | '.join(c.replace('|', '/') for c in z[:7]) + ' |\n')
with open(os.path.join(AUS, 'bausteine_2c.txt'), 'w', encoding='utf-8') as fo:
    fo.write('\n'.join(AUSGABE) + '\n')
print('Teiltabelle 2c:', len(TAB), 'Zeilen · Korpus', dict(kz), '· Fundstelle', dict(fz))

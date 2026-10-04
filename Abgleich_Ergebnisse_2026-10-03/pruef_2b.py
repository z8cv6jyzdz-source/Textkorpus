# -*- coding: utf-8 -*-
"""
pruef_2b.py — Teilschritt 2 (b), 03.10.2026: Prüfkatalog des Befunds § 6.5 Nr. 1 bis 10, Bauregeln K1 bis K10
(Zählregel: Code nach dem Codebuch), Projektregeln P1 bis P12 (gegen ihre Fundstelle) und die übrigen Aussagen des
Befunds, die Kapitel 5 berühren, am Textstand von Kapitel 5. Dazu die Prüfpunkte aus Fortsetzungsübergabe 1 § 5 Nr. 4.

Eingänge im Ordner des Skripts: textstand.json, eigen.json, abgleich_2a.json, master_saetze.json, konsens_2a.py.
Eingänge im Claude-Ordner (Pfade in QUELLEN): Befund, Anlage …_Saetze.csv, Fassung 17, Stilprofil, Gliederung v6,
Berichtsraster, Plan, Textvorschlag 5, Textvorschlag 6.1, Übergabe mit Register, Umfangsdokument (Umwandlung in quellen),
Kennzahlenblatt (Werte.csv), Memo des Codierers B, Bericht der Registerprüfung.

Ausgaben: pruef_2b.txt (Belege, Abschnittsnummern 0 bis 17 sind die Belege der Teiltabelle), teiltabelle_2b.csv
(Trennzeichen chr(59), alle Felder in Anführungszeichen), teiltabelle_2b.md (Tabelle für § 3.2 des Abgleichbefunds).

Die Spalte Ergebnis setzt gemessene Werte aus den Abschnitten ein. Handurteile stehen im Wortlaut der Zeilen und werden
durch PRUEF-Bedingungen an die Messung gebunden: Weicht ein Wert ab, bricht das Skript ab. Jede wörtlich angeführte
Fundstelle wird in § 16 am Quelltext gesucht (Zitatprüfung, dazu Kapitel 5, die Sätze des Masters und die Anlage), fehlt eine,
bricht das Skript ab. Die Spalte Befundstelle beginnt mit dem Maßstab der Zeile: Korpus (Zählregel des Befunds § 6.5, Code
nach dem Codebuch), Fundstelle (Projektregel oder Steuerdokument) oder beides.

Aufruf: python pruef_2b.py [<Claude-Ordner>] [<Ausgabeordner>]
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
import statistics
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
    ('f17', ['00_Steuerung', 'Projektanweisungen_Fassung17.md']),
    ('stil', ['01_Verfahren', 'Stilprofil_2026-09-13.md']),
    ('gliederung', ['01_Verfahren', 'Gliederung_2026-09-28.md']),
    ('raster', ['02_Befunde', 'Berichtsraster_2026-09-23.md']),
    ('plan', ['04_Uebergaben', 'Plan_Weitere_Schritte_2026-09-25.md']),
    ('tv5', ['04_Uebergaben', 'Textvorschlag_5_2026-09-30.md']),
    ('tv61', ['04_Uebergaben', 'Textvorschlag_6.1_2026-10-02.md']),
    ('uebergabe', ['04_Uebergaben', 'Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md']),
    ('umfang', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'quellen', 'Auswertungs_und_Berichtsumfang_2026-09-24.md']),
    ('werte', ['02_Befunde', 'Kennzahlen_2026-09-25_Werte.csv']),
    ('memo_b', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'blind', 'memo_B.md']),
    ('register', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'register_pruefung.md']),
])
LOKAL = ['textstand.json', 'eigen.json', 'abgleich_2a.json', 'master_saetze.json', 'konsens_2a.py']


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


def pz(x, n=1):
    return ('{:.' + str(n) + 'f}').format(x).replace('.', ',')


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
TXT = {k: lies(pfad(k)) for k in QUELLEN if k not in ('anlage', 'werte')}

SATZ = OrderedDict()
for a in TS['absaetze']:
    for s in a['saetze']:
        SATZ[s['id']] = s
IDS = list(SATZ.keys())
MERK = {s['id']: s for s in EI['saetze']}
K = konsens_2a.K
KH = konsens_2a.KH
PRUEF(IDS == list(K.keys()), 'Satzfolge textstand.json gleich konsens_2a.K')
PRUEF(len(IDS) == 29, '29 Sätze')


def T(i):
    return SATZ[i]['text']


def W(i):
    return SATZ[i]['woerter']


KORPUS = list(csv.DictReader(open(pfad('anlage'), encoding='utf-8'), delimiter=SK))
STUD = OrderedDict()
for r in KORPUS:
    STUD.setdefault(r['studie'], []).append(r)
KERN = [s for s in STUD if STUD[s][0]['gruppe'] == 'Kern']
ERW = [s for s in STUD if STUD[s][0]['gruppe'] != 'Kern']
PRUEF(len(KERN) == 10 and len(ERW) == 6, 'Kern 10, erweitert 6')


def sek(r):
    return [c for c in r['sekundaer'].split(SK) if c]


WERTE = {}
for r in csv.DictReader(open(pfad('werte'), encoding='utf-8')):
    WERTE[r['k_kennung']] = r

# ---------------------------------------------------------------- § 0 Eingänge
aus('Teilschritt 2 (b), pruef_2b.py — Belege der Teiltabelle 2b (Abgleichbefund § 3.2)')
aus('')
aus('0 Eingänge (MD5)')
for f in LOKAL:
    aus('  ' + f.ljust(62), md5(os.path.join(HIER, f)))
for k in QUELLEN:
    aus('  ' + '/'.join(QUELLEN[k]).ljust(62), md5(pfad(k)))
aus('')

# ---------------------------------------------------------------- § 1 Umfang und Gewicht
U = A2['umfang']
G = A2['anteile']['Codebuch']['gruppe']
PRUEF(U['W'] == 450 and U['P'] == 6 and U['S'] == 29, 'Umfang 450, 6, 29')
anteil_b = 100 * G['B'] / U['W']
anteil_vz = 100 * (G['V'] + G['Z']) / U['W']
anteil_o = 100 * G['O'] / U['W']
rahmen = A2['rahmen']['Codebuch']
kern_b, kern_b_ohne_b2 = {}, {}
for s in KERN:
    rs = STUD[s]
    w = sum(int(r['woerter']) for r in rs)
    b = sum(int(r['woerter']) for r in rs if r['primaer'].startswith('B'))
    b2 = sum(int(r['woerter']) for r in rs if r['primaer'] == 'B2')
    kern_b[s] = 100 * b / w
    kern_b_ohne_b2[s] = 100 * (b - b2) / (w - b2)
med_b2 = statistics.median(kern_b_ohne_b2.values())
min_b2 = min(kern_b_ohne_b2.values())
max_b2 = max(kern_b_ohne_b2.values())
unter_k5 = sorted(s for s in KERN if kern_b_ohne_b2[s] < anteil_b)
PRUEF(round(statistics.median(kern_b.values()), 1) == 72.5, 'Kernmedian Befundanteil 72,5 wie Befund')
PRUEF(unter_k5 == ['Moran2024'], 'ohne B2 liegt nur Moran unter Kapitel 5')
naechste_b2 = min((v, s) for s, v in kern_b_ohne_b2.items() if s != 'Moran2024')
PRUEF(naechste_b2[1] == 'Beato2018' and naechste_b2[0] > anteil_b, 'nächste Kernstudie ohne B2 ist Beato, über Kapitel 5')
PRUEF(all(r['primaer'] == 'B2' for r in STUD['Moran2024'] if r['primaer'].startswith('B')), 'Moran: alle Befundsätze B2')
# Rasterzeilen je Satz aus Textvorschlag 5 § 4
tv5 = TXT['tv5']
abschnitt4 = tv5.split('## 4 Rasterzuordnung')[1].split('## 5 ')[0]
RASTER = {}
for z in abschnitt4.split('\n'):
    m = re.match(r'^\| (A\d S\d+) \| .*? \| (.*) \|$', z)
    if m:
        RASTER[m.group(1)] = (re.findall(r'(\d\.\d\.\d+) \((P°|P|E)[ ,)]', m.group(2)), re.findall(r'\((P°|P|E)[ ,)]', m.group(2)))
PRUEF(len(RASTER) == 29, 'TV5 § 4 mit 29 Sätzen')
vor_ids = IDS[:IDS.index(rahmen['erster_befund'])]
PRUEF(len(vor_ids) == 16, '16 Sätze vor dem ersten Befund')
vor_ohne_pe = [i for i in vor_ids if not [e for e in RASTER[i][1] if e in ('P', 'P°', 'E')]]
PRUEF(vor_ohne_pe == [], 'jeder Satz vor dem ersten Befund trägt eine P- oder E-Zeile')
aus('1 Umfang und Gewicht (Prüfkatalog Nr. 1, Prüfpunkt Befundanteil und Rahmen)')
aus('  Wörter', U['W'], '· Absätze', U['P'], '· Sätze', U['S'], '· Median Satzlänge', U['med'], '· längster Satz', U['maxsatz'])
aus('  Codegruppen nach Codebuch (Wörter):', G, '· B', pz(anteil_b), '% · O', pz(anteil_o), '% · V+Z', pz(anteil_vz), '%')
aus('  Kern Befundanteil (B in % der Wörter): Median', pz(statistics.median(kern_b.values())), '· Spanne', pz(min(kern_b.values())), 'bis', pz(max(kern_b.values())))
aus('  Nachrechnung: Kern ohne B2-Sätze (Zähler und Nenner ohne B2): Median', pz(med_b2), '· Spanne', pz(min_b2), 'bis', pz(max_b2))
for s in KERN:
    aus('    ' + s.ljust(14), 'B', pz(kern_b[s]).rjust(6), '· ohne B2', pz(kern_b_ohne_b2[s]).rjust(6))
aus('  Kernstudien ohne B2 unter Kapitel 5 (' + pz(anteil_b) + ' %):', ', '.join(unter_k5), '(alle Befundsätze B2) · nächste darüber:', naechste_b2[1], pz(naechste_b2[0]), '%')
aus('  Rasterzeilen der Sätze vor dem ersten Befund (Textvorschlag 5 § 4):')
for i in vor_ids:
    aus('    ' + i.ljust(7), ' · '.join(z + ' ' + e for z, e in RASTER[i][0]) or ' · '.join(RASTER[i][1]))
aus('')

# ---------------------------------------------------------------- § 2 Rahmen vor dem ersten Befund (K1)
vor_codes = [K[i][0] for i in vor_ids]
z_vor = [i for i in vor_ids if K[i][0].startswith('Z')]
aus('2 Rahmen vor dem ersten Befund (K1)')
aus('  Kapitel 5: erster Befund', rahmen['erster_befund'], '·', rahmen['saetze_vor'], 'Sätze ·', rahmen['vor'], 'Wörter =', pz(100 * rahmen['vor'] / U['W']), '%')
aus('  Codes vor dem ersten Befund:', ' '.join(vor_codes), '· Z-Sätze:', ', '.join(z_vor), '(' + str(sum(W(i) for i in z_vor)) + ' Wörter)')
kern_mit_rahmen = 0
z2_prim_vor, z2_sek_vor = [], []
for s in STUD:
    rs = STUD[s]
    fb = next((n for n, r in enumerate(rs) if r['primaer'].startswith('B')), len(rs))
    vor = rs[:fb]
    if s in KERN and fb > 0:
        kern_mit_rahmen += 1
    for r in vor:
        if r['primaer'] == 'Z2':
            z2_prim_vor.append(s + ' ' + r['satz'])
        if 'Z2' in sek(r):
            z2_sek_vor.append(s + ' ' + r['satz'])
    aus('  ' + s.ljust(15), rs[0]['gruppe'].ljust(16), 'vor dem ersten Befund:', ' '.join(r['primaer'] for r in vor) or '—')
PRUEF(kern_mit_rahmen == 8, 'K1 8 von 10')
PRUEF(z2_prim_vor == [], 'Z2 nie als Primärcode vor dem ersten Befund')
aus('  Kern mit Rahmen vor dem ersten Befund:', kern_mit_rahmen, 'von 10 · Z2 primär vor dem ersten Befund: keiner · Z2 sekundär vor dem ersten Befund:', ', '.join(z2_sek_vor))
aus('')

# ---------------------------------------------------------------- § 3 Objekte (K3)
OBJ_RE = re.compile(r'(Tab\. H?\d|Abb\. H?\d)')
k5_obj = OrderedDict()
for i in IDS:
    for o in OBJ_RE.findall(T(i)):
        k5_obj.setdefault(o, []).append(i)
vor_k5 = OrderedDict()
for s in MS:
    if s['abschnitt'] in ('5',) or s['abschnitt'].startswith('6') or s['abschnitt'].startswith('Anhang'):
        continue
    for o in OBJ_RE.findall(s['text']):
        vor_k5.setdefault(o, []).append(s['id'])
erst_k5 = [o for o in k5_obj if o not in vor_k5]
wieder_k4 = [o for o in k5_obj if o in vor_k5]
erst = A2['objekte']['erstnennung']
erst_k5_objsatz = [o for o in erst_k5 if erst[o][1] == 'Objektsatz']
erst_k5_klammer = [o for o in erst_k5 if erst[o][1] != 'Objektsatz']
objsatz = [i for i in IDS if MERK[i]['merkmale']['objekt_subjekt'] or MERK[i]['merkmale']['objekt_ort']]
klammer = [i for i in IDS if MERK[i]['merkmale']['objekt_klammer_ende']]
befund_ids = [i for i in IDS if K[i][0].startswith('B')]
klammer_befund = [i for i in befund_ids if i in klammer]
PRUEF(erst_k5 == ['Abb. 1', 'Tab. 2', 'Tab. H3', 'Tab. H2', 'Tab. H5', 'Tab. 3', 'Abb. 2'], 'Erstnennungen im Manuskript in Kapitel 5')
PRUEF(wieder_k4 == ['Tab. 1', 'Tab. H1', 'Tab. H4'], 'Wiederaufrufe aus Kapitel 4')
PRUEF(len(erst_k5_objsatz) == 5 and klammer_befund == [], 'fünf Objektsätze, keine Klammer im Befundsatz')
PRUEF(all('Präsens' in MERK[i]['verb'] for i in objsatz), 'Objektsätze im Präsens')
aus('3 Objekte (K3)')
for o in k5_obj:
    aus('  ' + o.ljust(7), 'in Kapitel 5:', ', '.join(k5_obj[o]).ljust(22), '· vor Kapitel 5:', ', '.join(vor_k5.get(o, [])) or '—', '· Erstnennung in Kapitel 5:', ' · '.join(erst[o]))
aus('  zuerst in Kapitel 5 genannt:', len(erst_k5), '(' + ', '.join(erst_k5) + '), davon per Objektsatz', len(erst_k5_objsatz), '· per Klammer', len(erst_k5_klammer), '(' + ', '.join(erst_k5_klammer) + ')')
aus('  Wiederaufrufe aus Kapitel 4:', ', '.join(wieder_k4), '· Wiederaufrufe im Kapitel:', ' · '.join(' '.join(x) for x in A2['objekte']['wiederaufruf']))
aus('  Objektsätze:', ', '.join(objsatz), '(Ort-Form', sum(MERK[i]['merkmale']['objekt_ort'] for i in IDS), ') · Klammer am Satzende:', ', '.join(klammer), '· in Befundsätzen:', len(klammer_befund))
aus('  Folge der Textobjekte, die Kapitel 5 zuerst nennt:', ', '.join(o for o in erst_k5 if not o.split()[1].startswith('H')))
aus('')

# ---------------------------------------------------------------- § 4 Zielgrößenfolge (K5, Prüfkatalog Nr. 3)
KAT = OrderedDict([('S', r'Sprint|\b\d+-m-Zeit'), ('C', r'Richtungswechsel|505'), ('J', r'Sprung|Standweitsprung|\bWeiten?\b')])


def folge(text):
    pos = []
    for k, rx in KAT.items():
        m = re.search(rx, text)
        if m:
            pos.append((m.start(), k))
    return ''.join(k for _, k in sorted(pos))


aus('4 Zielgrößenfolge (K5, Prüfkatalog Nr. 3, F17 § 5.1)')
mehr = OrderedDict((i, folge(T(i))) for i in IDS if len(folge(T(i))) >= 2)
for i, f in mehr.items():
    aus('  ' + i.ljust(7), K[i][0], f)
PRUEF(mehr.get('A4 S2') == 'SJC' and mehr.get('A5 S5') == 'CJ' and mehr.get('A5 S11') == 'SC', 'Folgen in A4 S2, A5 S5, A5 S11')
PRUEF(A2['bloecke']['Codebuch']['zfolge'] == 'S C J', 'Blockfolge S C J')
anker = {}
for s in MS:
    if s['id'] in ('B5 S1', 'B5 S3', 'B5 S4', '4.1 A4 S2', '4.7 A3 S1'):
        anker[s['id']] = folge(s['text'])
titel = re.search(r'\*\*Thema:\*\* (.*)', TXT['f17']).group(1)
anker['Titel (F17 § 2)'] = folge(titel)
for nr in ('3', '4', '5'):
    s1 = next(s for s in MS if s['id'] == '6.1 A' + nr + ' S1')
    anker['6.1 A' + nr + ' S1'] = folge(s1['text'])
aus('  Bezüge:', ' · '.join(k + ' ' + (v or '—') for k, v in anker.items()))
PRUEF(anker['B5 S1'] == 'SCJ' and anker['B5 S3'] == 'SCJ' and anker['B5 S4'] == '' and anker['4.1 A4 S2'] == 'SCJ', 'Hypothesen und 4.1')
PRUEF(anker['4.7 A3 S1'] == 'SCJ' and anker['Titel (F17 § 2)'] == 'SCJ', '4.7 und Titel')
PRUEF([anker['6.1 A3 S1'], anker['6.1 A4 S1'], anker['6.1 A5 S1']] == ['S', 'C', 'J'], '6.1 A3 bis A5')
abschn44 = [s['abschnitt'] for s in MS if s['abschnitt'] in ('4.4.1', '4.4.2', '4.4.3') and s['satz'] == 1 and s['absatz'].endswith('A1')]
aus('  Methodik 4.4.1 bis 4.4.3 erste Sätze:', ' · '.join(a + ' ' + folge(next(s['text'] for s in MS if s['abschnitt'] == a and s['satz'] == 1)) for a in abschn44))
aus('  Blockfolge der Befundsätze:', A2['bloecke']['Codebuch']['zfolge'], '· erste Nennung im Befundtext (B-Sätze):', ' '.join(folge(T(i)) for i in befund_ids if folge(T(i))))
aus('')

# ---------------------------------------------------------------- § 5 Befundordnung und Blockbeginn (K4, K6)
aus('5 Befundordnung und Blockbeginn (K4, K6)')
for i in befund_ids + ['A5 S11']:
    aus('  ' + i.ljust(7), K[i][0].ljust(3), (MERK[i]['satzanfang'] or '').ljust(52), '|', T(i)[:70])
b2_saetze = [i for i in IDS if K[i][0] == 'B2' or 'B2' in K[i][1]]
PRUEF(b2_saetze == [], 'keine Veränderung je Gruppe')
aus('  Sätze mit B2 (Veränderung je Gruppe):', len(b2_saetze), '· Blöcke nach abgleich_2a:', ' · '.join(b[0] + ':' + '–'.join(b[1]) for b in A2['bloecke']['Codebuch']['bloecke']))
aus('')

# ---------------------------------------------------------------- § 6 Null-, Sammel-, Gegenbefunde (K7 bis K9)
QU = re.compile(r'\b(Alle|alle|allen|keiner|Keine|keine|Jedes|jedes)\b')
aus('6 Nullbefunde, Sammelbefunde, Kontraste (K7 bis K9)')
for i, art in A2['null']:
    aus('  Nullbefund', i, '·', art)
qsaetze = [i for i in IDS if QU.search(T(i))]
for i in qsaetze:
    aus('  Quantor', i.ljust(7), 'K', K[i][0], '+'.join(K[i][1]) or '', '· KH', KH[i][0], '+'.join(KH[i][1]) or '', '|', ', '.join(QU.findall(T(i))))
b4_k = [i for i in IDS if K[i][0] == 'B4' or 'B4' in K[i][1]]
b4_kh = [i for i in IDS if KH[i][0] == 'B4' or 'B4' in KH[i][1]]
PRUEF(b4_k == ['A5 S10'], 'B4 nach Codebuch nur A5 S10')
memo = TXT['memo_b']
PRUEF('Nach Wortlaut erfasst „bei keiner Zielgröße“ alle Zielgrößen der Studie.' in memo, 'Memo B zu A5 S6')
kontrast = [i for i in IDS if re.search(r'\b(jedoch|aber|während|dagegen|hingegen)\b', T(i))]
PRUEF(kontrast == [], 'keine Kontrastkonnektoren')
aus('  Quantor in A5 S2 über Spieler (Objektsatz), in A6 S4 über Analysen (memo_B), A1 S4 und A4 S1 über alle sieben Zielgrößen, A5 S3, S6, S7, S9 über die drei konfirmatorischen')
aus('  B4 nach Codebuch:', ', '.join(b4_k), '· nach den Hinweisen:', ', '.join(b4_kh), '· Kontrastkonnektoren: keine')
aus('  Memo B zu A5 S6: „Nach Wortlaut erfasst „bei keiner Zielgröße“ alle Zielgrößen der Studie.“')
aus('')

# ---------------------------------------------------------------- § 7 Schluss (K10)
letzter = IDS[-1]
letzter_b = befund_ids[-1]
KL_END = re.compile(r'\([^()]*\b(Table|Tab\.|Figure|Fig)\b[^()]*\)\s*\.?\s*$')
schluss = OrderedDict()
for s in STUD:
    r = STUD[s][-1]
    schluss[s] = (r['gruppe'], r['primaer'], '+'.join(sek(r)), bool(KL_END.search(r['text'])))
kern_letzt = Counter(schluss[s][1][0] for s in KERN)
kern_klammer = [s for s in KERN if schluss[s][3]]
erw_letzt = Counter(schluss[s][1][0] for s in ERW)
PRUEF(K[letzter][0] == 'Z1' and K[letzter][1] == ['B1', 'V2'] and KH[letzter][1] == ['B4', 'V2'], 'Code A6 S4')
PRUEF(MERK[letzter]['merkmale']['objekt_klammer_ende'] == 1 and letzter_b == 'A5 S10' and letzter_b not in klammer, 'Klammer A6 S4, A5 S10 ohne')
PRUEF(kern_letzt == Counter({'B': 8, 'X': 2}) and len(kern_klammer) == 5, 'Kern Schluss 8 B, 2 X, Klammer 5')
PRUEF(erw_letzt == Counter({'O': 4, 'X': 1, 'B': 1}), 'erweitert Schluss 4 O, 1 X, 1 B')
aus('7 Schluss (K10, Prüfkatalog Nr. 6)')
aus('  Kapitel 5: letzter Satz', letzter, 'K', K[letzter][0], '+'.join(K[letzter][1]), '· KH', KH[letzter][0], '+'.join(KH[letzter][1]), '· Klammer am Satzende ja · letzter Befundsatz', letzter_b, 'ohne Klammer, danach', ', '.join(IDS[IDS.index(letzter_b) + 1:]))
for s, v in schluss.items():
    aus('  ' + s.ljust(15), v[0].ljust(16), 'letzter Satz', (v[1] + (' (' + v[2] + ')' if v[2] else '')).ljust(12), 'Klammer am Satzende' if v[3] else '')
aus('  Kern: letzter Satz nach Gruppe', dict(kern_letzt), '· mit Klammer am Satzende', len(kern_klammer), '(' + ', '.join(kern_klammer) + ') · erweitert', dict(erw_letzt))
aus('')

# ---------------------------------------------------------------- § 8 Tempus
praes = [i for i in IDS if 'Präsens' in MERK[i]['verb']]
praet = [i for i in IDS if 'Präteritum' in MERK[i]['verb']]
PRUEF(praes == objsatz and len(praet) == 25, 'Präsens nur in Objektsätzen')
aus('8 Tempus (Prüfkatalog Nr. 6)')
aus('  Präsens:', ', '.join(praes), '· Präteritum:', len(praet), 'Sätze')
aus('')

# ---------------------------------------------------------------- § 9 Projektregeln P1 bis P12
ALLE = ' '.join(T(i) for i in IDS)
p = OrderedDict()
p['P1'] = ('standardisierter Differenz d' in T('A1 S3') and 'Überlappung' in T('A1 S3') and not re.search(r'\d', T('A1 S4'))
           and not re.search(r'signifik|Test\b|p =', T('A1 S3') + T('A1 S4')))
proz = [i for i in IDS if '%' in T(i)]
p['P2'] = (b2_saetze == [] and proz == ['A2 S2', 'A5 S4'] and not re.search(r'\b(verbesser\w*|Erhalt\w*|Effekt\w*|Verschlechter\w*|stieg|sank|Rückgang)\b', ALLE))
DIFF = re.compile(r'([−+]\d+,(\d+)) (s|cm) \((?:95-%-Konfidenzintervall )?([−+]\d+,\d+) bis ([−+]\d+,\d+) (?:s|cm), p = (\d,\d{3})\)')
treffer = DIFF.findall(T('A5 S4')) + DIFF.findall(T('A5 S5'))
stellen = [(t[2], len(t[1]), len(t[3].split(',')[1]), len(t[4].split(',')[1])) for t in treffer]
p['P3'] = (len(treffer) == 3 and stellen == [('s', 3, 3, 3), ('s', 3, 3, 3), ('cm', 1, 1, 1)]
           and 'Interventions- minus Kontrollgruppe' in T('A5 S4') and "Hedges' g" in T('A5 S1') and MERK['A5 S4']['merkmale']['stat'] == 0)
p['P4'] = ('unadjustierten und adjustierten Gruppendifferenzen' in T('A5 S1') and 'Alle unadjustierten Differenzen' in T('A5 S3')
           and 'als die adjustierten' in T('A5 S3') and not re.search(r'\d', T('A5 S3')))
p['P5'] = (all(MERK[i]['merkmale']['klasse'] == 0 for i in IDS) and 'relevanten Unterschieden in beide Richtungen vereinbar' in T('A5 S7')
           and T('A5 S8') == 'Die Befunde waren unschlüssig.' and not re.search(r'\b(klein|moderat|groß|trivial|stark)\w*', ALLE))
p['P6'] = ('Bei keiner Zielgröße war damit ein Gruppenunterschied nachweisbar.' == T('A5 S6') and not re.search(r'kein Effekt|no significant|Erhalt', ALLE))
p['P7'] = (T('A5 S9') == 'Keine adjustierte Differenz zeigte mit p < 0,05 einen Vorteil der Interventionsgruppe.'
           and T('A5 S10') == 'Die Nullhypothese wurde nicht verworfen.' and not re.search(r'Studienprotokoll|Ethikantrag', ALLE))
p8_wortlaut = 'geprüft und nicht verworfen' in T('A6 S3')
p['P8'] = (re.search(r'W = 0,\d{3}, p = 0,\d{3}', T('A6 S1')) is not None and 'nachträglich festgelegte Bootstrap-Konfidenzintervall' in T('A6 S2')
           and 'von −0,177 bis +0,107 s' in T('A6 S2') and 'geprüften' in T('A6 S3') and 'nicht verworfen' in T('A6 S3') and 'erfüllt' not in ALLE)
m47 = next(s['text'] for s in MS if s['id'] == '4.7 A5 S1')
p['P9'] = ('beobachtende Per-Protokoll-Vergleich' in T('A6 S4') and 'sechs Sensitivitätsanalysen' in T('A6 S4') and T('A6 S4').endswith('(Tab. H4).')
           and m47.startswith('Sechs vorab festgelegte Sensitivitätsanalysen') and T('A6 S4').startswith('Soweit die Fallzahl eine Inferenz zuließ'))
ue = WERTE['K-10.12']['darstellung']
p['P10'] = (ue == '12 · 8 · 2 · 2 · 9 Spieler' and T('A3 S3').startswith('Zwölf Meldungen von neun Spielern') and 'je zwei zu nicht und zu teilweise' in T('A3 S3')
            and T('A3 S4') == 'Für die Kontrollgruppe wurden solche Angaben nicht erhoben.' and not re.search(r'Knie|Sprunggelenk|Lokalisation|schmerzbedingt', ALLE))
p['P11'] = (not re.search(r'\b16\b', ALLE) and 'gingen 26 in die Analyse ein' in T('A1 S2'))
kon = [i for i in IDS if MERK[i]['merkmale']['konnektor']]
p['P12'] = (U['med'] == 15 and U['maxsatz'] == 28 and SK not in ALLE and kon == [])
aus('9 Projektregeln am Satz (P1 bis P12)')
for k2, v in p.items():
    aus('  ' + k2.ljust(4), 'Satzprüfung bestanden' if v else 'Satzprüfung NICHT bestanden', '(P8: Inhalt, Wortlaut der Formel gesondert)' if k2 == 'P8' else '')
aus('  P2 Prozentzeichen in:', ', '.join(proz), '(Umsetzungsrate, 95-%-Konfidenzintervall)')
aus('  P3 Treffer (Wert, Stellen Wert/untere/obere Grenze):', ' · '.join(t[0] + ' ' + t[2] + ' ' + str(st[1:]) for t, st in zip(treffer, stellen)))
aus('  P8 Formel „geprüft und nicht verworfen“ wörtlich in A6 S3:', 'ja' if p8_wortlaut else 'nein', '· Wortlaut:', T('A6 S3'))
aus('  P10 K-10.12:', ue, '· K-10.4:', WERTE['K-10.4']['darstellung'], '· K-10.9:', WERTE['K-10.9']['darstellung'], '(Berichtsort', WERTE['K-10.9']['berichtsort'] + ')')
aus('  P11 „Zehn Spieler“ in A2 S3 ist K-10.10 (Schwelle sechs), keine Gruppengröße (TV5 § 5)')
aus('  P12 Median', U['med'], '· längster', U['maxsatz'], '· Semikola', ALLE.count(SK), '· adverbiale Konnektoren', len(kon))
PRUEF(all(v for v in p.values()), 'P1 bis P12 am Satz')
PRUEF(not p8_wortlaut, 'P8 Wortlaut nicht wörtlich (Befund 6g)')
aus('')

# ---------------------------------------------------------------- § 10 Umsetzung (Prüfkatalog Nr. 8)
o2 = [i for i in IDS if K[i][0] == 'O2']
o2w = sum(W(i) for i in o2)
aus('10 Umsetzung (Prüfkatalog Nr. 8)')
aus('  Kapitel 5:', ', '.join(o2), '·', o2w, 'Wörter =', pz(100 * o2w / U['W']), '% · vor dem ersten Befund:', all(IDS.index(i) < IDS.index(rahmen['erster_befund']) for i in o2))
o2_studie = OrderedDict()
for s in STUD:
    rs = STUD[s]
    w = sum(int(r['woerter']) for r in rs)
    idx = [n for n, r in enumerate(rs) if r['primaer'].startswith('B')]
    fb, lb = (idx[0], idx[-1]) if idx else (None, None)
    w2 = sum(int(r['woerter']) for r in rs if r['primaer'] == 'O2')
    lage = sorted(set(('vor' if n < fb else ('nach' if n > lb else 'im Befundteil')) for n, r in enumerate(rs) if r['primaer'] == 'O2'))
    o2_studie[s] = (rs[0]['gruppe'], 100 * w2 / w, lage)
    if w2:
        aus('  ' + s.ljust(15), rs[0]['gruppe'].ljust(16), 'O2', pz(100 * w2 / w).rjust(5), '% ·', ', '.join(lage))
setting = [o2_studie[s][1] for s in ('Klusemann2012', 'Veith2021', 'Rogers2020', 'Hilska2021')]
PRUEF(min(setting) <= 100 * o2w / U['W'] <= max(setting), 'Umsetzung im Bereich der Settingstudien')
tv61 = TXT['tv61']
PRUEF('6.3 G6: Gründe nicht durchgeführter Einheiten wurden nicht erfasst' in tv61, 'Gründe nicht erfasst (TV 6.1 § 9)')
aus('  Gründe nicht durchgeführter Einheiten: nicht erfasst (Textvorschlag 6.1 § 9, Vormerkung 6.3 G6)')
aus('')

# ---------------------------------------------------------------- § 11 Absicherung (Prüfkatalog Nr. 9)
aus('11 Absicherung (Prüfkatalog Nr. 9)')
nach_b = IDS[IDS.index(letzter_b) + 1:]
aus('  Kapitel 5 nach dem letzten Befundsatz:', ' · '.join(i + ' ' + K[i][0] for i in nach_b))
for s in STUD:
    rs = STUD[s]
    idx = [n for n, r in enumerate(rs) if r['primaer'].startswith('B')]
    fb, lb = (idx[0], idx[-1]) if idx else (None, None)
    v = []
    for n, r in enumerate(rs):
        codes = [r['primaer']] + sek(r)
        if any(c in ('V1', 'V2', 'Z1') for c in codes):
            lage = 'vor' if fb is not None and n < fb else ('nach' if lb is not None and n > lb else 'im Befundteil')
            v.append(r['satz'] + ' ' + r['primaer'] + ('(' + '+'.join(sek(r)) + ')' if sek(r) else '') + ' ' + lage)
    if v:
        aus('  ' + s.ljust(15), STUD[s][0]['gruppe'].ljust(16), ' · '.join(v))
v2_lage = []
for s in STUD:
    rs = STUD[s]
    idx = [n for n, r in enumerate(rs) if r['primaer'].startswith('B')]
    for n, r in enumerate(rs):
        if 'V2' in [r['primaer']] + sek(r):
            v2_lage.append('nach' if idx and n > idx[-1] else ('vor' if idx and n < idx[0] else 'im Befundteil'))
PRUEF('nach' not in v2_lage and len(v2_lage) == 7, 'V2 im Korpus siebenmal, nie nach dem letzten Befund')
abstand_30m = IDS.index('A6 S1') - IDS.index('A5 S4') - 1
PRUEF(abstand_30m == 7, 'zwischen A5 S4 und A6 S1 stehen sieben Sätze')
aus('  V2 im Korpus (primär oder sekundär):', len(v2_lage), 'Sätze ·', ', '.join(k + ' ' + str(v) for k, v in Counter(v2_lage).items()), '· nach dem letzten Befund keiner · Kapitel 5: A5 S11 (V2) nach A5 S10')
aus('  Zwischen dem 30-m-Befund (A5 S4) und seiner Einschränkung (A6 S1) stehen', abstand_30m, 'Sätze')
plan = TXT['plan']
PRUEF('Voraussetzungen in einem Satz je Zielgröße, verworfene mit Zahl (R2), Sensitivitäten als Sammelsatz (R1 regelt die Ausnahme), deskriptive Zielgrößen in einem Satz (Tab. H3)' in plan, 'Plan-Folge')
aus('  Plan § 3 Task 11: … Abb. 2 mit einem einführenden Satz, Voraussetzungen …, Sensitivitäten als Sammelsatz …, deskriptive Zielgrößen in einem Satz (Tab. H3), Antragskriterium deskriptiv, letzter Satz mit Objektverweis, kein Resümee')
aus('  Kapitel 5: Tab. 3 (A5 S1) → Abb. 2 (A5 S2) → Befunde (A5 S3 bis S10) → deskriptive Zielgrößen (A5 S11) → Voraussetzungen (A6 S1 bis S3) → Sammelsatz (A6 S4) · Antragskriterium in A2 S3 (Register 9c)')
aus('')

# ---------------------------------------------------------------- § 12 Anschluss an 6.1 (Prüfkatalog Nr. 10)
BEZUG = OrderedDict([
    ('6.1 A1 S2', (['A5 S4', 'A5 S6', 'A5 S10'], [])), ('6.1 A1 S3', (['A5 S3'], ['Tab. 3'])),
    ('6.1 A1 S4', (['A5 S3', 'A1 S4'], ['Abb. 2'])), ('6.1 A1 S5', (['A5 S7'], [])), ('6.1 A1 S6', (['A5 S8'], [])),
    ('6.1 A2 S2', (['A2 S1', 'A2 S2'], ['Tab. H2', 'Tab. H5'])), ('6.1 A2 S4', (['A2 S2'], [])),
    ('6.1 A2 S5', (['A6 S4', 'A2 S3'], [])), ('6.1 A2 S6', (['A6 S4'], ['Tab. H4'])),
    ('6.1 A3 S2', ([], ['Tab. 2', 'Tab. 3'])), ('6.1 A3 S3', (['A5 S4', 'A5 S7'], [])), ('6.1 A3 S6', (['A5 S4', 'A5 S7'], [])),
    ('6.1 A4 S2', ([], ['Tab. 2', 'Tab. 3'])), ('6.1 A4 S3', (['A5 S5', 'A5 S7'], [])), ('6.1 A4 S4', (['A5 S5', 'A5 S6'], [])),
    ('6.1 A5 S2', ([], ['Tab. 2', 'Tab. 3'])), ('6.1 A5 S3', (['A5 S5', 'A5 S7'], [])), ('6.1 A5 S4', (['A5 S5', 'A5 S6'], [])),
    ('6.1 A5 S8', ([], ['Tab. 2'])), ('6.1 A6 S1', (['A3 S1'], [])), ('6.1 A6 S2', (['A3 S3'], ['Tab. H2'])),
    ('6.1 A6 S3', (['A3 S3'], [])), ('6.1 A6 S4', (['A3 S4'], [])), ('6.1 A6 S5', (['A3 S3', 'A3 S4'], [])),
])
ms_ids = {s['id'] for s in MS}
PRUEF(all(k in ms_ids for k in BEZUG), 'Sätze von 6.1 im Master')
PRUEF(all(o in k5_obj for v in BEZUG.values() for o in v[1]), 'Objekte, auf die 6.1 baut, sind in Kapitel 5 verwiesen')
je_absatz = OrderedDict((a, sorted({k for k, v in BEZUG.items() if any(x.startswith(a + ' ') for x in v[0])})) for a in ('A1', 'A2', 'A3', 'A4', 'A5', 'A6'))
aus('12 Anschluss an 6.1 (Prüfkatalog Nr. 10, Zuordnung nach Abgleichbefund § 1.4)')
aus('  ', len(BEZUG), 'Sätze von 6.1, alle im Master, jedes Objekt, auf das sie bauen, wird in Kapitel 5 verwiesen:', ', '.join(sorted({o for v in BEZUG.values() for o in v[1]})))
for a, ss in je_absatz.items():
    aus('  ' + a, 'berührt', len(ss), 'Satz:' if len(ss) == 1 else 'Sätze:', ', '.join(ss) or '— (6.1 nimmt den Absatz nicht auf)')
nur_obj = [k for k, v in BEZUG.items() if not v[0]]
aus('  nur über Objekte:', ', '.join(nur_obj), '· dazu Teile von 6.1 A2 S2 (K-10.15), A2 S6 (K-08.1), A6 S2 (K-10.9, Bezugsmenge 15)')
PRUEF(je_absatz['A4'] == [], 'A4 ohne Bezug in 6.1')
aus('')

# ---------------------------------------------------------------- § 13 weitere Aussagen des Befunds
befund = TXT['befund']
anteil_budget = 100 * 450 / 6350
PRUEF(pz(anteil_budget) == '7,1' and 'Kapitel 5 hat 450 Wörter Budget (Gliederung v6), 7,1 % von 6.350.' in befund, 'Budgetanteil')
glied = TXT['gliederung']
PRUEF('| 5 | 3 | Ergebnisse (ohne Unterabschnitte, Ä16) | 450 | 0 | Abb. 1, Tab. 2, Abb. 2, Tab. 3 |' in glied, 'Gliederung v6 Zeile Ergebnisse')
textobjekte = [o for o in erst_k5 if not o.split()[1].startswith('H')]
PRUEF(textobjekte == ['Abb. 1', 'Tab. 2', 'Tab. 3', 'Abb. 2'], 'Folge der Textobjekte')
aus('13 Weitere Aussagen des Befunds')
aus('  § 4 Budget: 450 von 6.350 =', pz(anteil_budget, 2), '% · Gliederung v6: Ergebnisse 450, Objekte „Abb. 1, Tab. 2, Abb. 2, Tab. 3“ · Kapitel 5 im Master 450')
aus('  Folge der Textobjekte, die Kapitel 5 zuerst nennt:', ', '.join(textobjekte), '· Tab. 1 seit 4.4 eingeführt')
aus('  § 1.1 vier Fragen: Umsetzung ohne Aufsicht', ', '.join(o2), '· unerwünschte Ereignisse', ', '.join(i for i in IDS if K[i][0] == 'Z2'), '· Intervalle', ', '.join(A2['statistik']['alle']['ki']), '· Messgüte gegen den SESOI A4 S1')
aus('')

# ---------------------------------------------------------------- § 14 Stil: Stilprofil Teil 2, 3, 5 und 7 (r1)
AUSSAGE = OrderedDict([
    ('A1 S1', 'eine'), ('A1 S2', 'eine'), ('A1 S3', 'komma: Tab. 2 …, Tab. H3 … (zweiter Hauptsatz elliptisch)'), ('A1 S4', 'eine'),
    ('A2 S1', 'angehängt: Status der Meldungen, nach dem Komma der Median je Spieler (andere Größe)'),
    ('A2 S2', 'eine (Variante derselben Größe in der Klammer)'),
    ('A2 S3', 'komma: zehn …, drei … (zweiter Hauptsatz elliptisch)'), ('A2 S4', 'komma: zwei Zählregeln (zweiter Hauptsatz elliptisch)'),
    ('A3 S1', 'eine (Kennwerte derselben Größe in der Klammer)'), ('A3 S2', 'eine (Kennwerte derselben Größe in der Klammer)'),
    ('A3 S3', 'angehängt: „davon je zwei …“ (Status der Meldungen)'), ('A3 S4', 'eine'),
    ('A4 S1', 'eine'), ('A4 S2', 'komma: Interventionsgruppe …, Kontrollgruppe … (zweiter Hauptsatz elliptisch)'),
    ('A5 S1', 'eine'), ('A5 S2', 'eine'), ('A5 S3', 'angehängt: zweite Angabe mit „und“ an dasselbe Verb (Richtung, Abstand zur adjustierten)'),
    ('A5 S4', 'eine'), ('A5 S5', 'komma: zwei Zielgrößen (zweiter Hauptsatz elliptisch)'), ('A5 S6', 'eine'), ('A5 S7', 'eine'),
    ('A5 S8', 'eine'), ('A5 S9', 'eine'), ('A5 S10', 'eine'), ('A5 S11', 'eine'), ('A6 S1', 'eine'), ('A6 S2', 'eine'), ('A6 S3', 'eine'),
    ('A6 S4', 'Bedingung im vorangestellten Nebensatz und zwei Hauptsätze mit „und“ („Soweit …, änderten …, und keine davon …“)'),
])
PRUEF(list(AUSSAGE.keys()) == IDS, 'Handurteil je Satz vollständig')
eine = [i for i, v in AUSSAGE.items() if v.startswith('eine')]
eine_klammer = [i for i, v in AUSSAGE.items() if v.startswith('eine (')]
komma = [i for i, v in AUSSAGE.items() if v.startswith('komma')]
angeh = [i for i, v in AUSSAGE.items() if v.startswith('angehängt')]
bedingung = [i for i, v in AUSSAGE.items() if v.startswith('Bedingung')]
PRUEF((len(eine), len(komma), len(angeh), len(bedingung)) == (20, 5, 3, 1), 'Handurteil 20, 5, 3, 1')
PRUEF(eine_klammer == ['A2 S2', 'A3 S1', 'A3 S2'], 'eine Aussage mit Werten derselben Größe in der Klammer')


def kommas(i):
    return len(re.findall(r', ', re.sub(r'\([^()]*\)', '', T(i))))


KOMMA = OrderedDict((i, kommas(i)) for i in IDS)
PRUEF(all(KOMMA[i] == 0 for i in eine) and all(KOMMA[i] == 1 for i in komma), 'Kommas außerhalb der Klammern: eine Aussage 0, Komma-Ausnahme 1')
PRUEF([KOMMA[i] for i in angeh] == [2, 1, 0] and KOMMA['A6 S4'] == 2, 'Kommas in A2 S1, A3 S3, A5 S3 und A6 S4')
nebensatz_vorn = [i for i in IDS if re.match(r'^(Soweit|Wenn|Falls|Sofern|Da|Weil|Obwohl|Nachdem)\b', T(i))]
PRUEF(nebensatz_vorn == bedingung == ['A6 S4'], 'einziger vorangestellter Nebensatz in A6 S4')
VERBOT = [r'\bim Rahmen von\b', r'\bGegenstand der Untersuchung', r'\bes ist festzuhalten', r'\bdarüber hinaus\b', r'\bdes Weiteren\b',
          r'\bhierbei gilt es', r'\bzunächst\b', r'\banschließend\b', r'\babschließend\b', r'\bsodass\b', r'\bweshalb\b', r'\bweil\b',
          r'\bda\b', r'\bbestätig', r'\bEffekt', r'\bsignifikant', r'\brandomisiert', r'\bITT\b', r'\bWirkung', r'\bTraining',
          r'\bverbesser', r'\bErhalt']
treffer_verbot = [w for w in VERBOT if re.search(w, ALLE, re.IGNORECASE)]
PRUEF(treffer_verbot == [], 'keine Verbots- und Deutungswörter')
thema = [i for i in IDS if MERK[i]['satzanfang'].startswith('Themenanker')]
aus('14 Stil (Stilprofil Teil 2, 3, 5 und 7, Registerergänzung r1)')
aus('  eine Aussage je Satz (Handurteil, Regel: Werte derselben Größe in der Klammer zählen nicht als weitere Aussage · zwei gleichrangige Hauptsätze mit Komma ohne Konjunktion, der zweite elliptisch, fallen unter die Komma-Ausnahme von Teil 3 · eine zweite Aussage, die anders angehängt ist, und eine vorangestellte Bedingung zählen gesondert):')
for i, v in AUSSAGE.items():
    if not v.startswith('eine'):
        aus('    ' + i.ljust(7), v)
aus('  eine Aussage:', len(eine), '(davon mit Werten derselben Größe in der Klammer:', ', '.join(eine_klammer) + ') · Komma-Ausnahme:', len(komma), '(' + ', '.join(komma) + ') · zweite Aussage angehängt:', len(angeh), '(' + ', '.join(angeh) + ') · Bedingung im Nebensatz:', ', '.join(bedingung))
aus('  Kommas außerhalb der Klammern (Komma mit Leerzeichen, Dezimalkommas zählen nicht):', ' · '.join(i + ' ' + str(v) for i, v in KOMMA.items() if v))
aus('  Registerprüfung r1 nannte: A2 S1, A2 S4, A5 S5, A6 S4')
aus('  Verbots- und Deutungswörter (Stilprofil Teil 3 und 5, Plan § 3 Task 11, TV5 § 0):', 'keine' if not treffer_verbot else treffer_verbot)
aus('  Themenanker am Satzanfang:', ', '.join(thema), '· Klammerverweise am Satzende:', len(klammer), 'von', len(IDS), 'Sätzen, alle Objektverweise (Zielwert Teil 2 etwa jeder sechste, bei 29 Sätzen etwa fünf)')
aus('  je Zielgröße derselbe Satzbau: A5 S4 „betrug die Differenz … beim 30-m-Sprint … (95-%-KI …, p = …)“, A5 S5 „betrug sie … (…, p = …), beim Standweitsprung … (…, p = …)“')
aus('')

# ---------------------------------------------------------------- § 15 Prüfpunkte Bezugsmenge und Satzenden
ende_buchst = [i for i in IDS if re.search(r"(^|[\s'’])[a-zäöüß]\.$", T(i))]
ende_ziffer = [i for i in IDS if re.search(r'\d\.$', T(i))]
PRUEF(ende_buchst == ['A5 S1', 'A6 S2'] and ende_ziffer == [], 'Satzenden')
PRUEF(WERTE['K-10.4']['darstellung'] == '18' and WERTE['K-10.9']['darstellung'] == '15', 'K-10.4 und K-10.9')
s62 = next(s['text'] for s in MS if s['id'] == '6.1 A6 S2')
aus('15 Prüfpunkte aus Schritt 1 (Bezugsmenge, Satzenden)')
aus('  A3 S3:', T('A3 S3'))
aus('  Mengen: zugeteilte IG-Spieler K-10.4 =', WERTE['K-10.4']['darstellung'], '· Spieler mit mindestens einer Meldung K-10.9 =', WERTE['K-10.9']['darstellung'], '· neun von 18 = 50,0 % · neun von 15 = 60,0 %')
aus('  6.1 A6 S2:', s62)
aus('  Satzende auf einen einzelnen Kleinbuchstaben:', ', '.join(ende_buchst), '· auf eine Ziffer:', ', '.join(ende_ziffer) or 'keiner')
aus('')

# ---------------------------------------------------------------- § 16 Zitatprüfung
ZITATE = [
    ('befund', 'Rahmen vor dem ersten Befund: Orientierung oder Objektsätze'),
    ('befund', 'Den Ausgangsvergleich der Gruppen vor die Befunde stellen'),
    ('befund', 'Die Objekte des Rahmens vor dem ersten Befund mit einem Objektsatz einführen, als Subjekt oder Ort im Präsens, Wiederaufruf als Klammer am Satzende'),
    ('befund', 'Das Modellergebnis vor Vergleiche einzelner Gruppen stellen'),
    ('befund', 'Eine Reihenfolge der Zielgrößen mit einem Bezug im Text (Methodik oder Titel), bei Wiederkehr dieselbe'),
    ('befund', 'Für Kapitel 5 zählt die Blockfolge, weil K5 die Blöcke ordnet.'),
    ('befund', 'Befunde nach Zielgröße ordnen, den Block mit Zielgröße, Befund, Modellterm oder der Analyse beginnen'),
    ('befund', 'Nullbefunde ausdrücklich berichten'),
    ('befund', 'Sammelbefund mit Quantor, wo er über alle Zielgrößen gilt, Ausnahmen benennen'),
    ('befund', 'Gegenbefunde und Kontraste am Ort des Befunds, den sie einschränken'),
    ('befund', 'Schluss mit einem Befund- oder Objektsatz, kein Resümee, kein Beleg, Befunde im Präteritum'),
    ('befund', '→ Absicherung (Voraussetzungen, Sensitivität) → letzter Befundsatz mit Objektklammer.'),
    ('befund', 'Steht je Zielgröße das Modellergebnis vor allem anderen?'),
    ('befund', 'Gilt die Reihenfolge Sprint → Richtungswechsel → Sprung durchgehend, und deckt sie sich mit Titel, Hypothesen, Methodik (4.4) und 6.1?'),
    ('befund', 'Endet das Kapitel mit einem Befundsatz und Objektklammer? Steht ein Satz im Präsens außerhalb der Objektsätze?'),
    ('befund', 'Ausgangslage ohne Signifikanztest, Größe und Überlappung im Objekt'),
    ('befund', 'Keine Veränderung innerhalb der Gruppen mit Test, keine Prozentveränderung'),
    ('befund', 'Adjustierte Differenz mit 95-%-KI und p im Satz, g im Objekt'),
    ('befund', 'Unadjustiert neben adjustiert (CONSORT 18)'),
    ('befund', 'Keine Größenklasse, Einordnung über die Schlusslogik'),
    ('befund', 'Nullbefund als „kein Gruppenunterschied nachweisbar“ mit Schätzer, Intervall und Fall'),
    ('befund', 'Entscheidung über H0 im Ergebnisteil'),
    ('befund', 'Verworfene Voraussetzung mit Prüfgröße, p und Bootstrap-KI, übrige „geprüft und nicht verworfen“'),
    ('befund', 'Sensitivität und Per-Protokoll in einem Sammelsatz (R1)'),
    ('befund', 'Ereignisse und Schmerzmeldungen je Status, Kontrollgruppe ohne Instrument (CONSORT 19)'),
    ('befund', 'Analysezahl je Gruppe und Zielgröße im Objekt (CONSORT 16, Abb. 1, Tab. 3)'),
    ('befund', 'Satzlänge im Median 14 bis 18, höchstens 32 Wörter, kein Semikolon'),
    ('befund', 'Kapitel 5 hat 450 Wörter Budget (Gliederung v6), 7,1 % von 6.350.'),
    ('befund', 'Umsetzung ohne Aufsicht, unerwünschte Ereignisse, Intervalle, Messgüte gegen eine kleinste bedeutsame Veränderung'),
    ('befund', 'Interviewbefunde sind eine eigene Textsorte, Kapitel 5 hat keine'),
    ('befund', 'Kein Ergebnisteil endet mit einem Resümee, keiner entscheidet über eine Hypothese.'),
    ('befund', 'Für die adjustierte Differenz mit Intervall im Satz ist Veith et al. (2021, 2.5) das nächste Vorbild'),
    ('f17', 'keine Signifikanztests auf Baseline-Unterschiede (15)'),
    ('f17', 'adjustierte und unadjustierte Differenz nebeneinander (18)'),
    ('f17', '**Reihenfolgetreue:** Sprint → Richtungswechsel → Sprung in den Hypothesen, den Ergebnissen und der Diskussion identisch.'),
    ('f17', 'Verbindliche Formulierung in 5.2: „geprüft und nicht verworfen“, 4.7 kündigt sie nicht an.'),
    ('f17', 'Der Fließtext nennt Teststatistik, Richtung und den Fall der Schlusslogik'),
    ('f17', 'Flussdiagramm im Methodikteil – es gehört nach 5.1 (CONSORT 13a).'),
    ('f17', 'Ordnung: Orientierungszug (Teilnehmerfluss, Adhärenz, Ausgangswerte, Messgüte – zugleich Einführung der Objekte), dann je Zielgröße in fester Reihenfolge.'),
    ('f17', 'Korrekt: „kein Gruppenunterschied nachweisbar“, mit Punktschätzer, Konfidenzintervall und der Einordnung nach der Schlusslogik (§ 11.2b).'),
    ('f17', 'wie bisher: drei konfirmatorische Zielgrößen plus Fluss, Adhärenz, Ausgangswerte'),
    ('f17', '**Thema:** Effekte eines sechswöchigen videobasierten, gerätefreien plyometrischen Heimtrainings während der Sommerpause auf Sprint-, Richtungswechsel- und Sprungleistung'),
    ('plan', 'je Zielgröße in fester Reihenfolge ein Block (adjustierte Differenz, KI, p, g als Verweis auf Tab. 3, Fall nach der Schlusslogik'),
    ('plan', 'Antragskriterium deskriptiv, letzter Satz mit Objektverweis, kein Resümee'),
    ('plan', 'unerwünschte Ereignisse, gültige Versuche und TE post'),
    ('plan', 'Der Text führt Abb. 1, Tab. 2, Abb. 2 und Tab. 3 per Verweis ein'),
    ('raster', 'Schluss = letzter Befundsatz mit Objektverweis'),
    ('raster', 'hier: adjustierte Differenz → KI → p → g'),
    ('stil', 'Eine Aussage je Satz, Ausnahmen in einen eigenen Satz.'),
    ('stil', 'Bedingungen hängen nicht als Nebensatz an, sie stehen separat'),
    ('stil', 'ist zulässig, aber die Teilung in zwei Sätze ist die Regel'),
    ('stil', 'Konnektoren maximal einer pro drei Sätze'),
    ('stil', 'Etwa jeder sechste Satz trägt einen Klammerverweis'),
    ('stil', 'Kap. 5: je Zielgröße derselbe Satzbau'),
    ('stil', '**Kapitel 5** verbietet jede Bewertung.'),
    ('stil', 'danach höchstens die Klammer am Satzende, wo die Daten besprochen werden'),
    ('gliederung', '450 Wörter mit vier Objekten in fester Reihenfolge'),
    ('tv5', 'Schluss: letzter Befundsatz mit Objektverweis, kein Resümee'),
    ('tv5', 'der Gruppenvergleich mit „Tab. 3 enthält …“ deutlich einsetzt'),
    ('tv5', 'A6 S3 spricht deshalb von den „mit Tests geprüften Voraussetzungen“'),
    ('umfang', 'Das Intervall ist mit relevanten Effekten in beide Richtungen vereinbar. Der Befund ist unschlüssig.'),
    ('umfang', '**R1 Sensitivität.** Ändert eine der vorab festgelegten Varianten den Fall nach § 5.1 oder die Entscheidung über H0, steht sie mit Zahl in 5.2'),
    ('umfang', '**R4 Fallzahlregel.** Unter acht Spielern je Gruppe keine Inferenz'),
    ('uebergabe', 'Projektauslegung: Anhangsobjekte (Tab. H1 bis H5) dürfen beim Erstverweis in der Klammer stehen'),
    ('uebergabe', 'kein Satz endet auf eine Ziffer oder einen Einzelbuchstaben'),
    ('register', '„eine Aussage je Satz“ in A2 S1, A2 S4, A5 S5 und A6 S4 mehrdeutig'),
    ('tv61', '6.3 G6: Gründe nicht durchgeführter Einheiten wurden nicht erfasst'),
    ('memo_b', 'Nach Wortlaut erfasst „bei keiner Zielgröße“ alle Zielgrößen der Studie.'),
    ('befund', 'in 5 von 10, vor dem ersten Befund in 4 (Lloyd danach)'),
    ('befund', 'einer mit einem Quantor über die Tests einer Zielgröße (Hammami 1.3)'),
    ('befund', 'nur, wo sie Frage der Studie sind'),
    ('befund', 'Erweitert am Anfang (Padrón-Cabo 1.1 und 1.2, Rogers 1.1 mit dem Ausgangsunterschied gegen die SWC) oder am Schluss (Klusemann 4.6, Asimakidis 1.7 mit der kleinsten bedeutsamen Veränderung).'),
    ('befund', 'Kein Kern-Ergebnistext verweist auf ein Flussdiagramm.'),
    ('befund', 'Die Zahl der analysierten Spieler je Gruppe nennt kein Kern-Ergebnistext.'),
    ('befund', 'Beanspruchung** einmal im Kern (Beato, RPE je Gruppe)'),
    ('befund', 'Nach Zielgröße geordnet sind 6 von 10'),
    ('befund', 'Einen Befundblock eröffnen sie in 5 von 38 Blöcken'),
    ('befund', 'Adverbiale Konnektoren am Satzanfang in 14 von 108 Kernsätzen (13 %)'),
    ('befund', 'ordnet parallele Werte Gruppen oder Tests zu (8 Sätze in 5 Studien)'),
    ('befund', 'Abweichungen davon entscheidet Textvorschlag 5.'),
    ('befund', 'Vorbild sind sie für Objektführung und Kürze.'),
    ('befund', 'Eröffnung mit Objektverweis oder Orientierungsbefund (8 von 10, Hammami und Bouafif mit Sammelbefund)'),
    ('befund', 'drei Unterüberschriften-Studien unter den elf des Bauplans'),
    ('befund', 'An denselben acht Studien gemessen: Mittel 347'),
    ('tv5', 'Block je Zielgröße: Objekt, Richtung, adjustierte Differenz → KI → p (g in Tab. 3) → Fall'),
    ('tv5', 'Status der betroffenen Meldungen'),
    ('register', 'letzter Satz Befund mit Klammer'),
    ('f17', 'Jede Zahl im Text nennt ihre Bezugsmenge.'),
    ('f17', 'Vorlage: Moran et al. (2024) und Negra et al. (2019).'),
    ('f17', '| 3 Ergebnisse (5) | 336 | **450** |'),
    ('plan', 'Fall nach der Schlusslogik im Wortlaut der Musterformulierung, keine verbalen Effektetiketten'),
    ('gliederung', 'Ergebnisse (ohne Unterabschnitte, Ä16)'),
    ('kap5', 'beim 30-m-Sprint und Standweitsprung zu beiden Zeitpunkten die Interventionsgruppe, beim 505-Test je Seite überwiegend die Kontrollgruppe'),
    ('kap5', 'Bei keiner Zielgröße war damit ein Gruppenunterschied nachweisbar.'),
    ('kap5', 'Die übrigen mit Tests geprüften Voraussetzungen wurden nicht verworfen'),
    ('kap5', 'Soweit die Fallzahl eine Inferenz zuließ,'),
    ('kap5', ', und keine davon'),
    ('kap5', 'Adjustiert für'),
    ('kap5', 'Beim 505-Seitenmittel'),
    ("kap5", "sowie Hedges' g."),
    ('kap5', 'bis +0,107 s.'),
    ('kap5', 'neun und zwei Spieler, nach verschiedenen Einheitennummern neun und einer'),
    ('kap5', 'Zwölf Meldungen von neun Spielern'),
    ('kap5', 'davon je zwei zu nicht und zu teilweise durchgeführten Einheiten'),
    ('master', 'Sprung, Beschleunigung und Richtungswechsel'),
    ('master', 'Mehr als die Hälfte der Spieler mit Meldungen'),
    ('master', 'überwiegend zu vollständig durchgeführten Einheiten'),
    ('anlage', 'notably poor'),
    ('anlage', 'unadjusted IRR, 0.81 [95% CI, 0.63-1.03]'),
    ('anlage', 'adjusted IRR, 0.82 [95% CI, 0.64-1.04]) (Table 2).'),
    ('anlage', 'None of the 3 agility tests'),
]
aus('16 Zitatprüfung der angeführten Fundstellen (Leerraum vereinheitlicht)')
fehlt = []
NT = {k: norm(v) for k, v in TXT.items()}
NT['kap5'] = norm(ALLE)
NT['master'] = norm(' '.join(s['text'] for s in MS))
NT['anlage'] = norm(' '.join(r['text'] for r in KORPUS))
for k2, z in ZITATE:
    ok = norm(z) in NT[k2]
    aus('  ' + ('gefunden ' if ok else 'FEHLT    ') + k2.ljust(10), z[:110])
    if not ok:
        fehlt.append((k2, z))
PRUEF(fehlt == [], 'Zitate gefunden')
aus('  ' + str(len(ZITATE)), 'Zitate, alle gefunden')
aus('')

# ---------------------------------------------------------------- Teiltabelle 2b
f = {
    'W': U['W'], 'P': U['P'], 'S': U['S'], 'med': pz(U['med']), 'max': U['maxsatz'],
    'bw': G['B'], 'bp': pz(anteil_b), 'op': pz(anteil_o), 'vzw': G['V'] + G['Z'], 'vzp': pz(anteil_vz),
    'rp': pz(100 * (G['O'] + G['V'] + G['X']) / U['W']), 'vorw': rahmen['vor'], 'vorp': pz(100 * rahmen['vor'] / U['W']),
    'b2med': pz(med_b2), 'b2min': pz(min_b2), 'b2max': pz(max_b2), 'zw': sum(W(i) for i in z_vor),
    'o2w': o2w, 'o2p': pz(100 * o2w / U['W']),
    'kl': len(klammer), 'eine': len(eine), 'komma': len(komma), 'angeh': len(angeh), 'beato': pz(naechste_b2[0]),
    'setmin': pz(min(setting)), 'setmax': pz(max(setting)),
}
ROWS = [
    # (Prüfgegenstand, Maßstab, Befundstelle, Fundstelle im Text, Ergebnis, Status mit Register, Beleg)
    # ---- Prüfkatalog Nr. 1
    ('Prüfkatalog Nr. 1: Umfang und Gewicht (Prüfpunkt Befundanteil und Rahmen)', 'Korpus und Fundstelle', '§ 6.5 Nr. 1, § 0 Nr. 3, § 2, § 4', 'A1 bis A6',
     'Gemessen in 2a.1 bis 2a.13: {W} Wörter und {P} Absätze in der Spanne des Kerns, {S} Sätze über, Satzlänge (Median {med}) unter der Spanne (P12). Befundanteil {bw} Wörter = {bp} % unter der Spanne (26,4 bis 100 %), Orientierung {op} % und Rahmen (O, V, X) {rp} % in der Spanne über dem Median, Verfahren und Zusatz {vzw} Wörter = {vzp} % ohne Kernvorbild. Nachrechnung zur Ursache, außerhalb der Zählregel: Ohne die Sätze zur Veränderung je Gruppe (B2), die P2 ausschließt, liegt der Befundanteil im Kern bei Median {b2med} % ({b2min} bis {b2max} %). Kapitel 5 läge damit unter neun von zehn Kernstudien (nächste Beato mit {beato} %), nur Moran fällt ohne B2 auf 0 %, weil dort alle Befundsätze B2 sind. P2 erklärt den Abstand also nur zum Teil, den Rest tragen Rahmen und Absicherung. Jeder der 16 Sätze vor dem ersten Befund trägt eine P- oder E-Zeile des Rasters (Textvorschlag 5 § 4), die Absicherung folgt P8 und P9.',
     'bewusst anders · P2, P8 bis P10, P12, Raster 5.1.1 bis 5.1.11, Register 7b, 9a', 'pruef_2b.txt § 1, 2a.1 bis 2a.13'),
    # ---- Prüfkatalog Nr. 2 mit K1 bis K3
    ('K1 Rahmen vor dem ersten Befund (Prüfkatalog Nr. 2, Prüfpunkt Befundanteil und Rahmen)', 'Korpus', '§ 6.2 K1 (8 von 10, Median 22 %), § 2.1', 'A1 S1 bis A5 S2, erster Befund A5 S3',
     'Rahmen aus 16 Sätzen, {vorw} Wörter = {vorp} %, in der Spanne (0 bis 67,2 %), höher nur Beato, Satzzahl über der Spanne (Kern 0 bis 6). Codes X1, O1 bis O5 und Z2. Die zwei Z2-Sätze (A3 S3, S4, {zw} Wörter) sind nach dem Codebuch weder Orientierung noch Objektsatz. Z2 steht in keiner Studie als Primärcode vor dem ersten Befund, als Sekundärcode nur erweitert bei Klusemann (1.1 Verletzung als Grund eines Ausschlusses, 1.3 und 1.6 Krankheit als Grund verpasster Einheiten). Die unerwünschten Ereignisse gehören nach Raster 5.1.8 und Plan § 3 Task 11 in den Orientierungszug.',
     'erfüllt (Rahmen aus O und X wie Korpus), Z2 im Rahmen bewusst anders · Raster 5.1.8, Register 7b, 9a', 'pruef_2b.txt § 2, 2a.13'),
    ('K2 Ausgangsvergleich der Gruppen vor den Befunden (Prüfkatalog Nr. 2)', 'Korpus', '§ 6.2 K2 (5 von 5), § 3.1', 'A1 S3, A1 S4',
     'Ausgangswerte mit standardisierter Differenz und Überlappung in Tab. 2 (A1 S3), Richtung aller Ausgangsunterschiede im Satz (A1 S4), beides vor dem ersten Befund, ohne Test (P1).',
     'erfüllt · Register 1e, 10e', '2a.17, pruef_2b.txt § 9'),
    ('K3 Objekte einführen und wiederaufrufen (Prüfkatalog Nr. 2, Prüfpunkt Tab. H3 als Subjekt)', 'Korpus', '§ 6.2 K3, § 3.2, § 0 Nr. 8', 'A1 S1, S3, A2 S1, S3, A4 S1, S2, A5 S1, S2, S11, A6 S3, S4',
     'Nach der Korpusbasis (Erstnennung im Ergebnisteil, 2a.25) stehen von neun Objekten vor dem ersten Befund fünf in einem Objektsatz (Abb. 1, Tab. 2, Tab. H3, Tab. 3, Abb. 2, Kern 11 von 14 Objekten des Rahmens), alle als Subjekt im Präsens, die Ort-Form fehlt (Kern 10 Sätze in 7 Studien). Vier stehen in der Klammer: Tab. H2 und Tab. H5 nach der Registerauslegung, Tab. 1 und Tab. H1, die seit 4.4 eingeführt sind. Nach der Erstnennung im Manuskript sind es fünf von sieben. Wiederaufrufe stehen als Klammer am Satzende, im Kapitel 3 von 3 (Kern 11 von 14 Wiederaufrufen), dazu Tab. H4 aus 4.7. Tab. H3 als Subjekt (elliptisch) folgt Stilprofil Teil 4 und K3, die Auslegung lässt die Klammer zu, verlangt sie nicht. Die Befundsätze A5 S3 bis S10 tragen keine Klammer, Tab. 3 und Abb. 2 stehen unmittelbar davor (Stilprofil Teil 4: „höchstens“).',
     'erfüllt · Register 1d, 1e, 1f, U2', 'pruef_2b.txt § 3, 2a.24 bis 2a.27'),
    # ---- Prüfkatalog Nr. 3 mit K4 und K5
    ('K4 Modellergebnis vor Vergleichen einzelner Gruppen (Prüfkatalog Nr. 3)', 'Korpus', '§ 6.2 K4 (4 von 5), § 3.3', 'A5 S4, S5',
     'Zwei Gruppen, keine Paarvergleiche, keine Veränderung je Gruppe (P2). Je Zielgröße ist die adjustierte Differenz das einzige Modellergebnis, Vergleiche einzelner Gruppen gibt es nicht. Die Stellung von A5 S3 vor dem Modellergebnis prüft 2b.6.',
     'erfüllt (gegenstandslos) · Register 10a', '2a.28, pruef_2b.txt § 5'),
    ('Prüfkatalog Nr. 3: Modellergebnis je Zielgröße vor allem anderen', 'Korpus', '§ 6.5 Nr. 3, § 6.1 (Grundfigur „das Modellergebnis zuerst“)', 'A5 S3 vor A5 S4, S5',
     'Je Zielgröße beginnt der Block mit der adjustierten Differenz (A5 S4, S5). Vor allen Blöcken steht A5 S3 mit Richtung und Abstand der unadjustierten Differenzen (B1 nach dem Codebuch), der Befundteil beginnt also nicht mit dem Modellergebnis. Unadjustiert vor adjustiert hat kein Kernvorbild, erweitert Hilska 3.3 (beide in einer Klammer). Die Folge steht in der Zug-Tabelle von Textvorschlag 5 („Objekt, Richtung, adjustierte Differenz → KI → p“), einen Grund nennt sie nicht.',
     'teilweise · P4, Raster 5.2.2, Register 9a, 10n', '2a.28, 2a.40, Textvorschlag 5 § 2'),
    ('K5 Folge der Zielgrößenblöcke mit Bezug, bei Wiederkehr dieselbe (Prüfkatalog Nr. 3)', 'Korpus', '§ 6.2 K5, § 3.3 („Für Kapitel 5 zählt die Blockfolge“)', 'A5 S4, S5 · A4 S2',
     'Blockfolge S → C → J wie Methodik (4.4.1 bis 4.4.3) und Thema (F17 § 2), nach der zweiten Lesart (erste Nennung im Befundtext) ebenso. In Befundsätzen kehrt keine Zielgröße wieder. A4 S2 (S, J, C) ist ein Orientierungssatz und zählt nach der Blockfolge nicht. Liest man „bei Wiederkehr dieselbe“ über das ganze Kapitel, kehren die Zielgrößen nach A4 S2 in anderer Folge wieder (2b.8).',
     'erfüllt (nach der Blockfolge) · —', 'pruef_2b.txt § 4, 2a.30'),
    ('Prüfkatalog Nr. 3: Reihenfolge durchgehend und deckungsgleich mit Titel, Hypothesen, 4.4 und 6.1 (Prüfpunkt A4 S2)', 'Fundstelle', '§ 6.5 Nr. 3 · F17 § 5.1 „Reihenfolgetreue“', 'A4 S2, A5 S4, S5, S11 · Thema, B5 S1, S3, 4.1 A4 S2, 4.4.1 bis 4.4.3, 4.7 A3 S1, 6.1 A3 bis A5',
     'Befundsätze und A5 S11 (S, C) folgen S → C → J. A4 S2 nennt S, J, C, weil der Satz nach der Gruppe mit mehr gültigen Versuchen ordnet („beim 30-m-Sprint und Standweitsprung … die Interventionsgruppe, beim 505-Test je Seite überwiegend die Kontrollgruppe“). Thema (F17 § 2), Ankersatz und H0 (B5 S1, S3), 4.1 A4 S2, 4.4.1 bis 4.4.3, 4.7 A3 S1 und die Absätze A3 bis A5 von 6.1 folgen S → C → J, H1 (B5 S4) nennt keine Folge. 6.1 A3 S7 zählt Fähigkeiten auf („Sprung, Beschleunigung und Richtungswechsel“), Prüfung in 2 (e). Zur Folge in A4 S2 gibt es keine Entscheidung, die Registerprüfung hat den Satz darauf nicht geprüft.',
     'teilweise · F17 § 5.1, Startprompt (Reihenfolge), kein Registereintrag', 'pruef_2b.txt § 4'),
    # ---- Prüfkatalog Nr. 4 mit K6
    ('K6 Ordnung nach Zielgröße, Blockbeginn (Prüfkatalog Nr. 4)', 'Korpus und Fundstelle', '§ 6.2 K6, § 3.3 · F17 § 5a, Plan § 3 Task 11', 'A5 S3 bis S10',
     'Geordnet nach Analyseschritt über alle Zielgrößen (unadjustiert → adjustiert je Zielgröße → Nachweis → Intervall gegen SESOI → Fall → Entscheidungsregel → H0) wie Sammoud (nach Gruppe oder Analyseschritt 3 von 10), nicht nach Zielgröße (6 von 10). Blockbeginn mit Quantor (A5 S3, S6), Modell als Partizip („Adjustiert für …“, A5 S4) und Themenanker („Beim 505-Seitenmittel“, A5 S5). Alle Formen sind im Kern belegt, ein Quantor als Einzelbefund am Blockbeginn aber nur in einem von 38 Blöcken (Hammami 1.3). F17 § 5a („dann je Zielgröße in fester Reihenfolge“) ist in der Folge erfüllt. Der Fall steht einmal für alle drei Zielgrößen (A5 S7, S8), der Plan sah ihn je Zielgröße im Block vor („je Zielgröße in fester Reihenfolge ein Block (…, Fall nach der Schlusslogik …)“).',
     'teilweise · Register 7b, 9a (freigegebener Wortlaut, Ordnung nicht eigens begründet)', '2a.28, 2a.29, pruef_2b.txt § 5'),
    # ---- Prüfkatalog Nr. 5 mit K7 bis K9
    ('K7 Nullbefunde ausdrücklich (Prüfkatalog Nr. 5)', 'Korpus', '§ 6.2 K7 (9 von 10), § 3.5', 'A5 S6 bis S10, A6 S4',
     'Fehlender Nachweis (S6), Intervall gegen den SESOI (S7), Fall (S8), Entscheidungsregel (S9), H0 (S10), Absicherung (A6 S4). Form nach P6.',
     'erfüllt · Register 3c, r2', '2a.33, pruef_2b.txt § 6'),
    ('K8 Sammelbefund mit Quantor, Ausnahmen (Prüfkatalog Nr. 5, Prüfpunkt Zählregel)', 'Korpus', '§ 6.2 K8 (6 von 10, B: 8), § 3.5, § 6.5 Zählregel', 'A5 S10 · Quantoren A1 S4, A4 S1, A5 S3, S6, S7, S9 · A5 S11',
     'Nach dem Codebuch B4 nur A5 S10 (Entscheidung über H0, Kern 0). Kein Befund gilt für alle sieben Zielgrößen, die deskriptiven sind nicht geprüft, ein Sammelbefund im Sinn von K8 ist daher nicht gefordert. Quantoren über alle sieben Zielgrößen stehen in Orientierungssätzen (A1 S4 nach Regel 2 O4, A4 S1 nach der Definition O5), Quantoren über die drei konfirmatorischen in Befundsätzen (A5 S3, S6, S7, S9, B1), die Ausnahme der deskriptiven nennt A5 S11. Nach den Hinweisen (H2, Projektauslegung) Sammelbefunde A5 S3, S6 bis S10 und A6 S4 sekundär. Für die Leseführung: A5 S6 („Bei keiner Zielgröße war damit …“) bindet den Quantor nur über „damit“ an die drei geprüften, Codierer B las ihn nach dem Wortlaut zunächst über alle Zielgrößen (memo_B), der Konsens nicht.',
     'erfüllt (nach dem Codebuch gegenstandslos) · Übergabe § 5 Nr. 3 (H2)', '2a.34, pruef_2b.txt § 6, blind/memo_B.md'),
    ('K9 Gegenbefunde und Kontraste am Ort (Prüfkatalog Nr. 5)', 'Korpus', '§ 6.2 K9, § 3.5', 'A4 S2, A5 S3 bis S5 · A6 S1, S2',
     'Kein Gegenbefund unter den Befunden (Fall C1 bei allen drei). Kontraste stehen am Ort: A4 S2 im selben Satz (gültige Versuche Interventions- gegen Kontrollgruppe), A5 S3 nennt den Abstand der unadjustierten zur adjustierten Differenz, deren Werte folgen in A5 S4 und S5 ohne Konnektor (2a.35). Die Einschränkung des 30-m-Befunds durch die verworfene Normalverteilung und das Bootstrap-Intervall (A6 S1, S2) folgt dem Befund (A5 S4) erst nach sieben weiteren Sätzen, in der Absicherung nach Plan (2b.28). Sie ist kein Gegenbefund im Sinn von K9, ein Kernvorbild gibt es nicht.',
     'erfüllt (Kontraste am Ort) · Register 6d, 10i', '2a.35, pruef_2b.txt § 6'),
    # ---- Prüfkatalog Nr. 6 mit K10
    ('K10 Schluss mit Befund- oder Objektsatz, kein Resümee, kein Beleg, Präteritum (Prüfkatalog Nr. 6, Prüfpunkt Schluss)', 'Korpus', '§ 6.2 K10 (10 von 10), § 2.1, § 6.1 Grundfigur', 'A6 S4, letzter Befundsatz A5 S10',
     'Letzter Satz A6 S4: nach dem Codebuch Z1 mit B1 und V2, nach den Hinweisen Z1 mit B4 und V2, Klammer am Satzende (Tab. H4). Kein Kern-Ergebnisteil endet mit einem Z-Satz (Befundsatz 8, Objektsatz 2, Klammer am Satzende 5), erweitert enden vier mit einem O-Satz. Der letzte Befundsatz A5 S10 hat keine Klammer, ihm folgen A5 S11 und die Absicherung. Kein Resümee, kein Beleg, Präteritum außerhalb der Objektsätze. Gegen die Grundfigur in § 6.1 („→ Absicherung … → letzter Befundsatz mit Objektklammer“) schließt die Absicherung selbst. Textvorschlag 5 § 2 und die Registerprüfung (10g: „letzter Satz Befund mit Klammer“) lesen A6 S4 als Befundsatz, dann ist auch Raster § 3.13 („Schluss = letzter Befundsatz mit Objektverweis“) erfüllt. Plan § 3 Task 11 („letzter Satz mit Objektverweis, kein Resümee“) ist in jeder Lesart erfüllt.',
     'teilweise (nach dem Codebuch Z1 am Schluss, Befundinhalt und Klammer wie Kern) · Register 9a, 10g', 'pruef_2b.txt § 7, 2a.16, 2a.27'),
    ('Prüfkatalog Nr. 6: Präsens außerhalb der Objektsätze', 'Korpus', '§ 6.5 Nr. 6, § 3.6', 'alle Sätze',
     'Präsens nur in den vier Objektsätzen (A1 S1, S3, A5 S1, S2), die übrigen 25 Sätze im Präteritum (F17 § 10, Zeitform).',
     'erfüllt · —', 'pruef_2b.txt § 8, 2a.37'),
    # ---- Prüfkatalog Nr. 7: P1 bis P12
    ('P1 Ausgangslage ohne Signifikanztest, Größe und Überlappung im Objekt (Prüfkatalog Nr. 7)', 'Fundstelle', '§ 6.3 P1 · F17 § 4, Raster 5.1.5', 'A1 S3, S4',
     'Tab. 2 mit standardisierter Differenz d und Überlappung der Kovariaten (A1 S3), im Satz nur die Richtung (A1 S4), kein Test, keine Zahl aus Tab. 2.',
     'erfüllt · Register 10e', 'pruef_2b.txt § 9'),
    ('P2 keine Veränderung je Gruppe mit Test, keine Prozentveränderung', 'Fundstelle', '§ 6.3 P2 · Textvorschlag 5 § 3 aus F17 § 11.2, § 10, Umfangsdokument § 5.4 Nr. 2 und 9', 'alle Sätze',
     'Kein B2-Satz, keine Prä-Post-Werte, Prozent nur als Umsetzungsrate (A2 S2) und im Wort „95-%-Konfidenzintervall“ (A5 S4), keine Veränderungswörter („verbessert“, „Erhalt“, „Rückgang“).',
     'erfüllt · Register 10d', 'pruef_2b.txt § 9'),
    ('P3 adjustierte Differenz mit 95-%-KI und p im Satz, g im Objekt', 'Fundstelle', '§ 6.3 P3 · F17 § 10, Raster § 3.13, Plan § 3 Task 11, Textvorschlag 5 § 3', 'A5 S1, S4, S5',
     'Je Zielgröße adjustierte Differenz mit Intervall („bis“) und exaktem p, Subtraktionsrichtung genannt („Interventions- minus Kontrollgruppe“), g als Inhalt von Tab. 3 (A5 S1), keine Teststatistik. Zeiten mit drei, Weite mit einer Nachkommastelle, Vorzeichen bei Differenzen und Grenzen (F17 § 5.3).',
     'erfüllt · Register Zeile 16, 10c, 11e, 11f', 'pruef_2b.txt § 9'),
    ('P4 unadjustiert neben adjustiert', 'Fundstelle', '§ 6.3 P4 · F17 § 4, Raster 5.2.2', 'A5 S1, S3 bis S5',
     'Tab. 3 enthält beide (A5 S1), A5 S3 nennt Richtung und Abstand der unadjustierten ohne Zahl, kein unadjustierter p-Wert.',
     'erfüllt · Register 10n', 'pruef_2b.txt § 9'),
    ('P5 keine Größenklasse, Einordnung über die Schlusslogik', 'Fundstelle', '§ 6.3 P5 · F17 § 5a, § 11.2b, Umfangsdokument § 5.1', 'A5 S6 bis S8',
     'Keine Größenklasse und kein Effektetikett. Plan § 3 Task 11 verlangt den „Fall nach der Schlusslogik im Wortlaut der Musterformulierung“. Fall C1 nach der Musterformulierung („Ein Gruppenunterschied ist nicht nachweisbar. Das Intervall ist mit relevanten Effekten in beide Richtungen vereinbar. Der Befund ist unschlüssig.“) in A5 S6 bis S8, abgewandelt im Präteritum (F17 § 10, Zeitform der Ergebnisse), für drei Zielgrößen gefasst („Bei keiner Zielgröße“, „Jedes Intervall“, „Die Befunde“) und mit „Unterschieden“ statt „Effekten“ („Effekt“ steht auf der Wortliste von Plan § 3 Task 11 und Textvorschlag 5 § 0).',
     'erfüllt · Register 3c, 6i, 10b', 'pruef_2b.txt § 9'),
    ('P6 Nullbefund als „kein Gruppenunterschied nachweisbar“ mit Schätzer, Intervall und Fall', 'Fundstelle', '§ 6.3 P6 · F17 § 10', 'A5 S4 bis S8',
     '„Bei keiner Zielgröße war damit ein Gruppenunterschied nachweisbar.“ (A5 S6), Schätzer und Intervall in A5 S4 und S5, Fall in A5 S7 und S8, ausgeschlossene Formen fehlen.',
     'erfüllt · Register 3c, r2', 'pruef_2b.txt § 9'),
    ('P7 Entscheidung über H0 im Ergebnisteil', 'Fundstelle', '§ 6.3 P7 · F17 § 11.2b, Umfangsdokument § 5.1, Textvorschlag 4.7 § 7', 'A5 S9, S10',
     'Entscheidungsregel an der adjustierten Differenz (A5 S9), Entscheidung in A5 S10, weder „Studienprotokoll“ noch „Ethikantrag“ im Kapitel.',
     'erfüllt · Register 4a, 6f, 6k', 'pruef_2b.txt § 9'),
    ('P8 verworfene Voraussetzung mit Prüfgröße, p und Bootstrap-KI, übrige „geprüft und nicht verworfen“ (Prüfpunkt A6 S3)', 'Fundstelle', '§ 6.3 P8 · F17 § 11.9, Umfangsdokument R2, Textvorschlag 4.7 § 7', 'A6 S1, S2, S3',
     'W und p beim 30-m-Sprint (A6 S1), Bootstrap-KI daneben, als nachträglich festgelegt gekennzeichnet (A6 S2), die übrigen Prüfungen in einem Sammelsatz (Zeile 16). A6 S3 („Die übrigen mit Tests geprüften Voraussetzungen wurden nicht verworfen“) trägt beide Teile der Formel, nicht ihren Wortlaut, „mit Tests“ grenzt die nur grafisch geprüfte Linearität aus (Textvorschlag 5 § 3). Kein „erfüllt“.',
     'teilweise (sinngleich, nicht wörtlich, Schwere C) · Register 6g, 6a, 6d, 10i, 10m, 3d (R2), Zeile 16, c4', 'pruef_2b.txt § 9, register_pruefung.md 6g'),
    ('P9 Sensitivität und Per-Protokoll in einem Sammelsatz', 'Fundstelle', '§ 6.3 P9 · Umfangsdokument R1, R4', 'A6 S4',
     'Ein Sammelsatz mit dem beobachtenden Per-Protokoll-Vergleich und den sechs Sensitivitätsanalysen in der Zählung von 4.7, Inferenz nur soweit die Fallzahl reicht (R4), keine Variante ändert Fall oder Entscheidung (R1), Klammer (Tab. H4).',
     'erfüllt · Register 3d (R1, R4), 6j, 10h, 10t, c4', 'pruef_2b.txt § 9'),
    ('P10 Ereignisse und Schmerzmeldungen je Status, Kontrollgruppe ohne Instrument', 'Fundstelle', '§ 6.3 P10 · CONSORT 19, Raster 5.1.8, Textvorschlag 5 § 4', 'A3 S3, S4',
     'Zwölf Meldungen von neun Spielern, je zwei zu nicht und zu teilweise durchgeführten Einheiten, Kontrollgruppe ohne Erhebung, ohne Lokalisation und ohne Kausalzuschreibung. Die acht Meldungen zu vollständig durchgeführten Einheiten ergeben sich nur rechnerisch (12 − 2 − 2), obwohl K-10.12 als Berichtsort den Text nennt, Textvorschlag 5 § 4 nennt den „Status der betroffenen Meldungen“. 6.1 A6 S2 baut darauf („überwiegend zu vollständig durchgeführten Einheiten“). Bezugsmenge der neun Spieler in 2b.45.',
     'erfüllt (Status „ganz“ nur rechnerisch) · Register 9d, V1, U1', 'pruef_2b.txt § 9, K-10.12'),
    ('P11 Analysezahl je Gruppe und Zielgröße im Objekt', 'Fundstelle', '§ 6.3 P11 · CONSORT 16, F17 § 3', 'A1 S1 bis S3, A5 S1',
     'Im Text nur 26 Analysierte gesamt (A1 S2), Spieler je Gruppe und Nenner je Zielgröße in Abb. 1, Tab. 2 und Tab. 3.',
     'erfüllt · Register 2c, 2f', 'pruef_2b.txt § 9'),
    ('P12 Satzlänge, Semikolon, Konnektoren', 'Fundstelle', '§ 6.3 P12 · Stilprofil Teil 2 und 3, F17 § 10', 'alle Sätze',
     'Median {med}, längster Satz {max} (A6 S4), kein Semikolon, kein adverbialer Konnektor am Satzanfang.',
     'erfüllt · Register 1b, r1', '2a.4, 2a.36, pruef_2b.txt § 9'),
    # ---- Prüfkatalog Nr. 8 bis 10
    ('Prüfkatalog Nr. 8: Umsetzung, Umfang gegen die Settingstudien, Stellung', 'Korpus und Fundstelle', '§ 6.5 Nr. 8, § 3.1, § 6.4', 'A2 S1 bis S4',
     '{o2w} Wörter = {o2p} % in vier Sätzen (Setting {setmin} bis {setmax} %, im Kern 4 bis 12 % in den vier Studien mit O2-Sätzen, Negra 2020 nur als Sekundärcode). Vor dem ersten Befund wie im Kern (Befund § 3.1: Umsetzung „in 5 von 10, vor dem ersten Befund in 4 (Lloyd danach)“) und wie bei Klusemann, bei Veith und Rogers danach, bei Hilska vor und nach den Befunden. Inhalt: Meldungen nach Status mit Nenner, Median, Umsetzungsrate, Schwellen sechs und neun, Untergrenzen. Spanne je Spieler, Verteilung und Wochenverlauf stehen nur in Tab. H2, Gründe nicht durchgeführter Einheiten sind nicht erfasst (Textvorschlag 6.1 § 9, 6.3 G6). Niedrige Umsetzung als Zahl an den Schwellen, ohne Etikett (Rogers: „notably poor“).',
     'erfüllt (Umfang wie Setting, Stellung nach Plan) · Register 2g, 9c, 10p, 10s, 14a, c7, c9', 'pruef_2b.txt § 10, 2a.18'),
    ('Prüfkatalog Nr. 9: Absicherung, Stellung und Grund', 'Fundstelle', '§ 6.5 Nr. 9, § 6.1, § 6.4 · F17 § 5a, Plan § 3 Task 11, Textvorschlag 5', 'A5 S11, A6 S1 bis S4',
     'Nach dem Gruppenvergleich und nach A5 S11. Der Kern hat keine Datenprüfung und keine Sensitivitätsanalyse, Z1 steht dort nur sekundär in Objektsätzen zu Einzelwertdarstellungen (Moran 1.1 bis 1.3 vorn, Liu 2.5 im Befundteil). Erweitert steht die Datenprüfung vorn (Veith 1.1, Asimakidis 1.1) oder mit einer Analyseregel im Befundteil (Hilska 6.1, Veith 2.3), Zusatzanalysen stehen vorn als Objektsatz (Rogers 1.3, 1.8), im Befundteil (Hilska 4.2, Rogers 2.1, 2.3, 2.4) oder danach (Asimakidis 1.6). Analyseregeln (V2) stehen vorn (Rogers 1.2, 1.9, sekundär Sammoud 1.1, Klusemann 1.5) oder im Befundteil (Hilska 6.1, Veith 2.3, sekundär Lloyd 1.3), nie nach dem letzten Befund. In Kapitel 5 steht A5 S11 (V2) danach, die Absicherung schließt das Kapitel (2b.13). F17 § 5a nennt keine Stellung, Plan § 3 Task 11 führt Voraussetzungen und Sensitivitäten nach den Zielgrößenblöcken auf, Textvorschlag 5 § 2 stellt sie an den Schluss. Einen Grund für die Stellung nennen Plan und Textvorschlag nicht, R2 verlangt das Bootstrap-KI neben der verworfenen Prüfung, keine Stellung im Kapitel.',
     'erfüllt (Stellung nach Plan) · Register 6d, 9a, 10h, 10i, Zeile 16', 'pruef_2b.txt § 11, 2a.22'),
    ('Prüfkatalog Nr. 10: Anschluss an 6.1', 'Fundstelle', '§ 6.5 Nr. 10', '24 Sätze von 6.1 (Abgleichbefund § 1.4)',
     'Jeder Befund, den 6.1 nennt, steht in Kapitel 5 oder in einem Objekt, auf das Kapitel 5 verweist (Tab. 2, Tab. 3, Abb. 2, Tab. H2, Tab. H4, Tab. H5). Nur über Objekte: 6.1 A3 S2, A4 S2, A5 S2, A5 S8 sowie Teile von A2 S2, A2 S6 und A6 S2 (Bezugsmenge 15). Der zweite Teil von 6.1 A6 S2 („überwiegend zu vollständig durchgeführten Einheiten“) beruht auf den acht Meldungen, die Kapitel 5 nur rechnerisch nennt (2b.24). Eine Änderung in A1, A2, A3, A5 oder A6 berührt Sätze von 6.1, A4 keinen (später 6.3 G5). Wortlaut und Doppelung in 2 (e).',
     'erfüllt (Deckung) · Register 15b, c8', 'pruef_2b.txt § 12, Abgleichbefund § 1.4'),
    # ---- Weitere Aussagen des Befunds
    ('§ 0 Nr. 4 Grundfigur, Resümee, Hypothese', 'Korpus', '§ 0 Nr. 4, § 2.1', 'A1 bis A6',
     'Rahmen → Befunde (nach Analyseschritt) → Absicherung → Schluss mit A6 S4. Kein Resümee über die Studie, A6 S4 fasst die Absicherung zusammen (R1). Entscheidung über H0 in A5 S10 (Kern 0, P7). Ordnung und Schluss in 2b.9 und 2b.13.',
     'teilweise (Absicherung als Schluss, H0 nach P7) · Register 4a, 9a, 10g', '2a.15, pruef_2b.txt § 7'),
    ('§ 0 Nr. 9 und § 6.1 abgeleitete Struktur, Projektteile gegen ihre Fundstellen', 'Korpus und Fundstelle', '§ 0 Nr. 9, § 6.1', 'A1 bis A6 · Gliederung v6 (Ergebnisse, Ä16), Plan § 3 Task 11',
     'Orientierungszug mit Objekteinführung (A1 bis A4) → Gruppenvergleich in fester Zielgrößenfolge, nach Analyseschritt (A5) → Absicherung (A6). Der Schluss ist nach Textvorschlag 5 § 2 der letzte Befundsatz mit Klammer (A6 S4), nach dem Codebuch ein Z1-Satz (2b.13). Zusammenstellung des Orientierungszugs wie Plan (Fluss, planmäßiges Ende, Ausgangswerte, Umsetzung mit Tab. H5, CR-10 und Load, unerwünschte Ereignisse, Messgüte), in A4 TE vor den gültigen Versuchen. Gegen die Aufzählung im Plan stehen Abb. 2 vor den Befunden, die deskriptiven Zielgrößen (A5 S11) vor der Absicherung und das Antragskriterium in A2 S3. Gliederung v6 und Plan nennen „Abb. 1, Tab. 2, Abb. 2, Tab. 3“, Kapitel 5 führt Tab. 3 vor Abb. 2 ein (Textvorschlag 5 § 0: der Gruppenvergleich setzt mit „Tab. 3 enthält …“ ein). Abweichungen von Plan und F17 § 5a entscheidet nach Befund § 6.1 Textvorschlag 5 („Abweichungen davon entscheidet Textvorschlag 5.“). Einen Grund nennt er für die Objektfolge (§ 0) und das Antragskriterium (Register 9c), für die Stellung von Abb. 2 und A5 S11 steht nur die Folge der Zug-Tabelle (§ 2).',
     'bewusst anders, wo Textvorschlag 5 entscheidet (Stellung von Abb. 2 und A5 S11, Objektfolge, Antragskriterium) · Register 7a, 7b, 9a, 9c, U9', 'pruef_2b.txt § 11, § 13'),
    ('§ 1.1 und § 1.2: Fragen von Kapitel 5, für die der Korpus erweitert ist, keine Interviewbefunde', 'Korpus', '§ 1.1, § 1.2', 'A2, A3 S3, S4, A4 S1, A5 S4, S5, A6 S2',
     'Alle vier Fragen stehen in Kapitel 5: Umsetzung ohne Aufsicht (A2), unerwünschte Ereignisse (A3 S3, S4), Intervalle (A5 S4, S5, A6 S2), Messgüte gegen eine kleinste bedeutsame Veränderung (A4 S1). Keine Interviewbefunde.',
     'erfüllt · —', 'pruef_2b.txt § 13'),
    ('§ 3.1 Orientierung im Einzelnen', 'Korpus', '§ 3.1, § 0 Nr. 5', 'A1 bis A4',
     'Ausgangslage als Gruppenvergleich ohne Test (Kern 5, davon 4 mit Test, P1) · Teilnehmerfluss mit Verweis auf das Flussdiagramm im Ergebnistext (Kern 0, CONSORT 13a, F17 § 5a: „Flussdiagramm im Methodikteil – es gehört nach 5.1“), „planmäßig“ beendet, Analysezahl je Gruppe wie im Kern nicht im Text · Messgüte vor den Befunden gegen den SESOI (Kern nur Aloui am Anfang, erweitert am Anfang Padrón-Cabo und Rogers mit dem Ausgangsunterschied gegen die SWC, am Schluss Klusemann und Asimakidis mit der kleinsten bedeutsamen Veränderung) · Beanspruchung nur der Interventionsgruppe (Kern Beato je Gruppe, die Kontrollgruppe hatte kein Instrument) · Umsetzung in 2b.27, Datenprüfung in 2b.28, Folge der Orientierung in 2b.42.',
     'bewusst anders (Ausgangslage ohne Test nach P1, Flussdiagramm im Ergebnisteil nach F17 § 5a), Messgüte und Beanspruchung wie Korpus · Register 3a, 8a, 10e, 11h', '2a.17 bis 2a.23'),
    ('§ 3.6 Leseführung', 'Korpus', '§ 3.6', 'alle Sätze',
     'Themenanker in A2 S2, S4, A3 S4, A5 S5 und A6 S1, als Blockbeginn einmal (A5 S5, Kern 5 von 38). Kein adverbialer Konnektor (Kern 13 %). Parallele Werte ohne Zuordnungswort in A2 S4 („neun und zwei Spieler … neun und einer“, zugeordnet über die Schwellen in A2 S3), Korpus „respectively“ in 8 Sätzen in 5 Studien, Bausteine in 2 (c). Passiv viermal, Analyse oder Test als Subjekt zweimal, keine Wir-Form.',
     'erfüllt (Leseführung ohne Konnektor), Zuordnung in A2 S4 offen für 2 (c) · Register r1', '2a.36, pruef_2b.txt § 14'),
    ('§ 3.7 Was der Ergebnisteil nicht tut', 'Korpus', '§ 3.7, § 0 Nr. 4', 'alle Sätze',
     'Wie der Kern: keine Belege, keine Deutung, Analysezahl je Gruppe nicht im Text. Anders nach Projektregeln: Hypothesenentscheidung (P7), unerwünschte Ereignisse (P10), Datenprüfung (P8), Sensitivität (P9), unadjustiert neben adjustiert (P4).',
     'bewusst anders (P4, P7 bis P10), Belege, Deutung und Analysezahl wie Korpus · Register 4a, 6d, 9d, 10r', '2a.38 bis 2a.40'),
    ('§ 4 Einordnung des eigenen Budgets (Projektableitung)', 'Fundstelle', '§ 4, letzter Absatz', 'Kapitel 5 · Gliederung v6, F17 § 5.2',
     'Budget 450 nach Gliederung v6 und F17 § 5.2, 450 von 6.350 = 7,1 %, in der Spanne des Kerns (2,9 bis 12,1 %) über dem Median (5,7 %), unter dem Maximum (539). Grund nach F17 § 5.2 („drei konfirmatorische Zielgrößen plus Fluss, Adhärenz, Ausgangswerte“). Kapitel 5 steht bei 450 von 450.',
     'erfüllt (Fundstellen stimmen) · Register 7c, 9a, 9b', 'pruef_2b.txt § 13'),
    ('§ 6.4 Was der Korpus nicht hergibt', 'Korpus und Fundstelle', '§ 6.4', 'A2, A5 S4 bis S8, A6',
     'Ohne Korpusvorbild umgesetzt: Schlusslogik mit Intervall gegen null und SESOI (A5 S7, S8), adjustierte Rohdifferenz mit Intervall im Satz (A5 S4, S5, erweitert Veith 2.5), Stellung der Absicherung (A6), Folge der Orientierung (Plan), niedrige Umsetzung vor den Befunden ohne Etikett (A2, erweitert Rogers danach mit Einstufung).',
     'bewusst anders · P3, P5, P6, Register 3c, 6d, 9a, Zeile 16', 'pruef_2b.txt § 9 bis § 11'),
    ('§ 7 Nr. 1 Satzfolge für die ANCOVA', 'Fundstelle', '§ 7 Nr. 1, Raster § 3.13 Kopfblock', 'A5 S1, S4, S5',
     'Adjustierte Differenz → KI → p im Satz, g in Tab. 3, keine Wechselwirkung, keine Haupteffekte, kein Post-hoc.',
     'erfüllt · Register U4, 10a, Zeile 16', 'pruef_2b.txt § 9'),
    ('§ 7 Nr. 2 Teststatistik, Richtung, Größenklasse, Kennwerte in der Tabelle', 'Korpus und Fundstelle', '§ 7 Nr. 2', 'A3 S1, S2, A5 S3 bis S8, A6 S1',
     'Keine Teststatistik zum Gruppenvergleich (W nur zur Voraussetzung in A6 S1), Richtung unadjustiert in Worten (A5 S3), adjustiert über das Vorzeichen bei genannter Subtraktionsrichtung, statt einer Größenklasse der Fall. Mittelwert ± SD nur in Orientierungssätzen (A3 S1, S2, wie Beato), nicht in Befundsätzen.',
     'erfüllt · Register 6i, 10c, Zeile 16', '2a.31, 2a.32'),
    ('§ 7 Nr. 4 und Nr. 5 keine Deutung, kein zusammenfassender Satz', 'Korpus', '§ 7 Nr. 4, Nr. 5', 'alle Sätze, A6 S4',
     'Deutung 0 nach beiden Codierern, keine Verbots- und Deutungswörter (Stilprofil Teil 3 und 5, Plan § 3 Task 11, Textvorschlag 5 § 0). Kein Resümee über die Studie: A6 S4 fasst die Absicherung zusammen (Z1 mit B1 und V2 nach dem Codebuch), kein Ergebnisteil des Korpus endet mit einem Z-Satz (2b.13).',
     'erfüllt · Register 10g, 10r, r1', 'pruef_2b.txt § 14'),
    ('§ 7 Nr. 7 Vorlagen', 'Korpus', '§ 7 Nr. 7', 'A1 S1, S3, A5 S1 bis S5',
     'Objektsätze als Subjekt wie Moran (3) und Negra 2019 (1). Gruppenvergleich im Post-Wert über alle Zielgrößen in einem Satz wie Sammoud 2.1, im Kern das nächste ANCOVA-Vorbild (dort folgen in 2.2 und 2.3 die Veränderungen je Gruppe, die P2 ausschließt). Adjustierte Differenz mit Intervall und p im Satz wie Veith 2.5, unadjustiert neben adjustiert wie Hilska 3.3 (dort beide Werte in einer Klammer, hier die Richtung im Satz, die Werte in Tab. 3). F17 § 5a und Raster § 3.13 nennen weiter Moran und Negra 2019 als Vorlage, nach Befund § 7 Nr. 7 Vorbild für Objektführung und Kürze (Vormerkung G37 p).',
     'erfüllt · Register U3', 'pruef_2b.txt § 3, § 9'),
    ('§ 7 Nr. 8 (a) Folge des Orientierungszugs', 'Fundstelle', '§ 7 Nr. 8 (a)', 'A1 bis A4',
     'Wie Plan § 3 Task 11 (Fluss mit Ende → Ausgangswerte → Umsetzung mit Tab. H5 → CR-10 und Load → unerwünschte Ereignisse → Messgüte), gegen F17 § 5a (Fluss → Adhärenz → Ausgangswerte → Messgüte). In A4 steht TE post vor den gültigen Versuchen, der Plan nennt „gültige Versuche und TE post“.',
     'bewusst anders gegen F17 § 5a, gedeckt · Register U9, 7b, 9a, Vormerkung G37 p', 'Abgleichbefund § 2.2 Nr. 4, pruef_2b.txt § 16'),
    ('§ 7 Nr. 8 (b) Statistik im Satz, Zahlen in den Objekten', 'Fundstelle', '§ 7 Nr. 8 (b), F17 § 5a Nr. 3', 'A1 S2, A2, A3, A5 S4, S5, A6 S1, S2',
     'Im Gruppenvergleich Richtung, adjustierte Differenz mit KI und p und der Fall, keine Teststatistik. Zahlen im Fließtext nur, wo Raster und Plan sie verlangen: Fluss 31 und 26 (5.1.2), Umsetzung (5.1.6), CR-10 und Load (5.1.7), Ereignisse (5.1.8), Schätzer (5.2.1), verworfene Prüfung mit Bootstrap (5.2.3, R2). Keine Zahl aus Tab. 2, keine Post-Mittel, kein g.',
     'erfüllt · Register Zeile 16, U8, 2a, 10c', 'pruef_2b.txt § 9'),
    ('§ 7 Nr. 9 bestätigte Bauplanaussagen', 'Korpus', '§ 7 Nr. 9', 'A1 S1, alle Sätze',
     'Eröffnung mit Objektverweis (A1 S1, Kern 8 von 10 mit Objektverweis oder Orientierungsbefund), Klammer als häufigste Verweisform ({kl} Sätze mit Klammer am Satzende gegen 4 Objektsätze), Belege 0, Tempus wie Korpus, keine Unterüberschriften (Gliederung v6, Ä16) wie 8 der 11 Bauplanstudien.',
     'erfüllt · Register 1d, 1e', '2a.14, 2a.24, 2a.37'),
    # ---- Prüfpunkte aus Schritt 1 und 2 (a)
    ('Bezugsmenge „neun Spieler“ (Prüfpunkt A3 S3)', 'Fundstelle', 'Registerzeile 2 (F17 § 3: „Jede Zahl im Text nennt ihre Bezugsmenge.“)', 'A3 S3, 6.1 A6 S2',
     '„Zwölf Meldungen von neun Spielern“ nennt die Menge der Spieler nicht. Gemeint sind Spieler der Interventionsgruppe (nur sie hatten das Instrument, A3 S4), offen bleibt, ob von 18 zugeteilten (K-10.4, dann genau die Hälfte) oder von 15 mit mindestens einer Meldung (K-10.9, Berichtsort Anmerkung zu Tab. H2, dann 60 %). 6.1 A6 S2 rechnet mit den 15 („Mehr als die Hälfte der Spieler mit Meldungen“). Als Zählung ist der Satz richtig, für den Anteil in 6.1 fehlt die Menge im Text.',
     'teilweise (Schwere B) · Register 2a', 'pruef_2b.txt § 15, register_pruefung.md 2a'),
    ('Satzenden auf einen Einzelbuchstaben (Prüfpunkt)', 'Fundstelle', 'Startprompt (Regeln), Übergabe § 6, Textvorschlag 5 § 7.2', 'A5 S1, A6 S2',
     'A5 S1 endet auf „… sowie Hedges\' g.“, A6 S2 auf „… bis +0,107 s.“. Die Satzteilung des Messskripts schützt nur Ziffer und Großbuchstabe vor dem Punkt, beide Sätze sind richtig geteilt (29 Sätze), kein Satz endet auf eine Ziffer.',
     'teilweise (Wortlaut der Regel verletzt, ihr Zweck erfüllt, Schwere C) · Startprompt', 'pruef_2b.txt § 15, textstand_pruefung.txt'),
    ('Stilprofil Teil 2, 3, 5 und 7 (Prüfpunkt r1: eine Aussage je Satz)', 'Fundstelle', 'Abgleichbefund § 2.4 r1 · Stilprofil Teil 3 („Eine Aussage je Satz, Ausnahmen in einen eigenen Satz.“, „Bedingungen hängen nicht als Nebensatz an“), Teil 2 und 7', 'A1 S3, A2 S1, S3, S4, A3 S3, A4 S2, A5 S3, S5, A6 S4',
     '{eine} Sätze tragen eine Aussage, Werte derselben Größe in der Klammer zählen nicht als weitere Aussage (A2 S2, A3 S1, S2). Fünf verbinden zwei gleichrangige Hauptsätze mit Komma ohne Konjunktion, der zweite elliptisch (A1 S3, A2 S3, S4, A4 S2, A5 S5). Teil 3 lässt das zu, „aber die Teilung in zwei Sätze ist die Regel“, sein Beispiel hat zwei vollständige Hauptsätze. Drei hängen eine zweite Aussage anders an, die Ausnahme deckt sie nicht: A2 S1 (Median je Spieler nach dem Komma, eine andere Größe), A3 S3 („davon je zwei …“), A5 S3 (zweite Angabe mit „und“ an dasselbe Verb). A6 S4 stellt eine Bedingung als Nebensatz voran und verbindet zwei Hauptsätze mit „und“ („Soweit die Fallzahl eine Inferenz zuließ, …, und keine davon …“), gegen „Bedingungen hängen nicht als Nebensatz an“. Die Registerprüfung nannte A2 S1, A2 S4, A5 S5 und A6 S4. Kein „sodass“, kein „weshalb“, keine Wörter der Verbotsliste, keine Bewertung. Je Zielgröße derselbe Kern „betrug … (KI, p)“, A5 S5 trägt zwei Zielgrößen. Zielwert Teil 2 „Etwa jeder sechste Satz trägt einen Klammerverweis“: {kl} von 29, über dem Zielwert (etwa fünf), alle sind Objektverweise.',
     'teilweise (A6 S4 gegen Teil 3, A2 S1, A3 S3 und A5 S3 außerhalb der Komma-Ausnahme) · Register r1, 1a', 'pruef_2b.txt § 14'),
]
f2 = dict(f)
zeilen = []
MASS = []
for n, r in enumerate(ROWS, 1):
    PRUEF(len(r) == 7 and r[1] in ('Korpus', 'Fundstelle', 'Korpus und Fundstelle'), 'Zeilenform 2b.' + str(n))
    MASS.append(r[1])
    zeilen.append(['2b.' + str(n), r[0], r[1] + ' · ' + r[2], r[3], r[4].format(**f2), r[5], r[6]])
status = Counter(z[5].split(' ')[0] for z in zeilen)
PRUEF(set(status) <= {'erfüllt', 'teilweise', 'bewusst', 'nicht'}, 'Statuswerte')
gegenstandslos = [z[0] for z in zeilen if 'gegenstandslos' in z[5].split(' · ')[0]]
REG = set(re.findall(r'^\| ([0-9]{1,2}[a-z]|[UVO][0-9]+) \|', TXT['register'], re.M)) | {'c' + str(n) for n in range(1, 10)} | {'r' + str(n) for n in range(1, 5)}
reg_verwendet = sorted({m for z in zeilen for m in re.findall(r'\b(\d{1,2}[a-z]|[UVOcr]\d+)\b', z[5].split(' · ', 1)[1] if ' · ' in z[5] else '')})
PRUEF(all(m in REG for m in reg_verwendet), 'Registerkennungen der Statusspalte vorhanden')
# Querverweise auf Zeilennummern im Wortlaut prüfen
for z in zeilen:
    for ref in re.findall(r'2b\.(\d+)', z[4] + z[5]):
        PRUEF(1 <= int(ref) <= len(zeilen), 'Querverweis 2b.' + ref)
ziel = OrderedDict([('2b.8', 'Reihenfolge durchgehend'), ('2b.9', 'K6'), ('2b.13', 'K10'), ('2b.24', 'P10'), ('2b.27', 'Prüfkatalog Nr. 8'),
                    ('2b.28', 'Prüfkatalog Nr. 9'), ('2b.42', '§ 7 Nr. 8 (a)'), ('2b.45', 'Bezugsmenge')])
for nr, kopf in ziel.items():
    z = next(z for z in zeilen if z[0] == nr)
    PRUEF(kopf in z[1], 'Querverweisziel ' + nr + ' ist ' + kopf)
nach_mass = OrderedDict()
for m, z in zip(MASS, zeilen):
    nach_mass.setdefault(m, Counter())[z[5].split(' ')[0]] += 1
aus('17 Teiltabelle 2b (Registerkennungen der Statusspalte, alle vorhanden:', ', '.join(reg_verwendet) + ')')
aus('  ', len(zeilen), 'Zeilen · Status', ' · '.join(k + ' ' + str(v) for k, v in status.most_common()), '· davon gegenstandslos', len(gegenstandslos), '(' + ', '.join(gegenstandslos) + ')')
for m, c in nach_mass.items():
    aus('  Maßstab ' + m + ':', sum(c.values()), 'Zeilen ·', ' · '.join(k + ' ' + str(v) for k, v in c.most_common()))
with open(os.path.join(AUS, 'teiltabelle_2b.csv'), 'w', newline='', encoding='utf-8') as fo:
    w = csv.writer(fo, delimiter=SK, quoting=csv.QUOTE_ALL)
    w.writerow(['Nr.', 'Prüfgegenstand', 'Befundstelle', 'Fundstelle im Text', 'Ergebnis', 'Status', 'Beleg'])
    for z in zeilen:
        w.writerow(z)
with open(os.path.join(AUS, 'teiltabelle_2b.md'), 'w', encoding='utf-8') as fo:
    fo.write('| Nr. | Prüfgegenstand | Befundstelle | Fundstelle im Text | Ergebnis | Status | Beleg |\n')
    fo.write('|---|---|---|---|---|---|---|\n')
    for z in zeilen:
        fo.write('| ' + ' | '.join(c.replace('|', '/') for c in z) + ' |\n')
with open(os.path.join(AUS, 'pruef_2b.txt'), 'w', encoding='utf-8') as fo:
    fo.write('\n'.join(AUSGABE) + '\n')
print('Teiltabelle 2b:', len(zeilen), 'Zeilen ·', dict(status), '· gegenstandslos', len(gegenstandslos), '·', {m: dict(c) for m, c in nach_mass.items()})

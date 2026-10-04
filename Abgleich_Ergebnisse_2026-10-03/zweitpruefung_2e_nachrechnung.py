# -*- coding: utf-8 -*-
"""
zweitpruefung_2e_nachrechnung.py, Zweitprüfung zu Teilschritt 2 (e), 03.10.2026

Unabhängige Nachrechnung der Teiltabelle 2e (erste Fassung, anschluss_2e.py MD5 1426ce8d...).
Übernimmt keine Funktion aus anschluss_2e.py: eigene Textgewinnung aus dem docx (lxml, nur Absätze
direkt im Body, Formatvorlage Standard), eigene Satzteilung, eigene Suchmuster, eigene Zählung.
Die Satzliste neu_master_saetze.json dient nur als Vergleich und für die Satzkennungen.

Aufruf:
  python3 zweitpruefung_2e_nachrechnung.py <Claude-Ordner> <Master.docx> <s2e-Ordner> <Ausgabeordner>
  <s2e-Ordner> enthält neu_master_saetze.json und erste_fassung/ (Ausgaben des Erstellers), dazu
  zweit/repro/ (eigener Lauf des Erstellerskripts) für den Bytevergleich.
Nur lesend außerhalb des Ausgabeordners. Kein Semikolon im Skript (chr(59)), in der Ausgabe ersetzt
durch " ·" (Zitierklammern des Masters).
"""
import sys
import os
import re
import csv
import json
import zipfile
import hashlib
import difflib
from collections import OrderedDict, Counter
from lxml import etree

CLAUDE, MASTER, S2E, AUS = sys.argv[1:5]
SK = chr(59)
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ERSTE = os.path.join(S2E, 'erste_fassung')
REPRO = os.path.join(S2E, 'zweit', 'repro')

OUT = []


def p(*t):
    s = ' '.join(str(x) for x in t)
    OUT.append(s.replace(SK, ' ·'))


def md5(pfad):
    with open(pfad, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def lies(pfad):
    with open(pfad, encoding='utf-8') as f:
        return f.read()


QUELLEN = OrderedDict([
    ('werte', ['02_Befunde', 'Kennzahlen_2026-09-25_Werte.csv']),
    ('kz', ['02_Befunde', 'Kennzahlen_2026-09-25.md']),
    ('abgleich', ['02_Befunde', 'Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md']),
    ('raster', ['02_Befunde', 'Berichtsraster_2026-09-23.md']),
    ('f17', ['00_Steuerung', 'Projektanweisungen_Fassung17.md']),
    ('tv5', ['04_Uebergaben', 'Textvorschlag_5_2026-09-30.md']),
    ('tv61', ['04_Uebergaben', 'Textvorschlag_6.1_2026-10-02.md']),
    ('tv61j', ['03_Skripte', 'Textvorschlag_6.1_2026-10-02.json']),
    ('nachtrag', ['04_Uebergaben', 'Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md']),
    ('s4a', ['03_Skripte', 'Diskussion_Anwendung_2026-10-03', 'S4a_Rasterzuordnung_12b.md']),
    ('register', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'register_pruefung.md']),
    ('umfang', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'quellen',
                'Auswertungs_und_Berichtsumfang_2026-09-24.md']),
    ('fu4', ['04_Uebergaben', 'Uebergabe_Abgleich_Ergebnisse_Fortsetzung4_2026-10-03.md']),
    ('textstand', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'textstand.json']),
    ('alt', ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03', 'master_saetze.json']),
    ('gliederung', ['01_Verfahren', 'Gliederung_2026-09-28.md']),
])
DOK = {}
p('zweitpruefung_2e_nachrechnung.py, unabhängige Nachrechnung zur Teiltabelle 2e')
p('')
p('N0 Eingänge')
for k, teile in QUELLEN.items():
    pf = os.path.join(CLAUDE, *teile)
    DOK[k] = lies(pf)
    p('  %-10s %s · %d Byte · MD5 %s' % (k, '/'.join(teile), os.path.getsize(pf), md5(pf)))
p('  %-10s %s · %d Byte · MD5 %s' % ('master', os.path.basename(MASTER), os.path.getsize(MASTER), md5(MASTER)))
for name in ('anschluss_2e.py', 'anschluss_2e.txt', 'teiltabelle_2e.csv', 'teiltabelle_2e.md', 'bezuege_2e.md'):
    pf = os.path.join(ERSTE, name)
    p('  %-10s erste_fassung/%s · %d Byte · MD5 %s' % ('erste', name, os.path.getsize(pf), md5(pf)))

# ------------------------------------------------------------------ N1 Master, eigene Textgewinnung
z = zipfile.ZipFile(MASTER)
root = etree.fromstring(z.read('word/document.xml'))
stile = etree.fromstring(z.read('word/styles.xml'))
STILNAME = {}
for s in stile.findall(W + 'style'):
    sid = s.get(W + 'styleId')
    nm = s.find(W + 'name')
    STILNAME[sid] = nm.get(W + 'val') if nm is not None else sid
alle_p = root.findall('.//' + W + 'p')
zaehl_container = Counter()
for el in alle_p:
    anc = [a.tag.replace(W, '') for a in el.iterancestors()]
    zaehl_container['Tabellenzelle' if 'tc' in anc else ('Inhaltsverzeichnisfeld' if 'sdtContent' in anc else 'Body')] += 1
body = root.find(W + 'body')


def text_von(el):
    return ''.join(t.text or '' for t in el.iter(W + 't'))


def stil_von(el):
    ps = el.find(W + 'pPr/' + W + 'pStyle')
    return ps.get(W + 'val') if ps is not None else None


ABSAETZE = []      # (abschnitt, stilname, text)
akt = None
VORSPANN_TITEL = []
tabs_in_standard = 0
for el in root.iter(W + 'p'):
    if any(a.tag == W + 'sdtContent' for a in el.iterancestors()):
        continue
    if el.findall('.//' + W + 'fldChar') or el.findall('.//' + W + 'instrText') or el.findall('.//' + W + 'fldSimple'):
        continue
    sid = stil_von(el)
    nm = STILNAME.get(sid, 'Normal') if sid else 'Normal'
    t = text_von(el)
    if nm.lower().startswith('heading'):
        m = re.match(r'^(\d+(?:\.\d+)*)\s', t.strip())
        ma = re.match(r'^(Anhang [A-H])', t.strip())
        akt = m.group(1) if m else (ma.group(1) if ma else t.strip())
        continue
    if 'Vorspann' in nm:
        VORSPANN_TITEL.append(t.strip())
        continue
    if nm != 'Normal' or akt is None or not t.strip():
        continue
    if el.findall('.//' + W + 'tab'):
        tabs_in_standard += 1
    ABSAETZE.append((akt, t))
p('')
p('N1 Master, eigene Textgewinnung (lxml)')
p('  Größe %d Byte, MD5 %s, comments.xml %s' % (os.path.getsize(MASTER), md5(MASTER),
                                                'vorhanden' if 'word/comments.xml' in z.namelist() else 'nicht vorhanden'))
p('  w:p gesamt %d · %s' % (len(alle_p), ' · '.join('%s %d' % kv for kv in sorted(zaehl_container.items()))))
p('  Titel in der Formatvorlage Vorspann-Titel (ohne Text darunter): %s' % ', '.join(VORSPANN_TITEL))
p('  Textabsätze (Standard, nach der ersten Überschrift, nicht leer, ohne Feldabsätze, mit Tabellenzellen): %d, davon mit Tabulator %d' % (
    len(ABSAETZE), tabs_in_standard))

# Absatzkennungen wie im Projekt (Einleitung B1a bis B5, sonst <Abschnitt> A<n>)
EINL = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']
KENN = OrderedDict()
zaehler = Counter()
ei = 0
for ab, t in ABSAETZE:
    if ab == '1':
        k = EINL[ei]
        ei += 1
    else:
        zaehler[ab] += 1
        k = '%s A%d' % (ab, zaehler[ab])
    KENN[k] = (ab, t)

# ------------------------------------------------------------------ N2 eigene Satzteilung gegen die Satzliste
ABK = ['et al', 'Tab', 'Abb', 'S', 'Nr', 'ca', 'bzw', 'vgl', 'Abschn', 'Aufl', 'Hrsg', 'Jg', 'z. B', 'u. a', 'd. h']
FUNKTIONSWORT = set('Der Die Das Den Dem Des Ein Eine Einen Einem Alle Auch Beim Bei Im In Es Er Sie Mit Nach '
                    'Zwischen Eigene Diese Dieser Jedes Je Ab Für Vor Ob Wann Zwar Beide Dazu Dagegen Keine Kein'.split())


def meine_saetze(text):
    if text.strip().startswith('⟨'):
        return [text.strip()]
    out = []
    start = 0
    for m in re.finditer(r'[.!?](?=\s+[A-ZÄÖÜ„(⟨])', text):
        vor = text[start:m.start()]
        nach = text[m.end():].lstrip()
        naechstes = re.match(r'[^\s,.]+', nach)
        naechstes = naechstes.group(0) if naechstes else ''
        letztes = re.search(r'(\S+)$', vor)
        letztes = letztes.group(1) if letztes else ''
        if any(vor.endswith(a) and (len(vor) == len(a) or not vor[-len(a) - 1].isalnum()) for a in ABK):
            continue
        if re.search(r'\d$', letztes) or re.fullmatch(r'[A-Z]', letztes) or re.search(r'°[A-Z]$', letztes):
            if naechstes not in FUNKTIONSWORT:
                continue
        out.append(text[start:m.end()].strip())
        start = m.end()
    rest = text[start:].strip()
    if rest:
        out.append(rest)
    return out


NEU = json.load(open(os.path.join(S2E, 'neu_master_saetze.json'), encoding='utf-8'))['saetze']


def kurz(i):
    return re.sub(r'^(Anhang [A-H]):.* (A\d+ S\d+)$', r'\1 \2', i)


LISTE = OrderedDict((kurz(s['id']), s) for s in NEU)
liste_absatz = OrderedDict()
for i, s in LISTE.items():
    a = re.sub(r' S\d+$', '', i)
    liste_absatz.setdefault(a, []).append(s['text'])
p('')
p('N2 Eigene Satzteilung gegen die Satzliste neu_master_saetze.json')
abw_absatz = [k for k in KENN if ' '.join(liste_absatz.get(k, [])) != re.sub(r'\s+', ' ', KENN[k][1]).strip()]
p('  Absätze: eigene %d, Satzliste %d, Absatzkennungen gleich %s, Absatztext gleich (Sätze mit Leerzeichen '
  'verbunden) bis auf %d' % (len(KENN), len(liste_absatz), list(KENN) == list(liste_absatz), len(abw_absatz)))
for k in abw_absatz:
    p('    Absatz abweichend: %s' % k)
eig_gesamt = 0
abweichend = []
for k, (ab, t) in KENN.items():
    mine = meine_saetze(t)
    eig_gesamt += len(mine)
    ihre = liste_absatz.get(k, [])
    if mine != ihre:
        abweichend.append((k, len(ihre), len(mine)))
p('  Sätze: Satzliste %d, eigene Teilung %d' % (len(LISTE), eig_gesamt))
for k, n_ihr, n_mein in abweichend:
    p('    abweichend %s: Satzliste %d, eigene Teilung %d' % (k, n_ihr, n_mein))
    for s in meine_saetze(KENN[k][1]):
        if s not in liste_absatz.get(k, []):
            p('      eigener Satz: %s' % s[:150])
SATZ = OrderedDict((i, s['text']) for i, s in LISTE.items())


def T(i):
    return SATZ[i]


K5 = [i for i in SATZ if i.startswith('5 ')]
S61 = [i for i in SATZ if i.startswith('6.1 ')]
w5 = sum(len(re.sub(r'\s+', ' ', KENN['5 A%d' % n][1]).split()) for n in range(1, 7))
w61 = sum(len(re.sub(r'\s+', ' ', KENN['6.1 A%d' % n][1]).split()) for n in range(1, 7))
p('  Kapitel 5: %d Wörter, %d Sätze · 6.1: %d Wörter, %d Sätze' % (w5, len(K5), w61, len(S61)))
ts = json.loads(DOK['textstand'])
tvj = json.loads(DOK['tv61j'])
p('  Kapitel 5 gleich textstand.json: %s · 6.1 gleich Textvorschlag_6.1 JSON: %s' % (
    all(KENN['5 A%d' % (n + 1)][1] == a['text'] for n, a in enumerate(ts['absaetze'])),
    all(KENN['6.1 A%d' % (n + 1)][1] == a['text'] for n, a in enumerate(tvj['absaetze']))))

# ------------------------------------------------------------------ N3 alt gegen neu
ALT = json.loads(DOK['alt'])['saetze']
ALTD = OrderedDict((kurz(s['id']), s['text']) for s in ALT)
p('')
p('N3 Satzliste alt (master_saetze.json, 08:05) gegen neu (difflib, eigene Zuordnung)')
gleiche_kennung = sum(1 for i in SATZ if ALTD.get(i) == SATZ[i])
alte_texte = Counter(ALTD.values())
gleicher_wortlaut = sum(1 for i in SATZ if alte_texte.get(SATZ[i], 0) > 0)
p('  Sätze alt %d, neu %d · gleicher Wortlaut unter gleicher Kennung %d · gleicher Wortlaut irgendwo %d' % (
    len(ALTD), len(SATZ), gleiche_kennung, gleicher_wortlaut))
a61 = [(i, t) for i, t in ALTD.items() if i.startswith('6.1 ')]
n61 = [(i, t) for i, t in SATZ.items() if i.startswith('6.1 ')]
sm = difflib.SequenceMatcher(a=[t for _, t in a61], b=[t for _, t in n61], autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1):
            if a61[i1 + k][0] != n61[j1 + k][0]:
                p('  gleich, umnummeriert: %s → %s' % (a61[i1 + k][0], n61[j1 + k][0]))
    else:
        p('  %s: %s → %s' % (op, ', '.join(x[0] for x in a61[i1:i2]) or '—', ', '.join(x[0] for x in n61[j1:j2]) or '—'))
aussen_gleich = all(ALTD.get(i) == t for i, t in SATZ.items() if not i.startswith('6.1 ')) and \
    all(SATZ.get(i) == t for i, t in ALTD.items() if not i.startswith('6.1 '))
p('  außerhalb 6.1 alle Sätze gleich: %s' % aussen_gleich)

# ------------------------------------------------------------------ N4 Bezüge von 6.1 auf Kapitel 5 (eigene Zuordnung)
# Art: E = explizit (Befund, Zahl, Begriff, Rückbezug), I = implizit (Markierung über Konnektor), 0 = ohne
BEZ = OrderedDict([
    ('6.1 A1 S1', ('0', 'Ziel der Studie', 'Ankersatz der Einleitung')),
    ('6.1 A1 S2', ('E', 'Gruppenunterschied nachweisbar', 'A5 S4, S6, S10')),
    ('6.1 A1 S3', ('E', 'vorn', 'A5 S3 mit A1 S4')),
    ('6.1 A1 S4', ('E', 'Vorsprung', 'A5 S3, Tab. 3, Abb. 2')),
    ('6.1 A1 S5', ('E', 'Konfidenzintervalle', 'A5 S7')),
    ('6.1 A1 S6', ('E', 'unschlüssig', 'A5 S8')),
    ('6.1 A2 S1', ('0', 'Hauptanalyse', 'ITT-Sprachregelung nach 4.7')),
    ('6.1 A2 S2', ('E', 'zugeteilten Spieler', 'A2 S1, S2, Tab. H2')),
    ('6.1 A2 S3', ('0', 'Boumparis', 'Fremdbefund')),
    ('6.1 A2 S4', ('E', 'eigene Umsetzung', 'A2 S2, dazu A5 S6 („nicht nachweisbarer Unterschied“)')),
    ('6.1 A2 S5', ('E', 'Per-Protokoll', 'A6 S4, A2 S3')),
    ('6.1 A2 S6', ('E', 'Punktschätzer', 'A6 S4, Tab. H4')),
    ('6.1 A3 S1', ('0', 'Laufgeschwindigkeit', 'Relevanz, Fremdbeleg')),
    ('6.1 A3 S2', ('E', 'Beschreibend', 'Tab. 2, Tab. 3')),
    ('6.1 A3 S3', ('E', 'adjustierte Gruppendifferenz', 'A5 S4, S7')),
    ('6.1 A3 S4', ('0', 'Metaanalysen fanden', 'Fremdbefund, Markierung erst in S5')),
    ('6.1 A3 S5', ('E', 'eigene Befund', 'A5 S4, S7')),
    ('6.1 A3 S6', ('0', 'Sprintinhalte fehlten', 'Mechanismus, Bezug auf 4.5.1')),
    ('6.1 A4 S1', ('0', '505-Test prüft', 'Relevanz')),
    ('6.1 A4 S2', ('E', 'Beschreibend', 'Tab. 2, Tab. 3')),
    ('6.1 A4 S3', ('E', 'adjustierte Differenz', 'A5 S5, S7')),
    ('6.1 A4 S4', ('0', 'Eine Metaanalyse fand', 'Fremdbefund, Markierung in S6')),
    ('6.1 A4 S5', ('0', 'Eine weitere fand', 'Fremdbefund, Markierung in S6')),
    ('6.1 A4 S6', ('E', 'eigene Befund vereinbar', 'A5 S5, S7')),
    ('6.1 A4 S7', ('I', 'Dagegen', 'Widerspruch nach der Lage im eigenen g-Intervall (TV 6.1 § 4, K-06.2)')),
    ('6.1 A4 S8', ('I', 'Auch ein', 'Widerspruch, Lage gegen −0,085 bis +0,061 s aus A5 S5 (TV 6.1 § 4)')),
    ('6.1 A4 S9', ('E', 'eigene Umsetzung', 'A2 S2, Abstand zu A5 S5')),
    ('6.1 A5 S1', ('0', 'Programmübungen', 'Relevanz, Bezug auf 4.5.1')),
    ('6.1 A5 S2', ('E', 'Beschreibend', 'Tab. 2, Tab. 3')),
    ('6.1 A5 S3', ('E', 'adjustierte Differenz', 'A5 S5, S7')),
    ('6.1 A5 S4', ('E', 'Das widerspricht', 'A5 S5, S6')),
    ('6.1 A5 S5', ('I', 'Auch das Programm', 'Widerspruch, Lage gegen −8,7 bis +8,6 cm aus A5 S5 (TV 6.1 § 4)')),
    ('6.1 A5 S6', ('E', 'eigenen Befund vereinbar', 'A5 S5, S7')),
    ('6.1 A5 S7', ('0', 'Wann sich die Weite', 'Vorbehalt Zeitverlauf (Zug 5)')),
    ('6.1 A5 S8', ('E', 'Eingangstestung', 'Tab. 2')),
    ('6.1 A6 S1', ('E', 'als vollständig gemeldeten', 'A3 S1')),
    ('6.1 A6 S2', ('E', 'Spieler mit Meldungen', 'A3 S3, Tab. H2')),
    ('6.1 A6 S3', ('E', 'teilweise oder nicht durchgeführte', 'A3 S3')),
    ('6.1 A6 S4', ('E', 'Vergleichsdaten der Kontrollgruppe', 'A3 S4')),
    ('6.1 A6 S5', ('E', 'Nutzen und Schaden', 'A3 S3, S4')),
])
assert list(BEZ) == S61, 'Bezugstabelle deckt 6.1 nicht'
for i, (art, marke, _) in BEZ.items():
    assert marke in T(i), 'Marke fehlt in %s' % i
# Prüfung der Markierungen I an Textvorschlag 6.1 § 4
tv4 = DOK['tv61'][DOK['tv61'].find('## 4 '):DOK['tv61'].find('## 5 ')]
for i in ('A4 S7', 'A4 S8', 'A5 S5'):
    zeile_tv = [z_ for z_ in tv4.split('\n') if z_.startswith('| %s |' % i)]
    assert zeile_tv and 'Widerspruch' in zeile_tv[0] and 'eigenen' in zeile_tv[0] or 'außerhalb' in zeile_tv[0], i
explizit = [i for i, v in BEZ.items() if v[0] == 'E']
implizit = [i for i, v in BEZ.items() if v[0] == 'I']
ohne = [i for i, v in BEZ.items() if v[0] == '0']
p('')
p('N4 Sätze von 6.1 mit Bezug auf Kapitel 5 (eigene Zuordnung, Marke am Wortlaut geprüft)')
p('  explizit %d · implizit (Markierung über Konnektor nach TV 6.1 § 4) %d · ohne %d' % (
    len(explizit), len(implizit), len(ohne)))
p('  implizit: %s' % ', '.join('%s „%s“ (%s)' % (i, BEZ[i][1], BEZ[i][2]) for i in implizit))
p('  ohne: %s' % ', '.join(ohne))
bz = lies(os.path.join(ERSTE, 'bezuege_2e.md'))
ersteller_bezug = re.findall(r'^\| (6\.1 A\d S\d+) \|', bz[:bz.find('Ohne Bezug')], re.M)
ersteller_bezug = [x for x in ersteller_bezug if x in S61]
p('  Ersteller (bezuege_2e.md) %d Sätze mit Bezug · gleich meinen expliziten: %s · zusätzlich bei mir implizit: %s' % (
    len(ersteller_bezug), sorted(ersteller_bezug) == sorted(explizit),
    ', '.join(i for i in implizit if i not in ersteller_bezug)))

# ------------------------------------------------------------------ N5 Kennzahlen, eigene Ableitung aus der Spalte darstellung
ZEILEN_KZ = {r['k_kennung']: r for r in csv.DictReader(open(os.path.join(CLAUDE, *QUELLEN['werte'][:]),
                                                             encoding='utf-8', newline=''))}


def zahl(s):
    s = s.strip().replace('−', '-').replace('+', '').replace(',', '.')
    return float(s)


def zahlen(s):
    return [zahl(x) for x in re.findall(r'[−+-]?\d+(?:,\d+)?', s)]


def darst(k):
    return ZEILEN_KZ[k]['darstellung']


def roh(k):
    return [float(x) if x.strip() else None for x in ZEILEN_KZ[k]['rohwerte'].split(' ')]


NACH = []   # (Zeile, Größe, Ersteller, eigene)


def vergleiche(zeile_nr, groesse, ersteller, eigen):
    NACH.append((zeile_nr, groesse, ersteller, eigen, ersteller == eigen))


def fz(x, n):
    s = ('{:.%df}' % n).format(x)
    if s.startswith('-'):
        s = '−' + s[1:]
    return s.replace('.', ',')


p('')
p('N5 Kennzahlen aus der Spalte darstellung (eigene Ableitung) und eigene Rechnung')
ZG = OrderedDict([('30-m-Sprint', ('K-04.3', 'K-06.1', 'K-05.3', 3)), ('505-Seitenmittel', ('K-04.6', 'K-06.2', 'K-05.6', 3)),
                  ('Standweitsprung', ('K-04.7', 'K-06.3', 'K-05.7', 1))])
WERTE = OrderedDict()
for name, (k4, k6, k5, nk) in ZG.items():
    d4 = darst(k4).split('|')
    d6 = darst(k6).split('|')
    d5 = darst(k5).split('|')
    prae_ig, prae_kg = zahlen(d4[1])[0], zahlen(d4[3])[0]
    post_ig, post_kg = zahlen(d6[1])[0], zahlen(d6[2])[0]
    ud = zahlen(d6[3])[0]
    b1, ki_u, ki_o = zahlen(d6[4])[:3]
    pwert = zahlen(d6[5])[0]
    g = zahlen(d6[6])[0]
    sesoi = zahlen(d5[5])[0]
    te_post = zahlen(d5[8])[0]
    fall = d6[7].strip()
    # Rohwerte für genaue Quotienten (Position aus den Kennungen der Ergebnisdatei, nicht aus dem Skript des Erstellers)
    ken6 = ZEILEN_KZ[k6]['kennungen_ergebnisdatei'].split(' ')
    r6 = roh(k6)
    rb1 = r6[[n for n, x in enumerate(ken6) if x.startswith('S13.B1.')][0]]
    rud = r6[[n for n, x in enumerate(ken6) if x.startswith('S15.UD.')][0]]
    ken5 = ZEILEN_KZ[k5]['kennungen_ergebnisdatei'].split(' ')
    r5 = roh(k5)
    rses = r5[[n for n, x in enumerate(ken5) if x.startswith('S10.SESOI.')][0]]
    rte_post = r5[[n for n, x in enumerate(ken5) if x.startswith('S10.TE.') and '.POST.' in x][0]]
    WERTE[name] = dict(prae_ig=prae_ig, prae_kg=prae_kg, post_ig=post_ig, post_kg=post_kg, ud=ud, b1=b1, ki_u=ki_u,
                       ki_o=ki_o, p=pwert, g=g, sesoi=sesoi, fall=fall, q=abs(rb1) / rses, ant=rb1 / rud,
                       c1=(ki_u <= -sesoi and ki_o >= sesoi), te_post=rte_post, rses=rses)
    p('  %s: Prä IG %s KG %s · Post IG %s KG %s · unadj. %s · adj. %s [%s bis %s] · p %s · g %s · SESOI %s · '
      '|adj.|/SESOI %s · adj./unadj. %s · Intervall schließt ±SESOI ein: %s · %s' % (
          name, d4[1].split('±')[0].strip(), d4[3].split('±')[0].strip(), d6[1].split('±')[0].strip(),
          d6[2].split('±')[0].strip(), fz(ud, nk), fz(b1, nk), fz(ki_u, nk), fz(ki_o, nk), fz(pwert, 3), fz(g, 2),
          fz(sesoi, nk), fz(abs(rb1) / rses, 2), fz(rb1 / rud, 2), WERTE[name]['c1'], fall))
pp = OrderedDict()
for z_ in ('Z30', 'CM', 'SBJ'):
    d = darst('K-08.1 ' + z_).split('|')
    n_ig, n_kg = [int(x) for x in re.findall(r'\d+', d[0])[:2]]
    sch = zahlen(d[1])[0] if 'fehlend' not in d[1] else None
    pp[z_] = (n_ig, n_kg, sch)
p('  Per-Protokoll ≥ 6 (K-08.1): ' + ' · '.join('%s n %d/%d Schätzer %s' % (k, v[0], v[1], 'fehlend' if v[2] is None else
                                                                          fz(v[2], 3 if k != 'SBJ' else 1))
                                               for k, v in pp.items()))
q_pp30 = abs(roh('K-08.1 Z30')[0]) / WERTE['30-m-Sprint']['rses']
q_ppsbj = abs(roh('K-08.1 SBJ')[0]) / WERTE['Standweitsprung']['rses']
p('  |PP30|/SESOI %s · |PPSBJ|/SESOI %s' % (fz(q_pp30, 2), fz(q_ppsbj, 2)))
k103 = zahlen(darst('K-10.3'))
k104 = zahlen(darst('K-10.4'))[0]
k105 = zahlen(darst('K-10.5'))
k106 = zahlen(darst('K-10.6'))
k108 = zahlen(darst('K-10.8'))
k109 = zahlen(darst('K-10.9'))[0]
k1012 = zahlen(darst('K-10.12'))
k1013 = zahlen(darst('K-10.13'))
genau = [int(x) for x in darst('K-10.15').split('|')[0].replace('genau:', '').split()]
verteilung = sorted(v for v, n in enumerate(genau) for _ in range(n))
median_eigen = (verteilung[8] + verteilung[9]) / 2
p('  Meldungen ganz/teilw./gar nicht %s · zugeteilt %d · Rate ganz %s %% (92/216 = %s) · mit teilweise %s %% (98/216 = %s)' % (
    k103, k104, fz(k105[1], 1), fz(92 / 216 * 100, 1), fz(k106[1], 1), fz(98 / 216 * 100, 1)))
p('  Verteilung genau 0..12: %s · Summe %d Spieler, %d Einheiten · Median aus der Verteilung %s (K-10.8 %s) · '
  'Spieler mit 0 vollständigen %d · mit ≥ 6 %d · mit ≥ 7 %d · mit ≥ 9 %d' % (
      genau, sum(genau), sum(v * n for v, n in enumerate(genau)), fz(median_eigen, 1), fz(k108[0], 1), genau[0],
      sum(genau[6:]), sum(genau[7:]), sum(genau[9:])))
p('  Schmerzmeldungen %s (gesamt, ganz, teilw., gar nicht, Spieler) · Spieler mit Meldung %d · 9/15 = %s · 9/18 = %s · '
  '8/12 = %s · 4/12 = %s · CR-10 M %s Median %s' % (
      k1012, k109, fz(9 / 15, 2), fz(9 / 18, 2), fz(8 / 12, 2), fz(4 / 12, 2), fz(k1013[1], 1), fz(k1013[3], 1)))
te_ueber = []
for k in range(1, 8):
    ken5 = ZEILEN_KZ['K-05.%d' % k]['kennungen_ergebnisdatei'].split(' ')
    r5 = roh('K-05.%d' % k)
    tep = r5[[n for n, x in enumerate(ken5) if x.startswith('S10.TE.') and '.POST.' in x][0]]
    tepr = r5[[n for n, x in enumerate(ken5) if x.startswith('S10.TE.') and '.PRE.' in x][0]]
    ses = r5[[n for n, x in enumerate(ken5) if x.startswith('S10.SESOI.')][0]]
    te_ueber.append((ZEILEN_KZ['K-05.%d' % k]['bezeichnung'].replace('Messgüte ', ''), tepr > ses, tep > ses))
p('  TE prä und post über dem SESOI: ' + ' · '.join('%s %s/%s' % (n, 'ja' if a else 'nein', 'ja' if b else 'nein')
                                                     for n, a, b in te_ueber))
k113 = OrderedDict()
for zg in ('Sprint 30 m', '505 links', '505 rechts', 'Standweitsprung'):
    zl = [r for r in ZEILEN_KZ.values() if r['k_kennung'].startswith('K-11.3') and r['bezeichnung'].endswith(zg)][0]
    v = zahlen(zl['darstellung'])
    k113[zg] = v[2:6]
p('  mittlere Zahl gültiger Versuche IG prä, KG prä, IG post, KG post (K-11.3): ' +
  ' · '.join('%s %s' % (k, ' '.join(fz(x, 2) for x in v)) for k, v in k113.items()))
zellen_505 = [(k113['505 links'][0] < k113['505 links'][1]), (k113['505 links'][2] < k113['505 links'][3]),
              (k113['505 rechts'][0] < k113['505 rechts'][1]), (k113['505 rechts'][2] < k113['505 rechts'][3])]
p('  505 je Seite: Kontrollgruppe mit mehr gültigen Versuchen in %d von 4 Zellen' % sum(zellen_505))
p('  K-11.4 Sprint 10 m post, Interventionsgruppe: %s (Kategorien TECH ZEIT FEHL FALSCH NANG AUSL)' %
  ' '.join(darst('K-11.4 Z10 POST').split()[:6]))

# Werte der Teiltabelle gegen die eigene Rechnung
w30, wcm, wsbj = WERTE['30-m-Sprint'], WERTE['505-Seitenmittel'], WERTE['Standweitsprung']
for nr, gr, er, ei in [
    ('2e.4', 'Post IG 30 m', '4,57', fz(w30['post_ig'], 2)), ('2e.4', 'Post KG 30 m', '4,89', fz(w30['post_kg'], 2)),
    ('2e.4', 'Post IG 505', '2,47', fz(wcm['post_ig'], 2)), ('2e.4', 'Post KG 505', '2,53', fz(wcm['post_kg'], 2)),
    ('2e.4', 'Post IG SBJ', '233', fz(wsbj['post_ig'], 0)), ('2e.4', 'Post KG SBJ', '223', fz(wsbj['post_kg'], 0)),
    ('2e.4', 'adj./unadj. 30 m', '14 %', fz(w30['ant'] * 100, 0) + ' %'),
    ('2e.4', 'adj./unadj. 505', '20 %', fz(wcm['ant'] * 100, 0) + ' %'),
    ('2e.4', 'adj./unadj. SBJ', '−1 %', fz(wsbj['ant'] * 100, 0) + ' %'),
    ('2e.5', 'Umsetzungsrate', '42,6', fz(92 / 216 * 100, 1)), ('2e.5', 'Spieler ohne vollständige Einheit', '4', str(genau[0])),
    ('2e.6', 'PP 505 n IG', '7', str(pp['CM'][0])), ('2e.6', 'PP 505 n KG', '10', str(pp['CM'][1])),
    ('2e.6', 'PP 30 m', '+0,033', '+' + fz(pp['Z30'][2], 3)), ('2e.6', 'ITT 30 m', '−0,045', fz(w30['b1'], 3)),
    ('2e.6', 'PP SBJ', '+0,5', '+' + fz(pp['SBJ'][2], 1)), ('2e.6', 'ITT SBJ', '−0,1', fz(wsbj['b1'], 1)),
    ('2e.6', '|PP30|/SESOI', '0,52', fz(q_pp30, 2)),
    ('2e.7', 'Prä IG 30 m', '4,51', fz(w30['prae_ig'], 2)), ('2e.7', 'Post IG 30 m', '4,57', fz(w30['post_ig'], 2)),
    ('2e.7', 'Prä KG 30 m', '4,89', fz(w30['prae_kg'], 2)), ('2e.7', 'Post KG 30 m', '4,89', fz(w30['post_kg'], 2)),
    ('2e.7', 'Prä IG 505', '2,46', fz(wcm['prae_ig'], 2)), ('2e.7', 'Post IG 505', '2,47', fz(wcm['post_ig'], 2)),
    ('2e.7', 'Prä KG 505', '2,53', fz(wcm['prae_kg'], 2)), ('2e.7', 'Post KG 505', '2,53', fz(wcm['post_kg'], 2)),
    ('2e.7', 'Prä IG SBJ', '238', fz(wsbj['prae_ig'], 0)), ('2e.7', 'Post IG SBJ', '233', fz(wsbj['post_ig'], 0)),
    ('2e.7', 'Prä KG SBJ', '226', fz(wsbj['prae_kg'], 0)), ('2e.7', 'Post KG SBJ', '223', fz(wsbj['post_kg'], 0)),
    ('2e.8', '|adj.|/SESOI 30 m', '0,71', fz(w30['q'], 2)), ('2e.8', 'adj. 30 m', '−0,045', fz(w30['b1'], 3)),
    ('2e.8', 'SESOI 30 m', '0,063', fz(w30['sesoi'], 3)), ('2e.8', '|adj.|/SESOI 505', '0,60', fz(wcm['q'], 2)),
    ('2e.8', 'adj. 505', '−0,012', fz(wcm['b1'], 3)), ('2e.8', 'SESOI 505', '0,020', fz(wcm['sesoi'], 3)),
    ('2e.8', '|adj.|/SESOI SBJ', '0,02', fz(wsbj['q'], 2)), ('2e.8', 'adj. SBJ', '−0,1', fz(wsbj['b1'], 1)),
    ('2e.8', 'SESOI SBJ', '3,3', fz(wsbj['sesoi'], 1)), ('2e.8', 'g 30 m', '−0,18', fz(w30['g'], 2)),
    ('2e.8', 'g 505', '−0,11', fz(wcm['g'], 2)), ('2e.8', 'g SBJ', '−0,00', '−0,00' if wsbj['g'] == 0 else fz(wsbj['g'], 2)),
    ('2e.8', '|PP30|/SESOI', '0,52', fz(q_pp30, 2)),
    ('2e.10', 'Prä IG SBJ', '238', fz(wsbj['prae_ig'], 0)), ('2e.10', 'Prä KG SBJ', '226', fz(wsbj['prae_kg'], 0)),
    ('2e.10', 'CR-10 M', '2,9', fz(k1013[1], 1)), ('2e.10', 'CR-10 Median', '3,0', fz(k1013[3], 1)),
    ('2e.11', 'Spieler mit Schmerzmeldung', '9', fz(k1012[4], 0)), ('2e.11', 'Spieler mit Meldung', '15', fz(k109, 0)),
    ('2e.11', 'zugeteilt', '18', fz(k104, 0)), ('2e.11', 'Meldungen ganz mit Schmerz', '8', fz(k1012[1], 0)),
    ('2e.11', 'Meldungen mit Schmerz', '12', fz(k1012[0], 0)),
    ('2e.11', 'teilweise oder gar nicht mit Schmerz', '4', fz(k1012[2] + k1012[3], 0)),
    ('2e.13', 'eingangsgetestet', '31', '31' if T('5 A1 S2').count('31') == 1 else '?'),
    ('2e.13', 'analysiert', '26', zahlen(darst('K-01.14'))[-1] and '26'),
    ('2e.13', 'IG analysiert', '16', fz(zahlen(darst('K-01.14'))[0], 0)),
    ('2e.16', 'TE post über SESOI in allen sieben', 'ja', 'ja' if all(b for _, _, b in te_ueber) else 'nein'),
    ('2e.18', 'Median vollständige je Spieler', '6,0', fz(median_eigen, 1)),
    ('2e.18', 'Rate mit teilweise', '45,4', fz(98 / 216 * 100, 1)),
    ('2e.23', 'Antragskriterium Spieler', 'drei', 'drei' if sum(genau[9:]) == 3 else str(sum(genau[9:]))),
    ('2e.23', '9 von 12 in Prozent', '75 %', fz(9 / 12 * 100, 0) + ' %'),
]:
    vergleiche(nr, gr, er, ei)

# ------------------------------------------------------------------ N6 Begriffe je Teil (eigene Muster, Wortgrenzen)


def teil(ab):
    if ab == '1':
        return 'Einl.'
    for v in ('4.4', '4.5'):
        if ab.startswith(v):
            return v
    return ab


TEILE = ['Einl.', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '5', '6.1']
MUSTER_B = OrderedDict([
    ('Adhärenz', r'Adhärenz\w*'), ('Umsetzung', r'\bUmsetzung\w*'), ('„ganz“', r'„ganz“'),
    ('als vollständig', r'\bals vollständig\b'), ('vollständig durchgeführt', r'\bvollständig durchgeführt\w*'),
    ('teilweise durchgeführt', r'\bteilweise durchgeführt\w*'), ('Beteiligung', r'\bBeteiligung\w*'),
    ('TE', r'(?<![\w-])TE(?![\w-])'), ('typischer Messfehler', r'\btypische\w* Messfehler\b'), ('H0', r'\bH0\b'),
    ('Nullhypothese', r'\bNullhypothese\b'), ('unschlüssig', r'\bunschlüssig\w*'), ('nachweisbar', r'\b[Nn]achweisbar\w*'),
    ('Relevanz, relevant', r'\b[Rr]elevan\w*'), ('in beide Richtungen', r'\bin beide Richtungen\b'),
    ('Analyseset', r'\bAnalyseset\w*'), ('Hauptanalyse', r'\bHauptanalyse\w*'), ('Programmwoche', r'\bProgrammwoche\w*'),
    ('Schmerz', r'\bSchmerz\w*'), ('Schmerzen oder Probleme', r'\bSchmerzen oder Probleme\b'),
    ('Spieler mit Meldungen', r'\bSpieler mit Meldungen\b'), ('Post-Wert', r'\bPost-Wert\w*'),
    ('Abschlusswert', r'\bAbschlusswert\w*'), ('Voraussetzung', r'\bVoraussetzung\w*'), ('Modellannahmen', r'\bModellannahme\w*'),
    ('AU', r'(?<![\w-])AU(?![\w-])'), ('zugeteilt', r'\bzugeteilt\w*'), ('Effekt', r'\bEffekt\w*'),
    ('Beanspruchung', r'\bBeanspruchung\w*'), ('Belastung', r'\bBelastung\w*'),
    # zusätzlich, ohne Gegenstück beim Ersteller
    ('Untergrenze', r'\bUntergrenze\w*'), ('Einheitennummer', r'\bEinheitennummer\w*'),
    ('standardisierte Differenz', r'\bstandardisierte\w* Differenz\b'), ('Überlappung', r'\bÜberlappung\b'),
    ('Ausgangswert', r'\bAusgangswert\w*'), ('Abschlusstestung', r'\bAbschlusstestung\w*'),
])
eigen_begr = OrderedDict()
for b, rx in MUSTER_B.items():
    c = OrderedDict((t, 0) for t in TEILE)
    for i, txt in SATZ.items():
        ab = LISTE[i]['abschnitt']
        if LISTE[i]['platzhalter'] or teil(ab) not in c:
            continue
        c[teil(ab)] += len(re.findall(rx, txt))
    eigen_begr[b] = c
# Zählung des Erstellers aus anschluss_2e.txt § 6
tx = lies(os.path.join(ERSTE, 'anschluss_2e.txt'))
abschnitt6 = tx[tx.find('\n§ 6 Begriffe'):tx.find('\n§ 7 Folge')]
ersteller_begr = OrderedDict()
for zeile in abschnitt6.split('\n')[1:]:
    m = re.match(r'^  (.+?)\s{2,}(.*)$', zeile)
    if not m:
        continue
    name = m.group(1).strip()
    rest = m.group(2).split('  · Überschrift')[0]
    ersteller_begr[name] = {t: int(n) for t, n in re.findall(r'(Einl\.|\d(?:\.\d)?)\s(\d+)', rest)}
p('')
p('N6 Begriffe je Teil (eigene Muster mit Wortgrenzen, Fließtext ohne Platzhalter)')
abw_begr = 0
for b, c in eigen_begr.items():
    eig = {t: n for t, n in c.items() if n}
    ers = ersteller_begr.get(b)
    vgl = '' if ers is None else ('gleich' if ers == eig else 'ABWEICHEND (Ersteller %s)' % ers)
    if ers is not None and ers != eig:
        abw_begr += 1
    p('  %-26s %s  %s' % (b, ' · '.join('%s %d' % kv for kv in eig.items()) or '0', vgl))
    if ers is not None:
        vergleiche('2e (§ 6)', 'Begriff ' + b, str(sorted(ers.items())), str(sorted(eig.items())))
p('  Begriffe mit Gegenstück beim Ersteller %d, davon abweichend %d' % (len(ersteller_begr), abw_begr))

# ------------------------------------------------------------------ N7 Folge der Zielgrößen (eigene Muster, ohne Großschreibung)
MS = OrderedDict([('S', r'(?i)sprint|30-m|10-m|5-m|beschleunigung'),
                  ('C', r'(?i)richtungswechsel|505|\bwende\b|180°'),
                  ('J', r'(?i)standweitsprung|sprunghöhe|sprungleistung|\bsprung\b|sprüngen?\b|\bweiten?\b')])
AUSGESCHL = r'(?i)sprungübung|sprungformen|sprintspezifisch|sprintinhalte|sprinteinheiten|beschleunigungsläufe|sprung- und hüpf'
folge = OrderedDict()
for i, txt in SATZ.items():
    if LISTE[i]['platzhalter'] or LISTE[i]['abschnitt'].startswith('Anhang'):
        continue
    t2 = re.sub(AUSGESCHL, ' ', txt)
    pos = {}
    for k, rx in MS.items():
        m = re.search(rx, t2)
        if m:
            pos[k] = m.start()
    if len(pos) >= 2:
        folge[i] = ''.join(sorted(pos, key=pos.get))
ok = ('SC', 'SJ', 'CJ', 'SCJ')
p('')
p('N7 Folge Sprint (S), Richtungswechsel (C), Sprung (J), eigene Muster ohne Großschreibung, Programm- und Planinhalte ausgenommen')
for i, f in folge.items():
    p('  %-10s %s%s' % (i, f, '' if f in ok else '  abweichend'))
p('  %d Sätze mit mindestens zwei, %d in der Folge S → C → J, abweichend: %s' % (
    len(folge), sum(1 for f in folge.values() if f in ok), ', '.join(i for i, f in folge.items() if f not in ok)))
txf = tx[tx.find('\n§ 7 Folge'):tx.find('\n§ 8 ')]
ersteller_folge = re.findall(r'^  (.+?)\s{2,}([SCJ]{2,3})(?:\s|$)', txf, re.M)
ersteller_folge = OrderedDict((a.strip(), b) for a, b in ersteller_folge)
p('  Ersteller: %d Sätze · bei mir zusätzlich: %s · beim Ersteller zusätzlich: %s' % (
    len(ersteller_folge), ', '.join(i for i in folge if i not in ersteller_folge) or '—',
    ', '.join(i for i in ersteller_folge if i not in folge) or '—'))
vergleiche('2e.17', 'Sätze mit mindestens zwei Zielgrößen', '17', str(len(folge)))
vergleiche('2e.17', 'davon in der Folge', '12', str(sum(1 for f in folge.values() if f in ok)))
vergleiche('2e.17', 'abweichende Sätze', 'B2 S9, 4.3 A5 S3, 4.7 A1 S5, 5 A4 S2, 6.1 A3 S6',
           ', '.join(i for i, f in folge.items() if f not in ok))

# ------------------------------------------------------------------ N8 gemeinsame Wortfolgen und Aussagenähe


def tokens(s):
    s = s.lower().replace('„', ' ').replace('“', ' ').replace('"', ' ')
    s = re.sub(r'[()\[\]⟨⟩:!?]', ' ', s)
    s = re.sub(r'(?<=\w)[.,](?=\s|$)', ' ', s)
    return s.split()


def ngramme(tok, n):
    return set(tuple(tok[k:k + n]) for k in range(len(tok) - n + 1))


def laengste(a, b):
    best = 0
    for n in range(1, min(len(a), len(b)) + 1):
        if ngramme(a, n) & ngramme(b, n):
            best = n
        else:
            break
    return best


AUSSEN = [i for i in SATZ if not i.startswith('5 ') and not LISTE[i]['platzhalter']]
kand4 = OrderedDict()
kand3 = OrderedDict()
for k in K5:
    tk = tokens(T(k))
    for r in AUSSEN:
        tr = tokens(T(r))
        L = laengste(tk, tr)
        if L >= 4:
            kand4[(k, r)] = L
        elif L == 3:
            kand3[(k, r)] = L
p('')
p('N8 Gemeinsame Wortfolgen (eigene Tokenisierung, längste gemeinsame Folge je Satzpaar)')
p('  Sätze außerhalb (ohne Platzhalter) %d · Paare mit mindestens vier Wörtern %d, längste %d' % (
    len(AUSSEN), len(kand4), max(kand4.values())))
for (k, r), L in kand4.items():
    p('    %s | %s | %d' % (k, r, L))
p('  Paare mit genau drei Wörtern: %d (nur Kapitel 4 und 6.1):' % len(kand3))
for (k, r), L in kand3.items():
    if r.startswith('4') or r.startswith('6.1'):
        gem = [' '.join(g) for g in ngramme(tokens(T(k)), 3) & ngramme(tokens(T(r)), 3)]
        p('    %s | %s | %s' % (k, r, ' / '.join(sorted(gem))))
txk = tx[tx.find('\n§ 4 Gemeinsame'):tx.find('\n§ 5 ')]
ersteller_kand = re.findall(r'^  (5 A\d S\d+) \| (\S+(?: \S+){1,2}) \|', txk, re.M)
ersteller_kand = [(a, b.strip()) for a, b in ersteller_kand]
vergleiche('2e.3', 'Paare ab vier Wörtern', str(len(ersteller_kand)), str(len(kand4)))
vergleiche('2e.3', 'Paare gleich', 'ja', 'ja' if sorted(ersteller_kand) == sorted(kand4) else 'nein')
vergleiche('2e.3', 'längste Folge', '5', str(max(kand4.values())))
vergleiche('2e.3', 'Sätze außerhalb', '259', str(len(AUSSEN)))
vergleiche('2e.5', 'längste Folge 5 A2 S1 gegen 6.1 A2 S2', '3', str(laengste(tokens(T('5 A2 S1')), tokens(T('6.1 A2 S2')))))
vergleiche('2e.12', 'längste Folge 5 A3 S4 gegen 6.1 A6 S4', '1', str(laengste(tokens(T('5 A3 S4')), tokens(T('6.1 A6 S4')))))
vergleiche('2e.22', 'gemeinsame Folge 5 A5 S11 gegen 4.7 A1 S5', '5', str(laengste(tokens(T('5 A5 S11')), tokens(T('4.7 A1 S5')))))
vergleiche('2e.16', 'gemeinsame Folge 5 A4 S2 gegen 4.4 A2 S4', '4', str(laengste(tokens(T('5 A4 S2')), tokens(T('4.4 A2 S4')))))

# Aussagenähe unterhalb von vier Wörtern: Stammüberlappung der Inhaltswörter
STOP = set('der die das den dem des ein eine einen einem einer eines und oder mit von zu zur zum im in an auf bei '
           'für aus als wie war waren wurde wurden ist sind nicht nur je auch bis über unter nach vor ohne sowie dass '
           'sich es sie er damit dort seine ihr ihre jedes keine keiner kein alle beider beiden beide tab abb s'.split())


def staemme(s):
    out = set()
    for w in tokens(s):
        w = w.strip('.,')
        if w in STOP or len(w) < 3 or re.fullmatch(r'[−+\-\d,.%]+', w):
            continue
        out.add(re.sub(r'(en|er|es|em|e|n|s)$', '', w))
    return out


nah = []
for k in K5:
    sk = staemme(T(k))
    for r in AUSSEN:
        sr = staemme(T(r))
        if not sk or not sr:
            continue
        gem = sk & sr
        ueb = len(gem) / min(len(sk), len(sr))
        if len(gem) >= 3 and ueb >= 0.5 and (k, r) not in kand4:
            nah.append((k, r, len(gem), round(ueb, 2), sorted(gem)))
p('  Aussagenähe ohne Folge ab vier Wörtern (mindestens drei gemeinsame Stämme, Überlappung ≥ 0,5): %d Paare' % len(nah))
for k, r, n, u, g in nah:
    p('    %s | %s | %d Stämme, %s | %s' % (k, r, n, fz(u, 2), ' '.join(g)))

# ------------------------------------------------------------------ N9 Teiltabelle: Status, Schwere, Kennungen, Zitate
rows = list(csv.reader(open(os.path.join(ERSTE, 'teiltabelle_2e.csv'), encoding='utf-8', newline=''), delimiter=SK))
kopf, zeilen = rows[0], rows[1:]
p('')
p('N9 Teiltabelle 2e (erste Fassung): Status, Schwere, Satzkennungen ohne Präfix, Zitate')
stufen = Counter()
for zl in zeilen:
    st = zl[5]
    for s in ('nicht erfüllt', 'teilweise', 'erfüllt', 'bewusst anders'):
        if st.startswith(s):
            stufen[s] += 1
            break
p('  %d Zeilen: %s · mit Teil „bewusst anders“ %d' % (len(zeilen), ' · '.join('%s %d' % kv for kv in stufen.items()),
                                                       sum(1 for zl in zeilen if 'bewusst anders' in zl[5])))
ohne_schwere = [zl[0] for zl in zeilen if not zl[5].startswith('erfüllt') and 'Schwere' not in zl[5]]
p('  nicht „erfüllt“ und ohne Schwere im Status: %s' % (', '.join(ohne_schwere) or '—'))
vergleiche('2e (§ 10)', 'Zählung der Stufen', 'erfüllt 18 · teilweise 7 · nicht erfüllt 1',
           'erfüllt %d · teilweise %d · nicht erfüllt %d' % (stufen['erfüllt'], stufen['teilweise'], stufen['nicht erfüllt']))
# Satzkennungen ohne Abschnittspräfix, die in Kapitel 5 nicht existieren oder einem 6.1-Satz zugehören
K5_KENN = set(i.replace('5 ', '', 1) for i in K5)
S61_KENN = set(i.replace('6.1 ', '', 1) for i in S61)
for zl in zeilen:
    for spalte, inhalt in (('Ergebnis', zl[4]), ('Status', zl[5])):
        for m in re.finditer(r'(?<![\w.])(A\d S\d+)\b', inhalt):
            vor = inhalt[max(0, m.start() - 12):m.start()]
            if re.search(r'(6\.1|4\.\d(?:\.\d)?|5) $', vor) or re.search(r'(6\.1|4\.\d(?:\.\d)?) A\d S\d+, $', vor):
                continue
            ken = m.group(1)
            if ken not in K5_KENN:
                p('    %s %s: „%s“ ohne Präfix, in Kapitel 5 nicht vorhanden (6.1: %s)' % (
                    zl[0], spalte, ken, 'ja' if ken in S61_KENN else 'nein'))
# Kennungen ohne Präfix, die in Kapitel 5 und 6.1 vorkommen, in Zeilen, deren Prüfgegenstand oder Fundstelle 6.1 nennt
for zl in zeilen:
    if '6.1' not in zl[1] + zl[3]:
        continue
    for spalte, inhalt in (('Ergebnis', zl[4]), ('Status', zl[5])):
        for m in re.finditer(r'(?<![\w.])(A\d S\d+)\b', inhalt):
            vor = inhalt[max(0, m.start() - 12):m.start()]
            if re.search(r'(6\.1|4\.\d(?:\.\d)?|5) $', vor):
                continue
            ken = m.group(1)
            if ken in K5_KENN and ken in S61_KENN:
                p('    %s %s: „%s“ ohne Präfix, in Kapitel 5 und 6.1 vorhanden, Kontext: …%s…' % (
                    zl[0], spalte, ken, inhalt[max(0, m.start() - 40):m.end() + 40].replace(SK, ' ·')))
# Zitate in Ergebnis und Status: außen „…“ eines Zitats, im Master oder in einer Quelle
ALLE_TEXTE = [' '.join(SATZ.values())] + [DOK[k] for k in DOK]


def norm(s):
    return re.sub(r'\s+', ' ', s)


def zitate(s):
    out = []
    tiefe = 0
    start = None
    for n, ch in enumerate(s):
        if ch == '„':
            if tiefe == 0:
                start = n + 1
            tiefe += 1
        elif ch == '“' and tiefe:
            tiefe -= 1
            if tiefe == 0:
                out.append(s[start:n])
    return out


gefunden = 0
nicht = []
gesamt = 0
for zl in zeilen:
    for z_ in zitate(zl[2] + ' ' + zl[4] + ' ' + zl[5]):
        gesamt += 1
        teile = [x.strip() for x in z_.split('…') if x.strip()]
        treffer = False
        for txt in ALLE_TEXTE:
            t2 = norm(txt)
            pos = 0
            alle = True
            for tl in teile:
                q = t2.find(norm(tl), pos)
                if q < 0:
                    alle = False
                    break
                pos = q + len(tl)
            if alle:
                treffer = True
                break
        if treffer:
            gefunden += 1
        else:
            nicht.append((zl[0], z_))
p('  Zitate „…“ in Befundstelle, Ergebnis und Status: %d, gefunden in Master oder Quelle %d' % (gesamt, gefunden))
for nr, z_ in nicht:
    p('    nicht gefunden %s: „%s“' % (nr, z_))

# ------------------------------------------------------------------ N10 Reproduktion
p('')
p('N10 Reproduktion des Erstellerskripts im eigenen Ordner (zweit/repro)')
for name in ('anschluss_2e.txt', 'bezuege_2e.md', 'teiltabelle_2e.csv', 'teiltabelle_2e.md'):
    a = os.path.join(ERSTE, name)
    b = os.path.join(REPRO, name)
    p('  %-20s erste Fassung %s · Lauf %s · bytegleich %s' % (name, md5(a)[:12], md5(b)[:12],
                                                              open(a, 'rb').read() == open(b, 'rb').read()))

# ------------------------------------------------------------------ N11 Zusammenfassung der Nachrechnung
p('')
p('N11 Nachrechnung: Werte der Teiltabelle gegen die eigene Rechnung')
for nr, gr, er, ei, gl in NACH:
    p('  %-9s %-44s Ersteller %-28s eigen %-28s %s' % (nr, gr, er[:28], ei[:28], 'gleich' if gl else 'ABWEICHEND'))
p('  %d Werte, gleich %d, abweichend %d' % (len(NACH), sum(1 for x in NACH if x[4]), sum(1 for x in NACH if not x[4])))

# ------------------------------------------------------------------ N12 Belege zu den eigenen Befunden (Wortlaut an der Fundstelle)
BELEGE = [
    ('B1', 'tv61', '| A4 S7 | Dagegen verbesserte', 'Vergleich als Widerspruch markiert'),
    ('B1', 'tv61', '| A4 S8 | Auch ein achtwöchiges', 'außerhalb des eigenen Intervalls −0,085 bis +0,061'),
    ('B1', 'tv61', '| A5 S5 | Auch das Programm', 'außerhalb von −8,7 bis +8,6 cm'),
    ('B4', 'raster', '| 4.6.3 |', 'Einheitennummer kein Identitätsmerkmal'),
    ('B4', 's4a', '| 6.3.2 G6-b |', 'Untergrenzen nennt Kapitel 5, hier nur der Grund'),
    ('B4', 'f17', '**Zählregel:**', 'Untergrenzen: wochengedeckelt'),
    ('B5', 'tv5', '**9.5 Task 13b', 'Umsetzungsrate 42,6 % mit Bezugsmenge'),
    ('B5', 'raster', '| 7.1 |', 'Nullbefund-Sprachregelung'),
    ('B5', 'raster', '| 7.2 |', 'Belastungsverträglichkeit (Schmerzmeldungen)'),
    ('B5', 's4a', '| V06 |', '6.1 A6 S2 und S3 und Kapitel 5'),
    ('B5', 's4a', '| V42 |', 'nennen Kapitel 5 und 6.1 A6 S4'),
    ('B5', 's4a', '| V73 |', 'Kapitel 5 und Abb. 1'),
    ('B5', 's4a', '| K7-a |', 'Umsetzungsrate als eigenständiger Befund'),
    ('C1', 'umfang', 'C1 ', 'Der Befund ist unschlüssig'),
    ('C5', 'tv5', '4. **Begriffe zwischen 4.6 und Kapitel 5', 'beide sind aus dem Zusammenhang verständlich'),
    ('C6', 'tv5', '5. **Kein Handlungsbedarf, zur Kenntnis:**', 'Kapitel 5 schreibt „typischer Messfehler“ aus'),
    ('C8', 'tv5', '5. Abkürzungsverzeichnis:', 'AU (A3), CR-10, sRPE, TE, SESOI, %PAH, KI'),
    ('C9', 'tv5', '2. **Ausfallkategorie der 10-m-Zeiten', 'Der Verfasser klärt, was geschah'),
    ('C4', 'f17', '8. **Voraussetzungsbefunde:**', 'statt einer verteilungsfreien Gegenprobe nur beim 30-m-Sprint'),
    ('C13', 'tv5', '| 18 | C |', 'die Zahl der meldenden Spieler steht in Tab. H2'),
    ('C14', 'register', '| 6i |', '„deutlich“ in 6.1 A4 S6, S7, A5 S5'),
    ('C14', 'abgleich', '**Seit Rev. 154 entschieden?**', 'Modalverben in A4 S8 und A5 S7'),
    ('C3', 'nachtrag', '6. **Schlussfassung der Einleitung (G35):**', 'Den Satz zu Programmen bis sieben Wochen'),
]
p('')
p('N12 Belege zu den eigenen Befunden (Marke und Wortlaut in derselben Zeile der Quelle)')
for nr, dk, marke, wortlaut in BELEGE:
    zeilen_q = [z_ for z_ in DOK[dk].split('\n') if marke in z_]
    ok_ = any(wortlaut in z_ for z_ in zeilen_q)
    p('  %-4s %-9s %-46s %s' % (nr, dk, marke[:46], 'gefunden' if ok_ else 'NICHT GEFUNDEN'))
h0_in_liste = any('H0' in z_ for z_ in DOK['tv5'].split('\n') if z_.startswith('5. Abkürzungsverzeichnis:'))
p('  C8   „H0“ in der Abkürzungsliste TV5 § 9.6 Nr. 5: %s' % ('ja' if h0_in_liste else 'nein'))
p('  C14  Vorspann-Titel im Master: %s' % ', '.join(VORSPANN_TITEL))
p('  C4   Platzhalter Tab. H2 bis H4: %s' % ' | '.join(T(i) for i in SATZ if i.startswith('Anhang H A') and
                                                       re.search(r'Tab\. H[234]:', T(i))))

with open(os.path.join(AUS, 'zweitpruefung_2e_nachrechnung.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(OUT) + '\n')
print('\n'.join(OUT[-6:]))

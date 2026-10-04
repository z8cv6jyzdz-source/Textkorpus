# nachzaehlung_2d.py - Teilschritt 2 (d) des Tasks "Ergebnisse: Abgleich mit der Argumentationsstruktur und Ueberarbeitung"
# Jede Korpusaussage, auf die sich ein Potenzial fuer Kapitel 5 stuetzen soll, wird an der Anlage
# 02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv unabhaengig nachgezaehlt,
# die Lesart von "unclear", "substantial" und "trivial" am Methodenteil der Volltexte (Klusemann 2012, Beato 2018,
# Lloyd 2016, Negra 2019, Moran 2024).
# Eigenes Skript: keine Funktion aus pruef_2b.py, bausteine_2c.py, textbausteine.py oder analyse.py.
# Handurteile stehen als Tabellen im Skript und sind mit Pruefbedingungen an den Satztext gebunden.
# Weicht eine Bedingung ab, bricht das Skript ab.
# Aufruf: PYTHONDONTWRITEBYTECODE=1 python3 nachzaehlung_2d.py [Claude-Ordner] [Ausgabeordner] [PDF-Ordner]
# Ohne Argumente: Claude-Ordner zwei Ebenen ueber dem Skript, Ausgabe neben dem Skript,
# PDF-Ordner "Ideen und Studien" neben dem Claude-Ordner.
# Ausgaben: nachzaehlung_2d.txt (Protokoll), teiltabelle_2d.csv (Trennzeichen chr(59), alle Felder in Anfuehrungszeichen), teiltabelle_2d.md.
# Im Protokoll steht fuer ein Semikolon im Korpustext das Zeichen <SK> als Kennung, das Skript selbst
# und seine Ausgaben enthalten sonst kein Semikolon.
import csv, json, re, sys, hashlib, subprocess, pathlib, collections, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
C = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent.parent
OUT = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else HERE
PDFDIR = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else C.parent / 'Ideen und Studien'
SK = chr(59)
SKMARK = ' ‹SK› '

ANL = C / '02_Befunde' / 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv'
BEF = C / '02_Befunde' / 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md'
T2B = C / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03' / 'teiltabelle_2b.csv'
T2C = C / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03' / 'teiltabelle_2c.csv'
CODB = C / '03_Skripte' / 'Argumentationsstruktur_Ergebnisteile_2026-10-02' / 'codes_B.json'
QMD5 = C / '03_Skripte' / 'Argumentationsstruktur_Ergebnisteile_2026-10-02' / 'Quell_PDF_md5.txt'

LINES = []
def P(*a):
    LINES.append(' '.join(str(x) for x in a))

def stop(msg):
    sys.exit('Pruefbedingung verletzt: ' + msg)

def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()

def ws(s):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', s)).strip()

def sk(s):
    return s.replace(SK, SKMARK)

# ---------- Eingaenge ----------
for p in (ANL, BEF, T2B, T2C, CODB, QMD5):
    if not p.exists():
        stop('Eingang fehlt: ' + str(p))
A = list(csv.DictReader(open(ANL, encoding='utf-8'), delimiter=SK))
IDX = {(r['studie'], r['satz']): r for r in A}
KERN = list(dict.fromkeys(r['studie'] for r in A if r['gruppe'] == 'Kern'))
EXT = list(dict.fromkeys(r['studie'] for r in A if r['gruppe'] != 'Kern'))
if len(KERN) != 10 or len(EXT) != 6 or len(A) != 212:
    stop('Korpusgroesse')
BEFTXT = ws(open(BEF, encoding='utf-8').read())
T2BROWS = {row[0]: row for row in csv.reader(open(T2B, encoding='utf-8'), delimiter=SK)}
T2CROWS = {row[0]: row for row in csv.reader(open(T2C, encoding='utf-8'), delimiter=SK)}
CB = json.load(open(CODB, encoding='utf-8'))

def sec(r):
    return [x for x in r['sekundaer'].split(SK) if x]

def has(r, code):
    return r['primaer'] == code or code in sec(r)

def T(st, s):
    if (st, s) not in IDX:
        stop('Satz fehlt in der Anlage: ' + st + ' ' + s)
    return IDX[(st, s)]['text']

def need(st, s, rx, why):
    if not re.search(rx, T(st, s)):
        stop(why + ' bei ' + st + ' ' + s)

def kurz(st, s, n=150):
    t = sk(T(st, s))
    return t if len(t) <= n else t[:n] + ' …'

NAME = {'Lloyd2016': 'Lloyd', 'Hammami2016': 'Hammami', 'Beato2018': 'Beato', 'Negra2019': 'Negra 2019', 'Negra2020': 'Negra 2020',
        'Aloui2022': 'Aloui', 'Liu2024': 'Liu', 'Moran2024': 'Moran', 'Sammoud2024': 'Sammoud', 'Bouafif2026': 'Bouafif',
        'Hilska2021': 'Hilska', 'Klusemann2012': 'Klusemann', 'Veith2021': 'Veith', 'Rogers2020': 'Rogers',
        'PadronCabo2025': 'Padrón-Cabo', 'Asimakidis2022': 'Asimakidis'}
if set(NAME) != set(KERN) | set(EXT):
    stop('Studiennamen')
def lab(st, s):
    return (NAME[st] + ' ' + s).strip()
def nm(xs):
    return ', '.join(NAME[x] for x in xs)
def liste(keys):
    # Saetze je Studie zusammengefasst: "Klusemann 2.2, 2.4, Padrón-Cabo 2.1"
    out, cur = [], None
    for st, n in keys:
        if st != cur:
            out.append(NAME[st] + ' ' + n)
            cur = st
        else:
            out[-1] += ', ' + n
    return ', '.join(out)
LAGEN = ('vor dem ersten Befund', 'im Befundteil', 'nach dem letzten Befund')
def nach_lage(items):
    teile = []
    for lg in LAGEN:
        xs = [(st, n, a) for st, n, a, l in items if l == lg]
        teile.append(lg + ': ' + (', '.join(lab(st, n) + (' sekundär' if a == 'sekundaer' else '') for st, n, a in xs) if xs else 'keine'))
    return ' · '.join(teile)

# ---------- Volltexte ----------
PDFNAME = {}
for line in open(QMD5, encoding='utf-8'):
    parts = line.rstrip('\n').split('  ')
    if len(parts) >= 4:
        PDFNAME[parts[2]] = (parts[0], parts[3])
VOLL = ['Klusemann2012', 'Beato2018', 'Lloyd2016', 'Negra2019', 'Moran2024']

def pdftext(path, page, layout=False):
    cmd = ['pdftotext', '-f', str(page), '-l', str(page)] + (['-layout'] if layout else []) + [str(path), '-']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        stop('pdftotext ' + str(path))
    return res.stdout

def page_norm(raw):
    keep = [l for l in raw.split('\n') if not re.fullmatch(r'\s*\d{1,4}\s*', l)]
    return ws(' '.join(keep))

PDFPATH = {}
for k in VOLL:
    m5, name = PDFNAME[k]
    p = PDFDIR / name
    if not p.exists():
        stop('PDF fehlt: ' + name)
    if md5(p) != m5:
        stop('PDF-Pruefsumme weicht ab: ' + name)
    PDFPATH[k] = p

# Wortlaut der Methoden- und Ergebnisstellen: (Studie, PDF-Seite, gedruckte Seite oder Ort, Zitat)
VQ = [
 ('Klusemann2012', 3, 'S. 2679', 'Qualitative descriptors of standardized effects were assessed using these criteria: trivial'),
 ('Klusemann2012', 3, 'S. 2679', 'Precision of estimates is indicated with 90% confidence limits'),
 ('Klusemann2012', 3, 'S. 2679', 'Effects with confidence limits overlapping the thresholds for small positive and negative effects (exceeding 0.2 of the SD on both sides of the null) were defined as unclear.'),
 ('Klusemann2012', 3, 'S. 2679', 'Clear small or larger effect sizes were defined as substantial.'),
 ('Beato2018', 9, 'Manuskript S. 8, Z. 190 f.', 'Threshold values for benefit or harmful effect was evaluated based on the smallest worthwhile change (0.2 multiplied by the between-subjects SD)'),
 ('Beato2018', 9, 'Manuskript S. 8, Z. 191 bis 193', 'Effect size (ES) based on the Cohen d principle was interpreted as trivial <0.2, small 0.2-0.6, moderate 0.6-1.2, large 1.2-2.0, very large >2.0 (12).'),
 ('Beato2018', 9, 'Manuskript S. 8, Z. 193 f.', 'Data were analyzed for mechanistic (practical) significance using magnitude-based inferences'),
 ('Beato2018', 9, 'Manuskript S. 8, Z. 196', '>25% to 75%, possible'),
 ('Beato2018', 10, 'Manuskript S. 9, Z. 197 bis 199', 'If the chance of having beneficial or detrimental performances was >5%, the true difference was considered unclear.'),
 ('Beato2018', 10, 'Manuskript S. 9, Z. 215 f.', 'CODJ-G reported substantially better results in long jump test (ES = 0.32 (small), [CL90% -0.05'),
 ('Beato2018', 10, 'Manuskript S. 9, Z. 216 f.', 'with chances for beneficial, trivial, detrimental performance of 71/27/2%) than COD-G.'),
 ('Beato2018', 10, 'Manuskript S. 9, Z. 217 f.', 'All the other tests did not report any substantial variation between groups after the protocol.'),
 ('Beato2018', 10, 'Manuskript S. 9, Z. 218 f.', 'Forest plot with between-groups standardized changes is reported in figure 2.'),
 ('Beato2018', 12, 'Manuskript S. 11, Z. 255', 'found a meaningful improvement in 505 COD test (unclear effect).'),
 ('Beato2018', 13, 'Manuskript S. 12, Z. 274 f.', 'all the other parameters showed trivial and unclear differences between the two groups.'),
 ('Lloyd2016', 6, 'S. 1244', 'The smallest worthwhile effect was used to determine whether the observed changes were considered negative, trivial, or positive.'),
 ('Lloyd2016', 6, 'S. 1244', 'The smallest worthwhile effect was calculated as 0.20 of the pooled between-group SD before training (1).'),
 ('Lloyd2016', 6, 'S. 1244', 'The outcome was deemed unclear when the 90% confidence interval of the mean change overlapped both positive and negative outcomes'),
 ('Lloyd2016', 6, 'S. 1244', 'the inference reported as the category (negative, trivial, or positive) where the greatest probability was observed.'),
 ('Lloyd2016', 6, 'S. 1244, Legende zu Abb. 1', 'inferences are represented by U = unclear'),
 ('Negra2019', 11, 'akzeptiertes Manuskript ohne Seitenzahl', 'An effect size of 0.2 was considered to be the “smallest worthwhile change”.'),
 ('Negra2019', 11, 'akzeptiertes Manuskript ohne Seitenzahl', 'The estimates were considered unclear when the chance of a beneficial effect was high enough to justify the use of the intervention (>25%), yet the risk of being harmful was unacceptable (>0.5%).'),
 ('Negra2019', 11, 'akzeptiertes Manuskript ohne Seitenzahl', 'Uncertainty in the effect sizes was represented by 90% confidence limits.'),
 ('Negra2019', 11, 'akzeptiertes Manuskript ohne Seitenzahl', 'Effects were considered unclear if the confidence interval crossed thresholds for substantial positive and negative values.'),
 ('Negra2019', 11, 'akzeptiertes Manuskript ohne Seitenzahl', 'Otherwise, the effect was clear and reported as the magnitude of the observed value with a'),
 ('Negra2019', 12, 'akzeptiertes Manuskript ohne Seitenzahl', 'trivial between-group differences were demonstrated (Table 4).'),
 ('Moran2024', 5, 'S. 5', 'For informational rather than analytical purposes, we also present group effect sizes (Cohen’s d) alongside 95% confidence intervals (CI).'),
 ('Moran2024', 5, 'S. 5', 'Effect sizes (Tables 2 and 3) for the 10 m sprint were trivial in every group.'),
]
PAGECACHE = {}
def page(k, i):
    if (k, i) not in PAGECACHE:
        PAGECACHE[(k, i)] = pdftext(PDFPATH[k], i)
    return PAGECACHE[(k, i)]

VQOK = []
for k, pg, ort, q in VQ:
    if ws(q) not in page_norm(page(k, pg)):
        stop('Volltextzitat nicht auf der Seite: ' + k + ' ' + str(pg) + ' ' + q[:50])
    VQOK.append((k, pg, ort, q))
# Gedruckte Seiten: Klusemann S. 2679 auf PDF-Seite 3, Lloyd S. 1244 auf PDF-Seite 6, Moran 5 / 12 auf PDF-Seite 5,
# Beato (Manuskript) erste Zeile der PDF-Seite ist die Seitenzahl
if not re.search(r'OCTOBER 2012 \|\s+2679\s*$', pdftext(PDFPATH['Klusemann2012'], 3, layout=True), re.M):
    stop('Seite 2679')
if not re.search(r'^\s*1244\s+Journal of Strength and Conditioning Research', pdftext(PDFPATH['Lloyd2016'], 6, layout=True), re.M):
    stop('Seite 1244')
if not re.search(r'May 23, 2024\s+5 / 12\s*$', pdftext(PDFPATH['Moran2024'], 5, layout=True), re.M):
    stop('Seite 5 / 12')
for pg in (11, 12):
    if 'by Negra Y et al.' not in pdftext(PDFPATH['Negra2019'], pg) or 'Human Kinetics' not in pdftext(PDFPATH['Negra2019'], pg):
        stop('Negra Kopf des akzeptierten Manuskripts')
for pg, num in ((9, '8'), (10, '9'), (12, '11'), (13, '12')):
    first = [l.strip() for l in page('Beato2018', pg).split('\n') if l.strip()][0]
    if first != num:
        stop('Beato Seitenzahl ' + str(pg))
# Beato: Zeilennummern des Manuskripts je Zitat (die Nummer steht als eigene Zeile vor ihrer Textzeile)
def beato_zeilen(pg, q):
    nummer, stuecke = None, []
    for l in page('Beato2018', pg).split('\n'):
        t = l.strip()
        if re.fullmatch(r'\d{3}', t) and 100 <= int(t) <= 400:
            nummer = int(t)
        elif t and not re.fullmatch(r'\d{1,2}', t) and nummer is not None:
            stuecke.append((nummer, ws(t)))
    text, start = '', []
    for nr, t in stuecke:
        start.append((len(text), nr))
        text += t + ' '
    i = text.find(ws(q))
    if i < 0:
        stop('Beato Zeilen: Zitat nicht gefunden ' + q[:40])
    j = i + len(ws(q)) - 1
    erste = [nr for pos, nr in start if pos <= i][-1]
    letzte = [nr for pos, nr in start if pos <= j][-1]
    return erste, letzte
BEATOZ = []
for k, pg, ort, q in VQ:
    if k != 'Beato2018':
        continue
    m = re.search(r'Z\. (\d+)(?: (f\.)| bis (\d+))?$', ort)
    soll = (int(m.group(1)), int(m.group(1)) + 1 if m.group(2) else int(m.group(3)) if m.group(3) else int(m.group(1)))
    ist = beato_zeilen(pg, q)
    if soll != ist:
        stop('Beato Zeilenangabe ' + ort + ' gegen ' + str(ist))
    BEATOZ.append((ort, ist))
# Beato Abb. 2 (PDF-Seite 23) und Lloyd Abb. 1 (S. 1244): Bild ohne Textschicht, Urteile je Vergleich von Hand am
# gerenderten Bild gelesen (pdftoppm, 110 dpi). Gebunden ist nur, dass Seite 23 keine Textschicht hat und die Legende
# von Lloyd die Abkuerzungen erklaert.
if pdftext(PDFPATH['Beato2018'], 23).strip():
    stop('Beato Seite 23 hat eine Textschicht')
FIG = {
 'Beato2018': ('Abb. 2, PDF-Seite 23', [('Long jump', 'Possible'), ('Triple hop rechts', 'Likely trivial'), ('Triple hop links', 'Most likely trivial'),
               ('Sprint 10 m', 'Unclear'), ('Sprint 30 m', 'Unclear'), ('Sprint 40 m', 'Unclear'), ('505 COD', 'Trivial')]),
 'Lloyd2016': ('Abb. 1, S. 1244', [('PLY 10 m', 'VL-N'), ('TST 10 m', 'T'), ('COM 10 m', 'T'), ('CON 10 m', 'T'),
               ('PLY SJ', 'VL-P'), ('TST SJ', 'T'), ('COM SJ', 'T'), ('CON SJ', 'T'),
               ('PLY 20 m', 'T'), ('TST 20 m', 'T'), ('COM 20 m', 'U'), ('CON 20 m', 'T'),
               ('PLY RSI', 'T'), ('TST RSI', 'T'), ('COM RSI', 'T'), ('CON RSI', 'T')]),
}
def fig_unclear(st):
    return [n for n, u in FIG[st][1] if u in ('Unclear', 'U')]
def fig_trivial(st):
    return [n for n, u in FIG[st][1] if u.lower().endswith('trivial') or u == 'T']
# Negra 2019 Tab. 4 (PDF-Seite 25): die vier Vergleiche aus 2.8 heissen "similar", ihre Grenzen ueberschreiten beide Schwellen
t4 = pdftext(PDFPATH['Negra2019'], 25, layout=True)
if 'Table 4: Between-group effect sizes, confidence limits' not in t4:
    stop('Negra Tab. 4 Kopf')
NEGRA4 = []
for line in t4.split('\n'):
    m = re.match(r'\s*(ICoD test \(s\)|10-m sprint \(s\)|20-m sprint \(s\)|CMJ \(cm\))\s+(\S+)\s+([\d.]+)\s+(-?[\d.]+) to (-?[\d.]+)\s+([\d.]+/[\d.]+/[\d.]+)\s+(Most likely|Very likely)\s+\d+\s*$', line)
    if m:
        NEGRA4.append((m.group(1), float(m.group(3)), float(m.group(4)), float(m.group(5)), m.group(6), m.group(7)))
if len(NEGRA4) != 4 or t4.count('similar') != 4:
    stop('Negra Tab. 4 Zeilen')
for n, es, lo, hi, ch, d in NEGRA4:
    if not (lo < -0.2 and hi > 0.2 and es < 0.2):
        stop('Negra Tab. 4 Grenzen ' + n)
# Moran: der Text vor "Results" nennt keine Schwellen der Groessenklassen
mor = ''.join(page('Moran2024', i) for i in range(1, 6))
mor_meth = mor[:mor.rfind('\nResults')]
for w in ('trivial', 'smallest worthwhile', 'threshold'):
    if w in mor_meth.lower():
        stop('Moran Text vor Results enthaelt ' + w)
# Beato Tab. 1 (PDF-Seiten 20 und 21, Satzspiegel): "Unclear" genau dort, wo Nutzen und Schaden ueber 5 % liegen
tab = pdftext(PDFPATH['Beato2018'], 20, layout=True) + pdftext(PDFPATH['Beato2018'], 21, layout=True)
if 'Table 1. Summary of baseline and follow-up data' not in tab or 'better/trivial/worse' not in tab:
    stop('Beato Tab. 1 Kopf')
TABROWS = []
for line in tab.split('\n'):
    m = re.search(r'(\d+)/(\d+)/(\d+)\s+(\S.*?)\s*$', line)
    if m and re.search(r'\((?:m|s|cm)\)', line):
        name = line[:line.find('(')].strip()
        TABROWS.append((name, int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4).strip()))
if len(TABROWS) != 14:
    stop('Beato Tab. 1 Zeilenzahl ' + str(len(TABROWS)))
for name, b, t, d, q in TABROWS:
    if (b > 5 and d > 5) != (q == 'Unclear'):
        stop('Beato Tab. 1 Regel bei ' + name)
UNCL = [(n, b, t, d) for n, b, t, d, q in TABROWS if q == 'Unclear']
# Wortlaut "beneficial or detrimental ... >5%" woertlich angewandt
WOERTL = [(n, b, t, d, q) for n, b, t, d, q in TABROWS if b > 5 or d > 5]
WOERTL_ANDERS = [x for x in WOERTL if x[4] != 'Unclear']

# ---------- Zitate an der Befundstelle ----------
# Ort: "Befund § 3.5" (Abschnitt bis zur naechsten Ueberschrift gleicher oder hoeherer Ebene),
# "Befund § 0 Nr. 7" (Listenpunkt im Abschnitt), "Befund § 6.2 K4" (Tabellenzeile im Abschnitt),
# "2b.37" oder "2c.41" (Zeile der Teiltabelle). Gesucht wird nach Vereinheitlichung des Leerraums,
# ein Treffer zaehlt nur an Wortgrenzen.
BEFLINES = open(BEF, encoding='utf-8').read().split('\n')
def befund_ort(spec):
    m = re.fullmatch(r'(\d+(?:\.\d+)?)(?: Nr\. (\d+)| (K\d+))?', spec)
    if not m:
        stop('Befundort unlesbar: ' + spec)
    head = [i for i, l in enumerate(BEFLINES) if re.match(r'^(#{2,4}) ' + re.escape(m.group(1)) + r' ', l)]
    if len(head) != 1:
        stop('Abschnitt nicht eindeutig: ' + spec)
    i = head[0]
    lev = len(re.match(r'^(#+)', BEFLINES[i]).group(1))
    j = next((k for k in range(i + 1, len(BEFLINES)) if re.match(r'^#{1,' + str(lev) + r'} ', BEFLINES[k])), len(BEFLINES))
    part = BEFLINES[i + 1:j]
    if m.group(2):
        part = [l for l in part if l.startswith(m.group(2) + '. ')]
    if m.group(3):
        part = [l for l in part if l.startswith('| ' + m.group(3) + ' |')]
    if len(part) == 0:
        stop('Ort leer: ' + spec)
    return ws(' '.join(part).replace('**', ''))
def an_wortgrenze(qn, txt, start):
    # erste Fundstelle ab start, deren Raender an Wortgrenzen liegen, sonst -1
    while True:
        i = txt.find(qn, start)
        if i < 0:
            return -1
        vor = txt[i - 1] if i > 0 else ' '
        nach = txt[i + len(qn)] if i + len(qn) < len(txt) else ' '
        if (not qn[0].isalnum() or not vor.isalnum()) and (not qn[-1].isalnum() or not nach.isalnum()):
            return i + len(qn)
        start = i + 1
ZIT = []
def zit(ort, *frags):
    # mehrere Bruchstuecke muessen in dieser Folge am Ort stehen, ausgegeben mit Auslassungszeichen
    if ort.startswith('Befund § '):
        txt = befund_ort(ort[len('Befund § '):])
    elif ort in T2BROWS:
        txt = ws(' '.join(T2BROWS[ort]))
    elif ort in T2CROWS:
        txt = ws(' '.join(T2CROWS[ort]))
    else:
        stop('Ort unbekannt: ' + ort)
    pos = 0
    for q in frags:
        if SK in q:
            stop('Semikolon im Zitat ' + q[:40])
        pos = an_wortgrenze(ws(q), txt, pos)
        if pos < 0:
            stop('Zitat nicht am Ort ' + ort + ': ' + q[:60])
    ZIT.append((ort, ' … '.join(frags)))
    innen = [q.replace('„', '‚').replace('“', '‘') for q in frags]
    return '„' + ' … '.join(innen) + '“ (' + ort + ')'

# Zeilen der Teiltabelle: Nummer nach der Folge der Aufrufe, Querverweise als ‹Schluessel› im Text
ROWS = []
def row(**kw):
    for k, v in kw.items():
        if SK in str(v):
            stop('Semikolon in Spalte ' + k + ' von ' + kw.get('key', '?'))
    if kw['mass'] not in ('Korpus', 'Korpus (mit Volltext)'):
        stop('Massstab ' + kw['key'])
    kw['nr'] = '2d.' + str(len(ROWS) + 1)
    ROWS.append(kw)
def verweise():
    nr = {r['key']: r['nr'] for r in ROWS}
    for r in ROWS:
        for k, v in list(r.items()):
            if isinstance(v, str):
                for ref in re.findall(r'‹(?!SK›)(\w+)›', v):
                    if ref not in nr:
                        stop('Verweis unbekannt: ' + ref)
                r[k] = re.sub(r'‹(?!SK›)(\w+)›', lambda m: nr[m.group(1)], r[k])

# ---------- 1 Korpus ----------
P('Nachzaehlung 2 (d): Korpusaussagen, auf die sich ein Potenzial stuetzen soll (nachzaehlung_2d.py)')
P('')
P('0 Eingaenge (MD5)')
for p in (ANL, BEF, T2B, T2C, CODB, QMD5):
    P('  C/' + str(p.relative_to(C)).replace('\\', '/'), md5(p))
for k in VOLL:
    P('  PDF/' + PDFNAME[k][1], md5(PDFPATH[k]), '(gleich Quell_PDF_md5.txt)')
P('')
P('1 Korpus der Anlage')
P('  Kern', len(KERN), 'Studien', sum(1 for r in A if r['studie'] in KERN), 'Saetze, erweitert', len(EXT), 'Studien', sum(1 for r in A if r['studie'] in EXT), 'Saetze')
P('  Kern:', ', '.join(KERN))
P('  erweitert:', ', '.join(EXT))
P('  Im Protokoll steht' + SKMARK.strip() + 'fuer ein Semikolon im Korpustext.')
P('')

P('2 Volltexte: Wortlaut der Methoden- und Ergebnisstellen (je Zitat auf der genannten PDF-Seite gefunden)')
for k, pg, ort, q in VQOK:
    P('  ' + k, 'PDF-Seite', pg, '(' + ort + '):', '„' + q + '“')
P('  Moran 2024: Der Text vor „Results“ (PDF-Seiten 1 bis 5, Abstract, Einleitung und Methoden) enthaelt weder „trivial“ noch „smallest worthwhile“ noch „threshold“.')
P('  Beato 2018, Zeilennummern je Zitat geprueft:', ', '.join(o.split(', ')[-1] for o, z in BEATOZ))
P('  Beato 2018, Wortlaut „beneficial or detrimental … >5%“ woertlich angewandt:', len(WOERTL), 'von', len(TABROWS), 'Zeilen waeren unclear,', len(WOERTL_ANDERS), 'davon tragen ein anderes Urteil. Tab. 1 wendet „Nutzen und Schaden ueber 5 %“ an.')
P('  Abbildungen, Urteile je Vergleich von Hand am gerenderten Bild gelesen (pdftoppm, 110 dpi). Beato PDF-Seite 23 hat keine Textschicht, Lloyd S. 1244 traegt nur die Legende als Text („inferences are represented by U = unclear“):')
for st in ('Beato2018', 'Lloyd2016'):
    P('   ', NAME[st], FIG[st][0] + ':', ', '.join(n + ' ' + u for n, u in FIG[st][1]))
P('  Negra 2019, Tab. 4 (PDF-Seite 25): die vier Vergleiche aus 2.8 mit Effektstaerke unter 0,2, Grenzen und Beschreibung:', ', '.join('{} {} ({} bis {}, {} similar)'.format(n, es, lo, hi, d) for n, es, lo, hi, ch, d in NEGRA4))
P('  Beato 2018, Tab. 1 (PDF-Seiten 20 und 21, Veraenderung je Gruppe, Chancen „better/trivial/worse“):', len(TABROWS), 'Zeilen. „Unclear“ genau dort, wo Nutzen und Schaden ueber 5 % liegen:',
  ', '.join(n + ' ' + str(b) + '/' + str(t) + '/' + str(d) for n, b, t, d in UNCL) + '. Alle uebrigen Zeilen haben einen Schaden von hoechstens ' + str(max(d for n, b, t, d, q in TABROWS if q != 'Unclear')) + ' %.')
P('')

# ---------- 3 Nullbefunde (2d.1, 2d.2) ----------
# Handliste der Nullbefundsaetze des Kerns mit Form und Pruefausdruck.
# Formen: SIG fehlende Signifikanz, DIFF fehlender Unterschied oder fehlende Veraenderung ohne Signifikanzwort,
# KAT Groessen- oder Relevanzkategorie ("trivial", "substantial").
NULLK = [
 ('Lloyd2016', '1.2', 'SIG', r'none of the control groups made any significant changes'),
 ('Lloyd2016', '4.1', 'SIG', r'failed to determine any significant differences'),
 ('Lloyd2016', '4.2', 'SIG+KAT', r'were not significant and “trivial”'),
 ('Hammami2016', '1.1', 'SIG', r'did not show any significant differences'),
 ('Hammami2016', '1.3', 'SIG', r'None of the 3 agility tests showed any significant gains'),
 ('Hammami2016', '1.4', 'DIFF', r'remained unchanged'),
 ('Hammami2016', '1.5', 'SIG', r'No significant changes'),
 ('Beato2018', '4.2', 'KAT', r'did not report any substantial variation'),
 ('Negra2019', '2.8', 'KAT', r'trivial between-group differences'),
 ('Negra2020', '1.4', 'SIG+DIFF', r'except for the 1RM half-squat test \(p > 0\.05\), and the CG showed no changes'),
 ('Negra2020', '1.5', 'DIFF', r'No differences were found'),
 ('Liu2024', '2.1', 'SIG', r'There was not a significant main effect'),
 ('Liu2024', '2.4', 'SIG', r'did not significantly vary'),
 ('Liu2024', '3.3', 'SIG', r'no other significant differences were found'),
 ('Liu2024', '3.4', 'SIG', r'did not significantly varied'),
 ('Moran2024', '1.5', 'KAT', r'were trivial in every group'),
 ('Moran2024', '1.6', 'KAT', r'A trivial effect size was also observed'),
 ('Sammoud2024', '2.3', 'SIG', r'no significant pre-to-post changes'),
 ('Sammoud2024', '3.2', 'SIG', r'but not for the CG'),
 ('Bouafif2026', '1.1', 'SIG', r'except not for the CoD with right foot \(F = 0\.21, p = 0\.65'),
 ('Bouafif2026', '3.1', 'SIG', r'while the rest was not significant'),
 ('Bouafif2026', '3.2', 'SIG', r'no other effects reached significance level'),
 ('Bouafif2026', '3.3', 'SIG', r'No significant effects were found'),
 ('Bouafif2026', '4.1', 'SIG', r'no significant changes were observed'),
]
NULLRX = re.compile(r'\bno (?:statistically )?significant\b|\bnot (?:a )?significant|\bnot significantly\b|\bnonsignificant\b|\bdid not\b|\bfailed to\b|\bno (?:\w+ )?differences?\b|\bnone of\b|\bnot for\b|\bremained (?:unchanged|similar|trivial)\b|\bunchanged\b|\bno changes?\b|\bno clear\b|\bno observable\b|\bno other\b|\btrivial\b|\bunclear\b|\bnot report\b|\bnot \w+ significance\b|\bwas not\b', re.I)
NULLSET = {(s, n) for s, n, f, rx in NULLK}
for s, n, f, rx in NULLK:
    need(s, n, rx, 'Nullbefund-Handurteil')
    if not IDX[(s, n)]['primaer'].startswith('B'):
        stop('Nullbefund ohne B-Code ' + s + ' ' + n)
# Vollstaendigkeit: jeder Kern-Befundsatz mit einer Nullformel steht in der Handliste, ausser den begruendeten Ausnahmen
NULLAUS = {('Beato2018', '4.1'): r'chances for beneficial, trivial, detrimental'}
for r in A:
    if r['studie'] in KERN and r['primaer'].startswith('B') and NULLRX.search(r['text']):
        key = (r['studie'], r['satz'])
        if key in NULLSET:
            continue
        if key in NULLAUS and re.search(NULLAUS[key], r['text']):
            continue
        stop('Nullformel ohne Handurteil: ' + key[0] + ' ' + key[1])
nstud = list(dict.fromkeys(s for s, n, f, rx in NULLK))
form = collections.defaultdict(list)
for s, n, f, rx in NULLK:
    for x in f.split('+'):
        form[x].append(lab(s, n))
nki = [lab(s, n) for s, n, f, rx in NULLK if IDX[(s, n)]['ki'] != '0']
P('3 Nullbefunde im Kern (‹null›, ‹nullki›)')
P('  Nullbefundsaetze:', len(NULLK), 'in', len(nstud), 'von 10 Kernstudien, ohne:', ', '.join(x for x in KERN if x not in nstud))
for s, n, f, rx in NULLK:
    P('   ', lab(s, n), IDX[(s, n)]['primaer'], f, '|', kurz(s, n, 120))
P('  Ausnahme ohne Nullbefund: Beato 4.1 („trivial“ nur in der Chancenfolge „beneficial, trivial, detrimental“)')
P('  Formen: fehlende Signifikanz', len(form['SIG']), '(' + ', '.join(form['SIG']) + ')')
P('          fehlender Unterschied ohne Signifikanzwort', len(form['DIFF']), '(' + ', '.join(form['DIFF']) + ')')
P('          Groessen- oder Relevanzkategorie', len(form['KAT']), '(' + ', '.join(form['KAT']) + ')')
P('  Nullbefundsaetze mit Intervall (Spalte ki):', str(len(nki)) + (' (' + ', '.join(nki) + ')' if nki else ''))
# Kategorien, die der Methodenteil an der SWC festmacht (Volltext, Abschnitt 2)
KATSWC = [('Lloyd2016', '4.2', 'trivial', 'S. 1244: SWC 0,20 der gepoolten SD, Kategorie negativ, trivial, positiv nach der groessten Wahrscheinlichkeit'),
          ('Negra2019', '2.8', 'trivial', 'akzeptiertes Manuskript, PDF-Seite 11: Effektstaerke 0,2 als SWC, 90-%-Grenzen, klar und nach der Groesse berichtet')]
KATNEG = [('Beato2018', '4.2', 'substantial', 'Manuskript S. 8: Schwellen fuer Nutzen und Schaden an der SWC, „substantial“ nicht definiert, verneint fasst es nach Abb. 2 unclear und trivial zusammen')]
KATOHNE = [('Moran2024', '1.5'), ('Moran2024', '1.6')]
for s_, n_, w_, why_ in KATSWC + KATNEG:
    need(s_, n_, w_, 'Kategoriewort')
for s_, n_ in KATOHNE:
    need(s_, n_, 'trivial', 'Kategoriewort')
if {(s_, n_) for s_, n_, f_, r_ in NULLK if 'KAT' in f_} != {(s_, n_) for s_, n_, w_, why_ in KATSWC + KATNEG} | set(KATOHNE):
    stop('Kategorieform und Kategorielisten verschieden')
P('  Kategorie an der SWC nach dem Methodenteil:', len(KATSWC), 'Saetze in', len({s_ for s_, n_, w_, why_ in KATSWC}), 'Studien:')
for s_, n_, w_, why_ in KATSWC:
    P('   ', lab(s_, n_), '„' + w_ + '“,', why_)
P('  Verneinung von „substantial“:', ', '.join(lab(s_, n_) + ' (' + why_ + ')' for s_, n_, w_, why_ in KATNEG))
P('  Kategorie ohne Schwelle im Text vor „Results“:', ', '.join(lab(*k) for k in KATOHNE), '(„for informational rather than analytical purposes“)')
P('  Lloyd 4.2 „Nearly all … trivial“, in Abb. 1 unclear:', ', '.join(fig_unclear('Lloyd2016')), '· Beato 4.2 „not … any substantial“, in Abb. 2 unclear:', ', '.join(fig_unclear('Beato2018')), '· trivial:', ', '.join(fig_trivial('Beato2018')))
KLUN = [r for r in A if r['studie'] == 'Klusemann2012' and re.search(r'\bunclear\b', r['text'])]
# Klusemann: jeder Befundsatz mit ± nach Handurteil, ob ein Nullbefund eigene Grenzen traegt
KLPM = {
 '2.2': ('Grenzen nur an der Ausnahme', r'remained similar to baseline in all physical tests except for the agility test \(−1\.5 ± 1\.6%'),
 '2.3': ('kein Nullbefund', r'made small improvements'),
 '2.4': ('kein Nullbefund', r'small increase'),
 '2.5': ('Nullbefund mit eigenen Grenzen', r'^Trivial or unclear changes occurred in 20-m sprint time \(−0\.5 ± 1\.0%'),
 '2.6': ('Nullbefund mit eigenen Grenzen', r'remained trivial for the supervised group \(−1\.2 ± 1\.1%\)'),
 '2.8': ('kein Nullbefund', r'greater improvements'),
 '2.9': ('kein Nullbefund', r'better Yo-Yo IRL1 performance'),
 '3.1': ('kein Nullbefund', r'substantial increase'),
 '3.3': ('Nullbefund mit eigenen Grenzen', r'but with little difference compared with the video group \(−4\.2 ± 8\.0%'),
 '4.1': ('kein Nullbefund', r'small increases'),
 '4.2': ('kein Nullbefund', r'substantial decrease'),
 '4.4': ('Nullbefund mit eigenen Grenzen', r'^No clear changes were found in the pull-up test for the supervised group \(1 ± 13%\)'),
}
KLPMB_SAETZE = [r['satz'] for r in A if r['studie'] == 'Klusemann2012' and r['primaer'].startswith('B') and '±' in r['text']]
if set(KLPM) != set(KLPMB_SAETZE):
    stop('Klusemann ±-Saetze und Handurteil verschieden')
for n_, (kl_, rx_) in KLPM.items():
    need('Klusemann2012', n_, rx_, 'Klusemann ' + kl_)
KLNULLKI = [n_ for n_, (kl_, rx_) in KLPM.items() if kl_ == 'Nullbefund mit eigenen Grenzen']
KLNULLKI_B1 = [n_ for n_ in KLNULLKI if IDX[('Klusemann2012', n_)]['primaer'] == 'B1']
P('  erweitert: „unclear“ bei Klusemann in', len(KLUN), 'Saetzen (' + ', '.join(r['satz'] for r in KLUN) + '), Nullbefund mit eigenen ± 90-%-Grenzen in', len(KLNULLKI), '(' + ', '.join(KLNULLKI) + ', Gruppenvergleich: ' + ', '.join(KLNULLKI_B1) + '), Grenzen nur an der Ausnahme: 2.2')
uk = [lab(r['studie'], r['satz']) for r in A if r['studie'] in KERN and re.search(r'\bunclear\b', r['text'], re.I)]
P('  „unclear“ im Kern-Ergebnistext:', len(uk), 'Saetze')
P('')
row(key='null', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus', fund='Befund § 3.5, § 0 Nr. 7 · 2a.33, 2b.10',
    aussage=zit('Befund § 3.5', 'berichten 9 von 10 ausdrücklich (alle außer Aloui). Drei Formen: fehlende Signifikanz', 'fehlender Unterschied', 'und Größenklasse „trivial“'),
    zahl='9 von 10 (alle außer Aloui), drei Formen',
    nach='{} Nullbefundsätze in {} von 10 Kernstudien, ohne Aloui. Fehlende Signifikanz {}, fehlender Unterschied ohne Signifikanzwort {}, Größen- oder Relevanzkategorie {} ({}). Zwei Formen tragen {} Sätze ({}).'.format(
        len(NULLK), len(nstud), len(form['SIG']), len(form['DIFF']), len(form['KAT']), ', '.join(form['KAT']), len([1 for s_, n_, f_, r_ in NULLK if '+' in f_]), ', '.join(lab(s_, n_) for s_, n_, f_, r_ in NULLK if '+' in f_)),
    erg='bestätigt',
    folge='Zur dritten Form gehört neben „trivial“ auch „not … any substantial“ (Beato 4.2). Für den Fall C1 ohne Folge: Die Formen tragen den Nullbefund, die Lesart des Intervalls steht in ‹nullki›.',
    beleg='nachzaehlung_2d.txt § 3')
row(key='nullki', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus (mit Volltext)', fund='Befund § 3.5, § 0 Nr. 7 · 2a.33',
    aussage=zit('Befund § 3.5', 'Keine Studie liest einen Nullbefund über ein Intervall oder gegen eine Relevanzschwelle.') + ' · ' + zit('Befund § 0 Nr. 7', 'Nullbefunde berichten 9 von 10, immer ohne Intervall'),
    zahl='Intervall 0, Relevanzschwelle 0',
    nach='Intervall im Satz: {} der {} Nullbefundsätze des Kerns. Kategorie, die der Methodenteil an der kleinsten bedeutsamen Veränderung (SWC, 0,2 SD) festmacht: {} Sätze ({}), dazu {} als Verneinung des im Methodenteil nicht definierten „substantial“, das nach Abb. 2 die Urteile unclear ({}) und trivial ({}) zusammenfasst. {} „trivial“ ohne Schwelle. Negra 2019 nennt die {} Vergleiche aus 2.8 in Tab. 4 „similar“, ihre 90-%-Grenzen ({}) überschreiten beide Schwellen. Lloyd 4.2 übergeht mit „Nearly all“ ein „U“ in Abb. 1 ({}). Kern-Objekte mit „unclear“ je Vergleich: Lloyd Abb. 1 ({} von {}), Beato Abb. 2 ({} von {}). Erweitert Klusemann mit eigenen ± 90-%-Grenzen im Nullbefund ({}) und „unclear“ in {} Sätzen. „unclear“ im Kern-Ergebnistext {}.'.format(
        len(nki), len(NULLK), len(KATSWC), liste([(a, b) for a, b, c, d in KATSWC]), liste([(a, b) for a, b, c, d in KATNEG]), len(fig_unclear('Beato2018')), len(fig_trivial('Beato2018')), liste(KATOHNE), len(NEGRA4),
        ', '.join(sorted({'{} bis {}'.format(lo, hi).replace('.', ',').replace('-', '−') for n, es, lo, hi, ch, d in NEGRA4})), ', '.join(fig_unclear('Lloyd2016')),
        len(fig_unclear('Lloyd2016')), len(FIG['Lloyd2016'][1]), len(fig_unclear('Beato2018')), len(FIG['Beato2018'][1]), ', '.join(KLNULLKI), len(KLUN), len(uk)),
    erg='abweichend („ohne Intervall“ bestätigt, „gegen keine Relevanzschwelle“ nicht)',
    folge='Der Kern liest Nullbefunde gegen die SWC nur als Kategorie ohne Intervall, auch wo das Intervall beide Schwellen überschreitet (Negra 2019 2.8), und fasst „unclear“ aus den Objekten im Text in Sammelbefunde (Lloyd 4.2, Beato 4.2). Für § 3.5 und 2a.33 heißt es genauer „nie über ein Intervall, gegen die SWC nur als Kategorie oder als ‚nicht substantiell‘“. Der Status von 2c.20 (abgewandelt) bleibt.',
    beleg='nachzaehlung_2d.txt § 2, § 3')

# ---------- 4 Schlusslogik, Klusemann, Beato, Urteil in der Klammer (2d.3 bis 2d.6) ----------
P('4 Schlusslogik im Korpus (‹kein_vorbild› bis ‹klammer›)')
# Kernstudien mit MBI nach Befund § 2.1 (Spalte Hauptverfahren), ihre Methodenteile in Abschnitt 2 gelesen
i21 = next(i for i, l in enumerate(BEFLINES) if l.startswith('### 2.1 '))
j21 = next(i for i in range(i21 + 1, len(BEFLINES)) if BEFLINES[i].startswith('### '))
ROWS21 = [[c.strip() for c in l.strip().strip('|').split('|')] for l in BEFLINES[i21:j21] if re.match(r'^\| [A-Z][\w-]+(?: \d{4})? \|', l) and not l.startswith('| Studie')]
if len(ROWS21) != 10:
    stop('Befund § 2.1: Zeilenzahl ' + str(len(ROWS21)))
MBIK = [r_[0] for r_ in ROWS21 if 'MBI' in r_[2]]
if MBIK != ['Lloyd 2016', 'Beato 2018', 'Negra 2019']:
    stop('Befund § 2.1: MBI-Zeilen ' + str(MBIK))
METH_UNCL = ['Lloyd S. 1244', 'Beato Manuskript S. 8 f. über die Chancen', 'Negra 2019 akzeptiertes Manuskript PDF-Seite 11']
P('  Kernstudien mit MBI nach Befund § 2.1 (Hauptverfahren):', ', '.join(r_[0] + ' „' + r_[2] + '“' for r_ in ROWS21 if 'MBI' in r_[2]), '· ohne MBI:', ', '.join(r_[0] for r_ in ROWS21 if 'MBI' not in r_[2]))
P('  Methodenteile mit Schwelle 0,2 SD als SWC und „unclear“ fuer ein Intervall ueber beide Schwellen: Kern', len(METH_UNCL), '(' + ', '.join(METH_UNCL) + '), erweitert Klusemann (S. 2679)')
P('  Beato definiert „unclear“ ueber Chancen („beneficial or detrimental performances was >5%“), angewandt wie oben (Tab. 1)')
kiB = [r for r in A if r['studie'] in KERN and r['primaer'].startswith('B') and r['ki'] != '0']
P('  Kern-Befundsaetze mit Intervall (Spalte ki):', len(kiB), '(' + ', '.join(lab(r['studie'], r['satz']) for r in kiB) + ')')
need('Beato2018', '4.1', r'ES = 0\.32 \(small\), \[CL90% -0\.05', 'Beato 4.1 Intervall')
need('Beato2018', '4.1', r'71/27/2%', 'Beato 4.1 Chancen')
need('Beato2018', '4.1', r'reported substantially better results in long jump', 'Beato 4.1 substantially')
need('Beato2018', '4.1', r'\[CL90% -0\.05' + SK + r'\s*0\.69\]', 'Beato 4.1 obere Grenze')
P('  Beato 4.1:', kurz('Beato2018', '4.1', 260))
P('  Beato 4.2:', kurz('Beato2018', '4.2'))
P('  Klusemann, Saetze mit „unclear“:')
for r in KLUN:
    P('   ', r['satz'], r['primaer'], '|', kurz(r['studie'], r['satz'], 160))
klB1 = [r['satz'] for r in KLUN if r['primaer'] == 'B1']
klPM = [r['satz'] for r in KLUN if '±' in r['text']]
klPMB = [r['satz'] for r in A if r['studie'] == 'Klusemann2012' and r['primaer'].startswith('B') and '±' in r['text']]
P('  davon Gruppenvergleich (B1):', ', '.join(klB1), '· mit ± im Satz:', ', '.join(klPM))
P('  Klusemann, Saetze mit Primaercode B und ±:', len(klPMB), '(' + ', '.join(klPMB) + ')')
need('Klusemann2012', '2.2', r'mean ± 90% confidence limits', 'Klusemann 2.2 Grenzen')
P('  Klusemann 2.2 erklaert ± als „mean ± 90% confidence limits“, die Methodik als 90-%-Grenzen (Abschnitt 2).')
# Urteil oder Klasse in der Klammer neben Schaetzer und Grenzen
KLASSE = re.compile(r'\b(trivial|small|moderate|large|very large|unclear)\b')
def klammern(t):
    out, depth, start = [], 0, None
    for i, ch in enumerate(t):
        if ch == '(':
            if depth == 0:
                start = i
            depth += 1
        elif ch == ')' and depth:
            depth -= 1
            if depth == 0:
                out.append(t[start + 1:i])
    return out
URT = collections.defaultdict(list)
for r in A:
    if not r['primaer'].startswith('B'):
        continue
    for kl in klammern(r['text']):
        if not KLASSE.search(kl):
            continue
        grenze = bool(re.search(r'\bCL\d*|\bCI\b|confidence', kl)) or (r['studie'] == 'Klusemann2012' and '±' in kl)
        URT['mit' if grenze else 'ohne'].append((r['studie'], r['satz'], KLASSE.findall(kl)))
def uniq(xs):
    return list(dict.fromkeys((s, n) for s, n, w in xs))
mit = uniq(URT['mit'])
ohne = [x for x in uniq(URT['ohne']) if x not in mit]
mitK = [x for x in mit if x[0] in KERN]
mitE = [x for x in mit if x[0] not in KERN]
unclKl = uniq([x for x in URT['mit'] if 'unclear' in x[2]])
P('  Klasse oder Urteil in der Klammer neben Schaetzer und Grenzen: Kern', len(mitK), '(' + ', '.join(lab(*x) for x in mitK) + '), erweitert', len(mitE), '(' + ', '.join(lab(*x) for x in mitE) + ')')
P('  davon mit „unclear“ in der Klammer:', ', '.join(lab(*x) for x in unclKl))
P('  Klasse in der Klammer ohne Grenzen:', ', '.join(lab(*x) for x in ohne))
P('')
row(key='kein_vorbild', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus (mit Volltext)', fund='Befund § 6.4, § 2.1 · 2b.37',
    aussage=zit('Befund § 6.4', 'Kein Vorbild für die Schlusslogik (Intervall gegen null und SESOI, Fall C1)') + ' · ' + zit('2b.37', 'Ohne Korpusvorbild umgesetzt: Schlusslogik mit Intervall gegen null und SESOI (A5 S7, S8)'),
    zahl='kein Vorbild',
    nach='MBI nach Befund § 2.1 in {} Kernstudien, ihre Methodenteile setzen die Schwelle 0,2 SD als SWC und lesen „unclear“ als Intervall über beide Schwellen ({}), erweitert ebenso Klusemann. Ergebnistext: Fall C1 („unclear“) Kern {}, erweitert Klusemann {} Sätze. Kern-Objekte tragen „unclear“ je Vergleich (Lloyd Abb. 1, Beato Abb. 2), Beato 4.2 fasst es im Text als „not … any substantial“. Ein Intervall gegen beide Schwellen liest im Kern-Ergebnistext nur Beato 4.1 ({} Satz, Chancen 71/27/2, Vorteil „possible“). Urteil als Kategorie an der SWC {} Sätze (‹nullki›).'.format(
        len(MBIK), ', '.join(METH_UNCL), len(uk), len(KLUN), len(kiB), len(KATSWC)),
    erg='abweichend (Fall C1 erweitert bei Klusemann im Text, im Kern in Objekten, nur für den Kern-Ergebnistext bestätigt)',
    folge='„Kein Vorbild“ gilt nur für den Fall C1 im Ergebnistext des Kerns. Im Kern stehen Schwelle und Lesart im Methodenteil, das Urteil „unclear“ in Objekten und als Sammelbefund im Text, erweitert liest Klusemann den Fall C1 im Text. 2b.37 bleibt „bewusst anders“ (P3, P5, P6), sein Korpusteil heißt genauer „ohne Kernvorbild für den Fall C1 im Text, erweitert Klusemann“.',
    beleg='nachzaehlung_2d.txt § 2, § 4')
row(key='klusemann', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus (mit Volltext)', fund='2c.41, 2c.21, 2c.22 · Befund § 3.4',
    aussage=zit('2c.41', 'Erweitert liest Klusemann Gruppenvergleiche über Schätzer ± 90-%-Grenzen mit dem Urteil „unclear“ (3.3, ohne Intervall im Satz 2.7 und 4.3)') + ' · ' + zit('2c.41', 'Dass „unclear“ ein Intervall über beide Relevanzschwellen bezeichnet, ist an der Methodik zu bestätigen (2 d).') + ' · ' + zit('Befund § 3.4', 'Klusemann (Veränderung mit 90-%-Grenzen, erklärt in 2.2, ± in 12 Befundsätzen)'),
    zahl='Gruppenvergleich mit „unclear“ 3.3, ohne Intervall 2.7 und 4.3 · ± in 12 Befundsätzen',
    nach='„unclear“ in {} Sätzen ({}), davon Gruppenvergleich (B1) {} ({}), mit ± im Satz {} ({}). ± in {} Sätzen mit Primärcode B. Methodik S. 2679: Grenzen als 90-%-Vertrauensgrenzen, „unclear“, wenn die Grenzen die Schwellen für kleine positive und negative Effekte überschreiten (0,2 SD auf beiden Seiten der Null), „substantial“ für einen klaren Effekt ab „small“ (Wortlaut im Protokoll § 2). Nullbefund mit eigenen Grenzen: {}, darunter der Gruppenvergleich {}.'.format(
        len(KLUN), ', '.join(r['satz'] for r in KLUN), len(klB1), ', '.join(klB1), len(klPM), ', '.join(klPM), len(klPMB), ', '.join(KLNULLKI), ', '.join(KLNULLKI_B1)),
    erg='bestätigt (in 2c.41 ungenau: Nullformel mit eigenen Grenzen auch im Gruppenvergleich {})'.format(', '.join(KLNULLKI_B1)),
    folge='„unclear“ ist ein 90-%-Intervall über beide Schwellen (± 0,2 SD), „substantial“ ein klarer Effekt ab „small“. Das erweiterte Vorbild trifft den Fall C1 mit 90 statt 95 % und der Schwelle 0,2 SD wie der SESOI (0,2 × Zwischen-Athleten-SD), für den Fall C1 bleibt 2c.41 „nur erweitert“. In 2c.41 tragen Nullformel und Grenzen nicht „nur Veränderungen je Gruppe (2.2, 2.5, 2.6, 4.4)“, sondern {}, darunter der Gruppenvergleich {}, 2.2 hat Grenzen nur an der Ausnahme.'.format(', '.join(KLNULLKI), ', '.join(KLNULLKI_B1)),
    beleg='nachzaehlung_2d.txt § 2, § 3, § 4')
row(key='beato', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus (mit Volltext)', fund='Befund § 0 Nr. 7, § 3.4 · 2c.21, 2c.22, 2c.41',
    aussage=zit('2c.21', 'Im Kern liest Beato eine Effektstärke mit 90-%-Grenzen gegen Schwellen in beide Richtungen') + ' · ' + zit('Befund § 0 Nr. 7', 'ein Intervall nur bei Beato (90-%-Grenzen)') + ' · ' + zit('Befund § 3.4', 'Beato 4.1 (ANCOVA, ES mit 90-%-Grenzen der MBI)'),
    zahl='Intervall im Befundsatz nur Beato 4.1',
    nach='Kern-Befundsätze mit Intervall (Spalte ki): {} ({}). Methodik (Manuskript S. 8 f., Z. 190 bis 199): Schwellen für Nutzen und Schaden an der SWC (0,2 × Zwischen-Personen-SD), Effektstärkeklassen nach Cohen (trivial unter 0,2, small 0,2 bis 0,6), Chancen über 25 bis 75 % „possible“, „unclear“ nach dem Wortlaut bei einer Chance für Nutzen oder Schaden über 5 %. Tab. 1 wendet „und“ an ({}), wörtlich angewandt wären {} von {} Zeilen unclear. „substantial“ ist im Methodenteil nicht definiert. 4.1 „substantially better“ mit ES 0,32 (small), Grenzen −0,05 bis 0,69 und Chancen 71/27/2 („possible“). 4.2 Nullbefund ohne Intervall, in Abb. 2 dreimal unclear und dreimal trivial, in der Diskussion „trivial and unclear differences“ (Manuskript S. 12).'.format(
        len(kiB), ', '.join(lab(r['studie'], r['satz']) for r in kiB), ', '.join(n + ' ' + str(b) + '/' + str(t) + '/' + str(d) for n, b, t, d in UNCL), len(WOERTL), len(TABROWS)),
    erg='bestätigt („substantial“ im Methodenteil nicht definiert)',
    folge='Beato 4.1 ist ein Kernbaustein der Funktion „Lesart des Intervalls“ in anderer Bauform (Grenzen und Chancen in der Klammer, bei möglichem Vorteil statt im Fall C1), Lloyd 4.2 und Negra 2019 2.8 sind Kernbausteine der Funktion „Urteil“ als Kategorie an der SWC (‹nullki›). Nach der Statusregel von § 3.3 stehen 2c.21 und 2c.22 deshalb auf „abgewandelt“ statt „nur erweitert“, der Teil ohne Kernvorbild ist der Fall C1 im Text (erweitert Klusemann 2.7, 3.3, 4.3). 2c.41 bleibt für den Fall C1 „nur erweitert“, sein Satz „Lesart des Intervalls und Urteil haben im Kern kein Vorbild.“ gilt nur für diesen Fall. 2c je Satz danach: abgewandelt 14 Sätze mit 220 Wörtern, nur erweitert 8 mit 122, Kernbaustein 19 Sätze mit 311 von 450 Wörtern, über alle Zeilen abgewandelt 21, nur erweitert 16.',
    beleg='nachzaehlung_2d.txt § 2, § 4')
row(key='klammer', pot='Fall C1 je Zielgröße oder in der Klammer (2b.9, 2c.41)',
    mass='Korpus (mit Volltext)', fund='2c.41 · 2b.9',
    aussage=zit('2c.41', 'Ein Vorbild für den Fall je Vergleich in der Klammer ist Klusemann 3.3.'),
    zahl='Klusemann 3.3 (erweitert)',
    nach='Befundsätze mit Klasse oder Urteil in der Klammer neben Schätzer und Grenzen: Kern {} ({}), erweitert {} ({}), „unclear“ in der Klammer nur {}. Klasse in der Klammer ohne Grenzen: {}. Den Fall für mehrere Vergleiche in einem Satz fassen Beato 4.2 (Kern, „not … any substantial“ über sechs Tests, je Test in Abb. 2 dreimal unclear und dreimal trivial) und Klusemann 2.7 (erweitert, „trivial or unclear“ über drei Tests).'.format(
        len(mitK), liste(mitK), len(mitE), liste(mitE), liste(unclKl), liste(ohne)),
    erg='bestätigt',
    folge='Für den Fall je Zielgröße in der Klammer gibt es ein Kernvorbild der Form (Beato 4.1, Klasse neben Grenzen und Chancen) und ein erweitertes Vorbild des Falls (Klusemann 3.3, „unclear“ neben Schätzer ± Grenzen). Auch die jetzige Form, der Fall einmal für mehrere Zielgrößen (2b.9), hat Vorbilder: Beato 4.2 im Kern mit dem Fall je Test in Abb. 2, Klusemann 2.7 erweitert.',
    beleg='nachzaehlung_2d.txt § 2, § 4')

# ---------- 5 Zuordnung paralleler Werte (2d.7, 2d.8) ----------
RESP = re.compile(r'\brespectively\b|\brespectfully\b', re.I)
respK = [r for r in A if r['studie'] in KERN and RESP.search(r['text'])]
respK_streng = [r for r in respK if re.search(r'\brespectively\b', r['text'])]
respE = [r for r in A if r['studie'] not in KERN and RESP.search(r['text'])]
respKst = list(dict.fromkeys(r['studie'] for r in respK))
respEst = list(dict.fromkeys(r['studie'] for r in respE))
need('Beato2018', '1.1', r'respectfully', 'Schreibfehler respectfully')
need('Hammami2016', '1.3', r'had respective p values', 'respective')
# Kandidaten paralleler Werte: Zahlen mit "and", "vs." oder "versus" verbunden, jeder Satz mit Zuordnungswort,
# dazu Saetze mit mindestens zwei Klammern mit Statistik oder einer Klammer mit mindestens zwei Gliedern "Bezeichnung: Wert"
CAND = re.compile(r'\d(?:[\d.,]*\d)?\s*(?:%|s|m|cm|kg|°)?\s*\)?\s*,?\s*(?:and|vs\.?|versus)\s+\(?(?:[Δ∆]|[A-Za-z]{1,6}\s*=\s*)?[−-]?\d')
STATX = re.compile(r'(?:\bp\s*[<>=≤≥]|\bF\s*[=≥≤(]|\bd\s*=|[Δ∆]|\bES\s*=|η|\bCI\b|mean difference|±|\d\s*%|\bIRR\b|\bchange\s*=)')
GLIED = re.compile(r'(?:^|,|' + SK + r')\s*[^\s:(),' + SK + r']{1,30}(?: [^\s:(),' + SK + r']{1,30}){0,3}:\s*[−\-]?[Δ∆\d]')
def cand2(t):
    kl = klammern(t)
    return sum(1 for k in kl if STATX.search(k)) >= 2 or any(len(GLIED.findall(k)) >= 2 for k in kl)
# Handurteil je Kandidat. Kennungen: ZW Zuordnungswort fuer Werte, ZO Zuordnungswort fuer Objekte, GL Gleichheitszeichen,
# BZ Bezeichnung je Wert (jeder Wert direkt bei seiner Bezeichnung), FO Folge ohne Zuordnungswort mit der Bezugsfolge
# im selben Satz, VS Folge mit der Bezugsfolge im vorigen Satz, GR Grenzfall (ein benannter Wert und ein Sammelwert
# fuer den Rest), KP keine parallelen Werte.
ZUO = {
 ('Lloyd2016', '1.1'): ('ZO', r'displayed in Table 4 for pre- and post-PHV groups, respectively'),
 ('Lloyd2016', '1.3'): ('GL', r'plyometric training = 91%, traditional strength training = 89%'),
 ('Hammami2016', '1.2'): ('KP', r'over distances of 5m, 10m and 20m \(p≤0\.05\)'),
 ('Hammami2016', '1.3'): ('ZW', r'had respective p values of 0\.08, 0\.06 and 0\.142'),
 ('Hammami2016', '1.4'): ('ZW', r'p<0\.01 and p<0\.05 respectively'),
 ('Beato2018', '1.1'): ('ZW', r'respectfully'),
 ('Beato2018', '2.1'): ('ZW', r'93% and 96% for CODJ-G and COD-G, respectively'),
 ('Beato2018', '2.2'): ('ZW', r'5\.5 ± 0\.99 and 5\.50 ± 1 for CODJ-G and COD-G, respectively'),
 ('Beato2018', '3.2'): ('ZO', r'Tables 1 and 2, respectively'),
 ('Negra2019', '2.3'): ('ZW', r'large and very large effect sizes .* respectively'),
 ('Negra2020', '1.4'): ('BZ', r'the RTG showed significant improvements in all tests \(p < 0\.05\)'),
 ('Aloui2022', '2.1'): ('BZ', r'\(SJ: Δ'),
 ('Aloui2022', '3.1'): ('BZ', r'\(10 m sprint: Δ'),
 ('Aloui2022', '4.1'): ('BZ', r'\(S90◦: Δ'),
 ('Aloui2022', '5.1'): ('FO', r'\(RSSA best and RSSA mean\), with time decreases of Δ−8% \(p < 0\.01, d = 0\.72\) and Δ−8%'),
 ('Aloui2022', '6.1'): ('BZ', r'\(anterior: Δ'),
 ('Aloui2022', '6.2'): ('BZ', r'\(anterior: Δ'),
 ('Liu2024', '1.1'): ('BZ', r'on CMJ \(F=0\.979'),
 ('Liu2024', '2.3'): ('BZ', r'different from HIIT \(mean difference: \W?2\.133cm'),
 ('Liu2024', '2.4'): ('ZW BZ', r'p>0\.080, respectively\), while PJT significantly improved \(mean difference'),
 ('Liu2024', '3.3'): ('GR', r'different from HIIT \(mean difference: \W?270\.67m.* no other significant differences were found \(p>0\.05\)'),
 ('Liu2024', '3.4'): ('BZ', r'HIIT did not significantly varied from pre to post \(p=0\.474\), while PJT significantly declined \(mean difference'),
 ('Liu2024', '4.3'): ('BZ', r'different from HIIT \(mean difference: 0\.031s'),
 ('Liu2024', '4.4'): ('BZ', r'HIIT significantly declined from pre to post \(mean difference: 0\.023s'),
 ('Moran2024', '1.5'): ('KP', r'\(Tables 2 and 3\)'),
 ('Sammoud2024', '1.5'): ('GR', r'were observed \(p > 0\.05\), except for the inter-limb asymmetry score \(p < 0\.05\)'),
 ('Sammoud2024', '2.1'): ('BZ', r'for CMJ height \(p < 0\.001'),
 ('Sammoud2024', '2.2'): ('BZ', r'in CMJ height \(∆16\.85%'),
 ('Sammoud2024', '2.3'): ('BZ', r'for CMJ height \(∆0\.76%'),
 ('Sammoud2024', '3.2'): ('BZ', r'for the PJT group \(change = -4\.75%%, d = 0\.43\) but not for the CG \(change = 1\.96%'),
 ('Bouafif2026', '1.1'): ('GR', r'^All performances were significantly enhanced from pre- to post test \(F ≥ 4\.3.*except not for the CoD with right foot \(F = 0\.21'),
 ('Bouafif2026', '1.2'): ('BZ', r'for all tests \(F ≥ 7\.2.*for the balance and CoD test with the right foot \(F ≥ 4\.2'),
 ('Bouafif2026', '3.1'): ('BZ', r'by training age \(F = 15\.0'),
 ('Bouafif2026', '3.2'): ('BZ', r'by training group \(F = 6\.5'),
 ('Hilska2021', '2.1'): ('ZW', r'96% and 95% in the intervention and control groups, respectively'),
 ('Hilska2021', '4.1'): ('ZW', r'1\.8 and 2\.7 per 1000 hours of exposure in the intervention and control groups, respectively'),
 ('Hilska2021', '4.2'): ('BZ', r'in joint/ligament injuries \(by 38% in the unadjusted model\) and in ankle injuries \(41%\)'),
 ('Hilska2021', '6.2'): ('KP', r'between 0 and 7 days'),
 ('Hilska2021', '6.3'): ('KP', r'between 0 and 7 days'),
 ('Hilska2021', '8.3'): ('BZ', r'included planks \(94% of the teams who answered\), single-leg squats and/or lunges \(82%\)'),
 ('Klusemann2012', '2.3'): ('ZW FO BZ', r'^The supervised and video groups made .*respectively\) and agility \(−2\.2 ± 2\.2% and −3\.8 ± 1\.1%\)'),
 ('Klusemann2012', '2.5'): ('FO BZ', r'\(−0\.5 ± 1\.0% and −1\.6 ± 2\.0%\).* for the supervised and video groups\.$'),
 ('Klusemann2012', '2.6'): ('BZ', r'for the supervised group \(−1\.2 ± 1\.1%\) but declined for the video group \(−1\.6 ± 1\.7%\)'),
 ('Klusemann2012', '2.8'): ('BZ', r'in agility \(−1\.7 ± 2\.4%'),
 ('Klusemann2012', '3.1'): ('BZ', r'in the supervised group \(5\.0 ± 4\.2%'),
 ('Klusemann2012', '3.3'): ('BZ', r'than the control group \(−9\.2 ± 7\.3%'),
 ('Klusemann2012', '4.1'): ('FO', r'^Both the supervised and video groups .*\(20 ± 13% and 23 ± 15%\)'),
 ('Klusemann2012', '4.4'): ('BZ', r'for the supervised group \(1 ± 13%\) and video group \(1 ± 21%\)'),
 ('Veith2021', '1.3'): ('BZ', r'^Height \(p < 0\.001\) and body mass \(p < 0\.001\)'),
 ('Veith2021', '2.1'): ('BZ', r'\(HG 3\.5 cm'),
 ('Veith2021', '2.4'): ('BZ', r'\(HG 2\.5 kg'),
 ('Veith2021', '2.5'): ('BZ', r'at test 1 \(1\.6 kg.*only in the HG \(1\.9 kg'),
 ('Veith2021', '3.3'): ('BZ', r'Having no partner \(48\.9%\) and injury/soreness/sickness \(44\.7%\)'),
 ('Veith2021', '3.4'): ('ZW', r'\(29% and 28%, respectively\)'),
 ('Rogers2020', '1.7'): ('ZO', r'Tables 3 and 4 respectively'),
 ('Rogers2020', '1.8'): ('KP', r'Figures 3 and 4'),
 ('Rogers2020', '2.7'): ('KP', r'between 0 and 11 sessions'),
 ('PadronCabo2025', '2.1'): ('BZ', r'for SJ \(F = 0\.604'),
 ('PadronCabo2025', '2.2'): ('ZW BZ', r'main effects for time \(F = 4\.456.*respectively\) and group \(F = 9\.249'),
 ('PadronCabo2025', '2.3'): ('BZ', r'for U15 \(d = 0\.21\) and U17 \(d = 0\.46\)'),
 ('PadronCabo2025', '2.4'): ('BZ', r'the U15 \(d = 0\.30\) and U17 \(d = 0\.63\)'),
 ('PadronCabo2025', '3.1'): ('BZ', r'in the 5-m \(F = 8\.865'),
 ('PadronCabo2025', '3.2'): ('BZ', r'in the 5-m \(F = 47\.764'),
 ('PadronCabo2025', '3.3'): ('BZ', r'in 5-m \(d = 0\.80\), 10-m \(d = 0\.80\)'),
 ('PadronCabo2025', '3.4'): ('BZ', r'in 5-m \(d = 2\.21\), 10-m \(d = 2\.21\)'),
 ('PadronCabo2025', '3.5'): ('ZW BZ', r'in the 20-m sprint test \(F = 12\.715.*respectively\) sprint tests'),
 ('PadronCabo2025', '4.1'): ('BZ', r'interaction \(F = 0\.229.*main effect for time \(F = 3\.550'),
 ('PadronCabo2025', '5.1'): ('BZ', r'interaction \(F = 0\.105.*main effect of time \(F = 37\.351'),
 ('PadronCabo2025', '5.2'): ('ZW', r'\(d = 1\.39 and 1\.24, respectively\)'),
 ('Asimakidis2022', '1.2'): ('ZO', r'Figures 1–4 illustrate the group data for COD ability and linear sprint, respectively'),
 ('Asimakidis2022', '1.3'): ('BZ', r'using both the right \(p = 0\.037'),
 ('Asimakidis2022', '1.4'): ('BZ', r'Similarly, 10 m \(p < 0\.001'),
 ('Asimakidis2022', '1.6'): ('ZW', r'for the CMJ, 10 m, 20 m, and COD test of the right and left leg, respectively\)'),
 ('Asimakidis2022', '1.7'): ('ZW', r'for the 10 m, 20 m, COD of the right leg, the left leg, and the CMJ, respectively'),
}
ZTAGS = {'ZW': 'Zuordnungswort fuer Werte', 'ZO': 'Zuordnungswort fuer Objekte', 'GL': 'Gleichheitszeichen', 'BZ': 'Bezeichnung je Wert',
         'FO': 'Folge, Bezugsfolge im Satz', 'VS': 'Folge, Bezugsfolge im vorigen Satz', 'GR': 'Grenzfall Wert und Sammelwert', 'KP': 'keine parallelen Werte'}
for (s_, n_), (kl_, rx_) in ZUO.items():
    if not set(kl_.split()) <= set(ZTAGS):
        stop('Kennung unbekannt ' + kl_)
    need(s_, n_, rx_, 'Zuordnung ' + kl_)
for r in A:
    key = (r['studie'], r['satz'])
    if (CAND.search(r['text']) or RESP.search(r['text']) or cand2(r['text'])) and key not in ZUO:
        stop('Kandidat paralleler Werte ohne Handurteil: ' + key[0] + ' ' + key[1])
    if key in ZUO and not (CAND.search(r['text']) or RESP.search(r['text']) or cand2(r['text'])):
        stop('Handurteil ohne Kandidat: ' + key[0] + ' ' + key[1])
def zuo(tag, kern):
    return [k for k, v in ZUO.items() if tag in v[0].split() and ((k[0] in KERN) == kern)]
folgeK, folgeE = zuo('FO', True), zuo('FO', False)
vorig = zuo('VS', True) + zuo('VS', False)
bezK, bezE = zuo('BZ', True), zuo('BZ', False)
zwK, zwE = zuo('ZW', True), zuo('ZW', False)
zoK, zoE = zuo('ZO', True), zuo('ZO', False)
grK = zuo('GR', True)
gleichK = zuo('GL', True)
respWerteK = [(r['studie'], r['satz']) for r in respK if 'ZW' in ZUO[(r['studie'], r['satz'])][0].split()]
respObjK = [(r['studie'], r['satz']) for r in respK if 'ZO' in ZUO[(r['studie'], r['satz'])][0].split()]
respWerte = [lab(*k) for k in respWerteK]
respObj = [lab(*k) for k in respObjK]
P('5 Zuordnung paralleler Werte (‹resp›, ‹zuo›)')
P('  „respectively“ im Kern:', len(respK_streng), 'Saetze in', len(dict.fromkeys(r['studie'] for r in respK_streng)), 'Studien, mit „respectfully“ (Beato 1.1)', len(respK), 'in', len(respKst), '(' + ', '.join(lab(r['studie'], r['satz']) for r in respK) + ')')
P('  davon Werte:', len(respWerte), '(' + ', '.join(respWerte) + ') · Objekte:', len(respObj), '(' + ', '.join(respObj) + ')')
P('  „respective“ zusaetzlich: Hammami 1.3')
P('  erweitert:', len(respE), 'Saetze in', len(respEst), 'Studien (' + nm(respEst) + ')')
P('  Handurteil je Kandidat (verbundene Zahlen, Zuordnungswort, zwei Klammern mit Statistik oder zwei Glieder „Bezeichnung: Wert“):')
for (s_, n_), (kl_, rx_) in sorted(ZUO.items(), key=lambda x: (A.index(IDX[x[0]]))):
    P('   ', ('Kern ' if s_ in KERN else 'erw. ') + lab(s_, n_), '|', ' + '.join(ZTAGS[x] for x in kl_.split()), '|', kurz(s_, n_, 110))
P('  Kern: Bezeichnung je Wert', len(bezK), 'Saetze in', len({s_ for s_, n_ in bezK}), 'Studien (' + liste(bezK) + ') · Zuordnungswort fuer Werte', len(zwK), 'in', len({s_ for s_, n_ in zwK}), '(' + liste(zwK) + ') · fuer Objekte', len(zoK), '(' + liste(zoK) + ') · Gleichheitszeichen', len(gleichK), '(' + liste(gleichK) + ') · Folge mit Bezugsfolge im Satz', len(folgeK), '(' + liste(folgeK) + ') · Grenzfall', len(grK), '(' + liste(grK) + ')')
P('  erweitert: Bezeichnung je Wert', len(bezE), 'Saetze in', len({s_ for s_, n_ in bezE}), 'Studien · Zuordnungswort fuer Werte', len(zwE), '· fuer Objekte', len(zoE), '(' + liste(zoE) + ') · Folge mit Bezugsfolge im Satz', len(folgeE), '(' + liste(folgeE) + ')')
P('  Folge mit Bezugsfolge im vorigen Satz:', len(vorig))
P('')
row(key='resp', pot='Zuordnung in A2 S4 (2c.8, 2c.47, 2b.34)',
    mass='Korpus', fund='Befund § 3.6 · 2c.47, 2b.34',
    aussage=zit('Befund § 3.6', '„respectively“ ordnet parallele Werte Gruppen oder Tests zu (8 Sätze in 5 Studien).') + ' · ' + zit('2c.47', 'Parallele Werte ordnet der Kern mit „respectively“ zu (8 Sätze in 5 Kernstudien, erweitert in 6 Studien)'),
    zahl='Kern 8 Sätze in 5 Studien, erweitert 6 Studien',
    nach='„respectively“ im Kern {} Sätze in {} Studien, mit dem Schreibfehler „respectfully“ (Beato 1.1) {} in {}. Davon ordnen {} Werte zu ({}), {} Objekte ({}). Mit „respective“ (Hammami 1.3) steht ein Zuordnungswort für Werte im Kern in {} Sätzen aus {} Studien. Erweitert {} Sätze in {} Studien.'.format(
        len(respK_streng), len(dict.fromkeys(r['studie'] for r in respK_streng)), len(respK), len(respKst), len(respWerte), liste(respWerteK), len(respObj), liste(respObjK), len(zwK), len({s_ for s_, n_ in zwK}), len(respE), len(respEst)),
    erg='ungenau (zwei der acht Sätze ordnen Objekte zu)',
    folge='Werte ordnet der Kern am häufigsten über eine Bezeichnung je Wert zu (‹zuo›), ein Zuordnungswort steht in {} Sätzen aus {} Studien. Für A2 S4 ist das Zuordnungswort eine von drei belegten Lösungen, nicht die mit der breitesten Kernbasis.'.format(len(zwK), len({s_ for s_, n_ in zwK})),
    beleg='nachzaehlung_2d.txt § 5')
row(key='zuo', pot='Zuordnung in A2 S4 (2c.8, 2c.47, 2b.34)',
    mass='Korpus', fund='2c.47, 2c.8',
    aussage=zit('2c.47', 'mit „=“ (Lloyd 1.3) oder mit Bezeichnungen in der Klammer (Aloui 3.1, 4.1)') + ' · ' + zit('2c.47', 'Erweitert ordnet Klusemann auch über die Folge ohne Zuordnungswort zu, die Bezugsfolge im selben Satz (2.3, 2.5, 4.1)') + ' · ' + zit('2c.47', 'Nur A2 S4 ordnet die Paare „neun und zwei“ und „neun und einer“ über die Folge der Schwellen zu, deren Bezugsfolge im vorigen Satz steht (A2 S3), dafür hat der Korpus kein Vorbild.'),
    zahl='„=“ 1, Bezeichnungen Aloui 3.1 und 4.1, Folge erweitert (3), Bezugsfolge im vorigen Satz 0',
    nach='Kern: „=“ {} ({}). Bezeichnung je Wert {} Sätze in {} Studien ({}). Folge ohne Zuordnungswort mit Bezugsfolge im selben Satz {} ({}). Grenzfälle mit einem benannten Wert und einem Sammelwert {} ({}). Erweitert: Bezeichnung je Wert {} Sätze in {} Studien, Folge {} ({}). Bezugsfolge im vorigen Satz: {}.'.format(
        len(gleichK), liste(gleichK), len(bezK), len({s_ for s_, n_ in bezK}), liste(bezK), len(folgeK), liste(folgeK), len(grK), liste(grK), len(bezE), len({s_ for s_, n_ in bezE}), len(folgeE), liste(folgeE), len(vorig)),
    erg='ungenau (häufigste Kernform ist die Bezeichnung je Wert, die Folge hat auch der Kern, Aloui 5.1)',
    folge='Für A2 S4 bestätigt: Die Bezugsfolge im vorigen Satz hat kein Vorbild. Häufigste Kernform ist die Bezeichnung je Wert ({} Sätze in {} Studien), dann das Zuordnungswort ({} in {}), die Folge mit der Bezugsfolge im selben Satz hat der Kern einmal (Aloui 5.1). Lösbar mit einer Bezeichnung je Wert (wie A2 S3), einem Zuordnungswort oder der Bezugsfolge im Satz, jede Lösung kostet Wörter.'.format(len(bezK), len({s_ for s_, n_ in bezK}), len(zwK), len({s_ for s_, n_ in zwK})),
    beleg='nachzaehlung_2d.txt § 5')

# ---------- 6 Befundbloecke und Themenanker (2d.9, 2d.10) ----------
# Blockdefinition nach Befund 3.3 in Worten: Folge von Befundsaetzen (Primaercode B) im selben Absatz mit derselben
# ersten Zielgroesse, ein Satz ohne B-Code beendet den Block. Eigene Umsetzung.
# Ordnung der Befundsaetze je Kernstudie: einzelne Zielgroesse gegen alle oder mehrere (zg X oder mit +)
ORD = collections.OrderedDict((k, []) for k in ('Zielgröße', 'Schritt', 'eine'))
ORDZ = {}
for st in KERN:
    bz = [x['zg'] or 'X' for x in A if x['studie'] == st and x['primaer'].startswith('B')]
    single = [z for z in bz if z != 'X' and '+' not in z]
    multi = len(bz) - len(single)
    laeufe = [z for i, z in enumerate(single) if i == 0 or single[i - 1] != z]
    if multi * 2 > len(bz):
        art = 'Schritt'
    elif len(set(single)) >= 2 and len(laeufe) == len(set(single)):
        art = 'Zielgröße'
    else:
        art = 'eine'
    ORD[art].append(lab(st, '').strip())
    ORDZ[st] = (art, ' '.join(bz), len(bz), multi)
bouaZ = [x['zg'] or 'X' for x in A if x['studie'] == 'Bouafif2026' and x['primaer'].startswith('B')]
bouaX = next(i for i, z in enumerate(bouaZ) if z != 'X')
if [lab(st, '').strip() for st in KERN if ORDZ[st][0] == 'Zielgröße'] != ['Lloyd', 'Hammami', 'Aloui', 'Liu', 'Moran', 'Bouafif']:
    stop('Ordnung nach Zielgroesse')
BLOCKS = []
for st in KERN:
    prev = None
    for r in [x for x in A if x['studie'] == st]:
        if not r['primaer'].startswith('B'):
            prev = None
            continue
        zg1 = r['zg'].split('+')[0] if r['zg'] else 'X'
        key = (zg1, r['absatz'])
        if key != prev:
            BLOCKS.append((st, r['satz']))
        prev = key
# Handurteil je Blockbeginn mit Pruefausdruck. Vorrang wie Befund 3.3: Konnektor, Themenanker, Sammelbefund (B4),
# Zeitangabe, Modellterm, Quantor (Einzelbefund), Gruppe, sonst Zielgroesse, Befund oder Analyse.
BK = {
 ('Lloyd2016', '1.2'): ('Sammelbefund', r'^Irrespective of maturation, none of'),
 ('Lloyd2016', '2.1'): ('Modellterm', r'^Significant main effects'),
 ('Lloyd2016', '3.1'): ('Modellterm', r'showed main effects'),
 ('Lloyd2016', '4.1'): ('Sammelbefund', r'^Although within-group analysis'),
 ('Lloyd2016', '4.3'): ('Konnektor', r'^However,'),
 ('Hammami2016', '1.1'): ('Sammelbefund', r'^The control group did not show any'),
 ('Hammami2016', '1.2'): ('Konnektor', r'^However,'),
 ('Hammami2016', '1.3'): ('Quantor', r'^None of the 3 agility tests'),
 ('Hammami2016', '1.4'): ('Zielgroesse, Befund oder Analyse', r'^Two of the 3 RCOD scores'),
 ('Beato2018', '4.1'): ('Zeitangabe', r'^After 6 weeks of training,'),
 ('Beato2018', '4.2'): ('Sammelbefund', r'^All the other tests'),
 ('Negra2019', '2.1'): ('Zielgroesse, Befund oder Analyse', r'^Within-group analyses'),
 ('Negra2019', '2.2'): ('Gruppe', r'^In the same group,'),
 ('Negra2019', '2.4'): ('Themenanker', r'^For the ICoD,'),
 ('Negra2019', '2.5'): ('Zielgroesse, Befund oder Analyse', r'^The performance improvement for the SLJ'),
 ('Negra2019', '2.6'): ('Zielgroesse, Befund oder Analyse', r'^Outcomes of the between-group analyses'),
 ('Negra2019', '2.7'): ('Konnektor', r'^However,'),
 ('Negra2019', '2.8'): ('Themenanker', r'^For the remaining tests'),
 ('Negra2020', '1.4'): ('Sammelbefund', r'^After training, the RTG'),
 ('Aloui2022', '2.1'): ('Modellterm', r'^There were interaction effects'),
 ('Aloui2022', '3.1'): ('Modellterm', r'^There was a training effect'),
 ('Aloui2022', '4.1'): ('Modellterm', r'^There was a training effect'),
 ('Aloui2022', '5.1'): ('Themenanker', r'^For the ability to perform RSS,'),
 ('Aloui2022', '6.1'): ('Modellterm', r'^There was a training effect'),
 ('Liu2024', '2.1'): ('Modellterm', r'main effect of time'),
 ('Liu2024', '3.1'): ('Modellterm', r'main effect of time'),
 ('Liu2024', '4.1'): ('Modellterm', r'main effect of time'),
 ('Moran2024', '1.5'): ('Zielgroesse, Befund oder Analyse', r'^Effect sizes'),
 ('Moran2024', '1.7'): ('Zielgroesse, Befund oder Analyse', r'^Moderate effects'),
 ('Moran2024', '1.8'): ('Zielgroesse, Befund oder Analyse', r'^Largely equivalent small effects'),
 ('Sammoud2024', '2.1'): ('Zielgroesse, Befund oder Analyse', r'^A significant large between-group difference'),
 ('Sammoud2024', '3.1'): ('Themenanker', r'^Regarding the asymmetry scores,'),
 ('Bouafif2026', '1.1'): ('Sammelbefund', r'^All performances'),
 ('Bouafif2026', '1.4'): ('Zielgroesse, Befund oder Analyse', r'^Post hoc comparison revealed'),
 ('Bouafif2026', '2.1'): ('Zielgroesse, Befund oder Analyse', r'^Jump performance'),
 ('Bouafif2026', '2.3'): ('Konnektor', r'^Also,'),
 ('Bouafif2026', '3.1'): ('Themenanker', r'^About asymmetry,'),
 ('Bouafif2026', '4.1'): ('Zielgroesse, Befund oder Analyse', r'^Post hoc comparison revealed'),
}
if set(BK) != set(BLOCKS):
    stop('Blockliste und Handurteil verschieden')
for (s, n), (kl, rx) in BK.items():
    need(s, n, rx, 'Blockbeginn ' + kl)
    if kl == 'Sammelbefund' and IDX[(s, n)]['primaer'] != 'B4':
        stop('Sammelbefund ohne B4 ' + s + ' ' + n)
    if kl != 'Sammelbefund' and IDX[(s, n)]['primaer'] == 'B4' and kl not in ('Themenanker', 'Konnektor'):
        stop('B4 nicht als Sammelbefund ' + s + ' ' + n)
bk = collections.Counter(v[0] for v in BK.values())
konn = collections.Counter(re.match(r'^(\w+),', T(s, n)).group(1) for (s, n), v in BK.items() if v[0] == 'Konnektor')
doppel = [('Negra2019', '2.8', 'Themenanker und Sammelbefund (B4)'), ('Negra2020', '1.4', 'Zeitangabe und Sammelbefund (B4)'), ('Lloyd2016', '1.2', 'vorangestellte Einschraenkung und Sammelbefund (B4)')]
for s, n, w in doppel:
    if IDX[(s, n)]['primaer'] != 'B4':
        stop('Doppelzuordnung ' + s + ' ' + n)
quantB4 = [(s, n) for (s, n), v in BK.items() if v[0] == 'Sammelbefund' and re.match(r'^All\b', T(s, n))]
# Themenanker am Satzanfang im Kern: Handliste mit Pruefausdruck
TA = {
 ('Lloyd2016', '2.2'): r'^For both indices of sprinting,', ('Lloyd2016', '2.3'): r'^For acceleration,', ('Lloyd2016', '3.2'): r'^For both jumping variables,',
 ('Negra2019', '2.3'): r'^Regarding the LPJT group,', ('Negra2019', '2.4'): r'^For the ICoD,', ('Negra2019', '2.8'): r'^For the remaining tests',
 ('Aloui2022', '5.1'): r'^For the ability to perform RSS,', ('Aloui2022', '6.2'): r'^For the left support leg,',
 ('Liu2024', '2.4'): r'^Considering the within-group differences,', ('Liu2024', '3.4'): r'^Considering the within group differences,', ('Liu2024', '4.4'): r'^Considering the within group differences,',
 ('Sammoud2024', '1.5'): r'^In terms of physical fitness measures,', ('Sammoud2024', '3.1'): r'^Regarding the asymmetry scores,',
 ('Bouafif2026', '3.1'): r'^About asymmetry,',
}
TARX = re.compile(r'^(?:For (?:the|both|acceleration|sprint\w*|jump\w*)\b|Regarding\b|In terms of\b|In reference to\b|About\b|Considering\b|With regard to\b|As for\b|Concerning\b)')
for (s, n), rx in TA.items():
    need(s, n, rx, 'Themenanker')
for r in A:
    if r['studie'] in KERN and TARX.search(r['text']) and (r['studie'], r['satz']) not in TA:
        stop('Themenanker ohne Handurteil ' + r['studie'] + ' ' + r['satz'])
ANKERGRENZ = {('Lloyd2016', '3.6'): r'^In the post-PHV cohort,', ('Negra2019', '2.2'): r'^In the same group,'}
for (s_, n_), rx_ in ANKERGRENZ.items():
    need(s_, n_, rx_, 'Grenzfall Themenanker')
for r in A:
    if r['studie'] in KERN and re.match(r'^In the\b', r['text']) and (r['studie'], r['satz']) not in ANKERGRENZ:
        stop('Satzanfang In the ohne Handurteil ' + r['studie'] + ' ' + r['satz'])
taSt = list(dict.fromkeys(s for s, n in TA))
taBlock = [k for k in TA if k in BK]
P('6 Ordnung, Befundbloecke und Themenanker im Kern (‹ordnung› bis ‹anker›)')
P('  Ordnung der Befundsaetze (Zielgroesse je Befundsatz in der Folge, X = alle oder keine einzelne, + = mehrere):')
for st in KERN:
    P('   ', lab(st, '').strip(), '|', ORDZ[st][0], '|', ORDZ[st][1], '| ueber alle oder mehrere', ORDZ[st][3], 'von', ORDZ[st][2])
P('  nach Zielgroesse', len(ORD['Zielgröße']), '(' + ', '.join(ORD['Zielgröße']) + ') · nach Gruppe oder Analyseschritt', len(ORD['Schritt']), '(' + ', '.join(ORD['Schritt']) + ') · sonst', len(ORD['eine']), '(' + ', '.join(ORD['eine']) + ')')
P('  Bouafif: vorn', bouaX, 'Saetze ueber alle Zielgroessen, im Asymmetrieteil wieder Ba, J, C (siehe § 9)')
P('  Bloecke:', len(BLOCKS))
for k in BLOCKS:
    P('   ', lab(*k), '|', BK[k][0], '|', kurz(k[0], k[1], 90))
P('  Zaehlung:', ', '.join('{} {}'.format(c, n) for c, n in sorted(bk.items(), key=lambda x: -x[1])))
P('  Zielgroesse, Befund, Modellterm oder Analyse zusammen:', bk['Zielgroesse, Befund oder Analyse'] + bk['Modellterm'], '(davon Modellterm', str(bk['Modellterm']) + ')')
P('  Konnektoren:', dict(konn))
P('  Doppelte Zugehoerigkeit (Vorrang wie Befund 3.3):', ', '.join(lab(s, n) + ' ' + w for s, n, w in doppel))
P('  Sammelbefund mit Quantor am Satzanfang:', ', '.join(lab(*k) for k in quantB4))
P('  Themenanker am Satzanfang:', len(TA), 'Saetze in', len(taSt), 'Studien (' + ', '.join(lab(*k) for k in TA) + ')')
P('  davon Blockbeginn:', len(taBlock), '(' + ', '.join(lab(*k) for k in taBlock) + ')')
P('  Grenzfaelle ohne Themenankerformel (Gruppe oder Kohorte am Satzanfang, nach Befund § 3.6 kein Themenanker):', ', '.join(lab(*k) for k in ANKERGRENZ))
P('')
row(key='ordnung', pot='Fall C1 je Zielgröße im Block (2b.9)',
    mass='Korpus', fund='Befund § 3.3, § 0 Nr. 4 · 2b.9',
    aussage=zit('Befund § 3.3', 'Nach Zielgröße geordnet sind 6 von 10 (Lloyd, Hammami, Aloui, Liu, Moran, Bouafif teilweise).') + ' · ' + zit('Befund § 3.3', 'Nach Gruppe oder Analyseschritt über alle Zielgrößen ordnen Negra 2019 (Veränderung je Gruppe, dann Gruppenvergleich), Negra 2020 (Sammelbefunde je Analyseart) und Sammoud') + ' · ' + zit('Befund § 3.3', 'Beato berichtet den Weitsprung und einen Sammelbefund.'),
    zahl='nach Zielgröße 6 (Bouafif teilweise), nach Gruppe oder Analyseschritt 3, Beato 1',
    nach='Regel: nach Zielgröße, wenn die Befundsätze mit einer einzelnen Zielgröße mindestens zwei Zielgrößen nennen, jede in einem zusammenhängenden Lauf, und Sätze über alle oder mehrere Zielgrößen höchstens die Hälfte stellen. Nach Gruppe oder Analyseschritt, wenn diese Sätze mehr als die Hälfte stellen. Nach Zielgröße {} ({}), nach Gruppe oder Analyseschritt {} ({}), sonst {} ({}). Bouafif beginnt mit {} Sätzen über alle Zielgrößen, im Asymmetrieteil kehren Gleichgewicht, Sprung und Richtungswechsel wieder.'.format(
        len(ORD['Zielgröße']), ', '.join(ORD['Zielgröße']), len(ORD['Schritt']), ', '.join(ORD['Schritt']), len(ORD['eine']), ', '.join(ORD['eine']), bouaX),
    erg='bestätigt',
    folge='Beide Ordnungen sind im Kern belegt. Ein Fall je Zielgröße im Block folgte der Mehrheit, die Ordnung nach Analyseschritt hat mit Sammoud (2.1 bis 2.3 je ein Satz über alle Zielgrößen) das nächste ANCOVA-Vorbild. Für 2b.9 entscheiden Plan § 3 Task 11 und die Wortbilanz, nicht der Korpus.',
    beleg='nachzaehlung_2d.txt § 6')
row(key='bloecke', pot='Blockanfänge mit Quantor (2c.46), Fall je Zielgröße im Block (2b.9)',
    mass='Korpus', fund='Befund § 3.3 · 2a.29, 2c.46',
    aussage=zit('Befund § 3.3', 'Von 38 Befundblöcken beginnen 20 mit Zielgröße, Befund, Modellterm oder der Analyse als Satzanfang (9 davon mit einem Modellterm), 6 mit einem Sammelbefund, einer mit einem Quantor über die Tests einer Zielgröße (Hammami 1.3), 5 mit einem Themenanker, 4 mit einem Konnektor (dreimal „However“, einmal „Also“), einer mit einer Zeitangabe (Beato 4.1) und einer mit einer Gruppe.'),
    zahl='38 · 20 (9) · 6 · 1 · 5 · 4 · 1 · 1',
    nach='{} Blöcke: Zielgröße, Befund oder Analyse {} und Modellterm {} (zusammen {}), Sammelbefund {}, Quantor {} ({}), Themenanker {}, Konnektor {} (However {}, Also {}), Zeitangabe {}, Gruppe {}. Doppelt zugehörig und nach dem Vorrang des Befunds gezählt: {}. Quantor heißt hier All- oder Nullquantor („None of the 3 agility tests“), die Teilangabe Hammami 1.4 („Two of the 3 RCOD scores“) zählt wie im Befund zu Zielgröße oder Befund, als Quantor gezählt wären es 2 und 19. Modellterm heißt ein Haupteffekt oder eine Wechselwirkung als Gegenstand des Satzes, auch nach „There was“ oder „Analysis of … showed“ (Lloyd 3.1).'.format(
        len(BLOCKS), bk['Zielgroesse, Befund oder Analyse'], bk['Modellterm'], bk['Zielgroesse, Befund oder Analyse'] + bk['Modellterm'], bk['Sammelbefund'], bk['Quantor'], ', '.join(lab(*k) for k, v in BK.items() if v[0] == 'Quantor'), bk['Themenanker'], bk['Konnektor'], konn['However'], konn['Also'], bk['Zeitangabe'], bk['Gruppe'], ', '.join(lab(s_, n_) for s_, n_, w_ in doppel)),
    erg='bestätigt (mit der Vorrangfolge des Befunds, Quantor als All- oder Nullquantor)',
    folge='Für A5 S3 und A5 S6: Ein All- oder Nullquantor als Einzelbefund eröffnet einen von 38 Blöcken, Mehrheitsform ist Zielgröße, Befund, Modellterm oder Analyse am Satzanfang. Sammelbefunde mit Quantor am Satzanfang: {}.'.format(', '.join(lab(*k) for k in quantB4)),
    beleg='nachzaehlung_2d.txt § 6')
row(key='anker', pot='Blockanfänge mit Quantor (2c.46), Fall je Zielgröße im Block (2b.9)',
    mass='Korpus', fund='Befund § 3.6 · 2c.46, 2b.34',
    aussage=zit('Befund § 3.6', '(14 Sätze in 6 Studien, erweitert durchgehend bei Padrón-Cabo). Einen Befundblock eröffnen sie in 5 von 38 Blöcken (Negra 2019 2.4 und 2.8, Aloui 5.1, Sammoud 3.1, Bouafif 3.1).'),
    zahl='14 · 6, Blockbeginn 5',
    nach='Themenanker am Satzanfang {} Sätze in {} Studien, davon Blockbeginn {} ({}).'.format(len(TA), len(taSt), len(taBlock), ', '.join(lab(*k) for k in taBlock)),
    erg='bestätigt',
    folge='Ein Block je Zielgröße mit Themenanker (wie A5 S5 „Beim 505-Seitenmittel“) ist im Kern belegt, als Blockbeginn selten (5 von 38).',
    beleg='nachzaehlung_2d.txt § 6')

# ---------- 7 Modellergebnis und unadjustierter Schaetzer (2d.11, 2d.12) ----------
# Handurteil: je Studie mit Modellergebnis und Vergleichen einzelner Gruppen der erste Satz jeder Art
K4 = {
 'Lloyd2016': (('2.1', r'main effects'), ('2.4', r'improved in all 3 training groups'), 'Modellergebnis zuerst'),
 'Liu2024': (('2.1', r'main effect of time'), ('2.3', r'significantly different from HIIT'), 'Modellergebnis zuerst'),
 'Bouafif2026': (('1.1', r'F ≥ 4\.3'), ('1.4', r'Post hoc comparison revealed'), 'Modellergebnis zuerst'),
 'Sammoud2024': (('2.1', r'between-group difference at post-test'), ('2.2', r'the PJT group achieved significant large pre-to-post'), 'Modellergebnis zuerst'),
 'Negra2020': (('1.5', r'No differences were found in the improvements between experimental groups'), ('1.4', r'the RTG showed significant improvements in all tests'), 'Einzelgruppen zuerst'),
}
for st, ((sm, rm), (sg, rg), urteil) in K4.items():
    need(st, sm, rm, 'Modellergebnis')
    need(st, sg, rg, 'Einzelgruppe')
    first_m = A.index(IDX[(st, sm)]) < A.index(IDX[(st, sg)])
    if first_m != (urteil == 'Modellergebnis zuerst'):
        stop('Folge K4 ' + st)
k4ja = [st for st, v in K4.items() if v[2] == 'Modellergebnis zuerst']
# Uebrige Kernstudien: keine zwei Befundarten in eigenen Saetzen nebeneinander (Handurteil mit Pruefausdruck)
K4OHNE = {
 'Hammami2016': ('nur Veraenderung je Gruppe, kein Modellterm', '1.2', r'for the experimental group'),
 'Beato2018': ('nur Gruppenvergleich (ANCOVA), Veraenderung je Gruppe nur in Tab. 1', '4.1', r'than COD-G'),
 'Negra2019': ('Veraenderung je Gruppe vor dem Gruppenvergleich der Veraenderungen (MBI), kein Modellterm', '2.6', r'between-group analyses favored'),
 'Aloui2022': ('Grenzfall: Wechselwirkung mit der Veraenderung der Interventionsgruppe in der Klammer', '3.1', r'with the EG improving more than CG'),
 'Moran2024': ('nur Veraenderung je Gruppe, keine Inferenz', '1.5', r'in every group'),
}
if set(K4) | set(K4OHNE) != set(KERN) or set(K4) & set(K4OHNE):
    stop('K4: Kernstudien nicht vollstaendig zugeordnet')
for st, (art, n_, rx_) in K4OHNE.items():
    need(st, n_, rx_, 'K4 ' + art)
ADJ = re.compile(r'\b(?:unadjusted|adjusted|crude)\b', re.I)
adjK = [r for r in A if r['studie'] in KERN and ADJ.search(r['text'])]
unadjE = [r for r in A if r['studie'] not in KERN and re.search(r'\bunadjusted\b', r['text'])]
beide = [r for r in unadjE if re.search(r'unadjusted IRR', r['text']) and re.search(r'adjusted IRR', r['text'].replace('unadjusted IRR', ''))]
for r in beide:
    t = r['text']
    if not (t.find('unadjusted IRR') < t.replace('unadjusted IRR', 'X' * len('unadjusted IRR')).find('adjusted IRR')):
        stop('Folge unadjustiert vor adjustiert ' + r['satz'])
    if not re.search(r'(?:was|were) [\d.]+ (?:and [\d.]+ )?(?:per 1000 hours of exposure )?in the intervention|smaller in the intervention group compared with the control group', t):
        stop('Werte je Gruppe vor den Schaetzern ' + r['satz'])
beideWerte = [r['satz'] for r in beide if re.search(r'(?:was|were) [\d.]+ (?:and [\d.]+ )?(?:per 1000 hours of exposure )?in the intervention', r['text'])]
beideWorte = [r['satz'] for r in beide if r['satz'] not in beideWerte]
need('Hilska2021', '4.2', r'by 38% in the unadjusted model', 'Hilska 4.2 unadjustiert')
if 'adjusted IRR' in T('Hilska2021', '4.2') or re.search(r'(?<!un)adjusted model', T('Hilska2021', '4.2')):
    stop('Hilska 4.2 nennt ein adjustiertes Modell')
P('7 Modellergebnis, Einzelgruppen und unadjustierter Schaetzer (‹k4›, ‹unadj›)')
for st, ((sm, rm), (sg, rg), urteil) in K4.items():
    P('  ', st, '| Modellergebnis', sm, '| Einzelgruppen', sg, '|', urteil)
P('  Modellergebnis zuerst:', len(k4ja), 'von', len(K4))
for st, (art, n_, rx_) in K4OHNE.items():
    P('   ', NAME[st], '|', art, '(' + n_ + ')')
P('  „unadjusted“, „adjusted“ oder „crude“ im Kern:', len(adjK))
P('  „unadjusted“ erweitert:', ', '.join(lab(r['studie'], r['satz']) for r in unadjE))
P('  beide Schaetzer in einer Klammer, unadjustiert zuerst:', ', '.join(lab(r['studie'], r['satz']) for r in beide), '· nach den Inzidenzen je Gruppe:', ', '.join(beideWerte), '· nach einem Vergleich in Worten:', ', '.join(beideWorte))
for r in beide:
    P('   ', lab(r['studie'], r['satz']), '|', kurz(r['studie'], r['satz'], 230))
P('')
row(key='k4', pot='Unadjustiert vor dem Modellergebnis (2b.6, 2c.17, 2c.43)',
    mass='Korpus', fund='Befund § 6.2 K4, § 3.3 · 2b.6',
    aussage=zit('Befund § 6.2 K4', 'Das Modellergebnis vor Vergleiche einzelner Gruppen stellen', '4 von 5 (Lloyd innerhalb der Zielgrößenblöcke)') + ' · ' + zit('Befund § 3.3', 'Ausnahme Negra 2020: erst die Veränderungen je Gruppe, dann der Gruppenvergleich.'),
    zahl='4 von 5',
    nach='Modellergebnis vor den Einzelgruppen in {} von {} ({}), Einzelgruppen zuerst bei Negra 2020 ({} vor {}). Die übrigen fünf Kernstudien haben keine zwei Befundarten in eigenen Sätzen nebeneinander, Grenzfall Aloui mit der Veränderung der Interventionsgruppe in der Klammer des Modellsatzes (Protokoll § 7).'.format(len(k4ja), len(K4), nm(k4ja), K4['Negra2020'][1][0], K4['Negra2020'][0][0]),
    erg='bestätigt',
    folge='K4 ordnet Modellergebnis und Einzelgruppen, nicht unadjustiert und adjustiert. Für A5 S3 trägt K4 nur die Grundfigur „Modellergebnis zuerst“, das Vorbild für die Folge der Schätzer steht in ‹unadj›.',
    beleg='nachzaehlung_2d.txt § 7')
row(key='unadj', pot='Unadjustiert vor dem Modellergebnis (2b.6, 2c.17, 2c.43)',
    mass='Korpus', fund='Befund § 3.7 · 2c.43, 2c.17',
    aussage=zit('Befund § 3.7', 'unadjustierter neben adjustiertem Schätzer 0 (erweitert: Hilska, IRR mit 95-%-KI)') + ' · ' + zit('2c.43', 'Kern 0, erweitert Hilska 3.3, 4.1 und 6.4 (beide Schätzer mit 95-%-KI in einer Klammer, nach den Inzidenzen je Gruppe)'),
    zahl='Kern 0, erweitert 3 Sätze',
    nach='Kern {} Sätze mit „unadjusted“, „adjusted“ oder „crude“. Erweitert „unadjusted“ in {} Sätzen ({}), beide Schätzer in einer Klammer in {} ({}), jeweils der unadjustierte zuerst, nach den Inzidenzen je Gruppe in {}, nach einem Vergleich in Worten ohne Werte je Gruppe in {}. Hilska 4.2 nennt nur das unadjustierte Modell.'.format(
        len(adjK), len(unadjE), ', '.join(r['satz'] for r in unadjE), len(beide), ', '.join(r['satz'] for r in beide), ' und '.join(beideWerte), ', '.join(beideWorte)),
    erg='ungenau (2c.43: Hilska {} ohne Inzidenzen je Gruppe, Befund § 3.7 bestätigt)'.format(', '.join(beideWorte)),
    folge='Das einzige Vorbild stellt beide Schätzer in denselben Satz, den unadjustierten zuerst, meist nach den Werten je Gruppe. Ein eigener Satz zum unadjustierten Vergleich vor dem Modellergebnis (A5 S3) hat kein Vorbild. Hilska zu folgen hieße beide Werte im Satz, Kapitel 5 führt sie in Tab. 3 und nennt im Satz die Richtung. Vormerkung für 2c.43: „nach den Inzidenzen je Gruppe“ gilt für {}, nicht für {}.'.format(' und '.join(beideWerte), ', '.join(beideWorte)),
    beleg='nachzaehlung_2d.txt § 7')

# ---------- 8 Schluss und Stellung von V2, V1, Z1 (2d.13 bis 2d.16) ----------
def letzter(st):
    return [x for x in A if x['studie'] == st][-1]
def lage(st, r):
    rr = [x for x in A if x['studie'] == st]
    b = [i for i, x in enumerate(rr) if x['primaer'].startswith('B')]
    i = rr.index(r)
    return 'vor dem ersten Befund' if i < b[0] else ('nach dem letzten Befund' if i > b[-1] else 'im Befundteil')
OBJ = re.compile(r'\b(?:Table|Tables|Fig|Figs|Figure|Figures|figure)\s+\d')
KL_END = re.compile(r'\((?:[^()]*' + SK + r'\s*)?(?:see\s+)?(?:Table|Tables|Fig|Figure|figure)\s+\d[^()]*\)\s*\.?\s*$')
endK = {st: letzter(st) for st in KERN}
endE = {st: letzter(st) for st in EXT}
lastB = [st for st, r in endK.items() if r['primaer'].startswith('B')]
lastX = [st for st, r in endK.items() if r['primaer'].startswith('X')]
lastObj = [st for st, r in endK.items() if OBJ.search(r['text'])]
lastKl = [st for st, r in endK.items() if KL_END.search(r['text'])]
lastZ = [st for st, r in list(endK.items()) + list(endE.items()) if r['primaer'].startswith('Z')]
lastO_E = [st for st, r in endE.items() if r['primaer'].startswith('O')]
need('Aloui2022', '6.2', r'Table 5\)\.$', 'Aloui 6.2 Klammer am Satzende')
V2 = [(r['studie'], r['satz'], 'primaer' if r['primaer'] == 'V2' else 'sekundaer', lage(r['studie'], r)) for r in A if has(r, 'V2')]
V1 = [(r['studie'], r['satz'], 'primaer' if r['primaer'] == 'V1' else 'sekundaer', lage(r['studie'], r)) for r in A if has(r, 'V1')]
Z1 = [(r['studie'], r['satz'], 'primaer' if r['primaer'] == 'Z1' else 'sekundaer', lage(r['studie'], r)) for r in A if has(r, 'Z1')]
v2nach = [x for x in V2 if x[3] == 'nach dem letzten Befund']
v1K = [x for x in V1 if x[0] in KERN]
hyp = [r for r in A if re.search(r'hypothes', r['text'], re.I)]
SUMM = re.compile(r'\b(?:in summary|overall|taken together|in conclusion|to summari[sz]e|collectively|in sum)\b', re.I)
summ = [r for r in A if SUMM.search(r['text'])]
need('Veith2021', '2.3', r'ROG impacted upon the statistical model assessing EH-S', 'Veith 2.3 Modellpruefung')
if not (IDX[('Veith2021', '2.3')]['zg'] == IDX[('Veith2021', '2.4')]['zg'] == IDX[('Veith2021', '2.5')]['zg'] == 'K'):
    stop('Veith 2.3 vor dem Block der Zielgroesse')
P('8 Schluss, Resuemee, Hypothese und Stellung von Analyseregel, Datenpruefung und Zusatzanalysen (‹schluss› bis ‹v1z1›)')
for st, r in list(endK.items()) + list(endE.items()):
    P('  ', ('Kern ' if st in KERN else 'erw. ') + st, 'letzter Satz', r['satz'], r['primaer'] + ('(' + ','.join(sec(r)) + ')' if sec(r) else ''), '| Objekt', 'ja' if OBJ.search(r['text']) else 'nein', '| Klammer am Satzende', 'ja' if KL_END.search(r['text']) else 'nein')
P('  Kern: letzter Satz B', len(lastB), '· X', len(lastX), '(' + ', '.join(lastX) + ') · mit Objektverweis', len(lastObj), '· Klammer am Satzende', len(lastKl), '(' + ', '.join(lastKl) + ')')
P('  letzter Satz mit Z-Primaercode (alle 16):', len(lastZ), '· erweitert O-Satz', len(lastO_E), '(' + ', '.join(lastO_E) + ')')
P('  V2:', ', '.join('{} {} {} {}'.format(lab(s, n), a, '·', l) for s, n, a, l in V2))
P('  V2 nach dem letzten Befund:', len(v2nach))
P('  V1:', ', '.join('{} {} {} {}'.format(lab(s, n), a, '·', l) for s, n, a, l in V1), '· Kern', len(v1K))
P('  Z1:', ', '.join('{} {} {} {}'.format(lab(s, n), a, '·', l) for s, n, a, l in Z1))
P('  Veith 2.3 (Modellpruefung fuer EH-S) steht am Anfang des EH-S-Blocks, vor 2.4 und 2.5.')
P('  „hypothes…“ in', len(hyp), 'von', len(A), 'Saetzen · zusammenfassende Wendungen in', len(summ))
P('')
row(key='schluss', pot='Schluss mit dem Z1-Satz (2b.13, 2c.35)',
    mass='Korpus', fund='Befund § 2.1, § 6.2 K10 · 2b.13',
    aussage=zit('Befund § 2.1', '8 von 10: Rahmen vor dem ersten Befund, letzter Satz ist ein Befundsatz (die übrigen zwei enden mit einem Objektsatz).', '7 von 10: der letzte Satz verweist auf ein Objekt, 5 davon in der Klammer am Satzende.'),
    zahl='8 · 2 · 7 · 5',
    nach='Letzter Satz B-Code {}, Objektsatz {} ({}), mit Objektverweis {}, Klammer am Satzende {} ({}).'.format(len(lastB), len(lastX), nm(lastX), len(lastObj), len(lastKl), nm(lastKl)),
    erg='bestätigt',
    folge='A6 S4 hat die Klammer am Satzende wie 5 von 10, ist nach dem Codebuch aber kein Befundsatz (‹zschluss›).',
    beleg='nachzaehlung_2d.txt § 8')
row(key='zschluss', pot='Schluss mit dem Z1-Satz (2b.13, 2c.35)',
    mass='Korpus', fund='2b.13',
    aussage=zit('2b.13', 'Kein Kern-Ergebnisteil endet mit einem Z-Satz (Befundsatz 8, Objektsatz 2, Klammer am Satzende 5), erweitert enden vier mit einem O-Satz.'),
    zahl='Z am Schluss 0, erweitert O-Satz 4',
    nach='Letzter Satz mit Z-Primärcode {} von 16. Erweitert O-Satz {} ({}), die übrigen {}.'.format(len(lastZ), len(lastO_E), nm(lastO_E), ', '.join(lab(endE[st]['studie'], endE[st]['satz']) + ' (' + endE[st]['primaer'] + (' mit ' + ', '.join(sec(endE[st])) if sec(endE[st]) else '') + ')' for st in EXT if st not in lastO_E)),
    erg='bestätigt',
    folge='Ein Schluss mit Z1 hat kein Vorbild. Erweitert schließen Orientierungssätze nach den Befunden (Umsetzung, Messgüte, Begleitbedingungen).',
    beleg='nachzaehlung_2d.txt § 8')
row(key='resuemee', pot='Schluss und Entscheidung über H0 (2b.30)',
    mass='Korpus', fund='Befund § 0 Nr. 4, § 2.1 · 2b.30',
    aussage=zit('Befund § 0 Nr. 4', 'Kein Ergebnisteil endet mit einem Resümee, keiner entscheidet über eine Hypothese.') + ' · ' + zit('Befund § 2.1', '10 von 10: kein Beleg, kein Resümee über die Studie, keine Entscheidung über eine Hypothese.'),
    zahl='10 von 10',
    nach='„hypothes…“ in {} von {} Sätzen. Zusammenfassende Wendungen („in summary“, „overall“, „taken together“, „in conclusion“, „to summarize“, „collectively“, „in sum“) in {}. Letzter Satz im Kern Befundsatz {} oder Objektsatz {} (‹schluss›), erweitert Orientierungssatz {} von {} (‹zschluss›).'.format(
        len(hyp), len(A), len(summ), len(lastB), len(lastX), len(lastO_E), len(EXT)),
    erg='bestätigt',
    folge='A5 S10 (Entscheidung über H0) hat kein Vorbild, sie steht nach P7 (Register 4a). A6 S4 fasst die Absicherung zusammen, nicht die Studie (2b.30). Ein Potenzial, das P7 zurücknähme, bräuchte einen neuen Grund.',
    beleg='nachzaehlung_2d.txt § 8')
row(key='v2', pot='A5 S11 nach den Befunden (2b.28, 2b.30, 2c.25)',
    mass='Korpus', fund='2b.28 · 2c.25',
    aussage=zit('2b.28', 'Analyseregeln (V2) stehen vorn (Rogers 1.2, 1.9, sekundär Sammoud 1.1, Klusemann 1.5) oder im Befundteil (Hilska 6.1, Veith 2.3, sekundär Lloyd 1.3), nie nach dem letzten Befund.'),
    zahl='V2 7 Sätze, nach dem letzten Befund 0',
    nach='V2 primär oder sekundär in {} Sätzen, {}.'.format(len(V2), nach_lage(V2)),
    erg='bestätigt',
    folge='A5 S11 (V2) nach der Entscheidung über H0 hat kein Vorbild, eine Stellung vor den Befunden oder im Befundteil hätte eines.',
    beleg='nachzaehlung_2d.txt § 8')
row(key='v1z1', pot='Schluss mit dem Z1-Satz (2b.13, 2c.35), Einschränkung des 30-m-Befunds (2b.12)',
    mass='Korpus', fund='Befund § 6.4, § 3.7 · 2b.28, 2c.35',
    aussage=zit('Befund § 6.4', 'keine Stellungsregel für Voraussetzungen und Sensitivität (im Kern nie berichtet, erweitert vorn oder im Befundteil)') + ' · ' + zit('2b.28', 'Der Kern hat keine Datenprüfung und keine Sensitivitätsanalyse, Z1 steht dort nur sekundär in Objektsätzen zu Einzelwertdarstellungen (Moran 1.1 bis 1.3 vorn, Liu 2.5 im Befundteil).') + ' · ' + zit('2b.28', 'Erweitert steht die Datenprüfung vorn (Veith 1.1, Asimakidis 1.1) oder mit einer Analyseregel im Befundteil (Hilska 6.1, Veith 2.3), Zusatzanalysen stehen vorn als Objektsatz (Rogers 1.3, 1.8), im Befundteil (Hilska 4.2, Rogers 2.1, 2.3, 2.4) oder danach (Asimakidis 1.6).'),
    zahl='V1 Kern 0, erweitert 4 · Z1 Kern 4 sekundär, erweitert 7, danach 1',
    nach='Lage nach dem Primärcode B. V1 Kern {}, alle {} Sätze, {}. Z1 in {} Sätzen, {}. Z1 im Kern nur sekundär in Objektsätzen ({}). Nach dem letzten Befund nur {} (Primärcode {}, sekundär {}, Einzelreaktionen), darauf folgt {} ({}). Veith 2.3 steht am Anfang des Blocks der Zielgröße, deren Modell er prüft.'.format(
        len(v1K), len(V1), nach_lage(V1), len(Z1), nach_lage(Z1), ', '.join(lab(s, n) + ' ' + IDX[(s, n)]['primaer'] for s, n, a, l in Z1 if s in KERN), ', '.join(lab(s, n) for s, n, a, l in Z1 if l == 'nach dem letzten Befund'), IDX[('Asimakidis2022', '1.6')]['primaer'], ', '.join(sec(IDX[('Asimakidis2022', '1.6')])), lab('Asimakidis2022', '1.7'), IDX[('Asimakidis2022', '1.7')]['primaer']),
    erg='ungenau (§ 6.4: Z1 erweitert auch nach dem letzten Befund, 2b.28 bestätigt)',
    folge='Eine Zusatzanalyse nach allen Befunden hat ein erweitertes Vorbild (Asimakidis 1.6), keine Studie schließt mit ihr. Eine Datenprüfung steht nie nach dem letzten Befund, sondern vorn oder am Block, den sie betrifft (Veith 2.3). Die Stellung von A6 entscheiden Plan § 3 Task 11 und Textvorschlag 5 (2b.28).',
    beleg='nachzaehlung_2d.txt § 8')

# ---------- 9 Folge der Zielgroessen bei Wiederkehr (2d.17) ----------
ZGRX = {'S': re.compile(r'\b(?:sprint\w*|acceleration|maximal running velocity|\d+[- ]?m\b|5-|20-m|10-m)'),
        'C': re.compile(r'\b(?:CoD|change[- ]of[- ]direction|505|agility|S180|SBF|S 4 X 5|ICoD|S90)'),
        'J': re.compile(r'\b(?:jump\w*|CMJ\w*|SJ\b|SLJ|squat jump|reactive strength|long jump|hop\w*|FJT)')}
def zfolge(t):
    t2 = re.sub(r'\bCODJ?-G\b|\bCODJ\b|\bMKD\b|\b\d+[- ]?(?:week|weeks|day|days|hours?)\b', ' ', t)
    pos = {}
    for c, rx in ZGRX.items():
        m = rx.search(t2)
        if m:
            pos[c] = m.start()
    return ''.join(sorted(pos, key=pos.get))
MEHR = [(r['studie'], r['satz'], zfolge(r['text'])) for r in A if r['studie'] in KERN and len(zfolge(r['text'])) >= 2]
# Handkontrolle der Kandidaten mit Pruefausdruck
MEHRH = {
 ('Lloyd2016', '1.1'): ('SJ', r'changes in sprint and jump performances'),
 ('Lloyd2016', '4.3'): ('SJ', r'acceleration and squat jump height'),
 ('Hammami2016', '1.1'): ('SC', r'sprint, agility'),
 ('Negra2019', '2.1'): ('CSJ', r'ICoD, modified 505 CoD, 20-m sprint-time, CMJ'),
 ('Negra2019', '2.3'): ('SC', r'large and very large effect sizes were shown for the 10-m sprint-time and modified 505 CoD tests, respectively'),
 ('Negra2019', '2.4'): ('CSJ', r'For the ICoD, 5- and 20-m sprint-time, CMJ'),
 ('Negra2019', '2.6'): ('CJ', r'modified 505 CoD, SLJ'),
 ('Negra2019', '2.8'): ('CSJ', r'ICoD, 10-m, 20-m, and CMJ'),
 ('Liu2024', '1.1'): ('JS', r'on CMJ .*30-m sprint time'),
 ('Sammoud2024', '2.1'): ('JC', r'CMJ height .*505 CoD'),
 ('Sammoud2024', '2.2'): ('JC', r'CMJ height .*505 CoD'),
 ('Sammoud2024', '2.3'): ('JC', r'CMJ height .*505 CoD'),
 ('Bouafif2026', '1.2'): ('JC', r'all jump tests and for the balance and CoD test'),
 ('Bouafif2026', '1.3'): ('JC', r'jumps with right foot .*CoD with right foot'),
}
if {(s, n) for s, n, f in MEHR} != set(MEHRH):
    stop('Mehrfachnennungen und Handkontrolle verschieden: ' + str(sorted({(s, n) for s, n, f in MEHR} ^ set(MEHRH))))
for s, n, f in MEHR:
    if MEHRH[(s, n)][0] != f:
        stop('Folge ' + s + ' ' + n)
    need(s, n, MEHRH[(s, n)][1], 'Folge der Zielgroessen')
ref = {}
abw = []
for s, n, f in MEHR:
    if s not in ref:
        ref[s] = f
        continue
    r0 = ref[s]
    sub = [c for c in r0 if c in f]
    if ''.join(sub) != ''.join(c for c in f if c in r0):
        abw.append((s, n, f, r0))
# Bloecke: Lloyd S vor J und Wiederkehr in 4.3, Bouafif Gleichgewicht, Sprung, Richtungswechsel und Wiederkehr in 3.1 bis 4.2
BOUA = [('1.4', 'Ba', r'balance'), ('2.1', 'J', r'^Jump performance'), ('2.3', 'C', r'CoD times'), ('3.1', 'Ba', r'balance asymmetry'), ('3.2', 'J', r'^Jumping asymmetry'), ('3.3', 'C', r'change of direction'), ('4.1', 'Ba', r'for balance'), ('4.2', 'J', r'jump performance')]
for n, c, rx in BOUA:
    need('Bouafif2026', n, rx, 'Bouafif Zielgroesse')
need('Lloyd2016', '4.3', r'acceleration and squat jump height', 'Lloyd Wiederkehr')
BOUARANG = {'Ba': 0, 'J': 1, 'C': 2}
for teil in (('1', '2'), ('3',), ('4',)):
    folge_ = [BOUARANG[c] for n, c, rx in BOUA if n.split('.')[0] in teil]
    if folge_ != sorted(folge_):
        stop('Bouafif Folge im Teil ' + '+'.join(teil))
LLOYDLAEUFE = []
for x in A:
    if x['studie'] == 'Lloyd2016' and x['primaer'].startswith('B') and x['zg'] in ('S', 'J'):
        if LLOYDLAEUFE and LLOYDLAEUFE[-1][0] == x['zg']:
            LLOYDLAEUFE[-1][2] = x['satz']
        else:
            LLOYDLAEUFE.append([x['zg'], x['satz'], x['satz']])
if [l_[0] for l_ in LLOYDLAEUFE] != ['S', 'J'] or IDX[('Lloyd2016', '4.3')]['zg'] != 'S+J':
    stop('Lloyd Laeufe')
P('9 Folge der Zielgroessen bei Wiederkehr (‹folge›)')
P('  Blockebene: Lloyd S (2.x) vor J (3.x), Wiederkehr S, J in 4.3 · Bouafif', ' '.join(n + ':' + c for n, c, rx in BOUA))
P('  Satzebene, Kernsaetze mit mindestens zwei von Sprint (S), Richtungswechsel (C), Sprung (J):', len(MEHR), 'in', len({s for s, n, f in MEHR}), 'Studien')
for s, n, f in MEHR:
    P('   ', lab(s, n), f, '|', kurz(s, n, 110))
P('  abweichend von der ersten Aufzaehlung der Studie:', ', '.join('{} {} gegen {}'.format(lab(s, n), f, r0) for s, n, f, r0 in abw))
P('')
row(key='folge', pot='Folge in A4 S2 (2b.8, 2b.7)',
    mass='Korpus', fund='Befund § 3.3, § 6.2 K5 · 2b.7, 2b.8',
    aussage=zit('Befund § 3.3', 'Wo Zielgrößen wiederkehren (Lloyd, Bouafif), kehren sie in derselben Folge wieder.') + ' · ' + zit('Befund § 6.2 K5', 'bei Wiederkehr gleich (geprüft an Lloyd und Bouafif)'),
    zahl='2 Studien, Folge gleich',
    nach='Blockebene: Lloyd {}, beide wieder in 4.3 in derselben Folge. Bouafif {}, in jedem Teil steigend nach Gleichgewicht, Sprung, Richtungswechsel. Satzebene: {} Kernsätze in {} Studien nennen mindestens zwei von Sprint, Richtungswechsel und Sprung. Gegen die erste solche Aufzählung ihrer Studie geprüft, folgen {} der übrigen {} derselben Folge, abweichend {}.'.format(
        ', '.join({'S': 'Sprint', 'J': 'Sprung'}[z_] + ' ' + a_ + ' bis ' + b_ for z_, a_, b_ in LLOYDLAEUFE), ', '.join(n + ' ' + {'Ba': 'Gleichgewicht', 'J': 'Sprung', 'C': 'Richtungswechsel'}[c] for n, c, rx in BOUA),
        len(MEHR), len({s for s, n, f in MEHR}), len(MEHR) - len(ref) - len(abw), len(MEHR) - len(ref), ', '.join('{} ({} gegen {})'.format(lab(s, n), f, r0) for s, n, f, r0 in abw)),
    erg='bestätigt (Blockebene), auf Satzebene eine Ausnahme',
    folge='Eine nach dem Inhalt geordnete Folge in einem Satz hat ein Kernvorbild (Negra 2019 2.3, nach den Größenklassen „large and very large“ mit „respectively“). Ein Potenzial für A4 S2 stützt sich auf F17 § 5.1 (Reihenfolgetreue), nicht auf den Korpus.',
    beleg='nachzaehlung_2d.txt § 9')

# ---------- 10 Umsetzung: Wortwahl, Median, Werte je Teilnehmer (2d.18) ----------
O2K = [r for r in A if r['studie'] in KERN and has(r, 'O2')]
woerter = collections.OrderedDict()
for w in ('compliance', 'attendance', 'completed', 'adherence'):
    woerter[w] = [lab(r['studie'], r['satz']) for r in O2K if re.search(r'\b' + w + r'\b', r['text'], re.I)]
adhE = [lab(r['studie'], r['satz']) for r in A if r['studie'] not in KERN and re.search(r'\badherence\b', r['text'], re.I)]
med = [lab(r['studie'], r['satz']) + ' ' + r['primaer'] for r in A if re.search(r'\bmedian\b', r['text'], re.I)]
adhOhneZahl = all(not re.search(r'\d', r['text']) for r in A if r['studie'] not in KERN and re.search(r'\badherence\b', r['text'], re.I))
need('Rogers2020', '2.5', r'a mean of 9\.6 out of 16 possible lunch time sessions', 'Rogers 2.5')
need('Rogers2020', '2.7', r'logged between 0 and 11 sessions out of a possible 32', 'Rogers 2.7')
need('Hilska2021', '7.1', r'1\.7 per week in a team', 'Hilska 7.1 je Team')
OUTOF = re.compile(r'out of (?:a )?(?:possible )?\d+|\d+ possible\b|of a possible\b')
outof = [(r['studie'], r['satz']) for r in A if OUTOF.search(r['text'])]
if outof != [('Rogers2020', '2.5'), ('Rogers2020', '2.7')]:
    stop('out of possible: ' + str(outof))
werte = re.findall(r'(?<![\d.])(\d{2})\s*%', ' '.join(r['text'] for r in O2K))
P('10 Umsetzung im Korpus (‹umsetzung›)')
P('  O2 im Kern (primaer oder sekundaer):', len(O2K), 'Saetze in', len({r['studie'] for r in O2K}), 'Studien')
for r in O2K:
    P('   ', lab(r['studie'], r['satz']), r['primaer'], '|', kurz(r['studie'], r['satz'], 120))
P('  Wortwahl:', ', '.join('{} {} ({})'.format(w, len(v), ', '.join(v)) for w, v in woerter.items()))
P('  Prozentwerte der Kern-O2-Saetze:', ', '.join(werte), '· kleinster', min(int(x) for x in werte), '· groesster', max(int(x) for x in werte))
P('  „adherence“ erweitert:', ', '.join(adhE))
P('  „median“ im Korpus:', ', '.join(med))
P('  Werte je Teilnehmer mit der angebotenen Zahl: Rogers 2.5, 2.7 · Hilska 7.1 zaehlt je Team und Woche')
P('')
row(key='umsetzung', pot='„6,0 vollständige je Spieler“ in A2 S1 (Register 10u)',
    mass='Korpus', fund='Befund § 3.1 · 2c.5',
    aussage=zit('Befund § 3.1', 'Knapp: Raten je Gruppe (Lloyd, Beato), eine Rate für beide Gruppen (Negra 2019) oder „alle“ (Negra 2020, Sammoud mit „more than 85%“).') + ' · ' + zit('2c.5', '„median“ steht im Korpus nur in einem Objektsatz (Moran 1.2).') + ' · ' + zit('2c.5', 'Erweitert am nächsten sind Spanne und Mittel je Teilnehmer (Rogers 2.5, 2.7, Hilska 7.1)'),
    zahl='Kern 5 Studien, „median“ 1, je Teilnehmer 3 Sätze',
    nach='O2 im Kern {} Sätze in {} Studien, Wortwahl {}, Werte {} bis {} % oder „all“. „adherence“ erweitert {} ({}){}. „median“ {}. Je Teilnehmer mit der angebotenen Zahl („out of … possible“) nur {} im ganzen Korpus, Hilska 7.1 zählt je Team und Woche.'.format(
        len(O2K), len({r['studie'] for r in O2K}), ', '.join('„{}“ {}'.format(w, len(v)) for w, v in woerter.items()), min(int(x) for x in werte), max(int(x) for x in werte), len(adhE), ', '.join(adhE), ', ohne Zahl' if adhOhneZahl else '', ', '.join(med), liste(outof)),
    erg='ungenau (Hilska 7.1 je Team, nicht je Teilnehmer)',
    folge='Der Korpus kennt kein „adherence“ als Bezeichnung eines Werts je Spieler. Am nächsten an A2 S1 ist „x out of a possible N“ (Rogers 2.5, 2.7, erweitert). Die Begriffsbrücke bleibt eine Projektfrage (4.6, Textvorschlag 5 § 9.1 Nr. 4).',
    beleg='nachzaehlung_2d.txt § 10')

# ---------- 11 Sammelbefund, Ausnahmen, Menge des Quantors (2d.19) ----------
b4K = list(dict.fromkeys(r['studie'] for r in A if r['studie'] in KERN and has(r, 'B4')))
b4Kp = list(dict.fromkeys(r['studie'] for r in A if r['studie'] in KERN and r['primaer'] == 'B4'))
b4B = []
b4Bp = []
for st in KERN:
    for satz, prim, sek, zg, deut, memo in CB[st]:
        if prim == 'B4' or 'B4' in [x for x in sek.split(SK) if x]:
            if st not in b4B:
                b4B.append(st)
        if prim == 'B4' and st not in b4Bp:
            b4Bp.append(st)
excK = [lab(r['studie'], r['satz']) + ' ' + r['primaer'] for r in A if r['studie'] in KERN and re.search(r'\bexcept\b', r['text'])]
excB4St = list(dict.fromkeys(r['studie'] for r in A if r['studie'] in KERN and has(r, 'B4') and re.search(r'\bexcept\b', r['text'])))
# Quantorwoerter in Kern-Befundsaetzen: jeder Treffer mit Handurteil ueber den Bereich des Quantors.
# Bereich Tests mit Unterklasse, sonst Gruppen, Seiten, Modellterme, Paarvergleiche oder Einzeltest.
QW = re.compile(r'\b(?:all|any|none|no|nearly all|remaining|rest|both|every|each|neither|either|most|some|several|other|only|(?:one|two|three|four|five|six|\d+) of the)\b', re.I)
QDOM = {
 ('Lloyd2016', '1.2'): ('Tests', 'alle der Studie', r'none of the control groups made any significant changes in performance'),
 ('Lloyd2016', '2.2'): ('Tests', 'Zahl oder Testklasse', r'^For both indices of sprinting,'),
 ('Lloyd2016', '2.4'): ('Gruppen', '', r'in all 3 training groups'),
 ('Lloyd2016', '2.6'): ('Gruppen', '', r'of both pre- and post-PHV cohorts'),
 ('Lloyd2016', '3.1'): ('Modellterme', '', r'for both time and maturity'),
 ('Lloyd2016', '3.2'): ('Tests', 'Zahl oder Testklasse', r'^For both jumping variables,'),
 ('Lloyd2016', '3.3'): ('Tests', 'Liste', r'for both squat jump and reactive strength index'),
 ('Lloyd2016', '3.5'): ('Gruppen', '', r'in all pre-PHV training groups'),
 ('Lloyd2016', '4.1'): ('Tests', 'alle der Studie', r'failed to determine any significant differences in training response'),
 ('Lloyd2016', '4.2'): ('Tests', 'alle der Studie', r'^Nearly all the differences in training responses'),
 ('Hammami2016', '1.1'): ('Tests', 'alle der Studie (vollständige Liste)', r'any significant differences in anthropometric measures, sprint, agility, RSSA, RCOD'),
 ('Hammami2016', '1.3'): ('Tests', 'Zahl oder Testklasse', r'^None of the 3 agility tests'),
 ('Hammami2016', '1.4'): ('Tests', 'Teil mit Liste', r'^Two of the 3 RCOD scores \(RCODbest'),
 ('Hammami2016', '1.5'): ('Einzeltest', '', r'^No significant changes of RSSA performance'),
 ('Beato2018', '4.2'): ('Tests', 'anaphorisch („other“)', r'^All the other tests'),
 ('Negra2019', '2.8'): ('Tests', 'anaphorisch mit Liste („remaining“)', r'^For the remaining tests \(ICoD, 10-m, 20-m, and CMJ\)'),
 ('Negra2020', '1.4'): ('Tests', 'alle der Studie mit Ausnahme', r'in all tests \(p < 0\.05\) except for the 1RM'),
 ('Negra2020', '1.5'): ('Tests', 'alle der Studie mit Ausnahme', r'^No differences were found in the improvements between experimental groups except in the 1RM'),
 ('Aloui2022', '5.1'): ('Tests', 'Teil mit Liste', r'for most of its parameters \(RSSA best and RSSA mean\)'),
 ('Aloui2022', '6.1'): ('Seiten', '', r'on both legs'),
 ('Liu2024', '3.3'): ('Paarvergleiche', '', r'although no other significant differences were found'),
 ('Sammoud2024', '2.3'): ('Tests', 'alle der Studie (vollständige Liste)', r'no significant pre-to-post changes were found for CMJ height .*SLJ .*SHTD-D .*SHTD-ND .*505 CoD'),
 ('Moran2024', '1.5'): ('Gruppen', '', r'in every group'),
 ('Bouafif2026', '1.1'): ('Tests', 'alle der Studie mit Ausnahme', r'^All performances .*except not for the CoD'),
 ('Bouafif2026', '1.2'): ('Tests', 'alle der Studie', r'for all tests .*for all jump tests'),
 ('Bouafif2026', '1.3'): ('Tests', 'alle der Studie mit Ausnahme', r'^Only balance with the right foot showed'),
 ('Bouafif2026', '1.4'): ('Gruppen', '', r'for all groups'),
 ('Bouafif2026', '1.5'): ('Seiten', '', r'in both feet'),
 ('Bouafif2026', '2.2'): ('Gruppen', '', r'both plyometric groups'),
 ('Bouafif2026', '3.1'): ('Modellterme', '', r'while the rest was not significant'),
 ('Bouafif2026', '3.2'): ('Modellterme', '', r'no other effects reached significance'),
 ('Bouafif2026', '3.3'): ('Modellterme', '', r'^No significant effects were found for change of direction over time, training and age'),
 ('Bouafif2026', '4.1'): ('Gruppen', '', r'in both training groups .*while no significant changes were observed in the pre-PHV'),
}
QTREFF = [(r['studie'], r['satz']) for r in A if r['studie'] in KERN and r['primaer'].startswith('B') and QW.search(r['text'])]
if set(QTREFF) != set(QDOM):
    stop('Quantorwoerter und Handurteil verschieden: ' + str(sorted(set(QTREFF) ^ set(QDOM))))
for (s, n), (dom, kl, rx) in QDOM.items():
    need(s, n, rx, 'Quantor ' + dom)
QM = collections.OrderedDict((k, v) for k, v in QDOM.items() if v[0] == 'Tests')
qkl = collections.OrderedDict()
for k, (dom, kl, rx) in QM.items():
    qkl.setdefault(kl, []).append(k)
for k_ in (('Hammami2016', '1.1'), ('Sammoud2024', '2.3')):
    if IDX[k_]['zg'] != 'X':
        stop('vollstaendige Liste ohne zg X ' + k_[0])
for n_ in ('2.1', '2.2'):
    need('Sammoud2024', n_, r'CMJ height .*SLJ .*SHTD-D .*505 CoD', 'Sammoud dieselben Tests')
QALLE = [k for k, v in QM.items() if v[1].startswith('alle der Studie')]
QTEIL = [k for k, v in QM.items() if not v[1].startswith('alle der Studie')]
qand = collections.OrderedDict()
for k, (dom, kl, rx) in QDOM.items():
    if dom != 'Tests':
        qand.setdefault(dom, []).append(k)
P('11 Sammelbefund, Ausnahmen und Menge des Quantors (‹quantor›)')
P('  B4 Konsens Kern (primaer oder sekundaer):', len(b4K), '(' + ', '.join(b4K) + ') · primaer', len(b4Kp))
P('  B4 Codierer B Kern (codes_B.json, primaer oder sekundaer):', len(b4B), '(' + ', '.join(b4B) + ') · primaer', len(b4Bp))
P('  „except“ im Kern:', ', '.join(excK), '· in Sammelbefunden', len(excB4St), 'Studien (' + ', '.join(excB4St) + ')')
P('  Kern-Befundsaetze mit einem Quantorwort (all, any, none, no, remaining, rest, both, every, each, most, some, other, only, „two of the“ u. a.):', len(QDOM))
for (s, n), (dom, kl, rx) in QDOM.items():
    P('   ', lab(s, n), '|', dom + (' · ' + kl if kl else ''), '|', kurz(s, n, 110))
P('  Quantor ueber Tests:', len(QM), 'Saetze in', len({s for s, n in QM}), 'Studien ·', ' · '.join('{} {} ({})'.format(kl, len(v), ', '.join(lab(*k) for k in v)) for kl, v in qkl.items()))
P('  ueber alle Tests der Studie:', len(QALLE), '· ueber einen Teil, Menge in der Nominalphrase (Zahl, Testklasse, Liste, „other“, „remaining“):', len(QTEIL), '· ueber einen Teil nur aus dem Zusammenhang: 0')
P('  Quantor ueber anderes:', ' · '.join('{} {} ({})'.format(d, len(v), ', '.join(lab(*k) for k in v)) for d, v in qand.items()))
P('')
row(key='quantor', pot='Quantor in A5 S6 über „damit“ (2b.11)',
    mass='Korpus', fund='Befund § 3.5, § 6.2 K8 · 2b.11',
    aussage=zit('Befund § 3.5', 'Sammelbefunde (B4) in 6 von 10 (Codierer B: 8, darunter Liu 3.3 mit einem Nebensatz über die übrigen Paarvergleiche einer Zielgröße).') + ' · ' + zit('Befund § 3.5', 'Mit Quantor über alle oder alle übrigen Zielgrößen') + ' · ' + zit('Befund § 3.5', 'Mit Ausnahmeformel „except“ in 2 Studien (Negra 2020 zweimal, Bouafif), dazu Sammoud beim Ausgangsvergleich (1.5).') + ' · ' + zit('Befund § 6.2 K8', 'Sammelbefund mit Quantor, wo er über alle Zielgrößen gilt, Ausnahmen benennen'),
    zahl='6 von 10 (B: 8), „except“ 2 Studien',
    nach='B4 im Kern nach dem Konsens {} Studien, nach Codierer B {} (codes_B.json). „except“ in Sammelbefunden {} Studien ({}), dazu {}. Quantoren über Tests in Kern-Befundsätzen {} Sätze in {} Studien: über alle Tests der Studie {} ({}, darunter vollständige Listen {}), über einen Teil mit der Menge in der Nominalphrase {} ({}), über einen Teil nur aus dem Zusammenhang 0. Die übrigen {} Quantoren gelten Gruppen, Seiten, Modelltermen, Paarvergleichen oder einem Einzeltest.'.format(
        len(b4K), len(b4B), len(excB4St), nm(excB4St), ', '.join(re.sub(r' (\w+)$', r' (\1)', x) for x in excK if not x.endswith(' B4')), len(QM), len({s for s, n in QM}), len(QALLE), liste(QALLE), liste([k for k, v in QM.items() if 'vollständige Liste' in v[1]]), len(QTEIL), liste(QTEIL), len(QDOM) - len(QM)),
    erg='bestätigt',
    folge='Meint ein Kern-Quantor nur einen Teil der Tests, steht die Menge in der Nominalphrase („the 3 agility tests“, „both jumping variables“, „the other tests“, „the remaining tests (…)“ oder eine Liste). A5 S6 bindet „keiner Zielgröße“ nur über „damit“ an die drei konfirmatorischen, dafür hat der Kern kein Vorbild. Eine benannte Menge kostet Wörter.',
    beleg='nachzaehlung_2d.txt § 11')


# ---------- 12 Zitatpruefung und Teiltabelle ----------
verweise()
NR = {r['key']: r['nr'] for r in ROWS}
P('12 Zitatpruefung der Befundstellen (jedes Zitat am genannten Ort, an Wortgrenzen, Leerraum vereinheitlicht, Bruchstuecke in ihrer Folge)')
for ort, q in ZIT:
    P('  ok', ort, '|', q[:110] + (' …' if len(q) > 110 else ''))
P('  Zitate:', len(ZIT), '· Volltextzitate:', len(VQOK))
P('')
erg = collections.Counter(r['erg'].split(' (')[0] for r in ROWS)
P('13 Teiltabelle 2d')
P('  Massstab: Korpus = Satzanlage, Korpus (mit Volltext) = Satzanlage und Methodenteile, Tabellen oder Abbildungen der Volltexte.')
P('  Ergebnis: bestaetigt, wenn Zahl und Aussage zutreffen · abweichend, wenn eine ausdruecklich genannte Zahl oder eine tragende Teilaussage nicht zutrifft · ungenau, wenn die tragende Aussage zutrifft, eine Zahl, Liste oder Abgrenzung aber zu weit, zu eng oder unvollstaendig ist.')
P('  Zeilen:', len(ROWS), '·', ', '.join('{} {}'.format(k, v) for k, v in erg.items()))
for r in ROWS:
    P('  ', r['nr'], '|', r['erg'])

for r in ROWS:
    r['stelle'] = r['mass'] + ' · ' + r['fund']
COLS = [('nr', 'Nr.'), ('pot', 'Potenzial (Schritt 3)'), ('aussage', 'Korpusaussage (Wortlaut am Ort)'), ('stelle', 'Befundstelle'), ('zahl', 'Zahl laut Befund'),
        ('nach', 'Nachzählung'), ('erg', 'Ergebnis'), ('folge', 'Folge für das Potenzial'), ('beleg', 'Beleg')]
OUT.mkdir(parents=True, exist_ok=True)
with open(OUT / 'teiltabelle_2d.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=SK, quoting=csv.QUOTE_ALL, lineterminator='\n')
    w.writerow([c[1] for c in COLS])
    for r in ROWS:
        w.writerow([r[c[0]] for c in COLS])
with open(OUT / 'teiltabelle_2d.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write('| ' + ' | '.join(c[1] for c in COLS) + ' |\n')
    f.write('|' + '---|' * len(COLS) + '\n')
    for r in ROWS:
        cells = [str(r[c[0]]).replace('|', '/') for c in COLS]
        f.write('| ' + ' | '.join(cells) + ' |\n')
txt = '\n'.join(LINES) + '\n'
for ref in re.findall(r'‹(?!SK›)(\w+)›', txt):
    if ref not in NR:
        stop('Verweis im Protokoll unbekannt: ' + ref)
txt = re.sub(r'‹(?!SK›)(\w+)›', lambda m: NR[m.group(1)], txt)
if SK in txt.replace(SKMARK, ''):
    stop('Semikolon im Protokoll')
with open(OUT / 'nachzaehlung_2d.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(txt)
for name in ('teiltabelle_2d.md',):
    if SK in (OUT / name).read_text(encoding='utf-8'):
        stop('Semikolon in ' + name)
print('nachzaehlung_2d: {} Zeilen, {}'.format(len(ROWS), dict(erg)))

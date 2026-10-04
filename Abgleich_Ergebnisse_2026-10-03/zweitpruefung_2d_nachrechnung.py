# zweitpruefung_2d_nachrechnung.py
# Unabhaengige Nachrechnung der Teiltabelle 2d (Zweitpruefung zu Teilschritt 2 d,
# Task "Ergebnisse: Abgleich mit der Argumentationsstruktur und Ueberarbeitung").
# Importiert und kopiert nichts aus nachzaehlung_2d.py. Eigene Definitionen, eigene Ausdruecke,
# Volltexte mit pypdf statt pdftotext. Handurteile stehen mit Begruendung im Skript und sind
# per Pruefausdruck an den Satztext gebunden, eine verletzte Bedingung bricht den Lauf ab.
# Gelesen (nicht ausgefuehrt) werden die Ausgaben von nachzaehlung_2d.py: teiltabelle_2d.csv,
# nachzaehlung_2d.txt und der Quelltext (nur fuer die Konventionspruefung, Abschnitt 17).
# Aufruf: PYTHONDONTWRITEBYTECODE=1 python3 zweitpruefung_2d_nachrechnung.py
# Ausgabe: zweitpruefung_2d_nachrechnung.txt neben dem Skript.
# In der Ausgabe steht [SK] fuer ein Semikolon im zitierten Text. Skript und Ausgabe enthalten kein Semikolon.
import csv, json, re, sys, hashlib, pathlib, collections, unicodedata, logging
logging.disable(logging.CRITICAL)
import pypdf

SK = chr(59)
HERE = pathlib.Path(__file__).resolve().parent
UP = pathlib.Path('/mnt/user-data/uploads/Bachelorarbeit')
C = UP / 'Claude'
PDFDIR = UP / 'Ideen und Studien'
SPIEGEL = HERE.parent / 'spiegel' / 'Bachelorarbeit' / 'Claude' / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03'
LAUF = HERE / 'lauf'
ANL = C / '02_Befunde' / 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02_Saetze.csv'
BEF = C / '02_Befunde' / 'Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md'
ABG = C / '02_Befunde' / 'Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md'
T2B = C / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03' / 'teiltabelle_2b.csv'
T2C = C / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03' / 'teiltabelle_2c.csv'
KO = C / '03_Skripte' / 'Argumentationsstruktur_Ergebnisteile_2026-10-02'
CODB = KO / 'codes_B.json'
QMD5 = KO / 'Quell_PDF_md5.txt'
CODEBOOK = KO / 'codebook.md'
T2D = SPIEGEL / 'teiltabelle_2d.csv'
M2D = SPIEGEL / 'teiltabelle_2d.md'
P2D = SPIEGEL / 'nachzaehlung_2d.txt'
S2D = SPIEGEL / 'nachzaehlung_2d.py'

OUT = []
def w(*a):
    OUT.append(' '.join(str(x) for x in a).replace(SK, '[SK]'))

def halt(msg):
    sys.exit('Bedingung verletzt: ' + msg)

def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()

def nfc(s):
    return unicodedata.normalize('NFC', s)

def spaces(s):
    return re.sub(r'\s+', ' ', nfc(s)).strip()

# ------------------------------------------------------------------ Eingaenge
for p in (ANL, BEF, ABG, T2B, T2C, CODB, QMD5, CODEBOOK, T2D, M2D, P2D, S2D):
    if not p.exists():
        halt('fehlt ' + str(p))
ROWS = list(csv.DictReader(open(ANL, encoding='utf-8'), delimiter=SK))
BYKEY = {(r['studie'], r['satz']): r for r in ROWS}
ORDER = {(r['studie'], r['satz']): i for i, r in enumerate(ROWS)}
KERN = []
ERW = []
for r in ROWS:
    lst = KERN if r['gruppe'] == 'Kern' else ERW
    if r['studie'] not in lst:
        lst.append(r['studie'])
KURZ = {'Lloyd2016': 'Lloyd', 'Hammami2016': 'Hammami', 'Beato2018': 'Beato', 'Negra2019': 'Negra 2019',
        'Negra2020': 'Negra 2020', 'Aloui2022': 'Aloui', 'Liu2024': 'Liu', 'Moran2024': 'Moran',
        'Sammoud2024': 'Sammoud', 'Bouafif2026': 'Bouafif', 'Hilska2021': 'Hilska', 'Klusemann2012': 'Klusemann',
        'Veith2021': 'Veith', 'Rogers2020': 'Rogers', 'PadronCabo2025': 'Padrón-Cabo', 'Asimakidis2022': 'Asimakidis'}

def txt(st, n):
    if (st, n) not in BYKEY:
        halt('Satz fehlt ' + st + ' ' + n)
    return BYKEY[(st, n)]['text']

def bind(st, n, rx, why):
    if not re.search(rx, txt(st, n)):
        halt(why + ' ' + st + ' ' + n)

def sec(r):
    return [c for c in r['sekundaer'].split(SK) if c]

def allc(r):
    return [r['primaer']] + sec(r)

def isB(r):
    return r['primaer'].startswith('B')

def lab(k):
    return KURZ[k[0]] + ' ' + k[1]

def labs(keys):
    return ', '.join(lab(k) for k in keys)

def bystudy(keys):
    return list(dict.fromkeys(k[0] for k in keys))

def kurzsatz(st, n, m=110):
    t = txt(st, n)
    return t if len(t) <= m else t[:m] + ' …'

# ------------------------------------------------------------------ 0 Eingaenge und Reproduktion
w('Zweitpruefung 2 (d): unabhaengige Nachrechnung (zweitpruefung_2d_nachrechnung.py)')
w('')
w('0 Eingaenge (MD5)')
for p in (ANL, BEF, ABG, T2B, T2C, CODB, QMD5, CODEBOOK):
    w('  ' + str(p.relative_to(UP)), md5(p))
for p in (S2D, P2D, T2D, M2D):
    w('  geprueft ' + p.name, md5(p))
w('')
w('1 Reproduktion (Lauf aus dem gestagten Ordner in ' + str(LAUF) + ')')
same = True
for name in ('nachzaehlung_2d.txt', 'teiltabelle_2d.csv', 'teiltabelle_2d.md'):
    a, b = md5(SPIEGEL / name), md5(LAUF / name)
    w('  ' + name, 'neben dem Skript', a, '| eigener Lauf', b, '| gleich' if a == b else '| VERSCHIEDEN')
    same = same and a == b
w('  Ergebnis:', 'bytegleich' if same else 'nicht bytegleich')
w('')
w('2 Korpus: Kern', len(KERN), 'Studien', sum(1 for r in ROWS if r['studie'] in KERN), 'Saetze, erweitert', len(ERW), 'Studien', sum(1 for r in ROWS if r['studie'] in ERW), 'Saetze')
w('')

# ------------------------------------------------------------------ Teiltabelle 2d lesen
TD = list(csv.reader(open(T2D, encoding='utf-8'), delimiter=SK))
HEAD = TD[0]
TROWS = {r[0]: dict(zip(HEAD, r)) for r in TD[1:]}
if len(TROWS) != 21:
    halt('Teiltabelle 2d hat nicht 21 Zeilen')
def nach(nr):
    return TROWS[nr]['Nachzählung']

RES = collections.OrderedDict()
def res(nr, wert, eigen, gleich, notiz=''):
    RES.setdefault(nr, []).append((wert, eigen, gleich, notiz))
    w('  [' + nr + '] ' + wert + ': eigen ' + str(eigen) + ' | 2d ' + ('gleich' if gleich else 'ABWEICHEND') + (' | ' + notiz if notiz else ''))

def in_nach(nr, frag):
    return frag in nach(nr)

# ------------------------------------------------------------------ 3 Nullbefunde (2d.1, 2d.2)
# Eigene Definition: ausdruecklicher Nullbefund = ein Kern-Satz mit Primaercode B, der fuer mindestens eine
# Zielgroesse, Gruppe oder einen Modellterm wortwoertlich keinen (signifikanten) Effekt, keine Veraenderung,
# keinen Unterschied oder eine Groessenklasse "trivial" bzw. "nicht substantiell" berichtet. Implizite
# Nullbefunde (nur durch Weglassen oder ueber "Only", "Largely equivalent") zaehlen nicht.
# Screening breiter als jede Nullformel, danach Handurteil je Treffer.
SCREEN = re.compile(r'\b(?:no|not|none|nor|neither|never|without|fail\w*|unchanged|remain\w*|similar|trivial|unclear|except|only|almost|equivalent)\b|p\s*>\s*0?\.0', re.I)
# Handurteil: Schluessel -> (ja/nein, Formen oder Grund, Pruefausdruck)
NH = {
 ('Lloyd2016', '1.2'): ('ja', 'SIG', r'none of the control groups made any significant changes'),
 ('Lloyd2016', '4.1'): ('ja', 'SIG', r'failed to determine any significant differences'),
 ('Lloyd2016', '4.2'): ('ja', 'SIG KAT', r'were not significant and “trivial”'),
 ('Hammami2016', '1.1'): ('ja', 'SIG', r'did not show any significant differences'),
 ('Hammami2016', '1.3'): ('ja', 'SIG', r'None of the 3 agility tests showed any significant gains'),
 ('Hammami2016', '1.4'): ('ja', 'DIFF', r'RCOD decrement remained unchanged'),
 ('Hammami2016', '1.5'): ('ja', 'SIG', r'^No significant changes of RSSA'),
 ('Beato2018', '4.1'): ('nein', '"trivial" nur in der Chancenfolge eines Befunds mit Vorteil', r'chances for beneficial, trivial, detrimental'),
 ('Beato2018', '4.2'): ('ja', 'KAT', r'did not report any substantial variation'),
 ('Negra2019', '2.8'): ('ja', 'KAT', r'trivial between-group differences'),
 ('Negra2020', '1.4'): ('ja', 'SIG DIFF', r'except for the 1RM half-squat test \(p > 0\.05\), and the CG showed no changes'),
 ('Negra2020', '1.5'): ('ja', 'DIFF', r'^No differences were found in the improvements'),
 ('Aloui2022', '6.2'): ('nein', '"similar results" meint gleich signifikante Verbesserungen am linken Bein', r'we found similar results'),
 ('Liu2024', '2.1'): ('ja', 'SIG', r'There was not a significant main effect'),
 ('Liu2024', '2.4'): ('ja', 'SIG', r'did not significantly vary'),
 ('Liu2024', '3.3'): ('ja', 'SIG', r'no other significant differences were found'),
 ('Liu2024', '3.4'): ('ja', 'SIG', r'HIIT did not significantly varied'),
 ('Moran2024', '1.5'): ('ja', 'KAT', r'were trivial in every group'),
 ('Moran2024', '1.6'): ('ja', 'KAT', r'A trivial effect size was also observed'),
 ('Moran2024', '1.8'): ('nein', '"Largely equivalent small effects" ist eine Groessenaussage, kein Nullbefund', r'Largely equivalent small effects'),
 ('Sammoud2024', '2.3'): ('ja', 'SIG', r'no significant pre-to-post changes'),
 ('Sammoud2024', '3.2'): ('ja', 'SIG', r'but not for the CG'),
 ('Bouafif2026', '1.1'): ('ja', 'SIG', r'except not for the CoD with right foot \(F = 0\.21, p = 0\.65'),
 ('Bouafif2026', '1.3'): ('nein', 'nur implizit ueber "Only", kein ausdruecklicher Nullbefund', r'^Only balance with the right foot'),
 ('Bouafif2026', '3.1'): ('ja', 'SIG', r'while the rest was not significant'),
 ('Bouafif2026', '3.2'): ('ja', 'SIG', r'no other effects reached significance level'),
 ('Bouafif2026', '3.3'): ('ja', 'SIG', r'^No significant effects were found'),
 ('Bouafif2026', '4.1'): ('ja', 'SIG', r'no significant changes were observed in the pre-PHV group'),
}
cand = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and isB(r) and SCREEN.search(r['text'])]
if set(cand) != set(NH):
    halt('Screening und Handurteil Nullbefund verschieden: ' + str(sorted(set(cand) ^ set(NH))))
for k, (j, f, rx) in NH.items():
    bind(k[0], k[1], rx, 'Nullbefund')
NULL = [k for k in cand if NH[k][0] == 'ja']
NULL.sort(key=lambda k: ORDER[k])
forms = collections.defaultdict(list)
for k in NULL:
    for f in NH[k][1].split():
        forms[f].append(k)
two = [k for k in NULL if len(NH[k][1].split()) > 1]
nst = bystudy(NULL)
w('3 Nullbefunde im Kern (2d.1, 2d.2)')
w('  Definition: Kern-Satz mit Primaercode B, der wortwoertlich keinen (signifikanten) Effekt, keine Veraenderung, keinen Unterschied oder die Klasse "trivial" bzw. "nicht substantiell" berichtet. Screening:', len(cand), 'Kandidaten, jeder mit Handurteil:')
for k in sorted(cand, key=lambda k: ORDER[k]):
    w('   ', lab(k), BYKEY[k]['primaer'], '|', NH[k][0], NH[k][1], '|', kurzsatz(*k, 100))
w('  Nullbefundsaetze:', len(NULL), 'in', len(nst), 'Kernstudien, ohne:', ', '.join(KURZ[s] for s in KERN if s not in nst))
w('  Formen: SIG', len(forms['SIG']), '· DIFF', len(forms['DIFF']), '(' + labs(forms['DIFF']) + ') · KAT', len(forms['KAT']), '(' + labs(forms['KAT']) + ') · zwei Formen', len(two), '(' + labs(two) + ')')
res('2d.1', 'Nullbefundsaetze', len(NULL), in_nach('2d.1', '{} Nullbefundsätze in {} von 10'.format(len(NULL), len(nst))))
res('2d.1', 'fehlende Signifikanz', len(forms['SIG']), in_nach('2d.1', 'Fehlende Signifikanz {}'.format(len(forms['SIG']))))
res('2d.1', 'fehlender Unterschied', len(forms['DIFF']), in_nach('2d.1', 'Signifikanzwort {}'.format(len(forms['DIFF']))))
res('2d.1', 'Kategorie', len(forms['KAT']), in_nach('2d.1', 'Relevanzkategorie {} ({})'.format(len(forms['KAT']), labs(forms['KAT']))))
res('2d.1', 'zwei Formen', len(two), in_nach('2d.1', 'Zwei Formen tragen {} Sätze ({})'.format(len(two), labs(two))))
nki = [k for k in NULL if BYKEY[k]['ki'] != '0']
res('2d.2', 'Nullbefundsaetze mit Intervall (Spalte ki)', len(nki), in_nach('2d.2', 'Intervall im Satz: {} der {}'.format(len(nki), len(NULL))))
w('  Implizite Nullbefunde, nicht gezaehlt: Bouafif 1.3 ("Only ..."), Moran 1.8 ("Largely equivalent"), Lloyd 2.4, 2.6, 3.6 (Gruppen nur durch Weglassen)')
# Kategorie an der SWC: Methodenteil (Abschnitt 14 dieser Datei) und Lesart
w('  Kategorie je Satz und Methodenteil (Volltext, Abschnitt 14):')
w('    Lloyd 4.2 "trivial": MBI des Reifevergleichs, SWE 0,20 der gepoolten SD (S. 1244), Kategorie mit der groessten Wahrscheinlichkeit, Abb. 1 kennzeichnet T und U. Lesart Kategorie an der SWC: traegt.')
w('    Negra 2019 2.8 "trivial": ES 0,2 als SWC (PDF-Seite 11). Tab. 4 nennt die vier Vergleiche "most likely similar" bzw. "very likely similar" (ES 0,00 und 0,09) mit Grenzen -0,6 bis 0,6 und -0,7 bis 0,5, die nach der eigenen Intervallregel beide Schwellen schneiden. Lesart Kategorie (nicht Intervall): traegt.')
w('    Beato 4.2 "not ... any substantial": "substantial" im Methodenteil nicht definiert. Diskussion (Manuskript S. 12, Z. 274 f.): "trivial and unclear differences". Abb. 2 (Forest plot, PDF-Seite 23, Sichtpruefung): Sprint 10, 30 und 40 m "Unclear", Dreisprung rechts "Likely trivial", links "Most likely trivial", 505 "Trivial". Der Satz fasst also drei unclear- und drei trivial-Urteile als "nicht substantiell" zusammen. Lesart "Kategorie an der SWC": nur ungenau, es ist die Verneinung von "substantial" (trivial ODER unclear).')
w('    Moran 1.5, 1.6 "trivial": keine Schwelle im Text, Tab. 3 nur ES mit 95-%-KI. Lesart Kategorie ohne Schwelle: traegt.')
w('  Kern-Abbildungen mit "unclear" je Vergleich (nicht Ergebnistext, Sichtpruefung): Lloyd Abb. 1 (U bei COM 20 m, S. 1244), Beato Abb. 2 (3 x Unclear). Im Ergebnistext fassen Lloyd 4.2 ("Nearly all ... trivial") und Beato 4.2 ("not ... any substantial") diese Vergleiche zusammen, ohne "unclear" zu nennen.')
klu = [r['satz'] for r in ROWS if r['studie'] == 'Klusemann2012' and re.search(r'\bunclear\b', r['text'], re.I)]
res('2d.2', '"unclear" bei Klusemann', len(klu), in_nach('2d.2', '„unclear“ in {} Sätzen'.format(len(klu))), ', '.join(klu))
ukern = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and re.search(r'unclear', r['text'], re.I)]
res('2d.2', '"unclear" im Kern-Ergebnistext', len(ukern), in_nach('2d.2', 'Kern-Ergebnistext {}'.format(len(ukern))))
# Klusemann: Nullbefund mit +- (90-%-Grenzen) im selben Satzteil, Handurteil je Satz mit +-
KNH = {
 '2.2': ('nein', 'Nullteil "remained similar" ohne Grenzen, die Grenzen gehoeren zur Ausnahme (agility)', r'remained similar to baseline in all physical tests except for the agility test \(−1\.5 ± 1\.6%'),
 '2.3': ('nein', 'Verbesserung "small improvements"', r'made small improvements'),
 '2.4': ('nein', 'Verbesserung', r'small increase'),
 '2.5': ('ja', '"Trivial or unclear changes" mit Grenzen', r'Trivial or unclear changes occurred in 20-m sprint time \(−0\.5 ± 1\.0%'),
 '2.6': ('ja', '"remained trivial" mit Grenzen', r'remained trivial for the supervised group \(−1\.2 ± 1\.1%\)'),
 '2.8': ('nein', 'Vorteil "greater improvements"', r'greater improvements'),
 '2.9': ('nein', 'Vorteil "better"', r'showed better'),
 '3.1': ('nein', 'substantielle Veraenderungen', r'substantial increase'),
 '3.3': ('ja', 'zweiter Teil "little difference ... unclear" mit Grenzen (Gruppenvergleich)', r'but with little difference compared with the video group \(−4\.2 ± 8\.0%'),
 '4.1': ('nein', 'Verbesserung', r'small increases'),
 '4.2': ('nein', 'substantielle Abnahme', r'substantial decrease'),
 '4.4': ('ja', '"No clear changes" mit Grenzen', r'No clear changes were found in the pull-up test for the supervised group \(1 ± 13%\)'),
}
kpm = [r['satz'] for r in ROWS if r['studie'] == 'Klusemann2012' and isB(r) and '±' in r['text']]
if set(kpm) != set(KNH):
    halt('Klusemann +- und Handurteil verschieden')
for n, (j, why, rx) in KNH.items():
    bind('Klusemann2012', n, rx, 'Klusemann +-')
knull = [n for n in kpm if KNH[n][0] == 'ja']
w('  Klusemann, B-Saetze mit ± (90-%-Grenzen nach 2.2):', len(kpm), '(' + ', '.join(kpm) + ')')
for n in kpm:
    w('   ', n, KNH[n][0], '|', KNH[n][1])
res('2d.2', 'Klusemann Nullbefund mit ± im Satz', ', '.join(knull), in_nach('2d.2', '(' + ', '.join(knull) + ')'), '2d nennt 2.5, 4.4, 2c.41 nennt 2.2, 2.5, 2.6, 4.4')
w('')

# ------------------------------------------------------------------ 4 Schlusslogik, Klusemann, Beato, Klammer (2d.3 bis 2d.6)
w('4 Schlusslogik, Klusemann, Beato, Urteil in der Klammer (2d.3 bis 2d.6)')
kiB = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and isB(r) and r['ki'] != '0']
res('2d.3', 'Kern-Befundsaetze mit Intervall (ki)', labs(kiB), in_nach('2d.3', 'nur Beato 4.1 ({} Satz'.format(len(kiB))) and in_nach('2d.5', '(Spalte ki): {} ({})'.format(len(kiB), labs(kiB))))
bind('Beato2018', '4.1', r'71/27/2%', 'Beato 4.1 Chancen')
w('  Methodenteile mit SWC 0,2 SD und "unclear" ueber ein Intervall oder die Chancen: Lloyd (S. 1244), Negra 2019 (PDF-Seite 11, dazu eine zweite, klinische Regel ueber Chancen >25 % und >0,5 %), Beato (Chancen >5 %, Manuskript S. 9), erweitert Klusemann (S. 2679). Die uebrigen sieben Kernstudien nennen nach Befund § 2.1 (Hauptverfahren) keine MBI, ihre Volltexte sind nicht gestagt, daher nicht am Volltext geprueft.')
b1 = [r['satz'] for r in ROWS if r['studie'] == 'Klusemann2012' and r['satz'] in klu and r['primaer'] == 'B1']
pm = [n for n in klu if '±' in txt('Klusemann2012', n)]
res('2d.4', 'Klusemann unclear, Gruppenvergleich B1', ', '.join(b1), in_nach('2d.4', 'davon Gruppenvergleich (B1) {} ({})'.format(len(b1), ', '.join(b1))))
res('2d.4', 'Klusemann unclear mit ±', ', '.join(pm), in_nach('2d.4', 'mit ± im Satz {} ({})'.format(len(pm), ', '.join(pm))))
res('2d.4', 'Klusemann B-Saetze mit ±', len(kpm), in_nach('2d.4', '± in {} Sätzen mit Primärcode B'.format(len(kpm))))
bind('Klusemann2012', '2.2', r'mean ± 90% confidence limits', 'Klusemann 2.2')
# Klammern: eigener Parser
def brackets(t):
    out, stack = [], []
    for i, ch in enumerate(t):
        if ch == '(':
            stack.append(i)
        elif ch == ')' and stack:
            j = stack.pop()
            if not stack:
                out.append(t[j + 1:i])
    return out
CLASS = re.compile(r'\b(?:trivial|small|moderate|medium|large|very large|unclear)\b', re.I)
def limits(st, kl):
    if re.search(r'\bCL\s*\d*|\bCI\b|confidence', kl):
        return True
    return st == 'Klusemann2012' and '±' in kl
withK, withE, noK, noE, uncl = [], [], [], [], []
for r in ROWS:
    if not isB(r):
        continue
    k = (r['studie'], r['satz'])
    hasL = hasN = False
    for kl in brackets(r['text']):
        if CLASS.search(kl):
            if limits(r['studie'], kl):
                hasL = True
                if re.search(r'unclear', kl):
                    uncl.append(k)
            else:
                hasN = True
    if hasL:
        (withK if r['studie'] in KERN else withE).append(k)
    elif hasN:
        (noK if r['studie'] in KERN else noE).append(k)
res('2d.6', 'Klasse neben Grenzen in der Klammer, Kern', labs(withK), labs(withK) == 'Beato 4.1')
res('2d.6', 'dito erweitert', len(withE), in_nach('2d.6', 'erweitert {} (Klusemann 2.2, 2.4, 2.8, 2.9, 3.1, 3.3, 4.2)'.format(len(withE))), labs(withE))
res('2d.6', '"unclear" in der Klammer', labs(uncl), in_nach('2d.6', 'in der Klammer nur Klusemann 3.3') and labs(uncl) == 'Klusemann 3.3')
res('2d.6', 'Klasse in der Klammer ohne Grenzen', len(noK) + len(noE), (len(noK) + len(noE)) == 12, 'Kern ' + str(len(noK)) + ', erweitert ' + labs(noE))
w('')

# ------------------------------------------------------------------ 5 Beato Tab. 1 und Volltext-Stellen (Teil 1: Tabelle)
PDFN = {}
for line in open(QMD5, encoding='utf-8'):
    p = line.rstrip('\n').split('  ')
    if len(p) >= 4:
        PDFN[p[2]] = (p[0], p[3])
READERS = {}
def pdftxt(key, page):
    if key not in READERS:
        m5, name = PDFN[key]
        path = PDFDIR / name
        if md5(path) != m5:
            halt('PDF-Pruefsumme ' + key)
        READERS[key] = pypdf.PdfReader(str(path))
    return READERS[key].pages[page - 1].extract_text()
tab = pdftxt('Beato2018', 20) + '\n' + pdftxt('Beato2018', 21)
TROW = []
for line in tab.split('\n'):
    m = re.match(r'^\s*(.+?\((?:cm|m|s)\)).*?\b(\d{1,3})/(\d{1,3})/(\d{1,3})\s+(.+?)\s*$', line)
    if m:
        TROW.append((m.group(1).strip(), int(m.group(2)), int(m.group(3)), int(m.group(4)), re.sub(r'\s+', '', m.group(5))))
w('5 Beato Tab. 1 (pypdf, PDF-Seiten 20 und 21): Zeilen', len(TROW))
und = [(n, b, t, d, q) for n, b, t, d, q in TROW if (b > 5 and d > 5) != q.lower().startswith('unclear')]
oder = [(n, b, t, d, q) for n, b, t, d, q in TROW if (b > 5 or d > 5) != q.lower().startswith('unclear')]
uc = [(n, b, t, d) for n, b, t, d, q in TROW if q.lower().startswith('unclear')]
w('  "Unclear":', ', '.join('{} {}/{}/{}'.format(*x) for x in uc), '· groesster Schaden der uebrigen Zeilen:', max(d for n, b, t, d, q in TROW if not q.lower().startswith('unclear')), '%')
w('  Regel "unclear, wenn Nutzen UND Schaden ueber 5 %": Widersprueche', len(und), '· Wortlaut des Methodenteils "beneficial OR detrimental >5%": Widersprueche', len(oder), '(woertlich angewandt waeren', sum(1 for n, b, t, d, q in TROW if b > 5 or d > 5), 'der', len(TROW), 'Zeilen unclear, auch Beato 4.1 mit 71/27/2)')
res('2d.5', 'Tab. 1 Zeilen', len(TROW), len(TROW) == 14)
res('2d.5', 'Tab. 1 unclear', ', '.join('{} {}/{}/{}'.format(*x) for x in uc), in_nach('2d.5', '505 COD test 29/47/24'))
w('')

# ------------------------------------------------------------------ 6 Zuordnung paralleler Werte (2d.7, 2d.8)
w('6 Zuordnung paralleler Werte (2d.7, 2d.8)')
RW = re.compile(r'\brespectively\b|\brespectfully\b|\brespective\b', re.I)
rk = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and re.search(r'\brespectively\b', r['text'])]
rk2 = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and re.search(r'\brespectively\b|\brespectfully\b', r['text'])]
re_ = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in ERW and re.search(r'\brespectively\b', r['text'])]
res('2d.7', '"respectively" Kern', '{} in {}'.format(len(rk), len(bystudy(rk))), in_nach('2d.7', 'im Kern {} Sätze in {} Studien'.format(len(rk), len(bystudy(rk)))))
res('2d.7', 'mit "respectfully"', '{} in {}'.format(len(rk2), len(bystudy(rk2))), in_nach('2d.7', '{} in {}, dazu'.format(len(rk2), len(bystudy(rk2)))))
res('2d.7', '"respectively" erweitert', '{} in {}'.format(len(re_), len(bystudy(re_))), in_nach('2d.7', 'Erweitert {} Sätze in {} Studien'.format(len(re_), len(bystudy(re_)))))
# Was ordnet das Zuordnungswort zu? Handurteil je Kernsatz
WAS = {
 ('Lloyd2016', '1.1'): ('Objekt', r'are displayed in Table 4 for pre- and post-PHV groups, respectively'),
 ('Hammami2016', '1.3'): ('Werte', r'had respective p values of 0\.08, 0\.06 and 0\.142'),
 ('Hammami2016', '1.4'): ('Werte', r'p<0\.01 and p<0\.05 respectively'),
 ('Beato2018', '1.1'): ('Werte', r'respectfully'),
 ('Beato2018', '2.1'): ('Werte', r'93% and 96% for CODJ-G and COD-G, respectively'),
 ('Beato2018', '2.2'): ('Werte', r'5\.5 ± 0\.99 and 5\.50 ± 1 for CODJ-G and COD-G, respectively'),
 ('Beato2018', '3.2'): ('Objekt', r'reported in Tables 1 and 2, respectively'),
 ('Negra2019', '2.3'): ('Werte', r'large and very large effect sizes .*respectively'),
 ('Liu2024', '2.4'): ('Werte', r'p>0\.999 and p>0\.080, respectively'),
}
zk = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and RW.search(r['text'])]
if set(zk) != set(WAS):
    halt('Zuordnungswort Kern und Handurteil verschieden')
for k, (a, rx) in WAS.items():
    bind(k[0], k[1], rx, 'Zuordnungswort')
zw = [k for k in sorted(zk, key=lambda k: ORDER[k]) if WAS[k][0] == 'Werte']
zo = [k for k in sorted(zk, key=lambda k: ORDER[k]) if WAS[k][0] == 'Objekt']
w('  Zuordnungswort im Kern:', len(zk), 'Saetze in', len(bystudy(zk)), 'Studien. Ordnet Werte zu:', len(zw), 'in', len(bystudy(zw)), '(' + labs(zw) + '), ordnet Objekte zu:', len(zo), '(' + labs(zo) + ')')
res('2d.7', 'Zuordnungswort Kern (Saetze in Studien)', '{} in {}'.format(len(zk), len(bystudy(zk))), in_nach('2d.7', '') and ('9 Sätze in 5 Studien' in TROWS['2d.7']['Folge für das Potenzial']), 'davon nur fuer Werte {} in {}'.format(len(zw), len(bystudy(zw))))
# Bezeichnung je Wert: eigener Kandidatenausdruck. Ein Satz traegt mindestens zwei statistische Werte, jeder an einer
# eigenen Bezeichnung: entweder mindestens zwei Klammern mit Statistik (p, F, d, ES, Δ, change, mean difference)
# oder in einer Klammer mindestens zwei Segmente "Bezeichnung: Wert". Ohne Zuordnungswort und ohne Folge.
STAT = re.compile(r'\bp\s*[<>=≤≥]|\bF\s*[=≥≤]|\bd\s*=|\bES\s*=|[Δ∆]|change\s*=|mean difference|ηp?²|η2')
def labelled(t):
    kls = [kl for kl in brackets(t) if STAT.search(kl)]
    inner = max([len(re.findall(r'(?:^|' + SK + r'\s*)[A-Za-z0-9][\w◦°\- ]{0,25}:\s*[Δ∆]?\s*[−\-]?\d', kl)) for kl in brackets(t)] or [0])
    return len(kls) >= 2 or inner >= 2
BZ = {
 ('Aloui2022', '2.1'): ('ja', r'\(SJ: Δ19%'),
 ('Aloui2022', '3.1'): ('ja', r'\(10 m sprint: Δ−11%'),
 ('Aloui2022', '4.1'): ('ja', r'\(S90◦: Δ−9%'),
 ('Aloui2022', '5.1'): ('nein, Folge', r'\(RSSA best and RSSA mean\), with time decreases of Δ−8%'),
 ('Aloui2022', '6.1'): ('ja', r'\(anterior: Δ11%'),
 ('Aloui2022', '6.2'): ('ja', r'\(anterior: Δ11%'),
 ('Liu2024', '1.1'): ('ja', r'on CMJ \(F=0\.979'),
 ('Liu2024', '2.3'): ('ja', r'from HIIT \(mean difference: .?2\.133cm'),
 ('Liu2024', '2.4'): ('ja, mit Zuordnungswort im ersten Teil', r'while PJT significantly improved \(mean difference: \+0\.786cm'),
 ('Liu2024', '3.3'): ('Grenzfall', r'from HIIT \(mean difference: .?270\.67m.*no other significant differences were found \(p>0\.05\)'),
 ('Liu2024', '3.4'): ('ja', r'HIIT did not significantly varied from pre to post \(p=0\.474\), while PJT significantly declined \(mean difference'),
 ('Liu2024', '4.3'): ('ja', r'from HIIT \(mean difference: 0\.031s'),
 ('Liu2024', '4.4'): ('ja', r'HIIT significantly declined from pre to post \(mean difference: 0\.023s'),
 ('Sammoud2024', '2.1'): ('ja', r'for CMJ height \(p < 0\.001'),
 ('Sammoud2024', '2.2'): ('ja', r'in CMJ height \(∆16\.85%'),
 ('Sammoud2024', '2.3'): ('ja', r'for CMJ height \(∆0\.76%'),
 ('Sammoud2024', '3.2'): ('ja', r'for the PJT group \(change = -4\.75%%, d = 0\.43\) but not for the CG \(change = 1\.96%'),
 ('Bouafif2026', '1.1'): ('ja', r'\(F ≥ 4\.3, p ≤ 0\.045.*except not for the CoD with right foot \(F = 0\.21'),
 ('Bouafif2026', '1.2'): ('ja', r'for all tests \(F ≥ 7\.2.*with the right foot \(F ≥ 4\.2'),
 ('Bouafif2026', '3.1'): ('ja', r'training age \(F = 15\.0.*test time \(F = 35\.5'),
 ('Bouafif2026', '3.2'): ('ja', r'training group \(F = 6\.5.*training age almost reached significance level \(F = 3\.96'),
 ('Negra2020', '1.4'): ('ja', r'the RTG showed significant improvements in all tests \(p < 0\.05\).*except for the 1RM half-squat test \(p > 0\.05\)'),
 ('Sammoud2024', '1.5'): ('ja, Orientierungssatz O4', r'no significant baseline differences between groups were observed \(p > 0\.05\), except for the inter-limb asymmetry score \(p < 0\.05\)'),
}
bzc = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and labelled(r['text']) and not re.search(r'\brespectively\b|\brespectfully\b|\brespective\b', r['text'])]
bzc_all = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and labelled(r['text'])]
miss = set(bzc) - set(BZ)
extra = [k for k in BZ if k not in bzc_all]
if miss or extra:
    halt('Bezeichnung je Wert: Kandidaten und Handurteil verschieden ' + str(sorted(miss)) + str(sorted(extra)))
for k, (a, rx) in BZ.items():
    bind(k[0], k[1], rx, 'Bezeichnung je Wert')
bzj = [k for k in sorted(BZ, key=lambda k: ORDER[k]) if BZ[k][0] == 'ja']
bzg = [k for k in sorted(BZ, key=lambda k: ORDER[k]) if BZ[k][0] != 'ja' and not BZ[k][0].startswith('nein')]
w('  Bezeichnung je Wert (eigener Kandidatenausdruck, jeder Treffer mit Handurteil):', len(bzj), 'Saetze in', len(bystudy(bzj)), 'Studien:', labs(bzj))
w('    ausserhalb der Zaehlung:', ', '.join(lab(k) + ' (' + BZ[k][0] + ')' for k in bzg), '· Aloui 5.1 ordnet ueber die Folge zu')
bze = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in ERW and labelled(r['text']) and not re.search(r'respectiv', r['text'])]
w('  erweitert, Kandidaten des Ausdrucks ohne Handurteil (Sichtpruefung: Bezeichnung je Wert):', len(bze), '(' + labs(bze) + '), 2d nennt erweitert 5')
script_bz = ['Aloui2022 2.1', 'Aloui2022 3.1', 'Aloui2022 4.1', 'Aloui2022 6.1', 'Aloui2022 6.2', 'Liu2024 1.1', 'Sammoud2024 2.1', 'Sammoud2024 2.2', 'Sammoud2024 2.3']
nur_eigen = [k for k in bzj if (k[0] + ' ' + k[1]) not in script_bz]
w('    in 2d nicht gezaehlt:', len(nur_eigen), '(' + labs(nur_eigen) + ')')
res('2d.7', 'Bezeichnung je Wert Kern', '{} in {}'.format(len(bzj), len(bystudy(bzj))), False, '2d: 9 in 3 (Aloui, Liu, Sammoud). Die Folge "Zuordnungswort mit der breitesten Kernbasis" kehrt sich um')
res('2d.8', 'Bezeichnung je Wert Kern', len(bzj), in_nach('2d.8', 'Bezeichnung je Wert Kern {} Sätze'.format(len(bzj))))
eq = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and re.search(r'\b[a-z]+ training\s*=\s*\d', r['text'])]
res('2d.8', '"=" als Zuordnung im Kern', labs(eq), in_nach('2d.8', '„=“ Kern {} ({})'.format(len(eq), labs(eq))))
FOLGE = {('Aloui2022', '5.1'): r'\(RSSA best and RSSA mean\), with time decreases of Δ−8% \(p < 0\.01, d = 0\.72\) and Δ−8%',
         ('Klusemann2012', '2.3'): r'agility \(−2\.2 ± 2\.2% and −3\.8 ± 1\.1%\)',
         ('Klusemann2012', '2.5'): r'\(−0\.5 ± 1\.0% and −1\.6 ± 2\.0%\).*for the supervised and video groups',
         ('Klusemann2012', '4.1'): r'Both the supervised and video groups .*\(20 ± 13% and 23 ± 15%\)'}
for k, rx in FOLGE.items():
    bind(k[0], k[1], rx, 'Folge')
# Kandidaten der Folge: zwei Werte mit "and" verbunden ohne Bezeichnung und ohne Zuordnungswort im selben Teilsatz
FC = re.compile(r'[−\-]?\d+(?:\.\d+)?\s*(?:±\s*\d+(?:\.\d+)?)?\s*%?\s*(?:\([^()]*\))?\s*and\s*[Δ∆]?[−\-]?\d+(?:\.\d+)?\s*(?:±\s*\d+(?:\.\d+)?)?\s*%?\s*(?:\([^()]*\))?')
fcand = []
for r in ROWS:
    t = r['text']
    for m in FC.finditer(t):
        seg = t[m.start():m.end() + 40]
        if not re.search(r'respectiv|respectful', t) and not re.search(r'between [\d.]+ and|tests? \d and \d|Tables? \d+ and \d+|Figures? \d+ and \d+', t[max(0, m.start() - 15):m.end()]):
            fcand.append((r['studie'], r['satz']))
            break
w('  Folge ohne Zuordnungswort, Bezugsfolge im selben Satz:', labs(FOLGE), '· weitere Kandidaten zwei mit "and" verbundener Werte ohne Zuordnungswort:', labs([k for k in fcand if k not in FOLGE]) or 'keine')
w('  Bezugsfolge im vorigen Satz: kein Treffer (jede Folge oben hat die Bezugsfolge im selben Satz)')
w('')

# ------------------------------------------------------------------ 7 Ordnung, Bloecke, Themenanker (2d.9 bis 2d.11)
w('7 Ordnung, Befundbloecke und Themenanker (2d.9 bis 2d.11)')
# Eigene Ordnungsregel: Zielgroessenfolge der B-Saetze mit genau einer Zielgroesse (zg ohne +, nicht X).
# "nach Zielgroesse": mindestens zwei Zielgroessen und keine kehrt nach einem Wechsel wieder.
# "nach Analyseschritt": mehr als die Haelfte der B-Saetze mit zg X oder mehreren Zielgroessen.
ordn = collections.OrderedDict((x, []) for x in ('Zielgroesse', 'Analyseschritt', 'sonst'))
for st in KERN:
    seq = [r['zg'] or 'X' for r in ROWS if r['studie'] == st and isB(r)]
    single = [z for z in seq if z != 'X' and '+' not in z]
    changes = [z for i, z in enumerate(single) if i == 0 or z != single[i - 1]]
    multi = sum(1 for z in seq if z == 'X' or '+' in z)
    if multi > len(seq) / 2:
        ordn['Analyseschritt'].append(KURZ[st])
    elif len(set(single)) >= 2 and len(changes) == len(set(single)):
        ordn['Zielgroesse'].append(KURZ[st])
    else:
        ordn['sonst'].append(KURZ[st])
    w('   ', KURZ[st], ' '.join(seq))
res('2d.9', 'nach Zielgroesse', ', '.join(ordn['Zielgroesse']), in_nach('2d.9', 'Nach Zielgröße {} ({})'.format(len(ordn['Zielgroesse']), ', '.join(ordn['Zielgroesse']))))
res('2d.9', 'nach Analyseschritt', ', '.join(ordn['Analyseschritt']), in_nach('2d.9', 'Analyseschritt {} ({})'.format(len(ordn['Analyseschritt']), ', '.join(ordn['Analyseschritt']))))
bseq = [r['zg'] or 'X' for r in ROWS if r['studie'] == 'Bouafif2026' and isB(r)]
lead = 0
while bseq[lead] == 'X':
    lead += 1
res('2d.9', 'Bouafif, B-Saetze ueber alle vorn', lead, in_nach('2d.9', 'beginnt mit {} Sätzen'.format(lead)))
# Bloecke in drei Varianten
def blocks(variant):
    out = []
    for st in KERN:
        prev = None
        for r in [x for x in ROWS if x['studie'] == st]:
            if not isB(r):
                prev = None
                continue
            z = r['zg'] or 'X'
            k = {'a': (z.split('+')[0], r['absatz']), 'b': (z, r['absatz']), 'c': (z.split('+')[0],)}[variant]
            if k != prev:
                out.append((st, r['satz']))
            prev = k
    return out
BA, BB, BC = blocks('a'), blocks('b'), blocks('c')
w('  Bloecke: (a) gleicher Absatz und erste Zielgroesse', len(BA), '· (b) gleicher Absatz und volle zg', len(BB), '· (c) erste Zielgroesse ohne Absatzgrenze', len(BC))
res('2d.10', 'Befundbloecke (a)', len(BA), in_nach('2d.10', '{} Blöcke'.format(len(BA))))
# Eigenes Handurteil je Blockbeginn: Satzanfang nach Wortlaut, Vorrang Konnektor > Themenanker > Sammelbefund (B4) > Zeitangabe > Modellterm > Quantor > Gruppe > Zielgroesse/Befund/Analyse
BEG = {
 ('Lloyd2016', '1.2'): ('Sammelbefund', r'^Irrespective of maturation, none'),
 ('Lloyd2016', '2.1'): ('Modellterm', r'^Significant main effects'),
 ('Lloyd2016', '3.1'): ('Modellterm (Analyse als Subjekt, Haupteffekte als Objekt)', r'^Analysis of squat jump .*main effects'),
 ('Lloyd2016', '4.1'): ('Sammelbefund', r'^Although within-group analysis'),
 ('Lloyd2016', '4.3'): ('Konnektor', r'^However,'),
 ('Hammami2016', '1.1'): ('Sammelbefund', r'^The control group did not show any'),
 ('Hammami2016', '1.2'): ('Konnektor', r'^However,'),
 ('Hammami2016', '1.3'): ('Quantor', r'^None of the 3 agility tests'),
 ('Hammami2016', '1.4'): ('Quantor (Teilangabe "Two of the 3"), im Befund als Zielgroesse gezaehlt', r'^Two of the 3 RCOD scores'),
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
 ('Liu2024', '2.1'): ('Modellterm', r'^There was not a significant main effect'),
 ('Liu2024', '3.1'): ('Modellterm', r'^There was a significant main effect'),
 ('Liu2024', '4.1'): ('Modellterm', r'^There was a significant main effect'),
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
if set(BEG) != set(BA):
    halt('Blockbeginn und Handurteil verschieden')
for k, (a, rx) in BEG.items():
    bind(k[0], k[1], rx, 'Blockbeginn')
cnt = collections.Counter(v[0].split(' (')[0] for v in BEG.values())
w('  Blockbeginn, eigenes Urteil:', ', '.join('{} {}'.format(a, b) for a, b in cnt.most_common()))
w('  Hammami 1.4 "Two of the 3 RCOD scores" ist eine Mengenangabe ueber die Tests einer Zielgroesse wie Hammami 1.3, in Abschnitt 11 von nachzaehlung_2d.txt als "Tests · Teil mit Liste" gefuehrt. Als Quantor gezaehlt: Quantor 2, Zielgroesse/Befund/Analyse/Modellterm 19.')
res('2d.10', 'Quantor als Blockbeginn', cnt['Quantor'], in_nach('2d.10', 'Quantor {} (Hammami 1.3)'.format(cnt['Quantor'])), 'mit Allquantor oder Verneinung allein 1 (Hammami 1.3), wie 2d')
res('2d.10', 'Zielgroesse, Befund, Modellterm oder Analyse', cnt['Zielgroesse, Befund oder Analyse'] + cnt['Modellterm'], in_nach('2d.10', '(zusammen {})'.format(cnt['Zielgroesse, Befund oder Analyse'] + cnt['Modellterm'])), 'mit Hammami 1.4 als Zielgroesse 20, wie 2d')
res('2d.10', 'Sammelbefund, Themenanker, Konnektor, Zeitangabe, Gruppe', '{} {} {} {} {}'.format(cnt['Sammelbefund'], cnt['Themenanker'], cnt['Konnektor'], cnt['Zeitangabe'], cnt['Gruppe']), in_nach('2d.10', 'Sammelbefund {}'.format(cnt['Sammelbefund'])) and in_nach('2d.10', 'Themenanker {}, Konnektor {}'.format(cnt['Themenanker'], cnt['Konnektor'])))
# Themenanker: breiteres Screening vorangestellter Praepositionalgruppen im Kern
TS = re.compile(r'^(?:For|Regarding|In terms of|In reference to|Considering|About|As for|With regard to|Concerning|In the|Within|Among|Across|Irrespective of|After)\b')
TH = {
 ('Lloyd2016', '1.2'): ('nein', 'vorangestellte Einschraenkung'),
 ('Lloyd2016', '2.2'): ('ja', ''), ('Lloyd2016', '2.3'): ('ja', ''), ('Lloyd2016', '3.2'): ('ja', ''),
 ('Lloyd2016', '3.6'): ('Grenzfall', '"In the post-PHV cohort," setzt die Kohorte als Thema wie "Regarding the LPJT group"'),
 ('Negra2019', '2.2'): ('Grenzfall', '"In the same group," setzt die Gruppe als Thema, im Befund als "Gruppe" gezaehlt'),
 ('Negra2019', '2.3'): ('ja', ''), ('Negra2019', '2.4'): ('ja', ''), ('Negra2019', '2.8'): ('ja', ''),
 ('Negra2020', '1.4'): ('nein', 'Zeitangabe'),
 ('Aloui2022', '5.1'): ('ja', ''), ('Aloui2022', '6.2'): ('ja', ''),
 ('Liu2024', '2.4'): ('ja', ''), ('Liu2024', '3.4'): ('ja', ''), ('Liu2024', '4.4'): ('ja', ''),
 ('Sammoud2024', '1.5'): ('ja', ''), ('Sammoud2024', '3.1'): ('ja', ''),
 ('Bouafif2026', '3.1'): ('ja', ''),
 ('Beato2018', '4.1'): ('nein', 'Zeitangabe'),
 ('Beato2018', '3.2'): ('nein', '"Within-group" ist Attribut des Subjekts'),
 ('Negra2019', '2.1'): ('nein', '"Within-group" ist Attribut des Subjekts'),
}
tsc = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and TS.search(r['text'])]
if set(tsc) != set(TH):
    halt('Themenanker-Screening und Handurteil verschieden ' + str(sorted(set(tsc) ^ set(TH))))
thj = [k for k in sorted(tsc, key=lambda k: ORDER[k]) if TH[k][0] == 'ja']
thg = [k for k in sorted(tsc, key=lambda k: ORDER[k]) if TH[k][0] == 'Grenzfall']
thb = [k for k in thj if k in BA]
res('2d.11', 'Themenanker', '{} in {}'.format(len(thj), len(bystudy(thj))), in_nach('2d.11', '{} Sätze in {} Studien'.format(len(thj), len(bystudy(thj)))), 'Grenzfaelle ohne Zaehlung: ' + labs(thg))
res('2d.11', 'davon Blockbeginn', labs(thb), in_nach('2d.11', 'Blockbeginn {} ({})'.format(len(thb), labs(thb))))
w('')

# ------------------------------------------------------------------ 8 Modellergebnis, unadjustiert (2d.12, 2d.13)
w('8 Modellergebnis und Einzelgruppen, unadjustierter Schaetzer (2d.12, 2d.13)')
# Eigenes Handurteil: Studien mit Modellergebnis (Haupteffekt, Wechselwirkung, ANCOVA im Post-Wert) UND einem Vergleich
# einzelner Gruppen (Paarvergleich, Veraenderung je Gruppe) in eigenen Saetzen, je der erste Satz jeder Art.
K4 = {
 'Lloyd2016': ('2.1', r'main effects', '2.4', r'improved in all 3 training groups'),
 'Liu2024': ('2.1', r'main effect of time', '2.3', r'significantly different from HIIT'),
 'Bouafif2026': ('1.1', r'from pre- to post test \(F ≥ 4\.3', '1.4', r'Post hoc comparison'),
 'Sammoud2024': ('2.1', r'between-group difference at post-test', '2.2', r'pre-to-post training improvements'),
 'Negra2020': ('1.5', r'between experimental groups', '1.4', r'the RTG showed significant improvements'),
}
first = []
for st, (m, rm, g, rg) in K4.items():
    bind(st, m, rm, 'Modellergebnis')
    bind(st, g, rg, 'Einzelgruppe')
    if ORDER[(st, m)] < ORDER[(st, g)]:
        first.append(KURZ[st])
w('  Modellergebnis zuerst:', len(first), 'von', len(K4), '(' + ', '.join(first) + ')')
w('  Grenzfall ausserhalb der Zaehlung: Aloui nennt die Veraenderung der Interventionsgruppe nur in der Klammer des Modellsatzes (Befund § 3.3), dort ebenfalls nach dem Modellterm.')
res('2d.12', 'Modellergebnis zuerst', '{} von {}'.format(len(first), len(K4)), in_nach('2d.12', '{} von {} ({})'.format(len(first), len(K4), ', '.join(first))))
adjk = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and re.search(r'adjust|crude', r['text'], re.I)]
unad = [r['satz'] for r in ROWS if r['studie'] not in KERN and re.search(r'unadjusted', r['text'])]
both = [r['satz'] for r in ROWS if r['studie'] not in KERN and re.search(r'unadjusted IRR', r['text']) and re.search(r'(?<!un)adjusted IRR', r['text'])]
res('2d.13', 'Kern adjust/crude', len(adjk), in_nach('2d.13', 'Kern {} Sätze'.format(len(adjk))))
res('2d.13', 'erweitert "unadjusted"', ', '.join(unad), in_nach('2d.13', '({})'.format(', '.join(unad))))
res('2d.13', 'beide Schaetzer in einer Klammer', ', '.join(both), in_nach('2d.13', 'in {} ({})'.format(len(both), ', '.join(both))))
perg = [n for n in both if re.search(r'\d+(?:\.\d+)? in the intervention group and \d+(?:\.\d+)? in the control group|\d+(?:\.\d+)? and \d+(?:\.\d+)? per 1000 hours of exposure in the intervention and control groups', txt('Hilska2021', n))]
w('  davon mit Werten je Gruppe im selben Satz:', ', '.join(perg), '· ohne Werte je Gruppe (nur "smaller in the intervention group compared with the control group"):', ', '.join(n for n in both if n not in perg))
res('2d.13', '"jeweils ... nach den Werten je Gruppe"', ', '.join(perg), len(perg) == len(both), 'Hilska 6.4 hat keine Werte je Gruppe, 2c.43 "nach den Inzidenzen je Gruppe" gilt fuer 3.3 und 4.1')
w('')

# ------------------------------------------------------------------ 9 Schluss, V2, V1, Z1 (2d.14 bis 2d.18)
w('9 Schluss, Resuemee, Analyseregel, Datenpruefung, Zusatzanalysen (2d.14 bis 2d.18)')
def last(st):
    return [r for r in ROWS if r['studie'] == st][-1]
OBJ = re.compile(r'\b(?:Tables?|Fig(?:s|ure|ures)?|figure)\s*\d')
ENDK = re.compile(r'\(([^()]*)\)\s*\.\s*$')
lb = [s for s in KERN if isB(last(s))]
lx = [s for s in KERN if last(s)['primaer'].startswith('X')]
lo = [s for s in KERN if OBJ.search(last(s)['text'])]
lk = [s for s in KERN if ENDK.search(last(s)['text']) and OBJ.search(ENDK.search(last(s)['text']).group(1))]
res('2d.14', 'letzter Satz B, X, Objekt, Klammer am Satzende', '{} {} {} {}'.format(len(lb), len(lx), len(lo), len(lk)), in_nach('2d.14', 'Letzter Satz B-Code {}, Objektsatz {}'.format(len(lb), len(lx))) and in_nach('2d.14', 'Objektverweis {}, Klammer am Satzende {}'.format(len(lo), len(lk))), ', '.join(KURZ[s] for s in lk))
lz = [s for s in KERN + ERW if last(s)['primaer'].startswith('Z')]
loe = [s for s in ERW if last(s)['primaer'].startswith('O')]
res('2d.15', 'Schluss Z, erweitert O', '{} {}'.format(len(lz), len(loe)), in_nach('2d.15', 'Z-Primärcode {} von 16'.format(len(lz))) and in_nach('2d.15', 'O-Satz {} ('.format(len(loe))), ', '.join(KURZ[s] for s in loe))
hyp = [r for r in ROWS if re.search(r'hypothes', r['text'], re.I)]
summ = [r for r in ROWS if re.search(r'\b(?:in summary|to summari[sz]e|overall|taken together|in conclusion|we conclude|collectively|in sum|altogether|in general|to sum up)\b', r['text'], re.I)]
summ_obj = [lab((r['studie'], r['satz'])) for r in ROWS if re.search(r'summari[sz]ed in', r['text'])]
w('  breitere Liste der Wendungen (in summary, to summarize, overall, taken together, in conclusion, we conclude, collectively, in sum, altogether, in general, to sum up): 0 Treffer. "summarized in" nur im Objektsatz', ', '.join(summ_obj))
res('2d.16', 'hypothes / zusammenfassende Wendung (breitere Liste)', '{} {}'.format(len(hyp), len(summ)), in_nach('2d.16', '„hypothes…“ in {} von 212'.format(len(hyp))) and in_nach('2d.16', 'in {}. Letzter'.format(len(summ))))
def where(r):
    rr = [x for x in ROWS if x['studie'] == r['studie']]
    bi = [i for i, x in enumerate(rr) if isB(x)]
    i = rr.index(r)
    if i < bi[0]:
        return 'vorn'
    if i > bi[-1]:
        return 'danach'
    return 'Befundteil'
for code, nr in (('V2', '2d.17'), ('V1', '2d.18'), ('Z1', '2d.18')):
    hits = [(r['studie'], r['satz'], 'p' if r['primaer'] == code else 's', where(r)) for r in ROWS if code in allc(r)]
    lage = collections.OrderedDict((x, [h for h in hits if h[3] == x]) for x in ('vorn', 'Befundteil', 'danach'))
    w('  ' + code + ':', len(hits), 'Saetze ·', ' · '.join('{} {} ({})'.format(x, len(v), ', '.join(KURZ[a] + ' ' + b + ('' if c == 'p' else ' sek') for a, b, c, d in v)) for x, v in lage.items()))
    kern = [h for h in hits if h[0] in KERN]
    if code == 'V2':
        res(nr, 'V2 Saetze, danach', '{} {}'.format(len(hits), len(lage['danach'])), in_nach(nr, 'in {} Sätzen'.format(len(hits))) and in_nach(nr, 'nach dem letzten Befund: keine'))
    if code == 'V1':
        res(nr, 'V1 Kern, alle, danach', '{} {} {}'.format(len(kern), len(hits), len(lage['danach'])), in_nach(nr, 'V1 Kern {}, alle {} Sätze'.format(len(kern), len(hits))))
    if code == 'Z1':
        res(nr, 'Z1 Saetze, Kern nur sekundaer, danach', '{} {} {}'.format(len(hits), all(h[2] == 's' for h in kern), ', '.join(KURZ[a] + ' ' + b for a, b, c, d in lage['danach'])), in_nach(nr, 'Z1 in {} Sätzen'.format(len(hits))) and in_nach(nr, 'Nach dem letzten Befund nur Asimakidis 1.6'))
w('  Asimakidis 1.6 traegt B4 und B2 als Sekundaercode: "nach dem letzten Befund" gilt nach dem Primaercode.')
w('')

# ------------------------------------------------------------------ 10 Folge der Zielgroessen (2d.19)
w('10 Folge der Zielgroessen in Saetzen mit mindestens zwei von Sprint (S), Richtungswechsel (C), Sprung (J) (2d.19)')
# Eigenes Lexikon (Testnamen), Position der ersten Nennung je Kategorie
LEX = {'S': [r'sprint', r'acceleration', r'running velocity', r'\b\d+\s?-?m\b(?! ?(?:sprint)?\s*(?:week|day))'],
       'C': [r'\bCoD\b', r'\bICoD\b', r'\b505\b', r'agility', r'change of direction', r'\bS90', r'\bSBF\b', r'\bS180'],
       'J': [r'jump', r'\bCMJ', r'\bSJ\b', r'\bSLJ\b', r'reactive strength', r'\bhop', r'\bFJT\b']}
def zfirst(t):
    t = re.sub(r'\d+[- ]week|\d+[- ]day|\d+\.\d+m\b|\d+m\b(?=\s*[\x3b)])', ' ', t)
    pos = {}
    for c, pats in LEX.items():
        ps = [m.start() for p in pats for m in re.finditer(p, t)]
        if ps:
            pos[c] = min(ps)
    return ''.join(sorted(pos, key=pos.get))
MS = [((r['studie'], r['satz']), zfirst(r['text'])) for r in ROWS if r['studie'] in KERN and len(zfirst(r['text'])) >= 2]
for k, f in MS:
    w('   ', lab(k), f)
refs, dev, ok = {}, [], 0
for k, f in MS:
    if k[0] not in refs:
        refs[k[0]] = f
        continue
    a = ''.join(c for c in refs[k[0]] if c in f)
    b = ''.join(c for c in f if c in refs[k[0]])
    if a == b:
        ok += 1
    else:
        dev.append((k, f, refs[k[0]]))
res('2d.19', 'Saetze, Studien, gleich, abweichend', '{} {} {} {}'.format(len(MS), len(bystudy([k for k, f in MS])), ok, ', '.join(lab(k) + ' ' + f + ' gegen ' + g for k, f, g in dev)), in_nach('2d.19', '{} Kernsätze in {} Studien'.format(len(MS), len(bystudy([k for k, f in MS])))) and in_nach('2d.19', 'folgen {} der übrigen'.format(ok)))
w('')

# ------------------------------------------------------------------ 11 Umsetzung (2d.20)
w('11 Umsetzung (2d.20)')
o2 = [r for r in ROWS if r['studie'] in KERN and 'O2' in allc(r)]
ww = {x: [lab((r['studie'], r['satz'])) for r in o2 if re.search(r'\b' + x + r'\b', r['text'], re.I)] for x in ('compliance', 'attendance', 'completed', 'adherence')}
vals = [int(v) for r in o2 for v in re.findall(r'(\d{2})\s*%', r['text'])]
res('2d.20', 'O2 Kern', '{} in {}'.format(len(o2), len(set(r['studie'] for r in o2))), in_nach('2d.20', 'O2 im Kern {} Sätze in {} Studien'.format(len(o2), len(set(r['studie'] for r in o2)))))
res('2d.20', 'Wortwahl', ' '.join('{} {}'.format(a, len(b)) for a, b in ww.items()), all(in_nach('2d.20', '„{}“ {}'.format(a, len(b))) for a, b in ww.items()))
res('2d.20', 'Werte', '{} bis {}'.format(min(vals), max(vals)), in_nach('2d.20', 'Werte {} bis {} %'.format(min(vals), max(vals))))
adh = [lab((r['studie'], r['satz'])) for r in ROWS if r['studie'] in ERW and re.search(r'\badherence\b', r['text'], re.I)]
med = [lab((r['studie'], r['satz'])) for r in ROWS if re.search(r'\bmedian\b', r['text'], re.I)]
res('2d.20', '"adherence" erweitert, "median"', ', '.join(adh) + ' | ' + ', '.join(med), in_nach('2d.20', '({})'.format(', '.join(adh))) and in_nach('2d.20', '„median“ {}'.format(', '.join(med))))
outof = [lab((r['studie'], r['satz'])) for r in ROWS if re.search(r'out of (?:a )?(?:possible )?\d+|\d+ out of \d+ possible', r['text'])]
w('  "out of ... possible" je Teilnehmer:', ', '.join(outof), '· Hilska 7.1 je Team und Woche, Klusemann 1.5 "completed all 12 sessions" (Anzahl Spieler an der vollen Dosis, kein Wert je Spieler)')
bind('Hilska2021', '7.1', r'1\.7 per week in a team', 'Hilska 7.1')
w('')

# ------------------------------------------------------------------ 12 Sammelbefund und Quantor (2d.21)
w('12 Sammelbefund, Ausnahme, Menge des Quantors (2d.21)')
b4k = list(dict.fromkeys(r['studie'] for r in ROWS if r['studie'] in KERN and 'B4' in allc(r)))
CB = json.load(open(CODB, encoding='utf-8'))
b4b, b4bp = [], []
for st in KERN:
    for e in CB[st]:
        cs = [e[1]] + [c for c in e[2].split(SK) if c]
        if 'B4' in cs and st not in b4b:
            b4b.append(st)
        if e[1] == 'B4' and st not in b4bp:
            b4bp.append(st)
res('2d.21', 'B4 Konsens, Codierer B, B primaer', '{} {} {}'.format(len(b4k), len(b4b), len(b4bp)), in_nach('2d.21', 'nach dem Konsens {} Studien, nach Codierer B {}'.format(len(b4k), len(b4b))))
exc = list(dict.fromkeys(r['studie'] for r in ROWS if r['studie'] in KERN and 'B4' in allc(r) and re.search(r'\bexcept\b', r['text'])))
res('2d.21', '"except" in Sammelbefunden', ', '.join(KURZ[s] for s in exc), in_nach('2d.21', '„except“ in Sammelbefunden {} Studien'.format(len(exc))))
# Quantor ueber Tests: eigenes Urteil zur Menge (alle Tests der Studie, auch ueber eine vollstaendige Liste, oder ein Teil)
QT = {
 ('Lloyd2016', '1.2'): 'alle', ('Lloyd2016', '4.1'): 'alle', ('Lloyd2016', '4.2'): 'alle',
 ('Lloyd2016', '2.2'): 'Teil', ('Lloyd2016', '3.2'): 'Teil', ('Lloyd2016', '3.3'): 'Teil',
 ('Hammami2016', '1.1'): 'alle (vollstaendige Liste aller Tests: sprint, agility, RSSA, RCOD)',
 ('Hammami2016', '1.3'): 'Teil', ('Hammami2016', '1.4'): 'Teil',
 ('Beato2018', '4.2'): 'Teil', ('Negra2019', '2.8'): 'Teil',
 ('Negra2020', '1.4'): 'alle', ('Negra2020', '1.5'): 'alle',
 ('Aloui2022', '5.1'): 'Teil', ('Sammoud2024', '2.3'): 'Teil (alle Fitnesstests, ohne Asymmetrie)',
 ('Bouafif2026', '1.1'): 'alle', ('Bouafif2026', '1.2'): 'alle', ('Bouafif2026', '1.3'): 'alle',
}
bind('Hammami2016', '1.1', r'in anthropometric measures, sprint, agility, RSSA, RCOD', 'Hammami 1.1 Liste')
# Eigenes, breiteres Screening der Quantorwoerter in Kern-Befundsaetzen, Abgleich mit der Liste in nachzaehlung_2d.txt Abschnitt 11
QSC = re.compile(r'\b(?:all|any|none|no|both|every|each|most|some|several|remaining|rest|other|only|nearly|always|whole|entire|neither|either|(?:one|two|three|four|five|\d+) of (?:the|its))\b', re.I)
qsc = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and isB(r) and QSC.search(r['text'])]
prot = []
inside = False
for line in open(P2D, encoding='utf-8'):
    if line.startswith('11 '):
        inside = True
        continue
    if inside and line.startswith('12 '):
        break
    m = re.match(r'^    (.+?) (\d\.\d+) \| ', line)
    if inside and m:
        name = {v: k for k, v in KURZ.items()}.get(m.group(1))
        if name:
            prot.append((name, m.group(2)))
extra_q = [k for k in qsc if k not in prot]
w('  Quantorwoerter, eigenes breiteres Screening:', len(qsc), 'Kern-Befundsaetze · Liste in nachzaehlung_2d.txt Abschnitt 11:', len(prot), '· nur im eigenen Screening:', labs(extra_q) or 'keine', '· nur in der Liste:', labs([k for k in prot if k not in qsc]) or 'keine')
for k in extra_q:
    w('    ', lab(k), '|', ', '.join(sorted(set(m.group(0).lower() for m in QSC.finditer(txt(*k))))), '|', kurzsatz(*k, 100))
qa = [k for k, v in QT.items() if v.startswith('alle')]
qt = [k for k, v in QT.items() if v.startswith('Teil')]
w('  Quantor ueber Tests (dieselben 18 Saetze wie 2d):', len(QT), '· alle Tests der Studie', len(qa), '(' + labs(sorted(qa, key=lambda k: ORDER[k])) + ') · Teil', len(qt))
res('2d.21', 'alle / Teil', '{} {}'.format(len(qa), len(qt)), in_nach('2d.21', 'über alle Tests der Studie {}'.format(len(qa))), '2d: 8 / 10, Hammami 1.1 dort als Teil mit Liste, die Liste nennt aber alle Tests')
w('')

# ------------------------------------------------------------------ 13 Klammer am Satzende in Befundsaetzen (Befund § 3.2, nicht in 2d)
w('13 Zusatz: Klammer am Satzende mit Objekt (Befund § 3.2 "22 Saetze, 7 Studien, davon 18 Befundsaetze in 5 Studien")')
kl_end = [(r['studie'], r['satz']) for r in ROWS if r['studie'] in KERN and (lambda m: m and OBJ.search(m.group(1)))(ENDK.search(r['text']))]
kl_b = [k for k in kl_end if isB(BYKEY[k])]
w('  Kern: Klammer am Satzende mit Objekt', len(kl_end), 'Saetze in', len(bystudy(kl_end)), 'Studien, davon Befundsaetze', len(kl_b), 'in', len(bystudy(kl_b)), '(' + ', '.join(KURZ[s] for s in bystudy(kl_b)) + ')')
w('')

# ------------------------------------------------------------------ 14 Volltexte (pypdf)
w('14 Volltexte, unabhaengig mit pypdf gelesen')
for key in ('Klusemann2012', 'Lloyd2016', 'Beato2018', 'Negra2019', 'Moran2024'):
    m5, name = PDFN[key]
    w('  PDF', key, md5(PDFDIR / name), '(gleich Quell_PDF_md5.txt)' if md5(PDFDIR / name) == m5 else '(VERSCHIEDEN)')
def squash(s):
    s = nfc(s).replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', '', s)
def page_variants(key, page):
    t = pdftxt(key, page)
    if key == 'Beato2018':
        t = '\n'.join(re.sub(r'\s*\d{1,3}\s*$', '', l) for l in t.split('\n'))
    a = squash(t)
    b = squash(re.sub(r'-\s*\n\s*', '', t))
    return a, b
VQ = []
for line in open(P2D, encoding='utf-8'):
    m = re.match(r'^  (\w+) PDF-Seite (\d+) \((.*?)\): „(.*)“$', line.rstrip('\n'))
    if m:
        VQ.append((m.group(1), int(m.group(2)), m.group(3), m.group(4)))
okv = 0
for key, pg, ort, q in VQ:
    a, b = page_variants(key, pg)
    qq = squash(q)
    hit = qq in a or qq in b
    okv += hit
    w('  ' + ('ok   ' if hit else 'FEHLT'), key, 'PDF-Seite', pg, '|', q[:80])
w('  Volltextzitate im Protokoll:', len(VQ), '· auf der genannten Seite gefunden:', okv)
# Gedruckte Seiten und Kopf
chk = [
 ('Klusemann S. 2679 auf PDF-Seite 3', 'Klusemann2012', 3, r'OCTOBER 2012 \|\s*2679'),
 ('Lloyd S. 1244 auf PDF-Seite 6', 'Lloyd2016', 6, r'1244\s+Journal of Strength and Conditioning Research'),
 ('Moran 5 / 12 auf PDF-Seite 5', 'Moran2024', 5, r'May 23, 2024\s+5 / 12'),
 ('Negra Kopf des akzeptierten Manuskripts PDF-Seite 11', 'Negra2019', 11, r'by Negra Y et al\.'),
 ('Negra Kopf des akzeptierten Manuskripts PDF-Seite 12', 'Negra2019', 12, r'by Negra Y et al\.'),
]
for name, key, pg, rx in chk:
    w('  ' + ('ok   ' if re.search(rx, pdftxt(key, pg)) else 'FEHLT'), name)
for pg in (11, 12):
    lines = [l.strip() for l in pdftxt('Negra2019', pg).split('\n') if l.strip()]
    w('  Negra PDF-Seite', pg, 'Zeilen nur aus einer Zahl (Seitenzahl):', sum(1 for l in lines if re.fullmatch(r'\d{1,3}', l)))
for pg, n in ((9, '8'), (10, '9'), (12, '11'), (13, '12')):
    first_line = [l.strip() for l in pdftxt('Beato2018', pg).split('\n') if l.strip()][0]
    w('  ' + ('ok   ' if first_line == n else 'FEHLT'), 'Beato PDF-Seite', pg, 'Manuskriptseite', n, '(erste Zeile "' + first_line + '")')
# Beato: Zeilennummern je Zitat aus den Zeilennummern am Zeilenende
def beato_lines(pg):
    seq = []
    for l in pdftxt('Beato2018', pg).split('\n'):
        m = re.match(r'^(.*?)\s*(\d{3})\s*$', l)
        if m and 100 <= int(m.group(2)) <= 400:
            seq.append((int(m.group(2)), m.group(1)))
    return seq
def beato_range(pg, q):
    seq = beato_lines(pg)
    big, owner = '', []
    for n, t in seq:
        s = squash(re.sub(r'-\s*$', '', t))
        big += s
        owner += [n] * len(s)
    qq = squash(q)
    i = big.find(qq)
    if i < 0:
        return None
    return owner[i], owner[i + len(qq) - 1]
def ort_range(ort):
    m = re.search(r'Z\. (\d+)(?: bis (\d+)| (f\.))?', ort)
    if not m:
        return None
    a = int(m.group(1))
    return (a, int(m.group(2))) if m.group(2) else ((a, a + 1) if m.group(3) else (a, a))
for key, pg, ort, q in VQ:
    if key != 'Beato2018':
        continue
    got, exp = beato_range(pg, q), ort_range(ort)
    w('  ' + ('ok   ' if got == exp else 'ANDERS'), 'Beato', ort, '| eigene Zeilen', got)
# Methodenteile
mor = ''.join(pdftxt('Moran2024', p) for p in range(1, 6))
mm = mor[:mor.rfind('\nResults')] if '\nResults' in mor else mor
w('  Moran Seiten 1 bis 5 vor "Results": trivial', len(re.findall('trivial', mm, re.I)), '· smallest worthwhile', len(re.findall('smallest worthwhile', mm, re.I)), '· threshold', len(re.findall('threshold', mm, re.I)), '· 0.2', len(re.findall(r'\b0\.2\b', mm)))
morall = ''.join(pdftxt('Moran2024', p) for p in range(1, 13))
w('  Moran ganzes PDF: "trivial" nur in', sorted(set(p for p in range(1, 13) if re.search('trivial', pdftxt('Moran2024', p), re.I))), '(Ergebnisse, Seite 5), Schwellenangaben wie "<0.2" oder "smallest worthwhile":', len(re.findall(r'smallest worthwhile|<\s*0\.2|0\.2\s*[-–]', morall)))
bea = ''.join(pdftxt('Beato2018', p) for p in range(1, 24))
bsub = sorted(set(p for p in range(1, 24) if 'substantial' in squash(pdftxt('Beato2018', p)).lower()))
meth = squash(pdftxt('Beato2018', 9) + pdftxt('Beato2018', 10).split('Results')[0])
w('  Beato "substantial" (ohne Leerraum gesucht) auf PDF-Seiten:', bsub, '· im Methodenteil (PDF-Seite 9 und Seite 10 vor "Results"):', meth.lower().count('substantial'))
neg = pdftxt('Negra2019', 11)
w('  Negra 2019 PDF-Seite 11, zweite Regel fuer "unclear" ueber Chancen:', 'ja' if re.search(r'considered\s*unclear\s*when\s*the\s*chance\s*of\s*a\s*beneficial', re.sub(r'\s+', ' ', neg)) else 'nein', '(">25%" Nutzen und ">0.5%" Schaden, Odds Ratio etwa 60)')
llo = pdftxt('Lloyd2016', 6)
w('  Lloyd S. 1244: MBI fuer die Reifegruppen je Trainingsform ("differences in the training response between pre- and post-PHV groups"):', 'ja' if re.search(r'training\s*response\s*between\s*pre-\s*and\s*post-\s*PHV\s*groups', re.sub(r'\s+', ' ', llo)) else 'nein')
w('  Lloyd Abb. 1 Legende "U = unclear":', 'ja' if 'U = unclear' in re.sub(r'\s+', ' ', llo) else 'nein', '(Sichtpruefung der Abbildung: U bei COM, 20 m)')
w('  Beato Abb. 2 (PDF-Seite 23, Bild ohne Textschicht, Sichtpruefung): Long jump Possible, Triple hop right Likely trivial, Triple hop left Most likely trivial, Sprint 10, 30, 40 m Unclear, 505 COD Trivial')
w('')

# ------------------------------------------------------------------ 15 Zitate am Ort (eigene Ortsauflösung)
w('15 Zitate der Spalte Korpusaussage am genannten Ort (eigene Ortsauflösung)')
BL = open(BEF, encoding='utf-8').read().split('\n')
def befort(spec):
    m = re.fullmatch(r'(\d+(?:\.\d+)?)(?: Nr\. (\d+)| (K\d+))?', spec)
    if not m:
        return None
    hs = [i for i, l in enumerate(BL) if re.match(r'^#+ ' + re.escape(m.group(1)) + r' ', l)]
    if len(hs) != 1:
        return None
    lvl = len(BL[hs[0]]) - len(BL[hs[0]].lstrip('#'))
    end = len(BL)
    for j in range(hs[0] + 1, len(BL)):
        mm = re.match(r'^(#+) ', BL[j])
        if mm and len(mm.group(1)) <= lvl:
            end = j
            break
    part = BL[hs[0] + 1:end]
    if m.group(2):
        part = [l for l in part if re.match(r'^' + m.group(2) + r'\. ', l)]
    if m.group(3):
        part = [l for l in part if re.match(r'^\| ' + m.group(3) + r' \|', l)]
    return spaces(' '.join(part))
T2BR = {r[0]: spaces(' '.join(r)) for r in csv.reader(open(T2B, encoding='utf-8'), delimiter=SK)}
T2CR = {r[0]: spaces(' '.join(r)) for r in csv.reader(open(T2C, encoding='utf-8'), delimiter=SK)}
def at_boundary(text, frag, start):
    while True:
        i = text.find(frag, start)
        if i < 0:
            return -1
        pre = text[i - 1] if i > 0 else ' '
        post = text[i + len(frag)] if i + len(frag) < len(text) else ' '
        okl = not (frag[0].isalnum() and pre.isalnum())
        okr = not (frag[-1].isalnum() and post.isalnum())
        if okl and okr:
            return i + len(frag)
        start = i + 1
nq, nok = 0, 0
for nr in TROWS:
    cell = TROWS[nr]['Korpusaussage (Wortlaut am Ort)']
    for m in re.finditer(r'„(.*?)“ \(((?:Befund § [^()]+)|(?:2[bc]\.\d+))\)', cell):
        q = m.group(1).replace('‚', '„').replace('‘', '“')
        ort = m.group(2)
        if ort.startswith('Befund § '):
            src = befort(ort[len('Befund § '):])
        else:
            src = T2BR.get(ort) if ort.startswith('2b') else T2CR.get(ort)
        pos, good = 0, src is not None
        for frag in q.split(' … '):
            if not good:
                break
            pos = at_boundary(src, spaces(frag), pos)
            good = pos >= 0
        nq += 1
        nok += good
        if not good:
            w('  FEHLT', nr, ort, '|', q[:80])
w('  Zitate geprueft:', nq, '· am Ort an Wortgrenzen in Folge gefunden:', nok)
# Zahl laut Befund gegen den Ort
w('  Zahlen der Spalte "Zahl laut Befund", die im zitierten Wortlaut fehlen (nur ausserhalb der Zitate belegt):')
for nr in TROWS:
    z = TROWS[nr]['Zahl laut Befund']
    cell = TROWS[nr]['Korpusaussage (Wortlaut am Ort)']
    nums = re.findall(r'\b\d+(?:\.\d+)?\b', z)
    missing = [x for x in nums if x not in cell]
    if missing:
        w('    ', nr, '| Zahl laut Befund:', z, '| nicht im Zitat:', ', '.join(dict.fromkeys(missing)))
w('')

# ------------------------------------------------------------------ 16 Teiltabelle: Ergebnis, Befundstelle
w('16 Teiltabelle 2d: Befundstelle und Ergebnis')
ms = collections.Counter(TROWS[nr]['Befundstelle'].split(' · ')[0] for nr in TROWS)
w('  Massstab vorn:', dict(ms), '· Konvention (Fortsetzung 3 § 5 Nr. 6): "Korpus, Fundstelle oder beides"')
er = collections.Counter(TROWS[nr]['Ergebnis'].split(' (')[0] for nr in TROWS)
w('  Ergebnis:', dict(er))
w('')

# ------------------------------------------------------------------ 17 Konventionen
w('17 Konventionen')
for p in (S2D, P2D, M2D):
    w('  Semikolon in', p.name + ':', p.read_text(encoding='utf-8').count(SK))
raw = T2D.read_text(encoding='utf-8').split('\n')
raw = [l for l in raw if l]
w('  teiltabelle_2d.csv:', len(raw), 'Zeilen, Trennzeichen je Zeile', sorted(set(l.count(SK) for l in raw)), '· Felder in Anfuehrung', sum(1 for l in raw if '"' in l))
mdrows = [l for l in M2D.read_text(encoding='utf-8').split('\n') if l.startswith('| ') and not l.startswith('|---')]
mdcells = [[c.strip() for c in l.strip().strip('|').split(' | ')] for l in mdrows]
csvcells = [[c.replace('|', '/') for c in r] for r in TD]
w('  teiltabelle_2d.md gegen .csv: Zeilen', len(mdcells), 'gegen', len(csvcells), '· Zellen gleich', mdcells == csvcells)
src = S2D.read_text(encoding='utf-8')
tmpl = re.findall(r"\bnach='((?:[^'\\]|\\.)*)'", src)
w('  Vorlagen der Spalte Nachzaehlung im Quelltext:', len(tmpl))
for i, t in enumerate(tmpl, 1):
    lit = re.sub(r'\{\}', ' ', t)
    lit = re.sub(r'„[^“]*“', ' ', lit)
    refs = re.findall(r'(?:Lloyd|Hammami|Beato|Negra 20\d\d|Negra|Aloui|Liu|Moran|Sammoud|Bouafif|Hilska|Klusemann|Veith|Rogers|Asimakidis)(?: \d\.\d+(?:,? (?:und )?\d\.\d+)*)?|\(\d\.\d+(?:, \d\.\d+)+\)|\d\.\d+ vor \d\.\d+|(?<![\w.,])\d\.\d(?![\w.%])', lit)
    nums = re.findall(r'(?<![\w.])\d+(?:,\d+)?(?:/\d+/\d+)?(?![\w.])', lit)
    if refs or nums:
        w('    Vorlage', i, '| Satzangaben von Hand:', ', '.join(dict.fromkeys(x for x in refs if re.search(r'\d', x))) or '-', '| Zahlen von Hand:', ', '.join(dict.fromkeys(nums)) or '-')
w('')

# ------------------------------------------------------------------ 18 Zusammenfassung
w('18 Abgleich eigener Werte mit der Spalte Nachzaehlung')
nab = 0
for nr, items in RES.items():
    for wert, eigen, gleich, notiz in items:
        if not gleich:
            nab += 1
            w('  ABWEICHEND', nr, wert, '| eigen', eigen, '|', notiz)
w('  Werte verglichen:', sum(len(v) for v in RES.values()), '· abweichend:', nab)
w('')

# ------------------------------------------------------------------ 19 Zusatz zu Befund A1: Zaehlung von 2c bei "abgewandelt" fuer 2c.21 und 2c.22
# Angehaengt, damit die Zeilennummern der Abschnitte 0 bis 18 gleich bleiben. Liest die Zaehlung je Satz aus
# Abgleichbefund § 3.3, rechnet sie mit den Wortzahlen aus textstand.json nach und verschiebt die Saetze von
# 2c.21 und 2c.22 von "nur erweitert" nach "abgewandelt".
TST = C / '03_Skripte' / 'Abgleich_Ergebnisse_2026-10-03' / 'textstand.json'
if not TST.exists():
    halt('fehlt ' + str(TST))
w('19 Zusatz zu Befund A1: Zaehlung von 2c, wenn 2c.21 und 2c.22 "abgewandelt" sind')
w('  ' + str(TST.relative_to(UP)), md5(TST))
TS = json.load(open(TST, encoding='utf-8'))
WOE = {}
for a in TS['absaetze']:
    for s in a['saetze']:
        WOE[s['id']] = s['woerter']
w('  Saetze in textstand.json:', len(WOE), '· Woerter:', sum(WOE.values()), '(Messung: ' + str(TS['messung']['woerter']) + ')')
abgt = ABG.read_text(encoding='utf-8')
mz = re.search(r'Je Satz \(Teil A, (\d+) Wörter\): (.*?)\. (\d+) Sätze mit (\d+) von \d+ Wörtern nutzen einen Kernbaustein', abgt)
if not mz:
    halt('Zaehlung je Satz in Abgleichbefund § 3.3 nicht gefunden')

def sids(spec):
    out, para = [], None
    for tok in spec.split(', '):
        m = re.fullmatch(r'(?:(A\d) )?S(\d+)(?: bis S(\d+))?', tok.strip())
        if not m:
            halt('Satzangabe nicht lesbar: ' + tok)
        para = m.group(1) or para
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        out += [para + ' S' + str(i) for i in range(lo, hi + 1)]
    return out

KL = {}
for m in re.finditer(r'(wie Muster|abgewandelt|nur erweitert|kein Muster) (\d+)(?: Sätze)? mit (\d+)(?: Wörtern)? \(([^)]*)\)', mz.group(2)):
    ids = sids(m.group(4))
    summe = sum(WOE[i] for i in ids)
    KL[m.group(1)] = ids
    w('  laut § 3.3:', m.group(1), m.group(2), 'Saetze mit', m.group(3), '| nachgerechnet', len(ids), 'mit', summe, '|', 'gleich' if (len(ids), summe) == (int(m.group(2)), int(m.group(3))) else 'VERSCHIEDEN')
kb = KL['wie Muster'] + KL['abgewandelt']
w('  laut § 3.3: Kernbaustein', mz.group(3), 'Saetze mit', mz.group(4), '| nachgerechnet', len(kb), 'mit', sum(WOE[i] for i in kb), '|', 'gleich' if (len(kb), sum(WOE[i] for i in kb)) == (int(mz.group(3)), int(mz.group(4))) else 'VERSCHIEDEN')
T2CR = list(csv.reader(open(T2C, encoding='utf-8'), delimiter=SK))
neu = []
for r in T2CR[1:]:
    if r[0] in ('2c.21', '2c.22'):
        sid = re.match(r'(A\d S\d+)', r[3]).group(1)
        w('  ' + r[0], '| Satz', sid, '|', WOE[sid], 'Woerter | Status:', r[5])
        if not r[5].startswith('Korpus: nur erweitert'):
            halt('Status von ' + r[0])
        neu.append(sid)
abg2 = KL['abgewandelt'] + neu
ne2 = [i for i in KL['nur erweitert'] if i not in neu]
kb2 = KL['wie Muster'] + abg2
w('  danach je Satz: abgewandelt', len(abg2), 'mit', sum(WOE[i] for i in abg2), '· nur erweitert', len(ne2), 'mit', sum(WOE[i] for i in ne2), '· Kernbaustein', len(kb2), 'Saetze mit', sum(WOE[i] for i in kb2), 'von', mz.group(1), 'Woertern')
stc = collections.Counter(re.match(r'Korpus: (wie Muster|abgewandelt|nur erweitert|kein Muster)', r[5]).group(1) for r in T2CR[1:])
w('  Zeilen von 2c:', len(T2CR) - 1, '· Korpus jetzt', dict(stc), '· danach abgewandelt', stc['abgewandelt'] + len(neu), '· nur erweitert', stc['nur erweitert'] - len(neu))

text = '\n'.join(OUT) + '\n'
if SK in text:
    halt('Semikolon in der Ausgabe')
(HERE / 'zweitpruefung_2d_nachrechnung.txt').write_text(text, encoding='utf-8')
print('zweitpruefung_2d_nachrechnung:', sum(len(v) for v in RES.values()), 'Werte,', nab, 'abweichend')

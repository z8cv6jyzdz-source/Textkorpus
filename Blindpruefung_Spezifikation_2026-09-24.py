# -*- coding: utf-8 -*-
"""Blindprüfung der Spezifikation (Auswertungsverfahren, Schritt 2.2), maschinell.

Zweck      Prüfen, ob die Spezifikation vom 24.09.2026 (Stand Nachtrag 3) oder eine ihrer
           CSV-Anlagen eine Zahl aus den Studiendaten oder aus der ersten Rechnung enthält,
           und ob der Text auf Ergebnisse der ersten Rechnung anspielt.
Schritt    Auswertungsverfahren 2.2. Auftrag des Verfassers vom 24.09.2026:
           „Claude prüft maschinell“, Bestätigung durch den Verfasser danach.
           Erster Lauf auf Stand Nachtrag 1 (F.6), zweiter Lauf auf Stand Nachtrag 2 (F.7),
           dritter Lauf am 25.09.2026 auf Stand Nachtrag 3 (F.8, vier Klarstellungen aus der
           Code-Durchsicht 6.2). Seit dem dritten Lauf zusätzlich als Studienquellen: die
           Ergebnisdateien beider Implementierungen (R und Python), die Laufprotokolle der
           Gegenprobe und der Plausibilitätsprüfung, die drei Protokolle der Phase 6, der
           Auswertungsplan mit Register (R11 nennt Ergebnisse), die Rechenprobe der Handprobe
           und die Projektanweisungen Fassung 14.
Verfahren  (1) Alle Zahlen der Studienquellen einsammeln: Workbook (alle Blätter außer
               05_KhamisRoche, numerische Zellen auf 0 bis 4 Nachkommastellen gerundet),
               Ausgaben der Rechenkette B0 bis B9 und F1, Analyseprotokolle 12.09. und 15.09.,
               Kennzahlenblätter 15.09. und 22.09., Projektanweisungen Fassung 12 und 13,
               ancova_ergebnisse.csv. Seit dem zweiten Lauf zusätzlich die Dokumente, die nach
               der ersten Rechnung entstanden sind und sie erwähnen: Voraussetzungsprüfungen
               (24.09.), SPSS-Vorgehen (24.09.), Auswertungs- und Berichtsumfang (24.09.).
           (2) Jede Zahl der Spezifikation (Anlage _Zahlenliste.csv) und jede Zahl der
               Anlagen Konstanten, Koeffizienten_KR, Referenzdaten, Referenzdaten_Daten,
               Fragebogen, Vokabular und Kennungen damit vergleichen. Verglichen werden nur
               unterscheidungskräftige Zahlen: Dezimalzahlen mit mindestens drei
               signifikanten Stellen oder mit zwei Stellen ab 10, ganze Zahlen ab 13
               ohne Jahreszahlen.
           (3) Direktscan des Spezifikationstexts gegen die Zahlenliste: Jede
               unterscheidungskräftige Zahl des Texts muss in der Zahlenliste stehen.
           (4) Zeilenabgleich mit der Fassung vor dem jeweiligen Nachtrag: Treffer in
               unveränderten Zeilen sind in den früheren Läufen beurteilt, Treffer in neuen oder
               geänderten Zeilen werden im laufenden Lauf beurteilt. Im dritten Lauf ist die
               Vergleichsfassung der Stand Nachtrag 2.
           (5) Stichwortsuche im Text nach Bezügen auf die erste Rechnung.
Eingang    siehe Liste EINGANG unten, SHA-256 in der Ausgabe
Ausgabe    Blindpruefung_Spezifikation_2026-09-24.txt (Zusammenfassung ohne Kontexte aus
           Studienquellen)
           Blindpruefung_Spezifikation_2026-09-24_Treffer.csv (jeder Treffer mit Kontext
           beider Seiten). Die Trefferliste enthält Kontexte aus Studienquellen und gehört
           nicht in den Blindordner.
Fassung    25.09.2026, dritter Lauf (Nachtrag 3). Zweite Fassung vom 24.09.2026 im _Archiv
Aufruf     python3 Blindpruefung_Spezifikation_2026-09-24.py
           Die Pfade beziehen sich auf die Cowork-Arbeitsumgebung, in die die Dateien aus dem
           Ordner Bachelorarbeit gestaged wurden (U = Ordner Bachelorarbeit). SPEC_DIR enthält
           die Spezifikation im zu prüfenden Stand (Nachtrag 3), ALT_MD die Fassung Nachtrag 2
           (archiviert als Claude\\_Archiv\\_ersetzt_2026-09-25_Nachtrag3\\Spezifikation_2026-09-24.md).
           Die Zusatzquellen liegen in ZUSATZ_DIR als Textkopie (docx über pandoc).
"""
import csv, re, glob, os, hashlib, collections
from decimal import Decimal, InvalidOperation
import openpyxl

U = '/mnt/user-data/uploads/Bachelorarbeit/'
SPEC_DIR = '/home/claude/spez/'
ALT_MD = SPEC_DIR + 'alt_Spezifikation_2026-09-24.md'
ZUSATZ_DIR = SPEC_DIR + 'quellen/'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'
STAMM = 'Blindpruefung_Spezifikation_2026-09-24'

NUM = re.compile(r'(?<![\w.,])[-−–]?\d+(?:[.,]\d+)?(?![\w])')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 16), b''):
            h.update(b)
    return h.hexdigest()

def canon(tok):
    t = tok.replace('−', '-').replace('–', '-').strip()
    neg = t.startswith('-')
    t = t.lstrip('-')
    if re.fullmatch(r'\d{1,3}\.\d{3}', t):   # deutsches Tausenderformat 9.814
        t = t.replace('.', '')
    t = t.replace(',', '.')
    try:
        d = Decimal(t)
    except InvalidOperation:
        return None
    d = d.normalize()
    return ('-' if neg and d != 0 else '') + format(d, 'f')

def sig_digits(c):
    return len(c.lstrip('-').replace('.', '').lstrip('0'))

def distinctive(c):
    if c is None:
        return False
    v = abs(Decimal(c))
    if '.' in c:
        return sig_digits(c) >= 3 or (sig_digits(c) >= 2 and v >= 10)
    iv = int(v)
    return iv >= 13 and not (1900 <= iv <= 2100)

# ---------- Eingang ----------
STUDIE_TXT = sorted(glob.glob(U + 'Claude/03_Skripte/Auswertung_*.txt')) + [
    U + 'Claude/02_Befunde/Analyseprotokoll_2026-09-15.md',
    U + 'Claude/02_Befunde/Analyseprotokoll_2026-09-12.md',
    U + 'Claude/02_Befunde/Kennzahlen_2026-09-15.md',
    U + 'Claude/02_Befunde/Kennzahlen_2026-09-22.md',
    U + 'Claude/00_Steuerung/Projektanweisungen_Fassung12.md',
    U + 'Auswertung/ancova_ergebnisse.csv']
ZUSATZ = [
    ZUSATZ_DIR + 'Projektanweisungen_Fassung13.md',
    ZUSATZ_DIR + 'Projektanweisungen_Fassung14.md',
    ZUSATZ_DIR + 'Voraussetzungspruefungen_Literaturbefund_2026-09-24.md',
    ZUSATZ_DIR + 'SPSS_Auswertung_Vorgehen_2026-09-24.txt',
    ZUSATZ_DIR + 'Auswertungs_und_Berichtsumfang_2026-09-24.md',
    ZUSATZ_DIR + 'Ergebnisse_R_2026-09-25.csv',
    ZUSATZ_DIR + 'Ergebnisse_Python_2026-09-25.csv',
    ZUSATZ_DIR + 'Gegenprobe_Python_2026-09-25.txt',
    ZUSATZ_DIR + 'Plausibilitaet_2026-09-25.txt',
    ZUSATZ_DIR + 'Abgleichprotokoll_2026-09-25.md',
    ZUSATZ_DIR + 'Durchsichtsprotokoll_2026-09-25.md',
    ZUSATZ_DIR + 'Plausibilitaetsprotokoll_2026-09-25.md',
    ZUSATZ_DIR + 'Auswertungsplan_2026-09-12.md',
    ZUSATZ_DIR + 'Handprobe_Pruefung_2026-09-25.txt']
WORKBOOK = U + 'Statistik/Studiendaten_U15_gesamt.xlsx'
SPEC_MD = SPEC_DIR + 'Spezifikation_2026-09-24.md'
ZAHLENLISTE = SPEC_DIR + 'Spezifikation_2026-09-24_Zahlenliste.csv'
ANLAGEN = ['Konstanten', 'Koeffizienten_KR', 'Referenzdaten', 'Referenzdaten_Daten', 'Fragebogen', 'Vokabular', 'Kennungen']
ANLAGE_DIR = {a: U + 'Claude/02_Befunde/' for a in ANLAGEN}
ANLAGE_DIR['Kennungen'] = SPEC_DIR          # Stand Nachtrag 2, mit Nachtrag 3 unverändert
ANLAGE_PFAD = {a: ANLAGE_DIR[a] + 'Spezifikation_2026-09-24_' + a + '.csv' for a in ANLAGEN}
EINGANG = STUDIE_TXT + ZUSATZ + [WORKBOOK, SPEC_MD, ALT_MD, ZAHLENLISTE] + [ANLAGE_PFAD[a] for a in ANLAGEN]

# ---------- Studienquellen ----------
study = {}
def add(c, quelle, ctx):
    if c is None:
        return
    study.setdefault(c, [])
    if len(study[c]) < 6:
        study[c].append((quelle, ctx[:140]))

for p in STUDIE_TXT + ZUSATZ:
    txt = open(p, encoding='utf-8', errors='replace').read()
    for m in NUM.finditer(txt):
        a, b = max(0, m.start() - 60), min(len(txt), m.end() + 60)
        add(canon(m.group(0)), os.path.basename(p), txt[a:b].replace('\n', ' '))

wb = openpyxl.load_workbook(WORKBOOK, data_only=True)
for ws in wb.worksheets:
    if ws.title == '05_KhamisRoche':
        continue   # veröffentlichte Koeffizienten, keine Studiendaten
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if isinstance(v, bool) or v is None:
                continue
            if isinstance(v, (int, float)):
                for nd in (0, 1, 2, 3, 4):
                    r = round(v, nd)
                    add(canon(repr(r) if nd else str(int(round(v)))), 'Workbook ' + ws.title, f'{cell.coordinate} = {v}')
            elif isinstance(v, str):
                for m in NUM.finditer(v):
                    add(canon(m.group(0)), 'Workbook ' + ws.title, f'{cell.coordinate}: {v[:80]}')

# ---------- Zeilenabgleich mit der Fassung vor dem Nachtrag (hier Nachtrag 2) ----------
spec_lines = open(SPEC_MD, encoding='utf-8').read().split('\n')
alt_lines = set(open(ALT_MD, encoding='utf-8').read().split('\n'))
def zeilenstatus(nr):
    return 'unverändert' if spec_lines[int(nr) - 1] in alt_lines else 'neu oder geändert'

# ---------- Vergleich ----------
hits = []
zl = list(csv.DictReader(open(ZAHLENLISTE, encoding='utf-8')))
for r in zl:
    c = canon(r['zahl'])
    if distinctive(c) and c in study:
        hits.append(('Spezifikation', r['zeile'], r['zahl'], r['art'], r['herkunft'], r['textumgebung'][:140], study[c], zeilenstatus(r['zeile'])))

for a in ANLAGEN:
    rows = list(csv.reader(open(ANLAGE_PFAD[a], encoding='utf-8')))
    head = rows[0]
    for i, row in enumerate(rows[1:], start=2):
        for j, cell in enumerate(row):
            if a == 'Kennungen' and head[j] == 'kennung':
                continue   # Kennung ist die Zusammensetzung der Felder, Ziffern darin sind Codes
            for m in NUM.finditer(cell):
                c = canon(m.group(0))
                if distinctive(c) and c in study:
                    st = 'neu' if a == 'Kennungen' else 'unverändert'
                    hits.append(('Anlage ' + a, str(i), m.group(0), head[j] if j < len(head) else '', '', ' | '.join(row)[:140], study[c], st))

with open(OUT + STAMM + '_Treffer.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['ort', 'zeile', 'zahl', 'art_oder_spalte', 'herkunft_laut_zahlenliste', 'zeilenstatus', 'kontext_spezifikation', 'studienquelle_1', 'kontext_studie_1', 'weitere_quellen'])
    for h in hits:
        q = h[6]
        w.writerow([h[0], h[1], h[2], h[3], h[4], h[7], h[5], q[0][0], q[0][1], ' · '.join(sorted({x[0] for x in q[1:]}))])

# ---------- Direktscan Text gegen Zahlenliste ----------
# (a) Zerlegung des Texts nach der Regel der Zahlenliste (Datum, Uhrzeit, Exponent, Zahl) und
#     Abgleich mit ihren Zeilen. (b) Jede unterscheidungskräftige Zahl nach NUM muss in einem
#     Vorkommen der Zahlenliste liegen.
TOK = re.compile(r'''(?<![A-Za-zÄÖÜäöüß0-9.,\-])(
   \d{1,2}\.\d{1,2}\.(?:\d{4})?(?!\d)
 | \d{1,2}:\d{2}(?::\d{2})?
 | \d+e-\d+
 | \d+(?:[.,]\d+)?
)''', re.X)
zl_zeile = collections.defaultdict(list)
for r in zl:
    zl_zeile[r['zeile']].append(r['zahl'])
liste_abw = []
direkt_fehlt = []
for i, line in enumerate(spec_lines, start=1):
    toks = [(m.group(1), m.start(1), m.end(1)) for m in TOK.finditer(line)]
    if collections.Counter(t[0] for t in toks) != collections.Counter(zl_zeile.get(str(i), [])):
        liste_abw.append(i)
    for m in NUM.finditer(line):
        c = canon(m.group(0))
        if not distinctive(c):
            continue
        s0 = m.start() + (1 if m.group(0)[0] in '-−–' else 0)
        if not any(a <= s0 < b for _, a, b in toks):
            direkt_fehlt.append((i, m.group(0), line[max(0, m.start() - 40):m.end() + 30]))

# ---------- Stichwortsuche ----------
STICHWORTE = ['15.09', 'Python', 'erste Rechnung', 'ersten Rechnung', 'Vorprüfung', 'erweitert',
              'schief', 'verworfen', 'Kennzahlenblatt', 'Kennzahlen', 'Analyseprotokoll', 'SPSS',
              'Sitzungsnotizen', 'Teil 0', 'Rev. ', 'Nullbefund', 'Gruppenunterschied', 'signifikant',
              'Ergebnis der', 'ancova_ergebnisse', 'Berichtsumfang']
stich = []
for i, line in enumerate(spec_lines, start=1):
    for s in STICHWORTE:
        for m in re.finditer(re.escape(s), line):
            a, b = max(0, m.start() - 70), min(len(line), m.end() + 70)
            stich.append((i, s, line[a:b], 'unverändert' if line in alt_lines else 'neu oder geändert'))

# ---------- Zusammenfassung ----------
L = []
L.append('BLINDPRÜFUNG DER SPEZIFIKATION (Auswertungsverfahren 2.2), maschinell')
L.append('Fassung 25.09.2026, dritter Lauf · Spezifikation Stand Nachtrag 3 (F.8)')
L.append('')
L.append('EINGANG (SHA-256)')
for p in EINGANG:
    L.append(f'  {sha(p)}  {p.replace(U, "").replace(ZUSATZ_DIR, "Textkopie/").replace(SPEC_DIR, "02_Befunde/")}')
L.append('')
L.append(f'Studienzahlen (kanonisch): {len(study)}')
L.append(f'Zahlenvorkommen in der Spezifikation (Zahlenliste): {len(zl)}')
L.append(f'Zeilen der Spezifikation: {len(spec_lines) - (1 if spec_lines[-1] == "" else 0)}, davon neu oder geändert gegenüber Nachtrag 2: {sum(1 for l in spec_lines if l not in alt_lines)}')
L.append(f'Treffer gesamt: {len(hits)}')
for ort, n in collections.Counter(h[0] for h in hits).most_common():
    L.append(f'  {ort}: {n}')
L.append('')
L.append('DIREKTSCAN')
L.append(f'  Zeilen, deren Zahlen nicht mit der Zahlenliste übereinstimmen: {len(liste_abw)}' + (' (' + ', '.join(map(str, liste_abw)) + ')' if liste_abw else ''))
L.append('  Unterscheidungskräftige Zahlen im Text außerhalb der Zahlenliste:')
if direkt_fehlt:
    for i, z, ctx in direkt_fehlt:
        L.append(f'  {i} · {z} · …{ctx}…')
else:
    L.append('  keine')
L.append('')
spec_hits = [h for h in hits if h[0] == 'Spezifikation']
for status in ('unverändert', 'neu oder geändert'):
    sub = [h for h in spec_hits if h[7] == status]
    L.append(f'TREFFER IM SPEZIFIKATIONSTEXT, Zeilen {status}: {len(sub)} Vorkommen, nach Art (Zahlenliste, Teil H)')
    by_art = collections.defaultdict(list)
    for h in sub:
        by_art[h[3]].append(h[2])
    for art, zs in sorted(by_art.items(), key=lambda x: -len(x[1])):
        L.append(f'  {art}: {len(zs)} Vorkommen, Zahlen: ' + ', '.join(sorted(set(zs), key=lambda z: (len(z), z))))
    L.append('')
L.append('TREFFER IN NEUEN ODER GEÄNDERTEN ZEILEN, einzeln (Zeile · Zahl · Art · Umgebung im Spezifikationstext)')
for h in spec_hits:
    if h[7] == 'neu oder geändert':
        L.append(f'  {h[1]} · {h[2]} · {h[3]} · …{h[5][:110]}…')
L.append('')
L.append('TREFFER IN DEN ANLAGEN NACH SPALTE')
for a in ANLAGEN:
    c = collections.Counter(h[3] for h in hits if h[0] == 'Anlage ' + a)
    if c:
        L.append(f'  {a}: ' + ', '.join(f'{k} {v}' for k, v in c.most_common()))
    else:
        L.append(f'  {a}: keine')
kh = [h for h in hits if h[0] == 'Anlage Kennungen']
L.append('')
L.append('ANLAGE KENNUNGEN, Treffer nach Zahl und Spalte (Zahl · Spalte · Zahl der Zeilen · Beispiel)')
grp = collections.defaultdict(list)
for h in kh:
    grp[(h[2], h[3])].append(h)
for (z, sp), hs in sorted(grp.items(), key=lambda x: (x[0][1], len(x[0][0]), x[0][0])):
    L.append(f'  {z} · {sp} · {len(hs)} · {hs[0][5][:100]}')
L.append('')
L.append('STICHWORTSUCHE IM TEXT (Zeile · Stichwort · Zeilenstatus · Umgebung)')
for i, s, ctx, st in stich:
    L.append(f'  {i} · {s} · {st} · …{ctx}…')
L.append('')
L.append('Urteil je Treffer: siehe Vermerk 02_Befunde/Blindpruefung_Spezifikation_2026-09-24, Teil C (Nachtrag 3).')
open(OUT + STAMM + '.txt', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))

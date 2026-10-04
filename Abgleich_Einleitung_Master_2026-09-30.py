# -*- coding: utf-8 -*-
"""
Abgleich_Einleitung_Master_2026-09-30.py — Task 11, Schritt 0 (Plan Nachtrag 30.09., Rev. 134)

Gleicht die vom Verfasser übertragene Einleitung im Master gegen den freigegebenen Wortlaut ab:
`04_Uebergaben\\Textvorschlag_Einleitung_Ueberarbeitung_2026-09-30.md` § 5.1 (sechs Absätze B1a bis B5, 930 Wörter).
Ohne die aufgeschobenen Nachträge (G35 a, i, k, l, H12, I20, T1, T4), die folgen mit der Schlussfassung der Einleitung.

Prüft je Absatz: (1) Wortgleichheit exakt, (2) sonst nach Normalisierung (NFC, Leerraum, geschützte Leerzeichen,
typografische Anführungs- und Apostrophzeichen) mit Wortdiff, (3) Direktformatierung der Runs (fett, kursiv,
unterstrichen, Farbe, Schrift, Größe, Hervorhebung) und Absatzformat (Formatvorlage, Einzug, Ausrichtung),
(4) Kennungen B1a bis B5 im Text, (5) Leerabsätze im Abschnitt.
Misst wie Manuskriptstand_2026-09-25.py (Wörter = Leerraum-Token mit Belegklammern, Satzteilung saetze() unverändert),
dazu Semikola und Doppelpunkte außerhalb der Belegklammern, nummerierte Abschnittsverweise, Belegklammern.
Meldet, was außer der Einleitung zur Übertragung gehört (Rev. 134, Offen Nr. 1): Überschriften „2 Theoretischer
Hintergrund und Forschungsstand“ bis „3 Fragestellung und Hypothesen“ samt Text gelöscht (M24).
Aufruf: python Abgleich_Einleitung_Master_2026-09-30.py <Master.docx> <Textvorschlag.md> <Ausgabe.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import hashlib
import os
import statistics
import unicodedata
import difflib
from docx import Document
from docx.oxml.ns import qn

SRC, TV, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SEMI = chr(59)
FOLGE = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']
SOLL_W = {'B1a': 153, 'B1b': 152, 'B2': 229, 'B3': 121, 'B4': 176, 'B5': 99}   # § 5.2 Spalte „freigegeben“
RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')
KLAMMER = re.compile(r'\([^()]*\d{4}[^()]*\)')


def saetze(text):  # unverändert aus Manuskriptstand_2026-09-25.py (Fassung 3)
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


def norm(t):
    t = unicodedata.normalize('NFC', t)
    for a, b in [(' ', ' '), (' ', ' '), (' ', ' '), ('’', "'"), ('‘', "'"), ('‚', "'"),
                 ('“', '"'), ('”', '"'), ('„', '"'), ('­', '')]:
        t = t.replace(a, b)
    return re.sub(r'\s+', ' ', t).strip()


def ohne_klammern(t):
    return KLAMMER.sub('', t)


def ohne_belege(t):  # wie schritt4_messung.py
    return re.sub(r'\s+', ' ', KLAMMER.sub('', t)).replace(' .', '.').replace(' ,', ',').strip()


def de(x, nk=1):
    return (('%.' + str(nk) + 'f') % x).replace('.', ',')


# 1 Maßstab: § 5.1 des Textvorschlags
md = open(TV, encoding='utf-8').read()
m = re.search(r'### 5\.1 Wortlaut\s*\n(.*?)\n### 5\.2', md, re.S)
assert m, '§ 5.1 nicht gefunden'
teil = m.group(1)
SOLL = {}
for k in FOLGE:
    mm = re.search(r'\*\*' + k + r'\*\*\s*\n\s*\n(.+?)(?:\n\s*\n|\Z)', teil, re.S)
    assert mm, 'Absatz %s nicht gefunden' % k
    SOLL[k] = mm.group(1).strip()
for k in FOLGE:
    assert len(SOLL[k].split()) == SOLL_W[k], (k, len(SOLL[k].split()))
assert sum(SOLL_W.values()) == 930

# 2 Master: Absätze unter „1 Einleitung“ bis zur nächsten Überschrift
raw = open(SRC, 'rb').read()
d = Document(SRC)
paras = d.paragraphs
start = next(i for i, p in enumerate(paras) if p.style.name == 'Heading 1' and p.text.strip() == '1 Einleitung')
ende = next(i for i in range(start + 1, len(paras)) if paras[i].style.name.startswith('Heading'))
ist_p = [(i, paras[i]) for i in range(start + 1, ende)]
leer = [i for i, p in ist_p if not p.text.strip()]
ist = [(i, p) for i, p in ist_p if p.text.strip()]

z = []
z.append('Abgleich der Einleitung im Master gegen Textvorschlag Überarbeitung § 5.1 (Task 11, Schritt 0)')
z.append('Master: %s, %d Byte, MD5 %s' % (os.path.basename(SRC), len(raw), hashlib.md5(raw).hexdigest()))
z.append('Maßstab: %s § 5.1, 6 Absätze, 930 Wörter' % os.path.basename(TV))
z.append('')
z.append('Absätze unter „1 Einleitung“ (Master-Index %d bis %d): %d mit Text, %d leer (Index %s)'
         % (start, ende - 1, len(ist), len(leer), ', '.join(str(x) for x in leer) or '—'))
befunde = []
if len(ist) != 6:
    befunde.append('Zahl der Absätze %d statt 6' % len(ist))

W = {}
for n, k in enumerate(FOLGE):
    if n >= len(ist):
        z.append('%s: fehlt im Master' % k)
        befunde.append('%s fehlt' % k)
        continue
    i, p = ist[n]
    t = p.text.strip()
    W[k] = t
    if t == SOLL[k]:
        urteil = 'wortgleich (exakt, Zeichen für Zeichen)'
    elif norm(t) == norm(SOLL[k]):
        urteil = 'wortgleich nach Normalisierung (Leerraum oder typografische Zeichen weichen ab)'
        diffs = [(a, b) for a, b in zip(t, SOLL[k]) if a != b][:5]
        urteil += ', erste Zeichenabweichungen: ' + ', '.join('%r statt %r' % (a, b) for a, b in diffs)
        befunde.append('%s nur nach Normalisierung gleich' % k)
    else:
        a, b = norm(SOLL[k]).split(), norm(t).split()
        ops = [o for o in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes() if o[0] != 'equal']
        det = '; '.join('%s Soll „%s“ Ist „%s“' % (o[0], ' '.join(a[o[1]:o[2]]), ' '.join(b[o[3]:o[4]])) for o in ops)
        urteil = 'ABWEICHUNG: ' + det.replace(';', ' |')
        befunde.append('%s weicht ab' % k)
    # Formatierung
    fmt = []
    stil = p.style.name
    if stil != 'Normal':
        fmt.append('Formatvorlage %s' % stil)
    ppr = p._p.pPr
    if ppr is not None:
        for tag in ['w:ind', 'w:jc', 'w:spacing', 'w:numPr', 'w:rPr']:
            if ppr.find(qn(tag)) is not None:
                fmt.append('Absatz ' + tag)
    runs = p._p.findall(qn('w:r'))
    rfmt = set()
    for r in runs:
        rpr = r.find(qn('w:rPr'))
        if rpr is None:
            continue
        for ch in rpr:
            rfmt.add(ch.tag.split('}')[1])
    if rfmt:
        fmt.append('Run-Eigenschaften: ' + ', '.join(sorted(rfmt)))
    kenn = [x for x in FOLGE if re.search(r'\b' + x + r'\b', t)]
    z.append('%s (Index %d, %d Runs): %s' % (k, i, len(runs), urteil))
    z.append('    Format: %s' % ('ohne Direktformatierung' if not fmt else ' · '.join(fmt)))
    if kenn:
        z.append('    Kennungen im Text: ' + ', '.join(kenn))
        befunde.append('%s mit Kennung im Text' % k)

# 3 Messung
z.append('')
z.append('%-6s %6s %6s %6s %7s %8s %6s %5s %5s %5s' % ('Absatz', 'Sätze', 'Wörter', 'Soll', 'o. Bel.', 'längster',
                                                     'Median', 'Bel.', 'Semi', 'Dopp'))
alle_s = []
summe = 0
for k in FOLGE:
    if k not in W:
        continue
    t = W[k]
    s = saetze(t)
    sl = [len(x.split()) for x in s]
    alle_s += sl
    wo = len(t.split())
    summe += wo
    ob = len(ohne_belege(t).split())
    z.append('%-6s %6d %6d %6d %7d %8d %6s %5d %5d %5d' % (k, len(s), wo, SOLL_W[k], ob, max(sl),
                                                        de(statistics.median(sl)), len(KLAMMER.findall(t)),
                                                        ohne_klammern(t).count(SEMI), ohne_klammern(t).count(':')))
ganz = ' '.join(W.values())
z.append('%-6s %6d %6d %6d %7d %8d %6s %5d %5d %5d' % ('Summe', len(alle_s), summe, 930,
                                                    sum(len(ohne_belege(x).split()) for x in W.values()), max(alle_s),
                                                    de(statistics.median(alle_s)), len(KLAMMER.findall(ganz)),
                                                    ohne_klammern(ganz).count(SEMI), ohne_klammern(ganz).count(':')))
z.append('Nummerierte Abschnittsverweise: %d · Sätze über 32 Wörter: %d · über 40: %d'
         % (len(RE_REF.findall(ganz)), sum(1 for x in alle_s if x > 32), sum(1 for x in alle_s if x > 40)))
z.append('Vergleich mit § 5.2 (schritt4_messung.py, gleiche Satzteilung): 40 Sätze, 930 Wörter, 778 ohne Belegklammern, '
         'längster Satz 32, Median 24,0, 26 Belegklammern, 0 Semikola, 0 Abschnittsverweise')

# 4 Übrige Teile der Übertragung (Rev. 134, Offen Nr. 1)
z.append('')
alt = []
akt = None
for i, p in enumerate(paras):
    if p.style.name.startswith('Heading'):
        tt = p.text.strip()
        mm = re.match(r'^(\d+(?:\.\d+)*)\s', tt)
        nr = mm.group(1) if mm else ''
        akt = nr if (nr == '2' or nr.startswith('2.') or nr == '3') else None
        if akt:
            alt.append([nr, tt, 0, 0])
        continue
    if akt and p.text.strip():
        alt[-1][2] += len(p.text.split())
        alt[-1][3] += 1
if alt:
    z.append('Altbestand noch im Master (M24 nicht ausgeführt): %d Überschriften, %d Absätze, %d Wörter'
             % (len(alt), sum(a[3] for a in alt), sum(a[2] for a in alt)))
    for a in alt:
        z.append('    %-6s %-70s %5d Wörter, %d Absätze' % (a[0], a[1][:70], a[2], a[3]))
    befunde.append('Altbestand Kapitel 2 und 3 noch im Master (M24)')
else:
    z.append('Altbestand Kapitel 2 und 3: gelöscht (M24 erledigt)')

z.append('')
z.append('Ergebnis: ' + ('ohne Befund' if not befunde else ' · '.join(befunde)))
with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(z) + '\n')
print('\n'.join(z))

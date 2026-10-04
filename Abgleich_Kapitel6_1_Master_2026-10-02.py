# -*- coding: utf-8 -*-
"""
Abgleich_Kapitel6_1_Master_2026-10-02.py — Task 12a: Abgleich des Masters nach dem Einbau von 6.1

Vergleicht den Manuskript-Master (neu gestagt nach der Rückschreibung) mit dem Referenzstand aus Master_6_1_2026-10-02.py
und mit dem Wortlaut aus Textvorschlag_6.1_2026-10-02.json. Nur lesend, der Master wird nicht verändert.

Prüfungen:
  1. keine word/comments.xml
  2. Absatzfolge (Formatvorlage und Text) außerhalb der Verzeichnisse und Felder gleich der Referenz,
     leere Absätze gesondert gezählt
  3. 6.1: zwischen „6.1 Einordnung der Ergebnisse“ und „6.2 Methodendiskussion“ genau die Absätze der JSON ohne Modul,
     zeichengleich (bei Abweichung Zeichenposition und Unicode-Code), Formatvorlage Standard (kein pStyle),
     keine Direktformatierung, Wortzahl je Absatz und Summe gegen die JSON und das Budget
  4. Überschriften 6 bis 7 vorhanden und in der Reihenfolge, 6.2 und 6.3 weiterhin leer (Task 12b)
  5. Sprachprüfungen am eingebauten Text: Semikolon nur in Zitierklammern, kein nummerierter Abschnittsverweis,
     kein Satz über 32 Wörter, kein Absatz über 250 Wörter
Aufruf: python3 Abgleich_Kapitel6_1_Master_2026-10-02.py <Master.docx> <Referenz.docx> <Textvorschlag_6.1.json> <Ausgabe.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import json
import zipfile
import hashlib
import difflib
import unicodedata
from xml.sax.saxutils import unescape

MASTER, REF, TV, AUS = sys.argv[1:5]
SEMI = chr(59)
L = []


def log(*t):
    L.append(' '.join(str(x) for x in t))


def lesen(p):
    z = zipfile.ZipFile(p)
    return z, z.read('word/document.xml').decode('utf-8')


def absaetze(xml):
    out = []
    for m in re.finditer(r'<w:p(?=[ >/])', xml):
        a = m.start()
        k = xml.find('>', a)
        if xml[k - 1] == '/':
            out.append({'stil': '', 'text': '', 'feld': False, 'xml': ''})
            continue
        e = xml.find('</w:p>', a) + len('</w:p>')
        inh = xml[a:e]
        st = re.search(r'<w:pStyle w:val="([^"]+)"', inh)
        txt = unescape(''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', inh)))
        feld = 'fldChar' in inh or 'instrText' in inh or '<w:fldSimple' in inh
        out.append({'stil': st.group(1) if st else '', 'text': txt, 'feld': feld, 'xml': inh})
    return out


def vergleichbar(p):
    return not p['feld'] and not p['stil'].startswith('Verzeichnis')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def saetze(text):
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', text)
    t = re.sub(r'\b(et al|Abschn|Tab|Abb|vgl|bzw|ca|Nr|Aufl|Hrsg|Jg)\.', r'\1<P>', t)
    t = re.sub(r'\b([A-Z])\.\s', r'\1<P> ', t)
    t = re.sub(r'\bS\.\s', 'S<P> ', t)
    t = re.sub(r'(\d)\.\s', r'\1<P> ', t)
    teile = [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(⟨])', t) if s.strip()]
    return [s.replace('<P>', '.') for s in teile]


RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')

zm, xm = lesen(MASTER)
zr, xr = lesen(REF)
tv = json.load(open(TV, encoding='utf-8'))
soll_abs = [a for a in tv['absaetze'] if not a.get('modul')]
soll = [a['text'] for a in soll_abs]
budget = tv.get('budget', 700)
log('Abgleich_Kapitel6_1_Master_2026-10-02.py')
log('Master:', MASTER, 'MD5', md5(MASTER))
log('Referenz:', REF, 'MD5', md5(REF))
log('Wortlaut:', TV, '%d Absätze ohne Modul, %d Modul-Einträge nicht erwartet' % (len(soll), len(tv['absaetze']) - len(soll)))
befunde = []

# 1 Kommentare
if 'word/comments.xml' in zm.namelist():
    befunde.append('comments.xml vorhanden')
log('1 comments.xml im Master:', 'ja' if 'word/comments.xml' in zm.namelist() else 'nein')

# 2 Absatzfolge
PM, PR = absaetze(xm), absaetze(xr)
vm = [p for p in PM if vergleichbar(p)]
vr = [p for p in PR if vergleichbar(p)]
log('2 Absätze gesamt: Master %d, Referenz %d · ohne Verzeichnisse und Felder: Master %d, Referenz %d'
    % (len(PM), len(PR), len(vm), len(vr)))
km = [(p['stil'], p['text']) for p in vm if p['text'].strip()]
kr = [(p['stil'], p['text']) for p in vr if p['text'].strip()]
leer_m = sum(1 for p in vm if not p['text'].strip())
leer_r = sum(1 for p in vr if not p['text'].strip())
log('  leere Absätze außerhalb der Verzeichnisse: Master %d, Referenz %d' % (leer_m, leer_r))
if leer_m != leer_r:
    befunde.append('Zahl der leeren Absätze weicht ab (Master %d, Referenz %d)' % (leer_m, leer_r))
zr_ = ['%s | %s' % k for k in kr]
zm_ = ['%s | %s' % k for k in km]
diff = [d for d in difflib.unified_diff(zr_, zm_, lineterm='', n=0) if not d.startswith(('---', '+++', '@@'))]
if diff:
    befunde.append('%d abweichende Zeilen in der Absatzfolge (Text oder Formatvorlage)' % len(diff))
    log('  Abweichungen der nicht leeren Absätze (- Referenz, + Master):')
    sm = difflib.SequenceMatcher(None, zr_, zm_, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        for xx, yy in zip(zr_[a1:a2], zm_[b1:b2]):
            i = next((j for j in range(min(len(xx), len(yy))) if xx[j] != yy[j]), min(len(xx), len(yy)))
            log('    geändert ab Zeichen %d: - %r' % (i, xx[max(0, i - 40):i + 40]))
            log('                          + %r' % yy[max(0, i - 40):i + 40])
        for xx in zr_[a1:a2][len(zm_[b1:b2]):]:
            log('    nur in der Referenz: %r' % xx[:160])
        for yy in zm_[b1:b2][len(zr_[a1:a2]):]:
            log('    nur im Master: %r' % yy[:160])
else:
    log('  nicht leere Absätze: %d, Formatvorlage und Text gleich der Referenz' % len(km))


# 3 Abschnitt 6.1
def finde(P, stil, text):
    t = [i for i, p in enumerate(P) if p['stil'] == stil and p['text'].strip() == text]
    return t[0] if len(t) == 1 else None


i61 = finde(PM, 'berschrift2', '6.1 Einordnung der Ergebnisse')
i62 = finde(PM, 'berschrift2', '6.2 Methodendiskussion')
eingebaut_text = ''
if i61 is None or i62 is None:
    befunde.append('Überschrift „6.1 Einordnung der Ergebnisse“ oder „6.2 Methodendiskussion“ nicht eindeutig gefunden')
    log('3 Abschnitt 6.1: Überschriften nicht eindeutig gefunden')
else:
    region = PM[i61 + 1:i62]
    voll = [p for p in region if p['text'].strip()]
    leer = [p for p in region if not p['text'].strip()]
    log('3 Abschnitt 6.1: %d nicht leere Absätze, %d leere zwischen den Überschriften' % (len(voll), len(leer)))
    if leer:
        befunde.append('6.1 enthält %d leere Absätze' % len(leer))
    if len(voll) != len(soll):
        befunde.append('6.1 hat %d statt %d Absätze' % (len(voll), len(soll)))
    woerter = 0
    for n, (p, a) in enumerate(zip(voll, soll_abs), 1):
        t, s = p['text'], a['text']
        w = len(t.split())
        woerter += w
        if t == s:
            zust = 'zeichengleich'
        else:
            zust = 'ABWEICHUNG'
            befunde.append('Absatz %s in 6.1 weicht vom Wortlaut ab' % a['kennung'])
            sm = difflib.SequenceMatcher(None, s, t)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != 'equal':
                    log('    %s %s Soll %r Ist %r (Codes %s → %s)' % (
                        a['kennung'], op, s[a1:a2], t[b1:b2],
                        ' '.join('U+%04X' % ord(c) for c in s[a1:a2]) or '–',
                        ' '.join('U+%04X' % ord(c) for c in t[b1:b2]) or '–'))
        if w != a['woerter']:
            befunde.append('Absatz %s: %d statt %d Wörter' % (a['kennung'], w, a['woerter']))
        stil = p['stil'] or 'Standard'
        if stil != 'Standard':
            befunde.append('Absatz %s in 6.1 mit Formatvorlage %s' % (a['kennung'], stil))
        ppr = re.search(r'<w:pPr>(.*?)</w:pPr>', p['xml'], re.S)
        ppr_kinder = sorted(set(re.findall(r'<w:([A-Za-z]+)', ppr.group(1)))) if ppr else []
        ppr_kinder = [k for k in ppr_kinder if k not in ('pStyle',)]
        rpr = re.findall(r'<w:r(?: [^>]*)?>\s*<w:rPr>(.*?)</w:rPr>', p['xml'], re.S)
        rpr_kinder = sorted(set(k for r in rpr for k in re.findall(r'<w:([A-Za-z]+)', r)))
        direkt = [k for k in ppr_kinder + rpr_kinder if k not in ('lang', 'noProof', 'rFonts')]
        if direkt:
            befunde.append('Absatz %s in 6.1 mit Direktformatierung %s' % (a['kennung'], ', '.join(direkt)))
        log('  %s: %s, %d Wörter (JSON %d), Formatvorlage %s, Absatzeigenschaften %s, Laufeigenschaften %s' % (
            a['kennung'], zust, w, a['woerter'], stil, ', '.join(ppr_kinder) or 'keine', ', '.join(rpr_kinder) or 'keine'))
        if unicodedata.normalize('NFC', t) != t:
            log('    %s enthält nicht normalisierte Zeichen (NFC weicht ab)' % a['kennung'])
    for p in voll[len(soll_abs):]:
        befunde.append('überzähliger Absatz in 6.1: %r' % p['text'][:80])
    log('  Wörter 6.1 im Master: %d (JSON %d, Budget %d)' % (woerter, sum(a['woerter'] for a in soll_abs), budget))
    if woerter != sum(a['woerter'] for a in soll_abs):
        befunde.append('6.1 hat %d statt %d Wörter' % (woerter, sum(a['woerter'] for a in soll_abs)))
    if woerter > budget:
        befunde.append('6.1 über dem Budget %d' % budget)
    eingebaut_text = ' '.join(p['text'] for p in voll)

# 4 Überschriften und leere Nachbarabschnitte
folge = [(st, tx) for st, tx in (('berschrift1', '6 Diskussion'), ('berschrift2', '6.1 Einordnung der Ergebnisse'),
                                 ('berschrift2', '6.2 Methodendiskussion'), ('berschrift2', '6.3 Stärken und Limitationen'),
                                 ('berschrift1', '7 Fazit und Ausblick'))]
idx = [finde(PM, st, tx) for st, tx in folge]
log('4 Überschriften 6 bis 7: Positionen %s' % idx)
if None in idx or idx != sorted(idx):
    befunde.append('Überschriften 6 bis 7 fehlen oder stehen in anderer Reihenfolge')
else:
    i_62, i_63, i_7 = idx[2], idx[3], idx[4]
    inhalt_62 = [p for p in PM[i_62 + 1:i_63] if p['text'].strip()]
    inhalt_63 = [p for p in PM[i_63 + 1:i_7] if p['text'].strip()]
    log('  6.2: %d nicht leere Absätze · 6.3: %d nicht leere Absätze (beide erwartet 0 bis Task 12b)' % (len(inhalt_62), len(inhalt_63)))
    if inhalt_62 or inhalt_63:
        log('  Hinweis: 6.2 oder 6.3 tragen Text, nicht Teil dieses Abgleichs')

# 5 Sprachprüfungen
if eingebaut_text:
    ohne_klammern = re.sub(r'\([^)]*\d{4}[^)]*\)', '', eingebaut_text)
    semi = ohne_klammern.count(SEMI)
    refs = len(RE_REF.findall(eingebaut_text))
    lang = [s for s in saetze(eingebaut_text) if len(s.split()) > 32]
    log('5 Sprachprüfungen: Semikola außerhalb von Zitierklammern %d · nummerierte Abschnittsverweise %d · Sätze über 32 Wörter %d'
        % (semi, refs, len(lang)))
    if semi:
        befunde.append('%d Semikola außerhalb von Zitierklammern' % semi)
    if refs:
        befunde.append('%d nummerierte Abschnittsverweise' % refs)
    for s in lang:
        befunde.append('Satz über 32 Wörter: „%s…“' % ' '.join(s.split()[:6]))
    if i61 is not None and i62 is not None:
        for p in PM[i61 + 1:i62]:
            if len(p['text'].split()) > 250:
                befunde.append('Absatz über 250 Wörter in 6.1')

log('')
log('Ergebnis: ' + ('ohne Befund' if not befunde else '%d Befunde' % len(befunde)))
for b in befunde:
    log('  - ' + b)
open(AUS, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))

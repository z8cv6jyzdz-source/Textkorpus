# -*- coding: utf-8 -*-
"""
textstand.py — Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“, Schritt 1 (03.10.2026)

Nur lesend. Prüft den Manuskript-Master für Kapitel 5 und hält den Textstand mit Satznummern fest:
  1. Größe, MD5, word/comments.xml, Zahl der Absätze
  2. Kapitel 5: zwischen „5 Ergebnisse“ und „6 Diskussion“ genau sechs nicht leere Absätze, zeichengleich mit
     03_Skripte\\Textvorschlag_5_2026-09-30.json (bei Abweichung Zeichenposition und Unicode-Code), Formatvorlage
     Standard (kein pStyle), keine Direktformatierung (Kinder von w:pPr außer pStyle, Kinder von w:rPr der Läufe),
     keine Felder, keine Textmarken im Kapitel
  3. Satzteilung wie Manuskriptstand_2026-09-25.py (Fassung 4, Funktion saetze unverändert übernommen), Wörter als
     Leerraum-Token, je Satz Wörter, Ende auf Ziffer oder Einzelbuchstaben, Semikola, nummerierte Abschnittsverweise,
     Belegklammern, Ziffernzahlen, Präsens-Verbformen der Objektsätze (nur Kennzeichnung)
  4. Gegenprobe der Satznummern gegen Textvorschlag 5 § 4 (Spalte „Anfang des Satzes“)
Schreibt textstand.json, textstand_saetze.md und textstand_pruefung.txt in den Ausgabeordner.
Aufruf: python textstand.py <Master.docx> <Textvorschlag_5_2026-09-30.json> <Textvorschlag_5_2026-09-30.md> [<Ausgabeordner>]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import os
import re
import json
import zipfile
import hashlib
import difflib
import statistics
from xml.sax.saxutils import unescape

MASTER, TVJ, TVMD = sys.argv[1:4]
AUS = sys.argv[4] if len(sys.argv) > 4 else os.path.dirname(os.path.abspath(__file__))
SEMI = chr(59)
RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')
L = []


def log(*t):
    L.append(' '.join(str(x) for x in t))


def saetze(text):
    """Satzteilung wie Manuskriptstand_2026-09-25.py Fassung 4 (unverändert seit Fassung 1)."""
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


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


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


def ende_ziffer_buchstabe(s):
    """True, wenn das Zeichen vor dem Schlusszeichen eine Ziffer ist oder der Satz auf einen einzelnen Buchstaben endet
    (etwa „g.“ oder „°C.“). Eine schließende Klammer davor zählt nicht als Ziffer (… (Tab. H2).)."""
    kern = s.rstrip()
    if not kern or kern[-1] not in '.!?':
        return False
    vor = kern[:-1]
    if re.search(r'\d$', vor):
        return True
    return bool(re.search(r'(?:^|[^A-Za-zÄÖÜäöüß])[A-Za-zÄÖÜäöü]$', vor))


def verschmolzen(s):
    """Hinweis auf zwei Sätze, die die Satzteilung zusammengezogen hat: Ziffer oder Einzelbuchstabe, Punkt, Leerraum
    und ein Satzanfang im Inneren (Abkürzungen Tab., Abb., S., et al. ausgenommen)."""
    t = re.sub(r'\b(?:Tab|Abb|S|al|Nr|vgl|bzw|ca)\.\s', 'X ', s)
    return bool(re.search(r'(?:\d|(?:^|[^A-Za-zÄÖÜäöüß])[A-Za-zÄÖÜäöü])\.\s+[A-ZÄÖÜ„(]', t))


z = zipfile.ZipFile(MASTER)
xml = z.read('word/document.xml').decode('utf-8')
tv = json.load(open(TVJ, encoding='utf-8'))
soll = tv['absaetze']
befunde = []
log('textstand.py — Schritt 1 (Textstand Kapitel 5)')
log('Master:', MASTER)
log('  Größe %d Byte, MD5 %s' % (os.path.getsize(MASTER), md5(MASTER)))
log('Wortlaut:', TVJ, 'MD5', md5(TVJ), '· %d Absätze' % len(soll))
log('Textvorschlag:', TVMD, 'MD5', md5(TVMD))
log('')

# 1 Kommentare, Absätze
kom = 'word/comments.xml' in z.namelist()
log('1 word/comments.xml im Master:', 'ja' if kom else 'nein')
if kom:
    befunde.append('comments.xml vorhanden')
P = absaetze(xml)
log('  Absätze im Dokument: %d' % len(P))


def finde(stil, text):
    t = [i for i, p in enumerate(P) if p['stil'] == stil and p['text'].strip() == text]
    return t[0] if len(t) == 1 else None


i5, i6 = finde('berschrift1', '5 Ergebnisse'), finde('berschrift1', '6 Diskussion')
log('  „5 Ergebnisse“ an Position %s, „6 Diskussion“ an Position %s' % (i5, i6))
ergebnis = {'master': {'pfad': MASTER, 'bytes': os.path.getsize(MASTER), 'md5': md5(MASTER),
                       'comments_xml': kom, 'absaetze_dokument': len(P), 'pos_5': i5, 'pos_6': i6},
            'absaetze': []}

# 2 Kapitel 5 gegen JSON
if i5 is None or i6 is None:
    befunde.append('Überschriften nicht eindeutig gefunden')
else:
    region = P[i5 + 1:i6]
    voll = [p for p in region if p['text'].strip()]
    leer = [p for p in region if not p['text'].strip()]
    log('')
    log('2 Kapitel 5: %d nicht leere, %d leere Absätze zwischen den Überschriften' % (len(voll), len(leer)))
    if leer:
        befunde.append('Kapitel 5 enthält leere Absätze')
    if len(voll) != len(soll):
        befunde.append('Kapitel 5 hat %d statt %d Absätze' % (len(voll), len(soll)))
    for p, a in zip(voll, soll):
        t, s = p['text'], a['text']
        if t == s:
            zust = 'zeichengleich'
        else:
            zust = 'ABWEICHUNG'
            befunde.append('Absatz %s weicht vom JSON ab' % a['kennung'])
            sm = difflib.SequenceMatcher(None, s, t, autojunk=False)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != 'equal':
                    log('    %s %s ab Zeichen %d: JSON %r Master %r (Codes %s → %s)' % (
                        a['kennung'], op, a1, s[a1:a2], t[b1:b2],
                        ' '.join('U+%04X' % ord(c) for c in s[a1:a2]) or '–',
                        ' '.join('U+%04X' % ord(c) for c in t[b1:b2]) or '–'))
        stil = p['stil'] or 'Standard'
        ppr = re.search(r'<w:pPr>(.*?)</w:pPr>', p['xml'], re.S)
        ppr_k = sorted(set(re.findall(r'<w:([A-Za-z]+)', ppr.group(1)))) if ppr else []
        ppr_k = [k for k in ppr_k if k != 'pStyle']
        rpr = re.findall(r'<w:r(?: [^>]*)?>\s*<w:rPr>(.*?)</w:rPr>', p['xml'], re.S)
        rpr_k = sorted(set(k for r in rpr for k in re.findall(r'<w:([A-Za-z]+)', r)))
        direkt = [k for k in ppr_k + rpr_k if k not in ('lang', 'noProof')]
        marken = len(re.findall(r'<w:bookmarkStart', p['xml']))
        if stil != 'Standard':
            befunde.append('%s mit Formatvorlage %s' % (a['kennung'], stil))
        if direkt:
            befunde.append('%s mit Direktformatierung %s' % (a['kennung'], ', '.join(direkt)))
        if p['feld']:
            befunde.append('%s enthält ein Feld' % a['kennung'])
        log('  %s: %s, Formatvorlage %s, Absatzeigenschaften %s, Laufeigenschaften %s, Felder %s, Textmarken %d' % (
            a['kennung'], zust, stil, ', '.join(ppr_k) or 'keine', ', '.join(rpr_k) or 'keine',
            'ja' if p['feld'] else 'nein', marken))
    for p in voll[len(soll):]:
        befunde.append('überzähliger Absatz: %r' % p['text'][:80])

    # 3 Satzteilung und Messung
    log('')
    log('3 Messung (Satzteilung und Wortzählung wie Manuskriptstand_2026-09-25.py Fassung 4)')
    alle_s = []
    for p, a in zip(voll, soll):
        t = p['text']
        ss = saetze(t)
        sl = []
        for n, s in enumerate(ss, 1):
            w = len(s.split())
            ohne = re.sub(r'\([^)]*\d{4}[^)]*\)', '', s)
            sd = {'id': '%s S%d' % (a['kennung'], n), 'absatz': a['kennung'], 'nr': n, 'text': s, 'woerter': w,
                  'ende_ziffer_oder_buchstabe': ende_ziffer_buchstabe(s), 'verschmolzen': verschmolzen(s),
                  'semikola': ohne.count(SEMI), 'abschnittsverweise': len(RE_REF.findall(s)),
                  'belegklammern': len(re.findall(r'\([^)]*\d{4}[^)]*\)', s)),
                  'ziffernzahlen': len(re.findall(r'[−+-]?\d+(?:,\d+)?', s)),
                  'objekte': re.findall(r'(?:Tab|Abb)\.\s[A-H]?\d+[a-z]?', s)}
            sl.append(sd)
            alle_s.append(sd)
        w_abs = len(t.split())
        ergebnis['absaetze'].append({'kennung': a['kennung'], 'gruppe': a.get('gruppe', ''), 'text': t,
                                     'woerter': w_abs, 'saetze': sl, 'zeichengleich_json': t == a['text']})
        log('  %s: %d Wörter, %d Sätze, längster %d' % (a['kennung'], w_abs, len(sl), max(x['woerter'] for x in sl)))
    lw = [x['woerter'] for x in alle_s]
    ids0 = {x['id']: x['text'] for x in alle_s}
    gesamt = sum(x['woerter'] for x in ergebnis['absaetze'])
    ergebnis['messung'] = {'woerter': gesamt, 'budget': 450, 'absaetze': len(ergebnis['absaetze']),
                           'saetze': len(alle_s), 'median_satzlaenge': statistics.median(lw), 'laengster_satz': max(lw),
                           'kuerzester_satz': min(lw), 'saetze_ueber_32': sum(1 for x in lw if x > 32),
                           'absaetze_ueber_250': sum(1 for x in ergebnis['absaetze'] if x['woerter'] > 250),
                           'semikola': sum(x['semikola'] for x in alle_s),
                           'abschnittsverweise': sum(x['abschnittsverweise'] for x in alle_s),
                           'belegklammern': sum(x['belegklammern'] for x in alle_s),
                           'ende_ziffer_oder_buchstabe': [x['id'] for x in alle_s if x['ende_ziffer_oder_buchstabe']],
                           'verschmolzen': [x['id'] for x in alle_s if x['verschmolzen']],
                           'ziffernzahlen': sum(x['ziffernzahlen'] for x in alle_s)}
    m = ergebnis['messung']
    log('  Kapitel 5: %d Wörter (Budget 450), %d Absätze, %d Sätze, Median %.1f, längster %d, kürzester %d' % (
        m['woerter'], m['absaetze'], m['saetze'], m['median_satzlaenge'], m['laengster_satz'], m['kuerzester_satz']))
    log('  Sätze über 32: %d · Absätze über 250: %d · Semikola %d · Abschnittsverweise %d · Belegklammern %d' % (
        m['saetze_ueber_32'], m['absaetze_ueber_250'], m['semikola'], m['abschnittsverweise'], m['belegklammern']))
    log('  Satzende auf Ziffer oder Einzelbuchstaben (Zeichen vor dem Schlusspunkt): %s' % (
        ', '.join('%s „…%s“' % (i, ids0[i][-12:]) for i in m['ende_ziffer_oder_buchstabe']) or 'keines'))
    log('  Hinweis auf zusammengezogene Sätze (Satzteilung): %s' % (', '.join(m['verschmolzen']) or 'keiner'))
    log('  Ziffernzahlen (Regex, ohne Zahlwörter): %d' % m['ziffernzahlen'])
    if m['woerter'] != 450:
        befunde.append('Kapitel 5 hat %d statt 450 Wörter' % m['woerter'])
    for k in ('saetze_ueber_32', 'absaetze_ueber_250', 'semikola', 'abschnittsverweise', 'belegklammern'):
        if m[k]:
            befunde.append('%s: %d' % (k, m[k]))
    if m['ende_ziffer_oder_buchstabe']:
        befunde.append('Satzende auf Ziffer oder Einzelbuchstaben: %s' % ', '.join(m['ende_ziffer_oder_buchstabe']))
    if m['verschmolzen']:
        befunde.append('Satzteilung zieht Sätze zusammen: %s' % ', '.join(m['verschmolzen']))

    # 4 Gegenprobe der Satznummern gegen Textvorschlag 5 § 4
    md = open(TVMD, encoding='utf-8').read()
    teil4 = md.split('## 4 Rasterzuordnung')[1].split('## 5 ')[0]
    anf = re.findall(r'^\| (A\d S\d+) \| (.+?) … \|', teil4, re.M)
    log('')
    log('4 Gegenprobe Satznummern gegen Textvorschlag 5 § 4: %d Einträge' % len(anf))
    ids = {x['id']: x['text'] for x in alle_s}
    abw = 0
    for sid, a in anf:
        ok = sid in ids and ids[sid].startswith(a.strip())
        if not ok:
            abw += 1
            befunde.append('Satznummer %s passt nicht zu § 4 (%r)' % (sid, a))
    log('  übereinstimmend %d von %d, Sätze im Master %d' % (len(anf) - abw, len(anf), len(alle_s)))
    if len(anf) != len(alle_s):
        befunde.append('Zahl der Sätze weicht von § 4 ab (%d gegen %d)' % (len(alle_s), len(anf)))

log('')
log('Ergebnis: ' + ('ohne Befund' if not befunde else '%d Befunde' % len(befunde)))
for b in befunde:
    log('  - ' + b)
ergebnis['befunde'] = befunde
json.dump(ergebnis, open(os.path.join(AUS, 'textstand.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(AUS, 'textstand_pruefung.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')

# Satzliste
Z = ['# Kapitel 5 im Master — Textstand mit Satznummern (Schritt 1, 03.10.2026)', '',
     'Master %d Byte, MD5 `%s`. Satzteilung und Wörter wie `Manuskriptstand_2026-09-25.py` (Fassung 4). '
     'In Klammern die Wortzahl des Satzes.' % (os.path.getsize(MASTER), md5(MASTER)), '']
for a in ergebnis['absaetze']:
    Z.append('## %s (Absatzgruppe %s, %d Wörter, %d Sätze)' % (a['kennung'], a['gruppe'], a['woerter'], len(a['saetze'])))
    Z.append('')
    for s in a['saetze']:
        Z.append('%s (%d): %s' % (s['id'], s['woerter'], s['text']))
    Z.append('')
open(os.path.join(AUS, 'textstand_saetze.md'), 'w', encoding='utf-8').write('\n'.join(Z))
print('\n'.join(L))

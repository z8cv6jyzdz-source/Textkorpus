# -*- coding: utf-8 -*-
"""
Abgleich_Kapitel5_Master_2026-10-01.py — Task 11: Abgleich nach der Übertragung von Kapitel 5 durch den Verfasser

Vergleicht den Manuskript-Master nach der Übertragung (Kapitel 5 eingefügt, Überschriften 5.1 und 5.2 und Altbestand
Kapitel 2 und 3 gelöscht, F9) mit dem per Skript eingebauten Referenzstand (Master_5_2026-09-30.py mit --altbestand
auf der Archivkopie vom 30.09., MD5 53cc8f36…) und mit dem Wortlaut aus Textvorschlag_5_2026-09-30.json.
Nur lesend, der Master wird nicht verändert.

Prüfungen:
  1. keine word/comments.xml
  2. Absatzfolge (Formatvorlage und Text) außerhalb der Verzeichnisse und Felder gleich der Referenz.
     Absätze mit Feldern (Inhaltsverzeichnis, Abbildungs- und Tabellenverzeichnis) und Formatvorlagen „Verzeichnis…“
     werden nicht verglichen, weil F9 sie neu erzeugt. Leere Absätze werden gesondert gezählt.
  3. Kapitel 5: zwischen „5 Ergebnisse“ und „6 Diskussion“ genau sechs nicht leere Absätze, zeichengleich mit der JSON,
     bei Abweichung mit Zeichenposition und Unicode-Code, Formatvorlage Standard (kein pStyle), Direktformatierung je Absatz
     (Kinder von w:pPr außer pStyle, Kinder von w:rPr der Läufe), Wortzahl als Leerraum-Token
  4. keine Überschriften 5.1, 5.2 und keine Überschrift des Altbestands mehr im Master
Aufruf: python3 Abgleich_Kapitel5_Master_2026-10-01.py <Master.docx> <Referenz.docx> <Textvorschlag.json> <Ausgabe.txt>
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


zm, xm = lesen(MASTER)
zr, xr = lesen(REF)
tv = json.load(open(TV, encoding='utf-8'))
log('Abgleich_Kapitel5_Master_2026-10-01.py')
log('Master:', MASTER, 'MD5', md5(MASTER))
log('Referenz:', REF, 'MD5', md5(REF))
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
log('  Verzeichnis- und Feldabsätze (nicht verglichen, F9): Master %d, Referenz %d'
    % (len(PM) - len(vm), len(PR) - len(vr)))
km = [(p['stil'], p['text']) for p in vm if p['text'].strip()]
kr = [(p['stil'], p['text']) for p in vr if p['text'].strip()]
leer_m = sum(1 for p in vm if not p['text'].strip())
leer_r = sum(1 for p in vr if not p['text'].strip())
log('  leere Absätze außerhalb der Verzeichnisse: Master %d, Referenz %d' % (leer_m, leer_r))
if leer_m != leer_r:
    befunde.append('Zahl der leeren Absätze weicht ab (Master %d, Referenz %d)' % (leer_m, leer_r))
diff = [d for d in difflib.unified_diff(['%s | %s' % k for k in kr], ['%s | %s' % k for k in km], lineterm='', n=0)
        if not d.startswith(('---', '+++', '@@'))]
if diff:
    befunde.append('%d abweichende Zeilen in der Absatzfolge (Text oder Formatvorlage)' % len(diff))
    log('  Abweichungen der nicht leeren Absätze (- Referenz, + Master), Ausschnitt um die erste abweichende Stelle:')
    sm = difflib.SequenceMatcher(None, ['%s | %s' % k for k in kr], ['%s | %s' % k for k in km], autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        alt_z = ['%s | %s' % k for k in kr[a1:a2]]
        neu_z = ['%s | %s' % k for k in km[b1:b2]]
        for x, y in zip(alt_z, neu_z):
            i = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
            log('    geändert ab Zeichen %d: - %r' % (i, x[max(0, i - 40):i + 40]))
            log('                          + %r' % y[max(0, i - 40):i + 40])
        for x in alt_z[len(neu_z):]:
            log('    nur in der Referenz: %r' % x[:160])
        for y in neu_z[len(alt_z):]:
            log('    nur im Master: %r' % y[:160])
else:
    log('  nicht leere Absätze: %d, Formatvorlage und Text gleich der Referenz' % len(km))

# 3 Kapitel 5
def finde(P, stil, text):
    t = [i for i, p in enumerate(P) if p['stil'] == stil and p['text'].strip() == text]
    return t[0] if len(t) == 1 else None


i5, i6 = finde(PM, 'berschrift1', '5 Ergebnisse'), finde(PM, 'berschrift1', '6 Diskussion')
if i5 is None or i6 is None:
    befunde.append('Überschrift „5 Ergebnisse“ oder „6 Diskussion“ nicht eindeutig gefunden')
    log('3 Kapitel 5: Überschriften nicht eindeutig gefunden')
else:
    region = PM[i5 + 1:i6]
    voll = [p for p in region if p['text'].strip()]
    leer = [p for p in region if not p['text'].strip()]
    soll = [a['text'] for a in tv['absaetze']]
    log('3 Kapitel 5: %d nicht leere Absätze, %d leere zwischen den Überschriften' % (len(voll), len(leer)))
    if leer:
        befunde.append('Kapitel 5 enthält %d leere Absätze' % len(leer))
    if len(voll) != len(soll):
        befunde.append('Kapitel 5 hat %d statt %d Absätze' % (len(voll), len(soll)))
    woerter = 0
    for n, (p, s) in enumerate(zip(voll, soll), 1):
        t = p['text']
        woerter += len(t.split())
        if t == s:
            zust = 'zeichengleich'
        else:
            zust = 'ABWEICHUNG'
            befunde.append('Absatz %d in Kapitel 5 weicht vom Wortlaut ab' % n)
            sm = difflib.SequenceMatcher(None, s, t)
            for op, a1, a2, b1, b2 in sm.get_opcodes():
                if op != 'equal':
                    log('    A%d %s Soll %r Ist %r (Codes %s → %s)' % (
                        n, op, s[a1:a2], t[b1:b2],
                        ' '.join('U+%04X' % ord(c) for c in s[a1:a2]) or '–',
                        ' '.join('U+%04X' % ord(c) for c in t[b1:b2]) or '–'))
        stil = p['stil'] or 'Standard'
        if stil != 'Standard':
            befunde.append('Absatz %d in Kapitel 5 mit Formatvorlage %s' % (n, stil))
        ppr = re.search(r'<w:pPr>(.*?)</w:pPr>', p['xml'], re.S)
        ppr_kinder = sorted(set(re.findall(r'<w:([A-Za-z]+)', ppr.group(1)))) if ppr else []
        ppr_kinder = [k for k in ppr_kinder if k not in ('pStyle',)]
        rpr = re.findall(r'<w:r(?: [^>]*)?>\s*<w:rPr>(.*?)</w:rPr>', p['xml'], re.S)
        rpr_kinder = sorted(set(k for r in rpr for k in re.findall(r'<w:([A-Za-z]+)', r)))
        direkt = [k for k in ppr_kinder + rpr_kinder if k not in ('lang', 'noProof', 'rFonts')]
        if direkt:
            befunde.append('Absatz %d in Kapitel 5 mit Direktformatierung %s' % (n, ', '.join(direkt)))
        log('  A%d: %s, %d Wörter, Formatvorlage %s, Absatzeigenschaften %s, Laufeigenschaften %s' % (
            n, zust, len(t.split()), stil, ', '.join(ppr_kinder) or 'keine', ', '.join(rpr_kinder) or 'keine'))
        nfc = unicodedata.normalize('NFC', t)
        if nfc != t:
            log('    A%d enthält nicht normalisierte Zeichen (NFC weicht ab)' % n)
    log('  Wörter Kapitel 5 im Master: %d (Textvorschlag 450)' % woerter)
    if woerter != 450:
        befunde.append('Kapitel 5 hat %d statt 450 Wörter' % woerter)

# 4 entfernte Überschriften
weg = ['5.1 Teilnehmerfluss, Adhärenz und Ausgangswerte', '5.2 Gruppenvergleiche je Zielgröße',
       '2 Theoretischer Hintergrund und Forschungsstand', '2.1 Plyometrisches Training – Grundlagen',
       '2.2 Biologische Reifung und Trainierbarkeit im Nachwuchs', '2.3 Übergangsperiode und Detraining im Fußball',
       '2.4 Zielgrößen und ihre Diagnostik', '2.4.1 Lineare Sprintschnelligkeit (5/10/30 m)',
       '2.4.2 Richtungswechselfähigkeit (505)', '2.4.3 Sprungkraft (Standweitsprung)',
       '2.5 Forschungsstand: Effekte plyometrischen Trainings auf Sprint, Richtungswechsel und Sprung',
       '3 Fragestellung und Hypothesen']
noch = [p['text'].strip() for p in PM if p['stil'].startswith('berschrift') and p['text'].strip() in weg]
log('4 entfernte Überschriften noch im Master: %d' % len(noch))
for t in noch:
    befunde.append('Überschrift noch vorhanden: ' + t)
toc = [p['text'] for p in PM if p['stil'].startswith('Verzeichnis')]
alt_im_toc = [t for t in toc if any(t.startswith(w) for w in weg)]
log('  Inhaltsverzeichnis: %d Einträge, davon %d mit entfernten Überschriften (F9 %s)' % (
    len(toc), len(alt_im_toc), 'noch nicht ausgeführt' if alt_im_toc else 'ausgeführt oder Einträge aktuell'))
if alt_im_toc:
    befunde.append('Inhaltsverzeichnis führt noch %d entfernte Überschriften (F9 fehlt)' % len(alt_im_toc))

log('')
log('Ergebnis: ' + ('ohne Befund' if not befunde else '%d Befunde' % len(befunde)))
for b in befunde:
    log('  - ' + b)
open(AUS, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))

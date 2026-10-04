# -*- coding: utf-8 -*-
"""
Messen_Text_2026-09-25.py — Kennwerte eines Textvorschlags messen (Skill kapiteltext-bachelorarbeit, Schritt 6 Nr. 4)
Wörter je Absatz (Leerzeichen-Token), Sätze, Median und Maximum der Satzlänge, Absatzmaximum,
Semikola (gesamt und außerhalb von Klammern), nummerierte Abschnittsverweise, Kennungen [K-…],
Verbotsliste, Klammerbelege, Objekt- und Anhangsverweise. Ohne Semikolon im Skript (chr(59)).
Aufruf: python Messen_Text_2026-09-25.py <Textdatei.txt>   (Absätze durch Leerzeilen getrennt, Zeilen mit # werden ignoriert)
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re
import statistics

SEMI = chr(59)
txt = open(sys.argv[1], encoding='utf-8').read()
txt = '\n'.join(z for z in txt.split('\n') if not z.startswith('#'))
absaetze = [a.strip() for a in re.split(r'\n\s*\n', txt) if a.strip()]
ABK = ['S.', 'et al.', 'Abs.', 'Nr.', 'Tab.', 'Abb.', 'vgl.', 'bzw.', 'z. B.', 'u. a.', 'ca.', 'Hrsg.', 'Aufl.', 'Std.', 'min.', 'ggf.', 'Abschn.']


def saetze(a):
    s = a
    for i, ab in enumerate(ABK):
        s = s.replace(ab, ab.replace('.', '․'))
    s = re.sub(r'(\d)\.(\d)', r'\1․\2', s)
    s = re.sub(r'(\d{2})\.(\d{4})', r'\1․\2', s)
    s = re.sub(r'(\d{2})\.\s', r'\1․ ', s)
    teile = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(0-9])', s)
    return [t.replace('․', '.') for t in teile if t.strip()]


gesamt = 0
alle_saetze = []
print('Absatz | Wörter | Sätze | längster Satz')
for i, a in enumerate(absaetze, 1):
    w = len(a.split())
    ss = saetze(a)
    alle_saetze.extend(ss)
    gesamt += w
    print('%d | %d | %d | %d' % (i, w, len(ss), max(len(x.split()) for x in ss)))
laengen = [len(x.split()) for x in alle_saetze]
print('Wörter gesamt: %d' % gesamt)
print('Sätze: %d · Median %.1f · Mittel %.1f · längster %d · über 32: %d · über 40: %d' % (
    len(laengen), statistics.median(laengen), sum(laengen) / len(laengen), max(laengen),
    sum(1 for l in laengen if l > 32), sum(1 for l in laengen if l > 40)))
print('längster Absatz: %d Wörter' % max(len(a.split()) for a in absaetze))
ohne_klammern = re.sub(r'\([^)]*\)', '', txt)
print('Semikola gesamt: %d · außerhalb von Klammern: %d' % (txt.count(SEMI), ohne_klammern.count(SEMI)))
verweise = re.findall(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)', txt)
print('Abschnittsverweise: %d %r' % (len(verweise), verweise))
print('Kennungen im Text: %d' % len(re.findall(r'\[K-', txt)))
verboten = ['im Rahmen', 'Gegenstand der Untersuchung', 'es ist festzuhalten', 'darüber hinaus', 'des Weiteren', 'hierbei gilt', 'zunächst', 'anschließend', 'abschließend', 'sodass', 'weshalb', 'Interessanterweise', 'in diesem Zusammenhang', 'unsere ']
treffer = [v for v in verboten if v.lower() in txt.lower()]
print('Verbotsliste: %d %r' % (len(treffer), treffer))
belege = re.findall(r'\((?:[A-ZÄÖÜ][^()]*?\d{4}[^()]*)\)', txt)
print('Klammerbelege: %d' % len(belege))
for b in belege:
    print('   ', b)
print('Objektverweise: %r' % re.findall(r'(?:Tab|Abb)\.\s*H?\d+', txt))
print('Anhangsverweise: %r' % re.findall(r'Anhang [A-H]', txt))
for s in alle_saetze:
    if len(s.split()) > 32:
        print('LANG (%d): %s' % (len(s.split()), s))

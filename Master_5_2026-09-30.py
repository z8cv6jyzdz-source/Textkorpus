# -*- coding: utf-8 -*-
"""
Master_5_2026-09-30.py — Task 11: Einbau von Kapitel 5 (Ergebnisse) in den Manuskript-Master, nur Text

Setzt die Absätze aus Textvorschlag_5_2026-09-30.json unter die Überschrift „5 Ergebnisse“ und entfernt die
Überschriften „5.1 Teilnehmerfluss, Adhärenz und Ausgangswerte“ und „5.2 Gruppenvergleiche je Zielgröße“
(Gliederung v6, Ä16 und M28, E3 am Textvorschlag geprüft). Keine Objekte, keine Platzhalter (F17 § 5.3).
Optional (Schalter --altbestand, nur nach Klick des Verfassers): entfernt den Altbestand nach M24, die Überschriften
„2 Theoretischer Hintergrund und Forschungsstand“ bis einschließlich „3 Fragestellung und Hypothesen“ samt Text,
bis vor „4 Methodik“. Jede Operation greift genau einmal oder bricht ab. Absätze ohne Direktformatierung
(Formatvorlage Standard), Text XML-maskiert. Verzeichnisse aktualisiert der Verfasser mit F9.
Aufruf: python Master_5_2026-09-30.py <Master_ein.docx> <Textvorschlag.json> <Master_aus.docx> [--altbestand]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import json
import zipfile
import shutil
import os
from xml.sax.saxutils import escape

SRC, TV, DST = sys.argv[1], sys.argv[2], sys.argv[3]
ALT = '--altbestand' in sys.argv[4:]
AMP = chr(38)

zin = zipfile.ZipFile(SRC)
x = zin.read('word/document.xml').decode('utf-8')
assert 'word/comments.xml' not in zin.namelist(), 'comments.xml vorhanden: Kommentare beim Rebuild erhalten (Skill Schritt 8)'


def absaetze(xml):
    """Absätze des Body mit Start, Ende, Formatvorlage, Text. Selbstschließende <w:p …/> werden erkannt."""
    out = []
    for m in re.finditer(r'<w:p(?=[ >/])', xml):
        a = m.start()
        kopf_ende = xml.find('>', a)
        if xml[kopf_ende - 1] == '/':
            e = kopf_ende + 1
            inhalt = ''
        else:
            e = xml.find('</w:p>', a) + len('</w:p>')
            inhalt = xml[a:e]
            # verschachtelte Absätze (Textfelder, Tabellenzellen) wären hier ein Abbruchgrund
            assert inhalt.count('<w:p ') + inhalt.count('<w:p>') == 1, 'verschachtelter Absatz bei %d' % a
        st = re.search(r'<w:pStyle w:val="([^"]+)"', inhalt)
        txt = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', inhalt))
        out.append({'a': a, 'e': e, 'stil': st.group(1) if st else '', 'text': txt})
    return out


def einmal(liste, bedingung, name):
    treffer = [p for p in liste if bedingung(p)]
    assert len(treffer) == 1, '%s: %d Treffer statt 1' % (name, len(treffer))
    return treffer[0]


def ueberschrift(stil, text):
    return lambda p: p['stil'] == stil and p['text'].strip() == text


P = absaetze(x)
n_vorher = len(P)
h5 = einmal(P, ueberschrift('berschrift1', '5 Ergebnisse'), 'Überschrift 5')
h51 = einmal(P, ueberschrift('berschrift2', '5.1 Teilnehmerfluss, Adhärenz und Ausgangswerte'), 'Überschrift 5.1')
h52 = einmal(P, ueberschrift('berschrift2', '5.2 Gruppenvergleiche je Zielgröße'), 'Überschrift 5.2')
h6 = einmal(P, ueberschrift('berschrift1', '6 Diskussion'), 'Überschrift 6')
i5, i51, i52, i6 = [P.index(h) for h in (h5, h51, h52, h6)]
assert i51 == i5 + 1 and i52 == i51 + 1 and i6 == i52 + 1, 'Kapitel 5 ist nicht leer oder anders gegliedert: %d %d %d %d' % (i5, i51, i52, i6)

tv = json.load(open(TV, encoding='utf-8'))
neu = ''.join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(a['text']) for a in tv['absaetze'])
assert len(tv['absaetze']) == 6

protokoll = []
# Ersetzung von hinten nach vorn, damit die Positionen davor gültig bleiben
stueck5 = x[h51['a']:h52['e']]
assert '<w:sectPr' not in stueck5 and '<w:tbl' not in stueck5 and 'fldChar' not in stueck5, 'Abschnittswechsel, Tabelle oder Feld in 5.1/5.2'
s5 = set(re.findall(r'<w:bookmarkStart w:id="(\d+)"', stueck5))
e5 = set(re.findall(r'<w:bookmarkEnd w:id="(\d+)"', stueck5))
assert s5 == e5, 'Textmarken ragen aus den Überschriften 5.1/5.2 heraus: %s' % (s5 ^ e5)
x2 = x[:h51['a']] + neu + x[h52['e']:]
protokoll.append('Kapitel 5: Überschriften 5.1 und 5.2 entfernt (mit %d Verzeichnis-Textmarken, F9 aktualisiert das Inhaltsverzeichnis), '
                 '%d Absätze unter „5 Ergebnisse“ eingefügt' % (len(s5), len(tv['absaetze'])))

if ALT:
    P2 = absaetze(x2)
    h2 = einmal(P2, ueberschrift('berschrift1', '2 Theoretischer Hintergrund und Forschungsstand'), 'Überschrift 2')
    h3 = einmal(P2, ueberschrift('berschrift1', '3 Fragestellung und Hypothesen'), 'Überschrift 3')
    h4 = einmal(P2, ueberschrift('berschrift1', '4 Methodik'), 'Überschrift 4')
    i2, i3, i4 = P2.index(h2), P2.index(h3), P2.index(h4)
    assert i2 < i3 < i4 and i4 == i3 + 1, 'Altbestand anders als erwartet'
    region = P2[i2:i4]
    kopf = [p['text'].strip() for p in region if p['stil'].startswith('berschrift')]
    erwartet = ['2 Theoretischer Hintergrund und Forschungsstand', '2.1 Plyometrisches Training – Grundlagen',
                '2.2 Biologische Reifung und Trainierbarkeit im Nachwuchs', '2.3 Übergangsperiode und Detraining im Fußball',
                '2.4 Zielgrößen und ihre Diagnostik', '2.4.1 Lineare Sprintschnelligkeit (5/10/30 m)',
                '2.4.2 Richtungswechselfähigkeit (505)', '2.4.3 Sprungkraft (Standweitsprung)',
                '2.5 Forschungsstand: Effekte plyometrischen Trainings auf Sprint, Richtungswechsel und Sprung',
                '3 Fragestellung und Hypothesen']
    assert kopf == erwartet, 'Überschriften des Altbestands: %s' % kopf
    textabs = [p for p in region if not p['stil'].startswith('berschrift') and p['text'].strip()]
    woerter = sum(len(p['text'].split()) for p in textabs)
    assert len(textabs) == 25 and woerter == 4920, 'Altbestand: %d Absätze, %d Wörter' % (len(textabs), woerter)
    stueck = x2[region[0]['a']:region[-1]['e']]
    assert '<w:sectPr' not in stueck and '<w:tbl' not in stueck and 'fldChar' not in stueck, 'Abschnittswechsel, Tabelle oder Feld im Altbestand'
    starts = set(re.findall(r'<w:bookmarkStart w:id="(\d+)"', stueck))
    ends = set(re.findall(r'<w:bookmarkEnd w:id="(\d+)"', stueck))
    assert starts == ends, 'Textmarken ragen aus dem Altbestand heraus: %s' % (starts ^ ends)
    x2 = x2[:region[0]['a']] + x2[region[-1]['e']:]
    protokoll.append('Altbestand (M24): %d Überschriften, %d Textabsätze mit %d Wörtern entfernt, %d Textmarken mit ihnen'
                     % (len(kopf), len(textabs), woerter, len(starts)))

n_nachher = len(absaetze(x2))
protokoll.append('Absätze im Dokument: vorher %d, nachher %d' % (n_vorher, n_nachher))

tmp = DST + '.tmp'
with zipfile.ZipFile(SRC) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        daten = zi.read(it.filename)
        if it.filename == 'word/document.xml':
            daten = x2.encode('utf-8')
        zo.writestr(it, daten)
shutil.move(tmp, DST)
print('\n'.join(protokoll))

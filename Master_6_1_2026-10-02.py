# -*- coding: utf-8 -*-
"""
Master_6_1_2026-10-02.py — Task 12a: Einbau von 6.1 „Einordnung der Ergebnisse“ in den Manuskript-Master, nur Text

Setzt die Absätze aus Textvorschlag_6.1_2026-10-02.json (Kennungen A1 bis A6, Reihenfolge der Datei) unter die
Überschrift „6.1 Einordnung der Ergebnisse“, vor „6.2 Methodendiskussion“. Die Überschriften 6.1, 6.2 und 6.3 bleiben
stehen (Arbeitsnummern bis Task 18, Zusammenlegung von 6.2 und 6.3 nach Gliederung v6 erst in Task 12b/18).
Keine Objekte, keine Platzhalter (F17 § 5.3). Einträge der JSON mit "modul": true (offenes Modul A2-M) werden nicht
eingebaut, sondern im Protokoll gemeldet: Ein freigegebener Vergleichssatz muss vorher in den Wortlaut von A2
(Textvorschlag_6.1_2026-10-02.py, JSON neu erzeugt) eingearbeitet sein. Jede Operation greift genau einmal oder bricht ab.
Absätze ohne Direktformatierung (Formatvorlage Standard, kein pStyle), Text XML-maskiert. Verzeichnisse aktualisiert der
Verfasser mit F9. Nur nach Klickfreigabe des Wortlauts und ausdrücklicher Anweisung (F17 § 1.2), Word geschlossen.
Aufruf: python Master_6_1_2026-10-02.py <Master_ein.docx> <Textvorschlag_6.1.json> <Master_aus.docx> [--erwartet N]
  --erwartet N: erwartete Zahl der einzubauenden Absätze (Vorgabe 6), Abbruch bei Abweichung.
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import json
import zipfile
import shutil
import hashlib
from xml.sax.saxutils import escape

SRC, TV, DST = sys.argv[1], sys.argv[2], sys.argv[3]
ERWARTET = int(sys.argv[sys.argv.index('--erwartet') + 1]) if '--erwartet' in sys.argv else 6

H6 = ('berschrift1', '6 Diskussion')
H61 = ('berschrift2', '6.1 Einordnung der Ergebnisse')
H62 = ('berschrift2', '6.2 Methodendiskussion')
H63 = ('berschrift2', '6.3 Stärken und Limitationen')
H7 = ('berschrift1', '7 Fazit und Ausblick')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


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
            assert inhalt.count('<w:p ') + inhalt.count('<w:p>') == 1, 'verschachtelter Absatz bei %d' % a
        st = re.search(r'<w:pStyle w:val="([^"]+)"', inhalt)
        txt = ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', inhalt))
        out.append({'a': a, 'e': e, 'stil': st.group(1) if st else '', 'text': txt})
    return out


def einmal(liste, stil, text, name):
    treffer = [p for p in liste if p['stil'] == stil and p['text'].strip() == text]
    assert len(treffer) == 1, '%s: %d Treffer statt 1' % (name, len(treffer))
    return treffer[0]


P = absaetze(x)
n_vorher = len(P)
h6 = einmal(P, *H6, name='Überschrift 6')
h61 = einmal(P, *H61, name='Überschrift 6.1')
h62 = einmal(P, *H62, name='Überschrift 6.2')
h63 = einmal(P, *H63, name='Überschrift 6.3')
h7 = einmal(P, *H7, name='Überschrift 7')
i6, i61, i62, i63, i7 = [P.index(h) for h in (h6, h61, h62, h63, h7)]
assert i61 == i6 + 1 and i62 == i61 + 1 and i63 == i62 + 1 and i7 == i63 + 1, \
    'Kapitel 6 ist nicht leer oder anders gegliedert: %d %d %d %d %d' % (i6, i61, i62, i63, i7)
zwischen = x[h61['e']:h62['a']]
assert zwischen.strip() == '', 'zwischen den Überschriften 6.1 und 6.2 steht bereits Inhalt (%d Zeichen)' % len(zwischen)

tv = json.load(open(TV, encoding='utf-8'))
assert tv.get('abschnitt') == '6.1', 'JSON gehört nicht zu 6.1: %r' % tv.get('abschnitt')
module = [a for a in tv['absaetze'] if a.get('modul')]
einbau = [a for a in tv['absaetze'] if not a.get('modul')]
assert len(einbau) == ERWARTET, '%d statt %d einzubauende Absätze' % (len(einbau), ERWARTET)
for a in einbau:
    assert a['text'].strip() and '\n' not in a['text'], 'Absatz %s leer oder mit Zeilenumbruch' % a['kennung']
    assert len(a['text'].split()) == a['woerter'], 'Wortzahl von %s stimmt nicht mit der JSON überein' % a['kennung']
woerter = sum(len(a['text'].split()) for a in einbau)
assert woerter <= tv.get('budget', 700), '6.1 mit %d Wörtern über dem Budget %d' % (woerter, tv.get('budget', 700))

neu = ''.join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(a['text']) for a in einbau)
x2 = x[:h61['e']] + neu + x[h61['e']:]

P2 = absaetze(x2)
assert len(P2) == n_vorher + len(einbau), 'Absatzzahl nach dem Einbau unerwartet: %d' % len(P2)
j61 = P2.index(einmal(P2, *H61, name='Überschrift 6.1 nachher'))
j62 = P2.index(einmal(P2, *H62, name='Überschrift 6.2 nachher'))
region = P2[j61 + 1:j62]
assert [p['text'] for p in region] == [escape(a['text']) for a in einbau] or \
       [p['text'] for p in region] == [a['text'] for a in einbau], 'Rücklesen des eingebauten Texts weicht ab'
assert all(p['stil'] == '' for p in region), 'eingebaute Absätze tragen eine Formatvorlage'

tmp = DST + '.tmp'
with zipfile.ZipFile(SRC) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        daten = zi.read(it.filename)
        if it.filename == 'word/document.xml':
            daten = x2.encode('utf-8')
        zo.writestr(it, daten)
shutil.move(tmp, DST)

protokoll = [
    'Master_6_1_2026-10-02.py — Einbau 6.1',
    'Eingang: %s, MD5 %s, %d Absätze' % (SRC, md5(SRC), n_vorher),
    'Wortlaut: %s, %d Absätze eingebaut (%s), %d Wörter (Budget %d)' % (
        TV, len(einbau), ', '.join(a['kennung'] for a in einbau), woerter, tv.get('budget', 700)),
    'Nicht eingebaut (Modul, offen): %s' % (', '.join('%s (%d Wörter)' % (a['kennung'], a['woerter']) for a in module) or 'keines'),
    'Einfügestelle: nach „%s“, vor „%s“, Überschriften 6.1 bis 6.3 und 7 unverändert' % (H61[1], H62[1]),
    'Ausgabe: %s, MD5 %s, %d Absätze (vorher %d)' % (DST, md5(DST), len(P2), n_vorher),
]
print('\n'.join(protokoll))

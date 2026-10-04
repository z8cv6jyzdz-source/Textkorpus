# -*- coding: utf-8 -*-
"""
Abgleich_Hausstil_2026-09-30.py — Befund „Abgleich der Einleitung mit der Argumentationsstruktur“ nach .docx und .pdf
Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext.
Datierte Kopie von 03_Skripte\Argumentationsstruktur_Einleitungen_2026-09-30\Argumentationsstruktur_Hausstil_2026-09-30.py
(Fortsetzungsübergabe 1 § 6), unverändert bis auf diesen Kopf und den Aufruf.

Ruft Werkzeug_Hausstil_2026-09-25.py auf (pandoc, Hausstil nach Projektanweisungen § 9, soffice) und setzt danach:
- die Anhänge ab „Anhang A“ in einen eigenen Abschnitt im Querformat (breite Tabellen),
- Kopfzeilen jeder Tabelle als Wiederholungszeile, Tabellenzeilen nicht über Seiten getrennt,
- Code-Auszeichnung in 9 pt,
- DIN A4 in beiden Abschnitten (das Werkzeug setzt keine Seitengröße, soffice nahm sonst US Letter),
- die PDF neu mit soffice.
Aufruf: python Abgleich_Hausstil_2026-09-30.py <Befund.md> <Werkzeug_Hausstil_2026-09-25.py>
"""
import sys, os, subprocess, copy
from docx import Document
from docx.shared import Cm
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MD, WERKZEUG = sys.argv[1], sys.argv[2]
DOCX = os.path.splitext(os.path.abspath(MD))[0] + '.docx'
subprocess.run([sys.executable, WERKZEUG, MD, DOCX], check=True)

d = Document(DOCX)
body = d.element.body

# 1 DIN A4 hochkant für das ganze Dokument, dann Abschnittswechsel vor „Anhang A“, ab dort quer
erster = d.sections[0]
erster.orientation = WD_ORIENT.PORTRAIT
erster.page_width, erster.page_height = Cm(21.0), Cm(29.7)
kopf = next(p for p in d.paragraphs if p.text.startswith('Anhang A'))
hochkant = copy.deepcopy(body.sectPr)
leer = OxmlElement('w:p'); pPr = OxmlElement('w:pPr'); pPr.append(hochkant); leer.append(pPr)
kopf._p.addprevious(leer)
quer = d.sections[-1]
quer.orientation = WD_ORIENT.LANDSCAPE
quer.page_width, quer.page_height = Cm(29.7), Cm(21.0)
for rand in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'):
    setattr(quer, rand, Cm(2.0))

# 2 Tabellen: Kopfzeile wiederholen, Zeilen nicht trennen
for t in d.tables:
    for i, zeile in enumerate(t.rows):
        trPr = zeile._tr.get_or_add_trPr()
        if i == 0:
            h = OxmlElement('w:tblHeader'); h.set(qn('w:val'), 'true'); trPr.append(h)
        c = OxmlElement('w:cantSplit'); c.set(qn('w:val'), 'true'); trPr.append(c)

# 3 Code-Auszeichnung (Dateinamen, Pfade) in Textgröße, nicht größer als der Fließtext
from docx.shared import Pt
def laeufe():
    for p in d.paragraphs:
        yield from p.runs
    for t in d.tables:
        for zeile in t.rows:
            for zelle in zeile.cells:
                for p in zelle.paragraphs:
                    yield from p.runs
for r in laeufe():
    if r.style is not None and r.style.name == 'Verbatim Char':
        r.font.size = Pt(9)

d.save(DOCX)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(DOCX), DOCX],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('geschrieben:', DOCX, 'und', os.path.splitext(DOCX)[0] + '.pdf', '· Abschnitte:', len(Document(DOCX).sections))

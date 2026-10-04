# -*- coding: utf-8 -*-
"""
Werkzeug_Hausstil_2026-09-25.py — Markdown-Arbeitsdokument nach .docx (Hausstil) und .pdf
Bachelorarbeit U15-Plyometrie · Werkzeug für Arbeitsdokumente in Claude\02_Befunde (F14 § 9: Arial,
Navy-Überschriften #1F3864, hellblaue Bänder #D6E4F0, Zebra-Zeilen #EEF3F9). Kein Manuskripttext.

Aufruf: python Werkzeug_Hausstil_2026-09-25.py <Datei.md> [<Ziel.docx>]
  pandoc wandelt das Markdown, python-docx setzt den Hausstil, soffice erzeugt die PDF daneben.
Fassung: 2026-09-25, zweite Fassung (Überschriftenstile über den Dateinamen angesprochen, erste Fassung scheiterte an der Namensabbildung von python-docx).
"""
import sys, os, subprocess, shutil
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MD = sys.argv[1]
DOCX = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(MD)[0] + '.docx'
subprocess.run(['pandoc', MD, '-f', 'markdown', '-t', 'docx', '-o', DOCX, '--wrap=none'], check=True)

NAVY = RGBColor(0x1F, 0x38, 0x64)
def schattiere(zelle, hexfarbe):
    tcPr = zelle._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexfarbe); tcPr.append(shd)
def rahmen(tabelle):
    tbl = tabelle._tbl; tblPr = tbl.tblPr; borders = OxmlElement('w:tblBorders')
    for seite in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        b = OxmlElement('w:' + seite); b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '4'); b.set(qn('w:color'), 'BFBFBF'); borders.append(b)
    tblPr.append(borders)

d = Document(DOCX)
for stil in d.styles:
    try:
        if stil.type == 1: stil.font.name = 'Arial'; stil.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial') if stil.element.rPr is not None and stil.element.rPr.rFonts is not None else None
    except Exception: pass
d.styles['Normal'].font.size = Pt(10)
GROESSEN = {'Title': 18, 'Heading 1': 14, 'Heading 2': 12, 'Heading 3': 11}
for s in d.styles:
    # Zugriff über den Namen aus der Datei, nicht über den Word-internen Kleinschreibnamen von python-docx
    if s.type == 1 and s.name in GROESSEN:
        s.font.name = 'Arial'; s.font.size = Pt(GROESSEN[s.name]); s.font.bold = True; s.font.color.rgb = NAVY
for sec in d.sections:
    sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.2); sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
for p in d.paragraphs:
    for r in p.runs: r.font.name = 'Arial'
for t in d.tables:
    t.alignment = WD_TABLE_ALIGNMENT.CENTER; rahmen(t)
    for i, zeile in enumerate(t.rows):
        for zelle in zeile.cells:
            for p in zelle.paragraphs:
                for r in p.runs: r.font.name = 'Arial'; r.font.size = Pt(9)
            if i == 0:
                schattiere(zelle, 'D6E4F0')
                for p in zelle.paragraphs:
                    for r in p.runs: r.font.bold = True
            elif i % 2 == 0: schattiere(zelle, 'EEF3F9')
d.save(DOCX)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(os.path.abspath(DOCX)), DOCX], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('geschrieben:', DOCX, 'und', os.path.splitext(DOCX)[0] + '.pdf')

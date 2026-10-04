# Werkzeug_Aenderungsverfolgung_2026-09-12.py
# Helfer für Word-Änderungsverfolgung (w:ins/w:del) direkt in word/document.xml des Manuskript-Masters.
# Verfahren B der Textrevision (Uebergabe_4.4_Leistungsdiagnostik_2026-09-12.md § 6):
#   unzip Master → merge_runs.py (docx-Skill) → Tracker-Aufrufe → zip → validate.py --original --author "Claude"
#   → accept_changes.py als Gegenprobe → PDF-Render → Commit (neuer Ausgabepfad!) → erneut stagen, MD5 prüfen.
# Verwendung (Beispiel; Datei z. B. als tc_lib.py neben das Arbeitsverzeichnis kopieren):
#   from tc_lib import *
#   doc = etree.parse('work/word/document.xml'); kids = body_children(doc); T = Tracker(start_id=1000)
#   assert para_text(kids[95]).startswith('Die drei Zielgrößen')
#   T.replace_paragraph_text(kids[95], NEUER_TEXT)              # Absatz als Ganzes ersetzen (alt = w:del, neu = w:ins)
#   T.replace_substring(kids[105], 'alt', 'neu')                # wortgenau innerhalb eines Runs
#   for tr in tbl.findall(q('tr')): T.delete_row(tr)            # Tabellenzeilen als gelöscht markieren
#   tr_neu = T.new_row(['Zielgröße', 'n'], [2100, 450], header=True, fill='D9D9D9'); letzte_zeile.addnext(tr_neu)
#   doc.write('work/word/document.xml', xml_declaration=True, encoding='UTF-8', standalone=True)
# Keine Änderungen an Feldern (SEQ, TOC), Fußnoten, Formatvorlagen. Autor „Claude", IDs fortlaufend ab start_id.

"""Hilfsfunktionen für Word-Änderungsverfolgung (w:ins / w:del) direkt im document.xml.
Autor der Änderungen: "Claude". IDs werden fortlaufend vergeben.
"""
import copy
import re
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XML = 'http://www.w3.org/XML/1998/namespace'
NS = {'w': W}
AUTHOR = 'Claude'
DATE = '2026-09-12T15:00:00Z'


def q(tag):
    return '{%s}%s' % (W, tag)


class Tracker:
    def __init__(self, start_id=1000):
        self.next_id = start_id

    def _attrs(self, el):
        el.set(q('id'), str(self.next_id))
        el.set(q('author'), AUTHOR)
        el.set(q('date'), DATE)
        self.next_id += 1
        return el

    def ins_el(self):
        return self._attrs(etree.Element(q('ins')))

    def del_el(self):
        return self._attrs(etree.Element(q('del')))

    # ---------- Runs ----------
    def make_run(self, text, rpr=None):
        r = etree.Element(q('r'))
        if rpr is not None:
            r.append(copy.deepcopy(rpr))
        t = etree.SubElement(r, q('t'))
        t.text = text
        if text != text.strip() or '  ' in text:
            t.set('{%s}space' % XML, 'preserve')
        return r

    def run_to_deleted(self, r):
        """w:r → in w:del einhüllen, w:t → w:delText."""
        for t in r.findall(q('t')):
            t.tag = q('delText')
        d = self.del_el()
        parent = r.getparent()
        parent.replace(r, d)
        d.append(r)
        return d

    def delete_all_runs(self, p):
        for r in list(p.findall(q('r'))):
            self.run_to_deleted(r)

    def insert_runs(self, p, runs, after=None):
        """Neue Runs als w:ins anhängen (oder nach Element `after`)."""
        ins = self.ins_el()
        for r in runs:
            ins.append(r)
        if after is None:
            p.append(ins)
        else:
            after.addnext(ins)
        return ins

    def replace_paragraph_text(self, p, new_text, rpr=None):
        """Alle Runs des Absatzes als gelöscht markieren, neuen Text als eingefügt anhängen.
        rpr: optionales rPr-Element für den neuen Run (Kopie)."""
        self.delete_all_runs(p)
        return self.insert_runs(p, [self.make_run(new_text, rpr)])

    def replace_substring(self, p, old, new):
        """Wortgenaue Änderung innerhalb EINES Runs des Absatzes: old → new."""
        for r in p.findall(q('r')):
            t = r.find(q('t'))
            if t is None or t.text is None or old not in t.text:
                continue
            rpr = r.find(q('rPr'))
            before, after = t.text.split(old, 1)
            parent = r.getparent()
            idx = parent.index(r)
            parent.remove(r)
            pos = idx
            if before:
                parent.insert(pos, self.make_run(before, rpr)); pos += 1
            d = self.del_el(); dr = self.make_run(old, rpr)
            dr.find(q('t')).tag = q('delText')
            d.append(dr); parent.insert(pos, d); pos += 1
            i = self.ins_el(); i.append(self.make_run(new, rpr)); parent.insert(pos, i); pos += 1
            if after:
                parent.insert(pos, self.make_run(after, rpr)); pos += 1
            return True
        raise ValueError('substring not found in a single run: %r' % old[:60])

    # ---------- Absatzmarken ----------
    def mark_paragraph_inserted(self, p):
        ppr = p.find(q('pPr'))
        if ppr is None:
            ppr = etree.Element(q('pPr')); p.insert(0, ppr)
        rpr = ppr.find(q('rPr'))
        if rpr is None:
            rpr = etree.SubElement(ppr, q('rPr'))
        rpr.insert(0, self.ins_el())

    def mark_paragraph_deleted(self, p):
        ppr = p.find(q('pPr'))
        if ppr is None:
            ppr = etree.Element(q('pPr')); p.insert(0, ppr)
        rpr = ppr.find(q('rPr'))
        if rpr is None:
            rpr = etree.SubElement(ppr, q('rPr'))
        rpr.insert(0, self.del_el())

    def new_paragraph(self, text, ppr_template=None, rpr=None):
        """Neuer, als eingefügt markierter Absatz."""
        p = etree.Element(q('p'))
        if ppr_template is not None:
            p.append(copy.deepcopy(ppr_template))
        self.mark_paragraph_inserted(p)
        self.insert_runs(p, [self.make_run(text, rpr)])
        return p

    # ---------- Tabellenzeilen ----------
    def delete_row(self, tr):
        trpr = tr.find(q('trPr'))
        if trpr is None:
            trpr = etree.Element(q('trPr')); tr.insert(0, trpr)
        trpr.append(self.del_el())
        for r in list(tr.iter(q('r'))):
            if r.getparent().tag == q('del'):
                continue
            self.run_to_deleted(r)

    def new_row(self, cells, widths, header=False, jc_first='left', jc_rest='right', fill=None):
        """cells: Liste von Texten; widths: dxa je Zelle."""
        tr = etree.Element(q('tr'))
        trpr = etree.SubElement(tr, q('trPr'))
        if header:
            etree.SubElement(trpr, q('tblHeader'))
        trpr.append(self.ins_el())
        for i, (txt, wdt) in enumerate(zip(cells, widths)):
            tc = etree.SubElement(tr, q('tc'))
            tcpr = etree.SubElement(tc, q('tcPr'))
            tcw = etree.SubElement(tcpr, q('tcW')); tcw.set(q('w'), str(wdt)); tcw.set(q('type'), 'dxa')
            if fill:
                shd = etree.SubElement(tcpr, q('shd')); shd.set(q('val'), 'clear'); shd.set(q('color'), 'auto'); shd.set(q('fill'), fill)
            p = etree.SubElement(tc, q('p'))
            ppr = etree.SubElement(p, q('pPr'))
            sp = etree.SubElement(ppr, q('spacing')); sp.set(q('line'), '240'); sp.set(q('lineRule'), 'auto')
            jc = etree.SubElement(ppr, q('jc')); jc.set(q('val'), jc_first if i == 0 else jc_rest)
            prpr = etree.SubElement(ppr, q('rPr'))
            prpr.append(self.ins_el())
            s1 = etree.SubElement(prpr, q('sz')); s1.set(q('val'), '20')
            s2 = etree.SubElement(prpr, q('szCs')); s2.set(q('val'), '20')
            rpr = etree.Element(q('rPr'))
            if header:
                etree.SubElement(rpr, q('b')); etree.SubElement(rpr, q('bCs'))
            s1 = etree.SubElement(rpr, q('sz')); s1.set(q('val'), '20')
            s2 = etree.SubElement(rpr, q('szCs')); s2.set(q('val'), '20')
            self.insert_runs(p, [self.make_run(txt, rpr)])
        return tr


def body_children(doc):
    body = doc.find('.//w:body', NS)
    return [c for c in body if etree.QName(c).localname != 'sectPr']


def para_text(p):
    return ''.join(t.text or '' for t in p.iter(q('t')))


def words(s):
    return len(re.findall(r'\S+', s))

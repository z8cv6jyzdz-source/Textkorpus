# -*- coding: utf-8 -*-
"""
Blindpruefung_Vermerk_Bestaetigung_2026-09-25.py — Abschnitt 8 des Vermerks zur Blindprüfung nach der Klickfreigabe fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Blindprüfung 2.2, dritter Lauf (Nachtrag 3)

Zweck: Ersetzt im Vermerk `02_Befunde\Blindpruefung_Spezifikation_2026-09-24.docx` den Absatz des Abschnitts 8
(„Bestätigung des dritten Laufs“) durch den Wortlaut nach der Freigabe des Verfassers (Klick am 25.09.2026,
zusammen mit F2) und erzeugt die PDF neu. Sonst wird nichts geändert.
Aufruf: python Blindpruefung_Vermerk_Bestaetigung_2026-09-25.py <Vermerk.docx>
Fassung: 2026-09-25, erste Fassung. Ohne Semikolon.
"""
import sys
import os
import subprocess
from docx import Document

DOCX = sys.argv[1]
ALT_ANFANG = 'Maschinelle Prüfung im dritten Lauf bestanden.'
NEU = ('Maschinelle Prüfung im dritten Lauf bestanden. Der Verfasser hat Nachtrag 3 am 25.09.2026 per Klick freigegeben '
       'und diesen Lauf damit bestätigt, zusammen mit der Freigabe F2 (Sitzungsnotizen Rev. 91). Seitdem gilt die '
       'Spezifikation im Stand Nachtrag 3 (Teil F.8). Die Fassung im Blindordner bleibt der Stand Nachtrag 2, weil die '
       'Spezifikation nach dem Blindlauf nicht mehr an die zweite Instanz geht.')
d = Document(DOCX)
treffer = [p for p in d.paragraphs if p.text.startswith(ALT_ANFANG)]
if len(treffer) != 1:
    raise SystemExit('Absatz des Abschnitts 8 nicht eindeutig gefunden: %d Treffer' % len(treffer))
p = treffer[0]
for r in p.runs[1:]:
    r.text = ''
p.runs[0].text = NEU
d.save(DOCX)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(os.path.abspath(DOCX)), DOCX], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('Abschnitt 8 fortgeschrieben, PDF neu:', os.path.splitext(DOCX)[0] + '.pdf')

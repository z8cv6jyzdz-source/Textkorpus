# -*- coding: utf-8 -*-
"""
Blindpruefung_Vermerk_Nachtrag3_2026-09-25.py — Vermerk zur Blindprüfung um den dritten Lauf (Nachtrag 3) ergänzen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Schritt 2.2

Zweck: Hängt an 02_Befunde\\Blindpruefung_Spezifikation_2026-09-24.docx die Abschnitte 7 und 8 zum
dritten Lauf an (Zahlen aus der Skriptausgabe Blindpruefung_Spezifikation_2026-09-24.txt, dritter Lauf),
aktualisiert die Standzeile und erzeugt die PDF daneben. Formatierung wie im Bestand (Arial 9,5 pt,
Überschriften Heading 2, Tabellenkopf D6E4F0).
Aufruf: python Blindpruefung_Vermerk_Nachtrag3_2026-09-25.py <Vermerk.docx alt> <Ausgabe des dritten Laufs.txt> <Vermerk.docx neu>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re
import os
import subprocess
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ALT, TXT, NEU = sys.argv[1], sys.argv[2], sys.argv[3]
d = Document(ALT)
txt = open(TXT, encoding='utf-8').read()


def zahl(muster):
    m = re.search(muster, txt)
    if not m:
        raise SystemExit('nicht gefunden: ' + muster)
    return m.group(1)


n_studie = zahl(r'Studienzahlen \(kanonisch\): (\d+)')
n_vork = zahl(r'Zahlenvorkommen in der Spezifikation \(Zahlenliste\): (\d+)')
n_zeilen = zahl(r'Zeilen der Spezifikation: (\d+)')
n_neu = zahl(r'davon neu oder geändert gegenüber Nachtrag 2: (\d+)')
n_treffer = zahl(r'Treffer gesamt: (\d+)')
n_unv = zahl(r'Zeilen unverändert: (\d+) Vorkommen')
n_neuz = zahl(r'Zeilen neu oder geändert: (\d+) Vorkommen')
n_kenn = zahl(r'  Anlage Kennungen: (\d+)')
n_rdd = zahl(r'  Anlage Referenzdaten_Daten: (\d+)')
n_rd = zahl(r'  Anlage Referenzdaten: (\d+)')
n_kon = zahl(r'  Anlage Konstanten: (\d+)')
n_fb = zahl(r'  Anlage Fragebogen: (\d+)')
n_kr = zahl(r'  Anlage Koeffizienten_KR: (\d+)')
n_direkt = zahl(r'Zeilen, deren Zahlen nicht mit der Zahlenliste übereinstimmen: (\d+)')
direkt = re.search(r'Unterscheidungskräftige Zahlen im Text außerhalb der Zahlenliste:\n(.*?)\n\n', txt, re.S).group(1)
n_ausserhalb = len([l for l in direkt.split('\n') if l.strip() and l.strip() != 'keine'])
stich_neu = [l for l in txt.split('\n') if ' · neu oder geändert · ' in l]


def tausender(s):
    return '{:,}'.format(int(s)).replace(',', '.')


H2 = next(p for p in d.paragraphs if p.style is not None and p.style.name == 'Heading 2')


def absatz(text, fett=False, stil=None):
    p = d.add_paragraph()
    if stil:
        p.style = H2.style   # Stil über das Objekt eines vorhandenen Absatzes, der Name ist in der Datei nicht auflösbar
    r = p.add_run(text)
    r.font.name = 'Arial'
    r.font.size = Pt(13 if stil else 9.5)
    r.font.bold = True if (fett or stil) else None
    if stil:
        r.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    return p


def schattiere(zelle, hexfarbe):
    tcPr = zelle._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexfarbe)
    tcPr.append(shd)


def tabelle(kopf, zeilen):
    t = d.add_table(rows=1 + len(zeilen), cols=len(kopf))
    t.style = d.tables[0].style
    tbl = t._tbl
    borders = OxmlElement('w:tblBorders')
    for seite in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        b = OxmlElement('w:' + seite)
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), 'BFBFBF')
        borders.append(b)
    tbl.tblPr.append(borders)
    for j, k in enumerate(kopf):
        c = t.rows[0].cells[j]
        c.text = ''
        r = c.paragraphs[0].add_run(k)
        r.font.name = 'Arial'
        r.font.size = Pt(9)
        r.font.bold = True
        schattiere(c, 'D6E4F0')
    for i, z in enumerate(zeilen, 1):
        for j, v in enumerate(z):
            c = t.rows[i].cells[j]
            c.text = ''
            r = c.paragraphs[0].add_run(v)
            r.font.name = 'Arial'
            r.font.size = Pt(9)
            if i % 2 == 0:
                schattiere(c, 'EEF3F9')
    return t


# Standzeile anpassen
for p in d.paragraphs:
    if p.text.startswith('Vermerk · Stand 24.09.2026 · zwei Läufe'):
        for r in p.runs:
            r.text = ''
        p.runs[0].text = 'Vermerk · Stand 25.09.2026 · drei Läufe: Stand Nachtrag 1 und Stand Nachtrag 2 (24.09.2026), Stand Nachtrag 3 (25.09.2026, Abschnitte 7 und 8)'
        break

absatz('7 Dritter Lauf (Stand Nachtrag 3, 25.09.2026)', stil='Heading 2')
absatz('Anlass: Nachtrag 3 (Teil F.8) hält vier Klarstellungen aus der Code-Durchsicht über Kreuz der Phase 6.2 fest (Vorrang des Grunds „Eingang fehlt“ in S05, Bezugsmenge von Median und Mittel der Adhärenz in N4.3, Rangkriterium der Designmatrix, Dateinamen der Grafiken der Gegenprobe). Die Spezifikation ist damit nach dem Blindlauf geändert. Sie geht nicht mehr an die blinde Instanz, bleibt aber die Referenz für Anhang G und für jeden neuen Lauf beider Ketten. Deshalb ist die Prüfung nach Schritt 2.1 (Nachträge nur mit erneuter Blindprüfung) ein drittes Mal gelaufen, mit dem Skript in dritter Fassung (03_Skripte\\Blindpruefung_Spezifikation_2026-09-24.py, zweite Fassung im _Archiv).')
absatz('Zusätzliche Studienquellen im dritten Lauf, weil sie seit Phase 6 Ergebnisse enthalten: die Ergebnisdateien beider Implementierungen (Ergebnisse_R_2026-09-25.csv, Ergebnisse_Python_2026-09-25.csv), die Laufprotokolle der Gegenprobe und der Plausibilitätsprüfung, die drei Protokolle der Phase 6 (Abgleich, Durchsicht, Plausibilität), der Auswertungsplan mit dem Register (R11 nennt alte und neue Ergebnisse), die Rechenprobe des Handprobenblatts und die Projektanweisungen Fassung 14. Zusammen %s verschiedene Zahlen. Vergleichsfassung des Zeilenabgleichs ist der Stand Nachtrag 2. Die Anlage Kennungen ist unverändert.' % tausender(n_studie))
absatz('%s von %s Zeilen sind neu oder geändert. Die Zahlenliste führt %s Vorkommen, jedes mit Herkunft (neu eingeordnet sind die Zahlen der geänderten Zeilen, darunter die Toleranz 1e-7 als Regel und das Datum 25.09.2026). %s Treffer:' % (n_neu, n_zeilen, tausender(n_vork), tausender(n_treffer)))
tabelle(['Ort', 'Treffer', 'Getroffene Zahlen', 'Urteil'], [
    ['Spezifikationstext, unveränderte Zeilen', n_unv, 'wie im zweiten Lauf, dazu neu getroffen, weil die Ergebnisdateien und Protokolle sie nennen: Formelkonstanten 60 und 100, die Regelwerte 75 %, 1,96 und 0,45359237, die CASE-Nummern der Fallkorrekturen, die Kennungszahl 1.535 sowie Regel- und Paragraphennummern. Alle nach Teil H als Regel, Fundstelle, Konstante, Quellwert oder Wiederholung belegt', 'zulässig'],
    ['Spezifikationstext, neue oder geänderte Zeilen', n_neuz, '–', 'zulässig'],
    ['Anlage Kennungen', tausender(n_kenn), 'wie im zweiten Lauf: 30 und 505 als Testnamen, 95 in „95-%-KI“, 12.09 als Datum im Status', 'zulässig'],
    ['Anlage Referenzdaten_Daten', n_rdd, 'Beobachtungen und Werte veröffentlichter Referenzdatensätze, Gleichheit mit den zusätzlichen Quellen zufällig', 'zulässig'],
    ['Anlage Referenzdaten', n_rd, 'Sollwerte, Eingaben und Fundstellen aus Originalquellen, dazu Bestandteile von DOI und Seitenzahlen, die die Protokolle zitieren', 'zulässig'],
    ['Anlage Konstanten', n_kon, 'wie im zweiten Lauf, dazu Statusdaten, die die Protokolle nennen', 'zulässig'],
    ['Anlagen Fragebogen, Koeffizienten_KR, Vokabular', '%s · %s · 0' % (n_fb, n_kr), 'Codes des Codebuchs, Altersstufen der Tabelle von Khamis und Roche (1994)', 'zulässig'],
])
absatz('')
absatz('Direktscan: In %s Zeile weicht die Zahlenliste vom Text ab. Außerhalb der Zahlenliste stehen %s Ziffernfolgen, die an Bezeichnern hängen: die Datumsteile der Dateinamen Auswertungsverfahren_2026-09-24 und Durchsichtsprotokoll_2026-09-25 (der zweite neu mit Nachtrag 3), der Spielercode BW-14 (dreimal), SHA-256, ein DOI-Bestandteil und die Nummer einer NIST-Publikation. Keine ist eine Studienzahl.' % ('keiner' if n_direkt == '0' else n_direkt, n_ausserhalb))
absatz('Stichwortsuche in den neuen oder geänderten Zeilen: %d Fundstellen, beide das Wort „Python“ in N5.4, das die Gegenprobe als Implementierung benennt (Dateinamenszusatz). Kein Hinweis auf ein Ergebnis, weder der ersten Rechnung noch der Blindrechnung.' % len(stich_neu))
absatz('Urteil: Nachtrag 3 nennt keinen Messwert, keine Fallzahl, keine Streuung, keinen Messgüte-, p- oder Effektwert und kein anderes Ergebnis. Er verrät weder Richtung noch Größe eines Befunds. Die Klarstellungen sind Regeltext mit Fundstelle im Durchsichtsprotokoll. Die Spezifikation braucht keine Änderung.')
absatz('8 Bestätigung des dritten Laufs', stil='Heading 2')
absatz('Maschinelle Prüfung im dritten Lauf bestanden. Die Freigabe von Nachtrag 3 und die Bestätigung dieses Laufs erteilt der Verfasser per Klick zusammen mit der Freigabe F2 (Sitzungsnotizen Rev. 91). Bis dahin gilt die Spezifikation im Stand Nachtrag 2.')
d.save(NEU)
subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(os.path.abspath(NEU)), NEU], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('geschrieben:', NEU, 'und PDF')

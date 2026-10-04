# -*- coding: utf-8 -*-
"""
Endabgleich_Manuskript_2026-09-25.py — Phase 7.3: jede Ergebniszahl im Manuskript gegen das Kennzahlenblatt
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Schritt 7.3

Zweck: Liest den Manuskript-Master (nur lesend, keine Änderung), zerlegt den Text in Zahlen und ordnet
jede Zahl einer Klasse zu: Kennzahl des neuen Blatts (mit K-Kennung), überholte Kennzahl des Blatts
vom 22.09. (nur dort), Programmzahl (P-Kennung), Termin (K-03), Zitatjahr oder Seitenangabe, Verweis
auf Abschnitt, Tabelle, Abbildung oder Anhang, oder ungedeckt (Protokoll-, Antrags- oder Literaturangabe,
die nicht aus der Ergebnisdatei stammt). Dazu gezielte Satzprüfungen der Sätze, die Ergebniszahlen tragen
(4.2 Stichprobe, 4.4 Versuche und Tab. 1, 4.3 Termine, 4.5.1 Programmzahlen), formale Prüfungen nach F14 § 10
und eine nummerierte Vorschlagsliste. Der Master wird nicht verändert (Prozessregel F14 § 1.2).
Ergebniswerte stehen nur in den Ausgabedateien.
Aufruf: python Endabgleich_Manuskript_2026-09-25.py <Master.docx> <Kennzahlen_Werte.csv> <Kennzahlen_neu.md>
        <Kennzahlen_alt.md> <Programmkennzahlen.txt> <Objekte-Ordner> <Ausgabeordner>
Ausgabe: Endabgleich_Manuskript_2026-09-25.txt (Laufprotokoll), Endabgleich_Manuskript_2026-09-25_Zahlen.csv
        (jede Zahl mit Klasse), Abgleichprotokoll_Manuskript_2026-09-25.md (Befund und Vorschlagsliste).
Fassung: 2026-09-25, dritte Fassung (Prozessdaten der Auswertung als eigene Klasse, SP9c: die Festlegungsdaten 11.09., 12.09.
und 15.09.2026 in 4.7 werden gegen das Register geprüft, nicht gegen die Termine K-03). Zweite Fassung 25.09. nachmittags
(keine Kennungen im Manuskript, Vorschlag zu Tab. 1 nur bei Abweichung), erste Fassung 25.09. vormittags. Ohne Semikolon.
"""
import sys
import os
import re
import csv
import hashlib
import datetime
from collections import OrderedDict, defaultdict
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

MASTER, WERTE, KNEU, KALT, PDATEI, OBJ, AUS = sys.argv[1:8]
os.makedirs(AUS, exist_ok=True)
LAUF = []
SEMI = chr(59)


def log(*t):
    s = ' '.join(str(x) for x in t)
    LAUF.append(s)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def dez(s):
    """deutsche Zahl als float"""
    s = s.replace('−', '-').replace(' ', '').replace(' ', '')
    if re.fullmatch(r'-?\d{1,3}(\.\d{3})+(,\d+)?', s):
        s = s.replace('.', '')
    return float(s.replace(',', '.'))


def fmt(x, nd):
    s = ('%.' + str(nd) + 'f') % x
    return s.replace('.', ',')


# ------------------------------------------------------------------ Master lesen
d = Document(MASTER)
log('Endabgleich_Manuskript_2026-09-25.py, Laufprotokoll')
log('Datum:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
log('Master:', os.path.basename(MASTER), 'SHA-256', sha(MASTER), 'Größe', os.path.getsize(MASTER), 'Byte')
log('Kennzahlenblatt neu:', os.path.basename(KNEU), 'SHA-256', sha(KNEU))
log('Werte:', os.path.basename(WERTE), 'SHA-256', sha(WERTE))
log('Kennzahlenblatt alt:', os.path.basename(KALT), 'SHA-256', sha(KALT))
log('Programmkennzahlen:', os.path.basename(PDATEI), 'SHA-256', sha(PDATEI))

einheiten = []   # (nr, abschnitt, art, text, absatzindex, stil)
abschnitt = 'Vorspann'
kapitel = 'Vorspann'
pi = 0
for el in d.element.body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'p':
        p = Paragraph(el, d)
        st = p.style.name if p.style is not None else ''
        t = p.text
        if st.startswith('Heading'):
            abschnitt = t.strip()
            if st == 'Heading 1':
                kapitel = abschnitt
        einheiten.append((len(einheiten), abschnitt, 'Absatz', t, pi, st))
        pi += 1
    elif tag == 'tbl':
        tb = Table(el, d)
        zellen = []
        for r in tb.rows:
            zellen.append([c.text for c in r.cells])
        einheiten.append((len(einheiten), abschnitt, 'Tabelle', zellen, pi, 'Tabelle'))
log('Einheiten im Master:', len(einheiten), '(Absätze und Tabellen in Dokumentreihenfolge)')


def kurz(a):
    """Kapitelkurzname aus der Überschrift"""
    m = re.match(r'^(\d+(\.\d+)*)\s', a)
    return m.group(1) if m else a


# ------------------------------------------------------------------ Kennzahlen lesen
werte = list(csv.DictReader(open(WERTE, encoding='utf-8')))
log('Zeilen im Kennzahlenblatt (Werte):', len(werte))
TOK = re.compile(r'\d{1,2}\.\d{1,2}\.\d{4}|\d{1,2}\.\d{1,2}\.(?!\d)|\d\.\d(?:\.\d)?(?![\d,])|\d{1,2}:\d{2}|\d+(?:\.\d{3})+(?:,\d+)?|\d+,\d+|\d+')


def tokens(s):
    return TOK.findall(s.replace('−', '-'))


k_neu = defaultdict(set)      # Zahltoken -> K-Kennungen
for r in werte:
    for t in tokens(r['darstellung']):
        k_neu[t].add(r['k_kennung'])
k_neu_roh = defaultdict(set)
for r in werte:
    for t in re.findall(r'-?\d+(?:\.\d+)?', r['rohwerte']):
        k_neu_roh[t].add(r['k_kennung'])

# altes Blatt: Tabellenzeilen | K-xx.y | ... |
k_alt = defaultdict(set)
alt_zeilen = {}
for ln in open(KALT, encoding='utf-8'):
    m = re.match(r'^\|\s*(K-\d+[a-z]?\.\d+)\s*\|(.*)\|\s*$', ln)
    if m:
        alt_zeilen[m.group(1)] = m.group(2)
        felder = m.group(2).split('|')
        for t in tokens('|'.join(felder[1:])):   # erste Spalte ist die Bezeichnung (z. B. „505 links“), keine Kennzahl
            k_alt[t].add(m.group(1))
log('Zeilen im alten Kennzahlenblatt (22.09.):', len(alt_zeilen))

# Programmzahlen
p_tok = defaultdict(set)
p_zeilen = {}
for ln in open(PDATEI, encoding='utf-8'):
    m = re.match(r'^(P-\d\d)\s', ln)
    if m:
        p_zeilen[m.group(1)] = ln.strip()
        akt = m.group(1)
    elif ln.startswith('      ') and p_zeilen:
        p_zeilen[akt] += ' ' + ln.strip()
for k, v in p_zeilen.items():
    for t in tokens(v):
        p_tok[t].add(k)
log('Programmkennungen:', len(p_zeilen))

# Termine und Konstanten aus dem neuen Blatt
kneu_text = open(KNEU, encoding='utf-8').read()
termine = {}
for r in werte:
    if r['k_kennung'].startswith('K-03.') and r['k_kennung'] != 'K-03.4':
        dd = re.findall(r'\d{2}\.\d{2}\.\d{4}', r['darstellung'])
        termine[r['k_kennung']] = dd
m = re.search(r'Intervention (\d{2}\.\d{2}\.) bis (\d{2}\.\d{2}\.\d{4})', kneu_text)
intervention = (m.group(1) + m.group(2)[-4:], m.group(2)) if m else ()
datum_quelle = {}
for k, dd in termine.items():
    for x in dd:
        datum_quelle[x] = k
        datum_quelle[x[:6]] = k
for x in intervention:
    datum_quelle[x] = 'Intervention (Konstante der Spezifikation, K-03 Fußzeile)'
    datum_quelle[x[:6]] = datum_quelle[x]
# Antrag und Votum (F14 § 2, keine Ergebniszahlen)
ANTRAG = {'16.06.2026': 'Ethikantrag (Datum, F14 § 2)', '08.07.2026': 'Ethikvotum (Datum, F14 § 2)'}
for k, v in ANTRAG.items():
    datum_quelle[k] = v
# Prozessdaten der Auswertung (Festlegungen des Verfassers und Datum der ersten Auswertung, Register Auswertungsplan
# § 5.3 und § 5.10, F14 § 11.7 und § 11.9). Keine Termine und keine Ergebniszahlen, in 4.7 nach CONSORT 3b zu nennen.
PROZESSDATEN = {
    '11.09.2026': 'Mindestdosis sechs Einheiten und Fallzahlregel acht je Gruppe, Verfasser nach Sichtung der IG-Werte (Auswertungsplan § 5.3, F14 § 11.7 und § 11.9)',
    '12.09.2026': 'Adhärenzkriterium: Hauptanalyse mit allen Zugeteilten, Verfasser vor Kenntnis der KG-Werte (Auswertungsplan § 5.3)',
    '15.09.2026': 'erste Auswertung (Python, Analyseprotokoll_2026-09-15), Anlass für R5 (Auswertungsplan § 5.10)',
}
for k, v in PROZESSDATEN.items():
    datum_quelle[k] = 'Prozessdatum: ' + v

# ------------------------------------------------------------------ Klassifikation jeder Zahl
VERWEIS = re.compile(r'(Abschn\.|Abschnitt|Abschnitten|Kapitel|Tab\.|Tabelle|Tabellen|Abb\.|Abbildung|Anhang|Item|Items|Box|Stufe|Stufen|Woche|Wochen|W|KW|Block|Nr\.)\s*$')
VERWEIS_KETTE = re.compile(r'(\d\.\d(\.\d)?|\d)\s*(und|bis|beziehungsweise|,|–)\s*$')
ZITAT = re.compile(r"(et al\.,|[A-Za-zÄÖÜäöüß'’\-]+,|&\s+[A-Za-zÄÖÜäöüß'’\-]+,|[A-Za-zÄÖÜäöüß'’\-]+\s*\(|\d{4},|\d{4}\s*\()\s*$")
SEITE = re.compile(r'S\.\s*$|S\.\s*\d+[–-]$')
FACH = re.compile(r'(CONSORT|TIDieR|Tier|CR-|ISAK|Witty|RAMP|YouTube)\s*$|^\s*-\d+\s+Intermittent')

zahlen = []   # dicts
for nr, absch, art, inhalt, pidx, st in einheiten:
    if st.startswith('Heading'):
        continue
    texte = [inhalt] if art == 'Absatz' else [c for row in inhalt for c in row]
    for zi, text in enumerate(texte):
        t2 = text.replace('−', '-')
        for m in TOK.finditer(t2):
            tok = m.group(0)
            links = t2[max(0, m.start() - 40):m.start()].split(SEMI)[-1]
            rechts = t2[m.end():m.end() + 25].split(SEMI)[0]
            klasse, quelle = '', ''
            kap = kurz(absch)
            if art == 'Absatz' and re.match(r'^\d+(\.\d+)*\s', t2) and m.start() == 0:
                klasse, quelle = 'Nummer', 'Gliederungsnummer'
            elif re.fullmatch(r'\d{1,2}\.\d{1,2}\.', tok) and (VERWEIS.search(links) or VERWEIS_KETTE.search(links)) and not datum_quelle.get(tok, ''):
                klasse, quelle = 'Verweis', 'Abschnittsverweis'
            elif re.fullmatch(r'\d{1,2}\.\d{1,2}\.\d{4}', tok) or re.fullmatch(r'\d{1,2}\.\d{1,2}\.', tok):
                q = datum_quelle.get(tok, '')
                if q.startswith('K-03'):
                    klasse = 'Termin (K-03)'
                elif kap.startswith('4.5.2'):
                    klasse, q = 'Begleitbedingung (Anhang D)', ''
                elif re.search(r'Stand\s*$', links) or rechts.startswith(', S.'):
                    klasse, q = 'Zitatdatum', ''
                elif q.startswith('Prozessdatum'):
                    klasse = 'Prozessdatum (Register)'
                elif q:
                    klasse = 'Datum, Konstante'
                elif kap[:1] in ('1', '2', '3'):
                    klasse = 'Literaturangabe (Kapitel 1 bis 3)'
                else:
                    klasse = 'Datum, nicht im Kennzahlenblatt'
                quelle = q
            elif re.fullmatch(r'\d\.\d(\.\d)?', tok) and (VERWEIS.search(links) or VERWEIS_KETTE.search(links)):
                klasse, quelle = 'Verweis', 'Abschnittsverweis'
            elif re.search(r'KW\s*$|KW \d+[–-]$', links):
                klasse, quelle = 'Kalenderwoche (Antrag)', ''
            elif re.fullmatch(r'(19|20)\d{2}', tok) and (ZITAT.search(links) or rechts.startswith(')') or rechts.startswith(', S.')):
                klasse, quelle = 'Zitatjahr', ''
            elif re.fullmatch(r'20\d{2}', tok) and re.search(r'(Juni|Juli|August|September|Sommerpause|Saison|Sommer)\s*$', links):
                klasse, quelle = 'Kalenderjahr', ''
            elif SEITE.search(links):
                klasse, quelle = 'Seitenangabe', ''
            elif VERWEIS.search(links) and not re.search(r'(Woche|Wochen|W|Stufe|Stufen|Block)\s*$', links):
                klasse, quelle = 'Verweis', links.strip()[-12:]
            elif FACH.search(links):
                klasse, quelle = 'Fachbezeichnung', links.strip()[-12:]
            elif tok == '505' or re.match(r'^\s*-m-|^\s*m\b|^-m\b', rechts) or (tok in ('5', '10', '30') and re.match(r'^(, \d+ und \d+ m| und \d+ m|/\d+ m)', rechts)):
                klasse, quelle = 'Testname, Messstrecke', ''
            elif re.match(r'^-%-KI|^\s*× SD|^\s*× √|^\s*Zwischen-Athleten', rechts) or re.search(r'TE ×\s*$', links):
                klasse, quelle = 'Konstante der Methodik', ''
            elif kap.startswith('4.5.2'):
                klasse, quelle = 'Begleitbedingung (Anhang D)', ''
            elif kap[:1] in ('1', '2', '3') and not absch.startswith('Anhang'):
                klasse, quelle = 'Literaturangabe (Kapitel 1 bis 3)', ''
            elif tok in k_neu:
                kand = sorted(k_neu[tok])
                klasse = 'Kennzahl neu' + (' (mehrdeutig)' if len(kand) > 4 else '')
                quelle = ', '.join(kand[:6]) + (' …' if len(kand) > 6 else '')
            elif tok in k_alt:
                klasse, quelle = 'nur im alten Blatt (22.09.)', ', '.join(sorted(k_alt[tok]))
            elif tok in p_tok:
                klasse, quelle = 'Programmzahl', ', '.join(sorted(p_tok[tok]))
            elif kap.startswith('4.5.1') or re.search(r'(Woche|Wochen|W|Stufe|Stufen|Block)\s*$', links):
                klasse, quelle = 'Programmangabe (Trainingsdokumentation, Anhang B)', ''
            else:
                klasse, quelle = 'ungedeckt', ''
            zahlen.append(OrderedDict([('einheit', nr), ('abschnitt', absch), ('art', art), ('absatz', pidx), ('zelle', zi if art == 'Tabelle' else ''),
                                       ('zahl', tok), ('links', links.strip()), ('rechts', rechts.strip()), ('klasse', klasse), ('quelle', quelle)]))
with open(os.path.join(AUS, 'Endabgleich_Manuskript_2026-09-25_Zahlen.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(zahlen[0].keys()))
    w.writeheader()
    for z in zahlen:
        w.writerow(z)
log('Zahlen im Master gesamt:', len(zahlen))
klassen = defaultdict(int)
for z in zahlen:
    klassen[z['klasse']] += 1
for k in sorted(klassen):
    log('  Klasse', k + ':', klassen[k])

# ------------------------------------------------------------------ Hilfen
def absatztext(kap):
    """alle Absatztexte eines Abschnitts (Kurzname), mit Einheitennummer"""
    return [(nr, t) for nr, a, art, t, pidx, st in einheiten if art == 'Absatz' and kurz(a) == kap and not st.startswith('Heading')]


def wert(k):
    for r in werte:
        if r['k_kennung'] == k:
            return r
    raise SystemExit('Kennung fehlt im Blatt: ' + k)


def roh(k, i=0):
    return dez(wert(k)['rohwerte'].split(' ')[i].replace('.', ','))


def dar(k):
    """Zahlen der Darstellung einer Zeile (für Zeilen ohne Rohwerte)"""
    return tokens(wert(k)['darstellung'])


VORSCHLAEGE = []
BEFUNDE = []
GEDECKT = set()   # Einheiten (Absätze, Tabellen), die eine Satzprüfung mit Vorschlag abdeckt


def vorschlag(fund, befund, neu, grund):
    """Neufassungen ohne Kennungen im Text (Verfasserfestlegung 25.09.2026), die Kennungen wandern in die Begründung."""
    kenn = re.findall(r'\[(K-[^\]]*)\]', neu)
    neu = re.sub(r' ?\[K-[^\]]*\]', '', neu)
    if kenn:
        grund = grund + ' Kennungen: ' + ', '.join(kenn) + '.'
    VORSCHLAEGE.append((fund, befund, neu, grund))


def befund(text):
    BEFUNDE.append(text)


def satzanfang(t, n=9):
    return ' '.join(t.split()[:n]) + ' …'


def erster_satz_mit(kap, muster):
    for nr, t in absatztext(kap):
        for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ])', t):
            if re.search(muster, s):
                return nr, s
    return None, None


# ------------------------------------------------------------------ SP1 4.2 Fallzahlen und Jahrgänge
log('')
log('Satzprüfungen')
nr, s = erster_satz_mit('4.2', r'Analysiert wurden N = (\d+)')
sp = []
if s:
    n_text = int(re.search(r'N = (\d+)', s).group(1))
    n_ana = int(roh('K-01.14', 0) + roh('K-01.14', 1))
    ok = n_text == n_ana
    sp.append(('SP1a', '4.2 Analysepopulation N', 'Text ' + str(n_text), 'K-01.14 ' + wert('K-01.14')['darstellung'], ok))
    if not ok:
        vorschlag('4.2, Absatz mit „Analysiert wurden N = …“', 'N weicht von der Analysepopulation ab.', 'Analysiert wurden N = %d Spieler [K-01.14].' % n_ana, 'Bezugsmengen-Regel (2), Kennzahlenblatt K-01.14.')
nr, s = erster_satz_mit('4.2', r'Auf die Interventionsgruppe entfielen')
if s:
    m = re.search(r'entfielen (\d+) Spieler \(Verein A n = (\d+), Verein B n = (\d+), Geburtsjahrgang (\d{4})\), auf die Kontrollgruppe (\d+) \(Verein C, Geburtsjahrgang (\d{4})\)', s)
    if m:
        ig, a, b, jg_ig, kg, jg_kg = [int(x) for x in m.groups()]
        soll = (int(roh('K-01.14', 0)), int(dar('K-01.16')[0]), int(dar('K-01.16')[1]), int(dar('K-02.5')[0]), int(roh('K-01.14', 1)), int(dar('K-02.5')[1]))
        ist = (ig, a, b, jg_ig, kg, jg_kg)
        ok = ist == soll
        sp.append(('SP1b', '4.2 Zuteilung IG/KG, Vereine, Jahrgänge', 'Text ' + ' '.join(str(x) for x in ist), 'K-01.14, K-01.16, K-02.5: ' + ' '.join(str(x) for x in soll), ok))
        if not ok:
            vorschlag('4.2, Satz „Auf die Interventionsgruppe entfielen …“', 'Fallzahlen oder Jahrgänge weichen ab.',
                      'Auf die Interventionsgruppe entfielen %d Spieler (Verein A n = %d, Verein B n = %d, Geburtsjahrgang %d) [K-01.14, K-01.16, K-02.5], auf die Kontrollgruppe %d (Verein C, Geburtsjahrgang %d).' % soll,
                      'Kennzahlenblatt K-01.14, K-01.16, K-02.5.')
    else:
        sp.append(('SP1b', '4.2 Zuteilung', 'Satzmuster nicht erkannt', '', False))

# ------------------------------------------------------------------ SP2 4.2 Anthropometrie und %PAH
def msd(k, gruppe):
    r = wert(k)
    teile = r['darstellung'].split(' | ')
    t = teile[0] if gruppe == 'IG' else teile[1]
    m = re.match(r'([\d,]+) ± ([\d,]+) \(n = (\d+)\)', t)
    return m.group(1), m.group(2), int(m.group(3))


nr, s = erster_satz_mit('4.2', r'Interventionsgruppe war bei der Eingangstestung')
GEDECKT.add(nr)
m_ig = re.search(r'([\d,]+) ± ([\d,]+) Jahre alt, ([\d,]+) ± ([\d,]+) cm groß und ([\d,]+) ± ([\d,]+) kg schwer', s) if s else None
nr2, s2 = erster_satz_mit('4.2', r'Kontrollgruppe war ([\d,]+) ± ([\d,]+) Jahre')
m_kg = re.search(r'([\d,]+) ± ([\d,]+) Jahre alt, ([\d,]+) ± ([\d,]+) cm groß und ([\d,]+) ± ([\d,]+) kg schwer', s2) if s2 else None
nr3, s3 = erster_satz_mit('4.2', r'Reifestatus lag bei')
GEDECKT.add(nr3)
m_pah = re.search(r'([\d,]+) ± ([\d,]+) %PAH in der Interventionsgruppe und bei ([\d,]+) ± ([\d,]+) %PAH in der Kontrollgruppe', s3) if s3 else None
neu42 = {}
for gruppe, mm in (('IG', m_ig), ('KG', m_kg)):
    for i, k in enumerate(('K-02.1', 'K-02.2', 'K-02.3')):
        M, SD, n = msd(k, gruppe)
        neu42[(gruppe, k)] = (M, SD, n)
        if mm:
            ist = (mm.group(2 * i + 1), mm.group(2 * i + 2))
            ok = ist == (M, SD)
            sp.append(('SP2', '4.2 %s %s' % (gruppe, wert(k)['bezeichnung']), 'Text %s ± %s' % ist, '%s %s ± %s (n = %d)' % (k, M, SD, n), ok))
        else:
            sp.append(('SP2', '4.2 %s %s' % (gruppe, wert(k)['bezeichnung']), 'Satzmuster nicht erkannt', '', False))
for gruppe, gi in (('IG', 0), ('KG', 2)):
    M, SD, n = msd('K-02.4', gruppe)
    neu42[(gruppe, 'K-02.4')] = (M, SD, n)
    if m_pah:
        ist = (m_pah.group(gi + 1), m_pah.group(gi + 2))
        ok = ist == (M, SD)
        sp.append(('SP2', '4.2 %s %%PAH' % gruppe, 'Text %s ± %s' % ist, 'K-02.4 %s ± %s (n = %d)' % (M, SD, n), ok))
    else:
        sp.append(('SP2', '4.2 %s %%PAH' % gruppe, 'Satzmuster nicht erkannt', '', False))
if any(not x[4] for x in sp if x[0] == 'SP2'):
    ig = neu42
    vorschlag('4.2, Sätze „Die Interventionsgruppe war bei der Eingangstestung …“ bis „Der Reifestatus lag bei …“', 'Mindestens ein Kennwert weicht vom neuen Blatt ab (siehe Satzprüfung SP2).',
              'Die Interventionsgruppe war bei der Eingangstestung %s ± %s Jahre alt [K-02.1], %s ± %s cm groß [K-02.2] und %s ± %s kg schwer [K-02.3] (M ± SD). Die Kontrollgruppe war %s ± %s Jahre alt [K-02.1], %s ± %s cm groß [K-02.2] und %s ± %s kg schwer [K-02.3]. Der Reifestatus lag bei %s ± %s %%PAH in der Interventionsgruppe und bei %s ± %s %%PAH in der Kontrollgruppe [K-02.4].'
              % (ig[('IG', 'K-02.1')][0], ig[('IG', 'K-02.1')][1], ig[('IG', 'K-02.2')][0], ig[('IG', 'K-02.2')][1], ig[('IG', 'K-02.3')][0], ig[('IG', 'K-02.3')][1],
                 ig[('KG', 'K-02.1')][0], ig[('KG', 'K-02.1')][1], ig[('KG', 'K-02.2')][0], ig[('KG', 'K-02.2')][1], ig[('KG', 'K-02.3')][0], ig[('KG', 'K-02.3')][1],
                 ig[('IG', 'K-02.4')][0], ig[('IG', 'K-02.4')][1], ig[('KG', 'K-02.4')][0], ig[('KG', 'K-02.4')][1]),
              'Kennzahlenblatt K-02 (Analysepopulation, Menge ANA), Bezugsmengen-Regel (2). Der Reifestatus wird seit der Spezifikation S12 mit linear interpolierten Koeffizienten berechnet, Register R11 (Korrektur mit altem und neuem Ergebnis).')
else:
    befund('4.2: Alter, Körperhöhe, Körpermasse und %PAH je Gruppe stimmen mit K-02.1 bis K-02.4 des neuen Blatts überein (Analysepopulation). Es bleibt, die Kennungen bis zur Endfassung neben die Zahlen zu setzen.')

# ------------------------------------------------------------------ SP3 bis SP5 4.4 Versuche und Ausfälle
ZIEL6 = ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'SBJ']
gueltig_pre = {z: int(roh('K-11.3 ' + z, 0)) for z in ZIEL6}
kq_pre_ig = {z: roh('K-11.3 ' + z, 2) for z in ZIEL6}
kq_pre_kg = {z: roh('K-11.3 ' + z, 3) for z in ZIEL6}
KAT = ['TECH', 'ZEIT', 'FEHL', 'FALSCH', 'NANG', 'AUSL']


def kat(z, zeit, gruppe, name):
    r = wert('K-11.4 %s %s' % (z, zeit))
    felder = r['darstellung'].split(' ')
    if len(felder) != 12:
        raise SystemExit('K-11.4 %s %s: %d Felder statt 12' % (z, zeit, len(felder)))
    i = KAT.index(name) + (0 if gruppe == 'IG' else 6)
    return int(felder[i]) if felder[i] not in ('', '–', 'fehlend') else 0


n_ig, n_kg = int(roh('K-01.2', 0)), int(roh('K-01.3', 0))
n_pre = int(roh('K-01.1', 0))
vorgesehen = 3 * n_pre * 6
summe_gueltig = sum(gueltig_pre.values())
ungueltig = vorgesehen - summe_gueltig
kat_sum = {k: sum(kat(z, 'PRE', g, k) for z in ZIEL6 for g in ('IG', 'KG')) for k in KAT}
log('4.4 Versuche prä: vorgesehen', vorgesehen, '(3 Versuche × %d Spieler × 6 Messgrößen)' % n_pre, 'gültig', summe_gueltig, 'ungültig', ungueltig, 'Kategorien', kat_sum)
nr, s = erster_satz_mit('4.4', r'Von (\d+) vorgesehenen Prä-Versuchen')
if s:
    GEDECKT.add(nr)
    m = re.search(r'Von (\d+) vorgesehenen Prä-Versuchen waren (\d+) nicht gültig: (\d+) durch Lichtschrankenausfall, (\d+) durch einen aus Zeitgründen entfallenen dritten Versuch, (\d+) durch nicht wiederholbare Fehlversuche', s)
    if m:
        ist = tuple(int(x) for x in m.groups())
        soll = (vorgesehen, ungueltig, kat_sum['TECH'] + kat_sum['FALSCH'], kat_sum['ZEIT'], kat_sum['FEHL'])
        ok = ist == soll and kat_sum['NANG'] + kat_sum['AUSL'] == 0 and sum(soll[2:]) == ungueltig
        sp.append(('SP3', '4.4 Prä-Versuche vorgesehen, ungültig, drei Mechanismen', 'Text ' + ' '.join(str(x) for x in ist),
                   'K-01.1, K-11.3, K-11.4 Summe PRE: ' + ' '.join(str(x) for x in soll) + ' (TECH %d + FALSCH %d, ZEIT %d, FEHL %d, NANG %d, AUSL %d)' % (kat_sum['TECH'], kat_sum['FALSCH'], kat_sum['ZEIT'], kat_sum['FEHL'], kat_sum['NANG'], kat_sum['AUSL']), ok))
        if not ok:
            if kat_sum['FALSCH'] > 0:
                neu = 'Von %d vorgesehenen Prä-Versuchen [K-01.1, dreimal sechs Messgrößen] waren %d nicht gültig [K-11.3]: %d durch technischen Ausfall oder Fehlaufnahme der Lichtschranke, %d durch einen aus Zeitgründen entfallenen dritten Versuch, %d durch nicht wiederholbare Fehlversuche [K-11.4 Summe PRE].' % (vorgesehen, ungueltig, kat_sum['TECH'] + kat_sum['FALSCH'], kat_sum['ZEIT'], kat_sum['FEHL'])
            else:
                neu = 'Von %d vorgesehenen Prä-Versuchen [K-01.1, dreimal sechs Messgrößen] waren %d nicht gültig [K-11.3]: %d durch Lichtschrankenausfall, %d durch einen aus Zeitgründen entfallenen dritten Versuch, %d durch nicht wiederholbare Fehlversuche [K-11.4 Summe PRE].' % (vorgesehen, ungueltig, kat_sum['TECH'], kat_sum['ZEIT'], kat_sum['FEHL'])
            vorschlag('4.4, Satz „Von … vorgesehenen Prä-Versuchen …“', 'Versuchszahlen oder Ausfallkategorien weichen vom neuen Blatt ab (SP3).', neu, 'Kennzahlenblatt K-11.3 und K-11.4 (Kategorien der Spezifikation S05: TECH, ZEIT, FEHL, FALSCH).')
    else:
        sp.append(('SP3', '4.4 Prä-Versuche', 'Satzmuster nicht erkannt', '', False))

# SP4 Lichtschrankenausfälle je Spieler, Sprints
tech_ig = [kat(z, 'PRE', 'IG', 'TECH') / n_ig for z in ('Z05', 'Z10', 'Z30')]
tech_kg = [kat(z, 'PRE', 'KG', 'TECH') / n_kg for z in ('Z05', 'Z10', 'Z30')]
faktor = [(kat(z, 'PRE', 'KG', 'TECH') / n_kg) / (kat(z, 'PRE', 'IG', 'TECH') / n_ig) if kat(z, 'PRE', 'IG', 'TECH') > 0 else float('inf') for z in ('Z05', 'Z10', 'Z30')]
log('4.4 TECH je Spieler prä, Sprints: IG', [fmt(x, 2) for x in tech_ig], 'KG', [fmt(x, 2) for x in tech_kg], 'Faktor KG/IG', [('%.1f' % x) for x in faktor])
nr, s = erster_satz_mit('4.4', r'Lichtschrankenausfälle trafen')
if s:
    m = re.search(r'\(je Spieler ([\d,]+)[–-]([\d,]+) gegenüber ([\d,]+)[–-]([\d,]+)\)', s)
    mf = re.search(r'(\w+)- bis (\w+)mal häufiger', s)
    if m:
        ist = m.groups()
        soll = (fmt(min(tech_kg), 2), fmt(max(tech_kg), 2), fmt(min(tech_ig), 2), fmt(max(tech_ig), 2))
        ok = ist == soll
        sp.append(('SP4', '4.4 Lichtschrankenausfälle je Spieler (KG gegenüber IG, Sprints prä)', 'Text ' + '–'.join(ist[:2]) + ' gegenüber ' + '–'.join(ist[2:]), 'K-11.4 PRE TECH / K-01.2, K-01.3: ' + '–'.join(soll[:2]) + ' gegenüber ' + '–'.join(soll[2:]) + ' (Faktor KG/IG %s)' % ', '.join('%.1f' % x for x in faktor), ok))
        if not ok:
            vorschlag('4.4, Satz „Lichtschrankenausfälle trafen bei den Sprints …“', 'Ausfallraten je Spieler weichen ab (SP4).',
                      'Lichtschrankenausfälle trafen bei den Sprints die Kontrollgruppe häufiger als die Interventionsgruppe (je Spieler %s bis %s gegenüber %s bis %s) [K-11.4 PRE TECH, K-01.2, K-01.3].' % soll,
                      'Kennzahlenblatt K-11.4 (TECH prä je Sprintstrecke) bezogen auf die zugeteilten Spieler. Der Faktor „vier- bis achtmal“ ist am Verhältnis der Raten zu prüfen: %s.' % ', '.join('%.1f' % x for x in faktor))
    else:
        sp.append(('SP4', '4.4 Lichtschrankenausfälle je Spieler', 'Satzmuster nicht erkannt', '', False))
    if 'Zusammenhang' in s:
        vorschlag('4.4, Satz „Lichtschrankenausfälle trafen …“, Nebensatz „innerhalb der Gruppen ohne erkennbaren Zusammenhang …“', 'Der Satzteil ist die Aussage „die Ausfälle sind leistungsunabhängig“, die entfällt (F14 § 3.1, Umfangsdokument § 7 Nr. 2, Ausschluss Nr. 13).',
                  'Nebensatz streichen. Die Richtung der Verzerrung wird über die mittlere Zahl gültiger Versuche je Gruppe berichtet (Tab. H1) und in 6.3 als Limitation G5 eingeordnet.', 'Nicht signifikante Korrelationen bei 7 bis 13 Spielern je Verein können Unabhängigkeit nicht zeigen, die Korrelationen werden nicht mehr gerechnet.')

# SP5 mittlere gültige Versuche je Spieler
nr, s = erster_satz_mit('4.4', r'Im Mittel lagen je Zielgröße')
if s:
    m = re.search(r'([\d,]+) bis ([\d,]+) \(Interventionsgruppe\) beziehungsweise ([\d,]+) bis ([\d,]+) \(Kontrollgruppe\)', s)
    if m:
        ist = m.groups()
        soll = (fmt(min(kq_pre_ig.values()), 2), fmt(max(kq_pre_ig.values()), 2), fmt(min(kq_pre_kg.values()), 2), fmt(max(kq_pre_kg.values()), 2))
        ok = ist == soll
        sp.append(('SP5', '4.4 mittlere Zahl gültiger Prä-Versuche je Spieler, Spanne über sechs Messgrößen', 'Text IG %s bis %s, KG %s bis %s' % ist, 'K-11.3 k̄ prä: IG %s bis %s, KG %s bis %s' % soll, ok))
        if not ok:
            vorschlag('4.4, Satz „Im Mittel lagen je Zielgröße und zugeteiltem Spieler …“', 'Spannen der mittleren Zahl gültiger Versuche weichen ab (SP5).',
                      'Im Mittel lagen je Zielgröße und Spieler %s bis %s (Interventionsgruppe) beziehungsweise %s bis %s (Kontrollgruppe) gültige Versuche vor [K-11.3].' % soll,
                      'Kennzahlenblatt K-11.3 (Bezugsmenge: Spieler mit Zeilen zum Zeitpunkt). Die Spezifikation zählt je Spieler mit Versuchszeilen, das alte Blatt je zugeteiltem Spieler.')
    else:
        sp.append(('SP5', '4.4 mittlere gültige Versuche', 'Satzmuster nicht erkannt', '', False))

# ------------------------------------------------------------------ SP6 Tab. 1 gegen Tab_1_Messguete (R)
tab1_neu = list(csv.reader(open(os.path.join(OBJ, 'Tab_1_Messguete.csv'), encoding='utf-8')))
tab_master = [e for e in einheiten if e[2] == 'Tabelle' and e[3][0][0].startswith('Zielgröße')]
for e in tab_master:
    GEDECKT.add(e[0])
NORM = lambda s: re.sub(r'\s+', ' ', s.replace('−', '-').replace(' ', ' ')).strip()


def zielname(s):
    s = NORM(s).lower()
    s = re.sub(r'\s*\((s|cm)\)', '', s)
    s = s.replace('505 seitenmittel', '505-seitenmittel').replace('sprint ', '')
    return s


tab1_ok = True
if tab_master:
    tm = tab_master[0][3]
    kopf_m = [NORM(c) for c in tm[0]]
    kopf_n = [NORM(c) for c in tab1_neu[0]]
    log('Tab. 1 Master Spalten:', kopf_m)
    log('Tab. 1 neu Spalten:', kopf_n)
    gemeinsam = [c for c in kopf_m if c in kopf_n]
    fehlt_neu = [c for c in kopf_n if c not in kopf_m]
    fehlt_master = [c for c in kopf_m if c not in kopf_n]
    zeilen_n = {zielname(r[0]): r for r in tab1_neu[1:]}
    abw = []
    for r in tm[1:]:
        zn = zielname(r[0])
        if zn not in zeilen_n:
            abw.append((r[0], 'Zeile fehlt in der neuen Tabelle'))
            continue
        rn = zeilen_n[zn]
        for c in gemeinsam:
            a = NORM(r[kopf_m.index(c)])
            b = NORM(rn[kopf_n.index(c)])
            if re.sub(r'(\s*' + SEMI + r'\s*| bis )', '–', a) != re.sub(r'(\s*' + SEMI + r'\s*| bis )', '–', b):
                abw.append((r[0], c + ': Master „' + a.replace(SEMI, '⟨Semikolon⟩') + '“, neu „' + b + '“'))
    # SD-Spalte gegen S des Blatts (K-05 Spalte S)
    if 'SD' in kopf_m:
        for r in tm[1:]:
            zn = zielname(r[0])
            for k in ('K-05.1', 'K-05.2', 'K-05.3', 'K-05.4', 'K-05.5', 'K-05.6', 'K-05.7'):
                if zielname(wert(k)['bezeichnung'].replace('Messgüte ', '')) == zn:
                    teile = wert(k)['darstellung'].split(' | ')
                    s_neu = teile[4].split(' (')[0]
                    if NORM(r[kopf_m.index('SD')]) != s_neu:
                        abw.append((r[0], 'SD: Master „' + NORM(r[kopf_m.index('SD')]) + '“, Blatt S „' + s_neu + '“ (' + k + ')'))
    tab1_ok = not abw and not fehlt_neu and not fehlt_master
    for a in abw:
        log('Tab. 1 Abweichung:', a[0], a[1])
    sp.append(('SP6', 'Tab. 1 Master gegen Tab_1_Messguete.csv (R-Objekt) in den gemeinsamen Spalten ' + ', '.join(gemeinsam), '%d Abweichungen' % len(abw), 'Spalten nur neu: ' + ', '.join(fehlt_neu) + ' · nur Master: ' + ', '.join(fehlt_master), tab1_ok))
    if not tab1_ok:
        vorschlag('4.4, Tab. 1 (Messgüte)', ('Die Werte der gemeinsamen Spalten stimmen überein.' if not abw else '%d Zellen weichen ab (Laufprotokoll).' % len(abw)) + (' Die Spaltenform entspricht nicht dem Umfangsdokument § 3.2 (Spalten nur im Master: ' + ', '.join(fehlt_master) + ', fehlend: ' + ', '.join(fehlt_neu) + ').' if (fehlt_neu or fehlt_master) else ''),
                  'Tab. 1 durch Tab_1_Messguete aus `03_Skripte\\Objekte_2026-09-25\\Objekte_2026-09-25.docx` ersetzen (Spalten Zielgröße · n · TE [95-%-KI] · CV (%) · SESOI · TE/SESOI · TE post [95-%-KI], mit Anmerkung).',
                  'Umfangsdokument § 3.2 (ohne MDC, ohne TE/√n, mit TE post), R7 (Objekte aus der Ergebnisdatei), F14 § 5.3. Kennungen: K-05.1 bis K-05.7.')
else:
    sp.append(('SP6', 'Tab. 1', 'Tabelle nicht gefunden', '', False))

# ------------------------------------------------------------------ SP7 Anmerkung zu Tab. 1, SP8 TE/√n, MDC
for nr_, a, art, t, pidx, st in einheiten:
    if art != 'Absatz':
        continue
    if 'MDC' in t and kurz(a).startswith('4.4'):
        GEDECKT.add(nr_)
        m = re.search(r'Prä-Testung \(N = (\d+)\)', t)
        if m:
            sp.append(('SP7', 'Anmerkung Tab. 1: N', 'Text N = ' + m.group(1), 'K-01.1 ' + wert('K-01.1')['darstellung'] + ' (Eingangsgetestete)', int(m.group(1)) == n_pre))
        vorschlag('4.4, Anmerkung zu Tab. 1 (Absatz mit „MDC = …“)', 'Die Anmerkung nennt die kleinste nachweisbare Veränderung (MDC) je Zielgröße und die Zahl der Eingangsgetesteten (N). MDC entfällt, N gehört nach der Bezugsmengen-Regel (1) nicht in die Methodik.',
                  'Anmerkung durch die Anmerkung zu Tab_1_Messguete aus `03_Skripte\\Objekte_2026-09-25\\Objekte_2026-09-25.docx` ersetzen (n je Zielgröße prä in der Tabelle, n post in der Anmerkung, K-05.1 bis K-05.7).',
                  'Umfangsdokument § 7 Nr. 3 (MDC entfällt), Bezugsmengen-Regel (1), F14 § 11.3.')
    if 'TE/√n' in t or 'TE/√' in t:
        GEDECKT.add(nr_)
        vorschlag('4.4, Satz „… während der Standardfehler des Gruppenmittels (TE/√n) … Gruppenvergleiche trägt“', 'Das Kriterium TE/√n gegen SESOI entfällt (verkürzte Übertragung von Hopkins, 2000).',
                  'Satzteil streichen. Ersatz: „Die Auflösung des Gruppenvergleichs tragen die kleinste nachweisbare Effektstärke und die Breite der Konfidenzintervalle (Lakens, 2022).“',
                  'Umfangsdokument § 7 Nr. 1, F14 § 11.3, Ausschluss Nr. 14.')
    if re.search(r'Bereinigung der Standardabweichung um den Messfehler', t):
        befund('4.4: Der Satz zu Hopkins’ Bereinigung der Standardabweichung (0,2 · √(S² − e²)) bleibt sachlich richtig (Nachtrag 2: wird nicht gerechnet).')

# ------------------------------------------------------------------ SP9 4.3 Termine
for k in ('K-03.1', 'K-03.2', 'K-03.3'):
    dd = termine[k]
    for zi, t in enumerate(['prä', 'post']):
        treffer = [z for z in zahlen if z['zahl'] in (dd[zi], dd[zi][:6]) and kurz(z['abschnitt']).startswith('4')]
        sp.append(('SP9', '%s %s (%s)' % (wert(k)['bezeichnung'], t, dd[zi]), '%d Fundstellen in Kapitel 4' % len(treffer), (', '.join(sorted(set(kurz(z['abschnitt']) for z in treffer))) if treffer else 'im Master nicht genannt, Zeitstrahl Abb. H7 offen (Platzhalter in 4.3), kein Widerspruch'), True))
for z in zahlen:
    if z['klasse'] == 'Datum, nicht im Kennzahlenblatt' and kurz(z['abschnitt']).startswith('4'):
        verein = re.search(r'Verein[e]? ([ABC])', z['links'] + ' ' + z['rechts'])
        # nächstliegender Vereinsbuchstabe vor der Zahl
        mv = re.findall(r'\b([ABC]) \(', z['links'])
        vb = mv[-1] if mv else (verein.group(1) if verein else '')
        kk = {'A': 'K-03.1', 'B': 'K-03.2', 'C': 'K-03.3'}.get(vb, 'K-03')
        satz_ = ''
        for satz_k in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(])', einheiten[z['einheit']][3] if einheiten[z['einheit']][2] == 'Absatz' else ''):
            if z['zahl'] in satz_k:
                satz_ = satz_k
        zeitpunkt = 1 if re.search(r'Ausgangstest|Post|Abschluss', satz_[:satz_.find(z['zahl'])] if satz_ else z['links']) else 0
        neu_datum = (termine[kk][zeitpunkt] if kk != 'K-03' else 'siehe K-03.1 bis K-03.3')
        sp.append(('SP9b', '%s Absatz %s: Datum „%s“ (Kontext …%s %s %s…)' % (kurz(z['abschnitt']), z['absatz'], z['zahl'], z['links'][-25:], z['zahl'], z['rechts'][:12]), 'Text ' + z['zahl'], kk + ': ' + (wert(kk)['darstellung'] if kk != 'K-03' else 'Termine K-03.1 bis K-03.3'), False))
        vorschlag('%s, Absatz %s, Datum „%s“' % (kurz(z['abschnitt']), z['absatz'], z['zahl']), 'Das Datum steht nicht im Kennzahlenblatt (Termine K-03, Datensicherung Phase 1). Kontext: …%s %s %s…' % (z['links'][-30:], z['zahl'], z['rechts'][:15]),
                  'Datum nach %s setzen: %s [%s] (%s).' % (kk, neu_datum, kk, 'Ausgangstestung' if zeitpunkt else 'Eingangstestung'), 'Zahlenregel F14 § 1.2, Termine K-03 (Belegprotokoll der Datensicherung 24.09., Testdatum post Verein C).')
        GEDECKT.add(z['einheit'])

for z in zahlen:
    if z['klasse'] == 'Prozessdatum (Register)' and kurz(z['abschnitt']).startswith('4'):
        sp.append(('SP9c', '%s Absatz %s: Prozessdatum „%s“ (Kontext …%s %s %s…)' % (kurz(z['abschnitt']), z['absatz'], z['zahl'], z['links'][-25:], z['zahl'], z['rechts'][:12]), 'Text ' + z['zahl'], 'Register: ' + PROZESSDATEN[z['zahl']][:90], True))
        GEDECKT.add(z['einheit'])

# ------------------------------------------------------------------ SP10 4.1 Planungsfallzahl, 4.6 Antragskriterium
nr, s = erster_satz_mit('4.1', r'geplante Fallzahl von etwa (\d+)')
if s:
    m = re.search(r'etwa (\d+)', s)
    sp.append(('SP10', '4.1 geplante Fallzahl (Antrag, Planungsstand)', 'Text ' + m.group(1), 'Antrag ≈ 45 (F14 § 11.1), keine Ergebniszahl', m.group(1) == '45'))
nr, s = erster_satz_mit('4.6', r'mindestens (\d+) %')
if s:
    m = re.search(r'mindestens (\d+) %', s)
    sp.append(('SP10', '4.6 Antragskriterium', 'Text ' + m.group(1) + ' %', 'Antrag 75 % = 9 von 12 (F14 § 11.7), keine Ergebniszahl', m.group(1) == '75'))

# ------------------------------------------------------------------ SP11 4.5.1 Programmzahlen gegen P-Datei
nr, s = erster_satz_mit('4.5.1', r'Bodenkontakte je Einheit stiegen')
if s:
    ist = re.findall(r'\d+', s)
    soll = re.findall(r'\d+', p_zeilen['P-01'].split(':')[1].split('(')[0])
    sp.append(('SP11', '4.5.1 Kontakte je Einheit W1 bis W6', 'Text ' + ' '.join(ist), 'P-01 ' + ' '.join(soll), ist == soll))
nr, s = erster_satz_mit('4.5.1', r'Aufwärmvideo dauerte')
if s:
    ist = re.findall(r'\d+:\d\d', s)
    p10 = p_zeilen['P-10']
    erw = re.findall(r'Erwärmungsvideo (\d+:\d\d)', p10)
    m = re.search(r'Spanne Sitzung (\d+:\d\d)[–-](\d+:\d\d) min \(Wochenvideo (\d+:\d\d)[–-](\d+:\d\d)\)', p10)
    soll = [erw[0], m.group(3), m.group(4), m.group(1), m.group(2)] if (erw and m) else []
    sp.append(('SP11', '4.5.1 Videodauern (Aufwärmvideo, Wochenvideo von bis, Einheit von bis)', 'Text ' + ' '.join(ist), 'P-10 ' + ' '.join(soll), ist == soll))
nr, s = erster_satz_mit('4.5.1', r'begann das Programm mit (\d+) statt')
if s:
    m = re.search(r'mit (\d+) statt etwa (\d+) bis (\d+) Kontakten je Einheit und enthielt in Woche (\d+) und (\d+) keinen', s)
    p12 = p_zeilen['P-12']
    m2 = re.search(r'Startvolumen (\d+) \(< (\d+)[–-](\d+)\)', p12)
    m3 = re.search(r'kein Kraftblock W(\d+)[–-](\d+)', p12)
    if m and m2 and m3:
        sp.append(('SP11', '4.5.1 Abweichung vom Antrag: Startvolumen, Antragsspanne, Wochen ohne Kraftblock', 'Text ' + ' '.join(m.groups()), 'P-12 ' + ' '.join(m2.groups() + m3.groups()), m.groups() == m2.groups() + m3.groups()))
nr, s = erster_satz_mit('4.5.1', r'Zwischen den Sätzen lagen')
if s:
    mp = re.search(r'Sätzen lagen (\d+) Sekunden \(Stufe-\d-Übungen: (\d+) Sekunden\), zwischen den Übungen (\d+) Sekunden', s)
    ist = list(mp.groups()) if mp else re.findall(r'\d+', s)
    p09 = p_zeilen['P-09']
    soll = re.findall(r'(\d+) s zwischen Sätzen|(\d+) s zwischen den Stufe|(\d+) s zwischen Übungen', p09)
    soll = [x for g in soll for x in g if x]
    sp.append(('SP11', '4.5.1 Pausen (Sätze, Stufe-1-Sätze, Übungen)', 'Text ' + ' '.join(ist), 'P-09 ' + ' '.join(soll) + ' (⚠ P-09: die Stufe-1-Pause steht nur im Produktionsleitfaden, am Video prüfen)', [x for x in ist if x in soll] == ist and len(ist) == len(soll)))
nr, s = erster_satz_mit('4.5.1', r'Interventionsphase|Programmwochen|zwei Einheiten je Woche')
for nr_, t in absatztext('4.5.1'):
    m = re.search(r'\((\d{2}\.\d{2}\.)\s*bis (\d{2}\.\d{2}\.\d{4}), zwei Einheiten je Woche\)', t)
    if m:
        sp.append(('SP11', '4.5.1 Programmzeitraum', 'Text ' + m.group(1) + ' bis ' + m.group(2), 'Intervention ' + ' bis '.join(intervention) + ' (Konstante der Spezifikation)', (m.group(1) + m.group(2)[-4:], m.group(2)) == intervention))

for e in sp:
    log('  %s | %s | %s | %s | %s' % (e[0], e[1], e[2], e[3], 'stimmt' if e[4] else 'ABWEICHUNG'))
log('Satzprüfungen:', len(sp), 'davon stimmt', sum(1 for e in sp if e[4]), 'Abweichungen', sum(1 for e in sp if not e[4]))

# ------------------------------------------------------------------ altes gegen neues Blatt (K-02b, K-05, K-04)
log('')
log('Vergleich altes Blatt (22.09.) gegen neues Blatt (25.09.) in den vom Master genutzten Zeilen')
diff_alt = []
for i in range(1, 5):
    alt = alt_zeilen.get('K-02b.%d' % i, '')
    neu = wert('K-02.%d' % i)['darstellung']
    a_tok = tokens(alt)
    n_tok = tokens(neu)
    gleich = a_tok[:6] == n_tok[:6]
    log('  K-02b.%d alt gegen K-02.%d neu:' % (i, i), 'gleich' if gleich else 'verschieden', '|', alt.strip(), '|', neu)
    if not gleich:
        diff_alt.append('K-02.%d' % i)
vergleich = []
for i in range(1, 5):
    alt = alt_zeilen.get('K-02b.%d' % i, '')
    neu = wert('K-02.%d' % i)['darstellung']
    gleich = tokens(alt)[:6] == tokens(neu)[:6]
    vergleich.append(('K-02b.%d → K-02.%d (%s)' % (i, i, wert('K-02.%d' % i)['bezeichnung']), 'gleich' if gleich else 'verschieden', '' if gleich else 'R11 (Reifestatus nach S12)'))
alt_k05 = {}
for i in range(1, 8):
    fa_ = [x.strip() for x in alt_zeilen.get('K-05.%d' % i, '').split('|')]
    if fa_ and fa_[0]:
        alt_k05[zielname(fa_[0])] = ('K-05.%d' % i, fa_)
for i in range(1, 8):
    neu = wert('K-05.%d' % i)['darstellung']
    zn = zielname(wert('K-05.%d' % i)['bezeichnung'].replace('Messgüte ', ''))
    k_alt_name, fa = alt_k05.get(zn, ('', []))
    alt = ' | '.join(fa)
    fn = [x.strip() for x in neu.split('|')]
    # alt: Zielgröße, n, M ± SD, SESOI, TE, CV, TE/SESOI, TE/√n, MDC · neu: n, TE [KI], df, CV, S (n), SESOI, TE/SESOI, TE>SESOI, TE post
    if len(fa) >= 9 and len(fn) >= 9:
        sd_alt = fa[2].split('±')[1].strip()
        te_alt, sesoi_alt, cv_alt, rts_alt = fa[4], fa[3], fa[5], fa[6]
        te_neu, cv_neu, s_neu, sesoi_neu, rts_neu = fn[1].split(' [')[0], fn[3], fn[4].split(' (')[0], fn[5], fn[6]
        felder = [('TE', te_alt, te_neu), ('CV', cv_alt, cv_neu), ('SD/S', sd_alt, s_neu), ('SESOI', sesoi_alt, sesoi_neu), ('TE/SESOI', rts_alt, rts_neu)]
        versch = [f[0] for f in felder if f[1] != f[2]]
        vergleich.append(('%s alt → K-05.%d neu (%s)' % (k_alt_name, i, fa[0]), 'gleich' if not versch else 'verschieden in ' + ', '.join(versch), '' if not versch else ('R11 (TE des Seitenmittels, Paarung nach Versuchsnummer)' if 'Seitenmittel' in fa[0] else 'prüfen')))
        log('  %s alt:' % k_alt_name, alt.strip(), '| K-05.%d neu:' % i, neu, '| verschieden:', ', '.join(versch) or 'nein')
    else:
        vergleich.append(('K-05.%d (%s)' % (i, zn), 'Zeile im alten Blatt nicht gefunden', ''))
for k in ('K-04.1', 'K-04.2', 'K-04.3', 'K-04.4', 'K-04.5', 'K-04.6'):
    alt = alt_zeilen.get(k, '')
    log('  alt %s: %s' % (k, alt.strip()))

# ------------------------------------------------------------------ formale Prüfungen je Abschnitt
log('')
log('Formale Prüfungen (F14 § 10) je Abschnitt in Kapitel 4')
formal = []
for nr_, a, art, t, pidx, st in einheiten:
    if art != 'Absatz' or st.startswith('Heading') or not kurz(a).startswith('4'):
        continue
    semi = t.count(SEMI)
    verw = len(re.findall(r'Abschn(itt|itten|\.)\s*\d', t)) + len(re.findall(r'Kapitel \d', t)) + len(re.findall(r'Abschnitt \d', t))
    lang = [len(x.split()) for x in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(])', t) if len(x.split()) > 40]
    marker = len(re.findall(r'\[(BELEGT|EXTRAPOLATION|FÜR SCHWAB)[^\]]*\]', t))
    if semi or verw or lang or marker:
        formal.append((kurz(a), pidx, semi, verw, len(lang), marker))
        log('  %s Absatz %d: Semikola %d, Abschnittsverweise %d, Sätze über 40 Wörter %d, Marker %d' % (kurz(a), pidx, semi, verw, len(lang), marker))
verbot = {'randomisiert': r'\brandomisiert', 'SPSS': r'SPSS', 'leistungsunabhängig': r'leistungsunabhängig', 'MDC': r'\bMDC\b', 'TE/√n': r'TE/√n', 'ITT': r'\bITT\b', 'Signifikanz': r'[Ss]ignifikan'}
verbot_fund = defaultdict(list)
for nr_, a, art, t, pidx, st in einheiten:
    tt = t if art == 'Absatz' else ' '.join(c for row in t for c in row)
    for name, mu in verbot.items():
        for m in re.finditer(mu, tt):
            kontext = tt[max(0, m.start() - 30):m.start()].split(SEMI)[-1] + tt[m.start():m.end() + 30].split(SEMI)[0]
            verbot_fund[name].append((kurz(a) if not st.startswith('Heading') else a, pidx, kontext.replace('\n', ' ')))
for name in verbot:
    log('  Wortprüfung %s: %d Fundstellen' % (name, len(verbot_fund[name])), '· '.join('%s (%s)' % (f[0], f[2].strip()) for f in verbot_fund[name][:6]))
for f in verbot_fund['SPSS']:
    vorschlag('%s (%s)' % (f[0], 'Überschrift' if 'Anhang' in f[0] else 'Absatz %d' % f[1]), 'Nennung von SPSS: „' + f[2].strip() + '“. SPSS entfällt als Werkzeug (F14 § 11.4, § 11.10).',
              'Anhang G: Sensitivitäts-Poweranalyse und R-Skripte (Gliederung v4). Im Text R mit Version und tragenden Paketen nennen, Zitierform aus citation() der Blindrechnung.', 'F14 § 5.1 (Nachspann), § 11.10, Auswertungsverfahren 8.1.')
for f in verbot_fund['randomisiert']:
    if str(f[0]).startswith('2'):
        continue
    if 'nicht randomisiert' not in f[2] and 'nicht-randomisiert' not in f[2] and 'Nicht-randomisiert' not in f[2]:
        vorschlag('%s (Absatz %d)' % (f[0], f[1]), 'Wort „randomisiert“ als Studienbezeichnung: „' + f[2].strip() + '“', 'Sprachregelung F14 § 2 prüfen (quasi-experimentell, kontrolliert, pragmatische Zuteilung auf Vereinsebene). Zulässig nur als Verneinung oder für fremde Studien.', 'F14 § 2 Sprachregelung.')

# ------------------------------------------------------------------ ungedeckte und veraltete Zahlen in Kapitel 4
ung = [z for z in zahlen if z['klasse'] in ('ungedeckt', 'nur im alten Blatt (22.09.)') and kurz(z['abschnitt']).startswith('4')]
log('')
log('Zahlen in Kapitel 4 ohne Deckung im neuen Blatt (ungedeckt oder nur alt):', len(ung))
for z in ung:
    log('  %s Absatz %s: „…%s %s %s…“ [%s %s]' % (kurz(z['abschnitt']), z['absatz'], z['links'][-30:], z['zahl'], z['rechts'][:20], z['klasse'], z['quelle']))
veraltet = [z for z in zahlen if z['klasse'] == 'nur im alten Blatt (22.09.)' and z['einheit'] not in GEDECKT]
gruppen = OrderedDict()
for z in veraltet:
    gruppen.setdefault((kurz(z['abschnitt']), z['absatz'], z['einheit']), []).append(z)
for (kap_, pidx_, nr_), zz in gruppen.items():
    vorschlag('%s, Absatz %s' % (kap_, pidx_), 'Zahlen, die nur im Kennzahlenblatt vom 22.09. stehen: ' + ' · '.join('„%s“ (%s, Kontext …%s %s %s…)' % (z['zahl'], z['quelle'], z['links'][-20:], z['zahl'], z['rechts'][:12]) for z in zz),
              'Zahl aus der zugehörigen Zeile des neuen Blatts übernehmen und Kennung daneben setzen. Betrifft nach R11 alle Größen mit %PAH und den TE des 505-Seitenmittels.', 'Zahlenregel F14 § 1.2, Register R11.')

# ------------------------------------------------------------------ Protokoll schreiben
md = []
md.append('# Abgleichprotokoll Manuskript — Phase 7.3, Endabgleich gegen das Kennzahlenblatt vom 25.09.2026')
md.append('')
md.append('**Erzeugt am %s von `Claude\\03_Skripte\\Endabgleich_Manuskript_2026-09-25.py` · Master `Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (SHA-256 `%s`, %d Byte, nur gelesen) · Kennzahlenblatt `Kennzahlen_2026-09-25.md` (SHA-256 `%s`) · Objekte aus `Objekte_2026-09-25.R`.**' % (datetime.datetime.now().strftime('%d.%m.%Y %H:%M'), sha(MASTER), os.path.getsize(MASTER), sha(KNEU)))
md.append('')
md.append('Auswertungsverfahren 2026-09-24, Schritt 7.3: jede Ergebniszahl im Manuskript gegen das Kennzahlenblatt, per Skript. Der Master wurde nicht verändert (Prozessregel F14 § 1.2). Die Vorschlagsliste in Teil 5 ist zur Begutachtung durch den Verfasser bestimmt, Freigabe je Abschnitt. Kennungen stehen nicht im Manuskript (Verfasserfestlegung 25.09.2026), die Zuordnung jeder Zahl zu ihrer Kennung steht in der Zahlenliste dieses Laufs. Vollständige Zahlenliste mit Klasse je Zahl: `Endabgleich_Manuskript_2026-09-25_Zahlen.csv`, Laufprotokoll: `Endabgleich_Manuskript_2026-09-25.txt` (beide in `03_Skripte`).')
md.append('')
md.append('## 1 Bestand des Masters')
md.append('')
kap_stat = OrderedDict()
for nr_, a, art, t, pidx, st in einheiten:
    if st.startswith('Heading') or art != 'Absatz':
        continue
    k = kurz(a)
    kap_stat.setdefault(k, [0, 0])
    kap_stat[k][0] += len(t.split())
    kap_stat[k][1] += 1
geschrieben = [k for k in kap_stat if kap_stat[k][0] > 30 and k[0] in '1234567']
ohne_text = [k for k in ('4.7', '5.1', '5.2', '6.1', '6.2', '6.3', '7') if k not in geschrieben]
md.append('Geschriebene Abschnitte (mehr als 30 Wörter Absatztext): ' + ', '.join(geschrieben) + '. Ohne Text: ' + ', '.join(ohne_text) + '. Die Ergebniszahlen des Blatts K-04, K-06 bis K-10 und K-12 haben deshalb noch keine Fundstelle im Master. Der Abgleich betrifft die Zahlen, die der Master bereits trägt: 4.2 (Stichprobe), 4.3 (Termine), 4.4 (Versuche, Tab. 1), 4.5.1 (Programmzahlen), 4.6 (Antragskriterium).')
md.append('')
md.append('| Abschnitt | Wörter Absatztext | Absätze |')
md.append('|---|---:|---:|')
for k in geschrieben:
    md.append('| %s | %d | %d |' % (k, kap_stat[k][0], kap_stat[k][1]))
md.append('')
md.append('## 2 Klassifikation aller Zahlen des Masters')
md.append('')
md.append('Jede Zahl des Masters (Absätze und Tabellen, ohne Gliederungsnummern der Überschriften) wurde einer Klasse zugeordnet. „Kennzahl neu“ heißt, die Zahl kommt in der Darstellung mindestens einer Zeile des neuen Blatts vor (mehrdeutig bei mehr als vier Zeilen, meist kleine ganze Zahlen). „Ungedeckt“ sind Protokoll-, Antrags- und Literaturangaben, die nicht aus der Ergebnisdatei stammen und nach der Zahlenregel auch nicht aus ihr stammen müssen. Die Klasse ist ein Suchergebnis, die Zuordnung zur Kennung leisten die Satzprüfungen in Teil 3.')
md.append('')
md.append('| Klasse | Zahlen | davon in Kapitel 4 |')
md.append('|---|---:|---:|')
for k in sorted(klassen):
    md.append('| %s | %d | %d |' % (k, klassen[k], sum(1 for z in zahlen if z['klasse'] == k and kurz(z['abschnitt']).startswith('4'))))
md.append('')
md.append('Zahlen in Kapitel 4 ohne Deckung im neuen Blatt (Klasse ungedeckt oder nur alt), mit Kontext:')
md.append('')
md.append('| Abschnitt | Absatz | Kontext | Zahl | Klasse | Quelle |')
md.append('|---|---:|---|---|---|---|')
for z in ung:
    md.append('| %s | %s | …%s | %s | %s | %s |' % (kurz(z['abschnitt']), z['absatz'], z['links'][-35:].replace('|', '/'), z['zahl'], z['klasse'], z['quelle']))
md.append('')
md.append('## 2a Altes Blatt (22.09.) gegen neues Blatt (25.09.) in den vom Master genutzten Zeilen')
md.append('')
md.append('Die Zeilen des alten Blatts, aus denen der Master seine Zahlen bezog, verglichen mit den entsprechenden Zeilen des neuen Blatts. „n“ in Tab. 1 wird nicht verglichen, weil die Definition wechselt (alt: Spieler mit Bestwert, neu: TE-Menge mit mindestens zwei gültigen Versuchen, O5).')
md.append('')
md.append('| Zeile | Ergebnis | Grund |')
md.append('|---|---|---|')
for v in vergleich:
    md.append('| %s | %s | %s |' % v)
md.append('')
md.append('## 3 Satzprüfungen der Ergebniszahlen')
md.append('')
md.append('| Nr. | Prüfung | Master | Kennzahlenblatt | Ergebnis |')
md.append('|---|---|---|---|---|')
for e in sp:
    md.append('| %s | %s | %s | %s | %s |' % (e[0], e[1], e[2].replace('|', '/'), e[3].replace('|', '/'), 'stimmt' if e[4] else '**Abweichung**'))
md.append('')
md.append('Ergebnis: %d Satzprüfungen, %d stimmen, %d Abweichungen. Die Abweichungen werden in Teil 5 mit Neufassung vorgeschlagen.' % (len(sp), sum(1 for e in sp if e[4]), sum(1 for e in sp if not e[4])))
md.append('')
md.append('## 4 Formale Befunde in Kapitel 4 (F14 § 10)')
md.append('')
md.append('Semikola und nummerierte Abschnittsverweise werden abschnittsweise mit der Textrevision umgebaut (Maßnahmen G18, G19). Sätze über 40 Wörter verletzen die Obergrenze des Stilprofils. Marker [BELEGT], [EXTRAPOLATION] und [FÜR SCHWAB] werden im Endtext entfernt.')
md.append('')
md.append('| Abschnitt | Absatz | Semikola | Abschnittsverweise | Sätze über 40 Wörter | Marker |')
md.append('|---|---:|---:|---:|---:|---:|')
for f in formal:
    md.append('| %s | %d | %d | %d | %d | %d |' % f)
md.append('| **Summe** | | **%d** | **%d** | **%d** | **%d** |' % (sum(f[2] for f in formal), sum(f[3] for f in formal), sum(f[4] for f in formal), sum(f[5] for f in formal)))
md.append('')
md.append('Wortprüfung im ganzen Master: ' + ' · '.join('%s %d' % (n, len(verbot_fund[n])) for n in verbot) + '.')
md.append('')
if BEFUNDE:
    md.append('## 4a Bestätigte Stellen')
    md.append('')
    for b in BEFUNDE:
        md.append('- ' + b)
    md.append('')
md.append('## 5 Vorschlagsliste (Prozessregel F14 § 1.2, zur Begutachtung)')
md.append('')
if not VORSCHLAEGE:
    md.append('Keine Vorschläge. Alle Satzprüfungen stimmen mit dem Kennzahlenblatt und den Objekten überein, die Wortprüfung meldet keine entfallenen Größen mehr (SPSS, MDC, TE/√n, leistungsunabhängig).')
    md.append('')
for i, (fund, bef, neu, grund) in enumerate(VORSCHLAEGE, 1):
    md.append('**%d. %s**  ' % (i, fund))
    md.append('Befund: %s  ' % bef)
    md.append('Neufassung: %s  ' % neu)
    md.append('Begründung: %s' % grund)
    md.append('')
md.append('## 6 Was dieser Abgleich nicht leistet')
md.append('')
md.append('Die Zuordnung der Zahlen in 4.5.1 zu den Programmkennzahlen (P-01 bis P-12) ist geprüft, die Zahlen zu Vereinsprogrammen in 4.5.2 stammen aus den Sommerplänen der Vereine (Anhang D) und haben keine Kennung. Literatur- und Protokollangaben (Ferguson et al., Microgate, Altmann et al., Lloyd et al.) sind nicht Gegenstand des Kennzahlenblatts, sie werden mit der Quellenverifikation geprüft (F14 § 7). Kapitel 4.7, 5, 6 und 7 werden mit dem Berichtsraster geschrieben und nach jedem Textstand mit diesem Skript gegen das Kennzahlenblatt geprüft. Der Abgleich ist nach jedem Textstand erneut zu laufen, zuletzt vor der Abgabe (Phase 8).')
md.append('')
mdtext = '\n'.join(md)
if SEMI in mdtext.replace('(Schulz et al., 2010' + SEMI, '').replace('(Nimphius et al., 2016' + SEMI, ''):
    # Semikolon nur zulässig als Zitiersyntax in zitierten Masterstellen, alle anderen Stellen melden
    stellen = [ln for ln in mdtext.split('\n') if SEMI in ln]
    log('Hinweis: Semikolon im Protokoll in %d Zeilen, nur aus zitiertem Mastertext zulässig' % len(stellen))
    for ln in stellen:
        log('   ' + ln[:160])
with open(os.path.join(AUS, 'Abgleichprotokoll_Manuskript_2026-09-25.md'), 'w', encoding='utf-8') as f:
    f.write(mdtext + '\n')
log('')
log('Vorschläge:', len(VORSCHLAEGE), '· bestätigte Stellen:', len(BEFUNDE))
log('Dateien:', ', '.join(sorted(os.listdir(AUS))))
with open(os.path.join(AUS, 'Endabgleich_Manuskript_2026-09-25.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(LAUF) + '\n')
print('Laufprotokoll geschrieben, Zahlen', len(zahlen), 'Satzprüfungen', len(sp), 'Abweichungen', sum(1 for e in sp if not e[4]), 'Vorschläge', len(VORSCHLAEGE))

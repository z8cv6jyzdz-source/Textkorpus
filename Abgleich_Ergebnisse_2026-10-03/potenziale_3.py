#!/usr/bin/env python3
"""Schritt 3 des Tasks „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“.

Potenziale für Kapitel 5 mit Wortbilanz, Kürzungspaaren, Folgen für 6.1 und weitere Teile,
Grundlagen am Wortlaut ihrer Fundstelle und Prüfung jeder neuen Zahl am Kennzahlenblatt.
Dazu das Klickergebnis vom 03.10.2026 (FREIGABE) mit Bilanz, Schrittfolge für Schritt 4,
Satznummern-Konkordanz alt zu neu und den Bezügen anderer Teile mit neuer Kennung (Protokoll § 6).

Aufruf:  python3 potenziale_3.py [<Claude-Ordner> <Master.docx> <Ausgabeordner>]
Ohne Argumente liest das Skript relativ zu seinem Ordner (03_Skripte/Abgleich_Ergebnisse_2026-10-03).

Bauart: Jede Behauptung über eine Fundstelle ist ein Zitat, das am genannten Ort an Wortgrenzen
stehen muss. Jede Zahl der neuen Sätze muss deklariert sein und zum Kennzahlenblatt passen.
Weicht etwas ab, bricht das Skript ab. Kein Semikolon im Quelltext und in den Ausgaben.
"""
import csv
import hashlib
import io
import json
import os
import re
import statistics
import sys
import zipfile
import xml.etree.ElementTree as ET

HIER = os.path.dirname(os.path.abspath(__file__))
CLAUDE = sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(HIER, '..', '..'))
MASTER = sys.argv[2] if len(sys.argv) > 2 else os.path.normpath(
    os.path.join(CLAUDE, '..', 'Schreiben', 'Bachelorarbeit_Gerüst_v1_AKTUELL.docx'))
AUS = sys.argv[3] if len(sys.argv) > 3 else HIER
SEMI = chr(59)
BUDGET = 450

QUELLEN = {
    'textstand': '03_Skripte/Abgleich_Ergebnisse_2026-10-03/textstand.json',
    'bezuege': '03_Skripte/Abgleich_Ergebnisse_2026-10-03/bezuege_2e.md',
    'abgleich': '02_Befunde/Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md',
    'befund': '02_Befunde/Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md',
    'werte': '02_Befunde/Kennzahlen_2026-09-25_Werte.csv',
    'f17': '00_Steuerung/Projektanweisungen_Fassung17.md',
    'stilprofil': '01_Verfahren/Stilprofil_2026-09-13.md',
    'raster': '02_Befunde/Berichtsraster_2026-09-23.md',
    'tv5': '04_Uebergaben/Textvorschlag_5_2026-09-30.md',
    'tab1': '03_Skripte/Objekte_2026-10-01/Tab_1_Messguete.csv',
    'tabh1a': '03_Skripte/Objekte_2026-10-01/Tab_H1a_Versuche.csv',
    'tabh4c': '03_Skripte/Objekte_2026-10-01/Tab_H4c_Varianten.csv',
    's4b': '03_Skripte/Diskussion_Anwendung_2026-10-03/S4b_Geruest_12b.md',
    's4c': '03_Skripte/Diskussion_Anwendung_2026-10-03/S4c_Saetze.csv',
}

PROTOKOLL = []


def log(*teile):
    PROTOKOLL.append(' '.join(str(t) for t in teile))


def fehler(text):
    raise SystemExit('ABBRUCH: ' + text)


def md5(pfad):
    with open(pfad, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def lies(schluessel):
    pfad = os.path.join(CLAUDE, QUELLEN[schluessel])
    if not os.path.exists(pfad):
        fehler('Eingang fehlt: ' + pfad)
    with open(pfad, encoding='utf-8-sig') as f:
        return f.read()


# ---------------------------------------------------------------- Messung wie Messskript Fassung 4

def saetze(text):
    """Satzteilung mit Schutz der Abkürzungen und Dezimalzahlen (unverändert aus dem Messskript)."""
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', text)
    t = re.sub(r'\b(et al|Abschn|Tab|Abb|vgl|bzw|ca|Nr|Aufl|Hrsg|Jg)\.', r'\1<P>', t)
    t = re.sub(r'\b([A-Z])\.\s', r'\1<P> ', t)
    t = re.sub(r'\bS\.\s', 'S<P> ', t)
    t = re.sub(r'\b(u|z|d)\.\s?(a|B|h)\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})', r'\1<P>\2<P>\3', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d)\.\s', r'\1<P> ', t)
    teile = [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(⟨])', t) if s.strip()]
    return [s.replace('<P>', '.') for s in teile]


def woerter(text):
    return len(text.split())


def enthaelt(text, zitat):
    """Zitat an Wortgrenzen im Text (Leerraum vereinheitlicht)."""
    t = ' '.join(text.split())
    z = ' '.join(zitat.split())
    muster = r'(?<![\wÄÖÜäöüß])' + re.escape(z) + r'(?![\wÄÖÜäöüß])'
    return re.search(muster, t) is not None


# ---------------------------------------------------------------- Eingänge

TEXTSTAND = json.loads(lies('textstand'))
KAP5 = {}
ABSATZFOLGE = []
for a in TEXTSTAND['absaetze']:
    ABSATZFOLGE.append(a['kennung'])
    for s in a['saetze']:
        KAP5[s['id']] = s['text']
if sum(woerter(t) for t in KAP5.values()) != BUDGET or len(KAP5) != 29:
    fehler('Textstand nicht bei 450 Wörtern und 29 Sätzen')

ABGLEICH = lies('abgleich')
BEFUND = lies('befund')
F17 = lies('f17')
STIL = lies('stilprofil')
RASTER = lies('raster')
TV5 = lies('tv5')
S4B = lies('s4b')
BEZUEGE = lies('bezuege')

WERTE = {}
for z in csv.DictReader(io.StringIO(lies('werte'))):
    WERTE[z['k_kennung']] = z

S4C = {}
for z in csv.DictReader(io.StringIO(lies('s4c')), delimiter=SEMI):
    S4C['TV62 ' + z['satz_id'].replace('.', ' ')] = z['text']


def tabelle(schluessel):
    zeilen = list(csv.reader(io.StringIO(lies(schluessel))))
    return zeilen[0], zeilen[1:]


def zahl(text):
    t = text.replace('−', '-').replace('–', '').replace('+', '').replace(',', '.').strip()
    return float(t) if t else None


def master_absaetze(pfad):
    with zipfile.ZipFile(pfad) as z:
        namen = z.namelist()
        if 'word/comments.xml' in namen:
            fehler('Master trägt comments.xml')
        xml = z.read('word/document.xml')
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    wurzel = ET.fromstring(xml)
    absaetze = []
    for p in wurzel.iter(w + 'p'):
        absaetze.append(''.join(t.text or '' for t in p.iter(w + 't')))
    return absaetze


MASTER_ABS = master_absaetze(MASTER)
MASTER_MD5 = md5(MASTER)


def abschnitt(titel, ende):
    """Sätze eines Abschnitts im Master mit Kennung A1 S1 …, Absätze bis zur nächsten Überschrift."""
    treffer = [k for k, t in enumerate(MASTER_ABS) if t.strip() == titel]
    if not treffer:
        fehler('Überschrift fehlt im Master: ' + titel)
    i = treffer[-1]
    ergebnis = {}
    nr = 0
    for t in MASTER_ABS[i + 1:]:
        if t.strip().startswith(ende):
            break
        if not t.strip():
            continue
        nr += 1
        for k, s in enumerate(saetze(t.strip()), 1):
            ergebnis['A%d S%d' % (nr, k)] = s
    return ergebnis


SATZ61 = {'6.1 ' + k: v for k, v in abschnitt('6.1 Einordnung der Ergebnisse', '6.2').items()}
if len(SATZ61) != 40:
    fehler('6.1 nicht mit 40 Sätzen im Master: %d' % len(SATZ61))
KAP5_MASTER = abschnitt('5 Ergebnisse', '6 Diskussion')
for k, v in KAP5.items():
    if KAP5_MASTER.get(k) != v:
        fehler('Kapitel 5 im Master weicht vom Textstand ab: ' + k)
SATZ44 = {'4.4 ' + k: v for k, v in abschnitt('4.4 Leistungsdiagnostik', '4.4.1').items()}
SATZ46 = {'4.6 ' + k: v for k, v in abschnitt('4.6 Adhärenz- und Belastungsmonitoring', '4.7').items()}
SATZ47 = {'4.7 ' + k: v for k, v in abschnitt('4.7 Statistische Auswertung', '5 Ergebnisse').items()}

ORTE = {}
ORTE.update({k: v for k, v in KAP5.items()})
ORTE.update(SATZ61)
ORTE.update(SATZ44)
ORTE.update(SATZ46)
ORTE.update(SATZ47)
ORTE.update(S4C)


def zeile_abgleich(nr):
    for z in ABGLEICH.split('\n'):
        if z.startswith('| ' + nr + ' |'):
            return z
    fehler('Zeile fehlt im Abgleichbefund: ' + nr)


def ort_text(ort):
    if re.match(r'^2[a-e]\.\d+$', ort):
        return zeile_abgleich(ort)
    if ort in ORTE:
        return ORTE[ort]
    if ort.startswith('K-'):
        z = WERTE.get(ort)
        if z is None:
            fehler('Kennung fehlt: ' + ort)
        return ' '.join(z.values())
    if ort.startswith('S4b '):
        punkt = ort.split(' ', 1)[1]
        for z in S4B.split('\n'):
            if z.startswith('| ' + punkt + ' |'):
                return z
        fehler('Punkt fehlt im S4b-Gerüst: ' + punkt)
    quelle = {'F17': F17, 'Befund': BEFUND, 'Stilprofil': STIL, 'Raster': RASTER, 'TV5': TV5,
              'Abgleich': ABGLEICH, 'Bezuege': BEZUEGE}
    if ort in quelle:
        return quelle[ort]
    fehler('Unbekannter Ort: ' + ort)


def pruefe_zitat(ort, zitat, wofuer):
    if not enthaelt(ort_text(ort), zitat):
        fehler('Zitat nicht am Ort (%s): %s | %s' % (wofuer, ort, zitat))
    ZITATE.append((wofuer, ort, zitat))


ZITATE = []

# ---------------------------------------------------------------- Zahlen

ZAHLWORT = {'einer': 1, 'eins': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5, 'sechs': 6,
            'sieben': 7, 'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12}


def zahlen_im_satz(text):
    t = text
    for muster in [r'\b\d+-m-\w*', r'\b\d+- und \d+-m-\w*', r'\b505-[\wÄÖÜäöü-]+', r'CR-10[\w-]*',
                   r'Tab\. H?\d[a-e]?', r'Abb\. H?\d', r'95-%-\w+', r'\b\d+-m\b']:
        t = re.sub(muster, ' ', t)
    gefunden = []
    for m in re.finditer(r'(?<![\w,])(\d+(?:,\d+)?)(?!\w|,\d)|(?<![\wÄÖÜäöüß])([A-Za-zÄÖÜäöüß]+)(?![\wÄÖÜäöüß])', t):
        if m.group(1):
            gefunden.append((m.group(1), float(m.group(1).replace(',', '.'))))
        elif m.group(2).lower() in ZAHLWORT:
            gefunden.append((m.group(2), float(ZAHLWORT[m.group(2).lower()])))
    return gefunden


def rohwerte(kennung):
    return [float(x) for x in WERTE[kennung]['rohwerte'].split()]


def pruefe_zahlen(eintrag):
    """Jede Zahl der neuen Sätze ist deklariert (Kennung, Position in den Rohwerten oder Konstante)."""
    erwartet = eintrag.get('zahlen', [])
    gefunden = []
    for s in eintrag['neu']:
        gefunden += zahlen_im_satz(s)
    if [g[0] for g in gefunden] != [e[0] for e in erwartet]:
        fehler('Zahlen in %s: gefunden %s, deklariert %s' % (eintrag['nr'], [g[0] for g in gefunden],
                                                             [e[0] for e in erwartet]))
    for (tok, wert), (tok2, kennung, pos) in zip(gefunden, erwartet):
        if kennung.startswith('K-'):
            soll = rohwerte(kennung)[pos]
            stellen = len(tok.split(',')[1]) if ',' in tok else 0
            if round(soll, stellen) != wert:
                fehler('Zahl %s in %s passt nicht zu %s (%s)' % (tok, eintrag['nr'], kennung, soll))
        elif kennung == 'Konstante':
            if not enthaelt(TV5, 'Deckel der Zählweise WOCAP'):
                fehler('Konstante ohne Beleg in TV5: ' + tok)
        elif kennung == 'Bezeichnung':
            if not enthaelt(WERTE[pos]['bezeichnung'], tok2_bez(tok)):
                fehler('Schwelle %s nicht in der Bezeichnung von %s' % (tok, pos))
        else:
            fehler('Zahl ohne Kennung: ' + tok)
    return [(g[0], e[1], e[2]) for g, e in zip(gefunden, erwartet)]


def tok2_bez(tok):
    return '≥ %d' % ZAHLWORT.get(tok.lower(), 0) if tok.lower() in ZAHLWORT else '≥ ' + tok


# ---------------------------------------------------------------- Potenziale und Kürzungen

POTENZIALE = [
    {
        'nr': '1', 'prio': 'A', 'kurz': 'Schmerzmeldungen mit Bezugsmenge und Status',
        'art': 'ersetze', 'satz': 'A3 S3',
        'neu': ['Zwölf Meldungen von neun der 15 meldenden Spieler nannten Schmerzen oder Probleme.',
                'Acht davon betrafen als vollständig gemeldete Einheiten, je zwei teilweise und nicht durchgeführte.'],
        'zahlen': [('Zwölf', 'K-10.12', 0), ('neun', 'K-10.12', 4), ('15', 'K-10.9', 0),
                   ('Acht', 'K-10.12', 1), ('zwei', 'K-10.12', 2)],
        'paar': ['b', 'c'], 'empfehlung': True,
        'grundlage': [('F17', 'Jede Zahl im Text nennt ihre Bezugsmenge.'),
                      ('2b.45', 'nennt die Menge der Spieler nicht'),
                      ('2e.11', 'Bezugsmenge und Status „ganz“ nur über Tab. H2 und Rechnung'),
                      ('K-10.12', 'T · 5.1 unerwünschte Ereignisse (CONSORT 19)'),
                      ('K-10.9', 'Spieler mit mindestens einer Meldung (gleich welchen Status)')],
        'korpus': 'Schäden im Kern 0 von 10, erweitert 2 von 6, dort als Grund von Ausfällen',
        'korpus_belege': [('Befund', 'Schäden | 0 | 0 | 0 % | Krankheit als Grund verpasster Einheiten (Klusemann, erweitert) | 2')],
        'folge': [('6.1 A6 S2', 'Mehr als die Hälfte der Spieler mit Meldungen',
                   'im Text getragen (9 von 15, 8 von 12), „vollständig durchgeführten“ bleibt Folgeänderung (2e.11)'),
                  ('6.1 A6 S3', 'Einige betrafen teilweise oder nicht durchgeführte Einheiten', 'unberührt'),
                  ('TV62 A1 S6', 'unerwünschte Ereignisse je Einheit', 'unberührt'),
                  ('K-10.9', 'A · Tab. H2 Anmerkung', 'Berichtsort beim nächsten Erzeugerlauf auf Text')],
        'konflikt': 'keiner',
    },
    {
        'nr': '2', 'prio': 'A', 'kurz': 'Menge im Quantor des Nullbefunds',
        'art': 'ersetze', 'satz': 'A5 S6',
        'neu': ['Bei keiner konfirmatorischen Zielgröße war damit ein Gruppenunterschied nachweisbar.'],
        'zahlen': [], 'paar': ['a'], 'empfehlung': True,
        'grundlage': [('2b.11', 'Codierer B las ihn nach dem Wortlaut zunächst über alle Zielgrößen'),
                      ('2d.21', 'über einen Teil nur aus dem Zusammenhang 0')],
        'korpus': 'Kern-Quantor über einen Teil der Tests nennt die Menge in der Nominalphrase 8 von 8',
        'korpus_belege': [('2d.21', 'über einen Teil mit der Menge in der Nominalphrase 8')],
        'folge': [('6.1 A1 S2', 'war bei keiner Zielgröße ein Gruppenunterschied nachweisbar',
                   'derselbe Quantor, Folgeänderung beim Abschluss möglich (+1 in 6.1)'),
                  ('TV62 A2 S3', 'Der Nullbefund beschreibt damit das Auflösungsvermögen der Studie', 'unberührt')],
        'konflikt': 'keiner',
    },
    {
        'nr': '3', 'prio': 'B', 'kurz': 'Feste Folge der Zielgrößen in A4 S2',
        'art': 'ersetze', 'satz': 'A4 S2',
        'neu': ['Mehr gültige Versuche je Spieler hatte im Mittel beim 30-m-Sprint die Interventionsgruppe, '
                'beim 505-Test je Seite überwiegend die Kontrollgruppe, beim Standweitsprung die Interventionsgruppe (Tab. H1).'],
        'zahlen': [], 'paar': [], 'empfehlung': True,
        'grundlage': [('F17', 'Sprint → Richtungswechsel → Sprung in den Hypothesen, den Ergebnissen und der Diskussion identisch.'),
                      ('2e.19', 'A4 S2 gegen den Wortlaut von F17 § 5.1, Schwere B, keine Entscheidung')],
        'korpus': 'Kern: Folge in einem Satz wie die erste Aufzählung der Studie 7 von 8, nach dem Inhalt einmal (Negra 2019 2.3)',
        'korpus_belege': [('2d.19', 'folgen 7 der übrigen 8 derselben Folge, abweichend Negra 2019 2.3')],
        'folge': [('TV62 A5 S5', 'beim 30-m-Sprint und Standweitsprung um bis zu ein Viertel des SESOI, beim 505-Test je Seite',
                   'gruppiert ebenso nach dem Inhalt, Hinweis an den parallelen Task'),
                  ('S4b G5a', 'Richtung je Zielgröße steht in Kapitel 5, hier nur die Folge', 'trägt weiter')],
        'konflikt': 'keiner',
        'hinweis': '„zu beiden Zeitpunkten“ steht danach nur in Tab. H1',
    },
    {
        'nr': '4', 'prio': 'B', 'kurz': 'Deskriptive Zielgrößen vor die Befunde',
        'art': 'verschiebe', 'satz': 'A5 S11', 'nach': 'A5 S2',
        'neu': [], 'zahlen': [], 'paar': [], 'empfehlung': True,
        'grundlage': [('2d.17', 'nach dem letzten Befund: keine'),
                      ('2b.31', 'für die Stellung von Abb. 2 und A5 S11 steht nur die Folge der Zug-Tabelle')],
        'korpus': 'Analyseregeln in 7 Sätzen: vorn 4, im Befundteil 3, nach dem letzten Befund 0',
        'korpus_belege': [('2d.17', 'V2 primär oder sekundär in 7 Sätzen')],
        'folge': [('A5 S10', 'Die Nullhypothese wurde nicht verworfen.', 'schließt dann den Gruppenvergleich')],
        'konflikt': 'nimmt die Stellung aus Textvorschlag 5 (2b.31) mit neuem Grund zurück (2d.17)',
    },
    {
        'nr': '5', 'prio': 'B', 'kurz': 'Bezugsfolge der Untergrenzen in den Satz',
        'art': 'ersetze', 'satz': 'A2 S4',
        'neu': ['Als Untergrenzen für sechs und neun Einheiten ergaben sich mit höchstens zwei Meldungen je '
                'Programmwoche neun und zwei Spieler, nach verschiedenen Einheitennummern neun und einer.'],
        'zahlen': [('sechs', 'Bezeichnung', 'K-10.10'), ('neun', 'Bezeichnung', 'K-10.10'),
                   ('zwei', 'Konstante', 'Deckel der Zählweise WOCAP (Spezifikation S07, TV5 § 5)'),
                   ('neun', 'K-10.11', 0), ('zwei', 'K-10.11', 1),
                   ('neun', 'K-10.11', 2), ('einer', 'K-10.11', 3)],
        'paar': ['d'], 'empfehlung': False,
        'grundlage': [('2d.8', 'Bezugsfolge im vorigen Satz: 0'), ('2b.34', 'Parallele Werte ohne Zuordnungswort in A2 S4')],
        'korpus': 'Bezugsfolge im vorigen Satz 0, im selben Satz einmal (Aloui 5.1), Bezeichnung je Wert 19 Sätze in 5 Studien',
        'korpus_belege': [('2d.8', 'Bezeichnung je Wert 19 Sätze in 5 Studien'),
                          ('2d.8', 'Folge ohne Zuordnungswort mit Bezugsfolge im selben Satz 1 (Aloui 5.1)')],
        'folge': [('TV62 A6 S4', 'Die Umsetzung ist deshalb auch mit Untergrenzen berichtet.', 'unberührt')],
        'konflikt': 'keiner',
    },
    {
        'nr': '6', 'prio': 'C', 'kurz': 'Mediane Adhärenz als eigener Satz',
        'art': 'ersetze_folge', 'satz': 'A2 S1',
        'neu': ['Die 18 zugeteilten Spieler der Interventionsgruppe meldeten 92 Einheiten als vollständig, '
                '6 als teilweise und 13 als nicht durchgeführt (Tab. H2).'],
        'zusatz': ('A2 S2', ['Die mediane Adhärenz betrug 6,0 Einheiten.']),
        'zahlen': [('18', 'K-10.4', 0), ('92', 'K-10.3', 0), ('6', 'K-10.3', 1), ('13', 'K-10.3', 2),
                   ('6,0', 'K-10.8', 0)],
        'paar': [], 'empfehlung': True,
        'grundlage': [('4.6 A2 S1', 'Adhärenz ist die Zahl der Meldungen mit dem Status „ganz“ je Spieler bei zwölf angebotenen Einheiten.'),
                      ('4.7 A1 S3', 'ab einer Adhärenz von sechs Einheiten'),
                      ('2e.20', 'Begriffsbrücke Adhärenz offen, Register 10u'),
                      ('2b.47', 'A2 S1 (Median je Spieler nach dem Komma, eine andere Größe)')],
        'korpus': 'kein „adherence“ für einen Wert je Spieler, am nächsten „out of a possible“ (Rogers, erweitert)',
        'korpus_belege': [('2d.20', 'Der Korpus kennt kein „adherence“ als Bezeichnung eines Werts je Spieler.')],
        'folge': [('6.1 A2 S2', 'Die zugeteilten Spieler meldeten weniger als die Hälfte der angebotenen Einheiten als vollständig', 'unberührt'),
                  ('TV62 A1 S6', 'die Umsetzung je Spieler', 'unberührt')],
        'konflikt': 'keiner, Erstverweis auf Tab. H2 bleibt am ersten Satz',
    },
]

KUERZUNGEN = [
    {'nr': 'a', 'satz': 'A4 S1', 'kurz': '„Der TE“ statt „Der typische Messfehler“',
     'neu': ['Der TE überstieg auch bei der Abschlusstestung in allen Zielgrößen den SESOI (Tab. 1).'],
     'zahlen': [], 'grund': [('4.4 A3 S1', 'den typischen Messfehler (TE)'), ('4.4 A3 S2', 'Der TE überstieg bei allen Zielgrößen den SESOI')],
     'folge': [('TV62 A5 S1', 'Viertens wurde der typische Messfehler nur innerhalb einer Sitzung bestimmt', 'unberührt')]},
    {'nr': 'b', 'satz': 'A5 S11', 'kurz': '„Die übrigen Zielgrößen …“ statt der Namen',
     'neu': ['Die übrigen Zielgrößen wurden nur beschrieben (Tab. H3).'],
     'zahlen': [], 'grund': [('4.7 A1 S5', 'Beschreibend berichtet werden die 505-Seitenwerte laut Studienprotokoll sowie alle Teilmengen unter acht Spielern je Gruppe, so die 5- und 10-m-Sprintzeiten'),
                             ('Raster', 'Ohne p und ohne Effektstärke, Grund in 4.7')],
     'folge': []},
    {'nr': 'c', 'satz': 'A3 S1', 'kurz': '„Die CR-10-Werte … lagen bei …“',
     'neu': ['Die CR-10-Werte der 92 als vollständig gemeldeten Einheiten lagen bei 2,9 ± 0,9 (Median 3,0, Spanne 0,0 bis 5,0).'],
     'zahlen': [('92', 'K-10.13', 0), ('2,9', 'K-10.13', 1), ('0,9', 'K-10.13', 2), ('3,0', 'K-10.13', 3),
                ('0,0', 'K-10.13', 4), ('5,0', 'K-10.13', 5)],
     'grund': [('Befund', 'The average RPE was 5.5 ± 0.99 and 5.50 ± 1'), ('4.6 A1 S8', 'Der sRPE-Load ist das Produkt aus CR-10-Wert und Solldauer der Einheit.')],
     'folge': [('6.1 A6 S1', 'Die als vollständig gemeldeten Einheiten wurden im Mittel als leicht bis mäßig anstrengend empfunden.', 'unberührt')]},
    {'nr': 'd', 'satz': 'A6 S4', 'kurz': 'ohne „und keine davon erreichte p < 0,05“',
     'neu': ['Soweit die Fallzahl eine Inferenz zuließ, änderten weder der beobachtende Per-Protokoll-Vergleich '
             'noch die sechs Sensitivitätsanalysen die Einordnung als unschlüssig (Tab. H4).'],
     'zahlen': [('sechs', 'K-08', None)], 'grund': [('TV5', 'kleinster p 0,372')],
     'folge': [('6.1 A2 S5', 'änderte die Einordnung nicht', 'unberührt')]},
]

BELASSEN = [
    ('A5 S3 vor dem Modellergebnis', [('2d.12', 'K4 ordnet Modellergebnis und Einzelgruppen, nicht unadjustiert und adjustiert.'),
                                      ('2d.13', 'Das einzige Vorbild stellt beide Schätzer in denselben Satz, den unadjustierten zuerst'),
                                      ('A5 S6', 'Bei keiner Zielgröße war damit ein Gruppenunterschied nachweisbar.'),
                                      ('F17', 'Der tragende Befund für Kapitel 5 und 6 ist der Abstand zwischen unadjustierter und adjustierter Differenz (Tab. 3, Abb. 2)')]),
    ('Fall C1 einmal für alle drei Zielgrößen', [('2d.6', 'Auch die jetzige Form, der Fall einmal für mehrere Zielgrößen (2b.9), hat Vorbilder'),
                                                ('2d.9', 'Beide Ordnungen sind im Kern belegt.')]),
    ('Absicherung nach dem Gruppenvergleich, Schluss mit A6 S4', [('2d.18', 'Die Stellung von A6 entscheiden Plan § 3 Task 11 und Textvorschlag 5 (2b.28).'),
                                                                 ('2b.28', 'R2 verlangt das Bootstrap-KI neben der verworfenen Prüfung, keine Stellung im Kapitel')]),
    ('A6 S3 sinngleich statt „geprüft und nicht verworfen“', [('2b.22', '„mit Tests“ grenzt die nur grafisch geprüfte Linearität aus')]),
    ('A6 S4 mit vorangestellter Bedingung', [('2c.29', 'Inferenz nur, soweit die Fallzahl reicht (R4)')]),
    ('Satzenden A5 S1 und A6 S2', [('2b.46', 'beide Sätze sind richtig geteilt (29 Sätze), kein Satz endet auf eine Ziffer')]),
    ('A5 S3 mit zwei Angaben an einem Verb, Klammerverweise über dem Zielwert', [('2b.47', 'A5 S3 (zweite Angabe mit „und“ an dasselbe Verb)'),
                                                                               ('2b.47', 'alle sind Objektverweise')]),
    ('Befundanteil', [('2b.1', 'P2 erklärt den Abstand also nur zum Teil, den Rest tragen Rahmen und Absicherung.')]),
]

# Punkte des S4b-Gerüsts und Sätze des Textvorschlags 6.2 und 6.3, die auf Sätzen von Kapitel 5 aufbauen
S4B_BEZUG = [
    ('S4b B3', 'ohne Wiederholung von 4.4 und Kapitel 5 (TE über SESOI)', ['A4 S1']),
    ('S4b C2', 'die Umsetzung je Spieler und in der Interventionsgruppe unerwünschte Ereignisse je Einheit', ['A2 S1', 'A3 S3']),
    ('S4b G1f', 'nicht verworfene Prüfungen belegen die Voraussetzungen nicht', ['A6 S3']),
    ('S4b G1g', 'W, p und Intervall stehen in Kapitel 5, hier die Einordnung', ['A6 S1', 'A6 S2']),
    ('S4b G2c', 'im gemeinsamen Bereich des Ausgangswerts (Tab. 2, Abb. 2)', ['A1 S3', 'A5 S2']),
    ('S4b G4a', 'TE über SESOI steht in 4.4 und Kapitel 5', ['A4 S1']),
    ('S4b G5a', 'Richtung je Zielgröße steht in Kapitel 5, hier nur die Folge', ['A4 S2']),
    ('S4b G6c', 'Untergrenzen nennt Kapitel 5', ['A2 S4']),
    ('S4b G7b', 'Sensitivitätsanalyse steht im Sammelsatz von Kapitel 5', ['A6 S4']),
]
S4C_BEZUG = [
    ('TV62 A1 S4', 'typische Messfehler je Zielgröße', ['A4 S1']),
    ('TV62 A1 S6', 'die Umsetzung je Spieler', ['A2 S1', 'A3 S3']),
    ('TV62 A2 S3', 'Der Nullbefund', ['A5 S6']),
    ('TV62 A2 S6', 'Die Voraussetzungstests entdecken bei dieser Fallzahl nur große Abweichungen.', ['A6 S3']),
    ('TV62 A2 S7', 'Nicht verworfene Prüfungen belegen die Voraussetzungen nicht.', ['A6 S3']),
    ('TV62 A2 S8', 'änderte ein Bootstrap-Intervall die Einordnung nicht', ['A6 S1', 'A6 S2']),
    ('TV62 A3 S4', '(Tab. 2, Abb. 2)', ['A1 S3', 'A5 S2']),
    ('TV62 A3 S5', 'Die adjustierte Differenz ruht damit auf wenigen Spielern', ['A5 S4']),
    ('TV62 A5 S4', 'die ungleiche Zahl gültiger Versuche', ['A4 S2']),
    ('TV62 A5 S5', 'beim 30-m-Sprint und Standweitsprung', ['A4 S2']),
    ('TV62 A6 S4', 'auch mit Untergrenzen berichtet', ['A2 S4']),
]
ABHAENGIG_2E28 = ['A1 S1', 'A2 S2', 'A2 S4', 'A3 S3', 'A3 S4', 'A4 S2', 'A5 S6', 'A5 S7', 'A5 S8',
                  'A5 S9', 'A5 S10', 'A6 S1', 'A6 S2']

# Klickergebnis des Verfassers zu Schritt 3 (03.10.2026, Potenzialseite um 21:23 vorgelegt, Klick vor 21:29 Sitzungsuhr)
FREIGABE = {
    'potenziale': ['1', '3', '4', '6'],
    'kuerzungen': ['b', 'c'],
    'nicht_freigegeben': ['2', '5'],
    'register': ['Stellung', 'Wortlaut', 'Form'],
    # Schrittfolge für Schritt 4, jedes Paar im selben Schritt
    'schritte': [('A1', [], []), ('A2', ['6'], []), ('A3 mit A5 S11', ['1'], ['b', 'c']),
                 ('A4', ['3'], []), ('A5', ['4'], []), ('A6', [], [])],
}
# Gruppen der Frage „Belassen“ und die Zeilen von BELASSEN, die sie umfassen
BELASSEN_GRUPPEN = {
    'Stellung': ['A5 S3 vor dem Modellergebnis', 'Fall C1 einmal für alle drei Zielgrößen',
                 'Absicherung nach dem Gruppenvergleich, Schluss mit A6 S4'],
    'Wortlaut': ['A6 S3 sinngleich statt „geprüft und nicht verworfen“', 'A6 S4 mit vorangestellter Bedingung'],
    'Form': ['Satzenden A5 S1 und A6 S2', 'A5 S3 mit zwei Angaben an einem Verb, Klammerverweise über dem Zielwert',
             'Befundanteil'],
}


# ---------------------------------------------------------------- Kapitel aus einer Auswahl bauen

def ausgangslage():
    return {a: [(k, KAP5[k]) for k in KAP5 if k.startswith(a + ' ')] for a in ABSATZFOLGE}


def anwenden(kap, eintrag):
    satz = eintrag['satz']
    absatz = satz.split()[0]
    liste = kap[absatz]
    pos = next((i for i, (k, _) in enumerate(liste) if k == satz), None)
    if pos is None:
        fehler('Satz nicht im Kapitel: ' + satz)
    art = eintrag.get('art', 'ersetze')
    if art in ('ersetze', 'ersetze_folge'):
        neu = [(satz + ('' if j == 0 else chr(97 + j)), t) for j, t in enumerate(eintrag['neu'])]
        liste[pos:pos + 1] = neu
        if art == 'ersetze_folge':
            nach, saetze_neu = eintrag['zusatz']
            p2 = next(i for i, (k, _) in enumerate(liste) if k == nach)
            for j, t in enumerate(saetze_neu):
                liste.insert(p2 + 1 + j, (satz + '+', t))
    elif art == 'verschiebe':
        eintrag_satz = liste.pop(pos)
        p2 = next(i for i, (k, _) in enumerate(liste) if k == eintrag['nach'])
        liste.insert(p2 + 1, eintrag_satz)
    else:
        fehler('Unbekannte Art: ' + art)


def bauen(potenziale, kuerzungen):
    kap = ausgangslage()
    for k in KUERZUNGEN:
        if k['nr'] in kuerzungen:
            anwenden(kap, dict(k, art='ersetze'))
    for p in POTENZIALE:
        if p['nr'] in potenziale:
            anwenden(kap, p)
    return kap


def messen(kap):
    absaetze = {a: ' '.join(t for _, t in s) for a, s in kap.items()}
    satzliste = []
    for a in ABSATZFOLGE:
        teile = saetze(absaetze[a])
        if len(teile) != len(kap[a]):
            fehler('Satzteilung weicht ab in ' + a)
        satzliste += teile
    laengen = [woerter(s) for s in satzliste]
    return {
        'woerter': sum(woerter(t) for t in absaetze.values()),
        'je_absatz': {a: woerter(absaetze[a]) for a in ABSATZFOLGE},
        'saetze': len(satzliste),
        'median': statistics.median(laengen),
        'max': max(laengen),
        'semikola': sum(t.count(SEMI) for t in absaetze.values()),
    }


def neue_saetze_pruefen(texte, wofuer):
    for t in texte:
        if len(saetze(t)) != 1:
            fehler('Satzteilung trennt %s: %s' % (wofuer, t))
        if woerter(t) > 32:
            fehler('Satz über 32 Wörter in ' + wofuer)
        if SEMI in t:
            fehler('Semikolon in ' + wofuer)
        if re.search(r'\b(Abschn|Abschnitt|Kapitel)\b', t):
            fehler('Abschnittsverweis in ' + wofuer)
        if re.search(r'(\d|(?<![\wÄÖÜäöüß])[A-Za-zÄÖÜäöü])\.$', t):
            fehler('Satz endet auf Ziffer oder Einzelbuchstaben in ' + wofuer)
        for wort in ['weil', 'signifikant', 'Effekt', 'Wirkung', 'Training', 'verbessert', 'Erhalt', 'ITT']:
            if re.search(r'(?<![\wÄÖÜäöüß])' + wort + r'(?![\wÄÖÜäöüß])', t):
                fehler('Wort der Verbotsliste „%s“ in %s' % (wort, wofuer))


# ---------------------------------------------------------------- Prüfungen

def main():
    os.makedirs(AUS, exist_ok=True)
    log('# Prüfprotokoll potenziale_3.py (Schritt 3)')
    log('')
    log('## 0 Eingänge')
    for s, pfad in QUELLEN.items():
        p = os.path.join(CLAUDE, pfad)
        log('- %s: %s, %d Byte, MD5 %s' % (s, pfad, os.path.getsize(p), md5(p)))
    log('- master: %d Byte, MD5 %s, ohne comments.xml, %d Absätze' % (os.path.getsize(MASTER), MASTER_MD5, len(MASTER_ABS)))
    log('- Kapitel 5 im Master zeichengleich mit textstand.json (29 Sätze, 450 Wörter), 6.1 mit 40 Sätzen')
    log('')

    # 1 Alte Sätze, neue Sätze, Zahlen
    log('## 1 Wortlaut, Zahlen, Satzregeln')
    for e in POTENZIALE + KUERZUNGEN:
        art = e.get('art', 'ersetze')
        alt = KAP5[e['satz']]
        if art in ('ersetze', 'ersetze_folge'):
            neu = e['neu'] + (e['zusatz'][1] if art == 'ersetze_folge' else [])
            neue_saetze_pruefen(neu, e['nr'])
            if e['nr'] == 'd':
                if [t for t, _ in zahlen_im_satz(neu[0]) if t != '0,05' and t.lower() != 'sechs']:
                    fehler('Kürzung d mit unerwarteter Zahl')
                kz = []
            else:
                pruefe = dict(e, neu=neu)
                kz = pruefe_zahlen(pruefe)
            d = sum(woerter(t) for t in neu) - woerter(alt)
            e['delta'] = d
            log('- %s (%s): alt %d Wörter, neu %s Wörter, Bilanz %+d, Zahlen %s' % (
                e['nr'], e['satz'], woerter(alt), ' + '.join(str(woerter(t)) for t in neu), d,
                ', '.join('%s %s' % (t, k) for t, k, _ in kz) or 'keine'))
        else:
            e['delta'] = 0
            log('- %s (%s): verschoben nach %s, Bilanz 0' % (e['nr'], e['satz'], e['nach']))
    log('')

    # 2 Grundlagen, Korpus und Folgen am Wortlaut
    for e in POTENZIALE:
        for ort, z in e['grundlage']:
            pruefe_zitat(ort, z, 'Grundlage ' + e['nr'])
        for ort, z in e['korpus_belege']:
            pruefe_zitat(ort, z, 'Korpus ' + e['nr'])
        for ort, z, _ in e['folge']:
            pruefe_zitat(ort, z, 'Folge ' + e['nr'])
    for k in KUERZUNGEN:
        for ort, z in k['grund']:
            pruefe_zitat(ort, z, 'Kürzung ' + k['nr'])
        for ort, z, _ in k['folge']:
            pruefe_zitat(ort, z, 'Folge Kürzung ' + k['nr'])
    for titel, belege in BELASSEN:
        for ort, z in belege:
            pruefe_zitat(ort, z, 'Belassen: ' + titel)
    for ort, z, saetze5 in S4B_BEZUG + S4C_BEZUG:
        pruefe_zitat(ort, z, 'Bezug auf ' + ', '.join(saetze5))
    log('## 2 Zitate am Ort: %d gefunden' % len(ZITATE))
    for w, o, z in ZITATE:
        log('- %s · %s · „%s“' % (w, o, z if len(z) < 120 else z[:117] + '…'))
    log('')

    # 3 Sachprüfungen an den Objekten
    log('## 3 Sachprüfungen')
    kopf, h1a = tabelle('tabh1a')
    kbar = {z[0]: (zahl(z[2]), zahl(z[3]), zahl(z[5]), zahl(z[6])) for z in h1a}
    for ziel in ['30-m-Sprint', 'Standweitsprung']:
        ig_pre, kg_pre, ig_post, kg_post = kbar[ziel]
        if not (ig_pre > kg_pre and ig_post > kg_post):
            fehler('Potenzial 3: IG nicht zu beiden Zeitpunkten mit mehr gültigen Versuchen bei ' + ziel)
    kg_mehr = sum(1 for ziel in ['505 links', '505 rechts'] for ig, kg in
                  [(kbar[ziel][0], kbar[ziel][1]), (kbar[ziel][2], kbar[ziel][3])] if kg > ig)
    if kg_mehr != 3:
        fehler('Potenzial 3: 505 je Seite nicht in 3 von 4 Zellen KG höher')
    log('- Potenzial 3: k̄ IG über KG bei 30-m-Sprint und Standweitsprung zu beiden Zeitpunkten, 505 je Seite KG in 3 von 4 Zellen (Tab. H1a)')
    k1, t1 = tabelle('tab1')
    sesoi = {z[0].split(' (')[0]: zahl(z[4]) for z in t1}
    k4, h4c = tabelle('tabh4c')
    mit_inferenz = 0
    for z in h4c:
        if z[0].startswith('Bootstrap'):
            continue
        if z[3] in ('–', '-'):
            continue
        mit_inferenz += 1
        m = re.search(r'\[(.+?) bis (.+?)\]', z[3])
        u, o = zahl(m.group(1)), zahl(m.group(2))
        s = sesoi[z[1].split(' (')[0]]
        if not (u < -s and o > s):
            fehler('Kürzung d: Variante nicht im Fall C1: %s %s' % (z[0], z[1]))
        if zahl(z[4]) < 0.05:
            fehler('Kürzung d: Variante mit p < 0,05')
    log('- Kürzung d: %d Varianten mit Inferenz, jedes Intervall schließt −SESOI und +SESOI ein (Fall C1), damit auch null, kein p < 0,05 (Tab. H4c, Tab. 1)' % mit_inferenz)
    w = rohwerte('K-10.12')
    if w[0] != w[1] + w[2] + w[3]:
        fehler('K-10.12 Summe der Status')
    if not (w[4] / rohwerte('K-10.9')[0] > 0.5 and w[1] / w[0] > 0.5):
        fehler('Potenzial 1 trägt 6.1 A6 S2 nicht')
    log('- Potenzial 1: 12 = 8 + 2 + 2 (K-10.12), 9 von 15 Spielern über der Hälfte, 8 von 12 Meldungen überwiegend (trägt 6.1 A6 S2)')
    log('')

    # 4 Bilanz und Schritte
    empf_p = [p['nr'] for p in POTENZIALE if p['empfehlung']]
    empf_k = sorted({k for p in POTENZIALE if p['empfehlung'] for k in p['paar']})
    varianten = [
        ('Empfehlung', empf_p, empf_k),
        ('Empfehlung mit Potenzial 5', empf_p + ['5'], empf_k + ['d']),
        ('nur Potenzial 1 mit b und c', ['1'], ['b', 'c']),
        ('nur Potenzial 2 mit a', ['2'], ['a']),
    ]
    log('## 4 Bilanz')
    ergebnis_var = {}
    for name, pp, kk in varianten:
        m = messen(bauen(pp, kk))
        if m['woerter'] > BUDGET:
            fehler('Variante über 450: ' + name)
        if m['max'] > 32 or m['semikola']:
            fehler('Satzregel verletzt in Variante ' + name)
        ergebnis_var[name] = m
        log('- %s: %d Wörter (%s), %d Sätze, Median %.1f, längster Satz %d' % (
            name, m['woerter'], ' · '.join('%s %d' % (a, m['je_absatz'][a]) for a in ABSATZFOLGE),
            m['saetze'], m['median'], m['max']))
    for p in POTENZIALE:
        paar = sum(k['delta'] for k in KUERZUNGEN if k['nr'] in p['paar'])
        if p['delta'] + paar > 0:
            fehler('Paar mit positiver Bilanz: ' + p['nr'])
    plaene = [
        ('Empfehlung', [('A1', [], []), ('A2', ['6'], []), ('A3 mit A5 S11', ['1'], ['b', 'c']),
                        ('A4 mit A5 S6', ['3', '2'], ['a']), ('A5', ['4'], []), ('A6', [], [])]),
        ('Empfehlung mit Potenzial 5', [('A1', [], []), ('A2 mit A6 S4', ['6', '5'], ['d']),
                                        ('A3 mit A5 S11', ['1'], ['b', 'c']),
                                        ('A4 mit A5 S6', ['3', '2'], ['a']), ('A5', ['4'], []), ('A6', [], [])]),
    ]
    laufend = []
    for plan, schritte in plaene:
        # Paarregel: Zusatz und Kürzung eines Paars im selben Schritt
        for name, pp, kk in schritte:
            for p in POTENZIALE:
                if p['nr'] in pp and not set(p['paar']) <= set(kk):
                    fehler('Paar über zwei Schritte verteilt: ' + p['nr'] + ' in ' + name)
            for k in kk:
                if not any(k in p['paar'] for p in POTENZIALE if p['nr'] in pp):
                    fehler('Kürzung ohne ihren Zusatz im Schritt: ' + k + ' in ' + name)
        stand_p, stand_k = [], []
        log('- Schritt 4 in der Folge der Absätze (%s), Paare je im selben Schritt:' % plan)
        for name, pp, kk in schritte:
            stand_p += pp
            stand_k += kk
            m = messen(bauen(stand_p, stand_k))
            if m['woerter'] > BUDGET:
                fehler('Zwischenstand über 450 nach ' + name + ' (' + plan + ')')
            if plan == 'Empfehlung':
                laufend.append((name, m['woerter']))
            log('  - nach %s: %d' % (name, m['woerter']))
    log('')

    # 5 Abhängigkeiten
    abh = sorted(set(ABHAENGIG_2E28) | {s for _, _, l in S4B_BEZUG + S4C_BEZUG for s in l},
                 key=lambda s: (s.split()[0], int(s.split()[1][1:])))
    neu_dazu = [s for s in abh if s not in ABHAENGIG_2E28]
    log('## 5 Abhängigkeiten der späteren Teile')
    log('- 2e.28: ' + ', '.join(ABHAENGIG_2E28))
    log('- dazu aus S4b-Gerüst und Textvorschlag 6.2 und 6.3: ' + ', '.join(neu_dazu))
    for ort, z, l in S4B_BEZUG + S4C_BEZUG:
        log('  - %s → %s' % (ort, ', '.join(l)))
    log('')

    # 6 Klickergebnis mit Bilanz, Schrittfolge und Satznummern-Konkordanz
    log('## 6 Klickergebnis (03.10.2026)')
    fp, fk = FREIGABE['potenziale'], FREIGABE['kuerzungen']
    alle_nr = {p['nr'] for p in POTENZIALE}
    if set(fp) | set(FREIGABE['nicht_freigegeben']) != alle_nr or set(fp) & set(FREIGABE['nicht_freigegeben']):
        fehler('Klickergebnis deckt nicht jedes Potenzial genau einmal')
    for p in POTENZIALE:
        if p['nr'] in fp and not set(p['paar']) <= set(fk):
            fehler('Freigabe ohne die Kürzung ihres Paars: ' + p['nr'])
    for k in fk:
        if not any(k in p['paar'] for p in POTENZIALE if p['nr'] in fp):
            fehler('Kürzung ohne freigegebenen Zusatz: ' + k)
    gruppiert = [t for g in FREIGABE['register'] for t in BELASSEN_GRUPPEN[g]]
    if sorted(gruppiert) != sorted(t for t, _ in BELASSEN) or len(set(gruppiert)) != len(gruppiert):
        fehler('Gruppen der Frage „Belassen“ decken BELASSEN nicht genau')
    kap_f = bauen(fp, fk)
    m_f = messen(kap_f)
    if m_f['woerter'] > BUDGET or m_f['max'] > 32 or m_f['semikola']:
        fehler('Freigabe verletzt Budget oder Satzregeln')
    log('- freigegeben: Potenziale %s mit den Kürzungen %s · nicht freigegeben: %s mit ihren Kürzungen %s' % (
        ', '.join(fp), ', '.join(fk), ', '.join(FREIGABE['nicht_freigegeben']),
        ', '.join(k for p in POTENZIALE if p['nr'] in FREIGABE['nicht_freigegeben'] for k in p['paar'])))
    log('- als Registerzeile festgehalten: Belassen in den Gruppen %s (%d Punkte)' % (
        ', '.join(FREIGABE['register']), len(gruppiert)))
    log('- Kapitel 5 nach der Freigabe: %d Wörter (%s), %d Sätze, Median %.1f, längster Satz %d, 0 Semikola' % (
        m_f['woerter'], ' · '.join('%s %d' % (a, m_f['je_absatz'][a]) for a in ABSATZFOLGE),
        m_f['saetze'], m_f['median'], m_f['max']))
    sp, sk = [], []
    for name, pp, kk in FREIGABE['schritte']:
        for p in POTENZIALE:
            if p['nr'] in pp and not set(p['paar']) <= set(kk):
                fehler('Paar über zwei Schritte verteilt: ' + p['nr'])
        sp += pp
        sk += kk
    if sorted(sp) != sorted(fp) or sorted(sk) != sorted(fk):
        fehler('Schrittfolge deckt die Freigabe nicht')
    laufend_f, sp, sk = [], [], []
    for name, pp, kk in FREIGABE['schritte']:
        sp += pp
        sk += kk
        w_ = messen(bauen(sp, sk))['woerter']
        if w_ > BUDGET:
            fehler('Zwischenstand der Freigabe über 450 nach ' + name)
        laufend_f.append((name, w_))
    log('- Schritt 4 mit jedem Paar im selben Schritt: ' + ' · '.join('%s %d' % s for s in laufend_f))
    # Konkordanz alt zu neu
    neu_von = {}
    konk = []
    for a in ABSATZFOLGE:
        for i, (key, text) in enumerate(kap_f[a]):
            neu_id = '%s S%d' % (a, i + 1)
            if key.endswith('+'):
                zus = next(p['zusatz'][0] for p in POTENZIALE
                           if p['satz'] == key[:-1] and p.get('art') == 'ersetze_folge')
                alt_id, art = '', 'neu, nach dem bisherigen ' + zus
            elif key not in KAP5:
                alt_id, art = key[:-1], 'neu, zweiter Teil von ' + key[:-1]
            else:
                alt_id = key
                if text != KAP5[key]:
                    art = 'geändert'
                elif neu_id != key:
                    art = 'wortgleich, umnummeriert'
                else:
                    art = 'wortgleich'
                if key == 'A5 S11':
                    art += ', verschoben'
            if alt_id and not key.endswith('+') and key in KAP5:
                neu_von.setdefault(alt_id, []).insert(0, neu_id)
            elif alt_id:
                neu_von.setdefault(alt_id, []).append(neu_id)
            konk.append((alt_id, neu_id, art, woerter(text)))
    if sorted(neu_von) != sorted(KAP5):
        fehler('Konkordanz deckt nicht jeden alten Satz')
    log('- Satznummern-Konkordanz alt zu neu (%d alte, %d neue Sätze):' % (len(KAP5), len(konk)))
    for alt_id, neu_id, art, w_ in konk:
        log('  - %s → %s · %s · %d Wörter' % (alt_id or '–', neu_id, art, w_))
    # Abhängige Sätze anderer Teile mit neuer Kennung
    bez61 = []
    for zeile in BEZUEGE.splitlines():
        spalten = [s.strip() for s in zeile.strip().strip('|').split('|')]
        # nur die Bezugstabelle mit sechs Spalten, nicht die Konkordanztabelle darunter
        if zeile.startswith('| 6.1 A') and len(spalten) == 6:
            bez61.append((spalten[0], re.findall(r'A\d S\d+', spalten[3])))
    if len(bez61) != 30:
        fehler('Bezugsliste von 6.1 nicht vollständig gelesen')

    def nachher(s5):
        n = neu_von[s5]
        geaendert = any(art.startswith('geändert') or art.startswith('neu') for a_, n_, art, _ in konk
                        if a_ == s5)
        return ' + '.join(n) + (' (Wortlaut geändert)' if geaendert else ('' if n == [s5] else ' (umnummeriert)'))

    log('- Bezüge auf Kapitel 5 mit Kennung nach der Freigabe, nur wo sich Kennung oder Wortlaut ändert:')
    for ort, liste in bez61 + [(o, l) for o, _, l in S4B_BEZUG + S4C_BEZUG] + [('2e.28', ABHAENGIG_2E28)]:
        betroffen = [s5 + ' → ' + nachher(s5) for s5 in liste if nachher(s5) != s5]
        if betroffen:
            log('  - %s: %s' % (ort, ' · '.join(betroffen)))
    log('')

    # Ausgaben
    daten = {
        'stand': 'Schritt 3 mit Klickergebnis, 03.10.2026',
        'freigabe': {'potenziale': fp, 'kuerzungen': fk, 'nicht_freigegeben': FREIGABE['nicht_freigegeben'],
                     'register': FREIGABE['register'], 'messung': m_f, 'schritte': laufend_f,
                     'konkordanz': konk},
        'master_md5': MASTER_MD5,
        'potenziale': [{k: v for k, v in p.items()} for p in POTENZIALE],
        'kuerzungen': [{k: v for k, v in k_.items()} for k_ in KUERZUNGEN],
        'belassen': [t for t, _ in BELASSEN],
        'varianten': ergebnis_var,
        'schritte': laufend,
        'abhaengigkeiten': {'2e28': ABHAENGIG_2E28, 'neu': neu_dazu},
        'zitate': len(ZITATE),
    }
    with open(os.path.join(AUS, 'potenziale_3.json'), 'w', encoding='utf-8') as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
    with open(os.path.join(AUS, 'potenziale_3.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(PROTOKOLL) + '\n')
    for name in ['potenziale_3.json', 'potenziale_3.txt']:
        with open(os.path.join(AUS, name), encoding='utf-8') as f:
            if SEMI in f.read():
                fehler('Semikolon in der Ausgabe ' + name)
    print('ohne Befund: %d Zitate, Empfehlung %d Wörter, Schritte %s' % (
        len(ZITATE), ergebnis_var['Empfehlung']['woerter'], ' · '.join('%s %d' % s for s in laufend)))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
anschluss_2e.py — Teilschritt 2 (e), 03.10.2026: Anschluss von Kapitel 5 an Kapitel 4 (4.2, 4.4, 4.6, 4.7), an 6.1
und an die übrigen Teile aus Abgleichbefund § 1.4, geprüft am Master in seinem gültigen Stand (6.1 nach Rev. 163):
gleiche Begriffe, keine wörtliche Doppelung, keine Aussage, die Kapitel 5 nicht trägt. Dazu die Punkte aus
Fortsetzungsübergabe 4 § 5 Nr. 4 (Bezugsmenge der neun Spieler, acht Meldungen zu vollständig durchgeführten
Einheiten, Folge der Fähigkeiten in 6.1, „6,0 vollständige je Spieler“ gegen 4.6, Begriffe der Schlusslogik gegen 4.7).

Eigenes Skript ohne Funktionen aus früheren Skripten. Nur die Satzteilung saetze() ist die Funktion des Messskripts
Manuskriptstand_2026-09-25.py (Fassung 4), wörtlich übernommen, weil sie die Satznummern festlegt.

Eingänge: Master (docx) und die Dateien in QUELLEN, Pfade relativ zum Claude-Ordner, MD5 in § 0 der Ausgabe.
Ausgaben: anschluss_2e.txt (Belege, Abschnitte 0 bis 10), teiltabelle_2e.csv (Trennzeichen chr(59), alle Felder in
Anführungszeichen), teiltabelle_2e.md (Tabelle für § 3.5 des Abgleichbefunds), bezuege_2e.md (Sätze von 6.1 mit Bezug
auf Kapitel 5 nach Rev. 163 und Konkordanz alt zu neu).

Handurteile stehen als Tabellen im Skript (HAND_…) und sind mit Prüfbedingungen an Text und Kennzahlen gebunden. Jede
Kandidatensuche (gemeinsame Wortfolgen, Folgen der Zielgrößen, Spielerzahlen in Kapitel 4) verlangt ein Handurteil je
Kandidat. Jedes Zitat der Teiltabelle wird am genannten Ort an Wortgrenzen gesucht, Bruchstücke mit „…“ in ihrer Folge.
Weicht etwas ab, bricht das Skript ab. Jede Satzkennung in den Spalten der Teiltabelle wird aufgelöst (ohne Präfix
heißt Kapitel 5, eine Aufzählung erbt das Präfix ihres ersten Glieds) und muss im Master stehen.

Fassung 2 (03.10.2026): Befunde der Zweitprüfung eingearbeitet (zweitpruefung_2e.md, B1 bis B5, C1 bis C14).

Aufruf: python anschluss_2e.py [<Claude-Ordner>] [<Master.docx>] [<Ausgabeordner>]
  <Claude-Ordner>  Standard: zwei Ebenen über diesem Skript
  <Master.docx>    Standard: Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx neben dem Claude-Ordner
  <Ausgabeordner>  Standard: Ordner des Skripts
Nur lesend. Ohne Semikolon im Skript (chr(59)).
"""
import sys
import os
import re
import csv
import json
import zipfile
import hashlib
from collections import OrderedDict
from xml.sax.saxutils import unescape

HIER = os.path.dirname(os.path.abspath(__file__))
CLAUDE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(HIER))
MASTER = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(CLAUDE), 'Schreiben',
                                                                'Bachelorarbeit_Gerüst_v1_AKTUELL.docx')
AUS = sys.argv[3] if len(sys.argv) > 3 else HIER
SK = chr(59)
ORDNER = ['03_Skripte', 'Abgleich_Ergebnisse_2026-10-03']

QUELLEN = OrderedDict([
    ('textstand', ORDNER + ['textstand.json']),
    ('alt', ORDNER + ['master_saetze.json']),
    ('register', ORDNER + ['register_pruefung.md']),
    ('umfang', ORDNER + ['quellen', 'Auswertungs_und_Berichtsumfang_2026-09-24.md']),
    ('abgleich', ['02_Befunde', 'Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md']),
    ('werte', ['02_Befunde', 'Kennzahlen_2026-09-25_Werte.csv']),
    ('raster', ['02_Befunde', 'Berichtsraster_2026-09-23.md']),
    ('f17', ['00_Steuerung', 'Projektanweisungen_Fassung17.md']),
    ('tv5', ['04_Uebergaben', 'Textvorschlag_5_2026-09-30.md']),
    ('tv61', ['04_Uebergaben', 'Textvorschlag_6.1_2026-10-02.md']),
    ('tv61j', ['03_Skripte', 'Textvorschlag_6.1_2026-10-02.json']),
    ('nachtrag61', ['04_Uebergaben', 'Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md']),
    ('abg61', ['02_Befunde', 'Abgleich_Diskussion_6.1_Argumentationsstruktur_2026-10-03.md']),
    ('tv47', ['04_Uebergaben', 'Textvorschlag_4.7_2026-09-26.md']),
    ('s4a', ['03_Skripte', 'Diskussion_Anwendung_2026-10-03', 'S4a_Rasterzuordnung_12b.md']),
    ('fu4', ['04_Uebergaben', 'Uebergabe_Abgleich_Ergebnisse_Fortsetzung4_2026-10-03.md']),
])


def pfad(k):
    return os.path.join(CLAUDE, *QUELLEN[k])


def lies(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def md5(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def pz(x, n=2):
    s = ('{:.' + str(n) + 'f}').format(x).replace('.', ',')
    return s.replace('-', '−')


AUSGABE = []


def aus(*t):
    AUSGABE.append(' '.join(str(x) for x in t))


def PRUEF(bed, text):
    if not bed:
        raise SystemExit('PRUEF verletzt: ' + text)


def saetze(text):
    """Satzteilung wie Manuskriptstand_2026-09-25.py Fassung 4 (unverändert seit Fassung 1)."""
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


# ================================================================ § 0 Eingänge
aus('anschluss_2e.py — Teilschritt 2 (e), Anschluss von Kapitel 5 an Kapitel 4, 6.1 und weitere Teile')
aus('')
aus('§ 0 Eingänge (Pfade relativ zum Claude-Ordner, der Master relativ zu dessen Elternordner)')
for k in QUELLEN:
    p = pfad(k)
    aus('  %-10s %s · %d Byte · MD5 %s' % (k, '/'.join(QUELLEN[k]), os.path.getsize(p), md5(p)))
aus('  %-10s %s · %d Byte · MD5 %s' % ('master', 'Schreiben/' + os.path.basename(MASTER), os.path.getsize(MASTER),
                                      md5(MASTER)))
DOK = {k: lies(pfad(k)) for k in QUELLEN if k not in ('textstand', 'alt', 'tv61j', 'werte')}
TS = json.load(open(pfad('textstand'), encoding='utf-8'))
ALT = json.load(open(pfad('alt'), encoding='utf-8'))['saetze']
TV61 = json.load(open(pfad('tv61j'), encoding='utf-8'))

# Kennzahlenblatt: Rohwerte positionsgetreu (Leerstellen für fehlende Werte)
ROH = {}
BEZ = {}
with open(pfad('werte'), encoding='utf-8', newline='') as f:
    for z in csv.DictReader(f):
        ROH[z['k_kennung']] = z['rohwerte'].split(' ')
        BEZ[z['k_kennung']] = z['bezeichnung']


def kz(kennung, i):
    w = ROH[kennung][i]
    return float(w) if w.strip() else None


# ================================================================ § 1 Textstand
zf = zipfile.ZipFile(MASTER)
XML = zf.read('word/document.xml').decode('utf-8')
KOMMENTARE = 'word/comments.xml' in zf.namelist()
P = []
for m in re.finditer(r'<w:p(?=[ >/])', XML):
    a = m.start()
    k = XML.find('>', a)
    if XML[k - 1] == '/':
        P.append(('', '', False))
        continue
    e = XML.find('</w:p>', a) + 6
    inh = XML[a:e]
    st = re.search(r'<w:pStyle w:val="([^"]+)"', inh)
    txt = unescape(''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', inh)))
    feld = 'fldChar' in inh or 'instrText' in inh or '<w:fldSimple' in inh
    P.append((st.group(1) if st else '', txt, feld))

EINL = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']
SATZ = OrderedDict()      # Satzkennung -> Satzdaten
ABSATZ = OrderedDict()    # Absatzkennung -> Text
UEBERSCHRIFT = OrderedDict()
akt = None
zaehler = {}
einl_i = 0
for st, txt, feld in P:
    if st.startswith('berschrift'):
        m = re.match(r'^(\d+(?:\.\d+)*)\s', txt.strip())
        ma = re.match(r'^(Anhang [A-H])', txt.strip())
        akt = m.group(1) if m else (ma.group(1) if ma else txt.strip())
        UEBERSCHRIFT['Überschrift ' + akt] = txt.strip()
        continue
    if st.startswith('Verzeichnis') or feld or not txt.strip() or akt is None:
        continue
    if st not in ('', 'Standard'):
        continue
    if akt == '1':
        kenn = EINL[einl_i]
        einl_i += 1
    else:
        zaehler[akt] = zaehler.get(akt, 0) + 1
        kenn = '%s A%d' % (akt, zaehler[akt])
    ABSATZ[kenn] = txt
    platz = txt.strip().startswith('⟨')
    for n, s in enumerate(saetze(txt) if not platz else [txt.strip()], 1):
        SATZ['%s S%d' % (kenn, n)] = {'abschnitt': akt, 'absatz': kenn, 'nr': n, 'text': s,
                                       'woerter': len(s.split()), 'platzhalter': platz}


def T(i):
    return SATZ[i]['text']


aus('')
aus('§ 1 Textstand')
aus('  Master %d Byte, MD5 %s, word/comments.xml %s, %d Absätze im Dokument' % (
    os.path.getsize(MASTER), md5(MASTER), 'vorhanden' if KOMMENTARE else 'nicht vorhanden', len(P)))
PRUEF(os.path.getsize(MASTER) == 40337 and md5(MASTER).startswith('6c1db455'), 'Master wie nach Rev. 163')
PRUEF(not KOMMENTARE, 'keine comments.xml')
PRUEF(len(P) == 188, '188 Absätze')
K5 = [ABSATZ['5 A%d' % i] for i in range(1, 7)]
PRUEF('5 A7' not in ABSATZ, 'Kapitel 5 hat sechs Absätze')
for i, a in enumerate(TS['absaetze']):
    PRUEF(K5[i] == a['text'], 'Kapitel 5 %s zeichengleich mit textstand.json' % a['kennung'])
K5_IDS = [i for i in SATZ if SATZ[i]['abschnitt'] == '5']
K5_W = sum(len(t.split()) for t in K5)
PRUEF(K5_W == 450 and len(K5_IDS) == 29, 'Kapitel 5 mit 450 Wörtern und 29 Sätzen')
aus('  Kapitel 5: sechs Absätze zeichengleich mit textstand.json, %d Wörter, %d Sätze' % (K5_W, len(K5_IDS)))
for i, a in enumerate(TV61['absaetze']):
    PRUEF(ABSATZ['6.1 A%d' % (i + 1)] == a['text'], '6.1 A%d zeichengleich mit der JSON (Fassung 3)' % (i + 1))
PRUEF(TV61['fassung'].startswith('3 '), 'JSON von 6.1 in Fassung 3')
W61 = sum(len(ABSATZ['6.1 A%d' % i].split()) for i in range(1, 7))
S61 = [i for i in SATZ if SATZ[i]['abschnitt'] == '6.1']
PRUEF(W61 == 700 and len(S61) == 40, '6.1 mit 700 Wörtern und 40 Sätzen')
aus('  6.1: sechs Absätze zeichengleich mit Textvorschlag_6.1_2026-10-02.json (Fassung 3), %d Wörter, %d Sätze' % (
    W61, len(S61)))


def alt_id(i):
    return re.sub(r'^(Anhang [A-H]):.* (A\d+ S\d+)$', r'\1 \2', i)


ALTD = OrderedDict((alt_id(s['id']), s['text']) for s in ALT)
NEUD = OrderedDict((i, SATZ[i]['text']) for i in SATZ)
geaendert = [i for i in ALTD if ALTD[i] != NEUD.get(i)] + [i for i in NEUD if i not in ALTD]
abs_geaendert = sorted(set(re.sub(r' S\d+$', '', i) for i in geaendert))
PRUEF(abs_geaendert == ['6.1 A3', '6.1 A4', '6.1 A5'], 'nur 6.1 A3 bis A5 geändert')
gleich = [i for i in NEUD if ALTD.get(i) == NEUD[i]]
ALTE_TEXTE = set(ALTD.values())
gleich_wortlaut = [i for i in NEUD if NEUD[i] in ALTE_TEXTE]
PRUEF(len(gleich) == 287 and len(gleich_wortlaut) == 290, '287 unter gleicher Kennung, 290 dem Wortlaut nach')
aus('  gegen master_saetze.json (Stand 03.10., 08:05): %d Sätze dort, %d hier, geändert nur die Absätze %s, '
    'gleich %d Sätze unter gleicher Kennung, %d dem Wortlaut nach' % (len(ALTD), len(NEUD), ', '.join(abs_geaendert),
                                                                        len(gleich), len(gleich_wortlaut)))
# Titel des Vorspanns und ob darunter Text steht
VORSPANN = OrderedDict()
for j, (st, txt, feld) in enumerate(P):
    if st == 'Vorspann-Titel':
        mit_text = False
        for st2, txt2, feld2 in P[j + 1:]:
            if st2 == 'Vorspann-Titel' or st2.startswith('berschrift') or st2.startswith('Verzeichnis'):
                break
            if txt2.strip():
                mit_text = True
        VORSPANN[txt.strip()] = mit_text
PRUEF(VORSPANN.get('Zusammenfassung') is False and VORSPANN.get('Abstract') is False,
      'Zusammenfassung und Abstract als Titel ohne Text')
aus('  Vorspann-Titel: %s' % ' · '.join('%s (%s)' % (k, 'mit Text' if v else 'ohne Text') for k, v in VORSPANN.items()))
N_AUSSEN = len([i for i in SATZ if SATZ[i]['abschnitt'] != '5' and not SATZ[i]['platzhalter']])

# ================================================================ § 2 Konkordanz und Bezüge
aus('')
aus('§ 2 Konkordanz 6.1 A3 bis A5 alt zu neu und Sätze anderer Teile mit Bezug auf Kapitel 5')
alt61 = OrderedDict((i, t) for i, t in ALTD.items() if re.match(r'6\.1 A[345] ', i))
neu61 = OrderedDict((i, t) for i, t in NEUD.items() if re.match(r'6\.1 A[345] ', i))
KONK = OrderedDict()
for ia, ta in alt61.items():
    treffer = [inn for inn, tn in neu61.items() if tn == ta and inn.split(' S')[0] == ia.split(' S')[0]]
    KONK[ia] = (treffer[0], 'zeichengleich') if treffer else None
# Handurteile für die nicht zeichengleichen Sätze, gebunden an den Wortlaut
HAND_KONK = OrderedDict([
    ('6.1 A3 S5', (None, 'Stufe 3 der Kürzungsleiter des Nachtrags, Satz zu Ramirez-Campillo et al., 2020',
                   lambda a, n: 'Ramirez-Campillo et al., 2020' in a)),
    ('6.1 A3 S7', ('6.1 A3 S6', 'ohne „zudem“ (P6)', lambda a, n: a.replace('zudem ', '') == n)),
    ('6.1 A4 S4', ('6.1 A4 S4', 'neu gefasst: Population im Satz, kein Rückbezug mehr',
                   lambda a, n: 'Ramirez-Campillo et al., 2023' in a and 'Ramirez-Campillo et al., 2023' in n
                   and a.startswith('Das stimmt') and 'überwiegend von Mädchen' in n)),
    ('6.1 A4 S8', ('6.1 A4 S9', 'neu gefasst: Modalverb, eigene Umsetzung als Erklärungsangebot',
                   lambda a, n: 'auch das Vergleichsprogramm kam ohne Wende aus' in a
                   and 'auch das Vergleichsprogramm kam ohne Wende aus' in n and 'eigene Umsetzung' in n)),
    ('6.1 A5 S6', ('6.1 A5 S6', 'neu gefasst: „vereinbar“ markiert, ohne „Dagegen“',
                   lambda a, n: 'Lloyd et al., 2016' in a and 'Lloyd et al., 2016' in n and a.startswith('Dagegen')
                   and 'mit dem eigenen Befund vereinbar' in n)),
])
for ia, v in KONK.items():
    if v is None:
        PRUEF(ia in HAND_KONK, 'Handurteil für %s' % ia)
        ziel, grund, bed = HAND_KONK[ia]
        PRUEF(bed(alt61[ia], neu61.get(ziel, '')), 'Prüfbedingung Konkordanz %s' % ia)
        KONK[ia] = (ziel, grund)
    else:
        PRUEF(ia not in HAND_KONK, 'kein Handurteil für zeichengleiche %s' % ia)
NEU_OHNE_VORGAENGER = [i for i in neu61 if i not in [v[0] for v in KONK.values()]]
PRUEF(NEU_OHNE_VORGAENGER == ['6.1 A4 S6'], 'einziger neuer Satz 6.1 A4 S6')
PRUEF(T('6.1 A4 S6') == 'Mit beiden ist der eigene Befund vereinbar.', 'Wortlaut 6.1 A4 S6')
for ia, (ziel, grund) in KONK.items():
    aus('  %s → %s (%s)' % (ia, ziel or 'entfällt', grund))
aus('  neu ohne Vorgänger: 6.1 A4 S6 „%s“' % T('6.1 A4 S6'))

# Bezüge der Sätze von 6.1 auf Kapitel 5 (Zuordnung von Hand, Abgleichbefund § 1.4 a nach Rev. 163). Regel: Ein Satz
# hat Bezug, wenn er einen eigenen Befund, eine Zahl oder einen Begriff aus Kapitel 5 nennt, sich ausdrücklich auf den
# eigenen Befund bezieht oder über einen Konnektor einen Vergleich mit ihm markiert (TV 6.1 § 4, Zweitprüfung B1).
BEZUG = OrderedDict([
    ('6.1 A1 S2', ('A5 S4, A5 S6, A5 S10', 'Befund, Begriffe, nahezu wörtlich', 'Text')),
    ('6.1 A1 S3', ('A5 S3', 'Befund', 'Text, Tab. 3')),
    ('6.1 A1 S4', ('A5 S3, A1 S4', 'Befund mit Deutung (in 6.1 zulässig)', 'Text, Tab. 3, Abb. 2')),
    ('6.1 A1 S5', ('A5 S7', 'Befund (Fall C1)', 'Text')),
    ('6.1 A1 S6', ('A5 S8', 'Begriff „unschlüssig“', 'Text')),
    ('6.1 A2 S2', ('A2 S1, A2 S2', 'Befund in Worten', 'Text · „einige keine einzige“ nur Tab. H2')),
    ('6.1 A2 S3', ('A2 S2', 'Vergleich über Konnektor („Auch“, Umsetzung als Kontext)', 'Text')),
    ('6.1 A2 S4', ('A2 S2, A5 S6', 'Begriffe „Umsetzung“ und „nicht nachweisbar“', 'Text')),
    ('6.1 A2 S5', ('A6 S4, A2 S3', 'Befund, Begriffe', 'Text')),
    ('6.1 A2 S6', ('A6 S4', 'Befund', 'Text · Punktschätzer und Zielgröße ohne Inferenz nur Tab. H4')),
    ('6.1 A3 S2', ('Tab. 2, Tab. 3 (A1 S3, A5 S1)', 'Zahlen in Worten', 'nur Tab. 2 und Tab. 3')),
    ('6.1 A3 S3', ('A5 S4, A5 S7', 'Befund', 'Text · „nahe null“ nicht')),
    ('6.1 A3 S5', ('A5 S4, A5 S7', 'Rückbezug (bis Rev. 162 S6)', 'Text')),
    ('6.1 A4 S2', ('Tab. 2, Tab. 3 (A1 S3, A5 S1)', 'Zahlen in Worten', 'nur Tab. 2 und Tab. 3')),
    ('6.1 A4 S3', ('A5 S5, A5 S7', 'Befund', 'Text · „nahe null“ nicht')),
    ('6.1 A4 S6', ('A5 S5, A5 S7', 'Rückbezug, Markierung „vereinbar“ (neu seit Rev. 163)', 'Text, Tab. 3')),
    ('6.1 A4 S7', ('A5 S5, Tab. 3', 'Widerspruch über Konnektor („Dagegen“, bis Rev. 162 S6)', 'nur Tab. 3 (g-Intervall)')),
    ('6.1 A4 S8', ('A5 S5', 'Widerspruch über Konnektor („Auch“, bis Rev. 162 S7)', 'Text')),
    ('6.1 A4 S9', ('A2 S2, A5 S5', 'Begriff „Umsetzung“ (neu gefasst, bis Rev. 162 S8 ohne Bezug)', 'Text')),
    ('6.1 A5 S2', ('Tab. 2, Tab. 3 (A1 S3, A5 S1)', 'Zahlen in Worten', 'nur Tab. 2 und Tab. 3')),
    ('6.1 A5 S3', ('A5 S5, A5 S7', 'Befund', 'Text')),
    ('6.1 A5 S4', ('A5 S5, A5 S6', 'Rückbezug, Markierung „widerspricht“', 'Text, Tab. 3')),
    ('6.1 A5 S5', ('A5 S5', 'Widerspruch über Konnektor („Auch“)', 'Text')),
    ('6.1 A5 S6', ('A5 S5, A5 S7', 'Rückbezug, Markierung „vereinbar“ (neu gefasst seit Rev. 163)', 'Text, Tab. 3')),
    ('6.1 A5 S8', ('Tab. 2 (A1 S3)', 'Zahlen in Worten', 'nur Tab. 2')),
    ('6.1 A6 S1', ('A3 S1', 'Befund mit Skalenanker', 'Text')),
    ('6.1 A6 S2', ('A3 S3', 'Befund in Worten', 'Text · Bezugsmenge 15 nur Tab. H2, Status „ganz“ nur rechnerisch')),
    ('6.1 A6 S3', ('A3 S3', 'Befund', 'Text')),
    ('6.1 A6 S4', ('A3 S4', 'Befund, bewusst nicht wörtlich (Register c8)', 'Text')),
    ('6.1 A6 S5', ('A3 S3, A3 S4', 'Folgerung', 'Text')),
])
PRUEF(all(i in SATZ for i in BEZUG), 'alle Bezugssätze im Master')
for i, (wo, art, deck) in BEZUG.items():
    for r in re.findall(r'A\d S\d+', wo):
        PRUEF('5 ' + r in SATZ, 'Kapitel-5-Satz %s vorhanden' % r)
PRUEF(len(BEZUG) == 30, '30 Sätze von 6.1 mit Bezug')
OHNE = [i for i in S61 if i not in BEZUG]
PRUEF(len(OHNE) == 10, '10 Sätze von 6.1 ohne Bezug')
# Prüfbedingungen am Wortlaut: Rückbezüge nennen den eigenen Befund, Konnektoren markieren den Vergleich
for i in ('6.1 A3 S5', '6.1 A4 S6', '6.1 A5 S6'):
    PRUEF('eigene' in T(i) and 'Befund' in T(i), 'Rückbezug am Wortlaut %s' % i)
PRUEF(T('6.1 A5 S4').startswith('Das widerspricht'), 'Rückbezug 6.1 A5 S4')
PRUEF('eigene Umsetzung' in T('6.1 A4 S9') and 'eigene Umsetzung' in T('6.1 A2 S4'), 'eigene Umsetzung')
PRUEF('nicht nachweisbarer Unterschied' in T('6.1 A2 S4'), '6.1 A2 S4 nimmt A5 S6 auf')
KONNEKTOR = OrderedDict([('6.1 A2 S3', 'Auch '), ('6.1 A4 S7', 'Dagegen '), ('6.1 A4 S8', 'Auch '),
                         ('6.1 A5 S5', 'Auch ')])
for i, k in KONNEKTOR.items():
    PRUEF(T(i).startswith(k), 'Konnektor am Satzanfang %s' % i)
for i in ('6.1 A4 S7', '6.1 A4 S8', '6.1 A5 S5'):
    zeile_tv = DOK['tv61'][DOK['tv61'].find('| %s |' % i.replace('6.1 ', '')):]
    zeile_tv = zeile_tv[:zeile_tv.find('\n')]
    PRUEF('Widerspruch' in zeile_tv and 'außerhalb' in zeile_tv, 'TV 6.1 § 4 markiert %s als Widerspruch' % i)
PRUEF('Literaturvergleich der Umsetzung' in DOK['tv61'], 'TV 6.1 § 4 zu A2 S3')
for i in OHNE:
    PRUEF('eigene' not in T(i) and 'unschlüssig' not in T(i) and 'Beschreibend' not in T(i)
          and not T(i).startswith(('Auch ', 'Dagegen ', 'Das ')), 'Satz ohne Bezug %s ohne Marke' % i)
for i in ('6.1 A3 S2', '6.1 A4 S2', '6.1 A5 S2'):
    PRUEF(T(i).startswith('Beschreibend'), 'Beschreibend-Satz %s' % i)
GRENZ = OrderedDict([('6.1 A3 S6', 'Erwartung aus dem Programm (4.5.1), ohne Marke'),
                     ('6.1 A5 S7', 'Zeitverlauf als Vorbehalt, ohne Marke')])
PRUEF(all(i in OHNE for i in GRENZ), 'Grenzfälle ohne Bezug')
ALT_BEZUG = ['6.1 A1 S2', '6.1 A1 S3', '6.1 A1 S4', '6.1 A1 S5', '6.1 A1 S6', '6.1 A2 S2', '6.1 A2 S4', '6.1 A2 S5',
             '6.1 A2 S6', '6.1 A3 S2', '6.1 A3 S3', '6.1 A3 S6', '6.1 A4 S2', '6.1 A4 S3', '6.1 A4 S4', '6.1 A5 S2',
             '6.1 A5 S3', '6.1 A5 S4', '6.1 A5 S8', '6.1 A6 S1', '6.1 A6 S2', '6.1 A6 S3', '6.1 A6 S4', '6.1 A6 S5']
PRUEF(len(ALT_BEZUG) == 24, 'Abgleichbefund § 1.4 a mit 24 Sätzen von 6.1')
for i in ALT_BEZUG:
    PRUEF('| %s |' % i in DOK['abgleich'], '§ 1.4 a nennt %s' % i)


def neu_nr(ia):
    if not re.match(r'6\.1 A[345] ', ia):
        return ia
    return KONK[ia][0]


alt_nachgefuehrt = [neu_nr(i) for i in ALT_BEZUG]
ENTFALLEN_ALS_BEZUG = [i for i in alt_nachgefuehrt if i not in BEZUG]
NEU_ALS_BEZUG = [i for i in BEZUG if i not in alt_nachgefuehrt]
NEU_SEIT_163 = [i for i in NEU_ALS_BEZUG if NEUD[i] not in ALTE_TEXTE]
NACH_REGEL = [i for i in NEU_ALS_BEZUG if NEUD[i] in ALTE_TEXTE]
PRUEF(ENTFALLEN_ALS_BEZUG == ['6.1 A4 S4'], 'als Bezug entfällt nur 6.1 A4 S4')
PRUEF(NEU_SEIT_163 == ['6.1 A4 S6', '6.1 A4 S9', '6.1 A5 S6'], 'neue Bezüge seit Rev. 163')
PRUEF(NACH_REGEL == ['6.1 A2 S3', '6.1 A4 S7', '6.1 A4 S8', '6.1 A5 S5'], 'nach der Regel ergänzte, unveränderte Sätze')
aus('  Regel: Bezug hat ein Satz mit eigenem Befund, Zahl oder Begriff aus Kapitel 5, mit ausdrücklichem Rückbezug auf '
    'den eigenen Befund oder mit einem Konnektor, der einen Vergleich mit ihm markiert (TV 6.1 § 4)')
aus('  Sätze von 6.1 mit Bezug: %d (§ 1.4 a: 24), ohne Bezug %d: %s' % (len(BEZUG), len(OHNE), ', '.join(OHNE)))
aus('  Grenzfälle ohne Bezug: %s' % ' · '.join('%s (%s)' % (i, g) for i, g in GRENZ.items()))
aus('  als Bezug entfällt: %s · neu seit Rev. 163: %s · nach der Regel ergänzt, Wortlaut unverändert: %s · '
    'umnummeriert: 6.1 A3 S6 → S5, A4 S6 und S7 → S7 und S8' % (
        ', '.join(ENTFALLEN_ALS_BEZUG), ', '.join(NEU_SEIT_163), ', '.join(NACH_REGEL)))
# Stellen mit alten Satznummern von 6.1: nachführen oder als Stand vor Rev. 163 stehen lassen
NACHFUEHR = OrderedDict([
    ('Abgleichbefund § 1.4 (a)', ('abgleich', '| 6.1 A3 S6 | „Der eigene Befund blieb dahinter zurück',
                                  'nachführen', 'Vermerk am Ende von § 1.4: 30 Sätze nach bezuege_2e.md')),
    ('Abgleichbefund 2b.8', ('abgleich', '6.1 A3 S7 zählt Fähigkeiten auf', 'nachführen',
                             'Vermerk in § 3.2: 6.1 A3 S7 heißt 6.1 A3 S6')),
    ('Abgleichbefund 2b.29', ('abgleich', '24 Sätze von 6.1 (Abgleichbefund § 1.4)', 'nachführen',
                              'Vermerk in § 3.2: 30 statt 24 Sätze, nur über Objekte zusätzlich 6.1 A4 S7 (Tab. 3)')),
    ('Abgleichbefund § 1.1', ('abgleich', 'Modalverben in A4 S8 und A5 S7', 'bleibt',
                              'Stand 09:05 vor Rev. 163, jetzt 6.1 A4 S9')),
    ('register_pruefung.md 6i', ('register', '„deutlich“ in 6.1 A4 S6, S7, A5 S5', 'bleibt',
                                 'Bericht von Schritt 1, Stand vor Rev. 163, jetzt 6.1 A4 S7, S8, A5 S5')),
    ('Fortsetzung 4 § 5 Nr. 4', ('fu4', 'die Satznummern von 6.1 in den folgenden Punkten gelten für den Stand davor',
                                 'bleibt', 'nennt selbst den Stand vor Rev. 163, 6.1 A3 S7 heißt jetzt 6.1 A3 S6')),
])
for wo, (dk, stelle, wie, was) in NACHFUEHR.items():
    PRUEF(stelle in DOK[dk], 'alte Satznummer an der Stelle %s' % wo)
    aus('  %s: %s (%s)' % (wie, wo, was))
for i, (wo, art, deck) in BEZUG.items():
    aus('  %s · nimmt auf %s · %s · gedeckt durch %s · „%s“' % (i, wo, art, deck, T(i)[:70] + ' …'))

# ================================================================ § 3 Anschluss 6.1 am Kennzahlenblatt
aus('')
aus('§ 3 Aussagen von 6.1 über Kapitel 5 am Kennzahlenblatt (Rohwerte aus Kennzahlen_2026-09-25_Werte.csv)')
ZG = OrderedDict([('Z30', ('30-m-Sprint', 'K-04.3', 'K-06.1', 'K-05.3', 's', 3)),
                  ('CM', ('505-Seitenmittel', 'K-04.6', 'K-06.2', 'K-05.6', 's', 3)),
                  ('SBJ', ('Standweitsprung', 'K-04.7', 'K-06.3', 'K-05.7', 'cm', 1))])
WERT = OrderedDict()
for z, (name, k4, k6, k5, einheit, nk) in ZG.items():
    prae_ig, prae_kg = kz(k4, 2), kz(k4, 6)
    post_ig, post_kg = kz(k6, 2), kz(k6, 3)
    ud, b1, p, g = kz(k6, 5), kz(k6, 9), kz(k6, 12), kz(k6, 13)
    sesoi = kz(k5, 8)
    PRUEF(abs(sesoi - kz(k6, 17)) < 1e-12, 'SESOI in %s gleich %s' % (k5, k6))
    WERT[z] = dict(name=name, prae_ig=prae_ig, prae_kg=prae_kg, post_ig=post_ig, post_kg=post_kg, ud=ud, b1=b1, p=p,
                   g=g, sesoi=sesoi, q=abs(b1) / sesoi, anteil=b1 / ud, einheit=einheit, nk=nk,
                   ki_u=kz(k6, 10), ki_o=kz(k6, 11), g_u=kz(k6, 14), g_o=kz(k6, 15))
    aus('  %s: Prä IG %s, KG %s · Post IG %s, KG %s · unadjustiert %s · adjustiert %s (p = %s) · g %s · SESOI %s · '
        '|adjustiert|/SESOI %s · adjustiert/unadjustiert %s' % (
            name, pz(prae_ig, 2 if nk == 3 else 0), pz(prae_kg, 2 if nk == 3 else 0),
            pz(post_ig, 2 if nk == 3 else 0), pz(post_kg, 2 if nk == 3 else 0), pz(ud, nk), pz(b1, nk), pz(p, 3),
            pz(g, 2), pz(sesoi, nk), pz(abs(b1) / sesoi, 2), pz(b1 / ud, 2)))
z30, cm, sbj = WERT['Z30'], WERT['CM'], WERT['SBJ']


def pzv(x, n):
    return ('+' if x > 0 else '') + pz(x, n)


# Intervalle, gegen die TV 6.1 § 4 die Vorstudien in 6.1 A4 S7, A4 S8 und A5 S5 als Widerspruch markiert
KI_CM = '%s bis %s' % (pz(cm['ki_u'], 3), pzv(cm['ki_o'], 3))
KI_SBJ = '%s bis %s' % (pz(sbj['ki_u'], 1), pzv(sbj['ki_o'], 1))
GKI_CM = '%s bis %s' % (pz(cm['g_u'], 2), pzv(cm['g_o'], 2))
PRUEF(KI_CM == '−0,085 bis +0,061' and KI_SBJ == '−8,7 bis +8,6' and GKI_CM == '−0,81 bis +0,58',
      'Intervalle K-06.2 und K-06.3')
for kenn, marke in (('A4 S8', '−0,18 s außerhalb des eigenen Intervalls ' + KI_CM),
                    ('A5 S5', '+13,1 cm außerhalb von ' + KI_SBJ + ' cm'),
                    ('A4 S7', 'g 1,01, außerhalb des eigenen Intervalls')):
    zt = DOK['tv61'][DOK['tv61'].find('| %s |' % kenn):]
    PRUEF(marke in zt[:zt.find('\n')], 'TV 6.1 § 4 zu %s mit den Intervallen des Kennzahlenblatts' % kenn)
PRUEF('K-06.2, −0,81 bis +0,58' in DOK['tv61'], 'g-Intervall 505 in TV 6.1 § 4')
aus('  Intervalle für die Markierungen in 6.1: 505-Seitenmittel %s s (g %s), Standweitsprung %s cm, wie TV 6.1 § 4' % (
    KI_CM, GKI_CM, KI_SBJ))
# Beschreibend-Sätze (6.1 A3 S2, A4 S2, A5 S2), gerundet wie Tab. 2 und Tab. 3
PRUEF(round(z30['post_ig'], 2) > round(z30['prae_ig'], 2) and round(z30['post_kg'], 2) == round(z30['prae_kg'], 2),
      '30 m: IG etwas höher, KG gleich')
PRUEF(abs(round(cm['post_ig'], 2) - round(cm['prae_ig'], 2)) <= 0.011 and round(cm['post_kg'], 2) == round(
    cm['prae_kg'], 2), '505: nahezu unverändert')
PRUEF(round(sbj['post_ig']) < round(sbj['prae_ig']) and round(sbj['post_kg']) < round(sbj['prae_kg']),
      'Standweitsprung: beide gesunken')
# Vorsprung nach der Sommerpause (6.1 A1 S3) und Anteil des adjustierten am unadjustierten Abstand (6.1 A1 S4)
PRUEF(z30['post_ig'] < z30['post_kg'] and cm['post_ig'] < cm['post_kg'] and sbj['post_ig'] > sbj['post_kg'],
      'IG in allen drei Post-Werten vorn')
PRUEF(all(w['anteil'] < 0.25 for w in WERT.values()), 'adjustiert unter einem Viertel der unadjustierten Differenz')
# „nahe null“ (6.1 A3 S3, A4 S3, A5 S3) gegen den SESOI
PRUEF(z30['q'] > 0.5 and cm['q'] > 0.5 and sbj['q'] < 0.05, 'Lage der Schätzer gegen den SESOI')
pp30, ppsbj = kz('K-08.1 Z30', 0), kz('K-08.1 SBJ', 0)
pp_n_cm = (kz('K-08.1 CM', 4), kz('K-08.1 CM', 5))
PRUEF(kz('K-08.1 CM', 0) is None and pp_n_cm == (7.0, 10.0), 'Per-Protokoll 505 ohne Schätzer (7 und 10)')
PRUEF(pp30 > 0 > z30['b1'] and ppsbj > 0 > sbj['b1'], 'Vorzeichenwechsel der Per-Protokoll-Schätzer')
pp30_q = abs(pp30) / z30['sesoi']
aus('  Per-Protokoll ≥ 6 (K-08.1): 30 m %s s (|·|/SESOI %s), Standweitsprung %s cm (|·|/SESOI %s), '
    '505-Seitenmittel ohne Schätzer (%d und %d Spieler)' % (
        pz(pp30, 3).replace('0,', '+0,', 1), pz(pp30_q, 2), pz(ppsbj, 1).replace('0,', '+0,', 1),
        pz(abs(ppsbj) / sbj['sesoi'], 2), pp_n_cm[0], pp_n_cm[1]))
# Umsetzung (6.1 A2 S2) und Schmerzmeldungen (6.1 A6 S2, S3)
rate = kz('K-10.5', 1)
null_einheiten = kz('K-10.15', 0)
ue = [kz('K-10.12', i) for i in range(5)]
mit_meldung = kz('K-10.9', 0)
zugeteilt = kz('K-10.4', 0)
PRUEF(rate < 0.5 and null_einheiten == 4, 'weniger als die Hälfte, vier Spieler ohne vollständige Einheit')
PRUEF(ue == [12.0, 8.0, 2.0, 2.0, 9.0] and mit_meldung == 15 and zugeteilt == 18, 'K-10.12, K-10.9, K-10.4')
PRUEF(ue[4] / mit_meldung > 0.5 and ue[4] / zugeteilt == 0.5, 'Hälfte gegen 15 und gegen 18')
PRUEF(ue[1] / ue[0] > 0.5 and ue[0] - ue[2] - ue[3] == ue[1], 'acht Meldungen zu „ganz“ als Rest')
cr10 = [kz('K-10.13', i) for i in range(6)]
PRUEF(round(cr10[1], 1) == 2.9 and cr10[3] == 3.0, 'CR-10 2,9, Median 3,0')
te_post_ueber = all(kz('K-05.%d' % i, 12) > kz('K-05.%d' % i, 8) for i in range(1, 8))
falsch_z10 = kz('K-11.4 Z10 POST', 3)
tech_z10 = kz('K-11.4 Z10 POST', 0)
PRUEF(falsch_z10 == 27 and tech_z10 == 1, 'K-11.4: 10 m post IG 27 falsch aufgenommen, 1 technischer Ausfall')
wocap = (kz('K-10.11', 0), kz('K-10.11', 1))
PRUEF(te_post_ueber, 'TE post über dem SESOI in allen sieben Zielgrößen (K-05.1 bis K-05.7)')
aus('  Umsetzungsrate %s %% (K-10.5), Spieler ohne vollständige Einheit %d (K-10.15), Meldungen mit Schmerzangabe '
    '%d (ganz %d, teilweise %d, gar nicht %d) von %d Spielern (K-10.12), Spieler mit Meldungen %d (K-10.9), '
    'zugeteilt %d (K-10.4), CR-10 %s (Median %s), TE post über SESOI in allen sieben Zielgrößen' % (
        pz(rate * 100, 1), null_einheiten, ue[0], ue[1], ue[2], ue[3], ue[4], mit_meldung, zugeteilt, pz(cr10[1], 1),
        pz(cr10[3], 1)))

# ================================================================ § 4 Gemeinsame Wortfolgen
aus('')
aus('§ 4 Gemeinsame Wortfolgen: jeder Satz von Kapitel 5 gegen jeden Satz außerhalb (ohne Platzhalter), '
    'Kandidat ab vier Wörtern in Folge, je Kandidat ein Handurteil')


def tok(s):
    t = s.lower()
    t = re.sub(r'[„“”"()\[\]:!?⟨⟩]', ' ', t)
    t = re.sub(r'[.,](?=\s|$)', ' ', t)
    return t.split()


def folgen(a, b, k):
    m = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                m[i][j] = m[i - 1][j - 1] + 1
    out = []
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            n = m[i][j]
            if n >= k and (i == len(a) or j == len(b) or a[i] != b[j]):
                out.append(' '.join(a[i - n:i]))
    return out


AUSSEN = [i for i in SATZ if SATZ[i]['abschnitt'] != '5' and not SATZ[i]['platzhalter']]
KAND = OrderedDict()
for k in K5_IDS:
    for r in AUSSEN:
        ff = folgen(tok(T(k)), tok(T(r)), 3)
        if ff and max(len(f.split()) for f in ff) >= 4:
            KAND[(k, r)] = ff
HAND_FOLGEN = OrderedDict([
    (('5 A2 S2', '4.6 A2 S1'), ('Nenner', 'Nenner der Umsetzung nach der Bezugsmengen-Regel, keine Doppelung')),
    (('5 A3 S1', '6.1 A6 S1'), ('Bezeichnung', 'Status als Selbstauskunft, 6.1 nimmt ihn auf')),
    (('5 A4 S1', '4.4 A3 S2'), ('Bezeichnung', 'Vergleich TE gegen SESOI, A4 S1 knüpft mit „auch“ an, neuer Zeitpunkt')),
    (('5 A4 S2', '4.3 A3 S2'), ('Bezeichnung', 'Seitenangabe beim 505-Test')),
    (('5 A4 S2', '4.4 A2 S4'), ('Bezeichnung', 'Seitenangabe beim 505-Test')),
    (('5 A5 S4', '6.1 A1 S2'), ('Aufnahme nach Entscheidung', 'Hauptbefund in der Sprache von Kapitel 5 (Register 15b)')),
    (('5 A5 S9', '4.7 A3 S8'), ('Aufnahme nach Entscheidung', 'Entscheidung an der adjustierten Differenz in der '
                                'Sprache der Regel (Register 6f)')),
    (('5 A5 S10', '6.1 A1 S2'), ('Aufnahme nach Entscheidung', 'ganzer Satz A5 S10 in 6.1 A1 S2 (Register 15b)')),
    (('5 A5 S11', '4.7 A1 S5'), ('Bezeichnung', 'Namen der deskriptiven Zielgrößen, die Regel steht in 4.7')),
    (('5 A6 S2', '4.7 A5 S2'), ('Bezeichnung', 'Name des Verfahrens mit der Kennzeichnung „nachträglich“ (c4, Raster '
                                '5.2.4)')),
])
PRUEF(list(KAND.keys()) == list(HAND_FOLGEN.keys()), 'Handurteil je Kandidat (gemeinsame Wortfolgen)')
LAENGSTE = max(max(len(f.split()) for f in ff) for ff in KAND.values())
KATZ = OrderedDict()
for (k, r), ff in KAND.items():
    kat, urteil = HAND_FOLGEN[(k, r)]
    KATZ[kat] = KATZ.get(kat, 0) + 1
    aus('  %s | %s | %s | %s: %s' % (k, r, ' · '.join('„%s“' % f for f in ff), kat, urteil))
PRUEF(LAENGSTE == 5 and KATZ == {'Nenner': 1, 'Bezeichnung': 6, 'Aufnahme nach Entscheidung': 3}, 'Zählung § 4')
PRUEF(folgen(tok(T('5 A5 S10')), tok(T('6.1 A1 S2')), 5) == ['die nullhypothese wurde nicht verworfen'] and len(
    tok(T('5 A5 S10'))) == 5, 'A5 S10 vollständig in 6.1 A1 S2')
L_A6S4 = max([len(f.split()) for f in folgen(tok(T('5 A3 S4')), tok(T('6.1 A6 S4')), 1)] or [0])
L_A2S2 = max([len(f.split()) for f in folgen(tok(T('5 A2 S1')), tok(T('6.1 A2 S2')), 1)] or [0])
PRUEF(L_A6S4 == 1 and L_A2S2 == 3, 'längste Folgen A3 S4 gegen 6.1 A6 S4 und A2 S1 gegen 6.1 A2 S2')
aus('  %d Kandidaten bei %d Sätzen außerhalb, längste Folge %d Wörter · %s' % (
    len(KAND), len(AUSSEN), LAENGSTE, ' · '.join('%s %d' % (k, v) for k, v in KATZ.items())))
aus('  zum Vergleich: A3 S4 gegen 6.1 A6 S4 längste Folge %d Wort, A2 S1 gegen 6.1 A2 S2 %d Wörter' % (L_A6S4, L_A2S2))
PRUEF('nachträglich' in T('5 A6 S2').lower() and 'nachträglich' in T('4.7 A5 S2').lower(), 'nachträglich in beiden')
PRUEF('beobachtend' in T('5 A6 S4') and 'beobachtend' in T('4.7 A1 S4'), 'beobachtend in A6 S4 und 4.7 A1 S4')

# Aussagenähe unterhalb von vier Wörtern in Folge: gemeinsame Wortstämme (Zweitprüfung C10). Kandidat bei mindestens drei
# gemeinsamen Stämmen, die mindestens die Hälfte der Stämme des kürzeren Satzes ausmachen. Je Kandidat ein Handurteil.
STOPP = set(('der die das den dem des ein eine einen einem einer eines und oder mit von zu zur zum im in an auf bei für '
             'aus als wie war waren wurde wurden ist sind nicht nur je auch bis über unter nach vor ohne sowie dass sich '
             'es sie er damit dort sein seine ihr ihre jedes jede keine keiner kein alle allen aller beider beiden beide '
             'tab abb s d p n w m sd ging gingen lag lagen hatte hatten').split())


def staemme(s):
    out = set()
    for w in tok(s):
        if w in STOPP or len(w) < 3 or re.fullmatch(r'[−+\-\d,.%°]+', w):
            continue
        out.add(re.sub(r'(ern|en|er|es|em|e|n|s)$', '', w))
    return out


NAH = OrderedDict()
for k in K5_IDS:
    sk = staemme(T(k))
    for r in AUSSEN:
        if (k, r) in KAND:
            continue
        sr = staemme(T(r))
        if not sk or not sr:
            continue
        gem = sk & sr
        if len(gem) >= 3 and len(gem) / min(len(sk), len(sr)) >= 0.5:
            NAH[(k, r)] = (len(gem), len(gem) / min(len(sk), len(sr)), sorted(gem))
HAND_NAH = OrderedDict([
    (('5 A2 S1', '6.1 A2 S2'), ('Aufnahme in 6.1', 'Umsetzung in Worten ohne Zahl (Raster 6.1.3, TV 6.1 § 4)')),
    (('5 A2 S3', '4.7 A1 S2'), ('Plan und Ergebnis', 'dieselbe Zahl als Ergebnis und als Grund der Festlegung '
                                '(TV5 § 9.1 Nr. 5)')),
    (('5 A3 S3', '6.1 A6 S2'), ('Aufnahme in 6.1', 'Schmerzmeldungen in Worten (Raster 6.1.4)')),
    (('5 A4 S1', '4.4 A3 S1'), ('Plan und Ergebnis', '4.4 führt TE und SESOI ein, A4 S1 berichtet die Abschlusstestung')),
    (('5 A4 S2', '4.2 A1 S5'), ('Bezeichnung', 'Gruppennamen und „Spieler“, verschiedene Aussagen')),
    (('5 A5 S1', '4.7 A3 S4'), ('Plan und Ergebnis', 'Berichtsgrößen in 4.7, Objektsatz zu Tab. 3 in A5 S1')),
    (('5 A5 S1', '4.7 A3 S5'), ('Bezeichnung', 'Hedges\' g und Gruppendifferenz, 4.7 definiert, A5 S1 verweist')),
    (('5 A5 S6', '6.1 A1 S2'), ('Aufnahme in 6.1', 'Hauptbefund in der Sprache von Kapitel 5 (Register 15b)')),
    (('5 A5 S7', '6.1 A3 S3'), ('Aufnahme in 6.1', 'eigener Befund je Zielgröße (Raster 6.1.2, Zug 2)')),
    (('5 A5 S7', '6.1 A4 S3'), ('Aufnahme in 6.1', 'eigener Befund je Zielgröße (Raster 6.1.2, Zug 2)')),
    (('5 A5 S7', '6.1 A5 S3'), ('Aufnahme in 6.1', 'eigener Befund je Zielgröße (Raster 6.1.2, Zug 2)')),
])
PRUEF(list(NAH.keys()) == list(HAND_NAH.keys()), 'Handurteil je Kandidat (gemeinsame Wortstämme)')
NAHZ = OrderedDict()
for (k, r), (n, u, g) in NAH.items():
    kat, urteil = HAND_NAH[(k, r)]
    NAHZ[kat] = NAHZ.get(kat, 0) + 1
    aus('  Stämme: %s | %s | %d, Anteil %s | %s | %s: %s' % (k, r, n, pz(u, 2), ' '.join(g), kat, urteil))
PRUEF(NAHZ == {'Aufnahme in 6.1': 6, 'Plan und Ergebnis': 3, 'Bezeichnung': 2}, 'Zählung der Stammkandidaten')
PRUEF(all('relevant' in T(i) and 'beide Richtungen' in T(i) for i in ('6.1 A3 S3', '6.1 A4 S3', '6.1 A5 S3')),
      'A5 S7 dreimal in 6.1')
aus('  %d Paare über gemeinsame Wortstämme · %s' % (len(NAH), ' · '.join('%s %d' % (k, v) for k, v in NAHZ.items())))

# ================================================================ § 5 Bezugsmengen und Platzhalter
aus('')
aus('§ 5 Spielerzahlen der Menge „zur Eingangstestung angetreten“ in Kapitel 4 und Platzhalter in Anhang H')
KAND_Z = OrderedDict()
for i in SATZ:
    if SATZ[i]['abschnitt'].startswith('4'):
        for m in re.finditer(r'(?<![\d,.:])(31|18|13)(?![\d,.:])', T(i)):
            KAND_Z[(i, m.group(1))] = T(i)[max(0, m.start() - 30):m.end() + 10]
HAND_Z = {('4.7 A3 S6', '13'): 'Seitenzahl (Lakens, 2022, S. 13–14)'}
PRUEF(set(KAND_Z) == set(HAND_Z), 'Handurteil je Zahl 31, 18, 13 in Kapitel 4')
for (i, z), ctx in KAND_Z.items():
    aus('  %s „%s“ in „…%s…“: %s' % (i, z, ctx, HAND_Z[(i, z)]))
PRUEF('N = 26' in T('4.2 A1 S4') and '16 Spieler' in T('4.2 A1 S5'), '26 und 16 in 4.2')
PRUEF('31' in T('5 A1 S2') and '26' in T('5 A1 S2') and T('5 A2 S1').startswith('Die 18 zugeteilten'), '31, 26, 18')
PRUEF(sum(1 for i in SATZ if re.search(r'(?<![\d,.:])31(?![\d,.:])', T(i))) == 1, '31 nur in einem Satz')
PLATZ = [i for i in SATZ if SATZ[i]['platzhalter'] and SATZ[i]['abschnitt'] == 'Anhang H']
for i in PLATZ:
    aus('  %s: %s' % (i, T(i)))

# ================================================================ § 6 Begriffe
aus('')
aus('§ 6 Begriffe je Teil (Zählung der Fundstellen im Fließtext, Überschriften gesondert)')


def teil(ab):
    if ab == '1':
        return 'Einl.'
    if ab.startswith('4.4'):
        return '4.4'
    if ab.startswith('4.5'):
        return '4.5'
    return ab


TEILE = ['Einl.', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '5', '6.1']
BEGRIFFE = OrderedDict([
    ('Adhärenz', r'Adhärenz'),
    ('Umsetzung', r'Umsetzung'),
    ('„ganz“', r'„ganz“'),
    ('als vollständig', r'als vollständig'),
    ('vollständig durchgeführt', r'vollständig durchgeführt'),
    ('teilweise durchgeführt', r'teilweise durchgeführt'),
    ('Beteiligung', r'Beteiligung'),
    ('TE', r'\bTE\b'),
    ('typischer Messfehler', r'typische[nr]? Messfehler'),
    ('H0', r'\bH0\b'),
    ('Nullhypothese', r'Nullhypothese'),
    ('unschlüssig', r'unschlüssig'),
    ('nachweisbar', r'[Nn]achweisbar'),
    ('Relevanz, relevant', r'[Rr]elevan'),
    ('in beide Richtungen', r'in beide Richtungen'),
    ('Analyseset', r'Analyseset'),
    ('Hauptanalyse', r'Hauptanalyse'),
    ('Programmwoche', r'Programmwoche'),
    ('Schmerz', r'Schmerz'),
    ('Schmerzen oder Probleme', r'Schmerzen oder Probleme'),
    ('Spieler mit Meldungen', r'Spieler mit Meldungen'),
    ('Post-Wert', r'Post-Wert'),
    ('Abschlusswert', r'Abschlusswert'),
    ('Voraussetzung', r'Voraussetzung'),
    ('Modellannahmen', r'Modellannahme'),
    ('AU', r'\bAU\b'),
    ('zugeteilt', r'zugeteilt'),
    ('Effekt', r'Effekt'),
    ('Beanspruchung', r'Beanspruchung'),
    ('Belastung', r'Belastung'),
    ('standardisierte Differenz', r'standardisierte[rn]? Differenz'),
    ('Überlappung', r'Überlappung'),
    ('Untergrenze', r'Untergrenze'),
    ('Einheitennummer', r'Einheitennummer'),
    ('Zielgröße', r'Zielgröße'),
    ('abhängige Variable', r'\b[Aa]bhängige Variable'),
])
ZAHL = OrderedDict()
for b, rx in BEGRIFFE.items():
    z = OrderedDict((t, 0) for t in TEILE)
    for i in SATZ:
        tt = teil(SATZ[i]['abschnitt'])
        if tt in z and not SATZ[i]['platzhalter']:
            z[tt] += len(re.findall(rx, T(i)))
    ue_tr = [u for u in UEBERSCHRIFT.values() if re.search(rx, u)]
    ZAHL[b] = (z, ue_tr)
    aus('  %-26s %s%s' % (b, ' · '.join('%s %d' % (t, n) for t, n in z.items() if n),
                         ('  · Überschrift: ' + ' · '.join(ue_tr)) if ue_tr else ''))


def zb(b, t):
    return ZAHL[b][0][t]


# Handurteile zu den Begriffen, gebunden an die Zählung
PRUEF(zb('Adhärenz', '4.6') == 2 and zb('Adhärenz', '4.7') == 4 and zb('Adhärenz', '4.1') == 1
      and zb('Adhärenz', '5') == 0 and zb('Adhärenz', '6.1') == 0, 'Adhärenz nur in Kapitel 4')
PRUEF(ZAHL['Adhärenz'][1] == ['4.6 Adhärenz- und Belastungsmonitoring'], 'Überschrift 4.6 mit Adhärenz')
PRUEF(zb('Umsetzung', '5') == 1 and zb('Umsetzung', '6.1') == 3 and zb('Umsetzung', '4.5') == 1 and sum(
    zb('Umsetzung', t) for t in ('4.1', '4.2', '4.3', '4.4', '4.6', '4.7')) == 0, 'Umsetzung')
PRUEF('in ihrer Umsetzung erfasst' in T('4.5.2 A1 S1'), 'Umsetzung in 4.5.2 meint die Vereinsprogramme')
PRUEF(zb('„ganz“', '4.6') == 1 and zb('„ganz“', '5') == 0 and zb('als vollständig', '5') == 2
      and zb('als vollständig', '6.1') == 3, 'Status ganz gegen als vollständig')
PRUEF(zb('vollständig durchgeführt', '6.1') == 1 and zb('vollständig durchgeführt', '5') == 0
      and zb('teilweise durchgeführt', '5') == 2, 'vollständig durchgeführt nur in 6.1')
PRUEF(zb('Beteiligung', '4.6') == 1 and zb('Beteiligung', '5') == 0, 'Beteiligung')
PRUEF(zb('TE', '4.4') == 2 and zb('TE', '5') == 0 and zb('typischer Messfehler', '4.4') == 1
      and zb('typischer Messfehler', '5') == 1, 'TE und typischer Messfehler')
PRUEF(zb('H0', '4.7') == 1 and zb('Nullhypothese', '4.7') == 0 and zb('Nullhypothese', 'Einl.') == 1
      and zb('Nullhypothese', '5') == 1 and zb('Nullhypothese', '6.1') == 1, 'H0 und Nullhypothese')
PRUEF(zb('unschlüssig', '4.7') == 0 and zb('unschlüssig', '5') == 2 and zb('unschlüssig', '6.1') == 1,
      'unschlüssig nicht in 4.7')
PRUEF(zb('in beide Richtungen', '4.7') == 1 and zb('in beide Richtungen', '5') == 1
      and zb('in beide Richtungen', '6.1') == 3, 'in beide Richtungen')
PRUEF(zb('Analyseset', '5') == 1 and sum(zb('Analyseset', t) for t in TEILE if t != '5') == 0, 'Analyseset')
PRUEF(zb('Programmwoche', '5') == 1 and sum(zb('Programmwoche', t) for t in TEILE if t != '5') == 0, 'Programmwoche')
PRUEF(zb('Schmerzen oder Probleme', '5') == 1 and zb('Schmerzen oder Probleme', '6.1') == 1
      and zb('Schmerzen oder Probleme', '4.6') == 0 and zb('Schmerz', '4.6') == 1, 'Schmerzen oder Probleme')
PRUEF(zb('Spieler mit Meldungen', '6.1') == 1 and zb('Spieler mit Meldungen', '5') == 0, 'Spieler mit Meldungen')
PRUEF(zb('Post-Wert', '5') == 1 and zb('Abschlusswert', '5') == 1 and zb('Abschlusswert', '4.7') == 1,
      'Post-Wert und Abschlusswert')
PRUEF(zb('Modellannahmen', '4.7') == 1 and zb('Voraussetzung', '4.7') == 1 and zb('Voraussetzung', '5') == 1,
      'Modellannahmen und Voraussetzung')
PRUEF(zb('AU', '5') == 1 and sum(zb('AU', t) for t in TEILE if t != '5') == 0, 'AU nur in Kapitel 5')
PRUEF(zb('Effekt', '5') == 0, 'Kapitel 5 ohne „Effekt“')
PRUEF(zb('Beanspruchung', '4.6') == 2 and zb('Beanspruchung', '5') == 1 and zb('Belastung', '5') == 0,
      'Beanspruchung')
PRUEF(zb('standardisierte Differenz', '5') == 1 and sum(zb('standardisierte Differenz', t) for t in TEILE
                                                         if t != '5') == 0, 'd nur in Kapitel 5')
PRUEF(zb('Überlappung', '5') == 1 and zb('Überlappung', '4.7') == 1, 'Überlappung in A1 S3 und 4.7 A4 S3')
PRUEF(zb('Untergrenze', '5') == 1 and sum(zb('Untergrenze', t) for t in TEILE if t != '5') == 0, 'Untergrenzen')
PRUEF(zb('Einheitennummer', '5') == 1 and zb('Einheitennummer', '4.6') == 1, 'Einheitennummer')
PRUEF(zb('abhängige Variable', '4.1') == 1, 'abhängige Variablen in 4.1')

# ================================================================ § 7 Folge der Zielgrößen
aus('')
aus('§ 7 Folge Sprint (S), Richtungswechsel (C), Sprung (J) in Sätzen mit mindestens zweien davon (erste Nennung)')
MUSTER = OrderedDict([('S', r'[Ss]print|30-m|10-m|Beschleunigung|Laufgeschwindigkeit'),
                      ('C', r'Richtungswechsel|505|Wende\b'),
                      ('J', r'Sprung(?!übung|formen)|Standweitsprung|Sprunghöhe|Weite\b|Sprungleistung')])
FOLGE = OrderedDict()
for i in SATZ:
    if SATZ[i]['platzhalter'] or SATZ[i]['abschnitt'].startswith('Anhang'):
        continue
    pos = OrderedDict()
    for z, rx in MUSTER.items():
        m = re.search(rx, T(i))
        if m:
            pos[z] = m.start()
    if len(pos) >= 2:
        FOLGE[i] = ''.join(sorted(pos, key=pos.get))
REGEL = ('SC', 'SJ', 'CJ', 'SCJ')
ABW = [i for i, f in FOLGE.items() if f not in REGEL]
HAND_FOLGE = OrderedDict([
    ('B2 S9', ('Sprint- und Sprungleistung … während sich die Richtungswechselleistung',
               'Kontrast nach dem Befund der Vorstudie, Einleitung', False)),
    ('4.3 A5 S3', ('vom Sprint über den Standweitsprung bis zum belastungsintensivsten 505-Test',
                   'Testfolge des Protokolls, Methodik', False)),
    ('4.7 A1 S5', ('die 505-Seitenwerte laut Studienprotokoll sowie alle Teilmengen … so die 5- und 10-m-Sprintzeiten',
                   'nach dem Grund der Festlegung, Methodik', False)),
    ('5 A4 S2', ('beim 30-m-Sprint und Standweitsprung … beim 505-Test je Seite',
                 'nach der Gruppe mit mehr gültigen Versuchen, Ergebnisse (2b.8)', True)),
    ('6.1 A3 S6', ('Sprung, Beschleunigung und Richtungswechsel',
                   'Fähigkeiten, die ein Programm ansprechen dürfte, keine Zielgrößen (Transfer nach Oliver et al., '
                   '2024)', False)),
])
PRUEF(ABW == list(HAND_FOLGE.keys()), 'Handurteil je abweichender Folge')
for i, f in FOLGE.items():
    if i in HAND_FOLGE:
        z, urteil, in_regel = HAND_FOLGE[i]
        teile = [t.strip() for t in z.split('…')]
        p0 = 0
        for t in teile:
            p1 = T(i).find(t, p0)
            PRUEF(p1 >= 0, 'Aufzählung in %s' % i)
            p0 = p1 + len(t)
        aus('  %-10s %s  abweichend: „%s“ · %s · %s' % (i, f, z, urteil,
                                                       'gegen F17 § 5.1' if in_regel else 'außerhalb der Regel'))
    else:
        aus('  %-10s %s' % (i, f))
GEHALTEN = [i for i in FOLGE if i not in HAND_FOLGE]
PRUEF(len(FOLGE) == 18 and len(GEHALTEN) == 13, '18 Sätze, 13 in der festen Folge')
PRUEF(GEHALTEN == ['B1a S1', 'B1a S3', 'B1a S5', 'B1b S4', 'B1b S5', 'B4 S3', 'B5 S1', 'B5 S3', '4.1 A4 S2',
                    '4.7 A3 S1', '5 A5 S5', '5 A5 S11', '6.1 A1 S1'], 'Sätze in der festen Folge wie in der Zeile genannt')
ABW_REGEL = [i for i in HAND_FOLGE if HAND_FOLGE[i][2]]
PRUEF(ABW_REGEL == ['5 A4 S2'], 'gegen F17 § 5.1 nur A4 S2')
PRUEF(T('B1b S4').find('Maximalsprint') < T('B1b S4').find('180°-Wende') < T('B1b S4').find('Sprung mit'),
      'B1b S4 in der festen Folge')

# ================================================================ § 8 Spätere Teile
aus('')
aus('§ 8 Spätere Teile (im Master ohne Text): geplante Übernahmen aus Kapitel 5')
for spaet in ('6.2', '6.3', '7'):
    PRUEF(not any(SATZ[i]['abschnitt'] == spaet for i in SATZ), '%s ohne Text' % spaet)
    PRUEF(('Überschrift ' + spaet) in UEBERSCHRIFT, 'Überschrift %s im Master' % spaet)
aus('  6.2, 6.3 und 7 ohne Textabsatz im Master (nur Überschriften), Zusammenfassung und Abstract als Vorspann-Titel '
    'ohne Text')
S4A_ZEILEN = OrderedDict([('6.2.5 a', 'W und p stehen in Kapitel 5'),
                          ('6.2.6 b', 'Mechanismen nennt 4.4, die Richtung Kapitel 5 (5.1), hier nur die Folge'),
                          ('6.3.2 G6-b', 'Untergrenzen nennt Kapitel 5, hier nur der Grund'),
                          ('V06', 'Schmerzen ohne Lokalisation und Abbrüche: 6.1 A6 S2 und S3 und Kapitel 5'),
                          ('V42', 'die fehlenden Vergleichsdaten der Kontrollgruppe nennen Kapitel 5 und 6.1 A6 S4'),
                          ('V73', 'Kapitel 5 und Abb. 1 (Teilnehmerfluss)'),
                          ('K7-a', 'Forschungsempfehlung zur Umsetzung und ihrer Berichterstattung')])
for k, marke in S4A_ZEILEN.items():
    zt = DOK['s4a'][DOK['s4a'].find('| %s |' % k):]
    PRUEF(DOK['s4a'].find('| %s |' % k) >= 0 and marke in zt[:zt.find('\n')], 'S4a-Zeile %s' % k)
    aus('  S4a %s: %s' % (k, marke))
for k in ('7.1', '7.2'):
    PRUEF('| %s |' % k in DOK['raster'], 'Rasterzeile %s' % k)

# ================================================================ § 9 Teiltabelle 2e
ZITATE = []


def Q(z, ort):
    """Zitat mit Ort: Satzkennung des Masters, Überschrift, Dokumentschlüssel oder (Schlüssel, Anfangsmarke, Endmarke)."""
    ZITATE.append((z, ort))
    return '„' + z + '“'


def aufloesen(ort):
    if isinstance(ort, tuple):
        d = DOK[ort[0]]
        a = d.find(ort[1])
        PRUEF(a >= 0, 'Marke %r in %s' % (ort[1], ort[0]))
        e = d.find(ort[2], a + len(ort[1])) if len(ort) > 2 else len(d)
        PRUEF(e >= 0, 'Endmarke %r in %s' % (ort[2] if len(ort) > 2 else '', ort[0]))
        return d[a:e]
    if ort in SATZ:
        return T(ort)
    if ort in UEBERSCHRIFT:
        return UEBERSCHRIFT[ort]
    if ort in DOK:
        return DOK[ort]
    raise SystemExit('Ort unbekannt: %r' % (ort,))


def an_wortgrenze(text, t, start):
    i = text.find(t, start)
    while i >= 0:
        vor = text[i - 1] if i > 0 else ' '
        nach = text[i + len(t)] if i + len(t) < len(text) else ' '
        if (not vor.isalnum() or not t[0].isalnum()) and (not nach.isalnum() or not t[-1].isalnum()):
            return i
        i = text.find(t, i + 1)
    return -1


def zitat_ok(z, text):
    p = 0
    for t in [x.strip() for x in z.split('…') if x.strip()]:
        i = an_wortgrenze(text, t, p)
        if i < 0:
            return False
        p = i + len(t)
    return True


def g2(x):
    return pz(x, 2)


ZEILEN = OrderedDict()


def zeile(schluessel, gegenstand, befund, fund, ergebnis, status, beleg):
    PRUEF(schluessel not in ZEILEN, 'Schlüssel %s einmalig' % schluessel)
    PRUEF(SK not in ''.join([gegenstand, befund, fund, ergebnis, status, beleg]), 'kein Semikolon in %s' % schluessel)
    ZEILEN[schluessel] = OrderedDict([('Nr.', ''), ('Prüfgegenstand', gegenstand), ('Befundstelle', befund),
                                      ('Fundstelle im Text', fund), ('Ergebnis', ergebnis), ('Status', status),
                                      ('Beleg', beleg)])


Q_LOAD = Q('sRPE-Load', '5 A3 S2')
zeile('textstand', 'Textstand am Master nach Rev. 163',
      'Fundstelle · Startprompt Schritt 2 e, Fortsetzung 4 § 4',
      'Master, Kapitel 5, alle Textabsätze',
      'Master %s Byte, MD5 %s…, keine comments.xml, %d Absätze, unverändert seit Rev. 163. Kapitel 5 zeichengleich '
      'mit textstand.json (%d Wörter, %d Sätze), 6.1 zeichengleich mit der JSON der Fassung 3 (%d Wörter, %d Sätze). '
      'Gegen master_saetze.json (Stand 03.10., 08:05) sind nur 6.1 A3 bis A5 geändert, %d Sätze stehen unter gleicher '
      'Kennung gleich, %d dem Wortlaut nach. Zusammenfassung und Abstract stehen als Titel ohne Text.' % (
          '{:,}'.format(os.path.getsize(MASTER)).replace(',', '.'), md5(MASTER)[:8], len(P), K5_W, len(K5_IDS), W61,
          len(S61), len(gleich), len(gleich_wortlaut)),
      'erfüllt', 'anschluss_2e.txt § 1')

zeile('bezuege', 'Satznummern von 6.1 nach Rev. 163 und Sätze mit Bezug auf Kapitel 5 (Prüfpunkt Anschluss gegen den '
                 'gültigen Stand von 6.1)',
      'Fundstelle · Abgleichbefund § 1.4 (a), Befund § 6.5 Nr. 10, TV 6.1 § 4, Fortsetzung 4 § 5 Nr. 4',
      '6.1 A1 bis A6',
      '6.1 A3 S5 entfällt (Stufe 3), 6.1 A3 S6 und S7 werden S5 und S6 (S6 ohne „zudem“), 6.1 A4 S4 ist ohne Rückbezug '
      'neu gefasst. Neu ist 6.1 A4 S6 (%s), die bisherigen 6.1 A4 S6 bis S8 werden S7 bis S9, 6.1 A4 S9 und A5 S6 sind '
      'neu gefasst (%s). Bezug auf Kapitel 5 hat ein Satz mit eigenem Befund, Zahl oder Begriff aus Kapitel 5, mit '
      'ausdrücklichem Rückbezug auf den eigenen Befund oder mit einem Konnektor, der einen Vergleich mit ihm markiert. '
      'Danach haben %d von %d Sätzen Bezug. Seit Rev. 163 neu sind 6.1 A4 S6, A4 S9 und A5 S6, als Bezug entfällt 6.1 '
      'A4 S4. § 1.4 (a) führte vier unveränderte Sätze mit Konnektor nicht: 6.1 A2 S3 (%s, Umsetzung als Kontext) sowie '
      '6.1 A4 S7, A4 S8 und A5 S5, die einen Widerspruch markieren (TV 6.1 § 4 %s). Grenzfälle ohne Marke und ohne '
      'Bezug sind 6.1 A3 S6 und A5 S7. Nachzuführen sind § 1.4 (a), 2b.8 (die bisherige 6.1 A3 S7 heißt 6.1 A3 S6) '
      'und 2b.29 (30 statt 24 Sätze), als Stand vor Rev. 163 bleiben Abgleichbefund § 1.1, register_pruefung.md 6i und '
      'Fortsetzung 4 § 5 Nr. 4. Liste in bezuege_2e.md.' % (
          Q('Mit beiden ist der eigene Befund vereinbar.', '6.1 A4 S6'),
          Q('was mit dem eigenen Befund vereinbar ist', '6.1 A5 S6'), len(BEZUG), len(S61), Q('Auch', '6.1 A2 S3'),
          Q('Vergleich als Widerspruch markiert', ('tv61', '| A4 S7 |', '\n'))),
      'erfüllt (Liste am Master neu aufgestellt, Satznummern nachgeführt)', '§ 2, bezuege_2e.md')

zeile('doppelung', 'Wörtliche Doppelung, systematisch',
      'Fundstelle · Startprompt Schritt 2 e, F17 § 5a „Nicht übernehmen“ (Bauplan § 8), Register 15b, 6f, c4, c8, '
      'Raster 5.1.8, 6.1.2',
      '29 Sätze von Kapitel 5 gegen %d Sätze außerhalb' % len(AUSSEN),
      '%d Paare mit einer gemeinsamen Folge von mindestens vier Wörtern, längste %d Wörter. Handurteil je Paar: '
      'Bezeichnung %d (etwa %s in A4 S2 wie in 4.3 A3 S2 und 4.4 A2 S4, %s in A6 S2 wie in 4.7 A5 S2, beide mit der '
      'Kennzeichnung %s nach c4 und Raster 5.2.4), Nenner %d (%s in A2 S2 wie in 4.6 A2 S1), Aufnahme nach Entscheidung '
      '%d: A5 S10 steht vollständig in 6.1 A1 S2, ebenso %s (Register 15b), A5 S9 nimmt 4.7 A3 S8 in dessen Sprache auf '
      '(%s, Register 6f). Unterhalb von vier Wörtern findet eine Suche über gemeinsame Wortstämme (mindestens drei, '
      'mindestens die Hälfte des kürzeren Satzes) %d weitere Paare: Aufnahme in 6.1 %d (A5 S7 in 6.1 A3 S3, A4 S3 und '
      'A5 S3 als eigener Befund je Zielgröße nach Raster 6.1.2, dazu A2 S1, A3 S3 und A5 S6 in 6.1 A2 S2, A6 S2 und '
      'A1 S2), Plan und Ergebnis %d (A2 S3, A4 S1 und A5 S1 gegen 4.7 A1 S2, 4.4 A3 S1 und 4.7 A3 S4), Bezeichnung %d. '
      'Ohne gemeinsame Stämme tragen A3 S4 und 4.6 A1 S2 dieselbe Tatsache aus Plan und Ergebnis (Raster 5.1.8), %s '
      'steht in A6 S4 wie in 4.7 A1 S4 (c4), 6.1 A1 S5 nimmt A5 S7 in anderen Worten auf. Wörtliche Doppelung einer '
      'Methodenangabe ohne Entscheidung keine. Den Inhalt einer Regel wiederholt A5 S11 ({{deskriptiv}}).' % (
          len(KAND), LAENGSTE, KATZ['Bezeichnung'], Q('beim 505-Test je Seite', '4.4 A2 S4'),
          Q('Bootstrap-Konfidenzintervall der adjustierten Differenz', '4.7 A5 S2'), Q('nachträglich', '5 A6 S2'),
          KATZ['Nenner'], Q('bei zwölf angebotenen Einheiten', '4.6 A2 S1'), KATZ['Aufnahme nach Entscheidung'],
          Q('für Ausgangswert und Reifestatus', '6.1 A1 S2'), Q('einen Vorteil der Interventionsgruppe', '4.7 A3 S8'),
          len(NAH), NAHZ['Aufnahme in 6.1'], NAHZ['Plan und Ergebnis'], NAHZ['Bezeichnung'],
          Q('beobachtend', '4.7 A1 S4')),
      'erfüllt (keine wörtliche Doppelung einer Methodenangabe ohne Entscheidung), Aufnahmen bewusst anders · '
      'Register 15b, 6f, c4',
      '§ 4')

zeile('hauptbefund', '6.1 A1 S2 bis S6: Hauptbefund, Vorsprung, Fall C1, „unschlüssig“',
      'Fundstelle · Befund § 6.5 Nr. 10, Register 15b, F17 § 10 (Nullbefund- und ITT-Sprachregelung)',
      '6.1 A1 S2 bis S6 · A5 S3, S4, S6 bis S8, S10',
      'Begriffe wie Kapitel 5: %s, %s, %s, %s. 6.1 A1 S5 fasst A5 S7 als %s (ITT-Sprachregelung). 6.1 A1 S3 und S4 '
      'nehmen A5 S3 auf: Die IG lag in allen drei Post-Werten vorn (Tab. 3: %s gegen %s s, %s gegen %s s, %s gegen %s '
      'cm), die adjustierte Differenz beträgt %s, %s und %s der unadjustierten, was %s trägt. Kapitel 5 nennt Richtung '
      'und Abstand, die Größe nur Tab. 3 und Abb. 2. Doppelung des Hauptbefunds nach Register 15b ({{doppelung}}).' % (
          Q('Nach Adjustierung für Ausgangswert und Reifestatus', '6.1 A1 S2'),
          Q('Gruppenunterschied nachweisbar', '6.1 A1 S2'), Q('die Nullhypothese wurde nicht verworfen', '6.1 A1 S2'),
          Q('Die Befunde sind unschlüssig', '6.1 A1 S6'),
          Q('relevante Vorteile wie Nachteile des Programmangebots', '6.1 A1 S5'), pz(z30['post_ig'], 2),
          pz(z30['post_kg'], 2), pz(cm['post_ig'], 2), pz(cm['post_kg'], 2), pz(sbj['post_ig'], 0),
          pz(sbj['post_kg'], 0), pz(z30['anteil'] * 100, 0) + ' %', pz(cm['anteil'] * 100, 0) + ' %',
          pz(sbj['anteil'] * 100, 0) + ' %', Q('weitgehend', '6.1 A1 S4')),
      'erfüllt (Begriffe, Deckung), Doppelung bewusst anders · Register 15b', '§ 3, § 4')

zeile('umsetzung', '6.1 A2 S2 bis S4 und A4 S9: Umsetzung in Worten und Literaturvergleich',
      'Fundstelle · Befund § 6.5 Nr. 10, F17 § 3 (Bezugsmengen-Regel), § 11.7, TV 6.1 § 4',
      '6.1 A2 S2 bis S4, A4 S9 · A2 S1, S2, A5 S6',
      '%s, %s und %s wie A2 S1 und S2, %s wie %s (A2 S2). %s trägt %s %% (K-10.5). %s sind %d Spieler ohne vollständige '
      'Einheit (K-10.15), nur in Tab. H2. 6.1 A2 S3 vergleicht die eigene Umsetzung über %s mit einer Übersicht '
      '(TV 6.1 § 4), Kapitel 5 trägt die eigene Rate. 6.1 A2 S4 nimmt zudem A5 S6 auf (%s). 6.1 A4 S9 (seit Rev. 163) '
      'bietet die eigene Umsetzung als Erklärung an, Kapitel 5 trägt die Rate. Längste gemeinsame Folge mit A2 S1 drei '
      'Wörter.' % (
          Q('zugeteilten Spieler', '6.1 A2 S2'), Q('angebotenen Einheiten', '6.1 A2 S2'),
          Q('als vollständig', '6.1 A2 S2'), Q('Umsetzung', '6.1 A2 S4'), Q('Umsetzungsrate', '5 A2 S2'),
          Q('weniger als die Hälfte', '6.1 A2 S2'), pz(rate * 100, 1), Q('einige keine einzige', '6.1 A2 S2'),
          null_einheiten, Q('Auch', '6.1 A2 S3'), Q('Ein nicht nachweisbarer Unterschied', '6.1 A2 S4')),
      'erfüllt (zweiter Teil von 6.1 A2 S2 nur über Tab. H2)', '§ 2, § 3, § 4')

zeile('perprotokoll', '6.1 A2 S5, S6: Per-Protokoll',
      'Fundstelle · Befund § 6.5 Nr. 10, Register 10h, V7, c4, F17 § 11.2b (R4)',
      '6.1 A2 S5, S6 · A2 S3, A6 S4',
      '%s wie A6 S4 und 4.7 A1 S4, %s ist die Schwelle sechs (A2 S3, 4.7 A1 S3 %s). %s trägt A6 S4, ebenso %s (%s), '
      'bei welcher Zielgröße die Fallzahl nicht reichte, steht nur in Tab. H4 (505-Seitenmittel %d und %d Spieler, '
      'K-08.1). Punktschätzer und Vorzeichenwechsel (30-m-Sprint %s gegen %s s, Standweitsprung %s gegen %s cm, K-08.1, '
      'K-06) stehen nur in Tab. H4. %s misst {{nahenull}} am SESOI.' % (
          Q('beobachtende Per-Protokoll-Vergleich', '6.1 A2 S5'),
          Q('mindestens der Hälfte der Einheiten als vollständig gemeldet', '6.1 A2 S5'),
          Q('der Hälfte des Programms', '4.7 A1 S3'), Q('änderte die Einordnung nicht', '6.1 A2 S5'),
          Q('beim Richtungswechsel reichte die Fallzahl nicht', '6.1 A2 S6'),
          Q('Soweit die Fallzahl eine Inferenz zuließ', '5 A6 S4'), pp_n_cm[0], pp_n_cm[1],
          pzv(pp30, 3), pz(z30['b1'], 3), pzv(ppsbj, 1), pz(sbj['b1'], 1), Q('nahe null', '6.1 A2 S6')),
      'teilweise („nahe null“ beim Per-Protokoll-Schätzer des 30-m-Sprints, Schwere B, siehe {{nahenull}}), '
      'Punktschätzer und Zielgröße ohne Inferenz nur über Tab. H4', '§ 3')

zeile('beschreibend', '6.1 A3 S2, A4 S2, A5 S2: beschreibende Prä- und Post-Mittel',
      'Fundstelle · Register 10d, V6 (Prä- und Post-Mittel nach 6.1), TV5 § 9.3 Nr. 4, Befund § 6.5 Nr. 10',
      '6.1 A3 S2, A4 S2, A5 S2 · Tab. 2 (A1 S3), Tab. 3 (A5 S1)',
      '30-m-Sprint IG %s → %s s, KG %s → %s s (%s, %s) · 505-Seitenmittel IG %s → %s s, KG %s → %s s (%s) · '
      'Standweitsprung IG %s → %s cm, KG %s → %s cm (%s), K-04.3, K-04.6, K-04.7, K-06.1 bis K-06.3. Prä in Tab. 2, '
      'Post M ± SD in Tab. 3 (Raster 5.2.1). A5 S1 nennt als Inhalt von Tab. 3 die Differenzen und g, nicht die '
      'Post-Mittel.' % (
          pz(z30['prae_ig'], 2), pz(z30['post_ig'], 2), pz(z30['prae_kg'], 2), pz(z30['post_kg'], 2),
          Q('etwas höher als zuvor', '6.1 A3 S2'), Q('die der Kontrollgruppe gleich', '6.1 A3 S2'),
          pz(cm['prae_ig'], 2), pz(cm['post_ig'], 2), pz(cm['prae_kg'], 2), pz(cm['post_kg'], 2),
          Q('nahezu unverändert', '6.1 A4 S2'), pz(sbj['prae_ig'], 0), pz(sbj['post_ig'], 0), pz(sbj['prae_kg'], 0),
          pz(sbj['post_kg'], 0), Q('sanken', '6.1 A5 S2')),
      'erfüllt (nur über Tab. 2 und Tab. 3)', '§ 3')

ppsbj_q = abs(ppsbj) / sbj['sesoi']
PRUEF(round(ppsbj_q, 2) == 0.15 and round(pp30_q, 2) == 0.52, 'Per-Protokoll gegen den SESOI')
zeile('nahenull', '6.1 A3 S3, A4 S3, A5 S3 und A2 S6: „lag nahe null“ und Fall C1',
      'Fundstelle · Befund § 6.5 Nr. 10, F17 § 5a, § 10 (Nullbefund-Sprachregelung), § 11.2b, Umfangsdokument § 5.1, '
      '4.7 A3 S6, Abgleich Diskussion 6.1 (2c.3)',
      '6.1 A3 S3, A4 S3, A5 S3, A2 S6 · A5 S4, S5, S7, A6 S4',
      '%s ist A5 S7 (Fall C1). %s steht in Kapitel 5 nicht. 4.7 A3 S6 legt das Konfidenzintervall gegen null und den '
      'SESOI (%s), für den Punktschätzer hat das Projekt keine Regel und keine Musterformulierung (F17 § 11.2b, '
      'Umfangsdokument § 5.1). Gemessen am SESOI liegt der Schätzer beim 30-m-Sprint bei %s SESOI (%s gegen %s s), beim '
      '505-Seitenmittel bei %s (%s gegen %s s), beim Standweitsprung bei %s (%s gegen %s cm), g %s, %s und %s (K-05, '
      'K-06). Beim 30-m-Sprint und 505-Seitenmittel liegt er damit näher am SESOI als an null, knapp ebenso der '
      'Per-Protokoll-Schätzer des 30-m-Sprints (6.1 A2 S6, nur Tab. H4, %s SESOI). Nur beim Standweitsprung (%s, '
      'Per-Protokoll %s SESOI) trägt „nahe null“. Auf der Skala von g bliebe nur Cohens Konvention, F17 § 5a ordnet aber '
      '%s. Der parallele Task wertete die Formel als %s (Abgleich Diskussion 6.1, 2c.3), ohne den SESOI zu prüfen. Für '
      'die Klickfrage beim Abschluss: „lag nahe null“ streichen oder „lag dem Betrag nach unter dem SESOI“, das an allen '
      'vier Stellen getragen ist.' % (
          Q('ihr Intervall ließ relevante Unterschiede in beide Richtungen zu', '6.1 A3 S3'),
          Q('lag nahe null', '6.1 A3 S3'), Q('mit null und dem SESOI in beide Richtungen verglichen', '4.7 A3 S6'),
          g2(z30['q']), pz(z30['b1'], 3), pz(z30['sesoi'], 3), g2(cm['q']), pz(cm['b1'], 3), pz(cm['sesoi'], 3),
          g2(sbj['q']), pz(sbj['b1'], 1), pz(sbj['sesoi'], 1), g2(z30['g']), g2(cm['g']), pz(sbj['g'], 2), g2(pp30_q),
          g2(sbj['q']), g2(ppsbj_q),
          Q('Effektstärke ohne Schwellen, eingeordnet über das Konfidenzintervall gegen null und den SESOI', 'f17'),
          Q('Fall C1 sinngemäß nach dem Umfangsdokument § 5.1', ('abg61', '| 2c.3 |', '| 2c.4 |'))),
      'teilweise (Fall C1 erfüllt, „nahe null“ beim 30-m-Sprint und 505-Seitenmittel und beim Per-Protokoll-Schätzer '
      'des 30-m-Sprints von Kapitel 5 nicht getragen, Schwere B, Folgeänderung für 6.1 als eigene Klickfrage beim '
      'Abschluss)', '§ 3')

zeile('rueckbezuege', '6.1 A3 S5, A4 S6 bis S8, A5 S4 bis S6: Rückbezüge und Markierungen gegen den eigenen Befund',
      'Fundstelle · Befund § 6.5 Nr. 10, TV 6.1 § 4 (Markierung nach der Lage im eigenen Intervall), Register 3c',
      '6.1 A3 S5, A4 S6 bis S8, A5 S4 bis S6 · A5 S4 bis S7, Tab. 3',
      '„eigene Befund“ meint die adjustierte Differenz mit Intervall (A5 S4, S5) und den Fall C1 (A5 S7). %s in 6.1 A4 '
      'S6 und A5 S6 (beide seit Rev. 163) misst die Lage einer Vorstudie im eigenen Intervall, A5 S7 nutzt das Wort für '
      'das Intervall selbst, gleichsinnig. 6.1 A5 S4 markiert mit %s, 6.1 A4 S7, A4 S8 und A5 S5 über ihren Konnektor '
      'einen Widerspruch: Nach TV 6.1 § 4 liegen die Vorstudienwerte außerhalb des eigenen Intervalls, bei 6.1 A4 S8 und '
      'A5 S5 außerhalb der Intervalle aus A5 S5 (%s s, %s cm, %s und %s), bei 6.1 A4 S7 außerhalb des g-Intervalls aus '
      'Tab. 3 (%s, %s). %s in 6.1 A3 S5 bezieht sich auf die Befunde der Metaanalysen, Kapitel 5 meidet das Wort '
      '„Effekt“ (Register 3c). 6.1 A4 S4 ist seit Rev. 163 kein Rückbezug mehr.' % (
          Q('vereinbar', '6.1 A4 S6'), Q('Das widerspricht', '6.1 A5 S4'), KI_CM, KI_SBJ,
          Q('−0,18 s außerhalb des eigenen Intervalls', ('tv61', '| A4 S8 |', '\n')),
          Q('+13,1 cm außerhalb von', ('tv61', '| A5 S5 |', '\n')), GKI_CM,
          Q('g 1,01, außerhalb des eigenen Intervalls', ('tv61', '| A4 S7 |', '\n')), Q('solche Effekte', '6.1 A3 S5')),
      'erfüllt (6.1 A4 S7 nur über Tab. 3)', '§ 2, § 3')

zeile('ausgangswerte', '6.1 A5 S8 und A6 S1: Ausgangswerte und Beanspruchung',
      'Fundstelle · Befund § 6.5 Nr. 10, F17 § 5.3 (Normwerteinordnung Standweitsprung), § 10 (Load-Sprachregelung), '
      'Register 10e',
      '6.1 A5 S8, A6 S1 · Tab. 2 (A1 S3), A3 S1',
      '6.1 A5 S8 stützt sich auf die Ausgangswerte im Standweitsprung (IG %s, KG %s cm, K-04.7), die nur Tab. 2 trägt '
      '(der Text nennt nur die Richtung, Register 10e). 6.1 A6 S1 übernimmt %s (A3 S1, vier Wörter, Bezeichnung) und '
      'ordnet %s (Median %s, K-10.13) als %s ein, ohne Load.' % (
          pz(sbj['prae_ig'], 0), pz(sbj['prae_kg'], 0), Q('als vollständig gemeldeten Einheiten', '6.1 A6 S1'),
          pz(cr10[1], 1), pz(cr10[3], 1), Q('leicht bis mäßig anstrengend', '6.1 A6 S1')),
      'erfüllt (6.1 A5 S8 nur über Tab. 2)', '§ 3, § 4')

zeile('schmerz', '6.1 A6 S2, S3: Schmerzmeldungen, Bezugsmenge der neun Spieler und Status (Fortsetzung 4 § 5 Nr. 4, '
                 'Punkte 2 und 3)',
      'Fundstelle · Register 2a (F17 § 3), Befund § 6.5 Nr. 10, TV5 § 10 Nr. 3 und Nr. 18, 2b.24, 2b.45',
      '6.1 A6 S2, S3 · A3 S3, Tab. H2',
      '(1) %s rechnet %d von %d (K-10.12, K-10.9). Die %d stehen mit Grund nur in der Anmerkung zu Tab. H2 (TV5 § 10 '
      'Nr. 18 %s), Kapitel 5 nennt die neun ohne Menge (A3 S3) und als Bezugsmenge sonst die %d Zugeteilten (A2 S1), mit '
      'ihnen wäre es genau die Hälfte. (2) %s sind %d von %d Meldungen (K-10.12), die Kapitel 5 nur als Rest nennt '
      '(%d − %d − %d). (3) 6.1 A6 S2 schreibt %s. Diese Wendung verwarf TV5 § 10 Nr. 3 für Kapitel 5, sie %s. Kapitel 5 '
      'schreibt für denselben Status %s (A2 S1, A3 S1), „durchgeführten“ nur bei den übrigen Status (%s). (4) %s in 6.1 '
      'A6 S3 sind %d von %d.' % (
          Q('Mehr als die Hälfte der Spieler mit Meldungen', '6.1 A6 S2'), ue[4], mit_meldung, mit_meldung,
          Q('die Zahl der meldenden Spieler steht in Tab. H2', ('tv5', '## 10 Zweitprüfung', '## 11')), zugeteilt,
          Q('überwiegend zu vollständig durchgeführten Einheiten', '6.1 A6 S2'), ue[1], ue[0], ue[0], ue[2], ue[3],
          Q('vollständig durchgeführten', '6.1 A6 S2'),
          Q('stellt die Selbstauskunft als Tatsache dar', ('tv5', '## 10 Zweitprüfung', '## 11')),
          Q('als vollständig gemeldeten', '5 A3 S1'), Q('zu nicht und zu teilweise durchgeführten Einheiten', '5 A3 S3'),
          Q('Einige', '6.1 A6 S3'), ue[2] + ue[3], ue[0]),
      'teilweise (Bezugsmenge und Status „ganz“ nur über Tab. H2 und Rechnung, Statuswort gegen TV5 § 10 Nr. 3, '
      'Schwere B)', '§ 3, § 6')

zeile('kg', '6.1 A6 S4, S5: Kontrollgruppe ohne Vergleichsdaten',
      'Fundstelle · Register c8, F17 § 5a „Nicht übernehmen“',
      '6.1 A6 S4, S5 · A3 S4',
      '6.1 A6 S4 nimmt A3 S4 ohne wörtliche Doppelung auf (%s, längste gemeinsame Folge ein Wort), 6.1 A6 S5 folgert '
      'daraus.' % Q('ohne Vergleichsdaten der Kontrollgruppe', '6.1 A6 S4'),
      'erfüllt (Register c8)', '§ 4')

zeile('bezugsmengen', 'Bezugsmengen 31, 26, 18 und 16: 4.2, 4.7 und A1 S2, A2 S1',
      'Fundstelle · Register 2a, 2b, 2g (F17 § 3)',
      '4.2 A1 S4, S5, 4.7 A1 S1 · A1 S2, A2 S1',
      '31 steht nur in A1 S2, Kapitel 4 nennt keine Spielerzahl der Menge zur Eingangstestung angetreten (31, 18 und 13 '
      'als Spielerzahl in 4.1 bis 4.7 nicht vorhanden). 26 in %s und A1 S2, %s und %s ohne wörtliche Doppelung. Die 18 '
      'in A2 S1 (K-10.4) ist als Nenner der Umsetzung gekennzeichnet (%s, 4.7 A1 S1), 4.2 A1 S5 nennt für die IG 16 '
      'Analysierte.' % (
          Q('Analysiert wurden N = 26 Spieler.', '4.2 A1 S4'), Q('Analysiert wurden', '4.2 A1 S4'),
          Q('in die Analyse ein', '5 A1 S2'), Q('alle zugeteilten Spieler', '4.7 A1 S1')),
      'erfüllt (18 als Ausnahme nach Register 2g)', '§ 5')

zeile('planmaessig', '„planmäßig“ in A1 S1 gegen die Termine in 4.1',
      'Fundstelle · Register 8a, TV5 § 10 Nr. 12',
      '4.1 A5 S6 · A1 S1',
      '%s (4.1 A5 S6) steht neben %s (A1 S1). Die Zweitprüfung von Textvorschlag 5 sah die Spannung (§ 10 Nr. 12), '
      'entschieden ist „planmäßig“ nach dem Klick zu Rasterzeile 5.1.4, das Wort %s.' % (
          Q('Testtermine lagen teils außerhalb des geplanten Zeitfensters.', '4.1 A5 S6'),
          Q('bis zum planmäßigen Studienende', '5 A1 S1'),
          Q('bezieht sich auf das Studienende, nicht auf die Termine', ('tv5', '## 10 Zweitprüfung', '## 11'))),
      'erfüllt (verschiedener Bezug, Register 8a)', '§ 6')

zeile('analyseset', 'Analyseset und Programmwoche: Begriffe ohne Einführung in Kapitel 4',
      'Fundstelle · TV5 § 9.1 Nr. 4 und § 10 Nr. 19, Raster 5.1.5, F17 § 3.2',
      'A1 S3, A2 S4 · 4.7 A1 S1, 4.5.1',
      '%s steht nur in A1 S3 (Raster 5.1.5 %s), Kapitel 4 beschreibt dieselbe Menge ohne Namen (4.7 A1 S1 %s). %s steht '
      'nur in A2 S4 (F17 § 3.2), 4.5.1 zählt Wochen. TV5 § 9.1 Nr. 4 hält beide für %s, vorgemerkt ist dort nur die '
      'Begriffsbrücke zur Adhärenz ({{adhaerenz}}).' % (
          Q('Analyseset', '5 A1 S3'), Q('Analyseset je Zielgröße', 'raster'),
          Q('je Zielgröße mit vollständigen Prä- und Post-Werten und Reifestatus', '4.7 A1 S1'),
          Q('Programmwoche', '5 A2 S4'), Q('aus dem Zusammenhang verständlich', ('tv5', '**9.1 Kapitel 4**', '**9.2'))),
      'erfüllt (aus dem Zusammenhang verständlich nach TV5 § 9.1 Nr. 4, ohne Handlungsbedarf)', '§ 6')

PRUEF(wocap == (9.0, 2.0) and (kz('K-10.11', 2), kz('K-10.11', 3)) == (9.0, 1.0), 'K-10.11')
PRUEF('neun und zwei Spieler' in T('5 A2 S4') and 'neun und einer' in T('5 A2 S4'), 'Untergrenzen in A2 S4')
zeile('untergrenzen', 'Untergrenzen und Einheitennummer: 4.6 A2 S2, S3 gegen A2 S4',
      'Fundstelle · Raster 4.6.3, 5.1.6, F17 § 3.2, S4a 6.3.2 G6-b, TV5 § 9.1 Nr. 3',
      '4.6 A2 S2, S3 · A2 S4',
      'A2 S4 nennt zwei Zählregeln, die Kapitel 4 nicht einführt (%s, %s, K-10.11: %d und %d, %d und %d Spieler). '
      '4.6 A2 S2 und S3 legen die Zählung fest (%s, %s), Raster 4.6.3 ebenso, ohne Untergrenzen. Raster 5.1.6 verlangt '
      'sie im Ergebnis (%s), F17 § 3.2 nennt den Grund (%s), S4a plant ihn für 6.3 (6.3.2 G6-b %s). Ohne diesen Grund '
      'kann %s neben 4.6 A2 S3 als Widerspruch gelesen werden. Ein Halbsatz in 4.6 wäre eine Folgeänderung %s (TV5 § 9.1 '
      'Nr. 3), also nur mit Kürzung.' % (
          Q('mit höchstens zwei Meldungen je Programmwoche', '5 A2 S4'),
          Q('nach verschiedenen Einheitennummern', '5 A2 S4'), wocap[0], wocap[1], kz('K-10.11', 2), kz('K-10.11', 3),
          Q('Gezählt wurde je Meldung.', '4.6 A2 S2'), Q('Die Einheitennummer diente nicht als Identitätsmerkmal.',
                                                         '4.6 A2 S3'),
          Q('Untergrenzen wochengedeckelt und nach distinkten Nummern', 'raster'),
          Q('Die Einheitennummer (H003) ist kein Identitätsmerkmal', 'f17'),
          Q('Untergrenzen nennt Kapitel 5, hier nur der Grund', 's4a'),
          Q('nach verschiedenen Einheitennummern', '5 A2 S4'),
          Q('im Rahmen des Budgets 725 des Abschnitts 4.5 (722)', ('tv5', '**9.1 Kapitel 4**', '**9.2'))),
      'teilweise (Zählregeln der Untergrenzen ohne Einführung in Kapitel 4, Grund erst in 6.3, Schwere C, Folgeänderung '
      'für 4.6 als mögliche Klickfrage beim Abschluss)', '§ 6')

zeile('versuche', 'Versuche und Messgüte: 4.4 und A4',
      'Fundstelle · F17 § 10 (Versuchszahl-Sprachregelung), Raster 5.1.9, F17 § 5a „Nicht übernehmen“, TV5 § 9.1 Nr. 5',
      '4.4 A2 S1 bis S4, A3 S1, S2 · A4 S1, S2',
      '%s und %s in A4 S2 wie in 4.4 A2 S4 (vier Wörter gleich, Bezeichnung), Tab. H1 seit 4.4 A2 S3 eingeführt, in '
      'A4 S2 Wiederaufruf. A4 S1 knüpft mit %s an %s (4.4 A3 S2) an, gemeinsam vier Wörter, neue Aussage zur '
      'Abschlusstestung (TE post über dem SESOI in allen sieben Zielgrößen, K-05), 4.4 nennt den Zeitpunkt nicht. 4.4 A3 '
      'S1 führt %s ein und nutzt in 4.4 A3 S2 die Abkürzung, A4 S1 schreibt die Langform, nach TV5 § 9.1 Nr. 5 %s.' % (
          Q('gültigen Versuche', '4.4 A2 S4'), Q('beim 505-Test je Seite', '5 A4 S2'),
          Q('auch bei der Abschlusstestung', '5 A4 S1'), Q('Der TE überstieg bei allen Zielgrößen den SESOI',
                                                            '4.4 A3 S2'),
          Q('typischen Messfehler (TE)', '4.4 A3 S1'),
          Q('Kein Handlungsbedarf, zur Kenntnis', ('tv5', '**9.1 Kapitel 4**', '**9.2'))),
      'erfüllt (Langform ohne Handlungsbedarf nach TV5 § 9.1 Nr. 5)', '§ 3, § 4, § 6')

zeile('zielgroesse', 'Ausgangswerte, Kovariaten und Umfang von „Zielgröße“: 4.1 A4 S2, S3, 4.4.2 A1 S6, 4.7 A3 S1, '
                     'A4 S3 gegen A1 S3, A4 S1, A5 S1, S2, S6',
      'Fundstelle · TV 4.7 Nr. 43 und Zeile 4.7.5, F17 § 5.3 (Tab. 1 und Tab. 2), Raster 5.1.5',
      '4.1 A4 S2, S3, 4.4 A3 S1, 4.4.2 A1 S6, 4.7 A3 S1, A4 S3 · A1 S3, A4 S1, A5 S1, S2, S4, S6',
      '(1) %s (A1 S3) führt Kapitel 4 nicht ein, 4.7 nennt nur Hedges\' g. Den Satz mit d in 4.7 strich TV 4.7 Nr. 43 '
      '(%s), die Definition steht nach Zeile 4.7.5 in der Anmerkung zu Tab. 2 (%s, Task 18). (2) %s in A1 S3 wie in 4.7 '
      'A4 S3, %s in A5 S4 wie in 4.1 A4 S3. (3) „Zielgröße“ hat in Kapitel 4 wechselnden Umfang: Tab. 1 führt %s (F17 '
      '§ 5.3), darauf beziehen sich A4 S1 und 4.4 A3 S1 und S2. Drei konfirmatorische meinen A5 S1, S6 und 4.7 A3 S1, '
      'beim 505-Test ist nach 4.4.2 A1 S6 nur das Seitenmittel Zielgröße (%s), 4.1 A4 S2 nennt fünf abhängige Variablen. '
      'Kapitel 5 folgt 4.4 A3 und 4.7, die Spannung liegt in 4.4.2 A1 S6.' % (
          Q('standardisierter Differenz d', '5 A1 S3'),
          Q('berichtet wird die standardisierte Differenz d', ('tv47', '43. [ÄNDERN]', '\n')),
          Q('Definition in der Anmerkung zu Tab. 2', ('tv47', '| 4.7.5 |', '\n')),
          Q('Überlappung der Kovariaten', '5 A1 S3'), Q('Ausgangswert und Reifestatus', '5 A5 S4'),
          Q('sieben Zielgrößen', ('f17', '| Tab. 1 Messgüte je Zielgröße |', '\n')),
          Q('Zielgröße war das Mittel der beiden Seiten-Bestwerte', '4.4.2 A1 S6')),
      'teilweise (Umfang von „Zielgröße“ in 4.4.2 A1 S6 gegen Tab. 1, Schwere C, Vormerkung für die Endredaktion), '
      'd und Überlappung erfüllt', '§ 6')

zeile('folge', 'Folge der Zielgrößen über Kapitel 4, 5 und 6.1 (Fortsetzung 4 § 5 Nr. 4, Punkt 4)',
      'Fundstelle und Korpus · F17 § 5.1 (Reihenfolgetreue), Befund § 6.5 Nr. 3, 2b.8 · 2d.19',
      'alle Sätze mit mindestens zwei von Sprint, Richtungswechsel und Sprung',
      '%d Sätze nennen mindestens zwei der drei, %d in der festen Folge Sprint, Richtungswechsel, Sprung (acht Sätze der '
      'Einleitung, 4.1 A4 S2, 4.7 A3 S1, 6.1 A1 S1, in Kapitel 5 A5 S5 im Anschluss an A5 S4 und A5 S11). F17 § 5.1: %s. '
      'Abweichend in Kapitel 5 ist A4 S2, nach der Gruppe mit mehr gültigen Versuchen geordnet (2b.8). Außerhalb der '
      'Regel stehen B2 S9 (Kontrast der Vorstudie), 4.3 A5 S3 (Testfolge), 4.7 A1 S5 (Grund der Festlegung) und 6.1 A3 '
      'S6, das Fähigkeiten aufzählt, die ein Programm ansprechen dürfte, nicht die Zielgrößen (%s). Korpus: Eine nach dem '
      'Inhalt geordnete Folge in einem Satz hat ein Kernvorbild (Negra 2019 2.3, 2d.19), ein Potenzial für A4 S2 stützt '
      'sich auf F17 § 5.1. Die geplante G5-Zeile übernimmt die Folge von A4 S2 (S4a 6.2.6 b).' % (
          len(FOLGE), len(GEHALTEN),
          Q('Sprint → Richtungswechsel → Sprung in den Hypothesen, den Ergebnissen und der Diskussion identisch', 'f17'),
          Q('Sprung, Beschleunigung und Richtungswechsel', '6.1 A3 S6')),
      'teilweise (A4 S2 gegen den Wortlaut von F17 § 5.1, Schwere B, keine Entscheidung), Korpus: Ordnung nach dem '
      'Inhalt mit Kernvorbild (2d.19)', '§ 7')

beteiligung = kz('K-10.6', 1) * 100
PRUEF(pz(beteiligung, 1) == '45,4' and '45,4 %' in T('5 A2 S2'), '45,4 % aus K-10.6')
zeile('adhaerenz', 'Umsetzung, Adhärenz und Status: 4.6, 4.7 und 4.1 gegen A2 und 6.1 (Fortsetzung 4 § 5 Nr. 4, '
                   'Punkt 5)',
      'Fundstelle und Korpus · Raster 4.6.3, 5.1.6, TV5 § 9.1 Nr. 3 und 4, Register 10s, 10u, F17 § 3.2 · 2d.20',
      'Überschrift 4.6, 4.6 A2 S1, S4, 4.7 A1 S1 bis S3, S6, 4.1 A5 S9 · A2 S1 bis S3 · 6.1 A2 S2, S4, S5, A4 S9',
      '(1) %s steht %d-mal in 4.6 und in dessen Überschrift, %d-mal in 4.7 (auch als Wortteil), einmal in 4.1, nicht in '
      'Kapitel 5 und 6.1. %s (A2 S1) ist die mediane Adhärenz im Sinn von 4.6 A2 S1 (Zahl der Meldungen mit dem Status '
      '%s je Spieler, K-10.8), A2 S3 nennt die Schwellen von 4.7 A1 S2 und S3 ohne das Wort. (2) %s (A2 S2, Raster '
      '5.1.6) und %s (6.1) führt Kapitel 4 nicht ein, A2 S2 bestimmt die Rate im Satz. (3) Status: 4.6 %s und %s, '
      'Kapitel 5 %s, %s und %s (A2 S1). (4) %s (4.6 A2 S4) meidet Kapitel 5 nach Register 10s, die %s %% in A2 S2 '
      'umfassen beide Status (K-10.6). (5) Nenner %s in A2 S2 wie in 4.6 A2 S1 (Bezugsmengen-Regel). Korpus: kein '
      '„adherence“ für einen Wert je Spieler, am nächsten „x out of a possible N“ (2d.20). Ort einer Begriffsbrücke wäre '
      'neben 4.6 und A2 S1 der Titel von Tab. H2 (Platzhalter %s, Task 18).' % (
          Q('Adhärenz', '4.6 A2 S1'), zb('Adhärenz', '4.6'), zb('Adhärenz', '4.7'),
          Q('im Median 6,0 vollständige je Spieler', '5 A2 S1'), Q('ganz', '4.6 A2 S1'),
          Q('Umsetzungsrate', '5 A2 S2'), Q('Umsetzung', '6.1 A4 S9'), Q('ganz', '4.6 A2 S1'),
          Q('teilweise', '4.6 A2 S4'), Q('als vollständig', '5 A2 S1'), Q('als teilweise', '5 A2 S1'),
          Q('als nicht durchgeführt', '5 A2 S1'), Q('Beteiligung', '4.6 A2 S4'), pz(beteiligung, 1),
          Q('bei zwölf angebotenen Einheiten', '4.6 A2 S1'), Q('Adhärenz je Spieler', 'Anhang H A2 S1')),
      'teilweise (Begriffsbrücke Adhärenz offen, Register 10u, TV5 § 9.1 Nr. 4, Status „ganz“ gegen „vollständig“, '
      'Schwere C), „Beteiligung“ bewusst anders · Register 10s, Korpus: kein Vorbild für einen Wert je Spieler (2d.20)',
      '§ 6')

PRUEF('H007' in BEZ['K-10.12'], 'Item H007 in K-10.12')
zeile('beanspruchung', 'Beanspruchung, Load und Schmerzen: 4.6 und A3',
      'Fundstelle · F17 § 10 (Load-Sprachregelung), Register 3f, Raster 4.6.1, 4.6.7, 4.6.8, 5.1.7, 5.1.8, TV5 § 9.6 '
      'Nr. 5',
      '4.6 A1 S2, S3, S6, S8, S9 · A3 S1 bis S4',
      '%s, %s, %s und %s wie 4.6. A3 S2 %s nimmt die Definition aus 4.6 A1 S8 knapp auf (%s), nicht wörtlich, und hält '
      'die Load-Sprachregelung ein (F17 § 10 %s). %s steht erstmals in A3 S2, im Text nicht aufgelöst (TV5 § 9.6 Nr. 5 '
      '%s). 4.6 A1 S3 nennt %s, Kapitel 5 und 6.1 %s (Item H007, K-10.12), der Wortlaut des Items steht im Fragebogen '
      '(Anhang A). A3 S4 und 4.6 A1 S2 tragen dieselbe Tatsache aus Plan und Ergebnis, nicht wörtlich, wie Raster 5.1.8 '
      'es verlangt (%s, CONSORT 19).' % (
          Q('Beanspruchung', '4.6 A1 S6'), Q('CR-10-Skala', '4.6 A1 S6'), Q('sRPE-Load', '4.6 A1 S8'),
          Q('Solldauer', '4.6 A1 S8'), Q('Der mit der Solldauer berechnete sRPE-Load', '5 A3 S2'),
          Q('das Produkt aus CR-10-Wert und Solldauer der Einheit', '4.6 A1 S8'),
          Q('Der sRPE-Load ist CR-10 mal Solldauer.', 'f17'), Q('AU', '5 A3 S2'),
          Q('Abkürzungsverzeichnis: AU (A3)', ('tv5', '**9.6 Task 16 bis 18', '**9.7')), Q('Schmerzen', '4.6 A1 S3'),
          Q('Schmerzen oder Probleme', '5 A3 S3'), Q('Kontrollgruppe ohne Erfassungsinstrument', 'raster')),
      'teilweise („Schmerzen“ in 4.6 A1 S3 gegen „Schmerzen oder Probleme“, Schwere C, Vormerkung 4.6), AU über das '
      'Abkürzungsverzeichnis vorgemerkt', '§ 4, § 6')

zeile('analyse', 'Analyse, Berichtsgrößen, Voraussetzungen und Sensitivität: 4.7 und A5, A6',
      'Fundstelle · F17 § 10 (ANCOVA-Sprachregelung), § 11.9, Register 6g, 10m, 10t, c4, Raster 4.7.4, 4.7.10 bis '
      '4.7.12, 5.2.1, 5.2.3, 5.2.4',
      '4.7 A3 S1 bis S5, A4 S1 bis S4, A5 S1, S2 · A5 S1 bis S5, A6 S1 bis S4',
      'Zielgrößen wie 4.7 A3 S1 (%s), dazu %s, %s, %s, %s, %s (c4), %s (Register 10t) und %s wie 4.7. %s grenzt die '
      'grafisch geprüfte Linearität (4.7 A4 S2) aus (Register 10m). Abweichende Wörter ohne Folge: 4.7 %s und %s, '
      'Kapitel 5 %s · A5 S1 %s, A5 S2 %s (4.7 A1 S6 %s). A5 S1 nimmt 4.7 A3 S4 als Objektsatz auf, nicht wörtlich.' % (
          Q('30-m-Sprint, 505-Seitenmittel, Standweitsprung', '4.7 A3 S1'), Q('Ausgangswert und Reifestatus',
                                                                              '5 A5 S4'),
          Q("Hedges' g", '4.7 A3 S5'), Q('Shapiro-Wilk-Test', '5 A6 S1'),
          Q('Bootstrap-Konfidenzintervall der adjustierten Differenz', '5 A6 S2'), Q('nachträglich', '5 A6 S2'),
          Q('sechs Sensitivitätsanalysen', '5 A6 S4'), Q('beobachtende Per-Protokoll-Vergleich', '5 A6 S4'),
          Q('mit Tests geprüften Voraussetzungen', '5 A6 S3'), Q('Modellannahmen', '4.7 A4 S1'),
          Q('Voraussetzungsprüfung', '4.7 A6 S3'), Q('Voraussetzungen', '5 A6 S3'), Q('Post-Wert', '5 A5 S1'),
          Q('Abschlusswert', '5 A5 S2'), Q('Abschlusswerte', '4.7 A1 S6')),
      'erfüllt', '§ 4, § 6')

abk = DOK['tv5'][DOK['tv5'].find('5. Abkürzungsverzeichnis:'):]
abk = abk[:abk.find('\n')]
PRUEF('AU (A3)' in abk and 'H0' not in abk, 'Abkürzungsliste TV5 § 9.6 Nr. 5 ohne H0')
zeile('schlusslogik', 'Schlusslogik: 4.7 A3 S6, S8 gegen A5 S6 bis S10 und 6.1 A1 S5, S6 (Fortsetzung 4 § 5 Nr. 4, '
                      'Punkt 6)',
      'Fundstelle und Korpus (mit Volltext) · F17 § 11.2b, Umfangsdokument § 5.1, Register 3c, 4a, 6f, TV5 § 9.6 Nr. 5 '
      '· Abgleichbefund § 3.4 (Lesart der Methodenteile), 2d.3, 2d.4',
      '4.7 A3 S6, S8 · A5 S6 bis S10 · 6.1 A1 S5, S6',
      '%s (A5 S6) entspricht %s, %s (A5 S7) entspricht %s und %s (4.7 A3 S6). %s (A5 S8, A6 S4, 6.1 A1 S6) führt 4.7 '
      'nicht ein, die Lesart trägt A5 S7 unmittelbar davor, im Umfangsdokument ist es das Urteil des Falls C1 (%s). Im '
      'Korpus definieren die MBI-Studien ihr Urteil „unclear“ im Methodenteil als %s (Abgleichbefund § 3.4, Lesart der '
      'Methodenteile, 2d.3, 2d.4), hier steht es erst in Kapitel 5. A5 S9 nimmt 4.7 A3 S8 in dessen Sprache auf '
      '(Register 6f). 4.7 A3 S8 schreibt %s ohne Einführung, Einleitung (B5 S3), Kapitel 5 und 6.1 schreiben '
      '„Nullhypothese“, die Abkürzungsliste in TV5 § 9.6 Nr. 5 führt „H0“ nicht. Neu vorzumerken: „H0“ in 4.7 A3 S8 '
      'ausschreiben oder in das Abkürzungsverzeichnis aufnehmen.' % (
          Q('nachweisbar', '5 A5 S6'), Q('Nachweisbarkeit', '4.7 A3 S6'),
          Q('relevanten Unterschieden in beide Richtungen', '5 A5 S7'), Q('Relevanz', '4.7 A3 S6'),
          Q('mit null und dem SESOI in beide Richtungen', '4.7 A3 S6'), Q('unschlüssig', '5 A5 S8'),
          Q('Der Befund ist unschlüssig.', 'umfang'),
          Q('ein 90-%-Intervall über beide Schwellen von ± 0,2 SD', ('abgleich', '**Lesart der Methodenteile.**',
                                                                     '**Zweitprüfung.**')),
          Q('H0', '4.7 A3 S8')),
      'teilweise („unschlüssig“ und „H0“ in 4.7 nicht eingeführt, Schwere C, neue Vormerkung zu 4.7 A3 S8), Korpus: '
      'Urteil im Methodenteil definiert (2d.3, 2d.4), im Übrigen erfüllt', '§ 4, § 6')

zeile('deskriptiv', 'Deskriptive Zielgrößen: A5 S11 gegen 4.7 A1 S5 und 4.4.1 A1 S5',
      'Fundstelle · Raster 4.7.6, 5.2.5, F17 § 5a „Nicht übernehmen“, TV5 § 9.1 Nr. 2, K-11.4',
      'A5 S11 · 4.7 A1 S5, 4.4.1 A1 S5',
      'Namen wie 4.7 A1 S5 (%s, fünf Wörter gleich, %s). A5 S11 wiederholt die Regel (%s gegen %s) nicht wörtlich, mit '
      'dem Wiederaufruf von Tab. H3. Den Satz verlangt Raster 5.2.5 (%s), der Grund steht in 4.7 A1 S5 und 4.4.1 A1 S5 '
      '(10-m-Zeit von Verein B). A5 S11 nennt keinen Befund, für Schritt 3 als mögliche Kürzung vorgemerkt. 4.4.1 A1 S5 '
      'nennt als Ursache %s, K-11.4 führt die %d fehlenden 10-m-Zeilen der IG bei der Abschlusstestung aber als „falsch '
      'aufgenommen“ (technischer Ausfall %d), offen nach TV5 § 9.1 Nr. 2 (%s). Kapitel 5 nennt keine Kategorie und ist '
      'nicht berührt.' % (
          Q('die 5- und 10-m-Sprintzeiten und', '4.7 A1 S5'), Q('505-Seitenwerte', '4.7 A1 S5'),
          Q('Beschreibend berichtet werden', '4.7 A1 S5'), Q('wurden nur beschrieben', '5 A5 S11'),
          Q('ein Satz im Text. Ohne p und ohne Effektstärke, Grund in 4.7', 'raster'),
          Q('wegen eines Lichtschrankenausfalls', '4.4.1 A1 S5'), falsch_z10, tech_z10,
          Q('Der Verfasser klärt, was geschah.', ('tv5', '**9.1 Kapitel 4**', '**9.2'))),
      'erfüllt (Inhalt der Regel wiederholt, Ort nach Raster 5.2.5), Ausfallgrund in 4.4.1 A1 S5 offen nach TV5 § 9.1 '
      'Nr. 2', '§ 4')

zeile('antragskriterium', 'Antragskriterium: A2 S3 gegen 4.6 A2 S5, 4.7 A1 S2 und 4.1 A5 S9',
      'Fundstelle · TV5 § 9.1 Nr. 5, Raster 4.6.4, 4.7.6, Register 9c, 6k',
      'A2 S3 · 4.6 A2 S5, 4.7 A1 S2, 4.1 A5 S9',
      '%s (A2 S3) und %s (4.7 A1 S2): dieselbe Zahl als Ergebnis und als Grund der Festlegung, nicht wörtlich (TV5 '
      '§ 9.1 Nr. 5 %s, Raster 4.7.6 %s). %s (4.6 A2 S5) entspricht %s (4.7 A1 S2), 4.1 A5 S9 nennt die Nichtanwendung '
      'in der Hauptanalyse. Die Quelle des Kriteriums nennt nur 4.6 A2 S5 („Ethikantrag“), 4.7 A1 S2 und Kapitel 5 '
      'nennen keine (Register 6k, Kapitel 4 nicht gebunden).' % (
          Q('drei mindestens neun Einheiten', '5 A2 S3'), Q('da es nur drei Spieler erreichten', '4.7 A1 S2'),
          Q('beide Stellen sind nötig', ('tv5', '**9.1 Kapitel 4**', '**9.2')),
          Q('Antragskriterium ≥ 75 % nur deskriptiv (n = 3)', 'raster'), Q('mindestens 75 %', '4.6 A2 S5'),
          Q('mindestens neun von zwölf Einheiten', '4.7 A1 S2')),
      'erfüllt', '§ 6')

zeile('einleitung', 'Einleitung: Ankersatz, Hypothesen und 10-m-Erwartung',
      'Fundstelle · TV5 § 9.2 Nr. 1 bis 4, Nachtrag 6.1 § 11 Nr. 6, Teil 0 Rev. 134 (Einleitung pausiert)',
      'B1a S5, B5 S1, S3, S4 · A5 S6 bis S11',
      'B5 S3 spricht von %s, A5 S10 entscheidet an der adjustierten Differenz im Post-Wert (TV5 § 9.2 Nr. 1 %s). B5 S4 '
      'sagt %s, Kapitel 4, 5 und 6.1 „Zielgröße“ (TV5 § 9.2 Nr. 2). B1a S5 hebt %s hervor, A5 S11 beschreibt sie nur '
      '(TV5 § 9.2 Nr. 3 %s), Kapitel 5 kündigt keine Prüfung an. Denselben Satz B1a S5 setzt 6.1 seit Stufe 3 voraus, '
      'der Nachtrag zu 6.1 verlangt, ihn in der Schlussfassung zu halten (§ 11 Nr. 6 a %s). Den Ankersatz B5 S1 '
      'beantworten A5 S6 bis S8, 6.1 A1 S1 wiederholt ihn. Die Einleitung ist bis zur Schlussfassung pausiert.' % (
          Q('Veränderungen', 'B5 S3'), Q('Rechnerisch ist es dieselbe Gruppendifferenz', ('tv5', '**9.2', '**9.3')),
          Q('in mindestens einem der drei gleichrangigen Parameter', 'B5 S4'), Q('die 10-m-Zeit', 'B1a S5'),
          Q('Die Arbeit kann diese Erwartung nicht prüfen', ('tv5', '**9.2', '**9.3')),
          Q('Den Satz zu Programmen bis sieben Wochen (Absatz 1, Satz 5, Ramirez-Campillo et al., 2020) halten',
            ('nachtrag61', '6. **Schlussfassung der Einleitung (G35):**', '\n'))),
      'teilweise („Parameter“ in B5 S4, Schwere C, Entscheidung in der Schlussfassung), Kapitel 5 erfüllt', '§ 6')

zeile('anhangH', 'Anhang H: Platzhalter mit Bezug auf Kapitel 5',
      'Fundstelle · TV5 § 9.6 Nr. 4, Register 10t, V8, U6, F17 § 10 (Load-Sprachregelung), § 13 Nr. 8',
      'Anhang H A2 S1 bis A5 S1 (Platzhalter Tab. H2 bis Tab. H5)',
      '%s und %s nennen nach Gliederung v6 (E3, M28) entfallene Unterabschnitte, Tab. H4 %s zählt anders als 4.7 A5 S1 '
      '(sechs Sensitivitätsanalysen, Per-Protokoll gesondert), dem A6 S4 folgt, Tab. H5 %s, Erstverweis jetzt A2 S3. '
      'Dazu nennt Tab. H2 %s, A3 S2 und die Load-Sprachregelung %s. Tab. H3 nennt nur deskriptive Zielgrößen, A1 S3 '
      'verweist dorthin auch für %s. Tab. H4 heißt %s, A6 S3 verweist dorthin für die Voraussetzungen. %s ersetzte F17 '
      '§ 13 Nr. 8 durch das Bootstrap-Intervall für alle drei Zielgrößen (%s). Task 18: Die Titel von Tab. H3 und Tab. '
      'H4 müssen tragen, wofür A1 S3 und A6 S3 auf sie verweisen. TV5 § 9.6 Nr. 4: %s' % (
          Q('(aus 5.1)', 'Anhang H A2 S1'), Q('(aus 5.2)', 'Anhang H A3 S1'),
          Q('acht vorab festgelegte Varianten und Gegenprobe 30 m', 'Anhang H A4 S1'), Q('(aus 4.7)', 'Anhang H A5 S1'),
          Q('sRPE-Belastung', 'Anhang H A2 S1'), Q_LOAD,
          Q('die Ausgangswerte aller eingangsgetesteten Spieler', '5 A1 S3'),
          Q('Sensitivitätsanalysen', 'Anhang H A4 S1'), Q('Gegenprobe 30 m', 'Anhang H A4 S1'),
          Q('statt einer verteilungsfreien Gegenprobe nur beim 30-m-Sprint', 'f17'),
          Q('Task 18 ersetzt die Platzhalter durch die Objekte.', ('tv5', '**9.6 Task 16 bis 18', '**9.7'))),
      'nicht erfüllt (Platzhalter veraltet, Schwere C, vorgemerkt für Task 18, TV5 § 9.6 Nr. 4)', '§ 5')

zeile('spaeter', 'Spätere Teile: 6.2 mit 6.3, Kapitel 7, Zusammenfassung und Abstract',
      'Fundstelle · TV5 § 8 Nr. 3, § 9.4, § 9.5, Raster 7.1, 7.2, S4a (Task 12b), Register V8',
      'im Master ohne Text (6.2, 6.3 und 7 nur Überschriften, Zusammenfassung und Abstract nur Titel)',
      'Geplant nach S4a für 6.2 und 6.3: G1 mit der verworfenen Normalverteilung und dem Bootstrap als Halbsatz (6.2.5 a '
      '%s), G5 mit der Folge der gültigen Versuche wie A4 S2 (6.2.6 b %s, mit der seit Gliederung v6 entfallenen '
      'Abschnittsbezeichnung „(5.1)“, Register V8), G6 mit dem Grund der Untergrenzen (6.3.2 G6-b %s), dazu V06 '
      '(Schmerzen und Abbrüche, A3 S3), V42 (fehlende Vergleichsdaten der Kontrollgruppe, A3 S4) und V73 (zusätzliche '
      'Ausfälle der Kontrollgruppe, A1 S1 mit Abb. 1). Kapitel 7 antwortet nach Raster 7.1 in der Reihenfolge der '
      'Zielgrößen mit der Nullbefund-Sprachregelung (A5 S6 bis S10) und nennt nach Raster 7.2 Umsetzungsrate und '
      'Belastungsverträglichkeit (A2 S2, A3 S3), nach TV5 § 8 Nr. 3 %s, S4a K7-a merkt die Forschungsempfehlung zur '
      'Umsetzung vor. Die Zusammenfassung übernimmt den %s und die Umsetzungsrate mit Bezugsmenge (TV5 § 9.5). Eine '
      'Änderung von A1 S1, A2 S2, A2 S4, A3 S3, A3 S4, A4 S2, A5 S6 bis S10, A6 S1 oder A6 S2 berührt diese '
      'Planung.' % (
          Q('W und p stehen in Kapitel 5', 's4a'),
          Q('Mechanismen nennt 4.4, die Richtung Kapitel 5 (5.1), hier nur die Folge', 's4a'),
          Q('Untergrenzen nennt Kapitel 5, hier nur der Grund', 's4a'),
          Q('können nur Zahl und Status der Meldungen nennen', ('tv5', '**Nr. 3 — Lokalisation', '**Nr. 4')),
          Q('Hauptbefund im Wortlaut von Kapitel 5', ('tv5', '**9.5', '**9.6'))),
      'erfüllt (am Master gegenstandslos, Abhängigkeiten vermerkt)', '§ 8')

# ---------------------------------------------------------------- Nummern und Satzkennungen
NUMMER = OrderedDict((k, '2e.%d' % (n + 1)) for n, k in enumerate(ZEILEN))
for k, z in ZEILEN.items():
    z['Nr.'] = NUMMER[k]
    for sp in list(z.keys()):
        z[sp] = re.sub(r'\{\{(\w+)\}\}', lambda m: NUMMER[m.group(1)], z[sp])
        PRUEF('{{' not in z[sp] and '}}' not in z[sp], 'Querverweis aufgelöst in %s' % k)

ABSCHNITTE = set(SATZ[i]['abschnitt'] for i in SATZ)
ID_RX = re.compile(r'(?:(?P<pre>\d+(?:\.\d+)*|Anhang [A-H]) )?(?P<id>A\d+ S\d+)|(?P<einl>B\d[ab]? S\d+)')
LUECKE = re.compile(r'(?:(?:, | und | bis | oder | sowie )S\d+)*(?:, | und | bis | oder | sowie )')
HISTORISCH = re.compile(r'(?:bisherigen?|bis Rev\. 162) $')


def ohne_zitate(t):
    alt = None
    while alt != t:
        alt = t
        t = re.sub(r'„[^„“]*“', '„…“', t)
    return t


def kennungen(t):
    t = ohne_zitate(t)
    out = []
    ende, abschnitt = 0, None
    for m in ID_RX.finditer(t):
        if m.group('einl'):
            kenn = m.group('einl')
            PRUEF(kenn in SATZ, 'Satzkennung %s im Master' % kenn)
            out.append(kenn)
            ende, abschnitt = m.end(), None
            continue
        pre = m.group('pre') if m.group('pre') in ABSCHNITTE else None
        if pre:
            ab = pre
        elif abschnitt and LUECKE.fullmatch(t[ende:m.start()]):
            ab = abschnitt
        else:
            ab = '5'
        kenn = '%s %s' % (ab, m.group('id'))
        if HISTORISCH.search(t[:m.start()]):
            out.append(kenn + ' (bis Rev. 162)')
        else:
            PRUEF(kenn in SATZ, 'Satzkennung %s im Master (Text: …%s…)' % (kenn, t[max(0, m.start() - 40):m.end()]))
            out.append(kenn)
        ende, abschnitt = m.end(), ab
    return out


KENNUNGEN = OrderedDict()
for k, z in ZEILEN.items():
    ks = []
    for sp in ('Prüfgegenstand', 'Befundstelle', 'Fundstelle im Text', 'Ergebnis', 'Status'):
        ks += kennungen(z[sp])
    KENNUNGEN[z['Nr.']] = ks

# ---------------------------------------------------------------- Zitatprüfung
aus('')
aus('§ 9 Satzkennungen und Zitate der Teiltabelle')
aus('  Satzkennungen je Zeile, aufgelöst (ohne Präfix Kapitel 5, Aufzählungen erben das Präfix ihres ersten Glieds), '
    'jede im Master vorhanden:')
for nr, ks in KENNUNGEN.items():
    aus('  %s: %s' % (nr, ', '.join(ks) if ks else '—'))
for z, ort in ZITATE:
    PRUEF(zitat_ok(z, aufloesen(ort)), 'Zitat %r am Ort %r' % (z, ort))
ORTE = OrderedDict()
for z, ort in ZITATE:
    k = ort if isinstance(ort, str) else ort[0] + ' ' + ort[1].strip('*# ')
    ORTE[k] = ORTE.get(k, 0) + 1
aus('  %d Zitate am genannten Ort an Wortgrenzen gefunden, Bruchstücke in ihrer Folge · Orte: %s' % (
    len(ZITATE), ' · '.join('%s %d' % (k, v) for k, v in ORTE.items())))

# ---------------------------------------------------------------- Zählung
aus('')
aus('§ 10 Zählung der Teiltabelle 2e')
STATUS = OrderedDict([('erfüllt', 0), ('teilweise', 0), ('nicht erfüllt', 0), ('bewusst anders', 0)])
for z in ZEILEN.values():
    s = z['Status']
    for k in ('nicht erfüllt', 'teilweise', 'erfüllt', 'bewusst anders'):
        if s.startswith(k):
            STATUS[k] += 1
            break
    else:
        raise SystemExit('Status ohne Stufe: ' + s)
    PRUEF(s.startswith('erfüllt') or 'Schwere' in s, 'Schwere bei Abweichung in %s' % z['Nr.'])
MIT_BEWUSST = sum(1 for z in ZEILEN.values() if 'bewusst anders' in z['Status'])
PRUEF(sum(STATUS.values()) == len(ZEILEN), 'jede Zeile mit Stufe')
PRUEF(len(ZEILEN) == 28 and STATUS['erfüllt'] == 17 and STATUS['teilweise'] == 10 and STATUS['nicht erfüllt'] == 1
      and MIT_BEWUSST == 3, 'Zählung 28 Zeilen')
aus('  %d Zeilen: %s · davon mit einem Teil „bewusst anders“ %d' % (
    len(ZEILEN), ' · '.join('%s %d' % (k, v) for k, v in STATUS.items()), MIT_BEWUSST))
for z in ZEILEN.values():
    aus('  %s · %s' % (z['Nr.'], z['Status']))

# ================================================================ Ausgaben
ZL = list(ZEILEN.values())
with open(os.path.join(AUS, 'anschluss_2e.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(AUSGABE) + '\n')
with open(os.path.join(AUS, 'teiltabelle_2e.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=SK, quoting=csv.QUOTE_ALL, lineterminator='\n')
    w.writerow(list(ZL[0].keys()))
    for z in ZL:
        w.writerow(list(z.values()))
MD = ['| ' + ' | '.join(ZL[0].keys()) + ' |', '|' + '---|' * len(ZL[0])]
for z in ZL:
    MD.append('| ' + ' | '.join(v.replace('|', '/') for v in z.values()) + ' |')
with open(os.path.join(AUS, 'teiltabelle_2e.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(MD) + '\n')
B = ['# Sätze von 6.1 mit Bezug auf Kapitel 5 nach Rev. 163 (Teilschritt 2 e, 03.10.2026)', '',
     'Master %s Byte, MD5 `%s`. Ersetzt für 6.1 die Tabelle in Abgleichbefund § 1.4 (a), die vor dem Einbau des '
     'Nachtrags entstand. Satznummern neu, daneben die bis Rev. 162 gültige Nummer.' % (
         '{:,}'.format(os.path.getsize(MASTER)).replace(',', '.'), md5(MASTER)), '',
     'Regel: Bezug hat ein Satz mit eigenem Befund, Zahl oder Begriff aus Kapitel 5, mit ausdrücklichem Rückbezug auf '
     'den eigenen Befund oder mit einem Konnektor, der einen Vergleich mit ihm markiert (TV 6.1 § 4). Kennungen in den '
     'Spalten „nimmt auf“ meinen Kapitel 5.', '',
     '| Satz | bis Rev. 162 | Wortlaut (Anfang) | nimmt auf | Art | gedeckt durch |', '|---|---|---|---|---|---|']
RUECK = {v[0]: ia for ia, v in KONK.items() if v[0]}
for i, (wo, art, deck) in BEZUG.items():
    alt_nr = RUECK.get(i, i if not re.match(r'6\.1 A[345] ', i) else '—')
    B.append('| %s | %s | „%s …“ | %s | %s | %s |' % (i, alt_nr, ' '.join(T(i).split()[:8]), wo, art, deck))
B += ['', 'Ohne Bezug auf Kapitel 5 (%d): %s. Grenzfälle darunter: %s.' % (
    len(OHNE), ', '.join(OHNE), ' · '.join('%s (%s)' % (i, g) for i, g in GRENZ.items())), '',
      'Gegen § 1.4 (a): neu seit Rev. 163 %s · nach der Regel ergänzt, Wortlaut unverändert %s · als Bezug entfallen '
      '%s.' % (', '.join(NEU_SEIT_163), ', '.join(NACH_REGEL), ', '.join(ENTFALLEN_ALS_BEZUG)), '',
      '## Konkordanz 6.1 A3 bis A5, bis Rev. 162 zu jetzt', '', '| bis Rev. 162 | jetzt | Grund |', '|---|---|---|']
for ia, (ziel, grund) in KONK.items():
    B.append('| %s | %s | %s |' % (ia, ziel or 'entfällt', grund))
B.append('| — | 6.1 A4 S6 | neu (Markierung „vereinbar“ für beide Metaanalysen) |')
B += ['', '## Stellen mit Satznummern von 6.1 vor Rev. 163', '']
for wo, (dk, stelle, wie, was) in NACHFUEHR.items():
    B.append('- %s: %s (%s)' % (wo, was, wie))
with open(os.path.join(AUS, 'bezuege_2e.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(B) + '\n')
print('\n'.join(AUSGABE[-(len(ZEILEN) + 3):]))

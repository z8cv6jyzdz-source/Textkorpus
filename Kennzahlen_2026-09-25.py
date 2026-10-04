# -*- coding: utf-8 -*-
"""
Kennzahlen_2026-09-25.py — Kennzahlenblatt des Manuskripts aus der Ergebnisdatei der berichteten Rechnung
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 7.1

Zweck: Einzige Zahlenquelle des Manuskripttexts nach der Freigabe F2 (Verfasser, 25.09.2026). Jede
Ergebniszahl steht mit einer Kennung K-xx.y und mit der Kennung der Ergebnisdatei (Spezifikation 0.3).
Die Werte werden nach den Darstellungsregeln des Umfangsdokuments § 3.7 gerundet, die ungerundeten
Werte stehen in der Ergebnisdatei und in der Anlage _Werte.csv dieses Blatts. Nichts wird gerechnet,
außer den Ableitungen, die das Blatt selbst ausweist (Zuteilungsverhältnis, Prä-Post-Intervalle in
Wochen, Einordnung nach der Schlusslogik aus Konfidenzintervall und SESOI, Codelisten aus den
Mitgliedschaften). Das Blatt ersetzt Kennzahlen_2026-09-22 vollständig (R11).

Eingang: Ergebnisse_R_2026-09-25.csv (berichtete Rechnung, Prüfsumme gegen Pruefsummen_Abgabe_2026-09-25.txt),
Spezifikation_2026-09-24_Kennungen.csv (Beschreibung und Einheit je Kennung),
Auswertungs_und_Berichtsumfang_2026-09-24_Kennungen.csv (Berichtsort je Kennung)
Aufruf: python Kennzahlen_2026-09-25.py <Abgabe_R_2026-09-25-Ordner> <Spezifikation_Kennungen.csv> <Umfang_Kennungen.csv> <Ziel.md> <Ziel_Werte.csv>
Fassung: 2026-09-25, zweite Fassung (K-01.24 Clusterebene nach Angabe des Verfassers, Laufprotokoll als .txt).
"""
import sys
import os
import csv
import hashlib
import math
import datetime
from collections import OrderedDict

ABGABE, SPEZ_K, UMF_K, ZIEL_MD, ZIEL_CSV = sys.argv[1:6]
ERG = os.path.join(ABGABE, 'Ergebnisse_R_2026-09-25.csv')
PRUEF = os.path.join(ABGABE, 'Pruefsummen_Abgabe_2026-09-25.txt')

# ---------------------------------------------------------------- Eingang und Prüfsumme
sha_erg = hashlib.sha256(open(ERG, 'rb').read()).hexdigest()
soll = dict(line.rstrip('\n').split('  ', 1)[::-1] for line in open(PRUEF, encoding='utf-8') if line.strip())
if soll.get('Ergebnisse_R_2026-09-25.csv') != sha_erg:
    raise SystemExit('Prüfsumme der Ergebnisdatei stimmt nicht mit der Abgabe überein')
R = OrderedDict()
with open(ERG, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        R[r['Kennung']] = r
SPEZ = {r['kennung']: r for r in csv.DictReader(open(SPEZ_K, encoding='utf-8'))}
UMF = {r['kennung']: r for r in csv.DictReader(open(UMF_K, encoding='utf-8'))}
verwendet = OrderedDict()   # Kennung der Ergebnisdatei → Liste der K-Kennungen


def muster(k):
    """Kennung mit Spielercode auf das Muster P<Code> zurückführen (Anlagen führen nur das Muster)."""
    teile = k.split('.')
    if teile[4].startswith('P') and '-' in teile[4]:
        teile[4] = 'P<Code>'
    return '.'.join(teile)


def roh(k, kk=None):
    """Ungerundeter Wert einer Kennung, None bei fehlendem Wert (Grund über grund(k))."""
    if k not in R:
        raise SystemExit('Kennung fehlt in der Ergebnisdatei: ' + k)
    if kk:
        verwendet.setdefault(k, []).append(kk)
    v = R[k]['Wert']
    return float(v) if v != '' else None


def grund(k):
    return R[k]['Grund']


def ganz(k, kk=None):
    v = roh(k, kk)
    return None if v is None else int(round(v))


def ort(k):
    u = UMF.get(muster(k))
    return (u['umfang_N4'] + ' · ' + u['ort_oder_grund_N4']) if u else '?'


# ---------------------------------------------------------------- Darstellung (Umfangsdokument § 3.7)
ZIELE = OrderedDict([('Z05', 'Sprint 5 m'), ('Z10', 'Sprint 10 m'), ('Z30', 'Sprint 30 m'), ('CL', '505 links'),
                     ('CR', '505 rechts'), ('CM', '505-Seitenmittel'), ('SBJ', 'Standweitsprung')])
KONF = ['Z30', 'CM', 'SBJ']
EINHEIT = {z: ('cm' if z == 'SBJ' else 's') for z in ZIELE}
ND_MSD = {z: (0 if z == 'SBJ' else 2) for z in ZIELE}      # M ± SD
ND_DIFF = {z: (1 if z == 'SBJ' else 3) for z in ZIELE}     # Differenzen, KI, TE, SESOI
MINUS = '−'


def de(x, nd, sign=False):
    """Zahl mit nd Nachkommastellen, Dezimalkomma, typografisches Minus, auf Wunsch immer mit Vorzeichen."""
    if x is None:
        return 'fehlend'
    s = ('%.*f' % (nd, abs(x))).replace('.', ',')
    if x < 0:
        return MINUS + s   # Vorzeichen des ungerundeten Werts, auch wenn die Rundung 0 ergibt
    if sign:
        return '+' + s
    return s


def de_p(p):
    if p is None:
        return 'fehlend'
    return '< 0,001' if p < 0.001 else de(p, 3)


def ki(u, o, nd):
    if u is None or o is None:
        return 'fehlend'
    return '%s bis %s' % (de(u, nd, True), de(o, nd, True))


def msd(m, s, nd):
    if m is None or s is None:
        return 'fehlend'
    return '%s ± %s' % (de(m, nd), de(s, nd))


def fehl(k):
    """Text für einen fehlenden Wert mit Grund."""
    return 'fehlend (%s)' % grund(k)


def wert_oder(k, kk, formatter):
    v = roh(k, kk)
    return fehl(k) if v is None else formatter(v)


zeilen_md = []
werte_csv = []   # (K-Kennung, Bezeichnung, S-Kennungen, Rohwert, Darstellung, Ort)


def md(s=''):
    zeilen_md.append(s)


def notiere(kk, bez, ks, darstellung):
    """Zeile für die Anlage _Werte.csv: K-Kennung, S-Kennungen, Rohwerte, Darstellung, Ort."""
    ks = [ks] if isinstance(ks, str) else list(ks)
    rohs = ' '.join('' if R[k]['Wert'] == '' else R[k]['Wert'] for k in ks) if ks else ''
    werte_csv.append((kk, bez, ' '.join(ks), rohs, darstellung, ort(ks[0]) if ks else 'nicht aus der Ergebnisdatei'))
    for k in ks:
        verwendet.setdefault(k, []).append(kk)


def tabelle(kopf, zeilen, ausrichtung=None):
    md('| ' + ' | '.join(kopf) + ' |')
    md('|' + '|'.join((ausrichtung or ['---'] * len(kopf))) + '|')
    for z in zeilen:
        md('| ' + ' | '.join(str(x) for x in z) + ' |')
    md()


# ---------------------------------------------------------------- Kopf
heute = datetime.date(2026, 9, 25)
md('# Kennzahlenblatt — Bachelorarbeit U15-Plyometrie')
md()
md('**Erzeugt am %s aus der Ergebnisdatei der berichteten Rechnung (Phase 7.1) · Datenstand 2026-09-24 (eingefroren) · Freigabe F2: Verfasser, 25.09.2026 · Rev. 2 vom 25.09.2026: K-01.24 (Clusterebene, angefragte Vereine) ergänzt**' % heute.strftime('%d.%m.%Y'))
md()
md('Einzige Zahlenquelle für den Manuskripttext. Jede Zahl im Manuskript trägt eine Kennung K-xx.y aus diesem Blatt. Jede Zeile nennt daneben die Kennung der Ergebnisdatei (Spezifikation 0.3), aus der der Wert stammt. Zahlen aus Projektanweisungen, Sitzungsnotizen, Befund- oder Übergabedokumenten und aus dem Kennzahlenblatt vom 22.09.2026 werden nicht verwendet, das sind Abschriften oder überholte Stände (Register R11).')
md()
md('Quelle: `Blindrechnung_R_2026-09-24\\Abgabe_R_2026-09-25\\Ergebnisse_R_2026-09-25.csv` (R 4.3.3, blinde zweite Instanz, SHA-256 `%s`), Kopie in `Claude\\03_Skripte\\Abgabe_R_2026-09-25`. Abgleich mit der Gegenprobe (Python) je Kennung bestanden (Abgleichprotokoll_2026-09-25). Erzeuger: `Claude\\03_Skripte\\Kennzahlen_2026-09-25.py`. Bei neuem Datenstand oder neuem Lauf beider Ketten das Skript erneut laufen lassen, nie eine Zahl hier von Hand ändern. Anlage `Kennzahlen_2026-09-25_Werte.csv`: jede Zeile dieses Blatts mit ungerundetem Wert und Berichtsort (T Text, A Anhang, I intern nach dem Umfangsdokument).' % sha_erg)
md()
md('**Darstellungsregeln (Umfangsdokument § 3.7):** Zeiten M ± SD mit zwei Nachkommastellen, Differenzen, Konfidenzgrenzen, TE und SESOI mit drei · Standweitsprung M ± SD ganzzahlig, Differenzen und Grenzen mit einer Nachkommastelle · d und g mit zwei, p mit drei Nachkommastellen, darunter „< 0,001“, CV mit einer · Konfidenzintervalle als Spanne mit „bis“ · Vorzeichen bei Differenzen und Grenzen immer, Differenz IG minus KG, bei Zeiten bedeuten negative Werte eine schnellere IG.')
md()
md('**Bezugsmengen-Regel (Verfasser 22.09.2026, unverändert):** (1) *Zur Eingangstestung angetreten* (K-01.1 bis K-01.8) steht nur im Teilnehmerfluss (Abb. 1) und in genau einem Satz daneben in 5.1. Die Methodik nennt keine Spielerzahlen dieser Menge, 4.1 nennt die Zuteilung auf Vereinsebene. (2) *Analysepopulation* (K-01.14, K-01.16, Menge ANA der Spezifikation: im ITT-Set mindestens einer Zielgröße) ist die Stichprobe des Manuskripts: 4.2, Tab. 2 oben (K-02), Nenner je Zielgröße in Tab. 2 unten und Tab. 3 (K-04, K-06). (3) *Status ausgewertet* (K-01.10, zur Post-Testung angetreten) ist nur ein Zwischenschritt von Abb. 1. Jede Zahl im Text nennt ihre Bezugsmenge, K-02 gilt nur für die Analysepopulation.')
md()
md('**Programmzahlen** (Kontakte, Anteile, Wochen) stehen nicht hier, sondern in `Claude\\03_Skripte\\Programmkennzahlen_2026-09-23.txt` (P-01 bis P-12).')
md()

# ---------------------------------------------------------------- K-01 Teilnehmerfluss
md('## K-01 Teilnehmerfluss und Fallzahlen (Abb. 1, ein Satz in 5.1, Box 6 in 4.7)')
md()
z = []
def z_ganz(kk, bez, k, bezug):
    v = ganz(k, kk)
    z.append((kk, bez, v if v is not None else fehl(k), bezug, k))
    notiere(kk, bez, k, str(v) if v is not None else fehl(k))
z_ganz('K-01.1', 'N zugeteilt und eingangsgetestet', 'S01.N.X.X.ALL.X', 'alle Spieler der Personendaten (jeder mit Prätestdaten, K-01.8)')
for kk, bez, g in [('K-01.2', 'n Interventionsgruppe', 'IG'), ('K-01.3', 'n Kontrollgruppe', 'KG'), ('K-01.4', 'n Verein A (Hohenlind)', 'VA'),
                   ('K-01.5', 'n Verein B (Blau-Weiß)', 'VB'), ('K-01.6', 'n Verein C (Vorwärts Spoho)', 'VC')]:
    ks = ['S01.N.X.X.%s.X' % g, 'S08.FLZUG.X.X.%s.X' % g]
    v = [ganz(k, kk) for k in ks]
    if v[0] != v[1]:
        raise SystemExit('Zugeteilt nach S01 und S08 verschieden: ' + g)
    z.append((kk, bez, v[0], 'zugeteilt (S01 und Teilnehmerfluss S08 gleich)', ', '.join(ks)))
    notiere(kk, bez, ks, str(v[0]))
nig, nkg = ganz('S01.N.X.X.IG.X'), ganz('S01.N.X.X.KG.X')
verh = '%s : 1' % de(nig / nkg, 2)
z.append(('K-01.7', 'Zuteilungsverhältnis IG : KG (Spielerebene, abgeleitet)', verh, 'keine Textverwendung (Verfasser 22.09.), auf Vereinsebene 2 : 1', 'S01.N.X.X.IG.X, S01.N.X.X.KG.X'))
notiere('K-01.7', 'Zuteilungsverhältnis IG : KG', ['S01.N.X.X.IG.X', 'S01.N.X.X.KG.X'], verh)
for kk, bez, fam, bezug in [('K-01.8', 'mit Prätestdaten (mindestens ein gültiger Prä-Versuch)', 'FLPRE', 'zugeteilt'),
                            ('K-01.9', 'Post-Testung nicht angetreten', 'FLNANG', 'zugeteilt (Codes in K-12)'),
                            ('K-01.10', 'Status ausgewertet (zur Post-Testung angetreten)', 'FLAUSG', 'zugeteilt')]:
    ks = ['S08.%s.X.X.%s.X' % (fam, g) for g in ('IG', 'KG', 'VA', 'VB', 'VC')]
    vals = [ganz(k, kk) for k in ks]
    txt = 'IG %d · KG %d (A %d · B %d · C %d)' % tuple(vals)
    z.append((kk, bez, txt, bezug, ', '.join(ks)))
    notiere(kk, bez, ks, txt)
ks = ['S08.FLOPAH.PAH.X.IG.X', 'S08.FLOPAH.PAH.X.KG.X']
vals = [ganz(k, 'K-01.11') for k in ks]
txt = 'IG %d · KG %d' % tuple(vals)
z.append(('K-01.11', 'ohne %PAH (fehlende Anthropometrie, K2)', txt, 'zugeteilt (Codes in K-12)', ', '.join(ks)))
notiere('K-01.11', 'ohne %PAH', ks, txt)
for kk, g, bez in [('K-01.12', 'IG', 'Familiarisierung IG'), ('K-01.13', 'KG', 'Familiarisierung KG')]:
    ks = ['S12.NFAM1.FAM.PRE.%s.X' % g, 'S12.NFAM2.FAM.PRE.%s.X' % g, 'S12.NFAMNA.FAM.PRE.%s.X' % g]
    vals = [ganz(k, kk) for k in ks]
    txt = '%d× ein Termin, %d× zwei, %d ohne Angabe' % tuple(vals)
    z.append((kk, bez, txt, 'zugeteilt', ', '.join(ks)))
    notiere(kk, bez, ks, txt)
ks = ['S12.N.AGE.PRE.ANAIG.X', 'S12.N.AGE.PRE.ANAKG.X']
ana_ig, ana_kg = [ganz(k, 'K-01.14') for k in ks]
txt = 'IG %d · KG %d = %d' % (ana_ig, ana_kg, ana_ig + ana_kg)
z.append(('K-01.14', 'Analysepopulation ANA (im ITT-Set mindestens einer Zielgröße)', txt, 'Stichprobe des Manuskripts, Nenner je Zielgröße in K-04 und K-06', ', '.join(ks)))
notiere('K-01.14', 'Analysepopulation ANA', ks, txt)
# Codes der Analysepopulation und der nicht analysierten Spieler aus den Mitgliedschaften (abgeleitet)
codes = [k.split('.')[4][1:] for k in R if k.startswith('S05.PAH.PAH.PRE.P')]
in_ana = {c: any(ganz('S08.MITGL.%s.X.P%s.ITT' % (zz, c)) == 1 for zz in ZIELE) for c in codes}
nicht_ana = [c for c in codes if not in_ana[c]]
txt = '%d: %s' % (len(nicht_ana), ', '.join(nicht_ana))
z.append(('K-01.15', 'nicht in der Analysepopulation (abgeleitet aus den ITT-Mitgliedschaften)', txt, 'Post-Testung nicht angetreten oder ohne %PAH (Gründe je Spieler in K-12)', 'S08.MITGL.{Ziel}.X.P<Code>.ITT'))
notiere('K-01.15', 'nicht in der Analysepopulation', ['S08.MITGL.%s.X.P%s.ITT' % (zz, c) for c in codes for zz in ZIELE], txt)
verein = lambda c: {'HL': 'A', 'BW': 'B', 'VS': 'C'}[c[:2]]
ana_v = {v: sum(1 for c in codes if in_ana[c] and verein(c) == v) for v in 'ABC'}
txt = 'A %d · B %d · C %d' % (ana_v['A'], ana_v['B'], ana_v['C'])
z.append(('K-01.16', 'Analysepopulation je Verein (abgeleitet, Codepräfix HL = A, BW = B, VS = C)', txt, 'Bezugsmenge K-01.14, für 4.2', 'S08.MITGL.{Ziel}.X.P<Code>.ITT'))
notiere('K-01.16', 'Analysepopulation je Verein', [], txt)
ks = ['S07.GE01.ADH.X.IG.GANZ']
v = ganz(ks[0], 'K-01.17')
z.append(('K-01.17', 'Intervention erhalten (IG, mindestens eine vollständig gemeldete Einheit, CONSORT 13a)', v, 'zugeteilte IG-Spieler', ks[0]))
notiere('K-01.17', 'Intervention erhalten', ks, str(v))
# Clusterebene des Teilnehmerflusses (Abb. 1): Angabe des Verfassers vom 25.09.2026, nicht aus der Ergebnisdatei
VEREINE_ANGEFRAGT = 4
VEREINE_ZUGESAGT = 3
txt = 'angefragt %d · zugesagt %d (A, B, C) · ohne Zusage %d' % (VEREINE_ANGEFRAGT, VEREINE_ZUGESAGT, VEREINE_ANGEFRAGT - VEREINE_ZUGESAGT)
z.append(('K-01.24', 'Vereine (Clusterebene von Abb. 1, Angabe des Verfassers 25.09.2026, Zuteilung auf Vereinsebene vor der Eingangstestung)', txt, 'angefragte Vereine', 'nicht aus der Ergebnisdatei'))
notiere('K-01.24', 'Vereine angefragt, zugesagt, ohne Zusage', [], txt)
tabelle(['Kennung', 'Größe', 'Wert', 'Bezugsmenge', 'Kennung der Ergebnisdatei'], z)

md('**Box 6 nach CONSORT (K-01.18 bis K-01.22, je Gruppe gezählt, nicht exklusiv, 4.7):**')
md()
z = []
for kk, bez, ks in [('K-01.18', 'Nichteinhaltung (IG mit GANZ < 6, einschließlich 0)', ['S08.B6NE.X.X.IG.X']),
                    ('K-01.19', 'davon ohne jede Meldung', ['S08.B6NEKM.X.X.IG.X']),
                    ('K-01.20', 'Instrumentenfehler (kein Listenplatz)', ['S08.B6IF.X.X.IG.X']),
                    ('K-01.21', 'fehlende Kovariate %PAH', ['S08.B6FK.X.X.IG.X', 'S08.B6FK.X.X.KG.X']),
                    ('K-01.22', 'nicht angetreten', ['S08.B6NA.X.X.IG.X', 'S08.B6NA.X.X.KG.X'])]:
    vals = [ganz(k, kk) for k in ks]
    txt = ('IG %d' % vals[0]) if len(vals) == 1 else 'IG %d · KG %d' % tuple(vals)
    z.append((kk, bez, txt, ', '.join(ks)))
    notiere(kk, bez, ks, txt)
tabelle(['Kennung', 'Klasse', 'Wert', 'Kennung der Ergebnisdatei'], z)

md('**Erhebungs- und Attritionsanteile (K-01.23, Spieler mit BEST prä und post je zugeteiltem Spieler, 6.3 TESTEX 6):**')
md()
z = []
for zz, name in ZIELE.items():
    ks = ['S08.ANT.%s.X.%s.X' % (zz, g) for g in ('IG', 'KG', 'ALL')]
    vals = [roh(k, 'K-01.23') for k in ks]
    txt = ['%s %%' % de(100 * v, 1) for v in vals]
    z.append(('K-01.23', name, txt[0], txt[1], txt[2], ', '.join(ks)))
    notiere('K-01.23 ' + zz, 'Erhebungsanteil ' + name, ks, ' · '.join(txt))
ks = ['S08.ANTTN.X.X.%s.X' % g for g in ('IG', 'KG', 'ALL')]
vals = [roh(k, 'K-01.23') for k in ks]
txt = ['%s %%' % de(100 * v, 1) for v in vals]
z.append(('K-01.23', 'Teilnehmerebene (Status ausgewertet je zugeteilt)', txt[0], txt[1], txt[2], ', '.join(ks)))
notiere('K-01.23 TN', 'Erhebungsanteil Teilnehmerebene', ks, ' · '.join(txt))
tabelle(['Kennung', 'Zielgröße', 'IG', 'KG', 'gesamt', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-02 Stichprobe ANA
md('## K-02 Stichprobe der Analysepopulation (Tab. 2 oben, 4.2)')
md()
md('Bezugsmenge K-01.14 (Menge ANA). Prä-Werte. Keine Signifikanztests (CONSORT Item 15).')
md()
z = []
for kk, zz, bez, nd in [('K-02.1', 'AGE', 'Alter (Jahre)', 2), ('K-02.2', 'HGT', 'Körperhöhe (cm)', 1),
                        ('K-02.3', 'MASS', 'Körpermasse (kg)', 1), ('K-02.4', 'PAH', '%PAH', 2)]:
    zelle = []
    ks = []
    for g in ('ANAIG', 'ANAKG'):
        kn, km, ksd = ['S12.%s.%s.PRE.%s.X' % (x, zz, g) for x in ('N', 'M', 'SD')]
        ks += [kn, km, ksd]
        zelle.append('%s (n = %d)' % (msd(roh(km, kk), roh(ksd, kk), nd), ganz(kn, kk)))
    z.append((kk, bez, zelle[0], zelle[1], ', '.join(ks)))
    notiere(kk, bez, ks, ' | '.join(zelle))
z.append(('K-02.5', 'Geburtsjahrgang (Studienmerkmal, nicht in der Ergebnisdatei)', '2011', '2012', 'Studiensteckbrief, Mannschaftsjahrgang'))
notiere('K-02.5', 'Geburtsjahrgang', [], '2011 | 2012')
tabelle(['Kennung', 'Merkmal', 'Interventionsgruppe', 'Kontrollgruppe', 'Kennung der Ergebnisdatei'], z)
md('Alters- und Wertespannen (Minimum, Maximum) werden nicht mehr berichtet (Nachtrag 2, N4.11). Die Überlappung der Kovariaten je Analyseset steht in K-04.')
md()

# ---------------------------------------------------------------- K-03 Termine
md('## K-03 Termine und Prä-Post-Intervalle (4.3, Abb. H7)')
md()
md('Nicht Teil der Ergebnisdatei (der Datenstand enthält keine Testdaten). Übernommen aus dem Workbook `Statistik\\Studiendaten_U15_gesamt.xlsx`, Blatt `01_Personen`, wie im Kennzahlenblatt vom 22.09.2026 (K-03). Intervalle im Skript aus den Daten berechnet.')
md()
termine = [('K-03.1', 'Verein A (Hohenlind)', datetime.date(2026, 7, 2), datetime.date(2026, 9, 10)),
           ('K-03.2', 'Verein B (Blau-Weiß Köln)', datetime.date(2026, 7, 14), datetime.date(2026, 9, 1)),
           ('K-03.3', 'Verein C (Vorwärts Spoho)', datetime.date(2026, 7, 13), datetime.date(2026, 9, 14))]
z = []
for kk, v, pre, post in termine:
    tage = (post - pre).days
    txt = '%s | %s | %d Tage = %s Wochen' % (pre.strftime('%d.%m.%Y'), post.strftime('%d.%m.%Y'), tage, de(tage / 7, 1))
    z.append((kk, v, pre.strftime('%d.%m.%Y'), post.strftime('%d.%m.%Y'), '%d Tage = %s Wochen' % (tage, de(tage / 7, 1))))
    notiere(kk, 'Termine ' + v, [], txt)
tabelle(['Kennung', 'Verein', 'Prä', 'Post', 'Intervall'], z)
md('Spanne der Intervalle über die drei Vereine (K-03.4): %s bis %s Wochen. Intervention 20.07. bis 30.08.2026 (Programmwochen W1 bis W6, Konstanten der Spezifikation).' % (
    de(min((p2 - p1).days for _, _, p1, p2 in termine) / 7, 1), de(max((p2 - p1).days for _, _, p1, p2 in termine) / 7, 1)))
notiere('K-03.4', 'Spanne der Prä-Post-Intervalle', [], '%s bis %s Wochen' % (de(min((p2 - p1).days for _, _, p1, p2 in termine) / 7, 1), de(max((p2 - p1).days for _, _, p1, p2 in termine) / 7, 1)))
md()

# ---------------------------------------------------------------- K-04 Ausgangswerte
md('## K-04 Ausgangswerte je Zielgröße (Tab. 2 unten, Tab. H3)')
md()
md('**K-04.1 bis K-04.7 im Analyseset je Zielgröße (ITT: BEST prä, BEST post und %PAH vorhanden). d = (M_IG − M_KG) / SD_pool ohne J, nur deskriptiv. Überlappung nach S12 Regel 2 (Zahl der Spieler im gemeinsamen Bereich von Ausgangswert und %PAH, nur konfirmatorische Zielgrößen).**')
md()
z = []
for i, (zz, name) in enumerate(ZIELE.items(), 1):
    kk = 'K-04.%d' % i
    ks = []
    zelle = []
    for g in ('ITTIG', 'ITTKG'):
        kn, km, ksd = ['S12.%s.%s.PRE.%s.HAUPT' % (x, zz, g) for x in ('N', 'M', 'SD')]
        ks8 = 'S08.N.%s.X.%s.X' % (zz, g)
        if ganz(kn, kk) != ganz(ks8, kk):
            raise SystemExit('Setgröße nach S08 und S12 verschieden: ' + ks8)
        ks += [ks8, kn, km, ksd]
        zelle.append(str(ganz(kn, kk)))
        zelle.append(msd(roh(km, kk), roh(ksd, kk), ND_MSD[zz]))
    kd = 'S12.D.%s.PRE.ITT.HAUPT' % zz
    ks.append(kd)
    dtxt = wert_oder(kd, kk, lambda v: de(v, 2, True))
    if zz in KONF:
        ko = ['S14.%s.%s.X.ITT.HAUPT' % (x, zz) for x in ('OVPREIG', 'OVPREKG', 'OVPAHIG', 'OVPAHKG')]
        ks += ko
        ov = [ganz(k, kk) for k in ko]
        ovtxt = 'Prä IG %d, KG %d · %%PAH IG %d, KG %d' % tuple(ov)
    else:
        ovtxt = '–'
    z.append((kk, '%s (%s)' % (name, EINHEIT[zz]), zelle[0], zelle[1], zelle[2], zelle[3], dtxt, ovtxt, ', '.join(ks)))
    notiere(kk, 'Ausgangswerte ITT ' + name, ks, ' | '.join(zelle) + ' | d ' + dtxt + ' | ' + ovtxt)
tabelle(['Kennung', 'Zielgröße', 'n IG', 'M ± SD IG', 'n KG', 'M ± SD KG', 'd', 'Überlappung', 'Kennung der Ergebnisdatei'], z)
md('Gemeinsamer Bereich der Kovariaten (K-04.8, untere und obere Grenze, konfirmatorische Zielgrößen):')
md()
z = []
for zz in KONF:
    ks = ['S14.%s.%s.X.ITT.HAUPT' % (x, zz) for x in ('OVPRL', 'OVPRU', 'OVPAL', 'OVPAU')]
    v = [roh(k, 'K-04.8') for k in ks]
    txt = 'Prä %s bis %s %s · %%PAH %s bis %s' % (de(v[0], ND_DIFF[zz]), de(v[1], ND_DIFF[zz]), EINHEIT[zz], de(v[2], 2), de(v[3], 2))
    z.append(('K-04.8', ZIELE[zz], txt, ', '.join(ks)))
    notiere('K-04.8 ' + zz, 'gemeinsamer Bereich ' + ZIELE[zz], ks, txt)
tabelle(['Kennung', 'Zielgröße', 'gemeinsamer Bereich', 'Kennung der Ergebnisdatei'], z)
md('**K-04.9 bis K-04.15 alle eingangsgetesteten Spieler mit Bestwert prä (Menge BASE, Tab. H3, Ausfallvergleich zu Tab. 2):**')
md()
z = []
for i, (zz, name) in enumerate(ZIELE.items(), 9):
    kk = 'K-04.%d' % i
    ks = []
    zelle = []
    for g in ('IG', 'KG'):
        kn, km, ksd = ['S12.%s.%s.PRE.%s.HAUPT' % (x, zz, g) for x in ('N', 'M', 'SD')]
        ks += [kn, km, ksd]
        zelle.append(str(ganz(kn, kk)))
        zelle.append(msd(roh(km, kk), roh(ksd, kk), ND_MSD[zz]))
    kd = 'S12.D.%s.PRE.BASE.HAUPT' % zz
    ks.append(kd)
    dtxt = wert_oder(kd, kk, lambda v: de(v, 2, True))
    z.append((kk, '%s (%s)' % (name, EINHEIT[zz]), zelle[0], zelle[1], zelle[2], zelle[3], dtxt, ', '.join(ks)))
    notiere(kk, 'Ausgangswerte BASE ' + name, ks, ' | '.join(zelle) + ' | d ' + dtxt)
tabelle(['Kennung', 'Zielgröße', 'n IG', 'M ± SD IG', 'n KG', 'M ± SD KG', 'd', 'Kennung der Ergebnisdatei'], z)
md('**K-04.16 bis K-04.19 deskriptive Zielgrößen prä und post im Analyseset (Tab. H3, nur Deskription, R5):**')
md()
z = []
for i, zz in enumerate(['Z05', 'Z10', 'CL', 'CR'], 16):
    kk = 'K-04.%d' % i
    ks = []
    zelle = []
    for t in ('PRE', 'POST'):
        for g in ('ITTIG', 'ITTKG'):
            kn, km, ksd = ['S12.%s.%s.%s.%s.HAUPT' % (x, zz, t, g) for x in ('N', 'M', 'SD')]
            ks += [kn, km, ksd]
            zelle.append('%s (n = %d)' % (msd(roh(km, kk), roh(ksd, kk), ND_MSD[zz]), ganz(kn, kk)))
    z.append((kk, '%s (%s)' % (ZIELE[zz], EINHEIT[zz]), zelle[0], zelle[1], zelle[2], zelle[3], ', '.join(ks)))
    notiere(kk, 'Prä und Post deskriptiv ' + ZIELE[zz], ks, ' | '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'prä IG', 'prä KG', 'post IG', 'post KG', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-05 Messgüte
md('## K-05 Messgüte (Tab. 1 in 4.4, Tab. H1)')
md()
md('TE = gepoolte Innerspieler-SD der gültigen Wiederholungsversuche der Spieler mit k ≥ 2 (O5), 95-%-KI aus χ² (K12), CV = 100 · TE / Mittel der Versuche der TE-Menge (K13), S = SD der Bestwerte prä aller Spieler (O6), SESOI = 0,2 · S, RTS = TE/SESOI, FLEINZ = 1 wenn TE > SESOI. Seitenmittel aus beidseitig gültigen Versuchsnummern (K15). Ohne MDC und ohne TE/√n (Nachtrag 2).')
md()
z = []
for i, (zz, name) in enumerate(ZIELE.items(), 1):
    kk = 'K-05.%d' % i
    nd = ND_DIFF[zz]
    ks = ['S10.%s.%s.PRE.ALL.X' % (x, zz) for x in ('NTE', 'TE', 'TELO', 'TEHI', 'DFTE', 'CV', 'NSB', 'SB', 'SESOI', 'RTS', 'FLEINZ')]
    v = {x: roh('S10.%s.%s.PRE.ALL.X' % (x, zz), kk) for x in ('NTE', 'TE', 'TELO', 'TEHI', 'DFTE', 'CV', 'NSB', 'SB', 'SESOI', 'RTS', 'FLEINZ')}
    kp = ['S10.%s.%s.POST.ALL.X' % (x, zz) for x in ('NTE', 'TE', 'TELO', 'TEHI', 'DFTE')]
    vp = {x: roh('S10.%s.%s.POST.ALL.X' % (x, zz), kk) for x in ('NTE', 'TE', 'TELO', 'TEHI', 'DFTE')}
    te_txt = '%s [%s]' % (de(v['TE'], nd), ki(v['TELO'], v['TEHI'], nd).replace('+', ''))
    tep_txt = '%s [%s] (n = %d)' % (de(vp['TE'], nd), ki(vp['TELO'], vp['TEHI'], nd).replace('+', ''), int(vp['NTE']))
    zeile = (kk, '%s (%s)' % (name, EINHEIT[zz]), int(v['NTE']), te_txt, int(v['DFTE']), de(v['CV'], 1),
             '%s (n = %d)' % (de(v['SB'], nd), int(v['NSB'])), de(v['SESOI'], nd), de(v['RTS'], 2), int(v['FLEINZ']), tep_txt, ', '.join(ks + kp))
    z.append(zeile)
    notiere(kk, 'Messgüte ' + name, ks + kp, ' | '.join(str(x) for x in zeile[2:11]))
tabelle(['Kennung', 'Zielgröße', 'n prä', 'TE prä [95-%-KI]', 'df', 'CV (%)', 'S (Zwischen-SD der Bestwerte)', 'SESOI', 'TE/SESOI', 'TE > SESOI', 'TE post [95-%-KI]', 'Kennung der Ergebnisdatei'], z)
md('**K-05.8 TE je Verein (Tab. H1), prä und post, mit df und Zahl der Spieler der TE-Menge:**')
md()
z = []
for zz, name in ZIELE.items():
    nd = ND_DIFF[zz]
    zelle = []
    ks = []
    for t in ('PRE', 'POST'):
        for vv in ('VA', 'VB', 'VC'):
            kt, kd, kn = ['S10.%s.%s.%s.%s.X' % (x, zz, t, vv) for x in ('TE', 'DFTE', 'NTE')]
            ks += [kt, kd, kn]
            te = roh(kt, 'K-05.8')
            zelle.append(fehl(kt) if te is None else '%s (df %d, n %d)' % (de(te, nd), ganz(kd, 'K-05.8'), ganz(kn, 'K-05.8')))
    z.append(('K-05.8', '%s (%s)' % (name, EINHEIT[zz]), *zelle, ', '.join(ks)))
    notiere('K-05.8 ' + zz, 'TE je Verein ' + name, ks, ' | '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'prä A', 'prä B', 'prä C', 'post A', 'post B', 'post C', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-06 Hauptanalyse
md('## K-06 Hauptanalyse: ANCOVA im ITT-Set (Tab. 3, 5.2, 6.1, Tab. H4)')
md()
md('Modell Post = b0 + b1·G + b2·Prä + b3·%PAH, G = 1 für die IG. b1 = adjustierte Gruppendifferenz im Post-Wert (IG minus KG). Unadjustierte Differenz = Differenz der Post-Mittel im selben Set (O4). g = b1 / gepoolte Prä-SD × J, KI aus dem KI von b1 (O3). Einordnung nach der Schlusslogik (Umfangsdokument § 5.1): Differenz so gepolt, dass positive Werte einen Vorteil der IG bedeuten, gegen null und SESOI (K-05) gelegt.')
md()


def fall(kiu, kio, sesoi, zeit):
    """Fall A bis E nach Umfangsdokument § 5.1. Bei Zeiten wird das Intervall gespiegelt (Vorteil der IG positiv)."""
    L, U = (-kio, -kiu) if zeit else (kiu, kio)
    S = sesoi
    if L > S:
        return 'A'
    if 0 < L <= S < U:
        return 'B1'
    if 0 < L and U <= S:
        return 'B2'
    if U < 0:
        return 'E'
    if L < -S and U > S:
        return 'C1'
    if -S <= L <= 0 and U > S:
        return 'C2'
    if L < -S and 0 <= U <= S:
        return 'C3'
    if -S <= L <= 0 <= U <= S:
        return 'D'
    return '?'


FALLTEXT = {'A': 'Vorteil der IG mindestens in Höhe des SESOI', 'B1': 'Unterschied zugunsten der IG, Relevanz offen', 'B2': 'Unterschied zugunsten der IG unter dem SESOI',
            'C1': 'kein Unterschied nachweisbar, relevante Effekte in beide Richtungen vereinbar, unschlüssig', 'C2': 'kein Unterschied nachweisbar, nur ein relevanter Vorteil der IG vereinbar',
            'C3': 'kein Unterschied nachweisbar, nur ein relevanter Nachteil der IG vereinbar', 'D': 'kein Unterschied nachweisbar, Unterschiede in Höhe des SESOI ausgeschlossen', 'E': 'Vorteil der KG'}
z = []
for i, zz in enumerate(KONF, 1):
    kk = 'K-06.%d' % i
    nd, ndm = ND_DIFF[zz], ND_MSD[zz]
    g = lambda x, s='S13': '%s.%s.%s.X.ITT.HAUPT' % (s, x, zz)
    ks = [g('NIG'), g('NKG'), g('MPOSTIG', 'S15'), g('MPOSTKG', 'S15'), g('SDPOST', 'S15'), g('UD', 'S15'), g('UDKIU', 'S15'), g('UDKIO', 'S15'), g('UDP', 'S15'),
          g('B1'), g('KIU'), g('KIO'), g('P'), g('G', 'S15'), g('GKIU', 'S15'), g('GKIO', 'S15'), g('SIG'), 'S10.SESOI.%s.PRE.ALL.X' % zz]
    v = {k: roh(k, kk) for k in ks}
    # Post-SD je Gruppe aus S12 (ITT-Set)
    ksd = ['S12.SD.%s.POST.%s.HAUPT' % (zz, gg) for gg in ('ITTIG', 'ITTKG')]
    sd_ig, sd_kg = [roh(k, kk) for k in ksd]
    ks += ksd
    for gg, kn, km in (('ITTIG', 'NIG', 'MPOSTIG'), ('ITTKG', 'NKG', 'MPOSTKG')):
        k12n, k12m = 'S12.N.%s.POST.%s.HAUPT' % (zz, gg), 'S12.M.%s.POST.%s.HAUPT' % (zz, gg)
        if ganz(k12n, kk) != int(v[g(kn)]) or abs(roh(k12m, kk) - v[g(km, 'S15')]) > 1e-9:
            raise SystemExit('Post-Kennwerte nach S12 und S13/S15 verschieden: ' + k12n)
        ks += [k12n, k12m]
    n_txt = '%d / %d' % (v[g('NIG')], v[g('NKG')])
    post_ig = msd(v[g('MPOSTIG', 'S15')], sd_ig, ndm)
    post_kg = msd(v[g('MPOSTKG', 'S15')], sd_kg, ndm)
    ud_txt = '%s [%s]' % (de(v[g('UD', 'S15')], nd, True), ki(v[g('UDKIU', 'S15')], v[g('UDKIO', 'S15')], nd))
    b1_txt = '%s [%s]' % (de(v[g('B1')], nd, True), ki(v[g('KIU')], v[g('KIO')], nd))
    p_txt = de_p(v[g('P')])
    g_txt = '%s [%s]' % (de(v[g('G', 'S15')], 2, True), ki(v[g('GKIU', 'S15')], v[g('GKIO', 'S15')], 2))
    fl = fall(v[g('KIU')], v[g('KIO')], v['S10.SESOI.%s.PRE.ALL.X' % zz], zz != 'SBJ')
    z.append((kk, '%s (%s)' % (ZIELE[zz], EINHEIT[zz]), n_txt, post_ig, post_kg, ud_txt, b1_txt, p_txt, g_txt, de(v['S10.SESOI.%s.PRE.ALL.X' % zz], nd), '%s (%s)' % (fl, FALLTEXT[fl]), ', '.join(ks)))
    notiere(kk, 'Hauptanalyse ' + ZIELE[zz], ks, ' | '.join([n_txt, post_ig, post_kg, ud_txt, b1_txt, p_txt, g_txt, 'Fall ' + fl]))
tabelle(['Kennung', 'Zielgröße', 'n IG / KG', 'Post M ± SD IG', 'Post M ± SD KG', 'Differenz unadjustiert [95-%-KI]', 'Differenz adjustiert b1 [95-%-KI]', 'p', 'g [95-%-KI]', 'SESOI', 'Fall (Schlusslogik)', 'Kennung der Ergebnisdatei'], z)
ks = ['S13.H0REJ.X.X.ITT.HAUPT', 'S13.NTEST.X.X.ITT.HAUPT'] + ['S13.SIG.%s.X.ITT.HAUPT' % zz for zz in KONF]
h0, nt = ganz(ks[0], 'K-06.4'), ganz(ks[1], 'K-06.4')
sigs = [ganz(k, 'K-06.4') for k in ks[2:]]
txt = 'H0 %s (H0REJ = %d), %d konfirmatorische Tests, SIG je Zielgröße %s' % ('abgelehnt' if h0 == 1 else 'nicht abgelehnt', h0, nt, ', '.join('%s %d' % (zz, s) for zz, s in zip(KONF, sigs)))
md('**K-06.4 Entscheidung nach dem Antrag (K23, P6):** %s. Keine Adjustierung für Mehrfachtestung.' % txt)
notiere('K-06.4', 'Entscheidung über H0', ks, txt)
md()
md('**K-06.5 Modellkennwerte und adjustierte Mittelwerte (Tab. H4):**')
md()
z = []
for zz in KONF:
    nd, ndm = ND_DIFF[zz], ND_MSD[zz]
    g = lambda x: 'S13.%s.%s.X.ITT.HAUPT' % (x, zz)
    ks = [g(x) for x in ('B0', 'SEB0', 'B2', 'SEB2', 'B3', 'SEB3', 'SEB1', 'T', 'DF', 'SIGMA', 'R2', 'AMIG', 'AMIGU', 'AMIGO', 'AMKG', 'AMKGU', 'AMKGO', 'PREM', 'PAHM')]
    v = {k: roh(k, 'K-06.5') for k in ks}
    ndk = nd + 1 if zz == 'SBJ' else nd   # Koeffizienten beim Standweitsprung mit einer Stelle mehr als Differenzen
    zeile = ('K-06.5', ZIELE[zz],
             '%s (SE %s)' % (de(v[g('B0')], ndk), de(v[g('SEB0')], ndk)),
             '%s (SE %s)' % (de(v[g('B2')], 3), de(v[g('SEB2')], 3)),
             '%s (SE %s)' % (de(v[g('B3')], ndk), de(v[g('SEB3')], ndk)),
             de(v[g('SEB1')], nd), de(v[g('T')], 2), int(v[g('DF')]), de(v[g('SIGMA')], nd), de(v[g('R2')], 2),
             '%s [%s]' % (de(v[g('AMIG')], ndm if zz == 'SBJ' else 3), ki(v[g('AMIGU')], v[g('AMIGO')], ndm if zz == 'SBJ' else 3).replace('+', '')),
             '%s [%s]' % (de(v[g('AMKG')], ndm if zz == 'SBJ' else 3), ki(v[g('AMKGU')], v[g('AMKGO')], ndm if zz == 'SBJ' else 3).replace('+', '')),
             '%s · %s' % (de(v[g('PREM')], nd), de(v[g('PAHM')], 2)), ', '.join(ks))
    z.append(zeile)
    notiere('K-06.5 ' + zz, 'Modellkennwerte ' + ZIELE[zz], ks, ' | '.join(str(x) for x in zeile[2:13]))
tabelle(['Kennung', 'Zielgröße', 'b0', 'b2 (Prä)', 'b3 (%PAH)', 'SE(b1)', 't', 'df', 'Residuen-SD', 'R²', 'adj. Mittel IG [95-%-KI]', 'adj. Mittel KG [95-%-KI]', 'Prä-Mittel · %PAH-Mittel des Sets', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-07 Voraussetzungen
md('## K-07 Voraussetzungsprüfungen (5.2 Satz nach R2, Tab. H4, Anhang G)')
md()
md('Regel O7: Eine verworfene Prüfung (p < 0,05) ändert das Verfahren nicht, sie wird mit Prüfgröße und p berichtet. Nicht verworfene Prüfungen heißen „geprüft und nicht verworfen“.')
md()
z = []
for zz in KONF:
    nd = ND_DIFF[zz]
    g = lambda x, var='HAUPT': 'S14.%s.%s.X.ITT.%s' % (x, zz, var)
    ks = [g(x) for x in ('SWW', 'SWP', 'SWVERW', 'BFF', 'BFDF1', 'BFDF2', 'BFP', 'BFVERW', 'SDRIG', 'SDRKG', 'SDRQ')] + \
         [g(x, 'SLPRE') for x in ('BINT', 'SEINT', 'TINT', 'DFINT', 'PINT', 'VERW')] + [g(x, 'SLPAH') for x in ('BINT', 'SEINT', 'TINT', 'DFINT', 'PINT', 'VERW')]
    v = {k: roh(k, 'K-07.1') for k in ks}
    sw = 'W = %s, p = %s%s' % (de(v[g('SWW')], 3), de_p(v[g('SWP')]), ', verworfen' if v[g('SWVERW')] == 1 else ', nicht verworfen')
    bf = 'F(%d, %d) = %s, p = %s%s' % (v[g('BFDF1')], v[g('BFDF2')], de(v[g('BFF')], 2), de_p(v[g('BFP')]), ', verworfen' if v[g('BFVERW')] == 1 else ', nicht verworfen')
    sdr = 'IG %s, KG %s, Verhältnis KG/IG %s' % (de(v[g('SDRIG')], nd), de(v[g('SDRKG')], nd), de(v[g('SDRQ')], 2))
    sl1 = 'b = %s (SE %s), t(%d) = %s, p = %s%s' % (de(v[g('BINT', 'SLPRE')], 3, True), de(v[g('SEINT', 'SLPRE')], 3), v[g('DFINT', 'SLPRE')], de(v[g('TINT', 'SLPRE')], 2), de_p(v[g('PINT', 'SLPRE')]), ', verworfen' if v[g('VERW', 'SLPRE')] == 1 else '')
    sl2 = 'b = %s (SE %s), t(%d) = %s, p = %s%s' % (de(v[g('BINT', 'SLPAH')], 4, True), de(v[g('SEINT', 'SLPAH')], 4), v[g('DFINT', 'SLPAH')], de(v[g('TINT', 'SLPAH')], 2), de_p(v[g('PINT', 'SLPAH')]), ', verworfen' if v[g('VERW', 'SLPAH')] == 1 else '')
    z.append(('K-07.1', ZIELE[zz], sw, bf, sdr, sl1, sl2, ', '.join(ks)))
    notiere('K-07.1 ' + zz, 'Voraussetzungen ' + ZIELE[zz], ks, ' | '.join([sw, bf, sdr, sl1, sl2]))
tabelle(['Kennung', 'Zielgröße', 'Shapiro-Wilk der Residuen', 'Brown-Forsythe', 'Residuen-SD je Gruppe', 'Steigung Gruppe × Prä', 'Steigung Gruppe × %PAH', 'Kennung der Ergebnisdatei'], z)
md('**K-07.2 Vorab-Prüfung an den Prä-Werten (Menge BPAH, beschreibt die Ausgangslage, keine ANCOVA-Voraussetzung):**')
md()
z = []
for zz in KONF:
    ks = ['S14.%s.%s.PRE.BPAH.SLPAH' % (x, zz) for x in ('CINT', 'SECINT', 'TCINT', 'DFCINT', 'PCINT')] + ['S14.%s.%s.PRE.%s.X' % (x, zz, gg) for gg in ('BPAHIG', 'BPAHKG') for x in ('SWW', 'SWP')]
    v = {k: roh(k, 'K-07.2') for k in ks}
    c = ks[0]
    if v[c] is None:
        int_txt = fehl(c)
    else:
        int_txt = 'c3 = %s (SE %s), t(%d) = %s, p = %s' % (de(v[ks[0]], 4, True), de(v[ks[1]], 4), v[ks[3]], de(v[ks[2]], 2), de_p(v[ks[4]]))
    sw_ig = fehl(ks[5]) if v[ks[5]] is None else 'W = %s, p = %s' % (de(v[ks[5]], 3), de_p(v[ks[6]]))
    sw_kg = fehl(ks[7]) if v[ks[7]] is None else 'W = %s, p = %s' % (de(v[ks[7]], 3), de_p(v[ks[8]]))
    z.append(('K-07.2', ZIELE[zz], int_txt, sw_ig, sw_kg, ', '.join(ks)))
    notiere('K-07.2 ' + zz, 'Vorab-Prüfung ' + ZIELE[zz], ks, ' | '.join([int_txt, sw_ig, sw_kg]))
tabelle(['Kennung', 'Zielgröße', 'Interaktion Gruppe × %PAH im Prä-Modell', 'Shapiro-Wilk Prä IG', 'Shapiro-Wilk Prä KG', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-08 Sensitivität
md('## K-08 Per-Protokoll-Vergleich, Sensitivitätsanalysen und Bootstrap (Tab. H4, 5.2 Sammelsatz, 6.2)')
md()
md('Je Variante adjustierte Differenz b1 mit 95-%-KI, p und n je Gruppe. Bei INF = 0 (unter acht Spielern je Gruppe) nur Deskription (R4, R5). Änderungswertmodell (AEND) mit Δ = Post − Prä und %PAH, Modell ohne %PAH (OPAH), Familiarisierung als dritte Kovariate (FAMB, Set FAMS).')
md()
VARIANTEN = [('K-08.1', 'PP6 (Per-Protokoll ≥ 6, Hauptschwelle)', 'S16', 'PP6', 'HAUPT'), ('K-08.2', 'Mittelwert statt Bestwert (MW)', 'S17', 'ITT', 'MW'),
             ('K-08.3', 'PP5 (≥ 5)', 'S17', 'PP5', 'HAUPT'), ('K-08.4', 'PP7 (≥ 7)', 'S17', 'PP7', 'HAUPT'),
             ('K-08.5', 'Änderungswertmodell (AEND)', 'S17', 'ITT', 'AEND'), ('K-08.6', 'ohne %PAH (OPAH)', 'S17', 'ITT', 'OPAH'),
             ('K-08.7', 'Familiarisierung als Kovariate (FAMB)', 'S17', 'FAMS', 'FAMB')]
z = []
for kk, bez, s, menge, var in VARIANTEN:
    for zz in KONF:
        nd = ND_DIFF[zz]
        ks = ['%s.%s.%s.X.%s.%s' % (s, x, zz, menge, var) for x in ('B1', 'KIU', 'KIO', 'P', 'NIG', 'NKG', 'DF')]
        v = {k: roh(k, kk) for k in ks}
        n_txt = '%s / %s' % (int(v[ks[4]]), int(v[ks[5]]))
        if v[ks[0]] is None:
            b_txt, p_txt = fehl(ks[0]), '–'
        else:
            b_txt = '%s [%s]' % (de(v[ks[0]], nd, True), ki(v[ks[1]], v[ks[2]], nd))
            p_txt = de_p(v[ks[3]])
        fl = '–' if v[ks[0]] is None else fall(v[ks[1]], v[ks[2]], roh('S10.SESOI.%s.PRE.ALL.X' % zz), zz != 'SBJ')
        z.append((kk, bez, ZIELE[zz], n_txt, b_txt, p_txt, fl, ', '.join(ks)))
        notiere('%s %s' % (kk, zz), '%s %s' % (bez, ZIELE[zz]), ks, ' | '.join([n_txt, b_txt, p_txt, 'Fall ' + fl]))
tabelle(['Kennung', 'Variante', 'Zielgröße', 'n IG / KG', 'b1 [95-%-KI]', 'p', 'Fall', 'Kennung der Ergebnisdatei'], z)
md('**K-08.8 Bootstrap-KI der adjustierten Differenz (Perzentil, B = 10 000, Startwert 20260924, nachträglich O8, N3):**')
md()
z = []
for zz in KONF:
    nd = ND_DIFF[zz]
    ks = ['S19.%s.%s.X.ITT.BOOT' % (x, zz) for x in ('BKIU', 'BKIO', 'BSD', 'BMCU', 'BMCO', 'BNGUELT', 'BNVERW')]
    v = {k: roh(k, 'K-08.8') for k in ks}
    txt = ki(v[ks[0]], v[ks[1]], nd)
    z.append(('K-08.8', ZIELE[zz], txt, de(v[ks[2]], nd), '%s · %s' % (de(v[ks[3]], nd + 1), de(v[ks[4]], nd + 1)), '%d · %d' % (v[ks[5]], v[ks[6]]), ', '.join(ks)))
    notiere('K-08.8 ' + zz, 'Bootstrap-KI ' + ZIELE[zz], ks, txt)
tabelle(['Kennung', 'Zielgröße', 'Bootstrap-KI', 'SD der b1*', 'MC-SE untere · obere Grenze', 'gültige · verworfene Ziehungen', 'Kennung der Ergebnisdatei'], z)
md('**K-08.9 Deskription der Per-Protokoll-Mengen und des Familiarisierungssets (R5, Tab. H4), M ± SD der Bestwerte:**')
md()
z = []
for zz in KONF:
    ndm = ND_MSD[zz]
    zelle = []
    ks = []
    for s, menge, var, bez in [('S16', 'PP6IG', 'HAUPT', 'PP6 IG'), ('S17', 'PP5IG', 'HAUPT', 'PP5 IG'), ('S17', 'PP7IG', 'HAUPT', 'PP7 IG'), ('S17', 'FAMSIG', 'FAMB', 'FAMS IG'), ('S17', 'FAMSKG', 'FAMB', 'FAMS KG')]:
        for t in ('PRE', 'POST'):
            km, ksd = ['%s.%s.%s.%s.%s.%s' % (s, x, zz, t, menge, var) for x in ('M', 'SD')]
            ks += [km, ksd]
            zelle.append(msd(roh(km, 'K-08.9'), roh(ksd, 'K-08.9'), ndm))
    z.append(('K-08.9', ZIELE[zz], *zelle, ', '.join(ks)))
    notiere('K-08.9 ' + zz, 'Deskription PP und FAMS ' + ZIELE[zz], ks, ' | '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'PP6 IG prä', 'PP6 IG post', 'PP5 IG prä', 'PP5 IG post', 'PP7 IG prä', 'PP7 IG post', 'FAMS IG prä', 'FAMS IG post', 'FAMS KG prä', 'FAMS KG post', 'Kennung der Ergebnisdatei'], z)
md('n der Per-Protokoll- und Familiarisierungssets (K-08.10, IG, KG-Teil gleich dem ITT-KG):')
md()
z = []
for zz in KONF:
    ks = ['S08.N.%s.X.%s.X' % (zz, m) for m in ('PP5IG', 'PP6IG', 'PP7IG', 'AK9IG', 'FAMSIG', 'FAMSKG')] + ['S08.INF.%s.X.%s.X' % (zz, m) for m in ('ITT', 'PP5', 'PP6', 'PP7', 'FAMS')]
    v = [ganz(k, 'K-08.10') for k in ks]
    txt = 'PP5 %d · PP6 %d · PP7 %d · AK9 %d · FAMS IG %d, KG %d · inferenzfähig (ITT, PP5, PP6, PP7, FAMS): %s' % (v[0], v[1], v[2], v[3], v[4], v[5], ', '.join(str(x) for x in v[6:]))
    z.append(('K-08.10', ZIELE[zz], txt, ', '.join(ks)))
    notiere('K-08.10 ' + zz, 'Setgrößen ' + ZIELE[zz], ks, txt)
tabelle(['Kennung', 'Zielgröße', 'n je Set und Merkmal INF', 'Kennung der Ergebnisdatei'], z)
md('**K-08.11 Familiarisierung Variante a, nur deskriptiv: Δ = Post − Prä (Bestwert) je Gruppe und Zahl der Termine (Tab. H4):**')
md()
z = []
for zz in KONF:
    nd = ND_DIFF[zz]
    zelle = []
    ks = []
    for g in ('ITTIG', 'ITTKG'):
        for f in ('F1', 'F2'):
            kn, km, ksd = ['S17.%s.%s.DIFF.%s.%s' % (x, zz, g, f) for x in ('N', 'M', 'SD')]
            ks += [kn, km, ksd]
            n = ganz(kn, 'K-08.11')
            m, s = roh(km, 'K-08.11'), roh(ksd, 'K-08.11')
            zelle.append('n = %d: %s' % (n, 'fehlend (%s)' % grund(km) if m is None else ('%s ± %s' % (de(m, nd, True), de(s, nd)) if s is not None else de(m, nd, True))))
    z.append(('K-08.11', ZIELE[zz], *zelle, ', '.join(ks)))
    notiere('K-08.11 ' + zz, 'Familiarisierung Variante a ' + ZIELE[zz], ks, ' | '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'IG ein Termin', 'IG zwei Termine', 'KG ein Termin', 'KG zwei Termine', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-09 Poweranalyse
md('## K-09 Sensitivitäts-Poweranalyse, Standardweg (4.7, 6.2, Anhang G)')
md()
md('F-Test des Gruppenterms, df1 = 1, df2 = N − 4, λ = d²·n_IG·n_KG/N, α = 0,05, ohne Kovariatengewinn (O9). MDES = kleinster Effekt d mit Power 0,80, MDES/0,2 = Vielfaches des SESOI. Power bei den im Plan genannten Vorab-Erwartungen (D006 und D011 nur 10 m, D037 und D093 für die konfirmatorischen Zielgrößen).')
md()
z = []
for i, zz in enumerate(['Z10', 'Z30', 'CM', 'SBJ'], 1):
    kk = 'K-09.%d' % i
    ks = ['S18.%s.%s.X.ITT.X' % (x, zz) for x in ('NTOT', 'DF1', 'DF2', 'FCRIT')]
    v = [roh(k, kk) for k in ks]
    if zz == 'Z10':
        kp = ['S18.POW.Z10.X.ITT.D006', 'S18.POW.Z10.X.ITT.D011']
        ks += kp
        pw = [roh(k, kk) for k in kp]
        mdes_txt, pow_txt = '–', 'd = 0,06: %s · d = 0,11: %s' % (de(pw[0], 3), de(pw[1], 3))
    else:
        km = ['S18.MDES.%s.X.ITT.X' % zz, 'S18.MDESR.%s.X.ITT.X' % zz]
        kp = ['S18.POW.%s.X.ITT.D037' % zz, 'S18.POW.%s.X.ITT.D093' % zz]
        ks += km + kp
        mv = [roh(k, kk) for k in km]
        pw = [roh(k, kk) for k in kp]
        mdes_txt = '%s (%s × SESOI)' % (de(mv[0], 2), de(mv[1], 1))
        pow_txt = 'd = 0,37: %s · d = 0,93: %s' % (de(pw[0], 2), de(pw[1], 2))
    z.append((kk, ZIELE[zz], '%d' % v[0], '%d, %d' % (v[1], v[2]), de(v[3], 2), mdes_txt, pow_txt, ', '.join(ks)))
    notiere(kk, 'Poweranalyse ' + ZIELE[zz], ks, ' | '.join(['N %d' % v[0], mdes_txt, pow_txt]))
tabelle(['Kennung', 'Zielgröße', 'N', 'df1, df2', 'F_krit', 'MDES (Power 0,80)', 'Power bei Vorab-Erwartung', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-10 Adhärenz, Belastung, UE
md('## K-10 Adhärenz, Belastung, unerwünschte Ereignisse (4.6, 4.7, 5.1, Tab. H2, Tab. H5)')
md()
z = []
def z_fb(kk, bez, ks, fmt):
    vals = [roh(k, kk) for k in ks]
    txt = fmt(vals)
    z.append((kk, bez, txt, ', '.join(ks)))
    notiere(kk, bez, ks, txt)
z_fb('K-10.1', 'Meldungen des Fragebogens A gesamt', ['S06.NMELD.FB.X.ALL.X'], lambda v: '%d' % v[0])
z_fb('K-10.2', 'korrigierte Meldungen (Fallkorrekturen) · Dublettenpaare · Sammelmeldungspaare', ['S06.NKORR.FB.X.ALL.X', 'S06.NDUBL.FB.X.ALL.X', 'S06.NSAMM.FB.X.ALL.X'], lambda v: '%d · %d · %d' % tuple(v))
z_fb('K-10.3', 'Meldungen je Status: ganz · teilweise · gar nicht', ['S06.NSTAT.FB.X.IG.GANZ', 'S06.NSTAT.FB.X.IG.TEILW', 'S06.NSTAT.FB.X.IG.GARN'], lambda v: '%d · %d · %d' % tuple(v))
z_fb('K-10.4', 'zugeteilte IG-Spieler (Nenner 12 Einheiten je Spieler)', ['S07.NZUG.ADH.X.IG.X'], lambda v: '%d' % v[0])
z_fb('K-10.5', 'Summe und Umsetzungsrate GANZ', ['S07.SUMME.ADH.X.IG.GANZ', 'S07.RATE.ADH.X.IG.GANZ'], lambda v: '%d Einheiten, %s %%' % (v[0], de(100 * v[1], 1)))
z_fb('K-10.6', 'Summe und Beteiligungsrate GT (ganz oder teilweise)', ['S07.SUMME.ADH.X.IG.GT', 'S07.RATE.ADH.X.IG.GT'], lambda v: '%d Einheiten, %s %%' % (v[0], de(100 * v[1], 1)))
z_fb('K-10.7', 'Untergrenzen: Summe und Rate wochengedeckelt (WOCAP) · nach distinkten Nummern (DIST)', ['S07.SUMME.ADH.X.IG.WOCAP', 'S07.RATE.ADH.X.IG.WOCAP', 'S07.SUMME.ADH.X.IG.DIST', 'S07.RATE.ADH.X.IG.DIST'], lambda v: '%d, %s %% · %d, %s %%' % (v[0], de(100 * v[1], 1), v[2], de(100 * v[3], 1)))
z_fb('K-10.8', 'Median und Mittel der Zählung GANZ je zugeteiltem Spieler', ['S07.MED.ADH.X.IG.GANZ', 'S07.MITT.ADH.X.IG.GANZ'], lambda v: 'Median %s, Mittel %s' % (de(v[0], 1), de(v[1], 2)))
z_fb('K-10.9', 'Spieler mit mindestens einer Meldung (gleich welchen Status)', ['S07.NMELDSP.ADH.X.IG.X'], lambda v: '%d' % v[0])
z_fb('K-10.10', 'Spieler mit GANZ ≥ 6 · ≥ 9 (Hauptzählung)', ['S07.GE06.ADH.X.IG.GANZ', 'S07.GE09.ADH.X.IG.GANZ'], lambda v: '%d · %d' % tuple(v))
z_fb('K-10.11', 'Spieler mit ≥ 6 · ≥ 9 nach WOCAP und nach DIST', ['S07.GE06.ADH.X.IG.WOCAP', 'S07.GE09.ADH.X.IG.WOCAP', 'S07.GE06.ADH.X.IG.DIST', 'S07.GE09.ADH.X.IG.DIST'], lambda v: 'WOCAP %d · %d, DIST %d · %d' % tuple(v))
z_fb('K-10.12', 'unerwünschte Ereignisse (H007 = 1): Meldungen gesamt · ganz · teilweise · gar nicht · Spieler', ['S07.UE.FB.X.IG.X', 'S07.UE.FB.X.IG.GANZ', 'S07.UE.FB.X.IG.TEILW', 'S07.UE.FB.X.IG.GARN', 'S07.UESP.FB.X.IG.X'], lambda v: '%d · %d · %d · %d · %d Spieler' % tuple(v))
for kk, zz, bez, nd in [('K-10.13', 'CR10', 'CR-10 der Meldungen „ganz“', 1), ('K-10.14', 'LOAD', 'sRPE-Load der Meldungen „ganz“ (AU, CR-10 mal Solldauer der Woche)', 1)]:
    ks = ['S07.%s.%s.X.IG.GANZ' % (x, zz) for x in ('N', 'M', 'SD', 'MED', 'MIN', 'MAX')]
    z_fb(kk, bez, ks, lambda v, nd=nd: 'n = %d, %s ± %s, Median %s, Min %s, Max %s' % (v[0], de(v[1], nd), de(v[2], nd), de(v[3], nd), de(v[4], nd), de(v[5], nd)))
tabelle(['Kennung', 'Größe', 'Wert', 'Kennung der Ergebnisdatei'], z)
md('**K-10.15 Verteilung der Zählung GANZ und Schwellenlandschaft (Tab. H2, Tab. H5):**')
md()
ks_v = ['S07.V%02d.ADH.X.IG.GANZ' % i for i in range(13)]
ks_g = ['S07.GE%02d.ADH.X.IG.GANZ' % i for i in range(1, 13)]
vv = [ganz(k, 'K-10.15') for k in ks_v]
vg = [ganz(k, 'K-10.15') for k in ks_g]
tabelle(['Einheiten „ganz“'] + [str(i) for i in range(13)], [['Spieler mit genau'] + vv, ['Spieler mit mindestens', '–'] + vg])
notiere('K-10.15', 'Verteilung und Schwellenlandschaft GANZ', ks_v + ks_g, 'genau: ' + ' '.join(str(x) for x in vv) + ' | mindestens: ' + ' '.join(str(x) for x in vg))
md('**K-10.16 Wochenverlauf (Tab. H2): Wochenanteil der Meldungen „ganz“ (Meldungen / (2 · zugeteilte Spieler)), CR-10 und sRPE-Load je Programmwoche:**')
md()
z = []
for w in range(1, 7):
    kw = 'S07.ANTW.ADH.W%d.IG.GANZ' % w
    kc = ['S07.%s.CR10.W%d.IG.GANZ' % (x, w) for x in ('N', 'M', 'SD')]
    kl = ['S07.%s.LOAD.W%d.IG.GANZ' % (x, w) for x in ('N', 'M', 'SD')]
    a = roh(kw, 'K-10.16')
    c = [roh(k, 'K-10.16') for k in kc]
    l = [roh(k, 'K-10.16') for k in kl]
    ctxt = 'n = %d, %s' % (c[0], 'fehlend (%s)' % grund(kc[1]) if c[1] is None else msd(c[1], c[2], 1) if c[2] is not None else de(c[1], 1))
    ltxt = 'n = %d, %s' % (l[0], 'fehlend (%s)' % grund(kl[1]) if l[1] is None else msd(l[1], l[2], 1) if l[2] is not None else de(l[1], 1))
    z.append(('K-10.16', 'W%d' % w, '%s %%' % de(100 * a, 1), ctxt, ltxt, ', '.join([kw] + kc + kl)))
    notiere('K-10.16 W%d' % w, 'Wochenverlauf W%d' % w, [kw] + kc + kl, ' | '.join(['%s %%' % de(100 * a, 1), ctxt, ltxt]))
tabelle(['Kennung', 'Woche', 'Wochenanteil ganz', 'CR-10 (n, M ± SD)', 'sRPE-Load (n, M ± SD)', 'Kennung der Ergebnisdatei'], z)
md('**K-10.17 Antragskriterium (AK9, ≥ 9 von 12 Einheiten „ganz“): Einzelwerte Δ = BEST post − BEST prä je Spieler (Tab. H2), keine Inferenz:**')
md()
ak_codes = sorted(set(k.split('.')[4][1:] for k in R if k.startswith('S16.DIFF.')))
z = []
for c in ak_codes:
    ks = ['S16.DIFF.%s.DIFF.P%s.AK9' % (zz, c) for zz in KONF]
    v = [roh(k, 'K-10.17') for k in ks]
    txt = [('fehlend (%s)' % grund(k)) if x is None else de(x, ND_DIFF[zz], True) + ' ' + EINHEIT[zz] for k, x, zz in zip(ks, v, KONF)]
    z.append(('K-10.17', c, *txt, ', '.join(ks)))
    notiere('K-10.17 ' + c, 'Antragskriterium Δ ' + c, ks, ' | '.join(txt))
tabelle(['Kennung', 'Code', 'Δ 30 m', 'Δ 505-Seitenmittel', 'Δ Standweitsprung', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-11 Versuche und Ausfälle
md('## K-11 Versuche, Ausfälle, Bestwert-Bias (4.4, Tab. H1)')
md()
z = []
for kk, bez, ks, fmt in [('K-11.1', 'Zeilen der Versuchsdaten (Raster)', ['S01.NZEIL.X.X.ALL.X'], lambda v: '%d' % v[0]),
                         ('K-11.2', 'auslösegestörte Sprintläufe prä · post', ['S02.NAUSL.X.PRE.ALL.X', 'S02.NAUSL.X.POST.ALL.X'], lambda v: '%d · %d' % tuple(v))]:
    vals = [roh(k, kk) for k in ks]
    txt = fmt(vals)
    z.append((kk, bez, txt, ', '.join(ks)))
    notiere(kk, bez, ks, txt)
tabelle(['Kennung', 'Größe', 'Wert', 'Kennung der Ergebnisdatei'], z)
md('**K-11.3 gültige Versuche je Zielgröße und Zeitpunkt (alle Spieler) und mittlere Zahl gültiger Versuche je Spieler und Gruppe (S09, Bezugsmenge: Spieler mit Zeilen zum Zeitpunkt, post ohne nicht angetretene):**')
md()
z = []
for zz in ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'SBJ']:
    ks = ['S02.NGUELT.%s.%s.ALL.X' % (zz, t) for t in ('PRE', 'POST')] + ['S09.KMEAN.%s.%s.%s.X' % (zz, t, g) for t in ('PRE', 'POST') for g in ('IG', 'KG')]
    v = [roh(k, 'K-11.3') for k in ks]
    zeile = ('K-11.3', ZIELE[zz], '%d' % v[0], '%d' % v[1], de(v[2], 2), de(v[3], 2), de(v[4], 2), de(v[5], 2), ', '.join(ks))
    z.append(zeile)
    notiere('K-11.3 ' + zz, 'gültige Versuche ' + ZIELE[zz], ks, ' | '.join(zeile[2:8]))
tabelle(['Kennung', 'Zielgröße', 'gültig prä', 'gültig post', 'k̄ prä IG', 'k̄ prä KG', 'k̄ post IG', 'k̄ post KG', 'Kennung der Ergebnisdatei'], z)
md('**K-11.4 ungültige Zeilen je Ausfallkategorie (S03: TECH technischer Ausfall, ZEIT dritter Versuch aus Zeitmangel, FEHL nicht wiederholbarer Fehlversuch, FALSCH falsch aufgenommen, NANG nicht angetreten (nur post), AUSL auslösegestört):**')
md()
z = []
KAT = ['TECH', 'ZEIT', 'FEHL', 'FALSCH', 'NANG', 'AUSL']
summe = {(t, g, kat): 0 for t in ('PRE', 'POST') for g in ('IG', 'KG') for kat in KAT}
for zz in ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'SBJ']:
    for t in ('PRE', 'POST'):
        zelle = []
        ks = []
        for g in ('IG', 'KG'):
            for kat in KAT:
                if kat == 'NANG' and t == 'PRE':
                    zelle.append('–')
                    continue
                k = 'S03.NKAT.%s.%s.%s.%s' % (zz, t, g, kat)
                ks.append(k)
                n = ganz(k, 'K-11.4')
                summe[(t, g, kat)] += n
                zelle.append(str(n))
        z.append(('K-11.4', ZIELE[zz], 'prä' if t == 'PRE' else 'post', *zelle, ', '.join(ks)))
        notiere('K-11.4 %s %s' % (zz, t), 'Ausfallkategorien %s %s' % (ZIELE[zz], t), ks, ' '.join(zelle))
for t in ('PRE', 'POST'):
    zelle = []
    for g in ('IG', 'KG'):
        for kat in KAT:
            zelle.append('–' if (kat == 'NANG' and t == 'PRE') else str(summe[(t, g, kat)]))
    z.append(('K-11.4', 'Summe über die sechs Zielgrößen (abgeleitet)', 'prä' if t == 'PRE' else 'post', *zelle, 'Summe der Zeilen oben'))
    notiere('K-11.4 Summe %s' % t, 'Ausfallkategorien Summe %s' % t, [], ' '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'Zeit', 'IG TECH', 'IG ZEIT', 'IG FEHL', 'IG FALSCH', 'IG NANG', 'IG AUSL', 'KG TECH', 'KG ZEIT', 'KG FEHL', 'KG FALSCH', 'KG NANG', 'KG AUSL', 'Kennung der Ergebnisdatei'], z)
md('**K-11.5 fehlende Werte je Zielgröße (Teilnehmerfluss S08 Regel 8): Spieler ohne BEST prä · ohne BEST post, je Gruppe:**')
md()
z = []
for zz in ZIELE:
    ks = ['S08.%s.%s.X.%s.X' % (x, zz, g) for x in ('FLOPRE', 'FLOPOST') for g in ('IG', 'KG')]
    v = [ganz(k, 'K-11.5') for k in ks]
    txt = 'ohne Prä: IG %d, KG %d · ohne Post: IG %d, KG %d' % tuple(v)
    z.append(('K-11.5', ZIELE[zz], txt, ', '.join(ks)))
    notiere('K-11.5 ' + zz, 'fehlende Werte ' + ZIELE[zz], ks, txt)
tabelle(['Kennung', 'Zielgröße', 'Wert', 'Kennung der Ergebnisdatei'], z)
md('**K-11.6 Bestwert-Bias, gemessen (S11): Δ = best(V1, V2, V3) − best(V1, V2) über Spieler mit drei gültigen Versuchen, Mittel und Mittel/SESOI, nur deskriptiv:**')
md()
z = []
for zz in ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'SBJ']:
    zelle = []
    ks = []
    for t in ('PRE', 'POST'):
        kn, kd, ks_ = ['S11.%s.%s.%s.ALL.X' % (x, zz, t) for x in ('N', 'DMEAN', 'DSESOI')]
        ks += [kn, kd, ks_]
        n, d, s = ganz(kn, 'K-11.6'), roh(kd, 'K-11.6'), roh(ks_, 'K-11.6')
        zelle.append('n = %d, %s' % (n, 'fehlend (%s)' % grund(kd) if d is None else '%s %s (%s × SESOI)' % (de(d, 4 if zz != 'SBJ' else 2, True), EINHEIT[zz], de(s, 2, True))))
    z.append(('K-11.6', ZIELE[zz], zelle[0], zelle[1], ', '.join(ks)))
    notiere('K-11.6 ' + zz, 'Bestwert-Bias ' + ZIELE[zz], ks, ' | '.join(zelle))
tabelle(['Kennung', 'Zielgröße', 'prä', 'post', 'Kennung der Ergebnisdatei'], z)

# ---------------------------------------------------------------- K-12 Einschluss je Spieler und Einzelwerte für Abb. 2
md('## K-12 Einschluss je Spieler, Reifestatus, Bestwerte und Adhärenz (Abb. 1, Abb. 2, Tab. H2)')
md()
md('Eingeschlossen ist jeder zugeteilte Spieler (ITT, CONSORT Box 6). Ein fehlender Wert schließt den Spieler nur aus der Zielgröße aus, in der er fehlt, keine Fortschreibung. ✓ = im ITT-Set der Zielgröße (BEST prä, BEST post und %PAH vorhanden). Die Zählung je Spalte ergibt die Nenner in K-04 und K-06. Bestwerte prä und post der konfirmatorischen Zielgrößen und %PAH je Spieler sind die Einzelpunkte von Abb. 2 (Post dort auf den mittleren %PAH des Sets adjustiert, K-06.5). Adhärenz GANZ je IG-Spieler für Tab. H2.')
md()
z = []
for c in codes:
    g = 'IG' if c[:2] in ('HL', 'BW') else 'KG'
    pah = roh('S05.PAH.PAH.PRE.P%s.X' % c, 'K-12')
    mit = ['✓' if ganz('S08.MITGL.%s.X.P%s.ITT' % (zz, c), 'K-12') == 1 else '–' for zz in ZIELE]
    best = []
    for zz in KONF:
        for t in ('PRE', 'POST'):
            v = roh('S04.BEST.%s.%s.P%s.X' % (zz, t, c), 'K-12')
            best.append('–' if v is None else de(v, 3 if zz != 'SBJ' else 0))
    if g == 'IG':
        ka = 'S07.ADH.ADH.X.P%s.GANZ' % c
        a = roh(ka, 'K-12')
        adh = 'nicht erhebbar' if a is None else '%d' % a
    else:
        adh = '–'
    gr = []
    if ganz('S08.MITGL.Z30.X.P%s.ITT' % c) == 0 and all(m == '–' for m in mit):
        gr.append('ohne %PAH' if pah is None else 'Post nicht angetreten')
    zeile = ('K-12', c, g, verein(c), 'fehlend' if pah is None else de(pah, 2), *mit, *best, adh, ', '.join(gr) if gr else '—')
    z.append(zeile)
    notiere('K-12 ' + c, 'Spieler ' + c, ['S05.PAH.PAH.PRE.P%s.X' % c] + ['S08.MITGL.%s.X.P%s.ITT' % (zz, c) for zz in ZIELE] + ['S04.BEST.%s.%s.P%s.X' % (zz, t, c) for zz in KONF for t in ('PRE', 'POST')] + (['S07.ADH.ADH.X.P%s.GANZ' % c] if g == 'IG' else []), ' | '.join(str(x) for x in zeile[4:]))
tabelle(['Kennung', 'Code', 'Gruppe', 'Verein', '%PAH', '5 m', '10 m', '30 m', '505 L', '505 R', '505 M', 'SBJ', 'BEST 30 m prä', 'BEST 30 m post', 'BEST 505 M prä', 'BEST 505 M post', 'BEST SBJ prä', 'BEST SBJ post', 'GANZ', 'Anmerkung'], z)
md('Zahl der Spieler mit %%PAH (K-12.1): IG %d · KG %d (S05.NPAH.PAH.PRE.IG.X, S05.NPAH.PAH.PRE.KG.X).' % (ganz('S05.NPAH.PAH.PRE.IG.X', 'K-12.1'), ganz('S05.NPAH.PAH.PRE.KG.X', 'K-12.1')))
notiere('K-12.1', 'Spieler mit %PAH', ['S05.NPAH.PAH.PRE.IG.X', 'S05.NPAH.PAH.PRE.KG.X'], 'IG %d · KG %d' % (ganz('S05.NPAH.PAH.PRE.IG.X'), ganz('S05.NPAH.PAH.PRE.KG.X')))
md()

# ---------------------------------------------------------------- Abdeckung und Abschluss
nicht_verwendet = [k for k in R if k not in verwendet]
umf_T = [k for k in R if UMF.get(muster(k), {}).get('umfang_N4') == 'T']
fehlend_T = [k for k in umf_T if k not in verwendet]
md('## Abdeckung')
md()
md('Kennungen der Ergebnisdatei: %d, davon in diesem Blatt verwendet: %d. Kennungen mit Berichtsort Text (T) nach dem Umfangsdokument: %d, davon hier ohne Zeile: %d%s. Nicht verwendete Kennungen sind Zwischenwerte (I), Mittelwerte der Versuche und Bestwerte der deskriptiven Zielgrößen je Spieler, Setmitgliedschaften der Per-Protokoll-Mengen und Steuergrößen. Sie bleiben in der Ergebnisdatei abrufbar.' % (
    len(R), len(verwendet), len(umf_T), len(fehlend_T), '' if not fehlend_T else ' (' + ', '.join(fehlend_T[:20]) + ')'))
md()
md('Werte mit fehlendem Eintrag in der Ergebnisdatei erscheinen als „fehlend (Grund)“ nach Spezifikation G.1 Nr. 4. Semikolons kommen in diesem Blatt nicht vor.')

text = '\n'.join(zeilen_md) + '\n'
if chr(59) in text:
    raise SystemExit('Semikolon im Kennzahlenblatt')
with open(ZIEL_MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
with open(ZIEL_CSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['k_kennung', 'bezeichnung', 'kennungen_ergebnisdatei', 'rohwerte', 'darstellung', 'berichtsort'])
    for row in werte_csv:
        w.writerow(row)
meldung = 'geschrieben: %s und %s · Kennungen verwendet: %d von %d · Zeilen der Anlage: %d · T-Kennungen ohne Zeile: %d' % (ZIEL_MD, ZIEL_CSV, len(verwendet), len(R), len(werte_csv), len(fehlend_T))
print(meldung)
with open(os.path.splitext(ZIEL_MD)[0] + '.txt', 'w', encoding='utf-8') as f:
    f.write('Kennzahlen_2026-09-25.py, Laufprotokoll\n')
    f.write('Datum: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    f.write('Eingang: ' + ERG + ' (SHA-256 ' + sha_erg + ')\n')
    f.write('Kennungslisten: ' + SPEZ_K + ', ' + UMF_K + '\n')
    f.write(meldung + '\n')


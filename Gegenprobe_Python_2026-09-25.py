# -*- coding: utf-8 -*-
"""
Gegenprobe_Python_2026-09-25.py — erste Implementierung (Python), Ergebnisdatei nach Spezifikation G.1
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Phase 6.1

Zweck
  Die Python-Kette (Code-Stand 12.09.2026, Skripte Auswertung_B0 bis B9 und F1) ist nach dem
  Auswertungsverfahren die Gegenprobe zur berichteten R-Rechnung der blinden zweiten Instanz.
  Der Code-Stand vom 12.09. liegt vor der Spezifikation vom 24.09. (Stand Nachtrag 2): Er liest
  das Workbook statt des eingefrorenen Datenstands, kennt weder die Schrittfolge S01 bis S19
  noch die Kennungen der Anlage _Kennungen.csv, rechnet Größen, die mit Nachtrag 2 entfallen
  sind (partielles η², MDC, TE/√n, Korrelationen), und weicht in Einzelregeln von den am 24.09.
  entschiedenen Punkten ab (J mit df = n − 2 statt n − 4, zentrierte Kovariaten, Poweranalyse
  mit R²). Dieses Skript ist deshalb die neue, datierte Fassung der Gegenprobe: dieselbe
  Rechenlogik (numpy, scipy) auf den Datenstand_2026-09-24 nach den Regeln der Spezifikation,
  mit Ausgabe jeder der 1 535 Kennungen der Anlage (ausgeschrieben je Datenstand, Zahl im Laufprotokoll) nach G.1.

Änderungsvermerk Fassung 2 (25.09.2026, nach der unabhängigen Durchsicht 6.2, Befunde 1 bis 14)
  Ergebnisneutral, geprüft durch erneuten Gesamtlauf und erneuten Abgleich 6.1: S03 Widerspruchsprüfung
  über alle Post-Zeilen nicht angetretener Spieler (Befund 1) · S05 Vorrang „Eingang fehlt“ vor
  „außerhalb Gültigkeitsbereich“ wie in der berichteten Rechnung (Befund 2) · S19 Fehlerpfad bei weniger
  als zwei gültigen Ziehungen (Befund 4) · R03 zusätzlich über den S15-Rechenweg (Befund 5) · S01 Seite
  außerhalb 505 muss leer oder „–“ sein (Befund 7) · Abbruch bei doppelten Schlüsseln in den Anlagen
  (Befund 8) · Funktionsname ausloesepruefung, fmt vereinfacht (Befund 13). Die Grafikdateien tragen
  den Zusatz _Python, damit sie neben den Dateien der R-Rechnung liegen können (Befund 6, bewusst).
  Fassung 1 (SHA-256 943a4553fd7dfea4a3ce902a27d9e0f3754c308676d7bceed3e1eb5306e841ea) hat den
  Abgleich 6.1 bestanden, Fassung 2 wiederholt ihn.

Änderungsvermerk Fassung 1 (25.09.2026, erste Fassung dieses Skripts)
  Übernommen aus der Kette vom 12.09.: Gültigkeitsregel und Auslöseprüfung (B1), Aggregation
  Bestwert/Mittelwert und 505-Seitenmittel (B2), typischer Fehler als gepoolte Innerspieler-SD
  mit χ²-Intervall (B3), Analysesets und Fallzahlregel (B4/B9), Deskription ohne Tests (B5),
  Kleinste-Quadrate-ANCOVA mit t-Inferenz, Brown-Forsythe, Shapiro-Wilk, Steigungsmodelle (B6/B7),
  Sensitivitätsvarianten (B8/B9), Fragebogenregeln (F1: Fallkorrekturen, Kalenderregel,
  Dubletten, Untergrenzen).
  Neu nach Spezifikation: Datenstand als Eingang mit Prüfsummen (S01), Ausfallkategorien nach
  Vokabular-Anlage (S03), %PAH nach Khamis-Roche aus den Rohgrößen mit Interpolation (S05),
  Umsetzungsrate, Verteilung, Wochenanteil, CR-10 und sRPE-Load nach Nachtrag 2 (S07),
  Teilnehmerfluss, Box 6, Anteile, Menge ANA (S08), Bestwert-Bias (S11), adjustierte Mittelwerte
  am Setmittel (S13), Vorab-Prüfung in BPAH und Residuen-SD je Gruppe (S14), Hedges' g mit
  J(df = n − 2) und unadjustierte Differenz (S15), Poweranalyse nach dem Standardweg ohne R²
  (S18), Bootstrap-KI mit Monte-Carlo-Fehler (S19), Referenztests R01 bis R13 (Teil G.2),
  Grenzfälle mit Sollwerten von Hand (Phase 4.2), Ergebnisdatei nach G.1.
  Festlegungen aus der Blindrechnung vom 25.09.2026 (Antworten R1 bis R5, Anmerkungen A1 bis A13
  des Rückfragenprotokolls), hier gleich umgesetzt: R1 Lesart a (SESOI post intern für S11),
  R2 Zuordnung der Gründe, R3 Sammelmeldungspaar = Komplement des Dublettenpaars, R4 Fallzahlregel
  in BPAH für beide Vorab-Prüfungen, R5 Toleranz R08 (W 1e-5, F 1e-4), A1 kein VERW für die
  Vorab-Prüfungen, A5 NKORR = Meldungen mit CASE in der Korrekturliste, A7 FLPRE nach S02-Gültigkeit,
  A8 Abstand ≤ 300 s eingeschlossen, A9 Zusatzprüfungen der Zuordnung, A10 bei INF = 0 nur n_IG und
  n_KG, A11 bei INF = 0 keine Grafik.

Eingang (Ordner Blindrechnung_R_2026-09-24, SHA-256 der Dateien im Laufprotokoll dieses Skripts)
  Datenstand_2026-09-24/Versuchsdaten.csv, Personendaten.csv, Fragebogen_A.csv,
  Zuordnung_Fragebogen.csv, Listenplatz_IG.csv, Pruefsummen.txt
  Spezifikation_2026-09-24_Kennungen.csv, _Konstanten.csv, _Koeffizienten_KR.csv, _Vokabular.csv,
  _Fragebogen.csv, _Referenzdaten.csv, _Referenzdaten_Daten.csv

Aufruf
  python Gegenprobe_Python_2026-09-25.py <Eingangsordner> [Ausgabeordner]
  Eingangsordner = Blindrechnung_R_2026-09-24 (mit Anlagen und Datenstand_2026-09-24).
  Ausgabeordner voreingestellt: Ordner dieses Skripts.
Ausgabe
  Ergebnisse_Python_2026-09-25.csv (G.1) · Gegenprobe_Python_2026-09-25.txt (Laufprotokoll mit
  Referenztests, Grenzfällen, Prüfsummen) · S14_QQ_<ZIEL>_Python.png, S14_Linearitaet_<ZIEL>_Python.png
Regeln
  Gerechnet wird nur hier, keine Zahl von Hand. Abbruch mit Meldung statt stiller Korrektur
  (0.5 Nr. 10). Keine Rundung. Fehlende Werte mit Grund nach G.1 Nr. 4.
"""
import sys, os, io, csv, math, hashlib, datetime, platform
from collections import OrderedDict, Counter, defaultdict
import numpy as np
import scipy
from scipy import stats, optimize

FASSUNG = '2026-09-25'
FASSUNG_NR = 2
SKRIPT = os.path.basename(__file__)
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 2:
    sys.exit('Aufruf: python %s <Eingangsordner Blindrechnung_R_2026-09-24> [Ausgabeordner]' % SKRIPT)
EINGANG = os.path.abspath(sys.argv[1])
AUSGABE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else HERE
DATENSTAND = os.path.join(EINGANG, 'Datenstand_2026-09-24')
ANLAGE = lambda n: os.path.join(EINGANG, 'Spezifikation_2026-09-24_' + n + '.csv')
ERGEBNIS = os.path.join(AUSGABE, 'Ergebnisse_Python_%s.csv' % FASSUNG)
PROTOKOLL = os.path.join(AUSGABE, 'Gegenprobe_Python_%s.txt' % FASSUNG)

buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); buf.write(s + '\n')

class Abbruch(Exception):
    pass
def pruefe(bedingung, *meldung):
    if not bedingung:
        raise Abbruch('ABBRUCH: ' + ' '.join(str(m) for m in meldung))
def _bei_fehler(typ, wert, tb):
    """Jeder Fehler beendet den Lauf mit Meldung im Protokoll (0.5 Nr. 10), Status 1."""
    import traceback
    P('\n' + ''.join(traceback.format_exception(typ, wert, tb)) if typ is not Abbruch else '\n' + str(wert))
    P('Lauf abgebrochen:', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))
    with open(PROTOKOLL, 'w', encoding='utf-8') as f: f.write(buf.getvalue())
    sys.exit(1)
sys.excepthook = _bei_fehler

# =====================================================================================
# A  Konstanten (Anlage _Konstanten.csv) und Gründe (G.1 Nr. 4, Zuordnung nach R2)
# =====================================================================================
G_EINGANG = 'Eingang fehlt'
G_FALLZAHL = 'Fallzahlregel'
G_RANG = 'Rang'
G_WENIG = 'zu wenige Werte'
G_KONST = 'konstant'
G_BEREICH = 'außerhalb Gültigkeitsbereich'
G_NICHTERH = 'nicht erhebbar'
G_NULLST = 'keine Nullstelle'
GRUENDE = {G_EINGANG, G_FALLZAHL, G_RANG, G_WENIG, G_KONST, G_BEREICH, G_NICHTERH, G_NULLST}

ZIELE7 = ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']
ZIELE6 = ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']
KONF = ['Z30', 'CM', 'SBJ']
TEST_VON = {'Z05': ('Sprint_5m', '–'), 'Z10': ('Sprint_10m', '–'), 'Z30': ('Sprint_30m', '–'),
            'SBJ': ('Standweitsprung', '–'), 'CL': ('COD_505', 'L'), 'CR': ('COD_505', 'R')}
ZIEL_VON = {v: k for k, v in TEST_VON.items()}
RICHTUNG = {'Z05': 'min', 'Z10': 'min', 'Z30': 'min', 'CL': 'min', 'CR': 'min', 'CM': 'min', 'SBJ': 'max'}
SPRINT_DIST = {'Sprint_5m': 5.0, 'Sprint_10m': 10.0, 'Sprint_30m': 30.0}
ZEITEN = {'PRE': 'prä', 'POST': 'post'}

def lies_csv(pfad):
    with open(pfad, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def dict_eindeutig(paare, was):
    """Dictionary aus (Schlüssel, Wert)-Paaren, Abbruch bei doppeltem Schlüssel (0.5 Nr. 10, Fassung 2, Befund 8)."""
    d = {}
    for k, v in paare:
        pruefe(k not in d, was, ': Schlüssel doppelt', k); d[k] = v
    return d

def sha256_datei(pfad):
    h = hashlib.sha256()
    with open(pfad, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

KONST = dict_eindeutig(((r['name'], r['wert']) for r in lies_csv(ANLAGE('Konstanten'))), 'Konstanten')
ZOLL = float(KONST['ZOLL_IN_CM']); PFUND = float(KONST['PFUND_IN_KG'])
KR_MIN = float(KONST['KR_ALTER_MIN']); KR_MAX = float(KONST['KR_ALTER_MAX']); KR_RASTER = float(KONST['KR_RASTER'])
V_MAX = float(KONST['V_MAX']); DT_MIN = float(KONST['DT_MIN'])
EINHEITEN = int(KONST['EINHEITEN_ANGEBOTEN']); DECKEL = int(KONST['WOCHENDECKEL'])
W1_BEGINN = datetime.datetime.strptime(KONST['W1_BEGINN'], '%Y-%m-%d %H:%M:%S')
W6_ENDE = datetime.datetime.strptime(KONST['W6_ENDE'], '%Y-%m-%d %H:%M:%S')
DUBL_S = float(KONST['DUBLETTE_ABSTAND']) * 60.0
CR10_VERSATZ = int(KONST['CR10_VERSATZ'])
def _mmss(s):
    m, sek = s.split(':'); return int(m) + int(sek) / 60.0
DAUER = {w: _mmss(KONST['DAUER_W%d' % w]) for w in range(1, 7)}
PP_HAUPT = int(KONST['PP_SCHWELLE_HAUPT']); PP_SENS = [int(x) for x in KONST['PP_SCHWELLEN_SENSITIV'].split()]
AK_SCHWELLE = int(KONST['AK_SCHWELLE']); N_MIN = int(KONST['N_MIN_JE_GRUPPE'])
ALPHA = float(KONST['ALPHA']); KI = float(KONST['KI_NIVEAU']); POWER_ZIEL = float(KONST['POWER_ZIEL'])
SESOI_F = float(KONST['SESOI_FAKTOR'])
NULL_LO, NULL_HI = [float(x) for x in KONST['NULLSTELLE_INTERVALL'].split()]
NULL_TOL = float(KONST['NULLSTELLE_TOLERANZ'])
BOOT_B = int(KONST['BOOT_B']); BOOT_SEED = int(KONST['BOOT_STARTWERT']); BOOT_BLOECKE = int(KONST['BOOT_BLOECKE'])
D_ERW = {'D006': float(KONST['D_ERWARTUNG_D006']), 'D011': float(KONST['D_ERWARTUNG_D011']),
         'D037': float(KONST['D_ERWARTUNG_D037']), 'D093': float(KONST['D_ERWARTUNG_D093'])}
PQ = (1 + KI) / 2      # 0.975

# =====================================================================================
# B  Rechenkern (0.5 Rechenkonventionen)
# =====================================================================================
def mittel(x):
    """Arithmetisches Mittel, um den ersten Wert verschoben gerechnet (mathematisch identisch, nötig für
    9 Stellen bei R03, wie bei der zweiten Instanz A12), Summation exakt (math.fsum)."""
    x = [float(v) for v in x]
    if len(x) == 0: return None
    s = x[0]
    return s + math.fsum(v - s for v in x) / len(x)
def sd(x):
    """Standardabweichung mit Nenner n − 1 (0.5 Nr. 2), zweistufig, um den ersten Wert verschoben."""
    x = [float(v) for v in x]; n = len(x)
    if n < 2: return None
    s = x[0]; y = [v - s for v in x]; m = math.fsum(y) / n
    return math.sqrt(math.fsum((v - m) ** 2 for v in y) / (n - 1))
def sd_pool(a, b):
    """Gepoolte SD zweier Gruppen (0.5 Nr. 2), None bei n < 2 in einer Gruppe."""
    if len(a) < 2 or len(b) < 2: return None
    return math.sqrt(((len(a) - 1) * sd(a) ** 2 + (len(b) - 1) * sd(b) ** 2) / (len(a) + len(b) - 2))
def quantil7(x, p):
    """Quantil Typ 7 (0.5 Nr. 7)."""
    x = sorted(float(v) for v in x); n = len(x)
    if n == 0: return None
    h = (n - 1) * p + 1
    j = int(math.floor(h))
    if j >= n: return x[n - 1]
    return x[j - 1] + (h - j) * (x[j] - x[j - 1])
def median(x): return quantil7(x, 0.5)
def t_q(p, df): return float(stats.t.ppf(p, df))
def t_p2(t, df): return float(2 * stats.t.sf(abs(t), df))
def f_q(p, d1, d2): return float(stats.f.ppf(p, d1, d2))
def f_p(F, d1, d2): return float(stats.f.sf(F, d1, d2))
def chi2_q(p, df): return float(stats.chi2.ppf(p, df))

def kq(X, y):
    """Kleinste Quadrate über QR-Zerlegung. Rückgabe dict oder None bei Rangdefekt (0.5 Nr. 11)."""
    X = np.asarray(X, float); y = np.asarray(y, float); n, p = X.shape
    if n <= p: return None
    if np.linalg.matrix_rank(X) < p: return None
    Q, R = np.linalg.qr(X, mode='reduced')
    b = np.linalg.solve(R, Q.T @ y)
    Rinv = np.linalg.solve(R, np.eye(p))
    XtX_inv = Rinv @ Rinv.T
    fitted = X @ b; res = y - fitted
    df = n - p; sse = float(res @ res); s2 = sse / df
    cov = s2 * XtX_inv; se = np.sqrt(np.diag(cov))
    ybar = float(np.mean(y)); sst = float(((y - ybar) ** 2).sum())
    r2 = 1 - sse / sst if sst > 0 else float('nan')
    return dict(b=b, se=se, df=df, sigma=math.sqrt(s2), r2=r2, res=res, fitted=fitted, cov=cov, sse=sse, sst=sst, n=n, p=p)

def anova1(werte, gruppen):
    """Einfaktorielle Varianzanalyse: F, df1, df2, p, SS, MS, Residuen-SD, R²."""
    s = float(werte[0]); g = {}     # um den ersten Wert verschoben (A12), Quadratsummen unverändert
    for w, k in zip(werte, gruppen): g.setdefault(k, []).append(float(w) - s)
    alle = [float(w) - s for w in werte]; n = len(alle); k = len(g); gm = mittel(alle)
    ssb = math.fsum(len(v) * (mittel(v) - gm) ** 2 for v in g.values())
    ssw = math.fsum(math.fsum((x - mittel(v)) ** 2 for x in v) for v in g.values())
    df1, df2 = k - 1, n - k
    msb, msw = ssb / df1, ssw / df2
    F = msb / msw
    return dict(F=F, df1=df1, df2=df2, p=f_p(F, df1, df2), ssb=ssb, ssw=ssw, msb=msb, msw=msw,
                sigma=math.sqrt(msw), r2=ssb / (ssb + ssw))

def brown_forsythe(res, g):
    """Levene-Test mit Median (S14 Regel 2): z = |e − Median der Gruppe|, Varianzanalyse von z."""
    grp = {}
    for e, k in zip(res, g): grp.setdefault(k, []).append(float(e))
    med = {k: median(v) for k, v in grp.items()}
    z = [abs(float(e) - med[k]) for e, k in zip(res, g)]
    return anova1(z, list(g))

def shapiro(x):
    x = [float(v) for v in x]
    if len(x) < 3: return None
    W, p = stats.shapiro(x)
    return float(W), float(p)

def power_ncf(d1, d2, lam, fcrit):
    if lam == 0: return 1 - float(stats.f.cdf(fcrit, d1, d2))
    return 1 - float(stats.ncf.cdf(fcrit, d1, d2, lam))

def khamis_roche(S_in, W_lb, MP_in, b0, b1, b2, b3):
    return b0 + b1 * S_in + b2 * W_lb + b3 * MP_in

# =====================================================================================
# C  Ergebnisregister und Kennungen
# =====================================================================================
KENN = lies_csv(ANLAGE('Kennungen'))
pruefe(len(KENN) == 1535, 'Kennungsanlage hat', len(KENN), 'Muster statt 1535')
ERG = OrderedDict()      # Kennung -> (wert oder None, grund)
def setze(k, wert, grund=None):
    pruefe(k not in ERG, 'Kennung doppelt gesetzt:', k)
    if wert is None:
        pruefe(grund in GRUENDE, 'unzulässiger Grund', grund, 'für', k)
        ERG[k] = (None, grund)
    else:
        if isinstance(wert, (bool, np.bool_)): wert = int(wert)
        if isinstance(wert, (np.integer,)): wert = int(wert)
        if isinstance(wert, (np.floating,)): wert = float(wert)
        pruefe(isinstance(wert, (int, float)) and not (isinstance(wert, float) and (math.isnan(wert) or math.isinf(wert))),
               'unzulässiger Wert', wert, 'für', k)
        ERG[k] = (wert, '')
def kenn(s, groesse, ziel, zeit, menge, variante):
    return '.'.join([s, groesse, ziel, zeit, menge, variante])

# =====================================================================================
# D  Referenztests (Teil G.2, Phase 4.1)
# =====================================================================================
def referenztests():
    ref = lies_csv(ANLAGE('Referenzdaten')); dat = lies_csv(ANLAGE('Referenzdaten_Daten'))
    daten = defaultdict(lambda: defaultdict(dict))
    for r in dat:
        daten[r['ref_id']][r['variable']][int(r['beobachtung'])] = float(r['wert'])
    def spalte(rid, var):
        d = daten[rid][var]; return [d[i] for i in sorted(d)]
    # Nachtrag Toleranz R08 vom 25.09.2026 (Rückfrage R5): W 1e-5 statt 5e-7, F_9,90(0,95) 1e-4 statt 5e-5
    NACHTRAG = {('R08', 'Teststatistik W'): 1e-5, ('R08', 'F_9,90(0.95)'): 1e-4}
    eigen = {}
    # R01
    y = spalte('R01', 'y'); eigen[('R01', 'Mittel')] = mittel(y); eigen[('R01', 'SD mit Nenner n − 1')] = sd(y)
    # R02, R03
    for rid, var in (('R02', 'resistance'), ('R03', 'agwt')):
        a = anova1(spalte(rid, var), spalte(rid, 'instrument'))
        eigen.update({(rid, 'F'): a['F'], (rid, 'Residuen-SD'): a['sigma'], (rid, 'R²'): a['r2'], (rid, 'df zwischen'): a['df1'],
                      (rid, 'df innerhalb'): a['df2'], (rid, 'SS zwischen'): a['ssb'], (rid, 'SS innerhalb'): a['ssw'],
                      (rid, 'MS zwischen'): a['msb'], (rid, 'MS innerhalb'): a['msw']})
    # R03 zusätzlich über den S15-Rechenweg (Fassung 2, Befund 5 der Durchsicht): gepoolte SD und t² = F
    g3 = spalte('R03', 'instrument'); w3 = spalte('R03', 'agwt')
    a3 = [v for v, k in zip(w3, g3) if k == 1]; b3 = [v for v, k in zip(w3, g3) if k == 2]
    sp3 = sd_pool(a3, b3); t3 = (mittel(a3) - mittel(b3)) / (sp3 * math.sqrt(1 / len(a3) + 1 / len(b3)))
    zusatz = [('R03', 'Residuen-SD', sp3, 'S15 sd_pool'), ('R03', 'F', t3 * t3, 'S15 t²')]
    # R04
    x = spalte('R04', 'x'); y = spalte('R04', 'y'); m = kq(np.column_stack([np.ones(len(x)), x]), y)
    eigen.update({('R04', 'B0'): m['b'][0], ('R04', 'SE B0'): m['se'][0], ('R04', 'B1'): m['b'][1], ('R04', 'SE B1'): m['se'][1],
                  ('R04', 'Residuen-SD'): m['sigma'], ('R04', 'R²'): m['r2']})
    # R05
    X = np.column_stack([np.ones(16)] + [spalte('R05', 'x%d' % i) for i in range(1, 7)]); m = kq(X, spalte('R05', 'y'))
    for i in range(7):
        eigen[('R05', 'B%d' % i)] = m['b'][i]; eigen[('R05', 'SE B%d' % i)] = m['se'][i]
    eigen[('R05', 'Residuen-SD')] = m['sigma']; eigen[('R05', 'R²')] = m['r2']
    # R06, R07, R13 Quantile, R08, R09, R10, R11, R12, R13 T
    import re
    for r in ref:
        rid, gr, ein = r['ref_id'], r['groesse'], r['eingang']
        if rid == 'R06':
            df = int(re.search(r'df = (\d+)', ein).group(1)); p = float(re.search(r'p = ([0-9.]+)', ein).group(1))
            eigen[(rid, gr, ein)] = t_q(p, df)
        if rid in ('R07', 'R13') and gr.startswith('χ²'):
            df = int(re.search(r'df = (\d+)', ein).group(1)); p = float(re.search(r'p = ([0-9.]+)', ein).group(1))
            eigen[(rid, gr, ein)] = chi2_q(p, df)
    bf = brown_forsythe(spalte('R08 R13', 'diameter'), [int(v) for v in spalte('R08 R13', 'batch')])
    eigen.update({('R08', 'Teststatistik W'): bf['F'], ('R08', 'df1'): bf['df1'], ('R08', 'df2'): bf['df2'],
                  ('R08', 'F_9,90(0.95)'): f_q(0.95, 9, 90)})
    z = spalte('R09', 'y'); W, p = shapiro(z)
    eigen.update({('R09', 'n'): len(z), ('R09', 'W'): W, ('R09', 'p'): p})
    d10 = daten['R10']
    eigen[('R10', 'PAS in Zoll')] = khamis_roche(d10['stature_in'][1], d10['weight_lb'][1], d10['midparent_in'][1],
                                                  d10['beta0'][1], d10['stature_koeff'][1], d10['weight_koeff'][1], d10['midparent_koeff'][1])
    g = spalte('R11', 'gruppe'); w = spalte('R11', 'wert')
    m1 = [v for v, k in zip(w, g) if k == 1]; m2 = [v for v, k in zip(w, g) if k == 2]
    sp = sd_pool(m1, m2); n1, n2 = len(m1), len(m2); dfg = n1 + n2 - 2; J = 1 - 3 / (4 * dfg - 1)
    diff = mittel(m1) - mittel(m2); se = sp * math.sqrt(1 / n1 + 1 / n2); t = diff / se
    eigen.update({('R11', 'M Movie 1'): mittel(m1), ('R11', 'M Movie 2'): mittel(m2), ('R11', 'SD Movie 1'): sd(m1), ('R11', 'SD Movie 2'): sd(m2),
                  ('R11', 'd_s'): diff / sp, ('R11', 'g_s'): diff / sp * J, ('R11', 't'): t, ('R11', 'p'): t_p2(t, dfg),
                  ('R11', 'KI der Differenz, untere Grenze'): diff - t_q(PQ, dfg) * se, ('R11', 'KI der Differenz, obere Grenze'): diff + t_q(PQ, dfg) * se})
    # R12
    lam = 0.1 ** 2 * 2283; df2 = 2283 - 30; fc = f_q(0.95, 8, df2)
    eigen.update({('R12', 'λ'): lam, ('R12', 'F_crit'): fc, ('R12', 'df2'): df2, ('R12', 'Power'): power_ncf(8, df2, lam, fc)})
    N = 39
    while power_ncf(8, N - 30, 0.01 * N, f_q(0.95, 8, N - 30)) < 0.95: N += 1
    eigen[('R12', 'kleinstes N mit Power ≥ 0.95')] = N
    n = 20; lam = 0.40 ** 2 * 2 * n; d2 = 2 * (n - 1)
    eigen[('R12', 'Power × 100')] = 100 * power_ncf(1, d2, lam, f_q(0.95, 1, d2))
    def n_je_gruppe(f):
        n = 2
        while power_ncf(1, 2 * (n - 1), f ** 2 * 2 * n, f_q(0.95, 1, 2 * (n - 1))) < POWER_ZIEL: n += 1
        return n
    eigen[('R12', 'n je Gruppe', 'u = 1, α = 0.05, Power 0.80, f = 0.25')] = n_je_gruppe(0.25)
    eigen[('R12', 'n je Gruppe', 'zweiseitig α = 0.05, Power 0.80, d = 0.50, f = d/2')] = n_je_gruppe(0.25)
    eigen[('R12', 'n je Gruppe', 'zweiseitig α = 0.05, Power 0.80, d = 1.00, f = d/2')] = n_je_gruppe(0.50)
    dia = spalte('R08 R13', 'diameter')
    eigen[('R13', 'T')] = (len(dia) - 1) * (sd(dia) / 0.1) ** 2; eigen[('R13', 'df')] = len(dia) - 1
    # Bewertung
    P('\nREFERENZTESTS R01 bis R13 (Teil G.2), Nachtrag Toleranz R08 vom 25.09.2026 angewandt')
    P('%-4s %-34s %-24s %-24s %-11s %-9s %s' % ('Test', 'Größe', 'Soll', 'Ist', 'Abw.', 'Toleranz', 'bestanden'))
    best = 0; gesamt = 0
    for r in ref:
        rid, gr, ein = r['ref_id'], r['groesse'], r['eingang']
        soll = float(r['sollwert']); tol_txt = r['toleranz']
        key = (rid, gr) if (rid, gr) in eigen else ((rid, gr, ein) if (rid, gr, ein) in eigen else None)
        pruefe(key is not None, 'Referenztest ohne eigenen Wert:', rid, gr, ein)
        ist = float(eigen[key])
        if (rid, gr) in NACHTRAG: tol = NACHTRAG[(rid, gr)]; tol_txt = '%g (Nachtrag 25.09.)' % tol; ok = abs(ist - soll) <= tol
        elif tol_txt == 'exakt': tol = 0.0; ok = (ist == soll)
        elif tol_txt.startswith('exakt (1e-9'): tol = 1e-9 * max(1.0, abs(soll)); ok = abs(ist - soll) <= tol
        elif tol_txt.startswith('mindestens 9'): tol = 0.5 * 10 ** (math.floor(math.log10(abs(soll))) - 8); ok = abs(ist - soll) <= tol
        else: tol = float(tol_txt); ok = abs(ist - soll) <= tol
        gesamt += 1; best += int(ok)
        P('%-4s %-34s %-24s %-24s %-11.3g %-9s %s' % (rid, gr[:34], ('%.15g' % soll), ('%.15g' % ist), ist - soll, tol_txt[:9], 'ja' if ok else 'NEIN'))
    for rid, gr, ist, weg in zusatz:
        soll = [float(r['sollwert']) for r in ref if r['ref_id'] == rid and r['groesse'] == gr][0]
        tol = 0.5 * 10 ** (math.floor(math.log10(abs(soll))) - 8); ok = abs(ist - soll) <= tol
        gesamt += 1; best += int(ok)
        P('%-4s %-34s %-24s %-24s %-11.3g %-9s %s' % (rid, (gr + ' über ' + weg)[:34], ('%.15g' % soll), ('%.15g' % ist), ist - soll, '9 Stellen', 'ja' if ok else 'NEIN'))
    P('Referenztests: %d von %d Sollwerten bestanden (83 der Anlage und %d Zusatzprüfungen über den S15-Rechenweg)' % (best, gesamt, len(zusatz)))
    pruefe(best == gesamt, 'Referenztest nicht bestanden, die Auswertung hält an (G.2)')

# =====================================================================================
# E  Grenzfälle (Phase 4.2): konstruierte Kleindatensätze mit von Hand bestimmtem Ergebnis
# =====================================================================================
def grenzfaelle():
    P('\nGRENZFÄLLE (Phase 4.2), Sollwerte von Hand')
    faelle = []
    def fall(name, ist, soll, tol=0.0):
        ok = (ist == soll) if tol == 0 else (abs(ist - soll) <= tol)
        faelle.append(ok); P('  %-70s ist %-22s soll %-22s %s' % (name, repr(ist), repr(soll), 'ja' if ok else 'NEIN'))
    fall('Quantil Typ 7, Median von 1 2 3 4', median([1, 2, 3, 4]), 2.5)
    fall('Quantil Typ 7, p = 0,025 von 1..5 = 1 + 0,1·1', quantil7([5, 4, 3, 2, 1], 0.025), 1.1, 1e-12)
    fall('Quantil Typ 7, p = 1 gibt Maximum', quantil7([3, 1, 2], 1.0), 3.0)
    fall('SD bei n = 1 fehlt', sd([4.0]), None)
    fall('SD von 2 4 4 4 5 5 7 9 (Nenner n − 1) = √(32/7)', sd([2, 4, 4, 4, 5, 5, 7, 9]), math.sqrt(32 / 7), 1e-12)
    fall('gepoolte SD gleicher SD bleibt SD', sd_pool([1, 3], [11, 13]), math.sqrt(2), 1e-12)
    fall('Auslöseprüfung: 5 m 1,0 s, 10 m 1,4 s (12,5 m/s) gestört', ausloesepruefung([(5.0, 1.0), (10.0, 1.4)]), True)
    fall('Auslöseprüfung: 5 m 1,0 s, 30 m 3,5 s (10,0 m/s, nicht größer) ungestört', ausloesepruefung([(5.0, 1.0), (30.0, 3.5)]), False)
    fall('Auslöseprüfung: Δt = 0 gestört', ausloesepruefung([(5.0, 1.0), (10.0, 1.0)]), True)
    fall('Auslöseprüfung: nur 30 m 2,9 s (10,34 m/s ab 0) gestört', ausloesepruefung([(30.0, 2.9)]), True)
    fall('Auslöseprüfung: keine gültige Teilzeit ungestört', ausloesepruefung([]), False)
    fall('Bestwert Zeit = Minimum', bestwert([1.2, 1.1, 1.3], 'min'), 1.1)
    fall('Bestwert Sprung = Maximum', bestwert([201, 205, 199], 'max'), 205)
    fall('Interpolation Alter 14,25: w = 0,5', kr_gewichte(14.25), (14.0, 14.5, 0.5))
    fall('Interpolation Alter 17,5: Zeile 17,5 allein (w = 0)', kr_gewichte(17.5), (17.5, 18.0, 0.0))
    fall('Interpolation Alter 4,0: Zeile 4,0 allein', kr_gewichte(4.0), (4.0, 4.5, 0.0))
    fall('Programmwoche 20.07. 00:00 = W1', programmwoche(datetime.datetime(2026, 7, 20, 0, 0, 0)), 1)
    fall('Programmwoche 26.07. 23:59:59 = W1', programmwoche(datetime.datetime(2026, 7, 26, 23, 59, 59)), 1)
    fall('Programmwoche 27.07. 00:00 = W2', programmwoche(datetime.datetime(2026, 7, 27, 0, 0, 0)), 2)
    fall('Programmwoche 30.08. 23:59:59 = W6', programmwoche(datetime.datetime(2026, 8, 30, 23, 59, 59)), 6)
    fall('Programmwoche 31.08. 00:00 außerhalb (None)', programmwoche(datetime.datetime(2026, 8, 31, 0, 0, 0)), None)
    m = [dict(code='A', t=datetime.datetime(2026, 8, 1, 10, 0, 0), inh=(1, 1, 3, 1, 2, 2, 2)),
         dict(code='A', t=datetime.datetime(2026, 8, 1, 10, 5, 0), inh=(1, 1, 3, 1, 2, 2, 2)),
         dict(code='A', t=datetime.datetime(2026, 8, 1, 10, 9, 0), inh=(2, 1, 3, 1, 2, 2, 2)),
         dict(code='B', t=datetime.datetime(2026, 8, 1, 10, 0, 0), inh=(1, 1, 3, 1, 2, 2, 2))]
    nd, ns = paare(m)
    fall('Paare: A 10:00/10:05 identisch (Grenze 300 s eingeschlossen) = Dublette', nd, 1)
    fall('Paare: A 10:05/10:09 abweichend = Sammelmeldung, 10:00/10:09 > 5 min kein Paar, B anderer Code', ns, 1)
    fall('WOCAP: Wochen mit 3, 1, 0 Meldungen ganz → 2 + 1 = 3', wocap({1: 3, 2: 1}), 3)
    fall('Fallzahlregel: 8 und 8 inferenzfähig', int(8 >= N_MIN and 8 >= N_MIN), 1)
    fall('Fallzahlregel: 7 und 12 nicht inferenzfähig', int(7 >= N_MIN and 12 >= N_MIN), 0)
    X = np.array([[1, 0, 1.0], [1, 0, 1.0], [1, 1, 1.0], [1, 1, 1.0]]); fall('Rangdefekt (Spalte konstant = Achsenabschnitt) → None', kq(X, [1, 2, 3, 4]), None)
    m = kq(np.array([[1, 0.0], [1, 1.0], [1, 2.0], [1, 3.0]]), [1.0, 3.0, 5.0, 7.0]); fall('Kleinste Quadrate exakt: y = 1 + 2x, b1', float(m['b'][1]), 2.0, 1e-12)
    fall('Kleinste Quadrate exakt: σ̂ = 0', float(m['sigma']), 0.0, 1e-12)
    fall('J bei df = 18: 1 − 3/71', 1 - 3 / (4 * 18 - 1), 1 - 3 / 71.0, 1e-15)
    fall('TE gepoolt: Spieler (1,3) und (2,2,5): SS 2 + 6 = 8, df 1 + 2 = 3', te_aus([[1, 3], [2, 2, 5], [4]])[0], math.sqrt(8 / 3), 1e-12)
    fall('TE-Menge zählt nur k ≥ 2 (zwei von drei Spielern)', te_aus([[1, 3], [2, 2, 5], [4]])[1], 2)
    fall('TE df = Σ(k − 1) = 1 + 2', te_aus([[1, 3], [2, 2, 5], [4]])[2], 3)
    fall('TE leer → None', te_aus([[1], [2]])[0], None)
    fall('Überlappung: IG 1..5, KG 3..9 → [3, 5], IG 3, KG 2', ueberlappung([1, 2, 3, 4, 5], [3, 5, 8, 9]), (3, 5, 3, 2))
    fall('Überlappung leer: IG 1..2, KG 3..4 → 0, 0', ueberlappung([1, 2], [3, 4]), (3, 2, 0, 0))
    fall('Brown-Forsythe: Gruppen (−1, 0, 1) und (−1, 0, 1), gleiche |z| → F = 0', brown_forsythe([-1, 0, 1, -1, 0, 1], [1, 1, 1, 0, 0, 0])['F'], 0.0, 1e-12)
    # Gruppe 1: Residuen (1, −1, 2), Median 1, z = (0, 2, 1) · Gruppe 0: (−2, 5, −5), Median −2, z = (0, 7, 3)
    # SS zwischen = 3·(1 − 13/6)² + 3·(10/3 − 13/6)² = 49/6 · SS innerhalb = 2 + 222/9 = 80/3 · F = (49/6) / ((80/3)/4) = 49/40
    fall('Brown-Forsythe von Hand: F = 49/40', brown_forsythe([1, -1, 2, -2, 5, -5], [1, 1, 1, 0, 0, 0])['F'], 49 / 40, 1e-12)
    fall('Brown-Forsythe von Hand: df1 = 1, df2 = 4', (brown_forsythe([1, -1, 2, -2, 5, -5], [1, 1, 1, 0, 0, 0])['df1'], brown_forsythe([1, -1, 2, -2, 5, -5], [1, 1, 1, 0, 0, 0])['df2']), (1, 4))
    P('Grenzfälle: %d von %d bestanden' % (sum(faelle), len(faelle)))
    pruefe(all(faelle), 'Grenzfall nicht bestanden')

# Kernregeln als Funktionen (auch für die Grenzfälle)
def ausloesepruefung(teilzeiten):
    """S02 Regel 2: teilzeiten = [(Distanz, t)] der gültigen Teilzeiten eines Laufs. True = auslösegestört."""
    tz = sorted(teilzeiten); d0, t0 = 0.0, 0.0
    for d, t in tz:
        dt = t - t0; dd = d - d0
        if dt <= DT_MIN or dd / dt > V_MAX: return True
        d0, t0 = d, t
    return False
def bestwert(w, richtung): return min(w) if richtung == 'min' else max(w)
def kr_gewichte(alter):
    a_lo = math.floor(2 * alter) / 2; a_hi = a_lo + KR_RASTER; w = (alter - a_lo) / KR_RASTER
    return (a_lo, a_hi, w)
def programmwoche(t):
    if t < W1_BEGINN or t > W6_ENDE: return None
    return (t - W1_BEGINN).days // 7 + 1
def paare(meldungen):
    """S06 Regel 9: Dubletten- und Sammelmeldungspaare (R3 Lesart a, A8 Grenze eingeschlossen)."""
    nd = ns = 0; ms = sorted(meldungen, key=lambda m: (m['code'], m['t']))
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            a, b = ms[i], ms[j]
            if a['code'] != b['code']: continue
            if abs((b['t'] - a['t']).total_seconds()) <= DUBL_S:
                if a['inh'] == b['inh']: nd += 1
                else: ns += 1
    return nd, ns
def wocap(ganz_je_woche): return sum(min(DECKEL, n) for n in ganz_je_woche.values())
def te_aus(gruppen):
    """S10 Regel 1: gruppen = Liste der gültigen Werte je Spieler. Rückgabe (TE, n_TE, df_TE, Werte der TE-Menge)."""
    ss = 0.0; df = 0; n = 0; werte = []
    for w in gruppen:
        if len(w) >= 2:
            m = mittel(w); ss += math.fsum((x - m) ** 2 for x in w); df += len(w) - 1; n += 1; werte.extend(w)
    if df == 0: return None, n, df, werte
    return math.sqrt(ss / df), n, df, werte
def ueberlappung(ig, kg):
    L = max(min(ig), min(kg)); U = min(max(ig), max(kg))
    if L > U: return (L, U, 0, 0)
    return (L, U, sum(1 for x in ig if L <= x <= U), sum(1 for x in kg if L <= x <= U))

# =====================================================================================
# F  S01 Einlesen und Strukturprüfung
# =====================================================================================
def zahl(s, pos=True):
    if s == '': return None
    try: v = float(s)
    except ValueError: raise Abbruch('ABBRUCH: keine Zahl: %r' % s)
    pruefe((not pos) or v > 0, 'Zahl nicht größer 0:', s)
    return v

P('=' * 100)
P('GEGENPROBE PYTHON nach Spezifikation_2026-09-24 (Nachtrag 2), Fassung', FASSUNG, 'Nr.', FASSUNG_NR)
P('Skript:', SKRIPT, '· Lauf:', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))
P('Python', platform.python_version(), '· numpy', np.__version__, '· scipy', scipy.__version__, '·', platform.platform())
P('Eingang:', EINGANG)
P('=' * 100)
P('\nPRÜFSUMMEN DES EINGANGS (SHA-256)')
soll = {}
for line in open(os.path.join(DATENSTAND, 'Pruefsummen.txt'), encoding='utf-8'):
    if line.strip():
        h, n = line.split(); soll[n] = h
for n in ['Versuchsdaten.csv', 'Personendaten.csv', 'Fragebogen_A.csv', 'Zuordnung_Fragebogen.csv', 'Listenplatz_IG.csv', 'Datenwoerterbuch.md']:
    ist = sha256_datei(os.path.join(DATENSTAND, n)); pruefe(ist == soll[n], 'Prüfsumme weicht ab:', n)
    P('  %-45s %s  (Soll stimmt)' % ('Datenstand_2026-09-24/' + n, ist))
for n in ['Kennungen', 'Konstanten', 'Koeffizienten_KR', 'Vokabular', 'Fragebogen', 'Referenzdaten', 'Referenzdaten_Daten']:
    P('  %-45s %s' % ('Spezifikation_2026-09-24_%s.csv' % n, sha256_datei(ANLAGE(n))))

referenztests()
grenzfaelle()

P('\nS01 EINLESEN UND STRUKTURPRÜFUNG')
V = lies_csv(os.path.join(DATENSTAND, 'Versuchsdaten.csv'))
PERS = lies_csv(os.path.join(DATENSTAND, 'Personendaten.csv'))
FB = lies_csv(os.path.join(DATENSTAND, 'Fragebogen_A.csv'))
ZUO = lies_csv(os.path.join(DATENSTAND, 'Zuordnung_Fragebogen.csv'))
LP = lies_csv(os.path.join(DATENSTAND, 'Listenplatz_IG.csv'))
CODES = [r['Code'] for r in PERS]
pruefe(len(set(CODES)) == len(CODES), 'Code in Personendaten nicht eindeutig')
pers = OrderedDict()
for r in PERS:
    pruefe(r['Verein'] in ('A', 'B', 'C'), 'Verein unzulässig', r)
    pruefe(r['Gruppe'] == ('IG' if r['Verein'] in ('A', 'B') else 'KG'), 'Gruppe passt nicht zum Verein', r)
    pruefe(r['Familiarisierung'] in ('1', '2', ''), 'Familiarisierung unzulässig', r)
    pruefe(r['Status'] in ('ausgewertet', 'nicht angetreten'), 'Status unzulässig', r)
    pers[r['Code']] = dict(verein=r['Verein'], gruppe=r['Gruppe'], alter=zahl(r['Alter_prae']), hgt=zahl(r['Koerperhoehe_prae']),
                           mass=zahl(r['Koerpermasse_prae']), mutter=zahl(r['Groesse_Mutter']), vater=zahl(r['Groesse_Vater']),
                           fam=(int(r['Familiarisierung']) if r['Familiarisierung'] else None), status=r['Status'])
IG = [c for c in CODES if pers[c]['gruppe'] == 'IG']; KG = [c for c in CODES if pers[c]['gruppe'] == 'KG']
schluessel = set()
for r in V:
    pruefe(r['Zeitpunkt'] in ('prä', 'post'), 'Zeitpunkt unzulässig', r)
    pruefe(r['Test'] in ('Sprint_5m', 'Sprint_10m', 'Sprint_30m', 'COD_505', 'Standweitsprung'), 'Test unzulässig', r)
    pruefe((r['Seite'] in ('L', 'R')) if r['Test'] == 'COD_505' else (r['Seite'] in ('', '–')), 'Seite passt nicht zum Test', r)
    pruefe(r['Versuch'] in ('1', '2', '3'), 'Versuch unzulässig', r)
    k = (r['Code'], r['Zeitpunkt'], r['Test'], r['Seite'], r['Versuch']); pruefe(k not in schluessel, 'Schlüssel doppelt', k); schluessel.add(k)
    r['wert'] = zahl(r['Wert']); r['versuch'] = int(r['Versuch'])
    pruefe(r['Code'] in pers, 'Code nicht in den Personendaten', r['Code'])
    r['ziel'] = ZIEL_VON[(r['Test'], r['Seite'] if r['Test'] == 'COD_505' else '–')]
cases = set()
for r in FB:
    pruefe(r['CASE'] not in cases, 'CASE doppelt', r['CASE']); cases.add(r['CASE'])
    def inb(v, lo, hi): return v.isdigit() and lo <= int(v) <= hi
    pruefe(inb(r['H010'], 1, 22) and r['H002'] == '1' and inb(r['H003'], 1, 12) and inb(r['H004'], 1, 3) and inb(r['H005'], 1, 11)
           and inb(r['H006'], 1, 5) and inb(r['H007'], 1, 2) and inb(r['H008'], 1, 2) and inb(r['H009'], 1, 2), 'Fragebogenwert unzulässig', r)
# A9 Zusatzprüfung der Zuordnung
zuord = dict_eindeutig(((r['Listenlabel'], r['Analysecode']) for r in ZUO), 'Zuordnung_Fragebogen')
kein_lp = dict_eindeutig(((r['Code'], r['kein_Listenplatz']) for r in LP), 'Listenplatz_IG')
pruefe(list(kein_lp) == IG, 'Listenplatz_IG.csv enthält nicht genau die IG-Codes in Reihenfolge der Personendaten')
pruefe(all(v in ('ja', 'nein') for v in kein_lp.values()), 'kein_Listenplatz unzulässig')
for lab, code in zuord.items():
    if code: pruefe(code in pers and pers[code]['gruppe'] == 'IG', 'Analysecode der Zuordnung nicht IG oder unbekannt', lab, code)
pruefe(not any(kein_lp[c] == 'ja' and c in zuord.values() for c in IG), 'Spieler ohne Listenplatz ist einem Listenlabel zugeordnet')
for m, cs in (('ALL', CODES), ('IG', IG), ('KG', KG), ('VA', [c for c in CODES if pers[c]['verein'] == 'A']),
              ('VB', [c for c in CODES if pers[c]['verein'] == 'B']), ('VC', [c for c in CODES if pers[c]['verein'] == 'C'])):
    setze(kenn('S01', 'N', 'X', 'X', m, 'X'), len(cs))
setze('S01.NZEIL.X.X.ALL.X', len(V)); setze('S01.NMELD.FB.X.ALL.X', len(FB))
P('  Spieler %d (IG %d, KG %d), Versuchszeilen %d, Meldungen %d, Strukturprüfung ohne Verstoß' % (len(CODES), len(IG), len(KG), len(V), len(FB)))

# =====================================================================================
# G  S02 Gültigkeit, S03 Ausfallkategorien, S04 Aggregation
# =====================================================================================
P('\nS02 GÜLTIGKEIT DER VERSUCHE')
for r in V: r['roh'] = 1 if (r['wert'] is not None and r['ungültig'] == '') else 0
laeufe = defaultdict(list)
for r in V:
    if r['Test'] in SPRINT_DIST: laeufe[(r['Code'], r['Zeitpunkt'], r['versuch'])].append(r)
gestoert = set(); nausl = Counter()
for key, rows in laeufe.items():
    tz = [(SPRINT_DIST[r['Test']], r['wert']) for r in rows if r['roh'] == 1]
    if ausloesepruefung(tz): gestoert.add(key); nausl[key[1]] += 1
for r in V:
    r['ausl'] = 1 if (r['Test'] in SPRINT_DIST and (r['Code'], r['Zeitpunkt'], r['versuch']) in gestoert) else 0
    r['gueltig'] = 1 if (r['roh'] == 1 and r['ausl'] == 0) else 0
for zt, zp in ZEITEN.items(): setze(kenn('S02', 'NAUSL', 'X', zt, 'ALL', 'X'), nausl[zp])
for z in ZIELE6:
    for zt, zp in ZEITEN.items():
        setze(kenn('S02', 'NGUELT', z, zt, 'ALL', 'X'), sum(1 for r in V if r['ziel'] == z and r['Zeitpunkt'] == zp and r['gueltig'] == 1))
P('  auslösegestörte Läufe prä %d, post %d' % (nausl['prä'], nausl['post']))

P('\nS03 AUSFALLKATEGORIEN')
VOK = {}
for r in lies_csv(ANLAGE('Vokabular')):
    pruefe(r['bemerkung_exakt'] not in VOK, 'Vokabular: Bemerkungstext doppelt', r['bemerkung_exakt']); VOK[r['bemerkung_exakt']] = r['kategorie']
# Regel 1, Widerspruchsprüfung über alle Post-Zeilen nicht angetretener Spieler (Fassung 2, Befund 1 der Durchsicht)
for r in V:
    if r['Zeitpunkt'] == 'post' and pers[r['Code']]['status'] == 'nicht angetreten':
        pruefe(r['wert'] is None, 'Widerspruch: Wert in Post-Zeile eines nicht angetretenen Spielers', r['Code'], r['Test'], r['Versuch'])
nkat = Counter()
for r in V:
    if r['gueltig'] == 1: continue
    if r['Zeitpunkt'] == 'post' and pers[r['Code']]['status'] == 'nicht angetreten':
        pruefe(r['wert'] is None, 'Wert bei nicht angetretenem Spieler', r['Code']); kat = 'NANG'
    elif r['roh'] == 1 and r['ausl'] == 1: kat = 'AUSL'
    else:
        pruefe(r['Bemerkung'] in VOK, 'Bemerkung nicht im Vokabular oder leer (K5):', repr(r['Bemerkung']), r['Code'], r['Zeitpunkt'], r['Test'])
        kat = VOK[r['Bemerkung']]
    r['kat'] = kat; nkat[(r['ziel'], r['Zeitpunkt'], pers[r['Code']]['gruppe'], kat)] += 1
for z in ZIELE6:
    for zt, zp in ZEITEN.items():
        for g in ('IG', 'KG'):
            for kat in ['TECH', 'ZEIT', 'FEHL', 'FALSCH', 'NANG', 'AUSL']:
                if kat == 'NANG' and zt == 'PRE': continue
                setze(kenn('S03', 'NKAT', z, zt, g, kat), nkat[(z, zp, g, kat)])
P('  ungültige Zeilen je Kategorie:', dict(Counter(r['kat'] for r in V if r['gueltig'] == 0)))

P('\nS04 AGGREGATION JE SPIELER')
zellen = defaultdict(list)     # (code, zp, ziel) -> [(versuch, wert)] gültig
for r in V:
    if r['gueltig'] == 1: zellen[(r['Code'], r['Zeitpunkt'], r['ziel'])].append((r['versuch'], r['wert']))
K = {}; BEST = {}; MEAN = {}
for c in CODES:
    for zp in ('prä', 'post'):
        for z in ZIELE6:
            w = [v for _, v in sorted(zellen.get((c, zp, z), []))]
            K[(c, zp, z)] = len(w)
            BEST[(c, zp, z)] = bestwert(w, RICHTUNG[z]) if w else None
            MEAN[(c, zp, z)] = mittel(w) if w else None
        bl, br = BEST[(c, zp, 'CL')], BEST[(c, zp, 'CR')]
        BEST[(c, zp, 'CM')] = (bl + br) / 2 if (bl is not None and br is not None) else None
        ml, mr = MEAN[(c, zp, 'CL')], MEAN[(c, zp, 'CR')]
        MEAN[(c, zp, 'CM')] = (ml + mr) / 2 if (ml is not None and mr is not None) else None
for c in CODES:
    for z in ZIELE6:
        for zt, zp in ZEITEN.items(): setze(kenn('S04', 'K', z, zt, 'P' + c, 'X'), K[(c, zp, z)])
    for z in ZIELE7:
        for zt, zp in ZEITEN.items():
            for gr, D in (('BEST', BEST), ('MEAN', MEAN)):
                v = D[(c, zp, z)]
                if v is not None: setze(kenn('S04', gr, z, zt, 'P' + c, 'X'), v)
                else: setze(kenn('S04', gr, z, zt, 'P' + c, 'X'), None, G_EINGANG if z == 'CM' else G_WENIG)
P('  Bestwerte prä vorhanden je Zielgröße:', {z: sum(1 for c in CODES if BEST[(c, 'prä', z)] is not None) for z in ZIELE7})

# =====================================================================================
# H  S05 Reifestatus %PAH nach Khamis und Roche
# =====================================================================================
P('\nS05 REIFESTATUS %PAH')
KR = dict_eindeutig(((float(r['alter_jahre']), (float(r['beta0']), float(r['stature_in']), float(r['weight_lb']), float(r['midparent_in'])))
                     for r in lies_csv(ANLAGE('Koeffizienten_KR'))), 'Koeffizienten_KR')
PAH = {}
for c in CODES:
    p = pers[c]
    mp = (p['mutter'] / ZOLL + p['vater'] / ZOLL) / 2 if (p['mutter'] is not None and p['vater'] is not None) else None
    if mp is not None: setze(kenn('S05', 'MP', 'PAH', 'PRE', 'P' + c, 'X'), mp)
    else: setze(kenn('S05', 'MP', 'PAH', 'PRE', 'P' + c, 'X'), None, G_EINGANG)
    # Vorrang der Gründe (Fassung 2, Befund 2 der Durchsicht): fehlender Eingang vor Gültigkeitsbereich,
    # wie in der berichteten Rechnung. Die Spezifikation legt den Vorrang nicht fest (Nachtrag beim Verfasser).
    if p['hgt'] is None or p['mass'] is None or mp is None:
        PAH[c] = None; grund = G_EINGANG
    elif not (KR_MIN <= p['alter'] <= KR_MAX):
        PAH[c] = None; grund = G_BEREICH
    else:
        a_lo, a_hi, w = kr_gewichte(p['alter'])
        pruefe(a_lo in KR, 'Tabellenzeile fehlt', a_lo)
        if w == 0: co = KR[a_lo]
        else:
            pruefe(a_hi in KR, 'Tabellenzeile fehlt', a_hi); co = tuple((1 - w) * KR[a_lo][i] + w * KR[a_hi][i] for i in range(4))
        pas = khamis_roche(p['hgt'] / ZOLL, p['mass'] / PFUND, mp, *co)
        PAH[c] = 100.0 * (p['hgt'] / ZOLL) / pas; grund = None
        setze(kenn('S05', 'PAS', 'PAH', 'PRE', 'P' + c, 'X'), pas); setze(kenn('S05', 'PAH', 'PAH', 'PRE', 'P' + c, 'X'), PAH[c])
    if grund:
        setze(kenn('S05', 'PAS', 'PAH', 'PRE', 'P' + c, 'X'), None, grund); setze(kenn('S05', 'PAH', 'PAH', 'PRE', 'P' + c, 'X'), None, grund)
for g, cs in (('IG', IG), ('KG', KG)): setze(kenn('S05', 'NPAH', 'PAH', 'PRE', g, 'X'), sum(1 for c in cs if PAH[c] is not None))
P('  %%PAH vorhanden: IG %d, KG %d' % (sum(1 for c in IG if PAH[c] is not None), sum(1 for c in KG if PAH[c] is not None)))

# =====================================================================================
# I  S06 Fragebogen A, S07 Adhärenz, Belastung, unerwünschte Ereignisse
# =====================================================================================
P('\nS06 FRAGEBOGEN A')
FBA = dict_eindeutig((((r['variable'], r['code']), r['bedeutung']) for r in lies_csv(ANLAGE('Fragebogen'))), 'Fragebogen-Anlage')
KORR = dict_eindeutig(((r['code'], r['bedeutung'].replace('Listenlabel ', '')) for r in lies_csv(ANLAGE('Fragebogen')) if r['variable'] == 'CASE_KORREKTUR'), 'CASE_KORREKTUR')
meld = []
for r in FB:
    label = FBA[('H010', r['H010'])]
    if r['CASE'] in KORR: label = KORR[r['CASE']]
    code = zuord.get(label, '')
    pruefe(code != '', 'Meldung an Listenlabel ohne Analysecode:', label, 'CASE', r['CASE'])
    pruefe(pers[code]['gruppe'] == 'IG', 'Analysecode der KG', code)
    t = datetime.datetime.strptime(r['STARTED'], '%Y-%m-%d %H:%M:%S'); w = programmwoche(t)
    pruefe(w is not None, 'Meldung außerhalb W1 bis W6 (K8):', r['CASE'], r['STARTED'])
    meld.append(dict(case=r['CASE'], code=code, t=t, w=w, status={'1': 'GANZ', '2': 'TEILW', '3': 'GARN'}[r['H004']], h003=int(r['H003']),
                     cr10=int(r['H005']) - CR10_VERSATZ, h007=int(r['H007']), inh=tuple(int(r[h]) for h in ('H003', 'H004', 'H005', 'H006', 'H007', 'H008', 'H009')),
                     korr=(r['CASE'] in KORR)))
setze('S06.NMELD.FB.X.ALL.X', len(meld))
for c in IG: setze(kenn('S06', 'NMELD', 'FB', 'X', 'P' + c, 'X'), sum(1 for m in meld if m['code'] == c))
setze('S06.NKORR.FB.X.ALL.X', sum(1 for m in meld if m['korr']))
nd, ns = paare(meld); setze('S06.NDUBL.FB.X.ALL.X', nd); setze('S06.NSAMM.FB.X.ALL.X', ns)
for st in ('GANZ', 'TEILW', 'GARN'): setze(kenn('S06', 'NSTAT', 'FB', 'X', 'IG', st), sum(1 for m in meld if m['status'] == st))
P('  Meldungen %d, korrigiert %d, Dublettenpaare %d, Sammelmeldungspaare %d' % (len(meld), sum(1 for m in meld if m['korr']), nd, ns))

P('\nS07 ADHÄRENZ, BELASTUNG, UNERWÜNSCHTE EREIGNISSE')
ADH = {}      # code -> dict(GANZ, GT, WOCAP, DIST) oder None (nicht erhebbar)
for c in IG:
    ms = [m for m in meld if m['code'] == c]
    if kein_lp[c] == 'ja':
        pruefe(len(ms) == 0, 'Meldungen bei Spieler ohne Listenplatz', c); ADH[c] = None; continue
    ganz = [m for m in ms if m['status'] == 'GANZ']
    ADH[c] = dict(GANZ=len(ganz), GT=sum(1 for m in ms if m['status'] in ('GANZ', 'TEILW')),
                  WOCAP=wocap(Counter(m['w'] for m in ganz)), DIST=len(set(m['h003'] for m in ganz)))
for c in IG:
    for var in ('GANZ', 'WOCAP', 'DIST'):
        if ADH[c] is None: setze(kenn('S07', 'ADH', 'ADH', 'X', 'P' + c, var), None, G_NICHTERH)
        else: setze(kenn('S07', 'ADH', 'ADH', 'X', 'P' + c, var), ADH[c][var])
nzug = len(IG); setze('S07.NZUG.ADH.X.IG.X', nzug)
def zaehlung(c, var): return 0 if ADH[c] is None else ADH[c][var]
for var in ('GANZ', 'GT', 'WOCAP', 'DIST'):
    s = sum(zaehlung(c, var) for c in IG)
    setze(kenn('S07', 'SUMME', 'ADH', 'X', 'IG', var), s); setze(kenn('S07', 'RATE', 'ADH', 'X', 'IG', var), s / (EINHEITEN * nzug))
ganzw = [zaehlung(c, 'GANZ') for c in IG]
if max(ganzw) > EINHEITEN: P('  HINWEIS (A6): Zählung GANZ über 12 bei mindestens einem Spieler, V00 bis V12 decken nicht alle Spieler ab')
for v in range(0, 13): setze(kenn('S07', 'V%02d' % v, 'ADH', 'X', 'IG', 'GANZ'), sum(1 for x in ganzw if x == v))
for s in range(1, 13): setze(kenn('S07', 'GE%02d' % s, 'ADH', 'X', 'IG', 'GANZ'), sum(1 for x in ganzw if x >= s))
for var in ('WOCAP', 'DIST'):
    for s in (6, 9): setze(kenn('S07', 'GE%02d' % s, 'ADH', 'X', 'IG', var), sum(1 for c in IG if zaehlung(c, var) >= s))
setze('S07.MED.ADH.X.IG.GANZ', median(ganzw)); setze('S07.MITT.ADH.X.IG.GANZ', mittel(ganzw))
setze('S07.NMELDSP.ADH.X.IG.X', len(set(m['code'] for m in meld)))
for w in range(1, 7): setze(kenn('S07', 'ANTW', 'ADH', 'W%d' % w, 'IG', 'GANZ'), sum(1 for m in meld if m['status'] == 'GANZ' and m['w'] == w) / (DECKEL * nzug))
ganzm = [m for m in meld if m['status'] == 'GANZ']
for gr, f in (('CR10', lambda m: float(m['cr10'])), ('LOAD', lambda m: m['cr10'] * DAUER[m['w']])):
    x = [f(m) for m in ganzm]
    setze(kenn('S07', 'N', gr, 'X', 'IG', 'GANZ'), len(x))
    for st, fn in (('M', mittel), ('SD', sd), ('MED', median), ('MIN', min), ('MAX', max)):
        v = fn(x) if (len(x) > 0 and not (st == 'SD' and len(x) < 2)) else None
        setze(kenn('S07', st, gr, 'X', 'IG', 'GANZ'), v, None if v is not None else G_WENIG)
    for w in range(1, 7):
        xw = [f(m) for m in ganzm if m['w'] == w]
        setze(kenn('S07', 'N', gr, 'W%d' % w, 'IG', 'GANZ'), len(xw))
        setze(kenn('S07', 'M', gr, 'W%d' % w, 'IG', 'GANZ'), mittel(xw) if xw else None, None if xw else G_WENIG)
        setze(kenn('S07', 'SD', gr, 'W%d' % w, 'IG', 'GANZ'), sd(xw) if len(xw) >= 2 else None, None if len(xw) >= 2 else G_WENIG)
ue = [m for m in meld if m['h007'] == 1]
setze('S07.UE.FB.X.IG.X', len(ue))
for st in ('GANZ', 'TEILW', 'GARN'): setze(kenn('S07', 'UE', 'FB', 'X', 'IG', st), sum(1 for m in ue if m['status'] == st))
setze('S07.UESP.FB.X.IG.X', len(set(m['code'] for m in ue)))
P('  Summe GANZ %d, Rate %.4f, Spieler mit Meldung %d, Meldungen mit H007 = 1: %d' % (sum(ganzw), sum(ganzw) / (EINHEITEN * nzug), len(set(m['code'] for m in meld)), len(ue)))

# =====================================================================================
# J  S08 Analysesets, Nenner, Teilnehmerfluss
# =====================================================================================
P('\nS08 ANALYSESETS UND TEILNEHMERFLUSS')
def hat(c, zp, z): return BEST[(c, zp, z)] is not None
ITT = {z: [c for c in CODES if hat(c, 'prä', z) and hat(c, 'post', z) and PAH[c] is not None] for z in ZIELE7}
def teil(setz, g): return [c for c in setz if pers[c]['gruppe'] == g]
PP = {}; AK9 = {}; FAMS = {}
for z in KONF:
    for s in (5, 6, 7):
        PP[(z, s)] = [c for c in ITT[z] if pers[c]['gruppe'] == 'KG' or (ADH[c] is not None and ADH[c]['GANZ'] >= s)]
    AK9[z] = [c for c in ITT[z] if pers[c]['gruppe'] == 'IG' and ADH[c] is not None and ADH[c]['GANZ'] >= AK_SCHWELLE]
    FAMS[z] = [c for c in ITT[z] if pers[c]['fam'] is not None]
def inf(setz): return 1 if (len(teil(setz, 'IG')) >= N_MIN and len(teil(setz, 'KG')) >= N_MIN) else 0
INF = {}
for z in KONF:
    INF[(z, 'ITT')] = inf(ITT[z]); INF[(z, 'FAMS')] = inf(FAMS[z])
    for s in (5, 6, 7): INF[(z, 'PP%d' % s)] = inf(PP[(z, s)])
for z in ZIELE7:
    setze(kenn('S08', 'N', z, 'X', 'ITTIG', 'X'), len(teil(ITT[z], 'IG'))); setze(kenn('S08', 'N', z, 'X', 'ITTKG', 'X'), len(teil(ITT[z], 'KG')))
for z in KONF:
    for s in (5, 6, 7): setze(kenn('S08', 'N', z, 'X', 'PP%dIG' % s, 'X'), len(teil(PP[(z, s)], 'IG')))
    setze(kenn('S08', 'N', z, 'X', 'AK9IG', 'X'), len(AK9[z]))
    setze(kenn('S08', 'N', z, 'X', 'FAMSIG', 'X'), len(teil(FAMS[z], 'IG'))); setze(kenn('S08', 'N', z, 'X', 'FAMSKG', 'X'), len(teil(FAMS[z], 'KG')))
    for sn in ('ITT', 'PP5', 'PP6', 'PP7', 'FAMS'): setze(kenn('S08', 'INF', z, 'X', sn, 'X'), INF[(z, sn)])
for c in CODES:
    for z in ZIELE7: setze(kenn('S08', 'MITGL', z, 'X', 'P' + c, 'ITT'), int(c in ITT[z]))
    for z in KONF:
        for s in (5, 6, 7): setze(kenn('S08', 'MITGL', z, 'X', 'P' + c, 'PP%d' % s), int(c in PP[(z, s)]))
        setze(kenn('S08', 'MITGL', z, 'X', 'P' + c, 'AK9'), int(c in AK9[z])); setze(kenn('S08', 'MITGL', z, 'X', 'P' + c, 'FAMS'), int(c in FAMS[z]))
MENGEN = {'IG': IG, 'KG': KG, 'VA': [c for c in CODES if pers[c]['verein'] == 'A'], 'VB': [c for c in CODES if pers[c]['verein'] == 'B'], 'VC': [c for c in CODES if pers[c]['verein'] == 'C']}
praeg = set(r['Code'] for r in V if r['Zeitpunkt'] == 'prä' and r['gueltig'] == 1)
for m, cs in MENGEN.items():
    setze(kenn('S08', 'FLZUG', 'X', 'X', m, 'X'), len(cs)); setze(kenn('S08', 'FLPRE', 'X', 'X', m, 'X'), sum(1 for c in cs if c in praeg))
    setze(kenn('S08', 'FLAUSG', 'X', 'X', m, 'X'), sum(1 for c in cs if pers[c]['status'] == 'ausgewertet'))
    setze(kenn('S08', 'FLNANG', 'X', 'X', m, 'X'), sum(1 for c in cs if pers[c]['status'] == 'nicht angetreten'))
for g, cs in (('IG', IG), ('KG', KG)):
    for z in ZIELE7:
        setze(kenn('S08', 'FLITT', z, 'X', g, 'X'), len(teil(ITT[z], g)))
        setze(kenn('S08', 'FLOPRE', z, 'X', g, 'X'), sum(1 for c in cs if not hat(c, 'prä', z)))
        setze(kenn('S08', 'FLOPOST', z, 'X', g, 'X'), sum(1 for c in cs if not hat(c, 'post', z)))
    setze(kenn('S08', 'FLOPAH', 'PAH', 'X', g, 'X'), sum(1 for c in cs if PAH[c] is None))
    setze(kenn('S08', 'B6FK', 'X', 'X', g, 'X'), sum(1 for c in cs if PAH[c] is None))
    setze(kenn('S08', 'B6NA', 'X', 'X', g, 'X'), sum(1 for c in cs if pers[c]['status'] == 'nicht angetreten'))
b6ne = [c for c in IG if ADH[c] is not None and ADH[c]['GANZ'] < PP_HAUPT]
setze('S08.B6NE.X.X.IG.X', len(b6ne)); setze('S08.B6NEKM.X.X.IG.X', sum(1 for c in b6ne if not any(m['code'] == c for m in meld)))
setze('S08.B6IF.X.X.IG.X', sum(1 for c in IG if kein_lp[c] == 'ja'))
for g, cs in (('IG', IG), ('KG', KG), ('ALL', CODES)):
    for z in ZIELE7: setze(kenn('S08', 'ANT', z, 'X', g, 'X'), sum(1 for c in cs if hat(c, 'prä', z) and hat(c, 'post', z)) / len(cs))
    setze(kenn('S08', 'ANTTN', 'X', 'X', g, 'X'), sum(1 for c in cs if pers[c]['status'] == 'ausgewertet') / len(cs))
ANA = {g: [c for c in cs if any(c in ITT[z] for z in ZIELE7)] for g, cs in (('IG', IG), ('KG', KG))}
P('  ITT-Sets (IG/KG):', {z: (len(teil(ITT[z], 'IG')), len(teil(ITT[z], 'KG'))) for z in ZIELE7})
P('  INF:', {k: v for k, v in INF.items()}, '· ANA IG %d, KG %d' % (len(ANA['IG']), len(ANA['KG'])))

# =====================================================================================
# K  S09 Versuchszahlen
# =====================================================================================
P('\nS09 VERSUCHSZAHLEN')
for zt, zp in ZEITEN.items():
    bezug = [c for c in CODES if any(r['Code'] == c and r['Zeitpunkt'] == zp for r in V) and not (zp == 'post' and pers[c]['status'] == 'nicht angetreten')]
    for z in ZIELE6:
        for g in ('IG', 'KG'):
            ks = [K[(c, zp, z)] for c in bezug if pers[c]['gruppe'] == g]
            setze(kenn('S09', 'KMEAN', z, zt, g, 'X'), mittel(ks) if ks else None, None if ks else G_WENIG)
P('  Bezugsmenge prä %d, post %d' % (len(CODES), sum(1 for c in CODES if pers[c]['status'] != 'nicht angetreten')))

# =====================================================================================
# L  S10 Messgüte, S11 Bestwert-Bias
# =====================================================================================
P('\nS10 MESSGÜTE')
def werte_je_spieler(z, zp, codes):
    """Liste der gültigen Werte je Spieler (S10 Regel 1), für CM die Paarmittel m_ij (Regel 2)."""
    out = []
    for c in codes:
        if z == 'CM':
            L = dict(zellen.get((c, zp, 'CL'), [])); R = dict(zellen.get((c, zp, 'CR'), []))
            out.append([(L[j] + R[j]) / 2 for j in sorted(set(L) & set(R))])
        else:
            out.append([v for _, v in zellen.get((c, zp, z), [])])
    return out
SESOI = {}; SESOI_POST = {}
for z in ZIELE7:
    for zt, zp in ZEITEN.items():
        te, nte, dfte, werte = te_aus(werte_je_spieler(z, zp, CODES))
        setze(kenn('S10', 'DFTE', z, zt, 'ALL', 'X'), dfte); setze(kenn('S10', 'NTE', z, zt, 'ALL', 'X'), nte)
        if te is None:
            setze(kenn('S10', 'TE', z, zt, 'ALL', 'X'), None, G_WENIG)
            for gr in ('TELO', 'TEHI'): setze(kenn('S10', gr, z, zt, 'ALL', 'X'), None, G_EINGANG)
        else:
            setze(kenn('S10', 'TE', z, zt, 'ALL', 'X'), te)
            setze(kenn('S10', 'TELO', z, zt, 'ALL', 'X'), te * math.sqrt(dfte / chi2_q(PQ, dfte)))
            setze(kenn('S10', 'TEHI', z, zt, 'ALL', 'X'), te * math.sqrt(dfte / chi2_q(1 - PQ, dfte)))
        best = [BEST[(c, zp, z)] for c in CODES if BEST[(c, zp, z)] is not None]
        S = sd(best) if len(best) >= 2 else None
        if zt == 'PRE':
            setze(kenn('S10', 'NSB', z, zt, 'ALL', 'X'), len(best))
            setze(kenn('S10', 'SB', z, zt, 'ALL', 'X'), S, None if S is not None else G_WENIG)
            ses = SESOI_F * S if S is not None else None; SESOI[z] = ses
            setze(kenn('S10', 'SESOI', z, zt, 'ALL', 'X'), ses, None if ses is not None else G_EINGANG)
            if te is None:
                for gr in ('CV', 'RTS', 'FLEINZ'): setze(kenn('S10', gr, z, zt, 'ALL', 'X'), None, G_EINGANG)
            else:
                setze(kenn('S10', 'CV', z, zt, 'ALL', 'X'), 100.0 * te / mittel(werte))
                if ses is None:
                    setze(kenn('S10', 'RTS', z, zt, 'ALL', 'X'), None, G_EINGANG); setze(kenn('S10', 'FLEINZ', z, zt, 'ALL', 'X'), None, G_EINGANG)
                elif ses == 0:
                    setze(kenn('S10', 'RTS', z, zt, 'ALL', 'X'), None, G_KONST); setze(kenn('S10', 'FLEINZ', z, zt, 'ALL', 'X'), int(te > ses))
                else:
                    setze(kenn('S10', 'RTS', z, zt, 'ALL', 'X'), te / ses); setze(kenn('S10', 'FLEINZ', z, zt, 'ALL', 'X'), int(te > ses))
        else:
            SESOI_POST[z] = SESOI_F * S if S is not None else None     # R1 Lesart a, nur für S11, ohne Kennung
        for vm in ('VA', 'VB', 'VC'):
            tev, ntev, dftev, _ = te_aus(werte_je_spieler(z, zp, MENGEN[vm]))
            setze(kenn('S10', 'TE', z, zt, vm, 'X'), tev, None if tev is not None else G_WENIG)
            setze(kenn('S10', 'DFTE', z, zt, vm, 'X'), dftev); setze(kenn('S10', 'NTE', z, zt, vm, 'X'), ntev)
P('  SESOI prä:', {z: (round(SESOI[z], 5) if SESOI[z] else None) for z in ZIELE7})

P('\nS11 BESTWERT-BIAS')
for z in ZIELE6:
    for zt, zp in ZEITEN.items():
        deltas = []
        for c in CODES:
            d = dict(zellen.get((c, zp, z), []))
            if all(j in d for j in (1, 2, 3)):
                deltas.append(bestwert([d[1], d[2], d[3]], RICHTUNG[z]) - bestwert([d[1], d[2]], RICHTUNG[z]))
        setze(kenn('S11', 'N', z, zt, 'ALL', 'X'), len(deltas))
        dm = mittel(deltas) if deltas else None
        setze(kenn('S11', 'DMEAN', z, zt, 'ALL', 'X'), dm, None if dm is not None else G_WENIG)
        ses = SESOI[z] if zt == 'PRE' else SESOI_POST[z]
        if dm is None or ses is None: setze(kenn('S11', 'DSESOI', z, zt, 'ALL', 'X'), None, G_EINGANG)
        elif ses == 0: setze(kenn('S11', 'DSESOI', z, zt, 'ALL', 'X'), None, G_KONST)
        else: setze(kenn('S11', 'DSESOI', z, zt, 'ALL', 'X'), dm / ses)

# =====================================================================================
# M  S12 Deskription
# =====================================================================================
P('\nS12 DESKRIPTION')
def nmsd(s, gr_n, gr_m, gr_sd, z, zt, menge, var, werte):
    setze(kenn(s, gr_n, z, zt, menge, var), len(werte))
    setze(kenn(s, gr_m, z, zt, menge, var), mittel(werte) if werte else None, None if werte else G_WENIG)
    setze(kenn(s, gr_sd, z, zt, menge, var), sd(werte) if len(werte) >= 2 else None, None if len(werte) >= 2 else G_WENIG)
for g in ('IG', 'KG'):
    for z, f in (('AGE', lambda c: pers[c]['alter']), ('HGT', lambda c: pers[c]['hgt']), ('MASS', lambda c: pers[c]['mass']), ('PAH', lambda c: PAH[c])):
        nmsd('S12', 'N', 'M', 'SD', z, 'PRE', 'ANA' + g, 'X', [f(c) for c in ANA[g] if f(c) is not None])
    cs = MENGEN[g]
    setze(kenn('S12', 'NFAM1', 'FAM', 'PRE', g, 'X'), sum(1 for c in cs if pers[c]['fam'] == 1))
    setze(kenn('S12', 'NFAM2', 'FAM', 'PRE', g, 'X'), sum(1 for c in cs if pers[c]['fam'] == 2))
    setze(kenn('S12', 'NFAMNA', 'FAM', 'PRE', g, 'X'), sum(1 for c in cs if pers[c]['fam'] is None))
for z in ZIELE7:
    for mn, setz in (('BASE', [c for c in CODES if hat(c, 'prä', z)]), ('ITT', ITT[z])):
        ig = [BEST[(c, 'prä', z)] for c in teil(setz, 'IG')]; kg = [BEST[(c, 'prä', z)] for c in teil(setz, 'KG')]
        sp = sd_pool(ig, kg)
        if sp is None: setze(kenn('S12', 'D', z, 'PRE', mn, 'HAUPT'), None, G_WENIG)
        elif sp == 0: setze(kenn('S12', 'D', z, 'PRE', mn, 'HAUPT'), None, G_KONST)
        else: setze(kenn('S12', 'D', z, 'PRE', mn, 'HAUPT'), (mittel(ig) - mittel(kg)) / sp)
    for g in ('IG', 'KG'):
        nmsd('S12', 'N', 'M', 'SD', z, 'PRE', g, 'HAUPT', [BEST[(c, 'prä', z)] for c in MENGEN[g] if hat(c, 'prä', z)])
        for zt, zp in ZEITEN.items():
            nmsd('S12', 'N', 'M', 'SD', z, zt, 'ITT' + g, 'HAUPT', [BEST[(c, zp, z)] for c in teil(ITT[z], g)])

# =====================================================================================
# N  Modelle: S13 Hauptanalyse, S14 Voraussetzungen, S15 Effektstärke, S16, S17
# =====================================================================================
def modell(setz, y_von, kov, extra=None):
    """Kleinste Quadrate Post ~ G + Kovariaten im Set. kov = Liste von Funktionen c -> Wert. Rückgabe kq-dict oder None."""
    cs = list(setz); g = np.array([1.0 if pers[c]['gruppe'] == 'IG' else 0.0 for c in cs])
    cols = [np.ones(len(cs)), g] + [np.array([f(c) for c in cs], float) for f in kov]
    if extra is not None: cols.append(extra(cs, g))
    X = np.column_stack(cols); y = np.array([y_von(c) for c in cs], float)
    m = kq(X, y)
    if m is not None: m['g'] = g; m['cs'] = cs; m['X'] = X; m['y'] = y
    return m
def b1_ausgabe(s, z, menge, var, m, nig, nkg, inf_ok):
    """Ausgabe b1 mit SE, df, t, p, KI sowie n je Gruppe (S16, S17). A10: bei INF = 0 nur n_IG und n_KG."""
    setze(kenn(s, 'NIG', z, 'X', menge, var), nig); setze(kenn(s, 'NKG', z, 'X', menge, var), nkg)
    for gr in ('B1', 'SEB1', 'DF', 'T', 'P', 'KIU', 'KIO'):
        if not inf_ok: setze(kenn(s, gr, z, 'X', menge, var), None, G_FALLZAHL)
        elif m is None: setze(kenn(s, gr, z, 'X', menge, var), None, G_RANG)
    if inf_ok and m is not None:
        b1, se1, df = float(m['b'][1]), float(m['se'][1]), m['df']; t = b1 / se1; tc = t_q(PQ, df)
        for gr, v in (('B1', b1), ('SEB1', se1), ('DF', df), ('T', t), ('P', t_p2(t, df)), ('KIU', b1 - tc * se1), ('KIO', b1 + tc * se1)):
            setze(kenn(s, gr, z, 'X', menge, var), v)

P('\nS13 HAUPTANALYSE (ANCOVA im ITT-Set)')
MOD = {}; SIGS = {}
for z in KONF:
    setz = ITT[z]; nig, nkg = len(teil(setz, 'IG')), len(teil(setz, 'KG'))
    setze(kenn('S13', 'NIG', z, 'X', 'ITT', 'HAUPT'), nig); setze(kenn('S13', 'NKG', z, 'X', 'ITT', 'HAUPT'), nkg)
    GR = ['B0', 'B1', 'B2', 'B3', 'SEB0', 'SEB1', 'SEB2', 'SEB3', 'SIGMA', 'DF', 'R2', 'T', 'P', 'KIU', 'KIO', 'AMIG', 'AMKG', 'SEAMIG', 'SEAMKG',
          'AMIGU', 'AMIGO', 'AMKGU', 'AMKGO', 'SIG', 'PREM', 'PAHM']
    if INF[(z, 'ITT')] == 0:
        for gr in GR: setze(kenn('S13', gr, z, 'X', 'ITT', 'HAUPT'), None, G_FALLZAHL)
        MOD[z] = None; continue
    m = modell(setz, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)], lambda c: PAH[c]])
    if m is None:
        for gr in GR: setze(kenn('S13', gr, z, 'X', 'ITT', 'HAUPT'), None, G_RANG)
        MOD[z] = None; continue
    MOD[z] = m; b, se, df = m['b'], m['se'], m['df']; tc = t_q(PQ, df); t = float(b[1] / se[1]); p = t_p2(t, df)
    for i in range(4): setze(kenn('S13', 'B%d' % i, z, 'X', 'ITT', 'HAUPT'), float(b[i])); setze(kenn('S13', 'SEB%d' % i, z, 'X', 'ITT', 'HAUPT'), float(se[i]))
    setze(kenn('S13', 'SIGMA', z, 'X', 'ITT', 'HAUPT'), m['sigma']); setze(kenn('S13', 'DF', z, 'X', 'ITT', 'HAUPT'), df); setze(kenn('S13', 'R2', z, 'X', 'ITT', 'HAUPT'), m['r2'])
    setze(kenn('S13', 'T', z, 'X', 'ITT', 'HAUPT'), t); setze(kenn('S13', 'P', z, 'X', 'ITT', 'HAUPT'), p)
    setze(kenn('S13', 'KIU', z, 'X', 'ITT', 'HAUPT'), float(b[1] - tc * se[1])); setze(kenn('S13', 'KIO', z, 'X', 'ITT', 'HAUPT'), float(b[1] + tc * se[1]))
    prem = mittel([BEST[(c, 'prä', z)] for c in setz]); pahm = mittel([PAH[c] for c in setz])
    setze(kenn('S13', 'PREM', z, 'X', 'ITT', 'HAUPT'), prem); setze(kenn('S13', 'PAHM', z, 'X', 'ITT', 'HAUPT'), pahm)
    for g, lab in ((1.0, 'IG'), (0.0, 'KG')):
        cvec = np.array([1.0, g, prem, pahm]); am = float(cvec @ b); seam = math.sqrt(float(cvec @ m['cov'] @ cvec))
        setze(kenn('S13', 'AM' + lab, z, 'X', 'ITT', 'HAUPT'), am); setze(kenn('S13', 'SEAM' + lab, z, 'X', 'ITT', 'HAUPT'), seam)
        setze(kenn('S13', 'AM' + lab + 'U', z, 'X', 'ITT', 'HAUPT'), am - tc * seam); setze(kenn('S13', 'AM' + lab + 'O', z, 'X', 'ITT', 'HAUPT'), am + tc * seam)
    guenstig = (b[1] > 0) if RICHTUNG[z] == 'max' else (b[1] < 0)
    SIGS[z] = int(p < ALPHA and guenstig); setze(kenn('S13', 'SIG', z, 'X', 'ITT', 'HAUPT'), SIGS[z])
    P('  %s: n %d/%d, df %d, b1 (gerechnet, nicht im Chat zu nennen), SIG %d' % (z, nig, nkg, df, SIGS[z]))
setze('S13.H0REJ.X.X.ITT.HAUPT', int(any(v == 1 for v in SIGS.values()))); setze('S13.NTEST.X.X.ITT.HAUPT', sum(INF[(z, 'ITT')] for z in KONF))

P('\nS14 VORAUSSETZUNGEN')
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; GRAFIK = True
except Exception: GRAFIK = False
for z in KONF:
    m = MOD[z]
    GR1 = ['SWW', 'SWP', 'SWVERW', 'BFF', 'BFDF1', 'BFDF2', 'BFP', 'BFVERW', 'SDRIG', 'SDRKG', 'SDRQ', 'OVPREIG', 'OVPREKG', 'OVPRL', 'OVPRU', 'OVPAHIG', 'OVPAHKG', 'OVPAL', 'OVPAU']
    GR2 = ['BINT', 'SEINT', 'TINT', 'DFINT', 'PINT', 'VERW']
    if m is None:
        grund = G_FALLZAHL if INF[(z, 'ITT')] == 0 else G_RANG
        for gr in GR1: setze(kenn('S14', gr, z, 'X', 'ITT', 'HAUPT'), None, grund)
        for var in ('SLPRE', 'SLPAH'):
            for gr in GR2: setze(kenn('S14', gr, z, 'X', 'ITT', var), None, grund)
    else:
        res = m['res']; g = m['g']; cs = m['cs']
        sw = shapiro(res)
        if sw is None:
            for gr in ('SWW', 'SWP', 'SWVERW'): setze(kenn('S14', gr, z, 'X', 'ITT', 'HAUPT'), None, G_WENIG)
        else:
            setze(kenn('S14', 'SWW', z, 'X', 'ITT', 'HAUPT'), sw[0]); setze(kenn('S14', 'SWP', z, 'X', 'ITT', 'HAUPT'), sw[1]); setze(kenn('S14', 'SWVERW', z, 'X', 'ITT', 'HAUPT'), int(sw[1] < ALPHA))
        bf = brown_forsythe(res, [int(x) for x in g])
        setze(kenn('S14', 'BFF', z, 'X', 'ITT', 'HAUPT'), bf['F']); setze(kenn('S14', 'BFDF1', z, 'X', 'ITT', 'HAUPT'), bf['df1']); setze(kenn('S14', 'BFDF2', z, 'X', 'ITT', 'HAUPT'), bf['df2'])
        setze(kenn('S14', 'BFP', z, 'X', 'ITT', 'HAUPT'), bf['p']); setze(kenn('S14', 'BFVERW', z, 'X', 'ITT', 'HAUPT'), int(bf['p'] < ALPHA))
        rig = [float(e) for e, gg in zip(res, g) if gg == 1]; rkg = [float(e) for e, gg in zip(res, g) if gg == 0]
        sdi, sdk = sd(rig), sd(rkg)
        setze(kenn('S14', 'SDRIG', z, 'X', 'ITT', 'HAUPT'), sdi, None if sdi is not None else G_WENIG); setze(kenn('S14', 'SDRKG', z, 'X', 'ITT', 'HAUPT'), sdk, None if sdk is not None else G_WENIG)
        if sdi is None or sdk is None: setze(kenn('S14', 'SDRQ', z, 'X', 'ITT', 'HAUPT'), None, G_EINGANG)
        elif sdi == 0: setze(kenn('S14', 'SDRQ', z, 'X', 'ITT', 'HAUPT'), None, G_KONST)
        else: setze(kenn('S14', 'SDRQ', z, 'X', 'ITT', 'HAUPT'), sdk / sdi)
        for var, kov in (('SLPRE', lambda c: BEST[(c, 'prä', z)]), ('SLPAH', lambda c: PAH[c])):
            mi = modell(cs, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)], lambda c: PAH[c]],
                        extra=lambda cs_, g_: g_ * np.array([kov(c) for c in cs_], float))
            if mi is None:
                for gr in GR2: setze(kenn('S14', gr, z, 'X', 'ITT', var), None, G_RANG)
            else:
                bi, sei, dfi = float(mi['b'][4]), float(mi['se'][4]), mi['df']; ti = bi / sei; pi = t_p2(ti, dfi)
                for gr, v in (('BINT', bi), ('SEINT', sei), ('TINT', ti), ('DFINT', dfi), ('PINT', pi), ('VERW', int(pi < ALPHA))): setze(kenn('S14', gr, z, 'X', 'ITT', var), v)
        for lab, f in (('PR', lambda c: BEST[(c, 'prä', z)]), ('PA', lambda c: PAH[c])):
            L, U, nig_, nkg_ = ueberlappung([f(c) for c in teil(cs, 'IG')], [f(c) for c in teil(cs, 'KG')])
            pre = 'OVPRE' if lab == 'PR' else 'OVPAH'
            setze(kenn('S14', pre + 'IG', z, 'X', 'ITT', 'HAUPT'), nig_); setze(kenn('S14', pre + 'KG', z, 'X', 'ITT', 'HAUPT'), nkg_)
            setze(kenn('S14', 'OV' + lab + 'L', z, 'X', 'ITT', 'HAUPT'), L); setze(kenn('S14', 'OV' + lab + 'U', z, 'X', 'ITT', 'HAUPT'), U)
        if GRAFIK:
            for name, fig_fn in (('QQ', 'qq'), ('Linearitaet', 'lin')):
                fig, axs = plt.subplots(1, 1 if fig_fn == 'qq' else 3, figsize=(6 if fig_fn == 'qq' else 15, 5))
                if fig_fn == 'qq':
                    osm, osr = stats.probplot(res, dist='norm', fit=False)
                    order = np.argsort(res); gg = g[order]
                    axs.scatter(osm[gg == 1], osr[gg == 1], marker='o', facecolors='none', edgecolors='k', label='IG')
                    axs.scatter(osm[gg == 0], osr[gg == 0], marker='^', color='k', label='KG')
                    lim = [min(osm), max(osm)]; axs.plot(lim, [np.mean(res) + np.std(res, ddof=1) * v for v in lim], 'k--', lw=0.8)
                    axs.set_xlabel('theoretische Quantile'); axs.set_ylabel('Residuen'); axs.set_title('Normal-Q-Q ' + z); axs.legend()
                else:
                    for ax, (xx, xl) in zip(axs, ((m['fitted'], 'Vorhersage'), (m['X'][:, 2], 'Prä'), (m['X'][:, 3], '%PAH'))):
                        ax.scatter(xx[g == 1], res[g == 1], marker='o', facecolors='none', edgecolors='k', label='IG'); ax.scatter(xx[g == 0], res[g == 0], marker='^', color='k', label='KG')
                        ax.axhline(0, color='k', lw=0.8); ax.set_xlabel(xl); ax.set_ylabel('Residuen'); ax.legend()
                    fig.suptitle('Linearität ' + z)
                fig.savefig(os.path.join(AUSGABE, 'S14_%s_%s_Python.png' % (name, z)), dpi=100); plt.close(fig)
    # Regel 6: Vorab-Prüfung in BPAH (R4 Lesart a: Fallzahlregel für beide Prüfungen)
    bpah = [c for c in CODES if hat(c, 'prä', z) and PAH[c] is not None]
    if inf(bpah) == 0:
        for gr in ('CINT', 'SECINT', 'TCINT', 'DFCINT', 'PCINT'): setze(kenn('S14', gr, z, 'PRE', 'BPAH', 'SLPAH'), None, G_FALLZAHL)
        for g_ in ('IG', 'KG'):
            for gr in ('SWW', 'SWP'): setze(kenn('S14', gr, z, 'PRE', 'BPAH' + g_, 'X'), None, G_FALLZAHL)
    else:
        mv = modell(bpah, lambda c: BEST[(c, 'prä', z)], [lambda c: PAH[c]], extra=lambda cs_, g_: g_ * np.array([PAH[c] for c in cs_], float))
        if mv is None:
            for gr in ('CINT', 'SECINT', 'TCINT', 'DFCINT', 'PCINT'): setze(kenn('S14', gr, z, 'PRE', 'BPAH', 'SLPAH'), None, G_RANG)
        else:
            ci, sec, dfc = float(mv['b'][3]), float(mv['se'][3]), mv['df']; tcv = ci / sec
            for gr, v in (('CINT', ci), ('SECINT', sec), ('TCINT', tcv), ('DFCINT', dfc), ('PCINT', t_p2(tcv, dfc))): setze(kenn('S14', gr, z, 'PRE', 'BPAH', 'SLPAH'), v)
        for g_ in ('IG', 'KG'):
            sw = shapiro([BEST[(c, 'prä', z)] for c in teil(bpah, g_)])
            setze(kenn('S14', 'SWW', z, 'PRE', 'BPAH' + g_, 'X'), sw[0] if sw else None, None if sw else G_WENIG)
            setze(kenn('S14', 'SWP', z, 'PRE', 'BPAH' + g_, 'X'), sw[1] if sw else None, None if sw else G_WENIG)
P('  Voraussetzungsprüfungen gerechnet für', [z for z in KONF if MOD[z] is not None], '· Grafiken:', 'ja' if GRAFIK else 'nein (matplotlib fehlt)')

P('\nS15 EFFEKTSTÄRKE UND UNADJUSTIERTE DIFFERENZ')
for z in KONF:
    m = MOD[z]; GR = ['SDPRE', 'DFG', 'J', 'G', 'GKIU', 'GKIO', 'UD', 'UDSE', 'UDT', 'UDDF', 'UDP', 'UDKIU', 'UDKIO', 'MPOSTIG', 'MPOSTKG', 'SDPOST']
    if m is None:
        for gr in GR: setze(kenn('S15', gr, z, 'X', 'ITT', 'HAUPT'), None, G_FALLZAHL if INF[(z, 'ITT')] == 0 else G_RANG)
        continue
    cs = m['cs']; ig, kg = teil(cs, 'IG'), teil(cs, 'KG'); nig, nkg = len(ig), len(kg)
    sp = sd_pool([BEST[(c, 'prä', z)] for c in ig], [BEST[(c, 'prä', z)] for c in kg]); dfg = nig + nkg - 2; J = 1 - 3 / (4 * dfg - 1)
    b1, se1 = float(m['b'][1]), float(m['se'][1]); tc = t_q(PQ, m['df'])
    setze(kenn('S15', 'SDPRE', z, 'X', 'ITT', 'HAUPT'), sp); setze(kenn('S15', 'DFG', z, 'X', 'ITT', 'HAUPT'), dfg); setze(kenn('S15', 'J', z, 'X', 'ITT', 'HAUPT'), J)
    if sp == 0:
        for gr in ('G', 'GKIU', 'GKIO'): setze(kenn('S15', gr, z, 'X', 'ITT', 'HAUPT'), None, G_KONST)
    else:
        setze(kenn('S15', 'G', z, 'X', 'ITT', 'HAUPT'), b1 / sp * J); setze(kenn('S15', 'GKIU', z, 'X', 'ITT', 'HAUPT'), (b1 - tc * se1) / sp * J); setze(kenn('S15', 'GKIO', z, 'X', 'ITT', 'HAUPT'), (b1 + tc * se1) / sp * J)
    pi, pk = [BEST[(c, 'post', z)] for c in ig], [BEST[(c, 'post', z)] for c in kg]
    du = mittel(pi) - mittel(pk); spp = sd_pool(pi, pk); seu = spp * math.sqrt(1 / nig + 1 / nkg); tu = du / seu; dfu = nig + nkg - 2; tcu = t_q(PQ, dfu)
    for gr, v in (('UD', du), ('UDSE', seu), ('UDT', tu), ('UDDF', dfu), ('UDP', t_p2(tu, dfu)), ('UDKIU', du - tcu * seu), ('UDKIO', du + tcu * seu),
                  ('MPOSTIG', mittel(pi)), ('MPOSTKG', mittel(pk)), ('SDPOST', spp)): setze(kenn('S15', gr, z, 'X', 'ITT', 'HAUPT'), v)

P('\nS16 PER-PROTOKOLL UND ANTRAGSKRITERIUM')
for z in KONF:
    setz = PP[(z, 6)]; nig, nkg = len(teil(setz, 'IG')), len(teil(setz, 'KG')); ok = INF[(z, 'PP6')] == 1
    m = modell(setz, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)], lambda c: PAH[c]]) if ok else None
    b1_ausgabe('S16', z, 'PP6', 'HAUPT', m, nig, nkg, ok)
    for zt, zp in ZEITEN.items():
        w = [BEST[(c, zp, z)] for c in teil(setz, 'IG')]
        setze(kenn('S16', 'M', z, zt, 'PP6IG', 'HAUPT'), mittel(w) if w else None, None if w else G_WENIG)
        setze(kenn('S16', 'SD', z, zt, 'PP6IG', 'HAUPT'), sd(w) if len(w) >= 2 else None, None if len(w) >= 2 else G_WENIG)
    for c in AK9[z]: setze(kenn('S16', 'DIFF', z, 'DIFF', 'P' + c, 'AK9'), BEST[(c, 'post', z)] - BEST[(c, 'prä', z)])
P('  AK9-Sets:', {z: len(AK9[z]) for z in KONF})

P('\nS17 SENSITIVITÄTSANALYSEN')
for z in KONF:
    itt = ITT[z]; nig, nkg = len(teil(itt, 'IG')), len(teil(itt, 'KG')); ok = INF[(z, 'ITT')] == 1
    b1_ausgabe('S17', z, 'ITT', 'MW', modell(itt, lambda c: MEAN[(c, 'post', z)], [lambda c: MEAN[(c, 'prä', z)], lambda c: PAH[c]]) if ok else None, nig, nkg, ok)
    b1_ausgabe('S17', z, 'ITT', 'AEND', modell(itt, lambda c: BEST[(c, 'post', z)] - BEST[(c, 'prä', z)], [lambda c: PAH[c]]) if ok else None, nig, nkg, ok)
    b1_ausgabe('S17', z, 'ITT', 'OPAH', modell(itt, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)]]) if ok else None, nig, nkg, ok)
    for s in (5, 7):
        setz = PP[(z, s)]; oks = INF[(z, 'PP%d' % s)] == 1
        b1_ausgabe('S17', z, 'PP%d' % s, 'HAUPT', modell(setz, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)], lambda c: PAH[c]]) if oks else None,
                   len(teil(setz, 'IG')), len(teil(setz, 'KG')), oks)
        for zt, zp in ZEITEN.items():
            w = [BEST[(c, zp, z)] for c in teil(setz, 'IG')]
            setze(kenn('S17', 'M', z, zt, 'PP%dIG' % s, 'HAUPT'), mittel(w) if w else None, None if w else G_WENIG)
            setze(kenn('S17', 'SD', z, zt, 'PP%dIG' % s, 'HAUPT'), sd(w) if len(w) >= 2 else None, None if len(w) >= 2 else G_WENIG)
    fams = FAMS[z]; okf = INF[(z, 'FAMS')] == 1
    b1_ausgabe('S17', z, 'FAMS', 'FAMB', modell(fams, lambda c: BEST[(c, 'post', z)], [lambda c: BEST[(c, 'prä', z)], lambda c: PAH[c], lambda c: float(pers[c]['fam'])]) if okf else None,
               len(teil(fams, 'IG')), len(teil(fams, 'KG')), okf)
    for g in ('IG', 'KG'):
        for zt, zp in ZEITEN.items():
            w = [BEST[(c, zp, z)] for c in teil(fams, g)]
            setze(kenn('S17', 'M', z, zt, 'FAMS' + g, 'FAMB'), mittel(w) if w else None, None if w else G_WENIG)
            setze(kenn('S17', 'SD', z, zt, 'FAMS' + g, 'FAMB'), sd(w) if len(w) >= 2 else None, None if len(w) >= 2 else G_WENIG)
        for fv in (1, 2):
            w = [BEST[(c, 'post', z)] - BEST[(c, 'prä', z)] for c in teil(itt, g) if pers[c]['fam'] == fv]
            nmsd('S17', 'N', 'M', 'SD', z, 'DIFF', 'ITT' + g, 'F%d' % fv, w)

# =====================================================================================
# O  S18 Sensitivitäts-Poweranalyse, S19 Bootstrap
# =====================================================================================
P('\nS18 POWERANALYSE (Standardweg)')
for z in ('Z10', 'Z30', 'CM', 'SBJ'):
    nig, nkg = len(teil(ITT[z], 'IG')), len(teil(ITT[z], 'KG')); N = nig + nkg; df2 = N - 4
    setze(kenn('S18', 'NTOT', z, 'X', 'ITT', 'X'), N); setze(kenn('S18', 'DF1', z, 'X', 'ITT', 'X'), 1); setze(kenn('S18', 'DF2', z, 'X', 'ITT', 'X'), df2)
    ds = ['D006', 'D011'] if z == 'Z10' else ['D037', 'D093']
    if df2 <= 0 or nig == 0 or nkg == 0:
        setze(kenn('S18', 'FCRIT', z, 'X', 'ITT', 'X'), None, G_WENIG)
        for d in ds: setze(kenn('S18', 'POW', z, 'X', 'ITT', d), None, G_WENIG)
        if z != 'Z10':
            for gr in ('MDES', 'MDESR'): setze(kenn('S18', gr, z, 'X', 'ITT', 'X'), None, G_WENIG)
        continue
    fc = f_q(1 - ALPHA, 1, df2); setze(kenn('S18', 'FCRIT', z, 'X', 'ITT', 'X'), fc)
    pw = lambda d: power_ncf(1, df2, d * d * nig * nkg / N, fc)
    for d in ds: setze(kenn('S18', 'POW', z, 'X', 'ITT', d), pw(D_ERW[d]))
    if z != 'Z10':
        if pw(NULL_HI) < POWER_ZIEL:
            for gr in ('MDES', 'MDESR'): setze(kenn('S18', gr, z, 'X', 'ITT', 'X'), None, G_NULLST)
        else:
            dstar = float(optimize.brentq(lambda d: pw(d) - POWER_ZIEL, NULL_LO, NULL_HI, xtol=NULL_TOL, rtol=4 * np.finfo(float).eps, maxiter=500))
            setze(kenn('S18', 'MDES', z, 'X', 'ITT', 'X'), dstar); setze(kenn('S18', 'MDESR', z, 'X', 'ITT', 'X'), dstar / SESOI_F)
P('  gerechnet für Z10, Z30, CM, SBJ')

P('\nS19 BOOTSTRAP-KONFIDENZINTERVALL')
for z in KONF:
    GR = ['BKIU', 'BKIO', 'BSD', 'BMCU', 'BMCO', 'BNGUELT', 'BNVERW']
    if MOD[z] is None:
        for gr in GR: setze(kenn('S19', gr, z, 'X', 'ITT', 'BOOT'), None, G_FALLZAHL if INF[(z, 'ITT')] == 0 else G_RANG)
        continue
    rng = np.random.default_rng(BOOT_SEED)
    m = MOD[z]; X = m['X']; y = m['y']; g = m['g']
    iig = np.where(g == 1)[0]; ikg = np.where(g == 0)[0]; nig, nkg = len(iig), len(ikg)
    b1s = []; verworfen = 0
    for _ in range(BOOT_B):
        idx = np.concatenate([rng.choice(iig, nig, replace=True), rng.choice(ikg, nkg, replace=True)])
        Xb = X[idx]; yb = y[idx]
        if np.linalg.matrix_rank(Xb) < Xb.shape[1]: verworfen += 1; continue
        Q, R = np.linalg.qr(Xb, mode='reduced'); bb = np.linalg.solve(R, Q.T @ yb); b1s.append(float(bb[1]))
    ng = len(b1s)
    setze(kenn('S19', 'BNGUELT', z, 'X', 'ITT', 'BOOT'), ng); setze(kenn('S19', 'BNVERW', z, 'X', 'ITT', 'BOOT'), verworfen)
    if ng < 2:      # Fassung 2, Befund 4 der Durchsicht: Fehlerpfad ohne doppelte Kennung
        for gr in ('BKIU', 'BKIO', 'BSD', 'BMCU', 'BMCO'): setze(kenn('S19', gr, z, 'X', 'ITT', 'BOOT'), None, G_WENIG)
        P('  %s: %d gültige Ziehungen, %d verworfen, keine Grenzen' % (z, ng, verworfen)); continue
    setze(kenn('S19', 'BKIU', z, 'X', 'ITT', 'BOOT'), quantil7(b1s, 1 - PQ)); setze(kenn('S19', 'BKIO', z, 'X', 'ITT', 'BOOT'), quantil7(b1s, PQ)); setze(kenn('S19', 'BSD', z, 'X', 'ITT', 'BOOT'), sd(b1s))
    bl = BOOT_BLOECKE * (ng // BOOT_BLOECKE); bs = ng // BOOT_BLOECKE
    if bs < 1:
        for gr in ('BMCU', 'BMCO'): setze(kenn('S19', gr, z, 'X', 'ITT', 'BOOT'), None, G_WENIG)
    else:
        bloecke = [b1s[i * bs:(i + 1) * bs] for i in range(BOOT_BLOECKE)]
        setze(kenn('S19', 'BMCU', z, 'X', 'ITT', 'BOOT'), sd([quantil7(bk, 1 - PQ) for bk in bloecke]) / math.sqrt(BOOT_BLOECKE))
        setze(kenn('S19', 'BMCO', z, 'X', 'ITT', 'BOOT'), sd([quantil7(bk, PQ) for bk in bloecke]) / math.sqrt(BOOT_BLOECKE))
    P('  %s: %d gültige Ziehungen, %d verworfen' % (z, ng, verworfen))

# =====================================================================================
# P  Ergebnisdatei nach G.1: Sollliste ausschreiben, Vollständigkeit prüfen, schreiben
# =====================================================================================
P('\nERGEBNISDATEI NACH G.1')
soll_liste = []
for r in KENN:
    sm = r['spielermenge']
    if sm == '':
        soll_liste.append((r['kennung'], r['einheit']))
    else:
        if sm == 'ALLE': cs = CODES
        elif sm == 'IG': cs = IG
        elif sm == 'AK9': cs = AK9[r['ziel']]
        else: raise Abbruch('ABBRUCH: unbekannte Spielermenge ' + sm)
        for c in cs: soll_liste.append((r['kennung'].replace('P<Code>', 'P' + c), r['einheit']))
soll_set = set(k for k, _ in soll_liste)
pruefe(len(soll_set) == len(soll_liste), 'Sollliste hat doppelte Kennungen')
fehlt = [k for k in soll_set if k not in ERG]; zuviel = [k for k in ERG if k not in soll_set]
pruefe(not fehlt, 'Kennungen ohne Ausgabe:', len(fehlt), fehlt[:10])
pruefe(not zuviel, 'Kennungen außerhalb der Anlage:', len(zuviel), zuviel[:10])
def fmt(v):
    return str(v) if isinstance(v, int) else '%.17g' % v
with open(ERGEBNIS, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['Kennung', 'Wert', 'Einheit', 'Grund', 'Skript'])
    for k, einheit in soll_liste:
        v, grund = ERG[k]
        w.writerow([k, '' if v is None else fmt(v), einheit, grund, SKRIPT])
gruende = Counter(g for v, g in ERG.values() if v is None)
P('  Kennungen der Anlage (Muster): %d, ausgeschrieben: %d, davon Spielerkennungen: %d' % (len(KENN), len(soll_liste), len(soll_liste) - sum(1 for r in KENN if r['spielermenge'] == '')))
P('  Zeilen mit Wert: %d, fehlend mit Grund: %d' % (sum(1 for v, _ in ERG.values() if v is not None), sum(gruende.values())))
for gr, n in sorted(gruende.items()): P('    Grund %s: %d' % (gr, n))
P('  Datei:', ERGEBNIS, ' SHA-256', sha256_datei(ERGEBNIS))
P('  Skript:', os.path.abspath(__file__), ' SHA-256', sha256_datei(os.path.abspath(__file__)))
P('\nLauf beendet ohne Abbruch:', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))
with open(PROTOKOLL, 'w', encoding='utf-8') as f: f.write(buf.getvalue())

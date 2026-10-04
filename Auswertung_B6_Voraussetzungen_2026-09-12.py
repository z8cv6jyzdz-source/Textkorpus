# -*- coding: utf-8 -*-
"""
Auswertung_B6_Voraussetzungen_2026-09-12.py — Phase B, Schritt B6: Voraussetzungen der ANCOVA — was VOR dem 15.09. prüfbar ist
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.

Datenquelle: Statistik\Studiendaten_U15_gesamt.xlsx — 02_Rohdaten (B0.2/B0.3), 01_Personen.
Die residuenbasierten Prüfungen (Normalverteilung der Residuen, Varianzhomogenität, Homogenität der Steigungen
Gruppe × Prä und Gruppe × %PAH, Linearität) gehören zum gefitteten Post-Modell und stehen in B7; sie laufen
nach Eintragung der KG-Post-Werte. Hier: alles, was ohne KG-Post-Werte bereits prüfbar ist.

Verbindliche Formulierung (§ 11.9): „geprüft und nicht verworfen; der Test hat bei dieser Fallzahl nur die Kraft,
sehr große Unterschiede zu entdecken.“ Nicht „erfüllt“.

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B6_Voraussetzungen_2026-09-12.py [Pfad zum Workbook]
Inhalt:
  1  Überlappung der Kovariatenbereiche (%PAH, Prä-Wert) je Zielgröße im ANCOVA-Set — Extrapolationsrisiko
  2  Verteilung der Prä-Bestwerte und der IG-Post-Bestwerte: Shapiro-Wilk, Schiefe, Ausreißer (> 3 SD)
  3  Homogenität der Regressionssteigungen für %PAH an den PRÄ-Werten (Prä ~ Gruppe + %PAH + Gruppe × %PAH) —
     Vorabprüfung analog § 11.9 („kleinstes p = 0,110“; SBJ-Steigung KG ≈ 4 × IG)
  4  Linearität Prä ~ %PAH (quadratischer Term) je Gruppe — Vorabprüfung
  5  Innerhalb der IG (einzige Gruppe mit Post): Post ~ Prä + %PAH — Steigungen, Residuen; Muster für B7
"""
import sys, os, io, math, datetime, statistics
from collections import Counter, defaultdict, OrderedDict
import numpy as np
import openpyxl
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
def _finde(*rel):
    # Skript liegt in Claude\03_Skripte\ (Ordnerkonvention § 1.4) oder flach in Claude\ — beide Lagen werden gefunden
    for up in ('..', os.path.join('..', '..'), os.path.join('..', '..', '..')):
        p = os.path.join(HERE, up, *rel)
        if os.path.exists(p): return os.path.abspath(p)
    return os.path.join(HERE, '..', *rel)
WB = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else _finde('Statistik', 'Studiendaten_U15_gesamt.xlsx')
OUT = os.path.splitext(os.path.abspath(__file__))[0] + '.txt'
buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); buf.write(s + '\n')

ZIEL = OrderedDict([
    ('5m',   ('Sprint_5m', '–', 's', 'min')),
    ('10m',  ('Sprint_10m', '–', 's', 'min')),
    ('30m',  ('Sprint_30m', '–', 's', 'min')),
    ('505L', ('COD_505', 'L', 's', 'min')),
    ('505R', ('COD_505', 'R', 's', 'min')),
    ('505M', ('COD_505', 'M', 's', 'min')),   # abgeleitet: Mittelwert beider Beinseiten (Ethikantrag § 3), keine Rohzeilen
    ('SBJ',  ('Standweitsprung', '–', 'cm', 'max')),
])
GRUPPE = {'Hohenlind': 'IG', 'Blau-Weiß Köln': 'IG', 'Vorwärts Spoho': 'KG'}
VEREIN_KURZ = {'Hohenlind': 'A', 'Blau-Weiß Köln': 'B', 'Vorwärts Spoho': 'C'}
def num(v):
    if v is None or v == '': return None
    if isinstance(v, (int, float)): return float(v)
    try: return float(str(v).replace(',', '.'))
    except ValueError: return None
def lade_rohdaten(pfad):
    wb = openpyxl.load_workbook(pfad, data_only=True, read_only=True)
    ws = wb['02_Rohdaten']; rows = list(ws.iter_rows(values_only=True))
    COL = {str(h): i for i, h in enumerate(rows[0])}
    out = []
    for r in rows[1:]:
        if r[COL['Code']] is None: continue
        d = {c: r[COL[c]] for c in ('Code', 'Verein', 'Zeitpunkt', 'Test', 'Seite', 'Versuch', 'Wert', 'ungültig', 'Bemerkung')}
        d['Wert'] = num(d['Wert'])
        d['ungültig'] = str(d['ungültig']).strip() if d['ungültig'] not in (None, '') else ''
        d['gilt_neu'] = 1 if (d['Wert'] is not None and d['ungültig'] == '') else 0
        d['Gruppe'] = GRUPPE[d['Verein']]; d['VereinK'] = VEREIN_KURZ[d['Verein']]
        d['Z'] = next(k for k, (t, s, u, m) in ZIEL.items() if t == d['Test'] and s == d['Seite'])
        out.append(d)
    return out, wb

def ergaenze_505M(agg, tupel=False):
    """505 Mittelwert beider Beinseiten (Ethikantrag § 3, Auswertungsplan 12.09.): je Spieler und Zeitpunkt
    best = (Best_L + Best_R)/2, mittel = (Mittel_L + Mittel_R)/2 — nur wenn beide Seiten einen gültigen Wert haben.
    'werte' = versuchsweise gepaarte Einzelversuche ((V1_L+V1_R)/2, …), k = min(k_L, k_R): dient nur der Messgüte des
    zusammengesetzten Werts (B3/B8); Bestwert und Mittelwert werden NICHT aus den Paaren gebildet."""
    for (c, zp, z) in [k for k in agg if k[2] == '505L']:
        L, R = agg[(c, zp, '505L')], agg.get((c, zp, '505R'))
        if R is None: continue
        k = min(L['k'], R['k'])
        if 'werte' not in L: paare = []                     # Skripte ohne Einzelversuche (B5–B7): nur k, best, mittel
        elif tupel: paare = [(j + 1, (L['werte'][j][1] + R['werte'][j][1]) / 2) for j in range(k)]
        else: paare = [(L['werte'][j] + R['werte'][j]) / 2 for j in range(k)]
        agg[(c, zp, '505M')] = dict(k=k, werte=paare, best=(L['best'] + R['best']) / 2, mittel=(L['mittel'] + R['mittel']) / 2)
    return agg

def aggregiere(data):
    zellen = defaultdict(list)
    for d in sorted(data, key=lambda d: d['Versuch']):
        if d['gilt_neu'] == 1: zellen[(d['Code'], d['Zeitpunkt'], d['Z'])].append(d['Wert'])
    agg = {}
    for key, w in zellen.items():
        richtung = ZIEL[key[2]][3]
        agg[key] = dict(k=len(w), best=(min(w) if richtung == 'min' else max(w)), mittel=sum(w) / len(w))
    return agg
def lade_personen(wb):
    ws = wb['01_Personen']; rows = list(ws.iter_rows(values_only=True)); h = [str(x) for x in rows[0]]
    pers = OrderedDict()
    for r in rows[1:]:
        d = dict(zip(h, r)); c = d.get('Code')
        if not isinstance(c, str) or c[:3] not in ('HL-', 'BW-', 'VS-'): continue
        pers[c] = dict(Gruppe=GRUPPE[d['Verein']], VereinK=VEREIN_KURZ[d['Verein']], PAH=num(d.get('PAH_Prozent')))
    return pers

def ols(X, y):
    """Kleinste Quadrate; liefert b, SE, t, p, df_e, SSE, R²."""
    X = np.asarray(X, float); y = np.asarray(y, float); n, p = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; sse = float(res @ res); dfe = n - p
    s2 = sse / dfe; cov = s2 * np.linalg.inv(X.T @ X); se = np.sqrt(np.diag(cov)); t = b / se; pv = 2 * stats.t.sf(np.abs(t), dfe)
    sst = float(((y - y.mean()) ** 2).sum()); return dict(b=b, se=se, t=t, p=pv, dfe=dfe, sse=sse, r2=1 - sse / sst, res=res, cov=cov)
def f_nested(X0, X1, y):
    """F-Test des Modellvergleichs (X0 ⊂ X1)."""
    m0, m1 = ols(X0, y), ols(X1, y); df1 = X1.shape[1] - X0.shape[1]
    F = ((m0['sse'] - m1['sse']) / df1) / (m1['sse'] / m1['dfe']); return F, df1, m1['dfe'], stats.f.sf(F, df1, m1['dfe'])

data, wb = lade_rohdaten(WB); agg = ergaenze_505M(aggregiere(data)); pers = lade_personen(wb); codes = list(pers)
P('=' * 100)
P('B6 VORAUSSETZUNGEN — Prüfungen, die vor der KG-Post-Eingabe möglich sind')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P('=' * 100)

# ---------------------------------------------------------------- 1 Überlappung
P('\n1  ÜBERLAPPUNG DER KOVARIATENBEREICHE IM ANCOVA-SET (prä + %PAH; IG zusätzlich mit Post-Wert; KG-Post steht aus)')
P('  Wo sich die Gruppen im Wertebereich einer Kovariate nicht überlappen, extrapoliert die ANCOVA (§ 11.9).')
P(f"{'Zielgröße':10s}{'Kovariate':10s}{'IG n':>5s}{'IG Bereich':>18s}{'KG n':>5s}{'KG Bereich':>18s}{'gem. Bereich':>18s}{'IG im Ber.':>11s}{'KG im Ber.':>11s}{'Anteil ges.':>12s}")
for z in ZIEL:
    ig = [c for c in codes if pers[c]['Gruppe'] == 'IG' and (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    kg = [c for c in codes if pers[c]['Gruppe'] == 'KG' and (c, 'prä', z) in agg and pers[c]['PAH'] is not None]
    for kname, val in (('%PAH', lambda c: pers[c]['PAH']), ('Prä-Wert', lambda c: agg[(c, 'prä', z)]['best'])):
        a = [val(c) for c in ig]; b = [val(c) for c in kg]; lo, hi = max(min(a), min(b)), min(max(a), max(b))
        dec = 1 if (z == 'SBJ' and kname == 'Prä-Wert') else 2
        f = lambda x: f'{x:.{dec}f}'
        na = sum(1 for x in a if lo <= x <= hi); nb = sum(1 for x in b if lo <= x <= hi)
        P(f"{z:10s}{kname:10s}{len(a):5d}{(f(min(a)) + '–' + f(max(a))):>18s}{len(b):5d}{(f(min(b)) + '–' + f(max(b))):>18s}{(f(lo) + '–' + f(hi) if lo <= hi else 'KEINE'):>18s}{(str(na) + '/' + str(len(a))):>11s}{(str(nb) + '/' + str(len(b))):>11s}{100 * (na + nb) / (len(a) + len(b)):11.0f} %")
P('  5 m: KG-Set n = 7 (< 8) und IG nur zu einem Drittel im gemeinsamen Bereich → drittes Argument für „nur deskriptiv“ (§ 11.9).')
P('  10 m: IG-Set n = 7 (< 8), IG-Bereich liegt größtenteils unterhalb der KG → nur deskriptiv.')

# ---------------------------------------------------------------- 2 Verteilungen
P('\n2  VERTEILUNGEN DER BESTWERTE — Shapiro-Wilk (W, p), Schiefe (g1), Werte außerhalb M ± 3 SD')
P('  Ein nicht signifikanter Test ist bei diesen n kein Nachweis der Normalverteilung (§ 11.9: Erkennungsrate bei n = 8 nur 48 %).')
P(f"{'Zielgröße':10s}{'Menge':10s}{'n':>3s}{'W':>7s}{'p':>7s}{'Schiefe':>8s}{'> 3 SD':>8s}")
for z in ZIEL:
    for mname, filt, zp in (('IG prä', lambda c: pers[c]['Gruppe'] == 'IG', 'prä'), ('KG prä', lambda c: pers[c]['Gruppe'] == 'KG', 'prä'), ('IG post', lambda c: pers[c]['Gruppe'] == 'IG', 'post')):
        v = np.array([agg[(c, zp, z)]['best'] for c in codes if filt(c) and (c, zp, z) in agg])
        if len(v) < 4: P(f'{z:10s}{mname:10s}{len(v):3d}   —'); continue
        W, p = stats.shapiro(v); g1 = stats.skew(v, bias=False); out = int(np.sum(np.abs(v - v.mean()) > 3 * v.std(ddof=1)))
        P(f'{z:10s}{mname:10s}{len(v):3d}{W:7.3f}{p:7.3f}{g1:8.2f}{out:8d}')

# ---------------------------------------------------------------- 3 Steigungshomogenität PAH (prä)
P('\n3  HOMOGENITÄT DER REGRESSIONSSTEIGUNGEN FÜR %PAH — an den PRÄ-Werten (Vorabprüfung; die eigentliche Prüfung läuft am Post-Modell in B7)')
P('  Modell: Prä ~ Gruppe + %PAH + Gruppe × %PAH (ANCOVA-Set). F-Test des Interaktionsterms; Steigungen je Gruppe.')
P(f"{'Zielgröße':10s}{'n':>3s}{'Steig. IG':>11s}{'Steig. KG':>11s}{'Verh. KG/IG':>12s}{'F':>7s}{'df':>8s}{'p':>7s}")
for z in ZIEL:
    pl = [c for c in codes if (c, 'prä', z) in agg and pers[c]['PAH'] is not None and (pers[c]['Gruppe'] == 'KG' or (c, 'post', z) in agg)]
    y = np.array([agg[(c, 'prä', z)]['best'] for c in pl]); g = np.array([1.0 if pers[c]['Gruppe'] == 'IG' else 0.0 for c in pl]); pah = np.array([pers[c]['PAH'] for c in pl])
    pah_c = pah - pah.mean()
    X0 = np.column_stack([np.ones(len(pl)), g, pah_c]); X1 = np.column_stack([X0, g * pah_c])
    F, df1, df2, p = f_nested(X0, X1, y); m1 = ols(X1, y)
    s_kg = m1['b'][2]; s_ig = m1['b'][2] + m1['b'][3]
    P(f"{z:10s}{len(pl):3d}{s_ig:11.4f}{s_kg:11.4f}{(s_kg / s_ig if s_ig != 0 else float('nan')):12.2f}{F:7.2f}{(str(df1) + '/' + str(df2)):>8s}{p:7.3f}")
P('  § 11.9 (Stand F9, n = 28): „nirgends verworfen (kleinstes p = 0,110)“; SBJ: Steigung KG fast viermal so hoch wie IG. Hier mit den aktuellen Sets neu gerechnet.')

# ---------------------------------------------------------------- 4 Linearität prä ~ PAH
P('\n4  LINEARITÄT PRÄ ~ %PAH — F-Test eines quadratischen Terms (Prä ~ Gruppe + %PAH + %PAH²), ANCOVA-Set')
P(f"{'Zielgröße':10s}{'n':>3s}{'b linear':>10s}{'F quad.':>8s}{'p':>7s}{'R² lin.':>8s}{'R² quad.':>9s}")
for z in ZIEL:
    pl = [c for c in codes if (c, 'prä', z) in agg and pers[c]['PAH'] is not None and (pers[c]['Gruppe'] == 'KG' or (c, 'post', z) in agg)]
    y = np.array([agg[(c, 'prä', z)]['best'] for c in pl]); g = np.array([1.0 if pers[c]['Gruppe'] == 'IG' else 0.0 for c in pl]); pah = np.array([pers[c]['PAH'] for c in pl]); pah_c = pah - pah.mean()
    X0 = np.column_stack([np.ones(len(pl)), g, pah_c]); X1 = np.column_stack([X0, pah_c ** 2])
    F, df1, df2, p = f_nested(X0, X1, y); m0 = ols(X0, y); m1 = ols(X1, y)
    P(f"{z:10s}{len(pl):3d}{m0['b'][2]:10.4f}{F:8.2f}{p:7.3f}{m0['r2']:8.3f}{m1['r2']:9.3f}")

# ---------------------------------------------------------------- 5 IG: Post ~ Prä + PAH
P('\n5  INNERHALB DER IG: Post ~ Prä + %PAH (Bestwert) — Steigungen und Residuen; technisches Muster für B7, KEIN Gruppenvergleich')
P(f"{'Zielgröße':10s}{'n':>3s}{'b Prä':>8s}{'SE':>7s}{'b %PAH':>9s}{'SE':>8s}{'R²':>6s}{'SW-W Res.':>10s}{'p':>7s}{'Res.-SD':>9s}")
for z in ZIEL:
    pl = [c for c in codes if pers[c]['Gruppe'] == 'IG' and (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    if len(pl) < 6: P(f'{z:10s}{len(pl):3d}   — (n < 6)'); continue
    y = np.array([agg[(c, 'post', z)]['best'] for c in pl]); pre = np.array([agg[(c, 'prä', z)]['best'] for c in pl]); pah = np.array([pers[c]['PAH'] for c in pl])
    X = np.column_stack([np.ones(len(pl)), pre - pre.mean(), pah - pah.mean()]); m = ols(X, y); W, p = stats.shapiro(m['res'])
    P(f"{z:10s}{len(pl):3d}{m['b'][1]:8.3f}{m['se'][1]:7.3f}{m['b'][2]:9.4f}{m['se'][2]:8.4f}{m['r2']:6.2f}{W:10.3f}{p:7.3f}{math.sqrt(m['sse'] / m['dfe']):9.4f}")
P('  Lesart: b Prä nahe 1 = Post folgt dem Prä-Wert; R² ist die Vorhersagekraft der Kovariaten innerhalb der IG (Erwartung für die R²-Sensitivität in B8).')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

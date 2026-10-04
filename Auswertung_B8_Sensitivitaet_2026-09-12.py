# -*- coding: utf-8 -*-
"""
Auswertung_B8_Sensitivitaet_2026-09-12.py — Phase B, Schritt B8: Sensitivitätsanalysen (vorab festgelegt)
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.
Korrektur 12.09.2026 (Task 4.4, abends): Die Innerhalb-Spieler-Streuung wird am Mittel der jeweils verwendeten Werte zentriert (bei 505M: Mittel der
  gepaarten Versuche statt (Mittel_L + Mittel_R)/2). Betrifft nur 505M bei k_L ≠ k_R (HL-02, HL-03, VS-03): TE prä alle 0,0587 → 0,0579 s. Übrige Zielgrößen unverändert.

Vier Sensitivitätsanalysen nach § 11.5 / Übergabeprompt B8, Status am 11.09.2026:
  F6  Mittelwert statt Bestwert            → Modell in B7 (Abschnitt C), läuft nach KG-Post-Eingabe; Aggregation und Baseline-d hier verglichen
  F2  Familiarisierung                     → NICHT durchführbar: Spalte ohne Varianz (29 × „1“, 2 leer; B4 § 7). Schwab-Punkt 4.
  F3  R²-Variation 0,30–0,79               → hier: Sensitivitäts-Poweranalyse (MDES) mit den AKTUELLEN n je Zielgröße; R² über die Spanne
  Änderungswert-Rechnung (Δ ~ Gruppe + %PAH) → Modell in B7 (Abschnitt E), läuft nach KG-Post-Eingabe; Lord's Paradox in 6.1
  Schwellen ≥ 5 / ≥ 7 (B0.1 c)              → Modelle in B7 (Abschnitt D)

Sensitivitäts-Poweranalyse (§ 11.1; Verfahren identisch mit AnhangG_Kovariatenkorrelation.py, Stand 09.09.):
  Testfamilie: t-Test des Gruppenkoeffizienten der ANCOVA (zweiseitig, α = 0,05), Numerator-df = 1, 2 Gruppen, 2 Kovariaten,
  df_e = n1 + n2 − 2 − 2, Power 0,80. MDES (in Einheiten der Prä-SD zwischen Spielern) = ncp(0,80; df_e) · √(1 − R²) · √(1/n1 + 1/n2 + Q).
  R²max = rel², rel = 1 − TE²/SD² (Obergrenze der Prä-Post-Korrelation aus der Messgüte, B3 prä alle) — MODELLGRÖSSE, nach dem 15.09. am
  gefitteten Modell zu ersetzen (gemessenes R²). Q = (d1² − 2·r·d1·d2 + d2²) / [(1 − r²)·(N − 2)] mit d1 = Baseline-d (Prä), d2 = d(%PAH),
  r = gruppenzentrierte Korrelation Prä ↔ %PAH im Analyseset; SE-Inflation = √((1/n1 + 1/n2 + Q)/(1/n1 + 1/n2)).
  Software: Python 3 + SciPy (nichtzentrale t-Verteilung), Version im Kopf der Ausgabe. Kein Post-hoc-Power-Argument (§ 11.1).

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B8_Sensitivitaet_2026-09-12.py [Pfad zum Workbook]
"""
import sys, os, io, math, datetime, statistics, platform
from collections import Counter, defaultdict, OrderedDict
import numpy as np
import scipy, openpyxl
from scipy import stats, optimize

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

ALPHA, POWER, K_KOV = 0.05, 0.80, 2
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
        agg[key] = dict(k=len(w), werte=w, best=(min(w) if richtung == 'min' else max(w)), mittel=sum(w) / len(w))
    return agg
def lade_personen(wb):
    ws = wb['01_Personen']; rows = list(ws.iter_rows(values_only=True)); h = [str(x) for x in rows[0]]
    pers = OrderedDict()
    for r in rows[1:]:
        d = dict(zip(h, r)); c = d.get('Code')
        if not isinstance(c, str) or c[:3] not in ('HL-', 'BW-', 'VS-'): continue
        pers[c] = dict(Gruppe=GRUPPE[d['Verein']], VereinK=VEREIN_KURZ[d['Verein']], PAH=num(d.get('PAH_Prozent')), Fam=num(d.get('Familiarisierung')))
    return pers

def _pw(tc, df, nc):
    lo = stats.nct.cdf(-tc, df, nc); hi = stats.nct.sf(tc, df, nc)
    return (hi if hi == hi else 0.0) + (lo if lo == lo else 0.0)
def ncp_for_power(df, power=POWER, alpha=ALPHA):
    tc = stats.t.ppf(1 - alpha / 2, df)
    return optimize.brentq(lambda nc: _pw(tc, df, nc) - power, 0.01, 15.0)
def power_at(d, n1, n2, R2, Q, df):
    nc = d / (math.sqrt(1 - R2) * math.sqrt(1 / n1 + 1 / n2 + Q)); tc = stats.t.ppf(1 - ALPHA / 2, df)
    return _pw(tc, df, nc)
def d_pooled(a, b):
    n1, n2 = len(a), len(b); m1, m2 = sum(a) / n1, sum(b) / n2
    sp = math.sqrt((sum((v - m1) ** 2 for v in a) + sum((v - m2) ** 2 for v in b)) / (n1 + n2 - 2)); return (m1 - m2) / sp

data, wb = lade_rohdaten(WB); agg = ergaenze_505M(aggregiere(data)); pers = lade_personen(wb); codes = list(pers)
P('=' * 110)
P('B8 SENSITIVITÄTSANALYSEN — Stand und Sensitivitäts-Poweranalyse (MDES) mit aktuellen n')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P(f'Software: Python {platform.python_version()} · NumPy {np.__version__} · SciPy {scipy.__version__} (nichtzentrale t-Verteilung) · α = {ALPHA} zweiseitig · Power = {POWER}')
P('=' * 110)

# ---------------------------------------------------------------- Messgüte prä (für R²max, SESOI)
def messguete_prae(z):
    ss = 0.0; df = 0; bests = []
    for c in codes:
        a = agg.get((c, 'prä', z))
        if a is None: continue
        bests.append(a['best'])
        if a['k'] >= 2: m = sum(a['werte']) / len(a['werte']); ss += sum((x - m) ** 2 for x in a['werte']); df += a['k'] - 1
    te = math.sqrt(ss / df); sd = statistics.stdev(bests); return te, sd, 0.2 * sd

# ---------------------------------------------------------------- 1 MDES aktuell
P('\n1  SENSITIVITÄTS-POWERANALYSE (MDES) — Analyseset je Zielgröße: prä + %PAH; IG zusätzlich mit Post-Wert; KG = maximal erreichbar (Post steht aus)')
P(f"{'Zielgröße':10s}{'n1/n2':>7s}{'df_e':>5s}{'TE':>8s}{'SD':>8s}{'R²max':>7s}{'d1':>7s}{'d2':>7s}{'r_w':>7s}{'Q':>8s}{'Fakt.SE':>8s}{'MDES oQ':>9s}{'×SESOI':>8s}{'MDES mQ':>9s}{'×SESOI':>8s}{'KI½ mQ':>9s}")
ERG = {}
for z in ZIEL:
    ig = [c for c in codes if pers[c]['Gruppe'] == 'IG' and (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    kg = [c for c in codes if pers[c]['Gruppe'] == 'KG' and (c, 'prä', z) in agg and pers[c]['PAH'] is not None]
    n1, n2 = len(ig), len(kg); N = n1 + n2; df = N - 2 - K_KOV
    x = [agg[(c, 'prä', z)]['best'] for c in ig + kg]; y = [pers[c]['PAH'] for c in ig + kg]
    xc = [v - (sum(x[:n1]) / n1 if i < n1 else sum(x[n1:]) / n2) for i, v in enumerate(x)]
    yc = [v - (sum(y[:n1]) / n1 if i < n1 else sum(y[n1:]) / n2) for i, v in enumerate(y)]
    r_w = sum(a * b for a, b in zip(xc, yc)) / math.sqrt(sum(a * a for a in xc) * sum(b * b for b in yc))
    d1 = d_pooled(x[:n1], x[n1:]); d2 = d_pooled(y[:n1], y[n1:])
    base = 1 / n1 + 1 / n2; Q = (d1 ** 2 - 2 * r_w * d1 * d2 + d2 ** 2) / ((1 - r_w ** 2) * (N - 2)); infl = math.sqrt((base + Q) / base)
    te, sd, sesoi = messguete_prae(z); R2 = (1 - te ** 2 / sd ** 2) ** 2
    nc = ncp_for_power(df); m0 = nc * math.sqrt(1 - R2) * math.sqrt(base); m1 = nc * math.sqrt(1 - R2) * math.sqrt(base + Q)
    hw1 = stats.t.ppf(0.975, df) * sd * math.sqrt(1 - R2) * math.sqrt(base + Q)
    ERG[z] = dict(n1=n1, n2=n2, df=df, R2=R2, Q=Q, sd=sd, sesoi=sesoi, m0=m0, m1=m1)
    P(f"{z:10s}{(str(n1) + '/' + str(n2)):>7s}{df:5d}{te:8.4f}{sd:8.4f}{R2:7.3f}{d1:7.2f}{d2:7.2f}{r_w:7.3f}{Q:8.4f}{infl:8.3f}{m0:9.2f}{m0 * sd / sesoi:8.1f}{m1:9.2f}{m1 * sd / sesoi:8.1f}{hw1:9.4f}")
P('  MDES in Einheiten der Prä-SD zwischen Spielern (Cohen-d-Skala); ×SESOI = MDES·SD/SESOI = Vielfaches des SESOI (0,2·SD) → immer MDES/0,2.')
P('  505M = Mittelwert beider Beinseiten (konfirmatorisch, Ethikantrag); TE für R²max aus den gepaarten Einzelversuchen (B3 § 11). 505 L/R nur zur Information (deskriptiv).')
P('  KI½ = halbe Breite des 95-%-KI der adjustierten Differenz in Rohheiten (mit Q). 5 m und 10 m nur zur Information: nach § 11.9 deskriptiv.')
P('  Fassung 9 § 11.1 (n 17/7, 17/11, 17/11, 17/11, 16/10, 16/11): MDES mit Q 1,43 · 0,72 · 0,54 · 0,73 · 1,34 · 1,32 (×SESOI 7,1 · 3,6 · 2,7 · 3,7 · 6,7 · 6,6); Faktor SE 1,433 · 1,341 · 1,387 · 1,280 · 1,235 · 1,330.')
P('  ⚠ Abweichungen gegenüber § 11.1 entstehen aus den geänderten Analysesets (IG 16 statt 17 mit Post-Bedingung; 10 m IG 7), nicht aus einer Methodenänderung.')

# ---------------------------------------------------------------- 2 Power bei Vorab-Erwartungen
P('\n2  POWER BEI DEN DOKUMENTIERTEN VORAB-ERWARTUNGEN (§ 6.5/§ 11.1) — Literaturerwartungen, keine Annahmen über unseren Effekt')
ERW = [('Lloyd et al. (2016), 10 m, d = 0,06', 0.06), ('RC (2020), 10 m ≤ 7 Wo., d = 0,11', 0.11), ('Moran et al. (2017), CMJ, d = 0,37', 0.37), ('RC (2020), Sprung/Sprint kurz, d ≈ 0,7', 0.70), ('d = 0,93', 0.93)]
for i, (lab, d) in enumerate(ERW): P(f'   E{i + 1}: {lab}')
P(f"{'Zielgröße':10s}" + ''.join(f'{("E" + str(i + 1) + " (d=" + str(d) + ")"):>14s}' for i, (_, d) in enumerate(ERW)))
for z in ZIEL:
    e = ERG[z]; P(f'{z:10s}' + ''.join(f"{power_at(d, e['n1'], e['n2'], e['R2'], e['Q'], e['df']):14.2f}" for _, d in ERW))

# ---------------------------------------------------------------- 3 R²-Variation
P('\n3  R²-SENSITIVITÄT (F3): MDES mit Q über R² = 0,30 … 0,79 (statt R²max) — Schlussfolgerung darf nicht an der R²-Annahme hängen')
grid = [0.30, 0.40, 0.50, 0.60, 0.70, 0.79]
P(f"{'Zielgröße':10s}{'R²max':>7s}" + ''.join(f'{("R²=" + str(r)):>10s}' for r in grid) + '   (MDES in d, jeweils ×SESOI in Klammern)')
for z in ZIEL:
    e = ERG[z]; nc = ncp_for_power(e['df']); base = 1 / e['n1'] + 1 / e['n2']
    line = f"{z:10s}{e['R2']:7.3f}"
    for r in grid:
        m = nc * math.sqrt(1 - r) * math.sqrt(base + e['Q']); line += f'{m:5.2f}({m / 0.2:3.1f})'
    P(line)
P('  Über die gesamte Spanne bleibt der MDES bei 30 m, SBJ, 505M (und 505 L/R) ein Vielfaches des SESOI; die Aussage „Sprint unterpowert für d ≈ 0,1“ hängt nicht an R².')
P('  Nach dem 15.09.: R² aus dem gefitteten Modell (B7) einsetzen; R²max ist eine Obergrenze aus der Messgüte (Modellrechnung, § 1.1: Messung geht vor).')

# ---------------------------------------------------------------- 4 Aggregation: Bestwert vs Mittelwert (Vorbereitung F6)
P('\n4  F6 MITTELWERT STATT BESTWERT — Baseline-d und Prä-Post-Δ der IG unter beiden Aggregationen (das ANCOVA-Modell folgt in B7 C)')
P(f"{'Zielgröße':10s}{'d Baseline Best':>16s}{'d Baseline Mittel':>18s}{'Δ IG Best':>11s}{'Δ IG Mittel':>12s}{'Diff. Δ':>9s}{'in SESOI':>9s}")
for z in ZIEL:
    ig = [c for c in codes if pers[c]['Gruppe'] == 'IG' and (c, 'prä', z) in agg]; kg = [c for c in codes if pers[c]['Gruppe'] == 'KG' and (c, 'prä', z) in agg]
    db = d_pooled([agg[(c, 'prä', z)]['best'] for c in ig], [agg[(c, 'prä', z)]['best'] for c in kg]); dm = d_pooled([agg[(c, 'prä', z)]['mittel'] for c in ig], [agg[(c, 'prä', z)]['mittel'] for c in kg])
    pl = [c for c in ig if (c, 'post', z) in agg]
    if len(pl) < 2: P(f'{z:10s}{db:16.2f}{dm:18.2f}   —'); continue
    dlb = statistics.mean(agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best'] for c in pl); dlm = statistics.mean(agg[(c, 'post', z)]['mittel'] - agg[(c, 'prä', z)]['mittel'] for c in pl)
    P(f'{z:10s}{db:16.2f}{dm:18.2f}{dlb:11.3f}{dlm:12.3f}{dlm - dlb:9.3f}{(dlm - dlb) / ERG[z]["sesoi"]:9.2f}')
P('  Weichen Bestwert- und Mittelwertanalyse nach dem 15.09. nicht ab, ist § 11.8 erledigt; weichen sie ab, gehört das in 6.1.')

# ---------------------------------------------------------------- 5 Familiarisierung
P('\n5  F2 FAMILIARISIERUNG (Stand 12.09.: Spalte je Spieler 1/2 aus Anwesenheitslisten; Verein A durchgängig 1, B 8 × 2 / 3 × 1, C 12 × 2, VS-11 leer)')
P('  Variante a (Ausschluss der Spieler mit einer Familiarisierung): IG-Set fällt auf n < 8 → nur deskriptiv (B4 § 7). Variante b (Kovariate 1/2): in B7 Block F, nach KG-Post.')
P('  ⚠ In der IG ist die Dosis mit Verein A konfundiert (alle A = 1) — Variante b schätzt Vereins- und Familiarisierungseffekt gemeinsam; nur als Sensitivität berichten.')
P('  Deskriptiv heute (IG, Bestwert): Prä-Post-Δ nach Familiarisierungsdosis — kein Gruppenvergleich, keine Inferenz:')
for z in ZIEL:
    parts = []
    for famv in (1, 2):
        pl = [c for c in codes if pers[c]['Gruppe'] == 'IG' and pers[c]['Fam'] == famv and (c, 'prä', z) in agg and (c, 'post', z) in agg]
        if len(pl) < 2: parts.append(f'Fam={famv}: n={len(pl)}'); continue
        dl = [agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best'] for c in pl]
        parts.append(f'Fam={famv}: n={len(pl)} Δ={statistics.mean(dl):+.3f} (SD {statistics.stdev(dl):.3f})')
    P(f'   {z:5s} ' + ' · '.join(parts))
P('  (Zeiten negativ = schneller, Standweitsprung positiv = weiter; Fam = 1 ist bei 30 m/SBJ/505 praktisch Verein A + BW-01/BW-02.)')
P('\n6  ÄNDERUNGSWERT-RECHNUNG (Δ ~ Gruppe + %PAH) und MODELL OHNE %PAH — vorab festgelegt, Modelle in B7 E; Lord\'s Paradox in 6.1 (§ 11.2).')
P('   Erwartung: Bei Baseline-d bis −1,7 unterscheiden sich ANCOVA- und Änderungswert-Schätzer systematisch (b2 < 1); beide beantworten verschiedene Fragen.')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

# -*- coding: utf-8 -*-
"""
Auswertung_B7_ANCOVA_2026-09-12.py — Phase B, Schritt B7: Konfirmatorische ANCOVA — Spezifikation, Sperre, technische Verifikation
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.

⚠ SPERRE: Die konfirmatorische Rechnung läuft NUR, wenn für die Zielgröße KG-Post-Werte vorliegen. Am 11.09.2026 liegen keine vor
(KG-Post-Termin 15.09.2026). Bis dahin führt das Skript ausschließlich die technische Verifikation aus (Simulation mit bekanntem
Effekt; Pseudo-Gruppenvergleich Verein A gegen B innerhalb der IG als reiner Code-Test, ohne inhaltliche Bedeutung).
Die Rechenkette steht damit VOR Kenntnis der KG-Werte fest (Datum: 11.09.2026).

Modell (§ 11.2): Post = b0 + b1·Gruppe + b2·Prä + b3·%PAH + e,  Gruppe: IG = 1, KG = 0; Prä und %PAH am Gesamtmittel des Analysesets zentriert.
  b1 = adjustierte Gruppendifferenz im Post-Wert (IG − KG) „bei rechnerisch gleichem Ausgangswert und Reifestatus“ (§ 10).
  Ausgabe je Zielgröße (§ 11.2, CONSORT Item 17/18): n je Gruppe · adjustierte Mittelwerte mit 95-%-KI · adjustierte Differenz mit 95-%-KI ·
  exakter p-Wert (t-Test von b1, zweiseitig, α = 0,05) · Effektstärke: partielles η² mit 90-%- und 95-%-KI (nichtzentrale F-Verteilung) und
  standardisierte adjustierte Differenz d_adj = b1 / gepoolte Prä-SD mit KI · unadjustierte Differenz der Post-Mittel mit 95-%-KI.
  Voraussetzungen am gefitteten Modell: Normalverteilung der Residuen (Shapiro-Wilk) · Varianzhomogenität der Residuen (Brown-Forsythe) ·
  Homogenität der Steigungen (F-Test für Gruppe × Prä, Gruppe × %PAH, beide) · Linearität (F-Test für Prä²) · Kovariatenüberlappung.
  Verbindliche Formulierung (§ 11.9): „geprüft und nicht verworfen; der Test hat bei dieser Fallzahl nur die Kraft, sehr große Unterschiede zu entdecken.“
Zielgrößen mit Inferenz (Auswertungsplan 12.09., § 11.9, B4): 30 m, 505M (Mittelwert beider Beinseiten, Ethikantrag § 3), Standweitsprung.
5 m, 10 m: nur deskriptiv (B5). 505 links/rechts: nur deskriptiv (B5) — keine Modelle je Seite (Ethikantrag: Mittelwert; § 11.2 F9 „seitengetrennt“ ist überholt).
COD-Defizit: entfällt (nicht im Antrag; 10-m-Post IG n = 7).

Analysesets (§ 11.7, B9): ITT = alle Zugeteilten mit Prä-, Post-Wert und %PAH (vollständige Fälle, keine Fortschreibung) — Hauptanalyse,
  Ergebnis heißt „Wirkung des Programmangebots“. Per-Protokoll = IG-Spieler mit ≥ 6 vollständig absolvierten Einheiten (B0.1) gegen die KG —
  zusätzlich, beobachtender Vergleich. Sensitivitäten (B8): Mittelwert-Aggregation · PP ≥ 5 / ≥ 7 · Änderungswert-Modell (Δ ~ Gruppe + %PAH) ·
  Modell ohne %PAH (Schwab-Punkt 12).

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B7_ANCOVA_2026-09-12.py [Workbook] [Fragebogen-Datei]
Die Python-Rechnung ist die Gegenprobe zur SPSS-Syntax (Claude\SPSS_Syntax_2026-09-12.sps); weichen beide ab: anhalten und melden.
"""
import sys, os, io, csv, math, datetime, statistics
from collections import Counter, defaultdict, OrderedDict
import numpy as np
import openpyxl
from scipy import stats, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
def _finde(*rel):
    # Skript liegt in Claude\03_Skripte\ (Ordnerkonvention § 1.4) oder flach in Claude\ — beide Lagen werden gefunden
    for up in ('..', os.path.join('..', '..'), os.path.join('..', '..', '..')):
        p = os.path.join(HERE, up, *rel)
        if os.path.exists(p): return os.path.abspath(p)
    return os.path.join(HERE, '..', *rel)
WB = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else _finde('Statistik', 'Studiendaten_U15_gesamt.xlsx')
FB = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else _finde('SoSci_Fragebogen', 'Fragebogen Datensatz.txt')
OUT = os.path.splitext(os.path.abspath(__file__))[0] + '.txt'
buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); buf.write(s + '\n')

ALPHA = 0.05
SCHWELLE_PP = 6; SCHWELLEN_SENS = (5, 6, 7); N_MIN = 8
INFERENZ = ('30m', '505M', 'SBJ')          # Auswertungsplan 12.09.: 505 = Mittelwert beider Seiten (Ethikantrag); L/R deskriptiv
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
LISTE = {**{i: 'HL-%02d' % i for i in range(1, 9)}, **{i: 'BW-%02d' % (i - 8) for i in range(9, 23)}}
CASE_KORREKTUR = {'59': 'BW-06', '70': 'BW-06', '140': 'BW-04', '158': 'BW-04', '165': 'BW-04', '190': 'BW-04', '206': 'BW-04'}
MAP_WB = {'HL-04': 'HL-05'}   # Listenplatz HL-04 ↔ Workbook HL-05 (beide ohne echte Meldung; siehe B0 § 0)

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
        pers[c] = dict(Gruppe=GRUPPE[d['Verein']], VereinK=VEREIN_KURZ[d['Verein']], PAH=num(d.get('PAH_Prozent')), Fam=num(d.get('Familiarisierung')))
    return pers
def lade_adhaerenz(pfad):
    """vollständig absolvierte Einheiten je Workbook-Code (altes Schema, CASE-korrigiert); None = Datei fehlt."""
    if not os.path.exists(pfad): return None
    raw = open(pfad, encoding='utf-16').read(); meld = list(csv.DictReader(io.StringIO(raw), delimiter='\t'))
    ganz = Counter()
    for r in meld:
        c = CASE_KORREKTUR.get(r['CASE'], LISTE.get(int(r['H010'])) if r['H010'].strip().isdigit() else None)
        if c is None: continue
        c = MAP_WB.get(c, c)
        if r['H004'] == '1': ganz[c] += 1
    return ganz

# ---------------------------------------------------------------- Statistik-Kern
def ols(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float); n, p = X.shape
    XtX_inv = np.linalg.inv(X.T @ X); b = XtX_inv @ X.T @ y; res = y - X @ b; sse = float(res @ res); dfe = n - p
    s2 = sse / dfe; cov = s2 * XtX_inv; se = np.sqrt(np.diag(cov)); t = b / se; pv = 2 * stats.t.sf(np.abs(t), dfe)
    sst = float(((y - y.mean()) ** 2).sum())
    return dict(b=b, se=se, t=t, p=pv, dfe=dfe, sse=sse, s2=s2, r2=(1 - sse / sst if sst > 0 else float('nan')), res=res, cov=cov, X=X, y=y, fitted=X @ b)
def f_nested(X0, X1, y):
    m0, m1 = ols(X0, y), ols(X1, y); df1 = X1.shape[1] - X0.shape[1]
    F = ((m0['sse'] - m1['sse']) / df1) / (m1['sse'] / m1['dfe']); return F, df1, m1['dfe'], float(stats.f.sf(F, df1, m1['dfe']))
def ncp_ci(F, df1, df2, conf):
    """KI für die Nichtzentralität λ der F-Verteilung (Steiger, 2004); Rückgabe (λ_lo, λ_hi)."""
    lo_p, hi_p = (1 + conf) / 2, (1 - conf) / 2
    def solve(target):
        f = lambda lam: stats.ncf.cdf(F, df1, df2, lam) - target
        if f(0) < 0: return 0.0
        hi = 10.0
        while f(hi) > 0 and hi < 1e5: hi *= 2
        return optimize.brentq(f, 0, hi)
    return solve(lo_p), solve(hi_p)
def eta2_ci(F, df1, df2, conf):
    lo, hi = ncp_ci(F, df1, df2, conf); N = df1 + df2 + 1
    return lo / (lo + N), hi / (hi + N)
def brown_forsythe(res, g):
    a = res[g == 1]; b = res[g == 0]
    return stats.levene(a, b, center='median')

def ancova(y, g, x1, x2, label, dec=3, x1_name='Prä', x2_name='%PAH', sd_pre=None, x3=None, x3_name='Fam'):
    """Post ~ Gruppe + x1 + x2. Gibt Kennwerte zurück und schreibt einen Block."""
    y = np.asarray(y, float); g = np.asarray(g, float); x1 = np.asarray(x1, float); N = len(y)
    n1, n0 = int(g.sum()), int(N - g.sum())
    cols = [np.ones(N), g, x1 - x1.mean()]; names = ['const', 'Gruppe', x1_name]
    if x2 is not None:
        x2 = np.asarray(x2, float); cols.append(x2 - x2.mean()); names.append(x2_name)
    if x3 is not None:
        x3 = np.asarray(x3, float); cols.append(x3 - x3.mean()); names.append(x3_name)   # Sensitivität F2 (Variante b): Familiarisierung 1/2 als dritte Kovariate
    X = np.column_stack(cols); m = ols(X, y); dfe = m['dfe']; tc = stats.t.ppf(0.975, dfe)
    b1, se1 = m['b'][1], m['se'][1]; ci1 = (b1 - tc * se1, b1 + tc * se1); p1 = float(m['p'][1])
    # adjustierte Mittelwerte am Gesamtmittel der Kovariaten (zentriert → const bzw. const + b1)
    L_kg = np.zeros(X.shape[1]); L_kg[0] = 1; L_ig = L_kg.copy(); L_ig[1] = 1
    adj = {}
    for lab, L in (('IG', L_ig), ('KG', L_kg)):
        est = float(L @ m['b']); se = math.sqrt(float(L @ m['cov'] @ L)); adj[lab] = (est, est - tc * se, est + tc * se, se)
    F1 = float(m['t'][1] ** 2); eta2 = F1 / (F1 + dfe)
    e90 = eta2_ci(F1, 1, dfe, 0.90); e95 = eta2_ci(F1, 1, dfe, 0.95)
    # unadjustierte Differenz der Post-Mittel (gepoolte Varianz)
    yi, yk = y[g == 1], y[g == 0]; sp = math.sqrt(((n1 - 1) * yi.var(ddof=1) + (n0 - 1) * yk.var(ddof=1)) / (N - 2)); se_u = sp * math.sqrt(1 / n1 + 1 / n0)
    tu = stats.t.ppf(0.975, N - 2); du = yi.mean() - yk.mean()
    # Voraussetzungen
    W, pW = stats.shapiro(m['res']); lev = brown_forsythe(m['res'], g)
    Xi1 = np.column_stack([X, g * (x1 - x1.mean())]); Fi1, d1, d2, pi1 = f_nested(X, Xi1, y)
    if x2 is not None:
        Xi2 = np.column_stack([X, g * (x2 - x2.mean())]); Fi2, _, _, pi2 = f_nested(X, Xi2, y)
        Xi12 = np.column_stack([X, g * (x1 - x1.mean()), g * (x2 - x2.mean())]); Fi12, d12a, d12b, pi12 = f_nested(X, Xi12, y)
    Xq = np.column_stack([X, (x1 - x1.mean()) ** 2]); Fq, _, _, pq = f_nested(X, Xq, y)
    f = lambda v: f'{v:.{dec}f}'
    P(f'\n  ── {label}: N = {N} (IG {n1} / KG {n0}) · df_e = {dfe} · R² = {m["r2"]:.3f}')
    P(f'     adjustierte Mittelwerte (Kovariaten am Gesamtmittel): IG {f(adj["IG"][0])} [{f(adj["IG"][1])}; {f(adj["IG"][2])}] · KG {f(adj["KG"][0])} [{f(adj["KG"][1])}; {f(adj["KG"][2])}]')
    P(f'     adjustierte Differenz IG − KG: b1 = {f(b1)} [95 % {f(ci1[0])}; {f(ci1[1])}] · SE {f(se1)} · t({dfe}) = {m["t"][1]:.3f} · p = {p1:.4f}')
    J = 1 - 3 / (4 * dfe - 1)   # Hedges-Korrektur für kleine Stichproben
    dadj = (b1 / sd_pre * J, ci1[0] / sd_pre * J, ci1[1] / sd_pre * J) if sd_pre else (None, None, None)
    P(f'     partielles η² = {eta2:.3f} [90 % {e90[0]:.3f}; {e90[1]:.3f}] [95 % {e95[0]:.3f}; {e95[1]:.3f}]' + (f' · d_adj (Hedges, J = {J:.3f}) = b1·J/SD_prä = {dadj[0]:+.2f} [{dadj[1]:+.2f}; {dadj[2]:+.2f}]' if sd_pre else ''))
    P(f'     unadjustierte Differenz der Post-Mittel: {f(du)} [95 % {f(du - tu * se_u)}; {f(du + tu * se_u)}] (Item 18) · Post-Mittel IG {f(yi.mean())} KG {f(yk.mean())}')
    P(f'     Kovariaten: b_{x1_name} = {m["b"][2]:.4f} (SE {m["se"][2]:.4f}, p = {m["p"][2]:.4f})' + (f' · b_{x2_name} = {m["b"][3]:.4f} (SE {m["se"][3]:.4f}, p = {m["p"][3]:.4f})' if x2 is not None else '') + (f' · b_{x3_name} = {m["b"][4]:.4f} (SE {m["se"][4]:.4f}, p = {m["p"][4]:.4f})' if x3 is not None else ''))
    P(f'     Voraussetzungen: Residuen Shapiro-Wilk W = {W:.3f}, p = {pW:.3f} · Brown-Forsythe F = {lev.statistic:.2f}, p = {lev.pvalue:.3f} · Gruppe×{x1_name} F(1,{d2}) = {Fi1:.2f}, p = {pi1:.3f}'
      + (f' · Gruppe×{x2_name} F = {Fi2:.2f}, p = {pi2:.3f} · beide F(2,{d12b}) = {Fi12:.2f}, p = {pi12:.3f}' if x2 is not None else '') + f' · Linearität {x1_name}² F = {Fq:.2f}, p = {pq:.3f}')
    P(f'     Kovariatenbereiche: {x1_name} IG {x1[g == 1].min():.{dec}f}–{x1[g == 1].max():.{dec}f} / KG {x1[g == 0].min():.{dec}f}–{x1[g == 0].max():.{dec}f}' + (f' · {x2_name} IG {x2[g == 1].min():.2f}–{x2[g == 1].max():.2f} / KG {x2[g == 0].min():.2f}–{x2[g == 0].max():.2f}' if x2 is not None else ''))
    return dict(N=N, n1=n1, n0=n0, b1=b1, se1=se1, ci1=ci1, p=p1, eta2=eta2, e95=e95, adj=adj, du=du, pW=pW, pLev=lev.pvalue, pi1=pi1, pi2=(pi2 if x2 is not None else None), pq=pq, dadj=dadj, model=m)

# ---------------------------------------------------------------- Daten
data, wb = lade_rohdaten(WB); agg = ergaenze_505M(aggregiere(data)); pers = lade_personen(wb); codes = list(pers)
ganz = lade_adhaerenz(FB)
P('=' * 110)
P('B7 KONFIRMATORISCHE ANCOVA — Post ~ Gruppe + Prä + %PAH · Spezifikation, Sperre, Verifikation')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P('=' * 110)
kg_post = {z: sum(1 for c in codes if pers[c]['Gruppe'] == 'KG' and (c, 'post', z) in agg) for z in ZIEL}
P('\nKG-Post-Werte je Zielgröße:', dict(kg_post))
GESPERRT = all(v == 0 for v in kg_post.values())
P('STATUS:', 'GESPERRT — keine KG-Post-Werte; nur technische Verifikation (Abschnitt V).' if GESPERRT else 'FREIGEGEBEN — KG-Post-Werte vorhanden; Abschnitt A–E laufen.')
P('Adhärenz (Fragebogen A) geladen:', 'ja' if ganz is not None else 'NEIN — Per-Protokoll-Sets nicht bestimmbar')

def analyseset(z, agg_key='best', pp_min=None, gruppen=('IG', 'KG'), fam_min=None):
    """Zeilen (Code, Gruppe, post, prä, PAH) für das Set: vollständige Fälle; PP: IG-Spieler mit ≥ pp_min Einheiten."""
    rows = []
    for c in codes:
        if pers[c]['Gruppe'] not in gruppen: continue
        if (c, 'prä', z) not in agg or (c, 'post', z) not in agg or pers[c]['PAH'] is None: continue
        if pp_min is not None and pers[c]['Gruppe'] == 'IG' and (ganz is None or ganz.get(c, 0) < pp_min): continue
        if fam_min is not None and (pers[c]['Fam'] is None or pers[c]['Fam'] < fam_min): continue
        rows.append((c, pers[c]['Gruppe'], agg[(c, 'post', z)][agg_key], agg[(c, 'prä', z)][agg_key], pers[c]['PAH'], pers[c]['Fam']))
    return rows
def run_set(z, rows, label, dec, model='ancova'):
    g = np.array([1.0 if r[1] == 'IG' else 0.0 for r in rows]); y = np.array([r[2] for r in rows]); pre = np.array([r[3] for r in rows]); pah = np.array([r[4] for r in rows])
    n1, n0 = int(g.sum()), int(len(g) - g.sum())
    if n1 < N_MIN or n0 < N_MIN:
        P(f'\n  ── {label}: IG {n1} / KG {n0} → n < {N_MIN} in einer Gruppe: § 11.9, nur deskriptiv (keine Inferenz).'); return None
    sp = math.sqrt(((n1 - 1) * pre[g == 1].var(ddof=1) + (n0 - 1) * pre[g == 0].var(ddof=1)) / (len(g) - 2))
    if model == 'ancova': return ancova(y, g, pre, pah, label, dec, sd_pre=sp)
    if model == 'ohne_pah': return ancova(y, g, pre, None, label + ' — ohne %PAH', dec, sd_pre=sp)
    if model == 'fam':
        fam = np.array([r[5] if r[5] is not None else np.nan for r in rows])
        keep = ~np.isnan(fam)
        if keep.sum() < len(rows): P(f'     (Familiarisierung fehlt bei {int((~keep).sum())} Spieler(n) — ausgeschlossen)')
        return ancova(y[keep], g[keep], pre[keep], pah[keep], label + ' — + Familiarisierung (1/2) als Kovariate [F2 b]', dec, sd_pre=sp, x3=fam[keep])
    if model == 'aenderung': return ancova(y - pre, g, pah, None, label + ' — Änderungswert Δ ~ Gruppe + %PAH', dec, x1_name='%PAH', sd_pre=sp)

HAUPT = {}
if not GESPERRT:
    for z in INFERENZ:
        dec = 1 if z == 'SBJ' else 3
        P(f'\n{"=" * 110}\nZIELGRÖSSE {z} ({ZIEL[z][2]}) — Zeiten: negatives b1 = IG schneller; Standweitsprung: positives b1 = IG weiter')
        P('A  HAUPTANALYSE — ITT (vollständige Fälle), Bestwert')
        HAUPT[z] = run_set(z, analyseset(z), 'ITT · Bestwert', dec)
        P('B  PER-PROTOKOLL (≥ 6 Einheiten) — beobachtender Vergleich, nicht randomisiert')
        run_set(z, analyseset(z, pp_min=SCHWELLE_PP), f'PP ≥ {SCHWELLE_PP} · Bestwert', dec)
        P('C  SENSITIVITÄT: Mittelwert-Aggregation (§ 11.8)')
        run_set(z, analyseset(z, agg_key='mittel'), 'ITT · Mittelwert', dec)
        P('D  SENSITIVITÄT: PP-Schwellen ≥ 5 / ≥ 7 (B0.1 c)')
        for s in SCHWELLEN_SENS:
            if s != SCHWELLE_PP: run_set(z, analyseset(z, pp_min=s), f'PP ≥ {s} · Bestwert', dec)
        P('E  SENSITIVITÄT: Änderungswert-Modell und Modell ohne %PAH')
        run_set(z, analyseset(z), 'ITT · Bestwert', dec, model='aenderung')
        run_set(z, analyseset(z), 'ITT · Bestwert', dec, model='ohne_pah')
        P('F  SENSITIVITÄT: Familiarisierung (§ 11.5 Nr. 1) — Variante b: Kovariate 1/2 (in der IG mit Verein A konfundiert: alle A = 1); Variante a: Ausschluss der Spieler mit einer Familiarisierung')
        run_set(z, analyseset(z), 'ITT · Bestwert', dec, model='fam')
        run_set(z, analyseset(z, fam_min=2), 'ITT · Bestwert · nur Familiarisierung = 2 [F2 a]', dec)
    P('\nDeskriptiv: 5 m, 10 m (§ 11.9) sowie 505 links und rechts je Seite (Ethikantrag: Mittelwert) — siehe B5; hier keine Modelle.')
    if '--csv' in sys.argv:
        # Spaltenvertrag aus Auswertung\daten.ps1 (Lies-AncovaErgebnisse); ES = d_adj (Hedges), KI aus dem KI von b1.
        # Maßgeblich bleibt die SPSS-Ausgabe (LIESMICH: dokumentierter Übertragungsschritt) — diese Datei ist die Python-Gegenprobe
        # und wird nur nach bestandenem Vergleich (V5) für die Pipeline verwendet.
        csvp = os.path.join(os.path.dirname(_finde('Auswertung', 'daten.ps1')), 'ancova_ergebnisse.csv')
        with open(csvp, 'w', encoding='utf-8', newline='') as f:
            f.write('# Quelle: Auswertung_B7_ANCOVA_2026-09-12.py --csv (Python-Gegenprobe; SPSS-Werte vergleichen, V5); ITT, Bestwert, Post ~ Gruppe + Prä + %PAH; 505M = Mittelwert beider Seiten (Pipeline: Zielgröße 505M ergänzen)\n')
            f.write('Zielgroesse;AdjM_IG;KIu_IG;KIo_IG;AdjM_KG;KIu_KG;KIo_KG;AdjDiff;AdjDiff_KIu;AdjDiff_KIo;ES;ES_KIu;ES_KIo;P_Text\n')
            for z in INFERENZ:
                r = HAUPT.get(z)
                if not r: continue
                pt = '<0,001' if r['p'] < 0.001 else f"{r['p']:.3f}".replace('.', ',')
                vals = [r['adj']['IG'][0], r['adj']['IG'][1], r['adj']['IG'][2], r['adj']['KG'][0], r['adj']['KG'][1], r['adj']['KG'][2], r['b1'], r['ci1'][0], r['ci1'][1], r['dadj'][0], r['dadj'][1], r['dadj'][2]]
                f.write(z + ';' + ';'.join(f'{v:.4f}' for v in vals) + ';' + pt + '\n')
        P('→ ancova_ergebnisse.csv geschrieben:', csvp)

# ---------------------------------------------------------------- V Verifikation
P('\n' + '=' * 110 + '\nV  TECHNISCHE VERIFIKATION DES RECHENWEGS (läuft immer; ohne inhaltliche Bedeutung)')
P('V1 Reduktionsprobe: ohne Kovariaten muss b1 dem Mittelwertunterschied und t dem gepoolten Zweistichproben-t entsprechen.')
rng = np.random.default_rng(20260911)
a = rng.normal(0, 1, 16); b = rng.normal(0.5, 1, 11)
y = np.concatenate([a, b]); g = np.concatenate([np.ones(16), np.zeros(11)])
m = ols(np.column_stack([np.ones(27), g]), y); t_sc = stats.ttest_ind(a, b, equal_var=True)
P(f'   b1 = {m["b"][1]:+.6f} · Mittelwertdifferenz = {a.mean() - b.mean():+.6f} · t_OLS = {m["t"][1]:+.6f} · t_scipy = {t_sc.statistic:+.6f} · p_OLS = {m["p"][1]:.6f} · p_scipy = {t_sc.pvalue:.6f} → '
  + ('identisch' if abs(m['t'][1] - t_sc.statistic) < 1e-9 and abs(m['p'][1] - t_sc.pvalue) < 1e-9 else 'ABWEICHUNG'))
P('V2 Simulation mit bekanntem Effekt (Design wie unsere Studie: IG 16 / KG 11; Prä und %PAH aus den echten Daten der SBJ-Sets; KG-Post SIMULIERT):')
P('   Post = 0,9·Prä + 0,5·%PAH_c + δ·Gruppe + e, e ~ N(0, 7²). Prüfung: Wiederfindung von δ, KI-Überdeckung, Fehler 1. Art bei δ = 0 (2000 Wiederholungen).')
rows_ig = analyseset('SBJ', gruppen=('IG',)); kg_rows = [(c, 'KG', None, agg[(c, 'prä', 'SBJ')]['best'], pers[c]['PAH']) for c in codes if pers[c]['Gruppe'] == 'KG' and (c, 'prä', 'SBJ') in agg and pers[c]['PAH'] is not None]
pre = np.array([r[3] for r in rows_ig + kg_rows]); pah = np.array([r[4] for r in rows_ig + kg_rows]); g = np.array([1.0] * len(rows_ig) + [0.0] * len(kg_rows))
N = len(g); tc = stats.t.ppf(0.975, N - 4)
for delta in (0.0, 8.0):
    hits = 0; cover = 0; ests = []
    for i in range(2000):
        yy = 0.9 * pre + 0.5 * (pah - pah.mean()) + delta * g + rng.normal(0, 7, N)
        X = np.column_stack([np.ones(N), g, pre - pre.mean(), pah - pah.mean()]); mm = ols(X, yy)
        ests.append(mm['b'][1]); hits += mm['p'][1] < ALPHA; cover += (mm['b'][1] - tc * mm['se'][1] <= delta <= mm['b'][1] + tc * mm['se'][1])
    P(f'   δ = {delta:4.1f}: mittlere Schätzung {np.mean(ests):+.3f} (SD {np.std(ests):.3f}) · Anteil p < 0,05 = {hits / 2000:.3f} ({"Fehler 1. Art, Soll 0,05" if delta == 0 else "Power"}) · KI-Überdeckung {cover / 2000:.3f} (Soll 0,95)')
P('V3 Vollständiger Ausgabeblock an simulierten Daten (ein Datensatz, δ = 8 cm) — prüft Formatierung, η²-KI, Voraussetzungstests:')
yy = 0.9 * pre + 0.5 * (pah - pah.mean()) + 8.0 * g + rng.normal(0, 7, N)
sp = math.sqrt(((len(rows_ig) - 1) * pre[g == 1].var(ddof=1) + (len(kg_rows) - 1) * pre[g == 0].var(ddof=1)) / (N - 2))
ancova(yy, g, pre, pah, 'SIMULATION SBJ (KG-Post künstlich!)', 1, sd_pre=sp)
P('V4 Pseudo-Gruppen innerhalb der IG (Verein A = 1 gegen Verein B = 0), echte Post-Werte — reiner Code-Test, KEIN Ergebnis der Studie:')
for z in ('30m', 'SBJ'):
    rows = [(c, pers[c]['VereinK'], agg[(c, 'post', z)]['best'], agg[(c, 'prä', z)]['best'], pers[c]['PAH']) for c in codes if pers[c]['Gruppe'] == 'IG' and (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    g2 = np.array([1.0 if r[1] == 'A' else 0.0 for r in rows]); y2 = np.array([r[2] for r in rows]); p2 = np.array([r[3] for r in rows]); h2 = np.array([r[4] for r in rows])
    P(f'   (n A = {int(g2.sum())} < 8 → nach § 11.9 wäre dies ohnehin nur deskriptiv; hier nur Lauf des Codes)')
    ancova(y2, g2, p2, h2, f'PSEUDO A vs B · {z} (kein Studienergebnis)', 1 if z == 'SBJ' else 3, sd_pre=float(p2.std(ddof=1)))
P('\nV5 Gegenprobe zur SPSS-Syntax: Nach dem SPSS-Lauf die Werte b1, SE, p, adjustierte Mittelwerte und partielles η² je Zielgröße hier eintragen und vergleichen.')
P('   SPSS „Partial Eta Squared“ für Gruppe entspricht F/(F + df_e) mit F = t²; EMMEANS „Gruppe“ mit Kovariaten am Mittel = adjustierte Mittelwerte oben.')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

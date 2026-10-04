# -*- coding: utf-8 -*-
"""
Auswertung_B3_Messguete_2026-09-12.py — Phase B, Schritt B3: Messgüte (TE, CV, SESOI, MDC), prä und post getrennt
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.
Korrektur 12.09.2026 (Task 4.4, abends): Die Innerhalb-Spieler-Streuung wird am Mittel der jeweils verwendeten Werte zentriert (bei 505M: Mittel der
  gepaarten Versuche statt (Mittel_L + Mittel_R)/2). Betrifft nur 505M bei k_L ≠ k_R (HL-02, HL-03, VS-03): TE prä alle 0,0587 → 0,0579 s. Übrige Zielgrößen unverändert.

Einzige Datenquelle: Statistik\Studiendaten_U15_gesamt.xlsx, Blatt 02_Rohdaten (Gültigkeit nach B0.2).
04_Kennwerte wird NICHT übernommen, sondern am Ende gegengeprüft (nur prä vorhanden).

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B3_Messguete_2026-09-12.py [Pfad zum Workbook]
Ausgabe: gleichnamige .txt neben dem Skript.

Definitionen (§ 11.3; Hopkins, 2000, S. 8):
  TE   = typischer Fehler = gepoolte Intra-Personen-SD der gültigen Wiederholungsversuche einer Sitzung:
         TE = √( Σ_i SS_i / Σ_i (k_i − 1) ), SS_i = Σ_j (x_ij − x̄_i)², nur Spieler mit k_i ≥ 2.
         Das ist ein Innerhalb-Sitzung-Fehler (Untergrenze); ein Between-Session-TE ist ohne Retest nicht schätzbar (§ 12 Nr. 13).
  95-%-Konfidenzgrenzen des TE über χ² mit df = Σ (k_i − 1):  TE·√(df/χ²_{0,975;df}) … TE·√(df/χ²_{0,025;df}).
  CV   = TE / M × 100 (M = Mittel aller gültigen Versuche); zusätzlich log-CV = 100·(exp(TE_ln) − 1) mit TE_ln aus ln(x).
  SESOI = 0,2 · S_b, S_b = Zwischen-Spieler-SD der Bestwerte (Cohen, 1988, zit. n. Hopkins, 2000, S. 8) — Hauptvariante.
  SESOI_T = 0,2 · √(S_b² − TE²) — Hopkins' Präzisierung, als Sensitivitätsangabe (§ 11.3).
  MDC   = TE · 1,96 · √2 (minimal detectable change, 95 %) — Berichtsgröße, keine Entscheidungsgröße.
  TE/√n = Präzision eines Gruppenmittels aus n Spielern (Messpräzision) — NICHT die statistische Auflösung (MDES, § 11.1).
"""
import sys, os, io, math, datetime, statistics
from collections import Counter, defaultdict, OrderedDict
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
        agg[key] = dict(k=len(w), werte=w, best=(min(w) if richtung == 'min' else max(w)), mittel=sum(w) / len(w))
    return agg

data, wb = lade_rohdaten(WB); agg = ergaenze_505M(aggregiere(data))
codes = sorted(set(d['Code'] for d in data))
info = {c: next((d['Gruppe'], d['VereinK']) for d in data if d['Code'] == c) for c in codes}

def messguete(zp, z, filt=lambda c: True):
    """TE, CV, SESOI, MDC für Zielgröße z, Zeitpunkt zp, Spielerauswahl filt."""
    ss = 0.0; df = 0; ss_ln = 0.0; alle = []; bests = []; n_k2 = 0
    for c in codes:
        if not filt(c): continue
        a = agg.get((c, zp, z))
        if a is None: continue
        bests.append(a['best']); alle += a['werte']
        if a['k'] >= 2:
            n_k2 += 1; m = sum(a['werte']) / len(a['werte']); ss += sum((x - m) ** 2 for x in a['werte']); df += a['k'] - 1
            lw = [math.log(x) for x in a['werte']]; ml = sum(lw) / len(lw); ss_ln += sum((x - ml) ** 2 for x in lw)
    if df == 0 or len(bests) < 2: return None
    te = math.sqrt(ss / df); te_ln = math.sqrt(ss_ln / df)
    lo = te * math.sqrt(df / stats.chi2.ppf(0.975, df)); hi = te * math.sqrt(df / stats.chi2.ppf(0.025, df))
    M = sum(alle) / len(alle); cv = te / M * 100; cv_ln = 100 * (math.exp(te_ln) - 1)
    Mb = sum(bests) / len(bests); Sb = statistics.stdev(bests); sesoi = 0.2 * Sb
    sesoi_t = 0.2 * math.sqrt(Sb ** 2 - te ** 2) if Sb > te else float('nan')
    mdc = te * 1.96 * math.sqrt(2)
    n = len(bests)
    return dict(n=n, n_k2=n_k2, df=df, te=te, te_lo=lo, te_hi=hi, M=M, cv=cv, cv_ln=cv_ln, Mb=Mb, Sb=Sb, sesoi=sesoi, sesoi_t=sesoi_t,
                mdc=mdc, te_sesoi=te / sesoi, te_sesoi_t=(te / sesoi_t if sesoi_t == sesoi_t else float('nan')), te_sqrtn=te / math.sqrt(n), te_sqrtn_sesoi=te / math.sqrt(n) / sesoi)

P('=' * 110)
P('B3 MESSGÜTE — TE, CV, SESOI, MDC je Zielgröße, prä und post getrennt (Maßnahme D2)')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P('=' * 110)

def tab(titel, zp, filt):
    P(f'\n{titel}')
    P(f"{'Zielgröße':10s}{'n':>4s}{'n(k≥2)':>7s}{'df':>4s}{'M_best':>9s}{'S_b':>8s}{'TE':>8s}{'TE 95%-KI':>17s}{'Faktor':>7s}{'CV%':>6s}{'CVln%':>7s}{'SESOI':>8s}{'SESOI_T':>8s}{'TE/SESOI':>9s}{'TE/SES_T':>9s}{'MDC':>8s}{'TE/√n':>8s}{'TE/√n/SESOI':>12s}")
    res = {}
    for z in ZIEL:
        r = messguete(zp, z, filt); res[z] = r
        if r is None: P(f'{z:10s}   — (keine oder zu wenige Daten)'); continue
        dec = 0 if z == 'SBJ' else 3
        f = lambda x, d=dec: f'{x:.{d}f}' if x == x else 'nan'
        f4 = lambda x: f'{x:.4f}' if z != 'SBJ' else f'{x:.2f}'
        mb = f(r['Mb']) if z != 'SBJ' else '{:.1f}'.format(r['Mb'])
        ki = f4(r['te_lo']) + '–' + f4(r['te_hi'])
        P(f"{z:10s}{r['n']:4d}{r['n_k2']:7d}{r['df']:4d}{mb:>9s}{f4(r['Sb']):>8s}{f4(r['te']):>8s}{ki:>17s}{r['te_hi'] / r['te']:7.2f}{r['cv']:6.1f}{r['cv_ln']:7.1f}{f4(r['sesoi']):>8s}{f4(r['sesoi_t']):>8s}{r['te_sesoi']:9.2f}{r['te_sesoi_t']:9.2f}{f4(r['mdc']):>8s}{f4(r['te_sqrtn']):>8s}{r['te_sqrtn_sesoi']:12.2f}")
    return res
P('\nSpalten: n = Spieler mit Bestwert · n(k≥2) = Spieler, die zum TE beitragen · df = Σ(k−1) · Faktor = obere KI-Grenze / TE')
P('505M = Mittelwert beider Beinseiten (Ethikantrag): TE aus versuchsweise gepaarten Einzelversuchen (Messung am zusammengesetzten Wert); Abschnitt 11 vergleicht mit der Modellrechnung.')
prae_alle = tab('1  PRÄ, alle Spieler (N = 31) — Bezugsgröße für SESOI und Messqualitätstabelle 4.4', 'prä', lambda c: True)
prae_ig = tab('2  PRÄ, IG (n = 18)', 'prä', lambda c: info[c][0] == 'IG')
prae_kg = tab('3  PRÄ, KG (n = 13)', 'prä', lambda c: info[c][0] == 'KG')
post_ig = tab('4  POST, IG (16 Spieler mit Werten; KG-Post steht aus) — SESOI hier aus den Post-Bestwerten der IG, nur zur Einordnung', 'post', lambda c: info[c][0] == 'IG')
post_a = tab('5  POST, Verein A (n = 7)', 'post', lambda c: info[c][1] == 'A')
post_b = tab('6  POST, Verein B (n = 9)', 'post', lambda c: info[c][1] == 'B')

P('\n7  TE PRÄ GEGEN POST (IG) — Stabilität des Messfehlers zwischen den Sitzungen')
P(f"{'Zielgröße':10s}{'TE prä IG':>11s}{'TE post IG':>11s}{'Verh. post/prä':>15s}{'df prä':>7s}{'df post':>8s}{'F-Test p (Varianzen)':>22s}")
for z in ZIEL:
    a, b = prae_ig[z], post_ig[z]
    if a is None or b is None: P(f'{z:10s}   —'); continue
    F = (b['te'] ** 2) / (a['te'] ** 2); p = 2 * min(stats.f.cdf(F, b['df'], a['df']), stats.f.sf(F, b['df'], a['df']))
    P(f"{z:10s}{a['te']:11.4f}{b['te']:11.4f}{b['te'] / a['te']:15.2f}{a['df']:7d}{b['df']:8d}{p:22.3f}")
P('Lesart: Verhältnis nahe 1 = gleicher Innerhalb-Sitzung-Fehler an beiden Terminen. Der F-Test hat bei diesen df wenig Kraft.')

P('\n8  GEPOOLTER TE (prä alle + post IG) — größere df, als Berichtsgröße für 4.4 zu erwägen')
P(f"{'Zielgröße':10s}{'df':>5s}{'TE':>9s}{'95%-KI':>19s}{'CV%':>6s}{'MDC':>8s}{'TE/SESOI(prä)':>14s}")
for z in ZIEL:
    ss = 0.0; df = 0; alle = []
    for (c, zp, zz), a in agg.items():
        if zz != z or a['k'] < 2: continue
        if zp == 'post' and info[c][0] != 'IG': continue
        m = sum(a['werte']) / len(a['werte']); ss += sum((x - m) ** 2 for x in a['werte']); df += a['k'] - 1; alle += a['werte']
    te = math.sqrt(ss / df); lo = te * math.sqrt(df / stats.chi2.ppf(0.975, df)); hi = te * math.sqrt(df / stats.chi2.ppf(0.025, df))
    d4 = (lambda x: f'{x:.4f}') if z != 'SBJ' else (lambda x: f'{x:.2f}')
    P(f"{z:10s}{df:5d}{d4(te):>9s}{(d4(lo) + '–' + d4(hi)):>19s}{te / (sum(alle) / len(alle)) * 100:6.1f}{d4(te * 1.96 * math.sqrt(2)):>8s}{te / prae_alle[z]['sesoi']:14.2f}")

P('\n9  EINSTUFUNG (§ 11.3) — prä, alle Spieler')
for z in ZIEL:
    r = prae_alle[z]
    P(f"   {z:5s}: TE/SESOI = {r['te_sesoi']:.2f} → {'Einzelspielerebene NICHT auswertbar (TE > SESOI)' if r['te_sesoi'] > 1 else 'Einzelspielerebene auswertbar'};  TE/√n/SESOI = {r['te_sqrtn_sesoi']:.2f} → {'Gruppenmittel präziser als SESOI' if r['te_sqrtn_sesoi'] < 1 else 'Gruppenmittel NICHT präziser als SESOI'}")
P('   ⚠ TE/√n gegen SESOI ist Messpräzision des Gruppenmittels; die statistische Auflösung des Gruppenvergleichs (MDES) steht in B8/§ 11.1 und ist um ein Vielfaches gröber.')

P('\n10 ABGLEICH MIT BLATT 04_Kennwerte (Prä-Tabelle, § 3 Fassung 9) — nur Kontrolle')
try:
    ws = wb['04_Kennwerte']; rows = list(ws.iter_rows(values_only=True))
    for r in rows[:14]:
        if any(v is not None for v in r): P('   ' + ' | '.join('' if v is None else (f'{v:.4f}' if isinstance(v, float) else str(v)) for v in r[:10]))
except KeyError:
    P('   Blatt 04_Kennwerte nicht gefunden.')
P('   § 3 (F9): 5 m n 26, 1,08 ± 0,08, SESOI 0,016, TE 0,046, CV 4,3, TE/SESOI 2,92, TE/√n/SESOI 0,57 · 10 m n 31, TE 0,037, CV 1,9 · 30 m TE 0,077, CV 1,7 · SBJ TE 6,1, CV 2,7 · 505 L TE 0,089, CV 3,6 · 505 R TE 0,083, CV 3,3')
P('   neu (prä, alle): ' + ' · '.join(f"{z} n {prae_alle[z]['n']}, TE {prae_alle[z]['te']:.4f}, CV {prae_alle[z]['cv']:.1f}, SESOI {prae_alle[z]['sesoi']:.4f}, TE/SESOI {prae_alle[z]['te_sesoi']:.2f}" for z in ZIEL))
P('   § 11.3 Sensitivitätsangabe: 505 L SESOI_T 0,0143 (TE/SESOI_T 6,21), 505 R 0,0164 · neu: ' + ', '.join(f"{z} SESOI_T {prae_alle[z]['sesoi_t']:.4f} (TE/SESOI_T {prae_alle[z]['te_sesoi_t']:.2f})" for z in ('505L', '505R')))

P('\n11 505M — MODELLRECHNUNG GEGEN MESSUNG (§ 1.1: beides kennzeichnen, Messung geht vor)')
P('  Modell: TE_M = √(TE_L² + TE_R²) / 2 (unabhängige Seitenfehler). Messung: TE aus den gepaarten Einzelversuchen (Tabelle 1).')
for lab, res in (('prä alle', prae_alle), ('prä IG', prae_ig), ('prä KG', prae_kg), ('post IG', post_ig)):
    L, R, Mm = res.get('505L'), res.get('505R'), res.get('505M')
    if not (L and R and Mm): P(f'  {lab}: —'); continue
    te_mod = math.sqrt(L['te'] ** 2 + R['te'] ** 2) / 2
    P(f"  {lab:9s}: TE_L {L['te']:.4f} · TE_R {R['te']:.4f} → Modell TE_M {te_mod:.4f} · gemessen TE_M {Mm['te']:.4f} (df {Mm['df']}) · S_b(505M) {Mm['Sb']:.4f} · SESOI {Mm['sesoi']:.4f} · TE/SESOI {Mm['te_sesoi']:.2f} · TE/√n/SESOI {Mm['te_sqrtn_sesoi']:.2f}")
P('  Lesart: Der Mittelwert zweier Seiten hat einen kleineren Fehler als jede Seite allein, aber auch eine kleinere Zwischen-Spieler-SD; entscheidend ist TE/SESOI.')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

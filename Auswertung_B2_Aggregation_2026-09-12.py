# -*- coding: utf-8 -*-
"""
Auswertung_B2_Aggregation_2026-09-12.py — Phase B, Schritt B2: Aggregation der Versuche
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.

Einzige Datenquelle: Statistik\Studiendaten_U15_gesamt.xlsx, Blatt 02_Rohdaten (Gültigkeit nach B0.2).
03_Analyse wird NICHT übernommen, sondern am Ende zellgenau gegengeprüft.

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B2_Aggregation_2026-09-12.py [Pfad zum Workbook]
Ausgabe: gleichnamige .txt neben dem Skript.

Inhalt:
  1  Aggregationsregel (B0.3): Bestwert = Minimum (Zeiten) bzw. Maximum (Standweitsprung) der gültigen
     Versuche → Hauptanalyse; Mittelwert der gültigen Versuche → Sensitivitätsanalyse (§ 11.8)
  2  Je Spieler × Zielgröße × Zeitpunkt: k, Bestwert, Mittelwert, Einzelwerte
  3  Versuchszahl k: Verteilung und Mittel je Gruppe/Verein × Zeitpunkt × Zielgröße (Maßnahme D1)
  4  Bestwert-Bias an den eigenen Daten GEMESSEN (§ 11.8): Bestwert aus 3 gegen Bestwert aus den ersten 2,
     Bestwert aus 2 gegen Versuch 1; Gegenprobe: Mittelwert aus 3 gegen Mittelwert aus den ersten 2
  5  Zellgenauer Abgleich mit 03_Analyse (k_/Best_-Spalten) — Abweichungen werden gemeldet, nicht korrigiert
"""
import sys, os, io, math, datetime, statistics
from collections import Counter, defaultdict, OrderedDict
import openpyxl

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

# ---------------------------------------------------------------- Festlegungen (B0) — identisch mit B1
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
    """Liest 02_Rohdaten; gilt_neu nach B0.2 (Wert vorhanden UND 'ungültig' leer)."""
    wb = openpyxl.load_workbook(pfad, data_only=True, read_only=True)
    ws = wb['02_Rohdaten']; rows = list(ws.iter_rows(values_only=True))
    COL = {str(h): i for i, h in enumerate(rows[0])}
    out = []
    for r in rows[1:]:
        if r[COL['Code']] is None: continue
        d = {c: r[COL[c]] for c in ('Code', 'Verein', 'Zeitpunkt', 'Test', 'Seite', 'Versuch', 'Wert', 'ungültig', 'Bemerkung')}
        d['Wert'] = num(d['Wert'])
        d['ungültig'] = str(d['ungültig']).strip() if d['ungültig'] not in (None, '') else ''
        d['Bemerkung'] = str(d['Bemerkung']).strip() if d['Bemerkung'] not in (None, '') else ''
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
    """Je (Code, Zeitpunkt, Z): Liste gültiger Werte in Versuchsreihenfolge, k, Best, Mittel."""
    zellen = defaultdict(list)
    for d in sorted(data, key=lambda d: d['Versuch']):
        if d['gilt_neu'] == 1: zellen[(d['Code'], d['Zeitpunkt'], d['Z'])].append((d['Versuch'], d['Wert']))
    agg = {}
    for key, vs in zellen.items():
        w = [x for _, x in vs]; richtung = ZIEL[key[2]][3]
        agg[key] = dict(k=len(w), werte=vs, best=(min(w) if richtung == 'min' else max(w)), mittel=sum(w) / len(w))
    return agg

data, wb = lade_rohdaten(WB)
agg = ergaenze_505M(aggregiere(data), tupel=True)
codes = sorted(set(d['Code'] for d in data))
info = {c: next((d['Gruppe'], d['VereinK']) for d in data if d['Code'] == c) for c in codes}

P('=' * 100)
P('B2 AGGREGATION — Bestwert (Hauptanalyse) und Mittelwert (Sensitivitätsanalyse) je Spieler, Zielgröße, Zeitpunkt')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P('=' * 100)
P('\n1  AGGREGATIONSREGEL (B0.3, § 11.8)')
P('Bestwert = Minimum der gültigen Versuche bei Zeiten (5 m, 10 m, 30 m, 505 L/R), Maximum beim Standweitsprung → Hauptanalyse.')
P('505M (Ethikantrag § 3: „Mittelwert beider Beinseiten“) = (Best_L + Best_R)/2 bzw. (Mittel_L + Mittel_R)/2; nur wenn beide Seiten einen gültigen Wert haben.')
P('   k bei 505M = min(k_L, k_R) — Zahl der versuchsweise gepaarten Einzelversuche (nur für die Messgüte in B3 relevant).')
P('Mittelwert = arithmetisches Mittel der gültigen Versuche → Sensitivitätsanalyse. Beide werden berichtet, unabhängig vom Ausgang.')
P('Gültig ist ein Versuch nach B0.2 (Wert vorhanden, Spalte ungültig leer, Lauf nicht auslösegestört — B1 § 6: kein Lauf betroffen).')
P('Eine Zelle ohne gültigen Versuch hat keinen Wert (kein Ersatz, keine Fortschreibung, § 11.7).')

# ---------------------------------------------------------------- 2 Spielerwerte
P('\n2  WERTE JE SPIELER (k = Zahl gültiger Versuche; Einzelwerte in Versuchsreihenfolge mit Versuchsnummer)')
for zp in ('prä', 'post'):
    P(f'\n--- {zp} ---')
    P(f"{'Code':7s}{'Gr':3s}{'V':2s}" + ''.join(f'{z:>26s}' for z in ZIEL))
    for c in codes:
        g, v = info[c]
        line = f'{c:7s}{g:3s}{v:2s}'
        for z in ZIEL:
            a = agg.get((c, zp, z))
            if a is None: line += f"{'—':>26s}"; continue
            fmt = '{:.0f}' if z == 'SBJ' else '{:.2f}'
            ein = ' '.join(f'{vn}:' + fmt.format(w) for vn, w in a['werte'])
            line += f"{('k' + str(a['k']) + ' B=' + fmt.format(a['best']) + ' M=' + ('{:.1f}' if z == 'SBJ' else '{:.3f}').format(a['mittel'])):>26s}"
        P(line)
    P('Einzelwerte:')
    for c in codes:
        parts = []
        for z in ZIEL:
            a = agg.get((c, zp, z))
            if a: parts.append(z + ' [' + ', '.join(f"V{vn}={w:g}" for vn, w in a['werte']) + ']')
        if parts: P(f'   {c:7s} ' + ' · '.join(parts))

# ---------------------------------------------------------------- 3 Versuchszahl
P('\n3  VERSUCHSZAHL k (Maßnahme D1) — Verteilung je Gruppe × Zeitpunkt × Zielgröße')
P('Nenner: alle Spieler des Vereins/der Gruppe (auch k = 0). Protokollvorgabe: 3 Versuche je Spieler und Zielgröße.')
P(f"{'Zielgröße':10s}{'Gruppe':8s}{'Zeitp.':6s}{'k=0':>5s}{'k=1':>5s}{'k=2':>5s}{'k=3':>5s}{'n':>5s}{'k̄ (alle)':>10s}{'k̄ (k>0)':>10s}")
for z in ZIEL:
    for lab, filt in (('IG', lambda c: info[c][0] == 'IG'), ('  A', lambda c: info[c][1] == 'A'), ('  B', lambda c: info[c][1] == 'B'), ('KG', lambda c: info[c][0] == 'KG')):
        for zp in ('prä', 'post'):
            pl = [c for c in codes if filt(c)]
            ks = [agg[(c, zp, z)]['k'] if (c, zp, z) in agg else 0 for c in pl]
            cnt = Counter(ks); kpos = [k for k in ks if k > 0]
            P(f'{z:10s}{lab:8s}{zp:6s}{cnt[0]:5d}{cnt[1]:5d}{cnt[2]:5d}{cnt[3]:5d}{len(pl):5d}{sum(ks) / len(ks):10.2f}{(sum(kpos) / len(kpos) if kpos else float("nan")):10.2f}')
P('\nVersuchszahl-Differenz prä → post innerhalb der IG (k̄ post − k̄ prä, nur Spieler mit Werten an beiden Zeitpunkten):')
for z in ZIEL:
    for lab, filt in (('A', lambda c: info[c][1] == 'A'), ('B', lambda c: info[c][1] == 'B'), ('IG', lambda c: info[c][0] == 'IG')):
        pl = [c for c in codes if filt(c) and (c, 'prä', z) in agg and (c, 'post', z) in agg]
        if not pl: P(f'   {z:5s} {lab:3s}: keine gepaarten Spieler'); continue
        dk = [agg[(c, 'post', z)]['k'] - agg[(c, 'prä', z)]['k'] for c in pl]
        P(f'   {z:5s} {lab:3s}: n = {len(pl):2d}  k̄ prä {sum(agg[(c, "prä", z)]["k"] for c in pl) / len(pl):.2f}  k̄ post {sum(agg[(c, "post", z)]["k"] for c in pl) / len(pl):.2f}  Δk̄ = {sum(dk) / len(dk):+.2f}')

# ---------------------------------------------------------------- 4 Bestwert-Bias gemessen
P('\n4  BESTWERT-BIAS, AN DEN EIGENEN DATEN GEMESSEN (§ 11.8) — Messung, keine Modellrechnung')
P('Spieler mit k = 3: Bestwert aus 3 minus Bestwert aus den ersten 2 (Versuchsreihenfolge).')
P('Spieler mit k ≥ 2: Bestwert aus den ersten 2 minus Versuch 1.  Gegenprobe: Mittelwert aus 3 minus Mittelwert aus den ersten 2.')
P('Vorzeichen: bei Zeiten ist ein negativer Wert eine Verbesserung des Bestwerts, beim Standweitsprung ein positiver.')
P('Zusätzlich in Einheiten der Zwischen-Spieler-SD der Prä-Bestwerte (SD_b) und des SESOI = 0,2 · SD_b (§ 11.3).')
sd_b = {}
for z in [z for z in ZIEL if z != '505M']:
    vals = [agg[(c, 'prä', z)]['best'] for c in codes if (c, 'prä', z) in agg]
    sd_b[z] = statistics.stdev(vals)
def bias_tab(zp_filter, titel):
    P(f'\n{titel}')
    P(f"{'Zielgröße':10s}{'n(k=3)':>7s}{'B3−B2':>10s}{'SD':>8s}{'in SD_b':>9s}{'in SESOI':>9s}{'n(k≥2)':>8s}{'B2−V1':>10s}{'in SESOI':>9s}{'n(k=3)':>7s}{'M3−M2':>10s}{'in SESOI':>9s}")
    for z in [z for z in ZIEL if z != '505M']:
        richtung = ZIEL[z][3]; f = (lambda w: min(w)) if richtung == 'min' else (lambda w: max(w))
        d32, d21, m32 = [], [], []
        for c in codes:
            for zp in ('prä', 'post'):
                if not zp_filter(zp): continue
                a = agg.get((c, zp, z))
                if a is None: continue
                w = [x for _, x in a['werte']]
                if a['k'] >= 2: d21.append(f(w[:2]) - w[0])
                if a['k'] == 3:
                    d32.append(f(w) - f(w[:2])); m32.append(sum(w) / 3 - sum(w[:2]) / 2)
        ses = 0.2 * sd_b[z]
        def m(x): return sum(x) / len(x) if x else float('nan')
        def sd(x): return statistics.stdev(x) if len(x) > 1 else float('nan')
        P(f'{z:10s}{len(d32):7d}{m(d32):10.4f}{sd(d32):8.4f}{m(d32) / sd_b[z]:9.3f}{m(d32) / ses:9.2f}{len(d21):8d}{m(d21):10.4f}{m(d21) / ses:9.2f}{len(m32):7d}{m(m32):10.4f}{m(m32) / ses:9.2f}')
bias_tab(lambda zp: zp == 'prä', 'Prä (alle 31 Spieler) — Vergleich § 11.8: 10 m −0,0050 s (n = 10) · 30 m −0,0159 s (n = 17) · SBJ +0,75 cm (n = 12)')
bias_tab(lambda zp: zp == 'post', 'Post (IG, 16 Spieler mit Werten)')
bias_tab(lambda zp: True, 'Prä + Post gepoolt')
P('\nLesehilfe: B3−B2 ist der gemessene Zugewinn des Bestwerts durch den dritten Versuch. Ein Betrag nahe 0,25 SESOI bestätigt § 11.8.')
P('M3−M2 prüft die Annahme, dass der Erwartungswert des Mittelwerts nicht von k abhängt: Werte nahe 0 stützen sie;')
P('ein systematischer Wert würde einen Reihenfolge-/Lerneffekt über die Versuche anzeigen, der auch den Mittelwert träfe.')

# ---------------------------------------------------------------- 5 Abgleich 03_Analyse
P('\n5  ZELLGENAUER ABGLEICH MIT BLATT 03_Analyse (nur Kontrolle, keine Übernahme)')
ws = wb['03_Analyse']; rows = list(ws.iter_rows(values_only=True))
hdr = [str(h) if h is not None else '' for h in rows[0]]
P('Spaltenkopf 03_Analyse:', [h for h in hdr if h][:40])
# Spalten k_/Best_ je Zielgröße und Zeitpunkt suchen (Namensmuster aus dem Blatt)
MAP = {'5m': '5m', '10m': '10m', '30m': '30m', 'SBJ': 'SWS', '505L': '505_L', '505R': '505_R'}
abw = 0; gepr = 0
ci = hdr.index('Code')
for r in rows[1:]:
    c = r[ci]
    if c not in info: continue
    for z, name in MAP.items():
        for zp, suf in (('prä', 'prae'), ('post', 'post')):
            for typ in ('k', 'Best'):
                col = f'{typ}_{name}_{suf}'
                if col not in hdr:
                    cand = [h for h in hdr if h.lower().startswith(typ.lower() + '_') and name.lower() in h.lower() and suf in h.lower()]
                    if not cand: continue
                    col = cand[0]
                blatt = num(r[hdr.index(col)])
                a = agg.get((c, zp, z))
                neu = (a['k'] if a else 0) if typ == 'k' else (a['best'] if a else None)
                gepr += 1
                if typ == 'k':
                    if (blatt or 0) != neu: abw += 1; P(f'   ABWEICHUNG {c} {col}: Blatt {blatt} · neu {neu}')
                else:
                    if (blatt is None) != (neu is None) or (blatt is not None and abs(blatt - neu) > 1e-9): abw += 1; P(f'   ABWEICHUNG {c} {col}: Blatt {blatt} · neu {neu}')
P(f'Geprüfte Zellen: {gepr} · Abweichungen: {abw}' + ('  → 03_Analyse stimmt mit der Neuberechnung überein' if abw == 0 and gepr > 0 else ''))

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

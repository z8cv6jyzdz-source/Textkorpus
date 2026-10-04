# -*- coding: utf-8 -*-
"""
Auswertung_B1_Rohdaten_2026-09-12.py — Phase B, Schritt B1: Rohdatenschicht
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2): Vokabular um den Tippfehler „Fehversuch“ (Nachtrag des Verfassers vom 12.09.) ergänzt; sonst unverändert.

Einzige Datenquelle: Statistik\Studiendaten_U15_gesamt.xlsx, Blatt 02_Rohdaten.
Nichts wird aus 03_Analyse, 04_Kennwerte oder Notizen übernommen.

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):
    python Auswertung_B1_Rohdaten_2026-09-12.py [Pfad zum Workbook]
Ausgabe: gleichnamige .txt neben dem Skript.

Inhalt:
  1  Struktur- und Vollständigkeitsprüfung der 1.116 Zeilen
  2  Gültigkeitsflag nachrechnen (B0.2: gilt = Wert vorhanden UND kein Eintrag in 'ungültig')
  3  Bemerkungsvokabular → vier Ausfallkategorien (B0.4), Originalwortlaut erhalten
  4  Ausfälle je Kategorie × Zeitpunkt × Gruppe × Zielgröße; je Spieler
  5  Leistungsunabhängigkeit der technischen Ausfälle (roh und innerhalb der Gruppen)
  6  Plausibilität der Sprintläufe: Abschnittsgeschwindigkeiten (Regel für auslösegestörte Läufe, B0.2)
  7  Abgleich mit früheren Angaben (§ 3.1 Fassung 9; Datendurchsicht 10./11.09.)
"""
import sys, os, io, math, datetime
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

# ---------------------------------------------------------------- Festlegungen (B0)
ZIEL = OrderedDict([  # feste Reihenfolge § 2: Sprint → 505 → Sprung; intern 505 nach Sprint, SBJ zuletzt
    ('5m',   ('Sprint_5m', '–', 's', 'min')),
    ('10m',  ('Sprint_10m', '–', 's', 'min')),
    ('30m',  ('Sprint_30m', '–', 's', 'min')),
    ('505L', ('COD_505', 'L', 's', 'min')),
    ('505R', ('COD_505', 'R', 's', 'min')),
    ('SBJ',  ('Standweitsprung', '–', 'cm', 'max')),
])
GRUPPE = {'Hohenlind': 'IG', 'Blau-Weiß Köln': 'IG', 'Vorwärts Spoho': 'KG'}
VEREIN_KURZ = {'Hohenlind': 'A', 'Blau-Weiß Köln': 'B', 'Vorwärts Spoho': 'C'}

# B0.4 — verbindliches Vokabular. Schlüssel = Originalwortlaut (exakt, nach strip), Wert = Kategorie.
VOKABULAR = {
    'System nicht aufgenommen':       'technisch',
    'Sytem nicht aufgenommen':        'technisch',            # Tippfehler im Post-Block, 2 Zeilen
    'Nur 2 Versuche aus Zeitmangel':  'Zeitmangel',
    'Linie nicht getroffen':          'Fehlversuch',          # 505, Prä-Vokabular
    'Kein fester Stand':              'Fehlversuch',          # Standweitsprung, Prä-Vokabular
    'Fehlversuch':                    'Fehlversuch',          # Post-Vokabular für beides
    'Fehversuch':                     'Fehlversuch',          # Tippfehler, 1 Zeile (Nachtrag 12.09.)
    'System falsch aufgenommen':      'System falsch aufgenommen',
}
KATEGORIEN = ['technisch', 'Zeitmangel', 'Fehlversuch', 'System falsch aufgenommen', 'ohne Bemerkung', 'unbekannter Wortlaut']

# B0.2 — Regel für auslösegestörte Läufe (Sprint): eine Abschnittsgeschwindigkeit über V_MAX m/s
# oder eine nicht positive Abschnittszeit ist physiologisch unmöglich → alle Teilzeiten des Laufs ungültig.
V_MAX = 10.0   # m/s; Erwachsenen-Weltklasse erreicht ~12,4 m/s nur in der Höchstgeschwindigkeitsphase,
               # U15 in keinem Abschnitt über 10 m/s. Konservativ: markiert nur physikalisch Unmögliches.

def num(v):
    if v is None or v == '': return None
    if isinstance(v, (int, float)): return float(v)
    try: return float(str(v).replace(',', '.'))
    except ValueError: return None

# ---------------------------------------------------------------- Einlesen
wb = openpyxl.load_workbook(WB, data_only=True, read_only=True)
ws = wb['02_Rohdaten']
rows = list(ws.iter_rows(values_only=True))
header = [str(h) for h in rows[0]]
COL = {h: i for i, h in enumerate(header)}
need = ['Code', 'Verein', 'Zeitpunkt', 'Test', 'Seite', 'Versuch', 'Wert', 'Einheit', 'ungültig', 'Bemerkung', 'gilt']
assert all(c in COL for c in need), header
data = []
for r in rows[1:]:
    if r[COL['Code']] is None: continue
    d = {c: r[COL[c]] for c in need}
    d['Wert'] = num(d['Wert'])
    d['Bemerkung'] = (str(d['Bemerkung']).strip() if d['Bemerkung'] not in (None, '') else '')
    d['ungültig'] = (str(d['ungültig']).strip() if d['ungültig'] not in (None, '') else '')
    d['Gruppe'] = GRUPPE[d['Verein']]
    d['VereinK'] = VEREIN_KURZ[d['Verein']]
    zk = [k for k, (t, s, u, m) in ZIEL.items() if t == d['Test'] and s == d['Seite']]
    assert len(zk) == 1, (d['Test'], d['Seite'])
    d['Z'] = zk[0]
    data.append(d)

P('=' * 100)
P('B1 ROHDATENSCHICHT — Studiendaten_U15_gesamt.xlsx, Blatt 02_Rohdaten')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
P('Workbook:', os.path.abspath(WB), '· zuletzt geändert:', datetime.datetime.fromtimestamp(os.path.getmtime(WB)).strftime('%Y-%m-%d %H:%M'))
P('=' * 100)

# ---------------------------------------------------------------- 1 Struktur
P('\n1  STRUKTUR UND VOLLSTÄNDIGKEIT')
codes = sorted(set(d['Code'] for d in data))
P('Zeilen:', len(data), '· Spieler (Codes):', len(codes))
P('Codes:', ', '.join(codes))
by_ver = Counter((d['VereinK'], d['Gruppe']) for d in data if d['Zeitpunkt'] == 'prä' and d['Z'] == '5m' and d['Versuch'] == 1)
P('Spieler je Verein (aus Zeilenstruktur):', ', '.join(f'{v} ({g}) n = {n}' for (v, g), n in sorted(by_ver.items())))
keys = Counter((d['Code'], d['Zeitpunkt'], d['Z'], d['Versuch']) for d in data)
dup = [k for k, n in keys.items() if n > 1]
P('Doppelte Schlüssel (Code, Zeitpunkt, Zielgröße, Versuch):', len(dup), dup[:5])
erwartet = len(codes) * len(ZIEL) * 3 * 2
P(f'Erwartete Zeilen {len(codes)} Spieler × {len(ZIEL)} Zielgrößen × 3 Versuche × 2 Zeitpunkte = {erwartet} →', 'stimmt' if erwartet == len(data) else 'ABWEICHUNG')
P('Versuchsnummern:', dict(Counter(d['Versuch'] for d in data)))
P('Einheiten je Test:', dict(Counter((d['Test'], d['Einheit']) for d in data)))

# ---------------------------------------------------------------- 2 Gültigkeitsflag
P('\n2  GÜLTIGKEITSFLAG NACHGERECHNET (B0.2)')
P("Regel: gilt_neu = 1, wenn ein Wert eingetragen ist UND die Spalte 'ungültig' leer ist; sonst 0.")
diff = 0
for d in data:
    d['gilt_neu'] = 1 if (d['Wert'] is not None and d['ungültig'] == '') else 0
    g_alt = int(d['gilt']) if d['gilt'] not in (None, '') else 0
    d['gilt_alt'] = g_alt
    if g_alt != d['gilt_neu']:
        diff += 1; P('  ABWEICHUNG Blattwert gilt:', d['Code'], d['Zeitpunkt'], d['Z'], d['Versuch'], 'Blatt', g_alt, 'neu', d['gilt_neu'])
P('Abweichungen zwischen Blattspalte gilt und Nachrechnung:', diff)
mitwert_ung = [d for d in data if d['Wert'] is not None and d['ungültig'] != '']
P(f"Zeilen mit Wert, aber Eintrag in 'ungültig' (Wert wird verworfen): {len(mitwert_ung)}")
for d in mitwert_ung:
    P(f"   {d['Code']:6s} {d['Zeitpunkt']:4s} {d['Z']:5s} V{d['Versuch']}  Wert {d['Wert']}  Bemerkung: {d['Bemerkung'] or '(leer)'}")
for zp in ('prä', 'post'):
    for g in ('IG', 'KG'):
        n1 = sum(1 for d in data if d['Zeitpunkt'] == zp and d['Gruppe'] == g and d['gilt_neu'] == 1)
        n0 = sum(1 for d in data if d['Zeitpunkt'] == zp and d['Gruppe'] == g and d['gilt_neu'] == 0)
        P(f'  {zp:4s} {g}: gültig {n1:4d} · nicht gültig {n0:4d} · Zeilen {n1 + n0}')
P('  gesamt gültig:', sum(d['gilt_neu'] for d in data), '· nicht gültig:', sum(1 for d in data if d['gilt_neu'] == 0))

# ---------------------------------------------------------------- 3 Vokabular
P('\n3  BEMERKUNGSVOKABULAR → KATEGORIE (B0.4) — Originalwortlaut bleibt in der Spalte Bemerkung erhalten')
def kat(d):
    if d['gilt_neu'] == 1: return None
    b = d['Bemerkung']
    if b == '': return 'ohne Bemerkung'
    return VOKABULAR.get(b, 'unbekannter Wortlaut')
for d in data: d['Kat'] = kat(d)
P(f"{'Originalwortlaut':34s} {'Kategorie':26s} {'prä':>5s} {'post':>5s}")
wl = Counter((d['Bemerkung'], d['Zeitpunkt']) for d in data if d['gilt_neu'] == 0)
for w in sorted(set(k[0] for k in wl), key=lambda x: (VOKABULAR.get(x, 'zz'), x)):
    P(f"{(w or '(leer)'):34s} {VOKABULAR.get(w, 'ohne Bemerkung' if w == '' else 'unbekannter Wortlaut'):26s} {wl[(w, 'prä')]:5d} {wl[(w, 'post')]:5d}")
unk = [d for d in data if d['Kat'] == 'unbekannter Wortlaut']
P('Unbekannte Wortlaute (nicht im Vokabular):', len(unk))
bem_gueltig = [d for d in data if d['gilt_neu'] == 1 and d['Bemerkung']]
P('Gültige Versuche mit Bemerkung (informativ):', len(bem_gueltig))
for d in bem_gueltig: P(f"   {d['Code']:6s} {d['Zeitpunkt']:4s} {d['Z']:5s} V{d['Versuch']} Wert {d['Wert']}  '{d['Bemerkung']}'")

# ---------------------------------------------------------------- 4 Ausfälle
P('\n4  NICHT GÜLTIGE VERSUCHE JE KATEGORIE')
def tab_kat(filt, titel):
    P(f'\n{titel}')
    P(f"{'Kategorie':28s}" + ''.join(f'{z:>7s}' for z in ZIEL) + f"{'Summe':>8s}")
    tot = Counter()
    for k in KATEGORIEN:
        c = Counter(d['Z'] for d in data if filt(d) and d['Kat'] == k)
        if sum(c.values()) == 0: continue
        tot.update(c)
        P(f'{k:28s}' + ''.join(f'{c[z]:7d}' for z in ZIEL) + f'{sum(c.values()):8d}')
    P(f"{'Summe':28s}" + ''.join(f'{tot[z]:7d}' for z in ZIEL) + f'{sum(tot.values()):8d}')
tab_kat(lambda d: d['Zeitpunkt'] == 'prä', 'Prä, alle Spieler (N = 31)')
tab_kat(lambda d: d['Zeitpunkt'] == 'prä' and d['Gruppe'] == 'IG', 'Prä, IG (Verein A + B)')
tab_kat(lambda d: d['Zeitpunkt'] == 'prä' and d['Gruppe'] == 'KG', 'Prä, KG (Verein C)')
tab_kat(lambda d: d['Zeitpunkt'] == 'post' and d['Gruppe'] == 'IG', 'Post, IG (Verein A + B) — KG-Post steht aus')
tab_kat(lambda d: d['Zeitpunkt'] == 'post' and d['VereinK'] == 'A', 'Post, Verein A')
tab_kat(lambda d: d['Zeitpunkt'] == 'post' and d['VereinK'] == 'B', 'Post, Verein B')
tab_kat(lambda d: d['Zeitpunkt'] == 'post' and d['Gruppe'] == 'KG', 'Post, KG (Verein C) — Erwartung: 558/2 = 279 Zeilen leer')

P('\nSpieler ohne einen einzigen gültigen Post-Versuch (Teilnehmerebene, nicht Versuchsebene):')
ohne_post = sorted(c for c in codes if not any(d['gilt_neu'] == 1 for d in data if d['Code'] == c and d['Zeitpunkt'] == 'post'))
P('   ' + ', '.join(ohne_post))
P('   → BW-07, BW-21: zur Post-Testung nicht angetreten (Angabe Verfasser, Datendurchsicht § 1); VS-xx: KG-Post steht aus (15.09.).')
P('   Diese Zeilen sind keine undokumentierten Versuchslücken; sie gehören in den Teilnehmerfluss (B4).')
P('\nUndokumentierte Lücken auf Versuchsebene (nicht gültig, ohne Bemerkung, Spieler mit Post-Werten) — CONSORT Item 13a/16 brauchen einen Grund:')
for d in data:
    if d['Kat'] == 'ohne Bemerkung' and d['Code'] not in ohne_post:
        P(f"   {d['Code']:6s} {d['Zeitpunkt']:4s} {d['Z']:5s} V{d['Versuch']}  ungültig='{d['ungültig']}' Wert={d['Wert']}")
P('   Erwartung aus Datendurchsicht § 4.2 (post): BW-05 505R V2 · BW-09 505L V1 · BW-11 SBJ V2 · HL-02 SBJ V1; prä (§ 3.1): 3 ohne Bemerkung.')

P('\nTechnische Ausfälle je Spieler und Sprintstrecke (prä), Mittel je Gruppe — Vergleich mit § 3.1:')
for z in ('5m', '10m', '30m'):
    for g in ('IG', 'KG'):
        pl = sorted(set(d['Code'] for d in data if d['Gruppe'] == g))
        cnt = [sum(1 for d in data if d['Code'] == c and d['Zeitpunkt'] == 'prä' and d['Z'] == z and d['Kat'] == 'technisch') for c in pl]
        P(f'   {z:4s} {g}: {sum(cnt) / len(cnt):.2f} je Spieler (n = {len(cnt)}, Summe {sum(cnt)})')

P('\nMittlere Zahl gültiger Versuche je Spieler (k̄), Zielgröße × Zeitpunkt × Verein:')
P(f"{'Zielgröße':10s}" + ''.join(f'{c:>9s}' for c in ('A prä', 'A post', 'B prä', 'B post', 'C prä', 'C post')))
for z in ZIEL:
    line = f'{z:10s}'
    for v in ('A', 'B', 'C'):
        for zp in ('prä', 'post'):
            pl = sorted(set(d['Code'] for d in data if d['VereinK'] == v))
            ks = [sum(1 for d in data if d['Code'] == c and d['Zeitpunkt'] == zp and d['Z'] == z and d['gilt_neu'] == 1) for c in pl]
            line += f'{sum(ks) / len(ks):9.2f}'
    P(line)

# ---------------------------------------------------------------- 5 Leistungsunabhängigkeit
P('\n5  LEISTUNGSUNABHÄNGIGKEIT DER TECHNISCHEN AUSFÄLLE (prä)')
P('Je Spieler: Zahl technischer Ausfälle (Kategorie technisch) gegen Bestwert prä derselben Strecke.')
P('Pearson r roh (alle Spieler) und innerhalb der Gruppen; p zweiseitig (t-Verteilung). n = Spieler mit Bestwert.')
def pearson(x, y):
    n = len(x)
    if n < 3: return float('nan'), float('nan'), n
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0: return float('nan'), float('nan'), n
    r = sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sxx * syy)
    r = max(-0.999999, min(0.999999, r))
    t = r * math.sqrt((n - 2) / (1 - r * r))
    try:
        from scipy import stats
        p = 2 * stats.t.sf(abs(t), n - 2)
    except ImportError:
        p = float('nan')
    return r, p, n
def best(code, zp, z):
    v = [d['Wert'] for d in data if d['Code'] == code and d['Zeitpunkt'] == zp and d['Z'] == z and d['gilt_neu'] == 1]
    if not v: return None
    return min(v) if ZIEL[z][3] == 'min' else max(v)
for z in ('5m', '10m', '30m'):
    P(f'  {z}:')
    for label, filt in (('roh, alle', lambda d: True), ('innerhalb IG', lambda d: d['Gruppe'] == 'IG'), ('innerhalb KG', lambda d: d['Gruppe'] == 'KG'),
                        ('innerhalb A', lambda d: d['VereinK'] == 'A'), ('innerhalb B', lambda d: d['VereinK'] == 'B'), ('innerhalb C', lambda d: d['VereinK'] == 'C')):
        pl = sorted(set(d['Code'] for d in data if filt(d)))
        xs, ys = [], []
        for c in pl:
            b = best(c, 'prä', z)
            if b is None: continue
            xs.append(sum(1 for d in data if d['Code'] == c and d['Zeitpunkt'] == 'prä' and d['Z'] == z and d['Kat'] == 'technisch')); ys.append(b)
        r, p, n = pearson(xs, ys)
        P(f'     {label:14s} r = {r:+.3f}  p = {p:.3f}  n = {n}   (Ausfälle: {dict(sorted(Counter(xs).items()))})')
    # gruppenzentrierte (gepoolte Innerhalb-Gruppen-)Korrelation — das ist die Größe, die § 3.1 als
    # „innerhalb der Gruppen (−0,017 / −0,152 / +0,032)" führt
    pl = sorted(codes); xs, ys, gs = [], [], []
    for c in pl:
        b = best(c, 'prä', z)
        if b is None: continue
        xs.append(sum(1 for d in data if d['Code'] == c and d['Zeitpunkt'] == 'prä' and d['Z'] == z and d['Kat'] == 'technisch')); ys.append(b)
        gs.append(next(d['Gruppe'] for d in data if d['Code'] == c))
    xc, yc = [], []
    for g in ('IG', 'KG'):
        ix_ = [i for i, gg in enumerate(gs) if gg == g]
        mx = sum(xs[i] for i in ix_) / len(ix_); my = sum(ys[i] for i in ix_) / len(ix_)
        xc += [xs[i] - mx for i in ix_]; yc += [ys[i] - my for i in ix_]
    r, p, n = pearson(xc, yc)
    P(f'     {"gruppenzentriert":14s} r = {r:+.3f}  (gepoolt innerhalb IG/KG, n = {n}; p nicht ausgewiesen, df durch Zentrierung reduziert)')

# ---------------------------------------------------------------- 6 Plausibilität Sprintläufe
P('\n6  PLAUSIBILITÄT DER SPRINTLÄUFE — REGEL FÜR AUSLÖSEGESTÖRTE LÄUFE (B0.2)')
P(f'Ein Lauf (Code, Zeitpunkt, Versuch) ist auslösegestört, wenn eine Abschnittsgeschwindigkeit > {V_MAX} m/s')
P('oder eine Abschnittszeit ≤ 0 s ist. Folge: ALLE Teilzeiten des Laufs (5, 10, 30 m) werden verworfen.')
P('Geprüft werden alle Läufe mit mindestens zwei gültigen Teilzeiten; Läufe mit nur einer Teilzeit sind nicht prüfbar.')
laufe = defaultdict(dict)
for d in data:
    if d['Z'] in ('5m', '10m', '30m') and d['gilt_neu'] == 1:
        laufe[(d['Code'], d['Zeitpunkt'], d['Versuch'])][d['Z']] = d['Wert']
gestoert = []; npruef = 0; seg_stats = defaultdict(list)
for (c, zp, v), t in sorted(laufe.items()):
    segs = []
    if '5m' in t: segs.append(('0–5 m', 5.0, t['5m']))
    if '5m' in t and '10m' in t: segs.append(('5–10 m', 5.0, t['10m'] - t['5m']))
    elif '10m' in t: segs.append(('0–10 m', 10.0, t['10m']))
    if '10m' in t and '30m' in t: segs.append(('10–30 m', 20.0, t['30m'] - t['10m']))
    elif '5m' in t and '30m' in t: segs.append(('5–30 m', 25.0, t['30m'] - t['5m']))
    elif '30m' in t: segs.append(('0–30 m', 30.0, t['30m']))
    if len(t) >= 2: npruef += 1
    bad = []
    for name, dist, dt in segs:
        vel = dist / dt if dt > 0 else float('inf')
        seg_stats[name].append(vel)
        if dt <= 0 or vel > V_MAX: bad.append((name, dt, vel))
    if bad: gestoert.append((c, zp, v, t, bad))
P(f'Geprüfte Läufe (≥ 2 Teilzeiten): {npruef} · auslösegestört nach Regel: {len(gestoert)}')
for c, zp, v, t, bad in gestoert:
    P(f"   {c:6s} {zp:4s} V{v}: " + ', '.join(f'{k} {t[k]:.2f}' for k in ('5m', '10m', '30m') if k in t) + ' → ' + '; '.join(f'{n} {dt:.2f} s = {vel:.1f} m/s' for n, dt, vel in bad))
P('Verteilung der Abschnittsgeschwindigkeiten (m/s), alle gültigen Läufe prä + post:')
for name, vs in seg_stats.items():
    vs = sorted(vs)
    P(f'   {name:8s} n = {len(vs):3d}  min {vs[0]:5.2f}  Median {vs[len(vs) // 2]:5.2f}  max {vs[-1]:5.2f}')
P('Langsamste und schnellste Einzelwerte je Strecke (Sichtkontrolle der Ränder):')
for z in ('5m', '10m', '30m'):
    vals = sorted(((d['Wert'], d['Code'], d['Zeitpunkt'], d['Versuch']) for d in data if d['Z'] == z and d['gilt_neu'] == 1))
    P(f"   {z:4s} schnellste: " + ', '.join(f'{w:.2f} ({c} {zp} V{v})' for w, c, zp, v in vals[:3]) + '  · langsamste: ' + ', '.join(f'{w:.2f} ({c} {zp} V{v})' for w, c, zp, v in vals[-3:]))
P('\nHL-08 post, Versuch 2 (Fall aus Datendurchsicht § 4.1): aktuelle Blattwerte')
for d in data:
    if d['Code'] == 'HL-08' and d['Zeitpunkt'] == 'post' and d['Z'] in ('5m', '10m', '30m'):
        P(f"   {d['Z']:4s} V{d['Versuch']} Wert={d['Wert']} ungültig='{d['ungültig']}' Bemerkung='{d['Bemerkung']}'")
t = laufe.get(('HL-08', 'post', 2), {})
if '5m' in t and '10m' in t:
    P(f"   Abschnitt 5–10 m mit Blattwert 10 m = {t['10m']:.2f}: {t['10m'] - t['5m']:.2f} s = {5 / (t['10m'] - t['5m']):.1f} m/s → " + ('unmöglich' if 5 / (t['10m'] - t['5m']) > V_MAX else 'nach Regel zulässig'))
    P(f"   Zum Vergleich mit dem in der Datendurchsicht genannten Erstwert 1,55 s: {1.55 - t['5m']:.2f} s = {5 / (1.55 - t['5m']):.1f} m/s → unmöglich")
    P("   ⚠ Der Blattwert 1,95 trägt keine Bemerkung. Ob er der Bogenwert (Abtippfehler 1,55 ↔ 1,95) oder ein gesetzter Wert ist,")
    P("     steht nicht im Workbook. Bogenwert → Bemerkung 'nach Bogenprüfung korrigiert, ursprünglich 1,55'; gesetzter Wert → Lauf ungültig (B0.2).")

# ---------------------------------------------------------------- 7 Abgleich
P('\n7  ABGLEICH MIT FRÜHEREN ANGABEN')
prae_ng = Counter(d['Kat'] for d in data if d['Zeitpunkt'] == 'prä' and d['gilt_neu'] == 0)
prae_wl = Counter(d['Bemerkung'] for d in data if d['Zeitpunkt'] == 'prä' and d['gilt_neu'] == 0)
P('§ 3.1 (Fassung 9): 174 nicht gültige Prä-Versuche = 94 System nicht aufgenommen + 61 Zeitmangel + 12 Linie nicht getroffen + 4 (Kein fester Stand / Fehlversuch) + 3 ohne Bemerkung')
P(f"   neu gerechnet: {sum(prae_ng.values())} = {prae_wl['System nicht aufgenommen']} + {prae_wl['Nur 2 Versuche aus Zeitmangel']} + {prae_wl['Linie nicht getroffen']} + {prae_wl['Kein fester Stand'] + prae_wl['Fehlversuch']} + {prae_wl['']}"
  + ('   → stimmt' if (sum(prae_ng.values()), prae_wl['System nicht aufgenommen'], prae_wl['Nur 2 Versuche aus Zeitmangel'], prae_wl['Linie nicht getroffen'], prae_wl['Kein fester Stand'] + prae_wl['Fehlversuch'], prae_wl['']) == (174, 94, 61, 12, 4, 3) else '   → ABWEICHUNG'))
post_wl = Counter(d['Bemerkung'] for d in data if d['Zeitpunkt'] == 'post' and d['Gruppe'] == 'IG' and d['gilt_neu'] == 0)
P('Datendurchsicht 10./11.09. (Post, IG): 51 Zeitmangel · 27 System falsch aufgenommen · 16 Fehlversuch · 3 + 2 System/Sytem nicht aufgenommen · 4 ohne Bemerkung')
P(f"   neu gerechnet: {post_wl['Nur 2 Versuche aus Zeitmangel']} · {post_wl['System falsch aufgenommen']} · {post_wl['Fehlversuch']} · {post_wl['System nicht aufgenommen']} + {post_wl['Sytem nicht aufgenommen']} · {post_wl['']}   (Summe nicht gültig IG post: {sum(post_wl.values())}; davon BW-07/BW-21 nicht angetreten: {sum(1 for d in data if d['Zeitpunkt'] == 'post' and d['Code'] in ('BW-07', 'BW-21') and d['gilt_neu'] == 0)})")
P('   Bemerkungen der nicht angetretenen Spieler BW-07 / BW-21 (post):', dict(Counter(d['Bemerkung'] for d in data if d['Zeitpunkt'] == 'post' and d['Code'] in ('BW-07', 'BW-21'))))
P('Datendurchsicht Tab. 1 — Spieler mit ≥ 1 gültigem Versuch je Verein × Zeitpunkt × Zielgröße:')
P(f"{'Verein':8s}{'Zeitp.':7s}" + ''.join(f'{z:>7s}' for z in ZIEL))
for v in ('A', 'B', 'C'):
    for zp in ('prä', 'post'):
        line = f'{v:8s}{zp:7s}'
        for z in ZIEL:
            line += f"{len(set(d['Code'] for d in data if d['VereinK'] == v and d['Zeitpunkt'] == zp and d['Z'] == z and d['gilt_neu'] == 1)):7d}"
        P(line)
P('   Erwartung aus Datendurchsicht: A prä 7/7/7/6/7/7 (5m,10m,30m,505L,505R,SBJ), A post 7/7/7/7/7/7, B prä 11/11/11/11/10/11, B post 9/0/9/9/8/9, C prä 8/13/13/12/12/13')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

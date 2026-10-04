# -*- coding: utf-8 -*-
"""
Auswertung_B4_Analysepopulation_2026-09-12.py — Phase B, Schritt B4: Analysepopulation, Nenner, Teilnehmerfluss
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2 der Kette vom 11.09.): 505 als MITTELWERT BEIDER BEINSEITEN (Ethikantrag § 3) = Zielgröße 505M ergänzt; 505 L/R nur noch deskriptiv. Übrige Rechenschritte unverändert.

Datenquelle: Statistik\Studiendaten_U15_gesamt.xlsx — 02_Rohdaten (Gültigkeit nach B0.2) und 01_Personen
(Gruppe, %PAH, Familiarisierung, Status). Nichts aus 03_Analyse/06_Überlappung übernommen.

Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B4_Analysepopulation_2026-09-12.py [Pfad zum Workbook]
Ausgabe: gleichnamige .txt neben dem Skript.

Inhalt:
  1  Teilnehmerfluss auf Teilnehmerebene (zugeteilt / prä getestet / post getestet / nicht angetreten / ausstehend)
  2  Kovariate %PAH: Verfügbarkeit, Ausfallgründe
  3  Nenner je Gruppe und Zielgröße (CONSORT Item 16): prä · post · prä+post · prä+post+%PAH (= ANCOVA-Analyseset)
  4  Vier Ausschlussklassen nach CONSORT Box 6 (§ 11.7) — getrennt, mit Fällen
  5  Fallzahluntergrenze § 11.9 (n ≥ 8 je Gruppe): Einstufung je Zielgröße — aus der Regel, nicht aus der Datenlage
  6  Attrition und TESTEX-Kriterium (Outcome bei ≥ 85 % der Teilnehmer): je Zielgröße
  7  Familiarisierung (Spalte) und Status (Spalte): Stand
"""
import sys, os, io, datetime
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
N_MIN = 8   # § 11.9
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
def lade_personen(wb):
    ws = wb['01_Personen']; rows = list(ws.iter_rows(values_only=True)); h = [str(x) for x in rows[0]]
    pers = OrderedDict()
    for r in rows[1:]:
        d = dict(zip(h, r))
        c = d.get('Code')
        if not isinstance(c, str) or not (c[:3] in ('HL-', 'BW-', 'VS-')): continue
        pers[c] = dict(Verein=d['Verein'], Gruppe=GRUPPE[d['Verein']], VereinK=VEREIN_KURZ[d['Verein']], PAH=num(d.get('PAH_Prozent')),
                       Alter=num(d.get('Alter_prä_dez')), Groesse=num(d.get('Größe_prä_cm')), Gewicht=num(d.get('Gewicht_prä_kg')),
                       Fam=d.get('Familiarisierung'), Status=(d.get('Status') or ''), Geb=d.get('Geburtsdatum'), Bem=(d.get('Bemerkung') or ''))
    return pers

data, wb = lade_rohdaten(WB); pers = lade_personen(wb)
codes = sorted(set(d['Code'] for d in data))
hat = defaultdict(set)   # (zp, z) -> codes mit Bestwert
for d in data:
    if d['gilt_neu'] == 1: hat[(d['Zeitpunkt'], d['Z'])].add(d['Code'])
for zp in ('prä', 'post'): hat[(zp, '505M')] = hat[(zp, '505L')] & hat[(zp, '505R')]   # 505M: beide Seiten gültig (Ethikantrag § 3)
grp = {c: pers[c]['Gruppe'] for c in codes}; ver = {c: pers[c]['VereinK'] for c in codes}

P('=' * 100)
P('B4 ANALYSEPOPULATION, NENNER, TEILNEHMERFLUSS')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), '· Workbook:', os.path.abspath(WB))
P('=' * 100)

# ---------------------------------------------------------------- 1 Teilnehmerfluss
P('\n1  TEILNEHMERFLUSS (Teilnehmerebene)')
assert set(pers) == set(codes), (set(pers) ^ set(codes))
P('Codes in 01_Personen und 02_Rohdaten identisch:', len(codes))
for g in ('IG', 'KG'):
    pl = [c for c in codes if grp[c] == g]
    prae = [c for c in pl if any(c in hat[('prä', z)] for z in ZIEL)]
    post = [c for c in pl if any(c in hat[('post', z)] for z in ZIEL)]
    P(f'  {g}: zugeteilt {len(pl)} (' + ', '.join(f'{v} {sum(1 for c in pl if ver[c] == v)}' for v in sorted(set(ver[c] for c in pl))) + f') · prä mit ≥ 1 gültigem Wert {len(prae)} · post mit ≥ 1 gültigem Wert {len(post)}')
    st = Counter(pers[c]['Status'] for c in pl)
    for s, n in st.items(): P(f'     Status „{s}“: {n}' + ('  → ' + ', '.join(c for c in pl if pers[c]['Status'] == s) if n <= 3 else ''))
P('  Vor der Zuteilung ausgeschiedene Spieler (VS-09 entfernt; VS-12–VS-15 laut 00_Hinweise ohne Rohdaten) stehen NICHT im Workbook —')
P('  Zahl und Gründe für das Flussdiagramm (CONSORT Item 13a: „assessed / excluded“) sind vom Verfasser nachzuliefern. ⟨offen⟩')
P('  Sprachregel (Datendurchsicht § 1, CONSORT Box 6): BW-07, BW-21 = „zur Post-Testung nicht angetreten“ — kein Ausschluss, keine Fortschreibung (§ 11.7).')

# ---------------------------------------------------------------- 2 %PAH
P('\n2  KOVARIATE %PAH')
for g in ('IG', 'KG'):
    pl = [c for c in codes if grp[c] == g]; mit = [c for c in pl if pers[c]['PAH'] is not None]
    P(f'  {g}: %PAH vorhanden {len(mit)} von {len(pl)}' + (('; fehlt: ' + ', '.join(f"{c} ({'kein Geburtsdatum' if pers[c]['Geb'] is None else 'Größe/Gewicht „?“ · Alter außerhalb Koeffizientenbereich (§ 3)'})" for c in pl if pers[c]['PAH'] is None)) if len(mit) < len(pl) else ''))
P('  Fassung 9 § 3: „%PAH 28/31, fehlend HL-08, VS-11, VS-18“ → überholt: HL-08 liegt vor (Elterngrößen nachgereicht), N mit %PAH = 29 (IG 18 / KG 11).')

# ---------------------------------------------------------------- 3 Nenner
P('\n3  NENNER JE GRUPPE UND ZIELGRÖSSE (CONSORT Item 16)')
P('Spalten: prä = Bestwert prä · post = Bestwert post · gepaart = prä und post · ANCOVA = gepaart und %PAH (Analyseset Hauptanalyse)')
P('KG-Post steht aus (15.09.2026): KG-Spalten post/gepaart/ANCOVA zeigen die maximal erreichbare Zahl (prä und %PAH vorhanden) in Klammern.')
P(f"{'Zielgröße':10s}{'IG prä':>8s}{'IG post':>8s}{'IG gep.':>8s}{'IG ANC':>8s}{'KG prä':>8s}{'KG post':>8s}{'KG gep.':>9s}{'KG ANC':>9s}")
nenner = {}
for z in ZIEL:
    row = {}
    for g in ('IG', 'KG'):
        pl = [c for c in codes if grp[c] == g]
        pre = [c for c in pl if c in hat[('prä', z)]]; po = [c for c in pl if c in hat[('post', z)]]
        gep = [c for c in pre if c in hat[('post', z)]]; anc = [c for c in gep if pers[c]['PAH'] is not None]
        row[g] = dict(prae=pre, post=po, gep=gep, anc=anc, anc_max=[c for c in pre if pers[c]['PAH'] is not None])
    nenner[z] = row
    kg = row['KG']
    P(f"{z:10s}{len(row['IG']['prae']):8d}{len(row['IG']['post']):8d}{len(row['IG']['gep']):8d}{len(row['IG']['anc']):8d}{len(kg['prae']):8d}{('(' + str(len(kg['prae'])) + ')'):>8s}{('(' + str(len(kg['prae'])) + ')'):>9s}{('(' + str(len(kg['anc_max'])) + ')'):>9s}")
P('  Datendurchsicht Tab. 5 (11.09.): IG 16 / 7 / 16 / 16 / 15 / 14 · KG (max.) 7 / 11 / 11 / 10 / 11 / 11 — Reihenfolge 5m, 10m, 30m, SBJ, 505L, 505R')
P('  Fassung 9 § 3 rechnete mit IG 17 (%PAH fehlte bei HL-08) — überholt.')
P('\n  Fehlende IG-Fälle je Zielgröße (gepaart) — Codes und Grund:')
for z in ZIEL:
    pl = [c for c in codes if grp[c] == 'IG']
    fehl = [c for c in pl if c not in nenner[z]['IG']['gep']]
    gr = []
    for c in fehl:
        if c in ('BW-07', 'BW-21'): gr.append(f'{c} (nicht angetreten)')
        elif c not in hat[('prä', z)]: gr.append(f'{c} (kein gültiger Prä-Wert)')
        else:
            bem = Counter(d['Bemerkung'] for d in data if d['Code'] == c and d['Zeitpunkt'] == 'post' and d['Z'] == z)
            txt = '; '.join((b if b else 'ohne Bemerkung') + '×' + str(n) for b, n in bem.items())
            gr.append(f"{c} (kein gültiger Post-Wert: {txt})")
    P(f'   {z:5s}: ' + (', '.join(gr) if gr else '—'))

# ---------------------------------------------------------------- 4 Ausschlussklassen
P('\n4  VIER AUSSCHLUSSKLASSEN NACH CONSORT BOX 6 (§ 11.7) — getrennt behandeln')
P('  a) Nichteinhaltung (nur für die Per-Protokoll-Rechnung relevant; ITT behält alle): HL-04 alt = ? · BW-01 (keine Meldung) und alle unter der Mindestdosis — Fallliste in B0/B9.')
P('     ⚠ Codeschema: „HL-04“ in § 11.7 ist ein Code des Fragebogens (altes Schema). Im Workbook existiert HL-04 nicht (Codes HL-01, -02, -03, -05, -06, -07, -08).')
P('     Die Zuordnung Fragebogen ↔ Workbook läuft über die Konkordanz alt→neu (B0-Mindestdosis, Rechnung a). Vor jeder Per-Protokoll-Rechnung zu klären.')
P('  b) Instrumentenfehler: BW-11 neu / BW-21 alt stand in der Auswahlliste des Fragebogens nicht zur Verfügung → bleibt in JEDER Analyse (kein Ausschluss).')
P('  c) Fehlende Kovariate: VS-11 (kein Geburtsdatum), VS-18 (Alter außerhalb des Khamis-Roche-Koeffizientenbereichs; Größe/Gewicht „?“) → fehlen im ANCOVA-Set;')
P('     Verzerrungsrisiko benennen (§ 12 Nr. 18: beide gehören in der KG zur schwächeren Hälfte) — Prüfung in B5.')
P('  d) Versuchsausschluss (unterhalb der Teilnehmerebene, B1): kein Teilnehmerausschluss; Nenner je Zielgröße fallen auseinander (Tabelle oben).')
P('  Nicht angetreten (BW-07, BW-21): keine der vier Klassen — Ausfall bei der Nacherhebung, im Flussdiagramm gesondert.')

# ---------------------------------------------------------------- 5 § 11.9
P('\n5  FALLZAHLUNTERGRENZE § 11.9 (n ≥ 8 je Gruppe für Inferenzstatistik) — Regel vorab, nicht Datenlage')
for z in ZIEL:
    ig = len(nenner[z]['IG']['anc']); kg = len(nenner[z]['KG']['anc_max'])
    urteil = 'inferenzstatistisch (ANCOVA) möglich' if ig >= N_MIN and kg >= N_MIN else 'NUR DESKRIPTIV (n < 8 in ' + ', '.join(g for g, n in (('IG', ig), ('KG', kg)) if n < N_MIN) + ')'
    P(f'   {z:5s}: IG {ig:2d} · KG max. {kg:2d} → {urteil}')
P('   COD-Defizit (505 − 10 m, § 11.2): benötigt 10-m-Post → IG n = ' + str(len(nenner['10m']['IG']['anc'])) + ' → nur deskriptiv / entfällt (Datendurchsicht § 2).')
P('   Die KG-Zahlen sind Obergrenzen; nach dem 15.09. neu prüfen. Konfirmatorisch (Auswertungsplan 12.09.): 30 m, 505M, SBJ; 505 L/R nur deskriptiv.')
P('   Der Ethikantrag sieht keine primäre Zielgröße vor (H1: „mindestens einer der erhobenen Parameter“); nach § 11.1 hat allein der SBJ ausreichende Sensitivität → 6.1.')

# ---------------------------------------------------------------- 6 Attrition / TESTEX
P('\n6  ATTRITION UND TESTEX-KRITERIUM „Outcome bei ≥ 85 % der Teilnehmer“')
for g in ('IG', 'KG'):
    pl = [c for c in codes if grp[c] == g]; n = len(pl)
    post = [c for c in pl if any(c in hat[('post', z)] for z in ZIEL)]
    P(f'  {g}: Teilnehmerebene post {len(post)}/{n} = {100 * len(post) / n:.1f} %' + ('' if g == 'IG' else ' (ausstehend)'))
    for z in ZIEL:
        m = len(nenner[z][g]['gep'])
        P(f'     {z:5s} gepaart {m:2d}/{n} = {100 * m / n:5.1f} % → {"≥ 85 %" if m / n >= 0.85 else "< 85 % (TESTEX-Punkt nicht erfüllt)"}' if g == 'IG' else f'     {z:5s} prä {len(nenner[z][g]["prae"]):2d}/{n} = {100 * len(nenner[z][g]["prae"]) / n:5.1f} % (prä-Verfügbarkeit)')
P('  ⚠ § 12 Nr. 8 „15-%-Schwelle überschritten“: auf Teilnehmerebene IG 16/18 = 88,9 % (nicht überschritten); je Zielgröße überschritten bei 10 m (7/18), 505 R (14/18), 505 L (15/18).')
P('     Die Aussage ist je Zielgröße zu formulieren, nicht pauschal.')

# ---------------------------------------------------------------- 7 Familiarisierung / Status
P('\n7  SPALTEN FAMILIARISIERUNG UND STATUS (01_Personen)')
P('  Familiarisierung:', dict(Counter(str(pers[c]['Fam']) for c in codes)), '→ leer bei', ', '.join(c for c in codes if pers[c]['Fam'] in (None, '')))
P('  Stand 12.09. (Verfasser, Anwesenheitslisten): Zahl der absolvierten Familiarisierungstermine je Spieler; Verein A durchgängig 1 (nur ein Termin verfügbar), B 8 × 2 / 3 × 1, C 12 × 2.')
P('  F2-Machbarkeit (§ 11.5 Nr. 1): Variante a = Ausschluss der Spieler mit einer Familiarisierung; Variante b = Familiarisierung (1/2) als zusätzliche Kovariate (in B7, Block F).')
for z in ZIEL:
    anc = nenner[z]['IG']['anc']; ohne1 = [c for c in anc if str(pers[c]['Fam']) != '1']
    P(f"     {z:5s}: IG-ANCOVA-Set {len(anc):2d} → ohne Spieler mit Familiarisierung = 1: {len(ohne1):2d} ({'Inferenz' if len(ohne1) >= N_MIN else 'n < 8 → Variante a nur deskriptiv'})")
P('  Die Familiarisierungsdosis ist in der IG mit Verein A konfundiert (alle A = 1); Variante b schätzt deshalb einen Vereins-/Familiarisierungseffekt gemeinsam — nur als Sensitivität, ausdrücklich so benannt.')
P('  Status:', dict(Counter(pers[c]['Status'][:40] for c in codes)))
P('  → Datendurchsicht § 5.4 („Status weiterhin 0 von 31“) ist überholt: Spalte am 11.09. gefüllt.')

# ---------------------------------------------------------------- 8 Ausfallanalyse (Maßnahme D4)
P('\n8  AUSFALLANALYSE (D4): Prä-Bestwerte der zur Post-Testung nicht angetretenen IG-Spieler gegen die verbliebenen IG-Spieler')
P('  Deskriptiv (n = 2): Wert, Rang in der IG (1 = bester), Differenz zum Mittel der Verbliebenen in Einheiten der IG-SD.')
import statistics as _st
for z in [z for z in ZIEL if z != '505M']:
    vals = {}
    for d in data:
        if d['Gruppe'] == 'IG' and d['Zeitpunkt'] == 'prä' and d['Z'] == z and d['gilt_neu'] == 1:
            vals.setdefault(d['Code'], []).append(d['Wert'])
    best = {c: (min(v) if ZIEL[z][3] == 'min' else max(v)) for c, v in vals.items()}
    ranked = sorted(best, key=lambda c: best[c], reverse=(ZIEL[z][3] == 'max')); rang = {c: i + 1 for i, c in enumerate(ranked)}
    rest = [best[c] for c in best if c not in ('BW-07', 'BW-21')]
    m, sd = _st.mean(rest), _st.stdev(rest)
    parts = []
    for c in ('BW-07', 'BW-21'):
        if c in best: parts.append(f"{c} {best[c]:g} (Rang {rang[c]}/{len(best)}, {(best[c] - m) / sd:+.2f} SD)")
        else: parts.append(f'{c} kein Prä-Wert')
    P(f"   {z:5s} verbliebene IG n = {len(rest)}: M {m:.3f} SD {sd:.3f} · " + ' · '.join(parts))
P('  KG: Ausfallanalyse erst nach dem 15.09. möglich.')

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

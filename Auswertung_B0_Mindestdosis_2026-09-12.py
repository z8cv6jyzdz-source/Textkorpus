# -*- coding: utf-8 -*-
"""
Auswertung_B0_Mindestdosis_2026-09-12.py — Phase B, Sperrpunkt B0.1: Mindestdosis der Per-Protokoll-Rechnung
Bachelorarbeit U15-Plyometrie · DSHS Köln · Analyseprotokoll 2026-09-12
Stand 12.09.2026 (Rev. 2): Ethikantrag-Kriterium „Adherence ≥ 75 %“ (= ≥ 9 von 12) als Abschnitt 2b ausgewiesen; Festlegung ≥ 6/12 unverändert.
Ergänzung 12.09.2026, abends (Maßnahme K20, aus Auswertung_F1_Fragebogen_2026-09-12): Abschnitt 6 führt zwei Untergrenzen der Adhärenz mit —
    „Wo-cap“ = höchstens zwei „ganz“-Meldungen je Programmwoche nach Meldedatum (W1 20.–26.07. … W6 24.–30.08.; Veröffentlichung sonntags 20 Uhr)
    „H003-dist“ = Zahl distinkter Einheitennummern mit Status „ganz“. Hauptzählung (je Meldung, Status „ganz“) unverändert; Statusregel „ganz“ am 12.09. bestätigt (F1 § 6.3).

FESTLEGUNG DES VERFASSERS (11.09.2026, unverändert übernommen aus der Empfehlung § 11.7 / Maßnahmenliste 09.09.):
    Per-Protokoll = mindestens SECHS von zwölf angebotenen Einheiten VOLLSTÄNDIG absolviert (H004 = 1 „ganz“).
    Die Schwelle ist in Einheiten festgelegt und wird in diesem Skript NICHT verändert. Sie wird weder mit einer
    Literaturschwelle (§ 6.6: es gibt keine belegte Mindestdosis) noch mit der resultierenden Fallzahl begründet,
    sondern als inhaltliche Konvention: wer die Hälfte des angebotenen Programms vollständig absolviert hat, gilt als behandelt.
    Die Fallzahlfolgen werden berichtet, nicht als Grund angeführt.

Datenquellen: SoSci_Fragebogen\Fragebogen Datensatz.txt (UTF-16, tabgetrennt, 111 Meldungen) für die Adhärenz;
              Statistik\Studiendaten_U15_gesamt.xlsx (02_Rohdaten, 01_Personen) für Post-Werte und %PAH.
Aufruf (aus Claude\03_Skripte\ oder Claude\; Workbook wird unter ..\Statistik bzw. ..\..\Statistik gesucht):  python Auswertung_B0_Mindestdosis_2026-09-12.py [Workbook] [Fragebogen-Datei]
Ausgabe: gleichnamige .txt neben dem Skript.

Vier Rechnungen nach Übergabeprompt B0.1:
  a  Verteilung der vollständig absolvierten Einheiten je Spieler NACH den Codekorrekturen (CASE-Umschlüsselungen)
  b  Schnittmenge mit den Post-Werten je Zielgröße → tatsächliche Per-Protokoll-Nenner, Prüfung § 11.9
  c  Schwellen-Sensitivität ≥ 5 / ≥ 6 / ≥ 7 (die drei nach § 11.9 zulässigen Schwellen) — Nenner je Zielgröße
  d  Adhärenz stetig: absolvierte Einheiten gegen Prä-Post-Veränderung, nur innerhalb der IG, explorativ (F4)
Dazu: Umsetzungsrate, Adhärenz je Spieler, unerwünschte Effekte (CONSORT Item 19), Abbruchgründe — für B5.
"""
import sys, os, io, csv, math, datetime, statistics
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
FB = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else _finde('SoSci_Fragebogen', 'Fragebogen Datensatz.txt')
OUT = os.path.splitext(os.path.abspath(__file__))[0] + '.txt'
buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); buf.write(s + '\n')

SCHWELLE = 6          # Einheiten „ganz“ — Festlegung des Verfassers 11.09.2026, hier nicht ändern
SCHWELLEN_SENS = (5, 6, 7)
N_MIN = 8             # § 11.9
ANGEBOT = 12          # Einheiten je Spieler
ZIEL = OrderedDict([
    ('5m',   ('Sprint_5m', '–', 's', 'min')),
    ('10m',  ('Sprint_10m', '–', 's', 'min')),
    ('30m',  ('Sprint_30m', '–', 's', 'min')),
    ('505L', ('COD_505', 'L', 's', 'min')),
    ('505R', ('COD_505', 'R', 's', 'min')),
    ('SBJ',  ('Standweitsprung', '–', 'cm', 'max')),
])
GRUPPE = {'Hohenlind': 'IG', 'Blau-Weiß Köln': 'IG', 'Vorwärts Spoho': 'KG'}
VEREIN_KURZ = {'Hohenlind': 'A', 'Blau-Weiß Köln': 'B', 'Vorwärts Spoho': 'C'}

# ---- Fragebogen: Auswahlliste H010 (ALTES Schema, Kodierregeln Fragebogen_A_Datenextraktion_2026-08-31 § 2/3.4)
LISTE = {**{i: 'HL-%02d' % i for i in range(1, 9)}, **{i: 'BW-%02d' % (i - 8) for i in range(9, 23)}}
# Zwei bestätigte Verwechslungen [BELEGT: Angabe Verfasser 31.08.]: CASE → tatsächlicher Code (altes Schema)
CASE_KORREKTUR = {'59': 'BW-06', '70': 'BW-06', '140': 'BW-04', '158': 'BW-04', '165': 'BW-04', '190': 'BW-04', '206': 'BW-04'}
# Konkordanz alt → neu (nur zur Beschriftung; das Workbook führt das ALTE Schema, siehe Befund unten)
ALT_NEU = {'HL-01': 'HL-01', 'HL-02': 'HL-02', 'HL-03': 'HL-03', 'HL-04': 'HL-04', 'HL-06': 'HL-05', 'HL-07': 'HL-06', 'HL-08': 'HL-07',
           'BW-01': 'BW-01', 'BW-02': 'BW-02', 'BW-04': 'BW-03', 'BW-05': 'BW-04', 'BW-06': 'BW-05', 'BW-07': 'BW-06', 'BW-08': 'BW-07',
           'BW-09': 'BW-08', 'BW-10': 'BW-09', 'BW-11': 'BW-10', 'BW-21': 'BW-11'}

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
        pers[c] = dict(Gruppe=GRUPPE[d['Verein']], VereinK=VEREIN_KURZ[d['Verein']], PAH=num(d.get('PAH_Prozent')), Status=d.get('Status') or '')
    return pers

data, wb = lade_rohdaten(WB); agg = aggregiere(data); pers = lade_personen(wb)
ig_codes = sorted(c for c in pers if pers[c]['Gruppe'] == 'IG')
raw = open(FB, encoding='utf-16').read()
meld = list(csv.DictReader(io.StringIO(raw), delimiter='\t'))

P('=' * 100)
P('B0.1 MINDESTDOSIS DER PER-PROTOKOLL-RECHNUNG — Festlegung, Gegenprüfung, Berichtsform')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
P('Workbook:', os.path.abspath(WB), '· Fragebogen:', os.path.abspath(FB), f'({len(meld)} Meldungen)')
P('=' * 100)
P(f'\nFESTLEGUNG (11.09.2026): Per-Protokoll = ≥ {SCHWELLE} von {ANGEBOT} Einheiten vollständig absolviert (Konvention „Hälfte des Programms“).')
P('Begründungsauflagen: (1) keine Literaturschwelle, (2) keine Fallzahlbegründung, (3) Schwellenlandschaft vollständig offenlegen.')
P('Ethikantrag (16.06.2026, Abschnitt 8): „Adherence unter 75 % … Ausschluss aus der Hauptanalyse; Berücksichtigung in Sensitivitätsanalyse“ = ≥ 9 von 12 Einheiten.')
P('Auswertungsplan 12.09.: Das Antragskriterium bleibt berichtet (Abschnitt 2b); Hauptanalyse = alle Zugeteilten (ITT), weil die Antragsteilmenge n < 8 hat (§ 11.9).')
P('Protokollabweichung: Die Festlegung erfolgt nach Sichtung der IG-Post-Werte (Durchsicht 10.09.); § 11.7 verlangte sie davor.')
P('Mildernd: Die Schwelle steht unverändert seit der Maßnahmenliste vom 09.09. (vor dem Post-Termin von Verein A am 10.09.);')
P('die KG-Post-Werte, die den Vergleich tragen, sind bis heute unbekannt. Gesichtet wurde erst danach; die Schwelle ist nicht am Ergebnis ausgerichtet.')

# ---------------------------------------------------------------- Codeschema-Befund
P('\n0  CODESCHEMA — BEFUND VOR JEDER ZUSAMMENFÜHRUNG')
wb_ig = set(ig_codes)
alt_ig = set(ALT_NEU.keys()); neu_ig = set(ALT_NEU.values())
P('  Workbook-IG-Codes:', ', '.join(ig_codes))
P('  altes Schema (Fragebogen-Liste, 18 reale Spieler laut Konkordanz):', ', '.join(sorted(alt_ig)))
P('  neues Schema (Konkordanz):', ', '.join(sorted(neu_ig)))
P(f'  Übereinstimmung Workbook ∩ alt: {len(wb_ig & alt_ig)}/18 · Workbook ∩ neu: {len(wb_ig & neu_ig)}/18')
P('  nur im Workbook:', ', '.join(sorted(wb_ig - alt_ig)) or '—', '· nur im alten Schema:', ', '.join(sorted(alt_ig - wb_ig)) or '—')
P('  ⚠ BEFUND: Das Workbook führt das ALTE Schema (BW-21 und HL-08 vorhanden, BW-03/HL-04 nicht) — entgegen der Angabe im Übergabeprotokoll')
P('    Fragebogenauswertung § 3 („Die Studiendaten führen das NEUE“). Einzige Abweichung: Verein A hat im Workbook HL-05 statt HL-04.')
P('    HL-04 (Liste) und HL-05 (Liste) haben beide keine echte Meldung (die fünf HL-04-Meldungen sind CASE-korrigiert BW-04);')
P('    für die Adhärenzzuordnung ist deshalb ohne Belang, ob Workbook-HL-05 dem Listenplatz HL-04 oder HL-05 entspricht: 0 Meldungen in beiden Lesarten.')
P('    Folge für § 11.7 / Fassung 9: „BW-11 neu“ (Instrumentenfehler) ist im Workbook BW-21; Workbook-BW-11 ist ein anderer Spieler (BW-10 neu).')
P('    Zusammenführung Fragebogen ↔ Workbook in diesem Skript: Listen-Code (alt, CASE-korrigiert) = Workbook-Code; HL-04 (Liste) → HL-05 (Workbook).')
MAP_WB = {c: c for c in ALT_NEU}; MAP_WB['HL-04'] = 'HL-05'

# ---------------------------------------------------------------- Meldungen je Code
def code_roh(r):
    return LISTE.get(int(r['H010'])) if r['H010'].strip().isdigit() else None
def code_korr(r):
    return CASE_KORREKTUR.get(r['CASE'], code_roh(r))
for r in meld:
    r['code_roh'] = code_roh(r); r['code_alt'] = code_korr(r); r['code_wb'] = MAP_WB.get(r['code_alt'], r['code_alt'])
P('\n1  MELDUNGEN JE CODE — roh (wie gewählt) und CASE-korrigiert (altes Schema = Workbook-Code)')
P(f"{'Liste alt':10s}{'neu':7s}{'Workbook':9s}{'Meld. roh':>10s}{'ganz roh':>9s}{'Meld. korr':>11s}{'ganz':>6s}{'teilw.':>7s}{'gar nicht':>10s}{'Anteil ganz':>12s}")
ganz = {}; det = {}
for c in sorted(ALT_NEU):
    roh = [r for r in meld if r['code_roh'] == c]; korr = [r for r in meld if r['code_alt'] == c]
    a = Counter(r['H004'] for r in korr); ganz[MAP_WB[c]] = a['1']
    det[MAP_WB[c]] = dict(meld=len(korr), ganz=a['1'], teilw=a['2'], gar=a['3'])
    P(f"{c:10s}{ALT_NEU[c]:7s}{MAP_WB[c]:9s}{len(roh):10d}{sum(1 for r in roh if r['H004'] == '1'):9d}{len(korr):11d}{a['1']:6d}{a['2']:7d}{a['3']:10d}{100 * a['1'] / ANGEBOT:11.0f} %")
sonst = [r for r in meld if r['code_alt'] not in ALT_NEU]
P(f"  Meldungen unter Listencodes ohne realen Spieler (HL-05, BW-03, BW-12…14 alt) nach Korrektur: {len(sonst)}  " + (str(Counter(r['code_alt'] for r in sonst)) if sonst else ''))
P(f"  Summe Meldungen {len(meld)} · ganz {sum(1 for r in meld if r['H004'] == '1')} · teilweise {sum(1 for r in meld if r['H004'] == '2')} · gar nicht {sum(1 for r in meld if r['H004'] == '3')}")
P('  BW-21 (Workbook) = BW-11 neu: kein Listenplatz (Liste endete bei BW-14 alt) → Instrumentenfehler, 0 Meldungen, bleibt in jeder ITT-Analyse; für Per-Protokoll nicht klassifizierbar.')
n_ganz_gesamt = sum(ganz.values())
P(f'\n  Umsetzungsrate: {n_ganz_gesamt} vollständige von {ANGEBOT * len(ig_codes)} angebotenen Einheiten ({len(ig_codes)} × {ANGEBOT}) = {100 * n_ganz_gesamt / (ANGEBOT * len(ig_codes)):.1f} %')
vals = [ganz[c] for c in ig_codes]
P(f'  je zugeteiltem Spieler: Mittel {statistics.mean(vals):.2f} · Median {statistics.median(vals):.1f} · Spanne {min(vals)}–{max(vals)} (n = {len(vals)}, BW-21 mit 0 gezählt)')
vals2 = [ganz[c] for c in ig_codes if c != 'BW-21']
P(f'  ohne BW-21 (Instrumentenfehler): Mittel {statistics.mean(vals2):.2f} · Median {statistics.median(vals2):.1f} (n = {len(vals2)})')

# ---------------------------------------------------------------- a Verteilung / Schwellenlandschaft
P('\n2  RECHNUNG a — VERTEILUNG DER VOLLSTÄNDIGEN EINHEITEN NACH KORREKTUR (alle 18 zugeteilten IG-Spieler)')
verteilung = Counter(vals)
P('  vollständige Einheiten: ' + ' · '.join(f'{k}×{verteilung[k]}' for k in sorted(verteilung)))
P('  Übergabeprompt (Rohstand, vor Korrektur, 16 meldende Codes): 1×3 · 2×1 · 4×1 · 5×2 · 6×1 · 7×3 · 8×2 · 9×2 · 12×1')
P(f"\n{'Schwelle':>10s}{'Anteil Progr.':>14s}{'n (korrigiert)':>15s}{'n (roh, Prompt)':>16s}{'§ 11.9':>10s}   Spieler")
roh_n = {4: 12, 5: 11, 6: 9, 7: 8, 8: 5, 12: 1}
for s in (4, 5, 6, 7, 8, 9, 12):
    pl = [c for c in ig_codes if ganz[c] >= s]
    P(f"{('≥ ' + str(s)):>10s}{100 * s / ANGEBOT:13.0f} %{len(pl):15d}{(str(roh_n[s]) if s in roh_n else '—'):>16s}  {('ok' if len(pl) >= N_MIN else 'unterschritten'):15s}  " + ', '.join(pl) + ('   ← GEWÄHLT' if s == SCHWELLE else ''))
pp6 = [c for c in ig_codes if ganz[c] >= SCHWELLE]
P(f'\n  Bei ≥ {SCHWELLE} Einheiten: n = {len(pp6)} (Rohstand 9). Änderung durch die CASE-Korrekturen: BW-04 alt (= BW-03 neu) erhält die fünf unter HL-04 gemeldeten Einheiten')
P('  und erreicht damit die Schwelle. Die Schwelle bleibt; nur die Spielerzahl ändert sich (Auflage Rechnung a).')
P(f'  § 11.9 begrenzt die Schwelle nach oben: bei ≥ 8 Einheiten n = {sum(1 for c in ig_codes if ganz[c] >= 8)} < 8. Zulässige Schwellen nach § 11.9: ' + ', '.join(f'≥ {s}' for s in range(1, 13) if sum(1 for c in ig_codes if ganz[c] >= s) >= N_MIN))

# ---------------------------------------------------------------- 2b Ethikantrag-Kriterium
P('\n2b  ETHIKANTRAG-KRITERIUM „Adherence ≥ 75 %“ (≥ 9 von 12 vollständige Einheiten) — Abweichung mit Grund')
pp9 = [c for c in ig_codes if ganz[c] >= 9]
P(f'  Spieler mit ≥ 9 Einheiten: n = {len(pp9)} → ' + ', '.join(f'{c} ({ganz[c]})' for c in pp9))
for z in ZIEL:
    pl = [c for c in pp9 if (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    P(f'     {z:5s}: ANCOVA-fähig (prä + post + %PAH) n = {len(pl)} → ' + (', '.join(pl) if pl else '—'))
P(f'  Folge: Die im Antrag vorgesehene Hauptanalyse (nur Spieler ≥ 75 %) hätte n = {len(pp9)} < {N_MIN} in der IG — nach § 11.9 keine Inferenz möglich.')
P('  Deshalb (Auswertungsplan 12.09., vor Kenntnis der KG-Werte): Hauptanalyse = alle Zugeteilten (ITT, CONSORT-Logik); die Antragsteilmenge (≥ 9) wird')
P('  deskriptiv berichtet (Einzelwerte, kein Test); Per-Protokoll ≥ 6/12 (Festlegung des Verfassers) als zusätzlicher, beobachtender Vergleich.')
P('  Das ist die einzige Analyseabweichung vom Ethikantrag, die nicht durch die Datenlage erzwungen ist — sie ist durch die Umsetzungsrate erzwungen.')

# ---------------------------------------------------------------- b Schnittmenge Post
P('\n3  RECHNUNG b — SCHNITTMENGE MIT DEN POST-WERTEN (Per-Protokoll-Nenner je Zielgröße)')
P('  Per-Protokoll-fähig = Schwelle erreicht UND gültiger Prä- UND Post-Bestwert der Zielgröße UND %PAH (ANCOVA-Set).')
P(f"{'Zielgröße':10s}{'PP (≥6) n':>10s}  {'§ 11.9':20s}  Spieler")
pp_sets = {}
for z in ZIEL:
    pl = [c for c in pp6 if (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
    pp_sets[z] = pl
    P(f"{z:10s}{len(pl):10d}  {('ok' if len(pl) >= N_MIN else 'n < 8 → deskriptiv'):20s}  " + ', '.join(pl))
P('  Die Per-Protokoll-Rechnung ist ein beobachtender Vergleich der PP-Teilmenge der IG mit der (unveränderten) KG; die KG-Post-Werte stehen aus.')

# ---------------------------------------------------------------- c Schwellen-Sensitivität
P('\n4  RECHNUNG c — SCHWELLEN-SENSITIVITÄT (≥ 5 / ≥ 6 / ≥ 7), vorab festgelegt; Hauptaussage bleibt ≥ 6')
P(f"{'Zielgröße':10s}" + ''.join(f'{("n PP ≥" + str(s)):>10s}' for s in SCHWELLEN_SENS) + '   (ANCOVA-Set: prä + post + %PAH)')
for z in ZIEL:
    line = f'{z:10s}'
    for s in SCHWELLEN_SENS:
        pl = [c for c in ig_codes if ganz[c] >= s and (c, 'prä', z) in agg and (c, 'post', z) in agg and pers[c]['PAH'] is not None]
        line += f'{len(pl):10d}'
    P(line)
P('  Die drei ANCOVA-Läufe (je Schwelle) sind in B7 vorbereitet und laufen nach Eintragung der KG-Post-Werte; alle drei Ergebnisse werden berichtet.')
P('  Deskriptiv heute möglich: Prä-Post-Veränderung des Bestwerts innerhalb der jeweiligen PP-Teilmenge (kein Gruppenvergleich, keine Inferenz):')
for z in ZIEL:
    parts = []
    for s in SCHWELLEN_SENS:
        pl = [c for c in ig_codes if ganz[c] >= s and (c, 'prä', z) in agg and (c, 'post', z) in agg]
        if len(pl) < 2: parts.append(f'≥{s}: n={len(pl)}'); continue
        dl = [agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best'] for c in pl]
        parts.append(f'≥{s}: n={len(pl)} Δ={statistics.mean(dl):+.3f} (SD {statistics.stdev(dl):.3f})')
    rest = [c for c in ig_codes if ganz[c] < SCHWELLE and (c, 'prä', z) in agg and (c, 'post', z) in agg]
    if len(rest) >= 2:
        dl = [agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best'] for c in rest]
        parts.append(f'<6: n={len(rest)} Δ={statistics.mean(dl):+.3f} (SD {statistics.stdev(dl):.3f})')
    P(f'   {z:5s} ' + ' · '.join(parts))
P('  (Vorzeichen: Zeiten negativ = schneller; Standweitsprung positiv = weiter. Nur Orientierung — ein Vergleich „PP gegen Rest“ wäre eine zweite Selektionsschicht.)')

# ---------------------------------------------------------------- d Adhärenz stetig
P('\n5  RECHNUNG d — ADHÄRENZ STETIG GEGEN PRÄ-POST-VERÄNDERUNG, NUR IG, EXPLORATIV (Maßnahme F4)')
P('  x = vollständig absolvierte Einheiten (0–12); y = Bestwert post − Bestwert prä. Ohne BW-21 (Adhärenz unbekannt, Instrumentenfehler).')
P('  Variante I: nicht dokumentierende Spieler (BW-01, HL-05) mit 0 · Variante II: nur Spieler mit ≥ 1 Meldung.')
P('  Pearson r und Spearman ρ mit 95-%-KI (Fisher-z) und p; kein Gruppenvergleich nach Adhärenz. Ohne Adjustierung für Mehrfachtestung.')
def korr(x, y):
    n = len(x)
    r = stats.pearsonr(x, y); rho = stats.spearmanr(x, y)
    z = math.atanh(max(-0.9999, min(0.9999, r[0]))); se = 1 / math.sqrt(n - 3) if n > 3 else float('nan')
    lo, hi = math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)
    return r[0], r[1], lo, hi, rho[0], rho[1], n
for z in ZIEL:
    for var, filt in (('I', lambda c: c != 'BW-21'), ('II', lambda c: c != 'BW-21' and det[c]['meld'] > 0)):
        pl = [c for c in ig_codes if filt(c) and (c, 'prä', z) in agg and (c, 'post', z) in agg]
        if len(pl) < 5: P(f'   {z:5s} Var. {var:2s}: n = {len(pl)} — zu wenige Paare'); continue
        x = [ganz[c] for c in pl]; y = [agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best'] for c in pl]
        r, p, lo, hi, rho, prho, n = korr(x, y)
        P(f'   {z:5s} Var. {var:2s}: n = {n:2d}  r = {r:+.3f} [{lo:+.3f}; {hi:+.3f}] p = {p:.3f}   ρ = {rho:+.3f} p = {prho:.3f}')
P('  Einzelwerte (Variante I) je Spieler: Einheiten ganz | Δ je Zielgröße (post − prä, Bestwert):')
P(f"{'Code':7s}{'Verein':7s}{'ganz':>5s}" + ''.join(f'{z:>9s}' for z in ZIEL))
for c in ig_codes:
    line = f"{c:7s}{pers[c]['VereinK']:7s}{ganz[c]:5d}"
    for z in ZIEL:
        if (c, 'prä', z) in agg and (c, 'post', z) in agg:
            dlt = agg[(c, 'post', z)]['best'] - agg[(c, 'prä', z)]['best']
            line += f'{dlt:+9.2f}' if z != 'SBJ' else f'{dlt:+9.0f}'
        else: line += f"{'—':>9s}"
    P(line)
P('  Lesart nach Ramirez-Campillo et al. (2020): stetige Auswertung statt Dichotomisierung; sie kostet keine Fallzahl und erzeugt keine zweite Selektionsschicht.')

# ---------------------------------------------------------------- 6 Adhärenz je Spieler, unerwünschte Effekte
P('\n6  ADHÄRENZ JE SPIELER (für 4.6 / 5.1) — Nenner 12 angebotene Einheiten (Schwab-Punkt „Nenner“ offen)')
P('  K20 (12.09.): „Wo-cap“ = höchstens zwei „ganz“-Meldungen je Programmwoche nach Meldedatum; „H003-dist“ = distinkte Einheitennummern mit Status „ganz“ — beides Untergrenzen (F1 § 6.3).')
W1_START = datetime.datetime(2026, 7, 20)
def _woche(r):
    t = datetime.datetime.strptime(r['STARTED'].strip(), '%d.%m.%Y %H:%M'); w = (t - W1_START).days // 7 + 1
    return min(max(w, 0), 7)
def untergrenzen(rs):
    g = [r for r in rs if r['H004'] == '1']
    return sum(min(2, n) for n in Counter(_woche(r) for r in g).values()), len({r['H003'].strip() for r in g})
P(f"{'Workbook':9s}{'neu':7s}{'Meld.':>6s}{'ganz':>6s}{'Wo-cap':>7s}{'H003-dist':>10s}{'teilw':>6s}{'gar':>5s}{'Attendance':>11s}{'CR-10 M':>9s}{'Schmerz':>8s}{'Videopause':>11s}{'Fremdtr.':>9s}  Untergrund (ganz/teilw.)")
cr_alle = []; ug_cap = {}; ug_dist = {}
for c in ig_codes:
    rs = [r for r in meld if r['code_wb'] == c]
    neu = next((ALT_NEU[a] for a in ALT_NEU if MAP_WB[a] == c), '?')
    cr = [int(r['H005']) - 1 for r in rs if r['H004'] in ('1', '2') and r['H005'].strip().isdigit()]
    cr_alle += [int(r['H005']) - 1 for r in rs if r['H004'] == '1' and r['H005'].strip().isdigit()]
    ug = Counter({'1': 'Rasen', '2': 'Kunstrasen', '3': 'Hartplatz', '4': 'Drinnen', '5': 'Anderes'}.get(r['H006'], '?') for r in rs if r['H004'] in ('1', '2'))
    ug_cap[c], ug_dist[c] = untergrenzen(rs)
    P(f"{c:9s}{neu:7s}{len(rs):6d}{det[c]['ganz']:6d}{ug_cap[c]:7d}{ug_dist[c]:10d}{det[c]['teilw']:6d}{det[c]['gar']:5d}{100 * det[c]['ganz'] / ANGEBOT:10.0f} %{(statistics.mean(cr) if cr else float('nan')):9.1f}{sum(1 for r in rs if r['H007'] == '1'):8d}{sum(1 for r in rs if r['H008'] == '1'):11d}{sum(1 for r in rs if r['H009'] == '1'):9d}  {', '.join(f'{k} {v}' for k, v in ug.most_common())}")
P(f"  Summen: ganz {sum(det[c]['ganz'] for c in ig_codes)} · Wo-cap {sum(ug_cap.values())} · H003-dist {sum(ug_dist.values())} von 216 · Mengen ≥ 6: Haupt {sum(1 for c in ig_codes if det[c]['ganz'] >= 6)} / Wo-cap {sum(1 for c in ig_codes if ug_cap[c] >= 6)} / H003-dist {sum(1 for c in ig_codes if ug_dist[c] >= 6)} · ≥ 9: {sum(1 for c in ig_codes if det[c]['ganz'] >= 9)} / {sum(1 for c in ig_codes if ug_cap[c] >= 9)} / {sum(1 for c in ig_codes if ug_dist[c] >= 9)}")
P(f'  CR-10 (nur vollständige Einheiten, n = {len(cr_alle)}): M {statistics.mean(cr_alle):.2f} · SD {statistics.stdev(cr_alle):.2f} · Median {statistics.median(cr_alle):.0f} · Spanne {min(cr_alle)}–{max(cr_alle)}')
P('  Attendance = vollständige zu angebotenen Einheiten (12). Compliance (Protokolltreue) ist im unbeaufsichtigten Setting nicht objektiv prüfbar (§ 4). Meldedatum ≠ Trainingsdatum.')
P('  Vollständige Fragebogenauswertung (Zeitstruktur, Belastung, Untergrund, Videopausen, Fremdtraining, unerwünschte Ereignisse, Instrumentqualität): Auswertung_F1_Fragebogen_2026-09-12.py/.txt.')

P('\n7  UNERWÜNSCHTE EFFEKTE (CONSORT Item 19) — Schmerzmeldungen H007 = ja; Freitext H007_01; Abbruchgründe H004_03')
sm = [r for r in meld if r['H007'] == '1']
P(f'  Schmerzmeldungen: {len(sm)} von {len(meld)} Meldungen · betroffene Spieler: {len(set(r["code_wb"] for r in sm))} (' + ', '.join(sorted(set(r['code_wb'] for r in sm))) + ')')
for r in sorted(sm, key=lambda r: (r['code_wb'], r['STARTED'])):
    P(f"     {r['code_wb']:7s} {r['STARTED'][:10]}  absolviert={ {'1': 'ganz', '2': 'teilweise', '3': 'gar nicht'}[r['H004']]:9s}  „{(r.get('H007_01') or '').strip()[:90]}“")
P('  Nicht absolvierte Einheiten (H004 = gar nicht) mit Grund:')
for r in sorted([r for r in meld if r['H004'] == '3'], key=lambda r: (r['code_wb'], r['STARTED'])):
    P(f"     {r['code_wb']:7s} {r['STARTED'][:10]}  „{(r.get('H004_03') or '').strip()[:90] or '(kein Grund)'}“")
P('  Teilweise absolvierte Einheiten (H004 = teilweise) mit Grund:')
for r in sorted([r for r in meld if r['H004'] == '2'], key=lambda r: (r['code_wb'], r['STARTED'])):
    P(f"     {r['code_wb']:7s} {r['STARTED'][:10]}  „{(r.get('H004_02') or '').strip()[:90] or '(kein Grund)'}“")
P('  Für die KG bestand kein Erfassungsinstrument (Fragebogen B nie erhoben) — als Limitation berichten (§ 12 Nr. 12).')
P(f"  Bearbeitungsdauer TIME_SUM (s): Median {statistics.median([int(r['TIME_SUM']) for r in meld if r['TIME_SUM'].strip().isdigit()]):.0f} · Spanne {min(int(r['TIME_SUM']) for r in meld if r['TIME_SUM'].strip().isdigit())}–{max(int(r['TIME_SUM']) for r in meld if r['TIME_SUM'].strip().isdigit())} (Datenqualitätshinweis)")

open(OUT, 'w', encoding='utf-8').write(buf.getvalue())
print('\n→ geschrieben:', OUT)

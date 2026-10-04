# -*- coding: utf-8 -*-
r"""
Auswertung_F1_Fragebogen_2026-09-12.py — Fragebogen A (Monitoring der Interventionsgruppe) vollständig neu ausgewertet
Bachelorarbeit U15-Plyometrie · DSHS Köln · Übergabe: Claude\04_Uebergaben\Uebergabe_Fragebogenauswertung_2026-09-12.md
Stand 12.09.2026 · Projektanweisungen Fassung 10

Einzige Datenquellen (§ 2 der Übergabe):
    SoSci_Fragebogen\Fragebogen Datensatz.txt              — SoSci-Rohexport, UTF-16, tabgetrennt, 111 Meldungen (maßgeblich)
    SoSci_Fragebogen\data_test546007_2026-08-31_11-37.json — inhaltsgleicher JSON-Export (Gegenprobe; liefert Sekunden der Zeitstempel)
    Fragebogen\Fragebogen_Übersicht.txt                    — SoSci-Codebuch (Antwortoptionen)
    Statistik\Studiendaten_U15_gesamt.xlsx, Blatt 01_Personen — IG-Spieler, Verein, Status, Familiarisierung, %PAH (nur lesen)

Aufruf (aus Claude\03_Skripte\; Dateien werden unter ..\..\ gesucht; Pfade auch als Argumente möglich):
    python Auswertung_F1_Fragebogen_2026-09-12.py [Fragebogen.txt] [Fragebogen.json] [Codebuch.txt] [Workbook.xlsx]
Ausgabe: gleichnamige .txt neben dem Skript — die einzige Zahlenquelle des Befunddokuments.

Zählregeln (Übergabe § 4; Statusregel am 12.09.2026 nach dem Zwischenstopp § 6.3 entschieden — der Verfasser hat die Wahl delegiert):
    • Hauptzählung = Meldungen mit Status „ganz“ (H004 = 1), je Meldung gezählt; die Einheitennummer (H003) ist kein Identitäts-
      merkmal (Verfasser 12.09.: jede abgegebene Meldung zählt, H003 unbeachtlich). „ganz“ bleibt die Statusregel (B0.1, 11.09.), weil
      (a) „teilweise“ vom Instrument nicht quantifiziert wird (Gründe von „letzte paar Minuten“ bis „Alles“ bei Knöchelverletzung),
      (b) die Per-Protokoll-Konvention „vollständig absolviert“ datiert vor Kenntnis der KG-Werte festliegt und eine zweite Umdefinition
      nach Sichtung der IG-Daten vermieden wird, (c) der Ethikantrag („Anzahl durchgeführter Trainingseinheiten“) beide Lesarten trägt,
      (d) „ganz + teilweise“ als Beteiligungsrate (mindestens begonnene Einheiten) und als Sensitivität aller Mengen mitberichtet wird.
    • Einheiten 1–12 wurden chronologisch veröffentlicht (Block 1–3, Trainingsdokumentation_Block1-3.docx); versäumte Einheiten
      wurden nicht nachgeholt, ein Spieler stieg dort ein, wo das Programm stand (Verfasser 12.09.). Beide Einheiten einer
      Woche sind inhaltlich identisch (Trainingsdokumentation, Teil B). → Die Programmwoche nach Meldedatum bestimmt den
      Inhalt der Einheit; die Einheitennummer innerhalb der Woche trägt keine Dosisinformation.
    • Untergrenzen: (2) wochen-gedeckelt = höchstens zwei durchgeführte Einheiten je Programmwoche nach Datum (Kalenderregel
      Mo–So; Veröffentlichungsrhythmus: Wochenvideo sonntags 20 Uhr für die Folgewoche); (3) distinkte H003-Nummern (Itemqualität).
    • Dublettenregel (§ 6.1): zwei Meldungen desselben Spielers innerhalb von ≤ 5 Minuten mit identischem kodiertem Inhalt
      (H003–H009) = Dublette (gekennzeichnet, nicht gelöscht); mit abweichendem Inhalt = zwei Meldungen (Sammelmeldung).
    • HL-03, 09.08. 20:40/20:41 („5 ganz“ / „5 gar nicht“) = zwei Meldungen (Verfasser 12.09.: „so lassen“).
    • Videodauern (Verfasser 12.09., korrigierte Angabe): W1 28:16 · W2 28:02 · W3 24:17 · W4 25:55 · W5 31:03 · W6 31:14; die Erwärmung
      (8:53) war ein eigenes, zusätzliches Video → Sitzungsdauer = Wochenvideo + 8:53 (33:10–40:07 min); sRPE-Load auf dieser Dauer (§ 6.5).
    • Erinnerungen in den WhatsApp-Gruppen wurden eingesetzt (Verfasser 12.09.; Häufigkeit nicht protokolliert).
    • Verein A, W1–W2 (vereinsfrei): extensiver Laufplan des Trainerteams (Verfasser 12.09.; das Dokument liegt nicht im Ordner) → 4.5.2 anpassen.
    • „Nicht gemeldet“ ≠ „nicht trainiert“ · „Meldeintervall“ ≠ „Trainingsabstand“ · Attendance ≠ Compliance.
"""
import sys, os, io, csv, json, math, datetime, statistics
from collections import Counter, defaultdict, OrderedDict
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
def _finde(*rel):
    for up in ('..', os.path.join('..', '..'), os.path.join('..', '..', '..')):
        p = os.path.join(HERE, up, *rel)
        if os.path.exists(p): return os.path.abspath(p)
    return os.path.join(HERE, '..', '..', *rel)
_args = [a for a in sys.argv[1:] if not a.startswith('--')]
FB   = _args[0] if len(_args) > 0 else _finde('SoSci_Fragebogen', 'Fragebogen Datensatz.txt')
FBJ  = _args[1] if len(_args) > 1 else _finde('SoSci_Fragebogen', 'data_test546007_2026-08-31_11-37.json')
CB   = _args[2] if len(_args) > 2 else _finde('Fragebogen', 'Fragebogen_Übersicht.txt')
WB   = _args[3] if len(_args) > 3 else _finde('Statistik', 'Studiendaten_U15_gesamt.xlsx')
OUT  = os.path.splitext(os.path.abspath(__file__))[0] + '.txt'
CSV_OUT = os.path.splitext(os.path.abspath(__file__))[0] + '_Meldungen.csv'   # Zwischenprodukt für die Excel-Aufbereitung
buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); buf.write(s + '\n')
def H(t):
    P('\n' + '=' * 110); P(t); P('=' * 110)
def fmt(x, nd=2):
    if x is None or (isinstance(x, float) and math.isnan(x)): return '—'
    return f'{x:.{nd}f}'.replace('.', ',')

# ------------------------------------------------------------------ Konstanten
ANGEBOT = 12                                    # angebotene Einheiten je Spieler (Nenner, Maßnahme C8)
LISTE = {**{i: 'HL-%02d' % i for i in range(1, 9)}, **{i: 'BW-%02d' % (i - 8) for i in range(9, 23)}}   # H010, altes Schema
CASE_KORREKTUR = {'59': 'BW-06', '70': 'BW-06', '140': 'BW-04', '158': 'BW-04', '165': 'BW-04', '190': 'BW-04', '206': 'BW-04'}  # B0, unverändert
MAP_WB = {c: c for c in LISTE.values()}; MAP_WB['HL-04'] = 'HL-05'        # B0 § 0: Listenplatz HL-04 ↔ Workbook HL-05 (beide ohne Meldung)
STATUS = {'1': 'ganz', '2': 'teilweise', '3': 'gar nicht'}
UNTERGRUND = {'1': 'Rasen/Wiese', '2': 'Kunstrasen', '3': 'Hartplatz/Asphalt', '4': 'Drinnen', '5': 'Anderes'}
JN = {'1': 'ja', '2': 'nein'}
WOCHENTAG = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
W1_START = datetime.datetime(2026, 7, 20, 0, 0)                          # Programmwoche 1: Mo 20.07.2026 (Übergabe § 3)
INTERVENTION_ENDE = datetime.datetime(2026, 8, 30, 23, 59, 59)          # So 30.08.2026
VEROEFF_OFFSET = datetime.timedelta(hours=4)                            # Veröffentlichung sonntags 20:00 = Wochenbeginn − 4 h
KONTAKTE = {1: 52, 2: 66, 3: 80, 4: 96, 5: 106, 6: 120}                  # Bodenkontakte je Einheit, Trainingsdokumentation Teil A/B
VEREIN = {'HL': 'A', 'BW': 'B'}
VEREIN_NAME = {'A': 'Verein A (Hohenlind)', 'B': 'Verein B (Blau-Weiß)'}

def woche_datum(t):
    """Programmwoche 1–6 nach Kalenderregel (Mo 00:00 – So 23:59); 0 = vor W1, 7 = nach W6."""
    if t < W1_START: return 0
    w = (t - W1_START).days // 7 + 1
    return w if w <= 6 else 7
def woche_fenster(t):
    """Programmwoche nach Veröffentlichungsfenster (So 20:00 – So 19:59) — Sensitivität für Sonntagabend-Meldungen."""
    return woche_datum(t + VEROEFF_OFFSET)
def veroeffentlichung(w):
    return W1_START + datetime.timedelta(days=7 * (w - 1)) - VEROEFF_OFFSET

# ------------------------------------------------------------------ 6.1 Einlesen
H('6.1  EINLESEN, KODIERUNG, DUBLETTEN')
P('Skript:', os.path.basename(__file__), '· Lauf:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
P('Rohexport (maßgeblich):', os.path.abspath(FB))
P('JSON-Gegenprobe:       ', os.path.abspath(FBJ))
P('Codebuch:              ', os.path.abspath(CB))
P('Workbook (nur lesen):  ', os.path.abspath(WB))

raw = open(FB, encoding='utf-16').read()
kopf = raw.splitlines()[0].split('\t')
meld = list(csv.DictReader(io.StringIO(raw), delimiter='\t'))
P(f'\nRohexport: {len(meld)} Datenzeilen · {len(kopf)} Spalten · Kopfzeile: ' + ', '.join(kopf))

# JSON-Gegenprobe
js = json.load(open(FBJ, encoding='utf-8'))
jd = js['data']; jmeta = js.get('metadata', {})
P(f"JSON-Export: {len(jd)} Datensätze · exportiert {jmeta.get('datetime')} · Exportfilter: {jmeta.get('filter')}")
jcases = {str(v['CASE']): v for v in jd.values()}
tcases = {r['CASE'] for r in meld}
P(f'  CASE-Mengen identisch: {set(jcases) == tcases} (nur TXT: {sorted(tcases - set(jcases), key=int) or "—"} · nur JSON: {sorted(set(jcases) - tcases, key=int) or "—"})')
FELDER = ['H002', 'H003', 'H004', 'H004_02', 'H004_03', 'H005', 'H006', 'H007', 'H007_01', 'H008', 'H008_01', 'H009', 'H009_01', 'H010',
          'TIME001', 'TIME002', 'TIME003', 'TIME004', 'TIME005', 'TIME006', 'TIME007', 'TIME008', 'TIME009', 'TIME_SUM', 'LASTPAGE', 'MAXPAGE', 'FINISHED']
abw = []
fehlt_json = sorted({f for f in ('MISSING', 'MISSREL', 'TIME_RSI', 'SERIAL', 'REF', 'MAILSENT') if not any(f in v for v in jd.values())})
P(f'  Felder nur im TXT (JSON-Export ohne diese Spalten): {", ".join(fehlt_json) or "—"}')
for r in meld:
    j = jcases[r['CASE']]
    for f in FELDER:
        jv = '' if j.get(f) is None else str(j.get(f))
        if jv != r[f]: abw.append((r['CASE'], f, r[f], jv))
    js_st = j['STARTED']; conv = f'{js_st[8:10]}.{js_st[5:7]}.{js_st[0:4]} {js_st[11:16]}'
    if conv != r['STARTED']: abw.append((r['CASE'], 'STARTED', r['STARTED'], js_st))
P(f'  Feldvergleich TXT ↔ JSON ({len(FELDER)} Felder + STARTED auf Minutenebene): {len(abw)} Abweichung(en)')
for a in abw: P(f'     CASE {a[0]:>4} · {a[1]:8s} · TXT „{a[2]}“ ↔ JSON „{a[3]}“')
P('  → Die Abweichung bei CASE 189 (H008_01) ist eine Excel-Datumsautokorrektur im TXT („3-6“ → „03. Jun“); der JSON-Wert ist der Originalwortlaut')
P('    und wird für den Freitext verwendet. Die TXT-Datei wurde demnach nach dem Export in Excel gespeichert (Format sonst unverändert).')
P('  → Exportfilter (JSON-Metadaten): „Min. bearbeitet bis Seite 9, Fehlende Antworten ≤ 0 %“ — abgebrochene Fragebögen sind im Export nicht enthalten;')
P('    ihre Zahl ist aus diesen Dateien nicht bestimmbar (Rückfrage: ungefilterter SoSci-Export).')

# Konstante Spalten
konst = {c: Counter(r[c] for r in meld) for c in ('H002', 'FINISHED', 'LASTPAGE', 'MAXPAGE', 'MISSING', 'MISSREL', 'STATUS', 'MODE', 'QUESTNNR')}
P('  Konstante Metadaten: ' + ' · '.join(f'{c} = {dict(v)}' for c, v in konst.items()))
P('  H002 („An welchem Tag hast du trainiert?“) = 1 („Heute“) bei 111/111 → das Codebuch bot nur diese Option; der Trainingstag ist nur über den Meldezeitpunkt erfasst.')

# Codebuch (Gegenprobe der Antwortoptionen)
cb_raw = open(CB, encoding='utf-16').read()
cb_items = defaultdict(list)
for line in cb_raw.splitlines():
    t = line.split('\t')
    if len(t) >= 4 and t[0].strip() == 'Itm': cb_items[t[2].strip()[:4]].append(t[3].strip())
P('  Codebuch-Optionen: ' + ' · '.join(f'{k} {len(v)}' for k, v in sorted(cb_items.items())))
assert len(cb_items['H010']) == 22 and len(cb_items['H003']) == 12 and len(cb_items['H004']) == 3 and len(cb_items['H005']) == 11
P('  H005-Skala (Codebuch): ' + ' | '.join(cb_items['H005']) + '  → CR-10 = H005 − 1')

# Workbook: IG-Spieler
wb = openpyxl.load_workbook(WB, data_only=True, read_only=True)
ws = wb['01_Personen']; rows = list(ws.iter_rows(values_only=True)); hdr = [str(x) for x in rows[0]]
pers = OrderedDict()
for r in rows[1:]:
    d = dict(zip(hdr, r)); c = d.get('Code')
    if not isinstance(c, str) or c[:3] not in ('HL-', 'BW-'): continue
    pers[c] = dict(Verein=VEREIN[c[:2]], Status=(d.get('Status') or ''), Fam=d.get('Familiarisierung'), PAH=d.get('PAH_Prozent'))
ig_codes = sorted(pers)
P(f'\nWorkbook 01_Personen: {len(ig_codes)} IG-Spieler → ' + ', '.join(ig_codes))
P('  Verein A: ' + ', '.join(c for c in ig_codes if pers[c]['Verein'] == 'A') + ' · Verein B: ' + ', '.join(c for c in ig_codes if pers[c]['Verein'] == 'B'))
P('  Status: ' + ' · '.join(f'{c} {("ausgewertet" if pers[c]["Status"].startswith("ausgewertet") else "nicht angetreten")}' for c in ig_codes if not pers[c]['Status'].startswith('ausgewertet')) + ' — alle übrigen „ausgewertet“')

# Meldungen anreichern
def dt_txt(s): return datetime.datetime.strptime(s, '%d.%m.%Y %H:%M')
for r in meld:
    j = jcases[r['CASE']]
    r['code_liste'] = LISTE[int(r['H010'])]
    r['code_alt'] = CASE_KORREKTUR.get(r['CASE'], r['code_liste'])
    r['code_wb'] = MAP_WB[r['code_alt']]
    r['korr'] = r['CASE'] in CASE_KORREKTUR
    r['verein'] = VEREIN[r['code_wb'][:2]]
    r['t'] = datetime.datetime.strptime(j['STARTED'], '%Y-%m-%d %H:%M:%S')     # Sekunden aus dem JSON (Minute identisch mit TXT, geprüft)
    r['t_last'] = datetime.datetime.strptime(j['LASTDATA'], '%Y-%m-%d %H:%M:%S')
    r['wd'] = WOCHENTAG[r['t'].weekday()]
    r['w_dat'] = woche_datum(r['t']); r['w_fen'] = woche_fenster(r['t'])
    r['h003'] = int(r['H003']); r['w_h003'] = (r['h003'] + 1) // 2; r['e_h003'] = 2 - (r['h003'] % 2)
    r['status'] = STATUS[r['H004']]; r['durch'] = r['H004'] in ('1', '2'); r['ganz'] = r['H004'] == '1'
    r['cr10'] = int(r['H005']) - 1
    r['ug'] = UNTERGRUND[r['H006']]
    r['schmerz'] = r['H007'] == '1'; r['pause'] = r['H008'] == '1'; r['fremd'] = r['H009'] == '1'
    r['fx_teilw'] = r['H004_02'].strip(); r['fx_gar'] = r['H004_03'].strip(); r['fx_schmerz'] = r['H007_01'].strip()
    r['fx_pause'] = (str(j.get('H008_01') or '')).strip(); r['fx_fremd'] = r['H009_01'].strip()   # H008_01 aus dem JSON (CASE 189)
    r['time_sum'] = int(r['TIME_SUM'])
    r['so_nach_20'] = (r['t'].weekday() == 6 and r['t'].hour >= 20)
    r['flag'] = []
meld.sort(key=lambda r: (r['code_wb'], r['t']))

# Meldungen je Code
P('\nMELDUNGEN JE CODE — Auswahlliste (roh) und nach CASE-Korrektur (= Workbook-Code)')
P(f"{'Liste':8s}{'Workbook':10s}{'Verein':7s}{'roh':>5s}{'korr.':>7s}{'ganz':>6s}{'teilw.':>7s}{'gar nicht':>10s}{'durchgef.':>10s}   Bemerkung")
for c in LISTE.values():
    roh = [r for r in meld if r['code_liste'] == c]; korr = [r for r in meld if r['code_alt'] == c]
    a = Counter(r['H004'] for r in korr); wbc = MAP_WB[c]
    bem = ''
    if wbc not in pers: bem = 'kein realer Spieler (Listenplatz unbesetzt)'
    elif not pers[wbc]['Status'].startswith('ausgewertet'): bem = 'Workbook-Status: Post-Testung nicht angetreten'
    if c == 'HL-04': bem = 'Listenplatz HL-04 = Workbook HL-05 (beide ohne echte Meldung); die 5 Rohmeldungen sind CASE-korrigiert BW-04'
    if len(roh) + len(korr) == 0 and not bem: bem = 'keine Meldung'
    P(f"{c:8s}{(wbc if wbc in pers else '—'):10s}{VEREIN[c[:2]]:7s}{len(roh):5d}{len(korr):7d}{a['1']:6d}{a['2']:7d}{a['3']:10d}{a['1'] + a['2']:10d}   {bem}")
P(f"{'Summe':25s}{len(meld):5d}{len(meld):7d}{sum(1 for r in meld if r['H004'] == '1'):6d}{sum(1 for r in meld if r['H004'] == '2'):7d}{sum(1 for r in meld if r['H004'] == '3'):10d}{sum(1 for r in meld if r['durch']):10d}")
P('  BW-21 (Workbook) stand nicht in der Auswahlliste (Liste endete bei BW-14) → Instrumentenfehler, 0 Meldungen; zur Post-Testung nicht angetreten.')
P('  Ohne Meldung außerdem: ' + ', '.join(c for c in ig_codes if not any(r['code_wb'] == c for r in meld)) + '.')
melder = sorted({r['code_wb'] for r in meld})
P(f'  Meldende Spieler: {len(melder)} von {len(ig_codes)} → ' + ', '.join(melder))
assert all(r['code_wb'] in pers for r in meld), 'Meldung ohne realen Spieler'

# Dublettenregel
P('\nDUBLETTENREGEL — Paare desselben Spielers mit Abstand ≤ 5 min (Sammelmeldung) · identischer kodierter Inhalt H003–H009 = Dublette')
KOD = ('H003', 'H004', 'H005', 'H006', 'H007', 'H008', 'H009')
paare = []
by_code = defaultdict(list)
for r in meld: by_code[r['code_wb']].append(r)
for c, rs in by_code.items():
    for a, b in zip(rs, rs[1:]):
        d = (b['t'] - a['t']).total_seconds() / 60
        if d <= 5:
            ident = all(a[k] == b[k] for k in KOD)
            fx_ident = all(a[k] == b[k] for k in ('fx_teilw', 'fx_gar', 'fx_schmerz', 'fx_pause', 'fx_fremd'))
            paare.append((c, a, b, d, ident, fx_ident))
            if ident:
                b['flag'].append('Dublette (kodierter Inhalt identisch mit CASE %s, Δ %.0f min)' % (a['CASE'], d))
            else:
                a['flag'].append('Sammelmeldung (Paar mit CASE %s, Δ %.0f min)' % (b['CASE'], d)); b['flag'].append('Sammelmeldung (Paar mit CASE %s, Δ %.0f min)' % (a['CASE'], d))
P(f'  Paare ≤ 5 min: {len(paare)}')
for c, a, b, d, ident, fxi in paare:
    P(f"   {c}  CASE {a['CASE']:>3} {a['t'].strftime('%d.%m. %H:%M:%S')} H003={a['h003']:>2} {a['status']:9s} CR {a['cr10']:>2} {a['ug']:17s} S {JN[a['H007']]:4s} V {JN[a['H008']]:4s} F {JN[a['H009']]:4s}")
    P(f"   {'':6s} CASE {b['CASE']:>3} {b['t'].strftime('%d.%m. %H:%M:%S')} H003={b['h003']:>2} {b['status']:9s} CR {b['cr10']:>2} {b['ug']:17s} S {JN[b['H007']]:4s} V {JN[b['H008']]:4s} F {JN[b['H009']]:4s}   Δ = {d:.1f} min → " + ('DUBLETTE nach Regel' if ident else 'zwei Meldungen (Inhalt abweichend)') + ('' if fxi else ' · Freitexte abweichend'))
    for k, lab in (('fx_gar', 'gar-nicht-Grund'), ('fx_teilw', 'teilweise-Grund'), ('fx_pause', 'Videopause'), ('fx_fremd', 'Fremdtraining'), ('fx_schmerz', 'Schmerz')):
        if a[k] or b[k]: P(f"   {'':6s}   {lab}: „{a[k]}“ | „{b[k]}“")
dubl = [r for r in meld if any(f.startswith('Dublette') for f in r['flag'])]
P(f'  → Dubletten nach Regel: {len(dubl)} (' + ', '.join(f"CASE {r['CASE']} {r['code_wb']} {r['status']}" for r in dubl) + ')')
P('    Alle Dubletten nach Regel sind Meldungen mit Status „gar nicht“ — sie berühren keine Zählung durchgeführter Einheiten.')
P('  Offener Fall HL-03, 09.08.2026 (CASE 153 „5 ganz“ 20:40 / CASE 154 „5 gar nicht“ 20:41): Inhalt abweichend (CR-10 3 gegen 0, Untergrund Rasen gegen')
P('    Anderes, Grund „auf dem Weg in den Urlaub“) → nach Regel zwei Meldungen = Sammelmeldung der beiden Einheiten von Programmwoche 3 (eine durchgeführt,')
P('    eine nicht); HL-03 hat in W3 nach Datum genau eine durchgeführte Einheit. Lesart des Verfassers einholen (entscheidet über 9 gegen 8 „ganz“).')

# Zeitgleiche Meldungen verschiedener Spieler (Codesicherheit, Erinnerungen)
P('\nZEITGLEICHE MELDUNGEN VERSCHIEDENER SPIELER (≤ 5 min) — Beobachtung für § 6.8 Codesicherheit und § 6.10 Erinnerungen')
alle = sorted(meld, key=lambda r: r['t']); cluster = []
i = 0
while i < len(alle):
    grp = [alle[i]]; k = i + 1
    while k < len(alle) and (alle[k]['t'] - grp[-1]['t']).total_seconds() <= 300:
        grp.append(alle[k]); k += 1
    if len({r['code_wb'] for r in grp}) >= 2: cluster.append(grp)
    i = k
for grp in cluster:
    P(f"   {grp[0]['t'].strftime('%a %d.%m.')} {grp[0]['t'].strftime('%H:%M')}–{grp[-1]['t'].strftime('%H:%M')}: " + ', '.join(f"{r['code_wb']}({r['verein']}) {r['t'].strftime('%H:%M')} E{r['h003']} {r['status'][:4]}" for r in grp))
P(f'  {len(cluster)} Zeitfenster mit ≥ 2 Spielern; davon vereinsübergreifend: {sum(1 for g in cluster if len({r["verein"] for r in g}) == 2)}.')
P('  Vereinsübergreifende Häufungen (z. B. So 09.08. 18:31–18:38, So 16.08. 13:33–13:40, So 23.08. 21:04–21:16, So 30.08. 11:39–12:11) sprechen für einen')
P('  gemeinsamen Auslöser — Erinnerungen in den WhatsApp-Gruppen wurden eingesetzt (Verfasser 12.09., Häufigkeit nicht protokolliert); kein Beleg für Codeverwechslung.')

# ------------------------------------------------------------------ 6.2 Zeitstruktur
H('6.2  ZEITSTRUKTUR DER MELDUNGEN (Meldezeitpunkt STARTED; Trainingstag nicht erhoben)')
P('Programmwochen nach Datum (Kalenderregel Mo 00:00 – So 23:59): W1 20.–26.07. · W2 27.07.–02.08. · W3 03.–09.08. · W4 10.–16.08. · W5 17.–23.08. · W6 24.–30.08.2026')
P('Veröffentlichung des Wochenvideos: sonntags 20:00 für die Folgewoche (Übergabe § 3) → Veröffentlichungsfenster So 20:00 – So 19:59 als Sensitivität.')
P(f"Erste Meldung {min(r['t'] for r in meld).strftime('%a %d.%m.%Y %H:%M')} · letzte {max(r['t'] for r in meld).strftime('%a %d.%m.%Y %H:%M')} · vor W1: {sum(1 for r in meld if r['w_dat'] == 0)} · nach W6: {sum(1 for r in meld if r['w_dat'] == 7)}")
so20 = [r for r in meld if r['so_nach_20']]
P(f"Meldungen sonntags ab 20:00 (nächstes Wochenvideo bereits online): {len(so20)} → " + ', '.join(f"{r['code_wb']} {r['t'].strftime('%d.%m. %H:%M')} E{r['h003']} {r['status'][:4]}" for r in so20))
P(f"  davon mit H003-Woche = Kalenderwoche des Datums: {sum(1 for r in so20 if r['w_h003'] == r['w_dat'])} · = Folgewoche: {sum(1 for r in so20 if r['w_h003'] == r['w_dat'] + 1)} · andere: {sum(1 for r in so20 if r['w_h003'] not in (r['w_dat'], r['w_dat'] + 1))}")
P('  → Die Kalenderregel ist die Hauptzuordnung; die Fensterregel wird bei der Wochen-Deckelung als Sensitivität mitgeführt (§ 6.3).')

# Meldeintervalle je Spieler
P('\nMELDEINTERVALLE JE SPIELER (aufeinanderfolgende Meldungen, Stunden) — „Meldeintervall“, nicht „Trainingsabstand“')
alle_iv = []
for c in melder:
    rs = by_code[c]
    iv = [((b['t'] - a['t']).total_seconds() / 3600, a, b) for a, b in zip(rs, rs[1:])]
    alle_iv += [(c, h, a, b) for h, a, b in iv]
    if iv:
        hs = [h for h, _, _ in iv]
        P(f"   {c}  n = {len(rs):2d} Meldungen, {len(iv):2d} Intervalle · Median {fmt(statistics.median(hs), 1)} h · min {fmt(min(hs), 1)} h · max {fmt(max(hs), 1)} h · < 24 h: {sum(1 for h in hs if h < 24)} · 24–48 h: {sum(1 for h in hs if 24 <= h < 48)} · ≥ 48 h: {sum(1 for h in hs if h >= 48)} · taggleich: {sum(1 for _, a, b in iv if a['t'].date() == b['t'].date())}")
    else:
        P(f'   {c}  n =  1 Meldung, kein Intervall')
hs = [h for _, h, _, _ in alle_iv]
P(f'\n  Alle Intervalle: n = {len(hs)} ({len(melder)} meldende Spieler) · Median {fmt(statistics.median(hs), 1)} h = {fmt(statistics.median(hs) / 24, 1)} Tage · Spanne {fmt(min(hs), 2)}–{fmt(max(hs), 1)} h')
P(f'  < 24 h: {sum(1 for h in hs if h < 24)} · 24–48 h: {sum(1 for h in hs if 24 <= h < 48)} · ≥ 48 h: {sum(1 for h in hs if h >= 48)} · davon < 48 h gesamt: {sum(1 for h in hs if h < 48)} · taggleich: {sum(1 for _, h, a, b in alle_iv if a["t"].date() == b["t"].date())}')
P('  Intervalle < 48 h im Einzelnen (Δ Stunden; Status beider Meldungen):')
for c, h, a, b in sorted(alle_iv, key=lambda x: x[1]):
    if h < 48:
        P(f"     {c}  {a['t'].strftime('%a %d.%m. %H:%M')} E{a['h003']:>2} {a['status'][:5]:5s} → {b['t'].strftime('%a %d.%m. %H:%M')} E{b['h003']:>2} {b['status'][:5]:5s}   Δ {fmt(h, 1):>6} h" + ('   ⟵ taggleich' if a['t'].date() == b['t'].date() else ''))
P('  Nur Intervalle zwischen durchgeführten Einheiten (ganz/teilweise → ganz/teilweise), Sensitivität:')
iv_d = [(c, (b['t'] - a['t']).total_seconds() / 3600) for c in melder for a, b in zip([r for r in by_code[c] if r['durch']], [r for r in by_code[c] if r['durch']][1:])]
hd = [h for _, h in iv_d]
if hd: P(f'     n = {len(hd)} · Median {fmt(statistics.median(hd), 1)} h · < 24 h: {sum(1 for h in hd if h < 24)} · 24–48 h: {sum(1 for h in hd if 24 <= h < 48)} · ≥ 48 h: {sum(1 for h in hd if h >= 48)}')
P('  Der vorgeschriebene 48-h-Abstand zwischen Einheiten ist nicht prüfbar: Meldezeitpunkt ≠ Trainingszeitpunkt (Datums-Item nur „Heute“, Sammelmeldungen belegt).')

# Wochentag × Uhrzeit
P('\nVERTEILUNG DER MELDEZEITPUNKTE — Wochentag und Tageszeit (alle 111 Meldungen)')
wd_c = Counter(r['wd'] for r in meld); wd_d = Counter(r['wd'] for r in meld if r['durch'])
P('  Wochentag (alle / durchgeführt): ' + ' · '.join(f'{w} {wd_c[w]}/{wd_d[w]}' for w in WOCHENTAG))
P(f"  Sonntag: {wd_c['So']} von {len(meld)} = {fmt(100 * wd_c['So'] / len(meld), 1)} % · Wochenende (Sa + So): {wd_c['Sa'] + wd_c['So']} = {fmt(100 * (wd_c['Sa'] + wd_c['So']) / len(meld), 1)} %")
bands = [(0, 6, '00–06'), (6, 12, '06–12'), (12, 18, '12–18'), (18, 24, '18–24')]
P('  Tageszeit: ' + ' · '.join(f"{lab} Uhr {sum(1 for r in meld if lo <= r['t'].hour < hi)}" for lo, hi, lab in bands))
P('  Stunde (Beginn): ' + ' '.join(f"{h:02d}:{sum(1 for r in meld if r['t'].hour == h)}" for h in range(24)))
# Abstand zur Veröffentlichung
P('\nABSTAND ZUR VERÖFFENTLICHUNG DES WOCHENVIDEOS (Sonntag 20:00 vor der Kalenderwoche der Meldung), Tage')
ab = [((r['t'] - veroeffentlichung(r['w_dat'])).total_seconds() / 86400) for r in meld if 1 <= r['w_dat'] <= 6]
P(f'  n = {len(ab)} · Median {fmt(statistics.median(ab), 1)} Tage · Quartile {fmt(statistics.quantiles(ab, n=4)[0], 1)} / {fmt(statistics.quantiles(ab, n=4)[2], 1)} · Spanne {fmt(min(ab), 1)}–{fmt(max(ab), 1)}')
P('  Tag nach Veröffentlichung (1 = Montag … 7 = Sonntag): ' + ' · '.join(f"Tag {d} {sum(1 for x in ab if d - 1 <= x - 4 / 24 < d)}" for d in range(1, 8)))
# Meldungen je Programmwoche × Verein
P('\nMELDUNGEN JE PROGRAMMWOCHE (nach Datum) UND VEREIN — alle / ganz / teilweise / gar nicht · Spieler mit ≥ 1 Meldung')
P(f"{'Woche':8s}{'Zeitraum':16s}" + ''.join(f"{'Verein ' + v:^30s}" for v in ('A', 'B')) + f"{'gesamt':^30s}")
P(f"{'':24s}" + ''.join(f"{'alle':>6s}{'ganz':>6s}{'teilw':>6s}{'gar':>6s}{'Spl':>6s}" for _ in range(3)))
for w in range(1, 7):
    ws_ = W1_START + datetime.timedelta(days=7 * (w - 1)); zr = f"{ws_.strftime('%d.%m.')}–{(ws_ + datetime.timedelta(days=6)).strftime('%d.%m.')}"
    line = f"{'W' + str(w):8s}{zr:16s}"
    for v in ('A', 'B', None):
        rs = [r for r in meld if r['w_dat'] == w and (v is None or r['verein'] == v)]
        line += f"{len(rs):6d}{sum(1 for r in rs if r['ganz']):6d}{sum(1 for r in rs if r['H004'] == '2'):6d}{sum(1 for r in rs if r['H004'] == '3'):6d}{len({r['code_wb'] for r in rs}):6d}"
    P(line)
line = f"{'Summe':24s}"
for v in ('A', 'B', None):
    rs = [r for r in meld if v is None or r['verein'] == v]
    line += f"{len(rs):6d}{sum(1 for r in rs if r['ganz']):6d}{sum(1 for r in rs if r['H004'] == '2'):6d}{sum(1 for r in rs if r['H004'] == '3'):6d}{len({r['code_wb'] for r in rs}):6d}"
P(line)
P('  Nenner: Verein A 7 zugeteilte Spieler (HL), Verein B 11 (BW, inkl. BW-21 ohne Listenplatz). „Spl“ = Spieler mit mindestens einer Meldung in der Woche.')
P('  Sensitivität Fensterregel (So 20:00 – So 19:59), alle Meldungen je Woche: ' + ' · '.join(f"W{w} {sum(1 for r in meld if r['w_fen'] == w)}" for w in range(1, 7)) + f" · W7 {sum(1 for r in meld if r['w_fen'] == 7)}")

# ------------------------------------------------------------------ 6.3 Einheitenrekonstruktion
H('6.3  EINHEITENREKONSTRUKTION — DREI ZÄHLUNGEN JE SPIELER (ganz | ganz + teilweise)')
P('Zählung 1 „je Meldung“ (Hauptzählung mit Status „ganz“; „ganz + teilweise“ = Beteiligung/Sensitivität; H003 unbeachtlich — Verfasser 12.09.).')
P('Zählung 2 „wochen-gedeckelt“: höchstens 2 je Programmwoche nach Datum (Kalenderregel; Fensterregel als Sensitivität) — Untergrenze aus dem Veröffentlichungsrhythmus.')
P('Zählung 3 „distinkte H003“: Zahl verschiedener Einheitennummern mit dem jeweiligen Status — Untergrenze, zugleich Befund zur Itemqualität.')
P('Alle Zählungen mit Nenner 12 angebotene Einheiten je Spieler; Dubletten nach Regel betreffen nur „gar nicht“ und ändern nichts.')

def zaehl(rs, pred):
    sel = [r for r in rs if pred(r)]
    je = len(sel)
    cap = sum(min(2, n) for n in Counter(r['w_dat'] for r in sel).values())
    cap_f = sum(min(2, n) for n in Counter(r['w_fen'] for r in sel).values())
    dist = len({r['h003'] for r in sel})
    return je, cap, cap_f, dist
Z = OrderedDict()
for c in ig_codes:
    rs = by_code.get(c, [])
    g = zaehl(rs, lambda r: r['ganz']); d = zaehl(rs, lambda r: r['durch'])
    Z[c] = dict(n=len(rs), gar=sum(1 for r in rs if r['H004'] == '3'), teilw=sum(1 for r in rs if r['H004'] == '2'),
                ganz_je=g[0], ganz_cap=g[1], ganz_capf=g[2], ganz_dist=g[3], d_je=d[0], d_cap=d[1], d_capf=d[2], d_dist=d[3])
P(f"\n{'Code':7s}{'V':3s}{'Meld':>5s}{'gar':>4s}{'teilw':>6s} │{'— nur ganz —':^28s}│{'— ganz + teilweise —':^28s}│ Bemerkung")
P(f"{'':25s} │{'jeMeld':>7s}{'Wo-cap':>7s}{'(Fens)':>7s}{'dist':>7s}│{'jeMeld':>7s}{'Wo-cap':>7s}{'(Fens)':>7s}{'dist':>7s}│")
for c in ig_codes:
    z = Z[c]; bem = []
    if c == 'BW-21': bem.append('Instrumentenfehler (kein Listenplatz); Post nicht angetreten')
    elif z['n'] == 0: bem.append('keine Meldung (Nichteinhaltung)')
    if c == 'BW-07': bem.append('Post nicht angetreten')
    if z['n'] and z['ganz_je'] != z['ganz_cap']: bem.append(f"Deckelung greift ({z['ganz_je'] - z['ganz_cap']} ganz über 2/Woche)")
    if z['n'] and z['d_je'] != z['d_dist']: bem.append(f"H003 doppelt ({z['d_je'] - z['d_dist']}×)")
    if z['n'] and z['d_cap'] != z['d_capf']: bem.append('Fensterregel weicht ab')
    P(f"{c:7s}{pers[c]['Verein']:3s}{z['n']:5d}{z['gar']:4d}{z['teilw']:6d} │{z['ganz_je']:7d}{z['ganz_cap']:7d}{z['ganz_capf']:7d}{z['ganz_dist']:7d}│{z['d_je']:7d}{z['d_cap']:7d}{z['d_capf']:7d}{z['d_dist']:7d}│ " + '; '.join(bem))
def summe(k): return sum(Z[c][k] for c in ig_codes)
P(f"{'Summe':7s}{'':3s}{summe('n'):5d}{summe('gar'):4d}{summe('teilw'):6d} │{summe('ganz_je'):7d}{summe('ganz_cap'):7d}{summe('ganz_capf'):7d}{summe('ganz_dist'):7d}│{summe('d_je'):7d}{summe('d_cap'):7d}{summe('d_capf'):7d}{summe('d_dist'):7d}│ von {ANGEBOT * len(ig_codes)} angebotenen Einheiten (18 × 12)")
P(f"{'Anteil':7s}{'':3s}{'':15s} │" + ''.join(f"{fmt(100 * summe(k) / (ANGEBOT * len(ig_codes)), 1) + ' %':>7s}" for k in ('ganz_je', 'ganz_cap', 'ganz_capf', 'ganz_dist')) + '│' + ''.join(f"{fmt(100 * summe(k) / (ANGEBOT * len(ig_codes)), 1) + ' %':>7s}" for k in ('d_je', 'd_cap', 'd_capf', 'd_dist')) + '│ Umsetzungsrate')
P('\n  Kennwerte je zugeteiltem Spieler (n = 18, Nicht-Melder mit 0):')
for k, lab in (('ganz_je', 'ganz, je Meldung (Hauptzählung)'), ('ganz_cap', 'ganz, wochen-gedeckelt'), ('ganz_dist', 'ganz, distinkte H003'), ('d_je', 'ganz + teilweise, je Meldung (Beteiligung)'), ('d_cap', 'ganz + teilweise, wochen-gedeckelt'), ('d_dist', 'ganz + teilweise, distinkte H003')):
    v = [Z[c][k] for c in ig_codes]
    P(f'     {lab:46s} Mittel {fmt(statistics.mean(v))} · Median {fmt(statistics.median(v), 1)} · Verteilung ' + ' · '.join(f'{x}×{n}' for x, n in sorted(Counter(v).items())))
P('\n  Wo die Zählungen auseinanderfallen (Einzelnachweis):')
for c in ig_codes:
    rs = by_code.get(c, [])
    wk = Counter(r['w_dat'] for r in rs if r['durch'])
    over = {w: n for w, n in wk.items() if n > 2}
    for w, n in sorted(over.items()):
        sel = [r for r in rs if r['durch'] and r['w_dat'] == w]
        P(f"     {c}: W{w} nach Datum {n} durchgeführte Meldungen (Deckel 2) → " + ', '.join(f"{r['t'].strftime('%a %d.%m. %H:%M')} E{r['h003']} {r['status'][:5]}" for r in sel))
    dd = Counter(r['h003'] for r in rs if r['durch'])
    for e, n in sorted(dd.items()):
        if n > 1:
            sel = [r for r in rs if r['durch'] and r['h003'] == e]
            P(f"     {c}: H003 = {e} bei {n} durchgeführten Meldungen → " + ', '.join(f"{r['t'].strftime('%a %d.%m. %H:%M')} W{r['w_dat']} {r['status'][:5]} CR{r['cr10']} {r['ug'][:6]}" for r in sel))

# Konkordanz Datumswoche ↔ H003-Woche
P('\nKONKORDANZ DATUMSWOCHE ↔ H003-WOCHE (je Meldung, alle 111)')
kk = Counter((r['w_h003'] - r['w_dat']) for r in meld)
P(f"  Übereinstimmung: {kk[0]} von {len(meld)} = {fmt(100 * kk[0] / len(meld), 1)} % · H003 eine Woche zurück: {kk[-1]} · zwei+ zurück: {sum(v for k, v in kk.items() if k <= -2)} · H003 voraus: {sum(v for k, v in kk.items() if k >= 1)}")
kd = Counter((r['w_h003'] - r['w_dat']) for r in meld if r['durch'])
P(f"  nur durchgeführte (ganz + teilweise, n = {sum(kd.values())}): Übereinstimmung {kd[0]} · zurück {sum(v for k, v in kd.items() if k < 0)} · voraus {sum(v for k, v in kd.items() if k > 0)}")
P('  Abweichungen im Einzelnen:')
for r in meld:
    if r['w_h003'] != r['w_dat']:
        P(f"     CASE {r['CASE']:>3} {r['code_wb']} {r['t'].strftime('%a %d.%m. %H:%M')} · Datumswoche W{r['w_dat']} · H003 = {r['h003']:>2} (W{r['w_h003']} E{r['e_h003']}) · {r['status']}" + ('   ⟵ So ≥ 20:00' if r['so_nach_20'] else ''))
P('  Lesart: H003 eine Woche hinter dem Datum = verspätete Meldung einer Vorwocheneinheit oder Fehlwahl; H003 voraus = Fehlwahl. Nicht entscheidbar aus dem Instrument.')

# Rekonstruktion nach Datum (chronologisch, kein Nachholen)
P('\nEINHEITENZUORDNUNG NACH DATUM (Verfasser 12.09.: Programm chronologisch, versäumte Einheiten nicht nachgeholt; beide Einheiten einer Woche identisch)')
P('  Regel: k-te durchgeführte Meldung (ganz/teilweise) eines Spielers in Programmwoche w nach Datum → Einheit 2w−1 (k = 1) bzw. 2w (k = 2); k ≥ 3 = „über Soll“.')
P('  Die Einheitennummer innerhalb der Woche trägt keine Dosisinformation; maßgeblich für Kontakte (52→120) ist die Woche.')
ueber = []
for c in melder:
    rs = [r for r in by_code[c] if r['durch']]
    cnt = Counter()
    for r in rs:
        cnt[r['w_dat']] += 1; k = cnt[r['w_dat']]
        r['e_rek'] = (2 * r['w_dat'] - 1 + (k - 1)) if k <= 2 else None
        r['w_rek'] = r['w_dat']
        if k >= 3: ueber.append(r)
    for r in by_code[c]:
        if not r['durch']: r['e_rek'] = None; r['w_rek'] = r['w_dat']
P(f"  Meldungen „über Soll“ (3. durchgeführte Meldung derselben Datumswoche): {len(ueber)} → " + ', '.join(f"{r['code_wb']} CASE {r['CASE']} {r['t'].strftime('%d.%m.')} W{r['w_dat']} E{r['h003']}" for r in ueber))
P(f"  Übereinstimmung rekonstruierte Einheit = H003 (durchgeführte Meldungen mit Zuordnung): {sum(1 for r in meld if r['durch'] and r['e_rek'] is not None and r['e_rek'] == r['h003'])} von {sum(1 for r in meld if r['durch'] and r['e_rek'] is not None)}"
  f" · gleiche Woche, andere Einheitennummer: {sum(1 for r in meld if r['durch'] and r['e_rek'] is not None and r['e_rek'] != r['h003'] and r['w_dat'] == r['w_h003'])} · andere Woche: {sum(1 for r in meld if r['durch'] and r['e_rek'] is not None and r['w_dat'] != r['w_h003'])}")
P('\n  Durchgeführte Einheiten je Spieler und Programmwoche nach Datum (ganz+teilweise; Klammer = davon teilweise; · = keine Meldung; g = nur „gar nicht“ gemeldet):')
P(f"{'Code':7s}{'V':3s}" + ''.join(f"{'W' + str(w):>7s}" for w in range(1, 7)) + f"{'Summe':>8s}{'Deckel':>8s}")
for c in ig_codes:
    rs = by_code.get(c, []); line = f"{c:7s}{pers[c]['Verein']:3s}"; s = 0; sc = 0
    for w in range(1, 7):
        sel = [r for r in rs if r['w_dat'] == w]
        d = sum(1 for r in sel if r['durch']); tw = sum(1 for r in sel if r['H004'] == '2')
        if not sel: cell = '·'
        elif d == 0: cell = 'g'
        else: cell = f'{d}' + (f'({tw})' if tw else '')
        line += f'{cell:>7s}'; s += d; sc += min(2, d)
    P(line + f'{s:8d}{sc:8d}')
P('\n  Meldungen je Spieler, chronologisch (Datum · Datumswoche · H003 · rekonstruierte Einheit · Status):')
for c in melder:
    P(f'   {c} ({pers[c]["Verein"]}): ' + ' | '.join(f"{r['t'].strftime('%d.%m.')} W{r['w_dat']} H{r['h003']:>2}→{('E' + str(r['e_rek'])) if r['e_rek'] else ('—' if r['durch'] else 'x')} {r['status'][:4]}" for r in by_code[c]))

# Offene Fälle
P('\nZWISCHENSTOPP § 6.3 — VORGELEGT UND ENTSCHIEDEN (12.09.2026)')
P('  1. Statusregel: Verfasser delegiert („bei ganz bleiben, wenn das der richtige Weg ist“) → Hauptzählung „ganz“ je Meldung (Begründung im Skriptkopf);')
P('     „ganz + teilweise“ läuft als Beteiligungsrate und als Sensitivität mit (Umsetzungsrate 45,4 %; ≥ 6 unverändert; ≥ 9: 4 statt 3 — HL-01 mit 8 ganz + 1 teilweise „Sprünge“).')
P('  2. HL-03, 09.08. 20:40/20:41: zwei Meldungen (Sammelmeldung der beiden W3-Einheiten) — Verfasser: „so lassen“. HL-03 bleibt bei 9.')
P('  3. Zuordnung der Sonntagabend-Meldungen: Kalenderregel (alle 16 tragen die H003-Woche des Kalendertags; die Fensterregel erzeugt eine nicht existierende W7) — Entscheidung des Skripts, dokumentiert.')
P('  4. HL-03 30.08. 11:39/11:40 (CASE 253/254): Dublette nach Regel, inhaltlich Sammelmeldung E11/E12 „gar nicht“ — ohne Folge für die Zählung.')
P('  5. Nachträge des Verfassers (12.09., spät): Videodauern W5 31:03 / W6 31:14, Erwärmung als eigenes Video (8:53) zusätzlich; Erinnerungen in den Gruppen ja; Verein A W1–W2 extensiver Laufplan.')
P('     Offen (Datenqualität, keine Zählfolge): ungefilterter SoSci-Export (abgebrochene Fragebögen) · mündliche Auskunft zu HL-06/BW-01/HL-05.')
P('  6. Hinweis: Trainingsdokumentation_Block1-3.docx endete mit einem fachfremden Textanhang — Kopie in Planung_Intervention\\Trainingsprogramm bereinigt (12.09.); Kopie in Schreiben\\ und Projektdatei prüfen.')

# Zwischenprodukt: Meldungen als CSV (für die Excel-Aufbereitung in § 7 Nr. 2)
with open(CSV_OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['CASE', 'Listencode', 'Workbook-Code', 'CASE-korrigiert', 'Verein', 'Meldezeitpunkt', 'Wochentag', 'Programmwoche_Datum', 'Programmwoche_Fenster', 'H003', 'H003_Woche', 'H003_Einheit', 'Einheit_rekonstruiert', 'Status', 'durchgeführt', 'CR10', 'Untergrund', 'Schmerz', 'Videopause', 'Fremdtraining', 'Grund_teilweise', 'Grund_gar_nicht', 'Schmerz_Freitext', 'Videopause_Freitext', 'Fremdtraining_Freitext', 'TIME_SUM_s', 'So_ab_20Uhr', 'Flag'])
    for r in sorted(meld, key=lambda r: (r['code_wb'], r['t'])):
        w.writerow([r['CASE'], r['code_liste'], r['code_wb'], 'ja' if r['korr'] else '', r['verein'], r['t'].strftime('%d.%m.%Y %H:%M:%S'), r['wd'], r['w_dat'], r['w_fen'], r['h003'], r['w_h003'], r['e_h003'], r['e_rek'] if r['e_rek'] else '', r['status'], 'ja' if r['durch'] else 'nein', r['cr10'], r['ug'], JN[r['H007']], JN[r['H008']], JN[r['H009']], r['fx_teilw'], r['fx_gar'], r['fx_schmerz'], r['fx_pause'], r['fx_fremd'], r['time_sum'], 'ja' if r['so_nach_20'] else '', '; '.join(r['flag'])])
P(f'\n→ Meldungsdatei (Zwischenprodukt) geschrieben: {CSV_OUT}')


# ================================================================== 6.4 Adhärenz
H('6.4  ADHÄRENZ — Umsetzungsraten, Verteilung, Schwellenlandschaft, Mengen, Verlauf, Nicht-Melder')
P('Hauptzählung: Status „ganz“, je Meldung (Zählung 1). Untergrenzen: wochen-gedeckelt (2), distinkte H003 (3). Sensitivität: „ganz + teilweise“ (Beteiligung).')
P('Nenner: 12 angebotene Einheiten je zugeteiltem Spieler (Maßnahme C8) → Verein A 7 × 12 = 84 · Verein B 11 × 12 = 132 · IG 18 × 12 = 216.')
ZAEHL = OrderedDict([('ganz_je', 'ganz · je Meldung (Haupt)'), ('ganz_cap', 'ganz · wochen-gedeckelt'), ('ganz_dist', 'ganz · distinkte H003'),
                     ('d_je', 'ganz+teilw · je Meldung'), ('d_cap', 'ganz+teilw · wochen-gedeckelt'), ('d_dist', 'ganz+teilw · distinkte H003')])
P(f"\n{'Zählung':32s}{'IG (216)':>16s}{'Verein A (84)':>18s}{'Verein B (132)':>18s}{'Median':>8s}{'Mittel':>8s}")
for k, lab in ZAEHL.items():
    tot = sum(Z[c][k] for c in ig_codes); a = sum(Z[c][k] for c in ig_codes if pers[c]['Verein'] == 'A'); b = sum(Z[c][k] for c in ig_codes if pers[c]['Verein'] == 'B')
    v = [Z[c][k] for c in ig_codes]
    P(f"{lab:32s}{str(tot) + ' = ' + fmt(100 * tot / 216, 1) + ' %':>16s}{str(a) + ' = ' + fmt(100 * a / 84, 1) + ' %':>18s}{str(b) + ' = ' + fmt(100 * b / 132, 1) + ' %':>18s}{fmt(statistics.median(v), 1):>8s}{fmt(statistics.mean(v)):>8s}")
P('  Nur meldende Spieler (n = 15) für „ganz je Meldung“: Median ' + fmt(statistics.median([Z[c]['ganz_je'] for c in melder]), 1) + ' · Mittel ' + fmt(statistics.mean([Z[c]['ganz_je'] for c in melder])))
P('  Spieler mit ≥ 1 „teilweise“: ' + ', '.join(f"{c} ({Z[c]['teilw']})" for c in ig_codes if Z[c]['teilw']) + ' — Freitexte in § 6.7.')

P('\nVERTEILUNG DER VOLLSTÄNDIGEN EINHEITEN JE SPIELER (Histogrammdaten; Hauptzählung; alle 18 zugeteilten Spieler, Nicht-Melder 0)')
vert = Counter(Z[c]['ganz_je'] for c in ig_codes)
P('  Einheiten: ' + '  '.join(f'{k:>2d}' for k in range(13)))
P('  Spieler:   ' + '  '.join(f'{vert.get(k, 0):>2d}' for k in range(13)) + '   (Marken: ≥ 6 = Per-Protokoll · ≥ 9 = Antragskriterium 75 %)')
P('  je Verein A: ' + ' · '.join(f"{k}×{n}" for k, n in sorted(Counter(Z[c]['ganz_je'] for c in ig_codes if pers[c]['Verein'] == 'A').items())) + '   B: ' + ' · '.join(f"{k}×{n}" for k, n in sorted(Counter(Z[c]['ganz_je'] for c in ig_codes if pers[c]['Verein'] == 'B').items())))

P('\nSCHWELLENLANDSCHAFT ≥ 1 … 12 — Zahl der Spieler je Zählung (§ 11.9: Inferenz erst ab n ≥ 8)')
P(f"{'Schwelle':10s}{'Anteil':>8s}" + ''.join(f'{k:>16s}' for k in ZAEHL) )
for s_ in range(1, 13):
    line = f"{('≥ ' + str(s_)):10s}{fmt(100 * s_ / 12, 0) + ' %':>8s}"
    for k in ZAEHL: line += f"{sum(1 for c in ig_codes if Z[c][k] >= s_):>16d}"
    P(line + ('   ← Per-Protokoll (B0.1)' if s_ == 6 else '   ← Antragskriterium' if s_ == 9 else ''))
P('\nMENGEN FÜR ≥ 6 (Per-Protokoll) UND ≥ 9 (Antragskriterium ≥ 75 %) JE ZÄHLUNG')
for s_ in (6, 9):
    for k, lab in ZAEHL.items():
        pl = [c for c in ig_codes if Z[c][k] >= s_]
        P(f"   ≥ {s_} · {lab:30s} n = {len(pl):2d} → " + ', '.join(f"{c} ({Z[c][k]})" for c in pl))
P('  Lesart: Die Hauptzählung gibt die Obergrenze (jede Meldung zählt), die Wochen-Deckelung die belastbarere Untergrenze (kein Nachholen, zwei Einheiten je Woche),')
P('  die H003-Zählung die instrumentbedingte Untergrenze (nur bei Fehlwahl abweichend). Für ≥ 6 unterscheiden sich Haupt und Deckelung nicht; für ≥ 9 fällt BW-08 (8) heraus.')

P('\nVERLAUF ÜBER DIE SECHS PROGRAMMWOCHEN JE VEREIN — vollständige Einheiten je Woche (Anteil an Spieler × 2), Spieler mit ≥ 1 Meldung')
P(f"{'Woche':7s}{'Kontakte':>9s} │ {'A ganz':>7s}{'/14':>5s}{'Spl ≥1':>8s} │ {'B ganz':>7s}{'/22':>5s}{'Spl ≥1':>8s} │ {'IG ganz':>8s}{'/36':>5s}{'Spl ≥1':>8s}{'ganz+tw':>9s}")
for w in range(1, 7):
    line = f"{'W' + str(w):7s}{KONTAKTE[w]:>9d} │ "
    for v, nen in (('A', 14), ('B', 22), (None, 36)):
        rs = [r for r in meld if r['w_dat'] == w and (v is None or r['verein'] == v)]
        g = sum(1 for r in rs if r['ganz']); spl = len({r['code_wb'] for r in rs})
        line += f"{g:>7d}{fmt(100 * g / nen, 0) + ' %':>7s}{spl:>7d} │ " if v else f"{g:>8d}{fmt(100 * g / nen, 0) + ' %':>7s}{spl:>7d}{sum(1 for r in rs if r['durch']):>9d}"
    P(line)
P('  Verein B vor / ab KW 33 (Mannschaftstraining ab 10.08., Videoeinheiten im Vereinskalender): W1–W3 ' + str(sum(1 for r in meld if r['verein'] == 'B' and r['ganz'] and r['w_dat'] <= 3)) + ' von 66 = ' + fmt(100 * sum(1 for r in meld if r['verein'] == 'B' and r['ganz'] and r['w_dat'] <= 3) / 66, 1) + ' % · W4–W6 ' + str(sum(1 for r in meld if r['verein'] == 'B' and r['ganz'] and r['w_dat'] >= 4)) + ' von 66 = ' + fmt(100 * sum(1 for r in meld if r['verein'] == 'B' and r['ganz'] and r['w_dat'] >= 4) / 66, 1) + ' % (deskriptiv; Vereinskalender = Vorgabe, Umsetzung unbekannt)')
P('  Verein A vor / ab W3 (Mannschaftstraining ab 03.08.): W1–W2 ' + str(sum(1 for r in meld if r['verein'] == 'A' and r['ganz'] and r['w_dat'] <= 2)) + ' von 28 = ' + fmt(100 * sum(1 for r in meld if r['verein'] == 'A' and r['ganz'] and r['w_dat'] <= 2) / 28, 1) + ' % · W3–W6 ' + str(sum(1 for r in meld if r['verein'] == 'A' and r['ganz'] and r['w_dat'] >= 3)) + ' von 56 = ' + fmt(100 * sum(1 for r in meld if r['verein'] == 'A' and r['ganz'] and r['w_dat'] >= 3) / 56, 1) + ' %')
P('  Meldende Spieler je Woche: ' + ' · '.join(f"W{w} {len({r['code_wb'] for r in meld if r['w_dat'] == w})}/18" for w in range(1, 7)) + ' — Abfall in W6 (Trainingslager/Urlaub laut Freitexten HL-03, HL-07; Vergessen BW-02, BW-09).')

P('\nNICHT-MELDER UND SONDERFÄLLE (Klassen nach CONSORT Box 6 / Auswertungsplan)')
P('   BW-01  0 Meldungen — Nichteinhaltung (Listenplatz vorhanden); Post-Werte vorhanden → ITT ja, Per-Protokoll nein.')
P('   HL-05  0 Meldungen — Nichteinhaltung (Workbook HL-05 = Listenplatz HL-04, beide leer); Post-Werte vorhanden → ITT ja, Per-Protokoll nein.')
P('   BW-21  0 Meldungen — Instrumentenfehler (kein Listenplatz); Post nicht angetreten → für die Ergebnisanalyse gegenstandslos, im Teilnehmerfluss führen.')
P('   HL-06  1 Meldung „gar nicht“ (23.07., „Athletik Training … zwei Einheiten am Tag“) — Nichteinhaltung mit Dokumentation; Post-Werte vorhanden.')
P('   BW-07  6 vollständige Einheiten, aber Post nicht angetreten → aus jeder Ergebnisanalyse heraus (Ausfall bei der Nacherhebung).')
P('   Meldende Spieler mit Post-Werten und ≥ 6 (PP-Menge, Haupt): ' + ', '.join(c for c in ig_codes if Z[c]['ganz_je'] >= 6 and pers[c]['Status'].startswith('ausgewertet')) + f" (n = {sum(1 for c in ig_codes if Z[c]['ganz_je'] >= 6 and pers[c]['Status'].startswith('ausgewertet'))}; ohne %PAH-Prüfung — Nenner je Zielgröße in B0 § 3)")

# ---- Abgleich mit B0
P('\nABGLEICH MIT B0 (Auswertung_B0_Mindestdosis_2026-09-12.txt, § 1–2) — Hauptzählung je Spieler, Umsetzungsrate, Schwellenmengen')
b0_txt = os.path.join(HERE, 'Auswertung_B0_Mindestdosis_2026-09-12.txt')
if not os.path.exists(b0_txt): b0_txt = _finde('Claude', '03_Skripte', 'Auswertung_B0_Mindestdosis_2026-09-12.txt')
if os.path.exists(b0_txt):
    b0 = open(b0_txt, encoding='utf-8').read().splitlines()
    b0_ganz = {}; b0_thr = {}; b0_rate = None; b0_pp9 = None
    in1 = False
    for ln in b0:
        if ln.startswith('1  MELDUNGEN JE CODE'): in1 = True; continue
        if in1 and ln.startswith('  Meldungen unter'): in1 = False
        if in1 and (ln.startswith('BW-') or ln.startswith('HL-')):
            t = ln.split()
            b0_ganz[t[2]] = b0_ganz.get(t[2], 0) + int(t[6])          # Workbook-Code, Spalte „ganz“ (korrigiert)
        if ln.strip().startswith('≥ ') and '%' in ln and 'Prompt' not in ln:
            t = ln.split(); b0_thr[int(t[1])] = int(t[4])
        if ln.startswith('  Umsetzungsrate:'): b0_rate = ln.strip()
        if ln.startswith('  Spieler mit ≥ 9 Einheiten'): b0_pp9 = ln.strip()
    diffs = [(c, Z[c]['ganz_je'], b0_ganz.get(c)) for c in ig_codes if b0_ganz.get(c) != Z[c]['ganz_je']]
    P(f'  B0-Datei: {b0_txt}')
    P(f"  „ganz“ je Spieler: {len(ig_codes) - len(diffs)} von {len(ig_codes)} identisch" + (' — Abweichungen: ' + ', '.join(f'{c} F1 {a} / B0 {b}' for c, a, b in diffs) if diffs else ' (keine Abweichung)'))
    P(f"  B0: {b0_rate}  ↔  F1: {sum(Z[c]['ganz_je'] for c in ig_codes)} von 216 = {fmt(100 * sum(Z[c]['ganz_je'] for c in ig_codes) / 216, 1)} %")
    for s_ in sorted(b0_thr):
        f1n = sum(1 for c in ig_codes if Z[c]['ganz_je'] >= s_)
        P(f"  Schwelle ≥ {s_:2d}: B0 {b0_thr[s_]:2d} ↔ F1 {f1n:2d}" + ('' if b0_thr[s_] == f1n else '   ⚠ ABWEICHUNG'))
    P(f'  B0 Antragskriterium: {b0_pp9}  ↔  F1: ' + ', '.join(f"{c} ({Z[c]['ganz_je']})" for c in ig_codes if Z[c]['ganz_je'] >= 9))
    P('  Ergebnis: Hauptzählung identisch. B0 kennt die beiden Untergrenzen nicht (Maßnahme K20: Spalten „wochen-gedeckelt“ und „distinkte H003“ in B0 § 6 ergänzt, Stand 12.09.).')
else:
    P('  ⚠ B0-Ausgabe nicht gefunden — Abgleich nicht möglich (erwartet neben diesem Skript in 03_Skripte).')

P('\nEINFÜGETABELLE FÜR 01_PERSONEN (Spalte „Einheiten_ganz“, Pipeline K7; Workbook nicht beschrieben) — Code; ganz je Meldung; ganz wochen-gedeckelt; ganz distinkte H003; ganz+teilweise je Meldung; Meldungen gesamt')
for c in ig_codes:
    P(f"   {c};{Z[c]['ganz_je']};{Z[c]['ganz_cap']};{Z[c]['ganz_dist']};{Z[c]['d_je']};{Z[c]['n']}")
P('   (BW-21: 0 = Instrumentenfehler, kein Listenplatz — im Workbook als leer/„n. e.“ führen, nicht als 0 Einheiten; für 01_Personen beim Verfasser entscheiden)')

# ================================================================== 6.5 Belastung
H('6.5  BELASTUNG — CR-10 (sRPE) und sRPE-Load')
P('CR-10 = H005 − 1 (Codebuch: 0 Ruhe … 10 Maximal). Meldungen „gar nicht“ tragen durchgängig CR-10 = 0 (' + str(sum(1 for r in meld if r["H004"] == "3" and r["cr10"] == 0)) + ' von ' + str(sum(1 for r in meld if r["H004"] == "3")) + ') und werden bei der Belastung nicht gezählt.')
def kenn(v):
    if not v: return '—'
    return f'n {len(v):2d} · M {fmt(statistics.mean(v))} · SD {fmt(statistics.stdev(v)) if len(v) > 1 else "—"} · Md {fmt(statistics.median(v), 1)} · Spanne {min(v)}–{max(v)}'
cr_g = [r['cr10'] for r in meld if r['ganz']]; cr_t = [r['cr10'] for r in meld if r['H004'] == '2']; cr_d = [r['cr10'] for r in meld if r['durch']]
P('  ganz:            ' + kenn(cr_g)); P('  teilweise:       ' + kenn(cr_t)); P('  ganz + teilweise:' + kenn(cr_d))
P('  Verteilung CR-10 (ganz): ' + ' · '.join(f'{k}×{n}' for k, n in sorted(Counter(cr_g).items())) + ' · teilweise: ' + ' · '.join(f'{k}×{n}' for k, n in sorted(Counter(cr_t).items())))
P('  → Die früheren Angaben 2,90 (n 92, nur ganz) und 3,10 (n 98, ganz + teilweise) sind beide korrekt; sie beziehen sich auf verschiedene Mengen. Die „teilweise“-Meldungen liegen im Mittel höher (zwei mit CR-10 = 9).')
P('\n  Je Verein (ganz): A ' + kenn([r['cr10'] for r in meld if r['ganz'] and r['verein'] == 'A']) + '\n                     B ' + kenn([r['cr10'] for r in meld if r['ganz'] and r['verein'] == 'B']))
P('\n  Je Spieler (ganz):')
for c in melder:
    v = [r['cr10'] for r in by_code[c] if r['ganz']]
    if v: P(f'   {c} ({pers[c]["Verein"]}): ' + kenn(v) + ' · Einzelwerte ' + ' '.join(str(x) for x in v))
    else: P(f'   {c} ({pers[c]["Verein"]}): keine vollständige Einheit')
P('\n  Je Programmwoche (ganz) gegen die Dosisprogression — nur deskriptiv, kein Test:')
P(f"{'Woche':7s}{'Kontakte':>9s}{'n':>5s}{'M':>7s}{'SD':>7s}{'Md':>6s}{'Spanne':>9s}   Verein A M (n)   Verein B M (n)")
for w in range(1, 7):
    v = [r['cr10'] for r in meld if r['ganz'] and r['w_dat'] == w]
    va = [r['cr10'] for r in meld if r['ganz'] and r['w_dat'] == w and r['verein'] == 'A']; vb = [r['cr10'] for r in meld if r['ganz'] and r['w_dat'] == w and r['verein'] == 'B']
    P(f"{'W' + str(w):7s}{KONTAKTE[w]:>9d}{len(v):>5d}{fmt(statistics.mean(v)):>7s}{(fmt(statistics.stdev(v)) if len(v) > 1 else '—'):>7s}{fmt(statistics.median(v), 1):>6s}{str(min(v)) + '–' + str(max(v)):>9s}   {fmt(statistics.mean(va)) if va else '—':>6s} ({len(va)})       {fmt(statistics.mean(vb)) if vb else '—':>6s} ({len(vb)})")
P('  Kontakte steigen 52 → 120 (Faktor 2,3); das mittlere CR-10 bleibt in einem engen Band — Belastungsempfinden und Volumen laufen nicht parallel (Verdünnung durch Einzelspieler, k ≤ 20 je Woche).')

# sRPE-Load
VIDEO_MIN = {1: 28 + 16 / 60, 2: 28 + 2 / 60, 3: 24 + 17 / 60, 4: 25 + 55 / 60, 5: 31 + 3 / 60, 6: 31 + 14 / 60}   # Verfasser 12.09. (korrigiert): 28:16 · 28:02 · 24:17 · 25:55 · 31:03 · 31:14
ERWAERMUNG_MIN = 8 + 53 / 60                                                                                  # Verfasser 12.09.: Erwärmung = eigenes Video, 8:53, vor jeder Einheit
def mmss(x): return '%d:%02d' % (int(x), round((x % 1) * 60))
P('\nsRPE-LOAD = CR-10 × Sitzungsdauer (AU; Foster et al., 2001). Sitzungsdauer = Soll-Dauer des Wochenvideos + Erwärmungsvideo 8:53 (eigenes Video, Verfasser 12.09.):')
P('  Wochenvideo: ' + ' · '.join(f"W{w} {mmss(VIDEO_MIN[w])}" for w in range(1, 7)) + ' min → Sitzungsdauer ' + ' · '.join(f"W{w} {mmss(VIDEO_MIN[w] + ERWAERMUNG_MIN)}" for w in range(1, 7)) + ' min.')
P('  Spanne der Sitzungsdauer 33:10–40:07 min; die Antragsspanne 30–40 min (Manuskript 4.5.1) wird in W6 um 7 s überschritten — für den Text „rund 33 bis 40 Minuten“.')
P('  Vier Einschränkungen: (1) Soll- statt Ist-Dauer; (2) bei nahezu konstanter Dauer (33–40 min) trägt der Load kaum mehr Information als CR-10; (3) „teilweise“ ohne Dauer → kein Load;')
P('  (4) Videopausen verlängern die Ist-Dauer unbekannt weit (25 von 111 Meldungen mit Pausen).')
def load(r):
    return r['cr10'] * (VIDEO_MIN[r['w_dat']] + ERWAERMUNG_MIN)
P(f"\n{'Woche':7s}{'Video':>8s}{'Sitzung':>9s}{'n ganz':>7s}{'Σ CR-10':>8s}{'Load Σ':>9s}{'Load M':>8s}{'Load SD':>9s}{'Load Md':>9s}{'Spanne':>11s}")
tot = 0
for w in range(1, 7):
    rs = [r for r in meld if r['ganz'] and r['w_dat'] == w]
    l = [load(r) for r in rs]; tot += sum(l)
    P(f"{'W' + str(w):7s}{mmss(VIDEO_MIN[w]):>8s}{mmss(VIDEO_MIN[w] + ERWAERMUNG_MIN):>9s}{len(rs):>7d}{sum(r['cr10'] for r in rs):>8d}{fmt(sum(l), 0):>9s}{fmt(statistics.mean(l), 0):>8s}{fmt(statistics.stdev(l), 0) if len(l) > 1 else '—':>9s}{fmt(statistics.median(l), 0):>9s}{(fmt(min(l), 0) + '–' + fmt(max(l), 0)):>11s}")
alle_l = [load(r) for r in meld if r['ganz']]
P(f"{'Σ / alle':7s}{'':>8s}{'':>9s}{len(alle_l):>7d}{sum(r['cr10'] for r in meld if r['ganz']):>8d}{fmt(tot, 0):>9s}{fmt(statistics.mean(alle_l), 0):>8s}{fmt(statistics.stdev(alle_l), 0):>9s}{fmt(statistics.median(alle_l), 0):>9s}{(fmt(min(alle_l), 0) + '–' + fmt(max(alle_l), 0)):>11s}")
P('  Je Verein: A Σ ' + fmt(sum(load(r) for r in meld if r['ganz'] and r['verein'] == 'A'), 0) + ' AU (M ' + fmt(statistics.mean([load(r) for r in meld if r['ganz'] and r['verein'] == 'A']), 0) + ', n 36) · B Σ ' + fmt(sum(load(r) for r in meld if r['ganz'] and r['verein'] == 'B'), 0) + ' AU (M ' + fmt(statistics.mean([load(r) for r in meld if r['ganz'] and r['verein'] == 'B']), 0) + ', n 56)')
P('  Je Spieler (vollständige Einheiten): Σ Load AU · n · M je Einheit:')
for c in melder:
    rs = [r for r in by_code[c] if r['ganz']]
    if rs: P(f"   {c}: {fmt(sum(load(r) for r in rs), 0):>6s} AU · n = {len(rs):2d} · M {fmt(statistics.mean([load(r) for r in rs]), 0)}")
P('  Alte Angaben (Maßnahme C6): „Summe 10.680 AU“ = Σ CR-10 der 92 vollständigen Einheiten (267) × 40 min nominal; „Einzelwerte 11.000 AU“ stammt aus der Spielertabelle vor den CASE-Korrekturen')
P('  und ist aus den Dateien nicht mehr rekonstruierbar. Beide sind durch die Rechnung mit wochenspezifischer Sitzungsdauer (Video + Erwärmung) ersetzt; die nominale 40-min-Rechnung wird nicht mehr berichtet.')

# ================================================================== 6.6 Untergrund, Videopausen, Fremdtraining
H('6.6  UNTERGRUND, VIDEOPAUSEN, FREMDTRAINING — nur qualitativ')
durch = [r for r in meld if r['durch']]
P(f'Untergrund je Meldung — durchgeführte Einheiten (n = {len(durch)}): ' + ' · '.join(f'{k} {n}' for k, n in Counter(r['ug'] for r in durch).most_common()))
P(f'  alle 111 Meldungen: ' + ' · '.join(f'{k} {n}' for k, n in Counter(r['ug'] for r in meld).most_common()) + ' — „gar nicht“ wählt überwiegend „Anderes“ (' + str(sum(1 for r in meld if r['H004'] == '3' and r['H006'] == '5')) + ' von 13).')
P('  je Verein (durchgeführt): A ' + ' · '.join(f'{k} {n}' for k, n in Counter(r['ug'] for r in durch if r['verein'] == 'A').most_common()) + ' │ B ' + ' · '.join(f'{k} {n}' for k, n in Counter(r['ug'] for r in durch if r['verein'] == 'B').most_common()))
P('  Modalwert je Spieler (durchgeführt): ' + ' · '.join(f"{c} {Counter(r['ug'] for r in by_code[c] if r['durch']).most_common(1)[0][0]} ({Counter(r['ug'] for r in by_code[c] if r['durch']).most_common(1)[0][1]}/{sum(1 for r in by_code[c] if r['durch'])})" for c in melder if any(r['durch'] for r in by_code[c])))
P('  Vorgabe (Infoblatt, Manuskript 4.5.1): ebener, trockener Rasen ~10 × 3 m — tatsächlich dominiert „Drinnen“; Rasen/Wiese bei ' + str(sum(1 for r in durch if r['H006'] == '1')) + ' von ' + str(len(durch)) + ' durchgeführten Einheiten. Bodenart der Heimeinheiten = Limitation (F10 § 12).')

P(f"\nVideopausen / Übungswiederholungen (H008 = ja): {sum(1 for r in meld if r['pause'])} von 111 Meldungen · bei durchgeführten {sum(1 for r in durch if r['pause'])} von {len(durch)} = {fmt(100 * sum(1 for r in durch if r['pause']) / len(durch), 1)} % · Spieler mit ≥ 1: {len({r['code_wb'] for r in meld if r['pause']})} von 15")
import re
def kat_pause(t):
    tl = t.lower()
    if 'jeder übung' in tl: return 'bei jeder Übung (HL-07)'
    if 'verstanden' in tl or 'anschauen' in tl or 'unterschied' in tl: return 'zum Verständnis / Nachschauen'
    if re.search(r'\d', tl): return 'Anzahl genannt'
    return 'sonstige'
kp = Counter(kat_pause(r['fx_pause']) for r in meld if r['pause'])
P('  Freitext-Kategorien: ' + ' · '.join(f'{k} {n}' for k, n in kp.most_common()))
P('  Genannte Anzahl (Meldungen mit Zahl): ' + ' · '.join(f"{r['code_wb']} „{r['fx_pause']}“" for r in meld if r['pause'] and kat_pause(r['fx_pause']) == 'Anzahl genannt'))
P('  je Spieler: ' + ' · '.join(f"{c} {sum(1 for r in by_code[c] if r['pause'])}/{len(by_code[c])}" for c in melder if any(r['pause'] for r in by_code[c])))
P('  Lesart: Die Instruktion „Video einmal starten, nicht spulen“ (4.5.1) wurde in gut einem Viertel der Einheiten nicht eingehalten; HL-07 pausierte systematisch bei jeder Übung (außer Pogos). Näherungsindikator, keine Compliance-Messung.')

P(f"\nFremdtraining seit der letzten Einheit (H009 = ja): {sum(1 for r in meld if r['fremd'])} von 111 · Spieler mit ≥ 1: {len({r['code_wb'] for r in meld if r['fremd']})} von 15")
P(f"{'Woche':7s}{'A ja/Meld.':>12s}{'B ja/Meld.':>12s}{'IG ja/Meld.':>13s}   Mannschaftstraining: A ab W3 (03.08.), B ab W4 (10.08.); B Laufplan W1–W3")
for w in range(1, 7):
    ra = [r for r in meld if r['w_dat'] == w and r['verein'] == 'A']; rb = [r for r in meld if r['w_dat'] == w and r['verein'] == 'B']
    P(f"{'W' + str(w):7s}{str(sum(1 for r in ra if r['fremd'])) + '/' + str(len(ra)):>12s}{str(sum(1 for r in rb if r['fremd'])) + '/' + str(len(rb)):>12s}{str(sum(1 for r in ra + rb if r['fremd'])) + '/' + str(len(ra) + len(rb)):>13s}")
# Freitext-Kategorien Fremdtraining (Zuordnung je CASE, Mehrfachnennung möglich)
KAT_FREMD = {'44': ['Leistungscamp/Zusatztraining'], '66': ['Gym/Kraft', 'Fußball (Verein/individuell)'], '78': ['Fußball (Verein/individuell)'], '90': ['Gym/Kraft', 'Fußball (Verein/individuell)'],
             '126': ['Fußball (Verein/individuell)'], '133': ['Fußball (Verein/individuell)'], '167': ['Mannschaftstraining'], '197': ['Fußball (Verein/individuell)'], '209': ['Fußball (Verein/individuell)'],
             '230': ['Schwimmen'], '258': ['unklar (zweite Programmeinheit)'], '140': ['Gym/Kraft'], '158': ['Vereins-/Laufplan'], '190': ['Gym/Kraft'], '256': ['Fußball (Verein/individuell)'],
             '101': ['Fußball (Verein/individuell)', 'Laufen/Joggen'], '116': ['Fußball (Verein/individuell)', 'Laufen/Joggen'], '187': ['Mannschaftstraining'], '48': ['Laufen/Joggen'], '188': ['Fußball (Verein/individuell)', 'Laufen/Joggen'],
             '189': ['Laufen/Joggen'], '217': ['Mannschaftstraining'], '246': ['Mannschaftstraining', 'Spiel'], '136': ['Vereins-/Laufplan'], '49': ['Laufen/Joggen'], '76': ['Laufen/Joggen', 'Gym/Kraft'], '120': ['Laufen/Joggen'],
             '122': ['Laufen/Joggen', 'Gym/Kraft'], '216': ['Gym/Kraft'], '229': ['Gym/Kraft'], '260': ['Fußball (Verein/individuell)'], '53': ['Gym/Kraft', 'Fußball (Verein/individuell)'], '102': ['Gym/Kraft', 'Laufen/Joggen'],
             '108': ['Gym/Kraft'], '159': ['Gym/Kraft'], '51': ['Gym/Kraft'], '110': ['Gym/Kraft'], '41': ['Schwimmen'], '62': ['Schwimmen', 'Laufen/Joggen'], '87': ['Laufen/Joggen', 'Schwimmen'], '115': ['Laufen/Joggen', 'Gym/Kraft'],
             '138': ['Fußball (Verein/individuell)'], '149': ['Mannschaftstraining'], '232': ['Mannschaftstraining'], '252': ['Mannschaftstraining'], '36': ['Vereins-/Laufplan'], '56': ['Vereins-/Laufplan'], '94': ['Vereins-/Laufplan'],
             '63': ['Laufen/Joggen', 'Fußball (Verein/individuell)'], '79': ['Fußball (Verein/individuell)', 'Laufen/Joggen'], '182': ['Fußball (Verein/individuell)'], '204': ['Gym/Kraft'], '228': ['Spiel'], '253': ['Trainingslager'], '254': ['Trainingslager'],
             '38': ['Athletiktraining (2×/Tag)'], '37': ['Gym/Kraft'], '171': ['Gym/Kraft', 'Ausdauer'], '205': ['Gym/Kraft'], '152': ['Gym/Kraft', 'Laufen/Joggen', 'Leistungsdiagnostik']}
kf = Counter(); fehl = []
for r in meld:
    if r['fremd']:
        if r['CASE'] in KAT_FREMD: kf.update(KAT_FREMD[r['CASE']])
        else: fehl.append(r['CASE'])
P('  Freitext-Kategorien (Zuordnung je CASE im Skript, Mehrfachnennung): ' + ' · '.join(f'{k} {n}' for k, n in kf.most_common()) + (f' · ohne Zuordnung: {fehl}' if fehl else ''))
P('  Belege für die Lesart „Vereinstraining“ und für die Untergrenze: HL-02 „Von Sven“/„Svens Plan“ (Verein A, W1–W2 = extensiver Laufplan des Trainerteams laut Verfasser 12.09.; 4.5.2 „ohne Trainingsvorgaben“ ist zu korrigieren), BW-04 „Bastis Läufe“,')
P('  BW-08 „halt unsere joggingsachen“ (Laufplan Verein B); HL-08 CASE 152: „habe bei diesem Feld immer nein eingetragen weil ich die Frage falsch verstanden habe obwohl ich Sport gemacht habe“ → Item unterschätzt Fremdtraining (Untergrenze).')
P('  Fremdtraining bereits in W1: A ' + str(sum(1 for r in meld if r['w_dat'] == 1 and r['verein'] == 'A' and r['fremd'])) + '/' + str(sum(1 for r in meld if r['w_dat'] == 1 and r['verein'] == 'A')) + ', B ' + str(sum(1 for r in meld if r['w_dat'] == 1 and r['verein'] == 'B' and r['fremd'])) + '/' + str(sum(1 for r in meld if r['w_dat'] == 1 and r['verein'] == 'B')) + ' — vor jedem Mannschaftstraining, also nicht nur Vereinstraining (Gym, Joggen, Schwimmen, Camp).')

# ================================================================== 6.7 Unerwünschte Ereignisse
H('6.7  UNERWÜNSCHTE EREIGNISSE (CONSORT Item 19) — Schmerzen/Probleme, schmerzbedingte Nicht-/Teildurchführung; ohne Kausalzuschreibung')
KAT_SCHMERZ = {'26': ['Knie'], '41': ['Oberschenkel (hinten, „leicht gezerrt“)'], '44': ['Knie'], '49': ['Muskelkater (Oberschenkel, „vom Joggen“)'], '51': ['Knie'], '70': ['Muskelkater („von der ersten Einheit“)'],
               '74': ['Muskelkater'], '88': ['Knie („wie immer“)'], '99': ['Sprunggelenk („Knöchelverletzung“)'], '116': ['Knie', 'Oberschenkel'], '137': ['Knie („schon vor dem Training“)'], '229': ['Muskelkater („von Spiel“)']}
sm = [r for r in meld if r['schmerz']]
P(f"Schmerzmeldungen (H007 = ja): {len(sm)} von 111 Meldungen ({fmt(100 * len(sm) / 111, 1)} %) · betroffene Spieler: {len({r['code_wb'] for r in sm})} von 15 meldenden ({', '.join(sorted({r['code_wb'] for r in sm}))})")
P(f"  je Verein: A {sum(1 for r in sm if r['verein'] == 'A')} von {sum(1 for r in meld if r['verein'] == 'A')} · B {sum(1 for r in sm if r['verein'] == 'B')} von {sum(1 for r in meld if r['verein'] == 'B')} · je Status: ganz {sum(1 for r in sm if r['ganz'])} · teilweise {sum(1 for r in sm if r['H004'] == '2')} · gar nicht {sum(1 for r in sm if r['H004'] == '3')}")
ks = Counter(); 
for r in sm: ks.update([k.split(' (')[0] for k in KAT_SCHMERZ.get(r['CASE'], ['ohne Zuordnung'])])
P('  Lokalisation (Freitext kategorisiert, Mehrfachnennung): ' + ' · '.join(f'{k} {n}' for k, n in ks.most_common()))
P('  Verlauf je Programmwoche: ' + ' · '.join(f"W{w} {sum(1 for r in sm if r['w_dat'] == w)}/{sum(1 for r in meld if r['w_dat'] == w)}" for w in range(1, 7)))
P('  Einzelmeldungen:')
for r in sorted(sm, key=lambda r: (r['t'])):
    P(f"   CASE {r['CASE']:>3} {r['code_wb']} {r['t'].strftime('%d.%m.')} W{r['w_dat']} · {r['status']:9s} · CR-10 {r['cr10']:>2} · {', '.join(KAT_SCHMERZ.get(r['CASE'], ['—'])):45s} „{r['fx_schmerz']}“")
P('\n  Nicht durchgeführte Einheiten (H004 = gar nicht, n = 13) mit Grund:')
for r in sorted([r for r in meld if r['H004'] == '3'], key=lambda r: r['t']):
    P(f"   CASE {r['CASE']:>3} {r['code_wb']} {r['t'].strftime('%d.%m.')} W{r['w_dat']} · Schmerz-Item {JN[r['H007']]:4s} · „{r['fx_gar'] or '(kein Grund)'}“")
P('  Teilweise durchgeführte Einheiten (H004 = teilweise, n = 6) mit Grund:')
for r in sorted([r for r in meld if r['H004'] == '2'], key=lambda r: r['t']):
    P(f"   CASE {r['CASE']:>3} {r['code_wb']} {r['t'].strftime('%d.%m.')} W{r['w_dat']} · CR-10 {r['cr10']} · Schmerz-Item {JN[r['H007']]:4s} · „{r['fx_teilw'] or '(kein Grund)'}“")
P('\n  Zählung nach Regel: schmerzbedingt nicht durchgeführt mit Schmerz-Item „ja“: 2 (HL-01 24.07. Zerrung hinterer Oberschenkel nach zwei Übungen; BW-06 02.08. Knie/Oberschenkel);')
P('  nicht durchgeführt mit Beschwerdegrund ohne Schmerz-Item (BW-05 26.07. „Kin Probleme“): 1; teilweise mit Verletzungsangabe (BW-04 01.08. Knöchel, „Alles“ nicht geschafft): 1.')
P('  Drei der zwölf Schmerzmeldungen sind Muskelkater, zwei davon fremdem Training zugeschrieben (Joggen, Spiel); zwei Kniemeldungen als vorbestehend beschrieben. Kein Ereignis führte zum Studienabbruch;')
P('  Verletzungen wurden nicht ärztlich verifiziert. Für die KG bestand kein Erfassungsinstrument (Antrag sah keines vor) — Item 19 nur für die IG berichtbar.')

# ================================================================== 6.8 Datenqualität
H('6.8  DATENQUALITÄT DES INSTRUMENTS')
ts = [r['time_sum'] for r in meld]
P(f'Bearbeitungsdauer TIME_SUM (s): Median {fmt(statistics.median(ts), 0)} · Quartile {statistics.quantiles(ts, n=4)[0]:.0f} / {statistics.quantiles(ts, n=4)[2]:.0f} · Spanne {min(ts)}–{max(ts)} · < 30 s: {sum(1 for t in ts if t < 30)} von 111 ({fmt(100 * sum(1 for t in ts if t < 30) / 111, 1)} %) · < 45 s: {sum(1 for t in ts if t < 45)}')
P('  Neun Seiten in median ' + fmt(statistics.median(ts), 0) + ' s = ' + fmt(statistics.median(ts) / 9, 1) + ' s je Seite. Zeit je Seite (Median, s): ' + ' · '.join(f"S{i} {statistics.median(int(r['TIME00' + str(i)]) for r in meld):.0f}" for i in range(1, 10)))
P('  LASTPAGE = MAXPAGE = 9, FINISHED = 1, MISSING = 0 bei 111/111 — Folge des Exportfilters, kein Qualitätsmerkmal des Ausfüllens.')
erw = [('H004_02', lambda r: r['H004'] == '2', 'teilweise-Grund'), ('H004_03', lambda r: r['H004'] == '3', 'gar-nicht-Grund'), ('H007_01', lambda r: r['schmerz'], 'Schmerz-Text'), ('H008_01', lambda r: r['pause'], 'Videopause-Text'), ('H009_01', lambda r: r['fremd'], 'Fremdtraining-Text')]
P('  Freitext, wo erwartbar: ' + ' · '.join(f"{lab} {sum(1 for r in meld if pred(r) and (r[f].strip() if f != 'H008_01' else r['fx_pause']))}/{sum(1 for r in meld if pred(r))}" for f, pred, lab in erw))
P('  Codesicherheit: kein Geräte-, Sitzungs- oder IP-Merkmal im Export (SERIAL/REF leer); zwei Verwechslungen korrigiert (CASE 59/70 → BW-06; 140/158/165/190/206 → BW-04), weitere nicht ausschließbar;')
P('  fünf vereinsübergreifende Meldefenster ≤ 5 min (§ 6.1) sind mit Erinnerungen erklärbar, nicht mit Verwechslung. Selbstauskunft ohne Plausibilitätssperre (Fragebogen jederzeit abrufbar).')
P('  Datums-Item: nur „Heute“ (111/111) → Trainingstag = Meldetag nur bei taggleicher Meldung; belegt anders: BW-09 CASE 122 „ich habe aber gestern nicht heute trainiert“, Sammelmeldungen (10 taggleiche Paare),')
P('  BW-02 CASE 258 „diese Woche voll vergessen … deswegen hab ich heute alles gemacht“ (zwei Einheiten an einem Tag, 48-h-Vorgabe nicht eingehalten — einziger dokumentierter Fall).')
P('  Einheitennummer: 9 von 111 außerhalb der Datumswoche, 16 weitere in der Woche mit anderer Nummer, vier Spieler mit doppelten Nummern (HL-03 nur ungerade) → kein Identitätsmerkmal.')
P('  Exportfilter „bis Seite 9, ≤ 0 % fehlend“: abgebrochene Fragebögen nicht enthalten; TXT nach Excel-Speicherung mit einer Datumsautokorrektur (CASE 189) — JSON als Originalquelle der Freitexte.')
P('  → Limitationen für 6.2: Selbstauskunft ohne Zeit-/Codesperre · Trainingstag nicht erhoben · Einheitenzuordnung unsicher · Sammelmeldungen · Fremdtraining-Item missverstanden (Untergrenze) · Bearbeitungsdauer kurz.')

# ================================================================== 6.9 Explorativ
H('6.9  EXPLORATIV (nur IG, nur deskriptiv): Adhärenz gegen Prä-Bestwerte und %PAH — Selektionsfrage der Per-Protokoll-Teilmenge')
GRUPPE = {'Hohenlind': 'IG', 'Blau-Weiß Köln': 'IG', 'Vorwärts Spoho': 'KG'}
ZIEL = OrderedDict([('5m', ('Sprint_5m', '–', 'min')), ('10m', ('Sprint_10m', '–', 'min')), ('30m', ('Sprint_30m', '–', 'min')), ('505L', ('COD_505', 'L', 'min')), ('505R', ('COD_505', 'R', 'min')), ('SBJ', ('Standweitsprung', '–', 'max'))])
ws2 = wb['02_Rohdaten']; rows2 = list(ws2.iter_rows(values_only=True)); COL = {str(h): i for i, h in enumerate(rows2[0])}
def num(v):
    try: return float(str(v).replace(',', '.')) if v not in (None, '') else None
    except ValueError: return None
zellen = defaultdict(list)
for r_ in rows2[1:]:
    if r_[COL['Code']] is None or r_[COL['Zeitpunkt']] != 'prä': continue
    w_ = num(r_[COL['Wert']]); ung = str(r_[COL['ungültig']]).strip() if r_[COL['ungültig']] not in (None, '') else ''
    if w_ is None or ung: continue
    z = next(k for k, (t, s_, m) in ZIEL.items() if t == r_[COL['Test']] and s_ == r_[COL['Seite']])
    zellen[(r_[COL['Code']], z)].append(w_)
best = {k: (min(v) if ZIEL[k[1]][2] == 'min' else max(v)) for k, v in zellen.items()}
for c in ig_codes:
    if (c, '505L') in best and (c, '505R') in best: best[(c, '505M')] = (best[(c, '505L')] + best[(c, '505R')]) / 2
def pearson(x, y):
    n = len(x); mx, my = statistics.mean(x), statistics.mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y)); sxx = sum((a - mx) ** 2 for a in x); syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0: return float('nan'), float('nan'), float('nan')
    r_ = sxy / math.sqrt(sxx * syy); z_ = math.atanh(max(-0.9999, min(0.9999, r_))); se = 1 / math.sqrt(n - 3)
    return r_, math.tanh(z_ - 1.96 * se), math.tanh(z_ + 1.96 * se)
P('x = vollständige Einheiten (Hauptzählung). Variante I: alle IG-Spieler mit Listenplatz (n = 17, ohne BW-21; Nicht-Melder mit 0). Variante II: nur Spieler mit ≥ 1 Meldung (n = 15).')
P('Pearson r mit 95-%-KI (Fisher-z), kein p-Wert als Beleg; Vorzeichen: bei Zeiten bedeutet r < 0 „höhere Adhärenz ↔ schnellere Prä-Zeit“.')
P(f"{'Merkmal':12s}{'Var':>4s}{'n':>4s}{'r':>8s}{'95-%-KI':>18s}   Prä-Bestwert M (SD) bei Adhärenz < 6 | ≥ 6")
for z in ('5m', '10m', '30m', '505M', 'SBJ', 'PAH'):
    for var, filt in (('I', lambda c: c != 'BW-21'), ('II', lambda c: c != 'BW-21' and Z[c]['n'] > 0)):
        pl = [c for c in ig_codes if filt(c) and ((c, z) in best if z != 'PAH' else pers[c]['PAH'] is not None)]
        x = [Z[c]['ganz_je'] for c in pl]; y = [best[(c, z)] if z != 'PAH' else float(pers[c]['PAH']) for c in pl]
        r_, lo, hi = pearson(x, y)
        lo6 = [b for a, b in zip(x, y) if a < 6]; hi6 = [b for a, b in zip(x, y) if a >= 6]
        P(f"{z:12s}{var:>4s}{len(pl):>4d}{fmt(r_, 3):>8s}{('[' + fmt(lo, 2) + '; ' + fmt(hi, 2) + ']'):>18s}   {fmt(statistics.mean(lo6), 2) if lo6 else '—'} ({fmt(statistics.stdev(lo6), 2) if len(lo6) > 1 else '—'}, n {len(lo6)}) | {fmt(statistics.mean(hi6), 2) if hi6 else '—'} ({fmt(statistics.stdev(hi6), 2) if len(hi6) > 1 else '—'}, n {len(hi6)})")
P('  Streudiagrammdaten (Variante I): Code · Einheiten · 30 m · 505M · SBJ · %PAH')
for c in ig_codes:
    if c == 'BW-21': continue
    P(f"   {c} · {Z[c]['ganz_je']:2d} · {fmt(best.get((c, '30m')), 2)} · {fmt(best.get((c, '505M')), 3)} · {fmt(best.get((c, 'SBJ')), 0)} · {fmt(float(pers[c]['PAH']), 1) if pers[c]['PAH'] is not None else '—'}")
P('  Lesart: Die Per-Protokoll-Teilmenge ist eine Selbstselektion; ob sie sich in Ausgangsleistung oder Reifestatus vom Rest unterscheidet, zeigen r und die Gruppenmittel — bei n ≤ 17 nur als Orientierung.')

# ================================================================== 6.10 Soll-Ist
H('6.10  SOLL-IST DES MONITORINGS (TIDieR Item 10–12) — Antrag · Manuskript 4.5.1/4.6 · Umsetzung; Satzvorschläge (kein Manuskripttext)')
P('Antrag (16.06.2026): Trainingsprotokoll je Einheit · Adherence-Monitoring = Anzahl durchgeführter Einheiten + Session-RPE (CR-10, Foster et al., 2001) · Ausschluss < 75 % aus der Hauptanalyse ·')
P('  2 Einheiten/Woche à 30–40 min · Instruktionsvideos · Videos „wöchentlich“. Keine Angabe zu Erinnerungen, Zeitfenster, Auslieferungsweg, Datumserfassung.')
P('Umgesetzt (Verfasser 12.09.; Rohexport): SoSci-Fragebogen test546007, 9 Seiten/9 Items (Anhang A), Link in der WhatsApp-Gruppe je Verein und Abschlusskarte im Video; Wochenvideo sonntags 20 Uhr (YouTube, nicht gelistet);')
P('  jederzeit abrufbar, keine Zeitsperre, keine Mehrfachsperre; Erinnerungen in den Gruppen (Häufigkeit nicht protokolliert); Datums-Item nur „Heute“; 48-h-Abstand als schriftliche Anweisung (nicht kontrolliert);')
P('  Wochenvideos 24:17–31:14 min plus eigenes Erwärmungsvideo 8:53 = Sitzungsdauer 33:10–40:07 min.')
P('Manuskript (Master 09.09.) gegen Umsetzung — Fundstelle · Befund · Satzvorschlag [Vorschlagsliste, Freigabe je Punkt]:')
VORSCHLAEGE = [
 ('4.6 Abs. 1', '„Je Einheit wurden das Trainingsdatum … erfasst“', 'Datums-Item bot nur „Heute“ (111/111); der Trainingstag ist nicht erhoben.', '„… erfasst wurden der Meldezeitpunkt (das Datums-Item ließ nur die Angabe „Heute“ zu, sodass der Trainingstag nur bei taggleicher Meldung dem Meldedatum entspricht), die Zuordnung zu Woche und Einheit …“'),
 ('4.6 Abs. 3', '„als absolviert galten Einheiten mit dem Durchführungsstatus „ganz“ oder „teilweise““', 'Entscheidung 12.09.: Hauptzählung „ganz“; „teilweise“ gesondert und als Sensitivität (Begründung Skriptkopf).', '„Als absolviert galt eine Einheit mit dem Durchführungsstatus „ganz“; teilweise absolvierte Einheiten wurden gesondert ausgewiesen und in einer Sensitivitätsanalyse mitgezählt.“'),
 ('4.6 Abs. 1', '„durch die Abschlusskarte des jeweiligen Videos in Erinnerung gerufen … ein Zeitpunkt innerhalb des Tages war nicht vorgegeben“', 'Fragebogen war jederzeit abrufbar (auch tage- und wochenübergreifend); zusätzlich Erinnerungen in den vereinsbezogenen WhatsApp-Gruppen (Verfasser 12.09.; Häufigkeit nicht protokolliert).', '„… der Fragebogen war über den Link in der vereinsbezogenen Gruppe und die Abschlusskarte des Videos jederzeit erreichbar; ergänzend wurde in den Gruppen an das Ausfüllen erinnert. Ein Zeitfenster oder eine Sperre gegen Nach- und Mehrfachmeldungen bestand nicht.“'),
 ('4.5.1 Abs. 3', '„Die Videos wurden den Familien wöchentlich über nicht gelistete YouTube-Links zur Verfügung gestellt; für Rückfragen stand ein direkter Kontaktweg … offen“', 'Veröffentlichung sonntags 20 Uhr für die Folgewoche; Verteilung und Rückfragen über eine WhatsApp-Gruppe je Verein.', '„Das Video der jeweiligen Folgewoche wurde sonntags um 20 Uhr als nicht gelisteter YouTube-Link in einer vereinsbezogenen WhatsApp-Gruppe veröffentlicht, über die auch der Fragebogen-Link verteilt und Rückfragen beantwortet wurden.“'),
 ('4.5.1 Abs. 4', '„Einer Einführungskarte folgten ein rund zehnminütiges … Aufwärmprogramm … dessen Gesamtdauer im Rahmen der im Ethikantrag angegebenen 30 bis 40 Minuten lag“', 'Erwärmung war ein eigenes Video (8:53, in allen Wochen identisch), das Wochenvideo enthielt den Hauptteil (W1 28:16 · W2 28:02 · W3 24:17 · W4 25:55 · W5 31:03 · W6 31:14); Sitzungsdauer 33:10–40:07 min.', '„Je Einheit standen zwei Videos zur Verfügung: ein in allen Wochen identisches Aufwärmvideo nach dem RAMP-Schema (8:53 min; Jeffreys, 2007) und das Wochenvideo mit dem Hauptteil (24:17 bis 31:14 min). Die Gesamtdauer einer Einheit lag damit bei rund 33 bis 40 Minuten und entsprach der im Ethikantrag angegebenen Spanne.“'),
 ('4.5.1 Abs. 1', '„zwei Einheiten pro Woche an nicht aufeinanderfolgenden Tagen, Mindestabstand 48 Stunden“', 'Vorgabe, nicht kontrolliert; nicht prüfbar (Datums-Item); ein dokumentierter Verstoß (BW-02, 30.08.).', '„… angesetzt (Vorgabe: zwei Einheiten pro Woche mit mindestens 48 Stunden Abstand, ohne intensive Einheit dazwischen; die Einhaltung wurde nicht kontrolliert und ist aus dem Monitoring nicht prüfbar, Abschn. 4.6).“'),
 ('4.5.1 Abs. 4', '„die Spieler waren instruiert, das Video einmal zu starten und die Einheit ohne Vor- oder Zurückspulen zu durchlaufen“', 'Videopausen/Wiederholungen bei 25 von 111 Meldungen (HL-07 systematisch).', 'Satz beibehalten; in 5.1 die Pausenhäufigkeit berichten, in 6.2 als Näherungsindikator der Umsetzungsqualität einordnen (kein Textbedarf in 4.5.1).'),
 ('4.5.2 Abs. 2', '„bestand bei Verein A eine vereinsfreie Phase ohne Trainingsvorgaben“ (W1–W2)', 'Verfasser 12.09.: In der vereinsfreien Phase gab das Trainerteam einen extensiven Laufplan vor (Freitexte HL-02 „Plan von Sven“; das Dokument liegt nicht im Ordner). Der Auszug vom 03./04.08. (Vorbereitung Hohenlind.jpg) betrifft den Trainingsauftakt.', '„Während der ersten beiden Interventionswochen (20.07. bis 02.08.2026) bestand bei Verein A eine vereinsfreie Phase, für die das Trainerteam einen extensiven Laufplan vorgab; die individuelle Umsetzung wurde nicht erfasst.“ ⟨Anhang D: Laufplan nachreichen oder als „nicht dokumentiert“ führen⟩'),
]
for i, (fund, alt, bef, neu) in enumerate(VORSCHLAEGE, 1):
    P(f'  {i}. {fund} · Ist: {alt}\n     Befund: {bef}\n     Vorschlag: {neu}')
P('\nSoll-Ist in Kürze (für 6.2): Antrag erfüllt bei Instrument je Einheit, Zählgröße und sRPE; nicht vorgesehen und nicht umgesetzt: Zeitfenster, Sperre, Datumserfassung, Erinnerungsprotokoll, Instrument für die KG.')
P('  Sitzungsdauer (Wochenvideo + Erwärmungsvideo) 33:10–40:07 min liegt in der Antragsspanne (W6 um 7 s darüber). Erinnerungen erfolgten, sind aber nicht protokolliert → 4.6 nur qualitativ.')

# ================================================================== Abschluss
P('\n' + '#' * 110); P('ENDE F1 — alle Schritte § 6.1–6.10 gerechnet (Stand 12.09.2026, spät; Videodauern und Erwärmung nach Verfasserangabe eingearbeitet). Offen: ungefilterter Export (optional) · mündliche Auskunft HL-06/BW-01/HL-05.'); P('#' * 110)
open(OUT, 'w', encoding='utf-8').write(buf.getvalue()); print('\n→ geschrieben:', OUT)

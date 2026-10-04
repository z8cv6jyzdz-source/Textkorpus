# -*- coding: utf-8 -*-
"""
Datensicherung_Plausibilitaet_2026-09-24.py

Zweck:    Markiert unplausible und widersprüchliche Werte im Workbook nach Regeln, die
          vor dem Lauf mit Datum feststehen (Prüfregeln P1 bis P8, Schwellen unten).
          Der Verfasser prüft nur die markierten Werte am Papierbogen und trägt je Wert
          "stimmt" oder "korrigiert, alt -> neu" ein. Keine Zweiterfassung. Kein Wert wird
          wegen seiner Größe geändert oder ausgeschlossen. Die Regeln gelten für beide
          Gruppen und beide Zeitpunkte gleich.
Schritt:  Auswertungsverfahren_2026-09-24, Phase 1, Schritt 1.1
Eingang:  Statistik/Studiendaten_U15_gesamt.xlsx (Blätter 01_Personen, 02_Rohdaten)
              SHA-256 beim ersten Lauf: a3f665f83a97fef99e83b1e75c09cef2887f4de279c93e5467ebb536d80da6f7
          Die Prüfsumme wird bei jedem Lauf neu berechnet und ausgegeben.
Fassung:  2026-09-24, Fassung 2 (Claude, Task Datensicherung). Fassung 1 war der Vorschlag mit
          zwei Schwellenvarianten (A: P4 10/15 %, P6 8/12 % · B: P4 15/20 %, P6 10/15 %).
          Fassung 2 trägt die vom Verfasser am 24.09.2026 per Klick freigegebene Variante B.
Aufruf:   python Datensicherung_Plausibilitaet_2026-09-24.py [Basisordner] [--xlsx PFAD]
          Basisordner = Ordner "Bachelorarbeit" (Voreinstellung wie im Strukturskript).
          --xlsx PFAD schreibt die markierten Werte in das Blatt Markierte_Werte der
          Arbeitsliste (Datei wird angelegt oder das Blatt ersetzt). Ausgabe immer in die
          gleichnamige .txt neben dem Skript und auf die Konsole.
Regeln:   Keine Namen, kein Geburtsdatum, kein Testdatum je Spieler in der Ausgabe.
          Das Alter wird im Skript aus den Datumsfeldern gerechnet und nur als Zahl geprüft.
Bereits entschieden, wird nicht erneut vorgelegt (Übergabe Datensicherung):
          HL-08 post Sprint_10m Versuch 2 = 1,95 s bleibt (Verfasser 12.09.2026)
          alle 10-m-Post-Werte von Verein B "System falsch aufgenommen"
"""

import sys, os, io, re, hashlib, datetime, collections, statistics

FASSUNG = "2026-09-24, Fassung 2"
FREIGABE = "Schwellen vorgeschlagen am 24.09.2026 (Variante B), Freigabe durch den Verfasser per Klick am 24.09.2026"

# ----------------------------------------------------------------------------
# Prüfregeln und Schwellen (vor dem Lauf festgelegt, 24.09.2026)
# ----------------------------------------------------------------------------
# P1 Physiologische Grenzen je Test (grober Bereich, fängt Komma- und Einheitenfehler)
P1_GRENZEN = {"Sprint_5m": (0.70, 1.80), "Sprint_10m": (1.40, 3.00), "Sprint_30m": (3.50, 7.00),
              "COD_505": (1.80, 4.00), "Standweitsprung": (100, 300)}
# P2 Reihenfolge der Teilzeiten eines Laufs: 5 m vor 10 m vor 30 m (strikt steigend)
# P3 Abschnitte eines Laufs: Δt <= 0 oder v > 10,0 m/s (S02, Lauf auslösegestört) und
#    Abschnittsgeschwindigkeit nicht steigend (v 0-5 m >= v 5-10 m oder v 5-10 m >= v 10-30 m)
P3_VMAX = 10.0
# P4 Spannweite der Versuche eines Spielers (gleicher Test, Zeitpunkt, Seite): (Max - Min)/Min
P4_SPANNE = {"zeit": 0.15, "sbj": 0.20}
# P5 Ausreißer je Test, Seite und Zeitpunkt über alle gültigen Versuche aller Spieler:
#    |x - Median| > P5_K * 1,4826 * MAD
P5_K = 3.0
# P6 Prä-Post-Änderung des Bestwerts je Spieler: |Post - Prä| / Prä
P6_AEND = {"zeit": 0.10, "sbj": 0.15}
# P7 Alter und Anthropometrie
P7 = {"Alter_prae": (12.0, 16.0), "Groesse_prae": (140, 200), "Gewicht_prae": (35, 95), "BMI": (14.0, 30.0),
      "Groesse_Mutter": (145, 190), "Groesse_Vater": (155, 205)}
# P8 Muster: Zeiten mit mehr als 2 Nachkommastellen, Standweitsprung mit Nachkommastellen,
#    identische Versuchssätze zweier Spieler, drei identische Versuche eines Spielers,
#    Wert in einer Zeile mit Bemerkung "System nicht aufgenommen" oder "System falsch aufgenommen"
BEREITS_ENTSCHIEDEN = {("HL-08", "post", "Sprint_10m", "–", 2)}

# ----------------------------------------------------------------------------
if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
    BASIS = os.path.abspath(sys.argv[1])
else:
    BASIS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
XLSX = None
if "--xlsx" in sys.argv:
    XLSX = sys.argv[sys.argv.index("--xlsx") + 1]
P_WB = os.path.join(BASIS, "Statistik", "Studiendaten_U15_gesamt.xlsx")
P_OUT = os.path.splitext(os.path.abspath(__file__))[0] + ".txt"

out = io.StringIO()
def w(s=""): out.write(s + "\n")
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

w("Datensicherung, Schritt 1.1 Plausibilitätsprüfung")
w("Skriptfassung " + FASSUNG + " · Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
w(FREIGABE)
w("Basisordner: " + BASIS)
w("Eingang: " + os.path.relpath(P_WB, BASIS) + "  SHA-256 " + sha256(P_WB) + "  geändert " +
  datetime.datetime.fromtimestamp(os.path.getmtime(P_WB)).strftime("%Y-%m-%d %H:%M:%S"))
w()

import openpyxl
wb = openpyxl.load_workbook(P_WB, data_only=False)
CODE_RE = re.compile(r"^(HL|BW|VS)-\d{2}$")
ws = wb["01_Personen"]
hdr = [c.value for c in ws[1]]
col = {h: i + 1 for i, h in enumerate(hdr) if h is not None}
personen = {}
for r in range(2, ws.max_row + 1):
    code = ws.cell(r, col["Code"]).value
    if isinstance(code, str) and CODE_RE.match(code.strip()):
        d = {h: ws.cell(r, c).value for h, c in col.items()}
        d["_zeile"] = r
        personen[code.strip()] = d
ws2 = wb["02_Rohdaten"]
SOLL2 = ["Code", "Verein", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert", "Einheit", "ungültig", "Bemerkung", "gilt"]
roh = []
for r in range(2, ws2.max_row + 1):
    vals = [ws2.cell(r, c).value for c in range(1, 12)]
    if all(v in (None, "") for v in vals[:10]): continue
    d = dict(zip(SOLL2, vals)); d["_zeile"] = r
    d["Code"] = d["Code"].strip()
    d["Seite"] = d["Seite"] if d["Test"] == "COD_505" else "–"
    d["gueltig_roh"] = (d["Wert"] not in (None, "")) and (d["ungültig"] in (None, ""))
    roh.append(d)

def ist_zahl(v): return isinstance(v, (int, float)) and not isinstance(v, bool)
def zelle_wert(d): return "02_Rohdaten!G%d" % d["_zeile"]
def art(test): return "sbj" if test == "Standweitsprung" else "zeit"

mark = []   # dict je Markierung
def M(regel, code, zeitpunkt, test, seite, versuch, wert, zelle, befund):
    key = (code, zeitpunkt, test, seite, versuch)
    if key in BEREITS_ENTSCHIEDEN:
        w("   (bereits entschieden, nicht vorgelegt) %s: %s %s %s %s Versuch %s Wert %r: %s" % (regel, code, zeitpunkt, test, seite, versuch, wert, befund))
        return
    mark.append({"Regel": regel, "Code": code, "Zeitpunkt": zeitpunkt, "Test": test, "Seite": seite,
                 "Versuch": versuch, "Wert": wert, "Zelle": zelle, "Befund": befund})

# --- P1 -------------------------------------------------------------------
w("P1 Physiologische Grenzen: " + ", ".join("%s %s" % (t, g) for t, g in P1_GRENZEN.items()))
for d in roh:
    v = d["Wert"]
    if not ist_zahl(v): continue
    lo, hi = P1_GRENZEN[d["Test"]]
    if not (lo <= v <= hi):
        M("P1", d["Code"], d["Zeitpunkt"], d["Test"], d["Seite"], d["Versuch"], v, zelle_wert(d),
          "Wert außerhalb %s bis %s" % (lo, hi))

# --- P2 und P3: Läufe -------------------------------------------------------
w("P2 Teilzeitenfolge 5 m < 10 m < 30 m je Lauf · P3 Abschnitte: Δt <= 0 oder v > %.1f m/s (S02), Abschnittsgeschwindigkeit nicht steigend" % P3_VMAX)
laeufe = collections.defaultdict(dict)
zeilen = {}
for d in roh:
    if d["Test"] in ("Sprint_5m", "Sprint_10m", "Sprint_30m") and d["gueltig_roh"]:
        dist = {"Sprint_5m": 5, "Sprint_10m": 10, "Sprint_30m": 30}[d["Test"]]
        laeufe[(d["Code"], d["Zeitpunkt"], d["Versuch"])][dist] = d["Wert"]
        zeilen[(d["Code"], d["Zeitpunkt"], d["Versuch"], dist)] = d
TESTNAME = {5: "Sprint_5m", 10: "Sprint_10m", 30: "Sprint_30m"}
for (code, zp, vers), tz in laeufe.items():
    pts = sorted(tz.items())
    # P2
    for (d1, t1), (d2, t2) in zip(pts, pts[1:]):
        if not (t1 < t2):
            for dist, t in pts:
                dd = zeilen[(code, zp, vers, dist)]
                M("P2", code, zp, TESTNAME[dist], "–", vers, t, zelle_wert(dd),
                  "Teilzeiten nicht steigend: %s m %.2f s, %s m %.2f s (ganzer Lauf markiert)" % (d1, t1, d2, t2))
            break
    # P3
    d0, t0 = 0, 0.0
    vs = []
    gestoert = None
    for dist, t in pts:
        dt = t - t0
        if dt <= 0 or (dist - d0) / dt > P3_VMAX:
            gestoert = "Abschnitt bis %d m: Δt %.3f s, v %s m/s (Lauf nach S02 auslösegestört)" % (dist, dt, ("%.2f" % ((dist - d0) / dt)) if dt > 0 else "undefiniert")
            break
        vs.append((dist, (dist - d0) / dt))
        d0, t0 = dist, t
    if gestoert:
        for dist, t in pts:
            dd = zeilen[(code, zp, vers, dist)]
            M("P3", code, zp, TESTNAME[dist], "–", vers, t, zelle_wert(dd), gestoert + " (ganzer Lauf markiert)")
        continue
    for (da, va), (db, vb) in zip(vs, vs[1:]):
        if va >= vb:
            for dist, t in pts:
                dd = zeilen[(code, zp, vers, dist)]
                M("P3", code, zp, TESTNAME[dist], "–", vers, t, zelle_wert(dd),
                  "Abschnittsgeschwindigkeit fällt: bis %d m %.2f m/s, bis %d m %.2f m/s (ganzer Lauf markiert)" % (da, va, db, vb))
            break

# --- P4 Spannweite je Spieler ------------------------------------------------
w("P4 Spannweite der Versuche eines Spielers: (Max - Min)/Min > %d %% Zeiten, > %d %% Standweitsprung" % (P4_SPANNE["zeit"] * 100, P4_SPANNE["sbj"] * 100))
saetze = collections.defaultdict(list)
for d in roh:
    if d["gueltig_roh"]:
        saetze[(d["Code"], d["Zeitpunkt"], d["Test"], d["Seite"])].append(d)
for (code, zp, test, seite), ds in saetze.items():
    if len(ds) < 2: continue
    vals = [d["Wert"] for d in ds]
    mn, mx = min(vals), max(vals)
    sp = (mx - mn) / mn
    if sp > P4_SPANNE[art(test)]:
        med = statistics.median(vals)
        fern = max(ds, key=lambda d: abs(d["Wert"] - med))
        for d in ds:
            M("P4", code, zp, test, seite, d["Versuch"], d["Wert"], zelle_wert(d),
              "Spannweite %.1f %% (Werte %s), am weitesten vom Median: Versuch %s" % (sp * 100, ", ".join(str(v) for v in vals), fern["Versuch"]))

# --- P5 Ausreißer je Test, Seite, Zeitpunkt ---------------------------------
w("P5 Ausreißer über alle Spieler: |x - Median| > %.1f x 1,4826 x MAD je Test, Seite und Zeitpunkt" % P5_K)
gruppen = collections.defaultdict(list)
for d in roh:
    if d["gueltig_roh"]:
        gruppen[(d["Test"], d["Seite"], d["Zeitpunkt"])].append(d)
for (test, seite, zp), ds in sorted(gruppen.items()):
    vals = [d["Wert"] for d in ds]
    med = statistics.median(vals)
    mad = statistics.median([abs(v - med) for v in vals]) * 1.4826
    grenze = P5_K * mad
    w("   %s %s %s: n %d, Median %s, 1,4826·MAD %.4f, Grenze ±%.4f" % (test, seite, zp, len(vals), med, mad, grenze))
    if mad == 0: continue
    for d in ds:
        if abs(d["Wert"] - med) > grenze:
            M("P5", d["Code"], zp, test, seite, d["Versuch"], d["Wert"], zelle_wert(d),
              "Abweichung vom Median %s um %.3f (Grenze %.3f)" % (med, d["Wert"] - med, grenze))

# --- P6 Prä-Post-Änderung des Bestwerts --------------------------------------
w("P6 Prä-Post-Änderung des Bestwerts: |Post - Prä|/Prä > %d %% Zeiten, > %d %% Standweitsprung" % (P6_AEND["zeit"] * 100, P6_AEND["sbj"] * 100))
best = {}
for (code, zp, test, seite), ds in saetze.items():
    vals = [d["Wert"] for d in ds]
    best[(code, zp, test, seite)] = (max(vals) if test == "Standweitsprung" else min(vals), ds)
for (code, zp, test, seite), (b, ds) in best.items():
    if zp != "prä": continue
    post = best.get((code, "post", test, seite))
    if post is None: continue
    bp, dsp = post
    aend = (bp - b) / b
    if abs(aend) > P6_AEND[art(test)]:
        dpre = [d for d in ds if d["Wert"] == b][0]
        dpost = [d for d in dsp if d["Wert"] == bp][0]
        M("P6", code, "prä", test, seite, dpre["Versuch"], b, zelle_wert(dpre), "Bestwert prä %s, post %s, Änderung %+.1f %% (beide Bestwerte markiert)" % (b, bp, aend * 100))
        M("P6", code, "post", test, seite, dpost["Versuch"], bp, zelle_wert(dpost), "Bestwert prä %s, post %s, Änderung %+.1f %% (beide Bestwerte markiert)" % (b, bp, aend * 100))

# --- P7 Alter und Anthropometrie ---------------------------------------------
w("P7 Alter und Anthropometrie: " + ", ".join("%s %s" % (k, v) for k, v in P7.items()))
def spalte(h): return openpyxl.utils.get_column_letter(col[h])
for code, d in personen.items():
    gd, tp = d.get("Geburtsdatum"), d.get("Testdatum_prä")
    if isinstance(gd, (datetime.date, datetime.datetime)) and isinstance(tp, (datetime.date, datetime.datetime)):
        gd = gd.date() if isinstance(gd, datetime.datetime) else gd
        tp = tp.date() if isinstance(tp, datetime.datetime) else tp
        alter = (tp - gd).days / 365.25
        lo, hi = P7["Alter_prae"]
        if not (lo <= alter <= hi):
            M("P7", code, "prä", "Alter", "–", "", round(alter, 2), "01_Personen!%s%d und %s%d" % (spalte("Geburtsdatum"), d["_zeile"], spalte("Testdatum_prä"), d["_zeile"]),
              "Alter prä %.2f Jahre außerhalb %s bis %s (Geburtsdatum oder Testdatum prüfen)" % (alter, lo, hi))
    else:
        M("P7", code, "prä", "Alter", "–", "", "", "01_Personen!%s%d" % (spalte("Geburtsdatum"), d["_zeile"]), "Geburtsdatum oder Testdatum prä fehlt oder ist kein Datum")
    for h, k in (("Größe_prä_cm", "Groesse_prae"), ("Gewicht_prä_kg", "Gewicht_prae"), ("Größe_Mutter_cm", "Groesse_Mutter"), ("Größe_Vater_cm", "Groesse_Vater")):
        v = d.get(h)
        if v in (None, ""):
            M("P7", code, "prä", h, "–", "", "", "01_Personen!%s%d" % (spalte(h), d["_zeile"]), "%s leer" % h)
        elif not ist_zahl(v):
            M("P7", code, "prä", h, "–", "", v, "01_Personen!%s%d" % (spalte(h), d["_zeile"]), "%s ist Text: %r" % (h, v))
        else:
            lo, hi = P7[k]
            if not (lo <= v <= hi):
                M("P7", code, "prä", h, "–", "", v, "01_Personen!%s%d" % (spalte(h), d["_zeile"]), "%s außerhalb %s bis %s" % (h, lo, hi))
    g, m = d.get("Größe_prä_cm"), d.get("Gewicht_prä_kg")
    if ist_zahl(g) and ist_zahl(m) and g > 0:
        bmi = m / (g / 100) ** 2
        lo, hi = P7["BMI"]
        if not (lo <= bmi <= hi):
            M("P7", code, "prä", "BMI", "–", "", round(bmi, 1), "01_Personen!%s%d und %s%d" % (spalte("Größe_prä_cm"), d["_zeile"], spalte("Gewicht_prä_kg"), d["_zeile"]),
              "BMI %.1f außerhalb %s bis %s (Körperhöhe und Körpermasse prüfen)" % (bmi, lo, hi))

# --- P8 Muster -----------------------------------------------------------------
w("P8 Muster: Nachkommastellen, identische Versuchssätze, drei identische Versuche, Wert trotz Systemausfall")
for d in roh:
    v = d["Wert"]
    if not ist_zahl(v): continue
    s = repr(float(v))
    nd = len(s.split(".")[1]) if "." in s else 0
    if d["Test"] == "Standweitsprung" and nd > 0 and float(v) != int(v):
        M("P8", d["Code"], d["Zeitpunkt"], d["Test"], d["Seite"], d["Versuch"], v, zelle_wert(d), "Standweitsprung mit Nachkommastellen")
    if d["Test"] != "Standweitsprung" and nd > 2:
        M("P8", d["Code"], d["Zeitpunkt"], d["Test"], d["Seite"], d["Versuch"], v, zelle_wert(d), "Zeit mit mehr als zwei Nachkommastellen")
    if d["Bemerkung"] in ("System nicht aufgenommen", "Sytem nicht aufgenommen", "System falsch aufgenommen"):
        M("P8", d["Code"], d["Zeitpunkt"], d["Test"], d["Seite"], d["Versuch"], v, zelle_wert(d), "Wert vorhanden trotz Bemerkung %r" % d["Bemerkung"])
for (code, zp, test, seite), ds in saetze.items():
    vals = [d["Wert"] for d in ds]
    if len(vals) == 3 and len(set(vals)) == 1:
        for d in ds:
            M("P8", code, zp, test, seite, d["Versuch"], d["Wert"], zelle_wert(d), "drei identische Versuche")
saetze_voll = collections.defaultdict(list)
for (code, zp, test, seite), ds in saetze.items():
    vals = tuple(sorted(d["Wert"] for d in ds))
    if len(vals) >= 2:
        saetze_voll[(zp, test, seite, vals)].append((code, ds))
for (zp, test, seite, vals), lst in saetze_voll.items():
    if len(lst) > 1:
        codes = ", ".join(c for c, _ in lst)
        for code, ds in lst:
            for d in ds:
                M("P8", code, zp, test, seite, d["Versuch"], d["Wert"], zelle_wert(d), "identischer Versuchssatz bei %s (Werte %s)" % (codes, ", ".join(str(v) for v in vals)))

# ----------------------------------------------------------------------------
# Ausgabe
# ----------------------------------------------------------------------------
w()
w("=" * 78)
w("Markierte Werte: %d Markierungen" % len(mark))
cnt = collections.Counter(m["Regel"] for m in mark)
w("je Regel: " + ", ".join("%s %d" % (k, cnt[k]) for k in sorted(cnt)))
zellen = {m["Zelle"] for m in mark}
w("verschiedene Zellen: %d, Spieler betroffen: %d" % (len(zellen), len({m["Code"] for m in mark})))
w("=" * 78)
for m in sorted(mark, key=lambda m: (m["Regel"], m["Code"], m["Zeitpunkt"], m["Test"], m["Seite"], str(m["Versuch"]))):
    w("%-3s %-6s %-4s %-16s %-2s V%-2s %-8s %-26s %s" % (m["Regel"], m["Code"], m["Zeitpunkt"], m["Test"], m["Seite"], m["Versuch"], m["Wert"], m["Zelle"], m["Befund"]))

if XLSX:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    if os.path.exists(XLSX):
        xb = load_workbook(XLSX)
        if "Markierte_Werte" in xb.sheetnames:
            del xb["Markierte_Werte"]
        xs = xb.create_sheet("Markierte_Werte", 0)
    else:
        xb = Workbook(); xs = xb.active; xs.title = "Markierte_Werte"
    kopf = ["Nr", "Regel", "Code", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert im Workbook", "Zelle", "Befund",
            "Urteil (stimmt / korrigiert)", "Wert laut Papierbogen", "Bemerkung des Verfassers"]
    xs.append(kopf)
    for c in range(1, len(kopf) + 1):
        xs.cell(1, c).font = Font(bold=True); xs.cell(1, c).fill = PatternFill("solid", fgColor="D6E4F0")
    # eine Zeile je Zelle, mehrere Regeln und Befunde derselben Zelle zusammengefasst
    je_zelle = collections.OrderedDict()
    for m in sorted(mark, key=lambda m: (m["Code"], m["Zeitpunkt"], m["Test"], m["Seite"], str(m["Versuch"]), m["Regel"])):
        z = je_zelle.setdefault(m["Zelle"], dict(m, Regeln=[], Befunde=[]))
        if m["Regel"] not in z["Regeln"]:
            z["Regeln"].append(m["Regel"])
        z["Befunde"].append(m["Regel"] + ": " + m["Befund"])
    for i, z in enumerate(je_zelle.values(), 1):
        xs.append([i, ", ".join(z["Regeln"]), z["Code"], z["Zeitpunkt"], z["Test"], z["Seite"], z["Versuch"], z["Wert"], z["Zelle"], " | ".join(z["Befunde"]), "", "", ""])
    for row in xs.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for c in row[10:13]:
            c.fill = PatternFill("solid", fgColor="FFF2CC")
    for c, wd in zip("ABCDEFGHIJKLM", (5, 6, 8, 9, 16, 6, 8, 14, 22, 70, 26, 20, 30)):
        xs.column_dimensions[c].width = wd
    xs.freeze_panes = "A2"
    xb.save(XLSX)
    w("Arbeitsliste geschrieben: " + XLSX + " (Blatt Markierte_Werte, %d Zeilen, eine je Zelle)" % len(je_zelle))

text = out.getvalue()
with open(P_OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print(text)

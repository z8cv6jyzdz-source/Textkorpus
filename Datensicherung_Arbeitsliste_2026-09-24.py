# -*- coding: utf-8 -*-
"""
Datensicherung_Arbeitsliste_2026-09-24.py (Hilfsskript des Tasks Datensicherung, kein Rechenskript)

Zweck:    Legt die Arbeitsliste Claude/04_Uebergaben/Belegpruefung_2026-09-24.xlsx an mit den
          Blättern Markierte_Werte (Vorlage, wird vom Plausibilitätsskript gefüllt), Codezuordnung
          (Schritt 1.2 a und 1.2 b) und Offene_Punkte. Ohne Namen, ohne Geburtsdaten.
Schritt:  Auswertungsverfahren_2026-09-24, Phase 1, Schritt 1.2
Eingang:  Statistik/Studiendaten_U15_gesamt.xlsx (Blatt 01_Personen, nur Code, Verein, Gruppe,
          Familiarisierung, Status)
Fassung:  2026-09-24, Fassung 2 (Klickantworten vom 24.09.2026 eingetragen: Zuordnungstabelle bestätigt, Sprintlauf bestätigt, Post-Termin Verein C 14.09.2026)
Aufruf:   python Datensicherung_Arbeitsliste_2026-09-24.py [Basisordner] [Zielpfad]
"""
import sys, os, re, datetime
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASIS = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ZIEL = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASIS, "Claude", "04_Uebergaben", "Belegpruefung_2026-09-24.xlsx")
P_WB = os.path.join(BASIS, "Statistik", "Studiendaten_U15_gesamt.xlsx")

NAVY = "1F3864"; BAND = "D6E4F0"; ZEBRA = "EEF3F9"; GELB = "FFF2CC"
F_KOPF = Font(name="Arial", bold=True, color="FFFFFF", size=10)
F_TXT = Font(name="Arial", size=10)
F_TITEL = Font(name="Arial", bold=True, color=NAVY, size=12)
F_NOTE = Font(name="Arial", italic=True, size=9, color="555555")
FILL_KOPF = PatternFill("solid", fgColor=NAVY)
FILL_ZEBRA = PatternFill("solid", fgColor=ZEBRA)
FILL_GELB = PatternFill("solid", fgColor=GELB)
FILL_BAND = PatternFill("solid", fgColor=BAND)
thin = Side(style="thin", color="BBBBBB")
RAND = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

def tabelle(ws, r0, kopf, zeilen, breiten=None, gelb_spalten=()):
    for j, h in enumerate(kopf, 1):
        c = ws.cell(r0, j, h); c.font = F_KOPF; c.fill = FILL_KOPF; c.alignment = WRAP; c.border = RAND
    for i, z in enumerate(zeilen, 1):
        for j, v in enumerate(z, 1):
            c = ws.cell(r0 + i, j, v); c.font = F_TXT; c.alignment = WRAP; c.border = RAND
            if i % 2 == 0: c.fill = FILL_ZEBRA
            if j in gelb_spalten: c.fill = FILL_GELB
    if breiten:
        for j, b in enumerate(breiten, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = b
    return r0 + len(zeilen) + 1

wb_src = openpyxl.load_workbook(P_WB, data_only=False)
ws = wb_src["01_Personen"]
hdr = [c.value for c in ws[1]]
col = {h: i + 1 for i, h in enumerate(hdr) if h}
CODE_RE = re.compile(r"^(HL|BW|VS)-\d{2}$")
spieler = []
for r in range(2, ws.max_row + 1):
    code = ws.cell(r, col["Code"]).value
    if isinstance(code, str) and CODE_RE.match(code.strip()):
        spieler.append((code.strip(), ws.cell(r, col["Verein"]).value, ws.cell(r, col["Gruppe"]).value,
                        ws.cell(r, col["Familiarisierung"]).value, ws.cell(r, col["Status"]).value))
VMAP = {"Hohenlind": "A", "Blau-Weiß Köln": "B", "Vorwärts Spoho": "C"}
GMAP = {"Intervention": "IG", "Kontrolle": "KG"}
PFLICHT = {"VS-11": "ja (B3)", "VS-16": "ja (B3)", "VS-17": "ja (B3)", "VS-18": "ja (B3)",
           "VS-01": "ja (Einwilligung, PA § 3)", "VS-02": "ja (Einwilligung, PA § 3)"}

xb = Workbook()
# ---------------------------------------------------------------- Markierte_Werte (Vorlage)
xs = xb.active; xs.title = "Markierte_Werte"
xs["A1"] = "Markierte Werte (Schritt 1.1) – wird vom Plausibilitätsskript nach Freigabe der Prüfregeln gefüllt"; xs["A1"].font = F_TITEL
xs["A2"] = "Je Zeile ein Urteil eintragen: stimmt · korrigiert (dann Wert laut Papierbogen). Ein Wert, der dem Papierbogen entspricht, bleibt, auch wenn er extrem ist."; xs["A2"].font = F_NOTE
kopf = ["Nr", "Regel", "Code", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert im Workbook", "Zelle", "Befund",
        "Urteil (stimmt / korrigiert)", "Wert laut Papierbogen", "Bemerkung des Verfassers"]
tabelle(xs, 4, kopf, [], (5, 6, 8, 9, 16, 6, 8, 14, 22, 70, 26, 20, 30), gelb_spalten=(11, 12, 13))
xs.freeze_panes = "A5"

# ---------------------------------------------------------------- Codezuordnung
xc = xb.create_sheet("Codezuordnung")
xc["A1"] = "Codezuordnung Papier → Workbook (Schritt 1.2 a) – lokal ausfüllen, ohne Namen"; xc["A1"].font = F_TITEL
xc["A2"] = ("Gelbe Spalten füllt der Verfasser aus Papierbögen, Einwilligungserklärungen und Anwesenheitslisten. "
            "Pflicht: VS-11, VS-16 bis VS-18 (Maßnahme B3) und die Einwilligung von VS-01 und VS-02. "
            "Fehlt eine Einwilligung, wird angehalten."); xc["A2"].font = F_NOTE
kopf = ["Workbook-Code", "Verein", "Gruppe", "Code auf dem Prä-Bogen", "Code auf dem Post-Bogen",
        "Einwilligung liegt vor (ja / nein)", "Familiarisierungstermine laut Anwesenheitsliste (1 / 2)",
        "Familiarisierung im Workbook", "Status im Workbook", "Pflichtfeld", "Bemerkung des Verfassers"]
zeilen = []
for code, ver, gr, fam, st in spieler:
    zeilen.append([code, VMAP.get(ver, ver), GMAP.get(gr, gr), "", "", "", "", fam if fam is not None else "", st, PFLICHT.get(code, ""), ""])
r = tabelle(xc, 4, kopf, zeilen, (14, 8, 8, 20, 20, 18, 24, 16, 34, 20, 34), gelb_spalten=(4, 5, 6, 7, 11))
r += 1
xc.cell(r, 1, "Vergebene Codes ohne Studiendaten (gehören in Abb. 1 Teilnehmerfluss, nicht in den Datenstand)").font = F_TITEL
r += 1
kopf2 = ["Code", "Verein", "Grund (Verfasser)", "Einwilligung lag vor (ja / nein)", "Eingangstestung (ja / nein)", "Bemerkung des Verfassers"]
zeilen2 = [[c, "C", "", "", "", ""] for c in ("VS-09", "VS-12", "VS-13", "VS-14", "VS-15")]
r = tabelle(xc, r, kopf2, zeilen2, gelb_spalten=(3, 4, 5, 6))
r += 1
xc.cell(r, 1, "Zuordnungstabelle Fragebogen (Schritt 1.2 b): Listenlabel → Analysecode, vom Verfasser per Klick am 24.09.2026 bestätigt").font = F_TITEL
r += 1
kopf3 = ["Listenlabel (H010)", "Codebuch-Wert H010", "Analysecode (Workbook)", "kein_Listenplatz", "Herkunft der Regel"]
ZUO = [("HL-01", 1, "HL-01"), ("HL-02", 2, "HL-02"), ("HL-03", 3, "HL-03"), ("HL-04", 4, "HL-05"), ("HL-05", 5, ""),
       ("HL-06", 6, "HL-06"), ("HL-07", 7, "HL-07"), ("HL-08", 8, "HL-08"),
       ("BW-01", 9, "BW-01"), ("BW-02", 10, "BW-02"), ("BW-03", 11, ""), ("BW-04", 12, "BW-04"), ("BW-05", 13, "BW-05"),
       ("BW-06", 14, "BW-06"), ("BW-07", 15, "BW-07"), ("BW-08", 16, "BW-08"), ("BW-09", 17, "BW-09"), ("BW-10", 18, "BW-10"),
       ("BW-11", 19, "BW-11"), ("BW-12", 20, ""), ("BW-13", 21, ""), ("BW-14", 22, "")]
zeilen3 = []
for lab, h, ac in ZUO:
    if lab == "HL-04": q = "FA § 1: Listenplatz HL-04 = Workbook HL-05 (Verein A hat HL-05 statt Listenplatz HL-04, PA § 3.2)"
    elif ac == "": q = "kein realer Spieler (Übergabe 1.2 b)"
    else: q = "Listenlabel = Workbook-Code, altes Schema (FA § 1, PA § 3.2)"
    zeilen3.append([lab, h, ac if ac else "(leer)", "nein" if ac else "–", q])
zeilen3.append(["– (nicht in der Liste)", "–", "BW-21", "ja", "Instrumentenfehler: Workbook-BW-21 stand in der Auswahlliste nicht zur Verfügung (PA § 3.2, K9)"])
r = tabelle(xc, r, kopf3, zeilen3)

# ---------------------------------------------------------------- Offene_Punkte
xo = xb.create_sheet("Offene_Punkte")
xo["A1"] = "Offene Punkte für die Belegprüfung (Schritt 1.1 und 1.4)"; xo["A1"].font = F_TITEL
xo["A2"] = "Gelbe Spalten füllt der Verfasser. Korrekturen im Workbook schreibt Claude erst nach Freigabe, mit Sicherung und Blatt 00_Aenderungen."; xo["A2"].font = F_NOTE
kopf = ["Nr", "Fundstelle", "Befund", "Beleg", "Vorgeschlagene Korrektur", "Antwort des Verfassers", "Freigabe (ja / nein)"]
zeilen = [
    [1, "01_Personen, Status VS-01 bis VS-08, VS-10, VS-11, VS-17, VS-18 (11 Spieler)", "Status „Post-Testung ausstehend (Termin 15.09.2026)“, obwohl Post-Werte in 02_Rohdaten stehen", "Papierbogen Post Verein C", "Status → „ausgewertet“", "", ""],
    [2, "01_Personen, Status VS-07", "keine Post-Werte, kein Grund", "Papierbogen Post Verein C, Anwesenheit", "Status → „Post-Testung nicht angetreten – ⟨Grund⟩“ (Wortlaut wie BW-07, BW-21)", "", ""],
    [3, "01_Personen, Status VS-16", "keine Post-Werte, kein Grund", "Papierbogen Post Verein C, Anwesenheit", "Status → „Post-Testung nicht angetreten – ⟨Grund⟩“", "", ""],
    [4, "02_Rohdaten Zeile 918: VS-02 post COD_505 R Versuch 2", "ungültig „x“ ohne Wert und ohne Bemerkung (Spezifikation K5 bräche ab)", "Papierbogen Post Verein C", "Bemerkung aus dem Vokabular eintragen (Fehlversuch · Linie nicht getroffen · Kein fester Stand · System nicht aufgenommen · Nur 2 Versuche aus Zeitmangel)", "", ""],
    [5, "02_Rohdaten Zeile 989: VS-06 post COD_505 R Versuch 1", "ungültig „x“ ohne Wert und ohne Bemerkung (K5)", "Papierbogen Post Verein C", "Bemerkung aus dem Vokabular eintragen", "", ""],
    [6, "01_Personen, VS-11 Familiarisierung", "leer", "Anwesenheitsliste Familiarisierung Verein C", "1 oder 2 eintragen, sonst leer lassen (Spieler fällt dann aus FAMS)", "", ""],
    [7, "01_Personen, VS-18 Größe_prä_cm und Gewicht_prä_kg", "„?“ (Text in Zahlenspalten), %PAH deshalb nicht berechenbar", "Papierbogen Prä Verein C", "Werte nachtragen, falls auf dem Bogen vorhanden. Sonst Zellen leeren und Grund in Bemerkung („Körperhöhe und Körpermasse prä nicht erfasst“)", "", ""],
    [8, "01_Personen, VS-11 Bemerkung", "„Zeile nachträglich ergänzt – Geburtsdatum fehlt“ ist überholt (Geburtsdatum liegt vor)", "Verfasser", "Bemerkung leeren", "", ""],
    [9, "02_Rohdaten, Bemerkung „Sytem nicht aufgenommen“ (2 Zeilen) und „Fehversuch“ (1 Zeile)", "Schreibfehler, „Sytem …“ steht nicht im Vokabular der Spezifikation", "Verfasser (Tippfehler)", "→ „System nicht aufgenommen“ und „Fehlversuch“", "", ""],
    [10, "01_Personen, Testdatum_post Verein C", "Workbook 14.09.2026, Statustext und ältere Projektanweisungen 15.09.2026", "Papierbogen Post Verein C (Datum)", "Datum nach Beleg, das Alter im Datenstand hängt nur am Prätestdatum", "14.09.2026 (Workbook) gilt, per Klick 24.09.2026. Nur der Statustext wird ersetzt", "ja"],
    [11, "02_Rohdaten, VS-06 post Sprintlauf Versuch 1 (5 m 1,12 · 10 m 1,54 · 30 m 4,50)", "Abschnitt 5 bis 10 m in 0,42 s (11,9 m/s). Nach S02 gilt der ganze Lauf als auslösegestört", "Papierbogen Post Verein C", "10-m-Wert am Bogen prüfen (auch in Markierte_Werte, P3)", "", ""],
    [12, "Spezifikation S02, Hinweis", "Ein Sprintlauf wird über die gleiche Versuchsnummer in Sprint_5m, Sprint_10m und Sprint_30m gebildet. Zu bestätigen für das Datenwörterbuch", "Verfasser", "Bestätigung per Klick", "bestätigt per Klick 24.09.2026", "ja"],
]
tabelle(xo, 4, kopf, zeilen, (5, 40, 48, 30, 48, 36, 14), gelb_spalten=(6, 7))
xo.freeze_panes = "A5"

os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
xb.save(ZIEL)
print("geschrieben:", ZIEL, os.path.getsize(ZIEL), "B")

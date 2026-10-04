# -*- coding: utf-8 -*-
"""
Datenpruefung_Workbook_2026-10-01.py

Zweck:    Prüft, ob das aktuelle Workbook und der Fragebogen-Export noch genau den eingefrorenen
          Datenstand vom 24.09.2026 ergeben. Lässt dazu die Struktur- und die Exportprüfung der
          Phase 1 unverändert auf einer Kopie in einem temporären Ordner laufen und vergleicht die
          fünf Analysedateien per SHA-256 mit Statistik/Datenstand_2026-09-24. Im Datenwörterbuch
          wird nur das Datum des Datenstands in Titel und Erzeugungsangabe ersetzt, sonst Zeile für Zeile.
Schritt:  Auswertungsverfahren_2026-09-24, Vorprüfung zu Phase 8.4 (Reproduktionstest)
Eingang:  Statistik/Studiendaten_U15_gesamt.xlsx, Statistik/Datenstand_2026-09-24/ (nur lesen)
          SoSci_Fragebogen/data_test546007_2026-08-31_11-37.json und "Fragebogen Datensatz.txt"
          Claude/02_Befunde/Spezifikation_2026-09-24_Vokabular.csv und _Fragebogen.csv
          Claude/03_Skripte/Datensicherung_Struktur_2026-09-24.py und _Export_2026-09-24.py (unverändert)
Fassung:  2026-10-01, erste Fassung (Claude, Task Reproduktionstest vorbereiten)
Aufruf:   python Datenpruefung_Workbook_2026-10-01.py [Basisordner] [--aus <Datei.txt>]
          Basisordner = Ordner "Bachelorarbeit" (Voreinstellung: zwei Ebenen über dem Skript).
          Braucht openpyxl (wie die Phase-1-Skripte).
Ausgabe:  Datenpruefung_Workbook_2026-10-01.txt neben dem Skript oder die Datei aus --aus (für spätere
          Läufe, damit das Protokoll vom 01.10. erhalten bleibt). Sonst wird im Projekt nichts
          geschrieben, die Phase-1-Skripte laufen nur in der temporären Kopie.
Regeln:   Keine Namen, kein Geburtsdatum, kein Testdatum in der Ausgabe. Status 1, wenn eine
          Analysedatei abweicht oder eine Prüfung der Phase 1 nicht besteht.
"""

import sys, os, io, re, shutil, hashlib, tempfile, datetime, subprocess

FASSUNG = "2026-10-01, erste Fassung"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Windows-Konsole
except Exception:
    pass
KIND_ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
POS = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--aus"]
BASIS = os.path.abspath(POS[0]) if POS else \
    os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P_OUT = os.path.abspath(sys.argv[sys.argv.index("--aus") + 1]) if "--aus" in sys.argv else \
    os.path.splitext(os.path.abspath(__file__))[0] + ".txt"
DATEN = ["Versuchsdaten.csv", "Personendaten.csv", "Fragebogen_A.csv",
         "Zuordnung_Fragebogen.csv", "Listenplatz_IG.csv"]
EINGAENGE = [
    "Statistik/Studiendaten_U15_gesamt.xlsx",
    "SoSci_Fragebogen/data_test546007_2026-08-31_11-37.json",
    "SoSci_Fragebogen/Fragebogen Datensatz.txt",
    "Claude/02_Befunde/Spezifikation_2026-09-24_Vokabular.csv",
    "Claude/02_Befunde/Spezifikation_2026-09-24_Fragebogen.csv",
    "Claude/03_Skripte/Datensicherung_Struktur_2026-09-24.py",
    "Claude/03_Skripte/Datensicherung_Export_2026-09-24.py",
]
SHA_WB_EINFRIEREN = "d7c4ae29533429c0c8ed4acfbb9fbca3ef7e0ed092e3063532df2835c3e98642"  # Export-Laufprotokoll 24.09.

out = io.StringIO()
def w(s=""):
    out.write(s + "\n")
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()
def ende(code):
    with open(P_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out.getvalue())
    print(out.getvalue())
    sys.exit(code)

w("Datenprüfung Workbook gegen den eingefrorenen Datenstand 2026-09-24")
w("Skriptfassung " + FASSUNG + " · Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
w("Basisordner: " + BASIS)
try:
    import importlib.metadata as md
    opx = md.version("openpyxl")
except Exception:
    opx = "nicht gefunden"
w("Python " + sys.version.split()[0] + " · openpyxl " + opx)
w()
w("Eingänge (SHA-256, Größe, Dateizeit der gelesenen Datei in UTC, bei gestagten Kopien die Zeit der Kopie):")
for rel in EINGAENGE:
    p = os.path.join(BASIS, *rel.split("/"))
    if not os.path.isfile(p):
        w("  FEHLT: " + rel)
        ende(1)
    mt = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc)
    w("  %s  %s  %d B  %s" % (rel, sha256(p), os.path.getsize(p), mt.strftime("%Y-%m-%d %H:%M")))
gleich = sha256(os.path.join(BASIS, "Statistik", "Studiendaten_U15_gesamt.xlsx")) == SHA_WB_EINFRIEREN
w("Workbook-Prüfsumme gegen den Stand beim Einfrieren (d7c4ae29…, 110697 B): "
  + ("gleich" if gleich else "verschieden, die Datei wurde seither gespeichert. Entscheidend ist der Inhaltsvergleich unten."))
w()

# Eingefrorener Datenstand: Prüfsummenliste gegen die Dateien
FROZEN = os.path.join(BASIS, "Statistik", "Datenstand_2026-09-24")
soll = {}
with open(os.path.join(FROZEN, "Pruefsummen.txt"), encoding="utf-8") as f:
    for z in f:
        if z.strip():
            h, n = z.rstrip("\n").split("  ", 1)
            soll[n] = h
fehler = [n for n in soll if sha256(os.path.join(FROZEN, n)) != soll[n]]
w("Datenstand_2026-09-24, %d Dateien der Liste gegen Pruefsummen.txt: %s"
  % (len(soll), "bestanden" if not fehler else "ABWEICHUNG " + ", ".join(fehler)))
if fehler:
    ende(1)
w()

# Kopie im temporären Ordner, dort laufen die Phase-1-Skripte unverändert
gut = False
tmp = tempfile.mkdtemp(prefix="datenpruefung_")
try:
    for rel in EINGAENGE:
        ziel = os.path.join(tmp, *rel.split("/"))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copyfile(os.path.join(BASIS, *rel.split("/")), ziel)
    skripte = os.path.join(tmp, "Claude", "03_Skripte")
    lauf = {}
    for name, extra in (("Datensicherung_Struktur_2026-09-24", []),
                        ("Datensicherung_Export_2026-09-24", ["--datum", "Pruefung"])):
        r = subprocess.run([sys.executable, os.path.join(skripte, name + ".py"), tmp] + extra,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", env=KIND_ENV)
        w("Lauf %s: Status %d" % (name, r.returncode))
        if r.returncode != 0:
            w("  " + (r.stdout + r.stderr)[-600:])
            ende(1)
        with open(os.path.join(skripte, name + ".txt"), encoding="utf-8") as f:
            lauf[name] = f.read()
    s, e = lauf["Datensicherung_Struktur_2026-09-24"], lauf["Datensicherung_Export_2026-09-24"]
    for muster in (r"Verstöße, an denen die Spezifikation abbricht: \d+", r"Abbruchprobe bestanden: \w+"):
        m = re.search(muster, s)
        w("  Struktur: " + (m.group(0) if m else "Zeile fehlt: " + muster))
    for muster in (r"Gegenlesen JSON gegen TXT[^\n]*", r"Rückleseprobe bestanden: \w+", r"Abbruchprobe bestanden: \w+"):
        m = re.search(muster, e)
        w("  Export: " + (m.group(0) if m else "Zeile fehlt: " + muster))
    ok_proben = bool(re.search(r"Verstöße, an denen die Spezifikation abbricht: 0\b", s)) and \
        e.count("bestanden: ja") == 2 and bool(re.search(r"Gegenlesen JSON gegen TXT[^\n]*: 0 Abweichungen", e))
    w()
    neu = os.path.join(tmp, "Statistik", "Datenstand_Pruefung")
    w("Vergleich der Analysedateien (neu aus dem Workbook gegen Datenstand_2026-09-24):")
    abw = 0
    for n in DATEN:
        a, b = sha256(os.path.join(FROZEN, n)), sha256(os.path.join(neu, n))
        w("  %-26s %s  %s" % (n, "bytegleich" if a == b else "ABWEICHUNG", b))
        abw += a != b
    def ohne_datum(p):     # nur das Datum des Datenstands in Titel und Erzeugungsangabe ersetzen
        with open(p, encoding="utf-8") as f:
            t = f.read()
        return re.sub(r"(Datenstands|Erzeugt am) (\d{4}-\d{2}-\d{2}|Pruefung)", r"\1 <DATUM>", t).splitlines()
    dw = ohne_datum(os.path.join(FROZEN, "Datenwoerterbuch.md")) == ohne_datum(os.path.join(neu, "Datenwoerterbuch.md"))
    w("  %-26s %s" % ("Datenwoerterbuch.md", "gleich bis auf das Datum des Datenstands" if dw else "ABWEICHUNG"))
    w()
    gut = abw == 0 and dw and ok_proben
    w("Urteil: " + ("Das Workbook ergibt genau den eingefrorenen Datenstand. Kein neuer Datenstand nötig."
                    if gut else "ABWEICHUNG. Vor jeder Rechnung klären, Phase 1 für die betroffenen Zellen."))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
ende(0 if gut else 1)

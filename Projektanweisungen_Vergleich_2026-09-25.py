# -*- coding: utf-8 -*-
"""
Vergleich Projektanweisungen Fassung 14 gegen Fassung 15 und vier Prüfungen mit Abbruch
(Task Steuerdokumente, 25.09.2026, Übergabe Schritt 3).

(a) kein Semikolon außer Zitiersyntax (zwischen Quellen in einer Klammer oder das Zeichen Semikolon in Anführungszeichen als Regelgegenstand)
(b) keine Ergebniszahl in § 3 und § 11.2a (Dezimalzahl mit Einheit s, cm, %, oder p =, W =)
(c) jede Datei der Ordnerliste Claude\\ (ohne _Archiv) ist in § 1.3 genannt, unter „Veraltet“ geführt
    oder eine Anlage oder Skriptausgabe mit gleichem Namensstamm
(d) die Wortzahlen in § 5.2 stimmen mit 03_Skripte\\Manuskriptstand_2026-09-25.csv überein

Aufruf: python3 Projektanweisungen_Vergleich_2026-09-25.py <Claude-Ordner>
Ausgabe: Projektanweisungen_Vergleich_2026-09-25.txt (Liste der geänderten Absätze je Paragraf, Prüfergebnis)
Das Skript enthält kein Semikolon.
"""
import csv
import difflib
import os
import re
import sys

wurzel = sys.argv[1] if len(sys.argv) > 1 else "."
f14 = open(os.path.join(wurzel, "00_Steuerung", "Projektanweisungen_Fassung14.md"), encoding="utf-8").read()
f15 = open(os.path.join(wurzel, "00_Steuerung", "Projektanweisungen_Fassung15.md"), encoding="utf-8").read()
liste = [z.strip() for z in open(os.path.join(wurzel, "03_Skripte", "Projektanweisungen_Vergleich_2026-09-25_Ordnerliste.txt"), encoding="utf-8") if z.strip() and not z.startswith("#")]
messung = os.path.join(wurzel, "03_Skripte", "Manuskriptstand_2026-09-25.csv")
aus = []
fehler = []
SEMI = chr(59)


def abschnitte(t):
    """Text in Paragrafen nach Überschriften zerlegen: Liste (Überschrift, Absätze)."""
    teile = []
    aktuell = "Kopf"
    puffer = []
    for zeile in t.split("\n"):
        if zeile.startswith("#"):
            teile.append((aktuell, puffer))
            aktuell = zeile.strip("# ").strip()
            puffer = []
        else:
            puffer.append(zeile)
    teile.append((aktuell, puffer))
    return [(k, [a.strip() for a in "\n".join(p).split("\n\n") if a.strip()]) for k, p in teile]


def bereich(t, start, ende):
    i0 = t.index(start)
    i1 = t.index(ende, i0 + len(start))
    return t[i0:i1]


# ---------------------------------------------------------------- Vergleich
a14 = dict(abschnitte(f14))
a15 = abschnitte(f15)
aus.append("VERGLEICH Fassung 14 gegen Fassung 15 (absatzweise je Paragraf)")
aus.append("")
geaendert = 0
for kopf, absaetze in a15:
    alt = a14.get(kopf)
    if alt is None:
        # Überschrift umbenannt: nach Nummer suchen
        nr = kopf.split(" ")[0]
        kand = [k for k in a14 if k.split(" ")[0] == nr]
        alt = a14[kand[0]] if kand else []
        if kand:
            aus.append(f"[Überschrift geändert] {kand[0]}  →  {kopf}")
        else:
            aus.append(f"[neu] {kopf}")
    neu_set = [a for a in absaetze if a not in alt]
    weg_set = [a for a in alt if a not in absaetze]
    if neu_set or weg_set:
        geaendert += 1
        aus.append(f"§ {kopf}: {len(weg_set)} Absatz/Absätze ersetzt oder entfernt, {len(neu_set)} neu oder geändert")
        for a in neu_set:
            aus.append("   + " + (a[:160] + " …" if len(a) > 160 else a))
unveraendert = [k for k, _ in a15 if k in a14 and a14[k] == dict(a15)[k]]
aus.append("")
aus.append(f"Paragrafen mit Änderungen: {geaendert}, unverändert: {len(unveraendert)}")
zeilen_diff = list(difflib.unified_diff(f14.split("\n"), f15.split("\n"), lineterm="", n=0))
aus.append(f"Zeilendiff: {sum(1 for z in zeilen_diff if z.startswith('-') and not z.startswith('---'))} Zeilen entfernt, {sum(1 for z in zeilen_diff if z.startswith('+') and not z.startswith('+++'))} Zeilen hinzugefügt")

# ---------------------------------------------------------------- (a) Semikolon
aus.append("")
aus.append("PRÜFUNG (a) Semikolon außerhalb der Zitiersyntax")
treffer_a = []
for nr, zeile in enumerate(f15.split("\n"), 1):
    for m in re.finditer(SEMI, zeile):
        p = m.start()
        # erlaubt 1: das Zeichen als Regelgegenstand in typografischen Anführungszeichen
        if zeile[max(0, p - 1):p + 2] == "„" + SEMI + "“":
            continue
        # erlaubt 2: innerhalb einer Klammer, danach folgt ein Beleg Autor … Jahr
        offen = zeile.rfind("(", 0, p)
        zu = zeile.find(")", p)
        if offen != -1 and zu != -1 and zeile.rfind(")", 0, p) < offen:
            danach = zeile[p + 1:zu]
            if re.match(r"\s*[A-ZÄÖÜ][^()]*?\b(19|20)\d\d\b", danach):
                continue
        treffer_a.append(f"Zeile {nr}: …{zeile[max(0, p - 40):p + 40]}…")
if treffer_a:
    fehler.append("(a)")
    aus.extend("   " + t for t in treffer_a)
aus.append(f"   Ergebnis: {'NICHT BESTANDEN' if treffer_a else 'bestanden'} ({len(treffer_a)} Fundstellen)")

# ---------------------------------------------------------------- (b) Ergebniszahlen
aus.append("")
aus.append("PRÜFUNG (b) keine Ergebniszahl in § 3 und § 11.2a")
muster_b = re.compile(r"[−+-]?\d+,\d+\s*(s\b|cm\b|%)|\bp\s*[=<>]\s*0,\d|\bW\s*=\s*0,\d")
treffer_b = []
for name, (s, e) in {"§ 3": ("# 3. DATENSTAND", "# 4. "), "§ 11.2a": ("## 11.2a ", "## 11.2b ")}.items():
    for m in muster_b.finditer(bereich(f15, s, e)):
        treffer_b.append(f"{name}: {m.group(0)}")
if treffer_b:
    fehler.append("(b)")
    aus.extend("   " + t for t in treffer_b)
aus.append(f"   Ergebnis: {'NICHT BESTANDEN' if treffer_b else 'bestanden'} ({len(treffer_b)} Fundstellen)")

# ---------------------------------------------------------------- (c) Dokumentenkarte
aus.append("")
aus.append("PRÜFUNG (c) jede Datei der Ordnerliste in § 1.3 genannt, veraltet oder Anlage mit gleichem Namensstamm")
karte = bereich(f15, "## 1.3 Dokumentenkarte", "## 1.4 ")
roh = set(re.findall(r"`([^`]+)`", karte))
roh |= set(re.findall(r"[A-Za-z0-9ÄÖÜäöüß_.\-…*]+_\d{4}-\d{2}-\d{2}[A-Za-z0-9_.\-]*", karte))
roh |= set(re.findall(r"\b[A-Za-z0-9ÄÖÜäöüß\-]+_[A-Za-z0-9ÄÖÜäöüß_\-]+", karte))
marken = set()
for r in roh:
    for teil in re.split(r"[\\/ ,]+", r):
        teil = teil.strip("`() .")
        if len(teil) < 4:
            continue
        teil = re.sub(r"\.(md|docx|pdf|py|txt|csv|xlsx|R|zip|png|sps)$", "", teil)
        marken.add(teil)


ORDNER = {"Claude", "00_Steuerung", "01_Verfahren", "02_Befunde", "03_Skripte", "04_Uebergaben", "05_Protokolle", "06_Abbildungen", "_Archiv"}
marken = {m for m in marken if m not in ORDNER and len(re.sub(r"[*….]", "", m)) >= 4}


def passt(marke, name):
    """Namensstamm gleich oder Anlage mit gleichem Stamm (nächstes Zeichen _ oder Ende), Muster mit * oder …"""
    if "*" in marke or "…" in marke:
        teile = re.split(r"[*…]", marke.replace("B0…B9", "B§"))
        rx = "^" + ".*".join(re.escape(t).replace("§", "[0-9]") for t in teile) + ".*$"
        return re.match(rx, name) is not None
    return name == marke or name.startswith(marke + "_")


offen_c = []
for pfad in liste:
    teile = pfad.split("/")
    namen = [re.sub(r"\.[A-Za-z0-9]+$", "", t) for t in teile]
    if any(passt(m, n) for m in marken for n in namen):
        continue
    offen_c.append(pfad)
if offen_c:
    fehler.append("(c)")
    aus.extend("   nicht zugeordnet: " + p for p in offen_c)
aus.append(f"   Ergebnis: {'NICHT BESTANDEN' if offen_c else 'bestanden'} ({len(liste)} Dateien geprüft, {len(offen_c)} ohne Zuordnung)")

# ---------------------------------------------------------------- (d) Wortzahlen § 5.2
aus.append("")
aus.append("PRÜFUNG (d) Wortzahlen in § 5.2 gegen Manuskriptstand_2026-09-25.csv")
w = {}
with open(messung, encoding="utf-8") as f:
    for z in csv.DictReader(f):
        w[z["nr"]] = int(z["woerter"])
soll = {
    "4.1": w["4.1"], "4.2": w["4.2"], "4.3": w["4.3"],
    "4.4 mit 4.4.1 bis 4.4.3": w["4.4"] + w["4.4.1"] + w["4.4.2"] + w["4.4.3"],
    "4.5.1": w["4.5.1"], "4.5.2": w["4.5.2"], "4.6": w["4.6"], "4.7": w["4.7"],
}
soll["Kapitel 4 (4.1 bis 4.6)"] = sum(soll[k] for k in ["4.1", "4.2", "4.3", "4.4 mit 4.4.1 bis 4.4.3", "4.5.1", "4.5.2", "4.6"])
soll["mit 4.7"] = soll["Kapitel 4 (4.1 bis 4.6)"] + soll["4.7"]
soll["Kapitel 2 (2.1 bis 2.4)"] = w["2.1"] + w["2.2"] + w["2.3"] + w["2.4"] + w["2.4.1"] + w["2.4.2"] + w["2.4.3"]
soll["Absatztext Kapitel 1 bis 7"] = sum(v for k, v in w.items() if re.match(r"^[1-7](\.|$)", k))
soll["Kürzungsauftrag"] = (soll["Kapitel 2 (2.1 bis 2.4)"] - 2950) + (soll["mit 4.7"] - 2550)
b52 = bereich(f15, "## 5.2 Wortbudget", "## 5.3 ")
stand = b52[b52.index("**Stand am Master"):]
stand = stand[:stand.index("⚠")]
treffer_d = []
geprueft = 0
for etikett, wert in soll.items():
    m = re.search(re.escape(etikett) + r"\)?\s+(\d{1,3}(?:\.\d{3})+|\d+)(?![\d.]\d)", stand)
    if not m:
        treffer_d.append(f"{etikett}: im Satz „Stand am Master“ nicht gefunden")
        continue
    geprueft += 1
    gelesen = int(m.group(1).replace(".", ""))
    if gelesen != wert:
        treffer_d.append(f"{etikett}: § 5.2 nennt {gelesen}, Messung {wert}")
# Absatz „Was das bedeutet“ und Kapitelzeilen
def de(n):
    return f"{n:,}".replace(",", ".")
for erwartet in [f"**{de(soll['Absatztext Kapitel 1 bis 7'])} Wörter**", f"**{de(soll['Kürzungsauftrag'])} Wörter",
                 f"Kapitel 2 mit 2.1 bis 2.4 {de(soll['Kapitel 2 (2.1 bis 2.4)'])}", f"Kapitel 4 mit 4.1 bis 4.7 {de(soll['mit 4.7'])}",
                 f"**Kapitel 2: −{de(soll['Kapitel 2 (2.1 bis 2.4)'] - 2950)}**", f"**Kapitel 4: −{de(soll['mit 4.7'] - 2550)}**",
                 f"darin 4.7 von {de(soll['4.7'])} auf 550"]:
    geprueft += 1
    if erwartet not in b52:
        treffer_d.append(f"nicht gefunden: {erwartet}")
if treffer_d:
    fehler.append("(d)")
    aus.extend("   " + t for t in treffer_d)
aus.append(f"   Ergebnis: {'NICHT BESTANDEN' if treffer_d else 'bestanden'} ({geprueft} Werte geprüft)")

aus.append("")
aus.append("GESAMT: " + ("ABBRUCH, nicht bestanden: " + " ".join(fehler) if fehler else "alle vier Prüfungen bestanden"))
ziel = os.path.join(wurzel, "03_Skripte", "Projektanweisungen_Vergleich_2026-09-25.txt")
open(ziel, "w", encoding="utf-8").write("\n".join(aus) + "\n")
print("\n".join(aus[-40:]))
sys.exit(1 if fehler else 0)

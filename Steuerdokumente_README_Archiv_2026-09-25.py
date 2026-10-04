# -*- coding: utf-8 -*-
"""
README_Ordnerstruktur.md und Ordner_aufraeumen.ps1 fortschreiben, Archivkopien anlegen
(Task Steuerdokumente, 25.09.2026, Übergabe Schritte 4 und 5, Klickantwort „Gruppiert, Erledigtes ins Archiv“).

Jede Textstelle wird genau einmal ersetzt, sonst Abbruch. Das Aufräumskript behält BOM und CRLF.
Mit --fassung14 kommen zusätzlich die Archivkopie und der Papierkorbeintrag für Fassung 14 dazu
(nur nach der Klickantwort „Fassung 15 einsetzen“, Maßnahme A8).
Das Skript enthält kein Semikolon.

Aufruf: python3 Steuerdokumente_README_Archiv_2026-09-25.py <Claude-Ordner> <Quellordner der Übergaben> [--fassung14]
"""
import hashlib
import os
import shutil
import sys

wurzel = sys.argv[1]
quelle_ueb = sys.argv[2]
mit_f14 = "--fassung14" in sys.argv
protokoll = []


def ersetze(text, alt, neu, stelle):
    n = text.count(alt)
    if n != 1:
        sys.exit(f"ABBRUCH: {stelle}: Fundstelle {n}-mal statt genau einmal")
    protokoll.append(stelle)
    return text.replace(alt, neu)


# ---------------------------------------------------------------- README
p = os.path.join(wurzel, "README_Ordnerstruktur.md")
t = open(p, encoding="utf-8").read()
t = ersetze(t, "(Projektanweisungen § 1.4, Fassung 14 vom 24.09.2026, seit 25.09. in den Projekteinstellungen wirksam). Stand dieser Datei: 25.09.2026, nachmittags.",
            "(Projektanweisungen § 1.4, Fassung 15 vom 25.09.2026). Stand dieser Datei: 25.09.2026, abends (Task Steuerdokumente).",
            "README Kopf")
t = ersetze(t, "`Projektanweisungen_Fassung14.md` (Sicherung, wirksam in den Projekteinstellungen) | **Genau drei Dateien.** Fassung 10 bis 12 gehen per Skript in den Papierkorb |",
            "`Projektanweisungen_Fassung15.md` (Sicherung der Fassung in den Projekteinstellungen) | **Genau drei Dateien.** Fassung 14 geht nach dem Einsetzen von Fassung 15 per Skript in den Papierkorb, Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14` |",
            "README 00_Steuerung")
t = ersetze(t, "`Abgleichprotokoll_Manuskript_2026-09-25` (Phase 7.3, Vorschlagsliste für den Master)",
            "`Abgleichprotokoll_Manuskript_2026-09-25` (Phase 7.3, Endabgleich Fassung 3)",
            "README Endabgleich")
t = ersetze(t, "`Auswertungsplan_2026-09-12` (Register § 5.10, R1 bis R13)", "`Auswertungsplan_2026-09-12` (Register § 5.10, R1 bis R14)", "README Register 02")
t = ersetze(t, "· `Programmkennzahlen_2026-09-23` · `Korpus_*` · Werkzeuge |",
            "· `Programmkennzahlen_2026-09-23` · `Manuskriptstand_2026-09-25` (Messung des Masters je Abschnitt) · `Projektanweisungen_Fassung15_2026-09-25.py` mit `Projektanweisungen_Vergleich_2026-09-25` · `R_citation_2026-09-25.txt` (Zitierform von R) · `Korpus_*` · Werkzeug- und Steuerungsskripte |",
            "README 03_Skripte")
t = ersetze(t, "| `04_Uebergaben` | `Handprobe_2026-09-25.xlsx` (Fassung 2, Formelprobe) · `Belegpruefung_2026-09-24.xlsx` · offene Übergaben und Textvorschläge (4.3, 4.4, 4.5.1, 4.6, Textrevision, Datensicherung und Blindrechnung als Prompt-Belege für die KI-Deklaration) | Nach Erledigung in den Papierkorb oder ins `_Archiv` |",
            "| `04_Uebergaben` | **`Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2, Reihenfolge der Arbeit)** · `Uebergabe_Steuerdokumente_2026-09-25.md` · Eingänge der Textrevision Kapitel 4 (Übergaben 4.3, 4.4, 4.5.1, 4.6, Textvorschläge 4.5.1 und 4.7, `Uebergabe_Textrevision_2026-09-12.md`) · `Handprobe_2026-09-25.xlsx` (Fassung 2, Formelprobe) · `Belegpruefung_2026-09-24.xlsx` | Nach Erledigung Kopie ins `_Archiv\\_ersetzt_⟨Datum⟩_Uebergaben` (Prompt-Belege für die KI-Deklaration), Original über das Aufräumskript in den Papierkorb |",
            "README 04_Uebergaben")
t = ersetze(t, "(Nachtrag 2, Nachtrag 3, Kennzahlen 22.09.)", "(Nachtrag 2, Nachtrag 3, Kennzahlen 22.09., Übergaben 25.09., Fassung 14)", "README _Archiv")

a0 = t.index("## Was wo gilt")
a1 = t.index("## Schritt für Schritt")
neu_wwg = """## Was wo gilt (Stand 25.09.2026, abends)

Fünf Dokumente steuern das Schreiben. Jedes beantwortet eine Frage und ändert sich in seinem eigenen Rhythmus (Berichtsraster § 6: nicht zusammenführen).

| Dokument | Frage | Ändert sich, wenn … |
|---|---|---|
| `02_Befunde\\Berichtsraster_2026-09-23` (Rev. 2) | Was muss in den Abschnitt, was nicht? | eine Norm neu geprüft oder ein Abschnitt fertig wird |
| `02_Befunde\\Bauplan_Vergleichskorpus_2026-09-15` | In welcher Reihenfolge, mit welchen Zügen? | nie (gemessen an elf publizierten Studien), nur Errata |
| `02_Befunde\\Auswertungsplan_2026-09-12` § 5 mit Register § 5.10 · `Spezifikation_2026-09-24` · `Kennzahlen_2026-09-25.md` | Was wird wie gerechnet, wo weicht es vom Antrag ab, welche Zahl aus welcher Bezugsmenge? | ein Nachtrag zur Spezifikation entsteht oder der Datenstand neu läuft. Das Kennzahlenblatt entsteht nur per Skript |
| `01_Verfahren\\Stilprofil_2026-09-13.md` | Wie klingt der Satz? | der Verfasser eine Stilfestlegung trifft |
| `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) | Was kommt als Nächstes, mit welchem Budget? | ein Task abgeschlossen ist oder der Verfasser die Reihenfolge ändert |

Darüber stehen die Projektanweisungen (Fassung 15, Sicherung in `00_Steuerung`) und der Arbeitsstand in `00_Steuerung\\Cowork_Sitzungsnotizen.md`, Teil 0. Teil 0 ist die einzige Wahrheitsquelle für den Stand, das Projektdokument ist eine Kopie.

**Stand in Kürze:** Die Auswertung ist abgeschlossen (Phasen 0 bis 7, F2 und F3 am 25.09.). Zahlen kommen allein aus dem Kennzahlenblatt 25.09. (Rev. 2), im Manuskript steht keine Kennung. Die Budgets nach Projektanweisungen § 5.2 sind Vorgabe, 4.7 wird von 721 auf 550 zurückgeführt. Reihenfolge: Kürzung der vorhandenen Kapitel vor neuen Kapiteln, Anhänge zuletzt (Plan, Tasks 2 bis 18). Grafiken werden erst am Ende eingefügt, im Master stehen Platzhalter.

**Überholte Teile anderer Dokumente** (Vermerk nur hier und in Projektanweisungen § 1.3, nicht in den Dokumenten selbst): `CONSORT_Auswertung_und_Umsetzung_2026-09-09` § 4 (Vorschlagsliste) und Fallzahlangaben · Ist-Spalten von `Manuskriptstand_und_Vollstaendigkeit_2026-09-13` (ersetzt durch `03_Skripte\\Manuskriptstand_2026-09-25`) · Bauplan § 1, Zählung der Schlusskapitel: gemeint sind vier Studien ohne Fazitkapitel, nicht „vier weder noch“ · Analyseprotokoll 15.09. und Python-Kette B0 bis B9 nur als Arbeitsstand vor dem Abgleich, keine Zahlenquelle · Auswertungsverfahren 7.3, Umfangsdokument § 3.2, Berichtsraster 4.2.5, 3.11 und 4.7.13 und Kopf des Kennzahlenblatts mit Nachtragsvermerk (Projektanweisungen § 1.3).

"""
t = t[:a0] + neu_wwg + t[a1:]
protokoll.append("README Was wo gilt")
zusatz = "erledigte Übergaben und Textvorschläge (Datensicherung und Blindrechnung vom 24.09., 4.1 vom 22.09., Textvorschläge 4.1 und 4.2, Sofortblock, Kopien in `_Archiv\\_ersetzt_2026-09-25_Uebergaben`)"
if mit_f14:
    zusatz += " · Fassung 14 der Projektanweisungen, sobald Fassung 15 in den Projekteinstellungen steht (Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14`)"
t = ersetze(t, "Was im Papierkorb landet, steht als feste Liste im Skript: Projektanweisungen Fassung 10 bis 12 ·",
            "Was im Papierkorb landet, steht als feste Liste im Skript: Projektanweisungen Fassung 10 bis 12 · " + zusatz + " ·",
            "README Papierkorbliste")
open(p, "w", encoding="utf-8", newline="\n").write(t)

# ---------------------------------------------------------------- Aufräumskript (BOM, CRLF)
p = os.path.join(wurzel, "Ordner_aufraeumen.ps1")
roh = open(p, "rb").read()
assert roh.startswith(b"\xef\xbb\xbf") and b"\r\n" in roh
s = roh[3:].decode("utf-8").replace("\r\n", "\n")
s = ersetze(s, "#  Stand 25.09.2026 (nachmittags). Ersetzt die Fassung vom 24.09.2026.",
            "#  Stand 25.09.2026 (abends, Task Steuerdokumente). Ersetzt die Fassung vom 25.09.2026 (nachmittags).",
            "ps1 Kopf")
ueb = """  'Claude\\04_Uebergaben\\Uebergabe_Spezifikation_2026-09-24.md',
"""
neu_ueb = ueb + """  # Task Steuerdokumente 25.09.: erledigt, Kopien in Claude\\_Archiv\\_ersetzt_2026-09-25_Uebergaben
  'Claude\\04_Uebergaben\\Uebergabe_Datensicherung_2026-09-24.md',
  'Claude\\04_Uebergaben\\Uebergabe_Blindrechnung_R_2026-09-24.md',
  'Claude\\04_Uebergaben\\Uebergabe_4.1_Studiendesign_2026-09-22.md',
  'Claude\\04_Uebergaben\\Textvorschlag_4.1_2026-09-23.md',
  'Claude\\04_Uebergaben\\Textvorschlag_4.2_2026-09-22.md',
  'Claude\\04_Uebergaben\\Befunde_Sofortblock_2026-09-13.md',
"""
s = ersetze(s, ueb, neu_ueb, "ps1 Übergaben")
if mit_f14:
    f12 = """  'Claude\\00_Steuerung\\Projektanweisungen_Fassung12.md',
"""
    s = ersetze(s, f12, f12 + """  # Fassung 14: erst laufen lassen, wenn Fassung 15 in den Projekteinstellungen steht (A8). Kopie in Claude\\_Archiv\\_ersetzt_2026-09-25_Fassung14
  'Claude\\00_Steuerung\\Projektanweisungen_Fassung14.md',
""", "ps1 Fassung 14")
    s = ersetze(s, "muster = @('Cowork_Sitzungsnotizen.md','Massnahmenliste_Datenverarbeitung.md','Projektanweisungen_Fassung14.md')",
                "muster = @('Cowork_Sitzungsnotizen.md','Massnahmenliste_Datenverarbeitung.md','Projektanweisungen_Fassung15.md')",
                "ps1 Steuerungsmuster")
open(p, "wb").write(b"\xef\xbb\xbf" + s.replace("\n", "\r\n").encode("utf-8"))

# ---------------------------------------------------------------- Archivkopien
kopien = [("_ersetzt_2026-09-25_Uebergaben", n) for n in [
    "Uebergabe_Datensicherung_2026-09-24.md", "Uebergabe_Blindrechnung_R_2026-09-24.md",
    "Uebergabe_4.1_Studiendesign_2026-09-22.md", "Textvorschlag_4.1_2026-09-23.md",
    "Textvorschlag_4.2_2026-09-22.md", "Befunde_Sofortblock_2026-09-13.md"]]
for ordner, name in kopien:
    z = os.path.join(wurzel, "_Archiv", ordner)
    os.makedirs(z, exist_ok=True)
    shutil.copy2(os.path.join(quelle_ueb, "04_Uebergaben", name), os.path.join(z, name))
if mit_f14:
    z = os.path.join(wurzel, "_Archiv", "_ersetzt_2026-09-25_Fassung14")
    os.makedirs(z, exist_ok=True)
    shutil.copy2(os.path.join(quelle_ueb, "00_Steuerung", "Projektanweisungen_Fassung14.md"), os.path.join(z, "Projektanweisungen_Fassung14.md"))
    kopien.append(("_ersetzt_2026-09-25_Fassung14", "Projektanweisungen_Fassung14.md"))

print(f"Ersetzungen ({len(protokoll)}), je genau einmal: " + " · ".join(protokoll))
for ordner, name in kopien:
    q = os.path.join(wurzel, "_Archiv", ordner, name)
    print(f"Archivkopie _Archiv\\{ordner}\\{name}  SHA-256 {hashlib.sha256(open(q, 'rb').read()).hexdigest()}")
print("Fassung 14 einbezogen: " + ("ja" if mit_f14 else "nein"))

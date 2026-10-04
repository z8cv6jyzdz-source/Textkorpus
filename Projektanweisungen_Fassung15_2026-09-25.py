# -*- coding: utf-8 -*-
"""
Projektanweisungen Fassung 15 aus Fassung 14 erzeugen (Task Steuerdokumente, 25.09.2026).

Grundlage: 04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md, Schritt 2 (Aenderungsliste je Paragraf).
Jede Ersetzung muss genau einmal greifen, sonst Abbruch. Wortzahlen kommen aus
03_Skripte\\Manuskriptstand_2026-09-25.csv, keine Zahl von Hand. Budgets sind die Vorgabe aus F14 § 5.2.
Das Skript enthaelt kein Semikolon.

Aufruf: python3 Projektanweisungen_Fassung15_2026-09-25.py <Claude-Ordner>
"""
import csv
import hashlib
import os
import re
import sys

wurzel = sys.argv[1] if len(sys.argv) > 1 else "."
quelle = os.path.join(wurzel, "00_Steuerung", "Projektanweisungen_Fassung14.md")
ziel = os.path.join(wurzel, "00_Steuerung", "Projektanweisungen_Fassung15.md")
messung = os.path.join(wurzel, "03_Skripte", "Manuskriptstand_2026-09-25.csv")

text = open(quelle, encoding="utf-8").read()
sha14 = hashlib.sha256(text.encode("utf-8")).hexdigest()


def de(n):
    return f"{n:,}".replace(",", ".")


# ---------------------------------------------------------------- Messung lesen
w = {}
with open(messung, encoding="utf-8") as f:
    for z in csv.DictReader(f):
        w[z["nr"]] = int(z["woerter"])


def summe(*schluessel):
    return sum(w[k] for k in schluessel)


ist = {
    "4.1": w["4.1"], "4.2": w["4.2"], "4.3": w["4.3"],
    "4.4": summe("4.4", "4.4.1", "4.4.2", "4.4.3"),
    "4.5.1": w["4.5.1"], "4.5.2": w["4.5.2"], "4.6": w["4.6"], "4.7": w["4.7"],
    "2.1": w["2.1"], "2.2": w["2.2"], "2.3": w["2.3"],
    "2.4": summe("2.4", "2.4.1", "2.4.2", "2.4.3"),
}
kap4_46 = sum(ist[k] for k in ["4.1", "4.2", "4.3", "4.4", "4.5.1", "4.5.2", "4.6"])
kap4_47 = kap4_46 + ist["4.7"]
kap2 = sum(ist[k] for k in ["2.1", "2.2", "2.3", "2.4"])
kapitel = [k for k in w if re.match(r"^[1-7](\.|$)", k)]
gesamt = sum(w[k] for k in kapitel)
vorgabe = {"1": 600, "2.1": 800, "2.2": 850, "2.3": 600, "2.4": 700, "2.5": 400, "3": 200,
           "4.1": 300, "4.2": 215, "4.3": 340, "4.4": 420, "4.5.1": 420, "4.5.2": 150, "4.6": 155,
           "4.7": 550, "5.1": 230, "5.2": 220, "6.1": 700, "6.2": 400, "6.3": 500, "7": 250}
budget_kap2 = sum(vorgabe[k] for k in ["2.1", "2.2", "2.3", "2.4"])
budget_kap4 = sum(vorgabe[k] for k in ["4.1", "4.2", "4.3", "4.4", "4.5.1", "4.5.2", "4.6", "4.7"])
leer = [k for k in vorgabe if w.get(k, 0) == 0 and k not in ("4.4",)]
budget_leer = sum(vorgabe[k] for k in leer)
kuerz2 = kap2 - budget_kap2
kuerz4 = kap4_47 - budget_kap4
kuerz47 = ist["4.7"] - vorgabe["4.7"]
kuerz = kuerz2 + kuerz4
assert gesamt == kap2 + kap4_47, "Absatztext Kapitel 1 bis 7 ist nicht Kapitel 2 plus Kapitel 4"
anteil = f"{100 * kuerz / gesamt:.1f}".replace(".", ",")
leer_namen = ", ".join(k for k in ["1", "2.5", "3", "5.1", "5.2", "6.1", "6.2", "6.3", "7"] if k in leer)

# ---------------------------------------------------------------- Ersetzungen
ersetzungen = []


def ers(alt, neu, stelle):
    ersetzungen.append((alt, neu, stelle))


# Kopf ---------------------------------------------------------------------------
kopf_alt_beginn = "Fassung 14, Stand 24.09.2026, abends"
kopf_alt_ende = "die zwei Meldungen von HL-03 am 09.08. sind entschieden (§ 3.2).\n"
i0 = text.index(kopf_alt_beginn)
i1 = text.index(kopf_alt_ende) + len(kopf_alt_ende)
assert i0 == 0 and text.count(kopf_alt_ende) == 1
kopf_neu = f"""Fassung 15, Stand 25.09.2026, abends (ersetzt Fassung 14 vom 24.09.2026)

**Wirksam wird diese Fassung erst, wenn der Verfasser sie in die Projekteinstellungen einsetzt (Maßnahme A8).** Bis dahin gilt dort Fassung 14. Sicherung: `Claude\\00_Steuerung\\Projektanweisungen_Fassung15.md`, Projektkopie `claude/Projektanweisungen_Fassung15.md`. Erzeuger `Claude\\03_Skripte\\Projektanweisungen_Fassung15_2026-09-25.py`, Vergleich mit Fassung 14 in `Claude\\03_Skripte\\Projektanweisungen_Vergleich_2026-09-25.txt`.

Neu in Fassung 15 — sechs Änderungen, die alles Weitere steuern:

**(1) Die Auswertung ist abgeschlossen.** Die Phasen 0 bis 7 des Auswertungsverfahrens liefen am 24. und 25.09., F2 und F3 hat der Verfasser am 25.09. erteilt. Berichtet wird die Rechnung in R 4.3.3 der blinden zweiten Instanz (`03_Skripte\\Abgabe_R_2026-09-25`). Der Abgleich je Kennung mit der Python-Gegenprobe und die Handprobe sind bestanden. Zahlenquelle ist allein `02_Befunde\\Kennzahlen_2026-09-25.md` (Rev. 2, § 1.2, § 3, § 11.10).

**(2) Im Manuskript stehen keine Kennungen.** Die Rückverfolgbarkeit läuft über die Zahlenliste des Endabgleichs, die Kennungen stehen im Begleitteil des Textvorschlags (Verfasser 25.09., § 1.2).

**(3) Die Vorgabe gilt.** Die Budgets nach § 5.2 sind verbindlich, ohne Anhebung und ohne Gegenfinanzierung. Kein Textvorschlag liegt über dem Budget seines Abschnitts (Verfasser 25.09., abends). 4.7 steht mit {de(ist['4.7'])} Wörtern im Master und wird auf {de(vorgabe['4.7'])} zurückgeführt (§ 5.2, § 13).

**(4) Kürzung vor Neuem.** Die Reihenfolge folgt dem Plan der weiteren Schritte (Rev. 2): Die vorhandenen Kapitel werden gekürzt, bevor neue geschrieben werden. Die Anhänge kommen ganz zum Schluss (§ 5.2, § 13).

**(5) Die Kennwerte der Stichprobe stehen in 4.2.** Alter, Körperhöhe, Körpermasse und %PAH der Analysepopulation stehen im Text von 4.2. Tab. 2 führt nur die Ausgangswerte der Zielgrößen (Verfasser 25.09., § 5.3).

**(6) Die Maßnahmenliste ist bereinigt (Rev. 97).** Jeder offene Punkt ist einem Task des Plans zugeordnet (Zusammenfassung der Maßnahmenliste).

⚠ Korrekturen gegenüber Fassung 14: Errata E1 bis E5 zur Gliederung v4 aus dem Prüfprotokoll vom 23.09. übernommen (§ 5.1) · Familiarisierung KG nach K-01.13 „13× zwei“ (§ 2) · Kennungsbezüge auf das Kennzahlenblatt 25.09. umgestellt: Nenner je Zielgröße in K-04 und K-06, Versuche in K-11, K-02 gilt nur für die Analysepopulation (§ 2, § 3) · Erratum Khamis & Roche (1995) nicht beschaffbar und nicht eingesehen (§ 2, § 6.5) · L21 erledigt, `Dashboard\\daten\\` entfernt (§ 1.3) · Zitierform von R aus `citation()` in R 4.3.3 (§ 8, § 15) · Freigaben F2 und F3 nachgetragen (§ 1.5).
"""
text = kopf_neu + text[i1:]

# § 1.2 -------------------------------------------------------------------------
ers("""Verfahrensoption für die Textrevision (Empfehlung 12.09., ⟨Freigabe Verfasser⟩): Entscheidungen weiterhin als Vorschlagsliste, alle Textänderungen als Word-Änderungsverfolgung (Autor „Claude") in den Master, ein Commit je Abschnitt, Freigabe = Annehmen/Ablehnen in Word. Regeln und Werkzeugkette in `Uebergabe_Textrevision_2026-09-12.md` § 5a.""",
    """Verfahren (seit 22.09., bestätigt 25.09.): Textvorschlag als Datei in `04_Uebergaben` mit gemessenem Kopf, Zug-Tabelle und Kennungen je Zahl im Begleitteil, unabhängige Zweitprüfung durch einen Subagenten, Klickfreigabe je Abschnitt, Einbau per Skript, Endabgleich, Rev. in Teil 0. Die Zielwortzahl ist das Budget des Abschnitts nach § 5.2. Ein Textvorschlag über dem Budget wird nicht vorgelegt, eine Kürzungsleiter zeigt den Weg bis zum Budget (Verfasser 25.09.).""",
    "§ 1.2 Verfahren")
ers("""3. `Claude\\02_Befunde\\Kennzahlen_2026-09-22.md` (Rev. 4, mit Bezugsmengen-Regel) — **Zahlenquelle bis zum Abgleich der Blindrechnung**. Jede Zahl im Manuskript trägt eine Kennung aus diesem Blatt. Nach Phase 7.1 des Auswertungsverfahrens gilt allein das neue Kennzahlenblatt. Programmzahlen""",
    """3. `Claude\\02_Befunde\\Kennzahlen_2026-09-25.md` (Rev. 2, mit Bezugsmengen-Regel) — **Zahlenquelle**, Erzeuger `Claude\\03_Skripte\\Kennzahlen_2026-09-25.py`. Im Manuskript steht keine Kennung. Jede Zahl ist über die Zahlenliste des Endabgleichs (`03_Skripte\\Endabgleich_Manuskript_2026-09-25_Zahlen.csv`) auf ihre Kennung rückverfolgbar, die Kennungen stehen im Begleitteil des Textvorschlags. Programmzahlen""",
    "§ 1.2 Nr. 3")
ers("""`Claude\\02_Befunde\\Auswertungsplan_2026-09-12` § 5 mit § 5.10, `Claude\\02_Befunde\\Auswertungs_und_Berichtsumfang""",
    """`Claude\\02_Befunde\\Auswertungsplan_2026-09-12` § 5 mit § 5.10 (R1 bis R14), `Claude\\02_Befunde\\Auswertungs_und_Berichtsumfang""",
    "§ 1.2 Nr. 6")
ers("""8. Skill `kapiteltext-bachelorarbeit`.
""",
    """8. Skill `kapiteltext-bachelorarbeit`.
9. `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) — Reihenfolge, Budgets, Klickfragen, Startsätze.
""",
    "§ 1.2 Nr. 9")
ers("""(bis zum Abgleich `Claude\\03_Skripte\\Kennzahlen_2026-09-22.py`, danach das Skript aus Phase 7.1)""",
    """(`Claude\\03_Skripte\\Kennzahlen_2026-09-25.py`)""",
    "§ 1.2 Zahlenregel")

# § 1.3 -------------------------------------------------------------------------
ers("""| `Claude\\02_Befunde\\Kennzahlen_2026-09-22.md` | **Zahlenquelle des Manuskripts bis zum Abgleich.** Kennungen K-01 bis K-08 mit Bezugsmengen-Regel. Erzeuger `Claude\\03_Skripte\\Kennzahlen_2026-09-22.py` |""",
    """| `Claude\\02_Befunde\\Kennzahlen_2026-09-25.md` (Rev. 2) | **Zahlenquelle des Manuskripts.** Kennungen K-01 bis K-12 mit Bezugsmengen-Regel, Anlage `Kennzahlen_2026-09-25_Werte.csv`. Erzeuger `Claude\\03_Skripte\\Kennzahlen_2026-09-25.py` |""",
    "§ 1.3 Kennzahlen")
ers("""| `Claude\\02_Befunde\\Analyseprotokoll_2026-09-15.md` | Erste Rechnung (Python, 15.09.): Hauptanalyse, Sensitivitätsvarianten, Voraussetzungsprüfungen. Arbeitsstand bis zum Abgleich |
| `Claude\\04_Uebergaben\\Uebergabe_Datensicherung_2026-09-24.md` | Prompt für Phase 1 (Task im Projekt) |
| `Claude\\04_Uebergaben\\Uebergabe_Blindrechnung_R_2026-09-24.md` | Vorbereitung des Blindordners und Prompt für die Blindrechnung (neuer Chat außerhalb des Projekts). Nicht in den Blindordner |""",
    """| `Claude\\02_Befunde\\Analyseprotokoll_2026-09-15.md` | Erste Rechnung (Python, 15.09.). Arbeitsstand vor dem Abgleich, lesbar, keine Zahlenquelle |
| `Claude\\03_Skripte\\Abgabe_R_2026-09-25` (Ordner, dazu `.zip`) | **Berichtete Rechnung** der blinden zweiten Instanz: `Ergebnisse_R_2026-09-25.csv` mit SHA-256, Skripte S01 bis S19 mit Gesamtlauf und Funktionen, Laufprotokoll, Umgebung, Rückfragen- und Übergabeprotokoll |
| `Claude\\03_Skripte\\Gegenprobe_Python_2026-09-25.py` mit `Ergebnisse_Python_2026-09-25.csv` | Gegenprobe der ersten Instanz (Phase 5). `Abgabe_Kopie_2026-09-25.py` kopiert die Abgabe in den Ordner |
| `Claude\\02_Befunde\\Abgleichprotokoll_2026-09-25` (.md, .docx, .pdf), `Abgleich_2026-09-25.csv` mit `_Protokoll.txt` | Phase 6.1: Abgleich je Kennung, bestanden |
| `Claude\\02_Befunde\\Durchsichtsprotokoll_2026-09-25` · `Plausibilitaetsprotokoll_2026-09-25` (.md, .docx, .pdf) | Phase 6.2 Durchsicht und 6.4 Plausibilität, Skript `Plausibilitaet_2026-09-25.py` |
| `Claude\\04_Uebergaben\\Handprobe_2026-09-25.xlsx` | Phase 6.3 Handprobe, Urteil B4, Skripte `Handprobe_2026-09-25.py` und `Handprobe_Pruefung_2026-09-25.py` |
| `Claude\\02_Befunde\\Belegprotokoll_2026-09-24` (.docx, .pdf) mit `04_Uebergaben\\Belegpruefung_2026-09-24.xlsx` | Phase 1.1 Datensicherung, Skripte `Datensicherung_*_2026-09-24` |
| `Claude\\02_Befunde\\Abgleichprotokoll_Manuskript_2026-09-25` (.md, .docx, .pdf) | Endabgleich 7.3 (Fassung 3), Skript `Endabgleich_Manuskript_2026-09-25.py` mit Laufprotokoll und Zahlenliste `_Zahlen.csv` in `03_Skripte` |
| `Claude\\03_Skripte\\Objekte_2026-09-25` (Ordner) mit `Objekte_2026-09-25.R` und `06_Abbildungen` | Objekte aus der Ergebnisdatei (7.2): Tab. 1 bis 3, Tab. H1 bis H5 als CSV, Abb. 1, Abb. 2, Abb. H7, Word-Vorlage `Objekte_2026-09-25.docx`. `Objekte_2026-09-25_synthetisch` ist die Probe mit synthetischen Daten |
| `Claude\\03_Skripte\\Manuskriptstand_2026-09-25` (.py, .txt, .csv) | Messung des Masters je Abschnitt (Wörter, Semikola, Verweise, Platzhalter, Satzlängen) |
| `Claude\\03_Skripte\\Umgebung_2026-09-25.txt` · `R_citation_2026-09-25.txt` | Umgebungen beider Rechnungen mit Prüfsummen · Zitierform von R aus `citation()` in R 4.3.3 |
| `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) | **Reihenfolge der Arbeit:** achtzehn Tasks in fünf Blöcken, Budgets als Vorgabe, Klickfragen, Startsätze |
| `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md` | Prompt dieses Tasks (Task 1 des Plans), nach Erledigung ins Archiv |
| `Claude\\04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md` | Textvorschlag 4.7 mit Kürzungsleiter (§ 2) und Kennungen je Zahl (§ 7). Grundlage für Task 6 des Plans, Textstufen `Textvorschlag_4.7_2026-09-25_A/_Empf/_Kurz.txt` |
| `Claude\\05_Protokolle\\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25` (.md, .docx, .pdf) | Erratum 1995 nicht beschaffbar, Register R14 |""",
    "§ 1.3 Zeilen der Auswertung")
ers("""| `Claude\\03_Skripte\\Auswertung_B0…B9_2026-09-12.py` + `.txt` | Erste Implementierung (Python), Gegenprobe der R-Rechnung |""",
    """| `Claude\\03_Skripte\\Auswertung_B0…B9_2026-09-12.py` + `.txt` | Erste Implementierung (Python, Rechnung 15.09.). Keine Zahlenquelle, die Gegenprobe der R-Rechnung ist `Gegenprobe_Python_2026-09-25.py` |""",
    "§ 1.3 B0 bis B9")
ers("""Weitere Ablage: `Ideen und Studien` = alle Fachliteratur-PDFs, flach. Die Darstellungspipeline `Auswertung\\*.ps1` mit `ausgabe\\` ist überholt (Umfangsdokument § 4). Objekte entstehen per R-Skript aus der Ergebnisdatei (Auswertungsverfahren 7.2, Maßnahme L19).""",
    """Weitere Ablage: `Ideen und Studien` = alle Fachliteratur-PDFs, flach. Die Darstellungspipeline `Auswertung\\*.ps1` ist seit dem 25.09. entfernt (L21). Objekte entstehen per R-Skript aus der Ergebnisdatei (Auswertungsverfahren 7.2) und liegen in `03_Skripte\\Objekte_2026-09-25` und `06_Abbildungen`.

**Nachtragsvermerke** (Maßnahme I19, jeweils mit der nächsten Revision des Dokuments, keine eigene Fassung): Auswertungsverfahren 7.3 — die Kennung steht nicht neben der Zahl im Manuskript, Rückverfolgbarkeit über die Zahlenliste des Endabgleichs · Umfangsdokument § 3.2 — Tab. 2 ohne die Kennwerte der Stichprobe, diese stehen in 4.2 · Berichtsraster Zeile 4.2.5 — Kennwerte im Text von 4.2, Kopfblock 3.11 — Budget 4.7 bleibt 550 nach Vorgabe, Zeile 4.7.13 — Anhang G ist der Ort der Prüfprotokolle · Kennzahlenblatt, Kopf — der Satz „Jede Zahl im Manuskript trägt eine Kennung“ wird beim nächsten Lauf des Erzeugers auf die Regel aus § 1.2 Nr. 3 umgestellt. Dasselbe gilt für „Tab. 2 oben (K-02)“ im Kopf des Blatts, die Kennwerte stehen in 4.2. Bis dahin gilt die Regel dieser Fassung · `Manuskriptstand_2026-09-25.py` — rechnet 4.7 noch mit dem Budget 720, beim nächsten Lauf auf 550 umstellen (Vorgabe).

**Überholte Teile anderer Dokumente** (G26i, Vermerk hier und im README, nicht in den Dokumenten selbst): `CONSORT_Auswertung_und_Umsetzung_2026-09-09` § 4 (Vorschlagsliste) und die Fallzahlangaben · die Ist-Spalten von `Manuskriptstand_und_Vollstaendigkeit_2026-09-13` (ersetzt durch `Manuskriptstand_2026-09-25`) · Bauplan § 1, Zählung der Schlusskapitel: gemeint sind vier Studien ohne Fazitkapitel (Lloyd, Hammami, Beato, Padrón-Cabo), nicht „vier weder noch“ (G27b, Korrektur mit der nächsten Bauplan-Revision).""",
    "§ 1.3 Weitere Ablage und Nachträge")
ers("""· Projektanweisungen vor Fassung 14. `01_Verfahren""",
    """· Projektanweisungen vor Fassung 15 · `Kennzahlen_2026-09-22` (ersetzt durch 2026-09-25) · `Uebergabe_Datensicherung_2026-09-24`, `Uebergabe_Blindrechnung_R_2026-09-24`, `Uebergabe_4.1_Studiendesign_2026-09-22`, `Textvorschlag_4.1_2026-09-23`, `Textvorschlag_4.2_2026-09-22` und `Befunde_Sofortblock_2026-09-13` (erledigt, Kopien in `_Archiv\\_ersetzt_2026-09-25_Uebergaben`, Originale über `Ordner_aufraeumen.ps1`) · `Projektanweisungen_Fassung14` (Sicherung der wirksamen Fassung bis zum Einsetzen von F15, dann Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14`) · `Analyseprotokoll_2026-09-15` als Zahlenquelle · `Auswertung_B0…B9` als Zahlenquelle · `CONSORT_Auswertung_und_Umsetzung_2026-09-09` § 4 · Ist-Spalten von `Manuskriptstand_und_Vollstaendigkeit_2026-09-13` · Rev. 1 des Plans der weiteren Schritte. `01_Verfahren""",
    "§ 1.3 Veraltet")
ers("""`Dashboard\\daten\\` enthält nach den Dateinamen Kopien der Personendaten und ist zu prüfen und zu löschen (Maßnahme L21).""",
    """`Dashboard\\daten\\` ist seit dem 25.09. gelöscht (L21 erledigt). `Uebergabe_4.4_Querverweise_2026-09-12.md` liegt nur als Projektkopie `claude/` vor, nicht im Ordner.""",
    "§ 1.3 Hinweise")

ers("""| DSHS-Richtlinien im Anhang · DSHS-KI-Richtlinien 26.03.2025 | Formale Vorgaben und KI-Deklaration |""",
    """| DSHS-Richtlinien im Anhang · DSHS-KI-Richtlinien 26.03.2025 | Formale Vorgaben und KI-Deklaration |
| `Claude\\README_Ordnerstruktur.md` · `Claude\\Ordner_aufraeumen.ps1` | Ordnerstruktur mit „Was wo gilt“ · Aufräumskript, verschiebt Nicht-mehr-Gebrauchtes nach `Bachelorarbeit\\Papierkorb` (Cowork kann nicht löschen) |
| `Claude\\01_Verfahren\\Beschaffungsliste_Literatur_2026-08-28` | Beschaffungsliste, Stand 28.08. Der laufende Stand steht in der Maßnahmenliste, Gruppe H |
| `Claude\\02_Befunde\\Datendurchsicht_Post_2026-09-10` · `Fragebogenauswertung_2026-09-12` · `Statistische_Verfahren_Literaturbefund_2026-09-11` · `Testprotokoll_Literaturabgleich_2026-09-12` | Befunde vor der Blindrechnung: Herleitung und Literatur, keine Zahlenquelle. Die Fragebogenauswertung trägt die Lokalisation der Schmerzmeldungen (Plan Task 11), der Testprotokoll-Abgleich die Testbedingungen der Vergleichsstudien (Tasks 2 und 3) |
| `Claude\\04_Uebergaben\\Uebergabe_4.3_Untersuchungsablauf_2026-09-12` · `Uebergabe_4.4_Leistungsdiagnostik_2026-09-12` · `Uebergabe_4.5.1_Heimtrainingsprogramm_2026-09-23` · `Uebergabe_4.6_Monitoring_2026-09-14` · `Textvorschlag_4.5.1_2026-09-23` | Eingänge der Textrevision Kapitel 4 (Plan Tasks 2 bis 5), der Textvorschlag 4.5.1 mit der Kürzungsleiter (G28h). Nach dem jeweiligen Task ins Archiv |
| `Claude\\05_Protokolle\\Kommentarprotokoll_Kapitel2_2026-09-07` · `Kommentarprotokoll_Kapitel2-2_2026-09-07` · `Rechercheprotokoll_Suchstrings_2026-09-02` · `A1_Titelscreening_2026-09-11` · `Pruefprotokoll_Gliederung_2026-09-23` | Kommentare zu Kapitel 2 (Tasks 7 bis 10), Suchprotokoll, Titelscreening, Prüfprotokoll der Gliederung v4 mit den Errata (§ 5.1) |
| `Claude\\03_Skripte`: `Steuerung_Rev*` · `Werkzeug_*` · `Master_*` · `Messen_Text_*` · `measure*` · `Kuerzungsleiter_*` · `Massnahmenliste_Bereinigung_*` · `Auswertungsplan_Register_*` · `Blindpruefung_Vermerk_*` · `Spezifikation_Nachtrag3_*` · `Objekte_Synthetik_*` · `Korpus_*` · `Projektanweisungen_*` · `S14_*_Python.png` | Sitzungs- und Werkzeugskripte: Fortschreibung der Steuerung, Einbau in den Master, Messungen, Registernachträge, Korpusmessungen, Erzeugung und Vergleich der Projektanweisungen, Diagramme der Python-Gegenprobe. Keine eigene Rolle, sie belegen die Einträge in Teil 0 |
| `Claude\\06_Abbildungen`: `Abb_*` · `Anhang_G` · `Kandidaten_Evidenztabelle` · `README_Abbildungen.md` | Objektgrafiken (Abb. 1, Abb. 2, Abb. H7), Q-Q- und Linearitätsdiagramme für Anhang G, Kandidaten für die Evidenztabelle, Legende des Ordners |""",
    "§ 1.3 Zuordnung nach Klick")

# § 1.4 -------------------------------------------------------------------------
ers("""| `05_Protokolle` | Kommentar- und Rechercheprotokolle |
""",
    """| `05_Protokolle` | Kommentar- und Rechercheprotokolle |
| `06_Abbildungen` | Objektgrafiken aus dem R-Skript (Abb. 1, Abb. 2, Abb. H7), `Anhang_G` (Q-Q- und Linearitätsdiagramme), `Kandidaten_Evidenztabelle`, `README_Abbildungen.md` |
""",
    "§ 1.4 06_Abbildungen")

# § 1.5 -------------------------------------------------------------------------
ers("""**Freigaben:** F0, 0.2, 0.3 und F1 hat der Verfasser am 24.09. selbst gegeben.""",
    """**Freigaben:** F0, 0.2, 0.3 und F1 hat der Verfasser am 24.09. selbst gegeben, F2 und F3 am 25.09.""",
    "§ 1.5 Freigaben")

# § 2 ---------------------------------------------------------------------------
ers("""Mit %PAH 30 von 31. Nenner je Zielgröße K-07.""",
    """Mit %PAH 30 von 31. Nenner je Zielgröße K-04 und K-06.""",
    "§ 2 Gesamt")
ers("""KG 12× zwei, VS-11 ohne Angabe.""",
    """KG 13× zwei.""",
    "§ 2 Familiarisierung")
ers("""Das Erratum (1995) wird nicht verwendet, ist aber vor Phase 4 zu prüfen (L12) |""",
    """Das Erratum (1995) wurde nicht eingesehen (Rechercheprotokoll 25.09., Register R14), die Koeffizienten stammen aus der Originalpublikation. 4.3 nennt das in einem Satz |""",
    "§ 2 Reifestatus")
ers("""Für die Rechnung ein eingefrorener Datenstand aus Phase 1 (nur Analysevariablen als CSV, Datenwörterbuch, SHA-256). Berichtete Rechnung in R durch eine blinde zweite Instanz nach der Spezifikation, Python-Kette (Code 12.09.) als Gegenprobe, Abgleich je Kennung (§ 11.10) |""",
    """Für die Rechnung der eingefrorene Datenstand `Statistik\\Datenstand_2026-09-24` aus Phase 1 (nur Analysevariablen als CSV, Datenwörterbuch, SHA-256). Berichtete Rechnung erfolgt (`03_Skripte\\Abgabe_R_2026-09-25`, R 4.3.3, blinde zweite Instanz nach der Spezifikation), Python-Gegenprobe, Abgleich je Kennung bestanden (§ 11.10) |""",
    "§ 2 Datenhaltung")

# § 3 ---------------------------------------------------------------------------
ers("""# 3. DATENSTAND (Workbook-Stand 15.09.2026, 22:21 MESZ)""",
    """# 3. DATENSTAND (eingefrorener Datenstand vom 24.09.2026)""",
    "§ 3 Überschrift")
ers("""**Die Erhebung ist abgeschlossen. Die erste Rechnung (Python) lief am 15.09. Die berichtete Rechnung steht aus:** Phase 1 Datensicherung → Blindordner → Blindrechnung in R → Abgleich (Auswertungsverfahren, Maßnahmen L5, L11, L7, L8).""",
    """**Die Erhebung ist abgeschlossen. Die Auswertung ist abgeschlossen:** Phasen 0 bis 7 des Auswertungsverfahrens (Datensicherung 24.09., Spezifikation mit Nachtrag 1 bis 3, Blindrechnung in R 4.3.3, Abgleich je Kennung, Durchsicht, Handprobe, Plausibilität, F2, Kennzahlenblatt 25.09. Rev. 2, Objekte, Endabgleich Fassung 3, F3 am 25.09.). Offen ist Phase 8 (Plan Task 16).""",
    "§ 3 Kopf")
ers("""Fallzahlen, Kennwerte, Messgüte- und Ausgangswerte stehen im Kennzahlenblatt `Claude\\02_Befunde\\Kennzahlen_2026-09-22.md` unter den Kennungen K-01 bis K-08, die Ergebnisse der ersten Rechnung im `Analyseprotokoll_2026-09-15.md`. Wer eine Zahl braucht, liest sie dort und nennt im Manuskript ihre Kennung. Nach dem Abgleich gilt allein das neue Kennzahlenblatt.""",
    """Fallzahlen, Kennwerte, Messgüte-, Ausgangs- und Ergebniswerte stehen im Kennzahlenblatt `Claude\\02_Befunde\\Kennzahlen_2026-09-25.md` (Rev. 2) unter den Kennungen K-01 bis K-12. Das gilt auch für § 3.1 und § 3.2. Wer eine Zahl braucht, liest sie dort. Die Kennung steht im Begleitteil des Textvorschlags, nicht im Manuskript (§ 1.2).""",
    "§ 3 keine Zahlen")
ers("""**Bezugsmengen-Regel (Verfasser 22.09., Kennzahlenblatt Rev. 3 und 4):**""",
    """**Bezugsmengen-Regel (Verfasser 22.09., unverändert im Kennzahlenblatt 25.09.):**""",
    "§ 3 Bezugsmengen-Regel Quelle")
ers("""K-02 (alle Angetretenen) und K-02b (Analysepopulation) werden nie in einem Satz gemischt.""",
    """K-02 gilt nur für die Analysepopulation. Ausgangswerte aller Eingangsgetesteten stehen in Tab. H3 und werden nie mit K-02 in einem Satz gemischt.""",
    "§ 3 K-02")
ers("""**Offene Workbook-Punkte** (Analyseprotokoll § 6) erledigt der Task „Datensicherung“ mit Belegprüfung und Blatt `00_Aenderungen` (`04_Uebergaben\\Uebergabe_Datensicherung_2026-09-24.md`): Status der VS-Spieler · Ausfallgrund VS-07 und VS-16 · Bemerkung VS-11 · Familiarisierung VS-11 · Begründung VS-18 · Testdatum post Verein C · Tippfehler im Bemerkungsvokabular · zwei ungültige Zeilen ohne Bemerkung (VS-02, VS-06).""",
    """**Workbook-Punkte:** Die offenen Punkte aus dem Analyseprotokoll § 6 sind mit der Datensicherung vom 24.09. erledigt (Belegprotokoll, Blatt `00_Aenderungen`).""",
    "§ 3 Workbook-Punkte")
ers("""**Weiterhin blockiert:** Flowchart-Felder vor der Zuteilung (angefragte Vereine, SC West, VS-09, VS-12 bis VS-15, Einwilligung VS-01 und VS-02) · Vereins-Chronologie für 4.1.""",
    """**Weiterhin blockiert:** nur noch die gemeldeten Spieler je Verein (B5 Rest), falls Abb. 1 sie zeigen soll. Die Clusterebene steht in K-01.24.""",
    "§ 3 blockiert")
ers("""eine Wiederholung war aus Zeitgründen nicht möglich. Zahlen: K-04.""",
    """eine Wiederholung war aus Zeitgründen nicht möglich. Zahlen: K-11.""",
    "§ 3.1 Kennung")
ers("""Bei den Sprints dominiert der technische Ausfall, und er traf die KG vier- bis achtfach stärker.""",
    """Bei den Sprints dominiert der technische Ausfall, und er traf die KG stärker (K-11.4).""",
    "§ 3.1 ohne Zahl")
ers("""111 Meldungen. Nach zwei CASE-Korrekturen (59 und 70 → BW-06, 140, 158, 165, 190 und 206 → BW-04) 92 ganz, 6 teilweise, 13 gar nicht · 12 Schmerzmeldungen (9 Spieler, 2 Abbrüche) · Umsetzungsrate 92 von 216 = 42,6 % · Median 6,0 vollständige Einheiten je zugeteiltem Spieler (erste Rechnung, Fragebogenauswertung 12.09.).""",
    """Zahlen: K-10 (Meldungen je Status, Umsetzungsrate, Median, Untergrenzen, unerwünschte Ereignisse, CR-10, sRPE-Load). Zwei CASE-Korrekturen: 59 und 70 → BW-06, 140, 158, 165, 190 und 206 → BW-04.""",
    "§ 3.2 ohne Zahlen")

# § 5.1 -------------------------------------------------------------------------
ers("""**Reihenfolgetreue:** Sprint → Richtungswechsel → Sprung in Kapitel 3, 5 und 6 identisch.""",
    """**Reihenfolgetreue:** Sprint → Richtungswechsel → Sprung in Kapitel 3, 5 und 6 identisch.

**Errata zur Gliederung v4** (Prüfprotokoll `05_Protokolle\\Pruefprotokoll_Gliederung_2026-09-23` § 2, übernommen mit F15, G27a): E1 — 4.3 misst 590 Wörter ohne und 609 mit dem Platzhalterabsatz „Abb. 1 Zeitstrahl“, für das Budget gilt 590, der Platzhalter entfällt (M10) · E2 — M21 zählt 21 Abschnittsverweise (5.1: 6, 6.1: 8, 6.2: 7), die Prüfliste zu G19 enthält 4.5.2 Abs. 5 · E3 — Fassung 13 § 13 führte nur „Kapitelname 3“, nicht „Beibehaltung von 6.1–6.3“ (in F14 berücksichtigt) · E4 — CONSORT Item 25 (Förderung) ist übertragbar, die Bilanz lautet 28 übertragbar, 4 analog, 5 gegenstandslos · E5 — das unverbindliche Muster-Inhaltsverzeichnis des SMK-Leitfadens (Abb. 1, S. 18) mit „5.1 Deskriptive Ergebnisse · 5.2 Analytische Ergebnisse“ ist Gegenbefund zu den Inhaltsnamen von v4. Die v4-Namen bleiben (Klickantwort 23.09.).""",
    "§ 5.1 Errata")

# § 5.2 -------------------------------------------------------------------------
stand = (f"**Stand am Master (Messung 25.09., `03_Skripte\\Manuskriptstand_2026-09-25.txt`):** "
         f"4.1 {de(ist['4.1'])} · 4.2 {de(ist['4.2'])} · 4.3 {de(ist['4.3'])} · 4.4 mit 4.4.1 bis 4.4.3 {de(ist['4.4'])} · "
         f"4.5.1 {de(ist['4.5.1'])} · 4.5.2 {de(ist['4.5.2'])} · 4.6 {de(ist['4.6'])} · 4.7 {de(ist['4.7'])} · "
         f"Kapitel 4 (4.1 bis 4.6) {de(kap4_46)}, mit 4.7 {de(kap4_47)} · Kapitel 2 (2.1 bis 2.4) {de(kap2)} · "
         f"Absatztext Kapitel 1 bis 7 {de(gesamt)} · Kürzungsauftrag {de(kuerz)}. "
         f"4.7 steht seit dem 25.09. mit {de(ist['4.7'])} Wörtern im Master (Klickfreigabe der Stufe „Empfehlung“). "
         f"Die Vorgabe gilt (Verfasser 25.09., abends): keine Anhebung, keine Gegenfinanzierung, Rückführung auf {de(vorgabe['4.7'])} in Task 6 des Plans. "
         f"4.5.1: Ziel {de(vorgabe['4.5.1'])} nach Vorgabe. ")
alt_ub = re.search(r"Stand am Master nach dem 4\.5\.1-Task: .*?\(G16d\)\. ", text)
assert alt_ub and text.count(alt_ub.group(0)) == 1, "Unterbudget-Satz nicht eindeutig"
ers(alt_ub.group(0), stand, "§ 5.2 Stand am Master")
ers("""**Unterbudgets (Gliederung v4, Klick 5, Arbeitsfestlegung 23.09.):**""",
    """**Unterbudgets (Gliederung v4, Klick 5, Arbeitsfestlegung 23.09., Vorgabe seit 25.09.):**""",
    "§ 5.2 Unterbudgets Kopf")
alt_wdb = re.search(r"Der geschriebene Bestand vom 13\.09\. beträgt .*?geschrieben wird\.", text)
assert alt_wdb and text.count(alt_wdb.group(0)) == 1
ers(alt_wdb.group(0),
    (f"Der geschriebene Bestand beträgt am 25.09. **{de(gesamt)} Wörter** Absatztext (Kapitel 2 mit 2.1 bis 2.4 {de(kap2)}, "
     f"Kapitel 4 mit 4.1 bis 4.7 {de(kap4_47)}, Messung `03_Skripte\\Manuskriptstand_2026-09-25.txt`). "
     f"Das Budget sieht für dieselben Abschnitte **{de(budget_kap2 + budget_kap4)}** vor ({de(budget_kap2)} für 2.1 bis 2.4, {de(budget_kap4)} für 4.1 bis 4.7). "
     f"Zu kürzen sind also **{de(kuerz)} Wörter, {anteil} Prozent des Bestands**, bevor eine Zeile Kapitel 5 oder 6 geschrieben wird. "
     f"Die neun leeren Abschnitte ({leer_namen}) haben zusammen {de(budget_leer)} Wörter Budget."),
    "§ 5.2 Was das bedeutet")
alt_k4 = re.search(r"- \*\*Kapitel 4: rund −1\.920\*\* \(4\.1–4\.6 von 3\.918 auf 2\.000, dazu 4\.7 mit 550\)\.", text)
assert alt_k4, "Kapitel-4-Zeile nicht gefunden"
ers(alt_k4.group(0),
    f"- **Kapitel 4: −{de(kuerz4)}** (4.1 bis 4.7 von {de(kap4_47)} auf {de(budget_kap4)}, darin 4.7 von {de(ist['4.7'])} auf {de(vorgabe['4.7'])}).",
    "§ 5.2 Kapitel 4")
alt_k2 = "- **Kapitel 2: −1.970.**"
assert f"−{de(kuerz2)}" == "−1.970", "Kürzung Kapitel 2 weicht von der Vorgabe im Text ab"
ers(alt_k2, f"- **Kapitel 2: −{de(kuerz2)}** (2.1 bis 2.4 von {de(kap2)} auf {de(budget_kap2)}).", "§ 5.2 Kapitel 2")
ers("""Reihenfolge: erst der Sofortblock aus dem Manuskriptstand (A1, B5–B8, C14–C18, rund +150 Wörter, weil dort Berichtsstandards verletzt sind), dann die Kürzung, dann Kapitel 5.""",
    """Reihenfolge nach dem Plan der weiteren Schritte (Rev. 2): Steuerdokumente → Textrevision Kapitel 4 (4.3, 4.4, 4.5.2 mit 4.6, 4.1 mit 4.5.1, 4.7 auf 550) → Kürzung Kapitel 2 (2.4, 2.3, 2.1, 2.2) → Kapitel 5, 6, 7 mit Zusammenfassung, dann 1, 2.5, 3 → Literaturverzeichnis, Phase 8, Anhänge A bis F, Endredaktion.""",
    "§ 5.2 Reihenfolge")

# § 5.3 -------------------------------------------------------------------------
ers("""| Tab. 2 Stichprobe und Ausgangswerte | 5.1 | Alter, Körperhöhe, Körpermasse, %PAH der Analysepopulation, dann sieben Zielgrößen (Analyseset je Zielgröße).""",
    """| Tab. 2 Stichprobe und Ausgangswerte | 5.1 | sieben Zielgrößen (Analyseset je Zielgröße). Die Kennwerte Alter, Körperhöhe, Körpermasse und %PAH der Analysepopulation stehen in 4.2, nicht in Tab. 2 (Verfasser 25.09.).""",
    "§ 5.3 Tab. 2")
ers("""**Objektzuordnung:** Messgüte (Tab. 1, ohne MDC) → 4.4""",
    """**Objektzuordnung:** Kennwerte der Stichprobe (Alter, Körperhöhe, Körpermasse, %PAH der Analysepopulation) → 4.2 im Text · Messgüte (Tab. 1, ohne MDC) → 4.4""",
    "§ 5.3 Objektzuordnung")

# § 6.5 -------------------------------------------------------------------------
ers("""· Erratum Khamis & Roche (1995), doi 10.1542/peds.95.3.457, vor Phase 4 (L12)""",
    """· Erratum Khamis & Roche (1995), doi 10.1542/peds.95.3.457, nicht beschaffbar, nicht eingesehen (Rechercheprotokoll 25.09., R14)""",
    "§ 6.5 Erratum")

# § 8 ---------------------------------------------------------------------------
ers("""**Noch einzupflegen:** Havanecz et al. (2026)""",
    """**Noch einzupflegen:** R Core Team (2024) aus `citation()` (`03_Skripte\\R_citation_2026-09-25.txt`) · Hedges (1981) nur nach Beschaffung (H9) · Havanecz et al. (2026)""",
    "§ 8 einpflegen")

# § 11.2a -----------------------------------------------------------------------
a0 = text.index("## 11.2a Ergebnislage der ersten Rechnung")
a1 = text.index("## 11.2b Schlusslogik")
assert text.count("## 11.2a ") == 1 and a0 < a1
alt_112a = text[a0:a1]
ers(alt_112a,
    """## 11.2a Ergebnislage nach der Blindrechnung (25.09.2026)

Maßgeblich ist das Kennzahlenblatt 25.09. (K-06 bis K-09). Der Fall je konfirmatorischer Zielgröße nach der Schlusslogik steht in K-06. Der tragende Befund für Kapitel 5 und 6 ist der Abstand zwischen unadjustierter und adjustierter Differenz (Tab. 3, Abb. 2), die Verdünnungslogik (§ 11.7) trägt die Diskussion. Der Voraussetzungsbefund je Zielgröße steht in K-07 und wird nach Regel O7 und R2 berichtet, die Robustheitsaussage entfällt. Dieses Dokument führt keine Ergebniszahlen.

""",
    "§ 11.2a")

# § 11.3 ------------------------------------------------------------------------
ers("""Werte: K-05, nach dem Abgleich aus der Blindrechnung.""",
    """Werte: K-05.""",
    "§ 11.3 Werte")

# § 11.4 ------------------------------------------------------------------------
alt_sw = re.search(r"Software: R ⟨Version⟩.*?\(Auswertungsverfahren 8\.1\)\.", text)
assert alt_sw and text.count(alt_sw.group(0)) == 1
ers(alt_sw.group(0),
    """Software: R 4.3.3 ohne Zusatzpakete (R Core Team, 2024), berichtete Rechnung der blinden zweiten Instanz nach der Spezifikation, Skripte in Anhang G. Python-Kette als Gegenprobe, Abgleich bestanden (Abgleichprotokoll 25.09.).""",
    "§ 11.4 Software")

# § 11.10 -----------------------------------------------------------------------
ers("""**Gegenprobe:** die Python-Kette B0 bis B9 und F1 (Code 12.09., Rechnung 15.09.). Abgleich je Kennung mit den Toleranzen aus Spezifikation G.3 (Phase 6).""",
    """**Gegenprobe:** `03_Skripte\\Gegenprobe_Python_2026-09-25.py` (Fassung 2) mit `Ergebnisse_Python_2026-09-25.csv`. Abgleich je Kennung mit den Toleranzen aus Spezifikation G.3 (Phase 6), bestanden am 25.09.""",
    "§ 11.10 Gegenprobe")
ers("""**Danach:** Kennzahlenblatt per Skript (7.1), Objekte per R-Skript aus der Ergebnisdatei (7.2, vorbereitet mit synthetischen Daten, L19), Endabgleich des Manuskripts (7.3).""",
    """**Erledigt:** Kennzahlenblatt per Skript (7.1), Objekte per R-Skript aus der Ergebnisdatei (7.2), Endabgleich des Manuskripts (7.3, Fassung 3).""",
    "§ 11.10 Danach")
ers("""**Reihenfolge der nächsten Schritte:** Datensicherung im Projekt (L5, `04_Uebergaben\\Uebergabe_Datensicherung_2026-09-24.md`) → Blindordner (L11) → Blindrechnung in einem neuen Chat außerhalb des Projekts (L7, `04_Uebergaben\\Uebergabe_Blindrechnung_R_2026-09-24.md`) → Abgleich im Projekt (L8).""",
    """**Stand 25.09.:** Phasen 1 bis 7.3 abgeschlossen (L5, L11, L7, L8 erledigt). Offen: Phase 8 (L9, Plan Task 16).""",
    "§ 11.10 Stand")
ers("""`Auswertung\\ancova_ergebnisse.csv` gehört als Ausgabe der Python-Gegenprobe nach `03_Skripte` (L21).""",
    """`Auswertung\\ancova_ergebnisse.csv` liegt seit dem 25.09. als `03_Skripte\\Auswertung_B7_ANCOVA_2026-09-12_ancova_ergebnisse.csv` vor (L21).""",
    "§ 11.10 ancova")

# § 12 --------------------------------------------------------------------------
ers("""(Zahlen aus der Blindrechnung, Standardweg)""", """(K-09)""", "§ 12 G1")

# § 13 --------------------------------------------------------------------------
ers("""Der Load wird auf der Solldauer berechnet, die Dauer ist nicht individuell erfasst.
""",
    """Der Load wird auf der Solldauer berechnet, die Dauer ist nicht individuell erfasst.
10. **Kennungen:** nicht im Manuskript, Rückverfolgbarkeit über die Zahlenliste des Endabgleichs (25.09.).
11. **Kennwerte der Stichprobe:** in 4.2, Tab. 2 ohne diese Zeilen (25.09.).
12. **Vorgabe:** Budgets nach § 5.2 verbindlich, keine Anhebung, keine Gegenfinanzierung, kein Textvorschlag über dem Budget, 4.7 zurück auf 550 (25.09., abends).
13. **Reihenfolge:** Kürzung der vorhandenen Kapitel vor neuen Kapiteln, Anhänge ganz zum Schluss (25.09., abends).
14. **Maßnahmenliste:** Bereinigung freigegeben und ausgeführt, Rev. 97 (25.09., abends).
""",
    "§ 13 Nr. 10 bis 14")
ers("""· Kapitelname 3 und Kapitel-6-Struktur (Gliederung v4).""",
    """· Kapitelname 3 und Kapitel-6-Struktur (Gliederung v4) · Handprobe (bestanden 25.09.) · F2 und F3 (25.09.) · Erratum Khamis & Roche nicht beschaffbar (R14, 25.09.).""",
    "§ 13 Erledigt")

# § 14 --------------------------------------------------------------------------
ers("""Die Leitlinie beruft sich auf die DFG-Stellungnahme 2023 und die EU-KI-Verordnung Art. 50.""",
    """Die Leitlinie beruft sich auf die DFG-Stellungnahme 2023 und die EU-KI-Verordnung Art. 50. Textvorschläge und Skripte entstehen in Claude, die Sitzungen sind über die Rev.-Nummern der Sitzungsnotizen protokolliert (Grundlage des KI-Nutzungsprotokolls, Plan Task 16).""",
    "§ 14 KI-Nutzung")

# § 15 --------------------------------------------------------------------------
ers("""- R Core Team (⟨Jahr⟩). *R: A language and environment for statistical computing* (Version ⟨Version⟩). R Foundation for Statistical Computing. — Zitierform aus `citation()` der Blindrechnung übernehmen.""",
    """- R Core Team (2024). *R: A Language and Environment for Statistical Computing*. R Foundation for Statistical Computing, Vienna, Austria. https://www.R-project.org/ — Wortlaut von `citation()` in R 4.3.3 (2024-02-29), gleiche Version wie die Blindrechnung (`03_Skripte\\R_citation_2026-09-25.txt`). 4.7 nennt die Version 4.3.3, die APA-Form entsteht im Literaturverzeichnis (Plan Task 15).""",
    "§ 15 R Core Team")


# Folgekorrekturen nach der unabhängigen Zweitprüfung (Subagent, 25.09.) ---------------
ers("""Freigabe F1, Nachtrag 1 (Teil F.6) und Nachtrag 2 (Teil F.7), 1.535 Kennungen.""",
    """Freigabe F1, Nachtrag 1 (Teil F.6), Nachtrag 2 (Teil F.7) und Nachtrag 3 (Teil F.8, 25.09., R13), 1.535 Kennungen.""",
    "§ 1.3 Spezifikation Nachtrag 3")
ers("""(F1, Nachtrag 1 und 2, 1.535 Kennungen, acht CSV-Anlagen)""",
    """(F1, Nachtrag 1 bis 3, 1.535 Kennungen, acht CSV-Anlagen)""",
    "§ 11.10 Nachtrag 3")
ers("""Kennzahlen_2026-09-15 (ersetzt durch 2026-09-22)""", """Kennzahlen_2026-09-15 (ersetzt)""", "§ 1.3 Kennzahlen 15.09.")
ers("""(K-01.14, K-01.16: Prä, Post und %PAH, Spezifikation Menge ANA)""",
    """(K-01.14, K-01.16, Menge ANA der Spezifikation: im ITT-Set mindestens einer Zielgröße)""",
    "§ 3 Analysepopulation")
ers("""Die Zuordnungstabelle Listenlabel → Analysecode entsteht in Phase 1 (Schritt 1.2).""",
    """Die Zuordnungstabelle Listenlabel → Analysecode entstand in Phase 1 (Schritt 1.2, Belegprotokoll).""",
    "§ 3.2 Zuordnungstabelle")
ers("""MDES und Power liefert die Blindrechnung.""", """MDES und Power: K-09.""", "§ 11.1 MDES")
ers("""In der ersten Rechnung änderte keine Variante das Bild (Analyseprotokoll § 4).""", """Ergebnis je Variante: K-08.""", "§ 11.5 Varianten")
ers("""Schwellenlandschaft offenlegen (≥ 4: 12""", """Schwellenlandschaft nach K-10.15 offenlegen (≥ 4: 12""", "§ 11.7 Schwellen")
ers("""**Verdünnungslogik für 6.2:** Bei 42,6 % vollständig absolvierter Einheiten ist""",
    """**Verdünnungslogik für 6.2:** Bei der Umsetzungsrate nach K-10.5 (weniger als die Hälfte der Einheiten vollständig absolviert) ist""",
    "§ 11.7 Verdünnung")
ers("""**Erste Rechnung (15.09.):** Die Sensitivitätsanalyse mit dem Mittelwert weicht nicht ab. Der Bestwert bleibt Hauptmaß, der Bias bleibt Limitation. Die Blindrechnung rechnet beide erneut.""",
    """**Mittelwert-Sensitivität:** Ergebnis in K-08. Der Bestwert bleibt Hauptmaß, der Bias bleibt Limitation.""",
    "§ 11.8 Mittelwert")
ers("""In der ersten Rechnung betraf das die Normalverteilung der Residuen beim 30-m-Sprint (§ 11.2a).""",
    """Welche Prüfung verworfen wurde, steht in K-07.""",
    "§ 11.9 Verweis")
ers("""**G3 Umsetzung und Verdünnung.** 42,6 % vollständig absolvierte Einheiten,""",
    """**G3 Umsetzung und Verdünnung.** Umsetzungsrate nach K-10.5,""",
    "§ 12 G3")

# ---------------------------------------------------------------- anwenden
protokoll = []
for alt, neu, stelle in ersetzungen:
    n = text.count(alt)
    if n != 1:
        sys.exit(f"ABBRUCH: {stelle}: Fundstelle {n}-mal statt genau einmal")
    text = text.replace(alt, neu)
    protokoll.append(stelle)

if chr(59) in "".join(n for _, n, _ in ersetzungen) + kopf_neu:
    sys.exit("ABBRUCH: Semikolon im neuen Text")

open(ziel, "w", encoding="utf-8", newline="\n").write(text)
sha15 = hashlib.sha256(text.encode("utf-8")).hexdigest()
print(f"Fassung 14 gelesen: {quelle} SHA-256 {sha14}")
print(f"Fassung 15 geschrieben: {ziel} SHA-256 {sha15}, {len(text.encode('utf-8'))} Byte")
print(f"Kopf ersetzt, dazu {len(protokoll)} Ersetzungen, je genau einmal:")
for s in protokoll:
    print("  " + s)
print(f"Messwerte: Kapitel 2 {kap2}, Kapitel 4 bis 4.6 {kap4_46}, mit 4.7 {kap4_47}, gesamt {gesamt}, Kürzung {kuerz} ({anteil} %), leere Abschnitte {leer_namen} mit {budget_leer}")

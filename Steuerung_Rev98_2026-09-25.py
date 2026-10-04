# -*- coding: utf-8 -*-
"""
Steuerung Rev. 98 (Task 1 „Steuerdokumente“, 25.09.2026): Teil 0 der Sitzungsnotizen und Maßnahmenliste fortschreiben.
Jede Textstelle genau einmal, sonst Abbruch. Offene Punkte werden nach dem Schreiben gezählt, nicht geschätzt.
Das Skript enthält kein Semikolon.

Aufruf: python3 Steuerung_Rev98_2026-09-25.py <Claude-Ordner>
"""
import hashlib
import os
import re
import sys

wurzel = sys.argv[1]
pn = os.path.join(wurzel, "00_Steuerung", "Cowork_Sitzungsnotizen.md")
pm = os.path.join(wurzel, "00_Steuerung", "Massnahmenliste_Datenverarbeitung.md")
f15 = os.path.join(wurzel, "00_Steuerung", "Projektanweisungen_Fassung15.md")
sha15 = hashlib.sha256(open(f15, "rb").read()).hexdigest()
groesse15 = os.path.getsize(f15)
protokoll = []


def ersetze(text, alt, neu, stelle):
    n = text.count(alt)
    if n != 1:
        sys.exit(f"ABBRUCH: {stelle}: Fundstelle {n}-mal statt genau einmal")
    protokoll.append(stelle)
    return text.replace(alt, neu)


# ---------------------------------------------------------------- Maßnahmenliste
m = open(pm, encoding="utf-8").read()
vorher_h = len(re.findall(r"(?m)^- \[ \]", m))
vorher_t = len(re.findall(r"(?m)^[ \t]+- \[ \]", m))
m = ersetze(m, "- [x] **A8 · ⭐ Projektanweisungen Fassung 14 in die claude.ai-Projekteinstellungen einsetzen** — ",
            "- [ ] **A8 · ⭐ Projektanweisungen Fassung 15 in die claude.ai-Projekteinstellungen einsetzen** — **Rev. 98 (25.09., abends): Fassung 15 per Klick freigegeben. Offen beim Verfasser: den Text aus `00_Steuerung\\Projektanweisungen_Fassung15.md` (oder der Projektkopie) vollständig in die Projekteinstellungen kopieren, danach `Ordner_aufraeumen.ps1` mit `-WhatIf` und dann echt laufen lassen. Es nimmt Fassung 14 und sechs erledigte Übergaben in den Papierkorb, die Kopien liegen in `_Archiv\\_ersetzt_2026-09-25_Fassung14` und `_Archiv\\_ersetzt_2026-09-25_Uebergaben`.** Zu Fassung 14: ",
            "A8")
m = ersetze(m, "- [ ] **I19 · Folgeänderungen", "- [x] **I19 · Folgeänderungen", "I19 Kästchen")
m = ersetze(m, "(d) Berichtsraster Kopfblock 3.11 Budget und Zeile 4.7.13 mit Anhang G als Ort der Prüfprotokolle)*",
            "(d) Berichtsraster Kopfblock 3.11 Budget und Zeile 4.7.13 mit Anhang G als Ort der Prüfprotokolle)* ✅ erledigt 25.09. (Rev. 98, Task 1): (a) in Fassung 15 § 1.2 Nr. 3, (c) gegenstandslos, weil die Vorgabe gilt (Budget 4.7 bleibt 550, F15 § 5.2). (b), (d), Auswertungsverfahren 7.3 und der Kopf des Kennzahlenblatts stehen als Nachtragsvermerk in F15 § 1.3 und werden mit der nächsten Revision des jeweiligen Dokuments umgesetzt",
            "I19 Vermerk")
for kenn, vermerk in [
    ("G26i", "✅ erledigt 25.09. (Rev. 98): Vermerk in F15 § 1.3 und im README („Überholte Teile anderer Dokumente“), nicht in den Dokumenten selbst"),
    ("G26j", "✅ erledigt 25.09. (Rev. 98): README „Was wo gilt“ als Tabelle der fünf Ebenen-Dokumente mit Frage und Änderungsrhythmus"),
    ("G27a", "✅ erledigt 25.09. (Rev. 98): E1 bis E5 in F15 § 5.1, Kurzform im Kopf"),
    ("G27b", "✅ erledigt 25.09. (Rev. 98): Vermerk in F15 § 1.3 und im README, Korrektur im Bauplan selbst mit dessen nächster Revision"),
    ("G25f", "✅ erledigt 25.09. (Rev. 98): Datei liegt nicht mehr in `Schreiben\\` (Papierkorb-Lauf Rev. 93)"),
]:
    zeile = re.search(r"(?m)^(\s+- )\[ \] \*\*" + kenn + r" ·.*$", m)
    assert zeile, kenn
    alt = zeile.group(0)
    neu = alt.replace("[ ] **" + kenn, "[x] **" + kenn, 1) + " " + vermerk
    m = ersetze(m, alt, neu, kenn)
zeile = re.search(r"(?m)^[ \t]+- \[ \] \*\*G17g ·.*$", m).group(0)
m = ersetze(m, zeile, zeile + " *(Rev. 98: Dateiteil erledigt, die Datei liegt nicht mehr in `Schreiben\\` (Papierkorb-Lauf Rev. 93). Offen bleibt das Tab.-2-Feld beim Anlegen von 5.1, Task 11)*", "G17g")
zeile = re.search(r"(?m)^- \[ \] \*\*G30 ·.*$", m).group(0)
m = ersetze(m, zeile, zeile + " *(Rev. 98: Task 1 erledigt, Fassung 15 freigegeben. Nächster Task: Task 2 Textrevision 4.3)*", "G30")
m = ersetze(m, "| 1 Steuerdokumente (`Uebergabe_Steuerdokumente_2026-09-25.md`) | I19 · G26i · G26j · G27a · G27b · G25f, G17g, G27f (Verfasserschritte) |",
            "| 1 Steuerdokumente (erledigt 25.09., Rev. 98) | A8 und G27f (Verfasserschritte) |",
            "Zuordnung Task 1")
nachher_h = len(re.findall(r"(?m)^- \[ \]", m))
nachher_t = len(re.findall(r"(?m)^[ \t]+- \[ \]", m))
m = ersetze(m, "| **Summe** | **33 Hauptpunkte und 40 Teilpunkte offen** (gemessen 25.09., Rev. 97,",
            f"| **Summe** | **{nachher_h} Hauptpunkte und {nachher_t} Teilpunkte offen** (gemessen 25.09., Rev. 98, nach Task 1: I19, G25f, G26i, G26j, G27a, G27b geschlossen, A8 wieder offen. Zuvor: gemessen 25.09., Rev. 97,",
            "Summe")
kopf = re.search(r"(?m)^\*\*Stand 25\.09\.2026, 21:40 MESZ \(Rev\. 97 — ", m).group(0)
m = ersetze(m, kopf,
            f"**Stand 25.09.2026, 21:50 MESZ (Rev. 98 — Task 1 Steuerdokumente: Projektanweisungen Fassung 15 per Skript, Vergleich bestanden, per Klick freigegeben, A8 wieder offen bis zum Einsetzen. README „Was wo gilt“, Archivkopien, Aufräumskript. I19, G25f, G26i, G26j, G27a, G27b erledigt, offen {nachher_h} und {nachher_t}). Zuvor 25.09.2026, 21:40 MESZ (Rev. 97 — ",
            "Kopf Maßnahmenliste")
open(pm, "w", encoding="utf-8", newline="\n").write(m)

# ---------------------------------------------------------------- Sitzungsnotizen Teil 0
n = open(pn, encoding="utf-8").read()
n = ersetze(n, "**Stand: (Rev. 97 — siehe Block oben.) Zuvor: ", "**Stand: (Rev. 98 — siehe Block oben.) Zuvor: (Rev. 97 — siehe Block oben.) Zuvor: ", "Stand-Zeile")
block = f"""### ⭐⭐ NEU (Rev. 98, 25.09.2026, 21:50 MESZ): Task 1 „Steuerdokumente“ — Projektanweisungen Fassung 15 per Skript aus Fassung 14, Vergleich mit vier Prüfungen bestanden, Zweitprüfung eingearbeitet, README „Was wo gilt“, Archivkopien, **Fassung 15 per Klick freigegeben** (A8: Einsetzen beim Verfasser)

**Auftrag (Verfasser, 25.09., Startsatz der Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md`):** Schritte 1 bis 6 in der festgelegten Reihenfolge, kein Manuskripttext, Rücksprache nur per Klick.

**(1) Gelesen und geprüft:** Teil 0 Rev. 95 bis 97 · Plan Rev. 2 (§ 0, § 2.3, § 3, § 4 bis § 7) · Fassung 14 vollständig · Maßnahmenliste (I19, G26i, G26j, G27a, G27b, G30, Zuordnungstabelle) · Prüfprotokoll Gliederung E1 bis E5 · `Manuskriptstand_2026-09-25` · Kennzahlenblatt 25.09. (Kopf, K-01.13, K-02, K-10, K-11) · `Umgebung_2026-09-25.txt` · Ordnerliste `Claude\\` (403 Dateien ohne `_Archiv`). **4.7 ist nicht geprüft:** Der Master ist seit dem Einbau von 4.7 unverändert (55.198 Byte, Zeitstempel des Commits aus Rev. 95). Schritt 1.8 (Diff) entfällt, die Prüfung durch den Verfasser (Plan § 2) bleibt offen und muss vor Task 6 liegen.

**(2) Fassung 15** `00_Steuerung\\Projektanweisungen_Fassung15.md` ({groesse15} Byte, SHA-256 {sha15[:12]}…), Erzeuger `03_Skripte\\Projektanweisungen_Fassung15_2026-09-25.py` mit `.txt`: Kopf neu plus 63 Ersetzungen, jede genau einmal, Wortzahlen aus `Manuskriptstand_2026-09-25.csv`, keine Zahl von Hand. Umgesetzt nach Übergabe § 2: Kopf mit sechs Punkten und „Korrekturen gegenüber Fassung 14“ · § 1.2 (Verfahren seit 22.09., Nr. 3 ohne Kennung im Manuskript, Nr. 6 R1 bis R14, neue Nr. 9 Plan, Zahlenregel) · § 1.3 (Kennzahlen 25.09., Phase-6- und 7-Dokumente, Plan, Übergabe, Textvorschlag 4.7, Rechercheprotokoll Erratum, Nachtragsvermerke I19, überholte Teile G26i und G27b, Veraltet ergänzt) · § 1.4 `06_Abbildungen` · § 2 (Reifestatus, Datenhaltung, KG 13× zwei nach K-01.13) · § 3 ohne Ergebniszahlen, § 3.2 Zahlen nach K-10 · § 5.1 Errata E1 bis E5 · § 5.2 Tabellen unverändert, Stand am Master 25.09., Kürzungsauftrag 3.147, Reihenfolge nach Plan · § 5.3 Tab. 2 ohne Kennwerte · § 8 R Core Team und Hedges · § 11.2a ohne Zahl · § 11.4 R 4.3.3 · § 11.10 Stand · § 12 G1 (K-09) · § 13 Nr. 10 bis 14 · § 14 · § 15. **Über die Liste hinaus, als Folge der Änderungen:** Kennungsbezüge auf das Blatt 25.09. (Nenner K-04 und K-06 statt K-07, Versuche K-11 statt K-04, K-02b entfällt) · § 3.1 „vier- bis achtfach“ durch K-11.4 ersetzt · § 6.5 Erratum nicht beschaffbar · § 1.5 F2 und F3 · Reste der ersten Rechnung in § 11.1, 11.5, 11.7, 11.8, 11.9 und § 12 G3 auf Kennungen umgestellt · Nachtrag 3 der Spezifikation (Teil F.8) in § 1.3 und § 11.10.

**(3) Vergleich** `03_Skripte\\Projektanweisungen_Vergleich_2026-09-25.py` mit `.txt` und Eingangsliste `_Ordnerliste.txt`: 28 Paragrafen geändert, 27 unverändert. Prüfungen (a) Semikolon außerhalb der Zitiersyntax 0 · (b) Ergebniszahl in § 3 und § 11.2a 0 · (c) Dokumentenkarte 403 von 403 Dateien zugeordnet (vorher 91 ohne Zuordnung, Klick) · (d) 20 Wortzahlen in § 5.2 gleich der Messung. Negativprobe mit einer eingeschleusten Zahl und einer fremden Datei: Abbruch wie vorgesehen. **Unabhängige Zweitprüfung** (Subagent ohne Beteiligung): alle Punkte der Übergabe umgesetzt, 17 Befunde (7 muss, alle eingearbeitet). Nicht übernommen: TE 30 m post Verein A in § 11.3 und G4 (erst gegen Tab. H1e prüfen, Task 12) · „6 von 18“ und „6 von 13“ in § 11.9 (Task 11) · der Name „Tab. 2 Stichprobe und Ausgangswerte“ bleibt wie die CSV.

**Klickantworten des Verfassers:** (1) Zuordnung der 91 Dateien: **„Gruppiert, Erledigtes ins Archiv“** — Sammelzeilen in § 1.3, dazu Übergabe 4.1 (22.09.), Textvorschläge 4.1 und 4.2 und Befunde_Sofortblock als erledigt. (2) A8: **„Ja, freigeben“.**

**(4, 5) README und Archiv** (Erzeuger `03_Skripte\\Steuerdokumente_README_Archiv_2026-09-25.py` mit `.txt`): README mit Kopf, Ordnerzeilen und neuem Abschnitt „Was wo gilt“ (fünf Ebenen-Dokumente mit Frage und Änderungsrhythmus, Stand in Kürze, überholte Teile) · `Ordner_aufraeumen.ps1` (BOM und CRLF erhalten): sechs erledigte Übergaben und Fassung 14 in der Papierkorbliste, Steuerungsmuster auf Fassung 15 · Kopien in `_Archiv\\_ersetzt_2026-09-25_Uebergaben` (sechs Dateien) und `_Archiv\\_ersetzt_2026-09-25_Fassung14`.

**Befunde am Rand:** (1) `Umgebung_2026-09-25.txt` enthält die Ausgabe von `citation()` nicht, anders als die Übergabe annahm. Nachgeholt in `03_Skripte\\R_citation_2026-09-25.txt` mit R 4.3.3 (2024-02-29), derselben Version wie die Blindrechnung: „R Core Team (2024). R: A Language and Environment for Statistical Computing“. (2) G25f und G17g (Dateiteil) sind erledigt, beide Dateien liegen seit dem Papierkorb-Lauf (Rev. 93) nicht mehr in `Schreiben\\`. (3) `Uebergabe_4.4_Querverweise_2026-09-12.md` liegt nur als Projektkopie vor, Task 3 liest sie dort. (4) K-11.4 führt eine vierte Ausfallkategorie „falsch aufgenommen“ (10 m post, IG). § 3.1 nennt drei Mechanismen, der Fall ist der Erhebungsstand „10-m-Post nur Verein A“ (F15 § 1.5) — Vormerkung für Task 3. (5) `Manuskriptstand_2026-09-25.py` rechnet 4.7 noch mit dem Budget 720, beim nächsten Lauf 550 (Nachtragsvermerk F15 § 1.3).

**Regeln eingehalten:** kein Manuskripttext, Master unverändert, Zahlen gemessen oder gerechnet, Skripte ohne Semikolon, Blindordner, Abgabe, Datenstand und Workbook unverändert. `00_Steuerung` enthält bis zum Aufräumlauf vier Dateien (Fassung 14 und 15).

**Verfasserschritte:** (1) Fassung 15 vollständig in die Projekteinstellungen kopieren (A8). (2) Danach `Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt (Fassung 14 und sechs Übergaben in den Papierkorb). (3) G27f: Feldaktualisierung beim nächsten Öffnen des Masters. (4) 4.7 in Word prüfen (Plan § 2), vor Task 6.

**Dateien (Ordner):** `00_Steuerung\\Projektanweisungen_Fassung15.md` · `README_Ordnerstruktur.md` · `Ordner_aufraeumen.ps1` · `03_Skripte\\` Projektanweisungen_Fassung15_2026-09-25.py/.txt, Projektanweisungen_Vergleich_2026-09-25.py/.txt mit _Ordnerliste.txt, Steuerdokumente_README_Archiv_2026-09-25.py/.txt, R_citation_2026-09-25.txt, Steuerung_Rev98_2026-09-25.py · `_Archiv\\_ersetzt_2026-09-25_Uebergaben\\` · `_Archiv\\_ersetzt_2026-09-25_Fassung14\\`. Projektkopien: Fassung 15, Sitzungsnotizen, Maßnahmenliste.

**Nächste Schritte (ersetzt Rev. 97):** (0) Verfasserschritte 1 und 2 · (1) Task 2 Textrevision 4.3 mit dem Startsatz aus Plan § 8 · (2) 4.7 prüfen, spätestens vor Task 6 · danach Tasks 3 bis 18 nach Plan § 3. Beim Betreuer offen bleibt nur die Fußnotenfrage.

**Maßnahmenliste:** A8 wieder offen (Fassung 15 einsetzen) · I19 erledigt · G25f, G26i, G26j, G27a, G27b erledigt · G17g Dateiteil erledigt · G30 fortgeschrieben · Zuordnung Task 1 aktualisiert. Offen jetzt {nachher_h} Hauptpunkte und {nachher_t} Teilpunkte (gemessen, vorher {vorher_h} und {vorher_t}).

"""
anker = "### ⭐⭐ NEU (Rev. 97, 25.09.2026, 21:40 MESZ)"
n = ersetze(n, anker, block + anker, "Block Rev. 98")
if chr(59) in block:
    sys.exit("ABBRUCH: Semikolon im Rev.-Block")
open(pn, "w", encoding="utf-8", newline="\n").write(n)
print(f"Ersetzungen ({len(protokoll)}), je genau einmal: " + " · ".join(protokoll))
print(f"Maßnahmenliste offen: vorher {vorher_h} Hauptpunkte, {vorher_t} Teilpunkte, nachher {nachher_h} und {nachher_t}")

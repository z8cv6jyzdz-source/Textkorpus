# -*- coding: utf-8 -*-
"""
Steuerung_Rev141_2026-10-01.py

Zweck:    Schreibt Rev. 141 in Teil 0 der Sitzungsnotizen und ergänzt die Maßnahmenliste (Stand, L9, Summe).
          Task „Statistische Auswertung in Claude Code“: Reproduktionstest vorbereitet.
Eingang:  Cowork_Sitzungsnotizen.md und Massnahmenliste_Datenverarbeitung.md (Stand Rev. 140, gestagt)
Aufruf:   python Steuerung_Rev141_2026-10-01.py <Notizen.md> <Massnahmenliste.md> <Ausgabeordner>
Ausgabe:  beide Dateien im Ausgabeordner (frischer Pfad für die Rückschreibung), Laufprotokoll .txt neben dem Skript
Fassung:  2026-10-01, erste Fassung (Claude)
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSN, AUS = sys.argv[1:4]
ZEIT = datetime.datetime.now().strftime("%H:%M")
md5 = lambda b: hashlib.md5(b).hexdigest()

BLOCK = f"""### ⭐⭐ NEU (Rev. 141, 01.10.2026, {ZEIT} Sitzungsuhr, Auftrag 13:57): Statistische Auswertung in Claude Code — keine neue Auswertung, sondern Reproduktionstest (8.4) vorbereitet: Datenprüfung des Workbooks, Probelauf der Rechenkette in der Originalumgebung, Werkzeuge und Prompt für Claude Code unter Windows

**Auftrag (Verfasser, 01.10., 13:57, wörtlich):** „Die statistische Auswertung der im Projekt definierten Zielgrößen soll nun durchgeführt werden. Im ersten schritt sollen die Daten aus der Excel tabelle systematisch analysiert werden. Auf diesen Daten sollen dann die beschriebenen Statistischen Verfahren angewandt werden. Claude Code soll bei der Aufgabe übernehmen. Prüfe welches Vorgehen nach deiner Arbeitsweise am sinnvollsten ist, welche Schritt vor den Rechnungen der statistischen und deskriptiven verfahren notwendig sind. Ein Prompt soll für Claude Code erstellt werden, da dort die Statistik durchgeführt werden soll. Aber zunächst die vorgeschalteten Schritte“

**Einordnung:** Der Auftrag widerspricht dem Stand: Die Phasen 0 bis 7 sind seit dem 25.09. abgeschlossen (Rev. 88 bis 95), Kapitel 5 steht darauf (Rev. 137). Im Chat benannt. Klick (01.10.): „Reproduktionstest (Empfehlung)“, nicht „Neue Auswertung ab Excel“ und nicht „Methodenprüfung ohne Rechnung“. Ändert keinen Manuskripttext, keine Zahl und keine Reihenfolge.

**Vorgeschaltete Schritte (Datenprüfung):** Das Workbook wurde zuletzt am 25.09. um 08:31 Sitzungsuhr gespeichert, nach dem Einfrieren (passt zu Rev. 88, Nächste Schritte Nr. 1), Prüfsumme jetzt 86087d35…. Struktur- und Exportprüfung der Phase 1 unverändert auf einer Kopie: 0 Verstöße gegen die Abbruchregeln, Rückleseprobe und Abbruchprobe bestanden, die fünf Analysedateien bytegleich mit `Statistik\\Datenstand_2026-09-24`, Datenwörterbuch gleich bis auf das Datum des Datenstands. Kein neuer Datenstand nötig. `03_Skripte\\Datenpruefung_Workbook_2026-10-01.py` mit `.txt`.

**Probelauf in der Originalumgebung (diese Cloud-Sitzung):** Ubuntu 24.04.4 mit r-base-core 4.3.3-2build2, BLAS und LAPACK 3.12.0 wie bei der Blindrechnung. Paket aus dem ZIP unverändert, dazu Datenstand und sieben Anlagen: Ergebnisdatei bytegleich (3194a805…), Referenztests 83 von 83, Grenzfälle 114 von 114, Abgleich nach G.3 ohne Abweichung, 72 weitere Dateien bytegleich, Kennzahlenblatt aus der neuen Ergebnisdatei bytegleich. Jede Zahl des Manuskripts ist damit in der Originalumgebung reproduziert. Zweiter Lauf mit dem Windows-Zweig der neuen Steuerung (unter Linux erzwungen): ebenso. Vermerk `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Probelauf_Linux_2026-10-01.md`.

**Befund für Anhang G (Task 16):** Das archivierte Steuerskript läuft nach dem Quelltext von R 4.3.3 unter Windows nicht durch: `system2(env = …)` setzt die Angaben dort in die Befehlszeile, Rscript liest `LC_ALL=C.UTF-8` als Skriptdatei. Dazu fehlt `dpkg-query`, und G18 in `Grenzfaelle_2026-09-25.R` scheitert an der Maskierung von Backslash-Pfaden durch GNU sha256sum (Zweitprüfung). Vorbereitet ist `Gesamtlauf_Windows_2026-10-01.R` mit den Änderungen W1 bis W4, die Rechenskripte bleiben unverändert. Unter Windows nicht erprobt.

**Prompt für Claude Code:** `04_Uebergaben\\Prompt_Reproduktionstest_2026-10-01.md` (Projektkopie `claude/`). Lauf A mit dem unveränderten Paket (erwarteter Abbruch, Vorprobe zu sha256sum), Lauf B mit der Windows-Steuerung, Vergleich mit `Reproduktion_Vergleich_2026-10-01.py`, Protokoll `02_Befunde\\Reproduktionsprotokoll_<Datum>`, Klickfragen zu Anhang G und Schreibschutz. Die vier Werkzeuge stehen mit SHA-256 im Prompt.

**Zweitprüfung (Subagent):** Prüfsummen, Anzahlen, Umgebung und das Verhalten von R unter Windows am Material und am Quelltext bestätigt. Zehn Befunde (1 A, 5 B, 4 C), alle eingearbeitet: W4 und Vorprobe für G18 (A), Kennzahlenblatt bei nicht bytegleicher Ergebnisdatei, Versionszeile mit „ucrt“, Konsolen außerhalb des Laufordners, Laufzeit gegen das Zeitlimit, Abweichungen von Plan Task 16 d, Prüfsummen der Werkzeuge, elementweiser Vergleich der .rds, Datumsersetzung im Datenwörterbuch, Formulierungen im Vermerk. Korrekturen per Test nachgeprüft: Werte um 3e-15 relativ verändert ergibt „bestanden“, um 0,001 s verändert „nicht bestanden“, Lauf 2 mit W4 „bestanden“.

**Offen beim Verfasser:** Prompt in einer neuen Sitzung im Code-Tab starten (Arbeitsverzeichnis `Bachelorarbeit`). Sonst wie Rev. 137 bis 140.

**Stand der Dateien:** Neu: `03_Skripte\\Datenpruefung_Workbook_2026-10-01.py` mit `.txt` · `03_Skripte\\Reproduktion_2026-10-01\\` mit `Reproduktion_Aufbau_2026-10-01.py`, `Gesamtlauf_Windows_2026-10-01.R`, `Gesamtlauf_Windows_2026-10-01_Diff.txt`, `Reproduktion_Vergleich_2026-10-01.py`, `Vermerk_Probelauf_Linux_2026-10-01.md` und `Probelauf_Linux\\` (Lauf1_Original, Lauf2_Windowszweig) · `04_Uebergaben\\Prompt_Reproduktionstest_2026-10-01.md` · `03_Skripte\\Steuerung_Rev141_2026-10-01.py` mit `.txt`. Geändert: diese Notizen (Rev. 141 auf Rev. 140) und die Maßnahmenliste (Stand, L9, Summe), je Ordner und Projektkopie. Die Projektkopien standen auf Rev. 139 und tragen jetzt auch Rev. 140. Unverändert: Workbook, Datenstand, Abgabe und ZIP, Anlagen der Spezifikation, Kennzahlenblatt, Objekte, Master, Fassung 17, Plan. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** unverändert der Abgleich von Kapitel 5 nach der Übertragung als Schritt 0 von Task 12a, dann Task 12a. Der Reproduktionstest unter Windows kann daneben laufen, er ändert nichts am Manuskript.

"""

STAND_N_ALT = "**Stand: (Rev. 140 — siehe Block oben.)"
STAND_N_NEU = "**Stand: (Rev. 141 — siehe Block oben.) Zuvor: (Rev. 140 — siehe Block oben.)"
ANKER = "### ⭐⭐ NEU (Rev. 140,"

STAND_M_ALT = "**Stand 01.10.2026, 13:32 Sitzungsuhr (Rev. 140 — "
STAND_M_NEU = (f"**Stand 01.10.2026, {ZEIT} Sitzungsuhr (Rev. 141 — Reproduktionstest vorbereitet: Datenprüfung des Workbooks, "
               "Probelauf in der Originalumgebung bestanden, Werkzeuge in `03_Skripte\\Reproduktion_2026-10-01\\` und Prompt "
               "`04_Uebergaben\\Prompt_Reproduktionstest_2026-10-01.md` für Claude Code unter Windows, L9 ergänzt). "
               "Zuvor 01.10.2026, 13:32 Sitzungsuhr (Rev. 140 — ")
L9_ENDE = "Offen: KI-Deklaration mit Mindestinhalt, Nutzungsprotokoll, Anhang G mit Poweranalyse-Eingaben, R-Skripten und Diagrammen, Reproduktionstest.)*"
L9_NEU = L9_ENDE + (" *(Rev. 141, 01.10.: Reproduktionstest vorbereitet. Probelauf in der Originalumgebung bestanden, Ergebnisdatei und "
                    "Kennzahlenblatt bytegleich (Vermerk `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Probelauf_Linux_2026-10-01.md`). "
                    "Offen: Lauf unter Windows nach `04_Uebergaben\\Prompt_Reproduktionstest_2026-10-01.md`. Befund für Anhang G: "
                    "Die archivierte Steuerung läuft unter Windows nicht ohne Anpassung (system2 mit env, dpkg-query, G18 mit sha256sum), "
                    "die Windows-Steuerung mit W1 bis W4 ist vorbereitet.)*")
SUMME_ALT = "| **Summe** | Rev. 140 (01.10.):"
SUMME_NEU = "| **Summe** | Rev. 141 (01.10.): L9 ergänzt, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 140 (01.10.):"

log = []
def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit(f"ABBRUCH: {name} kommt {n}-mal vor statt einmal")
    log.append(f"  {name}: ersetzt")
    return text.replace(alt, neu)

for f in (BLOCK, STAND_M_NEU, L9_NEU, SUMME_NEU):
    if chr(59) in f:   # Semikolon
        raise SystemExit("ABBRUCH: Semikolon im neuen Text")

roh_n = open(NOTIZEN, "rb").read()
roh_m = open(MASSN, "rb").read()
t_n = roh_n.decode("utf-8")
t_m = roh_m.decode("utf-8")
if "(Rev. 141," in t_n:
    raise SystemExit("ABBRUCH: Rev. 141 steht schon in den Notizen")
t_n = ersetze(t_n, STAND_N_ALT, STAND_N_NEU, "Notizen, Stand")
t_n = ersetze(t_n, ANKER, BLOCK + ANKER, "Notizen, Block vor Rev. 140")
t_m = ersetze(t_m, STAND_M_ALT, STAND_M_NEU, "Maßnahmenliste, Stand")
t_m = ersetze(t_m, L9_ENDE, L9_NEU, "Maßnahmenliste, L9")
t_m = ersetze(t_m, SUMME_ALT, SUMME_NEU, "Maßnahmenliste, Summe")

os.makedirs(AUS, exist_ok=True)
neu_n = t_n.encode("utf-8")
neu_m = t_m.encode("utf-8")
open(os.path.join(AUS, "Cowork_Sitzungsnotizen.md"), "wb").write(neu_n)
open(os.path.join(AUS, "Massnahmenliste_Datenverarbeitung.md"), "wb").write(neu_m)
zeilen = [f"Steuerung_Rev141_2026-10-01.py, Lauf {datetime.datetime.now():%Y-%m-%d %H:%M:%S} (Sitzungsuhr)"] + log + [
    f"Cowork_Sitzungsnotizen.md: vorher {len(roh_n)} B MD5 {md5(roh_n)}, nachher {len(neu_n)} B MD5 {md5(neu_n)}",
    f"Massnahmenliste_Datenverarbeitung.md: vorher {len(roh_m)} B MD5 {md5(roh_m)}, nachher {len(neu_m)} B MD5 {md5(neu_m)}",
    "Semikola im neuen Text: 0"]
open(os.path.splitext(os.path.abspath(__file__))[0] + ".txt", "w", encoding="utf-8", newline="\n").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))

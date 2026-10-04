# -*- coding: utf-8 -*-
"""
Steuerung_Rev143_2026-10-01.py

Zweck:    Schreibt Rev. 143 in Teil 0 der Sitzungsnotizen und ergänzt die Maßnahmenliste (Stand, L9, Summe).
          Task „Reproduktionstest der Rechenkette unter Windows (Auswertungsverfahren 8.4) in Claude Code“.
          Rev. 142 hat die parallele Sitzung „Recherche Schritt 2“ um 17:36 vergeben, deshalb Rev. 143.
Eingang:  Cowork_Sitzungsnotizen.md und Massnahmenliste_Datenverarbeitung.md (Stand Rev. 142, Ordner),
          zweit.txt (Absatz Zweitprüfung), klick.txt (Absatz Klickentscheidungen), zwei Kurzangaben zu den Klicks (a) und (b)
Aufruf:   python Steuerung_Rev143_2026-10-01.py <Notizen.md> <Massnahmenliste.md> <Ausgabeordner> <zweit.txt> <klick.txt> "<Klick a kurz>" "<Klick b kurz>"
Ausgabe:  beide Dateien im Ausgabeordner (frischer Pfad für die Rückschreibung), Laufprotokoll .txt neben dem Skript
Fassung:  2026-10-01, erste Fassung (Claude Code)
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSN, AUS, ZWEIT_TXT, KLICK_TXT, KLICK_A, KLICK_B = sys.argv[1:8]
ZEIT = datetime.datetime.now().strftime("%H:%M")
md5 = lambda b: hashlib.md5(b).hexdigest()
ZWEIT = open(ZWEIT_TXT, encoding="utf-8").read().strip()
KLICK = open(KLICK_TXT, encoding="utf-8").read().strip()
MD5_N_SOLL = "73606ce4bfef7e2c01c3584d4b33972e"   # Stand nach Rev. 142 (Steuerung_Rev142_2026-10-01.txt)
MD5_M_SOLL = "c2331c015a2959c0e718853330b3573d"

BLOCK = """### ⭐⭐ NEU (Rev. 143, 01.10.2026, {ZEIT} Sitzungsuhr, Auftrag 16:16): Reproduktionstest der Rechenkette unter Windows (Auswertungsverfahren 8.4) in Claude Code: bestanden mit der Windows-Steuerung, das archivierte Steuerskript bricht unter Windows ab, Protokoll mit Zweitprüfung, Klickfragen zu Anhang G und Schreibschutz

**Auftrag (Verfasser, 01.10., Klick vom 01.10.):** `04_Uebergaben\\Prompt_Reproduktionstest_2026-10-01.md` in einer neuen Sitzung im Code-Tab (Claude Code, Fable 5.1, Arbeitsverzeichnis `Bachelorarbeit`). Keine neue Auswertung, keine neue Zahl für das Manuskript. Lief neben Rev. 142 (Recherche Schritt 2) in einer eigenen Sitzung, Rev. 142 kam um 17:36 über OneDrive an und ist hier berücksichtigt.

**Vorab:** Die vier Werkzeuge, das Workbook (86087d35…) und das ZIP (200b2595…) tragen die Prüfsummen des Prompts, der eigene Diff der Windows-Steuerung ist hunk-identisch mit der mitgelieferten Diff-Datei. Umgebung: Windows 11 (Build 26200), R 4.3.3 ucrt mit eingebautem BLAS und LAPACK 3.11.0, Python 3.11.9, Git Bash mit GNU sha256sum 8.32. Gerechnet im Scratchpad außerhalb von OneDrive, je Lauf ein frischer Ordner aus dem ZIP, Datenstand und Anlagen per SHA-256 geprüft.

**Lauf A (Paket unverändert):** Abbruch beim ersten Kindprozess (Referenztests, Status 5, Schrittausgabe leer), keine Ergebnisdatei. Ursache wie im Vermerk hergeleitet (`system2(env = …)` setzt die Angaben unter Windows in die Befehlszeile), die Erscheinung aber anders als dort erwartet: R 4.3.3 (ucrt) für Windows endet beim Start mit einer Zugriffsverletzung (0xC0000005, von `system2()` als 5 gemeldet), wenn die mit `--file=` übergebene Datei nicht geöffnet werden kann, über Rscript.exe wie über Rterm.exe, bevor eine Meldung geschrieben ist. Die „Fatal error“-Zeile aus Vermerk und Prompt gibt es unter Windows nicht. Vorprobe bestätigt: sha256sum maskiert Backslash-Pfade, G18 scheitert im Original.

**Lauf B (nur Steuerung angepasst, W1 bis W4):** ohne Abbruch, 20,3 min (Linux 6,4 bis 7,1), Referenztests 83 von 83, Grenzfälle 114 von 114, G18 über `sha256sum.cmd` (W4) bestanden, keine Warnungen. Windows lehnt `C.UTF-8` ab (Warnung je Prozess, R bleibt UTF-8, ohne Folge). Ergebnisdatei nicht bytegleich: genau eine von 3.559 Kennungen (S10.TELO.Z05.POST.ALL.X, untere KI-Grenze TE Sprint 5 m post) um eine Binärstelle (6,9 · 10⁻¹⁸ absolut, gewöhnlich relativ 2,1 · 10⁻¹⁶), alle anderen zeichengleich, auch ANCOVA, Bootstrap und Poweranalyse. Abgleich nach G.3 mit dem Skript der Abgabe: EXAKT 1.801, DETERM 1.714, ITERATIV 23, ZUFALL 6 bestanden, NACHRICHT 15, 0 Abweichungen. Kennzahlenblatt aus der neuen Ergebnisdatei: `.md` gleich bis auf die Prüfsumme der Quelle, `_Werte.csv` in der Darstellung gleich, Rohwerte bis 1e-9 gleich (eine Zeile, K-05.1, 17. signifikante Ziffer). Jede Zahl des Manuskripts ist unter Windows reproduziert. Wiederholungslauf B2 auf demselben Rechner: alle Ergebnisse bytegleich mit B. Sechs Grafiken S14 inhaltlich gleich, nur Schriftbild und Dateigröße anders.

**Vergleichsskript:** Zwei Fehler unter Windows, als Befund behandelt, nicht umgangen: Die erste Fassung scheitert bei der elementweisen `.rds`-Prüfung an „command line too long“ (58 lange Pfade), die zweite vergleicht Zahlen in Textform nicht nach DETERM. Neue Fassungen `Reproduktion_Vergleich_2026-10-01_Fassung2.py` und `_Fassung3.py` mit Diff-Dateien, die erste Fassung bleibt unverändert. Dritte Fassung: „Reproduktion bestanden“, keine offenen Punkte, Abschnitte A bis D und G in allen drei Fassungen zeichengleich.

**Urteil:** Reproduktionstest unter Windows bestanden (Maßstab Prompt § 4). Befund für Anhang G (Task 16): Das archivierte Steuerskript läuft unter Windows nicht, gerechnet hat die Windows-Steuerung bei unveränderten Rechenskripten. Zwölf Befunde in `02_Befunde\\Reproduktionsprotokoll_2026-10-01` (.md, .docx, .pdf), darunter: Der Projektordner `Abgabe_R_2026-09-25` trägt in den sechs PNG den seit dem 25.09. dokumentierten Transfer-Chunk caBX, das ZIP ist die Referenz (Pixel gleich).

**Zweitprüfung (Subagenten ohne Beteiligung):** {ZWEIT}

**Klick (Verfasser, 01.10.):** {KLICK}

**Vormerkung Task 16 (Anhang G, Ausführung unter Windows):** Hinweis zur Ausführung nach dem Protokoll: unter Linux (Ubuntu 24.04, R 4.3.3) mit `Gesamtlauf_2026-09-25.R`, unter Windows aus Git Bash mit `Gesamtlauf_Windows_2026-10-01.R` (W1 bis W4, Laufzeit rund 20 min, Warnung zur Spracheinstellung erwartet, Ergebnisdatei bis auf eine Binärstelle einer Kennung gleich, Abgleich nach G.3 ohne Abweichung). Vor der Beilage den Linux-Zweig der Windows-Steuerung einmal unter Linux laufen lassen (rund 7 min, bisher lief unter Linux nur der erzwungene Windows-Zweig). Die Formulierung zum Abbruch des Originals unter Windows nach Protokoll Abschnitt 5, nicht nach dem Vermerk. Abweichungen von Plan Task 16 d stehen im Protokoll Abschnitt 12.

**Stand der Dateien:** Neu: `02_Befunde\\Reproduktionsprotokoll_2026-10-01` (.md, .docx, .pdf) · `03_Skripte\\Reproduktion_2026-10-01\\Reproduktion_Vergleich_2026-10-01_Fassung2.py` mit `_Fassung2_Diff.txt`, `_Fassung3.py` mit `_Fassung3_Diff.txt`, `Protokoll_Hausstil_Lauf_2026-10-01.py`, Ordner `Lauf_Windows\\` (60 Belegdateien und `Ablage_Liste.txt` mit SHA-256) · `03_Skripte\\Steuerung_Rev143_2026-10-01.py` mit `.txt`. Geändert: diese Notizen (Rev. 143 auf Rev. 142) und die Maßnahmenliste (Stand, L9, Summe), nur im Ordner, die Projektkopien erreicht diese Sitzung nicht (der Verfasser lädt bei Bedarf hoch). Unverändert: Workbook, Datenstand, Abgabe und ZIP, Anlagen der Spezifikation, Kennzahlenblatt, Objekte, Master, Fassung 17, Plan, die vier Werkzeuge des Prompts, Vermerk. Kein Skript der Abgabe geändert, keine Zahl von Hand.

**Nächster Schritt:** unverändert der Abgleich von Kapitel 5 nach der Übertragung als Schritt 0 von Task 12a, dann Task 12a. Task 16 d (Reproduktionstest) ist erledigt, Task 16 e (Abgabestand einfrieren) und die übrigen Teile von Task 16 bleiben.

"""
BLOCK = BLOCK.replace("{ZEIT}", ZEIT).replace("{ZWEIT}", ZWEIT).replace("{KLICK}", KLICK)

STAND_N_ALT = "**Stand: (Rev. 142 — siehe Block oben.)"
STAND_N_NEU = "**Stand: (Rev. 143 — siehe Block oben.) Zuvor: (Rev. 142 — siehe Block oben.)"
ANKER = "### ⭐⭐ NEU (Rev. 142,"

STAND_M_ALT = "**Stand 01.10.2026, 17:36 Sitzungsuhr (Rev. 142 — "
STAND_M_NEU = ("**Stand 01.10.2026, " + ZEIT + " Sitzungsuhr (Rev. 143 — Reproduktionstest unter Windows bestanden: Lauf B mit der "
               "Windows-Steuerung reproduziert jede Zahl, das archivierte Steuerskript bricht unter Windows ab, Protokoll "
               "`02_Befunde\\Reproduktionsprotokoll_2026-10-01` mit Zweitprüfung, L9 fortgeschrieben). "
               "Zuvor 01.10.2026, 17:36 Sitzungsuhr (Rev. 142 — ")
L9_ENDE = "die Windows-Steuerung mit W1 bis W4 ist vorbereitet.)*"
L9_NEU = L9_ENDE + (" *(Rev. 143, 01.10.: **Reproduktionstest unter Windows bestanden** (Lauf B mit der Windows-Steuerung W1 bis W4, "
                    "Validierung 83 von 83 und 114 von 114, Abgleich nach G.3 ohne Abweichung, Kennzahlenblatt in der Darstellung "
                    "gleich, eine Kennung in der letzten Binärstelle, Wiederholungslauf bytegleich). Das archivierte Steuerskript "
                    "bricht unter Windows ab (Befund für Anhang G). Protokoll `02_Befunde\\Reproduktionsprotokoll_2026-10-01`, Belege "
                    "`03_Skripte\\Reproduktion_2026-10-01\\Lauf_Windows\\`. Offen in L9: KI-Deklaration mit Mindestinhalt, "
                    "Nutzungsprotokoll, Anhang G mit Poweranalyse-Eingaben, R-Skripten, Diagrammen und Hinweis zur Ausführung unter "
                    "Windows (Klick (a): " + KLICK_A + ", vorher Linux-Zweig der Windows-Steuerung einmal unter Linux laufen lassen), "
                    "Abgabestand mit Prüfsummen einfrieren (8.4 zweiter Satz, Task 16 e, Schreibschutz Klick (b): " + KLICK_B + ").)*")
SUMME_ALT = "| **Summe** | Rev. 142 (01.10.):"
SUMME_NEU = "| **Summe** | Rev. 143 (01.10.): L9 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 142 (01.10.):"

log = []
def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit("ABBRUCH: " + name + " kommt " + str(n) + "-mal vor statt einmal")
    log.append("  " + name + ": ersetzt")
    return text.replace(alt, neu)

for f in (BLOCK, STAND_M_NEU, L9_NEU, SUMME_NEU):
    if chr(59) in f:   # Semikolon
        raise SystemExit("ABBRUCH: Semikolon im neuen Text")

roh_n = open(NOTIZEN, "rb").read()
roh_m = open(MASSN, "rb").read()
if md5(roh_n) != MD5_N_SOLL or md5(roh_m) != MD5_M_SOLL:
    raise SystemExit("ABBRUCH: Eingang nicht auf dem Stand nach Rev. 142 (MD5 " + md5(roh_n) + " / " + md5(roh_m) + ")")
t_n = roh_n.decode("utf-8")
t_m = roh_m.decode("utf-8")
if "(Rev. 143," in t_n:
    raise SystemExit("ABBRUCH: Rev. 143 steht schon in den Notizen")
t_n = ersetze(t_n, STAND_N_ALT, STAND_N_NEU, "Notizen, Stand")
t_n = ersetze(t_n, ANKER, BLOCK + ANKER, "Notizen, Block vor Rev. 142")
t_m = ersetze(t_m, STAND_M_ALT, STAND_M_NEU, "Maßnahmenliste, Stand")
t_m = ersetze(t_m, L9_ENDE, L9_NEU, "Maßnahmenliste, L9")
t_m = ersetze(t_m, SUMME_ALT, SUMME_NEU, "Maßnahmenliste, Summe")

os.makedirs(AUS, exist_ok=True)
neu_n = t_n.encode("utf-8")
neu_m = t_m.encode("utf-8")
open(os.path.join(AUS, "Cowork_Sitzungsnotizen.md"), "wb").write(neu_n)
open(os.path.join(AUS, "Massnahmenliste_Datenverarbeitung.md"), "wb").write(neu_m)
zeilen = ["Steuerung_Rev143_2026-10-01.py, Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Sitzungsuhr)"] + log + [
    "Cowork_Sitzungsnotizen.md: vorher " + str(len(roh_n)) + " B MD5 " + md5(roh_n) + ", nachher " + str(len(neu_n)) + " B MD5 " + md5(neu_n),
    "Massnahmenliste_Datenverarbeitung.md: vorher " + str(len(roh_m)) + " B MD5 " + md5(roh_m) + ", nachher " + str(len(neu_m)) + " B MD5 " + md5(neu_m),
    "Semikola im neuen Text: 0"]
open(os.path.splitext(os.path.abspath(__file__))[0] + ".txt", "w", encoding="utf-8", newline="\n").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))

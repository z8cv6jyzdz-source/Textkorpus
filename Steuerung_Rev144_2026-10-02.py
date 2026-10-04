# -*- coding: utf-8 -*-
"""
Steuerung_Rev144_2026-10-02.py

Zweck:    Schreibt Rev. 144 in Teil 0 der Sitzungsnotizen und ergänzt die Maßnahmenliste (Stand, L9, Summe).
          Task „Linux-Zweig der Windows-Steuerung unter Linux prüfen und Ausführungshinweis für Anhang G vorschlagen“.
          Vor dem Schreiben geprüft: jüngste Rev. in den Notizen ist 143, keine parallele Sitzung hat seither geschrieben
          (MD5 unten). Ändert sich der Eingang, bricht das Skript ab und die Rev. ist neu zu bestimmen.
Eingang:  Cowork_Sitzungsnotizen.md und Massnahmenliste_Datenverarbeitung.md (Stand Rev. 143, Ordner),
          zweit.txt (Absatz Zweitprüfung), klick.txt (Absatz Klickentscheidungen), zwei Kurzangaben zu den Klicks (a) und (b)
Aufruf:   python Steuerung_Rev144_2026-10-02.py <Notizen.md> <Massnahmenliste.md> <Ausgabeordner> <zweit.txt> <klick.txt> "<Klick a kurz>" "<Klick b kurz>" "<Auftragszeit>"
Ausgabe:  beide Dateien im Ausgabeordner (frischer Pfad für die Rückschreibung), Laufprotokoll .txt neben dem Skript
Fassung:  2026-10-02, erste Fassung (Claude Code)
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSN, AUS, ZWEIT_TXT, KLICK_TXT, KLICK_A, KLICK_B, AUFTRAG = sys.argv[1:9]
ZEIT = datetime.datetime.now().strftime("%H:%M")
md5 = lambda b: hashlib.md5(b).hexdigest()
ZWEIT = open(ZWEIT_TXT, encoding="utf-8").read().strip()
KLICK = open(KLICK_TXT, encoding="utf-8").read().strip()
MD5_N_SOLL = "f3d9b1da27c587b9a6950921b6aebf96"   # Stand nach Rev. 143 (Steuerung_Rev143_2026-10-01.txt)
MD5_M_SOLL = "8d1cd14ca645bd4450e0dd89a8dbdd5f"

BLOCK = """### ⭐⭐ NEU (Rev. 144, 02.10.2026, {ZEIT} Sitzungsuhr, Auftrag {AUFTRAG}): Linux-Zweig der Windows-Steuerung unter Linux (WSL 2, Ubuntu-24.04) in Claude Code: rechnet wie das archivierte Steuerskript, Ergebnisdatei und Kennzahlenblatt bytegleich, sechs Grafiken nur in der Schrift verschieden (Ursache Schriftausstattung, Kontrolllauf D), Vermerk mit Zweitprüfung, Ausführungshinweis als Vorschlag für Task 16

**Auftrag (Verfasser, 02.10., Folge von Klick (a) vom 01.10.):** `04_Uebergaben\\Prompt_Linuxlauf_Windowssteuerung_2026-10-02.md` in Claude Code (Opus 5.5, Arbeitsverzeichnis `Bachelorarbeit`), gerechnet unter WSL 2 mit Ubuntu-24.04. Keine neue Auswertung, keine neue Zahl für das Manuskript. Ein erster Anlauf am 02.10. hatte in § 0 angehalten (WSL ohne Distribution), der Verfasser hat Ubuntu-24.04 und r-base-core danach selbst eingerichtet.

**Vorab:** Vorbedingung erfüllt, laut apt-Protokoll installierte der Verfasser r-base-core am 02.10. mit `apt-get install -y --no-install-recommends r-base-core`. Die vier Werkzeuge tragen auf der Windows- und der Ubuntu-Seite die Prüfsummen des Prompts. Umgebung: Ubuntu 24.04.5, WSL 3.0.1.0, r-base-core 4.3.3-2build2, libblas3 und liblapack3 3.12.0-3build1.1 wie Soll, libc6 2.39-0ubuntu8.8 statt 8.7 (Sicherheitsaktualisierung ohne Änderung an der Mathematikbibliothek, nach Prompt weitergerechnet), Python 3.12.3. Die Sitzung hat nichts installiert und kein sudo benutzt.

**Lauf C (Windows-Steuerung unverändert gestartet, Linux-Zweig):** Status 0, 13,3 min (Cloud 6,4 bis 7,1 min), Prüfsummenskript 3,2 min. Linux-Zweig belegt: Steuerungszeile „Linux-Zweig“, keine Zeile zur G18-Gegenprobe, keine Warnung zur Spracheinstellung, Umgebungsdatei mit `dpkg-query`. Ergebnisdatei bytegleich (3194a805…), Validierung 83 von 83 und 114 von 114, Abgleich nach G.3 ohne Abweichung, Kennzahlenblatt bytegleich (per SHA-256), 41 Zwischendateien und 25 R-Skripte bytegleich, Schrittausgaben bis auf Zeitstempel gleich.

**Grafiken S14:** Die sechs PNG sind nicht bytegleich mit dem Archiv, nur die Schrift ist anders (2,3 bis 3,0 % der Pixel, nur Text, in den Q-Q-Diagrammen ist der Titel rechts abgeschnitten). fontconfig wählt hier DejaVu Sans, die Titelbreite im Archiv passt zu Schriftmaßen wie Arial. Kontrolllauf D mit dem archivierten `Gesamtlauf_2026-09-25.R` in derselben Umgebung (10,6 min) ist mit Lauf C in 74 Dateien bytegleich, darunter alle sechs Grafiken. Ursache ist die Schriftausstattung, nicht die Steuerung. Der Maßstabspunkt „Grafiken bytegleich wie im Probelauf“ ist damit nicht erfüllt, Klickfrage (b).

**Werkzeuge:** Das Vergleichsskript (dritte Fassung) erklärt Grafikunterschiede pauschal und meldet „bestanden“, den strengeren Punkt des Prompts deckt es nicht ab (Grenze benannt, Skript unverändert). Zwei Fehler in Sitzungswerkzeugen, als Befund behandelt: Das eigene Prüfskript zum Linux-Zweig meldete in der ersten Fassung einen Fehlalarm („Abbruch“ in der Schlusszeile), zweite Fassung mit Gegentest. Das Startskript für Prüfung und Vergleich schrieb als Status den Rückgabewert von `date`, die Exit-Status sind durch einen Nachlauf belegt.

**Urteil:** Nach dem vorab festgelegten Maßstab ist Lauf C nicht bestanden (Grafiken). Der Verfasser hat die Abweichung per Klick (b) als erklärt gewertet, damit gilt Lauf C als bestanden und beide Zweige der Windows-Steuerung sind belegt. Belegt ist: Der Linux-Zweig rechnet wie `Gesamtlauf_2026-09-25.R`, in allen Zahlen gleich dem Archiv und unter denselben Bedingungen in allen geschriebenen Dateien ohne Zeitstempel gleich dem archivierten Steuerskript. Zwölf Befunde in `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Linuxzweig_2026-10-02.md` (Nachtrag zum Reproduktionsprotokoll vom 01.10., das unverändert bleibt).

**Zweitprüfung (Subagenten ohne Beteiligung):** {ZWEIT}

**Klick (Verfasser, 02.10.):** {KLICK}

**Vormerkung Task 16 (Anhang G):** `Gesamtlauf_Windows_2026-10-01.R` kommt als eigene Datei neben das unveränderte `Gesamtlauf_2026-09-25.R` (Klick (a) vom 01.10., Klick (b) vom 02.10.). Ausführungshinweis als Vorschlag `04_Uebergaben\\Vorschlag_Ausfuehrungshinweis_Anhang_G_2026-10-02.md`: Datei `LIESMICH.txt` für das Abgabepaket (Linux mit beiden Steuerskripten gleichwertig, Windows aus Git Bash mit der Windows-Steuerung, Abbruch des Originals unter Windows in einem Satz, Prüfung mit ZIP-Prüfsumme, Prüfsummenskript und Abgleichskript, Schriftabhängigkeit der Diagramme) und drei Sätze für den Fließtext, je Aussage mit Quelle. Den Umfang von Anhang G entscheidet weiter Klickfrage 12.

**Stand der Dateien:** Neu: `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Linuxzweig_2026-10-02.md` · Ordner `03_Skripte\\Reproduktion_2026-10-01\\Lauf_Linux_Windowssteuerung\\` (82 Belegdateien und `Ablage_Liste.txt` mit SHA-256 an der Quelle und auf der Windows-Seite nachgerechnet, darunter Läufe C und D, Grafikanalyse, Protokollauszüge aus Ubuntu, Skripte, Ergebnis der Zweitprüfung) · `04_Uebergaben\\Vorschlag_Ausfuehrungshinweis_Anhang_G_2026-10-02.md` · `03_Skripte\\Steuerung_Rev144_2026-10-02.py` mit `.txt`. Geändert: diese Notizen (Rev. 144 auf Rev. 143) und die Maßnahmenliste (Stand, L9, Summe), nur im Ordner, die Projektkopien erreicht diese Sitzung nicht. Unverändert (245 Dateien gegen eine Momentaufnahme vom Beginn per SHA-256 geprüft): Abgabe und ZIP, `Statistik` mit Workbook und Datenstand, Anlagen der Spezifikation, Kennzahlenblatt mit Erzeuger, Objekte, Master, Reproduktionsprotokoll vom 01.10., Werkzeuge und Vermerk zum Probelauf in `Reproduktion_2026-10-01`. Kein Skript der Abgabe geändert, auch die Windows-Steuerung nicht, keine Zahl von Hand. Die Arbeitsordner `~/repro_2026-10-02` (Läufe C und D) bleiben in Ubuntu liegen.

**Nächster Schritt:** unverändert der Abgleich von Kapitel 5 nach der Übertragung als Schritt 0 von Task 12a, dann Task 12a. In Task 16 bleiben KI-Deklaration, Nutzungsprotokoll, Anhang G mit Klickfrage 12 (mit Windows-Steuerung und `LIESMICH.txt` nach Klick) und Task 16 e (Abgabestand einfrieren, Schreibschutz als Verfasserschritt offen).

"""
BLOCK = BLOCK.replace("{ZEIT}", ZEIT).replace("{AUFTRAG}", AUFTRAG).replace("{ZWEIT}", ZWEIT).replace("{KLICK}", KLICK)

STAND_N_ALT = "**Stand: (Rev. 143 — siehe Block oben.)"
STAND_N_NEU = "**Stand: (Rev. 144 — siehe Block oben.) Zuvor: (Rev. 143 — siehe Block oben.)"
ANKER = "### ⭐⭐ NEU (Rev. 143,"

STAND_M_ALT = "**Stand 01.10.2026, 19:16 Sitzungsuhr (Rev. 143 — "
STAND_M_NEU = ("**Stand 02.10.2026, " + ZEIT + " Sitzungsuhr (Rev. 144 — Linux-Zweig der Windows-Steuerung unter Linux geprüft "
               "(WSL 2, Ubuntu-24.04): rechnet wie das archivierte Steuerskript, Ergebnisdatei und Kennzahlenblatt bytegleich, "
               "sechs Grafiken nur in der Schrift verschieden, Vermerk `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Linuxzweig_2026-10-02.md` "
               "mit Zweitprüfung, Ausführungshinweis für Anhang G vorgeschlagen, L9 fortgeschrieben). "
               "Zuvor 01.10.2026, 19:16 Sitzungsuhr (Rev. 143 — ")
L9_ENDE = "Schreibschutz Klick (b): ja, Verfasserschritt offen).)*"
L9_NEU = L9_ENDE + (" *(Rev. 144, 02.10.: **Linux-Zweig der Windows-Steuerung unter Linux geprüft** (WSL 2, Ubuntu-24.04, Lauf C): "
                    "rechnet wie `Gesamtlauf_2026-09-25.R`, Ergebnisdatei und Kennzahlenblatt bytegleich, Validierung 83 von 83 und "
                    "114 von 114, Abgleich nach G.3 ohne Abweichung. Die sechs Grafiken S14 sind nur in der Schrift verschieden "
                    "(Schriftausstattung der Umgebung, Kontrolllauf D mit dem archivierten Steuerskript bytegleich mit Lauf C), "
                    "Klick (b): " + KLICK_B + ". Vermerk `03_Skripte\\Reproduktion_2026-10-01\\Vermerk_Linuxzweig_2026-10-02.md`, "
                    "Belege `03_Skripte\\Reproduktion_2026-10-01\\Lauf_Linux_Windowssteuerung\\`. Ausführungshinweis vorgeschlagen "
                    "(`04_Uebergaben\\Vorschlag_Ausfuehrungshinweis_Anhang_G_2026-10-02.md`, Klick (a): " + KLICK_A + "). "
                    "Offen in L9: KI-Deklaration mit Mindestinhalt, Nutzungsprotokoll, Anhang G mit Klickfrage 12 (Poweranalyse-Eingaben, "
                    "R-Skripte, Diagramme, Windows-Steuerung mit `LIESMICH.txt`), Abgabestand mit Prüfsummen einfrieren (Task 16 e, "
                    "Schreibschutz als Verfasserschritt offen).)*")
SUMME_ALT = "| **Summe** | Rev. 143 (01.10.):"
SUMME_NEU = "| **Summe** | Rev. 144 (02.10.): L9 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 143 (01.10.):"

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
    raise SystemExit("ABBRUCH: Eingang nicht auf dem Stand nach Rev. 143 (MD5 " + md5(roh_n) + " / " + md5(roh_m) + "), Rev. neu bestimmen")
t_n = roh_n.decode("utf-8")
t_m = roh_m.decode("utf-8")
if "(Rev. 144," in t_n:
    raise SystemExit("ABBRUCH: Rev. 144 steht schon in den Notizen")
t_n = ersetze(t_n, STAND_N_ALT, STAND_N_NEU, "Notizen, Stand")
t_n = ersetze(t_n, ANKER, BLOCK + ANKER, "Notizen, Block vor Rev. 143")
t_m = ersetze(t_m, STAND_M_ALT, STAND_M_NEU, "Maßnahmenliste, Stand")
t_m = ersetze(t_m, L9_ENDE, L9_NEU, "Maßnahmenliste, L9")
t_m = ersetze(t_m, SUMME_ALT, SUMME_NEU, "Maßnahmenliste, Summe")

os.makedirs(AUS, exist_ok=True)
neu_n = t_n.encode("utf-8")
neu_m = t_m.encode("utf-8")
open(os.path.join(AUS, "Cowork_Sitzungsnotizen.md"), "wb").write(neu_n)
open(os.path.join(AUS, "Massnahmenliste_Datenverarbeitung.md"), "wb").write(neu_m)
zeilen = ["Steuerung_Rev144_2026-10-02.py, Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Sitzungsuhr)"] + log + [
    "Cowork_Sitzungsnotizen.md: vorher " + str(len(roh_n)) + " B MD5 " + md5(roh_n) + ", nachher " + str(len(neu_n)) + " B MD5 " + md5(neu_n),
    "Massnahmenliste_Datenverarbeitung.md: vorher " + str(len(roh_m)) + " B MD5 " + md5(roh_m) + ", nachher " + str(len(neu_m)) + " B MD5 " + md5(neu_m),
    "Semikola im neuen Text: 0"]
open(os.path.splitext(os.path.abspath(__file__))[0] + ".txt", "w", encoding="utf-8", newline="\n").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))

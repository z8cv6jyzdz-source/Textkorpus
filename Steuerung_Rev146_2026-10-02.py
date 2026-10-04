# -*- coding: utf-8 -*-
"""
Steuerung_Rev146_2026-10-02.py

Zweck:    Schreibt Rev. 146 in Teil 0 der Sitzungsnotizen, schreibt die Maßnahmenliste fort (Stand, G35, G37, H13,
          Taskzeile 11, Summe) und ersetzt in Textvorschlag 5 § 11 die Absätze zur Übertragung und zum offenen Abgleich
          durch das Ergebnis. Anlass: Anweisung des Verfassers 02.10., 12:31 „Kapitel 5 per Skript einbauen“ (Schritt 0
          von Task 12a), Einbau, Rückschreibung, Abgleich, Messskript Fassung 4 und Endabgleich am Master.
Eingang:  Cowork_Sitzungsnotizen.md und Massnahmenliste_Datenverarbeitung.md (Stand Rev. 145, Ordner),
          Textvorschlag_5_2026-09-30.md (Stand 01.10., Ordner)
Aufruf:   python Steuerung_Rev146_2026-10-02.py <Notizen.md> <Massnahmenliste.md> <Textvorschlag_5.md> <Ausgabeordner>
Ausgabe:  drei Dateien im Ausgabeordner (frischer Pfad für die Rückschreibung), Laufprotokoll .txt neben dem Skript
Fassung:  2026-10-02, erste Fassung. Ohne Semikolon im neuen Text (Prüfung mit chr(59)).
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSN, TV5, AUS = sys.argv[1:5]
ZEIT = datetime.datetime.now().strftime("%H:%M")
md5 = lambda b: hashlib.md5(b).hexdigest()
MD5_N_SOLL = "8be53f1a2a1faf6bbf505b05be35e1bd"   # Stand nach Rev. 145 (Ordner, gestagt 02.10.)
MD5_M_SOLL = "67c3382290db4b3a5b974fb622e57c29"
MD5_T_SOLL = "4bf7a417388c31a03e0e477365136e31"   # Textvorschlag 5, Stand 01.10. (Rev. 137)

BLOCK = """### ⭐⭐ NEU (Rev. 146, 02.10.2026, {ZEIT} Sitzungsuhr, Anweisung 12:31): Schritt 0 von Task 12a — Kapitel 5 per Skript in den Master eingebaut, Altbestand gelöscht, Abgleich bestanden, Messskript Fassung 4 und Endabgleich am Master, F9 offen

**Anweisung (Verfasser, 02.10., 12:31, wörtlich):** „Kapitel 5 per Skript einbauen“. Direkter Einbau auf ausdrückliche Anweisung (F17 § 1.2), statt der am 01.10. angekündigten Übertragung durch den Verfasser. Vorausgegangen war um 12:10 die Frage nach den nächsten Schritten, beantwortet im Chat mit der Reihenfolge nach Plan (Nachtrag 30.09.).

**Eingang:** Der Master war seit dem 30.09., 20:48 Sitzungsuhr unverändert (57.471 Byte, MD5 `c7657a2c…`, gleich der Archivkopie `_Archiv\\_ersetzt_2026-09-30_Master\\Bachelorarbeit_Geruest_v1_vor_Kapitel5_2026-09-30.docx`, keine `comments.xml`). Die Übertragung durch den Verfasser hatte nicht stattgefunden. Bei der ersten Prüfung nach 12:10 war der Master in Word geöffnet („open_in_another_app“), beim Neustagen nach der Anweisung nicht mehr gesperrt.

**Einbau:** `03_Skripte\\Master_5_2026-09-30.py <Master> Textvorschlag_5_2026-09-30.json <Ausgabe> --altbestand`, Skript und json per MD5 gleich den Fassungen aus Task 11. Protokoll: Überschriften 5.1 und 5.2 mit zwei Verzeichnis-Textmarken entfernt, sechs Absätze unter „5 Ergebnisse“ eingefügt · Altbestand (M24) mit 10 Überschriften, 25 Textabsätzen, 4.920 Wörtern und 10 Textmarken entfernt · Absätze 225 → 194. Ergebnis 39.115 Byte, MD5 `53cc8f368769ee3ed3abf57197c740fb`, bytegleich mit dem Referenzstand vom 30.09. (Textvorschlag 5 § 11, dort gerendert geprüft). Validierung gegen das Original (`validate.py` des docx-Skills) bestanden.

**Rückschreibung:** aus frischem Ausgabepfad, mit Schutz gegen eine zwischenzeitliche Änderung (Dateizeit des Eingangs), um 12:35 Sitzungsuhr. Danach neu gestagt: 39.115 Byte, MD5 `53cc8f36…` gleich der Ausgabe.

**Abgleich (`03_Skripte\\Abgleich_Kapitel5_Master_2026-10-01.py`, Ausgabe `.txt` daneben):** keine `comments.xml` · 194 Absätze, ohne Verzeichnisse und Felder 146, Formatvorlage und Text aller 130 nicht leeren Absätze gleich der Referenz · Kapitel 5 mit sechs Absätzen (49, 80, 66, 41, 146 und 68 Wörter), zeichengleich mit Textvorschlag 5 § 1, Formatvorlage Standard, ohne Absatz- und Laufeigenschaften, zusammen 450 Wörter · keine entfernte Überschrift mehr im Text. Einziger Befund: Das Inhaltsverzeichnis führt noch 12 entfernte Überschriften (2, 2.1 bis 2.5 mit 2.4.1 bis 2.4.3, 3, 5.1 und 5.2), F9 durch den Verfasser.

**Messskript Fassung 4 am Master (`03_Skripte\\Manuskriptstand_2026-09-25.txt` und `.csv`):** dieselben Werte wie am Referenzstand (Textvorschlag 5 § 7.2), die `.csv` bytegleich: Einleitung 930 gegen 1.500 · Kapitel 4 (4.1 bis 4.7) 2.416 gegen 2.550 · Kapitel 5 450 gegen 450 · Absatztext 3.796 gegen 6.350 · 0 Semikola und 0 Abschnittsverweise in Kapitel 1 bis 7 · 7 Platzhalter, alle in Anhang H · Prognose 27,8 Seiten (Modellrechnung). Das Semikolon in Anhang C bleibt vorgemerkt (Textvorschlag 5 § 9.6).

**Endabgleich Fassung 3 am Master (Ausgaben in `03_Skripte\\Endabgleich_2026-10-02_Kapitel5\\`):** 357 Zahlen, 23 Satzprüfungen, davon 21 stimmen, die zwei Abweichungen sind die erwarteten (SP6: Tab. 1 kommt erst in Task 18 · SP11: 45-s-Pause der Stufe 1, entfallen mit Klick G28h), Vorschläge 0. Die Zahlenliste ist bytegleich mit dem Lauf am Referenzstand. Die Zahlenliste `03_Skripte\\Endabgleich_Manuskript_2026-09-25_Zahlen.csv` bleibt bis zum Endabgleich Fassung 4 in Task 18 unverändert (Textvorschlag 5 § 9.6 Nr. 10).

**Offen beim Verfasser:** (1) F9 im Master (Inhaltsverzeichnis, danach Word schließen) · (2) Literatur für Task 12a: H13 bis H15 Priorität 1, Klusemann et al. (2012) liegt seit dem 01.10. im Ordner · (3) Schreibschutz auf `Abgabe_R_2026-09-25\\` und das ZIP, danach SHA-256 des ZIP prüfen (Klick (b) vom 01.10.) · übrige Punkte wie Rev. 137 bis 145.

**Stand der Dateien:** Geändert: `Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (39.115 Byte, MD5 `53cc8f36…`) · `03_Skripte\\Manuskriptstand_2026-09-25.txt` und `.csv` (Fassung 4 am Master) · `04_Uebergaben\\Textvorschlag_5_2026-09-30.md` (Kopf und § 11: Ergebnis von Einbau und Abgleich) · diese Notizen (Rev. 146 auf Rev. 145) und die Maßnahmenliste (Stand, G35, G37, H13, Taskzeile 11, Summe), je Ordner und Projektkopie, die Projektkopien von Notizen und Maßnahmenliste damit auch auf dem Stand von Rev. 143 bis 145. Neu: `03_Skripte\\Abgleich_Kapitel5_Master_2026-10-01.txt` · `03_Skripte\\Endabgleich_2026-10-02_Kapitel5\\` (Abgleichprotokoll, Laufprotokoll, Zahlenliste) · `03_Skripte\\Steuerung_Rev146_2026-10-02.py` mit `.txt`. Unverändert: Archivkopie des Masters vor Kapitel 5, Kennzahlenblatt, Objekte, Fassung 17, Plan, die Zahlenliste in `03_Skripte`. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** Task 12a (6.1 Einordnung der Ergebnisse, 700 Wörter) mit dem Startsatz aus Plan § 8 (ab 30.09.), Schritt 0 ist erledigt. Vormerkungen in Textvorschlag 5 § 9.3, Vergleichsstudien nach Rev. 142 nur als Kontext, zitiert wird nur, was als Volltext im Ordner liegt (H13 bis H15).

"""
BLOCK = BLOCK.replace("{ZEIT}", ZEIT)

STAND_N_ALT = "**Stand: (Rev. 145 — siehe Block oben.)"
STAND_N_NEU = "**Stand: (Rev. 146 — siehe Block oben.) Zuvor: (Rev. 145 — siehe Block oben.)"
ANKER = "### ⭐ NACHTRAG (Rev. 145,"

STAND_M_ALT = "**Stand 02.10.2026, 12:08 Sitzungsuhr (Rev. 145 — "
STAND_M_NEU = ("**Stand 02.10.2026, " + ZEIT + " Sitzungsuhr (Rev. 146 — Schritt 0 von Task 12a: Kapitel 5 per Skript in den Master "
               "eingebaut (Anweisung des Verfassers 12:31), Altbestand gelöscht (M24), Abgleich bestanden, Messskript Fassung 4 "
               "und Endabgleich am Master, F9 offen. G35, G37, H13 und Taskzeile 11 fortgeschrieben). "
               "Zuvor 02.10.2026, 12:08 Sitzungsuhr (Rev. 145 — ")
G35_ENDE = ("im Master löscht der Verfasser mit der Übertragung von Kapitel 5 (01.10.), Abgleich offen (Teil 0 Rev. 137).)*")
G35_NEU = G35_ENDE + (" *(Rev. 146, 02.10.: (e) erledigt: Altbestand im Master gelöscht, per Skript auf Anweisung des Verfassers "
                      "(02.10., 12:31), Abgleich bestanden, Master 39.115 Byte, MD5 `53cc8f36…` (Teil 0 Rev. 146). "
                      "F9 durch den Verfasser offen.)*")
G37_ENDE = ("Fassung 18 § 5.3 und § 11.9, Ausnahme zur 18 in Kapitel 5 · Skill mit Kapitel 5 als ein Abschnitt).)*")
G37_NEU = G37_ENDE + (" *(Rev. 146, 02.10.: (e) Kapitel-5-Teil erledigt: Überschriften 5.1 und 5.2 per Skript entfernt (M28), "
                      "Abgleich bestanden, F9 durch den Verfasser offen.)*")
H13_ENDE = "Vor jeder Zitation T1-Steckbrief und T4-Prüfung. *(Sitzung 30.09., Rev. 135)*"
H13_NEU = H13_ENDE + (" *(Rev. 146, 02.10.: Klusemann et al. (2012) liegt seit dem 01.10. in `Ideen und Studien` "
                      "(Dateizeit 15:25 Sitzungsuhr), vor der Zitation T1-Steckbrief und T4-Prüfung. "
                      "Die übrigen Posten bleiben offen.)*")
TASK11_ALT = "Übertragung in den Master durch den Verfasser (01.10.), Abgleich offen) | erledigt:"
TASK11_NEU = ("Übertragung durch den Verfasser vorgesehen (01.10.), Einbau per Skript auf Anweisung des Verfassers (02.10.), "
              "Abgleich bestanden, Rev. 146) | erledigt:")
TASK11B_ALT = "mit dem Abgleich nach der Übertragung: G35 (e) und G37 (e) Kapitel 5"
TASK11B_NEU = "mit dem Abgleich (02.10., Rev. 146) erledigt: G35 (e) und G37 (e) Kapitel 5"
SUMME_ALT = "| **Summe** | Rev. 145 (02.10.):"
SUMME_NEU = ("| **Summe** | Rev. 146 (02.10.): G35 (e) und G37 (e) Kapitel-5-Teil erledigt, H13 und Taskzeile 11 fortgeschrieben, "
             "keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 145 (02.10.):")

KOPF_ALT = "Stand nach Zweitprüfung und Einbau als Referenz, Übertragung in den Master durch den Verfasser (§ 11)"
KOPF_NEU = ("Stand nach Zweitprüfung und Einbau als Referenz, Einbau in den Master per Skript auf Anweisung des Verfassers "
            "am 02.10. (§ 11)")
P1_START = "**Übertragung in den Master: durch den Verfasser.**"
P1_ENDE = "Der Master wurde aus dieser Sitzung nicht beschrieben."
P2_START = "**Abgleich nach der Übertragung (offen):**"
P2_ENDE = "sonst Schritt 0 von Task 12a (Plan § 8, Startsatz 12a)."
P_NEU = ("**Übertragung in den Master:** Vorgesehen war die Übertragung durch den Verfasser. Word sperrte den Master am 30.09. "
         "bei jeder Prüfung bis 23:18 („open_in_another_app“), danach war der Rechner bis zum Morgen nicht mit der Sitzung "
         "verbunden. Am 01.10. um 07:34 meldete der Verfasser: „Rechner läuft, ich führe die Übertragung in das Word-Dokument "
         "durch“. Bis zum 02.10. blieb der Master unverändert (Stand 30.09., 20:48 Sitzungsuhr, MD5 `c7657a2c…`). Am 02.10. "
         "um 12:31 wies der Verfasser an: „Kapitel 5 per Skript einbauen“ (direkter Einbau nach F17 § 1.2, Teil 0 Rev. 146). "
         "Einbau mit `Master_5_2026-09-30.py … --altbestand` auf dem neu gestagten Master, Ergebnis bytegleich mit dem "
         "Referenzstand (39.115 Byte, MD5 `53cc8f368769ee3ed3abf57197c740fb`), Validierung bestanden. Rückschreibung aus "
         "frischem Ausgabepfad mit Schutz gegen eine zwischenzeitliche Änderung um 12:35 (Sitzungsuhr), danach neu gestagt, "
         "MD5 gleich der Ausgabe.\n\n"
         "**Abgleich nach dem Einbau (02.10., bestanden):** `03_Skripte\\Abgleich_Kapitel5_Master_2026-10-01.py` mit Ausgabe "
         "`.txt` daneben: keine `comments.xml`, alle 130 nicht leeren Absätze in Formatvorlage und Text gleich der Referenz, "
         "Kapitel 5 mit sechs Absätzen zeichengleich mit § 1 in der Formatvorlage Standard ohne Direktformatierung, "
         "450 Wörter, Überschriften 5.1 und 5.2 und Altbestand entfernt. Einziger Befund: Das Inhaltsverzeichnis führt noch "
         "12 entfernte Überschriften, F9 durch den Verfasser. Messskript Fassung 4 und Endabgleich Fassung 3 am Master mit "
         "denselben Werten wie am Referenzstand (§ 7.2 und oben), Ausgaben in `03_Skripte\\Manuskriptstand_2026-09-25.txt` "
         "und `.csv` und in `03_Skripte\\Endabgleich_2026-10-02_Kapitel5\\`.")

log = []
def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit("ABBRUCH: " + name + " kommt " + str(n) + "-mal vor statt einmal")
    log.append("  " + name + ": ersetzt")
    return text.replace(alt, neu)

for f in (BLOCK, STAND_M_NEU, G35_NEU, G37_NEU, H13_NEU, TASK11_NEU, TASK11B_NEU, SUMME_NEU, KOPF_NEU, P_NEU):
    if chr(59) in f:
        raise SystemExit("ABBRUCH: Semikolon im neuen Text")

roh_n = open(NOTIZEN, "rb").read()
roh_m = open(MASSN, "rb").read()
roh_t = open(TV5, "rb").read()
if md5(roh_n) != MD5_N_SOLL or md5(roh_m) != MD5_M_SOLL or md5(roh_t) != MD5_T_SOLL:
    raise SystemExit("ABBRUCH: Eingang nicht auf dem erwarteten Stand (MD5 " + md5(roh_n) + " / " + md5(roh_m) + " / "
                     + md5(roh_t) + "), Rev. neu bestimmen")
t_n = roh_n.decode("utf-8")
t_m = roh_m.decode("utf-8")
t_t = roh_t.decode("utf-8")
if "(Rev. 146," in t_n:
    raise SystemExit("ABBRUCH: Rev. 146 steht schon in den Notizen")

t_n = ersetze(t_n, STAND_N_ALT, STAND_N_NEU, "Notizen, Stand")
t_n = ersetze(t_n, ANKER, BLOCK + ANKER, "Notizen, Block vor Rev. 145")
t_m = ersetze(t_m, STAND_M_ALT, STAND_M_NEU, "Maßnahmenliste, Stand")
t_m = ersetze(t_m, G35_ENDE, G35_NEU, "Maßnahmenliste, G35")
t_m = ersetze(t_m, G37_ENDE, G37_NEU, "Maßnahmenliste, G37")
t_m = ersetze(t_m, H13_ENDE, H13_NEU, "Maßnahmenliste, H13")
t_m = ersetze(t_m, TASK11_ALT, TASK11_NEU, "Maßnahmenliste, Taskzeile 11 (Spalte Task)")
t_m = ersetze(t_m, TASK11B_ALT, TASK11B_NEU, "Maßnahmenliste, Taskzeile 11 (Spalte Punkte)")
t_m = ersetze(t_m, SUMME_ALT, SUMME_NEU, "Maßnahmenliste, Summe")

t_t = ersetze(t_t, KOPF_ALT, KOPF_NEU, "Textvorschlag 5, Kopf")
a = t_t.find(P1_START)
e = t_t.find(P2_ENDE)
if a < 0 or e < 0 or t_t.count(P1_START) != 1 or t_t.count(P2_ENDE) != 1 or t_t.count(P2_START) != 1 or t_t.count(P1_ENDE) != 1:
    raise SystemExit("ABBRUCH: Absätze in Textvorschlag 5 § 11 nicht eindeutig gefunden")
if not (a < t_t.find(P1_ENDE) < t_t.find(P2_START) < e):
    raise SystemExit("ABBRUCH: Reihenfolge der Absätze in § 11 anders als erwartet")
e = e + len(P2_ENDE)
t_t = t_t[:a] + P_NEU + t_t[e:]
log.append("  Textvorschlag 5, § 11: zwei Absätze ersetzt")

os.makedirs(AUS, exist_ok=True)
neu_n = t_n.encode("utf-8")
neu_m = t_m.encode("utf-8")
neu_t = t_t.encode("utf-8")
open(os.path.join(AUS, "Cowork_Sitzungsnotizen.md"), "wb").write(neu_n)
open(os.path.join(AUS, "Massnahmenliste_Datenverarbeitung.md"), "wb").write(neu_m)
open(os.path.join(AUS, "Textvorschlag_5_2026-09-30.md"), "wb").write(neu_t)
zeilen = ["Steuerung_Rev146_2026-10-02.py, Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Sitzungsuhr)"] + log + [
    "Cowork_Sitzungsnotizen.md: vorher " + str(len(roh_n)) + " B MD5 " + md5(roh_n) + ", nachher " + str(len(neu_n)) + " B MD5 " + md5(neu_n),
    "Massnahmenliste_Datenverarbeitung.md: vorher " + str(len(roh_m)) + " B MD5 " + md5(roh_m) + ", nachher " + str(len(neu_m)) + " B MD5 " + md5(neu_m),
    "Textvorschlag_5_2026-09-30.md: vorher " + str(len(roh_t)) + " B MD5 " + md5(roh_t) + ", nachher " + str(len(neu_t)) + " B MD5 " + md5(neu_t),
    "Semikola im neuen Text: 0"]
open(os.path.splitext(os.path.abspath(__file__))[0] + ".txt", "w", encoding="utf-8", newline="\n").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))

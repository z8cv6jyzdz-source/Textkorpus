# -*- coding: utf-8 -*-
"""
Steuerung_Rev145_2026-10-02.py

Zweck:    Schreibt Rev. 145 als Nachtrag in Teil 0 der Sitzungsnotizen und ergänzt die Maßnahmenliste (Stand, G38, Summe).
          Frage des Verfassers nach Rev. 144: Sind neue Grafiken nötig, welche Grafik zeigt die ANCOVA? Befund: keine neue
          Grafik, Abb. 2 trägt die ANCOVA, veraltete Kopien in 06_Abbildungen für Task 18 vorgemerkt.
Eingang:  Cowork_Sitzungsnotizen.md und Massnahmenliste_Datenverarbeitung.md (Stand Rev. 144, Ordner)
Aufruf:   python Steuerung_Rev145_2026-10-02.py <Notizen.md> <Massnahmenliste.md> <Ausgabeordner>
Ausgabe:  beide Dateien im Ausgabeordner (frischer Pfad für die Rückschreibung), Laufprotokoll .txt neben dem Skript
Fassung:  2026-10-02, erste Fassung (Claude Code)
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSN, AUS = sys.argv[1:4]
ZEIT = datetime.datetime.now().strftime("%H:%M")
md5 = lambda b: hashlib.md5(b).hexdigest()
MD5_N_SOLL = "a85e4013440970ce35bb01a78dcc84d5"   # Stand nach Rev. 144 (Steuerung_Rev144_2026-10-02.txt)
MD5_M_SOLL = "288f4dfa5d6828c33bd077add7040449"

BLOCK = """### ⭐ NACHTRAG (Rev. 145, 02.10.2026, {ZEIT} Sitzungsuhr, Frage des Verfassers im Chat nach Rev. 144): Abbildungen der Ergebnisse geprüft — keine neue Grafik nötig, Abb. 2 trägt die ANCOVA, veraltete Kopien in `06_Abbildungen` für Task 18 vorgemerkt

**Frage (Verfasser, 02.10.):** Ob auf Basis der vorhandenen Ergebnisse neue Grafiken nötig sind, welche Grafik die gerechnete ANCOVA, also den Vorher-Nachher-Vergleich der Zielgrößen, zeigt und ob dafür eine Grafik fehlt.

**Befund (nach F17 § 5.3, § 11.2, § 11.2b und § 11.6, geprüft an `03_Skripte\\Objekte_2026-10-01` und `03_Skripte\\Anhang_G_2026-10-01`):** Alle festgelegten Abbildungen sind aus der Ergebnisdatei erzeugt: Abb. 1 Teilnehmerfluss (5.1), Abb. 2 Ausgangswerte und reifeadjustierte Abschlusswerte (5.2), Abb. H1 Zeitstrahl der Testtermine, Abb. G1 bis G6 Q-Q- und Linearitätsdiagramme (Voraussetzungen der ANCOVA). Die ANCOVA zeigt Abb. 2 (`Abb_2_Modell.png`, Stand 01.10.): je konfirmatorischer Zielgröße ein Feld, x Ausgangswert, y auf das mittlere %PAH adjustierter Abschlusswert, ein Punkt je Spieler, Modelllinien je Gruppe, Gruppenmittel als Quadrate (nach Vickers und Altman, 2001). Der senkrechte Abstand der Linien ist die adjustierte Differenz, der waagerechte Abstand der Gruppenmittel der Ausgangsvorsprung. Die Zahlen trägt Tab. 3, die Bestwerte bei Eingangs- und Abschlusstestung je Gruppe Tab. H3b im Anhang. Ein zusätzliches Prä-Post-Mitteldiagramm ist nicht vorgesehen: Die Objekte stehen unabhängig vom Ergebnis fest (R7), ein Objekt kommt nur dazu, wenn kein anderes dieselbe Information trägt, es legte den ausgeschlossenen Schluss „die IG verbesserte sich stärker“ nach Rohwerten nahe (§ 11.2b), und über die fünf Objekte des Textteils hinaus gilt die Tauschregel. Ein Diagramm der adjustierten Differenzen mit KI gegen null und SESOI wäre höchstens im Anhang denkbar, dieselbe Information trägt Tab. 3, nicht empfohlen.

**Entscheidung (Verfasser, 02.10., „ok“ im Chat):** keine neue Grafik, Hinweis auf die veralteten Kopien in die Maßnahmenliste.

**Veraltete Kopien in `06_Abbildungen`:** `Abb_2_Modell.png` ist dort die Fassung vom 25.09. (MD5 aa01c89a…, 198.663 B), maßgeblich ist die nach dvs geprüfte Fassung vom 01.10. in `03_Skripte\\Objekte_2026-10-01` (MD5 9b0effc2…, 39.495 B). `Abb_H7_Zeitstrahl` trägt noch den alten Namen (Abb. H1 seit Klick vom 01.10.). Der Unterordner `Anhang_G` enthält die Diagramme der Kette (`S14_*.png`, mit Transfer-Chunk caBX), nicht Abb. G1 bis G6 aus `Anhang_G_Diagramme_2026-10-01.R`. `README_Abbildungen.md` nennt noch den Erzeuger `Objekte_2026-09-25.R`, `README_Ordnerstruktur.md` noch Abb. H7. Vorgemerkt in G38 (d) für Task 18, nichts geändert.

**Stand der Dateien:** Geändert: diese Notizen (Rev. 145 auf Rev. 144) und die Maßnahmenliste (Stand, G38, Summe), nur im Ordner, die Projektkopien erreicht diese Sitzung nicht. Neu: `03_Skripte\\Steuerung_Rev145_2026-10-02.py` mit `.txt`. Unverändert: Objekte, Anhang G, `06_Abbildungen`, Master, Kennzahlenblatt, Fassung 17.

**Nächster Schritt:** unverändert wie Rev. 144: Abgleich von Kapitel 5 nach der Übertragung als Schritt 0 von Task 12a, dann Task 12a.

"""
BLOCK = BLOCK.replace("{ZEIT}", ZEIT)

STAND_N_ALT = "**Stand: (Rev. 144 — siehe Block oben.)"
STAND_N_NEU = "**Stand: (Rev. 145 — siehe Block oben.) Zuvor: (Rev. 144 — siehe Block oben.)"
ANKER = "### ⭐⭐ NEU (Rev. 144,"

STAND_M_ALT = "**Stand 02.10.2026, 11:47 Sitzungsuhr (Rev. 144 — "
STAND_M_NEU = ("**Stand 02.10.2026, " + ZEIT + " Sitzungsuhr (Rev. 145 — Abbildungen der Ergebnisse geprüft: keine neue Grafik, "
               "Abb. 2 trägt die ANCOVA, veraltete Kopien in `06_Abbildungen` in G38 (d) vorgemerkt). "
               "Zuvor 02.10.2026, 11:47 Sitzungsuhr (Rev. 144 — ")
G38_ENDE = "(f) Abgabeprüfung: CONSORT 15 als „Tab. 2 mit 4.2“."
G38_NEU = G38_ENDE + (" *(Rev. 145, 02.10.: zu (d) konkret: In `06_Abbildungen` liegt `Abb_2_Modell.png` in der Fassung vom 25.09. "
                      "(aa01c89a…), maßgeblich ist `03_Skripte\\Objekte_2026-10-01\\Abb_2_Modell.png` (01.10., 9b0effc2…). "
                      "`Abb_H7_Zeitstrahl` umbenennen in Abb. H1, im Unterordner `Anhang_G` die Kettendiagramme `S14_*.png` "
                      "(mit caBX) durch Abb. G1 bis G6 aus `03_Skripte\\Anhang_G_2026-10-01` ersetzen, `README_Abbildungen.md` "
                      "(Erzeuger 25.09.) und `README_Ordnerstruktur.md` (Abb. H7) nachziehen. In Task 18 Objekte nur aus "
                      "`Objekte_2026-10-01` und `Anhang_G_2026-10-01` einsetzen. Verfasser 02.10.: keine neue Grafik, Abb. 2 trägt "
                      "die ANCOVA, Tab. 3 die Zahlen, Tab. H3b die Rohwerte.)*")
SUMME_ALT = "| **Summe** | Rev. 144 (02.10.):"
SUMME_NEU = "| **Summe** | Rev. 145 (02.10.): G38 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 144 (02.10.):"

log = []
def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit("ABBRUCH: " + name + " kommt " + str(n) + "-mal vor statt einmal")
    log.append("  " + name + ": ersetzt")
    return text.replace(alt, neu)

for f in (BLOCK, STAND_M_NEU, G38_NEU, SUMME_NEU):
    if chr(59) in f:   # Semikolon
        raise SystemExit("ABBRUCH: Semikolon im neuen Text")

roh_n = open(NOTIZEN, "rb").read()
roh_m = open(MASSN, "rb").read()
if md5(roh_n) != MD5_N_SOLL or md5(roh_m) != MD5_M_SOLL:
    raise SystemExit("ABBRUCH: Eingang nicht auf dem Stand nach Rev. 144 (MD5 " + md5(roh_n) + " / " + md5(roh_m) + "), Rev. neu bestimmen")
t_n = roh_n.decode("utf-8")
t_m = roh_m.decode("utf-8")
if "(Rev. 145," in t_n:
    raise SystemExit("ABBRUCH: Rev. 145 steht schon in den Notizen")
t_n = ersetze(t_n, STAND_N_ALT, STAND_N_NEU, "Notizen, Stand")
t_n = ersetze(t_n, ANKER, BLOCK + ANKER, "Notizen, Block vor Rev. 144")
t_m = ersetze(t_m, STAND_M_ALT, STAND_M_NEU, "Maßnahmenliste, Stand")
t_m = ersetze(t_m, G38_ENDE, G38_NEU, "Maßnahmenliste, G38")
t_m = ersetze(t_m, SUMME_ALT, SUMME_NEU, "Maßnahmenliste, Summe")

os.makedirs(AUS, exist_ok=True)
neu_n = t_n.encode("utf-8")
neu_m = t_m.encode("utf-8")
open(os.path.join(AUS, "Cowork_Sitzungsnotizen.md"), "wb").write(neu_n)
open(os.path.join(AUS, "Massnahmenliste_Datenverarbeitung.md"), "wb").write(neu_m)
zeilen = ["Steuerung_Rev145_2026-10-02.py, Lauf " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (Sitzungsuhr)"] + log + [
    "Cowork_Sitzungsnotizen.md: vorher " + str(len(roh_n)) + " B MD5 " + md5(roh_n) + ", nachher " + str(len(neu_n)) + " B MD5 " + md5(neu_n),
    "Massnahmenliste_Datenverarbeitung.md: vorher " + str(len(roh_m)) + " B MD5 " + md5(roh_m) + ", nachher " + str(len(neu_m)) + " B MD5 " + md5(neu_m),
    "Semikola im neuen Text: 0"]
open(os.path.splitext(os.path.abspath(__file__))[0] + ".txt", "w", encoding="utf-8", newline="\n").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))

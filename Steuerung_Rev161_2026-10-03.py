# -*- coding: utf-8 -*-
"""
Steuerung_Rev161_2026-10-03.py — Rev.-Block 161 in Teil 0 der Sitzungsnotizen (Taskwechsel des Tasks
„Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ nach Teilschritt 2 c)

Prüft, dass der oberste Block Rev. 160 ist, setzt den Block 161 davor und stellt die Stand-Zeile auf Rev. 161.
Schreibt die neue Fassung und ein Protokoll mit Größen und MD5 vorher und nachher.
Aufruf: python Steuerung_Rev161_2026-10-03.py <Notizen.md> <Ausgabe.md> <Protokoll.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import hashlib

EIN, AUS, PROT = sys.argv[1:4]
alt = open(EIN, encoding='utf-8').read()
STAND_ALT = '**Stand: (Rev. 160 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 161 — siehe Block oben.) Zuvor: (Rev. 160 — siehe Block oben.) Zuvor: '
ANKER = '### ⭐⭐ NEU (Rev. 160, 03.10.2026, 14:15 Sitzungsuhr'
assert alt.count(STAND_ALT) == 1, 'Stand-Zeile nicht auf Rev. 160'
assert alt.count(ANKER) == 1, 'oberster Block ist nicht Rev. 160'
assert '(Rev. 161,' not in alt, 'Rev. 161 schon vorhanden'
pos_teil0 = alt.find('## TEIL 0')
pos_anker = alt.find(ANKER)
assert 0 < pos_teil0 < pos_anker, 'Rev. 160 steht nicht unter Teil 0'
erster_block = alt.find('### ⭐⭐ NEU (Rev.', pos_teil0)
assert erster_block == pos_anker, 'Rev. 160 ist nicht der erste Block unter Teil 0'

BLOCK = '''### ⭐⭐ NEU (Rev. 161, 03.10.2026, 15:00 Sitzungsuhr, Auftrag 03.10., 11:45 mit dem Startprompt aus Fortsetzungsübergabe 2 § 0): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Teilschritt 2 (c) abgeschlossen und gesichert, Taskwechsel nach erneuter automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Teilschritt 2 (d), kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung2_2026-10-03.md` § 0: Teilschritt 2 (c), die Textbausteine des Befunds § 5.1 und die Formulierungssequenzen § 5.2 Satz für Satz an Kapitel 5 prüfen, je Satz Korpusmuster (linke Spalte, gezählt nach der Zählregel § 6.5) und Projektregel (rechte Spalte) getrennt, dazu jede Funktion ohne Muster, als Teiltabelle 2c per Skript und als § 3.3 des Abgleichbefunds, mit den Punkten aus Fortsetzung 2 § 5 Nr. 4. Danach 2 (d) und 2 (e), dann Schritt 3. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.

**Ergebnis:** (1) **Teilschritt 2 (c)** (gesichert 14:45): `bausteine_2c.py` (Fassung 2) prüft die 29 Sätze gegen die 19 Bausteine von Befund § 5.1 (Kernhäufigkeiten an `textbausteine.json` und an der Anlage nachgezählt) und die sechs Absätze gegen die sechs Sequenzen von § 5.2, je Zeile Korpusmuster und Projektregel getrennt, dazu die Funktionen ohne Kernmuster. Handurteile sind per Prüfbedingung an Anlage, Codes und Zählungen gebunden, 158 Zitate am genannten Ort an Wortgrenzen gefunden, Lauf im Spiegel, aus dem gestagten Claude-Ordner und aus der gestagten Ordnerfassung bytegleich. Teiltabelle 2c (Abgleichbefund § 3.3, 48 Zeilen): Korpus wie Muster 8, abgewandelt 19, nur erweitert 18, kein Muster 3 · Fundstelle erfüllt 35, teilweise 8, bewusst anders 3, keine Regel 2, nicht erfüllt 0. 17 von 29 Sätzen mit 297 von 450 Wörtern nutzen einen Kernbaustein. Für Schritt 3 vorgemerkt: A2 S4 mit der Zuordnung über die Folge · der Fall C1 einmal für alle drei Zielgrößen (Vorbild für den Fall je Vergleich in der Klammer: Klusemann 3.3) · Blockanfänge mit einem Quantor über drei Zielgrößen · die unadjustierte Differenz vor dem Modellergebnis · Schluss mit dem Z1-Satz. Kein Potenzial: die Ort-Form der Objektsätze und die Folge in A6. (2) **Zweitprüfung** der ersten Fassung (47 Zeilen) durch einen unabhängigen Subagenten: A 2 · B 11 · C 15, alle eingearbeitet, seine Reproduktion bytegleich. A-Befunde: Der Fall C1 hat ein erweitertes Vorbild (Klusemann, Schätzer mit 90-%-Grenzen und dem Urteil „unclear“), A5 S7 und S8 stehen auf „nur erweitert“, die Schlusslogik ist in den Fall (2c.41) und die Entscheidung (2c.42) geteilt. Ob „unclear“ bei Klusemann et al. (2012) und „substantial“ bei Beato et al. (2018) ein Intervall gegen Relevanzschwellen bezeichnen, prüft 2 (d) am Volltext. Die Folge in A6 hat Kernvorbilder (Beato 4.1 → 4.2, Negra 2019 2.6, 2.7 → 2.8), ein Potenzial „A6 umstellen“ entfällt. (3) **Fortsetzungsübergabe 3** mit neuem Startprompt (§ 0), den Dateien (§ 1.3), den offenen Klicks (§ 3), dem ersten Arbeitsgang von 2 (d) (§ 4) und den Punkten für 2 (d) bis Schritt 3 (§ 5 Nr. 4).

**Eigene Korrekturen in dieser Sitzung:** (1) Die Prüfbedingung „Analysezahl mit Zahl“ traf Sammoud 1.1 über „85%“, ersetzt durch „n =“ in O1-Sätzen. (2) „Nullbefund mit Intervall“ traf „trivial“ bei Beato 4.1 (Wahrscheinlichkeiten), ersetzt über die Familie `B_NULL` mit `msd`. (3) Vier angeführte Wendungen ohne Quelle umformuliert. (4) „planmäßig“ hat nicht die Funktion der Formel „wie zugeteilt“, A1 S1 deshalb abgewandelt. (5) Die Objektformen der Erweiterung sind gleich verteilt (je 5 Sätze in 3 Studien), nicht „Ort häufiger“. (6) Kein Satz der Anlage legt den Messfehler gegen eine SWC, Rogers 1.1 ist ein Ausgangsunterschied.

**Stand der Dateien:** Neu: in `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` die Dateien `bausteine_2c.py` (108.654 Byte, MD5 `a4407b53…`), `bausteine_2c.txt`, `teiltabelle_2c.csv`, `teiltabelle_2c.md`, `zweitpruefung_2c.md` und `zweitpruefung_2c_nachrechnung.py` mit `.txt`, der Ordner hat jetzt 42 Dateien · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung3_2026-10-03.md` (16.523 Byte, MD5 `920b193f…`) mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev161_2026-10-03.py` mit `.txt` · Projektkopie `claude/Uebergabe_Abgleich_Ergebnisse_Fortsetzung3_2026-10-03.md` (Projektspeicher 1.972.019 Byte vor der Ablage, danach rechnerisch 1.988.542 von 2.000.000). Geändert: `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (158.289 Byte, MD5 `5f5ef327…`, § 0, § 3.3 neu, § 3.4 und 3.5 folgen in 2 d und 2 e, § 5), der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung · `LIESMICH.md` des Arbeitsordners (Abschnitt Schritt 2 c, 7.958 Byte) · diese Notizen (Rev. 161 auf Rev. 160), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Von diesem Task nicht geändert: Master (40.331 Byte, Dateizeit 02.10., 19:18), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung3_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 160 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ (Rev. 160, Nachtrag zum Textvorschlag 6.1 mit Klickfreigabe je Absatz, die Datei des Nachtrags liegt seit 14:36 im Ordner), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 3 ab Teilschritt 2 (d): jede Korpusaussage, auf die sich ein Potenzial stützen soll, mit einem eigenen Skript `nachzaehlung_2d.py` an der Anlage `…_Saetze.csv` unabhängig nachzählen (Teiltabelle 2d, Abgleichbefund § 3.4), dazu die qualitative Inferenz bei Klusemann et al. (2012) und Beato et al. (2018) am Volltext, dann 2 (e) Anschluss an Kapitel 4, 6.1 und weitere Teile aus Befund § 1.4, danach Schritt 3 mit der Klickfrage zu den Potenzialen.

'''
neu = alt.replace(STAND_ALT, STAND_NEU, 1)
pos = neu.find(ANKER)
neu = neu[:pos] + BLOCK + neu[pos:]
assert chr(59) not in BLOCK, 'Semikolon im Block'
open(AUS, 'w', encoding='utf-8', newline='').write(neu)


def md5(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()


z = ['Steuerung Rev. 161 (03.10.2026)',
     'vorher: ' + str(len(alt.encode('utf-8'))) + ' Byte, MD5 ' + md5(alt),
     'nachher: ' + str(len(neu.encode('utf-8'))) + ' Byte, MD5 ' + md5(neu),
     'Block: ' + str(len(BLOCK.encode('utf-8'))) + ' Byte, eingesetzt vor Rev. 160, Stand-Zeile auf Rev. 161',
     'Prüfungen: Stand-Zeile auf Rev. 160, oberster Block Rev. 160, Rev. 161 nicht vorhanden, kein Semikolon im Block']
open(PROT, 'w', encoding='utf-8').write('\n'.join(z) + '\n')
print('\n'.join(z))

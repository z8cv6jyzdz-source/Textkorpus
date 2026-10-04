# -*- coding: utf-8 -*-
"""Steuerung Rev. 152 (02.10.2026, Task 12a, Abschluss): Variante A übernommen, 6.1 freigegeben und in den Master eingebaut.

Liest die beiden Steuerdokumente aus dem Quellordner (frisch gestagter Ordnerstand, Rev. 151), prüft die Anker,
setzt den Eintrag Rev. 152 an den Kopf von Teil 0, schreibt die Stand-Zeilen fort, ergänzt in der Maßnahmenliste
die Taskzeile 12, die Vermerke H16 und G35 und die Summe. Jeder Anker muss genau einmal vorkommen, sonst bricht das
Skript ab. Ausgabe in den Zielordner mit Protokoll (Zeilen, Bytes, MD5 vorher und nachher). Ohne Semikolon im Skript (chr(59)).

Aufruf: python3 Steuerung_Rev152_2026-10-02.py <Quellordner> <Zielordner>
"""
import hashlib
import os
import sys

SEMI = chr(59)
NOTIZEN = 'Cowork_Sitzungsnotizen.md'
MASSNAHMEN = 'Massnahmenliste_Datenverarbeitung.md'

EINTRAG_152 = """### ⭐⭐ NEU (Rev. 152, 02.10.2026, 19:36 Sitzungsuhr, Auftrag 18:38 mit dem Startsatz aus Rev. 151, Klicks des Verfassers): Task 12a abgeschlossen — Variante A in den Textvorschlag 6.1 übernommen, alle sechs Absätze per Klick freigegeben, PDF der Version of Record abgelegt, 6.1 per Skript in den Master eingebaut und geprüft

**Auftrag:** „Weiter mit Task 12a: Freigabe und Einbau 6.1 nach `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` § 8 und § 11.2 und dem Nachtrag `04_Uebergaben\\Textvorschlag_6.1_Nachtrag_K2_2026-10-02.md` § 8.1 (Variante A, per Klick gewählt). Zuerst Teil 0, mindestens Rev. 151. Die PDF der Version of Record muss vor dem Einbau in `Ideen und Studien` liegen. Bitte prüfe, ob wir in diesem Task weitermachen sollen oder einen neuen aufgrund des Kontextfensters starten sollen.“ Entscheidung: im Task weitergearbeitet (alle Stände auf der Platte, jeder Schritt per Skript mit MD5-Prüfung, Übergabe aus Teil 0 und Textvorschlag § 11.2 jederzeit möglich), dem Verfasser so gemeldet. Die Sitzung lief nach Rev. 150 weiter, der Kontext wurde einmal verdichtet, ohne Verlust am Stand der Dateien.

**Ergebnis:** (1) **Variante A übernommen** (Nachtrag § 8.1 Nr. 1): `03_Skripte\\Textvorschlag_6.1_2026-10-02.py` Fassung 2 (MD5 `c7ee7f79…`), A2 S3 Vergleichssatz zu Boumparis et al. (2026), A2 S4 „Der Schätzer ist durch die eigene Umsetzung stark verdünnt“, A3 ohne den Satz zu Liu et al. (2024), kein Modul mehr. Wortlaut zeichengleich mit `Textvorschlag_6.1_Nachtrag_K2_2026-10-02.json` (geprüft). Messung: 6.1 700 Wörter (A1 99 · A2 116 · A3 131 · A4 133 · A5 153 · A6 68), 40 Sätze, Median 16,0, längster 31, 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, 14 Belegklammern, neun Quellen, Prüfskript ohne Befund (`.txt` MD5 `8a0d0ffd…`, `.json` MD5 `627f6b15…`). (2) **Textvorschlag 6.1 nachgeführt** (Nachtrag § 8.1 Nr. 2 bis 4): § 0 bis § 11 auf Variante A, Belegtabelle mit der Zeile Boumparis (Fundstellen nach Nachtrag § 4, Seitenzahlen nach der PDF), Liu als „nicht im Text, nach 6.2/6.3 G8“, Klusemann unter „Gelesen, nicht im Text“, Kürzungsleiter Stufe 1 verbraucht, § 9.4 mit dem Literaturverzeichnis-Eintrag Boumparis (2026, zwölf Autorinnen und Autoren), drei Berichtigungen (Klusemann 77 % für alle 13 der Videogruppe, Obergrenze der Einleitung 1.200 statt 1.500, T1 `Liu2024` Distanz als Vormerkung). `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` 98.346 Byte, MD5 `c3de94d3…`, Erzeuger `03_Skripte\\tv61_md.py` Fassung 2 (MD5 `6ee0a458…`), Projektkopie `claude/`. (3) **Klicks des Verfassers** (nach 19:10 Sitzungsuhr): Freigabe des Wortlauts „Alle sechs Absätze freigeben“ (K6) · zur Frage nach dem Einbau „Pdf ist jetzt im Ordner“. (4) **PDF der Version of Record** in `Ideen und Studien`: „2026 Boumparis et al., Factors Influencing Adherence to Digital Lifestyle Interventions for Adolescents Systematic Review and Meta-Analysis of Attrition.pdf“, 503.950 Byte, MD5 `7b0c5660…`, 24 Seiten, am Text geprüft: Titel, 116 Studien, DOI 10.2196/84822, Interact J Med Res 2026, 15, e84822. Seitenzahlen der Fundstellen: Abstract › Conclusions S. 1 · Eligibility Criteria und Identification of Studies S. 3 · Characteristics of Digital Interventions S. 6 (55,2 %, SD 25,5 %, 66 Vergleiche) · Quantitative Synthesis of Attrition S. 7 bis 8 · Principal Findings S. 12 · Domain-Specific Adherence Patterns, Limitations, Implications for Future Research S. 14. Der Preprint (2025) bleibt im Ordner, nicht zitierfähig. (5) **Einbau 6.1** (19:18 Sitzungsuhr, Textvorschlag § 11.2 und § 11.3): Master frisch gestagt (MD5 `caa5dee2…`, 42.318 Byte, 182 Absätze, keine comments.xml), `03_Skripte\\Master_6_1_2026-10-02.py` aus frischem Ausgabepfad, sechs Absätze unter „6.1 Einordnung der Ergebnisse“, 182 → 188 Absätze, `validate.py` bestanden, Rückschreibung mit mtime-Prüfung, 10 s Wartezeit, neu gestagt: **Master 40.331 Byte, MD5 `2fda2144…`** gleich der Ausgabe. `Abgleich_Kapitel6_1_Master_2026-10-02.py` (Master gegen Ausgabe und JSON): ohne Befund, A1 bis A6 zeichengleich, 700 Wörter, Formatvorlage Standard, keine Direktformatierung, Überschriften 6 bis 7 an den Positionen 135, 136, 143, 144, 145, 6.2 und 6.3 leer (Protokolle `03_Skripte\\Master_6_1_2026-10-02.txt`, `Abgleich_Kapitel6_1_Master_2026-10-02.txt`). (6) **Messskript Fassung 4** (`03_Skripte\\Manuskriptstand_2026-09-25.txt` und `.csv`): 6.1 700 gegen 700, Kapitel 6 700 gegen 1.600, Absatztext Kapitel 1 bis 7 4.496 gegen 6.350, ungeschrieben 6.2 (mit 6.3, Budget 900) und 7 (250), 0 Semikola, 0 Abschnittsverweise, 7 Platzhalter (Anhang H), 47 verschiedene Autor-Jahr-Belege, Prognose 27,8 Seiten (Modellrechnung, unverändert gegenüber Rev. 146). (7) **Endabgleich Fassung 3** in `03_Skripte\\Endabgleich_2026-10-02_Kapitel6_1\\` (drei Dateien, Eingänge mit denselben SHA-256 wie im Lauf für Kapitel 5): 383 Zahlen, 26 in 6.1 (16 Zitatjahre, 7 Testnamen und Messstrecken, drei Klassifikationsartefakte „15“ in U15 und „15 bis 40 m“ sowie „90“ im 90. Perzentil, keine Ergebniszahl), Satzprüfungen 23, Abweichungen 2 wie am Vormittag (Tab. 1 bis Task 18 nicht im Master, P-09), Vorschläge 0, Zahlenliste `Endabgleich_Manuskript_2026-09-25_Zahlen.csv` bis Task 18 unverändert. (8) **T1** per `03_Skripte\\T1_Nachtrag_Einbau61_2026-10-02.py` (Protokoll `.txt`, 76 Steckbriefe, MD5 `9f9dd85b…`, nur zwei Felder geändert, alle anderen Zeilen byteidentisch): `Liu2024` Feld `kapitel` „2.3, 5.5“ → 6.2/6.3 G8 (Distanzfelder 2 · 1 · 2 unverändert, Angleichung an 1 · 1 · 0 der Belegtabelle vor 12b vorgemerkt) · `Boumparis2026` Feld `fassung` mit PDF, MD5 und Seitenzahlen (H16 für diese Quelle erledigt). ⚠ `T1_T4_Nachtrag_Boumparis_2026-10-02.py` setzt bei einem erneuten Lauf das Feld `fassung` auf seinen eigenen Stand zurück, es darf ohne Nachführung seiner T1-Zeile nicht erneut laufen. T4 unverändert (170).

**Eigene Korrekturen in dieser Sitzung:** (1) Beim Übertragen von Variante A fehlte in A3 S4 das Leerzeichen nach dem Zitier-Semikolon in der Klammer Oliver/Zheng, A3 maß 130 statt 131 Wörter. Vor dem Lauf gegen die Nachtrags-JSON erkannt und berichtigt, danach zeichengleich. (2) Ein Commit mit falsch angegebenem Ausgabepfad (Zeitstempel geraten statt gelesen) wurde vollständig abgewiesen, keine Datei geschrieben, Wiederholung mit dem richtigen Pfad, alle zwölf Dateien per MD5 bestätigt.

**Stand der Dateien:** Geändert: `Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (Master, 40.331 Byte, MD5 `2fda2144…`, 6.1 mit 700 Wörtern, 6.2, 6.3 und 7 leer) · `03_Skripte\\Textvorschlag_6.1_2026-10-02.py`, `.txt`, `.json` (Fassung 2) · `03_Skripte\\tv61_md.py` · `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` (Projektkopie `claude/`) · `03_Skripte\\Manuskriptstand_2026-09-25.txt` und `.csv` · `Schreiben\\ev3_daten\\T1_steckbriefe.csv` · diese Notizen (Rev. 152 auf Rev. 151) · Maßnahmenliste (Stand, Taskzeile 12, H16, G35, Summe), je Ordner und Projektkopie. Neu: `03_Skripte\\Master_6_1_2026-10-02.txt` · `Abgleich_Kapitel6_1_Master_2026-10-02.txt` · `Endabgleich_2026-10-02_Kapitel6_1\\` (drei Dateien) · `T1_Nachtrag_Einbau61_2026-10-02.py` mit `.txt` · `Steuerung_Rev152_2026-10-02.py` mit `.txt`. Neu im Ordner durch den Verfasser: die PDF der Version of Record (oben). Unverändert: Kennzahlenblatt, Zahlenliste, T4, Fassung 17, Plan Rev. 5 mit Nachträgen, Nachtrag K2, Analysebefund. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Preprint „2025 Boumparis et al., …“ umbenennen oder in den Papierkorb (Rev. 151, nicht zitierfähig) · (2) Verzeichnisse im Master nach dem Einbau mit F9 aktualisieren (bei Gelegenheit, nicht eilig) · (3) Task 12b eröffnen.

**Nächster Schritt:** Task 12b (6.2 und 6.3, nach Gliederung v6 ein Abschnitt „Methodendiskussion, Stärken und Limitationen“ mit Budget 900) nach Plan § 3 und § 8 (Startsatz dort). Eingänge: Textvorschlag 6.1 § 9.1 (Vormerkungen Nr. 1 bis 9, darunter Liu 2024 nach G8 und die Distanzangleichung in T1), Nachtrag K2 § 3.1, § 3.2 und § 8.2 (Satzkerne Nr. 3 bis 6, Klusemann 2012 mit Dosis und Niveau in G3, Boumparis 2026 in G3 und G6 oder Stärken), Textvorschlag 4.7 § 7, Textvorschlag 5 § 9.4, Berichtsraster § 3.14 (6.2.1 bis 6.2.12) und § 3.15, F17 § 12 (G1 bis G8). Kapitel 6 ist bis auf diesen Abschnitt geschrieben.

"""

STAND_ALT_N = '**Stand: (Rev. 151 — siehe Block oben.) Zuvor: '
STAND_NEU_N = '**Stand: (Rev. 152 — siehe Block oben.) Zuvor: (Rev. 151 — siehe Block oben.) Zuvor: '
ANKER_151 = '### ⭐⭐ NEU (Rev. 151, 02.10.2026, 18:17 Sitzungsuhr, Auftrag mit dem Startsatz aus Plan § 8, Klicks des Verfassers):'

STAND_ALT_M = '**Stand 02.10.2026, 18:17 Sitzungsuhr (Rev. 151 — '
STAND_NEU_M = ('**Stand 02.10.2026, 19:36 Sitzungsuhr (Rev. 152 — Task 12a abgeschlossen: Variante A in den Textvorschlag 6.1 übernommen, '
               'alle sechs Absätze per Klick freigegeben, PDF der Version of Record von Boumparis et al. (2026) im Ordner, 6.1 per Skript in den '
               'Master eingebaut (MD5 `2fda2144…`, 700 Wörter, Abgleich ohne Befund, Messskript 4.496 gegen 6.350, Prognose 27,8 Seiten, Endabgleich '
               'ohne neuen Befund), T1 `Liu2024` und `Boumparis2026` nachgeführt, Taskzeile 12, H16 und G35 fortgeschrieben). '
               'Zuvor 02.10.2026, 18:17 Sitzungsuhr (Rev. 151 — ')

TASK12_ANKER = ('Satzkerne Nr. 3 bis 6 und Liu 2024 nach G8 nach § 8.2 (12b), PDF der Version of Record vor dem Einbau |')
TASK12_NEU = ('Satzkerne Nr. 3 bis 6 und Liu 2024 nach G8 nach § 8.2 (12b), PDF der Version of Record vor dem Einbau · '
              '**12a erledigt (Rev. 152, 02.10.):** Variante A übernommen (Textvorschlag 6.1 Fassung 2, 700 Wörter), alle sechs Absätze per Klick '
              'freigegeben, PDF der Version of Record im Ordner, 6.1 per `Master_6_1_2026-10-02.py` eingebaut (Master MD5 `2fda2144…`, 188 Absätze), '
              'Abgleich ohne Befund, Messskript und Endabgleich (`Endabgleich_2026-10-02_Kapitel6_1\\`) ohne neuen Befund, T1 nachgeführt. '
              'Offen für 12b: Textvorschlag 6.1 § 9.1 und Nachtrag K2 § 8.2 |')

H16_ANKER = ('Seitenzahlen der Fundstellen nachtragen (Nachtrag K2 § 8.1 Nr. 5). Priorität 2 und 3 unverändert.)*')
H16_NEU = ('Seitenzahlen der Fundstellen nachtragen (Nachtrag K2 § 8.1 Nr. 5). Priorität 2 und 3 unverändert.)* '
           '*(Rev. 152, 02.10.: Für Boumparis 2026 erledigt: PDF der Version of Record seit 02.10. abends in „Ideen und Studien“ '
           '(503.950 Byte, MD5 `7b0c5660…`, 24 Seiten), Titel, 116 Studien und DOI am Text geprüft, Seitenzahlen der Fundstellen in Textvorschlag 6.1 § 5 '
           'und T1 `Boumparis2026` Feld `fassung`. Der Preprint bleibt im Ordner (Umbenennen oder Papierkorb beim Verfasser). '
           'Der Posten bleibt für die Prioritäten 2 und 3 offen.)*')

G35_ANKER = ('(17 Wörter, Rasterzeile 2.1, Nachtrag K2 § 3.4 und § 8.4). Kein Satz zur Umsetzung in der Lücke (Absatz 5).)*')
G35_NEU = ('(17 Wörter, Rasterzeile 2.1, Nachtrag K2 § 3.4 und § 8.4). Kein Satz zur Umsetzung in der Lücke (Absatz 5).)* '
           '*(Rev. 152, 02.10.: Textvorschlag 6.1 § 9.3 nachgeführt: Liu 2024 ist seit Variante A keine Vorstudie von 6.1 mehr und kommt nur über 12b '
           '(6.2/6.3 G8) in die Arbeit, die Obergrenze der Einleitung steht dort berichtigt mit 1.200 statt 1.500, der Gegenbefund in Absatz 3 als § 9.3 Nr. 5. '
           '6.1 steht im Master, der Ankersatz A1 S1 ist damit im Master zweimal vorhanden (Einleitung mit „deshalb“, 6.1 ohne).)*')

SUMME_ANKER = '| **Summe** | Rev. 151 (02.10.): '
SUMME_NEU = ('| **Summe** | Rev. 152 (02.10.): Taskzeile 12 (12a erledigt), H16 und G35 Vermerke, keine neuen Punkte, Zählung nicht neu erhoben. '
             'Zuvor: Rev. 151 (02.10.): ')


def md5(pfad):
    return hashlib.md5(open(pfad, 'rb').read()).hexdigest()


def lese(pfad):
    with open(pfad, encoding='utf-8', newline='') as f:
        return f.read()


def schreibe(pfad, text):
    with open(pfad, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Anker „%s“ kommt %d-mal vor, erwartet 1' % (name, n))
    protokoll.append('  %s: Anker gefunden (1x), ersetzt' % name)
    return text.replace(alt, neu)


def main():
    quelle, ziel = sys.argv[1], sys.argv[2]
    os.makedirs(ziel, exist_ok=True)
    for s in (EINTRAG_152, STAND_NEU_M, TASK12_NEU, H16_NEU, G35_NEU, SUMME_NEU):
        assert SEMI not in s, 'Semikolon im Einfügetext'
    protokoll = ['Steuerung Rev. 152 (02.10.2026, Task 12a, Abschluss) — Protokoll']
    qn = os.path.join(quelle, NOTIZEN)
    t = lese(qn)
    zeilenende = '\r\n' if '\r\n' in t else '\n'
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s, Zeilenende %s' % (NOTIZEN, len(t.encode('utf-8')), t.count('\n'), md5(qn), repr(zeilenende)))
    t = ersetze(t, STAND_ALT_N, STAND_NEU_N, 'Stand-Zeile Notizen', protokoll)
    eintrag = EINTRAG_152.replace('\n', zeilenende) if zeilenende != '\n' else EINTRAG_152
    t = ersetze(t, ANKER_151, eintrag + ANKER_151, 'Eintrag Rev. 152 vor Rev. 151', protokoll)
    zn = os.path.join(ziel, NOTIZEN)
    schreibe(zn, t)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (NOTIZEN, os.path.getsize(zn), t.count('\n'), md5(zn)))
    qm = os.path.join(quelle, MASSNAHMEN)
    m = lese(qm)
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, len(m.encode('utf-8')), m.count('\n'), md5(qm)))
    m = ersetze(m, STAND_ALT_M, STAND_NEU_M, 'Stand-Zeile Maßnahmenliste', protokoll)
    m = ersetze(m, TASK12_ANKER, TASK12_NEU, 'Taskzeile 12', protokoll)
    m = ersetze(m, H16_ANKER, H16_NEU, 'H16', protokoll)
    m = ersetze(m, G35_ANKER, G35_NEU, 'G35', protokoll)
    m = ersetze(m, SUMME_ANKER, SUMME_NEU, 'Summe', protokoll)
    zm = os.path.join(ziel, MASSNAHMEN)
    schreibe(zm, m)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, os.path.getsize(zm), m.count('\n'), md5(zm)))
    for n in (NOTIZEN, MASSNAHMEN):
        r = lese(os.path.join(ziel, n))
        protokoll.append('%s rückgelesen: Rev. 152 %s' % (n, 'enthalten' if 'Rev. 152' in r else 'FEHLT'))
    with open(os.path.join(ziel, 'Steuerung_Rev152_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

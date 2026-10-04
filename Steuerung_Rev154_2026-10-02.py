# -*- coding: utf-8 -*-
"""
Steuerung_Rev154_2026-10-02.py — Teil 0 der Sitzungsnotizen (Rev. 154) und Maßnahmenliste nach dem Task
„Argumentationsstruktur der Ergebnisteile“ (Auftrag des Verfassers 02.10.2026, Klick „Ergebnisse“).
Bachelorarbeit U15-Plyometrie · Arbeitsdokument.

Aufruf: python Steuerung_Rev154_2026-10-02.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Ausgabeordner>
Liest die frisch gestagten Fassungen, schreibt die fortgeschriebenen Fassungen in den Ausgabeordner und ein Protokoll
(Steuerung_Rev154_2026-10-02.txt) mit Größen und MD5. Jede Ersetzung muss genau einmal greifen, sonst Abbruch.
Die Uhrzeit ist die Sitzungsuhr (UTC+1), aus der UTC-Zeit des Arbeitsrechners berechnet.
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSNAHMEN, AUS = sys.argv[1], sys.argv[2], sys.argv[3]
ZEIT = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).strftime('%H:%M')
LOG = []

def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit(f'Abbruch: {name} trifft {n}-mal')
    LOG.append(f'ersetzt: {name}')
    return text.replace(alt, neu)

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

# ---------------------------------------------------------------- Sitzungsnotizen, Teil 0
s = open(NOTIZEN, encoding='utf-8', newline='').read()
if '(Rev. 154' in s:
    raise SystemExit('Abbruch: Rev. 154 steht schon in den Notizen, nächste freie Nummer prüfen')
if '### ⭐⭐ NEU (Rev. 153, 02.10.2026, 23:18 Sitzungsuhr' not in s:
    raise SystemExit('Abbruch: der oberste Block ist nicht Rev. 153')

BLOCK = f"""### ⭐⭐ NEU (Rev. 154, 02.10.2026, {ZEIT} Sitzungsuhr, Auftrag 02.10. abends mit Klick „Ergebnisse“): Task „Argumentationsstruktur der Ergebnisteile“ — 16 Ergebnisteile satzweise codiert und per Skript ausgewertet, Befund mit Bauregeln, Projektregeln und Prüfkatalog für Kapitel 5, Zweitprüfung und Nachprüfung durch unabhängige Subagenten eingearbeitet, Übergabe mit Startprompt für den Abgleich von Kapitel 5, kein Manuskripttext

**Auftrag:** „Für Methodik und Einleitung wurde Dateien erstellt, mit denen der Textkorpus des Kapitels standardisiert wurde. Führe die gleiche systematische Analyse für den Ergebnisteil durch. Prüfe vergleichbare Studien aus unserem Ordner. Prüfe diese Studien auf Umfang, die Struktur des Textabschnitts. Argumentationsstrang/roter Faden. Welche RElevanz nimmt das ein und in welchem Umfang wird das durchgeführt. Prüfe zudem die Formulierungsequenzen also welche Textbausteine genutzt werden für die Argumentationsstruktur. Erstelle zunächst ein Dokument, welches in einem neuen Task auf den Diskussionsteil angewandt wird. Erstelle zudem ein Prompt für den neuen Task“. Rückfrage per Klick (Ergebnisteil oder Diskussionsteil), Antwort „Ergebnisse“: Analysiert werden die Ergebnisteile, der neue Task gleicht Kapitel 5 ab, das seit Rev. 146 im Master steht.

**Ergebnis:** (1) **Korpus:** die zehn randomisierten Kernstudien wie in den Befunden zu Einleitung und Diskussion (108 Sätze), dazu Hilska et al. (2021), die drei Studien mit Video-, Online- oder Heimprogramm (Klusemann 2012, Veith 2021, Rogers 2020 nur mit Abschnitt 3.1) und zwei Detrainingstudien (Padrón-Cabo 2025, Asimakidis 2022), zusammen 212 Sätze aus den PDF. (2) **Codierung:** Codebuch in Fassung 1 für die Blindcodierung und in Fassung 2 nach dem Konsens, Ersteller und ein blinder Subagent, Primärcode 95,3 % (κ 0,945), im Kern 93,5 % (κ 0,922), zehn Abweichungen je Satz entschieden. (3) **Befund** `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02` (.md, .docx, .pdf, 23 Seiten A4, Anhänge quer, Anlage `…_Saetze.csv`): Ergebnisteil im Kern im Median 252,5 Wörter (115 bis 539), 5,7 % des Absatztexts · Grundfigur Rahmen → Befunde je Zielgröße → Schluss mit einem Befund- oder Objektsatz, kein Resümee, keine Entscheidung über eine Hypothese · Modellergebnis vor Vergleichen einzelner Gruppen (4 von 5) · statistischer Wert in 35 von 74 Befundsätzen, Intervall nur bei Beato, Mittelwerte mit Streuung in keinem Befundsatz · Objekte meist als Klammer am Satzende, Objektsätze im Präsens, Befunde im Präteritum, keine Belege · zehn Bauregeln K1 bis K10 mit Häufigkeit, zwölf Projektregeln P1 bis P12, Textbausteine und Sequenzen (§ 5), Prüfkatalog mit Zählregel (§ 6.5) · zehn Befunde zu Steuerdokumenten (§ 7), darunter die Satzfolge „Interaktion → Haupteffekte → Post-hoc-Vergleiche → Effektstärke“ (Bauplan § 2.3, Raster § 3.13), die nicht trägt, die Vorlagen Moran et al. (2024) und Negra et al. (2019), die nur für Objektführung und Kürze taugen, und die Statistik im Satz in F17 § 5a gegen Plan § 3 Task 11. (4) **Prüfrunden:** Zweitprüfung des Befunds (28 Befunde: 3 A, 10 B, 15 C) und der Übergabe (19: 1 A, 8 B, 10 C), danach Nachprüfung beider durch weitere Subagenten (16: 0 A, 6 B, 10 C und 16: 1 A, 5 B, 10 C), alle eingearbeitet (Befund § 8, Übergabe § 10). (5) **Reproduktion:** Kette der Anlage aus den Quell-PDF in einer frischen Kopie byte-gleich (elf Ausgabedateien). (6) **Übergabe** `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md` mit Startprompt (§ 0): Schritt 1 Textstand (Kapitel 5 gegen das JSON, Register an den Fundstellen, Sätze anderer Teile, die Kapitel 5 aufnehmen), Schritt 2 Abgleich mit Blindcodierung und Prüfkatalog, Schritt 3 Potenziale als Paare mit Kürzung im Budget 450 per Klick, Schritt 4 Überarbeitung Absatz für Absatz, dazu Entscheidungsregister (§ 4) und Taskwechsel mit Fortsetzungsübergabe (§ 8).

**Eigene Korrekturen in dieser Sitzung:** (1) Vor der Ablage gegen den parallel entstandenen Befund zur Diskussion (Rev. 153) gelesen. Dessen § 5.2 liest die Reihenfolge der Zielgrößen in den Ergebnisteilen nach der ersten Nennung im Text, der Befund zu den Ergebnisteilen hatte als Regel die erste Nennung genannt, aber die Blöcke gezählt, bei Sammoud die Folge im Satz. Die Regel ist jetzt benannt, beide Lesarten stehen mit Zahl im Befund (§ 0 Nr. 6, § 3.3, K5, § 8.2, Skript `zielgroessenfolge_text.py`), verschieden sind nur Bouafif und Negra 2019. (2) Die Fehler, die Zweitprüfung und Nachprüfung fanden, sind mit Fundstelle in Befund § 8 und Übergabe § 10 verzeichnet, darunter die gezählten Wiederaufrufe von Objekten, die Blockanfänge und die Fundstelle für Orientierungszug und Absicherung, die nur auf den Textvorschlag des geprüften Kapitels verwies.

**Stand der Dateien:** Neu: `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02.md` (78.208 Byte, MD5 `c474dbf0…`), `.docx`, `.pdf` und `_Saetze.csv` · `03_Skripte\\Argumentationsstruktur_Ergebnisteile_2026-10-02\\` (40 Dateien, davon 6 in `tools\\`, mit `LIESMICH.md` und den vier Prüfberichten) · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md` · `03_Skripte\\Steuerung_Rev154_2026-10-02.py` mit `.txt` · Projektkopie `claude/Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md`. Der Befund hat keine Projektkopie: Der Projektspeicher stand vor dieser Ablage bei 1,93 von 2,00 MB, der Befund passt nicht mehr hinein, es gilt die Ordnerfassung. Geändert: diese Notizen (Rev. 154 auf Rev. 153) · Maßnahmenliste (Stand, Taskzeile „Ergebnisse: Abgleich mit der Argumentationsstruktur“ neu, G37 (p), Summe), je Ordner und Projektkopie. Unverändert: Master (40.331 Byte, MD5 `2fda2144…`), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5. Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Abgleichtask mit dem Startprompt aus Übergabe § 0 in einem neuen Task eröffnen und in die Folge 12b → 13a → Einleitung → 13b einordnen. Er kann neben dem Task „Diskussion: Anwendung der Argumentationsstruktur“ (Rev. 153) laufen, dann gilt der Anschluss an 6.1 nach Übergabe § 5 Nr. 2 · (2) Projektspeicher: Für weitere Projektkopien müssten ältere Kopien entfernt werden, das geschieht nur auf Anweisung · (3) aus Rev. 152 und 153 weiter offen: Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master, Vormerkungen G37 (o) und jetzt (p) für den Steuerdokumente-Task.

**Nächster Schritt:** Neuer Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md` § 0: Textstand von Kapitel 5 sichern, gegen den Befund abgleichen, Potenziale per Klick freigeben lassen, dann Absatz für Absatz überarbeiten. Einbau in den Master nur auf Anweisung.

"""
s = ersetze(s, '### ⭐⭐ NEU (Rev. 153, 02.10.2026, 23:18 Sitzungsuhr', BLOCK + '### ⭐⭐ NEU (Rev. 153, 02.10.2026, 23:18 Sitzungsuhr', 'Rev.-Block vor Rev. 153')
s = ersetze(s, '**Stand: (Rev. 153 — siehe Block oben.) Zuvor:', '**Stand: (Rev. 154 — siehe Block oben.) Zuvor: (Rev. 153 — siehe Block oben.) Zuvor:', 'Stand-Zeile der Notizen')
assert ';' not in BLOCK
os.makedirs(os.path.join(AUS, '00_Steuerung'), exist_ok=True)
os.makedirs(os.path.join(AUS, '03_Skripte'), exist_ok=True)
p_n = os.path.join(AUS, '00_Steuerung', 'Cowork_Sitzungsnotizen.md')
open(p_n, 'w', encoding='utf-8', newline='').write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(MASSNAHMEN, encoding='utf-8', newline='').read()
if 'Rev. 154' in m:
    raise SystemExit('Abbruch: Rev. 154 steht schon in der Maßnahmenliste')
m = ersetze(m, '**Stand 02.10.2026, 23:18 Sitzungsuhr (Rev. 153 —',
            f'**Stand 02.10.2026, {ZEIT} Sitzungsuhr (Rev. 154 — Task „Argumentationsstruktur der Ergebnisteile“: Befund `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02` mit Anlage `03_Skripte\\Argumentationsstruktur_Ergebnisteile_2026-10-02\\` (16 Studien, 212 Sätze, blind doppelt codiert, Bauregeln, Projektregeln und Prüfkatalog für Kapitel 5), Zweitprüfung und Nachprüfung eingearbeitet, Übergabe mit Startprompt `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md`, Taskzeile „Ergebnisse: Abgleich mit der Argumentationsstruktur“ neu, G37 (p)). Zuvor 02.10.2026, 23:18 Sitzungsuhr (Rev. 153 —',
            'Stand-Zeile der Maßnahmenliste')
G37_NEU = (' *(Rev. 154, 02.10.: (p) neu aus dem Befund `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02` § 7 Nr. 10 (nach Zweitprüfung und Nachprüfung), '
           'für Fassung 18, Raster Rev. 4 und die Liste der überholten Teile: F17 § 5a Kapitel 5 mit den Bauregeln K1 bis K10 und ihren Häufigkeiten · '
           'Vorlage für den Gruppenvergleich Sammoud et al. (2024), für die adjustierte Differenz mit Intervall im Satz Veith et al. (2021), Moran et al. (2024) und Negra et al. (2019) nur für Objektführung und Kürze (Befund § 7 Nr. 7) · '
           'F17 § 5a an Plan § 3 Task 11 angleichen: im Satz Richtung, adjustierte Differenz mit KI, p und Fall, keine Teststatistik, die Folge des Orientierungszugs nach der Entscheidung zu Kapitel 5 (Befund § 7 Nr. 8) · '
           'G26i um Bauplan § 2.3 nach Befund § 7 Nr. 1 bis 6 (Satzfolge der Modellterme, Teststatistik und Größenklasse im Fließtext, Studien mit reiner Objektadressierung, Deutung, Schlusssatz, Umfangswerte mit „kürzester Sachteil“) und Bauplan § 9 (Vorlagen für den Ergebnisteil) · '
           'Raster § 3.13 Kopfblock nach Befund § 7 Nr. 1 und 7, dazu eine Zeile zur Entscheidung über H0 im Ergebnisteil (P7).)*')
anker = 'drei Studien ohne gebündelten Limitationsteil.)*'
m = ersetze(m, anker, anker + G37_NEU, 'G37 (p)')
z11 = 'Vormerkungen in Textvorschlag 5 § 9 |\n'
zneu = ('| Ergebnisse: Abgleich mit der Argumentationsstruktur (angelegt 02.10., Rev. 154, Übergabe mit Startprompt `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-02.md`, Einordnung in die Folge durch den Verfasser) | '
        'Kapitel 5 gegen den Befund `02_Befunde\\Argumentationsstruktur_Ergebnisteile_RCT_2026-10-02` abgleichen (Prüfkatalog und Zählregel § 6.5, K1 bis K10, P1 bis P12), Potenziale per Klick, Überarbeitung Absatz für Absatz im Budget 450 · '
        'Anschluss an 6.1 und an den Task „Diskussion: Anwendung der Argumentationsstruktur“ (Rev. 153) · Folgevermerke nach Übergabe § 5 Nr. 8 · G37 (p) um die Befunde des Abgleichs ergänzen |\n')
m = ersetze(m, z11, z11 + zneu, 'Taskzeile Ergebnisse')
m = ersetze(m, '| **Summe** | Rev. 153 (02.10.):', '| **Summe** | Rev. 154 (02.10.): Taskzeile „Ergebnisse: Abgleich mit der Argumentationsstruktur“ neu, G37 (p) neu als Vermerk, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 153 (02.10.):', 'Summe')
assert ';' not in G37_NEU and ';' not in zneu
p_m = os.path.join(AUS, '00_Steuerung', 'Massnahmenliste_Datenverarbeitung.md')
open(p_m, 'w', encoding='utf-8', newline='').write(m)

LOG.append(f'Zeit {ZEIT} Sitzungsuhr')
for q, p in [(NOTIZEN, p_n), (MASSNAHMEN, p_m)]:
    LOG.append(f'{os.path.basename(p)}: vorher {os.path.getsize(q)} Byte, MD5 {md5(q)} · nachher {os.path.getsize(p)} Byte, MD5 {md5(p)}')
open(os.path.join(AUS, '03_Skripte', 'Steuerung_Rev154_2026-10-02.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')
print('\n'.join(LOG))

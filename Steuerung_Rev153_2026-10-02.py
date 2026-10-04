# -*- coding: utf-8 -*-
"""
Steuerung_Rev153_2026-10-02.py — Teil 0 der Sitzungsnotizen (Rev. 153) und Maßnahmenliste nach dem Task
„Argumentationsstruktur der Diskussionen“ (Auftrag des Verfassers 02.10.2026, 19:59 Sitzungsuhr).
Bachelorarbeit U15-Plyometrie · Arbeitsdokument.

Aufruf: python Steuerung_Rev153_2026-10-02.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Ausgabeordner>
Liest die frisch gestagten Fassungen, schreibt die fortgeschriebenen Fassungen in den Ausgabeordner und ein Protokoll
(Steuerung_Rev153_2026-10-02.txt) mit Größen und MD5. Jede Ersetzung muss genau einmal greifen, sonst Abbruch.
"""
import sys, os, hashlib, datetime

NOTIZEN, MASSNAHMEN, AUS = sys.argv[1], sys.argv[2], sys.argv[3]
ZEIT = datetime.datetime.now().strftime('%H:%M')   # Sitzungsuhr (UTC+1), Uhr des Arbeitsrechners der Sitzung
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
if '(Rev. 153' in s:
    raise SystemExit('Abbruch: Rev. 153 steht schon in den Notizen, nächste freie Nummer prüfen')

BLOCK = f"""### ⭐⭐ NEU (Rev. 153, 02.10.2026, {ZEIT} Sitzungsuhr, Auftrag 19:59): Task „Argumentationsstruktur der Diskussionen“ — 16 Diskussionen satzweise codiert und per Skript ausgewertet, Befund mit Bauregeln für Kapitel 6 und 7, unabhängige Zweitprüfung mit 41 Befunden eingearbeitet, Übergabe mit Startprompt für den Anwendungstask, kein Manuskripttext

**Auftrag:** „Für Methodik und Einleitung wurde Dateien erstellt, mit denen der Textkorpus des Kapitels standardisiert wurde. Führe die gleiche systematische Analyse für den Diskussionsteil (kapitel 6) durch. Prüfe vergleichbare Studien aus unserem Ordner. Prüfe diese Studien auf Umfang, die Struktur des Textabschnitts. Argumentationsstrang/roter Faden. Prüfe außerdem welche Analyseinstrumente aufgenommen/behandelt wurden. In welchem Umfang werden die Ergebnisse auf Ergebnisse anderer Studien verglichen? Welche RElevanz nimmt das ein und in welchem Umfang wird das durchgeführt. Prüfe zudem die Formulierungsequenzen also welche Textbausteine gnutzt werden für die Argumentationsstruktur. Erstelle zunächst ein Dokument, welches in einem neuen Task auf den Diskussionsteil angewandt wird. Erstelle zudem ein Prompt für den neuen Task“

**Ergebnis:** (1) **Korpus:** die zehn randomisierten Kernstudien wie im Befund der Einleitungen, dazu Hilska et al. (2021), die drei Studien mit video-, online- oder heimbasierter Vermittlung im Ordner (Klusemann 2012, Rogers 2020, Veith 2021) und zwei Detrainingstudien (Padrón-Cabo 2025, Asimakidis 2022). Diskussionen und Schlussrubriken aus den PDF extrahiert, gegen die Textfassungen auf Vollständigkeit geprüft, 828 Sätze, 530 im Kern. (2) **Codierung:** Codebuch Fassung 1 (25 Codes in zehn Gruppen, neun Regeln), Ersteller und zwei blinde Subagenten, Primärcode im Kern 87,9 % (κ 0,87), gesamt 87,4 % (κ 0,87), 104 Abweichungen nach 18 Klarstellungen je Satz entschieden. (3) **Befund** `02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02` (.md, .docx, .pdf, 40 Seiten A4, Anhänge quer, Anlage `…_Saetze.csv`): Diskussion im Median 1.252 Wörter, Schlussrubrik 173 · Grundfigur Eröffnung → Befundteil → Limitationsblock → Schlussrubrik · Zielgrößenblock Befund → Vergleich → Erklärung · Vergleich mit anderen Studien 12,5 % der Sätze, überwiegend bestätigend, keine Prüfung gegen das eigene Konfidenzintervall · Erklärung größte Funktion (29,9 % der Wörter), eigene Nullbefunde über Studienmerkmale erklärt (28 Sätze in sieben Studien), nie über die statistische Auflösung · Analyseinstrumente kaum erörtert, keine Methodendiskussion als eigener Teil · Limitationsblock nach Sammoud et al. (2024) · neun Bauregeln (§ 12.2), Projektregeln (§ 12.3), Anwendung je Abschnitt (§ 12.4: Abgleich 6.1, Bauform 12b, Kapitel 7), Prüfliste mit zwölf Punkten (§ 12.5) · elf Befunde zu Steuerdokumenten (§ 13), zehn zu berichtigen oder zu präzisieren, darunter „11 von 11“ in F17 § 5a, Raster 6.1.1 und Textvorschlag 6.1 (Korpus: Zweck 7 von 10, ohne Zahl 9) und das Tempus der Diskussion (F17 § 10 und Stilprofil Teil 7 gegen Bauplan § 6 und den Wortlaut von 6.1). (4) **Zweitprüfung** durch einen unabhängigen Subagenten (Prüfbericht in der Anlage): 41 Befunde (4 A, 14 B, 23 C), alle eingearbeitet, zwei mit begründeter Abweichung (Befund § 14). Die A-Befunde betrafen die Ergebniszahl in der Eröffnung (Moran 1.2), die Absatzanfänge, das Tempus und die Regel zur Rechtfertigung hinter Limitationen (Raster: Muster ausgeschlossen, einzelne Entkräftungen nach F17 § 12 zulässig). (5) **Reproduktion:** Kette 1 bis 9 der Anlage in einer frischen Kopie byte-gleich (14 Ausgabedateien, 32 Zeilendateien) unter drei Werten von PYTHONHASHSEED, vor und nach der Einarbeitung. (6) **Übergabe** `04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` mit Startprompt (§ 0): Schritt 1 Stand (Master, 6.1, Skill-Nachtrag 4a), Schritt 2 Abgleich 6.1 mit Blindcodierung, Schritt 3 Potenziale per Klick, Schritt 4 Task 12b, Schritt 5 Vormerkungen 13a, dazu Entscheidungsregister (§ 4) und Taskwechsel mit Fortsetzungsübergabe (§ 8).

**Eigene Korrekturen in dieser Sitzung:** (1) Aloui et al. (2022): Die fünf Zwischenüberschriften der Diskussion fielen im Korpusbau wegen ihrer Schriftgröße heraus, ergänzt, Satztext unverändert. (2) Die Reihenfolge der Ergebnisse stand zunächst aus der Erinnerung im Entwurf, dann am PDF gelesen, nach der Zweitprüfung mit fester Regel (erste Nennung, gemeinsamer Block gleichrangig): fünf von acht, nach der ausführlichen Darstellung drei. (3) Die Ausgaben waren zunächst nicht deterministisch (Mengen, Schlüsselfolge), berichtigt und unter wechselndem Seed bestätigt.

**Stand der Dateien:** Neu: `02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02.md`, `.docx`, `.pdf` und `_Saetze.csv` · `03_Skripte\\Argumentationsstruktur_Diskussion_2026-10-02\\` (40 Dateien, dazu `lines\\` mit 32 und `blind\\` mit 9 Dateien, `LIESMICH.md`, Prüfbericht `Zweitpruefung_Befund.md`) · `04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` · `03_Skripte\\Steuerung_Rev153_2026-10-02.py` mit `.txt` · Projektkopien `claude/Argumentationsstruktur_Diskussion_RCT_2026-10-02.md` und `claude/Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md`. Geändert: diese Notizen (Rev. 153 auf Rev. 152) · Maßnahmenliste (Stand, G37 (o), Taskzeilen 12 und 13, Summe), je Ordner und Projektkopie. Unverändert: Master (40.331 Byte, MD5 `2fda2144…`), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5. Rückschreibung aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Offen beim Verfasser:** (1) Den Anwendungstask mit dem Startprompt aus Übergabe § 0 in einem neuen Task eröffnen · (2) aus Rev. 152 weiter offen: Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master · (3) Vormerkungen aus Befund § 13 für Fassung 18 und Raster Rev. 4 (G37 (o)) im Steuerdokumente-Task, die Angleichung des Tempus per Klick.

**Nächster Schritt:** Neuer Task „Diskussion: Anwendung der Argumentationsstruktur“ mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` § 0: zuerst 6.1 gegen den Befund abgleichen und die Potenziale per Klick freigeben lassen, dann Task 12b (6.2 und 6.3, 900 Wörter) nach Bauform § 12.4 und Prüfliste § 12.5, zuletzt die Vormerkungen für 13a.

"""
s = ersetze(s, '### ⭐⭐ NEU (Rev. 152, 02.10.2026, 19:36 Sitzungsuhr', BLOCK + '### ⭐⭐ NEU (Rev. 152, 02.10.2026, 19:36 Sitzungsuhr', 'Rev.-Block vor Rev. 152')
s = ersetze(s, '**Stand: (Rev. 152 — siehe Block oben.) Zuvor:', '**Stand: (Rev. 153 — siehe Block oben.) Zuvor: (Rev. 152 — siehe Block oben.) Zuvor:', 'Stand-Zeile der Notizen')
os.makedirs(os.path.join(AUS, '00_Steuerung'), exist_ok=True)
p_n = os.path.join(AUS, '00_Steuerung', 'Cowork_Sitzungsnotizen.md')
open(p_n, 'w', encoding='utf-8', newline='').write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(MASSNAHMEN, encoding='utf-8', newline='').read()
m = ersetze(m, '**Stand 02.10.2026, 19:36 Sitzungsuhr (Rev. 152 —',
            f'**Stand 02.10.2026, {ZEIT} Sitzungsuhr (Rev. 153 — Task „Argumentationsstruktur der Diskussionen“: Befund `02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02` mit Anlage `03_Skripte\\Argumentationsstruktur_Diskussion_2026-10-02\\` (16 Studien, 828 Sätze, blind doppelt codiert, Bauregeln und Prüfliste für Kapitel 6 und 7), unabhängige Zweitprüfung mit 41 Befunden eingearbeitet, Übergabe mit Startprompt `04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md`, G37 (o), Taskzeilen 12 und 13 fortgeschrieben). Zuvor 02.10.2026, 19:36 Sitzungsuhr (Rev. 152 —',
            'Stand-Zeile der Maßnahmenliste')
G37_NEU = (' *(Rev. 153, 02.10.: (o) neu aus dem Befund `02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02` § 13 (nach der Zweitprüfung), '
           'für Fassung 18, Raster Rev. 4 und die Liste der überholten Teile: F17 § 5a Kapitel 6 und 7 mit den Häufigkeiten des Befunds (§ 13 Nr. 1 bis 8) und den Bauregeln § 12.2 · '
           'Raster § 3.14 Zeile 6.1.1 „Bauplan (11/11)“ durch die Häufigkeiten ersetzen (Zweck 7 von 10, Hauptbefund 10, Gegenbefund 5, ohne Beleg 8, ohne Zahl 9), ebenso Textvorschlag 6.1 § 0, § 2, § 4 und § 7 und Kapitelstruktur-Abgleich B5, '
           'Kopfblock § 3.14 um die Bauform Befund § 12.4 · Raster § 3.15 Kopfblock: Zugfolge des Bauplans § 2.5 als Projektfolge kennzeichnen · '
           'Raster § 3.14 „Nicht hier“: die Rechtfertigung hinter jeder Limitation ist das Muster, einzelne Entkräftungen nach F17 § 12 bleiben zulässig (Befund § 9.5) · '
           'G26i um Befund § 13 Nr. 1 bis 5 und 7 bis 10, darunter Bauplan § 1 „sieben durchnummeriert“ (vier von elf) und § 2.4 „in der Reihenfolge der Ergebnisse“ (fünf von acht) · '
           'F17 § 10 und Stilprofil Teil 7 an Bauplan § 6 angleichen (Diskussion: Befunde im Präteritum, Relevanz, Mechanismus und Deutung im Präsens, wie 6.1), per Klick (Befund § 13 Nr. 11) · '
           '(c) bestätigt: drei Studien ohne gebündelten Limitationsteil.)*')
anker = 'Klusemann et al. (2012) für die Aufsicht in G3.)*'
m = ersetze(m, anker, anker + G37_NEU, 'G37 (o)')
z12_alt = 'Offen für 12b: Textvorschlag 6.1 § 9.1 und Nachtrag K2 § 8.2 |'
z12_neu = ('Offen für 12b: Textvorschlag 6.1 § 9.1 und Nachtrag K2 § 8.2 · **Task „Argumentationsstruktur der Diskussionen“ (Rev. 153, 02.10.):** Befund '
           '`02_Befunde\\Argumentationsstruktur_Diskussion_RCT_2026-10-02` (Bauregeln § 12.2, Projektregeln § 12.3, Anwendung je Abschnitt § 12.4, Prüfliste § 12.5) und Übergabe '
           '`04_Uebergaben\\Uebergabe_Diskussion_Argumentationsstruktur_2026-10-02.md` mit Startprompt: zuerst Abgleich von 6.1 und Potenziale per Klick, dann 12b nach Bauform § 12.4, Vormerkungen für 13a |')
m = ersetze(m, z12_alt, z12_neu, 'Taskzeile 12')
z13_alt = 'Nutzungsdaten und Gründe, Merkmale der Vermittlung als offene Frage, ohne Quelle und Zahl) |'
z13_neu = ('Nutzungsdaten und Gründe, Merkmale der Vermittlung als offene Frage, ohne Quelle und Zahl) · Befund Argumentationsstruktur der Diskussionen (Rev. 153) '
           '§ 10 und § 12.4 (13a: Hauptbefund und Praxis ohne Zahl und Quelle wie im Korpus, Reichweite und Ausblick als Projektbausteine nach Raster 7.3 und 7.4, Beitrag nur als Lücke des Settings), Prüfliste § 12.5 Nr. 10 |')
m = ersetze(m, z13_alt, z13_neu, 'Taskzeile 13')
m = ersetze(m, '| **Summe** | Rev. 152 (02.10.):', '| **Summe** | Rev. 153 (02.10.): G37 (o) neu als Vermerk, Taskzeilen 12 und 13 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 152 (02.10.):', 'Summe')
p_m = os.path.join(AUS, '00_Steuerung', 'Massnahmenliste_Datenverarbeitung.md')
open(p_m, 'w', encoding='utf-8', newline='').write(m)

LOG.append(f'Zeit {ZEIT} Sitzungsuhr')
for q, p in [(NOTIZEN, p_n), (MASSNAHMEN, p_m)]:
    LOG.append(f'{os.path.basename(p)}: vorher {os.path.getsize(q)} Byte, MD5 {md5(q)} · nachher {os.path.getsize(p)} Byte, MD5 {md5(p)}')
open(os.path.join(AUS, '03_Skripte', 'Steuerung_Rev153_2026-10-02.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')
print('\n'.join(LOG))

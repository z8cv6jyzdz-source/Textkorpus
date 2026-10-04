# -*- coding: utf-8 -*-
"""
Steuerung_Rev95_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 95) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task „4.7 Statistische Auswertung“

Zweck: Den Task 4.7 festhalten: Textvorschlag mit Kürzungsleiter und unabhängiger Zweitprüfung, Klickfreigabe
der Stufe „Empfehlung“, Einbau per Skript, Endabgleich Fassung 3 ohne Befund, Commit des Masters, Vormerkungen.
Größen, Prüfsummen, Zählwerte und Wortzahlen liest das Skript aus den Dateien (Master vor und nach dem Einbau,
Laufprotokoll des Endabgleichs, Kürzungsleiter), keine Zahl von Hand. Jede Textstelle wird genau einmal ersetzt,
sonst bricht das Skript ab. Ohne Semikolon (Semikola des Bestands über chr(59)).
Aufruf: python Steuerung_Rev95_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md>
        <Master_vor.docx> <Master_nach.docx> <Endabgleich_Manuskript_2026-09-25.txt> <Kuerzungsleiter_4.7_2026-09-25.txt>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re
import hashlib
from docx import Document

SN, ML, M_VOR, M_NACH, EA, KL = sys.argv[1:7]
SEMI = chr(59)


def sha_groesse(pfad):
    b = open(pfad, 'rb').read()
    return hashlib.sha256(b).hexdigest(), len(b)


def tsd(n):
    return format(n, ',').replace(',', ' ')


sha_vor, gr_vor = sha_groesse(M_VOR)
sha_nach, gr_nach = sha_groesse(M_NACH)
ea = open(EA, encoding='utf-8').read()
if 'SHA-256 ' + sha_nach not in ea:
    raise SystemExit('Laufprotokoll des Endabgleichs gehört nicht zum neuen Master')
n_zahlen = int(re.search(r'Zahlen im Master gesamt: (\d+)', ea).group(1))
m = re.search(r'Satzprüfungen: (\d+) davon stimmt (\d+) Abweichungen (\d+)', ea)
n_sp, n_stimmt, n_abw = int(m.group(1)), int(m.group(2)), int(m.group(3))
n_vor = int(re.search(r'Vorschläge: (\d+)', ea).group(1))
n_proz = int(re.search(r'Klasse Prozessdatum \(Register\): (\d+)', ea).group(1))
for w in ['SPSS', 'leistungsunabhängig', 'MDC', 'TE/√n', 'ITT']:
    if int(re.search(r'Wortprüfung ' + re.escape(w) + r': (\d+) Fundstellen', ea).group(1)) != 0:
        raise SystemExit('Wortprüfung nicht leer: ' + w)
kl = open(KL, encoding='utf-8').read()
w_A = int(re.search(r'Fassung A: (\d+) Wörter', kl).group(1))
w_E = int(re.search(r'Empfehlung \(A ohne [^)]*\): (\d+)', kl).group(1))
w_K = int(re.search(r'Kurz \(A ohne [^)]*\): (\d+)', kl).group(1))

# Kapitel-4-Bestand am neuen Master (Absatztext ohne Überschriften, Beschriftungen, Anmerkungen, Platzhalter)
d = Document(M_NACH)
bestand = {}
abschnitt = None
for p in d.paragraphs:
    t = p.text.strip()
    if p.style.name.startswith('Heading'):
        m = re.match(r'(\d(?:\.\d+)*)\s', t)
        abschnitt = m.group(1) if m else None
        continue
    if not abschnitt or not abschnitt.startswith('4') or not t:
        continue
    if p.style.name == 'Caption' or t.startswith('Anmerkung.') or t.startswith('⟨'):
        continue
    bestand[abschnitt] = bestand.get(abschnitt, 0) + len(t.split())
folge = ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.6', '4.7']
for k in folge:
    if k not in bestand:
        raise SystemExit('Abschnitt ohne Text im Master: ' + k)
if bestand['4.7'] != w_E:
    raise SystemExit('4.7 im Master (%d) entspricht nicht der Empfehlung (%d)' % (bestand['4.7'], w_E))
k4 = sum(bestand[k] for k in folge)
k4_ohne47 = k4 - bestand['4.7']
bestand_txt = ' · '.join('%s %d' % (k, bestand[k]) for k in folge)


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


ZEIT = '20:20 MESZ'
# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 94 — siehe Block oben.) Zuvor: (Rev. 93 — siehe Block oben.)',
            '**Stand: (Rev. 95 — siehe Block oben.) Zuvor: (Rev. 94 — siehe Block oben.) Zuvor: (Rev. 93 — siehe Block oben.)')
REV95 = '''### ⭐⭐ NEU (Rev. 95, 25.09.2026, %(zeit)s): Task „4.7 Statistische Auswertung“ — Textvorschlag mit Kürzungsleiter und unabhängiger Zweitprüfung, Klickfreigabe „Empfehlung“ (%(wE)s Wörter), Einbau per Skript, Endabgleich ohne Befund, Master committet

**Auftrag (Verfasser, 25.09., nach F3):** 4.7 nach Berichtsraster schreiben, Rücksprache nur per Klick. Grundlagen gelesen: Berichtsraster Rev. 2 § 3.11 (Zeilen 4.7.1 bis 4.7.15, § 4 Nr. 1 und 6, Prüfliste), Bauplan § 2.2 (Statistikabsatz) mit § 5, § 6 und § 8, Stilprofil, Skill `kapiteltext-bachelorarbeit`, Auswertungsplan § 5 mit § 5.10 (R1 bis R14), Umfangsdokument, Voraussetzungsprüfungen § 5.3, Kennzahlenblatt 25.09. (Rev. 2), Umgebung der Abgabe (R 4.3.3, Basis-R), T4-Zitierfallen, der Master 4.1 bis 4.6, und die Volltexte Lakens (2022), Moher et al. (2010), Fröhlich et al. (2020), Vickers und Altman (2001) am PDF (Seitenangaben geprüft). `citation()` in R 4.3.3 liefert „R Core Team (2024)“.

**(1) Textvorschlag** `04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md` (Erzeuger `03_Skripte\\Textvorschlag_4.7_2026-09-25.py`, Textstufen `Textvorschlag_4.7_2026-09-25_A/_Empf/_Kurz.txt`, Messskript `Messen_Text_2026-09-25.py`, Kürzungsleiter `Kuerzungsleiter_4.7_2026-09-25.py/.txt`): sieben Absätze in der Zugfolge Population → Abweichung nach Protokoll → Fallzahl → Modell → Sensitivität → Voraussetzungen → Prüfung und Software, Eröffnung mit der F3-Formel, Schluss mit der Software (Bauplan § 2.2). **Befund zum Budget:** Die vierzehn P- und E-Zeilen des Rasters ergeben gemessen **%(wA)s Wörter** (Fassung A). Das Budget 550 (23.09.) kannte die seitdem hinzugekommenen Berichtspflichten mit Berichtsort 4.7 nicht (R1, R3, R5, R9 bis R14, Voraussetzungsprüfungen mit O7, KI-Skripterstellung nach Auswertungsverfahren 8.1). Kürzungsleiter K1 bis K14 mit gemessener Ersparnis je Satz, Empfehlung %(wE)s Wörter (Daten- und Rechenprüfung auf zwei Sätze mit Verweis auf die Prüfprotokolle in Anhang G ausgelagert, Erratum-Satz nach 4.3, Tab. H5 nach 5.1, Bootstrap-Einzelheiten und Vorab-Prüfung nach Anhang G und Tab. H4), volle Leiter %(wK)s. Belege nur für Normen und Verfahren (Moher Box 6 und Item 7a, Lakens S. 3–5, 13–14, 14–15, Cohen Tab. 8.4.4, Vickers und Altman, Fröhlich S. 59 und S. 78, Khamis und Roche, R Core Team), alle am Volltext geprüft. Shapiro-Wilk-Test, Brown-Forsythe-Test, Hedges-Faktor J und Perzentil-Bootstrap stehen ohne Beleg, weil die Originalquellen nicht im Ordner liegen (F14 § 7.1, H8, neu H9 Hedges 1981).

**(2) Unabhängige Zweitprüfung** (Subagent ohne Beteiligung am Text): 16 Sachbefunde, zwei Vollständigkeitslücken (Planungsmodell der Antragsrechnung, Power bei Vorab-Erwartungen), Registerposten ohne Satz (R11, R9/R13, Vorab-Prüfung, Familiarisierung Variante a), neun Sprachpunkte, sieben Doppelungen und Widersprüche zu 4.1 bis 4.6, Zitatprüfung am Volltext (Fröhlich S. 59 nur als Norm tragfähig). Alle Befunde eingearbeitet, außer: Anlass des Bootstrap ohne Zahl im Satz (Ergebnis der ersten Rechnung gehört nach 5.2), kein Tab.-3-Verweis in 4.7 (Platzierungsregel § 9). Urteil der Zweitprüfung: verständlich, nachvollziehbar, schwerster Mangel das Budget.

**(3) Klickentscheidung des Verfassers:** Stufe **„Empfehlung“ (%(wE)s Wörter)**. Damit ist das Budget von 4.7 auf rund 720 gesetzt (Verfasserentscheidung per Klick 25.09.), Gegenfinanzierung in der Textrevision von 4.3 (%(b43)d gegen 340) und 4.5.2 (%(b452)d gegen 150). Der Produktname „Claude, Anthropic“ steht im Text (Prüfvermerk § 9 Nr. 1, nicht widersprochen).

**(4) Einbau per Skript** `03_Skripte\\Master_4.7_2026-09-25.py`: sieben Absätze in der Formatvorlage Standard ohne Direktformatierung unmittelbar nach der Überschrift 4.7, Vorbedingungen geprüft (Überschrift genau einmal, Abschnitt leer, keine `comments.xml`, kein Semikolon außerhalb von Klammern, kein Abschnittsverweis, keine Kennung). Validator der docx-Werkzeuge bestanden (Absätze 277 → 284), Render über LibreOffice geprüft (Text unter der Überschrift, nicht im Inhaltsverzeichnis, Blocksatz wie der Bestand). Master vorher %(gr_vor)s Byte (SHA-256 %(sha_vor)s…), nachher %(gr_nach)s Byte (SHA-256 %(sha_nach)s…), Sicherung des Vorstands `_Archiv\\_ersetzt_2026-09-25_Master\\Bachelorarbeit_Geruest_v1_vor_4.7_2026-09-25.docx`. Commit mit Zeitstempelprüfung, zurückgelesene Datei prüfsummengleich.

**(5) Endabgleich Fassung 3** (`Endabgleich_Manuskript_2026-09-25.py`): neue Klasse „Prozessdatum (Register)“ für die Festlegungsdaten 11.09., 12.09. und 15.09.2026 (Satzprüfung SP9c gegen das Register statt gegen die Termine K-03). Lauf am neuen Master: %(n_zahlen)s Zahlen, %(n_sp)s Satzprüfungen, %(n_stimmt)s stimmen, %(n_abw)s Abweichungen, %(n_vor)s Vorschläge, %(n_proz)s Prozessdaten geprüft. Wortprüfung SPSS, MDC, TE/√n, ITT und „leistungsunabhängig“ je 0 Fundstellen, „Signifikanz“ nur in 2.2 (Fremdstudie) und in 4.7 („nicht auf Signifikanz getestet“), „randomisiert“ nur in 2.2. Formale Prüfung 4.7: 0 Semikola, 0 Abschnittsverweise, 0 Sätze über 40 Wörter, 0 Marker. Protokoll `02_Befunde\\Abgleichprotokoll_Manuskript_2026-09-25` (.md/.docx/.pdf, vierter Lauf), Laufprotokoll und Zahlenliste in `03_Skripte`.

**Kapitel-4-Bestand am Master (Absatztext ohne Beschriftungen, Anmerkungen und Platzhalter):** %(bestand)s, Summe 4.1 bis 4.6 = %(k4o)s, mit 4.7 = **%(k4)s** gegen 2 550 (F14 § 5.2). Die Differenz liegt in 4.3, 4.4, 4.5.2 und 4.7 und wird mit der Textrevision (G5, G18, G19) abgebaut.

**Vormerkungen aus dem Task (Maßnahme G29):** 4.3: Erratum-Satz (R14) und Interpolation der Koeffizienten neben die Methode des Reifestatus, „Ausgangstestung“ → „Abschlusstestung“ (auch 4.4.1), Familiarisierungstermine je Verein, „Freigabe der Auswertung in einer Hand“ · 4.1: Adhärenzkriterium-Satz an 4.7 angleichen („nach Sichtung der Adhärenz- und Abschlusswerte“) · 4.4.1 und 4.6: Vorwärtsverweise auf 4.7 und „(neun von zwölf Einheiten)“ entfallen mit G19/G26b · 5.1: Tab. H5 einführen, Untergrenzen der Adhärenz · 5.2: Sammelsatz „sieben Varianten“ (Tab. H4), Prüfgrößen verworfener Voraussetzungen mit Bootstrap-KI (R2), Vorab-Prüfung in einem Satz, Anmerkung zu Tab. H4 mit K-07.2 und K-08.11 · 6.2/6.3: Planungsmodell der Antragsrechnung (L14 a), MDES und Power (G1), Trennschärfe und Robustheit, Konfundierung der Familiarisierung (G7), Cluster (G2), Verdünnung (G3) · Anhang G: Prüfprotokolle, Poweranalyse mit Eingaben, R-Skripte mit `citation()`, Diagramme · Tab. H6: R11 · Literaturverzeichnis: R Core Team (2024), Hedges (1981) nur nach Beschaffung · T4: Cohen1988 (Tab. 8.4.4), Lakens2022 (S. 13–14), Froehlich2020 (S. 59 nur Norm, S. 78 allgemein) · F14 § 5.2: Budget 4.7 rund 720 (I19).

**Regeln eingehalten:** Textvorschlag, Messung, Einbau, Endabgleich und Steuerung nur per Skript (alle ohne Semikolon), keine Zahl von Hand (jede Zahl des Textes mit Kennung oder Quelle im Begleitteil § 7), Kennungen nicht im Manuskript, Master nur nach Klickfreigabe geändert, Vorstand gesichert. Blindordner, Abgabe der zweiten Instanz, Datenstand und Workbook unverändert.

**Dateien (Ordner):** `Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (neu, %(gr_nach)s Byte) · `_Archiv\\_ersetzt_2026-09-25_Master\\` (Vorstand vor 4.7) · `04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md` · `02_Befunde\\Abgleichprotokoll_Manuskript_2026-09-25` (.md/.docx/.pdf) · `03_Skripte\\` Textvorschlag_4.7_2026-09-25.py mit _A/_Empf/_Kurz.txt, Kuerzungsleiter_4.7_2026-09-25.py/.txt, Messen_Text_2026-09-25.py, Master_4.7_2026-09-25.py, Endabgleich_Manuskript_2026-09-25.py (Fassung 3) mit .txt und _Zahlen.csv, Steuerung_Rev95_2026-09-25.py. Projektkopien der .md-Dateien unter `claude/`.

**Nächste Schritte (Reihenfolge fest):** (1) **Task „Kapitel 5“** — 5.1 Teilnehmerfluss, Adhärenz und Ausgangswerte (Abb. 1 als Platzhalter, Tab. 2 Fassung 3 aus `Objekte_2026-09-25.docx`, Tab. H2 und Tab. H5 als Anhangsverweise, Budget 230) und 5.2 Gruppenvergleiche je Zielgröße (Abb. 2 als Platzhalter, Tab. 3, Schlusslogik je Zielgröße nach K-06, verworfene Voraussetzung nach R2 mit Bootstrap-KI, Sammelsatz Tab. H4, Budget 220), drei Regeln des Bauplans (kein Beleg, keine Deutung, Zahlen in den Objekten), Textvorschlag zur Klickfreigabe, Einbau per Skript, Endabgleich · (2) Kapitel 6 und 7 · (3) Textrevision 4.3, 4.4, 4.5.2, 4.6 mit den Vormerkungen G29 und Kürzung Kapitel 2, danach Kapitel 1, 2.5, 3 · (4) Phase 8 (L9): KI-Deklaration, Anhang G, Reproduktionstest · (5) I19: Umfangsdokument § 3.2, Berichtsraster 4.2.5, Auswertungsverfahren 7.3, F14 § 1.2 Nr. 3 und § 5.2 (Budget 4.7) · (6) am Ende: Grafiken einsetzen, Objektverweise prüfen, Word-Seitenmessung (R6), Verzeichnisse F9. Beim Betreuer offen bleibt nur die Fußnotenfrage (§ 8, § 13).

**Maßnahmenliste:** L9 fortgeschrieben (4.7 steht, Anhang G und KI-Deklaration offen), L16 fortgeschrieben (4.7-Teil erledigt, 6.1/6.2-Teil offen), G29 neu (Vormerkungen aus dem 4.7-Task), H9 neu (Hedges 1981), I19 ergänzt (Budget 4.7 in F14 § 5.2).

''' % dict(zeit=ZEIT, wA=w_A, wE=w_E, wK=w_K, b43=bestand['4.3'], b452=bestand['4.5.2'],
           gr_vor=tsd(gr_vor), sha_vor=sha_vor[:8], gr_nach=tsd(gr_nach), sha_nach=sha_nach[:8],
           n_zahlen=n_zahlen, n_sp=n_sp, n_stimmt=n_stimmt, n_abw=n_abw, n_vor=n_vor, n_proz=n_proz,
           bestand=bestand_txt, k4o=tsd(k4_ohne47), k4=tsd(k4))
if SEMI in REV95:
    raise SystemExit('Semikolon im Rev.-95-Block')
s = ersetze(s, '### ⭐⭐ NEU (Rev. 94, 25.09.2026, 17:40 MESZ): Task „Handprobe, Vorschlagsliste und F3“',
            REV95 + '### ⭐⭐ NEU (Rev. 94, 25.09.2026, 17:40 MESZ): Task „Handprobe, Vorschlagsliste und F3“')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(ML, encoding='utf-8').read()
m = ersetze(m, '**Stand 25.09.2026, 17:40 MESZ (Rev. 94 — Handprobe bestanden (R12)',
            '**Stand 25.09.2026, %s (Rev. 95 — 4.7 Statistische Auswertung im Master (Klickfreigabe „Empfehlung“, %d Wörter, Budget 4.7 auf rund 720 gesetzt), Endabgleich Fassung 3 %d von %d Satzprüfungen ohne Abweichung, Kapitel 4 jetzt %s Wörter gegen 2 550. G29 und H9 neu, I19 ergänzt, L9 und L16 fortgeschrieben). Zuvor 25.09.2026, 17:40 MESZ (Rev. 94 — Handprobe bestanden (R12)' % (ZEIT, w_E, n_stimmt, n_sp, tsd(k4)))
# L9
m = ersetze(m, '*(Rev. 94, 25.09.: F3 erteilt, Task 4.7 gestartet — Textvorschlag zur Klickfreigabe, danach Einbau per Skript und Endabgleich)*',
            '*(Rev. 94, 25.09.: F3 erteilt, Task 4.7 gestartet — Textvorschlag zur Klickfreigabe, danach Einbau per Skript und Endabgleich)* *(Rev. 95, 25.09.: **4.7 steht im Master** (Stufe „Empfehlung“, %d Wörter, R 4.3.3 mit `citation()` zitiert, Daten- und Rechenprüfung mit Ergebnis, KI-Skripterstellung, F1 ohne unabhängige Prüfung als Einschränkung, Anhangsverweis G). Offen: KI-Deklaration und Nutzungsprotokoll, Anhang G mit Prüfprotokollen, Poweranalyse-Eingaben, R-Skripten und Diagrammen, Reproduktionstest)*' % w_E)
# L16
m = ersetze(m, 'Zuordnung der Zahlen in der Begründung des Textvorschlags. Task 4.7 gestartet)*',
            'Zuordnung der Zahlen in der Begründung des Textvorschlags. Task 4.7 gestartet)* *(Rev. 95, 25.09.: 4.7-Teil erledigt — Prüfungen in zwei Sätzen, Regel O7 mit Grund, „geprüft und nicht verworfen“, Bootstrap als nachträgliche Zusatzsensitivität, F1 ohne unabhängige Methodenprüfung. Offen: die sechs Punkte für 6.2 aus Befund § 5.3 und der 5.2-Satz nach R2)*')
# I19
m = ersetze(m, 'Das R-Skript (Fassung 3) und der Endabgleich (Fassung 2) sind bereits umgestellt. *(25.09., Rev. 94)*',
            'Das R-Skript (Fassung 3) und der Endabgleich (Fassung 2) sind bereits umgestellt. *(25.09., Rev. 94)* *(Rev. 95: dazu (c) F14 § 5.2 Budget 4.7 rund 720 statt 550 (Klickentscheidung 25.09., Begründung Textvorschlag 4.7 § 1), Gegenfinanzierung 4.3 und 4.5.2 · (d) Berichtsraster Kopfblock 3.11 Budget und Zeile 4.7.13 mit Anhang G als Ort der Prüfprotokolle)*')
# G29 neu vor dem H-Abschnitt
G29 = ('- [ ] **G29 · Vormerkungen aus dem Task 4.7 (25.09., Rev. 95, Textvorschlag § 10):** (a) 4.3: Erratum-Satz (R14) und Interpolation der Koeffizienten (O2) neben die Methode des Reifestatus · „Ausgangstestung“ → „Abschlusstestung“ (auch 4.4.1) · Familiarisierungstermine je Verein (Raster 4.3.4) · „Testleitung, Datenerhebung und Freigabe der Auswertung in einer Hand“ · '
       '(b) 4.1: Adhärenzkriterium-Satz an 4.7 angleichen („nach Sichtung der Adhärenz- und Abschlusswerte der Interventionsgruppe“) · (c) 4.4.1 und 4.6: „(Abschn. 4.7)“, „dessen Anwendung ist in Abschnitt 4.7 geregelt“ und „(neun von zwölf Einheiten)“ entfallen (G19, G26b) · '
       '(d) 5.1: Tab. H5 einführen (Schwellenlandschaft), Untergrenzen der Adhärenz (K-10.11) · (e) 5.2: Sammelsatz „sieben Varianten, darunter der Per-Protokoll-Vergleich“ (Tab. H4), Prüfgrößen verworfener Voraussetzungen mit Bootstrap-KI (R2), Vorab-Prüfung an den Prä-Werten in einem Satz, Anmerkung zu Tab. H4 mit K-07.2 und K-08.11 · '
       '(f) 6.2/6.3: Planungsmodell der Antragsrechnung (L14 a), MDES gegen SESOI und Power bei Vorab-Erwartungen (G1), Trennschärfe und Robustheit (Voraussetzungsprüfungen § 5.3), Konfundierung der Familiarisierung (G7), Analyseeinheit (G2), Verdünnung (G3) · '
       '(g) Anhang G: Prüfprotokolle (Belegprotokoll, Abgleich, Durchsicht, Plausibilität, Handprobe, Rückfragen, Nachtrag 3), Poweranalyse mit Eingaben je Zielgröße, R-Skripte mit `citation()`, Q-Q- und Linearitätsdiagramme · (h) Tab. H6: R11 (Reifestatus alt/neu) · '
       '(i) Literaturverzeichnis: R Core Team (2024) aus `citation()`, Hedges (1981) nur nach Beschaffung (H9) · (j) T4: Cohen1988 (Tab. 8.4.4 für die Planungsrechnung), Lakens2022 (S. 13–14 KI-Breite), Froehlich2020 (S. 59 nur Norm, S. 78 Bootstrapping allgemein). *(25.09., Rev. 95)*')
m = ersetze(m, '\n\n## H  BESCHAFFUNG — teils blockierend für die Begründung', '\n' + G29 + '\n\n## H  BESCHAFFUNG — teils blockierend für die Begründung')
# H9 neu nach H8
zeilen = m.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **H8 · Quellen aus dem Befund Voraussetzungsprüfungen')]
if len(idx) != 1:
    raise SystemExit('H8 nicht genau einmal gefunden')
H9 = ('- [ ] **H9 · Hedges, L. V. (1981). Distribution theory for Glass\'s estimator of effect size and related estimators. *Journal of Educational Statistics, 6*(2), 107–128.** Verfahrensquelle für den Kleinstichprobenfaktor J von Hedges\' g (Spezifikation O3). '
      '4.7 nennt den Faktor ohne Beleg, weil der Volltext fehlt (F14 § 7.1). Nach Beschaffung Klammer in 4.7 ergänzen, T1 anlegen. *(25.09., Rev. 95)*')
zeilen.insert(idx[0] + 1, H9)
m = '\n'.join(zeilen)
for neu in (G29, H9):
    if SEMI in neu:
        raise SystemExit('Semikolon in neuer Maßnahme')
# Tabelle und Summe
m = ersetze(m, '| H — Beschaffung | 5 (H3 Cohen erledigt 12.09.) |', '| H — Beschaffung | 6 (H3 Cohen erledigt 12.09., H9 Hedges 1981 neu Rev. 95) |')
m = ersetze(m, '| **Summe** | **57 offen** (Stand 25.09., Rev. 94: L8 und L10 erledigt, I19 neu — Zählung nicht neu erhoben.',
            '| **Summe** | **57 offen** (Stand 25.09., Rev. 95: G29 und H9 neu, L9, L16 und I19 fortgeschrieben — Zählung nicht neu erhoben. Stand 25.09., Rev. 94: L8 und L10 erledigt, I19 neu — Zählung nicht neu erhoben.')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
print('Sitzungsnotizen Rev. 95 und Maßnahmenliste fortgeschrieben: 4.7 %d Wörter, Kapitel 4 %d, Endabgleich %d/%d, Master %d → %d Byte' % (w_E, k4, n_stimmt, n_sp, gr_vor, gr_nach))

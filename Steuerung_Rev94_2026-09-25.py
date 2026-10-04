# -*- coding: utf-8 -*-
"""
Steuerung_Rev94_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 94) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Abschluss von Phase 7 (F3)

Zweck: Den Task „Handprobe, Vorschlagsliste und F3“ (Verfasser 25.09.: selbstständig durchführen, Rücksprache
nur per Klick) in den beiden Steuerdokumenten festhalten: Handprobe B4, Klickentscheidungen, Übertrag der
Vorschlagsliste 1 bis 7 in den Master, zwei Verfasserfestlegungen (keine Kennungen im Master, Kennwerte in 4.2),
R-Skript Fassung 3, Endabgleich Fassung 2 mit drittem Lauf, Freigabe F3. Größen, Prüfsummen, Zählwerte und das
Urteil der Handprobe liest das Skript aus den Dateien, keine Zahl von Hand. Jede Textstelle wird genau einmal
ersetzt, sonst bricht das Skript ab. Ohne Semikolon (Semikola des Bestands über chr(59)).
Aufruf: python Steuerung_Rev94_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md>
        <Master_vor.docx> <Master_nach.docx> <Endabgleich_Manuskript_2026-09-25.txt> <Handprobe_2026-09-25.xlsx>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re
import hashlib
from openpyxl import load_workbook

SN, ML, M_VOR, M_NACH, EA, HP = sys.argv[1:7]
SEMI = chr(59)


def sha_groesse(pfad):
    b = open(pfad, 'rb').read()
    return hashlib.sha256(b).hexdigest(), len(b)


sha_vor, gr_vor = sha_groesse(M_VOR)
sha_nach, gr_nach = sha_groesse(M_NACH)
ea = open(EA, encoding='utf-8').read()
m = re.search(r'Zahlen im Master gesamt: (\d+)', ea)
n_zahlen = int(m.group(1))
m = re.search(r'Satzprüfungen: (\d+) davon stimmt (\d+) Abweichungen (\d+)', ea)
n_sp, n_stimmt, n_abw = int(m.group(1)), int(m.group(2)), int(m.group(3))
m = re.search(r'Vorschläge: (\d+)', ea)
n_vor = int(m.group(1))
if 'SHA-256 ' + sha_nach not in ea:
    raise SystemExit('Laufprotokoll des Endabgleichs gehört nicht zum neuen Master')
wort = {}
for w in ['SPSS', 'leistungsunabhängig', 'MDC', 'TE/√n', 'ITT']:
    m = re.search(r'Wortprüfung ' + re.escape(w) + r': (\d+) Fundstellen', ea)
    wort[w] = int(m.group(1))
if any(v != 0 for v in wort.values()):
    raise SystemExit('Wortprüfung nicht leer: %r' % wort)
wb = load_workbook(HP)
b4 = wb['Handprobe']['B4'].value
if not (isinstance(b4, str) and b4.startswith('bestanden')):
    raise SystemExit('Handprobe B4 trägt kein Urteil „bestanden“: %r' % b4)


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


ZEIT = '17:40 MESZ'
# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 93 — siehe Block oben.) Zuvor: (Rev. 92 — siehe Block oben.)',
            '**Stand: (Rev. 94 — siehe Block oben.) Zuvor: (Rev. 93 — siehe Block oben.) Zuvor: (Rev. 92 — siehe Block oben.)')
REV94 = '''### ⭐⭐ NEU (Rev. 94, 25.09.2026, %(zeit)s): Task „Handprobe, Vorschlagsliste und F3“ — Handprobe bestanden (R12 abgeschlossen), Vorschlagsliste 1 bis 7 im Master, Endabgleich ohne Befund, **Freigabe F3 erteilt, Phase 7 abgeschlossen**, zwei Verfasserfestlegungen (keine Kennungen im Master, Kennwerte in 4.2 statt in Tab. 2)

**Auftrag (Verfasser, 25.09., nach 17:00 MESZ):** die drei Schritte aus dem Rev.-92-Block „selbstständig durchführen und nur per Klickantworten Rücksprache halten“ — Handprobe prüfen (Urteil in B4), Vorschlagsliste 1 bis 7 übertragen, Endabgleich erneut, Freigabe F3. Die Prozessregel (Freigabe je Abschnitt, F14 § 1.2) ist über die Klickantworten erfüllt. Alle Schritte erledigt, Details:

**(1) Handprobe 6.3 (R12) abgeschlossen.** Urteil des Verfassers per Klick, eingetragen in `04_Uebergaben\\Handprobe_2026-09-25.xlsx` Zelle B4: „%(b4)s“. Die Formeln der Mappe sind erhalten, die volle Neuberechnung beim Öffnen bleibt gesetzt. Damit ist Phase 6 vollständig (6.1 bis 6.4).

**(2) Klickentscheidungen zur Vorschlagsliste (zwei Runden).** Runde 1: 4.3 freigegeben (Vorschlag 6), 4.4 alle vier freigegeben (Vorschläge 2 bis 5 mit Tab. 1, Titel und Anmerkung), 4.2 mit Freitext des Verfassers: Die Kennungen „[K-…]“ neben den Zahlen haben keinen erkennbaren Mehrwert („eher streichen als hinzufügen“), die Angaben zu Körperhöhe, Körpermasse, Alter und Reifestatus sind „sehr wichtig“, aber auf Doppelung zu prüfen und dann an einem Ort zu führen. Runde 2 mit zwei **Verfasserfestlegungen (25.09.)**: (a) **Keine Kennungen im Master.** Die Rückverfolgbarkeit jeder Zahl leistet der Endabgleich (`Endabgleich_Manuskript_2026-09-25_Zahlen.csv`, Zuordnung je Zahl zur Kennung), nicht der Manuskripttext. Der Satz in Auswertungsverfahren 7.3 („Bis zur Endfassung steht die Kennung neben der Zahl“) und F14 § 1.2 Nr. 3 („Jede Zahl im Manuskript trägt eine Kennung aus diesem Blatt“) sind damit überholt (I19). (b) **Kennwerte der Stichprobe (Alter, Körperhöhe, Körpermasse, Reifestatus je Gruppe) bleiben in 4.2, Tab. 2 führt diese Zeilen nicht.** Das ersetzt die Zeile 4.2.5 des Berichtsrasters (Kennwerte in Tab. 2, 4.2 ohne Zahlen) und Umfangsdokument § 3.2 zu Tab. 2 (I19). Beide Festlegungen stehen hier und in der Maßnahmenliste, die Dokumente werden mit ihrer nächsten Revision nachgezogen.

**(3) Übertrag in den Master per Skript** `03_Skripte\\Master_Vorschlagsliste_2026-09-25.py` (Master, `Tab_1_Messguete.csv` des R-Objekts, Ziel): 4.2 Reifestatus je Gruppe nach R11 (Vorschlag 1, ohne Kennungen) · 4.3 Abschlusstestung Verein C 14.09. statt 15.09. (Vorschlag 6) · 4.4 Halbsatz „innerhalb der Gruppen ohne erkennbaren Zusammenhang mit der Leistung“ gestrichen und Verweis „(Tab. 1, n)“ entfernt (Vorschlag 2), TE/√n-Satz durch den Satz zu kleinster nachweisbarer Effektstärke und KI-Breite nach Lakens (2022) ersetzt (Vorschlag 4), Tab. 1 mit sieben Spalten aus der CSV des R-Objekts (Zielgröße, n, TE [95-%%-KI], CV (%%), SESOI, TE/SESOI, TE post [95-%%-KI]) ohne MDC und ohne TE/√n, Titel und Anmerkung neu (Vorschläge 3 und 5, ohne Kennungen, n post je Zielgröße in der Anmerkung) · Anhang G „Sensitivitäts-Poweranalyse und R-Skripte“ (Vorschlag 7, M7). Satz: Die Konfidenzintervalle der Tab. 1 passen einzeilig nicht in die Textbreite (mit Liberation-Sans-Metrik gemessen), deshalb zweizeilige Zellen (Wert, Zeilenumbruch, „[a bis b]“), Spaltenbreiten 2090, 400, 1600, 760, 730, 1040 und 1600 dxa (Summe 8220 = Textbreite), Zellrand 0,1 cm. Render über LibreOffice geprüft: Tab. 1 auf einer Seite, kein Umbruch innerhalb eines Intervalls. Master vorher %(gr_vor)s Byte (SHA-256 %(sha_vor)s…), nachher %(gr_nach)s Byte (SHA-256 %(sha_nach)s…), Sicherung des Vorstands `_Archiv\\_ersetzt_2026-09-25_Master\\Bachelorarbeit_Geruest_v1_vor_Vorschlagsliste_2026-09-25.docx`. Word war beim Commit geschlossen, Zielname und Größe geprüft.

**(4) R-Skript Fassung 3** (`03_Skripte\\Objekte_2026-09-25.R`): Tab. 2 ohne die Zeilen Alter, Körperhöhe, Körpermasse und %%PAH, erste Spalte „Zielgröße“, Titel „Ausgangswerte je Zielgröße im Analyseset, Mittelwert ± Standardabweichung, ohne Signifikanztests“, Anmerkung neu (Analyseset je Zielgröße: Spieler mit Prä- und Post-Wert und %%PAH). Alle Objekte neu erzeugt, real (1 470 Kennungen verwendet) und synthetisch (1 410), `Objekte_2026-09-25.docx` neu gesetzt, `06_Abbildungen` nachgeführt. Kein Wert geändert, nur die Auswahl der Zeilen von Tab. 2.

**(5) Endabgleich Fassung 2** (`03_Skripte\\Endabgleich_Manuskript_2026-09-25.py`): Neufassungen ohne Kennungen, die Kennungen stehen in der Begründung jedes Vorschlags · der Tab.-1-Vorschlag erscheint nur bei einer Abweichung · Teil 0 nennt die Kennungsregel des Verfassers · Teil 5 schreibt bei leerer Liste „Keine Vorschläge“. Dritter Lauf am neuen Master: %(n_zahlen)s Zahlen, %(n_sp)s Satzprüfungen, %(n_stimmt)s stimmen, %(n_abw)s Abweichungen, %(n_vor)s Vorschläge. Wortprüfung SPSS, MDC, TE/√n, ITT und „leistungsunabhängig“ je 0 Fundstellen, „randomisiert“ und „Signifikanz“ nur in 2.2 über Fremdstudien. Protokoll `02_Befunde\\Abgleichprotokoll_Manuskript_2026-09-25` (.md/.docx/.pdf), Laufprotokoll und Zahlenliste in `03_Skripte`.

**(6) Freigabe F3 erteilt** (Klick des Verfassers, 25.09., nach 17:30 MESZ, Auswertungsverfahren Phase 7 „Übertrag in das Manuskript“). Damit sind die Phasen 1 bis 7 abgeschlossen, L8 ist erledigt. Offen aus dem Verfahren: Phase 8 (L9) mit dem Methodenteil 4.7 als erstem Stück.

**Regeln eingehalten:** Übertrag, Steuerung und Objekte nur per Skript (alle ohne Semikolon), Ergebniswerte nur in Dateien, keine Zahl von Hand (Tab. 1 aus der CSV des R-Objekts, Reifestatus aus dem Kennzahlenblatt über die Vorschlagsliste). Blindordner, Abgabe der zweiten Instanz, Datenstand und Workbook unverändert. Master nur nach Klickfreigabe je Abschnitt geändert, Vorstand gesichert.

**Dateien (Ordner):** `Schreiben\\Bachelorarbeit_Gerüst_v1_AKTUELL.docx` (neu, %(gr_nach)s Byte) · `_Archiv\\_ersetzt_2026-09-25_Master\\` (Vorstand) · `02_Befunde\\` Abgleichprotokoll_Manuskript_2026-09-25 (.md/.docx/.pdf, dritter Lauf) · `03_Skripte\\` Master_Vorschlagsliste_2026-09-25.py, Endabgleich_Manuskript_2026-09-25.py (Fassung 2) mit .txt und _Zahlen.csv, Objekte_2026-09-25.R (Fassung 3), Objekte_2026-09-25\\ und _synthetisch\\ (neu gesetzt), Steuerung_Rev94_2026-09-25.py · `04_Uebergaben\\` Handprobe_2026-09-25.xlsx (B4) · `06_Abbildungen\\` (nachgeführt). Projektkopien der .md-Dateien unter `claude/`.

**Nächste Schritte (Reihenfolge fest):** (1) **Task „4.7 Statistische Auswertung“** — läuft: Berichtsraster Zeilen 4.7.1 bis 4.7.13, Bauplan-Statistikabsatz, Stilprofil, Skill, Budget 550, R1 bis R14 als nachträgliche Festlegungen, Einschränkungen F1 ohne unabhängige Prüfung und Erratum nicht eingesehen, R-Zitat aus `citation()` der Abgabe, keine Kennungen, kein Semikolon, kein Abschnittsverweis. Textvorschlag in `04_Uebergaben`, Freigabe per Klick, dann Einbau per Skript und Endabgleich erneut · (2) Task „Kapitel 5“ (5.1 mit Abb. 1 als Platzhalter und Tab. 2 Fassung 3, Tab. H2 im Anhang, 5.2 mit Abb. 2 als Platzhalter und Tab. 3, Schlusslogik je Zielgröße, Budget 450) · (3) Kapitel 6 und 7, danach Kürzung Kapitel 2 und Kapitel 1, 2.5, 3 · (4) Phase 8 (L9): KI-Deklaration, Anhang G, Reproduktionstest · (5) I19: Umfangsdokument § 3.2, Berichtsraster 4.2.5, Auswertungsverfahren 7.3 und F14 § 1.2 Nr. 3 an die Festlegungen vom 25.09. anpassen · (6) am Ende: Grafiken einsetzen, Objektverweise prüfen, Word-Seitenmessung (R6), Verzeichnisse F9. Beim Betreuer offen bleibt nur die Fußnotenfrage (§ 8, § 13).

**Maßnahmenliste:** L8 erledigt (F3), L10 Rest erledigt (M7), L16 fortgeschrieben (4.7 gestartet), L9 fortgeschrieben, I19 neu (Folgeänderungen der Festlegungen vom 25.09.).

''' % dict(zeit=ZEIT, b4=b4, gr_vor=format(gr_vor, ',').replace(',', ' '), sha_vor=sha_vor[:8],
           gr_nach=format(gr_nach, ',').replace(',', ' '), sha_nach=sha_nach[:8], n_zahlen=n_zahlen,
           n_sp=n_sp, n_stimmt=n_stimmt, n_abw=n_abw, n_vor=n_vor)
if SEMI in REV94:
    raise SystemExit('Semikolon im Rev.-94-Block')
s = ersetze(s, '### ⭐ NACHTRAG (Rev. 93, 25.09.2026, 17:05 MESZ): Papierkorb-Skript gelaufen',
            REV94 + '### ⭐ NACHTRAG (Rev. 93, 25.09.2026, 17:05 MESZ): Papierkorb-Skript gelaufen')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(ML, encoding='utf-8').read()
m = ersetze(m, '**Stand 25.09.2026, 17:05 MESZ (Rev. 93 — Papierkorb-Skript vom Verfasser gelaufen',
            '**Stand 25.09.2026, %s (Rev. 94 — Handprobe bestanden (R12), Vorschlagsliste 1 bis 7 im Master, Endabgleich %d von %d Satzprüfungen ohne Abweichung, **F3 erteilt, Phase 7 abgeschlossen**, Verfasserfestlegungen: keine Kennungen im Master, Kennwerte in 4.2 statt Tab. 2. L8 und L10 erledigt, I19 neu, Task 4.7 gestartet). Zuvor 25.09.2026, 17:05 MESZ (Rev. 93 — Papierkorb-Skript vom Verfasser gelaufen' % (ZEIT, n_stimmt, n_sp))
# L8
m = ersetze(m, '- [ ] **L8 · Phase 5–7:** Gesamtlauf beider Ketten',
            '- [x] **L8 · Phase 5–7:** **Erledigt 25.09. (Rev. 94): Handprobe bestanden (B4, R12), Vorschlagsliste 1 bis 7 per `Master_Vorschlagsliste_2026-09-25.py` im Master, Endabgleich dritter Lauf %d von %d Satzprüfungen ohne Abweichung und ohne Vorschlag, F3 per Klick erteilt.** Ursprünglich: Gesamtlauf beider Ketten' % (n_stimmt, n_sp))
m = ersetze(m, 'Ergebnis unverändert. **Offen:** Vorschlagsliste übertragen, Endabgleich danach erneut, **Freigabe F3**)*',
            'Ergebnis unverändert. **Offen:** Vorschlagsliste übertragen, Endabgleich danach erneut, **Freigabe F3**)* *(Rev. 94, 25.09.: alles erledigt, F3 erteilt, Verfasserfestlegung „keine Kennungen im Master“, Endabgleich Fassung 2 ohne Kennungen in den Neufassungen)*')
# L9
m = ersetze(m, 'Anhang G nur anonymisiert, Reproduktionstest. *(24.09.)*',
            'Anhang G nur anonymisiert, Reproduktionstest. *(24.09.)* *(Rev. 94, 25.09.: F3 erteilt, Task 4.7 gestartet — Textvorschlag zur Klickfreigabe, danach Einbau per Skript und Endabgleich)*')
# L10
m = ersetze(m, 'Offen daraus nur der Anhang-G-Titel im Master (M7, Textrevision).',
            'Offen daraus nur der Anhang-G-Titel im Master (M7, Textrevision). *(Rev. 94, 25.09.: M7 erledigt — Anhang G „Sensitivitäts-Poweranalyse und R-Skripte“ im Master, Vorschlag 7 des Endabgleichs)*')
# L16
m = ersetze(m, 'Koeffizienten der Originalpublikation von Khamis und Roche, Erratum nicht eingesehen)*',
            'Koeffizienten der Originalpublikation von Khamis und Roche, Erratum nicht eingesehen)* *(Rev. 94, 25.09.: TE/√n-Satz in 4.4 ersetzt (Vorschlag 4). Für 4.7 zusätzlich: keine Kennungen im Text (Verfasserfestlegung 25.09.), Zuordnung der Zahlen in der Begründung des Textvorschlags. Task 4.7 gestartet)*')
# I19 neu, nach I18
zeilen = m.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [x] **I18 · Neue Limitation: ungleiche Versuchszahl zwischen den Gruppen**')]
if len(idx) != 1:
    raise SystemExit('I18 nicht genau einmal gefunden')
I19 = ('- [ ] **I19 · Folgeänderungen der Verfasserfestlegungen vom 25.09.2026 (Rev. 94):** (a) keine Kennungen im Manuskript, '
       'Rückverfolgbarkeit über die Zahlenliste des Endabgleichs → Auswertungsverfahren 7.3 („Bis zur Endfassung steht die Kennung neben der Zahl“) '
       'und F14 § 1.2 Nr. 3 („Jede Zahl im Manuskript trägt eine Kennung aus diesem Blatt“) umformulieren · (b) Kennwerte der Stichprobe '
       '(Alter, Körperhöhe, Körpermasse, Reifestatus je Gruppe) in 4.2, Tab. 2 ohne diese Zeilen → Berichtsraster Zeile 4.2.5, '
       'Umfangsdokument § 3.2 (Tab. 2) und F14 § 5.3 (Tab. 2) nachziehen. Jeweils mit der nächsten Revision des Dokuments, keine eigene Fassung dafür. '
       'Das R-Skript (Fassung 3) und der Endabgleich (Fassung 2) sind bereits umgestellt. *(25.09., Rev. 94)*')
if SEMI in I19:
    raise SystemExit('Semikolon in I19')
zeilen.insert(idx[0] + 1, I19)
m = '\n'.join(zeilen)
# Tabelle und Summe
m = ersetze(m, '| I — Korrekturen | 7 (I10 erledigt 12.09.) |',
            '| I — Korrekturen | 8 (I10 erledigt 12.09., I19 neu Rev. 94) |')
m = ersetze(m, 'Rev. 93: L21 erledigt, Zählung nicht neu erhoben) | Phasen 1 bis 7 gelaufen, F3 und Vorschlagsliste beim Verfasser, dann 4.7, Kapitel 5, Phase 8 |',
            'Rev. 93: L21 erledigt, Rev. 94: L8 und L10 erledigt (F3), Zählung nicht neu erhoben) | Phasen 1 bis 7 abgeschlossen (F3 25.09.), Phase 8 läuft mit 4.7, dann Kapitel 5 |')
m = ersetze(m, '| **Summe** | **57 offen** (Stand 25.09., Rev. 93:',
            '| **Summe** | **57 offen** (Stand 25.09., Rev. 94: L8 und L10 erledigt, I19 neu — Zählung nicht neu erhoben. Stand 25.09., Rev. 93:')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
print('Sitzungsnotizen Rev. 94 und Maßnahmenliste fortgeschrieben: Endabgleich %d/%d, Vorschläge %d, Master %d → %d Byte' % (n_stimmt, n_sp, n_vor, gr_vor, gr_nach))

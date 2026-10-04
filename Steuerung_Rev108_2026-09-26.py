# -*- coding: utf-8 -*-
"""
Steuerung_Rev108_2026-09-26.py — Fortschreibung der Steuerdokumente nach Schritt 0 der Übergabe Kapitel 2
Bachelorarbeit U15-Plyometrie · DSHS Köln

Schreibt Rev. 108 in Teil 0 der Sitzungsnotizen, trägt A8 (Rev. 106), G26b, G29, G31, H9, L14, L16 und die neue
G32 in die Maßnahmenliste ein, ergänzt den Plan (Nachtrag, § 1a, § 3 Task 6) und hängt an den Textvorschlag 4.7
vom 26.09. den § 10 (Nachtrag Schritt 0) an. Jede Ersetzung muss genau einmal greifen, sonst Abbruch.
Aufruf: python Steuerung_Rev108_2026-09-26.py <Ordner Claude> <Ausgabeordner>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import os

CLA, AUS = sys.argv[1:3]
os.makedirs(AUS, exist_ok=True)
PROT = []


def lies(rel):
    return open(os.path.join(CLA, rel), encoding='utf-8').read()


def schreibe(name, text):
    with open(os.path.join(AUS, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    PROT.append('geschrieben ' + name + ' ' + str(len(text.encode('utf-8'))) + ' Byte')


def nach(text, anker, zusatz, was):
    n = text.count(anker)
    if n != 1:
        raise SystemExit('%s: Anker %d-mal gefunden' % (was, n))
    PROT.append('ergänzt: ' + was)
    return text.replace(anker, anker + zusatz, 1)


def ersetze(text, alt, neu, was):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('%s: Suchtext %d-mal gefunden' % (was, n))
    PROT.append('ersetzt: ' + was)
    return text.replace(alt, neu, 1)


def zeile(text, praefix, neu, was):
    z = [l for l in text.split('\n') if l.startswith(praefix)]
    if len(z) != 1:
        raise SystemExit('%s: Zeile %d-mal gefunden' % (was, len(z)))
    PROT.append('Zeile ersetzt: ' + was)
    return text.replace(z[0], neu, 1)


# ---------------------------------------------------------------- Sitzungsnotizen
SN = '00_Steuerung/Cowork_Sitzungsnotizen.md'
t = lies(SN)
t = ersetze(t, '**Stand: (Rev. 107 — siehe Block oben.)', '**Stand: (Rev. 108 — siehe Block oben.) Zuvor: (Rev. 107 — siehe Block oben.)', 'SN Stand')
REV108 = """### ⭐⭐ NEU (Rev. 108, 26.09.2026, 21:15 MESZ): Schritt 0 — Nachkorrekturen per Skript im Master (Verfasserauftrag), Task 6 abgeschlossen, Task 7 (2.4) begonnen

**Auftrag (Verfasser, 26.09., 20:51):** Startsatz der Übergabe Kapitel 2 mit Schritt 0, die sieben Nachkorrekturen seien übertragen. **Befund 20:52:** Master unverändert seit 20:21 (52.734 Byte, MD5 d8ca4d42…), keine der sieben Stellen gespeichert. **Verfasser 20:55:** „Bitte übernehme du das oder wir machen direkt mit Kapitel 2 weiter. Nicht das ganze Kapitel, sondern Abschnitt für Abschnitt.“ Das ist die ausdrückliche Anweisung zum direkten Einbau für Schritt 0 (F16 § 1.2). **Klick 4.6:** Wortlaut Rev. 105 mit Nr. 20 (Befund B1, Fortschrittskarte fehlte), „Ethikantrag“ bleibt (Nr. 29 nicht übernommen, wie Nr. 30 und 31).

**Einbau** per `03_Skripte\\Master_Schritt0_2026-09-26.py` (Protokoll `.txt`): 4.1 Abs. 5 Nr. 21 „Das Adhärenzkriterium wurde in der Hauptanalyse nicht angewandt.“ · 4.4.2 Schlusspunkt (Nr. 22, G31 a) · 4.6 Rev. 105 mit Fortschrittskarte und „Adhärenzkriterium“ (B1, Nr. 20) · 4.7 Abs. 1 „(Moher et al., 2010, S. 17)“ (Box 6 auf S. 17 von 28, am PDF erneut geprüft) und „laut Studienprotokoll“ · 4.7 Abs. 2 „nach einer ersten Auswertung“ · 4.7 Voraussetzungsabsatz vor Sensitivitätsabsatz (Nr. 54). Nicht übernommen: Festlegungsdaten in 4.7 (Verfasser: kommen in Tab. H6), Nr. 30, 31 und 57a (bis Task 18 offen). validate.py bestanden, Absätze 218 → 218, Diff (pandoc) nur an den sieben Absätzen, Render geprüft. Master **48.791 Byte, MD5 e35315d6…**, zurückgeschrieben 26.09., 21:05, mit mtime-Guard, `cmp` identisch, keine `comments.xml`.

**Messung** (`Manuskriptstand_2026-09-25.py`, `.txt` und `.csv` neu geschrieben): 4.1 291 · 4.2 208 · 4.3 340 · 4.4 392 · 4.5.1 418 · 4.5.2 150 · 4.6 154 · 4.7 463 · Kapitel 4 (4.1 bis 4.6) 1.953 gegen 2.000 · mit 4.7 2.416 gegen 2.550 · Kapitel 2 (2.1 bis 2.4) 4.920 gegen 2.950 · Absatztext 7.336 · Semikola 61 und Abschnittsverweise 35, alle in Kapitel 2. **Endabgleich** (Fassung 3): 657 Zahlen, 23 Satzprüfungen, 21 stimmen, 2 bekannte Abweichungen (SP6 Tab. 1 als Platzhalter, SP11 Pausen), keine Datumsprüfung in 4.7 mehr, „randomisiert“ zweimal und „Signifikanz“ einmal in 2.2 (Task 10). Die Zahlenliste wird wie bisher erst mit dem letzten Endabgleich erneuert (Task 18 g).

**Task 6 erledigt.** 4.7 steht mit 463 gegen 550, Kapitel 4 ist textlich fertig, der Kürzungsauftrag betrifft nur noch Kapitel 2 (1.970). Maßnahmenliste: A8 (Rev. 106 aus der Projektkopie), G26b, G29, G31 (a), H9, L14, L16 fortgeschrieben, **G32 neu** mit den Vormerkungen aus Textvorschlag 4.7 § 7 je Task, Zusammenfassung. Plan: Nachtrag, § 1a, § 3 Task 6. Textvorschlag 4.7 § 10 (Nachtrag Schritt 0).

**Befund zum Verfahren:** Die Übertragung war gemeldet, aber nicht gespeichert. Jeder Abgleich prüft deshalb zuerst Größe, MD5 und Speicherzeit gegen den letzten Stand.

**Nächster Schritt:** Task 7 (2.4 mit 2.4.1 bis 2.4.3 auf höchstens 700) in dieser Sitzung, Zug-Zuordnung und Kürzungsleiter zuerst, Vorschläge absatzweise im Chat, der Verfasser überträgt selbst.

"""
t = ersetze(t, '### ⭐⭐ NEU (Rev. 107, 26.09.2026, 20:35 MESZ)', REV108 + '### ⭐⭐ NEU (Rev. 107, 26.09.2026, 20:35 MESZ)', 'SN Rev. 108')
schreibe('Cowork_Sitzungsnotizen.md', t)

# ---------------------------------------------------------------- Maßnahmenliste
ML = '00_Steuerung/Massnahmenliste_Datenverarbeitung.md'
m = lies(ML)
m = ersetze(m, '**Stand 25.09.2026, 23:05 MESZ (Rev. 103 —',
            '**Stand 26.09.2026, 21:15 MESZ (Rev. 108 — Schritt 0 der Übergabe Kapitel 2: Nachkorrekturen per Skript im Master, Task 6 abgeschlossen. A8 nach Rev. 106 erledigt, G31 (a) Punkt erledigt, G26b, G29, H9, L14, L16 fortgeschrieben, G32 neu, Zusammenfassung. Die Revisionen 104 bis 107 stehen an den Punkten selbst, nicht in dieser Kopfzeile). Zuvor 25.09.2026, 23:05 MESZ (Rev. 103 —',
            'ML Stand')
m = ersetze(m, '- [ ] **A8 · ⭐ Projektanweisungen Fassung 15', '- [x] **A8 · ⭐ Projektanweisungen Fassung 15', 'ML A8 Kästchen')
m = nach(m, 'Danach `Ordner_aufraeumen.ps1` (führt jetzt auch Fassung 15 in den Papierkorb).**',
         ' **✓ Erledigt 25.09., 23:47 (Rev. 106): Fassung 16 eingesetzt, Aufräumskript gelaufen, Papierkorb geleert.**', 'ML A8 Rev. 106')
m = nach(m, 'Rev. 105: Abschlusskarte als Fortschrittskarte je Wochenvideo in 4.6 ergänzt, 4.6 = 154.)*',
         ' *(Rev. 108, 26.09.: Der Satz war mit dem Speichern des Masters am 26.09. früh verloren (Befund B1, Textvorschlag 4.7 vom 26.09. § 6), per Skript mit dem Wortlaut Rev. 105 wiederhergestellt, 4.6 = 154.)*', 'ML G26b')
m = nach(m, '*(Rev. 104: (b) und (c) 4.6-Teil erledigt, im Master.)*',
         ' *(Rev. 108, 26.09.: (b) weitergeführt, 4.1 sagt nach Nr. 21 „Das Adhärenzkriterium wurde in der Hauptanalyse nicht angewandt.“, die Doppelung mit 4.7 ist aufgelöst. (a) bis (c) erledigt. Offen (d) und (e) Task 11, (f) Task 12, (g) Task 16, (h) Task 18, (i) und (j) Task 15, Einzelheiten in G32.)*', 'ML G29')
m = nach(m, '(f) `Manuskriptstand_2026-09-25.py`: Beschriftungen nur über die Formatvorlage erkennen.',
         ' *(Rev. 105: (f) erledigt, Messskript Fassung 2.)* *(Rev. 108, 26.09.: (a) Punkt nach „berechnet“ erledigt, per Skript. Offen aus (a) die Überschrift 4.4.2 ohne „(bilateral)“ und der Platzhalter Tab. 1, beides Task 18. (c) läuft in Task 7.)*', 'ML G31')
m = nach(m, 'Nach Beschaffung Klammer in 4.7 ergänzen, T1 anlegen. *(25.09., Rev. 95)*',
         ' *(Rev. 108, 26.09.: Seit Task 6 nennt 4.7 Hedges\' g ohne Beleg und ohne den Faktor J, J steht nur noch in der Anmerkung zu Tab. 3. Nach Beschaffung „(Hedges, 1981)“ hinter „Hedges\' g“ in 4.7 Absatz 3 Satz 5, +2 Wörter.)*', 'ML H9')
m = nach(m, 'Offen: (c) und (d) an den Quellen prüfen, (a) und (b) im Text umsetzen)*',
         ' *(Rev. 108, 26.09.: (a) 4.7 nennt seit Task 6 nur den Planungsstand (f = 0,25, mindestens 34 Spieler), das abweichende Planungsmodell mit Cohen (1988, Tab. 8.4.4) kommt nach 6.2 (Task 12, G32 c). (b) Task 12. (c) und (d) Task 15.)*', 'ML L14')
m = nach(m, 'Offen: die sechs Punkte für 6.2 aus Befund § 5.3 und der 5.2-Satz nach R2)*',
         ' *(Rev. 108, 26.09.: 4.7 in Task 6 neu gefasst: Prüfungen mit dem Zweck „Verletzungen erkennen“, Regel O7 knapp, „geprüft und nicht verworfen“ steht nicht mehr in 4.7 und kommt nach 5.2 (Task 11), die Freigabe ohne unabhängige Methodenprüfung nach 6.3 (Task 12), der Bootstrap bleibt als streichbares Modul. Offen: 5.2-Satz nach R2 und die sechs Punkte für 6.2, beide in G32.)*', 'ML L16')
G32 = """- [ ] **G32 · Vormerkungen aus Task 6 (4.7, 26.09., Rev. 107 und 108, Wortlaut in `04_Uebergaben\\Textvorschlag_4.7_2026-09-26.md` § 7):** (a) Task 10 (2.2): Kovariatenbegründung im Absatz „Für die vorliegende Untersuchung folgt daraus zweierlei“ streichen, sie steht in 4.7 · (b) Task 11 (5.1, 5.2): Voraussetzungen mit „geprüft und nicht verworfen“, verworfene Normalverteilung beim 30-m-Sprint mit Prüfgröße und p (R2), Bootstrap in genau einem Satz oder Halbsatz, Anmerkungen zu Tab. 2 (d, Überlappung) und Tab. 3 (J, Vorzeichen, p), H0-Entscheidung an der adjustierten Differenz, Per-Protokoll nicht als „gleiches Ergebnis“, Nr. 23 (Einzelwerte) zu Beginn entscheiden · (c) Task 12 (6.1 bis 6.3): Material aus den gestrichenen Sätzen (Wirkung des Programmangebots, Planungsmodell der Antragsrechnung, Power bei den Vorab-Erwartungen, Trennschärfe, Analyseeinheit, Familiarisierung), Argumentationslinie für 6.1 und 6.2, Familienfehler höchstens 7,5 %, Freigabe ohne unabhängige Methodenprüfung genau einmal in G7 oder G3, Restrisiko ohne Zweiterfassung in G4 oder G5 · (d) Task 13 (7): „Wirkung des Programmangebots“ · (e) Task 14 (3): H0 und H1 ergänzend und nah am Antragswortlaut, drei Zielgrößen gleichrangig · (f) Task 15 mit H9: „(Hedges, 1981)“ nach Beschaffung · (g) Task 16: Poweranalyse mit allen Eingaben, KI-Deklaration mit Mindestinhalt, Kennzeichnung jedes Skripts in Anhang G, Anhang G ohne Prüfprotokolle, Klickfrage 12 · (h) Task 18: Tab. H6 aus Auswertungsplan § 5.10 mit Spalte Grund und mit den Festlegungsdaten (Per-Protokoll-Schwelle und Mindestgruppengröße 11.09.2026, Hauptanalyse 12.09.2026, Verfasser 26.09., 20:51), Anmerkung Tab. H4c, Platzhalter in Anhang H nachziehen, Nr. 57a, Streichpaket Bootstrap als Entscheidungspunkt, Kapitel 5 bis 7 mit „Studienprotokoll“ · (i) H8: Shapiro und Wilk (1965), Brown und Forsythe (1974) optional als Klammer in 4.7 Absatz 4 · (j) Steuerdokumente mit der nächsten Revision, keine eigene Fassung: F16 § 11.7 und Berichtsraster 4.7.7 („in 4.7 mit Datum“ → Tab. H6), Berichtsraster 4.1.10 („in der Hauptanalyse nicht angewandt“), F16 § 13 neue Einträge (Bootstrap als streichbares Modul 26.09., 18:16 · Schlussabsatz nur mit Verfahren und Pflichtangaben 26.09., abends · Festlegungsdaten in Tab. H6 26.09., 20:51), übrige Punkte der Zeile „Steuerdokumente“ in § 7. *(26.09., Rev. 108)*
"""
m = ersetze(m, '- [ ] **G30 · Plan der weiteren Schritte', G32 + '- [ ] **G30 · Plan der weiteren Schritte', 'ML G32')
m = zeile(m, '| 1 Steuerdokumente (erledigt 25.09., Rev. 98) |', '| 1 Steuerdokumente (erledigt 25.09., Rev. 98) | G27f (Verfasserschritt), A8 erledigt (Rev. 106) |', 'ML Tab Task 1')
m = zeile(m, '| 6 Textrevision 4.7 auf 550 |', '| 6 Textrevision 4.7 auf 550 (erledigt 26.09., Rev. 107 und 108, 463 Wörter) | — (Vormerkungen in G32) |', 'ML Tab Task 6')
m = zeile(m, '| 7 bis 10 Kürzung 2.4, 2.3, 2.1, 2.2 |', '| 7 bis 10 Kürzung 2.4, 2.3, 2.1, 2.2 | G13g (2.2) · G26e (2.4.1, 2.4.2, 2.2) · J2 (2.4.2) · K19 und G31 (c) (2.4.1) · G32 (a) (2.2) · G18c · G19c |', 'ML Tab Tasks 7-10')
m = zeile(m, '| 11 Kapitel 5 |', '| 11 Kapitel 5 | B5 (Rest) · G25d (M11, M12) · G17g (Tab.-2-Feld) · G28g · G29 (d), (e) · G32 (b) |', 'ML Tab Task 11')
m = zeile(m, '| 12 Kapitel 6 |', '| 12 Kapitel 6 | G17d · G17f · G26l · J6 · K23 · L14 (a), (b) · L16 · G29 (f) · G32 (c) |', 'ML Tab Task 12')
m = zeile(m, '| 13 Kapitel 7, Zusammenfassung, Abstract |', '| 13 Kapitel 7, Zusammenfassung, Abstract | G25d (M16) · G32 (d) |', 'ML Tab Task 13')
m = zeile(m, '| 14 Kapitel 1, 2.5, 3 |', '| 14 Kapitel 1, 2.5, 3 | G32 (e) |', 'ML Tab Task 14')
m = zeile(m, '| 15 Literaturverzeichnis |', '| 15 Literaturverzeichnis | I7 · I8 · I9 · I12 · K19 · G17j · G28f · L14 (c), (d) · K24 (Metadaten) · G29 (i), (j) · G32 (f) |', 'ML Tab Task 15')
m = zeile(m, '| 16 Phase 8 |', '| 16 Phase 8 | L9 · G29 (g) · G26g (Skill-Stand prüfen) · G32 (g) |', 'ML Tab Task 16')
m = zeile(m, '| 18 Endredaktion |', '| 18 Endredaktion | G29 (h) · G22 (Rest) · G18, G19 (Nullstand) · G13 (Rest) · G31 (a), (b) · G32 (h), (j) |', 'ML Tab Task 18')
m = ersetze(m, '**Summe** | **33 Hauptpunkte und 35 Teilpunkte offen** (gemessen 25.09., Rev. 98',
            '**Summe** | **33 Hauptpunkte und 35 Teilpunkte offen** (Rev. 108, 26.09.: A8 und G31 (a) Punkt erledigt, G32 neu, G26b, G29, H9, L14, L16 fortgeschrieben, Zählung nicht neu erhoben. Zuvor gemessen 25.09., Rev. 98',
            'ML Summe')
schreibe('Massnahmenliste_Datenverarbeitung.md', m)

# ---------------------------------------------------------------- Plan
PL = '04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md'
p = lies(PL)
p = nach(p, 'Von Hand fortgeschrieben per Skript `03_Skripte\\Plan_Rev4_2026-09-25.py`.',
         '\n\n**Nachtrag 26.09.2026 (Rev. 108 der Sitzungsnotizen), keine neue Revision des Plans:** Task 6 erledigt, 4.7 steht mit 463 gegen 550 Wörtern im Master (Rev. 107). Die Nachkorrekturen aus Schritt 0 der Übergabe `04_Uebergaben\\Uebergabe_Kapitel2_2026-09-26.md` hat Claude auf Anweisung des Verfassers per Skript eingebaut (`03_Skripte\\Master_Schritt0_2026-09-26.py`), dazu 4.6 im Wortlaut Rev. 105 (Befund B1). Kapitel 4 ist textlich fertig. Nächster Task ist 7 (2.4 auf 700), Block C Abschnitt für Abschnitt (Verfasser 26.09.). Stand in § 1a, Vormerkungen aus Task 6 als G32 in der Maßnahmenliste.',
         'PL Nachtrag')
p = ersetze(p, '**Offen aus Block B für spätere Tasks**',
            '**Stand nach Task 6 (26.09., Rev. 108, Master 48.791 Byte, gemessen mit Fassung 2 des Messskripts):** 4.1 291 · 4.2 208 · 4.3 340 · 4.4 392 · 4.5.1 418 · 4.5.2 150 · 4.6 154 · 4.7 **463 gegen 550** · Kapitel 4 (4.1 bis 4.6) 1.953 gegen 2.000, mit 4.7 2.416 gegen 2.550 · Kapitel 2 (2.1 bis 2.4) 4.920 gegen 2.950 · Absatztext Kapitel 1 bis 7 7.336 · Kürzungsauftrag nur noch Kapitel 2 mit 1.970 · Semikola 61 und Abschnittsverweise 35, alle in Kapitel 2. Die 134 Wörter unter dem Budget von Kapitel 4 werden nicht aufgefüllt (Regel R6).\n\n**Offen aus Block B für spätere Tasks**',
            'PL § 1a')
p = nach(p, '*Prüfung:* Endabgleich (die Prozessdaten 11.09., 12.09., 15.09. bleiben), Rasterzeilen 4.7.1 bis 4.7.15 einzeln zugeordnet, Messung 550 oder weniger.',
         '\n\n*Erledigt 26.09. (Rev. 107 und 108):* 4.7 mit 463 Wörtern in sechs Absätzen im Master, Textvorschlag `Textvorschlag_4.7_2026-09-26.md` (Fassung 13 mit Nachtrag § 10), Nachkorrekturen per Skript. Die Prozessdaten stehen nach Verfasserentscheidung nicht mehr in 4.7, sondern in Tab. H6 (Task 18). Vormerkungen als G32 in der Maßnahmenliste.',
         'PL Task 6')
schreibe('Plan_Weitere_Schritte_2026-09-25.md', p)

# ---------------------------------------------------------------- Textvorschlag 4.7, § 10
TV = '04_Uebergaben/Textvorschlag_4.7_2026-09-26.md'
v = lies(TV)
NACHTRAG = """

## 10 Nachtrag Schritt 0 (26.09.2026, 21:05, Rev. 108)

Der Verfasser hatte die Nachkorrekturen aus der Übergabe Kapitel 2 § 1 angenommen, gespeichert waren sie nicht (Master 52.734 Byte, MD5 d8ca4d42…, Stand 20:21). Auf seine Anweisung vom 26.09., 20:55 („Bitte übernehme du das“) hat Claude sie per Skript eingebaut (`03_Skripte\\Master_Schritt0_2026-09-26.py`, Protokoll `.txt`):

1. 4.7 Abs. 1: „(Moher et al., 2010, S. 17)“ statt „S. 7“ (Box 6 auf S. 17 von 28, am PDF geprüft) und „laut Studienprotokoll“ statt „nach Antrag“.
2. 4.7 Abs. 2: „festgelegt nach einer ersten Auswertung“ statt „der ersten“ (Nr. 52).
3. 4.7: Voraussetzungsabsatz als Absatz 4 vor dem Sensitivitätsabsatz (Nr. 54).
4. 4.4.2: Schlusspunkt (Nr. 22).
5. 4.6: Wortlaut Rev. 105 (§ 1.2) mit „Adhärenzkriterium“ (Nr. 20), „Ethikantrag“ bleibt an beiden Stellen (Nr. 29 nicht übernommen, Klick 26.09.).
6. 4.1 Abs. 5: „Das Adhärenzkriterium wurde in der Hauptanalyse nicht angewandt.“ (Nr. 21).

Nicht übernommen: die Festlegungsdaten in Absatz 1 (Verfasser: in Tab. H6), Nr. 30 und 31, Nr. 57a (bis Task 18 offen). 4.7 hat damit die Reihenfolge von Fassung 13, Absatz 1 bleibt in der Verfasserfassung vom 26.09., 20:21 (111 Wörter, „Ergänzend“, „da“, ohne Daten). Master nach dem Einbau 48.791 Byte, MD5 e35315d6…, Messung 4.1 291 · 4.6 154 · 4.7 463 · Kapitel 4 2.416. Endabgleich: 657 Zahlen, 21 von 23 Satzprüfungen, zwei bekannte Abweichungen (SP6, SP11).
"""
v = v.rstrip('\n') + NACHTRAG
PROT.append('ergänzt: TV § 10')
schreibe('Textvorschlag_4.7_2026-09-26.md', v)

print('\n'.join(PROT))

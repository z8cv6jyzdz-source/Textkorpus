# -*- coding: utf-8 -*-
"""
Steuerung_Rev96_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 96) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task „4.7 Statistische Auswertung“, Abschluss: Plan der weiteren Schritte

Zweck: Den Auftrag des Verfassers (Prüfung von 4.7 vor weiteren Kapiteln, Plan der weiteren Schritte, Kapitel in
eigenen Tasks), die Messung des Masters und den Plan festhalten. Zählwerte liest das Skript aus der Messung
(Manuskriptstand_2026-09-25.csv), dem Plan und der Maßnahmenliste, die Prüfsumme des Masters aus der Datei.
Jede Textstelle wird genau einmal ersetzt, sonst bricht das Skript ab. Ohne Semikolon (chr(59)).
Aufruf: python Steuerung_Rev96_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md>
        <Master.docx> <Manuskriptstand_2026-09-25.csv> <Plan_Weitere_Schritte_2026-09-25.md>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import csv
import hashlib

SN, ML, MASTER, CSVP, PLAN = sys.argv[1:6]
SEMI = chr(59)


def tsd(n):
    return format(int(n), ',').replace(',', '.')


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


b = open(MASTER, 'rb').read()
sha_master, gr_master = hashlib.sha256(b).hexdigest(), len(b)
rows = {r['nr']: r for r in csv.DictReader(open(CSVP, encoding='utf-8'))}
BUDGET = {'1': 600, '2.1': 800, '2.2': 850, '2.3': 600, '2.4': 700, '2.5': 400, '3': 200,
          '4.1': 300, '4.2': 215, '4.3': 340, '4.4': 420, '4.5.1': 420, '4.5.2': 150, '4.6': 155, '4.7': 720,
          '5.1': 230, '5.2': 220, '6.1': 700, '6.2': 400, '6.3': 500, '7': 250}
UNTER = {'2.4': ['2.4.1', '2.4.2', '2.4.3'], '4.4': ['4.4.1', '4.4.2', '4.4.3']}


def feld(nr, name):
    n = int(rows[nr][name])
    for u in UNTER.get(nr, []):
        n += int(rows[u][name])
    return n


ist = {k: feld(k, 'woerter') for k in BUDGET}
geschrieben = sum(ist.values())
leer = [k for k in BUDGET if ist[k] == 0]
budget_leer = sum(BUDGET[k] for k in leer)
kuerzung = geschrieben + budget_leer - 9000
k2 = sum(ist[k] for k in ['2.1', '2.2', '2.3', '2.4']) - 2950
k4 = sum(ist[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.5.1', '4.5.2', '4.6', '4.7']) - 2550
semi = sum(feld(k, 'semikola') for k in BUDGET)
verw = sum(feld(k, 'abschnittsverweise') for k in BUDGET)
s40 = sum(feld(k, 'saetze_ueber_40') for k in BUDGET)
if k2 + k4 != kuerzung:
    raise SystemExit('Budgetarithmetik geht nicht auf')
plan = open(PLAN, encoding='utf-8').read()
w_plan = len(plan.split())
if 'siebzehn Tasks' not in plan or 'Klickfrage 13' not in plan:
    raise SystemExit('Plan entspricht nicht dem erwarteten Stand')
ml = open(ML, encoding='utf-8').read()
offen_haupt = sum(1 for z in ml.split('\n') if z.startswith('- [ ]'))
offen_teil = sum(1 for z in ml.split('\n') if z.lstrip().startswith('- [ ]') and not z.startswith('- [ ]'))

ZEIT = '21:05 MESZ'
# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 95 — siehe Block oben.) Zuvor: (Rev. 94 — siehe Block oben.)',
            '**Stand: (Rev. 96 — siehe Block oben.) Zuvor: (Rev. 95 — siehe Block oben.) Zuvor: (Rev. 94 — siehe Block oben.)')
REV96 = '''### ⭐⭐ NEU (Rev. 96, 25.09.2026, %(zeit)s): Plan der weiteren Schritte — Verfasserauftrag „erst prüfen, dann Plan, weitere Kapitel in eigenen Tasks“, Master gemessen, siebzehn Tasks in fünf Blöcken, dreizehn Klickfragen gesammelt

**Auftrag (Verfasser, 25.09., Klickantwort als Freitext auf die Frage nach Kapitel 5):** „Bevor weitere Kapitel erarbeitet werden, erstmal prüfen durch mich und du einen Plan machen für weitere Schritte. Weitere Kapitel in anderen Tasks.“ Kein Kapiteltext mehr in diesem Task, Master unverändert (SHA-256 %(sha)s…, %(gr)s Byte).

**(1) Messung des Masters** `03_Skripte\\Manuskriptstand_2026-09-25.py` (.txt, .csv): Absatztext Kapitel 1 bis 7 **%(geschrieben)s Wörter**, leere Abschnitte (1, 2.5, 3, 5.1, 5.2, 6.1 bis 6.3, 7) mit %(budget_leer)s Wörtern Budget, bei Einhaltung aller Budgets %(summe)s gegen 9.000. **Kürzungsauftrag %(kuerzung)s Wörter** (Kapitel 2 %(k2)s gegen 2.950, Kapitel 4 %(k4)s gegen 2.550, darin 170 aus der Anhebung von 4.7). Bestand: %(semi)s Semikola außerhalb von Zitierklammern, %(verw)s nummerierte Abschnittsverweise, %(s40)s Sätze über 40 Wörter (Satzteiler des Messskripts, fast alle in Kapitel 2), 8 Platzhalter (4.3, Anhang H), 1 Marker (4.4). Kapitel-4-Zahlen wie Rev. 95.

**(2) Plan** `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (%(wplan)s Wörter, Erzeuger `03_Skripte\\Plan_Weitere_Schritte_2026-09-25.py`, Projektkopie `claude/`), ersetzt die Zeile „Nächste Schritte“ aus Rev. 95 und die Reihenfolge im Nachtrag 5 der Übergabe Textrevision. Inhalt: § 0 Kurzfassung · § 1 gemessener Stand je Abschnitt · § 2 Schritt 0, Prüfung von 4.7 durch den Verfasser (acht Sätze, die nur er bestätigen kann, Rückmeldeweg A direkt in Word mit Diff-Skript im Folgetask, B Freitext oder Klick, Kommentare nicht empfohlen) · § 3 siebzehn Tasks in fünf Blöcken — A Steuerung (Task 1: Fassung 15, I19, Maßnahmenliste bereinigen, Archiv) · B Kapitel 5, Kapitel 6, Kapitel 7 mit Zusammenfassung und Abstract (Tasks 2 bis 4) · C Textrevision 4.3, 4.4, 4.5.2 mit 4.6, 4.1 mit 4.5.1 (Tasks 5 bis 8) · D Kürzung 2.4, 2.3, 2.1, 2.2, dann Kapitel 1, 2.5 und 3 (Tasks 9 bis 13) · E Literaturverzeichnis, Phase 8, Anhänge A bis F, Endredaktion (Tasks 14 bis 17), je Task Ziel, Eingang, Budget, Klickpunkte, Ausgang, Prüfung · § 4 Begründung der Reihenfolge (Ergebnis vor Revision, Ankersatz aus 6.1, Kapitel 2 nach 6.1, Steuerung zuerst) · § 5 Budgetarithmetik mit **Empfehlung zur Gegenfinanzierung der 170 Wörter von 4.7 innerhalb von Teil A** (4.3 320, 4.5.2 130, 5.1 220, 5.2 200, 6.1 660, 6.2 380, 6.3 480, Kapitel 1 580) — weicht von der Klickentscheidung „4.3 und 4.5.2“ ab, weil 4.5.2 unter dem Rasterwert 130 und 4.3 mit acht P-Zeilen und G29 (a) die 170 nicht tragen, Klickfrage 2 · § 6 Bereinigungsvorschlag für die Maßnahmenliste (%(haupt)s Hauptpunkte und %(teil)s Teilpunkte offen, 32 Hauptpunkte erledigt oder gegenstandslos, Zuordnung der Teilpunkte zu den Tasks) · § 7 dreizehn Klickfragen mit Empfehlung, Beschaffungsfolgen, Betreuer (nur Fußnotenfrage) · § 8 Startsätze je Task · § 9 Prüfung.

**Regeln eingehalten:** kein Manuskripttext, Master unverändert, alle Zahlen gemessen oder gerechnet (Skripte ohne Semikolon, Abbruch bei Nichtaufgehen), Blindordner, Abgabe, Datenstand und Workbook unverändert.

**Dateien (Ordner):** `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` · `03_Skripte\\Manuskriptstand_2026-09-25.py/.txt/.csv` · `03_Skripte\\Plan_Weitere_Schritte_2026-09-25.py` · `03_Skripte\\Steuerung_Rev96_2026-09-25.py`. Projektkopien: Plan, Sitzungsnotizen, Maßnahmenliste.

**Nächste Schritte (ersetzt Rev. 95):** (0) Verfasser prüft 4.7 in Word (Plan § 2), Rückmeldung nach § 2.3 · (1) Task 1 „Steuerdokumente und Bereinigung“ mit dem Startsatz aus Plan § 8, zu Beginn Klickfragen 1 bis 3 (Reihenfolge, Gegenfinanzierung, Bereinigungsliste), Fassung 15 einsetzen (A8) · (2) Task 2 „Kapitel 5“ erst nach der Prüfung von 4.7 · danach die Tasks 3 bis 17 nach Plan § 3. Beim Betreuer offen bleibt nur die Fußnotenfrage.

''' % dict(zeit=ZEIT, sha=sha_master[:8], gr=tsd(gr_master), geschrieben=tsd(geschrieben), budget_leer=tsd(budget_leer),
           summe=tsd(geschrieben + budget_leer), kuerzung=tsd(kuerzung), k2=tsd(k2), k4=tsd(k4), semi=semi, verw=verw,
           s40=s40, wplan=tsd(w_plan), haupt=offen_haupt, teil=offen_teil)
if SEMI in REV96:
    raise SystemExit('Semikolon im Rev.-96-Block')
s = ersetze(s, '### ⭐⭐ NEU (Rev. 95, 25.09.2026, 20:20 MESZ): Task „4.7 Statistische Auswertung“',
            REV96 + '### ⭐⭐ NEU (Rev. 95, 25.09.2026, 20:20 MESZ): Task „4.7 Statistische Auswertung“')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = ml
m = ersetze(m, '**Stand 25.09.2026, 20:20 MESZ (Rev. 95 — 4.7 Statistische Auswertung im Master',
            '**Stand 25.09.2026, %s (Rev. 96 — Plan der weiteren Schritte `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (siebzehn Tasks, dreizehn Klickfragen, Bereinigungsvorschlag § 6), Master gemessen (%s Wörter, Kürzungsauftrag %s), G30 neu, G16c erledigt, L9 fortgeschrieben. Zuvor 25.09.2026, 20:20 MESZ (Rev. 95 — 4.7 Statistische Auswertung im Master' % (ZEIT, tsd(geschrieben), tsd(kuerzung)))
# G16c erledigt
m = ersetze(m, '  - [ ] **G16c · Übergaben für Kapitel 5, 6, 7 beim Anlegen mit Bauplan § 2.3–2.5 und Skill 4a bestücken**',
            '  - [x] **G16c · Übergaben für Kapitel 5, 6, 7 beim Anlegen mit Bauplan § 2.3–2.5 und Skill 4a bestücken** — erledigt 25.09. (Rev. 96): Plan § 3, Tasks 2 bis 4.')
# L9
m = ersetze(m, 'Offen: KI-Deklaration und Nutzungsprotokoll, Anhang G mit Prüfprotokollen, Poweranalyse-Eingaben, R-Skripten und Diagrammen, Reproduktionstest)*',
            'Offen: KI-Deklaration und Nutzungsprotokoll, Anhang G mit Prüfprotokollen, Poweranalyse-Eingaben, R-Skripten und Diagrammen, Reproduktionstest)* *(Rev. 96, 25.09.: als Task 15 im Plan der weiteren Schritte, Umfang von Anhang G ist Klickfrage 11)*')
# G30 neu nach G29
G30 = ('- [ ] **G30 · Plan der weiteren Schritte (25.09., Rev. 96):** `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` — siebzehn Tasks in fünf Blöcken (Steuerung · Kapitel 5, 6, 7 · Textrevision Kapitel 4 · Kürzung Kapitel 2, dann 1, 2.5, 3 · Literaturverzeichnis, Phase 8, Anhänge, Endredaktion), '
       'dreizehn Klickfragen (§ 7.1), Empfehlung zur Gegenfinanzierung der 170 Wörter von 4.7 innerhalb von Teil A (§ 5, Klickfrage 2), Bereinigungsvorschlag für diese Liste (§ 6: %d Hauptpunkte und %d Teilpunkte offen, 32 Hauptpunkte zu schließen, Klickfrage 3). '
       'Schritt 0 beim Verfasser: 4.7 in Word prüfen (§ 2). Nächster Task: Task 1 „Steuerdokumente und Bereinigung“ mit dem Startsatz aus § 8. Messung des Masters in `03_Skripte\\Manuskriptstand_2026-09-25.txt` (%s Wörter Absatztext, Kürzungsauftrag %s). *(25.09., Rev. 96)*' % (offen_haupt, offen_teil, tsd(geschrieben), tsd(kuerzung)))
if SEMI in G30:
    raise SystemExit('Semikolon in G30')
m = ersetze(m, '\n\n## H  BESCHAFFUNG — teils blockierend für die Begründung', '\n' + G30 + '\n\n## H  BESCHAFFUNG — teils blockierend für die Begründung')
m = ersetze(m, '| **Summe** | **57 offen** (Stand 25.09., Rev. 95: G29 und H9 neu, L9, L16 und I19 fortgeschrieben — Zählung nicht neu erhoben.',
            '| **Summe** | **57 offen** (Stand 25.09., Rev. 96: gemessen %d Hauptpunkte und %d Teilpunkte mit offenem Kästchen, G30 neu, G16c erledigt — Bereinigung nach Plan § 6 in Task 1. Stand 25.09., Rev. 95: G29 und H9 neu, L9, L16 und I19 fortgeschrieben — Zählung nicht neu erhoben.' % (offen_haupt + 1, offen_teil - 1))
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
print('Sitzungsnotizen Rev. 96 und Maßnahmenliste fortgeschrieben: Master %d Wörter, Kürzung %d, Plan %d Wörter, offen %d/%d' % (
    geschrieben, kuerzung, w_plan, offen_haupt, offen_teil))

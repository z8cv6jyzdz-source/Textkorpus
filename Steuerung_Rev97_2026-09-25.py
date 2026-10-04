# -*- coding: utf-8 -*-
"""
Steuerung_Rev97_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 97) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Abschluss des Tasks 4.7: drei Verfasserentscheidungen zum Plan, Plan Rev. 2,
Bereinigung der Maßnahmenliste, Übergabe Steuerdokumente

Zählwerte liest das Skript aus dem Bereinigungsprotokoll, der Maßnahmenliste, dem Plan und der Messung. Jede Textstelle
wird genau einmal ersetzt, sonst Abbruch. Ohne Semikolon (chr(59)).
Aufruf: python Steuerung_Rev97_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md>
        <Massnahmenliste_Bereinigung_2026-09-25.txt> <Plan_Weitere_Schritte_2026-09-25.md> <Manuskriptstand_2026-09-25.txt>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

SN, ML, BER, PLAN, MS = sys.argv[1:6]
SEMI = chr(59)


def tsd(n):
    return format(int(n), ',').replace(',', '.')


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


ber = open(BER, encoding='utf-8').read()
m = re.search(r'Geschlossen: (\d+) Hauptpunkte, (\d+) Teilpunkte\nDanach offen: (\d+) Hauptpunkte, (\d+) Teilpunkte', ber)
g_h, g_t, o_h, o_t = [int(x) for x in m.groups()]
plan = open(PLAN, encoding='utf-8').read()
if 'Rev. 2' not in plan[:200] or 'achtzehn Tasks' not in plan:
    raise SystemExit('Plan ist nicht Rev. 2')
w_plan = len(plan.split())
ms = open(MS, encoding='utf-8').read()
geschrieben = int(re.search(r'Absatztext Kapitel 1 bis 7 gesamt: (\d+)', ms).group(1))
k47 = int(re.search(r'\n4\.7\s+4\.7 Statistische Auswertung\s+(\d+)', ms).group(1))
budget_leer = int(re.search(r'Budget der ungeschriebenen Abschnitte: (\d+)', ms).group(1))
kuerzung = geschrieben + budget_leer - 9000
ml = open(ML, encoding='utf-8').read()
if sum(1 for z in ml.split('\n') if z.startswith('- [ ]')) != o_h:
    raise SystemExit('Maßnahmenliste passt nicht zum Bereinigungsprotokoll')

ZEIT = '21:40 MESZ'
# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 96 — siehe Block oben.) Zuvor: (Rev. 95 — siehe Block oben.)',
            '**Stand: (Rev. 97 — siehe Block oben.) Zuvor: (Rev. 96 — siehe Block oben.) Zuvor: (Rev. 95 — siehe Block oben.)')
REV97 = '''### ⭐⭐ NEU (Rev. 97, 25.09.2026, %(zeit)s): Drei Verfasserentscheidungen zum Plan — Vorgabe gilt (4.7 zurück auf 550), Kürzung vor Neuem, Anhänge zuletzt · Plan Rev. 2 · Maßnahmenliste bereinigt · Übergabe „Steuerdokumente“ mit Prompt

**Verfasserantworten auf Rev. 1 des Plans (25.09., abends, Freitext):** (1) Zur nicht gegenfinanzierten Anhebung von 4.7: „das ist schlecht. Wir müssen zukünftig bei der Vorgabe bleiben“ — gelesen als: Die Budgets nach F14 § 5.2 sind verbindlich, keine Anhebung, keine Gegenfinanzierung, also gilt auch für 4.7 das Budget 550. Die per Klick angenommenen %(k47)s Wörter werden in einem eigenen Task auf 550 zurückgeführt (Plan Task 6, Weg in Plan § 5: restliche Kürzungsleiter rund 100 Wörter auf 621, dann rund 70 Wörter durch Verschieben nach 6.2 und Tab. H4, Vorschlagsliste mit Zielort je Satz). Neue Regel für alle Tasks: kein Textvorschlag über dem Budget seines Abschnitts. Die Klickentscheidung „Gegenfinanzierung in 4.3 und 4.5.2“ und die Empfehlung aus Rev. 1 (Verteilung auf Kapitel 1, 5, 6) sind hinfällig. (2) Zur Maßnahmenliste: „Bitte aktualisieren“, dazu „einen Prompt schreiben, der für einen neuen Task genutzt werden kann, um die Dokumente zu aktualisieren“. (3) Zu den Anhängen: „kommen ganz zum Schluss oder brauchst du die bereits“ — Antwort: nicht vorher gebraucht, ganz zum Schluss vor der Endredaktion. Und: „zunächst die vorhandenen Kapitel bearbeiten, bevor weitere Kapitel verfasst werden, eine Kürzung der vorhandenen Kapitel hat Priorität“.

**(1) Plan Rev. 2** (`04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md`, %(wplan)s Wörter, Erzeuger `03_Skripte\\Plan_Weitere_Schritte_2026-09-25.py` mit Vorlage `Plan_Weitere_Schritte_2026-09-25_Vorlage.md`, Projektkopie): achtzehn Tasks in fünf Blöcken — A Steuerdokumente (1) · B Textrevision Kapitel 4: 4.3, 4.4, 4.5.2 mit 4.6, 4.1 mit 4.5.1, 4.7 auf 550 (2 bis 6) · C Kürzung 2.4, 2.3, 2.1, 2.2 (7 bis 10) · D Kapitel 5, 6, 7 mit Zusammenfassung, dann 1, 2.5, 3 (11 bis 14) · E Literaturverzeichnis, Phase 8, Anhänge A bis F, Endredaktion (15 bis 18). Budgets als Vorgabe (Kürzungsauftrag %(kuerzung)s Wörter bei %(geschrieben)s Wörtern Bestand, Kapitel 2 −1.970, Kapitel 4 −1.177, darin 4.7 −%(k47diff)s). Vormerkungen aus den Kapiteln 5 und 6 für Kapitel 4 und 2 werden gesammelt und in der Endredaktion in einem Durchgang eingearbeitet. Klickfragen 1 bis 3 beantwortet, 4 bis 14 an den Tasks. Rev. 1 ist ersetzt.

**(2) Maßnahmenliste bereinigt** (`03_Skripte\\Massnahmenliste_Bereinigung_2026-09-25.py`, Protokoll `.txt`): %(g_h)s Hauptpunkte und %(g_t)s Teilpunkte mit Datum und Grund auf erledigt oder gegenstandslos gesetzt (Kästchen, Vermerk am Zeilenende, nichts gelöscht), Zuordnung der offenen Punkte zu den Tasks des Plans in der Zusammenfassung eingetragen. Offen jetzt %(o_h)s Hauptpunkte und %(o_t)s Teilpunkte, zuvor 65 und 46 gemessen.

**(3) Übergabe** `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md` (Projektkopie): Prompt für Task 1 mit sechs Schritten — Vorprüfung und Diff von 4.7, Fassung 15 per Skript aus Fassung 14 mit Änderungsliste je Paragraf (Auswertung abgeschlossen, Kennzahlenblatt 25.09., keine Kennungen im Manuskript, Vorgabe-Regel, Reihenfolge, Kennwerte in 4.2, § 3 und § 11.2a ohne Ergebniszahlen, R 4.3.3, § 13 Nr. 10 bis 14, Errata E1 bis E5), Vergleichsskript mit vier Prüfungen, README „Was wo gilt“, Archivkopien, Steuerung, Klickfrage A8.

**Regeln eingehalten:** kein Manuskripttext, Master unverändert, Zahlen gemessen oder gerechnet (Skripte ohne Semikolon), Blindordner, Abgabe, Datenstand und Workbook unverändert.

**Dateien (Ordner):** `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) · `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md` · `03_Skripte\\Plan_Weitere_Schritte_2026-09-25.py` mit `_Vorlage.md` · `03_Skripte\\Massnahmenliste_Bereinigung_2026-09-25.py/.txt` · `03_Skripte\\Steuerung_Rev97_2026-09-25.py`. Projektkopien: Plan, Übergabe, Sitzungsnotizen, Maßnahmenliste.

**Nächste Schritte (ersetzt Rev. 96):** (0) Verfasser prüft 4.7 in Word (Plan § 2), Rückmeldung nach § 2.3 · (1) Task 1 „Steuerdokumente“ mit dem Startsatz aus `Uebergabe_Steuerdokumente_2026-09-25.md`, am Ende Fassung 15 einsetzen (A8) · (2) Task 2 Textrevision 4.3 · danach Tasks 3 bis 18 nach Plan § 3. Beim Betreuer offen bleibt nur die Fußnotenfrage.

''' % dict(zeit=ZEIT, k47=tsd(k47), k47diff=tsd(k47 - 550), wplan=tsd(w_plan), kuerzung=tsd(kuerzung), geschrieben=tsd(geschrieben),
           g_h=g_h, g_t=g_t, o_h=o_h, o_t=o_t)
if SEMI in REV97:
    raise SystemExit('Semikolon im Rev.-97-Block')
if ('**Kürzungsauftrag** | **%s**' % tsd(kuerzung)) not in plan:
    raise SystemExit('Kürzungsauftrag im Plan weicht ab')
s = ersetze(s, '### ⭐⭐ NEU (Rev. 96, 25.09.2026, 21:05 MESZ): Plan der weiteren Schritte',
            REV97 + '### ⭐⭐ NEU (Rev. 96, 25.09.2026, 21:05 MESZ): Plan der weiteren Schritte')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
ml = ersetze(ml, '**Stand 25.09.2026, 21:05 MESZ (Rev. 96 — Plan der weiteren Schritte',
             '**Stand 25.09.2026, %s (Rev. 97 — Verfasserentscheidungen: Vorgabe gilt (4.7 zurück auf 550), Kürzung vor Neuem, Anhänge zuletzt. Plan Rev. 2 (achtzehn Tasks), Maßnahmenliste bereinigt (%d Hauptpunkte und %d Teilpunkte geschlossen, offen %d und %d, Zuordnung zu den Tasks in der Zusammenfassung), Übergabe Steuerdokumente mit Prompt. Zuvor 25.09.2026, 21:05 MESZ (Rev. 96 — Plan der weiteren Schritte' % (ZEIT, g_h, g_t, o_h, o_t))
G30_ALT = '- [ ] **G30 · Plan der weiteren Schritte (25.09., Rev. 96):**'
G30_NEU = ('- [ ] **G30 · Plan der weiteren Schritte (25.09., Rev. 96, Rev. 2 des Plans mit Rev. 97):** *(Rev. 97: Plan Rev. 2 nach Verfasserentscheidungen — Vorgabe gilt, 4.7 zurück auf 550 (Task 6), Kürzung der vorhandenen Kapitel vor neuen Kapiteln (Tasks 2 bis 10 vor 11 bis 14), Anhänge A bis F als Task 17 vor der Endredaktion, achtzehn Tasks, Bereinigung ausgeführt, Task 1 mit eigener Übergabe `Uebergabe_Steuerdokumente_2026-09-25.md`. Nächster Task: Task 1 nach Prüfung von 4.7 durch den Verfasser.)* Ursprünglich (Rev. 96):')
ml = ersetze(ml, G30_ALT, G30_NEU)
ml = ersetze(ml, '| **Summe** | **57 offen** (Stand 25.09., Rev. 96: gemessen 65 Hauptpunkte und 46 Teilpunkte mit offenem Kästchen, G30 neu, G16c erledigt — Bereinigung nach Plan § 6 in Task 1.',
             '| **Summe** | **%d Hauptpunkte und %d Teilpunkte offen** (gemessen 25.09., Rev. 97, nach der Bereinigung: %d Hauptpunkte und %d Teilpunkte geschlossen, Zuordnung zu den Tasks des Plans oben. Zuvor: Stand 25.09., Rev. 96: gemessen 65 Hauptpunkte und 46 Teilpunkte mit offenem Kästchen, G30 neu, G16c erledigt — Bereinigung nach Plan § 6 in Task 1.' % (o_h, o_t, g_h, g_t))
if SEMI in G30_NEU:
    raise SystemExit('Semikolon in G30')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(ml)
print('Rev. 97 geschrieben: geschlossen %d/%d, offen %d/%d, Plan %d Wörter, 4.7 %d' % (g_h, g_t, o_h, o_t, w_plan, k47))

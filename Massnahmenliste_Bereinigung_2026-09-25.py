# -*- coding: utf-8 -*-
"""
Massnahmenliste_Bereinigung_2026-09-25.py — Bereinigung der Maßnahmenliste nach Plan § 6 (Verfasser 25.09.: „Bitte aktualisieren“)
Bachelorarbeit U15-Plyometrie · DSHS Köln

Setzt die im Plan der weiteren Schritte § 6 genannten Haupt- und Teilpunkte mit Datum und Grund auf erledigt oder
gegenstandslos (Kästchen [x], Vermerk am Zeilenende, nichts wird gelöscht), trägt die Zuordnung der offenen Punkte zu
den Tasks des Plans (Rev. 2) ein und zählt die offenen Kästchen neu. Jede Zeile wird genau einmal gefunden, sonst
Abbruch. Ohne Semikolon (chr(59)). Aufruf: python Massnahmenliste_Bereinigung_2026-09-25.py <Massnahmenliste.md> <Protokoll.txt>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

ML, OUT = sys.argv[1], sys.argv[2]
SEMI = chr(59)
DATUM = '25.09. (Rev. 97, Plan § 6, Verfasser „Bitte aktualisieren“)'

HAUPT = {
    'A2': 'erledigt %s: Verfasserentscheidung nach F14 § 13, keine primäre Zielgröße (Antrag)',
    'A3': 'erledigt %s: Verfasserentscheidung nach F14 § 13, Hedges\' g nach O3',
    'A4': 'erledigt %s: Verfasserentscheidung nach F14 § 13, ITT und Per-Protokoll nach § 11.7',
    'A5': 'erledigt %s: in F14 § 10 (ITT-Sprachregelung) und § 11.7 aufgenommen',
    'A6': 'erledigt %s: Post-Termine vorbei (10.09., 14.09.), Versuchszahlen in K-11',
    'A7': 'erledigt %s: Post-Termine vorbei, Versuchszahlen in K-11',
    'C10': 'erledigt %s: Rückfragen beantwortet, mündliche Auskünfte bleiben Vermerk',
    'C11': 'gegenstandslos %s: Adhärenz kommt aus S07 der Blindrechnung, das Workbook ist eingefroren',
    'D5': 'erledigt %s: Voraussetzungsprüfungen in S14 der Blindrechnung (K-07), Regel O7',
    'E1': 'erledigt %s: Hauptanalyse S13 der Blindrechnung (K-06)',
    'E2': 'erledigt %s: Ausgaben nach Spezifikation S13 und S15, Tab. 3 und Tab. H4 (K-06)',
    'E3': 'gegenstandslos %s: 505 als Seitenmittel nach Antrag, keine getrennten Modelle (F14 § 11.2)',
    'F1': 'gegenstandslos %s: COD-Defizit entfällt (F14 § 2, § 11.2)',
    'F2': 'erledigt %s: Familiarisierung als dritte Kovariate in S17 (K-08), Variante a nur beschreibend',
    'F5': 'erledigt %s: Per-Protokoll-Vergleich S16 der Blindrechnung (K-08)',
    'F6': 'erledigt %s: Mittelwert-Variante in S17 der Blindrechnung (K-08)',
    'G4': 'erledigt %s: Plausibilitätsprotokoll 25.09. (Auswertungsverfahren 6.4, Nenner gegen Teilnehmerfluss)',
    'H2': 'gegenstandslos %s: Lord (1967) gestrichen (F14 § 6.5, § 15)',
    'I11': 'gegenstandslos %s: Zahlen in überholten Fassungen, maßgeblich ist das Kennzahlenblatt 25.09. (Zahlenregel), F14 § 3 führt keine Zahlen',
    'I16': 'gegenstandslos %s: Sitzungsnotizen und Statistik-Lehrgang sind keine Zahlenquelle (Zahlenregel), Kennzahlenblatt 25.09. maßgeblich',
    'I17': 'gegenstandslos %s: Statistik-Lehrgang ist keine Zahlenquelle, Bestwert-Bias gemessen in K-11 und Tab. H1d',
    'K4': 'gegenstandslos %s: die Darstellungspipeline ist überholt (Umfangsdokument § 4), Objekte per R-Skript',
    'K21': 'gegenstandslos %s: alle Messgütewerte kommen aus der Blindrechnung (K-05), keine Fassung führt Zahlen',
    'J3': 'erledigt %s: F14 § 6.4 (Betreuung kein Distanzmaß) und § 12 G4 (Altmann 0,04 s)',
    'J4': 'zusammengelegt %s mit H6 (Clemente et al., 2022)',
    'J5': 'gegenstandslos %s: keine Betreuervorlage seit dem 24.09. (F14 § 13)',
    'K9': 'gegenstandslos %s: keine Betreuervorlage seit dem 24.09. (F14 § 13)',
    'K17': 'gegenstandslos %s: keine Betreuervorlage seit dem 24.09. (F14 § 13)',
    'K7': 'gegenstandslos %s: Objekte entstehen per R-Skript aus der Ergebnisdatei (L19), die Pipeline ist überholt',
    'K8': 'erledigt %s: Termin vorbei, Versuchszahl in K-11',
    'K10': 'erledigt %s: Hauptordner enthält nur README und Skript (Ordnerliste 25.09.)',
    'K12': 'erledigt %s: 4.1 nennt keine Termine mehr, Clusterebene in K-01.24 und Abb. 1',
}
TEIL = {
    'G16d': 'erledigt %s: Klick 5 der Gliederung v4, Unterbudgets in F14 § 5.2 und Plan § 5',
    'G17a': 'erledigt %s: 4.2 steht im Master (Rev. 12/13, 208 Wörter)',
    'G26a': 'erledigt %s: ITT-Wortlaut in 4.7 (Rev. 95)',
    'G26k': 'erledigt %s: Klick 5 der Gliederung v4',
    'G28a': 'erledigt %s: Programmkennzahlen_2026-09-23 liegen vor und sind Zahlenquelle (F14 § 1.2)',
    'G27e': 'gegenstandslos %s: TREND wird im Manuskript nicht genannt (Verfasser 23.09., F14 § 4)',
}

ZUORDNUNG = '''**Zuordnung der offenen Punkte zu den Tasks des Plans (`04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md`, Rev. 2 vom 25.09., Kürzung zuerst):**

| Task | Offene Punkte |
|---|---|
| 1 Steuerdokumente (`Uebergabe_Steuerdokumente_2026-09-25.md`) | I19 · G26i · G26j · G27a · G27b · G25f, G17g, G27f (Verfasserschritte) |
| 2 Textrevision 4.3 | G13b (4.3-Teil) · G13c (Klick) · G13d · G13f (Klick) · G14 (b) · G16b (Klick) · G17h · G22 · G25c (M10) · G26d · G29 (a) · G18b, G19b (4.3) |
| 3 Textrevision 4.4 | G11 (b) · G13a · G13b (4.4-Teil) · J2 (4.4.2) · K24 (Kennzeichnung) · G22 · G29 (c) · G18b, G19b (4.4) |
| 4 Textrevision 4.5.2 und 4.6 | C12 · G15 · G17c · G26b · G29 (c) · G18b, G19b (4.5.2, 4.6) |
| 5 Textrevision 4.1 und 4.5.1 | G23 (prüfen) · G25c (M17, M18) · G28h · G29 (b) |
| 6 Textrevision 4.7 auf 550 | Kürzungsleiter K1 bis K14 (Textvorschlag 4.7 § 2) · Auslagerung nach 6.2 (L14 a) und Tab. H4 |
| 7 bis 10 Kürzung 2.4, 2.3, 2.1, 2.2 | G13g (2.2) · G26e (2.4.1, 2.4.2, 2.2) · J2 (2.4.2) · G18c · G19c |
| 11 Kapitel 5 | B5 (Rest) · G25d (M11, M12) · G17g (Tab.-2-Feld) · G28g · G29 (d), (e) |
| 12 Kapitel 6 | G17d · G17f · G26l · J6 · K23 · L14 (b) · L16 · G29 (f) |
| 13 Kapitel 7, Zusammenfassung, Abstract | G25d (M16) |
| 14 Kapitel 1, 2.5, 3 | — |
| 15 Literaturverzeichnis | I7 · I8 · I9 · I12 · K19 · G17j · G28f · L14 (c), (d) · K24 (Metadaten) · G29 (i) |
| 16 Phase 8 | L9 · G29 (g) · G26g (Skill-Stand prüfen) |
| 17 Anhänge A bis F | G28d · C13 (Verfasser) |
| 18 Endredaktion | G29 (h) · G22 (Rest) · G18, G19 (Nullstand) · G13 (Rest) |
| Beschaffung (Verfasser, neben den Tasks) | H4 · H5 · H6 · H8 · H9 · K18 · K24 |

'''

m = open(ML, encoding='utf-8').read()
zeilen = m.split('\n')
protokoll = []


def schliesse(kennung, grund, teil):
    treffer = []
    for i, z in enumerate(zeilen):
        if teil:
            ok = z.startswith('  ') and z.lstrip().startswith('- [ ] **' + kennung + ' ')
        else:
            ok = z.startswith('- [ ] **' + kennung + ' ')
        if ok:
            treffer.append(i)
    if len(treffer) != 1:
        raise SystemExit('Punkt nicht genau einmal offen: %s (%d)' % (kennung, len(treffer)))
    i = treffer[0]
    text = grund % DATUM
    zeilen[i] = zeilen[i].replace('- [ ] **' + kennung + ' ', '- [x] **' + kennung + ' ', 1).rstrip() + ' ✅ ' + text
    protokoll.append('%s → %s' % (kennung, text))


for k, g in HAUPT.items():
    schliesse(k, g, False)
for k, g in TEIL.items():
    schliesse(k, g, True)
m = '\n'.join(zeilen)
anker = '## Zusammenfassung nach Dringlichkeit\n\n'
if m.count(anker) != 1:
    raise SystemExit('Anker der Zusammenfassung nicht genau einmal gefunden')
m = m.replace(anker, anker + ZUORDNUNG)
offen_haupt = sum(1 for z in m.split('\n') if z.startswith('- [ ]'))
offen_teil = sum(1 for z in m.split('\n') if z.lstrip().startswith('- [ ]') and not z.startswith('- [ ]'))
erl_haupt = sum(1 for z in m.split('\n') if z.startswith('- [x]'))
erl_teil = sum(1 for z in m.split('\n') if z.lstrip().startswith('- [x]') and not z.startswith('- [x]'))
if SEMI in ZUORDNUNG or any(SEMI in v for v in list(HAUPT.values()) + list(TEIL.values())):
    raise SystemExit('Semikolon im neuen Text')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('Bereinigung der Maßnahmenliste am 25.09.2026 (Rev. 97)\n')
    f.write('Geschlossen: %d Hauptpunkte, %d Teilpunkte\n' % (len(HAUPT), len(TEIL)))
    f.write('Danach offen: %d Hauptpunkte, %d Teilpunkte. Erledigt gesamt: %d Hauptpunkte, %d Teilpunkte\n\n' % (offen_haupt, offen_teil, erl_haupt, erl_teil))
    f.write('\n'.join(protokoll) + '\n')
print('Bereinigt: %d Haupt- und %d Teilpunkte geschlossen, offen jetzt %d / %d' % (len(HAUPT), len(TEIL), offen_haupt, offen_teil))

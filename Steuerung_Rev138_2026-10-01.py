# -*- coding: utf-8 -*-
"""
Steuerung_Rev138_2026-10-01.py — Rev. 138 in Teil 0 der Sitzungsnotizen einsetzen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Zuspitzung der Einleitung von Aloui et al. (2022), Auftrag 01.10., 07:42 Sitzungsuhr

Setzt den Block Rev. 138 über den obersten Block und ergänzt die Standzeile. Bricht ab, wenn der oberste Block oder die
Standzeile nicht Rev. 137 ist (parallele Sitzungen) oder Rev. 138 schon besteht. Der übrige Inhalt bleibt byte-gleich (geprüft).
Aufruf: python Steuerung_Rev138_2026-10-01.py <Cowork_Sitzungsnotizen.md> <Ausgabe.md> <Uhrzeit Sitzungsuhr>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import hashlib

SRC, OUT, UHR = sys.argv[1:4]
SEMI = chr(59)
roh_bytes = open(SRC, 'rb').read()
roh = roh_bytes.decode('utf-8')
zeilen = roh.split('\n')

KOPF_ALT = '**Stand: (Rev. 137 — siehe Block oben.) Zuvor: '
KOPF_NEU = '**Stand: (Rev. 138 — siehe Block oben.) Zuvor: '
if not zeilen[1].startswith(KOPF_ALT):
    raise SystemExit('Standzeile beginnt nicht mit Rev. 137, abgebrochen: ' + zeilen[1][:80])
pos = [i for i, z in enumerate(zeilen) if z.startswith('### ⭐⭐ NEU (Rev. ')]
if not pos or not zeilen[pos[0]].startswith('### ⭐⭐ NEU (Rev. 137, '):
    raise SystemExit('Oberster Block ist nicht Rev. 137, abgebrochen')
if any('(Rev. 138,' in z for z in zeilen) or '(Rev. 138 ' in zeilen[1]:
    raise SystemExit('Rev. 138 besteht schon, nichts geändert')

AUFTRAG = ('Aloui richtet die Einleitung stärker auf die Deatails seiner eigenen Studie aus. Beispiel: wenn er von Training unter '
           '8 Wochen Spricht, ist das nicht falsch, weil in der zitierten Quelle eine spanne vor 6-15 Wochen gegeben ist. '
           'Analysiere an welchen Stellen das zusätzlich in der Einleitung der Fall ist? Es ist keine reine Einleitung zum '
           'allgemeinen Thema sondern soll stark auf das Studienspezifische Konzept, Hypothesen, Forschungsfragen etc. '
           'ausgerichtete Argumentationskette dienen um die Eigene Studie unter berücksichtigung des Forschungsstand darzulegen. '
           'Aus diesem Grund recherchiere ich paralell zu videobasiertem Training im Nachwuchssport um passgenauere Vergleiche '
           'einzuleiten, bevor die Auswirkungen meines Projekts in Methodik, ergebnisse etc. dargelegt wird')

BLOCK = [
    '### ⭐⭐ NEU (Rev. 138, 01.10.2026, ' + UHR + ' Sitzungsuhr, Auftrag 07:42): Zuspitzung der Einleitung von Aloui et al. '
    '(2022) auf die eigene Studie — Analyse im Chat, T4 `Aloui2022` berichtigt, keine Änderung an der Einleitung',
    '',
    '**Auftrag (Verfasser, 01.10., 07:42, wörtlich):** „' + AUFTRAG + '“',
    '',
    '**Einordnung:** Folgeauftrag zu Rev. 136, lief neben Task 11 (Rev. 137) in einer eigenen Sitzung. Ändert keinen '
    'Manuskripttext und keine Reihenfolge. Die Einleitung bleibt pausiert (Rev. 134).',
    '',
    '**Befund (im Chat vorgelegt):** Neben „less than 8 weeks“ spitzt Aloui an elf weiteren Stellen auf die eigene Studie zu, in '
    'jedem Absatz: Anforderungsprofil in den Kategorien der Testbatterie · Kennzahlen mit den Schwellen der eigenen '
    'Testdistanzen (30 und 10 m) · Machbarkeit · Allgemeingültigkeit für Population und Zielgrößen · Kombination als Trend · '
    'Setting in der Saison als Empfehlung ohne Beleg · zwei Vorbilder (Hammami et al., 2020, und Sáez de Villarreal et al., 2015, '
    'das zweite liefert in der Methodik die Sprintdistanzen) · Lücke als genaue Kombination · Zweck und Hypothese als Sammlung '
    'der Bausteine. Nicht vorbereitet: Frequenz, Umfang, das Ersetzen gerade des technisch-taktischen Teils, Gleichgewicht als '
    'Zielgröße, Aufsicht. Grenze: Die Zuspitzung ist legitim, solange das eigene Maß in der Spanne der Quelle liegt. Sie kippt, '
    'wo das eigene Design als Befund erscheint („bilateral … unilateral“), eine Zahl den Bezug wechselt, ein Vorbild stärker '
    'gemacht wird, als es ist, oder die Überleitung ohne Beleg bleibt. Übertragen auf die eigene Einleitung (Textvorschlag '
    'Überarbeitung § 5.1, im Master nach Rev. 137 Schritt 0): Vor jedem Baustein des Zwecksatzes B5 S1 steht ein belegter '
    'Satz, außer vor der Vermittlung (videobasiert, ohne Aufsicht, zu Hause), die B2 S2 und S7 als eigene Folgerung setzen '
    '(Rev. 135).',
    '',
    '**Eigene Berichtigung:** Der T4-Eintrag `Aloui2022` vom 30.09. (Rev. 136) war in Punkt (5) zu streng (Hinweis des '
    'Verfassers: Die Dauer ist durch 6 bis 15 Wochen bei Markovic & Mikulic, 2010, S. 860, gedeckt) und nannte wiederholte '
    'Sprints fälschlich „ohne Begründung“. Berichtigt mit `03_Skripte\\T4_Nachtrag_Aloui2022_2026-10-01.py`: (5) Dauer gedeckt, '
    'die Verbindung beid- und einbeiniger Sprünge nicht · wiederholte Sprints vorbereitet, Gleichgewicht nur als Bestandteil '
    'anderer Kombinationen, beide ohne Hypothese · dazu Wang & Zhang (2016, PMC4950532, narrative Übersicht) gelesen, Herkunft '
    'der Formel in Punkt (4) und Widerspruch der Lückenformel zur eigenen Aufzählung ergänzt. T4 bleibt bei 152 Einträgen, '
    '`Aloui2022` viermal.',
    '',
    '**Vormerkungen für die Schlussfassung der Einleitung (Rev. 134, Prüfkatalog):** (1) Empfehlung: nach dem Volltext von '
    'Klusemann et al. (2012, H13) ein Kontextsatz hinter B2 S7, mit Population, Dosis und Vor-2020-Halbsatz, im selben Satz '
    'der Befund, dass sich die Bewegungsqualität nur mit Trainer verbesserte (Gegenbefund, bereitet G3 vor). Distanz 3 bis 4, '
    'nur als Kontext (Rev. 135 § 5 Nr. 1). (2) B4 S6: Halbsatz, dass die Metaanalysen zur Plyometrie Aufsicht und '
    'Vermittlungsweg nicht als Einflussgröße auswerten (Rev. 135, Gegenrecherche C4), vorher an Oliver et al. (2024), '
    'Ramirez-Campillo et al. (2020, 2023) und Zheng et al. (2025) am Volltext prüfen. (3) B1a S5: Ramirez-Campillo et al. '
    '(2020) teilen zugleich nach höchstens sieben Wochen und höchstens 14 Einheiten (Manuskriptfassung, Abschnitte 2.9 und 3.5, '
    'am 01.10. geprüft), „bis sieben Wochen und 14 Einheiten“ träfe die zwölf Einheiten. Betrifft denselben Satz wie '
    'Textvorschlag 5 § 9.2 Nr. 3 (10-m-Zeit als Gegenbefund), gemeinsam entscheiden.',
    '',
    '**Stand der Dateien:** Geändert: T4 (72.849 Byte, MD5 `ac232b81…`, vorher 71.507 Byte, MD5 `d98a80ae…`) · diese Notizen '
    '(Rev. 138 auf Rev. 137), Ordner und Projektkopie. Neu: `03_Skripte\\T4_Nachtrag_Aloui2022_2026-10-01.py` mit `.txt` · '
    '`03_Skripte\\Steuerung_Rev138_2026-10-01.py` mit `.txt`. Unverändert: Master, Einleitung, Textvorschläge, Maßnahmenliste, '
    'Plan, T1. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.',
    '',
    '**Nächster Schritt:** wie Rev. 137 (Abgleich nach der Übertragung, dann Task 12a). Dieser Eintrag ändert die Reihenfolge '
    'nicht.',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:60]

neu_zeilen = zeilen[:1] + [KOPF_NEU + zeilen[1][len('**Stand: '):]] + zeilen[2:pos[0]] + BLOCK + zeilen[pos[0]:]
neu = '\n'.join(neu_zeilen)
with open(OUT, 'wb') as f:
    f.write(neu.encode('utf-8'))

# Prüfungen: alles außer Standzeile und neuem Block byte-gleich
neu_bytes = open(OUT, 'rb').read()
rest_alt = '\n'.join(zeilen[2:])
rest_neu = '\n'.join(neu_zeilen[2:])
assert rest_neu.replace('\n'.join(BLOCK) + '\n', '', 1) == rest_alt, 'Bestand verändert'
assert neu_zeilen[0] == zeilen[0], 'Titelzeile'
assert neu_zeilen[1] == KOPF_NEU + zeilen[1][len('**Stand: '):], 'Standzeile'
assert neu_zeilen[1].count('(Rev. 138 ') == 1 and neu_zeilen[1].count('(Rev. 137 ') == 1, 'Standzeile doppelt'
assert sum(1 for z in neu_zeilen if z.startswith('### ⭐⭐ NEU (Rev. 138, ')) == 1, 'Block doppelt'
print('Eingabe: %d Byte, MD5 %s' % (len(roh_bytes), hashlib.md5(roh_bytes).hexdigest()))
print('Ausgabe: %d Byte, MD5 %s' % (len(neu_bytes), hashlib.md5(neu_bytes).hexdigest()))
print('Block Rev. 138: %d Zeilen vor Zeile %d (Rev. 137) eingesetzt, Standzeile ergänzt, Bestand byte-gleich' % (len(BLOCK), pos[0] + 1))

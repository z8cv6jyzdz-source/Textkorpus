# -*- coding: utf-8 -*-
"""Steuerung_Rev159_2026-10-03.py — Rev.-Block 159 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Ende von Schritt 3 mit Klickergebnis (Fortsetzung 2).
Setzt den Block vor den jüngsten Block (Rev. 158) und ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev159_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == '7cde45260e62e4bf2baa34419c2630c7', MD5_VORHER  # gestagt 03.10., Dateizeit 13:04 Sitzungsuhr (Rev. 158)
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 158 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 159 — siehe Block oben.) Zuvor: (Rev. 158 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 159' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 159, 03.10.2026, 13:55 Sitzungsuhr, Auftrag 03.10., 13:12 mit dem Startprompt aus Fortsetzungsübergabe 2 § 0): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Schritt 3 abgeschlossen: sieben Potenziale für 6.1 vorgelegt, Klick P1, P2, P5 und P6 '
    'wie empfohlen, P3 als Abweichung vermerkt, § 4 des Ergebnisdokuments gesichert (Fassung 7), kein Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung2_2026-10-03.md` § 0: Schritt 3, Potenziale für 6.1 kompakt auf '
    'höchstens einer Seite (A trägt das Argument, B Leseführung, C Stil), je mit Grundlage, Häufigkeit im Korpus, Wortbilanz innerhalb von 700 und '
    'möglichem Konflikt mit dem Entscheidungsregister, dazu zwei Zeilen zu dem, was 6.1 schon leistet, dann die Klickfrage mit Mehrfachauswahl.',
    '',
    '**Ergebnis:** (1) Rechner verbunden, Master unverändert (MD5 `2fda2144…`, keine comments.xml), Ergebnisdokument Fassung 6 bestätigt (`06a126fb…`), '
    'der Erzeuger reproduziert sie bytegleich. (2) **Sieben Potenziale** (`S3_Potenziale_2026-10-03.py`, Wortbilanz an Probeformulierungen gemessen, '
    'Korpuszahlen aus 2b und 2d): P1 A Pflicht, Vergleiche einheitlich nach der Lage markieren (Ramirez-Campillo et al., 2023, Zheng et al., 2025, und '
    'Lloyd et al., 2016, als „vereinbar“ wie A3 S6), +5 · P2 A, modales Angebot über die eigene Umsetzung nach der Verwerfung der Übungsauswahl in '
    'A4 S8, +8 · P3 B Pflicht, Relevanz zuerst in A3 und A5, im Ordner ohne Primärbeleg mit Spielbezug (Oliver et al., 2024, S. 624, nur Relais), '
    'Variante A3 +9 · P4 B, A5 endet mit dem Normwert · P5 C Pflicht, Modalverb in A4 S8, +1 · P6 C, „zudem“ in A3 S7, −1 · P7 C, „nur“ in A2 S3 '
    '(⚑ K2), −1. Vorgelegt im Chat mit Wortbilanz (Empfehlung +13, gedeckt durch Stufe 3 der Kürzungsleiter, A3 S5, −14, 6.1 dann 699), Geprüftem '
    'ohne Potenzial und dem, was bleibt. (3) **Klick des Verfassers** (gegen 13:46 Sitzungsuhr, drei Fragen nach Priorität mit Mehrfachauswahl): P1 '
    'und P2, keins aus B, P5 und P6, alle wie empfohlen. P3 ist nicht bearbeitet, die Abweichung von „Relevanz zuerst in jedem Block“ in A3 und A5 '
    'steht mit Grund in § 4 (⚑, kein Primärbeleg mit Spielbezug, Korpusbasis der Regel überzeichnet, die P-Zeile 6.1.2 bleibt über CONSORT 22 '
    'getragen). P4 und P7 sind nicht bearbeitet. (4) **§ 4 des Ergebnisdokuments** über das neue Modul `Abgleich_Dokument_4_2026-10-03.py`, Erzeuger in '
    'Fassung 7, § 1 bis § 3 und § 5 zeichengleich mit Fassung 6, bytegleich unter wechselndem `PYTHONHASHSEED`. Vormerkungen: Abweichung P3 an '
    'Berichtsraster Rev. 4 und Fassung 18 § 5a (G37) · G8 in 12b ohne erneute Normwerte, nur die Grenze des Belags · Nachführung von TV 6.1 § 0, '
    '§ 2, § 4 und § 5 mit dem Nachtrag.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Die erste Fassung von P3 nannte nur Faude et al. (2012) hinter Oliver et al. (2024, S. 624), dort '
    'stehen mehrere Verweise, keiner davon im Ordner, vor der Ablage berichtigt. (2) Die Vorlage im Chat nannte für A3 S1 „Korpus 9 von 14 '
    'Prämissen im Indikativ“, gezählt sind Prämissen ohne Modalmarker, § 4 sagt es so. (3) Das Klickprotokoll führte die Antwort in B zunächst mit der '
    'Beschreibung der Option, jetzt mit der Beschriftung und die Beschreibung gesondert.',
    '',
    '**Stand der Dateien:** Neu in `03_Skripte\\Diskussion_Anwendung_2026-10-03\\`: `S3_Potenziale_2026-10-03.py` (17.595 Byte, MD5 `ff543a5a…`), '
    '`S3_Potenziale.csv`, `S3_Potenziale.json`, `S3_Potenziale.txt`, `S3_Probe.csv`, `Abgleich_Dokument_4_2026-10-03.py` (3.293 Byte, MD5 '
    '`9e8e82b1…`) · geändert: `Abgleich_Dokument_2026-10-03.py` (Fassung 7, 26.316 Byte, MD5 `3689a828…`), `LIESMICH.md` (Abschnitt Schritt 3, '
    '19.199 Byte, MD5 `7b8109e3…`) · `02_Befunde\\Abgleich_Diskussion_6.1_Argumentationsstruktur_2026-10-03.md` Fassung 7 (181.914 Byte, MD5 '
    '`aa899bc1…`, § 1 bis § 5) · `03_Skripte\\Steuerung_Rev159_2026-10-03.py` mit `.txt`. Das Ergebnisdokument hat keine Projektkopie '
    '(Projektspeicher an der Grenze), es gilt die Ordnerfassung. Geändert: diese Notizen (Rev. 159 auf Rev. 158), nur im Ordner, die Projektkopie '
    'bleibt auf Rev. 154. Unverändert: Master, Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, '
    'Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenem Ausgabepfad, danach neu gestagt und per MD5 '
    'verglichen, 9 von 9 gleich.',
    '',
    '**Offen beim Verfasser:** (1) Klickfreigabe des Nachtrags zum Textvorschlag 6.1, sobald er vorliegt (P1, P2 mit P5, P6 und die Finanzierung mit '
    'Stufe 3, ⚑ K1) · (2) aus Rev. 152 bis 158 weiter offen: F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher. '
    'Der Preprint Boumparis liegt nicht mehr in `Ideen und Studien` (Ergebnisdokument § 1.5 Nr. 4), dieser Punkt ist erledigt.',
    '',
    '**Nächster Schritt:** Nachtrag zum Textvorschlag 6.1 (`04_Uebergaben\\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_2026-10-03.md`): '
    'Wortlaut für P1, P2 mit P5 und P6, Finanzierung mit Stufe 3, Messung, Zweitprüfung durch einen unabhängigen Subagenten, Klickfreigabe je Absatz, '
    'Einbau nur auf ausdrückliche Anweisung. Danach Schritt 4 (Task 12b).',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 158'
pos = [i for i, z in enumerate(zeilen) if z.startswith(ANKER)]
assert len(pos) == 1, pos
neu = zeilen[:pos[0]] + BLOCK + zeilen[pos[0]:]
neu[1] = STAND_NEU + zeilen[1][len(STAND_ALT):]
# Prüfung: außer Zeile 2 und dem eingefügten Block ist alles gleich
assert neu[:1] == zeilen[:1] and neu[2:pos[0]] == zeilen[2:pos[0]]
assert neu[pos[0] + len(BLOCK):] == zeilen[pos[0]:]
ausgabe = '\n'.join(neu).encode('utf-8')
open(AUS, 'wb').write(ausgabe)
MD5_NACHHER = hashlib.md5(ausgabe).hexdigest()
prot = [
    'Steuerung_Rev159_2026-10-03.py — Rev.-Block 159 in Teil 0',
    f'Eingabe: {len(roh)} Byte, MD5 {MD5_VORHER}',
    f'Ausgabe: {len(ausgabe)} Byte, MD5 {MD5_NACHHER}',
    f'Block vor Zeile {pos[0] + 1} (Rev. 158) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

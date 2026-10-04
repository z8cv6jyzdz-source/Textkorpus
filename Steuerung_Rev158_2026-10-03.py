# -*- coding: utf-8 -*-
"""Steuerung_Rev158_2026-10-03.py — Rev.-Block 158 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Taskwechsel nach Schritt 2 mit Zweitprüfung (Fortsetzungsübergabe 2).
Setzt den Block vor den jüngsten Block (Rev. 157) und ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev158_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == '596f7a433788fcffaa5d7d96bf0b1962', MD5_VORHER  # gestagt 03.10., Dateizeit 11:41:15 Sitzungsuhr
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 157 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 158 — siehe Block oben.) Zuvor: (Rev. 157 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 158' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 158, 03.10.2026, 13:05 Sitzungsuhr, Auftrag 03.10. mit dem Startprompt aus Fortsetzungsübergabe 1 § 0, Sitzung ab 09:17): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Teilschritte 2b bis 2d abgeschlossen, Schritt 2 durch zwei unabhängige Prüfer '
    'zweitgeprüft, Ergebnisdokument Fassung 6 gesichert, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Schritt 3, kein '
    'Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung1_2026-10-03.md` § 0: Teilschritt 2b (die neun Bauregeln '
    'aus Befund § 12.2 und die Projektregeln aus § 12.3 einzeln an 6.1), dann 2c und 2d nach dem Startprompt der Ausgangsübergabe § 0, je mit '
    'gesicherter Teiltabelle und Meldung.',
    '',
    '**Ergebnis:** (1) **Teilschritt 2b** (gesichert 09:44): 25 Zeilen, erfüllt 12 · teilweise 8 · nicht anwendbar 5. „bewusst abweichend“ kommt nicht '
    'vor, weil die Abweichungen vom Korpus selbst Projektregeln sind. Teilweise: Relevanz zuerst nur in A4 (A3 S1 Prämisse, A5 S1 Programmbeschreibung), '
    'Erklärungsanteil in A4 9,8 % (unter 28 von 30 Korpusblöcken), A4 S8 ohne Modalverb, Markierung in A5 S6, Übereinstimmung in A4 S4 nach dem p-Wert '
    'statt nach der Lage im eigenen Intervall (Kriterium nur in einer Zeile von TV 6.1 § 5), „nur“ bei Boumparis als Wertung offen. Lagetabelle: Alle '
    'vier Widerspruchssätze betreffen Effekte außerhalb des eigenen Intervalls, in 4 von 5 Paaren überlappen die Intervalle. (2) **Teilschritt 2c** '
    '(gesichert 09:55): 8 Prüfpunkte, erfüllt 4 · teilweise 4, Tempus je finitem Verb ohne Abweichung, Belegdichte 43,8 Wörter je Belegstelle. '
    '(3) **Teilschritt 2d** (gesichert 10:17): 12 Korpusaussagen am Satzkorpus nachgezählt, keine Befundzahl weicht ab, drei präzisiert (Auflösung '
    'ohne Gegenstück nur als Erklärung, Verwerfung in zwei Formen, Umsetzung erklärt außerhalb des Kerns auch im Zielgrößenblock). Rolle und Merkmale '
    'der Erklärungssätze blind doppelt codiert (Rolle 31 von 32, κ 0,94, Merkmalsmengen 25 von 28). Merkmalstabelle für A4: offen mit Grenze '
    'Umsetzung, Intensität und Reifung, nur als Vergleichbarkeitsmerkmal Saisonphase, Dauer, Dosis, Trainingsstand, Population und Testwahl, für A4 '
    'verworfen Programmgestaltung, gesperrt (12b) Aufsicht, Messgüte, Attrition und Begleitbedingungen. (4) **Zweitprüfung** (gesichert 12:53): '
    'Prüfer B (Subagent) prüfte Fassung 5 mit 23 Befunden, Prüfer C (Subagent) den Entwurf von Fassung 6 mit 14 Befunden und bytegleicher '
    'Reproduktion, kein Befund verworfen, Umgang je Befund in § 5 des Ergebnisdokuments. Vorrang für Schritt 3: Relevanz in A3 und A5, Markierung in '
    'A4 S5 und A5 S6 und das Modalverb in A4 S8 sind Bestandteile der P-Zeile Berichtsraster 6.1.2 (§ 3.4 „Für Schritt 3“ Nr. 8).',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Die Prüfer fanden Überdehnungen, die vor der Ablage berichtigt sind: Sammoud et al. (2024) sind nur '
    'für den Ausgangswert adjustiert, nicht „wie die eigenen“ · die Regel „Übereinstimmung nur, wo …“ stand an keiner Fundstelle, es gibt nur die '
    'Lageangabe einer Zeile in TV 6.1 § 5 · die erste Merkmalstabelle trug undefinierte Stände und fehlende Grenzen · der Auftrag der blinden Codierung '
    'enthielt Beispiele aus den zu codierenden Sätzen, die Kennwerte ohne diese Sätze stehen jetzt daneben (Rolle 27 von 28, Merkmalsmengen 22 von 24) · '
    'das Suchmuster für magnitudenbasierte Etiketten war zu eng (4 statt 6 einordnende Sätze). (2) Prüfer B erzeugte beim Import im gestagten '
    'Anlagenordner einen `__pycache__` und bat um Löschung. Er lag nur in der Sitzungskopie, nicht auf dem Rechner, und wurde nicht gelöscht. Alle '
    'weiteren Läufe mit `PYTHONDONTWRITEBYTECODE=1`.',
    '',
    '**Stand der Dateien:** Neu oder geändert in `03_Skripte\\Diskussion_Anwendung_2026-10-03\\`: 31 Dateien (Skripte und Ausgaben von 2b bis 2d, '
    'Zweitprüfung mit beiden Prüfberichten, blinde Codierung 2d, Erzeuger Fassung 6 mit Modul 5, `LIESMICH.md`), Byte und MD5 in der '
    'Fortsetzungsübergabe 2 § 1.3 · `02_Befunde\\Abgleich_Diskussion_6.1_Argumentationsstruktur_2026-10-03.md` Fassung 6 (172.708 Byte, MD5 '
    '`06a126fb…`, § 1 bis § 3.4 und § 5) · `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung2_2026-10-03.md` mit dem neuen Startprompt (§ 0) · '
    '`03_Skripte\\Steuerung_Rev158_2026-10-03.py` mit `.txt` · Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung2_2026-10-03.md`. Das '
    'Ergebnisdokument hat keine Projektkopie (Projektspeicher 1.976.797 von 2.000.000 Byte vor dieser Ablage), es gilt die Ordnerfassung. Geändert: '
    'diese Notizen (Rev. 158 auf Rev. 157), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Unverändert: Master, Textvorschläge, Kennzahlenblatt, '
    'T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). '
    'Rückschreibung aus eigenen Ausgabepfaden, danach neu gestagt und per MD5 verglichen.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung2_2026-10-03.md` § 0 in '
    'einem neuen Task fortsetzen · (2) aus Rev. 152 bis 155 weiter offen: Preprint Boumparis umbenennen oder in den Papierkorb, F9 im Master, '
    'Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 2 ab Schritt 3: Potenziale für 6.1 auf höchstens einer Seite (A, B, C mit Grundlage, Häufigkeit im Korpus, '
    'Wortbilanz innerhalb von 700 und Konflikt mit dem Register), zwei Zeilen zu dem, was 6.1 schon leistet, dann die Klickfrage mit Mehrfachauswahl. '
    'Danach der Nachtrag zum Textvorschlag 6.1 für freigegebene Potenziale und Schritt 4 (Task 12b).',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 157'
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
    'Steuerung_Rev158_2026-10-03.py — Rev.-Block 158 in Teil 0',
    f'Eingabe: {len(roh)} Byte, MD5 {MD5_VORHER}',
    f'Ausgabe: {len(ausgabe)} Byte, MD5 {MD5_NACHHER}',
    f'Block vor Zeile {pos[0] + 1} (Rev. 157) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

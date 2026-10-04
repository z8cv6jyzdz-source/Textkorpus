# -*- coding: utf-8 -*-
"""Steuerung_Rev160_2026-10-03.py — Rev.-Block 160 in Teil 0 der Sitzungsnotizen.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Taskwechsel nach Schritt 3 mit Klickergebnis (Fortsetzungsübergabe 3).
Setzt den Block vor den jüngsten Block (Rev. 159) und ergänzt die Stand-Zeile. Prüft, dass sonst nichts geändert wird.

Aufruf: python3 Steuerung_Rev160_2026-10-03.py <Sitzungsnotizen gestagt> <Ausgabe .md> <Protokoll .txt>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import sys

SEMI = chr(59)
EIN, AUS, PROT = sys.argv[1:4]
roh = open(EIN, 'rb').read()
MD5_VORHER = hashlib.md5(roh).hexdigest()
assert MD5_VORHER == '75b15739039f7cbd3efec9c8cdfcb2da', MD5_VORHER  # gestagt 03.10., Dateizeit 13:56:55 Sitzungsuhr (Rev. 159)
text = roh.decode('utf-8')
assert '\r\n' not in text
zeilen = text.split('\n')

STAND_ALT = '**Stand: (Rev. 159 — siehe Block oben.) Zuvor: '
STAND_NEU = '**Stand: (Rev. 160 — siehe Block oben.) Zuvor: (Rev. 159 — siehe Block oben.) Zuvor: '
assert zeilen[1].startswith(STAND_ALT)
assert 'Rev. 160' not in text

BLOCK = [
    '### ⭐⭐ NEU (Rev. 160, 03.10.2026, 14:15 Sitzungsuhr, Auftrag 03.10., 13:12 mit dem Startprompt aus Fortsetzungsübergabe 2 § 0): '
    'Task „Diskussion: Anwendung der Argumentationsstruktur“ — Taskwechsel nach Schritt 3 mit Klickergebnis nach automatischer Zusammenfassung des '
    'Verlaufs, Fortsetzungsübergabe 3 mit dem Entwurf des Nachtrags zu 6.1, Fortsetzung ab dem Nachtrag zum Textvorschlag 6.1, kein Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung2_2026-10-03.md` § 0 mit der Taskwechselregel der '
    'Ausgangsübergabe (§ 0 und § 8): Nach einer automatischen Zusammenfassung den laufenden Teilschritt abschließen, sichern und am Checkpoint wechseln.',
    '',
    '**Ergebnis:** (1) Schritt 3 stand vollständig in den Dateien (Rev. 159, Ergebnisdokument Fassung 7, alle Dateien per MD5 bestätigt). Danach wurde '
    'der Verlauf automatisch zusammengefasst, gewechselt wird am Checkpoint nach Schritt 3 mit Klickergebnis, vor dem Nachtrag. Vom Nachtrag gibt es '
    'noch keine Datei. (2) **Fortsetzungsübergabe 3** mit neuem Startprompt (§ 0), den Dateien von Schritt 3 (§ 1.2), dem Klick (§ 2), den offenen '
    'Klicks (§ 3) und dem ersten Arbeitsgang des Nachtrags (§ 4). § 5 Nr. 1 hält den in der Sitzung entworfenen Wortlaut fest, mit Leerraum-Token '
    'nachgezählt, nicht zweitgeprüft und nicht freigegeben: A3 S5 entfällt (Stufe 3, −14) · A3 S7 ohne „zudem“ (P6, −1) · A4 S4 nach der Lage '
    'markiert, dazu ein neuer Satz „Mit beiden ist der eigene Befund vereinbar.“ nach A4 S5 und „vereinbar“ in A5 S6 (P1, zusammen +7) · A4 S8 mit '
    'Modalverb und Angebot über die eigene Umsetzung in einem Satz (P2 mit P5, +5). 6.1 stünde danach bei 697 Wörtern (A3 116, A4 139, A5 159), '
    'längster Satz weiter 31, Belegklammern 14 auf 13, Quellen 9 auf 8. Abweichungen von § 4 des Ergebnisdokuments (P2 und P5 in einem Satz statt '
    'mit angehängtem Angebotssatz, 697 statt 699) begründet der Nachtrag. Prüfpunkte für den Nachtrag und die Zweitprüfung in § 5 Nr. 3.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** § 4 des Ergebnisdokuments begründet P1 mit der Lage im eigenen Intervall statt dem p-Wert. Für Lloyd '
    'et al. (2016) ist die Lage nicht prüfbar (Lagetabelle § 3.2, Innerhalb-Gruppen-Befund), „vereinbar“ stützt sich dort auf die gleiche '
    'Nichtnachweisbarkeit und die Regel des Registers („sonst weder bestätigt noch widerlegt“). Der Nachtrag sagt das in der Belegtabelle, § 4 wird '
    'nicht neu erzeugt (Fortsetzungsübergabe 3 § 5 Nr. 3 a).',
    '',
    '**Stand der Dateien:** Neu: `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung3_2026-10-03.md` (15.030 Byte, MD5 `e621d94a…`) mit '
    'Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung3_2026-10-03.md` (Projektspeicher 1.965.331 von 2.000.000 Byte vor der Ablage) · '
    '`03_Skripte\\Steuerung_Rev160_2026-10-03.py` mit `.txt`. Geändert: diese Notizen (Rev. 160 auf Rev. 159), nur im Ordner, die Projektkopie bleibt '
    'auf Rev. 154. Unverändert: Master (MD5 `2fda2144…`), Ergebnisdokument Fassung 7, Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\`, '
    'Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des '
    'Tasks, Übergabe § 7 Nr. 3). Rückschreibung aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung3_2026-10-03.md` § 0 in '
    'einem neuen Task fortsetzen · (2) danach die Klickfreigabe des Nachtrags je Absatz (A3, A4, A5) und der Finanzierung mit Stufe 3 (⚑ K1) · '
    '(3) aus Rev. 152 bis 159 weiter offen: F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 3 ab dem Nachtrag zum Textvorschlag 6.1 (`04_Uebergaben\\Textvorschlag_6.1_Nachtrag_Argumentationsstruktur_'
    '2026-10-03.md`): Wortlaut ausgehend vom Entwurf in Fortsetzungsübergabe 3 § 5 Nr. 1, Messung per Skript, Änderungs- und Belegtabelle, '
    'Zweitprüfung durch einen unabhängigen Subagenten, Klickfreigabe je Absatz, Einbau nur auf ausdrückliche Anweisung. Danach Schritt 4 (Task 12b).',
    '',
]
for z in BLOCK:
    assert SEMI not in z, z[:80]

ANKER = '### ⭐⭐ NEU (Rev. 159'
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
    'Steuerung_Rev160_2026-10-03.py — Rev.-Block 160 in Teil 0',
    f'Eingabe: {len(roh)} Byte, MD5 {MD5_VORHER}',
    f'Ausgabe: {len(ausgabe)} Byte, MD5 {MD5_NACHHER}',
    f'Block vor Zeile {pos[0] + 1} (Rev. 159) eingefügt, {len(BLOCK)} Zeilen, Stand-Zeile ergänzt, sonst unverändert (geprüft)',
]
open(PROT, 'w', encoding='utf-8', newline='\n').write('\n'.join(prot) + '\n')
assert SEMI not in open(__file__, encoding='utf-8').read()
print('\n'.join(prot))

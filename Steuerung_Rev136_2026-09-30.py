# -*- coding: utf-8 -*-
"""
Steuerung_Rev136_2026-09-30.py — Rev. 136 in Teil 0 der Sitzungsnotizen einsetzen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Prüfung der Einleitung von Aloui et al. (2022), Auftrag 30.09., 20:29 Sitzungsuhr

Setzt den Block Rev. 136 über den Block Rev. 135 und ergänzt die Standzeile. Bricht ab, wenn der oberste Block nicht Rev. 135 ist
(parallele Sitzungen). Der übrige Inhalt bleibt byte-gleich (geprüft).
Aufruf: python Steuerung_Rev136_2026-09-30.py <Cowork_Sitzungsnotizen.md> <Ausgabe.md> <Uhrzeit Sitzungsuhr>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import hashlib

SRC, OUT, UHR = sys.argv[1:4]
SEMI = chr(59)
roh_bytes = open(SRC, 'rb').read()
roh = roh_bytes.decode('utf-8')
zeilen = roh.split('\n')

KOPF_ALT = '**Stand: (Rev. 135 — siehe Block oben.) Zuvor: '
KOPF_NEU = '**Stand: (Rev. 136 — siehe Block oben.) Zuvor: '
if not zeilen[1].startswith(KOPF_ALT):
    raise SystemExit('Standzeile beginnt nicht mit Rev. 135, abgebrochen: ' + zeilen[1][:80])
ANKER = '### ⭐⭐ NEU (Rev. 135, 30.09.2026'
pos = [i for i, z in enumerate(zeilen) if z.startswith('### ⭐⭐ NEU (Rev. ')]
if not pos or not zeilen[pos[0]].startswith(ANKER):
    raise SystemExit('Oberster Block ist nicht Rev. 135, abgebrochen')
if any('(Rev. 136,' in z for z in zeilen):
    raise SystemExit('Rev. 136 besteht schon, nichts geändert')

BLOCK = [
    '### ⭐⭐ NEU (Rev. 136, 30.09.2026, ' + UHR + ' Sitzungsuhr, Auftrag 20:29): Prüfung der Einleitung von Aloui et al. (2022) — '
    'keine Änderung an der Einleitung, Zitierfalle `Aloui2022` in T4 nachgetragen',
    '',
    '**Auftrag (Verfasser, 30.09., 20:29, wörtlich):** „Prüfe die Einleitung der beigefügten Quelle. Sie ist aus meiner Sicht sehr '
    'ansprechend. Anders als bei meinem Projekt wir allerdings kein videobasiertes Training untersucht“',
    '',
    '**Einordnung:** Lief neben Rev. 134 und Rev. 135 in einer eigenen Sitzung. Ändert keinen Manuskripttext und keine Reihenfolge.',
    '',
    '**Befund (im Chat vorgelegt):** Die Einleitung (Korpusstudie des Befunds Argumentationsstruktur, 794 Wörter, 25 Sätze) liest '
    'sich gut durch einen durchgehenden Faden (kurze Sprints von der Anforderung bis zur Lücke), ein Thema je Absatz mit '
    'Anschlusssatz, Anschlusswörter in fast jedem zweiten Satz und wenig Last (randomisiert, betreut, in der Saison, ohne Setting, '
    'Reifung und Diagnostik). Geprüft an 10 der 38 zitierten Arbeiten stimmt in 7 der 25 Sätze der Beleg nicht oder nur teilweise. '
    'Die Lücke grenzt nicht von den eigenen Vorarbeiten ab (Hammami et al., 2019, Aloui et al., 2021), wiederholte Sprints und '
    'Gleichgewicht stehen ohne Begründung und ohne Hypothese. Einzelheiten im T4-Eintrag.',
    '',
    '**Empfehlung (im Chat):** Keine Änderung an der Einleitung. Sie hat dieselbe Grundfigur und ist bei Population, '
    'Gegenbefunden, Begründung der Zielgrößen und Lücke stärker. Alouis Lesefluss beruht vor allem auf zwei Bauformen, die als P5 '
    'und P7 geprüft und nicht gewählt wurden (Klick 17:32, die Gründe gelten weiter). Weniger fließend sind in der eigenen '
    'Einleitung die Anfänge von B2 und B3, beide so entschieden (B2 D6 Nr. 1, B3 Klick 07:00 Nr. 4). Kein neuer Prüfpunkt für '
    'die Schlussfassung (Rev. 134).',
    '',
    '**Klick (Verfasser, 30.09., vor 21:21 Sitzungsuhr):** Befunde als Zitierfalle in T4 eintragen, mit Rev.-Eintrag (Empfehlung).',
    '',
    '**Umgesetzt:** T4 um einen Eintrag `Aloui2022` ergänzt (Einleitung als Belegquelle ungeeignet, Lücke ohne Abgrenzung, '
    'Unabhängigkeit von Aloui et al., 2021, offen: gleiche Mannschaftsbeschreibung, gleiche Ethik-Referenznummer, fast gleiche '
    'Kontrollgruppe). T4 hat 152 statt 151 Einträge, `Aloui2022` viermal.',
    '',
    '**Vormerkung Task 12a (6.1):** Aloui et al. (2022) nur als Vergleich für betreutes, mit Sprints kombiniertes Training bei U15 '
    'in der Saison, vorher T4 `Aloui2022` lesen (vier Einträge). Aloui et al. (2021) nicht zusätzlich als unabhängigen Befund zählen.',
    '',
    '**Stand der Dateien:** Geändert: T4 (71.507 Byte, MD5 `d98a80ae…`, vorher 68.054 Byte, MD5 `4d981572…`) · diese Notizen '
    '(Rev. 136 auf Rev. 135), Ordner und Projektkopie. Neu: `03_Skripte\\T4_Nachtrag_Aloui2022_2026-09-30.py` mit `.txt` · '
    '`03_Skripte\\Steuerung_Rev136_2026-09-30.py` mit `.txt`. Unverändert: Master, Einleitung (Textvorschlag Überarbeitung '
    '§ 5.1), Textvorschläge, Maßnahmenliste, T1. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 '
    'verglichen.',
    '',
    '**Nächster Schritt:** wie Rev. 134: Task 11 (Kapitel 5) nach der Meldung der Übertragung.',
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
assert neu_zeilen[1] == KOPF_NEU + zeilen[1][len('**Stand: '):], 'Standzeile'
assert neu_zeilen[1].count('(Rev. 135 ') == 1 and neu_zeilen[1].count('(Rev. 136 ') == 1, 'Standzeile doppelt'
print('Eingabe: %d Byte, MD5 %s' % (len(roh_bytes), hashlib.md5(roh_bytes).hexdigest()))
print('Ausgabe: %d Byte, MD5 %s' % (len(neu_bytes), hashlib.md5(neu_bytes).hexdigest()))
print('Block Rev. 136: %d Zeilen vor Zeile %d (Rev. 135) eingesetzt, Standzeile ergänzt, Bestand byte-gleich' % (len(BLOCK), pos[0] + 1))

# -*- coding: utf-8 -*-
"""
Steuerung_Rev168_2026-10-03.py

Fügt in Teil 0 der Sitzungsnotizen den Rev.-Block 168 ein (Task „Diskussion: Anwendung der
Argumentationsstruktur“, Freigabe des Gerüsts und Schritt 4 c, Taskwechsel zu Fortsetzung 8) und setzt
die Standzeile auf Rev. 168. Rev. 167 stammt vom parallelen Task „Ergebnisse“ und bleibt darunter.

Aufruf: python3 Steuerung_Rev168_2026-10-03.py <Sitzungsnotizen_ein.md> <Sitzungsnotizen_aus.md> <Protokoll.txt>
Der Code enthält kein Semikolon.
"""
import hashlib
import sys

SEMI = chr(59)

BLOCK = [
    '### ⭐⭐ NEU (Rev. 168, 03.10.2026, 20:54 Sitzungsuhr, Auftrag 03.10. mit dem Startprompt aus Fortsetzungsübergabe 7 § 0, Stagung ab etwa 19:41): Task „Diskussion: Anwendung der Argumentationsstruktur“ — Freigabe des Gerüsts (Zielstufe 11) und Schritt 4 (c) des Tasks 12b: Textvorschlag 6.2 und 6.3 mit 895 Wörtern per Skript erzeugt und geprüft, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzungsübergabe 8, Fortsetzung ab Schritt 4 (d), kein Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung7_2026-10-03.md` § 0: Master und Teil 0 frisch stagen, die Freigabe des Gerüsts als Klick einholen (Zielstufe der Kürzungsleiter, Empfehlung Stufe 12 mit 874 Wörtern), Cohen (1988, S. 43 bis 44) und Mirwald et al. (2002, S. 689) am Volltext prüfen, dann Schritt 4 (c): Textvorschlag 6.2 und 6.3 nach Bauform A mit gemessenem Kopf, Zug-Tabelle, Rasterzuordnung je Satz, Belegtabelle mit Wortlaut und Seite, Kennungen im Begleitteil, Codierung und Prüfliste, höchstens 900 Wörter mit Kürzungsleiter, danach Schritt 4 (d) und (e). Dazu Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.',
    '',
    '**Ergebnis:** (1) **Master** neu gestagt und unverändert (40.337 Byte, MD5 `6c1db455…`, keine comments.xml, 6.2 und 6.3 leer), Teil 0 vor dem Schreiben neu gestagt (Rev. 167 des parallelen Tasks steht darunter). (2) **Klicks** des Verfassers: Freigabe des Gerüsts mit Zielstufe 11 (890 Wörter Satzkerne, Reserve 10), abweichend von der Empfehlung Stufe 12, damit bleiben Sáez-Sáez de Villarreal et al. (2009) in G8. Mit der Stufe entschieden: Startdistanz entfällt (K-Zeile) · Planungsmodell der Antragsrechnung nach Anhang G (Task 16) · Dambel et al. (2025) entfällt · Normlücke entfällt · Selbstauswahl im Per-Protokoll-Vergleich entfällt. G1h: Die Richtung der p-Werte („eher zu klein“) steht modal als eigene Ableitung ohne Beleg (Empfehlung angenommen). (3) **Volltextprüfungen:** Cohen (1988, S. 43 bis 44) nennt keine Richtung, nur „may differ greatly from the true values“ (S. 44) · Mirwald et al. (2002, S. 689) „categorical rather than a continuous assessment“ · jede Fundstelle der Belegtabelle am PDF im Ordner `Ideen und Studien`, Khamis und Roche (1994) Abb. 1 auf S. 506 am Seitenbild · Stilprofil gelesen. (4) **Textvorschlag** per `03_Skripte\\Diskussion_Anwendung_2026-10-03\\S4c_Textvorschlag_2026-10-03.py`, Ergebnis `04_Uebergaben\\Textvorschlag_6.2_6.3_2026-10-03.md` mit `S4c_Textvorschlag.json` (Wortlaut für den Einbau), `S4c_Saetze.csv` (je Satz Punkt, Teilzeilen, Code, Quellen, Kennungen) und Prüfprotokoll `S4c_Textvorschlag.txt`: sieben Absätze nach Bauform A (A1 Ankündigung, Methodenbegründungen und Stärken mit Korpus-Sammelsatz · A2 Scharnier und G1 · A3 G2 · A4 G3 · A5 G4 und G5 · A6 G6 und G7 · A7 G8 mit dem Ausblick als letztem Satz), 895 Wörter (Reserve 5), Absätze 122 · 135 · 146 · 127 · 147 · 109 · 109, 61 Sätze, Median 14, längster Satz 30, 20 Quellen in 16 Belegklammern. Zwölf Prüfungen per Skript ohne Befund (Budget, Satzteilung wie Messskript Fassung 4, Satzlänge, Semikola, Verweise und Wendungen, keine Folge von sechs Wörtern aus Einleitung bis 6.1 mit 68 Absätzen, Bauform A mit Kette Erstens bis Schließlich, alle 48 Gerüstpunkte der Stufe 11, Raster mit P- und E-Zeilen und allen 66 Kern-Teilzeilen, Quellen mit PDF, T1, T4 und Belegzeile, 37 Abgleiche am Kennzahlenblatt, Sprache, Master unverändert, Konsequenz je Limitation), zwei Läufe unter verschiedenem `PYTHONHASHSEED` bytegleich. Codierung nach dem Codebuch (Befund Anhang E): 34 Sätze L1 primär, Konsequenz im selben Satz bei 15, im nächsten bei 10, ohne bei 9 mit Grund je Satz (Korpus 17 von 22 mit Konsequenz), drei Entkräftungen nur nach F17 § 12 und R2 (Bootstrap in G1, Begleitprogramme in G2, Untergrenzen in G6), letzter Satz Ausblick. Modellrechnungen M1 (Familienfehler höchstens 7,5 %, 7,3 % bei Unabhängigkeit) und M2 (Richtung der p-Werte bei ungleichen Residuenstreuungen, für alle drei Zielgrößen gestützt). Seitenprognose nach dem Einbau rund 28,6 Seiten (Modellrechnung, das Literaturverzeichnis wächst um rund sieben Einträge). Kürzungsleiter T1 bis T4 bis 860 Wörter mit Rückholliste (§ 9), Vormerkungen für Kapitel 7 (§ 11.1) und für weitere Tasks und Steuerdokumente (§ 11.2), Klickfragen für 4 (e) (§ 12: Wortlaut, Einbauweg, G8b, Überschriften). (5) **Taskwechsel** nach automatischer Zusammenfassung des Verlaufs am Checkpoint nach Schritt 4 (c): Fortsetzungsübergabe 8 mit neuem Startprompt (§ 0), Ergebnis und Dateien (§ 1), offenen Klicks (§ 3), der Zweitprüfung als erstem Arbeitsgang mit Auftrag an den Subagenten (§ 4) und Besonderheiten (§ 5).',
    '',
    '**Befunde (Textvorschlag § 10):** D1 Cohen (1988, S. 43 bis 44) nennt keine Richtung der Verzerrung, T4-Nachtrag vorgemerkt · D2 der Fehler zwischen Testtagen steht bei Hopkins (2000) auf S. 13, nicht auf S. 7 · D3 „gerätefrei“ trägt in der Korpusaussage nicht (Sammoud et al., 2024, nennen keine Geräte), die Aussage lautet „unbeaufsichtigt oder videobasiert“ und gilt für Interventionsstudien zu plyometrischem Training im Nachwuchsfußball, betroffen F17 § 6.4 und § 6.5 und Raster 6.3.5 b, die Lücke der Einleitung bleibt unberührt · D4 „bis 1,6 Standardabweichungen“ trifft Tab. 2 nicht (10-m-Sprint d −2,23, K-04.2), der Text nennt den 30-m-Sprint mit 1,64 (K-04.3), betroffen Raster 6.2.10 c · D5 nur das Fitnessniveau zu nennen wäre selektiv, der Text nennt auch das Wettkampfniveau ohne gerichtetes Muster (Klickfrage G8b) · D6 Hilska et al. (2021): Studienverlauf statt Saisonverlauf · D7 Khamis und Roche (1994): Abb. 1 auf S. 506, nicht S. 505 · D8 die korrigierten Fallzuordnungen des Fragebogens (K-10.2) stehen weder in 4.6 noch in Kapitel 5, der Text nennt sie ohne Zahl · D9 „um ein Mehrfaches“ überzeichnet den Bestwert-Bias beim 505-Test je Seite (1,43- und 3,22-Faches des SESOI bei je vier Spielern, K-11.6), Text „um mehr als den SESOI“, betroffen Raster 6.2.6 c · D10 die Belegerkennung des Messskripts Fassung 4 kennt „ł“ und Namenspartikel wie „de“ nicht, Malina und Kozieł (2014) und Sáez-Sáez de Villarreal et al. (2009) fehlen in der Belegzählung der Seitenschätzung · D11 Einbauort der Überschriften 6.2 und 6.3 (Klickfrage, M28 analog).',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Der erste Entwurf lag mit 901 Wörtern über dem Budget, inhaltsneutral auf 895 gekürzt. (2) Die Zahlentabelle ordnete jede Zahl dem ersten Satz ihres Gerüstpunkts zu, sie führt jetzt die Satzkennung. (3) Die Zählung der Konsequenzen war mechanisch und rechnete einen L2-Satz der folgenden Limitation mit, jetzt am Wortlaut geprüft, jeder Satz ohne Konsequenz mit Grund (Prüfung 12). (4) Der Ausblick war als Vorsicht codiert, jetzt Forschung (A1 mit L2 wie im Korpus). (5) Im Entwurf „um ein Mehrfaches“ (D9) und „weitere Verwechslungen“ (D8) berichtigt. (6) Kleinere Fehler des Erzeugers: Satzanfänge, eine triviale Abweichungszeile, Wortzahl der Fassung G8b dynamisch (28 statt 27), Kopfzeile, Titel von § 15. (7) Rückschreibung der Übergabe: Die Datei wurde nach dem Anlegen im selben Ausgabeordner noch berichtigt (Uhrzeit), der Commit aus `ue8_2026-10-03_a` schrieb den Stand davor (MD5 `c6b59fea…`). Neu aus `ue8_2026-10-03_b` zurückgeschrieben, neu gestagt, MD5 gleich (F17 (F)). Die Übergabe nennt in § 1.4 und § 5 Nr. 1 nur `ue8_2026-10-03_a`, vergeben ist auch `ue8_2026-10-03_b`.',
    '',
    '**Stand der Dateien:** Neu: im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` die Dateien `S4c_Textvorschlag_2026-10-03.py` (98.858 Byte, MD5 `e6b6f2ef…`), `S4c_Textvorschlag.json` (15.746 Byte, `2ba17b38…`), `S4c_Saetze.csv` (11.597 Byte, `419c9061…`) und `S4c_Textvorschlag.txt` (4.095 Byte, `0747ee18…`), der Ordner hat jetzt 18 Dateien · `04_Uebergaben\\Textvorschlag_6.2_6.3_2026-10-03.md` (71.050 Byte, `327e2868…`), ohne Projektkopie, es gilt die Ordnerfassung · `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung8_2026-10-03.md` (15.475 Byte, `d04b23ec…`) mit dem neuen Startprompt (§ 0) und Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung8_2026-10-03.md`, Projektspeicher danach 1.943.551 von 2.000.000 Byte · `03_Skripte\\Steuerung_Rev168_2026-10-03.py` mit `.txt`. Geändert: `LIESMICH.md` des Arbeitsordners (Abschnitt „Schritt 4 (c)“, 43.755 Byte, `45b2ebd3…`) · diese Notizen (Rev. 168 auf Rev. 167), nur im Ordner. Unverändert: Master (`6c1db455…`), Gerüst und S4b-Dateien, S4a-Dateien, T1, T4, Kennzahlenblatt, Textvorschlag 6.1 Fassung 3, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Fortsetzungsübergabe 8 § 5 Nr. 7). Rückschreibung aus eigenen Ausgabepfaden (`s4c_2026-10-03_a` sechs Dateien um 20:42, `ue8_2026-10-03_a` und `ue8_2026-10-03_b` Übergabe, `rev168_2026-10-03_a` diese Notizen mit Skript und Protokoll), danach neu gestagt und per MD5 verglichen.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung8_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) dort nach der Zweitprüfung die Klicks aus Textvorschlag § 12 (Wortlaut, Einbauweg, G8b, Überschriften), Einbau nur auf ausdrückliche Anweisung · (3) aus Rev. 152 bis 167 weiter offen: Fortsetzung des Tasks „Ergebnisse“ mit Fortsetzungsübergabe 5 (Rev. 167), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 8: Master und Teil 0 frisch stagen (weicht die MD5 des Masters ab, das S4c-Skript in einen neuen Ausgabeordner laufen lassen, Prüfung 4 und 11 müssen bestehen), dann Schritt 4 (d) mit der Zweitprüfung durch einen unabhängigen Subagenten nach Fortsetzungsübergabe 8 § 4 (Auftrag `S4d_Zweitpruefung_Auftrag.md`, Bericht `S4d_Zweitpruefung_Bericht.md`, Schwere A, B, C), Einarbeitung per Skript als Fassung 2 des Textvorschlags, Rückschreibung, danach (e) Klickfreigabe, Einbau nur auf ausdrückliche Anweisung, Abgleich, Messskript Fassung 4 und Endabgleich Fassung 3 in eigenem Unterordner, dann Schritt 5, am Ende des Tasks Maßnahmenliste (Taskzeile 12, G37) und Rev.-Block.',
    '',
]


def main():
    ein, aus, prot = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(ein, 'rb') as f:
        roh = f.read()
    text = roh.decode('utf-8')
    zeilen = text.split('\n')
    p = []
    p.append('Eingang: ' + str(len(roh)) + ' Byte · MD5 ' + hashlib.md5(roh).hexdigest())
    marke = '### ⭐⭐ NEU (Rev. 167,'
    idx = [i for i, z in enumerate(zeilen) if z.startswith(marke)]
    if len(idx) != 1:
        sys.exit('Abbruch: Block Rev. 167 nicht genau einmal gefunden')
    if any(z.startswith('### ⭐⭐ NEU (Rev. 168,') for z in zeilen):
        sys.exit('Abbruch: Rev. 168 existiert bereits')
    oben = [i for i, z in enumerate(zeilen) if z.startswith('### ⭐⭐ NEU (Rev. ')]
    if not oben or oben[0] != idx[0]:
        sys.exit('Abbruch: Rev. 167 ist nicht der oberste Block')
    stand_alt = '**Stand: (Rev. 167 — siehe Block oben.)'
    if not zeilen[1].startswith(stand_alt):
        sys.exit('Abbruch: Standzeile beginnt nicht mit Rev. 167')
    zeilen[1] = '**Stand: (Rev. 168 — siehe Block oben.) Zuvor: (Rev. 167 — siehe Block oben.)' + zeilen[1][len(stand_alt):]
    neu = zeilen[:idx[0]] + BLOCK + zeilen[idx[0]:]
    ausgabe = '\n'.join(neu).encode('utf-8')
    with open(aus, 'wb') as f:
        f.write(ausgabe)
    p.append('Block Rev. 168 vor Zeile ' + str(idx[0] + 1) + ' eingefügt (' + str(len(BLOCK)) + ' Zeilen), Standzeile auf Rev. 168')
    p.append('Ausgang: ' + str(len(ausgabe)) + ' Byte · MD5 ' + hashlib.md5(ausgabe).hexdigest())
    rest_alt = text.encode('utf-8')
    zurueck = ausgabe.replace('\n'.join(BLOCK).encode('utf-8') + b'\n', b'', 1)
    zurueck = zurueck.replace(zeilen[1].encode('utf-8'), roh.decode('utf-8').split('\n')[1].encode('utf-8'), 1)
    p.append('Übriger Text unverändert: ' + ('ja' if zurueck == rest_alt else 'NEIN'))
    blocktext = '\n'.join(BLOCK)
    p.append('Semikola im Block: ' + str(blocktext.count(SEMI)))
    p.append('Wörter im Block: ' + str(len(blocktext.split())))
    with open(__file__, 'r', encoding='utf-8') as f:
        p.append('Semikola im Skript: ' + str(f.read().count(SEMI)))
    with open(prot, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(p) + '\n')
    print('\n'.join(p))


if __name__ == '__main__':
    main()

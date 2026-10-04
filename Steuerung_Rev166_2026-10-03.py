# -*- coding: utf-8 -*-
"""
Steuerung_Rev166_2026-10-03.py

Fügt in Teil 0 der Sitzungsnotizen den Rev.-Block 166 ein (Task „Diskussion: Anwendung der
Argumentationsstruktur“, Schritt 4 b, Taskwechsel zu Fortsetzung 7) und setzt die Standzeile auf Rev. 166.

Aufruf: python3 Steuerung_Rev166_2026-10-03.py <Sitzungsnotizen_ein.md> <Sitzungsnotizen_aus.md> <Protokoll.txt>
Der Code enthält kein Semikolon.
"""
import hashlib
import sys

SEMI = chr(59)

BLOCK = [
    '### ⭐⭐ NEU (Rev. 166, 03.10.2026, 19:40 Sitzungsuhr, Auftrag 03.10. mit dem Startprompt aus Fortsetzungsübergabe 6 § 0, Stagung ab etwa 18:20): Task „Diskussion: Anwendung der Argumentationsstruktur“ — Schritt 4 (b) des Tasks 12b: Klicks K-b1 bis K-b8, T1 und T4 nachgetragen, Gerüst für 6.2 und 6.3 mit Kürzungsleiter (Empfehlung 874 Wörter) per Skript erzeugt und geprüft, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzungsübergabe 7, Fortsetzung ab der Freigabe des Gerüsts und Schritt 4 (c), kein Manuskripttext',
    '',
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung6_2026-10-03.md` § 0: Schritt 4 (b), also Master und Teil 0 frisch stagen, die Klicks K-b1 bis K-b8 aus `S4a_Rasterzuordnung_12b.md` § 6 mit Empfehlung vorlegen, T1 `Liu2024` angleichen und die fehlenden T1-Steckbriefe der Kern-Quellen anlegen, dann Zug-Tabelle, Verzichtstabelle und Stichpunktgerüst nach Bauform A mit Quelle, Konvergenzstufe, Kennung und Zielwörtern je Punkt und einer Kürzungsleiter bis 900 Wörter, erst nach der Freigabe ausformulieren. Dazu Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.',
    '',
    '**Ergebnis:** (1) **Master** neu gestagt und unverändert (40.337 Byte, MD5 `6c1db455…`, keine comments.xml, 6.2 und 6.3 leer), Teil 0 vor dem Schreiben neu gestagt (Rev. 165 des parallelen Tasks steht darunter). (2) **Klicks** des Verfassers: K-b1 ohne Beleg (Stuart und H8 fehlen) · K-b2 Hilska et al. (2021) in G3 · K-b3 TESTEX in G5 mit Namen und Beleg · K-b4 Korpusaussage ohne Zahl mit drei Studien · K-b5 Fallzahlempfehlung ohne Zahl · K-b6 alle drei Mannschaften unterhalb der Verbandsebene (Kreis- oder Bezirksliga) · K-b7 weder Rechenkette noch Ethikvotum noch Schwellen als Stärke · K-b8 30-m-Sprint je Verein Verzicht. (3) **T1 und T4** per `03_Skripte\\Diskussion_Anwendung_2026-10-03\\S4b_T1_T4_Nachtrag_2026-10-03.py`: Liu2024 Distanz 2 · 1 · 2 auf 1 · 1 · 0, neue Steckbriefe Moher2010, KhamisRoche1994, Smart2015 und Malina2014 (T1 jetzt 80), sechs neue Zitierfallen zu Moher2010, KhamisRoche1994, Smart2015, Malina2014 und Dambel2025 (T4 jetzt 177), alle am Volltext geprüft, Metadaten über PubMed und Crossref. (4) **Gerüst** per `S4b_Geruest_2026-10-03.py`, Ergebnis `S4b_Geruest_12b.md` mit CSV und Prüfprotokoll: 64 Punkte mit Satzkern, Quelle und Fundstelle, Konvergenzstufe, Kennung und Zielwörtern (Vollstufe 1.166 Wörter), Kürzungsleiter in 13 Stufen, Empfehlung Stufe 12 mit 874 Wörtern, Stufe 13 als Sicherheit mit 861, Verzichtstabelle, Befunde C1 bis C9, Vormerkungen. Neun Prüfungen ohne Befund (Budget, alle 66 Kern-Teilzeilen mit Ort, P- und E-Zeilen nach der Empfehlung, 23 Quellen mit PDF, T1 und T4, Kennungen, Satzlänge und Wendungen, keine Folge von sechs Wörtern aus Einleitung bis 6.1, Kette Erstens bis Schließlich, Master ohne Kommentare), zwei Läufe unter verschiedenem `PYTHONHASHSEED` bytegleich. (5) **Taskwechsel** nach automatischer Zusammenfassung des Verlaufs am Checkpoint nach Schritt 4 (b): Fortsetzungsübergabe 7 mit neuem Startprompt (§ 0), Ergebnis und Dateien (§ 1), offenen Klicks (§ 3), Freigabe und Schritt 4 (c) als erstem Arbeitsgang (§ 4) und Besonderheiten (§ 5).',
    '',
    '**Befunde (Gerüst § 6):** C2 Khamis und Roche (1994) und Moher et al. (2010) standen im Master ohne T1-Steckbrief, Fröhlich et al. (2020) steht es weiter (Task 15) · C3 das TESTEX-Kriterium 6 erreichen insgesamt nur 30-m-Sprint und Standweitsprung, in der Kontrollgruppe keine Zielgröße, F17 § 4 und § 12 G5 sind nachzuführen · C4 Kapitel 5, 4.7, 4.3 und 4.1 tragen viele Tatsachen schon, 6.2 und 6.3 nennen nur Folgen · C5 die Fehlermaße nach Khamis und Roche gelten für die vorhergesagte Erwachsenengröße, der Altersverlauf nur aus Abb. 1 · C6 die Spielklasse steht nicht in 4.2 · 6.3.4 d entfällt, der Antrag nennt den Jahrgang 2012 als Einschluss · Moher Item 12a trägt die Analyseeinheit bei Clusterzuteilung nicht.',
    '',
    '**Eigene Korrekturen in dieser Sitzung:** (1) Ein Entwurfssatz nannte „bis zu ein Viertel des SESOI“ je zusätzlichem Versuch ohne Zielgröße, beim 5- und 10-m-Sprint lagen die Werte darüber, der Satz nennt jetzt 30-m-Sprint und Standweitsprung. (2) Eine verdichtete Fassung des Korpus-Sammelsatzes („adjustierten nicht für den Reifestatus“) hätte Lloyd et al. (2016) mit Reifegruppen unzutreffend beschrieben, es bleibt „nicht als Kovariate“. (3) Das Streichpaket Bootstrap stand zuerst in der Empfehlung, obwohl das Modul im Bericht bleibt (F17 § 13 Nr. 23), es steht jetzt in der Sicherheitsstufe. (4) Eine Verschmelzung der Messfehlersätze ließ die Folge zwischen Testtagen fallen, berichtigt. (5) Die Quellenspalte der Leiter führte gestrichene Belege weiter, das Skript gleicht sie jetzt mit dem Satzkern ab. (6) Zwei Semikola im Gerüst-Skript (XML-Entitäten, ein Prüfausdruck) vor dem Lauf in den Arbeitsordner entfernt. (7) In der Übergabe stand für G5 zuerst 92 statt 94 Wörter, berichtigt.',
    '',
    '**Stand der Dateien:** Neu: im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\` die Dateien `S4b_T1_T4_Nachtrag_2026-10-03.py` (18.570 Byte, MD5 `7ca5923e…`) mit `S4b_T1_T4_Nachtrag.txt` (1.517 Byte, `dbf13475…`), `S4b_Geruest_2026-10-03.py` (65.594 Byte, `5820be05…`), `S4b_Geruest_12b.md` (44.638 Byte, `8b995347…`), `S4b_Geruest.csv` (15.589 Byte, `54cf5cc2…`) und `S4b_Geruest.txt` (2.440 Byte, `40b8ad48…`) · `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung7_2026-10-03.md` (15.991 Byte, MD5 `5315c518…`) mit dem neuen Startprompt (§ 0) und Projektkopie `claude/Uebergabe_Diskussion_Anwendung_Fortsetzung7_2026-10-03.md` · `03_Skripte\\Steuerung_Rev166_2026-10-03.py` mit `.txt`. Geändert: `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (109.829 Byte, `11b22af8…`, 80 Steckbriefe) und `T4_zitierfallen.csv` (90.431 Byte, `a373f7b9…`, 177 Zeilen) · `03_Skripte\\Diskussion_Anwendung_2026-10-03\\LIESMICH.md` (Abschnitt „Schritt 4 (b)“, 40.446 Byte, `c83dc029…`) · diese Notizen (Rev. 166 auf Rev. 165), nur im Ordner, die Projektkopie bleibt auf Rev. 154. Unverändert: Master (`6c1db455…`), Textvorschlag 6.1 Fassung 3, S4a-Dateien, Kennzahlenblatt, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Maßnahmenliste (Nachführung am Ende des Tasks, Fortsetzungsübergabe 7 § 5 Nr. 7). Rückschreibung aus eigenen Ausgabepfaden (`s4b_2026-10-03_a` vier Dateien um 19:17, `s4b_2026-10-03_b` fünf Dateien um 19:34, `ue7_2026-10-03_a` Übergabe, `rev166_2026-10-03_a` diese Notizen mit Skript und Protokoll), danach neu gestagt und per MD5 verglichen.',
    '',
    '**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung7_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) dort die Freigabe des Gerüsts mit Zielstufe (Empfehlung Stufe 12, 874 Wörter, die Leiter legt die Abweichungen von früheren Vormerkungen offen), danach Textvorschlag, Zweitprüfung, Freigabe und Einbau von 6.2 und 6.3 · (3) aus Rev. 152 bis 165 weiter offen: Fortsetzung des Tasks „Ergebnisse“ (Rev. 165), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.',
    '',
    '**Nächster Schritt:** Fortsetzung 7: Master und Teil 0 frisch stagen, Freigabe des Gerüsts als Klick, Cohen (1988, S. 43 bis 44) und Mirwald et al. (2002, S. 689) am Volltext prüfen, Stilprofil lesen, dann Schritt 4 (c) mit dem Textvorschlag 6.2 und 6.3 (höchstens 900 Wörter, Erzeuger mit Präfix `S4c_`), danach (d) Zweitprüfung und (e) Freigabe und Einbau, am Ende des Tasks Maßnahmenliste und Rev.-Block.',
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
    marke = '### ⭐⭐ NEU (Rev. 165,'
    idx = [i for i, z in enumerate(zeilen) if z.startswith(marke)]
    if len(idx) != 1:
        sys.exit('Abbruch: Block Rev. 165 nicht genau einmal gefunden')
    if any(z.startswith('### ⭐⭐ NEU (Rev. 166,') for z in zeilen):
        sys.exit('Abbruch: Rev. 166 existiert bereits')
    stand_alt = '**Stand: (Rev. 165 — siehe Block oben.)'
    if not zeilen[1].startswith(stand_alt):
        sys.exit('Abbruch: Standzeile beginnt nicht mit Rev. 165')
    zeilen[1] = '**Stand: (Rev. 166 — siehe Block oben.) Zuvor: (Rev. 165 — siehe Block oben.)' + zeilen[1][len(stand_alt):]
    neu = zeilen[:idx[0]] + BLOCK + zeilen[idx[0]:]
    ausgabe = '\n'.join(neu).encode('utf-8')
    with open(aus, 'wb') as f:
        f.write(ausgabe)
    p.append('Block Rev. 166 vor Zeile ' + str(idx[0] + 1) + ' eingefügt (' + str(len(BLOCK)) + ' Zeilen), Standzeile auf Rev. 166')
    p.append('Ausgang: ' + str(len(ausgabe)) + ' Byte · MD5 ' + hashlib.md5(ausgabe).hexdigest())
    rest_alt = text.encode('utf-8')
    p.append('Übriger Text unverändert: ' + ('ja' if ausgabe.replace('\n'.join(BLOCK).encode('utf-8') + b'\n', b'', 1).replace(zeilen[1].encode('utf-8'), roh.decode('utf-8').split('\n')[1].encode('utf-8'), 1) == rest_alt else 'NEIN'))
    blocktext = '\n'.join(BLOCK)
    p.append('Semikola im Block: ' + str(blocktext.count(SEMI)))
    with open(__file__, 'r', encoding='utf-8') as f:
        p.append('Semikola im Skript: ' + str(f.read().count(SEMI)))
    with open(prot, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(p) + '\n')
    print('\n'.join(p))


if __name__ == '__main__':
    main()

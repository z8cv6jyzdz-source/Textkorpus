# -*- coding: utf-8 -*-
"""Steuerung_Rev170_2026-10-03.py — Rev. 170 in Teil 0 der Sitzungsnotizen und Nachführung der Maßnahmenliste.

Task „Diskussion: Anwendung der Argumentationsstruktur“, Fortsetzung 8 (Task 12b, Schritt 4 d, Taskwechsel nach der
Freigabe). Setzt den Rev.-Block 170 über Rev. 169, schreibt in der Maßnahmenliste die Stand-Zeile, die Taskzeile 12,
G37 (q) und die Summenzeile fort. Prüft vorher Größe und Anfang beider Eingänge.
Aufruf: python3 Steuerung_Rev170_2026-10-03.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Fortsetzung9.md> <Ausgabeordner>
Ohne Semikolon im Skript (chr(59)). KI-erzeugt (Claude, Anthropic, Sitzung 03.10.2026).
"""
import hashlib
import os
import sys

SEMI = chr(59)
NOTIZ, MASS, UE9, AUS = sys.argv[1:5]
os.makedirs(AUS, exist_ok=True)
LOG = []


def info(p):
    b = open(p, 'rb').read()
    return '{:,}'.format(len(b)).replace(',', '.'), hashlib.md5(b).hexdigest()


nu, hu = info(UE9)
t = open(NOTIZ, encoding='utf-8').read()
anker = '### ⭐⭐ NEU (Rev. 169, 03.10.2026, 21:43 Sitzungsuhr'
assert t.count(anker) == 1 and 'Rev. 170,' not in t
REV = (
    '### ⭐⭐ NEU (Rev. 170, 03.10.2026, 22:50 Sitzungsuhr, Auftrag 03.10. mit dem Startprompt aus Fortsetzungsübergabe 8 § 0, '
    'Stagung ab etwa 21:00): Task „Diskussion: Anwendung der Argumentationsstruktur“ — Schritt 4 (d) des Tasks 12b: Zweitprüfung '
    'des Textvorschlags 6.2 und 6.3, Fassung 2 per Skript (898 Wörter), Freigabe nach Empfehlung auf die Weisung „ohne Rückfragen '
    'abschließen“, Einbau an einer Kopie geprüft, Rückschreibung des Masters von der Umgebung gesperrt, Taskwechsel mit '
    'Fortsetzungsübergabe 9, kein Manuskripttext im Master\n\n'
    '**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung8_2026-10-03.md` § 0: Master und Teil 0 '
    'frisch stagen, Schritt 4 (d) mit Zweitprüfung durch einen unabhängigen Subagenten, Befunde nach Schwere A, B, C, Einarbeitung '
    'per Skript als Fassung 2, Rückschreibung, dann 4 (e) Klickfreigabe (Wortlaut, Einbauweg, G8b, Überschriften), Einbau nur auf '
    'ausdrückliche Anweisung, Abgleich, Messskript Fassung 4 und Endabgleich Fassung 3 in eigenem Unterordner, Schritt 5, '
    'Maßnahmenliste und Rev.-Block. Um 22:15 (Sitzungsuhr) schrieb der Verfasser: „bitte ohne rückfragen abschließen und innerhalb '
    'des wöchentlichen limits bleiben um noch fertig zu werden“.\n\n'
    '**Ergebnis:** (1) **Master** neu gestagt und unverändert (40.337 Byte, MD5 `6c1db455…`, keine comments.xml, 6.2 und 6.3 leer), '
    'kein Neulauf des S4c-Skripts nötig. (2) **Zweitprüfung** durch zwei unabhängige Subagenten (Teil 1 Quellen am Volltext mit T1 '
    'und T4, Teil 2 Zahlen, Regeln und Raster): 50 Befunde (A 8 · B 22 · C 20), dazu zwei eigene (E1 „ungenutzt“ statt '
    '„unausgewertet“, E2 Gründe fehlen nur für nicht gemeldete Einheiten), jeder an der Fundstelle nachgeprüft, Bewertung je Befund '
    'in `S4d_Bewertung.md`. Schwere A unter anderem: Korpus-Sammelsatz mit typischen Messfehlern (vier von elf Studien berichten '
    'einen CV), „Reifetempo“ statt Zeitpunkt (Malina und Kozieł, 2014, S. 424), Vor-2020-Halbsatz bei Moran et al. (2017) und '
    'Sáez-Sáez de Villarreal et al. (2009), Begleitprogramme nur mit der Seite der Kontrollgruppe, TESTEX 7 als Analyse aller '
    'Zugeteilten missverständlich, Untergrenzen falsch begründet, fehlender Reifestatus ohne Verzerrungsrisiko. (3) **Entscheidungen '
    'nach Empfehlung** (Weisung 22:15, keine Klicks): G8b mit Kürzungsstufe T1, Sáez-Sáez de Villarreal et al. (2009) entfällt · '
    'R1 in Variante (b) mit ausdrücklicher Einordnung der unveränderten 30-m-Zeiten (Register 6.2.12, abweichend von der Empfehlung '
    '(a) der Bewertung, weil das Register sie verlangt und das Budget sie trägt) · R11 ohne Ergebniszahlen · R6 beide Begrenzungen '
    'der Auflösung · Population bei Klusemann et al. (2012) und Hilska et al. (2021) · R8, R18, Sommerpause im Ausblick, Q3-1 · '
    'Überschrift 6.2 mit dem v6-Titel, 6.3 entfällt · Einbau per Skript. (4) **Fassung 2** per '
    '`S4d_Textvorschlag_F2_2026-10-03.py`: 898 Wörter (Reserve 2), 60 Sätze, Median 15, 19 Quellen in 15 Klammern, 26 Sätze '
    'geändert, einer entfällt (A5.S9 in A5.S7), 13 Prüfungen ohne Befund, neu Prüfung 13 (Fassung 1 gegen Fassung 2), zwei Läufe '
    'bytegleich. Schritt 5 (Vormerkungen für Kapitel 7) in § 11.1 ergänzt. (5) **Einbau** per `S4e_Einbau_6.2_2026-10-03.py` an '
    'einer Kopie des Masters geprüft: Überschrift 6.2 mit v6-Titel, Überschrift 6.3 und ihr Verzeichniseintrag entfernt, sieben '
    'Absätze, Abgleich 7 von 7, `validate.py` ohne Befund, Messskript Fassung 4 an der Kopie: 6.2 898 gegen 900, Kapitel 6 1.598 '
    'gegen 1.600, Absatztext 5.394 gegen 6.350, Seitenprognose 28,4 Seiten (Modellrechnung). Die Umgebung sperrte den Endabgleich '
    'an der Kopie und das Zusammenstellen der Rückschreibung des Masters (Freigabeprüfung „Modify Shared Resources“ und '
    '„Irreversible Local Destruction“). Master, § 14 des Textvorschlags und Einbauordner bleiben unverändert, das Einbauskript liegt '
    'nur im Arbeitsbereich der Sitzung, seine Spezifikation in Fortsetzung 9 § 3.\n\n'
    '**Eigene Korrekturen in dieser Sitzung:** (1) Die Bewertung empfahl zu R1 Variante (a), ohne Klick gilt die registerkonforme '
    'Variante (b). (2) Die Planrechnung der Bewertung unterschätzte zwei Wortformen um je ein Wort (Q3-1, R3), gemessen 898 statt '
    '896. (3) Ein erster Lauf der LIESMICH-Ergänzung scheiterte an falsch maskierten Zeilenumbrüchen, ohne Schreibvorgang auf dem '
    'Rechner, neu erzeugt.\n\n'
    '**Stand der Dateien:** Neu im Arbeitsordner `03_Skripte\\Diskussion_Anwendung_2026-10-03\\`: `S4d_Zweitpruefung_Auftrag.md` '
    '(15.589 Byte), `S4d_Zweitpruefung_Bericht.md` (73.988 Byte, `af988b76…`), `S4d_Bewertung.md` (13.438 Byte, `e09aa9aa…`), '
    '`S4d_Textvorschlag_F2_2026-10-03.py` (110.671 Byte, `9fb8573f…`), `S4d_Textvorschlag.json` (15.944 Byte, `c6573d0e…`), '
    '`S4d_Saetze.csv`, `S4d_Textvorschlag.txt` · geändert `LIESMICH.md` (Abschnitt 4 d, 47.293 Byte, `a3738c15…`) · '
    '`04_Uebergaben\\Textvorschlag_6.2_6.3_2026-10-03.md` jetzt Fassung 2 (87.544 Byte, `be74fc66…`), Fassung 1 in '
    '`_Archiv\\_ersetzt_2026-10-03_Textvorschlag_6.2_6.3_F1\\` · neu `04_Uebergaben\\Uebergabe_Diskussion_Anwendung_Fortsetzung9_2026-10-03.md` '
    '(' + nu + ' Byte, `' + hu[:8] + '…`) mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev170_2026-10-03.py` mit `.txt` · '
    'Maßnahmenliste (Stand Rev. 170, Taskzeile 12, G37 (q), Summe) · diese Notizen (Rev. 170 auf Rev. 169), Teil 0 und '
    'Maßnahmenliste nur im Ordner. Unverändert: Master (`6c1db455…`), Kennzahlenblatt, T1, T4, S4a-, S4b- und S4c-Dateien, F17, '
    'Plan Rev. 5.\n\n'
    '**Offen beim Verfasser:** (1) Den Einbau ausdrücklich anweisen, mit dem Startprompt aus Fortsetzung 9 § 0 in einem neuen Task '
    'oder als Antwort in derselben Sitzung, oder § 1 des Textvorschlags selbst übertragen · (2) danach Endabgleich Fassung 3 und F9 '
    'im Master · (3) aus Rev. 152 bis 169 weiter offen: Task „Ergebnisse“ mit Fortsetzungsübergabe 6 (Rev. 169), Vormerkungen G37 '
    '(o) bis (q) für den Steuerdokumente-Task, Projektspeicher.\n\n'
    '**Nächster Schritt:** Fortsetzung 9: Master und Teil 0 frisch stagen, auf ausdrückliche Anweisung Einbau per Skript nach '
    'Fortsetzung 9 § 3 mit Sicherung des Masters in `_Archiv\\_ersetzt_2026-10-03_Master_vor_6.2`, Abgleich, Messskript Fassung 4 '
    'und Endabgleich Fassung 3 in `03_Skripte\\Einbau_6.2_2026-10-03\\`, § 14 des Textvorschlags nachtragen, Taskzeile 12 '
    'abschließen, Rev.-Block.\n\n')
assert SEMI not in REV
t2 = t.replace(anker, REV + anker)
open(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'), 'w', encoding='utf-8', newline='').write(t2)
LOG.append('Sitzungsnotizen: Eingang ' + '/'.join(info(NOTIZ)) + ', Rev. 170 über Rev. 169 eingesetzt, Ausgabe '
           + '/'.join(info(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'))))

m = open(MASS, encoding='utf-8').read()
alt_stand = '**Stand 02.10.2026, 23:42 Sitzungsuhr (Rev. 154 — '
assert m.count(alt_stand) == 1
m = m.replace(alt_stand, '**Stand 03.10.2026, 22:50 Sitzungsuhr (Rev. 170 — Task „Diskussion: Anwendung der Argumentationsstruktur“, '
              'Task 12b: Textvorschlag 6.2 und 6.3 Fassung 2 nach Zweitprüfung, freigegeben, Einbau an einer Kopie geprüft und '
              'offen, Taskzeile 12 und G37 (q)). Zuvor 02.10.2026, 23:42 Sitzungsuhr (Rev. 154 — ')
zeilen = m.split('\n')
i37 = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **G37 · Kapitelstruktur: Gliederung v6')]
i12 = [i for i, z in enumerate(zeilen) if z.startswith('| 12 Kapitel 6 (nach Gliederung v6')]
isum = [i for i, z in enumerate(zeilen) if z.startswith('| **Summe** | Rev. 154 (02.10.)')]
assert len(i37) == 1 and len(i12) == 1 and len(isum) == 1
G37Q = (' *(Rev. 170, 03.10.: (q) neu als Sammelvermerk aus dem Task „Diskussion: Anwendung der Argumentationsstruktur“ '
        '(Fortsetzungsübergaben 4 bis 8 je § 5, Textvorschlag 6.2 und 6.3 Fassung 2 § 11.2), für Fassung 18, Raster Rev. 4, '
        'T1, T4, Messskript und die Liste der überholten Teile: aus Fortsetzung 4 § 5 Nr. 6 die Liste aus Fortsetzung 2 § 5 Nr. 7, '
        'die Vormerkungen 1 bis 3 am Ende von § 4 des Ergebnisdokuments aus Schritt 3 und der Nachtrag 6.1 § 11 Nr. 2, 4, 6 und 7 '
        '(dort nachzulesen) · aus Fortsetzung 6: Berichtsraster 6.3.1 „Rechenkette …“ und Korpusbasis „0/13“ berichtigen (B13, B2), '
        'Berichtsraster 6.2.4, F17 § 11.3 und § 12 G4 auf die Werte von K-05.8 (B1), F17 § 12 G5 „505 links“ durch „505-Seitenmittel“ '
        '(B5), Register R14 Berichtsort an F17 § 13 Nr. 40 angleichen (B10), Spezifikation S18 nennt Moran et al. (2016), zitiert '
        'wird 2017 (B9) · aus Fortsetzung 7: Raster 7.4 ohne Fallzahl (K-b5), F17 § 4 „≥ 85 % auf Teilnehmerebene erfüllt“ gilt nur '
        'gesamt und F17 § 12 G5 ohne 5-m-Sprint (C3), S4a B4 teilweise überholt (C1), 6.2.10 d ohne Moher (T4), Raster 6.2.8 auf das '
        'berichtete Verfahren beschränken, TESTEX und Hilska nach K-b2 und K-b3 in F17 § 12, G26l und Plan Task 12 einheitlich führen '
        '· aus Fortsetzung 8 und der Zweitprüfung: F17 § 6.4 und § 6.5 und Raster 6.3.5 b ohne „gerätefrei“ in der Korpusaussage (D3), '
        'Raster 6.2.10 c ohne „bis zu 1,6 SD“ (D4), Raster 6.2.6 c „mehr als den SESOI“ (D9), T4-Nachtrag Cohen (1988, S. 43 bis 44) '
        'ohne Richtung (D1), Messskript Fassung 5 mit Belegerkennung für „ł“ und Namenspartikel (D10), Gerüst G4a Hopkins S. 13 (D2), '
        'Kennzahlenblatt Spalte Berichtsort K-09.2 bis K-09.4 und K-11.6 beim nächsten Erzeugerlauf (R29), Raster § 2.3 TESTEX 4: '
        '−1,68 ist K-04.11, im Analyseset bis −2,23 (R29), F17 § 12 G5 „gerichtet zugunsten der IG“ einschränken (R29), T1 `Moran2017` '
        'und `RC2020` mit Heftangaben, T1 `Hilska2021` Feld kapitel (Q8-3), T1 und T4 `Malina2014` „Reifezeitpunkt“ (Q1-1), '
        'Gerüst C7 und Q8-1 gegenstandslos (Sáez-Sáez de Villarreal et al., 2009, entfällt mit T1) · für Task 18: Spielklasse und '
        'McKay-Junior-Vorbehalt in 4.2 prüfen (C6, R16, R29), Erstverweis auf Tab. H6 in 4.1 (R7), Auswertungsplan § 5.4 Nr. 4 vor Tab. H6 '
        'berichtigen (R7), TESTEX ins Abkürzungsverzeichnis (R21), Umnummerierung 6.2 → 4.2 ohne Überschrift 6.3.)*')
assert SEMI not in G37Q
zeilen[i37[0]] = zeilen[i37[0]] + G37Q
z12 = zeilen[i12[0]]
assert z12.endswith(' |')
zeilen[i12[0]] = z12[:-2] + (
    ' · **12b (Rev. 155 bis 170, 03.10.):** Rasterzuordnung (S4a), Gerüst (S4b, Zielstufe 11), Textvorschlag 6.2 und 6.3 Fassung 1 '
    '(S4c, 895 Wörter), Zweitprüfung mit 50 Befunden und Fassung 2 (S4d, 898 Wörter), Freigabe nach Empfehlung (Weisung 03.10., '
    '22:15), Einbau an einer Kopie geprüft, Rückschreibung von der Umgebung gesperrt, offen: Einbau mit Abgleich, Messskript und '
    'Endabgleich nach Fortsetzungsübergabe 9, danach 12b erledigt, Vormerkungen Kapitel 7 in Textvorschlag 6.2 und 6.3 § 11.1 (13a) |')
zs = zeilen[isum[0]]
pre = '| **Summe** | '
assert zs.startswith(pre)
zeilen[isum[0]] = pre + ('Rev. 170 (03.10.): Taskzeile 12 fortgeschrieben (12b), G37 (q) neu als Sammelvermerk, keine neuen Punkte, '
                         'Zählung nicht neu erhoben. Zuvor: ') + zs[len(pre):]
m2 = '\n'.join(zeilen)
assert SEMI not in m2.replace(m, '') or True
open(os.path.join(AUS, 'Massnahmenliste_Datenverarbeitung.md'), 'w', encoding='utf-8', newline='').write(m2)
LOG.append('Maßnahmenliste: Eingang ' + '/'.join(info(MASS)) + ', Stand-Zeile, G37 (q), Taskzeile 12 und Summe fortgeschrieben, '
           'Ausgabe ' + '/'.join(info(os.path.join(AUS, 'Massnahmenliste_Datenverarbeitung.md'))))
LOG.append('Fortsetzungsübergabe 9: ' + nu + ' Byte, MD5 ' + hu)
open(os.path.join(AUS, 'Steuerung_Rev170_2026-10-03.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(LOG) + '\n')
print('\n'.join(LOG))
assert SEMI not in open(os.path.abspath(__file__), encoding='utf-8').read()

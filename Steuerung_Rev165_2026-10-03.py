# Steuerung_Rev165_2026-10-03.py - Rev.-Block in Teil 0 der Sitzungsnotizen (Task "Ergebnisse: Abgleich mit der
# Argumentationsstruktur und Ueberarbeitung", Teilschritt 2 (d) abgeschlossen, Taskwechsel zu Fortsetzung 4).
# Aufruf: python3 Steuerung_Rev165_2026-10-03.py <Notizen ein> <Notizen aus> <Uhrzeit> <Projektsatz> <Rueckschreibesatz> <Uebergabe 4> [<Protokoll>]
# Die Rev.-Nummer ist die naechste freie nach dem obersten Block in Teil 0. Kein Semikolon im Skript.
import sys, re, hashlib, pathlib
ein, aus, zeit, projekt, rueck, ue4 = [sys.argv[i] for i in range(1, 7)]
proto = pathlib.Path(sys.argv[7]) if len(sys.argv) > 7 else None
ue4_b = pathlib.Path(ue4).read_bytes()
ue4_angabe = '(' + format(len(ue4_b), ',').replace(',', '.') + ' Byte, MD5 `' + hashlib.md5(ue4_b).hexdigest()[:8] + '…`)'
t = pathlib.Path(ein).read_text(encoding='utf-8')
md5_ein = hashlib.md5(pathlib.Path(ein).read_bytes()).hexdigest()
revs = [int(x) for x in re.findall(r'^### ⭐⭐ NEU \(Rev\. (\d+),', t, re.M)]
if not revs:
    sys.exit('kein Rev.-Block gefunden')
rev = max(revs) + 1
if revs[0] != max(revs):
    sys.exit('oberster Block ist nicht der neueste')
BLOCK = '''### ⭐⭐ NEU (Rev. ‹REV›, 03.10.2026, ‹ZEIT› Sitzungsuhr, Auftrag 03.10., Beginn mit der Stagung um 15:52, Startprompt aus Fortsetzungsübergabe 3 § 0): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Teilschritt 2 (d) abgeschlossen und gesichert, Taskwechsel nach erneuter automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Teilschritt 2 (e), kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung3_2026-10-03.md` § 0: Teilschritt 2 (d), jede Korpusaussage, auf die sich ein Potenzial stützen soll, direkt an der Anlage `…_Saetze.csv` unabhängig nachzählen, als Teiltabelle 2d per Skript und als § 3.4 des Abgleichbefunds, mit den Punkten aus Fortsetzung 3 § 5 Nr. 4, dazu die qualitative Inferenz bei Klusemann et al. (2012) und Beato et al. (2018) am Volltext. Danach 2 (e), dann Schritt 3. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.

**Ergebnis:** (1) **Teilschritt 2 (d)** (abgeschlossen 17:55, gesichert 18:31): `nachzaehlung_2d.py` zählt jede Korpusaussage, auf die sich ein Potenzial aus den Zwischenständen von § 3.2 und § 3.3 stützt, an der Anlage nach, ohne Funktionen der früheren Skripte, mit Handurteilen als Tabellen und Prüfausdrücken am Satztext, und prüft die Lesart an den Volltexten von Klusemann (2012), Beato (2018), Lloyd (2016), Negra (2019) und Moran (2024) mit pdftotext (28 Zitate, Seiten, Beato-Zeilen, Beato Tab. 1, Negra Tab. 4), die Urteile in Lloyd Abb. 1 und Beato Abb. 2 von Hand am gerenderten Bild. Lauf im Spiegel und aus dem gestagten Claude-Ordner bytegleich. Teiltabelle 2d (Abgleichbefund § 3.4, 21 Zeilen): bestätigt 14, abweichend 2, ungenau 5. Abweichend: Befund § 3.5 mit 2a.33 (der Kern liest Nullbefunde gegen die SWC als Kategorie) und § 6.4 mit 2b.37 (den Fall C1 hat Klusemann im Text, der Kern in Objekten). „unclear“ bezeichnet bei Klusemann, Lloyd, Negra 2019 und über die Chancen bei Beato ein 90-%-Intervall über beide Schwellen von ± 0,2 SD, „substantial“ ist bei Beato nicht definiert. (2) **Statusfolge für 2c** (Vermerk am Ende von § 3.3): 2c.21 und 2c.22 auf „abgewandelt“ statt „nur erweitert“ (Kernbausteine Beato 4.1, Lloyd 4.2, Negra 2019 2.8, ohne Kernvorbild der Fall C1 im Text), 2c.41 bleibt für den Fall C1 „nur erweitert“, dazu Berichtigungen zu 2c.5, 2c.8, 2c.43 und 2c.47. 2c je Satz danach: abgewandelt 14, nur erweitert 8, 19 Sätze mit 311 von 450 Wörtern nutzen einen Kernbaustein. (3) **Zweitprüfung** der ersten Fassung durch einen unabhängigen Subagenten: A 3 · B 5 · C 10, eingearbeitet bis auf C10 (Richtungsformeln aus 2c.17, nur bei Bedarf in Schritt 3), seine Reproduktion bytegleich. A-Befunde: Statusfolge 2c.21 und 2c.22 · die Kandidatensuche für parallele Werte übersah Bezeichnungen mit eigener Klammer (häufigste Kernform, 19 Sätze in 5 Studien, Zuordnungswort für Werte 7 in 4) · Hilska 6.4 ohne Inzidenzen je Gruppe. Für Schritt 3 trägt 2 (d): A2 S4 hat für die Bezugsfolge im vorigen Satz kein Vorbild, lösbar mit einer Bezeichnung je Wert, einem Zuordnungswort oder der Bezugsfolge im Satz · den Fall C1 je Zielgröße in der Klammer und einmal für mehrere Zielgrößen belegt der Korpus beide · ein eigener Satz zum unadjustierten Vergleich vor dem Modellergebnis hat kein Vorbild · eine Zusatzanalyse nach allen Befunden hat ein erweitertes Vorbild (Asimakidis 1.6), eine Datenprüfung nie. (4) **Rückschreibung:** Um 17:55 war der Rechner nicht erreichbar, die neun Dateien lagen ab 18:02 als Sicherung im Chat. Nach der Wiederverbindung um 18:30 aus `sicherung_2d_1757` zurückgeschrieben (Abgleichbefund und `LIESMICH.md` mit `expectedMtimeMs`), neu gestagt und per MD5 bestätigt, 9 von 9 gleich. (5) **Verfasser im Chat um 18:29:** „Die Erkenntnisse sollen in den Text einfließen. Welche Schritte folgen logischerweise als nächstes?“ Beantwortet mit der Schrittfolge 2 (e), Schritt 3 mit Klickfrage, Schritt 4 Absatz für Absatz und Abschluss mit den Folgeänderungen für 6.1, aufgenommen in Fortsetzung 4 § 2 Nr. 2 und in den Startprompt. Keine Freigabe eines Potenzials, keine Registeränderung. (6) **Fortsetzungsübergabe 4** mit neuem Startprompt (§ 0), den Dateien (§ 1.3), den offenen Klicks (§ 3), dem ersten Arbeitsgang von 2 (e) (§ 4, mit dem Master nach Rev. 163) und den Punkten für 2 (e) und Schritt 3 (§ 5 Nr. 4).

**Eigene Korrekturen in dieser Sitzung:** (1) Lloyd S. 1244 statt 1243 (PDF-Seite 6). (2) Beato Tab. 1 reicht über die PDF-Seiten 20 und 21. (3) Die Klammerentfernung in der Zielgrößenfolge löschte die Liste in Negra 2019 2.8, entfernt. (4) Lloyd 4.1 als Quantor über alle Tests nachgetragen, alle Quantorwörter nach ihrem Bereich klassifiziert. (5) Zeilen für die Ordnung nach Zielgröße (K6) und für Resümee und Hypothese (§ 0 Nr. 4) ergänzt.

**Stand der Dateien:** Neu: in `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` die Dateien `nachzaehlung_2d.py` (111.744 Byte, MD5 `1aa0d933…`), `nachzaehlung_2d.txt`, `teiltabelle_2d.csv`, `teiltabelle_2d.md`, `zweitpruefung_2d.md` und `zweitpruefung_2d_nachrechnung.py` mit `.txt`, der Ordner hat jetzt 49 Dateien · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung4_2026-10-03.md` ‹UE4› mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev‹REV›_2026-10-03.py` mit `.txt` · ‹PROJEKT› Geändert: `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (199.382 Byte, MD5 `0558e2a9…`, § 0, Vermerk am Ende von § 3.3, § 3.4 neu, § 3.5 folgt in 2 e, § 5), der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung · `LIESMICH.md` des Arbeitsordners (Abschnitt Schritt 2 d, 10.350 Byte) · diese Notizen (Rev. ‹REV› auf Rev. ‹VORHER›), nur im Ordner. Von diesem Task nicht geändert: Master (seit Rev. 163 durch den parallelen Task geändert, `6c1db455…`), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Befund zur Argumentationsstruktur (Berichtigungen zu § 3.5, § 3.6 und § 6.4 vorgemerkt in Fortsetzung 4 § 5 Nr. 7), Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). ‹RUECK›

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung4_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 164 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ ab Schritt 4 (b) mit Fortsetzungsübergabe 6, F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 4 ab Teilschritt 2 (e): Anschluss von Kapitel 5 an 4.2, 4.4, 4.6, 4.7, 6.1 und die Teile aus Abgleichbefund § 1.4 gegen den Master mit 6.1 nach Rev. 163 (Teiltabelle 2e, Abgleichbefund § 3.5), kompakt, danach im selben Task Schritt 3 mit der Klickfrage zu den Potenzialen, über die die Erkenntnisse aus 2 (d) und 2 (e) in den Text einfließen, dann Schritt 4.

'''
block = BLOCK.replace('‹REV›', str(rev)).replace('‹VORHER›', str(max(revs))).replace('‹ZEIT›', zeit).replace('‹PROJEKT›', projekt).replace('‹RUECK›', rueck).replace('‹UE4›', ue4_angabe)
if chr(59) in block or '‹' in block:
    sys.exit('Semikolon oder Platzhalter im Block')
i = t.index('### ⭐⭐ NEU (Rev. ' + str(max(revs)) + ',')
t2 = t[:i] + block + t[i:]
alt = '**Stand: '
j = t2.index(alt)
if j > 200:
    sys.exit('Standzeile nicht am Anfang')
t2 = t2[:j + len(alt)] + '(Rev. ' + str(rev) + ' — siehe Block oben.) Zuvor: ' + t2[j + len(alt):]
pathlib.Path(aus).write_text(t2, encoding='utf-8')
b = pathlib.Path(aus).read_bytes()
zeilen = ['Steuerung Rev. ' + str(rev), 'Eingang ' + ein + ' ' + str(len(pathlib.Path(ein).read_bytes())) + ' Byte MD5 ' + md5_ein,
          'Ausgang ' + aus + ' ' + str(len(b)) + ' Byte MD5 ' + hashlib.md5(b).hexdigest(), 'oberster Block vorher Rev. ' + str(max(revs)) + ', neu Rev. ' + str(rev)]
if proto:
    proto.write_text('\n'.join(zeilen) + '\n', encoding='utf-8')
print('\n'.join(zeilen))

# Steuerung_Rev169_2026-10-03.py - Rev.-Block in Teil 0 der Sitzungsnotizen (Task "Ergebnisse: Abgleich mit der
# Argumentationsstruktur und Ueberarbeitung", Schritt 3 mit Klickergebnis abgeschlossen, Taskwechsel zu Fortsetzung 6).
# Aufruf: python3 Steuerung_Rev169_2026-10-03.py <Notizen ein> <Notizen aus> <Uhrzeit> <Projektsatz> <Rueckschreibesatz> <Uebergabe 6> [<Protokoll>]
# Die Rev.-Nummer ist die naechste freie nach dem obersten Block in Teil 0. Sie muss mit der Angabe in der
# Fortsetzungsuebergabe 6 uebereinstimmen ("Teil 0: Rev. n." und "ab Rev. n,"), sonst bricht das Skript ab.
# Kein Semikolon im Skript.
import sys, re, hashlib, pathlib
ein, aus, zeit, projekt, rueck, ue6 = [sys.argv[i] for i in range(1, 7)]
proto = pathlib.Path(sys.argv[7]) if len(sys.argv) > 7 else None
ue6_b = pathlib.Path(ue6).read_bytes()
ue6_t = ue6_b.decode('utf-8')
ue6_angabe = '(' + format(len(ue6_b), ',').replace(',', '.') + ' Byte, MD5 `' + hashlib.md5(ue6_b).hexdigest()[:8] + '…`)'
t = pathlib.Path(ein).read_text(encoding='utf-8')
md5_ein = hashlib.md5(pathlib.Path(ein).read_bytes()).hexdigest()
revs = [int(x) for x in re.findall(r'^### ⭐⭐ NEU \(Rev\. (\d+),', t, re.M)]
if not revs:
    sys.exit('kein Rev.-Block gefunden')
rev = max(revs) + 1
if revs[0] != max(revs):
    sys.exit('oberster Block ist nicht der neueste')
if ('Teil 0: Rev. ' + str(rev) + '.') not in ue6_t or ('ab Rev. ' + str(rev) + ',') not in ue6_t:
    sys.exit('Rev. ' + str(rev) + ' passt nicht zur Fortsetzungsuebergabe 6')
BLOCK = '''### ⭐⭐ NEU (Rev. ‹REV›, 03.10.2026, ‹ZEIT› Sitzungsuhr, Auftrag 03.10. mit dem Startprompt aus Fortsetzungsübergabe 5 § 0, Stagung ab etwa 20:49): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Schritt 3 abgeschlossen: sechs Potenziale mit Kürzungspaaren vorgelegt, Klickergebnis (Potenziale 1, 3, 4 und 6 freigegeben), Registerzeilen 17 und 18, Taskwechsel nach automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Schritt 4, kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung5_2026-10-03.md` § 0: Schritt 3, Potenziale auf höchstens einer Seite, priorisiert (A trägt den Bericht, B Leseführung, C Stil), je mit Grundlage und Häufigkeit im Korpus, Wortbilanz, Folge für 6.1 und weitere Teile und möglichem Konflikt mit dem Entscheidungsregister oder einer Projektregel, gestützt auf die Kandidatenliste in Fortsetzung 5 § 5 Nr. 4, dazu zwei Zeilen, was der Text schon leistet, dann die Klickfragen mit Mehrfachauswahl, danach Schritt 4 Absatz für Absatz und der Abschluss mit den Folgeänderungen. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.

**Ergebnis:** (1) **Textstand:** Master neu gestagt und unverändert seit Rev. 163 (40.337 Byte, MD5 `6c1db455…`, keine comments.xml), Kapitel 5 zeichengleich mit dem Textstand (450 Wörter, 29 Sätze). Rev. 168 des parallelen Tasks gelesen, sein Textvorschlag 6.2 und 6.3 steht nicht im Master. (2) **Potenzialseite** per `potenziale_3.py` (80 Zitate am Ort, jede neue Zahl am Kennzahlenblatt, Satzregeln je neuem Satz, Sachprüfungen an Tab. H1a, Tab. H4c und K-10.12, Bilanz je Variante und je Schritt mit jedem Paar im selben Schritt, Lauf unter anderem `PYTHONHASHSEED` und im Spiegel des Ordners ohne Argumente bytegleich): sechs Potenziale, 1 Schmerzmeldungen mit Bezugsmenge 15 und Status (A), 2 Menge im Quantor von A5 S6 (A), 3 Folge Sprint, Richtungswechsel, Sprung in A4 S2 (B), 4 deskriptive Zielgrößen vor die Befunde (B, nimmt eine Stellung aus Textvorschlag 5 mit neuem Grund zurück), 5 Untergrenzen den Schwellen zuordnen (B), 6 mediane Adhärenz als eigener Satz (C), mit den Kürzungen a bis d, Empfehlung 448 Wörter. (3) **Klick** des Verfassers (vor 21:29): freigegeben 1 mit den Kürzungen b und c, 3, 4 und 6 · nicht freigegeben 2 mit a (abweichend von der Empfehlung) und 5 mit d · alle drei Gruppen „Belassen“ (Stellung, Wortlaut, Form) als Entscheidung ins Register. Kapitel 5 nach der Freigabe 448 Wörter, 31 Sätze, Median 14,0, längster Satz 28. Schrittfolge für Schritt 4: A1 wortgleich, A2 (450), A3 mit Kürzung b in A5 S11 (449), A4 (448), A5 (448), A6 wortgleich. (4) **Abgleichbefund § 4** mit Potenzialseite (§ 4.1), Klickergebnis, Schrittfolge und Satznummern-Konkordanz (§ 4.2), Registerzeilen 17 (Freigabe), 17a (Stellung von A5 S11), 17b (Registerzeile 10u und Textvorschlag 5 § 9.1 Nr. 4 in Kapitel 5 gelöst), 18a bis 18c (Belassen) (§ 4.3) und Folgen und Vormerkungen (§ 4.4). (5) **Folgen für andere Teile:** Von den 30 Bezugssätzen von 6.1 ändern 24 eine Bezugskennung, 19 nur durch Umnummerierung, inhaltlich berührt ist nur 6.1 A6 S2 (Folgeänderung beim Abschluss wie vorgemerkt). **Hinweis an den parallelen Task:** Im Textvorschlag 6.2 und 6.3 nennt A5 S5 die Größe des Bestwert-Bias nach dem Inhalt gruppiert („beim 30-m-Sprint und Standweitsprung … beim 505-Test je Seite …“). Kapitel 5 A4 S2 folgt nach Potenzial 3 der Folge Sprint, Richtungswechsel, Sprung (F17 § 5.1), entscheiden muss der parallele Task. Im S4b-Gerüst betrifft es C2 und G5a im Wortlaut und G6c in der Kennung (A2 S4 wird A2 S5), im Textvorschlag 6.2 und 6.3 A1 S6, A5 S4 und A5 S5 im Wortlaut und A2 S3, A3 S5 und A6 S4 in der Kennung (Liste in `potenziale_3.txt` § 6). (6) **Neue Vormerkungen:** K-10.9 steht künftig auch im Text (Berichtsort im Kennzahlenblatt nachführen) · die Titel von Tab. H2a, H2c und H5 sagen „vollständig durchgeführte“ gegen Textvorschlag 5 § 10 Nr. 3 (Task 18, G38) · die Satzende-Regel für Fassung 18 präzisieren (Ziffer oder einzelner Großbuchstabe, G37 p). (7) **Taskwechsel** nach automatischer Zusammenfassung des Verlaufs am Checkpoint nach Schritt 3: Fortsetzungsübergabe 6 mit neuem Startprompt (§ 0), Ergebnis und Dateien (§ 1), Klickergebnissen (§ 2), offenen Klicks (§ 3), Schritt 4 mit A1 und A2 als erstem Arbeitsgang (§ 4) und Besonderheiten mit dem freigegebenen Wortlaut und den Prüfpunkten für Schritt 4 (§ 5).

**Eigene Korrekturen in dieser Sitzung:** (1) Die Schrittfolge des ersten Entwurfs legte Potenzial 2 und seine Kürzung a in zwei Schritte, vor der Vorlage berichtigt, das Skript prüft die Paarregel je Schritt. (2) Nach der Vorlage am Objekt nachgeprüft: Auch der Titel von Tab. H5 sagt „vollständig durchgeführten“ (die Chatmeldung nannte nur H2a und H2c). (3) Im Skript berichtigt: Zahlenmuster für eine Dezimalzahl vor einem Komma, ein abgeschnittenes Zitat zum S4b-Punkt G1g, Abschnittssuche am letzten Überschriftentreffer statt im Inhaltsverzeichnis, die Zwei der Wochendeckelung als Konstante statt als Kennung, die Bezugstabelle von 6.1 ohne die Konkordanztabelle darunter. (4) Vor der Vorlage verworfen: Kürzung d mit −6 statt −7, der Mediansatz vor A2 S2 (dann bezöge sich „das“ auf den Median), A5 S3 hinter das Modellergebnis (bräche „damit“), die 45,4 % als Kürzung (Berichtsort Text), „geprüft und nicht verworfen“ im Wortlaut (schlösse die Linearität ein).

**Stand der Dateien:** Neu: in `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` die Dateien `potenziale_3.py` (43.827 Byte, MD5 `2b1cc9d6…`), `potenziale_3.txt`, `potenziale_3.json` und `potenziale_3.md`, der Ordner hat jetzt 61 Dateien · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung6_2026-10-03.md` ‹UE6› mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev‹REV›_2026-10-03.py` mit `.txt` · ‹PROJEKT›. Geändert: `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (257.513 Byte, MD5 `c87ea796…`, Stand-Zeile, § 0, § 4 neu), der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung · `LIESMICH.md` des Arbeitsordners (Abschnitt Schritt 3, 15.139 Byte) · diese Notizen (Rev. ‹REV› auf Rev. ‹VORHER›), nur im Ordner. Von diesem Task nicht geändert: Master (`6c1db455…`), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Befund zur Argumentationsstruktur, Maßnahmenliste (Nachführung am Ende des Tasks, Fortsetzung 6 § 5 Nr. 9). ‹RUECK›

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung6_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 168 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ mit Fortsetzungsübergabe 8 (Zweitprüfung und Klicks zum Textvorschlag 6.2 und 6.3), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 6 ab Schritt 4: Master, Teil 0 und Abgleichbefund frisch stagen und Änderungen seit Rev. 163 prüfen (eingebaute 6.2 und 6.3 des parallelen Tasks eingeschlossen), dann den Textvorschlag `04_Uebergaben\\Textvorschlag_5_Ueberarbeitung_2026-10-03.md` mit A1 (wortgleich) und A2 (Potenzial 6) anlegen, Zweitprüfung, Vorlage, Klickfreigabe, danach A3 mit Kürzung b in A5 S11, A4, A5, A6 und der Abschluss mit den Folgeänderungen je Abschnitt.

'''
block = BLOCK.replace('‹REV›', str(rev)).replace('‹VORHER›', str(max(revs))).replace('‹ZEIT›', zeit).replace('‹PROJEKT›', projekt).replace('‹RUECK›', rueck).replace('‹UE6›', ue6_angabe)
if chr(59) in block or '‹' in block or '›' in block:
    sys.exit('Semikolon oder Platzhalter im Block')
i = t.index('### ⭐⭐ NEU (Rev. ' + str(max(revs)) + ',')
t2 = t[:i] + block + t[i:]
alt = '**Stand: '
j = t2.index(alt)
if j > 200:
    sys.exit('Standzeile nicht am Anfang')
t2 = t2[:j + len(alt)] + '(Rev. ' + str(rev) + ' — siehe Block oben.) Zuvor: ' + t2[j + len(alt):]
if t2.replace(block, '', 1).replace('(Rev. ' + str(rev) + ' — siehe Block oben.) Zuvor: ', '', 1) != t:
    sys.exit('Eingriff ausserhalb von Block und Standzeile')
pathlib.Path(aus).write_text(t2, encoding='utf-8')
b = pathlib.Path(aus).read_bytes()
zeilen = ['Steuerung Rev. ' + str(rev), 'Eingang ' + ein + ' ' + str(len(pathlib.Path(ein).read_bytes())) + ' Byte MD5 ' + md5_ein,
          'Ausgang ' + aus + ' ' + str(len(b)) + ' Byte MD5 ' + hashlib.md5(b).hexdigest(), 'oberster Block vorher Rev. ' + str(max(revs)) + ', neu Rev. ' + str(rev),
          'Uebergabe 6 ' + ue6 + ' ' + str(len(ue6_b)) + ' Byte MD5 ' + hashlib.md5(ue6_b).hexdigest()]
if proto:
    proto.write_text('\n'.join(zeilen) + '\n', encoding='utf-8')
print('\n'.join(zeilen))

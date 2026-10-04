# Steuerung_Rev167_2026-10-03.py - Rev.-Block in Teil 0 der Sitzungsnotizen (Task "Ergebnisse: Abgleich mit der
# Argumentationsstruktur und Ueberarbeitung", Teilschritt 2 (e) abgeschlossen, Taskwechsel zu Fortsetzung 5).
# Aufruf: python3 Steuerung_Rev167_2026-10-03.py <Notizen ein> <Notizen aus> <Uhrzeit> <Projektsatz> <Rueckschreibesatz> <Uebergabe 5> [<Protokoll>]
# Die Rev.-Nummer ist die naechste freie nach dem obersten Block in Teil 0. Sie muss mit der Angabe in der
# Fortsetzungsuebergabe 5 uebereinstimmen ("Teil 0: Rev. n." und "ab Rev. n,"), sonst bricht das Skript ab.
# Kein Semikolon im Skript.
import sys, re, hashlib, pathlib
ein, aus, zeit, projekt, rueck, ue5 = [sys.argv[i] for i in range(1, 7)]
proto = pathlib.Path(sys.argv[7]) if len(sys.argv) > 7 else None
ue5_b = pathlib.Path(ue5).read_bytes()
ue5_t = ue5_b.decode('utf-8')
ue5_angabe = '(' + format(len(ue5_b), ',').replace(',', '.') + ' Byte, MD5 `' + hashlib.md5(ue5_b).hexdigest()[:8] + '…`)'
t = pathlib.Path(ein).read_text(encoding='utf-8')
md5_ein = hashlib.md5(pathlib.Path(ein).read_bytes()).hexdigest()
revs = [int(x) for x in re.findall(r'^### ⭐⭐ NEU \(Rev\. (\d+),', t, re.M)]
if not revs:
    sys.exit('kein Rev.-Block gefunden')
rev = max(revs) + 1
if revs[0] != max(revs):
    sys.exit('oberster Block ist nicht der neueste')
if ('Teil 0: Rev. ' + str(rev) + '.') not in ue5_t or ('ab Rev. ' + str(rev) + ',') not in ue5_t:
    sys.exit('Rev. ' + str(rev) + ' passt nicht zur Fortsetzungsuebergabe 5')
BLOCK = '''### ⭐⭐ NEU (Rev. ‹REV›, 03.10.2026, ‹ZEIT› Sitzungsuhr, Auftrag 03.10., Beginn mit der Stagung um 18:45, Startprompt aus Fortsetzungsübergabe 4 § 0): Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“ — Teilschritt 2 (e) abgeschlossen und gesichert, Taskwechsel nach erneuter automatischer Zusammenfassung des Verlaufs, Fortsetzung ab Schritt 3, kein Manuskripttext

**Auftrag:** Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung4_2026-10-03.md` § 0: Teilschritt 2 (e), Anschluss von Kapitel 5 an Kapitel 4 (4.2, 4.4, 4.6, 4.7), an 6.1 und an jeden weiteren Teil aus Abgleichbefund § 1.4 (gleiche Begriffe, keine wörtliche Doppelung, keine Aussage, die Kapitel 5 nicht trägt), geprüft am Master in seinem gültigen Stand (6.1 seit Rev. 163 mit dem eingebauten Nachtrag des parallelen Tasks), als Teiltabelle 2e per Skript und als § 3.5 des Abgleichbefunds, mit den Punkten aus Fortsetzung 4 § 5 Nr. 4. Danach im selben Task Schritt 3 mit der Klickfrage zu den Potenzialen, dann Schritt 4. Es gelten Schritte, Regeln, Sicherung und Taskwechsel des Startprompts in § 0 der Ausgangsübergabe.

**Ergebnis:** (1) **Teilschritt 2 (e)** (abgeschlossen 20:25, gesichert 20:26): Master unverändert seit Rev. 163 (40.337 Byte, MD5 `6c1db455…`, keine comments.xml), Kapitel 5 zeichengleich mit dem Textstand (450 Wörter, 29 Sätze), 6.1 zeichengleich mit der Fassung 3 des Textvorschlags 6.1. `anschluss_2e.py` (Fassung 2) prüft den Anschluss mit systematischer Suche: gemeinsame Wortfolgen ab vier Wörtern und gemeinsame Wortstämme zwischen den 29 Sätzen von Kapitel 5 und den 259 Sätzen außerhalb, 36 Begriffe je Teil, die Folge Sprint, Richtungswechsel, Sprung (18 Sätze, 13 in fester Folge, innerhalb der Regel weicht nur A4 S2 ab), die Spielerzahlen in Kapitel 4 und die Aussagen von 6.1 am Kennzahlenblatt. Handurteile mit Prüfbedingungen, 179 Zitate am Ort, jede Satzkennung aufgelöst und am Master geprüft, Lauf im Spiegel und aus dem gestagten Claude-Ordner bytegleich. Teiltabelle 2e (Abgleichbefund § 3.5, 28 Zeilen): erfüllt 17, teilweise 10, nicht erfüllt 1, mit einem Teil „bewusst anders“ 3. Schwere B: „lag nahe null“ in 6.1 (2e.6, 2e.8), 6.1 A6 S2 (2e.11), Folge in A4 S2 (2e.19). Bezug auf Kapitel 5 haben nach Rev. 163 30 von 40 Sätzen von 6.1 (vorher 24), Liste in `bezuege_2e.md`, Vermerke am Ende von § 1.4 und § 3.2 (2b.8, 2b.29). Über Kapitel 5 hinaus geht „lag nahe null“: Gemessen am SESOI liegt der Punktschätzer beim 30-m-Sprint bei 0,71, beim 505-Seitenmittel bei 0,60 SESOI, nur beim Standweitsprung nahe null, und für Punktschätzer hat 4.7 keine Regel (Folgeänderung für 6.1 per Klick beim Abschluss). 6.1 A6 S2 stützt sich auf die Bezugsmenge 15 aus Tab. H2 und auf „vollständig durchgeführt“, das Textvorschlag 5 § 10 Nr. 3 für Kapitel 5 verwarf. Vormerkungen für 4.6, 4.7 („H0“, „unschlüssig“), 4.4.2, 4.4.1, Einleitung B5 S4 und Anhang H stehen in Fortsetzung 5 § 5 Nr. 8. (2) **Zweitprüfung** der ersten Fassung durch einen unabhängigen Subagenten mit eigener Nachrechnung (103 Werte, 101 gleich, 161 von 161 Zitaten, Reproduktion bytegleich): A 0 · B 5 · C 14, alle eingearbeitet. (3) **Nachlauf** um 20:36 gegen den gesicherten Abgleichbefund: Teiltabelle und Bezugsliste bytegleich, in `anschluss_2e.txt` ändert sich nur die Eingangszeile des Abgleichbefunds. (4) **Fortsetzungsübergabe 5** mit neuem Startprompt (§ 0), Ergebnis und Dateien (§ 1), offenen Klicks (§ 3), Schritt 3 als erstem Arbeitsgang (§ 4), der Kandidatenliste für Schritt 3 (§ 5 Nr. 4), der Zuordnung der Zeilennummern im Bericht der Zweitprüfung (§ 5 Nr. 6) und den Vormerkungen aus 2 (e) (§ 5 Nr. 8).

**Eigene Korrekturen in dieser Sitzung:** (1) Erwartete Prüfzahlen am Text berichtigt (Adhärenz in 4.7, „als vollständig“ in 6.1, Beanspruchung in 4.6, Folge 18 und 13 mit B1b S4). (2) Eine Schleifenvariable überschrieb die Liste zu K-10.12, umbenannt. (3) Zwei Zitate am Ort berichtigt. (4) Das Definitionszitat zum sRPE-Load zitiert jetzt 4.6 A1 S8 statt Fassung 17. (5) Registerkennungen V6, V7, V8 und U6. (6) Geschachtelte Anführungszeichen in fünf Zitaten entfernt. (7) Wortgrenze bei „abhängige Variable“. (8) Im Entwurf von § 3.5 ein zu weiter Satz zu A2 S4 gestrichen.

**Stand der Dateien:** Neu: in `03_Skripte\\Abgleich_Ergebnisse_2026-10-03\\` die Dateien `anschluss_2e.py` (99.027 Byte, MD5 `d54b947c…`), `anschluss_2e.txt`, `teiltabelle_2e.csv`, `teiltabelle_2e.md`, `bezuege_2e.md`, `zweitpruefung_2e.md` und `zweitpruefung_2e_nachrechnung.py` mit `.txt`, der Ordner hat jetzt 57 Dateien · `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung5_2026-10-03.md` ‹UE5› mit dem neuen Startprompt (§ 0) · `03_Skripte\\Steuerung_Rev‹REV›_2026-10-03.py` mit `.txt` · ‹PROJEKT›. Geändert: `02_Befunde\\Abgleich_Ergebnisse_Argumentationsstruktur_2026-10-03.md` (242.439 Byte, MD5 `aa2fd4f7…`, Stand-Zeile, § 0, Vermerke am Ende von § 1.4 und § 3.2, § 3.5 neu, § 5), der Abgleichbefund hat keine Projektkopie, es gilt die Ordnerfassung · `LIESMICH.md` des Arbeitsordners (Abschnitt Schritt 2 e, 12.810 Byte) · diese Notizen (Rev. ‹REV› auf Rev. ‹VORHER›), nur im Ordner. Von diesem Task nicht geändert: Master (`6c1db455…`), Textvorschläge, Kennzahlenblatt, T1, T4, Fassung 17, Bauplan, Berichtsraster, Stilprofil, Plan Rev. 5, Befund zur Argumentationsstruktur (Berichtigungen vorgemerkt, Fortsetzung 5 § 5 Nr. 7), Maßnahmenliste (Nachführung am Ende des Tasks, Übergabe § 7 Nr. 3). ‹RUECK›

**Offen beim Verfasser:** (1) Den Task mit dem Startprompt aus `04_Uebergaben\\Uebergabe_Abgleich_Ergebnisse_Fortsetzung5_2026-10-03.md` § 0 in einem neuen Task fortsetzen · (2) aus Rev. 152 bis 166 weiter offen: Fortsetzung des Tasks „Diskussion: Anwendung der Argumentationsstruktur“ mit Fortsetzungsübergabe 7 (Freigabe des Gerüsts, Schritt 4 c), F9 im Master, Vormerkungen G37 (o) und (p) für den Steuerdokumente-Task, Projektspeicher.

**Nächster Schritt:** Fortsetzung 5 ab Schritt 3: Master, Teil 0, Abgleichbefund und das S4b-Gerüst des parallelen Tasks frisch stagen und Änderungen seit Rev. 163 prüfen, dann die Potenzialseite (höchstens eine Seite, A, B, C, je mit Grundlage und Häufigkeit im Korpus, Wortbilanz mit Kürzungspaar, Folge für 6.1 und weitere Teile, Registerkonflikt) aus der Kandidatenliste in Fortsetzung 5 § 5 Nr. 4, die Klickfragen, danach § 4 des Abgleichbefunds und Rev.-Block, dann Schritt 4 mit A1.

'''
block = BLOCK.replace('‹REV›', str(rev)).replace('‹VORHER›', str(max(revs))).replace('‹ZEIT›', zeit).replace('‹PROJEKT›', projekt).replace('‹RUECK›', rueck).replace('‹UE5›', ue5_angabe)
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
          'Uebergabe 5 ' + ue5 + ' ' + str(len(ue5_b)) + ' Byte MD5 ' + hashlib.md5(ue5_b).hexdigest()]
if proto:
    proto.write_text('\n'.join(zeilen) + '\n', encoding='utf-8')
print('\n'.join(zeilen))

import pathlib, hashlib, datetime
U = pathlib.Path('/mnt/user-data/uploads/Bachelorarbeit/Claude')
O = pathlib.Path('/mnt/user-data/outputs')
D = pathlib.Path('/tmp/claude-0/-home-claude/520514b1-8490-5649-b2dc-ebe1e177adbb/scratchpad/doc')
fails = []
def rep(s, old, new, name, n=1):
    if s.count(old) != n:
        if s.count(old) == 0 and s.count(new) == 1:
            return s   # bereits angewendet (Teile der Übergabe, zweiter Lauf)
        fails.append((name, old[:70], s.count(old))); return s
    return s.replace(old, new)

now = datetime.datetime.utcnow() + datetime.timedelta(hours=1)   # Sitzungsuhr = UTC+1
HM = now.strftime('%H:%M')
HM_ML = (now + datetime.timedelta(minutes=5)).strftime('%H:%M')

# ================= Übergabe: Teile auf Rev. 117 und Gliederung v6 =================
p0 = (D / 'part0.md').read_text(encoding='utf-8')
p0 = rep(p0, '**Stand:** 28.09.2026, Sitzungsuhr, Rev. 116 in Teil 0',
         '**Stand:** 28.09.2026, Sitzungsuhr (Sitzung 20:55 bis 23:10), Rückschreibung in den Ordner 29.09.2026, Rev. 117 in Teil 0', 'P0 Stand')
p0 = rep(p0, 'sechs Prüfberichte je Zug (Sitzung 28.09., Rev. 116), `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (71) und `T4_zitierfallen.csv` (148), Gliederung v5 § 3.2,',
         'sechs Prüfberichte je Zug (Sitzung 28.09., Rev. 117), `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (71) und `T4_zitierfallen.csv` (148), Gliederung v6 § 3.2 (`01_Verfahren\\Gliederung_2026-09-28`, seit Rev. 116, die Zug-Tabelle der Einleitung ist gegenüber v5 unverändert),', 'P0 Grundlage')
p0 = rep(p0, 'Zuerst Teil 0 der Sitzungsnotizen (Rev. 116), dann § 6 dieses Dokuments per Klick entscheiden',
         'Zuerst Teil 0 der Sitzungsnotizen (Rev. 117), dann § 6 dieses Dokuments per Klick entscheiden', 'P0 Startsatz')
p0 = rep(p0, '6. Für jeden Zug der Einleitung nach Gliederung v5 die Quellen mit der höchsten Relevanz identifizieren',
         '6. Für jeden Zug der Einleitung nach `Gliederung_2026-09-28` (zum Zeitpunkt des Auftrags v5, seit Rev. 116 v6 mit unveränderter Zug-Tabelle § 3.2) die Quellen mit der höchsten Relevanz identifizieren', 'P0 Auftrag 6')
p0 = rep(p0, '### 1.2 Diagnose des Textvorschlags vom 28.09. (Messung, Skript in der Sitzung Rev. 116)',
         '### 1.2 Diagnose des Textvorschlags vom 28.09. (Messung, Skript in der Sitzung Rev. 117)', 'P0 1.2')
p0 = rep(p0, 'Die Ablösung geht in Teil 0 (Rev. 116), in die Maßnahmenliste (G35) und mit der nächsten Fassung in die Projektanweisungen § 6.5.',
         'Die Ablösung geht in Teil 0 (Rev. 117), in die Maßnahmenliste (G35 k) und mit der nächsten Fassung in die Projektanweisungen § 6.5 (Steuerdokumente-Task G37).', 'P0 Ablösung')
(D / 'part0.md').write_text(p0, encoding='utf-8')

p48 = (D / 'part4_8.md').read_text(encoding='utf-8')
p48 = rep(p48, 'Die Wortzahlen des Textvorschlags vom 28.09. (Gliederung v5 § 3.2, gemessen) stehen zum Vergleich.',
          'Die Wortzahlen des Textvorschlags vom 28.09. (Gliederung v6 § 3.2, unverändert aus v5, gemessen) stehen zum Vergleich.', 'P48 § 5')
old = '**Nächster Schritt.** Startsatz in § 0. Vor dem ersten Satz Fließtext: Klicks 6.1 bis 6.5, 6.7, 6.8, Antwort auf 6.6, dann Stichpunktgerüst je Zug zur Freigabe.'
new = ('**Rückschreibung und Parallelstand (29.09.).** Am 28.09. ab 23:00 Sitzungsuhr war der Rechner nicht erreichbar, das Dokument wurde als Datei im Chat und als Projektkopie geliefert. Die Rückschreibung in den Ordner erfolgte am 29.09. aus einem eigenen Ausgabepfad mit MD5-Prüfung (Teil 0, Rev. 117). Parallel zu diesem Task lief am 28.09. der Task Kapitelstruktur (Rev. 116, 22:10 Sitzungsuhr): Gliederung v6 (`01_Verfahren\\Gliederung_2026-09-28`, 13 statt 22 Überschriften) ersetzt v5, die Einleitung bleibt dort ein Kapitel ohne Unterabschnitte mit höchstens 1.500 Wörtern und die Zug-Tabelle § 3.2 ist unverändert. Für dieses Dokument ändert sich dadurch nichts. Gliederung v6 § 0 Nr. 4 und M24 nennen noch die Übertragung des Textvorschlags vom 28.09., sie werden im Steuerdokumente-Task (G37) nachgezogen.\n\n'
       '**Nächster Schritt.** Startsatz in § 0. Vor dem ersten Satz Fließtext: Klicks 6.1 bis 6.5, 6.7, 6.8, Antwort auf 6.6, dann Stichpunktgerüst je Zug zur Freigabe.')
if 'Rückschreibung und Parallelstand' not in p48:
    p48 = rep(p48, old, new, 'P48 § 8')
(D / 'part4_8.md').write_text(p48, encoding='utf-8')

parts = ['part0.md','part3_12.md','part3_3.md','part3_4.md','part3_5.md','part3_678.md','part4_8.md']
ueb = ''.join((D / f).read_text(encoding='utf-8') for f in parts)
(D / 'Uebergabe_Einleitung_Quellenraster_2026-09-28.md').write_text(ueb, encoding='utf-8')
(O / 'rb_05').mkdir(parents=True, exist_ok=True)
(O / 'rb_05' / 'Uebergabe_Einleitung_Quellenraster_2026-09-28.md').write_text(ueb, encoding='utf-8')
assert 'Rev. 116 in Teil 0' not in ueb and 'Sitzungsnotizen (Rev. 116)' not in ueb

# ================= Sitzungsnotizen (Basis: Rev. 116 der Parallelsitzung) =================
src = U / '00_Steuerung' / 'Cowork_Sitzungsnotizen.md'
s = src.read_text(encoding='utf-8')
assert hashlib.md5(src.read_bytes()).hexdigest() in ('93632bf37c94b9521595a7113d3f2111','4c2dc836e0e6e0adb87d92c65acb15ce')
s = rep(s, '**Stand: (Rev. 116 — siehe Block oben.) Zuvor: (Rev. 115',
        '**Stand: (Rev. 117 — siehe Block oben.) Zuvor: (Rev. 116 — siehe Block oben.) Zuvor: (Rev. 115', 'SN Stand')
block = f'''### ⭐⭐ NEU (Rev. 117, 29.09.2026, {HM} Sitzungsuhr, Sitzung vom 28.09., 20:55 bis 23:10 Sitzungsuhr): Task „Einleitung Quellenraster“ — Verfasser: Einleitung nicht zufriedenstellend, passgenaue Referenz ist Killerkriterium · Belegprüfung aller 74 Volltexte · Übergabe `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` für die Neuformulierung · Textvorschlag Einleitung vom 28.09. wird nicht übertragen · Rückschreibung am 29.09.

**Einordnung:** Dieser Task lief am 28.09. abends parallel zum Task Kapitelstruktur (Rev. 116, 22:10 Sitzungsuhr). Er war um 23:10 fertig, der Rechner war ab 23:00 nicht erreichbar (Bridge getrennt, zwei Versuche), die Rückschreibung folgte am 29.09. beim nächsten Kontakt auf den Stand von Rev. 116, den die Parallelsitzung um 06:20 Sitzungsuhr noch einmal fortschrieb (G37 i erledigt). Beide Blöcke gelten, dieser ist der jüngere. Gliederung v6 ändert an der Einleitung nichts (ein Kapitel ohne Unterabschnitte, höchstens 1.500 Wörter, Zug-Tabelle § 3.2 unverändert), die Übergabe Quellenraster verweist auf v6.

**Auftrag (Verfasser, 28.09., gegen 20:55 Sitzungsuhr, 21:43 „aufgabe abschließen ohne nachfrage“):** Die Einleitung (Textvorschlag Rev. 114) ist nicht zufriedenstellend: roter Faden erkennbar, Argumentationskette schlüssig, Lesefluss begrenzt, sprachliche Formulierung unzureichend. Vorgaben: wissenschaftlich akribisch, Fachbegriffe aus der Literatur, Präzision des Argumentationsstrangs, Literatur gezielter, **passende Quelle = passende Kohorte und Leistungsparameter bei Anforderungen, Belastungen und Fähigkeiten, Killerkriterium, keine Erwachsenenprofile für den Jugendfußball**, akribisch im Ordner recherchieren und verifizieren, keine Plagiatssätze, je Zug der Gliederung die Quellen mit der höchsten Relevanz. Zuerst ein Dokument, die Neuformulierung in einem neuen Task. Master unverändert (48.791 Byte, MD5 e35315d6…, keine `comments.xml`).

**Erledigt:**
- 74 PDFs aus `Ideen und Studien` als Text (pdftotext -layout, Seitenwechsel als Formfeed) und in sechs parallelen Subagenten je Zug am Volltext geprüft (Briefing: Fundstelle gedruckt und PDF, Wortlaut, Population, Art eigener Befund/Relais/Definition/Meinung, Passung 0/1/2, T4 gelesen), dazu die Diagnose des Textvorschlags vom 28.09. per Skript (1.321 Wörter, 68 Sätze, 49 Belegklammern in 48 Sätzen = 71 %, Median 20 Wörter je Satz, zehn Sätze mit Quelle als Subjekt, sieben Modalisierungen).
- Übergabe `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` (rund 22.800 Wörter, Projektkopie `claude/`): § 0 Startsatz · § 1 Auftrag, Diagnose, Belegbefund je Absatz (was ausscheidet, was ersetzt) mit der Ablösung früherer Festlegungen · § 2 Regeln: Passgenauigkeit in drei Aussageklassen (Anforderung/Belastung/Fähigkeit → Population 0 Pflicht · Definition/Konzept/Verfahren → frei · Wirksamkeit → Quellenart und Population im Satz), Relais-Regel ohne Sekundärzitat, Konvergenz, Sprach-, Terminologie- und Plagiatsregeln · § 3 Quellenraster je Zug (81 Zeilen: Aussage, Quelle mit Fundstelle, englischer Prüfwortlaut, Population/Art/Passung, Formulierungsstärke, Vorbehalt und Gegenbefund, je Zug „Nicht verwenden“ mit Grund und Lücke) · § 4 Lücken und Beschaffungsposten in drei Stufen · § 5 Bauplan mit Zielwortzahl je Zug (Summe 1.430 von 1.500) · § 6 acht Klickfragen mit Empfehlung · § 7 T1- und T4-Nachträge · § 8 Ablage, Zweitprüfung, Rückschreibung und Parallelstand.
- Zweitprüfung durch einen unabhängigen Subagenten (24 Kernzeilen und 52 weitere am Wortlaut, zwölf Zahlenblöcke exakt): 1 A, 9 B, 22 C, alle eingearbeitet (A: Ablösung der Verbleibsliste und von G33 c ausdrücklich ausgesprochen · B: Nimphius nur als Erwachsenenkontrast, Morgan Passung 1/2 nur als Gegenbefund, RC 2020 einheitlich Passung 1, Havanecz ohne Seitendarstellung, Vor-2020-Halbsatz für Hammami und Beato, Relais-Regel nach § 7.1, vollständige Quellenliste, neun Aussage-Zellen als [Übersetzung, umbauen] markiert).

**Kernbefunde der Belegprüfung:** (1) Elf der 49 Belegklammern des Textvorschlags tragen ihre Aussage nicht (Turner & Stewart 2014 und Stølen 2005 Erwachsene · Oliver 2024 S. 624 „1.350 Aktionen“ und „Spielerfolg“ als Erwachsenenrelais auf Mohr 2003 · Zheng 2025 Sprintlängen als Relais auf Haugen 2014 · Hicks 2020 S. 2 Meinung · Dos’Santos 2018 Verletzungsbezug nur Erwachsene und Mädchen · Silva 2016 „4–6 Wochen“ ohne Beleg, Sprungbefund vergleicht reduziertes Training mit Karenz · Moran 2017 PHV-Zahl Relais · RC 2023 S. 11 Mechanismus im Absatz zur Maximalkraft mit Sale 1988). (2) Passgenau für das Nachwuchsspiel trägt nur Algroy et al. (2021, Tab. 1, U14), für die Niveaudiskriminanz nur Dugdale et al. (2019: SBJ r = 0,75, 505 r = 0,54, 10 m r = 0,02 als Pflichtgegenbefund), für die U15-Messgüte Dugdale (505 ICC 0,85, SBJ 0,95) mit Taylor 2018 als Gegenbefund. (3) Padrón-Cabo et al. (2025, U15, 15 Tage Winterpause: Sprint und Sprung schlechter, 505 nicht nachweisbar) fehlt im Textvorschlag und kommt hinein. Keine Quelle im Ordner ist passgenau für Detraining 13- bis 16-Jähriger in einer Sommerpause. (4) Kein Anpassungsmechanismus ist für 13- bis 15-Jährige belegt, alle Listen führen auf Markovic & Mikulic 2010 (Erwachsene), Radnor et al. (2018, OF-S. 10–11) benennen die Übertragungslücke. (5) Keine Datei im Ordner verbindet unbeaufsichtigtes, heimbasiertes oder videobasiertes Plyometrietraining mit einer Interventionsstudie, alle Korpusstudien betreut: die Lücke ist am Ordner bestätigt, als Korpuseigenschaft zu formulieren. (6) Die Reifemoderation ist uneinheitlich (Lloyd 2016 prä > post, Moran 2017 Mitte kleiner bei p = 0,09, RC 2023 kein Unterschied außer COD, Bouafif post > prä, Behm Kinder > Adoleszente), RC 2023 poolt circa-PHV-Gruppen in post, die Phase um den Gipfel ist nirgends ausgewertet. (7) „Vergleichsevidenz überwiegend Tier 3“ trägt nur für Oliver 2024, bei RC 2020 gemischt (19 von 33 „Moderate“), bei Zheng unberichtet. Oliver zählt regionale tunesische Mannschaften als Tier 3, die eigene Tier-2-Zuordnung braucht Spielklasse und Trainingsumfang (Rückfrage 6.6). (8) Der Kurzprogramm-Nullbefund für 10 m (RC 2020) hängt an fünf Gruppen, darunter Nakamura 2012 (Erwachsene, Off-Season) [ABGELEITET]. (9) T1-Fehler: Ferguson 2024 ICC3,1 statt 2,1 · Mujika & Padilla liegt als Volltext vor · Moran „PHV um 14“ Ms.-S. 5 · RC 2020 Ms.-S. 12 · Behm „alle betreut“ nicht im Text · Asimakidis Offset −0,8 prä, −0,1 post. 24 neue T4-Zitierfallen (Übergabe § 7).

**Ablösung früherer Festlegungen durch den Auftrag (Übergabe § 1.3):** Verbleibsliste vom 28.09. (Palucci Vieira, Algroy, Parr, nach Klick Price bleiben oder kehren zurück) · G33 c für Dugdale, Ferguson, Havanecz, Sammoud 2021 und Nimphius in Zug 1 und 2 · Zug-3-Liste um Padrón-Cabo 2025 ergänzt. Mit Fassung 18 in § 6.5 nachziehen (G35 k, im Steuerdokumente-Task G37). Die Übertragung des Textvorschlags vom 28.09. entfällt, der Altbestand Kapitel 2 und 3 bleibt bis zur Übertragung der neuen Einleitung im Master. Gliederung v6 § 0 Nr. 4 und M24 („Übertragung steht aus“) sind insoweit überholt und werden mit G37 nachgezogen.

**Klickfragen für den neuen Task (Übergabe § 6, Empfehlung jeweils zuerst):** 6.1 Verletzungssatz streichen (kein Nachwuchsbeleg) · 6.2 Silva 2016 streichen · 6.3 PHV-Zahl mit Malina & Kozieł (2014, S. 426) · 6.4 Rössler 2014 streichen (12,7 % Jungen, abweichend vom Klick 14:36, deshalb erneut gestellt) · 6.5 Neuformulierung aus dem Ordner, Beschaffung parallel · 6.6 Rückfrage Spielklasse und Trainingsumfang der drei Mannschaften · 6.7 Mechanismussatz streichen · 6.8 Richtungswechselhäufigkeit mit Havanecz und Morgan als Gegenbefund.

**Stand der Dateien:** Neu: Übergabe Quellenraster (Ordner und Projektkopie). Geändert: diese Notizen (Rev. 117 auf Rev. 116), Maßnahmenliste (G34 b, G35 a, i, k, l, G37 Vermerk, H12, I20, Zusammenfassung Zeile 7), Plan (Nachtrag Rev. 117, Block C, § 0, § 8 Startsatz, keine neue Revision). Rückschreibung am 29.09. je Datei aus eigenem Ausgabepfad (`rb_05` bis `rb_08`), danach neu gestagt und per MD5 verglichen. Projektkopien: Übergabe Quellenraster, Sitzungsnotizen, Maßnahmenliste, Plan. Master unverändert. Die Prüfberichte je Zug, die Zweitprüfung der Übergabe und die Textfassungen der PDFs lagen nur im Sitzungsspeicher, ihre Befunde stehen in der Übergabe § 3 und § 7.

**Offen beim Verfasser:** (1) `Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt (aus Rev. 115 und 116) · (2) Skill-Vorschlag speichern (G26g, beim nächsten Stand auf Gliederung v6, G37 h) · (3) **neu:** Task „Einleitung neu“ mit dem Startsatz aus Übergabe Quellenraster § 0 starten, dort Klicks 6.1 bis 6.8 und Antwort auf 6.6 (Spielklasse und Trainingsumfang der drei Mannschaften). Der Punkt „die Einleitung in den Master übertragen (Task 7 neu, Rev. 114)“ aus Rev. 115 und 116 entfällt.

**Nächster Schritt:** Task „Einleitung neu“ (Startsatz Übergabe Quellenraster § 0): Klicks, Stichpunktgerüst je Zug zur Freigabe, Textvorschlag mit Zug-Tabelle, Belegtabelle, Zweitprüfung gegen Wortlaut und Volltexte, Kürzungsleiter, dann Übertragung und Abgleich (Übergabe Einleitung § 8 Nr. 6 sinngemäß: Messskript, Endabgleich, Maßnahmenliste, T1, T4, Plan, Projektkopien), Rev. 118. Danach der Steuerdokumente-Task zur Kapitelstruktur (G37: Berichtsraster Rev. 4, Plan Rev. 6, Fassung 18 mit G35 k, Messskript Fassung 4, Nachtragsvermerk Bauplan § 1, Gliederung v6 § 0 Nr. 4 und M24), danach Task 11 (Kapitel 5 als ein Kapitel ohne Unterabschnitte) mit dem Startsatz aus Plan § 8, Nr. 23 per Klick zu Beginn.

'''
anchor = '### ⭐⭐ NEU (Rev. 116, 28.09.2026, 22:10 Sitzungsuhr'
s = rep(s, anchor, block + anchor, 'SN block')
(O / 'rb_06').mkdir(parents=True, exist_ok=True)
(O / 'rb_06' / 'Cowork_Sitzungsnotizen.md').write_text(s, encoding='utf-8')

# ================= Maßnahmenliste (Basis: Rev. 116 der Parallelsitzung) =================
src = U / '00_Steuerung' / 'Massnahmenliste_Datenverarbeitung.md'
m = src.read_text(encoding='utf-8')
assert hashlib.md5(src.read_bytes()).hexdigest() in ('5e6ecb0deb0dfe218d71f5c43611bc73','17add3f3d73f985a15e4a3137c1dfa7f')
m = rep(m, '**Stand 28.09.2026, 22:10 Sitzungsuhr, entspricht 23:10 MESZ (Rev. 116 — Task Kapitelstruktur:',
        f'**Stand 29.09.2026, {HM_ML} Sitzungsuhr (Rev. 117 — Task „Einleitung Quellenraster“, Sitzung 28.09. 20:55 bis 23:10 parallel zu Rev. 116, Rückschreibung 29.09.: Belegprüfung aller 74 Volltexte, Übergabe `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` für die Neuformulierung der Einleitung, Textvorschlag vom 28.09. wird nicht übertragen. G35 (k) und (l) neu, G35 (a) und (i), G34 (b) und G37 fortgeschrieben, H12 und I20 neu, Zusammenfassung Zeile 7 neu). Zuvor 28.09.2026, 22:10 Sitzungsuhr, entspricht 23:10 MESZ (Rev. 116 — Task Kapitelstruktur:', 'ML Stand')
old = 'Hilska 2021 für G5, Lloyd 2016 nach L14 b).)*'
new = ('Hilska 2021 für G5, Lloyd 2016 nach L14 b).)* *(Rev. 117, 29.09., Sitzung 28.09.: (a) der Textvorschlag Einleitung vom 28.09. wird nicht übertragen, der Verfasser hat ihn als nicht zufriedenstellend bewertet (Belege ohne passende Population, Lesefluss), Task 7 neu wird als Task „Einleitung neu“ nach `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` (Startsatz § 0 dort) neu geschrieben, Übergabe Einleitung § 8 Nr. 6 gilt sinngemäß erst nach der neuen Einleitung · (i) Spielklasse und Trainingsumfang der drei Mannschaften als Rückfrage 6.6 im neuen Task, bis zur Antwort „leistungsorientierter Breitensport“ ohne Tier-Nummer · (k) neu: Ablösung früherer Festlegungen durch den Auftrag (Übergabe Quellenraster § 1.3): Verbleibsliste vom 28.09. für Palucci Vieira, Algroy, Parr und nach Klick Price · G33 c für Dugdale, Ferguson, Havanecz, Sammoud 2021 und Nimphius in Zug 1 und 2 · Zug-3-Liste um Padrón-Cabo 2025 ergänzt, mit Fassung 18 in § 6.5 nachziehen (G37 c) · (l) neu: acht Klickfragen 6.1 bis 6.8 der Übergabe zu Beginn des neuen Tasks (Verletzungssatz, Silva, PHV-Zahl, Rössler, Beschaffung, Spielklasse, Mechanismussatz, Richtungswechselhäufigkeit), Empfehlungen dort.)*')
m = rep(m, old, new, 'ML G35')
old = '§ 12 G8 und § 13 · (b) mit Task 7 neu · (c) Hilska 2021 für Task 12.)*'
new = '§ 12 G8 und § 13 · (b) mit Task 7 neu · (c) Hilska 2021 für Task 12.)* *(Rev. 117, 29.09., Sitzung 28.09.: (b) Rössler 2014 in der Einleitung als Klickfrage 6.4 der Übergabe Quellenraster erneut gestellt, Empfehlung streichen nach dem Killerkriterium des Verfassers (12,7 % Jungen, konfundiert), Olivier 2026 bleibt Kernquelle · der Verletzungssatz nach Dos’Santos 2018 ist nur Erwachsenenrelais, Klickfrage 6.1 · Machbarkeit über McBurnie, Parr, et al. 2022 nur als Meinung aus dem Akademiekontext, dazu Ramirez-Campillo et al. 2023 S. 2 und Olivier 2026 S. 2, Silva 2016 nach Klick 6.2.)*'
m = rep(m, old, new, 'ML G34')
old = '(i) erledigt 29.09., 06:20: Word geschlossen, die v6-.docx im Ordner, per MD5 geprüft *(28.09., Rev. 116, (i) am 29.09.)*'
new = '(i) erledigt 29.09., 06:20: Word geschlossen, die v6-.docx im Ordner, per MD5 geprüft *(28.09., Rev. 116, (i) am 29.09.)* *(Rev. 117, 29.09.: Der Steuerdokumente-Task folgt nach Übertragung und Abgleich der neuen Einleitung (Task „Einleitung neu“ nach `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md`), nicht nach der Übertragung des Textvorschlags vom 28.09. Dort zusätzlich nachziehen: Gliederung v6 § 0 Nr. 4 und M24 (Übertragung des Textvorschlags entfällt), Fassung 18 § 6.5 nach G35 (k).)*'
m = rep(m, old, new, 'ML G37')
old = '\n---\n\n## I  KORREKTUREN AN DEN PROJEKTDOKUMENTEN'
new = ('- [ ] **H12 · Beschaffungsposten aus der Belegprüfung der Einleitung (28.09., Übergabe Quellenraster § 4):** Stufe 1 (würde je einen Satz der Einleitung passgenauer machen, für die Neuformulierung nicht nötig, Klick 6.5): Waldron & Murphy (2013, Pediatr Exerc Sci 25, 423–434, Laufprofil U14 elite gegen sub-elite) · Trecroci et al. (2018, J Hum Kinet 61, 209–216, Niveaudiskriminanz U15) · Reilly, Williams, Nevill & Franks (2000, J Sports Sci 18, 695–702) · Clemente, Ramirez-Campillo & Sarmento (2021, Sports Med 51, 795–814, = H5, Referenzquelle von Padrón-Cabo 2025 und Liu 2024) · Philippaerts et al. (2006, J Sports Sci 24, Längsschnitt Fußball, PHV und Leistung) · Asadi et al. (2018, drei Reifegruppen). Stufe 2 für 4.4, 6.1 und 6.2: Buchheit et al. 2010, Buchheit & Mendez-Villanueva 2014, Rumpf et al. 2011, Meyers et al. 2019, Buchheit et al. 2014, McCunn et al. 2016, Parr et al. 2020, Artero et al. 2012, España-Romero et al. 2010, Keiner et al. 2021, Comfort et al. 2014, Pereira et al. 2020, Meylan et al. 2014, Nakamura et al. 2012, Thomas et al. 2009, Randers et al. 2014, Malina et al. 2015, Baxter-Jones et al. 2005, Vera-Assaoka et al. 2020 (vollständig in § 4 der Übergabe). Stufe 3 (Relais-Ziele, nicht beschaffen): Pucsok 2021 (Nicht-aufnehmen-Liste), Schmidtbleicher 1992, Sale 1988, Positionspapiere NSCA und CSEP, ACSM 2018. *(Sitzung 28.09., Rev. 117)*\n'
       '\n---\n\n## I  KORREKTUREN AN DEN PROJEKTDOKUMENTEN')
m = rep(m, old, new, 'ML H12')
old = '- [x] **I10 · Ordnerfassung der Sitzungsnotizen aus dem Projektdokument erneuern**'
new = ('- [ ] **I20 · T1- und T4-Nachträge aus der Belegprüfung der Einleitung (Übergabe Quellenraster § 7):** T1: Ferguson2024 ICC3,1 statt 2,1 · Mujika2000 Volltext im Ordner · RC2020 „maturity is often not reported“ Ms.-S. 12 · Moran2017 „PHV um 14“ Ms.-S. 5, Zitierjahr 2017 · Behm2017 „alle betreut“ am Text nicht belegbar · Manou2022 Offset −0,8 prä und −0,1 post, Niveau offen, Aktivität gemessen · PadronCabo2025 Kapitelvermerk 1 · Radnor2017 und Hicks2019 Zitierjahre · neue Steckbriefe Malina2014 (nach Klick 6.3) und Prüfung des Kapitelvermerks 1 für alle Quellen des Rasters. T4: 24 neue Zitierfallen (Tabelle § 7 der Übergabe), darunter Vieira2019 und Parr2022 neu, RC2023 Dichotomisierung circa-PHV in post und S. 11 Relais Sale 1988, RC2020 Kurzprogramm-Subgruppe mit Nakamura 2012, Silva2016 „4–6 weeks“ ohne Beleg, Havanecz2026 „10 km“ fehlbelegt, Zheng2025 und Sammoud2024 McKay-Fehlbeleg, Negra2019 und Negra2020 Fehlbelege, Algroy2021 Einleitungszahlen, Oliver2024 Relais auf Review und Negra 2020 als Tier 3. Per Skript `T4_Nachtrag_⟨Datum⟩.py` zu Beginn des Tasks „Einleitung neu“ oder in Task 15. *(Sitzung 28.09., Rev. 117)*\n'
       '- [x] **I10 · Ordnerfassung der Sitzungsnotizen aus dem Projektdokument erneuern**')
m = rep(m, old, new, 'ML I20')
old = '| 7 neu: Einleitung (Kapitel 1 bis 3 zusammengelegt, höchstens 1.500 Wörter, ersetzt 7 bis 10 und den Einleitungsteil von 14) | G35 (a), (e), (g), (i) · G34 (b), (c) · G33 (a), (b), (e) · G32 (a), (e) · G26e · G13g · J2 · K19 und G31 (c) · G18c · G19c |'
new = '| 7 neu: Einleitung neu (Neuformulierung nach `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md`, Rev. 117, der Textvorschlag vom 28.09. wird nicht übertragen, Kapitel 1 bis 3 zusammengelegt, höchstens 1.500 Wörter, ersetzt 7 bis 10 und den Einleitungsteil von 14) | G35 (a), (e), (g), (i), (k), (l) · G34 (b), (c) · G33 (a), (b), (e) · G32 (a), (e) · G26e · G13g · J2 · K19 und G31 (c) · G18c · G19c · H12 (Stufe 1 optional, Klick 6.5) · I20 |'
m = rep(m, old, new, 'ML Zusammenfassung 7')
old = '| **Summe** | **Rev. 116 (28.09.), per Skript an den Kästchen gezählt:'
new = '| **Summe** | Rev. 117 (29.09., Sitzung 28.09.): H12 und I20 neu, G35 (k) und (l) neu, Zählung nicht neu erhoben. Zuvor: **Rev. 116 (28.09.), per Skript an den Kästchen gezählt:'
m = rep(m, old, new, 'ML Summe')
(O / 'rb_07').mkdir(parents=True, exist_ok=True)
(O / 'rb_07' / 'Massnahmenliste_Datenverarbeitung.md').write_text(m, encoding='utf-8')

# ================= Plan (Basis unverändert seit Rev. 115) =================
src = U / '04_Uebergaben' / 'Plan_Weitere_Schritte_2026-09-25.md'
p = src.read_text(encoding='utf-8')
assert hashlib.md5(src.read_bytes()).hexdigest() == '2efde8e9374692d2fe7a8320207e01d4'
old = '\n## 0 Ergebnis in Kürze'
new = ('\n**Nachtrag 29.09.2026 (Rev. 117 der Sitzungsnotizen, Sitzung 28.09.), keine neue Revision des Plans:** Der Textvorschlag Einleitung vom 28.09. (Rev. 114) wird nicht übertragen. Der Verfasser bewertete ihn als nicht zufriedenstellend (Belege ohne passende Population, Lesefluss) und legte fest: Eine passgenaue Referenz ist Killerkriterium, mit Anforderungs- oder Belastungsprofilen von Erwachsenen wird im Jugendfußball nicht argumentiert. Task 7 neu wird als **Task „Einleitung neu“** nach `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` neu geschrieben (Startsatz § 0 dort, Regeln § 2, Quellenraster je Zug § 3, Zielwortzahl je Zug § 5 mit Summe 1.430, acht Klickfragen § 6, Rückfrage Spielklasse 6.6). Der Stand Rev. 114 in Block C, der Startsatz für Task 7 neu in § 8 und der Abgleich nach Übergabe Einleitung § 8 Nr. 6 gelten in dieser Form nicht mehr, der Abgleich folgt sinngemäß nach der neuen Einleitung. Parallel entstand am 28.09. die Gliederung v6 (Rev. 116, G37): Die Einleitung bleibt dort unverändert, Kapitel 5 wird ein Kapitel ohne Unterabschnitte, 6.2 und 6.3 ein Abschnitt. Reihenfolge: Einleitung neu → Übertragung und Abgleich → Steuerdokumente-Task (G37, Plan Rev. 6) → Task 11. Maßnahmen G35 (k), (l), H12, I20.\n'
       '\n## 0 Ergebnis in Kürze')
p = rep(p, old, new, 'Plan Nachtrag')
old = 'Nächster Schritt ist die Übertragung der Einleitung und ihr Abgleich (Task 7 neu), danach Task 11. Die Punkte 0 bis 6 sind der Stand vom 25.09.'
new = 'Nächster Schritt ist die Übertragung der Einleitung und ihr Abgleich (Task 7 neu), danach Task 11. Die Punkte 0 bis 6 sind der Stand vom 25.09. *(Rev. 117, 29.09.: Die Übertragung des Textvorschlags vom 28.09. entfällt, nächster Schritt ist Task „Einleitung neu“, siehe Nachtrag im Kopf.)*'
p = rep(p, old, new, 'Plan § 0')
old = 'Die Tasks 7 bis 10 der Rev. 4 (Kürzung 2.4, 2.3, 2.1, 2.2) sind durch Task 7 neu ersetzt, ihre Beschreibungen stehen in Rev. 4 im Archiv.'
new = 'Die Tasks 7 bis 10 der Rev. 4 (Kürzung 2.4, 2.3, 2.1, 2.2) sind durch Task 7 neu ersetzt, ihre Beschreibungen stehen in Rev. 4 im Archiv. *(Rev. 117, 29.09.: überholt. Der Textvorschlag wird nicht übertragen, die Einleitung wird als Task „Einleitung neu“ nach `04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md` neu formuliert: Eingang dort § 2 bis § 5, Klickpunkte § 6, Budget 1.500 mit Zielsumme 1.430, Ausgang Textvorschlag mit Zug-Tabelle, Belegtabelle, Zweitprüfung gegen Wortlaut und Volltexte, Kürzungsleiter, danach Übertragung und Abgleich sinngemäß nach Übergabe Einleitung § 8 Nr. 6.)*'
p = rep(p, old, new, 'Plan Block C')
old = '(Textvorschlag liegt vor, nach der Übertragung weiter mit Übergabe Einleitung § 8 Nr. 6.) Die Startsätze der Tasks 7 bis 10 der Rev. 4 gelten nicht mehr.'
new = ('(Textvorschlag liegt vor, nach der Übertragung weiter mit Übergabe Einleitung § 8 Nr. 6.) Die Startsätze der Tasks 7 bis 10 der Rev. 4 gelten nicht mehr. *(Rev. 117: gilt nicht mehr, ersetzt durch den folgenden Startsatz.)*\n'
       '- **Task „Einleitung neu“ (ersetzt Task 7 neu, Rev. 117):** „Task „Einleitung neu“: Neuformulierung der Einleitung nach `Claude\\04_Uebergaben\\Uebergabe_Einleitung_Quellenraster_2026-09-28.md`. Zuerst Teil 0 der Sitzungsnotizen (Rev. 117), dann § 6 dieses Dokuments per Klick entscheiden, dann Stichpunktgerüst je Zug mit Quelle, Fundstelle und Formulierungsstärke zur Freigabe, erst danach Fließtext. Budget höchstens 1.500 Wörter, Zielwortzahl je Zug nach § 5. Jeder Satz mit Anforderungs-, Belastungs- oder Fähigkeitsaussage trägt eine Quelle der Passung 0 (§ 2.1). Zweitprüfung durch einen Subagenten gegen die Wortlaut-Spalten dieses Dokuments (Übersetzungsplagiat) und gegen die Volltexte (Quellentreue), bevor der Vorschlag vorgelegt wird.“')
p = rep(p, old, new, 'Plan § 8')
(O / 'rb_08').mkdir(parents=True, exist_ok=True)
(O / 'rb_08' / 'Plan_Weitere_Schritte_2026-09-25.md').write_text(p, encoding='utf-8')

print('FAILS', fails)
print('Sitzungsuhr', HM)
for d in ['rb_05/Uebergabe_Einleitung_Quellenraster_2026-09-28.md','rb_06/Cowork_Sitzungsnotizen.md','rb_07/Massnahmenliste_Datenverarbeitung.md','rb_08/Plan_Weitere_Schritte_2026-09-25.md']:
    b = (O / d).read_bytes(); print(d, len(b), hashlib.md5(b).hexdigest())
print('Uebergabe Wörter', len(ueb.split()))

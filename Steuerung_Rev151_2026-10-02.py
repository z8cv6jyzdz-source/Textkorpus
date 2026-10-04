# -*- coding: utf-8 -*-
"""
Steuerung_Rev151_2026-10-02.py — Fortschreibung von Teil 0 (Rev. 151), Maßnahmenliste und Plan
Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext.

Anlass: Task „Boumparis“ nach Plan Nachtrag 02.10. (Startsatz § 8) mit dem Prompt
04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md. Ergebnis: Analysebefund, Nachtrag K2 mit Zweitprüfung,
Klickfreigabe des Moduls A2-M (Variante A) und der Vormerkung für die Einleitung (Gegenbefund in Absatz 3), T1 und T4.

Aufruf: python Steuerung_Rev151_2026-10-02.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Plan.md> <Nachtrag_K2.md> <Ausgabeordner> <HH:MM>
Jede Ersetzung muss genau einmal greifen, sonst Abbruch. Schreibt die drei Steuerdateien neu in den Ausgabeordner
und das Protokoll (Größen, MD5, Ersetzungen, Semikola) nach stdout und in Steuerung_Rev151_2026-10-02.txt.
Ohne Semikolon im Skript (chr(59)).
"""
import sys, os, hashlib

SEMI = chr(59)
NOTIZEN, LISTE, PLAN, NACHTRAG, AUS, UHR = sys.argv[1:7]


def md5(b):
    return hashlib.md5(b).hexdigest()


def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Abbruch: %s greift %d-mal statt einmal' % (name, n))
    protokoll.append('  %s: 1 Ersetzung' % name)
    return text.replace(alt, neu)


kb = open(NACHTRAG, 'rb').read()
k_groesse, k_md5 = len(kb), md5(kb)
if kb.decode('utf-8').count(SEMI):
    raise SystemExit('Abbruch: Semikolon im Nachtrag K2')

prot = []
nb, lb, plb = open(NOTIZEN, 'rb').read(), open(LISTE, 'rb').read(), open(PLAN, 'rb').read()
prot.append('Eingang Notizen: %d Byte, MD5 %s' % (len(nb), md5(nb)))
prot.append('Eingang Maßnahmenliste: %d Byte, MD5 %s' % (len(lb), md5(lb)))
prot.append('Eingang Plan: %d Byte, MD5 %s' % (len(plb), md5(plb)))
prot.append('Nachtrag K2: %d Byte, MD5 %s, Semikola 0' % (k_groesse, k_md5))
n, l, pl = nb.decode('utf-8'), lb.decode('utf-8'), plb.decode('utf-8')

NACHTRAGPFAD = '`04_Uebergaben\\Textvorschlag_6.1_Nachtrag_K2_2026-10-02.md`'
BEFUNDPFAD = '`02_Befunde\\Analyse_Boumparis_2026_2026-10-02`'
PROMPTPFAD = '`04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md`'
TV61PFAD = '`04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md`'
GROESSE = '{:,}'.format(k_groesse).replace(',', '.')

# ---------- Sitzungsnotizen ----------
n = ersetze(n, '**Stand: (Rev. 150 — siehe Block oben.)',
            '**Stand: (Rev. 151 — siehe Block oben.) Zuvor: (Rev. 150 — siehe Block oben.)', 'Notizen Stand', prot)

block = f"""### ⭐⭐ NEU (Rev. 151, 02.10.2026, {UHR} Sitzungsuhr, Auftrag mit dem Startsatz aus Plan § 8, Klicks des Verfassers): Task „Boumparis“ — Version of Record am PMC-Volltext analysiert, Nachtrag K2 mit zwei Varianten und Einarbeitungsplan, unabhängige Zweitprüfung, Modul A2-M per Klick mit Variante A, Gegenbefund in Absatz 3 der Einleitung vorgemerkt, T1 und T4 nachgetragen, kein Manuskripttext

**Auftrag:** Startsatz aus Plan § 8 (Nachtrag 02.10.): „Task Boumparis nach Plan Nachtrag 02.10. Lies zuerst Teil 0 der Sitzungsnotizen (mindestens Rev. 148), dann {PROMPTPFAD} vollständig und arbeite ihn ab. Kein Manuskripttext im Master, Rücksprache nur per Klick.“ Während der Sitzung schickte der Verfasser den Prompt noch einmal als Anhang, ohne neue Anweisung. Die Sitzung lief parallel zu Task 12a (Rev. 149 und 150). Dieser Eintrag trägt die nächste freie Nummer, bis {UHR} Sitzungsuhr kam von 12a kein neuer Eintrag hinzu.

**Fassung und Vorbefunde (Prompt § 1):** In `Ideen und Studien` liegt weiterhin nur der Preprint (JMIR Preprints, Deckblatt mit der Zusammenfassung der Erstsuche, 85 Studien, im Manuskript das Update mit 119 Studien, Fußzeile „peer-reviewed preprint“). Die Version of Record (Interact J Med Res 15, e84822, doi 10.2196/84822, PMC13626193, 116 Studien, 143 Vergleiche) wurde nach Klick „PMC-Volltext nutzen“ am Volltext in PubMed Central gelesen, Fundstellen nach Abschnitt und Absatz. Vorbefunde aus Rev. 148 bestätigt: (a) 66,9 % (Abschlussrate, 68 Vergleiche) und 55,2 % (Bestandteil-Adhärenz, 66 Vergleiche) sind beschreibende Mittel, metaanalytisch zusammengefasst ist nur der Studienabbruch (gepoolt 16,9 %, 108 Vergleiche), Quellenart „systematische Übersicht“ · (b) Dauer: im Bewegungsteil zwei Studien, in der Moderatoranalyse des Studienabbruchs kein signifikanter Einfluss · (c) Distanz bei Umsetzungsvergleichen: per Klick „Anpassung wie vorgeschlagen“ eine Regel neben F17 § 6.4 (Population wie dort, an Stelle von Dosis und Zielgröße Programmform und Umsetzungsmaß, je 0 bis 2, Summen und Folgen wie § 6.4). Danach Klusemann et al. (2012) 2·0·0 = 2, Boumparis et al. (2026) 2·1·1 = 4 (strenger gelesen 5), nur Kontext. Die Distanzfelder in T1 bleiben die Wirksamkeitsdistanz.

**Ergebnis:** (1) Analysebefund {BEFUNDPFAD} (.md 44.505 Byte, .docx, .pdf mit 13 Seiten quer, Projektkopie `claude/`, Erzeuger `03_Skripte\\Analyse_Boumparis_Hausstil_2026-10-02.py`): Steckbrief, Definitionen mit Zuordnung der eigenen Maße (die eigene Umsetzungsrate K-10.5 ist wie die Bestandteil-Adhärenz gebaut, die Abschlussrate hat zwei Lesarten), Ergebnisse mit Fundstelle, Güte und Grenzen, Übertragbarkeit mit der Distanzregel, T1 und T4, offene Punkte. (2) Nachtrag K2 {NACHTRAGPFAD} ({GROESSE} Byte, MD5 `{k_md5[:8]}…`, Projektkopie `claude/`) mit Messskript `03_Skripte\\Textvorschlag_6.1_Nachtrag_K2_2026-10-02.py` (Fassung 2, `.txt`, `.json`): Variante A, Variante B und Verzicht, jeweils 6.1 mit 700 Wörtern (Budget 700), 40 Sätze, Median 16,0, längster 31, 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, 14 Belegklammern, neun Quellen. Einarbeitungsplan Nr. 1 bis 9 mit Satzkernen für 12b (Klusemann et al., 2012, in G3 mit Dosis und Niveau der Videogruppe · Verbleib überschätzt Nutzung in G3 · Bericht der Umsetzung als Stärke · fehlende Nutzungsdaten und Gründe in G6), für 13a (drei Sätze ohne Quelle und Zahl, keine Merkmale des eigenen Programms) und für die Schlussfassung der Einleitung, dazu Belegtabelle, Kennungen und Prüfung der ausgeschlossenen Schlüsse. Methodik und Kapitel 5 passen zur Einordnung, keine Änderung. (3) Zweitprüfung durch einen unabhängigen Subagenten: 22 Befunde (3 A, 11 B, 8 C), alle behandelt (Nachtrag § 9). Die drei A-Befunde: Kapitel 7 nannte Merkmale des eigenen Programms mit Richtung (berichtigt) · Satzkern Klusemann ohne Dosis und Niveau (berichtigt) · zwei Satzkerne falsch gezählt (seither gemessen). Nach dem B-Befund Nr. 4 wurde Variante B umformuliert und die Empfehlung von B auf A umgestellt.

**Klicks des Verfassers (02.10.):** „PMC-Volltext nutzen“ · Distanzregel „Anpassung wie vorgeschlagen“ · nach 17:54 Sitzungsuhr Modul A2-M (K2) „Variante A“ und Einleitung „Gegenbefund in Absatz 3“, jeweils die Empfehlung. **Variante A** (6.1, A2 nach S2, 27 Wörter): „Auch in digitalen Lebensstilprogrammen für Jugendliche wurde nach einer systematischen Übersicht im Mittel nur gut die Hälfte der Programmbestandteile absolviert, bei großer Streuung (Boumparis et al., 2026).“ A2 S3 beginnt dann „Der Schätzer ist durch die eigene Umsetzung stark verdünnt: …“ (+3). Gegenfinanziert mit Stufe 1 der Kürzungsleiter (A3 S8, Liu et al., 2024, −30, Liu nach 6.2/6.3 G8), 6.1 bleibt bei 700. Klusemann et al. (2012) geht nach 6.3 G3. Der Grund für die Fremdpopulation steht nur im Begleitteil (Nachtrag § 1), die Abweichung vom Wortlaut der Populationsregel ist mit dem Klick entschieden. **Gegenbefund für die Schlussfassung der Einleitung** (Absatz 3, nach „… ohne Trainingszeiten und Trainer des Vereins zu beanspruchen.“, 17 Wörter): „Jugendliche nutzten digitale Lebensstilprogramme nach einer systematischen Übersicht allerdings im Mittel nur teilweise (Boumparis et al., 2026).“ Nur Vormerkung (G35), kein Einbau. Freigabe des Wortlauts 6.1 und Einbau bleiben bei Task 12a.

**T1 und T4 (`03_Skripte\\T1_T4_Nachtrag_Boumparis_2026-10-02.py`, Protokoll `.txt` mit beiden Läufen):** Lauf 1 (17:53 Sitzungsuhr): T1 um `Boumparis2026` (75 → 76, Distanzfelder 2 · — · —, Umsetzungsdistanz im Feld `evidenzsicherheit`), bei `Klusemann2012` ein Vermerk zur Umsetzungsdistanz (Distanzfelder unverändert), T4 um zwölf Zeilen (158 → 170, elf zu Boumparis2026, eine zu Klusemann2012 „Bezugsmenge der 77 %“). Lauf 2 (18:06): Feld `kapitel` beider Steckbriefe nach Klick K2, T4 unverändert. T1 102.519 Byte, MD5 `5e4f1754…`, T4 85.384 Byte, MD5 `074e70a6…`.

**Zitationsbefunde (für 12a, 12b und Task 15, in T4):** Boumparis et al. (2026) nur nach der Version of Record zitieren, Zitierjahr 2026, für die Adhärenzwerte „systematische Übersicht“, nie „Metaanalyse“ · den ersten Satz der Zusammenfassung nicht als Ergebnis zitieren, er ist Hintergrund · Bewegungswerte beruhen auf wenigen Vergleichen, nach den Autoren nur hinweisend · Einflussfaktoren gezählt, nicht gepoolt, keine Dosis-Wirkung · Klusemann et al. (2012): die 77 % gelten rechnerisch für alle 13 der Videogruppe, nicht „nach Ausschluss zweier Spieler“ (Textvorschlag 6.1 § 5 zu berichtigen) · Preprint mit zwei Zusammenfassungen (Deckblatt Erstsuche, Manuskript Update), nicht zitierfähig.

**Eigene Korrekturen in dieser Sitzung:** (1) Ein wörtliches Semikolon im T1/T4-Skript vor Lauf 1 durch „ · “ ersetzt. (2) Analysebefund vor der Zweitprüfung berichtigt: „viele Programme kürzer“ (der Median von 84 Tagen ist länger als sechs Wochen), Erstsuche gegen Update statt Preprint gegen Version of Record bei den Studienzahlen. (3) Nach der Zweitprüfung: „Kernaussage“ → „Folgerung der Autoren“ · drei statt zwei zugeteilte IG-Spieler ohne jede Meldung (K-10.9, K-01.19, K-01.20) · τ² statt τ · „nicht begutachtet“ beim Preprint falsch (Fußzeile „peer-reviewed preprint“). (4) Nach der Klickfreigabe im Nachtrag § 3.1 Nr. 2 ergänzt: Variante A und Satzkern Nr. 4 beginnen gleich, 12b gibt Nr. 4 einen eigenen Anschluss.

**Offen beim Verfasser:** (1) PDF der Version of Record in `Ideen und Studien` ablegen (frei über https://doi.org/10.2196/84822 oder PMC13626193), vor dem Einbau von 6.1 (Nachtrag § 8.1 Nr. 5, H16), den Preprint umbenennen oder in den Papierkorb verschieben · (2) Task 12a fortsetzen: Variante A in den Textvorschlag 6.1 übernehmen, Klickfreigabe des Wortlauts je Absatz, Einbau per Skript (Nachtrag § 8.1, Textvorschlag 6.1 § 11.2) · (3) Projektspeicher: vor den Kopien dieses Tasks 1.806.923 von 2.000.000 (project_info), mit ihnen rund 1,9 Mio. (Rechnung aus den Dateigrößen). Vor weiteren großen Projektkopien prüfen, welche Kopien entbehrlich sind, die Ordnerfassungen bleiben maßgeblich.

**Vormerkungen (Nachtrag § 8):** 12a: Variante A übernehmen, Textvorschlag 6.1 mit Stufe 1 nachführen (§ 0, § 2 bis § 6, § 9.1, § 9.3), berichtigen: § 5 Zeile Klusemann (77 % für alle 13), § 9.3 Nr. 1 Budget der Einleitung 1.200 statt 1.500, T1 `Liu2024` Distanz (2 · 1 · 2 gegen 1 · 1 · 0 in der Belegtabelle) und Feld `kapitel` („2.3, 5.5“), § 9.4 Literaturverzeichnis · 12b: Satzkerne Nr. 3 bis 6 mit eigenem Anschluss für Nr. 4, Liu et al. (2024) nach 6.2/6.3 G8, Distanzregel für Umsetzungsvergleiche · 13a: Satzkerne Nr. 7, ohne Quelle, ohne Zahl, keine Merkmale des eigenen Programms · Schlussfassung der Einleitung: Gegenbefund in Absatz 3 (G35) · Task 15: Boumparis et al. (2026) mit allen zwölf Autorinnen und Autoren (Nachtrag § 8.5) · Task 16: Skripte dieses Tasks als KI-erzeugt, Zweitprüfung durch einen Subagenten · Steuerdokumente (Fassung 18): Distanzregel für Umsetzungsvergleiche in F17 § 6.4, F17 § 6.5 mit Boumparis et al. (2026) und Klusemann et al. (2012) (G37 n).

**Stand der Dateien:** Neu: Analysebefund {BEFUNDPFAD} (.md, .docx, .pdf, Projektkopie `claude/`) mit `03_Skripte\\Analyse_Boumparis_Hausstil_2026-10-02.py` · Nachtrag K2 {NACHTRAGPFAD} (Fassung 17:54 Sitzungsuhr vor der Klickfreigabe, gültig {UHR} nach der Klickfreigabe, {GROESSE} Byte, MD5 `{k_md5[:8]}…`, Projektkopie `claude/`) mit `03_Skripte\\Textvorschlag_6.1_Nachtrag_K2_2026-10-02.py`, `.txt` und `.json` · `03_Skripte\\T1_T4_Nachtrag_Boumparis_2026-10-02.py` mit `.txt` · `03_Skripte\\Steuerung_Rev151_2026-10-02.py` mit `.txt`. Geändert: `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (76 Steckbriefe) und `T4_zitierfallen.csv` (170 Zitierfallen) · diese Notizen (Rev. 151 auf Rev. 150) · Maßnahmenliste (Stand, H16, G35 und G37 Vermerke, Taskzeilen 12 und 13, Summe) · Plan (Nachtrag 02.10. abends, Startsätze in § 8), je Ordner und Projektkopie. Byte und MD5 je Datei im Nachtrag § 10. Durch diesen Task unverändert: Master (42.318 Byte, MD5 `caa5dee2…`, 6.1 leer), Textvorschlag 6.1 (81.240 Byte, MD5 `6afeed18…`) mit seinen Erzeugern, Kennzahlenblatt, Zahlenliste, Fassung 17, Prompt Boumparis, Befund Rev. 147. Rückschreibung je Commit aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** PDF der Version of Record ablegen, dann Task 12a fortsetzen (Startsatz: „Weiter mit Task 12a: Freigabe und Einbau 6.1 nach {TV61PFAD} § 8 und § 11.2 und dem Nachtrag {NACHTRAGPFAD} § 8.1 (Variante A, per Klick gewählt). Zuerst Teil 0, mindestens Rev. 151. Die PDF der Version of Record muss vor dem Einbau in `Ideen und Studien` liegen.“). Danach Task 12b, Reihenfolge sonst wie Rev. 148.

"""
anker = '### ⭐ NACHTRAG (Rev. 150, 02.10.2026, 16:45 Sitzungsuhr'
n = ersetze(n, anker, block + anker, 'Notizen Block Rev. 151', prot)

# ---------- Maßnahmenliste ----------
l = ersetze(l, '**Stand 02.10.2026, 16:45 Sitzungsuhr (Rev. 150 — ',
            f'**Stand 02.10.2026, {UHR} Sitzungsuhr (Rev. 151 — Task „Boumparis“: Analysebefund {BEFUNDPFAD}, Nachtrag K2 {NACHTRAGPFAD} mit Zweitprüfung, Modul A2-M per Klick mit Variante A, Gegenbefund in Absatz 3 der Einleitung vorgemerkt, T1 76 und T4 170, H16, G35 und G37 Vermerke, Taskzeilen 12 und 13 fortgeschrieben). Zuvor 02.10.2026, 16:45 Sitzungsuhr (Rev. 150 — ',
            'Liste Stand', prot)

h16_ende = f'Analyse und Einarbeitung im Task „Boumparis“, Prompt {PROMPTPFAD}.)*'
h16_neu = (h16_ende + f' *(Rev. 151, 02.10.: Version of Record am PMC-Volltext analysiert (Klick „PMC-Volltext nutzen“), Analysebefund {BEFUNDPFAD}, T1 `Boumparis2026` und elf T4-Zeilen. '
           'Für die Adhärenzwerte gilt „systematische Übersicht“, nicht „Metaanalyse“. Per Klick K2 trägt die Quelle in 6.1 den Vergleichssatz (Variante A), '
           'dazu 6.3 G3 und die Stärken oder G6 (12b) und die Schlussfassung der Einleitung (Gegenbefund in Absatz 3). '
           'Offen: die PDF der Version of Record vor dem Einbau von 6.1 in `Ideen und Studien` ablegen, Titel, 116 Studien und DOI an der Datei prüfen, '
           f'Seitenzahlen der Fundstellen nachtragen (Nachtrag K2 § 8.1 Nr. 5). Priorität 2 und 3 unverändert.)*')
l = ersetze(l, h16_ende, h16_neu, 'Liste H16', prot)

g35_ende = 'Vormerkung für die Schlussfassung der Einleitung in Textvorschlag 6.1 § 9.3.)*'
g35_neu = (g35_ende + ' *(Rev. 151, 02.10.: Vormerkung für die Schlussfassung, per Klick gewählt: Gegenbefund in Absatz 3 nach „… ohne Trainingszeiten und Trainer des Vereins zu beanspruchen.“: '
           '„Jugendliche nutzten digitale Lebensstilprogramme nach einer systematischen Übersicht allerdings im Mittel nur teilweise (Boumparis et al., 2026).“ '
           f'(17 Wörter, Rasterzeile 2.1, Nachtrag K2 § 3.4 und § 8.4). Kein Satz zur Umsetzung in der Lücke (Absatz 5).)*')
l = ersetze(l, g35_ende, g35_neu, 'Liste G35', prot)

g37_ende = '*(Rev. 146, 02.10.: (e) Kapitel-5-Teil erledigt: Überschriften 5.1 und 5.2 per Skript entfernt (M28), Abgleich bestanden, F9 durch den Verfasser offen.)*'
g37_neu = (g37_ende + f' *(Rev. 151, 02.10.: (n) neu aus dem Task „Boumparis“ für Fassung 18: F17 § 6.4 um die Regel für Umsetzungsvergleiche ergänzen (Klick 02.10., Analysebefund {BEFUNDPFAD} § 6.1: '
           'Population wie § 6.4, an Stelle von Dosis und Zielgröße Programmform und Umsetzungsmaß, je 0 bis 2, Summen und Folgen wie § 6.4), mit dem Hinweis, dass die Distanzfelder in T1 die Wirksamkeitsdistanz bleiben · '
           'F17 § 6.5: Boumparis et al. (2026) als Kontextquelle der Umsetzung (Version of Record, „systematische Übersicht“), Klusemann et al. (2012) für die Aufsicht in G3.)*')
l = ersetze(l, g37_ende, g37_neu, 'Liste G37', prot)

t12_ende = '· Einbau- und Abgleichskript bereit und an einer Kopie geprüft (Rev. 150, Textvorschlag 6.1 § 11.1 und § 11.2) |'
l = ersetze(l, t12_ende,
            '· Einbau- und Abgleichskript bereit und an einer Kopie geprüft (Rev. 150, Textvorschlag 6.1 § 11.1 und § 11.2) · '
            f'Task „Boumparis“ erledigt (Rev. 151): Nachtrag K2 {NACHTRAGPFAD}, Modul A2-M per Klick mit Variante A (Vergleichssatz Boumparis et al. 2026, Stufe 1, Klusemann 2012 nach G3), '
            'Übernahme in den Textvorschlag 6.1 und Berichtigungen nach § 8.1 (12a), Satzkerne Nr. 3 bis 6 und Liu 2024 nach G8 nach § 8.2 (12b), PDF der Version of Record vor dem Einbau |',
            'Liste Taskzeile 12', prot)

t13_ende = '· Textvorschlag 6.1 (Rev. 149) § 9.2 (13a: Hauptbefund in der Sprache von A1, Zeitverlauf der Weite offen, keine Programmdauer-Empfehlung, Umsetzung als Erkenntnisaspekt) |'
l = ersetze(l, t13_ende,
            '· Textvorschlag 6.1 (Rev. 149) § 9.2 (13a: Hauptbefund in der Sprache von A1, Zeitverlauf der Weite offen, keine Programmdauer-Empfehlung, Umsetzung als Erkenntnisaspekt) · '
            'Nachtrag K2 (Rev. 151) § 3.3 mit Satzkernen Nr. 7 (13a: Umsetzung mit Definition berichten, Nutzungsdaten und Gründe, Merkmale der Vermittlung als offene Frage, ohne Quelle und Zahl) |',
            'Liste Taskzeile 13', prot)

l = ersetze(l, '| **Summe** | Rev. 150 (02.10.): ',
            '| **Summe** | Rev. 151 (02.10.): H16, G35 und G37 Vermerke, Taskzeilen 12 und 13 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 150 (02.10.): ',
            'Liste Summe', prot)

# ---------- Plan ----------
nachtrag = ('**Nachtrag 02.10.2026, abends (Rev. 151 der Sitzungsnotizen), keine neue Revision des Plans:** '
            f'Task „Boumparis“ erledigt: Analysebefund {BEFUNDPFAD} und Nachtrag K2 {NACHTRAGPFAD} mit unabhängiger Zweitprüfung. '
            'Per Klick des Verfassers trägt das Modul A2-M die Variante A (Vergleichssatz Boumparis et al., 2026, Stufe 1 der Kürzungsleiter, Klusemann et al., 2012, nach 6.3 G3), '
            'für die Schlussfassung der Einleitung ist der Gegenbefund in Absatz 3 vorgemerkt. '
            'Nächster Schritt ist Task 12a mit der Übernahme von Variante A, der Freigabe des Wortlauts und dem Einbau, vorher die PDF der Version of Record im Ordner. '
            'Reihenfolge danach wie im Nachtrag vom 02.10. (Rev. 148). Startsatz in § 8.\n\n')
pl = ersetze(pl, 'Steuerdokumente-Task → Tasks 15 bis 18. Startsatz in § 8.\n\n## 0 Ergebnis in Kürze',
             'Steuerdokumente-Task → Tasks 15 bis 18. Startsatz in § 8.\n\n' + nachtrag + '## 0 Ergebnis in Kürze',
             'Plan Nachtrag 02.10. abends', prot)

pl = ersetze(pl, '- **Task „Boumparis“ (zwischen Textvorschlag und Freigabe von 12a, Nachtrag 02.10.):**',
             '- **Task „Boumparis“ (zwischen Textvorschlag und Freigabe von 12a, Nachtrag 02.10., erledigt 02.10., Rev. 151):**',
             'Plan Startsatz Boumparis erledigt', prot)

startsatz = ('- **Task 12a, Fortsetzung (Freigabe und Einbau 6.1, Nachtrag 02.10. abends):** '
             f'„Weiter mit Task 12a: Freigabe und Einbau 6.1 nach {TV61PFAD} § 8 und § 11.2 und dem Nachtrag {NACHTRAGPFAD} § 8.1 (Variante A, per Klick gewählt). '
             'Zuerst Teil 0, mindestens Rev. 151. Die PDF der Version of Record muss vor dem Einbau in `Ideen und Studien` liegen.“\n')
anker12b = '- **Task 12b (6.2 und 6.3):**'
pl = ersetze(pl, anker12b, startsatz + anker12b, 'Plan Startsatz 12a Fortsetzung', prot)

os.makedirs(AUS, exist_ok=True)
nb2, lb2, plb2 = n.encode('utf-8'), l.encode('utf-8'), pl.encode('utf-8')
open(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'), 'wb').write(nb2)
open(os.path.join(AUS, 'Massnahmenliste_Datenverarbeitung.md'), 'wb').write(lb2)
open(os.path.join(AUS, 'Plan_Weitere_Schritte_2026-09-25.md'), 'wb').write(plb2)
prot.append('Ausgang Notizen: %d Byte, MD5 %s' % (len(nb2), md5(nb2)))
prot.append('Ausgang Maßnahmenliste: %d Byte, MD5 %s' % (len(lb2), md5(lb2)))
prot.append('Ausgang Plan: %d Byte, MD5 %s' % (len(plb2), md5(plb2)))
prot.append('Semikola im neuen Block: %d · H16: %d · G35: %d · G37: %d · Plan-Nachtrag: %d · Startsatz: %d' % (
    block.count(SEMI), h16_neu.count(SEMI), g35_neu.count(SEMI), g37_neu.count(SEMI), nachtrag.count(SEMI), startsatz.count(SEMI)))
# Rücklesen: nur Einfügungen, keine Verluste
for name, alt, neu in (('Notizen', nb, nb2), ('Maßnahmenliste', lb, lb2), ('Plan', plb, plb2)):
    a, b = alt.decode('utf-8'), neu.decode('utf-8')
    assert len(b) > len(a), name
    zeilen_alt = a.split('\n')
    zeilen_neu = set(b.split('\n'))
    fehlend = [z for z in zeilen_alt if z not in zeilen_neu]
    prot.append('Rücklesen %s: %d Zeilen vorher, %d nachher, %d alte Zeilen verändert (erwartet: nur die ergänzten)' % (
        name, len(zeilen_alt), len(b.split('\n')), len(fehlend)))
text = '\n'.join(prot) + '\n'
open(os.path.join(AUS, 'Steuerung_Rev151_2026-10-02.txt'), 'w', encoding='utf-8').write(text)
print(text)

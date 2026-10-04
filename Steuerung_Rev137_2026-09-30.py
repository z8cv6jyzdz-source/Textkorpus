# -*- coding: utf-8 -*-
"""Steuerung Rev. 137 (30.09./01.10.2026): Task 11 Kapitel 5 (Ergebnisse) abgeschlossen, ohne Rückfrage entschieden
(Verfasser 30.09., 23:02), Einbau per Skript geprüft, Löschung des Altbestands (M24) entschieden, Messskript Fassung 4.

Schreibt drei Steuerdokumente fort, jede Änderung an einem eindeutigen Anker
(Abbruch, wenn ein Anker nicht genau einmal vorkommt):
  1. Plan_Weitere_Schritte_2026-09-25.md: Nachtrag (Rev. 137) nach dem Nachtrag vom 30.09. (Rev. 134),
     Verweise auf Textvorschlag 5 § 9 in den Startsätzen 12a, 12b, „Einleitung, Schlussfassung“ und 13b,
     in den Modi „offen“ und „verfasser“ dazu Schritt 0 (Abgleich von Kapitel 5 im Master) im Startsatz 12a
  2. Massnahmenliste_Datenverarbeitung.md: Stand, B5, G28g, G29, G32, G35, G37, Taskzeilen 11, 12, 13, 18
  3. Cowork_Sitzungsnotizen.md: Stand-Zeile, Block Rev. 137 in Teil 0 über Rev. 136

Aufruf: python3 Steuerung_Rev137_2026-09-30.py <Eingangsordner Claude> <Ausgabeordner> <Datum TT.MM.JJJJ> <Uhrzeit> <Modus>
  geschrieben: der per Skript eingebaute Master ist zurückgeschrieben und per MD5 geprüft
  offen: der Master im Ordner trägt noch den Stand vom Eingang (Word-Sperre oder Rechner nicht verbunden)
  verfasser: der Verfasser überträgt Kapitel 5 und die Löschung des Altbestands selbst in den Master (01.10., 07:34),
             der per Skript eingebaute Stand ist Referenz für den Abgleich, der danach folgt
Eingang: gestagte Fassungen aus dem Ordner (Notizen Rev. 136, Maßnahmenliste Rev. 135, Plan Rev. 134).
Kein Manuskripttext. Ohne Semikolon im Skript und in den geschriebenen Texten.
"""
import hashlib
import os
import sys

SRC, OUT, DATUM, UHR, MODUS = sys.argv[1:6]
assert MODUS in ('geschrieben', 'offen', 'verfasser'), MODUS
KURZ = DATUM[:6]
BS = chr(92)
LOG = []
NEU_TEXTE = []


def log(msg):
    LOG.append(msg)
    print(msg)


def lesen(rel):
    with open(os.path.join(SRC, rel), encoding='utf-8', newline='') as f:
        t = f.read()
    b = t.encode('utf-8')
    log('gelesen %s: %d Byte, MD5 %s' % (rel, len(b), hashlib.md5(b).hexdigest()))
    return t


def schreiben(rel, txt):
    assert chr(59) not in ''.join(NEU_TEXTE), 'Semikolon in einem neuen Text'
    ziel = os.path.join(OUT, os.path.basename(rel))
    with open(ziel, 'w', encoding='utf-8', newline='') as f:
        f.write(txt)
    b = txt.encode('utf-8')
    log('geschrieben %s: %d Byte, MD5 %s' % (ziel, len(b), hashlib.md5(b).hexdigest()))


def ersetze(txt, alt, neu, name):
    n = txt.count(alt)
    if n != 1:
        raise SystemExit('ABBRUCH %s: Anker %d-mal gefunden' % (name, n))
    log('ok ' + name)
    NEU_TEXTE.append(neu)
    return txt.replace(alt, neu)


def zeile_anhaengen(txt, praefix, zusatz, name):
    zeilen = txt.split('\n')
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise SystemExit('ABBRUCH %s: Zeilenanfang %d-mal gefunden' % (name, len(treffer)))
    i = treffer[0]
    zeilen[i] = zeilen[i].rstrip() + ' ' + zusatz
    NEU_TEXTE.append(zusatz)
    log('ok %s (Zeile %d)' % (name, i + 1))
    return '\n'.join(zeilen)


def zeile_ersetzen(txt, praefix, neu, name):
    zeilen = txt.split('\n')
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise SystemExit('ABBRUCH %s: Zeilenanfang %d-mal gefunden' % (name, len(treffer)))
    zeilen[treffer[0]] = neu
    NEU_TEXTE.append(neu)
    log('ok %s (Zeile %d)' % (name, treffer[0] + 1))
    return '\n'.join(zeilen)


def vor_letztem_strich(txt, praefix, zusatz, name):
    zeilen = txt.split('\n')
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise SystemExit('ABBRUCH %s: Zeilenanfang %d-mal gefunden' % (name, len(treffer)))
    z = zeilen[treffer[0]].rstrip()
    assert z.endswith(' |'), name
    zeilen[treffer[0]] = z[:-2] + ' ' + zusatz + ' |'
    NEU_TEXTE.append(zusatz)
    log('ok %s (Zeile %d)' % (name, treffer[0] + 1))
    return '\n'.join(zeilen)


TV5 = '`04_Uebergaben' + BS + 'Textvorschlag_5_2026-09-30.md`'
ARCHIV_M = '`_Archiv' + BS + '_ersetzt_2026-09-30_Master' + BS + 'Bachelorarbeit_Geruest_v1_vor_Kapitel5_2026-09-30.docx`'
ABGLEICH = ('Absatztexte des Masters per Skript gegen den Referenzstand (MD5 `53cc8f36…`): Kapitel 5 zeichengleich mit '
            'Textvorschlag 5 § 1, Überschriften 5.1 und 5.2 und Altbestand entfernt, übrige Absätze unverändert, '
            'keine Direktformatierung in Kapitel 5, keine `comments.xml`, danach Messskript Fassung 4 und Endabgleich am Master')

# ---------------------------------------------------------------- Texte je Modus
if MODUS == 'geschrieben':
    T = {
        'masterkurz': '',
        'plan_master': 'Der Master im Ordner trägt Kapitel 5 und keinen Altbestand mehr, F9 beim Verfasser. ',
        'plan_schritt0': False,
        'm_g35': '(e) erledigt: Altbestand per Skript mit dem Einbau von Kapitel 5 gelöscht (Archivkopie ' + ARCHIV_M + '), Messskript Fassung 4.',
        'm_g37e': '(e) Kapitel-5-Teil erledigt (M28, Überschriften 5.1 und 5.2 beim Einbau entfernt)',
        'm_zeile11': 'erledigt: G29 (d), (e) · G32 (b) Textteil mit Nr. 23 · G35 (e) · G37 (d), (e) Kapitel 5, (f) · G28g Kapitel-5-Teil',
        'titelzusatz': ', eingebaut mit Löschung des Altbestands (M24)',
        'einbau_label': '**Einbau:**',
        'rueck': ('**Rückschreibung:** Nach dem Schließen von Word aus eigenem, frischem Ausgabepfad zurückgeschrieben, nach kurzer '
                  'Wartezeit neu gestagt: 39.115 Byte, MD5 `53cc8f36…` gleich der Ausgabe.'),
        'mess_label': '**Messung nach dem Einbau (Messskript Fassung 4):**',
        'end_label': '**Endabgleich (Fassung 3):**',
        'end_ausgabe': 'Ausgabe in `03_Skripte' + BS + 'Endabgleich_2026-09-30_Task11' + BS + '`, die Zahlenliste in `03_Skripte` bleibt bis Task 18.',
        'offen1': '(1) F9 im Master (das Inhaltsverzeichnis verliert 2 bis 3, 5.1 und 5.2)',
        'stand_skripte': ('`03_Skripte' + BS + 'Endabgleich_2026-09-30_Task11' + BS + '` (Laufprotokoll, Zahlenliste, Abgleichprotokoll) · '),
        'stand_mess': 'Geändert: `03_Skripte' + BS + 'Manuskriptstand_2026-09-25.py` (Fassung 4) mit `.txt` und `.csv` am eingebauten Stand',
        'masterzeile': 'Master: Kapitel 5 eingebaut, Altbestand gelöscht (39.115 Byte, MD5 `53cc8f36…`).',
        'naechst': 'Task 12a (6.1) mit dem Startsatz aus Plan § 8 (ab 30.09.), Vormerkungen in Textvorschlag 5 § 9.3.',
    }
elif MODUS == 'offen':
    T = {
        'masterkurz': ', Rückschreibung des Masters offen',
        'plan_master': 'Die Rückschreibung des Masters steht aus (Teil 0 Rev. 137), bis dahin trägt der Master im Ordner den Stand vom Eingang. ',
        'plan_schritt0': True,
        'm_g35': '(e) Löschung entschieden, am Referenzstand per Skript geprüft (Archivkopie ' + ARCHIV_M + '), Messskript Fassung 4, Rückschreibung des Masters offen (Teil 0 Rev. 137).',
        'm_g37e': '(e) Kapitel-5-Teil am Referenzstand geprüft, Rückschreibung offen',
        'm_zeile11': 'erledigt: G29 (d), (e) · G32 (b) Textteil mit Nr. 23 · G37 (d), (f) · G28g Kapitel-5-Teil · offen: G35 (e) und G37 (e) Kapitel 5 mit der Rückschreibung',
        'titelzusatz': ', Rückschreibung des Masters offen',
        'einbau_label': '**Einbau als Referenz:**',
        'rueck': ('**Rückschreibung des Masters: offen.** Word hielt den Master bei jeder Prüfung bis 23:18 gesperrt („open_in_another_app“), '
                  'danach war der Rechner nicht mit der Sitzung verbunden. Der Master im Ordner trägt den Stand vom Eingang '
                  '(57.471 Byte, MD5 `c7657a2c…`). Nachholen: Word schließen, Master neu stagen und per MD5 gegen `c7657a2c…` prüfen, '
                  'eingebauten Stand (`53cc8f36…`) aus frischem Ausgabepfad zurückschreiben, kurze Wartezeit, neu stagen, MD5.'),
        'mess_label': '**Messung am Referenzstand (Messskript Fassung 4):**',
        'end_label': '**Endabgleich am Referenzstand (Fassung 3):**',
        'end_ausgabe': 'Die Ausgabe am Master folgt mit der Rückschreibung, die Zahlenliste in `03_Skripte` bleibt bis Task 18.',
        'offen1': '(1) Word schließen und die Rückschreibung des Masters auslösen, danach F9',
        'stand_skripte': '',
        'stand_mess': 'Geändert: `03_Skripte' + BS + 'Manuskriptstand_2026-09-25.py` (Fassung 4), die Ausgaben `.txt` und `.csv` folgen mit der Rückschreibung',
        'masterzeile': 'Master im Ordner noch unverändert (57.471 Byte, MD5 `c7657a2c…`), Rückschreibung offen.',
        'naechst': 'Zuerst die Rückschreibung des Masters (Offen Nr. 1), dann Task 12a (6.1) mit dem Startsatz aus Plan § 8 (ab 30.09.), Vormerkungen in Textvorschlag 5 § 9.3.',
    }
else:
    T = {
        'masterkurz': ', Übertragung in den Master durch den Verfasser (01.10.), Abgleich offen',
        'plan_master': ('Kapitel 5 überträgt der Verfasser selbst in den Master (01.10., 07:34), zusammen mit der Löschung des Altbestands. '
                        'Der per Skript eingebaute und geprüfte Stand ist Referenz für den Abgleich danach. Dieser folgt in der Sitzung '
                        'von Task 11 nach der Meldung des Verfassers, sonst als Schritt 0 von Task 12a (Teil 0 Rev. 137). '),
        'plan_schritt0': True,
        'm_g35': ('(e) Messskript-Teil erledigt (Fassung 4). Die Löschung des Altbestands ist entschieden (Textvorschlag 5 § 8 Nr. 4) und am '
                  'Referenzstand per Skript geprüft (Archivkopie ' + ARCHIV_M + '), im Master löscht der Verfasser mit der Übertragung '
                  'von Kapitel 5 (01.10.), Abgleich offen (Teil 0 Rev. 137).'),
        'm_g37e': '(e) Kapitel-5-Teil: Überschriften 5.1 und 5.2 entfallen mit der Übertragung durch den Verfasser (M28), Abgleich offen',
        'm_zeile11': ('erledigt: G29 (d), (e) · G32 (b) Textteil mit Nr. 23 · G37 (d), (f) · G28g Kapitel-5-Teil · mit dem Abgleich nach der '
                      'Übertragung: G35 (e) und G37 (e) Kapitel 5'),
        'titelzusatz': ', Übertragung in den Master durch den Verfasser',
        'einbau_label': '**Einbau als Referenz (per Skript, nicht zurückgeschrieben):**',
        'rueck': ('**Übertragung in den Master: durch den Verfasser.** Word sperrte den Master am 30.09. bei jeder Prüfung bis 23:18 '
                  '(„open_in_another_app“), danach war der Rechner bis zum Morgen nicht mit der Sitzung verbunden, die Rückschreibung '
                  'per Skript entfiel. Am 01.10. um 07:34 meldete der Verfasser: „Rechner läuft, ich führe die Übertragung in das '
                  'Word-Dokument durch“. Übertragen werden die sechs Absätze aus Textvorschlag 5 § 1 unter „5 Ergebnisse“ ohne die '
                  'Überschriften 5.1 und 5.2, gelöscht wird der Altbestand von „2 Theoretischer Hintergrund und Forschungsstand“ bis '
                  'einschließlich „3 Fragestellung und Hypothesen“ (Anleitung im Chat, 01.10.). Der Master wurde von dieser Sitzung '
                  'nicht beschrieben. **Abgleich offen:** ' + ABGLEICH + '. In der Sitzung von Task 11 nach der Meldung „fertig“, '
                  'sonst Schritt 0 von Task 12a.'),
        'mess_label': '**Messung am Referenzstand (Messskript Fassung 4):**',
        'end_label': '**Endabgleich am Referenzstand (Fassung 3):**',
        'end_ausgabe': 'Die Ausgaben am Master folgen mit dem Abgleich, die Zahlenliste in `03_Skripte` bleibt bis Task 18.',
        'offen1': ('(1) Übertragung abschließen: Kapitel 5 nach Textvorschlag 5 § 1 unter „5 Ergebnisse“, Überschriften 5.1 und 5.2 und '
                   'Altbestand löschen, F9, Word schließen, „fertig“ melden'),
        'stand_skripte': '',
        'stand_mess': ('Geändert: `03_Skripte' + BS + 'Manuskriptstand_2026-09-25.py` (Fassung 4), die Ausgaben `.txt` und `.csv` '
                       'folgen mit dem Abgleich am Master'),
        'masterzeile': 'Master: Übertragung durch den Verfasser (01.10.), bis zum Abgleich ungeprüft.',
        'naechst': ('Abgleich nach der Übertragung (in dieser Sitzung nach „fertig“, sonst Schritt 0 von Task 12a), dann Task 12a (6.1) '
                    'mit dem Startsatz aus Plan § 8 (ab 30.09.), Vormerkungen in Textvorschlag 5 § 9.3.'),
    }

# ---------------------------------------------------------------- 1 Plan
PLAN = '04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md'
plan = lesen(PLAN)
anker_plan = 'Startsätze in § 8 (ab 30.09.), die Startsätze für Task 11, 12 und 13 der Rev. 5 gelten nicht mehr.'
nachtrag = (anker_plan + '\n\n'
            '**Nachtrag ' + DATUM + ' (Rev. 137 der Sitzungsnotizen), keine neue Revision des Plans:** Task 11 erledigt. '
            'Kapitel 5 mit 450 Wörtern nach ' + TV5 + ', ohne Rückfrage entschieden (Verfasser 30.09., 23:02): '
            'Freigabe, Nr. 23 (Einzelwerte bleiben in Tab. H2), ohne Lokalisation der Schmerzmeldungen, Löschung des Altbestands (M24). '
            'Messskript Fassung 4 liegt vor. ' + T['plan_master']
            + 'Die Vormerkungen des Textvorschlags § 9 gehen an die Folgetasks: § 9.3 an Task 12a, § 9.4 an Task 12b, '
            '§ 9.2 an die Schlussfassung der Einleitung, § 9.5 an Task 13b, § 9.1 und § 9.6 an die Tasks 16 bis 18, '
            '§ 9.7 an den Steuerdokumente-Task. Die Startsätze in § 8 nennen sie. Nächster Task: 12a.')
plan = ersetze(plan, anker_plan, nachtrag, 'Plan Nachtrag Rev. 137')
alt12a = 'nach Plan § 3 Task 12 und Nachtrag 30.09. Zuerst Teil 0, Berichtsraster § 3.14 (6.1.1 bis 6.1.4)'
if T['plan_schritt0']:
    neu12a = ('nach Plan § 3 Task 12 und Nachtrag 30.09. Zuerst Teil 0. Schritt 0, falls Teil 0 (Rev. 137) ihn als offen führt: '
              'Kapitel 5 im Master per Skript gegen ' + TV5 + ' § 1 und den Referenzstand abgleichen (wortgleich, Überschriften 5.1 '
              'und 5.2 und Altbestand entfernt, übrige Absätze unverändert), Messskript Fassung 4 und Endabgleich am Master. '
              'Dann Berichtsraster § 3.14 (6.1.1 bis 6.1.4)')
    plan = ersetze(plan, alt12a, neu12a, 'Plan Startsatz 12a Schritt 0')
plan = ersetze(plan, 'Kapitel 5 im Master, die Vormerkungen für 6.1 bis 6.3 aus den Einleitungs-Textvorschlägen',
               'Kapitel 5 im Master mit den Vormerkungen aus ' + TV5 + ' § 9.3, die Vormerkungen für 6.1 bis 6.3 aus den Einleitungs-Textvorschlägen',
               'Plan Startsatz 12a')
plan = ersetze(plan, 'die Vormerkungen wie in Task 12a, Kapitel 5 und 6.1 im Master.',
               'die Vormerkungen wie in Task 12a mit Textvorschlag 5 § 9.4, Kapitel 5 und 6.1 im Master.',
               'Plan Startsatz 12b')
plan = ersetze(plan, 'Kapitel 5 bis 7 im Master und die dort gesammelten Vormerkungen für die Einleitung.',
               'Kapitel 5 bis 7 im Master und die in ihren Textvorschlägen gesammelten Vormerkungen für die Einleitung (Textvorschlag 5 § 9.2).',
               'Plan Startsatz Einleitung Schlussfassung')
plan = ersetze(plan, 'Kennzahlenblatt K-01, K-06 und K-10, Ankersatz ohne',
               'Kennzahlenblatt K-01, K-06 und K-10, Textvorschlag 5 § 9.5, Ankersatz ohne',
               'Plan Startsatz 13b')
schreiben(PLAN, plan)

# ---------------------------------------------------------------- 2 Maßnahmenliste
MASS = '00_Steuerung/Massnahmenliste_Datenverarbeitung.md'
mass = lesen(MASS)
mass = ersetze(mass, '**Stand 30.09.2026, 21:22 Sitzungsuhr (Rev. 135 — ',
               '**Stand ' + DATUM + ', ' + UHR + ' Sitzungsuhr (Rev. 137 — Task 11 Kapitel 5: Textvorschlag ' + TV5
               + ' mit Zweitprüfung, ohne Rückfrage entschieden (Verfasser 30.09., 23:02), Kapitel 5 mit 450 Wörtern, Einbau mit Löschung des Altbestands (M24) per Skript geprüft'
               + T['masterkurz'] + ', Messskript Fassung 4. B5, G28g, G29, G32, G35 und G37 fortgeschrieben, Taskzeile 11 erledigt). '
               'Zuvor 30.09.2026, 21:22 Sitzungsuhr (Rev. 135 — ', 'Maßnahmenliste Stand')
mass = zeile_anhaengen(mass, '- [ ] **B5 · Flowchart-Felder erheben:**',
                       '*(Rev. 137, ' + KURZ + ': weiter offen. Abb. 1 nennt die Gründe der zur Abschlusstestung nicht angetretenen Spieler nicht (Raster 5.1.1, P), Textvorschlag 5 § 4 und § 9.6 Nr. 1.)*',
                       'B5')
mass = zeile_anhaengen(mass, '    - [ ] **G28g · Vormerkungen für spätere Abschnitte',
                       '*(Rev. 137, ' + KURZ + ': Kapitel-5-Teil erledigt (Umsetzungsrate und Untergrenzen in Kapitel 5). Videopausen und Untergrund entfallen nach Umfangsdokument § 2.2 und § 2.4 (Verfasser 24.09.), G28g ist in diesem Teil überholt. Offen bleiben die Teile für 6.2 und 6.3 und das Literaturverzeichnis.)*',
                       'G28g')
mass = zeile_anhaengen(mass, '- [ ] **G29 · Vormerkungen aus dem Task 4.7',
                       '*(Rev. 137, ' + KURZ + ', Task 11: (d) erledigt, Tab. H5 in Kapitel 5 eingeführt, Untergrenzen als Spielerzahlen an den Schwellen (K-10.11) · (e) erledigt: Sammelsatz nach der Zählung von 4.7 („weder der beobachtende Per-Protokoll-Vergleich noch die sechs Sensitivitätsanalysen“, Zweitprüfung Nr. 1), verworfene Normalverteilung mit W, p und Bootstrap-KI (R2). Die Vorab-Prüfung an den Prä-Werten steht ohne eigenen Satz in der Anmerkung zu Tab. H4b (Textvorschlag 5 § 3), die Anmerkung zu Tab. H4 mit K-07.2 und K-08.11 in Task 18. Offen: (f) Tasks 12a und 12b, (h) Task 18, (i) und (j) Task 15.)*',
                       'G29')
mass = zeile_anhaengen(mass, '- [ ] **G32 · Vormerkungen aus Task 6',
                       '*(Rev. 137, ' + KURZ + ', Task 11: (b) Textteil erledigt, Nr. 23 ohne Rückfrage wie empfohlen entschieden (Einzelwerte bleiben in Tab. H2, Textvorschlag 5 § 8 Nr. 2), die Anmerkungen zu Tab. 2 und Tab. 3 mit Task 18 · (j) R5 bleibt unverändert. Rest für den Steuerdokumente-Task: Umfangsdokument R2 (Trennschärfe nach 6.2), F17 § 5.3 und § 11.9 (Antragskriterium mit Einzelwerten in Tab. H2, im Text bei der Umsetzung), Textvorschlag 5 § 9.7.)*',
                       'G32')
mass = zeile_anhaengen(mass, '- [ ] **G35 · Neuzuschnitt:',
                       '*(Rev. 137, ' + KURZ + ', Task 11 Schritt 0: Einleitung im Master zeichengleich mit Textvorschlag Überarbeitung § 5.1 (930 Wörter). ' + T['m_g35'] + ')*',
                       'G35')
mass = zeile_anhaengen(mass, '- [ ] **G37 · Kapitelstruktur:',
                       '*(Rev. 137, ' + KURZ + ', Task 11: (d) erledigt (Messskript Fassung 4, Fassung 3 in `_Archiv' + BS
                       + '_ersetzt_2026-09-30_Messskript_Fassung3' + BS + '`) · ' + T['m_g37e'] + ' · (f) erledigt: E3 hält, der Orientierungszug trägt ohne Überschrift · für (a), (c) und (h) die Vormerkungen aus Textvorschlag 5 § 9.7 (Raster Rev. 4 Zeilen 5.1.1, 5.1.6, 5.1.8, 5.2.3, 5.2.6 mit Prüfliste Nr. 6, Kopfblock 5.1 · Fassung 18 § 5.3 und § 11.9, Ausnahme zur 18 in Kapitel 5 · Skill mit Kapitel 5 als ein Abschnitt).)*',
                       'G37')
mass = zeile_ersetzen(mass, '| 11 Kapitel 5 (nach Gliederung v6',
                      '| 11 Kapitel 5 (erledigt ' + KURZ + ', Rev. 137: ein Kapitel ohne Unterabschnitte, 450 Wörter' + T['masterkurz']
                      + ') | ' + T['m_zeile11'] + ' · weitergegeben: B5 (Rest, Abb. 1) · G32 (j) Rest und G26g an den Steuerdokumente-Task · Vormerkungen in Textvorschlag 5 § 9 |',
                      'Taskzeile 11')
mass = vor_letztem_strich(mass, '| 12 Kapitel 6 (nach Gliederung v6', '· Textvorschlag 5 § 9.3 (12a) und § 9.4 (12b)', 'Taskzeile 12')
mass = vor_letztem_strich(mass, '| 13 Kapitel 7, Zusammenfassung, Abstract', '· Textvorschlag 5 § 9.5 (13b)', 'Taskzeile 13')
mass = vor_letztem_strich(mass, '| 18 Endredaktion', '· Textvorschlag 5 § 9.1 und § 9.6', 'Taskzeile 18')
schreiben(MASS, mass)

# ---------------------------------------------------------------- 3 Sitzungsnotizen
NOTIZ = '00_Steuerung/Cowork_Sitzungsnotizen.md'
notiz = lesen(NOTIZ)
notiz = ersetze(notiz, '**Stand: (Rev. 136 — siehe Block oben.) Zuvor:',
                '**Stand: (Rev. 137 — siehe Block oben.) Zuvor: (Rev. 136 — siehe Block oben.) Zuvor:', 'Notizen Stand')

block = '\n\n'.join([
    '### ⭐⭐ NEU (Rev. 137, ' + DATUM + ', ' + UHR + ' Sitzungsuhr, Auftrag 30.09., 21:15, Anweisung 30.09., 23:02): Task 11 Kapitel 5 (Ergebnisse) abgeschlossen — 450 Wörter, ohne Rückfrage entschieden' + T['titelzusatz'],
    '**Auftrag (Verfasser, 30.09., 21:15):** Startsatz Task 11 aus Plan § 8 (ab 30.09.), wörtlich wie dort. **Anweisung (Verfasser, 30.09., 23:02, wörtlich):** „Abschließen ohne rückfrage“.',
    '**Einordnung:** Folgt auf Rev. 134. Rev. 135 und 136 liefen parallel in anderen Sitzungen und berühren diesen Task nicht, ihre Stände von Notizen und Maßnahmenliste sind die Grundlage dieser Fortschreibung (neu gestagt, seit dem 30.09., 21:25 unverändert).',
    '**Schritt 0:** Die übertragene Einleitung steht zeichengleich wie Textvorschlag Überarbeitung § 5.1 im Master (930 Wörter, 40 Sätze, 0 Semikola, 0 Abschnittsverweise, `03_Skripte' + BS + 'Abgleich_Einleitung_Master_2026-09-30.py`). M24 war nicht ausgeführt: Der Altbestand Kapitel 2 und 3 (10 Überschriften, 25 Absätze, 4.920 Wörter mit allen 61 Semikola und 35 Abschnittsverweisen des Masters) stand noch im Master. Messskript Fassung 4 (G37 d), Fassung 3 im Archiv.',
    '**Ergebnis:** ' + TV5 + '. Kapitel 5 in sechs Absätzen ohne Unterabschnitte, 450 von 450 Wörtern, 29 Sätze, Median 15,0, längster Satz 28, 0 Semikola, 0 Abschnittsverweise, 0 Belege, 53 von 53 Zahlen gegen das Kennzahlenblatt (Kennungen im Begleitteil § 5, Objektverweise am Objekt geprüft § 6). Orientierungszug in vier Absätzen (Teilnehmerfluss und Ausgangswerte, Umsetzung, Beanspruchung und unerwünschte Ereignisse, Messgüte und Versuche), dann der Gruppenvergleich: bei allen drei konfirmatorischen Zielgrößen kein Gruppenunterschied nachweisbar, Fall C1 (unschlüssig), H0 nicht verworfen, dazu die verworfene Normalverteilung beim 30-m-Sprint mit Bootstrap-Intervall und der Sammelsatz aus Per-Protokoll-Vergleich und sechs Sensitivitätsanalysen. E3 hält (G37 f). Zweitprüfung durch einen Subagenten: A 1 · B 10 · C 9, A und B eingearbeitet (einer in anderer Form), ein C-Befund nicht übernommen („planmäßig“ ist Wortlaut des Verfasserklicks), Nachmessung ohne Befund.',
    '**Entschieden ohne Rückfrage (Anweisung 30.09., 23:02), jeweils wie empfohlen (Textvorschlag § 8):** (1) Freigabe des Wortlauts · (2) Nr. 23: Die Einzelwerte der drei Spieler des Antragskriteriums bleiben in Tab. H2, ohne eigenen Satz, offen abweichend von Textvorschlag 4.7 Nr. 23 (26.09.: streichen), den Ausschlag gibt das Versprechen in 4.7 (alle Teilmengen unter acht Spielern je Gruppe beschreibend) · (3) keine Lokalisation der Schmerzmeldungen (nicht im Kennzahlenblatt, Nachteil für 6.1.4 und 7.2 benannt) · (4) Altbestand löschen, vorher Archivkopie (' + ARCHIV_M + ', MD5 `c7657a2c…`, nach dem Schreiben per MD5 geprüft).',
    T['einbau_label'] + ' `03_Skripte' + BS + 'Master_5_2026-09-30.py` mit `--altbestand` auf dem Master vom Eingang (MD5 `c7657a2c…`, am 30.09. um 23:05 und 23:18 unverändert): Überschriften 5.1 und 5.2 entfernt (M28), sechs Absätze in der Formatvorlage Standard, Altbestand mit 10 Überschriften, 25 Absätzen und 10 Textmarken entfernt, 225 → 194 Absätze, keine Objekte, keine Platzhalter. Validierung bestanden, gerendert geprüft, Textvergleich ohne weitere Änderung. Ergebnis 39.115 Byte, MD5 `53cc8f36…` (zweiter Lauf identisch).',
    T['rueck'],
    T['mess_label'] + ' Einleitung 930 gegen 1.500 · Kapitel 4 2.416 gegen 2.550 · Kapitel 5 450 gegen 450 · Absatztext 3.796 gegen 6.350 · 0 Semikola und 0 Abschnittsverweise in Kapitel 1 bis 7 · 7 Platzhalter, alle in Anhang H · Prognose 27,8 Seiten (Modellrechnung, Einleitung mit gemessenen 930 Wörtern, bei der Obergrenze 1.200 der Schlussfassung rund 0,75 Seiten mehr).',
    T['end_label'] + ' 357 Zahlen, keine nur im alten Blatt. Kapitel 5: 45 Kennzahlen, die 3 Zahlen ohne Deckung sind Konstanten der Methodik (95-%-Konfidenzintervall, zweimal p < 0,05). Satzprüfungen 23, davon 21 stimmen, die zwei Abweichungen sind erwartet (SP6: Tab. 1 erst in Task 18 · SP11: die 45-s-Pause entfiel mit Klick G28h). Vorschläge 0. ' + T['end_ausgabe'],
    '**Vormerkungen (Textvorschlag 5 § 9, nicht eingebaut):** § 9.1 Kapitel 4 (Formatfehler 4.4, Ausfallkategorie der 10-m-Zeiten von Verein B, „Beteiligung“ in 4.6, Begriffe Adhärenz und Umsetzungsrate) · § 9.2 Schlussfassung der Einleitung (Hypothesen gegen die H0-Entscheidung, „Parameter“ gegen „Zielgröße“, 10-m-Gegenbefund, Ankersatz) · § 9.3 Task 12a · § 9.4 Task 12b · § 9.5 Task 13b · § 9.6 Tasks 16 bis 18 (Abb. 1 mit HL-06 und K-01.18, Anmerkung zu Tab. H3b, veraltete Platzhalter in Anhang H, kursive Symbole, leere Absätze, Semikolon in Anhang C, Endabgleich Fassung 4) · § 9.7 Steuerdokumente-Task (Raster Rev. 4, Umfangsdokument R2, F17 § 5.3 und § 11.9, Berichtsorte im Kennzahlenblatt, Messskript Fassung 5, Skill).',
    '**Offen beim Verfasser:** ' + T['offen1'] + ' · (2) Ausfallkategorie der 10-m-Zeiten von Verein B klären (Textvorschlag 5 § 9.1 Nr. 2) · (3) Gründe der zur Abschlusstestung nicht angetretenen Spieler für Abb. 1 (Raster 5.1.1, B9) · aus Rev. 130 bis 136: (4) `Ordner_aufraeumen.ps1` · (5) Skill-Vorschlag speichern (G26g, G37 h) · (6) H13.',
    '**Stand der Dateien:** Neu: ' + TV5 + ' (Ordner und Projektkopie) · `03_Skripte' + BS + 'Textvorschlag_5_2026-09-30.py` mit `.txt` und `.json` sowie den Bausteinen `_Baustein10.md` und `_Baustein11.md` · `03_Skripte' + BS + 'tv5_md.py` · `03_Skripte' + BS + 'Master_5_2026-09-30.py` · `03_Skripte' + BS + 'Abgleich_Einleitung_Master_2026-09-30.py` mit `.txt` · ' + T['stand_skripte'] + '`03_Skripte' + BS + 'Steuerung_Rev137_2026-09-30.py` mit `.txt` · ' + ARCHIV_M + ' (MD5 `c7657a2c…`) · `_Archiv' + BS + '_ersetzt_2026-09-30_Messskript_Fassung3' + BS + '` (Skript mit `.txt` und `.csv` vom 28.09.). ' + T['stand_mess'] + ' · diese Notizen (Rev. 137 auf Rev. 136) · Maßnahmenliste (Stand, B5, G28g, G29, G32, G35, G37, Taskzeilen) · Plan (Nachtrag, Startsätze 12a, 12b, Einleitung Schlussfassung, 13b), je Ordner und Projektkopie. ' + T['masterzeile'] + ' Unverändert: Fassung 17, Gliederung v6, Berichtsraster, Kennzahlenblatt, Objekte, T1, T4. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen. Die Übergabe `claude/Uebergabe_Rueckschreibung_Task11_2026-09-30.md` und `claude/task11/` im Projekt sind damit erledigt und gelöscht.',
    '**Nächster Schritt:** ' + T['naechst'],
])
NEU_TEXTE.append(block)
anker = '### ⭐⭐ NEU (Rev. 136, 30.09.2026, 21:25 Sitzungsuhr'
notiz = ersetze(notiz, anker, block + '\n\n' + anker, 'Notizen Block Rev. 137')
schreiben(NOTIZ, notiz)

with open(os.path.join(OUT, 'Steuerung_Rev137_2026-09-30.txt'), 'w', encoding='utf-8') as f:
    f.write('Steuerung_Rev137_2026-09-30.py, Modus %s, Datum %s, Uhrzeit %s\n' % (MODUS, DATUM, UHR) + '\n'.join(LOG) + '\n')
print('fertig')

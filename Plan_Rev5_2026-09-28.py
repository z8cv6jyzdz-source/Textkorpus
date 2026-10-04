# -*- coding: utf-8 -*-
"""
Plan_Rev5_2026-09-28.py — Plan der weiteren Schritte `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` Rev. 4 → Rev. 5
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task Steuerdokumente 28.09. (Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 5.3)

Inhalt: Kopf und Rev.-5-Vermerk · § 0 und § 1a auf den Stand vom 28.09. (Messskript Fassung 3, Textvorschlag Einleitung) · § 2 als erledigt,
§ 2.1 Nr. 5 bis 8 nach Textvorschlag 4.7 § 7 · Block A Task 1b · Block C → Task 7 neu (Einleitung) · Tasks 11 bis 18 auf Fassung 17,
Gliederung v5, Berichtsraster Rev. 3, Ankersatz aus der Einleitung (K6), Anhang G ohne Prüfprotokolle, Seitengrenze nach K1 bis K3, Task 14
entfällt, Task 18 (j) Umnummerierung · § 4 Reihenfolge · § 5 Budget mit 6.350 und Seitenmodell · § 7.1 Klickfragen 4, 10, 11, 14 ·
§ 8 Startsätze · § 9 Änderungsliste. Werte aus Messskript, Seitenmodell und Textvorschlag Einleitung, keine Zahl von Hand.
Jede Ersetzung genau einmal, sonst Abbruch. Verweise „F14 §“ werden nur in den laufenden Tasks (11 bis 18), § 7 und § 8 auf „F17 §“ gestellt.
Aufruf: python Plan_Rev5_2026-09-28.py <Plan_Rev4.md> <Manuskriptstand.csv> <Manuskriptstand.txt> <Seitenmodell.csv>
        <Textvorschlag_Einleitung.md> <Uebergabe_Einleitung.md> <Ausgabe.md>
Ohne Semikolon im Skript (chr(59)). Fassung 2 (28.09.): § 7.2 Hedges (1981) nach Textvorschlag 4.7 § 7.
Fassung 3 (28.09., nach der übergreifenden Zweitprüfung der Steuerdokumente und den Klicks von 19:25): Tasks 11 und 18 nach
Fassung 17 § 5.3 (Objekte erst in Task 18, im Text keine Platzhalter), Klickpunkt Nr. 23, Eingang Task 12, Tab. H6 ohne R14,
Verdünnungslogik in 6.1 und G3, „vorgemerkt für“ an leeren Zielorten, § 4 Nr. 1, § 7.1 Nr. 5 bis 9, Startsätze.
"""
import csv
import re
import sys

SRC, M_CSV, M_TXT, S_CSV, TV_E, UE_E, OUT = sys.argv[1:8]
SEMI = chr(59)
t = open(SRC, encoding='utf-8').read()
LOG = []


def de(x, nk=0):
    s = ('%.' + str(nk) + 'f') % x
    ganz, _, dez = s.partition('.')
    g = []
    while len(ganz) > 3:
        g.insert(0, ganz[-3:])
        ganz = ganz[:-3]
    g.insert(0, ganz)
    return '.'.join(g) + (',' + dez if dez else '')


def eins(muster, text, name):
    r = re.findall(muster, text, re.M)
    if len(r) != 1:
        raise SystemExit('Abbruch: %s %d-mal' % (name, len(r)))
    return r[0]


def rep(alt, neu):
    global t
    n = t.count(alt)
    if n != 1:
        raise SystemExit('Abbruch: %d Treffer statt 1 für: %s' % (n, alt[:110]))
    t = t.replace(alt, neu)
    LOG.append(alt[:60].replace('\n', ' '))


def zeile(praefix, neu):
    global t
    zl = t.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('Abbruch: %d Zeilen beginnen mit: %s' % (len(idx), praefix))
    zl[idx[0]] = neu
    t = '\n'.join(zl)
    LOG.append('Zeile ' + praefix[:50])


def abschnitt(von, bis, neu):
    global t
    zl = t.split('\n')
    i0 = [i for i, z in enumerate(zl) if z.startswith(von)]
    i1 = [i for i, z in enumerate(zl) if z.startswith(bis)]
    if len(i0) != 1 or len(i1) != 1 or i1[0] <= i0[0]:
        raise SystemExit('Abbruch: Abschnitt %s bis %s nicht eindeutig' % (von, bis))
    zl = zl[:i0[0]] + neu.rstrip('\n').split('\n') + [''] + zl[i1[0]:]
    t = '\n'.join(zl)
    LOG.append('Abschnitt ' + von[:50])


# ------------------------------------------------------------------ Werte
w = {r['arbeitsnummer']: int(r['woerter']) for r in csv.DictReader(open(M_CSV, encoding='utf-8'))}
mess = open(M_TXT, encoding='utf-8').read()
K4 = sum(w[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5', '4.5.1', '4.5.2', '4.6', '4.7'])
ALT = sum(w[k] for k in ['2', '2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.5', '3'])
GES = sum(v for k, v in w.items() if re.match(r'^[1-7](\.|$)', k))
SEMI_N = int(eins(r'Semikola außerhalb von Zitierklammern, Kapitel 1 bis 7: (\d+)', mess, 'Semikola'))
VERW_N = int(eins(r'Nummerierte Abschnittsverweise, Kapitel 1 bis 7: (\d+)', mess, 'Verweise'))
MP = eins(r'Prognose Einleitung bis Ende Literaturverzeichnis: (\d+,\d) Seiten', mess, 'Prognose Messskript')
P = {r['parameter']: float(r['wert']) for r in csv.DictReader(open(S_CSV, encoding='utf-8'), delimiter=SEMI)}
GB = de(P['prognose_gesamt_basis'], 1)
GO = de(P['prognose_gesamt_obere'], 1)
tv = open(TV_E, encoding='utf-8').read()
TVW = eins(r'\| Wörter gesamt \| \*\*(\d{1,2}\.\d{3}|\d{3,4})\*\*', tv, 'Wortzahl Textvorschlag')
TVW_I = int(TVW.replace('.', ''))
REST = 450 + 1600 + 250
ue = open(UE_E, encoding='utf-8').read()
START_E = eins(r'^> (Task 7 neu: Textvorschlag Einleitung nach .+)$', ue, 'Startsatz Übergabe Einleitung')
V = dict(k4=de(K4), alt=de(ALT), ges=de(GES), semi=SEMI_N, verw=VERW_N, mp=MP, gb=GB, go=GO, tvw=TVW, rest=de(REST),
         summe_b=de(1500 + K4 + REST), summe_t=de(TVW_I + K4 + REST), w47=w['4.7'])

# ------------------------------------------------------------------ Kopf und Rev.-5-Vermerk
rep('# Plan der weiteren Schritte — Stand 25.09.2026, spät, Rev. 4', '# Plan der weiteren Schritte — Stand 28.09.2026, Rev. 5')
rep('Die Startsätze in § 8 für die Tasks 7 bis 10 und 14 gelten nicht mehr. Maßnahme G35.\n',
    'Die Startsätze in § 8 für die Tasks 7 bis 10 und 14 gelten nicht mehr. Maßnahme G35.\n\n'
    '**Rev. 5 (28.09.2026, Task Steuerdokumente, Rev. 115 der Sitzungsnotizen):** Steuerdokumente auf dem Stand vom 28.09.: '
    'Projektanweisungen Fassung 17 (wirksam nach dem Einsetzen durch den Verfasser, A8), Gliederung v5 (`01_Verfahren\\Gliederung_2026-09-28`), '
    'Berichtsraster Rev. 3, Messskript Fassung 3, Seitenmodell `03_Skripte\\Seitenmodell_2026-09-28`. Umfang 6.350 Wörter und höchstens 33 Seiten '
    'von der Einleitung bis zum Ende des Literaturverzeichnisses (Klicks K1 bis K3), Regel R6 entfällt, Ankersatz in 6.1 und in der Zusammenfassung '
    '(K6). Block C ist Task 7 neu (Einleitung), der Textvorschlag liegt vor (Rev. 114), Klickfrage 10 ist dort entschieden. Task 14 entfällt, '
    'Task 1b (dieser Task) ist erledigt. Verweise „F14 §“ in den laufenden Tasks, in § 7 und § 8 zeigen auf Fassung 17 mit gleicher Nummer, '
    'in den erledigten Teilen bleiben sie historisch. Per Skript `03_Skripte\\Plan_Rev5_2026-09-28.py`, Rev. 4 als Kopie in '
    '`_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`. Änderungsliste in § 9.\n')

# ------------------------------------------------------------------ § 0
rep('0. **Stand Rev. 4.**',
    '**Stand Rev. 5 (28.09.).** Kapitel 4 ist textlich fertig (%(k4)s Wörter gegen 2.550). Die Einleitung liegt als Textvorschlag vor '
    '(%(tvw)s Wörter, Rev. 114), die Übertragung in den Master steht beim Verfasser. Im Master steht noch der Altbestand von Kapitel 2 und 3 '
    '(%(alt)s Wörter mit allen %(semi)d Semikola und %(verw)d Abschnittsverweisen). Zu schreiben sind Kapitel 5 bis 7 mit %(rest)s Wörtern '
    'Budget. Seitenprognose %(mp)s Seiten mit den gemessenen Wörtern, %(gb)s mit vollen Budgets (Modellrechnung, § 5). Nächster Schritt ist die '
    'Übertragung der Einleitung und ihr Abgleich (Task 7 neu), danach Task 11. Die Punkte 0 bis 6 sind der Stand vom 25.09.\n\n'
    '0. **Stand Rev. 4.**' % V)

# ------------------------------------------------------------------ § 1a
rep('Die 134 Wörter unter dem Budget von Kapitel 4 werden nicht aufgefüllt (Regel R6).',
    'Die 134 Wörter unter dem Budget von Kapitel 4 werden nicht aufgefüllt (Fassung 17 § 5.2, Regel R6 entfällt nach K2).\n\n'
    '**Stand 28.09. (Rev. 5, Messskript Fassung 3, Master unverändert seit 26.09.):** Kapitel 4 %(k4)s gegen 2.550, 4.7 %(w47)s gegen 550 · '
    'Einleitung im Master noch Altbestand %(alt)s (Kapitel 2 und 3), Textvorschlag Einleitung %(tvw)s gegen 1.500 · Absatztext mit Altbestand '
    '%(ges)s gegen 6.350 · Semikola %(semi)d und Abschnittsverweise %(verw)d, alle im Altbestand · Seitenprognose %(mp)s Seiten (Modellrechnung).' % V)

# ------------------------------------------------------------------ § 2
rep('## 2 Schritt 0 — Prüfung von 4.7 durch den Verfasser\n',
    '## 2 Schritt 0 — Prüfung von 4.7 durch den Verfasser\n\n**Erledigt 26.09. (Rev. 107 und 108):** Schritt 0 ist mit Task 6 abgeschlossen, '
    'die Nachkorrekturen stehen im Master. § 2 ist historisch.\n')
rep('8. **Absatz 7:** „Prüfprotokolle, Poweranalyse, Skripte und Diagramme der Voraussetzungsprüfung stehen in Anhang G.“',
    '**Stand nach Task 6 (Textvorschlag 4.7, Nr. 57, Verfasser 26.09.):** zu Nr. 5 — die Freigabe ohne unabhängige Methodenprüfung steht genau '
    'einmal in 6.3 · zu Nr. 6 — Gegenproben und Formelprobe werden in 4.7 nicht berichtet, die KI-Deklaration nennt die Gegenproben · zu Nr. 7 — '
    'der Produktname steht in der KI-Deklaration und in Anhang G, nicht in 4.7 · zu Nr. 8 — Anhang G ohne Prüfprotokolle, 4.7 verweist auf '
    'Skripte, Poweranalyse und Diagramme.\n\n'
    '8. **Absatz 7:** „Prüfprotokolle, Poweranalyse, Skripte und Diagramme der Voraussetzungsprüfung stehen in Anhang G.“')

# ------------------------------------------------------------------ § 3 Vorspann, Block A
rep('das Berichtsraster Rev. 2 als Einstieg je Abschnitt,', 'das Berichtsraster (seit dem 28.09. Rev. 3) als Einstieg je Abschnitt,')
rep('### Block B — Textrevision Kapitel 4 (Kürzung des Bestands, Priorität des Verfassers)',
    '**Task 1b · Steuerdokumente 28.09.** *Ziel:* Die Dokumente, die jeder Task zuerst liest, auf den Neuzuschnitt vom 28.09. bringen. '
    '*Eingang:* `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md`. *Klickpunkte:* K1 bis K3 (Seitengrenze), K6 (Ankersatz), K4 '
    '(Bereinigung der Projektdokumente), K5 (Freigabe von Fassung 17). *Erledigt 28.09. (Rev. 115):* Projektanweisungen Fassung 17 mit '
    'Prüfskript und Zweitprüfung, Gliederung v5, Berichtsraster Rev. 3, dieser Plan Rev. 5, Messskript Fassung 3, Seitenmodell, Übergabe '
    'Einleitung, README, Aufräumskript, Archivkopien, Skill-Vorschlag, Maßnahmenliste. Fassung 17 wird wirksam, wenn der Verfasser sie einsetzt (A8).\n\n'
    '### Block B — Textrevision Kapitel 4 (Kürzung des Bestands, Priorität des Verfassers)')

# ------------------------------------------------------------------ Block C → Task 7 neu
BLOCK_C = '''### Block C — Einleitung (Neuzuschnitt 28.09., ersetzt die Kürzung von Kapitel 2)

**Task 7 neu · Einleitung** (Kapitel 1 bis 3 in einem Kapitel ohne Unterabschnitte, höchstens 1.500 Wörter). *Ziel:* eine Einleitung als Trichter in acht Zügen, die Relevanz, Zielgrößen und Diagnostik, Sommerpause, Trainingsmittel, Reifung, Forschungsstand, Lücke, Zweck und Hypothesen trägt. *Eingang:* `04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md` (Bauplan § 3, Pflichtinhalte § 4, Verbleibsliste § 5, Regeln § 6) · Befund Relevanz Rev. 2 · Textvorschlag 2.4 Fassung 6 als Material · Master 2.1 bis 2.3 · Berichtsraster Rev. 3 § 3.1 (Kopfblock Einleitung) · Fassung 17 § 5a, § 6.2, § 6.4 bis § 6.6 · T1 und T4. *Budget:* höchstens 1.500, kein Unterbudget, nicht auffüllen. *Klickpunkte:* Verbleibsliste · Klickfrage 10 (Wortlaut des Ankersatzes) · Stufenwahl. *Ausgang:* Textvorschlag Einleitung, Übertragung durch den Verfasser (Gliederung v5, M24), danach Abgleich nach Übergabe Einleitung § 8 Nr. 6. *Prüfung:* Messung höchstens 1.500, null Semikola außerhalb der Zitiersyntax und null Abschnittsverweise, Zweitprüfung durch Subagent, Endabgleich.

*Stand 28.09. (Rev. 114):* Textvorschlag `04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md` mit %(tvw)s Wörtern vorgelegt, Verbleibsliste und Wortlaut des Zwecks per Klick entschieden (Klickfrage 10 erledigt), Zweitprüfung eingearbeitet. Offen: Übertragung durch den Verfasser, danach Abgleich Satz für Satz, Messskript, Endabgleich, Rev., Maßnahmenliste, T1, T4, Projektkopien (Übergabe Einleitung § 8 Nr. 6). Die Tasks 7 bis 10 der Rev. 4 (Kürzung 2.4, 2.3, 2.1, 2.2) sind durch Task 7 neu ersetzt, ihre Beschreibungen stehen in Rev. 4 im Archiv.
''' % V
abschnitt('### Block C — Kürzung Kapitel 2', '### Block D — Neue Kapitel', BLOCK_C)

# ------------------------------------------------------------------ Tasks 11 bis 18
rep('Gliederung v4 § 3.1 (Zeilen 5, 5.1, 5.2), § 3.2 „Kapitel 5“, M11, M12', 'Gliederung v5 § 3.1 (Zeilen 5, 5.1, 5.2), § 5 (M11, M12)')
rep('(Vorab-Erwartungen: Lloyd et al. 2016 mit dem Vorbehalt L14 b, Ramirez-Campillo et al. 2020, Moran et al. 2016/2017, Liu et al. 2024)',
    '(Vorab-Erwartungen: Lloyd et al. 2016 mit dem Vorbehalt L14 b, Ramirez-Campillo et al. 2020, Moran et al. 2017, Liu et al. 2024)')
rep('*Aufbau:* 6.1 Eröffnungsabsatz (Zweck als Ankersatz → Hauptbefund → Gegenbefund, ohne Beleg und Zahl)',
    '*Aufbau:* 6.1 Eröffnungsabsatz (Zweck als Ankersatz aus der Einleitung, nahezu wörtlich → Hauptbefund → Gegenbefund, ohne Beleg und Zahl)')
rep('*Besonderheiten:* Der **Ankersatz** (Zweck) wird hier formuliert und für Kapitel 1, 3 und die Zusammenfassung festgeschrieben (Klickfrage 10).',
    '*Besonderheiten:* Der **Ankersatz** (Zweck) kommt aus der Einleitung (Task 7 neu, Klickfrage 10 dort entschieden) und kehrt im '
    'Eröffnungsabsatz von 6.1 nahezu wörtlich wieder (Klick K6).')
rep('Zu Beginn wird der Skill-Nachtrag zu Schritt 4a (Zuordnung Eröffnung und Zielgrößen = 6.1, Methodendiskussion = 6.2, Limitationskette = 6.3, Ausblick = 7, Gliederung v4 § 7 Nr. 3) zur Speicherung vorgeschlagen.',
    'Der Skill-Nachtrag zu Schritt 4a (Zuordnung Eröffnung und Zielgrößen = 6.1, Methodendiskussion = 6.2, Limitationskette = 6.3, Ausblick = 7) '
    'ist mit dem Skill-Vorschlag vom 28.09. vorgelegt (Rev. 115). Ist er nicht gespeichert, wird er zu Beginn erneut vorgeschlagen.')
rep('*Klickpunkte:* Ankersatz · Vorstudien je Zielgröße (Vorschlag aus F14 § 6.5) · Stufenwahl.',
    '*Klickpunkte:* Vorstudien je Zielgröße (Vorschlag aus F17 § 6.5) · Stufenwahl.')
rep('Gliederung v4 § 3.3 (Vorspann, Klick 7: durchlaufender Block ohne Struktur-Label)', 'Gliederung v5 § 3.3 (Vorspann, Klick 7: durchlaufender Block ohne Struktur-Label)')
rep('· Ankersatz aus Task 12 · G25d (M16).', '· Ankersatz aus der Einleitung (Task 7 neu, K6) · G25d (M16) · G34 (b).')
rep('→ Forschungsausblick mit der in 6.2 hergeleiteten Fallzahlempfehlung, keine neue Zahl, keine Quelle',
    '→ Forschungsausblick mit der in 6.2 hergeleiteten Fallzahlempfehlung und zwei Satzteilen (Verletzungen als Endpunkt, Umsetzung als '
    'Hypothese, G34 b), keine neue Zahl, keine Quelle')
zeile('**Task 14 · Kapitel 1, 2.5 und 3**', '**Task 14 · entfällt** (Neuzuschnitt 28.09., G35): Kapitel 1, 2.5 und 3 gehen in der Einleitung auf (Task 7 neu). '
      'Die Beschreibung der Rev. 4 steht im Archiv.')
rep('Offene Metadaten als Vorschlagsliste: Clarke Verlagsfassung (K24), RC 2020 Band und Seiten (L14 d), Moran-Jahr (L14 c), Draper und Lancaster als Sekundärzitat, Dugdale 2019 statt 2020, Microgate (2016), FVM-Rahmenterminplan, Ferienordnung NRW.',
    'Offene Metadaten als Vorschlagsliste: Clarke Verlagsfassung (K24), RC 2020 Band und Seiten (L14 d), Draper und Lancaster als Sekundärzitat, '
    'Dugdale 2019 statt 2020, Microgate (2016), Zitierjahre nach der Version of Record (Hicks 2020, Radnor 2018, Moran 2017, L14 c erledigt). '
    'FVM-Rahmenterminplan und Ferienordnung NRW entfallen mit dem Altbestand 2.3, die übrigen Streichungen nennt die Verbleibsliste der '
    'Einleitung (Textvorschlag Einleitung § 4). *Seitenmessung:* Das fertige Verzeichnis wird in Word gemessen und gegen das Seitenmodell '
    'gehalten, Kontrolle der Grenze 33 nach K1 (F17 § 1.1).')
rep('Q-Q- und Linearitätsdiagramme (`06_Abbildungen\\Anhang_G`), Prüfprotokolle (Belegprotokoll, Abgleichprotokoll, Durchsichts- und Plausibilitätsprotokoll, Handprobe, Rückfragenprotokoll, Nachtrag 3), Umgebung.',
    'Q-Q- und Linearitätsdiagramme (`06_Abbildungen\\Anhang_G`), Umgebung, jedes Skript als KI-erzeugt gekennzeichnet. Ohne Prüfprotokolle '
    '(Verfasser 26.09., Textvorschlag 4.7, Nr. 57), sie bleiben im Projekt und werden auf Anfrage vorgelegt.')
rep('berichtete R-Rechnung durch eine blinde zweite Instanz, Python-Gegenprobe, Textvorschläge.',
    'berichtete R-Rechnung durch eine blinde zweite Instanz, Python-Gegenprobe, Textvorschläge. Mindestinhalt nach F17 § 14 '
    '(Textvorschlag 4.7, Nr. 57).')
rep('(a) Vormerkungen aus den Tasks 11 bis 14 für Kapitel 4 und 2 in einem Durchgang einarbeiten',
    '(a) Vormerkungen aus den Tasks 7 neu und 11 bis 13 für Kapitel 4 in einem Durchgang einarbeiten')
rep('Absatztext ≤ 9.000 und jeder Abschnitt im Budget', 'Absatztext ≤ 6.350 und jeder Abschnitt im Budget')
rep('Seitenzahl messen (≤ 37, Ziel ≥ 30, bei Unterschreitung Regel R6: Tab. H4, dann Tab. H2 in den Textteil, ohne Wortkosten)',
    'Seitenzahl messen, ≤ 33 nach der Zählweise aus K1 (Einleitung bis Ende des Literaturverzeichnisses, ohne Vorspann und Anhang), '
    'Regel R6 entfällt (K2), nie auffüllen')
rep('(i) Prüfliste Berichtsraster § 7 (vierzehn Punkte) als Protokoll `02_Befunde\\Abgabepruefung_⟨Datum⟩`. *Klickpunkte:* Ergebnis der Seitenmessung (R6), Freigabe der Abgabe.',
    '(i) Prüfliste Berichtsraster § 7 (vierzehn Punkte) als Protokoll `02_Befunde\\Abgabepruefung_⟨Datum⟩` · (j) Überschriften der alten '
    'Kapitel 2 und 3 entfernt (falls nicht schon nach Task 7 neu geschehen), Umnummerierung 4 → 2 bis 7 → 5 per Skript in Master, '
    'Steuerdokumenten, Skripten und Textvorschlägen (G35 d, Gliederung v5 M25), danach F9. *Klickpunkte:* Ergebnis der Seitenmessung '
    '(Grenze 33, Tauschregel ab 32), Freigabe der Abgabe.')

# F14 → F17 in den laufenden Tasks (11 bis 18), § 7 und § 8
zl = t.split('\n')
lauf = False
for i, z in enumerate(zl):
    if z.startswith('**Task 11 ·') or z.startswith('## 7 Klickfragen'):
        lauf = True
    if z.startswith('## 4 Reihenfolge') or z.startswith('## 9 Prüfung'):
        lauf = False
    if lauf and 'F14 §' in z:
        zl[i] = z.replace('F14 §', 'F17 §')
        LOG.append('F14 → F17 in Zeile %d' % (i + 1))
t = '\n'.join(zl)

# ------------------------------------------------------------------ § 4
rep('**Entscheidung (25.09., abends):** Die vorhandenen Kapitel werden zuerst gekürzt,',
    '**Rev. 5 (28.09.):** Mit dem Neuzuschnitt ersetzt die Einleitung (Task 7 neu) die Kürzung von Kapitel 2 und Task 14. Danach folgen '
    'Task 11, 12, 13 und 15 bis 18. Nr. 1 gilt für die Tasks 7 neu und 11 bis 13, Nr. 2 ist neu gefasst, Nr. 3 entfällt.\n\n'
    '**Entscheidung (25.09., abends):** Die vorhandenen Kapitel werden zuerst gekürzt,')
zeile('2. **Der Ankersatz** (Zweck der Arbeit)', '2. **Der Ankersatz** (Zweck der Arbeit) entsteht in der Einleitung (Task 7 neu, Wortlaut per Klick '
      'entschieden) und kehrt im Eröffnungsabsatz von 6.1 und in der Zusammenfassung nahezu wörtlich wieder, 4.1 bleibt ohne Zwecksatz (Klick K6, 28.09.).')
zeile('3. **Kapitel 2 wird gekürzt, bevor 2.5 und 6.1 stehen.**', '3. *Entfällt (28.09.):* Kapitel 2 wird nicht mehr gekürzt, sondern durch '
      'die Einleitung ersetzt.')

# ------------------------------------------------------------------ § 5
rep('## 5 Budgetarithmetik und Kürzungsauftrag\n',
    '## 5 Budgetarithmetik und Kürzungsauftrag\n\n**Stand Rev. 5 (28.09., Messskript Fassung 3, Budgets nach Fassung 17 § 5.2):**\n\n'
    '| Posten | Wörter |\n|---|---:|\n'
    '| Absatztext im Master mit Altbestand (Kapitel 2 und 3) | %(ges)s |\n'
    '| davon Altbestand, wird durch die Einleitung ersetzt | %(alt)s |\n'
    '| Kapitel 4 (Arbeitsnummer, 4.1 bis 4.7) gegen 2.550 | %(k4)s |\n'
    '| Textvorschlag Einleitung gegen 1.500 | %(tvw)s |\n'
    '| Budget der leeren Abschnitte 5.1 bis 7 | %(rest)s |\n'
    '| Summe mit vollem Einleitungsbudget | %(summe_b)s |\n'
    '| Summe mit dem Textvorschlag Einleitung | %(summe_t)s |\n'
    '| Hartgrenze (Fassung 17 § 1.1) | 6.350 |\n\n'
    'Einen Kürzungsauftrag gibt es nicht mehr. Nicht verbrauchte Wörter werden nicht aufgefüllt und gehen nicht auf andere Abschnitte über. '
    'Die Tabelle darunter ist der Stand vom 25.09.\n' % V)
rep('**Seitenprognose (F14 § 1.1, Modellrechnung, keine Messung):** 30,3 Seiten bei 9.000 Wörtern. Gemessen wird in Word nach Task 18 (h). Fällt die Messung unter 30, wird nicht mit Text aufgefüllt, sondern mit Tab. H4, dann Tab. H2 (Regel R6).',
    '**Seitenprognose (Fassung 17 § 1.1, Modellrechnung, keine Messung):** %(gb)s Seiten mit vollen Budgets, %(go)s in der oberen Variante des '
    'Literaturverzeichnisses, %(mp)s mit den am 28.09. gemessenen Wörtern (Messskript, Block „Seitenschätzung“), gezählt von der Einleitung bis '
    'zum Ende des Literaturverzeichnisses (K1). Grenze 33, Tauschregel ab 32 (K3), R6 entfällt (K2). Gemessen wird in Word nach Task 15 und in '
    'Task 18 (h). *Stand 25.09., historisch:* 30,3 Seiten bei 9.000 Wörtern.' % V)

# ------------------------------------------------------------------ § 7
zeile('| 4 | Fassung 15 in die Projekteinstellungen einsetzen (A8)', '| 4 | Fassung 15 in die Projekteinstellungen einsetzen (A8) | — | '
      '**historisch:** Fassung 15 wurde nicht eingesetzt, Fassung 16 am 25.09., Fassung 17 nach Klick K5 (Task 1b) |')
zeile('| 10 | Ankersatz (Zweck der Arbeit)', '| 10 | Ankersatz (Zweck der Arbeit) | — | **beantwortet 28.09. in Task 7 neu:** „… gegenüber einer '
      'Kontrollgruppe verbessert“ (Textvorschlag Einleitung § 7), Wiederkehr in 6.1 und in der Zusammenfassung (K6) |')
zeile('| 11 | Titel 2.5 (M9)', '| 11 | Titel 2.5 (M9) | — | **gegenstandslos:** 2.5 geht in der Einleitung auf |')
zeile('| 14 | Produktname in 4.7', '| 14 | Produktname in 4.7 (§ 2.1 Nr. 7) | — | **gegenstandslos:** 4.7 nennt kein Produkt, der Name steht in der '
      'KI-Deklaration und in Anhang G (Textvorschlag 4.7, Nr. 57) |')
rep('Clemente et al. (2022, H6, frei über PMC) und Melchiorri et al. (2023, H4), Ruf et al. (2024) und Clemente et al. (2021, H5) für 2.3 und 6.1',
    'Clemente et al. (2022, H6, frei über PMC, nur noch für 6.1) und Melchiorri et al. (2023, H4), Ruf et al. (2024) und Clemente et al. (2021, H5) für 6.1')
rep('Hedges (1981, H9) belegt den Faktor J in 4.7 — ohne Volltext bleibt der Satz ohne Klammer',
    'Hedges (1981, H9) belegt Hedges\' g in 4.7 (4.7 nennt den Faktor J nicht mehr, Textvorschlag 4.7 § 7) — ohne Volltext bleibt der Satz ohne Klammer')
rep('Vor Task 8 (2.3), Task 12 und Task 15 lohnt ein Blick auf die Liste.', 'Vor Task 12 und Task 15 lohnt ein Blick auf die Liste.')

# ------------------------------------------------------------------ § 8
rep('(ab Task 6: Fassung 16, Fassung 15 wird nicht eingesetzt)', '(bis zum Einsetzen von Fassung 17 gilt Fassung 16, danach Fassung 17)')
zeile('- **Tasks 7 bis 10:**', '- **Task 7 neu:** „%s“ (Textvorschlag liegt vor, nach der Übertragung weiter mit Übergabe Einleitung § 8 Nr. 6.) '
      'Die Startsätze der Tasks 7 bis 10 der Rev. 4 gelten nicht mehr.' % START_E)
rep('Skill-Nachtrag Schritt 4a vorschlagen, Ankersatz per Klick festlegen, dann 6.1, 6.2, 6.3',
    'Skill-Nachtrag Schritt 4a prüfen, Ankersatz aus der Einleitung übernehmen (K6), dann 6.1, 6.2, 6.3')
rep('Gliederung v4 § 3.3, F17 § 10, Ankersatz aus Rev. ⟨Nummer⟩.', 'Gliederung v5 § 3.3, F17 § 10, Ankersatz aus der Einleitung (Textvorschlag Einleitung, Absatz 9).')
zeile('- **Task 14:**', '- **Task 14:** entfällt (Einleitung, Task 7 neu).')
rep('Abgleich mit T1, T4 und F17 § 8, Volltextprüfung, Vorschlagsliste offener Metadaten,',
    'Abgleich mit T1, T4 und F17 § 8, Volltextprüfung, Seitenmessung des Verzeichnisses gegen das Seitenmodell, Vorschlagsliste offener Metadaten,')
rep('Vormerkungen aus den Tasks 11 bis 14 als Vorschlagsliste', 'Vormerkungen aus den Tasks 7 neu und 11 bis 13 als Vorschlagsliste')
rep('Seitenmessung und F9 durch den Verfasser, Ergebnis per Klick, Regel R6.',
    'Seitenmessung nach K1 und F9 durch den Verfasser, Ergebnis per Klick, Umnummerierung nach Gliederung v5 M25.')

# ------------------------------------------------------------------ § 9
rep('**Änderungen in Rev. 2 gegenüber Rev. 1 (beide 25.09., abends):**',
    '**Änderungen in Rev. 5 (28.09.2026):** Kopf und Rev.-5-Vermerk · § 0 Stand 28.09. · § 1a Stand nach Messskript Fassung 3, R6 nach K2 · '
    '§ 2 erledigt, Nr. 5 bis 8 nach Textvorschlag 4.7 Nr. 57 · Block A Task 1b · Block C Task 7 neu mit Stand Rev. 114 · Task 11 Gliederung v5 · '
    'Task 12 Ankersatz aus der Einleitung, Moran 2017, Skill-Nachtrag · Task 13 Ankersatz, Gliederung v5, G34 (b) · Task 14 entfällt · Task 15 '
    'Metadaten und Seitenmessung · Task 16 Anhang G ohne Prüfprotokolle, Deklaration nach F17 § 14 · Task 18 (a), (f), (h), (j) · § 4 Nr. 2 und 3 · '
    '§ 5 Budget mit 6.350 und Seitenmodell · § 7.1 Nr. 4, 10, 11, 14 · § 7.2 · § 8 Startsätze · „F14 §“ in den laufenden Teilen auf „F17 §“. '
    'Werte aus Messskript, Seitenmodell und Textvorschlag Einleitung per Skript `03_Skripte\\Plan_Rev5_2026-09-28.py`.\n\n'
    '**Änderungen in Rev. 2 gegenüber Rev. 1 (beide 25.09., abends):**')


# ------------------------------------------------------------------ Fassung 3: übergreifende Zweitprüfung (Befunde 1, 2, 9, 12, 14, 15, 22 bis 25,
# 37, 38) und Klicks 28.09., 19:25 (Erratum ohne Ort in der Arbeit, Verdünnungslogik in 6.1 und G3)
# Kopf und Nachtrag 28.09. (Befund 37)
rep('Übergabe für den ersten Task `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md`.',
    'Übergabe für den ersten Task `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md` (erledigt, Kopie in '
    '`_Archiv\\_ersetzt_2026-09-28_Uebergaben`).')
rep('Seitenprognose rund 21. Methodik bis Fazit', 'Seitenprognose rund 21 (überholt durch Rev. 5, § 5). Methodik bis Fazit')
# § 1 Objekte als historisch (Befund 1)
rep('**Objekte:** Tab. 1 steht in 4.4.',
    '**Objekte:** *Stand 25.09., historisch. Seit dem 25.09., 22:25 gilt Fassung 17 § 5.3: alle Objekte erst in Task 18, bis dahin im '
    'Text keine Platzhalter.* Tab. 1 steht in 4.4.')
# § 2.1: Block „Stand nach Task 6“ ans Ende, Zielorte als „vorgemerkt für“ (Befunde 12 und 37)
B_ALT = ('**Stand nach Task 6 (Textvorschlag 4.7, Nr. 57, Verfasser 26.09.):** zu Nr. 5 — die Freigabe ohne unabhängige Methodenprüfung steht '
         'genau einmal in 6.3 · zu Nr. 6 — Gegenproben und Formelprobe werden in 4.7 nicht berichtet, die KI-Deklaration nennt die Gegenproben · '
         'zu Nr. 7 — der Produktname steht in der KI-Deklaration und in Anhang G, nicht in 4.7 · zu Nr. 8 — Anhang G ohne Prüfprotokolle, 4.7 '
         'verweist auf Skripte, Poweranalyse und Diagramme.\n\n')
B_NEU = ('**Stand nach Task 6 (Textvorschlag 4.7, Nr. 57, Verfasser 26.09.):** zu Nr. 5 — die Freigabe ohne unabhängige Methodenprüfung ist '
         'für 6.3 vorgemerkt, dort genau einmal · zu Nr. 6 — Gegenproben und Formelprobe werden in 4.7 nicht berichtet, sie sind für die '
         'KI-Deklaration vorgemerkt · zu Nr. 7 — der Produktname ist für die KI-Deklaration und Anhang G vorgemerkt, nicht in 4.7 · zu Nr. 8 — '
         'Anhang G ohne Prüfprotokolle, 4.7 verweist auf Skripte, Poweranalyse und Diagramme.\n')
rep(B_ALT, '')
rep('sollte das jetzt sagen, dann wird der Satz in Task 6 angepasst.\n', 'sollte das jetzt sagen, dann wird der Satz in Task 6 angepasst.\n\n' + B_NEU)
# § 3 Vorspann (Befund 14)
rep('Unverändert für alle Tasks gilt F14 § 1.2 (verbindliche Lesefolge vor jeder Textproduktion)',
    'Unverändert für alle Tasks gilt F17 § 1.2 (verbindliche Lesefolge vor jeder Textproduktion)')
rep('(wie `Textvorschlag_4.7_2026-09-25.md` § 7)', '(wie `Textvorschlag_4.7_2026-09-26.md` § 5)')
# Task 11 (Befunde 1, 9, 22)
rep('Berichtsraster § 3.12 und § 3.13 (Zeilen 5.1.1 bis 5.1.10, 5.2.1 bis 5.2.8)', 'Berichtsraster § 3.12 und § 3.13 (Zeilen 5.1.1 bis 5.1.11, 5.2.1 bis 5.2.8)')
rep(' · Gliederung v5 § 3.1 (Zeilen 5, 5.1, 5.2), § 5 (M11, M12) · ', ' · Gliederung v5 § 3.1 (Zeilen 5, 5.1, 5.2) · ')
rep('· `Objekte_2026-09-25` (Tab. 2, Tab. 3, H1 bis H5, Abb. 1, Abb. 2) · G28g, G29 (d) und (e), G25d (M11, M12), G17g (Tab.-2-Feld), B5 (Rest) ·',
    '· `Objekte_2026-09-25` (Tab. 2, Tab. 3, H1 bis H5, Abb. 1, Abb. 2, zum Abgleich der Verweise) · Textvorschlag 4.7 (26.09.) § 7, Zeile '
    'Task 11 (Voraussetzungen nach R2, Bootstrap in genau einem Satz oder Halbsatz, H0-Entscheidung an der adjustierten Differenz, „Größenklasse“ '
    'als Fall der Schlusslogik und nicht als Cohen-Klasse, Per-Protokoll-Sammelsatz nicht als „gleiches Ergebnis“, Nr. 23) · G28g, G29 (d) und '
    '(e), G32 (b), B5 (Rest) · für Task 18 vorgemerkt, nicht in diesem Task: G25d (M11, M12), G17g (Tab.-2-Feld), die Anmerkungen zu Tab. 2 '
    'und Tab. 3 aus Textvorschlag 4.7 (26.09.) § 7 ·')
rep('*Objekte im Master:* Tab. 2 und Tab. 3 als Word-Tabellen per Skript aus den CSV (`Werkzeug_Objekte_Docx_2026-09-25.py`, Beschriftung als '
    'SEQ-Feld wie Tab. 1, damit F9 nummeriert, Anmerkungen nach Umfangsdokument § 3.7) · Abb. 1 und Abb. 2 als Platzhalter mit Beschriftungsfeld '
    '· Anhang H bleibt Platzhalter bis Task 18.',
    '*Objekte:* keine Objekte und keine Platzhalter im Master. Der Text führt Abb. 1, Tab. 2, Abb. 2 und Tab. 3 per Verweis ein, eingesetzt '
    'werden sie in Task 18 (F17 § 5.3). Die Platzhalter in Anhang H bleiben bis Task 18.')
rep('*Verfasserangaben, die der Task braucht:* Umsetzung der 48-h-Vorgabe je Testtermin (Zeile 5.1.10, E) · Bestätigung „planmäßig beendet“ (5.1.4).',
    '*Verfasserangabe, die der Task braucht:* Bestätigung „planmäßig beendet“ (5.1.4). Die 48-h-Vorgabe an den Testterminen steht als '
    'Tatsache in 4.3, Zeile 5.1.10 entfällt (Textvorschlag 4.3 § 6).')
rep('*Klickpunkte:* Lokalisation der Schmerzmeldungen (Zeile 5.1.8):',
    '*Klickpunkte:* zu Beginn Nr. 23 aus Textvorschlag 4.7 (26.09.): Einzelwerte der drei Spieler beim Antragskriterium (K-10.17) behalten '
    'oder den Per-Protokoll-Vergleich in 5.2 mit Zahlen berichten, gegenfinanziert durch den Wegfall der Einzelwerte (Raster 5.2.6, '
    'Umfangsdokument R5, F17 § 11.9) · Lokalisation der Schmerzmeldungen (Zeile 5.1.8):')
# Task 12 (Befund 23, Klick 19:25)
rep('Berichtsraster § 3.14 (6.1.1 bis 6.1.4, 6.2.1 bis 6.2.10, 6.3.1 bis 6.3.5)', 'Berichtsraster § 3.14 (6.1.1 bis 6.1.4, 6.2.1 bis 6.2.12, 6.3.1 bis 6.3.5)')
rep('· die aus 4.7 verschobenen Sätze (Task 6: Planungsmodell, Trennschärfe) · G17d, G17f, G26l, J6, K23, L16, G29 (f).',
    '· die aus 4.7 verschobenen Sätze (Task 6: Planungsmodell, Trennschärfe) · Textvorschlag 4.7 (26.09.) § 7, Zeilen Task 12 mit der '
    'Argumentationslinie für 6.1 und 6.2 (die Formel „Detraining-Prämisse nur an Akademie- und Profispielern belegt“ ist durch F17 § 12 G8 '
    'überholt) · Textvorschlag Einleitung § 6 Nr. 7 und Verbleibsliste § 4 · G17d, G17f, G26l, J6, K23, L16, G29 (f), G32 (c), G33 (d) und '
    '(f), G34 (c).')
rep('je Zielgröße ein Absatz im Fünf-Zug-Muster, Verdünnungslogik, Nutzen und Schaden',
    'je Zielgröße ein Absatz im Fünf-Zug-Muster, Verdünnungslogik als Einordnung des Hauptbefunds (als Limitation in 6.3 G3, Klick 28.09., '
    '19:25), Nutzen und Schaden')
# Task 15 (Befund 36)
rep('Clarke Verlagsfassung (K24), RC 2020 Band und Seiten (L14 d),',
    'Clarke Verlagsfassung (K24), RC 2020 mit den bei Crossref geprüften Heftangaben, Volltext nur als akzeptiertes Manuskript (L14 d, F17 § 8),')
# Task 16 (Befund 38, Klick 19:25)
rep('Umfang nach Klickfrage 12 (vollständiger Abdruck der Skripte oder Verzeichnis mit Ablageort und elektronischer Beigabe).',
    'Umfang nach Klickfrage 12 (vollständiger Abdruck der Skripte oder Verzeichnis mit Ablageort und elektronischer Beigabe). Folge für 4.7: '
    'Werden S01 bis S19 nur verzeichnet, lautet der Verweissatz dort „… sind in Anhang G verzeichnet“ (Textvorschlag 4.7 vom 26.09. § 7, '
    'Task 16 Nr. 4). Kein Hinweis auf das Erratum zu Khamis und Roche (F17 § 13 Nr. 40).')
# Task 18 (Befunde 2, 24, 25, Klick 19:25)
rep('(b) Anhang H setzen: Tab. H1 bis H5 per Skript aus den CSV, Tab. H6 per Skript aus Auswertungsplan § 5 mit § 5.10 (mit R11), je Objekt '
    'Beschriftung als Feld',
    '(b) Objekte setzen: im Textteil Tab. 1 mit Beschriftung und Anmerkung aus Textvorschlag 4.4 § 9 (G31 b, Gliederung v5 M26), Tab. 2 und '
    'Tab. 3 per Skript aus den CSV mit SEQ-Feld und den Anmerkungen aus Textvorschlag 4.7 (26.09.) § 7 (Gliederung v5 M11 und M12, G25d, '
    'G17g), Abb. 1 und Abb. 2 unter (c) · in Anhang H Tab. H1 bis H5 per Skript aus den CSV (Anmerkung zu Tab. H4c nach Textvorschlag 4.7 § 7, '
    'Anmerkung zu Tab. H1b nach G31 b), Tab. H6 per Skript aus Auswertungsplan § 5 mit § 5.10, mit Spalte Grund, den Festlegungsdaten und R11 '
    '(G32 h) und mit der nicht erhobenen 20-m-Zwischenzeit (G31 b), ohne R1, R9, R10, R12, R13 und R14 (F17 § 13 Nr. 40), je Objekt '
    'Beschriftung als Feld · Entscheidungspunkte: Streichpaket Bootstrap (Textvorschlag 4.7 § 7, G32 h) und Nr. 57a („skriptbasiert“ → „mit '
    'KI-generierten Skripten“)')
rep('(e) Marker und Platzhalter entfernen ([EXTRAPOLATION] in 4.4, alle ⟨…⟩)',
    '(e) verbliebene Marker und die Platzhalter in Anhang H entfernen (am 28.09. meldet das Messskript keinen Marker, der in 4.4 entfiel '
    'mit dem 20-m-Satz)')
rep('Umnummerierung 4 → 2 bis 7 → 5 per Skript in Master, Steuerdokumenten, Skripten und Textvorschlägen (G35 d, Gliederung v5 M25), danach F9.',
    'Umnummerierung 4 → 2 bis 7 → 5 per Skript in Master, Steuerdokumenten, Skripten und Textvorschlägen, vorher die Zeilen des Kopfblocks '
    'Einleitung im Berichtsraster auf das Präfix E umstellen (G35 d, Gliederung v5 M25), danach F9.')
rep('*Klickpunkte:* Ergebnis der Seitenmessung (Grenze 33, Tauschregel ab 32), Freigabe der Abgabe.',
    '*Klickpunkte:* Streichpaket Bootstrap, Nr. 57a, Ergebnis der Seitenmessung (Grenze 33, Tauschregel ab 32), Freigabe der Abgabe.')
# § 4 (Befund 15)
rep('Nr. 1 gilt für die Tasks 7 neu und 11 bis 13, Nr. 2 ist neu gefasst, Nr. 3 entfällt.', 'Nr. 1 und Nr. 2 sind neu gefasst, Nr. 3 entfällt.')
zeile('1. **Vormerkungen aus Kapitel 5 und 6 für Kapitel 4 und 2.**',
      '1. **Vormerkungen für Kapitel 4.** Beim Schreiben der Einleitung, der Ergebnisse und der Diskussion fallen erfahrungsgemäß '
      'Korrekturwünsche an die Methodik an (so wie G29 aus dem 4.7-Task). Sie werden in den Tasks 7 neu und 11 bis 13 gesammelt und in der '
      'Endredaktion (Task 18 a) in einem Durchgang eingearbeitet, nicht je Fund einzeln.')
rep('**Steuerung zuerst** (Task 1) bleibt: Jeder Task liest Fassung 14 zuerst.',
    '**Steuerung zuerst** (Task 1, am 28.09. Task 1b) bleibt. *Stand 25.09., historisch:* Jeder Task liest Fassung 14 zuerst.')
rep('Eine kurze Sitzung erspart Nacharbeit in allen folgenden.',
    'Eine kurze Sitzung erspart Nacharbeit in allen folgenden. Seit dem 28.09. liest jeder Task Fassung 17, sobald der Verfasser sie eingesetzt hat (A8).')
# § 7.1 (Befunde 12 und 37)
rep('| Formel „mindestens zwei, in der Regel zwei bis drei Minuten“ an einer Stelle | Task 2 |',
    '| Formel „mindestens zwei, in der Regel zwei bis drei Minuten“ an einer Stelle | **beantwortet 25.09. in Task 2:** Pausenregel beim '
    'Standweitsprung nur in 4.3 (F17 § 13 Nr. 17) |')
rep('| nicht aufnehmen, Definition nicht zurückholen | Task 2 |',
    '| nicht aufnehmen, Definition nicht zurückholen | **beantwortet 25.09. in Task 2:** keine Reifebänder, K11 geschlossen (F17 § 13 Nr. 18) |')
rep('| streichen, nicht am Verfassertext gemessen | Task 2 |',
    '| streichen, nicht am Verfassertext gemessen | **beantwortet 25.09. in Task 2:** gestrichen (F17 § 13 Nr. 18) |')
rep('| keine Kursivsetzung, Begriffe sind Fachsprache | Task 2, Umsetzung Task 18 |',
    '| keine Kursivsetzung, Begriffe sind Fachsprache | **beantwortet 25.09. in Task 2:** keine Kursivsetzung, Umsetzung in Task 18 '
    '(F17 § 13 Nr. 19) |')
rep('| wie § 5 | Task 6 |', '| wie § 5 | **erledigt 26.09. in Task 6:** Zielorte je verschobenem Satz im Textvorschlag 4.7 vom 26.09. (§ 2, § 7) |')
rep('der Name steht in der KI-Deklaration und in Anhang G (Textvorschlag 4.7, Nr. 57)',
    'der Name ist für die KI-Deklaration und Anhang G vorgemerkt (Textvorschlag 4.7, Nr. 57)')
# § 8 Startsätze (Befunde 1, 2, 15, 22, 23)
rep('Kennzahlenblatt 25.09. Rev. 2, Objekte_2026-09-25, Stilprofil, Skill. Textvorschlag 5.1 und 5.2 mit gemessenem Kopf und Kennungen im '
    'Begleitteil, Zweitprüfung durch Subagent, Klickfreigabe, Einbau per Skript mit Tab. 2 und Tab. 3, Endabgleich, Rev. Vormerkungen für '
    'Kapitel 4 und 2 sammeln, nicht einbauen.',
    'Kennzahlenblatt 25.09. Rev. 2, Objekte_2026-09-25, Textvorschlag 4.7 vom 26.09. § 7, Stilprofil, Skill. Nr. 23 per Klick zu Beginn. '
    'Textvorschlag 5.1 und 5.2 mit gemessenem Kopf und Kennungen im Begleitteil, Zweitprüfung durch Subagent, Klickfreigabe, Einbau per '
    'Skript (nur Text, keine Objekte und keine Platzhalter), Endabgleich, Rev. Vormerkungen für Kapitel 4 sammeln, nicht einbauen.')
rep('Kennzahlenblatt K-05 bis K-11, T1 und T4, die aus 4.7 verschobenen Sätze.',
    'Kennzahlenblatt K-05 bis K-11, T1 und T4, die aus 4.7 verschobenen Sätze, Textvorschlag 4.7 vom 26.09. § 7 und Textvorschlag '
    'Einleitung § 6 Nr. 7.')
rep('„Task Endredaktion nach Plan § 3 Task 18 (a) bis (i). Vormerkungen aus den Tasks 7 neu und 11 bis 13 als Vorschlagsliste, Objekte und '
    'Grafiken per Skript,',
    '„Task Endredaktion nach Plan § 3 Task 18 (a) bis (j). Vormerkungen aus den Tasks 7 neu und 11 bis 13 als Vorschlagsliste, Objekte des '
    'Textteils, Anhang H und Grafiken per Skript, Streichpaket Bootstrap und Nr. 57a per Klick,')
# Task 1b: Klicks K4 und K5 (28.09., 19:58)
rep('Fassung 17 wird wirksam, wenn der Verfasser sie einsetzt (A8).\n',
    'Fassung 17 wird wirksam, wenn der Verfasser sie einsetzt (A8). Klicks am Ende (19:58): K4 — 24 überholte Projektkopien gelöscht, '
    'deren Original im Ordner oder im Archiv liegt, fünf ohne auffindbares Original behalten · K5 — Fassung 17 freigegeben, Fassung 16 als '
    'Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` und in der Papierkorbliste des Aufräumskripts.\n')
# § 9
rep('Werte aus Messskript, Seitenmodell und Textvorschlag Einleitung per Skript `03_Skripte\\Plan_Rev5_2026-09-28.py`.\n',
    'Werte aus Messskript, Seitenmodell und Textvorschlag Einleitung per Skript `03_Skripte\\Plan_Rev5_2026-09-28.py`. Nach der '
    'übergreifenden Zweitprüfung (28.09., Fassung 3 des Erzeugers): Kopf mit Archivpfad · Nachtrag 28.09. mit Hinweis auf Rev. 5 · § 1 '
    'Objekte als historisch · § 2.1 Stand nach Task 6 ans Ende, Zielorte „vorgemerkt für“ · § 3 Vorspann auf F17 § 1.2 und Textvorschlag 4.7 '
    'vom 26.09. § 5 · Task 11 ohne Objekte und Platzhalter, Klickpunkt Nr. 23, ohne 48-h-Angabe · Task 12 Eingang mit Textvorschlag 4.7 § 7, '
    'Textvorschlag Einleitung § 6 Nr. 7, G32 (c), G33 (d) und (f), G34 (c), Verdünnungslogik in 6.1 und G3 (Klick 19:25) · Task 15 RC 2020 · '
    'Task 16 Folge der Klickfrage 12, kein Erratum (Klick 19:25) · Task 18 (b) mit den Objekten des Textteils, Tab. H6 ohne R1, R9, R10, R12, '
    'R13 und R14, Streichpaket Bootstrap und Nr. 57a, (e), (j) · § 4 Nr. 1 und Steuerung zuerst · § 7.1 Nr. 5 bis 9 und 14 · § 8 Startsätze '
    'Task 11, 12 und 18.\n')

text = re.sub(r'\n{3,}', '\n\n', t)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('Plan Rev. 5 geschrieben: %d Zeichen, %d Ersetzungen' % (len(text), len(LOG)))

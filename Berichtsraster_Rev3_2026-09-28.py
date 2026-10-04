# -*- coding: utf-8 -*-
"""
Berichtsraster_Rev3_2026-09-28.py — Berichtsraster `02_Befunde\\Berichtsraster_2026-09-23.md` Rev. 2 → Rev. 3
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task Steuerdokumente 28.09. (Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 5.2)

Inhalt: Kopfblock „Einleitung“ statt § 3.1 bis § 3.3 (Zeilen behalten ihre Nummern, neu E.1 und E.2) · § 2.1, § 2.4, § 3.0 ·
Nachträge I19 (4.2.5, § 3.11) · G32 (j): 4.1.10, 4.7.3, 4.7.5 bis 4.7.15, 6.2.1 nach Textvorschlag 4.7 § 3 und § 7 · 6.1.1 (K6) ·
7.4 (G34 b) · § 5 Zeilen 17 und 18 · § 7 Nr. 1, 10, 14 · § 8 historisch · neuer § 11. Ist-Spalten werden nicht fortgeschrieben.
Jede Ersetzung genau einmal, sonst Abbruch. Wortzahl von 4.7 aus dem Messskript Fassung 3.
Aufruf: python Berichtsraster_Rev3_2026-09-28.py <Raster_Rev2.md> <Manuskriptstand.csv> <Ausgabe.md>
Ohne Semikolon im Skript (chr(59)). Fassung 2 (28.09.): Budgets der Kopfblöcke 4.1 bis 6 nach Fassung 17 § 5.2
(bis Rev. 2 standen dort die Vorschläge aus § 8), Lesehinweis § 3 und Herkunftsvermerk im Kopf.
Fassung 3 (28.09., nach der übergreifenden Zweitprüfung der Steuerdokumente): Zahlenquelle und Kennungen vom 25.09.,
Tab. 2 ohne Kennwerte, 20-m-Zwischenzeit in Tab. H6 und 6.3, 48-h-Angabe als Tatsache in 4.3, 4.3-Zeilen nach Fassung 17 § 13
Nr. 17, 6.2.11 und 6.2.12, G2 in beide Richtungen, G8-Wortlaut, Einleitung endet mit den Hypothesen, „vorgemerkt“ statt „steht“,
Verdünnungslogik in 6.1 und Limitation in 6.3 (Klick 19:25), Semikola in geänderten Kopfblöcken ersetzt, Zeile 3.5 der Einleitung mit Zug- und Satzangaben nach der Zug-Tabelle des Textvorschlags.
"""
import csv
import sys

SRC, M_CSV, OUT = sys.argv[1:4]
SEMI = chr(59)
t = open(SRC, encoding='utf-8').read()
LOG = []
w47 = [int(r['woerter']) for r in csv.DictReader(open(M_CSV, encoding='utf-8')) if r['arbeitsnummer'] == '4.7'][0]


def rep(alt, neu):
    global t
    n = t.count(alt)
    if n != 1:
        raise SystemExit('Abbruch: %d Treffer statt 1 für: %s' % (n, alt[:100]))
    t = t.replace(alt, neu)
    LOG.append(alt[:70].replace('\n', ' '))


def zeile(praefix, neu):
    global t
    zl = t.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('Abbruch: %d Zeilen beginnen mit: %s' % (len(idx), praefix))
    zl[idx[0]] = neu
    t = '\n'.join(zl)
    LOG.append('Zeile ' + praefix[:60])


def abschnitt(von, bis, neu):
    global t
    zl = t.split('\n')
    i0 = [i for i, z in enumerate(zl) if z.startswith(von)]
    i1 = [i for i, z in enumerate(zl) if z.startswith(bis)]
    if len(i0) != 1 or len(i1) != 1 or i1[0] <= i0[0]:
        raise SystemExit('Abbruch: Abschnitt %s bis %s nicht eindeutig' % (von, bis))
    zl = zl[:i0[0]] + neu.rstrip('\n').split('\n') + [''] + zl[i1[0]:]
    t = '\n'.join(zl)
    LOG.append('Abschnitt ' + von[:60])


# ------------------------------------------------------------------ Kopf
rep('fortgeschrieben 24.09.2026 (Rev. 2)**', 'fortgeschrieben 24.09.2026 (Rev. 2) und 28.09.2026 (Rev. 3)**')
rep('> **Rev. 2 vom 24.09.2026:**',
    '> **Rev. 3 vom 28.09.2026 (Task Steuerdokumente, Projektanweisungen Fassung 17):** Kapitel 1 bis 3 werden eine Einleitung '
    '(Verfasser 28.09., 14:38, Klick 14:57). § 3.1 bis § 3.3 der Rev. 2 sind zu einem Kopfblock „Einleitung“ zusammengeführt (§ 3.1), die Zeilen '
    'behalten ihre Nummern, neu sind E.1 und E.2. Umfang 6.350 Wörter und höchstens 33 Seiten einschließlich Literaturverzeichnis. '
    'Zeilen zu 4.7 nach dem Wortlaut im Master vom 26.09. (Textvorschlag 4.7 § 3 und § 7), Nachträge I19 (4.2.5, § 3.11). Verweise '
    '„F14 §“ gelten für Fassung 17 mit gleicher Nummer, wo nicht anders vermerkt. Die Ist-Spalten stehen weiter auf dem Master vom '
    '22.09. und werden nicht fortgeschrieben, maßgeblich ist das Messskript. Für 4.7 nennen die Zeilen den Ort im Master vom 26.09. '
    'Die Zeilenkennungen der Einleitung (1.1 bis 3.5, E.1, E.2) sind keine Abschnittsnummern, sie werden in Task 18 mit umbenannt '
    '(Gliederung v5). Liste in § 11.\n\n> **Rev. 2 vom 24.09.2026:**')
rep('Zahl = Kennzahlen_2026-09-22.', 'Zahl = Kennzahlen_2026-09-25 (Rev. 2, seit Rev. 3 dieses Rasters).')

# ------------------------------------------------------------------ § 2.1 und § 2.4
zeile('| 2a |', '| 2a | Wissenschaftlicher Hintergrund und Begründung der Studie | Einleitung (1), Züge 1 bis 7 (§ 3.1) | P | '
      'Stand 28.09.: Textvorschlag Einleitung, Altbestand bis zur Übertragung |')
zeile('| 2b |', '| 2b | Genaue Fragestellung und Hypothesen | Einleitung (1), Zug 8: Zweck, Fragestellung, H0/H1 (§ 3.1) | P | '
      'Stand 28.09.: Textvorschlag Einleitung, Absatz 9 |')
zeile('| Grundlagen |', '| Grundlagen | begriffliche und theoretische Grundlagen, „nur die wirklich themenrelevanten“, Warnung vor '
      'Grundlagen-Überdehnung („extrem negativ auf die Bewertung“) | Einleitung (1), Züge 2 bis 5, kein eigenes Kapitel (Verfasser 28.09.) |')
zeile('| Forschungsstand |', '| Forschungsstand | eigenes Kapitel: wer hat sich wie derselben Frage gewidmet, mit welchem Ergebnis, '
      'kritische Bewertung, Schlussfolgerungen für das eigene Vorgehen | Einleitung (1), Züge 6 und 7. Abweichung: kein eigenes Kapitel, '
      'SMK Abschn. 4.1 bewusst nicht erfüllt (Verfasser 28.09., 14:38, Klick 14:57) |')
zeile('| Umfang |', '| Umfang | „30 bis 50 Textseiten nicht überschreiten“ (§ 15) · Verfasser höchstens 33 Seiten einschließlich '
      'Literaturverzeichnis, Einleitung bis Ende des Verzeichnisses (28.09., Klick K1) · Betreuer mündlich ≤ 37 · Steuerung 6.350 Wörter '
      '(Fassung 17 § 1.1) | — |')

# ------------------------------------------------------------------ § 3.0
rep('Budget: außerhalb der 9.000 (Zusammenfassung und Abstract je 200–300 Wörter, F14 § 10)',
    'Budget: außerhalb der 6.350 und außerhalb der Seitengrenze (Zusammenfassung und Abstract je 200–300 Wörter, Fassung 17 § 10, K1)')

# ------------------------------------------------------------------ § 3.1 Kopfblock Einleitung
EINL = '''### 3.1 Einleitung (Kapitel 1, Arbeits- und Endnummer 1) — ersetzt § 3.1 bis § 3.3 der Rev. 2

**Kopfblock.** Budget 1.500, kein Unterbudget (Fassung 17 § 5.2) · Bauplan § 2.1: Trichter in acht Zügen nach Übergabe Einleitung § 3, umgesetzt im Textvorschlag Einleitung (Zug-Tabelle § 2 dort), Schluss mit den Hypothesen, nie mit einem Literaturverweis · Auswertungsplan § 5.2 A3 (Hypothesen nah am Antragswortlaut, keine primäre Zielgröße) · Zahlen: keine Studienzahlen. Die Zeilen behalten ihre Nummern aus Rev. 2: 1.1 bis 1.6 aus Kapitel 1, 2.1 bis 2.5 als Rollen aus Kapitel 2, 3.1 bis 3.5 aus Kapitel 3. Neu sind E.1 und E.2. Doppelungen stehen als Querverweis in der Zeile. Ist = Textvorschlag Einleitung vom 28.09. (Absatz A1 bis A9), die Übertragung in den Master steht aus.

| Nr. | Soll-Inhalt | Anspruch | Et. | Ist 28.09. |
|---|---|---|---|---|
| 1.1 | Relevanz: Sprint, Richtungswechsel, Sprungkraft als leistungsbestimmend im Nachwuchsfußball (generalisierende Präsensaussage, Beleg am Satzende) | SMK 4.1 „Relevanz“ · CONSORT 2a | P | Zug 1, A1 |
| 1.2 | Gegenstand und Problem: Sommerpause als Zeitfenster mit wenig oder keinem Mannschaftstraining, Detraining mit offener Richtung bei Heranwachsenden, gerätefreies Heimprogramm als Antwort, Mechanismus nur angedeutet | SMK 4.1 „Gegenstand, Problemstellung“ · CONSORT 2a | P | Züge 3 und 4, A4 bis A6 |
| 1.3 | Forschungsstand knapp und Lücke als Kombination: kontrollierte Studien zu einem unbeaufsichtigten, videobasierten, gerätefreien Heimprogramm in der Sommerpause für Spieler des leistungsorientierten Breitensports um den Wachstumsgipfel fehlen (Fassung 17 § 6.5). Querverweis 3.1 | SMK 4.1 „Forschungsstand (hier knapp)“ · CONSORT 2a | P (Inhalt der Lücke: E) | Züge 6 und 7, A8 |
| 1.4 | Zweck in einem Satz, der Ankersatz. Er kehrt im Eröffnungsabsatz von 6.1 und in der Zusammenfassung nahezu wörtlich wieder, 4.1 bleibt ohne Zwecksatz (Klick K6, 28.09.). Wortlaut entschieden: „… gegenüber einer Kontrollgruppe verbessert“ (Klick in Task 7 neu) | CONSORT 2b · SMK 4.1 „Ziel und Erkenntnisinteresse“ | P | Zug 8, A9 |
| 1.5 | Fragestellung, getragen vom Zwecksatz. Querverweis 3.2 | CONSORT 2b | P | A9 |
| 1.6 | Ein Satz zur methodischen Vorgehensweise (quasi-experimentelle, kontrollierte Feldstudie mit Prä-Post-Diagnostik), ohne Kapitelverweis | SMK 4.1 „methodische Vorgehensweise bzw. Aufbau der Arbeit“ | P | A9 |
| 2.1 | Rolle Plyometrie: Dehnungs-Verkürzungs-Zyklus, Steuergrößen, gerätefrei und heimtauglich. Nicht hinein: Effektstärken, Mechanismusdetails (4.5.1), Funktionsanatomie | SMK 4.1 Grundlagen · CONSORT 2a | E | Zug 4, A5 |
| 2.2 | Rolle Reifung: Moderator der Trainingsantwort, Richtung uneinheitlich. Nicht hinein: Methodenwahl beim Reifestatus (vorgemerkt für 6.2, Klick in Task 7 neu), Kovariatenbegründung (4.7) | SMK 4.1 · CONSORT 2a | E | Zug 5, A7 |
| 2.3 | Rolle Sommerpause und Detraining als Kontext. Nicht hinein: Einzelwerte (bei Bedarf 6.1), Rahmenterminplan und Ferienordnung | SMK 4.1 · CONSORT 2a | E | Zug 3, A4 |
| 2.4 | Rolle Zielgrößen und Diagnostik, aus den Anforderungen des Wettkampfs abgeleitet (E.2). Nicht hinein: eigener Testaufbau (4.3, 4.4) | SMK 4.1 · CONSORT 2a | E | Zug 2, A2 und A3 |
| 2.5 | Rolle Forschungsstand: qualitativ, mit Gegenbefund (kurze Beschleunigung als Vorab-Erwartung für 5 und 10 m), Effektstärken nicht Pflicht | SMK 4.1 Forschungsstand · CONSORT 2a | E | Zug 6, A8 |
| 3.1 | Lücke aus dem Forschungsstand gezogen. Querverweis 1.3 | SMK 4.1 (Schlussfolgerungen aus dem Forschungsstand) | P | Zug 7, A8 |
| 3.2 | Fragestellung. Querverweis 1.5 | CONSORT 2b | P | A9 |
| 3.3 | H0 und H1 nah am Wortlaut des Ethikantrags („… in mindestens einem der erhobenen Parameter“), einander ergänzend, auf die Grundgesamtheit bezogen (G32 e) | CONSORT 2b · Antrag (Leitregel) | P/E | A9 |
| 3.4 | Keine primäre Zielgröße, als „gleichrangig“ benannt, nicht nachträglich gesetzt | Antrag · Fröhlich S. 95 | E | A9 |
| 3.5 | Feste Reihenfolge Sprint → Richtungswechsel → Sprung (identisch in 5 und 6) | Fassung 17 § 5.1 | E | Züge 6 und 8, A8 S1 und S4, A9 S1 und S3 |
| E.1 | Präventionssätze: Programmklasse, nicht das eigene Programm · Olivier et al. (2026) mit Quellenart und Population, ohne Zahl · Rössler et al. (2014) als Zwischen-Studien-Vergleich, „überwiegend Spielerinnen“, Vor-2020-Halbsatz | Befund Relevanz Rev. 2 § 4.3 · Klick 14:36 | E | Zug 4, A6 |
| E.2 | Zweck des Zielgrößenzugs: aus den physiologischen Anforderungen des Wettkampfs die Zielgrößen und ihre Diagnostik ableiten, kein Testablauf | Verfasser 28.09., 10:30 | E | Zug 2, A2 und A3 |

**Nicht hier:** eigene Studienzahlen · Methodendetails und Testabläufe · Ergebnisandeutungen · Aufbau-der-Arbeit-Absatz und Kapitelverweise (Verweisverbot 22.09.) · Literaturverweis als Schlusssatz · mehr als drei Quellen je Klammer · Präventionsaussagen über das eigene Programm und die übrigen Ausschlüsse aus Befund Relevanz Rev. 2 § 4.4 (Fassung 17 § 11.2b).

**Prüfvermerke.** SMK Abschn. 4.1 verlangt den Forschungsstand in einem eigenen Kapitel. Die Vorgabe ist bewusst nicht erfüllt (Verfasser 28.09., 14:38, Klick 14:57). CONSORT 2a und 2b liegen vollständig in der Einleitung. § 3.2 und § 3.3 der Rev. 2 sind in diesem Kopfblock aufgegangen, die Nummern der folgenden Paragrafen bleiben.
'''
abschnitt('### 3.1 Kapitel 1 — Einleitung', '### 3.4 Abschnitt 4.1 — Studiendesign', EINL)

# ------------------------------------------------------------------ 4.1.10 und 4.2.5 (I19)
zeile('| 4.1.10 |', '| 4.1.10 | Kurzregister der Änderungen gegenüber dem Antrag, jede mit Grund: Vereinswechsel (SC West ohne Rückmeldung, '
      'Hohenlind nach Antragstellung, Verein C Kontroll- statt Interventionsgruppe) · geplante Fallzahl etwa 45 nicht erreicht (ohne Zahl) · '
      'Termine teils außerhalb des Fensters · Vereinsprogramme statt trainingsfreier Ferien · Zweitvereinskriterium nicht erhoben ⟨Grund⟩ · '
      'Adhärenzkriterium in der Hauptanalyse nicht angewandt (Grund in 4.7, Datum in Tab. H6). Messaufbau → 4.4, Programm → 4.5.1 · '
      'Vollregister → Tab. H6, Erstverweis in 4.1 (Task 18) | CONSORT 3b · F14 § 5.3 | P | ~ (Zweitverein fehlt, G23 Nr. 2, Abs. 5 ohne '
      'Schlusspunkt, „N = 31 statt …“ entfällt, Rev. 69) |')
zeile('| 4.2.5 |', '| 4.2.5 | Kennwerte je Gruppe (Alter, Körperhöhe, Körpermasse, %PAH, M ± SD) der Analysepopulation (Menge ANA) stehen im '
      'Text von 4.2, Tab. 2 führt nur die Ausgangswerte der Zielgrößen (Verfasser 25.09., Fassung 17 § 5.3, Nachtrag I19) | CONSORT 15 '
      '(demografischer Teil) · Umfangsdokument § 3.2, § 9 | P | ✓ (K-02b im Master, Stand 26.09.) |')

# ------------------------------------------------------------------ § 3.11 Kopfblock (I19) und Zeilen 4.7 (G32 j)
zeile('**Kopfblock.** Budget 550 (F14 § 5.2)',
      '**Kopfblock.** Budget 550, bleibt nach Vorgabe (Fassung 17 § 5.2), Stand nach dem Messskript Fassung 3: %d Wörter (28.09.) · '
      'Bauplan § 2.2 Statistikabsatz mit den bewussten Abweichungen von 4.7 nach Fassung 17 § 5a: keine Darstellungskonvention im Text, '
      'Voraussetzungen nach dem Modell, Effektstärke ohne Schwellen, Software nicht als letztes Wort · Auswertungsplan § 5.2 (A1–A3), § 5.3, '
      '§ 5.6, § 5.9, § 5.10 (nachträgliche Festlegungen) · Spezifikation Teil F · Voraussetzungsprüfungen § 5.3 · Fassung 17 § 11 · Zahlen: '
      'Kennzahlenblatt vom 25.09. (Nenner, MDES) · Wortlaut im Master seit 26.09. nach Textvorschlag 4.7 (Fassung 13 mit Nachtrag Schritt 0), '
      'sechs Absätze: Analysepopulation · Fallzahl · Kovarianzanalyse · Voraussetzungen · Sensitivität · Datenprüfung und Software.' % w47)
Z47 = {
    '4.7.3': '| 4.7.3 | Ausschlussklassen nach Box 6 als Regel, ohne Codes: fehlender Post-Wert oder Reifestatus, Adhärenz kein Ausschlussgrund, '
             'das Antragskriterium entfällt als Ausschlussgrund. Ort im Master (26.09.): Abs. 1. Zielort der Klassen mit Zahlen: Abb. 1 (5.1). '
             'Der Instrumentenfehler ist für die Ergebnisanalyse gegenstandslos (Textvorschlag 4.7 § 3) | CONSORT 16 · F14 § 11.7 | P/E | n/a |',
    '4.7.5': '| 4.7.5 | Kovariaten vorab festgelegt und prognostisch begründet, ausdrücklich nicht abhängig von der Signifikanz eines '
             'Baseline-Unterschieds, beim Reifestatus verstärkt durch das Ungleichgewicht der Gruppen (Textvorschlag 4.7, Nr. 46). Keine '
             'Signifikanztests auf Ausgangswerte und kein Hinweis auf nicht gerechnete Tests (Verfasser 26.09.). Ort im Master: Abs. 3 und 4.1 '
             '(„Vorab festgelegte Kovariaten“). Zielort: d und Überlappung in Tab. 2 mit Anmerkung (Nr. 43) | CONSORT 12b · E&E 15 | P | n/a |',
    '4.7.6': '| 4.7.6 | Deskriptiv statt konfirmatorisch: 5 m, 10 m, 505 links und rechts. Grund: Fallzahluntergrenze acht je Gruppe und '
             'Messausfall. Antragskriterium ≥ 75 % nur deskriptiv (n = 3). Ort im Master: Abs. 1. Das Datum der Festlegung steht in Tab. H6, '
             '4.7 nennt die Reihenfolge ohne Datum (Verfasser 26.09., 20:51) | CONSORT 6b/12a · F14 § 11.9 · Auswertungsplan § 5.3 | P/E | n/a |',
    '4.7.7': '| 4.7.7 | Änderung gegenüber dem Antrag mit Grund: Adhärenzkriterium nicht als Ausschluss angewandt, Hauptanalyse alle '
             'Zugeteilten. Per-Protokoll ≥ 6 von 12 als beobachtender Zusatz (Konvention „Hälfte des Programms“, nach Sichtung der '
             'IG-Post-Werte und vor der Abschlusstestung der KG, so benennen). Ort im Master: Abs. 1. Datum je Festlegung → Tab. H6 '
             '(Verfasser 26.09., 20:51) | CONSORT 3b · Auswertungsplan § 5.3 | P | n/a |',
    '4.7.8': '| 4.7.8 | Fallzahl: A-priori-Poweranalyse des Antrags als Planungsstand (f = 0,25, mindestens 34 Spieler), begrenzt durch '
             'verfügbare Spieler und Testzeit (Ressourcenbegründung, Lakens 2022). Sensitivitäts-Poweranalyse nach dem Standardweg (O9) für '
             'die erreichte Spielerzahl je Zielgröße mit α und Power, Rechenweg „konservativ“ als nachträglich (R3). Keine Post-hoc-Power. '
             'Ort im Master: Abs. 2, Software Abs. 6. Zielorte: Planungsmodell der Antragsrechnung und keine Post-hoc-Power → 6.2 (6.2.1), '
             'Testfamilie, Zähler-df, Gruppen, Kovariaten, n je Zielgröße sowie α und Power der A-priori-Rechnung → Anhang G (Task 16) | '
             'CONSORT 7a · Moher E&E 7a · Auswertungsplan § 5.10 R3 | P | n/a |',
    '4.7.9': '| 4.7.9 | Effektstärke Hedges\' g = adjustierte Differenz / gepoolte Prä-SD × J, KI aus dem KI der Differenz. Kein partielles '
             'η² (K24). Ort im Master: Abs. 3 (Maß, gepoolter Nenner, Grund). Zielort: J mit df und die Herleitung des KI in der Anmerkung '
             'zu Tab. 3 (Textvorschlag 4.7, Nr. 44 und 48) | CONSORT 17a (Präzision) · Antrag („Cohens d bzw. Hedges\' g“) | P/E | n/a |',
    '4.7.10': '| 4.7.10 | Unadjustierte Differenz wird neben der adjustierten berichtet. Ort im Master: Abs. 3, Grund über das Ungleichgewicht '
              '(Textvorschlag 4.7, Nr. 47). Zielort: Spalte in Tab. 3 | CONSORT 18 · E&E 18 | P | n/a |',
    '4.7.11': '| 4.7.11 | Sensitivitätsanalysen, vorab festgelegt, in einem Satz mit Verweis auf Tab. H4. Bootstrap-KI der adjustierten '
              'Differenz für alle drei Zielgrößen als nachträglich festgelegte Zusatzsensitivität kennzeichnen (O8, N3), als streichbares '
              'Modul geführt (Verfasser 26.09., 18:16). Ort im Master: Abs. 5. Zielorte: Namen der Varianten in Tab. H4c mit Anmerkung, '
              'Konfundierung der Familiarisierung mit Verein A → 6.3 G7, Anlass und Datum des Bootstraps → Tab. H6 | CONSORT 12b, 18 '
              '(„präspezifiziert oder exploratorisch“) · Auswertungsplan § 5.10 R5 | P | n/a |',
    '4.7.12': '| 4.7.12 | Voraussetzungen an den Modellresiduen: Shapiro-Wilk, Brown-Forsythe, Linearität und Steigungen über Residuengrafiken '
              'und je einen Interaktionsterm mit der Gruppe, Überlappung der Kovariaten beschrieben. Regel O7 mit Grund: Eine verworfene '
              'Prüfung wird berichtet, das Modell bleibt. Im Text ohne Beleg für Prüfpflicht und Tests (Textvorschlag 4.7, Nr. 56), '
              'Originale nach H8 optional. Ort im Master: Abs. 4. Zielorte: Q-Q-Diagramm → Anhang G, Residuen-SD je Gruppe → Tab. H4b, '
              '„geprüft und nicht verworfen“ und verworfene Prüfungen mit Prüfgröße → 5.2 (R2), Trennschärfe → 6.2 (6.2.10) | CONSORT 12a · '
              'Voraussetzungsprüfungen § 5.3 (Leppink 2018, Shapiro & Wilk 1965, Brown & Forsythe 1974, Rochon et al. 2012) | P/E | n/a |',
    '4.7.13': '| 4.7.13 | Datenprüfung: digitalisierte Werte auf Plausibilität geprüft, auffällige am Papierprotokoll kontrolliert. Ort im '
              'Master: Abs. 6. Nach Verfasserentscheidung (Textvorschlag 4.7, Nr. 57): die Freigabe ohne unabhängige Methodenprüfung genau '
              'einmal → 6.3, KI-Nutzung → KI-Deklaration und Anhang G, Datenstand, Spezifikation, Gegenproben und Abgleich werden in 4.7 '
              'nicht berichtet, Anhang G ohne Prüfprotokolle. (Bis Rev. 1 stand hier TE/√n gegen SESOI, bis Rev. 2 die Rechenprüfung mit '
              'Ergebnis) | Auswertungsverfahren 8.1 · SMK 4.1 | E | n/a |',
    '4.7.14': '| 4.7.14 | Mehrfachtestung: keine Adjustierung, keine nachträgliche primäre Zielgröße, laut Studienprotokoll drei gleichrangige '
              'Zielgrößen. Ort im Master: Abs. 3. Der Familienfehler der „mindestens einer“-Hypothese (höchstens 7,5 %, Textvorschlag 4.7 '
              'B15) ist für 6.2 vorgemerkt (6.2.2) | F14 § 11.4 · CONSORT 20 (Multiplizität, Ort 6.2) | E | n/a |',
    '4.7.15': '| 4.7.15 | α = 0,05 zweiseitig, exakte p-Werte, 95-%-KI. Software R 4.3.3, die Paketangabe ist gegenstandslos (ohne '
              'Zusatzpakete), Skripte in Anhang G. Die Software ist nicht mehr das letzte Wort des Abschnitts (Textvorschlag 4.7, Nr. 57). '
              'Ort im Master: Abs. 3 und Abs. 6. Zielort: exakte p-Werte als Darstellungsregel in der Anmerkung zu Tab. 3 (Nr. 41) | '
              'CONSORT 12a · Korpus 10/13 · Auswertungsverfahren 8.1 | P/K | n/a |',
}
for nr, neu in Z47.items():
    zeile('| %s |' % nr, neu)

# ------------------------------------------------------------------ Kapitel 6 und 7
rep('| 6.1.1 | Zweck wiederholen →', '| 6.1.1 | Zweck wiederholen (Ankersatz aus der Einleitung, nahezu wörtlich, Klick K6) →')
rep('— der Nullbefund als Aussage über das Auflösungsvermögen | CONSORT 20 („fehlende Präzision")',
    '— der Nullbefund als Aussage über das Auflösungsvermögen · Planungsmodell der Antragsrechnung: n = 34 passt nicht zum Gruppenterm '
    'der Kovarianzanalyse (Cohen, 1988, Tab. 8.4.4), wohl aber zur Wechselwirkung im Messwiederholungsdesign mit den Voreinstellungen '
    'von G*Power (Modellrechnung, L14 a, Textvorschlag 4.7, Nr. 7) · Power-Werte mit dem Hinweis, dass keine nachträgliche Power '
    'gerechnet wurde (Nr. 26) | CONSORT 20 („fehlende Präzision")')
rep('Auslieferung und Monitoring unbeaufsichtigter Programme, Versuchszahl an der Gruppengröße ausrichten |',
    'Auslieferung und Monitoring unbeaufsichtigter Programme, Versuchszahl an der Gruppengröße ausrichten, zwei Satzteile im Ausblick '
    '(Verletzungen als Endpunkt, Umsetzung als Hypothese), ohne Quelle (Befund Relevanz Rev. 2, G34 b) |')

# ------------------------------------------------------------------ § 5, § 7, § 8
zeile('| 17 | 2.4.1 |', '| 17 | 2.4.1 | „die 10- und die 30-m-Zeit die konfirmatorischen Sprintmaße“ | 10 m deskriptiv (IG-Set 7) · entfällt '
      'mit der Einleitung (Gliederung v5, M24) | W14 |')
zeile('| 18 | 2.4.2, 2.2 |', '| 18 | 2.4.2, 2.2 | „seitengetrennt ausgewertet“, „(Abschnitt 4.2)“ zweimal für %PAH und Tier 2 | Seitenmittel, '
      'Verweise entfallen · entfällt mit der Einleitung (Gliederung v5, M24) | W16, G19c |')
zeile('1. Absatztext Kapitel 1 bis 7 gemessen:', '1. Absatztext der Kapitel 1 bis 5 (Arbeitsnummern 1 und 4 bis 7) gemessen: ≤ 6.350 (Fassung 17 '
      '§ 1.1) · Seitenzahl in Word ≤ 33 nach der Zählweise aus K1 (Einleitung bis Ende des Literaturverzeichnisses, ohne Vorspann und '
      'Anhang) · R6 entfällt (K2), nie Fließtext auffüllen.')
zeile('10. Abweichungsregister:', '10. Abweichungsregister: Kurzform 4.1, Messaufbau 4.4, Programm 4.5.1, Adhärenzkriterium 4.7, Limitation 6.3, '
      'Vollregister Tab. H6 mit Erstverweis in 4.1 (Task 18).')
zeile('14. KI-Deklaration', '14. KI-Deklaration im Wortlaut der DSHS-Richtlinie mit dem Mindestinhalt nach Fassung 17 § 14. Anhang G ohne '
      'Prüfprotokolle, jedes Skript als KI-erzeugt gekennzeichnet.')
rep('## 8 Vorschlag: Aufteilung des Kapitel-4-Budgets (G16d) und der Kapitel 5 und 6\n\n',
    '## 8 Vorschlag: Aufteilung des Kapitel-4-Budgets (G16d) und der Kapitel 5 und 6\n\n**Historisch (Stand 23.09.).** Die Budgets gelten '
    'nach Fassung 17 § 5.2 (Unterbudgets als Vorgabe seit 25.09., Kapitelbudgets nach dem Neuzuschnitt vom 28.09.).\n\n')

# ------------------------------------------------------------------ Kopfblöcke: Budgets nach Fassung 17 § 5.2 (Fassung 2)
rep('§ 2 (Wortbudget 11.000) ist durch F14 § 5.2 (9.000) ersetzt.',
    '§ 2 (Wortbudget 11.000) ist durch F14 § 5.2 (9.000) ersetzt, seit Fassung 17 gilt 6.350.')
rep('**Kopfblock** (Budget F14 § 5.2 ·', '**Kopfblock** (Budget Fassung 17 § 5.2 ·')
rep('**Kopfblock.** Budget 300 (Vorschlag Übergabe 22.09., Klickfrage) ·', '**Kopfblock.** Budget 300 (Vorgabe nach Fassung 17 § 5.2) ·')
rep('**Kopfblock.** Budget 215 (Ist nach Rev. 12/13' + SEMI + ' Vorschlag § 8) ·', '**Kopfblock.** Budget 215 (Vorgabe nach Fassung 17 § 5.2) ·')
rep('**Kopfblock.** Budget ≈ 330 (Vorschlag § 8' + SEMI + ' Übergabe 4.3 Nachtrag: ≈ 340) ·',
    '**Kopfblock.** Budget 340 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 330) ·')
rep('**Kopfblock.** Budget ≈ 560 ohne Tab. 1 (Vorschlag § 8) ·',
    '**Kopfblock.** Budget 420 mit 4.4.1 bis 4.4.3, ohne Tab. 1 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 560) ·')
rep('**Kopfblock.** Budget ≈ 300 (Vorschlag § 8) ·', '**Kopfblock.** Budget 420 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 300) ·')
rep('**Kopfblock.** Budget ≈ 130 (Vorschlag § 8) ·', '**Kopfblock.** Budget 150 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 130) ·')
rep('**Kopfblock.** Budget ≈ 165 (Ist 175' + SEMI + ' Vorschlag § 8) ·', '**Kopfblock.** Budget 155 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 165) ·')
rep('**Kopfblock.** Budget ≈ 250 von 450 (Vorschlag § 8' + SEMI + ' v4 § 3.4: 230) ·',
    '**Kopfblock.** Budget 230 von 450 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 250) ·')
rep('**Kopfblock.** Budget ≈ 200 von 450 (v4 § 3.4: 220) ·', '**Kopfblock.** Budget 220 von 450 (Vorgabe nach Fassung 17 § 5.2, bis Rev. 2 Vorschlag ≈ 200) ·')
rep('**Kopfblock.** Budget 1.600 gesamt nach Gliederung v4 (Klick 5):',
    '**Kopfblock.** Budget 1.600 gesamt nach Fassung 17 § 5.2 (Unterbudgets seit Gliederung v4, Klick 5):')

# ------------------------------------------------------------------ Verweise ohne Dokumentnamen im Altbestand (Fassung 2)
rep('(keine LOCF, § 11.7)', '(keine LOCF, Fassung 17 § 11.7)')
rep('die Volltexte liegen nicht im Ordner (§ 7.1)', 'die Volltexte liegen nicht im Ordner (F14 § 7.1)')

# ------------------------------------------------------------------ Fassung 3: übergreifende Zweitprüfung (Befunde 6 bis 12, 18, 22, 33 bis 35)
# Befund 6: Zahlenquelle und Kennungen vom 25.09.
rep('**Zahlen:** ausschließlich Kennzahlenblatt 2026-09-22 (Rev. 4) und Analyseprotokoll 2026-09-15' + SEMI + ' hier stehen sie nur mit Kennung.',
    '**Zahlen:** ausschließlich Kennzahlenblatt 2026-09-25 (Rev. 2), hier stehen sie nur mit Kennung (seit Rev. 3). Die Ist-Spalten tragen den Stand vom 22.09. und werden nicht fortgeschrieben, maßgeblich ist das Messskript.')
rep('Reliabilitätskennwert' + SEMI + ' Aggregation im Testabsatz, nie im Statistikteil' + SEMI + ' Padrón-Cabo als Vorlage · Auswertungsplan § 5.4 Nr. 1, 2, 7, 9 und § 5.7 (20 m), § 5.9 (505-Regel) · Zahlen: K-04, K-05.',
    'Reliabilitätskennwert · Aggregation im Testabsatz, nie im Statistikteil · Padrón-Cabo als Vorlage · Auswertungsplan § 5.4 Nr. 1, 2, 7, 9 und § 5.7 (20 m), § 5.9 (505-Regel) · Zahlen: K-05, K-11.')
rep('| P/E | ✓ Inhalt (K-04) · ✗ Zahlen noch im Fließtext (M19) |', '| P/E | ✓ Inhalt (K-11), Zahlen nicht im Fließtext (M19 erledigt) |')
rep('Orientierungszug führt alle Objekte ein (Abb. 1, Tab. 2, Tab. 3), Objektverweis als Satzsubjekt im Präsens' + SEMI + ' kein Beleg, keine Deutung, Zahlen in den Objekten · Auswertungsplan § 5.4 Nr. 3 (Rekrutierung), Analyseprotokoll § 2 · Zahlen: K-01 (Fluss), K-06/K-07 (Tab. 2 auf den ITT-Sets), K-04.8 (Versuche post), F1-Befund (Adhärenz, Schmerzmeldungen).',
    'Orientierungszug führt seine Objekte ein (Abb. 1, Tab. 2, Erstverweise auf Tab. H1, H2 und H5), Objektverweis als Satzsubjekt im Präsens · kein Beleg, keine Deutung, Zahlen in den Objekten · Auswertungsplan § 5.4 Nr. 3 (Rekrutierung) · Zahlen: K-01 (Fluss), K-04 (Tab. 2), K-05 (TE post), K-10 (Umsetzung, CR-10, Load, unerwünschte Ereignisse), K-11 (Versuche).')
rep('| 6.1.3 | Verdünnungslogik: bei 42,6 % Umsetzung ist der ITT-Befund ein Befund über das Angebot, nicht über das Training (Sprachregelung) | F14 § 11.7 |',
    '| 6.1.3 | Verdünnungslogik: bei der Umsetzungsrate nach K-10.5 ist der ITT-Befund ein Befund über das Angebot, nicht über das Training (Sprachregelung). Ort 6.1, als Limitation 6.3 G3, 6.2 ohne eigenen Absatz (Klick 28.09., 19:25) | Fassung 17 § 11.7 |')
# Befund 7: Tab. 2 ohne Kennwerte
rep('Tab. 2 Stichprobe und Ausgangswerte: Zeilen Alter, Körperhöhe, Körpermasse, %PAH (Analysepopulation), dann die sieben Zielgrößen',
    'Tab. 2 Stichprobe und Ausgangswerte: Zeilen der sieben Zielgrößen (die Kennwerte der Stichprobe stehen im Text von 4.2, Zeile 4.2.5)')
# Befund 8: 20-m-Zwischenzeit
rep('| 6b | Änderungen der Endpunkte nach Studienbeginn mit Gründen | 4.4 (20-m-Zwischenzeit), 4.7 (deskriptiv statt konfirmatorisch: 5 m, 10 m, 505-Seiten) | P | 4.4 ✓, 4.7 n/a |',
    '| 6b | Änderungen der Endpunkte nach Studienbeginn mit Gründen | Tab. H6 und 6.3 G7 (20-m-Zwischenzeit, Verfasser 25.09., 22:19), 4.7 (deskriptiv statt konfirmatorisch: 5 m, 10 m, 505-Seiten) | P | 20 m vorgemerkt, 4.7 ✓ |')
zeile('| 4.4.3 |', '| 4.4.3 | Änderung des Endpunkts (keine 20-m-Zwischenzeit): entfällt in 4.4 (Verfasser 25.09., 22:19), vorgemerkt für Tab. H6 und 6.3 G7 | CONSORT 6b · Auswertungsplan § 5.7 | P | entfallen, der Marker mit dem Satz |')
rep('G7 Design-/Protokollabweichungen (Intervalle, Familiarisierung, 20 m,', 'G7 Design-/Protokollabweichungen (Intervalle, Familiarisierung, 20 m nicht erhoben,')
# Befund 9: 48 h als Tatsache in 4.3
zeile('| 4.3.10 |', '| 4.3.10 | 48-h-Abstand: 4.3 berichtet die Einhaltung an den Testterminen als Tatsache (Textvorschlag 4.3 § 6) · KG-Halbsatz (vor der Trainingsbelastung getestet, belastungsreduzierter Vortag erbeten) | Fassung 17 § 10 Soll-Formulierung | E | ✓ |')
zeile('| 5.1.10 |', '| 5.1.10 | entfällt: Die Einhaltung der 48-h-Vorgabe an den Testterminen steht als Tatsache in 4.3 (Textvorschlag 4.3 § 6) | — | — | entfallen |')
# Befund 10: G8-Wortlaut
rep('E5-Evidenz von Akademiespielern [EXTRAPOLATION]',
    'E5-Evidenz überwiegend von Akademie- oder Profispielern, Ausnahmen Liu et al. (2024, regionale U19, Tier 2) und Dambel et al. (2025) [EXTRAPOLATION] (Fassung 17 § 12 G8)')
# Befund 11: Einleitung endet mit den Hypothesen
rep('Schluss bleibt der Zweck. Kein Aufbau-Absatz.',
    'Schluss bleibt der Zweck. Kein Aufbau-Absatz. *Überholt 28.09.:* In der Einleitung folgen auf den Zweck der Satz zum Vorgehen und die Hypothesen, sie endet mit H0 und H1 (Kopfblock Einleitung, Zeilen 1.6 und 3.3).')
# Befund 12: vorgemerkt statt steht
rep('Das Datum der Festlegung steht in Tab. H6, 4.7 nennt die Reihenfolge ohne Datum', 'Das Datum der Festlegung ist für Tab. H6 vorgemerkt, 4.7 nennt die Reihenfolge ohne Datum')
# Befund 18 und Klick 19:25: 6.2 und 6.3
rep('G2 Zuteilung/Konfundierung (Cluster, Jahrgang, Begleitprogramme, Sprintreiz KG)',
    'G2 Zuteilung/Konfundierung (Cluster, Jahrgang, Begleitprogramme in beide Richtungen: Sprintreiz KG, früheres Mannschaftstraining der IG-Vereine)')
rep('G3 Umsetzung (unbeaufsichtigt, Selbstauskunft, keine Verblindung rollenweise, kein KG-Monitoring)',
    'G3 Umsetzung und Verdünnung (unbeaufsichtigt, Selbstauskunft, keine Verblindung rollenweise, kein KG-Monitoring, ITT-Befund als Befund über das Angebot)')
zl = t.split('\n')
i10 = [i for i, z in enumerate(zl) if z.startswith('| 6.2.10 |')]
if len(i10) != 1:
    raise SystemExit('Abbruch: Zeile 6.2.10 nicht eindeutig')
zl[i10[0]:i10[0] + 1] = [zl[i10[0]],
    '| 6.2.11 | Methodenwahl beim Reifestatus: %PAH nach Khamis und Roche statt Mirwald, aus der Einleitung verlegt (Klick in Task 7 neu) | Fassung 17 § 13 Nr. 36, § 6.5 | E | n/a |',
    '| 6.2.12 | Begleitbedingungen in beide Richtungen: eigene Sprinteinheiten nur im Plan der Kontrollgruppe, früheres Mannschaftstraining der IG-Vereine | Fassung 17 § 2 (Begleitbedingungen), § 12 G2 | E | n/a |']
t = '\n'.join(zl)
LOG.append('Zeilen 6.2.11 und 6.2.12')
# Befund 33: 4.3-Zeilen und 14a nach Fassung 17 § 13 Nr. 17
rep('| 14a | Zeitraum der Rekrutierung und Nachbeobachtung | 4.3 (Termine je Verein), 4.2 (Rekrutierung Juni 2026) | P | ✓ (KG-Termin 15.09. → 14.09.) |',
    '| 14a | Zeitraum der Rekrutierung und Nachbeobachtung | Abb. H7 (Termine je Verein, Erstverweis in 4.3), 4.2 (Rekrutierung Juni 2026) | P | 4.2 ✓, Abb. H7 vorgemerkt (Task 18) |')
rep('| 4.3.1 | Vier Phasen je Verein (Familiarisierung, Eingangstestung, Intervention, Abschlusstestung) mit Terminen' + SEMI + ' Rekrutierungs- und Nachbeobachtungszeitraum |',
    '| 4.3.1 | Vier Phasen je Verein (Familiarisierung, Eingangstestung, Intervention, Abschlusstestung), Termine für Abb. H7 vorgemerkt, im Text keine Tagesdaten (Fassung 17 § 13 Nr. 17) · Rekrutierungs- und Nachbeobachtungszeitraum |')
rep('| 4.3.2 | Antragsfenster (Prä KW 29, Post KW 35–36) und Abweichungen mit Grund (Vereinspläne) |',
    '| 4.3.2 | Abweichungen vom Antragsfenster mit Grund (Vereinspläne), ohne Kalenderwochen (Fassung 17 § 13 Nr. 17) |')
rep('Elternhöhen per Selbstauskunft, keine Post-Anthropometrie mit Grund |', 'Elternhöhen per Selbstauskunft, ohne Aussage zur Post-Anthropometrie (Fassung 17 § 13 Nr. 17, G7) |')
rep('| 4.3.8 | Messtechnik: Witty, Basic-Modus mit Begründung, sequenzieller Umbau' + SEMI + ' Datenhaltung Handprotokoll, Digitalisierung ohne Geräteexport |',
    '| 4.3.8 | Datenhaltung: Handprotokoll, Digitalisierung ohne Geräteexport. Die Messtechnik (Witty, Basic-Modus, Umbau) steht in der Testkette von 4.4 |')
# Befund 34: Prüfvermerk § 3.11, V3, V4, Tab. H5 in 5.1, Zahlen in 5.1.3 und 5.1.8
rep('**Prüfvermerke.** Kapitel 5 kann erst nach Blindrechnung in R und Abgleich final werden (Auswertungsverfahren Phasen 3 bis 7, L7 und L8). Die Python-Werte im Analyseprotokoll sind bis dahin Arbeitsstand. Die MDES liefert die Blindrechnung nach dem Standardweg (S18, O9), ohne R² und ohne Faktor SE.',
    '**Prüfvermerke.** Blindrechnung in R und Abgleich sind abgeschlossen (25.09.), Zahlenquelle ist das Kennzahlenblatt vom 25.09. Die Python-Werte im Analyseprotokoll sind nur Arbeitsstand vor dem Abgleich. Die MDES stammt aus der Blindrechnung nach dem Standardweg (S18, O9), ohne R² und ohne Faktor SE.')
rep('| DSHS-KI-Richtlinie · F14 § 14 · Auswertungsverfahren 8.2 |', '| DSHS-KI-Richtlinie · Fassung 17 § 14 (Mindestinhalt nach Textvorschlag 4.7, Nr. 57) · Auswertungsverfahren 8.2 |')
rep('zugeteilt 31 (18/13) · Rekrutierungszeitraum · analysiert 26 (16/10) · je Zielgröße Effektschätzer mit 95-%-KI',
    'zugeteilt und analysiert je Gruppe (K-01) · Rekrutierungszeitraum · Zweck als Ankersatz aus der Einleitung (Klick K6) · je Zielgröße Effektschätzer mit 95-%-KI')
zl = t.split('\n')
i9 = [i for i, z in enumerate(zl) if z.startswith('| 5.1.10 |')]
if len(i9) != 1:
    raise SystemExit('Abbruch: Zeile 5.1.10 nicht eindeutig')
zl[i9[0]:i9[0] + 1] = [zl[i9[0]], '| 5.1.11 | Schwellenlandschaft der Mindestdosis in einem Satz mit Erstverweis auf Tab. H5 | Umfangsdokument § 3.5 (Tab. H5 in 5.1 statt 4.7) · Fassung 17 § 11.7 | E | n/a |']
t = '\n'.join(zl)
LOG.append('Zeile 5.1.11')
rep('Per-Protokoll-Zahlen je Zielgröße (≥ 6 von 12: 30 m 9, Standweitsprung 9, 505-Seitenmittel 7 — B4/B7, Analyseprotokoll § 4) in einem Satz oder in Abb. 1',
    'Per-Protokoll-Zahlen je Zielgröße (≥ 6 von 12, K-08) in einem Satz oder in Abb. 1')
rep('Unerwünschte Ereignisse: 12 Schmerzmeldungen bei 9 Spielern, Lokalisation, zwei schmerzbedingte Nichtdurchführungen (Fragebogenauswertung § 0 Nr. 7)',
    'Unerwünschte Ereignisse: Schmerzmeldungen mit Zahl der Spieler und schmerzbedingte Nichtdurchführungen (K-10.12), Lokalisation nach dem Klickpunkt in Task 11')
# Befund 22: Einzelwerte offen bis Nr. 23
rep('| 5.2.6 | Antragskriterium ≥ 75 %: Einzelwerte der drei Spieler, deskriptiv |',
    '| 5.2.6 | Antragskriterium ≥ 75 %: Einzelwerte der Spieler (K-10.17), deskriptiv, offen bis zur Entscheidung zu Nr. 23 zu Beginn von Task 11 (Textvorschlag 4.7) |')
# Befund 35: Semikola in geänderten Kopfblöcken und § 4 Nr. 11
rep('Design in einem Satz, Saisonlage, Messzeitpunkte, Zielgrößenliste' + SEMI + ' Korpusmaß Design-Zug', 'Design in einem Satz, Saisonlage, Messzeitpunkte, Zielgrößenliste · Korpusmaß Design-Zug')
rep('keine Spielerzahl (Rev. 69)' + SEMI + ' K-03 nur, falls Termine hier bleiben (Klickfrage: Empfehlung nur 4.3).', 'keine Spielerzahl (Rev. 69) · K-03 (Termine) nur in Abb. H7 (Fassung 17 § 13 Nr. 17).')
rep('Bauplan § 2.2 (Intervention nach Testprotokoll, vor Statistik)' + SEMI + ' Vorlage Padrón-Cabo · Auswertungsplan § 5.4 Nr. 8 (Startvolumen 52 statt 60–80) · Zahlen: Trainingsdokumentation (Kontakte 52 → 120, 1.040 gesamt), Videodauern (Fragebogenauswertung § 6.5).',
    'Bauplan § 2.2 (Intervention nach Testprotokoll, vor Statistik) · Vorlage Padrón-Cabo · Auswertungsplan § 5.4 Nr. 8 (Startvolumen) · Zahlen: Programmkennzahlen P-01 bis P-12 (`03_Skripte\\Programmkennzahlen_2026-09-23.txt`).')
rep('Zahlen: keine Studienzahlen' + SEMI + ' Programme aus Anhang D.', 'Zahlen: keine Studienzahlen, Programme aus Anhang D.')
zeile('**Nr. 11 — CONSORT 2010 gegen 2025, TREND.**',
      '**Nr. 11 — CONSORT 2010 gegen 2025, TREND.** Geprüft am 22.09. (Rev. 58, 65): CONSORT 2025 (Hopewell et al.) und TREND (Des Jarlais et al., 2004) ändern den Pflichtkern nicht, Fröhlich Tab. 9.2 führt TREND nicht, die Volltexte liegen nicht im Ordner (F14 § 7.1). **Festlegung:** CONSORT 2010 „in Anlehnung“, Fassung mit Jahr in 4.1 nennen · TREND wird nicht genannt (Verfasser 23.09., Fassung 17 § 4) · die Wahl von CONSORT 2010 gegenüber 2025 in einem Satz begründen (G17e).')

# ------------------------------------------------------------------ § 11
t = t.rstrip('\n') + '''

## 11 Änderungen am 28.09.2026 (Rev. 3)

- Kopf: Rev.-3-Vermerk, Kennzahlenblatt vom 25.09. als Zahlenquelle, Verweise „F14 §“ gelten für Fassung 17.
- § 2.1: CONSORT 2a und 2b mit dem Ort Einleitung.
- § 2.4: Grundlagen und Forschungsstand in der Einleitung mit Abweichungsvermerk, Umfang mit 33 Seiten und 6.350 Wörtern.
- § 3.0: außerhalb der 6.350 und der Seitengrenze.
- § 3.1: Kopfblock „Einleitung“ statt § 3.1 bis § 3.3 der Rev. 2, Zeilen 1.1 bis 1.6, 2.1 bis 2.5 (Rollen), 3.1 bis 3.5, neu E.1 (Präventionssätze) und E.2 (Zweck des Zielgrößenzugs), Zeile 1.4 nach K6, Zeile 3.3 nach G32 (e), Doppelungen als Querverweis, Prüfvermerk zu SMK Abschn. 4.1.
- 4.1.10: Adhärenzkriterium mit Datum in Tab. H6, Vollregister mit Erstverweis in 4.1.
- 4.2.5 und § 3.11: Nachträge I19.
- 4.7.3 und 4.7.5 bis 4.7.15: Ort im Master, Zielorte und Satzorte nach Textvorschlag 4.7 § 3 und § 7 (G32 j).
- 6.1.1: Ankersatz aus der Einleitung (K6). 6.2.1: Planungsmodell der Antragsrechnung (L14 a). 7.4: Satzteile im Ausblick (G34 b).
- § 5 Zeilen 17 und 18: entfallen mit der Einleitung.
- § 7 Nr. 1, 10 und 14: Umfang nach K1 und K2, Tab. H6 mit Erstverweis in 4.1, KI-Deklaration nach Fassung 17 § 14.
- § 8: als historisch gekennzeichnet.
- § 3.4 bis § 3.14, Kopfblöcke: Budgets nach Fassung 17 § 5.2 (4.3 340, 4.4 420, 4.5.1 420, 4.5.2 150, 4.6 155, 5.1 230, 5.2 220), die Vorschläge aus § 8 stehen als „bis Rev. 2“ dabei. Lesehinweis § 3 und Herkunftsvermerk im Kopf auf Fassung 17. § 2.3 Kriterium 7 und § 4 Nr. 11 mit Dokumentnamen am Paragrafenverweis.
- Nach der übergreifenden Zweitprüfung (28.09., Fassung 3 des Erzeugers): Maßstab mit dem Kennzahlenblatt vom 25.09., Kennungen in den Kopfblöcken 4.4 und 5.1 und in 4.4.4, 6.1.3 und V4, Tab. 2 ohne Kennwerte (5.1.5), 20-m-Zwischenzeit in Tab. H6 und 6.3 (6b, 4.4.3, 6.3.2), 48-h-Angabe als Tatsache in 4.3 (4.3.10, 5.1.10 entfällt), 4.3-Zeilen und 14a nach Fassung 17 § 13 Nr. 17, neu 5.1.11 (Tab. H5), 6.2.11 (Reifemethode) und 6.2.12 (Begleitbedingungen), G2 in beide Richtungen und G3 mit der Verdünnung (6.3.2, Klick 19:25), G8-Wortlaut (6.3.5), § 4 Nr. 2 als überholt, § 4 Nr. 11 ohne TREND-Halbsatz, Prüfvermerk § 3.11, V3 nach Fassung 17 § 14, 4.7.6 und 5.2.6 als vorgemerkt oder offen, Semikola in geänderten Kopfblöcken ersetzt, Zeile 3.5 der Einleitung mit Zug- und Satzangaben nach der Zug-Tabelle des Textvorschlags.
- Erzeuger `03_Skripte\\Berichtsraster_Rev3_2026-09-28.py`, Rev. 2 als Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`.
'''
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(t)
print('Berichtsraster Rev. 3 geschrieben: %d Zeichen, %d Ersetzungen' % (len(t), len(LOG)))

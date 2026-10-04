# -*- coding: utf-8 -*-
"""tv5_md.py — Task 11: erzeugt 04_Uebergaben/Textvorschlag_5_2026-09-30.md aus Textvorschlag_5_2026-09-30.json,
dem Laufprotokoll Textvorschlag_5_2026-09-30.txt und optional den Bausteinen § 10 (Zweitprüfung) und § 11 (Einbau).
Hilfsskript des Tasks, Teil der Dokumentation (03_Skripte). Ohne Semikolon (chr(59)).
Aufruf: python tv5_md.py <json> <laufprotokoll.txt> <ausgabe.md> [<baustein_10.md>] [<baustein_11.md>]"""
import json
import re
import sys
import os

J = json.load(open(sys.argv[1], encoding='utf-8'))
LAUF = open(sys.argv[2], encoding='utf-8').read()
AUS = sys.argv[3]
B10 = open(sys.argv[4], encoding='utf-8').read().strip() if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else None
B11 = open(sys.argv[5], encoding='utf-8').read().strip() if len(sys.argv) > 5 and os.path.exists(sys.argv[5]) else None
BS = chr(92)


def pfad(p):
    return p.replace('/', BS)


def saetze(text):  # unverändert aus Manuskriptstand_2026-09-25.py
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', text)
    t = re.sub(r'\b(et al|Abschn|Tab|Abb|vgl|bzw|ca|Nr|Aufl|Hrsg|Jg)\.', r'\1<P>', t)
    t = re.sub(r'\b([A-Z])\.\s', r'\1<P> ', t)
    t = re.sub(r'\bS\.\s', 'S<P> ', t)
    t = re.sub(r'\b(u|z|d)\.\s?(a|B|h)\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})', r'\1<P>\2<P>\3', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d)\.\s', r'\1<P> ', t)
    teile = [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(⟨])', t) if s.strip()]
    return [s.replace('<P>', '.') for s in teile]


RASTER = {
    ('A1', 1): '5.1.1 (P, CONSORT 13a, 13b, Abb. 1) · 5.1.4 (P°, CONSORT 14b, „planmäßig“ nach Klick 30.09.) · 5.1.3 (P, Per-Protokoll-Zahlen je Zielgröße stehen in Abb. 1)',
    ('A1', 2): '5.1.2 (E, Rev. 69, einziger Satz der Menge „zur Eingangstestung angetreten“)',
    ('A1', 3): '5.1.5 (P, CONSORT 15, Tab. 2) · 5.2.7 (E, Überlappung als Spalte von Tab. 2) · Tab. H3 (Umfangsdokument § 3.5, Erstverweis)',
    ('A1', 4): '5.1.5 (P, Richtung der Ausgangsunterschiede als Orientierungsbefund, ohne Zahl und ohne Test, gilt für alle sieben Zielgrößen in Tab. 2 und Tab. H3)',
    ('A2', 1): '5.1.6 (P, TIDieR 12) · Status der Meldungen nach Berichtsort K-10.3 (T) · Median (K-10.8) · Tab. H2 (Erstverweis)',
    ('A2', 2): '5.1.6 (P, Umsetzungsrate, Nenner zwölf Einheiten je zugeteiltem Spieler) · Anteil mit den teilweise durchgeführten (K-10.6, Beteiligung nach 4.6, ohne das mehrdeutige Wort)',
    ('A2', 3): '5.1.6 (P, Antragskriterium mit Zahl der Spieler) · 5.1.11 (E, Schwellenlandschaft mit Erstverweis Tab. H5) · 5.2.6 (E, Einzelwerte des Antragskriteriums in Tab. H2, Verweis nach § 8 Nr. 2)',
    ('A2', 4): '5.1.6 (P, Untergrenzen bei ≥ 6 und ≥ 9, als Untergrenzen benannt, F17 § 3.2 „in 5.1 als Sensitivität“)',
    ('A3', 1): '5.1.7 (E, CR-10 mit n, M, SD, Median, Minimum, Maximum, Verfasser 24.09. Nr. 3 b, „als vollständig gemeldet“ als Selbstauskunft)',
    ('A3', 2): '5.1.7 (E, sRPE-Load mit denselben Kennwerten, Load-Sprachregelung F17 § 10)',
    ('A3', 3): '5.1.8 (P, CONSORT 19, TESTEX 6: Meldungen, Spieler und Status der betroffenen Meldungen, ohne Kausalzuschreibung, ohne Lokalisation nach § 8 Nr. 3)',
    ('A3', 4): '5.1.8 (P, Kontrollgruppe ohne Erfassungsinstrument, CONSORT 19 „in each group“)',
    ('A4', 1): '5.1.9 (E, Messgüte post, Tab. 1 Wiederaufruf, „auch“ knüpft an 4.4 an)',
    ('A4', 2): '5.1.9 (E, gültige Versuche je Gruppe und Zeitpunkt, Tab. H1 Wiederaufruf)',
    ('A5', 1): '5.2.1 (P, CONSORT 16, 17a, 18, Tab. 3) · 5.2.2 (P, unadjustiert neben adjustiert) · g über Tab. 3 mit KI',
    ('A5', 2): '5.2.8 (E, Abb. 2 mit einem einführenden Satz)',
    ('A5', 3): '5.2.2 (P, der Abstand ist der Befund, die Deutung steht in 6.1)',
    ('A5', 4): '5.2.1 (P, CONSORT 17a, adjustierte Differenz mit KI und p, Sprint)',
    ('A5', 5): '5.2.1 (P, Richtungswechsel und Sprung in der Reihenfolge Sprint, Richtungswechsel, Sprung)',
    ('A5', 6): 'F17 § 11.2b (E, Einordnung, Nullbefund-Sprachregelung F17 § 10)',
    ('A5', 7): 'F17 § 11.2b (E, Fall C1 im Wortlaut der Musterformulierung „in beide Richtungen“, Umfangsdokument § 5.1)',
    ('A5', 8): 'F17 § 11.2b (E, Fall C1, „unschlüssig“ wie die Musterformulierung)',
    ('A5', 9): 'Entscheidungsregel 4.7 (E, K-06.4), H0 an der adjustierten Differenz (Textvorschlag 4.7, Nr. 47)',
    ('A5', 10): 'Entscheidung über H0 (E, K-06.4)',
    ('A5', 11): '5.2.5 (P, CONSORT 17a teilweise, TESTEX 9, SMK 4.8, Tab. H3 Wiederaufruf)',
    ('A6', 1): '5.2.3 (P, CONSORT 12a, R2 und O7, Prüfgröße und p)',
    ('A6', 2): '5.2.3 mit R2 (P, Bootstrap-KI neben der verworfenen Prüfung, genau ein Satz, streichbares Modul)',
    ('A6', 3): '5.2.3 (P, „geprüft und nicht verworfen“, F17 § 11.9, Tab. H4 Wiederaufruf)',
    ('A6', 4): '5.2.4 (P, CONSORT 18, R1 Sammelsatz in der Zählung von 4.7: Per-Protokoll-Vergleich und sechs Sensitivitätsanalysen, Per-Protokoll als beobachtend gekennzeichnet, Tab. H4)',
}

m51 = re.search(r'Absatzgruppe 5.1: (\d+)', LAUF).group(1)
m52 = re.search(r'Absatzgruppe 5.2: (\d+)', LAUF).group(1)
mk = re.search(r'Kapitel 5: (\d+) Wörter gegen Budget 450 \(([^)]*)\), (\d+) Sätze, Median ([\d,]+), längster Satz (\d+), Sätze über 32: (\d+)', LAUF)
mz = re.search(r'(\d+) von (\d+) Einträgen stimmen\. Ziffernzahlen im Text (\d+), erfasst (\d+)\. Zahlwörter im Text (\d+), erfasst (\d+)', LAUF)
ergebnis = re.search(r'Ergebnis: (.*)', LAUF).group(1)
W = {a['kennung']: len(a['text'].split()) for a in J['absaetze']}
stand = (('nach Zweitprüfung und Einbau als Referenz, Übertragung in den Master durch den Verfasser (§ 11)' if 'durch den Verfasser' in B11 else ('nach Zweitprüfung und Einbau, Rückschreibung ausstehend (§ 11)' if 'ausstehend' in B11 else 'nach Zweitprüfung, Einbau und Rückschreibung')) if B11 else 'nach der Zweitprüfung') if B10 else 'vor der Zweitprüfung'

RUECK = (' **Übertragung:** Der Verfasser überträgt Kapitel 5 und die Löschung des Altbestands selbst in den Master (01.10.), der per Skript eingebaute Stand ist Referenz für den Abgleich danach (§ 11).' if B11 and 'durch den Verfasser' in B11 else (' **Die Rückschreibung in den Ordner steht aus:** Word sperrte den Master, danach war der Rechner nicht mehr verbunden (§ 11).' if B11 and 'ausstehend' in B11 else ''))
L = []
A = L.append
A('# Textvorschlag Kapitel 5 (Ergebnisse) — Task 11 — 30.09.2026')
A('')
A('Erstellt 30.09.2026, Stand ' + stand + ' (Task 11 nach Plan § 3 und Nachtrag 30.09., Startsatz Plan § 8, Teil 0 Rev. 134) · **Grundlage:** Berichtsraster Rev. 3 § 3.12 und § 3.13, § 4 Nr. 6, 7 und 12 · Bauplan § 2.3, § 4, § 5, § 6, § 8 · Gliederung v6 § 3.1 (Kapitel 5 ohne Unterabschnitte, E3) · Umfangsdokument § 3, § 5 und § 7 · Kennzahlenblatt 25.09. Rev. 2 · `03_Skripte' + BS + 'Objekte_2026-09-25` · Textvorschlag 4.7 (26.09.) § 7, Zeile Task 11 · Stilprofil · Skill `kapiteltext-bachelorarbeit` · Master vom 30.09. (57.471 Byte, MD5 `c7657a2c…`) · **Verfahren:** Wortlaut, Messung und Prüfungen per Skript `03_Skripte' + BS + 'Textvorschlag_5_2026-09-30.py` (Ausgabe `.txt` und `.json`), dieses Dokument per `03_Skripte' + BS + 'tv5_md.py`, Einbau als Referenz per `03_Skripte' + BS + 'Master_5_2026-09-30.py`, Übertragung in den Master durch den Verfasser, nur Text, keine Objekte und keine Platzhalter (F17 § 5.3). Die Absatzkennungen A1 bis A6 und die Gruppenmarken 5.1 und 5.2 sind Arbeitskennungen und gehören nicht in den Master.')
A('')
A('## 0 Kopf — Messung und Ergebnis in Kürze')
A('')
A('| Größe | Wert | Vorgabe |')
A('|---|---|---|')
A('| Wörter Kapitel 5 (Leerraum-Token wie Messskript) | **%s** | Budget 450 (Gliederung v6 § 3.4, verbindlich nach E4) |' % mk.group(1))
A('| davon Absatzgruppe 5.1 (A1 bis A4) | %s | Richtwert 230 (Blockwert, nicht bindend nach E4) |' % m51)
A('| davon Absatzgruppe 5.2 (A5, A6) | %s | Richtwert 220 |' % m52)
A('| Absätze · Sätze | 6 · %s | kein Absatz über 250 Wörter |' % mk.group(3))
A('| Satzlänge Median · längster Satz | %s · %s | Median 14 bis 18, kein Satz über 32 |' % (mk.group(4), mk.group(5)))
A('| Semikola · Abschnittsverweise · Belegklammern | 0 · 0 · 0 | 0 · 0 · 0 (Kapitel 5 ohne Beleg, Bauplan § 2.3) |')
A('| Deutungs- und Verbotswörter (weil, da, bestätigt, Effekt, signifikant, kein Effekt, randomisiert, ITT, Wirkung, Training, verbessert, Erhalt u. a.) | 0 | 0 (Plan § 3 Task 11) |')
A('| Zahlen im Text | %s Ziffernzahlen, %s Zahlwörter, %s von %s Einträgen gegen das Kennzahlenblatt stimmig oder als Konstante ausgewiesen (§ 5) | jede Zahl aus dem Kennzahlenblatt |' % (mz.group(3), mz.group(5), mz.group(1), mz.group(2)))
A('| Objektverweise | Erstverweise Abb. 1, Tab. 2, Tab. H3, Tab. H2, Tab. H5, Tab. 3, Abb. 2 · Wiederaufrufe als Klammer Tab. 1, Tab. H1, Tab. H3, Tab. H4 · jede Aussage am Objekt geprüft (§ 6) | Textobjekte als Satzsubjekt im Präsens, Wiederaufruf nur als Klammer |')
A('| Satzenden auf Ziffer oder Einzelbuchstaben, die die Satzteilung des Messskripts verdeckt | 0 | 0 (§ 7.2) |')
A('| Seitenprognose am Referenzstand nach dem Einbau (Messskript Fassung 4) | 27,8 Seiten | Modellrechnung, Grenze 33, Schwelle 32 |')
A('| Ergebnis des Prüfskripts | %s | — |' % ergebnis)
A('')
A('**In Kürze.** Kapitel 5 steht als ein Kapitel ohne Unterabschnitte in sechs Absätzen: ein Orientierungszug in vier Absätzen (Teilnehmerfluss und Ausgangswerte, Umsetzung, Beanspruchung und unerwünschte Ereignisse, Messgüte und Versuche), dann der Gruppenvergleich (Tab. 3, Abb. 2, drei Zielgrößen in fester Reihenfolge, Fall der Schlusslogik, Entscheidung über H0, deskriptive Zielgrößen) und die Absicherung (verworfene Normalverteilung beim 30-m-Sprint mit Bootstrap-Intervall, übrige Voraussetzungen, Sammelsatz aus Per-Protokoll-Vergleich und sechs Sensitivitätsanalysen). Kein Beleg, keine Deutung, keine Cohen-Klasse. Der Verfasser wies am 30.09. um 23:02 an, ohne Rückfrage abzuschließen. Die Empfehlungen gelten damit als entschieden und sind umgesetzt: Freigabe des Wortlauts, Einzelwerte des Antragskriteriums bleiben in Tab. H2, keine Lokalisation der Schmerzmeldungen, Löschung des Altbestands mit Archivkopie (§ 8). Die unabhängige Zweitprüfung fand einen A-Befund (Zählung der Varianten gegen 4.7) und zehn B-Befunde, alle eingearbeitet, einen davon in anderer Form (§ 10). **E3 (Gliederung v6, G37 f) hält:** Der Orientierungszug trägt ohne Überschrift, weil jeder Absatz mit seinem Gegenstand beginnt und der Gruppenvergleich mit „Tab. 3 enthält …“ deutlich einsetzt. Die Überschriften 5.1 und 5.2 entfallen beim Einbau (M28). **Schritt 0:** Die Einleitung im Master ist wortgleich mit dem Textvorschlag Überarbeitung § 5.1, der Altbestand Kapitel 2 und 3 stand aber noch im Master, seine Löschung ist entschieden (M24, § 8 Nr. 4). Messskript Fassung 4 liegt vor (§ 7), Einbau als Referenz, Messung, Endabgleich und Übertragung in § 11.' + RUECK + ' Vormerkungen für Kapitel 4, die Schlussfassung der Einleitung und die Folgetasks in § 9, darunter ein Formatfehler in 4.4 und die Ausfallkategorie der 10-m-Zeiten von Verein B.')
A('')
A('## 1 Wortlaut (zum Einbau, ohne die Kennungen A1 bis A6)')
A('')
for a in J['absaetze']:
    s = saetze(a['text'])
    A('**%s (Absatzgruppe %s, %d Wörter, %d Sätze)**' % (a['kennung'], a['gruppe'], len(a['text'].split()), len(s)))
    A('')
    A(a['text'])
    A('')
A('## 2 Zug-Tabelle (Bauplan § 2.3, skaliert auf 450 Wörter)')
A('')
A('| Zug (Bauplan § 2.3) | Umsetzung | Rasterzeilen | Wörter |')
A('|---|---|---|---|')
A('| Orientierungszug: Teilnehmerfluss, Stichprobenfluss, Ausgangswerte, Objekte einführen (Objektverweis als Satzsubjekt im Präsens) | A1: Abb. 1, der eine Satz 31 → 26, planmäßiges Ende, Tab. 2 mit d und Überlappung, Tab. H3, Richtung der Ausgangsunterschiede | 5.1.1 bis 5.1.5, 5.2.7 | %d |' % W['A1'])
A('| Orientierungszug: Adhärenz | A2: Meldungen nach Status, Median, Umsetzungs- und Beteiligungsrate, Schwellen ≥ 6 und ≥ 9, Untergrenzen, Tab. H2 und Tab. H5 | 5.1.6, 5.1.11 | %d |' % W['A2'])
A('| Orientierungszug: Beanspruchung und Sicherheit | A3: CR-10 und sRPE-Load mit je sechs Kennwerten, Schmerzmeldungen mit Status, Kontrollgruppe ohne Instrument | 5.1.7, 5.1.8 | %d |' % W['A3'])
A('| Orientierungszug: Messgüte | A4: TE post gegen SESOI (Tab. 1), gültige Versuche je Gruppe (Tab. H1) | 5.1.9 | %d |' % W['A4'])
A('| Block je Zielgröße: Objekt, Richtung, adjustierte Differenz → KI → p (g in Tab. 3) → Fall, Reihenfolge Sprint → Richtungswechsel → Sprung | A5: Tab. 3, Abb. 2, unadjustiert gegen adjustiert, drei Zielgrößen, Fall C1 im Musterwortlaut, H0 an der adjustierten Differenz, deskriptive Zielgrößen (Tab. H3) | 5.2.1, 5.2.2, 5.2.5, 5.2.8, § 11.2b | %d |' % W['A5'])
A('| Schluss: letzter Befundsatz mit Objektverweis, kein Resümee | A6: verworfene Prüfung mit W und p, Bootstrap-KI (ein Satz), übrige Prüfungen, Sammelsatz der Varianten mit (Tab. H4) als letztem Wort | 5.2.3, 5.2.4 | %d |' % W['A6'])
A('')
A('Eröffnung: Objektverweis als Satzsubjekt („Abb. 1 zeigt …“), wie Bauplan § 2.3. Schluss: letzter Befundsatz mit Objektverweis in Klammern, kein Übergang zur Diskussion. Tempus: Präteritum für Befunde, Präsens nur in den Objektverweisen (Bauplan § 6). Die Absatzgruppe 5.1 hat %s Wörter (Richtwert 230), 5.2 hat %s (Richtwert 220), die Blockwerte binden nach E4 nicht. Das Kapitel hat %s Wörter bei einem Budget von 450. Eine Kürzungsleiter entfällt, eine Stufenwahl auch (eine Stufe, § 8 Nr. 1).' % (m51, m52, mk.group(1)))
A('')
A('## 3 Verzichtstabelle — was der Korpus tut oder naheläge und hier nicht geschieht')
A('')
A('| Was der Korpus tut oder was naheläge | Grund des Verzichts |')
A('|---|---|')
for a, b in [
    ('Interaktion Gruppe × Zeit, Haupteffekte, Post-hoc-Vergleiche (Messwiederholungs-ANOVA)', 'Hauptverfahren ist die Kovarianzanalyse mit zwei Gruppen (4.7), es gibt keinen Post-hoc-Test. Die Folge des Bauplans wird zu „adjustierte Differenz → KI → p → g → Fall“ (Raster § 3.13, Kopfblock)'),
    ('Effektstärken mit verbalen Etiketten („klein“, „moderat“, „groß“) und Cohen-Klassen', 'Raster § 3.13 „Nicht hier“, Prüfliste Nr. 6, Textvorschlag 4.7 § 7 (Größenklasse = Fall der Schlusslogik). Die Einordnung trägt das KI gegen null und SESOI (4.7, Lakens, 2022)'),
    ('g im Fließtext', 'g steht mit KI in Tab. 3 (Plan Task 11 „g als Verweis auf Tab. 3“). Im Text stünde g nur mit KI (F17 § 11.4), das kostete rund 15 Wörter ohne neue Aussage'),
    ('Veränderungen innerhalb der Gruppen mit p (gepaarte Tests), Prozentänderungen, Veränderungswerte prä → post', 'Umfangsdokument § 5.4 Nr. 2 und 9, F17 § 11.2 (keine Differenz- oder Prozentwerte), ANCOVA-Sprachregelung F17 § 10. Die Werte stehen in Tab. 2 und Tab. 3, eine rein beschreibende Einordnung ist für 6.1 vorgemerkt (§ 9.3)'),
    ('Signifikanztests der Ausgangswerte', 'CONSORT Item 15, F17 § 4, Bauplan § 8. Tab. 2 zeigt d und Überlappung, der Text nur die Richtung'),
    ('„no significant differences“, „kein Effekt“, „Erhalt“', 'Nullbefund-Sprachregelung F17 § 10, Umfangsdokument § 5.4 Nr. 1 und 9: „kein Gruppenunterschied nachweisbar“ mit Punktschätzer und KI'),
    ('Einzelwertgrafiken und individuelle Veränderungen (Moran 2024, Liu 2024)', 'F17 § 11.6, TE > SESOI. Abb. 2 zeigt das Modell, keine Veränderung je Spieler'),
    ('Zusammenfassender Schlusssatz, Überleitung zur Diskussion', 'Bauplan § 2.3 (kein Resümee), letzter Satz ist ein Befundsatz mit (Tab. H4)'),
    ('Unterabschnitte 5.1 und 5.2 (3 von 11 Korpusstudien)', 'Gliederung v6 Ä16, E3 am Text geprüft (§ 0)'),
    ('Per-Protokoll-Ergebnisse mit Zahlen im Text', 'Regel R1: nur wenn eine Variante den Fall oder die Entscheidung ändert. Das tut keine (K-08, Fall C1 in jeder Zeile mit Inferenz), Sammelsatz mit (Tab. H4). Die Vorzeichenwechsel der Punktschätzer sind für 6.1 vorgemerkt (§ 9.3)'),
    ('Bootstrap-Intervalle aller drei Zielgrößen im Text', 'R2 verlangt das Bootstrap-KI neben der verworfenen Prüfung, also nur beim 30-m-Sprint. Die beiden anderen stehen in Tab. H4c, das Modul bleibt in genau einem Satz (Streichpaket, Textvorschlag 4.7 § 7)'),
    ('Hinweis auf die geringe Trennschärfe der Voraussetzungstests (Umfangsdokument R2)', 'F17 § 11.9 (jünger, maßgeblich): vorgemerkt für 6.2 (Textvorschlag 4.7, Nr. 15). In Kapitel 5 wäre er Deutung. Umfangsdokument R2 nachziehen (§ 9.7)'),
    ('Vorab-Prüfung an den Prä-Werten (Shapiro-Wilk beim 505-Seitenmittel der IG verworfen, K-07.2)', 'R2: „höchstens ein Satz“, keine ANCOVA-Voraussetzung, Berichtsort K-07.2 ist der Anhang (Tab. H4). Die verworfene Prüfung steht in der Anmerkung zu Tab. H4b und bleibt damit sichtbar (Umfangsdokument § 3, SMK 4.8). G29 (e) „in einem Satz“ ist durch R2 und den Berichtsort abgelöst, Vormerkung 6.2 (§ 9.4)'),
    ('Residuen-SD je Gruppe, adjustierte Mittelwerte, Modellkennwerte im Text', 'Tab. H4 (R3, Umfangsdokument § 3.4). Die Folge des Verhältnisses KG zu IG beim 30-m-Sprint ordnet 6.2 ein'),
    ('Linearität als Ergebnis im Text', 'nur grafisch geprüft (4.7, Diagramme in Anhang G), das Kennzahlenblatt trägt kein Urteil. A6 S3 spricht deshalb von den „mit Tests geprüften Voraussetzungen“'),
    ('unadjustierter p-Wert der 30-m-Differenz (S15.UDP, p < 0,001)', 'Tab. 3 führt nur den p-Wert der adjustierten Differenz (Textvorschlag 4.7, Nr. 47). A5 S9 macht die Entscheidung ausdrücklich an der adjustierten Differenz fest'),
    ('Anteil mit Post-Messung je Gruppe und Zielgröße (K-01.23) im Text', 'Abb. 1 zeigt die Spieler je Gruppe, Tab. H1c die Erhebungsanteile je Zielgröße. Den Text dazu verortet das Kennzahlenblatt in 6.3 (TESTEX 6, F17 § 4: TESTEX als internes Prüfwerkzeug, Befunde in 6.3). Rasterzeile 5.1.6 nennt ihn noch für 5.1 (Vormerkung Raster Rev. 4, § 9.7)'),
    ('Raten der Untergrenzen (K-10.7) im Text', 'Berichtsort Tab. H2 (A). Im Text stehen die Untergrenzen als Spielerzahlen an den Schwellen ≥ 6 und ≥ 9 (K-10.11, F17 § 3.2)'),
    ('Lokalisation der Schmerzmeldungen', 'nicht im Kennzahlenblatt, nur Freitextkategorien der Fragebogenauswertung vom 12.09. (Zahlenregel F17 § 1.2). § 8 Nr. 3: ohne Lokalisation, entschieden 30.09.'),
    ('Videopausen und Trainingsuntergrund aus dem Fragebogen (G28g)', 'Umfangsdokument § 2.2 und § 2.4 (Verfasser 24.09.): entfällt, „Untergrund und Videopausen tragen keinen Schluss“, in 6.3 G6 ohne Zahl, der Punkt „Untergrund“ in G8 entfällt. G28g (23.09.) ist in diesem Teil überholt (Zweitprüfung Nr. 10). Eine Wiederaufnahme wäre eine neue, datierte Entscheidung'),
    ('Einzelwerte der drei Spieler des Antragskriteriums im Text', 'Berichtsort Tab. H2 (K-10.17, A). § 8 Nr. 2, entschieden 30.09.: Einzelwerte bleiben in Tab. H2, Verweis (Tab. H2 und Tab. H5) in A2 S3, kein eigener Satz'),
    ('Familiarisierung Variante a, Deskription der Per-Protokoll-Mengen', 'Tab. H4 (R5), über den Verweis (Tab. H4) in A6 erfasst, nicht Teil des Sammelsatzes'),
    ('Beleg für Testverfahren (Shapiro-Wilk, Bootstrap) im Ergebniskapitel', 'Kapitel 5 ohne Beleg (11 von 11, Bauplan § 5). Die Verfahren stehen in 4.7'),
    ('Das Wort „Beteiligungsrate“ (K-10.6)', '4.6 definiert Beteiligung mehrdeutig („teilweise … gesondert als Beteiligung“). A2 S2 nennt den Anteil mit den teilweise durchgeführten Einheiten ausdrücklich (45,4 %), die Klarstellung in 4.6 ist vorgemerkt (§ 9.1 Nr. 3, Zweitprüfung Nr. 4)'),
    ('„Sieben Varianten, darunter der Per-Protokoll-Vergleich“ (Plan Task 11, Textvorschlag 4.7 § 7)', '4.7 im Master nennt „Sechs vorab festgelegte Sensitivitätsanalysen“ und getrennt davon den Per-Protokoll-Vergleich. A6 S4 übernimmt diese Zählung, die Summe sieben stünde sonst nirgends (Zweitprüfung Nr. 1)'),
]:
    A('| %s | %s |' % (a, b))
A('')
A('## 4 Rasterzuordnung je Satz (Berichtsraster Rev. 3 § 3.12 und § 3.13)')
A('')
A('| Absatz, Satz | Anfang des Satzes | Rasterzeile (Etikett, Anspruch) |')
A('|---|---|---|')
for a in J['absaetze']:
    for i, s in enumerate(saetze(a['text']), 1):
        A('| %s S%d | %s | %s |' % (a['kennung'], i, ' '.join(s.split()[:6]) + ' …', RASTER[(a['kennung'], i)]))
A('')
A('Nicht im Text, mit Ort: 5.1.3 Per-Protokoll-Zahlen je Zielgröße in Abb. 1 (9, 7, 9) · 5.1.6 letzter Teil (Anteil mit Post-Messung je Gruppe): Spielerzahlen je Gruppe in Abb. 1, Erhebungsanteile in Tab. H1c, Text in 6.3 G5 (Berichtsort K-01.23, F17 § 4) · 5.1.8 „schmerzbedingte Nichtdurchführungen“: A3 S3 nennt den Status der Meldungen mit Schmerzangabe, keine Ursache (Kausalität aus der Meldung nicht ableitbar) · 5.1.10 entfallen (48-h-Vorgabe in 4.3) · 5.2.6 Einzelwerte in Tab. H2, Verweis in A2 S3 (§ 8 Nr. 2) · 5.2.7 Überlappungszahlen in Tab. 2. **Offen (Zweitprüfung Nr. 11):** 5.1.1 (P, CONSORT 13b) verlangt die Gründe der zur Abschlusstestung nicht angetretenen Spieler, Abb. 1 nennt nur ihre Zahl (B9). Der Verfasser liefert die Gründe, oder Abb. 1 nennt „Grund nicht erhoben“ (Task 18). 5.2.3 (P) schließt die Linearität ein, die nur grafisch geprüft wurde. Kennzahlenblatt und Text tragen dazu kein Urteil. Das Urteil des Verfassers zu den Diagrammen in Anhang G ist festzuhalten (Task 16), danach gegebenenfalls ein Halbsatz in 5.2 mit Ausgleich im Kapitel. Alle übrigen P- und P°-Zeilen sind im Text oder im zugewiesenen Objekt erfüllt.')
A('')
A('## 5 Kennungen je Zahl (Begleitteil, im Manuskript ohne Kennung)')
A('')
A('Geprüft per Skript gegen `02_Befunde' + BS + 'Kennzahlen_2026-09-25_Werte.csv` (Spalten darstellung und bezeichnung): %s von %s Einträgen stimmen, jede Ziffernzahl und jedes Zahlwort des Textes ist erfasst (Laufprotokoll `03_Skripte' % (mz.group(1), mz.group(2)) + BS + 'Textvorschlag_5_2026-09-30.txt`).')
A('')
A('| Absatz | Zahl im Text | Kennung | Bezugsmenge, Bedeutung |')
A('|---|---|---|---|')
for zz in J['zahlen']:
    A('| %s | %s | %s | %s |' % (zz['absatz'], zz['zahl'], zz['kennung'], zz['bezugsmenge']))
A('')
A('Ergebniszahlen, die bewusst nicht im Text stehen, mit Ort: Box-6-Klassen und Gründe (K-01.9, K-01.17 bis K-01.22) in Abb. 1 · Ausgangswerte, d und Überlappung (K-04.1 bis K-04.8) in Tab. 2 und Tab. H4 · Post-Mittelwerte, unadjustierte Differenzen, g (K-06.1 bis K-06.3) in Tab. 3 · TE post (K-05) in Tab. 1 · k̄ je Gruppe (K-11.3) in Tab. H1 · Erhebungsanteile (K-01.23) in Tab. H1c und 6.3 · Summe der Meldungen (K-10.1) in der Anmerkung zu Tab. H2 · Wochenverlauf (K-10.16) in Tab. H2 · übrige Voraussetzungsprüfungen (K-07.1, K-07.2) und Varianten (K-08.1 bis K-08.11) in Tab. H4 · Schwellenlandschaft (K-10.15) in Tab. H5.')
A('')

# ------------------------------------------------------------------ § 6 Objektverweise
A('## 6 Objektverweise — jede Aussage am Objekt geprüft (`03_Skripte' + BS + 'Objekte_2026-09-25`)')
A('')
A('Bauplan § 8: Verweisfehler sind der häufigste handwerkliche Fehler des Korpus. Geprüft wurde nicht nur, ob das Objekt existiert (Prüfung 6 des Skripts), sondern ob es trägt, was der Satz ihm zuschreibt.')
A('')
A('| Verweis | Ort, Form | Aussage im Text | Befund am Objekt |')
A('|---|---|---|---|')
for r in [
    ('Abb. 1', 'A1 S1, Subjekt, Erstverweis', 'Teilnehmerfluss bis zum planmäßigen Studienende, daneben der Satz 31 → 26', '`Abb_1_Teilnehmerfluss.png`: Clusterebene (vier Vereine angefragt, einer ohne Zusage, drei zugeteilt), IG 18 und KG 13 eingangsgetestet, nicht angetreten 2 und 2, ohne %PAH 0 und 1, analysiert 16 und 10, Nenner je Zielgröße, Per-Protokoll 9, 7, 9. Stimmt. Lücke im Objekt: „Intervention erhalten 14“ mit 2 + 1 genannten Gründen, der vierte Spieler (Meldung ohne vollständige Einheit, Tab. H2a) fehlt → § 9.6'),
    ('Tab. 2', 'A1 S3, Subjekt, Erstverweis', 'Ausgangswerte im Analyseset mit d und Überlappung der Kovariaten', '`Tab_2_Stichprobe_Ausgangswerte.csv`: sieben Zielgrößen, n und M ± SD je Gruppe, d, Überlappung von Prä und %PAH bei den drei konfirmatorischen. Stimmt'),
    ('Tab. H3', 'A1 S3, Subjekt des zweiten Satzglieds, Erstverweis', 'Ausgangswerte aller eingangsgetesteten Spieler', '`Tab_H3a_Ausgangswerte_alle.csv`: IG 18, KG 13 (5 m KG 8). Stimmt'),
    ('— (A1 S4)', '—', 'alle Ausgangsunterschiede zugunsten der IG', 'd in Tab. 2 bei allen sieben Zielgrößen zugunsten der IG (Zeiten negativ, Standweitsprung positiv), ebenso in Tab. H3a. Stimmt'),
    ('Tab. H2', 'A2 S1, Klammer, Erstverweis', 'Meldungen nach Status, Median', '`Tab_H2a_Adhaerenz_je_Spieler.csv` mit Anmerkung: ganz 92 von 216 (42,6 %), ganz oder teilweise 98 (45,4 %), Median 6,0, Meldungen je Spieler (Summe 111 = 92 + 6 + 13). Stimmt'),
    ('Tab. H2', 'A2 S3, Klammer mit Tab. H5, Wiederaufruf', 'Antragskriterium: drei Spieler mit mindestens neun Einheiten', '`Tab_H2c_Antragskriterium.csv`: Einzelwerte der drei Spieler. Stimmt (§ 8 Nr. 2)'),
    ('Tab. H5', 'A2 S3, Klammer mit Tab. H2, Erstverweis', 'mindestens sechs: zehn, mindestens neun: drei', '`Tab_H5_Schwellenlandschaft.csv`: mindestens 6 → 10, mindestens 9 → 3. Stimmt'),
    ('Tab. 1', 'A4 S1, Klammer, Wiederaufruf (Erstverweis in 4.4)', 'TE post über dem SESOI in allen Zielgrößen', '`Tab_1_Messguete.csv`: TE post 0,040 · 0,050 · 0,090 · 0,053 · 0,072 · 0,041 · 6,7 gegen SESOI 0,016 · 0,021 · 0,063 · 0,023 · 0,023 · 0,020 · 3,3. Stimmt. „auch“ knüpft an 4.4 an („Der TE überstieg bei allen Zielgrößen den SESOI“), der Satz beginnt mit seinem Gegenstand'),
    ('Tab. H1', 'A4 S2, Klammer, Wiederaufruf (4.4)', 'k̄ höher in der IG bei 30 m und Standweitsprung zu beiden Zeitpunkten, beim 505 je Seite überwiegend in der KG', '`Tab_H1a_Versuche.csv`: 30 m 2,61 gegen 2,38 und 2,56 gegen 2,18 · Standweitsprung 2,50 gegen 2,08 und 2,00 gegen 1,91 · 505 links 1,83 gegen 1,69 und 1,62 gegen 2,00 · 505 rechts 1,89 gegen 1,92 und 1,44 gegen 1,55, KG in drei von vier Zellen höher. Stimmt'),
    ('Tab. 3', 'A5 S1, Subjekt, Erstverweis', 'unadjustierte und adjustierte Differenz, g', '`Tab_3_Gruppenvergleich.csv`: Spalten wie Raster 5.2.1. Stimmt'),
    ('Abb. 2', 'A5 S2, Subjekt, Erstverweis', 'je Zielgröße Ausgangswert und reifeadjustierter Abschlusswert jedes Spielers mit den Modelllinien beider Gruppen', '`Abb_2_Modell.png`: drei Felder, x Ausgangswert, y Abschlusswert adjustiert, Punkte je Spieler, Modelllinien IG und KG, Gruppenmittel. Stimmt'),
    ('— (A5 S3)', '—', 'unadjustierte Differenzen zugunsten der IG und weiter von null als die adjustierten', 'Tab. 3: −0,327 gegen −0,045 s · −0,060 gegen −0,012 s · +10,1 gegen −0,1 cm. Stimmt'),
    ('Tab. H3', 'A5 S11, Klammer, Wiederaufruf', '5 m, 10 m und 505 je Seite nur beschrieben', '`Tab_H3b_Deskriptive_Zielgroessen.csv`: prä und post je Gruppe mit n. Stimmt. Anmerkung dort „bei der Eingangstestung“ statt „bei der Abschlusstestung“ → § 9.6'),
    ('Tab. H4', 'A6 S3, Klammer, Wiederaufruf (Erstverweis in 4.7)', 'übrige mit Tests geprüfte Voraussetzungen nicht verworfen', '`Tab_H4b_Voraussetzungen.csv`: Shapiro-Wilk 505 p = 0,136, Standweitsprung p = 0,580 · Brown-Forsythe p = 0,148, 0,301, 0,390 · Steigungen alle p ≥ 0,165. Die Vorab-Prüfung an den Prä-Werten steht in der Anmerkung und ist keine Voraussetzung. Stimmt'),
    ('Tab. H4', 'A6 S4, Klammer, Wiederaufruf', 'Per-Protokoll-Vergleich und sechs Sensitivitätsanalysen ändern die Einordnung nicht, keine p < 0,05, Inferenz nur soweit die Fallzahl reicht', '`Tab_H4c_Varianten.csv` mit K-08: jede Variante mit Inferenz im Fall C1, kleinster p 0,372, beim 505-Seitenmittel Per-Protokoll ≥ 6 und ≥ 7 ohne Inferenz (7 und 6 Spieler). Die Tabelle führt dazu das Bootstrap-Intervall als achte Zeile, A6 S2 nennt es gesondert. Stimmt'),
]:
    A('| %s | %s | %s | %s |' % r)
A('')

# ------------------------------------------------------------------ § 7 Schritt 0 und Messskript
A('## 7 Schritt 0 und Messskript Fassung 4')
A('')
A('**7.1 Abgleich der Einleitung.** Skript `03_Skripte' + BS + 'Abgleich_Einleitung_Master_2026-09-30.py` mit `.txt`, Master 57.471 Byte, MD5 `c7657a2c9e19cb699c311fb85320fdff`, ohne `comments.xml`. Die sechs Absätze B1a bis B5 unter „1 Einleitung“ stehen Zeichen für Zeichen wie in § 5.1 des Textvorschlags Überarbeitung, ohne Direktformatierung. Messung wie dort § 5.2: 40 Sätze, 930 Wörter, 778 ohne Belegklammern, längster Satz 32, Median 24,0, 26 Belegklammern, 0 Semikola, 0 Abschnittsverweise. Die aufgeschobenen Nachträge (G35 a, i, k, l, H12, I20, T1, T4) waren nicht Gegenstand. **Befund:** M24 ist nicht ausgeführt. Der Altbestand Kapitel 2 und 3 steht noch im Master (10 Überschriften, 25 Absätze, 4.920 Wörter, alle 61 Semikola und 35 Abschnittsverweise des Masters). Nach B5 folgt ein leerer Absatz. Word hatte die Datei beim Stagen geöffnet. Entschieden in § 8 Nr. 4, gelöscht mit der Übertragung durch den Verfasser (§ 11).')
A('')
A('**7.2 Messskript Fassung 4 (G37 d).** `03_Skripte' + BS + 'Manuskriptstand_2026-09-25.py` in Fassung 4, Fassung 3 geht nach `_Archiv' + BS + '_ersetzt_2026-09-30_Messskript_Fassung3`. Neu: Budgets je Abschnitt der Gliederung v6 mit Arbeits- und Endnummer (verbindlich nach E4) neben den Blockrichtwerten · Blöcke der zusammengelegten Abschnitte (4.4.1 bis 4.4.3 → 4.4, 4.5.1, 4.5.2 und 4.6 → 4.5, 5.1 und 5.2 → 5, 6.3 → 6.2) · Altbestand getrennt ausgewiesen, nicht der Einleitung zugeschlagen · ein Blockrichtwert ist nur messbar, wenn jeder Block seiner Gruppe eine eigene Überschrift hat, sonst steht „ohne eigene Überschrift im Master“ · die Einleitung zählt in der Seitenschätzung gemessen, sobald ihr Text im Master steht · Erkennung der Endnummern nach Task 18 (an einem synthetischen Dokument geprüft). Fassung 3 wies am selben Master die Einleitung mit 5.850 Wörtern und zugleich als „nicht geschrieben“ aus, weil sie den Altbestand zuschlug. **Ergebnis am Eingang:** Einleitung 930 gegen 1.500 · Kapitel 4 (4.1 bis 4.7) 2.416 gegen 2.550 · Absatztext 3.346 ohne, 8.266 mit Altbestand · Prognose 27,8 Seiten (Modellrechnung). **Am Referenzstand nach dem Einbau:** Kapitel 5 450 gegen 450 · Absatztext Kapitel 1 bis 7 3.796 gegen 6.350 · 0 Semikola außerhalb von Zitierklammern und 0 Abschnittsverweise in Kapitel 1 bis 7 · 7 Platzhalter, alle in Anhang H · Prognose 27,8 Seiten (sie setzt für ungeschriebene Abschnitte das Budget an, Kapitel 5 ändert sie deshalb nicht). **Zur Prognose (Zweitprüfung Nr. 16):** Sie zählt die pausierte Einleitung mit gemessenen 930 Wörtern. Fassung 3 kam mit dem Budget 1.500 auf 29,4 Seiten. Bei der Obergrenze der Schlussfassung von 1.200 Wörtern (Plan, Nachtrag 30.09.) kämen rund 0,75 Seiten hinzu (Modellrechnung).')
A('')
A('**Befund zur Satzteilung (unverändert seit Fassung 1, nicht geändert):** `saetze()` schützt „Ziffer + Punkt“ als Ordinalzahl und „Großbuchstabe + Punkt“ als Initiale. Ein Satz, der auf eine Zahl oder auf „°C“ endet, verschmilzt deshalb in der Messung mit dem folgenden. Die beiden „Sätze über 32 Wörter“, die das Messskript für Kapitel 4 meldet, sind solche Artefakte: 4.3 „… um bis zu 10 °C. Alle Testungen …“ und 4.5.1 „… auf 120. Der Verlauf …“, ebenso verschmilzt 4.5.2 „… am 07.09. Eigene Sprinteinheiten …“. Kapitel 4 hat keinen Satz über 32 Wörter. Im Textvorschlag endet deshalb kein Satz auf eine Ziffer (Prüfung 7 des Skripts, A5 S9 dafür umgestellt: „… zeigte mit p < 0,05 einen Vorteil der Interventionsgruppe.“). Die Korrektur der Satzteilung ist für eine Fassung 5 vorgemerkt (§ 9.7).')
A('')

# ------------------------------------------------------------------ § 8 Entscheidungen
A('## 8 Entscheidungen (ohne Rückfrage, im Wortlaut § 1 und im Einbau umgesetzt)')
A('')
A('Der Verfasser wies am 30.09. um 23:02 (Sitzungsuhr) an: „Abschließen ohne Rückfrage“. Die vier Klickfragen wurden deshalb nicht gestellt. Die Empfehlungen gelten als entschieden und sind umgesetzt. Gründe und Alternativen bleiben zur Nachprüfung stehen, jede Entscheidung lässt sich mit den genannten Folgen umkehren.')
A('')
A('**Nr. 1 — Freigabe des Wortlauts.** Entschieden: Freigabe wie vorgelegt, 450 von 450 Wörtern. Eine Stufenwahl entfällt, es gibt eine Stufe. Jede spätere Änderung am Wortlaut braucht eine Kürzung an anderer Stelle im Kapitel. Das streichbare Modul Bootstrap (A6 S2, 14 Wörter) bleibt, solange 4.7 den Bootstrap nennt, die Entscheidung über das Streichpaket gehört nach Task 18 (Textvorschlag 4.7 § 7). Per Skript eingebaut und als Referenz geprüft, in den Master überträgt der Verfasser (01.10., § 11): sechs Absätze unter „5 Ergebnisse“, die Überschriften 5.1 und 5.2 entfallen (M28), keine Objekte, keine Platzhalter. Danach F9 für das Inhaltsverzeichnis.')
A('')
A('**Nr. 2 — Nr. 23: Einzelwerte der drei Spieler des Antragskriteriums (K-10.17, Raster 5.2.6).** Entschieden wie empfohlen: **Die Einzelwerte bleiben in Tab. H2 (H2c), ohne eigenen Satz.** Der Text führt Tab. H2 bei den drei Spielern mit mindestens neun Einheiten auf (A2 S3, „(Tab. H2 und Tab. H5)“). Gründe: (1) 4.7 im Master verspricht: „Beschreibend berichtet werden … alle Teilmengen unter acht Spielern je Gruppe“. Ohne Einzelwerte bliebe die Teilmenge des Antragskriteriums bis auf ihre Größe unbeschrieben. (2) Umfangsdokument R5 legte am 24.09. die Einzelwerte beim Antragskriterium als einzige Ausnahme der Deskriptionsregel fest, R7 die Objekte unabhängig vom Ergebnis. (3) Im Text kostet die Entscheidung nur den Verweis auf Tab. H2 in A2 S3 (drei Wörter). (4) Das Deutungsrisiko (Dosis-Wirkung, Responder), mit dem Textvorschlag 4.7 Nr. 23 die Streichung begründete, begrenzen der fehlende Text und die ausgeschlossenen Schlüsse (Umfangsdokument § 5.4 Nr. 5 und 6). 6.1 greift die Einzelwerte nicht auf. **Dagegen spricht:** Der Erkenntniswert ist gering (drei Spieler, typischer Messfehler über dem SESOI). Weil diese Gründe ergebnisunabhängig sind, ließe das Umfangsdokument (§ 2.1) auch die Streichung zu. Prüfliste Nr. 6 des Berichtsrasters schließt Einzelwerte je Spieler aus, F17 § 5.3 und Plan Task 11 verorten das Antragskriterium in 5.2, hier steht es bei der Umsetzung in A2. Beides ist als Ausnahme nachzutragen (§ 9.7). **Das weicht offen von der Empfehlung vom 26.09. ab** (Textvorschlag 4.7 Nr. 23: streichen, auch wegen des fehlenden Erkenntniswerts). Den Ausschlag gibt das Versprechen in 4.7 im Master. Alternativen mit Folgen: (b) streichen: A2 S3 endet mit „(Tab. H5)“, drei Wörter weniger, das Versprechen in 4.7 wäre für diese Teilmenge nur mit ihrer Größe eingelöst, Umfangsdokument R5 und F17 § 11.9 nachziehen, Eintrag als nachträgliche Festlegung ins Register (Auswertungsplan § 5.10) · (c) statt der Einzelwerte n, M und SD der Veränderung nach der Regelform von R5: Dafür gibt es keine Kennung (nur die Einzelwerte K-10.17 und die Setgröße in K-08.10), nötig wären ein Erzeugerlauf mit neuer Kennung und ein Registereintrag · (d) Einzelwerte streichen und den Per-Protokoll-Vergleich mit Zahlen berichten: rund 30 Wörter mehr, nur mit Kürzung an anderer Stelle, R1 verlangt es nicht, weil keine Variante Fall oder Entscheidung ändert.')
A('')
A('**Nr. 3 — Lokalisation der Schmerzmeldungen (Raster 5.1.8).** Entschieden wie empfohlen: **ohne Lokalisation.** Gründe: (1) Zahlenregel F17 § 1.2: Das Kennzahlenblatt zählt Meldungen, Spieler und Status (K-10.12), die Lokalisation steht nur in der Fragebogenauswertung vom 12.09. (aus Freitext kategorisiert, keine Zahlenquelle). (2) Die Kategorien wären eine nachträgliche Kodierung von Freitext mit Spielraum: Mehrfachnennungen, Muskelkater teils anderem Training zugeschrieben, zwei der sechs Kniemeldungen nach dem Freitext vorbestehend. Über einen Zusammenhang mit dem Programm sagen sie nichts. (3) CONSORT 19 ist in der Mindestform bedient: Zahl der Meldungen und Spieler, Status der betroffenen Einheiten, Kontrollgruppe ohne Instrument. (4) Rund 12 Wörter, bei 450 von 450 nur mit Kürzung an anderer Stelle. **Nachteil:** 6.1 (Raster 6.1.4, Nutzen und Schaden) und Kapitel 7 (Raster 7.2, Belastungsverträglichkeit) können nur Zahl und Status der Meldungen nennen, nicht die Art der Beschwerden. Rasterzeile 5.1.8 nennt die Lokalisation, sie wird in Rev. 4 angepasst (§ 9.7). Alternative: Erzeuger Rev. 3 mit neuer Kennung K-10.18 (Kategorien per Skript aus dem Fragebogen-Export nach einer vorab festgelegten Kodierregel, als nachträglich gekennzeichnet), ein Satzteil in A3 mit Kürzung an anderer Stelle und kurzer Nachprüfung.')
A('')
A('**Nr. 4 — Altbestand Kapitel 2 und 3 (M24).** Entschieden wie empfohlen: **löschen**, vorher Archivkopie des Masters mit Altbestand: `_Archiv' + BS + '_ersetzt_2026-09-30_Master' + BS + 'Bachelorarbeit_Geruest_v1_vor_Kapitel5_2026-09-30.docx` (MD5 `c7657a2c…`, § 11). Am Referenzstand löschte das Skript (`--altbestand`) genau die zehn Überschriften von „2 Theoretischer Hintergrund und Forschungsstand“ bis „3 Fragestellung und Hypothesen“ samt 25 Textabsätzen mit 4.920 Wörtern und zehn Textmarken. Es hätte abgebrochen, wenn Überschriftentexte, Absatz- oder Wortzahl abgewichen wären, wenn im Bereich eine Tabelle, ein Feld oder ein Abschnittswechsel gelegen hätte oder wenn Textmarken aus dem Bereich herausgeragt hätten. Gründe: Die Einleitung ersetzt den Altbestand (F17 § 5.2), ohne die Löschung wäre die Übertragung nur halb erledigt, und im Altbestand standen alle 61 Semikola und 35 Abschnittsverweise des Masters. M24 war dem Verfasser zugeordnet (Gliederung v6, Änderungsliste). Falls er den Altbestand bewusst stehen ließ, etwa als Material für die Schlussfassung der Einleitung, liegt er vollständig in der Archivkopie. Im Master löscht der Verfasser den Altbestand mit der Übertragung von Kapitel 5 (01.10.), der Abgleich prüft es (§ 11). Der leere Absatz nach B5 bleibt, er gehört zur Endredaktion (§ 9.6).')
A('')

# ------------------------------------------------------------------ § 9 Vormerkungen
A('## 9 Vormerkungen (gesammelt, nicht eingebaut)')
A('')
A('**9.1 Kapitel 4**')
A('')
for i, t in enumerate([
    '**Formatfehler 4.4:** Die drei Absätze vor 4.4.1 tragen direkte Schriftgröße 10 pt (`w:sz` 20 an den Läufen und der Absatzmarke), alle übrigen Textabsätze von Einleitung und Kapitel 4 stehen ohne Direktformatierung in der Formatvorlage Standard (Prüfung am Master vom 30.09.). Korrektur per Skript in der Endredaktion (Task 18, mit M27), Wirkung auf die Seitenzahl gering.',
    '**Ausfallkategorie der 10-m-Zeiten von Verein B bei der Abschlusstestung:** 4.4 nennt als Ausfallgründe Lichtschrankenausfall, Zeitmangel und nicht wiederholbare Fehlversuche, 4.4.1 für die fehlende 10-m-Zeit von Verein B einen Lichtschrankenausfall. K-11.4 und Tab. H1b führen diese 27 Zeilen unter „falsch aufgenommen“ (Kategorie FALSCH nach S03), nicht als technischen Ausfall. Der Verfasser klärt, was geschah. Danach entweder 4.4 und 4.4.1 anpassen (etwa „oder falsch aufgenommene Zeiten“, Budget 4.4: 392 gegen 420) oder die Kategorie in der Datenhaltung berichtigen (neuer Datenstand, Erzeuger und Objekte). Kapitel 5 nennt keine Kategorie und ist nicht berührt.',
    '**4.6 „Beteiligung“:** 4.6 sagt „Meldungen mit dem Status „teilweise“ zählten gesondert als Beteiligung“. Das lässt sich lesen, als umfasse die Beteiligung nur „teilweise“ (6 von 216 angebotenen Einheiten). Kapitel 5 vermeidet das Wort und nennt den Anteil mit den teilweise durchgeführten Einheiten in Klammern (K-10.6: 98 Einheiten, 45,4 %). In der Endredaktion „als Beteiligung“ streichen oder klarstellen, dass die Beteiligung „ganz“ und „teilweise“ umfasst, im Rahmen des Budgets 725 des Abschnitts 4.5 (722).',
    '**Begriffe zwischen 4.6 und Kapitel 5 (Zweitprüfung Nr. 19):** 4.6 definiert Adhärenz als Zahl der Meldungen mit dem Status „ganz“ je Spieler bei zwölf angebotenen Einheiten. Kapitel 5 berichtet sie als „vollständige je Spieler“ (Median) und als Umsetzungsrate (Anteil an allen angebotenen Einheiten der Interventionsgruppe, K-10.5), ohne das Wort „Adhärenz“. In der Endredaktion prüfen, ob 4.6 die Umsetzungsrate einführt oder A2 S1 den Begriff aufnimmt (etwa „bei einer medianen Adhärenz von 6,0 Einheiten“, ein Wort mehr, nur mit Kürzung). „Analyseset“ und „Programmwoche“ kommen in Kapitel 4 nicht vor, beide sind aus dem Zusammenhang verständlich.',
    '**Kein Handlungsbedarf, zur Kenntnis:** 4.7 nennt die drei Spieler des Antragskriteriums als Grund der Festlegung, Kapitel 5 als Ergebnis (Raster 5.1.6, P). Keine wörtliche Doppelung (Bauplan § 8), beide Stellen sind nötig. 4.4 führt TE und SESOI ein, Kapitel 5 schreibt „typischer Messfehler“ aus und nutzt „SESOI“.',
], 1):
    A('%d. %s' % (i, t))
A('')
A('**9.2 Schlussfassung der Einleitung (Prüfkatalog des Plan-Nachtrags vom 30.09.)**')
A('')
for i, t in enumerate([
    '**(c) Hypothesen gegen die H0-Entscheidung:** B5 S3 und S4 sprechen von „Veränderungen“ und einer „besseren Leistungsveränderung“, Kapitel 5 berichtet die adjustierte Gruppendifferenz im Post-Wert und schreibt nur „Die Nullhypothese wurde nicht verworfen.“ (A5 S10). Rechnerisch ist es dieselbe Gruppendifferenz: Mit dem Ausgangswert als Kovariate ist der Gruppenkoeffizient für Post-Wert und Veränderung identisch. Kapitel 5 passt auf beide Fassungen von B5 und braucht keine Änderung. Für die Schlussfassung: „Veränderungen“ antragsnah lassen oder „bei gleichem Ausgangswert“ ergänzen (F17 § 10, ANCOVA-Sprachregelung).',
    '**(c) Begriff:** B5 S4 „in mindestens einem der drei gleichrangigen Parameter“, 4.7, Kapitel 5 und die Objekte sagen „Zielgröße“. Antragsnähe (G32 e) gegen Einheitlichkeit, Entscheidung in der Schlussfassung.',
    '**(a) 10-m-Zeit als Gegenbefund:** B1a S5 hebt hervor, dass die 10-m-Zeit nach Ramirez-Campillo et al. (2020) nicht nachweisbar besser wurde. Die Arbeit kann diese Erwartung nicht prüfen, 5 m und 10 m sind nur beschrieben (10 m in der IG 7 Spieler, Tab. 2). Prüfen, ob der Satz als Kontext für 6.1 trägt, ohne eine Prüfung anzukündigen.',
    '**(c) Zweck:** B5 S1 („… gegenüber einer Kontrollgruppe verbessert“) bleibt als Ankersatz. Kapitel 5 beantwortet ihn mit „kein Gruppenunterschied nachweisbar“ und Fall C1, 6.1 nimmt den Ankersatz ohne „deshalb“ auf (Rev. 128).',
], 1):
    A('%d. %s' % (i, t))
A('')
A('**9.3 Task 12a (6.1)**')
A('')
for i, t in enumerate([
    'Hauptbefund in der Sprache von Kapitel 5: kein Gruppenunterschied nachweisbar, Fall C1 bei allen drei Zielgrößen, H0 nicht verworfen (K-06). Der Abstand zwischen unadjustierter und adjustierter Differenz (Tab. 3, Abb. 2) trägt die Einordnung (F17 § 11.2a).',
    'Verdünnung (F17 § 11.7): Umsetzungsrate 42,6 %, Median 6,0 (K-10.5, K-10.8). K-10.15 zählt vier Spieler ohne vollständige Einheit, darunter BW-21 ohne Listenplatz (als null gezählt, in Tab. H2a „nicht erhebbar“). Textvorschlag 4.7 § 7 spricht von „drei Spielern ohne vollständige Einheit“, maßgeblich ist das Kennzahlenblatt, die Bezugsmenge im Satz nennen.',
    'Per-Protokoll nicht als „gleiches Ergebnis“: Die Punktschätzer wechseln das Vorzeichen (30 m +0,033 gegen −0,045 s, Standweitsprung +0,5 gegen −0,1 cm, K-08.1, K-06), beim 505-Seitenmittel nur Beschreibung (7 und 10 Spieler), beobachtend.',
    'Rein beschreibend, ohne Test und ohne „Erhalt“ (Umfangsdokument § 5.4 Nr. 2 und 9): Mittelwerte prä und post im Analyseset lagen beim 30-m-Sprint in der IG bei 4,51 und 4,57 s, in der KG bei 4,89 und 4,89 s, beim 505-Seitenmittel bei 2,46 und 2,47 s sowie 2,53 und 2,53 s, beim Standweitsprung bei 238 und 233 cm sowie 226 und 223 cm (K-04.3, K-04.6, K-04.7, K-06.1 bis K-06.3). Kein Test und kein Vergleich mit dem typischen Messfehler (der gilt für Einzelwerte, Umfangsdokument § 7 Nr. 1). Möglicher Bezug zur Sommerpause (Einleitung B3), modalisiert.',
    'Beanspruchung: CR-10 2,9 im Mittel, je Programmwoche 2,6 bis 3,3 bei steigender Kontaktzahl (K-10.13, K-10.16, P-Kennungen), Load-Sprachregelung beachten. Nutzen und Schaden: 12 Meldungen mit Schmerzangabe von neun Spielern, keine Erfassung in der KG (K-10.12).',
    '6.1.4 Nutzen und Schaden ohne Lokalisation (§ 8 Nr. 3): nur Zahl der Meldungen, Spieler und Status. Kein „schmerzbedingt“: Die Meldungen zu nicht und teilweise durchgeführten Einheiten tragen eine Schmerzangabe, einen Grund der Nichtdurchführung belegen sie nicht. Kein Zusammenhang mit dem Programm ableitbar, die Kontrollgruppe hatte kein Instrument.',
    'Die Einzelwerte des Antragskriteriums (Tab. H2c) nicht aufgreifen (§ 8 Nr. 2, Umfangsdokument § 5.4 Nr. 5 und 6).',
], 1):
    A('%d. %s' % (i, t))
A('')
A('**9.4 Task 12b (6.2 mit 6.3)**')
A('')
for i, t in enumerate([
    '6.2: Residuen-SD beim 30-m-Sprint in der KG fast doppelt so groß wie in der IG (Verhältnis 1,94) bei 16 zu 10 Spielern (K-07.1, Tab. H4b), Richtung der Folge für Intervall und p nach Voraussetzungsprüfungen § 5.3. Trennschärfe der Tests (F17 § 11.9, Textvorschlag 4.7, Nr. 15). Vorab-Prüfung an den Prä-Werten (505-Seitenmittel der IG, W = 0,871, p = 0,029, K-07.2) nur, wenn 6.2 die Ausgangslage beschreibt.',
    '6.3 G5, Richtung je Zielgröße: Mehr gültige Versuche hatte beim 30-m-Sprint und Standweitsprung die IG zu beiden Zeitpunkten, beim 505 je Seite überwiegend die KG (drei von vier Zellen), beim 5-m-Sprint die IG zu beiden Zeitpunkten, beim 10-m-Sprint vor der Intervention die IG und danach die KG (Tab. H1a, K-11.3). F17 § 12 G5 „gerichtet zugunsten der IG“ gilt damit für 30 m, 5 m und Standweitsprung, beim 505 eher umgekehrt. Je Zielgröße formulieren. A4 S2 nennt nur die konfirmatorischen Zielgrößen und den 505 je Seite (Zweitprüfung Nr. 19).',
    '6.3 G5, TESTEX 6: Erhebungsanteil auf Teilnehmerebene gesamt 87,1 %, IG 88,9 %, KG 84,6 % (K-01.23 TN). F17 § 4 „≥ 85 % auf Teilnehmerebene erfüllt“ gilt nur für die Gesamtzahl, die KG liegt knapp darunter. Je Zielgröße 10 m IG 38,9 %, 505-Seitenmittel 72,2 % und 76,9 %.',
    '6.3: Trainingsuntergrund und Videopausen entfallen nach Umfangsdokument § 2.2 und § 2.4 (Verfasser 24.09.: „tragen keinen Schluss“, G6 ohne Zahl, der Punkt „Untergrund“ in G8 entfällt). G28g ist in diesem Teil überholt. Unerwünschte Ereignisse: Die Kontrollgruppe hatte kein Erfassungsinstrument (CONSORT 19 „in each group“), in 6.3 als Grenze nennen.',
], 1):
    A('%d. %s' % (i, t))
A('')
A('**9.5 Task 13b (Zusammenfassung und Abstract):** Hauptbefund im Wortlaut von Kapitel 5 („kein Gruppenunterschied nachweisbar“, „unschlüssig“, keine Cohen-Klasse), Umsetzungsrate 42,6 % mit Bezugsmenge (K-10.5), Zahlen aus K-01, K-06 und K-10.')
A('')
A('**9.6 Task 16 bis 18 (Anhänge, Objekte und Endredaktion)**')
A('')
for i, t in enumerate([
    'Abb. 1: Die Box „Intervention erhalten: n = 14“ nennt 2 + 1 Gründe, der vierte Spieler ohne vollständige Einheit (HL-06, eine Meldung ohne Status „ganz“, Tab. H2a) fehlt. Zeile „Meldung ohne vollständige Einheit: n = 1“ im Objekte-Skript ergänzen, nicht von Hand. Die Box-6-Klasse Nichteinhaltung (K-01.18, IG 7 mit weniger als sechs vollständigen Einheiten, Berichtsort „T · Abb. 1, 4.7“) zeigt Abb. 1 nicht (Zweitprüfung Nr. 15). Gründe der nicht Angetretenen (Raster 5.1.1, B9) und gemeldete Spieler je Verein (B5 Rest) weiter offen.',
    'Tab. H3b, Anmerkung: „Beim 10-m-Sprint fiel bei der Eingangstestung von Verein B die Lichtschranke aus.“ Richtig ist die Abschlusstestung (Tab. H3a: 10 m prä IG 18, K-11.5: ohne Post-Wert IG 11). Die Ursache nach der Klärung in § 9.1 Nr. 2. Korrektur im Objekte-Skript.',
    'Tab. 3: g beim Standweitsprung erscheint nach der Darstellungsregel (Vorzeichen immer) als „−0,00“. Beim Setzen prüfen, ob „−0,00“ mit Anmerkung oder „0,00“.',
    'Platzhalter in Anhang H, nach M28 und den Erstverweisen veraltet: „Tab. H2 … (aus 5.1)“ und „Tab. H3 … (aus 5.2)“ (beide jetzt aus Kapitel 5) · „Tab. H4: Sensitivitätsanalysen – acht vorab festgelegte Varianten und Gegenprobe 30 m (aus 5.2)“ (4.7 zählt sechs Sensitivitätsanalysen und den Per-Protokoll-Vergleich, dazu das Bootstrap-Intervall für alle drei Zielgrößen, Erstverweis in 4.7) · „Tab. H5 … (aus 4.7)“ (Erstverweis jetzt in Kapitel 5). Task 18 ersetzt die Platzhalter durch die Objekte.',
    'Abkürzungsverzeichnis: AU (A3), CR-10, sRPE, TE, SESOI, %PAH, KI. „KI“ steht in den Tabellen für Konfidenzintervall, im Vorspann (KI-Deklaration) für künstliche Intelligenz. In der Endredaktion auflösen.',
    'Statistische Symbole (p, W, M, SD, n, d, g) stehen im Master nirgends kursiv, das Einbauskript setzt schlichte Läufe wie der übrige Text. Einheitlich in Task 18 entscheiden (F17 § 9, dvs 2020).',
    'Leere Absätze nach B5 der Einleitung und am Ende von 4.5.1. Formatfehler 4.4 (§ 9.1 Nr. 1).',
    'Anhang C, einleitender Absatz: ein Semikolon zwischen „… bewusst niedrigvolumig gehalten“ und „über die Probeversuche hinaus …“, in zwei Sätze teilen (Task 17). Kapitel 1 bis 7 sind frei von Semikola außerhalb von Zitierklammern.',
    'Objektverweise nach dem Einsetzen der Objekte erneut einzeln prüfen (Bauplan § 8), Grundlage § 6 dieses Dokuments. Anmerkungen zu Tab. 2 und Tab. 3 nach Textvorschlag 4.7 § 7.',
    'Endabgleich Fassung 4 (Task 18): Satzprüfungen für Kapitel 5 ergänzen (Fassung 3 ordnet die Zahlen von Kapitel 5 nur nach dem Wert zu, die Zuordnung je Zahl steht in § 5), SP6 (Tab. 1 steht bis Task 18 nicht im Master) und SP11 (die 45-s-Pause entfiel mit Klick G28h) anpassen, die Konstanten der Methodik in 4.4, 4.6 und 4.7 wieder als Konstanten erkennen (§ 11).',
], 1):
    A('%d. %s' % (i, t))
A('')
A('**9.7 Steuerdokumente-Task (G37) und Kennzahlenblatt**')
A('')
for i, t in enumerate([
    'Berichtsraster Rev. 4: Zeile 5.1.6, letzter Teil (Anteil mit Post-Messung je Gruppe) → Abb. 1, Tab. H1c und 6.3 · Zeile 5.1.8 „schmerzbedingte Nichtdurchführungen“ → „Meldungen mit Schmerzangabe je Status“ (keine Kausalzuschreibung), Lokalisation entfällt (§ 8 Nr. 3) · Zeile 5.2.6 und Prüfliste Nr. 6: Einzelwerte des Antragskriteriums in Tab. H2 als Ausnahme nach R5 (§ 8 Nr. 2) · 5.1.1 (Gründe der nicht Angetretenen) und 5.2.3 (Linearität) offen (§ 4) · Kopfblock 5.1: Tab. H1 ist seit 4.4 eingeführt, in Kapitel 5 nur Wiederaufruf · 5.1 und 5.2 als Absatzgruppen nach v6.',
    'Umfangsdokument R2: Der „Hinweis auf die geringe Trennschärfe“ steht nach F17 § 11.9 in 6.2, nicht in 5.2 (Nachtragsvermerk). R5 bleibt nach § 8 Nr. 2 unverändert, der Nachtragsvermerk „R5 nach der Entscheidung zu Nr. 23 in Task 11“ (F17 § 1.3) ist damit erledigt. F17 § 5.3 und § 11.9: Antragskriterium mit Einzelwerten in Tab. H2, im Text bei der Umsetzung, weil Kapitel 5 ohne Unterabschnitte steht. Nachtrag mit Fassung 18.',
    'Kennzahlenblatt beim nächsten Erzeugerlauf, Spalte Berichtsort (Zweitprüfung Nr. 13): K-04.16 bis K-04.19 „T · Tab. 2“ → „A · Tab. H3“ (Tab. 2 führt nur Ausgangswerte, Prä- und Post-Werte der deskriptiven Zielgrößen stehen in Tab. H3b, Raster 5.2.5) · K-01.1 „I · Strukturprüfung“ → Text Kapitel 5, genau ein Satz, und Abb. 1 (Bezugsmengen-Regel Menge 1) · K-10.10 „A · Tab. H5“ → auch Text Kapitel 5 · K-08.8 CM und SBJ „T · 5.2 Satz, Tab. H4“ → „A · Tab. H4“ (im Text nur K-08.8 Z30, R2) · K-11.3 „I · Strukturprüfung“ → auch Text Kapitel 5 (Richtung) und Tab. H1 · Die 18 in A2 S1 ist K-10.4 (Nenner der Umsetzungsrate, „T · 5.1 Nenner“), zahlengleich mit K-01.2 aus Menge 1 der Bezugsmengen-Regel. Die Ausnahme in F17 Fassung 18 festhalten.',
    'Messskript Fassung 5: Satzenden nach Ziffern und nach Einzelbuchstaben („°C.“) erkennen, ohne Ordinalzahlen und Daten zu teilen. Bis dahin sind die „Sätze über 32“ in 4.3 und 4.5.1 als Artefakte vermerkt (§ 7.2).',
    'Skill `kapiteltext-bachelorarbeit` (G26g, G37 h): Stand 28.09. mit Gliederung v5 (Budgets 5.1 230 und 5.2 220 als Abschnitte). Nach v6 ist Kapitel 5 ein Abschnitt mit 450 Wörtern und zwei Absatzgruppen. Die drei Kapitelregeln gelten unverändert. Skill-Vorschlag im Steuerdokumente-Task.',
    'Maßnahmenliste mit Rev. 137: G29 (d) erledigt, (e) erledigt mit dem Vermerk, dass die Vorab-Prüfung an den Prä-Werten ohne eigenen Satz in der Anmerkung zu Tab. H4b steht · G32 (b) Textteil erledigt, Anmerkungen zu Tab. 2 und Tab. 3 in Task 18, (j) R5 unverändert (§ 8 Nr. 2) · G37 (d) erledigt, (e) Kapitel-5-Teil mit der Übertragung und dem Abgleich, (f) erledigt · G28g Kapitel-5-Teil erledigt (Umsetzungsrate, Untergrenzen), Untergrund und Videopausen entfallen (Umfangsdokument § 2.4) · M24 mit der Übertragung durch den Verfasser und dem Abgleich (§ 8 Nr. 4, § 11) · B5 Rest bleibt (Abb. 1).',
], 1):
    A('%d. %s' % (i, t))
A('')

# ------------------------------------------------------------------ § 10 Zweitprüfung
A('## 10 Zweitprüfung')
A('')
A(B10 if B10 else 'Ausstehend.')
A('')

# ------------------------------------------------------------------ § 11 Einbau und Abgleich
A('## 11 Einbau, Messung, Endabgleich und Rückschreibung')
A('')
A(B11 if B11 else 'Ausstehend.')
A('')
open(AUS, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print(len('\n'.join(L).split()), 'Wörter,', '\n'.join(L).count(chr(59)), 'Semikola')

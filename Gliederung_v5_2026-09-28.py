# -*- coding: utf-8 -*-
"""
Gliederung_v5_2026-09-28.py — erzeugt `01_Verfahren\\Gliederung_2026-09-28.md` (Gliederung v5)
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task Steuerdokumente 28.09. (Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 5.1)

v5 ersetzt Gliederung v4 (23.09., Rev. 2 vom 24.09.) nach dem Neuzuschnitt vom 28.09.: Kapitel 1 bis 3 werden eine Einleitung,
fünf Kapitel mit Arbeits- und Endnummern, 6.350 Wörter, höchstens 33 Seiten einschließlich Literaturverzeichnis.
Werte: Wortzahlen aus dem Messskript Fassung 3 (`Manuskriptstand_2026-09-25.csv`, `.txt`), Seiten aus `Seitenmodell_2026-09-28.csv`,
Wortzahlen der Einleitung aus dem Textvorschlag Einleitung (Kopf und Zug-Tabelle), Korpuswerte aus Fassung 17 § 5.2, Errata E1 bis E5
aus Fassung 16 § 5.1, Stand der Änderungsliste M10 bis M22 am Master geprüft. Keine Zahl von Hand, Budgets sind Festlegungen.
Aufruf: python Gliederung_v5_2026-09-28.py <F16.md> <F17.md> <Manuskriptstand.csv> <Manuskriptstand.txt> <Seitenmodell.csv>
        <Textvorschlag_Einleitung.md> <Master.docx> <Ausgabe.md> <Berichtsraster_Rev3.md> <Gliederung_v4.md>
Ohne Semikolon im Skript (chr(59)). Fassung 2 (28.09., nach der übergreifenden Zweitprüfung der Steuerdokumente und dem Klick
von 19:25 zur Verdünnungslogik): v4 nur noch Herkunft, Urteil der Anwendbarkeitsprüfung und Ä2 bis Ä10 hier, Rasterspalte in § 3.2
aus dem Berichtsraster Rev. 3, M26 (Tab. 1 nach G31 b), Wortlaut der offenen M-Punkte. Jede Ersetzung genau einmal, sonst Abbruch.
"""
import csv
import hashlib
import os
import re
import sys
from docx import Document

F16, F17, M_CSV, M_TXT, S_CSV, TV_E, MASTER, OUT, RASTER, V4 = sys.argv[1:11]
SEMI = chr(59)


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
    t = re.findall(muster, text, re.S | re.M)
    if len(t) != 1:
        raise SystemExit('Abbruch: %s %d-mal gefunden' % (name, len(t)))
    return t[0]


# ------------------------------------------------------------------ Messwerte
w = {r['arbeitsnummer']: int(r['woerter']) for r in csv.DictReader(open(M_CSV, encoding='utf-8'))}
mess = open(M_TXT, encoding='utf-8').read()
W = dict(w)
W['4.4g'] = w['4.4'] + w['4.4.1'] + w['4.4.2'] + w['4.4.3']
W['4.5g'] = w['4.5'] + w['4.5.1'] + w['4.5.2']
K4 = sum(W[k] for k in ['4.1', '4.2', '4.3', '4.4g', '4.5g', '4.6', '4.7'])
ALT = sum(w[k] for k in ['2', '2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.5', '3'])
GES = sum(v for k, v in w.items() if re.match(r'^[1-7](\.|$)', k))
MP = eins(r'Prognose Einleitung bis Ende Literaturverzeichnis: (\d+,\d) Seiten', mess, 'Prognose des Messskripts')
P = {r['parameter']: float(r['wert']) for r in csv.DictReader(open(S_CSV, encoding='utf-8'), delimiter=SEMI)}
S_TEXT = 1500 / P['dichte_einleitung'] + 4850 / P['dichte_kapitel_4_bis_7']
S_OBJ = P['objekte_textteil'] * P['seiten_je_objekt']
S_END = P['kapitelenden_textteil'] * P['seiten_je_kapitelende']
S_TT = S_TEXT + S_OBJ + S_END
S_LIT = P['eintraege_basis'] / P['eintraege_je_seite'] + P['seiten_je_kapitelende']
S_GB = S_TT + S_LIT
S_GO = S_TT + P['eintraege_obere_variante'] / P['eintraege_je_seite'] + P['seiten_je_kapitelende']
if abs(S_GB - P['prognose_gesamt_basis']) > 0.01 or abs(S_GO - P['prognose_gesamt_obere']) > 0.01:
    raise SystemExit('Abbruch: Seitenrechnung weicht vom Seitenmodell ab')

# ------------------------------------------------------------------ Textvorschlag Einleitung
tv = open(TV_E, encoding='utf-8').read()
TVW = eins(r'\| Wörter gesamt \| \*\*(\d{1,2}\.\d{3}|\d{3,4})\*\*', tv, 'Wortzahl Textvorschlag')
ZUEGE = re.findall(r'^\| (\d) ([^|]+?) \| ([^|]+?) \| (\d+) \(≈ (\d+)\) \| ([^|]+?) \| ([^|]+?) \|$', tv, re.M)
if len(ZUEGE) != 8:
    raise SystemExit('Abbruch: Zug-Tabelle des Textvorschlags hat %d statt 8 Zeilen' % len(ZUEGE))
if sum(int(z[3]) for z in ZUEGE) != int(TVW.replace('.', '')):
    raise SystemExit('Abbruch: Zugwörter summieren sich nicht zur Wortzahl des Textvorschlags')
PLAN_SUM = sum(int(z[4]) for z in ZUEGE)

# ------------------------------------------------------------------ Korpuswerte und Errata
f17 = open(F17, encoding='utf-8').read()
KORPUS = {}
for nr, name in [('1', 'Einleitung'), ('2', 'Methodik'), ('3', 'Ergebnisse'), ('4', 'Diskussion'), ('5', 'Fazit und Ausblick')]:
    KORPUS[nr] = eins(r'^\| ' + nr + ' ' + name + r' \(\d\) \| ([\d.]+) \|', f17, 'Korpuswert ' + name)
KORPUS_SUM = eins(r'^\| \*\*Σ\*\* \| \*\*([\d.]+)\*\* \| \*\*6\.350\*\* \|', f17, 'Korpussumme')
f16 = open(F16, encoding='utf-8').read()
ERRATA = eins(r'\*\*Errata zur Gliederung v4\*\* \([^\n]*?\): (E1 — [^\n]+)', f16, 'Errata E1 bis E5')

# ------------------------------------------------------------------ Stand der Änderungsliste am Master
d = Document(MASTER)
txt, cur = {}, ''
for p in d.paragraphs:
    if p.style.name.startswith('Heading'):
        cur = p.text.strip().split(' ')[0]
        continue
    txt.setdefault(cur, []).append(p.text)
T = {k: ' '.join(v) for k, v in txt.items()}
PRUEF = {
    'M10': '(Abb. 1)' not in T.get('4.3', '') and '⟨Abb. 1' not in T.get('4.3', ''),
    'M17': 'Zuteilungsverbergung' not in T.get('4.1', ''),
    'M18': SEMI not in T.get('4.1', ''),
    'M19': '174' not in T.get('4.4', '') + T.get('4.4.1', '') + T.get('4.4.2', '') + T.get('4.4.3', ''),
    'M20': 'Abschnitt 5.1' not in T.get('4.5.1', '') + T.get('4.6', ''),
    'M22': 'Abschn. 6.2' not in T.get('4.3', ''),
}
KUERZ = sum(w[k] for k in ['2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3']) - 2950
VERW_ALT = int(eins(r'davon im Altbestand Kapitel 2 und 3: \d+ Semikola, (\d+) Abschnittsverweise', mess, 'Verweise im Altbestand'))


def stand(schluessel, erledigt, offen):
    return erledigt + ' (geprüft am Master 28.09.)' if PRUEF[schluessel] else offen


# ------------------------------------------------------------------ Dokument
Z = []
Z.append('''# Gliederung v5 — fünf Kapitel, Einleitung statt Kapitel 1 bis 3

Gliederung mit Arbeits- und Endnummern, Wortbudget, Seitenmodell und Objektzuordnung, Änderungsliste für den Master

Bachelorarbeit U15-Plyometrie · DSHS Köln · Arbeitsdokument, kein Manuskripttext · Stand 28.09.2026 · ersetzt Gliederung v4 (23.09., Rev. 2 vom 24.09.), Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` · Erzeuger `03_Skripte\\Gliederung_v5_2026-09-28.py`: Wortzahlen aus dem Messskript Fassung 3, Seiten aus dem Seitenmodell, keine Zahl von Hand · steuert zusammen mit den Projektanweisungen Fassung 17 (§ 5.1 bis § 5.3, § 5a) und gilt als revidierbare Arbeitsfestlegung

## 0 Ergebnis in Kürze

1. **Fünf Kapitel.** 1 Einleitung · 2 Methodik · 3 Ergebnisse · 4 Diskussion · 5 Fazit und Ausblick. Kapitel 1 bis 3 der v4 gehen in einer Einleitung ohne Unterabschnitte mit höchstens 1.500 Wörtern auf (Verfasser 28.09., 14:38, Klick 14:57). Die Vorgabe des SMK-Leitfadens, den Forschungsstand in einem eigenen Kapitel zu beschreiben (Abschn. 4.1), ist bewusst nicht erfüllt.
2. **Umfang.** Höchstens 6.350 Wörter Absatztext und höchstens 33 Seiten von der Einleitung bis zum Ende des Literaturverzeichnisses, ohne Vorspann und Anhang (Verfasser 28.09., 15:14, Klick K1). Regel R6 entfällt (K2), die Tauschregel greift ab 32 Seiten (K3). Die Seitenprognose ist eine Modellrechnung: %(gb)s Seiten mit vollen Budgets, %(mp)s mit den am 28.09. gemessenen Wörtern (§ 3.4).
3. **Arbeitsnummern bis Task 18.** Methodik bis Fazit behalten im Master und in allen Steuerdokumenten, Skripten und Textvorschlägen die Nummern 4 bis 7. Umnummeriert wird einmal per Skript in Task 18 (Ä13, M25).
4. **Stand.** Kapitel 4 ist textlich fertig (%(k4)s Wörter gegen 2.550). Die Einleitung liegt als Textvorschlag vor (%(tvw)s Wörter, Task 7 neu, Teil 0 Rev. 114), die Übertragung in den Master steht aus (M24). Ergebnisse, Diskussion und Fazit sind leer.
5. **Unverändert aus v4.** Kapitel 4 bis 7 in Nummern, Namen und Folge, die fünf Objekte im Text, Anhang A bis H, die Anwendbarkeitsprüfung und die CONSORT-Abbildung (v4 § 2, im Archiv). CONSORT 2a und 2b liegen jetzt vollständig in der Einleitung.

## 1 Grundlagen

Projektanweisungen Fassung 17 · Übergabe Einleitung (`04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md`, Bauplan § 3) · Textvorschlag Einleitung (`04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md`, Zug-Tabelle § 2, Verbleibsliste § 4) · Messskript `03_Skripte\\Manuskriptstand_2026-09-25` Fassung 3 (Messung 28.09.) · Seitenmodell `03_Skripte\\Seitenmodell_2026-09-28` · Gliederung v4 im Archiv mit Anwendbarkeitsprüfung (§ 2), Änderungen Ä1 bis Ä11 (§ 4), Änderungsliste M1 bis M23 (§ 5) und den Klickfragen vom 23.09. (§ 6).

## 2 Anwendbarkeit

Die Anwendbarkeitsprüfung der v4 gilt weiter: Die Berichtsstruktur folgt randomisierten kontrollierten Studien, das Design bleibt eine quasi-experimentelle, kontrollierte Prä-Post-Feldstudie mit nicht äquivalenter Kontrollgruppe (v4 § 2.2). In der CONSORT-Abbildung (v4 § 2.3) wandern 2a (Hintergrund) und 2b (Ziele und Hypothesen) aus Kapitel 1 und 3 in die Einleitung, alle übrigen Items behalten ihren Ort. Mit der Einleitung ist die Arbeit gebaut wie der Korpus, der Theorie und Forschungsstand in der Einleitung trägt (Bauplan § 7.1).

## 3 Gliederung v5

### 3.1 Übersicht

Budget nach Fassung 17 § 5.2. Ist = Messung am Master vom 28.09. (Messskript Fassung 3), vor der Übertragung der Einleitung. Objekte nach Fassung 17 § 5.3.

| Arbeitsnr. | Endnr. | Titel | Budget | Ist 28.09. | Objekte | Bauform und Anspruch |
|---|---|---|---:|---:|---|---|
| — | — | Vorspann: Titelblatt · Eidesstattliche Erklärung mit KI-Deklaration · Zusammenfassung · Abstract · Inhalts-, Abkürzungs-, Abbildungs-, Tabellenverzeichnis | — | Gerüst | — | DSHS, CONSORT 1a, 1b |
| 1 | 1 | Einleitung | 1.500 | %(alt)s im Altbestand, Textvorschlag %(tvw)s | — | Trichter in acht Zügen (§ 3.2), Schluss mit den Hypothesen, CONSORT 2a, 2b, SMK Abschn. 4.1 bewusst nicht erfüllt |
| 4 | 2 | Methodik | 2.550 | %(k4)s | Tab. 1 | Korpusfolge Design → Stichprobe → Ablauf → Tests → Intervention → Statistik |
| 4.1 | 2.1 | Studiendesign | 300 | %(w41)s | — | Design, Zeitraum, Zuteilung, Gruppen, Zielgrößen, Standards, Protokoll, Abweichungen als Sammelsatz mit Erstverweis auf Tab. H6 (Task 18), ohne Zwecksatz (K6) (CONSORT 3a, 3b, 23, 24, 25) |
| 4.2 | 2.2 | Stichprobe | 215 | %(w42)s | — | Zielpopulation, Tier 2 nach Wettkampfebene, Rekrutierung, Analysepopulation mit Kennwerten, Kriterien, Votum (CONSORT 4a, 4b) |
| 4.3 | 2.3 | Untersuchungsablauf | 340 | %(w43)s | — | Phasen, Standardisierung, Familiarisierung, Anthropometrie und %%PAH, Erwärmung (Anhang C), Testreihenfolge, Pausenregel beim Standweitsprung, Testleitung rollenweise, Termine für Abb. H7 vorgemerkt (CONSORT 11a) |
| 4.4 | 2.4 | Leistungsdiagnostik (4.4.1 bis 4.4.3) | 420 | %(w44)s | Tab. 1 | Testkette je Zielgröße mit Aggregationsregel und 505-Regel, Versuchsausfälle in einem Satz (Tab. H1), Messgüte als Tabelle (CONSORT 6a) |
| 4.5 | 2.5 | Trainingsintervention (4.5.1, 4.5.2) | 570 | %(w45)s | — | TIDieR 1 bis 10 |
| 4.5.1 | 2.5.1 | Plyometrisches Heimtrainingsprogramm | 420 | %(w451)s | — | ein Absatz je Baustein, Auslieferung (TIDieR 6) |
| 4.5.2 | 2.5.2 | Vergleichs- und Begleitbedingung | 150 | %(w452)s | — | drei Vereine, Details in Anhang D (CONSORT 5) |
| 4.6 | 2.6 | Adhärenz- und Belastungsmonitoring | 155 | %(w46)s | — | Instrument, Zählregel, sRPE-Load als CR-10 mal Solldauer, Kontrollgruppe ohne Instrument (TIDieR 11) |
| 4.7 | 2.7 | Statistische Auswertung | 550 | %(w47)s | — | Analysepopulation → Fallzahl mit Sensitivitäts-Poweranalyse → Kovarianzanalyse mit Kovariatenbegründung und Entscheidungsregel → Voraussetzungen an den Residuen (O7) → Sensitivitäten mit Bootstrap als streichbarem Modul (Tab. H4) → Datenprüfung, R 4.3.3, Anhang G (CONSORT 7a, 12a, 12b, 16) |
| 5 | 3 | Ergebnisse | 450 | %(w5)s | Abb. 1, Tab. 2, Abb. 2, Tab. 3 | nicht zitieren, nicht deuten, Zahlen in den Objekten |
| 5.1 | 3.1 | Teilnehmerfluss, Adhärenz und Ausgangswerte | 230 | %(w51)s | Abb. 1, Tab. 2 | Orientierungszug: Fluss bis zur Analysepopulation, Ausgangswerte mit d und Überlappung, Umsetzung (Tab. H2), Schwellenlandschaft (Tab. H5), unerwünschte Ereignisse (CONSORT 13a, 13b, 15, 19, TIDieR 12) |
| 5.2 | 3.2 | Gruppenvergleiche je Zielgröße | 220 | %(w52)s | Abb. 2, Tab. 3 | je Zielgröße Richtung und Fall der Schlusslogik mit Konfidenzintervall, keine Cohen-Klasse, deskriptive Zielgrößen (Tab. H3), Voraussetzungen „geprüft und nicht verworfen“, verworfene mit Zahl, Sensitivitäten in einem Satz (Tab. H4) (CONSORT 16, 17a, 18) |
| 6 | 4 | Diskussion | 1.600 | %(w6)s | — | Vorlage Sammoud |
| 6.1 | 4.1 | Einordnung der Ergebnisse | 700 | %(w61)s | — | Eröffnung mit dem Ankersatz aus der Einleitung → Hauptbefund → Gegenbefund, dann je Zielgröße ein Absatz (CONSORT 20, 22) |
| 6.2 | 4.2 | Methodendiskussion | 400 | %(w62)s | — | Verdünnung, Auflösung, Planungsmodell der Antragsrechnung, Familienfehler, Trennschärfe, Analyseeinheit, Begleitbedingungen in beide Richtungen, Methodenwahl beim Reifestatus |
| 6.3 | 4.3 | Stärken und Limitationen | 500 | %(w63)s | — | Stärken → Scharniersatz → acht Gruppen G1 bis G8, fehlende unabhängige Methodenprüfung genau einmal (CONSORT 20, 21) |
| 7 | 5 | Fazit und Ausblick | 250 | %(w7)s | — | ein Absatz, Präventions-Satzteil im Ausblick ohne Quelle (SMK Abschn. 4.1) |
| — | — | Literaturverzeichnis · Anhang A bis H (§ 3.3) | — | Gerüst | Tab. C1, C2, H1 bis H6, Abb. H7 | dvs 2020, das Verzeichnis zählt zur Seitengrenze (K1) |
| **Σ** | | **Kapitel 1 bis 5** | **6.350** | **%(ges)s mit Altbestand** | **5 im Text** | |
''' % dict(gb=de(S_GB, 1), mp=MP, k4=de(K4), tvw=TVW, alt=de(ALT), ges=de(GES), w41=W['4.1'], w42=W['4.2'], w43=W['4.3'],
           w44=W['4.4g'], w45=de(W['4.5g']), w451=W['4.5.1'], w452=W['4.5.2'], w46=W['4.6'], w47=W['4.7'], w5=W['5'],
           w51=W['5.1'], w52=W['5.2'], w6=W['6'], w61=W['6.1'], w62=W['6.2'], w63=W['6.3'], w7=W['7']))

zeilen = []
for nr, name, ort, ist, plan, raster, abw in ZUEGE:
    zeilen.append('| %s %s | %s | %s | %s | %s | %s |' % (nr, name.strip(), plan, ist, raster.strip(), ort.strip(), abw.strip()))
Z.append('''### 3.2 Einleitung — Trichter in acht Zügen

Bauplan nach Übergabe Einleitung § 3, umgesetzt im Textvorschlag Einleitung (Zug-Tabelle § 2 dort). Die Satzkerne sind Inhalt, kein Wortlaut. Wörter geplant und im Textvorschlag gemessen, Raster nach Berichtsraster Rev. 3, Kopfblock „Einleitung“.

| Zug | geplant | Textvorschlag | Raster | Absatz, Sätze | Abweichung vom Bauplan und Grund (Wortlaut der Zug-Tabelle im Textvorschlag) |
|---|---:|---:|---|---|---|
%s
| **Σ** | **≈ %s** | **%s** | | 9 Absätze | nicht aufgefüllt |

**Ankersatz.** Der Zweck ist der Ankersatz. Sein Wortlaut ist entschieden: „… gegenüber einer Kontrollgruppe verbessert“ statt „erhält oder verbessert“ des Antrags (Klick in Task 7 neu, Textvorschlag Einleitung § 7). Er kehrt im Eröffnungsabsatz von 6.1 und in der Zusammenfassung nahezu wörtlich wieder, 4.1 bleibt ohne Zwecksatz (Klick K6, 28.09., 16:27).

**Hypothesen.** H0 und H1 nah am Wortlaut des Ethikantrags („in mindestens einem der erhobenen Parameter“), einander ergänzend, auf die Grundgesamtheit bezogen, drei Zielgrößen gleichrangig, Reihenfolge Sprint → Richtungswechsel → Sprung (G32 e).

**Nicht in der Einleitung:** eigene Studienzahlen · Testabläufe (4.3, 4.4) · Kovariatenbegründung (4.7) · die Methodenwahl beim Reifestatus (vorgemerkt für 6.2, Klick in Task 7 neu) · Effektstärken als Pflicht, der Forschungsstand bleibt qualitativ · Präventionsaussagen über das eigene Programm (Befund Relevanz Rev. 2 § 4.3 und § 4.4).
''' % ('\n'.join(zeilen), de(PLAN_SUM), TVW))

Z.append('''### 3.3 Vorspann und Nachspann

**Vorspann** (Reihenfolge nach DSHS, Fassung 17 § 9): Titelblatt (Design im Titel, CONSORT 1a) · Eidesstattliche Erklärung mit KI-Deklaration im Wortlaut der DSHS-Leitlinie vom 26.03.2025 (Fassung 17 § 14) · Zusammenfassung · Abstract · Inhaltsverzeichnis · Abkürzungsverzeichnis · Abbildungsverzeichnis · Tabellenverzeichnis. Zusammenfassung und Abstract inhaltsgleich, je 200 bis 300 Wörter, nach der CONSORT-Abstract-Checkliste, als durchlaufender Block ohne Struktur-Label (Klick 7, 23.09.), keine Belege. Die Zusammenfassung wiederholt den Ankersatz (K6). Nicht im Wortbudget und nicht in der Seitengrenze (K1).

**Nachspann:** Literaturverzeichnis nach dvs 2020 (Fassung 17 § 8), es zählt zur Seitengrenze (K1). Dann der Anhang, der nicht auf den Umfang zählt und alle Objekte aufnimmt, die Fassung 17 § 5.3 auslagert.

| Anhang | Inhalt | Erstverweis im Text |
|---|---|---|
| A | Fragebogen A (SoSci Survey), Itemkatalog | 4.6 |
| B | Übungs- und Videoübersicht | 4.5.1 |
| C | Standardisiertes Aufwärmprogramm der Testtage (Tab. C1, C2) | 4.3 |
| D | Vereins-Sommerprogramme (anonymisierte Auszüge, Verein A ohne Plandokument, Task 17) | 4.5.2 |
| E | Ethikvotum und Ethikantrag (Studienprotokoll, CONSORT 24) | 4.1 |
| F | Einverständniserklärung und Erhebung der Elternhöhen | 4.2 |
| G | Sensitivitäts-Poweranalyse mit allen Eingaben, R-Skripte als KI-erzeugt gekennzeichnet, Q-Q- und Linearitätsdiagramme, ohne Prüfprotokolle (Verfasser 26.09., Fassung 17 § 14, CONSORT 7a) | 4.7 |
| H | Ergänzende Tabellen: H1 Versuche, Ausfälle und Messgüte je Verein · H2 Umsetzung · H3 Ausgangswerte aller Eingangsgetesteten und deskriptive Zielgrößen · H4 Modell und Robustheit · H5 Schwellenlandschaft der Mindestdosis · H6 Abweichungsregister · Abb. H7 Zeitstrahl der Termine | H1 4.4 · H2 und H5 5.1 · H3 5.2 · H4 4.7 · H6 4.1 (Task 18) · H7 4.3 |

Kein Rohdatenanhang, der pseudonymisierte Datenstand wird auf Anfrage bereitgestellt (Klick 6, 23.09.).
''')

KT = S_TEXT
Z.append('''### 3.4 Wortbudget und Seitenmodell

Hartgrenze 6.350 Wörter Absatztext der Kapitel 1 bis 5 (Fassung 17 § 1.1, § 5.2).

| Kapitel (Arbeitsnummer) | Korpus Ø | Budget |
|---|---:|---:|
| 1 Einleitung (1) | %(k1)s | 1.500 |
| 2 Methodik (4) | %(k2)s | 2.550 |
| 3 Ergebnisse (5) | %(k3)s | 450 |
| 4 Diskussion (6) | %(k4k)s | 1.600 |
| 5 Fazit und Ausblick (7) | %(k5)s | 250 |
| **Σ** | **%(ks)s** | **6.350** |

**Unterbudgets (Vorgabe, Klick 5 vom 23.09., verbindlich seit 25.09.):** 4.1 300 · 4.2 215 · 4.3 340 · 4.4 420 · 4.5.1 420 · 4.5.2 150 · 4.6 155 · 4.7 550 · 5.1 230 · 5.2 220 · 6.1 700 · 6.2 400 · 6.3 500 · 7 250. Die Einleitung hat kein Unterbudget. Nicht verbrauchte Wörter werden nicht aufgefüllt und gehen nicht auf andere Abschnitte über.

**Seitenmodell — Modellrechnung, keine Messung** (`03_Skripte\\Seitenmodell_2026-09-28`, Zählweise K1):

| Posten | Seiten | Art |
|---|---:|---|
| Text: Einleitung 1.500 Wörter bei %(de)s je Seite, Methodik bis Fazit 4.850 bei %(dr)s | %(st)s | Modellrechnung, Dichten am Master gemessen |
| fünf Objekte zu je %(so1)s Seiten | %(so)s | Modellrechnung, Annahme |
| fünf Kapitelenden zu je %(se1)s Seiten | %(se)s | Modellrechnung, Erwartungswert |
| **Textteil** | **%(tt)s** | Modellrechnung |
| Literaturverzeichnis, %(nb)d Einträge bei %(js)s je Seite und die letzte Seite | %(sl)s | Modellrechnung, Einträge geschätzt |
| **Einleitung bis Ende des Literaturverzeichnisses** | **%(gb)s** | Modellrechnung, Budgetprognose |
| obere Variante mit %(no)d Einträgen | %(go)s | Modellrechnung |
| mit den am 28.09. gemessenen Wörtern (Messskript, Block „Seitenschätzung“) | %(mp)s | Modellrechnung, steuernd |
| Schwelle der Tauschregel (K3) · Grenze des Verfassers · Grenze des Betreuers | 32 · 33 · 37 | Festlegung |

Steuernd ist die jüngste Prognose des Messskripts. Kontrolle ist die Word-Messung nach Ergebnissen und Diskussion und nach dem Literaturverzeichnis (Task 15). Regel R6 (unter 30 Seiten Anhangsobjekte in den Textteil holen) entfällt (K2), Fließtext wird nie aufgefüllt.
''' % dict(k1=KORPUS['1'], k2=KORPUS['2'], k3=KORPUS['3'], k4k=KORPUS['4'], k5=KORPUS['5'], ks=KORPUS_SUM,
           de=de(P['dichte_einleitung']), dr=de(P['dichte_kapitel_4_bis_7']), st=de(KT, 1), so1=de(P['seiten_je_objekt'], 1),
           so=de(S_OBJ, 1), se1=de(P['seiten_je_kapitelende'], 1), se=de(S_END, 1), tt=de(S_TT, 1), nb=int(P['eintraege_basis']),
           js=de(P['eintraege_je_seite'], 1), sl=de(S_LIT, 1), gb=de(S_GB, 1), no=int(P['eintraege_obere_variante']),
           go=de(S_GO, 1), mp=MP))

Z.append('''### 3.5 Objekte

Fünf Objekte im Textteil (Umfangsdokument § 3.2, Verfasser 24.09., unverändert gegenüber v4): Tab. 1 Messgüte je Zielgröße (4.4) · Abb. 1 Teilnehmerfluss (5.1) · Tab. 2 Stichprobe und Ausgangswerte, ohne die Kennwerte der Stichprobe, die in 4.2 stehen (5.1) · Abb. 2 Ausgangswerte und reifeadjustierte Abschlusswerte (5.2, nach Vickers & Altman, 2001) · Tab. 3 Gruppenvergleich der drei konfirmatorischen Zielgrößen (5.2). Spalten nach Fassung 17 § 5.3. Eingesetzt werden die Objekte in Task 18, wenn der Text steht (Verfasser 25.09., 22:25). Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter, den für Tab. 1 setzt Task 18 nach G31 (a).

**Tauschregel** (Fassung 17 § 5.3, K3): Ein Objekt kostet nach Annahme rund 0,4 Seiten. Die fünf Objekte kosten keine Wörter. Ein weiteres Objekt kostet Wörter, sobald die Seitenprognose 32 Seiten erreicht. Alles Weitere steht in Anhang H mit je einem zusammenfassenden Satz im Text. Jeder Objektverweis wird vor der Abgabe gegen das Objekt geprüft (Bauplan § 8).
''')

Z.append('''## 4 Änderungen gegenüber v4 — Begründung und Alternative

| Nr. | Änderung | Begründung | Alternative | Entscheidung |
|---|---|---|---|---|
| Ä12 | Kapitel 1 bis 3 → eine Einleitung ohne Unterabschnitte, höchstens 1.500 Wörter | Kapitel 2 hätte nach dem alten Budget von 2.950 Wörtern um %(kuerz)s Wörter gekürzt werden müssen, ohne dass ein Berichtsstandard die Länge trug. Die Zeitschriftenartikel des Korpus tragen Theorie und Forschungsstand in der Einleitung (Bauplan § 7.1). Die Arbeit wird kürzer und folgt dem Korpus | Kapitel 2 nach Plan kürzen (Tasks 7 bis 10), Kapitel 1 und 3 neu schreiben | Verfasser 28.09., 14:38, Klick 14:57 |
| Ä13 | Umnummerierung Methodik 4 → 2 bis Fazit 7 → 5 erst in Task 18, bis dahin Arbeitsnummern | Eine Umnummerierung mitten in der Arbeit bräche die Verweise in Steuerdokumenten, Berichtsraster, Skripten und Textvorschlägen | sofort umnummerieren | G35 (d), Rev. 112 |

Aus v4: Ä1 (Name von Kapitel 3) und Ä11 (Titel von 2.5) sind mit Ä12 gegenstandslos. Ä2 bis Ä10 gelten weiter (v4 § 4, Archiv).
''' % dict(kuerz=de(KUERZ)))

Z.append('''## 5 Änderungsliste für den Master

Nummerierte Vorschlagsliste nach Fassung 17 § 1.2. Kein Einbau in diesem Task.

| Nr. | Fundstelle | Neufassung | Begründung | Zeitpunkt |
|---|---|---|---|---|
| M24 | Überschriften „2 Theoretischer Hintergrund und Forschungsstand“, 2.1 bis 2.5 mit 2.4.1 bis 2.4.3 und „3 Fragestellung und Hypothesen“ samt Text | löschen, die neun Absätze des Textvorschlags Einleitung unter „1 Einleitung“ setzen, Verzeichnisse mit F9 aktualisieren | Ä12 | Verfasser, nach Task 7 neu (Textvorschlag Einleitung § 0) |
| M25 | Überschriften der Methodik bis zum Fazit | Umnummerierung 4 → 2, 5 → 3, 6 → 4, 7 → 5 mit allen Unterabschnitten, per Skript in Master, Steuerdokumenten, Skripten und Textvorschlägen, danach F9 | Ä13 | Task 18 (G35 d) |

**Stand der Änderungsliste aus v4** (M1 bis M23, Wortlaut in v4 § 5):

| Nr. | Stand |
|---|---|
| M1 bis M8, M14, M15 | im Master (Fassung 16 § 5.1) |
| M9 | gegenstandslos mit M24 |
| M10 | %(m10)s |
| M11, M12 | offen, Task 18 (Objekte erst nach dem Text, Verfasser 25.09., 22:25) |
| M13 | offen, vor der Abgabe (Task 18) |
| M16 | offen, Task 13 (Zusammenfassung und Abstract) |
| M17 | %(m17)s |
| M18 | %(m18)s |
| M19 | %(m19)s |
| M20 | %(m20)s |
| M21 | gegenstandslos mit M24, alle %(verw)d Abschnittsverweise stehen im Altbestand (Messskript) |
| M22 | %(m22)s |
| M23 | für die Einleitung gegenstandslos (Textvorschlag), für die übrigen leeren Abschnitte optional |
''' % dict(m10=stand('M10', 'erledigt, 4.3 ohne „(Abb. 1)“ und ohne Platzhalter', 'offen'),
           m17=stand('M17', 'erledigt, 4.1 ohne den Satz zur Zuteilungsverbergung', 'offen'),
           m18=stand('M18', 'erledigt, 4.1 ohne Semikolon', 'offen'),
           m19=stand('M19', 'erledigt, 4.4 ohne die Ausfallzahlen', 'offen'),
           m20=stand('M20', 'erledigt, 4.5.1 und 4.6 ohne Verweissatz auf 5.1', 'offen'),
           m22=stand('M22', 'erledigt, 4.3 ohne Abschnittsverweis', 'offen'), verw=VERW_ALT))

Z.append('''## 6 Herkunft

- **Gliederung v4** vom 23.09.2026 (Rev. 2 vom 24.09.), im Archiv. Klickantworten vom 23.09., alle mit der Empfehlung (Fassung 16 § 5.1): 1 Name von Kapitel 3 (gegenstandslos mit Ä12) · 2 Struktur Kapitel 5 und 6 (gilt) · 3 Praktische Implikationen in Kapitel 7 (gilt) · 4 Kapitel 7 ohne Unterabschnitte (gilt) · 5 Unterbudgets Kapitel 4 bis 7 (gilt, Vorgabe seit 25.09.) · 6 kein Rohdatenanhang (gilt) · 7 Zusammenfassung als durchlaufender Block (gilt).
- **Errata zur Gliederung v4** (Prüfprotokoll `05_Protokolle\\Pruefprotokoll_Gliederung_2026-09-23` § 2, übernommen mit Fassung 15, G27a): %(errata)s
- **Entscheidungen vom 28.09.2026:** Neuzuschnitt (Verfasser 14:38, Klick 14:57) · Seitengrenze 33 Seiten einschließlich Literaturverzeichnis (15:14) · Zählweise, Regel R6, Tauschregel und Ankersatz (Klicks K1, K2, K3 und K6, 16:27) · Textvorschlag Einleitung mit Verbleibsliste und Wortlaut des Zwecks (Task 7 neu, Rev. 114). Uhrzeiten nach der Sitzungsuhr (Fassung 17 § 1.2).

## 7 Prüfung

Prüfskript `03_Skripte\\Steuerdokumente_Pruefung_2026-09-28.py` mit Ausgabe `.txt`: kein Semikolon außer in der Zitiersyntax, Budgetarithmetik, Verweise auf Paragrafen dieses Dokuments. Wortzahlen aus dem Messskript, Seiten aus dem Seitenmodell, Stand von M10 bis M22 am Master (%(gr)s Byte, MD5 %(md5)s…) per Skript geprüft.
''' % dict(errata=ERRATA, gr=de(os.path.getsize(MASTER)), md5=hashlib.md5(open(MASTER, 'rb').read()).hexdigest()[:8]))

text = '\n'.join(Z)
text = re.sub(r'\n{3,}', '\n\n', text)

# ------------------------------------------------------------------ Fassung 2: übergreifende Zweitprüfung (Befunde 3, 4, 17, 25, 31, 32) und Klick 19:25
LOGV = []


def rp(alt, neu):
    global text
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Abbruch (Fassung 2): %d Treffer für: %s' % (n, alt[:90]))
    text = text.replace(alt, neu)
    LOGV.append(alt[:60])


# Befund 17: v4 ist nur noch Herkunft, gültige Inhalte stehen hier
rp('die Anwendbarkeitsprüfung und die CONSORT-Abbildung (v4 § 2, im Archiv).',
   'das Urteil der Anwendbarkeitsprüfung (§ 2) und die CONSORT-Zuordnung je Item (Berichtsraster Rev. 3 § 2.1).')
rp('· Gliederung v4 im Archiv mit Anwendbarkeitsprüfung (§ 2), Änderungen Ä1 bis Ä11 (§ 4), Änderungsliste M1 bis M23 (§ 5) und den Klickfragen vom 23.09. (§ 6).',
   '· Gliederung v4 als Herkunft (im Archiv, nicht mehr Grundlage): Das Urteil der Anwendbarkeitsprüfung, die weiter gültigen Änderungen Ä2 bis Ä10, der Wortlaut der offenen Punkte aus M1 bis M23 und die Klickantworten vom 23.09. stehen in diesem Dokument (§ 2, § 4, § 5, § 6).')
i0 = text.index('## 2 Anwendbarkeit\n')
i1 = text.index('## 3 Gliederung v5\n')
text = text[:i0] + '''## 2 Anwendbarkeit

**Urteil (aus v4 § 2.2, ohne die Zahlen der ersten Rechnung).** Die Arbeit hat alles, was einen kontrollierten Zwei-Gruppen-Versuch mit Prä-Post-Messung ausmacht: ein vorab festgelegtes Protokoll, eine vorab festgelegte Kontrollbedingung, vorab definierte Zielgrößen mit standardisierten Tests, eine vor der Abschlusstestung der Kontrollgruppe festgelegte Hauptanalyse mit gekennzeichneten nachträglichen Festlegungen (Fassung 17 § 1.5), Teilnehmerfluss, Adhärenzmonitoring, erfasste unerwünschte Ereignisse und Effektschätzer mit Konfidenzintervall. Das rechtfertigt, Bauform und Berichtsstandard des RCT zu übernehmen. Sie ist trotzdem kein RCT. Die Zufallszuteilung fehlt, zugeteilt wurde auf Vereinsebene in der Reihenfolge der Zusagen. Die Gruppen sind nicht äquivalent (Jahrgang, Reifestatus, Ausgangswerte, Tab. 2), dazu kommen drei Cluster ohne modellierbare Clusterstruktur, keine verblindete Rolle und eine unbeaufsichtigte Intervention. Übernommen werden deshalb Kapitelfolge, Abschnittsfolge der Methodik, die drei Ergebnisregeln, die Diskussionseröffnung und die Limitationskette, nicht das Etikett: Berichtet wird „in Anlehnung an“ CONSORT 2010, TREND wird nicht genannt (Fassung 17 § 4). Die Sätze, die den Unterschied tragen, gehören in 4.1, 4.7 und 6.2.

**CONSORT-Zuordnung.** Item für Item im Berichtsraster Rev. 3 § 2.1. Mit der Einleitung wandern 2a (Hintergrund) und 2b (Ziele und Hypothesen) aus Kapitel 1 und 3 in die Einleitung, alle übrigen Items behalten ihren Ort. Mit der Einleitung ist die Arbeit gebaut wie der Korpus, der Theorie und Forschungsstand in der Einleitung trägt (Bauplan § 7.1).

''' + text[i1:]
LOGV.append('§ 2 Anwendbarkeit')
v4 = open(V4, encoding='utf-8').read()
b4 = v4[v4.index('## 4 Änderungen gegenüber v3'):v4.index('## 5 Änderungsliste für den Master')]
ae = [z for z in b4.split('\n') if re.match(r'^\| Ä(\d+) \|', z) and 2 <= int(re.match(r'^\| Ä(\d+) \|', z).group(1)) <= 10]
if len(ae) != 9:
    raise SystemExit('Abbruch: Ä2 bis Ä10 in v4 § 4 nicht vollständig (%d Zeilen)' % len(ae))
ae = [z.replace(SEMI + ' ', ' · ').replace(SEMI, ' ·') for z in ae]
rp('|---|---|---|---|---|\n| Ä12 |', '|---|---|---|---|---|\n' + '\n'.join(ae) + '\n| Ä12 |')
rp('Aus v4: Ä1 (Name von Kapitel 3) und Ä11 (Titel von 2.5) sind mit Ä12 gegenstandslos. Ä2 bis Ä10 gelten weiter (v4 § 4, Archiv).',
   'Ä2 bis Ä10 aus v4 § 4 gelten weiter und stehen oben im Wortlaut der v4 (Semikola durch „·“ ersetzt, Verweise auf F13 und auf Paragrafen des damaligen Berichtsrasters historisch). Ä1 (Name von Kapitel 3) und Ä11 (Titel von 2.5) sind mit Ä12 gegenstandslos.')
# Befund 31: Inhaltsspalte mit Verweis auf das Raster, Klick 19:25 zur Verdünnungslogik
rp('(CONSORT 13a, 13b, 15, 19, TIDieR 12) |', '(CONSORT 13a, 13b, 14b, 15, 19, TIDieR 12), dazu gültige Versuche und TE post, vollständig im Berichtsraster § 3.12 |')
rp('Sensitivitäten in einem Satz (Tab. H4) (CONSORT 16, 17a, 18) |', 'Sensitivitäten in einem Satz (Tab. H4) (CONSORT 16, 17a, 18), vollständig im Berichtsraster § 3.13 |')
rp('Eröffnung mit dem Ankersatz aus der Einleitung → Hauptbefund → Gegenbefund, dann je Zielgröße ein Absatz (CONSORT 20, 22) |',
   'Eröffnung mit dem Ankersatz aus der Einleitung → Hauptbefund → Gegenbefund, Verdünnungslogik als Einordnung des Hauptbefunds (Klick 28.09., 19:25), dann je Zielgröße ein Absatz (CONSORT 20, 22) |')
rp('| Verdünnung, Auflösung, Planungsmodell der Antragsrechnung, Familienfehler, Trennschärfe, Analyseeinheit, Begleitbedingungen in beide Richtungen, Methodenwahl beim Reifestatus |',
   '| u. a. Auflösung, Planungsmodell der Antragsrechnung, Familienfehler, Trennschärfe, Analyseeinheit, Begleitbedingungen in beide Richtungen, Methodenwahl beim Reifestatus, vollständig im Berichtsraster § 3.14 (6.2.1 bis 6.2.12), ohne eigenen Absatz zur Verdünnung |')
rp('fehlende unabhängige Methodenprüfung genau einmal (CONSORT 20, 21) |',
   'fehlende unabhängige Methodenprüfung genau einmal, Verdünnung als Limitation in G3, Kurzform des Abweichungsregisters (CONSORT 20, 21), vollständig im Berichtsraster § 3.14 |')
# Befund 32: Rasterspalte in § 3.2 aus dem Berichtsraster Rev. 3
ra = open(RASTER, encoding='utf-8').read()
kb = ra[ra.index('### 3.1 Einleitung'):ra.index('**Nicht hier:**', ra.index('### 3.1 Einleitung'))]
ort_zug = {}
for nr, name, ort, ist, plan, raster, abw in ZUEGE:
    for a_ in re.findall(r'A(\d)', ort):
        ort_zug.setdefault(a_, set()).add(int(nr))
zug_zeilen = {}
for z in kb.split('\n'):
    m = re.match(r'^\| ((?:\d\.\d)|(?:E\.\d)) \|', z)
    if not m:
        continue
    letzte = z.rstrip(' |').split('|')[-1]
    zuege = [int(x) for x in re.findall(r'(?:Zug|Züge) (\d)(?: und (\d))?', letzte) for x in x if x]
    if not zuege:
        zuege = sorted(set(n for a_ in re.findall(r'A(\d)', letzte) for n in ort_zug.get(a_, set())))
    for n in zuege:
        zug_zeilen.setdefault(n, []).append(m.group(1))
if sorted(zug_zeilen) != list(range(1, 9)):
    raise SystemExit('Abbruch: Rasterzeilen nicht allen acht Zügen zugeordnet (%s)' % sorted(zug_zeilen))
for nr, name, ort, ist, plan, raster, abw in ZUEGE:
    alt_z = '| %s %s | %s | %s | %s | %s | %s |' % (nr, name.strip(), plan, ist, raster.strip(), ort.strip(), abw.strip())
    neu_z = '| %s %s | %s | %s | %s | %s | %s |' % (nr, name.strip(), plan, ist, ' · '.join(zug_zeilen[int(nr)]), ort.strip(), abw.strip())
    rp(alt_z, neu_z)
rp('Wörter geplant und im Textvorschlag gemessen, Raster nach Berichtsraster Rev. 3, Kopfblock „Einleitung“.',
   'Wörter geplant und im Textvorschlag gemessen, Rasterzeilen per Skript aus dem Berichtsraster Rev. 3 (Kopfblock „Einleitung“, letzte Spalte), bei Zeilen ohne Zug über den Absatz.')
# Befund 4: Tab. 1 nach G31 (b), ohne Platzhalter
rp('Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter, den für Tab. 1 setzt Task 18 nach G31 (a).',
   'Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter. Tab. 1 setzt Task 18 direkt nach G31 (b), der Platzhalter aus G31 (a) entfällt (M26).')
# Befund 25 und 3: M25, M26, offene M-Punkte mit Wortlaut
rp('per Skript in Master, Steuerdokumenten, Skripten und Textvorschlägen, danach F9 | Ä13 | Task 18 (G35 d) |',
   'per Skript in Master, Steuerdokumenten, Skripten und Textvorschlägen, danach F9. Vorher die Zeilen des Kopfblocks Einleitung im Berichtsraster auf das Präfix E umstellen (E1.1 bis E3.5, neben E.1 und E.2), damit sie nicht mit den Abschnitten 2.x und 3.x kollidieren | Ä13 | Task 18 (G35 d) |\n'
   '| M26 | 4.4, nach dem dritten Vorspann-Absatz („Je Zielgröße zeigt Tab. 1 den …“) | Tab. 1 Messgüte je Zielgröße mit Beschriftung als Feld und Anmerkung aus Textvorschlag 4.4 § 9, ohne vorherigen Platzhalter | G31 (b), Fassung 17 § 5.3 | Task 18 |')
rp('**Stand der Änderungsliste aus v4** (M1 bis M23, Wortlaut in v4 § 5):', '**Stand der Änderungsliste aus v4** (M1 bis M23, die offenen Punkte mit Wortlaut):')
rp('| M11, M12 | offen, Task 18 (Objekte erst nach dem Text, Verfasser 25.09., 22:25) |',
   '| M11 | offen, Task 18: Abb. 1 Teilnehmerfluss und Tab. 2 Stichprobe und Ausgangswerte (ohne die Kennwerte der Stichprobe) in 5.1, Beschriftung als Feld, Spaltenvertrag nach Umfangsdokument § 3.2, vorher keine Platzhalter (Fassung 17 § 5.3, Verfasser 25.09., 22:25) |\n'
   '| M12 | offen, Task 18: Abb. 2 Ausgangswerte und reifeadjustierte Abschlusswerte und Tab. 3 Gruppenvergleich der konfirmatorischen Zielgrößen in 5.2, Beschriftung als Feld, Anmerkungen nach Textvorschlag 4.7 (26.09.) § 7, vorher keine Platzhalter |')
rp('| M13 | offen, vor der Abgabe (Task 18) |', '| M13 | offen, Task 18: Abbildungs- und Tabellenverzeichnis mit F9 aktualisieren, sobald die Beschriftungen als Felder vorliegen |')
rp('| M16 | offen, Task 13 (Zusammenfassung und Abstract) |', '| M16 | offen, Task 13: Zusammenfassung und Abstract nach der Abstract-Checkliste (§ 3.3), mit dem Ankersatz (K6) |')
rp('| M23 | für die Einleitung gegenstandslos (Textvorschlag), für die übrigen leeren Abschnitte optional |',
   '| M23 | für die Einleitung gegenstandslos (Textvorschlag), für die übrigen leeren Abschnitte optional: je ein Platzhalterabsatz mit der Zugfolge aus § 3.1, die Tasks des Plans tragen dieselbe Information |')
rp('Wortzahlen aus dem Messskript, Seiten aus dem Seitenmodell, Stand von M10 bis M22 am Master',
   'Nach der übergreifenden Zweitprüfung (28.09.) ergänzt: Urteil der Anwendbarkeitsprüfung, Ä2 bis Ä10 und der Wortlaut der offenen M-Punkte (v4 ist nur noch Herkunft), M26, die Rasterspalte in § 3.2 aus dem Berichtsraster Rev. 3, der Verweis auf das Raster in der Inhaltsspalte, die Verdünnungslogik in 6.1 (Klick 19:25). Wortzahlen aus dem Messskript, Seiten aus dem Seitenmodell, Stand von M10 bis M22 am Master')

text = re.sub(r'\n{3,}', '\n\n', text)
if SEMI in text.replace('„' + SEMI + '“', ''):
    raise SystemExit('Abbruch: Semikolon im erzeugten Text')
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('Gliederung v5 geschrieben: %d Zeichen, Kapitel 4 %d, Altbestand %d, Textvorschlag %s, Prognose %s und %s Seiten' % (
    len(text), K4, ALT, TVW, de(S_GB, 1), MP))
print('Fassung 2: %d Ersetzungen' % len(LOGV))
print('Stand am Master: ' + ' · '.join('%s %s' % (k, 'erledigt' if v else 'offen') for k, v in PRUEF.items()))

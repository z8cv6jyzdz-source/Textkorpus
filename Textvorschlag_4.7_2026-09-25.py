# -*- coding: utf-8 -*-
"""
Textvorschlag_4.7_2026-09-25.py — Übergabedokument „Textvorschlag 4.7 Statistische Auswertung“ erzeugen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Skill kapiteltext-bachelorarbeit, Schritte 4 bis 7

Liest die drei Textstufen (Textvorschlag_4.7_2026-09-25_A.txt, Textvorschlag_4.7_2026-09-25_Empf.txt, Textvorschlag_4.7_2026-09-25_Kurz.txt), die Kürzungsleiter
(Kuerzungsleiter_4.7_2026-09-25.txt) und den Kapitel-4-Bestand des Masters (master/kap4_text.txt), misst jede Stufe
(Wörter, Sätze, Median, längster Satz, Semikola, Abschnittsverweise, Belege) und schreibt
Textvorschlag_4.7_2026-09-25.md. Alle Zahlen des Kopfblocks sind gemessen, keine von Hand. Ohne Semikolon.
Aufruf: python Textvorschlag_4.7_2026-09-25.py
Fassung: 2026-09-25, erste Fassung.
"""
import re
import statistics

SEMI = chr(59)
ABK = ['S.', 'et al.', 'Abs.', 'Nr.', 'Tab.', 'Abb.', 'vgl.', 'bzw.', 'z. B.', 'u. a.', 'ca.', 'Hrsg.', 'Aufl.']


def saetze(a):
    s = a
    for ab in ABK:
        s = s.replace(ab, ab.replace('.', '․'))
    s = re.sub(r'(\d)\.(\d)', r'\1․\2', s)
    s = re.sub(r'(\d{2})\.(\d{4})', r'\1․\2', s)
    s = re.sub(r'(\d{2})\.\s', r'\1․ ', s)
    teile = re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(0-9])', s)
    return [t.replace('․', '.') for t in teile if t.strip()]


def lese(pfad):
    txt = open(pfad, encoding='utf-8').read()
    titel = re.findall(r'^# \[(ABS\d)\] (.*)$', txt, re.M)
    body = '\n'.join(z for z in txt.split('\n') if not z.startswith('#'))
    abs_ = [a.strip() for a in re.split(r'\n\s*\n', body) if a.strip()]
    return titel, abs_


def messe(abs_):
    alle = []
    for a in abs_:
        alle.extend(saetze(a))
    ln = [len(x.split()) for x in alle]
    txt = '\n\n'.join(abs_)
    ohne = re.sub(r'\([^)]*\)', '', txt)
    return dict(
        woerter=sum(len(a.split()) for a in abs_),
        je_absatz=[len(a.split()) for a in abs_],
        saetze=len(ln), median=statistics.median(ln), laengster=max(ln),
        ueber32=sum(1 for l in ln if l > 32), ueber40=sum(1 for l in ln if l > 40),
        absatz_max=max(len(a.split()) for a in abs_),
        semi=txt.count(SEMI), semi_ausser=ohne.count(SEMI),
        verweise=len(re.findall(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)', txt)),
        belege=len(re.findall(r'\((?:[A-ZÄÖÜ][^()]*?\d{4}[^()]*)\)', txt)),
        objekte=sorted(set(re.findall(r'(?:Tab|Abb)\.\s*H\d+', txt))),
        anhang=sorted(set(re.findall(r'Anhang [A-H]', txt))),
        kennungen=len(re.findall(r'\[K-', txt)),
        konnektoren=len(re.findall(r'\b(Dabei|Außerdem|Zudem|Ferner|Darüber hinaus|Des Weiteren)\b', txt)),
    )


titelA, A = lese('Textvorschlag_4.7_2026-09-25_A.txt')
_, E = lese('Textvorschlag_4.7_2026-09-25_Empf.txt')
_, Kz = lese('Textvorschlag_4.7_2026-09-25_Kurz.txt')
mA, mE, mK = messe(A), messe(E), messe(Kz)
leiter = open('Kuerzungsleiter_4.7_2026-09-25.txt', encoding='utf-8').read().strip().split('\n')
kap4 = open('master/kap4_text.txt', encoding='utf-8').read()
bestand = {}
abschnitt = None
for z in kap4.split('\n'):
    m = re.match(r'## \[Heading \d\] (\d(?:\.\d)*(?:\.\d)?) ', z)
    if m:
        abschnitt = m.group(1)
        continue
    m = re.match(r'\[Normal, (\d+) W\]', z)
    if m and abschnitt and abschnitt.startswith('4') and not z.startswith('[Normal, 19 W] ⟨Abb'):
        bestand[abschnitt] = bestand.get(abschnitt, 0) + int(m.group(1))
anm = 100  # Anmerkung zu Tab. 1 (zählt als Beschriftung, nicht als Absatztext)
bestand['4.4'] -= anm
kap4_summe = sum(v for k, v in bestand.items() if k != '4.7')
for k in ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.6']:
    if k not in bestand:
        raise SystemExit('Abschnitt fehlt im Bestand: ' + k)


def tsd(n):
    return format(n, ',').replace(',', '.')


def kopf(m):
    return ('%d (%s) | %d · %.1f · %d | %d / %d | %d | %d | %d | %d' % (
        m['woerter'], '/'.join(str(x) for x in m['je_absatz']), m['saetze'], m['median'], m['laengster'],
        m['ueber32'], m['ueber40'], m['semi'], m['verweise'], m['belege'], m['kennungen'])).replace('.', ',')


def block(titel, abs_):
    out = []
    for (kurz, name), a in zip(titel, abs_):
        out.append('**[%s] — %d Wörter — %s**\n\n%s\n' % (kurz, len(a.split()), name, a))
    return '\n'.join(out)


doc = []
doc.append('# Textvorschlag 4.7 — Statistische Auswertung — Fassung A mit Kürzungsleiter\n')
doc.append('Erstellt 25.09.2026, abends (Rev. 95) · Grundlage: Berichtsraster Rev. 2 § 3.11 (Zeilen 4.7.1 bis 4.7.15, § 4 Nr. 1 und 6, Prüfliste), Bauplan § 2.2 Statistikabsatz und § 5/§ 6/§ 8, Stilprofil (F1 bis F4, Teil 3 bis 5), Auswertungsplan § 5.10 (R1 bis R14), Umfangsdokument § 2, § 5 und § 7, Voraussetzungsprüfungen § 5.3, Kennzahlenblatt 25.09. (Rev. 2), Umgebung der Abgabe (R 4.3.3), Volltexte Lakens (2022), Moher et al. (2010), Fröhlich et al. (2020), Vickers und Altman (2001), Cohen (1988) · Verfahren: Freigabe per Klick, danach Einbau per Skript in den Master und Endabgleich · **kein Einbau vor der Freigabe.**\n')
doc.append('Ablage: `Claude\\04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md` + Projektkopie `claude/…` — Maßstab für den Abgleich und Beleg für die KI-Deklaration. Erzeuger `Claude\\03_Skripte\\Textvorschlag_4.7_2026-09-25.py`, Textstufen und Messskript daneben.\n')
doc.append('---\n')
doc.append('## 0 Kopf — Messung (Leerzeichen-Token wie beim Master, Zeilen mit # ausgeschlossen)\n')
doc.append('| Stufe | Wörter (je Absatz) | Sätze · Median · längster | > 32 / > 40 | Semikola | Abschnittsverweise | Belegklammern | Kennungen |')
doc.append('|---|---|---|---|---|---|---|---|')
doc.append('| **Fassung A** (vollständig) | %s |' % kopf(mA))
doc.append('| **Empfehlung** (A ohne K5, K7, K8, K10, K12, K13) | %s |' % kopf(mE))
doc.append('| Kurz (A ohne K1 bis K14) | %s |' % kopf(mK))
doc.append('| Ziel | 550 (F14 § 5.2, Gliederung v4) | Median 14–18 · kein Satz > 32 | 0 / 0 | 0 | 0 | 1 je 100–300 Wörter | 0 |\n')
doc.append('Objektverweise in A: %s · Anhangsverweise: %s · adverbiale Konnektoren: %d · Verbotsliste: 0 · Marker: 0 · „randomisiert“, „ITT“, „erfüllt“ (positiv): 0.\n' % (', '.join(mA['objekte']), ', '.join(mA['anhang']), mA['konnektoren']))
doc.append('**Kapitel-4-Bestand im Master (25.09., nach der Vorschlagsliste, Absatztext ohne Beschriftungen und ohne die Anmerkung zu Tab. 1):** %s, Summe 4.1 bis 4.6 = **%s** (Budget 2.000). Mit 4.7 = 550 wären es %s gegen 2.550, mit der Empfehlung %s.\n' % (
    ' · '.join('%s %d' % (k, bestand[k]) for k in ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.6']), tsd(kap4_summe), tsd(kap4_summe + 550), tsd(kap4_summe + mE['woerter'])))
doc.append('---\n')
doc.append('## 1 Warum 550 Wörter mit den Pflichtzeilen nicht erreichbar sind\n')
doc.append('Das Budget 550 stammt aus dem Berichtsraster vom 23.09. (zwölf P-Zeilen). Seitdem sind Berichtspflichten mit Berichtsort 4.7 hinzugekommen, die das Budget nicht kannte: R1 (R als Rechenumgebung, blinde zweite Instanz, Python-Gegenprobe), R3 (Standardweg der Poweranalyse, nachträglich), R5 (Bootstrap für drei Zielgrößen, nachträglich), R9 bis R13 (Rückfragen, Gegenprobe, Korrektur des Reifestatus, Handprobe, Nachtrag 3), R14 (Erratum), die Voraussetzungsprüfungen mit Regel O7 (L16, Zeile 4.7.12) und die KI-gestützte Skripterstellung (Auswertungsverfahren 8.1). Das Raster führt jetzt fünfzehn Zeilen, davon vierzehn P, P° oder E. Eine unabhängige Zweitprüfung (§ 8) hat die vollständige Fassung A auf %d Wörter gemessen und keinen Satz gefunden, der einer anderen Zeile als 4.7 gehört. Die Kürzungsleiter (§ 2) zeigt, was jede Streichung kostet. Auch die volle Leiter (%d Wörter) erreicht 550 nicht, sie streicht dann Pflichtzeilen (Box-6-Klassen, Analyseeinheit). Entscheidung des Verfassers: Stufe wählen, das Budget von 4.7 auf rund 700 anheben und die Differenz in der Textrevision von 4.3 und 4.5.2 einsparen (beide liegen weit über ihrem Budget: 4.3 %d gegen 340, 4.5.2 %d gegen 150).\n' % (mA['woerter'], mK['woerter'], bestand['4.3'], bestand['4.5.2']))
doc.append('## 2 Kürzungsleiter (Ersparnis gemessen, jede Stelle ein vollständiger Satz oder Halbsatz der Fassung A)\n')
doc.append('| Nr. | Ersparnis | Wohin die Aussage geht | in der Empfehlung gestrichen |')
doc.append('|---|---|---|---|')
for z in leiter[1:-2]:
    nr, rest = z.split(': ', 1)
    ersp, grund = rest.split(' · ', 1)
    doc.append('| %s | %s | %s | %s |' % (nr, ersp, grund, 'ja' if nr in ('K5', 'K7', 'K8', 'K10', 'K12', 'K13') else 'nein'))
doc.append('')
doc.append('%s · %s\n' % (leiter[-2], leiter[-1]))
doc.append('**Empfehlung:** Fassung A ohne K5, K7, K8, K10, K12 und K13 (**%d Wörter**). K12 lagert die Daten- und Rechenprüfung aus: Die Sätze zu Reifestatus-Neuberechnung (R11), Rückfragen und Nachtrag 3 (R9, R13) und Excel-Handprobe (R12) werden zu zwei Sätzen mit Verweis auf die Prüfprotokolle in Anhang G, der Erratum-Satz (R14) wandert in die 4.3-Revision neben die Methode des Reifestatus, Tab. H5 wird in 5.1 eingeführt, die Bootstrap-Einzelheiten und die Vorab-Prüfung an den Prä-Werten gehen in Anhang G und die Anmerkung zu Tab. H4. Alle P-, P°- und E-Zeilen bleiben im Text. Nicht empfohlen: K1 (Verfasserfestlegung 23.09., TREND-Satz), K3 (Box 6, P/E), K14 (Methode der Power bei Vorab-Erwartungen, ohne sie hängen die Zahlen in 6.2 in der Luft).\n' % mE['woerter'])
doc.append('---\n')
doc.append('## 3 Zug-Tabelle (Bauplan § 2.2 Statistikabsatz, skaliert auf 15 Rasterzeilen)\n')
doc.append('| Zug | Umsetzung | Berichtsraster | Wörter A |')
doc.append('|---|---|---|---|')
zuege = [
    ('1 Analysepopulation als Eröffnung (F3-Satz), Ausschlussklassen, Nenner, Analyseeinheit', 'ABS1', '4.7.2 P · 4.7.3 P/E · § 4 Nr. 1 · F14 § 4 (TREND-Satz)'),
    ('2 Änderung nach Protokoll (F4-Satz), Per-Protokoll, deskriptive Zielgrößen mit Grund', 'ABS2', '4.7.7 P · 4.7.6 P/E · CONSORT 3b'),
    ('3 Fallzahl: Ressourcenbegründung, Antragsrechnung als Planungsstand, Sensitivitäts-Poweranalyse', 'ABS3', '4.7.8 P · CONSORT 7a · R3'),
    ('4 Hauptverfahren → Kovariaten → Effektstärke → Einordnung → α und Entscheidungsregel', 'ABS4', '4.7.4 P · 4.7.5 P · 4.7.9 P/E · 4.7.10 P · 4.7.14 E · 4.7.15 P/K · 4.1.8 E'),
    ('5 Sensitivitätsanalysen, Bootstrap nachträglich, Zusatzbeschreibungen', 'ABS5', '4.7.11 P · R5 · K-07.2, K-08.11'),
    ('6 Verteilungsprüfung (nach dem Modell, weil residuenbasiert), Regel O7', 'ABS6', '4.7.12 P/E · L16'),
    ('7 Daten- und Rechenprüfung, Software mit Version als letztes Wort', 'ABS7', '4.7.13 E · 4.7.15 P/K · Auswertungsverfahren 8.1 · R1, R9 bis R14'),
]
for (z, u, r), w in zip(zuege, mA['je_absatz']):
    doc.append('| %s | %s | %s | %d |' % (z, u, r, w))
doc.append('')
doc.append('Eröffnung mit der Analysepopulation (F3-Formel „gingen … in die Auswertung ein“), Schluss mit der Software (Bauplan § 2.2: letztes Wort der Methodik). Abweichend vom Bauplan steht die Verteilungsprüfung nach dem Hauptverfahren, weil sie an den Modellresiduen ansetzt und das Modell voraussetzt. Belege nur für Normen und Verfahren (Moher Box 6 und Item 7a, Lakens, Cohen, Vickers und Altman, Fröhlich, Khamis und Roche, R Core Team), keine für eine eigene Entscheidung. Präteritum für Getanes, Präsens für Berichtskonventionen, Definitionen und die Entscheidungsregel.\n')
doc.append('## 4 Verzichtstabelle\n')
doc.append('| Was der Korpus tut oder das Raster erwägt | Grund des Verzichts |')
doc.append('|---|---|')
verzicht = [
    ('Darstellungskonvention als erster Satz („Data are presented as mean ± SD“)', 'K-Zeile 4.7.1, Budget. Die Konvention steht in den Tabellenanmerkungen (Umfangsdokument § 3.7)'),
    ('Verteilungsprüfung an den Messwerten vor dem Hauptverfahren (6 von 11)', 'Prüfung an den Modellresiduen (Voraussetzungsprüfungen § 2.1), deshalb nach dem Modell'),
    ('Post-hoc-Tests', 'zwei Gruppen, Kovarianzanalyse ohne Post-hoc'),
    ('Reliabilität im Statistikabsatz', 'steht in 4.4 (Testkette, Tab. 1)'),
    ('Aggregationsregel, 505-Regel', 'stehen in 4.4 und 4.4.2 (Bauplan: Testabsatz, nie Statistikteil)'),
    ('Verbale Effektetiketten (klein, mittel, groß)', 'Einordnung gegen SESOI und Konfidenzintervall (Umfangsdokument § 5.1, Prüfliste Nr. 6)'),
    ('Baseline-Signifikanztests (6 von 13)', 'CONSORT Item 15, Zeile 4.7.5'),
    ('Post-hoc-Power (1 von 13)', 'Moher et al. (2010, Item 7a), Zeile 4.7.8'),
    ('Etikett „ITT“', 'CONSORT 2010 hat es gestrichen, Beschreibung statt Etikett (Berichtsraster § 4 Nr. 1). Das Wort kommt nicht vor'),
    ('„Voraussetzungen erfüllt“, Robustheitsaussage, TE/√n', 'Ausschlüsse Nr. 10, 11 und 14 (Umfangsdokument § 5.4)'),
    ('Verfahrensquellen Shapiro und Wilk (1965), Brown und Forsythe (1974), Hedges (1981), Perzentil-Bootstrap', 'Volltexte nicht im Ordner (F14 § 7.1). Testnamen ohne Beleg, Beschaffungsposten H (Hedges 1981 neu)'),
    ('Leppink (2018), Rochon et al. (2012), Stuart (2010) als Belege der Prüfungen (Voraussetzungsprüfungen § 5.3)', 'nur online gelesen (Status V), vor einer Zitation in `Ideen und Studien` ablegen und lesen'),
    ('Lehrbuchbegründung ANCOVA gegen Änderungswerte (Lord)', '6.2, ein Satz reicht in 4.7 nicht einmal'),
    ('Modellgleichung in Formelschreibweise', 'Wortform, die Gleichung steht im R-Skript (Anhang G) und in der Anmerkung zu Tab. 3'),
    ('Objektverweis auf Tab. 3 für die Nenner (Raster 4.7.2)', 'Tab. 3 wird in 5.2 eingeführt, ein Erstverweis in 4.7 kippte die Platzierungsregel (§ 9). Der Satz „Die Nenner werden je Zielgröße und Gruppe berichtet“ trägt die Regel'),
    ('Anlass des Bootstrap mit Zahl (verworfene Normalverteilung 30 m in der ersten Rechnung)', 'Ergebnis der ersten Rechnung. Der Grund steht ohne Zahl im Satz („mit Zweifeln an der Normalverteilung der Residuen“), die Zahl in 5.2 nach R2'),
    ('Zahl der geprüften und korrigierten Zellen der Belegprüfung', 'nicht im Kennzahlenblatt, Prüfprotokoll in Anhang G'),
    ('SPSS', 'R (F0, R1)'),
]
for a, b in verzicht:
    doc.append('| %s | %s |' % (a, b))
doc.append('')
doc.append('---\n')
doc.append('## 5 Wortlaut Fassung A — je Absatz (vollständig, %d Wörter)\n' % mA['woerter'])
doc.append(block(titelA, A))
doc.append('---\n')
doc.append('## 6 Wortlaut Empfehlung — je Absatz (%d Wörter, Übertragungsvorlage bei Klick „Empfehlung“)\n' % mE['woerter'])
doc.append(block(titelA, E))
doc.append('Die Stufe „Kurz“ (%d Wörter) liegt als `Textvorschlag_4.7_2026-09-25_Kurz.txt` in `03_Skripte` bereit und wird nur auf Klick gesetzt.\n' % mK['woerter'])
doc.append('---\n')
doc.append('## 7 Kennungen je Zahl (Begleitteil, im Fließtext ohne Kennung — Verfasserfestlegung 25.09.)\n')
doc.append('| Zahl im Text | Kennung oder Quelle | Bezugsmenge |')
doc.append('|---|---|---|')
kenn = [
    ('75 % der Einheiten (neun von zwölf)', 'Ethikantrag Abschn. 8 (Antragswortlaut), P-11 (zwölf Einheiten)', 'Sollvorgabe'),
    ('drei Spieler', 'K-10.10 (GANZ ≥ 9 = 3), Einzelwerte K-10.17', 'zugeteilte IG-Spieler (K-10.4: 18)'),
    ('11. und 12.09.2026', 'Prozessdaten: Auswertungsplan § 5.3, F14 § 11.7 und § 11.9', 'Festlegungen des Verfassers'),
    ('sechs absolvierten Einheiten, der Hälfte des Programms', 'Konvention PP6, Spezifikation S16, P-11', 'Status „ganz“ nach 4.6'),
    ('acht Spielern je Gruppe', 'Fallzahlregel R4, F14 § 11.9', 'Analyseset je Zielgröße'),
    ('5 und 10 m', 'K-01.23 und K-04: 5 m KG-Set 7, 10 m IG-Set 7 (unter acht)', 'Analyseset'),
    ('f = 0,25, erforderlich n = 34', 'Ethikantrag Abschn. 4 (Planungsrechnung)', 'Planungsstand'),
    ('Freiheitsgrade 1 und N − 4, α = 0,05, Power 0,80', 'Spezifikation S18 (O9), K-09', 'Standardweg'),
    ('für den 10-m-Sprint nur diese (Power bei Vorab-Erwartungen)', 'K-09.1 (d = 0,06 und 0,11), K-09.2 bis 09.4 (d = 0,37 und 0,93)', 'im Plan genannte Kombinationen (R7)'),
    ('30-m-Sprint, 505-Seitenmittel, Standweitsprung', 'konfirmatorische Zielgrößen, F14 § 11.9, K-06', 'ITT-Sets 16/10, 13/10, 16/10 (K-06)'),
    ('95-%-Konfidenzintervall, p < 0,05, α = 0,05 zweiseitig', 'Ethikantrag, Spezifikation S13, K23/P6 (K-06.4)', 'Entscheidungsregel'),
    ('sechs weitere Modellvarianten, fünf und sieben Einheiten', 'Spezifikation S16/S17, K-08.2 bis K-08.7 (mit PP6 sieben Varianten, F14 § 11.5)', 'Tab. H4'),
    ('15.09.2026', 'Datum der ersten Auswertung (Analyseprotokoll_2026-09-15), R5', 'Prozessdatum'),
    ('10 000 Ziehungen', 'Spezifikation S19, K-08.8 (B = 10 000, Startwert 20260924, Schichtung nach Gruppe)', 'Bootstrap'),
    ('1994, 1995 (Khamis und Roche, Erratum)', 'R14, Rechercheprotokoll_Erratum 25.09.', 'Verfahrensquelle'),
    ('R 4.3.3 (R Core Team, 2024)', 'Umgebung_2026-09-25.txt der Abgabe, citation() in R 4.3.3', 'Rechenumgebung'),
    ('ein Spieler ohne Reifestatus', 'K-01.11 (KG 1), K-01.21', 'zugeteilte Spieler'),
    ('drei Vereinen', 'K-01.24, K-01.4 bis K-01.6', 'Clusterebene'),
    ('Kleinstichprobenfaktor J', 'Spezifikation O3: J = 1 − 3/(4·df − 1), df = n_IG + n_KG − 2', 'Effektstärke'),
]
for a, b, c in kenn:
    doc.append('| %s | %s | %s |' % (a, b, c))
doc.append('')
doc.append('Nicht in 4.7: alle Ergebniswerte (K-05 bis K-09 Werte, K-10 Raten), N = 26 und die Nenner (4.2, Tab. 2, Tab. 3), MDES und Power-Werte (6.2, Anhang G), Prüfgrößen der Voraussetzungen (5.2 nach R2, Tab. H4).\n')
doc.append('---\n')
doc.append('## 8 Prüfung vor dem Vorlegen (Skill Schritt 6) und unabhängige Zweitprüfung\n')
doc.append('**1 Inhalt — jeder Satz einer Rasterzeile zugeordnet (Fassung A):** ABS1 S1 → 4.7.2 · S2 → Sprachregelung F14 § 10 (E) · S3–S4 → 4.7.3 · S5 → 4.7.2 (CONSORT 16) · S6 → F14 § 4 (Analyseeinheit) · ABS2 S1–S2 → 4.7.7 (3b) und 4.7.6 (Antragskriterium deskriptiv) · S3 → 4.7.7 (Per-Protokoll, Box 6) · S4 → 4.7.7 (Datum, Grund) · S5 → Tab. H5 (Umfangsdokument § 3.5) · S6 → 4.7.6 · ABS3 S1 → 4.7.8 (Ressourcenbegründung) · S2 → 4.7.8 (Planungsstand, L14 a) · S3–S6 → 4.7.8 (Sensitivitäts-Poweranalyse, Berichtsangaben, Vorab-Erwartungen) · S7 → R3 nachträglich · ABS4 S1 → 4.7.4 · S2 → 4.7.4, 4.7.10 · S3 → 4.7.5 · S4 → 4.7.5 (CONSORT 15) · S5 → 4.7.9 · S6 → Schlusslogik (Umfangsdokument § 5.1) · S7 → 4.1.8, 4.7.14, 4.7.15 · ABS5 S1–S2 → 4.7.11 · S3–S4 → 4.7.11 (Bootstrap nachträglich, R5) · S5 → K-07.2, K-08.11 (Tab. H4) · ABS6 S1–S2 → 4.7.12 · S3–S4 → 4.7.12 („geprüft und nicht verworfen“) · S5 → 4.7.12 (Regel O7) · ABS7 S1–S2 → 4.7.13 (Belegprüfung, Datenstand) · S3 → R14 · S4 → R11 · S5 → 4.7.13 (F1 ohne unabhängige Prüfung) · S6 → R9, R13 · S7–S9 → 4.7.13, Auswertungsverfahren 8.1 (KI-Skripterstellung, Gegenprobe, Handprobe R12) · S10 → Anhang G (8.1) · S11 → 4.7.15. Negativliste „Nicht hier“: keine Ergebniszahl, kein „erfüllt“, keine Robustheitsaussage, kein TE/√n, kein Objekt Tab. H5, keine Deutung. ✓\n')
doc.append('**2 Bauform:** Züge in der Reihenfolge Population → Abweichung → Fallzahl → Modell → Sensitivität → Voraussetzungen → Prüfung und Software (§ 3), Eröffnung F3, Schluss Software mit Version, ein Anhangsverweis (G, bei der ersten Erwähnung des Materials), ein Objektverweis (Tab. H5, in der Empfehlung nach 5.1 verschoben), Quellen nachgestellt, keine Namen als Satzsubjekt, Tempus nach Bauplan § 6. ✓\n')
doc.append('**3 Zahlen:** jede Ziffer mit Kennung oder Quelle (§ 7), Bezugsmenge im Satz („je Gruppe“, „des Analysesets“, „zugeteilten“). Keine Zahl aus einem Prosadokument außer Prozessdaten und Antragswortlaut. ✓\n')
doc.append('**4 Messung (§ 0):** Fassung A %d Wörter, Median %s, längster Satz %d, kein Satz über 32, längster Absatz %d, Semikola %d, Abschnittsverweise %d, Kennungen 0, Verbotsliste 0, Konnektoren %d, Belegklammern %d (eine je %d Wörter, über dem Korpuskorridor von einer je 100 bis 300, weil 4.7 die Normen trägt). ✓ mit Vorbehalt Wortzahl (§ 1).\n' % (mA['woerter'], str(mA['median']).replace('.', ','), mA['laengster'], mA['absatz_max'], mA['semi'], mA['verweise'], mA['konnektoren'], mA['belege'], round(mA['woerter'] / mA['belege'])))
doc.append('**Unabhängige Zweitprüfung (Subagent ohne Beteiligung am Text, 25.09.):** 16 Sachbefunde (A1 bis A16), zwei Vollständigkeitslücken (Planungsmodell-Hinweis, Power bei Vorab-Erwartungen), Registerposten ohne Satz (R11, R9/R13, Vorab-Prüfung, Familiarisierung Variante a), neun Sprachpunkte (Tempus der Berichtskonvention, tautologischer O7-Satz, „statt nur die“, Klammer mit Etikett und Beleg, Komma-Reihungen, Software als letztes Wort), sieben Doppelungen und Widersprüche zu 4.1 bis 4.6, neun Zitatprüfungen am Volltext (alle Fundstellen bestätigt, Fröhlich S. 59 nur als Norm „Voraussetzungen stets prüfen“ tragfähig, deshalb an den Prüfsatz gebunden). Alle Befunde sind in die Fassung A eingearbeitet, außer: der Anlass des Bootstrap bleibt ohne Zahl (§ 4), der Tab.-3-Verweis bleibt weg (§ 4), die Zitierdichte bleibt über dem Korridor. Das Urteil der Zweitprüfung zum Budget steht in § 1.\n')
doc.append('---\n')
doc.append('## 9 Prüfvermerke\n')
doc.append('1. **Produktname im Manuskript:** „ein KI-Sprachmodell (Claude, Anthropic)“ nennt das Werkzeug wie die KI-Deklaration (DSHS-Leitlinie: Anwendung und Datum). Ohne Namen: „ein KI-Sprachmodell“ (−2 Wörter), Entscheidung des Verfassers beim Klick.\n2. **Verfahrensquellen ohne Volltext:** Shapiro-Wilk-Test, Brown-Forsythe-Test, Hedges-Faktor J und Perzentil-Bootstrap stehen ohne Beleg (F14 § 7.1). Beschaffungsposten H: Shapiro und Wilk (1965), Brown und Forsythe (1974), Royston (1995) bereits gelistet, **Hedges (1981) neu** (Journal of Educational Statistics 6(2), 107–128). Nach Beschaffung je eine Klammer ergänzen.\n3. **Cohen (1988, Tab. 8.4.4):** stützt „nicht nachvollziehbar“ (64 je Gruppe bei f = 0,25, F14 § 11.1 L14 a). Seitenzahl der Tabelle vor der Abgabe am Scan nachtragen, T4-Zeile Cohen1988 ergänzen.\n4. **Terminologie im Master:** 4.3 und 4.4.1 nennen die Abschlusstestung „Ausgangstestung“, 4.1 und Tab. 1 „Abschlusstestung“, 4.7 verwendet „Ausgangswert“ nur für den Prä-Wert. In der 4.3- und 4.4-Revision auf „Abschlusstestung“ vereinheitlichen (G19/G18-Tasks).\n5. **Lakens (2022):** S. 3–5 (Resource constraints, Tab. 3), S. 14–15 (Plot a sensitivity power analysis), S. 13–14 (Breite des Konfidenzintervalls, welche Effekte zurückweisbar sind) am PDF geprüft, PDF-Seite = gedruckte Seite. T4-Zeile Lakens2022 gilt („Übertragung auf Feldstudien ist unser Schritt“).\n6. **Fröhlich et al. (2020):** S. 59 (Anwendungsvoraussetzungen stets zu prüfen), S. 78 (Bootstrapping ohne Normalverteilungsannahme), S. 106 (ITT-Definition, nicht zitiert) am PDF geprüft (gedruckte Seitenzahl im Kopf der Seite).\n7. **Moher et al. (2010):** Box 6 („non-randomised, observational comparison“, „dropped the specific request for intention-to-treat analysis“) und Item 7a („little merit in a post hoc calculation“) am Volltext geprüft, Fundstelle nach F14 § 15 die Item-Nummer.\n8. **Sieben gegen sechs Varianten:** 4.7 nennt sechs weitere Modellvarianten neben dem Per-Protokoll-Vergleich ab sechs Einheiten. Tab. H4 und 5.2 zählen sieben Varianten (F14 § 11.5). Beide Zählweisen sind vereinbar, 5.2 formuliert „sieben Varianten, darunter der Per-Protokoll-Vergleich“.\n9. **Beide Festlegungen nach Sichtung der IG-Werte:** 4.1 sagt „nach Sichtung der Adhärenzdaten“, 4.7 „nach Sichtung der Adhärenz- und Abschlusswerte“ (F14 § 11.7: nach Sichtung der IG-Post-Werte). 4.1 in der Textrevision angleichen (Vormerkung).\n10. **„Varianzkomponente … nicht modelliert“** statt „nicht schätzbar“ (Zweitprüfung A4): Mit drei Clustern ist eine Komponente rechnerisch schätzbar, aber nicht belastbar (F14 § 11.6).\n')
doc.append('## 10 Vormerkungen für andere Abschnitte (nicht in diesem Task einbauen)\n')
doc.append('- **4.3 (Textrevision):** Erratum-Satz (R14) und die Interpolation der Koeffizienten (O2) neben die Methode des Reifestatus, wenn K5/K12 gewählt werden · „Ausgangstestung“ → „Abschlusstestung“ · Familiarisierungstermine je Verein (Raster 4.3.4) · „Testleitung, Datenerhebung und Freigabe der Auswertung in einer Hand“ (Zweitprüfung D4).\n- **4.1:** Adhärenzkriterium-Satz an 4.7 angleichen („nach Sichtung der Adhärenz- und Abschlusswerte der Interventionsgruppe“).\n- **4.4.1:** „(Abschn. 4.7)“ entfällt mit G19, der Grund (Fallzahlregel) steht in 4.7.\n- **4.6:** „(neun von zwölf Einheiten)“ und „dessen Anwendung ist in Abschnitt 4.7 geregelt“ entfallen (G26b, G19), 4.7 ist selbsttragend.\n- **5.1:** Tab. H5 einführen (Adhärenz, Schwellenlandschaft), wenn K10/Empfehlung gewählt wird · Untergrenzen der Adhärenz (K-10.11).\n- **5.2:** Prüfgrößen verworfener Voraussetzungen mit Bootstrap-KI (R2) · Sammelsatz „sieben Varianten“ (Tab. H4) · Vorab-Prüfung an den Prä-Werten in einem Satz (Umfangsdokument R2) · Anmerkung zu Tab. H4 mit K-07.2 und K-08.11, wenn K13 gewählt wird.\n- **6.2/6.3:** Planungsmodell der Antragsrechnung (L14 a) · MDES gegen SESOI, Power bei Vorab-Erwartungen (G1) · Robustheit und Trennschärfe (Voraussetzungsprüfungen § 5.3) · Konfundierung der Familiarisierung (G7) · Analyseeinheit und Cluster (G2) · Verdünnungslogik (G3).\n- **Anhang G:** Prüfprotokolle (Belegprotokoll, Abgleichprotokoll, Durchsichts- und Plausibilitätsprotokoll, Handprobe, Rückfragenprotokoll, Nachtrag 3), Poweranalyse mit Eingaben je Zielgröße, R-Skripte mit citation(), Q-Q- und Linearitätsdiagramme.\n- **Tab. H6:** R11 (Reifestatus alt/neu) als Zeile des Abweichungsregisters.\n- **Literaturverzeichnis:** R Core Team (2024) aus citation() · Lakens (2022), Moher et al. (2010), Vickers und Altman (2001), Cohen (1988) bereits vorgesehen · Hedges (1981) nur nach Beschaffung.\n- **F14 § 5.2:** Budget 4.7 nach der Klickentscheidung (rund 700), Gegenfinanzierung in 4.3 und 4.5.2, Erratum in F14 § 1.5 ist eine Verfasserentscheidung (R14).\n- **T4:** Cohen1988 (Tab. 8.4.4 für die Planungsrechnung), Lakens2022 (S. 13–14 KI-Breite), Froehlich2020 (S. 59 nur Norm, S. 78 Bootstrapping allgemein).\n')
doc.append('## 11 Abgleich nach dem Einbau\n')
doc.append('Einbau per Skript `Master_4.7_2026-09-25.py` (sieben Absätze unter der Überschrift 4.7, Formatvorlage wie Bestand, keine Direktformatierung), Sicherung des Vorstands in `_Archiv`, Render über LibreOffice, danach `Endabgleich_Manuskript_2026-09-25.py` erneut (Wortprüfung SPSS, MDC, TE/√n, ITT, „leistungsunabhängig“, „randomisiert“) und Messung des Kapitel-4-Bestands. Ergebnis in Teil 0 (Rev. 95) und Maßnahmenliste (L9, L16, G5).\n')
out = '\n'.join(doc)
if SEMI in out.replace('(Schulz et al., 2010' + SEMI, ''):
    raise SystemExit('Semikolon im Dokument')
open('Textvorschlag_4.7_2026-09-25.md', 'w', encoding='utf-8', newline='\n').write(out)
print('geschrieben: Textvorschlag_4.7_2026-09-25.md, A %d, Empfehlung %d, Kurz %d, Kapitel 4.1 bis 4.6 %d' % (mA['woerter'], mE['woerter'], mK['woerter'], kap4_summe))

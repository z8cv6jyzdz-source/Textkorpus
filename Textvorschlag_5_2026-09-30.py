# -*- coding: utf-8 -*-
"""
Textvorschlag_5_2026-09-30.py — Task 11 (Kapitel 5 Ergebnisse), Textvorschlag mit Messung und Prüfungen

Hält den Wortlaut von Kapitel 5 je Absatz (Absatzgruppen 5.1 und 5.2 nach Gliederung v6, ohne Unterüberschriften),
misst wie Manuskriptstand_2026-09-25.py (Wörter = Leerraum-Token, Satzteilung saetze() unverändert) und prüft:
(1) Budget: Kapitel 5 gegen 450 (v6, verbindlich), Absatzgruppen gegen die Richtwerte 230 und 220,
(2) Satzlängen (Median, längster Satz, Sätze über 32), Absätze über 250 Wörter,
(3) Semikola, Abschnittsverweise, Belegklammern (Kapitel 5: null), Doppelpunkte,
(4) Wortprüfung auf Deutungs- und Verbotswörter (Plan § 3 Task 11, Stilprofil Teil 5, F17 § 10),
(5) jede Zahl (Ziffern und Zahlwörter) gegen ihre Kennung im Kennzahlenblatt (Werte.csv, Spalte darstellung),
(6) Objektverweise: Erstverweis je Objekt genau einmal als Satzsubjekt (Textobjekte) oder Klammer (Anhangsobjekte),
    Wiederaufruf nur als Klammer, jedes verwiesene Objekt existiert in Objekte_2026-09-25.
Schreibt Textvorschlag_5_2026-09-30.txt (Laufprotokoll) und Textvorschlag_5_2026-09-30.json (Absätze für das Einbauskript).
Aufruf: python Textvorschlag_5_2026-09-30.py <Kennzahlen_Werte.csv> <Objekte-Ordner> <Ausgabeordner>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import os
import re
import csv
import json
import statistics

WERTE, OBJ, AUS = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(AUS, exist_ok=True)
SEMI = chr(59)

# ---------------------------------------------------------------- Wortlaut (Absatzgruppe, Kennung des Absatzes, Text)
ABSAETZE = [
    ('5.1', 'A1', 'Abb. 1 zeigt den Teilnehmerfluss bis zum planmäßigen Studienende. '
                  'Von 31 zur Eingangstestung angetretenen Spielern gingen 26 in die Analyse ein. '
                  'Tab. 2 enthält die Ausgangswerte im Analyseset mit standardisierter Differenz d und Überlappung der '
                  'Kovariaten, Tab. H3 die Ausgangswerte aller eingangsgetesteten Spieler. '
                  'Alle Ausgangsunterschiede lagen zugunsten der Interventionsgruppe.'),
    ('5.1', 'A2', 'Die 18 zugeteilten Spieler der Interventionsgruppe meldeten 92 Einheiten als vollständig, 6 als '
                  'teilweise und 13 als nicht durchgeführt, im Median 6,0 vollständige je Spieler (Tab. H2). '
                  'Bei zwölf angebotenen Einheiten je Spieler entsprach das einer Umsetzungsrate von 42,6 % '
                  '(45,4 % mit den teilweise durchgeführten). '
                  'Zehn Spieler erreichten mindestens sechs, drei mindestens neun Einheiten (Tab. H2 und Tab. H5). '
                  'Als Untergrenzen ergaben sich mit höchstens zwei Meldungen je Programmwoche neun und zwei Spieler, '
                  'nach verschiedenen Einheitennummern neun und einer.'),
    ('5.1', 'A3', 'Die Beanspruchung der 92 als vollständig gemeldeten Einheiten lag auf der CR-10-Skala bei 2,9 ± 0,9 '
                  '(Median 3,0, Spanne 0,0 bis 5,0). '
                  'Der mit der Solldauer berechnete sRPE-Load betrug 106,7 ± 35,9 AU (Median 110,8, Spanne 0,0 bis 199,7). '
                  'Zwölf Meldungen von neun Spielern nannten Schmerzen oder Probleme, davon je zwei zu nicht und zu '
                  'teilweise durchgeführten Einheiten. '
                  'Für die Kontrollgruppe wurden solche Angaben nicht erhoben.'),
    ('5.1', 'A4', 'Der typische Messfehler überstieg auch bei der Abschlusstestung in allen Zielgrößen den SESOI (Tab. 1). '
                  'Mehr gültige Versuche je Spieler hatte im Mittel beim 30-m-Sprint und Standweitsprung zu beiden '
                  'Zeitpunkten die Interventionsgruppe, beim 505-Test je Seite überwiegend die Kontrollgruppe (Tab. H1).'),
    ('5.2', 'A5', "Tab. 3 enthält für die konfirmatorischen Zielgrößen die unadjustierten und adjustierten "
                  "Gruppendifferenzen im Post-Wert sowie Hedges' g. "
                  'Abb. 2 zeigt je Zielgröße Ausgangswert und reifeadjustierten Abschlusswert jedes Spielers mit den '
                  'Modelllinien beider Gruppen. '
                  'Alle unadjustierten Differenzen lagen zugunsten der Interventionsgruppe und weiter von null '
                  'entfernt als die adjustierten. '
                  'Adjustiert für Ausgangswert und Reifestatus betrug die Differenz Interventions- minus Kontrollgruppe beim '
                  '30-m-Sprint −0,045 s (95-%-Konfidenzintervall −0,199 bis +0,110 s, p = 0,557). '
                  'Beim 505-Seitenmittel betrug sie −0,012 s (−0,085 bis +0,061 s, p = 0,734), beim Standweitsprung '
                  '−0,1 cm (−8,7 bis +8,6 cm, p = 0,987). '
                  'Bei keiner Zielgröße war damit ein Gruppenunterschied nachweisbar. '
                  'Jedes Intervall war mit relevanten Unterschieden in beide Richtungen vereinbar. '
                  'Die Befunde waren unschlüssig. '
                  'Keine adjustierte Differenz zeigte mit p < 0,05 einen Vorteil der Interventionsgruppe. '
                  'Die Nullhypothese wurde nicht verworfen. '
                  'Die 5- und 10-m-Sprintzeiten und die 505-Seitenwerte wurden nur beschrieben (Tab. H3).'),
    ('5.2', 'A6', 'Beim 30-m-Sprint verwarf der Shapiro-Wilk-Test die Normalverteilung der Residuen (W = 0,915, p = 0,034). '
                  'Das nachträglich festgelegte Bootstrap-Konfidenzintervall der adjustierten Differenz reichte dort von '
                  '−0,177 bis +0,107 s. '
                  'Die übrigen mit Tests geprüften Voraussetzungen wurden nicht verworfen (Tab. H4). '
                  'Soweit die Fallzahl eine Inferenz zuließ, änderten weder der beobachtende Per-Protokoll-Vergleich noch '
                  'die sechs Sensitivitätsanalysen die Einordnung als unschlüssig, und keine davon erreichte p < 0,05 (Tab. H4).'),
]

# ---------------------------------------------------------------- Zahlen und Kennungen (Begleitteil)
# (Absatz, Zahl im Text, Wert zum Abgleich mit der Darstellung, Kennung oder Quelle, Bezugsmenge)
ZAHLEN = [
    ('A1', '31', '31', 'K-01.1', 'zur Eingangstestung angetreten (einziger Satz dieser Menge, Bezugsmengen-Regel 1)'),
    ('A1', '26', '26', 'K-01.14', 'Analysepopulation (Menge ANA)'),
    ('A2', '18', '18', 'K-10.4', 'zugeteilte IG-Spieler, Nenner der Umsetzung'),
    ('A2', '92', '92', 'K-10.3', 'Meldungen Status ganz'),
    ('A2', '6', '6', 'K-10.3', 'Meldungen Status teilweise (Ziffer neben 92 und 13, Zweitprüfung Nr. 17)'),
    ('A2', '13', '13', 'K-10.3', 'Meldungen Status gar nicht'),
    ('A2', '6,0', '6,0', 'K-10.8', 'Median der Einheiten ganz je zugeteiltem IG-Spieler'),
    ('A2', 'zwölf', '12', 'K-10.4', 'angebotene Einheiten je Spieler (Nenner, Bezeichnung von K-10.4)'),
    ('A2', '42,6', '42,6', 'K-10.5', 'Umsetzungsrate GANZ, zugeteilte IG-Spieler'),
    ('A2', '45,4', '45,4', 'K-10.6', 'Beteiligungsrate ganz oder teilweise, zugeteilte IG-Spieler'),
    ('A2', 'Zehn', '10', 'K-10.10', 'Spieler mit GANZ ≥ 6 (Hauptzählung)'),
    ('A2', 'sechs', '6', 'K-10.10', 'Schwelle (Per-Protokoll-Schwelle, Festlegung 11.09.2026), Bezeichnung von K-10.10'),
    ('A2', 'drei', '3', 'K-10.10', 'Spieler mit GANZ ≥ 9 (Hauptzählung, Antragskriterium)'),
    ('A2', 'neun', '9', 'K-10.10', 'Schwelle des Antragskriteriums, Bezeichnung von K-10.10'),
    ('A2', 'zwei', '2', 'Konstante', 'Deckel der Zählweise WOCAP: höchstens zwei Meldungen ganz je Programmwoche (Spezifikation S07, F17 § 3.2, Anmerkung Tab. H2)'),
    ('A2', 'neun', '9', 'K-10.11', 'WOCAP ≥ 6'),
    ('A2', 'zwei', '2', 'K-10.11', 'WOCAP ≥ 9'),
    ('A2', 'neun', '9', 'K-10.11', 'DIST ≥ 6'),
    ('A2', 'einer', '1', 'K-10.11', 'DIST ≥ 9'),
    ('A3', '92', '92', 'K-10.13', 'n der Meldungen ganz (CR-10)'),
    ('A3', '2,9', '2,9', 'K-10.13', 'CR-10 M'),
    ('A3', '0,9', '0,9', 'K-10.13', 'CR-10 SD'),
    ('A3', '3,0', '3,0', 'K-10.13', 'CR-10 Median'),
    ('A3', '0,0', '0,0', 'K-10.13', 'CR-10 Minimum'),
    ('A3', '5,0', '5,0', 'K-10.13', 'CR-10 Maximum'),
    ('A3', '106,7', '106,7', 'K-10.14', 'sRPE-Load M (AU, CR-10 mal Solldauer)'),
    ('A3', '35,9', '35,9', 'K-10.14', 'sRPE-Load SD'),
    ('A3', '110,8', '110,8', 'K-10.14', 'sRPE-Load Median'),
    ('A3', '0,0', '0,0', 'K-10.14', 'sRPE-Load Minimum'),
    ('A3', '199,7', '199,7', 'K-10.14', 'sRPE-Load Maximum'),
    ('A3', 'Zwölf', '12', 'K-10.12', 'Meldungen mit H007 = 1 gesamt'),
    ('A3', 'neun', '9', 'K-10.12', 'Spieler mit mindestens einer solchen Meldung'),
    ('A3', 'zwei', '2', 'K-10.12', 'davon je Status gar nicht und teilweise („je zwei“: 2 und 2)'),
    ('A5', '−0,045', '−0,045', 'K-06.1', 'adjustierte Differenz 30 m (b1), Analyseset'),
    ('A5', '−0,199', '−0,199', 'K-06.1', 'untere KI-Grenze'),
    ('A5', '+0,110', '+0,110', 'K-06.1', 'obere KI-Grenze'),
    ('A5', '0,557', '0,557', 'K-06.1', 'p'),
    ('A5', '−0,012', '−0,012', 'K-06.2', 'adjustierte Differenz 505-Seitenmittel'),
    ('A5', '−0,085', '−0,085', 'K-06.2', 'untere KI-Grenze'),
    ('A5', '+0,061', '+0,061', 'K-06.2', 'obere KI-Grenze'),
    ('A5', '0,734', '0,734', 'K-06.2', 'p'),
    ('A5', '−0,1', '−0,1', 'K-06.3', 'adjustierte Differenz Standweitsprung'),
    ('A5', '−8,7', '−8,7', 'K-06.3', 'untere KI-Grenze'),
    ('A5', '+8,6', '+8,6', 'K-06.3', 'obere KI-Grenze'),
    ('A5', '0,987', '0,987', 'K-06.3', 'p'),
    ('A5', 'null', '0', 'Konstante', 'Bezugswert der Differenz (keine Ergebniszahl)'),
    ('A5', '0,05', '0,05', 'Konstante', 'Testniveau der Entscheidungsregel (4.7, Studienprotokoll)'),
    ('A6', '0,915', '0,915', 'K-07.1 Z30', 'Shapiro-Wilk W der Residuen, 30 m'),
    ('A6', '0,034', '0,034', 'K-07.1 Z30', 'p'),
    ('A6', '−0,177', '−0,177', 'K-08.8 Z30', 'Bootstrap-KI untere Grenze'),
    ('A6', '+0,107', '+0,107', 'K-08.8 Z30', 'Bootstrap-KI obere Grenze'),
    ('A6', 'sechs', '6', 'K-08.2 bis K-08.7', 'vorab festgelegte Sensitivitätsanalysen wie in 4.7 (K-08.2 bis K-08.7), der Per-Protokoll-Vergleich (K-08.1) ist gesondert genannt'),
    ('A6', '0,05', '0,05', 'Konstante', 'Testniveau'),
]
ZAHLWORT = {'null': 0, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5, 'sechs': 6, 'sieben': 7,
            'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12}
# Testnamen, Messstrecken und Bezeichnungen, die keine Ergebniszahl sind
NAMEN = [r'\b30-m-Sprint', r'\b5- und 10-m-Sprintzeiten', r'\b505-Seitenmittel', r'\b505-Seitenwerte', r'\b505-Test',
         r'\bCR-10-Skala', r'\b95-%-Konfidenzintervall', r'\bAbb\. [12]\b', r'\bTab\. [123]\b', r'\bTab\. H[1-5]\b']


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


def de(x, nk=1):
    return (('%.' + str(nk) + 'f') % x).replace('.', ',')


z = []
fehler = []
# (1) bis (3) Messung
RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')
RE_BELEG = re.compile(r'\([^()]*\b(19|20)\d{2}\b[^()]*\)')
gruppe_w = {'5.1': 0, '5.2': 0}
alle_s = []
z.append('%-4s %-4s %6s %6s %8s %7s %5s %5s %5s %5s' % ('Gr.', 'Abs', 'Wörter', 'Sätze', 'längster', 'Median', 'Semi', 'Verw', 'Bel', 'Dopp'))
for g, k, t in ABSAETZE:
    w = len(t.split())
    s = [len(x.split()) for x in saetze(t)]
    alle_s += s
    gruppe_w[g] += w
    semi, verw, bel, dopp = t.count(SEMI), len(RE_REF.findall(t)), len(RE_BELEG.findall(t)), t.count(':')
    z.append('%-4s %-4s %6d %6d %8d %7s %5d %5d %5d %5d' % (g, k, w, len(s), max(s), de(statistics.median(s)), semi, verw, bel, dopp))
    if w > 250:
        fehler.append('%s über 250 Wörter' % k)
    for x in s:
        if x > 32:
            fehler.append('%s: Satz mit %d Wörtern' % (k, x))
    if semi or verw or bel:
        fehler.append('%s: Semikolon, Abschnittsverweis oder Beleg' % k)
gesamt = sum(gruppe_w.values())
z.append('')
z.append('Absatzgruppe 5.1: %d Wörter gegen Richtwert 230 (%+d)' % (gruppe_w['5.1'], gruppe_w['5.1'] - 230))
z.append('Absatzgruppe 5.2: %d Wörter gegen Richtwert 220 (%+d)' % (gruppe_w['5.2'], gruppe_w['5.2'] - 220))
z.append('Kapitel 5: %d Wörter gegen Budget 450 (%+d), %d Sätze, Median %s, längster Satz %d, Sätze über 32: %d'
         % (gesamt, gesamt - 450, len(alle_s), de(statistics.median(alle_s)), max(alle_s), sum(1 for x in alle_s if x > 32)))
if gesamt > 450:
    fehler.append('Kapitel 5 über dem Budget')

# (4) Wortprüfung
text = ' '.join(t for _, _, t in ABSAETZE)
VERBOTEN = [r'\bweil\b', r'\bda\b', r'\bbestätig', r'\bEffekt', r'\bsignifikant', r'\bSignifikanz', r'\bdeutet', r'\bspricht\b',
            r'\bvermutlich', r'\bkönnte', r'\bdürfte', r'\bim Rahmen von', r'\bGegenstand der Untersuchung', r'\bdarüber hinaus',
            r'\bdes Weiteren', r'\bzunächst\b', r'\banschließend', r'\babschließend', r'\bes ist festzuhalten',
            r'\brandomisiert', r'\bklein\w*\b', r'\bmoderat', r'\bgroß\w*\b', r'\bmittler\w* Effekt', r'\bverbessert',
            r'\bErhalt\b', r'\bwirkungslos', r'\bkein Effekt', r'\bsodass\b', r'\bweshalb\b', r'\bResponder', r'\berfüllt\b',
            r'\bleistungsunabhängig', r'\bITT\b', r'\bIntention', r'\bWirkung', r'\bTraining\b', r'\bEthikantrag',
            r'\bgleich wirksam', r'\bMDC\b', r'√']
treffer = []
for m in VERBOTEN:
    for f in re.finditer(m, text):
        treffer.append((m, text[max(0, f.start() - 25):f.end() + 15]))
z.append('')
z.append('Wortprüfung (Deutungs- und Verbotswörter): %d Treffer' % len(treffer))
for m, ctx in treffer:
    z.append('   %s  …%s…' % (m, ctx))

# (5) Zahlen gegen Kennungen
werte = {r['k_kennung']: r for r in csv.DictReader(open(WERTE, encoding='utf-8'))}
z.append('')
z.append('Zahlen gegen Kennungen:')
ok_n = 0
for absatz, zahl, wert, kenn, menge in ZAHLEN:
    if kenn == 'Konstante':
        z.append('  %-3s %-8s Konstante  %s' % (absatz, zahl, menge))
        ok_n += 1
        continue
    kandidaten = []
    if ' bis ' in kenn:
        a, b = re.findall(r'K-08\.(\d)', kenn)
        kandidaten = [k for k in werte if re.match(r'K-08\.[%s-%s]( |$)' % (a, b), k)]
        stimmt = len({k.split(' ')[0] for k in kandidaten}) == int(wert)
    else:
        r = werte.get(kenn)
        if r is None:
            z.append('  %-3s %-8s FEHLT: Kennung %s nicht im Blatt' % (absatz, zahl, kenn))
            fehler.append('Kennung fehlt: ' + kenn)
            continue
        dar = r['darstellung'] + ' | ' + r['bezeichnung']
        muster = r'(?<!\d)(?<!\d,)' + re.escape(wert) + r'(?!\d)(?!,\d)'
        stimmt = re.search(muster, dar) is not None
    z.append('  %-3s %-8s %-11s %-6s %s' % (absatz, zahl, kenn, 'stimmt' if stimmt else 'FEHLER', menge))
    if stimmt:
        ok_n += 1
    else:
        fehler.append('Zahl %s passt nicht zu %s' % (zahl, kenn))
# Vollständigkeit: jede Ziffernzahl und jedes Zahlwort im Text ist erfasst
rest = text
for n in NAMEN:
    rest = re.sub(n, ' ', rest)
ziffern = re.findall(r'[−+]?\d+(?:,\d+)?', rest)
zahlw = [w for w in re.findall(r'[A-Za-zÄÖÜäöüß]+', rest) if w.lower() in ZAHLWORT] + re.findall(r'(?<=neun und )einer\b', rest)
erfasst_z = [x[1] for x in ZAHLEN if re.match(r'[−+]?\d', x[1])]
erfasst_w = [x[1] for x in ZAHLEN if not re.match(r'[−+]?\d', x[1])]
from collections import Counter
dz = Counter(ziffern) - Counter(erfasst_z)
dz2 = Counter(erfasst_z) - Counter(ziffern)
dw = Counter(zahlw) - Counter(erfasst_w)
dw2 = Counter(erfasst_w) - Counter(zahlw)
z.append('  %d von %d Einträgen stimmen. Ziffernzahlen im Text %d, erfasst %d. Zahlwörter im Text %d, erfasst %d.'
         % (ok_n, len(ZAHLEN), len(ziffern), len(erfasst_z), len(zahlw), len(erfasst_w)))
for lab, d in [('im Text, nicht erfasst', dz + dw), ('erfasst, nicht im Text', dz2 + dw2)]:
    if d:
        z.append('  %s: %s' % (lab, dict(d)))
        fehler.append('Zahlen %s: %s' % (lab, dict(d)))

# (6) Objektverweise
OBJEKTE = {'Abb. 1': 'Abb_1_Teilnehmerfluss.png', 'Abb. 2': 'Abb_2_Modell.png', 'Tab. 1': 'Tab_1_Messguete.csv',
           'Tab. 2': 'Tab_2_Stichprobe_Ausgangswerte.csv', 'Tab. 3': 'Tab_3_Gruppenvergleich.csv',
           'Tab. H1': 'Tab_H1a_Versuche.csv', 'Tab. H2': 'Tab_H2a_Adhaerenz_je_Spieler.csv',
           'Tab. H3': 'Tab_H3a_Ausgangswerte_alle.csv', 'Tab. H4': 'Tab_H4c_Varianten.csv',
           'Tab. H5': 'Tab_H5_Schwellenlandschaft.csv'}
BEREITS = {'Tab. 1': '4.4', 'Tab. H1': '4.4', 'Tab. H4': '4.7'}   # im Master schon eingeführt
z.append('')
z.append('Objektverweise:')
gesehen = {}
for g, k, t in ABSAETZE:
    for sn, s in enumerate(saetze(t), 1):
        for m in re.finditer(r'(Abb|Tab)\. (H?\d)', s):
            o = m.group(1) + '. ' + m.group(2)
            if not os.path.exists(os.path.join(OBJ, OBJEKTE.get(o, '-'))):
                fehler.append('Objekt fehlt: ' + o)
            tiefe = s[:m.start()].count('(') - s[:m.start()].count(')')   # Verweis innerhalb einer Klammer
            form = 'Subjekt' if s.startswith(o + ' ') or re.search(r', ' + re.escape(o) + r' ', s) else (
                'Klammer' if tiefe > 0 else 'anders')
            erst = o not in gesehen and o not in BEREITS
            gesehen.setdefault(o, []).append((k, sn, form))
            z.append('  %-7s %s S%-2d %-8s %s' % (o, k, sn, form, 'Erstverweis' if erst else (
                'Wiederaufruf (eingeführt in %s)' % BEREITS[o] if o in BEREITS and len(gesehen[o]) == 1 else 'Wiederaufruf')))
            if not erst and form != 'Klammer':
                fehler.append('%s in %s S%d: Wiederaufruf nicht als Klammer' % (o, k, sn))
for o in ['Abb. 1', 'Tab. 2', 'Abb. 2', 'Tab. 3']:
    if o not in gesehen:
        fehler.append('Textobjekt nicht eingeführt: ' + o)
    elif gesehen[o][0][2] != 'Subjekt':
        fehler.append('Textobjekt nicht als Satzsubjekt eingeführt: ' + o)

# (7) Satzende auf Ziffer: saetze() schützt „Ziffer + Punkt“ als Ordinalzahl und trennt dort nicht.
#     Ein Satz, der auf eine Ziffer endet, verschmölze in der Messung mit dem folgenden.
z.append('')
#     Ebenso ein einzelner Großbuchstabe mit Punkt (Schutz für Initialen, etwa „°C.“).
verdeckt = [text[max(0, m.start() - 20):m.end() + 10]
            for m in re.finditer(r'(?:\d|(?<![A-Za-zÄÖÜäöüß])[A-Z])\.\s+[A-ZÄÖÜ]', text)]
z.append('Satzenden auf Ziffer oder Einzelbuchstaben (von saetze() nicht getrennt): %d' % len(verdeckt))
for v in verdeckt:
    z.append('   …%s…' % v)
    fehler.append('Satzende auf Ziffer: ' + v)

z.append('')
z.append('Ergebnis: ' + ('ohne Befund' if not fehler else 'BEFUNDE: ' + ' | '.join(fehler)))
with open(os.path.join(AUS, 'Textvorschlag_5_2026-09-30.txt'), 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('Textvorschlag Kapitel 5, Messung und Prüfungen (Textvorschlag_5_2026-09-30.py)\n\n' + '\n'.join(z) + '\n')
with open(os.path.join(AUS, 'Textvorschlag_5_2026-09-30.json'), 'w', encoding='utf-8') as fh:
    json.dump({'absaetze': [{'gruppe': g, 'kennung': k, 'text': t} for g, k, t in ABSAETZE],
               'zahlen': [dict(zip(['absatz', 'zahl', 'wert', 'kennung', 'bezugsmenge'], x)) for x in ZAHLEN]},
              fh, ensure_ascii=False, indent=1)
print('\n'.join(z))

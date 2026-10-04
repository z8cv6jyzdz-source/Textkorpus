# -*- coding: utf-8 -*-
"""
Kapitelstruktur_Zaehlung_2026-09-28.py — Überschriftenzählung: Vergleichskorpus, Master (Gliederung v5) und Empfehlung v6
Bachelorarbeit U15-Plyometrie · DSHS Köln · Grundlage des Befunds `02_Befunde\\Kapitelstruktur_Abgleich_2026-09-28`

Was das Skript tut:
(1) Korpus: Die Überschriften der elf Referenzstudien (Bauplan § 0) sind je Studie als Liste hinterlegt, nach Lesen der
    Volltexte am 28.09. bestimmt. Das Skript zieht den Text mit pdftotext und prüft je Überschrift, ob sie als eigene Zeile
    im Volltext steht (Absatztitel: als Zeilenanfang mit Punkt oder Doppelpunkt). Nicht gefundene Überschriften werden
    gemeldet, die Zählung bricht dann ab. Ebenen sind bei Autorenmanuskripten (Hammami, Beato, Negra 2019) am Satzbild
    nicht sicher bestimmbar, die Zuordnung ist dort eine Lesart und so gekennzeichnet.
(2) Master: zählt die Überschriften nach Formatvorlage (Heading 1 bis 3) für die Gliederung v5, ohne den Altbestand
    Kapitel 2 und 3, der mit der Einleitung entfällt (Fassung 17 § 5.2), und misst die Wörter je Unterabschnitt von
    Kapitel 4 (Absätze der Formatvorlage Standard, in python-docx „Normal“, Leerraum-Token wie im Messskript).
(3) Wörter je Überschrift: Korpus aus dem Absatztext je Studie (Bauplan § 7, dort gemessen) geteilt durch die Zahl der
    Überschriften ohne Absatztitel. Eigene Arbeit aus dem Budget 6.350 (Fassung 17 § 5.2).
Aufruf: python Kapitelstruktur_Zaehlung_2026-09-28.py <Ordner Ideen und Studien> <Master.docx> <Ausgabe.txt>
Ohne Semikolon im Skript (chr(59)).
Fassung 2 (28.09., nach der Zweitprüfung): Ebene 4 (Hammami), Sammoud 505-Test, Padrón-Cabo 30-15 IFT, Lloyd „Sprinting Protocols“,
Liu „Yo-Yo“, Bouafif „CoD tests“ entfernt (Zeilenrest, kein Absatztitel), Absatztitel auch innerhalb einer Zeile (Spaltenumbruch),
Limitationsblock je Studie am Wort „limitation“ in der Diskussion gezählt, Empfehlung v6 mit sechs Methodikabschnitten.
"""
import os
import re
import subprocess
import sys
from statistics import median
from docx import Document

STUDIEN, MASTER, OUT = sys.argv[1:4]
SEMI = chr(59)
Z = []


def p(s=''):
    Z.append(s)


# ---------------------------------------------------------------------------------------------------------------------
# (1) Korpus — Überschriften je Studie. Ebene: 1 Kapitel, 2 Unterabschnitt, 3 Unterunterabschnitt, 4 vierte Ebene, A Absatztitel
#     (eingerückter Titel am Absatzanfang, mit Punkt oder Doppelpunkt, nicht im Inhaltsverzeichnis). Datei = Anfang des
#     Dateinamens in `Ideen und Studien`. Absatztext = Bauplan § 7 (Absatztext Kap. 1–7).
# ---------------------------------------------------------------------------------------------------------------------
KORPUS = [
    dict(name='Lloyd et al. (2016)', zs='JSCR', datei='2016 Lloyd et al.', woerter=3586, bem='',
         ueb=[(1, 'INTRODUCTION'), (1, 'METHODS'), (2, 'Experimental Approach to the Problem'), (2, 'Subjects'),
              (2, 'Testing Procedures'), ('A', 'Anthropometrics'), ('A', 'Jump Protocols'), ('A', 'Sprinting Protocols'), (2, 'Training Programs'),
              ('A', 'Traditional Strength Training Group'), ('A', 'Plyometric Training Group'),
              ('A', 'Combined Training Group'), (2, 'Statistical Analyses'), (1, 'RESULTS'), (1, 'DISCUSSION'),
              (1, 'PRACTICAL APPLICATIONS')]),
    dict(name='Hammami et al. (2016)', zs='JSCR, Autorenmanuskript', datei='2016 Hammami', woerter=3984,
         bem='Ebenen unter „Procedures and evaluation“ am Manuskript nicht sicher, Lesart: Ebene 3 und 4',
         ueb=[(1, 'INTRODUCTION'), (1, 'METHODS'), (2, 'Experimental approach to the problem'), (2, 'Subjects'),
              (2, 'Procedures and evaluation'), (3, 'Details of the plyometric training program'), (3, 'Testing Schedule'),
              (3, 'Day 1'), (4, 'Anthropometry'), (4, 'Sprint 4 X 5m (S 4 X 5m)'), (4, '40m sprint performance'), (3, 'Day 2'),
              (3, 'Day 3'), (4, 'Sprint 9-3-6-3-9 m with backward and forward running (SBF)'),
              (4, 'Repeated-shuttle-sprint Ability Test (RSSA)'), (2, 'Statistical Analyses'), (1, 'RESULTS'), (1, 'DISCUSSION'),
              (1, 'PRACTICAL APPLICATIONS')]),
    dict(name='Beato et al. (2018)', zs='JSCR, Autorenmanuskript', datei='2018 Beato', woerter=3525, bem='',
         ueb=[(1, 'Introduction'), (1, 'Methods'), (2, 'Participants'), (2, 'Design and training protocol'),
              (2, 'Statistical analysis'), (1, 'Results'), (1, 'Discussion'), (1, 'Practical applications')]),
    dict(name='Negra et al. (2019)', zs='IJSPP, Autorenmanuskript', datei='2019 Negra', woerter=4356,
         bem='Ebene der sechs Testabschnitte am Manuskript nicht sicher, Lesart: Ebene 3 unter „Experimental design“. '
             'Statistik als eigenes Hauptkapitel',
         ueb=[(1, 'INTRODUCTION'), (1, 'METHODS'), (2, 'Participants'), (2, 'Experimental design'),
              (3, 'Illinois change of direction test'), (3, 'The modified 505 change of direction test'), (3, 'Sprint-time'),
              (3, 'Countermovement jump'), (3, 'Standing-long-jump'), (3, 'Maximal kicking distance test'),
              (2, 'Plyometric jump training'), (1, 'STATISTICAL ANALYSES'), (1, 'RESULTS'), (1, 'DISCUSSION'),
              (2, 'Change of direction'), (2, 'Speed performance'), (2, 'Jumping tests'), (2, 'Maximal kicking distance'),
              (1, 'PRACTICAL APPLICATIONS'), (1, 'CONCLUSIONS')]),
    dict(name='Negra et al. (2020)', zs='JSHS', datei='2020 Negra', woerter=4256, bem='nummerierte Unterabschnitte',
         ueb=[(1, '1. Introduction'), (1, '2. Methods'), (2, '2.1. Participants'), (2, '2.2. Procedures'),
              (2, '2.3. Sprint testing'), (2, '2.4. The Illinois change of direction test'), (2, '2.5. SJ and CMJ'),
              (2, '2.6. Multiple MB5'), (2, '2.7. SLJ'), (2, '2.8. Half-squat'), (2, '2.9. Maximal strength assessment'),
              (2, '2.10. RT and PT interventions'), (2, '2.11. Statistical analysis'), (1, '3. Results'),
              (2, '3.1. Effects of 12 weeks of RT vs. PT on measures of muscle'), (2, '3.2. Time course of improvements'),
              (1, '4. Discussion'), (1, '5. Conclusion')]),
    dict(name='Aloui et al. (2022)', zs='Front. Physiol.', datei='2022 Aloui', woerter=3383,
         bem='Tests nur per Verweis beschrieben (Bauplan § 8)',
         ueb=[(1, 'INTRODUCTION'), (1, 'MATERIALS AND METHODS'), (2, 'Participants'), (2, 'Experimental Design'),
              (2, 'Combined Plyometric and Short Sprint'), (2, 'Testing Schedule'), (2, 'Statistical Analyses'),
              (1, 'RESULTS'), (2, 'Training Effects on Sprint Performance'), (2, 'Training Effects on Jump Performance'),
              (2, 'Training Effects on Change-of-Direction'), (2, 'Training Effects on Repeated Shuttle'),
              (2, 'Training Effects on Balance Performance'), (1, 'DISCUSSION'),
              (2, 'Effect of Training on Sprint Performance'), (2, 'Effect of Training on Jump Performance'),
              (2, 'Effect of Training on Repeated Shuttle'), (2, 'Effect of Training on'),
              (2, 'Effect of Training on Balance'), (1, 'CONCLUSION')]),
    dict(name='Liu et al. (2024)', zs='JSSM', datei='2024 Liu', woerter=4313, bem='Tests als Absatztitel mit Doppelpunkt',
         ueb=[(1, 'Introduction'), (1, 'Methods'), (2, 'Study design and experimental approach'), (2, 'Participants'),
              (2, 'Offseason training programs'), (2, 'Physical fitness assessments'), ('A', 'Countermovement jump'),
              ('A', '30-m linear sprint test'), ('A', 'Yo-Yo Intermittent recovery test'), (2, 'Statistical analysis'), (1, 'Results'), (1, 'Discussion'),
              (1, 'Conclusion')]),
    dict(name='Moran et al. (2024)', zs='PLOS ONE', datei='2024 Moran', woerter=3983, bem='',
         ueb=[(1, 'Introduction'), (1, 'Methods'), (2, 'Experimental approach'), (2, 'Participants'), (2, 'Procedures'),
              ('A', 'Anthropometry'), ('A', 'Horizontal jump'), ('A', 'Vertical jump'), ('A', 'Sprint test'),
              ('A', 'Change-of-direction test'), (2, 'Statistical analyses'), ('A', 'Data analysis'), (1, 'Results'),
              (1, 'Discussion'), (1, 'Conclusion')]),
    dict(name='Sammoud et al. (2024)', zs='BMC SSMR', datei='2024 Sammoud', woerter=4571, bem='',
         ueb=[(1, 'Methods'), (2, 'Experimental approach to the problem'), (2, 'Participants'),
              (2, 'Anthropometric measures'), (2, 'Physical fitness tests'), (3, 'Countermovement jump'),
              (3, 'Standing long jump'), (3, 'Single leg hop test for distance with dominant'),
              (3, 'The 505 change of direction test'),
              (2, 'Plyometric jump training'), (2, 'Soccer training protocol'), (2, 'Statistical analyses'), (1, 'Results'),
              (1, 'Discussion'), (2, 'Jumping ability'), (2, 'Change of direction'), (2, 'Asymmetry score'),
              (2, 'Strengths and limitations'), (1, 'Conclusions')]),
    dict(name='Bouafif et al. (2026)', zs='PLOS ONE', datei='2026 Bouafif', woerter=5448,
         bem='weitere Tests als Absatztitel im PDF-Satz nicht sicher abgrenzbar, ein geprüftes Beispiel',
         ueb=[(1, 'Introduction'), (1, 'Materials and methods'), (2, 'Subjects'), (2, 'Procedure'), (2, 'Measurements'),
              ('A', 'Dynamic balance'), (2, 'Training program'), (2, 'Statistical analysis'),
              (1, 'Results'), (1, 'Discussion'), (1, 'Conclusion')]),
    dict(name='Padrón-Cabo et al. (2025)', zs='JSCR', datei='2025 Padron', woerter=3995, bem='',
         ueb=[(1, 'Introduction'), (1, 'Methods'), (2, 'Experimental Approach to the Problem'), (2, 'Subjects'),
              (2, 'Procedures'), ('A', 'Vertical Jump Tests'), ('A', 'Linear Sprint Test'), ('A', 'Modified 505 Test'),
              ('A', '30-15 Intermittent Fitness Test'), (2, 'Statistical Analyses'), (1, 'Results'),
              (2, 'Vertical Jump Performance'), (2, 'Sprint Performance'), (2, 'Modified 505 Test'),
              (2, '30-15 Intermittent Fitness Test'), (1, 'Discussion'), (1, 'Practical Applications')]),
]
# Sammoud: die Einleitung trägt im PDF keine Überschrift „Introduction“ (BMC-Satz), sie wird als Kapitel gezählt.
# Bouafif: Introduction steht im PDF, die Tests als Absatztitel, hier zwei geprüfte Beispiele.
ZUSATZ_KAPITEL = {'Sammoud et al. (2024)': 1}


def volltext(datei):
    kand = [f for f in os.listdir(STUDIEN) if f.startswith(datei) and f.lower().endswith('.pdf')]
    if len(kand) != 1:
        raise SystemExit('ABBRUCH: %d Dateien beginnen mit %s' % (len(kand), datei))
    r = subprocess.run(['pdftotext', os.path.join(STUDIEN, kand[0]), '-'], capture_output=True, text=True)
    return r.stdout, kand[0]


def steht(zeilen, titel, ebene):
    t = titel.strip()
    for z in zeilen:
        s = z.strip()
        if ebene == 'A':
            if (t + '. ') in s or (t + ': ') in s or s == t + '.' or s == t + ':':
                return True
        elif s == t:
            return True
    return False


p('Kapitelstruktur — Überschriftenzählung (28.09.2026), Skript Kapitelstruktur_Zaehlung_2026-09-28.py')
p('Ebene 1 Kapitel · 2 Unterabschnitt · 3 Unterunterabschnitt · A Absatztitel (kein Verzeichniseintrag)')
p()
p('(1) Vergleichskorpus — elf Referenzstudien, Überschriften am extrahierten Volltext geprüft')
p('%-28s %-24s %4s %4s %4s %4s  %-11s %-8s %-9s %-12s %-22s %s' % (
    'Studie', 'Zeitschrift', 'E1', 'E2', 'E3+4', 'Abs', 'Meth. E2', 'Erg. E2', 'Disk. E2', 'Limit.', 'Schluss', 'Wörter/Überschr.'))
fehl = []
meth_e2 = []
wpu = []
zusammen = {}
for st in KORPUS:
    text, dateiname = volltext(st['datei'])
    zeilen = text.split('\n')
    for eb, ti in st['ueb']:
        if not steht(zeilen, ti, eb):
            fehl.append('%s: „%s“ (Ebene %s) nicht als Zeile gefunden in %s' % (st['name'], ti, eb, dateiname))
    e1 = sum(1 for eb, _ in st['ueb'] if eb == 1) + ZUSATZ_KAPITEL.get(st['name'], 0)
    e2 = sum(1 for eb, _ in st['ueb'] if eb == 2)
    e3 = sum(1 for eb, _ in st['ueb'] if eb == 3)
    e4 = sum(1 for eb, _ in st['ueb'] if eb == 4)
    ea = sum(1 for eb, _ in st['ueb'] if eb == 'A')
    # Limitationsblock: Wort „limitation“ zwischen der Diskussionsüberschrift und dem Literaturverzeichnis
    tl = text.lower()
    d_idx = [m.start() for m in re.finditer(r'\n\s*(?:\d\.\s)?discussion\s*\n', tl)]
    r_idx = [m.start() for m in re.finditer(r'\n\s*references\s*\n', tl)]
    disk = tl[d_idx[-1]:(r_idx[-1] if r_idx and r_idx[-1] > d_idx[-1] else len(tl))] if d_idx else ''
    lim_ueb = any('limitation' in ti.lower() for _, ti in st['ueb'])
    lim = 'Überschrift' if lim_ueb else ('Absatz' if 'limitation' in disk else 'kein Block')
    # Unterabschnitte je Kapitel: Position der Kapitelüberschriften bestimmt die Zugehörigkeit
    kap = None
    je = {}
    for eb, ti in st['ueb']:
        if eb == 1:
            kap = ti.upper().lstrip('0123456789. ')
            je[kap] = [0, 0]
        elif kap is not None:
            if eb == 2:
                je[kap][0] += 1
            elif eb in (3, 4):
                je[kap][1] += 1
    m = [k for k in je if 'METHOD' in k]
    r = [k for k in je if k.startswith('RESULT')]
    d = [k for k in je if k.startswith('DISCUSSION')]
    schluss = [k for k in je if k.startswith(('PRACTICAL', 'CONCLUSION'))]
    m2, m3 = je[m[0]] if m else (0, 0)
    r2 = je[r[0]][0] if r else 0
    d2 = je[d[0]][0] if d else 0
    ohne_abs = e1 + e2 + e3 + e4
    w = st['woerter'] / ohne_abs
    meth_e2.append(m2)
    wpu.append(w)
    zusammen[st['name']] = dict(m2=m2, m3=m3, ea=ea, r2=r2, d2=d2, schluss=schluss, e1=e1, e2=e2, e3=e3 + e4, w=w, lim=lim)
    p('%-28s %-24s %4d %4d %4d %4d  %-11s %-8s %-9s %-12s %-22s %6.0f' % (
        st['name'], st['zs'], e1, e2, e3 + e4, ea, '%d (+%d E3/4)' % (m2, m3) if m3 else str(m2), str(r2), str(d2), lim,
        ' + '.join(k.title() for k in schluss), w))
if fehl:
    p()
    p('NICHT GEFUNDEN:')
    for f in fehl:
        p('  ' + f)
    open(OUT, 'w', encoding='utf-8').write('\n'.join(Z) + '\n')
    raise SystemExit('ABBRUCH: %d Überschriften nicht gefunden' % len(fehl))
p()
p('Zusammenfassung Korpus (n = 11), %d Überschriften und Absatztitel hinterlegt und gefunden:' % sum(len(st['ueb']) for st in KORPUS))
p('  Stichprobe als eigener Abschnitt: %d von 11 · Design als eigener Abschnitt (Experimental Approach, Experimental Design, Study design, Design): %d von 11' % (
    sum(1 for st in KORPUS if any(ti in ('Participants', 'Subjects', '2.1. Participants') for _, ti in st['ueb'])),
    sum(1 for st in KORPUS if any(('Experimental' in ti or 'Study design' in ti or ti.startswith('Design')) and eb == 2 for eb, ti in st['ueb']))))
p('  Unterabschnitte 2. Ebene in der Methodik: Median %s, Spanne %d bis %d' % (
    str(median(meth_e2)).replace('.', ','), min(meth_e2), max(meth_e2)))
p('  Testbeschreibung: Absatztitel %d · Zwischentitel der Ebene 3 oder 4 %d · eigene Unterabschnitte 2. Ebene %d (Negra 2020) · '
  'ohne Überschrift oder nur per Verweis %d (Beato, Aloui)' % (
      sum(1 for v in zusammen.values() if v['ea'] > 0),
      sum(1 for v in zusammen.values() if v['m3'] > 0), 1, 2))
p('  Ergebnisse ohne Unterabschnitte: %d von 11 · Diskussion ohne Unterabschnitte: %d von 11' % (
    sum(1 for v in zusammen.values() if v['r2'] == 0), sum(1 for v in zusammen.values() if v['d2'] == 0)))
p('  Limitationen: Überschrift %d · Absatz %d · kein Block %d (%s)' % (
    sum(1 for v in zusammen.values() if v['lim'] == 'Überschrift'), sum(1 for v in zusammen.values() if v['lim'] == 'Absatz'),
    sum(1 for v in zusammen.values() if v['lim'] == 'kein Block'),
    ', '.join(k for k, v in zusammen.items() if v['lim'] == 'kein Block')))
p('  Schlusskapitel (Practical Applications und/oder Conclusion): %d von 11' % sum(
    1 for v in zusammen.values() if v['schluss']))
p('  Dritte oder vierte Verzeichnisebene vorhanden: %d von 11 (Hammami, Negra 2019, Sammoud, Lesart bei den Manuskripten)' % sum(
    1 for v in zusammen.values() if v['e3'] > 0))
p('  Wörter je Überschrift (ohne Absatztitel): Median %.0f, Spanne %.0f bis %.0f' % (median(wpu), min(wpu), max(wpu)))

# ---------------------------------------------------------------------------------------------------------------------
# (2) Master — Gliederung v5 (Überschriften nach Formatvorlage, ohne Altbestand 2, 2.x, 3)
# ---------------------------------------------------------------------------------------------------------------------
p()
p('(2) Master — Überschriften der Gliederung v5 nach Formatvorlage, ohne den Altbestand Kapitel 2 und 3')
doc = Document(MASTER)
ALT = re.compile(r'^(2|3)(\.\d+)*\s')
zaehl = {1: [], 2: [], 3: []}
woerter = {}
aktuell = None
for para in doc.paragraphs:
    sn = para.style.name
    t = para.text.strip()
    m = re.match(r'Heading (\d)', sn)
    if m:
        eb = int(m.group(1))
        if not t or ALT.match(t) or not re.match(r'^\d', t):
            aktuell = None
            continue
        zaehl[eb].append(t)
        aktuell = t.split()[0]
        woerter[aktuell] = 0
        continue
    if aktuell and sn == 'Normal' and t and not re.match(r'^(Tab|Abb)\. [A-Z]?\d+\.', t):
        woerter[aktuell] += len(t.split())
p('  Ebene 1: %d  %s' % (len(zaehl[1]), ' · '.join(zaehl[1])))
p('  Ebene 2: %d  %s' % (len(zaehl[2]), ' · '.join(zaehl[2])))
p('  Ebene 3: %d  %s' % (len(zaehl[3]), ' · '.join(zaehl[3])))
ges = len(zaehl[1]) + len(zaehl[2]) + len(zaehl[3])
p('  Überschriften gesamt (v5, Kapitel 1 bis 7 in Arbeitsnummern): %d' % ges)
p('  Wörter je Unterabschnitt in Kapitel 4 (Absätze Standard, gemessen): ' + ' · '.join(
    '%s %d' % (k, v) for k, v in woerter.items() if k.startswith('4.')))
p('  Leere Elternüberschrift (0 Wörter eigener Text, direkt gefolgt von Ebene 3): ' + ', '.join(
    k for k, v in woerter.items() if v == 0 and k.startswith('4.') and any(x.startswith(k + '.') for x in woerter)))
p('  Wörter je Überschrift bei 6.350 Wörtern Budget: %.0f' % (6350 / ges))

# ---------------------------------------------------------------------------------------------------------------------
# (3) Empfehlung v6 — Überschriften und Budgets je Abschnitt (Festlegungen aus Fassung 17 § 5.2, Summen gerechnet)
# ---------------------------------------------------------------------------------------------------------------------
p()
p('(3) Gliederung v6 — Überschriften je Ebene und Budgets als Summen der Blöcke (Fassung 17 § 5.2)')
UNTER = {'4.1': 300, '4.2': 215, '4.3': 340, '4.4': 420, '4.5.1': 420, '4.5.2': 150, '4.6': 155, '4.7': 550,
         '5.1': 230, '5.2': 220, '6.1': 700, '6.2': 400, '6.3': 500, '7': 250, '1': 1500}
V6 = [('1', 'Einleitung', ['1']),
      ('2.1', 'Studiendesign', ['4.1']), ('2.2', 'Stichprobe', ['4.2']),
      ('2.3', 'Untersuchungsablauf', ['4.3']), ('2.4', 'Leistungsdiagnostik', ['4.4']),
      ('2.5', 'Trainingsintervention und Begleitbedingungen', ['4.5.1', '4.5.2', '4.6']),
      ('2.6', 'Statistische Auswertung', ['4.7']),
      ('3', 'Ergebnisse', ['5.1', '5.2']),
      ('4.1', 'Einordnung der Ergebnisse', ['6.1']),
      ('4.2', 'Methodendiskussion, Stärken und Limitationen', ['6.2', '6.3']),
      ('5', 'Fazit und Ausblick', ['7'])]
summe = 0
for nr, titel, bl in V6:
    b = sum(UNTER[x] for x in bl)
    summe += b
    p('  %-4s %-46s Budget %5d  aus %s' % (nr, titel, b, ' + '.join(bl)))
e1 = 5
e2 = sum(1 for nr, _, _ in V6 if nr.count('.') == 1)
p('  Summe Budgets: %d (Vorgabe 6.350)' % summe)
p('  Überschriften v6: Ebene 1 %d · Ebene 2 %d · Ebene 3 0 · gesamt %d (v5: %d) · Wörter je Überschrift %.0f' % (
    e1, e2, e1 + e2, ges, 6350 / (e1 + e2)))
p('  Varianten: Diskussion ohne Unterabschnitte gesamt %d (%.0f je Überschrift) · zusätzlich 4.3 und 4.4 zusammengelegt %d (%.0f) · '
  'Ergebnisse mit zwei Unterabschnitten %d (%.0f)' % (e1 + e2 - 2, 6350 / (e1 + e2 - 2), e1 + e2 - 3, 6350 / (e1 + e2 - 3),
                                                  e1 + e2 + 2, 6350 / (e1 + e2 + 2)))
if summe != 6350:
    raise SystemExit('ABBRUCH: Budgetsumme %d' % summe)
open(OUT, 'w', encoding='utf-8').write('\n'.join(Z) + '\n')
print('\n'.join(Z))

# -*- coding: utf-8 -*-
"""
Projektanweisungen_Vergleich_F16_F17_2026-09-28.py — Vergleich Fassung 16 gegen Fassung 17 und elf Prüfungen mit Abbruch
(Task Steuerdokumente 28.09., Übergabe `04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 6).

(a) kein Semikolon außer zwischen Quellen in einer Klammer und im zitierten Zeichen der Regel in § 8
(b) keine Ergebniszahl in § 3 und § 11.2a
(c) jede Datei der Ordnerliste Claude\\ (ohne _Archiv) steht in § 1.3, unter „Veraltet“ oder passt auf ein Muster
(d) Wortzahlen in § 5.2 und im Kopf gleich der Ausgabe des Messskripts Fassung 3
(e) Budgetarithmetik: Kapitelbudgets 6.350, Unterbudgets Kapitel 4 2.550 (2.000 und 550), Kapitel 5 450, Kapitel 6 1.600
(f) jede Angabe „§ x“ oder „§ x.y“ ohne fremden Dokumentnamen davor zeigt auf einen vorhandenen Paragrafen
(g) jede Entscheidung aus § 1 der Übergabe und jede Klickantwort steht in § 13 mit Datum
(h) jeder Punkt des Blocks „G32 j“ (Zeile „Steuerdokumente“ in Textvorschlag 4.7 § 7) hat einen Ort
(i) die Trefferliste „Durchgehend“ ist abgearbeitet (jeder Treffer ersetzt, Arbeitsnummer oder historisch)
(j) die Seitenrechnung ist per Skript gerechnet, jede Zeile als Modellrechnung oder Festlegung gekennzeichnet
(k) die Befunde der Zweitprüfung (1 bis 33) und die Punkte aus Rev. 114 (Task 7 neu) sind umgesetzt oder einem Schritt zugeordnet
    dazu die Befunde der übergreifenden Zweitprüfung, die Fassung 17 betreffen (Z2: 4, 5, 27, 36, 40), und die Klicks von 19:25

Aufruf: python Projektanweisungen_Vergleich_F16_F17_2026-09-28.py <F16.md> <F17.md> <Ordnerliste.txt>
        <Manuskriptstand.csv> <Seitenmodell.csv> <Textvorschlag_4.7_2026-09-26.md> <Ausgabe.txt>
Ohne Semikolon im Skript (chr(59)). Fassung 2 (28.09., nach der Zweitprüfung: (e) Restbudget 2.300, (g) Nr. 33 bis 39, (k) neu).
Fassung 3 (28.09., nach der übergreifenden Zweitprüfung): (g) Nr. 16, 40 und 41, (k) Befunde 4, 5, 27, 36 und 40 und die Klicks
von 19:25 (Erratum, Verdünnungslogik), Ordnerliste neu aus dem Gerät (Befund 29).
"""
import csv
import difflib
import re
import sys

F16, F17, ORDNER, M_CSV, S_CSV, TV47, OUT = sys.argv[1:8]
SEMI = chr(59)
f16 = open(F16, encoding='utf-8').read()
f17 = open(F17, encoding='utf-8').read()
aus = []
fehler = []


def bereich(t, start, ende):
    i0 = t.index(start)
    i1 = t.index(ende, i0 + len(start))
    return t[i0:i1]


def abschnitte(t):
    teile, aktuell, puffer = [], 'Kopf', []
    for z in t.split('\n'):
        if z.startswith('#'):
            teile.append((aktuell, puffer))
            aktuell, puffer = z.strip('# ').strip(), []
        else:
            puffer.append(z)
    teile.append((aktuell, puffer))
    return [(k, [a.strip() for a in '\n'.join(p).split('\n\n') if a.strip()]) for k, p in teile]


def ergebnis(name, treffer, zusatz=''):
    if treffer:
        fehler.append(name)
        aus.extend('   ' + x for x in treffer)
    aus.append('   Ergebnis: %s%s' % ('NICHT BESTANDEN' if treffer else 'bestanden', zusatz))


# ------------------------------------------------------------------ Vergleich
a16 = dict(abschnitte(f16))
a17 = abschnitte(f17)
aus.append('VERGLEICH Fassung 16 gegen Fassung 17 (absatzweise je Paragraf)')
aus.append('')
geaendert = 0
for kopf, absaetze in a17:
    alt = a16.get(kopf)
    if alt is None:
        nr = kopf.split(' ')[0]
        kand = [k for k in a16 if k.split(' ')[0] == nr]
        alt = a16[kand[0]] if kand else []
        aus.append(('[Überschrift geändert] %s  →  %s' % (kand[0], kopf)) if kand else '[neu] ' + kopf)
    neu = [a for a in absaetze if a not in alt]
    weg = [a for a in alt if a not in absaetze]
    if neu or weg:
        geaendert += 1
        aus.append('§ %s: %d Absatz/Absätze ersetzt oder entfernt, %d neu oder geändert' % (kopf, len(weg), len(neu)))
        for a in neu:
            aus.append('   + ' + (a[:170] + ' …' if len(a) > 170 else a))
nummern17 = [x.split(' ')[0] for x, _ in a17 if x[0].isdigit()]
entfallen = [k for k in a16 if k not in dict(a17) and not (k[0].isdigit() and k.split(' ')[0] in nummern17)]
for k in entfallen:
    aus.append('[entfallen] ' + k)
unver = [k for k, _ in a17 if k in a16 and a16[k] == dict(a17)[k]]
aus.append('')
aus.append('Paragrafen mit Änderungen: %d, unverändert: %d' % (geaendert, len(unver)))
aus.append('Unverändert: ' + ' · '.join(k.split(' ')[0] if k[0].isdigit() else k[:30] for k in unver))
zd = list(difflib.unified_diff(f16.split('\n'), f17.split('\n'), lineterm='', n=0))
aus.append('Zeilendiff: %d Zeilen entfernt, %d Zeilen hinzugefügt' % (
    sum(1 for z in zd if z.startswith('-') and not z.startswith('---')), sum(1 for z in zd if z.startswith('+') and not z.startswith('+++'))))

# ------------------------------------------------------------------ (a) Semikolon
aus.append('')
aus.append('PRÜFUNG (a) Semikolon außerhalb der Zitiersyntax')
ta = []
for nr, z in enumerate(f17.split('\n'), 1):
    for m in re.finditer(SEMI, z):
        p = m.start()
        if z[max(0, p - 1):p + 2] == '„' + SEMI + '“':
            continue
        offen = z.rfind('(', 0, p)
        zu = z.find(')', p)
        if offen != -1 and zu != -1 and z.rfind(')', 0, p) < offen:
            if re.match(r'\s*[A-ZÄÖÜ][^()]*?\b(19|20)\d\d\b', z[p + 1:zu]):
                continue
        ta.append('Zeile %d: …%s…' % (nr, z[max(0, p - 40):p + 40]))
ergebnis('(a)', ta, ' (%d Fundstellen, Semikola gesamt %d)' % (len(ta), f17.count(SEMI)))

# ------------------------------------------------------------------ (b) Ergebniszahlen
aus.append('')
aus.append('PRÜFUNG (b) keine Ergebniszahl in § 3 und § 11.2a')
mb = re.compile(r'[−+-]?\d+,\d+\s*(s\b|cm\b|%)|\bp\s*[=<>]\s*0,\d|\bW\s*=\s*0,\d')
tb = []
for name, (s, e) in {'§ 3': ('# 3. DATENSTAND', '# 4. '), '§ 11.2a': ('## 11.2a ', '## 11.2b ')}.items():
    for m in mb.finditer(bereich(f17, s, e)):
        tb.append('%s: %s' % (name, m.group(0)))
ergebnis('(b)', tb)

# ------------------------------------------------------------------ (c) Dokumentenkarte
aus.append('')
aus.append('PRÜFUNG (c) jede Datei der Ordnerliste in § 1.3, unter „Veraltet“ oder auf einem Muster der Werkzeugskripte')
liste = [z.strip() for z in open(ORDNER, encoding='utf-8') if z.strip() and not z.startswith('#')]
karte = bereich(f17, '## 1.3 Dokumentenkarte', '## 1.4 ')
roh = set(re.findall(r'`([^`]+)`', karte))
roh |= set(re.findall(r'[A-Za-z0-9ÄÖÜäöüß_.\-…*]+_\d{4}-\d{2}-\d{2}[A-Za-z0-9_.\-]*', karte))
roh |= set(re.findall(r'\b[A-Za-z0-9ÄÖÜäöüß\-]+_[A-Za-z0-9ÄÖÜäöüß_.\-]+', karte))
marken = set()
for r in roh:
    for teil in re.split(r'[\\/ ,]+', r):
        teil = teil.strip('`() .')
        if len(teil) < 4:
            continue
        marken.add(re.sub(r'\.(md|docx|pdf|py|txt|csv|xlsx|R|zip|png|sps|tsv|ps1)$', '', teil))
ORD = {'Claude', '00_Steuerung', '01_Verfahren', '02_Befunde', '03_Skripte', '04_Uebergaben', '05_Protokolle', '06_Abbildungen', '_Archiv'}
marken = {m for m in marken if m not in ORD and len(re.sub(r'[*….]', '', m)) >= 4}


def passt(marke, name):
    if '*' in marke or '…' in marke:
        teile = re.split(r'[*…]', marke.replace('B0…B9', 'B§'))
        rx = '^' + '.*'.join(re.escape(x).replace('§', '[0-9]') for x in teile) + '.*$'
        return re.match(rx, name) is not None
    return name == marke or name.startswith(marke + '_') or name.startswith(marke + '.')


tc = []
for pfad in liste:
    namen = [re.sub(r'\.[A-Za-z0-9]+$', '', x) for x in pfad.split('/')]
    if not any(passt(m, n) for m in marken for n in namen):
        tc.append('nicht zugeordnet: ' + pfad)
ergebnis('(c)', tc, ' (%d Dateien geprüft, %d ohne Zuordnung)' % (len(liste), len(tc)))

# ------------------------------------------------------------------ (d) Wortzahlen
aus.append('')
aus.append('PRÜFUNG (d) Wortzahlen in § 5.2 und im Kopf gegen die Ausgabe des Messskripts Fassung 3')
w = {r['arbeitsnummer']: int(r['woerter']) for r in csv.DictReader(open(M_CSV, encoding='utf-8'))}
soll = {'4.1': w['4.1'], '4.2': w['4.2'], '4.3': w['4.3'], '4.4 mit 4.4.1 bis 4.4.3': w['4.4'] + w['4.4.1'] + w['4.4.2'] + w['4.4.3'],
        '4.5.1': w['4.5.1'], '4.5.2': w['4.5.2'], '4.6': w['4.6'], '4.7': w['4.7']}
soll['Kapitel 4 (4.1 bis 4.6)'] = sum(soll[k] for k in ['4.1', '4.2', '4.3', '4.4 mit 4.4.1 bis 4.4.3', '4.5.1', '4.5.2', '4.6'])
soll['mit 4.7'] = soll['Kapitel 4 (4.1 bis 4.6)'] + soll['4.7']
alt_w = sum(w[k] for k in ['2', '2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.5', '3'])
ges_w = sum(v for k, v in w.items() if re.match(r'^[1-7](\.|$)', k))


def de(n):
    return '{:,}'.format(n).replace(',', '.')


b52 = bereich(f17, '## 5.2 Wortbudget', '## 5.3 ')
stand = b52[b52.index('**Stand am Master'):b52.index('### Was das bedeutet')]
td = []
gep = 0
for etikett, wert in soll.items():
    m = re.search(re.escape(etikett) + r'\)?\s+(\d{1,3}(?:\.\d{3})+|\d+)(?![\d.]\d)', stand)
    if not m:
        td.append('%s: im Satz „Stand am Master“ nicht gefunden' % etikett)
        continue
    gep += 1
    if int(m.group(1).replace('.', '')) != wert:
        td.append('%s: § 5.2 nennt %s, Messung %d' % (etikett, m.group(1), wert))
for erw in ['mit %s Wörtern im Master' % de(alt_w), 'Absatztext mit Altbestand %s' % de(ges_w)]:
    gep += 1
    if erw not in stand:
        td.append('nicht gefunden: ' + erw)
kopf = f17[:f17.index('# 1. ROLLE')]
for k, lab in [('4.1', '4.1'), ('4.2', '4.2'), ('4.3', '4.3'), ('4.4 mit 4.4.1 bis 4.4.3', '4.4'), ('4.5.1', '4.5.1'),
               ('4.5.2', '4.5.2'), ('4.6', '4.6'), ('4.7', '4.7')]:
    gep += 1
    if not re.search(r'(^|· |\. |\*\* )' + re.escape(lab) + r' ' + str(soll[k]) + r'\b', kopf, re.M):
        td.append('Kopf (C): %s %d nicht gefunden' % (lab, soll[k]))
for erw in ['zusammen %s gegen 2.000' % de(soll['Kapitel 4 (4.1 bis 4.6)']), 'mit 4.7 %s gegen 2.550' % de(soll['mit 4.7'])]:
    gep += 1
    if erw not in kopf:
        td.append('Kopf (C): nicht gefunden: ' + erw)
ergebnis('(d)', td, ' (%d Werte geprüft)' % gep)

# ------------------------------------------------------------------ (e) Budgetarithmetik
aus.append('')
aus.append('PRÜFUNG (e) Budgetarithmetik')
te = []
tab = [z for z in b52.split('\n') if z.startswith('| ') and re.match(r'^\| \d ', z)]
bud = [int(re.findall(r'\*\*(\d{1,3}(?:\.\d{3})?)\*\*', z)[0].replace('.', '')) for z in tab]
kor = [int(z.split('|')[2].strip().replace('.', '')) for z in tab]
if sum(bud) != 6350:
    te.append('Kapitelbudgets summieren sich zu %d statt 6.350' % sum(bud))
if '**6.350**' not in b52 or '**%s**' % de(sum(kor)) not in b52:
    te.append('Summenzeile der Tabelle stimmt nicht (Budget 6.350, Korpus %s)' % de(sum(kor)))
ub = re.search(r'\*\*Unterbudgets \(Vorgabe\):\*\*(.*)', b52).group(1)
u = {m.group(1): int(m.group(2).replace('.', '')) for m in re.finditer(r'(\d(?:\.\d){1,2}|\b7\b) (\d{1,3}(?:\.\d{3})?)\b', ub)}
k4o = sum(u[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.5.1', '4.5.2', '4.6'])
if k4o != 2000 or k4o + u['4.7'] != 2550 or bud[1] != 2550:
    te.append('Kapitel 4: %d + %d gegen Kapitelbudget %d' % (k4o, u['4.7'], bud[1]))
if u['5.1'] + u['5.2'] != 450 or bud[2] != 450:
    te.append('Kapitel 5: %d gegen %d' % (u['5.1'] + u['5.2'], bud[2]))
if u['6.1'] + u['6.2'] + u['6.3'] != 1600 or bud[3] != 1600:
    te.append('Kapitel 6: %d gegen %d' % (u['6.1'] + u['6.2'] + u['6.3'], bud[3]))
if u.get('7') != 250 or bud[4] != 250:
    te.append('Kapitel 7: %s gegen %d' % (u.get('7'), bud[4]))
if bud[0] != 1500:
    te.append('Einleitung: %d statt 1.500' % bud[0])
if '%s Wörtern Budget' % de(bud[2] + bud[3] + bud[4]) not in b52 or bud[2] + bud[3] + bud[4] != 2300:
    te.append('„2.300 Wörtern Budget“ für Kapitel 5 bis 7 fehlt oder rechnet nicht')
ergebnis('(e)', te, ' (Kapitel %s = %d, Kapitel 4 %d + %d, Kapitel 5 %d, Kapitel 6 %d, Kapitel 7 %d)' % (
    ' + '.join(str(x) for x in bud), sum(bud), k4o, u['4.7'], u['5.1'] + u['5.2'], u['6.1'] + u['6.2'] + u['6.3'], u['7']))

# ------------------------------------------------------------------ (f) Paragrafenverweise
aus.append('')
aus.append('PRÜFUNG (f) interne Paragrafenverweise zeigen auf vorhandene Paragrafen')
vorhanden = set()
for z in f17.split('\n'):
    m = re.match(r'^#+\s+(\d+[a-z]?(?:\.\d+[a-z]?)*)\.?\s', z)
    if m:
        vorhanden.add(m.group(1))
FREMD = ['Auswertungsplan', 'Umfangsdokument', 'Voraussetzungsprüfungen', 'Voraussetzungspruefungen', 'Bauplan', 'Berichtsraster',
         'Raster', 'Gliederung', 'Plan', 'Übergabe', 'Uebergabe', 'Textvorschlag', 'Befund', 'Vorarbeit', 'Prüfungsordnung',
         'Spezifikation', 'Kennzahlenblatt', 'Auswertungsverfahren', 'Stilprofil', 'CONSORT_Auswertung', 'Prüfprotokoll',
         'Leitfaden', 'Skill', 'Rahmenplan', 'Messskript', 'Seitenmodell', 'Nachtrag', 'Vorspann', 'Fassung 16', 'Anlage']
tf = []
nint = 0
for nr, z in enumerate(f17.split('\n'), 1):
    for m in re.finditer(r'§\s(\d+[a-z]?(?:\.\d+[a-z]?)?)', z):
        vor = z[max(0, m.start() - 55):m.start()]
        nach = z[m.end():m.end() + 8]
        if any(f in vor for f in FREMD) or nach.startswith(' dort') or re.search(r'§\s\d+(\.\d+)?\s(mit|und)\s$', vor):
            continue
        # Tabellenzeile: Dokumentname in der ersten Zelle, Nachtragsvermerk: Dokumentname vor dem letzten Gedankenstrich
        if z.startswith('| ') and any(f in z.split('|')[1] for f in FREMD + ['_2026-', 'Textvorschlag_', 'Uebergabe_']):
            continue
        strich = z.rfind(' — ', 0, m.start())
        if strich != -1 and any(f in z[max(0, strich - 40):strich] for f in FREMD):
            continue
        nint += 1
        if m.group(1) not in vorhanden:
            tf.append('Zeile %d: „§ %s“ ohne Paragraf (…%s…)' % (nr, m.group(1), z[max(0, m.start() - 50):m.end() + 10]))
ergebnis('(f)', tf, ' (%d interne Verweise geprüft, Paragrafen: %s)' % (nint, ' '.join(sorted(vorhanden, key=lambda x: [int(y) if y.isdigit() else y for y in re.split(r'(\d+)', x) if y]))))

# ------------------------------------------------------------------ (g) Entscheidungen in § 13
aus.append('')
aus.append('PRÜFUNG (g) Entscheidungen aus § 1 der Übergabe und Klickantworten in § 13 mit Datum')
b13 = bereich(f17, '# 13. VERFASSERENTSCHEIDUNGEN', '# 14. ')
G = [('23. **4.7 (Task 6, 26.09.):**', ['18:16', '20:51', 'streichbares Modul', 'Anhang G ohne Prüfprotokolle', 'Nr. 37', 'Nr. 42, 46']),
     ('24. **Direkter Einbau in Schritt 0 (26.09., 20:55):**', ['Einzelfall']),
     ('25. **Zweck des Zielgrößenteils (28.09., 10:30):**', ['Zug 2 der Einleitung']),
     ('26. **Belege zu den Zielgrößen (28.09.', ['Hicks et al. mit dem Jahr 2020', 'Sheppard & Young (2006)']),
     ('27. **Relevanz und Prävention (28.09., 14:36):**', ['Olivier et al. (2026)', 'Rössler et al. (2014)', 'Hilska']),
     ('28. **Einleitung (28.09., 14:38, Klick 14:57):**', ['1.500', 'SMK Abschn. 4.1', 'Festlegung vom 15.09.', '6.350']),
     ('29. **Seitengrenze (28.09., 15:14):**', ['33 Seiten einschließlich Literaturverzeichnis']),
     ('30. **Zählweise (Klick K1, 28.09., 16:27):**', ['ohne Vorspann und Anhang']),
     ('31. **Regel R6 (Klick K2, 28.09., 16:27):**', ['entfällt']),
     ('32. **Tauschregel (Klick K3, 28.09., 16:27):**', ['32 Seiten', 'abweichend von der Empfehlung']),
     ('33. **Ankersatz (Klick K6, 28.09., 16:27):**', ['6.1', 'Zusammenfassung', '4.1 bleibt ohne Zwecksatz']),
     ('34. **Verbleibsliste der Einleitung (28.09., Task 7 neu, Rev. 114):**', ['Textvorschlag Einleitung § 4']),
     ('35. **Verletzungssatz (Klick 2 in Task 7 neu):**', ["Dos'Santos et al., 2018"]),
     ('36. **Reifemethode (Klick 3 in Task 7 neu):**', ['vorgemerkt für 6.2']),
     ('37. **Zweck (Klick in Task 7 neu):**', ['gegenüber einer Kontrollgruppe verbessert', 'Klickfrage 10']),
     ('38. **de Villarreal et al. (2009) (Klick 28.09., nach der Zweitprüfung von Fassung 17):**', ['kein nachweisbarer Moderator']),
     ('39. **Vor-2020-Halbsatz (Klick 28.09., 17:54):**', ['Wirksamkeitsevidenz']),
     ('40. **Erratum Khamis & Roche (Klick 28.09., 19:25):**', ['kein Hinweis in der Arbeit', 'Anhang G', 'Tab. H6', 'R14']),
     ('41. **Verdünnungslogik (Klick 28.09., 19:25):**', ['6.1', 'G3', '6.2 ohne eigenen Absatz']),
     ('16. **Objekte:**', ['erst in Task 18', 'keine Platzhalter', 'Anhang H']),
     ('2. **Verfahren und Prüfer (0.2):**', ['genau einmal in 6.3']),
     ('4. **Adhärenzkriterium:**', ['Kurzform', 'B8'])]
tg = []
for kopf_, stichw in G:
    i = b13.find(kopf_)
    if i == -1:
        tg.append('fehlt in § 13: ' + kopf_)
        continue
    eintrag = b13[i:b13.find('\n', i)]
    for s in stichw:
        if s not in eintrag:
            tg.append('%s … ohne „%s“' % (kopf_[:40], s))
for s in ['Uhrzeiten nach der Sitzungsuhr', 'Bei Zustimmung sinkt das Wortbudget um die Wörter', 'Umfang und Seitengrenze (28.09.)',
          'Gliederung v5 (28.09.)', 'Relevanzstrang (28.09.)', 'Wortlaut des Ankersatzes (28.09., Task 7 neu)']:
    if s not in b13:
        tg.append('fehlt in § 13: ' + s)
ergebnis('(g)', tg, ' (%d Einträge, 6 Zusatzsätze)' % len(G))

# ------------------------------------------------------------------ (h) Block G32 j
aus.append('')
aus.append('PRÜFUNG (h) Block „G32 j“: jeder Punkt der Zeile „Steuerdokumente“ aus Textvorschlag 4.7 § 7 hat einen Ort')
tv = open(TV47, encoding='utf-8').read()
zeile = [z for z in tv.split('\n') if z.startswith('- **Steuerdokumente')][0]
punkte = [x.strip() for x in zeile.split(':**', 1)[1].strip().split(' · ')]
F17 = 'Fassung 17'
ORTE = [
    ('F16 § 4 Analyseeinheit', F17 + ' § 4', [('## 4', 'Er ist für 6.2 vorgemerkt (Textvorschlag 4.7, Nr. 4)')]),
    ('F16 § 11.1 „In 4.7 als Planungsstand', F17 + ' § 11.1', [('', 'Der Hinweis auf das abweichende Planungsmodell ist für 6.2 vorgemerkt')]),
    ('F16 § 11.9 Hinweis zur Trennschärfe', F17 + ' § 11.9', [('', 'ist für 6.2 vorgemerkt (Textvorschlag 4.7, Nr. 15)')]),
    ('F16 § 5.2 Stand am Master', F17 + ' § 5.2 (Messskript Fassung 3, Prüfung d)', [('', '**Stand am Master (Messung 28.09.')]),
    ('Berichtsraster 4.7.3, 4.7.8, 4.7.11, 4.7.12', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('Umfangsdokument § 3.5', F17 + ' § 1.3, Nachtragsvermerk Umfangsdokument', [('', '§ 3.5: Tab. H4 mit Erstverweis in 4.7, Tab. H5 in 5.1 statt 4.7')]),
    ('Plan § 1a und Task 6 als erledigt', 'Plan Rev. 5 (Prüfung in Schritt 4)', []),
    ('Berichtsraster 4.1.10', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('F16 § 11.7 und § 13 Nr. 4', F17 + ' § 11.7, § 13 Nr. 4 und Nachtragsvermerk Auswertungsplan', [('', 'Kurzform für „vor der Abschlusstestung der KG“, Textvorschlag 4.7 B8'), ('', '§ 5.3 und Register des Endabgleichs')]),
    ('Umfangsdokument R5 und F16 § 11.9', 'offen bis Task 11 (Nr. 23): ' + F17 + ' § 11.9 und Nachtragsvermerk R5', [('', 'Ob sie bleiben, entscheidet Task 11 zu Beginn'), ('', 'R5 nach der Entscheidung zu Nr. 23 in Task 11')]),
    ('Register R3 um den Befund B11', F17 + ' § 1.3, Nachtragsvermerk Auswertungsplan', [('', 'Register R3 um den Befund B11')]),
    ('F16 § 11.1 „Die Stichprobe ist durch die teilnehmenden Vereine vorgegeben“', F17 + ' § 11.1 und § 12 G1', [('', 'Die Stichprobe war durch die verfügbaren Spieler und die Zeit an den Testtagen begrenzt'), ('', 'beide Begrenzungen werden bei der Auflösung genannt')]),
    ('F16 § 11.2 Kovariaten-Begründung', F17 + ' § 11.2', [('', 'über den prognostischen Haupteffekt')]),
    ('F16 § 11.4 und Auswertungsplan § 5.2 A3', F17 + ' § 11.4, § 12 G1 und Nachtragsvermerk Auswertungsplan', [('', 'höchstens 7,5 %, 7,3 % bei Unabhängigkeit'), ('', '§ 5.2 A3 und § 6 Nr. 2: Familienfehler')]),
    ('Auswertungsplan § 6 Nr. 3', F17 + ' § 1.3, Nachtragsvermerk Auswertungsplan', [('', '§ 6 Nr. 3: „über Studien vergleichbar“ einschränken')]),
    ('Berichtsraster 4.7.5, 4.7.9 und 4.7.15 mit den Zielorten Tab. 2', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('Berichtsraster 4.7.9, 4.7.10, 4.7.14 und 4.7.15 mit den Satzorten', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('F16 § 13 neue Verfasserentscheidung: Bootstrap', F17 + ' § 13 Nr. 23', [('', 'Bootstrap bleibt im Bericht, als streichbares Modul geführt (18:16')]),
    ('Berichtsraster 4.7.12 und 4.7.5 mit den Zielorten', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('Berichtsraster 4.7.12: im Text ohne Beleg', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('Nr. 57: Berichtsraster 4.7.13', 'Berichtsraster Rev. 3 (Prüfung in Schritt 4)', []),
    ('F16 Nachtragsvermerk „Anhang G ist der Ort der Prüfprotokolle“', F17 + ' § 1.3, § 1.5, § 12, § 13 Nr. 23, § 14', [('', 'Entfallen ist der Vermerk „Berichtsraster Zeile 4.7.13'), ('', 'Sie ist genau einmal für 6.3 als Einschränkung vorgemerkt'), ('', 'gehört als Einschränkung genau einmal in 6.3'), ('', 'Schlussabsatz nur mit Verfahren und Pflichtangaben'), ('', 'Jedes Skript in Anhang G wird als KI-erzeugt gekennzeichnet')]),
    ('Auswertungsverfahren Grundsatz 3, 8.1 und 8.3', F17 + ' § 1.3, Nachtragsvermerk Auswertungsverfahren', [('', 'Grundsatz 3, 8.1 und 8.3: Ort der Einschränkung')]),
    ('Umfangsdokument, Zeile zu 4.7.13', F17 + ' § 1.3, Nachtragsvermerk Umfangsdokument', [('', 'Zeile zu 4.7.13: in 4.7 nur die Datenprüfung')]),
    ('Auswertungsplan § 5.10, Berichtsort', F17 + ' § 1.3, Nachtragsvermerk Auswertungsplan', [('', '§ 5.10: Berichtsort bei R1, R9, R10, R12 und R13 nicht mehr 4.7')]),
    ('Plan § 2.1 Nr. 5 bis 8', 'Plan Rev. 5 (Prüfung in Schritt 4)', []),
    ('Maßnahmenliste L9', 'Maßnahmenliste (Schritt 5)', []),
]
th = []
for i, p in enumerate(punkte, 1):
    treffer = [o for o in ORTE if p.startswith(o[0]) or o[0] in p[:len(o[0]) + 10]]
    if not treffer:
        th.append('Punkt %d ohne Ort: %s' % (i, p[:120]))
        continue
    _, ort, belege = treffer[0]
    fehlt = [b for _, b in belege if b not in f17]
    status = 'Ort geprüft' if belege and not fehlt else ('Ort in Schritt 4 oder 5' if not belege else 'FEHLT: ' + ' | '.join(fehlt))
    if fehlt:
        th.append('Punkt %d, %s: %s' % (i, ort, ' | '.join(fehlt)))
    aus.append('   %2d. %s → %s [%s]' % (i, p[:90] + ('…' if len(p) > 90 else ''), ort, status))
ergebnis('(h)', th, ' (%d Punkte)' % len(punkte))

# ------------------------------------------------------------------ (i) Trefferliste „Durchgehend“
aus.append('')
aus.append('PRÜFUNG (i) Trefferliste „Durchgehend“ (Übergabe § 4): jeder Treffer ersetzt, Arbeitsnummer oder historisch')
MUSTER = [r'9\.000', r'Teil A', r'Teil B', r'Kapitel 1 bis 7', r'Kapitel 2\b', r'Kapitel 3\b', r'(?<![\d.§ ])(?<!§ )2\.[1-5](?![\d])',
          r'Tasks 7 bis 10', r'Task 14', r'\bR6\b', r'30,3', r'36 Seiten', r'(?<![\d,.])37(?![\d,.])', r'Wortlaut des Antrags',
          r'Antragswortlaut', r'mehr Kapitel', r'Prüfprotokoll', r'vor Kenntnis der KG-Werte', r'in 4\.7', r'F14 §', r'F16 §']
REGELN = [
    (r'von 9\.000 auf 6\.350|damals bei 9\.000|damals 9\.000', 'historisch gekennzeichnet'),
    (r'Altbestand Kapitel 2|Kapitel 2 und 3 (entfallen|stehen)|Kapitel 2 entfällt|Kapitel 2 \(2\.1 bis 2\.4\) wird nicht mehr|in Kapitel 2 und 4 \(historisch\)', 'Altbestand, entfällt mit der Einleitung'),
    (r'_2\.4_|Textvorschlag_2\.4', 'Dateiname'),
    (r'Task 14 entfällt', 'als entfallen gekennzeichnet'),
    (r'R6 entfällt|Regel R6 \(|R6 und Tauschregel|§ 3\.6 und R6|Regel R6 \(Klick', 'neue Regel: R6 entfällt'),
    (r'höchstens 37 Textseiten|\| 37 \||Nr\. 37', 'Betreuergrenze oder Nummer im Textvorschlag 4.7'),
    (r'nah am (Wortlaut des Antrags|Antragswortlaut)', 'neue Regel: nah am Antragswortlaut'),
    (r'ohne Prüfprotokolle|keine Prüfprotokolle|Ort der Prüfprotokolle|Prüfprotokoll der Gliederung|Prüfprotokoll `05_Protokolle', 'neue Regel oder Dateibezug'),
    (r'vor Kenntnis der KG-Werte[^.]{0,80}(Kurzform|B8|Abschlusstestung der KG)', 'als Kurzform gekennzeichnet (B8)'),
    (r'„in 4\.7“|Erstverweis in 4\.7|: in 4\.7 nur die Datenprüfung|je ein Satz in 4\.7 für die Sensitivitätsanalysen|nicht in 4\.7 \(20:51\)|in 4\.7 „konservativ“|werden in 4\.7 nicht berichtet', 'geprüft gegen 4.7 im Master'),
    (r'Nr\. \d+ bis 37', 'Nummer in § 13'),
    (r'Für Kapitel 2 abgelöst durch Nr\. 28|Kapitelname 3 \(historisch', 'als abgelöst oder historisch gekennzeichnet'),
]
ti = []
zaehler = {}
for nr, z in enumerate(f17.split('\n'), 1):
    for mu in MUSTER:
        for m in re.finditer(mu, z):
            umg = z[max(0, m.start() - 70):m.end() + 90]
            grund = [g for rx, g in REGELN if re.search(rx, umg)]
            zaehler[mu] = zaehler.get(mu, 0) + 1
            if grund:
                aus.append('   Z%4d %-26s %s  (…%s…)' % (nr, mu[:26], grund[0], umg[40:150].replace('\n', ' ')))
            else:
                ti.append('Z%d %s ohne Einordnung: …%s…' % (nr, mu, umg))
aus.append('   Treffer je Muster: ' + ' · '.join('%s %d' % (k, v) for k, v in zaehler.items()))
aus.append('   Ohne Treffer: ' + ' · '.join(mu for mu in MUSTER if mu not in zaehler))
ergebnis('(i)', ti, ' (%d Treffer, alle eingeordnet)' % sum(zaehler.values()) if not ti else '')

# ------------------------------------------------------------------ (j) Seitenmodell
aus.append('')
aus.append('PRÜFUNG (j) Seitenrechnung per Skript, jede Zeile als Modellrechnung oder Festlegung gekennzeichnet')
P = {r['parameter']: r['wert'] for r in csv.DictReader(open(S_CSV, encoding='utf-8'), delimiter=SEMI)}
b11 = bereich(f17, '**Seitenrechnung — Modellrechnung, keine Messung.**', '**Kein Auffüllen.**')
zeilen = [z for z in b11.split('\n') if z.startswith('| ') and not z.startswith('| Posten') and not z.startswith('|---')]
tj = []
for z in zeilen:
    art = z.rstrip(' |').split('|')[-1].strip()
    if not (art.startswith('Modellrechnung') or art == 'Festlegung'):
        tj.append('Zeile ohne Kennzeichnung: ' + z)
gb = float(P['prognose_gesamt_basis'])
go = float(P['prognose_gesamt_obere'])
for wert in ['%.1f' % gb, '%.1f' % go, '%.1f' % float(P['prognose_textteil'])]:
    if ('**' + wert.replace('.', ',') + '**') not in b11 and ('| ' + wert.replace('.', ',') + ' |') not in b11:
        tj.append('Wert %s aus dem Seitenmodell steht nicht in der Tabelle' % wert.replace('.', ','))
ergebnis('(j)', tj, ' (%d Tabellenzeilen, Prognose %s und %s Seiten aus `Seitenmodell_2026-09-28.csv`)' % (
    len(zeilen), ('%.1f' % gb).replace('.', ','), ('%.1f' % go).replace('.', ',')))

# ------------------------------------------------------------------ (k) Befunde der Zweitprüfung und Rev. 114
aus.append('')
aus.append('PRÜFUNG (k) Befunde der Zweitprüfung von Fassung 17, Punkte aus Rev. 114, Befunde der übergreifenden Zweitprüfung zu Fassung 17 (Z2) und Klicks 19:25: Soll-Text vorhanden, Alt-Text entfernt')
S4 = 'Schritt 4 oder 5 (nicht Fassung 17)'
BEF = [
    ('B1 International 1,22', ['zwei Effektstärken einer einzigen Studie (Matavulj et al., 2001'], ['aus zwei Studien']),
    ('B2 Fitnessniveau', ['Fitnessniveau ist kein nachweisbarer Moderator'], ['Fitnessniveau ist kein starker Moderator']),
    ('B3 Berichtspflicht Poweranalyse', ['verweist ohne Zahl auf die erreichte Spielerzahl', 'für Anhang G vorgemerkt (Task 16, Textvorschlag 4.7, Nr. 8)'], ['die übrigen Angaben stehen in Anhang G']),
    ('B4 Oliver Ersatzkriterium', ['bei fehlender Angabe der Wettkampfebene nach dem Trainingsumfang'], ['ohne Angabe der Wettkampfebene nach den Trainingsstunden']),
    ('B5 vorgemerkt statt steht', ['Prävention ist als Zusatznutzen der Programmklasse vorgemerkt', '6.2 ist für beide Richtungen vorgemerkt', 'ist für Tab. H6 vorgemerkt (Verfasser 26.09., 20:51', 'geht auf Tab. H6 und diese Gruppe über (vorgemerkt'],
     ['Prävention steht als Zusatznutzen', '6.2 formuliert beide Richtungen', 'Das Datum jeder Festlegung steht in Tab. H6', 'tragen Tab. H6 und diese Gruppe', 'Das Erratum steht nur in Anhang G', 'beziehungsweise in Tab. H6 und 6.3 ·']),
    ('B6 keine Objektplatzhalter', ['auch nicht als Platzhalter. Tab. 1 setzt Task 18 direkt nach G31 (b)'], ['als Platzhalter im Master (§ 5.3)', 'Bis Task 18 stehen im Master nur Platzhalter']),
    ('B7 Zeilenabstand und Muster', ['Den Zeilenabstand des Verzeichnisses regelt der Leitfaden nicht', 'Das Muster-Inhaltsverzeichnis des SMK-Leitfadens'], ['es gilt 1,5 wie im Fließtext', 'Der SMK-Leitfaden paginiert']),
    ('B8 vertikale Sprunghöhe', ['Fitnessniveau ist kein nachweisbarer Moderator (vertikale Sprunghöhe)', 'fanden für die vertikale Sprunghöhe beim Sportniveau'], []),
    ('B9 Spielklasse', ['hängt an der Spielklasse der drei Mannschaften'], ['Die eigene Stichprobe liegt darunter']),
    ('B10 konservativ', ['Richtung gestützt, nicht allgemein bewiesen'], ['Der Standardweg ohne Kovariatengewinn ist konservativ, die MDES fällt größer aus.']),
    ('B11 Statistikabsatz', ['Effektstärke ohne Schwellen, eingeordnet über das Konfidenzintervall', 'keine Darstellungskonvention im Text'], []),
    ('B12 Vor-2020-Halbsatz', ['wenn sie Wirksamkeitsevidenz trägt'], ['Bei Konzept- und Diagnostikübersichten ohne neuere Entsprechung']),
    ('B13 Asimakidis in T1', ['Asimakidis et al. (2022, T1 `Manou2022`)'], []),
    ('B14 Hoffmann', ['der Teil Hoffmann et al. (2014) ist erledigt'], []),
    ('B15 Negra 2020', ['Negra et al. (2020) liegt seit dem 11.09. im Ordner (H7)'], ['⭐ Negra et al. (2020)']),
    ('B16 4.1 ohne Zwecksatz', ['4.1 bleibt ohne Zwecksatz.'], ['4.1 bleibt unverändert']),
    ('B17 steuernde Prognose', ['Steuernd ist seine jeweils jüngste Prognose', 'Maßgeblich ist die jüngste Prognose des Messskripts'], []),
    ('B18 Untergrenze', ['Eine sanktionierte Untergrenze nennt die Prüfungsordnung nicht'], ['Eine Untergrenze gibt es nicht']),
    ('B19 Objekt als Annahme', ['nach Annahme rund 0,4 Seiten'], []),
    ('B20 Arbeitsnummern', ['(Arbeitsnummern 5 und 6)', 'Zeilenkennungen des Berichtsrasters für die Einleitung'], ['nach Kapitel 5 und 6']),
    ('B21 Beispielsatz', ['Bei der Abschlusstestung von Verein B fiel die 10-m-Lichtschranke aus'], ['Bei der Ausgangstestung von Verein B']),
    ('B22 Pausenregel', ['Pausenregel beim Standweitsprung nur in 4.3, 4.4.3 nennt nur die Abweichung'], ['Pause beim Standweitsprung nur in 4.3']),
    ('B23 Beleg Methodenprüfung', ['Textvorschlag 4.7, Nr. 57, Auswertungsverfahren 8.1 wird nachgetragen'], []),
    ('B24 ausgeschlossene Schlüsse', ['§ 4.3 und § 4.4 (G34 f', '„Motivierte machen einen Sprung“', 'a posteriori'], ['„Motivierte machen den Sprung“']),
    ('B25 ITT-Zitat', ['„Die Hauptanalyse umfasste unabhängig von der Adhärenz alle zugeteilten Spieler'], ['„Analysiert wurden alle zugeteilten Spieler']),
    ('B26 H0-Regel', ['einen Vorteil der Interventionsgruppe mit p < 0,05 (zweiseitig) zeigt (Wortlaut 4.7'], ['in günstiger Richtung liegt']),
    ('B27 Familienfehler und Trennschärfe', ['ordnet 6.2 ein (Textvorschlag 4.7 § 7, Zeile Task 12)'], ['gehört in dieselbe Gruppe']),
    ('B28 KI-Deklaration', ['Task 16 führt beide zusammen', 'werden in 4.7 nicht berichtet'], []),
    ('B29 Übergabe Einleitung', [], [], S4),
    ('B30 Maßnahmenliste', [], [], S4),
    ('B31 T4 zurückschreiben, Hicks2020', ['T1 `Radnor2017` und `Hicks2019` werden nachgeführt (G35)'], [], 'T4-Rückschreibung in Schritt 5'),
    ('B32 Raster, Gliederung, Plan', [], [], S4),
    ('B33 Nr. 13 und Kapitelname 3', ['Für Kapitel 2 abgelöst durch Nr. 28', 'Kapitelname 3 (historisch'], []),
    ('R114 Liu 2024 Tier 2', ['Liu et al. (2024) untersuchten regionale U19'], ['*Leistungsniveau:* Kein Detraining-Vergleichssetting unterhalb der Akademieebene.', 'Die gesamte E5-Evidenz']),
    ('R114 Mirwald und Reifemethode', ['Mirwald et al. (2002) entfällt mit der Reifemethode'], ['Mirwald et al. (2002) wird in 2.2']),
    ('R114 Clemente 2022', ['Clemente et al. (2022), nicht im Ordner'], []),
    ('R114 Moran 2017', ['Moran et al. (2017), JSCR 31(2), 552–565'], ['Moran et al. (2016)', 'Jahr 2016 oder 2017']),
    ('R114 Klickfrage 10', ['Klickfrage 10'], []),
    ('Z2-4 Objekte und G31', ['Tab. 1 setzt Task 18 direkt nach G31 (b)', '16. **Objekte:** erst in Task 18 eingesetzt'], ['16. **Objekte:** zunächst als Platzhalter', 'nach G31 (a) (§ 5.3)', 'den für Tab. 1 setzt Task 18 nach G31 (a)']),
    ('Z2-5 Mindestdosis-Verbot', ['nicht als Beleg für eine Mindestdosis zitiert werden', 'Für andere Aussagen sind beide nach T4 zulässig'], ['**Zwei Quellen dürfen nicht als Beleg zitiert werden:**']),
    ('Z2-27 Prompt dieses Tasks', ['`Uebergabe_Steuerdokumente_2026-09-28.md` (erledigt, der Task vom 28.09. mit Rev. 115)'], ['Prompt des Tasks Steuerdokumente 28.09. (Task 1b des Plans']),
    ('Z2-36 Ramirez-Campillo 2020', ['Band und Seiten bei Crossref geprüft (50(12), 2125–2143'], ['Band, Seiten und DOI prüfen']),
    ('Z2-40 Textstufen 4.7', ['bleiben als Ausgaben des Skripts `Textvorschlag_4.7_2026-09-25.py`'], ['mit den Textstufen `_A`, `_Empf`, `_Kurz` (ersetzt']),
    ('Klick 19:25 Erratum', ['wird in der Arbeit nicht erwähnt, weder im Fließtext noch in Anhang G noch in Tab. H6'], ['Das Erratum ist nur für Anhang G vorgemerkt', 'Erratum Khamis & Roche (1995), doi']),
    ('Klick 19:25 Verdünnungslogik', ['**Verdünnungslogik für 6.1:**', '6.2 führt keinen eigenen Absatz dazu'], ['**Verdünnungslogik für 6.2:**']),
]
tk = []
for eintrag in BEF:
    name, soll_, weg_ = eintrag[0], eintrag[1], eintrag[2]
    ort = eintrag[3] if len(eintrag) > 3 else 'Fassung 17'
    fehlt = [x for x in soll_ if x not in f17]
    bleibt = [x for x in weg_ if x in f17]
    if fehlt or bleibt:
        tk.append('%s: fehlt %s, noch vorhanden %s' % (name, fehlt, bleibt))
    aus.append('   %-34s %s%s' % (name, ort, '' if (fehlt or bleibt) else ' [umgesetzt]' if soll_ or weg_ else ' [zugeordnet]'))
ergebnis('(k)', tk, ' (%d Einträge)' % len(BEF))

# ------------------------------------------------------------------ Ausgabe
aus.append('')
aus.append('GESAMT: ' + ('NICHT BESTANDEN: ' + ', '.join(fehler) if fehler else 'alle elf Prüfungen bestanden'))
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('Projektanweisungen_Vergleich_F16_F17_2026-09-28.py, Lauf am 28.09.2026\n\n' + '\n'.join(aus) + '\n')
print('\n'.join(x for x in aus if x.startswith('PRÜFUNG') or 'Ergebnis' in x or x.startswith('GESAMT') or 'NICHT' in x or 'ohne Einordnung' in x or 'nicht zugeordnet' in x or 'Zeile ' in x[:12]))
sys.exit(1 if fehler else 0)

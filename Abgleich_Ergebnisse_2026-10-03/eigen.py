# -*- coding: utf-8 -*-
"""
eigen.py — Merkmale je Satz für den Textstand von Kapitel 5 (deutsche Ausdrücke), Schritt 2 (a), 03.10.2026

Übergabe § 5 Nr. 7: textbausteine.py des Korpus zählt mit englischen Ausdrücken. Hier dieselben Merkmalsfamilien wie in
analyse.py des Korpus (RX, statwert, Konnektor, Objektformen), auf deutschen Text übertragen. Jede Familie ist an allen
29 Sätzen von Hand geprüft: HAND hält je Satz Satzanfang, finites Verb mit Tempus und die Art eines Nullbefunds fest,
PRUEF die Handprüfung der Treffer (Fehltreffer und Fehlende). Abweichungen vom Korpusausdruck stehen bei RX.
Aufruf: python eigen.py <textstand.json> [<Ausgabe.json> <Ausgabe.txt>]
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import json
import pathlib

B_ = pathlib.Path(__file__).resolve().parent
TS = sys.argv[1] if len(sys.argv) > 1 else str(B_ / 'textstand.json')
AUSJ = sys.argv[2] if len(sys.argv) > 2 else str(B_ / 'eigen.json')
AUST = sys.argv[3] if len(sys.argv) > 3 else str(B_ / 'eigen.txt')

OBJ = r'(?:Tab|Abb)\.\s[A-H]?\d+'
RX = {
    # wie Korpus: p mit Vergleichszeichen
    'p': r'\bp\s*[<>=≤≥]',
    # Korpus: F, t, χ2, Z. Hier zusätzlich W (Shapiro-Wilk)
    'stat': r'\b(?:F|t|W|χ2|Z)\s*(?:\(\d|[=≥≤])',
    # Effektstärke als Wert
    'es': r'\b(?:d|g)\s*=\s*[−+-]?\d',
    # Korpus: CI, CL90, confidence limits. Hier das Wort und die Intervallform „−x bis +y“
    'ki': r'Konfidenzintervall|[−+]\d+(?:,\d+)?\s*(?:s|cm)?\s+bis\s+[−+]\d',
    'prozent': r'%',
    'msd': r'±',
    # Größenklasse am Effekt oder Unterschied
    'klasse': r'(?i)\b(?:trivial\w*|klein\w*|mittler\w*|groß\w*|moderat\w*)\s+(?:Effekt\w*|Unterschied\w*|Differenz\w*|Veränderung\w*)',
    'sig': r'(?i)signifikan',
    'objekt': OBJ,
    'beleg': r'et al\.|\(\D{0,60}\d{4}[a-z]?\)',
    'wir': r'(?i)\b(?:wir|unser\w*|uns)\b',
    # Rohzählung wie die Korpusspalte null
    'null': r'(?i)\bkein\w*\b|\bnicht\b|\bweder\b',
    # Mittelwertdifferenz im Satz: „betrug … −x“
    'differenz': r'\bbetrug\b[^.(]*?[−+]\d',
}
KONNEKTOR = (r'^(Jedoch|Zudem|Außerdem|Allerdings|Darüber hinaus|Ebenso|Auch|Ferner|Dagegen|Hingegen|Zusätzlich|'
             r'Weiterhin|Insgesamt|Damit|Somit|Folglich|Dabei|Demgegenüber|Schließlich|Daneben|Ebenfalls|'
             r'Gleichzeitig|Dennoch|Trotzdem)\b')
OBJ_SUBJ = r'^' + OBJ + r'\s+(?:zeigt|enthält|fasst|stellt|gibt|führt|nennt)\b|,\s' + OBJ + r'\s+(?:die|den|das)\b'
OBJ_ORT = r'\b(?:in|auf)\s+' + OBJ + r'\s+(?:zusammengefasst|dargestellt|aufgeführt|enthalten|gezeigt)|\b(?:stehen|steht|finden sich|sind|ist)\s+in\s+' + OBJ
OBJ_KLAMMER_ENDE = r'\([^()]*\b' + OBJ + r'[^()]*\)\.$'
PRAES_OBJ = r'\b(?:zeigt|zeigen|enthält|enthalten|fasst|fassen|stellt|stellen|steht|stehen|führt|nennt)\b'

# Handprüfung je Satz: Satzanfang, finites Verb (Tempus), Art des Nullbefunds (nur Befund- und Zusatzsätze)
HAND = {
    'A1 S1': ('Objekt als Subjekt', 'zeigt (Präsens)', ''),
    'A1 S2': ('Bezugsmenge (Präpositionalgruppe mit Zahl)', 'gingen … ein (Präteritum)', ''),
    'A1 S3': ('Objekt als Subjekt (zweites elliptisch)', 'enthält (Präsens)', ''),
    'A1 S4': ('Quantor', 'lagen (Präteritum)', ''),
    'A2 S1': ('Gruppe als Subjekt (mit Bezugsmenge)', 'meldeten (Präteritum)', ''),
    'A2 S2': ('Themenanker (Bezugsgröße)', 'entsprach (Präteritum)', ''),
    'A2 S3': ('Zahl als Subjekt', 'erreichten (Präteritum)', ''),
    'A2 S4': ('Themenanker („Als Untergrenzen“)', 'ergaben sich (Präteritum)', ''),
    'A3 S1': ('Größe als Subjekt', 'lag (Präteritum)', ''),
    'A3 S2': ('Größe als Subjekt', 'betrug (Präteritum)', ''),
    'A3 S3': ('Zahl als Subjekt', 'nannten (Präteritum)', ''),
    'A3 S4': ('Themenanker (Gruppe)', 'wurden … erhoben (Präteritum, Passiv)', ''),
    'A4 S1': ('Größe als Subjekt', 'überstieg (Präteritum)', ''),
    'A4 S2': ('Größe im Vorfeld (Objekt)', 'hatte (Präteritum)', ''),
    'A5 S1': ('Objekt als Subjekt', 'enthält (Präsens)', ''),
    'A5 S2': ('Objekt als Subjekt', 'zeigt (Präsens)', ''),
    'A5 S3': ('Quantor', 'lagen (Präteritum)', ''),
    'A5 S4': ('Modell (Partizip „Adjustiert für …“)', 'betrug (Präteritum)', ''),
    'A5 S5': ('Themenanker (Zielgröße)', 'betrug (Präteritum)', ''),
    'A5 S6': ('Quantor (Präpositionalgruppe „Bei keiner Zielgröße“)', 'war (Präteritum)', 'fehlender Nachweis („kein Gruppenunterschied nachweisbar“)'),
    'A5 S7': ('Quantor', 'war (Präteritum)', 'Intervall gegen den SESOI („mit relevanten Unterschieden in beide Richtungen vereinbar“)'),
    'A5 S8': ('Befund als Subjekt', 'waren (Präteritum)', 'Fall der Schlusslogik („unschlüssig“)'),
    'A5 S9': ('Quantor', 'zeigte (Präteritum)', 'Entscheidungsregel („Keine … mit p < 0,05 einen Vorteil“)'),
    'A5 S10': ('Hypothese als Subjekt', 'wurde … verworfen (Präteritum, Passiv)', 'Hypothesenentscheidung („nicht verworfen“)'),
    'A5 S11': ('Zielgrößen als Subjekt', 'wurden … beschrieben (Präteritum, Passiv)', ''),
    'A6 S1': ('Themenanker (Zielgröße), Test als Subjekt', 'verwarf (Präteritum)', ''),
    'A6 S2': ('Analyse als Subjekt', 'reichte (Präteritum)', ''),
    'A6 S3': ('„übrige“ als Subjekt', 'wurden … verworfen (Präteritum, Passiv)', ''),
    'A6 S4': ('Subjunktion („Soweit …“)', 'zuließ, änderten, erreichte (Präteritum)', 'Absicherung („änderten weder … noch … die Einordnung“, „keine davon erreichte p < 0,05“)'),
}
# Handprüfung der Regex-Treffer: Fehltreffer und Fehlende je Satz (leer heißt geprüft und richtig)
PRUEF = {
    'A2 S1': 'null: „als nicht durchgeführt“ ist Status, kein Nullbefund',
    'A3 S3': 'null: „zu nicht … durchgeführten“ ist Status, kein Nullbefund',
    'A3 S4': 'null: „nicht erhoben“ ist Erhebungsangabe, kein Nullbefund',
    'A5 S4': 'prozent: „95-%“ im Wort Konfidenzintervall (im Korpus zählt „95% CI“ ebenso)',
    'A5 S9': 'p: Schwelle der Entscheidungsregel, kein p-Wert (im Korpus zählt „p < 0.05“ ebenso)',
    'A6 S3': 'null: „nicht verworfen“ ist Voraussetzungsprüfung, kein Nullbefund',
    'A6 S4': 'p: Schwelle, kein p-Wert',
}

ts = json.load(open(TS, encoding='utf-8'))
S = [s for a in ts['absaetze'] for s in a['saetze']]
assert set(x['id'] for x in S) == set(HAND), 'Satzliste und HAND verschieden'
R = []
for s in S:
    t = s['text']
    m = {k: len(re.findall(v, t)) for k, v in RX.items()}
    m['zahlen'] = len(re.findall(r'(?<![A-Za-zÄÖÜäöüß])[−+-]?\d+(?:[.,]\d+)?', t))
    m['statwert'] = int(any(m[k] > 0 for k in ('p', 'stat', 'es', 'ki', 'prozent', 'msd', 'differenz')))
    km = re.match(KONNEKTOR, t)
    m['konnektor'] = km.group(1) if km else ''
    m['objekt_subjekt'] = len(re.findall(OBJ_SUBJ, t))
    m['objekt_ort'] = len(re.findall(OBJ_ORT, t))
    m['objekt_klammer_ende'] = int(bool(re.search(OBJ_KLAMMER_ENDE, t)))
    m['praesens_objekt'] = int(bool(re.search(PRAES_OBJ, t)) and m['objekt_subjekt'] > 0)
    m['objekte'] = re.findall(OBJ, t)
    an, vb, nu = HAND[s['id']]
    R.append(dict(id=s['id'], woerter=s['woerter'], text=t, merkmale=m, satzanfang=an, verb=vb, nullform=nu,
                  pruefung=PRUEF.get(s['id'], '')))
json.dump({'quelle': TS, 'saetze': R}, open(AUSJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
Z = ['Merkmale je Satz, Textstand Kapitel 5 (eigen.py, deutsche Ausdrücke, Handprüfung je Satz)', '']
KEYS = ['p', 'stat', 'es', 'ki', 'prozent', 'msd', 'differenz', 'statwert', 'klasse', 'sig', 'objekt', 'objekt_subjekt',
        'objekt_ort', 'objekt_klammer_ende', 'praesens_objekt', 'beleg', 'wir', 'null', 'zahlen']
Z.append(f"{'Satz':7}" + ' '.join(f'{k[:6]:>6}' for k in KEYS))
for r in R:
    Z.append(f"{r['id']:7}" + ' '.join(f"{r['merkmale'][k]:>6}" for k in KEYS))
Z.append('')
for r in R:
    Z.append(f"{r['id']}: Anfang {r['satzanfang']} · Verb {r['verb']}" + (f" · Nullbefund {r['nullform']}" if r['nullform'] else '')
             + (f" · Konnektor {r['merkmale']['konnektor']}" if r['merkmale']['konnektor'] else '')
             + (f" · Handprüfung: {r['pruefung']}" if r['pruefung'] else ' · Handprüfung: Treffer richtig, keine fehlenden'))
open(AUST, 'w', encoding='utf-8').write('\n'.join(Z) + '\n')
print('\n'.join(Z))

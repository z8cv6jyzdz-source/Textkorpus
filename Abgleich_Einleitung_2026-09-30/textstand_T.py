# -*- coding: utf-8 -*-
"""
textstand_T.py — Schritt 1 des Tasks „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (30.09.2026)

Setzt den Textstand T nach den Klicks vom 30.09. zu Schritt 1 zusammen und misst ihn wie Manuskriptstand_2026-09-25.py
(Wörter = Leerraum-Token mit Belegklammern, Satzteilung mit derselben Funktion saetze()).

Klicks (Sitzungsuhr, vor 15:38):
  Frage 1  Textstand = Text des Verfassers (Anhang zum Taskstart, A)
  Frage 2  keine Abweichung angekreuzt -> nach dem Register zurückgesetzt:
           (1) Eröffnung mit den Wettkampfanforderungen, B3 beginnt nach B1 § 1.3 (18:50, 07:00 Nr. 4)
           (2) Moran et al. (2017) gestrichen (18:50)
           (3) B1a und B1b mit Illinois-Satz, Spannen-Satz, DVZ-Mechanismen, Programmsatz und B1b S4/S5 (07:00, 17:41)
           (4) B5 S1 mit „deshalb“ (10:00)
  Frage 3  B2 Fassung 4 freigegeben wie D1 (D6 Nr. 1 a, Nr. 2 a, Nr. 3 a)
  Frage 4  Kombinierte Programme nicht in der Einleitung (B3 bis B5 § 8 Nr. 3 a)
Wortlaut des Verfassers ohne Registerzeile bleibt: B1b S1 (A B1 S2), B1b S7 (A B1 S8), B3 S5 (A B3 S7), B4 (A B4, 6 Sätze).
Liest textstand_V.json und textstand_A.json (aus textstand.py). Schreibt textstand_T.json, textstand_T_saetze.md,
textstand_T_messung.txt. Ohne Semikolon außerhalb von Zeichenketten-Konstanten (chr(59)).
"""
import json, os, re, statistics as st
HIER = os.path.dirname(os.path.abspath(__file__))
SEMI = chr(59)


def saetze(text):  # unverändert aus Manuskriptstand_2026-09-25.py (Fassung 3)
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


KLAMMER = re.compile(r'\([^()]*\d{4}[^()]*\)')


def ohne_belege(t):
    return re.sub(r'\s+', ' ', KLAMMER.sub('', t)).replace(' .', '.').replace(' ,', ',').strip()


def quellen(t):
    out = []
    for k in KLAMMER.findall(t):
        for teil in k.strip('()').split(SEMI):
            m = re.match(r"(.+?),\s(\d{4}[a-z]?)", teil.strip())
            if m:
                out.append(m.group(1).replace('’', "'").strip() + ' ' + m.group(2))
    return out


V = json.load(open(os.path.join(HIER, 'textstand_V.json'), encoding='utf-8'))['absaetze']
A = json.load(open(os.path.join(HIER, 'textstand_A.json'), encoding='utf-8'))['absaetze']
SV = {k: saetze(t) for k, t in V.items()}
SA = {k: saetze(t) for k, t in A.items()}
assert [len(SV[k]) for k in ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']] == [6, 7, 11, 5, 7, 4]
assert [len(SA[k]) for k in ['B1', 'B2', 'B3', 'B4', 'B6']] == [8, 11, 7, 6, 4]


def v(k, i):
    return ('V %s S%d' % (k, i), SV[k][i - 1])


def a(k, i):
    return ('A %s S%d' % (k, i), SA[k][i - 1])


# Zuordnung Satz für Satz (Herkunft, Wortlaut)
PLAN = {
    'B1a': [v('B1a', 1), v('B1a', 2), v('B1a', 3), v('B1a', 4), v('B1a', 5), v('B1a', 6)],
    'B1b': [a('B1', 2), v('B1b', 2), v('B1b', 3), v('B1b', 4), v('B1b', 5), v('B1b', 6), a('B1', 8)],
    'B2': [v('B2', i) for i in range(1, 12)],
    'B3': [v('B3', 1), v('B3', 2), v('B3', 3), v('B3', 4), a('B3', 7)],
    'B4': [a('B4', i) for i in range(1, 7)],
    'B5': [v('B5', i) for i in range(1, 5)],
}
# Gegenproben: gleiche Sätze in A und V, wo T sie aus V nimmt
assert SV['B1b'][1] == SA['B1'][2] and SV['B1a'][2] == SA['B1'][0]
assert SV['B2'] == SA['B2']
assert SV['B3'][1:4] == SA['B3'][3:6]
assert SV['B4'][3:] == SA['B4'][2:]
assert SV['B5'][1:] == SA['B6'][1:] and SV['B5'][0].replace('es deshalb zu', 'es zu') == SA['B6'][0]
# A-Sätze, die nach Frage 2 zurückgesetzt sind
ENTFALLEN = {'A B1 S1': 'wortgleich V B1a S3 (steht in T an dritter Stelle)',
             'A B1 S3': 'wortgleich V B1b S2',
             'A B1 S4': 'alter DVZ-Satz, ersetzt durch V B1b S4 (Frage 2 Nr. 3)',
             'A B1 S5': 'alter Satz zur gemeinsamen Muskelaktion, ersetzt durch V B1b S5 und S6 (Frage 2 Nr. 3)',
             'A B1 S6': 'RC 2020 mit „Auch“, ersetzt durch V B1a S5 (Frage 2 Nr. 1 und 3)',
             'A B1 S7': 'Moran et al. (2017), gestrichen (Frage 2 Nr. 2)',
             'A B3 S1': 'Spielanalysen-Einstieg, Inhalt in V B1a S1 und S2 (Frage 2 Nr. 1)',
             'A B3 S2': 'wie A B3 S1',
             'A B3 S3': 'Hicks-Satz der Fassung 2, ersetzt durch den Beginn nach B1 § 1.3 (Frage 2 Nr. 1)',
             'A B6 S1': 'ohne „deshalb“, ersetzt durch V B5 S1 (Frage 2 Nr. 4)'}

T = {k: ' '.join(s for _, s in plan) for k, plan in PLAN.items()}
json.dump({'quelle': 'Textstand T nach den Klicks zu Schritt 1 (30.09.)', 'absaetze': T,
           'herkunft': {k: [h for h, _ in plan] for k, plan in PLAN.items()}},
          open(os.path.join(HIER, 'textstand_T.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# Messung
zeilen, alle, absw, alle_q, klammern = [], [], {}, [], 0
for k, t in T.items():
    s = saetze(t)
    assert s == [x for _, x in PLAN[k]], k  # Satzteilung gibt die Zuordnung exakt wieder
    absw[k] = len(t.split())
    for i, x in enumerate(s, 1):
        alle.append((k, i, x, len(x.split()), len(ohne_belege(x).split()), len(KLAMMER.findall(x)), PLAN[k][i - 1][0]))
    alle_q += quellen(t)
    klammern += len(KLAMMER.findall(t))
W = sum(absw.values())
Wo = sum(len(ohne_belege(t).split()) for t in T.values())
lens = [x[3] for x in alle]
lens_o = [x[4] for x in alle]
semi = sum(ohne_belege(t).count(SEMI) for t in T.values())
verw = sum(len(re.findall(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)', t)) for t in T.values())
dp = sum(ohne_belege(t).count(':') for t in T.values())
belegte = sum(1 for x in alle if x[5] > 0)
# Seitenprognose wie Messskript (d), Parameter aus Seitenmodell_2026-09-28.csv, Methodik bis Fazit 4716 (Messskript 30.09.)
p = {}
_SM = os.path.normpath(os.path.join(HIER, '..', 'Seitenmodell_2026-09-28.csv'))
if not os.path.isfile(_SM):
    _SM = '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Seitenmodell_2026-09-28.csv'
for z in open(_SM, encoding='utf-8').read().splitlines()[1:]:
    f = z.split(SEMI)
    p[f[0]] = float(f[1])
W_REST = 4716
seiten = (W / p['dichte_einleitung'] + W_REST / p['dichte_kapitel_4_bis_7'] + p['objekte_textteil'] * p['seiten_je_objekt']
          + p['kapitelenden_textteil'] * p['seiten_je_kapitelende'] + p['eintraege_basis'] / p['eintraege_je_seite']
          + p['seiten_je_kapitelende'])
de = lambda x, n=1: ('%.*f' % (n, x)).replace('.', ',')
zeilen.append('Textstand T (Klicks 30.09. zu Schritt 1): %d Wörter (ohne Belegklammern %d), %d Absätze: %s' % (
    W, Wo, len(T), ' · '.join('%s %d' % (k, w) for k, w in absw.items())))
zeilen.append('Sätze %d · Median %s (ohne Belegklammern %s) · längster %d (%s) · über 32: %d · Absätze über 250: %d' % (
    len(alle), de(st.median(lens)), de(st.median(lens_o)), max(lens), '%s S%d' % max(alle, key=lambda x: x[3])[:2],
    sum(1 for x in lens if x > 32), sum(1 for w in absw.values() if w > 250)))
zeilen.append('Belegklammern %d · Sätze mit Beleg %d von %d (%s %%) · Quellen %d · Semikola außerhalb von Belegklammern %d · '
              'Abschnittsverweise %d · Doppelpunkte außerhalb von Belegklammern %d' % (
                  klammern, belegte, len(alle), de(belegte / len(alle) * 100), len(set(alle_q)), semi, verw, dp))
zeilen.append('Seitenprognose (Modellrechnung wie Messskript, Methodik bis Fazit 4.716 Wörter, 49 Einträge): %s Seiten' % de(seiten))
zeilen.append('Quellen (%d): %s' % (len(set(alle_q)), ' · '.join(sorted(set(alle_q)))))
zeilen.append('')
zeilen.append('Satz | Wörter | ohne Klammern | Herkunft | Wortlaut')
for k, i, x, w, wo, kl, h in alle:
    zeilen.append('%s S%d | %d | %d | %s | %s' % (k, i, w, wo, h, x))
zeilen.append('')
zeilen.append('Nicht in T (nach Frage 2 zurückgesetzt oder doppelt):')
for h, g in ENTFALLEN.items():
    zeilen.append('  %s: %s' % (h, g))
open(os.path.join(HIER, 'textstand_T_messung.txt'), 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
print('\n'.join(zeilen))

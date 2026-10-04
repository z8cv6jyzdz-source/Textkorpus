# -*- coding: utf-8 -*-
"""
schritt4_messung.py — Schritt 4 des Tasks „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (30.09.2026)

Setzt die Einleitung aus dem Textstand T (textstand_T.json) und den Neufassungen der freigegebenen Potenziale
(Befund § 4, Klick 30.09., 17:32: P1 bis P4 und P9) zusammen und misst sie wie Manuskriptstand_2026-09-25.py
(Wörter = Leerraum-Token mit Belegklammern, Satzteilung mit derselben Funktion saetze()).
NEU enthält je Absatz die Sätze, die sich ändern, mit Status (vorgelegt oder freigegeben). Absätze ohne Eintrag bleiben wortgleich.
Liest textstand_T.json und textstand_V.json aus dem eigenen Ordner, sonst aus dem Staging-Pfad.
Seitenprognose wie textstand_T.py (Parameter aus ..\\Seitenmodell_2026-09-28.csv, Methodik bis Fazit 4.716 Wörter, 49 Einträge).
Prüft per Assertion, dass B1b nach P1 und P9 wortgleich mit der freigegebenen Fassung (textstand_V.json) ist.
VARIANTEN enthält Sätze, die nur per Klick an die Stelle der Neufassung treten, jede Variante für sich gemessen (zuerst B3 S5
ohne Ferguson et al., 2024, seit Klick 18:46 in NEU, dann B4-P4a und B4-P3e, beide nach Klick 19:45 nicht gewählt und nur
noch zur Dokumentation gemessen). Geschrieben wird der Stand ohne Variante.
Nach dem Einsetzen der Neufassungen wird jeder Absatz neu in Sätze geteilt, weil eine Neufassung zwei Sätze enthalten kann (B4 S1).
Je Absatz zusätzlich Belegklammern und narrative Zitate (Autor mit Jahr in Klammern im Satz, Prüfgröße für „Quelle als Subjekt“).
Schreibt schritt4_messung.txt und schritt4_stand.json. Ohne Semikolon (chr(59)).
"""
import json, os, re, statistics as st

HIER = os.path.dirname(os.path.abspath(__file__))
STAGING = '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Abgleich_Einleitung_2026-09-30'
SEMI = chr(59)
FOLGE = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']


def lade(name):
    for ort in (HIER, STAGING):
        p = os.path.join(ort, name)
        if os.path.exists(p):
            return json.load(open(p, encoding='utf-8'))['absaetze']
    raise FileNotFoundError(name)


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


def w(s):
    return len(s.split())


T = {k: saetze(v) for k, v in lade('textstand_T.json').items()}
V = {k: saetze(v) for k, v in lade('textstand_V.json').items()}
assert sum(w(s) for k in FOLGE for s in T[k]) == 913

# Neufassungen je Absatz: Satzindex (0-basiert) -> (neuer Satz, Potenzial, Status)
NEU = {
    'B1b': {
        0: (V['B1b'][0], 'P1', 'freigegeben 18:02'),   # freigegebene Fassung B1 § 1.2 S1
        6: (V['B1b'][6], 'P9', 'freigegeben 18:02'),   # freigegebene Fassung B1 § 1.2 S7
    },
    'B3': {  # P2 und Klick § 2.7 (a): ohne „und valide“, Klammer nur mit Dugdale et al. (2019)
        4: (T['B3'][4].replace('als reliable und valide feldbasierte', 'als reliable feldbasierte')
            .replace(' (Dugdale et al., 2019' + SEMI + ' Ferguson et al., 2024).', ' (Dugdale et al., 2019).'),
            'P2 und Passung (Klick § 2.7 a)', 'freigegeben 18:46'),
    },
    'B4': {  # P3: T S1 wird zu Fassung 3 S1 und S2 (Freigabe 29.09., 17:44). P4: Radnor modal mit „auch ohne Training“
        0: (V['B4'][0] + ' ' + V['B4'][1], 'P3 als P3b', 'freigegeben 19:45'),
        1: (V['B4'][2].replace(' (Radnor et al., 2018).',
                               ', wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018).'), 'P4 als P4c', 'freigegeben 19:45'),
    },
}
assert NEU['B3'][4][0].count('reliable feldbasierte') == 1 and 'valide' not in NEU['B3'][4][0]
assert 'Ferguson' not in NEU['B3'][4][0] and NEU['B3'][4][0].endswith('(Dugdale et al., 2019).')
assert NEU['B4'][1][0] != V['B4'][2] and 'auch ohne Training, wozu' in NEU['B4'][1][0] and 'infolgedessen' not in NEU['B4'][1][0]

# Varianten, die nur per Klick an die Stelle der Neufassung treten, jede für sich gemessen:
# Name -> {Absatz: {Satzindex im Textstand T: (Satz, Anlass)}}
VARIANTEN = {
    'B4-P4a DVZ-Bezug gestrichen (Fassung 3 S3, Freigabe 17:44, nach Klick 19:45 nicht gewählt)': {
        'B4': {1: (V['B4'][2], 'Klick § 3.7 b, nicht gewählt')},
    },
    'B4-P3e ein Satz ohne Spanne (erwogen, nicht vorgeschlagen, Textvorschlag § 3.2)': {
        'B4': {0: ('Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel, den Jungen in einer britischen '
                   'Längsschnittstudie im Mittel mit 14 Jahren erreichten (Tanner et al., 1966).', 'nicht zur Wahl')},
    },
}


def stand(variante=None):
    out = {}
    for k in FOLGE:
        s = list(T[k])
        for i, (neu, _, _) in NEU.get(k, {}).items():
            s[i] = neu
        if variante:
            for i, (var, _) in VARIANTEN[variante].get(k, {}).items():
                s[i] = var
        out[k] = saetze(' '.join(s))  # neu geteilt, weil eine Neufassung zwei Sätze enthalten kann
    return out


S = stand()
SVS = {name: stand(name) for name in VARIANTEN}
assert ' '.join(S['B1b']) == ' '.join(V['B1b']), 'B1b weicht von der Freigabe ab'
assert S['B3'] == saetze(' '.join(S['B3'])) and len(S['B3']) == 5
assert S['B4'][:3] == [V['B4'][0], V['B4'][1], NEU['B4'][1][0]] and S['B4'][3:] == T['B4'][2:], 'B4 falsch zusammengesetzt'
assert len(S['B4']) == 7

p = {}
_SM = os.path.normpath(os.path.join(HIER, '..', 'Seitenmodell_2026-09-28.csv'))
if not os.path.isfile(_SM):
    _SM = '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Seitenmodell_2026-09-28.csv'
for z in open(_SM, encoding='utf-8').read().splitlines()[1:]:
    f = z.split(SEMI)
    p[f[0]] = float(f[1])


def seitenprognose(woerter, rest=4716):
    return (woerter / p['dichte_einleitung'] + rest / p['dichte_kapitel_4_bis_7'] + p['objekte_textteil'] * p['seiten_je_objekt']
            + p['kapitelenden_textteil'] * p['seiten_je_kapitelende'] + p['eintraege_basis'] / p['eintraege_je_seite']
            + p['seiten_je_kapitelende'])


NARRATIV = re.compile(r"[A-ZÄÖÜ][\w’'-]+(?: et al\.| und [A-ZÄÖÜ][\w’'-]+| & [A-ZÄÖÜ][\w’'-]+)? \(\d{4}")


def block(zst, titel):
    z = [titel, '']
    z.append('Absatz | Sätze | Wörter T | Wörter neu | Differenz | ohne Belegklammern neu | längster Satz neu | Median neu'
             ' | Belegklammern | narrative Zitate')
    for k in FOLGE:
        wt = sum(w(x) for x in T[k])
        wn = sum(w(x) for x in zst[k])
        tk = ' '.join(zst[k])
        z.append('%s | %d | %d | %d | %+d | %d | %d | %.1f | %d | %d' % (
            k, len(zst[k]), wt, wn, wn - wt, sum(w(ohne_belege(x)) for x in zst[k]), max(w(x) for x in zst[k]),
            st.median([w(x) for x in zst[k]]), len(KLAMMER.findall(tk)), len(NARRATIV.findall(KLAMMER.sub('', tk)))))
    alle = [x for k in FOLGE for x in zst[k]]
    gesamt = sum(w(x) for x in alle)
    z.append('')
    z.append('Einleitung: %d Wörter (T 913), ohne Belegklammern %d, %d Sätze, Median %.1f, längster Satz %d' % (
        gesamt, sum(w(ohne_belege(x)) for x in alle), len(alle), st.median([w(x) for x in alle]), max(w(x) for x in alle)))
    text = ' '.join(alle)
    z.append('Semikola außerhalb von Belegklammern: %d · Belegklammern: %d · Sätze mit Beleg: %d · Quellen: %d' % (
        KLAMMER.sub('', text).count(SEMI), len(KLAMMER.findall(text)), sum(1 for x in alle if KLAMMER.search(x)),
        len(set(quellen(text)))))
    z.append('Abschnittsverweise: %d · Doppelpunkte außerhalb von Belegklammern: %d · narrative Zitate: %d' % (
        len(re.findall(r'\b(Abschn\.|Abschnitt|Kapitel)\s*\d', text)), KLAMMER.sub('', text).count(':'),
        len(NARRATIV.findall(KLAMMER.sub('', text)))))
    sp = seitenprognose(gesamt)
    z.append('Seitenprognose (Modellrechnung wie textstand_T.py): %.4f Seiten, gerundet %.1f (T: %.4f, gerundet %.1f)' % (
        sp, round(sp, 1), seitenprognose(913), round(seitenprognose(913), 1)))
    return z


zeilen = block(S, 'Schritt 4 — Messung (30.09.2026), Textstand T gegen den Stand mit den Neufassungen')
zeilen.append('B1b wortgleich mit der Freigabe (Textvorschlag B1 § 1.2): ja (Assertion)')
zeilen.append('')
zeilen.append('Geänderte Sätze:')
for k in FOLGE:
    for i, (neu, pot, status) in sorted(NEU.get(k, {}).items()):
        zeilen.append('%s S%d (%s, %s): %d -> %d Wörter' % (k, i + 1, pot, status, w(T[k][i]), w(neu)))
        zeilen.append('  alt: ' + T[k][i])
        zeilen.append('  neu: ' + neu)
zeilen.append('')
if VARIANTEN:
    for name, var in VARIANTEN.items():
        zeilen += block(SVS[name], 'Variante (nur per Klick): ' + name)
        for k, saetze_var in var.items():
            for i, (satz, anlass) in sorted(saetze_var.items()):
                zeilen.append('%s, Satz %d des Textstands (%s): Neufassung %d -> Variante %d Wörter' % (
                    k, i + 1, anlass, w(NEU[k][i][0]) if i in NEU.get(k, {}) else w(T[k][i]), w(satz)))
                zeilen.append('  Variante: ' + satz)
        zeilen.append('')
else:
    zeilen.append('Varianten: keine offen')
open(os.path.join(HIER, 'schritt4_messung.txt'), 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
json.dump({'quelle': 'Stand Schritt 4 (Textstand T mit Neufassungen)', 'absaetze': {k: ' '.join(S[k]) for k in FOLGE},
           'neu': {k: {str(i + 1): [p, s] for i, (_, p, s) in v.items()} for k, v in NEU.items()}},
          open(os.path.join(HIER, 'schritt4_stand.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n'.join(zeilen))

# -*- coding: utf-8 -*-
"""
wortbilanz_schritt3.py — Schritt 3 des Tasks „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (30.09.2026)

Misst die fünf Sätze im Wortlaut des Verfassers (Befund § 2.5, § 3.5) gegen die freigegebenen Fassungen und
gegen einfache Varianten, die sich ohne neuen Wortlaut ergeben (Streichung, Einfügung, Wortersatz).
Grundlage der Wortbilanz in Befund § 4. Wörter wie Manuskriptstand_2026-09-25.py (Leerraum-Token mit Belegklammern),
Satzteilung mit derselben Funktion saetze() wie textstand_T.py.
Drei Zeilen sind Entwürfe nur für den Richtwert (P3c, P3d, P4c), keine Textvorschläge. Stand nach der Zweitprüfung von Schritt 3.
Liest textstand_T.json und textstand_V.json aus dem eigenen Ordner, sonst aus dem Staging-Pfad.
Schreibt wortbilanz_schritt3.txt. Ohne Semikolon (chr(59)).
"""
import json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
STAGING = '/mnt/user-data/uploads/Bachelorarbeit/Claude/03_Skripte/Abgleich_Einleitung_2026-09-30'


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


def w(s):
    return len(s.split())


T = {k: saetze(v) for k, v in lade('textstand_T.json').items()}
V = {k: saetze(v) for k, v in lade('textstand_V.json').items()}
GESAMT = sum(w(s) for k in T for s in T[k])
assert GESAMT == 913, GESAMT


def ersetze(satz, alt, neu):
    assert satz.count(alt) == 1, (alt, satz)
    return satz.replace(alt, neu)


zeilen = []


def zeile(nr, bezeichnung, alt, neu, art):
    d = w(neu) - w(alt)
    zeilen.append((nr, bezeichnung, w(alt), w(neu), d, art, neu))


# P1 B1b S1: freigegebene Fassung (Textvorschlag B1 § 1.2)
zeile('P1', 'B1b S1 Freigabe 07:00', T['B1b'][0], V['B1b'][0], 'gemessen')
# P2 B3 S5: Wortlaut des Verfassers ohne „und valide“ · zum Vergleich die Freigabe (B3 bis B5 § 1, „als reliabel“)
zeile('P2', 'B3 S5 ohne „und valide“', T['B3'][4], ersetze(T['B3'][4], 'reliable und valide ', 'reliable '), 'gemessen')
zeile('P2*', 'B3 S5 Freigabe (Vergleich)', T['B3'][4], V['B3'][4], 'gemessen')
# P3 B4 S1: nur „Jungen“ · Rückkehr zu B4 Fassung 3 S1 und S2 · Entwurf mit Population (nur Richtwert)
zeile('P3a', 'B4 S1 nur „Jungen“ statt „jugendliche“', T['B4'][0], ersetze(T['B4'][0], 'jugendliche', 'Jungen'), 'gemessen, setzt P3 nicht um (F17 § 6.4)')
zeile('P3b', 'B4 S1 wie Fassung 3 S1 und S2', T['B4'][0], V['B4'][0] + ' ' + V['B4'][1], 'gemessen')
ENTWURF_P3 = ('In dieser Altersspanne befinden sich Jungen häufig in der Phase um den Wachstumsgipfel, '
              'den sie in einer britischen Längsschnittstudie im Mittel mit 14 Jahren erreichten (Tanner et al., 1966).')
zeile('P3c', 'B4 S1 mit Studie und Alter (Entwurf, Richtwert)', T['B4'][0], ENTWURF_P3, 'Richtwert')
ENTWURF_P3D = ('Spieler der U15 befinden sich nach einer britischen Längsschnittstudie an Jungen häufig '
               'in der Phase um den Wachstumsgipfel (Tanner et al., 1966).')
zeile('P3d', 'B4 S1 mit Studie ohne Alter, ohne Rückgriff (Entwurf, Richtwert)', T['B4'][0], ENTWURF_P3D, 'Richtwert')
# P4 B4 S2: Freigabe (B4 Fassung 3 S3) · Wortlaut des Verfassers mit „auch ohne Training“
zeile('P4a', 'B4 S2 Freigabe 17:44', T['B4'][1], V['B4'][2], 'gemessen')
zeile('P4b', 'B4 S2 Verfasser mit „auch ohne Training“', T['B4'][1],
      ersetze(T['B4'][1], 'Kindern und Jugendlichen (', 'Kindern und Jugendlichen auch ohne Training ('), 'gemessen, Indikativ bleibt')
ENTWURF_P4C = ('Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern '
               'und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018).')
zeile('P4c', 'B4 S2 DVZ-Bezug modal mit „auch ohne Training“ (Entwurf, Richtwert)', T['B4'][1], ENTWURF_P4C, 'Richtwert')
# P9 B1b S7: Freigabe (B1 § 1.2), gleich dem Wortlaut des Verfassers ohne „und“
zeile('P9', 'B1b S7 Freigabe 07:00', T['B1b'][6], V['B1b'][6], 'gemessen')
assert V['B1b'][6] == ersetze(T['B1b'][6], 'verringerten und (', 'verringerten (')

aus = ['Wortbilanz Schritt 3 (30.09.2026) — Textstand T: %d Wörter, Obergrenze 1.200, Korpus 506 bis 927' % GESAMT, '']
aus.append('Nr   | Variante | alt | neu | Differenz | Art')
for nr, bez, a, n, d, art, neu in zeilen:
    aus.append('%-4s | %s | %d | %d | %+d | %s' % (nr, bez, a, n, d, art))
aus.append('')
empf_min = sum(d for nr, _, _, _, d, _, _ in zeilen if nr in ('P1', 'P2', 'P3d', 'P4a', 'P9'))
empf_max = sum(d for nr, _, _, _, d, _, _ in zeilen if nr in ('P1', 'P2', 'P3b', 'P4c', 'P9'))
empf_mitte = sum(d for nr, _, _, _, d, _, _ in zeilen if nr in ('P1', 'P2', 'P3c', 'P4c', 'P9'))
aus.append('Empfohlen P1 bis P4 und P9 (regelkonforme Varianten): kleinste %+d (%d Wörter, P3d und P4a), größte %+d (%d, P3b und P4c), mit P3c und P4c %+d (%d, Richtwert)'
           % (empf_min, GESAMT + empf_min, empf_max, GESAMT + empf_max, empf_mitte, GESAMT + empf_mitte))
aus.append('')
aus.append('Varianten im Wortlaut:')
for nr, bez, a, n, d, art, neu in zeilen:
    aus.append('%s  %s' % (nr, neu))
open(os.path.join(HIER, 'wortbilanz_schritt3.txt'), 'w', encoding='utf-8').write('\n'.join(aus) + '\n')
print('\n'.join(aus))

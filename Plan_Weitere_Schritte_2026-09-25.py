# -*- coding: utf-8 -*-
"""
Plan_Weitere_Schritte_2026-09-25.py — Plan der weiteren Schritte nach dem Task 4.7 (Auftrag des Verfassers vom 25.09.2026)
Bachelorarbeit U15-Plyometrie · DSHS Köln

Erzeugt `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Projektkopie `claude/…`). Alle Wort-, Semikolon-, Verweis- und
Platzhalterzahlen stammen aus der Messung `Manuskriptstand_2026-09-25.csv` (Erzeuger `Manuskriptstand_2026-09-25.py` am
Master), die Budgetarithmetik rechnet das Skript, die Zählung der Maßnahmenliste liest es aus der Datei. Keine Zahl von
Hand. Ohne Semikolon (chr(59)), auch im erzeugten Text.
Aufruf: MASTER=<Master.docx> MASSNAHMENLISTE=<Massnahmenliste.md> BEREINIGUNG=<Bereinigungsprotokoll.txt>
        python Plan_Weitere_Schritte_2026-09-25.py <Manuskriptstand_2026-09-25.csv> <Plan.md>
Fassung: 2026-09-25, Rev. 2 (abends, nach den Verfasserentscheidungen zu Vorgabe, Reihenfolge und Anhängen). Rev. 1 vom
selben Abend ist ersetzt (Gegenfinanzierung der Anhebung von 4.7, Ergebniskapitel vor der Revision).
"""
import sys
import csv
import os
import re

CSVP, OUT = sys.argv[1], sys.argv[2]
SEMI = chr(59)


def tsd(n):
    return format(int(n), ',').replace(',', '.')


def vz(n):
    n = int(n)
    if n == 0:
        return '±0'
    return ('+' + tsd(n)) if n > 0 else ('−' + tsd(-n))


rows = {r['nr']: r for r in csv.DictReader(open(CSVP, encoding='utf-8'))}
# Vorgabe: Budgets nach F14 § 5.2 und Gliederung v4 § 3.4, 4.7 = 550 (Verfasser 25.09., abends: keine Anhebung)
BUDGET = {'1': 600, '2.1': 800, '2.2': 850, '2.3': 600, '2.4': 700, '2.5': 400, '3': 200,
          '4.1': 300, '4.2': 215, '4.3': 340, '4.4': 420, '4.5.1': 420, '4.5.2': 150, '4.6': 155, '4.7': 550,
          '5.1': 230, '5.2': 220, '6.1': 700, '6.2': 400, '6.3': 500, '7': 250}
UNTER = {'2.4': ['2.4.1', '2.4.2', '2.4.3'], '4.4': ['4.4.1', '4.4.2', '4.4.3']}


def feld(nr, name):
    n = int(rows[nr][name])
    for u in UNTER.get(nr, []):
        n += int(rows[u][name])
    return n


ist = {k: feld(k, 'woerter') for k in BUDGET}
semi = {k: feld(k, 'semikola') for k in BUDGET}
verw = {k: feld(k, 'abschnittsverweise') for k in BUDGET}
s40 = {k: feld(k, 'saetze_ueber_40') for k in BUDGET}
plh = {k: feld(k, 'platzhalter') for k in BUDGET}
mark = {k: feld(k, 'marker') for k in BUDGET}
geschrieben = sum(ist.values())
leer = [k for k in BUDGET if ist[k] == 0]
budget_leer = sum(BUDGET[k] for k in leer)
k2_ist = sum(ist[k] for k in ['2.1', '2.2', '2.3', '2.4'])
k2_bud = sum(BUDGET[k] for k in ['2.1', '2.2', '2.3', '2.4'])
K4 = ['4.1', '4.2', '4.3', '4.4', '4.5.1', '4.5.2', '4.6', '4.7']
k4_ist = sum(ist[k] for k in K4)
k4_bud = sum(BUDGET[k] for k in K4)
k4o_ist = k4_ist - ist['4.7']
gesamt_bei_budget = geschrieben + budget_leer
kuerzung = gesamt_bei_budget - 9000
kuerz_k2 = k2_ist - k2_bud
kuerz_k4 = k4_ist - k4_bud
kuerz_47 = ist['4.7'] - BUDGET['4.7']
semi_ges = sum(semi.values())
verw_ges = sum(verw.values())
s40_ges = sum(s40.values())
s40_k2 = sum(s40[k] for k in ['2.1', '2.2', '2.3', '2.4'])
plh_anh = sum(int(r['platzhalter']) for k, r in rows.items() if k.startswith('Anhang H'))
plh_ges = sum(int(r['platzhalter']) for r in rows.values())
mark_ges = sum(int(r['marker']) for r in rows.values())
if kuerz_k2 + kuerz_k4 != kuerzung or k4_bud != 2550 or sum(BUDGET.values()) != 9000:
    raise SystemExit('Budgetarithmetik geht nicht auf')
MASTER = os.environ.get('MASTER')
gr_master = tsd(os.path.getsize(MASTER)) if MASTER else '⟨Größe⟩'
ML = os.environ.get('MASSNAHMENLISTE')
BER = os.environ.get('BEREINIGUNG')
if not ML or not BER:
    raise SystemExit('Umgebungsvariablen MASSNAHMENLISTE und BEREINIGUNG fehlen')
ml_text = open(ML, encoding='utf-8').read()
offen_haupt = sum(1 for z in ml_text.split('\n') if z.startswith('- [ ]'))
offen_teil = sum(1 for z in ml_text.split('\n') if z.lstrip().startswith('- [ ]') and not z.startswith('- [ ]'))
ber = open(BER, encoding='utf-8').read()
m_ber = re.search(r'Geschlossen: (\d+) Hauptpunkte, (\d+) Teilpunkte', ber)
geschl_haupt, geschl_teil = int(m_ber.group(1)), int(m_ber.group(2))

tab = ['| Abschnitt | Ist | Budget (Vorgabe) | Differenz | Semikola | Verweise | Sätze > 40 | Platzhalter | Marker |',
       '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for k in BUDGET:
    tab.append('| %s | %s | %s | %s | %d | %d | %d | %d | %d |' % (
        k, tsd(ist[k]), tsd(BUDGET[k]), vz(ist[k] - BUDGET[k]), semi[k], verw[k], s40[k], plh[k], mark[k]))
tab.append('| **Kapitel 1 bis 7** | **%s** | **9.000** | **%s** | **%d** | **%d** | **%d** | **%d** | **%d** |' % (
    tsd(geschrieben), vz(geschrieben - 9000), semi_ges, verw_ges, s40_ges, sum(plh.values()), sum(mark.values())))
TAB = '\n'.join(tab)

KUERZ = ' · '.join('%s %s → %s' % (k, tsd(ist[k]), tsd(BUDGET[k])) for k in ['4.3', '4.4', '4.5.1', '4.5.2', '4.6', '4.7', '4.1', '2.4', '2.3', '2.1', '2.2'])

TEXT = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Plan_Weitere_Schritte_2026-09-25_Vorlage.md'), encoding='utf-8').read()

werte = dict(
    TAB=TAB, KUERZ=KUERZ, geschrieben=tsd(geschrieben), budget_leer=tsd(budget_leer), gesamt_bei_budget=tsd(gesamt_bei_budget),
    kuerzung=tsd(kuerzung), kuerz_k2=tsd(kuerz_k2), kuerz_k4=tsd(kuerz_k4), kuerz_47=tsd(kuerz_47),
    semi_ges=semi_ges, verw_ges=verw_ges, s40_ges=s40_ges, plh_ges=plh_ges, mark_ges=mark_ges, s40_k2=s40_k2,
    k2_ist=tsd(k2_ist), k2_bud=tsd(k2_bud), k2_diff=vz(k2_ist - k2_bud), k4o_ist=tsd(k4o_ist), k4o_diff=vz(k4o_ist - 2000),
    k4_ist=tsd(k4_ist), k4_diff=vz(k4_ist - k4_bud), plh_anh=plh_anh, gr_master=gr_master,
    offen_haupt=offen_haupt, offen_teil=offen_teil, geschl_haupt=geschl_haupt, geschl_teil=geschl_teil,
    b51=230, b52=220, b61=700, b62=400, b63=500, b7=250, b1=600, b25=400, b3=200,
    i43=tsd(ist['4.3']), b43=340, s43=semi['4.3'], v43=verw['4.3'],
    i44=tsd(ist['4.4']), b44=420, s44=semi['4.4'], v44=verw['4.4'], k44=tsd(ist['4.4'] - 420),
    i452=tsd(ist['4.5.2']), b452=150, s452=semi['4.5.2'], v452=verw['4.5.2'],
    i46=tsd(ist['4.6']), b46=155, s46=semi['4.6'], v46=verw['4.6'],
    i41=tsd(ist['4.1']), b41=300, i451=tsd(ist['4.5.1']), b451=420, i47=tsd(ist['4.7']), b47=550,
    i24=tsd(ist['2.4']), b24=700, s24=semi['2.4'], v24=verw['2.4'], x24=s40['2.4'],
    i23=tsd(ist['2.3']), b23=600, s23=semi['2.3'], v23=verw['2.3'], x23=s40['2.3'],
    i21=tsd(ist['2.1']), b21=800, s21=semi['2.1'], v21=verw['2.1'], x21=s40['2.1'],
    i22=tsd(ist['2.2']), b22=850, s22=semi['2.2'], v22=verw['2.2'], x22=s40['2.2'],
)
text = TEXT % werte
if SEMI in text:
    stelle = text.index(SEMI)
    raise SystemExit('Semikolon im Plan: ' + text[max(0, stelle - 60):stelle + 20])
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('Plan Rev. 2 geschrieben: %d Wörter, Kürzungsauftrag %d, 4.7 −%d, offen %d/%d' % (len(text.split()), kuerzung, kuerz_47, offen_haupt, offen_teil))

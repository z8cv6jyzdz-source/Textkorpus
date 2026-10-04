# -*- coding: utf-8 -*-
"""
Handprobe_2026-09-25.py — Handprobenblatt für Phase 6.3 des Auswertungsverfahrens, als Excel-Formelprobe
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 6.3

Zweck: Ein Excel-Arbeitsblatt mit 34 vorab bestimmten Kennwerten der berichteten R-Rechnung.
Fassung 2 trägt in jeder Zelle „Handwert“ eine Excel-Formel, die den Kennwert allein aus den
Eingangsblättern (Datenstand, Anlagen) nach den Regeln der Spezifikation berechnet. Excel ist damit
eine dritte Implementierung der 34 Kennwerte. Kein Zwischenwert wird aus der Ergebnisdatei in die
Formeln übernommen. Ausnahme nach dem vorab festgelegten Rechenweg von Kennwert Nr. 34: p und b1 der
Zielgrößen CM und SBJ stehen als Eingang aus der Ergebnisdatei in einer eigenen Tabelle.
Zusätzlich vergleicht das Blatt „Formelwerte“ die per Formel abgeleiteten Zwischengrößen je Spieler
mit der berichteten Rechnung (Blatt „Analysedaten“).

Eingang: Datenstand_2026-09-24 (CSV), Ergebnisse_R_2026-09-25.csv (berichtete Rechnung),
Ergebnisse_Python_2026-09-25.csv (Gegenprobe), Spezifikation_2026-09-24_Koeffizienten_KR.csv,
Spezifikation_2026-09-24_Vokabular.csv
Aufruf: python Handprobe_2026-09-25.py <Blindordner> <Ergebnisse_Python.csv> <Ziel.xlsx>
Fassung: 2026-09-25, zweite Fassung (Excel-Formelprobe, Verfasserentscheidung 25.09.2026, Register R12).
Änderung gegenüber der ersten Fassung: alle 34 Handwerte als Formeln, Hilfsspalten in Versuchsdaten
und Fragebogen_A, neue Blätter Vokabular, Formelwerte und ANCOVA_Z30, Zusatzprüfungen, Anleitung neu.
Die Auswahl der 34 Kennwerte, die Sollwerte und die Toleranzen sind unverändert.
"""
import sys
import os
import csv
import math
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EINGANG, PY_CSV, ZIEL = sys.argv[1], sys.argv[2], sys.argv[3]
DS = os.path.join(EINGANG, 'Datenstand_2026-09-24')
R_CSV = os.path.join(EINGANG, 'Abgabe_R_2026-09-25', 'Ergebnisse_R_2026-09-25.csv')


def lies(p):
    with open(p, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


V = lies(os.path.join(DS, 'Versuchsdaten.csv'))
PERS = lies(os.path.join(DS, 'Personendaten.csv'))
FB = lies(os.path.join(DS, 'Fragebogen_A.csv'))
KR = lies(os.path.join(EINGANG, 'Spezifikation_2026-09-24_Koeffizienten_KR.csv'))
VOK = lies(os.path.join(EINGANG, 'Spezifikation_2026-09-24_Vokabular.csv'))
ZUO = lies(os.path.join(DS, 'Zuordnung_Fragebogen.csv'))
R = {r['Kennung']: r for r in lies(R_CSV)}
PY = {r['Kennung']: r for r in lies(PY_CSV)}


def wert(d, k):
    v = d[k]['Wert']
    return float(v) if v != '' else None


codes = [p['Code'] for p in PERS]
gruppe = {p['Code']: p['Gruppe'] for p in PERS}
pers_v = {p['Code']: p for p in PERS}
NV, NP, NF, NK, NZ = len(V), len(PERS), len(FB), len(KR), len(ZUO)   # Zeilenzahlen der Datenblätter

FONT = 'Arial'
f_norm = Font(name=FONT, size=10)
f_bold = Font(name=FONT, size=10, bold=True)
f_h = Font(name=FONT, size=14, bold=True, color='1F3864')
f_blau = Font(name=FONT, size=10, color='0000FF')
f_gruen = Font(name=FONT, size=10, color='008000')
f_grau = Font(name=FONT, size=8, color='808080')
fill_kopf = PatternFill('solid', fgColor='D6E4F0')
fill_hand = PatternFill('solid', fgColor='FFFF00')
fill_zebra = PatternFill('solid', fgColor='EEF3F9')
fill_hilf = PatternFill('solid', fgColor='E2EFDA')
rand = Border(*(Side(style='thin', color='BFBFBF'),) * 4)
wrap = Alignment(wrap_text=True, vertical='top')

wb = Workbook()

# ---------------------------------------------------------------- Bereiche der Datenblätter (absolut)
def rng(sheet, col, n_rows):
    return "%s!$%s$2:$%s$%d" % (sheet, col, col, n_rows + 1)


VD = {c: rng('Versuchsdaten', c, NV) for c in 'ABCDEFGHIJKLMNOPQ'}
PD = {c: rng('Personendaten', c, NP) for c in 'ABCDEFGHIJ'}
FA = {c: rng('Fragebogen_A', c, NF) for c in 'ABCDEFGHIJKLM'}
KO = {c: rng('Koeffizienten_KR', c, NK) for c in 'ABCDE'}
ZU = {c: rng('Zuordnung', c, NZ) for c in 'AB'}

# ---------------------------------------------------------------- Anleitung
ws = wb.active
ws.title = 'Anleitung'
zeilen = [
    ('Handprobenblatt Phase 6.3 als Excel-Formelprobe — Auswertungsverfahren 2026-09-24, Schritt 6.3', f_h),
    ('Bachelorarbeit U15-Plyometrie · Datenstand 2026-09-24 · berichtete Rechnung: Blindrechnung in R vom 25.09.2026 · Gegenprobe: Python-Kette (Gegenprobe_Python_2026-09-25.py) · Erzeuger dieses Blatts: Handprobe_2026-09-25.py, Fassung 2', f_norm),
    ('', f_norm),
    ('Zweck', f_bold),
    ('Das Auswertungsverfahren sieht in 6.3 vor, dass der Verfasser vorab bestimmte Kennwerte in Excel nachrechnet. Verfasserentscheidung vom 25.09.2026 (Register R12): Die Handprobe wird als Formelprobe geführt. Jede gelbe Zelle „Handwert“ im Blatt „Handprobe“ enthält eine Excel-Formel, die den Kennwert allein aus den Eingangsblättern nach den Regeln der Spezifikation berechnet. Excel ist damit eine dritte, von R und Python unabhängige Implementierung der 34 Kennwerte. Die Formeln sind offen lesbar und in Excel Schritt für Schritt nachvollziehbar.', f_norm),
    ('', f_norm),
    ('Vorgehen für den Verfasser', f_bold),
    ('1. Datei in Excel öffnen. Excel berechnet alle Formeln beim Öffnen. Die Spalte „Urteil“ im Blatt „Handprobe“ muss bei allen 34 Kennwerten „stimmt“ zeigen, ebenso die Zusatzprüfungen unter der Tabelle.', f_norm),
    ('2. Formeln stichprobenartig lesen (Zelle anklicken): Sie greifen nur auf die Blätter Versuchsdaten, Personendaten, Fragebogen_A, Koeffizienten_KR, Vokabular und Zuordnung zu, teils über die Rechenblätter Formelwerte, TE_Z30_prae und ANCOVA_Z30. Kein Handwert liest einen Wert aus der Ergebnisdatei. Einzige Ausnahme nach dem vorab festgelegten Rechenweg von Kennwert Nr. 34: p und b1 der Zielgrößen CM und SBJ stehen als Eingang aus der Ergebnisdatei in der kleinen Tabelle rechts neben den Kennwerten.', f_norm),
    ('3. Blatt „Formelwerte“: Die per Formel abgeleiteten Zwischengrößen je Spieler (Bestwerte, 505-Seitenmittel, %PAH, Setmitgliedschaft, Adhärenz) stehen neben dem Vergleich mit der berichteten Rechnung (Blatt „Analysedaten“, grüne Werte). Die Zahl der abweichenden Zellen steht in der Zusatzprüfung Z2.', f_norm),
    ('4. Ergebnis mit Datum in Zelle B4 des Blatts „Handprobe“ eintragen („bestanden“ oder Liste der abweichenden Nummern), Datei sichern. Danach Freigabe F2.', f_norm),
    ('', f_norm),
    ('Aufbau der Rechenblätter', f_bold),
    ('Versuchsdaten: Spalten A bis H unverändert aus dem Datenstand. Hilfsspalten (grün hinterlegt, Formeln): I Gruppe des Spielers · J gültig_roh (S02 Regel 1: Wert vorhanden, ungültig leer) · K, L, M Teilzeiten 5, 10, 30 m des Laufs (gleiche Versuchsnummer, nur gültig_roh) · N auslösegestört (S02 Regel 2: ein Abschnitt mit Δt ≤ 0 s oder v > 10,0 m/s) · O gültig (S02 Regel 3) · P Status des Spielers · Q Ausfallkategorie (S03: NANG vor AUSL vor Vokabular).', f_norm),
    ('Fragebogen_A: Spalten A bis K unverändert. Hilfsspalten: L Listenlabel aus H010 mit den Fallkorrekturen (S06 Regel 1 und 2) · M Analysecode aus der Zuordnung (S06 Regel 3).', f_norm),
    ('Formelwerte: je Spieler S_in, W_lb, MP_in, a_lo, w, interpolierte Koeffizienten, PAS und %PAH (S05), Bestwerte 30 m, 505 je Seite und Seitenmittel, Standweitsprung, prä und post (S02, S04), ITT-Mitgliedschaft für 30 m, 505-Seitenmittel und Standweitsprung (S08 Regel 1), Adhärenz GANZ (S07 Regel 1 und 5), Rang im ITT-Set 30 m, rechts der Vergleich mit dem Blatt Analysedaten.', f_norm),
    ('TE_Z30_prae: gültige Versuche 30 m prä je Spieler (Formeln), k, Quadratsumme der Abweichungen vom Spielermittel, k − 1 (S10 Regel 1).', f_norm),
    ('ANCOVA_Z30: die Spieler des ITT-Sets 30 m in Blockform (über den Rang aus Formelwerte), LINEST für das Modell Post = b0 + b1·G + b2·Prä + b3·%PAH (S13), Hilfsspalten für die gepoolten Streuungen (S15).', f_norm),
    ('', f_norm),
    ('Hinweise', f_bold),
    ('Gruppe: Codes HL-xx und BW-xx sind IG (Verein A und B), VS-xx ist KG (Verein C). Zeitpunkte „prä“ und „post“. Toleranz der Urteile: Anzahlen exakt, übrige Größen relativ 1e-6 (Excel-Funktionen wie LINEST rechnen numerisch anders als die QR-Zerlegung, Unterschiede liegen weit unterhalb dieser Grenze).', f_norm),
    ('Die Formeln verwenden nur Funktionen, die Excel ab 2019 kennt: COUNTIFS, SUMIFS, AVERAGEIFS, MINIFS, MAXIFS, INDEX, MATCH, VLOOKUP, DEVSQ, STDEV.S, VAR.S, LINEST, T.DIST.2T, T.INV.2T, F.INV.RT. Ein Fehlerwert in einer Handwert-Zelle führt in der Spalte Urteil zu „FEHLER“, nie zu „stimmt“.', f_norm),
    ('Werte in diesem Blatt sind pseudonymisiert (Analysecodes). Die Datei bleibt im Projektordner (04_Uebergaben) und geht nicht an Dritte.', f_norm),
]
for i, (t, f) in enumerate(zeilen, 1):
    c = ws.cell(row=i, column=1, value=t)
    c.font = f
    c.alignment = wrap
ws.column_dimensions['A'].width = 150


# ---------------------------------------------------------------- Datenblätter
def daten_blatt(name, rows, spalten, breiten=None):
    s = wb.create_sheet(name)
    for j, sp in enumerate(spalten, 1):
        c = s.cell(row=1, column=j, value=sp)
        c.font = f_bold
        c.fill = fill_kopf
        c.border = rand
    for i, r in enumerate(rows, 2):
        for j, sp in enumerate(spalten, 1):
            v = r[sp]
            if v != '' and v is not None:
                try:
                    v = float(v) if ('.' in v or v.isdigit()) and sp not in ('Code', 'Listenlabel', 'Analysecode', 'STARTED', 'bemerkung_exakt', 'kategorie', 'bedeutung', 'quelle') else v
                except (ValueError, AttributeError):
                    pass
                if isinstance(v, float) and v.is_integer() and sp in ('Versuch', 'CASE', 'H010', 'H002', 'H003', 'H004', 'H005', 'H006', 'H007', 'H008', 'H009', 'Familiarisierung'):
                    v = int(v)
            c = s.cell(row=i, column=j, value=v if v != '' else None)
            c.font = f_norm
    for j, sp in enumerate(spalten, 1):
        s.column_dimensions[get_column_letter(j)].width = (breiten or {}).get(sp, 14)
    s.freeze_panes = 'A2'
    return s


def hilfsspalte(s, col, kopf, formel_je_zeile, n_rows, breite=16):
    c = s.cell(row=1, column=col, value=kopf)
    c.font = f_bold
    c.fill = fill_hilf
    c.border = rand
    for i in range(2, n_rows + 2):
        z = s.cell(row=i, column=col, value=formel_je_zeile(i))
        z.font = f_blau
        z.fill = fill_hilf
    s.column_dimensions[get_column_letter(col)].width = breite


sv = daten_blatt('Versuchsdaten', V, ['Code', 'Zeitpunkt', 'Test', 'Seite', 'Versuch', 'Wert', 'ungültig', 'Bemerkung'], {'Test': 16, 'Bemerkung': 30})
sp_ = daten_blatt('Personendaten', PERS, ['Code', 'Verein', 'Gruppe', 'Alter_prae', 'Koerperhoehe_prae', 'Koerpermasse_prae', 'Groesse_Mutter', 'Groesse_Vater', 'Familiarisierung', 'Status'], {'Alter_prae': 20, 'Status': 18})
sf = daten_blatt('Fragebogen_A', FB, ['CASE', 'STARTED', 'H010', 'H002', 'H003', 'H004', 'H005', 'H006', 'H007', 'H008', 'H009'], {'STARTED': 20})
daten_blatt('Koeffizienten_KR', KR, ['alter_jahre', 'beta0', 'stature_in', 'weight_lb', 'midparent_in'])
daten_blatt('Vokabular', VOK, ['bemerkung_exakt', 'kategorie', 'bedeutung', 'quelle'], {'bemerkung_exakt': 30, 'bedeutung': 40, 'quelle': 44})
daten_blatt('Zuordnung', ZUO, ['Listenlabel', 'Analysecode'])

# Hilfsspalten Versuchsdaten (S02, S03)
hilfsspalte(sv, 9, 'Gruppe (Formel)', lambda i: '=INDEX(%s,MATCH(A%d,%s,0))' % (PD['C'], i, PD['A']), NV, 14)
hilfsspalte(sv, 10, 'gültig_roh (S02 R1)', lambda i: '=IF(AND(F%d<>"",G%d=""),1,0)' % (i, i), NV, 16)


def teilzeit(i, test):
    krit = '%s,$A%d,%s,$B%d,%s,"%s",%s,$E%d,%s,1' % (VD['A'], i, VD['B'], i, VD['C'], test, VD['E'], i, VD['J'])
    return '=IF(LEFT(C%d,7)<>"Sprint_","",IF(COUNTIFS(%s)=1,SUMIFS(%s,%s),""))' % (i, krit, VD['F'], krit)


hilfsspalte(sv, 11, 't5 des Laufs', lambda i: teilzeit(i, 'Sprint_5m'), NV, 12)
hilfsspalte(sv, 12, 't10 des Laufs', lambda i: teilzeit(i, 'Sprint_10m'), NV, 12)
hilfsspalte(sv, 13, 't30 des Laufs', lambda i: teilzeit(i, 'Sprint_30m'), NV, 12)


def ausloese(i):
    # Abschnitte zwischen aufeinanderfolgenden vorhandenen Teilzeiten, der erste ab 0 m mit t = 0 (S02 Regel 2)
    seg5 = 'IF(ISNUMBER(K{i}),IF(K{i}<=0,1,IF(5/K{i}>10,1,0)),0)'
    seg10 = 'IF(ISNUMBER(L{i}),IF(ISNUMBER(K{i}),IF(L{i}-K{i}<=0,1,IF(5/(L{i}-K{i})>10,1,0)),IF(L{i}<=0,1,IF(10/L{i}>10,1,0))),0)'
    seg30 = ('IF(ISNUMBER(M{i}),IF(ISNUMBER(L{i}),IF(M{i}-L{i}<=0,1,IF(20/(M{i}-L{i})>10,1,0)),'
             'IF(ISNUMBER(K{i}),IF(M{i}-K{i}<=0,1,IF(25/(M{i}-K{i})>10,1,0)),IF(M{i}<=0,1,IF(30/M{i}>10,1,0)))),0)')
    f = '=IF(LEFT(C{i},7)<>"Sprint_",0,IF(' + seg5 + '+' + seg10 + '+' + seg30 + '>0,1,0))'
    return f.replace('{i}', str(i))


hilfsspalte(sv, 14, 'auslösegestört (S02 R2)', ausloese, NV, 18)
hilfsspalte(sv, 15, 'gültig (S02 R3)', lambda i: '=IF(AND(J%d=1,N%d=0),1,0)' % (i, i), NV, 14)
hilfsspalte(sv, 16, 'Status (Formel)', lambda i: '=INDEX(%s,MATCH(A%d,%s,0))' % (PD['J'], i, PD['A']), NV, 18)
hilfsspalte(sv, 17, 'Kategorie (S03)',
            lambda i: '=IF(O%d=1,"",IF(AND(B%d="post",P%d="nicht angetreten"),"NANG",IF(N%d=1,"AUSL",IFERROR(VLOOKUP(H%d,Vokabular!$A$2:$B$%d,2,FALSE),"UNBEKANNT"))))' % (i, i, i, i, i, len(VOK) + 1), NV, 16)

# Hilfsspalten Fragebogen_A (S06 Regel 1 bis 3)
hilfsspalte(sf, 12, 'Listenlabel (S06 R1, R2)',
            lambda i: '=IF(OR(A%d=59,A%d=70),"BW-06",IF(OR(A%d=140,A%d=158,A%d=165,A%d=190,A%d=206),"BW-04",IF(C%d<=8,"HL-0"&C%d,"BW-"&IF(C%d-8<10,"0"&(C%d-8),C%d-8))))' % ((i,) * 12), NF, 22)
hilfsspalte(sf, 13, 'Analysecode (S06 R3)',
            lambda i: '=IFERROR(VLOOKUP(L%d,Zuordnung!$A$2:$B$%d,2,FALSE)&"","?")' % (i, NZ + 1), NF, 20)

# ---------------------------------------------------------------- Analysedaten je Spieler (aus der Ergebnisdatei, mit Kennung, unverändert)
sa = wb.create_sheet('Analysedaten')
spalten = [('Code', None), ('Gruppe', None), ('Verein', None), ('G (IG = 1)', None), ('%PAH', 'S05.PAH.PAH.PRE.P{c}.X'),
           ('BEST Z30 prä', 'S04.BEST.Z30.PRE.P{c}.X'), ('BEST Z30 post', 'S04.BEST.Z30.POST.P{c}.X'),
           ('BEST CM prä', 'S04.BEST.CM.PRE.P{c}.X'), ('BEST CM post', 'S04.BEST.CM.POST.P{c}.X'),
           ('BEST SBJ prä', 'S04.BEST.SBJ.PRE.P{c}.X'), ('BEST SBJ post', 'S04.BEST.SBJ.POST.P{c}.X'),
           ('ITT Z30', 'S08.MITGL.Z30.X.P{c}.ITT'), ('ITT CM', 'S08.MITGL.CM.X.P{c}.ITT'), ('ITT SBJ', 'S08.MITGL.SBJ.X.P{c}.ITT'),
           ('GANZ (Adhärenz)', 'S07.ADH.ADH.X.P{c}.GANZ')]
sa.cell(row=1, column=1, value='Zwischengrößen je Spieler aus der berichteten Rechnung (Ergebnisse_R_2026-09-25.csv), nur zum Vergleich. Zeile 2 nennt das Kennungsmuster der Spalte. Leer = fehlend mit Grund in der Ergebnisdatei. Die Formeln der Handprobe lesen dieses Blatt nicht.').font = f_norm
for j, (sp, muster) in enumerate(spalten, 1):
    c = sa.cell(row=3, column=j, value=sp)
    c.font = f_bold
    c.fill = fill_kopf
    c.border = rand
    sa.cell(row=2, column=j, value=muster or '').font = f_grau
    sa.column_dimensions[get_column_letter(j)].width = 14
for i, c in enumerate(codes, 4):
    sa.cell(row=i, column=1, value=c).font = f_norm
    sa.cell(row=i, column=2, value=gruppe[c]).font = f_norm
    sa.cell(row=i, column=3, value=pers_v[c]['Verein']).font = f_norm
    sa.cell(row=i, column=4, value=1 if gruppe[c] == 'IG' else 0).font = f_norm
    for j, (sp, muster) in enumerate(spalten, 1):
        if muster is None:
            continue
        k = muster.format(c=c)
        if k in R:
            v = wert(R, k)
            cell = sa.cell(row=i, column=j, value=(int(v) if (v is not None and sp.startswith(('ITT', 'GANZ'))) else v))
            cell.font = f_gruen
sa.freeze_panes = 'B4'
ANA_ERSTE, ANA_LETZTE = 4, 3 + len(codes)

# ---------------------------------------------------------------- Formelwerte je Spieler (dritte Implementierung, Formeln)
sw = wb.create_sheet('Formelwerte')
sw.cell(row=1, column=1, value='Zwischengrößen je Spieler, allein per Formel aus den Eingangsblättern (S02, S04, S05, S06, S07, S08). Blaue Zellen sind Formeln. Rechts der Vergleich mit dem Blatt Analysedaten (berichtete Rechnung): 0 = gleich innerhalb 1e-9 relativ oder beide leer, 1 = Abweichung.').font = f_norm
FW_KOPF = ['Code', 'Gruppe', 'Verein', 'G (IG = 1)',
           'S_in (S05 R2)', 'W_lb (S05 R2)', 'MP_in (S05 R3)', 'a_lo (S05 R6)', 'w (S05 R6)',
           'β0 interp.', 'β1 interp.', 'β2 interp.', 'β3 interp.', 'PAS_in (S05 R7)', '%PAH (S05 R8)',
           'k Z30 prä', 'BEST Z30 prä', 'k Z30 post', 'BEST Z30 post',
           'BEST CL prä', 'BEST CR prä', 'BEST CM prä (S04 R4)', 'BEST CL post', 'BEST CR post', 'BEST CM post',
           'BEST SBJ prä', 'BEST SBJ post',
           'ITT Z30 (S08 R1)', 'ITT CM', 'ITT SBJ', 'GANZ (S07 R1)', 'Rang im ITT Z30',
           '', 'Abw. %PAH', 'Abw. BEST Z30 prä', 'Abw. BEST Z30 post', 'Abw. BEST CM prä', 'Abw. BEST CM post',
           'Abw. BEST SBJ prä', 'Abw. BEST SBJ post', 'Abw. ITT Z30', 'Abw. ITT CM', 'Abw. ITT SBJ', 'Abw. GANZ', 'Abw. je Spieler']
for j, sp in enumerate(FW_KOPF, 1):
    c = sw.cell(row=3, column=j, value=sp)
    c.font = f_bold
    c.fill = fill_kopf if sp else PatternFill()
    c.border = rand if sp else Border()
    sw.column_dimensions[get_column_letter(j)].width = 13
sw.column_dimensions['A'].width = 9
FW_ERSTE, FW_LETZTE = 4, 3 + len(codes)


def fw_col(name):
    return get_column_letter(FW_KOPF.index(name) + 1)


def fw_rng(name):
    col = fw_col(name)
    return "Formelwerte!$%s$%d:$%s$%d" % (col, FW_ERSTE, col, FW_LETZTE)


def best_formel(i, zeit, test, seite, art):
    """Bestwert (MIN bei Zeiten, MAX beim Standweitsprung) der gültigen Versuche eines Spielers, sonst leer (S04 Regel 1 und 2)."""
    krit = '%s,$A%d,%s,"%s",%s,"%s",%s,1' % (VD['A'], i, VD['B'], zeit, VD['C'], test, VD['O'])
    if seite:
        krit += ',%s,"%s"' % (VD['D'], seite)
    fn = 'MAXIFS' if art == 'max' else 'MINIFS'
    return '=IF(COUNTIFS(%s)=0,"",%s(%s,%s))' % (krit, fn, VD['F'], krit)


def k_formel(i, zeit, test):
    return '=COUNTIFS(%s,$A%d,%s,"%s",%s,"%s",%s,1)' % (VD['A'], i, VD['B'], zeit, VD['C'], test, VD['O'])


def interp(i, kr_col):
    lo = 'INDEX(%s,MATCH($H%d,%s,0))' % (KO[kr_col], i, KO['A'])
    hi = 'INDEX(%s,MATCH($H%d+0.5,%s,0))' % (KO[kr_col], i, KO['A'])
    return '=IF($I%d=0,%s,(1-$I%d)*%s+$I%d*%s)' % (i, lo, i, lo, i, hi)


def abw(i, fw_name, ana_col):
    a = '%s%d' % (fw_col(fw_name), i)
    b = 'Analysedaten!%s%d' % (ana_col, i)
    return '=IF(AND(%s="",%s=""),0,IF(OR(%s="",%s=""),1,IF(ABS(%s-%s)<=0.000000001*MAX(1,ABS(%s)),0,1)))' % (a, b, a, b, a, b, b)


for i, c in enumerate(codes, FW_ERSTE):
    p = pers_v[c]
    pr = 'MATCH($A%d,%s,0)' % (i, PD['A'])
    vals = {
        'Code': c, 'Gruppe': gruppe[c], 'Verein': p['Verein'], 'G (IG = 1)': 1 if gruppe[c] == 'IG' else 0,
        'S_in (S05 R2)': '=IF(ISNUMBER(INDEX(%s,%s)),INDEX(%s,%s)/2.54,"")' % (PD['E'], pr, PD['E'], pr),
        'W_lb (S05 R2)': '=IF(ISNUMBER(INDEX(%s,%s)),INDEX(%s,%s)/0.45359237,"")' % (PD['F'], pr, PD['F'], pr),
        'MP_in (S05 R3)': '=IF(AND(ISNUMBER(INDEX(%s,%s)),ISNUMBER(INDEX(%s,%s))),(INDEX(%s,%s)/2.54+INDEX(%s,%s)/2.54)/2,"")' % (PD['G'], pr, PD['H'], pr, PD['G'], pr, PD['H'], pr),
        'a_lo (S05 R6)': '=INT(2*INDEX(%s,%s))/2' % (PD['D'], pr),
        'w (S05 R6)': '=(INDEX(%s,%s)-H%d)/0.5' % (PD['D'], pr, i),
        'β0 interp.': interp(i, 'B'), 'β1 interp.': interp(i, 'C'), 'β2 interp.': interp(i, 'D'), 'β3 interp.': interp(i, 'E'),
        'PAS_in (S05 R7)': '=IF(AND(ISNUMBER(E%d),ISNUMBER(F%d),ISNUMBER(G%d),INDEX(%s,%s)>=4,INDEX(%s,%s)<=17.5),J%d+K%d*E%d+L%d*F%d+M%d*G%d,"")' % (i, i, i, PD['D'], pr, PD['D'], pr, i, i, i, i, i, i, i),
        '%PAH (S05 R8)': '=IF(ISNUMBER(N%d),100*E%d/N%d,"")' % (i, i, i),
        'k Z30 prä': k_formel(i, 'prä', 'Sprint_30m'),
        'BEST Z30 prä': best_formel(i, 'prä', 'Sprint_30m', None, 'min'),
        'k Z30 post': k_formel(i, 'post', 'Sprint_30m'),
        'BEST Z30 post': best_formel(i, 'post', 'Sprint_30m', None, 'min'),
        'BEST CL prä': best_formel(i, 'prä', 'COD_505', 'L', 'min'),
        'BEST CR prä': best_formel(i, 'prä', 'COD_505', 'R', 'min'),
        'BEST CM prä (S04 R4)': '=IF(AND(ISNUMBER(T%d),ISNUMBER(U%d)),(T%d+U%d)/2,"")' % (i, i, i, i),
        'BEST CL post': best_formel(i, 'post', 'COD_505', 'L', 'min'),
        'BEST CR post': best_formel(i, 'post', 'COD_505', 'R', 'min'),
        'BEST CM post': '=IF(AND(ISNUMBER(W%d),ISNUMBER(X%d)),(W%d+X%d)/2,"")' % (i, i, i, i),
        'BEST SBJ prä': best_formel(i, 'prä', 'Standweitsprung', None, 'max'),
        'BEST SBJ post': best_formel(i, 'post', 'Standweitsprung', None, 'max'),
        'ITT Z30 (S08 R1)': '=IF(AND(ISNUMBER(Q%d),ISNUMBER(S%d),ISNUMBER(O%d)),1,0)' % (i, i, i),
        'ITT CM': '=IF(AND(ISNUMBER(V%d),ISNUMBER(Y%d),ISNUMBER(O%d)),1,0)' % (i, i, i),
        'ITT SBJ': '=IF(AND(ISNUMBER(Z%d),ISNUMBER(AA%d),ISNUMBER(O%d)),1,0)' % (i, i, i),
        'GANZ (S07 R1)': '=IF(D%d=0,"",IF(COUNTIF(%s,$A%d)=0,"",COUNTIFS(%s,$A%d,%s,1)))' % (i, ZU['B'], i, FA['M'], i, FA['F']),
        'Rang im ITT Z30': '=IF(AB%d=1,COUNTIF($AB$%d:AB%d,1),"")' % (i, FW_ERSTE, i),
        'Abw. %PAH': abw(i, '%PAH (S05 R8)', 'E'), 'Abw. BEST Z30 prä': abw(i, 'BEST Z30 prä', 'F'), 'Abw. BEST Z30 post': abw(i, 'BEST Z30 post', 'G'),
        'Abw. BEST CM prä': abw(i, 'BEST CM prä (S04 R4)', 'H'), 'Abw. BEST CM post': abw(i, 'BEST CM post', 'I'),
        'Abw. BEST SBJ prä': abw(i, 'BEST SBJ prä', 'J'), 'Abw. BEST SBJ post': abw(i, 'BEST SBJ post', 'K'),
        'Abw. ITT Z30': abw(i, 'ITT Z30 (S08 R1)', 'L'), 'Abw. ITT CM': abw(i, 'ITT CM', 'M'), 'Abw. ITT SBJ': abw(i, 'ITT SBJ', 'N'),
        'Abw. GANZ': abw(i, 'GANZ (S07 R1)', 'O'),
        'Abw. je Spieler': '=SUM(AH%d:AR%d)' % (i, i),
    }
    for j, sp in enumerate(FW_KOPF, 1):
        if sp == '':
            continue
        v = vals[sp]
        cell = sw.cell(row=i, column=j, value=v)
        cell.font = f_blau if isinstance(v, str) and v.startswith('=') else f_norm
sw.freeze_panes = 'B4'
# Spaltenprüfung der Zuordnung der Vergleichsspalten (Skriptprüfung, kein Wert)
assert fw_col('Abw. %PAH') == 'AH' and fw_col('Abw. GANZ') == 'AR' and fw_col('ITT Z30 (S08 R1)') == 'AB' and fw_col('Rang im ITT Z30') == 'AF'
assert fw_col('%PAH (S05 R8)') == 'O' and fw_col('BEST Z30 prä') == 'Q' and fw_col('BEST Z30 post') == 'S' and fw_col('GANZ (S07 R1)') == 'AE'
FW_SUMME_ZEILE = FW_LETZTE + 2
col_sum = FW_KOPF.index('Abw. je Spieler') + 1
sw.cell(row=FW_SUMME_ZEILE, column=col_sum, value='=SUM(%s)' % fw_rng('Abw. je Spieler')).font = f_blau
sw.cell(row=FW_SUMME_ZEILE, column=1, value='Summe der Abweichungen gegen die berichtete Rechnung (Spalte %s):' % get_column_letter(col_sum)).font = f_bold

# ---------------------------------------------------------------- Hilfsblatt TE Z30 prä: gültige Versuche je Spieler (Formeln)
st = wb.create_sheet('TE_Z30_prae')
st.cell(row=1, column=1, value='Gültige Versuche 30 m prä je Spieler (Formeln aus dem Blatt Versuchsdaten: Test Sprint_30m, Zeitpunkt prä, gültig = 1, S02). Leer = kein gültiger Versuch. k, Quadratsumme der Abweichungen vom Spielermittel und k − 1 nach S10 Regel 1 (nur Spieler mit k ≥ 2). Für die Kennwerte Nr. 15 und 16.').font = f_norm
for j, sp in enumerate(['Code', 'V1', 'V2', 'V3', 'k', 'SS_i = DEVSQ', 'k − 1'], 1):
    c = st.cell(row=2, column=j, value=sp)
    c.font = f_bold
    c.fill = fill_kopf
    c.border = rand
    st.column_dimensions[get_column_letter(j)].width = 18
TE_ERSTE, TE_LETZTE = 3, 2 + len(codes)
for i, c in enumerate(codes, TE_ERSTE):
    st.cell(row=i, column=1, value=c).font = f_norm
    for j in (1, 2, 3):
        krit = '%s,$A%d,%s,"prä",%s,"Sprint_30m",%s,%d,%s,1' % (VD['A'], i, VD['B'], VD['C'], VD['E'], j, VD['O'])
        st.cell(row=i, column=1 + j, value='=IF(COUNTIFS(%s)=1,SUMIFS(%s,%s),"")' % (krit, VD['F'], krit)).font = f_blau
    st.cell(row=i, column=5, value='=COUNT(B%d:D%d)' % (i, i)).font = f_blau
    st.cell(row=i, column=6, value='=IF(E%d>=2,DEVSQ(B%d:D%d),"")' % (i, i, i)).font = f_blau
    st.cell(row=i, column=7, value='=IF(E%d>=2,E%d-1,"")' % (i, i)).font = f_blau
TE_SS = 'TE_Z30_prae!$F$%d:$F$%d' % (TE_ERSTE, TE_LETZTE)
TE_DF = 'TE_Z30_prae!$G$%d:$G$%d' % (TE_ERSTE, TE_LETZTE)

# ---------------------------------------------------------------- Auswahl der Beispielspieler (wie Fassung 1)
def k_pre(c, z):
    return sum(1 for r in V if r['Code'] == c and r['Zeitpunkt'] == 'prä' and r['Test'] == {'Z30': 'Sprint_30m'}[z] and r['Wert'] != '' and r['ungültig'] == '')


sp3 = next(c for c in codes if k_pre(c, 'Z30') == 3)
spcm = next(c for c in codes if R['S04.BEST.CM.PRE.P%s.X' % c]['Wert'] != '')
sppah = next(c for c in codes if R['S05.PAH.PAH.PRE.P%s.X' % c]['Wert'] != '' and (float(pers_v[c]['Alter_prae']) * 2) % 1 != 0)
spfb = next(z['Analysecode'] for z in ZUO if z['Listenlabel'] == 'HL-01')
h010_von = {z['Analysecode']: i + 1 for i, z in enumerate(ZUO) if z['Analysecode']}   # Listenplatz = Zeile der Zuordnung (HL-01 = 1)
kr_lo = math.floor(2 * float(pers_v[sppah]['Alter_prae'])) / 2

# ---------------------------------------------------------------- ANCOVA-Block Z30 (ITT-Set in Blockform, LINEST)
# Blockgröße aus der Zahl der ITT-Spieler der berichteten Rechnung (nur zur Dimensionierung, geprüft durch Z3)
N_ITT = int(wert(R, 'S08.N.Z30.X.ITTIG.X') + wert(R, 'S08.N.Z30.X.ITTKG.X'))
sb = wb.create_sheet('ANCOVA_Z30')
sb.cell(row=1, column=1, value='ITT-Set 30 m in Blockform: Zeile j holt über den Rang aus dem Blatt Formelwerte den j-ten Spieler mit ITT Z30 = 1. Modell S13: Post = b0 + b1·G + b2·Prä + b3·%PAH, geschätzt mit LINEST (Kleinste Quadrate). LINEST gibt die Koeffizienten in umgekehrter Reihenfolge der x-Spalten aus, b1 (Gruppe) steht in Zeile 1, Spalte 3, sein Standardfehler in Zeile 2, Spalte 3. Blockgröße = Zahl der ITT-Spieler, geprüft in Zusatzprüfung Z3.').font = f_norm
for j, sp in enumerate(['j', 'Code', 'G', 'Prä (BEST Z30)', '%PAH', 'Post (BEST Z30)', 'Prä IG', 'Prä KG', 'Post IG', 'Post KG'], 1):
    c = sb.cell(row=2, column=j, value=sp)
    c.font = f_bold
    c.fill = fill_kopf
    c.border = rand
    sb.column_dimensions[get_column_letter(j)].width = 16
B_ERSTE, B_LETZTE = 3, 2 + N_ITT
for j in range(1, N_ITT + 1):
    i = B_ERSTE + j - 1
    sb.cell(row=i, column=1, value=j).font = f_norm
    sb.cell(row=i, column=2, value='=INDEX(%s,MATCH(A%d,%s,0))' % (fw_rng('Code'), i, fw_rng('Rang im ITT Z30'))).font = f_blau
    for col, name in ((3, 'G (IG = 1)'), (4, 'BEST Z30 prä'), (5, '%PAH (S05 R8)'), (6, 'BEST Z30 post')):
        sb.cell(row=i, column=col, value='=INDEX(%s,MATCH($B%d,%s,0))' % (fw_rng(name), i, fw_rng('Code'))).font = f_blau
    sb.cell(row=i, column=7, value='=IF(C%d=1,D%d,"")' % (i, i)).font = f_blau
    sb.cell(row=i, column=8, value='=IF(C%d=0,D%d,"")' % (i, i)).font = f_blau
    sb.cell(row=i, column=9, value='=IF(C%d=1,F%d,"")' % (i, i)).font = f_blau
    sb.cell(row=i, column=10, value='=IF(C%d=0,F%d,"")' % (i, i)).font = f_blau
BY = 'ANCOVA_Z30!$F$%d:$F$%d' % (B_ERSTE, B_LETZTE)
BX = 'ANCOVA_Z30!$C$%d:$E$%d' % (B_ERSTE, B_LETZTE)
BG = 'ANCOVA_Z30!$C$%d:$C$%d' % (B_ERSTE, B_LETZTE)
B_PRE_IG = 'ANCOVA_Z30!$G$%d:$G$%d' % (B_ERSTE, B_LETZTE)
B_PRE_KG = 'ANCOVA_Z30!$H$%d:$H$%d' % (B_ERSTE, B_LETZTE)
B_POST_IG = 'ANCOVA_Z30!$I$%d:$I$%d' % (B_ERSTE, B_LETZTE)
B_POST_KG = 'ANCOVA_Z30!$J$%d:$J$%d' % (B_ERSTE, B_LETZTE)
# Kennwerte des Blocks
kz = B_LETZTE + 2
sb.cell(row=kz, column=1, value='Kennwerte des Blocks (Formeln)').font = f_bold
block_k = [
    ('n_IG', '=COUNTIF(%s,1)' % BG), ('n_KG', '=COUNTIF(%s,0)' % BG), ('N', '=B%d+B%d' % (kz + 1, kz + 2)),
    ('df = N − 4', '=B%d-4' % (kz + 3)),
    ('b1 (LINEST Zeile 1, Spalte 3)', '=INDEX(LINEST(%s,%s,TRUE,TRUE),1,3)' % (BY, BX)),
    ('SE(b1) (LINEST Zeile 2, Spalte 3)', '=INDEX(LINEST(%s,%s,TRUE,TRUE),2,3)' % (BY, BX)),
    ('Prüfung: Zahl der Spieler mit ITT Z30 = 1 im Blatt Formelwerte', '=COUNTIF(%s,1)' % fw_rng('ITT Z30 (S08 R1)')),
]
for q, (bez, f) in enumerate(block_k, 1):
    sb.cell(row=kz + q, column=1, value=bez).font = f_norm
    sb.cell(row=kz + q, column=2, value=f).font = f_blau
sb.column_dimensions['A'].width = 52
BK = {'nIG': 'ANCOVA_Z30!$B$%d' % (kz + 1), 'nKG': 'ANCOVA_Z30!$B$%d' % (kz + 2), 'N': 'ANCOVA_Z30!$B$%d' % (kz + 3),
      'df': 'ANCOVA_Z30!$B$%d' % (kz + 4), 'b1': 'ANCOVA_Z30!$B$%d' % (kz + 5), 'se': 'ANCOVA_Z30!$B$%d' % (kz + 6),
      'nITT_formel': 'ANCOVA_Z30!$B$%d' % (kz + 7)}

# ---------------------------------------------------------------- Handprobe
sh = wb.create_sheet('Handprobe', 1)
sh.cell(row=1, column=1, value='Handprobe Phase 6.3 als Excel-Formelprobe — Kennwerte, Sollwerte beider Implementierungen, Formelwert (Excel)').font = f_h
sh.cell(row=2, column=1, value='Gelbe Zellen tragen Excel-Formeln aus den Eingangsblättern (dritte Implementierung). Toleranz: Anzahlen exakt, übrige relativ 1e-6. Spalte „Wert R“ ist die berichtete Rechnung, „Wert Python“ die Gegenprobe (beide aus den Ergebnisdateien vom 25.09.2026).').font = f_norm
sh.cell(row=4, column=1, value='Ergebnis der Handprobe (Verfasser, Datum):').font = f_bold
sh.cell(row=4, column=2).fill = fill_hand
kopf = ['Nr.', 'Kennung', 'Beschreibung', 'Rechenweg (Regel der Spezifikation) und Formel', 'Eingang (Blatt, Auswahl)', 'Wert R', 'Wert Python', 'Handwert (Formel)', 'Abweichung Hand − R', 'Toleranz', 'Urteil']
for j, sp in enumerate(kopf, 1):
    c = sh.cell(row=6, column=j, value=sp)
    c.font = f_bold
    c.fill = fill_kopf
    c.border = rand
    c.alignment = wrap
for j, w in enumerate([5, 34, 34, 60, 40, 20, 20, 20, 16, 10, 12], 1):
    sh.column_dimensions[get_column_letter(j)].width = w
sh.freeze_panes = 'A7'

# Eingang aus der Ergebnisdatei für Kennwert Nr. 34 (vorab festgelegter Rechenweg)
sh.cell(row=6, column=13, value='Eingang aus der Ergebnisdatei nur für Nr. 34 (Rechenweg vorab festgelegt)').font = f_bold
eing34 = [('S13.P.CM.X.ITT.HAUPT', 'p 505-Seitenmittel'), ('S13.B1.CM.X.ITT.HAUPT', 'b1 505-Seitenmittel'),
          ('S13.P.SBJ.X.ITT.HAUPT', 'p Standweitsprung'), ('S13.B1.SBJ.X.ITT.HAUPT', 'b1 Standweitsprung')]
E34 = {}
for q, (k, bez) in enumerate(eing34, 7):
    sh.cell(row=q, column=13, value=k).font = f_norm
    sh.cell(row=q, column=14, value=bez).font = f_norm
    sh.cell(row=q, column=15, value=wert(R, k)).font = f_gruen
    E34[k] = '$O$%d' % q
sh.column_dimensions['M'].width = 26
sh.column_dimensions['N'].width = 22
sh.column_dimensions['O'].width = 18

ZEILE0 = 7
def z(n):
    """Zellbezug der Handwert-Zelle (Spalte H) von Kennwert Nr. n."""
    return '$H$%d' % (ZEILE0 + n - 1)


posten = []   # (Kennung, Beschreibung, Rechenweg, Eingang, exakt?, Formel)
posten.append(('S02.NGUELT.Z30.PRE.ALL.X', 'Zahl gültiger Versuche 30 m prä, alle Spieler',
    'S02 Regel 1 bis 3: Zeilen mit Test Sprint_30m, Zeitpunkt prä und gültig = 1 zählen (Spalte O des Blatts Versuchsdaten, mit Auslöseprüfung).',
    'Versuchsdaten', True,
    '=COUNTIFS(%s,"Sprint_30m",%s,"prä",%s,1)' % (VD['C'], VD['B'], VD['O'])))
posten.append(('S03.NKAT.Z30.POST.KG.TECH', 'Ungültige Zeilen 30 m post der KG, Kategorie TECH',
    'S03 Regel 1 bis 3 mit Vokabular: Zeilen mit Test Sprint_30m, Zeitpunkt post, Gruppe KG und Kategorie TECH zählen (Spalte Q des Blatts Versuchsdaten: NANG vor AUSL vor Vokabular).',
    'Versuchsdaten (Hilfsspalten I und Q)', True,
    '=COUNTIFS(%s,"Sprint_30m",%s,"post",%s,"KG",%s,"TECH")' % (VD['C'], VD['B'], VD['I'], VD['Q'])))
posten.append(('S04.K.Z30.PRE.P%s.X' % sp3, 'Zahl gültiger Versuche 30 m prä, Spieler %s' % sp3,
    'S04 Regel 1: gültige Versuche des Spielers zählen.', 'Versuchsdaten, Code %s' % sp3, True,
    '=COUNTIFS(%s,"%s",%s,"prä",%s,"Sprint_30m",%s,1)' % (VD['A'], sp3, VD['B'], VD['C'], VD['O'])))
posten.append(('S04.BEST.Z30.PRE.P%s.X' % sp3, 'Bestwert 30 m prä, Spieler %s' % sp3,
    'S04 Regel 2: Minimum der gültigen Werte (Zeit). MINIFS über die gültigen Zeilen des Spielers.', 'Versuchsdaten, Code %s' % sp3, False,
    '=MINIFS(%s,%s,"%s",%s,"prä",%s,"Sprint_30m",%s,1)' % (VD['F'], VD['A'], sp3, VD['B'], VD['C'], VD['O'])))
posten.append(('S04.MEAN.Z30.PRE.P%s.X' % sp3, 'Mittelwert 30 m prä, Spieler %s' % sp3,
    'S04 Regel 3: arithmetisches Mittel der gültigen Werte. AVERAGEIFS über die gültigen Zeilen des Spielers.', 'Versuchsdaten, Code %s' % sp3, False,
    '=AVERAGEIFS(%s,%s,"%s",%s,"prä",%s,"Sprint_30m",%s,1)' % (VD['F'], VD['A'], sp3, VD['B'], VD['C'], VD['O'])))
posten.append(('S04.BEST.CM.PRE.P%s.X' % spcm, '505-Seitenmittel prä, Spieler %s' % spcm,
    'S04 Regel 4: Bestwert (Minimum) je Seite L und R aus den gültigen Versuchen, dann Mittel der beiden Seiten-Bestwerte, nur wenn beide Seiten einen gültigen Versuch haben (Blatt Formelwerte, Spalten T, U, V).',
    'Versuchsdaten, Code %s, Test COD_505' % spcm, False,
    '=INDEX(%s,MATCH("%s",%s,0))' % (fw_rng('BEST CM prä (S04 R4)'), spcm, fw_rng('Code'))))
posten.append(('S05.MP.PAH.PRE.P%s.X' % sppah, 'Mittlere Elterngröße in Zoll, Spieler %s' % sppah,
    'S05 Regel 2 und 3: (Groesse_Mutter/2,54 + Groesse_Vater/2,54)/2 (Blatt Formelwerte, Spalte G).', 'Personendaten, Code %s' % sppah, False,
    '=INDEX(%s,MATCH("%s",%s,0))' % (fw_rng('MP_in (S05 R3)'), sppah, fw_rng('Code'))))
posten.append(('S05.PAS.PAH.PRE.P%s.X' % sppah, 'Vorhergesagte Erwachsenengröße in Zoll, Spieler %s' % sppah,
    'S05 Regel 6 und 7: a_lo = %.1f, a_hi = %.1f, w = (Alter − a_lo)/0,5. Jeden Koeffizienten linear interpolieren: c = (1 − w)·c(a_lo) + w·c(a_hi). PAS = β0 + β1·Körperhöhe/2,54 + β2·Körpermasse/0,45359237 + β3·MP (Blatt Formelwerte, Spalten H bis N).' % (kr_lo, kr_lo + 0.5),
    'Personendaten, Code %s, Koeffizienten_KR Zeilen %.1f und %.1f' % (sppah, kr_lo, kr_lo + 0.5), False,
    '=INDEX(%s,MATCH("%s",%s,0))' % (fw_rng('PAS_in (S05 R7)'), sppah, fw_rng('Code'))))
posten.append(('S05.PAH.PAH.PRE.P%s.X' % sppah, '%%PAH, Spieler %s' % sppah,
    'S05 Regel 8: 100 · (Körperhöhe/2,54) / PAS (Blatt Formelwerte, Spalte O).', 'Personendaten, Code %s' % sppah, False,
    '=INDEX(%s,MATCH("%s",%s,0))' % (fw_rng('%PAH (S05 R8)'), sppah, fw_rng('Code'))))
posten.append(('S06.NMELD.FB.X.P%s.X' % spfb, 'Zahl der Meldungen, Spieler %s (Listenplatz H010 = %d)' % (spfb, h010_von[spfb]),
    'S06 Regel 1 bis 3: Listenlabel aus H010 mit den Fallkorrekturen (CASE 59, 70, 140, 158, 165, 190, 206), Analysecode aus der Zuordnung (Blatt Fragebogen_A, Spalten L und M), Meldungen des Analysecodes zählen.',
    'Fragebogen_A, Zuordnung', True,
    '=COUNTIF(%s,"%s")' % (FA['M'], spfb)))
posten.append(('S07.ADH.ADH.X.P%s.GANZ' % spfb, 'Adhärenz GANZ, Spieler %s' % spfb,
    'S07 Regel 1: Meldungen des Analysecodes mit H004 = 1 zählen.', 'Fragebogen_A', True,
    '=COUNTIFS(%s,"%s",%s,1)' % (FA['M'], spfb, FA['F'])))
posten.append(('S07.SUMME.ADH.X.IG.GANZ', 'Summe der Meldungen „ganz“ über alle IG-Spieler',
    'S07 Regel 5 und 6: Summe der Zählung GANZ über die zugeteilten Spieler, Spieler ohne Meldung mit 0, Spieler ohne Listenplatz in der Summe mit 0 (Blatt Formelwerte, Spalte AE). Jede Meldung zählt (K7).',
    'Fragebogen_A über Formelwerte', True,
    '=SUM(%s)' % fw_rng('GANZ (S07 R1)')))
posten.append(('S07.RATE.ADH.X.IG.GANZ', 'Umsetzungsrate GANZ',
    'S07 Regel 6: Summe / (12 · Zahl der zugeteilten IG-Spieler der Personendaten).', 'Kennwert Nr. 12, Personendaten', False,
    '=%s/(12*COUNTIF(%s,"IG"))' % (z(12), PD['C'])))
posten.append(('S08.N.Z30.X.ITTIG.X', 'Zahl der IG-Spieler im ITT-Set 30 m',
    'S08 Regel 1: IG-Spieler mit BEST prä, BEST post und %PAH zählen (Blatt Formelwerte, Spalten D und AB).', 'Formelwerte', True,
    '=COUNTIFS(%s,1,%s,1)' % (fw_rng('G (IG = 1)'), fw_rng('ITT Z30 (S08 R1)'))))
posten.append(('S10.TE.Z30.PRE.ALL.X', 'Typischer Messfehler 30 m prä',
    'S10 Regel 1: je Spieler mit k ≥ 2 die Quadratsumme der Abweichungen vom Spielermittel (DEVSQ), Summe über Spieler geteilt durch Σ(k − 1), Wurzel (Blatt TE_Z30_prae).',
    'TE_Z30_prae', False,
    '=SQRT(SUM(%s)/SUM(%s))' % (TE_SS, TE_DF)))
posten.append(('S10.DFTE.Z30.PRE.ALL.X', 'Freiheitsgrade des TE 30 m prä', 'S10 Regel 1: Σ(k_i − 1) über Spieler mit k ≥ 2.', 'TE_Z30_prae', True,
    '=SUM(%s)' % TE_DF))
posten.append(('S10.SB.Z30.PRE.ALL.X', 'Zwischen-Athleten-SD der Bestwerte 30 m prä',
    'S10 Regel 5: STDEV.S über BEST Z30 prä aller Spieler mit Wert (beide Gruppen, Blatt Formelwerte, Spalte Q).', 'Formelwerte, Spalte BEST Z30 prä', False,
    '=STDEV.S(%s)' % fw_rng('BEST Z30 prä')))
posten.append(('S10.SESOI.Z30.PRE.ALL.X', 'SESOI 30 m', 'S10 Regel 6: 0,2 · S.', 'Kennwert Nr. 17', False,
    '=0.2*%s' % z(17)))
posten.append(('S12.M.Z30.PRE.ITTIG.HAUPT', 'Mittel BEST 30 m prä, IG im ITT-Set',
    'S12 Regel 4: AVERAGE über die Prä-Werte der IG-Spieler des ITT-Sets (Blatt ANCOVA_Z30, Spalte G).', 'ANCOVA_Z30', False,
    '=AVERAGE(%s)' % B_PRE_IG))
posten.append(('S12.SD.Z30.PRE.ITTIG.HAUPT', 'SD BEST 30 m prä, IG im ITT-Set',
    'S12 Regel 4: STDEV.S über dieselben Spieler.', 'ANCOVA_Z30', False,
    '=STDEV.S(%s)' % B_PRE_IG))
posten.append(('S15.UD.Z30.X.ITT.HAUPT', 'Unadjustierte Differenz der Post-Mittel 30 m (IG − KG), ITT-Set',
    'S15 Regel 4: Mittel BEST Z30 post der IG minus Mittel der KG, jeweils im ITT-Set (Blatt ANCOVA_Z30, Spalten I und J).', 'ANCOVA_Z30', False,
    '=AVERAGE(%s)-AVERAGE(%s)' % (B_POST_IG, B_POST_KG)))
posten.append(('S15.SDPOST.Z30.X.ITT.HAUPT', 'Gepoolte Post-SD 30 m, ITT-Set',
    '0.5 Nr. 2: √(((n_IG − 1)·s_IG² + (n_KG − 1)·s_KG²)/(n_IG + n_KG − 2)) mit VAR.S je Gruppe.', 'ANCOVA_Z30', False,
    '=SQRT(((%s-1)*VAR.S(%s)+(%s-1)*VAR.S(%s))/(%s-2))' % (BK['nIG'], B_POST_IG, BK['nKG'], B_POST_KG, BK['N'])))
posten.append(('S15.UDT.Z30.X.ITT.HAUPT', 't der unadjustierten Differenz',
    'S15 Regel 4: UD / (SD_pool · √(1/n_IG + 1/n_KG)).', 'Kennwerte Nr. 21 und 22', False,
    '=%s/(%s*SQRT(1/%s+1/%s))' % (z(21), z(22), BK['nIG'], BK['nKG'])))
posten.append(('S15.UDP.Z30.X.ITT.HAUPT', 'p der unadjustierten Differenz',
    'S15 Regel 4: zweiseitig, df = n − 2. Excel: T.DIST.2T(ABS(t), df).', 'Kennwert Nr. 23', False,
    '=T.DIST.2T(ABS(%s),%s-2)' % (z(23), BK['N'])))
posten.append(('S13.B1.Z30.X.ITT.HAUPT', 'Adjustierte Differenz b1 (ANCOVA 30 m, ITT)',
    'S13 Modell Post = b0 + b1·G + b2·Prä + b3·PAH. Excel: INDEX(LINEST(Post-Bereich, [G, Prä, PAH]-Bereich, WAHR, WAHR), 1, 3). LINEST gibt die Koeffizienten in umgekehrter Reihenfolge der x-Spalten aus, b1 steht in Zeile 1, Spalte 3 (Blatt ANCOVA_Z30).',
    'ANCOVA_Z30 (ITT-Set aus Formelwerte)', False,
    '=%s' % BK['b1']))
posten.append(('S13.SEB1.Z30.X.ITT.HAUPT', 'Standardfehler von b1', 'S13 Regel 1: zweite Zeile von LINEST, dieselbe Spalte wie b1.', 'ANCOVA_Z30', False,
    '=%s' % BK['se']))
posten.append(('S13.DF.Z30.X.ITT.HAUPT', 'Residualfreiheitsgrade', 'S13 Regel 1: n − 4.', 'ANCOVA_Z30', True,
    '=%s-4' % BK['N']))
posten.append(('S13.P.Z30.X.ITT.HAUPT', 'p von b1, zweiseitig', 'S13 Regel 2: t = b1/SE, p = T.DIST.2T(ABS(t), df).', 'Kennwerte Nr. 25 bis 27', False,
    '=T.DIST.2T(ABS(%s/%s),%s)' % (z(25), z(26), z(27))))
posten.append(('S13.KIU.Z30.X.ITT.HAUPT', 'Untere KI-Grenze von b1', 'S13 Regel 2: b1 − T.INV.2T(0,05, df) · SE.', 'Kennwerte Nr. 25 bis 27', False,
    '=%s-T.INV.2T(0.05,%s)*%s' % (z(25), z(27), z(26))))
posten.append(('S15.SDPRE.Z30.X.ITT.HAUPT', 'Gepoolte Prä-SD des ITT-Sets 30 m', 'S15 Regel 1: wie Nr. 22, mit den BEST prä (Blatt ANCOVA_Z30, Spalten G und H).', 'ANCOVA_Z30', False,
    '=SQRT(((%s-1)*VAR.S(%s)+(%s-1)*VAR.S(%s))/(%s-2))' % (BK['nIG'], B_PRE_IG, BK['nKG'], B_PRE_KG, BK['N'])))
posten.append(('S15.J.Z30.X.ITT.HAUPT', 'Korrekturfaktor J', 'S15 Regel 2: 1 − 3/(4·(n_IG + n_KG − 2) − 1).', 'ANCOVA_Z30', False,
    '=1-3/(4*(%s-2)-1)' % BK['N']))
posten.append(('S15.G.Z30.X.ITT.HAUPT', 'Hedges’ g', 'S15 Regel 3: b1 / SD_prä · J.', 'Kennwerte Nr. 25, 30, 31', False,
    '=%s/%s*%s' % (z(25), z(30), z(31))))
posten.append(('S18.FCRIT.Z30.X.ITT.X', 'Kritischer F-Wert der Poweranalyse 30 m',
    'S18 Regel 3: F_1,df2(0,95) mit df2 = N − 4. Excel: F.INV.RT(0,05, 1, df2).', 'ANCOVA_Z30 (N = n_IG + n_KG des ITT-Sets)', False,
    '=F.INV.RT(0.05,1,%s-4)' % BK['N']))
posten.append(('S13.H0REJ.X.X.ITT.HAUPT', 'Merkmal H0 abgelehnt',
    'S13 Entscheidungsregel: 1, wenn für mindestens eine der drei Zielgrößen p < 0,05 und b1 in günstiger Richtung (Zeiten negativ, Sprung positiv), sonst 0. Für 30 m aus den Kennwerten Nr. 25 und 28, für CM und SBJ aus der Tabelle „Eingang aus der Ergebnisdatei“ (Spalten M bis O), wie vorab festgelegt.',
    'Kennwerte Nr. 25 und 28, Eingang aus der Ergebnisdatei', True,
    '=IF(OR(AND(%s<0.05,%s<0),AND(%s<0.05,%s<0),AND(%s<0.05,%s>0)),1,0)' % (
        z(28), z(25), E34['S13.P.CM.X.ITT.HAUPT'], E34['S13.B1.CM.X.ITT.HAUPT'], E34['S13.P.SBJ.X.ITT.HAUPT'], E34['S13.B1.SBJ.X.ITT.HAUPT'])))
assert len(posten) == 34

zeile = ZEILE0
for i, (k, beschr, weg, eing, exakt, formel) in enumerate(posten, 1):
    vr, vp = wert(R, k), wert(PY, k)
    vals = [i, k, beschr, weg, eing, vr, vp, None, None, 0 if exakt else 1e-6, None]
    for j, v in enumerate(vals, 1):
        c = sh.cell(row=zeile, column=j, value=v)
        c.font = f_norm
        c.border = rand
        c.alignment = wrap
        if i % 2 == 0:
            c.fill = fill_zebra
    sh.cell(row=zeile, column=6).font = f_gruen
    sh.cell(row=zeile, column=7).font = f_gruen
    hz = sh.cell(row=zeile, column=8, value=formel)
    hz.fill = fill_hand
    hz.font = f_blau
    sh.cell(row=zeile, column=9, value='=IF(H%d="","",IFERROR(H%d-F%d,"FEHLER"))' % (zeile, zeile, zeile)).font = f_norm
    sh.cell(row=zeile, column=11, value='=IF(H%d="","offen",IFERROR(IF(ABS(H%d-F%d)<=J%d*MAX(1,ABS(F%d)),"stimmt","ABWEICHUNG"),"FEHLER"))' % (zeile, zeile, zeile, zeile, zeile)).font = f_norm
    zeile += 1
ZEILE_LETZTE = zeile - 1

# Zusatzprüfungen
zeile += 1
sh.cell(row=zeile, column=1, value='Zusatzprüfungen (Formeln, kein Kennwert der Liste)').font = f_bold
zeile += 1
zusatz = [
    ('Z1', 'Zahl auslösegestörter Sprintläufe prä und post (S02 Regel 2), Formel gegen berichtete Rechnung',
     '=COUNTIF(%s,1)/3' % VD['N'],
     wert(R, 'S02.NAUSL.X.PRE.ALL.X') + wert(R, 'S02.NAUSL.X.POST.ALL.X'), 'S02.NAUSL.X.PRE.ALL.X + S02.NAUSL.X.POST.ALL.X'),
    ('Z2', 'Zwischengrößen je Spieler (11 Größen × Spieler): Zahl der Zellen, in denen Formelwert und berichtete Rechnung abweichen (Blatt Formelwerte)',
     '=SUM(%s)' % fw_rng('Abw. je Spieler'), 0, 'Sollwert 0'),
    ('Z3', 'Blockgröße ANCOVA_Z30 = Zahl der Spieler mit ITT Z30 = 1 nach Formel',
     '=%s' % BK['nITT_formel'], N_ITT, 'Zeilen des Blocks'),
    ('Z4', 'Alle 34 Kennwerte mit Urteil „stimmt“',
     '=COUNTIF(K%d:K%d,"stimmt")' % (ZEILE0, ZEILE_LETZTE), 34, '34'),
]
for zk, bez, formel, soll, sollq in zusatz:
    sh.cell(row=zeile, column=1, value=zk).font = f_norm
    c = sh.cell(row=zeile, column=3, value=bez)
    c.font = f_norm
    c.alignment = wrap
    sh.cell(row=zeile, column=5, value=sollq).font = f_norm
    sh.cell(row=zeile, column=6, value=soll).font = f_gruen
    hz = sh.cell(row=zeile, column=8, value=formel)
    hz.fill = fill_hand
    hz.font = f_blau
    sh.cell(row=zeile, column=10, value=0).font = f_norm
    sh.cell(row=zeile, column=11, value='=IFERROR(IF(ABS(H%d-F%d)<=J%d,"stimmt","ABWEICHUNG"),"FEHLER")' % (zeile, zeile, zeile)).font = f_norm
    for j in range(1, 12):
        sh.cell(row=zeile, column=j).border = rand
    zeile += 1
zeile += 1
sh.cell(row=zeile, column=1, value='Quellen: Werte R aus Ergebnisse_R_2026-09-25.csv (SHA-256 3194a805…), Werte Python aus Ergebnisse_Python_2026-09-25.csv (SHA-256 2d4ce431…). Kennungen nach Spezifikation_2026-09-24_Kennungen.csv. Toleranzregel wie G.3 (deterministisch), für die Handprobe auf 1e-6 relativ gelockert, weil Excel andere Rechenwege nutzt. Fassung 2 vom 25.09.2026: Handwerte als Excel-Formeln (Verfasserentscheidung 25.09.2026, Register R12).').font = f_grau
sh.cell(row=zeile, column=1).alignment = wrap
sh.merge_cells(start_row=zeile, start_column=1, end_row=zeile, end_column=11)
sh.row_dimensions[zeile].height = 40
# Funktionen, die Excel erst nach 2007 kennt, tragen im Dateiformat den Namensraum _xlfn (sonst #NAME? beim Öffnen)
import re
NEUE_FUNKTIONEN = re.compile(r'(?<![A-Za-z_.])(MINIFS|MAXIFS|STDEV\.S|VAR\.S|T\.DIST\.2T|T\.INV\.2T|F\.INV\.RT)\(')
n_formeln = 0
for blatt in wb.worksheets:
    for zeile_zellen in blatt.iter_rows():
        for zelle in zeile_zellen:
            if isinstance(zelle.value, str) and zelle.value.startswith('='):
                n_formeln += 1
                zelle.value = NEUE_FUNKTIONEN.sub(r'_xlfn.\1(', zelle.value)
from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)   # Excel berechnet alle Formeln beim Öffnen, die Datei trägt keine gespeicherten Werte
wb.save(ZIEL)
print('geschrieben:', ZIEL, '· Kennwerte:', len(posten), '· Formeln:', n_formeln, '· Beispielspieler:', sp3, spcm, sppah, spfb, '· Blockgröße ANCOVA_Z30:', N_ITT)

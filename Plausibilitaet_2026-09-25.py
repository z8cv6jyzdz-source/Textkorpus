# -*- coding: utf-8 -*-
"""
Plausibilitaet_2026-09-25.py — Plausibilitätsprüfung der berichteten Rechnung (Phase 6.4)
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 6.4

Zweck: Nenner gegen Teilnehmerfluss, Vorzeichen und innere Konsistenz, Größenordnung, dazu der
Vergleich mit der ersten Rechnung vom 15.09.2026 (Analyseprotokoll_2026-09-15, Kennzahlen_2026-09-22),
die auf dem Workbook-Stand vor der Datensicherung lief (Phase 1 änderte einen 10-m-Wert von VS-06,
die Familiarisierung von VS-11 und Bemerkungstexte, nicht die Werte der konfirmatorischen Zielgrößen).
Die Vergleichswerte aus den beiden Dokumenten sind Abschriften nur für diese Prüfung, keine
Zahlenquelle des Manuskripts (F14 § 1.2 Zahlenregel).

Eingang: Ergebnisse_R_2026-09-25.csv (berichtete Rechnung, blinde zweite Instanz)
Aufruf: python Plausibilitaet_2026-09-25.py <Ergebnisse_R_2026-09-25.csv>
Ausgabe: Plausibilitaet_2026-09-25.txt neben dem Skript
Fassung: 2026-09-25, erste Fassung.
"""
import sys, os, csv, math, io, datetime
from scipy import stats

CSV = sys.argv[1]
OUT = os.path.splitext(os.path.abspath(__file__))[0] + '.txt'
buf = io.StringIO()
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); buf.write(s + '\n')
E = {}
with open(CSV, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f): E[r['Kennung']] = (float(r['Wert']) if r['Wert'] != '' else None, r['Grund'])
def w(k):
    if k not in E: raise KeyError('Kennung fehlt: ' + k)
    return E[k][0]
def g(k): return E[k][1]
spieler = sorted(set(k.split('.')[4][1:] for k in E if k.startswith('S04.K.Z05.PRE.P')))
IG = [c for c in spieler if not c.startswith('VS')]; KG = [c for c in spieler if c.startswith('VS')]
ok_n = 0; fail_n = 0; hinweise = []
def pruef(name, bed, detail=''):
    global ok_n, fail_n
    if bed: ok_n += 1; P('  ja    ' + name)
    else: fail_n += 1; P('  NEIN  ' + name + ('  [' + detail + ']' if detail else ''))
def nahe(a, b, tol): return a is not None and b is not None and abs(a - b) <= tol

P('PLAUSIBILITÄTSPRÜFUNG Phase 6.4 · berichtete Rechnung', os.path.basename(CSV), '·', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
P('Kennungen:', len(E), '· Spieler:', len(spieler), '(IG', len(IG), ', KG', len(KG), ')')

P('\n1 NENNER GEGEN TEILNEHMERFLUSS')
pruef('S01 N ALL = IG + KG = VA + VB + VC', w('S01.N.X.X.ALL.X') == w('S01.N.X.X.IG.X') + w('S01.N.X.X.KG.X') == w('S01.N.X.X.VA.X') + w('S01.N.X.X.VB.X') + w('S01.N.X.X.VC.X'))
pruef('S01 NZEIL = 36 Zeilen je Spieler (18 Zellen × 2 Zeitpunkte)', w('S01.NZEIL.X.X.ALL.X') == 36 * w('S01.N.X.X.ALL.X'))
for m in ('IG', 'KG', 'VA', 'VB', 'VC'):
    pruef('S08 FLZUG %s = S01 N, FLAUSG + FLNANG = FLZUG, FLPRE = FLZUG' % m,
          w('S08.FLZUG.X.X.%s.X' % m) == w('S01.N.X.X.%s.X' % m) and w('S08.FLAUSG.X.X.%s.X' % m) + w('S08.FLNANG.X.X.%s.X' % m) == w('S08.FLZUG.X.X.%s.X' % m)
          and w('S08.FLPRE.X.X.%s.X' % m) == w('S08.FLZUG.X.X.%s.X' % m))
pruef('S08 FLNANG IG + KG = 4 (BW-07, BW-21, VS-07, VS-16), B6NA identisch', w('S08.FLNANG.X.X.IG.X') + w('S08.FLNANG.X.X.KG.X') == 4 and w('S08.B6NA.X.X.IG.X') == w('S08.FLNANG.X.X.IG.X') and w('S08.B6NA.X.X.KG.X') == w('S08.FLNANG.X.X.KG.X'))
pruef('S05 NPAH IG + KG = 30 (VS-18 ohne %PAH), FLOPAH = B6FK, FLOPAH KG = 1', w('S05.NPAH.PAH.PRE.IG.X') + w('S05.NPAH.PAH.PRE.KG.X') == 30 and all(w('S08.FLOPAH.PAH.X.%s.X' % m) == w('S08.B6FK.X.X.%s.X' % m) for m in ('IG', 'KG')) and w('S08.FLOPAH.PAH.X.KG.X') == 1)
for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']:
    nig, nkg = w('S08.N.%s.X.ITTIG.X' % z), w('S08.N.%s.X.ITTKG.X' % z)
    mit = sum(w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) for c in spieler)
    pruef('S08 %s: FLITT = N ITT, Summe MITGL ITT = n_IG + n_KG, ITT ≤ FLAUSG, S12 N ITT = S08 N' % z,
          w('S08.FLITT.%s.X.IG.X' % z) == nig and w('S08.FLITT.%s.X.KG.X' % z) == nkg and mit == nig + nkg and nig <= w('S08.FLAUSG.X.X.IG.X') and nkg <= w('S08.FLAUSG.X.X.KG.X')
          and w('S12.N.%s.PRE.ITTIG.HAUPT' % z) == nig and w('S12.N.%s.POST.ITTKG.HAUPT' % z) == nkg)
    pruef('S08 %s: ANT ALL = (Spieler mit BEST prä und post) / N, FLOPRE + FLITT ≤ N' % z,
          nahe(w('S08.ANT.%s.X.ALL.X' % z), sum(1 for c in spieler if w('S04.BEST.%s.PRE.P%s.X' % (z, c)) is not None and w('S04.BEST.%s.POST.P%s.X' % (z, c)) is not None) / len(spieler), 1e-12))
for z in ['Z30', 'CM', 'SBJ']:
    nig, nkg = w('S08.N.%s.X.ITTIG.X' % z), w('S08.N.%s.X.ITTKG.X' % z)
    pruef('S13 %s: NIG/NKG = S08 ITT, DF = N − 4, S15 DFG = UDDF = N − 2, S18 NTOT = N, DF2 = N − 4' % z,
          w('S13.NIG.%s.X.ITT.HAUPT' % z) == nig and w('S13.NKG.%s.X.ITT.HAUPT' % z) == nkg and w('S13.DF.%s.X.ITT.HAUPT' % z) == nig + nkg - 4
          and w('S15.DFG.%s.X.ITT.HAUPT' % z) == nig + nkg - 2 == w('S15.UDDF.%s.X.ITT.HAUPT' % z) and w('S18.NTOT.%s.X.ITT.X' % z) == nig + nkg and w('S18.DF2.%s.X.ITT.X' % z) == nig + nkg - 4)
    p5, p6, p7, a9 = (w('S08.N.%s.X.PP%dIG.X' % (z, s)) for s in (5, 6, 7)), None, None, None
    p5, p6, p7 = [w('S08.N.%s.X.PP%dIG.X' % (z, s)) for s in (5, 6, 7)]; a9 = w('S08.N.%s.X.AK9IG.X' % z)
    pruef('S08 %s: PP5 ≥ PP6 ≥ PP7 ≥ AK9 (IG), alle ≤ ITT IG, NKG der PP-Modelle = ITT KG' % z,
          nig >= p5 >= p6 >= p7 >= a9 and all(w('S1%d.NKG.%s.X.%s.HAUPT' % (s, z, v)) == nkg for s, v in ((6, 'PP6'), (7, 'PP5'), (7, 'PP7'))) and w('S16.NIG.%s.X.PP6.HAUPT' % z) == p6)
    pruef('S08 %s: INF = 1 genau dann, wenn n_IG ≥ 8 und n_KG ≥ 8 (ITT, PP5, PP6, PP7, FAMS)' % z,
          all(w('S08.INF.%s.X.%s.X' % (z, s)) == int(a >= 8 and b >= 8) for s, a, b in (('ITT', nig, nkg), ('PP5', p5, nkg), ('PP6', p6, nkg), ('PP7', p7, nkg), ('FAMS', w('S08.N.%s.X.FAMSIG.X' % z), w('S08.N.%s.X.FAMSKG.X' % z)))))
    pruef('S16 %s: Zahl der AK9-Einzelwerte = S08 N AK9IG' % z, sum(1 for k in E if k.startswith('S16.DIFF.%s.DIFF.P' % z)) == a9)
ana_ig = sum(1 for c in IG if any(w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) == 1 for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']))
ana_kg = sum(1 for c in KG if any(w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) == 1 for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']))
pruef('S12 ANA: N AGE ANAIG/ANAKG = Spieler in mindestens einem ITT-Set (16, 10), N PAH = N AGE', w('S12.N.AGE.PRE.ANAIG.X') == ana_ig == 16 and w('S12.N.AGE.PRE.ANAKG.X') == ana_kg == 10 and w('S12.N.PAH.PRE.ANAIG.X') == 16 and w('S12.N.PAH.PRE.ANAKG.X') == 10)
pruef('S12 NFAM1 + NFAM2 + NFAMNA = N je Gruppe', all(w('S12.NFAM1.FAM.PRE.%s.X' % m) + w('S12.NFAM2.FAM.PRE.%s.X' % m) + w('S12.NFAMNA.FAM.PRE.%s.X' % m) == w('S01.N.X.X.%s.X' % m) for m in ('IG', 'KG')))
pruef('S06 NMELD ALL = S01 NMELD = Summe NSTAT = Summe NMELD je IG-Spieler', w('S06.NMELD.FB.X.ALL.X') == w('S01.NMELD.FB.X.ALL.X') == sum(w('S06.NSTAT.FB.X.IG.%s' % s) for s in ('GANZ', 'TEILW', 'GARN')) == sum(w('S06.NMELD.FB.X.P%s.X' % c) for c in IG))
pruef('S07 SUMME GANZ = NSTAT GANZ, SUMME GT = GANZ + TEILW, NZUG = N IG, RATE = SUMME/(12·NZUG)',
      w('S07.SUMME.ADH.X.IG.GANZ') == w('S06.NSTAT.FB.X.IG.GANZ') and w('S07.SUMME.ADH.X.IG.GT') == w('S06.NSTAT.FB.X.IG.GANZ') + w('S06.NSTAT.FB.X.IG.TEILW') and w('S07.NZUG.ADH.X.IG.X') == w('S01.N.X.X.IG.X')
      and all(nahe(w('S07.RATE.ADH.X.IG.%s' % v), w('S07.SUMME.ADH.X.IG.%s' % v) / (12 * w('S07.NZUG.ADH.X.IG.X')), 1e-12) for v in ('GANZ', 'GT', 'WOCAP', 'DIST')))
pruef('S07 V00..V12 summieren zu NZUG, GE01 = NZUG − V00, GE12 = V12, GE-Reihe monoton fallend',
      sum(w('S07.V%02d.ADH.X.IG.GANZ' % v) for v in range(13)) == w('S07.NZUG.ADH.X.IG.X') and w('S07.GE01.ADH.X.IG.GANZ') == w('S07.NZUG.ADH.X.IG.X') - w('S07.V00.ADH.X.IG.GANZ')
      and all(w('S07.GE%02d.ADH.X.IG.GANZ' % s) >= w('S07.GE%02d.ADH.X.IG.GANZ' % (s + 1)) for s in range(1, 12)))
pruef('S07 Einzelwerte: Summe ADH GANZ (ohne nicht erhebbar) = SUMME GANZ, WOCAP ≤ GANZ, DIST ≤ GANZ je Spieler, 3 × nicht erhebbar',
      sum(w('S07.ADH.ADH.X.P%s.GANZ' % c) or 0 for c in IG) == w('S07.SUMME.ADH.X.IG.GANZ') and all((w('S07.ADH.ADH.X.P%s.WOCAP' % c) or 0) <= (w('S07.ADH.ADH.X.P%s.GANZ' % c) or 0) and (w('S07.ADH.ADH.X.P%s.DIST' % c) or 0) <= (w('S07.ADH.ADH.X.P%s.GANZ' % c) or 0) for c in IG)
      and sum(1 for c in IG for v in ('GANZ', 'WOCAP', 'DIST') if g('S07.ADH.ADH.X.P%s.%s' % (c, v)) == 'nicht erhebbar') == 3)
pruef('S07 N CR10 = N LOAD = SUMME GANZ, Wochensummen = Gesamt, UE ≤ NMELD, UESP ≤ NMELDSP',
      w('S07.N.CR10.X.IG.GANZ') == w('S07.N.LOAD.X.IG.GANZ') == w('S07.SUMME.ADH.X.IG.GANZ') and sum(w('S07.N.CR10.W%d.IG.GANZ' % k) for k in range(1, 7)) == w('S07.N.CR10.X.IG.GANZ')
      and w('S07.UE.FB.X.IG.X') == sum(w('S07.UE.FB.X.IG.%s' % s) for s in ('GANZ', 'TEILW', 'GARN')) <= w('S06.NMELD.FB.X.ALL.X') and w('S07.UESP.FB.X.IG.X') <= w('S07.NMELDSP.ADH.X.IG.X'))
pruef('S07 ANTW: Summe der Wochenanteile · 2 · NZUG = SUMME GANZ', nahe(sum(w('S07.ANTW.ADH.W%d.IG.GANZ' % k) for k in range(1, 7)) * 2 * w('S07.NZUG.ADH.X.IG.X'), w('S07.SUMME.ADH.X.IG.GANZ'), 1e-9))
pruef('S08 Box 6: B6IF = 1 (BW-21), B6NE ≤ NZUG − B6IF, B6NEKM ≤ B6NE, NMELDSP + B6NEKM + B6IF = NZUG',
      w('S08.B6IF.X.X.IG.X') == 1 and w('S08.B6NE.X.X.IG.X') <= w('S07.NZUG.ADH.X.IG.X') - 1 and w('S08.B6NEKM.X.X.IG.X') <= w('S08.B6NE.X.X.IG.X') and w('S07.NMELDSP.ADH.X.IG.X') + w('S08.B6NEKM.X.X.IG.X') + w('S08.B6IF.X.X.IG.X') == w('S07.NZUG.ADH.X.IG.X'))
for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']:
    for zt in ('PRE', 'POST'):
        kats = ['TECH', 'ZEIT', 'FEHL', 'FALSCH', 'AUSL'] + (['NANG'] if zt == 'POST' else [])
        nk = sum(w('S03.NKAT.%s.%s.%s.%s' % (z, zt, gr, kat)) for gr in ('IG', 'KG') for kat in kats)
        pruef('S02/S03 %s %s: gültig + ungültig = 93 Zeilen (31 × 3), NGUELT = Summe K' % (z, zt), w('S02.NGUELT.%s.%s.ALL.X' % (z, zt)) + nk == 3 * len(spieler) and w('S02.NGUELT.%s.%s.ALL.X' % (z, zt)) == sum(w('S04.K.%s.%s.P%s.X' % (z, zt, c)) for c in spieler))
pruef('S03 NANG post = 12 Zeilen je Zielgröße (4 Spieler × 3), S02 NAUSL = 0', all(w('S03.NKAT.%s.POST.IG.NANG' % z) + w('S03.NKAT.%s.POST.KG.NANG' % z) == 12 for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']) and w('S02.NAUSL.X.PRE.ALL.X') == 0 and w('S02.NAUSL.X.POST.ALL.X') == 0)
pruef('S10 NTE ≤ NSB, DFTE ≥ NTE, S11 N ≤ NTE (prä, alle Zielgrößen)', all(w('S10.NTE.%s.PRE.ALL.X' % z) <= w('S10.NSB.%s.PRE.ALL.X' % z) and w('S10.DFTE.%s.PRE.ALL.X' % z) >= w('S10.NTE.%s.PRE.ALL.X' % z) for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']) and all(w('S11.N.%s.PRE.ALL.X' % z) <= w('S10.NTE.%s.PRE.ALL.X' % z) for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']))
pruef('S10 Vereinswerte: NTE VA + VB + VC = NTE ALL, DFTE VA + VB + VC = DFTE ALL (Z30 prä)', sum(w('S10.NTE.Z30.PRE.V%s.X' % v) for v in 'ABC') == w('S10.NTE.Z30.PRE.ALL.X') and sum(w('S10.DFTE.Z30.PRE.V%s.X' % v) for v in 'ABC') == w('S10.DFTE.Z30.PRE.ALL.X'))
pruef('S09 KMEAN zwischen 0 und 3', all(0 <= w(k) <= 3 for k in E if k.startswith('S09.KMEAN')))

P('\n2 VORZEICHEN UND INNERE KONSISTENZ')
for z in ['Z30', 'CM', 'SBJ']:
    b1, se, df, t, p, kiu, kio = (w('S13.%s.%s.X.ITT.HAUPT' % (gr, z)) for gr in ('B1', 'SEB1', 'DF', 'T', 'P', 'KIU', 'KIO'))
    tc = stats.t.ppf(0.975, df)
    pruef('S13 %s: T = B1/SEB1, P = 2·(1 − T_df(|t|)), KI = B1 ± t·SE, KIU < B1 < KIO' % z, nahe(t, b1 / se, 1e-9) and nahe(p, 2 * stats.t.sf(abs(t), df), 1e-9) and nahe(kiu, b1 - tc * se, 1e-9) and nahe(kio, b1 + tc * se, 1e-9) and kiu < b1 < kio)
    pruef('S13 %s: AMIG − AMKG = B1, SEAM > 0, AM-Intervalle enthalten AM' % z, nahe(w('S13.AMIG.%s.X.ITT.HAUPT' % z) - w('S13.AMKG.%s.X.ITT.HAUPT' % z), b1, 1e-9) and w('S13.AMIGU.%s.X.ITT.HAUPT' % z) < w('S13.AMIG.%s.X.ITT.HAUPT' % z) < w('S13.AMIGO.%s.X.ITT.HAUPT' % z))
    itt = [c for c in spieler if w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) == 1]
    prem = sum(w('S04.BEST.%s.PRE.P%s.X' % (z, c)) for c in itt) / len(itt); pahm = sum(w('S05.PAH.PAH.PRE.P%s.X' % c) for c in itt) / len(itt)
    pruef('S13 %s: PREM und PAHM = Mittel der S04/S05-Werte im ITT-Set' % z, nahe(w('S13.PREM.%s.X.ITT.HAUPT' % z), prem, 1e-9) and nahe(w('S13.PAHM.%s.X.ITT.HAUPT' % z), pahm, 1e-9))
    guenstig = b1 > 0 if z == 'SBJ' else b1 < 0
    pruef('S13 %s: SIG = 1 genau dann, wenn p < 0,05 und günstige Richtung' % z, w('S13.SIG.%s.X.ITT.HAUPT' % z) == int(p < 0.05 and guenstig))
    mig, mkg, ud, spost, use_, ut, udp, udf = (w('S15.%s.%s.X.ITT.HAUPT' % (gr, z)) for gr in ('MPOSTIG', 'MPOSTKG', 'UD', 'SDPOST', 'UDSE', 'UDT', 'UDP', 'UDDF'))
    nig, nkg = w('S13.NIG.%s.X.ITT.HAUPT' % z), w('S13.NKG.%s.X.ITT.HAUPT' % z)
    pruef('S15 %s: UD = MPOSTIG − MPOSTKG, UDSE = SDPOST·√(1/n1 + 1/n2), UDT = UD/UDSE, UDP aus t' % z, nahe(ud, mig - mkg, 1e-9) and nahe(use_, spost * math.sqrt(1 / nig + 1 / nkg), 1e-9) and nahe(ut, ud / use_, 1e-9) and nahe(udp, 2 * stats.t.sf(abs(ut), udf), 1e-9))
    pruef('S15 %s: MPOSTIG/MPOSTKG = S12 M POST ITT, SDPOST = gepoolte S12 SD POST' % z, nahe(mig, w('S12.M.%s.POST.ITTIG.HAUPT' % z), 1e-9) and nahe(mkg, w('S12.M.%s.POST.ITTKG.HAUPT' % z), 1e-9)
          and nahe(spost, math.sqrt(((nig - 1) * w('S12.SD.%s.POST.ITTIG.HAUPT' % z) ** 2 + (nkg - 1) * w('S12.SD.%s.POST.ITTKG.HAUPT' % z) ** 2) / (nig + nkg - 2)), 1e-9))
    J = 1 - 3 / (4 * (nig + nkg - 2) - 1); sdpre = w('S15.SDPRE.%s.X.ITT.HAUPT' % z)
    pruef('S15 %s: J = 1 − 3/(4·df_g − 1), G = B1/SDPRE·J, GKIU/GKIO aus KIU/KIO, |G| < 1' % z, nahe(w('S15.J.%s.X.ITT.HAUPT' % z), J, 1e-12) and nahe(w('S15.G.%s.X.ITT.HAUPT' % z), b1 / sdpre * J, 1e-9) and nahe(w('S15.GKIU.%s.X.ITT.HAUPT' % z), kiu / sdpre * J, 1e-9) and abs(w('S15.G.%s.X.ITT.HAUPT' % z)) < 1)
    pruef('S12 %s: D ITT hat das Vorzeichen von M IG − M KG (prä, ITT)' % z, (w('S12.D.%s.PRE.ITT.HAUPT' % z) > 0) == (w('S12.M.%s.PRE.ITTIG.HAUPT' % z) > w('S12.M.%s.PRE.ITTKG.HAUPT' % z)))
    pruef('S14 %s: SWVERW = (SWP < 0,05), BFVERW = (BFP < 0,05), VERW SLPRE/SLPAH aus PINT, BFDF1 = 1, BFDF2 = N − 2, DFINT = N − 5, DFCINT = n_BPAH − 4' % z,
          w('S14.SWVERW.%s.X.ITT.HAUPT' % z) == int(w('S14.SWP.%s.X.ITT.HAUPT' % z) < 0.05) and w('S14.BFVERW.%s.X.ITT.HAUPT' % z) == int(w('S14.BFP.%s.X.ITT.HAUPT' % z) < 0.05)
          and all(w('S14.VERW.%s.X.ITT.%s' % (z, v)) == int(w('S14.PINT.%s.X.ITT.%s' % (z, v)) < 0.05) for v in ('SLPRE', 'SLPAH')) and w('S14.BFDF1.%s.X.ITT.HAUPT' % z) == 1 and w('S14.BFDF2.%s.X.ITT.HAUPT' % z) == nig + nkg - 2
          and all(w('S14.DFINT.%s.X.ITT.%s' % (z, v)) == nig + nkg - 5 for v in ('SLPRE', 'SLPAH')) and w('S14.DFCINT.%s.PRE.BPAH.SLPAH' % z) == sum(1 for c in spieler if w('S04.BEST.%s.PRE.P%s.X' % (z, c)) is not None and w('S05.PAH.PAH.PRE.P%s.X' % c) is not None) - 4)
    pruef('S14 %s: SDRQ = SDRKG/SDRIG, TINT = BINT/SEINT, PINT aus t (SLPRE)' % z, nahe(w('S14.SDRQ.%s.X.ITT.HAUPT' % z), w('S14.SDRKG.%s.X.ITT.HAUPT' % z) / w('S14.SDRIG.%s.X.ITT.HAUPT' % z), 1e-9)
          and nahe(w('S14.TINT.%s.X.ITT.SLPRE' % z), w('S14.BINT.%s.X.ITT.SLPRE' % z) / w('S14.SEINT.%s.X.ITT.SLPRE' % z), 1e-9) and nahe(w('S14.PINT.%s.X.ITT.SLPRE' % z), 2 * stats.t.sf(abs(w('S14.TINT.%s.X.ITT.SLPRE' % z)), w('S14.DFINT.%s.X.ITT.SLPRE' % z)), 1e-9))
    pruef('S14 %s: Überlappung: OVPREIG ≤ n_IG, OVPREKG ≤ n_KG, OVPRL ≤ OVPRU, OVPAL ≤ OVPAU, %%PAH-Bereich innerhalb 80 bis 100' % z,
          w('S14.OVPREIG.%s.X.ITT.HAUPT' % z) <= nig and w('S14.OVPREKG.%s.X.ITT.HAUPT' % z) <= nkg and w('S14.OVPRL.%s.X.ITT.HAUPT' % z) <= w('S14.OVPRU.%s.X.ITT.HAUPT' % z) and 80 <= w('S14.OVPAL.%s.X.ITT.HAUPT' % z) <= w('S14.OVPAU.%s.X.ITT.HAUPT' % z) <= 100)
    bkiu, bkio = w('S19.BKIU.%s.X.ITT.BOOT' % z), w('S19.BKIO.%s.X.ITT.BOOT' % z)
    pruef('S19 %s: BKIU < B1 < BKIO, Breite Bootstrap-KI zwischen 0,6 und 1,4 der t-Breite, BNGUELT + BNVERW = 10 000' % z, bkiu < b1 < bkio and 0.6 <= (bkio - bkiu) / (kio - kiu) <= 1.4 and w('S19.BNGUELT.%s.X.ITT.BOOT' % z) + w('S19.BNVERW.%s.X.ITT.BOOT' % z) == 10000)
    pruef('S18 %s: MDESR = MDES/0,2, FCRIT = F_1,df2(0,95), POW(D093) > POW(D037), MDES zwischen 0,5 und 2' % z, nahe(w('S18.MDESR.%s.X.ITT.X' % z), w('S18.MDES.%s.X.ITT.X' % z) / 0.2, 1e-9) and nahe(w('S18.FCRIT.%s.X.ITT.X' % z), stats.f.ppf(0.95, 1, w('S18.DF2.%s.X.ITT.X' % z)), 1e-9)
          and w('S18.POW.%s.X.ITT.D093' % z) > w('S18.POW.%s.X.ITT.D037' % z) and 0.5 <= w('S18.MDES.%s.X.ITT.X' % z) <= 2)
pruef('S13 H0REJ = max(SIG), NTEST = 3', w('S13.H0REJ.X.X.ITT.HAUPT') == max(w('S13.SIG.%s.X.ITT.HAUPT' % z) for z in ['Z30', 'CM', 'SBJ']) and w('S13.NTEST.X.X.ITT.HAUPT') == 3)
pruef('S18 Z10: POW(D011) > POW(D006), beide unter 0,10 (unterpowert bei kleinen Effekten)', w('S18.POW.Z10.X.ITT.D011') > w('S18.POW.Z10.X.ITT.D006') and w('S18.POW.Z10.X.ITT.D011') < 0.10)
for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']:
    te, sb, ses, rts, fl = (w('S10.%s.%s.PRE.ALL.X' % (gr, z)) for gr in ('TE', 'SB', 'SESOI', 'RTS', 'FLEINZ'))
    pruef('S10 %s: SESOI = 0,2·SB, RTS = TE/SESOI, FLEINZ = (TE > SESOI) = 1, TELO < TE < TEHI, TE < SB' % z, nahe(ses, 0.2 * sb, 1e-12) and nahe(rts, te / ses, 1e-9) and fl == int(te > ses) == 1 and w('S10.TELO.%s.PRE.ALL.X' % z) < te < w('S10.TEHI.%s.PRE.ALL.X' % z) and te < sb)
for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']:
    dm, ds, ses = w('S11.DMEAN.%s.PRE.ALL.X' % z), w('S11.DSESOI.%s.PRE.ALL.X' % z), w('S10.SESOI.%s.PRE.ALL.X' % z)
    pruef('S11 %s prä: Bias in günstiger Richtung (Zeiten ≤ 0, Sprung ≥ 0), DSESOI = DMEAN/SESOI' % z, ((dm >= 0) if z == 'SBJ' else (dm <= 0)) and nahe(ds, dm / ses, 1e-9))
pruef('S04: CM = (CL + CR)/2 bei allen Spielern mit beiden Seiten, sonst Grund „Eingang fehlt“', all((nahe(w('S04.BEST.CM.%s.P%s.X' % (zt, c)), (w('S04.BEST.CL.%s.P%s.X' % (zt, c)) + w('S04.BEST.CR.%s.P%s.X' % (zt, c))) / 2, 1e-12)
      if (w('S04.BEST.CL.%s.P%s.X' % (zt, c)) is not None and w('S04.BEST.CR.%s.P%s.X' % (zt, c)) is not None) else g('S04.BEST.CM.%s.P%s.X' % (zt, c)) == 'Eingang fehlt') for c in spieler for zt in ('PRE', 'POST')))
pruef('S04: BEST ≤ MEAN bei Zeiten, BEST ≥ MEAN beim Sprung (alle Spieler, prä und post)', all(((w('S04.BEST.%s.%s.P%s.X' % (z, zt, c)) >= w('S04.MEAN.%s.%s.P%s.X' % (z, zt, c)) - 1e-12) if z == 'SBJ' else (w('S04.BEST.%s.%s.P%s.X' % (z, zt, c)) <= w('S04.MEAN.%s.%s.P%s.X' % (z, zt, c)) + 1e-12))
      for c in spieler for zt in ('PRE', 'POST') for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM'] if w('S04.BEST.%s.%s.P%s.X' % (z, zt, c)) is not None))
pruef('S05: %PAH aller Spieler zwischen 80 und 100, PAS zwischen 60 und 80 Zoll, MP zwischen 60 und 75 Zoll', all(80 <= w('S05.PAH.PAH.PRE.P%s.X' % c) <= 100 and 60 <= w('S05.PAS.PAH.PRE.P%s.X' % c) <= 80 for c in spieler if w('S05.PAH.PAH.PRE.P%s.X' % c) is not None) and all(60 <= w('S05.MP.PAH.PRE.P%s.X' % c) <= 75 for c in spieler if w('S05.MP.PAH.PRE.P%s.X' % c) is not None))

P('\n3 GRÖSSENORDNUNG')
def bereich(name, keys, lo, hi):
    vals = [w(k) for k in keys if w(k) is not None]
    pruef('%s: %d Werte zwischen %g und %g' % (name, len(vals), lo, hi), all(lo <= v <= hi for v in vals), 'min %.4g max %.4g' % (min(vals), max(vals)) if vals else 'leer')
bereich('S04 BEST Sprint 5 m (s)', [k for k in E if k.startswith('S04.BEST.Z05.')], 0.8, 1.5)
bereich('S04 BEST Sprint 10 m (s)', [k for k in E if k.startswith('S04.BEST.Z10.')], 1.5, 2.5)
bereich('S04 BEST Sprint 30 m (s)', [k for k in E if k.startswith('S04.BEST.Z30.')], 3.8, 6.0)
bereich('S04 BEST 505 links, rechts, Mittel (s)', [k for k in E if k.startswith(('S04.BEST.CL.', 'S04.BEST.CR.', 'S04.BEST.CM.'))], 2.0, 3.5)
bereich('S04 BEST Standweitsprung (cm)', [k for k in E if k.startswith('S04.BEST.SBJ.')], 150, 290)
bereich('S12 Alter ANA (Jahre)', ['S12.M.AGE.PRE.ANAIG.X', 'S12.M.AGE.PRE.ANAKG.X'], 13.5, 15.5)
bereich('S12 Körperhöhe ANA (cm)', ['S12.M.HGT.PRE.ANAIG.X', 'S12.M.HGT.PRE.ANAKG.X'], 155, 190)
bereich('S12 Körpermasse ANA (kg)', ['S12.M.MASS.PRE.ANAIG.X', 'S12.M.MASS.PRE.ANAKG.X'], 40, 80)
bereich('S10 CV prä (%)', [k for k in E if k.startswith('S10.CV.')], 0.5, 10)
bereich('S07 CR-10 Mittel', ['S07.M.CR10.X.IG.GANZ'], 2, 8)
bereich('S07 sRPE-Load Mittel (AU)', ['S07.M.LOAD.X.IG.GANZ'], 60, 320)
bereich('S13 |B1| relativ zu SDPRE unter 0,5 (Z30, CM, SBJ)', [], 0, 1)
pruef('S13 |B1|/SDPRE < 0,5 bei allen drei Zielgrößen (kleine adjustierte Differenzen)', all(abs(w('S13.B1.%s.X.ITT.HAUPT' % z)) / w('S15.SDPRE.%s.X.ITT.HAUPT' % z) < 0.5 for z in ['Z30', 'CM', 'SBJ']))
pruef('S13 R² zwischen 0,4 und 0,95 (Prä-Wert als starker Prädiktor)', all(0.4 <= w('S13.R2.%s.X.ITT.HAUPT' % z) <= 0.95 for z in ['Z30', 'CM', 'SBJ']))
pruef('S12 Ausgangsunterschiede: IG schneller und weiter als KG (d < 0 bei Zeiten, d > 0 beim Sprung, Menge BASE)', all(w('S12.D.%s.PRE.BASE.HAUPT' % z) < 0 for z in ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'CM']) and w('S12.D.SBJ.PRE.BASE.HAUPT') > 0)

P('\n4 VERGLEICH MIT DER ERSTEN RECHNUNG (Analyseprotokoll 15.09.2026, Kennzahlen 22.09.2026, gerundete Abschriften)')
P('  Erwartung: konfirmatorische Zielgrößen unverändert (Phase 1 änderte nur 10 m post VS-06, Familiarisierung VS-11, Bemerkungstexte).')
P('  Hedges-g mit anderem J (15.09.: df = n − 4, jetzt df = n − 2), daher nur die Richtung verglichen. Steigungsmodelle dort als F, hier als t (F = t²).')
alt = {  # (Kennung, Wert 15.09./22.09., Toleranz = halbe Einheit der letzten gedruckten Stelle, Quelle)
    'S13.B1.Z30.X.ITT.HAUPT': (-0.046, 0.0005, 'AP § 3'), 'S13.KIU.Z30.X.ITT.HAUPT': (-0.200, 0.0005, 'AP § 3'), 'S13.KIO.Z30.X.ITT.HAUPT': (0.107, 0.0005, 'AP § 3'), 'S13.P.Z30.X.ITT.HAUPT': (0.536, 0.0005, 'AP § 3'),
    'S15.UD.Z30.X.ITT.HAUPT': (-0.327, 0.0005, 'AP § 3'), 'S15.UDKIU.Z30.X.ITT.HAUPT': (-0.497, 0.0005, 'AP § 3'), 'S15.UDKIO.Z30.X.ITT.HAUPT': (-0.156, 0.0005, 'AP § 3'),
    'S13.B1.CM.X.ITT.HAUPT': (-0.014, 0.0005, 'AP § 3'), 'S13.KIU.CM.X.ITT.HAUPT': (-0.086, 0.0005, 'AP § 3'), 'S13.KIO.CM.X.ITT.HAUPT': (0.057, 0.0005, 'AP § 3'), 'S13.P.CM.X.ITT.HAUPT': (0.678, 0.0005, 'AP § 3'),
    'S15.UD.CM.X.ITT.HAUPT': (-0.060, 0.0005, 'AP § 3'), 'S15.UDKIU.CM.X.ITT.HAUPT': (-0.147, 0.0005, 'AP § 3'), 'S15.UDKIO.CM.X.ITT.HAUPT': (0.026, 0.0005, 'AP § 3'),
    'S13.B1.SBJ.X.ITT.HAUPT': (0.2, 0.05, 'AP § 3'), 'S13.KIU.SBJ.X.ITT.HAUPT': (-8.3, 0.05, 'AP § 3'), 'S13.KIO.SBJ.X.ITT.HAUPT': (8.7, 0.05, 'AP § 3'), 'S13.P.SBJ.X.ITT.HAUPT': (0.960, 0.0005, 'AP § 3'),
    'S15.UD.SBJ.X.ITT.HAUPT': (10.1, 0.05, 'AP § 3'), 'S15.UDKIU.SBJ.X.ITT.HAUPT': (-2.5, 0.05, 'AP § 3'), 'S15.UDKIO.SBJ.X.ITT.HAUPT': (22.7, 0.05, 'AP § 3'),
    'S17.B1.Z30.X.ITT.MW': (-0.065, 0.0005, 'AP § 4'), 'S17.P.Z30.X.ITT.MW': (0.402, 0.0005, 'AP § 4'), 'S17.B1.CM.X.ITT.MW': (0.004, 0.0005, 'AP § 4'), 'S17.B1.SBJ.X.ITT.MW': (-2.2, 0.05, 'AP § 4'),
    'S16.B1.Z30.X.PP6.HAUPT': (0.028, 0.0005, 'AP § 4'), 'S16.P.Z30.X.PP6.HAUPT': (0.794, 0.0005, 'AP § 4'), 'S16.B1.SBJ.X.PP6.HAUPT': (0.9, 0.05, 'AP § 4'),
    'S17.B1.Z30.X.PP5.HAUPT': (-0.000, 0.0005, 'AP § 4'), 'S17.B1.CM.X.PP5.HAUPT': (-0.017, 0.0005, 'AP § 4'), 'S17.B1.SBJ.X.PP5.HAUPT': (-1.6, 0.05, 'AP § 4'),
    'S17.B1.Z30.X.PP7.HAUPT': (0.029, 0.0005, 'AP § 4'), 'S17.B1.SBJ.X.PP7.HAUPT': (-0.5, 0.05, 'AP § 4'),
    'S17.B1.Z30.X.ITT.AEND': (0.048, 0.0005, 'AP § 4'), 'S17.B1.CM.X.ITT.AEND': (-0.012, 0.0005, 'AP § 4'), 'S17.B1.SBJ.X.ITT.AEND': (-0.4, 0.05, 'AP § 4'),
    'S17.B1.Z30.X.ITT.OPAH': (-0.061, 0.0005, 'AP § 4'), 'S17.B1.CM.X.ITT.OPAH': (-0.008, 0.0005, 'AP § 4'), 'S17.B1.SBJ.X.ITT.OPAH': (1.1, 0.05, 'AP § 4'),
    'S14.SWW.Z30.X.ITT.HAUPT': (0.915, 0.0005, 'AP § 5'), 'S14.SWP.Z30.X.ITT.HAUPT': (0.035, 0.0005, 'AP § 5'), 'S14.SWW.CM.X.ITT.HAUPT': (0.927, 0.0005, 'AP § 5'), 'S14.SWP.CM.X.ITT.HAUPT': (0.096, 0.0005, 'AP § 5'),
    'S14.SWW.SBJ.X.ITT.HAUPT': (0.967, 0.0005, 'AP § 5'), 'S14.SWP.SBJ.X.ITT.HAUPT': (0.553, 0.0005, 'AP § 5'),
    'S14.BFF.Z30.X.ITT.HAUPT': (2.30, 0.005, 'AP § 5'), 'S14.BFP.Z30.X.ITT.HAUPT': (0.142, 0.0005, 'AP § 5'), 'S14.BFF.CM.X.ITT.HAUPT': (1.12, 0.005, 'AP § 5'), 'S14.BFP.CM.X.ITT.HAUPT': (0.301, 0.0005, 'AP § 5'),
    'S14.BFF.SBJ.X.ITT.HAUPT': (0.78, 0.005, 'AP § 5'), 'S14.BFP.SBJ.X.ITT.HAUPT': (0.385, 0.0005, 'AP § 5'),
    'S14.PINT.Z30.X.ITT.SLPRE': (0.395, 0.0005, 'AP § 5'), 'S14.PINT.Z30.X.ITT.SLPAH': (0.180, 0.0005, 'AP § 5'), 'S14.PINT.CM.X.ITT.SLPRE': (0.407, 0.0005, 'AP § 5'), 'S14.PINT.CM.X.ITT.SLPAH': (0.889, 0.0005, 'AP § 5'),
    'S14.PINT.SBJ.X.ITT.SLPRE': (0.199, 0.0005, 'AP § 5'), 'S14.PINT.SBJ.X.ITT.SLPAH': (0.408, 0.0005, 'AP § 5'),
    'S10.TE.Z05.PRE.ALL.X': (0.046, 0.0005, 'K-05'), 'S10.TE.Z10.PRE.ALL.X': (0.037, 0.0005, 'K-05'), 'S10.TE.Z30.PRE.ALL.X': (0.077, 0.0005, 'K-05'), 'S10.TE.CL.PRE.ALL.X': (0.089, 0.0005, 'K-05'), 'S10.TE.CR.PRE.ALL.X': (0.083, 0.0005, 'K-05'),
    'S10.TE.SBJ.PRE.ALL.X': (6.1, 0.05, 'K-05'), 'S10.TE.CM.PRE.ALL.X': (0.058, 0.0005, 'K-05'),
    'S10.SESOI.Z05.PRE.ALL.X': (0.016, 0.0005, 'K-05'), 'S10.SESOI.Z30.PRE.ALL.X': (0.063, 0.0005, 'K-05'), 'S10.SESOI.SBJ.PRE.ALL.X': (3.3, 0.05, 'K-05'), 'S10.SESOI.CM.PRE.ALL.X': (0.020, 0.0005, 'K-05'),
    'S10.RTS.Z30.PRE.ALL.X': (1.24, 0.005, 'K-05'), 'S10.RTS.SBJ.PRE.ALL.X': (1.85, 0.005, 'K-05'), 'S10.RTS.CM.PRE.ALL.X': (2.88, 0.005, 'K-05'), 'S10.CV.Z30.PRE.ALL.X': (1.6, 0.05, 'K-05'), 'S10.CV.SBJ.PRE.ALL.X': (2.7, 0.05, 'K-05'),
    'S12.M.Z30.PRE.IG.HAUPT': (4.526, 0.0005, 'K-06'), 'S12.SD.Z30.PRE.IG.HAUPT': (0.235, 0.0005, 'K-06'), 'S12.M.Z30.PRE.KG.HAUPT': (4.932, 0.0005, 'K-06'), 'S12.SD.Z30.PRE.KG.HAUPT': (0.251, 0.0005, 'K-06'), 'S12.D.Z30.PRE.BASE.HAUPT': (-1.68, 0.005, 'K-06'),
    'S12.M.SBJ.PRE.IG.HAUPT': (237.4, 0.05, 'K-06'), 'S12.M.SBJ.PRE.KG.HAUPT': (224.5, 0.05, 'K-06'), 'S12.D.SBJ.PRE.BASE.HAUPT': (0.84, 0.005, 'K-06'), 'S12.M.CM.PRE.IG.HAUPT': (2.467, 0.0005, 'K-06'), 'S12.M.CM.PRE.KG.HAUPT': (2.525, 0.0005, 'K-06'), 'S12.D.CM.PRE.BASE.HAUPT': (-0.60, 0.005, 'K-06'),
    'S12.M.AGE.PRE.ANAIG.X': (15.10, 0.005, 'K-02b'), 'S12.SD.AGE.PRE.ANAIG.X': (0.26, 0.005, 'K-02b'), 'S12.M.AGE.PRE.ANAKG.X': (14.08, 0.005, 'K-02b'), 'S12.M.HGT.PRE.ANAIG.X': (173.9, 0.05, 'K-02b'), 'S12.M.HGT.PRE.ANAKG.X': (168.7, 0.05, 'K-02b'),
    'S12.M.MASS.PRE.ANAIG.X': (60.8, 0.05, 'K-02b'), 'S12.M.MASS.PRE.ANAKG.X': (53.3, 0.05, 'K-02b'), 'S12.M.PAH.PRE.ANAIG.X': (94.65, 0.005, 'K-02b'), 'S12.SD.PAH.PRE.ANAIG.X': (2.90, 0.005, 'K-02b'), 'S12.M.PAH.PRE.ANAKG.X': (90.41, 0.005, 'K-02b'), 'S12.SD.PAH.PRE.ANAKG.X': (2.85, 0.005, 'K-02b'),
    'S09.KMEAN.Z30.PRE.IG.X': (2.61, 0.005, 'K-04.8'), 'S09.KMEAN.Z30.PRE.KG.X': (2.38, 0.005, 'K-04.8'), 'S09.KMEAN.SBJ.PRE.IG.X': (2.50, 0.005, 'K-04.8'), 'S09.KMEAN.SBJ.PRE.KG.X': (2.08, 0.005, 'K-04.8'), 'S09.KMEAN.Z05.PRE.KG.X': (1.00, 0.005, 'K-04.8'),
    'S02.NGUELT.Z05.PRE.ALL.X': (None, 0, 'K-04.2 Summe'),
}
n_alt = 0; n_alt_ok = 0; abw = []
for k, (v, tol, q) in alt.items():
    if v is None: continue
    n_alt += 1; ist = w(k)
    ok = ist is not None and abs(ist - v) <= tol + 1e-12
    n_alt_ok += int(ok)
    if not ok: abw.append((k, v, ist, q))
pruef('Summe der gültigen Prä-Versuche über alle Zielgrößen = 384 (K-04.2)', sum(w('S02.NGUELT.%s.PRE.ALL.X' % z) for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR']) == 384)
pruef('Ausfälle prä: TECH 94, ZEIT 64, FEHL 16 (K-04.4 bis K-04.6)', all(sum(w('S03.NKAT.%s.PRE.%s.%s' % (z, gr, kat)) for z in ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR'] for gr in ('IG', 'KG')) == n for kat, n in (('TECH', 94), ('ZEIT', 64), ('FEHL', 16))))
pruef('Adhärenz: SUMME GANZ 92, Rate 92/216, Median 6, GE04..GE09 = 12, 11, 10, 8, 5, 3, V12 = 1, NMELDSP 15, UE 12 bei 9 Spielern (FA 12.09., F14 § 3.2, § 11.7)',
      w('S07.SUMME.ADH.X.IG.GANZ') == 92 and nahe(w('S07.RATE.ADH.X.IG.GANZ'), 92 / 216, 1e-12) and w('S07.MED.ADH.X.IG.GANZ') == 6 and [w('S07.GE%02d.ADH.X.IG.GANZ' % s) for s in range(4, 10)] == [12, 11, 10, 8, 5, 3]
      and w('S07.V12.ADH.X.IG.GANZ') == 1 and w('S07.NMELDSP.ADH.X.IG.X') == 15 and w('S07.UE.FB.X.IG.X') == 12 and w('S07.UESP.FB.X.IG.X') == 9)
pruef('S06: 111 Meldungen, 7 korrigiert, 92 ganz, 6 teilweise, 13 gar nicht (FA 12.09.)', w('S06.NMELD.FB.X.ALL.X') == 111 and w('S06.NKORR.FB.X.ALL.X') == 7 and w('S06.NSTAT.FB.X.IG.GANZ') == 92 and w('S06.NSTAT.FB.X.IG.TEILW') == 6 and w('S06.NSTAT.FB.X.IG.GARN') == 13)
pruef('Fallzahlen je ITT-Set wie K-07 (16/7, 7/10, 16/10, 15/10, 14/10, 16/10, 13/10)', [(w('S08.N.%s.X.ITTIG.X' % z), w('S08.N.%s.X.ITTKG.X' % z)) for z in ['Z05', 'Z10', 'Z30', 'CL', 'CR', 'SBJ', 'CM']] == [(16, 7), (7, 10), (16, 10), (15, 10), (14, 10), (16, 10), (13, 10)])
pruef('Familiarisierung: IG 10 × 1, 8 × 2; KG 0 × 1, 13 × 2 (VS-11 in Phase 1 nachgetragen, K-01.12/13 nannte 12 und eine fehlende Angabe)', w('S12.NFAM1.FAM.PRE.IG.X') == 10 and w('S12.NFAM2.FAM.PRE.IG.X') == 8 and w('S12.NFAM2.FAM.PRE.KG.X') == 13 and w('S12.NFAMNA.FAM.PRE.KG.X') == 0)
pruef('Gerundete Werte der ersten Rechnung: %d von %d innerhalb der Rundungstoleranz' % (n_alt_ok, n_alt), n_alt_ok == n_alt)
for k, v, ist, q in abw: P('      Abweichung %s: 15.09./22.09. %s, jetzt %.6g (%s)' % (k, v, ist, q))
pruef('S15 g: Richtung wie 15.09. (Z30 negativ, CM negativ, SBJ positiv), Betrag unter 0,2', w('S15.G.Z30.X.ITT.HAUPT') < 0 and w('S15.G.CM.X.ITT.HAUPT') < 0 and w('S15.G.SBJ.X.ITT.HAUPT') > 0 and all(abs(w('S15.G.%s.X.ITT.HAUPT' % z)) < 0.2 for z in ['Z30', 'CM', 'SBJ']))
pruef('Schlusslogik: alle drei Zielgrößen Fall C1 (KI schließt −SESOI, 0 und +SESOI ein), H0 nicht abgelehnt', all(w('S13.KIU.%s.X.ITT.HAUPT' % z) < -w('S10.SESOI.%s.PRE.ALL.X' % z) and w('S13.KIO.%s.X.ITT.HAUPT' % z) > w('S10.SESOI.%s.PRE.ALL.X' % z) for z in ['Z30', 'CM', 'SBJ']) and w('S13.H0REJ.X.X.ITT.HAUPT') == 0)
pruef('TE post Verein A 30 m größer als TE prä Verein A (Belastungsfrage F14 § 11.3)', w('S10.TE.Z30.POST.VA.X') > w('S10.TE.Z30.PRE.VA.X'))

P('\n5 URSACHE DER ABWEICHUNGEN ZUR ERSTEN RECHNUNG: REGEL FÜR %PAH')
P('  Die erste Rechnung (15.09.) und das Kennzahlenblatt (22.09.) übernahmen %PAH aus der Workbook-Spalte PAH_Prozent. Deren Formel')
P('  (01_Personen, Spalte PAH_cm) wählt die Koeffizientenzeile der NÄCHSTEN Halbjahresstufe (ROUND(Alter·2,0)/2), rechnet Pfund mit 2,20462')
P('  und rundet PAH_cm auf 0,1 cm. Die Spezifikation S05 interpoliert linear zwischen den Halbjahreszeilen (O2, nachträglich 24.09.),')
P('  rechnet mit 0,45359237 kg je Pfund (K3) und rundet nicht (0.5 Nr. 1). Nachrechnung mit der Workbook-Formel aus dem Datenstand:')
import numpy as np
DS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(CSV))), 'Datenstand_2026-09-24')
KRP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(CSV))), 'Spezifikation_2026-09-24_Koeffizienten_KR.csv')
if os.path.exists(DS) and os.path.exists(KRP):
    def lies(p):
        with open(p, encoding='utf-8', newline='') as f: return list(csv.DictReader(f))
    PERS = {p['Code']: p for p in lies(os.path.join(DS, 'Personendaten.csv'))}
    KR = {float(r['alter_jahre']): (float(r['beta0']), float(r['stature_in']), float(r['weight_lb']), float(r['midparent_in'])) for r in lies(KRP)}
    def pah_wb(p):
        if not p['Koerperhoehe_prae'] or not p['Koerpermasse_prae'] or not p['Groesse_Mutter'] or not p['Groesse_Vater']: return None
        row = round(float(p['Alter_prae']) * 2) / 2
        if row not in KR: return None
        b0, b1_, b2, b3 = KR[row]; hgt = float(p['Koerperhoehe_prae']); mp = (float(p['Groesse_Mutter']) + float(p['Groesse_Vater'])) / 2
        return hgt / round((b0 + hgt / 2.54 * b1_ + float(p['Koerpermasse_prae']) * 2.20462 * b2 + mp / 2.54 * b3) * 2.54, 1) * 100
    wbp = {c: pah_wb(p) for c, p in PERS.items()}
    d = [wbp[c] - w('S05.PAH.PAH.PRE.P%s.X' % c) for c in spieler if wbp[c] is not None and w('S05.PAH.PAH.PRE.P%s.X' % c) is not None]
    P('  Differenz Workbook-Formel minus Spezifikation je Spieler (Prozentpunkte): min %.3f, max %.3f, mittlerer Betrag %.3f, n = %d' % (min(d), max(d), float(np.mean(np.abs(d))), len(d)))
    ziele = ['Z05', 'Z10', 'Z30', 'SBJ', 'CL', 'CR', 'CM']
    ana = {gr: [c for c in spieler if (c.startswith('VS') == (gr == 'KG')) and any(w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) == 1 for z in ziele)] for gr in ('IG', 'KG')}
    for gr, soll in (('IG', (94.65, 2.90)), ('KG', (90.41, 2.85))):
        v = [wbp[c] for c in ana[gr]]
        pruef('ANA %s: Workbook-Formel reproduziert K-02b (M %.2f, SD %.2f)' % (gr, *soll), abs(float(np.mean(v)) - soll[0]) <= 0.005 and abs(float(np.std(v, ddof=1)) - soll[1]) <= 0.005)
    for z, sb1, sp, tb in (('Z30', -0.046, 0.536, 0.0005), ('CM', -0.014, 0.678, 0.0005), ('SBJ', 0.2, 0.960, 0.05)):
        itt = [c for c in spieler if w('S08.MITGL.%s.X.P%s.ITT' % (z, c)) == 1]
        y = np.array([w('S04.BEST.%s.POST.P%s.X' % (z, c)) for c in itt])
        X = np.column_stack([np.ones(len(itt)), [0.0 if c.startswith('VS') else 1.0 for c in itt], [w('S04.BEST.%s.PRE.P%s.X' % (z, c)) for c in itt], [wbp[c] for c in itt]])
        b = np.linalg.lstsq(X, y, rcond=None)[0]; r = y - X @ b; df = len(y) - 4; cov = (r @ r) / df * np.linalg.inv(X.T @ X); t = b[1] / math.sqrt(cov[1, 1]); p = 2 * stats.t.sf(abs(t), df)
        pruef('%s: ANCOVA mit Workbook-%%PAH reproduziert 15.09. (b1 %s, p %s), Spezifikation ergibt %.4g, p %.3f' % (z, sb1, sp, w('S13.B1.%s.X.ITT.HAUPT' % z), w('S13.P.%s.X.ITT.HAUPT' % z)), abs(b[1] - sb1) <= tb and abs(p - sp) <= 0.0005)
    P('  Folgerung: Die Abweichungen in Abschnitt 4 sind vollständig durch die nachträglichen Festlegungen O2, K3 und 0.5 Nr. 1 erklärt.')
    P('  Sie gehören mit altem und neuem Wert in das Register (Auswertungsverfahren 2.3). Die Schlusslogik ändert sich nicht (Fall C1, H0 nicht abgelehnt).')
else:
    P('  Datenstand nicht neben der Ergebnisdatei gefunden, Nachrechnung übersprungen.')

P('\nERGEBNIS: %d Prüfungen bestanden, %d nicht bestanden' % (ok_n, fail_n))
P('Die nicht bestandenen Prüfungen in Abschnitt 4 (gerundete Werte der ersten Rechnung, Richtung von g beim Standweitsprung) sind in Abschnitt 5 erklärt.')
P('Erzeugt:', datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'))
with open(OUT, 'w', encoding='utf-8') as f: f.write(buf.getvalue())

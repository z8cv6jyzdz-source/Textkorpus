#!/usr/bin/env python3
# Programmkennzahlen_2026-09-23.py — Kennzahlen des plyometrischen Heimtrainingsprogramms für 4.5.1 (Kennungen P-01 … P-08)
# Quelle: Planung_Intervention\Trainingsprogramm\Trainingsdokumentation_Block1-3.docx (bereinigte Kopie, 34.064 B, 12.09.2026), Teil B Wochentabellen,
#         von Hand übertragen (Übung, Stufe, DVZ-Typ, Sätze × Wdh., Kontakte). Videodauern: Fragebogenauswertung_2026-09-12 § 5 (Verfasser 12.09.).
# Zweck: einzige Zahlenquelle für Programmzahlen im Manuskript (das Kennzahlenblatt K-01…K-08 trägt nur Workbook-Zahlen).
# Ausgabe: Programmkennzahlen_2026-09-23.txt. Erstellt in Cowork, 23.09.2026. Prüfung: Wochensummen gegen die Dokumentationssummen 52/66/80/96/106/120.
from collections import OrderedDict, defaultdict

# (Übung, Lloyd-Stufe, DVZ-Typ, Richtung, unilateral, Sätze, Wdh, Kontakte) — Kontakte 0 bei Stufe-1-Übungen (keine Sprünge)
W = OrderedDict()
W[1] = [("Bodyweight Squats",1,"FMS","-",False,2,8,0), ("In-line Lunges",1,"FMS","-",False,2,6,0), ("Stick-Landing",2,"Landeschulung","vertikal",False,2,6,12),
        ("On-the-spot Jumps",2,"langsam","vertikal",False,2,8,16), ("Standing Vertical Jump",2,"langsam","vertikal",False,2,6,12), ("Standing Horizontal Jump",2,"langsam","horizontal",False,2,6,12)]
W[2] = [("Bodyweight Squats",1,"FMS","-",False,1,8,0), ("In-line Lunges",1,"FMS","-",False,1,6,0), ("Stick-Landing",2,"Landeschulung","vertikal",False,2,6,12),
        ("On-the-spot Jumps",2,"langsam","vertikal",False,3,8,24), ("Standing Vertical Jump",2,"langsam","vertikal",False,3,6,18), ("Standing Horizontal Jump",2,"langsam","horizontal",False,2,6,12)]
W[3] = [("Stick-Landing",2,"Landeschulung","vertikal",False,1,6,6), ("Standing Vertical Jump",2,"langsam","vertikal",False,3,6,18), ("Standing Horizontal Jump",2,"langsam","horizontal",False,3,6,18),
        ("Pogo Hops",3,"schnell","vertikal",False,3,8,24), ("Vorwärts Ankle Hops",3,"schnell","horizontal",False,2,7,14)]
W[4] = [("Stick-Landing",2,"Landeschulung","vertikal",False,1,6,6), ("Standing Vertical Jump",2,"langsam","vertikal",False,3,7,21), ("Standing Horizontal Jump",2,"langsam","horizontal",False,3,7,21),
        ("Pogo Hops",3,"schnell","vertikal",False,3,10,30), ("Vorwärts Ankle Hops",3,"schnell","horizontal",False,3,6,18)]
W[5] = [("Standing Vertical Jump",2,"langsam","vertikal",False,3,6,18), ("Standing Horizontal Jump",2,"langsam","horizontal",False,3,6,18), ("Pogo Hops",3,"schnell","vertikal",False,3,10,30),
        ("Vorwärts Ankle Hops",3,"schnell","horizontal",False,3,6,18), ("Zickzack-Sprünge",3,"schnell","multidirektional",False,2,8,16), ("Einbeiniger Standsprung",2,"langsam","horizontal",True,1,3,6)]
W[6] = [("Standing Vertical Jump",2,"langsam","vertikal",False,3,7,21), ("Standing Horizontal Jump",2,"langsam","horizontal",False,3,7,21), ("Pogo Hops",3,"schnell","vertikal",False,3,10,30),
        ("Vorwärts Ankle Hops",3,"schnell","horizontal",False,3,8,24), ("Zickzack-Sprünge",3,"schnell","multidirektional",False,2,8,16), ("Einbeiniger Standsprung",2,"langsam","horizontal",True,1,4,8)]
SOLL = {1:52, 2:66, 3:80, 4:96, 5:106, 6:120}
VIDEO = {1:"28:16", 2:"28:02", 3:"24:17", 4:"25:55", 5:"31:03", 6:"31:14"}; ERW = "8:53"
def mmss(s): m, sec = s.split(":"); return int(m)*60 + int(sec)
def fmt(t): return f"{t//60}:{t%60:02d}"

out = []
out.append("Programmkennzahlen 4.5.1 — aus Trainingsdokumentation_Block1-3.docx (Teil B), Stand 23.09.2026")
out.append("")
tot = 0; dvz = defaultdict(int); rich = defaultdict(int); uni = 0; ex = set(); reps = []; sets = []
out.append(f"{'Woche':<6}{'Übungen':>8}{'Kontakte/Einheit':>17}{'Soll (Dok.)':>12}{'davon schnell':>14}{'langsam':>9}{'Lande':>7}{'unilateral':>11}")
for wk, rows in W.items():
    k = sum(r[7] for r in rows); tot += k
    f = sum(r[7] for r in rows if r[2]=="schnell"); l = sum(r[7] for r in rows if r[2]=="langsam"); la = sum(r[7] for r in rows if r[2]=="Landeschulung"); u = sum(r[7] for r in rows if r[4])
    assert k == SOLL[wk], (wk, k, SOLL[wk])
    for r in rows:
        dvz[r[2]] += r[7]; rich[r[3]] += r[7]; ex.add(r[0]); reps.append(r[6]); sets.append(r[5])
    uni += u
    out.append(f"{wk:<6}{len(rows):>8}{k:>17}{SOLL[wk]:>12}{f:>14}{l:>9}{la:>7}{u:>11}")
out.append("")
out.append(f"P-01 Bodenkontakte je Einheit W1→W6: {' → '.join(str(SOLL[w]) for w in W)} (Wochensummen der Dokumentation reproduziert)")
out.append(f"P-02 Bodenkontakte je Programmwoche (2 identische Einheiten): {' · '.join(str(2*SOLL[w]) for w in W)}; Summe über 12 Einheiten = {2*tot} (Summe der 6 Wocheneinheiten = {tot})")
out.append(f"P-03 Übungen gesamt: {len(ex)} verschiedene ({', '.join(sorted(ex))}); je Einheit {min(len(r) for r in W.values())}–{max(len(r) for r in W.values())}")
out.append(f"P-04 Sätze × Wiederholungen: Sätze {min(sets)}–{max(sets)}, Wiederholungen {min(reps)}–{max(reps)} (Stufe-1-Übungen ohne Kontakte: Squats 2×8/1×8, Lunges 2×6/1×6 je Bein)")
tb = tot
out.append(f"P-05 DVZ-Typ (Kontakte je Programm, Basis {tb} = eine Einheit je Woche summiert; ×2 = 12 Einheiten): schnell {dvz['schnell']} ({100*dvz['schnell']/tb:.1f} %) · langsam {dvz['langsam']} ({100*dvz['langsam']/tb:.1f} %) · Landeschulung {dvz['Landeschulung']} ({100*dvz['Landeschulung']/tb:.1f} %)")
out.append(f"P-06 Richtung: vertikal {rich['vertikal']} ({100*rich['vertikal']/tb:.1f} %) · horizontal {rich['horizontal']} ({100*rich['horizontal']/tb:.1f} %) · multidirektional {rich['multidirektional']} ({100*rich['multidirektional']/tb:.1f} %)")
out.append(f"P-07 Unilateral: {uni} Kontakte ({100*uni/tb:.1f} %), nur W5/W6 (Einbeiniger Standsprung, Stufe 2, 1×3 bzw. 1×4 je Bein)")
out.append(f"P-08 Stufen nach Lloyd et al. (2011): Stufe 1 nur W1–W2 (Squats, Lunges) · Stufe 2 W1–W6 · Stufe 3 ab W3 (Pogo Hops, Ankle Hops; Zickzack ab W5) · Stufen 4–6 nicht verwendet")
out.append(f"P-09 Pausen (Dokumentation Teil B: 90 s zwischen Sätzen aller Übungen; Produktionsleitfaden § 2: 45 s zwischen den Stufe-1-Sätzen; Videografik: 120 s zwischen Übungen) — ⚠ 45 s steht NICHT in der Trainingsdokumentation, nur im Produktionsleitfaden; am Video prüfen")
out.append("P-10 Sitzungsdauer (Soll = Videodauer; Fragebogenauswertung § 5, Verfasser 12.09.):")
for wk in W:
    v = mmss(VIDEO[wk]); s = v + mmss(ERW)
    out.append(f"      W{wk}: Wochenvideo {VIDEO[wk]} + Erwärmungsvideo {ERW} = {fmt(s)} min")
lo = min(mmss(VIDEO[w]) for w in W) + mmss(ERW); hi = max(mmss(VIDEO[w]) for w in W) + mmss(ERW)
out.append(f"      Spanne Sitzung {fmt(lo)}–{fmt(hi)} min (Wochenvideo {min(VIDEO.values(), key=mmss)}–{max(VIDEO.values(), key=mmss)}); Antrag 30–40 min (W6 um {hi-40*60} s darüber)")
out.append("P-11 Frequenz/Dauer: 6 Wochen, 2 Einheiten je Woche = 12 Einheiten, 20.07.–30.08.2026 (Programmwochen Mo–So), Vorgabe ≥ 48 h Abstand (Infoblatt: „Mindestens 2 Tage Pause“)")
out.append("P-12 Antrag (16.06.2026, Abschnitt 2): 2 Einheiten/Woche à 30–40 min über 6 Wochen; Bausteine Koordination/Technik, Plyometrie, Kraft (Eigengewicht); W1–2 Technik/niedrig, W3–4 „Kraftblock“, W5–6 reaktiv mit zunehmend einbeinigen Übungen; Kontakte „etwa 60 bis 80“ → „etwa 100 bis 120“ je Einheit; RAMP-Erwärmung; Progression nach Lloyd & Oliver (2012)")
out.append("      Abgleich Programm wie geliefert: Startvolumen 52 (< 60–80) · Endvolumen 120 (im Rahmen) · kein Kraftblock W3–4 (Kraftübungen mit Eigengewicht nur W1–2, Stufe 1) · unilateral nur 14 Kontakte in W5–6 · Dauer 33:10–40:07 (im Rahmen, W6 +7 s) · Erwärmung als eigenes Video 8:53 (Antrag: RAMP, Dauer nicht festgelegt)")
txt = "\n".join(out)
print(txt)
open("Programmkennzahlen_2026-09-23.txt", "w", encoding="utf-8").write(txt + "\n")

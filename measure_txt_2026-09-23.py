#!/usr/bin/env python3
"""measure_txt.py — misst einen Textvorschlag (Absätze durch Leerzeilen getrennt) mit denselben Regeln wie measure451:
Leerzeichen-Token, Satzgrenzen, Semikola, Abschnittsverweise, Belegklammern, Anhangsverweise, Verbotsliste, 'Ausgangstestung'."""
import sys, re, statistics

path = sys.argv[1]
text = open(path, encoding="utf-8").read()
paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

def words(s): return len(s.split())
def sentences(s):
    s2 = re.sub(r"(Abschn|et al|ca|bzw|vgl|z\. B|u\. a|Nr|S|Tab|Abb)\.", lambda m: m.group(0).replace(".", "§"), s)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ(\d„*])", s2)
    return [x.replace("§", ".") for x in parts if x.strip()]

verboten = ["im Rahmen", "Gegenstand der Untersuchung", "es ist festzuhalten", "darüber hinaus", "des Weiteren",
            "hierbei gilt", "zunächst", "anschließend", "abschließend", "Interessanterweise", "in diesem Zusammenhang",
            "sodass", "weshalb", "unsere ", "Ausgangstestung", "randomisiert", "absolviert"]
total=0; all_s=[]; semi=0; refs=0; cites=0; anh=0
for i,p in enumerate(paras,1):
    w=words(p); total+=w; ss=sentences(p); all_s+=ss
    sc=p.count(";"); semi+=sc
    r=len(re.findall(r"Abschn(?:itt|\.)\s*\d|Abschnitten\s*\d|Kapitel\s*\d|siehe unten|siehe oben", p)); refs+=r
    c=len(re.findall(r"\([^()]*\d{4}[^()]*\)", p)); cites+=c
    a=len(re.findall(r"Anhang [A-H]", p)); anh+=a
    lens=[words(x) for x in ss]
    print(f"Abs. {i}: {w} Wörter, {len(ss)} Sätze (Median {statistics.median(lens)}, max {max(lens)}), Semikola {sc}, Abschnittsverweise {r}, Belegklammern {c}, Anhangsverweise {a}")
lens=[words(x) for x in all_s]
print(f"GESAMT: {total} Wörter, {len(all_s)} Sätze, Median {statistics.median(lens)}, längster {max(lens)}, > 32: {sum(l>32 for l in lens)}, > 40: {sum(l>40 for l in lens)}")
marker = len(re.findall(r"\[(EXTRAPOLATION|BELEGT|FÜR SCHWAB)\]", text))
print(f"Semikola {semi} · Abschnittsverweise {refs} · Belegklammern {cites} · Anhangsverweise {anh} · Marker {marker}")
hits=[v for v in verboten if v.lower() in text.lower()]
print("Verbotsliste-Treffer:", hits if hits else "keine")
print("Sätze > 28 Wörter:")
for s in all_s:
    if words(s) > 28: print(f"  [{words(s)}] {s}")

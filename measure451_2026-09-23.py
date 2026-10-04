#!/usr/bin/env python3
"""measure451_2026-09-23.py — Misst einen Abschnitt des Manuskript-Masters (Absatztext zwischen zwei Überschriften, ohne Überschriften,
Tabellen, Beschriftungen). Erstellt in Cowork 23.09.2026 (Task „Übergabe 4.5.1“, Rev. 75); reproduziert Rev. 74 (4.1 309, 4.5.1 854, 4.5.2 496, 4.6 175).
Aufruf: python3 measure451_2026-09-23.py master.docx "4.5.1" "4.5.2" [--dump]
Ausgabe: Wörter (Leerzeichen-Token, wie measure_all.py der Vorsitzungen), Sätze, Median und längster Satz, Semikola,
Abschnittsverweise (Abschn./Abschnitt/Kapitel + Ziffer, „siehe unten/oben“), Belegklammern, „Ausgangstestung“; mit --dump der Wortlaut je Absatz."""

import sys, re, statistics
from docx import Document

path, start, stop = sys.argv[1], sys.argv[2], sys.argv[3]
doc = Document(path)
paras = []
inside = False
for p in doc.paragraphs:
    t = p.text.strip()
    style = (p.style.name or "").lower()
    is_heading = style.startswith("heading") or style.startswith("überschrift") or re.match(r"^\d+(\.\d+)*\s+\S", t) and len(t) < 90
    if is_heading:
        if t.startswith(start + " "):
            inside = True
            continue
        if inside and t.startswith(stop + " "):
            break
        if inside:
            continue
    if inside and t:
        paras.append(t)

def words(s):
    return len(s.split())

def sentences(s):
    # Satzgrenzen: . ! ? gefolgt von Leerzeichen und Großbuchstabe/Klammer/Zahl; Abkürzungen grob ausgenommen
    s2 = re.sub(r"(Abschn|et al|ca|bzw|vgl|z\. B|u\. a|Nr|S|Tab|Abb)\.", lambda m: m.group(0).replace(".", "§"), s)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ(\d„*])", s2)
    return [x.replace("§", ".") for x in parts if x.strip()]

total = 0
all_sent = []
semi = 0
refs = 0
cites = 0
ausg = 0
print(f"Abschnitt {start}: {len(paras)} Absätze")
for i, p in enumerate(paras, 1):
    w = words(p)
    total += w
    ss = sentences(p)
    all_sent += ss
    sc = p.count(";")
    semi += sc
    r = len(re.findall(r"Abschn(?:itt|\.)\s*\d|Abschnitten\s*\d|Kapitel\s*\d|siehe unten|siehe oben", p))
    refs += r
    c = len(re.findall(r"\([^()]*\d{4}[^()]*\)", p))
    cites += c
    ausg += len(re.findall(r"Ausgangstestung", p))
    lens = [words(x) for x in ss]
    print(f"  Abs. {i}: {w} Wörter, {len(ss)} Sätze (Median {statistics.median(lens) if lens else 0}, max {max(lens) if lens else 0}), {sc} Semikola, {r} Abschnittsverweise, {c} Belegklammern")
lens = [words(x) for x in all_sent]
print(f"GESAMT: {total} Wörter, {len(all_sent)} Sätze, Median {statistics.median(lens)}, längster {max(lens)}, Sätze > 32: {sum(1 for l in lens if l > 32)}, > 40: {sum(1 for l in lens if l > 40)}")
print(f"Semikola {semi} · Abschnittsverweise {refs} · Belegklammern {cites} · 'Ausgangstestung' {ausg}")
print("Längste Sätze:")
for s in sorted(all_sent, key=words, reverse=True)[:5]:
    print(f"  [{words(s)}] {s[:160]}…")
if "--dump" in sys.argv:
    for i, p in enumerate(paras, 1):
        print(f"\n[ABS{i}]\n{p}")

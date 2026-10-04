#!/usr/bin/env python3
"""Literaturraster_Zaehlwerkzeug_2026-09-27.py — Zaehlwerkzeug fuer die Literaturanalyse Kapitel 2 (erstellt fuer 2.4, 27.09.2026). Textfassungen der PDF mit pdftotext nach /home/claude/txt (Pfad D anpassen).
Aufrufe:
  zaehle.py text "Satz oder Absatz"                 -> Woerter (Leerraum-Token)
  zaehle.py span DATEI "Startmarke" "Endmarke"       -> Woerter von Startmarke bis einschl. Endmarke:
                                                        roh (alle Token) und absatz (Bloecke <20 Woerter, zahlenlastige
                                                        Bloecke, Table/Figure-Zeilen verworfen), dazu PDF-Seiten
  zaehle.py seite DATEI "Textstelle"                 -> PDF-Seite (1-basiert) der Textstelle
Marken: 4 bis 12 Woerter woertlich aus der .txt-Datei (nicht .layout.txt); Gross/Klein, Satzzeichen, Zeilenumbrueche
und Silbentrennung am Zeilenende werden ignoriert. DATEI = Name in /home/claude/txt (mit oder ohne .txt)."""
import sys, re, os
D = "/home/claude/txt"
def load(f):
    p = f if os.path.isabs(f) else os.path.join(D, f if f.endswith('.txt') else f + '.txt')
    return open(p, encoding='utf-8', errors='ignore').read()
def norm(t): return re.sub(r'[^\w]', '', t.lower())
def tokens(txt):
    # pro Seite, Silbentrennung am Zeilenende zusammenziehen
    out = []  # (token, seite, block)
    pages = txt.split('\f')
    blk = 0
    for pi, pg in enumerate(pages, 1):
        pg = re.sub(r'(\w)-\n(\w)', r'\1\2', pg)
        for b in re.split(r'\n\s*\n', pg):
            blk += 1
            for w in b.split():
                out.append((w, pi, blk))
    return out
def find(toks, marke, start=0):
    m = [norm(x) for x in marke.split() if norm(x)]
    n = [norm(t[0]) for t in toks]
    for i in range(start, len(n) - len(m) + 1):
        if n[i:i+len(m)] == m: return i, i + len(m) - 1
    # tolerant: erstes und letztes Markenwort
    return None
def absatz(seg):
    from collections import defaultdict
    bl = defaultdict(list)
    for w, p, b in seg: bl[b].append(w)
    keep = 0
    for b, ws in bl.items():
        s = ' '.join(ws)
        num = sum(1 for w in ws if re.fullmatch(r'[\d.,±%()\-–−<>=/:;*]+', w))
        if len(ws) < 20: continue
        if num / len(ws) > 0.3: continue
        if re.match(r'^(Table|TABLE|Fig\.|Figure|FIGURE)\s*\d', s): continue
        keep += len(ws)
    return keep
if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    if a[0] == 'text':
        print(len(' '.join(a[1:]).split()))
    elif a[0] == 'span':
        toks = tokens(load(a[1]))
        s = find(toks, a[2])
        if not s: print('Startmarke nicht gefunden'); sys.exit(1)
        e = find(toks, a[3], s[0])
        if not e: print('Endmarke nicht gefunden (nach Startmarke)'); sys.exit(1)
        seg = toks[s[0]:e[1]+1]
        print(f"roh {len(seg)} · absatz {absatz(seg)} · PDF-S. {seg[0][1]}-{seg[-1][1]}")
        print('Anfang:', ' '.join(t[0] for t in seg[:8]), '| Ende:', ' '.join(t[0] for t in seg[-8:]))
    elif a[0] == 'seite':
        toks = tokens(load(a[1]))
        s = find(toks, a[2])
        print(f"PDF-S. {toks[s[0]][1]}" if s else 'nicht gefunden')

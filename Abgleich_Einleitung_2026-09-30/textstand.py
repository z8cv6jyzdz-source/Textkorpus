# -*- coding: utf-8 -*-
"""
textstand.py — Schritt 1 des Tasks „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (30.09.2026)

Baut zwei Kandidaten für den Textstand der Einleitung und misst sie wie Manuskriptstand_2026-09-25.py
(Wörter = Leerraum-Token mit Belegklammern, Satzteilung mit derselben Funktion saetze()):
  V  Zusammensetzung nach Übergabe § 3 aus den Textvorschlägen (Ordnerfassungen, per Zeilenanker gelesen):
     B1a und B1b nach Textvorschlag B1 § 1.1 und § 1.2 · B2 nach Textvorschlag B2 D1 (Fassung 4) ·
     B3 nach Textvorschlag B3 bis B5 § 1 (Fassung 2) mit dem Beginn nach Textvorschlag B1 § 1.3 ·
     B4 nach Textvorschlag B4 § 1 (Fassung 3) · B5 nach Textvorschlag B3 bis B5 § 1, S1 mit „deshalb“ (Befund § 7)
  A  Text des Verfassers, Anhang zum Taskstart 30.09.2026, 14:39 (Textstand_Verfasser_Anhang_2026-09-30.txt)
Schreibt textstand_V.json, textstand_A.json, textstand_messung.txt und textstand_diff.txt.
Ohne Semikolon im Skript (chr(59)).
"""
import json, os, re, statistics as st, difflib, sys
HIER = os.path.dirname(os.path.abspath(__file__))
_REL = os.path.normpath(os.path.join(HIER, '..', '..', '04_Uebergaben'))
TV = sys.argv[1] if len(sys.argv) > 1 else (_REL if os.path.isdir(_REL) else '/mnt/user-data/uploads/Bachelorarbeit/Claude/04_Uebergaben')
ANH = os.path.join(HIER, 'Textstand_Verfasser_Anhang_2026-09-30.txt')
SEMI = chr(59)


def lies(name):
    with open(os.path.join(TV, name), encoding='utf-8') as f:
        return f.read().split('\n')


def absatz_nach(zeilen, anker, versatz=2):
    """Absatz, der versatz Zeilen nach der Ankerzeile steht (Ankerzeile muss genau einmal vorkommen)."""
    idx = [i for i, z in enumerate(zeilen) if z.startswith(anker)]
    assert len(idx) == 1, (anker, idx)
    t = zeilen[idx[0] + versatz].strip()
    assert t and not t.startswith('#') and not t.startswith('|'), (anker, t[:60])
    return t


# --- Satzteilung wie Manuskriptstand_2026-09-25.py (Fassung 3), Funktion saetze() unverändert übernommen ---
def saetze(text):
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
            teil = teil.strip()
            m = re.match(r"(.+?),\s(\d{4}[a-z]?)", teil)
            if m:
                out.append(m.group(1).replace('’', "'").strip() + ' ' + m.group(2))
    return out


# --- V: Zusammensetzung nach Übergabe § 3 ---
b1 = lies('Textvorschlag_Einleitung_B1_2026-09-29.md')
b2 = lies('Textvorschlag_Einleitung_B2_2026-09-29.md')
b35 = lies('Textvorschlag_Einleitung_B3_B5_2026-09-29.md')
b4 = lies('Textvorschlag_Einleitung_B4_Reifung_2026-09-29.md')
B1a = absatz_nach(b1, '### 1.1 B1a')
B1b = absatz_nach(b1, '### 1.2 B1b')
hicks = absatz_nach(b1, '### 1.3 B3', 4)
assert hicks.startswith('Im Sprint entscheidet'), hicks[:40]
B2 = absatz_nach(b2, '## D1 Wortlaut B2, Fassung 4')
B3alt = absatz_nach(b35, '**B3 neu')
s3 = saetze(B3alt)
assert s3[0].startswith('Spielanalysen zufolge') and s3[1].startswith('Dabei werden sehr hohe') and s3[2].startswith('Beim Beschleunigen')
B3 = ' '.join([hicks] + s3[3:])
B4 = absatz_nach(b4, '## 1 Wortlaut B4, Fassung 3')
B5alt = absatz_nach(b35, '**B5 — Zweck')
assert B5alt.startswith('Ziel der Studie war es zu prüfen, ob')
B5 = B5alt.replace('Ziel der Studie war es zu prüfen, ob', 'Ziel der Studie war es deshalb zu prüfen, ob', 1)
V = {'B1a': B1a, 'B1b': B1b, 'B2': B2, 'B3': B3, 'B4': B4, 'B5': B5}

# --- A: Text des Verfassers ---
with open(ANH, encoding='utf-8-sig') as f:
    roh = [z.strip() for z in f.read().replace('\r', '').split('\n')]
A, akt = {}, None
for z in roh:
    if not z or z == 'Einleitung':
        continue
    m = re.match(r'^(B\d[a-z]?)\s—\s(.*)$', z)
    if m:
        akt = m.group(1)
        A[akt] = {'titel': m.group(2), 'text': ''}
        continue
    assert akt, z[:40]
    A[akt]['text'] = (A[akt]['text'] + ' ' + z).strip()
A_titel = {k: v['titel'] for k, v in A.items()}
A = {k: v['text'] for k, v in A.items()}


def messe(T, name):
    zeilen, alle, absw, alle_q, klammern = [], [], {}, [], 0
    for k, t in T.items():
        s = saetze(t)
        w = len(t.split())
        absw[k] = w
        for i, x in enumerate(s, 1):
            alle.append((k, i, x, len(x.split()), len(ohne_belege(x).split()), len(KLAMMER.findall(x))))
        alle_q += quellen(t)
        klammern += len(KLAMMER.findall(t))
    W = sum(absw.values())
    Wo = sum(len(ohne_belege(t).split()) for t in T.values())
    lens = [a[3] for a in alle]
    semi = sum(ohne_belege(t).count(SEMI) for t in T.values())
    verw = sum(len(re.findall(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)', t)) for t in T.values())
    belegte = sum(1 for a in alle if a[5] > 0)
    zeilen.append('Textstand %s: %d Wörter (ohne Belegklammern %d), %d Absätze %s' % (name, W, Wo, len(T), ' · '.join('%s %d' % (k, v) for k, v in absw.items())))
    zeilen.append('  Sätze %d · Median %s · längster %d (%s) · über 32: %d · Absätze über 250: %d' % (
        len(alle), str(st.median(lens)).replace('.', ','), max(lens), '%s S%d' % max(alle, key=lambda a: a[3])[:2],
        sum(1 for x in lens if x > 32), sum(1 for v in absw.values() if v > 250)))
    zeilen.append('  Belegklammern %d · Sätze mit Beleg %d von %d (%s %%) · Quellen %d · Semikola außerhalb von Belegklammern %d · Abschnittsverweise %d' % (
        klammern, belegte, len(alle), str(round(belegte / len(alle) * 100, 1)).replace('.', ','), len(set(alle_q)), semi, verw))
    zeilen.append('  Quellen: ' + ' · '.join(sorted(set(alle_q))))
    return zeilen, alle


out = []
for T, n in [(V, 'V (Zusammensetzung nach Übergabe § 3)'), (A, 'A (Text des Verfassers, Anhang 30.09.)')]:
    z, alle = messe(T, n)
    out += z
    out.append('')
    for k, i, x, w, wo, kl in alle:
        out.append('  %-4s S%-2d %3d W  %s' % (k, i, w, x))
    out.append('')
with open(os.path.join(HIER, 'textstand_messung.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
json.dump({'quelle': 'Übergabe § 3', 'absaetze': V}, open(os.path.join(HIER, 'textstand_V.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'quelle': 'Anhang des Verfassers 30.09.', 'titel': A_titel, 'absaetze': A}, open(os.path.join(HIER, 'textstand_A.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# --- Satzweiser Abgleich A gegen V ---
SV = [(k, i, x) for k, t in V.items() for i, x in enumerate(saetze(t), 1)]
SA = [(k, i, x) for k, t in A.items() for i, x in enumerate(saetze(t), 1)]
d = []
sm = difflib.SequenceMatcher(a=[x for _, _, x in SV], b=[x for _, _, x in SA], autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal':
        for a, b in zip(SV[i1:i2], SA[j1:j2]):
            d.append('=  V %s S%d  |  A %s S%d' % (a[0], a[1], b[0], b[1]))
        continue
    for a in SV[i1:i2]:
        best = max(SA, key=lambda b: difflib.SequenceMatcher(a=a[2], b=b[2]).ratio())
        r = difflib.SequenceMatcher(a=a[2], b=best[2]).ratio()
        d.append('-  V %s S%d (ähnlichster A-Satz %s S%d, Ähnlichkeit %.2f): %s' % (a[0], a[1], best[0], best[1], r, a[2]))
    for b in SA[j1:j2]:
        best = max(SV, key=lambda a: difflib.SequenceMatcher(a=a[2], b=b[2]).ratio())
        r = difflib.SequenceMatcher(a=best[2], b=b[2]).ratio()
        d.append('+  A %s S%d (ähnlichster V-Satz %s S%d, Ähnlichkeit %.2f): %s' % (b[0], b[1], best[0], best[1], r, b[2]))
with open(os.path.join(HIER, 'textstand_diff.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(d) + '\n')
print('\n'.join(out[:4]))
z, _ = messe(A, 'A')
print('\n'.join(z))

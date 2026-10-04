# -*- coding: utf-8 -*-
# Schreibt beide Kandidaten des Textstands mit Satznummern (Satzteilung wie Manuskriptstand_2026-09-25.py)
# Liest textstand_V.json und textstand_A.json aus textstand.py, schreibt textstand_saetze.md
import json, re
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
out = []
for name, f in [('V — Zusammensetzung nach Übergabe § 3 (B5 S1 mit „deshalb“)', 'textstand_V.json'), ('A — Text des Verfassers, Anhang 30.09.', 'textstand_A.json')]:
    d = json.load(open(f, encoding='utf-8'))
    out.append('## ' + name)
    out.append('')
    for k, t in d['absaetze'].items():
        s = saetze(t)
        out.append('### %s (%d Wörter, %d Sätze)' % (k, len(t.split()), len(s)))
        for i, x in enumerate(s, 1):
            out.append('%s S%d (%d): %s' % (k, i, len(x.split()), x))
        out.append('')
open('textstand_saetze.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))

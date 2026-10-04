# -*- coding: utf-8 -*-
"""
abschnitte_saetze.py — Task „Ergebnisse: Abgleich mit der Argumentationsstruktur und Überarbeitung“, Schritt 1

Alle Textabsätze des Masters (Formatvorlage Standard, ohne Felder, Platzhalter ⟨…⟩ gesondert) mit Satznummern,
Satzteilung wie Manuskriptstand_2026-09-25.py Fassung 4. Kennungen: Einleitung B1a, B1b, B2, B3, B4, B5 (wie im
Abgleich der Einleitung vom 30.09.), sonst <Abschnitt> A<n>, Kapitel 5 A1 bis A6, 6.1 A1 bis A6 (wie Textvorschlag 6.1).
Dazu je Satz die Merkmale, an denen ein Bezug auf Kapitel 5 erkennbar wird (Zahlen und Begriffe aus Kapitel 5,
Objektverweise). Die Merkmale sind Suchhilfe, die Zuordnung ist von Hand (bezug_kapitel5.md).
Aufruf: python abschnitte_saetze.py <Master.docx> <textstand.json> <Ausgabe.json> <Ausgabe.md>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import json
import zipfile
from xml.sax.saxutils import unescape

MASTER, TS, AUSJ, AUSM = sys.argv[1:5]
EINL = ['B1a', 'B1b', 'B2', 'B3', 'B4', 'B5']


def saetze(text):
    """Satzteilung wie Manuskriptstand_2026-09-25.py Fassung 4 (unverändert seit Fassung 1)."""
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


z = zipfile.ZipFile(MASTER)
xml = z.read('word/document.xml').decode('utf-8')
P = []
for m in re.finditer(r'<w:p(?=[ >/])', xml):
    a = m.start()
    k = xml.find('>', a)
    if xml[k - 1] == '/':
        P.append(('', '', False))
        continue
    e = xml.find('</w:p>', a) + 6
    inh = xml[a:e]
    st = re.search(r'<w:pStyle w:val="([^"]+)"', inh)
    txt = unescape(''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', inh)))
    feld = 'fldChar' in inh or 'instrText' in inh or '<w:fldSimple' in inh
    P.append((st.group(1) if st else '', txt, feld))

ts = json.load(open(TS, encoding='utf-8'))
k5 = ' '.join(a['text'] for a in ts['absaetze'])
# Zahlen aus Kapitel 5 (Ziffernfolgen mit Komma), ohne Objektnummern und Messstrecken
k5_ohne = re.sub(r'(?:Tab|Abb)\.\s[A-H]?\d+', ' ', k5)
k5_ohne = re.sub(r'\d+-m|505|CR-10|95-%', ' ', k5_ohne)
ZAHLEN = sorted(set(x.lstrip('−+') for x in re.findall(r'[−+]?\d+(?:,\d+)?', k5_ohne)), key=lambda x: (len(x), x))
BEGRIFFE = ['Teilnehmerfluss', 'planmäßig', 'Eingangstestung angetreten', 'Analyseset', 'Analysepopulation',
            'Ausgangswert', 'Ausgangsunterschied', 'Ausgangsvorsprung', 'zugunsten', 'standardisierte', 'Überlappung',
            'zugeteilt', 'meldeten', 'Meldung', 'vollständig', 'teilweise', 'nicht durchgeführt', 'Median',
            'Umsetzung', 'angebotene', 'mindestens sechs', 'mindestens neun', 'Untergrenze', 'Programmwoche',
            'Einheitennummer', 'Beanspruchung', 'CR-10', 'sRPE', 'Solldauer', 'Schmerz', 'Probleme',
            'typische Messfehler', 'typischen Messfehler', 'SESOI', 'gültige Versuche', 'gültigen Versuche',
            'unadjustiert', 'adjustiert', 'Gruppendifferenz', 'Gruppenunterschied', 'Hedges', 'Modelllinie',
            'reifeadjustiert', 'Konfidenzintervall', 'nachweisbar', 'beide Richtungen', 'unschlüssig',
            'Nullhypothese', 'verworfen', 'nur beschrieben', 'beschreibend', 'Beschreibend', 'Shapiro-Wilk',
            'Normalverteilung', 'Residuen', 'Bootstrap', 'Voraussetzung', 'Per-Protokoll', 'Sensitivitätsanalyse',
            'Fallzahl', 'Inferenz', 'Programmangebot', 'Antragskriterium', 'Adhärenz', 'Versuche']
OBJ = re.compile(r'(?:Tab|Abb)\.\s[A-H]?\d+[a-z]?')

out = []
akt = None
zaehler = {}
einl_i = 0
k5_i = 0
for st, txt, feld in P:
    if st.startswith('berschrift'):
        m = re.match(r'^(\d+(?:\.\d+)*)\s', txt.strip())
        akt = m.group(1) if m else txt.strip()
        continue
    if st.startswith('Verzeichnis') or feld or not txt.strip() or akt is None:
        continue
    if st not in ('', 'Standard'):
        continue
    if akt == '1':
        kenn = EINL[einl_i] if einl_i < len(EINL) else 'B?%d' % einl_i
        einl_i += 1
    else:
        zaehler[akt] = zaehler.get(akt, 0) + 1
        kenn = '%s A%d' % (akt, zaehler[akt])
    platz = txt.strip().startswith('⟨')
    for n, s in enumerate(saetze(txt) if not platz else [txt.strip()], 1):
        merk = []
        for zahl in ZAHLEN:
            if re.search(r'(?<![\d,])' + re.escape(zahl) + r'(?![\d,]|-m)', s):
                merk.append('Zahl ' + zahl)
        for b in BEGRIFFE:
            if b.lower() in s.lower():
                merk.append(b)
        merk += ['Objekt ' + o for o in OBJ.findall(s)]
        out.append({'abschnitt': akt, 'absatz': kenn, 'satz': n, 'id': '%s S%d' % (kenn, n), 'platzhalter': platz,
                    'woerter': len(s.split()), 'text': s, 'merkmale': merk})

json.dump({'zahlen_kapitel5': ZAHLEN, 'begriffe': BEGRIFFE, 'saetze': out}, open(AUSJ, 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
Z = ['# Master — alle Textabsätze mit Satznummern und Suchmerkmalen (Schritt 1, 03.10.2026)', '',
     'Zahlen aus Kapitel 5 als Suchmerkmal: ' + ', '.join(ZAHLEN), '']
akt = None
for s in out:
    if s['abschnitt'] != akt:
        akt = s['abschnitt']
        Z.append('')
        Z.append('## ' + akt)
        Z.append('')
    Z.append('%s (%d): %s%s' % (s['id'], s['woerter'], s['text'],
                                ('  ⟦' + ' · '.join(s['merkmale']) + '⟧') if s['merkmale'] else ''))
open(AUSM, 'w', encoding='utf-8').write('\n'.join(Z) + '\n')
print('Sätze:', len(out), '· mit Merkmal:', sum(1 for s in out if s['merkmale']))

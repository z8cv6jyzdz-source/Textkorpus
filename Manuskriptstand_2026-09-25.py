# -*- coding: utf-8 -*-
"""
Manuskriptstand_2026-09-25.py — Messung des Manuskript-Masters je Abschnitt
Bachelorarbeit U15-Plyometrie · DSHS Köln · Grundlage für Projektanweisungen § 5.2, Gliederung v6 § 3.4 und den Plan

Misst am docx (keine Schätzung, F17 § 1.1): Absatztext je Abschnitt (Formatvorlage Standard, ohne Beschriftungen,
Anmerkungen zu Objekten und Platzhalter ⟨…⟩), Wörter als Leerraum-Token wie in der Word-Zählung des Masters,
Semikola außerhalb von Zitierklammern, nummerierte Abschnittsverweise (Stilprofil Teil 4), Platzhalter, Marker
([BELEGT], [EXTRAPOLATION], [FÜR SCHWAB]), Sätze über 32 und über 40 Wörter, Absätze über 250 Wörter.

Fassung 4 (30.09.2026, Task 11, Maßnahme G37 d): Budgets nach Gliederung v6 § 3.4 (E4, verbindlich je Abschnitt der v6)
neben den Blockrichtwerten der Vorgabe vom 23.09. (4.1 bis 7). Zusammengelegte Blöcke werden ihrem v6-Abschnitt
zugeschlagen (ELTERN_V6): 4.4.1 bis 4.4.3 → 4.4 · 4.5.1, 4.5.2, 4.6 → 4.5 (Endnr. 2.5) · 5.1, 5.2 → 5 (Endnr. 3) ·
6.3 → 6.2 (Endnr. 4.2). Steht ein Kapitel ohne die Blocküberschriften im Master (Kapitel 5 ab Task 11, 6.2 und 6.3 ab
Task 12), ist der Block im Master nicht mehr messbar: Die Blockrichtwerte gelten dann für die Absatzgruppen im
Textvorschlag, die Ausgabe nennt das. Die Einleitung zählt nur ihren eigenen Text unter „1“, sobald er im Master steht.
Steht der Altbestand (2, 2.x, 3) noch daneben (M24 offen), wird er getrennt ausgewiesen und nicht der Einleitung
zugeschlagen. Ohne eigenen Text unter „1“ gilt wie in Fassung 3 der Altbestand als Einleitung.
Endnummern nach Task 18 (v6): 2.1 → 4.1, 2.2 → 4.2, 2.3 → 4.3, 2.4 → 4.4, 2.5 → 4.5, 2.6 → 4.7, 3 → 5, 4.1 → 6.1,
4.2 → 6.2, 5 → 7. Erkannt an „2 Methodik“ als Hauptüberschrift.
Block „Seitenschätzung — Modellrechnung, keine Messung“: Parameter aus `Seitenmodell_2026-09-28.csv`, gemessene Wörter
(Einleitung gemessen, sobald ihr Text im Master steht), Zahl verschiedener Autor-Jahr-Belege ohne Altbestand.
Beschriftungen: Formatvorlage Caption oder Absatz der Form „Tab. 1.“ / „Abb. H7.“. Ohne Semikolon im Skript (chr(59)).
Aufruf: python Manuskriptstand_2026-09-25.py <Master.docx> <Ausgabe.txt> [<Ausgabe.csv>] [<Seitenmodell.csv>]
        Ohne vierten Pfad wird `Seitenmodell_2026-09-28.csv` neben dem Skript gesucht.
Frühere Fassungen: 3 (28.09.): Einleitung statt Kapitel 1 bis 3, Summen gegen 6.350, Arbeits- und Endnummern,
Seitenschätzung · 2 (25.09., spät): Budget 4.7 = 550. Fassung 3 liegt in `_Archiv\\_ersetzt_2026-09-30_Messskript_Fassung3`.
"""
import sys
import os
import re
import csv
from docx import Document

SRC, OUT = sys.argv[1], sys.argv[2]
CSV = sys.argv[3] if len(sys.argv) > 3 else None
SMODELL = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                              'Seitenmodell_2026-09-28.csv')
SEMI = chr(59)

# Blockrichtwerte der Vorgabe (Arbeitsnummern, Klick 5 vom 23.09., verbindlich seit 25.09.). „1“ ist die Einleitung.
BUDGET = {'1': 1500,
          '4.1': 300, '4.2': 215, '4.3': 340, '4.4': 420, '4.5.1': 420, '4.5.2': 150, '4.6': 155, '4.7': 550,
          '5.1': 230, '5.2': 220, '6.1': 700, '6.2': 400, '6.3': 500, '7': 250}
# Budgets je Abschnitt der Gliederung v6 (E4), Schlüssel Arbeitsnummer, dazu Endnummer und Titel
V6 = [('1', '1', 'Einleitung', 1500),
      ('4.1', '2.1', 'Studiendesign', 300),
      ('4.2', '2.2', 'Stichprobe', 215),
      ('4.3', '2.3', 'Untersuchungsablauf', 340),
      ('4.4', '2.4', 'Leistungsdiagnostik', 420),
      ('4.5', '2.5', 'Trainingsintervention und Begleitbedingungen', 725),
      ('4.7', '2.6', 'Statistische Auswertung', 550),
      ('5', '3', 'Ergebnisse', 450),
      ('6.1', '4.1', 'Einordnung der Ergebnisse', 700),
      ('6.2', '4.2', 'Methodendiskussion, Stärken und Limitationen', 900),
      ('7', '5', 'Fazit und Ausblick', 250)]
GESAMT = 6350
assert sum(x[3] for x in V6) == GESAMT and sum(BUDGET.values()) == GESAMT
ALTBESTAND = ['2', '2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.5', '3']
# Block → v6-Abschnitt (Arbeitsnummern)
ELTERN_V6 = {'4.4.1': '4.4', '4.4.2': '4.4', '4.4.3': '4.4', '4.5.1': '4.5', '4.5.2': '4.5', '4.6': '4.5',
             '5.1': '5', '5.2': '5', '6.3': '6.2'}
# Block → Blockrichtwert (nur die Unterabschnitte von 4.4 gehen in 4.4 auf)
ELTERN_BLOCK = {'4.4.1': '4.4', '4.4.2': '4.4', '4.4.3': '4.4'}
MARKER = ['[BELEGT]', '[EXTRAPOLATION]', '[FÜR SCHWAB]']
RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')
NAME = r"[A-ZÄÖÜ][A-Za-zÄÖÜäöüßéèáíóúñ'’\-]+"
AUTOR = r"(?:R Core Team|" + NAME + r"(?:,\s" + NAME + r",\set al\.|\set al\.|\s(?:&|und)\s" + NAME + r")?)"


def saetze(text):
    """Satzteilung mit Schutz der Abkürzungen und Dezimalzahlen (unverändert seit Fassung 1)."""
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


def ohne_zitierklammern(text):
    return re.sub(r'\([^)]*\d{4}[^)]*\)', '', text)


def schluessel(autor, jahr):
    a = re.sub(r'\s+und\s+', ' & ', autor.strip().rstrip(','))
    return a.replace('’', "'") + ' ' + jahr


def belege(text):
    """Verschiedene Autor-Jahr-Belege eines Textes, Sekundärquellen vor „zitiert nach“ getrennt."""
    gefunden, sekundaer = set(), set()
    for m in re.finditer('(' + AUTOR + r')\s\((\d{4}[a-z]?)((?:,\s\d{4}[a-z]?)*)(?:,\s[^)]*)?\)', text):
        for j in [m.group(2)] + re.findall(r'\d{4}[a-z]?', m.group(3) or ''):
            gefunden.add(schluessel(m.group(1), j))
    for g in re.finditer(r'\(([^()]*?\d{4}[^()]*?)\)', text):
        for teil in g.group(1).split(SEMI):
            stuecke = re.split(r',\szitiert nach\s', teil.strip())
            for i, st in enumerate(stuecke):
                st = re.sub(r'^(?:vgl\.|nach)\s', '', st.strip())
                m = re.match('(' + AUTOR + r'),\s(\d{4}[a-z]?)((?:,\s\d{4}[a-z]?)*)', st)
                if not m:
                    continue
                for j in [m.group(2)] + re.findall(r'\d{4}[a-z]?', m.group(3) or ''):
                    k = schluessel(m.group(1), j)
                    if len(stuecke) > 1 and i == 0:
                        sekundaer.add(k)
                    else:
                        gefunden.add(k)
    return gefunden - sekundaer, sekundaer


def de(x, nk=1):
    s = ('%.' + str(nk) + 'f') % x
    ganz, _, dez = s.partition('.')
    ganz = ganz.lstrip('-')
    g = []
    while len(ganz) > 3:
        g.insert(0, ganz[-3:])
        ganz = ganz[:-3]
    g.insert(0, ganz)
    return ('−' if x < 0 else '') + '.'.join(g) + (',' + dez if dez else '')


d = Document(SRC)
abschnitte = []
akt = None
for p in d.paragraphs:
    st = p.style.name
    txt = p.text.strip()
    if st.startswith('Heading'):
        m = re.match(r'^(\d+(?:\.\d+)*)\s', txt)
        nr = m.group(1) if m else txt
        akt = {'nr': nr, 'titel': txt, 'ebene': st, 'absaetze': [], 'platzhalter': 0, 'beschriftungen': 0, 'anmerkungen': 0}
        abschnitte.append(akt)
        continue
    if akt is None or not txt:
        continue
    if txt.startswith('⟨'):
        akt['platzhalter'] += 1
        continue
    if st == 'Caption' or re.match(r'^(Tab|Abb)\.\s[A-H]?\d+\.(\s|$)', txt):
        akt['beschriftungen'] += 1
        continue
    if txt.startswith('Anmerkung.'):
        akt['anmerkungen'] += 1
        continue
    if st != 'Normal':
        continue
    akt['absaetze'].append(txt)

# Arbeits- und Endnummern: nach der Umnummerierung (Task 18) steht „2 Methodik“ als Hauptüberschrift
ENDNUMMERN = any(a['ebene'] == 'Heading 1' and re.match(r'^2\s+Methodik', a['titel']) for a in abschnitte)
END_ZU_ARBEIT = {'2': '4', '2.1': '4.1', '2.2': '4.2', '2.3': '4.3', '2.4': '4.4', '2.5': '4.5', '2.6': '4.7',
                 '3': '5', '4': '6', '4.1': '6.1', '4.2': '6.2', '5': '7'}


def arbeitsnummer(nr):
    if not re.match(r'^\d', nr):
        return nr
    if ENDNUMMERN:
        return END_ZU_ARBEIT.get(nr, nr)
    return nr


def v6_schluessel(an):
    return ELTERN_V6.get(an, an)


vorhanden = {arbeitsnummer(a['nr']) for a in abschnitte}
einl_eigen = sum(len(x.split()) for a in abschnitte if arbeitsnummer(a['nr']) == '1' for x in a['absaetze'])
alt_da = (not ENDNUMMERN) and any(a['nr'] in ALTBESTAND for a in abschnitte)
alt_w = sum(len(x.split()) for a in abschnitte if a['nr'] in ALTBESTAND and not ENDNUMMERN for x in a['absaetze'])
# Einleitung: eigener Text unter „1“, sobald vorhanden, sonst (Fassung 3) der Altbestand
alt_als_einleitung = alt_da and einl_eigen == 0

zeilen = []
csvz = []
zeilen.append('Nummerierung im Master: ' + ('Endnummern (Einleitung 1, Methodik 2 bis Fazit 5), unten als Arbeitsnummern 4 bis 7 geführt'
                                           if ENDNUMMERN else 'Arbeitsnummern (Einleitung 1, Methodik 4 bis Fazit 7)'))
zeilen.append('')
kopf = '%-8s %-8s %-48s %6s %6s %6s %5s %5s %5s %5s %5s %5s %5s' % ('Nr.', 'Arbeit', 'Abschnitt', 'Wörter', 'Richtw', 'Diff',
                                                                'Abs', 'Semi', 'Verw', 'Plh', 'Mark', '>32', '>40')
zeilen.append(kopf)
block = {}
v6 = {}
gesamt = 0
for a in abschnitte:
    nr = a['nr']
    an = arbeitsnummer(nr)
    text = ' '.join(a['absaetze'])
    w = sum(len(x.split()) for x in a['absaetze'])
    semi = ohne_zitierklammern(text).count(SEMI)
    verw = len(RE_REF.findall(text))
    mark = sum(text.count(m) for m in MARKER)
    s = [len(x.split()) for x in saetze(text)] if text else []
    s32 = sum(1 for x in s if x > 32)
    s40 = sum(1 for x in s if x > 40)
    a250 = sum(1 for x in a['absaetze'] if len(x.split()) > 250)
    ist_alt = nr in ALTBESTAND and not ENDNUMMERN
    if re.match(r'^\d', nr):
        gesamt += w
        if ist_alt:
            kb = '1' if alt_als_einleitung else 'ALT'
            kv = kb
        else:
            kb = ELTERN_BLOCK.get(an, an)
            kv = v6_schluessel(an)
        block[kb] = block.get(kb, 0) + w
        v6[kv] = v6.get(kv, 0) + w
    bud = BUDGET.get(an, '')
    diff = (w - bud) if isinstance(bud, int) and an not in ('1', '4.4') else ''
    zeilen.append('%-8s %-8s %-48s %6d %6s %6s %5d %5d %5d %5d %5d %5d %5d' % (
        nr[:8], (an if an != nr else '')[:8], a['titel'][:48], w, bud, diff, len(a['absaetze']), semi, verw,
        a['platzhalter'], mark, s32, s40))
    csvz.append(dict(nr=nr, arbeitsnummer=an, v6=('ALT' if ist_alt else v6_schluessel(an)) if re.match(r'^\d', nr) else '',
                     titel=a['titel'], woerter=w, richtwert=bud, absaetze=len(a['absaetze']),
                     semikola=semi, abschnittsverweise=verw, platzhalter=a['platzhalter'], marker=mark,
                     saetze_ueber_32=s32, saetze_ueber_40=s40, absaetze_ueber_250=a250,
                     beschriftungen=a['beschriftungen'], anmerkungen=a['anmerkungen']))

# Budgets je Abschnitt der Gliederung v6 (verbindlich, E4)
zeilen.append('')
zeilen.append('Budgets je Abschnitt der Gliederung v6 (verbindlich, E4), Schlüssel Arbeitsnummer, Endnummer ab Task 18:')
for an, en, titel, bud in V6:
    w = v6.get(an, 0)
    zus = [k for k, e in ELTERN_V6.items() if e == an and k in vorhanden]
    note = ('  (mit ' + ', '.join(zus) + ')') if zus else ''
    zeilen.append('  %-5s %-5s %-46s %6d gegen %5d  (%+d)%s' % (an, en, titel[:46], w, bud, w - bud, note))
if alt_da and not alt_als_einleitung:
    zeilen.append('  Altbestand 2, 2.x und 3 (M24 offen): %d Wörter, zusätzlich im Master, keiner Budgetzeile zugeschlagen'
                  % alt_w)

# Blockrichtwerte (Vorgabe 23.09.) innerhalb der zusammengelegten Abschnitte
zeilen.append('')
zeilen.append('Blockrichtwerte der Vorgabe (Arbeitsnummern, 4.4 = 4.4 + 4.4.1 bis 4.4.3):')
for key in BUDGET:
    if key == '1':
        continue
    gruppe = ELTERN_V6.get(key, key)
    glieder = [k for k in BUDGET if ELTERN_V6.get(k, k) == gruppe]
    # Ein Block ist im Master nur messbar, wenn alle Blöcke seines v6-Abschnitts eine eigene Überschrift tragen
    messbar = all(k in vorhanden for k in glieder) if len(glieder) > 1 else (key in vorhanden or key == '4.4')
    if messbar:
        w = block.get(key, 0)
        zeilen.append('  %-10s %6d gegen %5d  (%+d)' % (key, w, BUDGET[key], w - BUDGET[key]))
    else:
        zeilen.append('  %-10s ohne eigene Überschrift im Master, im Abschnitt %s enthalten, Richtwert %d gilt für die '
                      'Absatzgruppe im Textvorschlag' % (key, gruppe, BUDGET[key]))

k4 = sum(v6.get(k, 0) for k in ['4.1', '4.2', '4.3', '4.4', '4.5', '4.7'])
k4o = k4 - v6.get('4.7', 0)
k5 = v6.get('5', 0)
k6 = v6.get('6.1', 0) + v6.get('6.2', 0)
einl = block.get('1', 0) if alt_als_einleitung else einl_eigen
zeilen.append('')
zeilen.append('Einleitung (1%s): %d gegen 1500 (%+d)' % (', noch als Altbestand 2, 2.x und 3' if alt_als_einleitung else '',
                                                        einl, einl - 1500))
if alt_da and not alt_als_einleitung:
    zeilen.append('  Altbestand Kapitel 2 und 3 steht noch im Master: %d Wörter, zu löschen nach M24' % alt_w)
zeilen.append('Kapitel 4 (4.1 bis 4.6): %d gegen 2000 (%+d)' % (k4o, k4o - 2000))
zeilen.append('Kapitel 4 (4.1 bis 4.7): %d gegen 2550 (%+d)' % (k4, k4 - 2550))
zeilen.append('Kapitel 5: %d gegen 450 (%+d)' % (k5, k5 - 450))
zeilen.append('Kapitel 6 (6.1, 6.2 mit 6.3): %d gegen 1600 (%+d)' % (k6, k6 - 1600))
zeilen.append('Kapitel 7: %d gegen 250 (%+d)' % (v6.get('7', 0), v6.get('7', 0) - 250))
ohne_alt = gesamt - (alt_w if (alt_da and not alt_als_einleitung) else 0)
zeilen.append('Absatztext Kapitel 1 bis 7 (Arbeitsnummern): %d gegen %d (%+d)%s'
              % (ohne_alt, GESAMT, ohne_alt - GESAMT,
                 ', ohne den Altbestand' if (alt_da and not alt_als_einleitung) else ''))
if alt_da and not alt_als_einleitung:
    zeilen.append('  mit dem Altbestand, wie der Master heute steht: %d' % gesamt)
leer_v6 = [(an, en) for an, en, _, _ in V6 if v6.get(an, 0) == 0 and not (an == '1' and alt_als_einleitung)]
zeilen.append('Noch nicht geschrieben (0 Wörter, v6-Abschnitte): ' + (', '.join('%s (Endnr. %s)' % (an, en) for an, en in leer_v6) or '—'))
if alt_als_einleitung:
    zeilen.append('Einleitung: noch Altbestand, Text der Einleitung nicht im Master')
leer_an = {an for an, _ in leer_v6}
zeilen.append('Budget der ungeschriebenen Abschnitte: %d'
              % (sum(b for an, _, _, b in V6 if an in leer_an) + (1500 if alt_als_einleitung else 0)))
alle = ' '.join(x for a in abschnitte for x in a['absaetze'] if re.match(r'^\d', a['nr']))
zeilen.append('Semikola außerhalb von Zitierklammern, Kapitel 1 bis 7: %d' % ohne_zitierklammern(alle).count(SEMI))
zeilen.append('Nummerierte Abschnittsverweise, Kapitel 1 bis 7: %d' % len(RE_REF.findall(alle)))
if alt_da:
    alt = ' '.join(x for a in abschnitte for x in a['absaetze'] if a['nr'] in ALTBESTAND)
    zeilen.append('  davon im Altbestand Kapitel 2 und 3: %d Semikola, %d Abschnittsverweise'
                  % (ohne_zitierklammern(alt).count(SEMI), len(RE_REF.findall(alt))))
zeilen.append('Platzhalter ⟨…⟩ im ganzen Master: %d' % sum(a['platzhalter'] for a in abschnitte))
zeilen.append('Marker im ganzen Master: %d' % sum(sum(x.count(m) for m in MARKER) for a in abschnitte for x in a['absaetze']))

# Seitenschätzung — Modellrechnung, keine Messung
zeilen.append('')
zeilen.append('Seitenschätzung — Modellrechnung, keine Messung (Parameter aus dem Seitenmodell, Zählweise K1: Einleitung bis '
              'Ende des Literaturverzeichnisses, ohne Vorspann und Anhang)')
if not os.path.exists(SMODELL):
    zeilen.append('  Parameterdatei nicht gefunden: %s, Block entfällt' % SMODELL)
else:
    par = {r['parameter']: r for r in csv.DictReader(open(SMODELL, encoding='utf-8'), delimiter=SEMI)}
    f = lambda k: float(par[k]['wert'])
    wort = {}
    for an, en, titel, bud in V6:
        ist = einl if an == '1' else v6.get(an, 0)
        if an == '1' and alt_als_einleitung:
            wort[an] = (bud, 'Budget (Einleitung noch Altbestand)')
        elif ist > 0:
            wort[an] = (ist, 'gemessen')
        else:
            wort[an] = (bud, 'Budget (noch leer)')
    w_einl = wort['1'][0]
    w_rest = sum(v[0] for k, v in wort.items() if k != '1')
    s_text = w_einl / f('dichte_einleitung') + w_rest / f('dichte_kapitel_4_bis_7')
    s_obj = f('objekte_textteil') * f('seiten_je_objekt')
    s_end = f('kapitelenden_textteil') * f('seiten_je_kapitelende')
    textteil = s_text + s_obj + s_end
    ist_b = set()
    sek_b = set()
    for a in abschnitte:
        if re.match(r'^\d', a['nr']) and not (a['nr'] in ALTBESTAND and not ENDNUMMERN):
            g, s2 = belege(' '.join(a['absaetze']))
            ist_b |= g
            sek_b |= s2
    alle_b, _ = belege(alle)
    vollstaendig = not alt_da and not leer_v6
    eintraege = len(ist_b) if vollstaendig else max(len(ist_b), int(f('eintraege_basis')))
    s_lit = eintraege / f('eintraege_je_seite') + f('seiten_je_kapitelende')
    gesamt_s = textteil + s_lit
    zeilen.append('  Wörter: Einleitung %d (%s), Methodik bis Fazit %d (gemessen, wo geschrieben, sonst Budget)'
                  % (w_einl, wort['1'][1], w_rest))
    zeilen.append('  Text %s Seiten (Dichte %s und %s Wörter je Seite) + Objekte %s + Kapitelenden %s = Textteil %s Seiten'
                  % (de(s_text), de(f('dichte_einleitung'), 0), de(f('dichte_kapitel_4_bis_7'), 0), de(s_obj), de(s_end),
                     de(textteil)))
    zeilen.append('  Verschiedene Autor-Jahr-Belege im Master: %d in Kapitel 1 bis 7%s, %d ohne Altbestand, '
                  'Sekundärquellen ohne Eintrag: %s' % (len(alle_b), ' (mit Altbestand)' if alt_da else '', len(ist_b),
                                                        ', '.join(sorted(sek_b)) or 'keine'))
    zeilen.append('  Einträge im Modell: %d (%s) bei %s je Seite -> Literaturverzeichnis %s Seiten'
                  % (eintraege, 'gemessen' if vollstaendig else 'höherer Wert aus Ist ohne Altbestand und Basis des Seitenmodells',
                     de(f('eintraege_je_seite'), 1), de(s_lit)))
    zeilen.append('  Prognose Einleitung bis Ende Literaturverzeichnis: %s Seiten gegen die Grenze %s (Schwelle der Tauschregel %s)'
                  % (de(gesamt_s), par['grenze_verfasser']['wert'], par['schwelle_tauschregel']['wert']))
    if alt_da and not alt_als_einleitung:
        zeilen.append('  Der Altbestand ist in der Prognose nicht enthalten (M24 offen).')
    zeilen.append('  Kontrolle bleibt die Word-Messung am fertigen Dokument (F17 § 1.1).')

with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('Manuskriptstand am Master, gemessen mit Manuskriptstand_2026-09-25.py (Fassung 4)\nQuelle: %s\n\n'
             % os.path.basename(SRC))
    fh.write('\n'.join(zeilen) + '\n')
if CSV:
    with open(CSV, 'w', encoding='utf-8', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(csvz[0].keys()))
        wr.writeheader()
        wr.writerows(csvz)
print('\n'.join(zeilen))

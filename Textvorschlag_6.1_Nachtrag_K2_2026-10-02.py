# -*- coding: utf-8 -*-
"""Textvorschlag 6.1, Nachtrag K2 (Task „Boumparis“, 02.10.2026): Messung der Varianten für das Modul A2-M.

Liest den Wortlaut von 6.1 aus `Textvorschlag_6.1_2026-10-02.json` (Task 12a, unverändert), prüft ihn gegen die dort
geführten Wortzahlen, setzt je Variante den Vergleichssatz nach A2 S2 ein, ändert den Anfang von A2 S3 je Variante
(A: „Der Schätzer ist durch die eigene Umsetzung stark verdünnt“, B: „Der eigene Schätzer ist damit stark verdünnt“),
wendet Stufe 1 der Kürzungsleiter an (A3 S8, Liu et al., 2024, −30), misst zusätzlich die Satzkerne für die
Folgetasks (Fassung 2 nach der Zweitprüfung) und misst wie das Messskript Fassung 4 und das Skript des Textvorschlags 6.1: Wörter als Leerraum-Token,
Satzteilung saetze(), Semikola außerhalb von Zitierklammern, nummerierte Abschnittsverweise, Verbotswörter,
Satz- und Absatzgrenzen. Ausgabe: .txt (Messprotokoll) und .json (Wortlaut je Variante, A2 vollständig).
Funktionen saetze(), ohne_zitierklammern(), belegklammern(), RE_REF und VERBOTEN wörtlich aus
`Textvorschlag_6.1_2026-10-02.py` übernommen. Ohne Semikolon im Skript (chr(59)).

Aufruf: python3 Textvorschlag_6.1_Nachtrag_K2_2026-10-02.py <Textvorschlag_6.1_2026-10-02.json> [Ausgabeordner]
"""
import json
import os
import re
import statistics
import sys

SEMI = chr(59)
BUDGET = 700

# Varianten nach der Zweitprüfung (Nr. 4, 9, 16): A mit Streuung (Empfehlung), B ohne „Auch“ und ohne gemeinsames
# Subjekt. Je Variante der Anschluss in A2 S3, damit „verdünnt“ an die eigene Umsetzung bindet.
VARIANTEN = {
    'A': ('Auch in digitalen Lebensstilprogrammen für Jugendliche wurde nach einer systematischen Übersicht im Mittel '
          'nur gut die Hälfte der Programmbestandteile absolviert, bei großer Streuung (Boumparis et al., 2026).'),
    'B': ('In digitalen Lebensstilprogrammen für Jugendliche blieben nach einer systematischen Übersicht die meisten in '
          'der Studie, absolviert wurde im Mittel nur gut die Hälfte der Programmbestandteile (Boumparis et al., 2026).'),
}
S3_ALT = 'Der Schätzer ist damit stark verdünnt:'
S3_NEU = {'A': 'Der Schätzer ist durch die eigene Umsetzung stark verdünnt:',
          'B': 'Der eigene Schätzer ist damit stark verdünnt:'}
# Satzkerne für die Folgetasks (Nachtrag § 2, Nr. 3 bis 8), gemessen wie die Varianten
SATZKERNE = [
    ('Nr. 3 (6.3 G3, Klusemann)', 'In einer kontrollierten Studie mit Nachwuchsbasketballspielern absolvierte die '
     'Videogruppe eines sechswöchigen Krafttrainings mit zwölf Einheiten nach Online-Tagebuch gut drei Viertel davon, '
     'die betreute Gruppe fast alle (Klusemann et al., 2012).'),
    ('Nr. 4 (6.3 G3, nur bei A oder Verzicht)', 'Auch in digitalen Lebensstilprogrammen für Jugendliche überschätzte '
     'nach einer systematischen Übersicht der Verbleib in der Studie die tatsächliche Nutzung (Boumparis et al., 2026).'),
    ('Nr. 5 (6.3 Stärken oder G6)', 'Die Umsetzung wurde mit Definition als Anteil vollständig gemeldeter Einheiten '
     'und als Verteilung je Spieler berichtet, wie es eine systematische Übersicht zu digitalen Lebensstilprogrammen '
     'für Jugendliche empfiehlt (Boumparis et al., 2026).'),
    ('Nr. 6 (6.3 G6)', 'Objektive Nutzungsdaten der Videos und Gründe für nicht durchgeführte Einheiten wurden nicht '
     'erfasst, der Trainingstag nur über den Meldezeitpunkt. Wie genau die Selbstauskunft die Durchführung abbildet, '
     'bleibt offen.'),
    ('Nr. 7 (Kapitel 7, ohne Quelle)', 'Künftige Studien sollten die Umsetzung unbeaufsichtigter Heimprogramme als '
     'Anteil absolvierter Einheiten und als Anteil der Spieler mit vollständigem Programm berichten, jeweils mit '
     'Definition. Dazu gehören objektive Nutzungsdaten und die Gründe ausgelassener Einheiten. Welche Merkmale der '
     'Vermittlung die Umsetzung unbeaufsichtigter Heimprogramme im Nachwuchssport erhöhen, wäre experimentell zu prüfen.'),
    ('Nr. 8 (Einleitung Abs. 3, Vormerkung)', 'Jugendliche nutzten digitale Lebensstilprogramme nach einer '
     'systematischen Übersicht allerdings im Mittel nur teilweise (Boumparis et al., 2026).'),
    ('Alternative Lücke Abs. 5 (nicht empfohlen)', 'Wie weit Spieler ein solches Programm ohne Aufsicht umsetzen, ist '
     'ebenso offen.'),
]
STUFE1_BEGINN = 'In der einzigen kontrollierten Studie zur Übergangsperiode mit plyometrischem Arm'
STUFE1_WOERTER = 30

RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')


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


def ohne_zitierklammern(text):
    return re.sub(r'\([^)]*\d{4}[^)]*\)', '', text)


def belegklammern(text):
    return re.findall(r'\([^()]*?\d{4}[^()]*?\)', text)


VERBOTEN = [
    'randomisiert', 'randomized', 'kein Effekt', 'wirkungslos', 'gleich wirksam', 'Erhalt', 'Schutz vor',
    'ITT', 'sodass', 'weshalb', 'im Rahmen', 'Gegenstand der Untersuchung', 'es ist festzuhalten',
    'darüber hinaus', 'des Weiteren', 'hierbei gilt', 'Responder', 'signifikant', 'adressiert', 'beseitigt',
    'Wirkung des Programms', 'Wirkung des Trainings', 'profitier', 'klein', 'moderat', 'groß', 'trivial',
    'MDES', 'Power', 'Familienfehler', 'genuinely', 'Abschn.', 'siehe oben', 'siehe unten',
]
# Zusätzlich für diesen Nachtrag (Prompt § 3.2 Nr. 1 und Nr. 6): Wertungen, die die Übersicht nicht trägt,
# und Wörter, die eine Norm oder Ursache nahelegen
WERTUNG = ['typisch', 'gering', 'niedrig', 'deutlich darunter', 'Norm', 'Zielmarke', 'wegen', 'weil', 'Metaanalyse']


def pruefe(text):
    befunde = []
    for v in VERBOTEN:
        if v == 'groß':
            if re.search(r'\bgroß(?:e|er|es)?\s+(?:Effekt|Unterschied)', text):
                befunde.append('Etikett „groß“')
            continue
        if v == 'klein':
            if re.search(r'\bklein(?:e|er|es)?\s+(?:Effekt|Unterschied)', text):
                befunde.append('Etikett „klein“')
            continue
        if v == 'ITT':
            if re.search(r'\bITT\b', text):
                befunde.append('Verbotswort „ITT“')
            continue
        if v.lower() in text.lower():
            befunde.append('Verbotswort „%s“' % v)
    if SEMI in ohne_zitierklammern(text):
        befunde.append('Semikolon außerhalb einer Zitierklammer')
    if RE_REF.search(text):
        befunde.append('nummerierter Abschnittsverweis')
    for s in saetze(text):
        if len(s.split()) > 32:
            befunde.append('Satz über 32 Wörter: „%s…“' % ' '.join(s.split()[:6]))
    if len(text.split()) > 250:
        befunde.append('Absatz über 250 Wörter')
    return befunde


def wertungen(text):
    return [w for w in WERTUNG if re.search(r'\b' + re.escape(w), text, flags=re.IGNORECASE)]


def main():
    quelle = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
    j = json.load(open(quelle, encoding='utf-8'))
    absaetze = {a['kennung']: a for a in j['absaetze']}
    reihe = [a['kennung'] for a in j['absaetze'] if str(a['modul']) != 'True']
    zeilen = ['Textvorschlag 6.1, Nachtrag K2 — Messprotokoll (02.10.2026, Zählung wie Messskript Fassung 4)', '']
    # Ausgangsstand gegen die JSON prüfen
    basis = 0
    for k in reihe:
        w = len(absaetze[k]['text'].split())
        assert w == int(absaetze[k]['woerter']), (k, w)
        basis += w
    assert basis == BUDGET, basis
    zeilen.append('Ausgangsstand (JSON Task 12a): %s = %d Wörter ohne Modul, Modul A2-M alt %d Wörter'
                  % (' + '.join('%s %s' % (k, absaetze[k]['woerter']) for k in reihe), basis,
                     len(absaetze['A2-M']['text'].split())))
    # Stufe 1 der Kürzungsleiter
    a3 = saetze(absaetze['A3']['text'])
    s8 = [s for s in a3 if s.startswith(STUFE1_BEGINN)]
    assert len(s8) == 1 and a3.index(s8[0]) == 7, 'A3 S8 nicht gefunden'
    assert len(s8[0].split()) == STUFE1_WOERTER, len(s8[0].split())
    a3_neu = ' '.join(a3[:7])
    zeilen.append('Stufe 1: A3 S8 gestrichen (%d Wörter): „%s…“' % (STUFE1_WOERTER, ' '.join(s8[0].split()[:8])))
    # A2 zerlegen
    a2 = saetze(absaetze['A2']['text'])
    assert len(a2) == 5 and a2[2].startswith(S3_ALT), a2[2][:40]
    zeilen.append('Ausgangsstand A2 S3: „%s“ (%d Wörter)' % (a2[2], len(a2[2].split())))
    ergebnis = {'quelle': os.path.basename(quelle), 'stufe1_gestrichen': s8[0], 'varianten': {}}
    for name in ('A', 'B', 'Verzicht'):
        if name == 'Verzicht':
            a2_neu = absaetze['A2']['text']
            texte = {k: absaetze[k]['text'] for k in reihe}
            modul = ''
        else:
            modul = VARIANTEN[name]
            a2_neu = ' '.join([a2[0], a2[1], modul, a2[2].replace(S3_ALT, S3_NEU[name], 1), a2[3], a2[4]])
            texte = {k: absaetze[k]['text'] for k in reihe}
            texte['A2'] = a2_neu
            texte['A3'] = a3_neu
        summe = sum(len(texte[k].split()) for k in reihe)
        alle = ' '.join(texte[k] for k in reihe)
        sl = [len(s.split()) for k in reihe for s in saetze(texte[k])]
        quellen = sorted(set(re.findall(r'([A-ZÄÖÜ][A-Za-zäöüß\-]+(?: et al\.| & [A-ZÄÖÜ][a-zäöüß]+)?), (\d{4})', alle)))
        zeilen.append('')
        zeilen.append('Variante %s%s' % (name, '' if name == 'Verzicht' else ' (Modul nach A2 S2, A2 S3 „%s“, Stufe 1)' % S3_NEU[name]))
        if modul:
            ms = saetze(modul)
            zeilen.append('  Modul: %d Wörter, %d Satz, Belegklammern %d, Wertungswörter: %s'
                          % (len(modul.split()), len(ms), len(belegklammern(modul)),
                             ', '.join(wertungen(modul)) or 'keine'))
            zeilen.append('  Modul + Anschluss S3: %d Wörter' % (len(modul.split()) + len(S3_NEU[name].split()) - len(S3_ALT.split())))
        for k in reihe:
            ss = saetze(texte[k])
            l = [len(s.split()) for s in ss]
            zeilen.append('  %s: %d Wörter, %d Sätze, Median %.1f, längster %d' % (
                k, len(texte[k].split()), len(ss), statistics.median(l), max(l)))
            for b in pruefe(texte[k]):
                zeilen.append('     BEFUND: ' + b)
        zeilen.append('  Summe 6.1: %d Wörter (Budget %d, Rest %d)%s' % (summe, BUDGET, BUDGET - summe,
                      '' if summe <= BUDGET else ' — ÜBER BUDGET'))
        zeilen.append('  Sätze %d, Median %.1f, längster %d · Semikola außerhalb von Zitierklammern %d · '
                      'Abschnittsverweise %d · Belegklammern %d · Quellen %d'
                      % (len(sl), statistics.median(sl), max(sl), ohne_zitierklammern(alle).count(SEMI),
                         len(RE_REF.findall(alle)), len(belegklammern(alle)), len(quellen)))
        zeilen.append('  Quellen: ' + ', '.join('%s (%s)' % q for q in quellen))
        ergebnis['varianten'][name] = {'modul': modul, 'A2': a2_neu, 'A3': texte['A3'], 'summe': summe,
                                       'saetze': len(sl), 'median': statistics.median(sl), 'laengster': max(sl)}
        assert summe <= BUDGET, (name, summe)
    zeilen.append('')
    zeilen.append('Satzkerne für die Folgetasks (Nachtrag § 2), Wörter je Satz und gesamt:')
    ergebnis['satzkerne'] = {}
    for name, text in SATZKERNE:
        ss = saetze(text)
        l = [len(x.split()) for x in ss]
        bef = pruefe(text) + ['Wertung „%s“' % w for w in wertungen(text)]
        zeilen.append('  %s: %s = %d Wörter, längster Satz %d%s' % (name, ' + '.join(str(x) for x in l), sum(l), max(l),
                      (' · BEFUND: ' + ', '.join(bef)) if bef else ''))
        ergebnis['satzkerne'][name] = {'text': text, 'woerter_je_satz': l}
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'Textvorschlag_6.1_Nachtrag_K2_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(zeilen) + '\n')
    with open(os.path.join(out, 'Textvorschlag_6.1_Nachtrag_K2_2026-10-02.json'), 'w', encoding='utf-8') as f:
        json.dump(ergebnis, f, ensure_ascii=False, indent=1)
    print('\n'.join(zeilen))


if __name__ == '__main__':
    main()

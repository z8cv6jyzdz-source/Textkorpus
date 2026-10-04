# -*- coding: utf-8 -*-
"""
nachtrag_T1_T4.py — Schritt 4 des Tasks „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (30.09.2026)

Trägt vor der Belegtabelle zu B4 die Vormerkungen aus Textvorschlag B4 § 5 (Tanner1966) und Textvorschlag B3 bis B5 § 7
(Radnor2017, Begriffe „children“ und „youth“) in T1 und T4 nach und berichtigt in T1 die Zeile Roessler2014:
Ihr Feld „kapitel“ enthielt ein ungeschütztes Semikolon und zerfiel in zwei Felder (16 statt 15), der Inhalt stand noch
auf dem Klick vom 28.09. und wird auf das Register vom 29.09., 06:40 nachgeführt (Vormerkung Textvorschlag Überarbeitung § 1.8).
Alle Angaben am PDF geprüft (Tanner et al., 1966: Scan mit Textschicht, MD5 c63022b5…, S. 454, 457, 461, 465, Tab. I am
Seitenbild · Radnor et al., 2018: Online-First, MD5 395ea66f…, OF-S. 1 und 2), Heftangaben von Tanner bei PubMed (PMID 5957718).

Bestehende Zeilen bleiben byte-gleich (geprüft), neue Zeilen im Stil der Dateien: Semikolon als Trenner, Anführungszeichen
nur bei Bedarf, UTF-8 mit BOM, LF. Liest die Dateien aus dem Staging-Pfad oder aus den Pfaden der Argumente, prüft die MD5 der
Eingaben und schreibt nach AUS (Standard: Unterordner ev3_daten neben dem Skript). Ohne Semikolon im Skript (chr(59)).
Aufruf: python nachtrag_T1_T4.py [<Ordner ev3_daten>] [<Ausgabeordner>]
"""
import csv, hashlib, io, os, sys

SEMI = chr(59)
HIER = os.path.dirname(os.path.abspath(__file__))
EIN = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/Bachelorarbeit/Schreiben/ev3_daten'
AUS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HIER, 'ev3_daten')
MD5_VORHER = {'T1_steckbriefe.csv': 'ff015c061061ede7cf50bcbc9afd12f9', 'T4_zitierfallen.csv': '1bf90f1da185639cd4c0b1db0487dee9'}
BOM = b'\xef\xbb\xbf'


def md5(b):
    return hashlib.md5(b).hexdigest()


def zeile(felder):
    puffer = io.StringIO()
    csv.writer(puffer, delimiter=SEMI, quoting=csv.QUOTE_MINIMAL, lineterminator='\n').writerow(felder)
    return puffer.getvalue()


def lies(name):
    b = open(os.path.join(EIN, name), 'rb').read()
    assert md5(b) == MD5_VORHER[name], name + ': Eingabe weicht vom geprüften Stand ab'
    assert b.startswith(BOM) and b.count(b'\r\n') == 0 and b.endswith(b'\n'), name + ': Format unerwartet'
    return b[len(BOM):].decode('utf-8')


# ---------- T1 ----------
t1 = lies('T1_steckbriefe.csv')
t1_zeilen = t1.split('\n')[:-1]
kopf1 = next(csv.reader([t1_zeilen[0]], delimiter=SEMI))
assert len(kopf1) == 15

ROESSLER_KAPITEL = ('1 (Einleitung, B1b S7: nur Mitzitation neben Olivier et al., 2026, ohne Population und ohne '
                    'Vor-2020-Halbsatz, Register 29.09., 06:40. Löst den Klick 1 vom 28.09. ab, der den Sprungbefund als '
                    'Zwischen-Studien-Vergleich mit Population „überwiegend Spielerinnen“ und Vor-2020-Halbsatz vorsah)')
neu1 = []
geaendert1 = []
for i, z in enumerate(t1_zeilen):
    f = next(csv.reader([z], delimiter=SEMI))
    if f[0] == 'Roessler2014':
        assert len(f) == 16 and f[14].startswith('1 (Klick 1, 28.09.') and f[15].strip().startswith('Einleitung, Task 7 neu')
        f = f[:14] + [ROESSLER_KAPITEL]
        neu1.append(zeile(f).rstrip('\n'))
        geaendert1.append(i + 1)
    else:
        neu1.append(z)

TANNER_T1 = [
    'Tanner1966',
    'Tanner et al. (1966)',
    'Tanner, J. M., Whitehouse, R. H., & Takaishi, M. (1966). Standards from birth to maturity for height, weight, height '
    'velocity, and weight velocity: British children, 1965. Part I. Archives of Disease in Childhood, 41(219), 454–471. '
    'https://doi.org/10.1136/adc.41.219.454',
    'Verlagsfassung als Scan mit Textschicht (PMC2019592), Heftangaben und DOI bei PubMed geprüft 30.09.2026 (PMID 5957718). '
    'Volltext ✓ 29.09.2026, Tab. I am Seitenbild geprüft 30.09.2026. Zitiert wird Part I, Literatur und Anhänge stehen in '
    'Part II (Fußnote S. 454)',
    'BMJ (Archives of Disease in Childhood) — kein MDPI',
    'Wachstumsstandards von der Geburt bis zur Reife. Individuelle Kurven des Wachstumsschubs aus dem Längsschnitt der '
    'Harpenden Growth Study (im Schub dreimonatlich gemessen, S. 457), Distanzstandards aus Querschnittsdaten',
    '49 gesunde britische Jungen und 41 Mädchen der Harpenden Growth Study, die in einem Kinderheim lebten (S. 457, S. 465)',
    'Kernthema: Alter beim Wachstumsgipfel, Jungen 14,1 ± 0,13 Jahre (Mittelwert ± Standardfehler), SD 0,93, Spanne '
    '12,0–16,0 · Mädchen 12,1 ± 0,14, SD 0,87, Spanne 10,5–13,5 (Tab. I, S. 461). Im Standard um 0,2 Jahre vorverlegt, '
    'Jungen 13,9 (S. 465)',
    'nicht anwendbar',
    'nicht anwendbar',
    'Konzept- und Standardquelle (E3), keine Wirksamkeit. Einzelbefund, Population im Satz nennen (F17 § 6.4). Stichprobe '
    'aus einem Kinderheim, Menarche etwas später als bei Londoner Schulkindern (S. 465). Die Standards halten die Autoren für '
    'repräsentativ für städtische Kinder Südenglands in den frühen 1960er Jahren (S. 465), den Messzeitraum der Harpenden '
    'Growth Study nennt Part I nicht. Deming (1957, Denver) rund ein halbes Jahr früher, nach den Autoren wohl '
    'sozioökonomisch und ernährungsbedingt (S. 461). Kein Vor-2020-Halbsatz (Standardreferenz, F17 § 6.2)',
    '1',
    '—',
    '—',
    '1 (Einleitung, Zug Reifung: Alter beim Wachstumsgipfel, Register 29.09., 17:12, ersetzt Malina & Kozieł, 2014)',
]
assert len(TANNER_T1) == 15
assert not any(r.startswith('Tanner1966' + SEMI) for r in t1_zeilen)
neu1.append(zeile(TANNER_T1).rstrip('\n'))
t1_neu = '\n'.join(neu1) + '\n'

# ---------- T4 ----------
t4 = lies('T4_zitierfallen.csv')
t4_zeilen = t4.split('\n')[:-1]
assert next(csv.reader([t4_zeilen[0]], delimiter=SEMI)) == ['quelle_id', 'art', 'befund_und_konsequenz']
assert not any(r.startswith('Tanner1966' + SEMI) for r in t4_zeilen)
T4_NEU = [
    ['Tanner1966', 'Tab. I: Standardfehler statt SD / Geschlecht',
     'Tab. I (S. 461): Alter beim Wachstumsgipfel Jungen 14,1 ± 0,13 Jahre ist Mittelwert ± Standardfehler, die SD beträgt '
     '0,93, die Spanne 12,0–16,0. Mädchen 12,1 ± 0,14, SD 0,87, Spanne 10,5–13,5. Nie „± 0,13“ als Streuung zitieren. '
     'Den Gipfel mit rund 14 Jahren trägt die Quelle nur für Jungen, nicht für „Jugendliche“. [Nachgetragen 30.09.2026, '
     'am Seitenbild geprüft]'],
    ['Tanner1966', 'Stichprobe / Standard / Fassung',
     'Die 49 Jungen und 41 Mädchen der Harpenden Growth Study lebten in einem Kinderheim (S. 457, S. 465). Weil die '
     'Menarche dort etwas später lag als bei Londoner Schulkindern, verlegten die Autoren das Alter beim Gipfel im Standard '
     'um 0,2 Jahre vor, auf 13,9 Jahre bei Jungen (S. 465). Die Denver-Kinder von Deming (1957) erreichten den Gipfel rund '
     'ein halbes Jahr früher, nach den Autoren wohl sozioökonomisch und ernährungsbedingt (S. 461). „14 Jahre“ deckt beide '
     'Werte. Zitiert wird Part I (S. 454–471), Literatur und Anhänge stehen in Part II (Fußnote S. 454). Einzelbefund: '
     'Population im Satz nennen (F17 § 6.4). [Nachgetragen 30.09.2026, am PDF geprüft]'],
    ['Radnor2017', 'Begriffe „children“, „adolescents“, „youth“ / Sprint nur im Abstract / Modalität',
     'Operational Definitions (OF-S. 2): „children“ meint Mädchen bis etwa 11 und Jungen bis etwa 13 Jahre ohne sekundäre '
     'Geschlechtsmerkmale, „adolescents“ Mädchen 12–18 und Jungen 14–18 Jahre, „youth“ umfasst beide. Aussagen über '
     '„children“ nicht auf U15-Spieler übertragen, „youth“ als „Kinder und Jugendliche“ wiedergeben. Die Definition „Natural '
     'development“ (OF-S. 2) spricht von „children“, für Kindheit und Jugend tragen Abstract („throughout childhood and '
     'adolescence“, OF-S. 1) und Schluss (OF-S. 11). Den altersbedingten Anstieg der Sprintleistung nennen nur Abstract und '
     'Key Points (OF-S. 1), Hauptteil (OF-S. 2) und Schluss (OF-S. 11) nennen Hüpfen und Springen (Quellenraster Zeile 5.2). '
     'Abstract und Schluss formulieren die verbesserte DVZ-Funktion indikativ, nur die Key Points modal („may result in an '
     'improved SSC function“), die Mechanismen der DVZ-Entwicklung nennen die Autoren ungeklärt („remain unclear“, OF-S. 1). '
     'Im Text modal nach F17 § 10, nicht wegen der Quelle. [Nachgetragen 30.09.2026 nach Textvorschlag B3 bis B5 § 7, am '
     'PDF geprüft]'],
]
t4_neu = t4 + ''.join(zeile(f) for f in T4_NEU)

# ---------- Prüfungen ----------
p1 = list(csv.reader(t1_neu.split('\n')[:-1], delimiter=SEMI))
p4 = list(csv.reader(t4_neu.split('\n')[:-1], delimiter=SEMI))
assert all(len(r) == 15 for r in p1), 'T1: Spaltenzahl'
assert all(len(r) == 3 for r in p4), 'T4: Spaltenzahl'
alt1 = t1.split('\n')[:-1]
gleich1 = sum(1 for a, b in zip(alt1, t1_neu.split('\n')[:-1]) if a == b)
assert gleich1 == len(alt1) - len(geaendert1)
assert t4_neu.startswith(t4)
assert SEMI not in open(os.path.abspath(__file__), encoding='utf-8').read()

os.makedirs(AUS, exist_ok=True)
open(os.path.join(AUS, 'T1_steckbriefe.csv'), 'wb').write(BOM + t1_neu.encode('utf-8'))
open(os.path.join(AUS, 'T4_zitierfallen.csv'), 'wb').write(BOM + t4_neu.encode('utf-8'))

bericht = [
    'Nachtrag T1 und T4 (30.09.2026, Schritt 4 vor B4)',
    '',
    'T1: %d Steckbriefe vorher, %d nachher (neu: Tanner1966). Zeile %s (Roessler2014) berichtigt: 16 → 15 Felder, '
    '„kapitel“ nach Register 29.09., 06:40. Übrige Zeilen byte-gleich: %d von %d.' % (
        len(alt1) - 1, len(p1) - 1, ', '.join(str(x) for x in geaendert1), gleich1, len(alt1)),
    'T4: %d Einträge vorher, %d nachher (neu: Tanner1966 zweimal, Radnor2017 einmal). Bestehende Zeilen byte-gleich.' % (
        len(t4_zeilen) - 1, len(p4) - 1),
    'MD5 vorher: T1 %s · T4 %s' % (MD5_VORHER['T1_steckbriefe.csv'], MD5_VORHER['T4_zitierfallen.csv']),
    'MD5 nachher: T1 %s · T4 %s' % (md5(BOM + t1_neu.encode('utf-8')), md5(BOM + t4_neu.encode('utf-8'))),
    '',
    'Neue oder geänderte Zeilen:',
]
for r in p1:
    if r[0] in ('Tanner1966', 'Roessler2014'):
        bericht.append('T1 ' + r[0] + ' | kapitel: ' + r[14])
for r in p4[len(t4_zeilen):]:
    bericht.append('T4 ' + r[0] + ' | ' + r[1])
open(os.path.join(HIER, 'nachtrag_T1_T4.txt'), 'w', encoding='utf-8').write('\n'.join(bericht) + '\n')
print('\n'.join(bericht))

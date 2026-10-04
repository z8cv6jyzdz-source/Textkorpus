# -*- coding: utf-8 -*-
"""
T4_Nachtrag_Aloui2022_2026-10-01.py — Berichtigung des T4-Eintrags `Aloui2022` vom 30.09.2026
Bachelorarbeit U15-Plyometrie · DSHS Köln · Folgeauftrag des Verfassers vom 01.10.2026, 07:42 Sitzungsuhr (Rev. 138)

Anlass: Der Verfasser wies darauf hin, dass „less than 8 weeks“ bei Aloui et al. (2022) gedeckt ist, weil Markovic & Mikulic
(2010) kurzfristiges Training als 6 bis 15 Wochen fassen. Punkt (5) des Eintrags vom 30.09. war damit zu streng. Bei der
Nachprüfung fiel ein zweiter eigener Fehler auf: Wiederholte Sprints standen „ohne Begründung“, sie sind aber vorbereitet.
Dazu am 01.10. gelesen: Wang & Zhang (2016), PMC4950532, narrative Übersicht.

Geändert wird nur der Text des Eintrags `Aloui2022` mit der Art vom 30.09., in fünf benannten Stellen. Jede alte Stelle muss
genau einmal vorkommen. Alle übrigen Bytes der Datei bleiben gleich (geprüft), die Zahl der Einträge bleibt 152.
Aufruf: python T4_Nachtrag_Aloui2022_2026-10-01.py <T4_zitierfallen.csv> <Ausgabe.csv>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import csv
import io
import hashlib

SRC, OUT = sys.argv[1:3]
SEMI = chr(59)
roh_bytes = open(SRC, 'rb').read()
roh = roh_bytes.decode('utf-8-sig')
zeilen = list(csv.reader(io.StringIO(roh), delimiter=SEMI))
ID = 'Aloui2022'
ART = 'Einleitung als Belegquelle ungeeignet / Lücke ohne Abgrenzung / Unabhängigkeit von Aloui et al. (2021) offen'
treffer = [i for i, z in enumerate(zeilen) if z and z[0] == ID and len(z) > 1 and z[1] == ART]
if len(treffer) != 1:
    raise SystemExit('Eintrag nicht genau einmal gefunden (%d), nichts geändert' % len(treffer))
alt = zeilen[treffer[0]][2]
if 'berichtigt 01.10.2026' in alt:
    raise SystemExit('Berichtigung besteht schon, nichts geändert')

ERSATZ = [
    ('Kopf: Prüfumfang',
     'Einleitung (S. 1–2) am 30.09.2026 an 10 der 38 zitierten Arbeiten geprüft: ',
     'Einleitung (S. 1–2) am 30.09.2026 an 10 der 38 zitierten Arbeiten geprüft, am 01.10.2026 dazu Wang & Zhang (2016): '),
    ('Kopf: PMC-Liste',
     '(Hammami et al., 2020, PMC7663380 · Aloui et al., 2021, PMC8508367)',
     '(Hammami et al., 2020, PMC7663380 · Aloui et al., 2021, PMC8508367 · Wang & Zhang, 2016, PMC4950532, narrative Übersicht)'),
    ('Punkt (4): Herkunft der Formel',
     'dort moderierte das Alter den CMJ-Zuwachs (ab 16 Jahren ES 1,28, darunter 0,38). ',
     'dort moderierte das Alter den CMJ-Zuwachs (ab 16 Jahren ES 1,28, darunter 0,38). Sinngemäß steht die Formel im Schluss '
     'von Wang & Zhang (2016, Abschnitt 4), mit Sprint, Agilität und vertikalem Sprung „in male and female individuals at any '
     'age, whether in recreational or professional athletes“, an dieser Stelle von Aloui nicht zitiert. '),
    ('Punkt (5): Dauer gedeckt, Übungsmix nicht',
     '(5) „less than 8 weeks, bilateral jumping coupled with unilateral drills“ steht nicht bei Markovic & Mikulic (2010), '
     'kurzfristig heißt dort 6 bis 15 Wochen (S. 860), Wang & Zhang (2016) nicht geprüft. ',
     '(5) „even in a short duration of less than 8 weeks, bilateral jumping coupled with unilateral drills enhanced performance“: '
     'Die Dauer ist gedeckt. Kurzfristig heißt bei Markovic & Mikulic (2010) zwei bis drei Einheiten je Woche über 6 bis '
     '15 Wochen (S. 860), Zuwächse nach 4 bis 6 Wochen führen sie etwa auf S. 882 f. und 885 an, Wang & Zhang (2016) nennen '
     'sechswöchige Programme. Die Verbindung beid- und einbeiniger Sprünge steht in keiner der beiden Quellen. Sie beschreibt '
     'Alouis eigenes Programm (Hürdensprünge, Bouncy Strides, einbeinige Hops, S. 3). '),
    ('Lücke und wiederholte Sprints',
     'Beide kombinierten Plyometrie und Sprints mit Richtungswechsel über acht Wochen zweimal wöchentlich. Wiederholte Sprints '
     'und Gleichgewicht stehen ohne Begründung und ohne Hypothese. ',
     'Beide kombinierten Plyometrie und Sprints mit Richtungswechsel über acht Wochen zweimal wöchentlich. „the least '
     'scientifically investigated combination training mode than the others mentioned previously“ widerspricht der eigenen '
     'Aufzählung (S. 2: drei Studien zu Plyometrie und Sprint, eine zu Schlitten, zwei zu Gleichgewicht und Plyometrie). '
     'Wiederholte Sprints sind vorbereitet (S. 1 „repeatedly sprint“, S. 2 Kargarfard et al., 2020, nach dem Titel, und '
     'Hammami et al., 2020, „repeated change-of-direction ability“), Gleichgewicht nur als Bestandteil anderer '
     'Kombinationsprogramme (S. 2). Beide fehlen in der Hypothese. '),
    ('Herkunftsvermerk',
     '[Nachgetragen 30.09.2026, Einleitung am PDF geprüft (MD5 ccc022fe…), Belege wie oben]',
     '[Nachgetragen 30.09.2026, Einleitung am PDF geprüft (MD5 ccc022fe…), Belege wie oben · berichtigt 01.10.2026 nach '
     'Hinweis des Verfassers: (5) Dauer gedeckt, wiederholte Sprints vorbereitet, Wang & Zhang (2016) gelesen, Aufzählung zur '
     'Lücke ergänzt]'),
]
neu_text = alt
for name, a, n in ERSATZ:
    if neu_text.count(a) != 1:
        raise SystemExit('Stelle nicht genau einmal gefunden: ' + name)
    assert SEMI not in n and '"' not in n and '\n' not in n, name
    neu_text = neu_text.replace(a, n, 1)


def zeile(felder):
    buf = io.StringIO()
    csv.writer(buf, delimiter=SEMI, quoting=csv.QUOTE_MINIMAL, lineterminator='\n').writerow(felder)
    return buf.getvalue().encode('utf-8')


alt_b = zeile([ID, ART, alt])
neu_b = zeile([ID, ART, neu_text])
if roh_bytes.count(alt_b) != 1:
    raise SystemExit('Zeile nicht byte-gleich wiedergefunden, nichts geändert')
pos = roh_bytes.index(alt_b)
neu_bytes = roh_bytes[:pos] + neu_b + roh_bytes[pos + len(alt_b):]
with open(OUT, 'wb') as f:
    f.write(neu_bytes)

# Prüfungen: alles vor und nach der Zeile byte-gleich, Zahl der Einträge gleich, übrige Einträge gleich, drei Felder je Zeile
pruef = open(OUT, 'rb').read()
assert pruef[:pos] == roh_bytes[:pos] and pruef[pos + len(neu_b):] == roh_bytes[pos + len(alt_b):], 'Bestand verändert'
zeilen_neu = list(csv.reader(io.StringIO(pruef.decode('utf-8-sig')), delimiter=SEMI))
assert len(zeilen_neu) == len(zeilen), 'Zeilenzahl'
assert all(len(z) == 3 for z in zeilen_neu), 'Feldzahl'
assert all(zeilen_neu[i] == zeilen[i] for i in range(len(zeilen)) if i != treffer[0]), 'andere Einträge verändert'
assert zeilen_neu[treffer[0]] == [ID, ART, neu_text], 'neuer Eintrag'
print('Eingabe: %d Byte, MD5 %s' % (len(roh_bytes), hashlib.md5(roh_bytes).hexdigest()))
print('Ausgabe: %d Byte, MD5 %s' % (len(pruef), hashlib.md5(pruef).hexdigest()))
print('T4: %d Einträge ohne Kopfzeile (unverändert), Eintrag %s in Zeile %d berichtigt' % (len(zeilen_neu) - 1, ID, treffer[0] + 1))
print('Einträge %s: %d' % (ID, sum(1 for z in zeilen_neu[1:] if z[0] == ID)))
for name, a, n in ERSATZ:
    print('  ersetzt: %s (%d -> %d Zeichen)' % (name, len(a), len(n)))
print('Text: %d -> %d Zeichen, Bestand außerhalb der Zeile byte-gleich' % (len(alt), len(neu_text)))

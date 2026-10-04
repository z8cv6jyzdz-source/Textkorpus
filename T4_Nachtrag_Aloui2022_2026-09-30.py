# -*- coding: utf-8 -*-
"""
T4_Nachtrag_Aloui2022_2026-09-30.py — Zitierfalle zur Einleitung von Aloui et al. (2022) in T4 nachtragen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Prüfung der Einleitung von Aloui et al. (2022), Auftrag 30.09., 20:29 Sitzungsuhr,
Klick „Ja, eintragen“ (Rev. 136)

Anlass: Der Verfasser fand die Einleitung von Aloui et al. (2022) ansprechend und bat um Prüfung. Geprüft wurden am 30.09.2026
10 der 38 dort zitierten Arbeiten: vier Volltexte im Ordner (Stølen et al., 2005 · Markovic & Mikulic, 2010 · Beato et al., 2018 ·
Ramirez-Campillo et al., 2020, Manuskriptfassung), zwei PMC-Volltexte (Hammami et al., 2020 · Aloui et al., 2021) und vier
PubMed-Abstracts (Hammami et al., 2019 · Andrade et al., 2018 · Ramirez-Campillo, Sanchez-Sanchez, et al., 2020 ·
Ramirez-Campillo et al., 2021, Volleyball). Der Eintrag wird angehängt, bestehende Zeilen bleiben unverändert (geprüft).
Aufruf: python T4_Nachtrag_Aloui2022_2026-09-30.py <T4_zitierfallen.csv> <Ausgabe.csv>
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
if any(z and z[0] == ID and z[1] == ART for z in zeilen):
    raise SystemExit('Eintrag besteht schon, nichts geändert')
TEXT = (
    'Einleitung (S. 1–2) am 30.09.2026 an 10 der 38 zitierten Arbeiten geprüft: Volltexte im Ordner (Stølen et al., 2005 · '
    'Markovic & Mikulic, 2010 · Beato et al., 2018 · Ramirez-Campillo et al., 2020, Manuskriptfassung), PMC-Volltexte '
    '(Hammami et al., 2020, PMC7663380 · Aloui et al., 2021, PMC8508367), PubMed-Abstracts (Hammami et al., 2019 · '
    'Andrade et al., 2018 · Ramirez-Campillo, Sanchez-Sanchez, et al., 2020 · Ramirez-Campillo et al., 2021, Volleyball). '
    'In 7 der 25 Sätze stimmt der Beleg nicht oder nur teilweise: '
    '(1) „96 % … unter 30 m, 49 % unter 10 m“ geben Stølen et al. (2005, S. 526) aus einem Kongressbeitrag über brasilianische '
    'Elitespieler weiter (Valquer et al., 1998, dort Ref. 167). '
    '(2) „1–11 % of that distance“ meint bei Stølen et al. (2005, S. 503) die Gesamtlaufstrecke und fasst vier Studien zusammen, '
    'bei Aloui bezieht es sich grammatisch auf die Sprintstrecke und steht unter Mohr et al. (2003). '
    '(3) „easy to administer and therefore popular“ steht nicht bei Ramirez-Campillo et al. (2020), die beiden anderen Belege '
    'betreffen Ausdauerläufer und Individualsportler. '
    '(4) „Regardless of age, gender, sport, and expertise … consistently … vertical jumping, agility, and sprinting“: Andrade et al. '
    '(2018) ohne Sprint- und Agilitätstest (vier Wochen, Reaktivkraftindex, 2-km-Lauf), Ramirez-Campillo, Sanchez-Sanchez, et al. '
    '(2020) nur CMJ bei Fußballerinnen, Ramirez-Campillo et al. (2021, Volleyball) laut Abstract ohne Agilitätsmaß, dort '
    'moderierte das Alter den CMJ-Zuwachs (ab 16 Jahren ES 1,28, darunter 0,38). '
    '(5) „less than 8 weeks, bilateral jumping coupled with unilateral drills“ steht nicht bei Markovic & Mikulic (2010), '
    'kurzfristig heißt dort 6 bis 15 Wochen (S. 860), Wang & Zhang (2016) nicht geprüft. '
    '(6) „combined training is superior“: Beato et al. (2018) fanden nur beim Weitsprung einen kleinen Vorteil der Kombination, '
    'sonst keinen Gruppenunterschied (Ms.-Z. 270–272). '
    '(7) Hammami et al. (2020) verbesserten den Richtungswechsel nur mit Fußgewichten, die unbeschwerte Variante, die Alouis '
    'Programm entspricht, nicht (Ergebnisse). '
    'Die Lücke („least investigated“, „paucity of data“) grenzt nicht von Hammami et al. (2019, Aloui Mitautor, U15-Handball) '
    'und Aloui et al. (2021, U15-Fußball) ab. Beide kombinierten Plyometrie und Sprints mit Richtungswechsel über acht Wochen '
    'zweimal wöchentlich. Wiederholte Sprints und Gleichgewicht stehen ohne Begründung und ohne Hypothese. 13 Belege in einem '
    'Satz. Zwei Arbeiten mit sechs Autoren als Zwei-Autoren-Zitat (Ramirez-Campillo & Castillo, Ramirez-Campillo & '
    'Sanchez-Sanchez). '
    'Aloui et al. (2021): gleiche Mannschaftsbeschreibung (eine Mannschaft der ersten nationalen Liga), gleiche '
    'Ethik-Referenznummer KS000002020 (Genehmigung 10.11.2020 gegen 10.12.2020), fast gleiche Kennwerte der Kontrollgruppe '
    '(14,6 Jahre, 1,67 ± 0,05 m, 11,8 % Körperfett, 61,0 gegen 61,1 kg, n 17 gegen 16). Ob sich die Stichproben überschneiden, '
    'ist aus beiden Texten nicht entscheidbar. '
    'KONSEQUENZ: keine Aussage aus dieser Einleitung über Aloui et al. (2022) zitieren. In 6.1 Aloui et al. (2022) und (2021) '
    'nicht als unabhängige Befunde zählen. Stølen et al. (2005) bleibt ausgeschlossen (F17 § 6.5). '
    '[Nachgetragen 30.09.2026, Einleitung am PDF geprüft (MD5 ccc022fe…), Belege wie oben]'
)
assert SEMI not in TEXT and SEMI not in ART and '\n' not in TEXT
buf = io.StringIO()
w = csv.writer(buf, delimiter=SEMI, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
w.writerow([ID, ART, TEXT])
neu = roh if roh.endswith('\n') else roh + '\n'
neu += buf.getvalue()
with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(neu)

# Prüfungen: alte Zeilen unverändert, genau eine Zeile mehr, drei Felder je Zeile
neu_bytes = open(OUT, 'rb').read()
assert neu_bytes.startswith(roh_bytes), 'Bestand verändert'
zeilen_neu = list(csv.reader(io.StringIO(neu_bytes.decode('utf-8-sig')), delimiter=SEMI))
assert len(zeilen_neu) == len(zeilen) + 1, 'Zeilenzahl'
assert all(len(z) == 3 for z in zeilen_neu), 'Feldzahl'
assert zeilen_neu[-1] == [ID, ART, TEXT], 'neue Zeile'
print('Eingabe: %d Byte, MD5 %s' % (len(roh_bytes), hashlib.md5(roh_bytes).hexdigest()))
print('Ausgabe: %d Byte, MD5 %s' % (len(neu_bytes), hashlib.md5(neu_bytes).hexdigest()))
print('T4: %d Einträge ohne Kopfzeile (vorher %d)' % (len(zeilen_neu) - 1, len(zeilen) - 1))
print('Einträge %s jetzt: %d' % (ID, sum(1 for z in zeilen_neu[1:] if z[0] == ID)))
print('Neuer Eintrag: %d Zeichen, Bestand byte-gleich übernommen' % len(TEXT))

# -*- coding: utf-8 -*-
"""
T4_Nachtrag_dV2009_2026-09-28.py — Zitierfalle zu Sáez-Sáez de Villarreal et al. (2009), Tab. 2, in T4 nachtragen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Task Steuerdokumente 28.09. (Übergabe § 1 Nr. 11, Maßnahme G34 d)

Anlass: Fassung 16 § 6.6 und § 12 G8 führten p = 0,102 als Beleg für „Leistungsniveau ist kein starker Moderator“.
Der Wert gehört zur Zeile „Fitness“. Am PDF geprüft am 28.09.2026 (Tab. 2 auf der gedruckten Seite 501,
Diskussionssatz der Autoren auf S. 500). Der Eintrag wird angehängt, bestehende Zeilen bleiben unverändert.
Aufruf: python T4_Nachtrag_dV2009_2026-09-28.py <T4_zitierfallen.csv> <Ausgabe.csv>
Ohne Semikolon im Skript (chr(59)). Fassung 2 (28.09., nach der Zweitprüfung von Fassung 17, Befund 1: die oberste Stufe
beim Sportniveau beruht auf zwei Effektstärken einer einzigen Studie, n in Tab. 2 zählt Effektstärken).
"""
import sys
import csv
import io

SRC, OUT = sys.argv[1:3]
SEMI = chr(59)
roh = open(SRC, encoding='utf-8-sig').read()
zeilen = list(csv.reader(io.StringIO(roh), delimiter=SEMI))
ART = 'Tab. 2: Fitness gegen Sport level (Moderator Leistungsniveau)'
if any(z and z[0] == 'dV2009' and z[1] == ART for z in zeilen):
    raise SystemExit('Eintrag besteht schon, nichts geändert')
TEXT = ('Tab. 2 (S. 501): Die Zeile „Fitness“ trägt F(3,121) = 1,97, p = 0,102 (ES Bad 0,80 · Normal 0,54 · Good 0,84 · '
        'Elite 0,70). Die Zeile „Sport level“ trägt F(3,121) = 5,26, p = 0,001 (ES International 1,22 bei n = 2 · National '
        '0,55 bei n = 18 · Regional 0,47 bei n = 32 · No athletes 0,94 bei n = 44, n zählt Effektstärken, nicht Studien). Der Wert p = 0,102 gehört zum '
        'Fitnessniveau, nicht zum Leistungsniveau. Das Muster nach Sport level ist nicht monoton, die Autoren deuten es als '
        'Vorteil internationaler gegenüber regionalen Athleten (S. 500). Die oberste Stufe beruht auf zwei Effektstärken einer '
        'einzigen Studie (Matavulj et al., 2001, Tab. 1: 1,13 und 1,32). '
        'KONSEQUENZ: nicht als Beleg für „Leistungsniveau ist kein starker Moderator“ zitieren, für das Leistungsniveau keine '
        'Richtung angeben und nicht auf Sprint oder Richtungswechsel übertragen. Tragfähig ist nur: Das Fitnessniveau moderierte '
        'die Effektstärke der vertikalen Sprunghöhe nicht nachweisbar. '
        '[Nachgetragen 28.09.2026, Task Steuerdokumente, am PDF geprüft]')
buf = io.StringIO()
w = csv.writer(buf, delimiter=SEMI, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
w.writerow(['dV2009', ART, TEXT])
neu = roh if roh.endswith('\n') else roh + '\n'
neu += buf.getvalue()
with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(neu)
anz = len(list(csv.reader(io.StringIO(neu), delimiter=SEMI))) - 1
print('T4: %d Einträge ohne Kopfzeile (vorher %d)' % (anz, len(zeilen) - 1))

# -*- coding: utf-8 -*-
"""Plan_Rev4_2026-09-25.py - schreibt den Plan der weiteren Schritte von Rev. 3 auf Rev. 4 fort (Abschluss Tasks 2 bis 5).
Aufruf: python Plan_Rev4_2026-09-25.py <Plan.md> <Plan_neu.md>"""
import sys
SRC, OUT = sys.argv[1:3]
t = open(SRC, encoding='utf-8').read()
REV4 = """

**Rev. 4 (25.09.2026, spät, Rev. 105 der Sitzungsnotizen):** Block B bis auf 4.7 abgeschlossen. Task 1 (Steuerdokumente, Rev. 98), Task 2 (4.3, Rev. 99/100), Task 3 (4.4, Rev. 101), Task 4 (4.5, Rev. 102/103) und Task 5 (4.6 mit 4.1, Rev. 104/105) sind erledigt. Kapitel 4 ohne 4.7 steht mit 1.962 gegen 2.000 Wörtern im Master, ohne Semikolon und ohne Abschnittsverweis (§ 1a). Nächster Task ist 6 (4.7 auf 550), danach Block C. Projektanweisungen: Fassung 16 ersetzt die nicht eingesetzte Fassung 15 (Startsätze § 8). Von Hand fortgeschrieben per Skript `03_Skripte\\Plan_Rev4_2026-09-25.py`."""
R = [
("# Plan der weiteren Schritte — Stand 25.09.2026, abends, Rev. 3", "# Plan der weiteren Schritte — Stand 25.09.2026, spät, Rev. 4"),
("Startsätze in § 8 angepasst. Von Hand fortgeschrieben, Erzeuger und Vorlage stehen auf Rev. 2.", "Startsätze in § 8 angepasst. Von Hand fortgeschrieben, Erzeuger und Vorlage stehen auf Rev. 2." + REV4),
("## 0 Ergebnis in Kürze\n\n1. **Stand.**", "## 0 Ergebnis in Kürze\n\n0. **Stand Rev. 4.** Tasks 1 bis 5 erledigt. Absatztext Kapitel 1 bis 7 jetzt **7.603 Wörter**, Kürzungsauftrag **2.141** (Kapitel 2 1.970, 4.7 171). Kapitel 4 ohne 4.7 im Budget. Die 61 Semikola und 35 Abschnittsverweise stehen alle in Kapitel 2. Die Punkte 1 und 4 unten sind der Stand vor der Textrevision.\n1. **Stand (vor der Textrevision, Rev. 1 bis 3).**"),
("\n---\n\n## 2 Schritt 0", """

### 1a Stand nach Block B (Rev. 4, 25.09.2026, spät)

Gemessen am Master (49.304 Byte, Rev. 105) mit `Manuskriptstand_2026-09-25.py`, Fassung 2 (Budget 4.7 = 550, Beschriftungen nur Formatvorlage Caption oder „Tab. 1.“).

| Abschnitt | vorher (Rev. 3) | jetzt | Budget | Semikola | Verweise | Task |
|---|---:|---:|---:|---:|---:|---|
| 4.1 | 309 | 300 | 300 | 0 | 0 | 5 (Rev. 104) |
| 4.2 | 208 | 208 | 215 | 0 | 0 | — |
| 4.3 | 590 | 340 | 340 | 0 | 0 | 2 (Rev. 100) |
| 4.4 mit 4.4.1 bis 4.4.3 | 760 | 392 | 420 | 0 | 0 | 3 (Rev. 101) |
| 4.5.1 | 468 | 418 | 420 | 0 | 0 | 4 (Rev. 103) |
| 4.5.2 | 496 | 150 | 150 | 0 | 0 | 4 (Rev. 103) |
| 4.6 | 175 | 154 | 155 | 0 | 0 | 5 (Rev. 104/105) |
| 4.7 | 721 | 721 | 550 | 0 | 0 | **6 offen** |
| 2.1 bis 2.4 | 4.920 | 4.920 | 2.950 | 61 | 35 | **7 bis 10 offen** |
| **Kapitel 1 bis 7** | **8.647** | **7.603** | **9.000** | **61** | **35** | |

Kapitel 4 ohne 4.7: 1.962 gegen 2.000. Mit 4.7: 2.683 gegen 2.550 (+133). Platzhalter 7 (Anhang H), Tab. 1 ist nach Verfasserentscheidung vom 25.09. aus dem Master entfernt und wird in Task 18 eingesetzt.

**Offen aus Block B für spätere Tasks** (Quelle: Textvorschläge 4.3, 4.4, 4.5, 4.1_4.6 vom 25.09., je § Vormerkungen): Task 12 (6.2, 6.3) Temperaturdifferenz, Abschlusstestungen teils in der Saison, Aufwärmzustand B und C, Personalunion, Vorhersagegenauigkeit %PAH, 20 m mit Ferguson, Startdistanz 0,5 gegen 0,3 m, TE ohne Wiederholungstermin, Verzerrungsrichtung der Begleitprogramme beidseitig, 48-h-Abstand nicht prüfbar, Mastery-Kriterium · Task 15 Clarke als Manuskript · Task 17 Anhang D: Laufplan Verein A nicht dokumentiert, Vornamen in Hohenlind.jpg schwärzen, Trainingsdokumentation bereinigen · Task 18 Tab. 1 mit gesicherter Beschriftung, Tab. H6 mit 20 m, Begriff „videogeführt“ einheitlich, Überschrift 4.4.2 ohne „(bilateral)“, Punkt nach „berechnet“ in 4.4.2 prüfen.

---

## 2 Schritt 0"""),
("**Task 3 · 4.4 Leistungsdiagnostik", "*Erledigt 25.09. (Rev. 99/100):* 4.3 mit 340 Wörtern im Master, Klickfragen 5 bis 8 beantwortet, Textvorschlag `Textvorschlag_4.3_2026-09-25.md`.\n\n**Task 3 · 4.4 Leistungsdiagnostik"),
("**Task 4 · 4.5 Trainingsintervention komplett", "*Erledigt 25.09. (Rev. 101):* 4.4 mit 392 Wörtern im Master, 20-m-Satz entfällt, Tab. 1 als Platzhalter bis Task 18, Textvorschlag `Textvorschlag_4.4_2026-09-25.md`.\n\n**Task 4 · 4.5 Trainingsintervention komplett"),
("**Task 5 · 4.6 Adhärenz- und Belastungsmonitoring und 4.1 Studiendesign**", "*Erledigt 25.09. (Rev. 103):* 4.5.1 418 und 4.5.2 150 im Master, vom Verfasser übertragen, Abgleich bestanden.\n\n**Task 5 · 4.6 Adhärenz- und Belastungsmonitoring und 4.1 Studiendesign**"),
("**Task 6 · 4.7 Statistische Auswertung auf 550 zurückführen**", "*Erledigt 25.09. (Rev. 104/105):* 4.1 300 und 4.6 154 im Master, auf Anweisung des Verfassers direkt eingebaut. Abschlusskarte (Fortschrittskarte je Wochenvideo) in 4.6 ergänzt, Zusagereihenfolge und Laufplan Verein A vom Verfasser bestätigt. Textvorschlag `Textvorschlag_4.1_4.6_2026-09-25.md`.\n\n**Task 6 · 4.7 Statistische Auswertung auf 550 zurückführen**"),
("**Kürzungen je Abschnitt (Ist → Budget):**", "**Stand Rev. 4:** Kürzungsauftrag noch **2.141** (Kapitel 2 1.970, 4.7 171). Die Kürzungen in 4.1 bis 4.6 sind erledigt (§ 1a).\n\n**Kürzungen je Abschnitt (Ist → Budget, Stand vor der Textrevision):**"),
("Jeder Startsatz setzt voraus, dass die aktuelle Fassung der Projektanweisungen in den Projekteinstellungen steht (ab Task 2: Fassung 15)", "Jeder Startsatz setzt voraus, dass die aktuelle Fassung der Projektanweisungen in den Projekteinstellungen steht (ab Task 6: Fassung 16, Fassung 15 wird nicht eingesetzt)"),
]
for a, b in R:
    n = t.count(a)
    assert n == 1, (n, a[:70])
    t = t.replace(a, b)
open(OUT, 'w', encoding='utf-8', newline='\n').write(t)
print('ok', len(R))

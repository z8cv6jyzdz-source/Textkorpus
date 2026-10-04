# -*- coding: utf-8 -*-
"""Projektanweisungen_Fassung16_2026-09-25.py - erzeugt Fassung 16 aus Fassung 15 (gezielte Ersetzungen, jede genau einmal)
und den Vergleich beider Fassungen. Anlass: Abschluss der Textrevision 4.1 bis 4.6 (Tasks 2 bis 5, Rev. 99 bis 105).
Aufruf: python Projektanweisungen_Fassung16_2026-09-25.py <F15.md> <F16.md> <Vergleich.txt>"""
import sys, difflib
SRC, OUT, CMP = sys.argv[1:4]
t = open(SRC, encoding='utf-8').read()
alt = t

KOPF_ALT = t[:t.find('**(1) Die Auswertung ist abgeschlossen.**')]
KOPF_NEU = """Fassung 16, Stand 25.09.2026, spät (ersetzt Fassung 15 vom 25.09.2026, abends, die nicht eingesetzt wurde)

**Wirksam wird diese Fassung erst, wenn der Verfasser sie in die Projekteinstellungen einsetzt (Maßnahme A8).** Bis dahin gilt dort Fassung 14. Fassung 15 entfällt, sie wird nicht mehr eingesetzt. Sicherung: `Claude\\00_Steuerung\\Projektanweisungen_Fassung16.md`, Projektkopie `claude/Projektanweisungen_Fassung16.md`. Erzeuger `Claude\\03_Skripte\\Projektanweisungen_Fassung16_2026-09-25.py`, Vergleich mit Fassung 15 in `Claude\\03_Skripte\\Projektanweisungen_Vergleich_F15_F16_2026-09-25.txt`.

Neu in Fassung 16 — Stand nach Abschluss der Textrevision 4.1 bis 4.6 (Plan Tasks 2 bis 5, Rev. 99 bis 105):

**(A) Kapitel 4 ohne 4.7 steht im Budget.** 4.1 300 · 4.2 208 · 4.3 340 · 4.4 392 · 4.5.1 418 · 4.5.2 150 · 4.6 154, zusammen 1.962 gegen 2.000, ohne Semikolon und ohne Abschnittsverweis. Offen sind 4.7 (721 gegen 550, Task 6) und Kapitel 2 (2.1 bis 2.4 4.920 gegen 2.950, Tasks 7 bis 10). Messung `03_Skripte\\Manuskriptstand_2026-09-25.txt`, Fassung 2 des Skripts (§ 5.2).

**(B) Objekte zunächst als Platzhalter.** Tabellen und Grafiken kommen erst in den Master, wenn der Text steht und feststeht, welche Objekte übernommen werden (Verfasser 25.09., 22:25). Tab. 1 ist deshalb aus dem Master entfernt, Beschriftung und Anmerkung sind in `04_Uebergaben\\Textvorschlag_4.4_2026-09-25.md` § 9 gesichert, eingesetzt wird in Task 18 (§ 5.3).

**(C) Begleitbedingungen korrigiert.** Verein A gab in W1 bis W2 einen extensiven Laufplan vor (Verfasserangabe, kein Plandokument, nach Verfasser 25.09. ohne Sprints). Die Formel „Sprintreiz exklusiv bei der KG = konservative Verzerrung“ trägt nur für die Vereinspläne. Mannschaftstraining hatte A ab 03.08., B ab 10.08. mit Testspielen, C erst ab 07.09. Die Verzerrungsrichtung ist nicht einseitig und wird in 6.2 beidseitig formuliert (§ 2, § 12 G2).

**(D) Entscheidungen der Tasks 2 bis 5** (§ 13 Nr. 15 bis 22): 20-m-Satz in 4.4 entfällt · keine Tagesdaten in 4.3, Termine nur in Abb. H7 · Erratum Khamis & Roche nur in Anhang G und R14 · keine Reifebänder (K11 geschlossen) · keine Kursivsetzung fremdsprachiger Fachbegriffe (§ 9) · Pause beim Standweitsprung nur in 4.3 · überall 90 s Satzpause · Zusagereihenfolge A vor C bestätigt.

**(E) Direkter Einbau.** Für Task 5 hat der Verfasser den Einbau ohne Freigabe je Abschnitt angewiesen (25.09., 23:04). Das ist eine ausdrückliche Anweisung nach § 1.2 für diesen Task, keine neue Regel. Ohne solche Anweisung gilt weiter: Textvorschlag im Chat, der Verfasser überträgt oder gibt frei.

Aus Fassung 15 unverändert gültig — sechs Änderungen, die alles Weitere steuern:

"""
t = t.replace(KOPF_ALT, KOPF_NEU, 1)

R = [
# § 1.2 Plan-Revision
("9. `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) — Reihenfolge, Budgets, Klickfragen, Startsätze.",
 "9. `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 4) — Reihenfolge, Budgets, Klickfragen, Startsätze, Stand der Tasks."),
("| `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 2) | **Reihenfolge der Arbeit:** achtzehn Tasks in fünf Blöcken, Budgets als Vorgabe, Klickfragen, Startsätze |",
 "| `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 4) | **Reihenfolge der Arbeit:** achtzehn Tasks in fünf Blöcken, Budgets als Vorgabe, Klickfragen, Startsätze. Tasks 1 bis 5 erledigt, nächster Task 6 (4.7 auf 550) |\n| `Claude\\04_Uebergaben\\Textvorschlag_4.3_2026-09-25.md` · `Textvorschlag_4.4_2026-09-25.md` · `Textvorschlag_4.5_2026-09-25.md` · `Textvorschlag_4.1_4.6_2026-09-25.md` | Maßstab des Abgleichs der Tasks 2 bis 5 mit Zug-Zuordnung, Zweitprüfung und **Vormerkungen für die Tasks 7 bis 18** (je § „Vormerkungen“ oder „Offen“). Textvorschlag 4.4 § 9 trägt Beschriftung und Anmerkung von Tab. 1 |"),
# Uebergaben 4.3 bis 4.6 erledigt
("| Eingänge der Textrevision Kapitel 4 (Plan Tasks 2 bis 5), der Textvorschlag 4.5.1 mit der Kürzungsleiter (G28h). Nach dem jeweiligen Task ins Archiv |",
 "| Eingänge der Textrevision Kapitel 4 (Plan Tasks 2 bis 5), **erledigt am 25.09.** (Rev. 99 bis 105). Keine Grundlage mehr für Manuskripttext, die offenen Vormerkungen stehen in den Textvorschlägen vom 25.09. Archivkopie und Aufräumskript mit Task 18 |"),
# Nachtragsvermerk Messskript
("`Manuskriptstand_2026-09-25.py` — rechnet 4.7 noch mit dem Budget 720, beim nächsten Lauf auf 550 umstellen (Vorgabe).",
 "`Manuskriptstand_2026-09-25.py` — Fassung 2 vom 25.09. (spät) rechnet 4.7 mit 550 und erkennt Beschriftungen nur noch an der Formatvorlage Caption oder der Form „Tab. 1.“, erledigt."),
# § 2 Intervention
("Satzpause 90 s · 2×/Woche, ≥ 48 h · 2–3 × 6–10 Wdh. · RAMP ~10 min.",
 "Satzpause 90 s, Übungspause 120 s · 2×/Woche, ≥ 48 h ohne intensive Einheit dazwischen · 1–3 Sätze × 3–10 Wdh. (P-03, P-04) · Aufwärmvideo nach RAMP 8:53 min, Einheit mit Wochenvideo 33:10–40:07 min (P-10) · Tonsignal 120 Schläge je Minute ab W3 (Pogo Hops, Vorwärts Ankle Hops), ab W5 auch Zickzack · jedes Wochenvideo endet mit einer Karte zum Programmfortschritt („Woche x von 6“, Vorschau der Folgewoche)."),
# § 2 Begleitbedingungen
("| Begleitbedingungen [BELEGT] | B: W1–3 Laufplan 2×/Wo aerob, Mannschaftstraining ab 10.08. · A: W1–2 frei, Mannschaftstraining ab 03.08. · C (KG): W1–2 frei, Lauf-/Stabi-Plan 03.–30.08. mit Sprintanteilen, ohne Sprünge, Mannschaftstraining ab 07.09. → Sprintreiz exklusiv bei der KG = konservative Verzerrungsrichtung |",
 "| Begleitbedingungen [BELEGT] | B: W1–3 Laufplan 2×/Wo (Dauerläufe und Fahrtspiele mit Lauf-ABC, ohne Sprints und Sprünge, Plandokument SC BW U16), Mannschaftstraining ab 10.08. mit Testspielen · A: W1–2 extensiver Laufplan (Verfasserangabe, kein Plandokument, ohne Sprints nach Verfasser 25.09.), Mannschaftstraining ab 03.08. · C (KG): W1–2 frei, Lauf- und Athletikplan 03.–30.08. mit Sprints über 30 bis 100 m, ohne Sprünge, Mannschaftstraining ab 07.09. → Eigene Sprinteinheiten sah nur der KG-Plan vor. Die Verzerrungsrichtung ist wegen des früheren Mannschaftstrainings in A und B nicht einseitig (6.2) |"),
# § 2 Reifestatus
("Reifebänder nicht aufgenommen, Entscheidung offen (K11).", "Keine Reifebänder (Klick 6, 25.09., K11 geschlossen)."),
("die Koeffizienten stammen aus der Originalpublikation. 4.3 nennt das in einem Satz |",
 "die Koeffizienten stammen aus der Originalpublikation. Das Erratum steht nur in Anhang G und im Register R14, nicht im Fließtext (Verfasser 25.09.) |"),
# § 2 Monitoring
("| Monitoring | Nur Fragebogen A (IG, je Einheit, SoSci test546007). Für die KG sah der Antrag kein Instrument vor.",
 "| Monitoring | Nur Fragebogen A (IG, je Einheit, SoSci test546007). Treuesicherung (TIDieR 11): Erinnerungen in den WhatsApp-Gruppen ohne protokollierte Häufigkeit, Fortschrittskarte am Ende jedes Wochenvideos (beides in 4.6). Für die KG sah der Antrag kein Instrument vor."),
# § 5.2 Stand am Master
("**Stand am Master (Messung 25.09., `03_Skripte\\Manuskriptstand_2026-09-25.txt`):** 4.1 309 · 4.2 208 · 4.3 590 · 4.4 mit 4.4.1 bis 4.4.3 760 · 4.5.1 468 · 4.5.2 496 · 4.6 175 · 4.7 721 · Kapitel 4 (4.1 bis 4.6) 3.006, mit 4.7 3.727 · Kapitel 2 (2.1 bis 2.4) 4.920 · Absatztext Kapitel 1 bis 7 8.647 · Kürzungsauftrag 3.147.",
 "**Stand am Master (Messung 25.09., spät, Rev. 105, `03_Skripte\\Manuskriptstand_2026-09-25.txt`, Skript Fassung 2):** 4.1 300 · 4.2 208 · 4.3 340 · 4.4 mit 4.4.1 bis 4.4.3 392 · 4.5.1 418 · 4.5.2 150 · 4.6 154 · 4.7 721 · Kapitel 4 (4.1 bis 4.6) 1.962, mit 4.7 2.683 · Kapitel 2 (2.1 bis 2.4) 4.920 · Absatztext Kapitel 1 bis 7 7.603 · Kürzungsauftrag 2.141 (Kapitel 2 1.970, 4.7 171) · Semikola außerhalb der Zitierklammern 61 und Abschnittsverweise 35, alle in Kapitel 2. Vor der Textrevision (25.09., abends): 4.1 309 · 4.3 590 · 4.4 760 · 4.5.1 468 · 4.5.2 496 · 4.6 175 · Absatztext 8.647 · Kürzungsauftrag 3.147."),
("Der geschriebene Bestand beträgt am 25.09. **8.647 Wörter** Absatztext",
 "**Stand vor der Textrevision Kapitel 4 (historisch, Rev. 96).** Der geschriebene Bestand betrug am 25.09. abends **8.647 Wörter** Absatztext"),
("- **Kapitel 4: −1.177** (4.1 bis 4.7 von 3.727 auf 2.550, darin 4.7 von 721 auf 550).",
 "- **Kapitel 4: −1.177** (4.1 bis 4.7 von 3.727 auf 2.550, darin 4.7 von 721 auf 550). **Stand 25.09., spät: 4.1 bis 4.6 erledigt (1.962 gegen 2.000), offen nur 4.7 mit −171.**"),
("Reihenfolge nach dem Plan der weiteren Schritte (Rev. 2): Steuerdokumente → Textrevision Kapitel 4 (4.3, 4.4, 4.5.2 mit 4.6, 4.1 mit 4.5.1, 4.7 auf 550)",
 "Reihenfolge nach dem Plan der weiteren Schritte (Rev. 4): ~~Steuerdokumente → Textrevision 4.3, 4.4, 4.5, 4.6 mit 4.1~~ (erledigt 25.09.) → 4.7 auf 550 (Task 6)"),
# § 5.3 Objekte als Platzhalter
("**Im Textteil stehen fünf Objekte** (Verfasser 24.09.):",
 "**Im Textteil stehen fünf Objekte** (Verfasser 24.09.). Bis Task 18 stehen im Master nur Platzhalter, eingesetzt wird, wenn der Text steht (Verfasser 25.09., 22:25):"),
# § 9 Kursivsetzung
("⟨Offen⟩ Kursivsetzung fremdsprachiger Fachbegriffe. Entscheidung treffen und einheitlich umsetzen.",
 "Keine Kursivsetzung fremdsprachiger Fachbegriffe (Klick 8, 25.09.). Umsetzung in der Endredaktion (Task 18)."),
# § 12 G2
("Sprint- und Kraftanteile im KG-Plan bei sprintfreier Intervention → konservative Verzerrung, die über den Sprintanteil der 505-Gesamtzeit auch die Richtungswechsel-Zielgröße erreicht.",
 "Sprint- und Kraftanteile im KG-Plan bei sprintfreier Intervention verzerren konservativ, über den Sprintanteil der 505-Gesamtzeit auch die Richtungswechsel-Zielgröße. Gegenläufig wirkt das frühere Mannschaftstraining der IG-Vereine (A ab 03.08., B ab 10.08. mit Testspielen, C ab 07.09.). Die Richtung ist deshalb nicht einseitig, beide Seiten nennen."),
# § 12 G7
("20-m-Zwischenzeit nicht erhoben – als begründete Entscheidung des Messaufbaus formulieren [EXTRAPOLATION], nicht als Literaturbefund.",
 "20-m-Zwischenzeit nicht erhoben – der Satz in 4.4 entfällt (Verfasser 25.09.), die Pflicht nach CONSORT 6b tragen Tab. H6 und diese Gruppe, als Entscheidung des Messaufbaus, nicht als Literaturbefund."),
# § 13 neue Entscheidungen
("14. **Maßnahmenliste:** Bereinigung freigegeben und ausgeführt, Rev. 97 (25.09., abends).",
 """14. **Maßnahmenliste:** Bereinigung freigegeben und ausgeführt, Rev. 97 (25.09., abends).
15. **20 m in 4.4:** Der Satz zum Verzicht auf die 20-m-Zwischenzeit entfällt, die Pflicht geht auf Tab. H6 und 6.3 G7 über (25.09., 22:19).
16. **Objekte:** zunächst als Platzhalter, eingesetzt in Task 18 (25.09., 22:25).
17. **4.3:** keine Tagesdaten und Kalenderwochen (Termine in Abb. H7), Temperatur bei den Abschlusstestungen niedriger, bis zu 10 °C (Verfasserangabe), Erratum nicht im Fließtext, keine Aussage zur fehlenden Post-Anthropometrie, Pause beim Standweitsprung nur in 4.3 (25.09., Klick 5).
18. **Reifebänder und Stilprofil Teil 8:** keine Reifebänder (K11 geschlossen), Stilprofil Teil 8 gestrichen (25.09., Klick 6 und 7).
19. **Kursivsetzung:** keine für fremdsprachige Fachbegriffe (25.09., Klick 8).
20. **4.5:** überall 90 s Satzpause, 48 h ohne intensive Einheit dazwischen, Tonsignal ab W5 auch bei den Zickzack-Sprüngen (25.09., Klick G28h).
21. **4.1:** Verein C sagte verbindlich nach Verein A zu, die Zuteilung nach der Zusagereihenfolge ist damit belegt (25.09., 23:23).
22. **Laufplan Verein A:** nach Verfasser ohne Sprints (25.09., 23:23). Ein Plandokument liegt nicht vor, Anhang D führt A als „nicht dokumentiert“ oder mit Plan vom Trainerteam (Task 17)."""),
("Projektanweisungen vor Fassung 15 ·", "Projektanweisungen vor Fassung 16 (Fassung 15 wurde nicht eingesetzt, Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung15`) ·"),
("(Sicherung der wirksamen Fassung bis zum Einsetzen von F15, dann Kopie", "(Sicherung der wirksamen Fassung bis zum Einsetzen von F16, dann Kopie"),
("**(4) Kürzung vor Neuem.** Die Reihenfolge folgt dem Plan der weiteren Schritte (Rev. 2):", "**(4) Kürzung vor Neuem.** Die Reihenfolge folgt dem Plan der weiteren Schritte (Rev. 4):"),
]
for a, b in R:
    n = t.count(a)
    assert n == 1, (n, a[:80])
    t = t.replace(a, b)
assert chr(59) not in KOPF_NEU
open(OUT, 'w', encoding='utf-8', newline='\n').write(t)
d = list(difflib.unified_diff(alt.splitlines(), t.splitlines(), 'Fassung15', 'Fassung16', n=0, lineterm=''))
with open(CMP, 'w', encoding='utf-8', newline='\n') as f:
    f.write('Vergleich Projektanweisungen Fassung 15 -> Fassung 16 (25.09.2026, spät), %d Ersetzungen plus Kopf\n' % len(R))
    f.write('Zeichen: F15 %d, F16 %d\n\n' % (len(alt), len(t)))
    f.write('\n'.join(d) + '\n')
print('ok', len(R), len(alt), len(t))

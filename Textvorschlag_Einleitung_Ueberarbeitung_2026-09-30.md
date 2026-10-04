# Textvorschlag Einleitung — Überarbeitung nach dem Abgleich mit der Argumentationsstruktur — 30.09.2026

Anlass: Task „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“, Schritt 4 (Startprompt der Übergabe `04_Uebergaben\Uebergabe_Abgleich_Einleitung_Argumentationsstruktur_2026-09-30.md` § 0, Fortsetzung 1). Grundlage ist der Befund `02_Befunde\Abgleich_Einleitung_Argumentationsstruktur_2026-09-30.md`: Textstand T (§ 1.3), Wortlautbefunde (§ 3.5), Potenziale mit Klick (§ 4, 30.09., 17:32 Sitzungsuhr: P1 bis P4 und P9). Überarbeitet wird Absatz für Absatz in der Folge B1a, B1b, B2, B3, B4, B5, nur mit den freigegebenen Potenzialen. Absätze ohne freigegebenes Potenzial bleiben wortgleich. Je Absatz: Kopf, Wortlaut, Zug-, Änderungs- und Belegtabelle, Zweitprüfung durch einen unabhängigen Subagenten, Klickstatus. Am Ende die ganze Einleitung im freigegebenen Wortlaut mit Messung. Messung mit `03_Skripte\Abgleich_Einleitung_2026-09-30\schritt4_messung.py` (wie `Manuskriptstand_2026-09-25.py`, Leerraum-Token mit Belegklammern). Ablage `Claude\04_Uebergaben\`, Projektkopie `claude/`. Keine Änderung am Master, der Verfasser überträgt.

## 0 Übersicht

| Absatz | Potenziale | Stand |
|---|---|---|
| B1a Relevanz und Wirksamkeit | — | wortgleich mit dem Textstand (153 Wörter) |
| B1b Dehnungs-Verkürzungs-Zyklus | P1, P9 | § 1, freigegeben 30.09., 18:02 |
| B2 Heimprogramm und Detraining | — | wortgleich mit dem Textstand (229 Wörter) |
| B3 Zielgrößen und Diagnostik | P2 | § 2, freigegeben 30.09., 18:46, S5 ohne Ferguson et al. (2024) (Klick § 2.7 a) |
| B4 Einordnung und Lücke | P3, P4 | § 3, freigegeben 30.09., 19:45, P3b und P4c (DVZ-Bezug modal, Klick § 3.7 a). `Tanner1966` in T1 und T4 nachgetragen 30.09. |
| B5 Zweck, Vorgehen, Hypothesen | — | wortgleich mit dem Textstand (99 Wörter), § 4 |
| Ganze Einleitung | — | § 5, im freigegebenen Wortlaut, neu codiert und gemessen (930 Wörter) |

## 1 B1b — Dehnungs-Verkürzungs-Zyklus als gemeinsame Grundlage (P1, P9)

### 1.1 Kopf (gemessen mit `schritt4_messung.py`, Stand nach B1b und vor P2)

| Größe | Wert | Vorgabe oder Vergleich |
|---|---|---|
| Wörter B1b | **152** (ohne Belegklammern 116) | Textstand 152 (S1 +1, S7 −1) · kein Absatz über 250 |
| Einleitung | **913** (ohne Belegklammern 757), 39 Sätze, Median 24,0, längster Satz 32 | Obergrenze 1.200 · Korpus 506 bis 927 |
| Sätze B1b · Median · längster | 7 · 22,0 · 30 | höchstens 32 |
| Semikola außerhalb von Belegklammern · Abschnittsverweise · Quelle als Subjekt | 0 · 0 · 0 | 0 |
| Belegklammern B1b · Quellen der Einleitung | 6 · 23 | unverändert |
| Zahlen aus dem Kennzahlenblatt | keine | keine Studienzahlen |
| Seitenprognose | rund 27,8 Seiten (27,76, Modellrechnung wie `textstand_T.py`, Parameter aus `Seitenmodell_2026-09-28.csv`, Wortzahl unverändert) | Schwelle 32, Grenze 33 |

### 1.2 Wortlaut (Neufassung, Satzzählung für § 1.3 bis § 1.6)

Der Dehnungs-Verkürzungs-Zyklus (DVZ) stellt bei Sprung- und Hüpfbewegungen die grundlegende Muskelaktion des plyometrischen Trainings dar (Markovic & Mikulic, 2010). Er verbindet eine exzentrische Dehnung des Muskels mit der unmittelbar folgenden Verkürzung, die dadurch mehr Leistung abgibt als ohne Vordehnung (Radnor et al., 2018). Zu dieser Mehrleistung könnten ein Kraftaufbau schon während der Dehnung, gespeicherte elastische Energie, Dehnreflexe sowie eine neuronale und kontraktile Potenzierung beitragen (Markovic & Mikulic, 2010; Radnor et al., 2018). Mit Bodenkontakten unter 250 ms verläuft der DVZ im Maximalsprint schnell, mit längeren in der 180°-Wende und im Sprung mit Ausholbewegung langsam (Dos’Santos et al., 2018; Lloyd et al., 2011). An Sprint-, Richtungswechsel- und Sprungleistung sind damit schneller und langsamer DVZ beteiligt. Ein Programm mit Übungen beider Formen setzt an dieser gemeinsamen Muskelaktion an (Lloyd et al., 2011). Plyometrische Übungen sind zudem Bestandteil mehrkomponentiger Präventionsprogramme, die in Metaanalysen zum Nachwuchssport Verletzungen verringerten (Olivier et al., 2026; Rössler et al., 2014).

S1 19 · S2 24 · S3 29 · S4 30 · S5 12 · S6 16 · S7 22 Wörter. Der Absatz ist damit wortgleich mit der freigegebenen Fassung (Textvorschlag B1 § 1.2, Klick 30.09., 07:00), per Assertion in `schritt4_messung.py` geprüft.

### 1.3 Zug-Tabelle

Codes nach der Konsenscodierung des Textstands (Befund Anhang A), Sekundärcode in Klammern. Die Neufassung ändert keinen Code.

| Satz | Code | Zug (Befund Argumentationsstruktur § 3) und Bauregel (§ 6) |
|---|---|---|
| S1 | T2 | Mechanismus nach der Einführung des Trainingsmittels (B1a S3), der DVZ als Muskelaktion der Trainingsform (§ 3.3) · Register 29.09., 17:41: DVZ als Grundlage für Programm und Auswahl der Leistungen · keine Bauregel betroffen |
| S2 | T2 | Beschreibung des DVZ im Indikativ (§ 3.3) · keine Bauregel betroffen |
| S3 | T2 | Erklärungsangebot modal („könnten“, F17 § 10, Befund § 3.2 b20) · keine Bauregel betroffen |
| S4 | T2 | schnelle und langsame Form (Register 17:41: prägnant) · keine Bauregel betroffen |
| S5 | T2 | Folgerung: alle drei Leistungen mit DVZ (Register 17:41: Grundlage der Auswahl, nicht „die Tests messen den DVZ“) · keine Bauregel betroffen |
| S6 | T4 (T2) | Programmgestaltung an der gemeinsamen Muskelaktion, Bezugswort „Muskelaktion“ aus S1 · keine Bauregel betroffen |
| S7 | T3 (E1) | Zusatznutzen der Programmklasse (§ 3.2), Bauregel 2 (Vorzüge), Stellung nach Klick 07:00 Nr. 3 a. Die bekannten Abweichungen bleiben: Vorzüge nicht im Einführungssatz (Befund b17), Prävention nicht direkt nach der Einführung (b18), P5 und P8 nicht gewählt · Register 28.09. (Prävention nur als Zusatznutzen der Programmklasse) und 29.09., 06:40 (Rössler et al., 2014, nur als Mitzitation, ohne Population und Vor-2020-Halbsatz) |

### 1.4 Änderungstabelle

| Satz | alt (Textstand, Wortlaut des Verfassers) | neu | Grund |
|---|---|---|---|
| S1 | „Der Dehnungs-Verkürzungs-Zyklus (DVZ), stellt bei Sprung- und Hüpfbewegungen den grundlegenden Wirkmechanismus der Trainingsform dar (…)“ | „Der Dehnungs-Verkürzungs-Zyklus (DVZ) stellt bei Sprung- und Hüpfbewegungen die grundlegende Muskelaktion des plyometrischen Trainings dar (…)“ | P1: „Wirkmechanismus“ bei Markovic & Mikulic (2010, S. 860) nicht gedeckt, dort ist der DVZ die Muskelaktion der Übungen (Befund § 3.5 w1). Komma zwischen Subjekt und Prädikat entfällt. „Muskelaktion“ gibt S6 das Bezugswort zurück, „des plyometrischen Trainings“ nennt die Trainingsform ausdrücklich statt über die Absatzgrenze. +1 Wort |
| S7 | „… die in Metaanalysen zum Nachwuchssport Verletzungen verringerten und (…).“ | „… die in Metaanalysen zum Nachwuchssport Verletzungen verringerten (…).“ | P9: Der Satz brach nach „und“ ab, ohne „und“ ist er an Olivier et al. (2026) und Rössler et al. (2014) gedeckt (Befund § 3.5 w2). −1 Wort |
| S2 bis S6 | unverändert | | |

### 1.5 Belegtabelle

| Satz | Quelle | Wortlaut (nur zur Prüfung) | Seite | Volltext | T1 | T4 |
|---|---|---|---|---|---|---|
| S1 | Markovic & Mikulic (2010) | „It involves performing bodyweight jumping-type exercises … using the so-called stretch-shortening cycle (SSC) muscle action.“ | S. 860 | ✓ 30.09. (MD5 `0d2da9b3…`) | `MM2010` | `MarkovicMikulic2010` (Dauerangaben) und `MM2010` (Verletzungsreduktion nur bei Athletinnen, Plantarflexoren), beide hier ohne Folge |
| S2 | Radnor et al. (2018) | „an eccentric ‘stretching’ action prior to a subsequent concentric ‘shortening’ action … has been shown to enhance the performance of the final concentric phase in comparison to an isolated concentric action“ · für „unmittelbar“: „longer transition times between the eccentric and concentric contraction causes a decay in the magnitude of potentiation“ | OF-S. 2, OF-S. 5 | ✓ 30.09. (MD5 `395ea66f…`) | `Radnor2017` | `Radnor2017` (Online-First, zitiert als 2018) · `Nicol2006` („unmittelbar“ trägt Radnor OF-S. 5, nicht Nicol) |
| S3 | Markovic & Mikulic (2010) · Radnor et al. (2018) | Markovic (Semikola des Originals hier als ·): „(i) the time available for force development · (ii) storage and reutilization of elastic energy · (iii) potentiation of the contractile machinery … (v) the contribution of reflexes“ · Radnor: „increased elastic energy reutilisation, increased neural potentiation and an enhanced stretch-reflex contribution“ (OF-S. 1) · „fast SSC actions promote greater movement speed via elastic energy usage, stretch reflex contributions and a greater level of neural excitation from the preceding stretch“ (OF-S. 2) | S. 875 · OF-S. 1 bis 2 | ✓ 30.09. | `MM2010`, `Radnor2017` | `Nicol2006` (die Mechanismenliste trägt Markovic S. 875, nicht Nicol) |
| S4 | Dos’Santos et al. (2018) · Lloyd et al. (2011) | Dos’Santos: 180°-Wenden mit Kontaktzeiten über 0,25 s, „Slow SSC actions“, dazu Sprung mit Ausholbewegung und Standweitsprung · Lloyd: „Fast SSC activities (<250 milliseconds) are prevalent in the stance phase during maximal sprinting …, whereas slow SSC actions are evident in the performance of maximal vertical countermovement jumps“. Die 250-ms-Schwelle ist in beiden Quellen ein Relais auf Schmidtbleicher (1992) | Tab. 2, S. 2240 · S. 23 | unverändert, geprüft 29.09. (Textvorschlag B1 § 3, § 5), Seiten am Volltext bestätigt 30.09. (Zweitprüfung) | `DosSantos2018`, `Lloyd2011` | `DosSantos2020` (Winkel-Geschwindigkeits-Trade-off gehört zu 2018, hier richtig) |
| S5 | — | Folgerung aus S4 | — | — | — | — |
| S6 | Lloyd et al. (2011) | „athlete programs are designed with consideration given to the desired training form of SSC“ | S. 23 | unverändert, geprüft 29.09. | `Lloyd2011` | — |
| S7 | Olivier et al. (2026) · Rössler et al. (2014) | Olivier: „Multifaceted NMTS (n = 8) reduced the number of injuries among adolescent males“ · „The multifaceted neuromuscular strategies included running, plyometrics, core training …“ · Rössler: 13 von 21 Programmen mit „jumping/plyometric exercises“, Gesamteffekt in „children and adolescents“ | Olivier S. 6, S. 10 · Rössler S. 1741 (Population S. 1733) | ✓ 30.09. (MD5 `41355fc5…`, `6bf5030f…`) | `Olivier2026`, `Roessler2014` | `Olivier2026` (nicht fußballspezifisch, nicht als Rate, Abstract zur Kraft selektiv) · `Roessler2014` (nicht „im Jugendfußball“, Sprungvergleich nicht als Wirkung, p nur aus dem Ergebnisteil, Niveau-Subgruppe a posteriori, Leistungsgewinn ist Relais), alle ohne Folge für den Satz |

Keine neue Quelle. Gegenüber der Belegtabelle der Freigabe (B1 § 3) ergänzt: Radnor OF-S. 5 für „unmittelbar“ in S2 (wie T4 `Nicol2006`) und OF-S. 2 in S3, die dort schon genannt war. Übersetzungsnähe: S1 übernimmt aus Markovic & Mikulic nur den Begriff der Muskelaktion, Satzbau und Formulierung („grundlegende Muskelaktion des plyometrischen Trainings“) sind eigene (Quellenraster § 2.5). Erwogen ist der Hinweis aus der Zweitprüfung von Schritt 3 (Radnor, OF-S. 1: „this key muscle action“ trüge „grundlegend“ wörtlicher). P1 stellt die Freigabe her, Markovic & Mikulic tragen „grundlegend“ sinngemäß (B1 § 3).

### 1.6 Zweitprüfung (unabhängiger Subagent, 30.09., Bericht `03_Skripte\Abgleich_Einleitung_2026-09-30\zweitpruefung_B1b.md`)

Urteil: vorlegbar nach Nachtrag zweier Belegstellen. Der Wortlaut ist byte-gleich mit B1 § 1.2 und weicht vom Textstand genau in S1 und S7 ab. Alle Belege tragen ihre Sätze am Volltext, kein Satz ist eine Übersetzung (S3 mit vier sinngleichen Wörtern an der Grenze, nicht darüber), Codes, Projektregeln und Register eingehalten, keine P- oder P°-Zeile geht verloren. 0 A, 2 B, 9 C.

| Nr. | Schwere | Befund | Umsetzung |
|---|---|---|---|
| 1 | B | S2: „unmittelbar“ trägt OF-S. 2 nicht („subsequent“), T4 `Nicol2006` weist es Radnor OF-S. 5 zu, der Eintrag fehlte | OF-S. 5 mit Wortlaut und `Nicol2006` in § 1.5, Wortlaut von S2 bleibt |
| 2 | B | S3: Radnor nur mit OF-S. 1, die Freigabe nannte OF-S. 1 und 2 | OF-S. 1 bis 2 mit Wortlaut OF-S. 2, Schlusssatz von § 1.5 angepasst |
| 3 | C | Seitenprognose 27,74 statt 27,8 | abgelehnt: mit dem gestagten `Seitenmodell_2026-09-28.csv` nachgerechnet 27,76, gerundet 27,8. Jetzt im Skript |
| 4 | C | „vom Skript geprüft“ ohne Vergleich im Skript | Assertion gegen die Freigabe in `schritt4_messung.py`, Kopf nennt die Herkunft |
| 5 | C | T4 unvollständig: `MM2010`, Olivier und Rössler mit weiteren Einträgen | in § 1.5 ergänzt. `MM2010` fehlt auch in der T4-Liste von Befund § 3.5, Nachtrag vorgemerkt (§ 1.8) |
| 6 | C | T1 `Roessler2014`, Spalte „kapitel“ steht auf dem Klick 28.09., 14:36, gegen Register 29.09., 06:40 | vorgemerkt (§ 1.8) |
| 7 | C | S4: Reihenfolge der Seiten | umgestellt |
| 8 | C | S4: Relais-Vorbehalt zur 250-ms-Schwelle fehlte, Dos’Santos Tab. 2 trägt auch den Sprung | ergänzt |
| 9 | C | S3: „·“ statt der Semikola des Originals ohne Kennzeichnung | gekennzeichnet |
| 10 | C | Zug-Tabelle ohne „keine Bauregel betroffen“, S7 ohne die bekannten Abweichungen b17 bis b18 | ergänzt |
| 11 | C | Übersetzungsnähe: „Formulierung“ statt „Aussage“, Hinweis „key muscle action“ nicht als erwogen vermerkt | umgesetzt |

### 1.7 Klick

Freigabe B1b wie § 1.2: (a) freigeben (Empfehlung) · (b) nicht freigeben, mit Angabe, was sich ändern soll.

**Entschieden (Klick 30.09., 18:02 Sitzungsuhr): (a).** B1b ist wie § 1.2 freigegeben, wortgleich mit Textvorschlag B1 § 1.2. Der Verfasser überträgt.

### 1.8 Vormerkungen aus B1b

- **Befund § 3.5 (Verfahren):** T4-Liste um `MM2010` ergänzen (zweite Kennung zu Markovic & Mikulic, 2010), beim nächsten Speichern des Befunds.
- **T1 `Roessler2014`:** Spalte „kapitel“ auf das Register vom 29.09., 06:40 nachführen (nur Mitzitation neben Olivier et al., 2026, ohne Population und ohne Vor-2020-Halbsatz), am Ende des Tasks oder in Task 15. *Erledigt 30.09. mit `nachtrag_T1_T4.py` vor B4, dabei das ungeschützte Semikolon im Feld berichtigt (16 statt 15 Felder).*

## 2 B3 — Zielgrößen und Diagnostik (P2)

B2 bleibt wortgleich mit dem Textstand (kein freigegebenes Potenzial).

### 2.1 Kopf (gemessen mit `schritt4_messung.py`, Ausgabe `schritt4_messung.txt`)

| Größe | Neufassung § 2.2 (P2) | Variante ohne Ferguson et al. (2024), nur per Klick § 2.7 (a) | Vorgabe oder Vergleich |
|---|---|---|---|
| Wörter B3 | **125** (ohne Belegklammern 101) | 121 (101) | Textstand 127 · kein Absatz über 250 |
| Einleitung | **911** (ohne Belegklammern 755), 39 Sätze, Median 24,0, längster Satz 32 (B5 S1) | 907 (755), sonst gleich | Obergrenze 1.200 · Korpus 506 bis 927 |
| Sätze B3 · Median · längster | 5 · 29,0 · 30 (S5, vorher 32) | 5 · 26,0 · 29 (S1, S2) | höchstens 32 |
| Semikola außerhalb von Belegklammern · Abschnittsverweise · narrative Zitate (Quelle als Subjekt) | 0 · 0 · 0 | 0 · 0 · 0 | 0 |
| Belegklammern B3 · Quellen der Einleitung | 5 · 23 | 5 · 22 (Ferguson et al., 2024, steht nur in B3 S5) | — |
| Zahlen aus dem Kennzahlenblatt | keine | keine | keine Studienzahlen |
| Seitenprognose | rund 27,8 Seiten (27,75) | rund 27,7 Seiten (27,74) | Schwelle 32, Grenze 33 · Modellrechnung wie `textstand_T.py`, Parameter aus `Seitenmodell_2026-09-28.csv` |

**Freigegeben ist die Variante (Klick § 2.7 a, 18:46), ihr Kopf steht in der rechten Wertespalte.** Alle Werte aus den Läufen vom 30.09. Das Skript misst seit diesem Absatz auch Varianten und zählt je Absatz Belegklammern und narrative Zitate (Autor mit Jahr in Klammern im Satz, Prüfgröße für „Quelle als Subjekt“). Die Quellenart steht in B3 nirgends im Satz.

### 2.2 Wortlaut (Neufassung, Satzzählung für § 2.3 bis § 2.6)

Im Sprint entscheidet in der Beschleunigungsphase vor allem die horizontale Ausrichtung der Bodenreaktionskraft, in der Phase maximaler Geschwindigkeit eine hohe vertikale Kraft in kurzen Bodenkontakten (Hicks et al., 2020). Da beide Phasen eine unterschiedliche Kraftentwicklung verlangen, werden Sprintzeiten bis 10 m der Beschleunigung und Zeiten über 15 bis 40 m der maximalen Geschwindigkeit zugeordnet (Oliver et al., 2024). Entschleunigen und erneutes Beschleunigen fordert der 505-Test, der in seinen Varianten zu den gebräuchlichsten Richtungswechseltests gehört (Dugdale et al., 2020). Der Standweitsprung ist ein bei Kindern und Jugendlichen international verbreiteter Feldtest der Schnellkraft (Tomkinson et al., 2021). Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019; Ferguson et al., 2024).

S1 29 · S2 29 · S3 20 · S4 17 · S5 30 Wörter. S1 bis S4 wortgleich mit dem Textstand (B3 bis B5 § 1, Fassung 2, Beginn nach Textvorschlag B1 § 1.3), S5 im Wortlaut des Verfassers ohne „und valide“.

**Variante S5, nur per Klick § 2.7 (a):** Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019). (26 Wörter)

Freigegeben ist S5 in dieser Variante (Klick § 2.7 a, 18:46). Den ganzen Absatz im freigegebenen Wortlaut enthält § 2.7.

### 2.3 Zug-Tabelle

Codes nach der Konsenscodierung des Textstands (Befund Anhang A). Neufassung und Variante ändern keinen Code, D1 schließt Reliabilität und Validität ein.

| Satz | Code | Zug und Bauregel |
|---|---|---|
| S1 | D1 | Kraftentwicklung je Sprintphase als Grundlage der Diagnostik (Register 28.09., 10:30, und 29.09., 15:12) · Diagnostik ist im Korpus kein Einleitungszug, Projektbaustein ohne Bauregel (Befund Argumentationsstruktur § 0 Nr. 6, § 5.3) |
| S2 | D1 | Teilzeiten aus der Kraftentwicklung abgeleitet (15:12) · ohne Bauregel |
| S3 | D1 | 505-Test über die Anforderung (Rückbezug durch die Wortwiederaufnahme, Befund Argumentationsstruktur § 7 Nr. 2) und seine Verbreitung, ohne 180°-Wende und Agilität (15:12) · ohne Bauregel |
| S4 | D1 | Standweitsprung über die Verbreitung, kein Satz zur Schnellkraft als Voraussetzung (15:12) · ohne Bauregel |
| S5 | D1 | Verbreitung und Reliabilität der drei Testformen verbunden (15:12), Messgüte in einem Satz (12:54) · ohne Bauregel |

### 2.4 Änderungstabelle

| Satz | alt (Textstand, Wortlaut des Verfassers) | neu | Grund |
|---|---|---|---|
| S5 | „… erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable und valide feldbasierte Leistungsdiagnostiktests (…).“ | „… erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (…).“ | P2: „valide“ ist in dieser Form nicht gedeckt. Dugdale et al. (2019) prüften Validität nur als Trennung von Alters- und Spielergruppen über U11 bis U17, die Spielergruppen trennte der 10-m-Sprint nicht, ein 30-m-Sprint fehlte, Ferguson et al. (2024) prüften keine Validität (Befund § 3.5 w3). Eine eingeschränkte Validitätsaussage wäre der per Klick gestrichene Niveausatz (30.09., 07:00 Nr. 2 b), die Validität des 505-Tests ist für 6.2 vorgemerkt. „reliable“ ist attributiv richtig und bleibt. −2 Wörter, der Satz liegt mit 30 Wörtern nicht mehr an der Obergrenze |
| S5, Klammer (Klick § 2.7 a, freigegeben 18:46) | „… (Dugdale et al., 2019; Ferguson et al., 2024).“ | „… (Dugdale et al., 2019).“ | Passung (neuer Grund aus der Zweitprüfung, Nr. 2): S5 ist ein Satz der Klasse a (Messgüte der Tests, Quellenraster § 2.1). Dort ist Passung 0 Pflicht, Passung 1 nur mit Nennung der Abweichung im Satz, nach dem Startprompt nur Passung 0. Ferguson et al. (2024) haben Passung 1 (Akademie), die Abweichung steht nicht im Satz. Dugdale et al. (2019) tragen den Satz mit Passung 0 allein. Dazu schränken Fergusons eigene Befunde „reliabel“ für kurze Teilstrecken ein (5 und 10 m nur moderat, systematische Unterschiede zwischen den Terminen). −4 Wörter. Preis: kein Reliabilitätsbeleg für die 30-m-Strecke in der Einleitung. Die Messgüte des eigenen 30-m-Sprints steht in Tab. 1. Ferguson et al. (2024) sind im Master nur im Altbestand 2.4.1 zitiert, nicht in 4.4, und bleiben für 6.2 vorgemerkt (§ 2.8) |
| S1 bis S4 | unverändert | | |

### 2.5 Belegtabelle

| Satz | Quelle | Wortlaut oder Fundstelle (nur zur Prüfung) | Seite | Volltext | T1 | T4 |
|---|---|---|---|---|---|---|
| S1 | Hicks et al. (2020) | AoP-S. 1: „involves 2 key phases: acceleration and maximal velocity“ · AoP-S. 2: „the ability to apply horizontally oriented force has been shown to be one of the key determining factors“, „oriented vertically over the contact phase“ · für „vor allem die horizontale Ausrichtung“ AoP-S. 4: „Directing the resultant GRF in a more forward or horizontally oriented direction is more important during the acceleration phase of a sprint compared with the overall magnitude of force applied to the ground“ · für „hohe vertikale Kraft in kurzen Bodenkontakten“ AoP-S. 4: „a greater reliance is placed on achieving high GRF with a vertical orientation to limit time spent on the ground“ und AoP-S. 9: „the production of high (mostly vertically oriented) force is vital at maximal velocity“ | AoP-S. 1 bis 2, 4, 9 | geprüft 29.09. (Textvorschlag B1 § 3, B3 bis B5 § 4), AoP-S. 4 und 9 am 30.09. nachgeprüft (MD5 `4d6dab24…`) | `Hicks2019` | `Hicks2019` (Ahead-of-Print, zitiert als 2020, keine „erste 10 m“-Aussage) |
| S2 | Oliver et al. (2024) | Einteilung der Sprintstrecken nach Rumpf et al. (2011), „maximal speed“ | S. 626, S. 624 und 634 | unverändert, geprüft 29.09. (B3 bis B5 § 4) | `Oliver2024` | `Oliver2024` (Abstract und Tabellen, hier ohne Folge) |
| S3 | Dugdale et al. (2020) | „versions of the “505” test are most commonly selected due to their ability to challenge deceleration and reacceleration qualities“ (Verbreitung in der Einleitung der Quelle mit Verweis auf [10,17–19], ohne Zahl) | S. 2 | unverändert, geprüft 29.09., Wortlaut am 30.09. zeichengenau nachgeprüft (MD5 `281c4ed2…`) | `Dugdale2020` | `Dugdale2020` (MDPI, modifizierter 505, Einleitungszahl nicht verwenden · Aggregation wie die eigene, hier ohne Folge). Nachtrag „most commonly selected“ ohne Zahl, Relais vorgemerkt (§ 2.8) |
| S4 | Tomkinson et al. (2021) | Daten aus 29 Ländern, 9 bis 17 Jahre · „widely used … measure of functional explosive strength“ | S. 531, S. 532 | unverändert, geprüft 29.09. | `Tomkinson2021` | `Tomkinson2021` (Reliabilität dort nur Relais, hier nicht zitiert) |
| S5 | Dugdale et al. (2019) · Ferguson et al. (2024) | Dugdale: „a battery of commonly used generic field-based fitness tests (grip dynamometry, standing broad jump, …, 505 (505COD) … and 10/20 m sprint tests) on two separate occasions within 7–14 days“, „We have shown field-based fitness tests to be reliable measures of physical performance in youth soccer players“ (OF-S. 1), Tab. I U14 bis U16 (10 m ICC 0,84 bis 0,94, 505 0,85 bis 0,89, Standweitsprung 0,93 bis 0,96). Die Verbreitung in OF-S. 3 ist ein Relais („commonly used as physical performance measures within youth soccer (Paul & Nassis, 2015)“), S5 trägt sie über die eigene Rahmung in OF-S. 1 und 9 · Ferguson: „assessing sprint performance using split-times is commonplace in soccer (41)“ (Relais auf Taylor et al., 2022), „All players competed at a professional youth level … The players attended the same elite youth academy“, 37 Spieler, 14,7 ± 0,8 Jahre, drei Termine mit 24 bis 48 h Abstand, ICC3,1, 20 m 0,86, 30 m 0,93 (5 m 0,53, 10 m 0,73), „relative reliability ranged from moderate to excellent and improved with increased distance“ | Dugdale OF-S. 1, 3, 9, Tab. I OF-S. 5 · Ferguson S. e96, e97, e98, e99 | ✓ 30.09. (MD5 `86536a60…`, `4352339e…`) | `Dugdale2019`, `Ferguson2024` (führt „ICC(2,1)-Typ“ und d_pop 0, beides zu berichtigen, § 2.8) | `Dugdale2019` (Tab. I 20-m-KI nicht zitieren, Online-First als 2019 · 505 als Mittel der Bestwerte beider Beine, kein seitengetrennter Beleg · Reliabilitätsstudie, kein Interventionsbeleg) · `Ferguson2024` (standardisierte Zwischen-Termin-Differenzen bis 2,63 und 2,73 SD bei 5 und 10 m, systematischer Bias möglich, nur ICC und SEM zitieren · SEM relativ und absolut trennen). Ohne Folge für den Wortlaut, der keine Kennwerte nennt |

**Passung (Quellenraster § 2.1, Klasse a „Messgüte der Tests“).** Dugdale et al. (2019): Passung 0, 373 schottische Nachwuchsspieler U11 bis U17 vom Amateur- bis zum Leistungsniveau, U14 bis U16 in Tab. I, alle drei Testformen (Quellenraster Zeilen 2.6 und 2.14). Die Quelle trägt S5 allein. Ferguson et al. (2024): Passung 1, Akademiespieler auf „professional youth level“ (S. e97, Quellenraster Zeile 2.5), nur Sprint, flankierend für 20 und 30 m. Die Abweichung steht nicht im Satz, „aus Akademievereinen“ engte Dugdale et al. (2019) falsch ein. S5 weicht damit in der Fassung des Verfassers von der Regel ab: Passung 1 ohne Nennung im Satz, nach dem Startprompt nur Passung 0. Die Abweichung besteht seit Fassung 2 (Ferguson et al., 2024, dort für den konfirmatorischen 30-m-Sprint aufgenommen, B3 bis B5 § 6.1 und § 6.2). Befund § 2.2 Nr. 3 prüfte S5 nur auf „valide“. Entschieden per Klick § 2.7 (a), 18:46: Ferguson et al. (2024) aus der Klammer, S5 trägt nur Dugdale et al. (2019) mit Passung 0.

Keine neue Quelle, keine neue Belegstelle für den Wortlaut. Übersetzungsnähe (Quellenraster § 2.5 Nr. 5, für diesen Satz des Verfassers erstmals zweitgeprüft): keine Übersetzung. „als reliable feldbasierte Leistungsdiagnostiktests“ hat vier Entsprechungen in OF-S. 1 („field-based fitness tests to be reliable measures“), dort nicht zusammenhängend und in anderer Folge. Satzbau (zwei Prädikate, Verbreitung zuerst) und Glieder (U14 bis U16, alle drei Testformen, gängige Testbatterien) sind eigen. P2 beseitigt zugleich die Nähe zum Titel („Reliability and validity of field-based fitness tests“, mit „und valide“ fünf sinngleiche Wörter in Folge). Gegenstellen zur Reliabilität bleiben für 6.2 vorgemerkt (B3 bis B5 § 7): Ferguson et al. (2024) mit moderater Reliabilität über 5 und 10 m und systematischen Unterschieden zwischen den Terminen, Taylor et al. (2018) zum modifizierten 505 in Akademien. Die Gegenbefundpflicht gilt in der Einleitung nur für Wirksamkeits- und Erwartungsaussagen (Quellenraster § 2.2).

### 2.6 Zweitprüfung (unabhängiger Subagent, 30.09., Bericht `03_Skripte\Abgleich_Einleitung_2026-09-30\zweitpruefung_B3.md`)

Urteil: vorlegbar nach der Berichtigung einer Kopfzahl und zwei Nachträgen in der Belegtabelle. § 2.2 setzt genau P2 um, S5 ist grammatisch richtig („sich erweisen als“ mit Nominativ, „reliable“ mit e-Tilgung wie „variable“, kein Komma zwischen den nicht gleichrangigen Adjektiven) und in der neuen Form am Volltext gedeckt, getragen von Dugdale et al. (2019). S1 bis S4 wortgleich mit dem Textstand, Codes und Register stimmen, keine P- oder P°-Zeile geht verloren (die E-Zeilen 2.4 und E.2 trägt B3 unverändert). 1 A, 2 B, 7 C. Die A- und B-Befunde sind am Volltext und an den Steuerdokumenten nachgeprüft.

| Nr. | Schwere | Befund | Umsetzung |
|---|---|---|---|
| 1 | A | Seitenprognose „rund 27,7“ falsch gerundet, 27,7549 ergibt 27,8 | berichtigt. Das Skript gibt jetzt vier Nachkommastellen und den gerundeten Wert aus |
| 2 | B | Passung: Ferguson et al. (2024) mit Passung 1 ohne Nennung im Satz, Klasse a verlangt Passung 0 | Passung je Quelle in § 2.5, Variante gemessen (§ 2.1, § 2.2, § 2.4), Klickfrage § 2.7, entschieden 18:46: ohne Ferguson. Nachgeprüft: Quellenraster § 2.1 und Zeilen 2.5, 2.6, 2.14, Startprompt, Ferguson S. e97 wörtlich. Dazu der Befund der Quelle selbst (S. e99, T4 Z. 41), der „reliabel“ für 5 und 10 m einschränkt |
| 3 | B | Hicks: AoP-S. 1 bis 2 trägt „vor allem“ und „kurze Bodenkontakte“ nicht ganz | AoP-S. 4 und 9 mit Wortlaut in § 2.5, am PDF nachgeprüft. Wortlaut von S1 bleibt |
| 4 | C | Übersetzungsnähe nicht geprüft, Schlussabsatz ungenau | Prüfung nach Quellenraster § 2.5 Nr. 5 im Schlussabsatz von § 2.5 |
| 5 | C | T4-Spalte S5 unvollständig, T1 mit falschem ICC-Typ, Gegenbefund Taylor et al. (2018) | `Dugdale2019` Z. 118 und 131 und `Ferguson2024` Z. 41 in § 2.5, T1 in § 2.8, Taylor im Schlussabsatz (vorgemerkt seit B3 bis B5 § 7) |
| 6 | C | Verbreitungsaussagen als Relais, T4-Nachtrag `Dugdale2020` offen, Anführungszeichen im Prüfzitat S3 | Relais in § 2.5 gekennzeichnet, Prüfzitat zeichengenau, T4-Nachtrag in § 2.8 |
| 7 | C | „Befund § 7 Nr. 2“ mehrdeutig, Einleitungssatz der Zug-Tabelle fehlt | „Befund Argumentationsstruktur § 7 Nr. 2“, Einleitungssatz ergänzt |
| 8 | C | „nur als Trennung von Spielergruppen“ zu eng | „Alters- und Spielergruppen“, am Volltext bestätigt (Ziele ii und iii, OF-S. 2) |
| 9 | C | Herkunft zweier Kopfwerte, § 1.1 verweist auf die überschriebene Ausgabe, im Ordner liegt die Vorfassung des Skripts | Skript zählt Belegklammern und narrative Zitate je Absatz, § 1.1 als Stand nach B1b und vor P2 gekennzeichnet, Skript und Ausgaben gehen mit diesem Absatz in den Ordner |
| 10 | C | T1-Spalte „kapitel“ veraltet, `Dugdale2020` als „nicht zitiert“ geführt | § 2.8 (Task 15) |

### 2.7 Klick

Freigabe B3: (a) freigeben mit P2 und S5 ohne Ferguson et al. (2024), Variante § 2.2 (Empfehlung) · (b) freigeben wie § 2.2, Ferguson et al. (2024) bleibt, die Abweichung von der Passungsregel steht in § 2.5 · (c) nicht freigeben, mit Angabe, was sich ändern soll.

**Entschieden (Klick 30.09., 18:46 Sitzungsuhr): (a).** B3 ist freigegeben mit P2 und S5 ohne Ferguson et al. (2024). Der Verfasser überträgt. Freigegebener Wortlaut (121 Wörter, S1 29 · S2 29 · S3 20 · S4 17 · S5 26, gleich `schritt4_stand.json`):

Im Sprint entscheidet in der Beschleunigungsphase vor allem die horizontale Ausrichtung der Bodenreaktionskraft, in der Phase maximaler Geschwindigkeit eine hohe vertikale Kraft in kurzen Bodenkontakten (Hicks et al., 2020). Da beide Phasen eine unterschiedliche Kraftentwicklung verlangen, werden Sprintzeiten bis 10 m der Beschleunigung und Zeiten über 15 bis 40 m der maximalen Geschwindigkeit zugeordnet (Oliver et al., 2024). Entschleunigen und erneutes Beschleunigen fordert der 505-Test, der in seinen Varianten zu den gebräuchlichsten Richtungswechseltests gehört (Dugdale et al., 2020). Der Standweitsprung ist ein bei Kindern und Jugendlichen international verbreiteter Feldtest der Schnellkraft (Tomkinson et al., 2021). Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019).

Stand der Einleitung nach B3: 907 Wörter (ohne Belegklammern 755), 39 Sätze, Median 24,0, längster Satz 32 (B5 S1), 22 Quellen, Seitenprognose rund 27,7 (27,74, Modellrechnung).

### 2.8 Vormerkungen aus B3

- **T1 `Ferguson2024`:** d_pop 0 → 1 (Akademie, F17 § 6.4 „Nachwuchs anderer Stufe/Niveau“), „ICC(2,1)-Typ“ → ICC3,1 (S. e98, Quellenraster Zeile 2.5), in Task 15.
- **T1, Spalte „kapitel“:** `Dugdale2019`, `Dugdale2020` (jetzt in B3 S3 zitiert, nicht mehr „nicht zitiert“), `Ferguson2024`, `Hicks2019`, `Oliver2024`, `Tomkinson2021` auf die Einleitung nachführen, wie `Roessler2014` (§ 1.8), in Task 15.
- **T4 `Dugdale2020`:** Nachtrag „most commonly selected“ ohne Zahl, Relais auf [10,17–19] (B3 bis B5 § 7), mit dem nächsten `T4_Nachtrag_`-Lauf.
- **6.2 (Task 12):** Gegenstellen zur Reliabilität und Validität des 505-Tests wie B3 bis B5 § 7, dazu die Passung von Ferguson et al. (2024) als Akademiestudie.
- **Ferguson et al. (2024) nach dem Klick 18:46:** Im Master steht die Quelle nur im Altbestand 2.4.1, nicht in 4.4 (Master geprüft 30.09., MD5 `e35315d6…`). Nach der Übertragung der Einleitung ist sie bis 6.2 nirgends zitiert. F17 § 6.5 („dienen 4.4 und 6.2“) trifft damit für 4.4 nicht zu. Ins Literaturverzeichnis nur, wenn 6.2 sie zitiert (F17 § 8 „Noch einzupflegen“, Task 15).

## 3 B4 — Einordnung der Reifung und Lücke (P3, P4)

Vorher nachgetragen (30.09., `03_Skripte\Abgleich_Einleitung_2026-09-30\nachtrag_T1_T4.py`, am PDF geprüft): T1 `Tanner1966` neu, Heftangaben und DOI bei PubMed geprüft (PMID 5957718) · T4 `Tanner1966` zweimal (Standardfehler statt SD und nur Jungen · Kinderheim, Standard 13,9, Deming, Part I) · T4 `Radnor2017` (Begriffe, Sprint nur im Abstract, Modalität, Vormerkung B3 bis B5 § 7) · T1 `Roessler2014` berichtigt (§ 1.8). T1 72, T4 151 Einträge. Nach der Zweitprüfung (§ 3.6 Nr. 9 und 10) sind die Einträge `Tanner1966` in T1 und `Radnor2017` in T4 berichtigt, derselbe Lauf aus dem Stand vor dem Nachtrag.

### 3.1 Kopf (gemessen mit `schritt4_messung.py`, Ausgabe `schritt4_messung.txt`)

| Größe | Neufassung § 3.2 (P3b, P4c) | Variante P4a, DVZ-Bezug gestrichen | Vorgabe oder Vergleich |
|---|---|---|---|
| Wörter B4 | **176** (ohne Belegklammern 152) | 168 (144) | Textstand 153 · Fassung 3 (Freigabe 17:44) 168 · kein Absatz über 250 |
| Einleitung | **930** (ohne Belegklammern 778), 40 Sätze, Median 24,0, längster Satz 32 (B5 S1) | 922 (770), 40 Sätze, Median 23,5 | Obergrenze 1.200 · Korpus 506 bis 927 · Wortbilanz Befund § 4: 912 bis 934 |
| Sätze B4 · Median · längster | 7 · 27,0 · 31 (S6) | 7 · 24,0 · 31 | höchstens 32 |
| Reifeteil (S1 bis S5) | 118 Wörter | 110 Wörter, wie Fassung 3 | Korpusbefund § 6, Zeile B4: schon 110 über dem Korpus, nach den Aufträgen vom 29.09. |
| Semikola außerhalb von Belegklammern · Abschnittsverweise · narrative Zitate (Quelle als Subjekt) | 0 · 0 · 0 | 0 · 0 · 0 | 0 |
| Belegklammern B4 · Quellen der Einleitung | 4 · 22 | 4 · 22 | unverändert |
| Zahlen aus dem Kennzahlenblatt | keine | keine | keine eigenen Studienzahlen, die Altersangaben in S2 sind Literaturwerte (Tanner et al., 1966) wie in Fassung 3 |
| Seitenprognose | rund 27,8 Seiten (27,81) | rund 27,8 (27,79) | Schwelle 32, Grenze 33 · Modellrechnung wie `textstand_T.py`, Parameter aus `Seitenmodell_2026-09-28.csv` |

Die Neufassung kostet 23 Wörter. P3b trägt 19 davon, Grund ist F17 § 6.4 (Einzelbefund mit Population im Satz). P4c trägt 4, gegenüber P4a 8. Grund ist der DVZ-Bezug im Wortlaut des Verfassers und der Anschluss an B1b. Mit P4c liegt die Einleitung 3 Wörter über dem Korpusmaximum, innerhalb der Wortbilanz von Befund § 4. Mit P4a bleibt sie im Korpus.

### 3.2 Wortlaut (Neufassung, Satzzählung für § 3.3 bis § 3.6)

Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel. In einer britischen Längsschnittstudie erreichten Jungen ihn im Mittel mit 14 Jahren, bei einer Spanne von 12 bis 16 Jahren (Tanner et al., 1966). Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018). Einem Training lassen sich Leistungsveränderungen in diesem Alter deshalb verlässlicher zuschreiben, wenn beim Vergleich von Interventions- und Kontrollgruppe der Reifestatus konstant gehalten wird. Plyometrisches Training verbesserte nach einer Metaanalyse zu Kindern und Jugendlichen die meisten Leistungsmerkmale vor wie nach dem Wachstumsgipfel, den Richtungswechsel dagegen in keiner Reifegruppe nachweisbar (Ramirez-Campillo et al., 2023). Die Phase um den Gipfel selbst, Spieler des leistungsorientierten Breitensports und die Übergangsperiode sind in den Metaanalysen eingeschränkt abgebildet (Oliver et al., 2024; Ramirez-Campillo et al., 2023; Zheng et al., 2025). Welches Potenzial ein unbeaufsichtigtes, videobasiertes und gerätefreies plyometrisches Heimtrainingsprogramm in der Sommerpause für U15-Spieler des leistungsorientierten Breitensports bietet, ist nach derzeitigem Kenntnisstand in kontrollierten Studien unzureichend untersucht.

S1 12 · S2 24 · S3 30 · S4 23 · S5 29 · S6 31 · S7 27 Wörter. S1 und S2 wortgleich mit Fassung 3 (Textvorschlag B4 § 1, Freigabe 29.09., 17:44), in der Wortbilanz von Schritt 3 P3b. S3 ist Fassung 3 S3 mit dem DVZ-Bezug des Verfassers in modaler Form (P4c). S4 bis S7 wortgleich mit dem Textstand (T S3 bis S6). Per Assertion in `schritt4_messung.py` geprüft.

**Variante P4a, nur per Klick § 3.7 (b):** S3 wie Fassung 3, ohne DVZ-Bezug: „Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training (Radnor et al., 2018).“ (22 Wörter)

**Für P3 keine Variante.** Erwogen sind die Kandidaten aus der Wortbilanz von Schritt 3 und ein einsätziger Entwurf. P3a und P3c behalten „In dieser Altersspanne“ und damit den Rückgriff auf B3. P3d („Spieler der U15 befinden sich nach einer britischen Längsschnittstudie an Jungen häufig …“) schreibt die U15-Folgerung der Studie zu. Der einsätzige Entwurf P3e („Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel, den Jungen in einer britischen Längsschnittstudie im Mittel mit 14 Jahren erreichten (Tanner et al., 1966).“, 28 Wörter, im Skript gemessen) verliert die Spanne, die Prämisse für S4, die Klammer am Satzende schreibt auch die unbelegte Folgerung Tanner zu, und „den Jungen“ lässt sich zuerst als Artikel mit Nomen lesen (Zweitprüfung Nr. 2). Gleichwertig mit Fassung 3 ist damit keiner.

### 3.3 Zug-Tabelle

Codes nach der Konsenscodierung des Textstands (Befund Anhang A). Die Neufassung teilt T S1 in zwei Sätze. S1 behält K1, S2 ist nach Codebuch E2 (konkret beschriebene Primärstudie) K1 (E2), wie die Konsensentscheidung zu B2 S9. S3 behält K1 (T2) von T S2, mit P4a entfällt T2. Die Zugfolge K1 → L1 → L1 bleibt (Befund Argumentationsstruktur § 6, Zeile B4). Bauregeln nach Befund § 3.3.

| Satz | Code | Zug und Bauregel |
|---|---|---|
| S1 | K1 | Reifung: U15 um den Wachstumsgipfel, Folgerung aus S2 (Register 29.09., 17:12, Freigabe 17:44) · Reife direkt vor der Lücke wie Negra 2020 (Befund Argumentationsstruktur § 6, Zeile B4) · keine Bauregel betroffen |
| S2 | K1 (E2) | Einzelbefund mit Population im Satz (F17 § 6.4), die Spanne trägt die Prämisse für S4 (Textvorschlag B4 § 2 Nr. 1) · keine Bauregel betroffen |
| S3 | K1 (T2) | Reifung steigert die Leistung auch ohne Training („Zuwächse zu was“, 17:12), DVZ-Bezug modal (F17 § 10, wie B1b S3). Mit P4a K1 · keine Bauregel betroffen |
| S4 | K1 | Folgerung: Zuschreibung bei konstant gehaltenem Reifestatus, „verlässlicher“ (17:59, Klick 18:01), Reife als Bedingung, kein Gegenstand (17:12) · Bauregel 4: baut die Designdimension „kontrollierte Studien“ vor dem schließenden Lückensatz auf (Befund § 3.3 c4) |
| S5 | K1 (E1, E3) | Metaanalyse nach Reifegruppen mit Gegenbefund beim Richtungswechsel · Bauregel 3 erfüllt (c3) · unverändert |
| S6 | L1 (K1, K4) | Grenzen der Metaanalysen als Prämisse vor der Kenntnisstandformel · Bauregel 5 teilweise erfüllt: Formel und Prämisse erfüllt, mehr Dimensionen als im Regelfall (c5) · unverändert |
| S7 | L1 (K2, K4) | schließender Lückensatz mit Kenntnisstandformel · Bauregel 5 wie S6 (c5), die zentrale Dimension bauen B2 und S4 auf (Bauregel 4, c4) · unverändert |

### 3.4 Änderungstabelle

| Satz | alt (Textstand, Wortlaut des Verfassers) | neu | Grund |
|---|---|---|---|
| S1, S2 (T S1) | „In dieser Altersspanne befinden sich jugendliche häufig in der Phase um den Wachstumsgipfel (Tanner et al., 1966).“ | „Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel. In einer britischen Längsschnittstudie erreichten Jungen ihn im Mittel mit 14 Jahren, bei einer Spanne von 12 bis 16 Jahren (Tanner et al., 1966).“ | P3 (P3b): Tanner et al. (1966) tragen den Gipfel um 14 Jahre nur für Jungen, Mädchen erreichten ihn im Mittel mit 12,1 Jahren (Tab. I, S. 461). Eine Einzelstudie ohne Population im Satz verstößt gegen F17 § 6.4. „In dieser Altersspanne“ griff über die Absatzgrenze auf die Stichproben der Reliabilitätsstudien in B3 S5 zurück, „jugendliche“ stand klein (Befund § 3.5 w4). Die Neufassung ist wortgleich mit Fassung 3 (Freigabe 17:44): Folgerung in S1, Befund mit Population in S2. Die Spanne zeigt, dass Gleichaltrige unterschiedlich weit gereift sind, und trägt so die Prämisse für S4. +19 Wörter |
| S3 (T S2) | „Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Leistung während des DVZ und infolgedessen die Sprint- und Sprungleistung von Kindern und Jugendlichen (Radnor et al., 2018).“ | „Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018).“ | P4 (P4c, Klick 17:32 „Radnor modal“): Die Kette über den DVZ stand mit „infolgedessen“ im Indikativ, gegen F17 § 10 (Mechanismus modal). „die Leistung während des DVZ“ war doppeldeutig und machte die Kette nahezu zirkulär, gemeint ist die Funktion des DVZ („improved SSC function“). „auch ohne Training“ kehrt zurück, erst damit schließt S4 mit „deshalb“ eindeutig an (Befund § 3.5 w5). Der DVZ-Bezug des Verfassers bleibt als Erklärungsangebot und knüpft an B1b an: Reifung und Training setzen an derselben Muskelaktion an. +4 Wörter |
| S4 bis S7 (T S3 bis S6) | unverändert | | |

### 3.5 Belegtabelle

| Satz | Quelle | Wortlaut oder Fundstelle (nur zur Prüfung) | Seite | Volltext | T1 | T4 |
|---|---|---|---|---|---|---|
| S1 | — | Folgerung aus S2 ohne eigene Klammer. So geführt in Befund § 3.5 w4 („Fassung 3 trennte die Folgerung (S1 ohne Beleg) vom Befund“) und mit der Freigabe 17:44, Textvorschlag B4 § 3 führte S1 und S2 gemeinsam unter Tanner et al. (1966) | — | — | — | — |
| S2 | Tanner et al. (1966) | S. 457: „the age of its occurrence varies greatly“, Harpenden Growth Study mit „49 healthy boys and 41 healthy girls followed … before, during, and after puberty“, im Schub dreimonatlich gemessen · S. 461: „The ages at which peak height velocity was reached averaged, in our data, 14·1 ± 0·13 years for boys and 12·1 ± 0·14 years for girls“ · Tab. I, S. 461 (Seitenbild): Jungen SD 0,93, Spanne 12,0–16,0 | S. 457, S. 461 | ✓ 29.09., Text und Tab. I am 30.09. nachgeprüft (MD5 `c63022b5…`) | `Tanner1966` (neu 30.09.) | `Tanner1966` (neu 30.09.: ± 0,13 ist Standardfehler, nur Jungen · Kinderheim, Standard 13,9, Deming ein halbes Jahr früher, Part I). Ohne Folge: „im Mittel mit 14 Jahren“ deckt 14,1 und 13,9, Population und Geschlecht stehen im Satz |
| S3 | Radnor et al. (2018) | für „steigern … die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training“: Abstract, OF-S. 1: „Innate SSC development throughout childhood and adolescence enables children to increase power (jump higher and sprint faster) as they mature“ · Key Points, OF-S. 1: „Stretch-shortening cycle (SSC) performance increases with age in various forms of hopping, jumping, and sprinting tasks“ · Schluss, OF-S. 11: „As children transition towards adulthood they demonstrate natural improvements in their ability to perform hopping and jumping tasks“ · Begriffsbestimmung, OF-S. 2: „Natural development represents the increase in physical ability (strength, power, speed, etc.) that is apparent in children as they experience growth and maturation, independent of any specific physical training“ · für den DVZ-Bezug: Key Points, OF-S. 1: „these adaptations may result in an improved SSC function“ · Schluss, OF-S. 11: „resulting in an improved SSC function“ | OF-S. 1, 2, 11 | ✓ 30.09. (MD5 `395ea66f…`) | `Radnor2017` | `Radnor2017` (Online-First, zitiert als 2018 · neu 30.09.: „children“ meint Jungen bis etwa 13 Jahre, „youth“ Kinder und Jugendliche, Sprint nur in Abstract und Key Points, DVZ-Funktion nur in den Key Points modal). „Kindern und Jugendlichen“ gibt „youth“ wieder (Titel, Abstract „throughout childhood and adolescence“). Die Sprintleistung stützen nur Abstract und Key Points, Hauptteil und Schluss nennen Hüpfen und Springen (Quellenraster Zeile 5.2). Mit Sprint steht der Satz so seit Fassung 3 (Freigabe 17:44). Modal steht der DVZ-Bezug nach F17 § 10, Abstract und Schluss formulieren indikativ |
| S4 | — | eigene Folgerung aus S2 und S3 (Textvorschlag B4 § 3) | — | — | — | — |
| S5 bis S7 | wie Textstand | Belegtabellen Textvorschlag B3 bis B5 § 4 und B4 § 3 | — | unverändert | — | — |

**Passung (Quellenraster § 2.1).** Maßstab ist § 2.1 des Quellenrasters: Passung 0 Pflicht, Passung 1 nur mit Nennung der Abweichung im Satz. Die Kurzfassung „nur Passung 0“ im Startprompt ist nach Befund § 2.2 Nr. 3 ungenau. S2 (Tanner et al., 1966) verortet den Gipfel, im Quellenraster Zug 5 Kette Nr. 1 mit Passung 1 und Population im Satz vorgesehen (damals für Malina & Kozieł, 2014). Tanner hat Passung 1 (britische Jungen ohne Sportbezug aus einem Kinderheim), „britische Längsschnittstudie“ und „Jungen“ stehen im Satz, also zulässig. Das Quellenraster führte Tanner unter „Nicht verwenden“ (n = 49, Standardfehler statt SD), der Verfasser hat Tanner am 29.09., 17:12 bestimmt, die Zahlen stehen ohne Streuungsmaß. S3 (Radnor et al., 2018) ist Klasse a („Reifeeffekt auf die Leistung“) mit Passung 1 (Übersicht über Kinder und Jugendliche beider Geschlechter, nicht fußballspezifisch, Quellenraster Zeile 5.2, T1 d_pop 1). Die Abweichung steht mit „Nach einer Übersichtsarbeit“ und „von Kindern und Jugendlichen“ im Satz, also zulässig. Eine Übersicht der Passung 0 zum Reifeeffekt liegt nicht im Ordner. Den Satz tragen außerdem der Auftrag vom 29.09., 12:54 („Reviews geben hier die Substanz“), die Freigabe 17:44 und der Klick 17:32. Der Unterschied zu Ferguson et al. (2024) in B3 S5: Dort stand die Abweichung nicht im Satz.

Keine neue Quelle. Übersetzungsnähe (Quellenraster § 2.5 Nr. 5): S2 gibt den Befund mit eigenem Satzbau wieder (Studienart, Population, Mittel und Spanne), Fassung 3 war darauf zweitgeprüft (B4 § 4, keine Übersetzungsnähe). In S3 entsprechen „verbesserte Funktion des DVZ“ und „improved SSC function“ einander mit drei sinngleichen Wörtern in anderer Folge, unter der Meldeschwelle. Die Abstract-Formel „jump higher and sprint faster as they mature“ ist nicht übernommen.

### 3.6 Zweitprüfung (unabhängiger Subagent, 30.09., Bericht `03_Skripte\Abgleich_Einleitung_2026-09-30\zweitpruefung_B4.md`)

Urteil: vorlegbar nach Umsetzung der vier B-Befunde. Der Wortlaut ist am Volltext gedeckt, hält die Regeln ein und setzt genau P3 und P4 um, S1 und S2 zeichengleich mit Fassung 3, S4 bis S7 mit T S3 bis S6. Kopfzahlen und der Nachtrag T1/T4 sind byte-gleich reproduziert. S1 trägt als Folgerung, „deshalb“ in S4 trägt weiter, keine P- oder P°-Zeile geht verloren. 0 A, 4 B, 8 C. Die A- und B-Befunde sind am Volltext und an den Steuerdokumenten nachgeprüft.

| Nr. | Schwere | Befund | Umsetzung |
|---|---|---|---|
| 1 | B | Optionsnamen kollidierten mit der Wortbilanz von Schritt 3 (P3b, P4c, P4a), P3e ohne Herleitung | Namen nach der Wortbilanz in § 3.1, § 3.2, § 3.7, § 3.8. P3e hergeleitet und nicht zur Wahl gestellt (§ 3.2) |
| 2 | B | Überschreitung des Korpusmaximums F17 § 6.4 zugeschrieben, sie folgt aus P4c. Klickfrage ohne Folgen je Option, Kosten von P3e | Grund je Potenzial im Kopf, Folgen je Option in § 3.7. P3e wegen der Mängel nicht zur Wahl |
| 3 | B | Passung für S2 und S3 nicht geprüft | Passungsabsatz in § 3.5, mit dem Unterschied zu B3 S5 |
| 4 | B | „auch ohne Training“ nur über die Begriffsbestimmung OF-S. 2 belegt, die von „children“ spricht | in § 3.5 Abstract und Schluss zugeordnet, OF-S. 2 als Begriffsbestimmung. Wortlaut bleibt |
| 5 | C | Bauregeln in der Zug-Tabelle: S4 trägt Bauregel 4, S5 Bauregel 3, S6 Bauregel 5 nur teilweise | berichtigt nach Befund § 3.3 c3 bis c5 |
| 6 | C | S2 nach Codebuch K1 (E2), mit P4a entfällt T2 in S3 | übernommen |
| 7 | C | Fundstelle für „Folgerung ohne Beleg“ in S1 | Befund § 3.5 w4 und Freigabe 17:44 genannt, Textvorschlag B4 § 3 richtig wiedergegeben |
| 8 | C | Reifeteil unvollständig angegeben | Kopfzeile Reifeteil je Option, Vormerkung „falls P4c“ |
| 9 | C | T1 `Tanner1966`: „Daten der 1950er und 1960er Jahre“ steht so nicht in Part I | berichtigt: Standards nach den Autoren repräsentativ für die frühen 1960er Jahre (S. 465), Messzeitraum in Part I nicht genannt. Neulauf des Nachtrags |
| 10 | C | T4 `Radnor2017`: Abstract und Schluss indikativ, modal nur die Key Points | berichtigt, dazu „Sprint nur in Abstract und Key Points“ (Quellenraster Zeile 5.2). Neulauf des Nachtrags |
| 11 | C | Sprintleistung nur in Abstract und Key Points, Key-Points-Zitat und Vorbehalt fehlten | in § 3.5 ergänzt |
| 12 | C | Skript und Ausgaben im Ordner noch auf dem Stand B3 | Rückschreibung mit der Freigabe von B4, per MD5 geprüft |

### 3.7 Klick

Freigabe B4 wie § 3.2 mit P3b, dazu für P4:

- **(a) P4c, DVZ-Bezug modal (Empfehlung):** hält den DVZ-Bezug, den der Verfasser in den Satz geschrieben hat, regelkonform und knüpft an B1b an. B4 176 Wörter, Einleitung 930 (3 über dem Korpusmaximum), Reifeteil 118.
- **(b) P4a, DVZ-Bezug gestrichen:** Wortlaut von Fassung 3 S3, freigegeben und zweitgeprüft (17:44), knapper im Sinn des Auftrags vom 29.09., 12:54 („prägnanter“). B4 168 Wörter, Einleitung 922 (im Korpus), Reifeteil 110.
- **(c) nicht freigeben,** mit Angabe, was sich ändern soll.

Die Prämisse für S4 tragen beide Optionen gleich (Spanne in S2, „auch ohne Training“ in S3).

**Entschieden (Klick 30.09., 19:45 Sitzungsuhr): (a) P4c.** B4 ist wie § 3.2 freigegeben, mit P3b und dem DVZ-Bezug in modaler Form. Der Verfasser überträgt. Die Klickfrage war um 19:30 gestellt und wurde um 19:39 abgebrochen, als die App den Startprompt vom Sitzungsbeginn erneut schickte. Um 19:44 wurde sie unverändert neu gestellt. Freigegebener Wortlaut (176 Wörter, S1 12 · S2 24 · S3 30 · S4 23 · S5 29 · S6 31 · S7 27, gleich `schritt4_stand.json`):

Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel. In einer britischen Längsschnittstudie erreichten Jungen ihn im Mittel mit 14 Jahren, bei einer Spanne von 12 bis 16 Jahren (Tanner et al., 1966). Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018). Einem Training lassen sich Leistungsveränderungen in diesem Alter deshalb verlässlicher zuschreiben, wenn beim Vergleich von Interventions- und Kontrollgruppe der Reifestatus konstant gehalten wird. Plyometrisches Training verbesserte nach einer Metaanalyse zu Kindern und Jugendlichen die meisten Leistungsmerkmale vor wie nach dem Wachstumsgipfel, den Richtungswechsel dagegen in keiner Reifegruppe nachweisbar (Ramirez-Campillo et al., 2023). Die Phase um den Gipfel selbst, Spieler des leistungsorientierten Breitensports und die Übergangsperiode sind in den Metaanalysen eingeschränkt abgebildet (Oliver et al., 2024; Ramirez-Campillo et al., 2023; Zheng et al., 2025). Welches Potenzial ein unbeaufsichtigtes, videobasiertes und gerätefreies plyometrisches Heimtrainingsprogramm in der Sommerpause für U15-Spieler des leistungsorientierten Breitensports bietet, ist nach derzeitigem Kenntnisstand in kontrollierten Studien unzureichend untersucht.

Stand der Einleitung nach B4: 930 Wörter (ohne Belegklammern 778), 40 Sätze, Median 24,0, längster Satz 32 (B5 S1), 22 Quellen, Seitenprognose rund 27,8 (27,81, Modellrechnung). 3 Wörter über dem Korpusmaximum von 927, innerhalb der Wortbilanz von Befund § 4 (912 bis 934) und weit unter der Obergrenze von 1.200.

### 3.8 Vormerkungen aus B4

- **Task 15:** Tanner et al. (1966) ins Literaturverzeichnis mit 41(219), 454–471, https://doi.org/10.1136/adc.41.219.454 (PubMed geprüft 30.09.), wie T1.
- **Korpusbefund und Steuerdokumente:** Reifeteil mit 118 statt 110 Wörtern, weil P4c freigegeben ist (Klick 19:45, Befund Argumentationsstruktur § 6, Zeile B4). Die Vormerkungen aus Textvorschlag B4 § 5 zu Fassung 18 und Berichtsraster Rev. 4 gelten weiter.

## 4 B5 — Zweck, Vorgehen, Hypothesen

Kein freigegebenes Potenzial. B5 bleibt wortgleich mit dem Textstand (99 Wörter, 4 Sätze, per Assertion in `schritt4_abschluss.py` geprüft), ohne Neufassung und ohne Zweitprüfung. B5 S1 steht mit „deshalb“ (Register 30.09., 10:00). Der Ankersatz in 6.1 und in der Zusammenfassung bleibt ohne „deshalb“ (Vormerkung aus Schritt 1).

## 5 Die ganze Einleitung im freigegebenen Wortlaut (Schritt 4, Abschluss)

Zusammengesetzt aus `schritt4_stand.json`: B1b wie § 1.2 (Klick 18:02), B3 wie § 2.7 (Klick 18:46), B4 wie § 3.2 (Klick 19:45), B1a, B2 und B5 wortgleich mit dem Textstand. Neu codiert und gemessen mit `03_Skripte\Abgleich_Einleitung_2026-09-30\schritt4_abschluss.py` (Ausgabe `schritt4_abschluss.txt`), Wortzahlen und Seitenprognose aus `schritt4_messung.txt`. Die Kennungen B1a bis B5 sind Arbeitskennungen und gehören nicht in den Master. Die Einleitung hat keine Unterabschnitte, die sechs Absätze stehen ohne Zwischenüberschrift.

### 5.1 Wortlaut

**B1a**

Im Wettkampf von U14- bis U16-Fußballspielern aus Akademievereinen sind Beschleunigungen, Entschleunigungen und Richtungswechsel um 45 bis 135° häufig (Algroy et al., 2021; Havanecz et al., 2026; Parr et al., 2022). Auf sehr hohe Geschwindigkeiten entfällt nur ein kleiner Teil der Laufstrecke (Algroy et al., 2021; Parr et al., 2022). Plyometrisches Training verbessert nach Metaanalysen die Sprint-, Richtungswechsel- und Sprungleistung junger Fußballspieler (Oliver et al., 2024; Ramirez-Campillo et al., 2020; Zheng et al., 2025). Bei der Richtungswechselleistung war die Verbesserung in einer Metaanalyse nur im Illinois-Test nachweisbar, weder im Zickzack-Lauf noch im T-Test (Zheng et al., 2025). In einer weiteren Metaanalyse verbesserten schon Programme bis sieben Wochen Sprint über 20 und 30 m und Sprunghöhe, die 10-m-Zeit dagegen nicht nachweisbar (Ramirez-Campillo et al., 2020). Die Programme, nach denen sich alle drei Leistungen verbesserten, dauerten überwiegend sechs bis zwölf Wochen (Oliver et al., 2024; Zheng et al., 2025), eine Mindestdauer lässt sich daraus nicht ableiten.

**B1b**

Der Dehnungs-Verkürzungs-Zyklus (DVZ) stellt bei Sprung- und Hüpfbewegungen die grundlegende Muskelaktion des plyometrischen Trainings dar (Markovic & Mikulic, 2010). Er verbindet eine exzentrische Dehnung des Muskels mit der unmittelbar folgenden Verkürzung, die dadurch mehr Leistung abgibt als ohne Vordehnung (Radnor et al., 2018). Zu dieser Mehrleistung könnten ein Kraftaufbau schon während der Dehnung, gespeicherte elastische Energie, Dehnreflexe sowie eine neuronale und kontraktile Potenzierung beitragen (Markovic & Mikulic, 2010; Radnor et al., 2018). Mit Bodenkontakten unter 250 ms verläuft der DVZ im Maximalsprint schnell, mit längeren in der 180°-Wende und im Sprung mit Ausholbewegung langsam (Dos’Santos et al., 2018; Lloyd et al., 2011). An Sprint-, Richtungswechsel- und Sprungleistung sind damit schneller und langsamer DVZ beteiligt. Ein Programm mit Übungen beider Formen setzt an dieser gemeinsamen Muskelaktion an (Lloyd et al., 2011). Plyometrische Übungen sind zudem Bestandteil mehrkomponentiger Präventionsprogramme, die in Metaanalysen zum Nachwuchssport Verletzungen verringerten (Olivier et al., 2026; Rössler et al., 2014).

**B2**

In der Sommerpause, der Übergangsperiode zwischen zwei Spielzeiten, wird das Mannschaftstraining unterbrochen oder im Umfang reduziert. Trainingsangebote für diese Zeit müssen daher niedrigschwellig sein, das heißt ohne Aufsicht durch Trainer und ohne Trainingsgeräte auskommen. Plyometrische Trainingsprogramme sind ohne Trainingsgeräte durchführbar, wenn sie aus grundlegenden Sprungübungen wie Sprüngen auf der Stelle und Standsprüngen bestehen. Die Belastung im plyometrischen Training wird unter anderem über Intensität, Umfang und Häufigkeit gesteuert. Die Intensität wird vor allem über die Übungsauswahl bestimmt und der Umfang in Bodenkontakten je Einheit bemessen (Lloyd et al., 2011). Auch ohne Trainingsgeräte lässt sich die Intensität etwa über Sprungrichtung, Bodenkontaktzeit und ein- oder beidbeinige Landung abstufen (Ramirez-Campillo et al., 2023). Da Trainingsvideos diese Belastungsgrößen vorgeben können, ist ein gerätefreies Programm als Heimtraining umsetzbar, ohne Trainingszeiten und Trainer des Vereins zu beanspruchen. Wird das Training unterbrochen oder deutlich reduziert, können trainingsbedingte Anpassungen teilweise oder vollständig verloren gehen, was als Detraining bezeichnet wird (Mujika & Padilla, 2000). Bei U15-Spielern der Akademie eines spanischen Fußball-Erstligisten sanken Sprint- und Sprungleistung nach einer 15-tägigen trainingsfreien Winterpause, während sich die Richtungswechselleistung nicht nachweisbar veränderte (Padrón-Cabo et al., 2025). Im Kindes- und Jugendalter sind die Befunde insgesamt uneinheitlich, da neben Rückgängen auch unveränderte und gestiegene Leistungen berichtet wurden (Asimakidis et al., 2022; Dambel et al., 2025). Die Sommerpause führt damit nicht zwangsläufig zu einem Leistungsverlust, bietet aber ein Zeitfenster, das sich für ein gerätefreies Heimtrainingsprogramm nutzen lässt.

**B3**

Im Sprint entscheidet in der Beschleunigungsphase vor allem die horizontale Ausrichtung der Bodenreaktionskraft, in der Phase maximaler Geschwindigkeit eine hohe vertikale Kraft in kurzen Bodenkontakten (Hicks et al., 2020). Da beide Phasen eine unterschiedliche Kraftentwicklung verlangen, werden Sprintzeiten bis 10 m der Beschleunigung und Zeiten über 15 bis 40 m der maximalen Geschwindigkeit zugeordnet (Oliver et al., 2024). Entschleunigen und erneutes Beschleunigen fordert der 505-Test, der in seinen Varianten zu den gebräuchlichsten Richtungswechseltests gehört (Dugdale et al., 2020). Der Standweitsprung ist ein bei Kindern und Jugendlichen international verbreiteter Feldtest der Schnellkraft (Tomkinson et al., 2021). Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019).

**B4**

Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel. In einer britischen Längsschnittstudie erreichten Jungen ihn im Mittel mit 14 Jahren, bei einer Spanne von 12 bis 16 Jahren (Tanner et al., 1966). Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018). Einem Training lassen sich Leistungsveränderungen in diesem Alter deshalb verlässlicher zuschreiben, wenn beim Vergleich von Interventions- und Kontrollgruppe der Reifestatus konstant gehalten wird. Plyometrisches Training verbesserte nach einer Metaanalyse zu Kindern und Jugendlichen die meisten Leistungsmerkmale vor wie nach dem Wachstumsgipfel, den Richtungswechsel dagegen in keiner Reifegruppe nachweisbar (Ramirez-Campillo et al., 2023). Die Phase um den Gipfel selbst, Spieler des leistungsorientierten Breitensports und die Übergangsperiode sind in den Metaanalysen eingeschränkt abgebildet (Oliver et al., 2024; Ramirez-Campillo et al., 2023; Zheng et al., 2025). Welches Potenzial ein unbeaufsichtigtes, videobasiertes und gerätefreies plyometrisches Heimtrainingsprogramm in der Sommerpause für U15-Spieler des leistungsorientierten Breitensports bietet, ist nach derzeitigem Kenntnisstand in kontrollierten Studien unzureichend untersucht.

**B5**

Ziel der Studie war es deshalb zu prüfen, ob ein sechswöchiges videobasiertes, gerätefreies plyometrisches Heimtrainingsprogramm in der Sommerpause die Sprint-, Richtungswechsel- und Sprungleistung männlicher U15-Fußballspieler des leistungsorientierten Breitensports gegenüber einer Kontrollgruppe verbessert. Dazu wurde eine quasi-experimentelle, kontrollierte Feldstudie mit Leistungsdiagnostik vor und nach der Sommerpause durchgeführt. Die Nullhypothese lautete, dass sich Interventions- und Kontrollgruppe in der Grundgesamtheit nach der Sommerpause nicht in den Veränderungen der Sprint-, Richtungswechsel- und Sprungleistung unterscheiden. Die Alternativhypothese lautete, dass in der Grundgesamtheit die Interventionsgruppe in mindestens einem der drei gleichrangigen Parameter eine bessere Leistungsveränderung zeigt als die Kontrollgruppe, einen geringeren Rückgang oder eine Verbesserung.

### 5.2 Messung

| Absatz | Sätze | Wörter T | Wörter freigegeben | Differenz | ohne Belegklammern | längster Satz | Median | Belegklammern |
|---|---|---|---|---|---|---|---|---|
| B1a | 6 | 153 | 153 | 0 | 105 | 30 | 25,5 | 6 |
| B1b | 7 | 152 | 152 | 0 | 116 | 30 | 22,0 | 6 |
| B2 | 11 | 229 | 229 | 0 | 205 | 27 | 21,0 | 5 |
| B3 | 5 | 127 | 121 | −6 | 101 | 29 | 26,0 | 5 |
| B4 | 7 | 153 | 176 | +23 | 152 | 31 | 27,0 | 4 |
| B5 | 4 | 99 | 99 | 0 | 99 | 32 | 26,5 | 0 |
| **Einleitung** | **40** | **913** | **930** | **+17** | **778** | **32 (B5 S1)** | **24,0** | **26** |

Semikola außerhalb von Belegklammern 0 · Abschnittsverweise 0 · Doppelpunkte außerhalb von Belegklammern 0 · narrative Zitate (Quelle als Subjekt) 0 · Sätze mit Beleg 26 von 40 (65,0 %) · Quellen 22 (Ferguson et al., 2024, entfällt mit B3) · Zahlen aus dem Kennzahlenblatt keine · Seitenprognose rund 27,8 Seiten (27,81, Modellrechnung wie `textstand_T.py`, Parameter aus `Seitenmodell_2026-09-28.csv`, Schwelle 32, Grenze 33). Obergrenze 1.200 Wörter eingehalten. Gegen den Korpus der zehn Kern-RCTs (Minimum, Median, Maximum): Wörter 506, 666, 927, die Einleitung liegt 3 Wörter über dem Maximum, innerhalb der Wortbilanz von Befund § 4 · Sätze 15, 22, 34, darüber wie schon der Textstand · Satzlänge im Median 27,0, 30,2, 31,0, darunter wie der Textstand, beides Folge der Projektregeln (kein Satz über 32 Wörter, kein Semikolon) · Sätze mit Beleg 60,7, 74,2, 87,0 %, in der Spanne.

### 5.3 Codierung, Anteile und Grundfigur

Codiert nach `codebook.md` (Fassung 1): unveränderte Sätze mit dem Konsens aus Befund Anhang A, geänderte nach den Zug-Tabellen § 1.3, § 2.3 und § 3.3, dort je vom unabhängigen Zweitprüfer geprüft. Keine erneute Blindcodierung. Geändert haben sich nur die Satzgrenzen in B4: T S1 ist jetzt S1 K1 und S2 K1 (E2), S3 bis S7 tragen die Codes von T S2 bis S6. Die Codes von B1b S1 (T2), B1b S7 (T3 mit E1) und B3 S5 (D1) bleiben.

| Primärcode (Wortanteil in %) | R | T | E | K | D | L | Z |
|---|---|---|---|---|---|---|---|
| Textstand T | 11,0 | 31,8 | 5,5 | 20,7 | 13,9 | 6,4 | 10,8 |
| freigegeben | 10,8 | 31,2 | 5,4 | 22,8 | 13,0 | 6,2 | 10,6 |
| Korpus Minimum bis Maximum (Median) | 5,3 bis 43,0 (19,1) | 5,4 bis 39,5 (16,1) | 7,2 bis 39,3 (18,4) | 0,0 bis 25,0 (5,5) | 0,0 bis 28,5 (0,0) | 4,2 bis 28,5 (20,5) | 4,7 bis 22,6 (9,3) |

Zugfolge unverändert (R T E K T K T R E K D K L Z), ebenso die Absatzdominanz (K T T D K Z) und das Vorkommen aller Funktionen. Der Kontextanteil steigt mit dem Reifeteil um 2,1 Punkte und bleibt in der Korpusspanne. Der Evidenzanteil liegt wie im Textstand unter der Spanne (codierabhängig, Befund § 3.1, geprüft ohne neuen Grund in § 4). Die Grundfigur ist unverändert: Ende mit Lücke und Zweck, Zweck als Folgerung („deshalb“), Lückensatz vor dem Zweck (jetzt B4 S7), Eröffnung mit Relevanz, Relevanz vor Trainingsmittel vor Lücke vor Zweck, Kontext zwischen Trainingsmittel und Lücke, Trainingsmittel im ersten Absatz mit Begründung im selben Satz, Schluss mit Hypothese. Nicht erfüllt bleibt wie im Textstand: Lücke und Zweck im selben Absatz (8 von 10 im Korpus, Befund § 4 ohne neuen Grund).

### 5.4 Änderungen gegenüber dem Textstand (für die Übertragung)

Fünf Stellen, alle übrigen Sätze sind wortgleich mit dem Textstand (Befund § 1.3). Satznummern nach dem freigegebenen Stand, in Klammern nach dem Textstand.

| Ort | Wortlaut im Textstand | freigegebener Wortlaut | Potenzial, Klick |
|---|---|---|---|
| B1b S1 | „Der Dehnungs-Verkürzungs-Zyklus (DVZ), stellt bei Sprung- und Hüpfbewegungen den grundlegenden Wirkmechanismus der Trainingsform dar (Markovic & Mikulic, 2010).“ | „Der Dehnungs-Verkürzungs-Zyklus (DVZ) stellt bei Sprung- und Hüpfbewegungen die grundlegende Muskelaktion des plyometrischen Trainings dar (Markovic & Mikulic, 2010).“ | P1, Klick 18:02 |
| B1b S7 | „Plyometrische Übungen sind zudem Bestandteil mehrkomponentiger Präventionsprogramme, die in Metaanalysen zum Nachwuchssport Verletzungen verringerten und (Olivier et al., 2026; Rössler et al., 2014).“ | „Plyometrische Übungen sind zudem Bestandteil mehrkomponentiger Präventionsprogramme, die in Metaanalysen zum Nachwuchssport Verletzungen verringerten (Olivier et al., 2026; Rössler et al., 2014).“ | P9, Klick 18:02 |
| B3 S5 | „Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable und valide feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019; Ferguson et al., 2024).“ | „Im Nachwuchsfußball gehören alle drei Testformen zu gängigen Testbatterien und erwiesen sich bei U14- bis U16-Spielern zwischen Testtagen als reliable feldbasierte Leistungsdiagnostiktests (Dugdale et al., 2019).“ | P2 und Passung, Klick 18:46 |
| B4 S1 und S2 (T S1) | „In dieser Altersspanne befinden sich jugendliche häufig in der Phase um den Wachstumsgipfel (Tanner et al., 1966).“ | „Spieler der U15 befinden sich häufig in der Phase um den Wachstumsgipfel. In einer britischen Längsschnittstudie erreichten Jungen ihn im Mittel mit 14 Jahren, bei einer Spanne von 12 bis 16 Jahren (Tanner et al., 1966).“ | P3b, Klick 19:45 |
| B4 S3 (T S2) | „Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Leistung während des DVZ und infolgedessen die Sprint- und Sprungleistung von Kindern und Jugendlichen (Radnor et al., 2018).“ | „Nach einer Übersichtsarbeit steigern Wachstum und Reifung die Sprint- und Sprungleistung von Kindern und Jugendlichen auch ohne Training, wozu eine verbesserte Funktion des DVZ beitragen könnte (Radnor et al., 2018).“ | P4c, Klick 19:45 |

Nach der Übertragung misst das Messskript den Master (`Manuskriptstand_2026-09-25.py`), der Abgleich gegen § 5.1 ist vorgemerkt. Offene Vormerkungen stehen in § 1.8, § 2.8 und § 3.8.

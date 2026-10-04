# Codebuch Satzfunktionen in Ergebnisteilen von Interventionsstudien (Fassung 2, 02.10.2026)

Fassung 1 ging an beide Codierer. Fassung 2 hält fest, wie die Abweichungen entschieden wurden (Abschnitt „Klarstellungen aus der Adjudikation“), die Übereinstimmungswerte gelten für Fassung 1.

Einheit: Satz. Je Satz genau ein Primärcode (die Funktion, die der Satz im Bericht erfüllt) und bis zu zwei Sekundärcodes (weitere Inhalte, die der Satz trägt). Codiert wird die Funktion im Bericht, nicht das Thema einzelner Wörter. Dazu je Satz die Zielgröße, über die er berichtet (Feld `zg`), und ob er deutet (Feld `deutung`, 1 oder 0).

## O — Orientierung (Rahmen, bevor oder neben den Befunden)
- O1 Teilnehmerfluss und Analysepopulation: Ausfälle, Ausschlüsse mit Grund, „received treatment as allocated“, Zahl der analysierten Teilnehmer, Einschluss in die Analyse.
- O2 Umsetzung der Intervention: Adhärenz, Compliance, Anwesenheit, erhaltene Dosis, verpasste Einheiten und ihre Gründe, Rücklauf des Monitorings, Dauer der Einheiten wie durchgeführt.
- O3 Beanspruchung und Begleitbedingungen: RPE oder sRPE, Expositionsstunden, Training oder Vorbeugemaßnahmen der Kontrollgruppe, sonstige Bedingungen neben der Intervention.
- O4 Ausgangslage: Stichprobenmerkmale, Ausgangswerte, Vergleich der Gruppen zu Beginn (mit oder ohne Test), auch Veränderungen von Größe und Masse als Kennwerte der Stichprobe.
- O5 Messgüte: Reliabilität, typischer Fehler, Variationskoeffizient, kleinste bedeutsame Veränderung (SWC, SESOI), gültige Versuche.

## V — Verfahrensbezug (Analyse, im Ergebnisteil berichtet)
- V1 Datenprüfung und Voraussetzungen: Verteilungsprüfung, Voraussetzungen, Ausreißer, Prüfung des Modells.
- V2 Analyseregel im Ergebnisteil: Definitionen, Schwellen und Einschlussregeln (etwa „acceptable compliance as 75 %“, „included regardless of compliance“) oder Modellentscheidungen (Kovariate aufgenommen), die im Ergebnisteil stehen.

## X — Objektverweis und Gliederung
- X1 Objektverweis als Satzfunktion: Der Hauptsatz verweist auf eine Tabelle oder Abbildung und beschreibt, was dort steht (Objekt als Subjekt oder Ort, etwa „Table 3 displays …“, „… are presented in Table 2.“). Trägt ein zweiter Hauptsatz einen Befund, ist dieser Sekundärcode. Ein Befundsatz mit Verweis in Klammer ist kein X1.
- X2 Gliederungssatz: kündigt einen Block an oder benennt ihn, ohne Befund und ohne Objekt (etwa ein Satz in der Form einer Überschrift).

## B — Befund
- B1 Gruppenvergleich: Wechselwirkung Gruppe × Zeit, Unterschied zwischen Gruppen in der Veränderung oder im Post-Wert, adjustierte Differenz, Vergleich zweier Trainingsformen oder Bedingungen. Auch in Studien ohne Kontrollgruppe, wenn Gruppen verglichen werden. Auch Post-hoc-Vergleiche zwischen Gruppen.
- B2 Veränderung innerhalb einer Gruppe: Haupteffekt Zeit, Prä-Post-Veränderung je Gruppe, Effektstärke einer Veränderung innerhalb einer Gruppe, Post-hoc-Vergleiche innerhalb einer Gruppe.
- B3 Moderator-, Haupt- oder Untergruppeneffekt: Effekte von Reife, Alter, Altersgruppe oder Geschlecht, Haupteffekt Gruppe ohne Zeitbezug, Untergruppenanalysen.
- B4 Sammelbefund oder Gesamturteil: Der Satz urteilt über alle oder alle übrigen Zielgrößen oder Gruppen, mit Quantor („none of the control groups …“, „all performances …“, „for the remaining tests …“) oder mit der vollständigen Liste ohne Einzelwerte, oder er entscheidet über die Hypothese. Die Art des zusammengefassten Befunds steht als Sekundärcode (B1, B2 oder B3).
- B5 Deskription einer Zielgröße ohne Vergleich: Anzahl, Häufigkeit oder Verteilung einer Zielgröße über alle Teilnehmer, ohne Gruppen- oder Zeitvergleich.

## Z — Zusatz
- Z1 Zusatz- und Sensitivitätsanalysen: Per-Protokoll, Sensitivität, individuelle Antworten, Responder, weitere Analysen außerhalb der Hauptanalyse.
- Z2 Unerwünschte Ereignisse und Schäden: Verletzungen, Krankheit, Schmerzen als Ereignis. Nicht, wenn Verletzungen die Zielgröße der Studie sind (dann B).

## Felder
- `zg` (Zielgröße des Satzes): S Sprint · C Richtungswechsel oder Agilität · J Sprung · A Asymmetrie · Ba Gleichgewicht · E Ausdauer · K Kraft · F Beweglichkeit · M Bewegungsqualität (FMS, AIMS) · V Verletzung · W wiederholte Sprints · X mehrere oder alle · leer, wenn keine Zielgröße. Mehrere mit „+“ in der Reihenfolge der Nennung.
- `deutung` 1, wenn der Satz einen Befund erklärt, bewertet oder einen Schluss zieht, der über die Messung hinausgeht (etwa „suggesting that …“, „This was especially the result of …“, „almost certainly improved“ als Wahrscheinlichkeitsurteil zählt nicht, es ist die Ergebnisform der magnitude-based inference).

## Regeln
1. Ein Befundsatz mit Objektverweis in Klammer bekommt den Code des Befunds, der Verweis wird als Merkmal per Skript gezählt. X1 nur, wenn der Satz keinen Befund trägt.
2. Ausgangsvergleiche sind O4, auch wenn ein Test berichtet wird. Veränderungen von Körperhöhe und Körpermasse über die Studie sind O4 (Stichprobe), nicht B2.
3. Wechselwirkung und Unterschied zwischen Gruppen sind B1, Haupteffekt Zeit und Veränderung je Gruppe B2. Trägt ein Satz beides, entscheidet der Hauptsatz, der andere Befund wird Sekundärcode. Bei zwei gleichrangigen Hauptsätzen entscheidet der erste.
4. Verletzungen: Zielgröße der Studie → B1 oder B2. Grund eines Ausfalls → O1 mit Sekundärcode Z2. Ereignis während der Intervention ohne Ausfall → Z2.
5. B4 nur nach seiner Definition. Eine Aufzählung benannter Zielgrößen mit Einzelwerten oder mit gemeinsamem Befund ohne Quantor ist kein Sammelbefund, sondern B1 oder B2 mit `zg` = X.
6. Nennt ein Satz mehrere Wechselwirkungen gleichrangig, ist die mit der Untersuchungsgruppe B1, die übrigen sind Sekundärcode. Eine dreifache Wechselwirkung mit einem Moderator allein ist B3.
7. Gruppen, die nach Alter oder Reife gebildet sind (etwa U15 gegen U17 in einer Studie ohne Kontrollgruppe), sind Moderatorgruppen: ihre Vergleiche sind B3, nicht B1.

## Klarstellungen aus der Adjudikation (Fassung 2)
- B4: Der Quantor muss alle oder alle übrigen Zielgrößen der Studie erfassen (oder alle Gruppen über alle Zielgrößen). Ein Quantor nur über Gruppen bei einer einzelnen Zielgröße („in every group“) oder nur über die Tests eines Zielgrößenblocks („none of the 3 agility tests“) ist ein Einzelbefund (B1, B2 oder B3). Ein Nebensatz mit Sammelbefund über alle oder alle übrigen Zielgrößen ist Sekundärcode B4, ein Nebensatz über die übrigen Gruppen oder Paarvergleiche einer Zielgröße nicht (berichtigt nach der Zweitprüfung vom 02.10., Liu 3.3).
- Z1: Responder- und Einzelwertdarstellungen sind Z1 nur neben einer Hauptanalyse. Sind sie die Hauptanalyse oder Hauptdarstellung, gilt der Befundcode mit Sekundärcode Z1. Verweist ein X1-Satz auf eine Einzelwertdarstellung, ist Z1 Sekundärcode.
- `zg`: eine Kategorie ihr Code, zwei Kategorien „A+B“ in der Reihenfolge der Nennung, ab drei Kategorien oder bei „alle“ und „übrige“ X. Mehrere Maße einer Kategorie (5, 10, 20 m) ergeben den Code der Kategorie. Line drill ist W. In O-, V- und X-Sätzen steht X, wenn der Satz alle Zielgrößen betrifft.
- O1 gegen O2: „completed the programs“ und „received treatment as allocated“ sind O1 mit O2 als Sekundärcode, Werte der Teilnahme (Prozent, Einheiten) sind O2.
- Regel 4 gilt für Krankheit und Schmerz entsprechend: Grund verpasster Einheiten ist O2 mit Sekundärcode Z2.
- V1 gegen V2: Eine Modellprüfung mit anschließender Entscheidung ist V2 mit Sekundärcode V1.
- `deutung`: Ein Schluss über die Stichprobe, der Ausgangsunterschiede relativiert („suggesting that …“, „Nevertheless, … indicated that all participants were prepubertal“), ist 1. Ein Kausalverb, das eine Veränderung innerhalb einer Gruppe der Intervention zuschreibt („induced“), ist 1. Einordnungen nach einer vorab definierten Schwelle („acceptable reliability“, „poor compliance“) sind 0.

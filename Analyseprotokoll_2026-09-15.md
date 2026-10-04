# Analyseprotokoll — Rechenkette mit vollständigen Daten

**Stand 15.09.2026, abends · Rev. 3** (ersetzt Rev. 2 vom 12.09.) · Datenstand des Workbooks: 15.09.2026, 20:21
Rechenkette `Claude\03_Skripte\Auswertung_B0…B9_2026-09-12.py`, unverändert seit 12.09. — nur die Daten sind neu.
Zahlengrundlage: `Claude\02_Befunde\Kennzahlen_2026-09-15.md`.

---

## 0 Ergebnis in einem Satz

**Die Hauptanalyse zeigt in keiner der drei konfirmatorischen Zielgrößen einen Gruppenunterschied**; alle Effektschätzer liegen unter dem SESOI, alle Konfidenzintervalle schließen die Null ein, und keine der acht vorab festgelegten Sensitivitätsvarianten ändert das Bild.

## 1 Sperre aufgehoben

B7 meldet `STATUS: FREIGEGEBEN — KG-Post-Werte vorhanden`. Die Sperre war am 11.09. gesetzt worden, also vor Kenntnis der Kontrollgruppenwerte; die Rechenkette stand damit fest, bevor die Daten vorlagen (§ 11.10).

## 2 Analysepopulation

| Zielgröße | n IG | n KG | Inferenz |
|---|---:|---:|---|
| Sprint 30 m | 16 | 10 | ja |
| 505 Seitenmittel | 13 | 10 | ja |
| Standweitsprung | 16 | 10 | ja |
| Sprint 5 m | 16 | 7 | nein — KG < 8 (§ 11.9) |
| Sprint 10 m | 7 | 10 | nein — IG < 8 (§ 11.9) |

Gegenüber dem Planungsstand vom 12.09. (Obergrenzen 16/11, 13/10, 16/11) fehlt in der Kontrollgruppe je ein Fall: **VS-07 und VS-16 sind zur Post-Testung nicht angetreten**, **VS-18** hat keine %PAH-Kovariate. **VS-11** wurde am 15.09. vom Verfasser nachgetragen (%PAH = 92,73) und ist vollständig.

Vier Spieler ohne jeden Post-Wert: BW-07, BW-21 (IG) · VS-07, VS-16 (KG). Keine Fortschreibung von Prä-Werten (LOCF), kein Ausschluss aus der Studie — ITT behält alle Zugeteilten, die Nenner fallen je Zielgröße auseinander (CONSORT Item 16).

## 3 Hauptanalyse — ITT, Bestwert, Post ~ Gruppe + Prä + %PAH

| Zielgröße | n | adj. Differenz IG − KG [95 %] | p | Hedges' g [95 %] | unadj. Differenz [95 %] |
|---|---|---|---|---|---|
| Sprint 30 m (s) | 16/10 | −0,046 [−0,200; +0,107] | 0,536 | −0,19 [−0,82; +0,44] | −0,327 [−0,497; −0,156] |
| 505 Seitenmittel (s) | 13/10 | −0,014 [−0,086; +0,057] | 0,678 | −0,14 [−0,81; +0,54] | −0,060 [−0,147; +0,026] |
| Standweitsprung (cm) | 16/10 | +0,2 [−8,3; +8,7] | 0,960 | +0,01 [−0,49; +0,52] | +10,1 [−2,5; +22,7] |

Negatives Vorzeichen bei Zeiten = Interventionsgruppe schneller; positives beim Sprung = weiter. Adjustierte Mittelwerte, Kovariatenkoeffizienten und Kovariatenbereiche in `Auswertung_B7_ANCOVA_2026-09-12.txt`.

**Der Abstand zwischen unadjustierter und adjustierter Differenz ist der eigentliche Befund dieser Tabelle.** Beim 30-m-Sprint schrumpft er von −0,327 s auf −0,046 s, beim Standweitsprung von +10,1 cm auf +0,2 cm. Das ist der Ausgangswertvorsprung der Interventionsgruppe, nicht die Wirkung des Programmangebots — und genau der Grund, aus dem der Ethikantrag die Adjustierung vorsieht. CONSORT Item 18 verlangt beide Zahlen nebeneinander; sie gehören zusammen berichtet, sonst liest sich die unadjustierte Differenz wie ein Effekt.

## 4 Sensitivitätsanalysen — alle acht Varianten

| Variante | 30 m | 505 M | SBJ |
|---|---|---|---|
| ITT · Bestwert (Hauptanalyse) | −0,046 (p = 0,536) | −0,014 (p = 0,678) | +0,2 (p = 0,960) |
| ITT · Mittelwert statt Bestwert | −0,065 (p = 0,402) | +0,004 (p = 0,923) | −2,2 (p = 0,565) |
| Per-Protokoll ≥ 6 | +0,028 (p = 0,794) | n = 7 → deskriptiv | +0,9 (p = 0,865) |
| Per-Protokoll ≥ 5 | −0,000 (p = 0,997) | −0,017 (p = 0,727) | −1,6 (p = 0,767) |
| Per-Protokoll ≥ 7 | +0,029 (p = 0,803) | n = 6 → deskriptiv | −0,5 (p = 0,927) |
| Änderungswert Δ ~ Gruppe + %PAH | +0,048 (p = 0,523) | −0,012 (p = 0,734) | −0,4 (p = 0,931) |
| Modell ohne %PAH | −0,061 (p = 0,372) | −0,008 (p = 0,771) | +1,1 (p = 0,757) |
| + Familiarisierung als Kovariate | −0,095 (p = 0,149) | −0,027 (p = 0,502) | +2,5 (p = 0,582) |

Kein p-Wert unter 0,05; alle Effektstärken zwischen −0,39 und +0,20. Die Vorzeichenwechsel (Per-Protokoll beim 30 m, Mittelwert beim Standweitsprung) liegen weit innerhalb der Konfidenzintervalle und tragen keine Aussage.

Damit ist die Frage aus § 11.8 entschieden: **Bestwert- und Mittelwertanalyse weichen nicht ab** — der Bestwert-Bias bleibt als Limitation bestehen, ändert aber kein Ergebnis. Die Per-Protokoll-Rechnung beim 505-Seitenmittel ist mit sieben Spielern nicht auswertbar (§ 11.9).

## 5 Voraussetzungsprüfungen

| Prüfung | 30 m | 505 M | SBJ |
|---|---|---|---|
| Normalverteilung der Residuen (Shapiro-Wilk) | **W = 0,915, p = 0,035 → verworfen** | W = 0,927, p = 0,096 | W = 0,967, p = 0,553 |
| Varianzhomogenität (Brown-Forsythe) | F = 2,30, p = 0,142 | F = 1,12, p = 0,301 | F = 0,78, p = 0,385 |
| Steigungen Gruppe × Prä | F = 0,75, p = 0,395 | F = 0,72, p = 0,407 | F = 1,76, p = 0,199 |
| Steigungen Gruppe × %PAH | F = 1,92, p = 0,180 | F = 0,02, p = 0,889 | F = 0,71, p = 0,408 |
| Linearität (Prä²) | F = 0,82, p = 0,375 | F = 0,13, p = 0,723 | F = 0,34, p = 0,565 |

⚠ **Beim 30-m-Sprint ist die Normalverteilung der Residuen verworfen.** Das ist der einzige Voraussetzungsbefund der Kette und darf nicht unter die Standardformulierung „geprüft und nicht verworfen" (§ 11.9) fallen — die gilt für die übrigen Prüfungen und für die beiden anderen Zielgrößen.

Einordnung: Die ANCOVA ist bei n = 26 gegenüber moderater Abweichung von der Normalverteilung robust, und der Befund betrifft die Residuen, nicht die Rohwerte. Er ändert die Schlussfolgerung nicht — der Punktschätzer liegt bei einem Fünftel des SESOI. **Empfehlung:** den Befund in 5.2 mit Zahl berichten und eine verteilungsfreie Gegenprobe (Rangtransformation oder Bootstrap-Konfidenzintervall) als zusätzliche, nicht vorab festgelegte Sensitivität rechnen — ausdrücklich als post-hoc gekennzeichnet (§ 1.5: Ergänzung, keine Abweichung). Die Alternative, den Befund nur zu erwähnen, ist vertretbar, lässt aber eine Frage offen, die ein Zweitprüfer stellen wird.

## 6 Was im Workbook nachzuziehen ist

| # | Fundstelle | Befund | Folge |
|---|---|---|---|
| 1 | `01_Personen`, Status VS-01…VS-18 | steht auf „Post-Testung ausstehend (Termin 15.09.2026)", obwohl die Werte vorliegen | B4 führt VS-07 und VS-16 nicht als „nicht angetreten"; der Teilnehmerfluss (CONSORT 13a) ist unvollständig |
| 2 | `01_Personen`, VS-07 und VS-16 | kein Post-Wert, keine Bemerkung | Grund eintragen, analog BW-07/BW-21 |
| 3 | `01_Personen`, VS-11 Bemerkung | „Zeile nachträglich ergänzt – Geburtsdatum fehlt" | überholt, seit dem Nachtrag |
| 4 | `01_Personen`, VS-11 Familiarisierung | leer | fehlt für die F2-Sensitivität (§ 11.5) |
| 5 | `01_Personen`, VS-18 `PAH_cm` | „Alter außerhalb" | ⚠ **sachlich falsch**: Alter prä = 13,81 Jahre, die Koeffiziententabelle in `05_KhamisRoche` reicht von 4,0 bis 17,5 Jahren. Ursache ist allein, dass Körperhöhe und -masse als „?" erfasst sind. Die Begründung ist in Projektanweisungen § 3 und im Auswertungsplan zu korrigieren |
| 6 | `01_Personen`, Testdatum_post Verein C | 14.09.2026 | Projektanweisungen § 2 und der Status nennen den 15.09.; das Datum im Manuskript 4.3 danach richten |
| 7 | `02_Rohdaten`, Bemerkungen | „Sytem nicht aufgenommen" (2×), „Fehversuch" (1×) | Tippfehler lassen Auszählungen nach Grund auseinanderfallen |

## 7 Prä-Post-Intervalle, gemessen

| Verein | Prä | Post | Intervall |
|---|---|---|---|
| A (Hohenlind) | 02.07.2026 | 10.09.2026 | 70 Tage = **10,0 Wochen** |
| B (Blau-Weiß) | 14.07.2026 | 01.09.2026 | 49 Tage = **7,0 Wochen** |
| C (Vorwärts Spoho) | 13.07.2026 | 14.09.2026 | 63 Tage = **9,0 Wochen** |

Das Manuskript nennt in 4.1 „sieben bis neun Wochen" — zu korrigieren auf **sieben bis zehn**.

## 8 Offen

1. **B8 neu rechnen.** Die Sensitivitäts-Poweranalyse läuft noch mit „KG = maximal erreichbar" und R²max aus der Messgüte. Jetzt sind die echten n und das gefittete R² verfügbar (30 m 0,777 · 505 M 0,635 · SBJ 0,763). Das Skript verlangt das selbst.
2. **SPSS.** Die Python-Rechnung ist die Gegenprobe; berichtet wird SPSS (§ 11.4). `SPSS_Syntax_2026-09-12.sps` rechnet dieselben Modelle — Werte gegenprüfen (V5), Version eintragen.
3. **Darstellungspipeline** `Auswertung\*.ps1`: Zielgröße 505M nachrüsten, Post-Termine im Kopf von `abbildungen.ps1` nachtragen.
4. **Verteilungsfreie Gegenprobe** beim 30 m, falls der Empfehlung aus § 5 gefolgt wird.

---

*Erzeugt am 15.09.2026. Rechenkette Rev. 2 unverändert; Läufe protokolliert in den gleichnamigen `.txt` unter `Claude\03_Skripte\`. ANCOVA-Kennwerte zusätzlich maschinenlesbar in `Auswertung\ancova_ergebnisse.csv`.*

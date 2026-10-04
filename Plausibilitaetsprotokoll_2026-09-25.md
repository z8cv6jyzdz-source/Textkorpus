# Plausibilitätsprotokoll Phase 6.4

**Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 6.4 · Stand 25.09.2026**

Geprüfte Datei: `Ergebnisse_R_2026-09-25.csv` (berichtete Rechnung der blinden zweiten Instanz, SHA-256 `3194a805…`). Prüfskript `03_Skripte\Plausibilitaet_2026-09-25.py`, Ausgabe `Plausibilitaet_2026-09-25.txt` (147 Einzelprüfungen mit Urteil). Dieses Protokoll fasst zusammen und enthält die Zahlen, die für das Register gebraucht werden. Es ist keine Zahlenquelle des Manuskripts.

## 1 Ergebnis

**145 von 147 Prüfungen bestanden.** Nenner, Vorzeichen, innere Konsistenz und Größenordnung sind ohne Befund. Die zwei nicht bestandenen Prüfungen betreffen den Vergleich mit der ersten Rechnung vom 15.09.2026 und sind vollständig erklärt (Abschnitt 4): Die Spezifikation berechnet %PAH nach einer anderen Regel als die Workbook-Spalte, aus der die erste Rechnung und das Kennzahlenblatt vom 22.09. den Reifestatus übernommen hatten. Die Schlusslogik ändert sich dadurch nicht.

## 2 Nenner gegen Teilnehmerfluss (39 Prüfungen, alle bestanden)

- 31 Spieler in den Personendaten, IG 18 und KG 13, Vereine A 7, B 11, C 13. Versuchsdaten 1 116 Zeilen (36 je Spieler). Fragebogen 111 Meldungen.
- Teilnehmerfluss: zugeteilt = Personendaten, jeder Spieler mit mindestens einem gültigen Prä-Versuch, Status ausgewertet plus nicht angetreten = zugeteilt in jeder Menge, nicht angetreten 4 (IG 2, KG 2), ohne %PAH 1 (KG, VS-18), Box 6 identisch mit dem Fluss.
- ITT-Sets je Zielgröße wie das Kennzahlenblatt K-07 (5 m 16/7 · 10 m 7/10 · 30 m 16/10 · 505 links 15/10 · 505 rechts 14/10 · Standweitsprung 16/10 · 505-Mittel 13/10), Mitgliedschaften summieren zu den Setgrößen, Nenner in S12, S13, S15 und S18 stimmen mit S08 überein (df = N − 4, df_g = N − 2). PP5 ≥ PP6 ≥ PP7 ≥ AK9 in der IG, KG-Teil der PP-Sets gleich dem ITT-KG. INF = 1 genau bei mindestens acht Spielern je Gruppe (505-Mittel: PP6 und PP7 nicht inferenzfähig).
- Analysepopulation ANA: IG 16, KG 10 (K-01.14). Familiarisierung: IG 10 mal ein Termin und 8 mal zwei, KG 13 mal zwei (VS-11 in Phase 1 nachgetragen).
- Fragebogen: 111 Meldungen, 7 korrigiert, 92 ganz, 6 teilweise, 13 gar nicht, Summen und Raten konsistent, Verteilung 0 bis 12 summiert zu 18, Schwellenlandschaft ≥ 4 bis ≥ 9: 12, 11, 10, 8, 5, 3, 15 Spieler mit Meldung, 12 Meldungen mit Beschwerden bei 9 Spielern (Fragebogenauswertung 12.09.).
- Versuche: je Zielgröße und Zeitpunkt 93 Zeilen = gültig plus ungültig je Kategorie, 12 NANG-Zeilen post je Zielgröße (vier Spieler mal drei Versuche), 0 auslösegestörte Läufe, 384 gültige Prä-Versuche (K-04.2), Ausfälle prä TECH 94, ZEIT 64, FEHL 16 (K-04.4 bis K-04.6).

## 3 Vorzeichen, innere Konsistenz, Größenordnung (94 Prüfungen, alle bestanden)

- S13: t = b1/SE, p aus der t-Verteilung, KI = b1 ± t·SE, b1 im KI, AM_IG − AM_KG = b1, PREM und PAHM gleich den Mitteln der S04- und S05-Werte im ITT-Set, SIG nach Richtungsregel, H0REJ = 0, NTEST = 3.
- S15: unadjustierte Differenz gleich der Differenz der Post-Mittel, SE, t und p konsistent, g = b1/SD_prä · J mit J aus df = n − 2, |g| unter 0,2.
- S14: Merkmale VERW aus den p-Werten, Freiheitsgrade (BF n − 2, Steigungen n − 5, Vorab n − 4), Quotient der Residuen-SD, Überlappung innerhalb der Gruppengrößen, %PAH-Bereiche innerhalb 80 bis 100.
- S19: Bootstrap-Grenzen schließen b1 ein, Breite zwischen 0,6 und 1,4 der t-Breite, 10 000 Ziehungen.
- S18: MDESR = MDES/0,2, F_crit aus der F-Verteilung, Power steigt mit d, MDES zwischen 0,5 und 2 SD-Einheiten, Power bei d = 0,06 und 0,11 (10 m) unter 0,10.
- S10 und S11: SESOI = 0,2·S, RTS = TE/SESOI, TE > SESOI bei allen sieben Zielgrößen (FLEINZ = 1), TE innerhalb seines χ²-Intervalls, TE kleiner als die Zwischen-Athleten-SD, Bestwert-Bias prä in günstiger Richtung.
- S04 und S05: 505-Mittel gleich dem Mittel der Seiten-Bestwerte, Bestwert vor dem Mittelwert (Zeiten kleiner, Sprung größer), %PAH zwischen 80 und 100, PAS zwischen 60 und 80 Zoll.
- Größenordnung: Sprint 5 m 0,8 bis 1,5 s, 10 m 1,5 bis 2,5 s, 30 m 3,8 bis 6,0 s, 505 2,0 bis 3,5 s, Standweitsprung 150 bis 290 cm, Alter 13,5 bis 15,5 Jahre, Körperhöhe 155 bis 190 cm, Körpermasse 40 bis 80 kg, CV unter 10 Prozent, CR-10-Mittel zwischen 2 und 8, Load zwischen 60 und 320 AU, |b1|/SD_prä unter 0,5, R² zwischen 0,4 und 0,95, Ausgangsunterschiede zugunsten der IG bei allen Zielgrößen.
- Schlusslogik (Umfangsdokument § 5): Bei allen drei konfirmatorischen Zielgrößen schließt das 95-%-KI der adjustierten Differenz −SESOI, 0 und +SESOI ein, also Fall C1, H0 nicht abgelehnt. TE post Verein A beim 30-m-Sprint größer als prä (Belastungsfrage für 6.2, F14 § 11.3).

## 4 Vergleich mit der ersten Rechnung und Ursache der Abweichungen

Von 100 gerundeten Vergleichswerten aus dem Analyseprotokoll vom 15.09. und dem Kennzahlenblatt vom 22.09. liegen 52 innerhalb der Rundungstoleranz, 48 nicht. Unverändert sind alle Größen ohne %PAH: unadjustierte Differenzen, Modell ohne %PAH (OPAH), Messgüte außer dem 505-Mittel, Ausgangswerte, Alter, Körperhöhe, Körpermasse, Versuchszahlen, Adhärenz. Verschoben sind alle Größen mit %PAH: %PAH der Analysepopulation, ANCOVA-Schätzer aller Varianten mit Kovariate %PAH, Residuen und damit Shapiro-Wilk, Brown-Forsythe und Steigungsmodelle.

**Ursache, nachgerechnet:** Die Workbook-Spalte `PAH_Prozent` (Blatt `01_Personen`, Formel in `PAH_cm`) wählt die Koeffizientenzeile der nächsten Halbjahresstufe (`ROUND(Alter·2, 0)/2`), rechnet Pfund mit dem Faktor 2,20462 und rundet PAH_cm auf 0,1 cm. Die Spezifikation S05 interpoliert linear zwischen den benachbarten Halbjahreszeilen (O2), rechnet mit 0,45359237 kg je Pfund (K3) und rundet nicht (0.5 Nr. 1). Mit der Workbook-Formel aus dem Datenstand lassen sich das Kennzahlenblatt (K-02b: %PAH IG 94,65 ± 2,90, KG 90,41 ± 2,85) und die ANCOVA vom 15.09. (30 m b1 −0,046, p 0,536 · 505-Mittel −0,014, p 0,678 · Standweitsprung +0,2, p 0,960) exakt reproduzieren. Die Differenz je Spieler beträgt zwischen −0,63 und +0,55 Prozentpunkte, im Betrag im Mittel 0,29.

Die zweite Abweichung, der TE des 505-Seitenmittels (K-05.7: 0,058 s, jetzt 0,055 s), folgt aus K15: Die erste Rechnung paarte die gültigen Versuche beider Seiten nach ihrer Position in der Liste, die Spezifikation nach der Versuchsnummer. Beides ist als nachträgliche Festlegung im Register dokumentiert (R4 der Tab. 5 des Auswertungsplans).

*Tab. 1.* Alte und neue Werte der Hauptanalyse (Darstellungsregeln des Umfangsdokuments § 3.7)

| Zielgröße | Größe | 15.09.2026 (Workbook-%PAH) | 25.09.2026 (Spezifikation) |
|---|---|---|---|
| Sprint 30 m | adjustierte Differenz [95-%-KI], s | −0,046 [−0,200 bis +0,107] | −0,045 [−0,199 bis +0,110] |
| Sprint 30 m | p | 0,536 | 0,557 |
| Sprint 30 m | Hedges’ g [95-%-KI] | −0,19 [−0,82 bis +0,44] (J mit df = n − 4) | −0,18 [−0,83 bis +0,46] (J mit df = n − 2) |
| 505-Mittel | adjustierte Differenz [95-%-KI], s | −0,014 [−0,086 bis +0,057] | −0,012 [−0,085 bis +0,061] |
| 505-Mittel | p | 0,678 | 0,734 |
| 505-Mittel | Hedges’ g [95-%-KI] | −0,14 [−0,81 bis +0,54] | −0,11 [−0,81 bis +0,58] |
| Standweitsprung | adjustierte Differenz [95-%-KI], cm | +0,2 [−8,3 bis +8,7] | −0,1 [−8,7 bis +8,6] |
| Standweitsprung | p | 0,960 | 0,987 |
| Standweitsprung | Hedges’ g [95-%-KI] | +0,01 [−0,49 bis +0,52] | −0,00 [−0,52 bis +0,51] |
| Shapiro-Wilk 30 m (Residuen) | W, p | 0,915, 0,035, verworfen | 0,915, 0,034, verworfen |
| %PAH Analysepopulation | IG, KG (M ± SD) | 94,65 ± 2,90, 90,41 ± 2,85 | 94,74 ± 2,77, 90,50 ± 2,73 |

Folgen: (1) Der Eintrag gehört als Korrektur mit altem und neuem Ergebnis in das Register (Auswertungsverfahren 2.3, Auswertungsplan § 5.10, neu R11). (2) Das Kennzahlenblatt vom 22.09. ist für alle Größen mit %PAH überholt und wird in Phase 7.1 aus der Ergebnisdatei neu erzeugt, bis dahin sind K-02, K-02b Zeile 4 und die Ergebnisangaben des Analyseprotokolls vom 15.09. nicht in das Manuskript zu übernehmen (F14 § 1.2 Zahlenregel). (3) Der Manuskripttext 4.2 (Rev. 11 vom 22.09.) nennt %PAH-Kennwerte aus K-02b und ist beim Endabgleich 7.3 zu korrigieren. (4) Die Workbook-Spalten `PAH_cm`, `PAH_Prozent` und `Reifeband` sind nach Spezifikation 0.4 keine Eingänge und bleiben unverändert, ihr Rechenweg weicht aber von der berichteten Rechnung ab, das gehört als Hinweis in das Blatt `00_Hinweise` des Workbooks (Verfasser). (5) Die Aussagen des Analyseprotokolls vom 15.09. § 0 und § 3 bleiben inhaltlich gültig: kein Gruppenunterschied nachweisbar, alle Effektschätzer unter dem SESOI, alle Konfidenzintervalle schließen die Null ein, keine Sensitivitätsvariante ändert das Bild.

## 5 Bewertung

Die berichtete Rechnung ist in sich konsistent, ihre Nenner folgen dem Teilnehmerfluss, Vorzeichen und Größenordnungen sind plausibel, und die Unterschiede zur ersten Rechnung sind vollständig auf die datierten, nachträglichen Festlegungen O2, K3, K15 und 0.5 Nr. 1 zurückgeführt. Aus Sicht von 6.4 steht der Freigabe F2 nichts entgegen. Der Verfasser entscheidet mit F2 zugleich, dass die Regel O2 (Interpolation) und nicht die Workbook-Formel die berichtete Rechnung trägt. Das ist bereits Inhalt der Spezifikation (F1 vom 24.09.), wird aber erst jetzt in seiner Wirkung sichtbar.

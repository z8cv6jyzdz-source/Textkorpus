# Auswertungsplan — Vorgehen nach dem Ethikantrag, mit so wenigen Abweichungen wie möglich

**Bachelorarbeit U15-Plyometrie · DSHS Köln · Stand 12.09.2026 (Nachtrag am selben Tag: § 5.9, Versuchszahl, Familiarisierung, Beindominanz) — vor Eintragung der KG-Post-Werte (15.09.) · Arbeitsdokument, kein Manuskripttext · ersetzt `Auswertungsplan_2026-09-11`**

> **Nachtrag 24.09.2026 (Rev. 87):** Was nach dem Sperrdatum 15.09.2026 festgelegt oder geändert wurde, steht im Register § 5.10. Es ersetzt insbesondere A4 (§ 5.2): Berichtet wird die Rechnung in R durch eine zweite, blinde Instanz, nicht in SPSS (F0, Verfasser 24.09.2026). Umgesetzt ist der Plan in `02_Befunde\Spezifikation_2026-09-24` mit Nachtrag 1 und Nachtrag 2. Für die Rechnung ist die Spezifikation maßgeblich. Der Text ab § 0 ist Stand 12.09. und bleibt unverändert. Zahlen darin sind Planungsstand vor den Post-Werten der Kontrollgruppe. § 6 ist keine Betreuerliste mehr: Die Punkte sind seit dem 24.09. Verfasserentscheidungen (Projektanweisungen Fassung 14 § 13). Fehlende Kovariate ist nur noch VS-18 (VS-11 am 15.09. nachgetragen), die Analysepopulation umfasst N = 26 (Kennzahlenblatt vom 22.09., K-01.14).
>
> **Nachtrag 25.09.2026 (Phase 6 und 7):** Das Register § 5.10 trägt die Zeilen R9 bis R14: Festlegungen aus der Blindrechnung (R9), Gegenprobe als neue Fassung der Python-Kette mit bestandenem Abgleich je Kennung (R10), eine Korrektur mit altem und neuem Ergebnis zur Berechnung des Reifestatus (R11), die Handprobe 6.3 als Excel-Formelprobe (R12), Nachtrag 3 zur Spezifikation (R13) und die Verfasserentscheidung, das Erratum zu Khamis und Roche nicht zu beschaffen (R14, O1 endgültig). Nachweise: `02_Befunde\Abgleichprotokoll_2026-09-25`, `Durchsichtsprotokoll_2026-09-25`, `Plausibilitaetsprotokoll_2026-09-25`, `03_Skripte\Handprobe_Pruefung_2026-09-25.txt`, `02_Befunde\Blindpruefung_Spezifikation_2026-09-24` (dritter Lauf), `05_Protokolle\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25`.

**Geltung.** Dieses Dokument ist der operative Auswertungsplan. Leitregel (Verfasser, 12.09.2026): *Der Ethikantrag vom 16.06.2026 ist das Studienprotokoll (CONSORT Item 24). Das Vorgehen folgt ihm. Abgewichen wird nur, wo der Erhebungsstand es bereits erzwungen hat oder wo die Analyse sonst nicht durchführbar wäre; jede Abweichung wird berichtet, keine kaschiert.* Gegenüber dem Plan vom 11.09. sind damit vier Analyseentscheidungen auf den Antrag zurückgeführt (§ 5.2); es bleibt eine einzige erzwungene Analyseabweichung (§ 5.3) und der Erhebungsstand (§ 5.4). Rechenkette: `Claude\03_Skripte\Auswertung_B0…B9_2026-09-12.py` + `.txt` und `SPSS_Syntax_2026-09-12.sps` (Rev. 2 der Kette vom 11.09., Änderungen im Kopf jeder Datei). Es ersetzt in allen Zahlen und Festlegungen: `Auswertungsplan_2026-09-11`, `Statistischer_Analyseplan_2026-09-09`, `Korrelationsbefund_und_Geruest_4.7_2026-09-09`, `Uebergabe_4.7_Statistische_Auswertung.md`. Die `CONSORT_Auswertung_und_Umsetzung_2026-09-09` bleibt als Berichtsstandard-Referenz gültig. Die Projektanweisungen Fassung 9 gelten weiter; die Folgeänderungen für Fassung 10 stehen in § 8.

---

## 0 Kurzfassung

1. **Leitregel:** Antrag vor Optimierung. Was der Antrag festlegt und die Daten hergeben, wird so gerechnet — auch dort, wo eine andere Wahl methodisch vertretbar wäre (§ 1).
2. **Auf den Antrag zurückgeführt** (keine Abweichung mehr): 505-Zeit als **Mittelwert beider Beinseiten** (statt seitengetrennt) · Effektstärke **Hedges' g** (statt η² als Hauptmaß) · Hypothesen im **Wortlaut des Antrags** ohne nachträgliche primäre Zielgröße · **SPSS** als Analysewerkzeug, Python nur als interne Gegenprobe (§ 5.2). Nebenfolgen: COD-Defizit, Asymmetrie- und Beindominanzfragen entfallen; § 11.2 Fassung 9 („seitengetrennt in zwei Modellen“) ist überholt.
3. **Die eine erzwungene Analyseabweichung:** Das Antragskriterium „Adherence unter 75 % → Ausschluss aus der Hauptanalyse“ ließe **3 Spieler** in der IG (BW-02, BW-08, HL-03). Deshalb: Hauptanalyse = alle Zugeteilten (ITT), das Antragskriterium wird deskriptiv berichtet, die Per-Protokoll-Schwelle ≥ 6/12 (Verfasser, 11.09.) als zusätzlicher beobachtender Vergleich (§ 5.3).
4. **Erhebungsstand** (eingetreten, nur zu berichten, keine Entscheidung): 20 m nicht gemessen · Startdistanz 0,5 m · N = 31 statt 45 mit anderer Vereinszuteilung · Termine gestaffelt · KG-Vereinsprogramm · Jahrgang konfundiert · Versuchszahl nicht durchgängig drei · Intervention wie durchgeführt (§ 5.4).
5. **Keine Abweichungen vom Antrag** sind: Familiarisierung (≥ 1 Termin je Spieler, wie vorgesehen; nur die Dosis ist ungleich) und das fehlende KG-Monitoring (der Antrag sah für die KG kein Instrument vor — TESTEX-Lücke, keine Protokollabweichung) (§ 5.5). Beide Punkte verlassen die Betreuerliste.
6. **Ergänzungen, die der Antrag nicht regelt** (Berichtsstandard, keine Abweichung): Sensitivitäts-Poweranalyse statt der nicht erreichten A-priori-Fallzahl · Messgüte aus eigenen Daten · Aggregationsregel Bestwert mit Mittelwert-Sensitivität · Nenner je Analyse · Voraussetzungsprüfung mit Ergebnis (§ 5.6).
7. **Zahlen (Stand 12.09., KG-Post offen):** konfirmatorisch 30 m (16/11), 505 Mittelwert (13/10), Standweitsprung (16/11); deskriptiv 5 m, 10 m, 505 links/rechts. MDES mit Q: 0,58 · 1,21 · 0,77 (2,9 · 6,1 · 3,9 × SESOI). Messgüte 505 Mittelwert: TE 0,059 s, CV 2,3 %, TE/SESOI 2,92 — besser als jede Seite allein (§ 2).
8. **505-Regel** (§ 5.9): Zwei getrennte Operationen — *Versuche* werden wie bei allen Zielgrößen zum Bestwert aggregiert, *Seiten* werden gemittelt (Antrag). Vorbild mit exakt dieser Regel im Nachwuchsfußball: Dugdale et al. (2019, 2020) — „the mean score of the best attempt from each leg“. Der Mittelwert aller Versuche ist die vorab festgelegte Sensitivitätsanalyse; die Frage „Bestwert oder Mittelwert“ ist in der Literatur für U13–U17-Fußballer untersucht (Al Haddad et al., 2015 — Beschaffungsposten).
9. **Versuchszahl präzisiert** (Verfasser 12.09.): Durchgeführt wurden stets mindestens zwei Versuche; k zählt *gültige* Versuche. Bei k = 1 lieferte der zweite Versuch keinen Wert (Fehlversuch oder Lichtschrankenausfall), eine Wiederholung war aus Zeitgründen nicht möglich. Alle sieben Versuchslücken sind seit 12.09. mit Bemerkung versehen (prä 94 technisch · 64 Zeitmangel · 16 Fehlversuch · 0 ohne).
10. **Familiarisierung** (Spalte seit 12.09. aus Anwesenheitslisten): 10 Spieler × 1 (alle sieben von Verein A — dort stand nur ein Termin zur Verfügung — sowie BW-01, BW-02, BW-21), 20 × 2, VS-11 leer. F2 ist damit möglich, aber nur als Kovariate (Variante b, B7 Block F); der Ausschluss der Spieler mit einer Familiarisierung (Variante a) lässt die IG auf n = 5–7 fallen → deskriptiv. Beindominanz wurde nicht erhoben — protokolliert (§ 5.5).
11. **20-m-Schranke** (§ 5.7): Die Begründung „kein Mehrwert neben 10 und 30 m“ ist als Behauptung im Korpus nicht belegt. Belegbar ist die Zwei-Komponenten-Lesart (Beschleunigung 5–10 m, maximale Geschwindigkeit 20–40 m; Ferguson et al., 2024) und die dort berichtete Reliabilität (30 m ICC 0,93 gegen 20 m 0,86, gleicher absoluter Fehler). Formulierung als begründete Entscheidung, nicht als Befund.
12. **Betreuerentscheidungen** (§ 6, Mail am 14.09.): vier statt zehn — Adhärenzkriterium, Hypothesen/Mehrfachtestung, Effektstärkespezifikation, fehlende %PAH. Der Rest ist Kenntnisnahme.
13. **Timing:** Alles hier steht vor Kenntnis der KG-Werte. Nach dem 15.09. läuft die Kette ohne Änderung; jede spätere Änderung an § 2 ist als Abweichung zu dokumentieren.

---

## 1 Grundsatz: dem Antrag folgen, nicht den Korpus nachbauen und nicht nachträglich optimieren

Zwei Versuchungen sind auszuschließen. Die erste ist, den Korpus der Vergleichsstudien als Vorbild zu nehmen — er konvergiert in mehreren schwachen Praktiken (Phase A: Varianzanalyse Zeit × Gruppe ohne Kovariate bei sieben von elf, keine Nenner je Analyse, Effektstärken ohne Konfidenzintervall). Die zweite ist, nach Sichtung der eigenen Daten die Analyse zu verbessern — jede solche Änderung ist eine Abweichung vom vorregistrierten Vorgehen und muss als solche berichtet werden, auch wenn sie methodisch besser ist.

Deshalb gilt seit dem 12.09.: Maßstab ist der Ethikantrag. Der Korpus bleibt Vergleichsfeld für 6.2 (wo liegen wir über, wo unter dem Standard des Felds) und Vorlage für die Darstellung (Sammoud 2024 Tab. 3; Liu 2024 Fig. 2; Padrón-Cabo 2025 Tab. 2). Die Berichtsnormen — CONSORT (Moher et al., 2010), Vickers & Altman (2001), Hopkins (2000) — bestimmen, was zusätzlich zum Antrag berichtet wird; sie ändern nicht, was der Antrag festlegt.

Vier Etiketten je Schritt in § 3: **Antrag** (so im Antrag festgelegt) · **übernommen** (Korpuspraxis, unverändert) · **Ergänzung** (vom Antrag nicht geregelt, aus Normgründen berichtet) · **Abweichung** (vom Antrag abweichend, mit Grund in § 5).

---

## 2 Die Rechenkette — operativer Plan (Stand 12.09.)

Alle Schritte sind gerechnet und dokumentiert (`Claude\03_Skripte\Auswertung_B⟨n⟩_…_2026-09-12.py` + `.txt`). B7 ist gesperrt, bis die KG-Post-Werte eingetragen sind; der freigegebene Pfad wurde am 12.09. mit simulierten KG-Werten technisch geprüft (Ergebnisse ohne Bedeutung, nicht abgelegt). Einzige Datenquelle: `02_Rohdaten` (+ `01_Personen`, Fragebogen-Rohexport).

**Zielgrößen (Antrag § 3, Erhebungsstand):** Sprint 5 m, 10 m, 30 m · 505 als Mittelwert beider Beinseiten (Bestwert je Seite, dann Mittel; nur Spieler mit beiden Seiten) · Standweitsprung (Bestwert). Konfirmatorisch nach § 11.9 (n ≥ 8 je Gruppe): 30 m, 505 Mittelwert, Standweitsprung. Deskriptiv: 5 m (KG-Set n = 7), 10 m (IG-Set n = 7), 505 links und rechts je Seite.

| Schritt | Inhalt | Festlegung / Ergebnis (Stand 12.09.) | Kapitel |
|---|---|---|---|
| B0.1 Mindestdosis | Per-Protokoll = ≥ 6 von 12 vollständige Einheiten (Verfasser 11.09.) · **Antragskriterium ≥ 75 % = ≥ 9/12 ausgewiesen** | ≥ 6: 10 Spieler; PP-Nenner 30 m 9 · SBJ 9 · 505 Mittelwert **7 (< 8 → deskriptiv)** · ≥ 9: 3 Spieler (BW-02, BW-08, HL-03) → nur deskriptiv (§ 5.3) | 4.7, 6.1 |
| B0.2 Gültigkeit | gilt = Wert vorhanden ∧ `ungültig` leer; auslösegestörte Läufe (Abschnittsgeschwindigkeit > 10 m/s) ungültig | 0 Abweichungen zur Blattspalte; kein Lauf betroffen; HL-08 post 10 m V2 = 1,95 s **bleibt** (Verfasser 12.09.) | 4.4 |
| B0.3 Aggregation | Bestwert (Haupt), Mittelwert (Sensitivität); 505 Mittelwert = (Best_L + Best_R)/2 | Bestwert-Bias gemessen: ¼ SESOI je Versuch bei 10 m/30 m/SBJ; 1,4–3,2 SESOI bei 5 m/505 je Seite (n 4–6) | 4.4, 6.1 |
| B0.4 Vokabular | 4 Ausfallkategorien, Originalwortlaut bleibt; Tippfehler „Fehversuch“ ergänzt | prä 94 technisch / 64 Zeitmangel / 16 Fehlversuch / 0 ohne; post IG 5 / 51 / 20 / 27 (falsch aufgenommen) / 0 ohne + 36 nicht angetreten — Verfasser hat die sieben Lücken am 12.09. nachgetragen | 4.4 |
| B0.5 Deskriptiv | 5 m, 10 m, 505 je Seite nur deskriptiv | KG-Set 5 m n = 7; IG-Set 10 m n = 7; Seitenwerte als M ± SD prä/post je Gruppe | 4.7, 5.1 |
| B1 Rohdaten | 1.116 Zeilen, Ausfälle je Kategorie × Gruppe × Zielgröße, Leistungsunabhängigkeit | unverändert gegenüber 11.09. | 4.4 |
| B2 Aggregation | k, Best, Mittel je Zelle; 505 Mittelwert je Spieler; Versuchszahl prä/post | `03_Analyse` zellgenau bestätigt (sechs Rohzielgrößen) | 4.4 |
| B3 Messgüte | TE, TE-KI, CV, SESOI, SESOI_T, MDC — prä/post getrennt, gepoolt; **505 Mittelwert: TE gemessen an gepaarten Versuchen 0,0587 s, Modell √(TE_L² + TE_R²)/2 = 0,0607 s** | 505 Mittelwert prä (n 27): M 2,490, S_b 0,100, CV 2,3 %, SESOI 0,020, TE/SESOI 2,92, TE/√n/SESOI 0,56, MDC 0,163 — gegenüber links 3,89 / rechts 3,55 | 4.4, 6.1 |
| B4 Population | Teilnehmerfluss, Nenner je Analyse, Box-6-Klassen, § 11.9, TESTEX, F2-Machbarkeit | ITT-Sets IG/KG(max): 5 m 16/7 · 10 m 7/11 · 30 m 16/11 · 505 M 13/10 · SBJ 16/11 (505 L 15/10, R 14/11); TESTEX ≥ 85 % nicht erfüllt bei 10 m (38,9 %), 505 M (72,2 %); ohne Spieler mit Familiarisierung = 1 bleiben IG 5–7 → F2-Variante a deskriptiv | 4.7, 5.1 |
| B5 Deskriptiv | Stichprobe, Baseline (n, M, SD, d, Überlappung; keine Tests), Prä→Post IG, Adhärenz, AE | Baseline-d: 30 m −1,68 · 505 M −0,60 · SBJ +0,84 (alle Fälle); ANCOVA-Set −1,70 · −0,56 · +0,65 | 5.1 |
| B6 Voraussetzungen | Überlappung, Steigung %PAH (prä), Linearität, Verteilungen | 505 M: %PAH-Überlappung IG 6/13, KG 9/10; Steigungshomogenität p = 0,606; IG-prä-Verteilung linksschief (W = 0,871, p = 0,029) → am Post-Modell prüfen | 4.7, 5.2 |
| B7 ANCOVA | Post ~ Gruppe + Prä + %PAH je Zielgröße (30 m, 505 M, SBJ); ITT Haupt, PP ≥ 6 zusätzlich, Sensitivitäten | gesperrt; Rechenweg verifiziert (Fehler 1. Art 0,048, Überdeckung 0,952); `--csv` schreibt 30m/505M/SBJ | 5.2 |
| B8 Sensitivität | MDES mit Q je Zielgröße; R² 0,30–0,79; Mittelwert; Änderungswert; ohne %PAH; F2 (Familiarisierung als Kovariate, B7 Block F; deskriptive Δ nach Dosis) | MDES mit Q: 30 m 0,58 (2,9×) · 505 M 1,21 (6,1×) · SBJ 0,77 (3,9×); Faktor SE 1,475 · 1,297 · 1,334; Power bei d = 0,37: 0,43 · 0,14 · 0,27 | 4.7, Anh. G |
| B9 Sets | Zugehörigkeit je Spieler × Zielgröße (ITT / PP ≥ 6 / PP ≥ 9) | Tabelle in B9-Ausgabe | 4.7, 5.1 |
| B10 Darstellung | Pipeline `Auswertung\*.ps1` | § 4 — Zielgröße `505M` in der Pipeline zu ergänzen | 5 |

---

## 3 Gegenüberstellung: Antrag, Korpuspraxis und eigenes Vorgehen

Korpus = elf Interventionsstudien (Lloyd 2016, Hammami 2016, Beato 2018, Negra 2019, Negra 2020, Aloui 2022, Liu 2024, Moran 2024, Sammoud 2024, Bouafif 2026, Padrón-Cabo 2025); Zählungen aus `T6_auswertungspraxis.csv`. „n. b.“ = nicht berichtet.

*Tab. 1.* Auswertungsschritte im Vergleich

| Schritt | Korpuspraxis (von 11) | Eigenes Vorgehen | Etikett | Begründung / Norm |
|---|---|---|---|---|
| Zielgrößen | Sprintsplits 5–30 m üblich; 505 nach Seite/dominantem Bein uneinheitlich | 5, 10, 30 m · 505 Mittelwert beider Seiten · SBJ — wie Antrag § 3 (ohne 20 m: § 5.4 Nr. 1) | Antrag | Antrag § 3; CONSORT Item 6a |
| Versuchszahl je Test | 3 (4 Studien), 2 (3), gemischt (2), n. b. (1) | Protokoll 3; durchgeführt stets ≥ 2, gültig 1–3 (k = gültige Versuche; bei k = 1 war der zweite Versuch ein Fehlversuch oder Schrankenausfall ohne Wiederholungsmöglichkeit), gruppenungleich (B1/B2) | Abweichung (Erhebungsstand) | Keine Studie berichtet ungleiche Versuchszahl; wir berichten k je Gruppe/Zeitpunkt und den gemessenen Bestwert-Bias (§ 11.8) |
| Aggregation der Versuche | Bestwert 9/9 mit Regel; Mittelwert 0 | Bestwert Haupt-, Mittelwert der Versuche als Sensitivitätsanalyse — für alle Zielgrößen, auch 505 je Seite | übernommen + Ergänzung | Antrag: SBJ „bester von drei Versuchen“, für Sprint und 505 nicht festgelegt; der Mittelwert der Versuche ist erwartungstreu unabhängig von k (§ 11.8), der Bestwert nicht — deshalb beide berichten. Literatur zur Frage Best- vs. Mittelwert: Al Haddad et al. (2015, U13–U17-Fußball; Beschaffungsposten) |
| 505-Seiten (Kombination) | seitengetrennt: Nimphius 2016, Clarke 2020, Taylor 2018, Bouafif 2026 · bevorzugter Fuß: Beato 2018, Negra 2019 · **Bestwert je Seite, dann Seitenmittel: Dugdale 2019, Dugdale 2020** | **Mittelwert beider Seiten** aus den Bestwerten je Seite (Antrag; Regel wie Dugdale 2019/2020); Seiten nur deskriptiv | Antrag | Antrag § 3; Item 12a (ein Wert je Spieler); Beindominanz nicht erhoben → dominant/nicht-dominant nicht möglich; Begründung § 5.9 |
| Familiarisierung | 1–2 Termine (7), Routine/keine (3), Probeversuch (1) | je Spieler 1 oder 2 Termine (Anwesenheitslisten): Verein A durchgängig 1 (nur ein Termin verfügbar), B 8 × 2 / 3 × 1, C 12 × 2 | Antrag | Antrag § 5: „vorgeschaltete Familiarisierungseinheit“ — erfüllt; Dosisungleichheit als Limitation und Sensitivität F2 (Kovariate; in der IG mit Verein A konfundiert) |
| Eigene Messgüte | ICC (7), CV (4), TE/SEM/MDC (0) | TE mit 95-%-KI, CV, SESOI und SESOI_T, MDC — prä und post | Ergänzung | Hopkins (2000, S. 8, 13); Vorbild Padrón-Cabo Tab. 2, Aloui Tab. 3 |
| Hypothesen | gerichtete Hypothese 8; keine 3; primäre Zielgröße 0 | **H0/H1 im Wortlaut des Antrags** („mindestens einer der erhobenen Parameter“); keine nachträgliche primäre Zielgröße | Antrag | Antrag § 1; Folge: Mehrfachtestung offen benennen (§ 6 Nr. 2) |
| Analysepopulation | Etikett 0/11; „Completer“ faktisch 11/11 | ITT = alle Zugeteilten mit vollständigen Fällen (Hauptanalyse); Antragskriterium ≥ 75 % deskriptiv; PP ≥ 6 beobachtend; Nenner je Analyse | **Abweichung** (§ 5.3) + Ergänzung | CONSORT Item 16, Box 6; § 11.7; keine Fortschreibung (LOCF) |
| Baseline-Vergleich | Signifikanztest 5; kein Test 3; n. b. 3 | n, M, SD, d, Überlappung — kein Test | Ergänzung | § 4; CONSORT Item 15 |
| Hauptverfahren | ANOVA Zeit × Gruppe 7; ANCOVA mit Ausgangswert 2 | ANCOVA Post ~ Gruppe + Prä + %PAH je Zielgröße | Antrag | Antrag § 1 („ANCOVA mit dem jeweiligen Pre-Test-Wert und dem %PAH als Kovariaten“); Vickers & Altman (2001) mit Grenzen (§ 11.2) |
| Reifestatus | erhoben 8; Kovariate 0 | %PAH kontinuierlich als zweite Kovariate | Antrag | Antrag § 1 („kontinuierliche Größe“, Towlson et al., 2021) |
| Voraussetzungen | genannt, Ergebnis n. b. 6; Steigungshomogenität 0 | Residuen, Brown-Forsythe, Gruppe × Prä, Gruppe × %PAH, Linearität, Überlappung — mit Ergebnis | Ergänzung | § 11.9-Sprachregel: „geprüft und nicht verworfen“ |
| Effektstärke | ohne KI 6; mit KI 4 | **Hedges' g** = adjustierte Differenz / gepoolte Prä-SD, Hedges-korrigiert, mit 95-%-KI; partielles η² nur, weil SPSS es ausgibt | Antrag | Antrag § 1 („Cohens d bzw. Hedges' g“); CONSORT Item 17a (Präzision) |
| Mehrfachtestung | über Zielgrößen 0/11 | keine Adjustierung (Antrag: α = 0,05 je Test); exakte p-Werte; Familienfehler in 6.1 benannt ⟨Schwab⟩ | Antrag | Antrag § 1; § 11.4 |
| Fallzahlbegründung | keine 7; a priori 4 | Antragsrechnung (f = 0,25 → n = 34, geplant 45) als Planungsstand; erreicht N = 31 → Sensitivitäts-Poweranalyse (MDES) | Antrag + Ergänzung | Antrag § 4; Lakens (2022); CONSORT Item 7a |
| Drop-out / Ausfälle | behandelt 3; n. b. 6 | Teilnehmerfluss mit Gründen; Ausfallanalyse; vier Box-6-Klassen | Ergänzung | CONSORT Item 13; Box 6 |
| Adhärenz | berichtet 5 (Prozent ohne Nenner) | Einheiten je Spieler (Nenner 12), Session-RPE — wie Antrag § 3 | Antrag | Antrag § 3 (Adherence-Monitoring); Attendance/Compliance getrennt (§ 4) |
| Unerwünschte Ereignisse | systematisch 0 | 12 Schmerzmeldungen, 9 Spieler, 2 Abbrüche; KG ohne Instrument | Ergänzung | CONSORT Item 19 |
| Flussdiagramm | 4 von 11 | ja, in Anlehnung an CONSORT | übernommen | Item 13a |
| Ergebnistabelle | Sammoud 2024 Tab. 3 | Sammoud-Schablone + Nenner je Gruppe + unadjustierte Differenz + g mit KI | übernommen + Ergänzung | CONSORT Item 17a/18 |
| Software | SPSS 8 (v19–28); JASP 1 | **SPSS** ⟨Version⟩ mit Syntax (Antrag: „SPSS und/oder R“); Python-Rechnung nur interne Gegenprobe, im Text nicht als Analysewerkzeug | Antrag | Antrag § 1; § 11.4 |

**Was daraus für 6.2 folgt.** Über dem Standard des Vergleichsfelds: Messgüte aus eigenen Daten mit KI und MDC, Sensitivitäts-Poweranalyse, Reifekovariate, Nenner je Analyse, vorab festgelegte Sensitivitätsanalysen, Effektstärken mit KI, unerwünschte Ereignisse. Unter dem Standard: Fallzahl (N = 31 gegen 24–85), Versuchszahl, Betreuung (0 von 11 unbeaufsichtigt), Adhärenz (42,6 % gegen 83–96 %).

---

## 4 Darstellungsplan

### 4.1 Was die Pipeline schon leistet

`Auswertung\Erzeuge_Ausgaben.ps1` liest das Workbook (`daten.ps1`), rendert Abbildungen (`abbildungen.ps1`) und Tabellen (`tabellen.ps1`) über `dvs_stil.ps1` und schreibt `ausgabe\protokoll.txt`.

| Objekt (Pipeline-Name) | Inhalt | Kapitel | Status |
|---|---|---|---|
| `Abb_Untersuchungsablauf`, `Abb_Interventionsstruktur` | Zeitstrahlen je Verein / Blöcke | 4.3, 4.5 | rendert; Termine im Kopf von `abbildungen.ps1` sind Stand 27.08. — Post-Termine (01.09./10.09./15.09.) und Familiarisierungstermine nachtragen |
| `Abb_PAH_Ueberlappung` | %PAH je Spieler beider Gruppen | 4.2 / 4.7 | rendert (n = 29) |
| `Abb_Einzelwerte_prae_⟨Ziel⟩` | Prä-Bestwerte je Gruppe, Einzelpunkte mit M ± SD | 5.1 | rendert (sechs Rohzielgrößen) |
| `Abb_Einzelwerte_prae_post_⟨Ziel⟩` | Prä- und Post-Bestwerte beider Gruppen | 5.2 | rendert, sobald Post-Werte stehen |
| `Abb_ANCOVA_adjustiert_⟨Ziel⟩` | adjustierte Mittelwerte mit 95-%-KI | 5.2 | wartet auf `ancova_ergebnisse.csv` |
| `Tab_Stichprobencharakteristika` | Alter, Größe, Gewicht, %PAH je Gruppe | 5.1 | rendert |
| `Tab_Baseline_Praewerte` | n, M, SD, d je Zielgröße | 5.1 | rendert; Überlappungsspalte fehlt |
| `Tab_Messqualitaet` | TE, CV, SESOI, TE/SESOI | 4.4 | rendert; um TE-95-%-KI und MDC erweitern |
| `Tab_Ergebnisse_ANCOVA` | Prä M ± SD · Post M ± SD · adj. M [KI] · adj. Differenz [KI] · p · ES [KI] | 5.2 | wartet auf `ancova_ergebnisse.csv`; Nenner je Gruppe und unadjustierte Differenz ergänzen |

### 4.2 Was zu ergänzen ist (nächster Task, auf dem Rechner)

1. **Zielgröße `505M`** in `daten.ps1` (aus `505L`/`505R` ableiten: Mittel der Bestwerte, nur wenn beide vorhanden), `abbildungen.ps1` (Definition „505 (Mittel beider Seiten)“, Achse 2,10–2,90 s) und `tabellen.ps1`. Bis dahin überspringt die Pipeline die CSV-Zeile `505M` mit Protokollvermerk.
2. **Teilnehmerfluss** (CONSORT-Diagramm) außerhalb der Pipeline (Word/PowerPoint); Felder vor der Zuteilung vom Verfasser.
3. **Adhärenz-Histogramm** (vollständige Einheiten je Spieler, Schwellen ≥ 6 und ≥ 9 markiert) — Quelle B0-Ausgabe § 1; Spalte `Einheiten_ganz` in `01_Personen` nachtragen, dann liest `daten.ps1` sie mit.
4. **Versuchszahl-Übersicht** als Tabelle (`Tab_Versuchszahl`, B2 § 3).
5. **Deskriptive Tabelle** 5 m / 10 m / 505 links / 505 rechts: n, M, SD prä und post je Gruppe, ohne p, ohne ES.
6. **Sensitivitätstabelle** (5.2, kurz): adjustierte Differenz [KI] je Zielgröße für ITT-Bestwert · ITT-Mittelwert · PP ≥ 6 · PP ≥ 5 · PP ≥ 7 · Änderungswert · ohne %PAH; die Antragsteilmenge ≥ 9 nur mit Einzelwerten.

### 4.3 Spaltenvertrag `ancova_ergebnisse.csv` (aus `daten.ps1`)

`Zielgroesse` (30m, 505M, SBJ) · `AdjM_IG` · `KIu_IG` · `KIo_IG` · `AdjM_KG` · `KIu_KG` · `KIo_KG` (Pflicht) · `AdjDiff` · `AdjDiff_KIu` · `AdjDiff_KIo` · `ES` · `ES_KIu` · `ES_KIo` (= Hedges' g mit KI) · `P_Text`. Trenner `;`, UTF-8, `#`-Zeilen sind Kommentare. Maßgeblich ist die SPSS-Ausgabe; `Auswertung_B7_ANCOVA_2026-09-12.py --csv` schreibt die Datei als Gegenprobe (nur nach bestandenem Vergleich V5 für die Pipeline verwenden).

---

## 5 Abweichungsregister — auf das Notwendige reduziert

Quelle: `Ethikantrag_Klier_U15_Plyometrie.pdf` (16.06.2026), Abschnitte 1–5 und 8. Vier Klassen: **5.2** Analyse auf den Antrag zurückgeführt (keine Abweichung mehr) · **5.3** die eine erzwungene Analyseabweichung · **5.4** Erhebungsstand (eingetreten, nur zu berichten) · **5.6** Ergänzungen (vom Antrag nicht geregelt). Berichtsorte nach der Objektzuordnung § 5 der Projektanweisungen.

### 5.1 Leitregel

Eine Abweichung ist zulässig, wenn (a) sie bereits eingetreten und nicht rückholbar ist (Erhebungsstand) oder (b) die Analyse nach Antrag nicht durchführbar wäre und die Abweichung das Projekt am Laufen hält. Methodische Verbesserungen, die der Antrag nicht verlangt, sind keine Abweichungen, sondern Ergänzungen — sie ändern nichts an dem, was der Antrag festlegt, und werden als Berichtsstandard begründet.

### 5.2 Analyse: auf den Antrag zurückgeführt (Änderung gegenüber dem Plan vom 11.09.)

*Tab. 2.* Vier Entscheidungen, die am 11.09. als Abweichung geführt wurden und jetzt dem Antrag folgen

| Nr. | Antrag | Plan 11.09. | Jetzt (12.09.) | Folgen |
|---|---|---|---|---|
| A1 | 505: „Zeit im 505-Test (Mittelwert beider Beinseiten)“ | seitengetrennt, zwei Modelle (Item 12a) | **Mittelwert beider Seiten** aus den Bestwerten je Seite; nur Spieler mit beiden Seiten; Seiten deskriptiv | ITT-Set 13/10 statt 15/10 und 14/11; PP ≥ 6 nur 7 → deskriptiv; Messgüte besser (TE/SESOI 2,92 statt 3,89/3,55); MDES 1,21 statt 1,41/1,43; COD-Defizit, Asymmetrie, Beindominanz entfallen; B3/B7/B8/B9 und SPSS-Syntax angepasst; Pipeline-Zielgröße `505M` nachzurüsten; § 11.2 F9 überholt |
| A2 | „Effektstärken (Cohens d bzw. Hedges' g)“ | partielles η² mit KI als Hauptmaß, d_adj zusätzlich | **Hedges' g** = adjustierte Differenz / gepoolte Prä-SD × J, KI aus dem KI von b1 (in B7 implementiert); η² erscheint nur, weil SPSS es ausgibt | CSV-Spalte `ES` = g; Ergebnistabelle: g [95 %] |
| A3 | H1: „signifikant bessere Leistungsveränderungen … in mindestens einem der erhobenen Parameter“; α = 0,05 | Hypothesen je Zielgröße, primäre Zielgröße Standweitsprung, übrige sekundär | **Wortlaut des Antrags**; keine nachträgliche primäre Zielgröße; alle konfirmatorischen Zielgrößen gleichrangig mit exakten p-Werten; das Mehrfachtestungsproblem der „mindestens einer“-Hypothese wird in 6.1 benannt (Familienfehler bei drei Tests bis 14 %) | Kapitel 3 formuliert H0/H1 nach Antrag; § 13 Nr. 1 wird zur Kenntnisnahme (§ 6 Nr. 2); die Sensitivitätsbetrachtung (nur SBJ mit Power > 0,25 bei d = 0,37) bleibt Diskussionsstoff, keine Analyseentscheidung |
| A4 | „Datenaufbereitung und Analyse erfolgen in SPSS und/oder R“ | SPSS + Python als Gegenprobe (im Text) | **SPSS** als einziges berichtetes Analysewerkzeug (Version, Syntax im Anhang); Python-Rechnung als interne Gegenprobe, nur in der KI-Deklaration erwähnt | 4.7 nennt SPSS; Anhang G enthält die SPSS-Syntax; keine Python-Ausgaben im Manuskript |
| A5 | „Sprintleistung: … Zeit … Leistungsveränderungen“ (Sprachfrage) | als Abweichung Nr. 10 geführt | **keine Abweichung**: Die ANCOVA ist das Verfahren des Antrags; „Leistungsveränderung“ ist Alltagssprache des Antrags, die Sprachregelung § 10 („adjustierte Gruppendifferenz im Post-Wert“) betrifft den Manuskripttext | aus dem Register gestrichen |

### 5.3 Die eine erzwungene Analyseabweichung

*Tab. 3.* Adhärenzkriterium

| Antrag (Abschnitt 8) | Datenlage | Entscheidung (12.09., vor Kenntnis der KG-Werte) | Berichtsort |
|---|---|---|---|
| „Adherence unter 75 % der vorgesehenen Trainingseinheiten in der Interventionsgruppe (Ausschluss aus der Hauptanalyse; Berücksichtigung in Sensitivitätsanalyse)“ = ≥ 9 von 12 | ≥ 9 Einheiten: **3 Spieler** (BW-02 12, BW-08 9, HL-03 9); Umsetzungsrate 92 von 216 Einheiten (42,6 %); ≥ 6: 10 Spieler | Hauptanalyse = **alle Zugeteilten** (ITT, vollständige Fälle; „Wirkung des Programmangebots“). Das Antragskriterium wird **deskriptiv** berichtet (Einzelwerte der drei Spieler, kein Test — § 11.9). Per-Protokoll ≥ 6/12 (Verfasser, 11.09.) als zusätzlicher, ausdrücklich beobachtender Vergleich; Schwellen ≥ 5/≥ 7 als Sensitivität | 4.7 (Festlegung mit Datum und Grund), 5.2, 6.1, 6.2 |

Begründung im Text: nicht „ab sechs Einheiten wirkt Training“ (§ 6.6: keine belegte Mindestdosis), sondern: Die im Protokoll vorgesehene Teilmenge ist mit n = 3 nicht auswertbar; die Umstellung auf die ITT-Hauptanalyse folgt der CONSORT-Logik (Box 6) und verringert die Abweichung vom Berichtsstandard, nicht nur vom Protokoll. Die Verdünnungslogik (§ 11.7) gehört daneben: Ein ITT-Nullbefund bei 42,6 % Umsetzung sagt zunächst nur, dass das Angebot in dieser Umsetzungsrate nichts bewirkt hat.

### 5.4 Erhebungsstand — eingetreten, nicht rückholbar, nur zu berichten

*Tab. 4.* Abweichungen vom Antrag durch den Verlauf der Erhebung

| Nr. | Antrag | Umsetzung | Grund / Bewertung | Berichtsort |
|---|---|---|---|---|
| 1 | Zielvariablen Sprint 5, 10, **20**, 30 m | 5, 10, 30 m | Entscheidung des Verfassers vor dem Prätest: Zwischenzeit bei 20 m verzichtbar neben 10 und 30 m — literaturgestützte Einordnung in § 5.7 | 4.1 (Änderung nach Protokoll, CONSORT Item 3b), 4.4 |
| 2 | Startdistanz 0,3 m (Altmann et al., 2015) | 0,5 m | Messaufbau; Altmann et al. beziffern 0,3 vs 0,5 m bei Erwachsenen mit 0,04 s — betrifft Absolutwerte, nicht den Gruppenvergleich (beide Gruppen gleich) | 4.4, 6.1 |
| 3 | Fallzahl ≈ 45 (n = 34 erforderlich, f = 0,25); IG = Vorwärts Spoho + SC Blau-Weiß (≈ 30), KG = SC West (≈ 15) | N = 31: IG = Hohenlind + Blau-Weiß (18), KG = Vorwärts Spoho (13); SC West nicht dabei | Rekrutierung; Zuteilung vor den Eingangstestungen, ergebnisunabhängig (Stärke); Fallzahl unter Plan → Sensitivitäts-Poweranalyse (§ 5.6); Chronologie und Gründe ⟨Verfasser⟩ fürs Flussdiagramm | 4.1, 4.2, 5.1, 6.2 |
| 4 | Prä KW 29; Post KW 35–36 „in den ersten Trainingseinheiten“; Familiarisierung Juni/Anfang Juli | Prä 02.07. (A, vor dem Ethikvotum 08.07.), 13.07. (C), 14.07. (B); Post 01.09. (B), 10.09. (A), 15.09. (C) | gestaffelt; Intervalle 7–9 Wochen, gruppenungleich (§ 12 Nr. 9); Chronologie Verein A neutral berichten | 4.3, 6.2 |
| 5 | KG „kein strukturiertes Training“ | KG erhielt Vereins-Lauf-/Stabi-Plan 03.–30.08. mit Sprintanteilen, ohne Sprünge | Vereinsentscheidung außerhalb der Studie; konservative Verzerrungsrichtung (Sprintreiz nur in der KG) | 4.5.2, 6.1 |
| 6 | Einschluss „Jahrgang 2011 oder 2012“ | IG Jahrgang 2011, KG Jahrgang 2012 — vollständig konfundiert mit der Gruppe | Vereinsstruktur; %PAH-Kovariate adressiert die Reife, nicht das Trainingsalter (Restkonfundierung § 12 Nr. 3) | 4.2, 6.2 |
| 7 | SBJ „bester von drei Versuchen“; drei Versuche je Test | Durchgeführt stets ≥ 2 Versuche; gültig 1–3 (k̄ prä 2,1–2,7, post IG 1,7–1,8); 174 ungültige Prä-Versuche (94 technisch, 64 Zeitmangel = dritter Versuch nicht durchgeführt, 16 Fehlversuch); Fehlversuche konnten aus Zeitgründen nicht wiederholt werden | Lichtschrankenausfälle und Gruppengröße je Termin; Bestwert-Bias gemessen (§ 11.8); Mittelwert-Sensitivität | 4.4, 6.1 |
| 8 | Intervention: 60–80 → 100–120 Kontakte; Bausteine Koordination/Technik, Plyometrie, Kraft (Eigengewicht); Kraftblock W3–4, reaktiv W5–6 | 52 → 120 Kontakte, 12 Einheiten, drei Zwei-Wochen-Blöcke, 10 Übungen; Zweitvereinskriterium nicht erhoben | Programm wie durchgeführt nach TIDieR Item 10–12 beschreiben; Abweichung klein (Startvolumen) | 4.5 |
| 9 | Zielvariable Sprint 10 m für alle | 10-m-Post-Werte von Verein B fehlen vollständig (Lichtschranke „System falsch aufgenommen“, 27 Zeilen); 10 m post nur Verein A (n = 7) | 10 m deskriptiv (§ 11.9); kein Ersatz, keine Fortschreibung; in 4.4 als Messausfall berichten | 4.4, 5.1, 6.1 |

### 5.5 Keine Abweichungen vom Antrag (Klarstellung gegenüber dem 11.09.)

- **Familiarisierung.** Antrag § 5: „vorgeschaltete Familiarisierungseinheit, in der alle Testbewegungen geübt werden“. Verfasser (12.09., protokollgetreu aus den Anwesenheitslisten in die Spalte `Familiarisierung` eingetragen): Verein A durchgängig 1 (der Trainer stellte nur einen Termin zur Verfügung), Verein B 8 × 2 und 3 × 1 (BW-01, BW-02, BW-21), Verein C 12 × 2 (VS-11 leer). Jeder Spieler hat mindestens eine Familiarisierung absolviert — der Antrag ist erfüllt. Berichtet wird die ungleiche Dosis (§ 12 Nr. 4) als Limitation, nicht als Protokollabweichung. F2 (§ 11.5 Nr. 1): Variante a (Ausschluss der Spieler mit einer Familiarisierung) lässt die IG auf 5–7 fallen → nur deskriptiv; Variante b (Familiarisierung 1/2 als dritte Kovariate) ist vorab festgelegt (B7 Block F, SPSS 9.4) — mit dem ausdrücklichen Vorbehalt, dass die Dosis in der IG mit Verein A konfundiert ist und die Kovariate deshalb Vereins- und Familiarisierungseffekt gemeinsam trägt.
- **Beindominanz.** Nicht erhoben (protokolliert 12.09.). Der Antrag sah keine Erhebung vor und legte den Seitenmittelwert fest; ein Vergleich dominant/nicht-dominant ist nicht möglich und nicht vorgesehen. Die Seitenwerte werden nur als links/rechts deskriptiv berichtet.
- **KG-Monitoring.** Der Antrag sieht das Trainingsprotokoll (Einheiten, Session-RPE) nur für die IG vor; für die KG „kein strukturiertes Training“ und kein Instrument. Der nie erhobene Fragebogen B war eine spätere Planung, keine Antragsfestlegung. Folge: Der Punkt bleibt als TESTEX-Lücke in 6.2 (§ 12 Nr. 12), verlässt aber die Liste der Protokollabweichungen und die Betreuerliste (§ 13 Nr. 6).
- **Hypothesenwortlaut, ANCOVA-Spezifikation, Kovariaten, α, Effektstärkemaß, Software, Adhärenz-Monitoring der IG:** wie Antrag (§ 5.2).

### 5.6 Ergänzungen, die der Antrag nicht regelt (Berichtsstandard; keine Abweichungen)

| Ergänzung | Grund | Ort |
|---|---|---|
| Sensitivitäts-Poweranalyse (MDES je Zielgröße bei erreichtem n) — die Antragsrechnung (f = 0,25 → n = 34) wird als Planungsstand berichtet | N = 31 < 34; CONSORT Item 7a; Lakens (2022) | 4.7, Anhang G |
| Messgüte aus eigenen Daten (TE mit KI, CV, SESOI, MDC) | Hopkins (2000); § 11.3 | 4.4 |
| Aggregationsregel Bestwert, Sensitivität Mittelwert; Versuchszahl je Gruppe | § 11.8; Bestwert versuchszahlabhängig | 4.4, 5.2 |
| Nenner je Analyse, Analysepopulations-Etikett, Teilnehmerfluss, vier Box-6-Klassen, keine Fortschreibung | CONSORT Items 13, 16; Box 6 | 4.7, 5.1 |
| Voraussetzungsprüfung mit Ergebnis (Residuen, Varianzen, Steigungen, Linearität, Überlappung) | § 11.9 | 4.7, 5.2 |
| Sensitivitäten: Mittelwert · PP ≥ 5/≥ 7 · Änderungswert (Lord's Paradox) · ohne %PAH · R²-Spanne | § 11.5, vorab festgelegt | 4.7, 5.2, 6.1 |
| Unerwünschte Ereignisse (Schmerzmeldungen) systematisch | CONSORT Item 19 | 5.1 |

### 5.7 Die fehlende 20-m-Zwischenzeit — literaturgestützte Prüfung der Begründung (12.09.)

**Angabe des Verfassers:** Die 20-m-Schranke wurde nicht gesetzt, weil dieser Wert neben 10 m und 30 m keinen größeren Mehrwert habe — „aus der Literatur entnommen“.

**Prüfung am Korpus (nur Volltexte im Ordner, § 7.1):** Eine Quelle, die ausdrücklich sagt, eine 20-m-Zwischenzeit sei neben 10 und 30 m verzichtbar, gibt es im Korpus nicht; die Behauptung „kein Mehrwert“ ist als Befund nicht belegt und wird so nicht geschrieben. Belegbar ist:

1. **Zwei-Komponenten-Lesart** (Ferguson et al., 2024, S. e96; Volltext im Ordner, JSCR 38(3), e96–e103, doi 10.1519/JSC.0000000000004639): „measurement over a range of distances provides information on acceleration ability (e.g., 5–10 m) and maximal velocity (20–40 m)“ — mit Verweis auf Darrall-Jones et al. (2015). Danach decken 5 und 10 m die Beschleunigung, 30 m den Abschnitt der maximalen Geschwindigkeit ab; eine Schranke bei 20 m läge im selben Abschnitt wie 30 m. Population: Akademiespieler 14,7 ± 0,8 Jahre (Distanz Population 1, Zielgröße 0).
2. **Reliabilität steigt mit der Distanz** (Ferguson et al., 2024, S. e99): ICC 5 m 0,53 · 10 m 0,73 · 20 m 0,86 · 30 m 0,93; SEM 20 m 0,07 s (2 %), 30 m 0,07 s (1 %). Die 30-m-Zeit ist das reliabelste Sprintmaß; die 20-m-Zeit hat denselben absoluten Fehler bei geringerer relativer Reliabilität.
3. **Sammoud et al. (2021)** messen 5/10/20 m ohne 30 m und nutzen den 10–20-m-Abschnitt für das COD-Defizit; **Dugdale et al. (2019)** 10/20 m ohne 30 m. Der Korpus ist in der Wahl der Splits uneinheitlich — das stützt, dass es keine verbindliche Splitliste gibt, nicht aber die konkrete Verzichtbarkeit von 20 m.

**Formulierung für 4.4 (Vorschlag, [EXTRAPOLATION] kenntlich):** „Abweichend vom Ethikantrag wurde keine Zwischenzeit bei 20 m erhoben. Die Splits bei 5 und 10 m bilden die Beschleunigung ab, die 30-m-Zeit den Übergang zur maximalen Laufgeschwindigkeit (Ferguson et al., 2024); eine Zwischenzeit bei 20 m hätte innerhalb desselben Abschnitts gelegen und ist nach Ferguson et al. (2024) weniger reliabel als die 30-m-Zeit. Der Verzicht ist eine Entscheidung des Messaufbaus, kein Literaturbefund.“ — Beschaffungsposten, falls ein direkter Beleg gewünscht ist: Darrall-Jones et al. (2015), JSCR 30(5), 1359–1364; Buchheit et al. (2014), J Sports Sci 32(20), 1906–1913 (Vmax-Erreichung im Nachwuchsfußball).

### 5.8 Abweichungen von Fassung 9 der Projektanweisungen (Kurzform)

| Gegenstand | Fassung 9 | Jetzt |
|---|---|---|
| 505 | seitengetrennt in zwei Modellen (§ 11.2); COD-Defizit explorativ; links/rechts statt Beindominanz | Mittelwert beider Seiten (Antrag); Seiten deskriptiv; COD-Defizit, Asymmetrie, Beindominanz entfallen |
| Effektstärke | partielles η² plus adjustierte Differenz (§ 13 Nr. 5) | Hedges' g (Antrag) mit KI; η² nur SPSS-Nebenausgabe |
| Primäre Zielgröße | „allein der Standweitsprung kommt in Betracht“ (§ 11.1, § 13 Nr. 1) | keine primäre Zielgröße (Antrag); SBJ-Sensitivität nur in 6.1 |
| N mit %PAH; Analysesets | 28; 17/7 · 17/11 · 17/11 · 17/11 · 16/10 · 16/11 | 29; 16/7 · 7/11 · 16/11 · 13/10 (505 M) · 16/11 |
| 10 m | konfirmatorisch | deskriptiv (IG 7) |
| Mindestdosis | Empfehlung ≥ 6 | festgelegt 11.09.; Antragskriterium ≥ 9 deskriptiv berichtet (§ 5.3) |
| MDES mit Q | 30 m 0,54 · SBJ 0,73 · 505 1,34/1,32 | 0,58 · 0,77 · 505 M 1,21 |
| Bestwert-Bias | „konsistent ¼ SESOI“ | nur 10 m/30 m/SBJ; 5 m/505 je Seite 1,4–3,2 SESOI |
| TESTEX 15 % | pauschal überschritten | je Zielgröße (10 m, 505 M/R/L); Teilnehmerebene 88,9 % |
| Familiarisierung | ungleiche Dosis, Sensitivitätsanalyse | ≥ 1 je Spieler (Antrag erfüllt); F2 nur mit Spalte 1/2 |
| Fragebogen B | Protokollabweichung (§ 13 Nr. 6) | keine Antragsfestlegung; TESTEX-Lücke in 6.2 |
| HL-08 post 10 m V2 | offen | bleibt 1,95 s (Verfasser 12.09.) |
| Codes in § 11.7 | „BW-11 neu“, „HL-04“ | Workbook: BW-21, HL-05 (altes Schema) |
| Vickers & Altman | Beschaffungsposten | liegt vor, verifiziert (T1/T4) |

### 5.9 505: Seitenmittel und Versuchsaggregation — Begründung (12.09.)

**Zwei Operationen, die nicht vermischt werden dürfen.** (1) *Aggregation der Versuche* innerhalb eines Tests: Bestwert (Minimum) — wie bei 5 m, 10 m, 30 m und Standweitsprung (Antrag für den SBJ „bester von drei Versuchen“; Korpus 9 von 9). (2) *Kombination der beiden Seiten* des 505: arithmetisches Mittel der beiden Seiten-Bestwerte — ein Wert je Spieler (Antrag § 3 „Mittelwert beider Beinseiten“). Die Formulierung „Mittelwert“ im Antrag betrifft allein Schritt 2. Der Satz „Mittelwert sichert gegen k-Abhängigkeit“ (Tab. 1) betrifft dagegen Schritt 1: Der *Mittelwert der Versuche* ist die Sensitivitätsanalyse nach § 11.8, weil sein Erwartungswert nicht von der Versuchszahl k abhängt, der Bestwert als Extremwert aber schon.

**Vorbild im Korpus für Schritt 2 (Volltexte im Ordner):** Dugdale et al. (2019, Methods, 505COD): „Participants completed two attempts for each turning leg (R/L) with the mean score of the best attempt from each leg being used for analysis“ — 373 schottische Nachwuchsfußballer U11–U17. Dugdale et al. (2020, Methods 2.5, m505COD): „Best attempts from each direction were selected, and a mean time from these two attempts was calculated and used for analysis“ — 86 Akademiespieler 10,6–17,3 Jahre, Microgate Witty. Die übrigen Korpusstudien werten seitengetrennt (Nimphius et al., 2016 — Cricket, Erwachsene; Clarke et al., 2020; Taylor et al., 2018; Bouafif et al., 2026 — Asymmetrie als Fragestellung) oder nur den bevorzugten Fuß (Beato et al., 2018; Negra et al., 2019). Es gibt also drei Praktiken; der Antrag hat eine davon gewählt, und sie ist im Nachwuchsfußball belegt.

**Warum das Seitenmittel für diese Studie die richtige der drei Praktiken ist:** (a) Antragstreue. (b) Ein Wert je Spieler — die Seiten sind keine unabhängigen Beobachtungen (CONSORT Item 12a), zwei Modelle würden die Tests verdoppeln. (c) Beindominanz wurde nicht erhoben; „bevorzugter Fuß“ ist nicht bestimmbar, links/rechts wäre eine willkürliche Trennung. (d) Messung an den eigenen Daten (B3 § 11): Das Seitenmittel hat einen kleineren Messfehler relativ zum SESOI als jede Seite allein (TE/SESOI 2,92 gegen 3,89 links und 3,55 rechts; TE gemessen an versuchsweise gepaarten Einzelversuchen 0,0587 s, Modellrechnung √(TE_L² + TE_R²)/2 = 0,0607 s). Preis: Seitenspezifische Information (Asymmetrie) geht verloren — sie ist keine Fragestellung dieser Arbeit; ITT-Nenner 13/10 statt 15/10 und 14/11, weil beide Seiten einen gültigen Wert brauchen.

**„Nur Spieler mit beiden Seiten“ heißt:** mindestens ein gültiger Versuch je Seite. Fehlt eine Seite ganz, gibt es kein Seitenmittel (kein Ersatz durch die andere Seite, § 11.7).

**Bestwert oder Mittelwert der Versuche (Schritt 1) — die Rückfrage vom 12.09.:** Der Einwand trifft: Bei k = 1 ist der Bestwert ein einzelner Versuch. Stand prä: 505 links k = 1 bei 4 IG- und 3 KG-Spielern, rechts bei 2 und 1; post IG links 6, rechts 7 von 16. Der Mittelwert aller Versuche hilft dort aber nicht — bei k = 1 sind Best- und Mittelwert identisch. Er hilft bei k ≥ 2: Der Mittelwert ist erwartungstreu unabhängig von k (§ 11.8), sein Fehler sinkt mit √k; der Bestwert wird mit jedem zusätzlichen Versuch systematisch besser (gemessen: 505 je Seite 1,4–3,2 SESOI je drittem Versuch, n = 4). Genau deshalb ist die Mittelwert-Aggregation als Sensitivitätsanalyse vorab festgelegt (B7 Block C, SPSS 9.1; für 505 als (Mittel_L + Mittel_R)/2, beide Seiten gleich gewichtet). Empfehlung: Bestwert als Hauptanalyse beibehalten — Antragskonvention (SBJ), Korpus 9/9, Vergleichbarkeit mit der Literatur, Vorbild Dugdale — und beide Ergebnisse nebeneinander berichten; weichen sie ab, gehört das in 6.1. Ein Wechsel des Hauptmaßes müsste jetzt (vor dem 15.09.) und für alle Zielgrößen einheitlich fallen; für ihn spricht die Fehlerlogik, gegen ihn die Vergleichbarkeit. Die Frage ist in der Zielpopulation empirisch untersucht: Al Haddad, Simpson & Buchheit (2015), *Monitoring changes in jump and sprint performance: Best or average values?*, IJSPP 10(7), 931–934, doi 10.1123/ijspp.2014-0540 — 102 hochtrainierte Nachwuchsfußballer U13–U17; nach der PubMed-Zusammenfassung liefern beide Ansätze ähnliche Ergebnisse. **Beschaffungsposten** (§ 7.1: vor Zitation Volltext prüfen); Dugdale et al. (2020) berufen sich für ihre Mittelung auf genau diese Quelle.


### 5.10 Nachträgliche Festlegungen nach dem Sperrdatum (Stand 25.09.2026)

Was nach dem 15.09.2026 festgelegt oder geändert wurde, gilt als nachträglich (Auswertungsverfahren 2.3, Spezifikation 0.2). Die Einträge R1 bis R8 hat der Verfasser am 24.09.2026 entschieden, R9 bis R13 kamen am 25.09.2026 aus der Blindrechnung, dem Abgleich, der Handprobe und der Code-Durchsicht (Phase 6), R14 ist die Verfasserentscheidung vom 25.09.2026 zum Erratum von Khamis und Roche, alle ohne Rücksprache mit dem Betreuer. Die Rechnung vom 15.09. war dabei bekannt. Wo sie Anlass war, steht es in der Spalte Grund. Quellen: Spezifikation der Rechenschritte vom 24.09.2026 (Teil F), `02_Befunde\Auswertungs_und_Berichtsumfang_2026-09-24`, `02_Befunde\Voraussetzungspruefungen_Literaturbefund_2026-09-24`. Im Manuskript gehören die Einträge als Änderungen nach Protokoll (CONSORT Item 3b) in 4.1 und 4.7 und als Limitation in 6.2.

*Tab. 5.* Nachträgliche Festlegungen

| Nr. | Festlegung | ersetzt oder ergänzt | Grund | Berichtsort |
|---|---|---|---|---|
| R1 | Rechenumgebung R. Die berichtete Rechnung schreibt eine zweite, blinde Instanz nach der Spezifikation. Die Python-Kette (Code 12.09.) ist Gegenprobe (F0) | ersetzt A4 (SPSS) und den Task „SPSS und Pipeline“ (§ 9 Nr. 8) | Unabhängige Gegenprüfung der Umsetzung (Auswertungsverfahren 0.1). Der Antrag nennt „SPSS und/oder R“, die Änderung ist antragskonform | 4.7, Anhang G, KI-Deklaration |
| R2 | Kein partielles η² (K24) | ergänzt A2 | Es war nur als SPSS-Nebenausgabe vorgesehen | – |
| R3 | Sensitivitäts-Poweranalyse nach dem Standardweg: df2 = N − 4, λ = d²·n_IG·n_KG/N, MDES bei Power 0,80, ohne R²max, ohne Faktor SE und ohne R²-Spanne (O9) | ersetzt die Rechnung mit R² und Q (B8) und die Zeile „R²-Spanne“ in § 5.6 | Verfasserentscheidung gegen die Empfehlung. Der Standardweg ohne Kovariatengewinn ist konservativ, die MDES fällt größer aus | 4.7, Anhang G |
| R4 | Präzisierungen O1 bis O8 und K1 bis K30 bei der Ausarbeitung der Spezifikation, P1 bis P7 mit der Freigabe F1 bestätigt | ergänzt § 2 | Der Plan ließ diese Größen offen (Spezifikation Teil F.2 und F.3). Seit Nachtrag 2 sind P1 und P3 ohne Anwendung, P7 ist eingeschränkt | 4.7 |
| R5 | Bootstrap-KI der adjustierten Differenz für alle drei konfirmatorischen Zielgrößen, B = 10 000, Startwert 20260924, Schichtung nach Gruppe (O8, N3) | ergänzt § 5.6 (Sensitivitäten) | Anlass für O8: In der Rechnung vom 15.09. war beim 30-m-Sprint die Normalverteilung der Residuen verworfen. N3 dehnt das Intervall auf alle drei Zielgrößen aus, damit die Zusatzanalyse nicht an einem Vortest hängt (Rochon et al., 2012) | 4.7 als nachträgliche Zusatzsensitivität, Tab. H4 |
| R6 | Q-Q-Diagramm der Residuen je Zielgröße und Residuen-SD je Gruppe mit dem Verhältnis KG zu IG (N1, N2, Nachtrag 1) | ergänzt die Voraussetzungsprüfung (§ 5.6) | Grafik neben dem Test, Richtung einer Verzerrung bei ungleich großen Gruppen (Voraussetzungsprüfungen § 5.1) | Anhang G, Tab. H4 |
| R7 | Berichtsumfang (N4, Nachtrag 2): Gerechnet wird nur, was berichtet wird oder was eine Prüfung oder die Darstellung braucht, 1.535 Kennungen. Stichprobenbeschreibung in der Analysepopulation ANA. Poweranalyse nur für die im Plan genannten Kombinationen. sRPE-Load bleibt, auf der Solldauer der Programmwoche | ergänzt § 2 und § 4 | Entscheidungsregel mit Kriterien, die bei jedem Ergebnis gleich entschieden (Umfangsdokument § 2.1). Was in der ersten Rechnung ungünstig oder auffällig war, bleibt mindestens im Anhang | 4.6, 4.7, Kapitel 5 |
| R8 | Abb. 2: Ausgangswert gegen reifeadjustierten Abschlusswert mit den Linien des Modells je Gruppe (Vickers & Altman, 2001) | ergänzt den Darstellungsplan (§ 4) | Kriterium ist die Größe der Ausgangsunterschiede, bekannt seit der Eingangstestung im Juli. Festgelegt nach dem 15.09. | 5.2 |
| R9 | Festlegungen aus der Blindrechnung (25.09.2026, Rückfragenprotokoll der zweiten Instanz): SESOI post intern aus den Bestwerten post nur für den Bestwert-Bias S11 (R1, Lesart a) · Zuordnung der acht Gründe fehlender Werte (R2) · Sammelmeldungspaar als Komplement des Dublettenpaars, jedes Paar gezählt (R3, Lesart a) · Fallzahlregel in der Menge BPAH für beide Vorab-Prüfungen (R4, Lesart a) · Toleranz des Referenztests R08 (W 1e-5 statt 5e-7, F_9,90(0,95) 1e-4 statt 5e-5, Genauigkeit der Quelle) (R5) · Lesarten A1 bis A13 | ergänzt die Spezifikation (Nachträge zu S06, S11, S14, G.1, G.2) | Rückfragen der blinden Instanz beim Lesen der Spezifikation, Antworten des Verfassers per Auswahl oder durch die Instanz nach Freigabe. Ohne Wirkung auf die Hauptanalyse | 4.7 (Daten- und Rechenprüfung), Anhang G (Rückfragenprotokoll) |
| R10 | Gegenprobe als neue Fassung der Python-Kette nach der Spezifikation: `Gegenprobe_Python_2026-09-25.py` (Fassung 2) statt des Code-Stands vom 12.09. Referenztests, Grenzfälle, Ergebnisdatei nach G.1. Abgleich 6.1 je Kennung bestanden (3 559 Kennungen, 0 Abweichungen), Durchsicht 6.2 und Plausibilität 6.4 ohne Regelabweichung | ergänzt R1 (Gegenprobe) | Der Code-Stand vom 12.09. kennt weder den Datenstand noch die Kennungen und rechnet nach Regeln, die vor den Festlegungen O1 bis O9 und K1 bis K30 liegen (Abgleichprotokoll_2026-09-25 § 3) | 4.7 |
| R11 | Korrektur mit altem und neuem Ergebnis (Auswertungsverfahren 2.3): %PAH nach S05 (lineare Interpolation der Koeffizienten, O2, exakte Umrechnung 0,45359237 kg je Pfund, K3, ohne Rundung) statt der Workbook-Spalte `PAH_Prozent` (nächste Halbjahreszeile, Faktor 2,20462, PAH_cm auf 0,1 cm gerundet), aus der die Rechnung vom 15.09. und das Kennzahlenblatt vom 22.09. den Reifestatus übernommen hatten. Differenz je Spieler −0,63 bis +0,55 Prozentpunkte. Adjustierte Differenz 30 m −0,046 → −0,045 s (p 0,536 → 0,557), 505-Mittel −0,014 → −0,012 s (p 0,678 → 0,734), Standweitsprung +0,2 → −0,1 cm (p 0,960 → 0,987), %PAH der Analysepopulation IG 94,65 ± 2,90 → 94,74 ± 2,77, KG 90,41 ± 2,85 → 90,50 ± 2,73. Dazu TE des 505-Seitenmittels 0,058 → 0,055 s durch die Paarung nach Versuchsnummer (K15). Schlusslogik unverändert (alle drei Zielgrößen Fall C1, H0 nicht abgelehnt) | ersetzt die %PAH-Werte des Kennzahlenblatts vom 22.09. (K-02, K-02b) und die Ergebnisangaben des Analyseprotokolls vom 15.09. | Plausibilitätsprüfung 6.4 am 25.09.2026 (Plausibilitaetsprotokoll_2026-09-25 § 4). Die Regel O2 stand seit F1 fest, ihre Wirkung wurde erst im Vergleich beider Rechnungen sichtbar. Kennzahlenblatt in Phase 7.1 aus der Ergebnisdatei neu, Manuskript 4.2 beim Endabgleich 7.3 anpassen | 4.7, 6.3 (Kurzform im Abweichungsregister Tab. H6) |
| R12 | Handprobe 6.3 als Excel-Formelprobe (Verfasser 25.09.2026): Die 34 vorab bestimmten Kennwerte werden nicht von Hand nachgerechnet, sondern in `04_Uebergaben\Handprobe_2026-09-25.xlsx` (Fassung 2, Erzeuger `03_Skripte\Handprobe_2026-09-25.py`) mit Excel-Formeln allein aus den Eingangsblättern des Datenstands und der Anlagen berechnet, mit Auslöseprüfung, Ausfallkategorien, Interpolation der Koeffizienten, Analysesets und LINEST für die ANCOVA. Excel ist damit eine dritte Implementierung der 34 Kennwerte neben R und Python. Dazu der Vergleich von elf Zwischengrößen je Spieler mit der berichteten Rechnung und vier Zusatzprüfungen. Rechenprobe mit LibreOffice Calc (`03_Skripte\Handprobe_Pruefung_2026-09-25.py` und `.txt`): 34 von 34 Kennwerte stimmen, Zusatzprüfungen 4 von 4, größte relative Abweichung 4e-15. Der Verfasser prüft Formeln und Urteile in Excel und trägt das Ergebnis in Zelle B4 ein | ergänzt Auswertungsverfahren 6.3 (Handprobe des Verfassers in Excel) | Eine Formelprobe ist nachvollziehbar und wiederholbar und prüft die Regeln der Spezifikation unabhängig von beiden Skriptsprachen. Von Hand eingetippte Werte wären weder prüfbar noch von der Rechnung unabhängig | 4.7 (Daten- und Rechenprüfung) |
| R13 | Nachtrag 3 zur Spezifikation (Teil F.8, 25.09.2026, N5.1 bis N5.4): Vorrang des Grunds „Eingang fehlt“ in S05 · Median und Mittel der Adhärenz über die zugeteilten Spieler, N4.3 an Regel 7 und die Kennungsanlage angeglichen · Rangkriterium der Designmatrix (QR-Zerlegung, Toleranz 1e-7, spaltenskaliert, oder gleichwertig) · Zusatz `_Python` in den Grafiknamen der Gegenprobe. Blindprüfung 2.2 im dritten Lauf bestanden | ergänzt R9 (Klarstellungen der Spezifikation nach dem Blindlauf) | Code-Durchsicht 6.2 (`Durchsichtsprotokoll_2026-09-25`, Teil C). Beide Implementierungen hatten die vier Stellen gleich gelesen, kein Wert der Ergebnisdatei ändert sich | 4.7, Anhang G |
| R14 | Reifestatus endgültig nach Tab. 1 der Originalpublikation von Khamis und Roche (1994), O1 und O2 unverändert (Verfasser 25.09.2026). Das Erratum (Pediatrics 95(3), 457, 1995, doi 10.1542/peds.95.3.457) wird nicht beschafft. Es ist nur über die Bibliothek erreichbar, die Recherche über PubMed, Crossref, Unpaywall und den Verlag blieb ohne Volltext (`05_Protokolle\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25`). Der Vorbehalt aus O1 und L12, die Rechnung bei einem Treffer im Erratum zu wiederholen, entfällt | ergänzt R4 (O1) und schließt L12 der Maßnahmenliste | Das Erratum korrigiert nach Crossref „Tables 1 and 2“ der Originalpublikation. Ohne Volltext ist nicht bekannt, ob verwendete Koeffizientenzeilen betroffen sind und in welche Richtung ein Fehler die Kovariate je Altersjahr verschieben würde. Alle Spieler wurden nach derselben Tabelle und Regel berechnet, der Reifestatus ist Kovariate, nicht Zielgröße. Gearbeitet wird mit dem vorliegenden Stand (Verfasser 25.09.: „damit arbeiten, was wir aktuell haben“) | 4.3 und 4.7 als Einschränkung (Koeffizienten der Originalpublikation, Erratum nicht eingesehen), 6.3 (G2, Restkonfundierung über die Kovariate) |

*Tab. 6.* In der ersten Rechnung enthalten, künftig nicht gerechnet und nicht berichtet

| Auswertung | Stelle der ersten Rechnung | Grund des Wegfalls |
|---|---|---|
| Explorative Korrelationen der Adhärenz mit den Ausgangswerten | B0 § 5, Tabellenbild Tab15 vom 12.09. | ohne Hypothese und bei höchstens 18 Spielern ohne Aussage. Sie laden zu einer Dosis-Wirkungs-Deutung ein, die ausgeschlossen ist |
| Leistungsunabhängigkeit der Versuchsausfälle (Korrelationen roh und je Verein) | B1, PA F12 § 3.1 | Nicht signifikante Korrelationen bei 7 bis 13 Spielern je Verein können Unabhängigkeit nicht zeigen. Die Richtung zeigt die mittlere Zahl gültiger Versuche je Gruppe |
| Instrumentkennwerte des Fragebogens (Meldeabstände, Bearbeitungsdauer, Wochentag, Tageszeit, Konkordanz) | Fragebogenauswertung 12.09. | kein Schluss hängt daran. Der Meldezeitpunkt ist nicht der Trainingszeitpunkt |
| MDC, SESOI nach Hopkins mit Messfehlerkorrektur (SESOI_T), TE/√n mit Merkmal | B3 | MDC dient Einzelaussagen, die TE > SESOI ausschließt. TE/√n ist eine verkürzte Übertragung von Hopkins (2000, S. 7–8) |
| g und unadjustierte Differenz der Sensitivitätsvarianten | Analyseprotokoll 15.09. § 4 | Für die Robustheit genügt die adjustierte Differenz mit KI je Variante |

Die Wegfälle folgen der Entscheidungsregel des Umfangsdokuments (§ 2.1). Die Vorab-Prüfung an den Prä-Werten, die Messgüte je Verein und der Bestwert-Bias bleiben ausdrücklich, weil ungünstige oder auffällige Befunde nicht gestrichen werden (SMK-Leitfaden Abschn. 4.8).

---

## 6 Entscheidungen für den Betreuer (Mail 14.09.) — mit Empfehlung

| # | Entscheidung | Empfehlung | Begründung |
|---|---|---|---|
| 1 | **Adhärenzkriterium** — Antrag: ≥ 75 % für die Hauptanalyse | Zustimmung zu § 5.3: Hauptanalyse ITT; Antragskriterium deskriptiv (n = 3); PP ≥ 6/12 beobachtend; Festlegung vor Kenntnis der KG-Werte dokumentiert | einzige erzwungene Analyseabweichung; n = 3 ist nicht auswertbar (§ 11.9); Umstellung folgt CONSORT Box 6 |
| 2 | **Hypothesen und Mehrfachtestung** — Antrag: „mindestens einer der erhobenen Parameter“, α = 0,05 | beim Antrag bleiben: keine nachträgliche primäre Zielgröße, keine Adjustierung; Familienfehler in 6.1 benennen (drei konfirmatorische Tests: bis 14 %); Alternative nur auf Wunsch des Betreuers: SBJ als primäre Zielgröße (dann Abweichung mit Grund § 11.1) | Antragstreue; die Sensitivitätsbetrachtung (SBJ Power 0,27 bei d = 0,37; 30 m 0,43; 505 M 0,14) gehört in die Diskussion |
| 3 | **Spezifikation der Effektstärke** — Antrag: „Cohens d bzw. Hedges' g“ | Hedges' g = adjustierte Differenz / gepoolte Prä-SD, Korrektur J = 1 − 3/(4·df − 1), 95-%-KI aus dem KI der adjustierten Differenz | protokollkonform; über Studien vergleichbar (Prä-SD als Nenner); in B7 implementiert |
| 4 | **Fehlende %PAH** (VS-11, VS-18) — Antrag: %PAH als Kovariate | Kovariate behalten (N = 29 statt 31); Verzerrungsrisiko benennen (beide in der schwächeren KG-Hälfte) | Antragstreue; Verzicht senkt den MDES kaum, kostet die Reifeadjustierung |
| — | Kenntnisnahme: 505 als Mittelwert beider Seiten (Antrag; ersetzt § 13 „505 seitengetrennt“), SPSS als Analysewerkzeug (Antrag), Familiarisierung erfüllt (ersetzt § 13 Nr. 4), Fragebogen B keine Protokollabweichung (ersetzt § 13 Nr. 6), Nenner der Adhärenzquote 12, TESTEX-Befunde in 6.2 ohne Score, KG-Termin 15.09. außerhalb KW 35–36 (Abweichung § 5.4 Nr. 4), Einverständniserklärung ohne Zuteilungshinweis, Umfang/Format, Zweitprüfer, Videoplattform | — | organisatorisch bzw. bereits durch den Antrag entschieden |

---

## 7 Quellenlage für 4.7 und 5 (§ 7.1 Volltextpflicht) — DOIs am 12.09. über Crossref/PubMed geprüft

| Quelle | Status | DOI / Zugang | Verwendung |
|---|---|---|---|
| Vickers & Altman (2001), BMJ 323(7321), 1123–1124 | im Ordner, Volltext geprüft; T1/T4 ergänzt | 10.1136/bmj.323.7321.1123 | ANCOVA-Begründung mit Grenzen (Randomisierung vorausgesetzt; Effizienz nur r < 0,8) |
| Hopkins (2000), Sports Med 30(1), 1–15 | im Ordner, geprüft | 10.2165/00007256-200030010-00001 | TE, CV, SESOI (S. 8), TE-KI (S. 13) |
| Moher et al. (2010), BMJ 340, c869 | im Ordner, geprüft; Fundstelle = Item | 10.1136/bmj.c869 | Items 7a, 12, 13, 16–19, Box 6 |
| Schulz et al. (2010), BMJ 340, c332 — CONSORT Statement | **im Ordner seit 12.09., Volltext geprüft**; T1 `Schulz2010`, T4 ergänzt | 10.1136/bmj.c332 | 4.1 (Design in Titel/Abstract, Item 1a; Änderungen nach Studienbeginn, Item 3b); stabile Fundstelle = Item-Nummer |
| Lakens (2022), Collabra: Psychology 8(1), 33267 | **im Ordner seit 12.09., Volltext geprüft**; T1 `Lakens2022`, T4 ergänzt | 10.1525/collabra.33267 | Ressourcenbegründung (S. 3–4), Sensitivitäts-Poweranalyse (Tab. 3, S. 5), „honesty requires you to state there is no sample size justification“ (S. 9) |
| Lord (1967), Psychol Bull 68(5), 304–305 | nicht beschaffbar (Verfasser 12.09.) → **gestrichen**; Lord's Paradox nur über Vickers & Altman (2001) und eigene Darlegung | 10.1037/h0025105 | 6.1 |
| Dugdale et al. (2019), EJSS 19(6), 745–756 · Dugdale et al. (2020), Sports 8(4), 51 | im Ordner, Volltext geprüft; T4 ergänzt (505-Regel) | 10.1080/17461391.2018.1556739 · 10.3390/sports8040051 | § 5.9: Vorbild „Bestwert je Seite, dann Seitenmittel“ (4.4, 4.7) |
| Al Haddad, Simpson & Buchheit (2015), IJSPP 10(7), 931–934 | **Beschaffungsposten** (Human Kinetics; nur PubMed-Zusammenfassung bekannt) | 10.1123/ijspp.2014-0540 | Best- vs. Mittelwert wiederholter Versuche bei U13–U17-Fußballern (§ 5.9, § 11.8); ohne Volltext nicht zitierbar |
| Ferguson et al. (2024), JSCR 38(3), e96–e103 | im Ordner, Volltext geprüft (12.09.) | 10.1519/JSC.0000000000004639 (PMC10880938) | Splitdistanzen und Reliabilität (§ 5.7); Populationsdistanz 1 |
| Cohen (1988) | fehlt (Buch, kein DOI) | — | 0,2-Regel als Sekundärzitat nach Hopkins |
| Nimphius et al. (2016) | im Ordner | 10.1519/JSC.0000000000001421 | nur noch als entfallene Analyse (COD-Defizit) |
| Ditroilo et al. (2025), Abt et al. (2025), Correll et al. (2020) | fehlen | — | weglassen; die Aussagen tragen ohne sie |

---

## 8 Folgeänderungen für Fassung 10 der Projektanweisungen (Änderungsliste)

1. § 1.1 Leitplanken: Leitregel „Antrag vor Optimierung“ (§ 5.1 hier) aufnehmen.
2. § 1.3 Dokumentenkarte: `Claude\02_Befunde\Auswertungsplan_2026-09-12` als operativen Plan; `Analyseprotokoll_2026-09-12.md` als Rechenprotokoll; `03_Skripte` mit B0–B9 (2026-09-12) und `SPSS_Syntax_2026-09-12.sps`; Ordnerstruktur § 1.4 als umgesetzt.
3. § 2 Steckbrief: Zielgrößen „505 (Mittelwert beider Beinseiten)“ statt „seitengetrennt“; „Explorativ: COD-Defizit“ streichen; Beindominanz-Zeile streichen; „Analysierbares N = 28“ → 29; Post-Tests B 01.09., A 10.09., C 15.09.; Familiarisierung: zwei Termine je Mannschaft angeboten, ≥ 1 je Spieler.
4. § 3 Datenstand: Füllstand aktualisieren; Messgütetabelle um die Zeile „505 Mittelwert (n 27, 2,49 ± 0,10, SESOI 0,020, TE 0,059, CV 2,3, TE/SESOI 2,92, TE/√n/SESOI 0,56)“; analysierbare n 16/7 · 7/11 · 16/11 · 13/10 · 16/11; Baseline-d 505 M −0,60; Fragebogen-Absatz: Codeumstellung für die Zusammenführung mit dem Workbook nicht nötig (altes Schema), nur zwei CASE-Korrekturen; die sieben Bemerkungen ohne Kategorie als „kein Wert notiert“ (nach Verfasserentscheidung).
5. § 4: Familiarisierung als erfüllt; Fragebogen B als TESTEX-Lücke, nicht Protokollabweichung.
6. § 6.5 / § 7.1: Vickers & Altman aus den Beschaffungsposten streichen; Lakens (2022), Schulz et al. (2010) mit DOI aufnehmen; Ferguson et al. (2024) in den Korpus 2.4 (Splitdistanzen, Reliabilität).
7. § 11.1: Tabelle durch B8 § 1 (Stand 12.09.) ersetzen; Power bei Vorab-Erwartungen aktualisieren; Satz „allein der Standweitsprung kommt als primäre in Betracht“ → „der Antrag sieht keine primäre Zielgröße vor; allein der SBJ hat ausreichende Sensitivität (6.1)“.
8. § 11.2: 505 als Mittelwert beider Seiten (ein Modell); Satz „seitengetrennt in zwei Modellen“ streichen; COD-Defizit als entfallen; Effektstärke Hedges' g nach § 6 Nr. 3.
9. § 11.5: F2 nur unter Vorbehalt der Spalte 1/2; Sensitivitätsliste = Mittelwert · PP ≥ 5/≥ 7 · Änderungswert · ohne %PAH · R².
10. § 11.7: Antragskriterium ≥ 75 % als deskriptiv berichtete Teilmenge; Workbook-Codes (BW-21, HL-05); Mindestdosis als festgelegt (11.09.); PP-Nenner 505 M = 7 → deskriptiv.
11. § 11.8: Bestwert-Bias-Aussage auf 10 m/30 m/SBJ einschränken; B0.2-Regel für auslösegestörte Läufe.
12. § 11.9: 10 m deskriptiv (IG 7); 505 M PP deskriptiv; Steigungshomogenität 505 M p = 0,606; IG-prä-Verteilung 505 M linksschief.
13. § 12: Nr. 8 TESTEX je Zielgröße; Nr. 18 „%PAH fehlt bei 2 von 31“; Nr. 20 (Beindominanz) streichen; Nr. 23 Bias-Präzisierung; neu: Ausfall BW-21 nicht neutral; TE 30 m post Verein A; 20-m-Verzicht mit Ferguson-Einordnung; Abweichungsregister (§ 5 hier).
14. § 13 Betreuerliste: auf § 6 hier reduzieren (vier Entscheidungen + Kenntnisnahmen); Nr. 4 (Familiarisierung), Nr. 6 (Fragebogen B), Nr. 5/„505 seitengetrennt“/„COD-Defizit“/„Trennung links/rechts“ erledigt.
15. § 15: Ferguson et al. (2024), Lakens (2022), Schulz et al. (2010) mit DOI; Lord (1967) und Cohen (1988) bleiben Sekundär-/Ersatzwege.
16. § 3.1: Versuchszahl-Sprachregelung — „durchgeführt stets ≥ 2, gültig 1–3; k zählt gültige Versuche; Fehlversuche aus Zeitgründen nicht wiederholt“; Ausfalltabelle prä 94 / 64 / 16 / 0 (keine Zeile „ohne Bemerkung“ mehr).
17. § 2 Steckbrief: Zeile „Beindominanz: nicht erhoben; Trennung nach links/rechts“ → „nicht erhoben; 505 als Seitenmittel, Seiten nur deskriptiv“; Familiarisierung: je Spieler 1 oder 2 (Verein A durchgängig 1).
18. § 11.5 Nr. 1: F2 = Familiarisierung (1/2) als dritte Kovariate, Vorbehalt Konfundierung mit Verein A; Ausschlussvariante nur deskriptiv.
19. § 11.8: 505-Regel (§ 5.9 hier) aufnehmen; Beschaffungsposten Al Haddad et al. (2015).

---

## 9 Ablauf — wer was tut

**Erledigt am 12.09. (Cowork):** Rechenkette Rev. 2 (505 Mittelwert, Antragskriterium) gerechnet und geprüft · SPSS-Syntax angepasst · Ordnerstruktur § 1.4 auf dem Rechner angelegt und Dateien einsortiert · DOIs geprüft · 20-m-Begründung am Korpus geprüft · HL-08-Entscheidung und Familiarisierungsangabe dokumentiert.

**Verfasser (nicht delegierbar):**
1. `Ordner_aufraeumen.ps1` ausführen (Anleitung in `README_Ordnerstruktur.md`, Abschnitt „Schritt für Schritt“); Word/Excel vorher schließen.
2. Mail an den Betreuer am 14.09. mit § 6 (vier Entscheidungen, Kenntnisnahmen).
3. ~~Lakens (2022) und Schulz et al. (2010) laden~~ — erledigt 12.09. (im Ordner, geprüft). Neu: Al Haddad et al. (2015) über die Bibliothek beschaffen (§ 7), falls die Aggregationsfrage im Text mit Literatur belegt werden soll.
4. ~~Sieben Bemerkungen~~ — erledigt 12.09. (nachgetragen: drei als Zeitmangel, vier als Fehlversuch).
5. ~~Familiarisierungsspalte~~ — erledigt 12.09. (1/2 je Spieler eingetragen).
6. Flussdiagramm-Felder vor der Zuteilung (angefragte Vereine, SC West, VS-09, VS-12–15, Einwilligung VS-01/02) nachliefern.
7. 15.09.: KG-Post mit drei Versuchen je Zielgröße; Belastungszustand erheben; Codes VS-11/16–18 klären; Werte in `02_Rohdaten` eintragen (Bemerkungsvokabular B0.4).
8. Danach neuer Task „SPSS und Pipeline“: `Auswertung_B1…B9_2026-09-12` laufen lassen, `Auswertung_B7_ANCOVA_2026-09-12.py --csv`, `SPSS_Syntax_2026-09-12.sps` in SPSS ausführen, Ergebnisse vergleichen (V5), SPSS-Version eintragen, Pipeline um `505M` ergänzen, `Erzeuge_Ausgaben.ps1` starten.

**Nächster Cowork-Task danach:** Vorschlagsliste 4.7 (700–900 Wörter, sechs Bausteine) mit den Zahlen aus diesem Plan; anschließend 5.1/5.2. Startsatz: „Der Ordner Bachelorarbeit ist verbunden. Arbeite nach `Claude\02_Befunde\Auswertungsplan_2026-09-12` und dem Analyseprotokoll. Lege die Vorschlagsliste für 4.7 vor — sechs Bausteine, 700–900 Wörter, Zahlen aus B3/B4/B8 (Stand 12.09.), Betreuerentscheidungen als ⟨FÜR SCHWAB⟩. Kein Einbau ohne Freigabe.“

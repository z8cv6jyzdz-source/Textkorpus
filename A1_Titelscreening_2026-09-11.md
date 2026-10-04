# Phase A · Schritt A1 — Titelscreening `Ideen und Studien`

**Stand 11.09.2026 · Zwischenstand zur Freigabe, kein Ablagedokument** (wird Abschnitt 1 des Befunddokuments `Claude\RCT_Auswertungspraxis_2026-09-11.md`).

**Grundlage.** Vollständige Auflistung des Ordners (`device_list_dir`, 11.09.2026): **105 Einträge**, davon 92 PDF und 13 Nicht-PDF. Jeder Eintrag wurde einzeln eingestuft. Einstufungsgrundlage: Titel; bei allen Interventionskandidaten zusätzlich das Abstract (Seiten 1–2 bzw. 1–4 extrahiert); T1_steckbriefe.csv als ungeprüfte Vorinformation. Volltexte wurden **nicht** ausgewertet.

**Klassen** (nach Übergabeprompt A1): **R1** Primärstudie, randomisierte Zuteilung im Titel oder Abstract behauptet · **R2** kontrollierte Interventionsstudie ohne Randomisierung · **R3** kein Interventionsvergleich · **—** keine Literatur (Software, eigene Dokumente, Bilddubletten). **◆** = Diagnostikbeleg, in A4 mitzuführen (R3-Ausnahme).

## 1 Ergebnis in Zahlen

| Klasse | n | Einträge |
|---|---|---|
| R1 | 10 | Lloyd 2016 · Hammami 2016 · Beato 2018 · Negra 2019 · Hilska 2021 · Aloui 2022 · Liu 2024 · Moran 2024 · Sammoud 2024 · Bouafif 2026 |
| R2 (klassisch) | **0** | — |
| R2* (Sonderfall) | 1 | Padrón-Cabo 2025 |
| R3 | 80 | davon 14 mit ◆ Diagnostikbezug |
| — | 14 | 1 Zertifikat-PDF, 2 Installer, 3 eigene Dokumente, 8 JPEG (4 Khamis-Roche-Seitenbilder, 4 Lloyd-Abbildungsausschnitte) |

## 2 R1/R2-Menge im Detail (Kandidaten für A2–A5)

| # | Studie | Zuteilung laut Abstract/Titel | Kontrollgruppe | Erste Einordnung |
|---|---|---|---|---|
| 1 | Lloyd et al. (2016) | „randomly assigned“, innerhalb zweier Reifegruppen | ja (inaktiv) | dosisnächste Studie (6 Wo/12 E); Schüler, keine Fußballer |
| 2 | Hammami et al. (2016) | „randomly divided into two groups“ | ja (aktiv) | ⚠ Vorauswahl führte R2 — Abstract behauptet Randomisierung |
| 3 | Beato et al. (2018) | „randomized pre-post parallel group trial“ | **nein** (zwei aktive Arme) | einzige ANCOVA-Quelle des Korpus; 505 + Long Jump + 10/30 m |
| 4 | Negra et al. (2019) | „randomly assigned“ (LPJT/UPJT) | **nein** (zwei aktive Arme) | Kontakte 50→120, 90 s — dosisnah; prä-PHV |
| 5 | Hilska et al. (2021) | Cluster-RCT (Titel) | ja | Zielgröße Verletzungen → nach A4 ohne Zielgrößen-Überschneidung; nur A7 (Adhärenzverlauf) |
| 6 | Aloui et al. (2022) | „allocated at random“ | ja (aktiv) | U15, Tunesien; ⚠ Baseline-Signifikanztest bereits im Abstract |
| 7 | Liu et al. (2024) | „randomized parallel controlled study“ | ja (inaktiv) | Off-Season, Tier 2, 3 Wo/6 E; einzige Übergangsperioden-Studie mit plyometrischem Arm |
| 8 | Moran et al. (2024) | „randomly allocated“ | **nein** (drei aktive Arme) | Erwachsene (22,3 J.) — Population fern |
| 9 | Sammoud et al. (2024) | RCT (Titel) | ja (aktiv) | prä-PHV; ANCOVA mit Baseline; 505 + SLJ |
| 10 | Bouafif et al. (2026) | RCT, stratifiziert nach Reife (Titel) | ja (aktiv) | Tier 2; 505; nur η² |
| 11 | Padrón-Cabo et al. (2025) | **nicht randomisiert** — zwei Jahrgangskohorten U15/U17 | keine (beide Kohorten exponiert) | **R2\*-Sonderfall**: keine Intervention (2 Wo Trainingsstopp), aber die einzige Arbeit im Ordner mit unserer Kernkonstellation „Jahrgangsunterschied zwischen den Gruppen“ |

Vier der zehn R1-Studien haben **keine** Kontrollgruppe (Beato, Negra, Moran) bzw. nur eine aktive Vergleichsbedingung — für die Frage „wie wird ein Gruppenunterschied gegen eine Kontrollbedingung geschätzt“ tragen sie weniger; für Aggregation, Grafik und Deskriptiva bleiben sie voll verwertbar.

## 3 Abweichungen von der Vorauswahl aus T1 (Übergabeprompt A1)

1. **Hammami et al. (2016): R1 statt R2.** Das Abstract sagt „randomly divided“. T1 führt keine Randomisierung — der Steckbrief ist an dieser Stelle unvollständig. Ob ein Verfahren beschrieben ist, klärt A3 am Methodenteil. Folge: **Im Ordner liegt keine einzige kontrollierte Interventionsstudie ohne Randomisierung.** Die Klasse R2, die dem eigenen Design am nächsten stünde, ist im Korpus leer.
2. **Asimakidis et al. (2022): R3 statt R2.** Einarmige Prä-Post-Beobachtung (n = 29, gepaarte t-Tests), kein Vergleichsarm — ohne zweiten Arm keine „kontrollierte“ Studie. Bleibt E5-Kontext für 2.3, fällt aus dem A5-Raster.
3. **Padrón-Cabo et al. (2025): R2\* statt R2.** Keine Interventionsstudie, aber nicht randomisierter Zwei-Kohorten-Vergleich mit Altersunterschied. Empfehlung: **mitführen**, ausdrücklich als Sonderfall, mit Schwerpunkt auf der Frage, wie die Autoren den Alters-/Reifeunterschied in der Auswertung behandeln (laut Verfahrensbefund vom 11.09.: gar nicht — Kovariate kommt nicht vor).
4. **Hilska et al. (2021): R1, aber nur A7.** Cluster-RCT mit Verletzungen als Zielgröße; nach A4 ohne Überschneidung. Wird nicht durch das A5-Raster geführt, sondern ausschließlich in A7 (Mindestteilnahme/Adhärenzverfall, Betreuungsgrad durch Vereinstrainer).
5. **Diagnostikbelege:** Die Vorauswahl nannte Sammoud 2021 · Taylor 2018 · Dugdale 2018/2019 · Ferguson 2024 · Clark 2020 · Fernandez-Santos 2015 · Marín-Jiménez 2024. Ergänzt um: Altmann 2015 (Startdistanz 5 m), Nimphius 2016 (505/COD-Defizit), Dos'Santos 2020 (505-Protokoll), Ortega 2008 (SBJ-Reliabilität HELENA), Thomas 2020 (SBJ-Normprotokoll) und Koch 2003 (SBJ/Erwärmung, nur Kontext). Rahman 2021 bleibt nach § 6.5 ausgeschlossen. ⚠ **Dugdale et al. (2020, Sports)** — laut T1 „Volltext ✓ 06.09.“ — liegt **nicht** im Ordner; vorhanden ist nur Dugdale 2019 (EJSS, Datei „Dugdale 2018 et al.,.pdf“).

## 4 Weitere Befunde des Screenings

- **Nicht im Ordner, obwohl im Korpus geführt:** Clemente et al. (2022; T1 „Volltext ✓ 07.09.“, aber keine Datei — Maßnahme H6 offen) · Dugdale et al. (2020) · Melchiorri et al. (2023) · Negra et al. (2020) · Ruf et al. (2024) · Vickers & Altman liegt vor. Clemente 2022 wäre nach seinem Design (Randomisierung erst nach der Detraining-Phase, zwei aktive Retraining-Arme) ein R1-Kandidat ohne inaktive Kontrolle — kann erst nach Ablage im Ordner geschient werden.
- **Dubletten:** Foster et al. (2001) zweimal · Dos'Santos et al. (2020) zweimal (identische Größe 1.377.456 Byte) · Khamis & Roche als PDF und als vier JPEG.
- **Dateinamen ohne Erstautor/Jahr:** „2026 et al., Effect of neuromuscular training …“ (= Olivier et al., 2026) · „Algroy et al., …“ (2021) · „Three_Filament_Theory.pdf“ · „Dugdale 2018 et al.,.pdf“ (= 2019 EJSS).
- **Sylvester et al. (2024)** ist keine RCT, sondern einarmig (23 weibliche Volleyballspielerinnen, gepaarter t-Test) — deckt sich mit dem Ausschluss in § 6.5. **Birch et al. (2025)** ist eine biomechanische Laborstudie zur Hüpffrequenz.

## 5 Vollständige Einstufung (105 Einträge)

| Nr. | Datei (gekürzt) | Klasse | Begründung (Titel / Abstract / T1) | A4-Diagnostikbeleg |
|---|---|---|---|---|
| 1 | 1.Hilfe und DLRG_Silber KLIER.pdf | **—** | Persönliches Zertifikat, keine Literatur |  |
| 2 | 1966 Tanner et al., PHV.pdf | **R3** | Wachstums-/Reifungsgrundlage (Längsschnitt), kein Interventionsvergleich |  |
| 3 | 1976 Harris et al., Phosphorylcreatine Resynthesis.pdf | **R3** | Physiologische Grundlagenstudie (Muskelbiopsie), kein Trainingsvergleich |  |
| 4 | 1994_Khamis_Roche_Pediatrics_504-507.pdf | **R3** | Verfahrensquelle %PAH (Methodenentwicklung) |  |
| 5 | 1997 Ferris & Farley Hz_Frequenz während Plyos.pdf | **R3** | Biomechanische Laborstudie (Hüpffrequenz), kein Interventionsvergleich |  |
| 6 | 2000 Hopkins, Measures of.pdf | **R3** | Methodennorm (TE, CV, kleinster lohnender Effekt) |  |
| 7 | 2000 Mujika & Padilla, Detraining Loss of Training-Induced Physiolo… | **R3** | Narrative Übersicht (Detraining-Definition) |  |
| 8 | 2001 Foster et al., A New Approach to Monitoring Exercise Training.pdf | **R3** | Methodenquelle sRPE; ⚠ Dublette (zwei Dateien derselben Arbeit) |  |
| 9 | 2001 Foster et al., a-new-approach-to-monitoring-exercise-training.pdf | **R3** | Dublette von Foster et al. (2001) |  |
| 10 | 2001 Vickers & Altman, Analysing controlled trials with baseline an… | **R3** | Methodennorm (ANCOVA bei Prä-Post-Messung) |  |
| 11 | 2002 Mirwald et al.,.pdf | **R3** | Methodenentwicklung Maturity Offset |  |
| 12 | 2003 Koch et al., Effect of Warm-Up on the Standing Broad Jump.pdf | **R3** | Akutes Crossover (Erwärmungsroutinen, randomisierte Reihenfolge), Erwachsene; kein Trainingsinterventionsvergleich | ◆ SBJ-Protokoll/Erwärmung – nur Kontext (Erwachsene) |
| 13 | 2004 Price et al., The Football Association medical research progra… | **R3** | Prospektives Verletzungsaudit (Beobachtung) |  |
| 14 | 2005 Glaister, Multiple Sprint Work.pdf | **R3** | Narratives Review |  |
| 15 | 2005 Stølen et al., Physiology of soccer An update.pdf | **R3** | Narratives Review; nach § 6.5 nicht aufzunehmen |  |
| 16 | 2006 Nicol et al., DVZ _ SSC.pdf | **R3** | Narratives Review (DVZ) |  |
| 17 | 2006 Ratel et a., Muscle Fatigue during High-Intensity exercise in … | **R3** | Narratives Review |  |
| 18 | 2006 Seppard et al., Agility literature review Classifications, tra… | **R3** | Narratives Review (Agility-Systematik) |  |
| 19 | 2007 Jeffreys, RAMP-Erwärmung.pdf | **R3** | Praxisartikel (Erwärmungskonzept) |  |
| 20 | 2008 Ortega, Reliability of health-related physical fitness tests i… | **R3** | Test-Retest-Reliabilität einer Feldtestbatterie (HELENA), Jugendliche m/w | ◆ SBJ (Eurofit-Protokoll) – voraussichtlich „verwandt“ |
| 21 | 2009 Sáez-Sáez de Villarreal et al., DETERMINING VARIABLES OF PLYOM… | **R3** | Metaanalyse |  |
| 22 | 2010 markovic & Mikulic Neuro-MusculoskeletalandPerformance.pdf | **R3** | Narratives Review |  |
| 23 | 2010 Moher et al., CONSORT 2010 Explanation and Elaboration updated… | **R3** | Berichtsnorm CONSORT |  |
| 24 | 2011 Lloyd et al., The Natural Development of Plyometrics.pdf | **R3** | Übersichts-/Positionsartikel |  |
| 25 | 2012 Lloyd & Oliver The Youth Physical Development Model.pdf | **R3** | Konzeptpapier (YPD-Modell) |  |
| 26 | 2014 Hoffmann et al., Better reporting of interventions template fo… | **R3** | Berichtsnorm TIDieR |  |
| 27 | 2014 Malina & Koziel, Validation of maturity offset in a longitudin… | **R3** | Validierungsstudie (Längsschnitt), kein Interventionsvergleich |  |
| 28 | 2014 Turner et al., Strength and Conditioning fpr soccer players.pdf | **R3** | Narrative Übersicht |  |
| 29 | 2015 Altmann et al., starting distances affect 5-m sprint times.pdf | **R3** | Querschnittliche Messgütestudie (Sprint-Startdistanz), Erwachsene | ◆ Sprint 5 m, Lichtschranken/Startdistanz – Protokollabgleich |
| 30 | 2015 Bedoya et al., Plyometric Training Effects on Athletic Perform… | **R3** | Systematisches Review |  |
| 31 | 2015 Bianco et al., Test Batteries.pdf | **R3** | Systematisches Review über Testbatterien |  |
| 32 | 2015 Fernandez-Santos et al., Reliability and validity of tests to … | **R3** | Reliabilitäts-/Validitätsstudie, Kinder 6–12 J. (m/w) | ◆ SBJ – voraussichtlich „verwandt“ (Alter fern) |
| 33 | 2015 Smart et al., Validation of a new tool for the assessment of s… | **R3** | Berichts-/Qualitätsnorm TESTEX |  |
| 34 | 2016 Hammami Effects of an in-season plyometric training program on… | **R1** | Abstract: „randomly divided into two groups“ (E n = 15 / aktive C n = 13). ⚠ Abweichung: Vorauswahl führte R2, T1 nennt keine Randomisierung; Verfahren im Methodenteil prüfen (A3) |  |
| 35 | 2016 Lloyd et al., Changes in Sprint and Jump performance after tra… | **R1** | Abstract: „randomly assigned“ zu 4 Armen inkl. Kontrollgruppe, innerhalb der Reifegruppen; Schüler GB, keine Fußballer; dosisnächste Studie (6 Wo/12 E) |  |
| 36 | 2016 Moran et al., Age-related variation in male youth athletes’ co… | **R3** | Metaanalyse kontrollierter Studien (Moran et al., 2017, JSCR); Dateiname trägt 2016 |  |
| 37 | 2016 Nimphius Change of Direction Deficit A More Isolated Measure o… | **R3** | Querschnittsstudie (Erwachsene, Cricket) | ◆ 505 / COD-Defizit-Definition – Protokollabgleich |
| 38 | 2016 Silva et al., The Transition Period in Soccer.pdf | **R3** | Current Opinion (Übergangsperiode) |  |
| 39 | 2017 Behm et al., ffectiveness of Traditional Strength vs. Power Tr… | **R3** | Systematisches Review + Metaanalyse |  |
| 40 | 2017 Cumming et al., Bio_banding in sport_youth athletes.pdf | **R3** | Narrative Übersicht (Bio-Banding) |  |
| 41 | 2017 Haddad et al., Session-RPE Monitoring.pdf | **R3** | Narratives Review (sRPE) |  |
| 42 | 2017 radnor et al., The influence of growth and maturity on SSC.pdf | **R3** | Narratives Review |  |
| 43 | 2018 Beato et al. Effects of Plyometric and Directional Training on… | **R1** | Abstract: „randomized pre-post parallel group trial“, zwei aktive Arme (CODJ-G/COD-G), KEINE Kontrollgruppe; U18-Akademie; 10/30/40 m, Long Jump, 505 |  |
| 44 | 2018 Dos Santos et al., The effect of angle and velocity on change … | **R3** | Narratives Review (Biomechanik) |  |
| 45 | 2018 Norton, STANDARDS FOR ANTHROPOMETRY.pdf | **R3** | Norm (ISAK-Anthropometrie) |  |
| 46 | 2018 Taylor et al.,.pdf | **R3** | Test-Retest-Reliabilität (mod. 505 seitengetrennt, COD-Defizit), U12–U18 Akademie | ◆ 505 seitengetrennt, MDC – „verwandt“ (modifizierter 505, Brower) |
| 47 | 2018 Walker & Hawkins Structuring a Program in.pdf | **R3** | Praxisorientierte Übersicht (Saisonstruktur) |  |
| 48 | 2019 Hicks et a., Improving mechanical.pdf | **R3** | Methodenreview (Sprint-Kraft-Geschwindigkeits-Profil) |  |
| 49 | 2019 Negra et al. The Increased Effectiveness of Loaded Versus Unlo… | **R1** | Abstract: „randomly assigned“ zu LPJT (n = 13) / UPJT (n = 16), KEINE Kontrollgruppe; prä-PHV, Tunesien; Accepted Manuscript |  |
| 50 | 2019 Vieira et al., Match Running Performance in Young Soccer Playe… | **R3** | Systematisches Review |  |
| 51 | 2020 Clark et al., 505 COD.pdf | **R3** | Reliabilitätsstudie (Clarke et al., 2020), traditioneller 505, Rugby U17 | ◆ 505 traditionell, Between-session – Protokollabgleich |
| 52 | 2020 Dos Santos et al., 505 Change of Direction Speed Test.pdf | **R3** | Querschnittlich-biomechanisch (505 / mod. 505), Erwachsene; ⚠ Dublette (identische Dateigröße 1.377.456 Byte) | ◆ 505-Protokoll (Draper & Lancaster als Sekundärzitat) |
| 53 | 2020 Dos Santos et al., Biomechanical determinants of the modified … | **R3** | Dublette der vorstehenden Datei (identische Größe) | ◆ s. o. |
| 54 | 2020 Fröhlich et al., Statistik.pdf | **R3** | Lehrbuch (Methoden/Statistik) |  |
| 55 | 2020 Ramirez-Campillo et al. Effects of plyometric jump training.pdf | **R3** | Systematisches Review + Metaanalyse |  |
| 56 | 2020 Thomas et al., Percentile values of the standing broad jump in… | **R3** | Normwertstudie (Querschnitt) | ◆ SBJ-Normprotokoll (Hallenboden) – nur Protokollabgleich |
| 57 | 2021 Fukutani et al., Evidence for Muscle Cell-Based ... stretch sh… | **R3** | Kurzreview (Mechanismen) |  |
| 58 | 2021 Hilska et al., Neuromuscular Training Warm-up Prevents Acute N… | **R1** | Titel: Cluster-RCT (Randomisierung auf Vereins-/Stadtebene); Zielgröße Verletzungen → nach A4 ohne Zielgrößen-Überschneidung; nur Kontext und A7 (Adhärenzverlauf) |  |
| 59 | 2021 McBurnie et al., Deceleration.pdf | **R3** | Narratives Review |  |
| 60 | 2021 Rahman et al., Reliability, validity, and norm references of s… | **R3** | Reliabilitäts-/Normwertstudie; nach § 6.5 nicht aufzunehmen | (◆ SBJ – ausgeschlossen nach § 6.5) |
| 61 | 2021 Sammoud et al., sensitivity COD linear sprint prepubertal male… | **R3** | Test-Retest-Reliabilität und Sensitivität (505, 5/10/20 m), präpubertäre Fußballer | ◆ 505 nach Draper & Lancaster, Microgate – voraussichtlich „identisch“ (Gerät) / „verwandt“ (Alter) |
| 62 | 2021 Tomkinson et al., Temporal Trends in the Standing Broad Jump P… | **R3** | Systematische Trendanalyse (Normwerte) |  |
| 63 | 2022 Aloui et al. Combined Plyometric and Short Sprint training.pdf | **R1** | Abstract: „allocated at random“, EG n = 17 / aktive CG n = 17; U15, Tunesien. ⚠ Abstract berichtet Baseline-Signifikanztest („no baseline difference … p ≥ 0.05“) |  |
| 64 | 2022 Asimakidis et al., COVID-19 negative effetct detraining.pdf | **R3** | Einarmige Prä-Post-Beobachtung (n = 29, gepaarte t-Tests), kein Vergleichsarm. ⚠ Abweichung: Vorauswahl führte R2 – ohne zweiten Arm ist es keine kontrollierte Studie; bleibt E5-Kontext (2.3) |  |
| 65 | 2022 McBurnie et al. Multidirectional_Speed_in_Youth_Soccer_Players… | **R3** | Narrative Übersicht / konzeptioneller Rahmen |  |
| 66 | 2022 McKay et al., Defining Training and Performance Caliber A Part… | **R3** | Klassifikationsrahmen (Tier-System) |  |
| 67 | 2022 Morgan et al., Change of direction frequency off the ball new … | **R3** | Beobachtungsstudie (Notationsanalyse) |  |
| 68 | 2022 Parr et al., Maturity Associated Differences in Match Running … | **R3** | Beobachtungsstudie (GPS) |  |
| 69 | 2023 Liu et al., Session RPE als monitoring tool.pdf | **R3** | Metaanalyse zur Kriteriumsvalidität der sRPE (PRISMA), keine Intervention |  |
| 70 | 2023 Ramirez-Campilo et al., Plyometric‑Jump Training Effects on Ph… | **R3** | Systematisches Review + Metaanalyse |  |
| 71 | 2024 Ferguson et al., reliability-of-measures-of-lower-body-strengt… | **R3** | Reliabilitätsstudie (3 Termine), Akademie 14,7 J. | ◆ Sprint 5/10/30 m – voraussichtlich „verwandt“; Gerät/Startdistanz prüfen |
| 72 | 2024 Liu et al. Supervised Offseason Training Programs are able to … | **R1** | Titel/Abstract: „randomized parallel controlled study“, 4 Arme inkl. inaktive Kontrolle; U19, Off-Season, 3 Wo/6 E; CMJ, 30 m, YYIRT |  |
| 73 | 2024 Moran et al. Effect of vertical, horizontal, and combined.pdf | **R1** | Abstract: „randomly allocated“, drei aktive Arme (VPT/HPT/V+HPT), KEINE Kontrollgruppe; Erwachsene (22,3 J.) |  |
| 74 | 2024 Oliver et al.The Effects of Strength, Plyometric and Combined … | **R3** | Systematisches Review + Metaanalyse |  |
| 75 | 2024 Sammoud et al. Effects of plyometric jump training.pdf | **R1** | Titel: „A randomized controlled trial“; PJT n = 13 / aktive CG n = 14; prä-PHV; 505, CMJ, SLJ, Hop-Tests; ANCOVA mit Baseline |  |
| 76 | 2024 Sylvester et al., Hz-Dosis Plyos.pdf | **R3** | Einarmige Prä-Post-Studie (gepaarter t-Test), weibliche Volleyballspielerinnen post-PHV, Neuseeland/Tschechien; nach § 6.5 nicht aufzunehmen |  |
| 77 | 2025 Birch et al., Hz Plyos.pdf | **R3** | Biomechanische Laborstudie (Hüpffrequenz/Untergrund), kein Interventionsvergleich |  |
| 78 | 2025 Dambel et al., Lifestyle disruptions.pdf | **R3** | Scoping Review |  |
| 79 | 2025 Flores et al., Skeletal age.pdf | **R3** | Modellentwicklung/-validierung (Querschnitt) |  |
| 80 | 2025 Padron-Cabro et al., Effects of a Short-Term Detraining Period… | **R2*** | Zwei nicht randomisierte Jahrgangskohorten (U15 n = 17 / U17 n = 13) mit Prä-Post-Vergleich über 2 Wo In-Season-Trainingsstopp; KEINE Intervention, beide Gruppen exponiert. Formal kein R2 (keine Interventionsstudie), aber die einzige Arbeit im Ordner mit unserer Kernkonstellation „Jahrgangsunterschied zwischen den Gruppen“ → Empfehlung: als R2-Sonderfall mitführen (Schwerpunkt: Umgang mit Alters-/Reifeunterschied in der Auswertung) | ◆ 5/10 m Splits, mod. 505 – zusätzlich Diagnostikabgleich |
| 81 | 2025 Zheng et al. Effects of plyometric training on jump, sprint, a… | **R3** | Systematisches Review + Metaanalyse |  |
| 82 | 2026 Bouafif et al. Effects of plyometric jump training on measures… | **R1** | Titel: „A randomized controlled trial“; stratifiziert nach Reifestatus, aktive Kontrolle; Tier 2; 505, Single-leg hop, Y-Balance.; 15 Seiten, Text extrahierbar |  |
| 83 | 2026 et al., Effect of neuromuscular training strategies on injury … | **R3** | Systematisches Review + Metaanalyse (Olivier et al., 2026); Dateiname ohne Erstautor |  |
| 84 | 2026 Havanecz et al., Leg dominance influences side-specific direct… | **R3** | Beobachtungsstudie (Saisonlängsschnitt) |  |
| 85 | Algroy et al., Motion Analysis of Match Play in U14 Male Soccer Pla… | **R3** | Deskriptive Beobachtungsstudie (GPS); Dateiname ohne Jahr (2021) |  |
| 86 | anyconnect-win-4.10.08029-core-vpn-webdeploy-k9.msi | **—** | Software-Installer, keine Literatur |  |
| 87 | Checkliste_Traininsgprogramm.docx | **—** | Eigenes Arbeitsdokument |  |
| 88 | Dugdale 2018 et al.,.pdf | **R3** | Between-day-Reliabilität + Diskriminanzvalidität (Dugdale et al., 2019, EJSS; Online-first 2018), U11–U17 drei Leistungsstufen | ◆ SBJ, 505, 10/20 m – „verwandt“; ⚠ Dugdale et al. (2020, Sports; Witty Dual-Beam) laut T1 geprüft, Datei liegt NICHT im Ordner |
| 89 | dvs-Richtlinien-2020_11.pdf | **R3** | Formale Norm (Manuskriptgestaltung) |  |
| 90 | European Journal of Sport Science - 2024 - Marin‐Jimenez - Criterio… | **R3** | Validitäts-/Reliabilitätsstudie, Erwachsene 18–64 J. | ◆ SBJ – voraussichtlich „nicht vergleichbar“ (Erwachsene), nur Protokollabgleich |
| 91 | Khamis_Roche_Seite1.jpeg | **—** | Seitenbild der Khamis-&-Roche-PDF (Dublette als Bild) |  |
| 92 | Khamis_Roche_Seite2.jpeg | **—** | Seitenbild (Dublette) |  |
| 93 | Khamis_Roche_Seite3.jpeg | **—** | Seitenbild (Dublette) |  |
| 94 | Khamis_Roche_Seite4.jpeg | **—** | Seitenbild (Dublette) |  |
| 95 | Leitfaden für wiss. Arbeiten_BA SMK_final.pdf | **R3** | Formale Vorgabe DSHS (SMK-Leitfaden) |  |
| 96 | Leitfaden_Abschlussarbeiten_TUM.pdf | **R3** | Formaler Leitfaden (TUM) |  |
| 97 | Leitfaden_wissenschaftl_Arbeit_Sportmedizin.pdf | **R3** | Formaler Leitfaden |  |
| 98 | Lloyd (A) Bodyweight squats and (B) in-line lunges..jpeg | **—** | Abbildungsausschnitt aus Lloyd et al. (2011), keine eigene Quelle |  |
| 99 | Llyod_Korrektes_Unkorrektes_Landen_Sprung.jpeg | **—** | Abbildungsausschnitt (Lloyd 2011) |  |
| 100 | Llyod_Progression_Plyos_Alter.jpeg | **—** | Abbildungsausschnitt (Lloyd 2011) |  |
| 101 | Llyod_Sprünge.jpeg | **—** | Abbildungsausschnitt (Lloyd 2011) |  |
| 102 | Notion Setup 7.32.0.exe | **—** | Software-Installer, keine Literatur |  |
| 103 | Rechercheprotokoll_Suchstrings_2026-09-02.docx | **—** | Eigenes Arbeitsdokument (liegt zusätzlich in Claude\) |  |
| 104 | Three_Filament_Theory.pdf | **R3** | Physiologisches Review (Titin/Muskelmodell), Jahr/Autor im Dateinamen fehlen |  |
| 105 | Verletzungsprävention_Vereinssport.pptx | **—** | Eigene Präsentation |  |

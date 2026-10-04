# Rückfragenprotokoll der Blindrechnung in R

Zweite, unabhängige Implementierung nach Spezifikation_2026-09-24 (Stand Nachtrag 2). Jede Rückfrage und jede Antwort mit Datum. Antworten werden wörtlich eingetragen, sobald sie vorliegen. Bis zur Antwort wird die betroffene Stelle nicht gerechnet. Stand nach den Antworten vom 2026-09-25: keine Rückfrage offen.

## Rückfragen aus Schritt 0 (Lesen), gestellt am 2026-09-25

### R1 (2026-09-25) S11 DSESOI zum Zeitpunkt POST

S11 verlangt „Mittel von Δ geteilt durch SESOI desselben Ziels und Zeitpunkts“ und die Anlage _Kennungen.csv führt `S11.DSESOI.{Z05,Z10,Z30,SBJ,CL,CR}.{PRE,POST}.ALL.X`, also auch POST. Nach Nachtrag 2 (N4.10) gelten S, SESOI, CV, RTS und FLEINZ in S10 nur prä. S11 ist laut F.7 unverändert. Für POST gibt es damit kein SESOI in S10.

Mögliche Lesarten:
- (a) SESOI post wird intern nach S10 Regel 5 und 6 aus den BEST-Werten post gebildet (S = SD der BEST post aller Spieler mit BEST post, beide Gruppen, SESOI = 0,2 · S) und nur für S11 verwendet, ohne eigene Kennung.
- (b) DSESOI post wird mit dem SESOI prä derselben Zielgröße gebildet.
- (c) DSESOI post ist fehlend mit Grund „Eingang fehlt“.

Antwort (2026-09-25, Verfasser per Auswahl im Chat): Lesart (a). SESOI post wird intern nach S10 Regel 5 und 6 aus den BEST-Werten post gebildet und nur in S11 verwendet, ohne eigene Kennung. Umsetzung: Schalter LESART_R1 in S11_Bestwertbias_2026-09-25.R auf „a“.

### R2 (2026-09-25) Zuordnung der Gründe für fehlende Werte (G.1 Nr. 4)

G.1 Nr. 4 nennt acht zulässige Gründe, ordnet sie aber nicht den einzelnen Fällen zu. Vorgeschlagene Zuordnung, bitte bestätigen oder ändern:
- „zu wenige Werte“: Statistik verlangt mehr Werte als vorhanden (0.5 Nr. 13). Fälle: BEST und MEAN bei k = 0 (S04), Mittel, Median, Minimum und Maximum bei n = 0, SD bei n < 2, TE bei leerer TE-Menge oder df_TE = 0, S bei n_S < 2, S11 DMEAN bei n = 0, Shapiro-Wilk bei n < 3, S18 bei df2 ≤ 0.
- „Eingang fehlt“: abgeleitete Größe, deren Eingang fehlt (0.5 Nr. 3). Fälle: CM bei fehlender Seite, MP bei fehlender Elterngröße, PAS und %PAH bei fehlender Körperhöhe, Körpermasse oder Elterngröße, TELO, TEHI, CV, RTS und FLEINZ bei fehlendem TE, SESOI und RTS bei fehlendem S, DSESOI bei fehlendem SESOI oder fehlendem DMEAN.
- „außerhalb Gültigkeitsbereich“: Alter außerhalb 4,0 bis 17,5 Jahre (S05 Regel 4), dann PAS und %PAH.
- „nicht erhebbar“: Adhärenz-Einzelwerte GANZ, WOCAP und DIST bei kein_Listenplatz = ja (S07 Regel 5).
- „Fallzahlregel“: alle Kennungen einer Analyse mit INF = 0, einschließlich SIG (S13 bis S17, S19) und die Vorab-Prüfung S14 Regel 6 in der Menge BPAH.
- „Rang“: Designmatrix ohne vollen Rang (0.5 Nr. 11), auch für die Sensitivitätsmodelle und die Prüfmodelle.
- „konstant“: Division durch eine SD oder ein SESOI gleich 0 (d in S12, g in S15, RTS in S10, DSESOI in S11, Verhältnis SD_KG / SD_IG in S14 bei SD_IG = 0).
- „keine Nullstelle“: S18 MDES, wenn Power(10) unter 0,80 liegt (S18 Regel 4).

Antwort (2026-09-25, Verfasser per Auswahl im Chat): Zuordnung bestätigt. Umsetzung: Konstanten GRUND_... in Funktionen_2026-09-25.R, Verwendung in S04 bis S19.

### R3 (2026-09-25) S06 Regel 9 Sammelmeldungspaar

Ein Dublettenpaar ist definiert über denselben Analysecode, Abstand STARTED höchstens 5 Minuten und identische Werte in H003 bis H009. Ein Sammelmeldungspaar über denselben Code, höchstens 5 Minuten Abstand und „abweichenden Inhalt“.

Mögliche Lesarten:
- (a) „abweichender Inhalt“ = nicht identisch in H003 bis H009, also das Komplement der Dublettendefinition innerhalb des 5-Minuten-Abstands. Jedes Paar wird gezählt, auch wenn eine Meldung zu mehreren Paaren gehört, wie bei Dubletten.
- (b) ein anderer Feldumfang (welcher?).

Antwort (2026-09-25, durch die Instanz nach Freigabe des Verfassers vom 2026-09-25, Rückfragen wenn möglich selbst zu klären): Lesart (a). Begründung: Regel 9 definiert das Dublettenpaar über die Felder H003 bis H009, das Sammelmeldungspaar ist im selben Satz als Gegenstück mit „abweichendem Inhalt“ eingeführt, ein anderer Feldumfang ist nirgends genannt. Umsetzung: Funktion paare_zaehlen in Funktionen_2026-09-25.R, Aufruf in S06.

### R4 (2026-09-25) S14 Regel 6 Fallzahlregel in der Menge BPAH

Regel 6 nennt „mit der Fallzahlregel S08 Regel 3 für diese Menge“ vor dem Prä-Modell. Danach folgt der Shapiro-Wilk-Test der BEST-Werte prä je Gruppe in derselben Menge.

Mögliche Lesarten:
- (a) Die Fallzahlregel gilt für beide Vorab-Prüfungen. Bei n_IG < 8 oder n_KG < 8 in BPAH sind CINT bis PCINT und SWW, SWP für BPAHIG und BPAHKG fehlend mit Grund „Fallzahlregel“.
- (b) Die Fallzahlregel gilt nur für das Prä-Modell. Shapiro-Wilk je Gruppe wird gerechnet, sobald n ≥ 3 in der Gruppe.

Antwort (2026-09-25, durch die Instanz nach Freigabe des Verfassers vom 2026-09-25): Lesart (a). Begründung: Die Regel nennt die Fallzahlregel „für diese Menge“, also für die Menge BPAH als Ganzes, und P5 stellt fest, dass beide Vorab-Prüfungen auf denselben Spielern laufen. Im vorliegenden Datenstand ist die Fallzahlregel in BPAH für alle drei konfirmatorischen Zielgrößen erfüllt, die Lesart hat daher keinen Einfluss auf die Ausgabe. Umsetzung: Schalter LESART_R4 in S14_Voraussetzungen_2026-09-25.R auf „a“.

### R5 (2026-09-25) Referenztest R08 (GEAR, Brown-Forsythe) nicht bestanden

Der Referenztest R08 nach Anlage _Referenzdaten.csv besteht in zwei von vier Sollwerten nicht, alle übrigen 81 Sollwerte der Tests R01 bis R13 bestehen:
- Teststatistik W: Soll 1,705910 (Handbuch 1.3.5.10, Dataplot), eigener Wert 1,7059176930, Abweichung 7,7e-6, Toleranz 5e-7. Eine unabhängige Kontrollrechnung mit den R-Funktionen lm und anova auf |y − Gruppenmedian| liefert denselben Wert 1,7059176930. Die Varianten mit Gruppenmittel (2,15946) und getrimmtem Mittel (2,15371) liegen weit entfernt, der Handbuchwert gehört also zur Medianvariante. Die Größe der Abweichung entspricht einer Rechnung mit einfacher Genauigkeit in der Quelle oder einer Abweichung einzelner Datenwerte der Anlage gegenüber der Quelle. Die Varianzstatistik T des Tests R13 aus denselben 100 Werten (Soll 0,3903, eigener Wert 0,390304) besteht.
- F_9,90(0,95): Soll 1,9855 (gedruckt), eigener Wert 1,9855949637, Abweichung 9,5e-5, Toleranz 5e-5. Der gedruckte Wert ist offenbar abgeschnitten statt gerundet (gerundet wäre 1,9856). Alle anderen Quantiltests (R06, R07, R13) bestehen.

Nach G.2 hält ein nicht bestandener Test die Auswertung an, nach G.3 wird eine Toleranz nicht durch die Instanz angepasst. Mögliche Wege, jeweils als datierter Nachtrag durch den Verfasser:
- (a) Die beiden Sollwerte bleiben, die Toleranz wird in der Anlage für W auf 1e-5 und für F_9,90(0,95) auf 1e-4 gesetzt, mit Begründung (Genauigkeit der Quelle). Der Test gilt dann als bestanden.
- (b) Die beiden Sollwerte werden durch Werte aus einer anderen Quelle ersetzt.
- (c) Der Test bleibt nicht bestanden. Dann kann der Gesamtlauf über die Studiendaten nicht beginnen.

Antwort (2026-09-25, Verfasser per Auswahl im Chat): Weg (a), datierter Nachtrag zur Toleranz. Nachtrag Toleranz R08 vom 2026-09-25: Für R08 Teststatistik W gilt die Toleranz 1e-5 statt 5e-7, für R08 F_9,90(0,95) die Toleranz 1e-4 statt 5e-5. Grund: Genauigkeit der Quelle (Rechnung in einfacher Genauigkeit in Dataplot, gedruckter Quantilwert abgeschnitten). Alle übrigen 81 Sollwerte behalten ihre Toleranz. Umsetzung: Tabelle NACHTRAEGE_TOLERANZ in Referenztests_2026-09-25.R, die Anlage _Referenzdaten.csv bleibt unverändert. Ergänzende Prüfung der Instanz: Werden die 100 Datenwerte in einfacher Genauigkeit gespeichert und in doppelter gerechnet, verschiebt sich W bereits um etwa 2e-6, also in der Größenordnung der beobachteten Abweichung.

## Anmerkungen ohne Rückfrage (Lesarten und Hinweise, 2026-09-25)

- A1 Für die Vorab-Prüfungen (S14 Regel 6) ist in der Anlage _Kennungen.csv kein Merkmal VERW vorgesehen. Die Anlage ist maßgeblich, es wird kein VERW dafür ausgegeben.
- A2 Die Prüfsummenliste des Datenstands deckt nur die sechs Dateien des Datenstands ab. Für die Anlagen der Spezifikation und den Prozessplan gibt es keine Sollprüfsummen. Ihre SHA-256-Werte werden im Laufprotokoll und in den Skriptköpfen dokumentiert, ohne Sollabgleich.
- A3 Alle abgegebenen Dateien kommen in den Unterordner `Abgabe_R_2026-09-25` des Ordners Blindrechnung_R_2026-09-24. Die Eingangsdateien bleiben unverändert.
- A4 R 4.3.3 aus den Ubuntu-Paketquellen (noble, universe) ist installierbar. Diese R-Fassung hat keine eingebaute SHA-256-Funktion. Die Prüfsummen werden in reinem R gerechnet (eigene Funktion in der Funktionsbibliothek) und im Validierungsprotokoll gegen das Systemwerkzeug sha256sum gegengeprüft. Zusatzpakete werden nicht verwendet.
- A5 S06 NKORR wird als Zahl der Meldungen gezählt, deren CASE in der Korrekturliste steht. Alle sieben CASE-Nummern sind im Export vorhanden.
- A6 Da nach K7 jede Meldung zählt, kann GANZ je Spieler 12 überschreiten. Dann decken V00 bis V12 nicht alle zugeteilten Spieler ab. Tritt das ein, wird es im Laufprotokoll gemeldet.
- A7 S08 Regel 8 FLPRE verwendet „gültig“ im Sinn von S02 Regel 3 (nach der Auslöseprüfung).
- A8 S06 Regel 9 „höchstens 5 Minuten“ wird als |Δ STARTED| ≤ 300 s mit eingeschlossener Grenze gelesen. STARTED wird als exportierte Ortszeit ohne Zeitzonenumrechnung verarbeitet (K6). Der Zeitraum W1 bis W6 enthält keinen Wechsel der Sommerzeit.
- A9 Die Zuordnungstabelle liegt im Datenstand als zwei Dateien vor (Zuordnung_Fragebogen.csv und Listenplatz_IG.csv). Zusätzliche Strukturprüfung in S01: die Codes in Listenplatz_IG.csv sind genau die IG-Codes der Personendaten, jeder Analysecode der Zuordnung steht in den Personendaten und ist IG, ein IG-Spieler mit kein_Listenplatz = ja darf keinem Listenlabel zugeordnet sein. Verstöße führen zum Abbruch.
- A10 Bei INF = 0 werden in S13, S16 und S17 die Anzahlen n_IG und n_KG der Analyse ausgegeben (Rechenkonvention 0.5 Nr. 13, Zahlen werden immer ausgegeben), alle übrigen Kennungen der Analyse fehlen mit Grund „Fallzahlregel“, in S13 auch SIG, PREM und PAHM (Regel 3 gilt nur bei INF = 1). Im vorliegenden Datenstand haben alle drei ITT-Sets INF = 1, die Lesart wirkt nur auf Per-Protokoll- und Sensitivitätssets mit INF = 0.
- A11 Bei INF = 0 einer Zielgröße werden in S14 keine Grafikdateien erzeugt, weil kein Modell vorliegt. Im vorliegenden Datenstand betrifft das keine Zielgröße.
- A12 Mittel und Standardabweichung werden in der Bibliothek um den ersten Wert verschoben gerechnet (zweistufiger Algorithmus). Das ist mathematisch identisch mit den Formeln in 0.5 und war nötig, damit der Referenztest R03 (AtmWtAg) die geforderten 9 Stellen erreicht. Der Referenztest R01 prüft die Exaktheit.
- A13 Kleinste Quadrate laufen über eine QR-Zerlegung der spaltenweise auf Norm 1 skalierten Designmatrix mit Rückskalierung der Koeffizienten und der Kovarianzmatrix. Der Referenztest R05 (Longley) prüft die numerische Stabilität. Eine Designmatrix ohne vollen Rang wird nach 0.5 Nr. 11 erkannt (Toleranz der QR-Zerlegung in R, 1e-7).

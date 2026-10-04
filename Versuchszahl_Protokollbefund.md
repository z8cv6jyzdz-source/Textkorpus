# Versuchszahl und Versuchsausfälle — systematische Festhaltung

**Stand 09.09.2026.** Sachverhalt, Ursache, statistische Folge und Entscheidung für die ausstehenden Post-Termine. Grundlage: Blatt `02_Rohdaten` des Workbooks, Rechnungen in `Claude\Versuchszahl_Rechenausgabe.txt`.

---

## 1  Der Sachverhalt

Das Testprotokoll sah **drei Versuche je Spieler und Zielgröße** vor. Diese Vorgabe wurde nicht durchgängig eingehalten: Ein Teil der Spieler absolvierte aus Zeitgründen nur zwei Versuche. Die tatsächliche Versuchszahl ist je Spieler, Zielgröße und Zeitpunkt im Messprotokoll dokumentiert; daraus geht ebenso die Zahl der fehlgeschlagenen Versuche hervor.

**Der Sachverhalt ist damit vollständig rekonstruierbar** — das ist die Voraussetzung dafür, ihn methodisch behandeln zu können statt ihn nur zu benennen.

---

## 2  Die Ursache — und eine Korrektur

⚠ **Richtigstellung zur Formulierung.** Die Kausalkette lautet: Die Interventionsgruppe bestand an den jeweiligen Testterminen aus **weniger** Spielern als die Kontrollgruppe (Verein A n = 7, Verein B n = 11, Verein C n = 13). Daraus folgt **mehr Zeit je Spieler in der Interventionsgruppe**, nicht in der Kontrollgruppe. Genau das zeigen die Daten: Die IG hat durchweg die höhere mittlere Versuchszahl.

| Verein | Gruppe | n | mittlere gültige Versuche (5 m / 10 m / 30 m / SBJ / 505 L / 505 R) |
|---|---|---|---|
| Hohenlind + Blau-Weiß | Intervention | 18 | 2,22 · 2,56 · 2,61 · 2,50 · 1,94 · 2,00 |
| Vorwärts Spoho | Kontrolle | 13 | 1,62 · 1,62 · 2,38 · 2,08 · 1,83 · 2,08 |

**Der Mechanismus ist organisatorisch, nicht leistungsbezogen** — und genau deshalb eine Verzerrungsquelle: Er wirkt auf das Messergebnis, ohne mit der Leistung zusammenzuhängen.

**Was es verhindert hätte:** eine von vornherein einheitliche Festlegung auf zwei Versuche je Spieler, oder eine an die Gruppengröße angepasste Zeitplanung. Beides gehört als Empfehlung in 6.3 und 7.2.

---

## 3  Die Ausfälle sind bereits sauber protokolliert

Auszählung der 174 nicht gültigen Prä-Versuche aus `02_Rohdaten`:

| Grund | Anzahl | Charakter |
|---|---|---|
| „System nicht aufgenommen" | **94** | technischer Ausfall der Lichtschranke — leistungsunabhängig |
| „Nur 2 Versuche aus Zeitmangel" | **61** | organisatorisch — leistungsunabhängig, aber **gruppensystematisch** |
| „Linie nicht getroffen" | **12** | Fehlversuch im 505 — **potenziell leistungsabhängig** |
| „Kein fester Stand" / „Fehlversuch" | 4 | Fehlversuch — potenziell leistungsabhängig |
| ohne Bemerkung | 3 | zu klären |

⚠ **Zahlenkorrektur:** Die Projektanweisungen (§ 3) und die Sitzungsnotizen führen „sechs 505-Versuche wegen ‚Linie nicht getroffen'". **Tatsächlich sind es zwölf.** Vor der Verwendung in 5.1 zu berichtigen.

**Drei Ausfallmechanismen, die getrennt zu berichten sind** (CONSORT Item 13b verlangt Art und exakten Grund):
1. **Technischer Ausfall** (94) — trifft überwiegend den 5-m-Sprint, weil die Lichtschranke den Start bei 0,5 m oft nicht registrierte. Leistungsunabhängig, aber nicht gleichverteilt über die Zielgrößen.
2. **Zeitmangel** (61) — leistungsunabhängig, aber systematisch nach Gruppengröße und damit nach Gruppe.
3. **Fehlversuch** (16) — der einzige Mechanismus, der mit der Leistung zusammenhängen kann. Wer riskanter wendet, verfehlt die Linie eher.

---

## 4  Die statistische Folge — kleiner als zunächst gerechnet

Der Bestwert aus k Versuchen ist ein Extremwert; sein Erwartungswert verschiebt sich mit k. Die frühere Angabe stützte sich auf eine Modellrechnung über Erwartungswerte des Minimums normalverteilter Messfehler. **Die direkte Messung an den eigenen Daten ergibt einen deutlich kleineren Effekt.**

Gemessen wurde bei allen Spielern mit drei gültigen Versuchen: Bestwert aus drei gegen Bestwert aus den ersten zwei — ohne jede Modellannahme.

| Zielgröße | n (k = 3) | Gewinn des 3. Versuchs | × SESOI | Modellrechnung sagte |
|---|---|---|---|---|
| Sprint 10 m | 10 | −0,0050 s | **0,23** | 0,49 |
| Sprint 30 m | 17 | −0,0159 s | **0,25** | 0,35 |
| Standweitsprung | 12 | +0,75 cm | **0,23** | 0,52 |
| Sprint 5 m | 6 | −0,0283 s | 1,79 | 0,82 |
| 505 links | 4 | −0,0325 s | 1,43 | 1,10 |
| 505 rechts | 4 | −0,0750 s | 3,22 | 1,00 |

**Belastbar sind nur die ersten drei Zeilen** (n = 10 bis 17). Dort liegt der Effekt konsistent bei rund **einem Viertel des SESOI je zusätzlichem Versuch** — real und gerichtet, aber etwa halb so groß wie die Modellrechnung nahelegte. Die drei unteren Zeilen beruhen auf vier bis sechs Fällen und sind nicht interpretierbar.

⚠ **Konsequenz für die bisherigen Dokumente:** Die Angabe „scheinbarer IG-Vorsprung von zwei Dritteln bis vier Fünfteln des SESOI" im Statistik-Lehrgang und in den Sitzungsnotizen ist eine **Modellrechnung**, die die Daten so nicht bestätigen. Die belastbare Formulierung lautet: **rund ein Viertel des SESOI je zusätzlichem Versuch, bei einer mittleren Differenz von 0,6 bis 0,9 Versuchen zwischen den Gruppen im Sprint.**

---

## 5  Der kontraintuitive Teil: Einheitlichkeit im Post-Test löst das Problem nicht

Im ANCOVA-Modell gilt für den geschätzten Gruppeneffekt:

```
b1_beobachtet  =  b1_wahr  +  ( Δb_post  −  β₂ · Δb_prä )
```

mit Δb = Bias der IG minus Bias der KG und β₂ = Regressionsgewicht des Prä-Werts (0,6 bis 0,9).

Daraus folgt etwas, das der Intuition widerspricht:

| Szenario | Δb_post | Verbleibender Bias | Sprint 10 m in SESOI |
|---|---|---|---|
| Post **einheitlich** für alle | 0 | −β₂ · Δb_prä | **+0,52** (zuungunsten der IG) |
| Post mit **derselben** Ungleichverteilung wie prä | = Δb_prä | (1 − β₂) · Δb_prä | −0,13 |

**Eine einheitliche Post-Versuchszahl beseitigt den Bias nicht — sie lässt den vollen Prä-Bias mal β₂ stehen.** Der Grund: Die ANCOVA subtrahiert den verzerrten Prä-Wert mit dem Gewicht β₂ vom unverzerrten Post-Wert.

Praktisch lässt sich die Prä-Verteilung im Post-Test aber weder reproduzieren noch wäre das methodisch vertretbar. **Die Lösung liegt deshalb nicht in der Versuchszahl, sondern im Aggregat** — siehe § 6.

---

## 6  Die eigentliche Lösung: der Mittelwert als Sensitivitätsanalyse

Der Erwartungswert des **Mittelwerts** ist unabhängig von k. Nur seine Präzision hängt von k ab (SE = TE/√k). Der Mittelwert hat also **keinen** versuchszahlabhängigen Bias.

Vergleich an den Prä-Daten:

| Zielgröße | Δroh Bestwert | Δroh Mittelwert | gepoolte SD: Änderung |
|---|---|---|---|
| Sprint 5 m | −0,0851 s | −0,0794 s | −10,7 % |
| Sprint 10 m | −0,1178 s | −0,1158 s | −4,7 % |
| Sprint 30 m | −0,4068 s | −0,4211 s | −2,6 % |
| Standweitsprung | 12,98 cm | 12,00 cm | +1,4 % |
| 505 links | −0,0769 s | −0,0903 s | −10,0 % |
| 505 rechts | −0,0196 s | −0,0235 s | −4,1 % |

Zwei Effekte überlagern sich: Die Gruppendifferenz ändert sich kaum, die **Streuung sinkt** aber deutlich — der Mittelwert ist das präzisere Maß. Deshalb fällt die standardisierte Effektstärke mit dem Mittelwert sogar größer aus, obwohl der Unterschied in Rohheiten gleich bleibt.

**Festlegung:** Hauptanalyse mit dem **Bestwert** (Konvention der Leistungsdiagnostik, Vergleichbarkeit mit der Literatur). **Sensitivitätsanalyse mit dem Mittelwert** — sie ist die eigentliche Absicherung gegen den Versuchszahl-Effekt und in 4.7 zu dokumentieren. Weichen beide Analysen im Ergebnis nicht ab, ist der Punkt erledigt; weichen sie ab, gehört das in 6.1.

---

## 7  Entscheidung für die zwei ausstehenden Post-Termine

**Empfehlung: drei Versuche anpeilen.** Begründung:

1. **Für den differentiellen Bias ist die Zahl gleichgültig, solange sie zwischen den Gruppen gleich ist.** Zwei oder drei — entscheidend ist, dass beide ausstehenden Termine dieselbe Vorgabe haben.
2. **Der dritte Versuch bringt 18 Prozent Präzision** (SE sinkt von TE/√2 auf TE/√3). Bei ohnehin knapper Auflösung ist das nicht nichts.
3. **Man kann später auf zwei kürzen, aber nicht auf drei erweitern.** Wer drei erhebt, kann in der Analyse einheitlich die ersten zwei verwenden. Umgekehrt ist die Information verloren.
4. **Drei entspricht dem Protokoll** und damit dem Ethikantrag; eine Abweichung müsste begründet werden.

**Zwei Bedingungen, ohne die die Empfehlung nicht gilt:**

- ⚠ **Die Zeitplanung muss drei Versuche tatsächlich hergeben.** Genau daran ist es im Prä-Test gescheitert. Wenn absehbar ist, dass die größere Gruppe nur zwei schafft, dann **für beide Termine zwei festlegen** — konsequent und vorab, nicht während des Termins entschieden. Eine bewusste Zwei-Versuche-Regel ist besser als ein unabsichtlicher Mix.
- ⚠ **Abgleich mit dem bereits getesteten IG-Verein.** Wurde dort am 01.–03.09. mit drei Versuchen getestet, spricht alles für drei. Wurde mit zwei getestet, entstünde bei drei eine Ungleichheit **innerhalb** der IG. Diese Zahl ist vor dem morgigen Termin aus dem Messprotokoll zu prüfen.

**In jedem Fall:**
- Versuchszahl je Spieler und Zielgröße protokollieren, getrennt nach nicht durchgeführt / technisch ausgefallen / Fehlversuch.
- Nach der Dateneingabe die mittleren Versuchszahlen je Gruppe und Zeitpunkt vergleichen (Maßnahmenliste D1).
- Mittelwert-Sensitivitätsanalyse rechnen.

---

## 8  Verortung im Manuskript

| Abschnitt | Was hineingehört |
|---|---|
| **4.4** | Protokollvorgabe drei Versuche; tatsächliche Umsetzung; die drei Ausfallmechanismen mit Zahlen |
| **4.7** | Bestwert als Aggregationsregel; Mittelwert-Sensitivitätsanalyse mit Begründung |
| **5.1** | Mittlere Versuchszahlen je Gruppe und Zeitpunkt; Zahl der Ausfälle je Grund (⚠ zwölf, nicht sechs, im 505) |
| **6.1** | Einordnung: organisatorisch bedingte Ungleichheit, gerichtet zugunsten der IG, Größenordnung rund ein Viertel SESOI je Versuch; Ergebnis der Mittelwert-Sensitivitätsanalyse |
| **6.3 / 7.2** | Empfehlung: Versuchszahl vorab an der Gruppengröße ausrichten oder von vornherein einheitlich auf zwei festlegen |

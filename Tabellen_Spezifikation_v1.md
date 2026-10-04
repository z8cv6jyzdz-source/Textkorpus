# Spezifikation: Evidenztabelle im Review-Format (v4)

**Bachelorarbeit U15-Plyometrie · Übergabedokument für den Codier-Task · Stand 30.08.2026**

Dieses Dokument ist die vollständige Vorgabe für die Neucodierung der Evidenztabelle. Es setzt keinen Kontext aus der vorangegangenen Sitzung voraus.

---

## 0 Grundregel für den Codier-Task

**Die Daten sind fertig und verifiziert. Der Codier-Task rechnet nichts nach, recherchiert nichts und interpretiert nichts — er rendert.**

Eingabe: die fünf CSV-Dateien in `Schreiben\ev3_daten\` (Semikolon-getrennt, UTF-8 mit BOM). Sie enthalten 22 am Volltext geprüfte Quellen, 73 Befundzeilen, 17 Anforderungskennwerte, 21 Zitierfallen, 5 Synthesen. Jede Zahl darin stammt aus dem **Ergebnisteil** der jeweiligen Arbeit, nie aus dem Abstract.

Wenn im Codier-Task eine Zahl fehlt oder unklar ist: **nicht schätzen, nicht aus dem Abstract ergänzen** — Feld leer lassen und in eine Liste offener Punkte schreiben.

---

## 1 Analyse der Referenzarbeiten

Geprüft wurden die Tabellenkonventionen von Oliver et al. (2024, *Sports Medicine*), Ramirez-Campillo et al. (2020, *Sports Medicine*; 2023, *Sports Medicine – Open*), Zheng et al. (2025, *PLoS One*), Moran et al. (2017, *JSCR*) und Olivier et al. (2026, *Physical Therapy in Sport*).

### 1.1 Welche Tabellentypen diese Arbeiten verwenden

| Typ | Referenz | Funktion |
|---|---|---|
| **A — Studiencharakteristika** | Zheng Tab. 3 („Summary of Study Demographics, Training Parameters, and Outcome Measures"), Moran Tab. 2, Oliver Tab. 2 | Eine Zeile je Studienarm. Wer, wie viele, wie alt, wie lange, wie oft, was gemessen. |
| **B — Methodische Qualität** | Oliver Tab. 1 (PEDro-Items 1–11 als Spalten, Total, Einstufung), Zheng Tab. 4 und 5 (PEDro + ROB-2-Domänenmatrix) | Item × Studie als Matrix, Urteil als eigene Spalte. |
| **C — Metaanalytische Ergebnisse** | **Oliver Tab. 3 — das beste Vorbild** | Zielgröße × Interventionsart mit vollständiger Unsicherheitsangabe. |
| **D — Moderator-/Subgruppenanalysen** | RC 2020 Appendix S1, Moran Tab. 4 | Moderator, Subgruppe, k, ES [KI], p, Within-I², **Between-p**. |
| **E — Programmierrahmen** | **RC 2023 Tab. 7 — für uns der direkte Bezugsrahmen** | Je Zielgröße die Dosisspanne der wirksamen Studien. |

### 1.2 Der Spaltensatz von Oliver Tab. 3 (Vorbild für unsere Ergebnistabelle)

```
Outcome measure | Training intervention | No. of studies | No. of groups (EG vs CON)
| Total sample (EG vs CON) | p value | Effect size g (95 % CI) | Effect (verbal)
| I² | χ² (p value) | Prediction interval
```

Beispielzeile im Original: `Lower body strength | PTG vs CON | 5 | 7 vs 5 | 136 vs 82 | 0.060 | 0.27 (−0.01 to 0.54) | Small | 0 % | 0.430 | −0.08 to 0.62`

Bemerkenswert: **Effektstärke, Konfidenzintervall, verbale Einstufung, Heterogenität und Prädiktionsintervall stehen nebeneinander.** Das Prädiktionsintervall ist der modernere Standard und in unseren übrigen Referenzarbeiten nicht vorhanden — es beantwortet die Frage, die uns interessiert: Was ist bei einer *neuen* Studie zu erwarten?

### 1.3 Der Spaltensatz von RC 2023 Tab. 7 (Vorbild für unsere Dosistabelle)

```
Outcome (k) | Freq | Duration | Int | BH | NTJ (jumps per week) | Tply | Comb
| RBR | RBS | RBTS | Tsurf | PO | Repl
```

Alles als Spannweiten, Zweitgrößen in Klammern (`600–1,590 (92–265)` = Gesamtsprünge und Sprünge pro Woche), Abkürzungen ausschließlich in einer Legende unter der Tabelle. **Das ist die Tabelle, in die unsere eigene Intervention als Zeile gehört** — dann liest man auf einen Blick, wo wir innerhalb oder außerhalb der wirksamen Spannen liegen.

### 1.4 Formale Konventionen, die alle fünf Arbeiten teilen

- **Keine Prosa in Zellen.** Zahlen, Spannweiten, Abkürzungen. Erläuterungen nur in der Legende.
- **k in Klammern hinter dem Zielgrößennamen**: `Change of direction speed time (4)`.
- **Spannweiten mit Halbgeviertstrich**, Zweitgröße in Klammern.
- **Effektstärke und Konfidenzintervall in einer Zelle**: `0.27 (−0.01 to 0.54)`.
- **Verbale Magnitude als eigene Spalte**, nicht als Klammerzusatz.
- **Vorzeichen bei Zeitmaßen erhalten** — negativ bedeutet Verbesserung; Konvention in der Legende festhalten.
- **Fehlende Werte einheitlich**: Zheng nutzt `/`, andere `NR`. Wir nutzen durchgängig **`n. b.`** (nicht berichtet) und unterscheiden davon **`n. a.`** (nicht anwendbar).
- **Fußnotenmarken a, b, c** für Definitionen, die eine einzelne Zelle betreffen.

### 1.5 Was in allen Referenzarbeiten fehlt und für uns Pflicht ist

Keine der fünf Arbeiten führt eine **Distanz zur eigenen Untersuchung**, weil ein Review keine eigene Studie hat. Für uns ist genau das der Zweck. Ebenso fehlt überall eine **Zitierfallen-Spalte** — bei 21 dokumentierten inneren Widersprüchen in 22 Quellen ist sie unverzichtbar.

Beides gehört in eine **eigene Tabelle**, nicht in die metaanalytischen Tabellen. Sonst verlieren diese ihre Vergleichbarkeit mit der publizierten Form.

---

## 2 Zielstruktur: sechs Tabellen

### T1 — Studiencharakteristika
Eine Zeile je Studienarm. Reine Datentypen, keine Fließtextspalten.

| Spalte | Typ | Beispiel | Fehlend |
|---|---|---|---|
| `id` | Text | `Lloyd2016` | — |
| `autor_jahr` | Text | `Lloyd et al. (2016)` | — |
| `design` | Kategorie | `RCT` · `CT` · `SR/MA` · `Beobachtung` | — |
| `land` | Text | `GB` | n. b. |
| `sportart` | Kategorie | `Fußball` · `Schulsport` · `gemischt` | — |
| `niveau_tier` | Kategorie 1–5 nach McKay | `3` | n. b. |
| `geschlecht` | Kategorie | `m` · `w` · `m+w` | — |
| `n_eg`, `n_kg` | Ganzzahl | `10` / `10` | n. b. |
| `alter_eg_m`, `alter_eg_sd` | Dezimal | `16,2` / `0,4` | n. b. |
| `reife_verfahren` | Kategorie | `Mirwald` · `Moore` · `Tanner` · `%PAH` · `chronologisch` · `n. b.` | — |
| `reife_wert` | Text | `+1,3 J. zu PHV` | n. b. |
| `dauer_wo` | Ganzzahl | `6` | — |
| `freq_pro_wo` | Dezimal | `2` | — |
| `einheiten_ges` | Ganzzahl | `12` | n. b. |
| `kontakte_min`, `kontakte_max` | Ganzzahl | `74` / `88` | n. b. |
| `kontakte_ges` | Ganzzahl | `972` | n. b. |
| `intensitaet` | Kategorie | `max` · `submax` · `gemischt` · `n. b.` | — |
| `betreuung` | Kategorie | `betreut` · `unbeaufsichtigt` | — |
| `saisonphase` | Kategorie | `In-Season` · `Pre-Season` · `Off-Season` | — |
| `additiv_substituierend` | Kategorie | `additiv` · `substituierend` · `alleinig` | — |
| `untergrund` | Text | `Rasen` | n. b. |
| `geraetefrei` | Ja/Nein | `nein` | — |
| `anteil_schnell_dvz` | Prozent | `n. b.` | n. b. |
| `anteil_vertikal` | Prozent | `n. b.` | n. b. |
| `zielgroessen` | Kürzelliste | `SPR10; SPR20; SJ; RSI` | — |
| `fassung` | Kategorie | `Verlag` · `AcceptedMs` · `AheadOfPrint` | — |
| `mdpi` | Ja/Nein | `nein` | — |

**Pflicht:** Eine Zeile `EIGENE_STUDIE` mit unseren Werten — 6 Wo, 2×/Wo, 12 Einheiten, 52–120 Kontakte, 1040 gesamt, unbeaufsichtigt, Off-Season, additiv, Rasen, gerätefrei ja, 42,3 % schneller DVZ, 57,3 % vertikal, Zielgrößen `SPR5; SPR10; SPR30; COD505; SBJ`. Nur so wird die Tabelle zum Vergleichsmaßstab.

### T2 — Effektstärken (Vorbild Oliver Tab. 3)

| Spalte | Beispiel |
|---|---|
| `zielgroesse` | `SPRINT` · `COD` · `SPRUNG_H` · `SPRUNG_V` · `KRAFT` · `VERLETZUNG` |
| `test` | `10 m` · `505 (10-m-Anlauf)` · `Standweitsprung` |
| `id` | `RC2020` |
| `vergleich` | `PJT vs. KON` · `PJT vs. Kraft` · `prä vs. post` |
| `k_studien`, `k_gruppen` | `10` / `12` |
| `n_eg`, `n_kg` | `166` / `121` |
| `metrik` | `g` · `d` · `SMD` · `RR` · `IRR` · `η²` |
| `es` | `0,60` |
| `ki_u`, `ki_o` | `0,17` / `1,04` (getrennte Spalten — Voraussetzung für Forest Plots) |
| `p` | `0,007` |
| `magnitude` | `trivial` · `klein` · `moderat` · `groß` (Skala in `magnitude_skala` benennen: Hopkins vs. Cohen — Moran und Zheng verwenden unterschiedliche) |
| `i2` | `70,1` |
| `chi2_p` | `n. b.` |
| `pi_u`, `pi_o` | `−0,24` / `1,72` |
| `art` | `meta` · `zwischen` · `innen` |
| `vorzeichen` | `neg_ist_besser` · `pos_ist_besser` |
| `dosisgematcht` | Ja/Nein — markiert die Zeilen, die unserer Dosis entsprechen |

### T3 — Moderatoren (Vorbild RC 2020 Appendix S1, Moran Tab. 4)

`id | zielgroesse | moderator | subgruppe | k | es | ki_u | ki_o | p_innen | i2_innen | p_zwischen | trifft_auf_uns_zu`

Die letzte Spalte ist der eigentliche Zweck: Für unsere Dosis sind es `< 7,5 Wochen`, `< 14,5 Einheiten` und `≤ 7 Wo und ≤ 14 Einheiten` — genau diese Zeilen tragen Kapitel 2.6.

### T4 — Methodische Qualität (Vorbild Oliver Tab. 1)

`id | instrument | item_1..item_n | gesamt | einstufung | randomisierung | verblindung_tn | verblindung_auswerter | itt | praereg | publikationsbias_test | publikationsbias_ergebnis | grade`

### T5 — Programmierrahmen (Vorbild RC 2023 Tab. 7)

Je Zielgröße eine Zeile mit den Spannweiten der wirksamen Studien, plus eine Zeile `EIGENE_STUDIE`:

`zielgroesse (k) | freq | dauer_wo | intensitaet | kontakte_ges (pro_wo) | uebungstyp | betreuung | pause_saetze_s | pause_einheiten_h | untergrund | progression | additiv_substituierend`

### T6 — Projektspezifisch (unsere Ergänzung, getrennt von T1–T5)

`id | d_pop | d_dos | d_ziel | d_summe | verwendbarkeit | zitierfalle_code | zitierfalle_schwere | kapitel`

`zitierfalle_schwere`: `kritisch` (Wert nicht zitierfähig) · `hoch` (Abstract weicht ab) · `formal` (Setzfehler).

---

## 3 Abbildungen — hier entsteht die Aussagekraft

Eine Tabelle ohne Text wird durch **Abbildungen** aussagekräftig, nicht durch mehr Spalten. Vier lohnen sich, alle direkt aus T2 und T3 berechenbar.

**A1 — Forest Plot je Zielgröße.** Studie auf der Y-Achse, ES mit Konfidenzintervall auf der X-Achse, Punktgröße nach n, Rautensymbol für gepoolte Werte, gestrichelte Nulllinie. Unsere drei Zielgrößen ergeben drei Abbildungen. Das ist die Standarddarstellung und ersetzt jeden Fließtext.

**A2 — Dosis-Wirkungs-Streudiagramm.** X-Achse Einheiten gesamt, Y-Achse Effektstärke, Punktgröße n, Farbe Zielgröße, **senkrechte Referenzlinie bei 12 Einheiten** (unsere Dosis). Damit ist die zentrale Limitation der Arbeit eine Abbildung statt eines Absatzes.

**A3 — Distanzmatrix.** Quellen × drei Distanzdimensionen als Graustufenmatrix, sortiert nach Summe. Zeigt sofort, welche Quellen tragen und welche nur Kontext sind.

**A4 — Evidenzlandkarte.** X-Achse Zielgröße, Y-Achse Populationsnähe, Blasengröße Studienzahl, Blasenfarbe mittlere Effektstärke. Macht die Korpuslücke sichtbar: kein unbeaufsichtigtes, gerätefreies Vergleichssetting.

**Gestaltung nach dvs-Richtlinien (§ 9):** Graustufen mit deutlichen Abstufungen, Rahmen, Unterschrift unterhalb, 10 pt, integrierte Legende. Keine Farbe, wenn die Abbildung in die Arbeit soll.

---

## 4 Ausgabeformate

| Format | Zweck |
|---|---|
| `.xlsx` | Arbeitsfassung, ein Blatt je Tabelle, Filter, eingefrorene Kopfzeilen |
| `.docx` + `.pdf` | Lesefassung im Hausstil (§ 13: Arial, Navy `#1F3864`, Bänder `#D6E4F0`, Zebra `#EEF3F9`), Querformat |
| `.png` (300 dpi) | die vier Abbildungen, Graustufen |
| Manuskriptauszug | T2 und T5 gefiltert auf `d_summe ≤ 3`, im dvs-Tabellenformat (§ 9: „Tab. X." kursiv oberhalb, Kopfzeile 15 % grau und fett, 10 pt, Dezimalausrichtung) — das wird Tab. 2 in Kapitel 2.5 |

---

## 5 Architektur

```
evidenztabelle/
  daten/          T1..T6 als CSV — einzige Quelle der Wahrheit, von Hand pflegbar
  render/         tabellen.py · abbildungen.py · hausstil.py
  pruefung/       validate.py — Konsistenzprüfungen
  ausgabe/        xlsx, docx, pdf, png
```

**Trennung von Daten und Darstellung ist die wichtigste Entscheidung.** Neue Quellen kommen als CSV-Zeile dazu, das Rendern bleibt unverändert. Ohne diese Trennung wird jede Erweiterung wieder ein Codier-Projekt.

### Verpflichtende Konsistenzprüfungen in `validate.py`

1. Jede `id` in T2–T6 existiert in T1.
2. `ki_u < es < ki_o` für jede Zeile mit vollständigem Konfidenzintervall.
3. `pi_u ≤ ki_u` und `pi_o ≥ ki_o`, wo beide vorhanden sind.
4. `0 ≤ i2 ≤ 100`.
5. `d_summe = d_pop + d_dos + d_ziel`.
6. Bei `vorzeichen = neg_ist_besser` ist ein positiver Wert ein Warnhinweis.
7. Jede Zeile mit `zitierfalle_schwere = kritisch` wird in der Ausgabe sichtbar markiert.
8. Fehlende Werte ausschließlich als `n. b.` oder `n. a.`, nie als leere Zelle oder `0`.

---

## 6 Bekannte Lücken in den vorhandenen Daten

Diese Felder sind derzeit `n. b.` und lassen sich **nur durch erneute Volltextprüfung** füllen — nicht durch Schätzung:

- `kontakte_ges` bei RC 2020, Zheng 2025, Moran 2017, Oliver 2024, Liu 2024, Aloui 2022, Hammami 2016 (Aloui und Hammami: aus den Progressionstabellen rekonstruierbar, aber im Text nicht ausgewiesen)
- `anteil_schnell_dvz` und `anteil_vertikal` bei allen Quellen außer der eigenen Studie — keine Arbeit berichtet die Zusammensetzung ihres Übungskatalogs quantitativ. **Das ist selbst ein Befund** und gehört in 5.5.
- `pi_u`, `pi_o` nur bei Oliver 2024 vorhanden
- `i2` bei Zheng 2025 für keine Zielgröße numerisch berichtet
- `niveau_tier` bei den meisten Quellen nicht nach McKay klassifiziert

---

## 7 Was der Codier-Task NICHT tun soll

- Keine Zahl aus einem Abstract übernehmen.
- Keine fehlenden Werte interpolieren, mitteln oder aus verwandten Studien übertragen.
- Keine eigenen Effektstärken aus Prä-Post-Mittelwerten berechnen, ohne dass die Quelle sie selbst so ausweist.
- Keine gepoolten Werte über Quellen hinweg rechnen — wir führen keine eigene Metaanalyse durch; das wäre eine andere Arbeit und methodisch nicht abgesichert.
- Die Interpretationsspalten aus T5 der bisherigen Fassung (`tragfaehige_formulierung`, `staerkster_gegenbefund`) nicht in die metaanalytischen Tabellen mischen — sie bleiben ein eigenes Dokument.

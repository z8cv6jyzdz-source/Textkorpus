# Raster Literaturanalyse 2.4 „Zielgrößen und ihre Diagnostik“ (27.09.2026)

## Kontext
Bachelorarbeit (DSHS Köln), quasi-experimentelle kontrollierte Studie: sechswöchiges videobasiertes, gerätefreies plyometrisches Heimtraining in der Sommerpause, männliche U15-Fußballer (Leistungsniveau Tier 2). Zielgrößen: Sprint 5/10/30 m (Lichtschranken), Richtungswechsel 505-Test (Mittel beider Seiten), Standweitsprung. Kapitel 2 der Arbeit („Theoretischer Hintergrund und Forschungsstand“) hat einen Abschnitt 2.4 „Zielgrößen und ihre Diagnostik“. Zeitschriftenartikel haben kein eigenes Theoriekapitel.
Frage: WO und WIE führen Studien ihre Zielgrößen und deren Diagnostik ein, WOMIT begründen sie die Wahl, und WIE UMFANGREICH ist das im Verhältnis zum Gesamttext?

## Arbeitsweise
- Texte: `/home/claude/txt/<Datei>.txt` (Lesereihenfolge) und `<Datei>.layout.txt` (layouttreu, hilft bei zweispaltigem Satz und Seitenzahlen). Lies jeden Artikel vollständig bis zum Beginn der Literaturliste. Nur, was im Text steht, keine Vermutungen, keine Web-Suche, keine anderen Dateien ändern.
- Wörter zählen ausschließlich mit `python3 /home/claude/werkzeug/zaehle.py` (Doku im Dateikopf): Abschnitte mit `span DATEI "Startmarke" "Endmarke"` (Marken 5–12 Wörter wörtlich aus der .txt, bei Kurzwörtern wie „Methods“ immer mehrere Wörter nehmen, das Ergebnis „Anfang/Ende“ kontrollieren), Einzelsätze mit `text "…"`. Für alle Anteile den Wert „absatz“ verwenden.
- Seiten: gedruckte Seitenzahl aus Kopf-/Fußzeile oder Zeitschriftenpaginierung („S. 625“). Wenn keine erkennbar: „PDF-S. n“ (`seite`).
- Zitate: wörtlich, höchstens 25 Wörter, aus dem Haupttext (nicht aus dem Abstract).
- Arbeite zügig und ohne Rückfragen. Nicht bestimmbar → null und Grund in der Antwort.

## Ausgabe je Studie (ein JSON-Objekt, Feldnamen genau so)
```
{
 "id": "Nachname Jahr",
 "datei": "<Dateiname ohne .txt>",
 "typ": "<siehe Typen>",
 "population": "Alter, Geschlecht, Niveau, Sportart (kurz)",
 "zielgroessen": "Tests/Strecken kurz",
 "woerter_haupttext": <absatz-Wert: erstes Wort der Einleitung bis letztes Wort vor der Literaturliste, ohne Abstract, Praxisrubrik/Fazit eingeschlossen>,
 "gliederung": ["Überschrift Ebene 1 > Ebene 2", "..."],
 "zg_abschnitt": {
   "eigener_abschnitt": "ja" | "nein" | "teilweise",
   "ort": "Einleitung" | "Methodik" | "Diskussion" | "eigenes Kapitel" | "mehrere: …",
   "titel": ["wörtliche Überschrift(en)"],
   "titel_hinweis": "inhaltlich vergleichbar, aber anders betitelt: wie genau; sonst leer",
   "woerter": <absatz-Wert, Summe der Abschnitte ohne Überschriften>,
   "anteil_prozent": <woerter / woerter_haupttext * 100, eine Nachkommastelle>,
   "inhalt": ["aus: Konstruktdefinition, Relevanzbegründung, Begründung der Testwahl, Protokoll/Ablauf, Gerät, Versuche/Pausen, Aggregationsregel, Reliabilität (zitiert), Reliabilität (eigene Daten), Validität, Normwerte, Standardisierung/Aufwärmen, Testreihenfolge, Sonstiges: …"],
   "ziel": "ein Satz: Welche Funktion erfüllt der Abschnitt im Text?"
 },
 "einleitung": {
   "woerter": <absatz-Wert der Einleitung>,
   "absaetze": [{"nr": 1, "thema": "<Thema>", "woerter": n}],
   "zg_woerter": <Summe der Wörter aller Einleitungssätze, deren Gegenstand die Zielgrößen oder ihre Diagnostik sind: Relevanz, Definition, Messung — nicht Sätze über Trainingseffekte oder Mechanismen der Trainingsmethode>,
   "kette": [{"zug": "Z1…Z10", "beleg": "B1…B13 oder ohne", "quellenart": "Review/MA | Primärstudie | Positionspapier/Lehrbuch | ohne Beleg", "zitat": "…", "seite": "S. x"}]
 },
 "methodik_belege": [{"beleg": "B5", "test": "505", "quellenart": "…", "zitat": "…", "seite": "…"}],
 "diskussion": {"relevanzsatz_je_zielgroesse": "ja | nein | teilweise", "beispiel": "…", "seite": "…"},
 "fuer_2_4": "höchstens 40 Wörter: was für die Formulierung von 2.4 nützlich ist (gute Kette, Definition, Beleg, Warnung) oder leer"
}
```
- `einleitung.absaetze[].thema` aus: Anforderung/Leistungsrelevanz der Zielgrößen · Konstrukt/Diagnostik · Mechanismus/Trainingsmethode · Reifung/Alter · Saisonphase/Detraining · Interventionsevidenz · Lücke · Zweck/Hypothese · Sonstiges. Ein Absatz mit mehreren Themen: das überwiegende nehmen.
- `einleitung.kette`: nur Sätze, die Zielgrößen oder Diagnostik betreffen, in Textreihenfolge (Züge Z1–Z10). Bei langen Einleitungen je Zug höchstens zwei Einträge.
- `methodik_belege`: jede Begründung eines Tests oder einer Zielgröße im Methodenteil (Reliabilität, Validität, Protokollherkunft, Verbreitung, Praktikabilität …), je Test höchstens zwei Einträge.

## Züge (Z) — Funktion des Satzes bei der Einführung der Zielgrößen/Diagnostik
- Z1 Sport-/Spielanforderung (Häufigkeit, Umfang, Bedeutung von Sprints, Richtungswechseln, Sprüngen im Spiel)
- Z2 Leistungs-/Erfolgsrelevanz (Fähigkeit trennt Leistungsniveaus, entscheidet Spielsituationen, Talent/Selektion, Zusammenhang mit Spielleistung)
- Z3 Konstruktdefinition/-abgrenzung (was die Fähigkeit ist, Teilkomponenten wie Beschleunigung/Maximalgeschwindigkeit, COD vs. Agilität, Schnellkraft)
- Z4 Determinanten/Mechanismus der Fähigkeit (Kraft, DVZ/SSC, Technik)
- Z5 Trainierbarkeit/Interventionsevidenz (Fähigkeit reagiert auf Training)
- Z6 Testwahl/Operationalisierung (welcher Test erfasst die Fähigkeit und warum)
- Z7 Messgüte (Reliabilität, Validität, Sensitivität, Messfehler)
- Z8 Moderator/Kontext der Zielgröße (Alter, Reife, Saisonphase, Verletzung)
- Z9 Lücke (bezogen auf Zielgröße oder Diagnostik)
- Z10 Zweck/Hypothese mit Nennung der Zielgrößen

## Belegverfahren (B) — womit die Wahl einer Zielgröße oder eines Tests gerechtfertigt wird
- B1 Spielanforderung (Zeit-Bewegungs-Analysen, Häufigkeiten, Torsituationen)
- B2 Leistungsrelevanz/Trennschärfe (Unterschiede zwischen Leistungsniveaus, Selektion, Korrelation mit Spielleistung)
- B3 Mechanistische Nähe zur Intervention (Spezifität, DVZ/SSC, Kraftübertragung)
- B4 Trainierbarkeit/Sensitivität (frühere Interventionsbefunde an dieser Zielgröße)
- B5 Reliabilität (ICC, CV, TE; zitiert oder eigene Daten)
- B6 Validität (Konstrukt-, Kriteriums-, Diskriminanzvalidität)
- B7 Konvention/Verbreitung („commonly used“, „widely used“, Standardtest, Testbatterie)
- B8 Protokollherkunft („as previously described“, Verweis auf Originalprotokoll)
- B9 Konstruktdefinition/-abgrenzung als Begründung
- B10 Praktikabilität/Feldtauglichkeit/Sicherheit/Kosten
- B11 Normwerte/Vergleichbarkeit mit Literatur
- B12 Verletzungsprävention/Gesundheit
- B13 Sonstiges (benennen)

## Typen
„Intervention (randomisiert)“ · „Intervention (nicht randomisiert/kontrolliert)“ · „Detraining/Beobachtung (Längsschnitt)“ · „SR/MA“ · „Systematische Übersicht ohne MA“ · „Narrative Übersicht/Positionspapier“ · „Reliabilität/Validität“ · „Normwerte/Trends“ · „Spielanalyse/Querschnitt“ · „Biomechanik/Querschnitt“ · „Praxisbeitrag“

## Typspezifische Hinweise
- **Interventions- und Detrainingstudien:** `zg_abschnitt` = die Testabschnitte der Methodik („Testing procedures“, „Measurements“, „Physical fitness assessment“, „Outcome measures“, einzelne Testüberschriften …), Summe aller Unterabschnitte, die Tests beschreiben — ohne Stichprobe, Design, Intervention, Statistik. Einleitung vollständig nach `absaetze` aufschlüsseln.
- **SR/MA und systematische Übersichten:** `zg_abschnitt` = Abschnitte der Methodik, die die Zielgrößen festlegen („Types of outcome measures“, „Outcomes“, Outcome-Kriterium im PICO, Kategorisierung der Zielgrößen). Nur eine Zeile im PICO → `teilweise`, Wörter entsprechend klein.
- **Reliabilität/Validität/Normwerte:** Die ganze Studie handelt von Diagnostik. `zg_abschnitt` = Testbeschreibungen der Methodik. Entscheidend ist die Einleitung: Wie wird begründet, warum die Fähigkeit/der Test wichtig ist und warum Gütedaten nötig sind (Kette vollständig).
- **Spielanalysen, narrative Übersichten, Praxisbeiträge:** `zg_abschnitt` = Abschnitte, die Leistungsvoraussetzungen, Zielgrößen oder Testverfahren behandeln (z. B. „Physical demands“, „Testing“, „Assessment“), falls vorhanden. Kette: Wie werden Sprint, Richtungswechsel, Sprung als relevant eingeführt?

## Abgabe
1. JSON-Liste aller Studien deiner Gruppe nach `/home/claude/ergebnisse/<Gruppe>.json` (UTF-8, `ensure_ascii=False`), Gültigkeit mit `python3 -m json.tool` prüfen.
2. Antwort an mich, höchstens 200 Wörter: (1) bearbeitete IDs, (2) auffällige Muster deiner Gruppe (typische Kette, anders betitelte Abschnitte, typische Belegverfahren), (3) Probleme (Extraktion, Duplikate, Zweifelsfälle). JSON-Inhalte nicht wiederholen.

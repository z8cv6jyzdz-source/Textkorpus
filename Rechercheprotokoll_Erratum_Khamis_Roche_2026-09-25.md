# Rechercheprotokoll — Erratum zu Khamis und Roche (1994), Versuch über PubMed und Crossref (Maßnahme L12)

**Datum:** 25.09.2026, 14:45 MESZ · **Auftrag:** Schritt 6 des Tasks „Phase 6 abschließen und Phase 7“ (Verfasser, 25.09.): „Erratum Khamis & Roche über PubMed und Crossref versuchen.“ · **Werkzeuge:** PubMed (E-utilities über den Projektanschluss), Crossref REST API, Unpaywall REST API, Europe PMC REST API (Abfrage vom Proxy abgewiesen, siehe unten).

## 1 Gegenstand

Der Reifestatus (%PAH) wird nach Khamis und Roche (1994) berechnet, Tab. 1 „White Males“ unverändert, lineare Interpolation der Koeffizienten (Spezifikation S05, O1, O2, Anlage `Spezifikation_2026-09-24_Koeffizienten_KR.csv`, 28 Alterszeilen). Zu dem Artikel ist ein Erratum bekannt (Pediatrics, 1995, Band 95, Heft 3, S. 457, doi 10.1542/peds.95.3.457). Es liegt nicht vor und wurde in der Rechnung nicht verwendet. Die Maßnahme L12 verlangt, es zu beschaffen und gegen die verwendeten Koeffizientenzeilen zu prüfen. Phase 4 (Blindrechnung) und Phase 7.1 (Kennzahlenblatt) sind gelaufen, ohne dass das Erratum vorlag.

## 2 Ergebnis je Quelle

| Quelle | Abfrage | Befund |
|---|---|---|
| PubMed | `Khamis HJ[Author] AND Roche AF[Author] AND Pediatrics[Journal]` | Ein Treffer, der Originalartikel: Khamis, H. J., & Roche, A. F. (1994). Predicting adult stature without using skeletal age: the Khamis-Roche method. *Pediatrics, 94*(4 Pt 1), 504–507. PMID 7936860. Kein eigener Datensatz für das Erratum, kein PMC-Volltext. |
| PubMed | Zitationsabgleich Pediatrics 1995, Band 95, S. 457 (mit und ohne Autor Khamis) | Nicht gefunden. |
| PubMed | `Khamis-Roche method erratum` · `Pediatrics[Journal] AND 1995[pdat] AND 95[Volume] AND 457[Page]` | Keine Treffer. PubMed führt das Erratum nicht als eigenen Eintrag. |
| Crossref | `works/10.1542/peds.95.3.457` | Eintrag vorhanden: Typ journal-article, Titel „ERRATUM“, *Pediatrics* 95(3), S. 457, erschienen 01.03.1995, Verlag American Academy of Pediatrics, ISSN 0031-4005 und 1098-4275, ohne Autorenfeld, ohne „update-to“-Relation. Der hinterlegte Abstract lautet: „In the article entitled ‘Predicting Adult Stature Without Using Skeletal Age: The Khamis-Roche Method’ authored by Harry J. Khamis, PhD and Alex F. Roche, MD, PhD, DSc, which appeared in the October 1994 issue of Pediatrics, there were some errors in Tables 1 and 2. The corrected version of Tables 1 and 2 appears below.“ Volltextlinks: `https://publications.aap.org/pediatrics/article/95/3/457/59792/ERRATUM` und `…/article-pdf/95/3/457/983170/457.pdf`. |
| Verlagsseite (AAP) | Artikelseite und PDF-Link | Beide Abrufe mit HTTP 403 abgewiesen (Zugriff nur mit Lizenz). |
| Unpaywall | `v2/10.1542/peds.95.3.457` | is_oa false, oa_status „closed“, keine frei zugängliche Kopie. |
| Europe PMC | `search?query=DOI:10.1542/peds.95.3.457` | Abfrage vom Netzwerk-Proxy mit HTTP 429 abgewiesen, nicht wiederholt. Kein Befund. |

## 3 Bewertung

1. Das Erratum existiert und ist bibliografisch gesichert (Crossref). Es korrigiert nach eigenem Wortlaut „Tables 1 and 2“ des Artikels von 1994. Tab. 1 ist die Koeffiziententabelle, aus der die Spezifikation die Zeilen für männliche Spieler entnimmt. Welche Zeilen oder Werte betroffen sind, ergibt sich erst aus dem Volltext.
2. Der Volltext ist über PubMed, Crossref, Unpaywall und den Verlag ohne Lizenz nicht zu erhalten. Der Beschaffungsweg bleibt die Bibliothek der DSHS (Zeitschriftenzugang der AAP oder Fernleihe), wie in F14 § 6.5 vorgesehen.
3. Bis der Volltext vorliegt, gilt die Verfasserentscheidung vom 24.09. (O1: Tab. 1 von 1994 unverändert). Das Kennzahlenblatt vom 25.09. beruht auf diesen Koeffizienten. Betrifft das Erratum verwendete Zeilen, folgt der in L12 festgelegte Weg: datierter Nachtrag zur Spezifikation, neuer Lauf beider Ketten, Wiederholung von 6.1 und 7.1 bis 7.3, Korrektur mit altem und neuem Ergebnis im Register wie R11.
4. Im Manuskript (4.3 und 4.7) ist bis dahin zu berichten, dass die Koeffizienten der Originalpublikation verwendet wurden und das Erratum nicht vorlag. Das ist eine Einschränkung, keine Abweichung vom Antrag.

## 4 Literaturangaben (verifiziert an den Datenbankeinträgen, nicht am Volltext des Erratums)

- Khamis, H. J., & Roche, A. F. (1994). Predicting adult stature without using skeletal age: The Khamis-Roche method. *Pediatrics, 94*(4), 504–507. PMID 7936860 (PubMed, 25.09.2026).
- Erratum. (1995). *Pediatrics, 95*(3), 457. https://doi.org/10.1542/peds.95.3.457 (Crossref, 25.09.2026). Nicht eingesehen.

Quellenangaben nach PubMed: Originalartikel PMID 7936860 (kein DOI im PubMed-Eintrag hinterlegt). Nach Crossref: Erratum [DOI 10.1542/peds.95.3.457](https://doi.org/10.1542/peds.95.3.457).

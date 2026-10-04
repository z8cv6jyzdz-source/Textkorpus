# -*- coding: utf-8 -*-
"""
Steuerung_Rev92_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 92) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln

Zweck: Die Verfasserentscheidungen vom 25.09.2026 (nachmittags) in die beiden Steuerdokumente eintragen:
Papierkorb-Skript, Sammelordner 06_Abbildungen, Platzhalter-Regel für Grafiken, vier angefragte Vereine
(K-01.24, Abb. 1), Abb. H7, L12 abgeschlossen (Erratum nicht beschaffbar, R14), A8 erledigt, Handprobe
Fassung 2 committet. Jede Textstelle wird genau einmal ersetzt, sonst bricht das Skript ab. Ohne Semikolon.
Aufruf: python Steuerung_Rev92_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md> <Ordner_aufraeumen.ps1>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

SN, ML, PS1 = sys.argv[1], sys.argv[2], sys.argv[3]
ps1 = open(PS1, encoding='utf-8-sig').read()
block = ps1.split('$papierkorbListe = @(')[1].split('\n)')[0]
N_PAPIERKORB = len([l for l in block.split('\n') if l.strip().startswith("'")])
if chr(59) in ps1:
    raise SystemExit('Semikolon im PowerShell-Skript')


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 91 — siehe Block oben.) Zuvor: (Rev. 90 — siehe Block oben.)',
            '**Stand: (Rev. 92 — siehe Block oben.) Zuvor: (Rev. 91 — siehe Block oben.) Zuvor: (Rev. 90 — siehe Block oben.)')

REV92 = '''### ⭐ NEU (Rev. 92, 25.09.2026, 16:35 MESZ): Verfasserentscheidungen nach Phase 7 — Papierkorb-Skript, Sammelordner `06_Abbildungen`, Platzhalter-Regel für Grafiken, vier angefragte Vereine (K-01.24, Abb. 1), Abb. H7, Erratum nicht beschaffbar (L12 geschlossen, R14), A8 erledigt, Handprobe Fassung 2 committet

**Anlass (Verfasser, 25.09., nachmittags, eine Nachricht):** Excel geschlossen · alle nicht mehr gebrauchten Dokumente in einen Ordner „Papierkorb“ führen, damit sie gesammelt gelöscht werden können · das Erratum zu Khamis und Roche wird nie vorliegen (nur über die Bibliothek), gearbeitet wird mit dem, was vorliegt · es waren vier angefragte Vereine · Fassung 14 steht bereits in den Projektanweisungen · Abbildungen und Grafiken gesammelt in einem Ordner zusammenführen · im Master zunächst mit Platzhaltern arbeiten, Grafiken erst am Ende einfügen, wenn der Großteil des Textes steht und feststeht, welche Grafiken wirklich gebraucht werden · Frage nach den weiteren Schritten. Alles umgesetzt, Details:

**(1) Handprobe Fassung 2 auf dem Rechner.** `04_Uebergaben\\Handprobe_2026-09-25.xlsx` (Fassung 2, 299 675 Byte, volle Neuberechnung beim Öffnen) ist committet. Der Vorbehalt aus Rev. 91 Nr. 1 ist erledigt. Der Verfasser trägt sein Urteil in Zelle B4 ein (R12).

**(2) Papierkorb statt Archiv (neuer Verfasserweg).** Cowork kann weder verschieben noch löschen, deshalb `Claude\\Ordner_aufraeumen.ps1` in neuer Fassung (Stand 25.09. nachmittags, UTF-8 mit BOM, CRLF, ohne Semikolon, Vorgängerfassung in `_Archiv\\_ersetzt_2026-09-25_Hauptordner`). Das Skript legt `Bachelorarbeit\\Papierkorb` neben `Claude` an, verschiebt %d Einträge (Dateien und ganze Ordner) mit ihrem bisherigen relativen Pfad dorthin, sortiert lose Dateien im Hauptordner `Claude` nach der Ordnerkonvention ein und schreibt ein Protokoll (`Papierkorb\\Papierkorb_Protokoll_⟨Datum⟩.txt`, Kopie in `_Archiv`). Es löscht nichts, ist wiederholbar und kennt `-WhatIf` als Probelauf. Aufruf in PowerShell im Ordner `Claude`: `powershell -ExecutionPolicy Bypass -File .\\Ordner_aufraeumen.ps1 -WhatIf`, dann ohne `-WhatIf`, danach Papierkorb durchsehen und löschen. Liste (Skript Abschnitt 2): Projektanweisungen F10 bis F12 · Kennzahlenblätter 15.09. und 22.09. mit Erzeugern · Berichtsraster_und_Wortbudget 13.09. · Analyseprotokoll 12.09. · SPSS-Vorgehen und SPSS-Syntax · drei einmalige Hilfsskripte · fünf erledigte oder doppelte Übergaben · Transferprobe · die Ordner `Claude outputs`, `Statistik\\Claude outputs`, `Statistik\\Fragebogen Auswertung`, `Auswertung` (Darstellungspipeline) und `Dashboard` (mit `daten\\`, L21) · `Statistik\\RCT_Auswertungspraxis_2026-09-11.docx` (Doppelablage) · `Daten\\Datenerfassung_Praetest_U15_1.xlsx` und das alte Prä-Daten-Dashboard · in `Schreiben\\` die alte Manuskriptfassung `_ALT`, Auswertungs-und-Darstellungskonzept, Evidenztabelle v2 (.pdf und .docx), Literaturübersicht v2, zwei alte Gliederungen (darunter die Rev.-1-Kopie der Gliederung v4), die Bauplan-Kopie und der Manuskriptstand vom 13.09. · die Doppelablage der CONSORT-Auswertung im Hauptordner · zwei Installationsdateien aus `Ideen und Studien` (G26h). **Vorher gerettet und abgelegt:** `Auswertung\\ancova_ergebnisse.csv` → `03_Skripte\\Auswertung_B7_ANCOVA_2026-09-12_ancova_ergebnisse.csv` (L21), `Fragebogen_A_aufbereitet_2026-09-12.xlsx` → `03_Skripte\\Auswertung_F1_Fragebogen_2026-09-12_aufbereitet.xlsx`, `A1_Titelscreening_2026-09-11.md` → `05_Protokolle\\`, die Forest-Plots und Landkarten der Evidenztabelle → `06_Abbildungen\\Kandidaten_Evidenztabelle`. **Nicht im Papierkorb:** `_Archiv` (Belegkette), Blindordner, Datenstand, Workbook, Papierbögen in `Daten\\`, Literatur, Master, `Schreiben\\BA-Arbeit Sicherheit`, die `Evidenztabelle\\`-Pipeline, die Übergaben Datensicherung und Blindrechnung (Prompt-Belege für die KI-Deklaration), die offenen Übergaben 4.3, 4.4, 4.5.1 und 4.6 samt Textvorschlägen, `Belegpruefung_2026-09-24.xlsx`. `Ideen und Studien\\1.Hilfe und DLRG_Silber KLIER.pdf` ist kein Projektdokument und bleibt liegen, der Verfasser legt es selbst außerhalb ab. `README_Ordnerstruktur.md` neu gefasst (Stand 25.09. nachmittags, mit `06_Abbildungen`, Papierkorb-Anleitung und Standübersicht).

**(3) Erratum Khamis und Roche — L12 geschlossen, R14.** Verfasserentscheidung 25.09.: Das Erratum wird nicht beschafft, gearbeitet wird mit dem vorliegenden Stand. O1 und O2 (Tab. 1 der Originalpublikation 1994, lineare Interpolation) sind endgültig, der Vorbehalt „bei einem Treffer beide Ketten wiederholen“ entfällt. Eingetragen als **R14** im Register (`03_Skripte\\Auswertungsplan_Register_R14_2026-09-25.py`, Auswertungsplan .md/.docx/.pdf neu gesetzt). Im Manuskript bleibt die Einschränkung in 4.3 und 4.7 (Koeffizienten der Originalpublikation, Erratum nicht eingesehen, Richtung eines etwaigen Fehlers unbekannt) und in 6.3 unter G2. Die Beschaffungsposten zum Erratum in F14 § 6.5 und § 7.1 sind damit gegenstandslos, F14 wird deswegen nicht neu gefasst (Entscheidung steht hier und im Register).

**(4) Vier angefragte Vereine — K-01.24 und Abb. 1.** Angabe des Verfassers 25.09.: vier Vereine angefragt, drei Zusagen (A, B, C), einer ohne Zusage. Aufgenommen als neue Zeile **K-01.24** im Kennzahlenblatt (`Kennzahlen_2026-09-25.py` Rev. 2, Kopfzeile mit Rev.-Vermerk, Anlage jetzt 216 Zeilen, Quelle „nicht aus der Ergebnisdatei“, Bezugsmenge angefragte Vereine). Das Blatt vom 25.09. ist in Rev. 2 an Ort und Stelle ersetzt, die Änderung ist rein additiv (Diff: eine Zeile in `_Werte.csv`, eine Zeile und der Kopfvermerk in `.md`, keine Kennung geändert), deshalb keine eigene Archivkopie von Rev. 1. `Objekte_2026-09-25.R` Fassung 2 trägt `ANGEFRAGT <- 4L` und `ZUGESAGT <- 3L` und beschriftet den Clusterkasten von Abb. 1 mit „angefragt n = 4, ohne Zusage n = 1, Zusagen 3 Vereine (A, B, C), Zuteilung auf Vereinsebene vor der Eingangstestung“. Der Endabgleich 7.3 lief mit Rev. 2 erneut, Ergebnis unverändert (835 Zahlen, 29 Satzprüfungen, 4 Abweichungen, 7 Vorschläge, Master unverändert), Protokoll neu gesetzt.

**(5) Abb. H7 Zeitstrahl neu im R-Skript.** Eingangs- und Abschlusstestung je Verein (Quadrat und Kreis), Programmzeitraum 20.07. bis 30.08. als Balken bei den IG-Vereinen, Prä-Post-Intervall in Wochen am Zeilenende (A 10,0, B 7,0, C 9,0), Graustufen, 16 × 5,5 cm, PNG 300 dpi und PDF. Termine aus K-03 des Datenstands, Familiarisierungstermine liegen nicht als Datum vor (steht in der Bildunterschrift). Damit erzeugt das Skript alle drei Abbildungen des Objektkatalogs (Abb. 1, Abb. 2, Abb. H7). Synthetische Probe erneut gelaufen.

**(6) Sammelordner `Claude\\06_Abbildungen` (neuer Unterordner, vom Verfasser angeordnet).** Inhalt: `Abb_1_Teilnehmerfluss`, `Abb_2_Modell`, `Abb_H7_Zeitstrahl` (je .png und .pdf, Kopien der Skriptausgabe) · `Anhang_G\\` mit den sechs Q-Q- und Linearitätsdiagrammen der berichteten Rechnung (Kopien aus der Abgabe der zweiten Instanz ohne Transferblock) · `Kandidaten_Evidenztabelle\\` mit sieben Grafiken der Evidenztabellen-Pipeline vom 27.08. (in der Objektpolitik nicht vorgesehen, nur für die Entscheidung am Ende) · `README_Abbildungen.md` mit Objekt, Ort, Erzeuger, Datenquelle und Stand je Datei. Regel: Jede Grafik ist Skriptausgabe, bei neuem Lauf wird die Datei ersetzt, nie von Hand geändert (R7). Die Tabellen bleiben in `03_Skripte\\Objekte_2026-09-25\\` (CSV und `Objekte_2026-09-25.docx`).

**(7) Verfasserfestlegung „Grafiken erst am Ende“.** Im Master stehen bis auf Weiteres Platzhalter (⟨Abb. X hier einfügen⟩ mit Bildunterschrift), keine eingebetteten Grafiken. Eingefügt wird erst, wenn der Großteil des Textes steht und feststeht, welche Grafiken wirklich gebraucht werden. Die Objektverweise im Text werden trotzdem gesetzt und am Ende einzeln gegen das Objekt geprüft (F14 § 5.3). Die Textvorschläge für 5.1 und 5.2 nennen deshalb Abb. 1 und Abb. 2 mit Platzhalter, die Seitenprognose (R6) wird mit dem Platzhalter-Umfang der Objekte (rund 0,4 Seiten je Objekt) gerechnet.

**(8) A8 erledigt.** Fassung 14 steht laut Verfasser in den Projekteinstellungen. F10 bis F12 gehen per Skript in den Papierkorb, `00_Steuerung` enthält danach genau drei Dateien.

**Regeln eingehalten:** Papierkorb-Skript, R-Skript Fassung 2, Kennzahlen-Skript Rev. 2, Register-Skript und dieses Skript ohne Semikolon, Ergebniswerte nur in Dateien, keine Zahl von Hand (K-01.24 ist eine Verfasserangabe, als solche gekennzeichnet). Blindordner, Abgabe der zweiten Instanz, Datenstand, Workbook und Master unverändert.

**Dateien (Ordner):** `Claude\\Ordner_aufraeumen.ps1` (neu gefasst), `Claude\\README_Ordnerstruktur.md` (neu gefasst) · `02_Befunde\\` Kennzahlen_2026-09-25.md + _Werte.csv (Rev. 2), Abgleichprotokoll_Manuskript_2026-09-25 (.md/.docx/.pdf, zweiter Lauf), Auswertungsplan_2026-09-12 (.md/.docx/.pdf, R14) · `03_Skripte\\` Kennzahlen_2026-09-25.py/.txt (Rev. 2), Objekte_2026-09-25.R (Fassung 2), Objekte_2026-09-25\\ (28 Dateien, mit Abb_H7), Objekte_2026-09-25_synthetisch\\ (29), Endabgleich_Manuskript_2026-09-25.txt/_Zahlen.csv (zweiter Lauf), Auswertungsplan_Register_R14_2026-09-25.py, Steuerung_Rev92_2026-09-25.py, Auswertung_B7_ANCOVA_2026-09-12_ancova_ergebnisse.csv, Auswertung_F1_Fragebogen_2026-09-12_aufbereitet.xlsx · `04_Uebergaben\\` Handprobe_2026-09-25.xlsx (Fassung 2) · `05_Protokolle\\` A1_Titelscreening_2026-09-11.md · `06_Abbildungen\\` (20 Dateien) · `_Archiv\\_ersetzt_2026-09-25_Hauptordner\\` (Skript und README vom 24.09.). Projektkopien der .md-Dateien unter `claude/`.

**Projektspeicher (Nachtrag 16:55 MESZ):** Der Projektspeicher war mit 1,93 von 2,00 MB voll, die Projektkopie der Sitzungsnotizen ließ sich nicht auf Rev. 92 bringen. Der Verfasser hat die Löschung überholter Projektdokumente freigegeben (Gegenstück zum Papierkorb, Freigabe per Chat 25.09.). Gelöscht wurden 26 Dokumente: `claude/Projektanweisungen_Fassung5` bis `Fassung13`, `Kennzahlen_2026-09-15.md`, `Kennzahlen_2026-09-22.md` und `.py`, `Analyseprotokoll_2026-09-12.md`, `Berichtsraster_und_Wortbudget_2026-09-13.md`, die Übergaben Spezifikation (24.09.), 4.1 (12.09.), 4.2 (14.09.), Fragebogenauswertung, RCT-Auswertungspraxis und 4.7, `Naechste_Schritte_2026-09-06.md`, `Gliederung_v3_Umnummerierung_2026-09-06.md`, `Bestandsaufnahme_Projekt_2026-09-01.md`, `Gliederung_Bachelorarbeit_v2.docx`, `Literaturübersicht.docx`, `Auswertungs-und-Darstellungskonzept.docx`. Die Ordnerfassungen bleiben (Papierkorb oder `_Archiv`). Danach Projektkopie der Sitzungsnotizen auf Rev. 92 geschrieben.

**Nächste Schritte (Reihenfolge fest, Antwort auf die Frage des Verfassers):** (1) Verfasser: `Ordner_aufraeumen.ps1` mit `-WhatIf`, dann echt, Papierkorb durchsehen und löschen · (2) Verfasser: Handprobe in Excel prüfen, Urteil in B4 · (3) Verfasser: **Vorschlagsliste 1 bis 7** des Abgleichprotokolls je Abschnitt freigeben und in den Master übertragen (Kennung neben der Zahl, Tab. 1 aus `Objekte_2026-09-25.docx`), danach Claude: `Endabgleich_Manuskript_2026-09-25.py` erneut · (4) **Freigabe F3** (Übertrag in das Manuskript, Auswertungsverfahren Phase 7) · (5) Task „4.7 Statistische Auswertung“ nach Berichtsraster (Budget 550, Zeilen 4.7.1 bis 4.7.13, R1 bis R14 als nachträgliche Festlegungen, Einschränkungen F1 ohne unabhängige Prüfung und Erratum nicht eingesehen, R-Zitat aus `citation()` der Abgabe) · (6) Task „Kapitel 5“ (5.1 mit Abb. 1 als Platzhalter und Tab. 2, Tab. H2 im Anhang, 5.2 mit Abb. 2 als Platzhalter und Tab. 3, Schlusslogik Fall C1 je Zielgröße, Budget 450) · (7) Kapitel 6 und 7, danach Kürzung Kapitel 2 und Kapitel 1, 2.5, 3 · (8) Phase 8 (L9): KI-Deklaration, Anhang G, Reproduktionstest · (9) am Ende: Grafiken einsetzen, Objektverweise prüfen, Word-Seitenmessung (R6), Verzeichnisse F9. Beim Betreuer offen bleibt nur die Fußnotenfrage (§ 8, § 13).

**Maßnahmenliste:** A8 erledigt, L12 erledigt (entschieden, R14), L19 Rest erledigt (angefragte Vereine), L21 fortgeschrieben (ancova-CSV gerettet, Rest per Papierkorb), G21 und G26h auf den Papierkorb umgestellt, L8 fortgeschrieben (Endabgleich zweiter Lauf), L16 fortgeschrieben (R14 für 4.7).

'''
s = ersetze(s, '### ⭐ NEU (Rev. 91, 25.09.2026, 14:55 MESZ): Task „Phase 6 abschließen und Phase 7“',
            (REV92 % N_PAPIERKORB) + '### ⭐ NEU (Rev. 91, 25.09.2026, 14:55 MESZ): Task „Phase 6 abschließen und Phase 7“')
if chr(59) in REV92:
    raise SystemExit('Semikolon im Rev.-92-Block')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(ML, encoding='utf-8').read()
m = ersetze(m, '**Stand 25.09.2026, 14:55 MESZ (Rev. 91 — Task „Phase 6 abschließen und Phase 7“:',
            '**Stand 25.09.2026, 16:35 MESZ (Rev. 92 — Verfasserentscheidungen nach Phase 7: Papierkorb-Skript (`Ordner_aufraeumen.ps1`, %d Einträge, Verfasser löscht gesammelt), Sammelordner `06_Abbildungen`, Grafiken erst am Ende (Platzhalter im Master), vier angefragte Vereine (K-01.24, Abb. 1), Abb. H7, Erratum nicht beschaffbar (R14). A8 und L12 erledigt, L19 Rest erledigt, L8, L16 und L21 fortgeschrieben, G21 und G26h auf den Papierkorb umgestellt). Zuvor 25.09.2026, 14:55 MESZ (Rev. 91 — Task „Phase 6 abschließen und Phase 7“:' % N_PAPIERKORB)
# A8
m = ersetze(m, '- [ ] **A8 · ⭐ Projektanweisungen Fassung 14 in die claude.ai-Projekteinstellungen einsetzen** — **Stand 24.09.2026 (Rev. 87):**',
            '- [x] **A8 · ⭐ Projektanweisungen Fassung 14 in die claude.ai-Projekteinstellungen einsetzen** — **Erledigt 25.09.2026 (Rev. 92): Fassung 14 steht laut Verfasser in den Projekteinstellungen. F10 bis F12 gehen mit `Ordner_aufraeumen.ps1` (Fassung 25.09.) in den Papierkorb, nicht mehr ins `_Archiv`.** Vorher **Stand 24.09.2026 (Rev. 87):**')
# L8
m = ersetze(m, 'Master unverändert. **Offen:** Vorschlagsliste durch den Verfasser übertragen, Endabgleich erneut laufen lassen, **Freigabe F3**, Zahl der angefragten Vereine für Abb. 1)*',
            'Master unverändert. **Offen:** Vorschlagsliste durch den Verfasser übertragen, Endabgleich erneut laufen lassen, **Freigabe F3**, Zahl der angefragten Vereine für Abb. 1)* *(Rev. 92, 25.09.: angefragte Vereine erledigt (K-01.24, Abb. 1 mit vier angefragten und drei zugesagten Vereinen), Abb. H7 ergänzt, Endabgleich mit Kennzahlenblatt Rev. 2 erneut gelaufen, Ergebnis unverändert. **Offen:** Vorschlagsliste übertragen, Endabgleich danach erneut, **Freigabe F3**)*')
# L12
m = ersetze(m, '- [ ] **L12 · Erratum Khamis & Roche (Pediatrics 95(3), 457, 1995, doi 10.1542/peds.95.3.457) beschaffen**',
            '- [x] **L12 · Erratum Khamis & Roche (Pediatrics 95(3), 457, 1995, doi 10.1542/peds.95.3.457) beschaffen** — **Erledigt durch Entscheidung 25.09.2026 (Rev. 92): Das Erratum wird nicht beschafft (nur über die Bibliothek erreichbar), gearbeitet wird mit dem vorliegenden Stand. O1 und O2 endgültig, keine Wiederholung der Rechnung, Registereintrag R14, Einschränkung in 4.3, 4.7 und 6.3 (G2).** Vorher:')
# L19
m = ersetze(m, 'Offen bleibt die Zahl der angefragten Vereine in Abb. 1 (Platzhalter `ANGEFRAGT`).',
            'Offen bleibt die Zahl der angefragten Vereine in Abb. 1 (Platzhalter `ANGEFRAGT`). *(Rev. 92, 25.09.: erledigt, `ANGEFRAGT <- 4L`, `ZUGESAGT <- 3L` nach Angabe des Verfassers, K-01.24 im Kennzahlenblatt Rev. 2. Fassung 2 des Skripts zeichnet zusätzlich Abb. H7 (Zeitstrahl). Grafiken gesammelt in `06_Abbildungen`, im Master bis zum Ende nur Platzhalter)*')
# L21
m = ersetze(m, "*(Rev. 87: `Ordner_aufraeumen.ps1` arbeitet nur in `Claude\\`. Die Dateien unter `Schreiben\\`, `Auswertung\\`, `Claude outputs\\` und `Dashboard\\daten\\` liegen außerhalb und bleiben ein eigener Schritt)*",
            "*(Rev. 87: `Ordner_aufraeumen.ps1` arbeitet nur in `Claude\\`. Die Dateien unter `Schreiben\\`, `Auswertung\\`, `Claude outputs\\` und `Dashboard\\daten\\` liegen außerhalb und bleiben ein eigener Schritt)* *(Rev. 92, 25.09.: **umgestellt auf den Papierkorb.** `Auswertung\\ancova_ergebnisse.csv` gerettet als `03_Skripte\\Auswertung_B7_ANCOVA_2026-09-12_ancova_ergebnisse.csv`. Das Skript in der Fassung vom 25.09. arbeitet im ganzen Ordner `Bachelorarbeit` und verschiebt `Schreiben\\Auswertungs-und-Darstellungskonzept.docx`, `Auswertung\\` (ganz, mit `ausgabe\\`), `Claude outputs\\` (ganz), `Dashboard\\` (ganz, mit `daten\\`) nach `Bachelorarbeit\\Papierkorb`. Löschen tut der Verfasser nach Durchsicht. Offen bis zum Lauf des Skripts durch den Verfasser)*")
# G21
m = ersetze(m, 'Ebenso `_Archiv\\probe_transfer_2026-09-25.zip` (Transferprobe) löschen)*',
            'Ebenso `_Archiv\\probe_transfer_2026-09-25.zip` (Transferprobe) löschen)* *(Rev. 92, 25.09.: alle genannten Dateien stehen in der Papierkorb-Liste von `Ordner_aufraeumen.ps1` (Fassung 25.09.), der Verfasser löscht den Papierkorb gesammelt. Offen bis zum Lauf des Skripts)*')
# G26h
m = ersetze(m, "drei fachfremde Dateien aus `Ideen und Studien` entfernen (AnyConnect-.msi 17 MB, Notion-Setup-.exe 108 MB, DLRG-Nachweis-PDF — nicht Teil des Projekts).",
            "drei fachfremde Dateien aus `Ideen und Studien` entfernen (AnyConnect-.msi 17 MB, Notion-Setup-.exe 108 MB, DLRG-Nachweis-PDF — nicht Teil des Projekts). *(Rev. 92, 25.09.: alles Genannte steht in der Papierkorb-Liste von `Ordner_aufraeumen.ps1` (Fassung 25.09.), auch die beiden Installationsdateien. Der DLRG-Nachweis bleibt liegen, der Verfasser legt ihn selbst außerhalb des Projekts ab. Offen bis zum Lauf des Skripts)*")
# L16
m = ersetze(m, 'Der Endabgleich 7.3 schlägt für 4.4 die Streichung des TE/√n-Satzes vor (Vorschlag 4))*',
            'Der Endabgleich 7.3 schlägt für 4.4 die Streichung des TE/√n-Satzes vor (Vorschlag 4))* *(Rev. 92, 25.09.: Für 4.3 und 4.7 zusätzlich R14, Koeffizienten der Originalpublikation von Khamis und Roche, Erratum nicht eingesehen)*')
# Tabelle L und Summe
m = ersetze(m, '| L — Auswertungsverfahren | 19 (neu 24.09., L12–L14 Rev. 81, L17–L21 Rev. 85, L17 erledigt Rev. 86, L4 und L7 erledigt Rev. 90, L8 zu 6.1 bis 6.4 erledigt, Rev. 91: L19 erledigt, L8 zu 6.3, F2 und 7.1 bis 7.3 erledigt, Zählung nicht neu erhoben) | Phasen 1 bis 7 gelaufen, F3 und Vorschlagsliste beim Verfasser, dann Phase 8 |',
            '| L — Auswertungsverfahren | 19 (neu 24.09., L12–L14 Rev. 81, L17–L21 Rev. 85, L17 erledigt Rev. 86, L4 und L7 erledigt Rev. 90, L8 zu 6.1 bis 6.4 erledigt, Rev. 91: L19 erledigt, L8 zu 6.3, F2 und 7.1 bis 7.3 erledigt, Rev. 92: L12 entschieden (R14), L19 Rest erledigt, L21 auf den Papierkorb umgestellt, Zählung nicht neu erhoben) | Phasen 1 bis 7 gelaufen, F3 und Vorschlagsliste beim Verfasser, dann 4.7, Kapitel 5, Phase 8 |')
m = ersetze(m, '| **Summe** | **57 offen** (Stand 25.09., Rev. 91:',
            '| **Summe** | **57 offen** (Stand 25.09., Rev. 92: A8 und L12 erledigt, L19 Rest erledigt, L8, L16, L21, G21 und G26h fortgeschrieben — Zählung nicht neu erhoben. Stand 25.09., Rev. 91:')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
print('Sitzungsnotizen Rev. 92 und Maßnahmenliste fortgeschrieben, Papierkorb-Einträge: %d' % N_PAPIERKORB)

# -*- coding: utf-8 -*-
"""
Steuerung_Rev91_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 91) und Maßnahmenliste nach dem Task „Phase 6 abschließen und Phase 7“
Bachelorarbeit U15-Plyometrie · DSHS Köln · 25.09.2026

Zweck: Trägt den Abschluss des Tasks in die beiden Steuerdateien ein, als exakte Zeichenkettenersetzungen und
Einfügungen, ohne den übrigen Text zu berühren. Bricht ab, wenn eine Ankerstelle nicht genau einmal vorkommt.
Aufruf: python Steuerung_Rev91_2026-09-25.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Ausgabeordner>
Fassung: 2026-09-25, erste Fassung. Ohne Semikolon.
"""
import sys
import os

SN, ML, AUS = sys.argv[1:4]
os.makedirs(AUS, exist_ok=True)
SEMI = chr(59)


def ersetze(text, alt, neu, name):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Anker „%s“ kommt %d-mal vor statt einmal' % (name, n))
    return text.replace(alt, neu)


# ------------------------------------------------------------------ Sitzungsnotizen
sn = open(SN, encoding='utf-8').read()
sn = ersetze(sn, '**Stand: (Rev. 90 — siehe Block oben.) Zuvor:', '**Stand: (Rev. 91 — siehe Block oben.) Zuvor: (Rev. 90 — siehe Block oben.) Zuvor:', 'Standzeile')

BLOCK = r'''### ⭐ NEU (Rev. 91, 25.09.2026, 14:55 MESZ): Task „Phase 6 abschließen und Phase 7“ (L8 Teil 6.3, F2, Nachtrag 3, 7.1 bis 7.3, Abgabekopie, L12) — Phase 7 gerechnet, Vorschlagsliste für den Master liegt vor, Freigabe F3 beim Verfasser

**Auftrag (Verfasser, 25.09.):** sechs Schritte, Regeln wie Phase 6 (nur Skript, Ergebniswerte nur in Dateien, ohne Semikolon). Alle sechs erledigt, Details je Schritt:

**(1) Handprobe 6.3 als Excel-Formelprobe (R12):** `03_Skripte\Handprobe_2026-09-25.py` Fassung 2 erzeugt `04_Uebergaben\Handprobe_2026-09-25.xlsx` mit Excel-Formeln je Kennwert (34 Kennwerte über alle Schrittgruppen, Blätter Vokabular, Formelwerte, TE_Z30_prae, ANCOVA_Z30, Zusatzprüfungen Z1 bis Z4, Funktionen mit `_xlfn.`-Präfix, volle Neuberechnung beim Öffnen). `03_Skripte\Handprobe_Pruefung_2026-09-25.py/.txt` rechnet die Mappe in LibreOffice nach: 34 von 34 „stimmt“, Zusatzprüfungen 4 von 4, größte relative Abweichung 4e-15, bestanden. Verfasserentscheidung 25.09. als **R12** im Register (§ 5.10). ⚠ Die Fassung 2 der Mappe konnte nicht auf den Rechner geschrieben werden, weil die Datei in Excel geöffnet war (Fassung 1 vom Vormittag liegt dort). Sie liegt bereit und wird beim nächsten Task committet, sobald Excel geschlossen ist (oder der Verfasser führt `Handprobe_2026-09-25.py` selbst aus).

**(2) Nachtrag 3 (Teil F.8, N5.1 bis N5.4):** `03_Skripte\Spezifikation_Nachtrag3_2026-09-25.py/.txt` arbeitet C.1 bis C.4 nach der Empfehlung des Durchsichtsprotokolls ein (zehn Ersetzungen, Zahlenliste neu erzeugt). Spezifikation .md/.docx/.pdf im Stand Nachtrag 3 in `02_Befunde`, Stand Nachtrag 2 in `_Archiv\_ersetzt_2026-09-25_Nachtrag3`. Blindprüfung 2.2, dritter Lauf (`Blindpruefung_Spezifikation_2026-09-24.py` Fassung 3 mit den Ergebnisdateien und Protokollen der Phase 6 als zusätzliche Studienquellen): 0 Treffer in 16 neuen oder geänderten Zeilen, Direktscan ohne Abweichung. Vermerk `02_Befunde\Blindpruefung_Spezifikation_2026-09-24.docx/.pdf` um Abschnitte 7 und 8 erweitert, Abschnitt 8 nach der Klickfreigabe fortgeschrieben (`03_Skripte\Blindpruefung_Vermerk_Nachtrag3_2026-09-25.py`, `Blindpruefung_Vermerk_Bestaetigung_2026-09-25.py`). **Verfasser hat Nachtrag 3 per Klick freigegeben** (25.09.), Registereintrag **R13**. Der Blindordner bleibt im Stand Nachtrag 2.

**(3) Freigabe F2:** per Klick erteilt (Verfasser, 25.09.). Phase 6 ist damit abgeschlossen.

**(4) Phase 7.1 Kennzahlenblatt:** `03_Skripte\Kennzahlen_2026-09-25.py/.txt` erzeugt `02_Befunde\Kennzahlen_2026-09-25.md` (Abschnitte K-01 bis K-12, Bezugsmengen-Regel unverändert, jede Zeile mit den Kennungen der Ergebnisdatei, 1 843 von 3 559 Kennungen verwendet, alle T-Kennungen des Umfangsdokuments gedeckt) und die Anlage `Kennzahlen_2026-09-25_Werte.csv` (215 Zeilen mit ungerundeten Werten und Berichtsort). Quelle ist `Ergebnisse_R_2026-09-25.csv` (SHA 3194a805…), Prüfsumme gegen die Liste der Abgabe verifiziert. **Das Blatt vom 22.09. ist ersetzt** (mit Erzeuger im `_Archiv\_ersetzt_2026-09-25_Kennzahlen`, Originale im Ordner zum Löschen per Skript). Neu gegenüber dem 22.09.: %PAH und alle davon abhängigen Größen (R11), TE des 505-Seitenmittels (K29), n in Tab. 1 als TE-Menge (O5). **7.2 Objekte:** `03_Skripte\Objekte_2026-09-25.R` (base R, ohne Semikolon) erzeugt aus der Ergebnisdatei Tab. 1 bis 3, Abb. 1 (Teilnehmerfluss, Cluster- und Spielerebene) und Abb. 2 (reifeadjustierte Abschlusswerte gegen Ausgangswerte, Modelllinien je Gruppe, Gruppenmittel als Quadrate, Graustufen) sowie Tab. H1a bis H5 als CSV, dazu `Objekte_2026-09-25.md` und die Word-Datei `Objekte_2026-09-25.docx` (Werkzeug `Werkzeug_Objekte_Docx_2026-09-25.py`, Manuskriptformat: Titel kursiv oberhalb, Kopfzeile grau, Gitternetz, Anmerkung). Ausgabe in `03_Skripte\Objekte_2026-09-25\` (1 492 Kennungen verwendet). Vorab nach L19 mit synthetischen Daten geprüft (`Objekte_Synthetik_2026-09-25.py`, Lauf in `03_Skripte\Objekte_2026-09-25_synthetisch\`). Zahlen aller Zellen gegen das Kennzahlenblatt gegengeprüft. Offen in Abb. 1: Zahl der angefragten Vereine (Platzhalter `ANGEFRAGT`, Verfasser). **7.3 Endabgleich:** `03_Skripte\Endabgleich_Manuskript_2026-09-25.py/.txt` liest den Master nur, klassifiziert alle 835 Zahlen (`_Zahlen.csv`), führt 29 Satzprüfungen (25 stimmen) und formale Prüfungen und schreibt `02_Befunde\Abgleichprotokoll_Manuskript_2026-09-25` (.md/.docx/.pdf) mit **Vorschlagsliste (7 Punkte, Neufassungen mit Kennung neben der Zahl)**: 4.2 Reifestatus je Gruppe (R11) · 4.4 Nebensatz „ohne erkennbaren Zusammenhang mit der Leistung“ streichen (Ausschluss Nr. 13) · Tab. 1 durch Tab_1_Messguete ersetzen (Spaltenform § 3.2, TE des Seitenmittels) · TE/√n-Satz streichen · Anmerkung Tab. 1 ohne MDC und ohne N der Eingangsgetesteten · Datum der Ausgangstestung von Verein C in 4.3 nach K-03.3 · Anhang G „SPSS-Syntax“ → „R-Skripte“. Alles Übrige in 4.2, 4.4, 4.5.1 und 4.6 stimmt mit dem neuen Blatt und den Programmkennzahlen überein. Master unverändert (Prozessregel).

**(5) Abgabe der zweiten Instanz kopiert:** `03_Skripte\Abgabe_Kopie_2026-09-25.py/.txt` → `03_Skripte\Abgabe_R_2026-09-25\` (101 Dateien) und `03_Skripte\Abgabe_R_2026-09-25.zip`. 100 von 100 Prüfsummen der Liste der zweiten Instanz stimmen, die sechs PNG nach Entfernen des Transferblocks `caBX`. ⚠ Der Dateitransfer fügt den Block beim Schreiben auf den Rechner wieder ein (Probe 25.09.: PNG verändert, ZIP unverändert). Deshalb ist das ZIP die prüfsummenexakte Referenz, der Ordner die lesbare Kopie. Die Probedatei `_Archiv\probe_transfer_2026-09-25.zip` ist zu löschen (Skript). Blindordner unverändert.

**(6) Erratum Khamis & Roche (L12):** `05_Protokolle\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25` (.md/.docx/.pdf). PubMed führt nur den Originalartikel (PMID 7936860), kein Datensatz für das Erratum. Crossref bestätigt Erratum, Pediatrics 95(3), 457, 01.03.1995, mit dem Abstract „errors in Tables 1 and 2 … corrected version … appears below“. Volltext beim Verlag gesperrt (403), Unpaywall „closed“, Europe PMC vom Proxy abgewiesen. **Beschaffung nur über die Bibliothek (AAP-Zugang oder Fernleihe).** Bis dahin gilt O1, im Manuskript als Einschränkung zu berichten. Betrifft das Erratum verwendete Zeilen der Tab. 1, folgt der Weg aus L12 (Nachtrag, neuer Lauf beider Ketten, R-Eintrag wie R11).

**Regeln eingehalten:** alle neuen Skripte, Protokolle und das Kennzahlenblatt ohne Semikolon (das R-Skript wurde dafür auf eine Anweisung je Zeile umgestellt), Ergebniswerte stehen nur in Dateien, keine Zahl von Hand.

**Dateien (Ordner):** `02_Befunde\` Kennzahlen_2026-09-25.md + _Werte.csv, Abgleichprotokoll_Manuskript_2026-09-25 (.md/.docx/.pdf), Spezifikation_2026-09-24 (.md/.docx/.pdf, Nachtrag 3) + _Zahlenliste.csv, Blindpruefung_Spezifikation_2026-09-24 (.docx/.pdf), Auswertungsplan_2026-09-12 (.md/.docx/.pdf, R12 und R13) · `03_Skripte\` Handprobe_2026-09-25.py (F2), Handprobe_Pruefung_2026-09-25.py/.txt, Spezifikation_Nachtrag3_2026-09-25.py/.txt, Blindpruefung_Spezifikation_2026-09-24.py/.txt/_Treffer.csv (dritter Lauf), Blindpruefung_Vermerk_Nachtrag3_2026-09-25.py, Blindpruefung_Vermerk_Bestaetigung_2026-09-25.py, Auswertungsplan_Register_R12_R13_2026-09-25.py, Kennzahlen_2026-09-25.py/.txt, Objekte_2026-09-25.R, Objekte_2026-09-25\ (27 Dateien), Objekte_Synthetik_2026-09-25.py, Objekte_2026-09-25_synthetisch\ (27), Werkzeug_Objekte_Docx_2026-09-25.py, Endabgleich_Manuskript_2026-09-25.py/.txt/_Zahlen.csv, Abgabe_Kopie_2026-09-25.py/.txt, Abgabe_R_2026-09-25\ (101), Abgabe_R_2026-09-25.zip, Steuerung_Rev91_2026-09-25.py · `05_Protokolle\` Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25 (.md/.docx/.pdf) · `_Archiv\` _ersetzt_2026-09-25_Nachtrag3\, _ersetzt_2026-09-25_Kennzahlen\, Blindprüfung zweiter Lauf. Projektkopien der .md-Dateien unter `claude/`.

**Zu löschen per `Ordner_aufraeumen.ps1` (Cowork kann nicht löschen):** `02_Befunde\Kennzahlen_2026-09-22.md`, `03_Skripte\Kennzahlen_2026-09-22.py` und `.txt` (archiviert), `_Archiv\probe_transfer_2026-09-25.zip`, dazu weiterhin G21 (Kennzahlen_2026-09-15).

**Nicht geändert:** Blindordner und Abgabe der zweiten Instanz, Datenstand, Workbook, Manuskript-Master, Umfangsdokument, Berichtsraster.

**Nächste Schritte (Reihenfolge fest):** (1) Verfasser: Handprobe in Excel öffnen und prüfen (Fassung 2 folgt nach dem Schließen), Abgleichprotokoll Manuskript lesen, **Vorschlagsliste 1 bis 7 je Abschnitt freigeben** und in den Master übertragen (Kennung neben der Zahl), danach `Endabgleich_Manuskript_2026-09-25.py` erneut laufen lassen · (2) **Freigabe F3** (Übertrag in das Manuskript, Auswertungsverfahren Phase 7) · (3) Zahl der angefragten Vereine für Abb. 1 nennen (Flowchart-Felder vor der Zuteilung, F14 § 3) · (4) Kapitel 4.7 und 5 nach Berichtsraster mit dem Kennzahlenblatt vom 25.09. schreiben (Objekte aus `Objekte_2026-09-25.docx`) · (5) Phase 8 (L9) · A8 (Fassung 14 in die Projekteinstellungen) und L12 (Erratum über die Bibliothek) weiterhin offen. Nach Erhalt des Erratums zuerst L12 prüfen, weil ein Treffer die Rechnung wiederholt.

**Maßnahmenliste:** L8 zu 6.3, F2, 7.1 bis 7.3 erledigt (F3 offen), L19 erledigt, L12 fortgeschrieben (Rechercheprotokoll), L16 fortgeschrieben, G21 erweitert (Kennzahlen_2026-09-22).

'''
sn = ersetze(sn, '### ⭐ NEU (Rev. 90, 25.09.2026, 12:50 MESZ):', BLOCK + '### ⭐ NEU (Rev. 90, 25.09.2026, 12:50 MESZ):', 'Block Rev. 90')

# ------------------------------------------------------------------ Maßnahmenliste
ml = open(ML, encoding='utf-8').read()
ml = ersetze(ml, '**Stand 25.09.2026, 12:50 MESZ (Rev. 90 —',
             '**Stand 25.09.2026, 14:55 MESZ (Rev. 91 — Task „Phase 6 abschließen und Phase 7“: Handprobe 6.3 als Excel-Formelprobe bestanden (R12), Nachtrag 3 freigegeben (R13), F2 erteilt, Kennzahlenblatt vom 25.09. per Skript (ersetzt 22.09.), Objekte per R-Skript, Endabgleich des Masters mit Vorschlagsliste (7 Punkte), Abgabe kopiert (100 von 100 Prüfsummen), Erratum-Recherche ohne Volltext. L8 zu 6.3, F2 und 7.1 bis 7.3 erledigt (F3 offen), L19 erledigt, L12 und L16 fortgeschrieben, G21 erweitert). Zuvor 25.09.2026, 12:50 MESZ (Rev. 90 —', 'Standzeile ML')

ml = ersetze(ml, "7.2 Objekte (L19), 7.3 Endabgleich Manuskript (4.2 %PAH-Werte, Tab. 2))*",
             "7.2 Objekte (L19), 7.3 Endabgleich Manuskript (4.2 %PAH-Werte, Tab. 2))* *(Rev. 91, 25.09.: **6.3 erledigt** — Handprobe als Excel-Formelprobe, `Handprobe_2026-09-25.py` Fassung 2 und `Handprobe_Pruefung_2026-09-25.py/.txt`, 34 von 34 und Zusatzprüfungen 4 von 4 bestanden, Verfasserentscheidung R12. **F2 erteilt** (Klick 25.09.), Nachtrag 3 freigegeben (R13). **7.1 erledigt** — `02_Befunde\\Kennzahlen_2026-09-25.md` + `_Werte.csv` aus `Ergebnisse_R_2026-09-25.csv`, Erzeuger `03_Skripte\\Kennzahlen_2026-09-25.py`, Blatt vom 22.09. archiviert. **7.2 erledigt** — `03_Skripte\\Objekte_2026-09-25.R`, Ausgabe `Objekte_2026-09-25\\` mit Tab. 1 bis 3, Abb. 1 und 2, Tab. H1 bis H5, `Objekte_2026-09-25.docx` als Übergabematerial, synthetische Probe. **7.3 erledigt** — `03_Skripte\\Endabgleich_Manuskript_2026-09-25.py`, `02_Befunde\\Abgleichprotokoll_Manuskript_2026-09-25` mit Vorschlagsliste (7 Punkte, darunter 4.2 %PAH nach R11, Tab. 1 neu, TE/√n und MDC entfallen, Datum Verein C in 4.3, Anhang G ohne SPSS). Master unverändert. **Offen:** Vorschlagsliste durch den Verfasser übertragen, Endabgleich erneut laufen lassen, **Freigabe F3**, Zahl der angefragten Vereine für Abb. 1)*", 'L8')

ml = ersetze(ml, "Korrektur mit altem und neuem Ergebnis ins Register wie R11)*\n- [x] **L13",
             "Korrektur mit altem und neuem Ergebnis ins Register wie R11)* *(Rev. 91, 25.09.: Versuch über PubMed und Crossref, `05_Protokolle\\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25`: PubMed ohne eigenen Datensatz, Crossref bestätigt Erratum Pediatrics 95(3), 457, 01.03.1995 („errors in Tables 1 and 2“), Volltext beim Verlag gesperrt, Unpaywall „closed“. Beschaffung nur über die Bibliothek (AAP-Zugang oder Fernleihe). Phase 7.1 ist ohne das Erratum gelaufen, in 4.3 und 4.7 als Einschränkung berichten. Nach Erhalt zuerst prüfen, weil ein Treffer beide Ketten wiederholt)*\n- [x] **L13", 'L12')

ml = ersetze(ml, "Umgebung aus `Umgebung_2026-09-25.txt`)*\n- [x] **L17",
             "Umgebung aus `Umgebung_2026-09-25.txt`)* *(Rev. 91, 25.09.: Für 4.7 zusätzlich R12 (Handprobe als Formelprobe) und R13 (Nachtrag 3), Zahlen aus `Kennzahlen_2026-09-25` K-06 und K-07, verworfene Voraussetzung mit Prüfgröße, p und Bootstrap-KI nach R2. Der Endabgleich 7.3 schlägt für 4.4 die Streichung des TE/√n-Satzes vor (Vorschlag 4))*\n- [x] **L17", 'L16')

ml = ersetze(ml, "- [ ] **L19 · Objektskripte in R für Phase 7.2 vorbereiten:**", "- [x] **L19 · Objektskripte in R für Phase 7.2 vorbereiten:**", 'L19 Haken')
ml = ersetze(ml, "bis dahin synthetische Daten im selben Format)*\n- [x] **L20",
             "bis dahin synthetische Daten im selben Format)* **Erledigt 25.09. (Rev. 91):** `03_Skripte\\Objekte_2026-09-25.R` (base R), synthetische Probe `Objekte_Synthetik_2026-09-25.py` mit Lauf in `Objekte_2026-09-25_synthetisch\\`, realer Lauf in `Objekte_2026-09-25\\` (19 Tabellen als CSV, Abb. 1 und 2 als PNG und PDF, `Objekte_2026-09-25.md`, `Objekte_2026-09-25.docx`). Offen bleibt die Zahl der angefragten Vereine in Abb. 1 (Platzhalter `ANGEFRAGT`).\n- [x] **L20", 'L19 Text')

ml = ersetze(ml, "kein Handlungsbedarf.", "kein Handlungsbedarf. *(Rev. 91, 25.09.: dazu `02_Befunde\\Kennzahlen_2026-09-22.md`, `03_Skripte\\Kennzahlen_2026-09-22.py` und `.txt` — ersetzt durch `Kennzahlen_2026-09-25`, Kopien in `_Archiv\\_ersetzt_2026-09-25_Kennzahlen`, Originale löschen. Ebenso `_Archiv\\probe_transfer_2026-09-25.zip` (Transferprobe) löschen)*", 'G21')

ml = ersetze(ml, "| L — Auswertungsverfahren | 19 (neu 24.09., L12–L14 Rev. 81, L17–L21 Rev. 85, L17 erledigt Rev. 86, L4 und L7 erledigt Rev. 90, L8 zu 6.1 bis 6.4 erledigt, Zählung nicht neu erhoben) | Phasen 1 bis 6 gelaufen, F2 beim Verfasser, dann Phasen 7 und 8 |",
             "| L — Auswertungsverfahren | 19 (neu 24.09., L12–L14 Rev. 81, L17–L21 Rev. 85, L17 erledigt Rev. 86, L4 und L7 erledigt Rev. 90, L8 zu 6.1 bis 6.4 erledigt, Rev. 91: L19 erledigt, L8 zu 6.3, F2 und 7.1 bis 7.3 erledigt, Zählung nicht neu erhoben) | Phasen 1 bis 7 gelaufen, F3 und Vorschlagsliste beim Verfasser, dann Phase 8 |", 'Tabelle L')

ml = ersetze(ml, "| **Summe** | **57 offen** (Stand 25.09., Rev. 90:", "| **Summe** | **57 offen** (Stand 25.09., Rev. 91: L19 erledigt, L8 zu 6.3, F2, 7.1 bis 7.3 erledigt, L12, L16, G21 fortgeschrieben — Zählung nicht neu erhoben. Stand 25.09., Rev. 90:", 'Summe')

for text, name in ((sn, 'Cowork_Sitzungsnotizen.md'), (ml, 'Massnahmenliste_Datenverarbeitung.md')):
    with open(os.path.join(AUS, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
neu_sn = BLOCK
print('geschrieben:', ', '.join(os.listdir(AUS)), '· Semikolon im neuen Block:', SEMI in neu_sn)

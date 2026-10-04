# Abgleich_Einleitung_2026-09-30 — Skripte und Arbeitsdateien

Task „Einleitung: Abgleich mit der Argumentationsstruktur und Überarbeitung“ (Startprompt `04_Uebergaben\Uebergabe_Abgleich_Einleitung_Argumentationsstruktur_2026-09-30.md` § 0). Befund: `02_Befunde\Abgleich_Einleitung_Argumentationsstruktur_2026-09-30.md`. Alle Skripte ohne Semikolon (chr(59)), Satzteilung und Wortzählung wie `03_Skripte\Manuskriptstand_2026-09-25.py` (Fassung 3).

## Schritt 1 — Textstand (30.09.2026)

Reihenfolge:
1. `python textstand.py [<Pfad zu 04_Uebergaben>]` — setzt V (Zusammensetzung nach Übergabe § 3 aus den Textvorschlägen B1, B2 D1, B3 bis B5, B4, B5 S1 mit „deshalb“) und liest A (`Textstand_Verfasser_Anhang_2026-09-30.txt`, Anhang des Verfassers zum Taskstart). Schreibt `textstand_V.json`, `textstand_A.json`, `textstand_messung.txt`, `textstand_diff.txt` (satzweiser Abgleich A gegen V).
2. `python saetze_liste.py` — beide Kandidaten mit Satznummern (`textstand_saetze.md`), Grundlage der Registerprüfung.
3. `python textstand_T.py` — Textstand T nach den Klicks zu Schritt 1, Satz für Satz mit Herkunft, Messung und Seitenprognose (Modellrechnung, Parameter aus `..\Seitenmodell_2026-09-28.csv`). Schreibt `textstand_T.json`, `textstand_T_messung.txt`.
4. `python befund_schritt1.py` — schreibt § 0 und § 1 des Befunds (`befund_teil1.md`), § 2 ist von Hand (`befund_teil2.md`).

Weitere Dateien:
- `master_messung.txt`, `master_messung.csv` — Ausgabe des Messskripts am Master (48.791 Byte, MD5 e35315d68ecca83176bcdc2c6ca557c0): Einleitung nicht übertragen.
- `register_pruefung.md` — Prüfbericht des unabhängigen Subagenten: jede Zeile des Entscheidungsregisters (Übergabe § 4) an der Fundstelle, Teilentscheidungen gegen V und A, fehlende Registerzeilen.

## Schritt 2 (a) — Codierung, Zugfolge, Anteile (30.09.2026)

- `blind_input.md` — Satzliste des Textstands T ohne Codes, einzige Eingabe des blinden Zweitcodierers neben `..\Argumentationsstruktur_Einleitungen_2026-09-30\codebook.md`.
- `codes_A_T.py` — Codierung A (Ersteller dieses Abgleichs), festgelegt vor Kenntnis von B.
- `codes_B_T.json`, `memo_B_T.md` — Codierung B des unabhängigen Subagenten mit Notizen zu schwankenden Fällen.
- `konsens_T.py` — Entscheidungen zu allen 13 Abweichungen mit Grund, daraus der Konsens.
- `python abgleich_2a.py [<Pfad zur Anlage Argumentationsstruktur_Einleitungen_2026-09-30>]` — Übereinstimmung (κ), Umfang, Anteile, Zugfolge, Grundfigur, erstes Auftreten, Vorkommen, Lesarten gegen den Korpus (`summary.json` der Anlage). Schreibt `abgleich_2a.txt` und `abgleich_2a.json`. Liest `textstand_T.json` aus Schritt 1.

## Schritt 2 (b) — Aussagen des Befunds über die eigene Einleitung (30.09.2026)

- Teiltabelle 2b steht im Befund § 3.2 (53 Prüfpunkte). Die Messungen dazu (Konnektoren, Zahlen, Wortsummen) in `abgleich_2b.txt`. Grundlage: Anhang A und `abgleich_2a.txt`.

## Schritt 2 (c) — Bauregeln und Lücke (30.09.2026)

- Teiltabelle 2c steht im Befund § 3.3 (sieben Bauregeln, Lücke nach dem Schema von Anhang C). Grundlage: Konsenscodierung (Anhang A, `abgleich_2a.json`), kein eigenes Skript.

## Schritt 2 (d) — Korpusaussagen nachgezählt (30.09.2026)

- `python nachzaehlung_2d.py [<Anlage Argumentationsstruktur_Einleitungen_2026-09-30> <Saetze.csv> <Befund.md>]` — zählt am Satzkorpus der Anlage (Konsens und Codierer B) Vorzüge und Einführungssatz in zwei Lesarten, Gerät und Setting, Brückensatz, Mechanismus, Reife, Prävention, Bedeutung der Lücke, Dosis, Lücke und Zweck im selben Absatz, Anteile je Gruppe, dazu die Lückendimensionen aus Anhang C des Befunds mit Prüfung der Satzbezüge. Pfade relativ zum Ordner des Skripts. Schreibt `nachzaehlung_2d.txt`.
- Teiltabelle 2d steht im Befund § 3.4 (elf Prüfgegenstände, Korpusbasis der Kandidaten für Schritt 3).

## Schritt 3 — Wortlaut am Volltext und Potenziale (30.09.2026)

- `python wortbilanz_schritt3.py` — misst die fünf Sätze im Wortlaut des Verfassers gegen die freigegebenen Fassungen und gegen einfache Varianten (Streichung, Einfügung, Wortersatz), drei Entwürfe nur als Richtwert (P3c, P3d, P4c), keine Textvorschläge. Liest `textstand_T.json` und `textstand_V.json` aus dem eigenen Ordner, sonst aus dem Staging-Pfad. Schreibt `wortbilanz_schritt3.txt`. Grundlage der Wortbilanz in Befund § 4.
- Teiltabelle 3a (die fünf Sätze am Volltext) steht im Befund § 3.5, die Potenziale mit Klickergebnis in § 4. Die Volltextprüfung ist von Hand an den PDFs in `Ideen und Studien` gemacht (MD5 im Befund), kein eigenes Skript.
- `zweitpruefung_schritt3.md` — Bericht des unabhängigen Zweitprüfers zu § 0 Nr. 11 und 12, § 2.5, § 3.5 und § 4 (1 A, 8 B, 19 C), Umsetzung in Befund § 5.

## Schritt 4 — Überarbeitung Absatz für Absatz (30.09.2026)

- `python schritt4_messung.py` — setzt die Einleitung aus dem Textstand T (`textstand_T.json`) und den Neufassungen der freigegebenen Potenziale zusammen (Dict `NEU`, je Satz mit Potenzial und Klickstatus) und misst sie wie `Manuskriptstand_2026-09-25.py`: Wörter, Sätze, Median, längster Satz, Belegklammern und narrative Zitate je Absatz, Semikola, Abschnittsverweise, Quellen. Seitenprognose wie `textstand_T.py` (Modellrechnung, Parameter aus `..\Seitenmodell_2026-09-28.csv`). Prüft per Assertion, dass B1b wortgleich mit der Freigabe in Textvorschlag B1 § 1.2 ist. Sätze, die nur per Klick gelten, stehen im Dict `VARIANTEN` und werden je Variante getrennt gemessen (B4-P4a und B4-P3e, nach dem Klick 19:45 nur zur Dokumentation). Liest `textstand_T.json` und `textstand_V.json` aus dem eigenen Ordner, sonst aus dem Staging-Pfad. Schreibt `schritt4_messung.txt` und `schritt4_stand.json` (freigegebener Stand, Grundlage der Textvorschläge je Absatz).
- `zweitpruefung_B1b.md`, `zweitpruefung_B3.md`, `zweitpruefung_B4.md` — Berichte der unabhängigen Zweitprüfer je Absatz. Die Umsetzung steht im Textvorschlag `04_Uebergaben\Textvorschlag_Einleitung_Ueberarbeitung_2026-09-30.md` (§ 1.6, § 2.6, § 3.6).
- `python nachtrag_T1_T4.py [<Ordner ev3_daten> <Ausgabeordner>]` — trägt vor B4 die Vormerkungen nach: T1 `Tanner1966` neu, T1 `Roessler2014` berichtigt (Feld „kapitel“ mit ungeschütztem Semikolon, 16 statt 15 Felder, Inhalt nach Register 29.09., 06:40), T4 `Tanner1966` zweimal und `Radnor2017` („children“, „youth“, Modalität) neu. Prüft die MD5 der Eingaben, bestehende Zeilen bleiben byte-gleich. Schreibt `ev3_daten\T1_steckbriefe.csv`, `ev3_daten\T4_zitierfallen.csv` (im Projekt nach `Schreiben\ev3_daten` zurückgeschrieben) und `nachtrag_T1_T4.txt`. T1 72, T4 151 Einträge.
- `python schritt4_abschluss.py [<Anlage Argumentationsstruktur_Einleitungen_2026-09-30>]` — Abschluss von Schritt 4: codiert die ganze Einleitung im freigegebenen Wortlaut (`schritt4_stand.json`) neu, unveränderte Sätze mit dem Konsens aus `konsens_T.py`, geänderte nach den Zug-Tabellen des Textvorschlags (§ 1.3, § 2.3, § 3.3), und misst Profil, Anteile, Zugfolge, Absatzdominanz, Grundfigur und erstes Auftreten wie `abgleich_2a.py`, für den Textstand T und den freigegebenen Stand nebeneinander, gegen die zehn Kern-RCTs (`summary.json` der Anlage). Prüft per Assertion jeden Absatz gegen seine Freigabe. Schreibt `schritt4_abschluss.txt` und `schritt4_abschluss.json`. Ergebnis im Textvorschlag § 5 und im Befund § 6.
- `python Abgleich_Hausstil_2026-09-30.py <Befund.md> <Werkzeug_Hausstil_2026-09-25.py>` — datierte Kopie von `..\Argumentationsstruktur_Einleitungen_2026-09-30\Argumentationsstruktur_Hausstil_2026-09-30.py`, setzt den Befund `02_Befunde\Abgleich_Einleitung_Argumentationsstruktur_2026-09-30.md` als .docx und .pdf im Hausstil (Anhang A quer, DIN A4).
- Stand: Schritt 4 abgeschlossen. B1b freigegeben 18:02 (P1, P9), B3 freigegeben 18:46 (P2, S5 ohne Ferguson et al., 2024, Klick § 2.7 a), B4 freigegeben 19:45 (P3b, P4c mit DVZ-Bezug modal, Klick § 3.7 a). B1a, B2 und B5 bleiben wortgleich. Einleitung 930 Wörter, neu codiert 19:51 (Zugfolge und Grundfigur unverändert).

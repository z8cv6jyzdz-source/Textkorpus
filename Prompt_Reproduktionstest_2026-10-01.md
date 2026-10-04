Task Reproduktionstest der Rechenkette (Auswertungsverfahren 8.4) in Claude Code unter Windows

Auftrag des Verfassers (01.10.2026): Die statistische Auswertung soll Claude Code übernehmen. Per Klick entschieden (01.10.): keine neue Auswertung, sondern der offene Reproduktionstest nach Auswertungsverfahren 8.4 („frische Sitzung installiert allein aus dem Paket, rechnet neu, vergleicht mit dem Archiv“, Maßnahme L9, Plan Task 16 d). Neue Zahlen für das Manuskript entstehen nicht.

Stand vorab (Rev. 141):
- Datenprüfung: Das Workbook ergibt bytegleich den eingefrorenen Datenstand vom 24.09. (`Claude\03_Skripte\Datenpruefung_Workbook_2026-10-01.txt`).
- Probelauf in der Originalumgebung (Cloud-Sitzung, Ubuntu 24.04.4, r-base-core 4.3.3-2build2, BLAS und LAPACK 3.12.0 wie bei der Blindrechnung): Ergebnisdatei bytegleich, Validierung bestanden, Abgleich nach G.3 ohne Abweichung, Kennzahlenblatt bytegleich. Ein zweiter Lauf mit dem Windows-Zweig der Steuerung (unter Linux erzwungen) ebenso. Belege und Grenzen: `Claude\03_Skripte\Reproduktion_2026-10-01\Vermerk_Probelauf_Linux_2026-10-01.md`.
- Offen ist damit: Läuft das Paket unter Windows, so wie ein Leser von Anhang G es startet, und liefert es dort dieselben Zahlen?

Verfahren nach F17 § 1.2: rechnen und vergleichen nur per Skript, Protokoll mit nummerierter Befundliste, unabhängige Zweitprüfung durch einen Subagenten, Klickfragen, Teil 0. Unverändert bleiben `Claude\03_Skripte\Abgabe_R_2026-09-25\` und `Abgabe_R_2026-09-25.zip`, der Ordner `Statistik`, die Anlagen der Spezifikation, Kennzahlenblatt, Objekte und Master. Kein Skript der Abgabe wird geändert. Keine Zahl von Hand.

## 0 Vorab
- Arbeitsverzeichnis ist der Ordner `Bachelorarbeit`. Lesen: Teil 0 der Sitzungsnotizen (jüngste Rev., mindestens Rev. 141), Maßnahmenliste L9, `Claude\01_Verfahren\Auswertungsverfahren_2026-09-24` Phase 8, F17 § 1.2 und § 11.10, den Vermerk oben.
- Werkzeuge wie in Rev. 140: `<Rscript>` = `C:\Users\acul2\AppData\Local\Programs\R\R-4.3.3\bin\Rscript.exe`, `<Python>` = `C:\Users\acul2\AppData\Local\Programs\Python\Python311\python.exe`, Shell Git Bash mit `PYTHONIOENCODING=utf-8`. Immer mit vollem Pfad aufrufen, Versionen notieren. Rscript aus Git Bash starten, nicht aus PowerShell: `Grenzfaelle_2026-09-25.R` (G18) ruft `sha256sum` auf, das nur dort im Pfad liegt (`command -v sha256sum` muss einen Treffer liefern).
- SHA-256 der vier Werkzeuge vor der Verwendung prüfen (Werte in § 1). Weicht einer ab: stoppen.
- Workbook: SHA-256 von `Statistik\Studiendaten_U15_gesamt.xlsx` muss 86087d35390559ae331794d13020fce7d1a799a67c5b47879da06b39fefd1ac7 sein (Stand der Datenprüfung). Sonst zuerst `"<Python>" Claude/03_Skripte/Datenpruefung_Workbook_2026-10-01.py --aus "<S>/Datenpruefung_<Datum>.txt"` (braucht openpyxl, fehlt es: `"<Python>" -m pip install openpyxl`). Bei Abweichung stoppen.
- Gerechnet wird außerhalb von OneDrive im Scratchpad dieser Sitzung (im Folgenden `<S>`), je Lauf ein frischer Arbeitsordner. Konsolenausgaben nach `<S>/repro_X/Konsole_Lauf_X.txt`, nie in den Laufordner (der Vergleich zählt jede fremde Datei dort als Befund).
- Laufzeit: Gesamtlauf unter Linux rund 7 min, Prüfsummenskript rund 2 min, unter Windows eher länger. Lange Läufe im Hintergrund starten und auf das Ende warten oder mit Timeout 600000 ms.

## 1 Werkzeuge (vor der Verwendung lesen)
| Datei | SHA-256 |
|---|---|
| `Claude\03_Skripte\Reproduktion_2026-10-01\Reproduktion_Aufbau_2026-10-01.py` | 0b4a859c57724604ebd8665c4018234cd1458a4f4e39beb8df4c19cfd65ea02e |
| `Claude\03_Skripte\Reproduktion_2026-10-01\Gesamtlauf_Windows_2026-10-01.R` | f58734b9050de2c0b5ebc3f16b7c3ee3d8f773335388e1e6d930005876a94b13 |
| `Claude\03_Skripte\Reproduktion_2026-10-01\Reproduktion_Vergleich_2026-10-01.py` | 8059562578cb3b5440a6f9b532667a73733c79bfccdbe9b4c55c19fe6fb2ae0b |
| `Claude\03_Skripte\Datenpruefung_Workbook_2026-10-01.py` | f39021e2a631098b8d03b69a3f4dfa5ff3f7a95d0b050f04fb5c723db6e7516c |

- Aufbau `<Arbeitsordner>`: prüft das ZIP (SHA-256 200b2595…) und seinen Inhalt gegen `Pruefsummen_Abgabe_2026-09-25.txt`, entpackt es als Vergleichsstand nach `archiv\`, legt `lauf\` im Aufbau des Blindordners an (25 R-Skripte, Windows-Steuerung, Datenstand, sieben Anlagen, die Dateien der Abgabe, des Datenstands und die Anlagen per SHA-256 gegen ihre Sollliste).
- Steuerung: Kopie von `Gesamtlauf_2026-09-25.R` mit vier Änderungen W1 bis W4 (Kopf des Skripts, vollständiger Unterschied in `Gesamtlauf_Windows_2026-10-01_Diff.txt`). W1 Kindprozesse ohne `env =`, W2 Umgebungsdatei ohne `dpkg-query`, W3 Aufruf und Prüfsumme der Steuerung im Laufprotokoll, W4 `sha256sum.cmd` für G18, damit GNU sha256sum Pfade mit `/` erhält. Rechenskripte unverändert.
- Vergleich `<Arbeitsordner> --rscript <Rscript>`: Bestand, Ergebnisdatei, Abgleich nach G.3 mit `Abgleich_2026-09-25.R` der Abgabe, Validierung, Zwischendateien, Textausgaben nach Maskierung von Zeitstempeln, Laufdauern und Pfaden, Kennzahlenblatt aus der neuen Ergebnisdatei gegen `Claude\02_Befunde\Kennzahlen_2026-09-25`. Gleicht nichts an.
Die Skripte sind Werkzeuge, kein Ersatz für eigenes Hinsehen. Findest du in ihnen einen Fehler, nicht stillschweigend umgehen: als Befund, Korrektur nur als neue Fassung mit Datum.

## 2 Lauf A: Paket unverändert
1. `"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Aufbau_2026-10-01.py "<S>/repro_A"`
2. Vorprobe im Laufordner `<S>/repro_A/lauf/Abgabe_R_2026-09-25`: `"<Rscript>" -e "cat(system2('sha256sum', shQuote(normalizePath('Funktionen_2026-09-25.R')), stdout = TRUE))"`. Beginnt die Ausgabe mit `\`, maskiert sha256sum den Pfad mit Backslash, und G18 kann im unveränderten Paket nicht bestehen. Ergebnis ins Protokoll.
3. Im selben Ordner `"<Rscript>" Gesamtlauf_2026-09-25.R > "<S>/repro_A/Konsole_Lauf_A.txt" 2>&1`.
4. Erwartung nach dem Quelltext von R 4.3.3 (Vermerk, Abschnitt „Erwarteter Abbruch“), am Lauf zu prüfen und nicht vorwegzunehmen: Abbruch bei den Referenztests, weil `system2()` unter Windows `LC_ALL=C.UTF-8` vor den Skriptnamen in die Befehlszeile setzt und Rscript es als Skriptdatei liest. `Referenztests_2026-09-25.txt` zeigt dann „Fatal error: cannot open file 'LC_ALL=C.UTF-8'“.
5. Ergebnis mit Konsole und Schrittausgabe ins Protokoll. Bestätigt sich der Abbruch, ist das ein Befund für Anhang G (Task 16): Das archivierte Paket läuft unter Windows nicht ohne Anpassung der Steuerung.
6. Läuft Lauf A wider Erwarten durch: `"<Rscript>" Pruefsummen_Abgabe_2026-09-25.R` im selben Ordner, Vergleich wie in Abschnitt 4 mit `repro_A`, Lauf B entfällt.

## 3 Lauf B: nur die Steuerung angepasst
1. `"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Aufbau_2026-10-01.py "<S>/repro_B"`
2. Im Laufordner `<S>/repro_B/lauf/Abgabe_R_2026-09-25`: `"<Rscript>" Gesamtlauf_Windows_2026-10-01.R > "<S>/repro_B/Konsole_Lauf_B.txt" 2>&1`
3. Danach im selben Ordner `"<Rscript>" Pruefsummen_Abgabe_2026-09-25.R > "<S>/repro_B/Konsole_Pruefsummen_B.txt" 2>&1`. Es schreibt die Prüfsummenliste des Laufs, das Kennzahlenblatt prüft die Ergebnisdatei dagegen.
4. Bricht Lauf B ab: anhalten, Ursache aus Laufprotokoll, Konsole und Schrittausgabe bestimmen. W4 ist unter Windows nicht erprobt (Ausführung von `.cmd` durch R, Zeichensatz der Pfade). Weitere Änderungen nur an der Steuerung, als neue Fassung mit Datum im Namen und Grund im Kopf, Rechenskripte nie. Jede Änderung ist ein Befund.

## 4 Vergleich
`"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Vergleich_2026-10-01.py "<S>/repro_B" --rscript "<Rscript>"`, Ausgabe in `<S>/repro_B/vergleich/`.

Maßstab, vorab festgelegt:
- Ergebnisdatei: bytegleich (SHA-256 3194a805dc3e2c4bf0142ecab5f091d9e201449f3f2811b78073b406c74392a8) oder je Kennung nach G.3 (EXAKT gleich, DETERM |a − b| ≤ 1e-9 · max(1, |a|), ITERATIV ≤ 1e-6 relativ, ZUFALL ≤ 3 · √(MCSE_a² + MCSE_b²)). S19 zieht mit demselben Generator und Startwert wie das Original. Die Bootstrap-Grenzen sollten deshalb bis auf Rechengenauigkeit gleich sein, eine Abweichung, die nur innerhalb der ZUFALL-Toleranz liegt, ist zu erklären. Jede nicht identische Kennung mit Skript und relativer Abweichung ins Protokoll.
- Validierung: Referenztests 83 von 83, Grenzfälle 114 von 114.
- Kennzahlenblatt aus der neuen Ergebnisdatei: bei bytegleicher Ergebnisdatei `Kennzahlen_2026-09-25.md` und `_Werte.csv` bytegleich, sonst .md gleich bis auf die Prüfsumme der Quelle und in der _Werte.csv die gerundete Darstellung gleich, die Rohwerte nach DETERM. Dann ist jede Zahl des Manuskripts reproduziert.
- Unter Windows zu erwarten und nur zu benennen: Zeilenenden (CRLF), Bytes der .rds-Dateien (Betriebssystemkennung im gzip-Kopf, Inhalt gleich), Schrift und Rendering der Grafiken S14, Meldungen zur Spracheinstellung, die Versionszeile mit „ucrt“, letzte Stellen von Gleitkommazahlen (anderes BLAS und andere Mathematikbibliothek). Die sechs Grafiken S14 ansehen, ein Satz dazu ins Protokoll. Jeden weiteren Unterschied erklären. Nichts angleichen.
- Urteil: bestanden, wenn die Validierung bestanden ist, der Abgleich nach G.3 keine Abweichung zeigt, das Kennzahlenblatt nach dem Maßstab oben gleich ist und jeder Unterschied erklärt ist.

## 5 Ergebnis
- Protokoll `Claude\02_Befunde\Reproduktionsprotokoll_<Datum>` als .md, Lesefassung .docx mit `Claude\03_Skripte\Werkzeug_Hausstil_2026-09-25.py`, .pdf: Umgebung (`sessionInfo()`, `La_library()`, `extSoftVersion()`, Rscript- und Python-Pfad), Befehle wörtlich, Vorprobe, Lauf A, Lauf B, Vergleich nach den Abschnitten A bis G des Vergleichsskripts, Befundliste (Nr., Befund, Beleg, Folge, Ort der Änderung), Urteil, Klickfragen. Erst das Protokoll, dann eine kurze Zusammenfassung im Chat.
- Abweichungen von Plan Task 16 d im Protokoll nennen: Sitzung im Projektordner statt außerhalb, Eingang aus dem ZIP und dazu Datenstand und Anlagen (das ZIP enthält sie nicht, die Kette braucht sie), vorhandene R-Installation, Kenntnis des Probelaufs. Der Vergleich ist maschinell, das Vorwissen ändert sein Ergebnis nicht.
- Ausgaben nach `Claude\03_Skripte\Reproduktion_2026-10-01\Lauf_Windows\`: Aufbau- und Vergleichsprotokolle, Konsolen, Laufprotokolle, Umgebung, Validierungsprotokoll, Abgleich (.csv und _Protokoll.txt), Kennzahlen der Reproduktion, gegebenenfalls die Datenprüfung. Die Ergebnisdatei nur, wenn sie nicht bytegleich ist. Kein Zwischenordner.

## 6 Zweitprüfung, Freigabe, Abschluss
1. Subagent ohne Beteiligung am Protokoll: Aufbauprotokoll gegen ZIP, Datenstand und Anlagen, Unterschied der Steuerung (nur W1 bis W4 und begründete Nachträge), Ergebnisdatei je Kennung mit eigener Implementierung, Stichproben im Kennzahlenblatt, jede Aussage des Protokolls. Umgang je Befund dokumentieren.
2. Klickfragen mit AskUserQuestion, Empfehlung zuerst: (a) Anhang G (Task 16): archivierte Steuerung unverändert lassen und die geprüfte Windows-Steuerung als eigene Datei mit Hinweis zur Ausführung daneben stellen (Empfehlung bei bestandenem Lauf B) oder nur einen Hinweis zur Ausführung unter Windows aufnehmen · (b) Abgabeordner und ZIP vom Verfasser schreibgeschützt setzen lassen · (c) je unerklärtem Unterschied das weitere Vorgehen.
3. Teil 0 mit der nächsten freien Rev., Maßnahmenliste L9 (Reproduktionstest erledigt oder offen mit Grund), Vormerkung für Task 16 (Anhang G, Ausführung unter Windows). Die Projektkopien erreicht diese Sitzung nicht, das Protokoll lädt der Verfasser bei Bedarf hoch. Läuft der Kontext voll, rechtzeitig eine Übergabe schreiben.

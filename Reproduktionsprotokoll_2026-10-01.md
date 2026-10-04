# Reproduktionsprotokoll: Rechenkette unter Windows (Auswertungsverfahren 8.4)

**Bachelorarbeit U15-Plyometrie · Reproduktionstest der Rechenkette der Abgabe vom 25.09.2026 auf einem Windows-Rechner · 01.10.2026 · Claude Code (Fable 5.1), Arbeitsverzeichnis `Bachelorarbeit`**

Auftrag: `04_Uebergaben\Prompt_Reproduktionstest_2026-10-01.md` (Verfasser, 01.10.2026, Klick „Reproduktionstest“). Verfahren: Auswertungsverfahren 8.4, Maßnahme L9, Plan Task 16 d, F17 § 1.2 und § 11.10. Vorarbeit: `03_Skripte\Reproduktion_2026-10-01\Vermerk_Probelauf_Linux_2026-10-01.md` (Rev. 141). Neue Zahlen für das Manuskript entstehen nicht. Gerechnet und verglichen wurde nur per Skript, keine Zahl von Hand.

**Urteil in einem Satz:** Der Reproduktionstest unter Windows ist bestanden. Mit der geprüften Windows-Steuerung (W1 bis W4) und den unveränderten Rechenskripten entstehen auf diesem Rechner alle 3.559 Kennungen neu, Validierung 83 von 83 und 114 von 114, Abgleich nach G.3 ohne Abweichung, Kennzahlenblatt in der Darstellung gleich, einziger Unterschied eine Binärstelle einer Kennung. Das archivierte Steuerskript selbst bricht unter Windows ab, das ist der Befund für Anhang G.

Schreibweise: `<S>` steht für das Scratchpad dieser Sitzung, `C:\Users\acul2\AppData\Local\Temp\claude\C--Users-acul2-OneDrive-Desktop-Bachelorarbeit\2d971373-9de6-424e-a881-76f494acc75b\scratchpad`. `<Rscript>` steht für `C:\Users\acul2\AppData\Local\Programs\R\R-4.3.3\bin\Rscript.exe`, `<Python>` für `C:\Users\acul2\AppData\Local\Programs\Python\Python311\python.exe`. Uhrzeiten in UTC, wie die Kette sie schreibt. Die Sitzungsuhr liegt eine Stunde später.

## 1 Vorab: Werkzeuge, Eingänge, Lektüre

Gelesen: Teil 0 der Sitzungsnotizen (Rev. 141), Maßnahmenliste L9, Auswertungsverfahren Phase 8 (8.1 bis 8.4), F17 § 1.2 und § 11.10, Plan Task 16 d, der Vermerk zum Probelauf, die drei Werkzeugskripte des Ordners `Reproduktion_2026-10-01`, die Diff-Datei der Steuerung, `Gesamtlauf_2026-09-25.R`, `Funktionen_2026-09-25.R` (Abschnitt A, SHA-256-Funktionen) und der Abschnitt G18 in `Grenzfaelle_2026-09-25.R`.

**Prüfsummen vor der Verwendung (SHA-256, mit GNU sha256sum 8.32 aus Git Bash):**

| Datei | Soll (Prompt § 1) | Ist | Urteil |
|---|---|---|---|
| `Reproduktion_Aufbau_2026-10-01.py` | 0b4a859c… | 0b4a859c57724604ebd8665c4018234cd1458a4f4e39beb8df4c19cfd65ea02e | stimmt |
| `Gesamtlauf_Windows_2026-10-01.R` | f58734b9… | f58734b9050de2c0b5ebc3f16b7c3ee3d8f773335388e1e6d930005876a94b13 | stimmt |
| `Reproduktion_Vergleich_2026-10-01.py` | 80595625… | 8059562578cb3b5440a6f9b532667a73733c79bfccdbe9b4c55c19fe6fb2ae0b | stimmt |
| `Datenpruefung_Workbook_2026-10-01.py` | f39021e2… | f39021e2a631098b8d03b69a3f4dfa5ff3f7a95d0b050f04fb5c723db6e7516c | stimmt |
| `Statistik\Studiendaten_U15_gesamt.xlsx` | 86087d35… | 86087d35390559ae331794d13020fce7d1a799a67c5b47879da06b39fefd1ac7 | stimmt, Stand der Datenprüfung vom 01.10., keine neue Datenprüfung nötig |
| `Claude\03_Skripte\Abgabe_R_2026-09-25.zip` | 200b2595… | 200b25956c4e12a9104164c025eddbe67dadc79ee12c3300b3a8b6e1a786525f | stimmt, 871.200 B |
| `Abgabe_R_2026-09-25\Gesamtlauf_2026-09-25.R` | c027d74b… (Kopf der Windows-Steuerung) | c027d74b50b0bf8ac7ac982c9f3e43d397128d094212f3afad08d21c45fbd2e7 | stimmt |

**Eigener Unterschied der Steuerung:** `diff -u Gesamtlauf_2026-09-25.R Gesamtlauf_Windows_2026-10-01.R` (143 Zeilen) ist in allen Hunks identisch mit der mitgelieferten `Gesamtlauf_Windows_2026-10-01_Diff.txt`. Die Windows-Steuerung enthält damit genau die Änderungen W1 bis W4 und den Kopf, sonst nichts.

**Werkzeuge der Sitzung:** `<Rscript>` ist R 4.3.3 (2024-02-29 ucrt). `<Python>` ist Python 3.11.9 (openpyxl fehlt, es wird nicht gebraucht). Shell Git Bash, GNU bash 5.3.15 (MINGW64), `command -v sha256sum` liefert `/usr/bin/sha256sum` (GNU coreutils 8.32, Windows-Pfad `C:\Users\acul2\AppData\Local\Programs\Git\usr\bin\sha256sum.exe`). Alle Aufrufe mit vollem Pfad und `PYTHONIOENCODING=utf-8`, Rscript aus Git Bash.

## 2 Umgebung

Aufgezeichnet mit `<S>\umgebung\umgebung.R` vor den Läufen (Datei `Umgebung_Sitzung_R.txt`, Kopie unter `Lauf_Windows\`), dazu die Umgebungsdatei, die Lauf B nach W2 schreibt.

| Angabe | Wert |
|---|---|
| Rechner | Windows 11 Pro, Build 26200, x86-64 (`sessionInfo()`: „Windows 11 x64 (build 26200)“, `Sys.info()`: release „10 x64“) |
| R | R version 4.3.3 (2024-02-29 ucrt), Plattform x86_64-w64-mingw32/x64 (64-bit), CRAN-Installer im Benutzerordner, `R.home()` = `C:/Users/acul2/AppData/Local/Programs/R/R-4.3.3`, `R.home("bin")` = `…/bin/x64` |
| Rscript | `<Rscript>` (`bin\Rscript.exe`) startet `bin\x64\Rscript.exe`, das R selbst lädt (R.dll, kein Rterm-Kindprozess), `commandArgs()[1]` meldet `bin\x64\Rterm.exe` als Programmnamen. Die Steuerung ruft die Kindprozesse über `file.path(R.home("bin"), "Rscript")`, unter Windows also `bin/x64/Rscript` |
| BLAS und LAPACK | `La_version()` 3.11.0, `La_library()` leer (R für Windows mit eingebautem Rblas und Rlapack, `sessionInfo()`: „Matrix products: default“), `extSoftVersion()["BLAS"]` leer. Original: Ubuntu-Pakete libblas3 und liblapack3 3.12.0 |
| extSoftVersion | zlib 1.3, bzlib 1.0.8, xz 5.4.4, PCRE 10.42, ICU 73.2, TRE 0.8.0, iconv win_iconv |
| Grafik | `capabilities()`: cairo TRUE, png TRUE |
| Spracheinstellung | beim Start `German_Germany.utf8` (LC_NUMERIC C), Codepage 65001, `l10n_info()$UTF-8` TRUE. `Sys.setlocale("LC_ALL", "C.UTF-8")` wird vom System abgelehnt: Warnung „OS meldet: Anfrage Lokalisierung auf "C.UTF-8" zu setzen kann nicht beachtet werden“, Rückgabe `""`, Einstellung bleibt `German_Germany.utf8`. Das ist der im Vermerk offen gelassene Fall, R rechnet in UTF-8 weiter |
| Zeitzone | Elternprozess Europe/London (`sessionInfo()`), `Funktionen_2026-09-25.R` setzt in jedem Prozess TZ=UTC |
| Umgebungsvariablen | LANG, LC_ALL, LANGUAGE und TZ beim Start leer |
| sha256sum aus R | `Sys.which("sha256sum")` = `C:\Users\acul2\AppData\Local\Programs\Git\usr\bin\SHA256~1.EXE` (Kurzname von sha256sum.exe) |
| Python | `<Python>`, 3.11.9 |
| Originalumgebung zum Vergleich | Ubuntu 24.04.4, r-base-core 4.3.3-2build2, libblas3 und liblapack3 3.12.0 (Vermerk, `Umgebung_2026-09-25.txt` der Abgabe) |

`sessionInfo()` des Elternprozesses wörtlich:

```
R version 4.3.3 (2024-02-29 ucrt)
Platform: x86_64-w64-mingw32/x64 (64-bit)
Running under: Windows 11 x64 (build 26200)

Matrix products: default

locale:
[1] LC_COLLATE=German_Germany.utf8  LC_CTYPE=German_Germany.utf8
[3] LC_MONETARY=German_Germany.utf8 LC_NUMERIC=C
[5] LC_TIME=German_Germany.utf8

time zone: Europe/London
tzcode source: internal

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base

loaded via a namespace (and not attached):
[1] compiler_4.3.3
```

Quelltext von `system2()` dieser R-Fassung unter Windows, geprüft mit `deparse(system2)`: die Zeile `command <- paste(c(shQuote(command), env, args), collapse = " ")` ist vorhanden. Die Angaben aus `env =` stehen unter Windows also in der Befehlszeile, wie der Vermerk sagt.

## 3 Aufbau der Arbeitsordner

Befehle (aus `Bachelorarbeit`, Git Bash):

```
"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Aufbau_2026-10-01.py "<S>/repro_A"
"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Aufbau_2026-10-01.py "<S>/repro_B"
```

Beide Aufbauten bestanden (`Aufbau_Protokoll.txt` je Ordner, Läufe 16:20:58 und 16:21:03 Sitzungsuhr): ZIP 200b2595… (Soll stimmt), 101 Dateien entpackt, Prüfsummenliste der Abgabe 100 Einträge, 0 Abweichungen · Laufordner mit 25 R-Skripten der Abgabe (Prüfsummen wie in der Liste) und `Gesamtlauf_Windows_2026-10-01.R` f58734b9… · `Datenstand_2026-09-24` 7 Dateien, davon 6 gegen `Pruefsummen.txt` bestanden, die Liste selbst (a125862c…) wie im Laufprotokoll des Archivs · sieben Anlagen der Spezifikation, jede gleich dem Soll in `Funktionen_2026-09-25.R`. Der Aufbau liest nur aus dem Projektordner und schreibt nur in `<S>`.

## 4 Vorprobe zu sha256sum (Prompt § 2 Nr. 2)

Im Laufordner `<S>\repro_A\lauf\Abgabe_R_2026-09-25`:

```
"<Rscript>" -e "cat(system2('sha256sum', shQuote(normalizePath('Funktionen_2026-09-25.R')), stdout = TRUE))"
```

Ausgabe (Datei `Vorprobe_sha256sum_A.txt`):

```
\30c74291db1a027df40d3f2e1a794ca10b4907c49d5fcb667224cff54ef2dd10 *C:\\Users\\acul2\\…\\repro_A\\lauf\\Abgabe_R_2026-09-25\\Funktionen_2026-09-25.R
```

Die Ausgabe beginnt mit `\`: GNU sha256sum maskiert den Dateinamen, weil R den Pfad aus `normalizePath()` mit Backslash übergibt, und stellt der Prüfsumme einen Backslash voran. `Grenzfaelle_2026-09-25.R` schneidet in G18 nur ab dem ersten Leerzeichen ab und vergliche `\30c74291…` mit `30c74291…`. G18 kann im unveränderten Paket unter Windows nicht bestehen, wie im Vermerk (Erwarteter Abbruch Nr. 3) hergeleitet. Ergänzung aus Git Bash: derselbe Pfad mit `/` ergibt `30c74291… *C:/Users/…/Funktionen_2026-09-25.R` ohne Maskierung, derselbe Pfad mit `\` wieder die maskierte Form. Die Prüfsumme 30c74291… ist der Sollwert in `Pruefsummen_Abgabe_2026-09-25.txt` des Archivs (Zeile 3) und steht so im Laufprotokoll von Lauf A. Der abschließende `grep` in der Belegdatei ging ins Leere, weil die Liste nur im Archiv liegt, nicht im Laufordner.

## 5 Lauf A: Paket unverändert

Befehl im Laufordner `<S>\repro_A\lauf\Abgabe_R_2026-09-25`:

```
"<Rscript>" Gesamtlauf_2026-09-25.R > "<S>/repro_A/Konsole_Lauf_A.txt" 2>&1
```

Start 15:22:14 UTC, Ende 15:23:45 UTC, Exit-Status 1 (`Zeiten_Lauf_A.txt`).

**Verlauf (Konsole und `Laufprotokoll_2026-09-25.txt`):** Als Erstes die Warnmeldung zu `Sys.setlocale("LC_ALL", "C.UTF-8")` (Abschnitt 2). Das Laufprotokoll ist bis zur Phase 4 geschrieben: Kopf, Skriptfassungen mit SHA-256 der 23 Skripte, die die Steuerung führt (Funktionen, Gesamtlauf, Referenztests, Grenzfälle, S01 bis S19, Werte wie in der Prüfsummenliste), Prüfsummen des Eingangs (Datenstand und sieben Anlagen, „Soll stimmt“). Dann:

```
Phase 4, Validierung (Referenztests und Grenzfälle):
  Referenztests_2026-09-25.R               Status 5  Dauer    0.1 s  Warnungen 0  Ausgabe Referenztests_2026-09-25.txt
  ABBRUCH der Kette: Referenztests_2026-09-25.R nicht bestanden.

ABBRUCH: Validierung nicht bestanden: Referenztests_2026-09-25.R
Fehler: ABBRUCH: Validierung nicht bestanden: Referenztests_2026-09-25.R
Ausführung angehalten
```

`Referenztests_2026-09-25.txt` ist 0 Byte groß. Der Ordner `Zwischen` ist leer, es gibt keine Ergebnisdatei. Die Kette bricht beim ersten Kindprozess ab. Damit entfällt Prompt § 2 Nr. 6, Lauf B ist nötig.

**Abweichung von der Erwartung:** Der Vermerk erwartet nach dem Quelltext von R 4.3.3 und einer Nachstellung unter Linux den Status 2 und in `Referenztests_2026-09-25.txt` die Zeile „Fatal error: cannot open file 'LC_ALL=C.UTF-8'“. Beobachtet wurden Status 5 und eine leere Schrittausgabe. Die Ursache wurde mit isolierten Tests außerhalb der Laufordner geklärt (`<S>\test_system2\`, Dateien `Tests_system2_Ergebnis.txt` und `Tests_status_Ergebnis.txt`, Kopien unter `Lauf_Windows\`). Testskript `hallo.R` schreibt eine Zeile, TZ, LC_ALL, LANGUAGE und den eigenen `--file=`-Eintrag:

| Test | Aufruf aus R (`RS = file.path(R.home("bin"), "Rscript")`, wie in der Steuerung) | Status | Ausgabe |
|---|---|---|---|
| T1 | wie `Gesamtlauf_2026-09-25.R`: `env = c("LC_ALL=C.UTF-8", "LANG=C.UTF-8", "TZ=UTC")`, stdout = stderr = Datei | 5 | Datei 0 B |
| T2 | wie W1: ohne `env`, stdout = stderr = Datei | 0 | vollständig, TZ, LC_ALL und LANGUAGE leer, `--file=` zeigt `hallo.R` |
| T3 | `env` wie T1, stdout und stderr getrennte Dateien | 5 | beide 0 B |
| T4 | `env` wie T1, `stdout = TRUE` | 5 (Attribut status) | leer |
| T5 | nur `env = "TZ=UTC"` | 5 | 0 B, ein einziger Eintrag in `env` genügt |
| T8 | `Rscript --file=LC_ALL=C.UTF-8` ohne weitere Argumente | 1 | „file name is missing“ (Rscript-Frontend) |
| T9 | `Rscript "<S>/test_system2/gibt_es_nicht.R"` (nicht vorhandene Skriptdatei, ohne `env`) | 5 | 0 B, dieselbe Erscheinung wie T1 |

T6 und T7 (Rterm.exe und bin/x64/Rscript.exe direkt) sind ohne Aussage: Ich hatte `x64` doppelt in den Pfad gesetzt, weil `R.home("bin")` unter Windows schon `bin/x64` liefert (Status 127, „not found“). Das ist ein Fehler meiner Testanlage, nicht der Kette.

Direkt aus Git Bash, ohne R dazwischen (nach der Zweitprüfung erneut ausgeführt und als `Tests_GitBash_Direkt_Ergebnis.txt` mit `Tests_GitBash_Direkt.sh` abgelegt):

```
"<Rscript>" LC_ALL=C.UTF-8 LANG=C.UTF-8 TZ=UTC hallo.R      → Segmentation fault, Status 139
"<R-Ordner>/bin/x64/Rscript.exe" LC_ALL=C.UTF-8 LANG=C.UTF-8 TZ=UTC hallo.R   → Segmentation fault, Status 139
"<Rscript>" --file=LC_ALL=C.UTF-8                             → file name is missing, Status 1
"<Rscript>" gibt_es_nicht.R                                   → Segmentation fault, Status 139
"<R-Ordner>/bin/x64/Rterm.exe" --no-echo --no-restore --file=gibt_es_nicht.R   → Segmentation fault, Status 139
"<R-Ordner>/bin/x64/Rterm.exe" --no-echo --no-restore --file=LC_ALL=C.UTF-8    → Segmentation fault, Status 139
"<R-Ordner>/bin/x64/Rterm.exe" --no-echo --no-restore --file=hallo.R (Kontrolle) → Ausgabe vollständig, Status 0
"<Rscript>" hallo.R  (Kontrolle)                              → Ausgabe vollständig, Status 0
```

Statusabbildung von `system2()` unter Windows, geprüft mit `cmd /c exit <Code>`: 3221225477 (0xC0000005, STATUS_ACCESS_VIOLATION) wird als 5 gemeldet, 3221225478 (0xC0000006) als 6, 3221225725 (0xC00000FD) als 253, 2147483649 als 1, 65541 als 5, 261 als 261, 256 als 256, 2 als 2. `system2()` gibt also die unteren 16 Bit des Prozessendes zurück. Derselbe Aufruf `cmd /c exit 3221225477` endet in Git Bash mit „Segmentation fault“, Status 139 (128 + 11). Status 5 in Lauf A ist damit das Ende des Kindprozesses mit 0xC0000005, einer Zugriffsverletzung.

**Schluss zu Lauf A:** Der im Vermerk hergeleitete Mechanismus trifft zu: `system2()` setzt die Angaben aus `env =` unter Windows in die Befehlszeile (Abschnitt 2, T1 gegen T2, T5), und das Rscript-Frontend nimmt `LC_ALL=C.UTF-8` als Skriptdatei. Die Erscheinung ist unter Windows aber eine andere als unter Linux: R 4.3.3 (ucrt) für Windows endet beim Start mit einer Zugriffsverletzung (0xC0000005), wenn die mit `--file=` übergebene Datei nicht geöffnet werden kann, über `Rscript.exe` wie über `Rterm.exe`, bevor eine Meldung geschrieben ist (T9, Direktaufrufe oben). `bin\x64\Rscript.exe` lädt R dabei selbst (R.dll), ein Rterm-Kindprozess entsteht nicht, der Fehler liegt also im Start von R und nicht allein im Rscript-Frontend. Die Schrittausgabe bleibt leer, das Laufprotokoll zeigt Status 5 statt 2. Das ist ein Verhalten dieser R-Fassung unter Windows, nicht der Kette. Ein Beitrag in der Posit Community (R 4.4.0 unter Git Bash) berichtet nebenbei, dass ein falscher Dateiname denselben Segmentation fault auslöst (Beleg in der Befundliste). Ob spätere R-Fassungen das Verhalten zeigen, wurde nicht geprüft, nur R 4.3.3 ist installiert. Das archivierte Paket läuft unter Windows nicht ohne Anpassung der Steuerung (Befund für Anhang G, Task 16). Die Formulierung „Referenztests_2026-09-25.txt zeigt dann ‚Fatal error: cannot open file …‘“ im Vermerk und im Prompt trifft unter Windows nicht zu und ist zu berichtigen.

## 6 Lauf B: nur die Steuerung angepasst

Befehle im Laufordner `<S>\repro_B\lauf\Abgabe_R_2026-09-25` (Git Bash, Hintergrund):

```
"<Rscript>" Gesamtlauf_Windows_2026-10-01.R > "<S>/repro_B/Konsole_Lauf_B.txt" 2>&1
"<Rscript>" Pruefsummen_Abgabe_2026-09-25.R > "<S>/repro_B/Konsole_Pruefsummen_B.txt" 2>&1
```

Gesamtlauf: Start 15:26:27 UTC, Ende 15:46:44 UTC, Exit-Status 0, Dauer nach Laufprotokoll 20,3 min (Linux: Blindrechnung vom 25.09. 6,4 min, Probelauf Lauf 2 vom 01.10. 7,1 min). Die Kindprozesse brauchen 32 bis 46 s je Schritt statt 9 bis 16 s, S19 63,8 s statt 17,9 s (Blindrechnung) und 22,4 s (Probelauf Lauf 2). Treiber ist die SHA-256-Berechnung in reinem R, die jeder Schritt für Datenstand und Anlagen ausführt.

**Laufprotokoll (`Laufprotokoll_2026-09-25.txt`):** Kopf mit „Steuerung: Gesamtlauf_Windows_2026-10-01.R, Windows-Anpassung W1 bis W4, Rechenskripte unverändert“ und „G18-Gegenprobe (W4): sha256sum.cmd mit Pfaden in /, ruft C:\Users\acul2\AppData\Local\Programs\Git\usr\bin\SHA256~1.EXE“ (W3, W4). Skriptfassungen mit SHA-256 wie im Archiv, dazu die Zeile „Gesamtlauf_Windows_2026-10-01.R  Steuerung dieses Laufs  f58734b9…“. Prüfsummen des Eingangs wie im Archiv, alle Anlagen „Soll stimmt“. Die vier Zeilen „nur dokumentiert, nicht gelesen“ fehlen wie im Probelauf, weil Spezifikation und Auswertungsverfahren nicht im Eingangsordner liegen (die Kette liest sie nicht).

```
Phase 4, Validierung (Referenztests und Grenzfälle):
  Referenztests_2026-09-25.R               Status 0  Dauer    9.1 s  Warnungen 0
  Grenzfaelle_2026-09-25.R                 Status 0  Dauer   25.8 s  Warnungen 0
Validierung bestanden. Studiendaten werden gerechnet.
Phase 5, Gesamtlauf S01 bis S19: alle 19 Schritte Status 0, Warnungen 0
Ergebnisdatei nach G.1:
  Kennungen der Anlage (Muster): 1535, ausgeschrieben: 3559, davon Spielerkennungen: 2096
  Zeilen der Ergebnisdatei: 3559, mit Wert: 3425, fehlend mit Grund: 134
    Grund Eingang fehlt: 22 · Fallzahlregel: 14 · nicht erhebbar: 3 · zu wenige Werte: 95
  Datei: Ergebnisse_R_2026-09-25.csv  SHA-256 08fdc3f3ad46f36e9b707690cdd029a0bd88f9bc0c5dc8ba653787afbf0de700
Warnungen der Skripte (jede mit Erklärung):
  keine Warnungen
Ende des Gesamtlaufs: 2026-10-01 15:46:43 UTC, Dauer 20.3 min
Gesamtlauf ohne Abbruch beendet.
```

Der Block zur Ergebnisdatei ist bis auf die Prüfsumme wortgleich mit dem Archiv (gleiche Zahlen 1535, 3559, 2096, 3425, 134, 22, 14, 3, 95).

**Validierung (`Validierungsprotokoll_2026-09-25.txt`):** Referenztests 83 Sollwerte, bestanden 83, nicht bestanden 0 · Grenzfälle 114 Fälle, bestanden 114, nicht bestanden 0 · „Urteil: Validierung bestanden, Studiendaten wurden gerechnet.“ Die 13 G18-Zeilen (sieben Dateien des Datenstands, sechs Auffüllgrenzen) stehen auf 1, Soll und Ist gleich. W4 hat damit unter Windows funktioniert: R hat die `.cmd`-Datei ausgeführt, GNU sha256sum hat den Pfad mit `/` ohne Maskierung angenommen.

**Spracheinstellung in den Kindprozessen:** Jede Schrittausgabe beginnt mit drei Zeilen, die im Archiv fehlen:

```
Warning message:
In Sys.setlocale("LC_ALL", "C.UTF-8") :
  OS reports request to set locale to "C.UTF-8" cannot be honored
```

Das ist die in Abschnitt 2 gezeigte Ablehnung von „C.UTF-8“ durch Windows, dank `LANGUAGE=en` (W1) in englischer Fassung. R rechnet in der UTF-8-Voreinstellung weiter, die Zählung „Warnungen 0“ der Steuerung zählt nur Zeilen mit „WARNUNG:“ und ist davon nicht berührt. Die Konsole des Elternprozesses trägt dieselbe Warnung auf Deutsch, weil `LANGUAGE=en` erst nach dem Laden von `Funktionen_2026-09-25.R` gesetzt wird.

**Umgebungsdatei (`Umgebung_2026-09-25.txt`, W2):** Betriebssystem Windows, Installation R für Windows (CRAN-Installer), Aufruf „Rscript Gesamtlauf_Windows_2026-10-01.R im Ordner Abgabe_R_2026-09-25, LANGUAGE=en, LC_ALL nicht gesetzt (W1), sha256sum über C:\Users\acul2\AppData\Local\Programs\Git\usr\bin\SHA256~1.EXE (W4)“, Plattformangaben Sys.info Windows 10 x64 build 26200 x86-64, La_version 3.11.0, La_library leer, extSoftVersion wie in Abschnitt 2, R.home, R.version.string „R version 4.3.3 (2024-02-29 ucrt)“, `sessionInfo()` mit Zeitzone UTC, Rscript-Pfad `…/bin/x64/Rscript`, „Rscript (R) version 4.3.3 (2024-02-29)“.

**Ergebnisdatei:** SHA-256 08fdc3f3… statt 3194a805…, nicht bytegleich. Eigene Durchsicht vor dem Vergleichsskript (`<S>\analyse_kennungen.py`, Ausgabe `Analyse_Kennungen_eigene_Durchsicht.txt`): 3.559 Zeilen in beiden Dateien, gleiche Reihenfolge der Kennungen, Einheit, Grund und Skript in allen Zeilen gleich, der Wert in 3.558 Zeilen zeichengleich. Genau eine Kennung weicht ab:

| Kennung | Bedeutung (Anlage Kennungen) | Archiv | Lauf B | Abstand |
|---|---|---|---|---|
| S10.TELO.Z05.POST.ALL.X | untere 95-%-KI-Grenze TE, Sprint 5 m, Abschlusstestung, alle Spieler, in s | 0.032338581242701427 | 0.032338581242701420 | 6,9 · 10⁻¹⁸ absolut, nach G.3 bezogen auf max(1, Betrag a) = 1 derselbe Wert, gewöhnlich relativ 2,1 · 10⁻¹⁶, eine Binärstelle (Bitmuster 3fa08eaeb9ac4215 gegen …4214) |

Der Wert entsteht in `S10_Messguete_2026-09-25.R` Zeile 75 als `te * sqrt(df / qchisq(p, df))`. Quantil, Wurzel und Division laufen über die Mathematikbibliothek der Plattform (UCRT statt glibc), eine Abweichung in der letzten Binärstelle ist der im Prompt erwartete Fall „letzte Stellen von Gleitkommazahlen“. Alle übrigen 3.558 Werte sind auch nach 17 Ziffern gleich, darunter die ANCOVA-Schätzer aus S13 (LAPACK 3.11.0 statt 3.12.0), die Bootstrap-Grenzen aus S19 (gleicher Generator, gleicher Startwert) und die Poweranalyse aus S18. Im Kennzahlenblatt geht die Kennung in K-05.1 ein, dort gerundet als „0,032“ (untere Grenze des TE-KI für den 5-m-Sprint post), die Rundung ist von der 17. signifikanten Ziffer nicht berührt.

**Weitere Dateien gegen das Archiv (Bytes, eigene Durchsicht):** 41 Zwischendateien, alle 12 `.csv` unter `Zwischen` nur in den Zeilenenden verschieden (CRLF), alle 29 `.rds` byteverschieden bei gleicher Größe (S10_ergebnisse.rds 2.809 statt 2.808 B, das ist die Datei mit der abweichenden Kennung), die sechs Grafiken S14 byteverschieden und kleiner (28 bis 35 KB statt 46 bis 51 KB). Die inhaltliche Prüfung der `.rds` übernimmt das Vergleichsskript (Abschnitt 8 E).

**Sichtprüfung der sechs Grafiken S14 (Lauf B gegen Archiv):** Die sechs Grafiken (Q-Q-Diagramme der Residuen und Residuen gegen Vorhersage, Prä-Wert und %PAH für Z30, CM und SBJ) zeigen dieselben Punkte an denselben Stellen, dieselben Referenzlinien, Achsenbereiche, Achsenbeschriftungen, Titel und Legenden (IG gefüllt, KG offen), verschieden sind nur Schriftbild und Rasterung (Windows-Schrift über Cairo) und damit die Dateigröße. Ein inhaltlicher Unterschied ist nicht zu sehen.

## 7 Prüfsummenskript nach Lauf B

`Pruefsummen_Abgabe_2026-09-25.R` im Laufordner B, Start 15:48:17 UTC, Ende 15:54:21 UTC, Exit-Status 0 (6,1 min, Probelauf Lauf 1 unter Linux 2,1 min). Ausgabe: „Prüfsummenliste geschrieben: Pruefsummen_Abgabe_2026-09-25.txt (98 Dateien)“. Das Archiv führt 100 Einträge, der Lauf 98: ohne die drei Dokumente der Blindinstanz (Prompt, Rückfragenprotokoll, Übergabeprotokoll), dazu die Windows-Steuerung. Das Kennzahlenskript prüft die Ergebnisdatei gegen diese Liste (Abschnitt 8 G).

## 8 Vergleich mit dem archivierten Paket

Befehl (aus `Bachelorarbeit`):

```
"<Python>" Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Vergleich_2026-10-01.py "<S>/repro_B" --rscript "<Rscript>"
```

Ausgabe in `<S>\repro_B\vergleich\` (erste Fassung, Status 1, 31 offene Punkte). Zwei Fehler des Vergleichsskripts unter Windows (Befunde 8 und 9, Abschnitt 10) wurden nicht umgangen, sondern als zweite und dritte Fassung mit Datum und Grund im Kopf behoben (`Reproduktion_Vergleich_2026-10-01_Fassung2.py`, `…_Fassung3.py`, Unterschiede in `…_Fassung2_Diff.txt` und `…_Fassung3_Diff.txt`, erste Fassung unverändert, SHA-256 wie im Prompt). Beide Fassungen liefen in eigene Ausgabeordner (`vergleich_F2`, `vergleich_F3`). Die Abschnitte A bis D und G sind in allen drei Fassungen zeichengleich (geprüft mit `diff`), die Fassungen unterscheiden sich nur in E, in den Folgezeilen von F und im Urteil. Maßgeblich ist die dritte Fassung (`vergleich_F3\Vergleich_Protokoll.txt`, Status 0):

**A Bestand:** Archiv 101 Dateien, Lauf 99, gemeinsam 98. Nur im Archiv: `Prompt_Projektsitzung_Phase6_2026-09-25.md`, `Rueckfragenprotokoll_2026-09-25.md`, `Uebergabeprotokoll_2026-09-25.md` (Dokumente der Blindinstanz, erwartet). Nur im Lauf: `Gesamtlauf_Windows_2026-10-01.R` (Steuerung des Laufs, erwartet). Keine fremde Datei im Laufordner.

**B Ergebnisdatei:** Archiv 3194a805…, Lauf 08fdc3f3…, verschieden. Kennungen Archiv 3.559, Lauf 3.559, Wert, Einheit, Grund und Skript identisch in 3.558. Nicht identisch je Skript: S10_Messguete_2026-09-25.R 1. Größte Abweichung nach dem Maßstab von G.3 (Betrag der Differenz, bezogen auf max(1, Betrag a), das Vergleichsskript nennt die Spalte rel_Abweichung): S10.TELO.Z05.POST.ALL.X 6,94 · 10⁻¹⁸ (`Vergleich_Kennungen.csv`, Abschnitt 6).

**C Abgleich nach Spezifikation G.3** mit `Abgleich_2026-09-25.R` der Abgabe (Datei 1 Archiv, Datei 2 Lauf), Status 0, `Abgleich_Reproduktion.csv` und `_Protokoll.txt`: gemeinsame Kennungen 3.559, nur in einer Datei 0.

| Klasse | Kennungen | bestanden | Abweichung | nachrichtlich |
|---|---:|---:|---:|---:|
| EXAKT | 1.801 | 1.801 | 0 | 0 |
| DETERM | 1.714 | 1.714 | 0 | 0 |
| ITERATIV | 23 | 23 | 0 | 0 |
| ZUFALL | 6 | 6 | 0 | 0 |
| NACHRICHT | 15 | 0 | 0 | 15 |

„Urteil: bestanden. Keine Abweichung außerhalb der Toleranzen von G.3.“ Je Schritt S01 bis S19 Abweichungen 0. Die sechs ZUFALL-Kennungen (Bootstrap-Grenzen S19) sind nicht nur innerhalb der Toleranz, sondern zeichengleich (Abschnitt B), wie bei gleichem Generator und Startwert erwartet.

**D Validierung im Lauf:** Referenztests 83 Sollwerte, bestanden 83, nicht bestanden 0 · Grenzfälle 114 Fälle, bestanden 114, nicht bestanden 0 · „Urteil: Validierung bestanden, Studiendaten wurden gerechnet.“

**E Weitere Dateien** (Text mit angeglichenen Zeilenenden, sonst Bytes): bytegleich 25 (die 25 R-Skripte aus dem ZIP). Verschieden und erklärt: sechs Grafiken S14 (Schrift und Rendering plattformabhängig, Sichtprüfung in Abschnitt 6) · 12 `.csv` unter `Zwischen` nur Zeilenenden · 28 `.rds` Bytes verschieden, Inhalt identisch (elementweise in R, `readRDS` und `identical`) · `Zwischen/S10_ergebnisse.rds` Bytes verschieden, Inhalt gleich bis 1e-9 (die eine Kennung aus Abschnitt 6, als Text mit 17 Ziffern gespeichert, eigene Prüfung `S10_ergebnisse_rds_Pruefung.txt`: 238 Zeilen, 5 Spalten, genau eine Zelle verschieden, nach Ausblenden dieser Zelle `identical()` TRUE). Die Byteunterschiede der `.rds` kommen aus dem gzip-Kopf (Betriebssystemkennung) bei gleichem Inhalt, wie im Prompt erwartet. Reichweite der dritten Fassung: Der numerische Textvergleich gilt für jede Textzelle jeder `.rds`, die in beiden Dateien als Zahl lesbar ist, in diesem Lauf nur für die Spalte Wert der 19 `*_ergebnisse.rds`, die Abschnitt B ohnehin zeichengenau vergleicht. Reine Darstellungsunterschiede innerhalb der Toleranz (etwa `1.0` gegen `1`) würden in E nicht gemeldet.

**F Textausgaben** (`.txt`, nach Maskierung von Zeitstempeln, Laufdauern und Pfaden): Referenztests, Grenzfälle und S01 bis S19 je 4 Unterschiede, unerklärt 0, nämlich die drei Warnzeilen zur Spracheinstellung am Anfang und die Versionszeile „R version 4.3.3 (2024-02-29 ucrt)“ statt „(2024-02-29)“ (Diff ohne Maskierung: dazu nur Start und Ende als Zeitstempel). S10 5 Unterschiede, davon 1 „nur Zahlen bis 1e-9“ (die Zeile der Kennung S10.TELO.Z05.POST.ALL.X). Validierungsprotokoll 8 (zweimal die vier aus Referenztests und Grenzfällen). Laufprotokoll 81 Unterschiede, unerklärt 0: Aufrufbefehl, Steuerungszeilen W3 und W4, Rechenumgebung mit „ucrt“, fehlende vier Zeilen „nur dokumentiert, nicht gelesen“, Laufdauern, Prüfsummen der Textausgaben, der Ergebnisdatei (Abgleich bestanden), der Grafiken und der `.rds`. Prüfsummenliste Einträge Archiv 100, Lauf 98, unerklärt 0. Umgebungsdatei nicht gewertet (Abschnitt 6).

**G Kennzahlenblatt aus der neuen Ergebnisdatei** (`Kennzahlen_2026-09-25.py` auf den Laufordner B, Status 0, `Kennzahlen_Reproduktion.md`, `_Werte.csv`, `.txt`): Weil die Ergebnisdatei nicht bytegleich ist, gilt der zweite Maßstab des Prompts. `Kennzahlen_2026-09-25.md` gleich bis auf die Prüfsumme der Quelle (einziger Unterschied im `diff`: Zeile 7, SHA-256 08fdc3f3… statt 3194a805…), `Kennzahlen_2026-09-25_Werte.csv` Darstellung gleich, Rohwerte gleich bis 1e-9, Zeilen mit anderen Rohwerten 1 (K-05.1 Messgüte Sprint 5 m, Rohwert S10.TELO.Z05.POST.ALL.X in der 17. signifikanten Ziffer, Darstellung „0,040 [0,032 bis 0,051] (n = 25)“ unverändert). Damit ist jede Zahl des Manuskripts aus der Windows-Rechnung reproduziert. Hinweis: Die Kopfzeilen der `Kennzahlen_Reproduktion.md` (Datum 25.09., Quellpfad der Blindrechnung, Satz zur Gegenprobe) sind Vorlagentext des Kennzahlenskripts, berechnet ist dort nur die Prüfsumme der Quelle, die Herkunft aus Lauf B steht in `Kennzahlen_Reproduktion.txt`. Die Datei ist Beleg, nicht Ersatz für das Kennzahlenblatt.

**Urteil des Vergleichsskripts:** erste Fassung „NICHT bestanden oder Unterschiede zu erklären“, 31 offene Punkte, alle Folge des Pfadfehlers in E (Befund 8) · zweite Fassung 2 offene Punkte, Folge des Textvergleichs in E (Befund 9) · dritte Fassung „Offene Punkte: keine. Urteil: Reproduktion bestanden.“

**Zeilenenden:** Die Kette schreibt die Ergebnisdatei im Binärmodus mit LF, sie ist deshalb auch unter Windows bis auf die eine Kennung byteweise gleich (241.822 B in beiden Dateien). Die Textausgaben und die `.csv` unter `Zwischen` entstehen über Textverbindungen und tragen unter Windows CRLF (Prompt: zu erwarten, nur zu benennen). Zahlen dazu in Abschnitt 14.

## 9 Wiederholungslauf B2 auf demselben Rechner

Aufbau mit demselben Skript nach `<S>\repro_B2` (bestanden, 16:33 Sitzungsuhr). Ein erster, vom Werkzeug abgekoppelter Start um 15:33:52 UTC scheiterte („setsid: command not found“), kein Prozess, Laufordner unberührt (Befund 11). Danach Start wie Lauf B im Hintergrund: 15:52:37 UTC bis 16:11:23 UTC, Exit-Status 0, Dauer 18,7 min, teils parallel zu Prüfsummenskript und Vergleich auf einem Rechner mit acht Kernen. Validierung 83 von 83 und 114 von 114, keine Warnungen, Ergebnisdatei SHA-256 08fdc3f3…, bytegleich mit Lauf B. Das Prüfsummenskript lief in B2 nicht.

Vergleich B gegen B2 (`vergleich_B_B2.py`, Ausgabe `Vergleich_B_B2.txt`): Lauf B 99 Dateien, B2 98 (ohne Prüfsummenliste), gemeinsam 98. Bytegleich 74: die 25 R-Skripte, die Windows-Steuerung, die Ergebnisdatei, alle 41 Zwischendateien einschließlich der 29 `.rds`, die sechs Grafiken S14. Gleich nach Maskierung von Zeitstempeln, Laufdauern und Pfaden 24 Textdateien (das Laufprotokoll dazu bis auf die Prüfsummen der Textdateien, die ihre Zeitstempel enthalten). Verschieden 0. Unter Windows schreibt die Kette also von Lauf zu Lauf dieselben Bytes, auch in `.rds` und PNG. Die Byteunterschiede zum Archiv (Abschnitt 8 E) stammen aus der Plattform, nicht aus dem einzelnen Lauf.

## 10 Befundliste

| Nr. | Befund | Beleg | Folge | Ort der Änderung |
|---|---|---|---|---|
| 1 | Das archivierte Paket läuft unter Windows nicht ohne Anpassung der Steuerung: `Gesamtlauf_2026-09-25.R` bricht beim ersten Kindprozess ab (Referenztests Status 5), keine Rechnung, keine Ergebnisdatei. Ursache: `system2()` setzt unter Windows die Angaben aus `env =` in die Befehlszeile, das Rscript-Frontend nimmt `LC_ALL=C.UTF-8` als Skriptdatei. Ohne `env =` läuft derselbe Aufruf (T2). | `LaufA_Laufprotokoll`, `LaufA_Konsole`, `Tests_system2_Ergebnis.txt` (T1, T2, T5), `deparse(system2)` in `Umgebung_Sitzung_R.txt` | Befund für Anhang G (Task 16): Hinweis zur Ausführung unter Windows, Klickfrage (a) | Anhang G, keine Änderung an der Abgabe |
| 2 | Die Erscheinungsform des Abbruchs weicht vom Vermerk ab: statt Status 2 mit „Fatal error: cannot open file 'LC_ALL=C.UTF-8'“ endet R 4.3.3 (ucrt) für Windows beim Start mit einer Zugriffsverletzung (0xC0000005, von `system2()` als Status 5 gemeldet, in Git Bash „Segmentation fault“ 139), wenn die mit `--file=` übergebene Datei nicht geöffnet werden kann, über `Rscript.exe` wie über `Rterm.exe`, bevor eine Meldung geschrieben ist. Das gilt für jede nicht vorhandene Skriptdatei (T9, Direktaufrufe). `system2()` meldet unter Windows die unteren 16 Bit des Prozessendes. | `Tests_system2_Ergebnis.txt` (T1, T3, T4, T9), `Tests_GitBash_Direkt_Ergebnis.txt` (Direktaufrufe, Rterm, cmd exit), `Tests_status_Ergebnis.txt`, Posit Community „Rscript leading to Segmentation fault“ (https://forum.posit.co/t/rscript-leading-to-segmentation-fault/191559, R 4.4.0 unter Git Bash, nennt nebenbei den falschen Dateinamen als Auslöser desselben Segmentation fault) | Vermerk („Erwartete Abbrüche“ Nr. 1) und Prompt (§ 2 Nr. 4) treffen unter Windows in diesem Punkt nicht zu, Anhang G formuliert nach diesem Protokoll. Verhalten dieser R-Fassung, nicht der Kette | dieses Protokoll, Vormerkung Task 16. Vermerk und Prompt bleiben als Dokumente ihres Stands unverändert |
| 3 | Vorprobe: GNU sha256sum maskiert den von R mit Backslash übergebenen Pfad und stellt der Prüfsumme `\` voran. G18 des unveränderten Pakets kann unter Windows nicht bestehen (bestätigt Vermerk Nr. 3). | `LaufA_Vorprobe_sha256sum.txt`, Sollwert aus `Pruefsummen_Abgabe_2026-09-25.txt` des Archivs | W4 ist nötig und ausreichend (Befund 5) | keine |
| 4 | `Sys.setlocale("LC_ALL", "C.UTF-8")` in `Funktionen_2026-09-25.R` wird von Windows abgelehnt. Jeder Prozess warnt einmal („OS reports request to set locale to "C.UTF-8" cannot be honored“, im Elternprozess auf Deutsch), R bleibt bei `German_Germany.utf8` mit UTF-8 und rechnet unverändert (Validierung und Abgleich bestanden). | `Umgebung_Sitzung_R.txt`, Kopf jeder Schrittausgabe in Lauf B, Vergleich F unerklärt 0 | Hinweis für Anhang G: Die Warnung ist unter Windows zu erwarten und ohne Folge. Die Zählung „Warnungen 0“ der Steuerung betrifft nur Zeilen mit „WARNUNG:“ | keine (Rechenskripte bleiben unverändert) |
| 5 | Die Windows-Steuerung `Gesamtlauf_Windows_2026-10-01.R` (W1 bis W4, sonst nichts, eigener Diff hunk-identisch mit der mitgelieferten Diff-Datei) besteht unter Windows: Gesamtlauf ohne Abbruch, 21 Kindprozesse Status 0, Validierung 83 von 83 und 114 von 114, G18 über `sha256sum.cmd` (W4) 13 von 13, Umgebungsdatei nach W2, Laufprotokoll mit W3. Start aus Git Bash ist nötig (sha256sum im PATH). | `LaufB_Laufprotokoll`, `LaufB_Validierungsprotokoll`, `LaufB_Umgebung`, `Lauf_Windows\LaufB_Konsole.txt` | Steuerung geprüft, Grundlage für Klickfrage (a) | Anhang G (Klick) |
| 6 | Ergebnisdatei unter Windows nicht bytegleich: genau eine von 3.559 Kennungen weicht ab, S10.TELO.Z05.POST.ALL.X um eine Binärstelle (6,9 · 10⁻¹⁸ absolut und nach dem Maßstab von G.3, gewöhnlich relativ 2,1 · 10⁻¹⁶, `te * sqrt(df / qchisq(p, df))`, Mathematikbibliothek UCRT statt glibc). Abgleich nach G.3 ohne Abweichung in allen Klassen, Kennzahlenblatt in der Darstellung gleich, Rohwerte gleich bis 1e-9. Alle übrigen 3.558 Werte zeichengleich, darunter ANCOVA, Bootstrap und Poweranalyse. | Vergleich B, C, G, `Vergleich_Kennungen.csv`, `LaufB_Analyse_Kennungen_eigene_Durchsicht.txt`, `LaufB_S10_ergebnisse_rds_Pruefung.txt` | Erwarteter Fall („letzte Stellen von Gleitkommazahlen“), keine Folge für das Manuskript. Hinweis für Anhang G: unter Windows bis auf eine Binärstelle einer Kennung gleich | keine |
| 7 | Laufzeit unter Windows: Gesamtlauf 20,3 min (Linux: Blindrechnung vom 25.09. 6,4 min, Probelauf Lauf 2 7,1 min), Prüfsummenskript 6,1 min (Probelauf Lauf 1 2,1 min), Kindprozesse 32 bis 64 s je Schritt (Linux 9 bis 22 s). Treiber ist die SHA-256-Berechnung in reinem R. | Laufprotokolle, `LaufB_Zeiten`, `LaufB_Zeiten_Pruefsummen` | Hinweis zur Ausführung in Anhang G (Dauer), Werkzeughinweis für künftige Sitzungen: Läufe im Hintergrund starten | Anhang G Hinweis |
| 8 | Vergleichsskript, erste Fassung, Abschnitt E: Der Aufruf von Rscript mit den 58 Pfaden der `.rds`-Dateien als Argumente scheitert unter Windows an „command line too long“ (R-Status 27, rund 11.400 Zeichen allein für die 58 Pfade nach der Größe der Listendatei der dritten Fassung, die Befehlszeile der ersten Fassung mit Anführungszeichen und Trennzeichen entsprechend länger). Folge: alle 29 `.rds` „nicht geprüft“, dazu ihre 58 Prüfsummenzeilen im Laufprotokoll und 29 in der Prüfsummenliste „unerklärt“, 31 offene Punkte, Urteil „NICHT bestanden“. | `Vergleich_Fassung1_Protokoll.txt` | Korrektur als zweite Fassung: Pfade über eine Listendatei `rds_liste.txt`, sonst unverändert | neu `Reproduktion_Vergleich_2026-10-01_Fassung2.py` mit `_Fassung2_Diff.txt`, erste Fassung unverändert |
| 9 | Vergleichsskript, zweite Fassung, Abschnitt E: Die elementweise R-Prüfung vergleicht Textspalten nur mit `identical()`. In den `*_ergebnisse.rds` steht der Wert als Text mit 17 Ziffern, deshalb meldet sie `S10_ergebnisse.rds` als „VERSCHIEDEN“, obwohl die einzige abweichende Zelle nach DETERM gleich ist. Folge: 2 offene Punkte. | `Vergleich_Fassung2_Protokoll.txt`, `LaufB_S10_ergebnisse_rds_Pruefung.txt` | Korrektur als dritte Fassung: Zellen, die in beiden Dateien als Zahl lesbar sind, nach DETERM, alle übrigen identisch. Dritte Fassung: keine offenen Punkte, „Reproduktion bestanden“. Reichweite des neuen Zweigs in Abschnitt 8 E | neu `Reproduktion_Vergleich_2026-10-01_Fassung3.py` mit `_Fassung3_Diff.txt` |
| 10 | Erwartete und benannte Unterschiede ohne Folge: CRLF in den Textausgaben und den `.csv` unter `Zwischen` · `.rds` byteverschieden bei identischem Inhalt (gzip-Kopf) · sechs Grafiken S14 mit anderem Schriftbild und kleinerer Datei bei gleichem Inhalt · Versionszeile mit „ucrt“ · zwei Zusatzzeilen W3 und W4 im Laufprotokoll · vier fehlende Zeilen „nur dokumentiert, nicht gelesen“ (Spezifikation und Auswertungsverfahren nicht im Eingangsordner, die Kette liest sie nicht) · Umgebungsdatei nach W2 · `La_library()` leer (eingebautes BLAS/LAPACK 3.11.0 statt 3.12.0 der Ubuntu-Pakete). | Vergleich E und F, Abschnitt 6 | keine | keine |
| 11 | Werkzeug der Sitzung: `setsid` fehlt in dieser Git Bash, der erste abgekoppelte Start des Wiederholungslaufs B2 scheiterte ohne Spur im Laufordner. Das Zeitlimit des Bash-Werkzeugs greift bei Hintergrundläufen nicht (Lauf B 20,3 min). | `LaufB2_Zeiten.txt` | B2 später auf demselben Weg wie B gestartet (Abschnitt 9) | keine |
| 12 | Abschlussprüfung des Projektordners `Claude\03_Skripte\Abgabe_R_2026-09-25\` gegen seine Prüfsummenliste: 94 von 100 Prüfsummen stimmen, die sechs Grafiken S14 weichen ab. Ursache vorbekannt und im Kopierprotokoll vom 25.09. dokumentiert (`03_Skripte\Abgabe_Kopie_2026-09-25.txt`): Der Dateitransfer fügt PNG-Dateien beim Schreiben auf den Rechner den Chunk `caBX` (C2PA-Herkunftsangabe) ein, deshalb wurde am 25.09. das ZIP als prüfsummenexakte Referenz angelegt. Eigene Prüfung: Chunkfolge im Projektordner `IHDR, caBX, pHYs, IDAT…`, im ZIP ohne `caBX`, Pixelinhalt gleich (Pillow, 0 verschiedene Pixel), Dateidatum 25.09. 13:42, also vor dieser Sitzung (erste Ordnerliste dieser Sitzung zeigt dieselben Größen). Gleiches gilt für die Kopien in `06_Abbildungen\Anhang_G`. | `Abgabe_Kopie_2026-09-25.txt`, `LaufB_PNG_Chunk_Pixel_Pruefung.txt` mit `.py` (Chunks, Pixel, Zeitstempel) | Keine Folge für den Test, der aus dem ZIP aufgebaut wurde. Hinweis zu Klickfrage (b): Das ZIP ist die zu schützende Referenz, der Ordner die lesbare Kopie | keine |

## 11 Urteil

Nach dem vorab festgelegten Maßstab (Prompt § 4):

- Validierung bestanden: Referenztests 83 von 83, Grenzfälle 114 von 114. ✓
- Abgleich nach G.3 ohne Abweichung: EXAKT 1.801, DETERM 1.714, ITERATIV 23, ZUFALL 6 bestanden, NACHRICHT 15, Abweichungen 0. ✓
- Kennzahlenblatt: Ergebnisdatei nicht bytegleich, deshalb zweiter Maßstab: `.md` gleich bis auf die Prüfsumme der Quelle, `_Werte.csv` in der gerundeten Darstellung gleich, Rohwerte nach DETERM gleich (eine Zeile, 17. signifikante Ziffer). ✓
- Jeder Unterschied erklärt: eine Kennung in der letzten Binärstelle, Zeilenenden, gzip-Köpfe der `.rds`, Grafikrendering, Versionszeile, Warnung zur Spracheinstellung, Steuerungszeilen. Das Vergleichsskript in der dritten Fassung meldet keine offenen Punkte. ✓

**Der Reproduktionstest unter Windows ist bestanden.** Jede Zahl des Manuskripts ist auf diesem Windows-Rechner mit R 4.3.3 aus dem Paket neu entstanden. Einschränkung, die der Leser von Anhang G kennen muss: Das archivierte Steuerskript selbst läuft unter Windows nicht (Befund 1), gerechnet hat die Windows-Steuerung mit den Änderungen W1 bis W4 bei unveränderten Rechenskripten. Lauf A ist damit ein Befund für Anhang G, Lauf B der bestandene Reproduktionstest.

## 12 Abweichungen von Plan Task 16 d

Plan Task 16 d sieht eine frische Claude-Sitzung außerhalb des Projekts vor, nur mit `Abgabe_R_2026-09-25.zip`, neuem Gesamtlauf, Prüfsummenvergleich der Ergebnisdatei und Reproduktionsprotokoll. Abweichungen dieses Laufs, wie im Prompt § 5 vorgesehen:

1. **Sitzung im Projektordner** statt außerhalb: Arbeitsverzeichnis `Bachelorarbeit`, gerechnet wurde aber ausschließlich in `<S>` außerhalb von OneDrive, der Projektordner wurde nur gelesen (Aufbau) und am Ende mit den Belegen beschrieben (Abschnitt 14).
2. **Eingang aus dem ZIP und dazu Datenstand und Anlagen:** Das ZIP enthält den Datenstand und die sieben Anlagen nicht, die Kette braucht sie (`Funktionen_2026-09-25.R` erwartet sie im übergeordneten Ordner). Beide kamen aus `Statistik\Datenstand_2026-09-24` und `Claude\02_Befunde`, jede Datei per SHA-256 gegen ihre Sollliste geprüft (Abschnitt 3).
3. **Vorhandene R-Installation:** R 4.3.3 war am 01.10. vom Verfasser installiert worden, die Sitzung hat nichts installiert.
4. **Kenntnis des Probelaufs:** Der Vermerk vom 01.10. (Linux) war Eingang dieses Tasks. Der Vergleich ist maschinell (Vergleichsskript, Abgleichskript der Abgabe, Kennzahlenskript), das Vorwissen ändert sein Ergebnis nicht. Wo das Vorwissen nicht zutraf (Erscheinungsform des Abbruchs in Lauf A), steht es als Befund.
5. **Steuerung:** Gerechnet hat die Windows-Steuerung `Gesamtlauf_Windows_2026-10-01.R` (W1 bis W4), nicht das archivierte `Gesamtlauf_2026-09-25.R`, weil dieses unter Windows abbricht (Lauf A). Die 24 Rechen-, Funktions- und Validierungsskripte liefen unverändert mit den Prüfsummen der Abgabe.
6. **Wiederholungslauf B2:** Ein zweiter, identisch aufgebauter Windows-Lauf war als Sicherung gegen das Zeitlimit des Werkzeugs gedacht (erster Start 15:33 UTC gescheitert, Befund 11) und lief nach dem Ende von Lauf B als Wiederholungslauf auf demselben Rechner (Abschnitt 9). Der Prompt sieht ihn nicht vor, er ändert am Vergleich mit dem Archiv nichts und zeigt nur, ob die Kette unter Windows von Lauf zu Lauf dieselben Bytes schreibt.

## 13 Klickfragen

Empfehlung jeweils zuerst.

**(a) Anhang G, Ausführung unter Windows (Task 16):**
- *Empfehlung:* Die archivierte Steuerung `Gesamtlauf_2026-09-25.R` bleibt unverändert im Abgabepaket. Die geprüfte Windows-Steuerung `Gesamtlauf_Windows_2026-10-01.R` kommt als eigene Datei daneben, mit Hinweis zur Ausführung: unter Windows aus Git Bash starten, weil Grenzfall G18 GNU sha256sum braucht, Laufzeit etwa 20 min, Ergebnisdatei bis auf eine Binärstelle einer Kennung gleich, Abgleich nach G.3 ohne Abweichung. Lauf B hat diese Steuerung unter Windows bestanden. Ihr Windows-Zweig rechnete unter Linux bytegleich mit dem Original (Probelauf Lauf 2, Testkopie mit erzwungenem Windows-Zweig), ihr Linux-Zweig ist bisher nicht gelaufen. Vor der Beilage zu Anhang G die Datei einmal unter Linux starten (rund 7 min), damit beide Zweige belegt sind.
- Alternative: nur ein Hinweis in Anhang G, dass das Paket unter Linux (Ubuntu 24.04, R 4.3.3) läuft und unter Windows die Steuerung anzupassen ist (W1 bis W4), ohne die Datei beizulegen.

**(b) Schreibschutz:** Abgabeordner `Claude\03_Skripte\Abgabe_R_2026-09-25\` und `Abgabe_R_2026-09-25.zip` vom Verfasser schreibgeschützt setzen lassen (Empfehlung: ja, Attribut „Schreibgeschützt“ auf Ordner mit Inhalt und auf das ZIP, danach SHA-256 des ZIP erneut 200b2595…). Das ZIP ist die prüfsummenexakte Referenz, der Ordner trägt in den sechs PNG den Transfer-Chunk (Befund 12). Alternative: so lassen, die Prüfsummen bleiben der Maßstab.

**(c) Unerklärte Unterschiede:** keiner offen, deshalb keine Klickfrage. Zur Kenntnis: Die eine Abweichung in der letzten Binärstelle (Abschnitt 6) ist erklärt und liegt rund acht Größenordnungen unter der Toleranz DETERM (1e-9 gegen 6,9 · 10⁻¹⁸), das Kennzahlenblatt ist in der Darstellung gleich.

**Entscheidung des Verfassers (01.10., Klick nach der Zweitprüfung):** (a) Windows-Steuerung beilegen, wie empfohlen, mit vorherigem Lauf des Linux-Zweigs. (b) Schreibschutz ja, wie empfohlen, als Verfasserschritt offen. (c) entfällt.

**(d) Vermerk und Prompt berichtigen (Vorschlag, kein Klick nötig):** Der Satz zur erwarteten „Fatal error“-Zeile in `Referenztests_2026-09-25.txt` (Vermerk, Abschnitt „Erwartete Abbrüche“ Nr. 1, und Prompt § 2 Nr. 4) trifft unter Windows nicht zu (Abschnitt 5). Der Vermerk bleibt als Dokument des Probelaufs unverändert, dieses Protokoll hält die Berichtigung fest, Anhang G formuliert nach diesem Protokoll.

## 14 Ablage, Dateien, Zeilenenden

**Zeilenenden (Bytes, gezählt mit Python):**

| Datei | Archiv (Linux) | Lauf B (Windows) |
|---|---|---|
| `Ergebnisse_R_2026-09-25.csv` | 0 CRLF, 3.560 LF, 241.822 B | 0 CRLF, 3.560 LF, 241.822 B (Binärmodus, byteweise gleich bis auf die eine Kennung) |
| `S01_Einlesen_2026-09-25.txt` | 0 CRLF, 61 Zeilen, 3.313 B | 64 CRLF (61 Zeilen und drei Warnzeilen), 3.505 B |
| `Laufprotokoll_2026-09-25.txt` | 168 LF, 16.004 B | 167 CRLF, 16.104 B |
| `Zwischen\S02_versuche.csv` | 1.117 LF, 70.533 B | 1.117 CRLF, 71.650 B |
| `S01_Einlesen_2026-09-25.R` (aus dem ZIP) | 214 LF, 12.929 B | 214 LF, 12.929 B (bytegleich) |

**Protokoll:** `Claude\02_Befunde\Reproduktionsprotokoll_2026-10-01.md`, dazu `.docx` und `.pdf` im Hausstil (`Werkzeug_Hausstil_2026-09-25.py` unverändert, gestartet über `Reproduktion_2026-10-01\Protokoll_Hausstil_Lauf_2026-10-01.py`, das den fehlenden `soffice`-Aufruf auf den PDF-Export von Word umleitet, wie bei der Objektprüfung vom 01.10.).

**Neu in `Claude\03_Skripte\Reproduktion_2026-10-01\`:** `Reproduktion_Vergleich_2026-10-01_Fassung2.py` mit `_Fassung2_Diff.txt` · `Reproduktion_Vergleich_2026-10-01_Fassung3.py` mit `_Fassung3_Diff.txt` · `Protokoll_Hausstil_Lauf_2026-10-01.py` · Ordner `Lauf_Windows\` mit 60 Belegdateien und der Liste `Ablage_Liste.txt` (SHA-256 je Datei), flach:

- Umgebung und Tests der Sitzung: `Umgebung_Sitzung_R.txt` und `.R`, `Tests_system2_Ergebnis.txt` mit `Tests_system2.R` und `Tests_system2_hallo.R`, `Tests_status_Ergebnis.txt` mit `Tests_status.R` und `Tests_status2.R`, `Tests_GitBash_Direkt_Ergebnis.txt` mit `Tests_GitBash_Direkt.sh` (nach der Zweitprüfung erneut ausgeführt)
- Lauf A: `LaufA_Aufbau_Protokoll.txt`, `LaufA_Vorprobe_sha256sum.txt`, `LaufA_Konsole.txt`, `LaufA_Zeiten.txt`, `LaufA_Laufprotokoll_2026-09-25.txt`, `LaufA_Referenztests_2026-09-25.txt` (0 Byte)
- Lauf B: `LaufB_Aufbau_Protokoll.txt`, `LaufB_Konsole.txt`, `LaufB_Zeiten.txt`, `LaufB_Konsole_Pruefsummen.txt`, `LaufB_Zeiten_Pruefsummen.txt`, `LaufB_Laufprotokoll_2026-09-25.txt`, `LaufB_Umgebung_2026-09-25.txt`, `LaufB_Validierungsprotokoll_2026-09-25.txt`, `LaufB_Pruefsummen_Abgabe_2026-09-25.txt`, `LaufB_Ergebnisse_R_2026-09-25.csv` (abgelegt, weil nicht bytegleich), `LaufB_Analyse_Kennungen_eigene_Durchsicht.txt` mit `.py`, `LaufB_S10_ergebnisse_rds_Pruefung.txt` mit `.R`, `LaufB_PNG_Chunk_Pixel_Pruefung.txt` mit `.py`, die sechs Grafiken `LaufB_S14_*.png`
- Vergleich (dritte Fassung, maßgeblich): `Vergleich_Protokoll.txt`, `Vergleich_Kennungen.csv`, `Abgleich_Reproduktion.csv`, `Abgleich_Reproduktion_Protokoll.txt`, `Kennzahlen_Reproduktion.md`, `Kennzahlen_Reproduktion_Werte.csv`, `Kennzahlen_Reproduktion.txt`, `Vergleich_rds_vergleich.R`, `Vergleich_rds_liste.txt`, `Vergleich_Konsole.txt`, dazu `Vergleich_Fassung1_Protokoll.txt`, `Vergleich_Fassung1_Konsole.txt`, `Vergleich_Fassung2_Protokoll.txt`, `Vergleich_Fassung2_Konsole.txt`
- Wiederholungslauf B2: `LaufB2_Aufbau_Protokoll.txt`, `LaufB2_Konsole.txt`, `LaufB2_Zeiten.txt`, `LaufB2_Laufprotokoll_2026-09-25.txt`, `LaufB2_Umgebung_2026-09-25.txt`, `LaufB2_Validierungsprotokoll_2026-09-25.txt`, `LaufB2_Vergleich_mit_LaufB.txt` mit `.py`

Keine Datenprüfung abgelegt, weil das Workbook die Prüfsumme der Datenprüfung vom 01.10. trägt (Abschnitt 1).

**Unverändert geblieben** (nach Abschluss erneut per SHA-256 geprüft, Abschnitt 1 Tabelle): `Abgabe_R_2026-09-25.zip` (200b2595…) und `Claude\03_Skripte\Abgabe_R_2026-09-25\` (Dateidaten 25.09. 13:41 bis 13:43, 94 von 100 Prüfsummen stimmen, die sechs PNG tragen den seit dem 25.09. dokumentierten Transfer-Chunk `caBX`, Befund 12), der Ordner `Statistik` mit Workbook (86087d35…) und Datenstand, die Anlagen der Spezifikation, Kennzahlenblatt, Objekte, Master, die vier Werkzeuge des Prompts (erste Fassungen), der Vermerk zum Probelauf. Kein Skript der Abgabe wurde geändert. Keine Zahl von Hand.

**Sitzung:** Claude Code (Fable 5.1), 01.10.2026, Beginn 16:16 Sitzungsuhr, Protokoll geschrieben 19:16 Sitzungsuhr. Zweitprüfung durch Subagenten ohne Beteiligung am Protokoll: Abschnitt 15.

**Quellen:** R 4.3.3, `src/library/base/R/windows/system.R` (nach dem Vermerk, am laufenden R mit `deparse(system2)` bestätigt), Absturz beim Start von R für Windows bei nicht lesbarer `--file=`-Datei (eigene Prüfung, `Rscript.exe` und `Rterm.exe`, Abschnitt 5) · Posit Community, „Rscript leading to Segmentation fault“, https://forum.posit.co/t/rscript-leading-to-segmentation-fault/191559 (R 4.4.0 unter Git Bash, intermittierender Segmentation fault aus Make heraus, nebenbei: ein falscher Dateiname löst denselben Fehler aus) · GNU coreutils 8.32, sha256sum, Maskierung von Dateinamen mit Backslash.

## 15 Zweitprüfung und Umgang je Befund

**Verfahren:** Nach dem ersten vollständigen Stand des Protokolls (17:15 Sitzungsuhr) prüfte ein Workflow aus Subagenten ohne Beteiligung am Protokoll sechs Dimensionen unabhängig voneinander: Aufbau gegen ZIP, Datenstand und Anlagen (13 Prüfungen) · Unterschied der Steuerung und der Werkzeugfassungen (14) · Ergebnisdatei je Kennung mit eigener Implementierung ohne Abgleich- und Vergleichsskript (15) · Stichproben im Kennzahlenblatt (12) · jede Aussage des Protokolls am Material (22) · Ursachenanalyse zu Lauf A mit eigener Nachstellung (21). Jeden gemeldeten Befund prüften drei weitere Agenten mit dem Auftrag, ihn zu widerlegen (Linsen Korrektheit am Material, Relevanz für das Urteil, alternative Erklärung), bestätigt galt ein Befund, wenn mindestens zwei ihn nicht widerlegen konnten. 99 Agenten, Dauer 77 min. Die Prüfer durften nichts verändern und haben nichts verändert (Hilfsdateien nur im Scratchpad).

**Bestätigt am Material:** ZIP 200b2595… mit 871.200 B und 101 Dateien, 100 von 100 Prüfsummen in eigener Entpackung · Datenstand und sieben Anlagen gleich dem Soll · die 25 R-Skripte im Laufordner B nach dem Lauf unverändert, Windows-Steuerung f58734b9… · eigener Diff der Steuerung zeichengleich mit der mitgelieferten Diff-Datei, alle drei Diff-Dateien der Werkzeuge erzeugen per `patch` bytegleich die Zieldateien, keine Änderung berührt den Rechenweg · eigene Implementierung des Abgleichs: 3.559 Kennungen, EXAKT 1.801, DETERM 1.714, ITERATIV 23, ZUFALL 6, NACHRICHT 15, außerhalb der Toleranz 0, Wert zeichengleich 3.558, die eine Abweichung mit Bitmuster bestätigt, Lauf B2 bytegleich · Kennzahlenblatt: alle 2.097 Rohwerte der 216 Zeilen zeichengleich mit der Ergebnisdatei des Laufs B, Rundung in 45 Zeilen nachgerechnet, keine Darstellungsabweichung · Statusabbildung von `system2()` mit acht Kontrollwerten, Windows-Ereignisprotokoll mit Ausnahmecode 0xc0000005 für Rscript.exe und Rterm.exe, Vorprobe nachgestellt · Umgebung, Zeiten, Prüfsummen, Zeilenenden und Ablage Zahl für Zahl belegt.

**Befunde:** 31 bestätigt (3 A, 16 B, 12 C), 0 verworfen. Keiner berührt Validierung, Abgleich, Kennzahlenblatt oder Urteil. Mehrfachmeldungen desselben Punkts sind zusammengefasst. Alle Korrekturen sind in diesem Protokoll eingearbeitet, die ursprünglichen Formulierungen stehen hier.

| Nr. | Prüfer | Schwere | Befund | Umgang |
|---|---|---|---|---|
| Z1 | aufbau, steuerung, ergebnisdatei, aussagen | A | Zählung der Zwischendateien: unter `Zwischen` liegen 12 `.csv` und 29 `.rds`, das Protokoll nannte in Abschnitt 6, 8 E und 9 „15 .csv“ und „26 .rds“ (Summe 41 stimmte). | Berichtigt an allen drei Stellen. Urteil unberührt, das Vergleichsskript weist jede der 41 Dateien einzeln aus. |
| Z2 | ergebnisdatei, kennzahlen, aussagen | B | „6,9 · 10⁻¹⁸ relativ“ ist der Betrag der Differenz, der nach G.3 auf max(1, Betrag a) = 1 bezogen denselben Wert ergibt. Gewöhnlich relativ sind es 2,1 · 10⁻¹⁶, eine Binärstelle bei 0,032. | Berichtigt in Abschnitt 6 (Tabelle), 8 B, Befund 6 und Klickfrage (c), Maßstab von G.3 jeweils benannt. |
| Z3 | steuerung, ergebnisdatei, aussagen | B | „sechs Größenordnungen unter der Toleranz DETERM“: 1e-9 gegen 6,9 · 10⁻¹⁸ sind rund acht. | Berichtigt in Klickfrage (c). |
| Z4 | lauf_a | B | Der Absturz ist nicht allein dem Rscript-Frontend zuzuordnen: `Rterm.exe` mit `--file=` auf eine nicht vorhandene Datei stürzt ebenso ab (0xC0000005), `bin\x64\Rscript.exe` lädt R.dll selbst, ein Rterm-Kindprozess entsteht nicht. Die Zeile „Rscript ruft Rterm.exe“ in Abschnitt 2 traf nicht zu. | Berichtigt in Abschnitt 2 (Zeile Rscript), Abschnitt 5 (Schluss), Befund 2 und Quellen. Eigene Nachstellung ergänzt: `Rterm.exe --file=gibt_es_nicht.R` und `--file=LC_ALL=C.UTF-8` je Status 139, Kontrolle mit vorhandener Datei 0 (`Tests_GitBash_Direkt_Ergebnis.txt`). |
| Z5 | aussagen, lauf_a | B | Die Direktaufrufe aus Git Bash und `cmd /c exit 3221225477` hatten keine Belegdatei, nur Konsolenausgabe dieser Sitzung. Werte von den Prüfern reproduziert. | Erneut ausgeführt und abgelegt: `Tests_GitBash_Direkt_Ergebnis.txt` mit `Tests_GitBash_Direkt.sh`, Belege in Abschnitt 5 und Befund 2 angepasst. |
| Z6 | aussagen | B | Die Chunk- und Pixelprüfung der sechs PNG (Befund 12) hatte keine Belegdatei. Aussagen von den Prüfern bestätigt. | Als Skript und Ausgabe abgelegt: `LaufB_PNG_Chunk_Pixel_Pruefung.py` und `.txt` (Projektordner, Anhang_G, ZIP, Lauf B, Zeitstempel), Befund 12 angepasst. |
| Z7 | lauf_a, aussagen | B | Die Posit-Quelle behandelt einen intermittierenden Segmentation fault aus Make heraus (R 4.4.0) und nennt den falschen Dateinamen nur nebenbei, „gleichlautend beschrieben“ war zu stark. | Enger gefasst in Abschnitt 5, Befund 2 und Quellen. |
| Z8 | steuerung | B | Klickfrage (a) sagte, die Windows-Steuerung „rechnet unter Linux wie das Original (Probelauf Lauf 2)“. Lauf 2 war der Windows-Zweig in einer Testkopie, der Linux-Zweig der Datei ist nie gelaufen. | Berichtigt, Empfehlung um einen Linux-Lauf vor der Beilage ergänzt, in die Vormerkung für Task 16 aufgenommen. |
| Z9 | lauf_a | B | Das Laufprotokoll von Lauf A führt 23 Skripte mit SHA-256 (ohne Abgleich und Prüfsummenskript), nicht 25. | Berichtigt in Abschnitt 5. |
| Z10 | aussagen | B | „11.424 Zeichen in der Pfadliste“ ist die Größe der Listendatei der dritten Fassung, nicht die gemessene Befehlszeile der ersten. | Umformuliert in Befund 8. |
| Z11 | aussagen | B | `.docx` und `.pdf` lagen zur Zeit der Prüfung nicht vor. | Nach der Einarbeitung erzeugt, Abschnitt 14 trifft damit zu. |
| Z12 | steuerung | C | Die dritte Fassung des Vergleichsskripts wertet jede beidseitig als Zahl lesbare Textzelle numerisch, Darstellungsunterschiede innerhalb der Toleranz blieben in E ungemeldet. In diesem Lauf betrifft das nur die Spalte Wert der 19 `*_ergebnisse.rds`, die Abschnitt B zeichengenau vergleicht. | Reichweite in Abschnitt 8 E und Befund 9 benannt, Skript unverändert. |
| Z13 | kennzahlen | C | Die Kopfzeilen der `Kennzahlen_Reproduktion.md` sind Vorlagentext des Kennzahlenskripts (Datum 25.09., Quellpfad der Blindrechnung, Satz zur Gegenprobe), nur die Prüfsumme ist berechnet. | Hinweis in Abschnitt 8 G, Datei bleibt als Beleg abgelegt. |
| Z14 | aufbau | C | „Datenstand 7 Dateien, gegen Pruefsummen.txt bestanden“: geprüft werden 6 Dateien, die Liste selbst ist über das Laufprotokoll des Archivs gedeckt (a125862c…). | Präzisiert in Abschnitt 3. |
| Z15 | aufbau | C | Im Werkzeugordner lag ein Ordner `__pycache__` aus der Syntaxprüfung (`py_compile`) der zweiten und dritten Fassung. | Entfernt (eigenes Artefakt dieser Sitzung), hier vermerkt. |
| Z16 | aussagen, lauf_a | C | Die Belegdatei der Vorprobe endet mit einem fehlgeschlagenen `grep`, weil die Prüfsummenliste nur im Archiv liegt. Der Sollwert 30c74291… stammt aus der Archivliste und dem Laufprotokoll A. | Abschnitt 4 und Befund 3 ergänzt. |
| Z17 | aussagen | C | `Lauf_Windows` enthielt 57 Dateien: 56 Belege und die Liste. | Präzisiert in Abschnitt 14 (nach der Zweitprüfung 60 Belegdateien und die Liste). |
| Z18 | aussagen | C | Befund 12 stand vor Befund 11. | Reihenfolge berichtigt. |
| Z19 | aussagen | C | Abschnitt 14 verwies auf einen Abschnitt 15, den es nicht gab. | Dieser Abschnitt. |
| Z20 | aussagen | C | Dateidaten des Abgabeordners reichen bis 13:43 (Zwischendateien), nicht nur bis 13:42. | Berichtigt in Abschnitt 14. |
| Z21 | aussagen | C | Die Linux-Vergleichswerte stammten ohne Angabe aus zwei Probeläufen (7,1 min und Schrittdauern aus Lauf 2, 2,1 min aus Lauf 1), die Blindrechnung selbst zeigt 6,4 min und 9 bis 18 s. | Quellen in Abschnitt 6, 7 und Befund 7 genannt. |
| Z22 | kennzahlen (Frage) | C | „17. Ziffer“ ist die 17. signifikante Ziffer (zugleich 18. Nachkommastelle). | Präzisiert in Abschnitt 6, 8 G und Urteil. |

**Hinweise der Prüfer ohne Änderung:** Das Maskierungsmuster in Abschnitt F des Vergleichsskripts (`warning`, `locale`, `OS reports`) erklärt jede Zeile mit diesen Wörtern, in diesem Lauf sind das nur die drei Warnzeilen je Schrittausgabe (Diff ohne Maskierung in Abschnitt 8 F), für künftige Läufe eine bekannte Grenze des Werkzeugs · Die abgelehnte Spracheinstellung lässt `LC_COLLATE` auf `German_Germany.utf8` statt `C`, Sortierungen könnten sich in anderen Daten unterscheiden, hier sind alle Ausgaben gleich, ein ausdrückliches `Sys.setlocale("LC_COLLATE", "C")` in der Windows-Steuerung wäre eine Änderung der Steuerung und bleibt eine Entscheidung für Task 16 · G.3 nennt für ITERATIV eine relative Toleranz ohne Nenner, das Abgleichskript rechnet mit max(Betrag a, Betrag b), hier ohne Folge (alle 23 Werte zeichengleich) · Die Zuordnung der Kennungen zu den G.3-Klassen steht nur im Abgleichskript, nicht in der Kennungen-Anlage · Ob R 4.4 oder 4.5 unter Windows denselben Absturz zeigt und ob er mit angeschlossener Konsole eine Meldung zeigt, wurde nicht geprüft · Beim Lesen des Workbooks mit Python kam ein Zugriffsfehler, sha256sum las die Datei (das Workbook war vermutlich in Excel geöffnet), die Prüfsumme stimmt.

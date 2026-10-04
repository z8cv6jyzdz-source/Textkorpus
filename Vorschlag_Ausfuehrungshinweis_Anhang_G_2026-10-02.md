# Vorschlag: Ausführungshinweis für Anhang G (Task 16)

**Bachelorarbeit U15-Plyometrie · Vorschlag, kein Einbau · 02.10.2026 · Claude Code (Opus 5.5) · Folge von Klick (a) vom 01.10. (Windows-Steuerung als eigene Datei neben `Gesamtlauf_2026-09-25.R`, mit Hinweis zur Ausführung)**

Den Umfang von Anhang G entscheidet Klickfrage 12 in Task 16, dieser Vorschlag nimmt sie nicht vorweg. Inhalt nur aus den Protokollen vom 01.10. und dem Lauf vom 02.10. mit seiner Zweitprüfung, je Aussage mit Quelle (Abschnitt 3). Beide Fassungen enthalten kein Semikolon und keine Kennung der Ergebnisdatei. Nach der Zweitprüfung überarbeitet (Vermerk vom 02.10., Abschnitt 13, H1 bis H11).

**Vorbehalt:** Nach dem vorab festgelegten Maßstab ist der Linuxlauf vom 02.10. nicht bestanden, weil die sechs Diagramme nur in der Schrift vom Archiv abweichen (Vermerk vom 02.10., Abschnitte 7 und 9). Der Hinweis setzt voraus, dass der Verfasser diese Abweichung in Klickfrage (b) des Vermerks als erklärt wertet. Abschnitt 5 der Datei `LIESMICH.txt` ist die Folge davon.

**Klick des Verfassers (02.10., 11:45 Sitzungsuhr):** (b) Abweichung als erklärt gewertet, der Vorbehalt ist damit erfüllt. (a) Dieser Vorschlag ist in der vorgelegten Fassung für Task 16 vorgemerkt.

Quellen:
- **[P]** `Claude\02_Befunde\Reproduktionsprotokoll_2026-10-01.md` (Windows, 01.10.)
- **[V1]** `Claude\03_Skripte\Reproduktion_2026-10-01\Vermerk_Probelauf_Linux_2026-10-01.md` (Linux, Cloud, 01.10.)
- **[V2]** `Claude\03_Skripte\Reproduktion_2026-10-01\Vermerk_Linuxzweig_2026-10-02.md` (Linux, WSL, 02.10., mit Zweitprüfung in Abschnitt 13)
- Köpfe und Quelltext der Skripte im ZIP der Abgabe

## 1 Fassung als Datei `LIESMICH.txt` für das Abgabepaket

```
LIESMICH  Ausführung und Prüfung der Rechenkette (Abgabe_R_2026-09-25)

Voraussetzung
Basis-R 4.3.3 ohne Zusatzpakete, unter Windows zusätzlich Git für Windows
(Git Bash). Für den Lauf einen eigenen Ordner Abgabe_R_2026-09-25 anlegen und
darin nur die R-Skripte aus dem ZIP und Gesamtlauf_Windows_2026-10-01.R ablegen.
Eine unberührte Fassung des entpackten ZIP bleibt getrennt davon als Vergleich,
denn der Lauf schreibt Ergebnisdatei und Prüfsummenliste neu. Der Ordner über dem
Laufordner enthält den Datenstand (Ordner Datenstand_2026-09-24) und die sieben
Anlagen der Spezifikation Spezifikation_2026-09-24_Kennungen.csv, _Konstanten,
_Koeffizienten_KR, _Vokabular, _Fragebogen, _Referenzdaten und
_Referenzdaten_Daten (je .csv). Gestartet wird im Laufordner.

1 Linux (Ubuntu 24.04, R 4.3.3 aus den Paketquellen des Systems)
    Rscript Gesamtlauf_2026-09-25.R
  oder
    Rscript Gesamtlauf_Windows_2026-10-01.R
Beide Steuerskripte sind unter Linux gleichwertig und starten die Rechenskripte
auf demselben Weg. Mit r-base-core 4.3.3-2build2 und Referenz-BLAS und -LAPACK
3.12.0 ergab jedes dieselbe Ergebnisdatei Byte für Byte. Mit anderen
Paketfassungen gelten die Toleranzen der Spezifikation (siehe 4 c). Laufzeit je
nach Rechner 6 bis 14 Minuten.

2 Windows (R 4.3.3)
Aus Git Bash starten, Rscript mit vollem Pfad aus dem Ordner bin der
R-Installation (oder diesen Ordner in den Suchpfad aufnehmen):
    "<Pfad zu R-4.3.3>/bin/Rscript.exe" Gesamtlauf_Windows_2026-10-01.R
Git Bash ist nötig, weil ein Grenzfall der Validierung die SHA-256-Berechnung in
R mit dem Programm sha256sum gegenprüft. Unter Windows liegt es nur in Git Bash
im Suchpfad. Die Laufzeit beträgt rund 20 Minuten. Jede Schrittausgabe beginnt
mit einer Warnung, dass Windows die Spracheinstellung "C.UTF-8" nicht annimmt.
Sie ist zu erwarten und ohne Folge, R rechnet in UTF-8 weiter. Die Ergebnisdatei
stimmt mit der archivierten bis auf die letzte Binärstelle eines einzigen Werts
überein. Der Abgleich mit den Toleranzen der Spezifikation zeigt keine Abweichung.

3 Warum Gesamtlauf_2026-09-25.R unter Windows abbricht
R für Windows setzt die Umgebungsangaben, die das Steuerskript den Schritten
mitgibt, als Wörter in die Befehlszeile, Rscript nimmt die erste davon als
Skriptdatei, R kann sie nicht öffnen und endet ohne eigene Ausgabe, die Kette
meldet dann bei den Referenztests Status 5 und "Validierung nicht bestanden".
Gesamtlauf_Windows_2026-10-01.R ändert nur die Steuerung, die Rechenskripte
bleiben unverändert.

4 Prüfung
a) Prüfsumme des Archivs
     sha256sum Abgabe_R_2026-09-25.zip                            (Linux, Git Bash)
     Get-FileHash Abgabe_R_2026-09-25.zip -Algorithm SHA256       (PowerShell)
   Soll 200b25956c4e12a9104164c025eddbe67dadc79ee12c3300b3a8b6e1a786525f
b) Prüfsummenliste, nach dem Lauf im Laufordner
     Rscript Pruefsummen_Abgabe_2026-09-25.R
   Das Skript schreibt Pruefsummen_Abgabe_2026-09-25.txt mit der SHA-256 jeder
   Datei des Laufordners. Diese Liste mit der Liste der unberührten Fassung
   vergleichen. Die neue Liste führt zusätzlich Gesamtlauf_Windows_2026-10-01.R,
   die Liste im Archiv drei Dokumente der Blindrechnung, die beim Lauf nicht
   entstehen. Unter Linux stimmen Ergebnisdatei, Zwischendateien und Skripte Byte
   für Byte überein (Paketfassungen wie in Abschnitt 1). Abweichen dürfen die
   Textausgaben (Zeitstempel, Aufruf- und Versionszeilen) und die sechs Diagramme
   (Schrift, siehe Abschnitt 5). Unter Windows weichen zusätzlich die
   Ergebnisdatei (eine Binärstelle), die Zeilenenden der Textdateien und die Bytes
   der Zwischendateien ab, inhaltlich sind diese gleich bis auf dieselbe
   Binärstelle.
c) Abgleich je Wert mit den Toleranzen der Spezifikation
     Rscript Abgleich_2026-09-25.R <Ergebnisdatei der unberührten Fassung> <neue Ergebnisdatei>
   Das Skript schreibt Abgleich_<Datum>.csv und Abgleich_<Datum>_Protokoll.txt
   in den aktuellen Ordner. Status 0 heißt bestanden. Bei Status 1 zeigt das
   Protokoll, ob eine Abweichung oder ein Fehler vorliegt.

5 Diagramme
Die sechs Diagramme der Voraussetzungsprüfung hängen von den installierten
Schriften ab. Mit einer anderen Schrift sind Titel und Beschriftungen breiter
oder schmaler, in den Q-Q-Diagrammen kann der Titel am rechten Rand abgeschnitten
sein. Punkte, Linien und Achsen bleiben gleich.
```

## 2 Fassung für den Fließtext von Anhang G (drei Sätze)

> Die Rechenkette wurde unter Ubuntu 24.04 mit R 4.3.3 nachgerechnet und ergab mit dem archivierten wie mit dem beigelegten Windows-Steuerskript dieselbe Ergebnisdatei Byte für Byte. Unter Windows bricht das archivierte Steuerskript beim ersten Schritt ab, weil R für Windows die Umgebungsangaben für die Schritte in die Befehlszeile setzt. Das Windows-Steuerskript ändert nur die Steuerung und ergab dort aus Git Bash jeden Wert neu, einen davon mit Abweichung in der letzten Binärstelle (Hinweise zu Ausführung und Prüfung in der beigelegten Datei LIESMICH).

## 3 Quelle je Aussage

| Nr. | Aussage | Quelle |
|---|---|---|
| L1 | Basis-R 4.3.3 ohne Zusatzpakete | `sessionInfo()` in [P] Abschnitt 2 und [V2] Abschnitt 2 (nur Basispakete), keines der 25 R-Skripte lädt ein Paket ([V2] Abschnitt 13, H9) |
| L1a | Unter Windows Git für Windows (Git Bash) | [P] Abschnitt 1 (Git Bash mit GNU sha256sum) und Befund 5 |
| L2 | Eigener Laufordner nur mit den R-Skripten aus dem ZIP und der Windows-Steuerung, unberührte Fassung getrennt, der Lauf schreibt Ergebnisdatei und Prüfsummenliste neu | [V1] Lauf 1: „Aufbau wie im Blindordner (Eingangsordner mit Datenstand und Anlagen, darunter `Abgabe_R_2026-09-25` mit den 25 R-Skripten aus dem ZIP)“, Kopf von `Reproduktion_Aufbau_2026-10-01.py` (Archiv und Laufordner getrennt), [P] Abschnitt 3, [V2] Abschnitt 4, [V2] Abschnitt 13 (H2: `Gesamtlauf_2026-09-25.R` schreibt die Ergebnisdatei neu, `Pruefsummen_Abgabe_2026-09-25.R` liest den ganzen Ordner) |
| L2a | Datenstand und die sieben Anlagen im Ordner über dem Laufordner, Start im Laufordner | [P] Abschnitt 12 Nr. 2 („`Funktionen_2026-09-25.R` erwartet sie im übergeordneten Ordner“), [P] Abschnitt 3, Liste der sieben Anlagen in `Funktionen_2026-09-25.R` (ANLAGEN) |
| L3 | Linux: beide Steuerskripte gleichwertig, gleicher Weg | [V2] Abschnitte 5 und 7 (Linux-Zweig mit den `env`-Angaben des Originals, Lauf C gegen Lauf D in allen geschriebenen Dateien ohne Zeitstempel bytegleich) |
| L3a | Byte für Byte mit r-base-core 4.3.3-2build2 und Referenz-BLAS und -LAPACK 3.12.0, sonst Toleranzen der Spezifikation | [V1] Umgebung und Lauf 1, [V2] Abschnitte 2 und 6 (bytegleich auch mit libc6 8.8), Prompt vom 02.10. § 0 (bei anderer Version Maßstab G.3), [V2] Befund 2 |
| L4 | Laufzeit Linux 6 bis 14 Minuten | [P] Abschnitt 6 (Blindrechnung 6,4 min), [V1] (6,9 und 7,1 min), [V2] Abschnitt 4 und Befund 9 (13,3 und 10,6 min) |
| L5 | Windows aus Git Bash, Rscript mit vollem Pfad | [P] Befund 5 („Start aus Git Bash ist nötig (sha256sum im PATH)“), [P] Abschnitt 1 („Alle Aufrufe mit vollem Pfad“) und Abschnitt 6, [V2] Abschnitt 13 (H1: Rscript liegt auf dem geprüften Rechner nicht im Suchpfad) |
| L6 | Grund: Grenzfall der Validierung prüft SHA-256 in R gegen sha256sum, unter Windows nur in Git Bash | [P] Abschnitt 4 und 6 (G18, 13 Zeilen), Befund 3, [V1] „Erwartete Abbrüche“ Nr. 3 |
| L7 | Laufzeit Windows rund 20 Minuten | [P] Abschnitt 6 (20,3 min) und Abschnitt 9 (18,7 min) |
| L8 | Warnung zur Spracheinstellung je Schritt, zu erwarten, ohne Folge, R rechnet in UTF-8 | [P] Abschnitt 6 („Spracheinstellung in den Kindprozessen“) und Befund 4 |
| L9 | Ergebnisdatei bis auf die letzte Binärstelle eines Werts gleich | [P] Abschnitt 6 und Befund 6 |
| L10 | Abgleich mit den Toleranzen der Spezifikation ohne Abweichung | [P] Abschnitt 8 C |
| L11 | Abbruch des archivierten Steuerskripts unter Windows (ein Satz), Meldung der Kette Status 5 und „Validierung nicht bestanden“ | [P] Abschnitt 5 (Verlauf mit „Status 5“ und „ABBRUCH: Validierung nicht bestanden“, „Schluss zu Lauf A“) und Befunde 1 und 2 |
| L12 | Windows-Steuerung ändert nur die Steuerung | [P] Abschnitt 1 (eigener Diff hunk-identisch) und Befund 5, Kopf von `Gesamtlauf_Windows_2026-10-01.R` |
| L13 | Soll-Prüfsumme des ZIP, Befehl unter Linux, Git Bash und PowerShell | [P] Abschnitt 1, [V2] Abschnitt 1, [V2] Abschnitt 13 (H6: `Get-FileHash` ergibt denselben Wert) |
| L14 | Prüfsummenskript schreibt die Liste mit SHA-256 je Datei des Ordners | [P] Abschnitt 7, [V2] Abschnitt 4, Kopf von `Pruefsummen_Abgabe_2026-09-25.R` |
| L15 | Neue Liste mit der Windows-Steuerung, Liste im Archiv mit drei Dokumenten der Blindrechnung | [P] Abschnitt 7 und Abschnitt 8 A, [V2] Abschnitt 6 |
| L16 | Linux: Ergebnisdatei, Zwischendateien und Skripte bytegleich, Textausgaben (Zeitstempel, Aufruf- und Versionszeilen) und Diagramme (Schrift) abweichend | [V2] Abschnitte 6 und 7, [V1] Lauf 1 |
| L17 | Windows: Ergebnisdatei, Zeilenenden und Bytes der Zwischendateien abweichend, Inhalt gleich bis auf die Binärstelle | [P] Abschnitt 8 B und E, Abschnitt 14 und Befund 10 |
| L18 | Abgleichskript: Aufruf mit zwei Ergebnisdateien, Ausgabedateien, Status 0 bestanden, Status 1 Abweichung oder Fehler | Kopf von `Abgleich_2026-09-25.R` (Ausgabestamm voreingestellt `Abgleich_JJJJ-MM-TT`), [P] Abschnitt 8 C, [V2] Abschnitt 13 (H5, eigener Test der Zweitprüfung) |
| L19 | Diagramme schriftabhängig, Titel in den Q-Q-Diagrammen abgeschnitten, Punkte, Linien und Achsen gleich | [V2] Abschnitt 7 und Befund 5, [P] Abschnitt 6 (Sichtprüfung unter Windows) |
| F1 | Linux, beide Steuerskripte, dieselbe Ergebnisdatei Byte für Byte | wie L3 und L3a |
| F2 | Abbruch unter Windows, Grund | wie L11 |
| F3 | Windows-Steuerung ändert nur die Steuerung, aus Git Bash jeder Wert neu, einer mit Abweichung in der letzten Binärstelle | wie L5, L9 und L12 |

## 4 Hinweise für Task 16

1. Die Datei `LIESMICH.txt` setzt voraus, dass `Gesamtlauf_Windows_2026-10-01.R` und `Abgleich_2026-09-25.R` im Abgabepaket liegen. Die zweite liegt schon im ZIP.
2. Abschnitt „Voraussetzung“ beschreibt den Aufbau, den die Kette erwartet. Ob Datenstand und Anlagen in Anhang G beigegeben werden, entscheidet Task 16 (Anhang G nur anonymisiert, L9).
3. Die Soll-Prüfsumme des ZIP gehört in `LIESMICH.txt` neben dem ZIP, nicht in das ZIP selbst. Wird das ZIP für die Abgabe neu gepackt (Task 16 e), ist die Prüfsumme neu zu setzen.
4. In der Fließtextfassung steht kein Abschnittsverweis. Der Verweis auf die Datei LIESMICH ist ein Dateiname.
5. „Dokumente der Blindrechnung“ in 4 b vereinfacht „Dokumente der Blindinstanz“ (Prompt der Phase 6, Rückfragen- und Übergabeprotokoll).

Task Linux-Zweig der Windows-Steuerung prüfen und Ausführungshinweis für Anhang G vorschlagen (Auswertungsverfahren 8.3 und 8.4, Nachgang zum Reproduktionstest)

Auftrag des Verfassers (01.10.2026, Klick (a) nach dem Reproduktionstest): Die geprüfte Windows-Steuerung `Gesamtlauf_Windows_2026-10-01.R` kommt als eigene Datei neben das unveränderte `Gesamtlauf_2026-09-25.R` in das Abgabepaket für Anhang G, mit Hinweis zur Ausführung. Vorher läuft ihr Linux-Zweig einmal unter Linux. Neue Zahlen für das Manuskript entstehen nicht.

Stand vorab (Rev. 143):
- Reproduktionstest unter Windows bestanden: `Claude\02_Befunde\Reproduktionsprotokoll_2026-10-01` (.md, .docx, .pdf), Belege in `Claude\03_Skripte\Reproduktion_2026-10-01\Lauf_Windows\`. Lauf B mit der Windows-Steuerung: Validierung 83 von 83 und 114 von 114, Abgleich nach G.3 ohne Abweichung, eine Kennung in der letzten Binärstelle, Kennzahlenblatt in der Darstellung gleich.
- Unter Linux lief bisher nur der Windows-Zweig dieser Datei, erzwungen in einer Testkopie (Probelauf Lauf 2, `Vermerk_Probelauf_Linux_2026-10-01.md`). Der Linux-Zweig, der beim normalen Start unter Linux läuft, ist ungetestet (Protokoll Abschnitt 15, Befund Z8). Er startet die Kindprozesse mit denselben `env`-Angaben wie das Original und schreibt zwei Zusatzzeilen ins Laufprotokoll (W3).
- Gerechnet wird in Claude Code auf dem Windows-Rechner unter WSL 2 mit Ubuntu 24.04 (WSL seit 02.10. installiert). Ist WSL nicht nutzbar, läuft derselbe Prompt in der Cloud-Sitzung von Cowork wie der Probelauf vom 01.10.

Vorbedingung, vom Verfasser vor dem Start auszuführen (Linux-Benutzer und sudo-Passwort legt nur der Verfasser an, die Sitzung gibt kein Passwort ein und umgeht sudo nicht):
1. In PowerShell: `wsl --install -d Ubuntu-24.04`, beim ersten Start Linux-Benutzername und Passwort festlegen.
2. In Ubuntu: `sudo apt-get update` und danach `sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends r-base-core`.
Fehlt eines davon, hält die Sitzung in § 0 an und nennt die Befehle.

Verfahren nach F17 § 1.2: rechnen und vergleichen nur per Skript, Protokoll mit nummerierter Befundliste, unabhängige Zweitprüfung durch einen Subagenten, Klickfragen, Teil 0. Unverändert bleiben `Claude\03_Skripte\Abgabe_R_2026-09-25\` und `Abgabe_R_2026-09-25.zip`, der Ordner `Statistik`, die Anlagen der Spezifikation, Kennzahlenblatt, Objekte, Master, das Reproduktionsprotokoll vom 01.10. und alle Werkzeuge in `Reproduktion_2026-10-01`. Kein Skript der Abgabe wird geändert, auch die Windows-Steuerung nicht. Keine Zahl von Hand.

## 0 Vorab
- Lesen: Teil 0 der Sitzungsnotizen (jüngste Rev., mindestens Rev. 143), Maßnahmenliste L9, Reproduktionsprotokoll vom 01.10. Abschnitte 5, 6, 8, 13 und 15, Vermerk zum Probelauf (Umgebung, Lauf 1, Lauf 2), `Gesamtlauf_Windows_2026-10-01_Diff.txt`.
- Prüfen: `wsl.exe -l -v` zeigt Ubuntu-24.04 mit Version 2, in Ubuntu liefern `cat /etc/os-release`, `command -v Rscript` und `python3 --version` Treffer. Sonst anhalten (Vorbedingung oben).
- Umgebung wie beim Probelauf und bei der Blindrechnung: Ubuntu 24.04, r-base-core aus den Paketquellen des Systems. Versionen mit `dpkg-query -W -f '${Package} ${Version}\n' r-base-core libblas3 liblapack3 libc6` notieren, dazu `wsl.exe --version` (WSL- und Kernelversion). Soll: r-base-core 4.3.3-2build2, libblas3 und liblapack3 3.12.0-3build1.1, libc6 2.39-0ubuntu8.7. Weicht eine Version ab: weiterrechnen, im Protokoll nennen, Maßstab für die Ergebnisdatei ist dann G.3 statt Bytegleichheit.
- Aufruf aus Claude Code (Git Bash): Befehle als Shellskript in den Arbeitsordner schreiben und mit `wsl.exe -d Ubuntu-24.04 -- bash <Skript>` starten, mit `MSYS_NO_PATHCONV=1`, damit Git Bash Linux-Pfade nicht umschreibt. Der Projektordner ist in Ubuntu `/mnt/c/Users/acul2/OneDrive/Desktop/Bachelorarbeit` (im Folgenden `<P>`), Skripte und Daten dort nur lesen.
- Gerechnet wird im Linux-Dateisystem außerhalb von OneDrive, Arbeitsordner `~/repro_2026-10-02` in Ubuntu (im Folgenden `<S>`). Konsolenausgaben nach `<S>/repro_C/Konsole_*.txt`, nie in den Laufordner.
- Laufzeit unter Linux rund 7 min, Prüfsummenskript rund 2 min.

## 1 Werkzeuge (SHA-256 vor der Verwendung prüfen, bei Abweichung stoppen)
| Datei | SHA-256 |
|---|---|
| `Claude\03_Skripte\Reproduktion_2026-10-01\Reproduktion_Aufbau_2026-10-01.py` | 0b4a859c57724604ebd8665c4018234cd1458a4f4e39beb8df4c19cfd65ea02e |
| `Claude\03_Skripte\Reproduktion_2026-10-01\Gesamtlauf_Windows_2026-10-01.R` | f58734b9050de2c0b5ebc3f16b7c3ee3d8f773335388e1e6d930005876a94b13 |
| `Claude\03_Skripte\Reproduktion_2026-10-01\Reproduktion_Vergleich_2026-10-01_Fassung3.py` | 7d99c49f17a6f59946b57fa2cb7a33b28b80ab2a92ee5d605340a677c3ff257d |
| `Claude\03_Skripte\Abgabe_R_2026-09-25.zip` | 200b25956c4e12a9104164c025eddbe67dadc79ee12c3300b3a8b6e1a786525f |

Die dritte Fassung des Vergleichs ist maßgeblich (zweite und dritte Fassung beheben zwei Fehler, die unter Windows auftraten, siehe Protokoll Befunde 8 und 9). Findest du in einem Werkzeug einen Fehler: nicht stillschweigend umgehen, als Befund, Korrektur nur als neue Fassung mit Datum und Grund im Kopf.

## 2 Lauf C: Windows-Steuerung im Linux-Zweig
1. `python3 <P>/Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Aufbau_2026-10-01.py <S>/repro_C` (das Skript findet `<P>` selbst, sonst `--basis <P>`)
2. Im Laufordner `<S>/repro_C/lauf/Abgabe_R_2026-09-25`: `Rscript Gesamtlauf_Windows_2026-10-01.R > <S>/repro_C/Konsole_Lauf_C.txt 2>&1`. Die Datei unverändert starten, ohne Testkopie und ohne erzwungenen Zweig, Shell mit ihrer normalen Spracheinstellung.
3. Danach im selben Ordner `Rscript Pruefsummen_Abgabe_2026-09-25.R > <S>/repro_C/Konsole_Pruefsummen_C.txt 2>&1`.
4. Am Laufprotokoll prüfen, dass wirklich der Linux-Zweig lief: Zeile „Steuerung: Gesamtlauf_Windows_2026-10-01.R, Linux-Zweig, rechnet wie Gesamtlauf_2026-09-25.R“, keine Zeile „G18-Gegenprobe (W4)“, keine Warnung zur Spracheinstellung in den Schrittausgaben, Umgebungsdatei mit `dpkg-query`-Zeilen.
5. Bricht Lauf C ab: anhalten, Ursache aus Laufprotokoll, Konsole und Schrittausgabe bestimmen, als Befund ins Protokoll, Klickfrage zum weiteren Vorgehen. Keine Änderung an der Steuerung ohne Klick.

## 3 Vergleich
`python3 <P>/Claude/03_Skripte/Reproduktion_2026-10-01/Reproduktion_Vergleich_2026-10-01_Fassung3.py <S>/repro_C --rscript Rscript`, Ausgabe in `<S>/repro_C/vergleich/`.

Maßstab, vorab festgelegt (bei Sollversionen nach § 0):
- Ergebnisdatei bytegleich, SHA-256 3194a805dc3e2c4bf0142ecab5f091d9e201449f3f2811b78073b406c74392a8
- Validierung: Referenztests 83 von 83, Grenzfälle 114 von 114
- Abgleich nach G.3 ohne Abweichung
- alle weiteren gemeinsamen Dateien bytegleich wie im Probelauf (41 Zwischendateien, sechs Grafiken S14, 25 R-Skripte)
- Kennzahlenblatt aus der neuen Ergebnisdatei: `Kennzahlen_2026-09-25.md` und `_Werte.csv` bytegleich mit `Claude\02_Befunde`
- Erwartet und nur zu benennen: im Laufprotokoll Aufrufbefehl, die beiden Zusatzzeilen aus W3 (Steuerung, Prüfsumme der Steuerung), die vier fehlenden Zeilen „nur dokumentiert, nicht gelesen“, in der Umgebungsdatei die Aufrufzeile mit dem Namen der Steuerung und die fest eingetragenen Installationsbefehle vom 25.09., in der Prüfsummenliste der Eintrag der Windows-Steuerung
- Urteil: bestanden, wenn alle Punkte erfüllt sind und jeder weitere Unterschied erklärt ist. Dann sind beide Zweige der Windows-Steuerung belegt und die Datei kann nach Klick (a) dem Abgabepaket beigelegt werden.

## 4 Ausführungshinweis für Anhang G (Vorschlag, kein Einbau)
Nach bestandenem Lauf C einen kurzen Hinweis zur Ausführung als Vorschlag für Task 16 schreiben: `Claude\04_Uebergaben\Vorschlag_Ausfuehrungshinweis_Anhang_G_2026-10-02.md`. Inhalt nur aus den Protokollen vom 01.10. und diesem Lauf, je Aussage mit Quelle:
- Linux (Ubuntu 24.04, R 4.3.3): `Rscript Gesamtlauf_2026-09-25.R` oder die Windows-Steuerung, beide gleichwertig
- Windows (R 4.3.3): `Rscript Gesamtlauf_Windows_2026-10-01.R` aus Git Bash, weil Grenzfall G18 GNU sha256sum braucht, Laufzeit rund 20 min, eine Warnung zur Spracheinstellung je Schritt ist zu erwarten und ohne Folge, die Ergebnisdatei ist bis auf die letzte Binärstelle einer Kennung gleich, der Abgleich nach G.3 zeigt keine Abweichung
- warum das archivierte Steuerskript unter Windows abbricht (ein Satz nach Protokoll Abschnitt 5)
- Prüfung: ZIP-Prüfsumme, `Pruefsummen_Abgabe_2026-09-25.R`, Abgleich mit `Abgleich_2026-09-25.R`
Zwei Fassungen vorlegen: als Datei `LIESMICH` für das Abgabepaket und als höchstens drei Sätze für den Fließtext von Anhang G. Den Umfang von Anhang G entscheidet Klickfrage 12 in Task 16, dieser Task nimmt sie nicht vorweg. Kein Semikolon, keine Kennung im Text.

## 5 Ergebnis
- Vermerk `Claude\03_Skripte\Reproduktion_2026-10-01\Vermerk_Linuxzweig_2026-10-02.md`: Umgebung mit `dpkg-query` und `sessionInfo()`, Befehle wörtlich, Lauf C, Vergleich nach den Abschnitten A bis G, Befundliste (Nr., Befund, Beleg, Folge, Ort der Änderung), Urteil, Klickfragen. Das Reproduktionsprotokoll vom 01.10. bleibt unverändert, der Vermerk ist sein Nachtrag.
- Ausgaben aus Ubuntu per Kopie nach `Claude\03_Skripte\Reproduktion_2026-10-01\Lauf_Linux_Windowssteuerung\`, flach, mit `Ablage_Liste.txt` (SHA-256 je Datei, nach dem Kopieren auf der Windows-Seite nachgerechnet): Aufbau- und Vergleichsprotokoll, Konsolen, Laufprotokoll, Umgebung, Validierungsprotokoll, Abgleich (.csv und _Protokoll.txt), Kennzahlen der Reproduktion. Die Ergebnisdatei nur, wenn sie nicht bytegleich ist.

## 6 Zweitprüfung, Klickfragen, Abschluss
1. Subagent ohne Beteiligung: Umgebung gegen Soll, Linux-Zweig wirklich gelaufen (§ 2 Nr. 4), Vergleich gegen eigene Messung (Ergebnisdatei per SHA-256 und je Kennung), jede Aussage des Vermerks, Ausführungshinweis gegen die Protokolle. Umgang je Befund im Vermerk.
2. Klickfragen mit AskUserQuestion, Empfehlung zuerst: (a) Ausführungshinweis in der vorgelegten Fassung für Task 16 vormerken oder ändern · (b) bei Abbruch oder unerklärtem Unterschied je Punkt das weitere Vorgehen.
3. Teil 0 mit der nächsten freien Rev. Vorher den Stand von Sitzungsnotizen und Maßnahmenliste neu lesen, parallele Sitzungen vergeben Rev.-Nummern (am 01.10. vergab die Recherche-Sitzung Rev. 142, der Reproduktionstest schrieb deshalb Rev. 143). Maßnahmenliste L9 fortschreiben: Linux-Zweig geprüft, Ausführungshinweis vorgeschlagen, offen bleiben KI-Deklaration, Nutzungsprotokoll, Anhang G mit Klickfrage 12, Abgabestand einfrieren. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen. Läuft der Kontext voll, rechtzeitig eine Übergabe schreiben.

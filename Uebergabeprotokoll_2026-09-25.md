# Übergabeprotokoll der Blindrechnung in R

Stand 2026-09-25 nach dem Gesamtlauf. Dieses Protokoll erlaubt einer neuen, ebenfalls blinden Sitzung, die Arbeit ohne Kenntnis des bisherigen Chats fortzusetzen oder zu wiederholen. Es enthält keine Ergebniswerte.

## Auftrag und Regeln

Zweite, unabhängige Implementierung der Auswertung nach `Spezifikation_2026-09-24` (Stand Nachtrag 2) in R, Phasen 3 bis 5 des Auswertungsverfahrens. Regeln der Aufgabenstellung: nur im Skript rechnen, Formeln nur aus dem Ordner, keine früheren Ergebnisse suchen oder nutzen, Spezifikation wörtlich umsetzen, Unklarheiten als Rückfrage, nur R, Eingangsdateien nie verändern, keine Interpretation, Texte auf Deutsch ohne Semikolons. Abgabe als Dateien in den Ordner, im Chat nur Dateiliste, Rückfragen, Anmerkungen und Warnungen.

## Ablage

- Eingang: Ordner `Blindrechnung_R_2026-09-24` (Spezifikation, Anlagen, `Datenstand_2026-09-24`, Prozessplan). Unverändert.
- Abgabe: Unterordner `Abgabe_R_2026-09-25` darin. Alle Skripte lesen den Eingang aus dem übergeordneten Ordner (`..`), Zwischendateien liegen in `Abgabe_R_2026-09-25/Zwischen`.
- Rechenumgebung: Ubuntu 24.04, R 4.3.3 aus `apt` (r-base-core), nur Basis-R, Einzelheiten in `Umgebung_2026-09-25.txt`. Aufruf der ganzen Kette: `Rscript Gesamtlauf_2026-09-25.R` im Abgabeordner (Umgebungsvariablen LC_ALL=C.UTF-8, TZ=UTC). Danach `Rscript Pruefsummen_Abgabe_2026-09-25.R` für die Prüfsummenliste.

## Aufbau der Skripte

- `Funktionen_2026-09-25.R`: Bibliothek (Pfade, Abbruch, SHA-256 in reinem R, strenges Einlesen, Mittel und SD verschoben gerechnet, Quantil Typ 7, Kleinste Quadrate über QR mit Spaltenskalierung, Varianzanalyse, Brown-Forsythe, Shapiro-Wilk über `shapiro.test` (AS R94), Power der nichtzentralen F-Verteilung, Khamis-Roche-Vorhersage, Kernregeln von S02, S05, S06, S07, S14 als Funktionen, Ergebnisregister mit Formatierung `%#.17g`, Sollliste der Kennungen mit ausgeschriebenen Spielerkennungen).
- `Referenztests_2026-09-25.R` (Phase 4a, R01 bis R13, mit Nachtrag Toleranz R08 vom 2026-09-25) und `Grenzfaelle_2026-09-25.R` (Phase 4b, 114 Fälle mit ausgeschriebenen Sollwerten).
- `S01_...` bis `S19_...`: ein Skript je Rechenschritt, jedes prüft am Ende, dass genau die Kennungen der Anlage `_Kennungen.csv` für seinen Schritt gesetzt sind. Ausgabe je Skript als `.txt` gleichen Namensstamms.
- `Gesamtlauf_2026-09-25.R`: startet Validierung und S01 bis S19 je in eigenem R-Prozess, führt `Ergebnisse_R_2026-09-25.csv` nach G.1 zusammen, schreibt `Laufprotokoll_2026-09-25.txt`, `Validierungsprotokoll_2026-09-25.txt` und `Umgebung_2026-09-25.txt`.
- `Pruefsummen_Abgabe_2026-09-25.R`: Prüfsummenliste aller abgegebenen Dateien (`Pruefsummen_Abgabe_2026-09-25.txt`), als letzter Schritt.
- `Abgleich_2026-09-25.R`: neutrales Abgleichskript für Phase 6.1 (zwei Ergebnisdateien, Toleranzklassen nach G.3, Bootstrap-Regel nach S19 Regel 6). Aufruf `Rscript Abgleich_2026-09-25.R <Ergebnisse_1.csv> <Ergebnisse_2.csv> [Ausgabestamm]`, Status 1 bei Abweichung. Die zweite Instanz hat es nur gegen ihre eigene Datei und gegen eine absichtlich gestörte Kopie geprüft.

## Rückfragen und Lesarten

Alle Rückfragen R1 bis R5 sind am 2026-09-25 beantwortet und mit Antwort im `Rueckfragenprotokoll_2026-09-25.md` festgehalten. R1 (Lesart a) und R4 (Lesart a) stehen als Schalter `LESART_R1` in S11 und `LESART_R4` in S14. R2 (Gründe) über die Konstanten `GRUND_...` der Bibliothek. R3 (Lesart a) in `paare_zaehlen`. R5 als Nachtrag zur Toleranz in `NACHTRAEGE_TOLERANZ` im Referenztest-Skript, die Anlage ist unverändert. Anmerkungen A1 bis A13 im Rückfragenprotokoll dokumentieren die übrigen Lesarten.

## Wiederholung

Für einen Reproduktionstest genügt der Abgabeordner neben dem unveränderten Eingang: R 4.3.3 installieren, im Abgabeordner den Unterordner `Zwischen` leeren, `Rscript Gesamtlauf_2026-09-25.R` ausführen, `Ergebnisse_R_2026-09-25.csv` gegen die archivierte Fassung vergleichen (Prüfsumme im Laufprotokoll und in der Prüfsummenliste). Zufallsverfahren: S19 mit `set.seed(20260924)` je Zielgröße, Mersenne-Twister, so dass die Bootstrap-Werte bei gleicher R-Fassung exakt reproduzierbar sind.

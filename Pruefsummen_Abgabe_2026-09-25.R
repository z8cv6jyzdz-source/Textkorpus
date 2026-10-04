# =====================================================================
# Pruefsummen_Abgabe_2026-09-25.R
# Zweck: Prüfsummenliste (SHA-256) aller abgegebenen Dateien des Ordners
#        Abgabe_R_2026-09-25 einschließlich des Unterordners Zwischen, ohne die
#        Liste selbst. Wird als letzter Schritt nach dem Gesamtlauf ausgeführt.
# Schritt der Spezifikation: Abgabe (Aufgabenstellung), Auswertungsverfahren 5.3 und 8.4
# Eingangsdateien: alle Dateien des Ordners Abgabe_R_2026-09-25 (Prüfsummen sind die Ausgabe)
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript Pruefsummen_Abgabe_2026-09-25.R
# Ausgabe: Pruefsummen_Abgabe_2026-09-25.txt (Form: Prüfsumme  Dateiname, wie Pruefsummen.txt des Datenstands)
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

ZIEL <- paste0("Pruefsummen_Abgabe_", FASSUNG, ".txt")
dateien <- sort(list.files(ORDNER_ABGABE, recursive = TRUE, all.files = FALSE))
dateien <- dateien[dateien != ZIEL]
zeilen <- character(0)
for (f in dateien) {
  zeilen <- c(zeilen, paste0(sha256_datei(file.path(ORDNER_ABGABE, f)), "  ", f))
  cat(zeilen[length(zeilen)], "\n", sep = "")
}
writeLines(zeilen, pfad_abgabe(ZIEL), useBytes = TRUE)
cat("Prüfsummenliste geschrieben: ", ZIEL, " (", length(zeilen), " Dateien)\n", sep = "")

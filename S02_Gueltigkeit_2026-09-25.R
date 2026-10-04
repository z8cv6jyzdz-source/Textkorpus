# =====================================================================
# S02_Gueltigkeit_2026-09-25.R
# Zweck: Gültigkeit jedes Versuchs festlegen: gültig_roh aus Wert und
#        ungültig, Auslöseprüfung der Sprintläufe über Abschnitte (K4),
#        gültig = gültig_roh und Lauf nicht auslösegestört.
# Schritt der Spezifikation: S02 (Teil A)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds (aus S01, Datenstand mit den Prüfsummen im Kopf von S01)
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S02_Gueltigkeit_2026-09-25.R
# Ausgabe: S02_Gueltigkeit_2026-09-25.txt, Zwischen/S02_versuche.rds,
#          Zwischen/S02_versuche.csv (Gültigkeit je Versuchszeile, ohne Kennung),
#          Zwischen/S02_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
schreibe_kopf(
  zweck = "Gültigkeit der Versuche und Auslöseprüfung der Sprintläufe",
  schritt = "S02",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
V_MAX <- konstante_zahl(konst, "V_MAX")
DT_MIN <- konstante_zahl(konst, "DT_MIN")
dist_text <- konstante_text(konst, "SPRINT_DISTANZEN")
DISTANZEN <- as.numeric(strsplit(trimws(dist_text), "\\s+")[[1]])
pruefe(length(DISTANZEN) == 3 && all(!is.na(DISTANZEN)) && all(diff(DISTANZEN) > 0),
       "SPRINT_DISTANZEN nicht als drei aufsteigende Zahlen lesbar: ", dist_text)
TESTS_SPRINT <- c("Sprint_5m", "Sprint_10m", "Sprint_30m")
names(DISTANZEN) <- TESTS_SPRINT
cat("\nKonstanten: V_MAX = ", V_MAX, " m/s, DT_MIN = ", DT_MIN, " s, Distanzen = ",
    paste(DISTANZEN, collapse = " "), " m\n", sep = "")

v <- daten$versuche

# Regel 1
v$gueltig_roh <- as.integer(!is.na(v$Wert) & v$ungueltig == "")

# Regel 2: Auslöseprüfung je Lauf (Code, Zeitpunkt, Versuch) über die Sprinttests
ist_sprint <- v$Test %in% TESTS_SPRINT
v$Lauf <- ifelse(ist_sprint, paste(v$Code, v$Zeitpunkt, v$Versuch, sep = "|"), NA_character_)
laeufe <- unique(v$Lauf[ist_sprint])
gestoert <- logical(length(laeufe))
names(gestoert) <- laeufe
for (l in laeufe) {
  zeilen <- which(ist_sprint & v$Lauf == l & v$gueltig_roh == 1)
  if (length(zeilen) == 0) next
  pruefe(!any(duplicated(v$Test[zeilen])), "Lauf mit doppeltem Sprinttest: ", l)
  gestoert[l] <- lauf_gestoert(unname(DISTANZEN[v$Test[zeilen]]), v$Wert[zeilen], V_MAX, DT_MIN)
}
v$auslgestoert <- ifelse(ist_sprint, unname(gestoert[v$Lauf]), FALSE)
v$auslgestoert[is.na(v$auslgestoert)] <- FALSE

# Regel 3
v$gueltig <- as.integer(v$gueltig_roh == 1 & !v$auslgestoert)

cat("Zeilen gesamt: ", nrow(v), ", gültig_roh = 1: ", sum(v$gueltig_roh), ", gültig = 1: ", sum(v$gueltig), "\n", sep = "")
cat("Sprintläufe geprüft: ", length(laeufe), ", davon auslösegestört: ", sum(gestoert), "\n", sep = "")

# Ausgabe
reg <- register_neu("S02_Gueltigkeit_2026-09-25.R")
for (zk in ZEIT_KENN) {
  zp <- if (zk == "PRE") ZEITPUNKT_PRAE else ZEITPUNKT_POST
  laeufe_zk <- laeufe[grepl(paste0("\\|", zp, "\\|"), laeufe)]
  setze(reg, paste0("S02.NAUSL.X.", zk, ".ALL.X"), sum(gestoert[laeufe_zk]), "anzahl")
}
for (z in ZIELE_SECHS) for (zk in ZEIT_KENN) {
  setze(reg, paste0("S02.NGUELT.", z, ".", zk, ".ALL.X"), sum(v$gueltig[v$Ziel == z & v$ZeitKenn == zk]), "anzahl")
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S02", daten$spieler))

saveRDS(v, pfad_zwischen("S02_versuche.rds"))
write.csv(v[, c("Code", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert", "ungueltig", "Bemerkung",
                "gueltig_roh", "auslgestoert", "gueltig")],
          pfad_zwischen("S02_versuche.csv"), row.names = FALSE, fileEncoding = "UTF-8")
register_speichere(reg, "S02")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

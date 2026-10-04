# =====================================================================
# S07_Adhaerenz_2026-09-25.R
# Zweck: Adhärenz je IG-Spieler (GANZ, GT, WOCAP, DIST), Umsetzungsraten mit
#        Nenner 12 × zugeteilte Spieler (K9), Verteilung und Schwellen,
#        Wochenanteile (P4), CR-10 und sRPE-Load der Meldungen ganz (K10),
#        unerwünschte Ereignisse (H007 = 1).
# Schritt der Spezifikation: S07 (Teil A), Regeln 9, 10 und 14 bis 22 entfallen (Nachtrag 2)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, Zwischen/S06_meldungen.rds (aus S01 und S06)
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S07_Adhaerenz_2026-09-25.R
# Ausgabe: S07_Adhaerenz_2026-09-25.txt, Zwischen/S07_adhaerenz.rds,
#          Zwischen/S07_adhaerenz.csv, Zwischen/S07_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
fb <- lies_zwischen("S06_meldungen.rds")
schreibe_kopf(
  zweck = "Adhärenz, Belastung und unerwünschte Ereignisse der IG",
  schritt = "S07",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
EINHEITEN <- konstante_zahl(konst, "EINHEITEN_ANGEBOTEN")
DECKEL <- konstante_zahl(konst, "WOCHENDECKEL")
WOCHEN <- paste0("W", 1:6)
dauer_min <- numeric(6)
names(dauer_min) <- WOCHEN
for (w in 1:6) {
  txt <- konstante_text(konst, paste0("DAUER_W", w))
  teile <- regmatches(txt, regexec("^([0-9]+):([0-9]{2})$", txt))[[1]]
  pruefe(length(teile) == 3, "Sitzungsdauer nicht im Format min:s: ", txt)
  dauer_min[w] <- as.numeric(teile[2]) + as.numeric(teile[3]) / 60
}
cat("\nKonstanten: Einheiten je Spieler = ", EINHEITEN, ", Wochendeckel = ", DECKEL, "\n", sep = "")
cat("Sitzungsdauer in Minuten je Woche: ", paste(sprintf("%s %.10g", WOCHEN, dauer_min), collapse = ", "), "\n", sep = "")

ig <- daten$spieler$IG
n_zug <- length(ig)
lp <- daten$listenplatz
ohne_platz <- lp$Code[lp$kein_Listenplatz == "ja"]
pruefe(all(fb$Analysecode %in% ig), "Meldung mit Analysecode außerhalb der IG")

# Regel 1 bis 5: Zählungen je IG-Spieler
adh <- data.frame(Code = ig, kein_Listenplatz = ig %in% ohne_platz, NMELD = 0L, GANZ = 0L, GT = 0L,
                  WOCAP = 0L, DIST = 0L, stringsAsFactors = FALSE)
for (i in seq_len(nrow(adh))) {
  m <- fb[fb$Analysecode == adh$Code[i], ]
  za <- adhaerenz_zaehlung(m$Status, m$Woche, m$H003, DECKEL, WOCHEN)
  adh$NMELD[i] <- za$NMELD
  adh$GANZ[i] <- za$GANZ
  adh$GT[i] <- za$GT
  adh$WOCAP[i] <- za$WOCAP
  adh$DIST[i] <- za$DIST
}
pruefe(all(adh$NMELD[adh$kein_Listenplatz] == 0), "Spieler ohne Listenplatz mit Meldungen")
# Einzelwerte für Spieler ohne Listenplatz fehlend (nicht erhebbar), in Summen und Verteilung 0
adh$Grund <- ifelse(adh$kein_Listenplatz, GRUND_NICHT_ERHEBBAR, "")
if (any(adh$GANZ > EINHEITEN)) {
  cat("HINWEIS: Zählung GANZ über ", EINHEITEN, " bei: ", paste(adh$Code[adh$GANZ > EINHEITEN], collapse = ", "),
      " (jede Meldung zählt, K7). V00 bis V12 decken diese Spieler nicht ab.\n", sep = "")
}
cat("Zugeteilte IG-Spieler: ", n_zug, ", ohne Listenplatz: ", sum(adh$kein_Listenplatz),
    ", mit mindestens einer Meldung: ", sum(adh$NMELD > 0), "\n", sep = "")

reg <- register_neu("S07_Adhaerenz_2026-09-25.R")
for (i in seq_len(nrow(adh))) {
  cd <- adh$Code[i]
  for (z in c("GANZ", "WOCAP", "DIST")) {
    wert <- if (adh$kein_Listenplatz[i]) NA_real_ else adh[[z]][i]
    setze(reg, paste0("S07.ADH.ADH.X.P", cd, ".", z), wert, "anzahl", adh$Grund[i])
  }
}
# Regel 6: Summen und Raten
setze(reg, "S07.NZUG.ADH.X.IG.X", n_zug, "anzahl")
for (z in c("GANZ", "GT", "WOCAP", "DIST")) {
  s <- sum(adh[[z]])
  setze(reg, paste0("S07.SUMME.ADH.X.IG.", z), s, "anzahl")
  setze(reg, paste0("S07.RATE.ADH.X.IG.", z), s / (EINHEITEN * n_zug), "zahl")
}
# Regel 7: Verteilung der Zählung GANZ über die zugeteilten Spieler
for (v in 0:12) setze(reg, sprintf("S07.V%02d.ADH.X.IG.GANZ", v), sum(adh$GANZ == v), "anzahl")
for (s in 1:12) setze(reg, sprintf("S07.GE%02d.ADH.X.IG.GANZ", s), sum(adh$GANZ >= s), "anzahl")
for (z in c("WOCAP", "DIST")) for (s in c(6, 9)) {
  setze(reg, sprintf("S07.GE%02d.ADH.X.IG.%s", s, z), sum(adh[[z]] >= s), "anzahl")
}
setze(reg, "S07.MED.ADH.X.IG.GANZ", median7(adh$GANZ), "zahl")
setze(reg, "S07.MITT.ADH.X.IG.GANZ", mittel(adh$GANZ), "zahl")
setze(reg, "S07.NMELDSP.ADH.X.IG.X", sum(adh$NMELD > 0), "anzahl")

# Regel 8: Wochenanteile
ganz <- fb[fb$Status == "GANZ", ]
for (w in WOCHEN) {
  setze(reg, paste0("S07.ANTW.ADH.", w, ".IG.GANZ"), sum(ganz$Woche == w) / (DECKEL * n_zug), "zahl")
}

# Regel 11 und 12: CR-10 und sRPE-Load der Meldungen ganz
ganz$Load <- ganz$CR10 * dauer_min[ganz$Woche]
statistik <- function(x, praefix, suffix) {
  n <- length(x)
  setze(reg, paste0(praefix, "N", suffix), n, "anzahl")
  setze(reg, paste0(praefix, "M", suffix), mittel(x), "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0(praefix, "SD", suffix), sd_n1(x), "zahl", GRUND_ZU_WENIG)
}
for (gr in c("CR10", "LOAD")) {
  x <- if (gr == "CR10") ganz$CR10 else ganz$Load
  praefix <- "S07."
  suffix <- paste0(".", gr, ".X.IG.GANZ")
  statistik(x, praefix, suffix)
  setze(reg, paste0(praefix, "MED", suffix), median7(x), "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0(praefix, "MIN", suffix), min_na(x), "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0(praefix, "MAX", suffix), max_na(x), "zahl", GRUND_ZU_WENIG)
  for (w in WOCHEN) statistik(x[ganz$Woche == w], praefix, paste0(".", gr, ".", w, ".IG.GANZ"))
}

# Regel 13: unerwünschte Ereignisse
ue <- fb[fb$H007 == 1, ]
setze(reg, "S07.UE.FB.X.IG.X", nrow(ue), "anzahl")
for (st in c("GANZ", "TEILW", "GARN")) setze(reg, paste0("S07.UE.FB.X.IG.", st), sum(ue$Status == st), "anzahl")
setze(reg, "S07.UESP.FB.X.IG.X", length(unique(ue$Analysecode)), "anzahl")

register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S07", daten$spieler))
saveRDS(adh, pfad_zwischen("S07_adhaerenz.rds"))
write.csv(adh, pfad_zwischen("S07_adhaerenz.csv"), row.names = FALSE, fileEncoding = "UTF-8")
register_speichere(reg, "S07")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

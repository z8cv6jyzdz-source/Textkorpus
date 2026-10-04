# =====================================================================
# S19_Bootstrap_2026-09-25.R
# Zweck: Bootstrap-Perzentil-KI der adjustierten Differenz b1 (Modell S13, ITT-Set),
#        B = 10 000 Ziehungen, Schichtung nach Gruppe, Startwert 20260924 vor jeder
#        Zielgröße neu (O8, N3), Ziehungen ohne vollen Rang verworfen und gezählt,
#        SD der b1*, Monte-Carlo-Fehler je KI-Grenze aus 20 Blöcken.
# Schritt der Spezifikation: S19 (Teil E)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S13_modelle.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S19_Bootstrap_2026-09-25.R
# Zufallszahlen: R 4.3.3, RNGkind Mersenne-Twister, Inversion, Rejection (Voreinstellung),
#   set.seed(BOOT_STARTWERT) vor jeder Zielgröße, je Ziehung erst n_IG Indizes der IG,
#   dann n_KG Indizes der KG mit sample(..., replace = TRUE).
# Ausgabe: S19_Bootstrap_2026-09-25.txt, Zwischen/S19_b1stern_<ZIEL>.csv, Zwischen/S19_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
m13 <- lies_zwischen("S13_modelle.rds")
schreibe_kopf(
  zweck = "Bootstrap-Konfidenzintervall der adjustierten Differenz",
  schritt = "S19",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
B <- konstante_zahl(konst, "BOOT_B")
STARTWERT <- konstante_zahl(konst, "BOOT_STARTWERT")
BLOECKE <- konstante_zahl(konst, "BOOT_BLOECKE")
KI <- konstante_zahl(konst, "KI_NIVEAU")
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
cat("\nKonstanten: B = ", B, ", Startwert = ", STARTWERT, ", Blöcke = ", BLOECKE, ", KI-Niveau = ", KI, "\n", sep = "")
cat("Zufallszahlengenerator: ", paste(RNGkind(), collapse = ", "), "\n", sep = "")
p_lo <- (1 - KI) / 2
p_hi <- 1 - p_lo

reg <- register_neu("S19_Bootstrap_2026-09-25.R")
for (z in ZIELE_KONF) {
  m <- m13$modelle[[z]]
  d <- m$daten
  suf <- paste0(".", z, ".X.ITT.BOOT")
  if (m$inf == 0) {
    for (nm in c("BKIU", "BKIO", "BSD", "BMCU", "BMCO")) setze(reg, paste0("S19.", nm, suf), NA_real_, "zahl", GRUND_FALLZAHL)
    for (nm in c("BNGUELT", "BNVERW")) setze(reg, paste0("S19.", nm, suf), NA_real_, "anzahl", GRUND_FALLZAHL)
    cat("\nZielgröße ", z, ": INF = 0, kein Bootstrap\n", sep = "")
    next
  }
  idx_ig <- which(d$G == 1)
  idx_kg <- which(d$G == 0)
  n_ig <- length(idx_ig)
  n_kg <- length(idx_kg)
  set.seed(STARTWERT)
  b1 <- rep(NA_real_, B)
  verworfen <- 0L
  t0 <- Sys.time()
  for (b in seq_len(B)) {
    idx <- c(sample(idx_ig, n_ig, replace = TRUE), sample(idx_kg, n_kg, replace = TRUE))
    ds <- d[idx, ]
    fit <- kq_schaetzung(cbind(1, ds$G, ds$Pre, ds$PAH), ds$Post)
    if (!fit$rang_voll) {
      verworfen <- verworfen + 1L
    } else {
      b1[b] <- fit$koef[2]
    }
  }
  gueltig <- b1[!is.na(b1)]
  n_g <- length(gueltig)
  pruefe(n_g + verworfen == B, "Ziehungen nicht vollständig gezählt")
  cat("\nZielgröße ", z, ": ", B, " Ziehungen, gültig ", n_g, ", verworfen ", verworfen, ", Dauer ",
      format(round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1)), " s\n", sep = "")
  setze(reg, paste0("S19.BNGUELT", suf), n_g, "anzahl")
  setze(reg, paste0("S19.BNVERW", suf), verworfen, "anzahl")
  setze(reg, paste0("S19.BKIU", suf), quantil7(gueltig, p_lo), "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S19.BKIO", suf), quantil7(gueltig, p_hi), "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S19.BSD", suf), sd_n1(gueltig), "zahl", GRUND_ZU_WENIG)
  # Regel 5: Monte-Carlo-Fehler aus Blöcken in Ziehungsreihenfolge
  m_bl <- floor(n_g / BLOECKE)
  if (m_bl >= 1) {
    q_lo <- numeric(BLOECKE)
    q_hi <- numeric(BLOECKE)
    for (k in seq_len(BLOECKE)) {
      block <- gueltig[((k - 1) * m_bl + 1):(k * m_bl)]
      q_lo[k] <- quantil7(block, p_lo)
      q_hi[k] <- quantil7(block, p_hi)
    }
    setze(reg, paste0("S19.BMCU", suf), sd_n1(q_lo) / sqrt(BLOECKE), "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S19.BMCO", suf), sd_n1(q_hi) / sqrt(BLOECKE), "zahl", GRUND_ZU_WENIG)
  } else {
    setze(reg, paste0("S19.BMCU", suf), NA_real_, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S19.BMCO", suf), NA_real_, "zahl", GRUND_ZU_WENIG)
  }
  write.csv(data.frame(Ziehung = seq_len(B), b1_stern = b1), pfad_zwischen(paste0("S19_b1stern_", z, ".csv")),
            row.names = FALSE, na = "")
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S19", daten$spieler))
register_speichere(reg, "S19")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

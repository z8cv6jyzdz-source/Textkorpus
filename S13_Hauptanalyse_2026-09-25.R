# =====================================================================
# S13_Hauptanalyse_2026-09-25.R
# Zweck: Hauptanalyse: ANCOVA Post = b0 + b1·G + b2·Prä + b3·PAH im ITT-Set je
#        konfirmatorischer Zielgröße (Z30, CM, SBJ) mit BEST-Werten, Kleinste
#        Quadrate über QR, adjustierte Differenz b1 mit SE, t, p und KI,
#        adjustierte Mittelwerte am Kovariatenmittel (K17), Entscheidung über H0 (K23, P6).
# Schritt der Spezifikation: S13 (Teil E)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S04_aggregat.rds, S05_pah.rds, S08_sets.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S13_Hauptanalyse_2026-09-25.R
# Ausgabe: S13_Hauptanalyse_2026-09-25.txt, Zwischen/S13_modelle.rds, Zwischen/S13_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
sets <- lies_zwischen("S08_sets.rds")
schreibe_kopf(
  zweck = "Hauptanalyse: ANCOVA im ITT-Set",
  schritt = "S13",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
ALPHA <- konstante_zahl(konst, "ALPHA")
KI <- konstante_zahl(konst, "KI_NIVEAU")
cat("\nKonstanten: alpha = ", ALPHA, ", KI-Niveau = ", KI, "\n", sep = "")
gruppe <- sets$gruppe

reg <- register_neu("S13_Hauptanalyse_2026-09-25.R")
modelle <- list()
sig_liste <- integer(0)
n_test <- 0L
for (z in ZIELE_KONF) {
  itt <- sets$itt[[z]]
  d <- modelldaten(itt, z, agg, pah, gruppe, sets$fam, "BEST")
  n_ig <- sum(d$G == 1)
  n_kg <- sum(d$G == 0)
  inf <- inf_von(sets, z, "ITT")
  pre <- paste0("S13.")
  suf <- paste0(".", z, ".X.ITT.HAUPT")
  setze(reg, paste0(pre, "NIG", suf), n_ig, "anzahl")
  setze(reg, paste0(pre, "NKG", suf), n_kg, "anzahl")
  namen_modell <- c("B0", "B1", "B2", "B3", "SEB0", "SEB1", "SEB2", "SEB3", "SIGMA", "DF", "R2", "T", "P",
                    "KIU", "KIO", "AMIG", "AMKG", "SEAMIG", "SEAMKG", "AMIGU", "AMIGO", "AMKGU", "AMKGO",
                    "PREM", "PAHM")
  cat("\nZielgröße ", z, ": n_IG = ", n_ig, ", n_KG = ", n_kg, ", INF = ", inf, "\n", sep = "")
  if (inf == 0) {
    for (nm in namen_modell) setze(reg, paste0(pre, nm, suf), NA_real_, if (nm == "DF") "anzahl" else "zahl", GRUND_FALLZAHL)
    setze(reg, paste0(pre, "SIG", suf), NA_real_, "merkmal", GRUND_FALLZAHL)
    modelle[[z]] <- list(daten = d, inf = inf, fit = NULL)
    next
  }
  n_test <- n_test + 1L
  X <- cbind(1, d$G, d$Pre, d$PAH)
  fit <- kq_schaetzung(X, d$Post)
  if (!fit$rang_voll) {
    cat("  Designmatrix ohne vollen Rang, Modell nicht gerechnet\n")
    for (nm in namen_modell) setze(reg, paste0(pre, nm, suf), NA_real_, if (nm == "DF") "anzahl" else "zahl", GRUND_RANG)
    setze(reg, paste0(pre, "SIG", suf), NA_real_, "merkmal", GRUND_RANG)
    modelle[[z]] <- list(daten = d, inf = inf, fit = fit)
    next
  }
  ki <- koef_inferenz(fit, 2, KI)
  for (j in 1:4) {
    setze(reg, paste0(pre, "B", j - 1, suf), fit$koef[j], "zahl")
    setze(reg, paste0(pre, "SEB", j - 1, suf), fit$se[j], "zahl")
  }
  setze(reg, paste0(pre, "SIGMA", suf), fit$sigma, "zahl")
  setze(reg, paste0(pre, "DF", suf), fit$df, "anzahl")
  setze(reg, paste0(pre, "R2", suf), fit$r2, "zahl")
  setze(reg, paste0(pre, "T", suf), ki$t, "zahl")
  setze(reg, paste0(pre, "P", suf), ki$p, "zahl")
  setze(reg, paste0(pre, "KIU", suf), ki$kiu, "zahl")
  setze(reg, paste0(pre, "KIO", suf), ki$kio, "zahl")
  # Regel 3: adjustierte Mittelwerte am Mittel der Kovariaten des Analysesets
  p_quer <- mittel(d$Pre)
  a_quer <- mittel(d$PAH)
  q <- t_quantil(1 - (1 - KI) / 2, fit$df)
  am <- list()
  for (g in c(1, 0)) {
    cvek <- c(1, g, p_quer, a_quer)
    wert <- sum(cvek * fit$koef)
    se <- sqrt(as.numeric(t(cvek) %*% fit$V %*% cvek))
    nm <- if (g == 1) "IG" else "KG"
    setze(reg, paste0(pre, "AM", nm, suf), wert, "zahl")
    setze(reg, paste0(pre, "SEAM", nm, suf), se, "zahl")
    setze(reg, paste0(pre, "AM", nm, "U", suf), wert - q * se, "zahl")
    setze(reg, paste0(pre, "AM", nm, "O", suf), wert + q * se, "zahl")
  }
  setze(reg, paste0(pre, "PREM", suf), p_quer, "zahl")
  setze(reg, paste0(pre, "PAHM", suf), a_quer, "zahl")
  # Entscheidungsregel
  sig <- as.integer(ki$p < ALPHA && guenstig(ki$b, z))
  setze(reg, paste0(pre, "SIG", suf), sig, "merkmal")
  sig_liste <- c(sig_liste, sig)
  cat("  Modell gerechnet, df = ", fit$df, ", SIG = ", sig, "\n", sep = "")
  modelle[[z]] <- list(daten = d, inf = inf, fit = fit)
}
setze(reg, "S13.H0REJ.X.X.ITT.HAUPT", as.integer(any(sig_liste == 1)), "merkmal")
setze(reg, "S13.NTEST.X.X.ITT.HAUPT", n_test, "anzahl")
cat("\nKonfirmatorische Zielgrößen mit INF = 1: ", n_test, "\n", sep = "")

register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S13", daten$spieler))
saveRDS(list(modelle = modelle, ALPHA = ALPHA, KI = KI), pfad_zwischen("S13_modelle.rds"))
register_speichere(reg, "S13")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

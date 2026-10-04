# =====================================================================
# S15_Effektstaerke_2026-09-25.R
# Zweck: Hedges' g = b1 / gepoolte Prä-SD × J mit KI aus dem KI von b1 (O3) und
#        unadjustierte Differenz der Post-Mittel mit gepoolter Varianz (O4),
#        nur für die Hauptanalyse (Nachtrag 2), nur bei INF = 1.
# Schritt der Spezifikation: S15 (Teil E)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S13_modelle.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S15_Effektstaerke_2026-09-25.R
# Ausgabe: S15_Effektstaerke_2026-09-25.txt, Zwischen/S15_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
m13 <- lies_zwischen("S13_modelle.rds")
schreibe_kopf(
  zweck = "Effektstärke und unadjustierte Differenz der Hauptanalyse",
  schritt = "S15",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
KI <- konstante_zahl(konst, "KI_NIVEAU")
pruefe(konstante_text(konst, "J_FORMEL") == "1 − 3/(4·df_g − 1)", "J_FORMEL der Konstanten weicht von der Bibliothek ab")

reg <- register_neu("S15_Effektstaerke_2026-09-25.R")
for (z in ZIELE_KONF) {
  m <- m13$modelle[[z]]
  d <- m$daten
  fit <- m$fit
  suf <- paste0(".", z, ".X.ITT.HAUPT")
  namen_zahl <- c("SDPRE", "J", "G", "GKIU", "GKIO", "UD", "UDSE", "UDT", "UDP", "UDKIU", "UDKIO",
                  "MPOSTIG", "MPOSTKG", "SDPOST")
  if (m$inf == 0) {
    for (nm in namen_zahl) setze(reg, paste0("S15.", nm, suf), NA_real_, "zahl", GRUND_FALLZAHL)
    for (nm in c("DFG", "UDDF")) setze(reg, paste0("S15.", nm, suf), NA_real_, "anzahl", GRUND_FALLZAHL)
    cat("\nZielgröße ", z, ": INF = 0, keine Effektstärke\n", sep = "")
    next
  }
  pre_ig <- d$Pre[d$G == 1]
  pre_kg <- d$Pre[d$G == 0]
  post_ig <- d$Post[d$G == 1]
  post_kg <- d$Post[d$G == 0]
  # Regel 1 bis 3
  sd_pre <- sd_pool(pre_ig, pre_kg)
  df_g <- length(pre_ig) + length(pre_kg) - 2
  J <- faktor_j(df_g)
  setze(reg, paste0("S15.SDPRE", suf), sd_pre, "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S15.DFG", suf), df_g, "anzahl")
  setze(reg, paste0("S15.J", suf), J, "zahl")
  if (is.null(fit) || !fit$rang_voll) {
    for (nm in c("G", "GKIU", "GKIO")) setze(reg, paste0("S15.", nm, suf), NA_real_, "zahl", GRUND_RANG)
  } else if (is.na(sd_pre)) {
    for (nm in c("G", "GKIU", "GKIO")) setze(reg, paste0("S15.", nm, suf), NA_real_, "zahl", GRUND_ZU_WENIG)
  } else if (sd_pre == 0) {
    for (nm in c("G", "GKIU", "GKIO")) setze(reg, paste0("S15.", nm, suf), NA_real_, "zahl", GRUND_KONSTANT)
  } else {
    ki <- koef_inferenz(fit, 2, KI)
    setze(reg, paste0("S15.G", suf), ki$b / sd_pre * J, "zahl")
    setze(reg, paste0("S15.GKIU", suf), ki$kiu / sd_pre * J, "zahl")
    setze(reg, paste0("S15.GKIO", suf), ki$kio / sd_pre * J, "zahl")
  }
  # Regel 4: unadjustierte Differenz
  zg <- zwei_gruppen(post_ig, post_kg, KI)
  setze(reg, paste0("S15.UD", suf), zg$d, "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S15.MPOSTIG", suf), zg$m1, "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S15.MPOSTKG", suf), zg$m2, "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S15.SDPOST", suf), zg$sd_pool, "zahl", GRUND_ZU_WENIG)
  setze(reg, paste0("S15.UDDF", suf), zg$df, "anzahl")
  grund_ud <- if (is.na(zg$sd_pool)) GRUND_ZU_WENIG else if (zg$sd_pool == 0) GRUND_KONSTANT else ""
  setze(reg, paste0("S15.UDSE", suf), zg$se, "zahl", grund_ud)
  setze(reg, paste0("S15.UDT", suf), zg$t, "zahl", grund_ud)
  setze(reg, paste0("S15.UDP", suf), zg$p, "zahl", grund_ud)
  setze(reg, paste0("S15.UDKIU", suf), zg$kiu, "zahl", grund_ud)
  setze(reg, paste0("S15.UDKIO", suf), zg$kio, "zahl", grund_ud)
  cat("\nZielgröße ", z, ": df_g = ", df_g, ", gerechnet\n", sep = "")
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S15", daten$spieler))
register_speichere(reg, "S15")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

# =====================================================================
# S18_Poweranalyse_2026-09-25.R
# Zweck: Sensitivitäts-Poweranalyse nach dem Standardweg (O9): F-Test des
#        Gruppenterms mit df1 = 1, df2 = N − 4, λ = d²·n_IG·n_KG/N, Power aus der
#        nichtzentralen F-Verteilung, MDES bei Power 0,80 durch Nullstellensuche,
#        Power bei den dokumentierten Vorab-Erwartungen (Nachtrag 2: nur die
#        im Plan genannten Kombinationen). Unabhängig von INF (P7).
# Schritt der Spezifikation: S18 (Teil E)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S08_sets.rds (nur n_IG und n_KG der ITT-Sets)
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S18_Poweranalyse_2026-09-25.R
# Ausgabe: S18_Poweranalyse_2026-09-25.txt, Zwischen/S18_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
sets <- lies_zwischen("S08_sets.rds")
schreibe_kopf(
  zweck = "Sensitivitäts-Poweranalyse, Standardweg",
  schritt = "S18",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
ALPHA <- konstante_zahl(konst, "ALPHA")
POWER_ZIEL <- konstante_zahl(konst, "POWER_ZIEL")
SESOI_FAKTOR <- konstante_zahl(konst, "SESOI_FAKTOR")
TOL <- konstante_zahl(konst, "NULLSTELLE_TOLERANZ")
intervall <- as.numeric(strsplit(trimws(konstante_text(konst, "NULLSTELLE_INTERVALL")), "\\s+")[[1]])
pruefe(length(intervall) == 2 && !anyNA(intervall) && intervall[1] < intervall[2], "NULLSTELLE_INTERVALL nicht lesbar")
d_erw <- c(D006 = konstante_zahl(konst, "D_ERWARTUNG_D006"), D011 = konstante_zahl(konst, "D_ERWARTUNG_D011"),
           D037 = konstante_zahl(konst, "D_ERWARTUNG_D037"), D093 = konstante_zahl(konst, "D_ERWARTUNG_D093"))
cat("\nKonstanten: alpha = ", ALPHA, ", Zielpower = ", POWER_ZIEL, ", Intervall [", intervall[1], ", ", intervall[2],
    "], Toleranz ", TOL, ", d-Erwartungen ", paste(names(d_erw), d_erw, collapse = " "), "\n", sep = "")
gruppe <- sets$gruppe
kombinationen <- list(Z10 = c("D006", "D011"), Z30 = c("D037", "D093"), CM = c("D037", "D093"), SBJ = c("D037", "D093"))

reg <- register_neu("S18_Poweranalyse_2026-09-25.R")
for (z in c("Z10", "Z30", "CM", "SBJ")) {
  itt <- sets$itt[[z]]
  n_ig <- sum(gruppe[itt] == "IG")
  n_kg <- sum(gruppe[itt] == "KG")
  N <- n_ig + n_kg
  df1 <- 1
  df2 <- N - 4
  suf <- paste0(".", z, ".X.ITT.X")
  setze(reg, paste0("S18.NTOT", suf), N, "anzahl")
  setze(reg, paste0("S18.DF1", suf), df1, "anzahl")
  setze(reg, paste0("S18.DF2", suf), df2, "anzahl")
  rechenbar <- df2 >= 1 && n_ig >= 1 && n_kg >= 1
  cat("\nZielgröße ", z, ": N = ", N, ", df2 = ", df2, if (rechenbar) "" else ", nicht rechenbar", "\n", sep = "")
  lambda <- function(d) d^2 * n_ig * n_kg / N
  power <- function(d) power_f(df1, df2, lambda(d), ALPHA)
  setze(reg, paste0("S18.FCRIT", suf), if (rechenbar) f_krit(df1, df2, ALPHA) else NA_real_, "zahl", GRUND_ZU_WENIG)
  if (z %in% ZIELE_KONF) {
    if (!rechenbar) {
      setze(reg, paste0("S18.MDES", suf), NA_real_, "zahl", GRUND_ZU_WENIG)
      setze(reg, paste0("S18.MDESR", suf), NA_real_, "zahl", GRUND_ZU_WENIG)
    } else if (power(intervall[2]) < POWER_ZIEL) {
      setze(reg, paste0("S18.MDES", suf), NA_real_, "zahl", GRUND_NULLSTELLE)
      setze(reg, paste0("S18.MDESR", suf), NA_real_, "zahl", GRUND_NULLSTELLE)
    } else {
      ns <- uniroot(function(d) power(d) - POWER_ZIEL, interval = intervall, tol = TOL, maxiter = 10000)
      pruefe(abs(ns$f.root) < 1e-8, "Nullstellensuche nicht konvergiert")
      setze(reg, paste0("S18.MDES", suf), ns$root, "zahl")
      setze(reg, paste0("S18.MDESR", suf), ns$root / SESOI_FAKTOR, "zahl")
      cat("  MDES gefunden nach ", ns$iter, " Iterationen, geschätzte Genauigkeit ", format(ns$estim.prec), "\n", sep = "")
    }
  }
  for (dk in kombinationen[[z]]) {
    setze(reg, paste0("S18.POW.", z, ".X.ITT.", dk), if (rechenbar) power(d_erw[[dk]]) else NA_real_, "zahl", GRUND_ZU_WENIG)
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S18", daten$spieler))
register_speichere(reg, "S18")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

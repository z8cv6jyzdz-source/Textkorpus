# =====================================================================
# S17_Sensitivitaet_2026-09-25.R
# Zweck: Vorab festgelegte Sensitivitätsanalysen je konfirmatorischer Zielgröße:
#        MW (Mittelwert statt Bestwert, ITT), PP5 und PP7, AEND (Änderungswertmodell),
#        OPAH (ohne %PAH, K22), FAMB (Familiarisierung als Kovariate, Set FAMS),
#        Variante a deskriptiv (Δ je Gruppe und Familiarisierung), Deskription der Sets.
# Schritt der Spezifikation: S17 (Teil E), Umfang nach Nachtrag 2
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S04_aggregat.rds, S05_pah.rds, S08_sets.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S17_Sensitivitaet_2026-09-25.R
# Ausgabe: S17_Sensitivitaet_2026-09-25.txt, Zwischen/S17_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
sets <- lies_zwischen("S08_sets.rds")
schreibe_kopf(
  zweck = "Sensitivitätsanalysen MW, PP5, PP7, AEND, OPAH, FAMB",
  schritt = "S17",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
KI <- konstante_zahl(konst, "KI_NIVEAU")
gruppe <- sets$gruppe

reg <- register_neu("S17_Sensitivitaet_2026-09-25.R")
deskription <- function(x, kennung_m, kennung_sd) {
  setze(reg, kennung_m, mittel(x), "zahl", GRUND_ZU_WENIG)
  setze(reg, kennung_sd, sd_n1(x), "zahl", GRUND_ZU_WENIG)
}
for (z in ZIELE_KONF) {
  cat("\nZielgröße ", z, "\n", sep = "")
  itt <- sets$itt[[z]]
  inf_itt <- inf_von(sets, z, "ITT")
  # Regel 1: MW
  dm <- modelldaten(itt, z, agg, pah, gruppe, sets$fam, "MEAN")
  fit <- if (inf_itt == 1) kq_schaetzung(cbind(1, dm$G, dm$Pre, dm$PAH), dm$Post) else NULL
  g1 <- setze_b1_analyse(reg, "S17", z, "ITT", "MW", dm, fit, inf_itt, KI)
  # Regel 2: PP5 und PP7
  for (s in c(5, 7)) {
    set <- sets$pp[[paste0("PP", s)]][[z]]
    dp <- modelldaten(set, z, agg, pah, gruppe, sets$fam, "BEST")
    inf_pp <- inf_von(sets, z, paste0("PP", s))
    fit <- if (inf_pp == 1) kq_schaetzung(cbind(1, dp$G, dp$Pre, dp$PAH), dp$Post) else NULL
    setze_b1_analyse(reg, "S17", z, paste0("PP", s), "HAUPT", dp, fit, inf_pp, KI)
    # Regel 7: Deskription des IG-Teils
    for (zk in ZEIT_KENN) {
      x <- if (zk == "PRE") dp$Pre[dp$G == 1] else dp$Post[dp$G == 1]
      deskription(x, paste0("S17.M.", z, ".", zk, ".PP", s, "IG.HAUPT"), paste0("S17.SD.", z, ".", zk, ".PP", s, "IG.HAUPT"))
    }
    cat("  PP", s, ": n_IG = ", sum(dp$G == 1), ", n_KG = ", sum(dp$G == 0), ", INF = ", inf_pp, "\n", sep = "")
  }
  # Regel 3: AEND, Regel 4: OPAH im ITT-Set mit BEST
  db <- modelldaten(itt, z, agg, pah, gruppe, sets$fam, "BEST")
  delta <- db$Post - db$Pre
  fit <- if (inf_itt == 1) kq_schaetzung(cbind(1, db$G, db$PAH), delta) else NULL
  setze_b1_analyse(reg, "S17", z, "ITT", "AEND", db, fit, inf_itt, KI)
  fit <- if (inf_itt == 1) kq_schaetzung(cbind(1, db$G, db$Pre), db$Post) else NULL
  setze_b1_analyse(reg, "S17", z, "ITT", "OPAH", db, fit, inf_itt, KI)
  # Regel 5: FAMB im Set FAMS
  fams <- sets$fams[[z]]
  df_ <- modelldaten(fams, z, agg, pah, gruppe, sets$fam, "BEST")
  pruefe(!anyNA(df_$F), "Familiarisierung fehlt im Set FAMS")
  inf_f <- inf_von(sets, z, "FAMS")
  fit <- if (inf_f == 1) kq_schaetzung(cbind(1, df_$G, df_$Pre, df_$PAH, df_$F), df_$Post) else NULL
  gf <- setze_b1_analyse(reg, "S17", z, "FAMS", "FAMB", df_, fit, inf_f, KI)
  for (g in c("IG", "KG")) for (zk in ZEIT_KENN) {
    x <- if (zk == "PRE") df_$Pre[df_$G == as.numeric(g == "IG")] else df_$Post[df_$G == as.numeric(g == "IG")]
    deskription(x, paste0("S17.M.", z, ".", zk, ".FAMS", g, ".FAMB"), paste0("S17.SD.", z, ".", zk, ".FAMS", g, ".FAMB"))
  }
  cat("  ITT: INF = ", inf_itt, if (g1 != "") paste0(" (", g1, ")") else "", ". FAMS: n_IG = ", sum(df_$G == 1),
      ", n_KG = ", sum(df_$G == 0), ", INF = ", inf_f, if (gf != "") paste0(" (", gf, ")") else "", "\n", sep = "")
  # Regel 6: Variante a, deskriptiv, im ITT-Set je Gruppe und F
  for (g in c("IG", "KG")) for (f in 1:2) {
    x <- delta[db$G == as.numeric(g == "IG") & !is.na(db$F) & db$F == f]
    suf <- paste0(".", z, ".DIFF.ITT", g, ".F", f)
    setze(reg, paste0("S17.N", suf), length(x), "anzahl")
    deskription(x, paste0("S17.M", suf), paste0("S17.SD", suf))
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S17", daten$spieler))
register_speichere(reg, "S17")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

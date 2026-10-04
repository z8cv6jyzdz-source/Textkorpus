# =====================================================================
# S16_PerProtokoll_2026-09-25.R
# Zweck: Per-Protokoll-Vergleich (Set PP6, Modell S13 mit Fallzahlregel, nur b1 mit
#        SE, df, t, p, KI und n je Gruppe), Deskription des IG-Teils von PP6 und
#        Antragskriterium AK9 als Einzelwerte Δ = BEST post − BEST prä.
# Schritt der Spezifikation: S16 (Teil E), Umfang nach Nachtrag 2
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S04_aggregat.rds, S05_pah.rds, S08_sets.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S16_PerProtokoll_2026-09-25.R
# Ausgabe: S16_PerProtokoll_2026-09-25.txt, Zwischen/S16_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
sets <- lies_zwischen("S08_sets.rds")
schreibe_kopf(
  zweck = "Per-Protokoll-Vergleich PP6 und Antragskriterium AK9",
  schritt = "S16",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
KI <- konstante_zahl(konst, "KI_NIVEAU")
gruppe <- sets$gruppe

reg <- register_neu("S16_PerProtokoll_2026-09-25.R")
for (z in ZIELE_KONF) {
  # Regel 1: Modell S13 im Set PP6
  pp6 <- sets$pp$PP6[[z]]
  d <- modelldaten(pp6, z, agg, pah, gruppe, sets$fam, "BEST")
  inf <- inf_von(sets, z, "PP6")
  fit <- if (inf == 1) kq_schaetzung(cbind(1, d$G, d$Pre, d$PAH), d$Post) else NULL
  grund <- setze_b1_analyse(reg, "S16", z, "PP6", "HAUPT", d, fit, inf, KI)
  cat("\nZielgröße ", z, ": PP6 n_IG = ", sum(d$G == 1), ", n_KG = ", sum(d$G == 0), ", INF = ", inf,
      if (grund != "") paste0(" (", grund, ")") else "", "\n", sep = "")
  # Regel 2: Deskription des IG-Teils von PP6, unabhängig von INF
  for (zk in ZEIT_KENN) {
    x <- if (zk == "PRE") d$Pre[d$G == 1] else d$Post[d$G == 1]
    setze(reg, paste0("S16.M.", z, ".", zk, ".PP6IG.HAUPT"), mittel(x), "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S16.SD.", z, ".", zk, ".PP6IG.HAUPT"), sd_n1(x), "zahl", GRUND_ZU_WENIG)
  }
  # Regel 3: Antragskriterium AK9, Einzelwerte
  ak9 <- sets$ak9[[z]]
  if (length(ak9) > 0) {
    da <- modelldaten(ak9, z, agg, pah, gruppe, sets$fam, "BEST")
    for (i in seq_len(nrow(da))) {
      setze(reg, paste0("S16.DIFF.", z, ".DIFF.P", da$Code[i], ".AK9"), da$Post[i] - da$Pre[i], "zahl")
    }
  }
  cat("  AK9: ", length(ak9), " Spieler\n", sep = "")
}
spieler <- daten$spieler
spieler$AK9 <- sets$ak9
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S16", spieler))
register_speichere(reg, "S16")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

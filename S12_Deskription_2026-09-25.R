# =====================================================================
# S12_Deskription_2026-09-25.R
# Zweck: Stichprobenbeschreibung in der Analysepopulation ANA (Alter, Körperhöhe,
#        Körpermasse, %PAH), Familiarisierung je Gruppe, Ausgangsunterschied d
#        ohne J in den Mengen BASE und ITT (K26), n, M, SD der Bestwerte prä
#        über alle Fälle und prä und post im ITT-Set (K29). Keine Tests.
# Schritt der Spezifikation: S12 (Teil D), Regel 2 wird in S14 Regel 5 angewandt
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S04_aggregat.rds, S05_pah.rds, S08_sets.rds
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S12_Deskription_2026-09-25.R
# Ausgabe: S12_Deskription_2026-09-25.txt, Zwischen/S12_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
sets <- lies_zwischen("S08_sets.rds")
schreibe_kopf(
  zweck = "Deskription: Stichprobe, Ausgangswerte, Prä und Post",
  schritt = "S12",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
kenn <- lies_kennungen()
p <- daten$personen
codes <- p$Code
gruppe <- sets$gruppe

best_von <- function(spieler, z, zk) {
  a <- agg[agg$Ziel == z & agg$ZeitKenn == zk, ]
  b <- a$BEST[match(spieler, a$Code)]
  pruefe(length(b) == length(spieler), "BEST unvollständig")
  b
}

reg <- register_neu("S12_Deskription_2026-09-25.R")

# Regel 1: Stichprobe in ANA
groessen <- list(AGE = p$Alter_prae, HGT = p$Koerperhoehe_prae, MASS = p$Koerpermasse_prae,
                 PAH = pah$PAH[match(codes, pah$Code)])
for (g in c("IG", "KG")) {
  s <- sets$ana[[g]]
  for (gr in names(groessen)) {
    x <- groessen[[gr]][match(s, codes)]
    x <- x[!is.na(x)]
    setze(reg, paste0("S12.N.", gr, ".PRE.ANA", g, ".X"), length(x), "anzahl")
    setze(reg, paste0("S12.M.", gr, ".PRE.ANA", g, ".X"), mittel(x), "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S12.SD.", gr, ".PRE.ANA", g, ".X"), sd_n1(x), "zahl", GRUND_ZU_WENIG)
  }
  f <- p$Familiarisierung[p$Gruppe == g]
  setze(reg, paste0("S12.NFAM1.FAM.PRE.", g, ".X"), sum(f == 1, na.rm = TRUE), "anzahl")
  setze(reg, paste0("S12.NFAM2.FAM.PRE.", g, ".X"), sum(f == 2, na.rm = TRUE), "anzahl")
  setze(reg, paste0("S12.NFAMNA.FAM.PRE.", g, ".X"), sum(is.na(f)), "anzahl")
}

# Regel 3 und 4
d_wert <- function(x_ig, x_kg) {
  sp <- sd_pool(x_ig, x_kg)
  if (is.na(sp)) return(list(d = NA_real_, grund = GRUND_ZU_WENIG))
  if (sp == 0) return(list(d = NA_real_, grund = GRUND_KONSTANT))
  list(d = (mittel(x_ig) - mittel(x_kg)) / sp, grund = "")
}
for (z in ZIELE_SIEBEN) {
  # BASE: alle Fälle mit BEST prä, je Gruppe
  b_pre <- best_von(codes, z, "PRE")
  ig_base <- b_pre[gruppe[codes] == "IG" & !is.na(b_pre)]
  kg_base <- b_pre[gruppe[codes] == "KG" & !is.na(b_pre)]
  dw <- d_wert(ig_base, kg_base)
  setze(reg, paste0("S12.D.", z, ".PRE.BASE.HAUPT"), dw$d, "zahl", dw$grund)
  for (g in c("IG", "KG")) {
    x <- if (g == "IG") ig_base else kg_base
    setze(reg, paste0("S12.N.", z, ".PRE.", g, ".HAUPT"), length(x), "anzahl")
    setze(reg, paste0("S12.M.", z, ".PRE.", g, ".HAUPT"), mittel(x), "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S12.SD.", z, ".PRE.", g, ".HAUPT"), sd_n1(x), "zahl", GRUND_ZU_WENIG)
  }
  # ITT-Set
  itt <- sets$itt[[z]]
  ig_itt <- itt[gruppe[itt] == "IG"]
  kg_itt <- itt[gruppe[itt] == "KG"]
  dw <- d_wert(best_von(ig_itt, z, "PRE"), best_von(kg_itt, z, "PRE"))
  setze(reg, paste0("S12.D.", z, ".PRE.ITT.HAUPT"), dw$d, "zahl", dw$grund)
  for (g in c("IG", "KG")) for (zk in ZEIT_KENN) {
    x <- best_von(if (g == "IG") ig_itt else kg_itt, z, zk)
    pruefe(!anyNA(x), "BEST fehlt im ITT-Set")
    setze(reg, paste0("S12.N.", z, ".", zk, ".ITT", g, ".HAUPT"), length(x), "anzahl")
    setze(reg, paste0("S12.M.", z, ".", zk, ".ITT", g, ".HAUPT"), mittel(x), "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S12.SD.", z, ".", zk, ".ITT", g, ".HAUPT"), sd_n1(x), "zahl", GRUND_ZU_WENIG)
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S12", daten$spieler))
register_speichere(reg, "S12")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

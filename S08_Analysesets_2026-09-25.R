# =====================================================================
# S08_Analysesets_2026-09-25.R
# Zweck: Analysesets je Zielgröße (ITT, PP5, PP6, PP7, AK9, FAMS), Fallzahlregel
#        INF, Mitgliedschaften je Spieler, Teilnehmerfluss, CONSORT-Box-6-Klassen,
#        Erhebungs- und Attritionsanteile (K27), Analysepopulation ANA (Nachtrag 2).
# Schritt der Spezifikation: S08 (Teil B)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S02_versuche.rds, S04_aggregat.rds, S05_pah.rds, S07_adhaerenz.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S08_Analysesets_2026-09-25.R
# Ausgabe: S08_Analysesets_2026-09-25.txt, Zwischen/S08_sets.rds, Zwischen/S08_mitglied.csv,
#          Zwischen/S08_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
adh <- lies_zwischen("S07_adhaerenz.rds")
schreibe_kopf(
  zweck = "Analysesets, Fallzahlregel, Teilnehmerfluss, Box 6, Anteile, Menge ANA",
  schritt = "S08",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
N_MIN <- konstante_zahl(konst, "N_MIN_JE_GRUPPE")
PP_HAUPT <- konstante_zahl(konst, "PP_SCHWELLE_HAUPT")
PP_SENS <- as.numeric(strsplit(trimws(konstante_text(konst, "PP_SCHWELLEN_SENSITIV")), "\\s+")[[1]])
AK <- konstante_zahl(konst, "AK_SCHWELLE")
pruefe(PP_HAUPT == 6 && identical(PP_SENS, c(5, 7)) && AK == 9,
       "Schwellen der Konstanten passen nicht zu den Kennungen PP5, PP6, PP7, AK9")
cat("\nKonstanten: Fallzahlregel n >= ", N_MIN, " je Gruppe, PP-Schwellen ", paste(c(PP_SENS[1], PP_HAUPT, PP_SENS[2]), collapse = " "),
    ", Antragskriterium ", AK, "\n", sep = "")

p <- daten$personen
codes <- p$Code
gruppe <- p$Gruppe
names(gruppe) <- codes
ig <- codes[gruppe == "IG"]
kg <- codes[gruppe == "KG"]

best <- function(cd, z, zk) {
  a <- agg[agg$Code == cd & agg$Ziel == z & agg$ZeitKenn == zk, ]
  pruefe(nrow(a) == 1, "Aggregat nicht eindeutig")
  a$BEST
}
hat_best <- function(z, zk) vapply(codes, function(cd) !is.na(best(cd, z, zk)), TRUE)
hat_pah <- !is.na(pah$PAH[match(codes, pah$Code)])
names(hat_pah) <- codes
ganz <- adh$GANZ[match(codes, adh$Code)]
ganz[!(codes %in% ig)] <- NA_integer_
ganz[codes %in% adh$Code[adh$kein_Listenplatz]] <- NA_integer_
names(ganz) <- codes
fam <- p$Familiarisierung
names(fam) <- codes

# Regel 1: ITT-Sets
itt <- list()
for (z in ZIELE_SIEBEN) {
  itt[[z]] <- codes[hat_best(z, "PRE") & hat_best(z, "POST") & hat_pah]
}
# Regel 4 bis 6 für die konfirmatorischen Zielgrößen
pp <- list()
ak9 <- list()
fams <- list()
for (z in ZIELE_KONF) {
  for (s in c(5, 6, 7)) {
    pp[[paste0("PP", s)]][[z]] <- itt[[z]][gruppe[itt[[z]]] == "KG" | (!is.na(ganz[itt[[z]]]) & ganz[itt[[z]]] >= s)]
  }
  ak9[[z]] <- itt[[z]][gruppe[itt[[z]]] == "IG" & !is.na(ganz[itt[[z]]]) & ganz[itt[[z]]] >= AK]
  fams[[z]] <- itt[[z]][!is.na(fam[itt[[z]]])]
}
n_g <- function(set, g) sum(gruppe[set] == g)
inf <- function(set) as.integer(n_g(set, "IG") >= N_MIN && n_g(set, "KG") >= N_MIN)

cat("\nSetgrößen (IG / KG):\n")
for (z in ZIELE_SIEBEN) cat(sprintf("  ITT %-4s %2d / %2d\n", z, n_g(itt[[z]], "IG"), n_g(itt[[z]], "KG")))
for (z in ZIELE_KONF) {
  cat(sprintf("  %-4s PP5 %2d  PP6 %2d  PP7 %2d  AK9 %2d  FAMS %2d / %2d\n", z,
              n_g(pp$PP5[[z]], "IG"), n_g(pp$PP6[[z]], "IG"), n_g(pp$PP7[[z]], "IG"), length(ak9[[z]]),
              n_g(fams[[z]], "IG"), n_g(fams[[z]], "KG")))
}

reg <- register_neu("S08_Analysesets_2026-09-25.R")
for (z in ZIELE_SIEBEN) {
  setze(reg, paste0("S08.N.", z, ".X.ITTIG.X"), n_g(itt[[z]], "IG"), "anzahl")
  setze(reg, paste0("S08.N.", z, ".X.ITTKG.X"), n_g(itt[[z]], "KG"), "anzahl")
}
inf_tab <- data.frame(Ziel = character(0), Set = character(0), INF = integer(0), stringsAsFactors = FALSE)
for (z in ZIELE_KONF) {
  for (s in c(5, 6, 7)) setze(reg, paste0("S08.N.", z, ".X.PP", s, "IG.X"), n_g(pp[[paste0("PP", s)]][[z]], "IG"), "anzahl")
  setze(reg, paste0("S08.N.", z, ".X.AK9IG.X"), length(ak9[[z]]), "anzahl")
  setze(reg, paste0("S08.N.", z, ".X.FAMSIG.X"), n_g(fams[[z]], "IG"), "anzahl")
  setze(reg, paste0("S08.N.", z, ".X.FAMSKG.X"), n_g(fams[[z]], "KG"), "anzahl")
  sets <- list(ITT = itt[[z]], PP5 = pp$PP5[[z]], PP6 = pp$PP6[[z]], PP7 = pp$PP7[[z]], FAMS = fams[[z]])
  for (nm in names(sets)) {
    i <- inf(sets[[nm]])
    setze(reg, paste0("S08.INF.", z, ".X.", nm, ".X"), i, "merkmal")
    inf_tab[nrow(inf_tab) + 1, ] <- list(z, nm, i)
  }
}
# Regel 7: Mitgliedschaften
mitglied <- data.frame(Code = codes, stringsAsFactors = FALSE)
for (z in ZIELE_SIEBEN) {
  mitglied[[paste0("ITT_", z)]] <- as.integer(codes %in% itt[[z]])
  for (cd in codes) setze(reg, paste0("S08.MITGL.", z, ".X.P", cd, ".ITT"), as.integer(cd %in% itt[[z]]), "merkmal")
}
for (z in ZIELE_KONF) {
  sets <- list(PP5 = pp$PP5[[z]], PP6 = pp$PP6[[z]], PP7 = pp$PP7[[z]], AK9 = ak9[[z]], FAMS = fams[[z]])
  for (nm in names(sets)) {
    mitglied[[paste0(nm, "_", z)]] <- as.integer(codes %in% sets[[nm]])
    for (cd in codes) setze(reg, paste0("S08.MITGL.", z, ".X.P", cd, ".", nm), as.integer(cd %in% sets[[nm]]), "merkmal")
  }
}

# Regel 8: Teilnehmerfluss
mengen <- list(IG = ig, KG = kg, VA = codes[p$Verein == "A"], VB = codes[p$Verein == "B"], VC = codes[p$Verein == "C"])
pre_gueltig <- v$Code[v$gueltig == 1 & v$ZeitKenn == "PRE"]
status <- p$Status
names(status) <- codes
for (m in names(mengen)) {
  s <- mengen[[m]]
  setze(reg, paste0("S08.FLZUG.X.X.", m, ".X"), length(s), "anzahl")
  setze(reg, paste0("S08.FLPRE.X.X.", m, ".X"), sum(s %in% pre_gueltig), "anzahl")
  setze(reg, paste0("S08.FLAUSG.X.X.", m, ".X"), sum(status[s] == "ausgewertet"), "anzahl")
  setze(reg, paste0("S08.FLNANG.X.X.", m, ".X"), sum(status[s] == "nicht angetreten"), "anzahl")
}
for (g in c("IG", "KG")) {
  s <- mengen[[g]]
  for (z in ZIELE_SIEBEN) {
    setze(reg, paste0("S08.FLITT.", z, ".X.", g, ".X"), sum(s %in% itt[[z]]), "anzahl")
    setze(reg, paste0("S08.FLOPRE.", z, ".X.", g, ".X"), sum(!hat_best(z, "PRE")[s]), "anzahl")
    setze(reg, paste0("S08.FLOPOST.", z, ".X.", g, ".X"), sum(!hat_best(z, "POST")[s]), "anzahl")
  }
  setze(reg, paste0("S08.FLOPAH.PAH.X.", g, ".X"), sum(!hat_pah[s]), "anzahl")
}
# Regel 9: Box 6
ne <- ig[!is.na(ganz[ig]) & ganz[ig] < PP_HAUPT]
nmeld <- adh$NMELD[match(ig, adh$Code)]
names(nmeld) <- ig
setze(reg, "S08.B6NE.X.X.IG.X", length(ne), "anzahl")
setze(reg, "S08.B6NEKM.X.X.IG.X", sum(nmeld[ne] == 0), "anzahl")
setze(reg, "S08.B6IF.X.X.IG.X", sum(adh$kein_Listenplatz), "anzahl")
for (g in c("IG", "KG")) {
  s <- mengen[[g]]
  setze(reg, paste0("S08.B6FK.X.X.", g, ".X"), sum(!hat_pah[s]), "anzahl")
  setze(reg, paste0("S08.B6NA.X.X.", g, ".X"), sum(status[s] == "nicht angetreten"), "anzahl")
}
# Regel 10: Anteile
mengen3 <- list(IG = ig, KG = kg, ALL = codes)
for (z in ZIELE_SIEBEN) {
  beide <- hat_best(z, "PRE") & hat_best(z, "POST")
  for (m in names(mengen3)) {
    s <- mengen3[[m]]
    setze(reg, paste0("S08.ANT.", z, ".X.", m, ".X"), sum(beide[s]) / length(s), "zahl")
  }
}
for (m in names(mengen3)) {
  s <- mengen3[[m]]
  setze(reg, paste0("S08.ANTTN.X.X.", m, ".X"), sum(status[s] == "ausgewertet") / length(s), "zahl")
}
# Regel 11: Analysepopulation ANA
in_irgendeinem_itt <- codes[vapply(codes, function(cd) any(vapply(ZIELE_SIEBEN, function(z) cd %in% itt[[z]], TRUE)), TRUE)]
ana <- list(IG = in_irgendeinem_itt[gruppe[in_irgendeinem_itt] == "IG"],
            KG = in_irgendeinem_itt[gruppe[in_irgendeinem_itt] == "KG"])
cat("Analysepopulation ANA: IG ", length(ana$IG), ", KG ", length(ana$KG), "\n", sep = "")

register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S08", daten$spieler))
sets <- list(itt = itt, pp = pp, ak9 = ak9, fams = fams, inf = inf_tab, ana = ana, gruppe = gruppe,
             ganz = ganz, fam = fam, N_MIN = N_MIN)
saveRDS(sets, pfad_zwischen("S08_sets.rds"))
write.csv(mitglied, pfad_zwischen("S08_mitglied.csv"), row.names = FALSE, fileEncoding = "UTF-8")
register_speichere(reg, "S08")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

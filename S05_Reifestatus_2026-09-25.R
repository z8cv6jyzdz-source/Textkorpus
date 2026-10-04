# =====================================================================
# S05_Reifestatus_2026-09-25.R
# Zweck: Prozentsatz der prognostizierten Erwachsenengröße (%PAH) je Spieler
#        nach Khamis und Roche (1994), Tab. 1 unverändert (O1), lineare
#        Interpolation der Koeffizienten zwischen Halbjahreszeilen (O2),
#        Einheiten Zoll und Pfund (K3), fehlende Elterngröße → fehlend (K2).
# Schritt der Spezifikation: S05 (Teil A)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds (Personendaten, Prüfsummen im Kopf von S01)
#   Spezifikation_2026-09-24_Koeffizienten_KR.csv
#     1eb1ffabf2b5e8949c752ca243254fcf93b77b4c368551fb2d6f5744abcd0c5f
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S05_Reifestatus_2026-09-25.R
# Ausgabe: S05_Reifestatus_2026-09-25.txt, Zwischen/S05_pah.rds, Zwischen/S05_pah.csv,
#          Zwischen/S05_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
schreibe_kopf(
  zweck = "Reifestatus %PAH nach Khamis und Roche",
  schritt = "S05",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Koeffizienten_KR.csv" = unname(ANLAGEN["_Koeffizienten_KR.csv"]),
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
ZOLL <- konstante_zahl(konst, "ZOLL_IN_CM")
PFUND <- konstante_zahl(konst, "PFUND_IN_KG")
ALTER_MIN <- konstante_zahl(konst, "KR_ALTER_MIN")
ALTER_MAX <- konstante_zahl(konst, "KR_ALTER_MAX")
RASTER <- konstante_zahl(konst, "KR_RASTER")
PROZENT <- konstante_zahl(konst, "PROZENT_FAKTOR")
cat("\nKonstanten: Zoll = ", ZOLL, " cm, Pfund = ", PFUND, " kg, Gültigkeit ", ALTER_MIN, " bis ", ALTER_MAX,
    " Jahre, Raster ", RASTER, " Jahre\n", sep = "")

ko <- lies_anlage("_Koeffizienten_KR.csv")
pruefe_spalten(ko, c("alter_jahre", "beta0", "stature_in", "weight_lb", "midparent_in"), "_Koeffizienten_KR.csv")
for (sp in names(ko)) ko[[sp]] <- als_zahl(ko[[sp]], paste0("Koeffizienten ", sp), leer_erlaubt = FALSE)
pruefe(!any(duplicated(ko$alter_jahre)), "Koeffizienten: doppelte Alterszeilen")
ko <- ko[order(ko$alter_jahre), ]
pruefe(isTRUE(all.equal(ko$alter_jahre, seq(ALTER_MIN, ALTER_MAX, by = RASTER))),
       "Koeffizienten: Alterszeilen nicht das Raster von ", ALTER_MIN, " bis ", ALTER_MAX)
cat("Koeffiziententabelle: ", nrow(ko), " Zeilen von ", min(ko$alter_jahre), " bis ", max(ko$alter_jahre), " Jahren\n", sep = "")

p <- daten$personen
erg <- data.frame(Code = p$Code, Gruppe = p$Gruppe, Alter = p$Alter_prae, S_in = p$Koerperhoehe_prae / ZOLL,
                  W_lb = p$Koerpermasse_prae / PFUND, Mutter_in = p$Groesse_Mutter / ZOLL,
                  Vater_in = p$Groesse_Vater / ZOLL, stringsAsFactors = FALSE)
erg$MP_in <- (erg$Mutter_in + erg$Vater_in) / 2
erg$Grund_MP <- ifelse(is.na(erg$MP_in), GRUND_EINGANG, "")
erg$a_lo <- NA_real_
erg$w <- NA_real_
erg$beta0 <- NA_real_
erg$beta1 <- NA_real_
erg$beta2 <- NA_real_
erg$beta3 <- NA_real_
erg$PAS_in <- NA_real_
erg$PAH <- NA_real_
erg$Grund_PAH <- ""

for (i in seq_len(nrow(erg))) {
  if (is.na(erg$S_in[i]) || is.na(erg$W_lb[i]) || is.na(erg$MP_in[i])) {
    erg$Grund_PAH[i] <- GRUND_EINGANG
    next
  }
  alter <- erg$Alter[i]
  if (alter < ALTER_MIN || alter > ALTER_MAX) {
    erg$Grund_PAH[i] <- GRUND_BEREICH
    next
  }
  ip <- interpoliere_kr(ko, alter, RASTER)
  erg$a_lo[i] <- ip$a_lo
  erg$w[i] <- ip$w
  b <- ip$beta
  erg$beta0[i] <- b[1]
  erg$beta1[i] <- b[2]
  erg$beta2[i] <- b[3]
  erg$beta3[i] <- b[4]
  pas <- khamis_roche_pas(b[1], b[2], b[3], b[4], erg$S_in[i], erg$W_lb[i], erg$MP_in[i])
  pruefe(is.finite(pas) && pas > 0, "Vorhergesagte Erwachsenengröße nicht positiv für ", erg$Code[i])
  erg$PAS_in[i] <- pas
  erg$PAH[i] <- PROZENT * erg$S_in[i] / pas
}

cat("Spieler: ", nrow(erg), ", mit %PAH: ", sum(!is.na(erg$PAH)), ", ohne %PAH: ", sum(is.na(erg$PAH)), "\n", sep = "")
for (i in which(is.na(erg$PAH))) cat("  ohne %PAH: ", erg$Code[i], " Grund: ", erg$Grund_PAH[i], "\n", sep = "")

reg <- register_neu("S05_Reifestatus_2026-09-25.R")
for (i in seq_len(nrow(erg))) {
  cd <- erg$Code[i]
  setze(reg, paste0("S05.MP.PAH.PRE.P", cd, ".X"), erg$MP_in[i], "zahl", erg$Grund_MP[i])
  setze(reg, paste0("S05.PAS.PAH.PRE.P", cd, ".X"), erg$PAS_in[i], "zahl", erg$Grund_PAH[i])
  setze(reg, paste0("S05.PAH.PAH.PRE.P", cd, ".X"), erg$PAH[i], "zahl", erg$Grund_PAH[i])
}
setze(reg, "S05.NPAH.PAH.PRE.IG.X", sum(!is.na(erg$PAH) & erg$Gruppe == "IG"), "anzahl")
setze(reg, "S05.NPAH.PAH.PRE.KG.X", sum(!is.na(erg$PAH) & erg$Gruppe == "KG"), "anzahl")
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S05", daten$spieler))

saveRDS(erg, pfad_zwischen("S05_pah.rds"))
write.csv(erg, pfad_zwischen("S05_pah.csv"), row.names = FALSE, fileEncoding = "UTF-8", na = "")
register_speichere(reg, "S05")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

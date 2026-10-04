# =====================================================================
# S10_Messguete_2026-09-25.R
# Zweck: Typischer Messfehler TE als gepoolte Innerspieler-SD (O5) mit
#        χ²-Konfidenzintervall (K12), Seitenmittel aus beidseitig gültigen
#        Versuchsnummern (K15), CV (K13), Zwischen-Athleten-SD S (O6), SESOI,
#        Verhältnis TE/SESOI und Merkmal FLEINZ, TE je Verein.
# Schritt der Spezifikation: S10 (Teil C), Regel 7 entfällt (Nachtrag 2)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S02_versuche.rds, S04_aggregat.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S10_Messguete_2026-09-25.R
# Ausgabe: S10_Messguete_2026-09-25.txt, Zwischen/S10_messguete.rds, Zwischen/S10_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
agg <- lies_zwischen("S04_aggregat.rds")
schreibe_kopf(
  zweck = "Messgüte: typischer Messfehler, SESOI und abgeleitete Größen",
  schritt = "S10",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
SESOI_FAKTOR <- konstante_zahl(konst, "SESOI_FAKTOR")
PROZENT <- konstante_zahl(konst, "PROZENT_FAKTOR")
KI <- konstante_zahl(konst, "KI_NIVEAU")
cat("\nKonstanten: SESOI-Faktor = ", SESOI_FAKTOR, ", KI-Niveau = ", KI, "\n", sep = "")

p <- daten$personen
codes <- p$Code
verein <- p$Verein
names(verein) <- codes
gv <- v[v$gueltig == 1, ]

# Liste der Versuchswerte je Spieler (Regel 1) oder der Paarmittel m_ij (Regel 2, CM)
werte_je_spieler <- function(z, zk, spieler) {
  erg <- list()
  for (cd in spieler) {
    if (z == "CM") {
      l <- gv[gv$Code == cd & gv$ZeitKenn == zk & gv$Ziel == "CL", ]
      r <- gv[gv$Code == cd & gv$ZeitKenn == zk & gv$Ziel == "CR", ]
      gemeinsam <- intersect(l$Versuch, r$Versuch)
      if (length(gemeinsam) == 0) next
      m <- (l$Wert[match(gemeinsam, l$Versuch)] + r$Wert[match(gemeinsam, r$Versuch)]) / 2
      erg[[cd]] <- m
    } else {
      w <- gv$Wert[gv$Code == cd & gv$ZeitKenn == zk & gv$Ziel == z]
      if (length(w) == 0) next
      erg[[cd]] <- w
    }
  }
  erg
}

reg <- register_neu("S10_Messguete_2026-09-25.R")
messguete <- data.frame(Ziel = character(0), ZeitKenn = character(0), TE = numeric(0), DFTE = integer(0),
                        NTE = integer(0), SB = numeric(0), NSB = integer(0), SESOI = numeric(0),
                        stringsAsFactors = FALSE)
for (z in ZIELE_SIEBEN) for (zk in ZEIT_KENN) {
  te <- te_gepoolt(werte_je_spieler(z, zk, codes))
  grund_te <- if (is.na(te$te)) GRUND_ZU_WENIG else ""
  setze(reg, paste0("S10.TE.", z, ".", zk, ".ALL.X"), te$te, "zahl", grund_te)
  telo <- if (is.na(te$te)) NA_real_ else te$te * sqrt(te$df / chi2_quantil(1 - (1 - KI) / 2, te$df))
  tehi <- if (is.na(te$te)) NA_real_ else te$te * sqrt(te$df / chi2_quantil((1 - KI) / 2, te$df))
  setze(reg, paste0("S10.TELO.", z, ".", zk, ".ALL.X"), telo, "zahl", GRUND_EINGANG)
  setze(reg, paste0("S10.TEHI.", z, ".", zk, ".ALL.X"), tehi, "zahl", GRUND_EINGANG)
  setze(reg, paste0("S10.DFTE.", z, ".", zk, ".ALL.X"), te$df, "anzahl")
  setze(reg, paste0("S10.NTE.", z, ".", zk, ".ALL.X"), te$n, "anzahl")
  # Regel 5 und 6: S und SESOI aus den BEST-Werten, Ausgabe nur prä (Nachtrag 2)
  b <- agg$BEST[agg$Ziel == z & agg$ZeitKenn == zk]
  b <- b[!is.na(b)]
  sb <- sd_n1(b)
  sesoi <- if (is.na(sb)) NA_real_ else SESOI_FAKTOR * sb
  if (zk == "PRE") {
    cv <- if (is.na(te$te)) NA_real_ else PROZENT * te$te / te$mittel_alle
    setze(reg, paste0("S10.CV.", z, ".PRE.ALL.X"), cv, "zahl", GRUND_EINGANG)
    setze(reg, paste0("S10.SB.", z, ".PRE.ALL.X"), sb, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S10.NSB.", z, ".PRE.ALL.X"), length(b), "anzahl")
    setze(reg, paste0("S10.SESOI.", z, ".PRE.ALL.X"), sesoi, "zahl", GRUND_EINGANG)
    if (is.na(te$te) || is.na(sesoi)) {
      setze(reg, paste0("S10.RTS.", z, ".PRE.ALL.X"), NA_real_, "zahl", GRUND_EINGANG)
      setze(reg, paste0("S10.FLEINZ.", z, ".PRE.ALL.X"), NA_real_, "merkmal", GRUND_EINGANG)
    } else if (sesoi == 0) {
      setze(reg, paste0("S10.RTS.", z, ".PRE.ALL.X"), NA_real_, "zahl", GRUND_KONSTANT)
      setze(reg, paste0("S10.FLEINZ.", z, ".PRE.ALL.X"), as.integer(te$te > sesoi), "merkmal")
    } else {
      setze(reg, paste0("S10.RTS.", z, ".PRE.ALL.X"), te$te / sesoi, "zahl")
      setze(reg, paste0("S10.FLEINZ.", z, ".PRE.ALL.X"), as.integer(te$te > sesoi), "merkmal")
    }
  }
  messguete[nrow(messguete) + 1, ] <- list(z, zk, te$te, te$df, te$n, sb, length(b), sesoi)
  # Regel 10: je Verein
  for (vn in c("A", "B", "C")) {
    tev <- te_gepoolt(werte_je_spieler(z, zk, codes[verein == vn]))
    setze(reg, paste0("S10.TE.", z, ".", zk, ".V", vn, ".X"), tev$te, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S10.DFTE.", z, ".", zk, ".V", vn, ".X"), tev$df, "anzahl")
    setze(reg, paste0("S10.NTE.", z, ".", zk, ".V", vn, ".X"), tev$n, "anzahl")
  }
}
cat("\nTE-Mengen (Spieler, df) je Zielgröße und Zeitpunkt:\n")
for (i in seq_len(nrow(messguete))) {
  cat(sprintf("  %-4s %-5s NTE %2d  DFTE %3d  NSB %2d\n", messguete$Ziel[i], messguete$ZeitKenn[i],
              messguete$NTE[i], messguete$DFTE[i], messguete$NSB[i]))
}

register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S10", daten$spieler))
saveRDS(messguete, pfad_zwischen("S10_messguete.rds"))
register_speichere(reg, "S10")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

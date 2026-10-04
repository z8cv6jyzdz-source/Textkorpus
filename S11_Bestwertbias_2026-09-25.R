# =====================================================================
# S11_Bestwertbias_2026-09-25.R
# Zweck: Bestwert-Bias des dritten Versuchs, gemessen: Δ = best(x1, x2, x3) −
#        best(x1, x2) über alle Spieler mit gültigen Versuchen 1, 2 und 3,
#        je Zielgröße und Zeitpunkt. n, Mittel von Δ und Mittel von Δ / SESOI.
# Schritt der Spezifikation: S11 (Teil C)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S02_versuche.rds, S10_messguete.rds
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S11_Bestwertbias_2026-09-25.R
# Ausgabe: S11_Bestwertbias_2026-09-25.txt, Zwischen/S11_ergebnisse.rds
# Rückfrage R1 (Rückfragenprotokoll): SESOI für den Zeitpunkt POST. Lesart (a),
#   Antwort des Verfassers vom 2026-09-25, gesetzt in LESART_R1.
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

# Lesart der Rückfrage R1: "a" SESOI post intern nach S10 Regel 5 und 6 aus den BEST post,
# "b" SESOI prä auch für POST, "c" DSESOI post fehlend mit Grund Eingang fehlt, "offen" Abbruch
LESART_R1 <- "a"

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
mg <- lies_zwischen("S10_messguete.rds")
schreibe_kopf(
  zweck = "Bestwert-Bias des dritten Versuchs",
  schritt = "S11",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
kenn <- lies_kennungen()
pruefe(LESART_R1 %in% c("a", "b", "c"), "Rückfrage R1 (SESOI für POST in S11) ist offen. Lesart nicht gesetzt.")
cat("\nLesart R1 für das SESOI zum Zeitpunkt POST: ", LESART_R1, "\n", sep = "")

gv <- v[v$gueltig == 1, ]
codes <- daten$spieler$ALLE

sesoi_von <- function(z, zk) {
  zk_sesoi <- if (LESART_R1 == "b") "PRE" else zk
  s <- mg$SESOI[mg$Ziel == z & mg$ZeitKenn == zk_sesoi]
  pruefe(length(s) == 1, "SESOI nicht eindeutig für ", z, " ", zk)
  s
}

reg <- register_neu("S11_Bestwertbias_2026-09-25.R")
for (z in ZIELE_SECHS) for (zk in ZEIT_KENN) {
  delta <- numeric(0)
  for (cd in codes) {
    w <- gv[gv$Code == cd & gv$ZeitKenn == zk & gv$Ziel == z, ]
    if (nrow(w) != 3 || !setequal(w$Versuch, 1:3)) next
    x <- w$Wert[match(1:3, w$Versuch)]
    delta <- c(delta, bestwert(x, z) - bestwert(x[1:2], z))
  }
  n <- length(delta)
  dmean <- mittel(delta)
  setze(reg, paste0("S11.N.", z, ".", zk, ".ALL.X"), n, "anzahl")
  setze(reg, paste0("S11.DMEAN.", z, ".", zk, ".ALL.X"), dmean, "zahl", GRUND_ZU_WENIG)
  kenn_ds <- paste0("S11.DSESOI.", z, ".", zk, ".ALL.X")
  if (zk == "POST" && LESART_R1 == "c") {
    setze(reg, kenn_ds, NA_real_, "zahl", GRUND_EINGANG)
  } else {
    sesoi <- sesoi_von(z, zk)
    if (is.na(dmean) || is.na(sesoi)) {
      setze(reg, kenn_ds, NA_real_, "zahl", GRUND_EINGANG)
    } else if (sesoi == 0) {
      setze(reg, kenn_ds, NA_real_, "zahl", GRUND_KONSTANT)
    } else {
      setze(reg, kenn_ds, dmean / sesoi, "zahl")
    }
  }
  cat(sprintf("  %-4s %-5s Spieler mit drei gültigen Versuchen: %2d\n", z, zk, n))
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S11", daten$spieler))
register_speichere(reg, "S11")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

# =====================================================================
# S04_Aggregation_2026-09-25.R
# Zweck: Je Spieler, Zeitpunkt und Zielgröße die Zahl gültiger Versuche k,
#        den Bestwert BEST und den Mittelwert MEAN bilden. 505-Seitenmittel CM
#        aus den Seitenbestwerten und Seitenmitteln, nur wenn beide Seiten k ≥ 1.
# Schritt der Spezifikation: S04 (Teil A)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, Zwischen/S02_versuche.rds (aus S01 und S02)
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S04_Aggregation_2026-09-25.R
# Ausgabe: S04_Aggregation_2026-09-25.txt, Zwischen/S04_aggregat.rds,
#          Zwischen/S04_aggregat.csv, Zwischen/S04_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
schreibe_kopf(
  zweck = "Aggregation je Spieler: k, Bestwert, Mittelwert, 505-Seitenmittel",
  schritt = "S04",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
kenn <- lies_kennungen()
codes <- daten$spieler$ALLE

# Regel 1 bis 3 je Spieler × Zeitpunkt × Zielgröße (sechs Zielgrößen)
agg <- expand.grid(Code = codes, ZeitKenn = ZEIT_KENN, Ziel = ZIELE_SIEBEN, stringsAsFactors = FALSE)
agg$K <- NA_integer_
agg$BEST <- NA_real_
agg$MEAN <- NA_real_
agg$Grund <- ""
gv <- v[v$gueltig == 1, ]
for (i in seq_len(nrow(agg))) {
  if (agg$Ziel[i] == "CM") next
  w <- gv$Wert[gv$Code == agg$Code[i] & gv$ZeitKenn == agg$ZeitKenn[i] & gv$Ziel == agg$Ziel[i]]
  pruefe(length(w) <= 3, "Mehr als drei gültige Versuche: ", agg$Code[i], " ", agg$Ziel[i])
  agg$K[i] <- length(w)
  if (length(w) == 0) {
    agg$Grund[i] <- GRUND_ZU_WENIG
  } else {
    agg$BEST[i] <- bestwert(w, agg$Ziel[i])
    agg$MEAN[i] <- mittel(w)
  }
}
# Regel 4: Seitenmittel CM
for (i in which(agg$Ziel == "CM")) {
  l <- agg[agg$Code == agg$Code[i] & agg$ZeitKenn == agg$ZeitKenn[i] & agg$Ziel == "CL", ]
  r <- agg[agg$Code == agg$Code[i] & agg$ZeitKenn == agg$ZeitKenn[i] & agg$Ziel == "CR", ]
  pruefe(nrow(l) == 1 && nrow(r) == 1, "Seitenwerte nicht eindeutig")
  if (l$K >= 1 && r$K >= 1) {
    agg$BEST[i] <- (l$BEST + r$BEST) / 2
    agg$MEAN[i] <- (l$MEAN + r$MEAN) / 2
  } else {
    agg$Grund[i] <- GRUND_EINGANG
  }
}
# Konsistenz: MEAN vorhanden genau dann, wenn BEST vorhanden (S08 Regel 1)
pruefe(all(is.na(agg$BEST) == is.na(agg$MEAN)), "BEST und MEAN nicht gleich vorhanden")

cat("\nAggregate: ", nrow(agg), " Zellen, davon mit Wert: ", sum(!is.na(agg$BEST)), "\n", sep = "")
for (z in ZIELE_SIEBEN) for (zk in ZEIT_KENN) {
  s <- agg$Ziel == z & agg$ZeitKenn == zk
  cat(sprintf("  %-4s %-5s Spieler mit Wert: %2d von %d\n", z, zk, sum(!is.na(agg$BEST[s])), sum(s)))
}

reg <- register_neu("S04_Aggregation_2026-09-25.R")
for (cd in codes) {
  for (z in ZIELE_SECHS) for (zk in ZEIT_KENN) {
    a <- agg[agg$Code == cd & agg$Ziel == z & agg$ZeitKenn == zk, ]
    setze(reg, paste0("S04.K.", z, ".", zk, ".P", cd, ".X"), a$K, "anzahl")
  }
  for (z in ZIELE_SIEBEN) for (zk in ZEIT_KENN) {
    a <- agg[agg$Code == cd & agg$Ziel == z & agg$ZeitKenn == zk, ]
    setze(reg, paste0("S04.BEST.", z, ".", zk, ".P", cd, ".X"), a$BEST, "zahl", a$Grund)
  }
  for (z in ZIELE_SIEBEN) for (zk in ZEIT_KENN) {
    a <- agg[agg$Code == cd & agg$Ziel == z & agg$ZeitKenn == zk, ]
    setze(reg, paste0("S04.MEAN.", z, ".", zk, ".P", cd, ".X"), a$MEAN, "zahl", a$Grund)
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S04", daten$spieler))

saveRDS(agg, pfad_zwischen("S04_aggregat.rds"))
write.csv(agg, pfad_zwischen("S04_aggregat.csv"), row.names = FALSE, fileEncoding = "UTF-8", na = "")
register_speichere(reg, "S04")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

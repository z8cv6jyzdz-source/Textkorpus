# =====================================================================
# S09_Versuchszahlen_2026-09-25.R
# Zweck: Mittlere Zahl gültiger Versuche k je Zielgröße, Zeitpunkt und Gruppe
#        über die Bezugsmenge (Spieler mit Zeilen zum Zeitpunkt, post ohne
#        Status nicht angetreten).
# Schritt der Spezifikation: S09 (Teil B), Regeln 3 und 4 entfallen (Nachtrag 2)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S02_versuche.rds, S04_aggregat.rds
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S09_Versuchszahlen_2026-09-25.R
# Ausgabe: S09_Versuchszahlen_2026-09-25.txt, Zwischen/S09_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
agg <- lies_zwischen("S04_aggregat.rds")
schreibe_kopf(
  zweck = "Mittlere Zahl gültiger Versuche je Gruppe",
  schritt = "S09",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
kenn <- lies_kennungen()
p <- daten$personen

reg <- register_neu("S09_Versuchszahlen_2026-09-25.R")
for (zk in ZEIT_KENN) {
  bezug <- unique(v$Code[v$ZeitKenn == zk])
  if (zk == "POST") bezug <- bezug[p$Status[match(bezug, p$Code)] != "nicht angetreten"]
  cat("\nBezugsmenge ", zk, ": ", length(bezug), " Spieler\n", sep = "")
  for (g in c("IG", "KG")) {
    s <- bezug[p$Gruppe[match(bezug, p$Code)] == g]
    for (z in ZIELE_SECHS) {
      k <- agg$K[agg$Ziel == z & agg$ZeitKenn == zk & agg$Code %in% s]
      pruefe(length(k) == length(s) && !anyNA(k), "k unvollständig für ", z, " ", zk, " ", g)
      setze(reg, paste0("S09.KMEAN.", z, ".", zk, ".", g, ".X"), mittel(k), "zahl", GRUND_ZU_WENIG)
    }
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S09", daten$spieler))
register_speichere(reg, "S09")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

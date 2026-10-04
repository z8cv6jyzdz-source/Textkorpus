# =====================================================================
# S03_Ausfallkategorien_2026-09-25.R
# Zweck: Jede ungültige Versuchszeile (gültig = 0) genau einer Ausfallkategorie
#        zuordnen: NANG, AUSL, sonst nach Bemerkung und Vokabular (K5).
# Schritt der Spezifikation: S03 (Teil A)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, Zwischen/S02_versuche.rds (aus S01 und S02)
#   Spezifikation_2026-09-24_Vokabular.csv
#     7afaa01d82dc9f5ca10534a09f916dca5475842caa32e71aad866ba43612860f
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S03_Ausfallkategorien_2026-09-25.R
# Ausgabe: S03_Ausfallkategorien_2026-09-25.txt, Zwischen/S03_versuche.rds,
#          Zwischen/S03_versuche.csv, Zwischen/S03_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
v <- lies_zwischen("S02_versuche.rds")
schreibe_kopf(
  zweck = "Ausfallkategorien der ungültigen Versuchszeilen",
  schritt = "S03",
  eingang = c(daten$pruefsummen, "Spezifikation_2026-09-24_Vokabular.csv" = unname(ANLAGEN["_Vokabular.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
kenn <- lies_kennungen()
vok <- daten$vokabular
pruefe_kategorie(vok$kategorie, "Vokabular kategorie", c("TECH", "ZEIT", "FEHL", "FALSCH"))
pruefe(!any(duplicated(vok$bemerkung_exakt)), "Vokabular: doppelte Bemerkungstexte")

status <- daten$personen$Status[match(v$Code, daten$personen$Code)]
gruppe <- daten$personen$Gruppe[match(v$Code, daten$personen$Code)]
v$Gruppe <- gruppe
v$Kategorie <- NA_character_

# Regel 1, Widerspruchsprüfung über alle Post-Zeilen nicht angetretener Spieler
nang_post <- v$ZeitKenn == "POST" & status == "nicht angetreten"
pruefe(all(is.na(v$Wert[nang_post])), "Widerspruch: Wert in Post-Zeile eines nicht angetretenen Spielers: ",
       paste(unique(v$Code[nang_post & !is.na(v$Wert)]), collapse = ", "))

ungueltig <- which(v$gueltig == 0)
for (i in ungueltig) {
  if (v$ZeitKenn[i] == "POST" && status[i] == "nicht angetreten") {
    pruefe(is.na(v$Wert[i]), "Widerspruch: Wert in Post-Zeile eines nicht angetretenen Spielers, Code ",
           v$Code[i], ", Test ", v$Test[i], ", Versuch ", v$Versuch[i])
    v$Kategorie[i] <- "NANG"
  } else if (v$gueltig_roh[i] == 1) {
    pruefe(isTRUE(v$auslgestoert[i]), "Zeile ungültig ohne erkennbaren Grund: Zeile ", i)
    v$Kategorie[i] <- "AUSL"
  } else {
    b <- v$Bemerkung[i]
    pruefe(b != "", "Ungültige Zeile ohne Bemerkung (K5): Code ", v$Code[i], ", ", v$Zeitpunkt[i], ", ",
           v$Test[i], ", Seite ", v$Seite[i], ", Versuch ", v$Versuch[i])
    pruefe(b %in% vok$bemerkung_exakt, "Bemerkungstext nicht in der Anlage (K5): ", b)
    v$Kategorie[i] <- vok$kategorie[vok$bemerkung_exakt == b]
  }
}
pruefe(all(!is.na(v$Kategorie[v$gueltig == 0])), "Ungültige Zeile ohne Kategorie")
pruefe(all(is.na(v$Kategorie[v$gueltig == 1])), "Gültige Zeile mit Kategorie")
cat("\nUngültige Zeilen: ", length(ungueltig), "\n", sep = "")
tab <- table(v$Kategorie[ungueltig])
for (k in names(tab)) cat("  ", k, ": ", tab[[k]], "\n", sep = "")

reg <- register_neu("S03_Ausfallkategorien_2026-09-25.R")
KAT_PRE <- c("TECH", "ZEIT", "FEHL", "FALSCH", "AUSL")
KAT_POST <- c("TECH", "ZEIT", "FEHL", "FALSCH", "NANG", "AUSL")
for (z in ZIELE_SECHS) for (zk in ZEIT_KENN) for (g in c("IG", "KG")) {
  kats <- if (zk == "PRE") KAT_PRE else KAT_POST
  for (k in kats) {
    n <- sum(v$gueltig == 0 & v$Ziel == z & v$ZeitKenn == zk & v$Gruppe == g & v$Kategorie == k, na.rm = TRUE)
    setze(reg, paste0("S03.NKAT.", z, ".", zk, ".", g, ".", k), n, "anzahl")
  }
}
# Prüfung: keine NANG-Zeile zum Zeitpunkt prä
pruefe(!any(v$Kategorie == "NANG" & v$ZeitKenn == "PRE", na.rm = TRUE), "Kategorie NANG zum Zeitpunkt prä")
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S03", daten$spieler))

saveRDS(v, pfad_zwischen("S03_versuche.rds"))
write.csv(v[, c("Code", "Gruppe", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert", "ungueltig", "Bemerkung",
                "gueltig_roh", "auslgestoert", "gueltig", "Kategorie")],
          pfad_zwischen("S03_versuche.csv"), row.names = FALSE, fileEncoding = "UTF-8", na = "")
register_speichere(reg, "S03")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

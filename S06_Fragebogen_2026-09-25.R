# =====================================================================
# S06_Fragebogen_2026-09-25.R
# Zweck: Fragebogen A dekodieren: Listenlabel aus H010, Fallkorrekturen der
#        CASE-Nummern, Analysecode aus der Zuordnungstabelle, Status aus H004,
#        CR-10 aus H005, Meldezeitpunkt (K6), Programmwoche nach Kalenderregel
#        (K8), Dubletten- und Sammelmeldungspaare (K7).
# Schritt der Spezifikation: S06 (Teil A), Regel 8 entfällt (Nachtrag 2)
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds (Fragebogen, Zuordnung, Listenplatz, Prüfsummen im Kopf von S01)
#   Spezifikation_2026-09-24_Fragebogen.csv
#     04318c066939248c5feca5077c65a703508a1137738310fdfa68b3a329003f04
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S06_Fragebogen_2026-09-25.R
# Ausgabe: S06_Fragebogen_2026-09-25.txt, Zwischen/S06_meldungen.rds,
#          Zwischen/S06_meldungen.csv, Zwischen/S06_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

daten <- lies_zwischen("S01_daten.rds")
schreibe_kopf(
  zweck = "Fragebogen A: Dekodierung, Fallkorrekturen, Zuordnung, Wochen, Dubletten",
  schritt = "S06",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Fragebogen.csv" = unname(ANLAGEN["_Fragebogen.csv"]),
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
cb <- lies_anlage("_Fragebogen.csv")
pruefe_spalten(cb, c("variable", "code", "bedeutung", "quelle"), "_Fragebogen.csv")

fb <- daten$fragebogen
zu <- daten$zuordnung
personen <- daten$personen

# Regel 1: Listenlabel aus H010 nach Codebuch
h010 <- cb[cb$variable == "H010", ]
h010$code <- als_ganzzahl(h010$code, "Codebuch H010 code")
pruefe(setequal(h010$code, 1:22) && !any(duplicated(h010$code)), "Codebuch H010: Codes nicht 1 bis 22")
label_soll <- c(sprintf("HL-%02d", 1:8), sprintf("BW-%02d", 1:14))
pruefe(identical(h010$bedeutung[order(h010$code)], label_soll),
       "Codebuch H010: Labels weichen von der Regel 1 bis 8 HL-01 bis HL-08 und 9 bis 22 BW-01 bis BW-14 ab")
fb$Listenlabel_roh <- h010$bedeutung[match(fb$H010, h010$code)]
pruefe(!anyNA(fb$Listenlabel_roh), "Listenlabel nicht zuordenbar")

# Regel 2: Fallkorrekturen nach Anlage (CASE_KORREKTUR)
kor <- cb[cb$variable == "CASE_KORREKTUR", ]
kor$case <- als_ganzzahl(kor$code, "CASE_KORREKTUR code")
kor$label <- sub("^Listenlabel ", "", kor$bedeutung)
pruefe(all(kor$label %in% label_soll), "CASE_KORREKTUR: Label nicht bekannt: ", paste(kor$label, collapse = ", "))
pruefe(!any(duplicated(kor$case)), "CASE_KORREKTUR: CASE doppelt")
fehlend <- kor$case[!(kor$case %in% fb$CASE)]
pruefe(length(fehlend) == 0, "CASE der Korrekturliste nicht im Export: ", paste(fehlend, collapse = ", "))
fb$Listenlabel <- fb$Listenlabel_roh
fb$korrigiert <- 0L
for (i in seq_len(nrow(kor))) {
  j <- which(fb$CASE == kor$case[i])
  fb$Listenlabel[j] <- kor$label[i]
  fb$korrigiert[j] <- 1L
}
cat("\nFallkorrekturen angewandt: ", sum(fb$korrigiert), " Meldungen (CASE ",
    paste(sort(kor$case), collapse = ", "), ")\n", sep = "")

# Regel 3: Analysecode
fb$Analysecode <- zu$Analysecode[match(fb$Listenlabel, zu$Listenlabel)]
pruefe(!anyNA(fb$Analysecode), "Listenlabel ohne Zeile in der Zuordnung")
ohne_code <- fb$Analysecode == ""
pruefe(!any(ohne_code), "Meldung an Listenlabel ohne Analysecode: CASE ",
       paste(fb$CASE[ohne_code], collapse = ", "), " Label ", paste(unique(fb$Listenlabel[ohne_code]), collapse = ", "))
gruppe <- personen$Gruppe[match(fb$Analysecode, personen$Code)]
pruefe(!anyNA(gruppe), "Analysecode nicht in den Personendaten")
pruefe(all(gruppe == "IG"), "Meldung mit Analysecode der KG: ", paste(fb$CASE[gruppe != "IG"], collapse = ", "))
ohne_platz <- daten$listenplatz$Code[daten$listenplatz$kein_Listenplatz == "ja"]
pruefe(!any(fb$Analysecode %in% ohne_platz), "Meldung eines Spielers ohne Listenplatz")

# Regel 4 und 5
fb$Status <- c("GANZ", "TEILW", "GARN")[fb$H004]
CR10_VERSATZ <- konstante_zahl(konst, "CR10_VERSATZ")
fb$CR10 <- fb$H005 - CR10_VERSATZ
pruefe(all(fb$CR10 >= 0 & fb$CR10 <= 10), "CR-10 außerhalb 0 bis 10")

# Regel 6 und 7: Meldezeitpunkt und Programmwoche
fb$Zeit <- as.POSIXct(fb$STARTED, format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
pruefe(!anyNA(fb$Zeit), "STARTED nicht lesbar")
fb$Meldedatum <- format(fb$Zeit, "%Y-%m-%d")
w1 <- as.POSIXct(konstante_text(konst, "W1_BEGINN"), format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
w6e <- as.POSIXct(konstante_text(konst, "W6_ENDE"), format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
pruefe(!is.na(w1) && !is.na(w6e), "Wochengrenzen der Konstanten nicht lesbar")
pruefe(as.numeric(difftime(w6e, w1, units = "secs")) == 6 * 7 * 86400 - 1,
       "W6_ENDE passt nicht zu W1_BEGINN plus sechs Wochen")
cat("Programmwochen: W1 ab ", format(w1, "%Y-%m-%d %H:%M:%S"), ", W6 bis ", format(w6e, "%Y-%m-%d %H:%M:%S"), "\n", sep = "")
sek <- as.numeric(difftime(fb$Zeit, w1, units = "secs"))
woche <- floor(sek / (7 * 86400)) + 1
ausserhalb <- sek < 0 | fb$Zeit > w6e | woche < 1 | woche > 6
pruefe(!any(ausserhalb), "Meldung außerhalb von W1 bis W6 (K8): CASE ", paste(fb$CASE[ausserhalb], collapse = ", "))
fb$Woche <- paste0("W", woche)

# Regel 9: Dubletten- und Sammelmeldungspaare (jedes Paar gezählt)
ABSTAND <- konstante_zahl(konst, "DUBLETTE_ABSTAND") * 60
inhalt <- paste(fb$H003, fb$H004, fb$H005, fb$H006, fb$H007, fb$H008, fb$H009)
n <- nrow(fb)
pz <- paare_zaehlen(fb$Analysecode, fb$Zeit, inhalt, ABSTAND)
fb$dublette <- pz$dublette
fb$sammel <- pz$sammel
n_dubl <- pz$n_dubl
n_samm <- pz$n_samm
paare <- pz$paare
cat("Meldungen: ", n, ", Dublettenpaare: ", n_dubl, ", Sammelmeldungspaare: ", n_samm, "\n", sep = "")
if (nrow(paare) > 0) for (i in seq_len(nrow(paare))) {
  cat(sprintf("  Paar CASE %d und %d: %s, Abstand %.0f s\n", fb$CASE[paare$i[i]], fb$CASE[paare$j[i]], paare$Art[i], paare$Abstand_s[i]))
}

# Ausgabe
reg <- register_neu("S06_Fragebogen_2026-09-25.R")
setze(reg, "S06.NMELD.FB.X.ALL.X", n, "anzahl")
for (cd in daten$spieler$IG) {
  setze(reg, paste0("S06.NMELD.FB.X.P", cd, ".X"), sum(fb$Analysecode == cd), "anzahl")
}
setze(reg, "S06.NKORR.FB.X.ALL.X", sum(fb$korrigiert), "anzahl")
setze(reg, "S06.NDUBL.FB.X.ALL.X", n_dubl, "anzahl")
setze(reg, "S06.NSAMM.FB.X.ALL.X", n_samm, "anzahl")
for (st in c("GANZ", "TEILW", "GARN")) {
  setze(reg, paste0("S06.NSTAT.FB.X.IG.", st), sum(fb$Status == st), "anzahl")
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S06", daten$spieler))

saveRDS(fb, pfad_zwischen("S06_meldungen.rds"))
write.csv(fb[, c("CASE", "STARTED", "H010", "Listenlabel_roh", "Listenlabel", "korrigiert", "Analysecode",
                 "Status", "CR10", "Woche", "H003", "H006", "H007", "H008", "H009", "dublette", "sammel")],
          pfad_zwischen("S06_meldungen.csv"), row.names = FALSE, fileEncoding = "UTF-8")
register_speichere(reg, "S06")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

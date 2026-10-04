# =====================================================================
# S01_Einlesen_2026-09-25.R
# Zweck: Eingang prüfen, bevor gerechnet wird: SHA-256 der Datenstand-Dateien
#        gegen Pruefsummen.txt, Struktur und Wertebereiche nach Spezifikation
#        S01 und Datenwörterbuch, Umwandlung in typisierte Tabellen.
# Schritt der Spezifikation: S01 (Teil A), Eingang 0.4
# Eingangsdateien (SHA-256, Soll laut Pruefsummen.txt des Datenstands):
#   Datenstand_2026-09-24/Versuchsdaten.csv
#     429b0f045fb22d2f78905b8ced97ed5f4bf91685cabe15578a6490ba642946ba
#   Datenstand_2026-09-24/Personendaten.csv
#     acf1f52b915734cec540c93229d648547b490263d4709be041047e20d8c28aef
#   Datenstand_2026-09-24/Fragebogen_A.csv
#     5c2a32084b3470453ad001615498f272ac59effd32601012643908ce92af57a4
#   Datenstand_2026-09-24/Zuordnung_Fragebogen.csv
#     f98eee51d9ad1b3de62ffab89cb2df7e75a2554ca0be85349eba0b0605c653fa
#   Datenstand_2026-09-24/Listenplatz_IG.csv
#     2c999317806e4f01e180fa968c5a44bda0e731acd3425636496193feecedcca8
#   Datenstand_2026-09-24/Datenwoerterbuch.md
#     07394867ffcdf9697618ccd295ccce6ac70a2e3aceff1329ab16052125b08fb6
#   Datenstand_2026-09-24/Pruefsummen.txt (Sollliste, selbst ohne Soll)
#   Spezifikation_2026-09-24_Vokabular.csv
#     7afaa01d82dc9f5ca10534a09f916dca5475842caa32e71aad866ba43612860f
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S01_Einlesen_2026-09-25.R
# Ausgabe: S01_Einlesen_2026-09-25.txt, Zwischen/S01_daten.rds, Zwischen/S01_ergebnisse.rds
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

DATEIEN_DATENSTAND <- c("Versuchsdaten.csv", "Personendaten.csv", "Fragebogen_A.csv",
                        "Zuordnung_Fragebogen.csv", "Listenplatz_IG.csv", "Datenwoerterbuch.md")

# ---------------------------------------------------------------------
# Regel 1: Prüfsummen gegen die Liste des Datenstands
# ---------------------------------------------------------------------
pfad_liste <- pfad_datenstand("Pruefsummen.txt")
pruefe(file.exists(pfad_liste), "Pruefsummen.txt fehlt im Datenstand")
zeilen <- readLines(pfad_liste, encoding = "UTF-8", warn = FALSE)
zeilen <- zeilen[nchar(trimws(zeilen)) > 0]
soll <- character(0)
for (z in zeilen) {
  teile <- regmatches(z, regexec("^([0-9a-f]{64})\\s+[*]?(.+)$", z))[[1]]
  pruefe(length(teile) == 3, "Pruefsummen.txt: Zeile ohne Form 'Prüfsumme  Dateiname': ", z)
  soll[trimws(teile[3])] <- teile[2]
}
pruefe(setequal(names(soll), DATEIEN_DATENSTAND),
       "Pruefsummen.txt nennt andere Dateien als erwartet: ", paste(names(soll), collapse = ", "))
vorhanden <- list.files(ORDNER_DATENSTAND)
pruefe(setequal(vorhanden, c(DATEIEN_DATENSTAND, "Pruefsummen.txt")),
       "Datenstand enthält andere Dateien als erwartet: ", paste(vorhanden, collapse = ", "))

ist <- character(0)
for (f in DATEIEN_DATENSTAND) ist[f] <- sha256_datei(pfad_datenstand(f))
ist["Pruefsummen.txt"] <- sha256_datei(pfad_liste)

schreibe_kopf(
  zweck = "Einlesen, Prüfsummen und Strukturprüfung des Datenstands",
  schritt = "S01",
  eingang = c(ist, "Spezifikation_2026-09-24_Vokabular.csv" = unname(ANLAGEN["_Vokabular.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)

cat("\nRegel 1: SHA-256 gegen Pruefsummen.txt\n")
for (f in DATEIEN_DATENSTAND) {
  ok <- identical(ist[[f]], soll[[f]])
  cat(sprintf("  %-28s Soll %s\n  %-28s Ist  %s  %s\n", f, soll[[f]], "", ist[[f]],
              if (ok) "stimmt" else "ABWEICHUNG"))
  pruefe(ok, "Prüfsumme weicht ab: ", f)
}
cat("Alle Prüfsummen des Datenstands stimmen.\n")

# ---------------------------------------------------------------------
# Einlesen als Text
# ---------------------------------------------------------------------
versuche <- lies_csv(pfad_datenstand("Versuchsdaten.csv"))
personen <- lies_csv(pfad_datenstand("Personendaten.csv"))
fragebogen <- lies_csv(pfad_datenstand("Fragebogen_A.csv"))
zuordnung <- lies_csv(pfad_datenstand("Zuordnung_Fragebogen.csv"))
listenplatz <- lies_csv(pfad_datenstand("Listenplatz_IG.csv"))
vokabular <- lies_anlage("_Vokabular.csv")
pruefe_spalten(vokabular, c("bemerkung_exakt", "kategorie", "bedeutung", "quelle"), "_Vokabular.csv")
kenn <- lies_kennungen()

pruefe_spalten(versuche, c("Code", "Zeitpunkt", "Test", "Seite", "Versuch", "Wert", "ungültig", "Bemerkung"),
               "Versuchsdaten.csv")
pruefe_spalten(personen, c("Code", "Verein", "Gruppe", "Alter_prae", "Koerperhoehe_prae", "Koerpermasse_prae",
                           "Groesse_Mutter", "Groesse_Vater", "Familiarisierung", "Status"), "Personendaten.csv")
pruefe_spalten(fragebogen, c("CASE", "STARTED", "H010", "H002", "H003", "H004", "H005", "H006", "H007",
                             "H008", "H009"), "Fragebogen_A.csv")
pruefe_spalten(zuordnung, c("Listenlabel", "Analysecode"), "Zuordnung_Fragebogen.csv")
pruefe_spalten(listenplatz, c("Code", "kein_Listenplatz"), "Listenplatz_IG.csv")

# ---------------------------------------------------------------------
# Regel 3: Personendaten
# ---------------------------------------------------------------------
cat("\nRegel 3: Personendaten\n")
pruefe(nrow(personen) > 0, "Personendaten leer")
pruefe(!any(duplicated(personen$Code)), "Personendaten: Code nicht eindeutig")
pruefe(all(grepl("^[A-Z]{2}-[0-9]{2}$", personen$Code)), "Personendaten: Code nicht nach Muster XX-nn")
pruefe_kategorie(personen$Verein, "Verein", c("A", "B", "C"))
pruefe_kategorie(personen$Gruppe, "Gruppe", c("IG", "KG"))
gruppe_soll <- ifelse(personen$Verein %in% c("A", "B"), "IG", "KG")
pruefe(all(personen$Gruppe == gruppe_soll), "Personendaten: Gruppe passt nicht zu Verein (IG genau dann, wenn A oder B)")
personen$Alter_prae <- als_zahl(personen$Alter_prae, "Alter_prae", leer_erlaubt = FALSE)
pruefe(all(personen$Alter_prae > 0), "Alter_prae nicht größer 0")
for (sp in c("Koerperhoehe_prae", "Koerpermasse_prae", "Groesse_Mutter", "Groesse_Vater")) {
  personen[[sp]] <- als_zahl(personen[[sp]], sp, leer_erlaubt = TRUE)
  pruefe(all(is.na(personen[[sp]]) | personen[[sp]] > 0), sp, " nicht größer 0")
}
personen$Familiarisierung <- als_ganzzahl(personen$Familiarisierung, "Familiarisierung", zulaessig = c(1L, 2L),
                                          leer_erlaubt = TRUE)
pruefe_kategorie(personen$Status, "Status", c("ausgewertet", "nicht angetreten"))
cat("  Personendaten geprüft: ", nrow(personen), " Zeilen\n", sep = "")

# ---------------------------------------------------------------------
# Regel 2: Versuchsdaten
# ---------------------------------------------------------------------
cat("\nRegel 2: Versuchsdaten\n")
pruefe(nrow(versuche) > 0, "Versuchsdaten leer")
pruefe_kategorie(versuche$Zeitpunkt, "Zeitpunkt", c(ZEITPUNKT_PRAE, ZEITPUNKT_POST))
pruefe_kategorie(versuche$Test, "Test", TESTS)
ist_505 <- versuche$Test == "COD_505"
pruefe(all(versuche$Seite[ist_505] %in% c("L", "R")), "Seite beim COD_505 nicht L oder R")
pruefe(all(versuche$Seite[!ist_505] == SEITE_LEER), "Seite außerhalb COD_505 nicht der Halbgeviertstrich")
versuche$Versuch <- als_ganzzahl(versuche$Versuch, "Versuch", zulaessig = 1:3)
schluessel <- paste(versuche$Code, versuche$Zeitpunkt, versuche$Test, versuche$Seite, versuche$Versuch)
pruefe(!any(duplicated(schluessel)), "Versuchsdaten: Schlüssel (Code, Zeitpunkt, Test, Seite, Versuch) nicht eindeutig")
versuche$Wert <- als_zahl(versuche$Wert, "Wert", leer_erlaubt = TRUE)
pruefe(all(is.na(versuche$Wert) | versuche$Wert > 0), "Wert nicht größer 0")
pruefe(all(versuche$Code %in% personen$Code), "Versuchsdaten: Code nicht in den Personendaten: ",
       paste(unique(versuche$Code[!(versuche$Code %in% personen$Code)]), collapse = ", "))
pruefe_kategorie(versuche[["ungültig"]], "ungültig", c("", "x"))
pruefe_kategorie(versuche$Bemerkung, "Bemerkung", c("", vokabular$bemerkung_exakt))
names(versuche)[names(versuche) == "ungültig"] <- "ungueltig"
versuche$Ziel <- ZIEL_VON_TEST_SEITE(versuche$Test, versuche$Seite)
pruefe(!anyNA(versuche$Ziel), "Zielgröße nicht zuordenbar")
versuche$ZeitKenn <- zeit_kennung(versuche$Zeitpunkt)
cat("  Versuchsdaten geprüft: ", nrow(versuche), " Zeilen\n", sep = "")

# ---------------------------------------------------------------------
# Regel 4: Fragebogen
# ---------------------------------------------------------------------
cat("\nRegel 4: Fragebogen\n")
pruefe(nrow(fragebogen) > 0, "Fragebogen leer")
fragebogen$CASE <- als_ganzzahl(fragebogen$CASE, "CASE")
pruefe(!any(duplicated(fragebogen$CASE)), "Fragebogen: CASE nicht eindeutig")
pruefe(all(grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$", fragebogen$STARTED)),
       "STARTED nicht im Format JJJJ-MM-TT hh:mm:ss")
zeit <- as.POSIXct(fragebogen$STARTED, format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
pruefe(!anyNA(zeit), "STARTED nicht als Zeitpunkt lesbar")
fragebogen$H010 <- als_ganzzahl(fragebogen$H010, "H010", zulaessig = 1:22)
fragebogen$H002 <- als_ganzzahl(fragebogen$H002, "H002", zulaessig = 1L)
fragebogen$H003 <- als_ganzzahl(fragebogen$H003, "H003", zulaessig = 1:12)
fragebogen$H004 <- als_ganzzahl(fragebogen$H004, "H004", zulaessig = 1:3)
fragebogen$H005 <- als_ganzzahl(fragebogen$H005, "H005", zulaessig = 1:11)
fragebogen$H006 <- als_ganzzahl(fragebogen$H006, "H006", zulaessig = 1:5)
fragebogen$H007 <- als_ganzzahl(fragebogen$H007, "H007", zulaessig = 1:2)
fragebogen$H008 <- als_ganzzahl(fragebogen$H008, "H008", zulaessig = 1:2)
fragebogen$H009 <- als_ganzzahl(fragebogen$H009, "H009", zulaessig = 1:2)
cat("  Fragebogen geprüft: ", nrow(fragebogen), " Zeilen\n", sep = "")

# ---------------------------------------------------------------------
# Zuordnungstabelle und Listenplatz (Datenwörterbuch, Anmerkung A9)
# ---------------------------------------------------------------------
cat("\nZuordnungstabelle und Listenplatz\n")
labels_soll <- c(sprintf("HL-%02d", 1:8), sprintf("BW-%02d", 1:14))
pruefe(setequal(zuordnung$Listenlabel, labels_soll) && !any(duplicated(zuordnung$Listenlabel)) &&
         nrow(zuordnung) == 22, "Zuordnung: Listenlabels nicht genau HL-01 bis HL-08 und BW-01 bis BW-14")
zc <- zuordnung$Analysecode
pruefe(all(zc == "" | zc %in% personen$Code), "Zuordnung: Analysecode nicht in den Personendaten: ",
       paste(unique(zc[!(zc == "" | zc %in% personen$Code)]), collapse = ", "))
pruefe(!any(duplicated(zc[zc != ""])), "Zuordnung: Analysecode mehrfach vergeben")
ig_codes <- personen$Code[personen$Gruppe == "IG"]
pruefe(setequal(listenplatz$Code, ig_codes) && !any(duplicated(listenplatz$Code)),
       "Listenplatz_IG: Codes sind nicht genau die IG-Codes der Personendaten")
pruefe_kategorie(listenplatz$kein_Listenplatz, "kein_Listenplatz", c("ja", "nein"))
ohne <- listenplatz$Code[listenplatz$kein_Listenplatz == "ja"]
pruefe(!any(ohne %in% zc), "Spieler mit kein_Listenplatz = ja ist einem Listenlabel zugeordnet: ",
       paste(ohne[ohne %in% zc], collapse = ", "))
mit <- listenplatz$Code[listenplatz$kein_Listenplatz == "nein"]
pruefe(all(mit %in% zc), "IG-Spieler mit Listenplatz ohne Listenlabel in der Zuordnung: ",
       paste(mit[!(mit %in% zc)], collapse = ", "))
cat("  Zuordnung geprüft: ", nrow(zuordnung), " Listenlabels, ", sum(zc != ""), " mit Analysecode\n", sep = "")
cat("  Listenplatz_IG geprüft: ", nrow(listenplatz), " IG-Spieler, davon ohne Listenplatz: ", length(ohne), "\n", sep = "")

# ---------------------------------------------------------------------
# Ausgabe
# ---------------------------------------------------------------------
reg <- register_neu("S01_Einlesen_2026-09-25.R")
setze(reg, "S01.N.X.X.ALL.X", nrow(personen), "anzahl")
setze(reg, "S01.N.X.X.IG.X", sum(personen$Gruppe == "IG"), "anzahl")
setze(reg, "S01.N.X.X.KG.X", sum(personen$Gruppe == "KG"), "anzahl")
setze(reg, "S01.N.X.X.VA.X", sum(personen$Verein == "A"), "anzahl")
setze(reg, "S01.N.X.X.VB.X", sum(personen$Verein == "B"), "anzahl")
setze(reg, "S01.N.X.X.VC.X", sum(personen$Verein == "C"), "anzahl")
setze(reg, "S01.NZEIL.X.X.ALL.X", nrow(versuche), "anzahl")
setze(reg, "S01.NMELD.FB.X.ALL.X", nrow(fragebogen), "anzahl")

spieler <- list(ALLE = personen$Code, IG = ig_codes, AK9 = list())
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S01", spieler))

daten <- list(versuche = versuche, personen = personen, fragebogen = fragebogen, zuordnung = zuordnung,
              listenplatz = listenplatz, vokabular = vokabular, pruefsummen = ist, spieler = spieler)
saveRDS(daten, pfad_zwischen("S01_daten.rds"))
register_speichere(reg, "S01")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

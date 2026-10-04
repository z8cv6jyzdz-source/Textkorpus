# =====================================================================
# Gesamtlauf_2026-09-25.R
# Zweck: Steuerskript der Blindrechnung in R. Ein Befehl startet die Kette:
#        Validierung (Referenztests, Grenzfälle), danach S01 bis S19 in fester
#        Reihenfolge, je Schritt ein eigener R-Prozess mit Ausgabe in eine
#        .txt-Datei gleichen Namensstamms. Danach Zusammenführung der
#        Ergebnisdatei nach G.1, Laufprotokoll, Umgebungsdatei und
#        Validierungsprotokoll.
# Schritt der Spezifikation: alle, Teil G.1 (Ergebnisdatei), Auswertungsverfahren
#        Phasen 3 bis 5
# Eingangsdateien (SHA-256): Datenstand_2026-09-24 (Sollliste Pruefsummen.txt, geprüft in S01),
#        Anlagen der Spezifikation (Sollprüfsummen in Funktionen_2026-09-25.R, ANLAGEN),
#        alle Skripte dieses Ordners (Prüfsummen im Laufprotokoll).
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript Gesamtlauf_2026-09-25.R
# Ausgabe: Ergebnisse_R_2026-09-25.csv, Laufprotokoll_2026-09-25.txt, Umgebung_2026-09-25.txt,
#          Validierungsprotokoll_2026-09-25.txt, je Skript <Namensstamm>.txt
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

START <- Sys.time()
AUFRUF <- "Rscript Gesamtlauf_2026-09-25.R"
RSCRIPT <- file.path(R.home("bin"), "Rscript")
protokoll <- character(0)
p_zeile <- function(...) {
  z <- paste0(...)
  protokoll <<- c(protokoll, z)
  cat(z, "\n", sep = "")
}

p_zeile("LAUFPROTOKOLL der Blindrechnung in R")
p_zeile("Datum und Uhrzeit des Starts: ", format(START, "%Y-%m-%d %H:%M:%S UTC"))
p_zeile("Aufrufbefehl: ", AUFRUF, " (Arbeitsverzeichnis ", ORDNER_ABGABE, ")")
p_zeile("Rechenumgebung: ", R.version.string, ", Plattform ", R.version$platform, ", Basis-R ohne Zusatzpakete")
p_zeile("Spezifikation: Spezifikation_2026-09-24 mit Nachtrag 1 und Nachtrag 2, Anlagen mit Sollprüfsummen in Funktionen_2026-09-25.R")
p_zeile("")

# ---------------------------------------------------------------------
# Skriptfassungen und Prüfsummen
# ---------------------------------------------------------------------
SCHRITTE <- c("S01_Einlesen", "S02_Gueltigkeit", "S03_Ausfallkategorien", "S04_Aggregation", "S05_Reifestatus",
              "S06_Fragebogen", "S07_Adhaerenz", "S08_Analysesets", "S09_Versuchszahlen", "S10_Messguete",
              "S11_Bestwertbias", "S12_Deskription", "S13_Hauptanalyse", "S14_Voraussetzungen",
              "S15_Effektstaerke", "S16_PerProtokoll", "S17_Sensitivitaet", "S18_Poweranalyse", "S19_Bootstrap")
VALIDIERUNG <- c("Referenztests", "Grenzfaelle")
skripte <- c("Funktionen", "Gesamtlauf", VALIDIERUNG, SCHRITTE)
p_zeile("Skriptfassungen (Datei, Fassung im Kopf, SHA-256):")
for (s in skripte) {
  f <- paste0(s, "_", FASSUNG, ".R")
  pruefe(file.exists(pfad_abgabe(f)), "Skript fehlt: ", f)
  kopf <- readLines(pfad_abgabe(f), n = 40, encoding = "UTF-8", warn = FALSE)
  fz <- grep("^# Fassung:", kopf, value = TRUE)
  p_zeile("  ", f, "  ", if (length(fz) == 1) trimws(sub("^# Fassung:", "", fz)) else "ohne Fassung", "  ", sha256_datei(pfad_abgabe(f)))
}
p_zeile("")
p_zeile("Prüfsummen des Eingangs (SHA-256):")
for (f in c("Versuchsdaten.csv", "Personendaten.csv", "Fragebogen_A.csv", "Zuordnung_Fragebogen.csv",
            "Listenplatz_IG.csv", "Datenwoerterbuch.md", "Pruefsummen.txt")) {
  p_zeile("  Datenstand_2026-09-24/", f, "  ", sha256_datei(pfad_datenstand(f)))
}
for (a in names(ANLAGEN)) {
  ist <- sha256_datei(pfad_anlage(a))
  p_zeile("  Spezifikation_2026-09-24", a, "  ", ist, if (identical(ist, unname(ANLAGEN[a]))) "  (Soll stimmt)" else "  (ABWEICHUNG vom Soll)")
  pruefe(identical(ist, unname(ANLAGEN[a])), "Anlage weicht von der Sollprüfsumme ab: ", a)
}
for (f in c("Spezifikation_2026-09-24.md", "Spezifikation_2026-09-24.pdf", "Spezifikation_2026-09-24_Zahlenliste.csv",
            "Auswertungsverfahren_2026-09-24.pdf")) {
  pf <- file.path(ORDNER_EINGANG, f)
  if (file.exists(pf)) p_zeile("  ", f, "  ", sha256_datei(pf), "  (nur dokumentiert, nicht gelesen)")
}
p_zeile("")

# ---------------------------------------------------------------------
# Ein Skript in eigenem Prozess ausführen, Ausgabe in .txt
# ---------------------------------------------------------------------
fuehre_aus <- function(stamm) {
  skript <- paste0(stamm, "_", FASSUNG, ".R")
  ausgabe <- pfad_abgabe(paste0(stamm, "_", FASSUNG, ".txt"))
  t0 <- Sys.time()
  status <- system2(RSCRIPT, shQuote(pfad_abgabe(skript)), stdout = ausgabe, stderr = ausgabe,
                    env = c("LC_ALL=C.UTF-8", "LANG=C.UTF-8", "TZ=UTC"))
  dauer <- round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1)
  zeilen <- readLines(ausgabe, encoding = "UTF-8", warn = FALSE)
  warn <- grep("^WARNUNG:", zeilen, value = TRUE)
  abbr <- grep("^ABBRUCH:", zeilen, value = TRUE)
  p_zeile(sprintf("  %-40s Status %d  Dauer %6.1f s  Warnungen %d  Ausgabe %s", skript, status, dauer, length(warn),
                  basename(ausgabe)))
  list(status = status, warnungen = warn, abbrueche = abbr, skript = skript)
}

# ---------------------------------------------------------------------
# Phase 4: Validierung vor den Studiendaten
# ---------------------------------------------------------------------
p_zeile("Phase 4, Validierung (Referenztests und Grenzfälle):")
alle_warnungen <- list()
for (s in VALIDIERUNG) {
  e <- fuehre_aus(s)
  alle_warnungen[[e$skript]] <- e$warnungen
  if (e$status != 0) {
    p_zeile("  ABBRUCH der Kette: ", e$skript, " nicht bestanden. ", paste(e$abbrueche, collapse = " | "))
    writeLines(protokoll, pfad_abgabe(paste0("Laufprotokoll_", FASSUNG, ".txt")), useBytes = TRUE)
    abbruch("Validierung nicht bestanden: ", e$skript)
  }
}
p_zeile("Validierung bestanden. Studiendaten werden gerechnet.")
p_zeile("")

# ---------------------------------------------------------------------
# Phase 5: Gesamtlauf S01 bis S19
# ---------------------------------------------------------------------
p_zeile("Phase 5, Gesamtlauf S01 bis S19:")
for (s in SCHRITTE) {
  e <- fuehre_aus(s)
  alle_warnungen[[e$skript]] <- e$warnungen
  if (e$status != 0) {
    p_zeile("  ABBRUCH der Kette bei ", e$skript, ". ", paste(e$abbrueche, collapse = " | "))
    writeLines(protokoll, pfad_abgabe(paste0("Laufprotokoll_", FASSUNG, ".txt")), useBytes = TRUE)
    abbruch("Schritt nicht durchgelaufen: ", e$skript)
  }
}
p_zeile("")

# ---------------------------------------------------------------------
# Ergebnisdatei nach G.1
# ---------------------------------------------------------------------
p_zeile("Ergebnisdatei nach G.1:")
kenn <- lies_kennungen()
daten <- lies_zwischen("S01_daten.rds")
sets <- lies_zwischen("S08_sets.rds")
spieler <- daten$spieler
spieler$AK9 <- sets$ak9
erwartet <- do.call(rbind, lapply(paste0("S", sprintf("%02d", 1:19)), function(s) erwartete_kennungen(kenn, s, spieler)))
pruefe(!any(duplicated(erwartet$Kennung)), "Sollliste der Kennungen enthält Duplikate")
ergebnisse <- do.call(rbind, lapply(paste0("S", sprintf("%02d", 1:19)), function(s) lies_zwischen(paste0(s, "_ergebnisse.rds"))))
pruefe(!any(duplicated(ergebnisse$Kennung)), "Ergebnisse enthalten doppelte Kennungen")
fehlt <- setdiff(erwartet$Kennung, ergebnisse$Kennung)
zuviel <- setdiff(ergebnisse$Kennung, erwartet$Kennung)
pruefe(length(fehlt) == 0, "Kennungen ohne Ergebnis: ", paste(head(fehlt, 20), collapse = ", "))
pruefe(length(zuviel) == 0, "Ergebnisse ohne Kennung in der Anlage: ", paste(head(zuviel, 20), collapse = ", "))
ergebnisse <- ergebnisse[match(erwartet$Kennung, ergebnisse$Kennung), ]
ergebnisse$Einheit <- erwartet$Einheit
leer <- ergebnisse$Wert == ""
pruefe(all(ergebnisse$Grund[leer] %in% GRUENDE_ZULAESSIG), "Fehlender Wert ohne zulässigen Grund in der Ergebnisdatei")
pruefe(all(ergebnisse$Grund[!leer] == ""), "Wert mit Grund in der Ergebnisdatei")
pruefe(all(grepl("^S[0-9]{2}(\\.[A-Z0-9<>-]+){5}$", ergebnisse$Kennung)), "Kennung außerhalb des Zeichenvorrats")
csv_feld <- function(x) {
  x <- enc2utf8(as.character(x))
  braucht <- grepl("[,\"]", x)
  x[braucht] <- paste0("\"", gsub("\"", "\"\"", x[braucht]), "\"")
  x
}
zeilen <- c("Kennung,Wert,Einheit,Grund,Skript",
            paste(csv_feld(ergebnisse$Kennung), csv_feld(ergebnisse$Wert), csv_feld(ergebnisse$Einheit),
                  csv_feld(ergebnisse$Grund), csv_feld(ergebnisse$Skript), sep = ","))
pfad_erg <- pfad_abgabe(paste0("Ergebnisse_R_", FASSUNG, ".csv"))
con <- file(pfad_erg, open = "wb")
writeLines(zeilen, con, sep = "\n", useBytes = TRUE)
close(con)
p_zeile("  Kennungen der Anlage (Muster): ", nrow(kenn), ", ausgeschrieben: ", nrow(erwartet),
        ", davon Spielerkennungen: ", nrow(erwartet) - sum(kenn$spielermenge == ""))
p_zeile("  Zeilen der Ergebnisdatei: ", nrow(ergebnisse), ", mit Wert: ", sum(!leer), ", fehlend mit Grund: ", sum(leer))
tab <- table(ergebnisse$Grund[leer])
for (g in names(tab)) p_zeile("    Grund ", g, ": ", tab[[g]])
p_zeile("  Datei: ", basename(pfad_erg), "  SHA-256 ", sha256_datei(pfad_erg))
p_zeile("")

# ---------------------------------------------------------------------
# Warnungen mit Erklärung
# ---------------------------------------------------------------------
p_zeile("Warnungen der Skripte (jede mit Erklärung):")
n_warn <- sum(vapply(alle_warnungen, length, 1L))
if (n_warn == 0) {
  p_zeile("  keine Warnungen")
} else {
  for (s in names(alle_warnungen)) for (w in alle_warnungen[[s]]) {
    p_zeile("  ", s, ": ", w)
    p_zeile("    Erklärung: siehe Abschnitt Warnungen im Rückfragenprotokoll, die Warnung ist dort bewertet.")
  }
}
p_zeile("")

# ---------------------------------------------------------------------
# Validierungsprotokoll aus den Ausgaben der Validierungsskripte
# ---------------------------------------------------------------------
vp <- c("VALIDIERUNGSPROTOKOLL der Blindrechnung in R (Phase 4)",
        paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC")),
        "Teil a: Referenztests R01 bis R13 (Spezifikation Teil G.2) mit den Anlagen _Referenzdaten.csv und _Referenzdaten_Daten.csv.",
        "Teil b: Grenzfälle mit konstruierten Kleindatensätzen, Sollwerte von Hand ausgeschrieben im Skript Grenzfaelle_2026-09-25.R.",
        "Beide Teile rechnen mit denselben Funktionen (Funktionen_2026-09-25.R) wie die Schritte S01 bis S19.",
        "Urteil je Zeile: bestanden 1, nicht bestanden 0. Die Kette läuft nur weiter, wenn alle Zeilen bestanden sind.",
        "")
for (s in VALIDIERUNG) {
  vp <- c(vp, paste0("===== Teil ", if (s == "Referenztests") "a" else "b", ": ", s, " (Ausgabe von ", s, "_", FASSUNG, ".R) ====="),
          readLines(pfad_abgabe(paste0(s, "_", FASSUNG, ".txt")), encoding = "UTF-8", warn = FALSE), "")
}
rt <- read.csv(pfad_zwischen("Referenztests_ergebnis.csv"), colClasses = "character", encoding = "UTF-8")
gf <- read.csv(pfad_zwischen("Grenzfaelle_ergebnis.csv"), colClasses = "character", encoding = "UTF-8")
vp <- c(vp, "===== Zusammenfassung =====",
        paste0("Referenztests: ", nrow(rt), " Sollwerte, bestanden ", sum(rt$bestanden == "1"), ", nicht bestanden ", sum(rt$bestanden != "1")),
        paste0("Grenzfälle: ", nrow(gf), " Fälle, bestanden ", sum(gf$bestanden == "1"), ", nicht bestanden ", sum(gf$bestanden != "1")),
        if (all(rt$bestanden == "1") && all(gf$bestanden == "1")) "Urteil: Validierung bestanden, Studiendaten wurden gerechnet." else "Urteil: Validierung NICHT bestanden.")
writeLines(vp, pfad_abgabe(paste0("Validierungsprotokoll_", FASSUNG, ".txt")), useBytes = TRUE)
p_zeile("Validierungsprotokoll geschrieben: Validierungsprotokoll_", FASSUNG, ".txt")

# ---------------------------------------------------------------------
# Umgebungsdatei
# ---------------------------------------------------------------------
si <- capture.output(print(sessionInfo()))
pakete <- system2("dpkg-query", c("-W", "-f", shQuote("${Package} ${Version}\\n"), "r-base-core", "libblas3", "liblapack3", "libc6"), stdout = TRUE, stderr = TRUE)
um <- c("UMGEBUNG der Blindrechnung in R",
        paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC")),
        "",
        "Betriebssystem: Ubuntu 24.04 LTS (Container, x86_64), Paketquellen des Systems (apt, noble/universe)",
        "Installationsbefehle (am 2026-09-25 ausgeführt):",
        "  apt-get update",
        "  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends r-base-core",
        "Zusatzpakete: keine (nur Basis-R: base, stats, utils, graphics, grDevices)",
        "Aufruf der Kette: Rscript Gesamtlauf_2026-09-25.R im Ordner Abgabe_R_2026-09-25 mit LC_ALL=C.UTF-8 und TZ=UTC",
        "Grafiken: png() über Cairo",
        "Zufallszahlen: RNGkind Mersenne-Twister, Inversion, Rejection, set.seed(20260924) je Zielgröße in S19",
        "",
        "Installierte Systempakete (dpkg-query):",
        paste0("  ", pakete),
        "",
        paste0("R.version.string: ", R.version.string),
        "",
        "sessionInfo():",
        si,
        "",
        "Rscript: ", RSCRIPT,
        paste0("Rscript --version: ", paste(system2(RSCRIPT, "--version", stdout = TRUE, stderr = TRUE), collapse = " ")))
writeLines(um, pfad_abgabe(paste0("Umgebung_", FASSUNG, ".txt")), useBytes = TRUE)
p_zeile("Umgebungsdatei geschrieben: Umgebung_", FASSUNG, ".txt")
p_zeile("")

# ---------------------------------------------------------------------
# Prüfsummen der Ausgaben
# ---------------------------------------------------------------------
p_zeile("Prüfsummen der Ausgaben (SHA-256):")
ausgaben <- c(paste0("Ergebnisse_R_", FASSUNG, ".csv"), paste0("Validierungsprotokoll_", FASSUNG, ".txt"),
              paste0("Umgebung_", FASSUNG, ".txt"), paste0(c(VALIDIERUNG, SCHRITTE), "_", FASSUNG, ".txt"),
              paste0("S14_QQ_", ZIELE_KONF, ".png"), paste0("S14_Linearitaet_", ZIELE_KONF, ".png"))
for (f in ausgaben) {
  if (file.exists(pfad_abgabe(f))) p_zeile("  ", f, "  ", sha256_datei(pfad_abgabe(f)))
  else p_zeile("  ", f, "  fehlt (bei INF = 0 werden keine Grafiken erzeugt)")
}
zw <- sort(list.files(ORDNER_ZWISCHEN))
p_zeile("  Zwischendateien im Ordner Zwischen (ohne Kennung, G.1 Nr. 7): ", length(zw), " Dateien")
for (f in zw) p_zeile("    Zwischen/", f, "  ", sha256_datei(pfad_zwischen(f)))
p_zeile("")
ENDE <- Sys.time()
p_zeile("Ende des Gesamtlaufs: ", format(ENDE, "%Y-%m-%d %H:%M:%S UTC"), ", Dauer ",
        round(as.numeric(difftime(ENDE, START, units = "mins")), 1), " min")
p_zeile("Gesamtlauf ohne Abbruch beendet.")
writeLines(protokoll, pfad_abgabe(paste0("Laufprotokoll_", FASSUNG, ".txt")), useBytes = TRUE)

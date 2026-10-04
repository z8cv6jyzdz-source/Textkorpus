# =====================================================================
# Abgleich_2026-09-25.R
# Zweck: Abgleich zweier Ergebnisdateien nach G.1 je Kennung mit den Toleranzen
#        der Spezifikation Teil G.3 (Phase 6.1 des Auswertungsverfahrens).
#        Neutrales Skript ohne Bezug zu einer der beiden Implementierungen,
#        nur Basis-R. Es gleicht nichts an, es berichtet nur. Bei mindestens
#        einer Abweichung endet es mit Status 1, damit die Kette anhält.
# Schritt der Spezifikation: Teil G.3 (Toleranzen), S19 Regel 6 (Zufallsverfahren)
# Eingang: zwei Ergebnisdateien mit den Spalten Kennung, Wert, Einheit, Grund, Skript
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript Abgleich_2026-09-25.R <Ergebnisse_1.csv> <Ergebnisse_2.csv> [Ausgabestamm]
#         Datei 1 ist die erste Implementierung (a), Datei 2 die zweite (b).
#         Ausgabestamm voreingestellt: Abgleich_JJJJ-MM-TT (Datum des Laufs)
# Ausgabe: <Ausgabestamm>.csv (je Kennung) und <Ausgabestamm>_Protokoll.txt (Zusammenfassung)
#
# Toleranzklassen nach G.3:
#   EXAKT      Anzahlen, Merkmale, Setzugehörigkeiten: exakt gleich
#   DETERM     deterministische Rechnungen: |a − b| <= 1e-9 · max(1, |a|)
#   ITERATIV   Nullstellensuche S18 (MDES, MDESR), Shapiro-Wilk-p (S14 SWP), nichtzentrale
#              F-Verteilung (S18 POW): |a − b| <= 1e-6 · max(|a|, |b|)
#   ZUFALL     Bootstrap-Grenzen S19 BKIU und BKIO: |a − b| <= 3 · sqrt(MCSE_a² + MCSE_b²)
#              mit den MC-Standardfehlern BMCU und BMCO derselben Zielgröße aus beiden Dateien
#   NACHRICHT  S19 BSD, BMCU, BMCO, BNGUELT, BNVERW: nur berichtet, kein Urteil
#              (unterschiedliche Zufallsgeneratoren sind zulässig, S19 Regel 6)
# Fehlende Werte: beide fehlend mit gleichem Grund = bestanden, mit verschiedenem Grund
#   oder nur in einer Datei fehlend = Abweichung. Kennungen, die nur in einer Datei
#   stehen, sind Abweichungen.
# =====================================================================

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  cat("Aufruf: Rscript Abgleich_2026-09-25.R <Ergebnisse_1.csv> <Ergebnisse_2.csv> [Ausgabestamm]\n")
  quit(status = 2)
}
datei_a <- args[1]
datei_b <- args[2]
stamm <- if (length(args) >= 3) args[3] else paste0("Abgleich_", format(Sys.Date(), "%Y-%m-%d"))
invisible(Sys.setlocale("LC_ALL", "C.UTF-8"))

TOL_DETERM <- 1e-9
TOL_ITERATIV <- 1e-6
FAKTOR_ZUFALL <- 3

GROESSEN_EXAKT <- c("N", "K", "NZEIL", "NMELD", "NAUSL", "NGUELT", "NKAT", "NPAH", "NKORR", "NDUBL", "NSAMM",
                    "NSTAT", "ADH", "NZUG", "SUMME", sprintf("V%02d", 0:12), sprintf("GE%02d", 1:12), "NMELDSP",
                    "UE", "UESP", "INF", "MITGL", "FLZUG", "FLPRE", "FLAUSG", "FLNANG", "FLITT", "FLOPRE",
                    "FLOPOST", "FLOPAH", "B6NE", "B6NEKM", "B6IF", "B6FK", "B6NA", "DFTE", "NTE", "NSB", "FLEINZ",
                    "NFAM1", "NFAM2", "NFAMNA", "DF", "DFG", "UDDF", "DFINT", "DFCINT", "BFDF1", "BFDF2", "SIG",
                    "H0REJ", "NTEST", "NIG", "NKG", "SWVERW", "BFVERW", "VERW", "OVPREIG", "OVPREKG", "OVPAHIG",
                    "OVPAHKG", "NTOT", "DF1", "DF2", "BNGUELT", "BNVERW")
ITERATIV <- list(c("S18", "MDES"), c("S18", "MDESR"), c("S14", "SWP"), c("S18", "POW"))
ZUFALL <- list(c("S19", "BKIU"), c("S19", "BKIO"))
NACHRICHT <- list(c("S19", "BSD"), c("S19", "BMCU"), c("S19", "BMCO"), c("S19", "BNGUELT"), c("S19", "BNVERW"))

lies <- function(pfad) {
  stopifnot(file.exists(pfad))
  d <- read.csv(pfad, colClasses = "character", na.strings = character(0), check.names = FALSE,
                encoding = "UTF-8", fileEncoding = "UTF-8")
  fehlt <- setdiff(c("Kennung", "Wert", "Grund"), names(d))
  if (length(fehlt) > 0) stop("Spalten fehlen in ", pfad, ": ", paste(fehlt, collapse = ", "))
  if (any(duplicated(d$Kennung))) stop("Doppelte Kennungen in ", pfad)
  ok <- d$Wert == "" | grepl("^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)([eE][-+]?[0-9]+)?$", d$Wert)
  if (!all(ok)) stop("Werte außerhalb des Zahlenformats in ", pfad, ": ", paste(head(d$Wert[!ok], 5), collapse = " | "))
  d$zahl <- suppressWarnings(as.numeric(d$Wert))
  d$zahl[d$Wert == ""] <- NA_real_
  d
}
a <- lies(datei_a)
b <- lies(datei_b)

felder <- function(k) {
  t <- strsplit(k, ".", fixed = TRUE)[[1]]
  if (length(t) != 6) return(c(NA, NA, NA, NA, NA, NA))
  t
}
klasse_von <- function(k) {
  f <- felder(k)
  schritt <- f[1]
  groesse <- f[2]
  in_liste <- function(l) any(vapply(l, function(x) x[1] == schritt && x[2] == groesse, TRUE))
  if (in_liste(NACHRICHT)) return("NACHRICHT")
  if (in_liste(ZUFALL)) return("ZUFALL")
  if (in_liste(ITERATIV)) return("ITERATIV")
  if (groesse %in% GROESSEN_EXAKT) return("EXAKT")
  "DETERM"
}

alle <- sort(union(a$Kennung, b$Kennung))
ia <- match(alle, a$Kennung)
ib <- match(alle, b$Kennung)
erg <- data.frame(Kennung = alle, Klasse = vapply(alle, klasse_von, ""),
                  Wert_1 = ifelse(is.na(ia), "(fehlt)", a$Wert[ia]),
                  Wert_2 = ifelse(is.na(ib), "(fehlt)", b$Wert[ib]),
                  Grund_1 = ifelse(is.na(ia), "", a$Grund[ia]),
                  Grund_2 = ifelse(is.na(ib), "", b$Grund[ib]),
                  Abweichung = NA_real_, Toleranz = NA_real_, Urteil = "", stringsAsFactors = FALSE)

mcse <- function(d, ziel, groesse) {
  k <- paste0("S19.", groesse, ".", ziel, ".X.ITT.BOOT")
  j <- match(k, d$Kennung)
  if (is.na(j)) return(NA_real_)
  d$zahl[j]
}

for (i in seq_len(nrow(erg))) {
  k <- erg$Kennung[i]
  kl <- erg$Klasse[i]
  if (is.na(ia[i]) || is.na(ib[i])) {
    erg$Urteil[i] <- "ABWEICHUNG: Kennung nur in einer Datei"
    next
  }
  xa <- a$zahl[ia[i]]
  xb <- b$zahl[ib[i]]
  fa <- is.na(xa)
  fb <- is.na(xb)
  if (fa && fb) {
    erg$Urteil[i] <- if (identical(a$Grund[ia[i]], b$Grund[ib[i]])) "bestanden (beide fehlend, gleicher Grund)"
                     else "ABWEICHUNG: beide fehlend, Grund verschieden"
    next
  }
  if (fa != fb) {
    erg$Urteil[i] <- "ABWEICHUNG: nur in einer Datei fehlend"
    next
  }
  abw <- xb - xa
  erg$Abweichung[i] <- abw
  if (kl == "NACHRICHT") {
    erg$Urteil[i] <- "nachrichtlich"
  } else if (kl == "EXAKT") {
    erg$Toleranz[i] <- 0
    erg$Urteil[i] <- if (abw == 0) "bestanden" else "ABWEICHUNG"
  } else if (kl == "DETERM") {
    tol <- TOL_DETERM * max(1, abs(xa))
    erg$Toleranz[i] <- tol
    erg$Urteil[i] <- if (abs(abw) <= tol) "bestanden" else "ABWEICHUNG"
  } else if (kl == "ITERATIV") {
    tol <- TOL_ITERATIV * max(abs(xa), abs(xb))
    erg$Toleranz[i] <- tol
    erg$Urteil[i] <- if (abs(abw) <= tol) "bestanden" else "ABWEICHUNG"
  } else if (kl == "ZUFALL") {
    f <- felder(k)
    gr_mc <- if (f[2] == "BKIU") "BMCU" else "BMCO"
    ma <- mcse(a, f[3], gr_mc)
    mb <- mcse(b, f[3], gr_mc)
    if (is.na(ma) || is.na(mb)) {
      erg$Urteil[i] <- "ABWEICHUNG: MC-SE fehlt, Regel nicht anwendbar"
    } else {
      tol <- FAKTOR_ZUFALL * sqrt(ma^2 + mb^2)
      erg$Toleranz[i] <- tol
      erg$Urteil[i] <- if (abs(abw) <= tol) "bestanden" else "ABWEICHUNG"
    }
  }
}

erg$Abweichung_txt <- ifelse(is.na(erg$Abweichung), "", sprintf("%.6g", erg$Abweichung))
erg$Toleranz_txt <- ifelse(is.na(erg$Toleranz), "", sprintf("%.6g", erg$Toleranz))
aus <- erg[, c("Kennung", "Klasse", "Wert_1", "Wert_2", "Grund_1", "Grund_2", "Abweichung_txt", "Toleranz_txt", "Urteil")]
names(aus) <- c("Kennung", "Klasse", "Wert_1", "Wert_2", "Grund_1", "Grund_2", "Abweichung", "Toleranz", "Urteil")
write.csv(aus, paste0(stamm, ".csv"), row.names = FALSE, fileEncoding = "UTF-8")

abw <- grepl("^ABWEICHUNG", erg$Urteil)
p <- character(0)
p <- c(p, "ABGLEICHPROTOKOLL Phase 6.1 (Abgleich je Kennung nach Spezifikation Teil G.3)",
       paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
       paste0("Datei 1 (a): ", datei_a, ", Kennungen ", nrow(a)),
       paste0("Datei 2 (b): ", datei_b, ", Kennungen ", nrow(b)),
       paste0("Gemeinsame Kennungen: ", sum(!is.na(ia) & !is.na(ib)), ", nur in Datei 1: ", sum(!is.na(ia) & is.na(ib)),
              ", nur in Datei 2: ", sum(is.na(ia) & !is.na(ib))),
       "",
       "Urteile je Klasse (bestanden / Abweichung / nachrichtlich):")
for (kl in c("EXAKT", "DETERM", "ITERATIV", "ZUFALL", "NACHRICHT")) {
  s <- erg$Klasse == kl
  p <- c(p, sprintf("  %-10s %5d Kennungen: bestanden %5d, Abweichung %5d, nachrichtlich %5d", kl, sum(s),
                    sum(s & grepl("^bestanden", erg$Urteil)), sum(s & abw), sum(s & erg$Urteil == "nachrichtlich")))
}
p <- c(p, "", "Urteile je Schritt:")
schritte <- vapply(erg$Kennung, function(k) felder(k)[1], "")
for (st in sort(unique(schritte))) {
  s <- schritte == st
  p <- c(p, sprintf("  %-4s %5d Kennungen: Abweichungen %4d", st, sum(s), sum(s & abw)))
}
p <- c(p, "", "Größte relative Abweichungen der bestandenen deterministischen Kennungen (nachrichtlich):")
det <- erg[erg$Klasse == "DETERM" & grepl("^bestanden", erg$Urteil) & !is.na(erg$Abweichung) & erg$Abweichung != 0, ]
if (nrow(det) == 0) p <- c(p, "  keine (alle bestandenen deterministischen Kennungen sind identisch)")
if (nrow(det) > 0) {
  rel <- abs(det$Abweichung) / pmax(1, abs(as.numeric(det$Wert_1)))
  o <- order(-rel)[seq_len(min(10, nrow(det)))]
  for (j in o) p <- c(p, sprintf("  %-45s relativ %.3g", det$Kennung[j], rel[j]))
}
if (any(abw)) {
  p <- c(p, "", paste0("ABWEICHUNGEN (", sum(abw), "), zu klären in Phase 6, nichts angleichen:"))
  for (j in which(abw)) {
    p <- c(p, sprintf("  %-45s %-9s Wert 1 %-24s Wert 2 %-24s Abw %-12s Tol %-12s %s", erg$Kennung[j], erg$Klasse[j],
                      erg$Wert_1[j], erg$Wert_2[j], erg$Abweichung_txt[j], erg$Toleranz_txt[j], erg$Urteil[j]))
  }
  p <- c(p, "", "Urteil: NICHT bestanden. Die Kette hält an (Auswertungsverfahren 6.1).")
} else {
  p <- c(p, "", "Urteil: bestanden. Keine Abweichung außerhalb der Toleranzen von G.3.")
}
writeLines(p, paste0(stamm, "_Protokoll.txt"), useBytes = TRUE)
cat(p, sep = "\n")
quit(status = if (any(abw)) 1 else 0)

# =====================================================================
# Anhang_G_Diagramme_2026-10-01.R
# Zweck: Darstellungsskript für die Diagramme der Voraussetzungsprüfung in Anhang G (Abb. G1 bis G6):
#        Normal-Q-Q-Diagramme der Residuen und Residuen gegen vorhergesagten Abschlusswert,
#        Ausgangswert und %PAH je konfirmatorischer Zielgröße. Ersetzt für das Manuskript die
#        Grafiken S14_QQ_<Ziel>.png und S14_Linearitaet_<Ziel>.png der Abgabe, die unverändert bleibt.
# Rechnung: dieselbe wie S14 der berichteten Rechnung, aus dem eingefrorenen Datenstand der
#        Ergebnisdatei: Spieler des Analysesets je Zielgröße (S08.MITGL … ITT = 1), Bestwerte prä und
#        post (S04.BEST), %PAH (S05.PAH), Koeffizienten der Kovarianzanalyse (S13.B0 bis S13.B3).
#        Vorhersage = b0 + b1 · Gruppe + b2 · Ausgangswert + b3 · %PAH, Residuum = Abschlusswert − Vorhersage.
#        Keine neue Schätzung. Der Abgleich der Punkte mit den Modellobjekten der Abgabe
#        (Zwischen/S13_modelle.rds) läuft in einem eigenen Prüfskript.
# Form nach der Objektprüfung dvs vom 01.10.2026 (Befunde Anhang G, Klickfreigabe KF6, KF9):
#        Nummern Abb. G1 bis G6 mit Unterschrift und Anmerkung, keine Titel im Bild, keine Kürzel der
#        Ergebnisdatei, Achsen mit Einheit, Dezimalkomma und Minus U+2212, Arial 10 pt bei Endbreite,
#        Linien ab ¾ pt, Graustufen, Legende in der Anmerkung (Symbole beschrieben).
# Ausgabe (im Ausgabeordner): Abb_G1 … Abb_G6 als PNG (300 dpi, Graustufen) und PDF,
#        Anhang_G_2026-10-01_Liste.csv (Kennzeichnung, Titel, Anmerkung), Anhang_G_2026-10-01.md,
#        Anhang_G_2026-10-01_Punkte.csv (alle gezeichneten Punkte), Anhang_G_2026-10-01.txt.
# Aufruf: Rscript Anhang_G_Diagramme_2026-10-01.R <Ergebnisdatei.csv> <Ausgabeordner>
# Nur base R und grDevices.
# =====================================================================

invisible(suppressWarnings(Sys.setlocale("LC_CTYPE", "C.UTF-8")))
if (.Platform$OS.type == "windows") grDevices::windowsFonts(Arial = grDevices::windowsFont("Arial"))
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Aufruf: Rscript Anhang_G_Diagramme_2026-10-01.R <Ergebnisdatei.csv> <Ausgabeordner>")
EINGANG <- args[1]
AUS <- args[2]
dir.create(AUS, showWarnings = FALSE, recursive = TRUE)
FASSUNG <- "Anhang_G_2026-10-01"

E <- read.csv(EINGANG, colClasses = "character", encoding = "UTF-8", check.names = FALSE)
if (any(duplicated(E$Kennung))) stop("Kennung doppelt in der Ergebnisdatei")
WERT <- suppressWarnings(as.numeric(E$Wert))
names(WERT) <- E$Kennung
verwendet <- character(0)
w <- function(k) {
  if (!(k %in% names(WERT))) stop(paste("Kennung fehlt in der Ergebnisdatei:", k))
  verwendet <<- c(verwendet, k)
  unname(WERT[k])
}

MINUS <- "−"
ZIELE <- c(Z30 = "30-m-Sprint", CM = "505-Seitenmittel", SBJ = "Standweitsprung")
EINH <- function(z) if (z == "SBJ") "cm" else "s"
achse <- function(x, nd) gsub("-", MINUS, formatC(x, format = "f", digits = nd, decimal.mark = ","), fixed = TRUE)
nd_achse <- function(x) {
  for (nd in 0:4) if (all(abs(x * 10^nd - round(x * 10^nd)) < 1e-9)) return(nd)
  4
}

# ---------------------------------------------------------------- Daten je Zielgröße
codes <- sub("^S05\\.PAH\\.PAH\\.PRE\\.P(.*)\\.X$", "\\1", grep("^S05\\.PAH\\.PAH\\.PRE\\.P", E$Kennung, value = TRUE))
gruppe_von <- function(cd) if (substr(cd, 1, 2) %in% c("HL", "BW")) 1 else 0   # Vereine A und B sind die IG
DAT <- lapply(setNames(names(ZIELE), names(ZIELE)), function(z) {
  itt <- codes[sapply(codes, function(cd) w(sprintf("S08.MITGL.%s.X.P%s.ITT", z, cd)) == 1)]
  pre <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.PRE.P%s.X", z, cd)))
  post <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.POST.P%s.X", z, cd)))
  pah <- sapply(itt, function(cd) w(sprintf("S05.PAH.PAH.PRE.P%s.X", cd)))
  G <- sapply(itt, gruppe_von)
  ok <- !is.na(pre) & !is.na(post) & !is.na(pah)
  b <- c(w(sprintf("S13.B0.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B2.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B3.%s.X.ITT.HAUPT", z)))
  if (any(is.na(b))) stop(paste("Koeffizienten fehlen:", z))
  d <- data.frame(code = itt[ok], G = G[ok], pre = pre[ok], post = post[ok], pah = pah[ok], stringsAsFactors = FALSE)
  d$fitted <- b[1] + b[2] * d$G + b[3] * d$pre + b[4] * d$pah
  d$resid <- d$post - d$fitted
  if (sum(d$G == 1) != w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z)) || sum(d$G == 0) != w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z))) stop(paste("Analyseset weicht ab:", z))
  qq <- qqnorm(d$resid, plot.it = FALSE)
  d$qq_theor <- qq$x
  d
})

# ---------------------------------------------------------------- Geräte in Endbreite (KF9)
PT <- 10
LWD <- 1
grafik <- function(datei, breite_cm, hoehe_cm, zeichne) {
  if (.Platform$OS.type == "windows") {
    png(file.path(AUS, paste0(datei, ".png")), width = breite_cm, height = hoehe_cm, units = "cm", res = 300, pointsize = PT, type = "windows", antialias = "gray", family = "Arial")
  } else {
    png(file.path(AUS, paste0(datei, ".png")), width = breite_cm, height = hoehe_cm, units = "cm", res = 300, pointsize = PT, type = "cairo", antialias = "gray", family = "Arial")
  }
  zeichne()
  dev.off()
  cairo_pdf(file.path(AUS, paste0(datei, ".pdf")), width = breite_cm / 2.54, height = hoehe_cm / 2.54, pointsize = PT, family = "Arial")
  zeichne()
  dev.off()
}
achsen <- function(xl, yl) {
  xt <- pretty(xl, n = 4); xt <- xt[xt >= xl[1] & xt <= xl[2]]
  yt <- pretty(yl, n = 4); yt <- yt[yt >= yl[1] & yt <= yl[2]]
  axis(1, at = xt, labels = achse(xt, nd_achse(xt)), lwd = LWD)
  axis(2, at = yt, labels = achse(yt, nd_achse(yt)), lwd = LWD, las = 1)
  box(lwd = LWD)
}
spanne <- function(x, f = 0.06) range(x) + c(-1, 1) * f * diff(range(x))

LISTE <- data.frame(id = character(0), art = character(0), bereich = character(0), kennzeichnung = character(0),
                    titel = character(0), anmerkung = character(0), datei = character(0), stringsAsFactors = FALSE)
MD <- c("# Diagramme der Voraussetzungsprüfung (Anhang G)", "",
        paste0("Erzeugt von ", FASSUNG, ".R aus ", basename(EINGANG), ". Gesetzt wird mit Werkzeug_Objekte_Docx_2026-10-01.py."), "")
abbildung <- function(nr, id, titel, anmerkung) {
  stopifnot(!grepl("\\.$", titel))
  LISTE[nrow(LISTE) + 1, ] <<- c(id, "Abbildung", "Anhang", paste0("Abb. G", nr, "."), titel, anmerkung, paste0(id, ".png"))
  MD <<- c(MD, paste0("<!-- Objekt ", id, " -->"), paste0("![](", id, ".png)"), "", paste0("*Abb. G", nr, ".* ", titel), "", paste0("*Anmerkung.* ", anmerkung), "")
}
ABK <- "IG = Interventionsgruppe, KG = Kontrollgruppe, %PAH = Reifestatus als prozentualer Anteil der prognostizierten Erwachsenenkörperhöhe"
SYMBOLE <- "Gefüllte Kreise: IG, offene Kreise: KG"
nsatz <- function(z) paste0("Analyseset IG n = ", sum(DAT[[z]]$G == 1), ", KG n = ", sum(DAT[[z]]$G == 0))

# ---------------------------------------------------------------- Abb. G1 bis G3: Normal-Q-Q-Diagramme
QQ_BREITE <- 8.5
nr <- 0
for (z in names(ZIELE)) {
  nr <- nr + 1
  d <- DAT[[z]]
  zeichne <- function() {
    par(mar = c(3.2, 3.9, 0.6, 0.6), family = "Arial", mgp = c(2.1, 0.5, 0), tcl = -0.3, lwd = LWD, cex = 1)
    xl <- spanne(d$qq_theor); yl <- spanne(d$resid)
    plot(d$qq_theor, d$resid, type = "n", axes = FALSE, xlim = xl, ylim = yl, xlab = "Theoretisches Quantil", ylab = paste0("Residuum (", EINH(z), ")"))
    achsen(xl, yl)
    qqline(d$resid, lwd = LWD, lty = 1)
    points(d$qq_theor, d$resid, pch = ifelse(d$G == 1, 16, 1), cex = 0.8, lwd = LWD)
  }
  id <- sprintf("Abb_G%d_QQ_%s", nr, z)
  grafik(id, QQ_BREITE, QQ_BREITE, zeichne)
  abbildung(nr, id, paste0("Normal-Q-Q-Diagramm der Residuen der Kovarianzanalyse, ", ZIELE[[z]]),
    paste0(nsatz(z), ". ", ABK, ". Residuen des Modells mit Ausgangswert und %PAH als Kovariaten. Die Gerade verläuft durch das erste und dritte Quartil. ", SYMBOLE, ". Das Diagramm wurde nachträglich festgelegt."))
}

# ---------------------------------------------------------------- Abb. G4 bis G6: Residuen gegen Vorhersage, Ausgangswert und %PAH
LIN_BREITE <- 14.25
for (z in names(ZIELE)) {
  nr <- nr + 1
  d <- DAT[[z]]
  zeichne <- function() {
    par(mfrow = c(1, 3), mar = c(4.3, 4.5, 0.6, 0.4), family = "Arial", mgp = c(2.8, 0.5, 0), tcl = -0.3, lwd = LWD, cex = 1)
    xs <- list(d$fitted, d$pre, d$pah)
    xlab <- list(paste0("Vorhergesagter\nAbschlusswert (", EINH(z), ")"), paste0("Ausgangswert (", EINH(z), ")"), "%PAH")
    yl <- spanne(d$resid)
    for (k in 1:3) {
      xl <- spanne(xs[[k]])
      plot(xs[[k]], d$resid, type = "n", axes = FALSE, xlim = xl, ylim = yl, xlab = "", ylab = if (k == 1) paste0("Residuum (", EINH(z), ")") else "")
      mtext(xlab[[k]], side = 1, line = if (k == 1) 3.2 else 2.1, cex = 1)
      achsen(xl, yl)
      abline(h = 0, lty = 2, lwd = LWD)
      points(xs[[k]], d$resid, pch = ifelse(d$G == 1, 16, 1), cex = 0.8, lwd = LWD)
    }
  }
  id <- sprintf("Abb_G%d_Linearitaet_%s", nr, z)
  grafik(id, LIN_BREITE, 6.2, zeichne)
  abbildung(nr, id, paste0("Residuen der Kovarianzanalyse gegen vorhergesagten Abschlusswert, Ausgangswert und %PAH, ", ZIELE[[z]]),
    paste0(nsatz(z), ". ", ABK, ". Gestrichelt: Residuum null. ", SYMBOLE, "."))
}

# ---------------------------------------------------------------- Abschluss
if (any(grepl(intToUtf8(59), c(MD, unlist(LISTE)), fixed = TRUE))) stop("Semikolon in einem Objekt")
if (any(grepl("\\b(Z30|CM|SBJ|ITT|HAUPT|BEST)\\b", c(LISTE$titel, LISTE$anmerkung)))) stop("Kürzel der Ergebnisdatei in einer Beschriftung")
utils::write.table(LISTE, file.path(AUS, paste0(FASSUNG, "_Liste.csv")), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
punkte <- do.call(rbind, lapply(names(DAT), function(z) cbind(ziel = z, DAT[[z]])))
utils::write.table(punkte, file.path(AUS, paste0(FASSUNG, "_Punkte.csv")), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
writeLines(MD, file.path(AUS, paste0(FASSUNG, ".md")), useBytes = TRUE)
prot <- c(paste0(FASSUNG, ".R, Laufprotokoll"), paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")), paste0("Eingang: ", EINGANG),
          paste0("R: ", R.version.string), paste0("Kennungen verwendet: ", length(unique(verwendet))),
          paste0("Punkte je Zielgröße: ", paste(sapply(names(DAT), function(z) paste0(z, " ", nrow(DAT[[z]]))), collapse = ", ")),
          paste0("Dateien: ", paste(sort(list.files(AUS)), collapse = ", ")))
writeLines(prot, file.path(AUS, paste0(FASSUNG, ".txt")), useBytes = TRUE)
cat(paste(prot, collapse = "\n"), "\n")

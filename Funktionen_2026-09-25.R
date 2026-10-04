# =====================================================================
# Funktionen_2026-09-25.R
# Zweck: Funktionsbibliothek der Blindrechnung in R (zweite, unabhängige
#        Implementierung). Wird von jedem Schrittskript mit source() geladen.
#        Enthält keine Rechnung über Studiendaten und keine Zahl aus den Daten.
# Schritt der Spezifikation: Rechenkonventionen 0.5, Teil E (Notation),
#        Teil G (Ausgabe, Referenztests), sowie Hilfsfunktionen für S01 bis S19.
# Eingangsdateien: keine (die Bibliothek liest selbst keine Daten).
#        Die Pfade und Sollprüfsummen der Anlagen stehen unten in ANLAGEN.
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: nicht direkt. In jedem Skript: source("Funktionen_2026-09-25.R")
# Rechenumgebung: R 4.3.3, nur Basis-R (base, stats, utils, graphics, grDevices).
# =====================================================================

# ---------------------------------------------------------------------
# A Umgebung, Pfade, Abbruch
# ---------------------------------------------------------------------

invisible(Sys.setlocale("LC_ALL", "C.UTF-8"))
Sys.setenv(TZ = "UTC")
options(warn = 1, digits = 15, stringsAsFactors = FALSE, scipen = 0)

FASSUNG <- "2026-09-25"
DATUM_SPEZIFIKATION <- "2026-09-24"

# Ordner des laufenden Skripts (bei Rscript aus --file, sonst Arbeitsverzeichnis)
skript_ordner <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  treffer <- grep("^--file=", args, value = TRUE)
  if (length(treffer) == 1) {
    return(normalizePath(dirname(sub("^--file=", "", treffer))))
  }
  normalizePath(getwd())
}

skript_name <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  treffer <- grep("^--file=", args, value = TRUE)
  if (length(treffer) == 1) return(basename(sub("^--file=", "", treffer)))
  "interaktiv"
}

ORDNER_ABGABE <- skript_ordner()
ORDNER_EINGANG <- normalizePath(file.path(ORDNER_ABGABE, ".."))
ORDNER_DATENSTAND <- file.path(ORDNER_EINGANG, paste0("Datenstand_", DATUM_SPEZIFIKATION))
ORDNER_ZWISCHEN <- file.path(ORDNER_ABGABE, "Zwischen")
if (!dir.exists(ORDNER_ZWISCHEN)) dir.create(ORDNER_ZWISCHEN)

pfad_anlage <- function(name) {
  file.path(ORDNER_EINGANG, paste0("Spezifikation_", DATUM_SPEZIFIKATION, name))
}
pfad_datenstand <- function(name) file.path(ORDNER_DATENSTAND, name)
pfad_zwischen <- function(name) file.path(ORDNER_ZWISCHEN, name)
pfad_abgabe <- function(name) file.path(ORDNER_ABGABE, name)

# Sollprüfsummen der Anlagen der Spezifikation (ohne Sollliste im Datenstand,
# dokumentiert bei der Übernahme am 2026-09-25 und vor jeder Verwendung geprüft)
ANLAGEN <- c(
  "_Kennungen.csv"          = "90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe",
  "_Konstanten.csv"         = "6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329",
  "_Koeffizienten_KR.csv"   = "1eb1ffabf2b5e8949c752ca243254fcf93b77b4c368551fb2d6f5744abcd0c5f",
  "_Vokabular.csv"          = "7afaa01d82dc9f5ca10534a09f916dca5475842caa32e71aad866ba43612860f",
  "_Fragebogen.csv"         = "04318c066939248c5feca5077c65a703508a1137738310fdfa68b3a329003f04",
  "_Referenzdaten.csv"      = "5fcd4f50130cffe0271074af537d2430346e76191282ebe67dfac2e517c1bb88",
  "_Referenzdaten_Daten.csv" = "a6003700cf923646cf9341c866637fe227995543ce9096b458a5c4a45f662ac7"
)

# Abbruch mit klarer Meldung (Rechenkonvention 0.5 Nr. 10)
abbruch <- function(...) {
  meldung <- paste0(...)
  cat("\nABBRUCH: ", meldung, "\n", sep = "")
  stop(paste0("ABBRUCH: ", meldung), call. = FALSE)
}

pruefe <- function(bedingung, ...) {
  if (length(bedingung) != 1 || is.na(bedingung) || !isTRUE(bedingung)) abbruch(...)
  invisible(TRUE)
}

# Warnungen sichtbar machen und zählen
WARNUNGEN <- new.env()
WARNUNGEN$liste <- character(0)
merke_warnung <- function(w) {
  WARNUNGEN$liste <- c(WARNUNGEN$liste, conditionMessage(w))
  cat("WARNUNG: ", conditionMessage(w), "\n", sep = "")
  invokeRestart("muffleWarning")
}

# Kopf jedes Skripts auf die Standardausgabe
schreibe_kopf <- function(zweck, schritt, eingang) {
  cat("=====================================================================\n")
  cat("Skript:   ", skript_name(), "\n", sep = "")
  cat("Fassung:  ", FASSUNG, "\n", sep = "")
  cat("Zweck:    ", zweck, "\n", sep = "")
  cat("Schritt:  ", schritt, "\n", sep = "")
  cat("Aufruf:   Rscript ", skript_name(), "\n", sep = "")
  cat("Start:    ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")
  cat("R:        ", R.version.string, "\n", sep = "")
  cat("Eingang (Datei, SHA-256):\n")
  for (i in seq_along(eingang)) {
    cat("  ", names(eingang)[i], "  ", eingang[i], "\n", sep = "")
  }
  cat("=====================================================================\n")
}

# ---------------------------------------------------------------------
# B SHA-256 in reinem R (FIPS 180-4). R 4.3.3 hat keine eingebaute Funktion.
#   32-Bit-Wörter werden als double in [0, 2^32) geführt. Bitoperationen
#   laufen über die beiden 16-Bit-Hälften, weil R-Ganzzahlen 2^31 nicht fassen.
#   Die Konstanten entstehen aus den Wurzeln der ersten Primzahlen, wie im
#   Standard definiert, und werden nicht abgetippt.
# ---------------------------------------------------------------------

.M32 <- 4294967296
.primzahlen <- function(n) {
  p <- integer(0)
  k <- 2
  while (length(p) < n) {
    if (all(k %% p[p * p <= k] != 0)) p <- c(p, k)
    k <- k + 1
  }
  p
}
.SHA_PRIM <- .primzahlen(64)
.SHA_K <- floor(((.SHA_PRIM^(1 / 3)) %% 1) * .M32)
.SHA_H0 <- floor((sqrt(.SHA_PRIM[1:8]) %% 1) * .M32)

.xor32 <- function(a, b) {
  ah <- a %/% 65536
  bh <- b %/% 65536
  bitwXor(as.integer(ah), as.integer(bh)) * 65536 +
    bitwXor(as.integer(a - ah * 65536), as.integer(b - bh * 65536))
}
.and32 <- function(a, b) {
  ah <- a %/% 65536
  bh <- b %/% 65536
  bitwAnd(as.integer(ah), as.integer(bh)) * 65536 +
    bitwAnd(as.integer(a - ah * 65536), as.integer(b - bh * 65536))
}
.not32 <- function(a) 4294967295 - a
.rotr32 <- function(x, n) {
  t <- 2^n
  (x %/% t) + (x %% t) * (2^(32 - n))
}
.shr32 <- function(x, n) x %/% (2^n)

.sha256_block <- function(H, w16) {
  w <- numeric(64)
  w[1:16] <- w16
  for (i in 17:64) {
    x15 <- w[i - 15]
    x2 <- w[i - 2]
    s0 <- .xor32(.xor32(.rotr32(x15, 7), .rotr32(x15, 18)), .shr32(x15, 3))
    s1 <- .xor32(.xor32(.rotr32(x2, 17), .rotr32(x2, 19)), .shr32(x2, 10))
    w[i] <- (w[i - 16] + s0 + w[i - 7] + s1) %% .M32
  }
  a <- H[1]
  b <- H[2]
  c <- H[3]
  d <- H[4]
  e <- H[5]
  f <- H[6]
  g <- H[7]
  h <- H[8]
  for (i in 1:64) {
    S1 <- .xor32(.xor32(.rotr32(e, 6), .rotr32(e, 11)), .rotr32(e, 25))
    ch <- .xor32(.and32(e, f), .and32(.not32(e), g))
    temp1 <- (h + S1 + ch + .SHA_K[i] + w[i]) %% .M32
    S0 <- .xor32(.xor32(.rotr32(a, 2), .rotr32(a, 13)), .rotr32(a, 22))
    maj <- .xor32(.xor32(.and32(a, b), .and32(a, c)), .and32(b, c))
    temp2 <- (S0 + maj) %% .M32
    h <- g
    g <- f
    f <- e
    e <- (d + temp1) %% .M32
    d <- c
    c <- b
    b <- a
    a <- (temp1 + temp2) %% .M32
  }
  (H + c(a, b, c, d, e, f, g, h)) %% .M32
}

sha256_bytes <- function(bytes) {
  b <- as.integer(bytes)
  L <- length(b)
  bitlen <- L * 8
  rest <- (L + 1) %% 64
  nullen <- if (rest <= 56) 56 - rest else 120 - rest
  laenge <- integer(8)
  x <- bitlen
  for (i in 8:1) {
    laenge[i] <- x %% 256
    x <- x %/% 256
  }
  m <- c(b, 128L, rep(0L, nullen), as.integer(laenge))
  pruefe(length(m) %% 64 == 0, "SHA-256: Auffüllung fehlerhaft")
  w_alle <- m[seq(1, length(m), 4)] * 16777216 + m[seq(2, length(m), 4)] * 65536 +
    m[seq(3, length(m), 4)] * 256 + m[seq(4, length(m), 4)]
  H <- .SHA_H0
  nblock <- length(w_alle) / 16
  for (k in seq_len(nblock)) {
    H <- .sha256_block(H, w_alle[((k - 1) * 16 + 1):(k * 16)])
  }
  paste0(sprintf("%04x%04x", as.integer(H %/% 65536), as.integer(H %% 65536)), collapse = "")
}

sha256_datei <- function(pfad) {
  pruefe(file.exists(pfad), "Datei fehlt: ", pfad)
  groesse <- file.info(pfad)$size
  bytes <- readBin(pfad, what = "raw", n = groesse)
  pruefe(length(bytes) == groesse, "Datei unvollständig gelesen: ", pfad)
  sha256_bytes(bytes)
}

sha256_text <- function(text) sha256_bytes(charToRaw(enc2utf8(text)))

# Anlage lesen und Prüfsumme gegen die dokumentierte Sollprüfsumme prüfen
lies_anlage <- function(name) {
  pfad <- pfad_anlage(name)
  ist <- sha256_datei(pfad)
  pruefe(identical(ist, unname(ANLAGEN[name])),
         "Prüfsumme der Anlage ", name, " weicht ab. Soll ", ANLAGEN[name], " Ist ", ist)
  lies_csv(pfad)
}

# ---------------------------------------------------------------------
# C Einlesen von CSV (alles als Text, strenge Umwandlung danach)
# ---------------------------------------------------------------------

lies_csv <- function(pfad) {
  pruefe(file.exists(pfad), "Datei fehlt: ", pfad)
  d <- read.csv(pfad, colClasses = "character", na.strings = character(0),
                check.names = FALSE, encoding = "UTF-8", fileEncoding = "UTF-8",
                strip.white = FALSE, blank.lines.skip = FALSE)
  for (j in seq_along(d)) d[[j]] <- enc2utf8(d[[j]])
  names(d) <- enc2utf8(names(d))
  d
}

pruefe_spalten <- function(d, erwartet, datei) {
  pruefe(identical(names(d), enc2utf8(erwartet)),
         "Spaltennamen der Datei ", datei, " weichen ab. Erwartet: ",
         paste(erwartet, collapse = ", "), ". Gefunden: ", paste(names(d), collapse = ", "))
}

# Zahl im Datenformat (Dezimalpunkt, optional Vorzeichen, optional Exponent)
.MUSTER_ZAHL <- "^[-+]?([0-9]+([.][0-9]*)?|[.][0-9]+)([eE][-+]?[0-9]+)?$"
.MUSTER_GANZ <- "^[-+]?[0-9]+$"

als_zahl <- function(x, feld, leer_erlaubt = TRUE) {
  x <- as.character(x)
  leer <- is.na(x) | x == ""
  if (!leer_erlaubt) pruefe(!any(leer), "Feld ", feld, " enthält leere Werte")
  ok <- leer | grepl(.MUSTER_ZAHL, x)
  pruefe(all(ok), "Feld ", feld, " enthält Werte außerhalb des Zahlenformats: ",
         paste(unique(x[!ok]), collapse = " | "))
  erg <- rep(NA_real_, length(x))
  erg[!leer] <- as.numeric(x[!leer])
  erg
}

als_ganzzahl <- function(x, feld, zulaessig = NULL, leer_erlaubt = FALSE) {
  x <- as.character(x)
  leer <- is.na(x) | x == ""
  if (!leer_erlaubt) pruefe(!any(leer), "Feld ", feld, " enthält leere Werte")
  ok <- leer | grepl(.MUSTER_GANZ, x)
  pruefe(all(ok), "Feld ", feld, " enthält Werte außerhalb des Ganzzahlformats: ",
         paste(unique(x[!ok]), collapse = " | "))
  erg <- rep(NA_integer_, length(x))
  erg[!leer] <- as.integer(x[!leer])
  if (!is.null(zulaessig)) {
    falsch <- !leer & !(erg %in% zulaessig)
    pruefe(!any(falsch), "Feld ", feld, " enthält unzulässige Werte: ",
           paste(unique(x[falsch]), collapse = " | "))
  }
  erg
}

pruefe_kategorie <- function(x, feld, zulaessig) {
  x <- as.character(x)
  falsch <- !(x %in% enc2utf8(zulaessig))
  pruefe(!any(falsch), "Feld ", feld, " enthält unbekannte Kategorien: ",
         paste(unique(x[falsch]), collapse = " | "))
  invisible(TRUE)
}

# Konstanten der Anlage als benannte Liste (Text), Zahl über konstante_zahl()
lies_konstanten <- function() {
  k <- lies_anlage("_Konstanten.csv")
  pruefe_spalten(k, c("name", "wert", "einheit", "schritt", "bedeutung", "quelle", "fundstelle", "status"),
                 "_Konstanten.csv")
  pruefe(!any(duplicated(k$name)), "Konstantenliste: doppelte Namen")
  k
}
konstante_zahl <- function(k, name) {
  pruefe(name %in% k$name, "Konstante fehlt in der Anlage: ", name)
  als_zahl(k$wert[k$name == name], paste0("Konstante ", name), leer_erlaubt = FALSE)
}
konstante_text <- function(k, name) {
  pruefe(name %in% k$name, "Konstante fehlt in der Anlage: ", name)
  k$wert[k$name == name]
}

# ---------------------------------------------------------------------
# D Statistische Grundfunktionen (Rechenkonventionen 0.5)
# ---------------------------------------------------------------------

# Summen werden um den ersten Wert verschoben gerechnet (verschobene Daten,
# zweistufiger Algorithmus). Das vermeidet Auslöschung bei eng liegenden Werten
# und ist mathematisch identisch mit der direkten Formel. Der Referenztest R03
# (AtmWtAg) prüft die Stellengenauigkeit.

# Mittel, fehlend bei n = 0 (0.5 Nr. 13)
mittel <- function(x) {
  x <- x[!is.na(x)]
  n <- length(x)
  if (n == 0) return(NA_real_)
  c0 <- x[1]
  c0 + sum(x - c0) / n
}

# Summe der quadrierten Abweichungen vom Mittel, verschoben gerechnet
ss_abweichung <- function(x) {
  n <- length(x)
  if (n == 0) return(NA_real_)
  c0 <- x[1]
  d <- x - c0
  md <- sum(d) / n
  sum((d - md)^2)
}

# Standardabweichung mit Nenner n − 1, fehlend bei n < 2 (0.5 Nr. 2 und Nr. 13)
sd_n1 <- function(x) {
  x <- x[!is.na(x)]
  n <- length(x)
  if (n < 2) return(NA_real_)
  sqrt(ss_abweichung(x) / (n - 1))
}

# Gepoolte SD zweier Gruppen (0.5 Nr. 2), fehlend wenn eine Gruppe n < 2
sd_pool <- function(x1, x2) {
  x1 <- x1[!is.na(x1)]
  x2 <- x2[!is.na(x2)]
  n1 <- length(x1)
  n2 <- length(x2)
  if (n1 < 2 || n2 < 2) return(NA_real_)
  s1 <- sd_n1(x1)
  s2 <- sd_n1(x2)
  sqrt(((n1 - 1) * s1^2 + (n2 - 1) * s2^2) / (n1 + n2 - 2))
}

# Quantil Typ 7 nach 0.5 Nr. 7, fehlend bei n = 0
quantil7 <- function(x, p) {
  x <- sort(x[!is.na(x)])
  n <- length(x)
  if (n == 0) return(NA_real_)
  h <- (n - 1) * p + 1
  j <- floor(h)
  if (j >= n) return(x[n])
  x[j] + (h - j) * (x[j + 1] - x[j])
}
median7 <- function(x) quantil7(x, 0.5)

# Sicheres Minimum und Maximum (fehlend bei n = 0)
min_na <- function(x) {
  x <- x[!is.na(x)]
  if (length(x) == 0) return(NA_real_)
  min(x)
}
max_na <- function(x) {
  x <- x[!is.na(x)]
  if (length(x) == 0) return(NA_real_)
  max(x)
}

# Verteilungsquantile ungerundet (0.5 Nr. 12)
t_quantil <- function(p, df) qt(p, df = df)
chi2_quantil <- function(p, df) qchisq(p, df = df)
f_quantil <- function(p, df1, df2) qf(p, df1 = df1, df2 = df2)

# Zweiseitiger p-Wert aus der t-Verteilung (S13 Regel 2), numerisch über die
# obere Schwanzwahrscheinlichkeit, mathematisch gleich 2 · (1 − T_df(|t|))
p_zweiseitig_t <- function(t, df) 2 * pt(abs(t), df = df, lower.tail = FALSE)

# ---------------------------------------------------------------------
# E Kleinste Quadrate über QR-Zerlegung (Teil E Notation)
#    X Designmatrix mit einer Spalte je Parameter (erste Spalte Achsenabschnitt)
#    Rückgabe: rang_voll, koef, se, sigma, df, r2, V, resid, fitted, n, p
# ---------------------------------------------------------------------

kq_schaetzung <- function(X, y) {
  X <- as.matrix(X)
  pruefe(nrow(X) == length(y), "Kleinste Quadrate: Zeilenzahl von X und y verschieden")
  pruefe(!anyNA(X) && !anyNA(y), "Kleinste Quadrate: fehlende Werte in X oder y")
  n <- nrow(X)
  p <- ncol(X)
  if (n <= p) {
    return(list(rang_voll = FALSE, rang = NA_integer_, n = n, p = p, df = n - p))
  }
  # Spalten skalieren (numerische Stabilität), Achsenabschnitt unverändert
  skala <- apply(X, 2, function(s) {
    r <- sqrt(sum(s^2))
    if (r == 0) 1 else r
  })
  Xs <- sweep(X, 2, skala, "/")
  zerlegung <- qr(Xs)
  if (zerlegung$rank < p) {
    return(list(rang_voll = FALSE, rang = zerlegung$rank, n = n, p = p, df = n - p))
  }
  pruefe(identical(zerlegung$pivot, seq_len(p)), "Kleinste Quadrate: unerwartete Spaltenvertauschung")
  koef_s <- qr.coef(zerlegung, y)
  fitted <- as.vector(Xs %*% koef_s)
  resid <- y - fitted
  df <- n - p
  sse <- sum(resid^2)
  sigma2 <- sse / df
  R <- qr.R(zerlegung)
  Rinv <- backsolve(R, diag(p))
  XtXinv_s <- Rinv %*% t(Rinv)
  # Rückskalierung: koef = koef_s / skala, Kovarianz entsprechend
  koef <- koef_s / skala
  XtXinv <- XtXinv_s / outer(skala, skala)
  V <- sigma2 * XtXinv
  se <- sqrt(diag(V))
  sst <- ss_abweichung(y)
  r2 <- 1 - sse / sst
  list(rang_voll = TRUE, rang = p, n = n, p = p, df = df, koef = unname(koef), se = unname(se),
       sigma = sqrt(sigma2), r2 = r2, V = unname(V), resid = resid, fitted = fitted, sse = sse)
}

# Zusammenfassung eines Koeffizienten: Schätzer, SE, t, p, KI (0.5 Nr. 6 und 12)
koef_inferenz <- function(fit, j, niveau = 0.95) {
  b <- fit$koef[j]
  se <- fit$se[j]
  t <- b / se
  p <- p_zweiseitig_t(t, fit$df)
  q <- t_quantil(1 - (1 - niveau) / 2, fit$df)
  list(b = b, se = se, t = t, df = fit$df, p = p, kiu = b - q * se, kio = b + q * se)
}

# Einfaktorielle Varianzanalyse (S14 Regel 2, Referenztests R02, R03, R08)
anova_einfach <- function(y, gruppe) {
  pruefe(!anyNA(y) && !anyNA(gruppe), "Varianzanalyse: fehlende Werte")
  g <- factor(gruppe)
  k <- nlevels(g)
  n <- length(y)
  pruefe(k >= 2, "Varianzanalyse: weniger als zwei Gruppen")
  # verschobene Rechnung um den ersten Wert (siehe Abschnitt D)
  c0 <- y[1]
  d <- y - c0
  gesamt_d <- sum(d) / n
  ng <- tapply(d, g, length)
  mg_d <- tapply(d, g, function(v) sum(v) / length(v))
  ss_zw <- sum(ng * (mg_d - gesamt_d)^2)
  ss_in <- sum((d - mg_d[as.integer(g)])^2)
  df1 <- k - 1
  df2 <- n - k
  ms_zw <- ss_zw / df1
  ms_in <- ss_in / df2
  F <- ms_zw / ms_in
  p <- pf(F, df1, df2, lower.tail = FALSE)
  list(F = F, df1 = df1, df2 = df2, p = p, ss_zw = ss_zw, ss_in = ss_in,
       ms_zw = ms_zw, ms_in = ms_in, sigma = sqrt(ms_in), r2 = ss_zw / (ss_zw + ss_in),
       n = n, k = k)
}

# Brown-Forsythe: Levene mit Median als Zentrum (S14 Regel 2)
brown_forsythe <- function(werte, gruppe) {
  g <- factor(gruppe)
  zentren <- tapply(werte, g, median7)
  z <- abs(werte - zentren[as.integer(g)])
  anova_einfach(as.vector(z), g)
}

# Shapiro-Wilk nach Royston 1995, AS R94 (S14 Regel 1), n zwischen 3 und 5000
shapiro_wilk <- function(x) {
  x <- x[!is.na(x)]
  if (length(x) < 3) return(list(W = NA_real_, p = NA_real_, n = length(x)))
  pruefe(length(x) <= 5000, "Shapiro-Wilk: n über 5000")
  erg <- shapiro.test(x)
  list(W = unname(erg$statistic), p = unname(erg$p.value), n = length(x))
}

# Zwei-Gruppen-Vergleich mit gepoolter Varianz (S15 Regel 4, Referenztest R11)
zwei_gruppen <- function(x1, x2, niveau = 0.95) {
  x1 <- x1[!is.na(x1)]
  x2 <- x2[!is.na(x2)]
  n1 <- length(x1)
  n2 <- length(x2)
  m1 <- mittel(x1)
  m2 <- mittel(x2)
  sp <- sd_pool(x1, x2)
  d <- m1 - m2
  if (is.na(sp) || sp == 0) {
    return(list(n1 = n1, n2 = n2, m1 = m1, m2 = m2, sd_pool = sp, d = d, se = NA_real_,
                t = NA_real_, df = n1 + n2 - 2, p = NA_real_, kiu = NA_real_, kio = NA_real_))
  }
  se <- sp * sqrt(1 / n1 + 1 / n2)
  t <- d / se
  df <- n1 + n2 - 2
  p <- p_zweiseitig_t(t, df)
  q <- t_quantil(1 - (1 - niveau) / 2, df)
  list(n1 = n1, n2 = n2, m1 = m1, m2 = m2, sd_pool = sp, d = d, se = se, t = t, df = df, p = p,
       kiu = d - q * se, kio = d + q * se)
}

# Korrekturfaktor J (S15 Regel 2)
faktor_j <- function(df_g) 1 - 3 / (4 * df_g - 1)

# Typischer Messfehler als gepoolte Innerspieler-SD (S10 Regel 1)
# werte: Liste, ein Vektor je Spieler mit dessen gültigen Versuchen (nur k >= 2)
te_gepoolt <- function(liste) {
  liste <- liste[vapply(liste, length, 1L) >= 2]
  n_sp <- length(liste)
  if (n_sp == 0) return(list(te = NA_real_, df = 0L, n = 0L, mittel_alle = NA_real_))
  ss <- 0
  df <- 0
  alle <- numeric(0)
  for (v in liste) {
    ss <- ss + ss_abweichung(v)
    df <- df + (length(v) - 1)
    alle <- c(alle, v)
  }
  list(te = sqrt(ss / df), df = as.integer(df), n = as.integer(n_sp), mittel_alle = mittel(alle))
}

# ---------------------------------------------------------------------
# F Power der nichtzentralen F-Verteilung (S18, Referenztest R12)
# ---------------------------------------------------------------------

f_krit <- function(df1, df2, alpha) qf(1 - alpha, df1, df2)
power_f <- function(df1, df2, lambda, alpha) {
  fc <- f_krit(df1, df2, alpha)
  1 - pf(fc, df1, df2, ncp = lambda)
}

# Khamis-Roche-Vorhersage (S05 Regel 7)
khamis_roche_pas <- function(beta0, beta1, beta2, beta3, s_in, w_lb, mp_in) {
  beta0 + beta1 * s_in + beta2 * w_lb + beta3 * mp_in
}

# ---------------------------------------------------------------------
# G Ergebnisregister und Formatierung (G.1)
# ---------------------------------------------------------------------

GRUENDE_ZULAESSIG <- c("Eingang fehlt", "Fallzahlregel", "Rang", "zu wenige Werte", "konstant",
                       "außerhalb Gültigkeitsbereich", "nicht erhebbar", "keine Nullstelle")
# Zuordnung der Gründe zu den Fällen (Rückfrage R2 im Rückfragenprotokoll)
GRUND_EINGANG <- "Eingang fehlt"
GRUND_FALLZAHL <- "Fallzahlregel"
GRUND_RANG <- "Rang"
GRUND_ZU_WENIG <- "zu wenige Werte"
GRUND_KONSTANT <- "konstant"
GRUND_BEREICH <- "außerhalb Gültigkeitsbereich"
GRUND_NICHT_ERHEBBAR <- "nicht erhebbar"
GRUND_NULLSTELLE <- "keine Nullstelle"

formatiere_wert <- function(wert, typ) {
  if (is.null(wert) || length(wert) != 1 || is.na(wert)) return("")
  if (typ %in% c("anzahl", "merkmal")) {
    pruefe(is.finite(wert) && wert == round(wert), "Anzahl oder Merkmal nicht ganzzahlig: ", wert)
    if (typ == "merkmal") pruefe(wert %in% c(0, 1), "Merkmal nicht 0 oder 1: ", wert)
    return(sprintf("%.0f", wert))
  }
  pruefe(is.finite(wert), "Wert nicht endlich")
  # 17 signifikante Stellen einschließlich abschließender Nullen (G.1 Nr. 3, mindestens zwölf Stellen)
  sprintf("%#.17g", wert)
}

register_neu <- function(skript) {
  e <- new.env()
  e$kennung <- character(0)
  e$wert <- character(0)
  e$grund <- character(0)
  e$typ <- character(0)
  e$roh <- list()
  e$skript <- skript
  e
}

# wert NA und grund leer ist unzulässig (jeder fehlende Wert braucht einen Grund)
register_setze <- function(reg, kennung, wert, typ = "zahl", grund = "") {
  pruefe(length(kennung) == 1 && nchar(kennung) > 0, "Leere Kennung")
  pruefe(!(kennung %in% reg$kennung), "Kennung doppelt gesetzt: ", kennung)
  fehlt <- is.null(wert) || length(wert) != 1 || is.na(wert)
  if (fehlt) {
    pruefe(grund %in% GRUENDE_ZULAESSIG, "Fehlender Wert ohne zulässigen Grund: ", kennung, " Grund: ", grund)
    text <- ""
  } else {
    grund <- ""
    text <- formatiere_wert(wert, typ)
  }
  reg$kennung <- c(reg$kennung, kennung)
  reg$wert <- c(reg$wert, text)
  reg$grund <- c(reg$grund, grund)
  reg$typ <- c(reg$typ, typ)
  reg$roh[[kennung]] <- if (fehlt) NA_real_ else wert
  invisible(NULL)
}

# Bequeme Kurzform: setze Wert, bei NA mit Grund
setze <- function(reg, kennung, wert, typ = "zahl", grund = "") register_setze(reg, kennung, wert, typ, grund)

register_als_df <- function(reg) {
  data.frame(Kennung = reg$kennung, Wert = reg$wert, Grund = reg$grund, Skript = reg$skript,
             Typ = reg$typ, stringsAsFactors = FALSE)
}

register_speichere <- function(reg, schritt) {
  d <- register_als_df(reg)
  saveRDS(d, pfad_zwischen(paste0(schritt, "_ergebnisse.rds")))
  cat("\nErgebnisregister ", schritt, ": ", nrow(d), " Kennungen, davon fehlend mit Grund: ",
      sum(d$Wert == ""), "\n", sep = "")
  invisible(d)
}

# Ausgabe des Registers in die Textausgabe des Skripts
register_drucke <- function(reg) {
  d <- register_als_df(reg)
  cat("\nKennung | Wert | Grund\n")
  for (i in seq_len(nrow(d))) {
    cat(d$Kennung[i], " | ", d$Wert[i], " | ", d$Grund[i], "\n", sep = "")
  }
  invisible(NULL)
}

# ---------------------------------------------------------------------
# H Kennungen: Sollliste je Schritt mit ausgeschriebenen Spielerkennungen (0.3)
# ---------------------------------------------------------------------

lies_kennungen <- function() {
  k <- lies_anlage("_Kennungen.csv")
  pruefe_spalten(k, c("kennung", "schritt", "groesse", "ziel", "zeit", "menge", "variante",
                      "einheit", "beschreibung", "status", "spielermenge"), "_Kennungen.csv")
  pruefe(!any(duplicated(k$kennung)), "Kennungsliste: doppelte Kennungen")
  k
}

# spieler: Liste mit ALLE (alle Codes), IG (IG-Codes), AK9 (Liste je Zielgröße)
erwartete_kennungen <- function(kenn, schritt, spieler) {
  k <- kenn[kenn$schritt == schritt, ]
  erg <- character(0)
  typ <- character(0)
  einheit <- character(0)
  for (i in seq_len(nrow(k))) {
    sm <- k$spielermenge[i]
    if (sm == "") {
      erg <- c(erg, k$kennung[i])
      einheit <- c(einheit, k$einheit[i])
    } else {
      codes <- if (sm == "ALLE") spieler$ALLE else if (sm == "IG") spieler$IG else if (sm == "AK9") {
        pruefe(k$ziel[i] %in% names(spieler$AK9), "AK9-Menge fehlt für Ziel ", k$ziel[i])
        spieler$AK9[[k$ziel[i]]]
      } else abbruch("Unbekannte Spielermenge in der Kennungsliste: ", sm)
      pruefe(grepl("P<Code>", k$kennung[i], fixed = TRUE), "Spielermenge ohne Muster P<Code>: ", k$kennung[i])
      for (cd in codes) {
        erg <- c(erg, sub("P<Code>", paste0("P", cd), k$kennung[i], fixed = TRUE))
        einheit <- c(einheit, k$einheit[i])
      }
    }
  }
  data.frame(Kennung = erg, Einheit = einheit, stringsAsFactors = FALSE)
}

kennung_spieler <- function(muster, code) sub("P<Code>", paste0("P", code), muster, fixed = TRUE)

# Prüfung: Register enthält genau die erwarteten Kennungen
register_pruefe_vollstaendig <- function(reg, erwartet) {
  soll <- erwartet$Kennung
  ist <- reg$kennung
  fehlt <- setdiff(soll, ist)
  zuviel <- setdiff(ist, soll)
  pruefe(length(fehlt) == 0, "Kennungen fehlen im Register: ", paste(head(fehlt, 20), collapse = ", "),
         if (length(fehlt) > 20) " ..." else "")
  pruefe(length(zuviel) == 0, "Kennungen ohne Eintrag in der Anlage: ", paste(head(zuviel, 20), collapse = ", "),
         if (length(zuviel) > 20) " ..." else "")
  pruefe(!any(duplicated(ist)), "Doppelte Kennungen im Register")
  cat("Vollständigkeit der Kennungen geprüft: ", length(ist), " Kennungen wie in der Anlage.\n", sep = "")
  invisible(TRUE)
}

# ---------------------------------------------------------------------
# I Feste Bezeichner der Spezifikation (0.3, 0.4)
# ---------------------------------------------------------------------

ZEITPUNKT_PRAE <- "prä"
ZEITPUNKT_POST <- "post"
SEITE_LEER <- "–"
TESTS <- c("Sprint_5m", "Sprint_10m", "Sprint_30m", "COD_505", "Standweitsprung")
ZIEL_VON_TEST_SEITE <- function(test, seite) {
  ifelse(test == "Sprint_5m", "Z05",
  ifelse(test == "Sprint_10m", "Z10",
  ifelse(test == "Sprint_30m", "Z30",
  ifelse(test == "Standweitsprung", "SBJ",
  ifelse(test == "COD_505" & seite == "L", "CL",
  ifelse(test == "COD_505" & seite == "R", "CR", NA_character_))))))
}
ZIELE_SECHS <- c("Z05", "Z10", "Z30", "SBJ", "CL", "CR")
ZIELE_SIEBEN <- c("Z05", "Z10", "Z30", "SBJ", "CL", "CR", "CM")
ZIELE_KONF <- c("Z30", "CM", "SBJ")
ZIELE_ZEIT <- c("Z05", "Z10", "Z30", "CL", "CR", "CM")
ZEIT_KENN <- c("PRE", "POST")
zeit_kennung <- function(zeitpunkt) ifelse(zeitpunkt == ZEITPUNKT_PRAE, "PRE", ifelse(zeitpunkt == ZEITPUNKT_POST, "POST", NA_character_))

# Bester Wert einer Zielgröße: Minimum bei Zeiten, Maximum beim Standweitsprung (S04 Regel 2)
bestwert <- function(x, ziel) {
  x <- x[!is.na(x)]
  if (length(x) == 0) return(NA_real_)
  if (ziel == "SBJ") max(x) else min(x)
}

# Günstige Richtung für die IG (0.5 Nr. 5)
guenstig <- function(b1, ziel) if (ziel == "SBJ") b1 > 0 else b1 < 0

# ---------------------------------------------------------------------
# J Kernregeln der Aufbereitung als Funktionen (S02, S05, S06, S07, S14)
# ---------------------------------------------------------------------

# S02 Regel 2: Ist ein Sprintlauf auslösegestört? d Distanzen der vorhandenen
# gültigen Teilzeiten, t die Teilzeiten. Abschnitte ab 0 m mit t = 0.
lauf_gestoert <- function(d, t, v_max, dt_min) {
  if (length(d) == 0) return(FALSE)
  pruefe(length(d) == length(t) && !anyNA(d) && !anyNA(t), "Auslöseprüfung: ungültige Eingabe")
  pruefe(!any(duplicated(d)), "Auslöseprüfung: doppelte Distanz im Lauf")
  o <- order(d)
  dd <- diff(c(0, d[o]))
  dt <- diff(c(0, t[o]))
  if (any(dt <= dt_min)) return(TRUE)
  any(dd / dt > v_max)
}

# S05 Regel 6: Koeffizienten für ein Alter durch lineare Interpolation zwischen
# den Tabellenzeilen a_lo = floor(Alter / Raster) · Raster und a_lo + Raster
interpoliere_kr <- function(ko, alter, raster) {
  zeile <- function(a) {
    j <- which(abs(ko$alter_jahre - a) < 1e-9)
    pruefe(length(j) == 1, "Koeffizientenzeile fehlt für Alter ", a)
    c(ko$beta0[j], ko$stature_in[j], ko$weight_lb[j], ko$midparent_in[j])
  }
  a_lo <- floor(alter / raster) * raster
  w <- (alter - a_lo) / raster
  if (w == 0) return(list(a_lo = a_lo, w = w, beta = zeile(a_lo)))
  list(a_lo = a_lo, w = w, beta = (1 - w) * zeile(a_lo) + w * zeile(a_lo + raster))
}

# S06 Regel 9: Dubletten- und Sammelmeldungspaare. code, zeit (POSIXct), inhalt (Text)
paare_zaehlen <- function(code, zeit, inhalt, abstand_s) {
  n <- length(code)
  dubl <- integer(n)
  samm <- integer(n)
  n_dubl <- 0L
  n_samm <- 0L
  paare <- data.frame(i = integer(0), j = integer(0), Art = character(0), Abstand_s = numeric(0),
                      stringsAsFactors = FALSE)
  if (n >= 2) for (i in seq_len(n - 1)) for (j in (i + 1):n) {
    if (code[i] != code[j]) next
    abst <- abs(as.numeric(difftime(zeit[i], zeit[j], units = "secs")))
    if (abst > abstand_s) next
    if (inhalt[i] == inhalt[j]) {
      n_dubl <- n_dubl + 1L
      dubl[c(i, j)] <- 1L
      paare[nrow(paare) + 1, ] <- list(i, j, "Dublette", abst)
    } else {
      n_samm <- n_samm + 1L
      samm[c(i, j)] <- 1L
      paare[nrow(paare) + 1, ] <- list(i, j, "Sammelmeldung", abst)
    }
  }
  list(n_dubl = n_dubl, n_samm = n_samm, dublette = dubl, sammel = samm, paare = paare)
}

# S07 Regel 1 bis 4: Zählungen eines Spielers aus seinen Meldungen
adhaerenz_zaehlung <- function(status, woche, h003, deckel, wochen = paste0("W", 1:6)) {
  ganz <- status == "GANZ"
  list(NMELD = length(status),
       GANZ = sum(ganz),
       GT = sum(status %in% c("GANZ", "TEILW")),
       WOCAP = sum(vapply(wochen, function(w) min(deckel, sum(ganz & woche == w)), 0)),
       DIST = length(unique(h003[ganz])))
}

# S12 Regel 2: Überlappung zweier Gruppen mit eingeschlossenen Grenzen
ueberlappung <- function(xi, xk) {
  L <- max(min(xi), min(xk))
  U <- min(max(xi), max(xk))
  if (L > U) return(list(L = L, U = U, n_ig = 0L, n_kg = 0L))
  list(L = L, U = U, n_ig = sum(xi >= L & xi <= U), n_kg = sum(xk >= L & xk <= U))
}

# Modelldaten eines Analysesets (Teil E): Code, G, Prä, Post, PAH, F
# aggregat "BEST" (Hauptmodell) oder "MEAN" (Sensitivität MW)
modelldaten <- function(spieler, z, agg, pah, gruppe, fam, aggregat = "BEST") {
  a_pre <- agg[agg$Ziel == z & agg$ZeitKenn == "PRE", ]
  a_post <- agg[agg$Ziel == z & agg$ZeitKenn == "POST", ]
  d <- data.frame(Code = spieler, G = as.numeric(gruppe[spieler] == "IG"),
                  Pre = a_pre[[aggregat]][match(spieler, a_pre$Code)],
                  Post = a_post[[aggregat]][match(spieler, a_post$Code)],
                  PAH = pah$PAH[match(spieler, pah$Code)],
                  F = as.numeric(fam[spieler]), stringsAsFactors = FALSE)
  pruefe(!anyNA(d[, c("G", "Pre", "Post", "PAH")]), "Modelldaten unvollständig für ", z)
  d
}

# Merkmal INF eines Sets aus der Tabelle von S08
inf_von <- function(sets, z, set) {
  i <- sets$inf$INF[sets$inf$Ziel == z & sets$inf$Set == set]
  pruefe(length(i) == 1, "INF nicht eindeutig für ", z, " ", set)
  i
}

# Kennungen b1, SE, df, t, p, KI, n je Gruppe einer Analyse setzen (S16, S17)
setze_b1_analyse <- function(reg, schritt, z, menge, variante, d, fit, inf, KI, spalte_g = 2, grund_zusatz = "") {
  suf <- paste0(".", z, ".X.", menge, ".", variante)
  setze(reg, paste0(schritt, ".NIG", suf), sum(d$G == 1), "anzahl")
  setze(reg, paste0(schritt, ".NKG", suf), sum(d$G == 0), "anzahl")
  namen <- c("B1", "SEB1", "DF", "T", "P", "KIU", "KIO")
  grund <- if (inf == 0) GRUND_FALLZAHL else if (is.null(fit) || !fit$rang_voll) GRUND_RANG else ""
  if (grund != "") {
    for (nm in namen) setze(reg, paste0(schritt, ".", nm, suf), NA_real_, if (nm == "DF") "anzahl" else "zahl", grund)
    return(invisible(grund))
  }
  ki <- koef_inferenz(fit, spalte_g, KI)
  setze(reg, paste0(schritt, ".B1", suf), ki$b, "zahl")
  setze(reg, paste0(schritt, ".SEB1", suf), ki$se, "zahl")
  setze(reg, paste0(schritt, ".DF", suf), ki$df, "anzahl")
  setze(reg, paste0(schritt, ".T", suf), ki$t, "zahl")
  setze(reg, paste0(schritt, ".P", suf), ki$p, "zahl")
  setze(reg, paste0(schritt, ".KIU", suf), ki$kiu, "zahl")
  setze(reg, paste0(schritt, ".KIO", suf), ki$kio, "zahl")
  invisible("")
}

# Hilfsfunktion: Zwischendatei lesen mit Abbruch, wenn sie fehlt
lies_zwischen <- function(name) {
  pfad <- pfad_zwischen(name)
  pruefe(file.exists(pfad), "Zwischendatei fehlt (vorheriger Schritt nicht gelaufen): ", name)
  readRDS(pfad)
}

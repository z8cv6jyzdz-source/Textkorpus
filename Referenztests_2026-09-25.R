# =====================================================================
# Referenztests_2026-09-25.R
# Zweck: Referenztests R01 bis R13 (Spezifikation Teil G.2, Phase 4.1).
#        Jeder Sollwert der Anlage _Referenzdaten.csv wird mit den Daten der
#        Anlage _Referenzdaten_Daten.csv und denselben Funktionen gerechnet,
#        die später die Studiendaten rechnen (Funktionen_2026-09-25.R).
#        Ausgabe je Sollwert: Test, Größe, Sollwert, eigener Wert, Abweichung,
#        Toleranz, bestanden (0 oder 1). Ein nicht bestandener Test hält an.
# Schritt der Spezifikation: Teil G.2 und G.3 (Toleranzen)
# Eingangsdateien (SHA-256):
#   Spezifikation_2026-09-24_Referenzdaten.csv
#     5fcd4f50130cffe0271074af537d2430346e76191282ebe67dfac2e517c1bb88
#   Spezifikation_2026-09-24_Referenzdaten_Daten.csv
#     a6003700cf923646cf9341c866637fe227995543ce9096b458a5c4a45f662ac7
#   Funktionen_2026-09-25.R (Bibliothek, Prüfsumme im Laufprotokoll)
# Fassung: 2026-09-25, erste Fassung mit Nachtrag Toleranz R08 vom 2026-09-25
#   (Rückfrage R5, Antwort des Verfassers: Toleranz für R08 Teststatistik W 1e-5 statt
#   5e-7 und für R08 F_9,90(0,95) 1e-4 statt 5e-5, Grund Genauigkeit der Quelle.
#   Die Anlage bleibt unverändert, der Nachtrag steht in NACHTRAEGE_TOLERANZ).
# Aufruf: Rscript Referenztests_2026-09-25.R
# Ausgabe: Referenztests_2026-09-25.txt (Standardausgabe), Zwischen/Referenztests_ergebnis.csv
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

schreibe_kopf(
  zweck = "Referenztests R01 bis R13 mit veröffentlichten Sollwerten",
  schritt = "Teil G.2 (Phase 4.1)",
  eingang = c("Spezifikation_2026-09-24_Referenzdaten.csv" = ANLAGEN["_Referenzdaten.csv"],
              "Spezifikation_2026-09-24_Referenzdaten_Daten.csv" = ANLAGEN["_Referenzdaten_Daten.csv"])
)

ref <- lies_anlage("_Referenzdaten.csv")
pruefe_spalten(ref, c("ref_id", "datensatz", "url", "fundstelle", "eingang", "groesse", "sollwert",
                      "toleranz", "schritt", "hinweis"), "_Referenzdaten.csv")
# Nachtrag Toleranz (Rückfragenprotokoll R5, 2026-09-25): ersetzt die Toleranz einzelner Sollwerte
NACHTRAEGE_TOLERANZ <- data.frame(
  ref_id = c("R08", "R08"),
  groesse = c("Teststatistik W", "F_9,90(0.95)"),
  toleranz_neu = c("0.00001", "0.0001"),
  datum = c("2026-09-25", "2026-09-25"),
  grund = c("Genauigkeit der Quelle (Rechnung in einfacher Genauigkeit in Dataplot)",
            "gedruckter Quantilwert abgeschnitten statt gerundet"),
  stringsAsFactors = FALSE)
cat("\nNachträge zur Toleranz (Verfasser, Rückfrage R5):\n")
for (i in seq_len(nrow(NACHTRAEGE_TOLERANZ))) {
  j <- which(ref$ref_id == NACHTRAEGE_TOLERANZ$ref_id[i] & ref$groesse == NACHTRAEGE_TOLERANZ$groesse[i])
  pruefe(length(j) == 1, "Nachtrag Toleranz: Sollwert nicht eindeutig gefunden: ", NACHTRAEGE_TOLERANZ$groesse[i])
  cat("  ", ref$ref_id[j], " ", ref$groesse[j], ": Toleranz ", ref$toleranz[j], " ersetzt durch ",
      NACHTRAEGE_TOLERANZ$toleranz_neu[i], " (Nachtrag vom ", NACHTRAEGE_TOLERANZ$datum[i], ", ",
      NACHTRAEGE_TOLERANZ$grund[i], ")\n", sep = "")
  ref$toleranz[j] <- NACHTRAEGE_TOLERANZ$toleranz_neu[i]
}

dat <- lies_anlage("_Referenzdaten_Daten.csv")
pruefe_spalten(dat, c("ref_id", "datensatz", "beobachtung", "variable", "wert"), "_Referenzdaten_Daten.csv")
dat$wert_zahl <- als_zahl(dat$wert, "Referenzdaten wert", leer_erlaubt = FALSE)
dat$beob <- als_ganzzahl(dat$beobachtung, "Referenzdaten beobachtung")

# Daten eines Referenztests als breite Tabelle (eine Zeile je Beobachtung)
daten_von <- function(id) {
  d <- dat[dat$ref_id == id, ]
  pruefe(nrow(d) > 0, "Keine Referenzdaten für ", id)
  vars <- unique(d$variable)
  beob <- sort(unique(d$beob))
  erg <- data.frame(beob = beob)
  for (v in vars) {
    dv <- d[d$variable == v, ]
    pruefe(!any(duplicated(dv$beob)), "Referenzdaten ", id, ": doppelte Beobachtung für ", v)
    erg[[v]] <- dv$wert_zahl[match(beob, dv$beob)]
  }
  erg
}

# Zahl aus einem Text der Spalte eingang ziehen, etwa "df = 10"
zahl_aus_text <- function(text, name) {
  muster <- paste0(name, "\\s*=?\\s*([-+]?[0-9]*[.]?[0-9]+)")
  m <- regmatches(text, regexec(muster, text))[[1]]
  pruefe(length(m) == 2, "Parameter ", name, " nicht gefunden in: ", text)
  as.numeric(m[2])
}

# Toleranzprüfung nach Teil G.3
pruefe_toleranz <- function(soll, ist, toleranz) {
  if (is.na(ist)) return(list(bestanden = 0L, abweichung = NA_real_, regel = toleranz))
  abw <- ist - soll
  tol <- trimws(toleranz)
  if (tol == "exakt") {
    ok <- abw == 0
  } else if (grepl("1e-9 relativ", tol, fixed = TRUE)) {
    ok <- abs(abw) <= 1e-9 * max(1, abs(soll))
  } else if (grepl("signifikante Stellen", tol, fixed = TRUE)) {
    stellen <- zahl_aus_text(tol, "mindestens")
    lre <- if (abw == 0) Inf else -log10(abs(abw) / abs(soll))
    ok <- lre >= stellen
  } else if (grepl(.MUSTER_ZAHL, tol)) {
    ok <- abs(abw) <= as.numeric(tol)
  } else {
    abbruch("Unbekannte Toleranzangabe: ", toleranz)
  }
  list(bestanden = as.integer(ok), abweichung = abw, regel = tol)
}

# ---------------------------------------------------------------------
# Rechnung je Test, Ergebnis als benannte Liste groesse -> Istwert
# ---------------------------------------------------------------------

ist_werte <- list()

# R01 NumAcc1
d <- daten_von("R01")
ist_werte[["R01"]] <- list("Mittel" = mittel(d$y), "SD mit Nenner n − 1" = sd_n1(d$y))

# R02 SiRstv, R03 AtmWtAg: einfaktorielle Varianzanalyse
anova_liste <- function(a) {
  list("F" = a$F, "Residuen-SD" = a$sigma, "R²" = a$r2, "df zwischen" = a$df1,
       "df innerhalb" = a$df2, "SS zwischen" = a$ss_zw, "SS innerhalb" = a$ss_in,
       "MS zwischen" = a$ms_zw, "MS innerhalb" = a$ms_in)
}
d <- daten_von("R02")
ist_werte[["R02"]] <- anova_liste(anova_einfach(d$resistance, d$instrument))
d <- daten_von("R03")
ist_werte[["R03"]] <- anova_liste(anova_einfach(d$agwt, d$instrument))

# R04 Norris: einfache Regression
d <- daten_von("R04")
fit <- kq_schaetzung(cbind(1, d$x), d$y)
pruefe(fit$rang_voll, "R04: Designmatrix ohne vollen Rang")
ist_werte[["R04"]] <- list("B0" = fit$koef[1], "SE B0" = fit$se[1], "B1" = fit$koef[2], "SE B1" = fit$se[2],
                           "Residuen-SD" = fit$sigma, "R²" = fit$r2)

# R05 Longley: multiple Regression
d <- daten_von("R05")
X <- cbind(1, d$x1, d$x2, d$x3, d$x4, d$x5, d$x6)
fit <- kq_schaetzung(X, d$y)
pruefe(fit$rang_voll, "R05: Designmatrix ohne vollen Rang")
l <- list()
for (j in 0:6) {
  l[[paste0("B", j)]] <- fit$koef[j + 1]
  l[[paste0("SE B", j)]] <- fit$se[j + 1]
}
l[["Residuen-SD"]] <- fit$sigma
l[["R²"]] <- fit$r2
ist_werte[["R05"]] <- l

# R08 und R13: GEAR
d <- daten_von("R08 R13")
bf <- brown_forsythe(d$diameter, d$batch)
ist_werte[["R08"]] <- list("Teststatistik W" = bf$F, "df1" = bf$df1, "df2" = bf$df2)
s_gear <- sd_n1(d$diameter)
n_gear <- sum(!is.na(d$diameter))
ist_werte[["R13"]] <- list("df" = n_gear - 1)
ist_werte[["R13_sd"]] <- s_gear
ist_werte[["R13_n"]] <- n_gear

# R09 ZARR13: Shapiro-Wilk
d <- daten_von("R09")
sw <- shapiro_wilk(d$y)
ist_werte[["R09"]] <- list("n" = sw$n, "W" = sw$W, "p" = sw$p)

# R10 Khamis-Roche-Beispiel
d <- daten_von("R10")
pruefe(nrow(d) == 1, "R10: genau eine Beobachtung erwartet")
ist_werte[["R10"]] <- list("PAS in Zoll" = khamis_roche_pas(d$beta0, d$stature_koeff, d$weight_koeff,
                                                             d$midparent_koeff, d$stature_in, d$weight_lb,
                                                             d$midparent_in))

# R11 Lakens Tab. 3: zwei unabhängige Gruppen
d <- daten_von("R11")
g1 <- d$wert[d$gruppe == 1]
g2 <- d$wert[d$gruppe == 2]
zg <- zwei_gruppen(g1, g2)
ds <- zg$d / zg$sd_pool
ist_werte[["R11"]] <- list("M Movie 1" = zg$m1, "M Movie 2" = zg$m2, "SD Movie 1" = sd_n1(g1),
                           "SD Movie 2" = sd_n1(g2), "d_s" = ds, "g_s" = ds * faktor_j(zg$df),
                           "t" = zg$t, "p" = zg$p, "KI der Differenz, untere Grenze" = zg$kiu,
                           "KI der Differenz, obere Grenze" = zg$kio)

# ---------------------------------------------------------------------
# Vergleich je Zeile der Anlage
# ---------------------------------------------------------------------

ergebnis <- data.frame(Test = character(0), Groesse = character(0), Sollwert = character(0),
                       Ist = character(0), Abweichung = character(0), Toleranz = character(0),
                       bestanden = integer(0), stringsAsFactors = FALSE)

for (i in seq_len(nrow(ref))) {
  id <- ref$ref_id[i]
  gr <- ref$groesse[i]
  eingang <- ref$eingang[i]
  soll <- als_zahl(ref$sollwert[i], paste0("Sollwert ", id, " ", gr), leer_erlaubt = FALSE)
  ist <- NA_real_
  if (id %in% c("R01", "R02", "R03", "R04", "R05", "R08", "R09", "R10", "R11")) {
    if (gr %in% names(ist_werte[[id]])) {
      ist <- ist_werte[[id]][[gr]]
    } else if (id == "R08" && grepl("^F_", gr)) {
      alpha <- zahl_aus_text(eingang, "α")
      ist <- f_quantil(1 - alpha, zahl_aus_text(eingang, "df1"), zahl_aus_text(eingang, "df2"))
    } else {
      abbruch("Referenztest ", id, ": Größe ohne Rechnung: ", gr)
    }
  } else if (id == "R06") {
    ist <- t_quantil(zahl_aus_text(eingang, "p"), zahl_aus_text(eingang, "df"))
  } else if (id == "R07") {
    ist <- chi2_quantil(zahl_aus_text(eingang, "p"), zahl_aus_text(eingang, "df"))
  } else if (id == "R13") {
    if (gr == "T") {
      sigma0 <- zahl_aus_text(eingang, "σ0")
      ist <- (ist_werte[["R13_n"]] - 1) * (ist_werte[["R13_sd"]] / sigma0)^2
    } else if (gr == "df") {
      ist <- ist_werte[["R13"]][["df"]]
    } else if (grepl("^χ²", gr)) {
      ist <- chi2_quantil(zahl_aus_text(eingang, "p"), zahl_aus_text(eingang, "df"))
    } else {
      abbruch("R13: Größe ohne Rechnung: ", gr)
    }
  } else if (id == "R12") {
    if (ref$datensatz[i] == "G*Power Beispiel") {
      f <- zahl_aus_text(eingang, "f")
      alpha <- zahl_aus_text(eingang, "α")
      df1 <- zahl_aus_text(eingang, "df1")
      k <- zahl_aus_text(eingang, "k")
      N <- zahl_aus_text(eingang, "N")
      lambda <- f^2 * N
      df2 <- N - k
      if (gr == "λ") ist <- lambda
      else if (gr == "F_crit") ist <- f_krit(df1, df2, alpha)
      else if (gr == "df2") ist <- df2
      else if (gr == "Power") ist <- power_f(df1, df2, lambda, alpha)
      else if (grepl("^kleinstes N", gr)) {
        ziel <- zahl_aus_text(gr, "Power ≥")
        Nk <- k + 1
        while (power_f(df1, Nk - k, f^2 * Nk, alpha) < ziel) Nk <- Nk + 1
        ist <- Nk
      } else abbruch("R12 G*Power: Größe ohne Rechnung: ", gr)
    } else if (ref$datensatz[i] == "Cohen Tab. 8.3.12") {
      u <- zahl_aus_text(eingang, "u")
      alpha <- zahl_aus_text(eingang, "α")
      n <- zahl_aus_text(eingang, "n")
      f <- zahl_aus_text(eingang, "f")
      pruefe(gr == "Power × 100", "R12 Cohen 8.3.12: unerwartete Größe ", gr)
      ist <- 100 * power_f(u, 2 * (n - 1), f^2 * 2 * n, alpha)
    } else if (ref$datensatz[i] %in% c("Cohen Tab. 8.4.4", "Cohen Tab. 2.4.1")) {
      alpha <- zahl_aus_text(eingang, "α")
      ziel <- zahl_aus_text(eingang, "Power")
      f <- if (grepl("f = d/2", eingang, fixed = TRUE)) zahl_aus_text(eingang, "d") / 2 else zahl_aus_text(eingang, "f")
      pruefe(gr == "n je Gruppe", "R12 Cohen: unerwartete Größe ", gr)
      n <- 2
      while (power_f(1, 2 * (n - 1), f^2 * 2 * n, alpha) < ziel) n <- n + 1
      ist <- n
    } else abbruch("R12: unbekannter Datensatz ", ref$datensatz[i])
  } else {
    abbruch("Unbekannter Referenztest: ", id)
  }
  tp <- pruefe_toleranz(soll, ist, ref$toleranz[i])
  ergebnis[nrow(ergebnis) + 1, ] <- list(id, gr, ref$sollwert[i], sprintf("%.15g", ist),
                                         if (is.na(tp$abweichung)) "" else sprintf("%.6g", tp$abweichung),
                                         tp$regel, tp$bestanden)
}

cat("\nReferenztests: Soll, Ist, Abweichung, Toleranz, bestanden\n")
cat("---------------------------------------------------------------------\n")
for (i in seq_len(nrow(ergebnis))) {
  cat(sprintf("%-4s %-36s Soll %-22s Ist %-22s Abw %-12s Tol %-36s bestanden %d\n",
              ergebnis$Test[i], ergebnis$Groesse[i], ergebnis$Sollwert[i], ergebnis$Ist[i],
              ergebnis$Abweichung[i], ergebnis$Toleranz[i], ergebnis$bestanden[i]))
}
cat("---------------------------------------------------------------------\n")
cat("Sollwerte gesamt: ", nrow(ergebnis), ", bestanden: ", sum(ergebnis$bestanden),
    ", nicht bestanden: ", sum(ergebnis$bestanden == 0), "\n", sep = "")

write.csv(ergebnis, pfad_zwischen("Referenztests_ergebnis.csv"), row.names = FALSE, fileEncoding = "UTF-8")

pruefe(all(ergebnis$bestanden == 1), "Mindestens ein Referenztest nicht bestanden. Die Auswertung hält an.")
cat("Alle Referenztests bestanden.\n")
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

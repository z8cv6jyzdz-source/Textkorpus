# =====================================================================
# Grenzfaelle_2026-09-25.R
# Zweck: Grenzfälle (Phase 4.2): kleine konstruierte Datensätze mit fehlenden,
#        ungültigen oder doppelten Werten. Das erwartete Ergebnis steht je Fall
#        ausgeschrieben im Skript (von Hand nachrechenbar), gerechnet wird mit
#        denselben Bibliotheksfunktionen wie in den Schritten S01 bis S19.
#        Ausgabe je Fall: Fall, Soll, Ist, Urteil (bestanden 0 oder 1).
# Schritt der Spezifikation: Auswertungsverfahren Phase 4.2, Rechenkonventionen 0.5
# Eingangsdateien (SHA-256):
#   Funktionen_2026-09-25.R (Bibliothek, Prüfsumme im Laufprotokoll)
#   Datenstand_2026-09-24 (nur für die Gegenprobe der SHA-256-Funktion, Prüfsummen im Kopf von S01)
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript Grenzfaelle_2026-09-25.R
# Ausgabe: Grenzfaelle_2026-09-25.txt, Zwischen/Grenzfaelle_ergebnis.csv
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

schreibe_kopf(zweck = "Grenzfälle mit von Hand nachrechenbaren Sollwerten", schritt = "Phase 4.2",
              eingang = c("Funktionen_2026-09-25.R" = sha256_datei(pfad_abgabe("Funktionen_2026-09-25.R"))))

faelle <- data.frame(Fall = character(0), Soll = character(0), Ist = character(0), bestanden = integer(0),
                     stringsAsFactors = FALSE)
gleich <- function(soll, ist, tol = 1e-12) {
  if (length(soll) != length(ist)) return(FALSE)
  if (is.character(soll)) return(identical(soll, ist))
  if (any(is.na(soll) != is.na(ist))) return(FALSE)
  s <- soll[!is.na(soll)]
  i <- ist[!is.na(ist)]
  all(abs(s - i) <= tol * pmax(1, abs(s)))
}
fmt <- function(x) {
  if (is.character(x)) return(paste(x, collapse = " "))
  paste(ifelse(is.na(x), "NA", format(x, digits = 15)), collapse = " ")
}
fall <- function(name, soll, ist, tol = 1e-12) {
  ok <- gleich(soll, ist, tol)
  faelle[nrow(faelle) + 1, ] <<- list(name, fmt(soll), fmt(ist), as.integer(ok))
  invisible(ok)
}
# Erwarteter Abbruch: bestanden, wenn die Funktion mit ABBRUCH endet
erwarte_abbruch <- function(name, ausdruck) {
  erg <- tryCatch({
    force(ausdruck)
    "kein Abbruch"
  }, error = function(e) if (grepl("^ABBRUCH", conditionMessage(e))) "Abbruch" else "anderer Fehler")
  # Die Funktion abbruch() schreibt die Meldung auf die Ausgabe, das ist hier beabsichtigt
  fall(name, "Abbruch", erg)
}

# G01 Mittel und SD, Nenner n − 1 (0.5 Nr. 2): x = 1, 2, 3, 4: Mittel 10/4 = 2,5,
# Abweichungsquadrate 2,25 + 0,25 + 0,25 + 2,25 = 5, SD = sqrt(5/3)
fall("G01a Mittel von 1 2 3 4 = 2.5", 2.5, mittel(c(1, 2, 3, 4)))
fall("G01b SD von 1 2 3 4 = sqrt(5/3)", sqrt(5 / 3), sd_n1(c(1, 2, 3, 4)))
# fehlende Werte werden nicht ersetzt (0.5 Nr. 3): 1, NA, 3: Mittel 2, SD sqrt((1 + 1)/1) = sqrt(2)
fall("G01c Mittel von 1 NA 3 = 2", 2, mittel(c(1, NA, 3)))
fall("G01d SD von 1 NA 3 = sqrt(2)", sqrt(2), sd_n1(c(1, NA, 3)))
# zu wenige Werte (0.5 Nr. 13): SD bei n = 1 fehlend, Mittel bei n = 0 fehlend
fall("G01e SD bei n = 1 fehlend", NA_real_, sd_n1(5))
fall("G01f Mittel bei n = 0 fehlend", NA_real_, mittel(numeric(0)))
# konstante Werte: SD 0
fall("G01g SD von 3 3 3 = 0", 0, sd_n1(c(3, 3, 3)))

# G02 Quantil Typ 7 (0.5 Nr. 7): x = 1, 2, 3, 4, n = 4
# p = 0,5: h = 3 · 0,5 + 1 = 2,5, Quantil x2 + 0,5 · (x3 − x2) = 2,5
# p = 0,25: h = 1,75, Quantil 1 + 0,75 · 1 = 1,75
# p = 0,975: h = 3,925, Quantil 3 + 0,925 · 1 = 3,925
# p = 1: h = n, Quantil x4 = 4. n = 1: Quantil = Wert
fall("G02a Median von 1 2 3 4 = 2.5", 2.5, median7(c(1, 2, 3, 4)))
fall("G02b Quantil 0.25 von 1 2 3 4 = 1.75", 1.75, quantil7(c(1, 2, 3, 4), 0.25))
fall("G02c Quantil 0.975 von 1 2 3 4 = 3.925", 3.925, quantil7(c(1, 2, 3, 4), 0.975))
fall("G02d Quantil 1 von 1 2 3 4 = 4", 4, quantil7(c(1, 2, 3, 4), 1))
fall("G02e Quantil 0.3 von 7 = 7", 7, quantil7(7, 0.3))
fall("G02f Quantil 0.025 von 4 3 2 1 (unsortiert) = 1.075", 1.075, quantil7(c(4, 3, 2, 1), 0.025))
fall("G02g Quantil 0.975 wie quantile(type = 7) bei 10 Werten", unname(quantile(c(5, 1, 9, 2, 8, 3, 7, 4, 6, 10), 0.975, type = 7)),
     quantil7(c(5, 1, 9, 2, 8, 3, 7, 4, 6, 10), 0.975))

# G03 Gepoolte SD (0.5 Nr. 2): x1 = 1, 2, 3 (Varianz 1, n1 = 3), x2 = 2, 4, 6, 8 (Varianz 20/3, n2 = 4)
# SD_pool = sqrt((2 · 1 + 3 · 20/3) / 5) = sqrt(22/5)
fall("G03a SD_pool = sqrt(22/5)", sqrt(22 / 5), sd_pool(c(1, 2, 3), c(2, 4, 6, 8)))
fall("G03b SD_pool fehlend bei n2 = 1", NA_real_, sd_pool(c(1, 2, 3), 4))

# G04 Bestwert (S04 Regel 2): Zeiten Minimum, Standweitsprung Maximum, NA ausgelassen, alles NA fehlend
fall("G04a Bestwert Zeit von 1.9 1.7 1.8 = 1.7", 1.7, bestwert(c(1.9, 1.7, 1.8), "Z30"))
fall("G04b Bestwert SBJ von 190 210 205 = 210", 210, bestwert(c(190, 210, 205), "SBJ"))
fall("G04c Bestwert Zeit von NA 1.8 = 1.8", 1.8, bestwert(c(NA, 1.8), "CL"))
fall("G04d Bestwert von NA NA fehlend", NA_real_, bestwert(c(NA_real_, NA_real_), "Z05"))
fall("G04e Gleichstand 1.5 1.5 = 1.5", 1.5, bestwert(c(1.5, 1.5), "Z10"))

# G05 Auslöseprüfung (S02 Regel 2), V_MAX 10, DT_MIN 0
# a) 5 m 1,0 s, 10 m 1,8 s, 30 m 4,5 s: v = 5/1,0 = 5, 5/0,8 = 6,25, 20/2,7 = 7,41: nicht gestört
fall("G05a Lauf 1.0 1.8 4.5 nicht gestört", FALSE, lauf_gestoert(c(5, 10, 30), c(1.0, 1.8, 4.5), 10, 0))
# b) 5 m 1,0 s, 10 m 1,4 s: 5/0,4 = 12,5 > 10: gestört
fall("G05b Lauf 1.0 1.4 4.0 gestört (12.5 m/s)", TRUE, lauf_gestoert(c(5, 10, 30), c(1.0, 1.4, 4.0), 10, 0))
# c) 5 m 1,0 s, 10 m 0,9 s: Δt < 0: gestört
fall("G05c Lauf 1.0 0.9 gestört (dt < 0)", TRUE, lauf_gestoert(c(5, 10), c(1.0, 0.9), 10, 0))
# d) 5 m fehlt, 10 m 1,8 s, 30 m 4,5 s: Abschnitte 0 bis 10 (5,56 m/s) und 10 bis 30 (7,41 m/s): nicht gestört
fall("G05d Lauf ohne 5 m, 1.8 4.5 nicht gestört", FALSE, lauf_gestoert(c(10, 30), c(1.8, 4.5), 10, 0))
# e) 5 m 1,0 s, 10 m 1,0 s: Δt = 0: gestört. f) Reihenfolge der Eingabe unerheblich
fall("G05e Lauf 1.0 1.0 gestört (dt = 0)", TRUE, lauf_gestoert(c(5, 10), c(1.0, 1.0), 10, 0))
fall("G05f Lauf in Reihenfolge 30 5 10 nicht gestört", FALSE, lauf_gestoert(c(30, 5, 10), c(4.5, 1.0, 1.8), 10, 0))
# g) Grenze: genau 10,0 m/s ist nicht gestört (v > 10 verlangt): 5 m in 0,5 s
fall("G05g Lauf mit genau 10 m/s nicht gestört", FALSE, lauf_gestoert(5, 0.5, 10, 0))
# h) leerer Lauf nicht gestört
fall("G05h Lauf ohne gültige Teilzeit nicht gestört", FALSE, lauf_gestoert(numeric(0), numeric(0), 10, 0))

# G06 Dubletten- und Sammelmeldungspaare (S06 Regel 9), Abstand 300 s
zeit <- as.POSIXct(c("2026-07-20 10:00:00", "2026-07-20 10:05:00", "2026-07-20 10:10:01",
                     "2026-07-20 10:03:00", "2026-07-20 10:00:00"), format = "%Y-%m-%d %H:%M:%S", tz = "UTC")
code <- c("A", "A", "A", "A", "B")
inhalt <- c("x", "x", "x", "y", "x")
# Paare desselben Codes A: (1,2) 300 s identisch = Dublette, (1,3) 601 s = nichts,
# (1,4) 180 s abweichend = Sammelmeldung, (2,3) 301 s = nichts, (2,4) 120 s abweichend = Sammelmeldung,
# (3,4) 421 s = nichts. Code B nur mit A: nichts. Also 1 Dublette, 2 Sammelmeldungen.
pz <- paare_zaehlen(code, zeit, inhalt, 300)
fall("G06a Dublettenpaare = 1", 1L, pz$n_dubl)
fall("G06b Sammelmeldungspaare = 2", 2L, pz$n_samm)
fall("G06c Kennzeichnung Dublette je Meldung = 1 1 0 0 0", c(1L, 1L, 0L, 0L, 0L), pz$dublette)
fall("G06d Kennzeichnung Sammelmeldung je Meldung = 1 1 0 1 0", c(1L, 1L, 0L, 1L, 0L), pz$sammel)
fall("G06e eine Meldung: keine Paare", c(0L, 0L), c(paare_zaehlen("A", zeit[1], "x", 300)$n_dubl, paare_zaehlen("A", zeit[1], "x", 300)$n_samm))

# G07 Adhärenzzählungen (S07 Regel 1 bis 4), Deckel 2
# Meldungen: W1 ganz (E1), W1 ganz (E1 doppelt), W1 ganz (E2), W2 ganz (E3), W2 teilweise (E4), W3 gar nicht (E5)
st <- c("GANZ", "GANZ", "GANZ", "GANZ", "TEILW", "GARN")
wo <- c("W1", "W1", "W1", "W2", "W2", "W3")
h3 <- c(1L, 1L, 2L, 3L, 4L, 5L)
# NMELD 6, GANZ 4, GT 5, WOCAP min(2,3) + min(2,1) = 3, DIST der ganz-Meldungen: 1, 2, 3 = 3
za <- adhaerenz_zaehlung(st, wo, h3, 2)
fall("G07a NMELD = 6", 6L, za$NMELD)
fall("G07b GANZ = 4", 4L, za$GANZ)
fall("G07c GT = 5", 5L, za$GT)
fall("G07d WOCAP = 3", 3L, za$WOCAP)
fall("G07e DIST = 3", 3L, za$DIST)
za0 <- adhaerenz_zaehlung(character(0), character(0), integer(0), 2)
fall("G07f ohne Meldung alles 0", c(0L, 0L, 0L, 0L, 0L), c(za0$NMELD, za0$GANZ, za0$GT, za0$WOCAP, za0$DIST))

# G08 Interpolation der Khamis-Roche-Koeffizienten (S05 Regel 6), Raster 0,5
ko <- data.frame(alter_jahre = c(14.0, 14.5, 15.0), beta0 = c(-6, -5, -4), stature_in = c(0.6, 0.7, 0.8),
                 weight_lb = c(-0.001, -0.002, -0.003), midparent_in = c(0.5, 0.4, 0.3))
# Alter 14,5 genau auf der Zeile: w = 0, Zeile 14,5. Alter 14,7: a_lo 14,5, w = 0,4,
# beta0 = 0,6 · (−5) + 0,4 · (−4) = −4,6, stature 0,6 · 0,7 + 0,4 · 0,8 = 0,74,
# weight 0,6 · (−0,002) + 0,4 · (−0,003) = −0,0024, midparent 0,6 · 0,4 + 0,4 · 0,3 = 0,36
ip1 <- interpoliere_kr(ko, 14.5, 0.5)
fall("G08a Alter 14.5 auf der Zeile: w = 0", 0, ip1$w)
fall("G08b Alter 14.5 Koeffizienten der Zeile", c(-5, 0.7, -0.002, 0.4), ip1$beta)
ip2 <- interpoliere_kr(ko, 14.7, 0.5)
fall("G08c Alter 14.7: a_lo = 14.5, w = 0.4", c(14.5, 0.4), c(ip2$a_lo, ip2$w))
fall("G08d Alter 14.7 interpoliert", c(-4.6, 0.74, -0.0024, 0.36), ip2$beta)
# Vorhersage (S05 Regel 7) mit einfachen Zahlen: 1 + 2 · 3 + 4 · 5 + 6 · 7 = 69
fall("G08e Vorhersage 1 + 2·3 + 4·5 + 6·7 = 69", 69, khamis_roche_pas(1, 2, 4, 6, 3, 5, 7))
erwarte_abbruch("G08f Alter 15.2 über der Tabelle: Abbruch", interpoliere_kr(ko, 15.2, 0.5))

# G09 Kleinste Quadrate (Teil E): x = 1, 2, 3, y = 1, 3, 2
# Steigung 0,5, Achsenabschnitt 1, Residuen −0,5, 1, −0,5, SSE 1,5, df 1, sigma sqrt(1,5),
# SE Steigung sigma / sqrt(2) = sqrt(0,75), R² = 1 − 1,5/2 = 0,25
fit <- kq_schaetzung(cbind(1, c(1, 2, 3)), c(1, 3, 2))
fall("G09a Koeffizienten 1 und 0.5", c(1, 0.5), fit$koef)
fall("G09b Residuen -0.5 1 -0.5", c(-0.5, 1, -0.5), fit$resid)
fall("G09c sigma = sqrt(1.5), df = 1", c(sqrt(1.5), 1), c(fit$sigma, fit$df))
fall("G09d SE Steigung = sqrt(0.75)", sqrt(0.75), fit$se[2])
fall("G09e R² = 0.25", 0.25, fit$r2)
# exakte Gerade y = 1 + 2x: Residuen 0, sigma 0
fit2 <- kq_schaetzung(cbind(1, c(1, 2, 3, 4)), c(3, 5, 7, 9))
fall("G09f exakte Gerade: Koeffizienten 1 und 2, sigma 0", c(1, 2, 0), c(fit2$koef, fit2$sigma))
# Rangdefekt: doppelte Spalte (0.5 Nr. 11)
fit3 <- kq_schaetzung(cbind(1, c(1, 2, 3, 4), c(2, 4, 6, 8)), c(3, 5, 7, 9))
fall("G09g doppelte Spalte: kein voller Rang", FALSE, fit3$rang_voll)
# konstante Gruppenspalte (alle 1): kollinear mit dem Achsenabschnitt
fit4 <- kq_schaetzung(cbind(1, c(1, 1, 1, 1), c(1, 2, 3, 4)), c(3, 5, 7, 9))
fall("G09h konstante Gruppe: kein voller Rang", FALSE, fit4$rang_voll)
# n <= p: kein Modell
fit5 <- kq_schaetzung(cbind(1, c(1, 2)), c(1, 2))
fall("G09i n = p: kein voller Rang", FALSE, fit5$rang_voll)
# Inferenz: t = 0,5 / sqrt(0,75), p zweiseitig mit df 1, KI mit t_1(0,975)
ki <- koef_inferenz(fit, 2, 0.95)
fall("G09j t = 0.5/sqrt(0.75)", 0.5 / sqrt(0.75), ki$t)
fall("G09k p = 2·(1 − T_1(|t|))", 2 * (1 - pt(0.5 / sqrt(0.75), 1)), ki$p)
fall("G09l KI = b ± t_1(0.975)·SE", c(0.5 - qt(0.975, 1) * sqrt(0.75), 0.5 + qt(0.975, 1) * sqrt(0.75)), c(ki$kiu, ki$kio))

# G10 Varianzanalyse und Brown-Forsythe (S14 Regel 2): Gruppen 1, 2, 3 und 2, 4, 6
# Mittel 2 und 4, Gesamt 3, SS zwischen 3 · 1 + 3 · 1 = 6, SS innerhalb 2 + 8 = 10, df 1 und 4, F = 6 / 2,5 = 2,4
av <- anova_einfach(c(1, 2, 3, 2, 4, 6), c(1, 1, 1, 2, 2, 2))
fall("G10a ANOVA F = 2.4, df 1 und 4", c(2.4, 1, 4), c(av$F, av$df1, av$df2))
fall("G10b ANOVA SS zwischen 6, SS innerhalb 10", c(6, 10), c(av$ss_zw, av$ss_in))
fall("G10c ANOVA p = 1 − F_1,4(2.4)", 1 - pf(2.4, 1, 4), av$p)
# Brown-Forsythe: Mediane 2 und 4, z = 1, 0, 1 und 2, 0, 2, Mittel 2/3 und 4/3, Gesamt 1,
# SS zwischen 3 · 1/9 + 3 · 1/9 = 2/3, SS innerhalb 6/9 + 24/9 = 10/3, F = (2/3) / (10/12) = 0,8
bf <- brown_forsythe(c(1, 2, 3, 2, 4, 6), c(1, 1, 1, 2, 2, 2))
fall("G10d Brown-Forsythe F = 0.8", 0.8, bf$F)
# gleiche Streuung in beiden Gruppen: z identisch, SS zwischen 0, F = 0
fall("G10e Brown-Forsythe bei gleichen Gruppen 1 2 3 und 1 2 3: F = 0", 0, brown_forsythe(c(1, 2, 3, 1, 2, 3), c(1, 1, 1, 2, 2, 2))$F)
fall("G10f Brown-Forsythe df1 = 1, df2 = 4", c(1, 4), c(bf$df1, bf$df2))

# G11 Typischer Messfehler (S10 Regel 1): Spieler A 1, 3 (Mittel 2, SS 2, df 1), B 2, 2, 5 (Mittel 3, SS 6, df 2),
# C 7 (k = 1, nicht in der TE-Menge). TE = sqrt(8/3), df 3, n 2, Mittel aller Versuche der TE-Menge 13/5
te <- te_gepoolt(list(A = c(1, 3), B = c(2, 2, 5), C = 7))
fall("G11a TE = sqrt(8/3)", sqrt(8 / 3), te$te)
fall("G11b df_TE = 3, n = 2", c(3L, 2L), c(te$df, te$n))
fall("G11c Mittel aller Versuche der TE-Menge = 2.6", 2.6, te$mittel_alle)
te0 <- te_gepoolt(list(C = 7))
fall("G11d leere TE-Menge: TE fehlend, df 0, n 0", c(NA_real_, 0, 0), c(te0$te, te0$df, te0$n))
# KI-Grenzen (S10 Regel 3) für TE = 2, df = 3: 2 · sqrt(3 / χ²_3(0,975)) und 2 · sqrt(3 / χ²_3(0,025))
fall("G11e KI-Grenze unten = 2·sqrt(3/chi2_3(0.975))", 2 * sqrt(3 / qchisq(0.975, 3)), 2 * sqrt(3 / chi2_quantil(0.975, 3)))

# G12 Korrekturfaktor J (S15 Regel 2): df 18: 1 − 3/71
fall("G12a J bei df 18 = 1 − 3/71", 1 - 3 / 71, faktor_j(18))
# Zwei-Gruppen-Vergleich (S15 Regel 4): 1, 2, 3 gegen 2, 4, 6: d = −2, SD_pool = sqrt((2·1 + 2·4)/4) = sqrt(2,5),
# SE = sqrt(2,5) · sqrt(2/3), df 4
zg <- zwei_gruppen(c(1, 2, 3), c(2, 4, 6))
fall("G12b Differenz −2, SD_pool sqrt(2.5), df 4", c(-2, sqrt(2.5), 4), c(zg$d, zg$sd_pool, zg$df))
fall("G12c SE = sqrt(2.5)·sqrt(2/3)", sqrt(2.5) * sqrt(2 / 3), zg$se)
fall("G12d konstante Gruppen: t fehlend", NA_real_, zwei_gruppen(c(1, 1), c(2, 2))$t)

# G13 Überlappung (S12 Regel 2): IG 1, 5 und KG 3, 8: L = 3, U = 5, IG darin 1 (5), KG darin 1 (3)
ov <- ueberlappung(c(1, 5), c(3, 8))
fall("G13a Überlappung L 3, U 5, IG 1, KG 1", c(3, 5, 1, 1), c(ov$L, ov$U, ov$n_ig, ov$n_kg))
ov2 <- ueberlappung(c(1, 2), c(3, 4))
fall("G13b disjunkt: L 3 > U 2, beide 0", c(3, 2, 0, 0), c(ov2$L, ov2$U, ov2$n_ig, ov2$n_kg))
ov3 <- ueberlappung(c(2, 2, 6), c(2, 6))
fall("G13c Grenzen eingeschlossen: IG 3, KG 2", c(3, 2), c(ov3$n_ig, ov3$n_kg))

# G14 Power (S18): λ = 0 ergibt Power = α, Power steigt mit λ
fall("G14a Power bei lambda 0 = 0.05", 0.05, power_f(1, 20, 0, 0.05), tol = 1e-9)
fall("G14b Power steigt mit lambda", TRUE, power_f(1, 20, 4, 0.05) > power_f(1, 20, 2, 0.05))
fall("G14c F_krit(1, 20, 0.05) = qf(0.95, 1, 20)", qf(0.95, 1, 20), f_krit(1, 20, 0.05))

# G15 Formatierung der Ausgabe (G.1 Nr. 3): mindestens zwölf signifikante Stellen, Anzahlen ganzzahlig
fall("G15a 1/3 mit 17 Stellen", "0.33333333333333331", formatiere_wert(1 / 3, "zahl"))
fall("G15a2 1.05 mit 17 Stellen einschließlich Nullen", "1.0500000000000000", formatiere_wert(1.05, "zahl"))
fall("G15b Anzahl 3 als 3", "3", formatiere_wert(3, "anzahl"))
fall("G15c Merkmal 1 als 1", "1", formatiere_wert(1, "merkmal"))
fall("G15d fehlend als leer", "", formatiere_wert(NA_real_, "zahl"))
fall("G15e Rücklesen von 0.1 + 0.2 ohne Verlust", 0.1 + 0.2, as.numeric(formatiere_wert(0.1 + 0.2, "zahl")), tol = 0)
erwarte_abbruch("G15f Anzahl 2.5: Abbruch", formatiere_wert(2.5, "anzahl"))
erwarte_abbruch("G15g Merkmal 2: Abbruch", formatiere_wert(2, "merkmal"))

# G16 Strenges Einlesen (0.5 Nr. 10): Zahl, leer, Text, Dezimalkomma
fall("G16a '1.5' und '' ergeben 1.5 und NA", c(1.5, NA), als_zahl(c("1.5", ""), "Test"))
erwarte_abbruch("G16b 'abc': Abbruch", als_zahl("abc", "Test"))
erwarte_abbruch("G16c '1,5' (Dezimalkomma): Abbruch", als_zahl("1,5", "Test"))
erwarte_abbruch("G16d Ganzzahl 4 außerhalb 1 bis 3: Abbruch", als_ganzzahl("4", "Test", zulaessig = 1:3))
erwarte_abbruch("G16e leere Ganzzahl ohne Erlaubnis: Abbruch", als_ganzzahl("", "Test"))
erwarte_abbruch("G16f unbekannte Kategorie: Abbruch", pruefe_kategorie("D", "Test", c("A", "B", "C")))

# G17 Ergebnisregister (G.1 Nr. 4): fehlender Wert ohne zulässigen Grund und doppelte Kennung
reg <- register_neu("Test")
setze(reg, "S00.A.X.X.X.X", 1, "zahl")
erwarte_abbruch("G17a fehlend ohne Grund: Abbruch", setze(reg, "S00.B.X.X.X.X", NA_real_, "zahl", ""))
erwarte_abbruch("G17b fehlend mit unzulässigem Grund: Abbruch", setze(reg, "S00.C.X.X.X.X", NA_real_, "zahl", "unbekannt"))
erwarte_abbruch("G17c doppelte Kennung: Abbruch", setze(reg, "S00.A.X.X.X.X", 2, "zahl"))
setze(reg, "S00.D.X.X.X.X", NA_real_, "zahl", "Eingang fehlt")
fall("G17d fehlend mit Grund: Wert leer, Grund gesetzt", c("", "Eingang fehlt"), c(reg$wert[2], reg$grund[2]))

# G18 SHA-256 in reinem R gegen das Systemwerkzeug sha256sum (Gegenprobe ohne Werte aus dem Gedächtnis)
for (f in c("Versuchsdaten.csv", "Personendaten.csv", "Fragebogen_A.csv", "Zuordnung_Fragebogen.csv",
            "Listenplatz_IG.csv", "Datenwoerterbuch.md", "Pruefsummen.txt")) {
  pfad <- pfad_datenstand(f)
  sys <- system2("sha256sum", shQuote(pfad), stdout = TRUE)
  sys <- sub("\\s.*$", "", sys)
  fall(paste0("G18 SHA-256 von ", f, " wie sha256sum"), sys, sha256_datei(pfad))
}
# Auffüllgrenzen: Texte der Länge 55, 56, 64 Byte
for (L in c(0, 55, 56, 63, 64, 65)) {
  txt <- strrep("a", L)
  tf <- tempfile()
  writeBin(charToRaw(txt), tf)
  sys <- sub("\\s.*$", "", system2("sha256sum", shQuote(tf), stdout = TRUE))
  fall(paste0("G18 SHA-256 von 'a' x ", L, " wie sha256sum"), sys, sha256_text(txt))
  unlink(tf)
}

# G19 Bestwert-Bias (S11): x1 = 2,0, x2 = 1,9, x3 = 1,8 (Zeit): best(1,2,3) − best(1,2) = 1,8 − 1,9 = −0,1
fall("G19a Bias Zeit 2.0 1.9 1.8 = -0.1", -0.1, bestwert(c(2.0, 1.9, 1.8), "Z30") - bestwert(c(2.0, 1.9), "Z30"))
fall("G19b Bias SBJ 200 210 205 = 0", 0, bestwert(c(200, 210, 205), "SBJ") - bestwert(c(200, 210), "SBJ"))

# G20 Günstige Richtung (0.5 Nr. 5)
fall("G20a Zeit: b1 < 0 günstig", c(TRUE, FALSE), c(guenstig(-0.1, "Z30"), guenstig(0.1, "CM")))
fall("G20b SBJ: b1 > 0 günstig", c(TRUE, FALSE), c(guenstig(3, "SBJ"), guenstig(-3, "SBJ")))

cat("\nGrenzfälle: Fall, Soll, Ist, bestanden\n")
cat("---------------------------------------------------------------------\n")
for (i in seq_len(nrow(faelle))) {
  cat(sprintf("%-62s Soll %-32s Ist %-32s %d\n", faelle$Fall[i], faelle$Soll[i], faelle$Ist[i], faelle$bestanden[i]))
}
cat("---------------------------------------------------------------------\n")
cat("Fälle gesamt: ", nrow(faelle), ", bestanden: ", sum(faelle$bestanden), ", nicht bestanden: ",
    sum(faelle$bestanden == 0), "\n", sep = "")
write.csv(faelle, pfad_zwischen("Grenzfaelle_ergebnis.csv"), row.names = FALSE, fileEncoding = "UTF-8")
pruefe(all(faelle$bestanden == 1), "Mindestens ein Grenzfall nicht bestanden. Die Auswertung hält an.")
cat("Alle Grenzfälle bestanden.\n")
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

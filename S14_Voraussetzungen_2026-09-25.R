# =====================================================================
# S14_Voraussetzungen_2026-09-25.R
# Zweck: Voraussetzungen der Modelle aus S13 prüfen und berichten (O7): Shapiro-Wilk
#        der Residuen (K18) mit Q-Q-Diagramm (N1), Brown-Forsythe der Residuen
#        nach Gruppe (K19) mit Residuen-SD je Gruppe (N2), Steigungshomogenität in
#        zwei Modellen (K20), Linearitätsgrafiken (K21), Überlappung der Kovariaten,
#        Vorab-Prüfung an den Prä-Werten in der Menge BPAH (P5).
# Schritt der Spezifikation: S14 (Teil E), Grafiken nach G.1 Nr. 6
# Eingangsdateien (SHA-256):
#   Zwischen/S01_daten.rds, S04_aggregat.rds, S05_pah.rds, S08_sets.rds, S13_modelle.rds
#   Spezifikation_2026-09-24_Konstanten.csv
#     6eec0094230e13ca52896f8e0828a55fafffcc9fa52f9c7620368f1bddad4329
#   Spezifikation_2026-09-24_Kennungen.csv
#     90bb105ffb13417882c8bcd59cd80b5f021ce6e430f25435f9760f1ab8c78dfe
# Fassung: 2026-09-25, erste Fassung.
# Aufruf: Rscript S14_Voraussetzungen_2026-09-25.R
# Ausgabe: S14_Voraussetzungen_2026-09-25.txt, S14_QQ_<ZIEL>.png, S14_Linearitaet_<ZIEL>.png,
#          Zwischen/S14_ergebnisse.rds
# Rückfrage R4 (Rückfragenprotokoll): Fallzahlregel in BPAH für Shapiro-Wilk je Gruppe.
#   Lesart (a), geklärt am 2026-09-25 (Rückfragenprotokoll), gesetzt in LESART_R4.
# =====================================================================

source(file.path(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])),
                 "Funktionen_2026-09-25.R"))

withCallingHandlers({

# Lesart der Rückfrage R4: "a" Fallzahlregel für beide Vorab-Prüfungen, "b" nur für das Prä-Modell
LESART_R4 <- "a"

daten <- lies_zwischen("S01_daten.rds")
agg <- lies_zwischen("S04_aggregat.rds")
pah <- lies_zwischen("S05_pah.rds")
sets <- lies_zwischen("S08_sets.rds")
m13 <- lies_zwischen("S13_modelle.rds")
schreibe_kopf(
  zweck = "Voraussetzungen der Hauptanalyse",
  schritt = "S14",
  eingang = c(daten$pruefsummen,
              "Spezifikation_2026-09-24_Konstanten.csv" = unname(ANLAGEN["_Konstanten.csv"]),
              "Spezifikation_2026-09-24_Kennungen.csv" = unname(ANLAGEN["_Kennungen.csv"]))
)
konst <- lies_konstanten()
kenn <- lies_kennungen()
pruefe(LESART_R4 %in% c("a", "b"), "Rückfrage R4 (Fallzahlregel in BPAH für Shapiro-Wilk) ist offen. Lesart nicht gesetzt.")
cat("\nLesart R4: ", LESART_R4, "\n", sep = "")
ALPHA <- konstante_zahl(konst, "ALPHA")
KI <- konstante_zahl(konst, "KI_NIVEAU")
N_MIN <- sets$N_MIN
gruppe <- sets$gruppe
codes <- daten$spieler$ALLE

verworfen <- function(p) as.integer(!is.na(p) && p < ALPHA)
farbe <- function(g) ifelse(g == 1, "black", "grey55")
symbol <- function(g) ifelse(g == 1, 16, 1)

reg <- register_neu("S14_Voraussetzungen_2026-09-25.R")
for (z in ZIELE_KONF) {
  m <- m13$modelle[[z]]
  d <- m$daten
  fit <- m$fit
  suf <- paste0(".", z, ".X.ITT.HAUPT")
  gerechnet <- m$inf == 1 && !is.null(fit) && isTRUE(fit$rang_voll)
  grund <- if (m$inf == 0) GRUND_FALLZAHL else if (!gerechnet) GRUND_RANG else ""
  cat("\nZielgröße ", z, ": INF = ", m$inf, if (gerechnet) ", Prüfungen gerechnet" else paste0(", nicht gerechnet (", grund, ")"), "\n", sep = "")
  if (!gerechnet) {
    for (nm in c("SWW", "SWP", "BFF", "BFP", "SDRIG", "SDRKG", "SDRQ")) setze(reg, paste0("S14.", nm, suf), NA_real_, "zahl", grund)
    for (nm in c("BFDF1", "BFDF2")) setze(reg, paste0("S14.", nm, suf), NA_real_, "anzahl", grund)
    for (nm in c("SWVERW", "BFVERW")) setze(reg, paste0("S14.", nm, suf), NA_real_, "merkmal", grund)
    for (mod in c("SLPRE", "SLPAH")) {
      s2 <- paste0(".", z, ".X.ITT.", mod)
      for (nm in c("BINT", "SEINT", "TINT", "PINT")) setze(reg, paste0("S14.", nm, s2), NA_real_, "zahl", grund)
      setze(reg, paste0("S14.DFINT", s2), NA_real_, "anzahl", grund)
      setze(reg, paste0("S14.VERW", s2), NA_real_, "merkmal", grund)
    }
    for (nm in c("OVPREIG", "OVPREKG", "OVPAHIG", "OVPAHKG")) setze(reg, paste0("S14.", nm, suf), NA_real_, "anzahl", grund)
    for (nm in c("OVPRL", "OVPRU", "OVPAL", "OVPAU")) setze(reg, paste0("S14.", nm, suf), NA_real_, "zahl", grund)
  } else {
    e <- fit$resid
    # Regel 1: Shapiro-Wilk der Residuen und Q-Q-Diagramm
    sw <- shapiro_wilk(e)
    setze(reg, paste0("S14.SWW", suf), sw$W, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S14.SWP", suf), sw$p, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S14.SWVERW", suf), verworfen(sw$p), "merkmal")
    png(pfad_abgabe(paste0("S14_QQ_", z, ".png")), width = 900, height = 900, res = 150, type = "cairo")
    qq <- qqnorm(e, plot.it = FALSE)
    plot(qq$x, qq$y, col = farbe(d$G), pch = symbol(d$G), xlab = "Theoretische Quantile",
         ylab = "Residuen", main = paste0("Normal-Q-Q-Diagramm der Residuen, ", z, " (ITT, HAUPT)"))
    qqline(e)
    legend("topleft", legend = c("IG", "KG"), col = c("black", "grey55"), pch = c(16, 1), bty = "n")
    dev.off()
    # Regel 2: Brown-Forsythe und Residuen-SD je Gruppe
    bf <- brown_forsythe(e, d$G)
    setze(reg, paste0("S14.BFF", suf), bf$F, "zahl")
    setze(reg, paste0("S14.BFDF1", suf), bf$df1, "anzahl")
    setze(reg, paste0("S14.BFDF2", suf), bf$df2, "anzahl")
    setze(reg, paste0("S14.BFP", suf), bf$p, "zahl")
    setze(reg, paste0("S14.BFVERW", suf), verworfen(bf$p), "merkmal")
    sd_ig <- sd_n1(e[d$G == 1])
    sd_kg <- sd_n1(e[d$G == 0])
    setze(reg, paste0("S14.SDRIG", suf), sd_ig, "zahl", GRUND_ZU_WENIG)
    setze(reg, paste0("S14.SDRKG", suf), sd_kg, "zahl", GRUND_ZU_WENIG)
    if (is.na(sd_ig) || is.na(sd_kg)) setze(reg, paste0("S14.SDRQ", suf), NA_real_, "zahl", GRUND_ZU_WENIG)
    else if (sd_ig == 0) setze(reg, paste0("S14.SDRQ", suf), NA_real_, "zahl", GRUND_KONSTANT)
    else setze(reg, paste0("S14.SDRQ", suf), sd_kg / sd_ig, "zahl")
    # Regel 3: Steigungshomogenität in zwei getrennten Modellen
    for (mod in c("SLPRE", "SLPAH")) {
      s2 <- paste0(".", z, ".X.ITT.", mod)
      inter <- if (mod == "SLPRE") d$G * d$Pre else d$G * d$PAH
      X <- cbind(1, d$G, d$Pre, d$PAH, inter)
      f2 <- kq_schaetzung(X, d$Post)
      if (!f2$rang_voll) {
        for (nm in c("BINT", "SEINT", "TINT", "PINT")) setze(reg, paste0("S14.", nm, s2), NA_real_, "zahl", GRUND_RANG)
        setze(reg, paste0("S14.DFINT", s2), NA_real_, "anzahl", GRUND_RANG)
        setze(reg, paste0("S14.VERW", s2), NA_real_, "merkmal", GRUND_RANG)
      } else {
        ki <- koef_inferenz(f2, 5, KI)
        setze(reg, paste0("S14.BINT", s2), ki$b, "zahl")
        setze(reg, paste0("S14.SEINT", s2), ki$se, "zahl")
        setze(reg, paste0("S14.TINT", s2), ki$t, "zahl")
        setze(reg, paste0("S14.DFINT", s2), ki$df, "anzahl")
        setze(reg, paste0("S14.PINT", s2), ki$p, "zahl")
        setze(reg, paste0("S14.VERW", s2), verworfen(ki$p), "merkmal")
      }
    }
    # Regel 4: Linearität grafisch
    png(pfad_abgabe(paste0("S14_Linearitaet_", z, ".png")), width = 1800, height = 650, res = 150, type = "cairo")
    par(mfrow = c(1, 3), mar = c(4.5, 4.5, 3, 1))
    for (k in 1:3) {
      xw <- list(fit$fitted, d$Pre, d$PAH)[[k]]
      xl <- c("Vorhersage", "Prä-Wert (BEST)", "%PAH")[k]
      plot(xw, e, col = farbe(d$G), pch = symbol(d$G), xlab = xl, ylab = "Residuen",
           main = paste0("Residuen gegen ", xl, ", ", z))
      abline(h = 0, lty = 2)
      if (k == 1) legend("topleft", legend = c("IG", "KG"), col = c("black", "grey55"), pch = c(16, 1), bty = "n")
    }
    dev.off()
    # Regel 5: Überlappung der Kovariaten (S12 Regel 2)
    for (kov in c("PRE", "PAH")) {
      x <- if (kov == "PRE") d$Pre else d$PAH
      ov <- ueberlappung(x[d$G == 1], x[d$G == 0])
      L <- ov$L
      U <- ov$U
      n_i <- ov$n_ig
      n_k <- ov$n_kg
      nm_ig <- if (kov == "PRE") "OVPREIG" else "OVPAHIG"
      nm_kg <- if (kov == "PRE") "OVPREKG" else "OVPAHKG"
      nm_l <- if (kov == "PRE") "OVPRL" else "OVPAL"
      nm_u <- if (kov == "PRE") "OVPRU" else "OVPAU"
      setze(reg, paste0("S14.", nm_ig, suf), n_i, "anzahl")
      setze(reg, paste0("S14.", nm_kg, suf), n_k, "anzahl")
      setze(reg, paste0("S14.", nm_l, suf), L, "zahl")
      setze(reg, paste0("S14.", nm_u, suf), U, "zahl")
    }
    cat("  Grafiken geschrieben: S14_QQ_", z, ".png, S14_Linearitaet_", z, ".png\n", sep = "")
  }
  # Regel 6: Vorab-Prüfung in der Menge BPAH (Spieler mit BEST prä und %PAH)
  a_pre <- agg[agg$Ziel == z & agg$ZeitKenn == "PRE", ]
  b_pre <- a_pre$BEST[match(codes, a_pre$Code)]
  pah_w <- pah$PAH[match(codes, pah$Code)]
  bpah <- codes[!is.na(b_pre) & !is.na(pah_w)]
  db <- data.frame(Code = bpah, G = as.numeric(gruppe[bpah] == "IG"), Pre = b_pre[match(bpah, codes)],
                   PAH = pah_w[match(bpah, codes)], stringsAsFactors = FALSE)
  n_ig <- sum(db$G == 1)
  n_kg <- sum(db$G == 0)
  inf_b <- as.integer(n_ig >= N_MIN && n_kg >= N_MIN)
  cat("  Menge BPAH: n_IG = ", n_ig, ", n_KG = ", n_kg, ", Fallzahlregel erfüllt: ", inf_b, "\n", sep = "")
  s3 <- paste0(".", z, ".PRE.BPAH.SLPAH")
  if (inf_b == 0) {
    for (nm in c("CINT", "SECINT", "TCINT", "PCINT")) setze(reg, paste0("S14.", nm, s3), NA_real_, "zahl", GRUND_FALLZAHL)
    setze(reg, paste0("S14.DFCINT", s3), NA_real_, "anzahl", GRUND_FALLZAHL)
  } else {
    X <- cbind(1, db$G, db$PAH, db$G * db$PAH)
    f3 <- kq_schaetzung(X, db$Pre)
    if (!f3$rang_voll) {
      for (nm in c("CINT", "SECINT", "TCINT", "PCINT")) setze(reg, paste0("S14.", nm, s3), NA_real_, "zahl", GRUND_RANG)
      setze(reg, paste0("S14.DFCINT", s3), NA_real_, "anzahl", GRUND_RANG)
    } else {
      ki <- koef_inferenz(f3, 4, KI)
      setze(reg, paste0("S14.CINT", s3), ki$b, "zahl")
      setze(reg, paste0("S14.SECINT", s3), ki$se, "zahl")
      setze(reg, paste0("S14.TCINT", s3), ki$t, "zahl")
      setze(reg, paste0("S14.DFCINT", s3), ki$df, "anzahl")
      setze(reg, paste0("S14.PCINT", s3), ki$p, "zahl")
    }
  }
  for (g in c("IG", "KG")) {
    x <- db$Pre[db$G == as.numeric(g == "IG")]
    s4 <- paste0(".", z, ".PRE.BPAH", g, ".X")
    if (LESART_R4 == "a" && inf_b == 0) {
      setze(reg, paste0("S14.SWW", s4), NA_real_, "zahl", GRUND_FALLZAHL)
      setze(reg, paste0("S14.SWP", s4), NA_real_, "zahl", GRUND_FALLZAHL)
    } else {
      sw <- shapiro_wilk(x)
      setze(reg, paste0("S14.SWW", s4), sw$W, "zahl", GRUND_ZU_WENIG)
      setze(reg, paste0("S14.SWP", s4), sw$p, "zahl", GRUND_ZU_WENIG)
    }
  }
}
register_pruefe_vollstaendig(reg, erwartete_kennungen(kenn, "S14", daten$spieler))
register_speichere(reg, "S14")
register_drucke(reg)
cat("Ende: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S UTC"), "\n", sep = "")

}, warning = merke_warnung)

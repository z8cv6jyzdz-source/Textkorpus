# =====================================================================
# Objekte_2026-09-25.R
# Zweck: Tabellen und Abbildungen des Manuskripts aus der Ergebnisdatei der berichteten
#        Rechnung erzeugen (Auswertungsverfahren 2026-09-24, Schritt 7.2, Maßnahme L19).
#        Fünf Objekte im Textteil (Tab. 1 bis 3, Abb. 1 und 2) und Anhang H (Tab. H1 bis H5)
#        nach Auswertungs_und_Berichtsumfang_2026-09-24 § 3.2, § 3.5 und § 3.7. Jede Zelle
#        stammt aus einer Kennung der Ergebnisdatei, keine Zahl von Hand. Rundung und
#        Zahlenformat nach § 3.7 (Dezimalkomma, typografisches Minus, Vorzeichen bei
#        Differenzen und Konfidenzgrenzen, Intervalle mit „bis“).
# Eingang: Ergebnisdatei nach Spezifikation G.1 (Ergebnisse_R_2026-09-25.csv der zweiten
#        Instanz, SHA-256 3194a805…, oder eine synthetische Datei im selben Format zur Probe).
# Ausgabe (im Ausgabeordner): je Tabelle eine CSV mit formatierten Zellen (Trennzeichen Komma,
#        UTF-8), Objekte_2026-09-25.md mit allen Tabellen und Anmerkungen, Abb_1_Teilnehmerfluss
#        und Abb_2_Modell als PNG (300 dpi) und PDF, Objekte_2026-09-25.txt als Laufprotokoll.
# Aufruf: Rscript Objekte_2026-09-25.R <Ergebnisdatei.csv> <Ausgabeordner> [synthetisch]
# Fassung: 2026-09-25, dritte Fassung (Tab. 2 ohne die Kennwertzeilen Alter, Körperhöhe, Körpermasse und %PAH, die im Methodikteil 4.2 stehen,
#          Verfasserentscheidung per Klick 25.09.2026). Zweite Fassung: angefragte Vereine eingesetzt, Abb. H7 Zeitstrahl ergänzt. Nur base R (wie die berichtete Rechnung).
# Clusterebene von Abb. 1: vier angefragte Vereine, drei Zusagen (Angabe des Verfassers 25.09.2026, Kennzahlenblatt K-01.24).
# Abb. H7 (Zeitstrahl der Termine) aus den Terminkonstanten des Kennzahlenblatts K-03 (nicht aus der Ergebnisdatei).
# =====================================================================

invisible(Sys.setlocale("LC_CTYPE", "C.UTF-8"))   # Umlaute und Sonderzeichen in Grafiken und Dateien, wie LC_ALL=C.UTF-8 der zweiten Instanz
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Aufruf: Rscript Objekte_2026-09-25.R <Ergebnisdatei.csv> <Ausgabeordner> [synthetisch]")
EINGANG <- args[1]
AUS <- args[2]
SYNTH <- length(args) >= 3 && args[3] == "synthetisch"
dir.create(AUS, showWarnings = FALSE, recursive = TRUE)
ANGEFRAGT <- 4L   # Zahl der angefragten Vereine (Clusterebene Abb. 1), Angabe des Verfassers vom 25.09.2026 (K-01.24)
ZUGESAGT <- 3L    # Vereine A, B, C

# ---------------------------------------------------------------- Eingang
sha256 <- function(pfad) {
  out <- tryCatch(system2("sha256sum", pfad, stdout = TRUE), error = function(e) NA_character_)
  if (length(out) == 0 || is.na(out[1])) return("nicht ermittelt")
  strsplit(out[1], " ")[[1]][1]
}
SHA <- sha256(EINGANG)
E <- read.csv(EINGANG, colClasses = "character", encoding = "UTF-8", check.names = FALSE)
stopifnot(all(c("Kennung", "Wert", "Einheit", "Grund", "Skript") %in% names(E)))
if (any(duplicated(E$Kennung))) stop("Kennung doppelt in der Ergebnisdatei")
WERT <- suppressWarnings(as.numeric(E$Wert))
names(WERT) <- E$Kennung
GRUND <- E$Grund
names(GRUND) <- E$Kennung
verwendet <- character(0)

w <- function(k) {
  if (!(k %in% names(WERT))) stop(paste("Kennung fehlt in der Ergebnisdatei:", k))
  verwendet <<- c(verwendet, k)
  unname(WERT[k])
}
g <- function(k) unname(GRUND[k])
fehl <- function(k) paste0("fehlend (", g(k), ")")

# ---------------------------------------------------------------- Darstellung (§ 3.7)
MINUS <- "−"
fmt <- function(x, nd, sign = FALSE) {
  if (is.na(x)) return("fehlend")
  s <- sub("\\.", ",", formatC(abs(x), format = "f", digits = nd))
  if (x < 0) return(paste0(MINUS, s))
  if (sign) return(paste0("+", s))
  s
}
fp <- function(p) if (is.na(p)) "fehlend" else if (p < 0.001) "< 0,001" else fmt(p, 3)
ki <- function(u, o, nd, sign = TRUE) if (is.na(u) || is.na(o)) "fehlend" else paste(fmt(u, nd, sign), "bis", fmt(o, nd, sign))
msd <- function(m, s, nd) if (is.na(m) || is.na(s)) "fehlend" else paste(fmt(m, nd), "±", fmt(s, nd))
ZIELE <- c(Z05 = "Sprint 5 m", Z10 = "Sprint 10 m", Z30 = "Sprint 30 m", CL = "505 links", CR = "505 rechts", CM = "505-Seitenmittel", SBJ = "Standweitsprung")
KONF <- c("Z30", "CM", "SBJ")
EINH <- function(z) if (z == "SBJ") "cm" else "s"
NDM <- function(z) if (z == "SBJ") 0 else 2     # M ± SD
NDD <- function(z) if (z == "SBJ") 1 else 3     # Differenzen, KI, TE, SESOI

MD <- character(0)
md <- function(...) MD <<- c(MD, paste0(...))
schreibe_tabelle <- function(name, titel, df, anmerkung = NULL) {
  utils::write.table(df, file.path(AUS, paste0(name, ".csv")), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
  md("*", titel, "*")
  md("")
  md("| ", paste(names(df), collapse = " | "), " |")
  md("|", paste(rep("---", ncol(df)), collapse = "|"), "|")
  for (i in seq_len(nrow(df))) md("| ", paste(unlist(df[i, ]), collapse = " | "), " |")
  md("")
  if (!is.null(anmerkung)) {
    md("Anmerkung. ", anmerkung)
    md("")
  }
}

md("# Objekte des Manuskripts aus der Ergebnisdatei (Phase 7.2)")
md("")
md("Erzeugt von Objekte_2026-09-25.R aus ", basename(EINGANG), " (SHA-256 ", SHA, ")", if (SYNTH) " · SYNTHETISCHE PROBEDATEN, KEINE STUDIENERGEBNISSE" else "", ". Darstellungsregeln nach Auswertungs_und_Berichtsumfang_2026-09-24 § 3.7. Tabellentitel kursiv oberhalb, Kopfzeile grau und fett, Gitternetz beim Setzen in Word (F14 § 9).")
md("")

# ---------------------------------------------------------------- Tab. 1 Messgüte
t1 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE,
  "Zielgröße" = character(0), "n" = character(0), "TE [95-%-KI]" = character(0), "CV (%)" = character(0),
  "SESOI" = character(0), "TE/SESOI" = character(0), "TE post [95-%-KI]" = character(0))
npost <- character(0)
for (z in names(ZIELE)) {
  nd <- NDD(z)
  te <- w(sprintf("S10.TE.%s.PRE.ALL.X", z))
  lo <- w(sprintf("S10.TELO.%s.PRE.ALL.X", z))
  hi <- w(sprintf("S10.TEHI.%s.PRE.ALL.X", z))
  tep <- w(sprintf("S10.TE.%s.POST.ALL.X", z))
  lop <- w(sprintf("S10.TELO.%s.POST.ALL.X", z))
  hip <- w(sprintf("S10.TEHI.%s.POST.ALL.X", z))
  t1[nrow(t1) + 1, ] <- c(paste0(ZIELE[z], " (", EINH(z), ")"), as.character(w(sprintf("S10.NTE.%s.PRE.ALL.X", z))),
    paste0(fmt(te, nd), " [", ki(lo, hi, nd, FALSE), "]"), fmt(w(sprintf("S10.CV.%s.PRE.ALL.X", z)), 1),
    fmt(w(sprintf("S10.SESOI.%s.PRE.ALL.X", z)), nd), fmt(w(sprintf("S10.RTS.%s.PRE.ALL.X", z)), 2),
    paste0(fmt(tep, nd), " [", ki(lop, hip, nd, FALSE), "]"))
  npost <- c(npost, paste0(ZIELE[z], " ", w(sprintf("S10.NTE.%s.POST.ALL.X", z))))
}
schreibe_tabelle("Tab_1_Messguete", "Tab. 1. Messgüte je Zielgröße aus den Wiederholungsversuchen der Eingangstestung (alle Spieler mit mindestens zwei gültigen Versuchen)", t1,
  paste0("TE = typischer Messfehler (gepoolte Innerspieler-SD der gültigen Versuche einer Sitzung), 95-%-KI aus der χ²-Verteilung. CV = 100 · TE / Mittel der Versuche. SESOI = 0,2 · SD der Bestwerte aller Spieler. Seitenmittel aus beidseitig gültigen Versuchsnummern. TE post aus der Abschlusstestung, n post: ", paste(npost, collapse = ", "), "."))

# ---------------------------------------------------------------- Tab. 2 Stichprobe und Ausgangswerte
# Alter, Körperhöhe, Körpermasse und %PAH der Analysepopulation stehen im Methodikteil (4.2), nicht in Tab. 2 (Verfasser 25.09.2026).
t2 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "n IG" = character(0), "M ± SD IG" = character(0),
  "n KG" = character(0), "M ± SD KG" = character(0), "d" = character(0), "Überlappung IG / KG" = character(0))
for (z in names(ZIELE)) {
  ov <- if (z %in% KONF) paste0("Prä ", w(sprintf("S14.OVPREIG.%s.X.ITT.HAUPT", z)), " / ", w(sprintf("S14.OVPREKG.%s.X.ITT.HAUPT", z)), ", %PAH ", w(sprintf("S14.OVPAHIG.%s.X.ITT.HAUPT", z)), " / ", w(sprintf("S14.OVPAHKG.%s.X.ITT.HAUPT", z))) else "–"
  t2[nrow(t2) + 1, ] <- c(paste0(ZIELE[z], " (", EINH(z), ")"), as.character(w(sprintf("S12.N.%s.PRE.ITTIG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.ITTIG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.ITTIG.HAUPT", z)), NDM(z)),
    as.character(w(sprintf("S12.N.%s.PRE.ITTKG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.ITTKG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.ITTKG.HAUPT", z)), NDM(z)), fmt(w(sprintf("S12.D.%s.PRE.ITT.HAUPT", z)), 2, TRUE), ov)
}
schreibe_tabelle("Tab_2_Stichprobe_Ausgangswerte", "Tab. 2. Ausgangswerte je Zielgröße im Analyseset, Mittelwert ± Standardabweichung, ohne Signifikanztests", t2,
  "IG = Interventionsgruppe, KG = Kontrollgruppe. Analyseset je Zielgröße: Spieler mit Prä- und Post-Wert und %PAH. Bestwert der gültigen Versuche, 505 als Mittel der beiden Seiten-Bestwerte. d = (M_IG − M_KG) / gepoolte SD, nur beschreibend. Überlappung = Zahl der Spieler je Gruppe im gemeinsamen Bereich des Ausgangswerts und des %PAH, nur konfirmatorische Zielgrößen.")

# ---------------------------------------------------------------- Tab. 3 Gruppenvergleich
t3 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "n IG / KG" = character(0), "Post M ± SD IG" = character(0), "Post M ± SD KG" = character(0),
  "Differenz unadjustiert [95-%-KI]" = character(0), "Differenz adjustiert [95-%-KI]" = character(0), "p" = character(0), "g [95-%-KI]" = character(0))
sesoi_txt <- character(0)
for (z in KONF) {
  nd <- NDD(z)
  t3[nrow(t3) + 1, ] <- c(paste0(ZIELE[z], " (", EINH(z), ")"), paste0(w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z)), " / ", w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z))),
    msd(w(sprintf("S15.MPOSTIG.%s.X.ITT.HAUPT", z)), w(sprintf("S12.SD.%s.POST.ITTIG.HAUPT", z)), NDM(z)),
    msd(w(sprintf("S15.MPOSTKG.%s.X.ITT.HAUPT", z)), w(sprintf("S12.SD.%s.POST.ITTKG.HAUPT", z)), NDM(z)),
    paste0(fmt(w(sprintf("S15.UD.%s.X.ITT.HAUPT", z)), nd, TRUE), " [", ki(w(sprintf("S15.UDKIU.%s.X.ITT.HAUPT", z)), w(sprintf("S15.UDKIO.%s.X.ITT.HAUPT", z)), nd), "]"),
    paste0(fmt(w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), nd, TRUE), " [", ki(w(sprintf("S13.KIU.%s.X.ITT.HAUPT", z)), w(sprintf("S13.KIO.%s.X.ITT.HAUPT", z)), nd), "]"),
    fp(w(sprintf("S13.P.%s.X.ITT.HAUPT", z))),
    paste0(fmt(w(sprintf("S15.G.%s.X.ITT.HAUPT", z)), 2, TRUE), " [", ki(w(sprintf("S15.GKIU.%s.X.ITT.HAUPT", z)), w(sprintf("S15.GKIO.%s.X.ITT.HAUPT", z)), 2), "]"))
  sesoi_txt <- c(sesoi_txt, paste0(ZIELE[z], " ", fmt(w(sprintf("S10.SESOI.%s.PRE.ALL.X", z)), nd), " ", EINH(z)))
}
schreibe_tabelle("Tab_3_Gruppenvergleich", "Tab. 3. Gruppenvergleich der konfirmatorischen Zielgrößen im Analyseset: unadjustierte und adjustierte Differenz der Abschlusswerte", t3,
  paste0("Differenz IG minus KG, bei Zeiten bedeuten negative Werte eine schnellere IG. Unadjustiert: Differenz der Post-Mittel. Adjustiert: Koeffizient der Gruppe im Modell Post = b0 + b1·Gruppe + b2·Prä + b3·%PAH (ANCOVA, kleinste Quadrate), Analyse in der zugeteilten Gruppe. g = adjustierte Differenz / gepoolte Prä-SD × J (Hedges). SESOI (0,2 · SD der Bestwerte prä): ", paste(sesoi_txt, collapse = ", "), "."))

# ---------------------------------------------------------------- Tab. H1 Versuche, Ausfälle, Messgüte je Verein
h1a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "gültige Versuche prä" = character(0), "gültige Versuche post" = character(0),
  "k̄ prä IG" = character(0), "k̄ prä KG" = character(0), "k̄ post IG" = character(0), "k̄ post KG" = character(0))
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) {
  h1a[nrow(h1a) + 1, ] <- c(ZIELE[z], as.character(w(sprintf("S02.NGUELT.%s.PRE.ALL.X", z))), as.character(w(sprintf("S02.NGUELT.%s.POST.ALL.X", z))),
    fmt(w(sprintf("S09.KMEAN.%s.PRE.IG.X", z)), 2), fmt(w(sprintf("S09.KMEAN.%s.PRE.KG.X", z)), 2), fmt(w(sprintf("S09.KMEAN.%s.POST.IG.X", z)), 2), fmt(w(sprintf("S09.KMEAN.%s.POST.KG.X", z)), 2))
}
schreibe_tabelle("Tab_H1a_Versuche", "Tab. H1a. Gültige Versuche je Zielgröße und Zeitpunkt (alle Spieler) und mittlere Zahl gültiger Versuche je Spieler (k̄) je Gruppe", h1a,
  paste0("Protokollvorgabe drei Versuche je Spieler und Zielgröße. Bezugsmenge je Zeitpunkt: Spieler mit Zeilen zu diesem Zeitpunkt, post ohne die zur Abschlusstestung nicht angetretenen Spieler. Auslösegestörte Sprintläufe prä ", w("S02.NAUSL.X.PRE.ALL.X"), ", post ", w("S02.NAUSL.X.POST.ALL.X"), "."))

KAT <- c(TECH = "technischer Ausfall", ZEIT = "dritter Versuch aus Zeitmangel", FEHL = "Fehlversuch", FALSCH = "falsch aufgenommen", NANG = "nicht angetreten", AUSL = "auslösegestört")
h1b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Zeitpunkt" = character(0),
  "IG technisch" = character(0), "IG Zeitmangel" = character(0), "IG Fehlversuch" = character(0), "IG falsch aufgenommen" = character(0), "IG nicht angetreten" = character(0),
  "KG technisch" = character(0), "KG Zeitmangel" = character(0), "KG Fehlversuch" = character(0), "KG falsch aufgenommen" = character(0), "KG nicht angetreten" = character(0))
ausl_summe <- 0
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) for (t in c("PRE", "POST")) {
  zelle <- c(ZIELE[z], if (t == "PRE") "prä" else "post")
  for (gr in c("IG", "KG")) {
    for (k in c("TECH", "ZEIT", "FEHL", "FALSCH", "NANG")) {
      if (k == "NANG" && t == "PRE") { zelle <- c(zelle, "–") } else zelle <- c(zelle, as.character(w(sprintf("S03.NKAT.%s.%s.%s.%s", z, t, gr, k))))
    }
    ausl_summe <- ausl_summe + w(sprintf("S03.NKAT.%s.%s.%s.AUSL", z, t, gr))
  }
  h1b[nrow(h1b) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H1b_Ausfallmechanismen", "Tab. H1b. Ungültige Versuche je Ausfallmechanismus, Zielgröße, Zeitpunkt und Gruppe", h1b,
  paste0("Jede ungültige Zeile trägt genau eine Kategorie: nicht angetreten (Abschlusstestung ohne den Spieler) vor auslösegestört vor Bemerkungsvokabular. Auslösegestörte Zeilen gesamt: ", ausl_summe, "."))

h1c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "ohne Prä-Wert IG" = character(0), "ohne Prä-Wert KG" = character(0), "ohne Post-Wert IG" = character(0), "ohne Post-Wert KG" = character(0), "Erhebungsanteil IG" = character(0), "Erhebungsanteil KG" = character(0))
for (z in names(ZIELE)) {
  h1c[nrow(h1c) + 1, ] <- c(ZIELE[z], as.character(w(sprintf("S08.FLOPRE.%s.X.IG.X", z))), as.character(w(sprintf("S08.FLOPRE.%s.X.KG.X", z))), as.character(w(sprintf("S08.FLOPOST.%s.X.IG.X", z))), as.character(w(sprintf("S08.FLOPOST.%s.X.KG.X", z))),
    paste0(fmt(100 * w(sprintf("S08.ANT.%s.X.IG.X", z)), 1), " %"), paste0(fmt(100 * w(sprintf("S08.ANT.%s.X.KG.X", z)), 1), " %"))
}
schreibe_tabelle("Tab_H1c_Fehlende_Werte", "Tab. H1c. Fehlende Werte je Zielgröße und Gruppe (Spieler ohne Bestwert) und Erhebungsanteil (Spieler mit Prä- und Post-Wert je zugeteiltem Spieler)", h1c,
  "Gründe werden unabhängig gezählt, ein Spieler kann mehrere haben. Zur Abschlusstestung nicht angetreten zählen unter „ohne Post-Wert“.")

h1d <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "n prä" = character(0), "Δ prä" = character(0), "Δ prä / SESOI" = character(0), "n post" = character(0), "Δ post" = character(0), "Δ post / SESOI" = character(0))
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) {
  nd <- if (z == "SBJ") 2 else 4
  zelle <- ZIELE[z]
  for (t in c("PRE", "POST")) {
    n <- w(sprintf("S11.N.%s.%s.ALL.X", z, t))
    d <- w(sprintf("S11.DMEAN.%s.%s.ALL.X", z, t))
    s <- w(sprintf("S11.DSESOI.%s.%s.ALL.X", z, t))
    zelle <- c(zelle, as.character(n), if (is.na(d)) fehl(sprintf("S11.DMEAN.%s.%s.ALL.X", z, t)) else paste(fmt(d, nd, TRUE), EINH(z)), if (is.na(s)) "–" else fmt(s, 2, TRUE))
  }
  h1d[nrow(h1d) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H1d_Bestwertbias", "Tab. H1d. Bestwert-Bias, gemessen: mittlere Verschiebung des Bestwerts durch den dritten Versuch, Δ = best(V1, V2, V3) − best(V1, V2), Spieler mit drei gültigen Versuchen", h1d,
  "Nur beschreibend. Bei Zeiten ist Δ höchstens null, beim Standweitsprung mindestens null. Δ / SESOI mit dem SESOI desselben Zeitpunkts (post intern aus den Bestwerten post).")

h1e <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Verein A prä" = character(0), "Verein B prä" = character(0), "Verein C prä" = character(0), "Verein A post" = character(0), "Verein B post" = character(0), "Verein C post" = character(0))
for (z in names(ZIELE)) {
  zelle <- ZIELE[z]
  for (t in c("PRE", "POST")) for (v in c("VA", "VB", "VC")) {
    te <- w(sprintf("S10.TE.%s.%s.%s.X", z, t, v))
    zelle <- c(zelle, if (is.na(te)) fehl(sprintf("S10.TE.%s.%s.%s.X", z, t, v)) else paste0(fmt(te, NDD(z)), " (", w(sprintf("S10.NTE.%s.%s.%s.X", z, t, v)), ", df ", w(sprintf("S10.DFTE.%s.%s.%s.X", z, t, v)), ")"))
  }
  h1e[nrow(h1e) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H1e_TE_je_Verein", "Tab. H1e. Typischer Messfehler je Verein und Zeitpunkt (Zahl der Spieler der TE-Menge, Freiheitsgrade)", h1e,
  "TE aus den Wiederholungsversuchen der Spieler mit mindestens zwei gültigen Versuchen, je Verein getrennt, nur beschreibend.")

# ---------------------------------------------------------------- Tab. H2 Umsetzung
ig_codes <- sub("^S07\\.ADH\\.ADH\\.X\\.P(.*)\\.GANZ$", "\\1", grep("^S07\\.ADH\\.ADH\\.X\\.P.*\\.GANZ$", E$Kennung, value = TRUE))
h2a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Code" = character(0), "Meldungen" = character(0), "Einheiten ganz (Hauptzählung)" = character(0), "wochengedeckelt" = character(0), "distinkte Nummern" = character(0))
for (cd in ig_codes) {
  a <- w(sprintf("S07.ADH.ADH.X.P%s.GANZ", cd))
  h2a[nrow(h2a) + 1, ] <- c(cd, as.character(w(sprintf("S06.NMELD.FB.X.P%s.X", cd))),
    if (is.na(a)) fehl(sprintf("S07.ADH.ADH.X.P%s.GANZ", cd)) else as.character(a),
    if (is.na(w(sprintf("S07.ADH.ADH.X.P%s.WOCAP", cd)))) "nicht erhebbar" else as.character(w(sprintf("S07.ADH.ADH.X.P%s.WOCAP", cd))),
    if (is.na(w(sprintf("S07.ADH.ADH.X.P%s.DIST", cd)))) "nicht erhebbar" else as.character(w(sprintf("S07.ADH.ADH.X.P%s.DIST", cd))))
}
schreibe_tabelle("Tab_H2a_Adhaerenz_je_Spieler", "Tab. H2a. Umsetzung je Spieler der Interventionsgruppe: gemeldete Einheiten mit Status „ganz“ (Hauptzählung) und beide Untergrenzen", h2a,
  paste0("Zwölf angebotene Einheiten je Spieler. Wochengedeckelt: höchstens zwei Meldungen „ganz“ je Programmwoche. Distinkte Nummern: verschiedene Einheitennummern unter den Meldungen „ganz“. Spieler ohne Listenplatz im Fragebogen: nicht erhebbar. Summe ganz ", w("S07.SUMME.ADH.X.IG.GANZ"), " von ", 12 * w("S07.NZUG.ADH.X.IG.X"), " (", fmt(100 * w("S07.RATE.ADH.X.IG.GANZ"), 1), " %), ganz oder teilweise ", w("S07.SUMME.ADH.X.IG.GT"), " (", fmt(100 * w("S07.RATE.ADH.X.IG.GT"), 1), " %), wochengedeckelt ", w("S07.SUMME.ADH.X.IG.WOCAP"), " (", fmt(100 * w("S07.RATE.ADH.X.IG.WOCAP"), 1), " %), distinkt ", w("S07.SUMME.ADH.X.IG.DIST"), " (", fmt(100 * w("S07.RATE.ADH.X.IG.DIST"), 1), " %). Median ", fmt(w("S07.MED.ADH.X.IG.GANZ"), 1), ", Mittel ", fmt(w("S07.MITT.ADH.X.IG.GANZ"), 2), " Einheiten je zugeteiltem Spieler."))

h2b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Programmwoche" = character(0), "Wochenanteil ganz" = character(0), "CR-10: n" = character(0), "CR-10: M ± SD" = character(0), "sRPE-Load (AU): n" = character(0), "sRPE-Load: M ± SD" = character(0))
for (wk in 1:6) {
  cn <- w(sprintf("S07.N.CR10.W%d.IG.GANZ", wk))
  cm <- w(sprintf("S07.M.CR10.W%d.IG.GANZ", wk))
  cs <- w(sprintf("S07.SD.CR10.W%d.IG.GANZ", wk))
  ln <- w(sprintf("S07.N.LOAD.W%d.IG.GANZ", wk))
  lm <- w(sprintf("S07.M.LOAD.W%d.IG.GANZ", wk))
  ls <- w(sprintf("S07.SD.LOAD.W%d.IG.GANZ", wk))
  h2b[nrow(h2b) + 1, ] <- c(paste0("W", wk), paste0(fmt(100 * w(sprintf("S07.ANTW.ADH.W%d.IG.GANZ", wk)), 1), " %"), as.character(cn), if (is.na(cm)) fehl(sprintf("S07.M.CR10.W%d.IG.GANZ", wk)) else if (is.na(cs)) fmt(cm, 1) else msd(cm, cs, 1),
    as.character(ln), if (is.na(lm)) fehl(sprintf("S07.M.LOAD.W%d.IG.GANZ", wk)) else if (is.na(ls)) fmt(lm, 1) else msd(lm, ls, 1))
}
schreibe_tabelle("Tab_H2b_Wochenverlauf", "Tab. H2b. Verlauf je Programmwoche: Wochenanteil der Meldungen „ganz“ (Meldungen / (2 · zugeteilte Spieler)), Anstrengung CR-10 und sRPE-Load der Meldungen „ganz“", h2b,
  paste0("sRPE-Load = CR-10 mal Solldauer der Programmwoche (Wochen- und Aufwärmvideo), keine individuell gemessene Dauer. Über alle Wochen: CR-10 n ", w("S07.N.CR10.X.IG.GANZ"), ", ", msd(w("S07.M.CR10.X.IG.GANZ"), w("S07.SD.CR10.X.IG.GANZ"), 1), ", Median ", fmt(w("S07.MED.CR10.X.IG.GANZ"), 1), ", Min ", fmt(w("S07.MIN.CR10.X.IG.GANZ"), 1), ", Max ", fmt(w("S07.MAX.CR10.X.IG.GANZ"), 1), ". Load n ", w("S07.N.LOAD.X.IG.GANZ"), ", ", msd(w("S07.M.LOAD.X.IG.GANZ"), w("S07.SD.LOAD.X.IG.GANZ"), 1), " AU, Median ", fmt(w("S07.MED.LOAD.X.IG.GANZ"), 1), ", Min ", fmt(w("S07.MIN.LOAD.X.IG.GANZ"), 1), ", Max ", fmt(w("S07.MAX.LOAD.X.IG.GANZ"), 1), "."))

ak_codes <- unique(sub("^S16\\.DIFF\\.[A-Z0-9]+\\.DIFF\\.P(.*)\\.AK9$", "\\1", grep("^S16\\.DIFF\\..*\\.AK9$", E$Kennung, value = TRUE)))
h2c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Code" = character(0), "Δ Sprint 30 m (s)" = character(0), "Δ 505-Seitenmittel (s)" = character(0), "Δ Standweitsprung (cm)" = character(0))
for (cd in ak_codes) {
  zelle <- cd
  for (z in KONF) {
    d <- w(sprintf("S16.DIFF.%s.DIFF.P%s.AK9", z, cd))
    zelle <- c(zelle, if (is.na(d)) fehl(sprintf("S16.DIFF.%s.DIFF.P%s.AK9", z, cd)) else fmt(d, NDD(z), TRUE))
  }
  h2c[nrow(h2c) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H2c_Antragskriterium", "Tab. H2c. Antragskriterium (mindestens 9 von 12 Einheiten „ganz“): Veränderung Post − Prä der Bestwerte je Spieler, nur Einzelwerte", h2c,
  "Kein Test und keine Effektstärke, weil die Teilmenge unter acht Spielern liegt.")

# ---------------------------------------------------------------- Tab. H3 Ausgangswerte aller Eingangsgetesteten, deskriptive Zielgrößen
h3a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "n IG" = character(0), "M ± SD IG" = character(0), "n KG" = character(0), "M ± SD KG" = character(0), "d" = character(0))
for (z in names(ZIELE)) {
  h3a[nrow(h3a) + 1, ] <- c(paste0(ZIELE[z], " (", EINH(z), ")"), as.character(w(sprintf("S12.N.%s.PRE.IG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.IG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.IG.HAUPT", z)), NDM(z)),
    as.character(w(sprintf("S12.N.%s.PRE.KG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.KG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.KG.HAUPT", z)), NDM(z)), fmt(w(sprintf("S12.D.%s.PRE.BASE.HAUPT", z)), 2, TRUE))
}
schreibe_tabelle("Tab_H3a_Ausgangswerte_alle", "Tab. H3a. Ausgangswerte aller eingangsgetesteten Spieler mit Bestwert je Zielgröße (Vergleich mit dem Analyseset in Tab. 2)", h3a,
  "d = (M_IG − M_KG) / gepoolte SD, nur beschreibend, keine Signifikanztests.")
h3b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "prä IG" = character(0), "prä KG" = character(0), "post IG" = character(0), "post KG" = character(0))
for (z in c("Z05", "Z10", "CL", "CR")) {
  zelle <- paste0(ZIELE[z], " (", EINH(z), ")")
  for (t in c("PRE", "POST")) for (gr in c("ITTIG", "ITTKG")) zelle <- c(zelle, paste0(msd(w(sprintf("S12.M.%s.%s.%s.HAUPT", z, t, gr)), w(sprintf("S12.SD.%s.%s.%s.HAUPT", z, t, gr)), NDM(z)), " (n = ", w(sprintf("S12.N.%s.%s.%s.HAUPT", z, t, gr)), ")"))
  h3b[nrow(h3b) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H3b_Deskriptive_Zielgroessen", "Tab. H3b. Deskriptive Zielgrößen im Analyseset, Bestwerte prä und post je Gruppe (keine Modelle, Fallzahlregel)", h3b,
  "Sprint 5 m und 10 m sowie 505 je Seite werden nur beschrieben. Beim 10-m-Sprint fiel bei der Eingangstestung von Verein B die Lichtschranke aus.")

# ---------------------------------------------------------------- Tab. H4 Modell und Robustheit
h4a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "b0 (SE)" = character(0), "b1 Gruppe (SE)" = character(0), "b2 Prä (SE)" = character(0), "b3 %PAH (SE)" = character(0), "Residuen-SD" = character(0), "R²" = character(0), "adj. Mittel IG [95-%-KI]" = character(0), "adj. Mittel KG [95-%-KI]" = character(0))
for (z in KONF) {
  nd <- NDD(z)
  ndk <- if (z == "SBJ") 2 else 3
  nda <- if (z == "SBJ") 0 else 3
  k <- function(x) w(sprintf("S13.%s.%s.X.ITT.HAUPT", x, z))
  h4a[nrow(h4a) + 1, ] <- c(paste0(ZIELE[z], " (", EINH(z), ")"), paste0(fmt(k("B0"), ndk), " (", fmt(k("SEB0"), ndk), ")"), paste0(fmt(k("B1"), nd, TRUE), " (", fmt(k("SEB1"), nd), ")"),
    paste0(fmt(k("B2"), 3), " (", fmt(k("SEB2"), 3), ")"), paste0(fmt(k("B3"), ndk, TRUE), " (", fmt(k("SEB3"), ndk), ")"), fmt(k("SIGMA"), nd), fmt(k("R2"), 2),
    paste0(fmt(k("AMIG"), nda), " [", ki(k("AMIGU"), k("AMIGO"), nda, FALSE), "]"), paste0(fmt(k("AMKG"), nda), " [", ki(k("AMKGU"), k("AMKGO"), nda, FALSE), "]"))
}
schreibe_tabelle("Tab_H4a_Modellkennwerte", "Tab. H4a. Modellkennwerte der ANCOVA im Analyseset und adjustierte Mittelwerte am Mittel der Kovariaten des Sets", h4a,
  paste0("Modell Post = b0 + b1·Gruppe + b2·Prä + b3·%PAH. df = n − 4. Adjustierte Mittelwerte bei Prä-Mittel und %PAH-Mittel des Analysesets: ", paste(sapply(KONF, function(z) paste0(ZIELE[z], " ", fmt(w(sprintf("S13.PREM.%s.X.ITT.HAUPT", z)), NDD(z)), " ", EINH(z), " und ", fmt(w(sprintf("S13.PAHM.%s.X.ITT.HAUPT", z)), 2), " %")), collapse = ", "), "."))

h4b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Shapiro-Wilk der Residuen" = character(0), "Brown-Forsythe" = character(0), "Residuen-SD IG / KG (KG/IG)" = character(0), "Gruppe × Prä" = character(0), "Gruppe × %PAH" = character(0), "Vorab: Gruppe × %PAH im Prä-Modell" = character(0))
for (z in KONF) {
  nd <- NDD(z)
  k <- function(x, v = "HAUPT") w(sprintf("S14.%s.%s.X.ITT.%s", x, z, v))
  verw <- function(f) if (!is.na(f) && f == 1) ", verworfen" else ""
  vorab <- w(sprintf("S14.CINT.%s.PRE.BPAH.SLPAH", z))
  h4b[nrow(h4b) + 1, ] <- c(ZIELE[z], paste0("W = ", fmt(k("SWW"), 3), ", p = ", fp(k("SWP")), verw(k("SWVERW"))),
    paste0("F(", k("BFDF1"), ", ", k("BFDF2"), ") = ", fmt(k("BFF"), 2), ", p = ", fp(k("BFP")), verw(k("BFVERW"))),
    paste0(fmt(k("SDRIG"), nd), " / ", fmt(k("SDRKG"), nd), " (", fmt(k("SDRQ"), 2), ")"),
    paste0("b = ", fmt(k("BINT", "SLPRE"), 3, TRUE), ", t(", k("DFINT", "SLPRE"), ") = ", fmt(k("TINT", "SLPRE"), 2), ", p = ", fp(k("PINT", "SLPRE")), verw(k("VERW", "SLPRE"))),
    paste0("b = ", fmt(k("BINT", "SLPAH"), 4, TRUE), ", t(", k("DFINT", "SLPAH"), ") = ", fmt(k("TINT", "SLPAH"), 2), ", p = ", fp(k("PINT", "SLPAH")), verw(k("VERW", "SLPAH"))),
    if (is.na(vorab)) fehl(sprintf("S14.CINT.%s.PRE.BPAH.SLPAH", z)) else paste0("c3 = ", fmt(vorab, 4, TRUE), ", t(", w(sprintf("S14.DFCINT.%s.PRE.BPAH.SLPAH", z)), ") = ", fmt(w(sprintf("S14.TCINT.%s.PRE.BPAH.SLPAH", z)), 2), ", p = ", fp(w(sprintf("S14.PCINT.%s.PRE.BPAH.SLPAH", z)))))
}
schreibe_tabelle("Tab_H4b_Voraussetzungen", "Tab. H4b. Voraussetzungsprüfungen der ANCOVA je Zielgröße (Regel O7: berichtet, Verfahren bleibt) und Vorab-Prüfung an den Ausgangswerten", h4b,
  paste0("Shapiro-Wilk auf allen Residuen des Modells, Brown-Forsythe (Levene mit Median) auf den Residuen nach Gruppe, Steigungshomogenität in zwei getrennten Modellen mit je einem Interaktionsterm (df = n − 5). Vorab-Prüfung an den Prä-Werten in der Menge mit Ausgangswert und %PAH (df = n − 4), sie beschreibt die Ausgangslage und ist keine ANCOVA-Voraussetzung. Shapiro-Wilk der Prä-Werte je Gruppe in derselben Menge: ", paste(sapply(KONF, function(z) paste0(ZIELE[z], " IG W = ", fmt(w(sprintf("S14.SWW.%s.PRE.BPAHIG.X", z)), 3), " (p = ", fp(w(sprintf("S14.SWP.%s.PRE.BPAHIG.X", z))), "), KG W = ", fmt(w(sprintf("S14.SWW.%s.PRE.BPAHKG.X", z)), 3), " (p = ", fp(w(sprintf("S14.SWP.%s.PRE.BPAHKG.X", z))), ")")), collapse = " · "), "."))

VAR <- list(c("PP6", "Per-Protokoll ≥ 6 von 12 Einheiten", "S16", "PP6", "HAUPT"), c("MW", "Mittelwert der Versuche statt Bestwert", "S17", "ITT", "MW"),
            c("PP5", "Per-Protokoll ≥ 5", "S17", "PP5", "HAUPT"), c("PP7", "Per-Protokoll ≥ 7", "S17", "PP7", "HAUPT"),
            c("AEND", "Änderungswertmodell (Δ = Post − Prä, mit %PAH)", "S17", "ITT", "AEND"), c("OPAH", "Modell ohne %PAH", "S17", "ITT", "OPAH"),
            c("FAMB", "Familiarisierung als dritte Kovariate", "S17", "FAMS", "FAMB"), c("BOOT", "Bootstrap-Perzentil-KI der Hauptanalyse (B = 10 000)", "S19", "ITT", "BOOT"))
h4c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Variante" = character(0), "Zielgröße" = character(0), "n IG / KG" = character(0), "adjustierte Differenz [95-%-KI]" = character(0), "p" = character(0))
for (v in VAR) for (z in KONF) {
  nd <- NDD(z)
  if (v[1] == "BOOT") {
    h4c[nrow(h4c) + 1, ] <- c(v[2], ZIELE[z], paste0(w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z)), " / ", w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z))),
      paste0(fmt(w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), nd, TRUE), " [", ki(w(sprintf("S19.BKIU.%s.X.ITT.BOOT", z)), w(sprintf("S19.BKIO.%s.X.ITT.BOOT", z)), nd), "]"), "–")
  } else {
    b1 <- w(sprintf("%s.B1.%s.X.%s.%s", v[3], z, v[4], v[5]))
    h4c[nrow(h4c) + 1, ] <- c(v[2], ZIELE[z], paste0(w(sprintf("%s.NIG.%s.X.%s.%s", v[3], z, v[4], v[5])), " / ", w(sprintf("%s.NKG.%s.X.%s.%s", v[3], z, v[4], v[5]))),
      if (is.na(b1)) paste0("keine Inferenz (", g(sprintf("%s.B1.%s.X.%s.%s", v[3], z, v[4], v[5])), ")") else paste0(fmt(b1, nd, TRUE), " [", ki(w(sprintf("%s.KIU.%s.X.%s.%s", v[3], z, v[4], v[5])), w(sprintf("%s.KIO.%s.X.%s.%s", v[3], z, v[4], v[5])), nd), "]"),
      if (is.na(b1)) "–" else fp(w(sprintf("%s.P.%s.X.%s.%s", v[3], z, v[4], v[5]))))
  }
}
schreibe_tabelle("Tab_H4c_Varianten", "Tab. H4c. Per-Protokoll-Vergleich, vorab festgelegte Sensitivitätsanalysen und Bootstrap-Konfidenzintervall: adjustierte Gruppendifferenz je Variante", h4c,
  "Adjustierte Differenz IG minus KG wie in Tab. 3. Unter acht Spielern je Gruppe keine Inferenz (Fallzahlregel), dann Deskription in Tab. H4d. Per-Protokoll-Vergleiche sind beobachtend und nicht randomisiert. Bootstrap: Schichtung nach Gruppe, Startwert 20260924, nachträglich festgelegt.")

h4d <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Menge" = character(0), "Zielgröße" = character(0), "n IG" = character(0), "IG prä M ± SD" = character(0), "IG post M ± SD" = character(0))
for (s in list(c("PP5", "S17", "PP5IG", "HAUPT"), c("PP6", "S16", "PP6IG", "HAUPT"), c("PP7", "S17", "PP7IG", "HAUPT"))) for (z in KONF) {
  h4d[nrow(h4d) + 1, ] <- c(paste0("Per-Protokoll ≥ ", substr(s[1], 3, 3)), ZIELE[z], as.character(w(sprintf("S08.N.%s.X.%sIG.X", z, s[1]))),
    msd(w(sprintf("%s.M.%s.PRE.%s.%s", s[2], z, s[3], s[4])), w(sprintf("%s.SD.%s.PRE.%s.%s", s[2], z, s[3], s[4])), NDM(z)), msd(w(sprintf("%s.M.%s.POST.%s.%s", s[2], z, s[3], s[4])), w(sprintf("%s.SD.%s.POST.%s.%s", s[2], z, s[3], s[4])), NDM(z)))
}
for (z in KONF) for (gr in c("IG", "KG")) {
  h4d[nrow(h4d) + 1, ] <- c(paste0("Familiarisierungsset ", gr), ZIELE[z], as.character(w(sprintf("S08.N.%s.X.FAMS%s.X", z, gr))),
    msd(w(sprintf("S17.M.%s.PRE.FAMS%s.FAMB", z, gr)), w(sprintf("S17.SD.%s.PRE.FAMS%s.FAMB", z, gr)), NDM(z)), msd(w(sprintf("S17.M.%s.POST.FAMS%s.FAMB", z, gr)), w(sprintf("S17.SD.%s.POST.FAMS%s.FAMB", z, gr)), NDM(z)))
}
schreibe_tabelle("Tab_H4d_Deskription_Teilmengen", "Tab. H4d. Beschreibung der Per-Protokoll-Teilmengen (IG) und des Familiarisierungssets: Bestwerte prä und post", h4d,
  "Der KG-Teil der Per-Protokoll-Mengen ist der KG-Teil des Analysesets (Tab. 2, Tab. 3). Spalte n IG: Spieler der Interventionsgruppe in der Menge, beim Familiarisierungsset die Zahl der jeweiligen Gruppe.")

h4e <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "IG, ein Termin" = character(0), "IG, zwei Termine" = character(0), "KG, ein Termin" = character(0), "KG, zwei Termine" = character(0))
for (z in KONF) {
  zelle <- ZIELE[z]
  for (gr in c("ITTIG", "ITTKG")) for (f in c("F1", "F2")) {
    n <- w(sprintf("S17.N.%s.DIFF.%s.%s", z, gr, f))
    m <- w(sprintf("S17.M.%s.DIFF.%s.%s", z, gr, f))
    s <- w(sprintf("S17.SD.%s.DIFF.%s.%s", z, gr, f))
    zelle <- c(zelle, paste0("n = ", n, if (is.na(m)) "" else paste0(": ", fmt(m, NDD(z), TRUE), if (is.na(s)) "" else paste0(" ± ", fmt(s, NDD(z))))))
  }
  h4e[nrow(h4e) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H4e_Familiarisierung_Variante_a", "Tab. H4e. Familiarisierung, Variante a (nur beschreibend): Veränderung Post − Prä der Bestwerte im Analyseset nach Gruppe und Zahl der Familiarisierungstermine", h4e,
  "In der IG ist die Zahl der Termine mit Verein A konfundiert (dort stand nur ein Termin zur Verfügung). Keine Inferenz.")

# ---------------------------------------------------------------- Tab. H5 Schwellenlandschaft
h5 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Einheiten „ganz“" = as.character(0:12),
  "Spieler mit genau dieser Zahl" = sapply(0:12, function(i) as.character(w(sprintf("S07.V%02d.ADH.X.IG.GANZ", i)))),
  "Spieler mit mindestens dieser Zahl" = c(as.character(w("S07.NZUG.ADH.X.IG.X")), sapply(1:12, function(i) as.character(w(sprintf("S07.GE%02d.ADH.X.IG.GANZ", i))))))
schreibe_tabelle("Tab_H5_Schwellenlandschaft", "Tab. H5. Schwellenlandschaft der Mindestdosis: Verteilung der vollständig gemeldeten Einheiten über die zugeteilten Spieler der Interventionsgruppe", h5,
  paste0("Zeile 0 der Spalte „mindestens“ = zugeteilte Spieler. Spieler mit mindestens einer Meldung gleich welchen Status: ", w("S07.NMELDSP.ADH.X.IG.X"), ". Untergrenzen: wochengedeckelt ≥ 6: ", w("S07.GE06.ADH.X.IG.WOCAP"), ", ≥ 9: ", w("S07.GE09.ADH.X.IG.WOCAP"), ", distinkte Nummern ≥ 6: ", w("S07.GE06.ADH.X.IG.DIST"), ", ≥ 9: ", w("S07.GE09.ADH.X.IG.DIST"), "."))

# ---------------------------------------------------------------- Abb. 1 Teilnehmerfluss
zeichne_abb1 <- function() {
  par(mar = c(0.2, 0.2, 0.2, 0.2), family = "sans", xpd = NA)
  plot.new()
  plot.window(xlim = c(0, 100), ylim = c(0, 100))
  box_ <- function(x, y, wdt, hgt, txt, fill = "grey95", cex = 0.62) {
    rect(x - wdt / 2, y - hgt / 2, x + wdt / 2, y + hgt / 2, col = fill, border = "grey20", lwd = 0.8)
    text(x, y, txt, cex = cex)
  }
  pfeil <- function(x0, y0, x1, y1) arrows(x0, y0, x1, y1, length = 0.05, lwd = 0.8, col = "grey20")
  nA <- w("S01.N.X.X.VA.X")
  nB <- w("S01.N.X.X.VB.X")
  nC <- w("S01.N.X.X.VC.X")
  angefragt <- as.character(ANGEFRAGT)
  L <- 26
  Rr <- 74
  B <- 46
  box_(50, 93, 70, 9, paste0("Vereine angefragt: n = ", angefragt, ", ohne Zusage: n = ", ANGEFRAGT - ZUGESAGT, "\nZusagen: ", ZUGESAGT, " Vereine (A, B, C), Zuteilung auf Vereinsebene vor der Eingangstestung"), "grey85")
  pfeil(38, 88.5, L + 4, 84.5)
  pfeil(62, 88.5, Rr - 4, 84.5)
  box_(L, 78, B, 12, paste0("Interventionsgruppe\nVerein A (n = ", nA, ") und Verein B (n = ", nB, ")\nzugeteilt und eingangsgetestet: n = ", w("S01.N.X.X.IG.X")), "grey90")
  box_(Rr, 78, B, 12, paste0("Kontrollgruppe (Warteliste)\nVerein C (n = ", nC, ")\nzugeteilt und eingangsgetestet: n = ", w("S01.N.X.X.KG.X")), "grey90")
  pfeil(L, 72, L, 68)
  pfeil(Rr, 72, Rr, 68)
  box_(L, 60, B, 15, paste0("Intervention erhalten: n = ", w("S07.GE01.ADH.X.IG.GANZ"), "\n(mindestens eine vollständig gemeldete Einheit)\nohne Meldung: n = ", w("S08.B6NEKM.X.X.IG.X"), "\nohne Listenplatz im Fragebogen: n = ", w("S08.B6IF.X.X.IG.X")))
  box_(Rr, 60, B, 15, "Wartelistenbedingung\n(Vereinsprogramm, kein Monitoring)")
  pfeil(L, 52.5, L, 48)
  pfeil(Rr, 52.5, Rr, 48)
  box_(L, 42, B, 11, paste0("Abschlusstestung nicht angetreten: n = ", w("S08.FLNANG.X.X.IG.X"), "\nohne %PAH: n = ", w("S08.FLOPAH.PAH.X.IG.X")))
  box_(Rr, 42, B, 11, paste0("Abschlusstestung nicht angetreten: n = ", w("S08.FLNANG.X.X.KG.X"), "\nohne %PAH (fehlende Anthropometrie): n = ", w("S08.FLOPAH.PAH.X.KG.X")))
  pfeil(L, 36.5, L, 30.5)
  pfeil(Rr, 36.5, Rr, 30.5)
  nenner <- function(gr) paste(sapply(KONF, function(z) paste0(sub("Sprint ", "", ZIELE[z]), " ", w(sprintf("S08.N.%s.X.ITT%s.X", z, gr)))), collapse = ", ")
  box_(L, 22, B, 16, paste0("Analysiert (Analysepopulation): n = ", w("S12.N.AGE.PRE.ANAIG.X"), "\nje Zielgröße:\n", nenner("IG"), "\nPer-Protokoll (mindestens 6 Einheiten): ", paste(sapply(KONF, function(z) w(sprintf("S08.N.%s.X.PP6IG.X", z))), collapse = ", ")), "grey90")
  box_(Rr, 22, B, 16, paste0("Analysiert (Analysepopulation): n = ", w("S12.N.AGE.PRE.ANAKG.X"), "\nje Zielgröße:\n", nenner("KG")), "grey90")
  text(50, 6, "Analyse in der zugeteilten Gruppe, je Zielgröße mit vollständigen Prä- und Post-Werten und Reifestatus (%PAH),\nohne Ersetzung fehlender Werte. Nenner der deskriptiven Zielgrößen in Tab. 2 und Tab. H3.", cex = 0.55)
}
png(file.path(AUS, "Abb_1_Teilnehmerfluss.png"), width = 16, height = 12, units = "cm", res = 300, type = "cairo")
zeichne_abb1()
dev.off()
cairo_pdf(file.path(AUS, "Abb_1_Teilnehmerfluss.pdf"), width = 16 / 2.54, height = 12 / 2.54, family = "sans")
zeichne_abb1()
dev.off()

# ---------------------------------------------------------------- Abb. 2 Ausgangswerte und reifeadjustierte Abschlusswerte
codes <- sub("^S05\\.PAH\\.PAH\\.PRE\\.P(.*)\\.X$", "\\1", grep("^S05\\.PAH\\.PAH\\.PRE\\.P", E$Kennung, value = TRUE))
gruppe_von <- function(cd) if (substr(cd, 1, 2) %in% c("HL", "BW")) 1 else 0   # S01 Regel 3: Vereine A und B sind die IG
zeichne_abb2 <- function() {
  par(mfrow = c(1, 3), mar = c(4.2, 4.2, 1.2, 0.8), family = "sans", mgp = c(2.6, 0.7, 0), las = 1)
  for (z in KONF) {
    nd <- NDD(z)
    itt <- codes[sapply(codes, function(cd) w(sprintf("S08.MITGL.%s.X.P%s.ITT", z, cd)) == 1)]
    pre <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.PRE.P%s.X", z, cd)))
    post <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.POST.P%s.X", z, cd)))
    pah <- sapply(itt, function(cd) w(sprintf("S05.PAH.PAH.PRE.P%s.X", cd)))
    G <- sapply(itt, gruppe_von)
    ok <- !is.na(pre) & !is.na(post) & !is.na(pah)   # im Analyseset immer erfüllt, Schutz für Probedaten
    pre <- pre[ok]
    post <- post[ok]
    pah <- pah[ok]
    G <- G[ok]
    b0 <- w(sprintf("S13.B0.%s.X.ITT.HAUPT", z))
    b1 <- w(sprintf("S13.B1.%s.X.ITT.HAUPT", z))
    b2 <- w(sprintf("S13.B2.%s.X.ITT.HAUPT", z))
    b3 <- w(sprintf("S13.B3.%s.X.ITT.HAUPT", z))
    pahm <- w(sprintf("S13.PAHM.%s.X.ITT.HAUPT", z))
    if (any(is.na(c(b0, b1, b2, b3, pahm))) || sum(G == 1) < 2 || sum(G == 0) < 2) {
      plot.new()
      text(0.5, 0.5, paste(ZIELE[z], "\nkein Modell (Fallzahlregel)"))
      next
    }
    yadj <- post - b3 * (pah - pahm)
    xl <- range(pre)
    yl <- range(yadj)
    xl <- xl + c(-1, 1) * 0.06 * diff(xl)
    yl <- yl + c(-1, 1) * 0.08 * diff(yl)
    plot(pre, yadj, type = "n", xlim = xl, ylim = yl, xlab = paste0("Ausgangswert (", EINH(z), ")"), ylab = paste0("Abschlusswert, adjustiert (", EINH(z), ")"), main = ZIELE[z], cex.main = 0.95, font.main = 1, cex.lab = 0.9, cex.axis = 0.85)
    for (gr in c(1, 0)) {
      sel <- G == gr
      xr <- range(pre[sel])
      lines(xr, b0 + b1 * gr + b2 * xr + b3 * pahm, lty = if (gr == 1) 1 else 2, lwd = 1.4, col = if (gr == 1) "black" else "grey45")
      points(pre[sel], yadj[sel], pch = if (gr == 1) 16 else 1, col = if (gr == 1) "black" else "grey30", cex = 0.95)
      xm <- mean(pre[sel])
      points(xm, b0 + b1 * gr + b2 * xm + b3 * pahm, pch = if (gr == 1) 15 else 0, cex = 1.6, col = if (gr == 1) "black" else "grey30", lwd = 1.3)
    }
    legend("topleft", legend = c("IG Spieler", "KG Spieler", "IG Modell", "KG Modell", "Gruppenmittel IG", "Gruppenmittel KG"), pch = c(16, 1, NA, NA, 15, 0), lty = c(NA, NA, 1, 2, NA, NA), col = c("black", "grey30", "black", "grey45", "black", "grey30"), pt.cex = c(0.95, 0.95, 1, 1, 1.3, 1.3), cex = 0.62, bty = "n")
  }
}
png(file.path(AUS, "Abb_2_Modell.png"), width = 16, height = 6.5, units = "cm", res = 300, type = "cairo")
zeichne_abb2()
dev.off()
cairo_pdf(file.path(AUS, "Abb_2_Modell.pdf"), width = 16 / 2.54, height = 6.5 / 2.54, family = "sans")
zeichne_abb2()
dev.off()
md("*Abb. 1.* Teilnehmerfluss auf Cluster- und Spielerebene (Abb_1_Teilnehmerfluss.png/.pdf). Clusterebene nach Angabe des Verfassers (K-01.24), Spielerebene aus der Ergebnisdatei.")
md("")
md("*Abb. 2.* Ausgangswert und reifeadjustierter Abschlusswert je Spieler (Post − b3·(%PAH − Mittel des Sets)) mit den Modelllinien je Gruppe über den beobachteten Bereich der Ausgangswerte und den Gruppenmitteln (Quadrate), konfirmatorische Zielgrößen im Analyseset (Abb_2_Modell.png/.pdf). Nach dem Muster von Vickers und Altman (2001), erweitert um die zweite Kovariate.")
md("")

# ---------------------------------------------------------------- Abb. H7 Zeitstrahl der Termine (Anhang H)
# Termine je Verein aus dem Kennzahlenblatt K-03 (Personendaten des Datenstands, nicht aus der Ergebnisdatei),
# Programmzeitraum W1 bis W6 aus den Konstanten der Spezifikation. Familiarisierungstermine liegen nicht als Datum vor.
TERMINE <- data.frame(verein = c("Verein A (IG)", "Verein B (IG)", "Verein C (KG)"),
                      prae = as.Date(c("2026-07-02", "2026-07-14", "2026-07-13")),
                      post = as.Date(c("2026-09-10", "2026-09-01", "2026-09-14")),
                      ig = c(TRUE, TRUE, FALSE), stringsAsFactors = FALSE)
PROGRAMM <- as.Date(c("2026-07-20", "2026-08-30"))
zeichne_h7 <- function() {
  par(mar = c(2.6, 6.2, 1.2, 0.6), family = "sans", mgp = c(1.6, 0.45, 0), tcl = -0.25)
  x0 <- as.Date("2026-06-28")
  x1 <- as.Date("2026-09-20")
  plot(NA, xlim = c(x0, x1), ylim = c(0.4, 3.6), xaxt = "n", yaxt = "n", xlab = "", ylab = "", bty = "n")
  ticks <- seq(as.Date("2026-07-01"), as.Date("2026-09-15"), by = "2 weeks")
  axis(1, at = ticks, labels = format(ticks, "%d.%m."), cex.axis = 0.6)
  axis(2, at = 3:1, labels = TERMINE$verein, las = 1, cex.axis = 0.65, lwd = 0)
  for (i in seq_len(nrow(TERMINE))) {
    y <- 4 - i
    segments(TERMINE$prae[i], y, TERMINE$post[i], y, col = "grey70", lwd = 1)
    if (TERMINE$ig[i]) rect(PROGRAMM[1], y - 0.18, PROGRAMM[2], y + 0.18, col = "grey85", border = "grey40", lwd = 0.7)
    points(TERMINE$prae[i], y, pch = 15, cex = 1.1, col = "black")
    points(TERMINE$post[i], y, pch = 16, cex = 1.1, col = "black")
    text(TERMINE$prae[i], y + 0.3, format(TERMINE$prae[i], "%d.%m."), cex = 0.55)
    text(TERMINE$post[i], y + 0.3, format(TERMINE$post[i], "%d.%m."), cex = 0.55)
    wochen <- as.numeric(TERMINE$post[i] - TERMINE$prae[i]) / 7
    text(TERMINE$post[i], y - 0.32, paste0(fmt(wochen, 1), " Wochen"), cex = 0.5, col = "grey30")
  }
  text(mean(PROGRAMM), 3.62, "Programm W1 bis W6 (20.07. bis 30.08.), nur Interventionsgruppe", cex = 0.55, col = "grey30")
  legend("bottomleft", legend = c("Eingangstestung", "Abschlusstestung", "Programmzeitraum"), pch = c(15, 16, 22), pt.bg = c(NA, NA, "grey85"), col = c("black", "black", "grey40"), pt.cex = c(1, 1, 1.4), cex = 0.55, bty = "n", horiz = TRUE, inset = c(0, -0.02))
}
png(file.path(AUS, "Abb_H7_Zeitstrahl.png"), width = 16, height = 5.5, units = "cm", res = 300, type = "cairo")
zeichne_h7()
dev.off()
cairo_pdf(file.path(AUS, "Abb_H7_Zeitstrahl.pdf"), width = 16 / 2.54, height = 5.5 / 2.54, family = "sans")
zeichne_h7()
dev.off()
md("*Abb. H7.* Zeitstrahl der Eingangs- und Abschlusstestungen je Verein mit dem Programmzeitraum der Interventionsgruppe und dem Prä-Post-Intervall in Wochen (Abb_H7_Zeitstrahl.png/.pdf). Termine nach Kennzahlenblatt K-03, Familiarisierungstermine liegen nicht als Datum vor.")
md("")

# ---------------------------------------------------------------- Abschluss
if (any(grepl(intToUtf8(59), MD, fixed = TRUE))) stop("Semikolon in einem Objekt")
writeLines(MD, file.path(AUS, "Objekte_2026-09-25.md"), useBytes = TRUE)
verw <- unique(verwendet)
prot <- c("Objekte_2026-09-25.R, Laufprotokoll", paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")), paste0("Eingang: ", EINGANG, " (SHA-256 ", SHA, ")", if (SYNTH) " SYNTHETISCH" else ""),
          paste0("R: ", R.version.string), paste0("Kennungen der Ergebnisdatei: ", nrow(E), ", davon in den Objekten verwendet: ", length(verw)),
          paste0("Dateien: ", paste(sort(list.files(AUS)), collapse = ", ")))
writeLines(prot, file.path(AUS, "Objekte_2026-09-25.txt"), useBytes = TRUE)
cat(paste(prot, collapse = "\n"), "\n")

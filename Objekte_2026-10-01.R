# =====================================================================
# Objekte_2026-10-01.R
# Zweck: Tabellen und Abbildungen des Manuskripts aus der Ergebnisdatei der berichteten
#        Rechnung erzeugen. Textteil: Tab. 1 bis 3, Abb. 1 und 2. Anhang H: Tab. H1a bis H5,
#        Abb. H1 (Zeitstrahl). Jede Zahl stammt aus einer Kennung der Ergebnisdatei oder aus
#        einer benannten Konstante (Angabe des Verfassers, Kennzahlenblatt K-01.24 und K-03).
#        Keine Zahl von Hand, keine Summe oder Differenz von Kennungen im Erzeuger.
# Grundlage: Objekte_2026-09-25.R (dritte Fassung), umgestellt nach der Objektprüfung dvs vom
#        01.10.2026 (05_Protokolle\Pruefprotokoll_Objekte_dvs_2026-10-01, Befundliste § 7,
#        Klickfreigabe § 12). Rechnung, Kennungen und Rundung unverändert.
# Änderungen gegenüber 2026-09-25 (Auswahl, je Befund im Protokoll):
#        Form der Beschriftung nach dvs (Kennzeichnung „Tab. X.“ aufrecht, Titel kursiv,
#        „Abb. X.“ kursiv, Unterschrift aufrecht, kein Schlusspunkt, Erklärungen in der Anmerkung),
#        keine Dateinamen und Kennungen in Beschriftungen, Begriffe des Manuskripts,
#        kein Hinweis auf nicht Gerechnetes, gerundete Null ohne Vorzeichen (KF7),
#        Tausendertrennung mit schmalem Leerzeichen U+202F (KF5), Spielercodes A-xx und B-xx (KF15),
#        Kategorie Lichtschrankenausfall in Tab. H1b (KF16), Grund der nicht Angetretenen (KF17),
#        Umbau zu breiter Tabellen ohne Zahländerung (KF8), Abb. H7 heißt Abb. H1 (KF6),
#        Abbildungen in Endbreite 14,25 cm mit 10 pt Arial und Linien ab ¾ pt, Graustufen-PNG (KF9).
# Ausgabe (im Ausgabeordner): je Tabelle eine CSV (Kopf zweistufig mit „::“, Zellabsatz „<br>“,
#        Index „~x~“), Objekte_2026-10-01_Liste.csv (Kennzeichnung, Titel, Anmerkung je Objekt,
#        für das Setzwerkzeug), Objekte_2026-10-01.md (Lesefassung), Abbildungen als PNG (300 dpi,
#        Graustufen) und PDF, Objekte_2026-10-01.txt (Laufprotokoll).
# Aufruf: Rscript Objekte_2026-10-01.R <Ergebnisdatei.csv> <Ausgabeordner> [synthetisch]
# Nur base R und grDevices.
# =====================================================================

invisible(Sys.setlocale("LC_CTYPE", "C.UTF-8"))
if (.Platform$OS.type == "windows") grDevices::windowsFonts(Arial = grDevices::windowsFont("Arial"))
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Aufruf: Rscript Objekte_2026-10-01.R <Ergebnisdatei.csv> <Ausgabeordner> [synthetisch]")
EINGANG <- args[1]
AUS <- args[2]
SYNTH <- length(args) >= 3 && args[3] == "synthetisch"
dir.create(AUS, showWarnings = FALSE, recursive = TRUE)
FASSUNG <- "Objekte_2026-10-01"

# ---------------------------------------------------------------- Konstanten (Angaben des Verfassers)
ANGEFRAGT <- 4L   # angefragte Vereine (Clusterebene Abb. 1), Angabe des Verfassers 25.09.2026, K-01.24
ZUGESAGT <- 3L    # Vereine A, B, C
GRUND_NANG <- "nicht anwesend am Testtag"   # Grund aller vier nicht zur Abschlusstestung Angetretenen, Angabe des Verfassers 01.10.2026 (KF17)

# ---------------------------------------------------------------- Eingang
sha256 <- function(pfad) {
  out <- tryCatch(suppressWarnings(system2("sha256sum", shQuote(pfad), stdout = TRUE, stderr = FALSE)), error = function(e) character(0))
  if (length(out) > 0 && grepl("^[0-9a-f]{64}", out[1])) return(substr(out[1], 1, 64))
  out <- tryCatch(suppressWarnings(system2("certutil", c("-hashfile", shQuote(normalizePath(pfad)), "SHA256"), stdout = TRUE, stderr = FALSE)), error = function(e) character(0))
  h <- grep("^[0-9a-fA-F ]{64,}$", out, value = TRUE)
  if (length(h) > 0) return(tolower(gsub(" ", "", h[1])))
  "nicht ermittelt"
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
LEERSTELLEN <- character(0)   # Zellen ohne Wert: Objekt | Kennung | Grund, im Laufprotokoll
leer <- function(objekt, k) {
  LEERSTELLEN <<- c(LEERSTELLEN, paste(objekt, k, g(k), sep = " | "))
  LEER
}
# Leere Zellen werden je Tabelle in der Anmerkung erklärt. Die Erklärung gilt nur für die
# erwarteten Leerstellen, jede andere bricht den Lauf ab (die Anmerkung bliebe sonst falsch).
pruefe_leer <- function(objekt, erwartet) {
  ist <- sub("^[^|]+ \\| ([^|]+) \\|.*$", "\\1", grep(paste0("^", objekt, " \\|"), LEERSTELLEN, value = TRUE))
  if (!setequal(ist, erwartet)) stop(paste0("Leerstellen in ", objekt, " weichen ab: ", paste(ist, collapse = ", ")))
}

# ---------------------------------------------------------------- Darstellung (§ 3.7, Klickfreigabe 01.10.)
MINUS <- "−"
LEER <- "–"
THIN <- " "     # schmales geschütztes Leerzeichen, Tausendertrennung (KF5)
BR <- "<br>"         # Zellabsatz
RUNDUNG <- data.frame(wert = character(0), stellen = integer(0), darstellung = character(0), stringsAsFactors = FALSE)   # jede Rundung, für die Prüfung der Gleichstände
fmt <- function(x, nd, sign = FALSE) {
  if (is.na(x)) return(LEER)
  s <- sub("\\.", ",", formatC(abs(x), format = "f", digits = nd))
  RUNDUNG[nrow(RUNDUNG) + 1, ] <<- list(sprintf("%.17g", x), as.integer(nd), s)
  if (as.numeric(sub(",", ".", s)) == 0) return(s)   # gerundete Null ohne Vorzeichen (KF7)
  if (x < 0) return(paste0(MINUS, s))
  if (sign) return(paste0("+", s))
  s
}
ganz <- function(n) if (is.na(n)) LEER else if (abs(n) >= 1000) formatC(n, format = "d", big.mark = THIN) else as.character(n)
fp <- function(p) if (is.na(p)) LEER else if (p < 0.001) "< 0,001" else fmt(p, 3)
ki <- function(u, o, nd, sign = TRUE) if (is.na(u) || is.na(o)) LEER else paste(fmt(u, nd, sign), "bis", fmt(o, nd, sign))
msd <- function(m, s, nd) if (is.na(m) || is.na(s)) LEER else paste(fmt(m, nd), "±", fmt(s, nd))
WORT <- c("null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf")
zahlwort <- function(n) if (!is.na(n) && n >= 0 && n <= 12 && n == round(n)) WORT[n + 1] else ganz(n)
ZIELE <- c(Z05 = "5-m-Sprint", Z10 = "10-m-Sprint", Z30 = "30-m-Sprint", CL = "505 links", CR = "505 rechts", CM = "505-Seitenmittel", SBJ = "Standweitsprung")
KONF <- c("Z30", "CM", "SBJ")
EINH <- function(z) if (z == "SBJ") "cm" else "s"
ZE <- function(z) paste0(ZIELE[[z]], " (", EINH(z), ")")
NDM <- function(z) if (z == "SBJ") 0 else 2     # M ± SD
NDD <- function(z) if (z == "SBJ") 1 else 3     # Differenzen, KI, TE, SESOI
code_neu <- function(cd) sub("^BW-", "B-", sub("^HL-", "A-", cd))   # Codes der Datenhaltung zu A-xx und B-xx (KF15)
ABK_GRUPPE <- "IG = Interventionsgruppe, KG = Kontrollgruppe"
ABK_PAH <- "%PAH = Reifestatus als prozentualer Anteil der prognostizierten Erwachsenenkörperhöhe"

# ---------------------------------------------------------------- Ausgabe
LISTE <- data.frame(id = character(0), art = character(0), bereich = character(0), kennzeichnung = character(0),
                    titel = character(0), anmerkung = character(0), datei = character(0), stringsAsFactors = FALSE)
MD <- character(0)
md <- function(...) MD <<- c(MD, paste0(...))
schreibe_tabelle <- function(id, kennzeichnung, titel, df, anmerkung) {
  stopifnot(!grepl("\\.$", titel))
  csv <- paste0(id, ".csv")
  utils::write.table(df, file.path(AUS, csv), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
  LISTE[nrow(LISTE) + 1, ] <<- c(id, "Tabelle", if (grepl("^Tab\\. [0-9]", kennzeichnung)) "Text" else "Anhang", kennzeichnung, titel, anmerkung, csv)
  md("<!-- Objekt ", id, " -->")
  md(kennzeichnung, " *", titel, "*")
  md("")
  md("| ", paste(names(df), collapse = " | "), " |")
  md("|", paste(rep("---", ncol(df)), collapse = "|"), "|")
  for (i in seq_len(nrow(df))) md("| ", paste(unlist(df[i, ]), collapse = " | "), " |")
  md("")
  md("*Anmerkung.* ", anmerkung)
  md("")
}
schreibe_abbildung <- function(id, kennzeichnung, titel, anmerkung) {
  stopifnot(!grepl("\\.$", titel))
  LISTE[nrow(LISTE) + 1, ] <<- c(id, "Abbildung", if (grepl("^Abb\\. [0-9]", kennzeichnung)) "Text" else "Anhang", kennzeichnung, titel, anmerkung, paste0(id, ".png"))
  md("<!-- Objekt ", id, " -->")
  md("![](", id, ".png)")
  md("")
  md("*", kennzeichnung, "* ", titel)
  md("")
  md("*Anmerkung.* ", anmerkung)
  md("")
}

md("# Objekte des Manuskripts aus der Ergebnisdatei")
md("")
md("Erzeugt von ", FASSUNG, ".R aus ", basename(EINGANG), " (SHA-256 ", SHA, ")", if (SYNTH) " · SYNTHETISCHE PROBEDATEN, KEINE STUDIENERGEBNISSE" else "",
   ". Lesefassung: Kopf zweistufig mit „::“, Zellabsatz „<br>“, Index „~x~“. Gesetzt wird mit Werkzeug_Objekte_Docx_2026-10-01.py nach dvs (2020).")
md("")

# ---------------------------------------------------------------- Tab. 1 Messgüte (Wortlaut nach Textvorschlag 4.4 § 9, KF18)
t1 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE,
  "Zielgröße" = character(0), "n" = character(0), "TE<br>[95-%-KI]" = character(0), "CV (%)" = character(0),
  "SESOI" = character(0), "TE/SESOI" = character(0), "TE post<br>[95-%-KI]" = character(0))
npost <- character(0)
for (z in names(ZIELE)) {
  nd <- NDD(z)
  t1[nrow(t1) + 1, ] <- c(ZE(z), ganz(w(sprintf("S10.NTE.%s.PRE.ALL.X", z))),
    paste0(fmt(w(sprintf("S10.TE.%s.PRE.ALL.X", z)), nd), BR, "[", ki(w(sprintf("S10.TELO.%s.PRE.ALL.X", z)), w(sprintf("S10.TEHI.%s.PRE.ALL.X", z)), nd, FALSE), "]"),
    fmt(w(sprintf("S10.CV.%s.PRE.ALL.X", z)), 1),
    fmt(w(sprintf("S10.SESOI.%s.PRE.ALL.X", z)), nd), fmt(w(sprintf("S10.RTS.%s.PRE.ALL.X", z)), 2),
    paste0(fmt(w(sprintf("S10.TE.%s.POST.ALL.X", z)), nd), BR, "[", ki(w(sprintf("S10.TELO.%s.POST.ALL.X", z)), w(sprintf("S10.TEHI.%s.POST.ALL.X", z)), nd, FALSE), "]"))
  npost <- c(npost, paste0(ZIELE[[z]], " ", ganz(w(sprintf("S10.NTE.%s.POST.ALL.X", z)))))
}
schreibe_tabelle("Tab_1_Messguete", "Tab. 1.",
  "Messgüte je Zielgröße aus den Wiederholungsversuchen der Eingangstestung (Spieler mit mindestens zwei gültigen Versuchen) und typischer Messfehler der Abschlusstestung", t1,
  paste0("n = Spieler mit mindestens zwei gültigen Versuchen in der Eingangstestung. TE = typischer Messfehler (gepoolte Intra-Personen-Standardabweichung der gültigen Versuche innerhalb der Sitzung) mit 95-%-Konfidenzintervall (KI) aus der χ²-Verteilung. CV = TE in Prozent des Mittelwerts aller gültigen Versuche. SESOI = kleinster praktisch bedeutsamer Unterschied (0,2 · Standardabweichung der Bestwerte aller Spieler bei der Eingangstestung). TE/SESOI > 1: Der Messfehler übersteigt den SESOI. 505 links/rechts = Wenderichtung, Seitenmittel aus beidseitig gültigen Versuchsnummern. TE post = typischer Messfehler der Abschlusstestung, n post: ",
         paste(npost, collapse = ", "), "."))

# ---------------------------------------------------------------- Tab. 2 Ausgangswerte (Anmerkung nach Textvorschlag 4.7 § 7)
t2 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "IG::n" = character(0), "IG::M ± SD" = character(0),
  "KG::n" = character(0), "KG::M ± SD" = character(0), "d" = character(0), "Überlappung IG / KG::Ausgangswert" = character(0), "Überlappung IG / KG::%PAH" = character(0))
for (z in names(ZIELE)) {
  ova <- if (z %in% KONF) paste0(ganz(w(sprintf("S14.OVPREIG.%s.X.ITT.HAUPT", z))), " / ", ganz(w(sprintf("S14.OVPREKG.%s.X.ITT.HAUPT", z)))) else LEER
  ovp <- if (z %in% KONF) paste0(ganz(w(sprintf("S14.OVPAHIG.%s.X.ITT.HAUPT", z))), " / ", ganz(w(sprintf("S14.OVPAHKG.%s.X.ITT.HAUPT", z)))) else LEER
  t2[nrow(t2) + 1, ] <- c(ZE(z), ganz(w(sprintf("S12.N.%s.PRE.ITTIG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.ITTIG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.ITTIG.HAUPT", z)), NDM(z)),
    ganz(w(sprintf("S12.N.%s.PRE.ITTKG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.ITTKG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.ITTKG.HAUPT", z)), NDM(z)), fmt(w(sprintf("S12.D.%s.PRE.ITT.HAUPT", z)), 2, TRUE), ova, ovp)
}
schreibe_tabelle("Tab_2_Ausgangswerte", "Tab. 2.", "Ausgangswerte je Zielgröße im Analyseset (Mittelwert ± Standardabweichung)", t2,
  paste0(ABK_GRUPPE, ", n = Zahl der Spieler, M ± SD = Mittelwert ± Standardabweichung, ", ABK_PAH, ". Analyseset je Zielgröße: Spieler mit Wert bei Eingangs- und Abschlusstestung und mit %PAH. Bestwert der gültigen Versuche, 505-Seitenmittel als Mittel der beiden Seiten-Bestwerte. d = Differenz der Gruppenmittelwerte bei der Eingangstestung, geteilt durch die gepoolte Standardabweichung (Cohen, 1988), bei Zeiten bedeutet ein negatives d eine schnellere IG. Überlappung = Zahl der Spieler je Gruppe im gemeinsamen Wertebereich beider Gruppen, für den Ausgangswert und den %PAH, angegeben für die konfirmatorischen Zielgrößen (", LEER, " bei den beschreibenden)."))

# ---------------------------------------------------------------- Tab. 3 Gruppenvergleich (transponiert, KF8, Anmerkung nach Textvorschlag 4.7 § 7)
t3 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Kennwert" = c("n IG / KG", "Abschlusswert IG, M ± SD", "Abschlusswert KG, M ± SD",
  "Differenz unadjustiert [95-%-KI]", "Differenz adjustiert [95-%-KI]", "p", "g [95-%-KI]"))
sesoi_txt <- character(0)
for (z in KONF) {
  nd <- NDD(z)
  t3[[ZE(z)]] <- c(paste0(ganz(w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z))), " / ", ganz(w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z)))),
    msd(w(sprintf("S15.MPOSTIG.%s.X.ITT.HAUPT", z)), w(sprintf("S12.SD.%s.POST.ITTIG.HAUPT", z)), NDM(z)),
    msd(w(sprintf("S15.MPOSTKG.%s.X.ITT.HAUPT", z)), w(sprintf("S12.SD.%s.POST.ITTKG.HAUPT", z)), NDM(z)),
    paste0(fmt(w(sprintf("S15.UD.%s.X.ITT.HAUPT", z)), nd, TRUE), BR, "[", ki(w(sprintf("S15.UDKIU.%s.X.ITT.HAUPT", z)), w(sprintf("S15.UDKIO.%s.X.ITT.HAUPT", z)), nd), "]"),
    paste0(fmt(w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), nd, TRUE), BR, "[", ki(w(sprintf("S13.KIU.%s.X.ITT.HAUPT", z)), w(sprintf("S13.KIO.%s.X.ITT.HAUPT", z)), nd), "]"),
    fp(w(sprintf("S13.P.%s.X.ITT.HAUPT", z))),
    paste0(fmt(w(sprintf("S15.G.%s.X.ITT.HAUPT", z)), 2, TRUE), BR, "[", ki(w(sprintf("S15.GKIU.%s.X.ITT.HAUPT", z)), w(sprintf("S15.GKIO.%s.X.ITT.HAUPT", z)), 2), "]"))
  sesoi_txt <- c(sesoi_txt, paste0(ZIELE[[z]], " ", fmt(w(sprintf("S10.SESOI.%s.PRE.ALL.X", z)), nd), " ", EINH(z)))
}
schreibe_tabelle("Tab_3_Gruppenvergleich", "Tab. 3.", "Gruppenvergleich der konfirmatorischen Zielgrößen im Analyseset: unadjustierte und adjustierte Differenz der Abschlusswerte", t3,
  paste0(ABK_GRUPPE, ", n = Zahl der Spieler, M ± SD = Mittelwert ± Standardabweichung, KI = Konfidenzintervall, ", ABK_PAH, ". Differenz IG minus KG, negative Zeit- und positive Weitendifferenzen liegen zugunsten der IG. Unadjustiert: Differenz der Mittelwerte der Abschlusstestung, KI aus dem t-Verfahren mit gepoolter Varianz. Adjustiert: Gruppenkoeffizient der Kovarianzanalyse mit Ausgangswert und %PAH als kontinuierlichen Kovariaten, Analyse in der zugeteilten Gruppe. p gehört zur adjustierten Differenz, mit drei Nachkommastellen, darunter < 0,001. g = adjustierte Differenz geteilt durch die gepoolte Standardabweichung der Ausgangswerte des Analysesets, korrigiert um J = 1 ", MINUS, " 3 / (4 · df ", MINUS, " 1) mit df = n~IG~ + n~KG~ ", MINUS, " 2 (Hedges' g), KI aus dem der adjustierten Differenz. SESOI = kleinster praktisch bedeutsamer Unterschied (0,2 · Standardabweichung der Bestwerte aller Spieler bei der Eingangstestung): ",
         paste(sesoi_txt, collapse = ", "), "."))

# ---------------------------------------------------------------- Tab. H1a Versuche
h1a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Eingangstestung::gültige Versuche" = character(0), "Eingangstestung::k̄ IG" = character(0), "Eingangstestung::k̄ KG" = character(0),
  "Abschlusstestung::gültige Versuche" = character(0), "Abschlusstestung::k̄ IG" = character(0), "Abschlusstestung::k̄ KG" = character(0))
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) {
  h1a[nrow(h1a) + 1, ] <- c(ZIELE[[z]], ganz(w(sprintf("S02.NGUELT.%s.PRE.ALL.X", z))), fmt(w(sprintf("S09.KMEAN.%s.PRE.IG.X", z)), 2), fmt(w(sprintf("S09.KMEAN.%s.PRE.KG.X", z)), 2),
    ganz(w(sprintf("S02.NGUELT.%s.POST.ALL.X", z))), fmt(w(sprintf("S09.KMEAN.%s.POST.IG.X", z)), 2), fmt(w(sprintf("S09.KMEAN.%s.POST.KG.X", z)), 2))
}
schreibe_tabelle("Tab_H1a_Versuche", "Tab. H1a.", "Gültige Versuche je Zielgröße und Testung und mittlere Zahl gültiger Versuche je Spieler (k̄) nach Gruppe", h1a,
  paste0(ABK_GRUPPE, ". Vorgesehen waren drei Versuche je Spieler und Zielgröße. Bezugsmenge der Eingangstestung sind die zugeteilten Spieler (IG ", ganz(w("S08.FLZUG.X.X.IG.X")), ", KG ", ganz(w("S08.FLZUG.X.X.KG.X")),
         "), der Abschlusstestung die zur Abschlusstestung angetretenen (IG ", ganz(w("S08.FLAUSG.X.X.IG.X")), ", KG ", ganz(w("S08.FLAUSG.X.X.KG.X")), "). k̄ = gültige Versuche je Spieler der Gruppe."))

# ---------------------------------------------------------------- Tab. H1b Ausfallgründe (Zeilen Zielgröße × Grund, KF8, KF16)
KAT <- c(TECH = "technischer Ausfall (Lichtschranke)", ZEIT = "Zeitmangel beim dritten Versuch", FEHL = "nicht wiederholbarer Fehlversuch", FALSCH = "Ausfall der 10-m-Lichtschranke", NANG = "nicht angetreten")
# Die Kategorie FALSCH („falsch aufgenommen“ im Messprotokoll) ist nach Angabe des Verfassers vom 01.10.2026 der Ausfall der 10-m-Lichtschranke (KF16).
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) for (t in c("PRE", "POST")) for (gr in c("IG", "KG")) {
  if (!(z == "Z10" && t == "POST" && gr == "IG") && w(sprintf("S03.NKAT.%s.%s.%s.FALSCH", z, t, gr)) != 0) stop("Kategorie FALSCH außerhalb von 10 m, Abschlusstestung, IG")
}
# Gestörte Auslösung (Kategorie AUSL) kam nicht vor, sie steht deshalb nur in der Anmerkung. Jede Kennung einzeln geprüft, keine Summe.
for (k in c("S02.NAUSL.X.PRE.ALL.X", "S02.NAUSL.X.POST.ALL.X", as.vector(outer(outer(c("Z05", "Z10", "Z30", "CL", "CR", "SBJ"), c("PRE", "POST"), paste, sep = "."), c("IG", "KG"), function(a, b) sprintf("S03.NKAT.%s.%s.AUSL", a, b))))) {
  if (w(k) != 0) stop(paste("Gestörte Auslösung nicht null:", k, "- Tab. H1b braucht die Zeile"))
}
h1b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Grund" = character(0),
  "Eingangstestung::IG" = character(0), "Eingangstestung::KG" = character(0), "Abschlusstestung::IG" = character(0), "Abschlusstestung::KG" = character(0))
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) for (k in names(KAT)) {
  zelle <- c(ZIELE[[z]], KAT[[k]])
  for (t in c("PRE", "POST")) for (gr in c("IG", "KG")) {
    zelle <- c(zelle, if (k == "NANG" && t == "PRE") LEER else ganz(w(sprintf("S03.NKAT.%s.%s.%s.%s", z, t, gr, k))))
  }
  h1b[nrow(h1b) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H1b_Ausfallgruende", "Tab. H1b.", "Ungültige Versuche je Zielgröße, Ausfallgrund, Testung und Gruppe", h1b,
  paste0(ABK_GRUPPE, ". Bezugsmengen wie in Tab. H1a. Jeder ungültige Versuch zählt bei genau einem Grund, in dieser Rangfolge: nicht angetreten (Abschlusstestung ohne den Spieler), gestörte Auslösung, dann der von der Testleitung vermerkte Grund. Versuche mit gestörter Auslösung kamen bei keiner Testung vor. Bei der Abschlusstestung von Verein B fiel die 10-m-Lichtschranke für alle Läufe aus, im Messprotokoll als „falsch aufgenommen“ vermerkt. ",
         LEER, " = entfällt, zur Eingangstestung waren alle zugeteilten Spieler anwesend."))

# ---------------------------------------------------------------- Tab. H1c Fehlende Werte (zweistufiger Kopf, KF8)
h1c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Ohne Wert der Eingangstestung::IG" = character(0), "Ohne Wert der Eingangstestung::KG" = character(0),
  "Ohne Wert der Abschlusstestung::IG" = character(0), "Ohne Wert der Abschlusstestung::KG" = character(0), "Erhebungsanteil::IG" = character(0), "Erhebungsanteil::KG" = character(0))
for (z in names(ZIELE)) {
  h1c[nrow(h1c) + 1, ] <- c(ZIELE[[z]], ganz(w(sprintf("S08.FLOPRE.%s.X.IG.X", z))), ganz(w(sprintf("S08.FLOPRE.%s.X.KG.X", z))), ganz(w(sprintf("S08.FLOPOST.%s.X.IG.X", z))), ganz(w(sprintf("S08.FLOPOST.%s.X.KG.X", z))),
    paste0(fmt(100 * w(sprintf("S08.ANT.%s.X.IG.X", z)), 1), " %"), paste0(fmt(100 * w(sprintf("S08.ANT.%s.X.KG.X", z)), 1), " %"))
}
schreibe_tabelle("Tab_H1c_Fehlende_Werte", "Tab. H1c.", "Spieler ohne Bestwert je Zielgröße, Testung und Gruppe und Erhebungsanteil", h1c,
  paste0(ABK_GRUPPE, ". Bezugsmenge sind die zugeteilten Spieler (IG ", ganz(w("S08.FLZUG.X.X.IG.X")), ", KG ", ganz(w("S08.FLZUG.X.X.KG.X")), "). Ein Spieler ohne Wert bei beiden Testungen zählt in beiden Spalten. Zur Abschlusstestung nicht angetretene Spieler zählen bei der Abschlusstestung. Erhebungsanteil = Spieler mit Werten beider Testungen je zugeteiltem Spieler."))

# ---------------------------------------------------------------- Tab. H1d Verschiebung des Bestwerts (Stellen nach § 3.7)
h1d <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Eingangstestung::n" = character(0), "Eingangstestung::Δ" = character(0), "Eingangstestung::Δ / SESOI" = character(0),
  "Abschlusstestung::n" = character(0), "Abschlusstestung::Δ" = character(0), "Abschlusstestung::Δ / SESOI" = character(0))
for (z in c("Z05", "Z10", "Z30", "CL", "CR", "SBJ")) {
  zelle <- ZE(z)
  for (t in c("PRE", "POST")) {
    kd <- sprintf("S11.DMEAN.%s.%s.ALL.X", z, t)
    ks <- sprintf("S11.DSESOI.%s.%s.ALL.X", z, t)
    d <- w(kd)
    s <- w(ks)
    zelle <- c(zelle, ganz(w(sprintf("S11.N.%s.%s.ALL.X", z, t))), if (is.na(d)) leer("H1d", kd) else fmt(d, NDD(z), TRUE), if (is.na(s)) leer("H1d", ks) else fmt(s, 2, TRUE))
  }
  h1d[nrow(h1d) + 1, ] <- zelle
}
pruefe_leer("H1d", c("S11.DMEAN.CL.POST.ALL.X", "S11.DMEAN.CR.POST.ALL.X", "S11.DSESOI.CL.POST.ALL.X", "S11.DSESOI.CR.POST.ALL.X"))
if (w("S11.N.CL.POST.ALL.X") != 0 || w("S11.N.CR.POST.ALL.X") != 0) stop("Tab. H1d: Leerstelle trotz Spielern mit drei Versuchen")
schreibe_tabelle("Tab_H1d_Bestwertverschiebung", "Tab. H1d.", "Verschiebung des Bestwerts durch den dritten Versuch je Zielgröße und Testung (Spieler mit drei gültigen Versuchen)", h1d,
  paste0("n = Spieler mit drei gültigen Versuchen. Δ = Bestwert aus allen drei Versuchen minus Bestwert aus den ersten beiden, gemittelt über die Spieler, bei Zeiten höchstens null, beim Standweitsprung mindestens null. SESOI = kleinster praktisch bedeutsamer Unterschied (0,2 · Standardabweichung der Bestwerte aller Spieler derselben Testung). ",
         LEER, " = kein Spieler mit drei gültigen Versuchen."))

# ---------------------------------------------------------------- Tab. H1e TE je Verein (Zellabsatz für n und df, KF8)
h1e <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0),
  "Eingangstestung::Verein A" = character(0), "Eingangstestung::Verein B" = character(0), "Eingangstestung::Verein C" = character(0),
  "Abschlusstestung::Verein A" = character(0), "Abschlusstestung::Verein B" = character(0), "Abschlusstestung::Verein C" = character(0))
for (z in names(ZIELE)) {
  zelle <- ZE(z)
  for (t in c("PRE", "POST")) for (v in c("VA", "VB", "VC")) {
    k <- sprintf("S10.TE.%s.%s.%s.X", z, t, v)
    te <- w(k)
    zelle <- c(zelle, if (is.na(te)) leer("H1e", k) else paste0(fmt(te, NDD(z)), BR, "n = ", ganz(w(sprintf("S10.NTE.%s.%s.%s.X", z, t, v))), BR, "df = ", ganz(w(sprintf("S10.DFTE.%s.%s.%s.X", z, t, v)))))
  }
  h1e[nrow(h1e) + 1, ] <- zelle
}
pruefe_leer("H1e", "S10.TE.Z10.POST.VB.X")
if (w("S03.NKAT.Z10.POST.IG.FALSCH") == 0) stop("Tab. H1e: Leerstelle ohne Lichtschrankenausfall")
schreibe_tabelle("Tab_H1e_TE_je_Verein", "Tab. H1e.", "Typischer Messfehler je Zielgröße, Verein und Testung", h1e,
  paste0("TE = typischer Messfehler aus den Wiederholungsversuchen der Spieler mit mindestens zwei gültigen Versuchen, je Verein getrennt. Darunter n = Zahl dieser Spieler und df = Freiheitsgrade. Vereine A und B bildeten die Interventionsgruppe, Verein C die Kontrollgruppe. ",
         LEER, " = kein Wert, bei der Abschlusstestung von Verein B fiel die 10-m-Lichtschranke aus."))

# ---------------------------------------------------------------- Tab. H2a Umsetzung je Spieler (Codes A-xx und B-xx, KF15)
alt_codes <- sub("^S07\\.ADH\\.ADH\\.X\\.P(.*)\\.GANZ$", "\\1", grep("^S07\\.ADH\\.ADH\\.X\\.P.*\\.GANZ$", E$Kennung, value = TRUE))
alt_codes <- alt_codes[order(code_neu(alt_codes))]
if (any(!grepl("^[AB]-", code_neu(alt_codes)))) stop("Unbekannter Codepräfix in der Interventionsgruppe")
h2a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Spieler" = character(0), "Meldungen" = character(0), "Vollständige Einheiten::gesamt" = character(0),
  "Vollständige Einheiten::höchstens zwei je Programmwoche" = character(0), "Vollständige Einheiten::verschiedene Einheitennummern" = character(0))
for (cd in alt_codes) {
  zelle <- c(code_neu(cd), ganz(w(sprintf("S06.NMELD.FB.X.P%s.X", cd))))
  for (v in c("GANZ", "WOCAP", "DIST")) {
    k <- sprintf("S07.ADH.ADH.X.P%s.%s", cd, v)
    a <- w(k)
    zelle <- c(zelle, if (is.na(a)) { leer("H2a", k); "nicht erhebbar" } else ganz(a))
  }
  h2a[nrow(h2a) + 1, ] <- zelle
}
pruefe_leer("H2a", c("S07.ADH.ADH.X.PBW-21.GANZ", "S07.ADH.ADH.X.PBW-21.WOCAP", "S07.ADH.ADH.X.PBW-21.DIST"))
schreibe_tabelle("Tab_H2a_Umsetzung_je_Spieler", "Tab. H2a.", "Umsetzung je zugeteiltem Spieler der Interventionsgruppe: Meldungen und vollständig durchgeführte Einheiten", h2a,
  paste0("Bezugsmenge sind die ", ganz(w("S07.NZUG.ADH.X.IG.X")), " zugeteilten Spieler der Interventionsgruppe mit je zwölf angebotenen Einheiten. Gemeldet wurden ", ganz(w("S06.NMELD.FB.X.ALL.X")), " Einheiten, davon ",
         ganz(w("S06.NSTAT.FB.X.IG.GANZ")), " vollständig, ", ganz(w("S06.NSTAT.FB.X.IG.TEILW")), " teilweise und ", ganz(w("S06.NSTAT.FB.X.IG.GARN")), " nicht durchgeführt. Untergrenzen der vollständigen Einheiten: höchstens zwei Meldungen je Programmwoche, nur verschiedene Einheitennummern. Spieler B-21 hatte keinen Listenplatz im Fragebogen, seine Einheiten sind nicht erhebbar und zählen in Summe, Umsetzungsrate, Median, Mittel und Tab. H5 als null. Summe vollständig ",
         ganz(w("S07.SUMME.ADH.X.IG.GANZ")), " (Umsetzungsrate ", fmt(100 * w("S07.RATE.ADH.X.IG.GANZ"), 1), " %), vollständig oder teilweise ", ganz(w("S07.SUMME.ADH.X.IG.GT")), " (", fmt(100 * w("S07.RATE.ADH.X.IG.GT"), 1), " %), höchstens zwei je Programmwoche ",
         ganz(w("S07.SUMME.ADH.X.IG.WOCAP")), " (", fmt(100 * w("S07.RATE.ADH.X.IG.WOCAP"), 1), " %), verschiedene Einheitennummern ", ganz(w("S07.SUMME.ADH.X.IG.DIST")), " (", fmt(100 * w("S07.RATE.ADH.X.IG.DIST"), 1), " %). Median ",
         fmt(w("S07.MED.ADH.X.IG.GANZ"), 1), ", Mittel ", fmt(w("S07.MITT.ADH.X.IG.GANZ"), 2), " vollständige Einheiten je zugeteiltem Spieler."))

# ---------------------------------------------------------------- Tab. H2b Verlauf je Programmwoche
h2b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Programmwoche" = character(0), "Anteil vollständiger Meldungen" = character(0), "Beanspruchung (CR-10)::n" = character(0), "Beanspruchung (CR-10)::M ± SD" = character(0),
  "sRPE-Load (AU)::n" = character(0), "sRPE-Load (AU)::M ± SD" = character(0))
for (wk in 1:6) {
  cm <- w(sprintf("S07.M.CR10.W%d.IG.GANZ", wk))
  cs <- w(sprintf("S07.SD.CR10.W%d.IG.GANZ", wk))
  lm <- w(sprintf("S07.M.LOAD.W%d.IG.GANZ", wk))
  ls <- w(sprintf("S07.SD.LOAD.W%d.IG.GANZ", wk))
  if (any(is.na(c(cm, cs, lm, ls)))) stop("Wochenwert fehlt in Tab. H2b")
  h2b[nrow(h2b) + 1, ] <- c(as.character(wk), paste0(fmt(100 * w(sprintf("S07.ANTW.ADH.W%d.IG.GANZ", wk)), 1), " %"), ganz(w(sprintf("S07.N.CR10.W%d.IG.GANZ", wk))), msd(cm, cs, 1),
    ganz(w(sprintf("S07.N.LOAD.W%d.IG.GANZ", wk))), msd(lm, ls, 1))
}
schreibe_tabelle("Tab_H2b_Wochenverlauf", "Tab. H2b.", "Verlauf je Programmwoche: Anteil vollständiger Meldungen, Beanspruchung und sRPE-Load der vollständig gemeldeten Einheiten", h2b,
  paste0("Bezugsmenge sind die ", ganz(w("S07.NZUG.ADH.X.IG.X")), " zugeteilten Spieler der Interventionsgruppe. Anteil = vollständige Meldungen der Woche geteilt durch zwei angebotene Einheiten je zugeteiltem Spieler. n = Zahl der Meldungen, M ± SD = Mittelwert ± Standardabweichung. CR-10 = Beanspruchung auf der CR-10-Skala. sRPE-Load = CR-10 mal Solldauer der Programmwoche (Wochen- und Aufwärmvideo) in willkürlichen Einheiten (AU), keine individuell gemessene Dauer. Über alle Wochen: CR-10 n = ",
         ganz(w("S07.N.CR10.X.IG.GANZ")), ", ", msd(w("S07.M.CR10.X.IG.GANZ"), w("S07.SD.CR10.X.IG.GANZ"), 1), ", Median ", fmt(w("S07.MED.CR10.X.IG.GANZ"), 1), ", Minimum ", fmt(w("S07.MIN.CR10.X.IG.GANZ"), 1), ", Maximum ", fmt(w("S07.MAX.CR10.X.IG.GANZ"), 1),
         ". sRPE-Load n = ", ganz(w("S07.N.LOAD.X.IG.GANZ")), ", ", msd(w("S07.M.LOAD.X.IG.GANZ"), w("S07.SD.LOAD.X.IG.GANZ"), 1), " AU, Median ", fmt(w("S07.MED.LOAD.X.IG.GANZ"), 1), ", Minimum ", fmt(w("S07.MIN.LOAD.X.IG.GANZ"), 1), ", Maximum ", fmt(w("S07.MAX.LOAD.X.IG.GANZ"), 1), "."))

# ---------------------------------------------------------------- Tab. H2c Adhärenzkriterium
ak_alt <- unique(sub("^S16\\.DIFF\\.[A-Z0-9]+\\.DIFF\\.P(.*)\\.AK9$", "\\1", grep("^S16\\.DIFF\\..*\\.AK9$", E$Kennung, value = TRUE)))
ak_alt <- ak_alt[order(code_neu(ak_alt))]
h2c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Spieler" = character(0), "30-m-Sprint (s)" = character(0), "505-Seitenmittel (s)" = character(0), "Standweitsprung (cm)" = character(0))
for (cd in ak_alt) {
  zelle <- code_neu(cd)
  for (z in KONF) {
    d <- w(sprintf("S16.DIFF.%s.DIFF.P%s.AK9", z, cd))
    if (is.na(d)) stop("Einzelwert fehlt in Tab. H2c")
    zelle <- c(zelle, fmt(d, NDD(z), TRUE))
  }
  h2c[nrow(h2c) + 1, ] <- zelle
}
n_ak <- w("S07.GE09.ADH.X.IG.GANZ")
if (n_ak != nrow(h2c)) stop("Tab. H2c: Zahl der Spieler stimmt nicht mit S07.GE09")
schreibe_tabelle("Tab_H2c_Adhaerenzkriterium", "Tab. H2c.", "Spieler mit mindestens neun von zwölf vollständig durchgeführten Einheiten (Adhärenzkriterium): Veränderung der Bestwerte von der Eingangs- zur Abschlusstestung", h2c,
  paste0("Veränderung = Abschluss- minus Eingangswert. Bei Zeiten bedeuten negative, beim Standweitsprung positive Werte eine Verbesserung. Das Kriterium erfüllten ", zahlwort(n_ak), " Spieler, die Tabelle zeigt ihre Einzelwerte."))

# ---------------------------------------------------------------- Tab. H3a Ausgangswerte aller Eingangsgetesteten
h3a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "IG::n" = character(0), "IG::M ± SD" = character(0), "KG::n" = character(0), "KG::M ± SD" = character(0), "d" = character(0))
for (z in names(ZIELE)) {
  h3a[nrow(h3a) + 1, ] <- c(ZE(z), ganz(w(sprintf("S12.N.%s.PRE.IG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.IG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.IG.HAUPT", z)), NDM(z)),
    ganz(w(sprintf("S12.N.%s.PRE.KG.HAUPT", z))), msd(w(sprintf("S12.M.%s.PRE.KG.HAUPT", z)), w(sprintf("S12.SD.%s.PRE.KG.HAUPT", z)), NDM(z)), fmt(w(sprintf("S12.D.%s.PRE.BASE.HAUPT", z)), 2, TRUE))
}
schreibe_tabelle("Tab_H3a_Ausgangswerte_alle", "Tab. H3a.", "Ausgangswerte aller eingangsgetesteten Spieler mit Bestwert je Zielgröße, zum Vergleich mit dem Analyseset in Tab. 2", h3a,
  paste0(ABK_GRUPPE, ", n = Zahl der Spieler mit Bestwert, M ± SD = Mittelwert ± Standardabweichung. d = Differenz der Gruppenmittelwerte, geteilt durch die gepoolte Standardabweichung (Cohen, 1988), bei Zeiten bedeutet ein negatives d eine schnellere IG."))

# ---------------------------------------------------------------- Tab. H3b Beschreibende Zielgrößen (n als Zellabsatz, KF8)
h3b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Eingangstestung::IG" = character(0), "Eingangstestung::KG" = character(0), "Abschlusstestung::IG" = character(0), "Abschlusstestung::KG" = character(0))
for (z in c("Z05", "Z10", "CL", "CR")) {
  zelle <- ZE(z)
  for (t in c("PRE", "POST")) for (gr in c("ITTIG", "ITTKG")) zelle <- c(zelle, paste0(msd(w(sprintf("S12.M.%s.%s.%s.HAUPT", z, t, gr)), w(sprintf("S12.SD.%s.%s.%s.HAUPT", z, t, gr)), NDM(z)), BR, "(n = ", ganz(w(sprintf("S12.N.%s.%s.%s.HAUPT", z, t, gr))), ")"))
  h3b[nrow(h3b) + 1, ] <- zelle
}
schreibe_tabelle("Tab_H3b_Beschreibende_Zielgroessen", "Tab. H3b.", "Beschreibende Zielgrößen im Analyseset: Bestwerte bei Eingangs- und Abschlusstestung je Gruppe", h3b,
  paste0(ABK_GRUPPE, ", Mittelwert ± Standardabweichung, n = Zahl der Spieler. Die 5- und 10-m-Sprintzeiten und die 505-Seitenwerte sind beschreibende Zielgrößen. Beim 10-m-Sprint fehlt in der IG die Abschlusstestung von Verein B, weil dort die 10-m-Lichtschranke ausfiel."))

# ---------------------------------------------------------------- Tab. H4a Modellkennwerte (transponiert, KF8)
h4a <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Kennwert" = c("b~0~ (SE)", "b~1~ Gruppe (SE)", "b~2~ Ausgangswert (SE)", "b~3~ %PAH (SE)", "Residuen-SD", "R²",
  "adjustiertes Mittel IG [95-%-KI]", "adjustiertes Mittel KG [95-%-KI]"))
for (z in KONF) {
  nd <- NDD(z)
  ndk <- if (z == "SBJ") 2 else 3
  k <- function(x) w(sprintf("S13.%s.%s.X.ITT.HAUPT", x, z))
  h4a[[ZE(z)]] <- c(paste0(fmt(k("B0"), ndk), " (", fmt(k("SEB0"), ndk), ")"), paste0(fmt(k("B1"), nd, TRUE), " (", fmt(k("SEB1"), nd), ")"),
    paste0(fmt(k("B2"), 3), " (", fmt(k("SEB2"), 3), ")"), paste0(fmt(k("B3"), ndk), " (", fmt(k("SEB3"), ndk), ")"), fmt(k("SIGMA"), nd), fmt(k("R2"), 2),
    paste0(fmt(k("AMIG"), nd), BR, "[", ki(k("AMIGU"), k("AMIGO"), nd, FALSE), "]"), paste0(fmt(k("AMKG"), nd), BR, "[", ki(k("AMKGU"), k("AMKGO"), nd, FALSE), "]"))
}
schreibe_tabelle("Tab_H4a_Modellkennwerte", "Tab. H4a.", "Modellkennwerte der Kovarianzanalyse im Analyseset und adjustierte Mittelwerte", h4a,
  paste0(ABK_GRUPPE, ", ", ABK_PAH, ". Modell: Abschlusswert = b~0~ + b~1~ · Gruppe + b~2~ · Ausgangswert + b~3~ · %PAH, Gruppe IG = 1, KG = 0, df = n ", MINUS, " 4. SE = Standardfehler, Residuen-SD = Standardabweichung der Residuen, R² = Bestimmtheitsmaß, KI = Konfidenzintervall. Adjustierte Mittelwerte beim Mittel von Ausgangswert und %PAH im Analyseset: ",
         paste(sapply(KONF, function(z) paste0(ZIELE[[z]], " ", fmt(w(sprintf("S13.PREM.%s.X.ITT.HAUPT", z)), NDD(z)), " ", EINH(z), " und ", fmt(w(sprintf("S13.PAHM.%s.X.ITT.HAUPT", z)), 2), " %")), collapse = ", "), "."))

# ---------------------------------------------------------------- Tab. H4b Voraussetzungsprüfungen (transponiert, Teilstatistik je Zellabsatz, KF8)
verw <- function(f) if (!is.na(f) && f == 1) paste0(BR, "verworfen") else ""
h4b <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Prüfung" = c("Shapiro-Wilk-Test der Residuen", "Brown-Forsythe-Test", "Residuen-SD IG / KG (Verhältnis KG / IG)",
  "Gruppe × Ausgangswert", "Gruppe × %PAH", "Vorab: Gruppe × %PAH im Modell der Ausgangswerte"))
for (z in KONF) {
  nd <- NDD(z)
  k <- function(x, v = "HAUPT") w(sprintf("S14.%s.%s.X.ITT.%s", x, z, v))
  vorab <- w(sprintf("S14.CINT.%s.PRE.BPAH.SLPAH", z))
  if (is.na(vorab)) stop("Vorab-Prüfung fehlt in Tab. H4b")
  h4b[[ZE(z)]] <- c(paste0("W = ", fmt(k("SWW"), 3), BR, "p = ", fp(k("SWP")), verw(k("SWVERW"))),
    paste0("F(", ganz(k("BFDF1")), ", ", ganz(k("BFDF2")), ") = ", fmt(k("BFF"), 2), BR, "p = ", fp(k("BFP")), verw(k("BFVERW"))),
    paste0(fmt(k("SDRIG"), nd), " / ", fmt(k("SDRKG"), nd), BR, "(", fmt(k("SDRQ"), 2), ")"),
    paste0("b = ", fmt(k("BINT", "SLPRE"), 3, TRUE), BR, "t(", ganz(k("DFINT", "SLPRE")), ") = ", fmt(k("TINT", "SLPRE"), 2), BR, "p = ", fp(k("PINT", "SLPRE")), verw(k("VERW", "SLPRE"))),
    paste0("b = ", fmt(k("BINT", "SLPAH"), 4, TRUE), BR, "t(", ganz(k("DFINT", "SLPAH")), ") = ", fmt(k("TINT", "SLPAH"), 2), BR, "p = ", fp(k("PINT", "SLPAH")), verw(k("VERW", "SLPAH"))),
    paste0("c~3~ = ", fmt(vorab, 4, TRUE), BR, "t(", ganz(w(sprintf("S14.DFCINT.%s.PRE.BPAH.SLPAH", z))), ") = ", fmt(w(sprintf("S14.TCINT.%s.PRE.BPAH.SLPAH", z)), 2), BR, "p = ", fp(w(sprintf("S14.PCINT.%s.PRE.BPAH.SLPAH", z)))))
}
sw_pre <- sapply(KONF, function(z) paste0(ZIELE[[z]], ": IG W = ", fmt(w(sprintf("S14.SWW.%s.PRE.BPAHIG.X", z)), 3), ", p = ", fp(w(sprintf("S14.SWP.%s.PRE.BPAHIG.X", z))),
  ", KG W = ", fmt(w(sprintf("S14.SWW.%s.PRE.BPAHKG.X", z)), 3), ", p = ", fp(w(sprintf("S14.SWP.%s.PRE.BPAHKG.X", z))), "."))
schreibe_tabelle("Tab_H4b_Voraussetzungen", "Tab. H4b.", "Voraussetzungsprüfungen der Kovarianzanalyse je Zielgröße und Vorab-Prüfung an den Ausgangswerten", h4b,
  paste0(ABK_GRUPPE, ", ", ABK_PAH, ". W, F und t = Prüfgrößen, p = Überschreitungswahrscheinlichkeit, verworfen = Voraussetzung bei p < 0,05 verworfen. Shapiro-Wilk-Test auf allen Residuen des Modells, Brown-Forsythe-Test (Levene-Test mit Median) auf den Residuen nach Gruppe. Residuen-SD = Standardabweichung der Residuen je Gruppe, nachträglich festgelegt. Steigungshomogenität in zwei getrennten Modellen mit je einem Interaktionsterm, b = dessen Koeffizient, df = n ",
         MINUS, " 5. Die Vorab-Prüfung an den Ausgangswerten in der Menge mit Ausgangswert und %PAH (df = n ", MINUS, " 4, c~3~ = Koeffizient des Interaktionsterms) beschreibt die Ausgangslage und ist keine Voraussetzung der Kovarianzanalyse. Shapiro-Wilk-Test der Ausgangswerte je Gruppe in derselben Menge, ",
         paste(sw_pre, collapse = " ")))

# ---------------------------------------------------------------- Tab. H4c Varianten (Vordersatz nach Textvorschlag 4.7 § 7)
VAR <- list(c("PP6", "Per-Protokoll ab sechs Einheiten", "S16", "PP6", "HAUPT"), c("MW", "Mittelwert statt Bestwert der Versuche", "S17", "ITT", "MW"),
            c("PP5", "Per-Protokoll ab fünf Einheiten", "S17", "PP5", "HAUPT"), c("PP7", "Per-Protokoll ab sieben Einheiten", "S17", "PP7", "HAUPT"),
            c("AEND", "Änderungswertmodell", "S17", "ITT", "AEND"), c("OPAH", "Modell ohne %PAH", "S17", "ITT", "OPAH"),
            c("FAMB", "Familiarisierungstermine als dritte Kovariate", "S17", "FAMS", "FAMB"), c("BOOT", "Bootstrap-Perzentil-KI der Hauptanalyse", "S19", "ITT", "BOOT"))
h4c <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Variante" = character(0), "Zielgröße" = character(0), "n IG / KG" = character(0), "Adjustierte Differenz [95-%-KI]" = character(0), "p" = character(0))
for (v in VAR) for (z in KONF) {
  nd <- NDD(z)
  if (v[1] == "BOOT") {
    h4c[nrow(h4c) + 1, ] <- c(v[2], ZE(z), paste0(ganz(w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z))), " / ", ganz(w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z)))),
      paste0(fmt(w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), nd, TRUE), BR, "[", ki(w(sprintf("S19.BKIU.%s.X.ITT.BOOT", z)), w(sprintf("S19.BKIO.%s.X.ITT.BOOT", z)), nd), "]"), LEER)
  } else {
    kb <- sprintf("%s.B1.%s.X.%s.%s", v[3], z, v[4], v[5])
    b1 <- w(kb)
    h4c[nrow(h4c) + 1, ] <- c(v[2], ZE(z), paste0(ganz(w(sprintf("%s.NIG.%s.X.%s.%s", v[3], z, v[4], v[5]))), " / ", ganz(w(sprintf("%s.NKG.%s.X.%s.%s", v[3], z, v[4], v[5])))),
      if (is.na(b1)) leer("H4c", kb) else paste0(fmt(b1, nd, TRUE), BR, "[", ki(w(sprintf("%s.KIU.%s.X.%s.%s", v[3], z, v[4], v[5])), w(sprintf("%s.KIO.%s.X.%s.%s", v[3], z, v[4], v[5])), nd), "]"),
      if (is.na(b1)) LEER else fp(w(sprintf("%s.P.%s.X.%s.%s", v[3], z, v[4], v[5]))))
  }
}
pruefe_leer("H4c", c("S16.B1.CM.X.PP6.HAUPT", "S17.B1.CM.X.PP7.HAUPT"))
B_boot <- unique(sapply(KONF, function(z) w(sprintf("S19.BNGUELT.%s.X.ITT.BOOT", z))))
if (length(B_boot) != 1) stop("Zahl der Bootstrap-Ziehungen je Zielgröße verschieden")
schreibe_tabelle("Tab_H4c_Varianten", "Tab. H4c.", "Per-Protokoll-Vergleich, vorab festgelegte Sensitivitätsanalysen und Bootstrap-Konfidenzintervall: adjustierte Gruppendifferenz je Variante", h4c,
  paste0("Neben dem Per-Protokoll-Vergleich ab sechs Einheiten waren vorab sechs Sensitivitätsanalysen festgelegt: Mittelwert statt Bestwert der Versuche, Per-Protokoll ab fünf und ab sieben Einheiten, Änderungswertmodell, Modell ohne %PAH, Familiarisierungstermine als dritte Kovariate (in der Interventionsgruppe mit Verein A konfundiert). ",
         ABK_GRUPPE, ", n = Zahl der Spieler, KI = Konfidenzintervall, ", ABK_PAH, ". Adjustierte Differenz IG minus KG wie in Tab. 3. Per-Protokoll-Vergleiche sind beobachtend und nicht randomisiert. ",
         LEER, " bei Differenz und p: Teilmenge mit weniger als acht Spielern je Gruppe, beschrieben in Tab. H4d. Bootstrap mit B = ", ganz(B_boot), " Ziehungen, geschichtet nach Gruppe, Startwert 20260924, nachträglich festgelegt, es liefert das Intervall zur Differenz der Hauptanalyse (", LEER, " bei p)."))

# ---------------------------------------------------------------- Tab. H4d Teilmengen (Gruppe in der Vorspalte)
h4d <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Menge" = character(0), "Gruppe" = character(0), "Zielgröße" = character(0), "n" = character(0),
  "M ± SD::Eingangstestung" = character(0), "M ± SD::Abschlusstestung" = character(0))
for (s in list(c("PP5", "S17", "PP5IG", "HAUPT", "fünf"), c("PP6", "S16", "PP6IG", "HAUPT", "sechs"), c("PP7", "S17", "PP7IG", "HAUPT", "sieben"))) for (z in KONF) {
  h4d[nrow(h4d) + 1, ] <- c(paste0("Per-Protokoll ab ", s[5], " Einheiten"), "IG", ZE(z), ganz(w(sprintf("S08.N.%s.X.%sIG.X", z, s[1]))),
    msd(w(sprintf("%s.M.%s.PRE.%s.%s", s[2], z, s[3], s[4])), w(sprintf("%s.SD.%s.PRE.%s.%s", s[2], z, s[3], s[4])), NDM(z)), msd(w(sprintf("%s.M.%s.POST.%s.%s", s[2], z, s[3], s[4])), w(sprintf("%s.SD.%s.POST.%s.%s", s[2], z, s[3], s[4])), NDM(z)))
}
for (gr in c("IG", "KG")) for (z in KONF) {
  h4d[nrow(h4d) + 1, ] <- c("Spieler mit Familiarisierungsangabe", gr, ZE(z), ganz(w(sprintf("S08.N.%s.X.FAMS%s.X", z, gr))),
    msd(w(sprintf("S17.M.%s.PRE.FAMS%s.FAMB", z, gr)), w(sprintf("S17.SD.%s.PRE.FAMS%s.FAMB", z, gr)), NDM(z)), msd(w(sprintf("S17.M.%s.POST.FAMS%s.FAMB", z, gr)), w(sprintf("S17.SD.%s.POST.FAMS%s.FAMB", z, gr)), NDM(z)))
}
schreibe_tabelle("Tab_H4d_Teilmengen", "Tab. H4d.", "Bestwerte der Per-Protokoll-Teilmengen und der Spieler mit Familiarisierungsangabe bei Eingangs- und Abschlusstestung", h4d,
  paste0(ABK_GRUPPE, ", n = Zahl der Spieler der Menge, M ± SD = Mittelwert ± Standardabweichung. Die KG der Per-Protokoll-Vergleiche ist die KG des Analysesets (Tab. 2, Tab. 3). Spieler mit Familiarisierungsangabe: Menge der Sensitivitätsanalyse mit den Familiarisierungsterminen als dritter Kovariate."))

# ---------------------------------------------------------------- Tab. H4e Familiarisierung (n als eigene Zeile, KF8)
h4e <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Zielgröße" = character(0), "Kennwert" = character(0), "IG::ein Termin" = character(0), "IG::zwei Termine" = character(0), "KG::ein Termin" = character(0), "KG::zwei Termine" = character(0))
for (z in KONF) {
  zn <- c(ZE(z), "n")
  zm <- c(ZE(z), "M ± SD")
  for (gr in c("ITTIG", "ITTKG")) for (f in c("F1", "F2")) {
    n <- w(sprintf("S17.N.%s.DIFF.%s.%s", z, gr, f))
    m <- w(sprintf("S17.M.%s.DIFF.%s.%s", z, gr, f))
    s <- w(sprintf("S17.SD.%s.DIFF.%s.%s", z, gr, f))
    zn <- c(zn, ganz(n))
    zm <- c(zm, if (is.na(m)) LEER else if (is.na(s)) fmt(m, NDD(z), TRUE) else paste0(fmt(m, NDD(z), TRUE), " ± ", fmt(s, NDD(z))))
  }
  h4e[nrow(h4e) + 1, ] <- zn
  h4e[nrow(h4e) + 1, ] <- zm
}
schreibe_tabelle("Tab_H4e_Familiarisierung", "Tab. H4e.", "Veränderung der Bestwerte von der Eingangs- zur Abschlusstestung im Analyseset nach Gruppe und Zahl der Familiarisierungstermine", h4e,
  paste0(ABK_GRUPPE, ", n = Zahl der Spieler, M ± SD = Mittelwert ± Standardabweichung der Veränderung (Abschluss- minus Eingangswert). In der IG fällt die Zahl der Termine mit dem Verein zusammen, Verein A hatte nur einen Termin. In der KG hatten alle Spieler zwei Termine (", LEER, ")."))

# ---------------------------------------------------------------- Tab. H5 Verteilung der vollständigen Einheiten
h5 <- data.frame(check.names = FALSE, stringsAsFactors = FALSE, "Vollständige Einheiten" = as.character(0:12),
  "Spieler mit genau dieser Zahl" = sapply(0:12, function(i) ganz(w(sprintf("S07.V%02d.ADH.X.IG.GANZ", i)))),
  "Spieler mit mindestens dieser Zahl" = c(ganz(w("S07.NZUG.ADH.X.IG.X")), sapply(1:12, function(i) ganz(w(sprintf("S07.GE%02d.ADH.X.IG.GANZ", i))))))
schreibe_tabelle("Tab_H5_Verteilung_Einheiten", "Tab. H5.", "Verteilung der vollständig durchgeführten Einheiten über die zugeteilten Spieler der Interventionsgruppe", h5,
  paste0("Bezugsmenge sind die ", ganz(w("S07.NZUG.ADH.X.IG.X")), " zugeteilten Spieler der Interventionsgruppe (Zeile 0 der letzten Spalte). Spieler B-21 ohne Listenplatz im Fragebogen zählt mit null Einheiten. Mindestens eine Meldung gleich welchen Status gaben ",
         ganz(w("S07.NMELDSP.ADH.X.IG.X")), " Spieler ab. Untergrenzen: mit höchstens zwei Meldungen je Programmwoche erreichten ", zahlwort(w("S07.GE06.ADH.X.IG.WOCAP")), " Spieler mindestens sechs und ", zahlwort(w("S07.GE09.ADH.X.IG.WOCAP")),
         " mindestens neun Einheiten, nach verschiedenen Einheitennummern ", zahlwort(w("S07.GE06.ADH.X.IG.DIST")), " und ", sub("^eins$", "einer", zahlwort(w("S07.GE09.ADH.X.IG.DIST"))), "."))

# ---------------------------------------------------------------- Abbildungen: Geräte in Endbreite (KF9)
BREITE_CM <- 14.25     # größte Bildbreite in der Formatvorlage „Abbildung“ (Satzspiegel 14,5 cm, Rahmen und Einzug)
PT <- 10               # Schrift 10 pt bei Endbreite
LWD <- 1               # lwd 1 = 0,75 pt
grafik <- function(datei, hoehe_cm, zeichne) {
  if (.Platform$OS.type == "windows") {
    png(file.path(AUS, paste0(datei, ".png")), width = BREITE_CM, height = hoehe_cm, units = "cm", res = 300, pointsize = PT, type = "windows", antialias = "gray", family = "Arial")
  } else {
    png(file.path(AUS, paste0(datei, ".png")), width = BREITE_CM, height = hoehe_cm, units = "cm", res = 300, pointsize = PT, type = "cairo", antialias = "gray", family = "Arial")
  }
  zeichne()
  dev.off()
  cairo_pdf(file.path(AUS, paste0(datei, ".pdf")), width = BREITE_CM / 2.54, height = hoehe_cm / 2.54, pointsize = PT, family = "Arial")
  zeichne()
  dev.off()
}
achse <- function(x, nd) gsub("-", MINUS, formatC(x, format = "f", digits = nd, decimal.mark = ","), fixed = TRUE)

# ---------------------------------------------------------------- Abb. 1 Teilnehmerfluss
umbruch <- function(txt, breite_cm) {
  # Zeilenumbruch nach gemessener Breite (cex 1, aktuelle Schrift), Zeilen mit „\n“ bleiben getrennt
  aus <- character(0)
  for (absatz in strsplit(txt, "\n", fixed = TRUE)[[1]]) {
    woerter <- strsplit(absatz, " ", fixed = TRUE)[[1]]
    zeile <- ""
    for (wd in woerter) {
      probe <- if (zeile == "") wd else paste(zeile, wd)
      if (strwidth(probe, units = "user") <= breite_cm || zeile == "") zeile <- probe else { aus <- c(aus, zeile); zeile <- wd }
    }
    aus <- c(aus, zeile)
  }
  aus
}
abb1_kaesten <- function() {
  nenner <- function(gr) paste(sapply(KONF, function(z) paste0(ZIELE[[z]], " ", ganz(w(sprintf("S08.N.%s.X.ITT%s.X", z, gr))))), collapse = ", ")
  list(
    oben = paste0("Vereine angefragt: n = ", ganz(ANGEFRAGT), ", ohne Zusage: n = ", ganz(ANGEFRAGT - ZUGESAGT), "\nZusagen: ", zahlwort(ZUGESAGT), " Vereine (A, B, C), Zuteilung auf Vereinsebene vor der Eingangstestung"),
    ig1 = paste0("Interventionsgruppe\nVerein A (n = ", ganz(w("S08.FLZUG.X.X.VA.X")), "), Verein B (n = ", ganz(w("S08.FLZUG.X.X.VB.X")), ")\nzugeteilt und eingangsgetestet: n = ", ganz(w("S08.FLPRE.X.X.IG.X"))),
    kg1 = paste0("Kontrollgruppe (Warteliste)\nVerein C (n = ", ganz(w("S08.FLZUG.X.X.VC.X")), ")\nzugeteilt und eingangsgetestet: n = ", ganz(w("S08.FLPRE.X.X.KG.X"))),
    ig2 = paste0("Intervention erhalten (mindestens eine vollständig gemeldete Einheit): n = ", ganz(w("S07.GE01.ADH.X.IG.GANZ")),
                 "\nnicht erhalten: ohne Meldung n = ", ganz(w("S08.B6NEKM.X.X.IG.X")), ", ohne Listenplatz im Fragebogen n = ", ganz(w("S08.B6IF.X.X.IG.X")),
                 "\nNichteinhaltung (weniger als sechs vollständige Einheiten, einschließlich null): n = ", ganz(w("S08.B6NE.X.X.IG.X"))),
    kg2 = "Wartelistenbedingung (Vereinsprogramm, ohne Erfassung)",
    ig3 = paste0("Abschlusstestung nicht angetreten (", GRUND_NANG, "): n = ", ganz(w("S08.FLNANG.X.X.IG.X")), "\nzur Abschlusstestung angetreten: n = ", ganz(w("S08.FLAUSG.X.X.IG.X")), "\nohne %PAH: n = ", ganz(w("S08.FLOPAH.PAH.X.IG.X"))),
    kg3 = paste0("Abschlusstestung nicht angetreten (", GRUND_NANG, "): n = ", ganz(w("S08.FLNANG.X.X.KG.X")), "\nzur Abschlusstestung angetreten: n = ", ganz(w("S08.FLAUSG.X.X.KG.X")), "\nohne %PAH (fehlende Anthropometrie): n = ", ganz(w("S08.FLOPAH.PAH.X.KG.X"))),
    ig4 = paste0("Analysiert (Analysepopulation): n = ", ganz(w("S12.N.AGE.PRE.ANAIG.X")), "\nje Zielgröße: ", nenner("IG"),
                 "\nPer-Protokoll (mindestens sechs vollständig gemeldete Einheiten): ", paste(sapply(KONF, function(z) paste0(ZIELE[[z]], " ", ganz(w(sprintf("S08.N.%s.X.PP6IG.X", z))))), collapse = ", ")),
    kg4 = paste0("Analysiert (Analysepopulation): n = ", ganz(w("S12.N.AGE.PRE.ANAKG.X")), "\nje Zielgröße: ", nenner("KG")))
}
ABB1_HOEHE <- NA
zeichne_abb1 <- function(nur_messen = FALSE) {
  par(mar = c(0, 0, 0, 0), xpd = NA, family = "Arial", lwd = LWD)
  plot.new()
  plot.window(xlim = c(0, BREITE_CM), ylim = c(0, if (is.na(ABB1_HOEHE)) 30 else ABB1_HOEHE), xaxs = "i", yaxs = "i")
  K <- abb1_kaesten()
  ZH <- 0.44          # Zeilenhöhe in cm (10 pt, Abstand genau 12 pt ≈ 0,42 cm)
  PAD <- 0.18         # Innenabstand oben und unten
  LUECKE <- 0.55      # Abstand zwischen Kastenreihen (Pfeil)
  BW <- 6.75          # Kastenbreite je Gruppe
  XL <- 0.05 + BW / 2
  XR <- BREITE_CM - 0.05 - BW / 2
  innen <- BW - 0.3
  zl <- function(txt, b = innen) umbruch(txt, b)
  hoehe <- function(z) length(z) * ZH + 2 * PAD
  reihen <- list(list(oben = zl(K$oben, BREITE_CM - 0.4)), list(zl(K$ig1), zl(K$kg1)), list(zl(K$ig2), zl(K$kg2)), list(zl(K$ig3), zl(K$kg3)), list(zl(K$ig4), zl(K$kg4)))
  hoehen <- sapply(reihen, function(r) max(sapply(r, hoehe)))
  gesamt <- sum(hoehen) + LUECKE * (length(reihen) - 1) + 0.1
  if (nur_messen) return(gesamt)
  kasten <- function(xm, yo, bw, h, zeilen) {
    rect(xm - bw / 2, yo - h, xm + bw / 2, yo, col = NA, border = "black", lwd = LWD)
    y0 <- yo - PAD - ZH / 2
    for (i in seq_along(zeilen)) text(xm - bw / 2 + 0.15, y0 - (i - 1) * ZH, zeilen[i], adj = c(0, 0.5), cex = 1)
  }
  pfeil <- function(x0, y0, x1, y1) arrows(x0, y0, x1, y1, length = 0.06, lwd = LWD, col = "black")
  y <- ABB1_HOEHE - 0.05
  kasten(BREITE_CM / 2, y, BREITE_CM - 0.1, hoehen[1], reihen[[1]][[1]])
  yu <- y - hoehen[1]
  y <- yu - LUECKE
  pfeil(XL, yu, XL, y)
  pfeil(XR, yu, XR, y)
  for (r in 2:length(reihen)) {
    kasten(XL, y, BW, hoehen[r], reihen[[r]][[1]])
    kasten(XR, y, BW, hoehen[r], reihen[[r]][[2]])
    yu <- y - hoehen[r]
    if (r < length(reihen)) {
      y <- yu - LUECKE
      pfeil(XL, yu, XL, y)
      pfeil(XR, yu, XR, y)
    }
  }
}
# Höhe aus dem Inhalt messen (Zeilenumbruch hängt von der Schrift ab), mit Reserve für abweichende Schriftmetrik der Geräte
messdatei <- tempfile(fileext = ".pdf")
cairo_pdf(messdatei, width = BREITE_CM / 2.54, height = 30 / 2.54, pointsize = PT, family = "Arial")
ABB1_HOEHE <- NA
ABB1_HOEHE <- ceiling(10 * zeichne_abb1(nur_messen = TRUE)) / 10 + 0.3
dev.off()
unlink(messdatei)
grafik("Abb_1_Teilnehmerfluss", ABB1_HOEHE, zeichne_abb1)
schreibe_abbildung("Abb_1_Teilnehmerfluss", "Abb. 1.", "Teilnehmerfluss auf Vereins- und Spielerebene bis zum planmäßigen Studienende",
  paste0("Zahl der angefragten und zusagenden Vereine nach Angabe des Verfassers. ", ABK_PAH, ". Analysiert wurde in der zugeteilten Gruppe, je Zielgröße mit Werten bei Eingangs- und Abschlusstestung und mit %PAH, ohne Ersetzung fehlender Werte. Fehlende Werte je Zielgröße in Tab. H1c, Nenner der beschreibenden Zielgrößen in Tab. 2 und Tab. H3b."))

# ---------------------------------------------------------------- Abb. 2 Ausgangswerte und reifeadjustierte Abschlusswerte
codes <- sub("^S05\\.PAH\\.PAH\\.PRE\\.P(.*)\\.X$", "\\1", grep("^S05\\.PAH\\.PAH\\.PRE\\.P", E$Kennung, value = TRUE))
gruppe_von <- function(cd) if (substr(cd, 1, 2) %in% c("HL", "BW")) 1 else 0   # Vereine A und B sind die IG
abb2_daten <- lapply(setNames(KONF, KONF), function(z) {
  itt <- codes[sapply(codes, function(cd) w(sprintf("S08.MITGL.%s.X.P%s.ITT", z, cd)) == 1)]
  pre <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.PRE.P%s.X", z, cd)))
  post <- sapply(itt, function(cd) w(sprintf("S04.BEST.%s.POST.P%s.X", z, cd)))
  pah <- sapply(itt, function(cd) w(sprintf("S05.PAH.PAH.PRE.P%s.X", cd)))
  G <- sapply(itt, gruppe_von)
  ok <- !is.na(pre) & !is.na(post) & !is.na(pah)
  list(pre = pre[ok], post = post[ok], pah = pah[ok], G = G[ok],
       b = c(w(sprintf("S13.B0.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B1.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B2.%s.X.ITT.HAUPT", z)), w(sprintf("S13.B3.%s.X.ITT.HAUPT", z))),
       pahm = w(sprintf("S13.PAHM.%s.X.ITT.HAUPT", z)))
})
zeichne_abb2 <- function() {
  layout(matrix(c(1, 2, 3, 4, 4, 4), nrow = 2, byrow = TRUE), heights = c(1, 0.24))
  par(mar = c(3.1, 3.4, 1.5, 0.4), family = "Arial", mgp = c(2.0, 0.5, 0), las = 1, tcl = -0.3, lwd = LWD, cex = 1)
  for (z in KONF) {
    D <- abb2_daten[[z]]
    b <- D$b
    if (any(is.na(c(b, D$pahm)))) stop("Modellkoeffizient fehlt für Abb. 2")
    yadj <- D$post - b[4] * (D$pah - D$pahm)
    nd <- if (z == "SBJ") 0 else 1
    xl <- range(D$pre)
    yl <- range(yadj)
    xl <- xl + c(-1, 1) * 0.06 * diff(xl)
    yl <- yl + c(-1, 1) * 0.08 * diff(yl)
    plot(D$pre, yadj, type = "n", xlim = xl, ylim = yl, axes = FALSE, xlab = "Ausgangswert", ylab = if (z == KONF[1]) "Abschlusswert, reifeadjustiert" else "",
         main = ZE(z), font.main = 1, cex.main = 1, cex.lab = 1)
    xt <- pretty(xl, n = 4)
    xt <- xt[xt >= xl[1] & xt <= xl[2]]
    yt <- pretty(yl, n = 4)
    yt <- yt[yt >= yl[1] & yt <= yl[2]]
    axis(1, at = xt, labels = achse(xt, nd), cex.axis = 1, lwd = LWD)
    axis(2, at = yt, labels = achse(yt, nd), cex.axis = 1, lwd = LWD)
    box(lwd = LWD)
    for (gr in c(1, 0)) {
      sel <- D$G == gr
      xr <- range(D$pre[sel])
      lines(xr, b[1] + b[2] * gr + b[3] * xr + b[4] * D$pahm, lty = if (gr == 1) 1 else 2, lwd = 1.5 * LWD, col = "black")
      points(D$pre[sel], yadj[sel], pch = if (gr == 1) 16 else 1, col = "black", cex = 0.7, lwd = LWD)
      xm <- mean(D$pre[sel])
      points(xm, b[1] + b[2] * gr + b[3] * xm + b[4] * D$pahm, pch = if (gr == 1) 15 else 0, cex = 1.3, col = "black", lwd = LWD)
    }
  }
  par(mar = c(0, 0, 0, 0))
  plot.new()
  leg <- c("IG Spieler", "KG Spieler", "IG Modell", "KG Modell", "IG Mittel", "KG Mittel")
  legend("center", legend = leg, pch = c(16, 1, NA, NA, 15, 0), lty = c(NA, NA, 1, 2, NA, NA),
         lwd = c(LWD, LWD, 1.5 * LWD, 1.5 * LWD, LWD, LWD), col = "black", pt.cex = c(0.7, 0.7, 1, 1, 1.3, 1.3), cex = 1, bty = "n", ncol = 3, x.intersp = 0.6,
         text.width = 1.25 * max(strwidth(leg)))
}
grafik("Abb_2_Modell", 8.2, zeichne_abb2)
n_abb2 <- paste(sapply(KONF, function(z) paste0(ZIELE[[z]], " IG ", ganz(w(sprintf("S13.NIG.%s.X.ITT.HAUPT", z))), ", KG ", ganz(w(sprintf("S13.NKG.%s.X.ITT.HAUPT", z))))), collapse = ", ")
schreibe_abbildung("Abb_2_Modell", "Abb. 2.", "Ausgangswert und reifeadjustierter Abschlusswert je Spieler mit den Modelllinien beider Gruppen",
  paste0("Konfirmatorische Zielgrößen im Analyseset, ", n_abb2, ". ", ABK_GRUPPE, ", ", ABK_PAH, ". Reifeadjustierter Abschlusswert = Abschlusswert ", MINUS, " b~3~ · (%PAH ", MINUS, " Mittel des %PAH im Analyseset), b~3~ = Koeffizient des %PAH in der Kovarianzanalyse (Tab. H4a). Linien: Modell je Gruppe über den beobachteten Bereich der Ausgangswerte, Quadrate: Gruppenmittel. Darstellung nach Vickers und Altman (2001), erweitert um die zweite Kovariate."))

# ---------------------------------------------------------------- Abb. H1 Zeitstrahl der Testungen (Anhang H, KF6)
# Termine je Verein aus dem Kennzahlenblatt K-03 (Personendaten des Datenstands, nicht aus der Ergebnisdatei),
# Programmzeitraum Woche 1 bis 6 aus den Konstanten der Spezifikation.
TERMINE <- data.frame(verein = c("Verein A (IG)", "Verein B (IG)", "Verein C (KG)"),
                      prae = as.Date(c("2026-07-02", "2026-07-14", "2026-07-13")),
                      post = as.Date(c("2026-09-10", "2026-09-01", "2026-09-14")),
                      ig = c(TRUE, TRUE, FALSE), stringsAsFactors = FALSE)
PROGRAMM <- as.Date(c("2026-07-20", "2026-08-30"))
zeichne_h1 <- function() {
  layout(matrix(1:2, nrow = 2), heights = c(1, 0.22))
  par(mar = c(3.0, 6.4, 0.6, 0.6), family = "Arial", mgp = c(1.9, 0.5, 0), tcl = -0.3, lwd = LWD, cex = 1, xpd = NA)
  x0 <- as.Date("2026-06-28")
  x1 <- as.Date("2026-09-20")
  plot(NA, xlim = c(x0, x1), ylim = c(0.5, 3.6), xaxt = "n", yaxt = "n", xlab = "Datum (2026)", ylab = "", bty = "n")
  ticks <- seq(as.Date("2026-07-01"), as.Date("2026-09-15"), by = "2 weeks")
  axis(1, at = ticks, labels = format(ticks, "%d.%m."), cex.axis = 1, lwd = LWD)
  axis(2, at = 3:1, labels = TERMINE$verein, las = 1, cex.axis = 1, lwd = 0)
  for (i in seq_len(nrow(TERMINE))) {
    y <- 4 - i
    segments(TERMINE$prae[i], y, TERMINE$post[i], y, col = "black", lwd = LWD, lty = 3)
    if (TERMINE$ig[i]) rect(PROGRAMM[1], y - 0.2, PROGRAMM[2] + 1, y + 0.2, col = "grey80", border = "black", lwd = LWD)
    points(TERMINE$prae[i], y, pch = 15, cex = 1.1, col = "black")
    points(TERMINE$post[i], y, pch = 16, cex = 1.1, col = "black")
    text(TERMINE$prae[i], y + 0.38, format(TERMINE$prae[i], "%d.%m."), cex = 1)
    text(TERMINE$post[i], y + 0.38, format(TERMINE$post[i], "%d.%m."), cex = 1)
    wochen <- as.numeric(TERMINE$post[i] - TERMINE$prae[i]) / 7
    text(TERMINE$prae[i] + as.numeric(TERMINE$post[i] - TERMINE$prae[i]) / 2, y - 0.38, paste0(fmt(wochen, 1), " Wochen"), cex = 1)
  }
  par(mar = c(0, 0, 0, 0))
  plot.new()
  legend("center", legend = c("Eingangstestung", "Abschlusstestung", "Programmzeitraum der IG"), pch = c(15, 16, 22), pt.bg = c(NA, NA, "grey80"), col = "black",
         pt.cex = c(1.1, 1.1, 1.6), cex = 1, bty = "n", horiz = TRUE, x.intersp = 0.6)
}
grafik("Abb_H1_Zeitstrahl", 7.2, zeichne_h1)
schreibe_abbildung("Abb_H1_Zeitstrahl", "Abb. H1.", "Termine der Eingangs- und Abschlusstestungen 2026 je Verein mit dem Programmzeitraum der Interventionsgruppe",
  paste0(ABK_GRUPPE, ". Programmzeitraum Woche 1 bis 6 vom ", format(PROGRAMM[1], "%d.%m."), " bis ", format(PROGRAMM[2], "%d.%m.%Y"), ". Unter jeder Linie der Abstand zwischen den Testungen in Wochen."))

# ---------------------------------------------------------------- Abschluss
if (any(grepl(intToUtf8(59), c(MD, unlist(LISTE)), fixed = TRUE))) stop("Semikolon in einem Objekt")
if (any(grepl("\\.(png|pdf|csv)", c(LISTE$titel, LISTE$anmerkung)))) stop("Dateiname in einer Beschriftung")
if (any(grepl("\\b(S[0-9]{2}|K-[0-9]{2})\\.", c(LISTE$titel, LISTE$anmerkung), perl = TRUE))) stop("Kennung in einer Beschriftung")
if (any(grepl("\\.$", LISTE$titel))) stop("Schlusspunkt im Titel")
utils::write.table(LISTE, file.path(AUS, paste0(FASSUNG, "_Liste.csv")), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
writeLines(MD, file.path(AUS, paste0(FASSUNG, ".md")), useBytes = TRUE)
verw_k <- unique(verwendet)
prot <- c(paste0(FASSUNG, ".R, Laufprotokoll"), paste0("Datum: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S %Z")), paste0("Eingang: ", EINGANG, " (SHA-256 ", SHA, ")", if (SYNTH) " SYNTHETISCH" else ""),
          paste0("R: ", R.version.string, ", Plattform ", R.version$platform), paste0("Kennungen der Ergebnisdatei: ", nrow(E), ", davon in den Objekten verwendet: ", length(verw_k)),
          paste0("Objekte: ", nrow(LISTE), " (", sum(LISTE$art == "Tabelle"), " Tabellen, ", sum(LISTE$art == "Abbildung"), " Abbildungen)"),
          paste0("Abb. 1 Höhe: ", ABB1_HOEHE, " cm, Breite aller Abbildungen ", BREITE_CM, " cm, Schrift ", PT, " pt"),
          "Leere Zellen (Objekt | Kennung | Grund der Ergebnisdatei):", paste0("  ", LEERSTELLEN),
          paste0("Dateien: ", paste(sort(list.files(AUS)), collapse = ", ")))
writeLines(prot, file.path(AUS, paste0(FASSUNG, ".txt")), useBytes = TRUE)
writeLines(verw_k, file.path(AUS, paste0(FASSUNG, "_Kennungen.txt")), useBytes = TRUE)
utils::write.table(RUNDUNG, file.path(AUS, paste0(FASSUNG, "_Rundungen.csv")), sep = ",", row.names = FALSE, qmethod = "double", fileEncoding = "UTF-8")
cat(paste(prot, collapse = "\n"), "\n")

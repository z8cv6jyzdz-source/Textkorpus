"""Pruefung_Standardweg_2026-09-26.py

Prüft am eigenen Datensatz, ob der Standardweg der Sensitivitäts-Poweranalyse
(Spezifikation S18, O9, Register R3) konservativ ist, also eine größere kleinste
nachweisbare Effektstärke unterstellt, als die Kovarianzanalyse tatsächlich auflöst.

Hintergrund: Der Standardweg rechnet mit lambda = d^2 * n_IG * n_KG / N und
df2 = N - 4. Er lässt zwei Größen weg, die in entgegengesetzte Richtung wirken:
den Gewinn durch die von Ausgangswert und %PAH erklärte Varianz (R^2) und den
Verlust durch das Ungleichgewicht der Kovariaten zwischen den Gruppen (Faktor SE).
Welche Seite überwiegt, hängt an den Daten. Nach F16 § 1.1 wird eine aus
Verteilungsannahmen abgeleitete Größe an den eigenen Daten geprüft.

Prüfgröße je konfirmatorischer Zielgröße: Quote = SE der adjustierten Differenz
(Hauptanalyse) geteilt durch den Standardfehler, den der Standardweg unterstellt
(Bezugs-SD mal Wurzel aus N / (n_IG * n_KG)). Quote < 1 heißt: Das
Konfidenzintervall der Hauptanalyse ist schmaler, als der Standardweg annimmt,
der Standardweg ist konservativ. Beide Seiten verwenden t mit df = N - 4, die
Quote gilt deshalb auch für die Breite des Konfidenzintervalls.

Drei Bezugs-SD:
  (1) gepoolte Post-SD des Analysesets (S15.SDPOST), maßgeblich, weil S18 Regel 2
      d in Einheiten der Innergruppen-SD ohne Minderung durch Kovariaten angibt,
      zugleich die strengste Wahl,
  (2) gepoolte Prä-SD des Analysesets (Nenner von Hedges' g, O3),
  (3) Prä-SD aller Eingangsgetesteten (S10.SB, Grundlage des SESOI).
Mit der Post-SD zerlegt das Skript die Quote in den Gewinn durch die Kovariaten
(Residuen-SD S13.SIGMA geteilt durch Post-SD) und den Verlust durch ihr
Ungleichgewicht (SE der adjustierten Differenz geteilt durch Residuen-SD mal
Wurzel aus N / (n_IG * n_KG)). Das Produkt ist die Quote.

Eingang: Anlage des Kennzahlenblatts (Kennzahlen_2026-09-25_Werte.csv), deren
Rohwerte aus der Ergebnisdatei der R-Rechnung stammen.
Die Quoten sind eine Prüfrechnung und keine Zahl für das Manuskript
(F16 § 1.2 Zahlenregel). Aus ihnen wird keine nachträgliche Power gerechnet
(CONSORT Item 7a).

Aufruf: python3 Pruefung_Standardweg_2026-09-26.py <Werte.csv> <Ausgabe.txt>
"""
import csv
import hashlib
import math
import sys

from scipy import optimize, stats

ZIELGROESSEN = [("Z30", "Sprint 30 m"), ("CM", "505-Seitenmittel"), ("SBJ", "Standweitsprung")]


def lese_werte(pfad):
    werte = {}
    with open(pfad, encoding="utf-8", newline="") as f:
        for zeile in csv.DictReader(f):
            kennungen = zeile["kennungen_ergebnisdatei"].split()
            roh = zeile["rohwerte"].split()
            if len(kennungen) != len(roh):
                continue
            for k, w in zip(kennungen, roh):
                try:
                    werte[k] = float(w)
                except ValueError:
                    pass
    return werte


def mdes_standardweg(n_ig, n_kg, alpha=0.05, power=0.80):
    n = n_ig + n_kg
    df2 = n - 4
    f_krit = stats.f.ppf(1 - alpha, 1, df2)

    def luecke(d):
        lam = d * d * n_ig * n_kg / n
        return stats.ncf.sf(f_krit, 1, df2, lam) - power

    return optimize.brentq(luecke, 0.01, 5.0)


def main():
    pfad_csv, pfad_aus = sys.argv[1], sys.argv[2]
    w = lese_werte(pfad_csv)
    sha = hashlib.sha256(open(pfad_csv, "rb").read()).hexdigest()
    zeilen = [
        "Pruefung_Standardweg_2026-09-26.py, Laufprotokoll",
        f"Eingang {pfad_csv.split('/')[-1]}, SHA-256 {sha}",
        "",
        "Quote = SE der adjustierten Differenz (Hauptanalyse) / SE nach Standardweg",
        "Quote < 1: Konfidenzintervall der Hauptanalyse schmaler als vom Standardweg unterstellt, Standardweg konservativ",
        "",
    ]
    alle_quoten = []
    for z, name in ZIELGROESSEN:
        n_ig = int(w[f"S13.NIG.{z}.X.ITT.HAUPT"])
        n_kg = int(w[f"S13.NKG.{z}.X.ITT.HAUPT"])
        n = n_ig + n_kg
        se_b1 = w[f"S13.SEB1.{z}.X.ITT.HAUPT"]
        b1 = w[f"S13.B1.{z}.X.ITT.HAUPT"]
        r2 = w[f"S13.R2.{z}.X.ITT.HAUPT"]
        df_modell = int(w[f"S13.DF.{z}.X.ITT.HAUPT"])
        sd_ig = w[f"S12.SD.{z}.PRE.ITTIG.HAUPT"]
        sd_kg = w[f"S12.SD.{z}.PRE.ITTKG.HAUPT"]
        sd_prae = math.sqrt(((n_ig - 1) * sd_ig ** 2 + (n_kg - 1) * sd_kg ** 2) / (n - 2))
        j = 1 - 3 / (4 * (n - 2) - 1)
        g_nach = b1 / sd_prae * j
        g_datei = w[f"S15.G.{z}.X.ITT.HAUPT"]
        sd_post = w[f"S15.SDPOST.{z}.X.ITT.HAUPT"]
        sd_alle = w[f"S10.SB.{z}.PRE.ALL.X"]
        faktor = math.sqrt(n / (n_ig * n_kg))
        mdes_datei = w[f"S18.MDES.{z}.X.ITT.X"]
        mdes_nach = mdes_standardweg(n_ig, n_kg)
        zeilen.append(f"{name}: n {n_ig}/{n_kg}, df {df_modell} (N - 4 = {n - 4}), R2 {r2:.3f}, SE b1 {se_b1:.6g}")
        zeilen.append(
            f"  Kontrolle Standardweg: MDES nachgerechnet {mdes_nach:.4f}, Ergebnisdatei {mdes_datei:.4f}, "
            f"Faktor Wurzel(N/(n_IG n_KG)) {faktor:.4f}"
        )
        zeilen.append(
            f"  Kontrolle Nenner von g: gepoolte Prä-SD {sd_prae:.6g}, g nachgerechnet {g_nach:.4f}, Ergebnisdatei {g_datei:.4f}"
        )
        for etikett, sd in (
            ("gepoolte Post-SD Analyseset (maßgeblich, S18 Regel 2: Innergruppen-SD ohne Minderung durch Kovariaten)", sd_post),
            ("gepoolte Prä-SD Analyseset (Nenner von g)", sd_prae),
            ("Prä-SD aller Eingangsgetesteten (Grundlage des SESOI)", sd_alle),
        ):
            quote = se_b1 / (sd * faktor)
            alle_quoten.append(quote)
            zeilen.append(f"  Quote mit {etikett} ({sd:.6g}): {quote:.3f}")
        sigma = w[f"S13.SIGMA.{z}.X.ITT.HAUPT"]
        gewinn = sigma / sd_post
        verlust = se_b1 / (sigma * faktor)
        zeilen.append(
            f"  Zerlegung mit der Post-SD: Gewinn durch die Kovariaten (Residuen-SD {sigma:.6g} / Post-SD) {gewinn:.3f}, "
            f"Verlust durch das Ungleichgewicht (SE b1 / (Residuen-SD mal Faktor)) {verlust:.3f}, netto {gewinn * verlust:.3f}"
        )
        zeilen.append("")
    urteil = "netto konservativ in allen drei Zielgrößen und mit allen drei Bezugs-SD" if max(alle_quoten) < 1 else "NICHT durchgehend konservativ"
    zeilen.append(f"Spanne der Quoten {min(alle_quoten):.3f} bis {max(alle_quoten):.3f}, Urteil: Standardweg {urteil}")
    zeilen.append("Die Quoten beruhen auf Schätzungen aus 23 bis 26 Spielern. Sie stützen die Richtung, sie beweisen sie nicht.")
    zeilen.append("Prüfrechnung, keine Zahl für das Manuskript (F16 § 1.2). Aus den Quoten wird keine tatsächliche Power und keine tatsächliche MDES abgeleitet (CONSORT Item 7a).")
    text = "\n".join(zeilen) + "\n"
    assert chr(59) not in text
    open(pfad_aus, "w", encoding="utf-8", newline="\n").write(text)
    print(text)


if __name__ == "__main__":
    main()

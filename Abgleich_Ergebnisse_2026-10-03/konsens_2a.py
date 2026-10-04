# -*- coding: utf-8 -*-
"""
konsens_2a.py — Konsenscodierung des Textstands von Kapitel 5, Schritt 2 (a), 03.10.2026

Zwei Fassungen je Satz:
  K  — Konsens nach Codebuch (Fassung 2) ohne die Anwendungshinweise der Übergabe § 5 Nr. 3. Gegen K1 bis K10 und
       gegen die Korpuszählungen zählt diese Fassung (Befund § 6.5, Übergabe § 5 Nr. 3 letzter Satz).
  KH — Fassung nach den Anwendungshinweisen (Adjudikation). Sie weicht nur dort von K ab, wo ein Hinweis den Code bestimmt.
HINWEIS nennt je Satz die Hinweise, deren Wortlaut den Satz erfasst (H1 bis H9, Wortlaut unten). Diese Sätze bilden die
Teilmenge für die getrennte Übereinstimmung.
Grundlage: codes_A.py (Codierer A, Ersteller), blind/codes_B.json mit blind/memo_B.md (Codierer B, unabhängiger
Subagent), Korpuskonsens in 03_Skripte\\Argumentationsstruktur_Ergebnisteile_2026-10-02\\saetze_codiert.csv.
Aufruf: python konsens_2a.py [<Ausgabe.csv>] — schreibt die Konsenstabelle (Trennzeichen chr(59) wie die Korpus-CSV).
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import csv

HINWEISTEXT = {
    'H1': 'Entscheidung über eine Hypothese ist B4 (Codebuch)',
    'H2': 'Quantor über alle konfirmatorischen Zielgrößen gilt als Sammelbefund B4 mit der Art als Sekundärcode (Projektauslegung)',
    'H3': 'Regel 2 und O-Codes gehen dem Quantor vor (Ausgangslage O4, Messgüte O5)',
    'H4': 'Einordnung nach vorab definierter Schwelle (Fall der Schlusslogik) ist deutung 0',
    'H5': 'Bootstrap-Intervall, Per-Protokoll-Vergleich und Sensitivitätsanalysen sind Z1',
    'H6': 'Meldungen mit Schmerzangabe sind Z2',
    'H7': 'gültige Versuche und typischer Messfehler sind O5',
    'H8': 'Beanspruchungsmaße (CR-10, sRPE-Load) sind O3',
    'H9': 'ein Satz, der nur eine Analyseregel nennt, ist V2',
}

# Satz: (Primärcode, Sekundärcodes, zg, deutung, Entscheidung mit Grund)
K = {
    'A1 S1': ('X1', ['O1'], '', 0, 'A und B X1. Sekundär O1 nach A: Das Objekt trägt nur Orientierung, wie im Korpuskonsens Veith 3.5 und Rogers 1.4 (X1 mit O2), Aloui 1.1 (X1 mit O5), Hilska 1.1 (X1 mit O4). B: Sekundärcode nur für einen Befund im zweiten Hauptsatz. Das Codebuch sagt das für Befunde, schließt weitere Inhalte nicht aus („bis zu zwei Sekundärcodes (weitere Inhalte, die der Satz trägt)“).'),
    'A1 S2': ('O1', [], '', 0, 'A und B gleich.'),
    'A1 S3': ('X1', ['O4'], 'X', 0, 'A und B X1. Sekundär O4 nach A: Beide Objekte enthalten nur Ausgangswerte, wie Hilska 1.1 (Spielermerkmale, X1 mit O4). Anders als Negra 2019 1.4 und Negra 2020 1.3, deren Objekte Ausgangs- und Post-Werte enthalten (X1 ohne Sekundärcode).'),
    'A1 S4': ('O4', [], 'X', 0, 'A und B gleich, Regel 2 (Ausgangsvergleich) vor dem Quantor „Alle“.'),
    'A2 S1': ('O2', [], '', 0, 'A und B gleich.'),
    'A2 S2': ('O2', [], '', 0, 'A und B gleich.'),
    'A2 S3': ('O2', [], '', 0, 'A und B gleich. Die Schwellen sechs und neun sind angewandt, nicht als Regel genannt (kein V2).'),
    'A2 S4': ('O2', ['Z1', 'V2'], '', 0, 'A O2 mit V2, B O2 mit Z1 und V2. Nach B: Fassung 17 § 3.2 führt die Untergrenzen „in 5.1 als Sensitivität“ (Z1 „Sensitivität“), der Satz nennt die Zählregeln (V2 „Definitionen … Einschlussregeln“).'),
    'A3 S1': ('O3', [], '', 0, 'A und B gleich.'),
    'A3 S2': ('O3', ['V2'], '', 0, 'A O3, B O3 mit V2. Nach B: „mit der Solldauer berechnet“ nennt die Definition der Größe (V2 „Definitionen“), wie Lloyd 1.3 (O2 mit V2).'),
    'A3 S3': ('Z2', ['O2'], '', 0, 'A und B gleich. Z2, nicht O2 mit Z2: Der Satz nennt Schmerzen nicht als Grund der Ausfälle (Klarstellung zu Regel 4 nicht einschlägig).'),
    'A3 S4': ('Z2', [], '', 0, 'A und B gleich. „solche Angaben“ bezieht sich auf den Vorsatz (Schmerzen oder Probleme).'),
    'A4 S1': ('O5', [], 'X', 0, 'A und B gleich, O5 vor dem Quantor.'),
    'A4 S2': ('O5', [], 'X', 0, 'A und B gleich (gültige Versuche nach O5).'),
    'A5 S1': ('X1', [], 'X', 0, 'A und B gleich. Tab. 3 enthält Ausgangs-, Post- und Differenzwerte, kein reiner Orientierungsinhalt (wie Negra 2020 1.3).'),
    'A5 S2': ('X1', ['Z1'], 'X', 0, 'A und B gleich, Klarstellung Z1 (X1 auf eine Einzelwertdarstellung). Abb. 2 zeigt jeden Spieler, die Modellgrafik ist keine Responderdarstellung, der Sekundärcode folgt dem Wortlaut der Klarstellung.'),
    'A5 S3': ('B1', [], 'X', 0, 'A und B gleich. Der Quantor reicht über die drei konfirmatorischen, nicht über alle sieben Zielgrößen (Klarstellung B4).'),
    'A5 S4': ('B1', [], 'S', 0, 'A B1, B B1 mit V2. Nach A: „Adjustiert für Ausgangswert und Reifestatus“ benennt den Schätzer, die Modellentscheidung steht in 4.7. Im Korpuskonsens trägt Hilska 3.3 (unadjustierte und adjustierte IRR) kein V2.'),
    'A5 S5': ('B1', [], 'C+J', 0, 'A und B gleich, zwei Kategorien nach der Klarstellung zu zg.'),
    'A5 S6': ('B1', [], 'X', 0, 'A B1, B B4 mit B1. Nach A: „damit“ bindet „keiner Zielgröße“ an die drei geprüften konfirmatorischen, der Quantor erfasst nicht alle Zielgrößen der Studie (Klarstellung B4). B entschied nach dem Wortlaut und nannte den Satz den schwierigsten Fall, die Lesart nach dem Kontext erwog B selbst.'),
    'A5 S7': ('B1', [], 'X', 0, 'A und B gleich, „jedes Intervall“ reicht über drei Intervalle.'),
    'A5 S8': ('B1', [], 'X', 0, 'A B4 mit B1, B B1. Nach B: kein Quantor über alle Zielgrößen der Studie, keine vollständige Liste, keine Hypothesenentscheidung (Regel 5 „B4 nur nach seiner Definition“). „Die Befunde“ meint die drei berichteten. Gleiche Lesart wie A5 S6.'),
    'A5 S9': ('B1', [], 'X', 0, 'A und B gleich. Die Entscheidungsregel wird geprüft, entschieden wird erst in S10.'),
    'A5 S10': ('B4', ['B1'], 'X', 0, 'A und B gleich, Entscheidung über die Hypothese (Definition B4).'),
    'A5 S11': ('V2', [], 'S+C', 0, 'A und B gleich. Der Satz nennt nur, wie die übrigen Zielgrößen behandelt wurden, Verweis in der Klammer (Regel 1).'),
    'A6 S1': ('V1', [], 'S', 0, 'A und B gleich.'),
    'A6 S2': ('Z1', ['B1'], 'S', 0, 'A und B gleich. Kein V2 für „nachträglich festgelegt“ (Zeitpunkt, keine Regel).'),
    'A6 S3': ('V1', [], 'X', 0, 'A und B gleich.'),
    'A6 S4': ('Z1', ['B1', 'V2'], 'X', 0, 'A Z1 mit B1, B Z1 mit B1 und V2. Nach B: „Soweit die Fallzahl eine Inferenz zuließ“ nennt die Regel, unter acht Spielern je Gruppe keine Inferenz (V2 „Schwellen“).'),
}

# Hinweise je Satz (Wortlaut erfasst den Satz), unabhängig davon, ob sie den Code ändern
HINWEIS = {
    'A1 S4': ['H3'], 'A3 S1': ['H8'], 'A3 S2': ['H8'], 'A3 S3': ['H6'], 'A3 S4': ['H6'],
    'A4 S1': ['H3', 'H7'], 'A4 S2': ['H7'],
    'A5 S3': ['H2'], 'A5 S6': ['H2', 'H4'], 'A5 S7': ['H2', 'H4'], 'A5 S8': ['H2', 'H4'], 'A5 S9': ['H2'],
    'A5 S10': ['H1'], 'A5 S11': ['H9'], 'A6 S2': ['H5'], 'A6 S4': ['H2', 'H4', 'H5'],
}

# Fassung nach den Hinweisen: nur Abweichungen von K
KH_ABW = {
    'A5 S3': ('B4', ['B1'], 'X', 0, 'H2: Quantor „Alle“ über die drei konfirmatorischen Zielgrößen.'),
    'A5 S6': ('B4', ['B1'], 'X', 0, 'H2: „Bei keiner Zielgröße“ über die drei konfirmatorischen.'),
    'A5 S7': ('B4', ['B1'], 'X', 0, 'H2: „Jedes Intervall“ über die drei konfirmatorischen, H4 deutung 0.'),
    'A5 S8': ('B4', ['B1'], 'X', 0, 'H2: „Die Befunde“ über die drei konfirmatorischen, H4 deutung 0 („unschlüssig“ ist Fall C1).'),
    'A5 S9': ('B4', ['B1'], 'X', 0, 'H2: „Keine adjustierte Differenz“ über die drei konfirmatorischen.'),
    'A6 S4': ('Z1', ['B4', 'V2'], 'X', 0, 'H5 Z1 primär. H2: Die Einordnung und „keine davon … p < 0,05“ gelten für alle konfirmatorischen Zielgrößen, Sekundärcode B4 (die Art B1 steckt im B4, höchstens zwei Sekundärcodes). Lesart ohne H2 für diesen Satz: Z1 mit B1 und V2 (Quantor über Analysen, nicht über Zielgrößen, so B).'),
}
KH = {s: (KH_ABW[s] if s in KH_ABW else K[s]) for s in K}

ORDNUNG = list(K.keys())

if __name__ == '__main__':
    aus = sys.argv[1] if len(sys.argv) > 1 else 'konsens_2a.csv'
    with open(aus, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=chr(59))
        w.writerow(['satz', 'primaer', 'sekundaer', 'zg', 'deutung', 'primaer_hinweis', 'sekundaer_hinweis', 'hinweise',
                    'grund', 'grund_hinweis'])
        for s in ORDNUNG:
            p, sec, zg, d, g = K[s]
            ph, sech, _, _, gh = KH[s]
            w.writerow([s, p, '+'.join(sec), zg, d, ph, '+'.join(sech), '+'.join(HINWEIS.get(s, [])), g,
                        gh if s in KH_ABW else ''])
    print('Sätze:', len(K), '· von Hinweisen erfasst:', len(HINWEIS), '· Code nach Hinweis anders:', len(KH_ABW))

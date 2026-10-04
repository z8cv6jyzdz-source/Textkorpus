# -*- coding: utf-8 -*-
"""
codes_A.py — Codierung A des Textstands von Kapitel 5 (Ersteller des Abgleichs), Schritt 2 (a), 03.10.2026

Nach `03_Skripte\\Argumentationsstruktur_Ergebnisteile_2026-10-02\\codebook.md` (Fassung 2), ohne die Anwendungshinweise
der Übergabe § 5 Nr. 3. Festgelegt vor Kenntnis der Codierung B. Der Ersteller kannte die Hinweise aus der Lektüre der
Übergabe, er hat sie beim Codieren nicht angewandt (Offenlegung im Befund § 3.1). Satznummern wie textstand_saetze.md.
Je Satz: Primärcode, Sekundärcodes (höchstens zwei), Zielgröße (zg), Deutung (0 oder 1), Notiz.
Ohne Semikolon im Skript (chr(59)).
"""

A = {
    'A1 S1': ('X1', ['O1'], '', 0, 'Objekt als Subjekt, beschreibt den Teilnehmerfluss (Muster Hilska 1.1, Aloui 1.1)'),
    'A1 S2': ('O1', [], '', 0, 'Zahl der Eingangsgetesteten und der Analysierten'),
    'A1 S3': ('X1', ['O4'], 'X', 0, 'zwei Objekte als Subjekt, Inhalt Ausgangswerte aller Zielgrößen'),
    'A1 S4': ('O4', [], 'X', 0, 'Ausgangsvergleich (Regel 2), der Quantor ändert die Funktion nicht'),
    'A2 S1': ('O2', [], '', 0, 'Meldungen nach Status, Median, Klammerverweis (Regel 1)'),
    'A2 S2': ('O2', [], '', 0, 'Umsetzungsrate'),
    'A2 S3': ('O2', [], '', 0, 'Spieler an den Schwellen sechs und neun'),
    'A2 S4': ('O2', ['V2'], '', 0, 'Untergrenzen mit Zählregel im Satz'),
    'A3 S1': ('O3', [], '', 0, 'CR-10 der als vollständig gemeldeten Einheiten'),
    'A3 S2': ('O3', [], '', 0, 'sRPE-Load'),
    'A3 S3': ('Z2', ['O2'], '', 0, 'Meldungen mit Schmerzangabe, Status der Einheiten ohne Grundzuschreibung'),
    'A3 S4': ('Z2', [], '', 0, 'keine Angaben zu Schäden in der Kontrollgruppe'),
    'A4 S1': ('O5', [], 'X', 0, 'typischer Messfehler gegen SESOI, Quantor über alle Zielgrößen bleibt O5'),
    'A4 S2': ('O5', [], 'X', 0, 'gültige Versuche je Gruppe, drei Kategorien'),
    'A5 S1': ('X1', [], 'X', 0, 'Objekt als Subjekt, ohne Befund'),
    'A5 S2': ('X1', ['Z1'], 'X', 0, 'Objekt als Subjekt, ein Punkt je Spieler (Einzelwerte, Klarstellung Z1)'),
    'A5 S3': ('B1', [], 'X', 0, 'Quantor nur über die drei konfirmatorischen, nicht über alle Zielgrößen der Studie (Klarstellung B4)'),
    'A5 S4': ('B1', [], 'S', 0, 'adjustierte Differenz mit KI und p'),
    'A5 S5': ('B1', [], 'C+J', 0, 'zwei Zielgrößen mit Einzelwerten (Regel 5)'),
    'A5 S6': ('B1', [], 'X', 0, 'Nullbefund über die drei konfirmatorischen, kein B4 nach der Klarstellung'),
    'A5 S7': ('B1', [], 'X', 0, 'Einordnung der Intervalle, vorab definierte Schwelle, keine Deutung'),
    'A5 S8': ('B4', ['B1'], 'X', 0, 'Gesamturteil über die Befunde'),
    'A5 S9': ('B1', [], 'X', 0, 'Prüfung der Entscheidungsregel an den adjustierten Differenzen'),
    'A5 S10': ('B4', ['B1'], 'X', 0, 'Entscheidung über die Hypothese (Definition B4)'),
    'A5 S11': ('V2', [], 'S+C', 0, 'Analyseregel: nur beschrieben, Klammerverweis'),
    'A6 S1': ('V1', [], 'S', 0, 'verworfene Voraussetzung mit Prüfgröße und p'),
    'A6 S2': ('Z1', ['B1'], 'S', 0, 'Bootstrap-Intervall als Zusatzanalyse zur adjustierten Differenz'),
    'A6 S3': ('V1', [], 'X', 0, 'übrige Prüfungen nicht verworfen'),
    'A6 S4': ('Z1', ['B1'], 'X', 0, 'Per-Protokoll und Sensitivität, Quantor über die Analysen'),
}

if __name__ == '__main__':
    import hashlib
    print('Sätze:', len(A))
    print('MD5 dieser Datei:', hashlib.md5(open(__file__, 'rb').read()).hexdigest())

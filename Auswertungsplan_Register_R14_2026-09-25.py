# -*- coding: utf-8 -*-
"""
Auswertungsplan_Register_R14_2026-09-25.py — Register § 5.10 des Auswertungsplans um R14 ergänzen
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24, Schritt 2.3 (Register)

Zweck: Die Verfasserentscheidung vom 25.09.2026 zum Erratum von Khamis und Roche (1995) als nachträgliche
Festlegung eintragen: Das Erratum wird nicht beschafft, O1 (Tab. 1 der Originalpublikation 1994) ist
endgültig, die Rechnung wird aus diesem Grund nicht wiederholt. Kopfkasten und Einleitung von § 5.10
werden nachgezogen. Jede Textstelle wird genau einmal ersetzt, sonst bricht das Skript ab.
Aufruf: python Auswertungsplan_Register_R14_2026-09-25.py <Auswertungsplan.md> <Rechercheprotokoll.md>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

MD, PROT = sys.argv[1], sys.argv[2]
s = open(MD, encoding='utf-8').read()
prot = open(PROT, encoding='utf-8').read()
if 'doi 10.1542/peds.95.3.457' not in prot:
    raise SystemExit('Rechercheprotokoll ohne DOI des Erratums, Register nicht ergänzt')
if 'errors in Tables 1 and 2' not in prot:
    raise SystemExit('Rechercheprotokoll ohne Crossref-Wortlaut, Register nicht ergänzt')


def ersetze(alt, neu):
    global s
    if s.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:70])
    s = s.replace(alt, neu)


ersetze('> **Nachtrag 25.09.2026 (Phase 6):** Das Register § 5.10 trägt die Zeilen R9 bis R13: Festlegungen aus der Blindrechnung (R9), Gegenprobe als neue Fassung der Python-Kette mit bestandenem Abgleich je Kennung (R10), eine Korrektur mit altem und neuem Ergebnis zur Berechnung des Reifestatus (R11), die Handprobe 6.3 als Excel-Formelprobe (R12) und Nachtrag 3 zur Spezifikation (R13). Nachweise: `02_Befunde\\Abgleichprotokoll_2026-09-25`, `Durchsichtsprotokoll_2026-09-25`, `Plausibilitaetsprotokoll_2026-09-25`, `03_Skripte\\Handprobe_Pruefung_2026-09-25.txt`, `02_Befunde\\Blindpruefung_Spezifikation_2026-09-24` (dritter Lauf).',
        '> **Nachtrag 25.09.2026 (Phase 6 und 7):** Das Register § 5.10 trägt die Zeilen R9 bis R14: Festlegungen aus der Blindrechnung (R9), Gegenprobe als neue Fassung der Python-Kette mit bestandenem Abgleich je Kennung (R10), eine Korrektur mit altem und neuem Ergebnis zur Berechnung des Reifestatus (R11), die Handprobe 6.3 als Excel-Formelprobe (R12), Nachtrag 3 zur Spezifikation (R13) und die Verfasserentscheidung, das Erratum zu Khamis und Roche nicht zu beschaffen (R14, O1 endgültig). Nachweise: `02_Befunde\\Abgleichprotokoll_2026-09-25`, `Durchsichtsprotokoll_2026-09-25`, `Plausibilitaetsprotokoll_2026-09-25`, `03_Skripte\\Handprobe_Pruefung_2026-09-25.txt`, `02_Befunde\\Blindpruefung_Spezifikation_2026-09-24` (dritter Lauf), `05_Protokolle\\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25`.')
ersetze('Die Einträge R1 bis R8 hat der Verfasser am 24.09.2026 entschieden, R9 bis R13 kamen am 25.09.2026 aus der Blindrechnung, dem Abgleich, der Handprobe und der Code-Durchsicht (Phase 6), alle ohne Rücksprache mit dem Betreuer.',
        'Die Einträge R1 bis R8 hat der Verfasser am 24.09.2026 entschieden, R9 bis R13 kamen am 25.09.2026 aus der Blindrechnung, dem Abgleich, der Handprobe und der Code-Durchsicht (Phase 6), R14 ist die Verfasserentscheidung vom 25.09.2026 zum Erratum von Khamis und Roche, alle ohne Rücksprache mit dem Betreuer.')
R14 = ('| R14 | Reifestatus endgültig nach Tab. 1 der Originalpublikation von Khamis und Roche (1994), O1 und O2 unverändert (Verfasser 25.09.2026). Das Erratum (Pediatrics 95(3), 457, 1995, doi 10.1542/peds.95.3.457) wird nicht beschafft. Es ist nur über die Bibliothek erreichbar, die Recherche über PubMed, Crossref, Unpaywall und den Verlag blieb ohne Volltext (`05_Protokolle\\Rechercheprotokoll_Erratum_Khamis_Roche_2026-09-25`). Der Vorbehalt aus O1 und L12, die Rechnung bei einem Treffer im Erratum zu wiederholen, entfällt | ergänzt R4 (O1) und schließt L12 der Maßnahmenliste | Das Erratum korrigiert nach Crossref „Tables 1 and 2“ der Originalpublikation. Ohne Volltext ist nicht bekannt, ob verwendete Koeffizientenzeilen betroffen sind und in welche Richtung ein Fehler die Kovariate je Altersjahr verschieben würde. Alle Spieler wurden nach derselben Tabelle und Regel berechnet, der Reifestatus ist Kovariate, nicht Zielgröße. Gearbeitet wird mit dem vorliegenden Stand (Verfasser 25.09.: „damit arbeiten, was wir aktuell haben“) | 4.3 und 4.7 als Einschränkung (Koeffizienten der Originalpublikation, Erratum nicht eingesehen), 6.3 (G2, Restkonfundierung über die Kovariate) |')
marker = '\n\n*Tab. 6.* In der ersten Rechnung enthalten, künftig nicht gerechnet und nicht berichtet'
ersetze(marker, '\n' + R14 + marker)
if chr(59) in R14:
    raise SystemExit('Semikolon im neuen Eintrag')
with open(MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)
print('Register ergänzt: R14, Kopfkasten und § 5.10 nachgezogen')

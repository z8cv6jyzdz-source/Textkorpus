# -*- coding: utf-8 -*-
"""Steuerung_Rev135_2026-09-30.py — Fortschreibung der Steuerung nach der Recherche videobasiertes Training.

Rev. 135 (30.09.2026): Teil 0 der Sitzungsnotizen (Stand-Zeile, neuer Block vor Rev. 134) und
Maßnahmenliste (Stand-Zeile, H13 neu nach H12, G37 (m), Taskzuordnung, Summe).
Liest die frisch gestagten Fassungen, prüft deren MD5 gegen den Stand von Rev. 134 und schreibt
beide Dateien in einen eigenen, frischen Ausgabeordner. Jede Ersetzung ist per Assertion auf genau
eine Fundstelle geprüft. Ausgabe der Prüfsummen in Steuerung_Rev135_2026-09-30.txt.

Aufruf: python Steuerung_Rev135_2026-09-30.py <Ordner mit den gestagten Dateien> <Ausgabeordner> <Uhrzeit HH:MM>
"""
import hashlib
import os
import sys

EIN, AUS, UHR = sys.argv[1], sys.argv[2], sys.argv[3]
SN = 'Cowork_Sitzungsnotizen.md'
ML = 'Massnahmenliste_Datenverarbeitung.md'
ERWARTET = {SN: '0a24966a8f7498739141d3537fdae1d1', ML: 'df77f62de743fddb7c9c11109f6bf950'}

def md5(b):
    return hashlib.md5(b).hexdigest()

def lesen(name):
    b = open(os.path.join(EIN, name), 'rb').read()
    assert md5(b) == ERWARTET[name], (name, md5(b))
    return b.decode('utf-8')

def ersetze(t, alt, neu):
    n = t.count(alt)
    assert n == 1, (n, alt[:120])
    return t.replace(alt, neu)

protokoll = []

# ---------------------------------------------------------------- Sitzungsnotizen
sn = lesen(SN)
sn = ersetze(sn, '**Stand: (Rev. 134 — siehe Block oben.) Zuvor: ',
             '**Stand: (Rev. 135 — siehe Block oben.) Zuvor: (Rev. 134 — siehe Block oben.) Zuvor: ')

BLOCK = f"""### ⭐⭐ NEU (Rev. 135, 30.09.2026, {UHR} Sitzungsuhr, Auftrag 20:27): Recherche videobasiertes Training (Sportler, Plyometrie, Fußball) — Befund im Hausstil, Folgen für 12a, 12b, 13b, die Schlussfassung der Einleitung und G37

**Auftrag (Verfasser, 30.09., 20:27, wörtlich):** „suche gezielt nach studien, die videobsiertes Training für Sportler untersucht. Weite im zweiten Schritt deine Recherche explizit auf Plyometrisches Training aus. Besonders relevant sind Studien mit fußballbezug. Es soll herausgefunden werden, wie gut das videobasierte Training untersucht worden ist und ob die Wirksamkeit untersucht wurde. orientiere dich an den von mir genutzten Forschungsfragen“

**Einordnung:** Lief neben Rev. 134 (Entscheidung 20:33 bis 20:50 in einer anderen Sitzung). Die Recherche ändert keinen Manuskripttext und keine Reihenfolge, sie liefert Stoff für die Tasks nach Rev. 134.

**Vorgehen:** Suchrahmen nach der Forschungsfrage des Ethikantrags (PDF-S. 3 f.) in drei Stufen: Sportler, Plyometrie, Fußball. Consensus-Fragen K11 bis K13 im Stil des Rechercheprotokolls vom 02.09. (danach Monatskontingent erschöpft, Neustart 01.10.), PubMed P1 bis P11 mit 517 gesichteten Treffern, Unpaywall und Verlagsseiten. Ein unabhängiger Subagent versuchte vier Kernaussagen zu widerlegen. Die Schlussprüfung an den PubMed-Abstracts berichtigte mehrere Angaben, darunter Guo et al. (2025, visuelles Training allgemein, nicht „video-based“), die Satzbezüge auf den freigegebenen Wortlaut der Einleitung und Pucsok et al. (2021, Nicht-aufnehmen-Liste nach F17 § 6.5).

**Ergebnis (Befund § 0):** (1) „Video-based training“ meint überwiegend Wahrnehmungs- und Entscheidungstraining (gut untersucht) oder Technikrückmeldung (kleine Laborstudien). (2) Video als Vermittlungsweg eines Trainingsprogramms, der Sinn der Arbeit, ist bei Sportlern dünn untersucht: eine kleine RCT mit Kontrollgruppe ohne Programm und Sprint- und Sprungzielgrößen (Klusemann et al., 2012, Nachwuchsbasketball, sechs Wochen), wenige Vergleiche digitaler mit betreuter Vermittlung, sonst unkontrollierte Lockdown-Studien. Keine SR/MA für Sportler, für ältere Erwachsene Adliah et al. (2025). (3) Die Wirksamkeit ist nur in kleinen Einzelstudien geprüft. Bei Sprung, Sprint oder Agilität unterschieden sich digitale oder unbeaufsichtigte und betreute Durchführung nicht, Aufsicht verbesserte Umsetzung, Kraft und Bewegungsqualität. (4) Plyometrie: ein kontrolliertes, per App vermitteltes, unbeaufsichtigtes Heimprogramm (Dos Santos et al., 2025, erwachsene Handballer, aktive Kontrolle, rund 50 % Umsetzung). Keine Metaanalyse wertet Aufsicht oder Vermittlungsweg aus. (5) Fußball: keine kontrollierte Studie zu einem videobasierten Heimprogramm mit den Zielgrößen der Arbeit im Nachwuchs, am nächsten Veith et al. (2021, 11+ Teil 2 zu Hause, Akademie, laufende Saison). (6) Keine Studie unter der Distanzsumme 3 (F17 § 6.4).

**Folgen (Befund § 5):** Schlussfassung der Einleitung: Lückenformel „in kontrollierten Studien unzureichend untersucht“ (B4 S7) gestützt, „fehlen“ nicht, kein neuer Satz, Prüfstoff für Prüfkatalog (b) · G37 (m): F17 § 6.5 Korpuslücke mit Zusatz, Liu-Formel „einzige“ einschränken (Nakamura et al., 2012), „fehlen“ in § 5a Zug 7 und Raster Zeile 1.3 angleichen · Task 12a: Umsetzungsraten unbeaufsichtigter digitaler Programme als Spanne, Klusemann et al. (2012) als Präzedenzfall erst nach dem Volltext · Task 12b: G3 (Aufsicht, Vorbild ohne Rückmeldung) und G8 (Übertragbarkeit) · Task 13b: englisch „video-guided“ oder „video-delivered home training“, deutsch bleibt „videobasiert“ · Beschaffung H13.

**Offen beim Verfasser:** H13 Priorität 1: Klusemann et al. (2012) über die DSHS, Veith et al. (2021) und Dos Santos et al. (2025) frei. Sonst wie Rev. 134.

**Stand der Dateien:** Neu: `02_Befunde\\Recherche_Videobasiertes_Training_2026-09-30` als .md (34.479 Byte, MD5 `13531813…`), .docx und .pdf (15 Seiten, Hausstil), Projektkopie `claude/` · `03_Skripte\\Recherche_Videobasiertes_Training_2026-09-30\\` mit `Recherche_Hausstil_2026-09-30.py`, `suchprotokoll_2026-09-30.json` und `titelliste_2026-09-30.csv` · `03_Skripte\\Steuerung_Rev135_2026-09-30.py` mit `.txt`. Geändert: diese Notizen (Rev. 135 auf Rev. 134) · Maßnahmenliste (Stand, H13 neu, G37 (m), Taskzuordnung, Summe), je Ordner und Projektkopie. Durch diesen Task unverändert: Master, Fassung 17, Plan, Gliederung v6, Berichtsraster, Textvorschläge, T1, T4. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** wie Rev. 134: Task 11 (Kapitel 5) nach der Meldung der Übertragung.

"""
ANKER = '### ⭐⭐ NEU (Rev. 134, 30.09.2026, 20:50 Sitzungsuhr'
sn = ersetze(sn, ANKER, BLOCK + ANKER)
assert ';' not in BLOCK

# ---------------------------------------------------------------- Maßnahmenliste
ml = lesen(ML)
ml = ersetze(ml, '**Stand 30.09.2026, 20:50 Sitzungsuhr (Rev. 134 —',
             f'**Stand 30.09.2026, {UHR} Sitzungsuhr (Rev. 135 — Recherche videobasiertes Training: Befund '
             '`02_Befunde\\Recherche_Videobasiertes_Training_2026-09-30` (.md, .docx, .pdf), H13 und G37 (m) neu, '
             'Taskzuordnung ergänzt). Zuvor 30.09.2026, 20:50 Sitzungsuhr (Rev. 134 —')

H13 = ('- [ ] **H13 · Beschaffungsposten aus der Recherche videobasiertes Training (30.09., Befund '
       '`02_Befunde\\Recherche_Videobasiertes_Training_2026-09-30` § 6):** Priorität 1 für 6.1 und 6.3: '
       'Klusemann et al. (2012, JSCR 26(10), 2677–2684, doi 10.1519/JSC.0b013e318241b021, DSHS) · '
       'Veith et al. (2021, Sci Med Footb 5(4), 339–346, doi 10.1080/24733938.2021.1874616, Einreichungsfassung frei bei der Universität Bath) · '
       'Dos Santos et al. (2025, Appl Sci 15(24), 13108, doi 10.3390/app152413108, frei, MDPI, Zitierfalle Autorenreihenfolge). '
       'Priorität 2: Nakamura et al. (2012, schon in H12 Stufe 2, jetzt auch für G37 m) · Smart & Gill (2013) und Coutts et al. (2004) für 6.3 G3. '
       'Priorität 3 nur bei Bedarf: Lippi et al. (2025), Dauty et al. (2021), Stanković et al. (2022, frei beim Verlag). '
       'Frei über PMC gelesen, ablegen nur, falls zitiert: Rogers et al. (2020), Paludo et al. (2022), Keemss et al. (2022). '
       'Pucsok et al. (2021) bleibt auf der Nicht-aufnehmen-Liste. Vor jeder Zitation T1-Steckbrief und T4-Prüfung. *(Sitzung 30.09., Rev. 135)*')
assert ';' not in H13
zeilen = ml.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **H12 · ')]
assert len(idx) == 1
zeilen.insert(idx[0] + 1, H13)
ml = '\n'.join(zeilen)

G37 = (' *(Rev. 135, 30.09.: (m) neu aus der Recherche videobasiertes Training, Befund § 5 Nr. 2, für Fassung 18 und Raster Rev. 4: '
       'F17 § 6.5, Korpuslücke: „Keine erfasste Interventionsstudie war unbeaufsichtigt, videobasiert oder gerätefrei“ gilt für den '
       'Vergleichskorpus und bleibt, mit dem Zusatz, dass außerhalb des Korpus vereinzelte, populationsferne Studien existieren · '
       '„Liu et al. (2024) bleibt die einzige kontrollierte Studie mit plyometrischem Arm in der Übergangsperiode“ einschränken, etwa '
       '„die einzige gefundene im Nachwuchsfußball“ (Nakamura et al., 2012: Nachsaison, Plyometrie gegen Kontrolle ohne Training, Alter am '
       'Volltext prüfen) · Lückenformel „fehlen“ in F17 § 5a Zug 7 und Raster Zeile 1.3 an „unzureichend untersucht“ angleichen, wie '
       'B4 S7 des freigegebenen Wortlauts.)*')
assert ';' not in G37
zeilen = ml.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **G37 · ')]
assert len(idx) == 1
zeilen[idx[0]] = zeilen[idx[0]] + G37

def zeile_anhaengen(anfang, zusatz):
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(anfang)]
    assert len(treffer) == 1, (anfang, treffer)
    z = zeilen[treffer[0]]
    assert z.endswith(' |'), z[-40:]
    zeilen[treffer[0]] = z[:-2] + zusatz + ' |'

zeile_anhaengen('| 7 neu: Einleitung neu', ' · Recherche videobasiertes Training § 5 Nr. 1 (Rev. 135, Prüfkatalog b)')
zeile_anhaengen('| 12 Kapitel 6', ' · H13 · Recherche videobasiertes Training § 5 Nr. 3 (12a) und Nr. 4 (12b)')
zeile_anhaengen('| 13 Kapitel 7, Zusammenfassung, Abstract', ' · Recherche videobasiertes Training § 5 Nr. 5 (13b, englisch „video-guided“)')
zeile_anhaengen('| 18 Endredaktion', ' · einheitlich „videobasiert“ (Recherche videobasiertes Training § 5 Nr. 5)')
zeile_anhaengen('| Beschaffung (Verfasser, neben den Tasks)', ' · H13')
ml = '\n'.join(zeilen)
ml = ersetze(ml, '| **Summe** | Rev. 117 (29.09., Sitzung 28.09.):',
             '| **Summe** | Rev. 135 (30.09.): H13 und G37 (m) neu, Zählung nicht neu erhoben. Zuvor: Rev. 117 (29.09., Sitzung 28.09.):')

# ---------------------------------------------------------------- schreiben
os.makedirs(AUS, exist_ok=True)
for name, text in ((SN, sn), (ML, ml)):
    b = text.encode('utf-8')
    open(os.path.join(AUS, name), 'wb').write(b)
    protokoll.append(f'{name}: {len(b)} Byte, MD5 {md5(b)} (vorher {ERWARTET[name]})')
protokoll.append(f'Uhrzeit (Sitzungsuhr): {UHR}')
open(os.path.join(AUS, 'Steuerung_Rev135_2026-09-30.txt'), 'w', encoding='utf-8').write('\n'.join(protokoll) + '\n')
print('\n'.join(protokoll))

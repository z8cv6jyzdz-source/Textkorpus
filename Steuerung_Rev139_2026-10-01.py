# -*- coding: utf-8 -*-
"""Steuerung_Rev139_2026-10-01.py — Fortschreibung der Steuerung nach der Recherche videobasiertes Training im Nachwuchssport.

Rev. 139 (01.10.2026): Teil 0 der Sitzungsnotizen (Stand-Zeile, neuer Block vor Rev. 138) und
Maßnahmenliste (Stand-Zeile, H14 neu nach H13, Taskzuordnung, Summe).
Liest die frisch gestagten Fassungen, prüft deren MD5 gegen den Stand nach Rev. 138 (Notizen) und
Rev. 137 (Maßnahmenliste) und schreibt beide Dateien in einen eigenen, frischen Ausgabeordner.
Jede Ersetzung ist per Assertion auf genau eine Fundstelle geprüft. Prüfsummen in Steuerung_Rev139_2026-10-01.txt.
Muster: Steuerung_Rev135_2026-09-30.py.

Aufruf: python Steuerung_Rev139_2026-10-01.py <Ordner mit den gestagten Dateien> <Ausgabeordner> <Uhrzeit HH:MM>
"""
import hashlib
import os
import sys

EIN, AUS, UHR = sys.argv[1], sys.argv[2], sys.argv[3]
SN = 'Cowork_Sitzungsnotizen.md'
ML = 'Massnahmenliste_Datenverarbeitung.md'
ERWARTET = {SN: 'b5f5124145e56a5f8eda2aeb8fb6661c', ML: '8067be47b9e5b72a00398530fe8a9f3c'}


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
sn = ersetze(sn, '**Stand: (Rev. 138 — siehe Block oben.) Zuvor: ',
             '**Stand: (Rev. 139 — siehe Block oben.) Zuvor: (Rev. 138 — siehe Block oben.) Zuvor: ')

BLOCK = f"""### ⭐⭐ NEU (Rev. 139, 01.10.2026, {UHR} Sitzungsuhr, Auftrag 07:18): Recherche videobasiertes Training im Nachwuchssport (Wirkung auf Sprint, Richtungswechsel und Sprung, Adhärenz) mit zwei geprüften PubMed-Suchstrings — Befund im Hausstil, H14 neu

**Auftrag (Verfasser, 01.10., 07:18, wörtlich):** „schritt 1: führe eine erneute recherche durch. Videobasiertes Training im Nachwuchssport. 1. Effekt auf die Parameter, die wir erhoben haben, 2. Adherenz während des Programms. Erstelle mir zudem jeweils einen Suchstring, mit dem ich gezielt in Pubmed recherchieren kann.“

**Einordnung:** Folgeauftrag zu Rev. 135, lief neben Rev. 137 und Rev. 138 in einer eigenen Sitzung (Rev. 138 nennt diese Recherche). „Schritt 1“: Weitere Schritte kündigt der Verfasser an. Ändert keinen Manuskripttext und keine Reihenfolge.

**Vorgehen:** Suchrahmen nach Population, Vermittlung, Vergleich und Zielgröße für zwei Fragen. PubMed über die E-Utilities (Zähltreffer, Abstracts, bibliographische Daten), Consensus K14 bis K20 (je zehn Arbeiten), Websuche, freie Volltexte. Zwei Suchstrings aus fünf Blöcken, in zwölf Varianten getestet, 95 Treffer nach Titel und Abstract gesichtet. Ein unabhängiger Subagent prüfte 18 Aussagen, die Sensitivität der Strings an je zehn selbst gefundenen Prüfstudien und drei Kernaussagen.

**Ergebnis (Befund § 0):** (1) Wirkung: Im Nachwuchssport prüft genau eine gefundene RCT ein per Video vermitteltes Programm gegen eine Kontrolle ohne Programm (Klusemann et al., 2012, Basketball, 14 bis 15 Jahre, Krafttraining, sechs Wochen: Sprung und 20 m in Video- und betreuter Gruppe um 3 bis 5 % stärker verbessert als in der Kontrolle). Vergleiche desselben Programms mit und ohne Aufsicht oder zu Hause gegen im Training fanden bei Sprung und Sprint keinen Gruppenunterschied (Coutts et al., 2004 · Haugen et al., 2015 · Veith et al., 2021 · Rogers et al., 2020), Aufsicht brachte mehr Kraft und bessere Bewegungsqualität. Richtungswechsel und Standweitsprung sind unter diesen Bedingungen bei Nachwuchssportlern nicht belegt. Keine SR/MA. (2) Adhärenz: Spanne von 12 % (Onlineeinheiten bei Schulathleten, Rogers et al., 2020) über 26 % (DVD-Heimprogramm, Thein-Nissenbaum & Brooks, 2016) und 60 % (Heimteil, Emery et al., 2007) bis 78,5 % (Lockdown-Programm einer Akademie, Sampson et al., 2021) und 84,7 % (unbeaufsichtigtes Krafttraining, Coutts et al., 2004, betreut 94,5 %), fast nur Selbstauskunft mit verschiedenen Definitionen. (3) Distanz überall ≥ 3, nur Kontext.

**Suchstrings (Befund § 4, Datei `pubmed_suchstrings_2026-10-01.txt`):** String 1 (Wirkung) 55 Treffer, String 2 (Adhärenz) 46 Treffer, zusammen 95 (01.10.2026, ohne Warnung, SHA-256 im Suchprotokoll). Fassung 2 nach der Gegenprüfung: `unsupervised[tiab]` und `young[tiab]` statt zwölf Phrasen, Prüfstudien 9 von 10 und 10 von 10 (Fassung 1: je 8 von 10 bei 45 und 40 Treffern).

**Gegenprüfung (Befund § 5):** Keine der 18 Aussagen widerlegt, zehn präzisiert und übernommen. Berichtigt gegenüber Rev. 135: Zitierjahre Lippi et al. (2026), Twist et al. (2022) und Nimmerichter et al. (2016) nach der Version of Record · Smart & Gill (2013) im Abstract ohne Zufallszuteilung, Adhärenz von den Autoren nur als mögliche Erklärung. Der Befund vom 30.09. bleibt unverändert, die Berichtigungen stehen im neuen Befund § 5.3.

**Folgen (Befund § 6):** Task 12a: Umsetzungsrate (K-10.5) als Spanne gegen die Nachwuchswerte, je mit Definition und Population (ergänzt Rev. 135 § 5 Nr. 3) · Twist et al. (2022) und Asimakidis et al. (2022) als Gegenstücke zur offenen Detraining-Richtung, erst nach dem Volltext · Task 12b (G3): höhere Teilnahme mit Aufsicht und in Präsenz, Barrieren Zeit und Vergessen, Selbstauskunft als gemeinsames Messproblem · Task 13: Live-Videoeinheiten und Gruppenaustausch nur als Forschungsempfehlung (Albino et al., 2022) · Einleitung: keine neue Folge, Lückenformel weiter gestützt · H14 neu.

**Offen beim Verfasser:** H14 Priorität 1: Sampson et al. (2021) und Emery et al. (2007) über die DSHS, Thein-Nissenbaum & Brooks (2016) frei. Schritt 2 der Recherche nach Auftrag. Sonst wie Rev. 137 und 138.

**Stand der Dateien:** Neu: `02_Befunde\\Recherche_Videobasiertes_Training_Nachwuchs_2026-10-01` als .md (40.354 Byte, MD5 `b5f700f0…`), .docx und .pdf (12 Seiten, Hausstil), Projektkopie `claude/` · `03_Skripte\\Recherche_Videobasiertes_Training_Nachwuchs_2026-10-01\\` mit `Recherche_Hausstil_2026-10-01.py`, `suchprotokoll_2026-10-01.json`, `titelliste_2026-10-01.csv` (95 Treffer mit Sichtungsurteil), `gegenpruefung_2026-10-01.json` und `pubmed_suchstrings_2026-10-01.txt` · `03_Skripte\\Steuerung_Rev139_2026-10-01.py` mit `.txt`. Geändert: diese Notizen (Rev. 139 auf Rev. 138) · Maßnahmenliste (Stand, H14 neu, Taskzuordnung, Summe), je Ordner und Projektkopie. Durch diesen Task unverändert: Master, Fassung 17, Plan, Textvorschläge, T1, T4, Befund vom 30.09. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** wie Rev. 137 und 138 (Abgleich nach der Übertragung, dann Task 12a). Dieser Eintrag ändert die Reihenfolge nicht.

"""
ANKER = '### ⭐⭐ NEU (Rev. 138, 01.10.2026, 08:03 Sitzungsuhr'
sn = ersetze(sn, ANKER, BLOCK + ANKER)
assert ';' not in BLOCK

# ---------------------------------------------------------------- Maßnahmenliste
ml = lesen(ML)
ml = ersetze(ml, '**Stand 01.10.2026, 07:41 Sitzungsuhr (Rev. 137 —',
             f'**Stand 01.10.2026, {UHR} Sitzungsuhr (Rev. 139 — Recherche videobasiertes Training im Nachwuchssport: Befund '
             '`02_Befunde\\Recherche_Videobasiertes_Training_Nachwuchs_2026-10-01` (.md, .docx, .pdf) mit zwei geprüften '
             'PubMed-Suchstrings, H14 neu, Taskzuordnung ergänzt). Zuvor 01.10.2026, 07:41 Sitzungsuhr (Rev. 137 —')

H14 = ('- [ ] **H14 · Beschaffungsposten aus der Recherche videobasiertes Training im Nachwuchssport (01.10., Befund '
       '`02_Befunde\\Recherche_Videobasiertes_Training_Nachwuchs_2026-10-01` § 7):** Priorität 1 für 6.1: '
       'Sampson et al. (2021, Sci Med Footb 5(sup1), 38–43, doi 10.1080/24733938.2021.1983203, DSHS) · '
       'Thein-Nissenbaum & Brooks (2016, WMJ 115(1), 37–42, ohne DOI, frei bei WMJ) · '
       'Emery et al. (2007, Clin J Sport Med 17(1), 17–24, doi 10.1097/JSM.0b013e31802e9c05, DSHS). '
       'Priorität 2: Twist et al. (2022, Sci Med Footb 6(3), 347–354, doi 10.1080/24733938.2021.1959944, DSHS, Detraining-Kontext für 12a) · '
       'Steffen, Meeuwisse et al. (2013, BJSM 47(8), 480–487, doi 10.1136/bjsports-2012-091887, DSHS, 12b) · '
       'Coutts et al. (2004) frei im Repositorium der UTS (steht in H13 Priorität 2). '
       'Priorität 3 nur bei Bedarf: Albino et al. (2022, DSHS), Evans & Gahreman (2023, frei), Cowley et al. (2021, frei, MDPI). '
       'Frei über PMC, ablegen nur, falls zitiert: Haugen et al. (2015), Wang et al. (2024), Edouard et al. (2021). '
       'Zitierjahr nach der Version of Record: Lippi et al. 2026 (H13 nennt 2025). '
       'Vor jeder Zitation T1-Steckbrief und T4-Prüfung, MDPI kennzeichnen. *(Sitzung 01.10., Rev. 139)*')
assert ';' not in H14
zeilen = ml.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **H13 · ')]
assert len(idx) == 1
zeilen.insert(idx[0] + 1, H14)


def zeile_anhaengen(anfang, zusatz):
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(anfang)]
    assert len(treffer) == 1, (anfang, treffer)
    z = zeilen[treffer[0]]
    assert z.endswith(' |'), z[-40:]
    zeilen[treffer[0]] = z[:-2] + zusatz + ' |'


zeile_anhaengen('| 12 Kapitel 6', ' · H14 · Recherche videobasiertes Training im Nachwuchssport (Rev. 139) § 6 Nr. 1 und 3 (12a), Nr. 2 (12b)')
zeile_anhaengen('| 13 Kapitel 7, Zusammenfassung, Abstract', ' · Recherche videobasiertes Training im Nachwuchssport (Rev. 139) § 6 Nr. 4 (Ausblick)')
zeile_anhaengen('| Beschaffung (Verfasser, neben den Tasks)', ' · H14')
ml = '\n'.join(zeilen)
ml = ersetze(ml, '| **Summe** | Rev. 135 (30.09.):',
             '| **Summe** | Rev. 139 (01.10.): H14 neu, Zählung nicht neu erhoben. Zuvor: Rev. 135 (30.09.):')

# ---------------------------------------------------------------- schreiben
os.makedirs(AUS, exist_ok=True)
for name, text in ((SN, sn), (ML, ml)):
    b = text.encode('utf-8')
    open(os.path.join(AUS, name), 'wb').write(b)
    protokoll.append(f'{name}: {len(b)} Byte, MD5 {md5(b)} (vorher {ERWARTET[name]})')
protokoll.append(f'Uhrzeit (Sitzungsuhr): {UHR}')
open(os.path.join(AUS, 'Steuerung_Rev139_2026-10-01.txt'), 'w', encoding='utf-8').write('\n'.join(protokoll) + '\n')
print('\n'.join(protokoll))

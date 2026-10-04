# -*- coding: utf-8 -*-
"""Steuerung_Rev142_2026-10-01.py — Fortschreibung der Steuerung nach Recherche Schritt 2 (Studien ähnlich Klusemann et al., 2012).

Rev. 142 (01.10.2026): Teil 0 der Sitzungsnotizen (Stand-Zeile, neuer Block vor Rev. 141) und
Maßnahmenliste (Stand-Zeile, H15 neu nach H14, Taskzuordnung, Summe).
Liest die frisch gestagten Fassungen, prüft deren MD5 gegen den Stand nach Rev. 141 und schreibt beide
Dateien in einen eigenen, frischen Ausgabeordner. Jede Ersetzung ist per Assertion auf genau eine Fundstelle
geprüft. Prüfsummen in Steuerung_Rev142_2026-10-01.txt.
Muster: Steuerung_Rev139_2026-10-01.py.

Aufruf: python Steuerung_Rev142_2026-10-01.py <Ordner mit den gestagten Dateien> <Ausgabeordner> <Uhrzeit HH:MM>
        <Byte der Befund-md> <MD5 der Befund-md> <Seiten der PDF>
"""
import hashlib
import os
import sys

EIN, AUS, UHR, MD_BYTE, MD_MD5, SEITEN = sys.argv[1:7]
SN = 'Cowork_Sitzungsnotizen.md'
ML = 'Massnahmenliste_Datenverarbeitung.md'
ERWARTET = {SN: 'f5256b0566b3bfb0eaa4f2fe984e86b8', ML: '26c1ca5bca638e4530b41fcc9c16e3e6'}


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


def tausender(z):
    return f'{int(z):,}'.replace(',', '.')


protokoll = []

# ---------------------------------------------------------------- Sitzungsnotizen
sn = lesen(SN)
sn = ersetze(sn, '**Stand: (Rev. 141 — siehe Block oben.) Zuvor: ',
             '**Stand: (Rev. 142 — siehe Block oben.) Zuvor: (Rev. 141 — siehe Block oben.) Zuvor: ')

BLOCK = f"""### ⭐⭐ NEU (Rev. 142, 01.10.2026, {UHR} Sitzungsuhr, Auftrag 15:30): Recherche Schritt 2 — Studien ähnlich Klusemann et al. (2012), videovermitteltes Training kurzer Dauer, Fußball zuerst, mit zwei geprüften PubMed-Suchstrings — Befund im Hausstil, H15 neu

**Auftrag (Verfasser, 01.10., 15:30, wörtlich):** „suche genauer und weite deine Suche aus. Plyometrie muss nicht untersucht worden sein. Video basiert ist der Fokus. Kurze Periode. Ich brauche ähnliche wie klusemann am besten im Fußball“

**Einordnung:** Schritt 2 nach Rev. 139, lief neben Rev. 140 und Rev. 141 in einer eigenen Sitzung. Ändert keinen Manuskripttext und keine Reihenfolge.

**Vorgehen:** Suchrahmen nach Klusemann et al. (2012): Vermittlung überwiegend per Video (aufgezeichnet, Plattform, App oder live), jedes körperliche Training, bis rund zwölf Wochen, Kontrolle oder Präsenz als Vergleich, Leistung als Zielgröße. PubMed über die E-Utilities mit neuem Vermittlungsblock (66 Begriffe), Titelsuche und Prüfset aus 25 Studien. Zitationssuche über OpenAlex (43 Arbeiten zitieren Klusemann et al., 4 Rogers et al.) und PubMed „Similar articles“. Zwei Such-Subagenten (Fußball, andere Sportarten) mit Websuche in acht Sprachen und Consensus K21 bis K24. Eigene Prüfung der Kernstudien an Abstract und PMC-Volltext. Ein dritter Subagent prüfte 21 Aussagen und zwei Kernaussagen (K25).

**Ergebnis (Befund § 0):** (1) Im Fußball kein Gegenstück zu Klusemann et al. (2012). Alle Suchmerkmale erfüllt nur eine kleine quasi-experimentelle Studie an 21 Futsalspielerinnen mit live per Videokonferenz angeleitetem Sprungtraining, ohne Gruppenvergleich der Veränderung (Estupiñán Corredor & Agudelo Velásquez, 2021). Ein aufgezeichnetes, unbeaufsichtigtes Videoprogramm gegen eine Kontrolle ohne Programm mit Sprint-, Sprung- oder Richtungswechseltest fand sich nicht. (2) Am nächsten im Fußball: Wilson et al. (2021, webbasiertes Nackenkraftprogramm, sechs Wochen, 15-Jährige, Mannschaftszuteilung, Kontrolle, Zielgröße Nackenkraft) · Nuttouch et al. (2023, Online- gegen Präsenz-HIIT, Profis) · Scoz et al. (2022, Videoanrufe gegen Anweisungen, Profis, retrospektiv) · Lippi et al. (2026, 11+ digital gegen Präsenz, sechs Monate). (3) Außerhalb des Fußballs bleibt Klusemann et al. (2012) nach dieser Suche die einzige RCT mit Online-Video-, Betreuungs- und Kontrollarm bei Nachwuchssportlern. Nahe: Rogers et al. (2020) · Kwapisz Dos Santos et al. (2025) · Gergüz & Aras Bayram (2023) · Wang et al. (2025). (4) Video gegen Präsenz: bei einfachen Leistungstests kein Unterschied nachweisbar, Präsenz oder Livebetreuung vorn bei Maximalkraft, Bewegungsqualität und Herz-Kreislauf-Größen, Adhärenz fallend von live über aufgezeichnet zu schriftlich und von Präsenz über App zu PDF (Daveri et al., 2022 · Gavanda et al., 2025). Distanz überall ≥ 3, nur Kontext.

**Suchstrings (Befund § 6, Datei `pubmed_suchstrings_schritt2_2026-10-01.txt`):** String F (Fußball) 76 Treffer, String A (alle Sportarten) 303 Treffer, mit Designfilter 46 und 177 (01.10.2026, ohne Warnung). Prüfset: String F 10 von 14 Fußballstudien, String A 15 von 25. Die erste Fassung des Vermittlungsblocks erfasste nur 3 von 14 und 7 von 25, daher 18 Ergänzungen.

**Gegenprüfung (Befund § 7):** 12 von 21 Aussagen bestätigt, 9 präzisiert und übernommen, keine widerlegt. Die Kernaussage „keine kontrollierte Studie im Fußball“ widerlegte der Prüfer mit der eigenen Futsalstudie, § 0 Nr. 1 ist danach neu gefasst. Die Kernaussage zu Klusemann et al. (2012) ist nicht widerlegt. Wang et al. (2025): Abstract über die Verlagsseite gelesen (randomisiert, 20 Personen, online gegen Trainerbetreuung, acht Wochen, kein Gruppenunterschied), Population nur im Volltext. Berichtigt gegenüber Rev. 135 und 139: Magliato et al. (2025) und Veeck et al. (2025) nach der Version of Record · Kwapisz Dos Santos et al. (2025) statt Dos Santos et al. (laut Crossref, am Original prüfen).

**Folgen (Befund § 8):** Einleitung [PRÜFEN]: Die Lückenformel bleibt gestützt, trägt aber nur als Kombination (unbeaufsichtigt, Sommerpause, leistungsorientierter Breitensport, Wachstumsgipfel). Wilson et al. (2021) und die Futsalstudie widerlegen weiter gefasste Formeln · Task 12a: Klusemann et al. (2012), Wilson et al. (2021) und Kwapisz Dos Santos et al. (2025) als nächste Vergleiche, nur Kontext · Task 12b (G3): Adhärenz nach Vermittlungsform · Task 13: Design nach Klusemann et al. (2012) im Nachwuchsfußball nur als Forschungsempfehlung · H15 neu.

**Offen beim Verfasser:** H15 Priorität 1: Wang et al. (2025) und Wilson et al. (2021) über die DSHS, Klusemann et al. (2012) steht schon in H13. Sonst wie Rev. 139 bis 141.

**Stand der Dateien:** Neu: `02_Befunde\\Recherche_Videobasiertes_Training_Schritt2_2026-10-01` als .md ({tausender(MD_BYTE)} Byte, MD5 `{MD_MD5[:8]}…`), .docx und .pdf ({SEITEN} Seiten, Hausstil), Projektkopie `claude/` · `03_Skripte\\Recherche_Videobasiertes_Training_Schritt2_2026-10-01\\` mit `Recherche_Hausstil_Schritt2_2026-10-01.py`, `suchprotokoll_schritt2_2026-10-01.json` (Strings, Trefferzahlen, Prüfset, PMID-Listen), `pubmed_fussball_treffer_2026-10-01.csv` (76 Treffer mit Sichtungsurteil), `pubmed_suchstrings_schritt2_2026-10-01.txt`, `suche_fussball_2026-10-01.json`, `suche_andere_2026-10-01.json` und `gegenpruefung_schritt2_2026-10-01.json` · `03_Skripte\\Steuerung_Rev142_2026-10-01.py` mit `.txt`. Geändert: diese Notizen (Rev. 142 auf Rev. 141) · Maßnahmenliste (Stand, H15 neu, Taskzuordnung, Summe), je Ordner und Projektkopie. Durch diesen Task unverändert: Master, Fassung 17, Plan, Textvorschläge, T1, T4, die Befunde vom 30.09. und 01.10. (Rev. 139). Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** wie Rev. 141. Dieser Eintrag ändert die Reihenfolge nicht.

"""
ANKER = '### ⭐⭐ NEU (Rev. 141, 01.10.2026, 16:10 Sitzungsuhr'
sn = ersetze(sn, ANKER, BLOCK + ANKER)
assert ';' not in BLOCK

# ---------------------------------------------------------------- Maßnahmenliste
ml = lesen(ML)
ml = ersetze(ml, '**Stand 01.10.2026, 16:10 Sitzungsuhr (Rev. 141 —',
             f'**Stand 01.10.2026, {UHR} Sitzungsuhr (Rev. 142 — Recherche Schritt 2, Studien ähnlich Klusemann et al. (2012): Befund '
             '`02_Befunde\\Recherche_Videobasiertes_Training_Schritt2_2026-10-01` (.md, .docx, .pdf) mit zwei geprüften '
             'PubMed-Suchstrings, H15 neu, Taskzuordnung ergänzt). Zuvor 01.10.2026, 16:10 Sitzungsuhr (Rev. 141 —')

H15 = ('- [ ] **H15 · Beschaffungsposten aus Recherche Schritt 2, Studien ähnlich Klusemann et al. (2012) (01.10., Befund '
       '`02_Befunde\\Recherche_Videobasiertes_Training_Schritt2_2026-10-01` § 9):** Priorität 1: '
       'Wang, Tsai, Tu, Wu & Chen (2025, Sport Sci Health 21(2), 969–978, doi 10.1007/s11332-025-01335-8, DSHS, Population und Vermittlungsform) · '
       'Wilson et al. (2021, JSCR 35(4), 1149–1155, doi 10.1519/JSC.0000000000002907, DSHS, Videoanteil und Adhärenz). '
       'Klusemann et al. (2012) steht in H13 Priorität 1. '
       'Priorität 2: Estupiñán Corredor & Agudelo Velásquez (2021, VIREF 10(3), 49–65, frei bei der Universidad de Antioquia) · '
       'Kwapisz Dos Santos et al. (2025, doi 10.3390/app152413108, frei, MDPI, in H13 als Dos Santos et al., Autorenname am Original prüfen). '
       'Priorität 3 nur bei Bedarf: Nuttouch et al. (2023, frei) · Gergüz & Aras Bayram (2023, DSHS) · McNamara et al. (2008, DSHS) · Bulca et al. (2022, DSHS). '
       'Frei über PMC, ablegen nur, falls zitiert: Daveri et al. (2022) · Gavanda et al. (2025) · García-Suárez et al. (2022) · Lee et al. (2021) · Yan et al. (2024). '
       'Zitierjahre nach der Version of Record: Magliato et al. 2025 und Veeck et al. 2025 (Rev. 135 und 139 nennen 2024). '
       'Vor jeder Zitation T1-Steckbrief und T4-Prüfung, MDPI kennzeichnen. *(Sitzung 01.10., Rev. 142)*')
assert ';' not in H15
zeilen = ml.split('\n')
idx = [i for i, z in enumerate(zeilen) if z.startswith('- [ ] **H14 · ')]
assert len(idx) == 1
zeilen.insert(idx[0] + 1, H15)


def zeile_anhaengen(anfang, zusatz):
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(anfang)]
    assert len(treffer) == 1, (anfang, treffer)
    z = zeilen[treffer[0]]
    assert z.endswith(' |'), z[-40:]
    zeilen[treffer[0]] = z[:-2] + zusatz + ' |'


zeile_anhaengen('| 12 Kapitel 6', ' · H15 · Recherche Schritt 2 (Rev. 142) § 8 Nr. 2 (12a), Nr. 3 (12b)')
zeile_anhaengen('| 13 Kapitel 7, Zusammenfassung, Abstract', ' · Recherche Schritt 2 (Rev. 142) § 8 Nr. 4 (Ausblick)')
zeile_anhaengen('| Beschaffung (Verfasser, neben den Tasks)', ' · H15')
ml = '\n'.join(zeilen)
ml = ersetze(ml, '| **Summe** | Rev. 141 (01.10.):',
             '| **Summe** | Rev. 142 (01.10.): H15 neu, Zählung nicht neu erhoben. Zuvor: Rev. 141 (01.10.):')

# ---------------------------------------------------------------- schreiben
os.makedirs(AUS, exist_ok=True)
for name, text in ((SN, sn), (ML, ml)):
    b = text.encode('utf-8')
    open(os.path.join(AUS, name), 'wb').write(b)
    protokoll.append(f'{name}: {len(b)} Byte, MD5 {md5(b)} (vorher {ERWARTET[name]})')
protokoll.append(f'Uhrzeit (Sitzungsuhr): {UHR}')
protokoll.append(f'Befund-md: {MD_BYTE} Byte, MD5 {MD_MD5}, PDF {SEITEN} Seiten')
open(os.path.join(AUS, 'Steuerung_Rev142_2026-10-01.txt'), 'w', encoding='utf-8').write('\n'.join(protokoll) + '\n')
print('\n'.join(protokoll))

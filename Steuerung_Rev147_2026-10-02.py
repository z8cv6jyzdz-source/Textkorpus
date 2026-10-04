# -*- coding: utf-8 -*-
"""
Steuerung_Rev147_2026-10-02.py — Fortschreibung von Teil 0 (Rev. 147) und Maßnahmenliste
Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext.

Anlass: Recherche Umsetzungsrate videogestützter Trainingsprogramme im Nachwuchs (Auftrag 02.10., 14:10 Sitzungsuhr),
Befund 02_Befunde\\Recherche_Umsetzungsrate_Videoprogramme_Jugend_2026-10-02.

Aufruf: python Steuerung_Rev147_2026-10-02.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Befund.md> <Ausgabeordner> <HH:MM>
Jede Ersetzung muss genau einmal greifen, sonst Abbruch. Schreibt beide Dateien neu in den Ausgabeordner
und ein Protokoll (Größen, MD5, Ersetzungen) nach stdout.
"""
import sys, os, hashlib

NOTIZEN, LISTE, BEFUND, AUS, UHR = sys.argv[1:6]

def md5(b):
    return hashlib.md5(b).hexdigest()

def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit(f'Abbruch: {name} greift {n}-mal statt einmal')
    protokoll.append(f'  {name}: 1 Ersetzung')
    return text.replace(alt, neu)

befund_b = open(BEFUND, 'rb').read()
befund_groesse, befund_md5 = len(befund_b), md5(befund_b)

prot = []
nb = open(NOTIZEN, 'rb').read()
lb = open(LISTE, 'rb').read()
prot.append(f'Eingang Notizen: {len(nb)} Byte, MD5 {md5(nb)}')
prot.append(f'Eingang Maßnahmenliste: {len(lb)} Byte, MD5 {md5(lb)}')
prot.append(f'Befund: {befund_groesse} Byte, MD5 {befund_md5}')
n = nb.decode('utf-8')
l = lb.decode('utf-8')

# ---------- Sitzungsnotizen ----------
n = ersetze(n, '**Stand: (Rev. 146 — siehe Block oben.)',
            '**Stand: (Rev. 147 — siehe Block oben.) Zuvor: (Rev. 146 — siehe Block oben.)', 'Notizen Stand', prot)

block = f"""### ⭐ NACHTRAG (Rev. 147, 02.10.2026, {UHR} Sitzungsuhr, Auftrag 14:10): Recherche Umsetzungsrate videogestützter Trainingsprogramme im Nachwuchs — Befund im Hausstil mit Gegenprüfung, H16 neu

**Auftrag (Verfasser, 02.10., 14:10, wörtlich):** „Lit-Recherche: Adhärenz bei einem Videogestützten Trainingsprogramm im Jugendbereich. Frage: wie ist die Umsetzungsrate bei einem videogestützten Programm.“

**Einordnung:** Nebenauftrag vor Task 12a, ändert keinen Manuskripttext und keine Reihenfolge. Ergänzt Rev. 139 § 3 und Rev. 142 § 5.2 für die Einordnung der Umsetzungsrate (K-10.5) in 6.1.

**Vorgehen:** Drei Such-Subagenten parallel (Nachwuchssportler · Kinder und Jugendliche · Übersichten) mit 62 Suchschritten in PubMed, PubMed „Similar articles“, Consensus K26 bis K30 und Websuche. Eigene Prüfung der Kernwerte an den Volltexten im Ordner (Klusemann, Rogers, Veith, Hilska), an PMC, PubMed und Crossref. Gegenprüfung durch einen vierten Subagenten ohne Kenntnis des Befunds (23 Einzelaussagen, drei Kernaussagen, Consensus K31 und K32).

**Ergebnis (Befund § 0):** (1) Für aufgezeichnete, unbeaufsichtigte Videoprogramme bei Nachwuchssportlern bis 19 Jahre weiterhin nur vier Studien mit Umsetzungswert, von 12 % (Rogers et al., 2020) bis 77 % (Klusemann et al., 2012), dazwischen 26 % der Antwortenden mit mindestens der Hälfte eines DVD-Programms (Thein-Nissenbaum & Brooks, 2016) und 76 % beim digitalen Teil eines hybriden Programms (Evans & Gahreman, 2023). (2) Nächster Vergleich ist Klusemann et al. (2012), jetzt am Volltext: gleiche Dosis (12 Einheiten in 6 Wochen), Compliance 77 % per Video gegen 96 % betreut, 5 von 13 mit allen Einheiten, 2 unter 75 % ausgeschlossen (S. 2681). (3) Übersichten: digitale Lebensstilprogramme für 10- bis 19-Jährige im Mittel 55,2 % absolvierte Programmbestandteile, bei Bewegung 62,8 % (Boumparis et al., 2026, erschienen 30.09.), trainergeleitete Präventionsprogramme 77 % (Viiala et al., 2026). Eine Übersicht zu unbeaufsichtigten Videoprogrammen bei Nachwuchssportlern fand sich nicht. (4) Kontext ohne Sportauswahl: 2,2 von 3 täglichen Videos, 23,9 % alle (Beemer et al., 2026) · YouTube-Sommerprogramm mit 91,2 % Selbstauskunft gegen 16,8 % angesehene Videolänge in nicht teilnehmergenauen Kanaldaten (Tripicchio et al., 2023). (5) In allen gefundenen direkten Vergleichen bei Nachwuchssportlern höhere Umsetzung mit Aufsicht, Rückgang über die Programmdauer, fast überall Selbstauskunft. (6) Die eigene Umsetzungsrate (K-10.5) liegt unter Klusemann et al. (2012) und den Mittelwerten der Metaanalyse, über Rogers et al. (2020), vergleichbar nur als Spanne mit Definition und Population. Distanzsumme 2 nur bei Klusemann et al. (2012).

**Gegenprüfung (Befund § 8):** 21 von 23 Einzelaussagen bestätigt, 1 präzisiert (McLaughlin et al., 2026), 1 nicht prüfbar (Prozentwerte bei Coutts et al., 2004, Richtung bestätigt), keine widerlegt. Kernaussagen C31 bis C33 nicht widerlegt, C32 nur als „in allen gefundenen direkten Vergleichen“ tragfähig, eingearbeitet.

**Folgen (Befund § 6):** Task 12a [DISKUTIEREN]: Umsetzungsrate in einem bis zwei Sätzen gegen Klusemann et al. (2012) und Rogers et al. (2020), Boumparis et al. (2026) nur mit Quellenart · Task 12b (G3, G6): Aufsicht und Selbstauskunft · Task 13: menschliche Unterstützung, Abwechslung und kürzere Videoeinheiten nur als Forschungsempfehlung · Klusemann et al. (2012) [PRÜFEN]: T1-Steckbrief und T4 vor der Zitation · H16 neu.

**Volltextstatus für Task 12a:** Rogers et al. (2020) und Veith et al. (2021) liegen seit dem 02.10. in `Ideen und Studien` (Dateizeit 13:38 und 13:42 Sitzungsuhr), Klusemann et al. (2012) seit dem 01.10. In H13 vermerkt.

**Hinweis:** Europe PMC wies einen Volltextabruf zu Tripicchio et al. (2023) wegen Ratenbegrenzung ab, die PMC-Seite war lesbar. Human Kinetics (Beemer, Rastogi) und Taylor & Francis (Sampson) blieben gesperrt.

**Offen beim Verfasser:** H16 Priorität 1: Boumparis et al. (2026), frei über PMC, nur falls 6.1 die Metaanalyse nennt. Sonst wie Rev. 146.

**Stand der Dateien:** Neu: `02_Befunde\\Recherche_Umsetzungsrate_Videoprogramme_Jugend_2026-10-02` als .md ({befund_groesse} Byte, MD5 `{befund_md5[:8]}…`), .docx und .pdf (10 Seiten, Hausstil), Projektkopie `claude/` · `03_Skripte\\Recherche_Umsetzungsrate_Videoprogramme_Jugend_2026-10-02\\` mit `Recherche_Hausstil_Umsetzungsrate_2026-10-02.py`, `suche_A_nachwuchssport.json`, `suche_B_kinder_jugend.json`, `suche_C_uebersichten.json` und `gegenpruefung_2026-10-02.json` · `03_Skripte\\Steuerung_Rev147_2026-10-02.py` mit `.txt`. Geändert: diese Notizen (Rev. 147 auf Rev. 146) · Maßnahmenliste (Stand, H13 Vermerk, H16 neu, Taskzuordnung 12 und 13, Beschaffung, Summe), je Ordner und Projektkopie. Durch diesen Task unverändert: Master, Kennzahlenblatt, Fassung 17, Plan, Textvorschläge, T1, T4, die Befunde vom 30.09. und 01.10. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** wie Rev. 146, Task 12a. Dieser Eintrag ändert die Reihenfolge nicht.

"""
anker = '### ⭐⭐ NEU (Rev. 146, 02.10.2026, 12:38 Sitzungsuhr'
n = ersetze(n, anker, block + anker, 'Notizen Block Rev. 147', prot)

# ---------- Maßnahmenliste ----------
l = ersetze(l, '**Stand 02.10.2026, 12:38 Sitzungsuhr (Rev. 146 — ',
            f'**Stand 02.10.2026, {UHR} Sitzungsuhr (Rev. 147 — Recherche Umsetzungsrate videogestützter Trainingsprogramme im Nachwuchs: Befund `02_Befunde\\Recherche_Umsetzungsrate_Videoprogramme_Jugend_2026-10-02` (.md, .docx, .pdf) mit Gegenprüfung, H16 neu, H13 und Taskzuordnung fortgeschrieben). Zuvor 02.10.2026, 12:38 Sitzungsuhr (Rev. 146 — ',
            'Liste Stand', prot)

h13_ende = 'Klusemann et al. (2012) liegt seit dem 01.10. in `Ideen und Studien` (Dateizeit 15:25 Sitzungsuhr), vor der Zitation T1-Steckbrief und T4-Prüfung. Die übrigen Posten bleiben offen.)*'
l = ersetze(l, h13_ende,
            h13_ende + ' *(Rev. 147, 02.10.: Rogers et al. (2020) und Veith et al. (2021) liegen seit dem 02.10. in `Ideen und Studien` (Dateizeit 13:38 und 13:42 Sitzungsuhr). Die Compliance-Werte von Klusemann et al. (2012) sind am Volltext belegt (S. 2681, Befund Rev. 147 § 2.1). Vor der Zitation T1-Steckbrief und T4-Prüfung, die übrigen Posten bleiben offen.)*',
            'Liste H13', prot)

h15_ende = 'Zitierjahre nach der Version of Record: Magliato et al. 2025 und Veeck et al. 2025 (Rev. 135 und 139 nennen 2024). Vor jeder Zitation T1-Steckbrief und T4-Prüfung, MDPI kennzeichnen. *(Sitzung 01.10., Rev. 142)*\n'
h16 = ('- [ ] **H16 · Beschaffungsposten aus der Recherche Umsetzungsrate videogestützter Trainingsprogramme im Nachwuchs (02.10., Befund `02_Befunde\\Recherche_Umsetzungsrate_Videoprogramme_Jugend_2026-10-02` § 7):** '
       'Priorität 1 für 6.1: Boumparis et al. (2026, Interact J Med Res 15, e84822, doi 10.2196/84822, frei über PMC13626193), nur falls 6.1 die Metaanalyse nennt. '
       'Priorität 2: Tripicchio et al. (2023, Transl Behav Med 13(1), 17–24, doi 10.1093/tbm/ibab151, frei über PMC8690196, 12b) · '
       'Johnson et al. (2020, BMJ Open 10(12), e040108, doi 10.1136/bmjopen-2020-040108, frei über PMC7757494, nur falls der Zeitverlauf genannt wird) · '
       'Viiala et al. (2026, Inj Prev 32(1), 31–40, doi 10.1136/ip-2025-045632, frei über PMC12911647, 12b). '
       'Priorität 3 nur bei Bedarf: Beemer et al. (2026, doi 10.1123/jtpe.2024-0017, DSHS) · Rastogi et al. (2025, doi 10.1123/pes.2024-0030, DSHS) · '
       'Seims et al. (2023, doi 10.1371/journal.pone.0289831, frei) · Møller et al. (2024, doi 10.1136/bjsports-2023-107880, frei). '
       'Sampson et al. (2021) und Thein-Nissenbaum & Brooks (2016) bleiben in H14. Vor jeder Zitation T1-Steckbrief und T4-Prüfung, MDPI kennzeichnen. *(Sitzung 02.10., Rev. 147)*\n')
l = ersetze(l, h15_ende, h15_ende + h16, 'Liste H16 neu', prot)

t12_ende = '· H15 · Recherche Schritt 2 (Rev. 142) § 8 Nr. 2 (12a), Nr. 3 (12b) |'
l = ersetze(l, t12_ende,
            '· H15 · Recherche Schritt 2 (Rev. 142) § 8 Nr. 2 (12a), Nr. 3 (12b) · H16 · Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 1 und 4 (12a), Nr. 2 (12b) |',
            'Liste Taskzeile 12', prot)

t13_ende = '· Recherche Schritt 2 (Rev. 142) § 8 Nr. 4 (Ausblick) |'
l = ersetze(l, t13_ende,
            '· Recherche Schritt 2 (Rev. 142) § 8 Nr. 4 (Ausblick) · Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 3 (Ausblick) |',
            'Liste Taskzeile 13', prot)

l = ersetze(l, '| Beschaffung (Verfasser, neben den Tasks) | H4 · H5 · H6 · H8 · H9 · H10 · K18 · K24 · H13 · H14 · H15 |',
            '| Beschaffung (Verfasser, neben den Tasks) | H4 · H5 · H6 · H8 · H9 · H10 · K18 · K24 · H13 · H14 · H15 · H16 |',
            'Liste Beschaffung', prot)

l = ersetze(l, '| **Summe** | Rev. 146 (02.10.): ',
            '| **Summe** | Rev. 147 (02.10.): H16 neu, H13 und Taskzuordnung 12 und 13 fortgeschrieben, Zählung nicht neu erhoben. Zuvor: Rev. 146 (02.10.): ',
            'Liste Summe', prot)

os.makedirs(AUS, exist_ok=True)
nb2, lb2 = n.encode('utf-8'), l.encode('utf-8')
open(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'), 'wb').write(nb2)
open(os.path.join(AUS, 'Massnahmenliste_Datenverarbeitung.md'), 'wb').write(lb2)
prot.append(f'Ausgang Notizen: {len(nb2)} Byte, MD5 {md5(nb2)}')
prot.append(f'Ausgang Maßnahmenliste: {len(lb2)} Byte, MD5 {md5(lb2)}')
prot.append(f'Semikola im neuen Block: {block.count(";")} · in H16: {h16.count(";")}')
print('\n'.join(prot))

# -*- coding: utf-8 -*-
"""Nachtrag T1 (Steckbriefe) und T4 (Zitierfallen) für den Task „Boumparis“, 02.10.2026.

Trägt Boumparis et al. (2026) nach der Version of Record (PMC-Volltext, PMC13626193, am 02.10.2026 gelesen) in
`Schreiben\\ev3_daten\\T1_steckbriefe.csv` ein, ergänzt ihre Zitierfallen in `T4_zitierfallen.csv` und vermerkt beim
Steckbrief Klusemann2012 die Distanz nach der Regel für Umsetzungsvergleiche (Anpassung von F17 § 6.4, Klick vom
02.10.2026, Analysebefund `02_Befunde\\Analyse_Boumparis_2026_2026-10-02` § 6.1) im Feld `evidenzsicherheit`. Die Felder
d_pop, d_dos und d_ziel bleiben in allen Zeilen die Distanz nach F17 § 6.4 (Wirksamkeit), nicht anwendbare Maße als „—“
(Zweitprüfung Nr. 10). Fassung 2 nach der Zweitprüfung (Nr. 5, 6, 10, 11, 13, 14, 21): Texte berichtigt, Klusemann-Felder
nicht mehr geändert, eine Zitierfalle zu Klusemann2012 (Bezugsmenge der 77 %) neu.

Lauf 2 (nach der Klickfreigabe des Moduls A2-M) setzt das Feld `kapitel` beider Steckbriefe nach der Entscheidung
(KAPITEL_NACH_KLICK, bis dahin leer) und bringt die eigenen Zeilen dieses Tasks (Boumparis2026 in T1 und T4) auf den
Stand des Skripts, etwa nach Befunden der Zweitprüfung. Idempotent: vorhandene Kennungen und Zitierfallen werden nicht
doppelt angelegt, Änderungen an fremden Zeilen nur, wenn der Ausgangswert passt. Format wie bisher (Semikolon-Trenner, UTF-8 mit BOM, LF,
Quoting nur bei Bedarf). Ohne Semikolon im Skript (chr(59)), die neuen Texte enthalten keins.

Aufruf: python3 T1_T4_Nachtrag_Boumparis_2026-10-02.py <Ordner mit T1_steckbriefe.csv und T4_zitierfallen.csv> <Ausgabeordner>
"""
import csv
import hashlib
import os
import sys

SEMI = chr(59)
VERMERK = '[Nachgetragen 02.10.2026, Task Boumparis]'

T1_NEU = [
    {
        'id': 'Boumparis2026',
        'kurzzitat': 'Boumparis et al. (2026)',
        'vollzitat': 'Boumparis, N., Studhalter, O., de Riedmatten, P., Yücel, I. D., Koutra, K., Champion, K., '
                     'Molina-Barceló, A., de Pablo-Pardo, T., Kondylakis, H., Schaub, M. P., Triantafyllidis, A., & '
                     'Haug, S. (2026). Factors influencing adherence to digital lifestyle interventions for adolescents: '
                     'Systematic review and meta-analysis of attrition. Interactive Journal of Medical Research, 15, '
                     'e84822. https://doi.org/10.2196/84822',
        'fassung': 'Version of Record vom 30.09.2026 (Interact J Med Res 15, e84822, PMID 42814774, PMC13626193), am '
                   '02.10.2026 als PMC-Volltext über PubMed gelesen, ohne Abbildungen und ohne Multimedia Appendix 1 '
                   '(Tab. S1 bis S18 nicht zugänglich). Im Ordner liegt nur der Preprint (JMIR Preprints, eingereicht '
                   '25.09.2025, „unpublished, peer-reviewed preprint“, Datei „2025 Boumparis et al., Factors Influencing '
                   'Adherence to Digital Lifestyle interventions for adolescence.pdf“, 1.062.847 Byte), nicht zitierfähig. '
                   'PDF der Version of Record vor dem Einbau in 6.1 ablegen, spätestens vor Task 15 (H16), bis dahin '
                   'Fundstellen nach Abschnitt und Absatz (APA 7)',
        'verlag': 'JMIR Publications — kein MDPI',
        'design': 'Systematische Übersicht nach PRISMA 2020 und SWiM über 116 Studien mit 143 Vergleichen (77 RCTs, 36 '
                  'quasi-experimentell, 3 beobachtend), Suche in PubMed, PsycINFO, CINAHL und Embase im März 2024, Update '
                  '22.06.2026. Einflussfaktoren der Adhärenz je Domäne nach Evidenzart (statistisch, beschreibend, '
                  'qualitativ) narrativ synthetisiert, nicht gepoolt. Metaanalyse (Zufallseffekte, logit-transformierte '
                  'Anteile, REML, Knapp-Hartung) nur für den Studienabbruch (108 Vergleiche aus 88 Studien). Abschlussrate '
                  'und Bestandteil-Adhärenz nur beschreibend. Kein Verzerrungsrisiko bewertet, Protokoll nicht registriert, '
                  'keine Zitationssuche',
        'population': 'Jugendliche von 10 bis 19 J. nach WHO (Studien mit einzelnen Älteren bei passendem Mittel '
                      'eingeschlossen), Alter 14,48 ± 2,07 J., 59,1 % weiblich (115 von 116 Studien mit Angabe), überwiegend '
                      'ohne Diagnose, klinisch am häufigsten Adipositas. 46.029 Teilnehmende über Interventions- und '
                      'Kontrollarme summiert, Median 52,5 je Studie. Zielgruppen Schüler, Studierende, Jugendliche außerhalb '
                      'formaler Bildung, Berufsausbildung, Jugendgruppen, klinische Gruppen, keine Sportauswahl als '
                      'Zielgruppe geführt. 26 Länder, 43,1 % der Studien aus den USA',
        'reifestatus': 'nicht berichtet',
        'dosis': 'Digitale Lebensstilprogramme mit digitaler Hauptkomponente (App 35,7 %, Web 35 %, Wearable mit Plattform '
                 '9,1 %, nur SMS 7,7 %, Computer 6,3 %, gemischt 5,6 %, VR 0,7 % der Vergleiche). Dauer Median 84 Tage (IQR '
                 '42 bis 135, Spanne 2 bis 730), persönliche Unterstützung in 50,3 % der Vergleiche, Anreize monetär oder '
                 'materiell 30,8 %, nicht monetär 14 %, keine 55,2 %. Domänen: Bewegung 32 Studien, Mehrkomponenten 31, '
                 'Adipositas 19, Tabak 14, Ernährung 10, Alkohol 10. Reine Kommunikationsplattformen (E-Mail-Coaching, '
                 'Videosprechstunden) und Einzelsitzungen ausgeschlossen, Video als Vermittlungsform nicht getrennt ausgewertet',
        'uebungskatalog': 'entfällt (Lebensstilprogramme, Bewegungsprogramme mit Aktivitätstrackern, Apps, Trainingsvideos '
                          'und anderem nicht nach Übungsinhalten beschrieben)',
        'evidenzsicherheit': 'Abschlussrate 66,9 % (SD 26 %, 68 Vergleiche), Bestandteil-Adhärenz 55,2 % (SD 25,5 %, 66 '
                             'Vergleiche), beschreibende Mittel ohne genannte Gewichtung (Results, Characteristics of Digital '
                             'Interventions, Abs. 4, und Limitations). Bewegung: Bestandteil-Adhärenz 62,8 % ohne SD und '
                             'Vergleichszahl (je Domäne 4 bis 24 Vergleiche, nach den Autoren nur hinweisend). Studienabbruch '
                             'gepoolt 16,9 % (95-%-KI 13,6 bis 20,9), I² 98,3 %, τ² 1,51 (Logit-Skala), Prognoseintervall 1,7 '
                             'bis 70,3, kein Moderator signifikant, Bewegung 14,1 % (9,9 bis 19,7, k = 32), auch diese Schätzer '
                             'nennen die Autoren beschreibend. Distanz nach F17 § 6.4 (Felder): Population 2, Dosis und '
                             'Zielgröße nicht anwendbar. Distanz nach der Regel für Umsetzungsvergleiche (Anpassung von F17 '
                             '§ 6.4, Klick 02.10.2026): Population 2 · Programmform 1 (strenger gelesen 2) · Umsetzungsmaß 1 = 4 '
                             'bis 5 → nur Kontext, Quellenart und Population im Satz. Analyse in '
                             '02_Befunde\\Analyse_Boumparis_2026_2026-10-02',
        'd_pop': '2',
        'd_dos': '—',
        'd_ziel': '—',
        'kapitel': '6.1 (Modul A2-M, Klick offen), 6.3 G3 und G6, 7 ohne Quelle, Einleitung Abs. 3 (Vormerkung '
                   'Schlussfassung)',
    },
]

# Änderungen an vorhandenen Steckbriefen: (id, Feld, erwarteter alter Wert, neuer Wert). Für `evidenzsicherheit`
# wird angehängt, wenn die Marke fehlt.
KLUSEMANN_MARKE = 'Regel für Umsetzungsvergleiche'
KLUSEMANN_ZUSATZ = (' · Für Aussagen zur Umsetzung gilt seit 02.10.2026 die Regel für Umsetzungsvergleiche (Anpassung von '
                    'F17 § 6.4, Klick im Task Boumparis): Population 2 (Basketball, gemischt) · Programmform 0 (sechs '
                    'Wochen, zwei Einheiten je Woche, Online-Videos ohne Aufsicht) · Umsetzungsmaß 0 (Anteil der Einheiten '
                    'nach Online-Tagebuch) = 2, nur mit Nennung der Abweichung im Satz. Die Felder d_pop, d_dos und d_ziel '
                    'bleiben die Distanz für Wirksamkeit (2 · 2 · 1 = 5)')
T1_AENDERN = []

# Lauf 2: Feld `kapitel` nach der Klickfreigabe des Moduls A2-M (Klick K2 am 02.10.2026: Variante A, Einleitung:
# Gegenbefund in Absatz 3)
KAPITEL_NACH_KLICK = {
    'Boumparis2026': '6.1 (Modul A2-M, Variante A, Klick K2 02.10.2026), 6.3 G3 (Verbleib überschätzt Nutzung) und '
                     'Stärken oder G6 (Berichtsempfehlung), 7 ohne Quelle, Einleitung Abs. 3 (Gegenbefund, Klick '
                     '02.10.2026, Schlussfassung)',
    'Klusemann2012': '6.3 G3 (Aufsicht, Umsetzung der Videogruppe, Klick K2 02.10.2026), nicht mehr 6.1',
}

T4_NEU = [
    ('Boumparis2026', 'Fassung: Preprint gegen Version of Record',
     'Die Datei im Ordner („2025 Boumparis et al., Factors Influencing Adherence to Digital Lifestyle interventions for '
     'adolescence.pdf“, 1.062.847 Byte) ist der Preprint aus JMIR Preprints (eingereicht 25.09.2025, Fußzeile '
     '„unpublished, peer-reviewed preprint“). Sie enthält zwei Zusammenfassungen: das Deckblatt mit dem Stand der '
     'Erstsuche (S. 3: 85 Studien, 32.397 Teilnehmende, Abschlussrate 51,85 %, Bestandteil-Adhärenz 49,35 %) und das '
     'überarbeitete Manuskript mit dem Update von 2026 (S. 7: 119 Studien, 46.029 Teilnehmende, 66,9 % und 55,2 %, '
     'Studienzahl abweichend von der Version of Record). Nicht zitierfähig (F17 § 6.1), keine Zahl und kein Zitat daraus. Zitiert wird die Version of Record vom '
     '30.09.2026, Interact J Med Res 15, e84822 (PMID 42814774, PMC13626193), Zitierjahr 2026. PDF der Version of Record '
     'vor dem Einbau in 6.1 ablegen, spätestens vor Task 15 (H16), bis dahin Fundstellen nach Abschnitt und Absatz des '
     'PMC-Volltexts, Seitenzahlen nach der Ablage nachtragen. Im abgerufenen Text fehlen die Ziffern der Belegnummern, die Zahl der Belege je Faktor ist an den '
     'Trennzeichen gezählt ([,] = zwei) und an der PDF zu prüfen. ' + VERMERK),
    ('Boumparis2026', 'Metaanalyse nur für den Studienabbruch',
     'Titel „Systematic Review and Meta-Analysis of Attrition“: gepoolt ist nur der Studienabbruch (16,9 %, 95-%-KI 13,6 '
     'bis 20,9). Abschlussrate (66,9 %) und Bestandteil-Adhärenz (55,2 %) sind beschreibende Mittel über die berichtenden '
     'Vergleiche (68 und 66), nach den Limitationen wegen uneinheitlicher Berichterstattung beschreibend und nach SWiM '
     'synthetisiert, nicht metaanalytisch (Discussion, Limitations). Eine Gewichtung nennt die Übersicht nicht, die '
     'Bezugsmenge innerhalb der Vergleiche (mit oder ohne Abbrecher) ebenfalls nicht. Auch die gepoolten Abbruchschätzer '
     'nennen die Autoren beschreibend und nicht nach dem Verzerrungsrisiko gewichtet. Für die Adhärenzwerte im Text '
     '„systematische Übersicht“ und „im Mittel“, nie „Metaanalyse“. Befund Rev. 147 § 0 Nr. 3 und Maßnahme H16 '
     '(„Metaanalyse“) sind so zu lesen. ' + VERMERK),
    ('Boumparis2026', 'Hintergrundsätze sind keine Ergebnisse',
     'Der erste Satz der Zusammenfassung (Background) referiert, Interventionsstudien berichteten häufig, weniger als die '
     'Hälfte der Jugendlichen schließe digitale Programme wie vorgesehen ab. Das ist eine Aussage über andere Studien, '
     'kein Ergebnis der Übersicht, und steht neben deren eigener mittlerer Abschlussrate von 66,9 %. Ebenso Introduction, '
     'Abs. 5: mittlere Adhärenz digitaler Programme „around 50%“, im abgerufenen Text ohne Beleg. Beides nicht als Befund '
     'von Boumparis et al. (2026) zitieren. ' + VERMERK),
    ('Boumparis2026', 'Bezugsmengen: Teilnehmende, Vergleiche, doppelte 55,2 %',
     '46.029 Teilnehmende sind über Interventions- und Kontrollarme summiert (Results, Characteristics of Study '
     'Populations, Abs. 1), nicht die Nutzer der Programme. Die Metaanalyse des Studienabbruchs umfasst 30.956 '
     'Teilnehmende in 108 Vergleichen aus 88 Studien. Viele Anteile beziehen sich auf 143 Vergleiche (Interventionsarme), '
     'nicht auf 116 Studien. 55,2 % steht zweimal: mittlere Bestandteil-Adhärenz (66 Vergleiche) und Anteil der Vergleiche '
     'ohne Anreize (79 von 143). Im Text Bezugsmenge nennen oder auf Zahlen verzichten (6.1: Klick K3, keine Zahlen der '
     'Vorstudien). ' + VERMERK),
    ('Boumparis2026', 'Dauer und Zeitverlauf: nur Bewegungsteil, insgesamt uneinheitlich',
     'Geringere Adhärenz bei längerer Studiendauer beruht im Bewegungsteil auf zwei zitierten Studien mit statistischer '
     'Evidenz (Results, Physical Activity, Intervention-Related Factors, Abs. 1). Bei Mehrkomponentenprogrammen war eine '
     'viermonatige Dauer beschreibend förderlich und abnehmende Teilnahme über lange Dauer hemmend, im Update ging '
     'kürzere Dauer mit weniger Abbruch einher. In der Metaregression des Studienabbruchs war die Dauer nicht signifikant '
     '(QM = 2,60, p = 0,11), die Zusammenfassung nennt die Evidenz zur Dauer uneinheitlich. Davon zu trennen ist der '
     'Rückgang der Nutzung im Verlauf eines Programms (Discussion, Intervention-Related Determinants of Adherence, Abs. 4, '
     'vor allem Ernährung und Mehrkomponenten, bei Adipositas statistisch erste gegen zweite Hälfte). Nur mit dieser '
     'Einschränkung verwenden, nicht als Erklärung des eigenen Rückgangs in Woche 6 (K-10.16). ' + VERMERK),
    ('Boumparis2026', 'Population: keine Sportauswahl, überwiegend weiblich',
     'Zielgruppen nach der Extraktion: Schüler, Studierende, Jugendliche außerhalb formaler Bildung, Berufsausbildung, '
     'Jugendgruppen, klinische Gruppen (Methods, Data Extraction, Abs. 2). Nachwuchssportler sind keine eigene Zielgruppe, '
     'ob Einzelstudien Sportler einschlossen, ist ohne Anhang nicht prüfbar. 59,1 % weiblich, Alter 14,48 ± 2,07 J., '
     'überwiegend ohne Diagnose. Distanz Population 2. Keine Norm und keine Zielmarke der Umsetzung für Nachwuchsspieler '
     'ableiten, im Satz „Jugendliche“ und „digitale Lebensstilprogramme“ nennen. ' + VERMERK),
    ('Boumparis2026', 'Video nicht getrennt ausgewertet',
     'Vermittlungsformen App, Web, Wearable mit Plattform, nur SMS, Computer, gemischt, VR (Results, Characteristics of '
     'Digital Interventions, Abs. 2). Video ist keine eigene Kategorie, reine Kommunikationsplattformen wie E-Mail-Coaching '
     'und Videosprechstunden waren ausgeschlossen (Methods, Eligibility Criteria, Abs. 4). Video kommt nur als Inhalt in '
     'Einzelstudien vor, im Bewegungsteil übermäßige Videolänge als beschreibendes Hemmnis in einer Studie und '
     'abwechslungsreiche Video- und Sportangebote als qualitativ förderlich in zwei. Keine Aussage über videobasierte '
     'Programme aus den Mittelwerten ableiten. ' + VERMERK),
    ('Boumparis2026', 'Bewegungswerte auf wenigen Vergleichen',
     'Bestandteil-Adhärenz bei Bewegung 62,8 % ohne SD und ohne Zahl der berichtenden Vergleiche, die Abschlussrate bei '
     'Bewegung steht nicht im Haupttext. Domänenwerte beruhen auf 4 bis 24 Vergleichen je Domäne, nach den Autoren nur '
     'hinweisend (Results, Characteristics of Health Domains, Abs. 3). Studienabbruch Bewegung 14,1 % (95-%-KI 9,9 bis '
     '19,7, k = 32). Werte aus den Tabellen des Anhangs (Tab. S7 bis S18, Zuordnung zu den Domänen im Text nicht '
     'genannt) erst nach Zugang. Bewegungswerte nur mit diesem '
     'Vorbehalt. ' + VERMERK),
    ('Boumparis2026', 'Einflussfaktoren gezählt, nicht gepoolt',
     'Förder- und Hemmfaktoren sind je Domäne aus Einzelstudien zusammengetragen und nach Evidenzart geordnet: '
     '„statistisch“ bedeutet p < 0,05 in einer Studie, „beschreibend“ ein Muster ohne Test, „qualitativ“ Interviews und '
     'offene Antworten (Methods, Data Synthesis, Abs. 1 und 2). Nicht gepoolt, ohne Bewertung des Verzerrungsrisikos, '
     'Studien ungeachtet ihrer methodischen Güte gleich behandelt (Limitations). Viele Faktoren beruhen auf ein oder zwei Belegen. Keinen Faktor als '
     'gesicherten Prädiktor zitieren und keinen Schluss auf Ursachen der eigenen Umsetzung ziehen (Erinnerungen in den '
     'WhatsApp-Gruppen, Fortschrittskarte, Videolänge). ' + VERMERK),
    ('Boumparis2026', 'Keine Dosis-Wirkung',
     'Wirksamkeit ist nur als Erreichen der primären Endpunkte gezählt: 52,8 % (47 von 89) der darauf geprüften Programme '
     '(Results, Characteristics of Digital Interventions, Abs. 4). Einen Zusammenhang zwischen Adhärenz und Wirksamkeit '
     'prüfte die Übersicht nicht, die Autoren empfehlen Dosis-Wirkungs-Analysen für künftige Forschung (Discussion, '
     'Implications for Future Research). Aus dieser Quelle keine Dosis-Wirkung und keine Wirkung der Adhärenz ableiten '
     '(F17 § 11.2b). ' + VERMERK),
    ('Boumparis2026', 'Verbleib und Nutzung: zwei Maße',
     'Folgerung der Autoren im Ergebnis- und Diskussionsteil, nicht in Zusammenfassung oder Schluss: Der gepoolte '
     'Studienabbruch (rund 17 %) liegt weit unter der Nichtnutzung, die die Abschluss- und Bestandteilwerte zeigen. Viele '
     'Jugendliche („many“, „tend to“) blieben nominell eingeschrieben und nutzten das Programm nur teilweise (Results, '
     'Quantitative Synthesis of Attrition, Abs. 3, Discussion, Domain-Specific Adherence Patterns, Abs. 3). Die Aussage '
     'verbindet ein gepooltes Maß (108 Vergleiche) und ein beschreibendes (66 Vergleiche), deren Bezugsmengen verschieden '
     'sind. „Die meisten“ trägt nur der gepoolte Abbruch. In einer Formulierung beide Maße in Worten benennen, ohne '
     'gemeinsames Subjekt, Verbleib nicht als Adhärenz ausgeben. ' + VERMERK),
    ('Klusemann2012', 'Bezugsmenge der 77 %',
     '„77% compliance from the video group“ (S. 2681) bezieht sich rechnerisch auf alle 13 Spieler der Videogruppe, nicht '
     'auf die 11 nach dem Ausschluss: Hätten die 11 Ausgewerteten je mindestens 75 % erreicht und 5 davon alle 12 '
     'Einheiten, ergäben sich mindestens 114 von 132 Einheiten (86,4 %). Der Ausschluss unter 75 % betrifft nur den '
     'Leistungsvergleich. Im Satz die Umsetzung der ganzen Videogruppe nennen, nicht „nach Ausschluss“. Textvorschlag 6.1 '
     '§ 5 („77 % nach Ausschluss zweier Spieler“) ist so zu berichtigen. [Nachgetragen 02.10.2026, Task Boumparis, '
     'Zweitprüfung Nr. 6]'),
]


def lese(pfad):
    with open(pfad, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f, delimiter=SEMI)
        return r.fieldnames, list(r)


def schreibe(pfad, felder, zeilen):
    with open(pfad, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=felder, delimiter=SEMI, lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for z in zeilen:
            w.writerow(z)


def md5(pfad):
    return hashlib.md5(open(pfad, 'rb').read()).hexdigest()


def main():
    quelle, ziel = sys.argv[1], sys.argv[2]
    os.makedirs(ziel, exist_ok=True)
    protokoll = []
    # Neue Texte ohne Semikolon (Stilprofil Teil 3, auch in Arbeitsdateien eingehalten)
    for z in T1_NEU:
        assert not any(SEMI in v for v in z.values()), z['id']
    assert SEMI not in KLUSEMANN_ZUSATZ
    for q, a, b in T4_NEU:
        assert SEMI not in a and SEMI not in b, a
    # T1
    f1, z1 = lese(os.path.join(quelle, 'T1_steckbriefe.csv'))
    vorher = [dict(z) for z in z1]
    vorhanden = {z['id'] for z in z1}
    neu = [dict(z) for z in T1_NEU if z['id'] not in vorhanden]
    assert all(set(z.keys()) == set(f1) for z in T1_NEU), 'T1-Felder passen nicht'
    geaendert = []
    # Eigene Zeilen dieses Tasks (Boumparis2026) werden bei späteren Läufen auf den Stand des Skripts gebracht
    # (Korrekturen nach der Zweitprüfung), das Feld `kapitel` nur über KAPITEL_NACH_KLICK.
    eigen = {z['id']: z for z in T1_NEU}
    for z in z1:
        if z['id'] in eigen:
            for feld, wert in eigen[z['id']].items():
                if feld != 'kapitel' and z[feld] != wert:
                    z[feld] = wert
                    geaendert.append('%s.%s korrigiert' % (z['id'], feld))
    for z in z1:
        for kid, feld, alt, wert in T1_AENDERN:
            if z['id'] == kid and z[feld] == alt:
                z[feld] = wert
                geaendert.append('%s.%s %s → %s' % (kid, feld, alt, wert))
        if z['id'] == 'Klusemann2012' and KLUSEMANN_MARKE not in z['evidenzsicherheit']:
            z['evidenzsicherheit'] = z['evidenzsicherheit'] + KLUSEMANN_ZUSATZ
            geaendert.append('Klusemann2012.evidenzsicherheit + Vermerk Distanzregel')
        if z['id'] in KAPITEL_NACH_KLICK and z['kapitel'] != KAPITEL_NACH_KLICK[z['id']]:
            geaendert.append('%s.kapitel → %s' % (z['id'], KAPITEL_NACH_KLICK[z['id']]))
            z['kapitel'] = KAPITEL_NACH_KLICK[z['id']]
    for z in neu:
        if z['id'] in KAPITEL_NACH_KLICK:
            z['kapitel'] = KAPITEL_NACH_KLICK[z['id']]
    z1.extend(neu)
    schreibe(os.path.join(ziel, 'T1_steckbriefe.csv'), f1, z1)
    protokoll.append('T1: %d Steckbriefe vorher, %d neu (%s), %d nachher' % (
        len(vorhanden), len(neu), ', '.join(z['id'] for z in neu), len(z1)))
    protokoll.append('T1 geändert: ' + (' · '.join(geaendert) if geaendert else 'nichts'))
    # T4
    f4, z4 = lese(os.path.join(quelle, 'T4_zitierfallen.csv'))
    vorh4 = {(z['quelle_id'], z['art']) for z in z4}
    neu4 = [{'quelle_id': q, 'art': a, 'befund_und_konsequenz': b} for q, a, b in T4_NEU if (q, a) not in vorh4]
    assert f4 == ['quelle_id', 'art', 'befund_und_konsequenz'], f4
    # Eigene Zitierfallen dieses Tasks bei späteren Läufen auf den Stand des Skripts bringen
    texte4 = {(q, a): b for q, a, b in T4_NEU}
    korr4 = 0
    for z in z4:
        schl = (z['quelle_id'], z['art'])
        if schl in texte4 and z['befund_und_konsequenz'] != texte4[schl]:
            z['befund_und_konsequenz'] = texte4[schl]
            korr4 += 1
    z4.extend(neu4)
    schreibe(os.path.join(ziel, 'T4_zitierfallen.csv'), f4, z4)
    protokoll.append('T4: %d Zitierfallen vorher, %d neu, %d korrigiert, %d nachher' % (len(vorh4), len(neu4), korr4, len(z4)))
    for n in ('T1_steckbriefe.csv', 'T4_zitierfallen.csv'):
        protokoll.append('%s: MD5 vorher %s, nachher %s, %d Byte' % (
            n, md5(os.path.join(quelle, n)), md5(os.path.join(ziel, n)), os.path.getsize(os.path.join(ziel, n))))
    # Rücklesen: Zeilenzahl, Felder, unveränderte Altzeilen bis auf die vorgesehenen Änderungen
    f1r, z1r = lese(os.path.join(ziel, 'T1_steckbriefe.csv'))
    assert f1r == f1
    erlaubt = {'Klusemann2012', 'Boumparis2026'} | set(KAPITEL_NACH_KLICK)
    for alt, neu_z in zip(vorher, z1r):
        assert alt['id'] == neu_z['id']
        if alt['id'] not in erlaubt:
            assert alt == neu_z, alt['id']
    f4r, z4r = lese(os.path.join(ziel, 'T4_zitierfallen.csv'))
    assert f4r == f4 and len(z4r) == len(z4)
    protokoll.append('T1_steckbriefe.csv rückgelesen: %d Zeilen, %d Felder, Altzeilen außer %s unverändert' % (
        len(z1r), len(f1r), ', '.join(sorted(erlaubt))))
    protokoll.append('T4_zitierfallen.csv rückgelesen: %d Zeilen, %d Felder' % (len(z4r), len(f4r)))
    with open(os.path.join(ziel, 'T1_T4_Nachtrag_Boumparis_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

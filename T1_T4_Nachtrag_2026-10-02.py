# -*- coding: utf-8 -*-
"""Nachtrag T1 (Steckbriefe) und T4 (Zitierfallen) für Task 12a, 02.10.2026.

Trägt die am 02.10.2026 am Volltext gelesenen Quellen Klusemann et al. (2012), Rogers et al. (2020) und
Veith et al. (2021) in `Schreiben\\ev3_daten\\T1_steckbriefe.csv` ein und ergänzt ihre Zitierfallen in
`T4_zitierfallen.csv`. Zweiter Lauf (02.10., nach Klick K5): eine T4-Zeile zu Zheng et al. (2025), Leistungsniveau nicht
berichtet. Idempotent: vorhandene Kennungen werden nicht doppelt angelegt. Format wie bisher
(Semikolon-Trenner, UTF-8 mit BOM, LF, Quoting nur bei Bedarf). Ohne Semikolon im Skript (chr(59)).

Aufruf: python3 T1_T4_Nachtrag_2026-10-02.py <Ordner mit T1_steckbriefe.csv und T4_zitierfallen.csv> <Ausgabeordner>
"""
import csv
import hashlib
import os
import sys

SEMI = chr(59)

T1_NEU = [
    {
        'id': 'Klusemann2012',
        'kurzzitat': 'Klusemann et al. (2012)',
        'vollzitat': 'Klusemann, M. J., Pyne, D. B., Fay, T. S., & Drinkwater, E. J. (2012). Online video-based resistance '
                     'training improves the physical capacity of junior basketball athletes. Journal of Strength and '
                     'Conditioning Research, 26(10), 2677–2684. https://doi.org/10.1519/JSC.0b013e318241b021',
        'fassung': 'Verlagsfassung (JSCR 26(10), 2677–2684), DOI nach PubMed (PMID 22105056), nicht im PDF-Text',
        'verlag': 'Lippincott Williams & Wilkins / NSCA — kein MDPI',
        'design': 'Dreiarmige kontrollierte Studie über 6 Wochen in der Saison: betreutes Krafttraining (SG), '
                  'videogeleitetes Krafttraining ohne Aufsicht (VG), Kontrolle (CG). Zuteilung durch Minimierung der '
                  'Gruppenunterschiede in Alter, Geschlecht und Kraft (S. 2678), im Abstract „randomly assigned“. '
                  'Magnitudenbasierte Inferenz mit 90-%-Konfidenzgrenzen, keine p-Werte. Ausschluss bei Compliance unter '
                  '75 % (2 VG), analysiert 36',
        'population': 'N = 38 Junioren-Basketballspieler (Landesauswahl oder Entwicklungsprogramm, Australien): 17 m '
                      '(14 ± 1 J.), 21 w (15 ± 1 J.), SG 13, VG 13, CG 12 (Methodenteil 13), ohne Krafttrainingserfahrung',
        'reifestatus': 'NICHT erhoben (nur Alter)',
        'dosis': '6 Wochen, 2×/Wo, 12 Einheiten Körpergewichts-Krafttraining mit Lande- und Sprungtechnik auf dem '
                 'Basketballfeld, VG per Online-Video. Compliance aus Online-Tagebuch: SG 96 %, VG 77 %, nur 5 VG mit allen '
                 '12 Einheiten (S. 2681)',
        'uebungskatalog': 'Kraftübungen mit Eigengewicht, Lande- und Sprungtechnik (S. 2679), plyometrischer Anteil nicht '
                          'quantifiziert',
        'evidenzsicherheit': 'Abstract: SG und VG mit 3–5 % größeren Verbesserungen in Vertikalsprung, 20 m und Yo-Yo '
                             'gegenüber CG. Tab. 1 (S. 2680): VG−CG Vertikalsprung 3,6 ± 4,2 % „trivial“, 20 m 4,4 ± 3,3 % '
                             '„small“, Agility 2,4 ± 1,9 % „small“ — das Abstract überzeichnet den Vertikalsprung. Für 6.1 '
                             'nur Kontext (Umsetzung Video gegen betreut), keine Wirksamkeitsevidenz',
        'd_pop': '2',
        'd_dos': '2',
        'd_ziel': '1',
        'kapitel': '6.1 (Kontext Umsetzung, Modul offen), 6.3 G3',
    },
    {
        'id': 'Rogers2020',
        'kurzzitat': 'Rogers et al. (2020)',
        'vollzitat': 'Rogers, S. A., Hassmén, P., Roberts, A. H., Alcock, A., Gilleard, W. L., & Warmenhoven, J. S. (2020). '
                     'Movement competency training delivery: At school or online? A pilot study of high-school athletes. '
                     'Sports, 8(4), 39. https://doi.org/10.3390/sports8040039',
        'fassung': 'Verlagsfassung (Version of Record, Open Access, PMC7240720)',
        'verlag': 'MDPI (Sports) — Ruf transparent einordnen (F17 § 6.1)',
        'design': 'Pilotstudie mit zwei Armen über 16 Wochen: F2F (eine Präsenzeinheit in der Schulpause plus eine '
                  'Online-Einheit je Woche, n = 18) und OL (zwei Online-Einheiten je Woche, n = 21). Zuteilung durch '
                  'Paarbildung nach dem AIMS-Ausgangswert (S. 6), keine Gruppe ohne Training. Deskriptive Auswertung mit '
                  'SWC und Einzelverläufen, Exit-Interviews',
        'population': '39 Schulsportler einer australischen High School verschiedener Sportarten: 19 m (14,5 ± 0,3 J., '
                      'Maturity Offset 0,8 ± 0,7 J.), 20 w (14,6 ± 0,3 J.), freiwilliges Zusatztraining, 22 mit Prä- und '
                      'Post-Daten (S. 3, 8)',
        'reifestatus': 'Maturity Offset nach Mirwald berichtet (Jungen 0,8 J.)',
        'dosis': '16 Wochen, 2 Einheiten/Wo à 20–30 min Bewegungskompetenz- und Athletiktraining, Online-Plattform mit '
                 'Videodemonstrationen. Compliance OL (n = 8 mit Prä- und Post-Daten): 0 bis 11 von 32 Einheiten '
                 'protokolliert, im Mittel 12 % (S. 9). F2F-Anwesenheit 60 % (31 bis 88 %)',
        'uebungskatalog': 'Integratives neuromuskuläres Training (Kniebeuge-, Druck-, Zug-, Rumpf-, Landevarianten, '
                          'Lauf-ABC), kein plyometrisches Programm',
        'evidenzsicherheit': 'Compliance-Schwellen aus Klusemann et al. (2012) übernommen (75 % akzeptabel, 50–75 % '
                             'moderat, unter 50 % gering, S. 8). Hoher Ausfall (39 → 22). Die 12 % gelten für die acht '
                             'OL-Spieler mit Prä- und Post-Daten, nicht für alle 21. Leistungsdaten ohne Inferenz. Für 6.1 '
                             'nur Kontext (untere Spanne der Umsetzung), Modul offen',
        'd_pop': '2',
        'd_dos': '2',
        'd_ziel': '2',
        'kapitel': '6.1 (Kontext Umsetzung, Modul offen), 6.3 G3',
    },
    {
        'id': 'Veith2021',
        'kurzzitat': 'Veith et al. (2021)',
        'vollzitat': 'Veith, S., Whalan, M., Williams, S., Colyer, S., & Sampson, J. A. (2021). Part 2 of the 11+ as an '
                     'effective home-based exercise programme in elite academy football (soccer) players: A one-club '
                     'matched-paired randomised controlled trial. Science and Medicine in Football, 5(4), 339–346. '
                     'https://doi.org/10.1080/24733938.2021.1874616',
        'fassung': 'Online-First-Fassung vom 25.01.2021 im Ordner (ohne Heft und Seiten), Version of Record 5(4), 339–346 '
                   'nach PubMed (PMID 35077306). Seitenangaben nach dem PDF',
        'verlag': 'Taylor & Francis — kein MDPI',
        'design': 'Paarweise randomisierte kontrollierte Studie innerhalb eines Vereins (Sydney FC): Teil 2 des 11+ nach '
                  'dem Training (TG, n = 32) gegen zu Hause (HG, n = 33) über die Saison 2019 (33 Wochen), lineare '
                  'gemischte Modelle, Bericht nach CONSORT. Keine Gruppe ohne Programm',
        'population': '65 männliche Akademiespieler U13 bis U16 (13,9 ± 1,2 J., 163,1 cm, 52,2 kg), Australien (S. 3)',
        'reifestatus': 'Nicht als Kovariate, Wachstumsrate (ROG) für die Hamstringkraft kontrolliert',
        'dosis': '3×/Wo Teil 2 des 11+ (Kraft, Plyometrie, Gleichgewicht, Level 1 bis 3) über die Saison, HG zu Hause. '
                 'Umsetzung HG per wöchentlichem Online-Fragebogen: 2,8 (KI 2,7 bis 2,9) Einheiten/Wo, alle Übungen in 87 % '
                 'der Fälle vollständig (S. 5). TG-Compliance nicht erfasst (S. 3)',
        'uebungskatalog': '11+ Teil 2 (u. a. Nordic Hamstring, Copenhagen, Sprünge), plyometrischer Anteil nicht '
                          'quantifiziert',
        'evidenzsicherheit': 'Präventions- und Kraftprogramm in der Saison, kein Sommerpausen-Setting. Compliance als '
                             'Selbstauskunft. Zielgrößen CMJ, exzentrische Hamstringkraft, Stabilisation, Verletzungen. Für '
                             '6.1 nur Kontext (obere Spanne der Umsetzung), bis zur erneuten Literatursuche des Verfassers offen',
        'd_pop': '1',
        'd_dos': '2',
        'd_ziel': '2',
        'kapitel': '6.1 (Kontext Umsetzung, Modul offen), 6.3 G3',
    },
]

T4_NEU = [
    ('Klusemann2012', 'Abstract vs. Tabelle 1 (Vertikalsprung)',
     'Abstract: SG und VG erreichten „3–5 % … greater improvements in several physical performance measures (vertical '
     'jump height, 20-m sprint time, and Yo-Yo …)“ gegenüber CG. Tab. 1 (S. 2680) weist für VG gegen CG beim '
     'Vertikalsprung 3,6 ± 4,2 % „trivial“ aus, als Unterschied gewertet sind nur 20 m (4,4 ± 3,3 %, small), Agility '
     '(2,4 ± 1,9 %, small) und Yo-Yo (small). Den Vertikalsprung nicht als Wirksamkeitsbefund der Videogruppe zitieren. '
     '[Nachgetragen 02.10.2026, Task 12a]'),
    ('Klusemann2012', 'Zuteilung und Fallzahl',
     'Abstract „randomly assigned“, Methodenteil (S. 2678): Zuteilung „with the aim of minimizing differences in group '
     'means of age, gender, and strength scores“, also Minimierung ohne Zufallsmechanismus. CG im Abstract n = 12, im '
     'Methodenteil n = 13, analysiert 36 (VG 11 nach Ausschluss von 2 Spielern unter 75 % Compliance). Als „kontrolliert“ '
     'führen, nicht als „randomisiert“. Die Compliance (SG 96 %, VG 77 %, Online-Tagebuch, S. 2681) ist eine '
     'Selbstauskunft, die Ausschlussregel macht den VG-Vergleich teilweise Per-Protokoll. [Nachgetragen 02.10.2026]'),
    ('Klusemann2012', 'Magnitudenbasierte Inferenz',
     'Ergebnisse als magnitudenbasierte Inferenz mit 90-%-Konfidenzgrenzen und Etiketten „trivial/small/unclear“, keine '
     'p-Werte. Die Etiketten nicht übernehmen (F17 § 5a, Bauplan § 8), nur Richtung und Größenordnung in Worten. '
     '[Nachgetragen 02.10.2026]'),
    ('Rogers2020', 'Bezugsmenge der 12 %',
     '„mean of 12 %“ (S. 9) gilt für die acht OL-Spieler mit Prä- und Post-Daten von 21 zugeteilten, protokolliert über '
     'die Online-Plattform. Die Compliance der 13 Abbrecher ist nicht berichtet, der Wert ist damit eher eine Obergrenze '
     'der Gruppe. Im Satz die Bezugsmenge nennen. Zuteilung durch Paarbildung nach dem Ausgangswert (S. 6), nicht '
     'randomisiert. Pilotstudie ohne inaktive Kontrollgruppe, Leistungsdaten ohne Inferenz. MDPI (Sports). '
     '[Nachgetragen 02.10.2026, Task 12a]'),
    ('Veith2021', 'Fassung, Compliance und Vergleich',
     'Im Ordner liegt die Online-First-Fassung (25.01.2021) ohne Heft und Seiten, zitiert wird die Version of Record 5(4), '
     '339–346 (PubMed, PMID 35077306), Seitenangaben nach dem PDF (Compliance S. 5). Die HG-Compliance von 2,8 '
     'Einheiten/Wo ist eine Selbstauskunft im wöchentlichen Online-Fragebogen, die TG-Compliance wurde nicht erfasst (S. 3), '
     'es gibt also keinen Vergleich der Umsetzung betreut gegen zu Hause. „randomised“ nur paarweise innerhalb eines '
     'Vereins, keine Gruppe ohne Programm, Präventionsprogramm in der Saison. [Nachgetragen 02.10.2026, Task 12a]'),
    ('Zheng2025', 'Leistungsniveau nicht berichtet',
     'Einschluss nach Alter (10 bis 18,99 Jahre, Tab. 1, S. 4), Tab. 3 (S. 6 bis 7) führt Geschlecht, Alter, Fallzahl, Dauer, Frequenz und Tests, '
     'aber kein Leistungsniveau der 20 Studien. Die Formel „junger Fußballspieler überwiegend höherer Spielklassen“ (6.1, Klick K5 vom 02.10.) stützt '
     'sich auf Oliver et al. (2024, ab Tier 3, S. 625) und auf die in T1 erfassten Einzelstudien Zhengs (Negra 2020, Sammoud 2024, Hammami 2016: regionale '
     'bis nationale Auswahlen Tunesiens, Padrón-Cabo 2025: LaLiga-Akademie), nicht auf eine Angabe von Zheng et al. Kein Leistungsniveau als Befund '
     'von Zheng et al. zitieren. [Nachgetragen 02.10.2026, Task 12a, zweiter Lauf]'),
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
    # T1
    f1, z1 = lese(os.path.join(quelle, 'T1_steckbriefe.csv'))
    vorhanden = {z['id'] for z in z1}
    neu = [z for z in T1_NEU if z['id'] not in vorhanden]
    assert all(set(z.keys()) == set(f1) for z in neu), 'T1-Felder passen nicht'
    z1.extend(neu)
    schreibe(os.path.join(ziel, 'T1_steckbriefe.csv'), f1, z1)
    protokoll.append('T1: %d Steckbriefe vorher, %d neu (%s), %d nachher' % (len(vorhanden), len(neu), ', '.join(z['id'] for z in neu), len(z1)))
    # T4
    f4, z4 = lese(os.path.join(quelle, 'T4_zitierfallen.csv'))
    vorh4 = {(z['quelle_id'], z['art']) for z in z4}
    neu4 = [{'quelle_id': q, 'art': a, 'befund_und_konsequenz': b} for q, a, b in T4_NEU if (q, a) not in vorh4]
    assert f4 == ['quelle_id', 'art', 'befund_und_konsequenz'], f4
    z4.extend(neu4)
    schreibe(os.path.join(ziel, 'T4_zitierfallen.csv'), f4, z4)
    protokoll.append('T4: %d Zitierfallen vorher, %d neu, %d nachher' % (len(vorh4), len(neu4), len(z4)))
    for n in ('T1_steckbriefe.csv', 'T4_zitierfallen.csv'):
        protokoll.append('%s: MD5 vorher %s, nachher %s, %d Byte' % (n, md5(os.path.join(quelle, n)), md5(os.path.join(ziel, n)), os.path.getsize(os.path.join(ziel, n))))
    # Rücklesen
    for n in ('T1_steckbriefe.csv', 'T4_zitierfallen.csv'):
        felder, zeilen = lese(os.path.join(ziel, n))
        protokoll.append('%s rückgelesen: %d Zeilen, %d Felder' % (n, len(zeilen), len(felder)))
    with open(os.path.join(ziel, 'T1_T4_Nachtrag_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

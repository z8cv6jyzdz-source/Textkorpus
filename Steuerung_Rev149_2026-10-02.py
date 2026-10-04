# -*- coding: utf-8 -*-
"""Steuerung Rev. 149 (02.10.2026, Task 12a): Teil 0 der Sitzungsnotizen und Maßnahmenliste fortschreiben.

Liest die beiden Steuerdokumente aus dem Quellordner (frisch gestagter Ordnerstand, Rev. 148), prüft die Anker,
setzt den Eintrag Rev. 149 an den Kopf von Teil 0, schreibt die Stand-Zeilen fort, ergänzt in der Maßnahmenliste
die Vermerke zu H13, G29, G32, G35, die Taskzeilen 12 und 13 und die Summe. Jeder Anker muss genau einmal vorkommen,
sonst bricht das Skript ab. Ausgabe in den Zielordner mit Protokoll (Zeilen, Bytes, MD5 vorher und nachher).
Ohne Semikolon im Skript (chr(59)).

Aufruf: python3 Steuerung_Rev149_2026-10-02.py <Quellordner> <Zielordner>
"""
import hashlib
import os
import sys

SEMI = chr(59)
NOTIZEN = 'Cowork_Sitzungsnotizen.md'
MASSNAHMEN = 'Massnahmenliste_Datenverarbeitung.md'

EINTRAG_149 = """### ⭐⭐ NEU (Rev. 149, 02.10.2026, 16:12 Sitzungsuhr, Auftrag: Prompt Task 12a nach Rev. 146): Task 12a — Textvorschlag 6.1 „Einordnung der Ergebnisse“ (700 Wörter) mit unabhängiger Zweitprüfung vorgelegt, Klicks K1 bis K7 des Verfassers, K5 umgesetzt, T1/T4-Nachtrag, Freigabe und Einbau zurückgestellt bis zum Task „Boumparis“

**Auftrag:** Task 12a nach Plan § 3 und Nachtrag 30.09./01.10. mit dem Prompt `claude/Prompt_Task12a_6.1_2026-10-02.md` (Projektkopie), Schritt 0 war Rev. 146. Auf Anweisung des Verfassers zuerst ein Zwischenschritt: die DOIs der Beschaffungsposten für 6.1 im Chat aufgezeigt, danach legte der Verfasser Rogers et al. (2020) und Veith et al. (2021) in `Ideen und Studien` ab (13:38 und 13:42 Sitzungsuhr, Rev. 147 vermerkt es in H13). Die Sitzung lief parallel zu Rev. 147 und 148, deren Nummern sind vergeben, dieser Eintrag trägt die nächste freie Nummer (Rev. 148, Absatz „Im Ordner vorgefunden“).

**Verfahren:** Lesefolge F17 § 1.2 (Berichtsraster § 3.14 mit 6.1.1 bis 6.1.4, Bauplan § 2.4 und § 8, Kennzahlenblatt Rev. 2, Umfangsdokument § 5.1 bis § 5.4, Stilprofil, Vormerkungen aus Textvorschlag 5 § 9.3, Textvorschlag 4.7 § 7 und den Einleitungs-Textvorschlägen). Alle Vorstudien am Volltext mit Seitenzuordnung geprüft, T4 vor jeder Zitation gelesen. Zug-Tabelle und Verzichtstabelle vor dem ersten Satz, Stichpunktgerüst mit vier Klickfragen, Gerüst freigegeben (K4), Wortlaut per Skript gemessen und geprüft, unabhängige Zweitprüfung durch einen Subagenten (17 Befunde: 2 A, 9 B, 6 C, alle behandelt), danach zweite Klickrunde (K5 bis K7).

**Klicks des Verfassers (02.10.):** K1 Vorstudien „wie im Gerüst“ · K2 Spanne der Umsetzungsraten: keine der vorgelegten Varianten („Ist alles nicht optimal. Ich suche erneut nach Literatur“), Modul A2-M bleibt offen · K3 „Ohne Zahlen der Vorstudien“ (Vorstudien nur mit Richtung, Nachweisbarkeit, Population und Dosis in Worten, Effektstärken in der Belegtabelle) · K4 Gerüst „Freigeben wie vorgelegt“ · K5 Leistungsniveau der Metaanalysen im Satz: „Ja, „überwiegend höherer Spielklassen“ ergänzen“ (A3 S4, A5 S4) · K6 Freigabe des Wortlauts nicht erteilt, zurückgestellt: „Ich habe eine neue Quelle dem Ordner hinzugefügt. In einem Separaten Task wir aktuell die Relevanz für unser Projekt herausgearbeiet und ein prompt erstellt, der die auf die Adhärenzbezogenen Textabschnitte mit der Quelle bearbeitet“ (das ist der Task „Boumparis“, Rev. 148) · K7 Einbau nach der Freigabe per Skript durch Claude.

**Ergebnis:** `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` (79.307 Byte, MD5 `764fef26…`, Projektkopie `claude/`), zwölf Teile (§ 0 bis § 11, § 11 Einbau folgt): Kopf mit Messung, Wortlaut A1 bis A6 und Modul A2-M, Zug-Tabelle, Verzichtstabelle, Rasterzuordnung je Satz, Belegtabelle mit Wortlaut, Fundstelle, T4 und Lage zum eigenen Intervall, Zahlen mit Kennungen, Kürzungsleiter (fünf Stufen), offene Punkte, Vormerkungen, Zweitprüfung. **6.1 ohne Modul 700 Wörter** (Budget 700, F17 § 5.2), mit Modul 729 (Stufe 1 der Kürzungsleiter, A3 S8 Liu et al. 2024, −30). 41 Sätze, Median 16, längster 31, 0 Semikola außerhalb von Zitierklammern, 0 Abschnittsverweise, 14 Belegklammern (eine je 50 Wörter), neun Quellen (Oliver 2024, Zheng 2025, Ramirez-Campillo 2020 und 2023, Liu 2024, Sammoud 2024, Lloyd 2016, Negra 2020, Thomas 2020), zehn mit dem Modul (Klusemann 2012). Bauform nach Bauplan § 2.4: Eröffnung mit Ankersatz, Hauptbefund und Gegenbefund ohne Beleg und Zahl (A1) · Programmangebot und Verdünnungslogik mit beobachtendem Per-Protokoll-Vergleich (A2, F17 § 11.7, Klick 28.09. 19:25) · je Zielgröße ein Fünf-Zug-Absatz Sprint, Richtungswechsel, Sprung (A3 bis A5) · Nutzen und Schaden (A6, CONSORT 22). Prüfskript ohne Befund (Sprachregelungen F17 § 10 und § 11.2b, kein „randomisiert“, Mechanismen nur mit Modalverb).

**Markierungsregel (aus der Zweitprüfung Nr. 1, in § 5 und § 0 des Textvorschlags):** „Widerspruch“ nur, wo der Effekt der Vorstudie außerhalb des eigenen g-Intervalls liegt (K-06.1 bis K-06.3), sonst „weder bestätigt noch widerlegt“. Danach: Sprint ohne Markierung (Effekte der Metaanalysen im eigenen Intervall) · Richtungswechsel Übereinstimmung mit Ramirez-Campillo et al. (2023), Widerspruch zu Oliver et al. (2024, CODS g 1,01) und Sammoud et al. (2024), Zheng et al. (2025) ohne Markierung (505 nicht enthalten, T4) · Sprung Widerspruch zu Oliver, Zheng und Sammoud, Übereinstimmung mit Lloyd et al. (2016). Vormerkung für F17 § 6.5 (nächste Fassung).

**K5 umgesetzt (16:00 Sitzungsuhr):** A3 S4 „bei jungen Fußballspielern überwiegend höherer Spielklassen“ (+4 Wörter), A5 S4 „junger Fußballspieler überwiegend höherer Spielklassen“ (+3), Gegenfinanzierung innerhalb von 6.1 um sieben Wörter (A3 S6 „schließt solche Effekte aber nicht aus“, A3 S7 ohne „hier“, A3 S8 „sechs Einheiten in drei Wochen“), 695 → 700. Beleglage: Oliver et al. (2024) nur ab Tier 3 (S. 625), Zheng et al. (2025) berichten kein Leistungsniveau (Tab. 3, S. 6 bis 7), „überwiegend“ stützt sich auf Oliver und die in T1 erfassten Einzelstudien Zhengs (Negra 2020, Sammoud 2024, Hammami 2016, Padrón-Cabo 2025). Dazu T4-Zeile `Zheng2025` „Leistungsniveau nicht berichtet“ (zweiter Lauf des Nachtragsskripts, 158 Zitierfallen, T1 unverändert 75).

**T1/T4-Nachtrag (`03_Skripte\\T1_T4_Nachtrag_2026-10-02.py`, Protokoll `.txt` mit beiden Läufen):** Lauf 1: T1 um Klusemann2012, Rogers2020, Veith2021 (72 → 75, MD5 `a4d07a26…`), T4 um fünf Zeilen (152 → 157). Lauf 2: T4 um die Zheng-Zeile (157 → 158, 76.133 Byte, MD5 `cba50a05…`), alte Zeilen bytegleich. Volltextbefunde: Klusemann et al. (2012) Compliance Videogruppe 77 % nach Online-Tagebuch gegen 96 % betreut (S. 2681), Zuteilung durch Minimierung, magnitudenbasierte Inferenz · Rogers et al. (2020) „mean of 12 %“ nur für acht von 21 Spielern mit Prä- und Post-Daten, Pilotstudie, MDPI · Veith et al. (2021) Online-First-Fassung im Ordner, Version of Record 5(4), 339–346, Compliance der Heimgruppe als Selbstauskunft, Trainingsgruppe nicht erfasst.

**Eigene Korrekturen in dieser Sitzung:** (1) Die Fassung von 15:31 nannte im Kopf „elf Quellen (zwölf mit dem Modul)“, richtig sind neun und zehn, seit 16:05 per Skript gezählt. (2) Die Distanz von Klusemann et al. (2012) stand in § 5 mit 2·2·1 = 5 (Maßstab Wirksamkeitsevidenz), für den Umsetzungsvergleich gilt wie im Befund Rev. 147 § 2.1 2·0·0 = 2 (Zielgröße ist die Umsetzungsrate selbst), Präzisierung (c) aus Rev. 148 damit auf Seiten des Textvorschlags erledigt. (3) Zweitprüfung Nr. 1 („widerspricht“ beim Sprint trotz Effekten im eigenen Intervall) und Nr. 2 (Oliver et al. 2024 fehlte beim Richtungswechsel) eingearbeitet, Nr. 10 nach K5 übernommen, Nr. 17 (Gliederung v6 gegen F17 v5) bleibt in anderer Form.

**Offen beim Verfasser:** (1) Task „Boumparis“ nach Rev. 148 (Version of Record ablegen, Startsatz Plan § 8), er liefert den Vergleichssatz für A2-M oder den Verzicht als `04_Uebergaben\\Textvorschlag_6.1_Nachtrag_K2_⟨Datum⟩.md` · (2) danach Klickfreigabe des Wortlauts 6.1 je Absatz (A1, A3 bis A6 stehen wie vorgelegt, A2 und A2-M nach dem Adhärenz-Prompt) · (3) Einbau per Skript durch Claude (`03_Skripte\\Master_6_1_2026-10-02.py`, Word geschlossen, Rückschreibung aus frischem Ausgabepfad, MD5, Abgleich, Messskript Fassung 4, Endabgleich Fassung 3 in `03_Skripte\\Endabgleich_2026-10-02_Kapitel6_1\\`, Zahlenliste bis Task 18 unverändert) · (4) F9 im Master, Schreibschutz der Abgabe, übrige Punkte wie Rev. 146 bis 148.

**Vormerkungen (Textvorschlag 6.1 § 9):** 12b: MDES gegen SESOI und Literaturerwartungen mit den Effektstärken aus § 5 (6.2.1), Messgüte und Attrition je Zielgröße (6.2.4, 6.2.6, G5), Begleitbedingungen in beide Richtungen (6.2.12, in 6.1 bewusst nicht genannt), Korpuslücke Setting und Tier-Diskrepanz (G8), Verdünnung als Limitation (G3), Gründe nicht durchgeführter Einheiten (G6), Moran et al. (2024) nur bei Übungsauswahl-Gedanke (6.2.8), Zerlegung des Abstands unadjustiert zu adjustiert und Überlappung (6.2.3, 6.2.10), Negativmuster des Korpus (Negra 2020, Liu 2024) · 13a: Hauptbefund in der Sprache von A1, Zeitverlauf der Weite offen, keine Programmdauer-Empfehlung, Umsetzung als Erkenntnisaspekt · Schlussfassung der Einleitung: Lloyd 2016, Sammoud 2024, Negra 2020, Liu 2024 noch nicht eingeführt, Ankersatz mit „deshalb“ nur dort · Task 15: sechs neue Einträge (Lloyd 2016, Sammoud 2024, Negra 2020, Liu 2024, Ramirez-Campillo 2023, Thomas 2020), Klusemann 2012 nur mit Modul · Task 16: Skripte dieser Sitzung als KI-erzeugt, Zweitprüfung · Task 18: leeres Feld im Titelabsatz, Umnummerierung 6.1 → 4.1 · Steuerdokumente: Berichtsraster § 3.14 Ist-Spalte nach dem Einbau, F17 § 6.5 Markierungsregel.

**Stand der Dateien:** Neu: `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` (Fassungen 15:31, 16:00 und 16:05 Sitzungsuhr, gültig 16:05, Projektkopie `claude/`) · `03_Skripte\\Textvorschlag_6.1_2026-10-02.py` mit `.txt` (Messprotokoll) und `.json` (Wortlaut je Absatz für den Einbau) · `03_Skripte\\tv61_md.py` (Erzeuger des Dokuments) · `03_Skripte\\T1_T4_Nachtrag_2026-10-02.py` mit `.txt` · `03_Skripte\\Steuerung_Rev149_2026-10-02.py` mit `.txt`. Geändert: `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (75 Steckbriefe) und `T4_zitierfallen.csv` (158 Zitierfallen) · diese Notizen (Rev. 149 auf Rev. 148) · Maßnahmenliste (Stand, H13, G29, G32, G35 Vermerke, Taskzeilen 12 und 13, Summe), je Ordner und Projektkopie. Durch diesen Task unverändert: Master (42.318 Byte, MD5 `caa5dee2…`, 6.1 leer), Kennzahlenblatt, Zahlenliste, Fassung 17, Plan, Berichtsraster, Befunde Rev. 147 und 148, Prompt Boumparis. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen (acht Dateien 16:00, zwei Dateien 16:04).

**Nächster Schritt:** Task „Boumparis“ (Rev. 148, Startsatz Plan § 8), dann Freigabe und Einbau von 6.1 in Task 12a mit dem freigegebenen Modul oder ohne (Startsatz: „Weiter mit Task 12a: Freigabe und Einbau 6.1 nach `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` § 8 und dem Nachtrag K2“), danach Task 12b. Reihenfolge sonst wie Rev. 146.

"""

STAND_ALT_N = '**Stand: (Rev. 148 — siehe Block oben.) Zuvor: '
STAND_NEU_N = '**Stand: (Rev. 149 — siehe Block oben.) Zuvor: (Rev. 148 — siehe Block oben.) Zuvor: '
ANKER_148 = '### ⭐ NACHTRAG (Rev. 148, 02.10.2026, 15:46 Sitzungsuhr, Auftrag 15:28):'

STAND_ALT_M = '**Stand 02.10.2026, 15:46 Sitzungsuhr (Rev. 148 — '
STAND_NEU_M = ('**Stand 02.10.2026, 16:12 Sitzungsuhr (Rev. 149 — Task 12a: Textvorschlag 6.1 „Einordnung der Ergebnisse“ '
               '`04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` mit 700 Wörtern und unabhängiger Zweitprüfung vorgelegt, Klicks K1 bis K7, '
               'K5 umgesetzt, T1 um drei Steckbriefe und T4 um sechs Zitierfallen ergänzt, Freigabe und Einbau zurückgestellt bis zum Task '
               '„Boumparis“. H13, G29, G32, G35 Vermerke, Taskzeilen 12 und 13 fortgeschrieben). Zuvor 02.10.2026, 15:46 Sitzungsuhr (Rev. 148 — ')

H13_ANKER = ('Vor der Zitation T1-Steckbrief und T4-Prüfung, die übrigen Posten bleiben offen.)*')
H13_NEU = (H13_ANKER + ' *(Rev. 149, 02.10.: Klusemann et al. (2012), Rogers et al. (2020) und Veith et al. (2021) am Volltext gelesen, '
           'T1-Steckbriefe und T4-Zitierfallen per `03_Skripte\\T1_T4_Nachtrag_2026-10-02.py` angelegt (Task 12a). Klusemann et al. (2012) steht '
           'vorläufig im Modul A2-M des Textvorschlags 6.1, Rogers und Veith bleiben Reserve (Textvorschlag 6.1 § 5, § 8 Nr. 1), der Vergleichssatz '
           'entsteht im Task „Boumparis“. Die übrigen Posten bleiben offen.)*')

G29_ANKER = '- [ ] **G29 · Vormerkungen aus dem Task 4.7 (25.09., Rev. 95, Textvorschlag § 10):**'
G29_VERMERK = (' *(Rev. 149, 02.10.: (f) 6.1 nennt keinen dieser Posten, alle bleiben für 12b, Textvorschlag 6.1 § 9.1 Nr. 1, 4, 5 und 8.)*')
G32_ANKER = '- [ ] **G32 · Vormerkungen aus Task 6 (4.7, 26.09., Rev. 107 und 108, Wortlaut in `04_Uebergaben\\Textvorschlag_4.7_2026-09-26.md` § 7):**'
G32_VERMERK = (' *(Rev. 149, 02.10.: (c) 6.1-Teil im Textvorschlag 6.1 umgesetzt (Wirkung des Programmangebots und Verdünnung in A2, '
               'Per-Protokoll beobachtend), die 6.2/6.3-Teile bleiben für 12b (Planungsmodell, Power, Trennschärfe, Analyseeinheit, Familiarisierung, '
               'Familienfehler, Freigabe ohne Methodenprüfung, Restrisiko ohne Zweiterfassung), Textvorschlag 6.1 § 9.1.)*')
G35_ANKER = '- [ ] **G35 ·'
G35_VERMERK = (' *(Rev. 149, 02.10.: (j) in 6.1 umgesetzt: Ankersatz als A1 S1 ohne „deshalb“, Zheng 2025 und Ramirez-Campillo 2023 beim 505 (A4), '
               'Lloyd 2016 nach L14 b (A5 S6, Veränderung innerhalb der Gruppe). Nicht in 6.1: Bouafif 2026 (Verzichtstabelle, Elitepopulation ohne '
               'Mehrwert gegenüber den Metaanalysen), Flores 2025 (6.2), Behm 2017 und de Villarreal 2009 (G8), Hilska 2021 (G5/G3). Vormerkung für die '
               'Schlussfassung der Einleitung in Textvorschlag 6.1 § 9.3.)*')

TASK12_ANKER = ('Task „Boumparis“ (Rev. 148): Vergleichssatz für das Modul A2-M (K2) und Satzkerne für 12b, Prompt '
                '`04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md` |')
TASK12_NEU = ('Task „Boumparis“ (Rev. 148): Vergleichssatz für das Modul A2-M (K2) und Satzkerne für 12b, Prompt '
              '`04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md` · Textvorschlag 6.1 (Rev. 149, '
              '`04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md`): Wortlaut 700 Wörter zweitgeprüft, K5 umgesetzt, Freigabe (K6) und Einbau per '
              'Skript (K7) nach dem Task „Boumparis“, Vormerkungen § 9.1 (12b) |')
TASK13_ANKER = 'Task „Boumparis“ (Rev. 148), Satzkern für den Ausblick |'
TASK13_NEU = ('Task „Boumparis“ (Rev. 148), Satzkern für den Ausblick · Textvorschlag 6.1 (Rev. 149) § 9.2 (13a: Hauptbefund in der Sprache von A1, '
              'Zeitverlauf der Weite offen, keine Programmdauer-Empfehlung, Umsetzung als Erkenntnisaspekt) |')
SUMME_ANKER = '| **Summe** | Rev. 148 (02.10.): '
SUMME_NEU = ('| **Summe** | Rev. 149 (02.10.): H13, G29, G32 und G35 Vermerke, Taskzeilen 12 und 13 fortgeschrieben, keine neuen Punkte, '
             'Zählung nicht neu erhoben. Zuvor: Rev. 148 (02.10.): ')


def md5(pfad):
    return hashlib.md5(open(pfad, 'rb').read()).hexdigest()


def lese(pfad):
    with open(pfad, encoding='utf-8', newline='') as f:
        return f.read()


def schreibe(pfad, text):
    with open(pfad, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Anker „%s“ kommt %d-mal vor, erwartet 1' % (name, n))
    protokoll.append('  %s: Anker gefunden (1x), ersetzt' % name)
    return text.replace(alt, neu)


def haenge_an_zeile(text, zeilenanker, zusatz, name, protokoll):
    n = text.count(zeilenanker)
    if n != 1:
        raise SystemExit('Zeilenanker „%s“ kommt %d-mal vor, erwartet 1' % (name, n))
    i = text.index(zeilenanker)
    ende = text.index('\n', i)
    protokoll.append('  %s: Zeile gefunden, Vermerk angehängt (%d Zeichen)' % (name, len(zusatz)))
    return text[:ende] + zusatz + text[ende:]


def main():
    quelle, ziel = sys.argv[1], sys.argv[2]
    os.makedirs(ziel, exist_ok=True)
    protokoll = ['Steuerung Rev. 149 (02.10.2026, Task 12a) — Protokoll']
    zeilenende = '\n'
    # Notizen
    qn = os.path.join(quelle, NOTIZEN)
    t = lese(qn)
    if '\r\n' in t:
        zeilenende = '\r\n'
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s, Zeilenende %s' % (NOTIZEN, len(t.encode('utf-8')), t.count('\n'), md5(qn), repr(zeilenende)))
    t = ersetze(t, STAND_ALT_N, STAND_NEU_N, 'Stand-Zeile Notizen', protokoll)
    eintrag = EINTRAG_149.replace('\n', zeilenende) if zeilenende != '\n' else EINTRAG_149
    t = ersetze(t, ANKER_148, eintrag + ANKER_148, 'Eintrag Rev. 149 vor Rev. 148', protokoll)
    zn = os.path.join(ziel, NOTIZEN)
    schreibe(zn, t)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (NOTIZEN, os.path.getsize(zn), t.count('\n'), md5(zn)))
    # Maßnahmenliste
    qm = os.path.join(quelle, MASSNAHMEN)
    m = lese(qm)
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, len(m.encode('utf-8')), m.count('\n'), md5(qm)))
    m = ersetze(m, STAND_ALT_M, STAND_NEU_M, 'Stand-Zeile Maßnahmenliste', protokoll)
    m = ersetze(m, H13_ANKER, H13_NEU, 'H13 Vermerk', protokoll)
    m = haenge_an_zeile(m, G29_ANKER, G29_VERMERK, 'G29 Vermerk', protokoll)
    m = haenge_an_zeile(m, G32_ANKER, G32_VERMERK, 'G32 Vermerk', protokoll)
    m = haenge_an_zeile(m, G35_ANKER, G35_VERMERK, 'G35 Vermerk', protokoll)
    m = ersetze(m, TASK12_ANKER, TASK12_NEU, 'Taskzeile 12', protokoll)
    m = ersetze(m, TASK13_ANKER, TASK13_NEU, 'Taskzeile 13', protokoll)
    m = ersetze(m, SUMME_ANKER, SUMME_NEU, 'Summe', protokoll)
    zm = os.path.join(ziel, MASSNAHMEN)
    schreibe(zm, m)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, os.path.getsize(zm), m.count('\n'), md5(zm)))
    # Rücklesen
    for n in (NOTIZEN, MASSNAHMEN):
        r = lese(os.path.join(ziel, n))
        protokoll.append('%s rückgelesen: Rev. 149 %s' % (n, 'enthalten' if 'Rev. 149' in r else 'FEHLT'))
    with open(os.path.join(ziel, 'Steuerung_Rev149_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Steuerung Rev. 150 (02.10.2026, Task 12a, Nachtrag): Probelauf des Einbauskripts 6.1 in Teil 0 und Maßnahmenliste.

Liest die beiden Steuerdokumente aus dem Quellordner (frisch gestagter Ordnerstand, Rev. 149), prüft die Anker,
setzt den Nachtrag Rev. 150 an den Kopf von Teil 0, schreibt die Stand-Zeilen fort, ergänzt in der Maßnahmenliste
die Taskzeile 12 und die Summe. Jeder Anker muss genau einmal vorkommen, sonst bricht das Skript ab.
Ausgabe in den Zielordner mit Protokoll (Zeilen, Bytes, MD5 vorher und nachher). Ohne Semikolon im Skript (chr(59)).

Aufruf: python3 Steuerung_Rev150_2026-10-02.py <Quellordner> <Zielordner>
"""
import hashlib
import os
import sys

SEMI = chr(59)
NOTIZEN = 'Cowork_Sitzungsnotizen.md'
MASSNAHMEN = 'Massnahmenliste_Datenverarbeitung.md'

EINTRAG_150 = """### ⭐ NACHTRAG (Rev. 150, 02.10.2026, 16:45 Sitzungsuhr, Auftrag 16:34 „weitermachen wo du aufgehört hast“): Task 12a — Einbau- und Abgleichskript für 6.1 bereitgestellt und an einer Kopie des Masters geprüft, kein Einbau

**Einordnung:** Fortsetzung von Rev. 149 im selben Task. Die Freigabe des Wortlauts steht bis zum Task „Boumparis“ aus (K6), die Version of Record von Boumparis et al. (2026) lag um 16:35 Sitzungsuhr noch nicht in `Ideen und Studien` (nur der Preprint, Rev. 148), der Nachtrag K2 liegt nicht vor. Vorbereitet wurde deshalb der Schritt, der nach der Freigabe folgt (K7, Einbau per Skript), ohne den Master anzufassen.

**Ergebnis:** `03_Skripte\\Master_6_1_2026-10-02.py` (Einbau der Absätze aus `Textvorschlag_6.1_2026-10-02.json` unter „6.1 Einordnung der Ergebnisse“, vor „6.2 Methodendiskussion“, Formatvorlage Standard, jede Operation genau einmal, Modul-Einträge der JSON werden nicht eingebaut, sondern gemeldet, Budgetprüfung gegen die JSON) · `03_Skripte\\Abgleich_Kapitel6_1_Master_2026-10-02.py` (nur lesend: comments.xml, Absatzfolge gegen die Referenz, 6.1 zeichengleich mit der JSON, Formatvorlage und Direktformatierung, Wortzahl je Absatz, Überschriften 6 bis 7, 6.2 und 6.3 leer, Sprachprüfungen) · Protokoll `03_Skripte\\Master_6_1_2026-10-02_Probelauf.txt`. Probelauf an einer Kopie des Masters (MD5 `caa5dee2…`, 42.318 Byte): sechs Absätze A1 bis A6 mit 700 Wörtern eingefügt, A2-M als offenes Modul gemeldet, 182 → 188 Absätze, Abgleich ohne Befund, Abgleich Probe gegen Original zeigt nur die sechs neuen Absätze, `validate.py` des docx-Skills bestanden, Messskript Fassung 4 an der Probe: 6.1 700 gegen 700, Absatztext 4.496 gegen 6.350, Prognose 27,8 Seiten (Modellrechnung, wie Rev. 146, weil das Budget schon eingerechnet war), LibreOffice-Rendering gesichtet (6.1 auf Seite 14 des Textteils, Blocksatz, keine Direktformatierung). Textvorschlag 6.1 § 11.1 trägt den Probelauf, § 11.2 den Ablauf nach der Freigabe, § 0 die Seitenprognose.

**Offen beim Verfasser:** unverändert Rev. 149: (1) Version of Record ablegen und Task „Boumparis“ eröffnen (Rev. 148, Startsatz Plan § 8) · (2) danach Klickfreigabe des Wortlauts 6.1 je Absatz, A2 und A2-M nach dem Nachtrag K2 · (3) Einbau per Skript durch Claude nach Textvorschlag 6.1 § 11.2.

**Stand der Dateien:** Neu: `03_Skripte\\Master_6_1_2026-10-02.py` · `03_Skripte\\Abgleich_Kapitel6_1_Master_2026-10-02.py` · `03_Skripte\\Master_6_1_2026-10-02_Probelauf.txt` · `03_Skripte\\Steuerung_Rev150_2026-10-02.py` mit `.txt`. Geändert: `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` (81.240 Byte, MD5 `6afeed18…`, § 0 und § 11, Projektkopie `claude/`) · `03_Skripte\\tv61_md.py` · diese Notizen (Rev. 150 auf Rev. 149) · Maßnahmenliste (Stand, Taskzeile 12, Summe), je Ordner und Projektkopie. Unverändert: Master (42.318 Byte, MD5 `caa5dee2…`, 6.1 leer), Kennzahlenblatt, Zahlenliste, T1, T4, Fassung 17, Plan. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** wie Rev. 149: Task „Boumparis“, dann Freigabe und Einbau 6.1 (Startsatz: „Weiter mit Task 12a: Freigabe und Einbau 6.1 nach `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` § 8 und § 11.2 und dem Nachtrag K2“), danach Task 12b.

"""

STAND_ALT_N = '**Stand: (Rev. 149 — siehe Block oben.) Zuvor: '
STAND_NEU_N = '**Stand: (Rev. 150 — siehe Block oben.) Zuvor: (Rev. 149 — siehe Block oben.) Zuvor: '
ANKER_149 = '### ⭐⭐ NEU (Rev. 149, 02.10.2026, 16:12 Sitzungsuhr, Auftrag: Prompt Task 12a nach Rev. 146):'

STAND_ALT_M = '**Stand 02.10.2026, 16:12 Sitzungsuhr (Rev. 149 — '
STAND_NEU_M = ('**Stand 02.10.2026, 16:45 Sitzungsuhr (Rev. 150 — Task 12a, Nachtrag: Einbauskript `03_Skripte\\Master_6_1_2026-10-02.py` und '
               'Abgleichskript `Abgleich_Kapitel6_1_Master_2026-10-02.py` an einer Kopie des Masters geprüft (Protokoll `Master_6_1_2026-10-02_Probelauf.txt`), '
               'kein Einbau, Master unverändert, Taskzeile 12 fortgeschrieben). Zuvor 02.10.2026, 16:12 Sitzungsuhr (Rev. 149 — ')

TASK12_ANKER = ('Wortlaut 700 Wörter zweitgeprüft, K5 umgesetzt, Freigabe (K6) und Einbau per '
                'Skript (K7) nach dem Task „Boumparis“, Vormerkungen § 9.1 (12b) |')
TASK12_NEU = ('Wortlaut 700 Wörter zweitgeprüft, K5 umgesetzt, Freigabe (K6) und Einbau per '
              'Skript (K7) nach dem Task „Boumparis“, Vormerkungen § 9.1 (12b) · Einbau- und Abgleichskript bereit und an einer Kopie geprüft '
              '(Rev. 150, Textvorschlag 6.1 § 11.1 und § 11.2) |')
SUMME_ANKER = '| **Summe** | Rev. 149 (02.10.): '
SUMME_NEU = ('| **Summe** | Rev. 150 (02.10.): Taskzeile 12 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. '
             'Zuvor: Rev. 149 (02.10.): ')


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


def main():
    quelle, ziel = sys.argv[1], sys.argv[2]
    os.makedirs(ziel, exist_ok=True)
    protokoll = ['Steuerung Rev. 150 (02.10.2026, Task 12a, Nachtrag) — Protokoll']
    qn = os.path.join(quelle, NOTIZEN)
    t = lese(qn)
    zeilenende = '\r\n' if '\r\n' in t else '\n'
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s, Zeilenende %s' % (NOTIZEN, len(t.encode('utf-8')), t.count('\n'), md5(qn), repr(zeilenende)))
    t = ersetze(t, STAND_ALT_N, STAND_NEU_N, 'Stand-Zeile Notizen', protokoll)
    eintrag = EINTRAG_150.replace('\n', zeilenende) if zeilenende != '\n' else EINTRAG_150
    t = ersetze(t, ANKER_149, eintrag + ANKER_149, 'Eintrag Rev. 150 vor Rev. 149', protokoll)
    zn = os.path.join(ziel, NOTIZEN)
    schreibe(zn, t)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (NOTIZEN, os.path.getsize(zn), t.count('\n'), md5(zn)))
    qm = os.path.join(quelle, MASSNAHMEN)
    m = lese(qm)
    protokoll.append('%s: vorher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, len(m.encode('utf-8')), m.count('\n'), md5(qm)))
    m = ersetze(m, STAND_ALT_M, STAND_NEU_M, 'Stand-Zeile Maßnahmenliste', protokoll)
    m = ersetze(m, TASK12_ANKER, TASK12_NEU, 'Taskzeile 12', protokoll)
    m = ersetze(m, SUMME_ANKER, SUMME_NEU, 'Summe', protokoll)
    zm = os.path.join(ziel, MASSNAHMEN)
    schreibe(zm, m)
    protokoll.append('%s: nachher %d Byte, %d Zeilen, MD5 %s' % (MASSNAHMEN, os.path.getsize(zm), m.count('\n'), md5(zm)))
    for n in (NOTIZEN, MASSNAHMEN):
        r = lese(os.path.join(ziel, n))
        protokoll.append('%s rückgelesen: Rev. 150 %s' % (n, 'enthalten' if 'Rev. 150' in r else 'FEHLT'))
    with open(os.path.join(ziel, 'Steuerung_Rev150_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

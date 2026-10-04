# -*- coding: utf-8 -*-
"""
Spezifikation_Nachtrag3_2026-09-25.py — Nachtrag 3 (Teil F.8) in die Spezifikation einarbeiten und die Zahlenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln · Auswertungsverfahren 2026-09-24 (Rev. 87), Schritt 2.1 (Nachträge nach F1)

Zweck: Die vier Klarstellungen C.1 bis C.4 aus der Code-Durchsicht der Phase 6.2
(02_Befunde\\Durchsichtsprotokoll_2026-09-25, Teil C) als datierter Nachtrag 3 (N5.1 bis N5.4) in
Spezifikation_2026-09-24.md einsetzen: Kopf, Deckblatt, 0.5 Nr. 11, S05 Regel 9, F.7 N4.3, G.1 Nr. 4
und Nr. 6 sowie ein neuer Abschnitt F.8. Danach wird die Anlage _Zahlenliste.csv (Teil H) neu erzeugt:
Jede Ziffernfolge des neuen Texts wird nach derselben Zerlegungsregel wie im Blindprüfungsskript
ausgelesen. Unveränderte Zeilen übernehmen Art und Herkunft aus der bisherigen Liste, neue oder
geänderte Zeilen erhalten Art und Herkunft aus der Tabelle NEU unten. Jede Textänderung wird als
genau ein Treffer geprüft, sonst bricht das Skript ab.

Eingang: Spezifikation_2026-09-24.md und _Zahlenliste.csv im Stand Nachtrag 2 (Kopie), Aufruf mit Ordner
Aufruf: python Spezifikation_Nachtrag3_2026-09-25.py <Ordner mit Spezifikation_2026-09-24.md und _Zahlenliste.csv>
Ausgabe: beide Dateien im Stand Nachtrag 3 (überschrieben), Meldung mit Zahl der Änderungen
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import os
import csv
import re
import collections
import hashlib

ORDNER = sys.argv[1]
MD = os.path.join(ORDNER, 'Spezifikation_2026-09-24.md')
ZL = os.path.join(ORDNER, 'Spezifikation_2026-09-24_Zahlenliste.csv')
alt_text = open(MD, encoding='utf-8').read()
alt_zl = list(csv.DictReader(open(ZL, encoding='utf-8')))
sha_alt = hashlib.sha256(alt_text.encode('utf-8')).hexdigest()

# ---------------------------------------------------------------- Textänderungen (alt → neu), jede genau einmal
AENDERUNGEN = [
    ('**Bachelorarbeit U15-Plyometrie · DSHS Köln · Stand 24.09.2026 · freigegeben (F1), Nachtrag 1 und Nachtrag 2**',
     '**Bachelorarbeit U15-Plyometrie · DSHS Köln · Stand 24.09.2026 · freigegeben (F1), Nachtrag 1 und Nachtrag 2 (24.09.2026), Nachtrag 3 (25.09.2026)**'),
    ('## Deckblatt (Freigabe F1, Nachtrag 1 und Nachtrag 2 am 24.09.2026)',
     '## Deckblatt (Freigabe F1, Nachtrag 1 und Nachtrag 2 am 24.09.2026, Nachtrag 3 am 25.09.2026)'),
    ('**Nachtrag 2 (Teil F.7):** Ausgabe auf die berichteten und für Prüfungen gebrauchten Größen beschränkt · Menge ANA für die Stichprobenbeschreibung · Mittel der Kovariaten im ITT-Set als Ausgabe · P7 eingeschränkt, P1 und P3 ohne Anwendung.\n',
     '**Nachtrag 2 (Teil F.7):** Ausgabe auf die berichteten und für Prüfungen gebrauchten Größen beschränkt · Menge ANA für die Stichprobenbeschreibung · Mittel der Kovariaten im ITT-Set als Ausgabe · P7 eingeschränkt, P1 und P3 ohne Anwendung.\n\n'
     '**Nachtrag 3 (Teil F.8):** vier Klarstellungen aus der Code-Durchsicht der Phase 6.2, nach bestandenem Abgleich beider Implementierungen: Vorrang des Grunds „Eingang fehlt“ in S05 · Bezugsmenge von Median und Mittel der Adhärenz in N4.3 · Rangkriterium der Designmatrix · Dateinamen der Grafiken der Gegenprobe. Keine Regel der Hauptanalyse, keine Kennung und kein Referenztest ändert sich.\n'),
    ('F1: Verfasser, 24.09.2026. Nachtrag 2: Verfasser, 24.09.2026. Referenztests R01 bis R13 vor der Studienrechnung (Teil G).',
     'F1: Verfasser, 24.09.2026. Nachtrag 2: Verfasser, 24.09.2026. Nachtrag 3: Verfasser, 25.09.2026. Referenztests R01 bis R13 vor der Studienrechnung (Teil G).'),
    ('11. Eine Analyse, deren Designmatrix nicht vollen Rang hat, wird nicht gerechnet. Ihre Kennungen werden als fehlend mit Grund ausgegeben.',
     '11. Eine Analyse, deren Designmatrix nicht vollen Rang hat, wird nicht gerechnet. Ihre Kennungen werden als fehlend mit Grund ausgegeben. Der Rang wird nach einer QR-Zerlegung mit der Toleranz 1e-7 auf der spaltenskalierten Designmatrix bestimmt oder mit einem gleichwertigen Kriterium (Nachtrag 3, N5.3, Klarstellung).'),
    ('9. Fehlt ein Eingang, auch nur eine Elterngröße, ist %PAH fehlend (K2).',
     '9. Fehlt ein Eingang, auch nur eine Elterngröße, ist %PAH fehlend (K2). Der Grund lautet dann „Eingang fehlt“, auch wenn zugleich das Alter außerhalb des Gültigkeitsbereichs der Regel 4 liegt (Nachtrag 3, N5.1).'),
    ('· Median und Mittel über Spieler mit Meldung, GTWOCAP und GTDIST entfallen |',
     '· Median und Mittel über die zugeteilten Spieler, Spieler ohne Listenplatz mit 0 (so Regel 7 und die Kennungsanlage, Nachtrag 3, N5.2), GTWOCAP und GTDIST entfallen |'),
    ('· „nicht erhebbar“ · „keine Nullstelle“. Weitere Gründe nur mit Rückfrage.',
     '· „nicht erhebbar“ · „keine Nullstelle“. Weitere Gründe nur mit Rückfrage. Treffen mehrere Gründe zu, gilt der in der Regel zuerst geprüfte, in S05 „Eingang fehlt“ vor „außerhalb Gültigkeitsbereich“ (Nachtrag 3, N5.1).'),
    ('6. Grafiken aus S14 Regel 1 und Regel 4 als Dateien `S14_QQ_<ZIEL>` und `S14_Linearitaet_<ZIEL>` im Format PNG oder PDF, ohne Kennung.',
     '6. Grafiken aus S14 Regel 1 und Regel 4 als Dateien `S14_QQ_<ZIEL>` und `S14_Linearitaet_<ZIEL>` im Format PNG oder PDF, ohne Kennung. Die Gegenprobe darf ihren Dateinamen den Zusatz `_Python` anhängen (Nachtrag 3, N5.4).'),
    ('Unverändert bleiben S01 bis S05, S11, S14, S19, Teil G und die Referenztests R01 bis R13.\n',
     'Unverändert bleiben S01 bis S05, S11, S14, S19, Teil G und die Referenztests R01 bis R13.\n\n'
     '### F.8 Nachtrag 3 nach der Freigabe F1 (25.09.2026)\n\n'
     'Grundlage: Code-Durchsicht über Kreuz der Phase 6.2 (`02_Befunde\\Durchsichtsprotokoll_2026-09-25`, Teil C), Entscheidung des Verfassers am 25.09.2026 nach bestandenem Abgleich 6.1. Beide Implementierungen hatten die vier Stellen bereits gleich gelesen. Der Nachtrag hält die Lesart schriftlich fest. Er ändert keine Regel der Hauptanalyse, keine Kennung und keinen Referenztest. Dass er keinen Wert der Ergebnisdatei berührt, hält das Durchsichtsprotokoll fest.\n\n'
     '| Nr. | Klarstellung | Stelle | Grund |\n'
     '|---|---|---|---|\n'
     '| N5.1 | Fehlt ein Eingang, gilt der Grund „Eingang fehlt“, auch bei Alter außerhalb des Gültigkeitsbereichs | S05 Regel 9, G.1 Nr. 4 | Der Vorrang der Gründe war nicht festgelegt. Beide Implementierungen prüfen den fehlenden Eingang zuerst |\n'
     '| N5.2 | Median und Mittel der Adhärenz GANZ über die zugeteilten Spieler, Spieler ohne Listenplatz mit 0 | F.7 N4.3, S07 Regel 7 | N4.3 sagte „über Spieler mit Meldung“, Regel 7 und die Kennungsanlage („je zugeteiltem Spieler“) nennen die zugeteilten Spieler. Beide Implementierungen rechnen so |\n'
     '| N5.3 | Rang der Designmatrix nach QR-Zerlegung mit Toleranz 1e-7 auf der spaltenskalierten Matrix oder gleichwertig | 0.5 Nr. 11 | Das Rangkriterium war nicht beziffert. Klarstellung, keine neue Regel |\n'
     '| N5.4 | Die Gegenprobe darf den Dateinamen der Grafiken den Zusatz `_Python` anhängen | G.1 Nr. 6 | Die Dateinamen waren nur für eine Implementierung eindeutig |\n'),
]
neu_text = alt_text
for alt, neu in AENDERUNGEN:
    n = neu_text.count(alt)
    if n != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden (%d): %s' % (n, alt[:80]))
    neu_text = neu_text.replace(alt, neu)
neu_zeilen = neu_text.split('\n')
alt_zeilen = alt_text.split('\n')

# ---------------------------------------------------------------- Zahlenliste neu (Zerlegung wie Direktscan des Blindprüfungsskripts)
TOK = re.compile(r'''(?<![A-Za-zÄÖÜäöüß0-9.,\-])(
   \d{1,2}\.\d{1,2}\.(?:\d{4})?(?!\d)
 | \d{1,2}:\d{2}(?::\d{2})?
 | \d+e-\d+
 | \d+(?:[.,]\d+)?
)''', re.X)

# Bisherige Einträge je (Zeilentext, laufende Nummer des Vorkommens)
alt_je_zeile = collections.defaultdict(list)
for r in alt_zl:
    alt_je_zeile[int(r['zeile'])].append(r)
alt_eintraege = {}   # (Zeilentext, Index) → Eintrag
for nr, eintraege in alt_je_zeile.items():
    text = alt_zeilen[nr - 1]
    for k, r in enumerate(eintraege):
        alt_eintraege[(text, k)] = r

# Art und Herkunft für Zahlen in neuen oder geänderten Zeilen
NEU = {
    '25.09.2026': ('Datum', 'Dokumentdatum: Datum des Nachtrags 3 (Teil F.8, Verfasserentscheidung nach der Code-Durchsicht 6.2)'),
    '24.09.2026': ('Datum', 'Dokumentdatum: Datum der Festlegungen und dieser Spezifikation'),
    '1e-7': ('Regel', 'Toleranz der Rangbestimmung der QR-Zerlegung (0.5 Nr. 11, Nachtrag 3, N5.3, Klarstellung nach Durchsichtsprotokoll 6.2 Teil A.3 Nr. 2)'),
    '0': ('Code, Index oder Formelkonstante', 'Wertebereich, Index, Merkmal oder Konstante der Formel an dieser Stelle (Datenformat 0.4, Codebuch, Formel des Schritts)'),
}
GLIEDERUNG = ('Gliederung', 'Verweis auf Regel, Schritt, Phase, Fassung oder Abschnitt')
NACHTRAG = ('Gliederung', 'Nummer eines Nachtrags zur Spezifikation (Teil F)')
UEBERSCHRIFT = ('Gliederung', 'Nummer einer Überschrift')


def abschnitt_von(zeilen, i):
    for j in range(i, -1, -1):
        if zeilen[j].startswith('#'):
            return zeilen[j].lstrip('#').strip()
    return ''


def einordnung(zahl, zeile, pos):
    vor = zeile[max(0, pos - 12):pos]
    if re.search(r'Nachtrag\s*$', vor):
        return NACHTRAG
    if zeile[:pos].count('`') % 2 == 1:
        return ('Gliederung', 'Ordner- oder Dateiname')
    if zeile.startswith('#'):
        return UEBERSCHRIFT
    if pos == 0 and re.match(r'\d+\. ', zeile):
        return ('Gliederung', 'Nummer eines Listenpunkts')
    if vor.endswith('S. '):
        return ('Fundstelle', 'Seitenzahl einer Quelle')
    if zahl == '0' and vor.endswith('mit '):
        return NEU['0']
    if zahl in NEU and zahl != '0':
        return NEU[zahl]
    return GLIEDERUNG


neu_zl = []
n_neu, n_alt = 0, 0
alt_texte = set(alt_zeilen)
for i, line in enumerate(neu_zeilen, start=1):
    toks = [(m.group(1), m.start(1)) for m in TOK.finditer(line)]
    if not toks:
        continue
    if line in alt_texte and all((line, k) in alt_eintraege for k in range(len(toks))):
        for k, (z, pos) in enumerate(toks):
            r = dict(alt_eintraege[(line, k)])
            if r['zahl'] != z:
                raise SystemExit('Zahl weicht in unveränderter Zeile ab: Zeile %d, %s gegen %s' % (i, r['zahl'], z))
            r['zeile'] = str(i)
            neu_zl.append(r)
            n_alt += 1
    else:
        for z, pos in toks:
            art, herkunft = einordnung(z, line, pos)
            neu_zl.append({'zeile': str(i), 'abschnitt': abschnitt_von(neu_zeilen, i - 1), 'zahl': z, 'art': art,
                           'herkunft': herkunft, 'textumgebung': line[max(0, pos - 80):pos + len(z) + 40]})
            n_neu += 1

with open(MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write(neu_text)
with open(ZL, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['zeile', 'abschnitt', 'zahl', 'art', 'herkunft', 'textumgebung'])
    w.writeheader()
    for r in neu_zl:
        w.writerow(r)
sha_neu = hashlib.sha256(neu_text.encode('utf-8')).hexdigest()
geaendert = sum(1 for l in neu_zeilen if l not in alt_texte)
print('Spezifikation Stand Nachtrag 2 SHA-256 %s → Stand Nachtrag 3 SHA-256 %s' % (sha_alt[:16], sha_neu[:16]))
print('Textänderungen: %d Stellen · Zeilen: %d → %d, davon neu oder geändert: %d' % (len(AENDERUNGEN), len(alt_zeilen), len(neu_zeilen), geaendert))
print('Zahlenliste: %d → %d Vorkommen (%d aus unveränderten Zeilen übernommen, %d neu eingeordnet)' % (len(alt_zl), len(neu_zl), n_alt, n_neu))
print('Semikolons im neuen Text außerhalb von Codeblöcken:', sum(1 for l in neu_zeilen if chr(59) in l and not l.strip().startswith('`')))

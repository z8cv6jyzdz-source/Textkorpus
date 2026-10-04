# -*- coding: utf-8 -*-
"""
Steuerdokumente_README_Archiv_2026-09-28.py — Folgeänderungen des Tasks Steuerdokumente 28.09. (Übergabe
`04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 5.4 bis § 5.6, Rev. 114 „Übergabe Einleitung weitgehend
verbraucht“):
  (1) Übergabe Einleitung: Kopf, Seitenzeilen in § 2 nach K1 bis K3 und Seitenmodell, Ankersatz nach K6, Zeile 3.3 nach
      G32 (e), Verweise auf Fassung 17 und Berichtsraster Rev. 3, § 8 Nr. 6 und Nr. 7 auf den Stand nach Rev. 115
  (2) README_Ordnerstruktur.md: Kopf, Ordnerzeilen, „Was wo gilt“ mit „Stand in Kürze“ und überholten Teilen, Papierkorbliste
  (3) Ordner_aufraeumen.ps1 (BOM und CRLF bleiben): Kopf, Papierkorbliste um die Originale mit Archivkopie, Muster 00_Steuerung
  (4) Archivkopien in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente` und `_Archiv\\_ersetzt_2026-09-28_Uebergaben`
Mit --fassung16 kommen Archivkopie, Papierkorbeintrag und README-Vermerk für Fassung 16 dazu (nur nach der Klickantwort
„Fassung 17 freigeben“, Maßnahme A8, Übergabe § 5.5: „Fassung 16 kommt erst nach dem Einsetzen von Fassung 17 in die Liste“).
Jede Textstelle wird genau einmal ersetzt, sonst Abbruch. Zahlen kommen aus Seitenmodell, Messskript Fassung 3 und dem Kopf
des Textvorschlags Einleitung, keine von Hand. Das Skript enthält kein Semikolon (chr(59)).
Fassung 2 (28.09., nach der übergreifenden Zweitprüfung der Steuerdokumente): Übergabe Einleitung § 4 Zeile 1.3 nach Berichtsraster
Rev. 3, § 8 Nr. 6 mit G31 (c) und G35 (i), README Zeile 00_Steuerung und Schritt 6 an die Folge nach A8 gebunden, Vorstände von README,
Aufräumskript und Übergabe Einleitung als Archivkopie (Übergabe Steuerdokumente § 0).

Aufruf: python Steuerdokumente_README_Archiv_2026-09-28.py <Quelle Claude-Ordner (gestagte Originale)> <Ziel Claude-Ordner>
        <Seitenmodell.csv> <Manuskriptstand.txt> <Manuskriptstand.csv> [--fassung16]
"""
import csv
import hashlib
import os
import re
import shutil
import sys

QUELLE, ZIEL, S_CSV, M_TXT, M_CSV = sys.argv[1:6]
MIT_F16 = '--fassung16' in sys.argv
SEMI = chr(59)
PROTOKOLL = []


def ersetze(text, alt, neu, stelle):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('ABBRUCH: %s: Fundstelle %d-mal statt genau einmal: %s' % (stelle, n, alt[:100]))
    PROTOKOLL.append(stelle)
    return text.replace(alt, neu)


def zeile(text, praefix, neu, stelle):
    zl = text.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('ABBRUCH: %s: %d Zeilen beginnen mit %s' % (stelle, len(idx), praefix[:80]))
    zl[idx[0]] = neu
    PROTOKOLL.append(stelle)
    return '\n'.join(zl)


def de(x, nk=0):
    s = ('%.' + str(nk) + 'f') % x
    ganz, _, dez = s.partition('.')
    g = []
    while len(ganz) > 3:
        g.insert(0, ganz[-3:])
        ganz = ganz[:-3]
    g.insert(0, ganz)
    return '.'.join(g) + (',' + dez if dez else '')


# ------------------------------------------------------------------ Werte aus den Dateien
P = {r['parameter']: r['wert'] for r in csv.DictReader(open(S_CSV, encoding='utf-8'), delimiter=SEMI)}
S_TT = de(float(P['prognose_textteil']), 1)
S_GB = de(float(P['prognose_gesamt_basis']), 1)
S_GO = de(float(P['prognose_gesamt_obere']), 1)
SCHWELLE = int(float(P['schwelle_tauschregel']))
GRENZE = int(float(P['grenze_verfasser']))
mess = open(M_TXT, encoding='utf-8').read()
m_mp = re.findall(r'Prognose Einleitung bis Ende Literaturverzeichnis: (\d+,\d) Seiten', mess)
if len(m_mp) != 1:
    raise SystemExit('ABBRUCH: Prognose des Messskripts nicht eindeutig')
MP = m_mp[0]
w = {r['arbeitsnummer']: int(r['woerter']) for r in csv.DictReader(open(M_CSV, encoding='utf-8'))}
K4 = sum(w[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.4.1', '4.4.2', '4.4.3', '4.5.1', '4.5.2', '4.6', '4.7'])
tv = open(os.path.join(QUELLE, '04_Uebergaben', 'Textvorschlag_Einleitung_2026-09-28.md'), encoding='utf-8').read()
m_tv = re.findall(r'\| Wörter gesamt \| \*\*(\d{1,2}\.\d{3}|\d{3,4})\*\*', tv)
if len(m_tv) != 1:
    raise SystemExit('ABBRUCH: Wortzahl im Kopf des Textvorschlags Einleitung nicht eindeutig')
TVW = m_tv[0]
os.makedirs(os.path.join(ZIEL, '04_Uebergaben'), exist_ok=True)

# ------------------------------------------------------------------ (1) Übergabe Einleitung
p = os.path.join(QUELLE, '04_Uebergaben', 'Uebergabe_Einleitung_2026-09-28.md')
u = open(p, encoding='utf-8').read()
u = ersetze(u, 'Nach Erledigung ins Archiv, zusammen mit `Uebergabe_2.4_Fassung6_2026-09-28.md` und `Uebergabe_Kapitel2_2026-09-26.md`.',
            'Nach Erledigung ins Archiv. `Uebergabe_2.4_Fassung6_2026-09-28.md` und `Uebergabe_Kapitel2_2026-09-26.md` liegen seit Rev. 115 als Kopie in `_Archiv\\_ersetzt_2026-09-28_Uebergaben`, die Originale entfernt das Aufräumskript.',
            'UE Kopf Archiv')
u = ersetze(u, 'Ob der Ankersatz auch in 4.1 wiederkehrt, entscheidet der Task Steuerdokumente (Klick K6). Vor diesem Task läuft der Task Steuerdokumente 28.09. (`04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md`).',
            '**Nachgezogen mit Rev. 115 (28.09., Task Steuerdokumente):** Die Übergabe ist durch den Textvorschlag `04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md` (Rev. 114) weitgehend verbraucht. Offen ist nur § 8 Nr. 6, der Abgleich nach der Übertragung. § 3 und § 5 bleiben als Herleitung stehen, maßgeblich sind Wortlaut, Belegtabelle und Verbleibsliste des Textvorschlags (zum Beispiel entfällt Clemente et al., 2022, dort § 6 Nr. 3). Nachgezogen sind die Seitenzeilen in § 2 (Klicks K1 bis K3, Seitenmodell), der Ankersatz in § 3 Zug 8 und § 4 (Klick K6), Zeile 3.3 in § 4 (G32 e), die Verweise auf Projektanweisungen Fassung 17 und Berichtsraster Rev. 3 sowie § 8. Der Task Steuerdokumente 28.09. (`04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md`) lief parallel zu Task 7 neu.',
            'UE Kopf Rev. 115')
u = ersetze(u, '| Seitenprognose Textteil nach F16 § 1.1 (327 Wörter je Seite, Umbrüche, Objekte) | 30,3 | rund 21 |',
            '| Seitenprognose Textteil, Einleitung bis Fazit (bisher nach F16 § 1.1, neu nach dem Seitenmodell vom 28.09., Modellrechnung) | 30,3 | %s |' % S_TT,
            'UE § 2 Textteil')
u = ersetze(u, '| mit Literaturverzeichnis (Modellrechnung, Übergabe Steuerdokumente § 3.1) | — | rund 25 bis 27 |',
            '| Einleitung bis Ende des Literaturverzeichnisses, ohne Vorspann und Anhang (Zählweise K1, Seitenmodell, Modellrechnung) | — | %s (obere Variante %s) |' % (S_GB, S_GO),
            'UE § 2 mit Literaturverzeichnis')
u = zeile(u, '- **Seiten:**',
          '- **Seiten:** Seit 15:14 gilt die Grenze des Verfassers: höchstens %d Seiten einschließlich Literaturverzeichnis. Gezählt wird von der Einleitung bis zum Ende des Literaturverzeichnisses, ohne Vorspann und Anhang (Klick K1, 28.09.). Das Seitenmodell rechnet mit vollen Budgets %s Seiten, in der oberen Variante %s, das Messskript mit den gemessenen Wörtern %s (Modellrechnung, F17 § 1.1). Regel R6 entfällt (K2). Ein Objekt über die fünf festen hinaus kostet Wörter, sobald die Prognose %d Seiten erreicht (K3). Der Textteil bleibt mit %s Seiten unter dem Rahmen „30 bis 50 Textseiten“ der Prüfungsordnung, der formal nur eine Obergrenze nennt. Die Begründung für das Budget von Teil B in F16 § 1.1 entfällt. Die Einleitung bleibt bei höchstens 1.500 Wörtern, die Seitengrenze ist kein Anlass, sie zu füllen. Aufgefüllt wird nicht.'
          % (GRENZE, S_GB, S_GO, MP, SCHWELLE, S_TT),
          'UE § 2 Seiten')
u = zeile(u, '- **Reihenfolge:**',
          '- **Reihenfolge:** Der Task Steuerdokumente 28.09. lief parallel und ist mit Rev. 115 erledigt (Projektanweisungen Fassung 17, Gliederung v5, Berichtsraster Rev. 3, Plan Rev. 5, Messskript Fassung 3, Seitenmodell). Dieser Task ersetzt die Tasks 7 bis 10 und den Einleitungsteil von Task 14. Danach folgen Task 11 (Kapitel 5), 12, 13, 15 bis 18. Task 14 entfällt.',
          'UE § 2 Reihenfolge')
u = ersetze(u, 'Zweck in einem Satz, der Ankersatz für Methodik und Diskussion ·',
            'Zweck in einem Satz, der Ankersatz. Er kehrt im Eröffnungsabsatz von 6.1 und in der Zusammenfassung nahezu wörtlich wieder, 4.1 bleibt ohne Zwecksatz (K6). Wortlaut entschieden in Task 7 neu: „… gegenüber einer Kontrollgruppe verbessert“ ·',
            'UE § 3 Zug 8 Ankersatz')
u = ersetze(u, 'F16 § 6.5 und § 6.6', 'F17 § 6.5 und § 6.6', 'UE § 3 Zug 6')
u = ersetze(u, '## 4 Pflichtinhalte (Berichtsraster § 3.1 bis § 3.3)',
            '## 4 Pflichtinhalte (Berichtsraster Rev. 3, § 3.1 Kopfblock Einleitung)', 'UE § 4 Überschrift')
u = ersetze(u, '1.3 Forschungsstand knapp und Lücke dreifach (unbeaufsichtigt und videobasiert · unterhalb der Akademieebene · Übergangsperiode in dieser Altersgruppe) ·',
            '1.3 Forschungsstand knapp und Lücke als Kombination: Kontrollierte Studien zu einem unbeaufsichtigten, videobasierten, gerätefreien Heimprogramm in der Sommerpause für Spieler des leistungsorientierten Breitensports um den Wachstumsgipfel fehlen (Berichtsraster Rev. 3 Zeile 1.3, F17 § 6.5, die Formel „unterhalb der Akademieebene“ trägt nicht) ·',
            'UE § 4 Zeile 1.3')
u = ersetze(u, '1.4 Zweck als Ankersatz ·',
            '1.4 Zweck als Ankersatz, Wiederkehr in 6.1 und in der Zusammenfassung, 4.1 ohne Zwecksatz (K6) ·', 'UE § 4 Zeile 1.4')
u = ersetze(u, '3.3 H0 und H1 im Antragswortlaut, auf die Grundgesamtheit bezogen ·',
            '3.3 H0 und H1 nah am Antragswortlaut, einander ergänzend, auf die Grundgesamtheit bezogen (G32 e) ·', 'UE § 4 Zeile 3.3')
u = ersetze(u, '- CONSORT 2a (Hintergrund und Begründung) und 2b (Ziele und Hypothesen) liegen damit vollständig in der Einleitung.',
            '- CONSORT 2a (Hintergrund und Begründung) und 2b (Ziele und Hypothesen) liegen damit vollständig in der Einleitung.\n- Rev. 3 des Berichtsrasters ergänzt die Rollen 2.1 bis 2.5 (je mit dem, was nicht hineingehört) sowie E.1 (Präventionssätze) und E.2 (Zweck des Zielgrößenzugs).',
            'UE § 4 Rev. 3')
u = ersetze(u, '## 5 Verbleibsliste (erster Schritt, per Klick)',
            '## 5 Verbleibsliste (erster Schritt, per Klick)\n\n**Entschieden per Klick in Task 7 neu (Rev. 114),** die Entscheidungen stehen im Textvorschlag Einleitung § 4. Die Tabelle bleibt als Herleitung.',
            'UE § 5 entschieden')
u = ersetze(u, 'Khamis und Roche statt Mirwald (F16 § 6.5)', 'Khamis und Roche statt Mirwald (F17 § 6.5)', 'UE § 5 Mirwald')
u = ersetze(u, '(F16 § 10, Stilprofil)', '(F17 § 10, Stilprofil)', 'UE § 6 Stil')
u = ersetze(u, '(F16 § 6.4, § 7)', '(F17 § 6.4, § 7)', 'UE § 6 Belege')
u = ersetze(u, 'Vor-2020-Halbsatz nach F16 § 6.2.', 'Vor-2020-Halbsatz nach F17 § 6.2.', 'UE § 6 Prävention')
u = ersetze(u, '(Befund Rev. 2 § 4.4, F16 § 11.2b)', '(Befund Rev. 2 § 4.4, F17 § 11.2b)', 'UE § 6 Ausgeschlossen')
u = ersetze(u, 'Berichtsraster `02_Befunde\\Berichtsraster_2026-09-23` § 3.1 bis § 3.3',
            'Berichtsraster `02_Befunde\\Berichtsraster_2026-09-23` Rev. 3, § 3.1 Kopfblock Einleitung', 'UE § 7 Nr. 4')
u = ersetze(u, '## 8 Verfahren\n', '## 8 Verfahren\n\nSchritte 1 bis 5 sind mit Rev. 114 erledigt (Textvorschlag Einleitung). Offen ist Schritt 6.\n', 'UE § 8 Stand')
u = zeile(u, '6. **Nach der Übertragung durch den Verfasser:**',
          '6. **Nach der Übertragung durch den Verfasser (offen):** Der Verfasser löscht die Überschriften 2, 2.1 bis 2.5 (mit 2.4.1 bis 2.4.3) und 3 samt Text und setzt die Einleitung unter „1 Einleitung“, Verzeichnisse mit F9. Dann Teil 0 Rev. 114 und 115 lesen, Master stagen (Größe, MD5, `comments.xml`), Abgleich Satz für Satz gegen den Textvorschlag Einleitung § 1, Messskript `Manuskriptstand_2026-09-25.py` Fassung 3 ohne Anpassung laufen lassen (Probe mit dem Wortlaut des Textvorschlags bestanden, `03_Skripte\\Steuerdokumente_Pruefung_2026-09-28.txt`), `Endabgleich_Manuskript_2026-09-25.py`, neue Rev. in Teil 0 (Rev. 113 bis 115 sind vergeben), Maßnahmenliste im Stand nach Rev. 115 (G35, G34, G33, G32 a und e, G31 c, G26e, G13g, G18c, G19c, J2, K19, H10), Plan Rev. 5 (§ 1a und Task 7 neu), T1 und T4 nach Textvorschlag § 6 Nr. 5 und 6, Projektkopien. Dazu die Spielklasse der drei Mannschaften gegen das Einschlusskriterium von Oliver et al. (2024) prüfen (F17 § 2, Zeile Leistungsniveau, G35 i). Rückschreibung je Commit aus einem eigenen Ausgabepfad, danach neu stagen und per MD5 vergleichen (Rev. 112 und 114).',
          'UE § 8 Nr. 6')
u = zeile(u, '7. **Nicht in diesem Task:**',
          '7. **Erledigt mit Rev. 115 (Task Steuerdokumente 28.09.):** Projektanweisungen Fassung 17, Gliederung v5 (`01_Verfahren\\Gliederung_2026-09-28`), Berichtsraster Rev. 3 mit Kopfblock Einleitung, Plan Rev. 5, Messskript Fassung 3 und Seitenmodell (G35 f, G36). Die Umnummerierung folgt in Task 18.',
          'UE § 8 Nr. 7')
open(os.path.join(ZIEL, '04_Uebergaben', 'Uebergabe_Einleitung_2026-09-28.md'), 'w', encoding='utf-8', newline='\n').write(u)

# ------------------------------------------------------------------ (2) README
p = os.path.join(QUELLE, 'README_Ordnerstruktur.md')
t = open(p, encoding='utf-8').read()
t = ersetze(t, '**Verbindlich seit 09.09.2026 (Projektanweisungen § 1.4, Fassung 16 vom 25.09.2026). Stand dieser Datei: 25.09.2026, spät (Rev. 105, nach Abschluss der Textrevision 4.1 bis 4.6).**',
            '**Verbindlich seit 09.09.2026 (Projektanweisungen § 1.4, Fassung 17 vom 28.09.2026). Stand dieser Datei: 28.09.2026 (Rev. 115, Task Steuerdokumente).**',
            'README Kopf')
t = ersetze(t, '`Projektanweisungen_Fassung16.md` (Sicherung der Fassung für die Projekteinstellungen) | **Genau drei Dateien.** Fassung 14 und die nicht eingesetzte Fassung 15 gehen nach dem Einsetzen von Fassung 16 per Skript in den Papierkorb, Kopien in `_Archiv\\_ersetzt_2026-09-25_Fassung14` und `_ersetzt_2026-09-25_Fassung15` |',
            '`Projektanweisungen_Fassung17.md` (Sicherung der Fassung für die Projekteinstellungen) | **Genau drei Dateien.** Fassung 16 geht nach dem Einsetzen von Fassung 17 per Skript in den Papierkorb, Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`. %s |' % (
                'Fassung 16 steht seit Rev. 115 in der Papierkorbliste, das Aufräumskript läuft erst, wenn Fassung 17 in den Projekteinstellungen steht (A8)'
                if MIT_F16 else 'Folge nach A8: Fassung 17 einsetzen, dann Fassung 16 per Skript archivieren und in die Papierkorbliste aufnehmen, dann das Aufräumskript laufen lassen. Bis dahin liegen dort vier Dateien'),
            'README 00_Steuerung')
t = ersetze(t, '`00_Steuerung` enthält danach genau drei Dateien.',
            '`00_Steuerung` enthält danach genau drei Dateien, %s.' % ('Fassung 16 steht in der Liste (A8)' if MIT_F16 else 'sobald Fassung 16 nach dem Einsetzen von Fassung 17 in der Liste steht (A8), vorher vier'),
            'README Schritt 6')
t = ersetze(t, '`Gliederung_2026-09-23` (v4, Rev. 2)',
            '`Gliederung_2026-09-28` (v5: fünf Kapitel, Einleitung ohne Unterabschnitte, Budget und Seitenmodell) · `Literaturraster_Kapitel2_2026-09-27.md` (Raster der Vorarbeit Zielgrößen)',
            'README 01_Verfahren')
t = ersetze(t, '`Berichtsraster_2026-09-23` (Rev. 2) ·',
            '`Berichtsraster_2026-09-23` (Rev. 3, Kopfblock Einleitung) · `Argumentation_Relevanz_Breitensport_2026-09-28` (Rev. 2, Relevanz und Prävention) · `Vorarbeit_2.4_Zielgroessen_2026-09-27` mit `Literaturraster_2.4_2026-09-27.csv` ·',
            'README 02_Befunde')
t = ersetze(t, '`Manuskriptstand_2026-09-25` (Messung des Masters je Abschnitt) · `Projektanweisungen_Fassung15_2026-09-25.py` mit `Projektanweisungen_Vergleich_2026-09-25`',
            '`Manuskriptstand_2026-09-25` (Messung des Masters je Abschnitt, Fassung 3 mit Seitenschätzung) · `Seitenmodell_2026-09-28` (Seitenzahl als Modellrechnung) · `Projektanweisungen_Fassung17_2026-09-28.py` mit `Projektanweisungen_Vergleich_F16_F17_2026-09-28` · Erzeuger und Prüfung der übrigen Steuerdokumente (`Gliederung_v5_*`, `Berichtsraster_Rev3_*`, `Plan_Rev5_*`, `Steuerdokumente_*`)',
            'README 03_Skripte')
t = ersetze(t, '**`Plan_Weitere_Schritte_2026-09-25.md` (Rev. 4, Reihenfolge der Arbeit, Tasks 1 bis 5 erledigt)** · **Textvorschläge 4.3, 4.4, 4.5 und 4.1_4.6 vom 25.09.** (Maßstab des Abgleichs, Vormerkungen für die Tasks 7 bis 18) · `Textvorschlag_4.7_2026-09-25.md` (Eingang Task 6) · erledigte Eingänge der Textrevision (Übergaben 4.3, 4.4, 4.5.1, 4.6, Textvorschlag 4.5.1 vom 23.09., `Uebergabe_Textrevision_2026-09-12.md`, `Uebergabe_Steuerdokumente_2026-09-25.md`, Archiv mit Task 18)',
            '**`Plan_Weitere_Schritte_2026-09-25.md` (Rev. 5, Reihenfolge der Arbeit, Tasks 1 bis 6 und 1b erledigt)** · **`Textvorschlag_Einleitung_2026-09-28.md`** (Task 7 neu, Übertragung und Abgleich offen) mit dem Eingang `Uebergabe_Einleitung_2026-09-28.md` (offen § 8 Nr. 6) und dem Material `Textvorschlag_2.4_2026-09-28_Fassung6.md` · **Textvorschläge 4.3, 4.4, 4.5 und 4.1_4.6 vom 25.09. und 4.7 vom 26.09.** (Maßstab des Abgleichs, Vormerkungen für die Tasks 7 neu bis 18) · erledigte Eingänge der Textrevision Kapitel 4 (Übergaben 4.3, 4.4, 4.5.1, 4.6, Textvorschlag 4.5.1 vom 23.09., Archiv mit Task 18)',
            'README 04_Uebergaben')
t = ersetze(t, 'Kandidaten aus der Evidenztabelle, mit `README_Abbildungen.md` | Grafiken kommen erst am Ende in den Master, bis dahin Platzhalter |',
            'Kandidaten aus der Evidenztabelle, mit `README_Abbildungen.md` | Grafiken kommen erst in Task 18 in den Master, bis dahin stehen Platzhalter nur für die Anhangsobjekte in Anhang H |',
            'README 06_Abbildungen')
t = ersetze(t, '(Nachtrag 2, Nachtrag 3, Kennzahlen 22.09., Übergaben 25.09., Fassung 14)',
            '(Nachtrag 2, Nachtrag 3, Kennzahlen 22.09., Übergaben 25.09. und 28.09., Fassung 14 und 15, Relevanz Rev. 1, Steuerdokumente 28.09.)',
            'README _Archiv')
a0 = t.index('## Was wo gilt')
a1 = t.index('## Schritt für Schritt')
if t.count('## Was wo gilt') != 1 or t.count('## Schritt für Schritt') != 1:
    raise SystemExit('ABBRUCH: README Abschnitt „Was wo gilt“ nicht eindeutig')
neu_wwg = """## Was wo gilt (Stand 28.09.2026, Rev. 115)

Fünf Dokumente steuern das Schreiben. Jedes beantwortet eine Frage und ändert sich in seinem eigenen Rhythmus (Berichtsraster § 6: nicht zusammenführen).

| Dokument | Frage | Ändert sich, wenn … |
|---|---|---|
| `02_Befunde\\Berichtsraster_2026-09-23` (Rev. 3, Kopfblock Einleitung in § 3.1) | Was muss in den Abschnitt, was nicht? | eine Norm neu geprüft oder ein Abschnitt fertig wird |
| `02_Befunde\\Bauplan_Vergleichskorpus_2026-09-15` | In welcher Reihenfolge, mit welchen Zügen? | nie (gemessen an elf publizierten Studien), nur Errata |
| `02_Befunde\\Auswertungsplan_2026-09-12` § 5 mit Register § 5.10 · `Spezifikation_2026-09-24` · `Kennzahlen_2026-09-25.md` | Was wird wie gerechnet, wo weicht es vom Antrag ab, welche Zahl aus welcher Bezugsmenge? | ein Nachtrag zur Spezifikation entsteht oder der Datenstand neu läuft. Das Kennzahlenblatt entsteht nur per Skript |
| `01_Verfahren\\Stilprofil_2026-09-13.md` | Wie klingt der Satz? | der Verfasser eine Stilfestlegung trifft |
| `04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 5) | Was kommt als Nächstes, mit welchem Budget? | ein Task abgeschlossen ist oder der Verfasser die Reihenfolge ändert |

Gliederung, Wortbudget und Seitenmodell stehen in `01_Verfahren\\Gliederung_2026-09-28` (v5). Eingang von Task 7 neu (Einleitung) sind `04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md` und `02_Befunde\\Argumentation_Relevanz_Breitensport_2026-09-28` (Rev. 2). Der Textvorschlag Einleitung ist der Maßstab des Abgleichs nach der Übertragung. Darüber stehen die Projektanweisungen (Fassung 17, Sicherung in `00_Steuerung`, einzusetzen nach A8) und der Arbeitsstand in `00_Steuerung\\Cowork_Sitzungsnotizen.md`, Teil 0. Teil 0 ist die einzige Wahrheitsquelle für den Stand, das Projektdokument ist eine Kopie.

**Stand in Kürze:** Die Auswertung ist abgeschlossen (Phasen 0 bis 7, F2 und F3 am 25.09.). Zahlen kommen allein aus dem Kennzahlenblatt 25.09. (Rev. 2), im Manuskript steht keine Kennung. Kapitel 4 ist textlich fertig (4.1 bis 4.7 mit %(k4)s gegen 2.550 Wörter, Task 6). Kapitel 1 bis 3 werden eine Einleitung ohne Unterabschnitte mit höchstens 1.500 Wörtern. Der Textvorschlag liegt mit %(tvw)s Wörtern vor, die Übertragung durch den Verfasser steht aus (Task 7 neu). Die Arbeit hat damit fünf Kapitel und höchstens 6.350 Wörter Absatztext. Die Seitengrenze des Verfassers lautet höchstens %(grenze)d Seiten von der Einleitung bis zum Ende des Literaturverzeichnisses (Seitenmodell %(sgb)s Seiten, Modellrechnung). Danach folgen Ergebnisse, Diskussion und Fazit (Tasks 11 bis 13), Anhänge zuletzt (Plan Rev. 5). Grafiken und Tabellen kommen erst in Task 18 in den Master.

**Überholte Teile anderer Dokumente** (Vermerk nur hier und in Projektanweisungen § 1.3, nicht in den Dokumenten selbst): `CONSORT_Auswertung_und_Umsetzung_2026-09-09` § 4 (Vorschlagsliste) und Fallzahlangaben · Ist-Spalten von `Manuskriptstand_und_Vollstaendigkeit_2026-09-13` (ersetzt durch `03_Skripte\\Manuskriptstand_2026-09-25`) · Bauplan § 1, Zählung der Schlusskapitel: gemeint sind vier Studien ohne Fazitkapitel, nicht „vier weder noch“ · `Argumentation_Relevanz_Breitensport_2026-09-28` § 6 Nr. 6 und § 7 nennen eine Übergabe zu 2.4 Fassung 7, die nie abgelegt wurde · Analyseprotokoll 15.09. und Python-Kette B0 bis B9 nur als Arbeitsstand vor dem Abgleich, keine Zahlenquelle · Nachtragsvermerke für Auswertungsverfahren, Umfangsdokument, Auswertungsplan, Kennzahlenblatt und Bauplan (Projektanweisungen § 1.3).

""" % dict(k4=de(K4), tvw=TVW, grenze=GRENZE, sgb=S_GB)
t = t[:a0] + neu_wwg + t[a1:]
PROTOKOLL.append('README Was wo gilt')
alt_pk = 'Was im Papierkorb landet, steht als feste Liste im Skript: Projektanweisungen Fassung 10 bis 12 · erledigte Übergaben und Textvorschläge (Datensicherung und Blindrechnung vom 24.09., 4.1 vom 22.09., Textvorschläge 4.1 und 4.2, Sofortblock, Kopien in `_Archiv\\_ersetzt_2026-09-25_Uebergaben`) · Fassung 14 der Projektanweisungen, sobald Fassung 15 in den Projekteinstellungen steht (Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14`) ·'
neu_pk = 'Was im Papierkorb landet, steht als feste Liste im Skript: Projektanweisungen Fassung 10 bis 12, 14 und 15 · erledigte Übergaben und Textvorschläge (Datensicherung und Blindrechnung vom 24.09., 4.1 vom 22.09., Textvorschläge 4.1 und 4.2, Sofortblock, Kopien in `_Archiv\\_ersetzt_2026-09-25_Uebergaben`) · Gliederung v4 (Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`) · die Übergaben und Textvorschläge zu Kapitel 2 und 2.4 vom 26. bis 28.09., die Übergaben Steuerdokumente vom 25.09. und 28.09., der Textvorschlag 4.7 vom 25.09. und die Übergabe Textrevision vom 12.09. (Kopien in `_Archiv\\_ersetzt_2026-09-28_Uebergaben`) ·'
if MIT_F16:
    neu_pk += ' Fassung 16 der Projektanweisungen, sobald Fassung 17 in den Projekteinstellungen steht (Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`) ·'
t = ersetze(t, alt_pk, neu_pk, 'README Papierkorbliste')
open(os.path.join(ZIEL, 'README_Ordnerstruktur.md'), 'w', encoding='utf-8', newline='\n').write(t)

# ------------------------------------------------------------------ (3) Aufräumskript (BOM, CRLF)
p = os.path.join(QUELLE, 'Ordner_aufraeumen.ps1')
roh = open(p, 'rb').read()
if not (roh.startswith(b'\xef\xbb\xbf') and b'\r\n' in roh):
    raise SystemExit('ABBRUCH: Aufräumskript ohne BOM oder ohne CRLF')
s = roh[3:].decode('utf-8').replace('\r\n', '\n')
s = ersetze(s, '#  Stand 25.09.2026 (spaet, Rev. 105: Fassung 15 der Projektanweisungen ergaenzt). Ersetzt die Fassung vom 25.09.2026 (abends).',
            '#  Stand 28.09.2026 (Rev. 115, Task Steuerdokumente: Gliederung v4 und erledigte Uebergaben ergaenzt%s). Ersetzt die Fassung vom 25.09.2026 (spaet).'
            % (', Fassung 16 der Projektanweisungen' if MIT_F16 else ''),
            'ps1 Kopf')
s = ersetze(s, '#  Grundlage: Projektanweisungen Fassung 14 § 1.3 "Veraltet, nicht verwenden", Sitzungsnotizen Rev. 92,',
            '#  Grundlage: Projektanweisungen Fassung 17 § 1.3 "Veraltet, nicht verwenden", Sitzungsnotizen Rev. 92 und 115,',
            'ps1 Grundlage')
s = ersetze(s, "  # Steuerung: Fassung 14 steht in den Projekteinstellungen, Vorgaengerfassungen entfallen\n",
            "  # Steuerung: Vorgaengerfassungen der Projektanweisungen entfallen, wirksam ist die Fassung in den Projekteinstellungen\n",
            'ps1 Steuerung Kommentar')
if MIT_F16:
    f15 = "  'Claude\\00_Steuerung\\Projektanweisungen_Fassung15.md',\n"
    s = ersetze(s, f15, f15 + "  # Fassung 16: erst laufen lassen, wenn Fassung 17 in den Projekteinstellungen steht (A8). Kopie in Claude\\_Archiv\\_ersetzt_2026-09-28_Steuerdokumente\n  'Claude\\00_Steuerung\\Projektanweisungen_Fassung16.md',\n",
                'ps1 Fassung 16')
sofort = "  'Claude\\04_Uebergaben\\Befunde_Sofortblock_2026-09-13.md',\n"
neu_ueb = sofort + """  # Task Steuerdokumente 28.09.: erledigt oder ersetzt, Kopien in Claude\\_Archiv\\_ersetzt_2026-09-28_Uebergaben
  'Claude\\04_Uebergaben\\Uebergabe_Kapitel2_2026-09-26.md',
  'Claude\\04_Uebergaben\\Uebergabe_2.4_Fassung6_2026-09-28.md',
  'Claude\\04_Uebergaben\\Textvorschlag_2.4_2026-09-26.md',
  'Claude\\04_Uebergaben\\Textvorschlag_2.4_2026-09-27.md',
  'Claude\\04_Uebergaben\\Textvorschlag_2.4_2026-09-27_Fassung5.md',
  'Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md',
  'Claude\\04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md',
  'Claude\\04_Uebergaben\\Uebergabe_Textrevision_2026-09-12.md',
  'Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md',
  # Gliederung v4: ersetzt durch v5 (Gliederung_2026-09-28), Kopien in Claude\\_Archiv\\_ersetzt_2026-09-28_Steuerdokumente
  'Claude\\01_Verfahren\\Gliederung_2026-09-23.md',
  'Claude\\01_Verfahren\\Gliederung_2026-09-23.docx',
  'Claude\\01_Verfahren\\Gliederung_2026-09-23.pdf',
"""
s = ersetze(s, sofort, neu_ueb, 'ps1 Uebergaben und Gliederung v4')
s = ersetze(s, "muster = @('Cowork_Sitzungsnotizen.md','Massnahmenliste_Datenverarbeitung.md','Projektanweisungen_Fassung15.md')",
            "muster = @('Cowork_Sitzungsnotizen.md','Massnahmenliste_Datenverarbeitung.md','Projektanweisungen_Fassung17.md')",
            'ps1 Muster 00_Steuerung')
open(os.path.join(ZIEL, 'Ordner_aufraeumen.ps1'), 'wb').write(b'\xef\xbb\xbf' + s.replace('\n', '\r\n').encode('utf-8'))

# ------------------------------------------------------------------ (4) Archivkopien
kopien = [('_ersetzt_2026-09-28_Steuerdokumente', q) for q in [
    '01_Verfahren/Gliederung_2026-09-23.md', '01_Verfahren/Gliederung_2026-09-23.docx', '01_Verfahren/Gliederung_2026-09-23.pdf',
    '02_Befunde/Berichtsraster_2026-09-23.md', '02_Befunde/Berichtsraster_2026-09-23.docx', '02_Befunde/Berichtsraster_2026-09-23.pdf',
    '04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md',
    '03_Skripte/Manuskriptstand_2026-09-25.py', '03_Skripte/Manuskriptstand_2026-09-25.txt', '03_Skripte/Manuskriptstand_2026-09-25.csv']]
kopien += [('_ersetzt_2026-09-28_Uebergaben', '04_Uebergaben/' + n) for n in [
    'Uebergabe_Kapitel2_2026-09-26.md', 'Uebergabe_2.4_Fassung6_2026-09-28.md', 'Textvorschlag_2.4_2026-09-26.md',
    'Textvorschlag_2.4_2026-09-27.md', 'Textvorschlag_2.4_2026-09-27_Fassung5.md', 'Uebergabe_Steuerdokumente_2026-09-25.md',
    'Textvorschlag_4.7_2026-09-25.md', 'Uebergabe_Textrevision_2026-09-12.md', 'Uebergabe_Steuerdokumente_2026-09-28.md']]
# Vorstände der in diesem Task geänderten Dateien (Übergabe Steuerdokumente § 0: „der Vorstand geht als Kopie ins Archiv“)
kopien += [('_ersetzt_2026-09-28_Steuerdokumente', 'README_Ordnerstruktur.md'), ('_ersetzt_2026-09-28_Steuerdokumente', 'Ordner_aufraeumen.ps1'),
           ('_ersetzt_2026-09-28_Uebergaben', '04_Uebergaben/Uebergabe_Einleitung_2026-09-28.md')]
if MIT_F16:
    kopien.append(('_ersetzt_2026-09-28_Steuerdokumente', '00_Steuerung/Projektanweisungen_Fassung16.md'))
# Vorstand prüfen: Die Kopien müssen die Originale vor diesem Task sein (Kopfzeilen der Vorstände)
pruef = {'02_Befunde/Berichtsraster_2026-09-23.md': 'Rev. 2', '04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md': 'Rev. 4',
         '03_Skripte/Manuskriptstand_2026-09-25.py': 'Fassung 2', '01_Verfahren/Gliederung_2026-09-23.md': 'v4',
         'README_Ordnerstruktur.md': 'Fassung 16 vom 25.09.2026', 'Ordner_aufraeumen.ps1': 'Stand 25.09.2026 (spaet, Rev. 105',
         '04_Uebergaben/Uebergabe_Einleitung_2026-09-28.md': 'Nachgezogen mit Rev. 113'}
for rel, merkmal in pruef.items():
    kopf = open(os.path.join(QUELLE, rel), encoding='utf-8').read()[:3000]
    if merkmal not in kopf:
        raise SystemExit('ABBRUCH: %s trägt im Kopf nicht „%s“, Vorstand unklar' % (rel, merkmal))
zeilen = []
for ordner, rel in kopien:
    z = os.path.join(ZIEL, '_Archiv', ordner)
    os.makedirs(z, exist_ok=True)
    ziel = os.path.join(z, os.path.basename(rel))
    shutil.copy2(os.path.join(QUELLE, rel), ziel)
    zeilen.append('Archivkopie _Archiv\\%s\\%s  %d Byte  MD5 %s' % (ordner, os.path.basename(rel), os.path.getsize(ziel),
                                                                 hashlib.md5(open(ziel, 'rb').read()).hexdigest()))

print('Werte: Textteil %s, Einleitung bis Literaturverzeichnis %s (obere Variante %s), Messskript %s, Schwelle %d, Grenze %d, Kapitel 4 %s, Textvorschlag Einleitung %s'
      % (S_TT, S_GB, S_GO, MP, SCHWELLE, GRENZE, de(K4), TVW))
print('Ersetzungen (%d), je genau einmal: ' % len(PROTOKOLL) + ' · '.join(PROTOKOLL))
print('\n'.join(zeilen))
print('Fassung 16 einbezogen: ' + ('ja' if MIT_F16 else 'nein'))

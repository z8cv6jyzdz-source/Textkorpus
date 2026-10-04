# -*- coding: utf-8 -*-
"""
Steuerung_Rev151_Nachtrag_2026-10-02.py — Berichtigung im Teil-0-Eintrag Rev. 151 (Task „Boumparis“)
Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext.

Anlass: Der Eintrag Rev. 151 (18:17 Sitzungsuhr, Steuerung_Rev151_2026-10-02.py) rechnete den Projektspeicher in Byte
(„rund 1,9 Mio.“). project_info zählt Token. Beim Ersetzen der Projektkopie der Notizen lehnte das Projekt die
Kopie zunächst ab (rund 205.000 Token, Höchstgröße 2.000.000), sie wurde in zwei Schritten ersetzt. Der Nachtrag
berichtigt Punkt (3) unter „Offen beim Verfasser“, ergänzt die eigenen Korrekturen und den Stand der Dateien.

Aufruf: python Steuerung_Rev151_Nachtrag_2026-10-02.py <Sitzungsnotizen.md> <Ausgabeordner> <HH:MM> <Projektspeicher>
Jede Ersetzung muss genau einmal greifen, sonst Abbruch. Ohne Semikolon im Skript (chr(59)).
"""
import sys, os, hashlib

SEMI = chr(59)
NOTIZEN, AUS, UHR, SPEICHER = sys.argv[1:5]


def md5(b):
    return hashlib.md5(b).hexdigest()


def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit('Abbruch: %s greift %d-mal statt einmal' % (name, n))
    protokoll.append('  %s: 1 Ersetzung' % name)
    return text.replace(alt, neu)


prot = []
nb = open(NOTIZEN, 'rb').read()
prot.append('Eingang Notizen: %d Byte, MD5 %s' % (len(nb), md5(nb)))
n = nb.decode('utf-8')

alt3 = ('(3) Projektspeicher: vor den Kopien dieses Tasks 1.806.923 von 2.000.000 (project_info), mit ihnen rund 1,9 Mio. '
        '(Rechnung aus den Dateigrößen). Vor weiteren großen Projektkopien prüfen, welche Kopien entbehrlich sind, '
        'die Ordnerfassungen bleiben maßgeblich.')
neu3 = (f'(3) Projektspeicher (project_info, Einheit Token): vor den Kopien dieses Tasks 1.806.923 von 2.000.000, '
        f'nach ihnen {SPEICHER} ({UHR} Sitzungsuhr). Beim Ersetzen einer Kopie rechnet die Prüfung des Projekts offenbar die volle neue Größe '
        'auf den Bestand, ohne die alte Fassung abzuziehen: Die Notizenkopie (rund 205.000 Token) wurde zunächst abgewiesen '
        'und in zwei Schritten ersetzt, erst mit einer kurzen Zwischenfassung (Teil 0 bis Rev. 146), dann vollständig '
        '(MD5 gleich der Ordnerfassung). Solange der freie Platz kleiner ist als die Notizenkopie, braucht jede Aktualisierung '
        'diese zwei Schritte, oder der Verfasser löscht entbehrliche Projektkopien, die Ordnerfassungen bleiben maßgeblich.')
n = ersetze(n, alt3, neu3, 'Notizen Rev. 151 Punkt (3)', prot)

alt4 = '(4) Nach der Klickfreigabe im Nachtrag § 3.1 Nr. 2 ergänzt: Variante A und Satzkern Nr. 4 beginnen gleich, 12b gibt Nr. 4 einen eigenen Anschluss.'
neu4 = (alt4 + f' (5) Die Fassung dieses Eintrags von 18:17 rechnete den Projektspeicher in Byte („rund 1,9 Mio.“), '
        f'project_info zählt Token, Punkt (3) unter „Offen beim Verfasser“ um {UHR} berichtigt.')
n = ersetze(n, alt4, neu4, 'Notizen Rev. 151 Korrektur (5)', prot)

alt5 = '`03_Skripte\\Steuerung_Rev151_2026-10-02.py` mit `.txt`. Geändert: `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (76 Steckbriefe)'
neu5 = ('`03_Skripte\\Steuerung_Rev151_2026-10-02.py` mit `.txt` · `03_Skripte\\Steuerung_Rev151_Nachtrag_2026-10-02.py` mit `.txt` '
        f'(Berichtigung von Punkt (3), {UHR}). Geändert: `Schreiben\\ev3_daten\\T1_steckbriefe.csv` (76 Steckbriefe)')
n = ersetze(n, alt5, neu5, 'Notizen Rev. 151 Stand der Dateien', prot)

for name, teil in (('Punkt (3)', neu3), ('Korrektur (5)', neu4), ('Stand der Dateien', neu5)):
    if teil.count(SEMI):
        raise SystemExit('Abbruch: Semikolon in ' + name)

os.makedirs(AUS, exist_ok=True)
nb2 = n.encode('utf-8')
open(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'), 'wb').write(nb2)
prot.append('Ausgang Notizen: %d Byte, MD5 %s' % (len(nb2), md5(nb2)))
a, b = nb.decode('utf-8').split('\n'), nb2.decode('utf-8').split('\n')
geaendert = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
assert len(a) == len(b), 'Zeilenzahl geändert'
prot.append('Rücklesen: %d Zeilen, geändert %d (Zeile %s, erwartet: nur der Eintrag Rev. 151)' % (
    len(b), len(geaendert), ', '.join(str(i + 1) for i in geaendert)))
prot.append('Semikola in den neuen Teilen: 0')
text = '\n'.join(prot) + '\n'
open(os.path.join(AUS, 'Steuerung_Rev151_Nachtrag_2026-10-02.txt'), 'w', encoding='utf-8').write(text)
print(text)

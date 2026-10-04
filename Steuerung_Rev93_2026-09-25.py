# -*- coding: utf-8 -*-
"""
Steuerung_Rev93_2026-09-25.py — Sitzungsnotizen Teil 0 (Rev. 93) und Maßnahmenliste fortschreiben
Bachelorarbeit U15-Plyometrie · DSHS Köln

Zweck: Den Lauf von Ordner_aufraeumen.ps1 (Fassung 25.09.) durch den Verfasser und das Leeren des
Papierkorbs in den beiden Steuerdokumenten festhalten und die davon abhängigen Maßnahmen G21, G26h und L21
abhaken. Die Zahlen stammen aus dem Protokoll des Skriptlaufs (_Archiv\\Aufraeumprotokoll_2026-09-25.txt),
das dieses Skript liest. Jede Textstelle wird genau einmal ersetzt, sonst bricht das Skript ab. Ohne Semikolon.
Aufruf: python Steuerung_Rev93_2026-09-25.py <Cowork_Sitzungsnotizen.md> <Massnahmenliste_Datenverarbeitung.md> <Aufraeumprotokoll.txt>
Fassung: 2026-09-25, erste Fassung.
"""
import sys
import re

SN, ML, PROT = sys.argv[1], sys.argv[2], sys.argv[3]
prot = open(PROT, encoding='utf-8-sig').read()
m_n = re.search(r'Verschoben: (\d+) Eintraege', prot)
if not m_n:
    raise SystemExit('Protokoll ohne Zeile „Verschoben“')
N_VERSCHOBEN = int(m_n.group(1))
N_FEHLER = prot.count('FEHLER bei')
N_UNSORTIERT = prot.count('UNSORTIERT:')
N_UEBERSPRUNGEN = prot.count('Ziel belegt, uebersprungen')
steuerung = [z.strip() for z in prot.split('Inhalt 00_Steuerung (Soll: genau drei Dateien):')[1].strip().split('\n') if z.strip()]
if len(steuerung) != 3:
    raise SystemExit('00_Steuerung enthält nicht genau drei Dateien: %r' % steuerung)


def ersetze(text, alt, neu):
    if text.count(alt) != 1:
        raise SystemExit('Textstelle nicht genau einmal gefunden: ' + alt[:80])
    return text.replace(alt, neu)


# ---------------------------------------------------------------- Sitzungsnotizen
s = open(SN, encoding='utf-8').read()
s = ersetze(s, '**Stand: (Rev. 92 — siehe Block oben.) Zuvor: (Rev. 91 — siehe Block oben.)',
            '**Stand: (Rev. 93 — siehe Block oben.) Zuvor: (Rev. 92 — siehe Block oben.) Zuvor: (Rev. 91 — siehe Block oben.)')
REV93 = '''### ⭐ NACHTRAG (Rev. 93, 25.09.2026, 17:05 MESZ): Papierkorb-Skript gelaufen, Papierkorb geleert, Projektspeicher bereinigt — G21, G26h und L21 erledigt

**Lauf des Verfassers (25.09., vor 17:00 MESZ):** `Claude\\Ordner_aufraeumen.ps1` (Fassung 25.09.) ist echt gelaufen. Protokoll `_Archiv\\Aufraeumprotokoll_2026-09-25.txt`: verschoben %d Einträge, %d Fehler, %d übersprungen, %d unsortiert, `00_Steuerung` mit genau drei Dateien (%s). Der Verfasser hat den Papierkorb anschließend geleert (Ordner `Bachelorarbeit\\Papierkorb` leer, geprüft 25.09. 17:00 MESZ). Damit sind aus dem Ordner entfernt: F10 bis F12, die Kennzahlenblätter 15.09. und 22.09. mit Erzeugern, Berichtsraster 13.09., Analyseprotokoll 12.09., SPSS-Vorgehen und SPSS-Syntax, drei Hilfsskripte, fünf Übergaben, die Transferprobe, die Ordner `Claude outputs`, `Statistik\\Claude outputs`, `Statistik\\Fragebogen Auswertung`, `Auswertung` und `Dashboard` (mit `daten\\`), die Doppelablagen in `Statistik\\`, `Schreiben\\` und im Hauptordner, `Daten\\Datenerfassung_Praetest_U15_1.xlsx`, das alte Prä-Daten-Dashboard und zwei Installationsdateien. Was bleibt und weiter gilt, steht in `README_Ordnerstruktur.md` (Stand 25.09. nachmittags). Der Ordner `Claude` enthält im Hauptordner nur noch `README_Ordnerstruktur.md` und `Ordner_aufraeumen.ps1`.

**Projektspeicher:** 26 überholte Projektdokumente auf Freigabe des Verfassers gelöscht (Liste im Rev.-92-Block), alle Projektkopien unter `claude/` auf dem Stand des Ordners, einschließlich der Sitzungsnotizen.

**Maßnahmenliste:** G21 erledigt (Kennzahlenblätter 15.09. und 22.09. gelöscht), G26h erledigt (Archiv und Aufräumen, der DLRG-Nachweis in `Ideen und Studien` bleibt beim Verfasser und ist kein Projektdokument), L21 erledigt (Altbestand der Darstellung: ancova-CSV gerettet, Rest gelöscht). Die Regel „Cowork kann nicht löschen, Verschieben und Löschen nur über das Skript und den Verfasser“ gilt weiter.

**Nächste Schritte:** unverändert wie im Rev.-92-Block, beginnend mit (2) Handprobe prüfen und (3) Vorschlagsliste 1 bis 7 übertragen, dann Freigabe F3.

''' % (N_VERSCHOBEN, N_FEHLER, N_UEBERSPRUNGEN, N_UNSORTIERT, ', '.join(steuerung))
if chr(59) in REV93:
    raise SystemExit('Semikolon im Rev.-93-Block')
s = ersetze(s, '### ⭐ NEU (Rev. 92, 25.09.2026, 16:35 MESZ): Verfasserentscheidungen nach Phase 7',
            REV93 + '### ⭐ NEU (Rev. 92, 25.09.2026, 16:35 MESZ): Verfasserentscheidungen nach Phase 7')
with open(SN, 'w', encoding='utf-8', newline='\n') as f:
    f.write(s)

# ---------------------------------------------------------------- Maßnahmenliste
m = open(ML, encoding='utf-8').read()
m = ersetze(m, '**Stand 25.09.2026, 16:35 MESZ (Rev. 92 — Verfasserentscheidungen nach Phase 7:',
            '**Stand 25.09.2026, 17:05 MESZ (Rev. 93 — Papierkorb-Skript vom Verfasser gelaufen (%d Einträge verschoben, %d Fehler), Papierkorb geleert, 26 überholte Projektdokumente gelöscht, Projektkopien auf Ordnerstand. G21, G26h und L21 erledigt). Zuvor 25.09.2026, 16:35 MESZ (Rev. 92 — Verfasserentscheidungen nach Phase 7:' % (N_VERSCHOBEN, N_FEHLER))
# G21
m = ersetze(m, '  - [ ] **G21 · Überholtes Kennzahlenblatt archivieren (22.09., 16:45):**',
            '  - [x] **G21 · Überholtes Kennzahlenblatt archivieren (22.09., 16:45):** **Erledigt 25.09. (Rev. 93): per `Ordner_aufraeumen.ps1` in den Papierkorb verschoben und vom Verfasser gelöscht, Kopien der Erzeuger in `_Archiv\\_ersetzt_2026-09-25_Kennzahlen`.** Vorher:')
# G26h
m = ersetze(m, '    - [ ] **G26h · Archiv und Aufräumen (Ordner_aufraeumen.ps1' + chr(59) + ' Cowork kann nicht löschen):**',
            '    - [x] **G26h · Archiv und Aufräumen (Ordner_aufraeumen.ps1' + chr(59) + ' Cowork kann nicht löschen):** **Erledigt 25.09. (Rev. 93): Skriptlauf des Verfassers, %d Einträge in den Papierkorb, Papierkorb geleert. Der DLRG-Nachweis bleibt beim Verfasser (kein Projektdokument, nicht verschoben).** Vorher:' % N_VERSCHOBEN)
# L21
m = ersetze(m, '- [ ] **L21 · Altbestand der Darstellung ordnen:**',
            '- [x] **L21 · Altbestand der Darstellung ordnen:** **Erledigt 25.09. (Rev. 93): `ancova_ergebnisse.csv` gerettet nach `03_Skripte`, `Auswertung\\`, `Dashboard\\` (mit `daten\\`), `Claude outputs\\` und `Schreiben\\Auswertungs-und-Darstellungskonzept.docx` per Skript in den Papierkorb und vom Verfasser gelöscht.** Vorher:')
# Tabelle L und Summe
m = ersetze(m, 'Rev. 92: L12 entschieden (R14), L19 Rest erledigt, L21 auf den Papierkorb umgestellt, Zählung nicht neu erhoben)',
            'Rev. 92: L12 entschieden (R14), L19 Rest erledigt, L21 auf den Papierkorb umgestellt, Rev. 93: L21 erledigt, Zählung nicht neu erhoben)')
m = ersetze(m, '| **Summe** | **57 offen** (Stand 25.09., Rev. 92:',
            '| **Summe** | **57 offen** (Stand 25.09., Rev. 93: G21, G26h und L21 erledigt — Zählung nicht neu erhoben. Stand 25.09., Rev. 92:')
with open(ML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(m)
print('Sitzungsnotizen Rev. 93 und Maßnahmenliste fortgeschrieben: verschoben %d, Fehler %d, unsortiert %d' % (N_VERSCHOBEN, N_FEHLER, N_UNSORTIERT))

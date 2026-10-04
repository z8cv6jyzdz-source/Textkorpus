# -*- coding: utf-8 -*-
"""
Steuerung_Rev148_2026-10-02.py — Fortschreibung von Teil 0 (Rev. 148), Maßnahmenliste und Plan
Bachelorarbeit U15-Plyometrie · Arbeitsdokument, kein Manuskripttext.

Anlass: Auftrag des Verfassers 02.10., 15:28 Sitzungsuhr (Boumparis et al. im Ordner, neuer Task zur Analyse
und Einarbeitung in die Argumentationskette). Ergebnis: Prompt 04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md.

Aufruf: python Steuerung_Rev148_2026-10-02.py <Sitzungsnotizen.md> <Massnahmenliste.md> <Plan.md> <Prompt.md> <Ausgabeordner> <HH:MM>
Jede Ersetzung muss genau einmal greifen, sonst Abbruch. Schreibt die drei Steuerdateien neu in den Ausgabeordner
und ein Protokoll (Größen, MD5, Ersetzungen, Semikola) nach stdout.
"""
import sys, os, hashlib

NOTIZEN, LISTE, PLAN, PROMPT, AUS, UHR = sys.argv[1:7]

def md5(b):
    return hashlib.md5(b).hexdigest()

def ersetze(text, alt, neu, name, protokoll):
    n = text.count(alt)
    if n != 1:
        raise SystemExit(f'Abbruch: {name} greift {n}-mal statt einmal')
    protokoll.append(f'  {name}: 1 Ersetzung')
    return text.replace(alt, neu)

pb = open(PROMPT, 'rb').read()
p_groesse, p_md5 = len(pb), md5(pb)
if pb.decode('utf-8').count(';'):
    raise SystemExit('Abbruch: Semikolon im Prompt')

prot = []
nb, lb, plb = open(NOTIZEN, 'rb').read(), open(LISTE, 'rb').read(), open(PLAN, 'rb').read()
prot.append(f'Eingang Notizen: {len(nb)} Byte, MD5 {md5(nb)}')
prot.append(f'Eingang Maßnahmenliste: {len(lb)} Byte, MD5 {md5(lb)}')
prot.append(f'Eingang Plan: {len(plb)} Byte, MD5 {md5(plb)}')
prot.append(f'Prompt: {p_groesse} Byte, MD5 {p_md5}, Semikola 0')
n, l, pl = nb.decode('utf-8'), lb.decode('utf-8'), plb.decode('utf-8')

PROMPTPFAD = '`04_Uebergaben\\Prompt_Boumparis_Einarbeitung_2026-10-02.md`'

# ---------- Sitzungsnotizen ----------
n = ersetze(n, '**Stand: (Rev. 147 — siehe Block oben.)',
            '**Stand: (Rev. 148 — siehe Block oben.) Zuvor: (Rev. 147 — siehe Block oben.)', 'Notizen Stand', prot)

block = f"""### ⭐ NACHTRAG (Rev. 148, 02.10.2026, {UHR} Sitzungsuhr, Auftrag 15:28): Boumparis et al. im Ordner als Preprint — Prompt für einen eigenen Task „Boumparis“ (Analyse und Einarbeitung in die Argumentationskette, Vergleichssatz K2 zu 6.1), Plan-Nachtrag 02.10.

**Auftrag (Verfasser, 02.10., 15:28, wörtlich):** „Boumparis et al., 2025 liegt jetzt im Ordner. Nutze die Ergebnisse für deine Ausführungen in den gegebenen Abschnitten des Textes. In einem neuen Task soll die Studie analysiert werden und die Erkenntnisse systematisch in den TExt bzw. die Argumentationskette eingearbeitet werden“

**Einordnung:** Folgeauftrag zu Rev. 147 (Befund § 6, H16 Priorität 1). Ergebnis ist der Prompt für einen eigenen Task. Kein Manuskripttext, keine Änderung an Master, Kennzahlenblatt, T1, T4, Textvorschlägen und Befund Rev. 147.

**Befund zur Fassung:** Die Datei `Ideen und Studien\\2025 Boumparis et al., Factors Influencing Adherence to Digital Lifestyle interventions for adolescence.pdf` (1.062.847 Byte, Dateizeit 15:26 Sitzungsuhr, MD5 `32ed3266…`) ist der Preprint aus JMIR Preprints (eingereicht 25.09.2025): Kopfzeile „JMIR Preprints“, Deckblatt mit älterer Zusammenfassung (85 Studien, 32.397 Teilnehmende, Abschlussrate 51,85 %, Bestandteil-Adhärenz 49,35 %), im Manuskript 119 Studien. Die Version of Record (Interact J Med Res 15, e84822, doi 10.2196/84822, PMC13626193, PMID 42814774, erschienen 30.09.2026, zwölf Autorinnen und Autoren, Titel „… Systematic Review and Meta-Analysis of Attrition“) nennt 116 Studien mit 143 Vergleichen. Die in Rev. 147 verwendeten Werte (66,9 %, 55,2 %, Bewegung 62,8 %) stammen aus der Version of Record. Zitierfähig ist nur sie (F17 § 6.1), Zitierjahr 2026, nicht 2025.

**Präzisierungen zu Rev. 147 (am Text der Version of Record, gehen an den neuen Task, Prompt § 1):** (a) 66,9 % und 55,2 % sind ungewichtete beschreibende Mittel über die berichtenden Vergleiche. Metaanalytisch zusammengefasst ist nur der Studienabbruch (gepoolt 16,9 %, 108 Vergleiche, sehr hohe Heterogenität). Befund § 0 Nr. 3 und H16 nennen für die Adhärenzwerte „Metaanalyse“, richtig ist „systematische Übersicht“. (b) Die geringere Adhärenz bei längerer Studiendauer (Befund § 0 Nr. 5) beruht im Bewegungsteil auf zwei Studien, insgesamt nennt die Übersicht die Evidenz zur Dauer uneinheitlich. (c) Die Distanz bei Umsetzungsvergleichen ist uneinheitlich gerechnet: Befund § 2.1 setzt Klusemann et al. (2012) mit P·D·Z 2·0·0 an, Textvorschlag 6.1 § 5 mit 2·2·1. Der Befund Rev. 147 bleibt unverändert, die Präzisierungen stehen hier und im Prompt.

**Im Ordner vorgefunden (Task 12a, parallele Sitzung, nicht Teil dieses Eintrags):** `04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md` (74.185 Byte, Dateizeit 15:31 Sitzungsuhr) mit `03_Skripte\\Textvorschlag_6.1_2026-10-02.py`, `.txt`, `.json` und `tv61_md.py`: Stand nach der Zweitprüfung, vor der Klickfreigabe, 6.1 ohne Modul 695 Wörter, Modul A2-M (Vergleichssatz der Umsetzung, vorläufig Klusemann et al., 2012) offen, weil der Verfasser erneut Literatur sucht (K2), K5 offen. T1 und T4 per `03_Skripte\\T1_T4_Nachtrag_2026-10-02.py` um Klusemann2012, Rogers2020 und Veith2021 ergänzt (75 Steckbriefe, 157 Zitierfallen). Boumparis et al. kommt dort nicht vor. Der Teil-0-Eintrag von Task 12a stand um 15:35 aus, der Textvorschlag plant ihn als „Rev. 147“ (§ 9.4 Nr. 2, § 9.5 Nr. 1). Rev. 147 und Rev. 148 sind vergeben, Task 12a trägt sich mit der nächsten freien Nummer ein.

**Ergebnis:** Prompt {PROMPTPFAD} ({p_groesse} Byte, MD5 `{p_md5[:8]}…`) mit Projektkopie für den Task „Boumparis“ zwischen Textvorschlag und Freigabe von 12a: (1) Stand, Fassung und die Präzisierungen (a) bis (c) prüfen, Klickfrage, falls die Version of Record fehlt, (2) Analysebefund `02_Befunde\\Analyse_Boumparis_2026_<Datum>` mit Steckbrief, Definitionen und Zuordnung der eigenen Maße über K-10.5, K-10.7, K-10.15 und K-01, Ergebnissen mit Fundstelle, Güte, Übertragbarkeit, T1 und T4, (3) Einarbeitungsplan je Glied der Argumentationskette als `04_Uebergaben\\Textvorschlag_6.1_Nachtrag_K2_<Datum>.md`: Vergleichssatz für A2-M in höchstens zwei Varianten im Budget über die Kürzungsleiter oder Verzicht, Satzkerne für 6.2 und 6.3 (G3, G6), Kapitel 7 ohne Quelle, Vormerkung für die Schlussfassung der Einleitung (Absatz 3 und 5), (4) Zweitprüfung, Klickfreigabe des Moduls. Freigabe des Wortlauts und Einbau von 6.1 bleiben bei Task 12a. Plan-Nachtrag 02.10. mit Startsatz in § 8.

**Offen beim Verfasser:** Version of Record als PDF in `Ideen und Studien` ablegen (frei über https://doi.org/10.2196/84822 oder PMC13626193), den Preprint umbenennen (Dateiname mit „Preprint“) oder in den Papierkorb verschieben. Danach Task „Boumparis“ mit dem Startsatz aus Plan § 8 eröffnen.

**Stand der Dateien:** Neu: {PROMPTPFAD}, Projektkopie `claude/` · `03_Skripte\\Steuerung_Rev148_2026-10-02.py` mit `.txt`. Geändert: diese Notizen (Rev. 148 auf Rev. 147) · Maßnahmenliste (Stand, H16 Vermerk, Taskzeilen 12 und 13, Summe) · Plan (Nachtrag 02.10., Startsatz in § 8), je Ordner und Projektkopie. Durch diesen Task unverändert: Master, Kennzahlenblatt, Fassung 17, Textvorschläge, T1, T4, Befund Rev. 147. Rückschreibung aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** Version of Record ablegen, dann Task „Boumparis“. Danach Freigabe und Einbau von 6.1 in Task 12a mit dem freigegebenen Modul oder ohne, dann Task 12b. Reihenfolge sonst wie Rev. 146.

"""
anker = '### ⭐ NACHTRAG (Rev. 147, 02.10.2026, 15:06 Sitzungsuhr, Auftrag 14:10)'
n = ersetze(n, anker, block + anker, 'Notizen Block Rev. 148', prot)

# ---------- Maßnahmenliste ----------
l = ersetze(l, '**Stand 02.10.2026, 15:06 Sitzungsuhr (Rev. 147 — ',
            f'**Stand 02.10.2026, {UHR} Sitzungsuhr (Rev. 148 — Boumparis et al. im Ordner als Preprint, Prompt für den Task „Boumparis“ (Analyse und Einarbeitung, Vergleichssatz K2 zu 6.1), H16 Vermerk, Taskzeilen 12 und 13 fortgeschrieben). Zuvor 02.10.2026, 15:06 Sitzungsuhr (Rev. 147 — ',
            'Liste Stand', prot)

h16_ende = 'MDPI kennzeichnen. *(Sitzung 02.10., Rev. 147)*'
h16_neu = (h16_ende + ' *(Rev. 148, 02.10.: Im Ordner liegt seit 15:26 Sitzungsuhr der Preprint (JMIR Preprints, eingereicht 25.09.2025, Dateiname mit 2025), nicht zitierfähig. '
           'Offen bleibt die Version of Record als PDF (doi 10.2196/84822, frei über PMC13626193), den Preprint umbenennen oder in den Papierkorb. '
           'Für die Adhärenzwerte ist die Quellenart „systematische Übersicht“, metaanalytisch zusammengefasst ist nur der Studienabbruch. '
           f'Analyse und Einarbeitung im Task „Boumparis“, Prompt {PROMPTPFAD}.)*')
l = ersetze(l, h16_ende, h16_neu, 'Liste H16', prot)

t12_ende = '· H16 · Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 1 und 4 (12a), Nr. 2 (12b) |'
l = ersetze(l, t12_ende,
            f'· H16 · Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 1 und 4 (12a), Nr. 2 (12b) · Task „Boumparis“ (Rev. 148): Vergleichssatz für das Modul A2-M (K2) und Satzkerne für 12b, Prompt {PROMPTPFAD} |',
            'Liste Taskzeile 12', prot)

t13_ende = '· Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 3 (Ausblick) |'
l = ersetze(l, t13_ende,
            '· Recherche Umsetzungsrate (Rev. 147) § 6 Nr. 3 (Ausblick) · Task „Boumparis“ (Rev. 148), Satzkern für den Ausblick |',
            'Liste Taskzeile 13', prot)

l = ersetze(l, '| **Summe** | Rev. 147 (02.10.): ',
            '| **Summe** | Rev. 148 (02.10.): H16 Vermerk (Preprint im Ordner, Version of Record offen), Taskzeilen 12 und 13 fortgeschrieben, keine neuen Punkte, Zählung nicht neu erhoben. Zuvor: Rev. 147 (02.10.): ',
            'Liste Summe', prot)

# ---------- Plan ----------
nachtrag = ('**Nachtrag 02.10.2026 (Rev. 148 der Sitzungsnotizen), keine neue Revision des Plans:** '
            'Der Textvorschlag 6.1 aus Task 12a liegt vor (`04_Uebergaben\\Textvorschlag_6.1_2026-10-02.md`, Dateizeit 15:31 Sitzungsuhr, Stand nach der Zweitprüfung). '
            'Offen sind der Vergleichssatz der Umsetzung (Modul A2-M, Klick K2), K5, die Freigabe und der Einbau. '
            'Für K2 hat der Verfasser die Recherche Umsetzungsrate beauftragt (Rev. 147) und Boumparis et al. in den Ordner gelegt, als Preprint, die Version of Record (2026) steht aus. '
            'Neu ist der **Task „Boumparis“** (Verfasser 02.10., 15:28) zwischen Textvorschlag und Freigabe von 12a: '
            f'Analyse von Boumparis et al. (2026) und Einarbeitung in die Argumentationskette nach {PROMPTPFAD}, '
            'mit dem Vergleichssatz für A2-M und Satzkernen für 12b, 13a und die Schlussfassung der Einleitung. '
            'Reihenfolge: Task „Boumparis“ → Freigabe und Einbau von 6.1 (Task 12a) → Task 12b → Task 13a → Task „Einleitung, Schlussfassung“ → Task 13b → Steuerdokumente-Task → Tasks 15 bis 18. '
            'Startsatz in § 8.\n\n')
pl = ersetze(pl, 'Nächster Task: 12a.\n\n## 0 Ergebnis in Kürze',
             'Nächster Task: 12a.\n\n' + nachtrag + '## 0 Ergebnis in Kürze', 'Plan Nachtrag 02.10.', prot)

startsatz = ('- **Task „Boumparis“ (zwischen Textvorschlag und Freigabe von 12a, Nachtrag 02.10.):** '
             f'„Task Boumparis nach Plan Nachtrag 02.10. Lies zuerst Teil 0 der Sitzungsnotizen (mindestens Rev. 148), dann {PROMPTPFAD} vollständig und arbeite ihn ab. '
             'Kein Manuskripttext im Master, Rücksprache nur per Klick.“\n')
anker12b = '- **Task 12b (6.2 und 6.3):**'
pl = ersetze(pl, anker12b, startsatz + anker12b, 'Plan Startsatz § 8', prot)

os.makedirs(AUS, exist_ok=True)
nb2, lb2, plb2 = n.encode('utf-8'), l.encode('utf-8'), pl.encode('utf-8')
open(os.path.join(AUS, 'Cowork_Sitzungsnotizen.md'), 'wb').write(nb2)
open(os.path.join(AUS, 'Massnahmenliste_Datenverarbeitung.md'), 'wb').write(lb2)
open(os.path.join(AUS, 'Plan_Weitere_Schritte_2026-09-25.md'), 'wb').write(plb2)
prot.append(f'Ausgang Notizen: {len(nb2)} Byte, MD5 {md5(nb2)}')
prot.append(f'Ausgang Maßnahmenliste: {len(lb2)} Byte, MD5 {md5(lb2)}')
prot.append(f'Ausgang Plan: {len(plb2)} Byte, MD5 {md5(plb2)}')
prot.append(f'Semikola im neuen Block: {block.count(";")} · im H16-Vermerk: {h16_neu.count(";")} · im Plan-Nachtrag: {nachtrag.count(";")} · im Startsatz: {startsatz.count(";")}')
print('\n'.join(prot))

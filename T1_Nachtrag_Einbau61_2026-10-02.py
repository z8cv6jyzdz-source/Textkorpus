# -*- coding: utf-8 -*-
"""T1_Nachtrag_Einbau61_2026-10-02.py — T1-Nachführung nach dem Einbau von 6.1 (Task 12a, 02.10.2026, abends).

Zwei Steckbriefe werden geändert, sonst nichts (Nachtrag K2 § 8.1 Nr. 3 und Nr. 5):
  Liu2024.kapitel        „2.3, 5.5“ (alte Gliederung) → 6.2/6.3 G8, seit Variante A nicht in 6.1 und nicht in der Einleitung.
                          Die Distanzfelder (2 · 1 · 2) bleiben, die Angleichung an die Belegtabelle 6.1 (1 · 1 · 0) ist für 12b vorgemerkt.
  Boumparis2026.fassung  Stand nach Ablage der PDF der Version of Record in „Ideen und Studien“ (02.10.2026), am PDF geprüft:
                          Titel, 116 Studien, DOI 10.2196/84822, Interact J Med Res 2026, 15, e84822, 24 Seiten, Seitenzahlen der Fundstellen.
Jede Änderung greift auf genau eine Zeile mit genau dem erwarteten Altwert, sonst Abbruch. Lese- und Schreibkonvention wie
T1_T4_Nachtrag_Boumparis_2026-10-02.py (utf-8-sig, Trennzeichen chr(59), LF, QUOTE_MINIMAL). Ohne Semikolon im Skript.
Hinweis: T1_T4_Nachtrag_Boumparis_2026-10-02.py setzt bei einem erneuten Lauf das Feld `fassung` von Boumparis2026 auf seinen
eigenen Stand zurück. Es darf ohne Nachführung seiner T1_NEU-Zeile nicht erneut laufen.
Aufruf: python3 T1_Nachtrag_Einbau61_2026-10-02.py <Quellordner ev3_daten> <Zielordner>
"""
import csv
import hashlib
import os
import sys

SEMI = chr(59)

LIU_ALT = '2.3, 5.5'
LIU_NEU = ('6.2/6.3 G8 (Korpuslücke Setting und Übergangsperiode, Vormerkung Task 12b, Textvorschlag 6.1 § 9.1 Nr. 4). '
           'Seit Variante A des Nachtrags K2 (Klick 02.10.2026) nicht in 6.1 (A3 S8 entfallen, Stufe 1 der Kürzungsleiter), '
           'nicht in der Einleitung. Distanzfelder 2 · 1 · 2 gegen 1 · 1 · 0 der Belegtabelle 6.1 vor 12b angleichen')

BOUM_ALT_ANFANG = 'Version of Record vom 30.09.2026 (Interact J Med Res 15, e84822, PMID 42814774, PMC13626193), am '
BOUM_NEU = ('Version of Record vom 30.09.2026 (Interact J Med Res 2026, 15, e84822, doi 10.2196/84822, PMID 42814774, '
            'PMC13626193). Am 02.10.2026 zuerst als PMC-Volltext über PubMed gelesen (Analysebefund), seit dem Abend des 02.10. '
            'liegt die PDF der Version of Record in „Ideen und Studien“ („2026 Boumparis et al., Factors Influencing Adherence to '
            'Digital Lifestyle Interventions for Adolescents Systematic Review and Meta-Analysis of Attrition.pdf“, 503.950 Byte, '
            'MD5 7b0c5660e07874d998c2ec20819b3dad, 24 Seiten, Antenna House, ohne Multimedia Appendix 1). Am PDF geprüft: Titel, '
            '116 Studien, DOI. Seitenzahlen der Fundstellen: Abstract › Conclusions S. 1 · Methods › Eligibility Criteria und '
            'Identification of Studies S. 3 · Results › Characteristics of Digital Interventions S. 6 (Bestandteil-Adhärenz 55,2 %, '
            'SD 25,5 %, 66 Vergleiche) · Results › Quantitative Synthesis of Attrition S. 7 bis 8 · Discussion › Principal Findings '
            'S. 12 · Domain-Specific Adherence Patterns, Limitations und Implications for Future Research S. 14. Der Preprint '
            '(„2025 Boumparis et al., Factors Influencing Adherence to Digital Lifestyle interventions for adolescence.pdf“, '
            '1.062.847 Byte) bleibt im Ordner, ist nicht zitierfähig. H16 erledigt')


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
    assert SEMI not in LIU_NEU and SEMI not in BOUM_NEU
    qp = os.path.join(quelle, 'T1_steckbriefe.csv')
    felder, zeilen = lese(qp)
    protokoll = ['T1_Nachtrag_Einbau61_2026-10-02.py — Protokoll',
                 'T1 vorher: %s, %d Steckbriefe, MD5 %s' % (qp, len(zeilen), md5(qp))]
    liu = [z for z in zeilen if z['id'] == 'Liu2024']
    boum = [z for z in zeilen if z['id'] == 'Boumparis2026']
    assert len(liu) == 1 and len(boum) == 1, 'Liu2024 oder Boumparis2026 nicht genau einmal vorhanden'
    assert liu[0]['kapitel'] == LIU_ALT, 'Liu2024.kapitel unerwartet: %r' % liu[0]['kapitel']
    assert boum[0]['fassung'].startswith(BOUM_ALT_ANFANG), 'Boumparis2026.fassung unerwartet: %r' % boum[0]['fassung'][:80]
    liu[0]['kapitel'] = LIU_NEU
    boum[0]['fassung'] = BOUM_NEU
    protokoll.append('Liu2024.kapitel: %r → %r' % (LIU_ALT, LIU_NEU[:60] + '…'))
    protokoll.append('Boumparis2026.fassung: PMC-Volltext ohne PDF → PDF der Version of Record im Ordner, Seitenzahlen der Fundstellen')
    zp = os.path.join(ziel, 'T1_steckbriefe.csv')
    schreibe(zp, felder, zeilen)
    f2, z2 = lese(zp)
    assert f2 == felder and len(z2) == len(zeilen), 'Rücklesen weicht ab'
    unveraendert = sum(1 for a, b in zip(zeilen, z2) if a == b)
    assert unveraendert == len(zeilen), 'Rücklesen weicht inhaltlich ab'
    protokoll.append('T1 nachher: %s, %d Steckbriefe, MD5 %s, zwei Felder geändert, alle anderen Zeilen unverändert' % (zp, len(z2), md5(zp)))
    with open(os.path.join(ziel, 'T1_Nachtrag_Einbau61_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(protokoll) + '\n')
    print('\n'.join(protokoll))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""Textvorschlag 6.1 Einordnung der Ergebnisse (Task 12a, 02.10.2026).

Fassung 3 (03.10.2026): A3, A4 und A5 zeichengleich aus dem freigegebenen Nachtrag Argumentationsstruktur übernommen
(`Diskussion_Anwendung_2026-10-03/S3_Nachtrag.json`, Nachtrag Fassung 3, Klick des Verfassers 03.10.2026 gegen 15:52
Sitzungsuhr): A3 ohne den Satz zu Ramirez-Campillo et al. (2020) (Stufe 3 der Kürzungsleiter) und ohne „zudem“ (P6),
A4 mit der Population in S4, der Markierung „vereinbar“ in S6 und dem modalen Erklärungsangebot in S9 (P1, P2 mit P5),
A5 mit der Markierung „vereinbar“ in S6 (P1). A1, A2 und A6 unverändert. Die JSON trägt das Feld „fassung“.

Fassung 2 (02.10., abends): Variante A des Nachtrags K2 (Klick des Verfassers, Rev. 151) zeichengleich aus
`Textvorschlag_6.1_Nachtrag_K2_2026-10-02.json` übernommen, der Vergleichssatz zu Boumparis et al. (2026) steht in A2 nach S2,
A2 S3 lautet „Der Schätzer ist durch die eigene Umsetzung stark verdünnt: …“, A3 ohne den Satz zu Liu et al. (2024)
(Stufe 1 der Kürzungsleiter). Das Modul A2-M entfällt. Fassung 1 (nachmittags) hielt A1 bis A6 und das offene Modul.

Hält den Wortlaut der Absätze A1 bis A6, misst ihn wie das Messskript
(Manuskriptstand_2026-09-25.py Fassung 4: Wörter als Leerraum-Token, Satzteilung saetze(), Semikola außerhalb
von Zitierklammern, nummerierte Abschnittsverweise RE_REF) und prüft die Sprachregelungen (F17 § 10, § 11.2b,
Stilprofil Teil 3 und 4). Ausgabe: .txt (Messprotokoll) und .json (Wortlaut je Absatz für den Einbau per Skript).

Aufruf: python3 Textvorschlag_6.1_2026-10-02.py [Ausgabeordner]
Ohne Semikolon im Skript (chr(59)).
"""
import json
import os
import re
import statistics
import sys

SEMI = chr(59)
BUDGET = 700
ZIEL = {'A1': 105, 'A2': 120, 'A3': 130, 'A4': 135, 'A5': 135, 'A6': 55}
FASSUNG = ('3 (03.10.2026): A3 bis A5 nach dem Nachtrag Argumentationsstruktur (Fassung 3), freigegeben per Klick des '
           'Verfassers am 03.10.2026 gegen 15:52 Sitzungsuhr, A1, A2 und A6 wie Fassung 2 (02.10.2026, Variante A des Nachtrags K2)')

# ----------------------------------------------------------------------------------------------------------
# Wortlaut (Arbeitskennungen A1 bis A6 gehören nicht in den Master)
# ----------------------------------------------------------------------------------------------------------
ABSAETZE = {
'A1': (
"Ziel der Studie war es zu prüfen, ob ein sechswöchiges videobasiertes, gerätefreies plyometrisches "
"Heimtrainingsprogramm in der Sommerpause die Sprint-, Richtungswechsel- und Sprungleistung männlicher "
"U15-Fußballspieler des leistungsorientierten Breitensports gegenüber einer Kontrollgruppe verbessert. "
"Nach Adjustierung für Ausgangswert und Reifestatus war bei keiner Zielgröße ein Gruppenunterschied "
"nachweisbar, die Nullhypothese wurde nicht verworfen. "
"Zwar lag die Interventionsgruppe auch nach der Sommerpause in allen konfirmatorischen Zielgrößen vorn. "
"Dieser Vorsprung entsprach jedoch weitgehend dem, was nach Ausgangswert und Reifestatus zu erwarten war. "
"Die Konfidenzintervalle schlossen relevante Vorteile wie Nachteile des Programmangebots ein. "
"Die Befunde sind unschlüssig, ein Vorteil des Angebots ist weder belegt noch ausgeschlossen."
),
'A2': (
"Die Hauptanalyse schätzt die Wirkung des Programmangebots, nicht die des Trainings. Die zugeteilten Spieler "
"meldeten weniger als die Hälfte der angebotenen Einheiten als vollständig, einige keine einzige. Auch in "
"digitalen Lebensstilprogrammen für Jugendliche wurde nach einer systematischen Übersicht im Mittel nur gut "
"die Hälfte der Programmbestandteile absolviert, bei großer Streuung (Boumparis et al., 2026). Der Schätzer "
"ist durch die eigene Umsetzung stark verdünnt: Ein nicht nachweisbarer Unterschied bedeutet zunächst nur, "
"dass das Angebot in dieser Umsetzung nichts Nachweisbares bewirkt hat. Der beobachtende "
"Per-Protokoll-Vergleich der Spieler mit mindestens der Hälfte der Einheiten als vollständig gemeldet änderte "
"die Einordnung nicht. Seine Punktschätzer lagen nahe null und wechselten das Vorzeichen, beim "
"Richtungswechsel reichte die Fallzahl nicht für eine Inferenz."
),
'A3': (
"Hohe Laufgeschwindigkeit, die die 30-m-Zeit mit erfasst, verlangt große Kräfte in kurzen Bodenkontakten "
"(Oliver et al., 2024). Beschreibend lagen die mittleren 30-m-Zeiten der Interventionsgruppe nach der "
"Sommerpause etwas höher als zuvor, die der Kontrollgruppe gleich. Die adjustierte Gruppendifferenz lag nahe "
"null, ihr Intervall ließ relevante Unterschiede in beide Richtungen zu. Metaanalysen fanden plyometrisches "
"Training bei jungen Fußballspielern überwiegend höherer Spielklassen für die Sprintleistung über 15 bis 40 m "
"wirksam (Oliver et al., 2024" + SEMI + " "
"Zheng et al., 2025). Der eigene Befund blieb dahinter zurück, schließt solche Effekte aber nicht aus. Beim "
"Sprint war am wenigsten zu erwarten: Programme mit vertikalen Sprüngen und langen Bodenkontakten dürften eher "
"Sprung, Beschleunigung und Richtungswechsel ansprechen (Oliver et al., 2024), Sprintinhalte fehlten."
),
'A4': (
"Der 505-Test prüft Entschleunigen und erneutes Beschleunigen, Bausteine der im Wettkampf häufigen "
"Richtungswechsel. "
"Beschreibend blieb das 505-Seitenmittel in beiden Gruppen nahezu unverändert. "
"Die adjustierte Differenz lag nahe null, ihr Intervall ließ relevante Unterschiede in beide Richtungen zu. "
"Eine Metaanalyse fand die Richtungswechselleistung, überwiegend von Mädchen, in keiner Reifegruppe "
"nachweisbar verbessert (Ramirez-Campillo et al., 2023). "
"Eine weitere fand sie insgesamt verbessert, in den Einzeltests nur im Illinois-Test, den 505-Test enthielt "
"sie nicht (Zheng et al., 2025). "
"Mit beiden ist der eigene Befund vereinbar. "
"Dagegen verbesserte plyometrisches Training die Richtungswechselleistung hochtrainierter Akademiespieler "
"nach einer Metaanalyse deutlich (Oliver et al., 2024). "
"Auch ein achtwöchiges Programm mit nahezu gleichem Kontaktverlauf verbesserte die 505-Zeit präpubertärer "
"Spieler deutlich, bei nicht adjustiertem Alters- und Reifeunterschied zur Kontrollgruppe (Sammoud et al., "
"2024). "
"Den Abstand könnte weniger die Übungsauswahl als die eigene Umsetzung erklären, auch das Vergleichsprogramm "
"kam ohne Wende aus."
),
'A5': (
"Der Standweitsprung steht den Programmübungen am nächsten, er gehörte selbst dazu. "
"Beschreibend sanken die mittleren Weiten beider Gruppen, was mit der Sommerpause zusammenhängen könnte. "
"Die adjustierte Differenz lag nahe null, ihr Intervall ließ relevante Unterschiede in beide Richtungen zu. "
"Das widerspricht Metaanalysen, nach denen plyometrisches Training die horizontale Sprungleistung junger "
"Fußballspieler überwiegend höherer Spielklassen verbesserte (Oliver et al., 2024" + SEMI + " Zheng et al., "
"2025). "
"Auch das Programm mit nahezu gleichem Kontaktverlauf steigerte die Weite präpubertärer Spieler deutlich "
"(Sammoud et al., 2024). "
"Die Sprunghöhe von Schülern nach dem Wachstumsgipfel blieb in einer älteren kontrollierten Studie "
"nach sechs Wochen ohne nachweisbare Veränderung (Lloyd et al., 2016), was mit dem eigenen Befund vereinbar ist. "
"Wann sich die Weite verbessert, ist offen: Bei präpubertären Spielern war sie erst nach acht Wochen "
"gegenüber dem Ausgangswert nachweisbar besser (Negra et al., 2020). "
"Beide Gruppen lagen im Mittel schon bei der Eingangstestung über dem 90. Perzentil gleichaltriger "
"europäischer Schulkinder, erhoben auf hartem Boden (Thomas et al., 2020)."
),
'A6': (
"Die als vollständig gemeldeten Einheiten wurden im Mittel als leicht bis mäßig anstrengend empfunden. "
"Mehr als die Hälfte der Spieler mit Meldungen nannte mindestens einmal Schmerzen oder Probleme, "
"überwiegend zu vollständig durchgeführten Einheiten. "
"Einige betrafen teilweise oder nicht durchgeführte Einheiten, einen Abbruch wegen Beschwerden belegen sie "
"nicht. "
"Ob sie mit dem Programm zusammenhingen, ist ohne Vergleichsdaten der Kontrollgruppe nicht beurteilbar. "
"Die Abwägung von Nutzen und Schaden bleibt unvollständig."
),
}
REIHENFOLGE = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']

# ----------------------------------------------------------------------------------------------------------
# Messung wie Manuskriptstand_2026-09-25.py (Fassung 4)
# ----------------------------------------------------------------------------------------------------------
RE_REF = re.compile(r'Abschn(?:itt)?\.?\s*\d|Kapitel\s*\d|siehe (?:oben|unten)')
NAME = r"[A-ZÄÖÜ][A-Za-zÄÖÜäöüßéèáíóúñ'’\-]+"
AUTOR = r"(?:R Core Team|" + NAME + r"(?:,\s" + NAME + r",\set al\.|\set al\.|\s(?:&|und)\s" + NAME + r")?)"


def saetze(text):
    t = re.sub(r'(\d)\.(\d)', r'\1<P>\2', text)
    t = re.sub(r'\b(et al|Abschn|Tab|Abb|vgl|bzw|ca|Nr|Aufl|Hrsg|Jg)\.', r'\1<P>', t)
    t = re.sub(r'\b([A-Z])\.\s', r'\1<P> ', t)
    t = re.sub(r'\bS\.\s', 'S<P> ', t)
    t = re.sub(r'\b(u|z|d)\.\s?(a|B|h)\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.(\d{4})', r'\1<P>\2<P>\3', t)
    t = re.sub(r'(\d{2})\.(\d{2})\.', r'\1<P>\2<P>', t)
    t = re.sub(r'(\d)\.\s', r'\1<P> ', t)
    teile = [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-ZÄÖÜ„(⟨])', t) if s.strip()]
    return [s.replace('<P>', '.') for s in teile]


def ohne_zitierklammern(text):
    return re.sub(r'\([^)]*\d{4}[^)]*\)', '', text)


def belegklammern(text):
    return re.findall(r'\([^()]*?\d{4}[^()]*?\)', text)


# Sprachregelungen: Wörter und Wendungen, die in 6.1 nicht stehen dürfen (F17 § 10, § 11.2b, Stilprofil)
VERBOTEN = [
    'randomisiert', 'randomized', 'kein Effekt', 'wirkungslos', 'gleich wirksam', 'Erhalt', 'Schutz vor',
    'ITT', 'sodass', 'weshalb', 'im Rahmen', 'Gegenstand der Untersuchung', 'es ist festzuhalten',
    'darüber hinaus', 'des Weiteren', 'hierbei gilt', 'Responder', 'signifikant', 'adressiert', 'beseitigt',
    'Wirkung des Programms', 'Wirkung des Trainings', 'profitier', 'klein', 'moderat', 'groß', 'trivial',
    'MDES', 'Power', 'Familienfehler', 'genuinely', 'Abschn.', 'siehe oben', 'siehe unten',
]
# Mechanismen nur modalisiert: Sätze mit diesen Signalwörtern müssen ein Modalverb tragen
MECHANISMUS_SIGNAL = ['Erklärung', 'angesprochen', 'zu kurz', 'überlasten']
MODAL = ['könnte', 'könnten', 'dürfte', 'dürften', 'kann', 'können', 'mag', 'ließe', 'käme', 'lässt sich']


def pruefe(text, key):
    befunde = []
    for v in VERBOTEN:
        # 'groß' nur als Etikett prüfen, 'großen Kräften' ist keins
        if v == 'groß':
            if re.search(r'\bgroß(?:e|er|es)?\s+(?:Effekt|Unterschied)', text):
                befunde.append('Etikett „groß“')
            continue
        if v == 'klein' and re.search(r'\bklein(?:e|er|es)?\s+(?:Effekt|Unterschied)', text):
            befunde.append('Etikett „klein“')
            continue
        if v in ('klein',):
            continue
        if v == 'ITT':
            if re.search(r'\bITT\b', text):
                befunde.append('Verbotswort „ITT“')
            continue
        if v.lower() in text.lower():
            befunde.append('Verbotswort „%s“' % v)
    if SEMI in ohne_zitierklammern(text):
        befunde.append('Semikolon außerhalb einer Zitierklammer')
    if RE_REF.search(text):
        befunde.append('nummerierter Abschnittsverweis')
    for s in saetze(text):
        if len(s.split()) > 32:
            befunde.append('Satz über 32 Wörter: „%s…“' % ' '.join(s.split()[:6]))
        if any(m in s for m in MECHANISMUS_SIGNAL) and not any(m in s for m in MODAL):
            befunde.append('Mechanismus ohne Modalverb: „%s…“' % ' '.join(s.split()[:6]))
    if len(text.split()) > 250:
        befunde.append('Absatz über 250 Wörter')
    return befunde


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    zeilen = ['Textvorschlag 6.1 — Messprotokoll (Fassung 3, 03.10.2026, A3 bis A5 nach dem freigegebenen Nachtrag '
              'Argumentationsstruktur, Zählung wie Messskript Fassung 4)', '']
    gesamt = 0
    alle_saetze = []
    json_out = {'abschnitt': '6.1', 'titel': '6.1 Einordnung der Ergebnisse', 'budget': BUDGET, 'fassung': FASSUNG,
                'absaetze': []}
    for key in REIHENFOLGE:
        text = ABSAETZE[key]
        w = len(text.split())
        ss = saetze(text)
        sl = [len(s.split()) for s in ss]
        alle_saetze.extend(sl)
        gesamt += w
        bk = belegklammern(text)
        bef = pruefe(text, key)
        zeilen.append('%s: %d Wörter (Ziel %d), %d Sätze, Median %.1f, längster %d, Belegklammern %d%s'
                      % (key, w, ZIEL[key], len(ss), statistics.median(sl), max(sl), len(bk),
                         ', Semikola in Klammern %d' % sum(k.count(SEMI) for k in bk) if bk else ''))
        for b in bef:
            zeilen.append('   BEFUND: ' + b)
        json_out['absaetze'].append({'kennung': key, 'text': text, 'woerter': w, 'saetze': len(ss),
                                     'modul': False})
    zeilen.append('')
    zeilen.append('Summe 6.1 (A1 bis A6, kein offenes Modul): %d Wörter (Budget %d, Rest %d)' % (gesamt, BUDGET, BUDGET - gesamt))
    zeilen.append('Sätze gesamt: %d, Median %.1f Wörter, längster %d' % (len(alle_saetze), statistics.median(alle_saetze), max(alle_saetze)))
    alle = ' '.join(ABSAETZE[k] for k in REIHENFOLGE)
    zeilen.append('Semikola außerhalb von Zitierklammern: %d · nummerierte Abschnittsverweise: %d · Belegklammern: %d'
                  % (ohne_zitierklammern(alle).count(SEMI), len(RE_REF.findall(alle)), len(belegklammern(alle))))
    zahlen = re.findall(r'\d+(?:,\d+)?', ohne_zitierklammern(alle))
    zeilen.append('Ziffernzahlen außerhalb von Zitierklammern: %s' % (', '.join(zahlen) if zahlen else 'keine'))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'Textvorschlag_6.1_2026-10-02.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(zeilen) + '\n')
    with open(os.path.join(out, 'Textvorschlag_6.1_2026-10-02.json'), 'w', encoding='utf-8') as f:
        json.dump(json_out, f, ensure_ascii=False, indent=1)
    print('\n'.join(zeilen))


if __name__ == '__main__':
    main()

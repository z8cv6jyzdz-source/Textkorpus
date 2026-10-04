# -*- coding: utf-8 -*-
"""
Projektanweisungen_Fassung17_2026-09-28.py — erzeugt Fassung 17 aus Fassung 16 (gezielte Ersetzungen, jede genau einmal,
ganze Abschnitte zwischen zwei Überschriften). Anlass: Task Steuerdokumente 28.09. (Übergabe
`04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` § 4): Einleitung statt Kapitel 1 bis 3, 6.350 Wörter, höchstens
33 Seiten einschließlich Literaturverzeichnis, Kapitel 4 fertig, Relevanz und Prävention, Entscheidungen seit dem 26.09.,
Unstimmigkeiten aus Fassung 16, Klicks K1, K2, K3 und K6 (28.09., 16:27 Sitzungsuhr).
Messwerte kommen aus der Ausgabe des Messskripts Fassung 3 (`Manuskriptstand_2026-09-25.csv` und `.txt`), die
Seitenrechnung aus `Seitenmodell_2026-09-28.csv` und `.txt`, die Zahl der Einträge von T1 und T4 aus den Dateien, Wortzahlen
des Textvorschlags Einleitung aus dessen Kopf und Zug-Tabelle. Keine Zahl von Hand.
Aufruf: python Projektanweisungen_Fassung17_2026-09-28.py <F16.md> <F17.md> <Manuskriptstand.csv> <Manuskriptstand.txt>
        <Seitenmodell.csv> <T1_steckbriefe.csv> <T4_zitierfallen.csv> <Textvorschlag_Einleitung.md> <Seitenmodell.txt>
Ohne Semikolon im Skript (chr(59)).
Fassung 2 (28.09., nach der Zweitprüfung): Befunde 1 bis 33 der Zweitprüfung, Rev. 114 aus Task 7 neu (Textvorschlag
Einleitung, parallel entstanden), Klicks zu § 6.6 (nach der Zweitprüfung) und § 6.2 (17:54 Sitzungsuhr).
Fassung 3 (28.09., nach der übergreifenden Zweitprüfung der Steuerdokumente): Befunde 4, 5, 27, 36 und 40, Klicks von
19:25 Sitzungsuhr zum Erratum Khamis & Roche (kein Hinweis in der Arbeit) und zur Verdünnungslogik (6.1, Limitation in 6.3).
"""
import sys
import re
import csv
import io

F16, F17, M_CSV, M_TXT, S_CSV, T1, T4, TV_E, S_TXT = sys.argv[1:10]
SEMI = chr(59)
t = open(F16, encoding='utf-8').read()
PROTOKOLL = []


def rep(alt, neu, anz=1):
    """Ersetzt eine Textstelle, die genau anz-mal vorkommen muss, sonst Abbruch."""
    global t
    n = t.count(alt)
    if n != anz:
        raise SystemExit('Abbruch: %d Treffer statt %d für: %s' % (n, anz, alt[:120]))
    t = t.replace(alt, neu)
    PROTOKOLL.append(alt[:70].replace('\n', ' '))


def zeile(praefix, neu):
    """Ersetzt die eine Zeile, die mit praefix beginnt."""
    global t
    zl = t.split('\n')
    idx = [i for i, z in enumerate(zl) if z.startswith(praefix)]
    if len(idx) != 1:
        raise SystemExit('Abbruch: %d Zeilen beginnen mit: %s' % (len(idx), praefix[:100]))
    zl[idx[0]] = neu
    t = '\n'.join(zl)
    PROTOKOLL.append('Zeile: ' + praefix[:62])


def abschnitt(von, bis, neu):
    """Ersetzt den Text ab der Zeile, die mit von beginnt, bis vor die Zeile, die mit bis beginnt."""
    global t
    zl = t.split('\n')
    i0 = [i for i, z in enumerate(zl) if z.startswith(von)]
    if len(i0) != 1:
        raise SystemExit('Abbruch: Abschnittsbeginn %d-mal: %s' % (len(i0), von))
    i1 = [i for i, z in enumerate(zl) if i > i0[0] and z.startswith(bis)]
    if not i1:
        raise SystemExit('Abbruch: Abschnittsende nicht gefunden: %s' % bis)
    zl = zl[:i0[0]] + neu.rstrip('\n').split('\n') + [''] + zl[i1[0]:]
    t = '\n'.join(zl)
    PROTOKOLL.append('Abschnitt: ' + von[:60])


def de(x, nk=0):
    s = ('%.' + str(nk) + 'f') % x
    ganz, _, dez = s.partition('.')
    g = []
    while len(ganz) > 3:
        g.insert(0, ganz[-3:])
        ganz = ganz[:-3]
    g.insert(0, ganz)
    return '.'.join(g) + (',' + dez if dez else '')


# ------------------------------------------------------------------ Messwerte und Parameter aus den Dateien
w = {}
for r in csv.DictReader(open(M_CSV, encoding='utf-8')):
    w[r['arbeitsnummer']] = int(r['woerter'])
mess = open(M_TXT, encoding='utf-8').read()
W = {k: w[k] for k in ['4.1', '4.2', '4.3', '4.5.1', '4.5.2', '4.6', '4.7']}
W['4.4'] = w['4.4'] + w['4.4.1'] + w['4.4.2'] + w['4.4.3']
K4O = sum(W[k] for k in ['4.1', '4.2', '4.3', '4.4', '4.5.1', '4.5.2', '4.6'])
K4 = K4O + W['4.7']
ALT = sum(w[k] for k in ['2', '2.1', '2.2', '2.3', '2.4', '2.4.1', '2.4.2', '2.4.3', '2.5', '3'])
GES = sum(v for k, v in w.items() if re.match(r'^[1-7](\.|$)', k))
SEMI_N = int(re.search(r'Semikola außerhalb von Zitierklammern, Kapitel 1 bis 7: (\d+)', mess).group(1))
VERW_N = int(re.search(r'Nummerierte Abschnittsverweise, Kapitel 1 bis 7: (\d+)', mess).group(1))
m_alt = re.search(r'davon im Altbestand Kapitel 2 und 3: (\d+) Semikola, (\d+) Abschnittsverweise', mess)
if not m_alt or int(m_alt.group(1)) != SEMI_N or int(m_alt.group(2)) != VERW_N:
    raise SystemExit('Abbruch: Semikola oder Verweise stehen nicht vollständig im Altbestand, Fassung 17 müsste anders lauten')
P = {r['parameter']: r['wert'] for r in csv.DictReader(open(S_CSV, encoding='utf-8'), delimiter=SEMI)}
D_E, D_R = float(P['dichte_einleitung']), float(P['dichte_kapitel_4_bis_7'])
JE_S = float(P['eintraege_je_seite'])
N_B, N_O = int(P['eintraege_basis']), int(P['eintraege_obere_variante'])
S_TEXT = 1500 / D_E + 4850 / D_R
S_OBJ = float(P['objekte_textteil']) * float(P['seiten_je_objekt'])
S_END = float(P['kapitelenden_textteil']) * float(P['seiten_je_kapitelende'])
S_TT = S_TEXT + S_OBJ + S_END
S_LIT = N_B / JE_S + float(P['seiten_je_kapitelende'])
S_GB = S_TT + S_LIT
S_GO = S_TT + N_O / JE_S + float(P['seiten_je_kapitelende'])
if abs(S_GB - float(P['prognose_gesamt_basis'])) > 0.01 or abs(S_GO - float(P['prognose_gesamt_obere'])) > 0.01:
    raise SystemExit('Abbruch: Seitenrechnung weicht von der Ausgabe des Seitenmodells ab')
VORSPANN = int(P['vorspann_seiten'])
N_T1 = len(list(csv.reader(open(T1, encoding='utf-8-sig'), delimiter=SEMI))) - 1
N_T4 = len(list(csv.reader(open(T4, encoding='utf-8-sig'), delimiter=SEMI))) - 1
FAKTOR = 6350 / 4127.0
UEBER = 6350 - 5448
WORD = 6350 * 1.21
REST = 450 + 1600 + 250
# Textvorschlag Einleitung (Task 7 neu, Rev. 114): Wortzahl aus dem Kopf, Präventionsteil aus der Zug-Tabelle
tv = open(TV_E, encoding='utf-8').read()
m_tv = re.findall(r'\| Wörter gesamt \| \*\*(\d{1,2}\.\d{3}|\d{3,4})\*\*', tv)
m_pr = re.findall(r'Prävention (\d+) Wörter', tv)
if len(m_tv) != 1 or len(m_pr) != 1:
    raise SystemExit('Abbruch: Wortzahl oder Präventionsteil im Textvorschlag Einleitung nicht eindeutig')
TV_W, TV_PR = m_tv[0], m_pr[0]
# Prognose des Messskripts (gemessene Wörter, sonst Budget) und gemessene Objektanteile aus dem Seitenmodell
m_mp = re.findall(r'Prognose Einleitung bis Ende Literaturverzeichnis: (\d+,\d) Seiten', mess)
stxt = open(S_TXT, encoding='utf-8').read()
m_ab = re.findall(r'Abb\. 1 .*?= (0,\d+) des Satzspiegels, Abb\. 2 .*?= (0,\d+)', stxt)
if len(m_mp) != 1 or len(m_ab) != 1:
    raise SystemExit('Abbruch: Prognose des Messskripts oder Objektmessung des Seitenmodells nicht eindeutig')
MP = m_mp[0]
A1, A2 = m_ab[0]

# ------------------------------------------------------------------ Kopf
KOPF = """Fassung 17, Stand 28.09.2026 (ersetzt Fassung 16 vom 25.09.2026, eingesetzt am 25.09.)

**Wirksam wird diese Fassung erst, wenn der Verfasser sie in die Projekteinstellungen einsetzt (Maßnahme A8).** Bis dahin gilt dort Fassung 16. Sicherung: `Claude\\00_Steuerung\\Projektanweisungen_Fassung17.md`, Projektkopie `claude/Projektanweisungen_Fassung17.md`. Erzeuger `Claude\\03_Skripte\\Projektanweisungen_Fassung17_2026-09-28.py`, Vergleich mit Fassung 16 und Prüfungen in `Claude\\03_Skripte\\Projektanweisungen_Vergleich_F16_F17_2026-09-28.txt`.

Neu in Fassung 17 — Stand nach Task 6, dem Neuzuschnitt vom 28.09. und dem Textvorschlag Einleitung (Teil 0 Rev. 107 bis 115):

**(A) Einleitung statt Kapitel 1 bis 3.** Kapitel 1, 2 und 3 werden eine Einleitung ohne Unterabschnitte mit höchstens 1.500 Wörtern (Verfasser 28.09., 14:38, Klick 14:57). Sie trägt Relevanz, Zielgrößen und Diagnostik, Sommerpause, Trainingsmittel, Reifung, Forschungsstand, Lücke, Zweck und Hypothesen. Die Vorgabe des SMK-Leitfadens, den Forschungsstand in einem eigenen Kapitel zu beschreiben (Abschn. 4.1), ist bewusst nicht erfüllt. Die Arbeit hat fünf Kapitel, bis Task 18 mit den Arbeitsnummern 1 und 4 bis 7 (§ 5.1). Task 7 neu lief parallel zu diesem Task: Der Textvorschlag `04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md` liegt mit %(tvw)s Wörtern vor, die Übertragung in den Master und der Abgleich danach stehen aus (Rev. 114, § 5a, § 13 Nr. 34 bis 37). Textvorschlag 2.4 Fassung 6 wird nicht übertragen (§ 13 Nr. 28).

**(B) Umfang: 6.350 Wörter und höchstens 33 Seiten einschließlich Literaturverzeichnis.** Die Wortgrenze sinkt mit der Einleitung von 9.000 auf 6.350 (§ 5.2). Die Seitengrenze des Verfassers (28.09., 15:14) zählt von der Einleitung bis zum Ende des Literaturverzeichnisses, ohne Vorspann und Anhang (Klick K1). Regel R6 entfällt (K2). Ein Objekt über die fünf festen hinaus kostet Wörter, sobald die Prognose 32 Seiten erreicht (K3). Das Messskript rechnet mit den gemessenen Wörtern %(mp)s Seiten, das Seitenmodell mit vollen Budgets rund %(GB)s, in der oberen Variante %(GO)s (Modellrechnung, § 1.1).

**(C) Kapitel 4 ist textlich fertig.** 4.1 %(w41)s · 4.2 %(w42)s · 4.3 %(w43)s · 4.4 %(w44)s · 4.5.1 %(w451)s · 4.5.2 %(w452)s · 4.6 %(w46)s · 4.7 %(w47)s, zusammen %(k4o)s gegen 2.000 und mit 4.7 %(k4)s gegen 2.550, ohne Semikolon und ohne Abschnittsverweis (Messung 28.09., Messskript Fassung 3, § 5.2). Nicht verbrauchte Wörter werden nicht aufgefüllt.

**(D) Relevanz und Prävention.** Leistung bleibt der Zweck nach Antrag. Die Relevanz für den leistungsorientierten Breitensport tragen Machbarkeit, das Zeitfenster der Sommerpause und die Lücke: kontrollierte Studien zu einem unbeaufsichtigten Heimprogramm in der Sommerpause für Spieler des leistungsorientierten Breitensports um den Wachstumsgipfel (§ 6.5). Prävention ist als Zusatznutzen der Programmklasse vorgemerkt, in der Einleitung (Olivier et al., 2026, dazu der Sprungbefund aus Rössler et al., 2014, als Zwischen-Studien-Vergleich, geplant rund 45 Wörter, im Textvorschlag %(tvpr)s) und als Satzteil im Ausblick (Klick 14:36, Befund `02_Befunde\\Argumentation_Relevanz_Breitensport_2026-09-28` Rev. 2, § 6.5, § 11.2b).

**(E) Entscheidungen seit dem 26.09.** (§ 13 Nr. 23 bis 39): 4.7 aus Task 6 mit Bootstrap als streichbarem Modul, Schlussabsatz nur mit Verfahren und Pflichtangaben, Anhang G ohne Prüfprotokolle, Festlegungsdaten für Tab. H6 vorgemerkt · direkter Einbau in Schritt 0 als Einzelfall · Zweck des Zielgrößenteils · Belege zu den Zielgrößen · Relevanz und Prävention · Einleitung · Seitengrenze mit Zählweise, R6 und Tauschregel · Ankersatz in 6.1 und in der Zusammenfassung, 4.1 bleibt ohne Zwecksatz (K6) · aus Task 7 neu: Verbleibsliste, Verletzungssatz, Reifemethode, Wortlaut des Zwecks · nach der Zweitprüfung dieser Fassung: Fitnessniveau bei de Villarreal et al. (2009), Vor-2020-Halbsatz nur bei Wirksamkeitsevidenz.

**(F) Rückschreibung mit Prüfung.** Am 28.09. meldeten Commits zweimal „written“ und hatten den vorherigen Stand geschrieben. Jede Rückschreibung geht aus einem eigenen, frischen Ausgabepfad mit kurzer Wartezeit, danach wird die Datei neu gestagt oder auf dem Rechner gelesen und per MD5 gegen die Ausgabe verglichen (§ 1.2, Rev. 112 und 114).

⚠ Korrigiert gegenüber Fassung 16 (Befunde vom 28.09.): § 6.6 und § 12 G8 stützten „Leistungsniveau“ auf p = 0,102 bei de Villarreal et al. (2009). Der Wert gehört zu „Fitness“, am PDF geprüft (Tab. 2, S. 501, T4 `dV2009`), die oberste Stufe beim Sportniveau beruht auf zwei Effektstärken einer einzigen Studie · § 11.4 nannte den Familienfehler „bis 14 %%“, nach der Entscheidungsregel sind es höchstens 7,5 %% · die fehlende unabhängige Methodenprüfung stand dreimal „in 4.7“, sie ist genau einmal für 6.3 vorgemerkt · § 1.3 führte Anhang G als Ort der Prüfprotokolle, seit dem 26.09. gilt Anhang G ohne Prüfprotokolle · der Ankersatz sollte in 4.1 wiederkehren, 4.1 hat keinen Zwecksatz (K6) · § 5.3 ordnete Aggregationsregel und 505-Regel 4.7 zu und den 20-m-Verzicht 4.4, die Regeln stehen in 4.4 und 4.4.2, der 20-m-Verzicht ist für Tab. H6 und 6.3 vorgemerkt · die Hypothesen werden nah am Antragswortlaut formuliert, H0 und H1 einander ergänzend (G32 e) · § 2 „Vergleichsevidenz überwiegend Tier 3+“ ist auf Oliver et al. (2024) eingegrenzt · § 6.5 „kein Detraining-Vergleichssetting unterhalb der Akademieebene“ und § 12 G8 „die gesamte E5-Evidenz von Akademie- oder Profispielern“ tragen nicht, Liu et al. (2024) untersuchten regionale U19 (Tier 2) · § 6.6 führte Moran et al. mit 2016, zitiert wird die Version of Record 2017 · im Text des Masters stehen bis Task 18 keine Objektplatzhalter, Fassung 16 nahm sie an · im Beispielsatz von § 10 fiel die 10-m-Lichtschranke bei der Abschlusstestung aus, nicht bei der Ausgangstestung.

Weiter gültig:
- Die Auswertung ist abgeschlossen. Zahlenquelle ist allein `02_Befunde\\Kennzahlen_2026-09-25.md` (Rev. 2, § 1.2, § 3, § 11.10).
- Im Manuskript stehen keine Kennungen, die Rückverfolgbarkeit läuft über die Zahlenliste des Endabgleichs (§ 1.2).
- Die Vorgabe gilt: Budgets verbindlich, ohne Anhebung und ohne Gegenfinanzierung, kein Textvorschlag über dem Budget seines Abschnitts (§ 5.2).
- Objekte kommen erst in Task 18 in den Master. Bis dahin stehen im Text keine Platzhalter für sie, den für Tab. 1 setzt Task 18 nach G31 (a) (§ 5.3).
- Die Kennwerte der Stichprobe stehen im Text von 4.2, Tab. 2 führt nur die Ausgangswerte der Zielgrößen (§ 5.3).
- Die Begleitbedingungen verzerren nicht einseitig, 6.2 ist für beide Richtungen vorgemerkt (§ 2, § 12 G2).
- Direkter Einbau nur auf ausdrückliche Anweisung, sonst Textvorschlag im Chat, der Verfasser überträgt oder gibt frei (§ 1.2).

Hinweis zur Nummerierung: Die Abschnittsnummern 4.1 bis 7 sind bis Task 18 Arbeitsnummern, auch in Angaben wie „Kapitel 5 und 6“. „Kapitel 1 bis 5“ zählt die fünf Kapitel nach Endnummern. Endnummern und Zeilenkennungen des Berichtsrasters in § 5.1.

---

""" % dict(GB=de(S_GB, 1), GO=de(S_GO, 1), w41=W['4.1'], w42=W['4.2'], w43=W['4.3'], w44=W['4.4'], w451=W['4.5.1'],
           w452=W['4.5.2'], w46=W['4.6'], w47=W['4.7'], k4o=de(K4O), k4=de(K4), tvw=TV_W, mp=MP, tvpr=TV_PR)
i_rolle = t.index('# 1. ROLLE, ARBEITSUMGEBUNG, DOKUMENTENKARTE')
t = KOPF + t[i_rolle:]
PROTOKOLL.append('Kopf bis „# 1. ROLLE“ ersetzt')

# ------------------------------------------------------------------ § 1.1 Umfang
UMFANG = """### Umfang (neu gefasst 28.09.2026)

**Hartgrenze: 6.350 Wörter Absatztext der Kapitel 1 bis 5 (Arbeitsnummern 1 und 4 bis 7).** Gezählt wird ohne Vorspann, Überschriften, Tabelleninhalte, Beschriftungen, Literaturverzeichnis und Anhang. Word zählt in seiner eigenen Funktion rund 21 Prozent mehr (bei 6.350 etwa %(word)s, Faktor aus Fassung 16, nicht neu gemessen) und steuert das Budget nicht. Budget je Abschnitt in § 5. Vor jeder Textproduktion Zielwortzahl festlegen und am Dokument messen, nie schätzen.

**Seitengrenze: höchstens 33 Seiten einschließlich Literaturverzeichnis** (Verfasser 28.09., 15:14: „Literaturverzeichnis inkludiert. Also ist die Seitengrenze nicht reiner Textanteil.“). Gezählt wird von der Einleitung bis zum Ende des Literaturverzeichnisses, ohne Vorspann und Anhang (Klick K1, 28.09.). Das Muster-Inhaltsverzeichnis des SMK-Leitfadens zeigt die Verzeichnisse römisch paginiert und die Seitenzählung ab der Einleitung (Abb. 1, S. 18, dort als Beispiel eingeführt).

| Ebene | Grenze | Grundlage |
|---|---|---|
| Verfasser | höchstens 33 Seiten, Einleitung bis Ende des Literaturverzeichnisses | Verfasser 28.09., 15:14, Zählweise nach K1 |
| Betreuer | höchstens 37 Textseiten | mündlich |
| Prüfungsordnung § 15 (1) | „Die Bachelorarbeit soll einen Umfang von 30 bis 50 Textseiten nicht überschreiten“ | Wortlaut im SMK-Leitfaden, Abschn. 2.2 |
| Steuerung | 6.350 Wörter Absatztext | § 5.2 |

Von den Obergrenzen gilt die strengste, die des Verfassers. Regel R6 entfällt (Klick K2, 28.09.). Eine sanktionierte Untergrenze nennt die Prüfungsordnung nicht, mit „soll … nicht überschreiten“ nennt sie eine Obergrenze. Den Rahmen „30 bis 50 Textseiten“ unterschreitet der Textteil nach der Seitenrechnung bewusst, als Entscheidung für die kürzere Arbeit (§ 13 Nr. 28 bis 31).

**Herleitung.** Der Vergleichskorpus aus elf publizierten Interventionsstudien umfasst im Absatztext von der Einleitung bis zum Fazit im Mittel 4.127 Wörter (Median 3.995, SD 576). Die Obergrenze liegt bei 5.448 Wörtern (Bouafif et al., 2026), die Untergrenze bei 3.383 (Aloui et al., 2022). Die Korpuswerte bleiben Maßstab. Die Festlegung vom 15.09., die Obergrenze des Korpus sei die eigene Obergrenze der korpusgebundenen Kapitel, ist abgelöst: 6.350 liegt rund %(ueber)s Wörter darüber (§ 13 Nr. 28). Mit der Einleitung ist die Arbeit gebaut wie der Korpus, Theorie und Forschungsstand stehen in der Einleitung. Die Einleitung ist mit 1.500 Wörtern länger als das Korpusmittel von 628, weil sie Zielgrößen, Übergangsperiode und Reifung trägt, die eine Zeitschrift voraussetzen kann. Die Überschreitung der Korpus-Obergrenze liegt in Einleitung und Methodik (Gründe in § 5.2). Die Zweiteilung in einen korpusgebundenen und einen freien Teil entfällt, ebenso die Begründung eines Mindestumfangs über den Rahmen der Prüfungsordnung.

**Seitenrechnung — Modellrechnung, keine Messung.** Quelle ist `03_Skripte\\Seitenmodell_2026-09-28` (.py, .txt, .csv): Dichte am Master vom 26.09. mit LibreOffice gerendert und gemessen, Literaturverzeichnis an einer Probe aus 20 Einträgen im Layout des Masters gemessen, Zahl der Einträge geschätzt. Word und LibreOffice brechen leicht verschieden um.

| Posten | Seiten | Art |
|---|---:|---|
| Einleitung 1.500 Wörter bei %(de)s Wörtern je Seite, Methodik bis Fazit 4.850 bei %(dr)s | %(st)s | Modellrechnung, Dichten gemessen |
| fünf Objekte zu je 0,4 Seiten | %(so)s | Modellrechnung, Annahme, Abbildungen gemessen %(a1)s und %(a2)s, Tabellen nicht gemessen |
| fünf Kapitelenden zu je 0,5 Seiten | %(se)s | Modellrechnung, Erwartungswert |
| **Textteil** | **%(tt)s** | Modellrechnung |
| Literaturverzeichnis, %(nb)d Einträge bei %(js)s je Seite, dazu 0,5 für die letzte Seite | %(sl)s | Modellrechnung, Einträge geschätzt, je Seite gemessen |
| **Einleitung bis Ende des Literaturverzeichnisses (K1)** | **%(gb)s** | Modellrechnung |
| obere Variante mit %(no)d Einträgen | %(go)s | Modellrechnung |
| Schwelle der Tauschregel (K3) | 32 | Festlegung |
| Grenze (Verfasser, 28.09.) | 33 | Festlegung |
| Grenze (Betreuer, mündlich) | 37 | Festlegung |

Die Tabelle ist die Budgetprognose, alle Abschnitte mit vollem Budget. Das Messskript schreibt die Rechnung mit den gemessenen Wörtern und Belegen fort (Block „Seitenschätzung“, für ungeschriebene Abschnitte das Budget), am 28.09. %(mp)s Seiten. Steuernd ist seine jeweils jüngste Prognose (§ 5.3). Der Vorspann zählt nach K1 nicht (im heutigen Master %(vs)d Seiten). Kontrolle ist die Word-Messung am fertigen Dokument, nach Ergebnissen und Diskussion (Arbeitsnummern 5 und 6) und nach dem Literaturverzeichnis (Task 15).

**Kein Auffüllen.** Regel R6 (unter 30 Seiten Anhangsobjekte in den Textteil holen) entfällt (Klick K2, 28.09.). Es bleibt die allgemeine Regel: Fließtext wird nie aufgefüllt, nicht verbrauchte Wörter eines Abschnitts gehen nicht auf andere über (§ 5.2). Der SMK-Leitfaden warnt vor „eine[r] viel zu große[n] Zahl an Seiten mit der Wiedergabe von allgemeinen Grundlagen … Berücksichtigen Sie, dass sich dies u. U. extrem negativ auf die Bewertung Ihrer Arbeit auswirkt“ (Abschn. 4.1).

Beim Betreuer wird zum Umfang nicht nachgefragt.
""" % dict(word=de(WORD, 0), ueber=de(round(UEBER, -2)), de=de(D_E), dr=de(D_R), st=de(S_TEXT, 1), so=de(S_OBJ, 1),
           se=de(S_END, 1), tt=de(S_TT, 1), nb=N_B, js=de(JE_S, 1), sl=de(S_LIT, 1), gb=de(S_GB, 1), no=N_O,
           go=de(S_GO, 1), vs=VORSPANN, a1=A1, a2=A2, mp=MP)
abschnitt('### Umfang (neu gefasst 15.09.2026)', '## 1.2 Arbeitsablauf', UMFANG)

# ------------------------------------------------------------------ § 1.2 Arbeitsablauf
rep("1. `Claude\\02_Befunde\\Berichtsraster_2026-09-23` (Rev. 2) — Einstieg je Abschnitt: Kopfblock mit Budget,",
    "1. `Claude\\02_Befunde\\Berichtsraster_2026-09-23` (Rev. 3) — Einstieg je Abschnitt, für die Einleitung der Kopfblock „Einleitung“: Kopfblock mit Budget,")
rep("9. `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 4) — Reihenfolge, Budgets, Klickfragen, Startsätze, Stand der Tasks.",
    "9. `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 5) — Reihenfolge, Budgets, Klickfragen, Startsätze, Stand der Tasks.\n\n"
    "Für den Rest von Task 7 neu (Abgleich nach der Übertragung, Übergabe Einleitung § 8 Nr. 6) kommen vor allem anderen `Claude\\04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md` (Maßstab des Abgleichs, Vormerkungen § 6 dort) und `Claude\\04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md` hinzu.")
rep("erhalten und danach Anker- und Referenzzahl gegenprüfen.",
    "erhalten und danach Anker- und Referenzzahl gegenprüfen. Rückschreibung je Commit aus einem eigenen, frischen Ausgabepfad mit kurzer Wartezeit, danach neu stagen oder auf dem Rechner lesen und per MD5 gegen die Ausgabe vergleichen. Ein „written“ des Commits allein genügt nicht (Befunde 28.09., Rev. 112 und 114).\n\n"
    "**Uhrzeiten:** Die Uhrzeiten in Teil 0 und in den Steuerdokumenten folgen der Sitzungsuhr (UTC+1). Bis Rev. 112 sind sie mit „MESZ“ beschriftet, in MESZ liegen sie eine Stunde später (Befund 28.09.). Ab Rev. 113 steht „Sitzungsuhr“ dabei, die alten Einträge bleiben, wie sie sind.")

# ------------------------------------------------------------------ § 1.3 Dokumentenkarte
zeile("| `Claude\\02_Befunde\\Berichtsraster_2026-09-23` (Rev. 2) |",
      "| `Claude\\02_Befunde\\Berichtsraster_2026-09-23` (Rev. 3) | **Einstieg je Abschnitt (Ebene Inhalt).** Berichtspflichten je Abschnitt mit Etiketten P, P°, K, E, Kopfblock „Einleitung“ (Zeilen 1.1 bis 1.6, 2.1 bis 2.5, 3.1 bis 3.5, E.1, E.2), Konflikte, Fehlerliste des Masters, Prüfliste |")
zeile("| `Claude\\01_Verfahren\\Gliederung_2026-09-23` (v4, Rev. 2) |",
      "| `Claude\\01_Verfahren\\Gliederung_2026-09-28` (v5) | Gliederung mit fünf Kapiteln, Arbeits- und Endnummern, Wortbudget und Seitenmodell, Objektzuordnung, Änderungen Ä12 und Ä13 gegenüber v4, Änderungsliste für den Master (M24, M25), Herkunft mit den Errata E1 bis E5 zu v4 |")
zeile("| `Claude\\03_Skripte\\Manuskriptstand_2026-09-25` (.py, .txt, .csv) |",
      "| `Claude\\03_Skripte\\Manuskriptstand_2026-09-25` (.py, .txt, .csv) | Messung des Masters je Abschnitt (Wörter, Semikola, Verweise, Platzhalter, Satzlängen), Fassung 3 vom 28.09.: Einleitung mit dem Altbestand 2, 2.x und 3, Summen gegen 6.350, Arbeits- und Endnummern, Block „Seitenschätzung“ als Modellrechnung |\n"
      "| `Claude\\03_Skripte\\Seitenmodell_2026-09-28` (.py, .txt, .csv) | **Seitenrechnung** (Modellrechnung): Dichte am Master, Probe des Literaturverzeichnisses, Zahl der Einträge, Parameter für das Messskript (§ 1.1) |")
zeile("| `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 4) |",
      "| `Claude\\04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md` (Rev. 5) | **Reihenfolge der Arbeit:** Tasks in fünf Blöcken, Budgets als Vorgabe, Klickfragen, Startsätze, Stand der Tasks. Tasks 1 bis 6 und 1b erledigt, Task 7 neu mit Textvorschlag (Übertragung und Abgleich offen), danach Task 11, Task 14 entfällt |")
rep("**Vormerkungen für die Tasks 7 bis 18** (je § „Vormerkungen“ oder „Offen“).",
    "**Vormerkungen für die Tasks 7 neu bis 18** (je § „Vormerkungen“ oder „Offen“), Vormerkungen zu 2.x gehen an Task 7 neu.")
zeile("| `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-25.md` |",
      "| `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` | Prompt des Tasks Steuerdokumente 28.09. (Task 1b des Plans, Fassung 17 und Folgeänderungen), nach Erledigung ins Archiv |\n"
      "| `Claude\\04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md` | **Eingang von Task 7 neu (Einleitung):** Bauplan in acht Zügen, Pflichtinhalte, Verbleibsliste, Regeln, Startsatz § 0. Durch den Textvorschlag weitgehend verbraucht, offen ist § 8 Nr. 6 (Abgleich nach der Übertragung) |\n"
      "| `Claude\\04_Uebergaben\\Textvorschlag_Einleitung_2026-09-28.md` | **Einleitung (Task 7 neu, Rev. 114):** Wortlaut in neun Absätzen, Zug-Tabelle, Belegtabelle mit Wortlaut und Seite, Verbleibsliste mit den Klicks, Zweitprüfung, Vormerkungen für T1, T4, Maßnahmenliste und die Tasks 12 und 13 (§ 6 dort). Maßstab des Abgleichs nach der Übertragung |\n"
      "| `Claude\\04_Uebergaben\\Textvorschlag_2.4_2026-09-28_Fassung6.md` | Zielgrößenteil, nicht übertragen (§ 13 Nr. 28). Material für Zug 2 der Einleitung, Zitationsbefunde § 6, Klicks § 7 |\n"
      "| `Claude\\02_Befunde\\Argumentation_Relevanz_Breitensport_2026-09-28` (Rev. 2, .md, .docx, .pdf) | Relevanz- und Präventionsstrang: Gesamtbild, Grenzen des Präventionssatzes, ausgeschlossene Schlüsse (§ 4), Neuzuschnitt (§ 8). Eingang von Task 7 neu. Rev. 1 im Archiv |\n"
      "| `Claude\\02_Befunde\\Vorarbeit_2.4_Zielgroessen_2026-09-27` (.md, .docx, .pdf) mit `Literaturraster_2.4_2026-09-27.csv` | Literaturanalyse zu Zielgrößen und Diagnostik mit den Einleitungskarten des Korpus (57 Studien), Raster `01_Verfahren\\Literaturraster_Kapitel2_2026-09-27.md`, Zählwerkzeug `03_Skripte\\Literaturraster_Zaehlwerkzeug_2026-09-27.py`. Quellenpool für Zug 2 der Einleitung (§ 6.5) |")
zeile("| `Claude\\04_Uebergaben\\Textvorschlag_4.7_2026-09-25.md` |",
      "| `Claude\\04_Uebergaben\\Textvorschlag_4.7_2026-09-26.md` | Wortlaut von 4.7 im Master (Fassung 13 mit Nachtrag Schritt 0 in § 10), Zug- und Satzorte (§ 3), Vormerkungen für die Tasks 7 neu bis 18 (§ 7), Befunde B8, B11 und B15 (§ 6) |")
rep("| Manuskript-Master. Einziger Ort für Manuskripttext (Gliederung v4, § 5) |",
    "| Manuskript-Master. Einziger Ort für Manuskripttext (Gliederung v5, § 5) |")
rep("T1 Steckbriefe (67)", "T1 Steckbriefe (%d)" % N_T1)
rep("T4 Zitierfallen (131)", "T4 Zitierfallen (%d)" % N_T4)
rep("| Aufnahme- und Ausschlussliste je Kapitel |",
    "| Aufnahme- und Ausschlussliste je Kapitel, Zuordnung nach Gliederung v3. Für die Einleitung gilt deren Verbleibsliste (Übergabe Einleitung § 5) |")
rep("| `Claude\\04_Uebergaben\\Uebergabe_Textrevision_2026-09-12.md` | Rahmenplan der Textrevision mit Nachträgen |\n", "")
rep("| Kommentare zu Kapitel 2 (Tasks 7 bis 10), Suchprotokoll, Titelscreening, Prüfprotokoll der Gliederung v4 mit den Errata (§ 5.1) |",
    "| Kommentare zum Altbestand Kapitel 2 (für Task 7 neu nur bei Bedarf), Suchprotokoll, Titelscreening, Prüfprotokoll der Gliederung v4 mit den Errata (Gliederung v5, Herkunft) |")
rep("· `Projektanweisungen_*` · `S14_*_Python.png` | Sitzungs- und Werkzeugskripte: Fortschreibung der Steuerung, Einbau in den Master, Messungen, Registernachträge, Korpusmessungen, Erzeugung und Vergleich der Projektanweisungen, Diagramme der Python-Gegenprobe.",
    "· `Projektanweisungen_*` · `S14_*_Python.png` · `Plan_*` · `Steuerdokumente_*` · `Textvorschlag_*` · `Herkunft_*` · `Verbleib_*` · `Optionale_Stufen_*` · `Satzersetzungen_*` · `Wortlaut_*` · `Pruefung_Standardweg_*` · `Literaturraster_*` · `Gliederung_*` · `Berichtsraster_*` · `Seitenmodell_*` · `T4_Nachtrag_*` | Sitzungs- und Werkzeugskripte: Fortschreibung der Steuerung, Einbau in den Master, Messungen, Registernachträge, Korpusmessungen, Erzeugung und Vergleich der Projektanweisungen und der übrigen Steuerdokumente, Textvorschläge mit ihren Läufen und Stufen, Literaturraster, Diagramme der Python-Gegenprobe.")
zeile("**Nachtragsvermerke** (Maßnahme I19,",
      "**Nachtragsvermerke** (Maßnahmen I19 und G32 j, jeweils mit der nächsten Revision des Dokuments, keine eigene Fassung): "
      "Auswertungsverfahren — 7.3: die Kennung steht nicht neben der Zahl im Manuskript, Rückverfolgbarkeit über die Zahlenliste des Endabgleichs · Grundsatz 3, 8.1 und 8.3: Ort der Einschränkung ohne unabhängige Methodenprüfung ist 6.3, Anhang G ohne Prüfprotokolle (Wortlaut vorher prüfen) · "
      "Umfangsdokument — § 3.2: Tab. 2 ohne die Kennwerte der Stichprobe, diese stehen in 4.2 · § 3.5: Tab. H4 mit Erstverweis in 4.7, Tab. H5 in 5.1 statt 4.7 · Zeile zu 4.7.13: in 4.7 nur die Datenprüfung (Textvorschlag 4.7, Nr. 57) · R5 nach der Entscheidung zu Nr. 23 in Task 11 · § 3.6 und R6: Seitenprognose nach § 1.1, R6 entfällt · "
      "Auswertungsplan — § 5.2 A3 und § 6 Nr. 2: Familienfehler „höchstens 7,5 %“ statt „bis 14 %“ · § 5.3 und Register des Endabgleichs: „vor Kenntnis der KG-Werte“ als Kurzform für „vor der Abschlusstestung der KG“ kennzeichnen (B8) · § 5.10: Berichtsort bei R1, R9, R10, R12 und R13 nicht mehr 4.7 · § 6 Nr. 3: „über Studien vergleichbar“ einschränken (Nr. 44) · Register R3 um den Befund B11 (Richtung des Standardwegs am Datensatz gestützt, `03_Skripte\\Pruefung_Standardweg_2026-09-26.py`) · "
      "Kennzahlenblatt, Kopf — der Satz „Jede Zahl im Manuskript trägt eine Kennung“ wird beim nächsten Lauf des Erzeugers auf die Regel aus § 1.2 Nr. 3 umgestellt, ebenso „Tab. 2 oben (K-02)“, die Kennwerte stehen in 4.2. Bis dahin gilt die Regel dieser Fassung · "
      "Bauplan § 7.1 — Kapitel 2 und 3 entfallen, die Einleitung trägt Theorie und Forschungsstand wie im Korpus. "
      "Erledigt mit Fassung 17: Berichtsraster 4.2.5 und 3.11 (Rev. 3), Messskript (Fassung 3). Entfallen ist der Vermerk „Berichtsraster Zeile 4.7.13 — Anhang G ist der Ort der Prüfprotokolle“, überholt durch die Entscheidung vom 26.09. (Anhang G ohne Prüfprotokolle, § 13 Nr. 23).")
rep("gemeint sind vier Studien ohne Fazitkapitel (Lloyd, Hammami, Beato, Padrón-Cabo), nicht „vier weder noch“ (G27b, Korrektur mit der nächsten Bauplan-Revision).",
    "gemeint sind vier Studien ohne Fazitkapitel (Lloyd, Hammami, Beato, Padrón-Cabo), nicht „vier weder noch“ (G27b, Korrektur mit der nächsten Bauplan-Revision) · `Argumentation_Relevanz_Breitensport_2026-09-28` § 6 Nr. 6 und § 7 nennen eine Übergabe zu 2.4 Fassung 7, die nie abgelegt wurde (ersetzt durch die Übergabe Einleitung).")
rep("Projektanweisungen vor Fassung 16 (Fassung 15 wurde nicht eingesetzt, Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung15`)",
    "Projektanweisungen vor Fassung 17 (Fassung 16 bleibt bis zum Einsetzen von Fassung 17 Sicherung der wirksamen Fassung, danach Kopie in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`, Fassung 15 wurde nie eingesetzt, Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung15`)")
rep("`Projektanweisungen_Fassung14` (Sicherung der wirksamen Fassung bis zum Einsetzen von F16, dann Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14`)",
    "`Projektanweisungen_Fassung14` (Kopie in `_Archiv\\_ersetzt_2026-09-25_Fassung14`)")
rep("Rev. 1 des Plans der weiteren Schritte. `01_Verfahren\\Tabellen_Spezifikation_v1.md` bleibt Arbeitsmittel",
    "Rev. 1 des Plans der weiteren Schritte · Gliederung v4 `Gliederung_2026-09-23` (.md, .docx, .pdf), Berichtsraster Rev. 2, Plan Rev. 4 und `Manuskriptstand_2026-09-25.py` Fassung 2 (Kopien in `_Archiv\\_ersetzt_2026-09-28_Steuerdokumente`) · `Uebergabe_Kapitel2_2026-09-26.md` (ersetzt durch die Übergabe Einleitung) · `Uebergabe_2.4_Fassung6_2026-09-28.md` (gegenstandslos) · `Textvorschlag_2.4_2026-09-26.md`, `Textvorschlag_2.4_2026-09-27.md` und `Textvorschlag_2.4_2026-09-27_Fassung5.md` (überholt) · `Uebergabe_Steuerdokumente_2026-09-25.md` (erledigt) · `Textvorschlag_4.7_2026-09-25.md` mit den Textstufen `_A`, `_Empf`, `_Kurz` (ersetzt durch den Textvorschlag vom 26.09.) · `Uebergabe_Textrevision_2026-09-12.md` (Kapitel 4 fertig, Kapitel 2 entfällt) · Befund Relevanz Rev. 1 (`_Archiv\\_ersetzt_2026-09-28_Relevanz_Rev1`) · die Übergabe zu 2.4 Fassung 7 (nie abgelegt). Kopien der Übergaben in `_Archiv\\_ersetzt_2026-09-28_Uebergaben`, die Originale entfernt `Ordner_aufraeumen.ps1`. `01_Verfahren\\Tabellen_Spezifikation_v1.md` bleibt Arbeitsmittel")

# ------------------------------------------------------------------ § 1.5 Leitregel
rep("Hedges' g · Hypothesen im Antragswortlaut, keine primäre Zielgröße ·",
    "Hedges' g · Hypothesen nah am Antragswortlaut, H0 und H1 einander ergänzend (G32 e), keine primäre Zielgröße ·")
rep("Eine unabhängige Methodenprüfung fand nicht statt. Das steht in 4.7 als Einschränkung (Auswertungsverfahren 8.1).",
    "Eine unabhängige Methodenprüfung fand nicht statt. Sie ist genau einmal für 6.3 als Einschränkung vorgemerkt (G3 oder G7, Verfasser 26.09., Textvorschlag 4.7, Nr. 57, Auswertungsverfahren 8.1 wird nachgetragen, § 1.3).")

# ------------------------------------------------------------------ § 2 Studiensteckbrief
rep("keine Akademiespieler. Vergleichsevidenz überwiegend Tier 3+ |",
    "keine Akademiespieler. Die Metaanalyse von Oliver et al. (2024) schloss nur Spieler ab Tier 3 nach McKay et al. (2022) ein, bei fehlender Angabe der Wettkampfebene nach dem Trainingsumfang europäischer Spitzenakademien (U13 bis U15 zehn Stunden je Woche, S. 625). Tier 3 umfasst dort auch Spieler aus „national or state (regional) level leagues“ (S. 625). 4.2 ordnet die Stichprobe nach Wettkampfebene und Vereinsbindung Tier 2 zu. Ob das gegen dieses Kriterium trägt, hängt an der Spielklasse der drei Mannschaften, vorgemerkt für den Abgleich der Einleitung (G35). Liu et al. (2024) ordnen regionale U19 selbst Tier 2 zu („trained/developmental“, S. 220) |")
rep("Das Erratum steht nur in Anhang G und im Register R14, nicht im Fließtext (Verfasser 25.09.) |",
    "Das Erratum ist nur für Anhang G vorgemerkt und steht im Register R14, nicht im Fließtext (Verfasser 25.09.) |")

# ------------------------------------------------------------------ § 4 Berichtsstandards
rep("Übernommen ist daraus nur der Satz zur Analyseeinheit in 4.7: Zuteilung auf Vereinsebene, Analyse auf Spielerebene, drei Cluster ohne Varianzkomponente.",
    "Übernommen ist daraus nur der Satz zur Analyseeinheit: Zuteilung auf Vereinsebene, Analyse auf Spielerebene, drei Cluster ohne Varianzkomponente. Er ist für 6.2 vorgemerkt (Textvorschlag 4.7, Nr. 4), 4.7 enthält ihn nicht mehr.")

# ------------------------------------------------------------------ § 5.1 Gliederung v5
G51 = """## 5.1 Gliederung (v5, 28.09.2026)

Die Gliederung v5 (`01_Verfahren\\Gliederung_2026-09-28`) gilt als revidierbare Arbeitsfestlegung. Sie ersetzt v4 nach dem Neuzuschnitt vom 28.09. (Verfasser 14:38, Klick 14:57): Kapitel 1 bis 3 werden eine Einleitung ohne Unterabschnitte.

**Vorspann:** Titelblatt · Eidesstattliche Erklärung mit KI-Deklaration (Platzhalter) · Zusammenfassung · Abstract (ohne Struktur-Label) · Verzeichnisse

1. **Einleitung** — ohne Unterabschnitte, höchstens 1.500 Wörter, Trichter in acht Zügen (§ 5a), endet mit den Hypothesen nah am Wortlaut des Ethikantrags (H0/H1 „in mindestens einem der erhobenen Parameter“, einander ergänzend, G32 e), keine primäre Zielgröße
2. **Methodik** (Arbeitsnummer 4) — 4.1 Studiendesign · 4.2 Stichprobe · 4.3 Untersuchungsablauf · 4.4 Leistungsdiagnostik · 4.5 Trainingsintervention (4.5.1, 4.5.2) · 4.6 Adhärenz- und Belastungsmonitoring · 4.7 Statistische Auswertung
3. **Ergebnisse** (Arbeitsnummer 5) — 5.1 Teilnehmerfluss, Adhärenz und Ausgangswerte · 5.2 Gruppenvergleiche je Zielgröße. Keine Interpretation
4. **Diskussion** (Arbeitsnummer 6) — 6.1 Einordnung der Ergebnisse · 6.2 Methodendiskussion · 6.3 Stärken und Limitationen
5. **Fazit und Ausblick** (Arbeitsnummer 7) — ein Absatz, mit den praktischen Implikationen, ohne Unterabschnitte

**Nachspann:** Literaturverzeichnis · Anhang A Fragebogen A · B Übungs- und Videoübersicht · C Aufwärmprogramm der Testtage · D Vereins-Sommerprogramme · E Ethikvotum und Ethikantrag · F Einverständniserklärung und Elternhöhen · G Sensitivitäts-Poweranalyse und R-Skripte, ohne Prüfprotokolle · H Ergänzende Tabellen H1 bis H6 und Abb. H7. Kein Rohdatenanhang, der pseudonymisierte Datenstand wird auf Anfrage bereitgestellt.

**Arbeits- und Endnummern.** Bis Task 18 behalten Methodik bis Fazit im Master und in allen Steuerdokumenten, Skripten und Textvorschlägen ihre Arbeitsnummern. Die Umnummerierung geschieht einmal per Skript in Task 18 (G35 d), danach aktualisiert der Verfasser die Verzeichnisse mit F9. Die Zeilenkennungen des Berichtsrasters für die Einleitung (1.1 bis 1.6, 2.1 bis 2.5, 3.1 bis 3.5, E.1, E.2) sind keine Abschnittsnummern. Sie werden in Task 18 mit umbenannt, damit sie nicht mit den Endnummern 2.1 bis 2.7 der Methodik verwechselt werden.

| Arbeitsnummer | Endnummer |
|---|---|
| 1 Einleitung | 1 |
| 4, 4.1 bis 4.7 (mit 4.4.1 bis 4.4.3, 4.5.1, 4.5.2) | 2, 2.1 bis 2.7 (mit 2.4.1 bis 2.4.3, 2.5.1, 2.5.2) |
| 5, 5.1, 5.2 | 3, 3.1, 3.2 |
| 6, 6.1 bis 6.3 | 4, 4.1 bis 4.3 |
| 7 | 5 |

**Reihenfolgetreue:** Sprint → Richtungswechsel → Sprung in den Hypothesen, den Ergebnissen und der Diskussion identisch.

Die Errata E1 bis E5 zur Gliederung v4 (Prüfprotokoll `05_Protokolle\\Pruefprotokoll_Gliederung_2026-09-23` § 2) stehen in der Gliederung v5, Abschnitt Herkunft.
"""
abschnitt('## 5.1 Gliederung (v4, Klickantworten 23.09.2026)', '## 5.2 Wortbudget', G51)

# ------------------------------------------------------------------ § 5.2 Wortbudget
G52 = """## 5.2 Wortbudget (verbindlich, neu gefasst 28.09.2026)

| Kapitel (Arbeitsnummer) | Korpus Ø | Budget | Grund |
|---|---:|---:|---|
| 1 Einleitung (1) | 628 | **1.500** | trägt Theorie, Forschungsstand und Hypothesen (Verfasser 28.09.). Länger als im Korpus, weil Zielgrößen, Übergangsperiode und Reifung dort vorausgesetzt werden |
| 2 Methodik (4) | 1.764 | **2.550** | wie bisher: CONSORT 3b, TIDieR mit zwölf Items, drei Begleitbedingungen, Versuchsausfälle, Posten, die der Korpus nicht kennt |
| 3 Ergebnisse (5) | 336 | **450** | wie bisher: drei konfirmatorische Zielgrößen plus Fluss, Adhärenz, Ausgangswerte |
| 4 Diskussion (6) | 1.416 | **1.600** | wie bisher: auf Korpusniveau, acht Limitationsgruppen statt 27 Einzelpunkte (§ 12) |
| 5 Fazit und Ausblick (7) | 208 | **250** | wie bisher: ein Absatz, wie im Korpus |
| **Σ** | **4.352** | **6.350** | |

**Unterbudgets (Vorgabe):** 4.1 300 · 4.2 215 · 4.3 340 · 4.4 420 · 4.5.1 420 · 4.5.2 150 · 4.6 155 (Summe 4.1 bis 4.6 = 2.000) · 4.7 550 · 5.1 230 · 5.2 220 · 6.1 700 · 6.2 400 · 6.3 500 · 7 250. Die Einleitung hat kein Unterbudget.

**Stand am Master (Messung 28.09., `03_Skripte\\Manuskriptstand_2026-09-25.txt`, Skript Fassung 3):** 4.1 %(w41)s · 4.2 %(w42)s · 4.3 %(w43)s · 4.4 mit 4.4.1 bis 4.4.3 %(w44)s · 4.5.1 %(w451)s · 4.5.2 %(w452)s · 4.6 %(w46)s · 4.7 %(w47)s · Kapitel 4 (4.1 bis 4.6) %(k4o)s gegen 2.000, mit 4.7 %(k4)s gegen 2.550 · Einleitung noch Altbestand: Kapitel 2 und 3 stehen mit %(alt)s Wörtern im Master, dort liegen alle %(semi)d Semikola und %(verw)d Abschnittsverweise · Absatztext mit Altbestand %(ges)s. Der Altbestand wird nicht gekürzt, sondern durch die Einleitung ersetzt. Der Textvorschlag Einleitung misst %(tvw)s Wörter und ersetzt nach der Übertragung den Altbestand mit allen Semikola und Verweisen (Task 7 neu, Rev. 114).

### Was das bedeutet

Kapitel 4 ist textlich fertig. Kapitel 2 (2.1 bis 2.4) wird nicht mehr gekürzt, sondern durch die Einleitung ersetzt, deren Textvorschlag vorliegt. Zu schreiben sind noch Kapitel 5 bis 7 (Arbeitsnummern) mit zusammen %(rest)s Wörtern Budget. Die Vorgabe gilt unverändert: keine Anhebung, keine Gegenfinanzierung, kein Textvorschlag über dem Budget seines Abschnitts. Nicht verbrauchte Wörter eines Abschnitts gehen nicht auf andere über. Reihenfolge nach Plan Rev. 5: Übertragung und Abgleich der Einleitung (Task 7 neu) → Kapitel 5, 6 und 7 mit Zusammenfassung und Abstract → Literaturverzeichnis, Phase 8, Anhänge A bis F, Endredaktion.

**Nicht im Budget und gesondert zu führen:** deutsche Zusammenfassung und englisches Abstract (je 200–300 Wörter, Vorspann), Anhang, Tabelleninhalte, Beschriftungen.
""" % dict(w41=W['4.1'], w42=W['4.2'], w43=W['4.3'], w44=W['4.4'], w451=W['4.5.1'], w452=W['4.5.2'], w46=W['4.6'],
           w47=W['4.7'], k4o=de(K4O), k4=de(K4), alt=de(ALT), semi=SEMI_N, verw=VERW_N, ges=de(GES), tvw=TV_W,
           rest=de(REST))
abschnitt('## 5.2 Wortbudget (verbindlich seit 15.09.2026)', '## 5.3 Objektpolitik', G52)

# ------------------------------------------------------------------ § 5.3 Objektpolitik
zeile("**Tauschregel (neu F14):**",
      "**Tauschregel (neu gefasst 28.09.):** Ein Objekt kostet im Layout nach Annahme rund 0,4 Seiten, also rund 130 Wörter Fließtext (Seitenmodell: Abb. 1 %s, Abb. 2 %s des Satzspiegels, Tabellen nicht gemessen). Die fünf Objekte des Textteils stehen fest (Verfasser 24.09., R7), tragen die CONSORT-Pflichten und kosten keine Wörter. Die Tauschregel betrifft nur Objekte über die fünf hinaus: Ihre Wortkosten werden angesetzt, sobald die Seitenprognose 32 Seiten erreicht (Klick K3, 28.09.). Maßgeblich ist die jüngste Prognose des Messskripts (Block „Seitenschätzung“, am 28.09. %s Seiten), die Budgetprognose des Seitenmodells liegt bei %s (§ 1.1). Kontrolle ist die Word-Messung nach Ergebnissen und Diskussion (Arbeitsnummern 5 und 6) und nach dem Literaturverzeichnis (Task 15)." % (A1, A2, MP, de(S_GB, 1)))
rep("**Im Textteil stehen fünf Objekte** (Verfasser 24.09.). Bis Task 18 stehen im Master nur Platzhalter, eingesetzt wird, wenn der Text steht (Verfasser 25.09., 22:25):",
    "**Im Textteil stehen fünf Objekte** (Verfasser 24.09.). Eingesetzt werden sie in Task 18, wenn der Text steht (Verfasser 25.09., 22:25). Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter, den für Tab. 1 setzt Task 18 nach G31 (a). Platzhalter stehen nur für die Anhangsobjekte in Anhang H. Die fünf Objekte:")
rep("· 20-m-Verzicht und Beindominanz → 4.4 ·",
    "· Beindominanz → 4.4.2 · 20-m-Verzicht → Tab. H6 und 6.3 G7 (der Satz in 4.4 entfällt, § 13 Nr. 15) ·")
rep("· ANCOVA-Spezifikation, Voraussetzungen mit Regel O7, 505-Regel, Analysepopulation, Aggregationsregel, Mindestdosis mit Datum, Daten- und Rechenprüfung → 4.7 · Poweranalyse und R-Skripte → Anhang G ·",
    "· Aggregationsregel → 4.4 und 505-Regel → 4.4.2 (Testkette, § 5a) · ANCOVA-Spezifikation, Voraussetzungen mit Regel O7, Analysepopulation, Mindestdosis und Datenprüfung → 4.7, das Datum jeder Festlegung vorgemerkt für Tab. H6 · Poweranalyse und R-Skripte → Anhang G, ohne Prüfprotokolle ·")

# ------------------------------------------------------------------ § 5a Bauplan
rep("Der Bauplan ist zu **skalieren, nicht zu kopieren** – die eigene Arbeit ist bei 9.000 Wörtern das 2,2-Fache des Korpusmittels, verteilt auf mehr Kapitel.",
    "Der Bauplan ist zu **skalieren, nicht zu kopieren** – die eigene Arbeit ist bei 6.350 Wörtern das %s-Fache des Korpusmittels (6.350 zu 4.127)." % de(FAKTOR, 1))
EINL = """## Einleitung — Trichter in acht Zügen

Bauplan nach `04_Uebergaben\\Uebergabe_Einleitung_2026-09-28.md` § 3, umgesetzt im Textvorschlag Einleitung (Zug-Tabelle § 2 dort, jede Abweichung mit Grund). Die Satzkerne sind Inhalt, kein Wortlaut.

1. **Relevanz** — generalisierende Präsensaussage über Sportart und Zielgrößen, Beleg am Satzende. Nie Quelle als Subjekt, nie Selbstbezug. Die Machbarkeit steht im Textvorschlag bei Zug 4, weil sie das Trainingsmittel begründet.
2. **Zielgrößen und Diagnostik** — aus den physiologischen Anforderungen des Wettkampfs die Zielgrößen und ihre Diagnostik ableiten. Kein Testablauf, der steht in 4.3 und 4.4 (Verfasser 28.09., 10:30). Dazu der Richtungswechsel als Aktion, die mit Verletzungen verbunden ist (Klick in Task 7 neu).
3. **Sommerpause und Detraining** — Zeitfenster, kein sicherer Verlust, bei Heranwachsenden ist die Richtung offen.
4. **Plyometrisches Training** — Dehnungs-Verkürzungs-Zyklus, Steuergrößen, gerätefrei und heimtauglich (Machbarkeit), dazu die Präventionssätze (§ 6.5, geplant rund 45 Wörter, im Textvorschlag %(pr)s, weil der Vor-2020-Halbsatz zu Rössler et al., 2014, einen eigenen Satz braucht).
5. **Reifung** — Moderator der Trainingsantwort, Richtung uneinheitlich. Die Reifemethode entfällt hier, sie ist für 6.2 vorgemerkt (Klick in Task 7 neu).
6. **Forschungsstand** — qualitativ, mit Gegenbefund (kurze Beschleunigung als Vorab-Erwartung für 5 und 10 m).
7. **Lücke** — kontrollierte Studien zu einem unbeaufsichtigten, videobasierten, gerätefreien Heimprogramm in der Sommerpause für Spieler des leistungsorientierten Breitensports um den Wachstumsgipfel fehlen. Tragend ist die Kombination, nicht das Leistungsniveau allein (§ 6.5).
8. **Zweck, Vorgehen, Hypothesen** — Zweck in einem Satz als Ankersatz, ein Satz zum Vorgehen ohne Kapitelverweis, H0 und H1 nah am Wortlaut des Ethikantrags und einander ergänzend, drei Zielgrößen gleichrangig, Reihenfolge Sprint → Richtungswechsel → Sprung.

Aus dem Korpus bleibt: Eröffnung als generalisierende Präsensaussage, Schluss mit den Hypothesen (8 von 11 Studien), nie mit einem Literaturverweis. Der Zweck ist der Ankersatz. Er kehrt im ersten Absatz der Diskussion (6.1) und in der Zusammenfassung nahezu wörtlich wieder, 4.1 bleibt ohne Zwecksatz (Klick K6, 28.09.). Sein Wortlaut ist entschieden: „… gegenüber einer Kontrollgruppe verbessert“ statt „erhält oder verbessert“ (Klick in Task 7 neu, Textvorschlag Einleitung § 7, § 13 Nr. 37). Keine eigenen Studienzahlen in der Einleitung.
""" % dict(pr=TV_PR)
abschnitt('## Kapitel 1 — Einleitung: Trichter aus sechs Zügen', '## Kapitel 4 — Methodik', EINL)
rep("**Statistikabsatz (4.7):** Darstellungskonvention → Verteilungsprüfung → Hauptverfahren → Post-hoc → Effektstärke mit Schwellen → Reliabilität → α → Software mit Version.",
    "**Statistikabsatz (4.7):** Korpusfolge Darstellungskonvention → Verteilungsprüfung → Hauptverfahren → Post-hoc → Effektstärke mit Schwellen → Reliabilität → α → Software mit Version. 4.7 im Master weicht bewusst ab (Textvorschlag 4.7): keine Darstellungskonvention im Text (K-Zeile, sie steht in den Tabellenanmerkungen, § 3 dort, Zeile 4.7.1) · Voraussetzungen nach dem Modell, weil sie an dessen Residuen ansetzen (Nr. 54) · kein Post-hoc bei zwei Gruppen · Effektstärke ohne Schwellen, eingeordnet über das Konfidenzintervall gegen null und den SESOI (§ 11.2b) · Reliabilität in 4.4 (Tab. 1) · α als Eingabe der Poweranalyse, das Testniveau in der Entscheidungsregel (Nr. 10) · Software vor dem Anhangsverweis, nicht als letztes Wort (Nr. 57, § 13 Nr. 23).")
rep("3. **Zahlen stehen in den Objekten.** Der Fließtext nennt Teststatistik, Richtung und Größenklasse.",
    "3. **Zahlen stehen in den Objekten.** Der Fließtext nennt Teststatistik, Richtung und den Fall der Schlusslogik (§ 11.2b), keine Cohen-Klasse (Textvorschlag 4.7 § 7, Zeile Task 11).")
rep("**Erster Absatz, in 11 von 11 Studien identisch:** Zweck wiederholen → Hauptbefund → Gegenbefund.",
    "**Erster Absatz, in 11 von 11 Studien identisch:** Zweck wiederholen (Ankersatz aus der Einleitung) → Hauptbefund → Gegenbefund.")
rep("gedeckt durch CONSORT und die Gliederung v4, nicht durch den Korpus.",
    "gedeckt durch CONSORT und die Gliederung v5, nicht durch den Korpus.")

# ------------------------------------------------------------------ § 6.2 Aktualität
rep("Jede Quelle vor 2020 wird beim ersten Auftreten in einem Halbsatz begründet.",
    "Eine Quelle vor 2020 wird beim ersten Auftreten in einem Halbsatz begründet, wenn sie Wirksamkeitsevidenz trägt, etwa „eine ältere Metaanalyse“ (Klick 28.09., 17:54, umgesetzt im Textvorschlag Einleitung bei Rössler et al., 2014, Moran et al., 2017, und Lloyd et al., 2016). Definitions-, Konzept-, Verfahrens- und Diagnostikquellen dürfen nach der Tabelle älter sein und brauchen ihn nicht. Sheppard & Young (2006) behalten als maßgebliche Begriffsklärung ihren Halbsatz (Klick zu 2.4 Fassung 6, Rev. 111).")

# ------------------------------------------------------------------ § 6.4 Rollentrennung
zeile("**Rollentrennung:**",
      "**Rollentrennung:** Einleitung: Zielgrößen und Diagnostik ohne eigenen Testaufbau · Übergangsperiode als Kontext · Mechanismus ohne Effektstärken · Reifung als Moderator · Forschungsstand qualitativ mit Gegenbefund, Effektstärken nicht Pflicht · Hypothesen ohne neue Quellen · Kapitel 6 Einordnung mit Effektstärken und Vorstudienvergleich.")

# ------------------------------------------------------------------ § 6.5 Literatur
rep("Mirwald et al. (2002) wird in 2.2 als verbreitete, kritisierte Alternative erwähnt – das begründet die Khamis-Roche-Wahl.",
    "Mirwald et al. (2002) entfällt mit der Reifemethode aus der Einleitung und fällt vorerst aus dem Literaturverzeichnis, die Methodenwahl ist für 6.2 vorgemerkt, 4.3 nennt das Verfahren (Klick in Task 7 neu, Textvorschlag Einleitung § 4).")
rep("Nimphius et al. (2016, S. 4, 7)", "Nimphius et al. (2016, S. 3027 und 3030, gedruckte Seiten, G33 c)")
rep("Im Manuskript 2.4.2/4.4.2 „zitiert nach", "Im Manuskript 4.4.2 „zitiert nach")
zeile("**Korpus 2.3 (E5), verifiziert:**",
      "**Zug 3 der Einleitung (E5), im Textvorschlag verwendet:** Silva et al. (2016) · Mujika & Padilla (2000), Volltext im Ordner, nicht mehr „zitiert nach Silva“ · Dambel et al. (2025) · Asimakidis et al. (2022, T1 `Manou2022`) · Liu et al. (2024). Entfallen für die Einleitung: Walker & Hawkins (2018) · Clemente et al. (2022), nicht im Ordner, für 6.1 nur nach Ablage (H6). Padrón-Cabo et al. (2025) bleibt Vergleichsstudie des Korpus (Textvorschlag Einleitung § 4 und § 6 Nr. 3).")
zeile("**Korpus 2.4:**",
      "**Quellenpool Zug 2 der Einleitung** nach der Vorarbeit Zielgrößen (`02_Befunde\\Vorarbeit_2.4_Zielgroessen_2026-09-27`): Übersichtsarbeiten, Primärstudien nur für 4.4 und 6.2 (G33 c). Nimphius et al. (2016) · Havanecz et al. (2026) · Ferguson et al. (2024) · Dugdale et al. (2019, 2020) dienen 4.4 und 6.2.\n\n"
      "**Relevanz und Prävention (Befund Relevanz Rev. 2, Klick 14:36):** Olivier et al. (2026) ist Kernquelle, mit Quellenart und Population im Satz, ohne Zahl · Rössler et al. (2014) nur für den Sprungbefund, als Zwischen-Studien-Vergleich, Population „überwiegend Spielerinnen“ im Satz, Vor-2020-Halbsatz, T4 `Roessler2014` vor der Zitation lesen · Hilska et al. (2021) nur Adhärenzreferenz, vorgemerkt für 6.3 · Faude et al. (2017) Reserve. Price et al. (2004) nicht für den Anstieg der Verletzungen nach Pausen (ohne Expositionszeit), im Übrigen entscheidet die Verbleibsliste der Einleitung.\n\n"
      "**Belege zu den Zielgrößen (Klicks 28.09. zu 2.4 Fassung 6):** Hicks et al. (2020) mit dem Jahr 2020, Version of Record SCJ 42(2), 45–62. Das PDF im Ordner ist die Ahead-of-Print-Fassung 2019. Vor-2020-Halbsatz im Zielgrößenteil nur bei Sheppard & Young (2006) (§ 6.2).\n\n"
      "**Zitierjahre nach der Version of Record (Crossref 28.09., Textvorschlag Einleitung § 6 Nr. 1 und 2):** Radnor et al. (2018), Sports Med 48(1), 57–71, das PDF ist die Online-First-Fassung 2017 · Moran et al. (2017), JSCR 31(2), 552–565, das PDF ist die Fassung „Publish Ahead of Print“ 2016, L14 (c) erledigt. Seitenangaben nach dem PDF im Ordner, T1 `Radnor2017` und `Hicks2019` werden nachgeführt (G35).")
rep("Negra 2019 ES 2,83 (Baseline-SD 0,0 s) · „1200–1400 Richtungswechsel pro Spiel\" · Alvurdu et al. 2022 · Gonzalo-Skok et al. 2025.",
    "Negra 2019 ES 2,83 (Baseline-SD 0,0 s) · „1200–1400 Richtungswechsel pro Spiel\" · Alvurdu et al. 2022 · Gonzalo-Skok et al. 2025 · Emery 2015 · Thorborg 2017 · Rössler 2016, 2018 und 2019 · Soligard 2008 · Gebert 2020 · Faude 2013 · Bull 2020 · Faigenbaum & Myer 2010 · Pucsok 2021 · Präsentationsquellen zu Screening und Kraftdiagnostik (Befund Relevanz Rev. 2 § 3).")
rep("*Leistungsniveau:* Kein Detraining-Vergleichssetting unterhalb der Akademieebene.",
    "*Leistungsniveau:* Die Formel „kein Detraining-Vergleichssetting unterhalb der Akademieebene“ trägt nicht. Liu et al. (2024) untersuchten regionale U19-Mannschaften, nach eigener Angabe „trained/developmental“ (S. 220), also Tier 2, mit sechs betreuten Einheiten (Textvorschlag Einleitung § 6 Nr. 4). Oliver et al. (2024, S. 623, 625) schlossen nur Spieler ab Tier 3 ein, Tier 3 umfasst dort auch regionale Ligen. Tragfähig ist die Lücke als Kombination aus leistungsorientiertem Breitensport, Wachstumsgipfel und unbeaufsichtigtem, videobasiertem, gerätefreiem Heimprogramm in der Sommerpause (Textvorschlag Einleitung, Absatz 8). Sie heißt „kontrollierte Studien“, weil Pucsok (2021) unkontrolliert ist (Befund Relevanz Rev. 2).")
rep("**Beschaffungsposten:** ⭐ Al Haddad, Simpson & Buchheit (2015) · ⭐ Negra et al. (2020) ·",
    "**Beschaffungsposten:** ⭐ Al Haddad, Simpson & Buchheit (2015) · Altmann et al. (2019), frei als PMC6693781 (H10, entbehrlich, falls 6.2 die Güteaussagen nicht braucht) ·")
rep("· Draper & Lancaster (1985, Fernleihe) · FVM-Rahmenterminplan und Ferienordnung NRW · Erratum Khamis & Roche (1995)",
    "· Draper & Lancaster (1985, Fernleihe) · Erratum Khamis & Roche (1995)")
rep("vor der Zitation in `Ideen und Studien` ablegen und selbst lesen (Voraussetzungsprüfungen § 5.4, § 6).",
    "vor der Zitation in `Ideen und Studien` ablegen und selbst lesen (Voraussetzungsprüfungen § 5.4, § 6). Negra et al. (2020) liegt seit dem 11.09. im Ordner (H7). FVM-Rahmenterminplan und Ferienordnung NRW entfallen mit dem Altbestand 2.3 (Textvorschlag Einleitung § 4).")
rep("Moran et al.: Jahr 2016 oder 2017 über doi 10.1519/JSC.0000000000001444 klären und einheitlich führen",
    "Moran et al.: 2017 nach der Version of Record (JSCR 31(2), 552–565, doi 10.1519/JSC.0000000000001444), L14 (c) erledigt 28.09.")

# ------------------------------------------------------------------ § 6.6 Mindestdosis
zeile("**Leistungsniveau ist kein starker Moderator:**",
      "**Fitnessniveau ist kein nachweisbarer Moderator (vertikale Sprunghöhe):** de Villarreal et al. (2009, Tab. 2, S. 501) fanden für „Fitness“ F(3,121) = 1,97, p = 0,102. Das Fitnessniveau moderierte die Effektstärke der vertikalen Sprunghöhe nicht nachweisbar, mehr trägt der Wert nicht (Klick 28.09., nach der Zweitprüfung von Fassung 17). Für „Sport level“ steht dort F(3,121) = 5,26, p = 0,001, mit nicht monotonem Muster der Effektstärken: International 1,22 aus zwei Effektstärken einer einzigen Studie (Matavulj et al., 2001, Tab. 1), National 0,55, Regional 0,47, keine Athleten 0,94 (am PDF geprüft 28.09., T4 `dV2009`). Für das Leistungsniveau wird keine Richtung angegeben, auf Sprint und Richtungswechsel wird nicht übertragen (T4 `dV2009`, Zielgröße nur vertikale Sprunghöhe) · Behm et al. (2017) ohne KI und p-Werte – nur als Vergleich zweier Punktschätzer formulieren, Vereinssportler zählen dort zu „trained“.")
rep("· Moran et al. (2016) „between 4 and 16 weeks\".", "· Moran et al. (2017) „between 4 and 16 weeks\".")
rep("**Was belegt ist:** Kurze Programme wirken. Moran et al. (2016):", "**Was belegt ist:** Kurze Programme wirken. Moran et al. (2017):")

# ------------------------------------------------------------------ § 7 Quellenverifikation
zeile("**Offene Posten:**",
      "**Offene Posten** (Maßnahmenliste Gruppe H und K18): H4 Melchiorri et al. (2023) · H5 Ruf et al. (2024) und Clemente et al. (2021) · H6 Clemente et al. (2022), frei über PMC9252184, nur noch bei Bedarf für 6.1, der Teil Hoffmann et al. (2014) ist erledigt (Volltext im Ordner, T1-Steckbrief fehlt, Task 15) · H8 Verfahrensquellen der Voraussetzungsprüfungen · H9 Hedges (1981) · H10 Altmann et al. (2019), frei als PMC6693781, nur falls 6.2 die Güteaussagen braucht · K18 Al Haddad et al. (2015) über die Bibliothek · Draper & Lancaster (1985) bleibt Sekundärzitat. Nicht-wissenschaftlicher Beleg zu sichern: Microgate-Handbuch (2016). FVM-Rahmenterminplan (2025) und Ferienordnung NRW entfallen mit dem Altbestand 2.3.")
rep("Die Zitierfallen stehen in `Schreiben\\ev3_daten\\T4_zitierfallen.csv` (131).",
    "Die Zitierfallen stehen in `Schreiben\\ev3_daten\\T4_zitierfallen.csv` (%d, gezählt am 28.09.)." % N_T4)

# ------------------------------------------------------------------ § 8 Zitierstil
rep("Gemessene Ersparnis, die damit entfällt: 184 Autor-Jahr-Einheiten binden 694 Wörter (7,5 % des Absatztexts).",
    "Gemessene Ersparnis, die damit entfiel (Messung vom 13.09., historisch): 184 Autor-Jahr-Einheiten banden 694 Wörter (7,5 % des damaligen Absatztexts).")
rep("Netto-Ersparnis nach Modellrechnung rund 0,35 Seiten. **Bei Zustimmung sinkt das Wortbudget gleichzeitig auf 8.300**, sonst warnt die Zählung nicht mehr vor der Seitengrenze.",
    "Netto-Ersparnis nach der Modellrechnung vom 13.09. rund 0,35 Seiten (historisch, damals bei 9.000 Wörtern). **Bei Zustimmung sinkt das Wortbudget gleichzeitig um die Wörter, die im Master zu diesem Zeitpunkt in Autor-Jahr-Belegen gebunden sind (Messung per Skript)**, sonst warnt die Zählung nicht mehr vor der Seitengrenze.")
rep("· Havanecz et al. (2026) · Clemente et al. (2022) · Mujika & Padilla (2000) ·", "· Havanecz et al. (2026) · Mujika & Padilla (2000) ·")
rep("· FVM-Rahmenterminplan · Ferienordnung NRW · Microgate (2016).",
    "· Microgate (2016) · die Quellen der Einleitung nach der Belegtabelle des Textvorschlags Einleitung (§ 3 dort), mit den bei Crossref geprüften Heftangaben aus Rev. 111 und 114 (McBurnie, Parr, et al., 2022, 44(2), 10–32 · Bianco et al., 2015, 445–478 · Ramirez-Campillo et al., 2020, 50(12), 2125–2143 · Hicks et al., 2020, 42(2), 45–62 · Radnor et al., 2018, 48(1), 57–71 · Moran et al., 2017, 31(2), 552–565). Clemente et al. (2022), FVM-Rahmenterminplan und Ferienordnung NRW entfallen mit dem Altbestand 2.3, die übrigen Streichungen nennt die Verbleibsliste der Einleitung (§ 4 dort).")

# ------------------------------------------------------------------ § 9 Formale Gestaltung
zeile("**Umfangsrahmen, drei Ebenen:**",
      "**Umfangsrahmen, vier Ebenen** (§ 1.1): Verfasser höchstens 33 Seiten einschließlich Literaturverzeichnis, gezählt von der Einleitung bis zum Ende des Literaturverzeichnisses (K1), strengste Grenze und vorgehend · mündliche Betreuervorgabe höchstens 37 Textseiten · Prüfungsordnung § 15 (1) „30 bis 50 Textseiten nicht überschreiten\" (Wortlaut im SMK-Leitfaden Abschn. 2.2) · eigene Steuerung über 6.350 Wörter mit einer Prognose von rund %s Seiten (Modellrechnung). Der Leitfaden Sportmedizin stammt vom Institut für Sportmedizin des Universitätsklinikums Münster und ist nicht einschlägig." % de(S_GB, 1))
rep("Vorspann römisch, Seitenzahlen oben rechts, Seitenumbruch vor jeder Hauptüberschrift.",
    "Vorspann römisch, Seitenzahlen oben rechts, Seitenumbruch vor jeder Hauptüberschrift (fünf Kapitel und Literaturverzeichnis).\n\n"
    "**Literaturverzeichnis:** nach dem Text, vor dem Anhang, hängender Absatz 1 bis 1,5 cm (SMK-Leitfaden Abschn. 4.6). Den Zeilenabstand des Verzeichnisses regelt der Leitfaden nicht, einzeilig verlangt er nur für Beschriftungen und Blockzitate (Abschn. 4.4.4, 4.4.5, 4.5.3). Das Seitenmodell nimmt 1,5 wie im Fließtext an (Abschn. 4.4.2) und hat die Probe so gemessen (§ 1.1). Ein engerer Satz des Verzeichnisses bleibt ein Hebel, falls die Seitengrenze eng wird.")

# ------------------------------------------------------------------ § 10 Sprachstil
rep("Der Master vom 14.09. trägt 92 in 8.796 Wörtern.",
    "Der Master vom 14.09. trug 92 in 8.796 Wörtern (historisch). Stand 28.09.: %d, alle im Altbestand Kapitel 2, der mit der Einleitung entfällt." % VERW_N)
rep("Bestand im Master wird abschnittsweise mit der Textrevision umgebaut (Maßnahmenliste G19).",
    "Kapitel 4 ist verweisfrei, der Rest entfällt mit dem Altbestand (Maßnahmenliste G19).")
rep("Der Bestand des Masters vom 14.09. trägt 168 Semikola in Kapitel 2 und 4. Sie werden abschnittsweise mit der Textrevision umgebaut (Maßnahmenliste G18).",
    "Der Master vom 14.09. trug 168 Semikola in Kapitel 2 und 4 (historisch). Stand 28.09.: %d, alle im Altbestand Kapitel 2, der mit der Einleitung entfällt (Maßnahmenliste G18)." % SEMI_N)
rep("In 4.7 wird die Analysepopulation beschrieben statt etikettiert: „Analysiert wurden alle zugeteilten Spieler in ihrer Gruppe, je Zielgröße mit vollständigen Prä- und Post-Werten und Reifestatus, ohne Ersetzung fehlender Werte.“",
    "4.7 beschreibt die Analysepopulation, statt sie zu etikettieren: „Die Hauptanalyse umfasste unabhängig von der Adhärenz alle zugeteilten Spieler in ihrer Gruppe, je Zielgröße mit vollständigen Prä- und Post-Werten und Reifestatus, ohne Ersetzung fehlender Werte.“")
rep("(„Bei der Ausgangstestung von Verein B fiel die 10-m-Lichtschranke aus.", "(„Bei der Abschlusstestung von Verein B fiel die 10-m-Lichtschranke aus.")
rep("**Kapitelspezifisch:** Theorie – Grundlagen vor Anwendung, Überleitungen.",
    "**Kapitelspezifisch:** Einleitung – vom Allgemeinen zum Besonderen, Überleitungen zwischen den Zügen, Schluss mit den Hypothesen.")

# ------------------------------------------------------------------ § 11 Statistik
rep("Die Stichprobe ist durch die teilnehmenden Vereine vorgegeben.",
    "Die Stichprobe war durch die verfügbaren Spieler und die Zeit an den Testtagen begrenzt (Verfasser 26.09., Textvorschlag 4.7, Nr. 37).")
rep("**Berichtspflicht:** Testfamilie, Numerator df, Gruppenzahl, Kovariatenzahl, n je Gruppe, α, Power, Software mit Version.",
    "**Berichtspflicht:** Testfamilie, Numerator df, Gruppenzahl, Kovariatenzahl, n je Gruppe, α, Power, Software mit Version. 4.7 nennt α, Power und Software und verweist ohne Zahl auf die erreichte Spielerzahl je Zielgröße. Testfamilie, Zähler-df, Gruppen- und Kovariatenzahl und n je Zielgröße sind für Anhang G vorgemerkt (Task 16, Textvorschlag 4.7, Nr. 8), ebenso α und Power der A-priori-Rechnung (Nr. 34). Die Nenner je Gruppe stehen in Tab. 2 und Tab. 3 (Task 11 und 18).")
rep("Der Standardweg ohne Kovariatengewinn ist konservativ, die MDES fällt größer aus.",
    "Der Standardweg ohne Kovariatengewinn fällt am eigenen Datensatz konservativ aus, die MDES größer (Prüfrechnung B11 in Textvorschlag 4.7: Richtung gestützt, nicht allgemein bewiesen, in 4.7 „konservativ“).")
rep("In 4.7 als Planungsstand mit Hinweis auf das abweichende Planungsmodell.",
    "4.7 nennt die Antragsrechnung als Planungsstand (f = 0,25, mindestens 34 Spieler). Der Hinweis auf das abweichende Planungsmodell ist für 6.2 vorgemerkt (Textvorschlag 4.7, Nr. 7).")
zeile("**Kovariaten-Begründung:**",
      "**Kovariaten-Begründung:** prognostisch und vorab festgelegt, ausdrücklich nicht abhängig davon, ob der Baseline-Unterschied signifikant ist (Item 12b). %PAH als externe Kovariate über den prognostischen Haupteffekt: Der Reifestatus bestimmt die Leistungsentwicklung im Jugendalter mit. Das Ungleichgewicht im Reifestatus zwischen den Gruppen verstärkt den Grund, ist aber nie der alleinige (Textvorschlag 4.7, Nr. 46). Nicht als Begründung: die Trainierbarkeit, sie ist eine Wechselwirkung (Prüfung Gruppe × %PAH in Tab. H4), und der Jahrgang, er war bei der Zuteilung nicht bekannt (Nr. 42). Das chronologische Alter überlappt zwischen den Gruppen nicht.")
rep("R6 Seitenzahl (§ 1.1)", "R6 entfällt (Klick K2, 28.09., § 1.1)")
rep("H0 wird verworfen, wenn in mindestens einer konfirmatorischen Zielgröße p < 0,05 in günstiger Richtung liegt (K23, P6).",
    "H0 gilt als verworfen, wenn mindestens eine konfirmatorische Zielgröße einen Vorteil der Interventionsgruppe mit p < 0,05 (zweiseitig) zeigt (Wortlaut 4.7, K23, P6). Zugunsten einer Gruppe liegt die adjustierte Differenz, nicht der p-Wert (Textvorschlag 4.7, Nr. 49).")
rep("· sRPE-Load als individuell gemessene Belastung.",
    "· sRPE-Load als individuell gemessene Belastung. **Dazu aus dem Befund Relevanz Rev. 2 § 4.3 und § 4.4 (G34 f, 28.09.):** „Motivierte machen einen Sprung“ aus den eigenen Daten (zulässig nur als Hypothese im Ausblick) · „Breitensport profitiert stärker“, auch nicht über Rössler et al. (2014), die die Niveaus a posteriori vergleichen · Detraining als alleinige Begründung · Prävention als Wirkung des eigenen Programms · „Sprungübungen tragen den Schutzeffekt“ (§ 4.3 dort) · Gesundheit, Screening, Kraftdiagnostik und Kosten als Relevanzargument.")
rep("H0/HA im Wortlaut des Antrags, auf die Grundgesamtheit bezogen",
    "H0/HA nah am Wortlaut des Antrags, einander ergänzend (G32 e), auf die Grundgesamtheit bezogen")
rep("Der Familienfehler der „mindestens einer“-Hypothese (drei konfirmatorische Tests: bis 14 %) wird in 6.2 benannt",
    "Der Familienfehler der „mindestens einer“-Hypothese (drei Tests zu je 2,5 % in günstiger Richtung: höchstens 7,5 %, 7,3 % bei Unabhängigkeit, Textvorschlag 4.7 B15) ist für 6.2 vorgemerkt")
rep("**Sparsam berichten:** je ein Satz in 4.7, Tab. H4 mit Sammelsatz in 5.2 (R1 regelt die Ausnahme), Einordnung in 6.2 und 6.3.",
    "**Sparsam berichten:** je ein Satz in 4.7 für die Sensitivitätsanalysen und das Bootstrap-Intervall (Absatz 5, Tab. H4 dort zuerst verwiesen), das Bootstrap-Intervall als streichbares Modul (§ 13 Nr. 23), Tab. H4 mit Sammelsatz in 5.2 (R1 regelt die Ausnahme), Einordnung vorgemerkt für 6.2 und 6.3.")
rep("nach Sichtung der IG-Post-Werte, vor Kenntnis der KG-Werte – Protokollabweichung",
    "nach Sichtung der IG-Post-Werte, vor Kenntnis der KG-Werte (Kurzform für „vor der Abschlusstestung der KG“, Textvorschlag 4.7 B8) – Protokollabweichung")
rep("Festlegung 12.09.2026, **vor Kenntnis der KG-Werte**, Verfasserentscheidung",
    "Festlegung 12.09.2026, **vor Kenntnis der KG-Werte** (Kurzform, B8), Verfasserentscheidung")
rep("Alle Schwellen standen vor Kenntnis der KG-Werte fest und werden in 4.7 mit Datum dokumentiert.",
    "Alle Schwellen standen vor Kenntnis der KG-Werte fest (vor der Abschlusstestung der KG, B8). Das Datum jeder Festlegung ist für Tab. H6 vorgemerkt (Verfasser 26.09., 20:51, Task 18), 4.7 nennt die Reihenfolge ohne Datum.")
rep("Einzelwerte nur beim Antragskriterium (drei Spieler, Tab. H2).",
    "Einzelwerte nur beim Antragskriterium (drei Spieler, Tab. H2). Ob sie bleiben, entscheidet Task 11 zu Beginn (Textvorschlag 4.7, Nr. 23, mit Umfangsdokument R5), bis dahin offen.")
rep("Verbindliche Formulierung: „geprüft und nicht verworfen“, mit dem Hinweis, dass der Test bei dieser Fallzahl nur sehr große Abweichungen entdeckt.",
    "Verbindliche Formulierung in 5.2: „geprüft und nicht verworfen“, 4.7 kündigt sie nicht an. Der Hinweis, dass der Test bei dieser Fallzahl nur sehr große Abweichungen entdeckt, ist für 6.2 vorgemerkt (Textvorschlag 4.7, Nr. 15).")

# ------------------------------------------------------------------ § 12 Limitationen
rep("Der Familienfehler der „mindestens einer“-Hypothese gehört in dieselbe Gruppe, ebenso die Grenzen der Voraussetzungsprüfungen (Voraussetzungsprüfungen § 5.3): geringe Trennschärfe, Robustheit bei dieser Fallzahl nicht gesichert, ungleiche Gruppengrößen mit der Richtung aus der Residuen-SD je Gruppe.",
    "Die Stichprobe war durch die verfügbaren Spieler und die Zeit an den Testtagen begrenzt, beide Begrenzungen werden bei der Auflösung genannt (Textvorschlag 4.7, Nr. 37). Familienfehler der „mindestens einer“-Hypothese (höchstens 7,5 %, § 11.4) und Grenzen der Voraussetzungsprüfungen (Voraussetzungsprüfungen § 5.3: geringe Trennschärfe, Robustheit bei dieser Fallzahl nicht gesichert, ungleiche Gruppengrößen mit der Richtung aus der Residuen-SD je Gruppe) ordnet 6.2 ein (Textvorschlag 4.7 § 7, Zeile Task 12). G1 nennt davon nur die Konsequenz in einem Halbsatz, ohne wörtliche Doppelung (§ 5a).")
rep("die Pflicht nach CONSORT 6b tragen Tab. H6 und diese Gruppe, als Entscheidung des Messaufbaus, nicht als Literaturbefund.",
    "die Pflicht nach CONSORT 6b geht auf Tab. H6 und diese Gruppe über (vorgemerkt für Task 18 und 12), als Entscheidung des Messaufbaus, nicht als Literaturbefund.")
rep("**G8 Übertragbarkeit.** Niveaudiskrepanz Stichprobe (Tier 2) gegen Vergleichsevidenz (Tier 3+) – für die Wirksamkeitserwartung nachrangig (de Villarreal et al., 2009, p = 0,102), für die Detraining-Prämisse relevant: Die gesamte E5-Evidenz stammt von Akademie- oder Profispielern [EXTRAPOLATION].",
    "**G8 Übertragbarkeit.** Niveaudiskrepanz Stichprobe (Tier 2 nach 4.2) gegen Vergleichsevidenz (Oliver et al., 2024: nur Spieler ab Tier 3, regionale Ligen eingeschlossen, S. 625). Ob das Leistungsniveau die Wirksamkeit moderiert, ist offen: de Villarreal et al. (2009, Tab. 2) fanden für die vertikale Sprunghöhe beim Sportniveau einen Unterschied ohne monotones Muster, dessen oberste Stufe an zwei Effektstärken einer einzigen Studie hängt (Matavulj et al., 2001), beim Fitnessniveau keinen nachweisbaren (§ 6.6). Behm et al. (2017) zählen Vereinssportler zu „trained“. Für die Detraining-Prämisse ist die Diskrepanz relevant: Die E5-Evidenz stammt überwiegend von Akademie- oder Profispielern, Ausnahmen sind Liu et al. (2024, regionale U19, Tier 2) und das Scoping Review von Dambel et al. (2025) über Kinder und Jugendliche [EXTRAPOLATION].")
rep("**F1 ohne unabhängige Methodenprüfung** gehört als Einschränkung in 4.7 und in G7.",
    "**F1 ohne unabhängige Methodenprüfung** gehört als Einschränkung genau einmal in 6.3, in G7 oder bei Personalunion und Verblindung in G3 (Verfasser 26.09., Textvorschlag 4.7, Nr. 57). Dazu ein Halbsatz zum Restrisiko ohne Zweiterfassung in G4 oder G5.")

# ------------------------------------------------------------------ § 13 Verfasserentscheidungen
rep("Die Berichtspflicht bleibt unverändert (Register im Auswertungsplan, 4.1, 4.7, 6.3).",
    "Die Berichtspflicht bleibt unverändert (Register im Auswertungsplan, 4.1, 4.7, 6.3). Uhrzeiten nach der Sitzungsuhr (§ 1.2).")
rep("F1 durch den Verfasser, ohne unabhängige Methodenprüfung, in 4.7 als Einschränkung (24.09.).",
    "F1 durch den Verfasser, ohne unabhängige Methodenprüfung, als Einschränkung genau einmal in 6.3 (24.09., Ort seit 26.09.).")
rep("Per-Protokoll ≥ 6 von 12 beobachtend (12.09., vor Kenntnis der KG-Werte).",
    "Per-Protokoll ≥ 6 von 12 beobachtend (12.09., vor Kenntnis der KG-Werte, Kurzform für „vor der Abschlusstestung der KG“, B8).")
NEU13 = """
23. **4.7 (Task 6, 26.09.):** Bootstrap bleibt im Bericht, als streichbares Modul geführt (18:16, Streichpaket in Textvorschlag 4.7 § 7) · Voraussetzungsabsatz ohne eigenen Annahmensatz · Beleg Fröhlich et al. (2020, S. 59) gestrichen · Schlussabsatz nur mit Verfahren und Pflichtangaben: Datenprüfung, Auswertung skriptbasiert in R 4.3.3, Anhang G · KI-Nutzung in KI-Deklaration und Anhang G · Gegenproben, Abgleich, Datenstand und Spezifikation werden in 4.7 nicht berichtet (die Gegenproben nennt die KI-Deklaration, Textvorschlag 4.7, Nr. 57), Anhang G ohne Prüfprotokolle · Freigabe ohne unabhängige Methodenprüfung genau einmal in 6.3 · Festlegungsdaten für Tab. H6 vorgemerkt, nicht in 4.7 (20:51) · Stichprobe begrenzt durch die verfügbaren Spieler und die Zeit an den Testtagen (Nr. 37) · Kovariatenbegründung über den prognostischen Haupteffekt (Nr. 42, 46).
24. **Direkter Einbau in Schritt 0 (26.09., 20:55):** Nachkorrekturen per Skript, ausdrückliche Anweisung nach § 1.2, Einzelfall wie Task 5, keine neue Regel.
25. **Zweck des Zielgrößenteils (28.09., 10:30):** aus den physiologischen Anforderungen des Wettkampfs die Zielgrößen und ihre Diagnostik ableiten, kein Testablauf (der steht in 4.3 und 4.4). Gilt für Zug 2 der Einleitung.
26. **Belege zu den Zielgrößen (28.09., Klicks zu 2.4 Fassung 6):** Hicks et al. mit dem Jahr 2020 (Version of Record) · Vor-2020-Halbsatz im Zielgrößenteil nur bei Sheppard & Young (2006), nicht bei Dos'Santos et al. (2018) und Bianco et al. (2015), allgemein geregelt seit Nr. 39 (§ 6.2).
27. **Relevanz und Prävention (28.09., 14:36):** Olivier et al. (2026) als Kernquelle und zusätzlich der Sprungbefund aus Rössler et al. (2014) als Zwischen-Studien-Vergleich, abweichend von der Empfehlung · Ort: Einleitung und ein Satzteil im Ausblick · Hilska et al. (2021) nur Adhärenzreferenz in 6.3 (§ 6.5).
28. **Einleitung (28.09., 14:38, Klick 14:57):** Kapitel 1 bis 3 werden eine Einleitung ohne Unterabschnitte mit höchstens 1.500 Wörtern · SMK Abschn. 4.1 (Forschungsstand in eigenem Kapitel) bewusst nicht erfüllt · 2.4 Fassung 6 wird nicht übertragen · Gesamt 6.350 Wörter, die Festlegung vom 15.09. zur Korpus-Obergrenze ist damit abgelöst.
29. **Seitengrenze (28.09., 15:14):** höchstens 33 Seiten einschließlich Literaturverzeichnis.
30. **Zählweise (Klick K1, 28.09., 16:27):** Einleitung bis Ende des Literaturverzeichnisses, ohne Vorspann und Anhang.
31. **Regel R6 (Klick K2, 28.09., 16:27):** entfällt. Fließtext wird nie aufgefüllt, der Textteil darf unter dem Rahmen „30 bis 50 Textseiten“ bleiben.
32. **Tauschregel (Klick K3, 28.09., 16:27):** Schwelle 32 Seiten, abweichend von der Empfehlung (31), nur für Objekte über die fünf festen hinaus.
33. **Ankersatz (Klick K6, 28.09., 16:27):** entsteht in der Einleitung, Wortlaut in Task 7 neu per Klick (Nr. 37), kehrt in 6.1 und in der Zusammenfassung wieder, 4.1 bleibt ohne Zwecksatz.
34. **Verbleibsliste der Einleitung (28.09., Task 7 neu, Rev. 114):** freigegeben wie vorgeschlagen (Textvorschlag Einleitung § 4), mit den Quellen, die aus dem Literaturverzeichnis fallen (Task 15), und denen, die bis Task 12 ohne Zitat bleiben.
35. **Verletzungssatz (Klick 2 in Task 7 neu):** aufgenommen, der Richtungswechsel als Aktion, die mit Verletzungen der unteren Extremität verbunden ist (Dos'Santos et al., 2018).
36. **Reifemethode (Klick 3 in Task 7 neu):** entfällt in der Einleitung, vorgemerkt für 6.2 (§ 6.5).
37. **Zweck (Klick in Task 7 neu):** „gegenüber einer Kontrollgruppe verbessert“ statt „erhält oder verbessert“ des Antrags, „ohne strukturiertes Training“ entfällt (Verein C hatte einen Lauf- und Athletikplan). Damit ist der Wortlaut des Ankersatzes entschieden (Plan, Klickfrage 10).
38. **de Villarreal et al. (2009) (Klick 28.09., nach der Zweitprüfung von Fassung 17):** „Fitnessniveau ist kein nachweisbarer Moderator“ statt „kein starker Moderator“, die oberste Stufe beim Sportniveau beruht auf zwei Effektstärken einer einzigen Studie (§ 6.6, § 12 G8).
39. **Vor-2020-Halbsatz (Klick 28.09., 17:54):** nur bei Wirksamkeitsevidenz, nicht bei Definitions-, Konzept-, Verfahrens- und Diagnostikquellen, wie im Textvorschlag Einleitung umgesetzt (§ 6.2)."""
rep("Anhang D führt A als „nicht dokumentiert“ oder mit Plan vom Trainerteam (Task 17).",
    "Anhang D führt A als „nicht dokumentiert“ oder mit Plan vom Trainerteam (Task 17)." + NEU13)
rep("13. **Reihenfolge:** Kürzung der vorhandenen Kapitel vor neuen Kapiteln, Anhänge ganz zum Schluss (25.09., abends).",
    "13. **Reihenfolge:** Kürzung der vorhandenen Kapitel vor neuen Kapiteln, Anhänge ganz zum Schluss (25.09., abends). Für Kapitel 2 abgelöst durch Nr. 28, die Einleitung ersetzt die Kürzung.")
rep("17. **4.3:** keine Tagesdaten und Kalenderwochen (Termine in Abb. H7),", "17. **4.3:** keine Tagesdaten und Kalenderwochen (Termine für Abb. H7 vorgemerkt),")
rep("Pause beim Standweitsprung nur in 4.3 (25.09., Klick 5).",
    "Pausenregel beim Standweitsprung nur in 4.3, 4.4.3 nennt nur die Abweichung vom Referenzprotokoll (25.09., Klick 5).")
rep("Kapitelname 3 und Kapitel-6-Struktur (Gliederung v4)", "Kapitelname 3 (historisch, Kapitel 3 geht in der Einleitung auf) und Kapitel-6-Struktur (Gliederung v4)")
rep("Bei Zustimmung sinkt das Wortbudget gleichzeitig auf 8.300 (§ 8).",
    "Bei Zustimmung sinkt das Wortbudget um die Wörter, die im Master in Autor-Jahr-Belegen gebunden sind, gemessen per Skript (§ 8).")
rep("**Erledigt:** Umfangsvorgabe (höchstens 37 Textseiten, Hartgrenze 9.000 Wörter)",
    "**Erledigt:** Umfangsvorgabe (höchstens 37 Textseiten, Hartgrenze damals 9.000 Wörter, seit 28.09. 6.350 und 33 Seiten, § 13 Nr. 28 bis 32)")
rep("· Erratum Khamis & Roche nicht beschaffbar (R14, 25.09.).",
    "· Erratum Khamis & Roche nicht beschaffbar (R14, 25.09.) · Umfang und Seitengrenze (28.09.) · Gliederung v5 (28.09.) · Relevanzstrang (28.09.) · Wortlaut des Ankersatzes (28.09., Task 7 neu).")

# ------------------------------------------------------------------ § 14 KI-Nutzung
rep("Textvorschläge und Skripte entstehen in Claude, die Sitzungen sind über die Rev.-Nummern der Sitzungsnotizen protokolliert (Grundlage des KI-Nutzungsprotokolls, Plan Task 16).",
    "Textvorschläge und Skripte entstehen in Claude, die Sitzungen sind über die Rev.-Nummern der Sitzungsnotizen protokolliert (Grundlage des KI-Nutzungsprotokolls, Plan Task 16).\n\n"
    "**Anhang G und Deklaration (Verfasser 26.09., Textvorschlag 4.7, Nr. 57):** Jedes Skript in Anhang G wird als KI-erzeugt gekennzeichnet, etwa „KI-generierter Code, Claude, ⟨Modell⟩, ⟨Datum⟩“, darunter `Objekte_2026-09-25.R`, das Tab. 1 bis 3 und Abb. 1 und 2 erzeugt. Anhang G trägt keine Prüfprotokolle, sie bleiben im Projekt und werden auf Anfrage vorgelegt. Mindestinhalt der KI-Deklaration nach Textvorschlag 4.7 § 7 (Zeile Task 16): Claude (Anthropic) mit Modellbezeichnung und Zeitraum · Zweck und Umfang (Erstellung und Ausführung aller R-Skripte, Prüfskripte der Datenaufbereitung, Gegenprüfung durch eine zweite Implementierung und eine per Skript angelegte Formelprobe, Textentwürfe) · Verarbeitung pseudonymisierter Studiendaten unter Verantwortung des Verfassers · Festlegungen, Freigaben und Prüfung durch den Verfasser · Verweis auf das KI-Nutzungsprotokoll. Umsetzung in Task 16. Die Aufzählung davor nennt, was offenzulegen ist, dieser Mindestinhalt, wie die Deklaration es fasst. Task 16 führt beide zusammen (Textvorschlag 4.7 B16 und § 7, Zeile Task 16).")

# ------------------------------------------------------------------ Fassung 3: übergreifende Zweitprüfung und Klicks 19:25
# Befund 4: Objekte ohne Platzhalter, Tab. 1 nach G31 (b)
rep("den für Tab. 1 setzt Task 18 nach G31 (a) (§ 5.3).",
    "Tab. 1 setzt Task 18 direkt nach G31 (b), der Platzhalter aus G31 (a) entfällt (§ 5.3).")
rep("Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter, den für Tab. 1 setzt Task 18 nach G31 (a).",
    "Bis dahin stehen sie nicht im Master, auch nicht als Platzhalter. Tab. 1 setzt Task 18 direkt nach G31 (b), der Platzhalter aus G31 (a) entfällt.")
rep("16. **Objekte:** zunächst als Platzhalter, eingesetzt in Task 18 (25.09., 22:25).",
    "16. **Objekte:** erst in Task 18 eingesetzt, bis dahin im Text keine Platzhalter, Platzhalter nur für die Anhangsobjekte in Anhang H (25.09., 22:25, präzisiert 28.09.).")
# Befund 5: Verbot nur für die Mindestdosis
rep("**Zwei Quellen dürfen nicht als Beleg zitiert werden:** Ramirez-Campillo et al. (2023)",
    "**Zwei Quellen dürfen nicht als Beleg für eine Mindestdosis zitiert werden:** Ramirez-Campillo et al. (2023)")
rep("Zheng et al. (2025) „within just 4–7 weeks\" ist ein Relais auf eine Querschnittsstudie ohne Intervention.",
    "Zheng et al. (2025) „within just 4–7 weeks\" ist ein Relais auf eine Querschnittsstudie ohne Intervention. Für andere Aussagen sind beide nach T4 zulässig, so in der Einleitung (Gegenbefund beim Richtungswechsel, Richtungswechsel und Programmdauer).")
# Befund 27: Prompt dieses Tasks erledigt
rep("| `Claude\\04_Uebergaben\\Uebergabe_Steuerdokumente_2026-09-28.md` | Prompt des Tasks Steuerdokumente 28.09. (Task 1b des Plans, Fassung 17 und Folgeänderungen), nach Erledigung ins Archiv |\n", "")
rep("`Uebergabe_Steuerdokumente_2026-09-25.md` (erledigt)",
    "`Uebergabe_Steuerdokumente_2026-09-25.md` und `Uebergabe_Steuerdokumente_2026-09-28.md` (erledigt, der Task vom 28.09. mit Rev. 115)")
# Befund 36: Ramirez-Campillo et al. (2020) in § 6.5 wie in § 8
rep("Ramirez-Campillo et al. (2020): nur das akzeptierte Manuskript im Ordner, Band, Seiten und DOI prüfen, Vorzeichen und Teilung nach Einheiten beachten.",
    "Ramirez-Campillo et al. (2020): nur das akzeptierte Manuskript im Ordner, Band und Seiten bei Crossref geprüft (50(12), 2125–2143, Rev. 111, § 8), Vorzeichen und Teilung nach Einheiten beachten.")
# Befund 40: Textstufen bleiben als Skriptausgaben
rep("`Textvorschlag_4.7_2026-09-25.md` mit den Textstufen `_A`, `_Empf`, `_Kurz` (ersetzt durch den Textvorschlag vom 26.09.)",
    "`Textvorschlag_4.7_2026-09-25.md` (ersetzt durch den Textvorschlag vom 26.09., die Textstufen `_A`, `_Empf`, `_Kurz` bleiben als Ausgaben des Skripts `Textvorschlag_4.7_2026-09-25.py` in `03_Skripte`)")
# Klick 19:25: Erratum Khamis & Roche ohne Hinweis in der Arbeit
rep("Das Erratum (1995) wurde nicht eingesehen (Rechercheprotokoll 25.09., Register R14), die Koeffizienten stammen aus der Originalpublikation. Das Erratum ist nur für Anhang G vorgemerkt und steht im Register R14, nicht im Fließtext (Verfasser 25.09.)",
    "Die Koeffizienten stammen aus der Originalpublikation. Das Erratum (1995) wurde nicht eingesehen (Rechercheprotokoll 25.09., Register R14) und wird in der Arbeit nicht erwähnt, weder im Fließtext noch in Anhang G noch in Tab. H6 (Verfasser 25.09. und 28.09., § 13 Nr. 40)")
rep(" · Erratum Khamis & Roche (1995), doi 10.1542/peds.95.3.457, nicht beschaffbar, nicht eingesehen (Rechercheprotokoll 25.09., R14)", "")
rep("Erratum nicht im Fließtext,", "Erratum nicht im Fließtext (seit 28.09. überhaupt nicht in der Arbeit, Nr. 40),")
# Klick 19:25: Verdünnungslogik in 6.1, Limitation in 6.3
rep("**Verdünnungslogik für 6.2:**", "**Verdünnungslogik für 6.1:**")
rep("**Dieser Satz trägt die Diskussion des Hauptbefunds.**",
    "**Dieser Satz trägt die Diskussion des Hauptbefunds.** Er steht in 6.1 als Einordnung des Hauptbefunds, als Limitation in 6.3 (G3), 6.2 führt keinen eigenen Absatz dazu (Klick 28.09., 19:25, § 13 Nr. 41).")
rep("39. **Vor-2020-Halbsatz (Klick 28.09., 17:54):** nur bei Wirksamkeitsevidenz, nicht bei Definitions-, Konzept-, Verfahrens- und Diagnostikquellen, wie im Textvorschlag Einleitung umgesetzt (§ 6.2).",
    "39. **Vor-2020-Halbsatz (Klick 28.09., 17:54):** nur bei Wirksamkeitsevidenz, nicht bei Definitions-, Konzept-, Verfahrens- und Diagnostikquellen, wie im Textvorschlag Einleitung umgesetzt (§ 6.2).\n"
    "40. **Erratum Khamis & Roche (Klick 28.09., 19:25):** kein Hinweis in der Arbeit, weder im Fließtext noch in Anhang G noch in Tab. H6. R14 steht wie R1, R9, R10, R12 und R13 nicht in Tab. H6. Das Rechercheprotokoll und der Registereintrag bleiben im Projekt (§ 2, Zeile Reifestatus).\n"
    "41. **Verdünnungslogik (Klick 28.09., 19:25):** in 6.1 als Einordnung des Hauptbefunds, als Limitation in 6.3 (G3), 6.2 ohne eigenen Absatz dazu (§ 11.7).")
rep("**(E) Entscheidungen seit dem 26.09.** (§ 13 Nr. 23 bis 39):", "**(E) Entscheidungen seit dem 26.09.** (§ 13 Nr. 23 bis 41):")
rep("nach der Zweitprüfung dieser Fassung: Fitnessniveau bei de Villarreal et al. (2009), Vor-2020-Halbsatz nur bei Wirksamkeitsevidenz.",
    "nach der Zweitprüfung dieser Fassung: Fitnessniveau bei de Villarreal et al. (2009), Vor-2020-Halbsatz nur bei Wirksamkeitsevidenz · nach der übergreifenden Zweitprüfung: Erratum ohne Hinweis in der Arbeit, Verdünnungslogik in 6.1.")

# ------------------------------------------------------------------ Ausgabe
t = re.sub(r'\n{3,}', '\n\n', t)
with open(F17, 'w', encoding='utf-8', newline='\n') as f:
    f.write(t)
print('Fassung 17 geschrieben: %d Zeichen, %d Ersetzungen' % (len(t), len(PROTOKOLL)))
for p in PROTOKOLL:
    print('  ersetzt:', p)

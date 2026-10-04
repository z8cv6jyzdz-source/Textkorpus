# -*- coding: utf-8 -*-
"""Steuerung Rev. 134 (30.09.2026): Verfasserentscheidung „Einleitung pausiert,
Schlussfassung am Ende des Prozesses“, neue Reihenfolge, Einleitung als Zwischenstand.

Schreibt drei Steuerdokumente fort, jede Änderung an einem eindeutigen Anker
(Abbruch, wenn ein Anker nicht genau einmal vorkommt):
  1. Plan_Weitere_Schritte_2026-09-25.md: Nachtrag 30.09. im Kopf, Vermerk in § 0,
     Startsätze ab 30.09. in § 8, Ersetzungsvermerk bei den alten Startsätzen 11 bis 13
  2. Massnahmenliste_Datenverarbeitung.md: Stand, G35, G37, Vermerk zur Zuordnungstabelle
  3. Cowork_Sitzungsnotizen.md: Stand-Zeile, Block Rev. 134 in Teil 0

Aufruf: python3 Steuerung_Rev134_2026-09-30.py <Eingangsordner Claude> <Ausgabeordner> <Uhrzeit>
Eingang: gestagte Fassungen aus dem Ordner (Stand Rev. 133). Kein Manuskripttext, Master unberührt.
"""
import hashlib
import os
import sys

SRC, OUT, UHR = sys.argv[1], sys.argv[2], sys.argv[3]
LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


def lesen(rel):
    with open(os.path.join(SRC, rel), encoding="utf-8", newline="") as f:
        return f.read()


def schreiben(rel, txt):
    ziel = os.path.join(OUT, os.path.basename(rel))
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    b = txt.encode("utf-8")
    log(f"geschrieben {ziel}: {len(b)} Byte, MD5 {hashlib.md5(b).hexdigest()}")
    return len(b), hashlib.md5(b).hexdigest()


def ersetze(txt, alt, neu, name):
    n = txt.count(alt)
    if n != 1:
        raise SystemExit(f"ABBRUCH {name}: Anker {n}-mal gefunden")
    log(f"ok {name}")
    return txt.replace(alt, neu)


def zeile_anhaengen(txt, praefix, zusatz, name):
    zeilen = txt.split("\n")
    treffer = [i for i, z in enumerate(zeilen) if z.startswith(praefix)]
    if len(treffer) != 1:
        raise SystemExit(f"ABBRUCH {name}: Zeilenanfang {len(treffer)}-mal gefunden")
    i = treffer[0]
    zeilen[i] = zeilen[i].rstrip() + " " + zusatz
    log(f"ok {name} (Zeile {i + 1})")
    return "\n".join(zeilen)


# ---------------------------------------------------------------- 1 Plan
PLAN = "04_Uebergaben/Plan_Weitere_Schritte_2026-09-25.md"
plan = lesen(PLAN)

nachtrag = (
    "**Nachtrag 30.09.2026 (Rev. 134 der Sitzungsnotizen), Verfasserentscheidung, keine neue Revision des Plans:** "
    "Die Einleitung wird pausiert und am Ende des Prozesses formuliert (Verfasser 30.09., 20:33). "
    "Der freigegebene Stand (`04_Uebergaben\\Textvorschlag_Einleitung_Ueberarbeitung_2026-09-30.md` § 5.1, 930 Wörter) "
    "kommt jetzt als Zwischenstand in den Master, der Verfasser überträgt, Task 11 gleicht in Schritt 0 ab. "
    "Neue Reihenfolge (Klick 30.09.): **Task 11** Kapitel 5 (450) → **Task 12a** 6.1 Einordnung der Ergebnisse (700) → "
    "**Task 12b** 6.2 und 6.3 als ein Abschnitt nach Gliederung v6 (900) → **Task 13a** Kapitel 7 (250) → "
    "**Task „Einleitung, Schlussfassung“** → **Task 13b** Zusammenfassung und Abstract → "
    "**Steuerdokumente-Task** (G37: Fassung 18, Berichtsraster Rev. 4, Plan Rev. 6) → Tasks 15 bis 18 unverändert. "
    "Das ersetzt die Reihenfolge des Nachtrags vom 29.09. Task 12 wird von vornherein geteilt, nicht erst bei vollem Kontext. "
    "Task 13 wird geteilt, weil Zusammenfassung und Abstract auch den Rahmen der Einleitung zusammenfassen. "
    "Bis zum Steuerdokumente-Task gilt Gliederung v6 vor Fassung 17 § 5.1 bis § 5.3 und § 5a (Rev. 116), "
    "das Messskript Fassung 4 kommt mit Task 11 (G37 d), die Zuordnung der Rasterzeilen 6.2.x zu G1 bis G8 zu Beginn von Task 12b. "
    "**Schlussfassung der Einleitung:** ein Task mit festem Prüfkatalog auf Basis des Zwischenstands, kein Neuaufbau, "
    "Obergrenze 1.200 Wörter (Klick 29.09.): (a) Forschungsstand und Gegenbefunde gegen die Vorstudien in 6.1 · "
    "(b) Lücke gegen Stärken und Limitationen in 6.3 · (c) Hypothesen gegen die H0-Entscheidung in Kapitel 5 · "
    "(d) Präventionssatz gegen den Satzteil im Ausblick · (e) Quellen gegen das Literaturverzeichnis. "
    "Danach Übertragung, Abgleich und die aufgeschobenen Nachträge (G35 a, i, k, l, H12, I20, T1, T4). "
    "Rasterzeile 5.1.4: Studie planmäßig beendet, ohne vorzeitigen Abbruch (Verfasser, Klick 30.09.). "
    "Startsätze in § 8 (ab 30.09.), die Startsätze für Task 11, 12 und 13 der Rev. 5 gelten nicht mehr.\n\n"
)
plan = ersetze(plan, "\n## 0 Ergebnis in Kürze\n", "\n" + nachtrag + "## 0 Ergebnis in Kürze\n", "Plan Nachtrag 30.09.")

alt0 = "nächster Schritt ist Task „Einleitung neu“, siehe Nachtrag im Kopf.)*"
plan = ersetze(
    plan,
    alt0,
    alt0 + " *(Rev. 134, 30.09.: Einleitung pausiert, Zwischenstand in den Master, nächster Task ist Task 11, siehe Nachtrag vom 30.09. im Kopf.)*",
    "Plan § 0 Vermerk",
)

intro8 = (
    "Jeder Startsatz setzt voraus, dass die aktuelle Fassung der Projektanweisungen in den Projekteinstellungen steht "
    "(bis zum Einsetzen von Fassung 17 gilt Fassung 16, danach Fassung 17) und Teil 0 der Sitzungsnotizen zuerst gelesen wird. "
    "Rücksprache nur per Klick.\n"
)
start_neu = (
    "\n**Startsätze ab 30.09. (Rev. 134 der Sitzungsnotizen), in dieser Reihenfolge:**\n\n"
    "- **Task 11 (Kapitel 5):** „Task Kapitel 5 (Ergebnisse) nach Plan § 3 Task 11 und Nachtrag 30.09. "
    "Lies zuerst Teil 0 der Sitzungsnotizen (Rev. 134). Schritt 0: die vom Verfasser übertragene Einleitung per Skript gegen "
    "`04_Uebergaben\\Textvorschlag_Einleitung_Ueberarbeitung_2026-09-30.md` § 5.1 abgleichen (wortgleich, Messung), "
    "ohne die aufgeschobenen Nachträge, dazu Messskript Fassung 4 (G37 d). Dann Berichtsraster § 3.12 und § 3.13, Bauplan § 2.3, "
    "Gliederung v6 § 3.1, Umfangsdokument § 3, § 5 und § 7, Kennzahlenblatt 25.09. Rev. 2, `Objekte_2026-09-25`, "
    "Textvorschlag 4.7 vom 26.09. § 7, Stilprofil, Skill. Kapitel 5 als ein Kapitel ohne Unterabschnitte "
    "(Absatzgruppen 5.1 und 5.2, E3 am Text prüfen), Budget 450. Rasterzeile 5.1.4: planmäßig beendet (Verfasser 30.09.). "
    "Textvorschlag mit gemessenem Kopf und Kennungen im Begleitteil, Zweitprüfung durch einen Subagenten, dann Klicks zu Nr. 23 "
    "und zur Lokalisation der Schmerzmeldungen zusammen mit der Freigabe, die Empfehlung ist im Vorschlag umgesetzt. "
    "Einbau per Skript, nur Text, keine Objekte und keine Platzhalter, Endabgleich, Rev. Vormerkungen für Kapitel 4 und für die "
    "Schlussfassung der Einleitung sammeln, nicht einbauen.“\n"
    "- **Task 12a (6.1):** „Task Diskussion, Einordnung der Ergebnisse (6.1) nach Plan § 3 Task 12 und Nachtrag 30.09. "
    "Zuerst Teil 0, Berichtsraster § 3.14 (6.1.1 bis 6.1.4), Bauplan § 2.4, Gliederung v6 § 3.1, F17 § 11.2, § 11.2b, § 11.7, "
    "§ 6.5 und § 6.6, Kennzahlenblatt K-05 bis K-11, T1 und T4, Textvorschlag 4.7 vom 26.09. § 7 (Zeilen Task 12), "
    "Kapitel 5 im Master, die Vormerkungen für 6.1 bis 6.3 aus den Einleitungs-Textvorschlägen (28.09. § 6 Nr. 7, 29.09. § 8, "
    "A1 A2 § 7, Umbau § 7, B1 § 6, B2 § 8 mit A5, C5 und D5, B3 bis B5 § 7, B4 § 5, Überarbeitung § 2.8). "
    "Eröffnung mit dem Ankersatz ohne „deshalb“, Verdünnungslogik als Einordnung des Hauptbefunds, je Zielgröße ein Absatz, "
    "Budget 700. Textvorschlag mit Zweitprüfung, Klickfreigabe, Einbau, Endabgleich, Rev. Vorstudien, die die Einleitung "
    "einführen muss, als Vormerkung für ihre Schlussfassung sammeln.“\n"
    "- **Task 12b (6.2 und 6.3):** „Task Diskussion, Methodendiskussion, Stärken und Limitationen (6.2 und 6.3 als ein Abschnitt "
    "nach Gliederung v6) nach Plan § 3 Task 12 und Nachtrag 30.09. Zuerst Teil 0, dann die Zuordnung der Rasterzeilen 6.2.x zu "
    "G1 bis G8 oder zu den Methodenbegründungen (G37 a, Berichtsraster § 3.14), F17 § 12, Voraussetzungsprüfungen § 5.3 und § 6, "
    "Umfangsdokument § 5 und § 7, Auswertungsplan § 5 mit § 5.10, `RCT_Auswertungspraxis_2026-09-11`, die aus 4.7 verschobenen "
    "Sätze, die Vormerkungen wie in Task 12a, Kapitel 5 und 6.1 im Master. Bauform Sammoud, Budget 900. Textvorschlag mit "
    "Zweitprüfung, Klickfreigabe, Einbau, Endabgleich, Rev.“\n"
    "- **Task 13a (Kapitel 7):** „Task Kapitel 7 (Fazit und Ausblick) nach Plan § 3 Task 13 und Nachtrag 30.09., ohne "
    "Zusammenfassung und Abstract. Zuerst Teil 0, Berichtsraster § 3.15, Bauplan § 2.5, Gliederung v6 § 3.1, Kapitel 5 und 6 im "
    "Master, G32 (d), G34 (b). Ein Absatz, Budget 250, keine neue Zahl, keine Quelle. Textvorschlag mit Zweitprüfung, "
    "Klickfreigabe, Einbau, Endabgleich, Rev.“\n"
    "- **Task „Einleitung, Schlussfassung“:** „Task Schlussfassung der Einleitung nach Plan Nachtrag 30.09. Zuerst Teil 0, die "
    "Einleitung im Master, Textvorschlag Überarbeitung § 5, Kapitel 5 bis 7 im Master und die dort gesammelten Vormerkungen für "
    "die Einleitung. Kein Neuaufbau: Prüfkatalog (a) bis (e) aus dem Nachtrag als Vorschlagsliste mit Fundstelle, Neufassung und "
    "Begründung, Obergrenze 1.200 Wörter, Zweitprüfung, Klick je Absatz, Übertragung durch den Verfasser, Abgleich, danach die "
    "aufgeschobenen Nachträge (G35 a, i, k, l, H12, I20, T1, T4).“\n"
    "- **Task 13b (Zusammenfassung und Abstract):** „Task Zusammenfassung und Abstract nach Plan § 3 Task 13 und Nachtrag 30.09. "
    "Zuerst Teil 0, Berichtsraster § 3.0 (V4, V5), Gliederung v6 § 3.3, F17 § 10, Kennzahlenblatt K-01, K-06 und K-10, "
    "Ankersatz ohne „deshalb“ aus der Schlussfassung der Einleitung, G25d (M16). Textvorschlag, Zweitprüfung, Klickfreigabe, "
    "Einbau, Endabgleich auch über den Vorspann, Rev.“\n"
    "\n**Startsätze der Rev. 5 (für Task 11, 12 und 13 ersetzt, siehe oben):**\n"
)
plan = ersetze(plan, intro8, intro8 + start_neu, "Plan § 8 Startsätze ab 30.09.")

vermerk_alt = "*(Rev. 134: ersetzt durch die Startsätze ab 30.09. oben.)*"
plan = zeile_anhaengen(plan, "- **Task 11:** „Task Kapitel 5 nach Plan § 3 Task 11.", vermerk_alt, "Plan § 8 alter Startsatz 11")
plan = zeile_anhaengen(plan, "- **Task 12:** „Task Kapitel 6 nach Plan § 3 Task 12.", vermerk_alt, "Plan § 8 alter Startsatz 12")
plan = zeile_anhaengen(plan, "- **Task 13:** „Task Kapitel 7, Zusammenfassung und Abstract", vermerk_alt, "Plan § 8 alter Startsatz 13")
if ";" in nachtrag + start_neu:
    raise SystemExit("ABBRUCH: Semikolon im neuen Plantext")
plan_bytes, plan_md5 = schreiben(PLAN, plan)

# ---------------------------------------------------------------- 2 Maßnahmenliste
ML = "00_Steuerung/Massnahmenliste_Datenverarbeitung.md"
ml = lesen(ML)
alt_stand = "**Stand 30.09.2026, 20:00 Sitzungsuhr (Rev. 133 — "
neu_stand = (
    f"**Stand 30.09.2026, {UHR} Sitzungsuhr (Rev. 134 — Verfasserentscheidung: Einleitung pausiert, Schlussfassung am Ende "
    "des Prozesses, freigegebener Stand als Zwischenstand in den Master, neue Reihenfolge nach Plan Nachtrag 30.09. "
    "G35 und G37 fortgeschrieben, Vermerk zur Zuordnungstabelle). Zuvor 30.09.2026, 20:00 Sitzungsuhr (Rev. 133 — "
)
ml = ersetze(ml, alt_stand, neu_stand, "Maßnahmenliste Stand")
v35 = (
    "*(Rev. 134, 30.09.: Einleitung pausiert (Verfasser 20:33), Schlussfassung als Task mit Prüfkatalog nach Task 13a "
    "(Plan Nachtrag 30.09.). Der freigegebene Stand kommt als Zwischenstand in den Master, Abgleich in Task 11 Schritt 0. "
    "(a), (i), (k) und (l) mit H12, I20, T1 und T4 folgen mit der Schlussfassung.)*"
)
ml = zeile_anhaengen(ml, "- [ ] **G35 · Neuzuschnitt", v35, "Maßnahmenliste G35")
v37 = (
    "*(Rev. 134, 30.09.: Der Steuerdokumente-Task folgt nach Task 13b, vor Task 15 (Plan Nachtrag 30.09.). (d) bleibt bei "
    "Task 11. Aus (a) die Zuordnung der Rasterzeilen 6.2.x zu G1 bis G8 zu Beginn von Task 12b. Bis dahin gilt Rev. 116.)*"
)
ml = zeile_anhaengen(ml, "- [ ] **G37 · Kapitelstruktur", v37, "Maßnahmenliste G37")
kopf_zuo = "**Zuordnung der offenen Punkte zu den Tasks des Plans (`04_Uebergaben\\Plan_Weitere_Schritte_2026-09-25.md`, Rev. 5 vom 28.09.):**\n\n"
v_zuo = (
    "*(Rev. 134, 30.09.: Reihenfolge nach Plan Nachtrag 30.09.: 11 → 12a (6.1) → 12b (6.2 und 6.3) → 13a (Kapitel 7: G32 d, "
    "G34 b) → Einleitung, Schlussfassung (Zeile 7 neu) → 13b (Zusammenfassung und Abstract: G25d M16) → Steuerdokumente (G37) → "
    "15 bis 18. Die Punkte der Zeile 12 verteilen sich nach Abschnitt auf 12a und 12b.)*\n\n"
)
ml = ersetze(ml, kopf_zuo, kopf_zuo + v_zuo, "Maßnahmenliste Zuordnungstabelle")
if ";" in neu_stand + v35 + v37 + v_zuo:
    raise SystemExit("ABBRUCH: Semikolon im neuen Text der Maßnahmenliste")
ml_bytes, ml_md5 = schreiben(ML, ml)

# ---------------------------------------------------------------- 3 Sitzungsnotizen
SN = "00_Steuerung/Cowork_Sitzungsnotizen.md"
sn = lesen(SN)
sn = ersetze(
    sn,
    "**Stand: (Rev. 133 — siehe Block oben.) Zuvor:",
    "**Stand: (Rev. 134 — siehe Block oben.) Zuvor: (Rev. 133 — siehe Block oben.) Zuvor:",
    "Notizen Stand-Zeile",
)
block = f"""### ⭐⭐ NEU (Rev. 134, 30.09.2026, {UHR} Sitzungsuhr, Auftrag 20:33): Verfasserentscheidung „Einleitung pausiert, Schlussfassung am Ende des Prozesses“ — neue Reihenfolge, nächster Task 11 (Kapitel 5), Einleitung als Zwischenstand in den Master

**Auftrag (Verfasser, 30.09., 20:33, wörtlich):** „Wir pausieren das Formulieren der Einleitung. Es ist der wichtigste TEil der Arbeit und sollte am Ende des Prozesses formuliert werden. Konzentrieren wird uns auf andere Abschnitte. Prüfe das optimale Vorgehen und welcher Abschnitt idealerweise jetzt ansteht“

**Befund (im Chat vorgelegt):** Kapitel 5 bis 7 warten auf nichts aus der Einleitung. Zweck als Ankersatz (Klick 28.09., in 6.1 und in der Zusammenfassung ohne „deshalb“, Rev. 128) und Hypothesen nah am Antrag stehen fest. Kapitel 5 ist der einzige Abschnitt ohne offene Abhängigkeit (Kennzahlenblatt, Objekte und Schlusslogik fertig), und die Diskussion deutet, was Kapitel 5 berichtet. Die Einleitung hatte seit dem 28.09. 18 Revisionen (Rev. 114 und 117 bis 133), die Schlussfassung wird deshalb ein Task mit festem Prüfkatalog auf Basis des freigegebenen Stands, kein Neuaufbau.

**Klickantworten (Verfasser, 30.09., bis 20:47 Sitzungsuhr, alle wie empfohlen):** (1) Reihenfolge wie unten · (2) der freigegebene Stand der Einleitung (Textvorschlag Überarbeitung § 5.1, 930 Wörter) kommt jetzt als Zwischenstand in den Master, der Verfasser überträgt · (3) Studie planmäßig beendet, ohne vorzeitigen Abbruch (CONSORT 14b, Rasterzeile 5.1.4, die Verfasserangabe aus Plan Task 11).

**Entschieden, Reihenfolge ab jetzt (Plan, Nachtrag 30.09.):** Task 11 Kapitel 5 (450) → Task 12a 6.1 Einordnung (700) → Task 12b 6.2 und 6.3 als ein Abschnitt nach Gliederung v6 (900) → Task 13a Kapitel 7 (250) → Task „Einleitung, Schlussfassung“ → Task 13b Zusammenfassung und Abstract → Steuerdokumente-Task (G37) → Tasks 15 bis 18 unverändert. Abgelöst: die Reihenfolge aus Rev. 133 (Übertragung → Abgleich → Steuerdokumente → Task 11) und aus dem Plan-Nachtrag vom 29.09., für die Einleitung auch F17 § 13 Nr. 13 („Kürzung vor Neuem“).

**Regeln dazu:**
- **Schlussfassung der Einleitung:** Grundlage ist der Zwischenstand im Master (wortgleich Textvorschlag Überarbeitung § 5.1), Obergrenze 1.200 Wörter (Klick 29.09.). Prüfkatalog: (a) Forschungsstand und Gegenbefunde gegen die Vorstudien in 6.1 · (b) Lücke gegen Stärken und Limitationen in 6.3 · (c) Hypothesen gegen die H0-Entscheidung in Kapitel 5: B5 spricht von „Veränderungen“, Kapitel 5 berichtet die adjustierte Differenz im Post-Wert. Bei Adjustierung für den Ausgangswert ist das rechnerisch dieselbe Gruppendifferenz, der Wortlaut soll trotzdem zusammenpassen (F17 § 10, ANCOVA-Sprachregelung) · (d) Präventionssatz (B1b S7) gegen den Satzteil im Ausblick (G34 b) · (e) Quellen gegen das Literaturverzeichnis (Task 15). Danach Übertragung, Abgleich und die aufgeschobenen Nachträge (G35 a, i, k, l, H12, I20, T1, T4). Vormerkungen für die Einleitung sammeln die Tasks 11 bis 13a.
- **Steuerdokumente:** Der Task (G37 a bis c, j bis l, G35 k, G32 j Rest) folgt nach Task 13b, vor Task 15. Bis dahin gilt Rev. 116: Gliederung v6 geht Fassung 17 § 5.1 bis § 5.3 und § 5a vor, Budgets je Abschnitt der v6 (3 450 · 4.1 700 · 4.2 900 · 5 250). Messskript Fassung 4 mit Task 11 (G37 d). Die Zuordnung der Rasterzeilen 6.2.x zu G1 bis G8 (G37 a, Raster § 3.14) zu Beginn von Task 12b.
- **Task 11:** Schritt 0 gleicht die übertragene Einleitung per Skript gegen Textvorschlag Überarbeitung § 5.1 ab (wortgleich, Messung), ohne die aufgeschobenen Nachträge. Ist sie beim Start nicht übertragen, misst Task 11 den Master wie vorgefunden, und der Abgleich wandert in den nächsten Task. Nr. 23 und die Lokalisation der Schmerzmeldungen (5.1.8) als Klick zusammen mit dem Textvorschlag, die Empfehlung ist im Vorschlag umgesetzt (Verfasserregel vom 26.09.: keine Rückfragen vor dem Textvorschlag).

**Offen beim Verfasser:** (1) Übertragung der Einleitung: im Master die Überschriften „2 Theoretischer Hintergrund und Forschungsstand“ bis einschließlich „3 Fragestellung und Hypothesen“ samt Text löschen (2.1 bis 2.5 mit 2.4.1 bis 2.4.3), die sechs Absätze aus Textvorschlag Überarbeitung § 5.1 ohne die Kennungen B1a bis B5 unter „1 Einleitung“ einfügen, F9, Word schließen, melden · aus Rev. 130 bis 133: (2) `Ordner_aufraeumen.ps1` · (3) Skill-Vorschlag speichern (G26g, G37 h).

**Stand der Dateien:** Geändert: diese Notizen (Rev. 134 auf Rev. 133) · Plan (Nachtrag 30.09., § 0, § 8 mit den Startsätzen für Task 11, 12a, 12b, 13a, „Einleitung, Schlussfassung“ und 13b, keine neue Revision, {plan_bytes:,} Byte, MD5 `{plan_md5[:8]}…`) · Maßnahmenliste (Stand, G35, G37, Vermerk zur Zuordnungstabelle, {ml_bytes:,} Byte, MD5 `{ml_md5[:8]}…`), je Ordner und Projektkopie. Neu: `03_Skripte\\Steuerung_Rev134_2026-09-30.py` mit `.txt`. Unverändert: Master (48.791 Byte, MD5 `e35315d6…`, keine `comments.xml`, geprüft 30.09.), Fassung 17, Gliederung v6, Berichtsraster, Textvorschläge, T1, T4. Rückschreibung je Datei aus eigenem Ausgabepfad, danach neu gestagt und per MD5 verglichen.

**Nächster Schritt:** Task 11 (Kapitel 5) mit dem Startsatz aus Plan § 8 (ab 30.09.), nach der Meldung der Übertragung.

"""
block = block.replace(f"{plan_bytes:,}", f"{plan_bytes:,}".replace(",", ".")).replace(f"{ml_bytes:,}", f"{ml_bytes:,}".replace(",", "."))
if ";" in block:
    raise SystemExit("ABBRUCH: Semikolon im Block Rev. 134")
anker133 = "### ⭐⭐ NEU (Rev. 133, 30.09.2026, 20:00 Sitzungsuhr, Taskende)"
sn = ersetze(sn, anker133, block + anker133, "Notizen Block Rev. 134")
schreiben(SN, sn)

with open(os.path.join(OUT, "Steuerung_Rev134_2026-09-30.txt"), "w", encoding="utf-8") as f:
    f.write("Steuerung Rev. 134, Lauf " + UHR + " Sitzungsuhr\n" + "\n".join(LOG) + "\n")
print("fertig")

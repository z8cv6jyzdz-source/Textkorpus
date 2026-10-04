# -*- coding: utf-8 -*-
"""
Master_Schritt0_2026-09-26.py — Schritt 0 der Übergabe Kapitel 2 (Abschluss Task 6)
Bachelorarbeit U15-Plyometrie · DSHS Köln

Direkter Einbau auf ausdrückliche Anweisung des Verfassers (26.09.2026, 20:55: „Bitte übernehme du das“,
F16 § 1.2), Umfang nach seiner Nachricht von 20:51 und der Klickantwort zu 4.6 (Rev. 105 mit Nr. 20):
  R1  4.1 Abs. 5, vorletzter Satz: Nr. 21 (Textvorschlag 4.7 vom 26.09. § 1.3)
  R2  4.4.2 Schlusssatz: Punkt ergänzt (Nr. 22, Maßnahme G31 a)
  R3  4.6 Abs. 1: Wortlaut Rev. 105 (Befund B1), „Ethikantrag“ bleibt (Nr. 29 nicht übernommen)
  R4  4.6 Abs. 2: Wortlaut Rev. 105 mit „Adhärenzkriterium“ (Nr. 20), „Ethikantrag“ bleibt
  R5  4.7 Abs. 1: Beleg „S. 7“ → „S. 17“ (Box 6 steht auf S. 17 von 28, am PDF geprüft)
  R6  4.7 Abs. 1: „nach Antrag“ → „laut Studienprotokoll“
  R7  4.7 Abs. 2: „nach der ersten Auswertung“ → „nach einer ersten Auswertung“
  S1  4.7: Absatz 4 (Sensitivität) und Absatz 5 (Voraussetzungen) getauscht (Nr. 54)
Nicht übernommen (Verfasser 20:51): Festlegungsdaten in 4.7 (kommen in Tab. H6), Nr. 30, 31, 57a.

Jede Ersetzung wirkt nur im Absatz, der den Suchtext trägt, und muss dort genau einmal greifen,
sonst bricht das Skript ab. Absatzeigenschaften und Runs außerhalb der Ersetzungen bleiben unverändert.
Aufruf: python Master_Schritt0_2026-09-26.py <Master.docx> <Ausgabe.docx> <Protokoll.txt>
Ohne Semikolon im Skript (chr(59)).
"""
import sys
import re
import zipfile
import hashlib

SRC, DST, LOG = sys.argv[1:4]
AUS = []


def log(*t):
    AUS.append(' '.join(str(x) for x in t))


def text(p):
    return ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', p))


def absaetze(xml):
    starts = [m.start() for m in re.finditer(r'<w:p(?=[ >])', xml)]
    return [(s, xml.find('</w:p>', s) + 6) for s in starts]


def finde(xml, kennung):
    treffer = [(s, e) for (s, e) in absaetze(xml) if kennung in text(xml[s:e])]
    if len(treffer) != 1:
        raise SystemExit('Absatz mit „%s“ %d-mal gefunden, erwartet 1' % (kennung, len(treffer)))
    return treffer[0]


def ersetze(xml, nr, kennung, alt, neu):
    s, e = finde(xml, kennung)
    p = xml[s:e]
    n = p.count(alt)
    if n != 1:
        raise SystemExit('%s: Suchtext %d-mal im Absatz, erwartet 1' % (nr, n))
    p2 = p.replace(alt, neu, 1)
    log(nr, 'ersetzt im Absatz „%s …“' % kennung[:40])
    log('   alt:', text(p))
    log('   neu:', text(p2))
    return xml[:s] + p2 + xml[e:]


ALT46_1 = ('Die Trainingsdurchführung der Interventionsgruppe wurde mit einem Online-Fragebogen (SoSci Survey) erhoben, '
           'der nach jeder Einheit auszufüllen war (Anhang A). Für die Kontrollgruppe sah der Ethikantrag kein Monitoring vor. '
           'Je Meldung wurden unter anderem Spielercode, Durchführungsstatus, Beanspruchung und Schmerzen erfasst. '
           'Erinnerungen erfolgten über die WhatsApp-Gruppen, ihre Häufigkeit wurde nicht protokolliert. '
           'Die Beanspruchung wurde nach der Session-RPE-Methode (sRPE) mit der CR-10-Skala erhoben (Foster et al., 2001). '
           'Die Methode gilt auch bei Jugendlichen als valide und reliabel (Haddad et al., 2017). '
           'Der sRPE-Load ist das Produkt aus CR-10-Wert und Solldauer der Einheit. Die Dauer wurde nicht individuell erfasst.')
NEU46_1 = ('Die Trainingsdurchführung wurde mit einem Online-Fragebogen (SoSci Survey) erhoben, '
           'der nach jeder Einheit auszufüllen war (Anhang A). Für die Kontrollgruppe sah der Ethikantrag kein Monitoring vor. '
           'Erfasst wurden unter anderem Spielercode, Durchführungsstatus, Beanspruchung und Schmerzen. '
           'Jedes Wochenvideo endete mit einer Karte zum Programmfortschritt. '
           'Erinnerungen erfolgten über die WhatsApp-Gruppen ohne protokollierte Häufigkeit. '
           'Die Beanspruchung wurde nach der Session-RPE-Methode (sRPE) mit der CR-10-Skala erhoben (Foster et al., 2001). '
           'Die Methode gilt auch bei Jugendlichen als valide und reliabel (Haddad et al., 2017). '
           'Der sRPE-Load ist das Produkt aus CR-10-Wert und Solldauer der Einheit. Die Dauer wurde nicht individuell erfasst.')
ALT46_2 = ('Adhärenz ist die Zahl der Meldungen mit dem Status „ganz“ je Spieler bei zwölf angebotenen Einheiten. '
           'Gezählt wurde je Meldung. Die gemeldete Einheitennummer diente nicht als Identitätsmerkmal. '
           'Meldungen mit dem Status „teilweise“ zählten gesondert als Beteiligung. '
           'Der Ethikantrag legte ein Analysekriterium von mindestens 75 % fest. '
           'Die Compliance, die protokollgetreue Übungsausführung, war im unbeaufsichtigten Heimsetting nicht objektiv überprüfbar.')
NEU46_2 = ('Adhärenz ist die Zahl der Meldungen mit dem Status „ganz“ je Spieler bei zwölf angebotenen Einheiten. '
           'Gezählt wurde je Meldung. Die Einheitennummer diente nicht als Identitätsmerkmal. '
           'Meldungen mit dem Status „teilweise“ zählten gesondert als Beteiligung. '
           'Der Ethikantrag legte ein Adhärenzkriterium von mindestens 75 % fest. '
           'Die Compliance, die protokollgetreue Übungsausführung, war im unbeaufsichtigten Heimsetting nicht objektiv überprüfbar.')

zin = zipfile.ZipFile(SRC)
teile = [(i, zin.read(i.filename)) for i in zin.infolist()]
xml = zin.read('word/document.xml').decode('utf-8')
if 'word/comments.xml' in zin.namelist():
    raise SystemExit('comments.xml vorhanden, Kommentaranker müssten erhalten werden. Abbruch.')
n_vorher = len(absaetze(xml))
log('Eingang', SRC, 'SHA-256', hashlib.sha256(open(SRC, 'rb').read()).hexdigest())
log('Absätze vorher', n_vorher, '· keine comments.xml')

xml = ersetze(xml, 'R1 (4.1, Nr. 21)', 'Die Studie wurde als studentische Qualifikationsarbeit nicht registriert',
              'Das Adhärenzkriterium wurde nach Sichtung der Adhärenz- und Abschlusswerte der Interventionsgruppe und vor Kenntnis der Kontrollgruppenwerte angepasst.',
              'Das Adhärenzkriterium wurde in der Hauptanalyse nicht angewandt.')
xml = ersetze(xml, 'R2 (4.4.2, Nr. 22)', 'Die Richtungswechselleistung wurde mit dem 505-Test',
              'Ein Asymmetrie-Index wurde nicht berechnet</w:t>',
              'Ein Asymmetrie-Index wurde nicht berechnet.</w:t>')
xml = ersetze(xml, 'R3 (4.6 Abs. 1, B1)', 'Die Trainingsdurchführung der Interventionsgruppe', ALT46_1, NEU46_1)
xml = ersetze(xml, 'R4 (4.6 Abs. 2, B1 und Nr. 20)', 'Adhärenz ist die Zahl der Meldungen', ALT46_2, NEU46_2)
xml = ersetze(xml, 'R5 (4.7 Abs. 1, S. 17)', 'Die Hauptanalyse umfasste unabhängig von der Adhärenz',
              '<w:r w:rsidR="009C3A31"><w:t xml:space="preserve"> 7</w:t></w:r>',
              '<w:r w:rsidR="009C3A31"><w:t xml:space="preserve"> 17</w:t></w:r>')
xml = ersetze(xml, 'R6 (4.7 Abs. 1, Studienprotokoll)', 'Die Hauptanalyse umfasste unabhängig von der Adhärenz',
              '505-Seitenwerte nach Antrag sowie', '505-Seitenwerte laut Studienprotokoll sowie')
xml = ersetze(xml, 'R7 (4.7 Abs. 2, einer)', 'Eine A-priori-Poweranalyse (f = 0,25)',
              'festgelegt nach der ersten Auswertung', 'festgelegt nach einer ersten Auswertung')

# S1: Tausch der beiden 4.7-Absätze (Sensitivität vor Voraussetzungen → Voraussetzungen vor Sensitivität)
s4, e4 = finde(xml, 'Sechs vorab festgelegte Sensitivitätsanalysen')
s5, e5 = finde(xml, 'Um Verletzungen der Modellannahmen zu erkennen')
if e4 != s5:
    raise SystemExit('S1: Absätze nicht unmittelbar aufeinanderfolgend')
xml = xml[:s4] + xml[s5:e5] + xml[s4:e4] + xml[e5:]
log('S1 (4.7, Nr. 54): Voraussetzungsabsatz vor Sensitivitätsabsatz gestellt')

n_nachher = len(absaetze(xml))
if n_nachher != n_vorher:
    raise SystemExit('Absatzzahl geändert: %d → %d' % (n_vorher, n_nachher))
log('Absätze nachher', n_nachher)

with zipfile.ZipFile(DST, 'w') as zout:
    for info, daten in teile:
        if info.filename == 'word/document.xml':
            daten = xml.encode('utf-8')
        zout.writestr(info, daten, compress_type=zipfile.ZIP_DEFLATED)
log('Ausgang', DST, 'SHA-256', hashlib.sha256(open(DST, 'rb').read()).hexdigest())

with open(LOG, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(AUS) + '\n')
print('\n'.join(AUS))

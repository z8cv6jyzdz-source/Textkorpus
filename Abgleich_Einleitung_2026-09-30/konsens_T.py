# -*- coding: utf-8 -*-
# Konsens: Codierung A mit den Entscheidungen zu allen 13 Abweichungen (1 Primärcode, 12 nur Sekundärcodes), Begründung je Satz
from codes_A_T import A
ENTSCHEID = {
 ('B1a', 4): ('E3', '', 'A: Die Testnamen sind Ort des Befunds, keine Aussage über Konstrukt oder Güte (Codebuch: Funktion, nicht Thema einzelner Wörter). D1 von B nicht übernommen'),
 ('B1a', 6): ('K3', 'L1', 'B: „eine Mindestdauer lässt sich daraus nicht ableiten“ ist eine Beschränkung vorhandener Studien (Codebuch L1)'),
 ('B1b', 1): ('T2', '', 'B: Eingeführt ist das Trainingsmittel in B1a S3 (Regel 1), der Satz nennt den Wirkmechanismus'),
 ('B2', 1): ('K2', 'R3', 'B: Die Unterbrechung des Mannschaftstrainings ist die Lage, auf die die Studie antwortet (Codebuch R3)'),
 ('B2', 2): ('T4', 'K2', 'B: Primär eine Gestaltungsanforderung an Trainingsangebote (Codebuch T4), das Setting liefert den Grund („daher“). Einzige Abweichung beim Primärcode'),
 ('B2', 9): ('R3', 'E2;E3', 'A: konkret beschriebene Primärstudie (Codebuch E2, Korpus Padrón-Cabo 3.3 R3 mit E2), die Winterpause ist Rahmen, K2 steht schon in B2 S1'),
 ('B2', 10): ('E3', 'R3', 'A: „Im Kindes- und Jugendalter“ begrenzt den Geltungsbereich, der Moderator trägt die Aussage nicht (Regel 5)'),
 ('B2', 11): ('K2', 'R3;L2', 'B: „nicht zwangsläufig zu einem Leistungsverlust“ trägt das Problem (Codebuch R3)'),
 ('B4', 2): ('K1', 'T2', 'B: Die Aussage bindet die Reifung an den DVZ, den Wirkmechanismus des Trainingsmittels (Codebuch T2)'),
 ('B4', 3): ('K1', '', 'A: allgemeine methodische Folgerung, keine angekündigte eigene Designentscheidung (Codebuch Z2), das Design steht in B5 S2'),
 ('B4', 5): ('L1', 'K1;K4', 'B: drei Moderatoren tragen den Satz, bei höchstens zwei Sekundärcodes nach Satzfolge. K2 (Übergangsperiode) steht in der Lückenanalyse nach Anhang C'),
 ('B4', 6): ('L1', 'K2;K4', 'B: Die Dimensionen der Lücke tragen den Satz, wie im Korpus Beato 4.2 (L1 mit K2, K4), Sammoud 2.9 und Moran 3.2 (L1 mit K4)'),
 ('B5', 1): ('Z1', '', 'A: Im Korpus stehen Zwecksätze mit „Therefore“ oder „Thus“ ohne L1, L1 nur mit Lückeninhalt im Satz (Moran 3.4, Hilska 4.1, Asimakidis 5.1). Regel 4 greift nicht'),
}
K = {k: [(p, s) for p, s in v] for k, v in A.items()}
for (blk, n), (p, s, why) in ENTSCHEID.items():
    K[blk][n - 1] = (p, s)

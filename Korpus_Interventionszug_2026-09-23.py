#!/usr/bin/env python3
# Korpus_Interventionszug_2026-09-23.py — Wortzahl des Interventions-Zugs in den zehn Interventionsstudien des Vergleichskorpus
# Zweck: Umfangsmaßstab für Abschnitt 4.5.1 Plyometrisches Heimtrainingsprogramm (Uebergabe_4.5.1_Heimtrainingsprogramm_2026-09-23.md § 5).
# Verfahren wie Korpus_Designzug_2026-09-22.py: pdftotext der Volltexte in `Ideen und Studien`, Sätze von Hand ausgewählt.
# Interventions-Zug (I) je Studie: Sätze der Methodik, die die EXPERIMENTELLE Intervention tragen — Rahmen (Zeitraum, Frequenz,
#   Einbettung, Abstand), Erwärmung der Trainingseinheit, Übungsauswahl, Progression (Sätze, Wiederholungen, Kontakte), Pausen,
#   Intensitätsinstruktion, Betreuung/Auslieferung, Ort/Untergrund, Normbezug (= Inhalt unseres 4.5.1, TIDieR 1–10).
# Getrennt gezählt: Kontroll-/Begleitbedingung (K, = unser 4.5.2) und Belastungsmonitoring (M, = unser 4.6).
# Nicht gezählt: Design/Zuteilung (Design-Zug), Tests, Ethik, Stichprobe, Tabelleninhalte, Seitenzubehör.
# Zweispaltige Layouts (Lloyd 2016) wurden an der layouttreuen pdftotext-Fassung rekonstruiert.
# Grenze: regelbasierte Näherung ± wenige Sätze je Studie; Wortzahl = Leerzeichen-Token.
# Ausgabe: Korpus_Interventionszug_2026-09-23.txt. Erstellt in Cowork, 23.09.2026.
import statistics

S = {
'Lloyd 2016 (JSCR)': {
 'I': [
  "Training took place twice per week for 6 weeks, and training sessions were designed and implemented by a fully accredited strength and conditioning coach.",
  "Training sessions were separated by at least 48 hours to enable full recovery.",
  "If participants were unable to competently perform any given exercise, relevant exercise regressions were prescribed on an individual basis.",
  "Within all training programs, training sessions lasted no longer than 60 minutes and prescribed inter-set rest periods ranged between 1 and 2 minutes dependent on the relative intensity of the exercise, an approach that is commensurate with recommended guidelines for youth resistance training (21).",
  "Plyometric Training Group. Plyometric training prescription included a combination of exercises that were geared toward developing both safe jumping and landing mechanics (e.g., drop landings, vertical jumps in place, single-leg forward hop and stick) and also to stress stretch-shortening cycle activity (e.g., pogo hopping, drop jumps, multiple horizontal rebounds).",
  "Within each session, participants were exposed to multiple sets of 4 exercises to enable sufficient repetition to develop motor control programs.",
  "The plyometric training program (Table 2) was progressed conservatively according to number of foot contacts completed within each session (week 1 foot contacts = 74 per session, week 6 foot contacts = 88 per session)."],
 'K': [
  "Throughout the intervention period, the control group received games-based physical education lessons commensurate with the requirements of the United Kingdom national curriculum.",
  "The principal investigator was not present during the physical education classes of the control group."],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche)'},
'Hammami 2016 (JSCR)': {
 'I': [
  "Details of the added plyometric training are given in Table 2.",
  "Sessions were always supervised by the same coach, who was a part of the research team.",
  "Verbal encouragement was given to ensure a high level of motivation throughout.",
  "Every Tuesday and Thursday for 8 weeks, the experimental subjects replaced a part of their standard regimen with plyometric training.",
  "Standard sessions began with a 15-minute warm-up and lasted for 20 minutes.",
  "Plyometric sessions began from rest with a 15-minute warm-up and they also lasted for some 20 minutes.",
  "Jumps were performed on a tartan track.",
  "Subjects were instructed to perform all jumps to the maximal possible height with minimal ground contact time.",
  "Both hurdle and drop jumps were performed with small angular knee movements; the ground was touched with the balls of the feet only, thereby specifically stressing the calf muscles (25).",
  "Hurdling comprised 7 to 10 continuous jumps over hurdles spaced at intervals of 1 m.",
  "Each set of drop jumps comprised 7 to 10 maximal rebounds after dropping from a 0.6-m to 0.7-m box, with a pause of 5 seconds between each rebound (25)."],
 'K': [
  "All subjects avoided any training other than that associated with the soccer team throughout the study.",
  "Before the competitive season (August), all subjects had already engaged in 7 training sessions per week for 2 months and had undertaken a light resistance training program for both the upper and the lower limbs (twice weekly sessions with exercises that used the body weight as a resistance).",
  "During the first part of the competitive season (September to December), subjects continued to train 4 to 5 times a week, participated in one official soccer match every Sunday, and undertook a supplementary resistance training session with light loads 3 times per month.",
  "During the second phase of the national championship (January to March), the same routine was maintained, except that the experimental group replaced their supplementary resistance training sessions with the plyometric program.",
  "All participants also engaged in a once weekly school physical education session; this lasted for 40 minutes and consisted mainly of ball games.",
  "All players thus began the trial in a well-trained state, although none had previously engaged in a regular soccer-specific plyometric training program."],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche)'},
'Beato 2018 (JSCR)': {
 'I': [
  "COD-G performed 2 times per week a protocol of short shuttle runs and sprints with COD with different angles such as 45°, 90° and 180°.",
  "In detail, they performed 3/4 sets of 3 short shuttle runs with 4 COD each, for an amount of 36 COD and 48 COD on Monday and Wednesday, respectively.",
  "CODJ-G performed the same number and type of COD but combined with a specific plyometric training (36 COD and 60 jumps) and 48 COD on Monday and Wednesday, respectively.",
  "COD ability refers (in this protocol) to a movement where no immediate reaction to a stimulus is required, so the direction change is pre-planned, while agility requires external and perceived stimuli prior to any direction change (3,15,29).",
  "Plyometric training consisted of 4 x 5 drop jumps from 60 cm high followed by a subsequent jump over an obstacle (15 cm height), as well as 4 x 5 jumps over obstacles of 15 cm height.",
  "Authors manipulated the two training protocols a priori, where COD-G performed a specific training that only involved COD (twice a week), while CODJ-G performed the same amount of COD with an additional plyometric volume (COD and plyometric training twice and once a week, respectively).",
  "Therefore, CODJ-G performed a higher training volume than COD-G in this study.",
  "Every training session was preceded with a 20-minutes standardized warm-up composed by aerobic running, dynamic stretching, as well as technical exercises.",
  "All the training sessions were performed at the same time (3.00 pm).",
  "Researchers asked both groups to maintain their normal lifestyle and nutrition behaviors throughout the duration of the protocol."],
 'K': [
  "During this study, the team performed 4 training session a week as team practices as well as an official match every Saturday, while Sunday was a day off."],
 'M': [
  "Internal training load was evaluated by ratings of perceived exertions (RPE-10) after all the training sessions to evaluate possible differences in training load (2)."],
 'tabelle': 'keine Programmtabelle (Dosis im Text)'},
'Negra 2019 (IJSPP)': {
 'I': [
  "The two experimental groups participated in an 8-week in-season PJT program consisting of two training sessions per week.",
  "Overall, the UPJT and LPJT groups conducted five regular soccer training sessions per week.",
  "The PJT was integrated into the regular training routine of the soccer team, replacing some soccer-specific drills.",
  "The inter-day rest interval between plyometric training sessions was at least 72 h.",
  "A standardised warm-up of 8 to 12-min duration was completed.",
  "It included low intensity running, coordination exercises, dynamic movements, sprints, and dynamic stretching for the lower limb muscles prior to each PJT session.",
  "Soccer training sessions lasted between 80 and 90-min.",
  "The LPJT and UPJT drills lasted between 20 and 25-min.",
  "The remaining training time was dedicated to technical and tactical drills.",
  "The first training session was performed at least 48 hours after the soccer match that was scheduled on the weekend.",
  "The LPJT and UPJT protocols were based on that of a previously published study 21.",
  "Details of the respective protocols are illustrated in Table 2.",
  "The PJT (i.e., LPJT, UPJT) included vertical (i.e., CMJs) and horizontal (i.e., bilateral forward ankle hops) jumps performed at maximal effort (i.e., maximal height and forward distance with a minimal contact time for vertical and horizontal jumping, respectively).",
  "Both groups performed cyclic jumps using an arm-swing.",
  "According to previous studies, 8,22 training volume was progressively increased throughout the 8-week intervention period.",
  "While participants of the UPJT group performed all jump exercises using no additional loads, participants in the LPJT group executed the same exercises using weighted vests (8% participants' body mass)15.",
  "Both sessions consisted of a volume of 4-6 sets and 6-10 repetitions.",
  "The total number of ground contacts per session was 50 during the first week and gradually increased to 120 after eight weeks of training.",
  "A 90-s rest was provided between each set of each exercise.",
  "The jump training protocols were supervised by a qualified instructor."],
 'K': [],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche)'},
'Negra 2020 (JSHS)': {
 'I': [
  "Both RT and PT sessions lasted 35-40 min.",
  "The second RT and PT session was completed 72 h after the first.",
  "In total, 24 sessions were devoted for each training program.",
  "The PT program was based on recommendations of intensity and volume from Söhnlein et al.8",
  "In brief, every first PT session in each week was focused on improving the vertical-horizontal leap, whereas every second session was focused on improving the lateral jumping ability.",
  "To ensure an appropriate training intensity for players and to limit stress on musculotendinous units, the training volume and intensity were progressively increased.",
  "The total number of ground contacts per week started at 112 during the first week and increased to 280 after 12 weeks.",
  "Plyometric exercises were executed at maximal intensity.",
  "Furthermore, all PT sessions were completed on an artificial turf pitch to minimize first landing impact and to be as soccer-specific as possible.",
  "During every vertical-horizontal PT session, the following jumps were performed: 2-footed ankle hop forward, hurdle jumps, and squat jump.",
  "During every lateral PT session, the following jumps were performed: lateral bound stabilization, lateral hurdle jumps, and double-leg zigzag.",
  "No drill lasted more than 10 s to ensure that muscular energy was mainly produced by intramuscular phosphagen degradation, and a 90-s rest period was provided between each set of exercises to allow for the resynthesis of phosphagens.5"],
 'K': [
  "In 2 sessions per week, the regular soccer training was replaced for the RTG and the PTG.",
  "The CG continued its regular soccer training."],
 'M': [],
 'tabelle': 'keine Programmtabelle (Dosis im Text)'},
'Aloui 2022 (Front Physiol)': {
 'I': [
  "The training group undertook four sessions or workshops, biweekly (Figure 1).",
  "Workshops commenced with plyometric exercises (i.e., hurdle jumps, lateral hurdle jumps, bouncy strides, and single-leg hop jumps) and ended with a short sprint of 10-15 m (Table 2).",
  "The total number of ground contacts per session was gradually increased throughout the intervention (from 72 to 144 ground contacts per session), as well as the number of sets (from 3 to 6 sets) for each workshop.",
  "The number of contacts per set was maintained at 6 contacts.",
  "A 90-s rest interval was planned between each set of exercises to allow sufficient recovery time (Negra et al., 2016).",
  "Jump training protocols were supervised by a qualified instructor.",
  "The training protocol was based on previously published recommendations for training volume and intensity from the study by Bedoya et al. (2015).",
  "Furthermore, the sprint training protocol was based on previously published recommendations for sprint distances (Sáez de Villarreal et al., 2015; Kargarfard et al., 2020)."],
 'K': [
  "Both groups undertook five training sessions per week (~90 min each session), plus a competitive match one time per week.",
  "Conditioning training was completed two times per week, with the first session developing aerobic fitness through small-sided games while the second session targeted anaerobic fitness with resistance (40-60% 1 RM).",
  "The controls maintained their normal training schedule throughout the 2 months of the intervention, whereas the EG replaced the technical-tactical part of their standard regimen by combined plyometric and short sprint training.",
  "Participants also engaged in the 60-min school physical education sessions weekly (Table 1)."],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche) + Figure 1 (Übungen)'},
'Liu 2024 (JSSM)': {
 'I': [
  "Each intervention group participated in two training sessions per week for three consecutive weeks, totaling six sessions throughout the intervention period.",
  "These sessions were conducted in small groups throughout the day, to accommodate the participants' availability.",
  "There was a 48-hour rest period between each training session.",
  "The HIIT sessions took place on the track field (straight line running), while the PJT sessions were conducted on a concrete floor.",
  "For HIIT, training intensity was standardized based on the results of the 30-15 Intermittent Fitness Test, which was administered the week prior to the start of the intervention solely to individualize training intensity for each player.",
  "In the case of PJT, players were instructed to perform each repetition at maximal intensity.",
  "Prior to each training session, all intervention groups (i.e., HIIT, PJT, and HIIT+PJT) completed a 7-minute warm-up protocol consisting of 4 minutes of jogging and 3 minutes of dynamic stretching focusing on the lower limbs.",
  "Following the warm-up, participants performed the training exercises as described in Table 2.",
  "These sessions were supervised and guided by two personal physical trainers with expertise in fitness training and backgrounds in sports sciences and physical education."],
 'K': [
  "The control group maintained their regular routines during the training cessation period.",
  "None of the participants engaged in any supplementary training."],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche)'},
'Moran 2024 (PLOS ONE)': {
 'I': [
  "The training intervention was carried out over a period of eight weeks, the composition of which can be seen in Table 1.",
  "The exercises were chosen on the basis of their directional orientation according to the principle of training specificity.",
  "The approach was based on previous meta-analysis [5] that supported the superiority of HPT but recommended further comparison with VPT and especially a combination of both, over a period of longer than seven weeks.",
  "The specific training parameters followed those recommended for soccer players by Ramirez-Campillo et al. spanning a period of more than seven weeks, incorporating two sessions per week, and a volume of 140–240 jumps per week (200 jumps were executed weekly).",
  "Based on those recommendations, the jumps were performed with maximal effort, utilising correct technique and a rest interval that exceeded 30 seconds between sets being observed (60 to 90 seconds was used).",
  "Additionally, recovery between sessions was around 48 hours.",
  "The training intervention was executed on Thursdays and Saturdays.",
  "On Thursday, following a comprehensive warm-up, players were divided into three groups and performed the PT research protocol simultaneously.",
  "Saturday, once again after a warm up, each group performed the PT protocol.",
  "All sessions for all of the experimental groups were overseen and supervised by a strength and conditioning coach who provided extensive direction on the performance of the exercises and controlled the application of the training load."],
 'K': [
  "The players undertook six training sessions in total each week.",
  "The day after a match, which occurred on a Monday, the players rested while those who played less than 70 minutes engaged in high-intensity interval training and small-sided games.",
  "On Wednesday, all players participated in a recovery session.",
  "After carrying out the PT, the players jointly participated in a soccer training session which included technical and tactical exercises.",
  "On Friday, the players jointly participated in further technical and physical training.",
  "On Sunday, an activation protocol was carried out by all players."],
 'M': [],
 'tabelle': 'Table 1 (Programm je Woche)'},
'Sammoud 2024 (BMC)': {
 'I': [
  "The PJT program was implemented during the second half of the in-season period, specifically in February and March of 2022.",
  "For both groups, a standardized warm-up lasting 8 to 12 min was conducted prior to each training session.",
  "This warm-up included activities such as low-intensity running, coordination exercises, dynamic movements (e.g., lunges, skips), sprints, and dynamic stretching targeting the muscles of the lower limbs.",
  "At the start of each training week, the first PJT session was scheduled at least 48 h after the last soccer match that took place over the weekend.",
  "The second PJT session was conducted 72 h after the first session, specifically on Tuesdays and Thursdays.",
  "The PJT drills were incorporated at the beginning of the regular soccer training sessions.",
  "The specific details of the PJT protocol can be found in the attached table (Table 2).",
  "The total ground contacts per week gradually increased from 50 during the first week to 120 during the last week of training [29, 30].",
  "Each PJT session included vertical (i.e., CMJs) and horizontal (i.e., two-footed ankles hop forward and double leg zigzag) jumps performed at a maximal intensity (i.e., maximal height and forward distance with a minimum contact time for vertical and horizontal jumping, respectively).",
  "During the first four weeks, all vertical and horizontal jumping was executed bilaterally whereas, during the last four weeks, horizontal jumping was performed bilaterally and unilaterally [29].",
  "The same order of the PJT exercises was maintained during the 8 weeks: CMJ, CMJ-akimbo, two footed ankles hop forward and double leg zigzag jumps.",
  "In addition, as indicated in Table 1, the number of foot ground contacts fluctuated within the training program, ranging from 50 to 120 contacts per session, thereby affecting the number of sets and repetitions per set.",
  "To allow sufficient rest, a 90-s was provided between each set of exercises."],
 'K': [
  "The active CG participated in a regular soccer-specific training program over the 8-week intervention period with 5 training sessions per week lasting between 80 and 90 min.",
  "The PJT group participated in 3 soccer-specific training sessions per week that were similar to those of the CG, and the 2 PJT sessions substituted 2 soccer-specific training sessions so that the overall exposition time to training was identical between the 2 groups.",
  "In general, soccer training included training in fast footwork, technical skills and moves, position games, and tactical games."],
 'M': [],
 'tabelle': 'Table 2 (Programm je Woche)'},
'Bouafif 2026 (PLOS ONE)': {
 'I': [
  "The plyometric programs were designed in accordance with the long-term athletic development prescription strategies proposed by Granacher et al. [7] and were implemented during the 2023 in-season period (February–March).",
  "Both pre- and post-PHV groups completed an 8-week in-season program consisting of two sessions per week, in addition to their regular soccer training, which primarily focused on developing sport-specific technical and tactical skills.",
  "Plyometric training was integrated within the players' regular 90-minute soccer sessions and conducted twice weekly, constituting a form of concurrent training in which neuromuscular (plyometric) and technical–tactical (soccer-specific) stimuli are combined within the same training cycle.",
  "This structure reflects the ecological conditions of youth soccer and aligns with evidence showing that concurrent training can promote complementary gains in neuromuscular power and endurance when appropriately sequenced and monitored [26,27].",
  "Each session began with a standardized 10-minute dynamic warm-up that included submaximal running, dynamic stretching, multidirectional low-intensity movements (forward, sideways, backward), acceleration runs, and preparatory jumps.",
  "Following the warm-up, athletes in the intervention groups performed plyometric exercises characterized by fast and explosive stretch–shortening cycle (SSC) actions, minimal ground contact times, and progressive overload, as described by Davies et al. [28].",
  "The plyometric protocol, adapted from Bogdanis et al. [29] and in line with youth training guidelines [26,27], included six lower-limb exercises per session targeting both vertical and horizontal force production (bilateral and unilateral 20-cm drop jumps, standing long jumps, and lateral bounds).",
  "Exercises were performed bilaterally and unilaterally, as appropriate, with ground contact times kept below 250 ms for all fast SSC drills, verified by coach observation and auditory feedback.",
  "Proper landing control and jump height were emphasized to ensure effective SSC utilization and safe mechanics.",
  "Training intensity and progression followed a progressive overload model, increasing the number of foot contacts (from 54 to 120 per session across the 8 weeks), jump height (from 20 to 30 cm for drop jumps), and task complexity (from bilateral to unilateral and multidirectional movements).",
  "Athletes performed 3–4 sets of 5–10 repetitions per exercise, with 30–60 seconds of rest between sets (Table 2).",
  "Each repetition was executed at maximal voluntary effort, emphasizing explosive take-off and minimal ground contact time.",
  "After completing the plyometric or passing component, all players continued with 60 minutes of identical soccer-specific training (30 minutes of technical–tactical drills and 30 minutes of small-sided games), followed by a 5-minute cooldown.",
  "All sessions were supervised by two qualified strength and conditioning specialists who provided real-time feedback on technique, posture, landing mechanics, and intensity to ensure safe execution and adherence to correct plyometric principles throughout the intervention."],
 'K': [
  "The control groups performed a matched-duration passing drill.",
  "The control groups performed passing drills (e.g., two-touch triangle and square patterns, low-driven passes) for the same duration as the plyometric component (Table 3).",
  "These drills were designed to maintain moderate cardiovascular demand (heart rates: 120–140 bpm), ensuring similar overall physiological load to the plyometric sessions.",
  "Consequently, total training exposure, duration, and internal load were matched across groups, minimizing potential confounding effects related to unequal workload."],
 'M': [
  "To address potential differences in total training load between groups, both internal and external loads were carefully monitored.",
  "The session rating of perceived exertion (sRPE) method (Foster et al., 2001) was used after each session to quantify internal load.",
  "The duration and structure of the plyometric and control sessions were matched (~25 minutes).",
  "External load in the experimental groups was further tracked by recording the total number of jump contacts per session and progression across weeks.",
  "No significant between-group differences in total session RPE were observed, indicating comparable perceived effort across training modalities."],
 'tabelle': 'Table 2 (Progression je Woche) + Table 3 (Einheitenaufbau)'},
}

def w(lst): return sum(len(s.split()) for s in lst)

lines = []
lines.append("Korpusmessung Interventions-Zug — zehn Interventionsstudien des Vergleichskorpus (Stand 23.09.2026)")
lines.append("Spalten: I = Interventionsbeschreibung (unser 4.5.1) · K = Kontroll-/Begleitbedingung (unser 4.5.2) · M = Belastungsmonitoring im Interventionsabsatz (unser 4.6) · Belege = Klammer-/Nummernbelege in I")
lines.append("")
lines.append(f"{'Studie':<28}{'Sätze I':>8}{'Wörter I':>10}{'Wörter K':>10}{'Wörter M':>10}  Programmtabelle")
I_vals, K_vals = [], []
import re
for name, d in S.items():
    wi, wk, wm = w(d['I']), w(d['K']), w(d['M'])
    I_vals.append(wi); K_vals.append(wk)
    lines.append(f"{name:<28}{len(d['I']):>8}{wi:>10}{wk:>10}{wm:>10}  {d['tabelle']}")
lines.append("")
lines.append(f"I: Median {statistics.median(I_vals):.0f} · Mittel {statistics.mean(I_vals):.0f} · Min {min(I_vals)} · Max {max(I_vals)} · SD {statistics.stdev(I_vals):.0f}")
lines.append(f"K: Median {statistics.median(K_vals):.0f} · Mittel {statistics.mean(K_vals):.0f} · Min {min(K_vals)} · Max {max(K_vals)}")
lines.append(f"Programmtabelle vorhanden: {sum(1 for d in S.values() if not d['tabelle'].startswith('keine'))} von {len(S)}")
# Belegdichte im Interventions-Zug (Belege von Hand am Wortlaut gezählt: Klammerzitat Autor-Jahr oder Nummernbeleg je Vorkommen)
belege = {'Lloyd 2016 (JSCR)': 1, 'Hammami 2016 (JSCR)': 2, 'Beato 2018 (JSCR)': 1, 'Negra 2019 (IJSPP)': 3, 'Negra 2020 (JSHS)': 2,
          'Aloui 2022 (Front Physiol)': 3, 'Liu 2024 (JSSM)': 0, 'Moran 2024 (PLOS ONE)': 2, 'Sammoud 2024 (BMC)': 2, 'Bouafif 2026 (PLOS ONE)': 5}
lines.append("")
lines.append("Belege im Interventions-Zug (von Hand gezählt; Wörter je Beleg):")
dens = []
for name, d in S.items():
    b = belege[name]; wi = w(d['I'])
    dens.append(wi / b if b else float('inf'))
    lines.append(f"  {name:<28} Belege {b} · Wörter {wi} · Wörter je Beleg {wi/b if b else float('nan'):.0f}")
lines.append(f"  Median Belege je Studie: {statistics.median(belege.values()):.0f} · Spanne 0–5 · Wörter je Beleg (Studien mit Beleg): Median {statistics.median([x for x in dens if x != float('inf')]):.0f}")
# Züge je Studie (Inhaltsanalyse, von Hand)
lines.append("")
lines.append("Züge im Interventions-Zug (von Hand am Wortlaut geprüft; x = im Fließtext vorhanden):")
zuege = {
 'Zeitraum/Frequenz/Dauer':   ['x','x','x','x','x','x','x','x','x','x'],
 'Abstand zwischen Einheiten':['x','-','-','x','x','-','x','x','x','-'],
 'Erwärmung der Einheit':     ['-','x','x','x','-','-','x','x','x','x'],
 'Übungen benannt':           ['x','x','x','x','x','x','-','-','x','x'],
 'Kontakte/Volumen je Einheit':['x','x','x','x','x','x','-','x','x','x'],
 'Sätze × Wiederholungen':    ['-','x','x','x','-','x','-','-','-','x'],
 'Satzpause':                 ['x','x','-','x','x','x','-','x','x','x'],
 'Intensitätsinstruktion':    ['-','x','-','x','x','-','x','x','x','x'],
 'Betreuung/Auslieferung':    ['x','x','-','x','x','x','x','x','-','x'],
 'Ort/Untergrund':            ['-','x','-','-','x','-','x','-','-','-'],
 'Programmvorlage/Norm belegt':['x','x','-','x','x','x','-','x','x','x'],
 'Regression/Individualisierung':['x','-','-','-','-','-','-','-','-','-'],
 'Modifikationen/Abweichungen genannt':['-','-','-','-','-','-','-','-','-','-'],
}
names = list(S.keys())
lines.append("  " + "Zug".ljust(36) + "  ".join(n.split()[0][:6].ljust(6) for n in names) + "  Summe")
for z, v in zuege.items():
    lines.append("  " + z.ljust(36) + "  ".join(x.ljust(6) for x in v) + f"  {v.count('x')}/10")
out = "\n".join(lines)
print(out)
open("Korpus_Interventionszug_2026-09-23.txt", "w", encoding="utf-8").write(out + "\n")

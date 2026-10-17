"""Original lecture-based questions; five distinct choices with teaching rationales."""
from pathlib import Path
import json,random
R=Path(__file__).parent
questions=[];pools={}
def pool(name,text): pools[name]=dict(l.split('~',1) for l in text.strip().splitlines())
def block(deck,topic,pname,text):
 for line in text.strip().splitlines():
  refs,stem,answer,why,*fig=line.split('|');pages=[int(p) for p in refs.split(',')]
  excluded={answer}
  if pname=='ocularDrug':
   # Do not use another equally correct member of a shared-mechanism class as a distractor.
   for group in [{'Brimonidine','Apraclonidine'},{'Acetazolamide','Dorzolamide','Brinzolamide'},{'Latanoprost','Bimatoprost'},{'Pilocarpine','Carbachol'}]:
    if answer in group: excluded|=group
  rng=random.Random(71000+len(questions));wrong=[(a,w) for a,w in pools[pname].items() if a not in excluded];rng.shuffle(wrong)
  opts=[dict(text=answer,why=why,correct=True)]+[dict(text=a,why=w,correct=False) for a,w in wrong[:4]]
  assert len(opts)==5
  rng.shuffle(opts);ans=next(i for i,o in enumerate(opts) if o.pop('correct'))
  for o in opts:o.pop('correct',None)
  questions.append(dict(id=f'Q{len(questions)+1:03}',deck=deck,topic=topic,pages=pages,page=pages[0],ref=f'slide-{deck}-{pages[0]}',stem=stem,options=opts,answer=ans,image=fig[0]+'.jpg' if fig else None))
def custom(deck,topic,refs,stem,options,fig=None):
 entries=[s.split('~',1) for s in options];pn='custom'+str(len(questions));pools[pn]=dict(entries[1:]);block(deck,topic,pn,refs+'|'+stem+'|'+entries[0][0]+'|'+entries[0][1]+('|' + fig if fig else ''))

pool('hearingDx','''Otitis media with effusion~Middle-ear fluid causes conductive loss and often an amber or dull tympanic membrane; it does not primarily damage the cochlear nerve.
Cerumen impaction~Obstructing wax causes conductive loss in the external canal; a normal canal with inner-ear deficits needs another explanation.
Otosclerosis~Stapes fixation impairs sound transmission and causes conductive or mixed loss, often with a relatively normal tympanic membrane.
Cholesteatoma~Keratinizing squamous tissue in the middle ear can erode ossicles and cause conductive loss, retraction debris, and chronic drainage.
Tympanic membrane perforation~A hole in the eardrum impairs mechanical transmission and can cause conductive loss; its appearance differs from an intact effusion-filled drum.
Presbycusis~Age-related loss is usually bilateral symmetric high-frequency sensorineural loss with impaired speech understanding, particularly in noise.
Noise-induced hearing loss~Chronic acoustic injury commonly produces a 3–6 kHz notch, often near 4 kHz, rather than a flat conductive air-bone gap.
Sudden sensorineural hearing loss~Abrupt inner-ear or neural hearing decline over hours to days requires urgent audiometric and otologic assessment; gradual loss has a different time course.
Vestibular schwannoma~A vestibular nerve Schwann-cell tumor can cause progressive asymmetric SNHL, unilateral tinnitus, and imbalance; MRI of the internal auditory canals evaluates it.
Connexin-26-related hearing loss~GJB2 variants can cause congenital nonsyndromic sensorineural loss, often recessive and present without a known family history.
Ototoxic cochlear injury~Aminoglycosides, cisplatin, loop diuretics, and salicylates can impair inner-ear function; reversibility and target vary by agent.
Congenital aural atresia~External canal malformation impairs sound conduction; it is not equivalent to congenital destruction of cochlear sensory cells.''')
block('av','Hearing disorder diagnosis','hearingDx','''3,4|A 3-year-old has recurrent ear infections and persistent amber-colored eardrums between episodes. Audiometry shows an air-bone gap. Which process best explains the persistent hearing deficit?|Otitis media with effusion|Residual middle-ear fluid restricts tympanic membrane and ossicular motion, causing conductive hearing loss. Tympanostomy can restore ventilation in appropriately selected children.|figure-effusion
6,7|An infant fails newborn hearing screening and has bilateral profound SNHL on ABR. Testing identifies biallelic GJB2 variants. There is no family history. What is the most likely diagnosis?|Connexin-26-related hearing loss|GJB2 encodes connexin 26, a gap-junction protein important for cochlear ion homeostasis. Recessive inheritance explains unaffected parents and an apparently negative family history.
8,9,51|A 55-year-old has five years of progressive left SNHL, persistent unilateral high-pitched tinnitus, and veering to the left. MRI shows the enhancing internal auditory canal/cerebellopontine angle lesion pictured. Which diagnosis fits?|Vestibular schwannoma|Asymmetric SNHL with unilateral tinnitus prompts evaluation for retrocochlear pathology. The enhancing vestibular nerve mass supports vestibular schwannoma.|figure-schwannoma
39|A patient has reduced hearing with a canal completely occluded by dark wax. Bone thresholds are normal. Which diagnosis is most likely?|Cerumen impaction|Wax blocks sound reaching the tympanic membrane and causes conductive loss. Removal addresses the obstruction when performed appropriately.|figure-wax
39|A child has congenital absence of a patent external auditory canal but preserved cochlear bone-conduction responses. Which diagnosis explains the deficit?|Congenital aural atresia|Aural atresia prevents ordinary air-conducted sound transmission. Preserved cochlear function allows consideration of bone-conduction hearing rehabilitation.
40,41|A young adult has progressive conductive hearing loss with a normal-appearing drum. Surgery identifies stapes fixation. Which diagnosis fits?|Otosclerosis|Otosclerotic remodeling commonly fixes the stapes footplate and impairs oval-window transmission; stapes surgery or amplification may help selected patients.
40|A chronically draining ear contains a retraction pocket filled with keratin debris and eroded ossicles. Which diagnosis is most likely?|Cholesteatoma|Cholesteatoma can enlarge and erode middle-ear structures, producing conductive loss and serious complications. It is not simply free wax in the external canal.
40,41|After ear trauma, examination shows an eardrum defect and audiometry shows preserved bone thresholds with reduced air thresholds. Which diagnosis best explains the loss?|Tympanic membrane perforation|A perforation reduces effective mechanical sound transfer. Tympanoplasty is a repair option when indicated; the deficit is conductive unless additional injury exists.
47|An 80-year-old has gradually progressive bilateral symmetric high-frequency hearing loss and difficulty understanding speech in a crowded room. What is the most likely diagnosis?|Presbycusis|Aging-related cochlear and neural degeneration commonly causes symmetric SNHL and reduced word recognition. Noise exposure, vascular disease, smoking, and genetic susceptibility can contribute.
48|A factory worker has a bilateral audiometric notch around 4 kHz after years of unprotected machine noise. What is the most likely diagnosis?|Noise-induced hearing loss|Noise commonly damages the 3–6 kHz region. Human cochlear hair cells do not meaningfully regenerate, so persistent injury can produce permanent threshold shifts.
49|A patient develops high-frequency SNHL while receiving cisplatin. Which category best explains the deficit?|Ototoxic cochlear injury|Cisplatin can cause irreversible outer hair cell injury, often initially affecting high frequencies. Baseline and follow-up auditory monitoring help detect toxicity.
50|A patient awakens with markedly reduced hearing in one ear. Audiometry shows a 35-dB loss at three adjacent frequencies arising over 48 hours. What diagnosis should be urgently considered?|Sudden sensorineural hearing loss|The common definition is at least 30 dB across three contiguous frequencies within 72 hours. Prompt assessment distinguishes SNHL from conductive causes and supports time-sensitive treatment. 
8,9|The pictured audiogram shows much worse left-ear thresholds than right-ear thresholds. Persistent unilateral tinnitus accompanies the loss. Which diagnosis warrants exclusion with MRI?|Vestibular schwannoma|Asymmetric SNHL raises concern for retrocochlear lesions. Audiometry identifies the asymmetry; MRI, rather than the audiogram alone, establishes a tumor.|figure-asymmetric
47,48|A retired worker has a slowly progressive downsloping symmetric sensorineural audiogram without an isolated focal middle-ear abnormality. Which age-associated condition is likely contributing?|Presbycusis|Presbycusis and prior noise injury can coexist. A symmetric high-frequency pattern is compatible with aging; a new major asymmetry requires separate evaluation.''')

pool('hearingType','''Normal hearing~Air and bone thresholds are within the usual normal range, without a meaningful gap. Abnormally elevated thresholds indicate hearing loss.
Conductive hearing loss~Air thresholds are worse than bone thresholds, with relatively preserved cochlear bone conduction; pathology lies in external or middle-ear transmission.
Sensorineural hearing loss~Air and bone thresholds are both elevated without a substantial air-bone gap, indicating cochlear or neural dysfunction.
Mixed hearing loss~Bone thresholds are elevated and air thresholds are still worse, indicating combined sensorineural and conductive components.
Central auditory processing impairment~Higher auditory lesions can impair localization, discrimination, or speech-in-noise processing despite preserved basic peripheral thresholds; this is not defined by an air-bone gap.''')
block('av','Audiogram interpretation','hearingType','''26,29|Air and bone thresholds are approximately 10 dB HL across tested frequencies. Which classification is most appropriate?|Normal hearing|Thresholds near 0–20/25 dB HL are generally considered normal in adults, depending on the convention. There is no significant elevation or air-bone gap.|figure-normal
24,26,31,36|The audiogram shows elevated air thresholds with near-normal masked bone thresholds and a large air-bone gap. What type of hearing loss is present?|Conductive hearing loss|A large air-bone gap with near-normal bone thresholds identifies impaired outer/middle-ear transmission rather than primary cochlear loss.|figure-conductive
24,30,37,44|Air and bone thresholds are elevated to similar levels in the affected frequencies, without a substantial gap. What type of hearing loss is present?|Sensorineural hearing loss|Both routes are impaired because they ultimately depend on the cochlea and auditory nerve. Similar air/bone thresholds do not mean normal hearing.|figure-sensorineural
32,38|The audiogram shows elevated bone thresholds and even worse air thresholds. Which classification is most appropriate?|Mixed hearing loss|Elevated bone thresholds establish a sensorineural component; the additional air-bone gap establishes a conductive component.|figure-mixed
35,36|A lesion blocks sound in the external auditory canal while the cochlea and nerve remain functional. What hearing loss category is expected?|Conductive hearing loss|External canal and middle-ear lesions impair mechanical delivery to the cochlea and typically create an air-bone gap.
35,37|Selective destruction of cochlear hair cells causes which category of hearing loss?|Sensorineural hearing loss|Cochlear sensory damage impairs both air- and bone-conducted hearing. Bone conduction bypasses the middle ear, not the cochlea.
35,38|A patient with longstanding cochlear hearing loss develops a middle-ear effusion. Which category now best describes the combined deficit?|Mixed hearing loss|A new conductive component is superimposed on existing SNHL. The audiogram shows elevated bone thresholds plus worse air thresholds.
20|A patient hears quiet pure tones but struggles to localize sounds and interpret complex acoustic patterns after cortical injury. Which category best fits?|Central auditory processing impairment|Auditory cortex contributes to hearing in noise, temporal judgment, localization, and complex sound interpretation; peripheral detection alone does not capture these functions.''')

pool('hearingTest','''Weber test~A midline tuning fork tests lateralization: toward the poorer ear in conductive loss and toward the better ear in unilateral SNHL.
Rinne test~This compares air with bone conduction at one ear. Air greater than bone occurs normally and in SNHL; bone at least as good as air suggests conductive loss.
Pure-tone audiometry~Frequency-specific threshold testing quantifies air and bone hearing levels; masked testing is needed when crossover could mislead.
Word recognition testing~Speech discrimination scores measure recognition of presented words, rather than simply the softest pure tone detected.
Tympanometry~Changing canal pressure measures middle-ear admittance/compliance and pressure; it does not directly measure cochlear sensory function.
Auditory brainstem response~ABR records time-locked neural responses from the auditory nerve/brainstem and permits objective assessment in infants or uncooperative patients.
MRI of the internal auditory canals~MRI with appropriate sequences and contrast can identify vestibular schwannoma and other retrocochlear lesions in asymmetric SNHL.
Whispered voice screening~This is a bedside hearing screen, but it does not replace calibrated audiometry or identify all types of hearing loss.''')
block('av','Hearing tests','hearingTest','''21|A clinician stands behind a patient, masks the opposite ear, and asks the patient to repeat quietly spoken letters or numbers. Which type of assessment is this?|Whispered voice screening|A voice screen estimates hearing impairment at the bedside. Distance, technique, masking, and examiner intensity affect performance; formal testing quantifies a deficit.
22|Which bedside test places a vibrating tuning fork in the midline to assess whether the sound lateralizes?|Weber test|Weber compares relative perception between ears. Lateralization must be interpreted with Rinne and the broader clinical examination.
22|Which bedside test compares sound heard beside the external canal with sound heard from the mastoid?|Rinne test|Rinne compares AC and BC in one ear. A positive Rinne, AC greater than BC, does not exclude SNHL.
23,24,25|Which test measures the softest detected tones at several frequencies using headphones and a mastoid vibrator?|Pure-tone audiometry|Air testing evaluates the entire pathway; bone testing bypasses external/middle-ear transmission. A sound-treated booth and calibration improve reliability.
25|A patient detects pure tones reasonably well but recognizes only 48% of words presented at an appropriate audible level. Which test quantifies this additional deficit?|Word recognition testing|Word recognition measures speech discrimination and provides information beyond threshold sensitivity. Poor recognition influences hearing rehabilitation decisions.
33|Which test measures middle-ear pressure, compliance, and ear canal volume using a probe seal?|Tympanometry|Tympanometry assesses middle-ear mechanics. A flat trace or negative-pressure peak requires interpretation with canal volume and otoscopy.
6,34|A 3-month-old cannot perform behavioral audiometry reliably. Which test objectively assesses auditory neural responses?|Auditory brainstem response|Scalp-recorded responses after acoustic stimuli permit objective hearing assessment in infants. ABR can estimate thresholds and evaluate neural timing.
9,51|A patient has progressive unilateral SNHL and a substantial interaural word-recognition difference. Which study best assesses a retrocochlear mass?|MRI of the internal auditory canals|MRI evaluates vestibular nerve and cerebellopontine angle lesions. A normal otoscopic examination does not exclude such pathology.''')

custom('av','Tuning fork interpretation','22','A left middle-ear effusion causes conductive loss. Which tuning fork pattern is expected?',[
'Weber to the left; left Rinne bone at least as good as air~Conductive loss makes Weber lateralize toward the affected ear and can reverse Rinne when sufficiently large.',
'Weber to the right; left Rinne air greater than bone~This pattern is more compatible with left SNHL than left conductive loss.',
'Weber midline; Rinne always proves normal thresholds~Rinne does not quantify thresholds, and unilateral conductive loss usually lateralizes Weber.',
'Weber to the right; normal bone thresholds exclude conductive loss~Normal cochlear bone thresholds actually support an isolated conductive component.',
'Weber direction cannot change with middle-ear disease~Conductive disease is a classic cause of Weber lateralization.'])
custom('av','Tuning fork interpretation','22','A patient has left cochlear SNHL and intact right hearing. Which pattern is expected?',[
'Weber to the right; Rinne air greater than bone~Weber lateralizes toward the better-hearing ear in unilateral SNHL. AC remains better than BC even though both are impaired.',
'Weber to the left; left Rinne bone greater than air~This is a classic conductive-loss pattern.',
'Weber midline in every unilateral loss~Asymmetric hearing can cause lateralization.',
'Rinne must be negative in all SNHL~Rinne is typically positive in SNHL.',
'Normal right hearing makes all left testing impossible~Contralateral masking can prevent crossover and permit ear-specific assessment.'])
custom('av','Audiometry principles','24,26','Why does bone-conduction testing help identify a conductive component?',[
'It bypasses external and middle-ear mechanical transmission~Bone vibration stimulates the cochlea more directly. A gap between air and bone thresholds identifies an additional transmission deficit.',
'It bypasses the cochlea and directly activates cortex~Bone-conducted hearing still requires cochlear and neural function.',
'It measures only vestibular responses~The test assesses auditory thresholds.',
'It removes all need for contralateral masking~Bone conduction can stimulate the opposite cochlea, making masking important.',
'It directly measures middle-ear fluid volume~Tympanometry and otoscopy assess middle-ear status; bone thresholds do not measure fluid volume.'])
custom('av','Audiometry principles','26','On a standard audiogram, what does moving downward on the vertical axis mean?',[
'A higher dB HL threshold and poorer hearing sensitivity~Audiograms plot increasing hearing level downward. A lower-positioned point means a louder test tone was needed.',
'A lower threshold and better sensitivity~This reverses the standard audiogram axis.',
'A higher sound frequency~Frequency is plotted on the horizontal axis.',
'Better word recognition by definition~Pure-tone thresholds do not directly equal speech recognition scores.',
'Greater middle-ear compliance~Compliance is a tympanometric measurement.'])
custom('av','Audiometry principles','26,28','What does 0 dB HL mean?',[
'A reference threshold based on normal hearing for that frequency~dB HL is referenced to normal auditory thresholds, not absolute absence of sound. Different frequencies have different physical reference intensities.',
'Complete absence of acoustic energy~Zero on the hearing-level scale does not mean no sound exists.',
'Profound deafness~Profound loss requires much higher thresholds.',
'A 0% word recognition score~Word recognition is a separate percentage measure.',
'A completely immobile tympanic membrane~Membrane mechanics are assessed by tympanometry.'])
pool('degree','''Mild loss~A commonly used adult range is roughly 26–40 dB HL; schemes vary, especially in children.
Moderate loss~A common adult range is about 41–55 dB HL.
Moderately severe loss~A common adult range is about 56–70 dB HL.
Severe loss~A common adult range is about 71–90 dB HL.
Profound loss~Thresholds above about 90 dB HL are generally considered profound; residual hearing and speech benefit still require assessment.''')
block('av','Hearing loss severity','degree','''27,28|A measured adult threshold is 35 dB HL. Using common lecture-style categories, how is its severity classified?|Mild loss|A 35-dB threshold is within a common mild range. Severity describes the threshold, not whether the loss is conductive or sensorineural.
27,28|An adult threshold is 50 dB HL. Which common category applies?|Moderate loss|A threshold near 50 dB HL lies in a typical moderate range; exact cutoffs vary slightly across conventions.
27,28|An adult threshold is 65 dB HL. Which category best fits?|Moderately severe loss|A typical moderately severe range is approximately 56–70 dB HL.
27,28|An adult threshold is 80 dB HL. Which category best fits?|Severe loss|An 80-dB threshold is commonly classified as severe rather than profound.
6,27,28|An infant has reliable thresholds around 105 dB HL bilaterally. Which severity category fits?|Profound loss|Thresholds above about 90 dB HL are profound. Objective testing and aided benefit guide rehabilitation; the number alone does not determine every treatment decision.''')
pool('tymp','''Type A: normal peak near atmospheric pressure~This usually reflects normal middle-ear pressure and compliance; a normal tympanogram does not exclude SNHL.
Type B: flat trace with normal canal volume~This commonly supports middle-ear effusion when the drum is intact and the probe is functioning properly.
Type B: flat trace with large canal volume~A perforation or patent tympanostomy tube exposes additional volume and can create a flat trace with high measured volume.
Type C: peak at negative pressure~This suggests negative middle-ear pressure, often from obstructive Eustachian tube dysfunction.
Type Ad: unusually high compliance~An excessively mobile system can occur with ossicular discontinuity or a thin/atrophic tympanic membrane; it differs from a flat effusion trace.''')
block('av','Tympanogram interpretation','tymp','''33|Tympanometry shows a normal compliance peak centered near 0 daPa. Which pattern is present?|Type A: normal peak near atmospheric pressure|A type A trace supports normal middle-ear mechanics. Cochlear hearing loss can still exist despite this pattern.
3,33|An intact amber tympanic membrane is accompanied by a flat tympanogram and normal canal volume. Which interpretation fits?|Type B: flat trace with normal canal volume|Middle-ear effusion reduces movement and produces a flat trace. Canal volume helps distinguish fluid from a perforation or tube.
4,33|A child with a patent tympanostomy tube has a flat tympanogram and large canal volume. Which interpretation fits?|Type B: flat trace with large canal volume|The open tube permits the probe to measure connected middle-ear volume. This is different from an intact fluid-filled middle ear.
5,33|A retracted drum has a tympanometric peak at strongly negative pressure. Which pattern is present?|Type C: peak at negative pressure|Obstructive Eustachian tube dysfunction can produce negative middle-ear pressure and drum retraction. A type C trace alone does not prove infected fluid.''')

pool('hearingTreatment','''Tympanostomy tube~A ventilation tube bypasses Eustachian tube dysfunction and ventilates the middle ear in selected persistent effusion/recurrent infection cases.
Balloon dilation of the Eustachian tube~Dilation can improve selected chronic obstructive Eustachian tube dysfunction; it is not a treatment for a patulous tube.
Conventional hearing aid~Amplification makes acoustic input more audible but still depends on functioning cochlear sensory/neural pathways.
Bone-conduction hearing device~This bypasses external/middle-ear transmission by vibrating the skull and requires adequate cochlear function at the receiving side.
Cochlear implant~An electrode array directly stimulates auditory nerve elements, bypassing severely damaged cochlear hair-cell transduction; it does not restore normal hair cells.
Stapedotomy with prosthesis~This bypasses a fixed stapes in selected otosclerosis cases to improve conductive transmission.
Tympanoplasty or ossicular reconstruction~Repair can restore damaged tympanic membrane/ossicular mechanics when the lesion is suitable.
Prompt corticosteroid-based evaluation/treatment for sudden SNHL~Time-sensitive otologic assessment can lead to systemic or intratympanic corticosteroid treatment after considering risks and alternatives.''')
block('av','Hearing rehabilitation','hearingTreatment','''3,4|A child with persistent middle-ear fluid and clinically significant hearing difficulty improves after placement of a small eardrum ventilation device. Which intervention was used?|Tympanostomy tube|A tube ventilates the middle ear and permits drainage without depending on normal Eustachian tube opening. Selection follows clinical duration, hearing, and infection criteria rather than every isolated effusion.|figure-tube
5|Which newer procedure targets selected chronic obstructive Eustachian tube dysfunction by expanding its cartilaginous segment?|Balloon dilation of the Eustachian tube|Balloon dilation is distinct from eardrum tube placement and from management of a patulous tube. Proper patient selection is important.|figure-balloon
45,47|An older adult has aidable bilateral SNHL and retains useful word recognition. Which device primarily increases acoustic input?|Conventional hearing aid|A hearing aid uses a microphone, processing/amplification, and a receiver to deliver sound. It does not bypass cochlear transduction in the way an implant does.
39,42,43|A patient with bilateral canal atresia has good cochlear bone thresholds. Which device can bypass the absent canals and middle-ear route?|Bone-conduction hearing device|Skull vibration reaches the cochlea while bypassing the conductive obstruction. Percutaneous systems cross the skin; transcutaneous systems transmit across intact skin.
6,7,44,46|An infant has profound bilateral cochlear loss and minimal benefit from an appropriate hearing-aid trial. Auditory nerve integrity is adequate. Which intervention can bypass damaged hair cells?|Cochlear implant|Implant electrodes stimulate spiral ganglion/auditory nerve pathways. Early appropriate auditory and language rehabilitation supports development; timing and candidacy are individualized.
41|A patient with stapes fixation undergoes placement of a small piston prosthesis. Which operation is described?|Stapedotomy with prosthesis|A prosthesis transmits ossicular vibration past the fixed stapes footplate. This treats the conductive mechanism rather than regenerating cochlear cells.
40,41|Chronic disease has damaged the eardrum and ossicular chain while cochlear thresholds are preserved. Which reconstructive option targets the deficit?|Tympanoplasty or ossicular reconstruction|Repair addresses the mechanical transmission abnormality. It cannot reverse an unrelated sensorineural component.
50|A patient has a new 40-dB unilateral SNHL across three adjacent frequencies within two days. Which approach is most appropriate?|Prompt corticosteroid-based evaluation/treatment for sudden SNHL|Sudden SNHL warrants urgent assessment. Corticosteroids may be offered early; intratympanic treatment has an important salvage role. Waiting months can miss a therapeutic window.''')
custom('av','Hearing rehabilitation','42,43','What distinguishes a percutaneous from a transcutaneous bone-conduction system?',[
'A percutaneous abutment crosses the skin; a transcutaneous system transmits across intact skin~Both aim to bypass a conductive pathway. Skin care, transmission efficiency, anatomy, and device candidacy influence selection.',
'Only a percutaneous device bypasses the cochlea entirely~Neither provides hearing without an effective receiving cochlea/neural pathway.',
'Transcutaneous systems require an open external canal~They can bypass external canal obstruction.',
'Percutaneous systems regenerate hair cells~These devices transfer vibration rather than regenerate sensory cells.',
'Both are ordinary air-conduction earbuds~Their defining route is skull vibration, not conventional ear-canal sound delivery.'])
custom('av','Hearing rehabilitation','6,7,46','Why does early rehabilitation matter in an infant with profound bilateral hearing loss?',[
'Auditory and language development depend on timely accessible input~Appropriate amplification, implantation when indicated, and language services support development. A good outcome in the lecture case is illustrative rather than guaranteed.',
'All congenital loss resolves spontaneously by school age~Many genetic profound losses persist.',
'A negative family history excludes genetic disease~Recessive or de novo conditions can occur without known affected relatives.',
'Cochlear implants directly stimulate the visual cortex~They stimulate auditory neural elements, not visual cortex.',
'Speech exposure is unnecessary after implantation~Rehabilitation and accessible language remain important.'])
custom('av','Vestibular schwannoma surgery','10','A translabyrinthine approach is chosen to remove a vestibular schwannoma from an ear with nonserviceable hearing. What is the key tradeoff?',[
'It sacrifices the labyrinth and residual hearing while providing access to the CPA~Drilling through the labyrinth provides exposure for tumor removal and facial nerve preservation, but this is not a hearing-preserving approach.',
'It reliably preserves normal hearing in every operated ear~The labyrinth is sacrificed in this approach.',
'It removes only external canal wax~The operation accesses a deep skull-base tumor.',
'It requires removal of the contralateral cochlea~The operation is directed to the affected side.',
'It intentionally transects the facial nerve in all cases~Facial nerve preservation is an important surgical goal.'])
custom('av','Asymmetric hearing loss','51','Which interaural difference is a screening clue cited in the lecture for asymmetric SNHL?',[
'About 10 dB across two test frequencies or more than 15 percentage points in word recognition~The lecture uses these teaching thresholds. Actual MRI referral criteria vary; clinical context and the complete audiogram matter.',
'Exactly the same air and bone thresholds on both sides~Symmetry does not create the cited concern.',
'Only a unilateral negative-pressure tympanogram~That suggests a middle-ear pressure issue rather than defining SNHL asymmetry.',
'A one-point word recognition difference in every patient~Small test variation is not equivalent to the substantial asymmetry cited.',
'An isolated conductive gap with normal cochlear thresholds~That describes a conductive rather than asymmetric sensorineural mechanism.'])

pool('ototoxic','''Gentamicin~An aminoglycoside can damage cochlear and vestibular hair cells, often irreversibly; gentamicin is especially notable for vestibular toxicity.
Furosemide~A loop diuretic can disrupt stria vascularis function and the endocochlear potential; toxicity is often dose/rate related and can be reversible.
High-dose aspirin~Salicylates can cause tinnitus and usually reversible hearing changes, involving cochlear biochemical effects and outer hair-cell function.
Cisplatin~Platinum chemotherapy can cause permanent outer hair-cell injury, often beginning with high-frequency loss.
Amoxicillin~This common penicillin is not one of the classic direct cochleotoxic agents in the lecture; treating an infection is distinct from aminoglycoside hair-cell injury.''')
block('av','Ototoxicity','ototoxic','''49,104|After prolonged antibiotic therapy, a patient develops oscillopsia and bilateral vestibular hypofunction. Which listed drug is a characteristic cause?|Gentamicin|Gentamicin can injure vestibular hair cells and cause persistent imbalance with gaze instability. Hearing may be relatively less affected in some patients.
49|A patient receives a high-rate IV loop diuretic infusion and develops transient hearing decline associated with altered stria vascularis function. Which drug fits?|Furosemide|Loop diuretics can reduce the endocochlear potential. Dose, infusion rate, renal status, and concurrent ototoxic exposures affect risk.
49|A patient taking large analgesic doses develops tinnitus that improves after the medication is withdrawn. Which agent best fits?|High-dose aspirin|Salicylate-associated tinnitus and threshold changes are often reversible, unlike many aminoglycoside or platinum injuries.
49|Which antineoplastic agent is classically associated with irreversible high-frequency outer hair-cell damage?|Cisplatin|Cisplatin cochleotoxicity is commonly permanent and can progress with cumulative exposure. This differs from the often reversible salicylate effect.''')
custom('av','Ototoxicity','49','Which cochlear region is often affected first in aminoglycoside-associated hearing loss?',[
'Basal-turn outer hair cells~The basal cochlea encodes high frequencies, and outer hair cells are often more susceptible than inner hair cells. Initial high-frequency loss can precede wider impairment.',
'Only apical low-frequency cells in every case~That reverses the characteristic basal high-frequency susceptibility.',
'Only the tympanic membrane~Ototoxicity is an inner-ear process, not solely mechanical drum injury.',
'Only the external auditory canal~Canal obstruction causes conductive loss rather than classic cochleotoxic injury.',
'Only the auditory cortex with preserved cochlear function~The described toxicity directly affects inner-ear tissues.'])
custom('av','Ototoxicity','49','Which strategy can help reduce preventable ototoxic exposure during necessary therapy?',[
'Use appropriate dosing/infusion practices, monitor relevant levels and renal function, and investigate early tinnitus or hearing change~Risk reduction depends on the agent and indication. Audiometric monitoring is useful; no strategy guarantees complete protection.',
'Ignore tinnitus until complete deafness develops~Early symptoms can precede severe irreversible injury.',
'Give every drug as the fastest possible IV bolus~Rapid high exposure can increase risk for some agents.',
'Assume normal renal function is irrelevant~Reduced clearance can increase toxic exposure.',
'Assume all drug-induced loss is reversible~Aminoglycoside and cisplatin injury may persist.'])
custom('av','Noise exposure','48','Under the lecture\'s OSHA-style 5-dB exchange rule, doubling sound level from 90 to 95 dBA changes an 8-hour permissible duration to what?',[
'4 hours~A 5-dB increase halves duration under the OSHA exchange rule. This is separate from the more protective NIOSH 85-dBA/8-hour recommendation with a 3-dB exchange rate.',
'16 hours~Increasing exposure level shortens, rather than lengthens, allowable duration.',
'8 hours~This ignores the exchange rule.',
'1 hour~One 5-dB increment halves eight hours to four, not one.',
'24 hours~That greatly increases noise dose rather than maintaining it.'])
custom('av','Noise exposure','48','NIOSH recommends 85 dBA for eight hours with a 3-dB exchange rate. What equivalent duration applies at 88 dBA?',[
'4 hours~A 3-dB rise halves the duration under NIOSH. The lecture combines an 85-dBA warning with an OSHA-style 5-dB rule; the standards should not be conflated.',
'8 hours~This would double the NIOSH daily dose.',
'16 hours~This changes duration in the wrong direction.',
'6 hours~This is not the 3-dB equal-energy tradeoff.',
'24 hours~This far exceeds the same-dose duration.'])
custom('av','Noise injury','48','Hearing thresholds worsen after loud music but return toward baseline after rest. What is this called?',[
'Temporary threshold shift~A reversible postexposure threshold change differs from persistent injury. Repeated exposure can still contribute to lasting damage.',
'Permanent threshold shift by definition~Recovery toward baseline is inconsistent with permanent threshold elevation.',
'Conductive ossicular fixation~Noise-induced cochlear effects are not stapes fixation.',
'Normal cochlear regeneration of all lost hair cells~Humans do not meaningfully replace destroyed cochlear hair cells.',
'A vestibular schwannoma~A tumor does not typically produce this reversible noise-linked pattern.'])

pool('tinnitusDx','''Subjective nonpulsatile tinnitus~Only the patient perceives the sound; cochlear injury and altered central auditory activity can contribute even without an external source.
Vascular pulsatile tinnitus~Pulse-synchronous sound suggests a vascular source such as arterial disease, venous abnormality, shunt, or intracranial hypertension; it warrants targeted evaluation.
Middle-ear muscle myoclonus~Tensor tympani or stapedius contractions can cause repetitive clicking that may be audible to an examiner and need not match the pulse.
Patulous Eustachian tube~An abnormally open tube can cause respiratory and voice autophony and aural fullness; this differs from an obstructed tube.
Obstructive Eustachian tube dysfunction~Failure of normal opening can produce negative middle-ear pressure and effusion; it is not the same as a persistently open tube.
Retrotympanic vascular mass~A red pulsatile mass behind the drum can cause pulsatile tinnitus and requires evaluation before invasive manipulation.''')
block('av','Tinnitus differential','tinnitusDx','''53,54|A patient hears constant ringing in a quiet room, but there is no external sound and the examiner cannot hear it. Which classification fits?|Subjective nonpulsatile tinnitus|Tinnitus is sound perception without an external acoustic stimulus. Subjective tinnitus is perceived only by the affected person.
54,55,56,58|A patient hears a whoosh synchronized with the heartbeat that accelerates during exercise. Which category requires evaluation for vascular causes?|Vascular pulsatile tinnitus|Pulse synchrony suggests a vascular mechanism. Some pulsatile tinnitus is not audible to an examiner, so pulsatile and objectively audible are overlapping rather than identical categories.
55,60|A patient has intermittent clicking that does not track the heartbeat. The examiner can occasionally hear the click and suspects stapedius contractions. Which diagnosis fits?|Middle-ear muscle myoclonus|Middle-ear muscle spasm can create mechanically generated objective tinnitus. Tensor tympani and stapedius are the lecture examples.
55,61|A patient hears the breathing and speaking voice unusually loudly in the affected ear and has aural fullness. The Eustachian tube remains abnormally open. What is the diagnosis?|Patulous Eustachian tube|Respiratory and phonatory autophony are characteristic clues. An open tube is different from the obstructive dysfunction treated by ventilation or selected balloon dilation.
57|Otoscopy in a patient with pulsatile tinnitus reveals the red lesion behind the tympanic membrane shown here. Which finding best describes the concern?|Retrotympanic vascular mass|A vascular middle-ear mass, such as a paraganglioma, can produce pulse-synchronous tinnitus. The image alone does not establish every possible vascular diagnosis; blind biopsy should be avoided.|figure-vascular-mass
3,5,61|A patient has drum retraction, negative middle-ear pressure, and intermittent effusion rather than loud breathing autophony. Which Eustachian tube problem fits?|Obstructive Eustachian tube dysfunction|Obstruction impairs pressure equalization and ventilation. Patulous dysfunction reflects excessive openness and has a different symptom pattern.''')
pool('tinnitusMechanism','''Reduced peripheral input with increased central gain~Deafferentation can reduce inhibitory control and increase central auditory activity, providing a model for subjective tinnitus.
Abnormal spontaneous auditory nerve activity~Injured or metabolically altered fibers may generate activity without an external acoustic stimulus.
Abnormal hair-cell activity after cochlear injury~Disordered cochlear signaling is one proposed contributor to subjective tinnitus; it is not the only mechanism.
Mechanical muscle-generated sound~Stapedius or tensor tympani contractions create an actual internal sound rather than purely central phantom perception.
Turbulent or abnormal vascular flow~Arterial/venous lesions can produce pulse-synchronous sound; this differs from typical nonpulsatile auditory deafferentation.''')
block('av','Tinnitus mechanisms','tinnitusMechanism','''63,64,65|Which model explains subjective tinnitus through diminished cochlear input and reduced inhibition at higher auditory centers?|Reduced peripheral input with increased central gain|The deafferentation/loss-of-inhibition model proposes compensatory central hyperactivity. It is a mechanistic framework rather than proof of one cause in every patient.
63|After neural injury, individual cochlear nerve fibers fire without an external stimulus. Which proposed tinnitus mechanism is illustrated?|Abnormal spontaneous auditory nerve activity|Spontaneous firing from injured or metabolically altered auditory fibers may contribute to phantom sound perception.
63|A hypothesis attributes tinnitus to repetitive cochlear sensory-cell discharge following hearing injury. Which mechanism is described?|Abnormal hair-cell activity after cochlear injury|The disordered hair-cell theory links peripheral injury to abnormal signaling interpreted as sound. Central changes may coexist.
56,58|A vascular shunt produces a pulse-synchronous sound. Which mechanism is responsible?|Turbulent or abnormal vascular flow|The sound tracks circulation rather than ordinary external acoustic input. Vascular anatomy and pressure relationships guide the workup.
60|The examiner hears clicks during involuntary stapedius contractions. Which mechanism is responsible?|Mechanical muscle-generated sound|Middle-ear muscle activity can generate a real internally produced acoustic signal. This is distinct from a purely phantom nonpulsatile percept.''')
custom('av','Tinnitus assessment','58,59','Which targeted imaging approaches may evaluate suspected vascular pulsatile tinnitus?',[
'MRA/MRV or CT angiographic approaches selected for the suspected cause~Vascular and temporal-bone imaging are tailored to the history and examination; catheter angiography is reserved for selected cases rather than every patient.',
'Routine lumbar spine radiography~This does not evaluate cranial vascular sources of tinnitus.',
'Only an external canal swab~A swab cannot exclude a vascular shunt or venous abnormality.',
'No imaging or assessment regardless of pulse synchrony~Persistent pulse-synchronous symptoms can signal important vascular disease.',
'Blind middle-ear biopsy before assessing vascularity~Manipulating an uncharacterized vascular lesion can cause bleeding.'])
custom('av','Tinnitus assessment','58','A patient has pulsatile tinnitus, headaches, transient visual obscurations, and papilledema. Which associated condition should be considered?',[
'Idiopathic intracranial hypertension after exclusion of secondary causes~Raised ICP can produce pulsatile tinnitus and papilledema. The diagnosis requires appropriate evaluation, not symptoms alone.',
'Isolated subjective tinnitus from noise exposure only~Papilledema and headache require an intracranial-pressure workup.',
'Benign wax impaction as the complete explanation~Wax cannot account for papilledema.',
'A patulous tube as the complete explanation~Autophony does not explain pressure-related disc edema.',
'Ordinary age-related hearing loss as the complete explanation~Presbycusis alone does not explain the neurologic/ocular findings.'])
custom('av','Tinnitus assessment','66','In hearing-loss-associated tinnitus, how can perceived pitch relate to the audiogram?',[
'It may correspond to the frequency region of greatest hearing loss~The deck emphasizes correlation with a high-frequency loss region, often 3–8 kHz. A population association is not a rule for every patient or proof of a specific lesion.',
'Pitch must always equal the lowest tested frequency~There is no such universal rule.',
'Tinnitus requires normal thresholds at every frequency~Hearing impairment commonly coexists.',
'A pitch match establishes a vestibular schwannoma~Pitch does not independently diagnose a retrocochlear mass.',
'Tinnitus pitch measures middle-ear pressure~Pitch matching and tympanometry measure different properties.'])
custom('av','Tinnitus management','67,68,69,70','A patient with persistent bothersome nonpulsatile tinnitus and aidable hearing loss asks about advertised supplements. Which approach has the best clinical basis?',[
'Audiologic care, hearing-aid evaluation, and tinnitus-focused behavioral management~Education, addressing hearing loss, and CBT-based approaches can reduce distress. Commercial supplement claims do not establish efficacy; treating anxiety or insomnia is distinct from curing tinnitus.',
'Recommend every advertised supplement as a proven cure~Marketing images in the deck are not evidence of benefit.',
'Prescribe benzodiazepines routinely as a definitive tinnitus cure~They are not routinely recommended solely for persistent primary tinnitus and have important risks.',
'Avoid all sound exposure indefinitely~Reasonable hearing protection differs from harmful overavoidance or withdrawal from daily activities.',
'Promise that one drug will eliminate tinnitus in all patients~No universal curative medication is established.'])
custom('av','Tinnitus management','68','Why should depression, sleep difficulty, TMJ symptoms, or cervical muscle tension be assessed in a patient with tinnitus?',[
'Treating relevant associated conditions can reduce symptom burden and distress~Management is individualized. An antidepressant may treat comorbid depression without being a proven direct cure for the tinnitus percept.',
'Each condition proves a vascular shunt~These associations do not establish a vascular source.',
'All tinnitus is caused by psychiatric illness~Peripheral hearing injury and other mechanisms can be present.',
'Their presence eliminates the need for hearing assessment~Audiologic evaluation remains important.',
'Each requires the same medication regardless of cause~Targeted treatment depends on the actual associated disorder.'])
custom('av','Tinnitus pharmacology','69','The lecture lists gabapentin as a GABA-related compound. What is its principal pharmacologic target?',[
'The alpha-2-delta subunit of voltage-gated calcium channels~Gabapentin is structurally related to GABA but is not a direct GABA receptor agonist. Its mechanism does not establish routine efficacy for primary tinnitus.',
'Direct activation of GABA-A receptors~Benzodiazepines enhance GABA-A signaling; gabapentin does not act as a direct GABA-A agonist.',
'Direct activation of GABA-B receptors~Baclofen is the classic GABA-B agonist, not gabapentin.',
'Irreversible inhibition of acetylcholinesterase~That is an organophosphate-type cholinergic mechanism.',
'Selective beta-2 blockade of ciliary epithelium~That is an ocular beta-blocker mechanism rather than gabapentin pharmacology.'])
custom('av','Tinnitus management','68,69','Which interpretation of the lecture\'s antidepressant, anticonvulsant, and tranquilizer list is most accurate?',[
'These are discussed options, not routine proven drugs for every case of primary tinnitus~Evidence-based tinnitus care distinguishes treatment of distress or comorbid conditions from direct suppression of the percept. Blanket use of these drug classes is not recommended solely for primary tinnitus.',
'Every listed drug has established equal curative efficacy~The evidence does not support this claim.',
'All tinnitus must be treated first with chronic benzodiazepines~This is not routine evidence-based care.',
'SSRIs permanently restore lost cochlear hair cells~They do not regenerate human cochlear sensory cells.',
'Anticonvulsants remove vascular shunts~A structural vascular cause requires cause-specific evaluation.'])
custom('av','Tinnitus management','68','A patient takes prescribed low-dose aspirin for a major cardiovascular indication and reads the lecture instruction to avoid ASA. What is the best interpretation?',[
'Review dose, indication, and symptoms with the treating clinician rather than stopping automatically~High-dose salicylates can cause tinnitus. A blanket instruction to stop indicated antiplatelet therapy ignores the balance of cardiovascular benefit and auditory risk.',
'All aspirin doses inevitably cause irreversible deafness~Salicylate auditory effects are commonly dose-related and reversible.',
'Stop all cardiovascular drugs without discussion~This can create preventable risk.',
'Increase aspirin to treat the tinnitus~High doses can worsen salicylate-related symptoms.',
'Tinnitus proves the patient has no cardiovascular risk~Auditory symptoms do not negate the original indication.'])

pool('vestDx','''Posterior canal BPPV~Brief triggered episodes after rolling, looking up, or bending, with torsional-upbeating positional nystagmus, suggest displaced otoconia in the posterior canal.
Vestibular neuritis~An acute sustained peripheral vestibular syndrome lasts days and typically lacks new hearing loss; hearing loss suggests labyrinthine or other pathology.
Labyrinthitis~Inflammation involving the labyrinth causes vertigo with hearing loss; bacterial spread from middle ear or meninges is a serious possibility.
Meniere disease~Spontaneous episodic vertigo with fluctuating, often low-frequency SNHL, tinnitus, and aural fullness fits Meniere disease rather than brief positional spells.
Bilateral vestibular hypofunction~Bilateral vestibular loss causes head-motion oscillopsia and imbalance, often worse in darkness or on uneven surfaces; ototoxicity is a possible cause.
Central vestibular lesion~Focal neurologic deficits, direction-changing gaze-evoked or vertical nystagmus, or severe truncal ataxia raise concern for a central lesion such as stroke.
Vestibular migraine~Recurrent vestibular symptoms associated with a migraine history and migrainous features suggest vestibular migraine; fluctuating cochlear loss is not required.
Orthostatic presyncope~Lightheadedness after standing with a blood-pressure fall reflects cerebral hypoperfusion rather than necessarily a labyrinthine spinning sensation.
Multisensory disequilibrium~Combined visual, proprioceptive, and vestibular deficits can impair balance, especially in older adults; no single end-organ lesion need explain all symptoms.''')
block('av','Vestibular differential','vestDx','''11,12,74,75,77,78|An 82-year-old with cataracts, reduced joint sensation, and age-related vestibular decline feels unstable when walking. Which concept best explains the additive balance problem?|Multisensory disequilibrium|Balance integrates vision, proprioception, and vestibular input. Impairment of multiple inputs reduces redundancy and increases fall risk.
85,86,87,88|A woman has 15-second spinning spells when rolling onto her right side in bed. She has no hearing change or focal neurologic deficit. Right Dix-Hallpike produces transient torsional-upbeating nystagmus. Which diagnosis fits?|Posterior canal BPPV|Brief position-triggered spells and the characteristic positional nystagmus indicate posterior canal BPPV, usually from utricular otoconia in the canal.
85,90|After a viral-like illness, a patient has continuous severe vertigo for two days with nausea and unidirectional horizontal-torsional nystagmus. Hearing is unchanged. Which peripheral diagnosis is favored after excluding stroke?|Vestibular neuritis|Vestibular neuritis affects vestibular function without the new cochlear loss expected in labyrinthitis. Symptoms peak early and improve as peripheral recovery and central compensation occur.
85,91|A patient with acute middle-ear infection develops severe vertigo and new SNHL. Which complication is most concerning?|Labyrinthitis|Cochlear plus vestibular involvement suggests labyrinthitis. Suppurative disease can spread from middle ear or meninges and requires urgent infection-directed care.
85,92,96|A 48-year-old has repeated spontaneous vertigo lasting 90 minutes with left aural fullness, roaring tinnitus, and fluctuating low-frequency SNHL. Which diagnosis fits?|Meniere disease|The classic tetrad is episodic vertigo, fluctuating hearing loss, tinnitus, and fullness. Attacks last much longer than typical posterior canal BPPV.
49,85,104|After gentamicin treatment, a patient sees the environment bob while walking and is unstable in darkness. Head impulse testing is abnormal in both directions. Which diagnosis fits?|Bilateral vestibular hypofunction|Bilateral vestibular hair-cell injury reduces the VOR, causing oscillopsia with head movement. Loss of visual compensation worsens balance in darkness.
84,85|A patient has acute sustained dizziness, dysarthria, limb ataxia, and direction-changing gaze-evoked nystagmus. Which category requires urgent exclusion?|Central vestibular lesion|Neurologic deficits and central ocular motor signs raise concern for posterior circulation disease. These should not be attributed to a benign peripheral diagnosis without evaluation.
84|A patient has recurrent vertigo with photophobia and migraine headaches but no documented fluctuating SNHL. Which listed diagnosis should be considered?|Vestibular migraine|Migraine-associated vestibular episodes are a common dizziness differential shown in the lecture diagram. The history differs from the cochlear tetrad of Meniere disease.
84|An older adult feels faint when standing; orthostatic BP falls substantially. There is no spinning or positional nystagmus. Which category best explains the episode?|Orthostatic presyncope|Dizziness is a broad symptom. Orthostatic hypoperfusion is distinguished from vestibular vertigo by triggers, associated symptoms, and measured hemodynamics.
86,90|A patient has continuous vertigo even while motionless, rather than isolated seconds-long spells after specific positions. Hearing is normal. Which peripheral syndrome is more likely than BPPV?|Vestibular neuritis|Head movement worsens many vestibular disorders, but BPPV is characterized by brief triggered episodes. A sustained acute vestibular syndrome requires a broader, including central, evaluation.
91,96|Which diagnosis is more likely when acute sustained vertigo and new hearing loss occur together during a serious ear infection?|Labyrinthitis|Labyrinthitis involves cochlear as well as vestibular structures. Meniere disease is typically episodic and not defined by an acute infectious spread.
97|A patient with years of recurrent vertigo and fluctuating hearing loss now has fewer acute attacks but chronic imbalance and persistent moderate hearing impairment. Which disorder has this described late course?|Meniere disease|A late 'burnt-out' pattern can include reduced attack frequency with chronic disequilibrium and lasting hearing loss. The lecture’s 50-dB/50%-WRS description is illustrative rather than universal.''')

pool('vestOrgan','''Utricle~The utricular macula primarily detects horizontal linear acceleration and head tilt relative to gravity; its otoconia can dislodge into a semicircular canal.
Saccule~The saccular macula is especially sensitive to vertical linear acceleration and gravity-related orientation.
Semicircular canals~Canal cristae detect angular acceleration through endolymph-induced cupular deflection; they are not primarily linear-acceleration sensors.
Cochlea~Cochlear hair cells transduce acoustic vibrations for hearing, rather than serving as the primary vestibular acceleration sensors.
Spiral ganglion~Spiral ganglion neurons carry cochlear auditory signals to the brainstem; vestibular afferent cell bodies are in the vestibular ganglion.''')
block('av','Vestibular end organs','vestOrgan','''72,73|Which end organ is most important for detecting horizontal translation in a car?|Utricle|The utricular macula is oriented to detect horizontal linear acceleration and head tilt. It belongs to the otolith system.
72,73|Which end organ is especially relevant when an elevator begins accelerating upward?|Saccule|The saccule preferentially detects vertical linear acceleration. The semicircular canals encode angular acceleration rather than elevator translation.
72,73|Which structures are primarily stimulated when the head begins rotating to the right?|Semicircular canals|Angular acceleration displaces endolymph relative to the canal and deflects the cupula over the crista hair cells.
72,86,87|Otoconia causing typical posterior canal BPPV most commonly originate from which end organ?|Utricle|Dislodged utricular otoconia can enter a semicircular canal or adhere to its cupula. They are not normally produced by cochlear auditory hair cells.
72,73|Which inner-ear structure contains the sensory organ for sound rather than gravity or acceleration?|Cochlea|The organ of Corti in the cochlea supports hearing. Utricle, saccule, and canals support vestibular sensing.''')
custom('av','Vestibular transduction','72,73','What mechanically stimulates canal hair cells during angular acceleration?',[
'Endolymph movement deflecting the cupula~Fluid inertia bends the cupula and hair bundles at the canal crista. Otolith maculae instead use an otoconial membrane for linear/gravitational signals.',
'Sound vibration of the tympanic membrane alone~This is the initial auditory conduction step, not the canal acceleration mechanism.',
'Light-induced cGMP breakdown~This is photoreceptor transduction.',
'Direct stapes contact with vestibular nerve axons~Stapes motion acts through inner-ear fluid, not direct axonal contact.',
'An air-bone gap in the external canal~This is an audiometric conductive-loss concept, not vestibular transduction.'])
custom('av','Vestibular transduction','72,73','Which feature distinguishes otolith organs from semicircular canals?',[
'Otolith organs use a weighted membrane to sense linear acceleration and gravity~Utricle and saccule contain otoconia. Canals use a cupula and endolymph dynamics to detect angular acceleration.',
'Only canals are inner-ear structures~Both are in the vestibular labyrinth.',
'Otolith organs detect only high-frequency sound~Their main function is vestibular orientation and translation sensing.',
'Canals contain the organ of Corti~The organ of Corti is cochlear.',
'Otolith organs have no hair cells~Macular hair cells are their sensory transducers.'])
custom('av','Balance integration','74,75','Which three major sensory streams support stable stance?',[
'Vestibular, visual, and proprioceptive input~These inputs are integrated with CNS processing and motor output. Losing one increases dependence on the others.',
'Only hearing, taste, and smell~These are not the three primary balance streams illustrated.',
'Only vision, with vestibular input unnecessary~Vestibular function contributes strongly during movement and when vision is unreliable.',
'Only joint receptors, with vision irrelevant~Visual information contributes to orientation and stability.',
'Only the labyrinth without central integration~Vestibular nuclei, cerebellum, and other CNS systems integrate and adapt the input.'])
custom('av','Balance integration','76','What is the principal role of the vestibulo-ocular reflex?',[
'Keep retinal images stable during head movement~The VOR produces compensatory eye movement opposite head movement, maintaining gaze on a target.',
'Amplify external sounds at the tympanic membrane~This is middle-ear mechanics rather than VOR function.',
'Generate conscious language comprehension~This involves cortical auditory-language networks.',
'Produce endolymph in the cochlea~Stria vascularis contributes to endolymph homeostasis.',
'Contract the pupil in bright light~The pupillary light reflex is a different circuit.'])
custom('av','Balance integration','76,78','What is the principal role of vestibulospinal responses?',[
'Adjust postural muscles to maintain orientation and balance~Vestibular signals influence axial and limb motor activity to stabilize the body as the head and center of gravity move.',
'Produce pupil dilation for an eye examination~This is autonomic iris pharmacology.',
'Convert sound into cochlear receptor potentials~This is auditory transduction.',
'Transmit smell from the nose~This is an olfactory pathway.',
'Replace all visual feedback~Postural control continues to use multiple sensory inputs.'])
custom('av','Balance integration','77','Which visual problems can worsen balance?',[
'Reduced acuity, impaired binocular vision, or abnormal ocular motor control~Clear visual targets and coordinated eyes support orientation and gaze stability; cataracts and ocular motor disease can reduce these contributions.',
'Only color-vision deficiency in every case~The lecture emphasizes acuity, ocular motor function, and binocular vision rather than a universal isolated color effect.',
'A normal retina guarantees normal balance~Vestibular, proprioceptive, and central deficits can still impair balance.',
'Vision contributes only when both ears are deaf~Visual orientation is routinely used for balance.',
'Visual deficits cannot interact with vestibular loss~Loss of visual compensation can substantially worsen vestibular imbalance.'])
custom('av','Balance integration','78','Why can joint disease or reduced sensation at the hips, knees, and ankles worsen balance?',[
'It reduces proprioceptive feedback used to adjust the center of gravity~Joint and somatic input helps estimate body position and support postural corrections. Orthopedic and sensory problems can add to vestibular deficits.',
'It directly destroys cochlear hair cells~Joint dysfunction does not inherently cause cochleotoxic injury.',
'It prevents retinal photopigment formation~Vitamin A pathways, not joint input, supply retinal chromophore.',
'It removes all motor strength in every patient~Proprioceptive impairment can affect balance even without complete weakness.',
'It improves accuracy by removing conflicting inputs in all cases~Reduced reliable input usually decreases sensory redundancy.'])
block('av','Multisensory conflict','vestDx','''79,80|A patient with vestibular hypofunction remains reasonably stable on a firm floor with eyes open. Which concept explains the benefit of intact vision and joint sensation?|Multisensory disequilibrium|Balance systems can compensate for one impaired input by relying on the other two. This question concerns multisensory integration, not proof that every input is normal.
79,80,81|A patient with vestibular loss becomes markedly more unstable when the eyes close, while joint sensation remains available. Which conceptual problem is illustrated?|Multisensory disequilibrium|Removing visual compensation leaves greater dependence on proprioception. An abnormal balance test must be interpreted with sensory and motor examination.
79,80,81,82|A patient has vestibular impairment and poor vision; standing on foam now further destabilizes the patient. What best explains this deterioration?|Multisensory disequilibrium|Foam reduces the reliability of somatosensory information. When all three streams are compromised, redundancy is greatly reduced.
79,80,83|After visual impairment improves, a vestibular-loss patient becomes steadier on a firm surface. Which principle is illustrated?|Multisensory disequilibrium|Restoring one reliable sensory stream can improve compensation for another deficit. Improvement does not necessarily mean vestibular hair cells regenerated.''')

custom('av','BPPV mechanism','86,87','What distinguishes canalithiasis from cupulolithiasis?',[
'Free particles within a canal versus particles attached to the cupula~Both involve displaced otoconia. Particle location changes the mechanics and can affect nystagmus duration and response to maneuvers.',
'Bacterial versus viral invasion of the cochlea~Those are infectious distinctions, not the two otoconial mechanisms.',
'Cochlear versus cortical hearing loss~These terms describe vestibular particle mechanics.',
'Anterior chamber versus trabecular outflow~These are ocular, not vestibular, structures.',
'Normal aging versus an RB1 mutation~Neither defines the particle locations.'])
custom('av','BPPV testing','86,88','Which Dix-Hallpike finding supports typical posterior canal BPPV?',[
'Brief torsional-upbeating nystagmus after positioning with the affected ear down~The response is aligned with the posterior canal and often has a short latency and fatigability. ' + 'The lecture\'s geotropic shorthand should not replace the full torsional-upbeat description.',
'Persistent pure downbeat nystagmus with focal neurologic deficits~This is a central warning pattern and is not typical posterior canal BPPV.',
'Only a low-frequency air-bone gap~That is an auditory conductive finding.',
'No positional symptoms but continuous vertigo for days~That is a sustained vestibular syndrome rather than classic brief triggered BPPV.',
'Pulsatile tinnitus alone~That requires a different, often vascular, assessment.'],'figure-dix')
custom('av','BPPV treatment','86,89','What is the goal of the Epley maneuver?',[
'Move canal otoconia back toward the utricle~Sequential head/body positions use gravity to clear particles from the posterior canal. It is a mechanical repositioning treatment.',
'Destroy both vestibular nerves~Epley is nonablative and does not transect nerves.',
'Increase endolymph production~That is not its mechanism.',
'Remove a vestibular schwannoma~A tumor requires separate management.',
'Treat all dizziness regardless of localization~Canal-specific repositioning is used for the appropriate BPPV phenotype.'],'figure-epley')
custom('av','BPPV treatment','86,89','A patient has confirmed posterior canal BPPV. Which approach is preferred over indefinite vestibular suppressant medication?',[
'Canalith repositioning or referral to a clinician who performs it~Repositioning targets the cause. Routine long-term suppressants can cause sedation and do not clear the displaced particles.',
'Chronic benzodiazepines as the only necessary treatment~These do not reposition otoconia and can increase fall risk.',
'Immediate labyrinthectomy in every case~This destructive operation is not ordinary BPPV treatment.',
'Cochlear implantation~This treats selected hearing loss, not a canal particle problem.',
'Antibiotics for all positional vertigo~BPPV is not normally an infection.'])
custom('av','Vestibular neuritis','90','Why is new hearing loss important in an apparent vestibular neuritis case?',[
'It suggests cochlear/labyrinthine involvement or another diagnosis~Pure vestibular neuritis usually spares hearing. Acute hearing loss with vertigo can also occur in vascular disease, so it should not automatically be assumed benign.',
'Hearing loss is required for vestibular neuritis~The classic syndrome lacks new cochlear loss.',
'It proves BPPV~BPPV usually lacks a new auditory deficit.',
'It makes stroke impossible~Some posterior circulation events affect auditory and vestibular structures.',
'It always represents wax regardless of otoscopy~The deficit requires actual localization.'])
custom('av','Labyrinthitis','91','How can infection or inflammatory products reach the labyrinth?',[
'Spread from the middle ear or intracranial/meningeal spaces through relevant interfaces~The lecture lists middle-ear routes, internal auditory canal, and cochlear aqueduct. Toxic/inflammatory mediators and frank bacteria can cause different severities.',
'Only through the external pinna without any intervening pathway~This ignores the anatomic routes described.',
'Only by a visual cortex lesion~Cortical visual injury is not a route of labyrinthine infection.',
'Only after surgical destruction of both ears~Labyrinthitis can occur without surgery.',
'Through an intact lens capsule~The lens is unrelated to ear infection spread.'])
custom('av','Labyrinthitis','91','Suppurative labyrinthitis is suspected in a patient with bacterial ear infection, vertigo, and new hearing loss. Which treatment principle is essential?',[
'Urgent antibiotics and management of the infectious source, with supportive vestibular care~Vestibular suppressants or antiemetics alone do not control bacterial infection. Steroids may be considered in selected circumstances, but cannot replace antibiotics/source management.',
'Only long-term meclizine~Symptom suppression does not eradicate infection.',
'Only an Epley maneuver~Repositioning does not treat suppurative disease.',
'Delay treatment until permanent deafness confirms the diagnosis~Delay can worsen complications.',
'Treat with hearing-aid fitting before addressing infection~Rehabilitation does not replace acute source control.'])
pool('vestTreatment','''Short-term symptom relief followed by rehabilitation~Acute suppressants/antiemetics may help severe vertigo, but prolonged suppression can hinder compensation and increase sedation.
Endolymphatic sac decompression or shunt~This attempts a nonablative sac-directed approach in selected refractory Meniere cases; benefit and selection require discussion.
Labyrinthectomy~This destroys labyrinthine vestibular function and sacrifices hearing, usually reserved for severe refractory disease with nonserviceable hearing.
Vestibular nerve section~Selective section aims to control disabling vertigo while preserving cochlear function when feasible; it is an invasive intracranial procedure.
Intratympanic gentamicin~Local aminoglycoside treatment chemically reduces vestibular function but can damage hearing; dosing and candidacy require specialist care.
Vestibular rehabilitation~Gaze, stance, gait, and habituation exercises promote central adaptation and sensory reweighting rather than regrowing lost hair cells.
Epley canalith repositioning~This treats posterior canal BPPV by moving displaced particles, not endolymphatic hydrops.''')
block('av','Vestibular treatment','vestTreatment','''90,105,109|After exclusion of a central cause, a patient with vestibular neuritis has severe nausea early in the illness. Which overall plan best balances immediate comfort with recovery?|Short-term symptom relief followed by rehabilitation|Brief symptom-directed medication may help acutely, while activity and vestibular rehabilitation support compensation. Corticosteroid benefit is context-dependent rather than guaranteed.
98|During a severe Meniere attack, a patient needs nausea control and temporary reduction of vestibular symptoms. Which management category is appropriate?|Short-term symptom relief followed by rehabilitation|Meclizine or selected sedating agents reduce acute vestibular symptoms; antiemetics such as ondansetron address nausea. Ondansetron is not a vestibular suppressant in the same mechanistic sense.
100|A refractory Meniere patient undergoes an operation intended to improve endolymphatic sac pressure/drainage without intentionally destroying the labyrinth. Which procedure is this?|Endolymphatic sac decompression or shunt|This is a sac-directed nonablative operation. The presence of hydrops does not guarantee success, and evidence/selection must be discussed.
101|A patient has disabling refractory unilateral vertigo and nonserviceable hearing. The operation deliberately removes or destroys labyrinthine function. Which procedure is described?|Labyrinthectomy|Labyrinthectomy is ablative and sacrifices residual hearing. Compensation requires an effective contralateral system and central adaptation.
102|Which operation attempts to disconnect vestibular signals while retaining the cochlear nerve in selected severe refractory Meniere disease?|Vestibular nerve section|Vestibular neurectomy may preserve hearing better than labyrinthectomy, though surgery carries intracranial and cranial nerve risks.
103|A specialist treats refractory Meniere vertigo with a middle-ear injection intended to reduce vestibular sensory function. Which treatment is most consistent?|Intratympanic gentamicin|Gentamicin crosses into the inner ear and exploits vestibulotoxicity to reduce attacks. Hearing damage and excessive vestibular loss remain important risks.|figure-intratympanic
105,106,109|A patient has persistent gaze instability and imbalance after unilateral vestibular injury. Which therapy targets adaptation rather than simply suppressing symptoms?|Vestibular rehabilitation|Exercises promote compensation, gaze stability, sensory reweighting, and gait function. They depend on active CNS plasticity and individualized progression.
110|The patient fixes the eyes on a stationary target while turning the head repeatedly, as shown. What treatment category is illustrated?|Vestibular rehabilitation|Gaze-stabilization exercises train compensatory vestibulo-ocular performance. The goal is better visual stability during head movement.|figure-gaze
111,112|A therapist uses graded stance, gait, and sensory-conflict activities for persistent imbalance. Which approach is being used?|Vestibular rehabilitation|Balance retraining varies sensory reliability and task demands to improve integration. Computerized posturography can help assess sensory dependence but does not itself prove one diagnosis.''')
custom('av','Meniere pathophysiology','92,93,94,95','Which histopathologic change is associated with Meniere disease?',[
'Distention of the endolymphatic compartment~Endolymphatic hydrops is the classic correlate, including enlargement of the cochlear duct. Hydrops and symptoms have a complex relationship, so it is not a complete single-cause explanation in every case.',
'A keratin sac eroding the ossicles~This is cholesteatoma, a middle-ear lesion.',
'Stapes footplate fixation~This is otosclerosis, a conductive mechanism.',
'Loss of all external canal skin~This is not the classic Meniere correlate.',
'An isolated vestibular nerve tumor~That suggests schwannoma rather than hydrops.'],'figure-hydrops')
custom('av','Endolymph homeostasis','95','Which cells/structures contribute to endolymph production in the auditory and vestibular labyrinth?',[
'Stria vascularis and vestibular dark cells~They help maintain the specialized endolymph ionic environment. Disrupted secretion, resorption, or homeostasis can contribute to hydrops.',
'Only the tympanic membrane~The eardrum does not produce inner-ear endolymph.',
'Only the external canal ceruminous glands~These produce wax, not cochlear endolymph.',
'Only the malleus and incus~Ossicles transmit vibration rather than secrete endolymph.',
'Only retinal pigment epithelium~That tissue serves the eye, not the labyrinth.'])
custom('av','Meniere course','96,97','Which hearing pattern is particularly characteristic early in Meniere disease?',[
'Fluctuating low-frequency sensorineural loss~Low-frequency cochlear impairment can accompany attacks; hearing may progressively worsen and flatten over time. Bilateral involvement is possible but not inevitable.',
'A stable isolated conductive gap from birth~That is a different mechanism and course.',
'Only a 4-kHz noise notch with no episodic symptoms~That suggests noise injury rather than the classic Meniere pattern.',
'Normal hearing is required at all times~Documented SNHL is part of definite Meniere diagnostic assessment.',
'Complete recovery of all hearing is guaranteed between every attack~Residual or progressive loss can occur.'])
custom('av','Meniere management','98,99','Which maintenance measures are discussed in the lecture for Meniere disease?',[
'Dietary/lifestyle counseling and selected diuretics or betahistine~The deck includes sodium reduction, moderation of caffeine/alcohol, sleep, and diuretics. Evidence varies and betahistine availability differs by country; these are not guaranteed cures.',
'Long-term high-dose gentamicin for every mild case~Destructive therapy is reserved for selected refractory disease because of hearing/vestibular risks.',
'Only repeated Epley maneuvers regardless of symptoms~Epley treats canal BPPV, not the Meniere syndrome itself.',
'Unlimited noise exposure to retrain the cochlea~Noise can cause additional auditory injury.',
'A cochlear implant as universal first-line vertigo prevention~Implants primarily rehabilitate selected hearing loss and are not universal Meniere maintenance treatment.'])
custom('av','Meniere medications','99','Which medication is a carbonic anhydrase inhibitor mentioned as a diuretic option in the lecture?',[
'Acetazolamide~Diamox inhibits carbonic anhydrase. The same class also reduces aqueous production in ophthalmology; clinical use and risk assessment depend on the indication.',
'Hydrochlorothiazide~This is a thiazide, not a carbonic anhydrase inhibitor.',
'Triamterene~This is a potassium-sparing epithelial sodium-channel blocker.',
'Betahistine~This is a histamine-related agent rather than a carbonic anhydrase inhibitor.',
'Meclizine~This is an antihistaminic vestibular suppressant, not a diuretic.'])
custom('av','Meniere medications','99','Dyazide and Maxzide are commonly recognized combinations of which agents?',[
'Hydrochlorothiazide and triamterene~The combination pairs a thiazide with a potassium-sparing agent. Calling the entire product simply a potassium-sparing class omits its thiazide component.',
'Acetazolamide and mannitol~These are carbonic anhydrase and osmotic agents, not the named combination.',
'Gentamicin and cisplatin~These are ototoxic drug examples, not the diuretic product.',
'Meclizine and ondansetron~These are symptom-control agents rather than the named maintenance diuretic combination.',
'Atropine and tropicamide~These are ocular antimuscarinics.'])
custom('av','Meniere medications','99','Which statement best describes betahistine as discussed in the lecture?',[
'A histamine-related agent used for Meniere symptoms in some countries~It has histaminergic actions and is proposed to affect inner-ear circulation/neurotransmission. Efficacy certainty and regulatory availability vary; it is not a universal proven cure.',
'A direct muscarinic agonist that clears canal particles~That neither identifies betahistine nor describes BPPV treatment correctly.',
'A platinum chemotherapy drug~That describes cisplatin rather than betahistine.',
'A prostaglandin eye-drop analog~That describes a different pharmacologic class.',
'A ventilation tube inserted through the eardrum~Betahistine is a medication, not a tympanostomy device.'])
custom('av','Central compensation','105,106','Which two broad phases of vestibular compensation are described?',[
'Reduction of acute asymmetry followed by recalibration of neural activity~Central plasticity reduces static imbalance and adapts dynamic responses. Recovery depends on injury severity, remaining inputs, and CNS health.',
'Universal hair-cell regeneration followed by new cochlear growth~Human sensory-cell replacement does not account for ordinary compensation.',
'Permanent suppression of all sensory input followed by immobility~Active adaptation requires useful sensory experience and movement.',
'Immediate normal function followed by inevitable complete paralysis~This is not the usual compensation framework.',
'Removal of the healthy labyrinth followed by elimination of vision~Destroying remaining inputs worsens redundancy.'])
custom('av','Central compensation','107','After initial vestibular recovery, illness and sedating medication lead to renewed imbalance. Which pattern is illustrated?',[
'Decompensation~Previously adequate compensation can deteriorate when health, medication exposure, or sensory conditions change. This differs from never achieving adequate recovery.',
'Guaranteed new bilateral hair-cell destruction~Renewed symptoms do not automatically prove a new peripheral structural injury.',
'Successful complete recovery by definition~Symptoms have worsened again.',
'Pure conductive hearing loss as the only explanation~A middle-ear threshold gap does not explain the entire compensation course.',
'Normal aging without any clinical significance~Fall risk and functional deterioration warrant reassessment.'])
custom('av','Central compensation','107,108','Which feature can delay vestibular compensation?',[
'Older age, CNS comorbidity, or prolonged vestibular suppressant exposure~Adaptation depends on CNS plasticity and adequate sensory experience. Recovery and residual deficits vary across patients.',
'Graded gaze and balance practice in all cases~Appropriate rehabilitation generally promotes adaptation rather than uniformly delaying it.',
'Restored visual acuity~Reliable vision can support compensation.',
'Appropriate mobility training~Activity-based rehabilitation helps many patients.',
'A stable reliable proprioceptive system~Reliable remaining input supports balance.'])
custom('av','Vestibular rehabilitation','109,110,111,112','What distinguishes habituation from simply avoiding all provoking movement?',[
'Repeated graded exposure reduces an excessive response to a tolerated stimulus~Habituation exercises aim to decrease pathologic motion sensitivity. They are tailored to safety and diagnosis; they are not unrestricted exposure during an undiagnosed acute emergency.',
'Permanent avoidance is required to create CNS plasticity~Avoidance can limit adaptive sensory experience.',
'Habituation means destroying the vestibular nerve~It is a learning/adaptation process, not ablation.',
'It restores lost cochlear hair cells~Habituation changes responses, not sensory-cell number.',
'It is identical to antibiotic eradication of infection~Behavioral adaptation and antimicrobial treatment are different mechanisms.'])

pool('ocularDrug','''Atropine~A long-acting muscarinic antagonist causes both mydriasis and cycloplegia, with effects lasting days.
Tropicamide~A relatively short-acting muscarinic antagonist is used for diagnostic mydriasis and can also impair accommodation.
Cyclopentolate~An antimuscarinic cycloplegic commonly used for refraction has an intermediate duration relative to tropicamide and atropine.
Phenylephrine~An alpha-1 agonist contracts the radial iris dilator, producing mydriasis without direct cycloplegia.
Timolol~A nonselective beta blocker reduces aqueous production but can cause systemic bradycardia and bronchospasm.
Betaxolol~A relatively beta-1-selective blocker lowers IOP, with less beta-2 blockade than timolol but continued potential cardiopulmonary risk.
Brimonidine~An alpha-2 agonist reduces aqueous production and increases uveoscleral outflow; allergy and CNS effects are relevant.
Apraclonidine~An alpha-2 agonist reduces aqueous production; local allergic reactions can limit sustained use.
Acetazolamide~A systemic carbonic anhydrase inhibitor reduces aqueous formation and can cause metabolic acidosis, hypokalemia, paresthesias, and stones.
Dorzolamide~A topical carbonic anhydrase inhibitor reduces aqueous production, generally with less systemic exposure than oral acetazolamide.
Brinzolamide~A topical carbonic anhydrase inhibitor lowers aqueous production; local irritation or taste disturbance can occur.
Mannitol~An osmotic agent increases plasma osmolality and shifts water out of ocular tissues to rapidly lower IOP in selected emergencies.
Latanoprost~A PGF2-alpha analog increases uveoscleral outflow and can darken iris pigmentation and increase eyelashes.
Bimatoprost~A prostaglandin-related ocular agent lowers IOP and can stimulate eyelash growth; its cosmetic formulation is marketed as Latisse.
Pilocarpine~A direct muscarinic agonist contracts the iris sphincter and ciliary muscle, causing miosis and increasing trabecular outflow.
Carbachol~A direct cholinergic agonist produces muscarinic ocular effects such as miosis and ciliary contraction; it is not an acetylcholinesterase inhibitor.
Echothiophate~A long-acting acetylcholinesterase inhibitor increases endogenous acetylcholine, indirectly producing miosis and increased trabecular outflow.
Netarsudil~A Rho kinase inhibitor lowers resistance in the conventional trabecular outflow pathway; conjunctival hyperemia is common.
Epinephrine~A mixed alpha/beta agonist has complex effects on aqueous dynamics and can dilate the pupil; it is not routinely used for glaucoma and is unsuitable in angle-closure risk.''')
block('oph','Ophthalmic drug identification','ocularDrug','''2,12|Which alpha-1 agonist dilates the pupil without directly paralyzing accommodation?|Phenylephrine|Radial iris dilator contraction causes mydriasis. Unlike antimuscarinics, phenylephrine does not directly block ciliary accommodation.
2|Which muscarinic antagonist has the longest mydriatic/cycloplegic duration among atropine, cyclopentolate, and tropicamide?|Atropine|The lecture gives atropine roughly 7–14 days, cyclopentolate about 24 hours, and tropicamide about six hours; actual duration varies with patient and formulation.
2|A diagnostic antimuscarinic eye drop has a lecture-listed duration of about six hours. Which agent fits?|Tropicamide|Tropicamide is relatively short acting, making it useful for routine diagnostic dilation. It can still blur near vision and increase angle-closure risk in susceptible eyes.
2|A child receives cycloplegic refraction with an antimuscarinic whose lecture-listed duration is about 24 hours. Which agent fits?|Cyclopentolate|Cyclopentolate is intermediate in duration compared with shorter tropicamide and much longer atropine.
4,10|Which nonselective beta-blocker eye drop can worsen asthma while lowering aqueous production?|Timolol|Ophthalmic timolol can be absorbed systemically, producing beta-2 bronchospasm and beta-1 cardiac effects. Topical delivery does not eliminate systemic contraindications.
4,10|Which glaucoma beta blocker is relatively beta-1 selective compared with timolol?|Betaxolol|Betaxolol is relatively beta-1 selective; the slide’s blanket description of all agents as beta-2 blockers is oversimplified. Selectivity does not make it risk-free in pulmonary or cardiac disease.
5,10|Which listed glaucoma drug reduces aqueous synthesis through alpha-2 activation and secondarily increases uveoscleral outflow?|Brimonidine|Brimonidine is an alpha-2 agonist. Its mechanism differs from phenylephrine’s alpha-1-mediated dilation; local allergy and systemic sedation can occur.
5|Which mixed alpha/beta agonist is no longer routinely used for glaucoma and should be avoided in angle-closure glaucoma because it can cause mydriasis?|Epinephrine|Epinephrine can initially stimulate beta-mediated aqueous production, with later pressure-lowering effects through other actions. Pupil dilation can worsen angle closure in a susceptible eye.
6,10|An oral glaucoma medication causes tingling, low bicarbonate, and potassium depletion. Which agent is most likely?|Acetazolamide|Systemic carbonic anhydrase inhibition causes renal bicarbonate loss and related adverse effects while also decreasing ciliary aqueous secretion.
6,10|Which listed topical glaucoma drug inhibits carbonic anhydrase in ciliary epithelium?|Dorzolamide|Dorzolamide is a topical CA inhibitor. It shares the aqueous-production mechanism of acetazolamide with generally lower systemic exposure.
6,10|Which listed topical carbonic anhydrase inhibitor can reduce aqueous production while limiting systemic exposure compared with oral acetazolamide?|Brinzolamide|Brinzolamide, like dorzolamide, reduces aqueous production through ciliary carbonic anhydrase inhibition.
6|An emergency IOP-lowering drug works by increasing serum osmolality. Which agent fits?|Mannitol|IV mannitol shifts water from ocular tissues toward plasma. It is an osmotic approach rather than inhibition of aqueous synthesis.
7,10|Which listed PGF2-alpha analog lowers IOP mainly by increasing uveoscleral outflow?|Latanoprost|Latanoprost increases uveoscleral outflow. Iris darkening and eyelash growth are characteristic local effects.
7|Which glaucoma-related drug is also marketed in a formulation for eyelash growth as Latisse?|Bimatoprost|Bimatoprost promotes eyelash growth and is used in glaucoma formulations. Cosmetic efficacy does not mean absence of pigmentation or ocular adverse effects.
8,11|Which direct muscarinic agonist lowers IOP by contracting the ciliary muscle and increasing trabecular drainage?|Pilocarpine|Pilocarpine activates muscarinic receptors directly, causing miosis and traction on the trabecular drainage apparatus.
8|A drug produces miosis through direct cholinergic receptor stimulation rather than blocking acetylcholinesterase. The agent is also used intraoperatively. Which drug fits?|Carbachol|Carbachol is a direct cholinergic agonist; echothiophate is an indirect cholinomimetic through enzyme inhibition.
8|Which ocular cholinomimetic inhibits acetylcholinesterase rather than directly activating muscarinic receptors?|Echothiophate|Echothiophate prolongs endogenous acetylcholine action, increasing muscarinic effects. It is a long-acting organophosphate-type inhibitor, not the same mechanism as pilocarpine.
9|A patient receives Rhopressa, which reduces trabecular cellular stiffness and outflow resistance. Which generic agent is this?|Netarsudil|Netarsudil inhibits Rho kinase and improves conventional outflow. Ripasudil is another Rho kinase inhibitor named in the lecture, with availability differing by region.''')

pool('ocularMechanism','''Muscarinic receptor blockade~This relaxes iris sphincter and ciliary muscle, causing mydriasis and cycloplegia rather than miosis.
Alpha-1 receptor activation~This contracts the radial iris dilator and causes mydriasis without direct paralysis of accommodation.
Beta-adrenergic blockade at ciliary epithelium~This lowers aqueous secretion; it does not primarily improve trabecular outflow or dilate the pupil.
Alpha-2 receptor activation~This reduces aqueous synthesis and can increase uveoscleral outflow, unlike alpha-1-mediated dilation.
Carbonic anhydrase inhibition~Reduced bicarbonate-dependent fluid secretion lowers aqueous formation; systemic agents also affect renal acid-base balance.
Increased plasma osmolality~An osmotic gradient shifts water out of ocular tissues and rapidly reduces IOP in selected emergencies.
Prostaglandin-mediated uveoscleral outflow~PGF2-alpha-related drugs increase an alternative aqueous drainage pathway rather than mainly suppressing secretion.
Direct M3 receptor stimulation~Ciliary muscle and iris sphincter contraction produce increased trabecular outflow and miosis.
Acetylcholinesterase inhibition~Higher endogenous acetylcholine indirectly produces ocular muscarinic effects; this differs from direct receptor agonism.
Rho kinase inhibition~Reduced trabecular contractility/stiffness lowers resistance in the conventional aqueous drainage pathway.''')
block('oph','Ophthalmic mechanisms','ocularMechanism','''2,12|What mechanism explains both dilation and cycloplegia after atropine eye drops?|Muscarinic receptor blockade|Antimuscarinic action inhibits iris sphincter and ciliary accommodation. The pupil dilates and near focusing is impaired.
2|A pupil dilates after phenylephrine but near accommodation remains largely intact. Which mechanism explains this?|Alpha-1 receptor activation|The radial dilator contracts while ciliary muscarinic receptors are not directly blocked.
4,10|How does timolol primarily lower IOP?|Beta-adrenergic blockade at ciliary epithelium|Blocking beta-mediated signaling reduces aqueous production. It does not produce the muscarinic ciliary contraction of pilocarpine.
5,10|What receptor mechanism explains apraclonidine’s main pressure-lowering effect?|Alpha-2 receptor activation|Alpha-2 activation reduces aqueous secretion. Brimonidine shares this class and can also improve uveoscleral outflow.
6,10|How does acetazolamide lower aqueous production?|Carbonic anhydrase inhibition|Ciliary bicarbonate-dependent secretion falls when carbonic anhydrase is inhibited, reducing aqueous formation.
6|Why can IV mannitol rapidly lower pressure in selected severe glaucoma cases?|Increased plasma osmolality|Osmotic water movement reduces ocular volume, including vitreous water. The slide’s focus solely on anterior chamber fluid is too narrow.
7,10|What is the principal outflow mechanism of latanoprost?|Prostaglandin-mediated uveoscleral outflow|Latanoprost increases uveoscleral drainage rather than primarily decreasing secretion at the ciliary epithelium.
8,11|Which mechanism underlies pilocarpine’s therapeutic effect in glaucoma?|Direct M3 receptor stimulation|Ciliary muscle contraction opens the conventional drainage apparatus and the iris sphincter produces miosis. This original question expands the lecture’s review item to five options.
8|Echothiophate increases trabecular drainage by which initiating mechanism?|Acetylcholinesterase inhibition|Blocking acetylcholine breakdown indirectly activates ocular muscarinic receptors. Pilocarpine reaches similar downstream effects through direct agonism.
9|Netarsudil improves aqueous drainage by which mechanism?|Rho kinase inhibition|Relaxation and reduced stiffness in the trabecular outflow system lower resistance; antifibrotic effects are also discussed in the lecture.''')
custom('oph','Pupil and accommodation','2','What does cycloplegia mean?',[
'Loss of accommodation from ciliary muscle paralysis~Cycloplegia impairs near focusing. Mydriasis means pupil dilation and can occur with or without cycloplegia.',
'Constriction of the pupil~This is miosis, not cycloplegia.',
'Permanent destruction of the retina~Cycloplegia is a focusing effect, not retinal ablation.',
'Increased tear secretion~Tears do not define cycloplegia.',
'An enlarged optic cup~Cupping reflects optic nerve head tissue loss rather than ciliary paralysis.'])
custom('oph','Pupil and accommodation','2','A clinician wants dilation without directly blocking accommodation. Which choice best fits?',[
'Phenylephrine~Alpha-1 stimulation contracts the iris dilator without muscarinic ciliary blockade.',
'Atropine~This causes both dilation and cycloplegia for a prolonged period.',
'Cyclopentolate~This antimuscarinic produces cycloplegia as well as dilation.',
'Tropicamide~It is shorter acting but still has antimuscarinic cycloplegic effects.',
'Pilocarpine~It causes miosis and ciliary contraction rather than diagnostic dilation.'])
custom('oph','Pupil and accommodation','2','Which ordering matches the lecture’s approximate duration of antimuscarinic dilation from longest to shortest?',[
'Atropine, cyclopentolate, tropicamide~The lecture estimates 7–14 days, 24 hours, and six hours respectively; these are teaching approximations, not precise predictions for every patient.',
'Tropicamide, cyclopentolate, atropine~This reverses the main duration relationship.',
'Cyclopentolate, atropine, tropicamide~Atropine generally lasts much longer than cyclopentolate.',
'Atropine, tropicamide, cyclopentolate~Tropicamide is usually shorter acting than cyclopentolate.',
'All have identical duration~Duration is a major practical distinction among the agents.'])
custom('oph','Beta-blocker safety','4,10','A patient develops wheezing soon after starting timolol eye drops. What is the best explanation?',[
'Systemic absorption causes beta-2 receptor blockade~Topical ocular administration can cause significant cardiopulmonary effects. Asthma or severe reactive airway disease is a major concern.',
'Timolol stimulates beta-2 receptors~Stimulation would tend toward bronchodilation rather than this blockade-related effect.',
'Eye drops cannot reach the systemic circulation~Nasolacrimal and other absorption routes permit systemic exposure.',
'The effect is caused by selective alpha-1 stimulation~Timolol is a beta blocker, not phenylephrine.',
'The effect proves a direct muscarinic agonist was prescribed~Beta-blocker bronchospasm can occur without a muscarinic drug.'])
custom('oph','Beta-blocker safety','4,10','Which cardiac history is especially concerning before starting topical timolol?',[
'Symptomatic sinus bradycardia or significant AV block~Systemic beta blockade can slow heart rate and conduction. Overt heart failure or cardiogenic shock also warrants avoidance according to labeling.',
'An isolated normal ECG~This is not itself a contraindication.',
'A remote uncomplicated fracture~This does not identify the major cardiac risk.',
'Only a need for reading glasses~Refractive correction does not identify a beta-blocker contraindication.',
'Normal resting pulse and no cardiac disease~This does not establish the high-risk condition asked about.'])
custom('oph','Beta-blocker safety','4','Which adverse-effect cluster can occur with systemic exposure to ocular beta blockers?',[
'Fatigue, dizziness, bradycardia, and bronchospasm~The slide’s illustrations emphasize systemic effects despite ocular dosing. Risk depends on selectivity, exposure, and comorbidity.',
'Iris darkening and eyelash growth as the defining cluster~These are more characteristic of prostaglandin-related drugs.',
'Metabolic acidosis, hypokalemia, and renal stones~These are characteristic systemic CA-inhibitor effects.',
'Mydriasis with cycloplegia as the main therapeutic action~This is antimuscarinic pharmacology.',
'Acetylcholinesterase inhibition with prolonged miosis~This describes echothiophate rather than beta blockade.'])
custom('oph','Ocular drug safety','5,10','Which local adverse effects can occur with alpha-2 glaucoma agonists?',[
'Hyperemia, itchy eyes, foreign-body sensation, and allergic irritation~Brimonidine/apraclonidine can cause local ocular reactions; systemic fatigue, dry mouth, or CNS effects also require attention.',
'Universal permanent retinal detachment~This is not the typical adverse-effect pattern.',
'Only renal bicarbonate wasting~That is systemic CA-inhibitor pharmacology.',
'Only increased eyelash growth without irritation~This more strongly suggests a prostaglandin effect and omits alpha-agonist allergy.',
'No possible local effects because receptors are systemic only~Ocular receptors and local drug exposure can produce ocular effects.'])
custom('oph','Carbonic anhydrase inhibitor safety','6,10','A patient on oral acetazolamide has low serum bicarbonate and tingling. What acid-base disturbance is expected?',[
'Hyperchloremic metabolic acidosis~Renal bicarbonate loss produces a non-anion-gap acidosis. Hypokalemia, paresthesias, and kidney stones are additional relevant effects.',
'Metabolic alkalosis from increased bicarbonate retention~This reverses the usual CA-inhibitor effect.',
'Primary respiratory alkalosis as the direct renal effect~Acetazolamide primarily alters renal bicarbonate handling.',
'No acid-base effect because only the eye is exposed~Oral or IV treatment has systemic effects.',
'Isolated respiratory acidosis from beta blockade~That is not the primary CA-inhibition mechanism.'])
custom('oph','Carbonic anhydrase inhibitor safety','6,10','Which adverse effect is especially associated with systemic carbonic anhydrase inhibition?',[
'Renal stones with paresthesias and potassium depletion~Urinary changes from CA inhibition favor stones, while systemic electrolyte and acid-base effects can produce symptoms.',
'Increased eyelash length as the main systemic effect~This is associated with bimatoprost/related drugs.',
'Mydriasis without cycloplegia~This is alpha-1 agonist pharmacology.',
'Direct irreversible acetylcholinesterase inhibition~This is not a CA-inhibitor mechanism.',
'Selective hearing recovery after ototoxic injury~CA inhibition does not regenerate cochlear cells.'])
custom('oph','Carbonic anhydrase inhibitor safety','6,10','Why may topical dorzolamide cause fewer systemic effects than oral acetazolamide?',[
'Topical administration generally produces lower systemic exposure~Both inhibit carbonic anhydrase. Route changes the exposure and adverse-effect burden, though topical drugs are not completely free of systemic effects.',
'Dorzolamide activates rather than inhibits carbonic anhydrase~Both are inhibitors.',
'Acetazolamide has no effect outside the eye~Its renal actions are central to its systemic adverse effects.',
'Topical administration prevents every possible adverse event~Local irritation and some systemic exposure remain possible.',
'Dorzolamide works only by pupil dilation~Its primary mechanism is reduced aqueous synthesis.'])
custom('oph','Osmotic therapy','6','After osmotic IOP-lowering therapy, a patient becomes volume depleted and creatinine rises. Which mechanism explains this risk?',[
'Mannitol-induced osmotic diuresis can cause dehydration and prerenal injury~Volume status and renal/cardiac function require monitoring. Mannitol can also initially expand intravascular volume, so risk is not limited to dehydration.',
'Mannitol directly blocks M3 receptors~That is not its osmotic mechanism.',
'Mannitol selectively inhibits beta-2 receptors~It is not a beta blocker.',
'Mannitol always prevents renal injury regardless of volume status~Renal risk depends on dose, clearance, and fluid status.',
'Only an iris pigmentation change explains the creatinine rise~Pigmentation does not explain systemic volume depletion.'])
custom('oph','Prostaglandin adverse effects','7,10','A glaucoma patient develops darker iris color and longer eyelashes. Which drug class best explains the change?',[
'Prostaglandin-related ocular agents~Latanoprost and bimatoprost can increase iris pigmentation and eyelash growth. Local redness/irritation may also occur.',
'Carbonic anhydrase inhibitors~These more characteristically cause taste disturbance/local irritation or systemic acidosis and stones.',
'Nonselective beta blockers~Their major systemic concerns are cardiac and pulmonary blockade.',
'Osmotic diuretics~These affect fluid distribution and do not characteristically lengthen eyelashes.',
'Antimuscarinic cycloplegics~These dilate pupils and impair near focusing rather than produce the characteristic lash/pigment cluster.'])
custom('oph','Cholinergic adverse effects','8,10','Why can pilocarpine make vision worse in dim light?',[
'Miosis reduces the amount of light entering the eye~Sphincter contraction constricts the pupil. Ciliary spasm can also cause brow pain, induced myopia, and near-focusing effects.',
'It causes maximal pupil dilation~Pilocarpine is miotic rather than mydriatic.',
'It directly removes retinal rods~Dim-light blur here is a pharmacologic pupil effect, not rod destruction.',
'It eliminates all aqueous secretion~Its primary pressure effect is increased outflow.',
'It blocks every photopigment molecule~It does not directly inhibit photopigment synthesis.'])
custom('oph','Cholinergic adverse effects','8','Sweating, salivation, diarrhea, and wheezing after excessive ocular cholinergic exposure suggest what?',[
'Systemic cholinergic toxicity~Direct or indirect cholinomimetics can produce systemic muscarinic effects if exposure is sufficient. Eye-drop delivery does not guarantee purely local action.',
'Antimuscarinic toxicity~That more often causes dry mouth, reduced sweating, tachycardia, and dilation.',
'Isolated alpha-1 agonism~That does not explain the secretory/cholinergic cluster.',
'Only a prostaglandin pigmentation effect~Pigmentation does not explain diarrhea and excess secretions.',
'A normal effect of routine accommodation without drug exposure~The systemic autonomic cluster requires evaluation.'])
custom('oph','Outflow pathway comparison','7,8,9','Which pairing correctly matches a drug with its main outflow pathway?',[
'Latanoprost: uveoscleral; pilocarpine: trabecular~Prostaglandin analogs increase alternative uveoscleral drainage. Ciliary contraction from pilocarpine improves conventional trabecular drainage; Rho kinase inhibitors also act on conventional resistance.',
'Latanoprost: aqueous synthesis blockade only; pilocarpine: no outflow effect~This misstates both principal mechanisms.',
'Timolol: direct M3 activation; phenylephrine: CA inhibition~Timolol is a beta blocker and phenylephrine is alpha-1 agonist.',
'Mannitol: acetylcholinesterase inhibition; echothiophate: osmotic shift~This reverses their pharmacologic identities.',
'Netarsudil: lens removal; dorzolamide: iris dilation~Neither is the drug’s pressure-lowering mechanism.'])
custom('oph','Angle-closure treatment context','4,5,6,8','A patient has acute angle closure with very high IOP. Which statement best places the lecture drug list in clinical context?',[
'Urgent multidrug pressure reduction and definitive relief of the closure mechanism are needed~Beta blockers, alpha-2 agents, systemic CA inhibition, or osmotic therapy may be used as appropriate; laser iridotomy treats pupillary block. Miotics may be ineffective until very high IOP falls.',
'Epinephrine dilation is the preferred way to open a crowded angle~Mydriasis can worsen susceptible angle closure.',
'A single chronic eye drop always replaces definitive treatment~Persistent pupillary block requires relief of the mechanism.',
'Wait several weeks to assess whether pain resolves~Acute angle closure threatens vision rapidly.',
'Pilocarpine must work immediately at any pressure~An ischemic iris sphincter may not respond until IOP is lowered.'])
custom('oph','Rho kinase inhibitors','9','A slide calls Rho kinase inhibitors well tolerated. Which counseling statement remains appropriate?',[
'Conjunctival hyperemia and other local effects can still occur~Netarsudil commonly causes redness; tolerability is relative, not an absence of adverse effects. Ripasudil availability differs by country.',
'No patient can experience ocular redness~This is contradicted by known class effects.',
'They are muscarinic antagonists that produce cycloplegia~Their mechanism is trabecular Rho kinase inhibition.',
'They primarily raise IOP through aqueous overproduction~They lower outflow resistance.',
'They regenerate a destroyed optic nerve~Lowering IOP limits further damage but does not restore lost axons.'])

pool('retinaCell','''Rod photoreceptor~Rods have high light sensitivity, support scotopic vision, lack color discrimination, and are absent from the central foveola; they converge for sensitivity at the cost of acuity.
Cone photoreceptor~Cones support daylight color vision and high acuity, are concentrated in the fovea, and require greater light intensity than rods.
ON bipolar cell~ON bipolar cells are depolarized by light-induced reduction of photoreceptor glutamate through a sign-inverting mGluR6 pathway.
OFF bipolar cell~OFF bipolar cells have sign-preserving ionotropic glutamate responses and are relatively hyperpolarized by reduced photoreceptor glutamate in light.
Retinal ganglion cell~Ganglion cells generate action potentials whose axons form the optic nerve; photoreceptors and bipolar cells mainly signal with graded potentials.
Retinal pigment epithelium~RPE supports photoreceptors, participates in the visual cycle, and maintains outer retinal homeostasis; it is not the principal action-potential output neuron.
Horizontal cell~Horizontal cells participate in lateral retinal processing, helping shape contrast and receptive fields rather than carrying optic nerve axons.''')
block('va','Retinal cell functions','retinaCell','''5,6|Which photoreceptor is most important for detecting a faint object on a moonless night?|Rod photoreceptor|Rods have low light thresholds and large amounts of rhodopsin, making them sensitive in dim illumination. They do not encode color and have lower spatial acuity.
5,6,15|Which photoreceptor supports high-acuity color vision in bright daylight?|Cone photoreceptor|Cones have wavelength-selective photopsins and are concentrated at the fovea. They require higher light levels than rods.
5,6|Which photoreceptor is absent from the central foveola and contributes little to fine central color discrimination?|Rod photoreceptor|The central foveola is cone dominated and lacks rods. Rods are optimized for sensitivity rather than fine color detail.
5,6|Which cells are densely packed in the fovea and support reading small print under adequate illumination?|Cone photoreceptor|Foveal cone density and limited convergence support high acuity. Rod convergence improves sensitivity while reducing spatial precision.
9,10,12|Reduced glutamate release from a light-stimulated rod depolarizes the bipolar pathway highlighted in the lecture. Which bipolar class is meant?|ON bipolar cell|The rod-to-ON bipolar synapse is sign inverting. Reduced glutamate relieves mGluR6-mediated suppression and depolarizes the ON bipolar cell; not all bipolar cells behave this way.
10,11|A bipolar cell has ionotropic glutamate receptors and becomes less depolarized when a photoreceptor releases less glutamate. Which class is described?|OFF bipolar cell|OFF bipolar cells are sign preserving and typically hyperpolarize when light reduces glutamate. This qualifies the slide shorthand that glutamate inhibits all bipolar cells.
10,12|Which retinal neurons send action potentials along axons that form the optic nerve?|Retinal ganglion cell|Ganglion cell output is spiking. Rods, cones, and bipolar cells mainly communicate through graded changes in voltage and transmitter release.
8,13,14|Which retinal support tissue is crucial to recycling the retinal chromophore for photopigment regeneration?|Retinal pigment epithelium|The RPE participates in the visual cycle that restores usable 11-cis-retinal. Vitamin A supply and intact recycling support photoreceptor function.
6|Which photoreceptor contributes to the slower, more sensitive phase of dark adaptation?|Rod photoreceptor|Cones adapt earlier, while rods dominate the later phase as sensitivity increases. This accounts for the classic biphasic dark-adaptation curve.
6|Which photoreceptor contributes to the earlier phase of dark adaptation?|Cone photoreceptor|Cone sensitivity improves relatively early, but rods later achieve much lower light thresholds.''')
custom('va','Photoreceptor structure','5','Which photoreceptor compartment contains the light-sensitive pigment-rich membranes?',[
'Outer segment~Pigment-bearing discs or membrane infoldings capture photons. Inner segments contain metabolic organelles, and terminals communicate with retinal interneurons.',
'Synaptic terminal only~The terminal releases transmitter but is not the principal pigment-bearing light-capture compartment.',
'Optic nerve axon~Photoreceptors do not send their own axons into the optic nerve.',
'Ciliary muscle~This changes lens shape for accommodation rather than housing retinal pigment discs.',
'Corneal epithelium~This protects the eye surface and is not a photoreceptor segment.'])
custom('va','Photoreceptor structure','5','Which compartment provides much of the photoreceptor’s metabolic machinery?',[
'Inner segment~The inner segment contains mitochondria and other organelles that support the metabolically demanding outer segment and synapse.',
'Only the outer segment lumen~The outer segment specializes in phototransduction membranes rather than housing all metabolic organelles.',
'Only the aqueous humor~Aqueous is not the photoreceptor’s organelle-containing compartment.',
'Only the optic chiasm~The chiasm carries retinal ganglion axons and is not part of a photoreceptor cell.',
'Only the lens nucleus~The lens refracts light and does not supply photoreceptor organelles.'])
custom('va','Photoreceptor pigment','8','What are the two molecular components of rhodopsin?',[
'Opsin protein and 11-cis-retinal~Retinal is a vitamin-A-derived chromophore; bound to rod opsin it forms rhodopsin, the light-sensitive pigment.',
'Opsin protein and acetylcholine~Acetylcholine is not the rhodopsin chromophore.',
'Transducin and glutamate~Transducin is a signaling G protein and glutamate is transmitter, not the pigment pair.',
'Arrestin and cGMP~These participate in shutoff and channel signaling rather than constituting rhodopsin.',
'Retinoic acid and collagen~These do not form the rod visual pigment.'])
custom('va','Photoreceptor pigment','8,10,11','What is the initial chromophore change after rhodopsin absorbs light?',[
'11-cis-retinal isomerizes to all-trans-retinal~This drives a conformational change in opsin and the activated metarhodopsin II state, initiating transducin signaling.',
'All-trans-retinal directly becomes glutamate~Retinal is a chromophore and does not turn into the synaptic transmitter.',
'cGMP directly converts to vitamin A~cGMP is hydrolyzed to GMP downstream, not converted into vitamin A.',
'Opsin is immediately phosphorylated to create the first active state~Photoisomerization activates the pigment; kinase phosphorylation helps terminate signaling.',
'Calcium becomes potassium~Ions are not converted into one another during phototransduction.'])
pool('photoStep','''High cGMP with open cyclic-nucleotide-gated channels~This is the dark-state condition, allowing inward cation current and relative photoreceptor depolarization.
Activated rhodopsin stimulates transducin~Light-activated pigment engages the G protein upstream of phosphodiesterase; kinase phosphorylation is not the activating step.
Phosphodiesterase hydrolyzes cGMP~PDE activation reduces cGMP and closes cyclic-nucleotide-gated channels during the light response.
Closure of outer-segment cation channels~Reduced inward Na+/Ca2+ current shifts the photoreceptor toward hyperpolarization while outward current continues.
Reduced photoreceptor glutamate release~Hyperpolarization decreases calcium-dependent synaptic release, changing bipolar signaling in a receptor-dependent manner.
Rhodopsin phosphorylation and arrestin binding~These shut down activated pigment and reduce further transducin activation, helping terminate the light response.
Restoration of cGMP and pigment readiness~Recovery requires signaling shutoff, cGMP restoration, and visual-cycle support; returning dark current is not due to sustained PDE activity.''')
block('va','Phototransduction sequence','photoStep','''9|What intracellular condition maintains the rod dark current?|High cGMP with open cyclic-nucleotide-gated channels|In darkness, relatively high cGMP keeps outer-segment cation channels open. Inward Na+/Ca2+ current maintains a relatively depolarized state and tonic transmitter release.
10,11|Immediately downstream of metarhodopsin II, which signaling event initiates the G-protein cascade?|Activated rhodopsin stimulates transducin|Transducin is the G protein, not an enzyme called 'transduction.' Activated transducin stimulates the cGMP phosphodiesterase pathway.
10,11|What enzymatic step lowers cGMP during phototransduction?|Phosphodiesterase hydrolyzes cGMP|Activated PDE converts cGMP to GMP, decreasing channel-opening ligand. Lower cGMP closes outer-segment cation channels.
10,11|Which membrane event directly reduces the photoreceptor dark current after cGMP falls?|Closure of outer-segment cation channels|The cyclic-nucleotide-gated channels carry Na+ and Ca2+ inward. Closing them reduces inward positive current and hyperpolarizes the cell.
10,12|What synaptic change follows rod hyperpolarization in light?|Reduced photoreceptor glutamate release|Hyperpolarization reduces synaptic calcium entry and glutamate release. This depolarizes the ON pathway while affecting OFF cells differently.
11,12|What function do rhodopsin kinase and arrestin serve?|Rhodopsin phosphorylation and arrestin binding|GRK1 phosphorylation followed by arrestin binding quenches light-activated rhodopsin. The source slide incorrectly describes phosphorylation as the activation event.
11,12|After the light response ends, what helps restore open cyclic-nucleotide-gated channels?|Restoration of cGMP and pigment readiness|Signal termination and cGMP replenishment permit cation channels to reopen. Continued PDE activity would instead keep cGMP low.
9,10,11|Which state is expected if cGMP phosphodiesterase is experimentally inhibited during a flash?|High cGMP with open cyclic-nucleotide-gated channels|Preventing cGMP hydrolysis blunts normal channel closure and hyperpolarization. The response will differ from an intact light cascade.
10,11|A loss-of-function mutation prevents transducin from activating PDE. Which normal step is directly lost?|Phosphodiesterase hydrolyzes cGMP|Without downstream PDE activation, the normal light-induced cGMP fall is impaired. The initial pigment photoisomerization can still occur.
11,12|A rod lacks functional arrestin. Which normal process is impaired, prolonging the light response?|Rhodopsin phosphorylation and arrestin binding|Arrestin normally caps phosphorylated activated pigment and blocks further transducin engagement. Loss slows response termination.''')
pool('voltage','''Depolarization with increased glutamate release~This is the response to greater inward depolarizing current or the relative dark state, not the usual photoreceptor response to light.
Hyperpolarization with decreased glutamate release~This is the usual rod/cone response to light: cGMP falls, cation channels close, and transmitter release decreases.
Depolarization with decreased glutamate release~This is not the ordinary direct voltage-release relationship at a photoreceptor synapse, though downstream ON cells depolarize when glutamate falls.
Hyperpolarization with increased glutamate release~The ordinary photoreceptor relationship is the opposite: hyperpolarization reduces calcium entry and release.
No voltage or transmitter change~A functional photoreceptor light response changes graded voltage and transmitter output; it is not electrically silent.''')
block('va','Dark and light predictions','voltage','''9,12|What best describes a rod when moving from bright light into darkness?|Depolarization with increased glutamate release|cGMP rises and outer-segment cation channels reopen. The rod becomes less negative and releases more glutamate than during bright stimulation.
10,11,12|What best describes a rod’s response to increased illumination?|Hyperpolarization with decreased glutamate release|Light reduces cGMP, closes cation channels, and decreases transmitter release. Photoreceptors respond with graded potentials rather than spikes.
9,10|An experiment rapidly lowers intracellular cGMP in an isolated rod. If cyclic-nucleotide-gated channel activation falls, what response is expected?|Hyperpolarization with decreased glutamate release|Closing the inward cation current makes the cell more negative and reduces transmitter output. Physiologically, light lowers intracellular cGMP through PDE.
9,10|A cGMP analog persistently holds rod outer-segment channels open despite illumination. Which tendency is expected?|Depolarization with increased glutamate release|Maintaining inward current opposes normal light-induced hyperpolarization and preserves relatively greater transmitter release.
10,11|A bright flash closes many cGMP-gated channels while outward potassium conductance continues. What is expected?|Hyperpolarization with decreased glutamate release|The balance shifts toward outward positive current, making the cell more negative and reducing calcium-dependent release.''')
custom('va','Photoreceptor voltages','9,10','The lecture uses about -30 mV in darkness and -70 mV in bright light. What is the important physiologic relationship?',[
'The dark state is relatively depolarized and light shifts the cell more negative~The precise voltages depend on conditions; the central prediction is hyperpolarization in light, not a photoreceptor action potential.',
'The dark state is more negative than the light state~This reverses the central relationship.',
'Light always produces a large positive action potential in rods~Rods mainly generate graded receptor potentials.',
'Both values mean the cell must be electrically identical~A substantial voltage change alters transmitter release.',
'Glutamate release rises because -70 mV is more depolarized~-70 mV is more negative than -30 mV and decreases ordinary synaptic release.'])
custom('va','ON and OFF pathways','9,10,11,12','Why is “glutamate inhibits bipolar cells” an incomplete general statement?',[
'ON and OFF bipolar cells express different receptor/signaling arrangements~ON bipolar cells invert the photoreceptor signal through mGluR6; OFF cells use sign-preserving ionotropic receptors. The rod ON pathway fits the lecture’s inhibitory shorthand.',
'All bipolar cells lack glutamate receptors~They do respond to photoreceptor glutamate.',
'Glutamate is never released by photoreceptors~It is their principal transmitter.',
'Only the optic nerve releases retinal glutamate~Photoreceptor synapses are a key retinal glutamatergic site.',
'ON and OFF cells always have identical light responses~Their opposing responses are central to retinal contrast processing.'])
custom('va','Retinal signaling','10,12','Which comparison between photoreceptors and ganglion cells is correct?',[
'Photoreceptors use graded potentials; ganglion axons carry action potentials~Graded photoreceptor voltage regulates glutamate release. Spiking ganglion output then transmits visual information through the optic nerve.',
'Both mainly transmit to the brain by diffusion of retinal chromophore~Chromophore recycling does not carry the neural visual signal.',
'Photoreceptors form the optic nerve directly~Ganglion cell axons form the nerve.',
'Ganglion cells capture light through rhodopsin as their main ordinary role~Rods and cones are the major image-forming photoreceptors; ganglion output integrates retinal signals.',
'Bipolar cells are all located in the optic chiasm~Bipolar neurons are within the retina.'])
custom('va','Vitamin A deficiency','13,14','A patient with fat malabsorption has trouble seeing at dusk but relatively preserved daylight acuity. Which mechanism best explains the early symptom?',[
'Inadequate retinal chromophore reduces rod rhodopsin availability~Vitamin A supplies retinal for photopigments. Rod dysfunction causes nyctalopia before severe cone/ocular surface involvement necessarily develops.',
'Excess acetylcholine contracts the iris sphincter in every case~That is not the primary vitamin A deficiency mechanism.',
'Selective destruction of the optic chiasm~That causes a field pattern rather than typical nutrition-related night blindness.',
'A blocked external auditory canal~That affects hearing rather than photopigment supply.',
'Excess cGMP synthesis guarantees normal night vision~Without adequate pigment, sensitivity is impaired despite downstream signaling components.'])
custom('va','Vitamin A deficiency','14','Why may night blindness take months to develop after vitamin A intake falls?',[
'Liver stores buffer supply until reserves are depleted~Substantial hepatic vitamin A stores can delay deficiency manifestations. Time course varies with initial stores and absorption.',
'Retinal never depends on systemic vitamin A~Vitamin A is required for retinal chromophore supply.',
'Rods regenerate the entire vitamin indefinitely without any dietary requirement~Recycling conserves chromophore but does not remove the nutritional requirement.',
'All deficiency symptoms require decades in every patient~Infants or severe malabsorption can deplete reserves more quickly.',
'Only the lens stores all vitamin A~The lecture emphasizes hepatic reserves, not the lens.'])
custom('va','Vitamin A deficiency','14','The source slide depicts white foamy ocular surface patches in vitamin A deficiency. What are these findings most consistent with?',[
'Bitot spots from conjunctival epithelial changes~These are conjunctival surface lesions associated with xerophthalmia, distinct from retinal blind spots or a scotoma. The slide’s generic blind spots wording is imprecise.',
'Drusen beneath the retinal pigment epithelium~Drusen are fundus deposits rather than foamy conjunctival patches.',
'Glaucomatous optic nerve cupping~That is a posterior optic disc change.',
'A bitemporal visual field defect~A field pattern cannot be identified as a conjunctival patch.',
'A middle-ear effusion~That is an otoscopic rather than ocular surface finding.'],'figure-bitot')
custom('va','Vitamin A deficiency','14','Which statement about treatment of vitamin A deficiency-related night blindness is most accurate?',[
'Repletion can improve reversible rod dysfunction, but route and recovery depend on clinical context~Oral treatment is common; severe malabsorption or other circumstances may require a parenteral route. The slide’s rapid IV response is not a universal dosing or recovery promise.',
'Every patient must receive IV vitamin A immediately without assessing dose or cause~Route and dose require clinical assessment; excess vitamin A can be toxic.',
'All structural corneal damage reverses within minutes~Established tissue injury may persist.',
'No visual symptom can improve with repletion~Reversible pigment-related dysfunction can improve.',
'Vitamin A treatment only works by lowering IOP~The main mechanism here is restoration of chromophore availability.'])
custom('va','Color vision','15','A boy has lifelong bilateral red-green discrimination difficulty with normal visual acuity and no progression. Which mechanism is most likely?',[
'An inherited abnormality of cone opsin genes, commonly X linked~Common red-green deficiency affects cone pigment discrimination. Rods do not distinguish colors, and ordinary acuity can remain normal.',
'Vitamin A depletion exclusively destroying rods~That causes dim-light dysfunction rather than the classic stable inherited red-green pattern.',
'An acute left optic tract infarct~That produces a contralateral field defect rather than lifelong bilateral color deficiency.',
'A conductive middle-ear lesion~This affects hearing, not color vision.',
'Loss of all cone cells causing complete central blindness~Common red-green deficiencies do not require complete cone destruction.'])
custom('va','Visual perception','17','A patient detects lines and light but cannot identify familiar visual objects after a cortical lesion. Which distinction is illustrated?',[
'Visual sensation can be present while cortical interpretation is impaired~Perception organizes sensory input into meaningful objects, faces, motion, depth, and color. Normal detection alone does not guarantee normal recognition.',
'Perception occurs entirely in the lens~The lens focuses light; cortical networks interpret it.',
'A normal retina guarantees recognition of every object~Cortical processing can be impaired despite retinal input.',
'Visual interpretation requires no neural processing~Meaningful recognition depends on brain function.',
'All recognition failure must be cataract~Media opacity reduces image quality but does not explain every cortical perceptual deficit.'])
custom('va','Depth perception','18,19','How does binocular stereopsis arise?',[
'The cortex compares and fuses the slightly different images from the two eyes~Binocular disparity supplies depth information. Monocular cues such as perspective and motion parallax also support depth judgments, so monocular vision does not eliminate every depth cue.',
'Both eyes must receive exactly identical images with no disparity~Small differences are the key stereoscopic signal.',
'The lens directly calculates object meaning~The lens performs optical focusing, not cortical fusion.',
'The cochlear nuclei fuse retinal signals~They process auditory input rather than stereopsis.',
'One eye cannot support any depth judgment of any kind~Monocular cues remain despite loss of true binocular stereopsis.'])
custom('va','Visual field localization','19','Complete destruction of the left optic nerve causes which primary field deficit?',[
'Left monocular vision loss~The optic nerve carries all retinal output from its eye before the chiasm. Binocular stereopsis is lost, though monocular depth cues remain.',
'Right homonymous hemianopia~That indicates a left retrochiasmal lesion, not isolated left optic nerve loss.',
'Bitemporal hemianopia~That suggests central chiasmal crossing-fiber injury.',
'Left homonymous hemianopia~That suggests a right retrochiasmal lesion.',
'Only right monocular blindness~That reverses the affected eye.'])
custom('va','Visual field localization','19','A stroke destroys the left primary visual cortex. Which field deficit is expected?',[
'Right homonymous hemianopia~Left retrochiasmal pathways represent the right visual hemifield from both eyes. Macular sparing may occur in some occipital lesions but is not mandatory.',
'Left monocular blindness~This would localize before the chiasm on the left.',
'Right monocular blindness~This would localize before the chiasm on the right.',
'Bitemporal hemianopia~This is characteristic of central optic chiasm injury.',
'Left homonymous hemianopia~That points to a right retrochiasmal lesion.'])
custom('va','Visual field localization','19','A lesion behind the optic chiasm affects one side of the visual pathway. Which general pattern is most likely?',[
'Loss of the contralateral visual hemifield in both eyes~Retrochiasmal pathways carry corresponding hemifields from both eyes, producing homonymous defects.',
'Loss of all vision only in the ipsilateral eye~That is an optic nerve/pre-chiasmal pattern.',
'Loss of all vision only in the contralateral eye~That does not match ordinary retrochiasmal organization.',
'Only a lens accommodation deficit~Accommodation is not the defining retrochiasmal field deficit.',
'Only reduced hearing on one side~This is a visual pathway lesion.'])

pool('earStructure','''External ear~The pinna and canal collect/direct airborne sound toward the tympanic membrane; they do not contain the main balance receptors.
Middle ear~The tympanic membrane/ossicular system transmits and impedance-matches sound to inner-ear fluid through the oval window.
Scala vestibuli~This perilymph-filled compartment begins at the oval window and lies above the cochlear duct.
Scala media~The cochlear duct contains potassium-rich endolymph and the organ of Corti’s apical sensory environment.
Scala tympani~This perilymph-filled compartment lies below the basilar membrane and communicates with the round window.
Basilar membrane~This supports the organ of Corti and separates scala media from scala tympani; stiffness varies from base to apex.
Reissner membrane~This separates scala vestibuli from scala media and helps maintain their distinct fluid compartments.
Tectorial membrane~This overlies cochlear hair cells and participates in relative shear that bends stereocilia, especially of outer hair cells.
Round window~This compliant interface permits pressure displacement as the stapes moves at the oval window; it is not the site of stapes insertion.
Stria vascularis~This lateral cochlear duct tissue maintains potassium-rich endolymph and the endocochlear potential.''')
block('va','Ear and cochlear anatomy','earStructure','''21,22|Which region collects and directs airborne sound before it reaches the eardrum?|External ear|The pinna and external auditory canal conduct sound toward the tympanic membrane. Hearing and balance receptors themselves are deeper in the inner ear.
22,28,36|Which ear region provides mechanical impedance matching between air and cochlear fluid?|Middle ear|Ossicular leverage and the tympanic membrane-to-stapes area relationship increase pressure at the oval window, improving air-to-fluid energy transfer.
24|Which cochlear compartment contains potassium-rich endolymph?|Scala media|The cochlear duct has high potassium endolymph. Scala vestibuli and tympani contain perilymph with a more extracellular-fluid-like ionic composition.
24|Which compartment receives stapes-driven pressure waves at the oval window?|Scala vestibuli|The oval window interfaces with scala vestibuli perilymph. Waves then produce differential pressure and basilar membrane motion.
24|Which fluid compartment lies below the basilar membrane and terminates at the round window?|Scala tympani|Scala tympani contains perilymph. The round window provides a compliant pressure outlet.
24,25|Which membrane separates the cochlear duct from scala tympani and supports the organ of Corti?|Basilar membrane|The basilar membrane is the frequency-selective mechanical platform for the sensory organ, unlike Reissner membrane above the duct.
24|Which membrane separates scala vestibuli from scala media?|Reissner membrane|The vestibular/Reissner membrane partitions perilymph above from endolymph in the cochlear duct.
25,32|Which structure overlies the hair bundles and participates in relative shear during cochlear motion?|Tectorial membrane|Relative motion among the organ of Corti, basilar membrane, and tectorial membrane deflects hair bundles. Outer hair bundles are embedded more directly than inner bundles.
24,28,36|Which window accommodates fluid displacement rather than receiving the stapes footplate?|Round window|Because inner-ear fluid is poorly compressible, a compliant round window allows displacement as the stapes moves at the oval window.
24|Which tissue maintains endolymph ionic composition and the endocochlear potential?|Stria vascularis|The stria vascularis supports the electrochemical driving force for hair-cell transduction. Loop diuretic toxicity can disrupt this function.''')
custom('va','Cochlear supporting cells','26','Which supporting cells are also called outer phalangeal cells and support outer hair cells?',[
'Deiters cells~These supporting cells stabilize outer hair cells. The slide’s pharyngeal wording is a typo for phalangeal.',
'Spiral ganglion neurons~These are afferent neuronal cell bodies rather than outer hair-cell supports.',
'Retinal bipolar cells~These are in the eye, not the cochlea.',
'Vestibular dark cells~These maintain vestibular fluid homeostasis rather than serving as Deiters cells.',
'Ossicular osteocytes~Bone cells are not the named organ of Corti supporting-cell class.'])
custom('va','Cochlear supporting cells','26','Which cells help form the tunnel of Corti?',[
'Inner and outer pillar cells~The lecture emphasizes outer pillar cells; together with inner pillar cells they form the tunnel’s supporting architecture.',
'Cochlear nerve Schwann cells only~These support axons rather than form the organ’s pillar tunnel.',
'Only stria vascularis marginal cells~These participate in fluid/ionic homeostasis.',
'Only retinal pigment cells~These are not cochlear supporting cells.',
'Only stapes osteoblasts~These are bone-forming cells, not organ of Corti pillars.'])
custom('va','Acoustic conduction','28,36','Which sequence correctly traces mechanical sound transmission?',[
'Canal, tympanic membrane, malleus, incus, stapes, oval window~The ossicular chain transmits and amplifies pressure before fluid displacement drives cochlear mechanics.',
'Canal, stapes, malleus, incus, round window~This misorders the chain and places the stapes at the wrong window.',
'Canal, cochlear nerve, tympanic membrane, cortex~Mechanical transmission precedes hair-cell and neural signaling.',
'Tympanic membrane, round window, incus, retina~This sequence mixes unrelated structures and incorrect interfaces.',
'Canal, scala media air, vestibular cortex, stapes~The scala media is fluid-filled and the sequence is not the sound-conduction path.'])
custom('va','Acoustic conduction','28','What is the helicotrema?',[
'An apical communication between scala vestibuli and scala tympani~Very low-frequency pressure changes can pass around the apex. The scala media retains a separate endolymphatic compartment.',
'The opening from ear canal into the middle ear~That is not the helicotrema; the intact tympanic membrane separates these spaces.',
'A direct passage through the stapes footplate~The helicotrema is at the cochlear apex, not the oval window.',
'A retinal membrane that contains rhodopsin~It is an inner-ear structure, not part of the retina.',
'The tunnel between pillar cells~That is the tunnel of Corti, not the communication of perilymphatic scalae.'])
pool('tonotopy','''Basal narrow stiff membrane~The cochlear base near the oval window has high mechanical stiffness and responds best to high frequencies.
Apical wide compliant membrane~The cochlear apex is broader and more flexible, with peak responses to lower frequencies.
Intermediate cochlear region~Middle frequencies peak between the extreme base and apex; the map is continuous rather than divided into only three discrete sites.
Uniform response at every cochlear position~This would eliminate place coding and is inconsistent with the stiffness gradient and traveling-wave peaks.
Frequency coded only by sound amplitude~Amplitude primarily relates to intensity; it does not replace the cochlear place code for pitch.''')
block('va','Tonotopy and traveling waves','tonotopy','''29,30,31|Where does a 10-kHz tone produce its greatest basilar membrane response?|Basal narrow stiff membrane|High frequencies peak near the cochlear base. The base is narrow and stiff compared with the apex.
29,30,31|Where does a low-frequency tone around 100 Hz produce its greatest response?|Apical wide compliant membrane|Low-frequency waves travel farther toward the compliant apex before peaking. They do not simply have zero motion everywhere at the base.
31|Where does a middle-frequency tone peak relative to very low and very high tones?|Intermediate cochlear region|The traveling-wave peak lies between basal high-frequency and apical low-frequency regions. The lecture uses about 800–1000 Hz as an illustrative middle example.
29,30|What cochlear structure/location is most vulnerable when basal hair-cell injury first causes high-frequency loss?|Basal narrow stiff membrane|The basal place code represents high pitches. The stiffness gradient is the key principle; a blanket claim that all high-frequency distinctions are easier is not required.
29,31|Which mechanical region is wider and less stiff than the basal turn?|Apical wide compliant membrane|The apical region supports low-frequency resonance. This mechanical gradient helps create a tonotopic map.''')
pool('hairCell','''Inner hair cells~Inner hair cells provide most afferent sensory information to spiral ganglion neurons and are the principal auditory receptor output cells.
Outer hair cells~Outer hair-cell electromotility amplifies and sharpens basilar motion and is subject to efferent modulation; their injury reduces sensitivity and tuning.
Deiters supporting cells~These support outer hair cells mechanically rather than serving as the principal afferent sound receptors.
Spiral ganglion neurons~Their cell bodies receive hair-cell input and their axons form the cochlear nerve; they generate neural action potentials downstream.
Vestibular hair cells~These transduce head movement/gravity signals rather than the cochlear frequency map.''')
block('va','Hair-cell roles','hairCell','''25,32|Which cells provide the majority of sensory afferent input for ordinary hearing?|Inner hair cells|Inner hair cells communicate through glutamate with spiral ganglion afferents. Outer hair cells primarily amplify mechanical tuning.
32|Which cells change length to amplify and sharpen basilar membrane vibration?|Outer hair cells|Outer hair-cell electromotility improves sensitivity and frequency selectivity. Efferent pathways can modulate the amplifier.
25,39|Which neurons send axons that form the cochlear branch of CN VIII?|Spiral ganglion neurons|These bipolar sensory neurons relay hair-cell output to ipsilateral cochlear nuclei before higher bilateral auditory processing.
26|Which cells stabilize the outer hair-cell rows rather than generating the primary auditory afferent signal?|Deiters supporting cells|Supporting cells help maintain the mechanical and cellular organization of the organ of Corti.
32|A drug preferentially damages the cochlear amplifier while leaving many inner hair cells initially intact. Which cells are primarily injured?|Outer hair cells|Outer hair-cell dysfunction raises thresholds and broadens tuning even if some afferent sensory transduction remains.''')
pool('hairResponse','''Depolarization with increased glutamate and afferent firing~Deflection toward the tallest stereocilia opens mechanotransduction channels; potassium enters from endolymph and promotes calcium-dependent release.
Hyperpolarization with decreased glutamate and afferent firing~Deflection away from the tallest stereocilia closes channels and reduces sensory output.
Depolarization caused primarily by potassium efflux at the apical bundle~The high-potassium endolymphatic environment drives potassium inward through apical channels, not the proposed outward depolarizing current.
No baseline activity and an all-or-none hair-cell spike~Hair cells normally have graded potentials and some resting transduction; spikes occur in afferent neurons.
Hyperpolarization with increased synaptic release~Ordinary hair-cell hyperpolarization reduces voltage-dependent calcium entry and release rather than increasing it.''')
block('va','Auditory mechanotransduction','hairResponse','''33,34,37|A cochlear hair bundle bends toward its tallest stereocilia. What response follows?|Depolarization with increased glutamate and afferent firing|Tip-link tension opens mechanically gated channels. Potassium-rich endolymph drives inward cation current, followed by basal calcium entry and increased release.
35,37|A hair bundle bends away from its tallest stereocilia. What response follows?|Hyperpolarization with decreased glutamate and afferent firing|Reduced tip-link tension closes mechanotransduction channels, decreasing inward current and transmitter output.
33|A drug increases the fraction of open hair-bundle channels at rest. What direction of response is expected?|Depolarization with increased glutamate and afferent firing|Some hair-cell channels are open at rest, permitting tonic output. Increasing opening increases depolarizing current and release; baseline firing allows bidirectional modulation rather than only an on/off response.
34,37|A sound deflects the bundle in the excitatory direction and increases synaptic calcium entry. Which downstream result is expected?|Depolarization with increased glutamate and afferent firing|Increased calcium promotes glutamate exocytosis onto cochlear afferents. Neural firing changes encode the mechanically transduced signal.
35|An experiment closes hair-bundle mechanotransduction channels while other conductances remain. Which result is expected?|Hyperpolarization with decreased glutamate and afferent firing|Removing inward depolarizing current reduces receptor voltage, calcium entry, and transmitter release.''')
custom('va','Auditory mechanotransduction','34','Why does opening apical potassium-permeable channels depolarize cochlear hair cells?',[
'Potassium-rich endolymph and its positive potential drive potassium into the cell~The unusual apical electrochemical environment differs from ordinary low-potassium extracellular fluid. Basolateral potassium exit then helps repolarize the cell.',
'Potassium concentration is zero in endolymph~Endolymph is potassium rich.',
'Potassium is actively transformed into sodium~Ions are not chemically converted during transduction.',
'The apical channel only carries outward potassium~The relevant transduction current is inward under normal conditions.',
'The cochlear duct contains only air~It contains endolymph, not air.'])
custom('va','Auditory mechanotransduction','34,37','Which event couples hair-cell depolarization to glutamate release?',[
'Opening of basal voltage-gated calcium channels~Calcium influx triggers synaptic vesicle fusion at the hair-cell ribbon synapse onto afferent fibers.',
'Closure of every calcium channel~That would reduce, rather than promote, release.',
'Release of rhodopsin into the synapse~Rhodopsin is a retinal pigment, not the cochlear transmitter.',
'Conversion of glutamate into endolymph~Glutamate is released as transmitter, not converted into bulk fluid.',
'An action potential traveling from cortex back into the stapes~This is not the local excitation-release sequence.'])
custom('va','Auditory mechanotransduction','33,34,35','What role do tip links play in cochlear hair bundles?',[
'They couple bundle displacement to mechanotransduction channel gating~Deflection toward the tallest row increases tension and channel opening; deflection away reduces tension and opening.',
'They are the axons forming the optic nerve~They are mechanical hair-bundle connections.',
'They synthesize glutamate from cGMP~They do not serve as that enzyme.',
'They connect the stapes directly to the auditory cortex~They are microscopic bundle structures rather than a macroscopic conduction tract.',
'They are retinal pigment discs~Those are photoreceptor structures.'])
custom('va','Auditory mechanotransduction','32,33','Which qualification is important when reading that the tallest stereocilium touches the tectorial membrane?',[
'Outer hair bundles are embedded, while inner hair bundles are generally driven by local fluid/shear motion~The slide is a useful simplified mechanical model but should not imply that every inner hair bundle is identically embedded.',
'No cochlear hair cell experiences mechanical bending~Bundle deflection is central to auditory transduction.',
'All auditory hair cells retain a mature kinocilium~Mature mammalian cochlear hair cells lack a kinocilium; stereociliary orientation still defines polarity.',
'The tectorial membrane is the same as the tympanic membrane~They are separate inner- and middle-ear structures.',
'Inner hair cells are in the external canal~They reside in the organ of Corti.'])
custom('va','Sensory comparison','10,34','Which comparison of light and excitatory cochlear bundle deflection is correct?',[
'Light hyperpolarizes photoreceptors; excitatory bundle deflection depolarizes hair cells~Both change graded receptor potentials and glutamate output, but their initial voltage responses to the respective stimuli are opposite.',
'Both always hyperpolarize their receptor cells~Excitatory hair-bundle deflection depolarizes.',
'Both always depolarize their receptor cells~Light usually hyperpolarizes rods and cones.',
'Both receptors transmit to the brain by their own long spiking axons~Ganglion/afferent neurons carry the long-distance action potentials.',
'Neither uses synaptic transmitter release~Both employ transmitter release onto downstream neurons.'])

pool('auditoryPath','''Cochlear nuclei~These are the first central auditory synapses at the pontomedullary region; input from each auditory nerve initially enters its ipsilateral nuclei.
Medial superior olive~This binaural circuit is especially important for interaural timing differences, useful for low-frequency sound localization.
Lateral superior olive~This circuit compares interaural level/intensity differences, particularly for high frequencies where head shadow is important.
Lateral lemniscus~This ascending brainstem auditory tract carries predominantly contralateral but bilateral-derived information toward the inferior colliculus.
Inferior colliculus~This midbrain auditory integration center contributes to orienting/reflex processing and projects toward the medial geniculate body.
Medial geniculate body~This thalamic auditory relay sends information toward auditory cortex; the lateral geniculate body is visual.
Primary auditory cortex~Heschl transverse temporal cortex, chiefly BA41 with adjacent BA42 auditory processing, supports tonotopic conscious sound analysis.
Spiral ganglion~These peripheral auditory sensory neuron bodies relay cochlear hair-cell information into the cochlear nerve.''')
block('va','Auditory pathway localization','auditoryPath','''39|Where does the cochlear nerve make its first central synapse?|Cochlear nuclei|Dorsal and ventral cochlear nuclei receive ipsilateral CN VIII input before ascending projections distribute information bilaterally.
39|Which binaural center is particularly important for interaural time differences at lower frequencies?|Medial superior olive|Time differences provide useful low-frequency localization cues. The lateral superior olive emphasizes level differences.
39|Which binaural center particularly uses interaural intensity differences for high-frequency localization?|Lateral superior olive|High-frequency head-shadow differences help lateralization. The LSO integrates excitation and inhibition to compare ear levels.
40|Which ascending tract connects lower auditory relays with the inferior colliculus?|Lateral lemniscus|The lateral lemniscus is an ascending brainstem tract, not confined exclusively to the midbrain. It carries information derived from both ears.
40|Which midbrain structure integrates auditory information and supports orienting to sound?|Inferior colliculus|The inferior colliculus is auditory; the superior colliculus is more strongly associated with visual orienting and multisensory functions.
40,41|Which thalamic nucleus relays auditory information to cortex?|Medial geniculate body|MGN/MGB is the auditory relay. The lateral geniculate nucleus relays vision.
41|Which cortical region receives the main thalamic auditory projection?|Primary auditory cortex|Heschl’s transverse temporal gyri contain primary auditory cortex, predominantly BA41. The lecture groups BA41/42 as the core/adjacent auditory region.
39|Where are the cell bodies of the neurons whose central axons form the cochlear nerve?|Spiral ganglion|Spiral ganglion afferents receive inner hair-cell input and carry frequency-coded information to brainstem cochlear nuclei.
39|A lesion selectively disrupts comparison of arrival timing between ears. Which circuit is most directly implicated?|Medial superior olive|Binaural timing comparison is especially associated with MSO circuitry, useful for localizing lower-frequency sounds.
39|A lesion impairs use of a high-frequency sound’s loudness difference across ears. Which circuit is implicated?|Lateral superior olive|The LSO contributes to interaural level comparison, especially where the head creates a substantial acoustic shadow.
41|Which auditory area preserves a frequency map that the lecture describes as posteromedial high frequencies and anterolateral low frequencies?|Primary auditory cortex|Tonotopy persists through the pathway. Cortical maps are more complex than a single strip, but the lecture’s orientation is a useful teaching description.
42,44,45|A focal lesion at the first central auditory relay causes marked ipsilateral hearing loss. Which site fits?|Cochlear nuclei|A lesion at or before the cochlear nuclei can interrupt information from one ear before robust bilateral distribution. Higher unilateral lesions rarely cause complete monaural deafness.''')
custom('va','Auditory pathway sequence','39,40,41,45','Which ordering follows the principal ascending auditory route?',[
'Spiral ganglion, cochlear nuclei, superior olive, lateral lemniscus, inferior colliculus, medial geniculate, auditory cortex~The pathway includes parallel and crossing routes, but this sequence summarizes the major relays.',
'Spiral ganglion, lateral geniculate, visual cortex, superior olive~The lateral geniculate and visual cortex are not the main auditory relays.',
'Cochlear nuclei, optic chiasm, inferior colliculus, retina~The optic chiasm and retina are visual structures.',
'Auditory cortex, middle ear, spiral ganglion, cochlear nuclei~This reverses the direction of the ordinary ascending sensory sequence.',
'Inner hair cell, vestibulospinal tract, motor endplate~This is not the conscious auditory pathway.'])
custom('va','Auditory lesion patterns','42,44,45','A complete lesion of the right cochlear nerve most directly produces which deficit?',[
'Marked right sensorineural hearing loss~The auditory nerve carries ipsilateral cochlear output before bilateral central projections. This is distinct from most higher unilateral lesions.',
'Complete left deafness with preserved right hearing~This reverses the peripheral nerve laterality.',
'Only a conductive air-bone gap~A nerve lesion is sensorineural, not a middle-ear transmission deficit.',
'Only bitemporal visual loss~This is a chiasmal visual pattern.',
'No hearing effect because all peripheral signals are bilateral before entering the nerve~Each cochlear nerve initially carries its own ear’s information.'])
custom('va','Auditory lesion patterns','43,45','A unilateral auditory cortex lesion is less likely than a cochlear nerve lesion to cause complete deafness in one ear. Why?',[
'Higher auditory pathways receive substantial bilateral input~Binaural ascending projections preserve basic hearing from both ears despite many higher unilateral lesions, while localization/discrimination may suffer.',
'The cortex receives no auditory information~Auditory cortex receives and processes thalamic auditory input.',
'The cochlear nerve already contains equal input from both cochleae~Bilateral distribution becomes substantial centrally, after initial ipsilateral entry.',
'Only the ossicles encode conscious sound meaning~Ossicles transfer mechanics; cortex interprets sound.',
'All cortical lesions leave every aspect of auditory processing normal~Complex processing can be impaired despite preserved thresholds.'])
custom('va','Auditory lesion patterns','43,44,45','A patient has profound isolated left-ear hearing loss. Which site is least likely to be the sole cause?',[
'Right primary auditory cortex alone~A single higher unilateral lesion usually does not eliminate hearing exclusively in one ear because of bilateral representation.',
'Left middle ear~A severe mechanical transmission lesion can substantially reduce left hearing through a conductive mechanism.',
'Left cochlea~Cochlear injury can cause severe ipsilateral SNHL.',
'Left cochlear nerve~This can markedly impair ipsilateral neural transmission.',
'Left cochlear nuclei~A complete early central relay lesion can cause major ipsilateral loss before bilateral distribution.'])
custom('va','Auditory processing','41,43','A patient detects sounds but has reduced sound localization and complex discrimination after a higher auditory lesion. Which interpretation is best?',[
'Bilateral input can preserve detection while central processing is impaired~Preserved thresholds do not mean every function of auditory cortex and pathways is intact. Speech-in-noise and temporal judgments may also suffer.',
'All auditory function is normal if a tone is detected~Detection is only one aspect of hearing.',
'The patient must have an isolated blocked ear canal~Central deficits can occur without a conductive lesion.',
'No CNS processing is needed for localization~Binaural and cortical networks contribute to localization.',
'A unilateral cortical lesion must create total ipsilateral deafness~That is not the usual higher unilateral lesion pattern.'])

block('av','Auditory foundations','hearingType','''14,15|A middle-ear lesion prevents efficient transfer of airborne sound energy into cochlear fluid. Which loss category is expected?|Conductive hearing loss|The external ear captures sound, the middle ear impedance-matches air to fluid, and the inner ear transduces fluid motion to neural activity. Failure of the transmission stage is conductive.
16,17|An experiment preserves ossicular motion but destroys the sensory apparatus that converts the resulting traveling wave into neural activity. Which loss category is expected?|Sensorineural hearing loss|The basilar traveling wave is the hydromechanical input to cochlear hair-cell transduction. Destroying sensory cells produces cochlear SNHL rather than a pure transmission gap.
19,20|A higher unilateral auditory lesion reduces localization and speech-in-noise performance without eliminating detection in either ear. Which category fits?|Central auditory processing impairment|Ascending auditory pathways distribute information bilaterally. The lecture gives simplified dorsal/ventral crossing patterns; the key clinical principle is bilateral representation above the initial cochlear input.''')
block('av','Cochlear place coding','tonotopy','''16,17,18|A high-frequency tone produces a traveling-wave maximum near the oval window. Which part of the basilar membrane is involved?|Basal narrow stiff membrane|The traveling-wave framework, associated with von Bekesy, links frequency to the place of maximal basilar displacement. High frequencies peak basally.
16,17,18|A low-pitch tone produces maximal displacement near the cochlear apex. Which region is involved?|Apical wide compliant membrane|Lower-frequency traveling waves peak farther along the wider, more flexible apical membrane. Tonotopy then persists in auditory neural coding.''')
custom('oph','Drug class members','4,10','Timolol, carteolol, and levobunolol belong to which glaucoma drug class?',[
'Beta-adrenergic antagonists~These agents reduce aqueous production. Betaxolol is a relatively beta-1-selective member; the others named here are nonselective.',
'Direct muscarinic agonists~Pilocarpine and carbachol are members of that class.',
'Carbonic anhydrase inhibitors~Acetazolamide, dorzolamide, and brinzolamide belong to that class.',
'Prostaglandin analogs~Latanoprost, travoprost, and bimatoprost-related therapy belong to that group.',
'Rho kinase inhibitors~Netarsudil and ripasudil are members of that class.'])
custom('oph','Drug class members','5,10','Apraclonidine and brimonidine are which receptor agonists?',[
'Alpha-2 agonists~They reduce aqueous synthesis, with uveoscleral outflow effects particularly relevant to brimonidine.',
'Alpha-1 agonists~Phenylephrine is the classic alpha-1 mydriatic.',
'M3 agonists~Pilocarpine and carbachol have direct muscarinic activity.',
'Beta-2 agonists~These would not describe the named alpha-2 pressure-lowering drugs.',
'Dopamine D2 agonists~This is not the glaucoma class of these agents.'])
custom('oph','Drug class members','7,10','Latanoprost, travoprost, and bimatoprost-related ocular therapy share which major effect?',[
'Increased uveoscleral aqueous outflow~These prostaglandin-related agents lower IOP through outflow enhancement and can cause pigmentation, redness, and lash changes.',
'Direct inhibition of acetylcholinesterase~That describes echothiophate.',
'Selective alpha-1-mediated dilation without cycloplegia~That describes phenylephrine.',
'Renal bicarbonate wasting as their principal ocular mechanism~That is systemic CA-inhibitor pharmacology.',
'Systemic osmotic extraction of ocular water~That is mannitol therapy.'])
custom('av','Ototoxic drug class members','49','Streptomycin, gentamicin, tobramycin, and amikacin share which clinically important class risk?',[
'Aminoglycoside cochlear and/or vestibular toxicity~Risk patterns differ among agents, but all can injure inner-ear structures. Basal outer hair cells and vestibular sensory cells are important targets.',
'Uniformly reversible salicylate-like toxicity only~Aminoglycoside damage can be permanent.',
'Selective external canal wax production~This is not the mechanism of their hearing/vestibular risk.',
'Direct therapeutic cochlear hair-cell regeneration~These drugs can damage rather than regenerate sensory cells.',
'Purely cortical visual field loss without inner-ear involvement~That does not capture the characteristic class toxicity.'])

block('av','Extended clinical cases','hearingDx','''3,4,33|A 3-year-old boy has had several documented episodes of acute otitis media during the past year. His parents now report that he turns up the television and does not always respond when called. He is afebrile and has no acute ear pain today. Otoscopy shows an intact dull amber membrane, and tympanometry is flat with a normal canal volume. Masked bone thresholds are near normal, while air thresholds are elevated. Which diagnosis best explains the persistent hearing problem between acute infections?|Otitis media with effusion|Persistent middle-ear fluid produces a conductive air-bone gap and a flat normal-volume tympanogram. It can affect functional hearing without fever or the bulging inflamed drum of an acute episode.|figure-effusion
6,7,34,46|A 7-month-old infant failed bilateral newborn hearing screening. ABR at three months showed profound loss, and repeated evaluation confirms minimal useful auditory response despite an appropriately fitted hearing-aid trial. The external and middle ears are normal. Genetic testing finds biallelic GJB2 variants, while both parents have normal hearing and no known affected relatives. Imaging and specialist assessment suggest that the auditory nerves are present. Which diagnosis best explains the hearing impairment and the apparently negative family history?|Connexin-26-related hearing loss|Recessive GJB2-related loss can occur in children of unaffected carrier parents. Connexin-26 dysfunction disrupts cochlear homeostasis; selected profound cases may benefit from implantation plus language rehabilitation.
8,9,10,51|A 56-year-old man reports gradually progressive hearing loss in the left ear for five years. He has constant left-sided high-pitched tinnitus and has noticed that he drifts to the left when walking. Otoscopy is normal. Audiometry confirms asymmetric SNHL with poor left word recognition rather than a large air-bone gap. MRI of the internal auditory canals with contrast shows the enhancing lesion pictured. Which diagnosis best accounts for the combination of asymmetric auditory and vestibular dysfunction?|Vestibular schwannoma|A vestibular nerve schwannoma can involve hearing through its internal canal/CPA location and produce imbalance. MRI identifies the lesion; the audiogram alone does not establish a tumor.|figure-schwannoma
47,48|A 78-year-old retired machinist says he can hear that people are speaking but has difficulty understanding them in restaurants. The problem has worsened slowly over a decade and affects both ears similarly. He has a history of occupational noise exposure, smoking, and cardiovascular disease. Otoscopy is normal, and audiometry shows a symmetric high-frequency sensorineural pattern. No new unilateral tinnitus or abrupt threshold change is present. Which age-associated disorder is the best overall explanation, while allowing that prior noise exposure may also contribute?|Presbycusis|Age-associated sensory and neural degeneration causes symmetric SNHL and impaired complex speech understanding. Multiple risk factors can contribute, but symmetry and gradual progression differ from sudden loss or a focal retrocochlear presentation.
50|A 43-year-old woman notices a marked reduction in hearing in the right ear on awakening. She assumes the ear is blocked and waits until the next afternoon, but the deficit persists. Otoscopy reveals no wax, fluid, or drum abnormality. Weber lateralizes left, and Rinne remains air greater than bone on the right. Urgent audiometry identifies a new loss exceeding 30 dB at three contiguous frequencies within 48 hours. Which diagnosis should guide time-sensitive otologic evaluation and discussion of corticosteroid therapy?|Sudden sensorineural hearing loss|Abrupt cochlear/neural loss with the rule-of-threes threshold pattern is SSNHL. Normal otoscopy and a positive Rinne do not rule it out. Prompt treatment assessment matters even when the patient describes fullness rather than explicitly reporting deafness.''')
block('av','Extended vestibular cases','vestDx','''85,86,88,89|A 62-year-old woman reports spinning every time she rolls toward her right side in bed or looks up to reach a high shelf. Each episode lasts less than a minute, and she is comfortable while sitting still between spells. She denies new hearing loss, aural fullness, severe headache, or limb symptoms. Right Dix-Hallpike positioning produces a brief delayed torsional-upbeating nystagmus that fades. The neurologic examination is otherwise normal. Which diagnosis best fits this triggered episodic pattern and supports a canalith repositioning maneuver?|Posterior canal BPPV|Brief positional attacks with the characteristic posterior-canal nystagmus support BPPV. Epley addresses displaced otoconia; it is more appropriate than routine chronic suppression or assuming the symptoms are Meniere attacks.|figure-dix
85,90,105,106|A 38-year-old man develops continuous severe spinning and vomiting several days after an upper respiratory illness. Symptoms persist at rest for two days and worsen with any head movement. Hearing is unchanged, and there is no fluctuating aural fullness. Specialist examination supports an acute peripheral vestibular deficit after appropriate assessment for central disease. He is given short-term nausea control, then encouraged to begin graded mobilization and vestibular exercises. Which diagnosis best matches the sustained time course and absence of new cochlear symptoms?|Vestibular neuritis|Vestibular neuritis causes a sustained acute vestibular syndrome, unlike seconds-long triggered BPPV. Preserved hearing distinguishes it from classic labyrinthitis; recovery depends partly on central compensation.
91|A 24-year-old with a severe bacterial middle-ear infection develops new intense vertigo, vomiting, and a substantial hearing decline in the same ear. The symptoms persist rather than occurring only during brief positional maneuvers. The clinician is concerned about spread of inflammation or infection to the inner ear and arranges urgent specialist management. Which diagnosis best explains combined cochlear and vestibular involvement and the need for infection-directed treatment rather than symptomatic medication alone?|Labyrinthitis|Labyrinthine involvement causes vertigo plus hearing loss. In a bacterial context, antibiotics and source management are essential; antiemetics or steroids cannot substitute for control of suppurative infection.
92,93,94,95,96,97|A 49-year-old woman has had several spontaneous vertigo attacks over six months, each lasting about one to two hours. During attacks she notices roaring left tinnitus, pressure in the left ear, and reduced hearing. Audiograms taken at different visits document fluctuating low-frequency SNHL. Between attacks she is often functional, although hearing has begun to decline. There is no consistent seconds-long trigger when rolling over in bed. Which diagnosis best unifies the episodic vestibular and fluctuating cochlear symptoms?|Meniere disease|The classic tetrad and duration favor Meniere disease. Endolymphatic hydrops is its characteristic histopathologic correlate, though the causal relationship and individual course are complex.|figure-hydrops
49,104,109|A 67-year-old received prolonged gentamicin for a serious infection. Since discharge, objects appear to bounce when he walks or turns his head. He is fairly steady while sitting, but becomes very unstable in a dark hallway or on an uneven surface. Examination demonstrates impaired compensatory eye movements with rapid head turns to either side. There is no single seconds-long positional trigger. Which disorder best explains the oscillopsia and increased dependence on vision and proprioception?|Bilateral vestibular hypofunction|Bilateral vestibulotoxic injury reduces VOR function and produces head-motion oscillopsia. Darkness and unstable surfaces remove reliable alternative inputs; rehabilitation aims to improve compensation and remaining sensory use.''')
custom('oph','Extended pharmacology cases','4,6,7,10','A 71-year-old man with open-angle glaucoma starts a new eye drop that reduces aqueous secretion without changing pupil size. Within days he develops wheezing, unusual fatigue, and a pulse of 46/min. He has a history of asthma and takes no new oral medication. The clinician explains that topical ocular drugs can still enter the systemic circulation and decides to stop the suspected agent while arranging an alternative pressure-lowering strategy. Which medication most plausibly caused this combined pulmonary and cardiac reaction?',[
'Timolol~Nonselective systemic beta blockade can provoke bronchospasm and bradycardia after ophthalmic absorption. Asthma and conduction disease are important contraindication concerns.',
'Latanoprost~This commonly causes local pigmentation/lash changes rather than this beta-blockade cluster.',
'Dorzolamide~A topical CA inhibitor can cause irritation or taste disturbance, but it does not primarily block cardiac and bronchial beta receptors.',
'Pilocarpine~A cholinergic drug can cause systemic secretory effects, but the question centers on a classic beta-blocker cardiopulmonary reaction in an asthmatic patient.',
'Netarsudil~This acts at trabecular outflow and commonly causes hyperemia, not nonselective beta blockade.'])
custom('oph','Extended pharmacology cases','6,10','A 59-year-old woman receives an oral medication to reduce aqueous production while awaiting further glaucoma treatment. Several days later she reports tingling around the mouth and in the fingers. Laboratory testing shows reduced bicarbonate and potassium, with a normal anion gap. She also has a history of calcium-containing kidney stones. The clinician suspects systemic inhibition of an enzyme involved in both ciliary secretion and renal bicarbonate handling. Which drug best explains the therapeutic and adverse effects?',[
'Acetazolamide~Systemic carbonic anhydrase inhibition reduces aqueous formation while causing bicarbonate wasting, hyperchloremic acidosis, potassium depletion, paresthesias, and stone risk.',
'Mannitol~Osmotic diuresis affects volume and osmolality but does not produce this characteristic CA-inhibitor mechanism.',
'Timolol~Beta blockade explains bradycardia/bronchospasm rather than bicarbonate wasting.',
'Tropicamide~Antimuscarinic dilation/cycloplegia does not explain the renal acid-base pattern.',
'Echothiophate~Acetylcholinesterase inhibition causes cholinergic effects rather than carbonic anhydrase-mediated bicarbonate loss.'])
custom('va','Extended physiology cases','8,9,10,11,12','A researcher records from an isolated rod while delivering a brief flash. In a control cell, the flash lowers cGMP, reduces inward cation current, makes the membrane potential more negative, and decreases glutamate release. In a mutant cell, the pigment still absorbs light normally, but activated transducin cannot stimulate its downstream effector. The mutant therefore fails to lower cGMP appropriately. Which normal enzymatic event is directly disrupted in this experiment?',[
'Phosphodiesterase-mediated cGMP hydrolysis~Transducin normally activates PDE6, which lowers cGMP and closes cyclic-nucleotide-gated channels. Normal pigment absorption does not rescue a block at this downstream step.',
'Initial 11-cis-retinal photoisomerization~The question states that pigment absorption/activation remains intact.',
'Direct M3-mediated ciliary contraction~That is an ocular drug mechanism, not rod phototransduction.',
'Renal bicarbonate secretion~This is unrelated to the isolated rod signaling defect.',
'Spiral ganglion action-potential generation~That belongs to auditory rather than retinal transduction.'])
custom('va','Extended physiology cases','24,25,32,33,34,35','An investigator applies a controlled shear displacement to a cochlear hair bundle toward its tallest stereocilia. The apical surface is bathed in normal potassium-rich endolymph, while the basal membrane remains in its usual environment. The investigator records a graded depolarization followed by increased synaptic transmitter release and greater firing of the connected auditory afferent. Which explanation correctly links the initial mechanical event to the electrical and synaptic changes?',[
'Tip-link tension opens apical channels, potassium enters, and depolarization opens basal calcium channels~The unusual endolymphatic potassium/electrical environment drives inward transduction current. Calcium then triggers glutamate release to spiral ganglion afferents.',
'Potassium exits apically and directly activates glutamate receptors inside the hair cell~The excitatory apical transduction current is inward, and glutamate acts downstream at the afferent synapse.',
'Light activates rhodopsin, lowering cGMP and depolarizing the cell~This is not the cochlear mechanical pathway; light also hyperpolarizes ordinary photoreceptors.',
'A large action potential in the hair cell directly travels into the cortex~Hair cells use graded receptor potentials; the connected neurons carry spikes.',
'The external canal produces neurotransmitter that diffuses through the stapes~The local sensory synapse is in the cochlea, not the external canal.'])
custom('va','Extended localization cases','39,40,41,42,43,44,45','A patient develops difficulty identifying where sounds originate after a focal unilateral lesion in a higher auditory pathway. Pure-tone testing still demonstrates useful hearing from both ears. The neurologist contrasts this with a lesion of the cochlear nerve, which can markedly reduce hearing from its own ear. The difference is explained by how auditory information is distributed after reaching the brainstem. Which principle best accounts for the patient’s preserved bilateral sound detection?',[
'Substantial bilateral representation develops above the initial ipsilateral cochlear input~Information from each ear reaches both higher auditory systems. Unilateral higher lesions often impair localization or discrimination more than basic monaural detection.',
'Each cochlear nerve already carries equal input from both ears~Peripheral cochlear nerves initially carry input from their own cochlea.',
'The auditory cortex receives only ipsilateral input~Higher auditory processing is bilaterally supplied, often with contralateral predominance.',
'The ossicles independently generate conscious sound recognition~They transfer mechanical energy rather than interpret sound.',
'A unilateral higher lesion must produce complete contralateral ear deafness~Bilateral representation makes that an unusual isolated pattern.'])

if __name__=='__main__':
 (R/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf8')
 print(len(questions),'questions')

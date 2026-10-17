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
  rng=random.Random(81000+len(questions));wrong=[(a,w) for a,w in pools[pname].items() if a not in excluded];rng.shuffle(wrong)
  opts=[dict(text=answer,why=why,correct=True)]+[dict(text=a,why=w,correct=False) for a,w in wrong[:4]]
  assert len(opts)==5
  rng.shuffle(opts);ans=next(i for i,o in enumerate(opts) if o.pop('correct'))
  for o in opts:o.pop('correct',None)
  questions.append(dict(id=f'Q{len(questions)+1:03}',deck=deck,topic=topic,pages=pages,page=pages[0],ref=f'slide-{deck}-{pages[0]}',stem=stem,options=opts,answer=ans,image=fig[0]+'.jpg' if fig else None))
def custom(deck,topic,refs,stem,options,fig=None):
 entries=[s.split('~',1) for s in options];pn='custom'+str(len(questions));pools[pn]=dict(entries[1:]);block(deck,topic,pn,refs+'|'+stem+'|'+entries[0][0]+'|'+entries[0][1]+('|' + fig if fig else ''))

pool('eyeDx','''Infectious keratitis~Corneal infection causes pain, photophobia, decreased acuity, and an infiltrate; it is more concerning for vision than routine superficial conjunctivitis.
Corneal ulcer~A corneal epithelial defect with underlying stromal infiltration/tissue loss is an ulcer; severe cases can scar, perforate, and threaten vision.
Conjunctivitis~Conjunctival inflammation commonly causes redness, irritation, tearing, and discharge with relatively preserved vision; severe pain or photophobia suggests deeper disease.
Anterior uveitis~Iris/ciliary inflammation causes ciliary redness, photophobia, and anterior chamber cells/flare rather than only superficial discharge.
Retinitis~Retinal inflammation causes floaters, scotomas, or vision loss with posterior retinal lesions; it is not diagnosed solely from a red ocular surface.
Allergic conjunctivitis~Itching, watery discharge, and an allergic context favor noninfectious conjunctival inflammation, although symptoms overlap with infection.''')
block('inf','Eye infection localization','eyeDx','''4|A painful eye has an epithelial defect overlying a white-gray stromal infiltrate with tissue loss. Which lesion is present?|Corneal ulcer|An ulcer combines epithelial breakdown with stromal involvement. Infection and inflammation can destroy corneal tissue and produce scarring or perforation.|figure-04
5|A contact lens wearer develops pain, photophobia, reduced visual acuity, and a corneal infiltrate. Which anatomic diagnosis best fits?|Infectious keratitis|The cornea is involved. Epithelial injury permits microbial invasion and an inflammatory response that can progress to ulceration and vision loss.
6|A child has red conjunctivae, mild irritation, tearing, and discharge but no major photophobia or reduction in acuity. Which diagnosis best fits?|Conjunctivitis|The symptoms localize to the conjunctival surface. Deeper pain, severe light sensitivity, or visual loss should trigger evaluation for corneal or intraocular disease.
8|An adult has a painful photophobic red eye with redness concentrated around the limbus. Slit-lamp examination shows inflammatory cells in the anterior chamber. Which diagnosis fits?|Anterior uveitis|Anterior uveal inflammation affects the iris/ciliary body and produces ciliary injection and cells/flare. Infectious, autoimmune, and idiopathic causes are possible.
9|A severely immunocompromised patient develops floaters, a field scotoma, and retinal hemorrhagic necrosis. Which anatomic syndrome is present?|Retinitis|Retinal damage explains posterior visual symptoms and funduscopic necrosis. Cytopathic viral injury can progress rapidly and threaten sight.
6,7|An atopic patient has bilateral itching, watery discharge, and seasonal recurrence without reduced acuity. Which diagnosis is most likely?|Allergic conjunctivitis|Prominent itching and seasonal recurrence favor allergy. Watery discharge alone is insufficient to distinguish allergic from viral conjunctivitis.
4,5,6|A patient initially calls a red eye pink eye, but examination reveals marked photophobia and a corneal opacity. Which diagnosis warrants priority over uncomplicated conjunctivitis?|Infectious keratitis|Corneal involvement, pain, and reduced visual function suggest sight-threatening keratitis rather than a routine superficial process. Urgent eye assessment is appropriate.''')
pool('eyeBug','''Pseudomonas aeruginosa~This water-associated gram-negative bacterium is important in contact lens-associated bacterial keratitis and otitis externa; it can cause rapid corneal destruction.
Staphylococcus aureus~This skin-associated gram-positive organism can cause bacterial conjunctivitis, keratitis, and otitis externa; culture/context distinguish it from other bacteria.
Streptococcus pneumoniae~An encapsulated gram-positive diplococcus can cause conjunctivitis, keratitis, otitis media, and meningitis rather than being restricted to one site.
Adenovirus~This common cause of contagious watery conjunctivitis can accompany pharyngitis and preauricular nodes; it is not a bacterium producing a Gram stain isolate.
Herpes simplex virus~HSV can cause recurrent dendritic epithelial keratitis or anterior uveitis. HSV-1 also causes temporal lobe encephalitis, while HSV-2 is associated with aseptic meningitis.
Acanthamoeba species~Water exposure with contact lenses, severe pain out of proportion, and a ring infiltrate suggest amebic keratitis, including in otherwise healthy people.
Fusarium species~Filamentous fungi can cause keratitis after vegetative trauma, often with feathery infiltrates; Fusarium is not a herpesvirus or bacterium.
Aspergillus species~This mold can cause fungal keratitis, otomycosis, or angioinvasive CNS disease in susceptible hosts.
Candida species~Yeasts can cause ocular infection, especially with a compromised cornea or systemic candidemia, and can also produce otomycosis or CNS invasion.
Chlamydia trachomatis~Chlamydia can cause chronic follicular conjunctivitis and trachoma, with repeated inflammation leading to scarring; serovar and exposure context matter.
Haemophilus influenzae~This bacterium is relevant to conjunctivitis and otitis media; nontypeable strains differ from encapsulated type b invasive disease.
Corynebacterium diphtheriae~This organism is a less common cause of membranous conjunctivitis in the appropriate clinical context, not the usual viral pink-eye agent.
Cytomegalovirus~CMV causes necrotizing retinitis particularly with profound cellular immunosuppression; it is a herpesvirus, not a protozoan.
Toxoplasma gondii~This protozoan is a major infectious cause of posterior retinochoroiditis and can reactivate as focal encephalitis in advanced HIV; it is not a fungus.''')
block('inf','Eye pathogens','eyeBug','''4,5|A contact lens wearer develops a rapidly progressive bacterial corneal ulcer. Culture grows an oxidase-positive gram-negative rod. Which organism is most likely?|Pseudomonas aeruginosa|Contact lenses and water exposure increase concern for Pseudomonas bacterial keratitis. Its tissue-destructive infection can progress quickly.
4,5|A lens wearer rinses lenses in tap water and develops extreme corneal pain with a ring infiltrate. Which pathogen is particularly concerning?|Acanthamoeba species|Acanthamoeba keratitis is strongly associated with water-contaminated lens practices. Severe pain and a ring infiltrate are clues, but not independently diagnostic.
4,5|A recurrent unilateral corneal epithelial lesion branches in a dendritic pattern with terminal bulbs. Which agent is favored?|Herpes simplex virus|Dendritic epithelial keratitis is characteristic of HSV. Recurrent corneal infection differs from adenoviral conjunctival inflammation.
4|After plant-related eye trauma, a patient develops a feathery corneal ulcer; culture identifies Fusarium. What is the causative organism?|Fusarium species|Vegetative trauma can introduce filamentous fungi. Fusarium and Aspergillus are important fungal ulcer pathogens.
4,5|A corneal culture shows a mold with septate acute-angle branching hyphae in a patient with fungal keratitis. Which organism fits?|Aspergillus species|Aspergillus is a filamentous mold capable of corneal infection. Its invasive systemic manifestations differ from isolated ocular infection.
5|A patient with a chronically compromised ocular surface develops keratitis with budding yeast and pseudohyphae on microscopy. Which genus is likely?|Candida species|Candida can infect a damaged cornea and is distinguished from filamentous molds by yeast/pseudohyphal morphology.
6|Several students develop watery pink eyes during a respiratory outbreak, with preauricular nodes and mild pharyngitis. Which agent is most likely?|Adenovirus|Adenovirus is a common viral conjunctivitis cause and can produce pharyngoconjunctival illness. Discharge character supports but does not prove etiology.
6|A patient has chronic follicular conjunctivitis, and testing identifies an obligate intracellular bacterium associated with trachoma. Which organism is responsible?|Chlamydia trachomatis|Repeated trachoma infection can scar conjunctiva and turn eyelashes inward, injuring the cornea. Trachoma serovars differ from typical genital inclusion-conjunctivitis serovars.
6|A conjunctivitis isolate is catalase-positive and coagulase-positive gram-positive cocci in clusters. Which listed organism fits?|Staphylococcus aureus|S. aureus is a bacterial cause of conjunctivitis and can also invade cornea. Morphology and coagulase positivity distinguish it from pneumococci.
4,6|A corneal or conjunctival bacterial isolate consists of encapsulated gram-positive diplococci. Which listed pathogen fits?|Streptococcus pneumoniae|Pneumococcus can cause infection at ocular, middle-ear, and meningeal sites. Its morphology differs from staphylococcal clusters.
6,14|A child has purulent conjunctivitis together with acute otitis media. Culture identifies a small gram-negative coccobacillus, often nontypeable. Which organism is associated?|Haemophilus influenzae|Nontypeable H. influenzae is important in conjunctivitis-otitis syndrome. This is distinct from the Hib capsule targeted by the type b vaccine.
6|A patient from an undervaccinated community has conjunctivitis with an adherent membrane and a toxigenic coryneform isolate. Which organism is a listed cause?|Corynebacterium diphtheriae|Diphtheria can involve conjunctiva with membranous inflammation. It is not a usual cause of ordinary viral watery conjunctivitis.
8|A patient has recurrent unilateral anterior uveitis and evidence of herpetic ocular infection. Which virus listed in the deck is most associated?|Herpes simplex virus|HSV can cause anterior uveal inflammation, often alongside corneal findings. Not all uveitis is infectious, so systemic/immune alternatives remain important.
8,9|An adult with advanced HIV and CD4 count of 24/µL develops floaters and hemorrhagic necrotizing retinal lesions. Which pathogen is most likely?|Cytomegalovirus|Profound cellular immunodeficiency predisposes to CMV retinitis. Ocular examination is central; a blood viral load alone does not establish the retinal diagnosis.
8,9|A focal white retinal inflammatory lesion adjacent to an old pigmented scar is associated with posterior uveitis. Which pathogen is favored?|Toxoplasma gondii|Ocular toxoplasmosis commonly produces retinochoroiditis. The slide's suggestion that Toxoplasma is a rare fungal cause is incorrect: it is a protozoan and an important ocular pathogen.''')
custom('inf','Conjunctivitis interpretation','6,7','Which conclusion is justified by mucopurulent discharge and eyelid matting?',[
'They increase the likelihood of bacterial conjunctivitis without proving it~Symptoms overlap across causes; no single discharge finding reliably distinguishes bacterial from viral disease.',
'They definitively exclude all viral disease~Viral and bacterial findings can overlap, so this is too absolute.',
'They prove that the retina is necrotic~Surface discharge does not establish retinitis.',
'They prove that the uvea is infected~Uveitis requires intraocular evidence, not discharge alone.',
'They make pain and visual acuity irrelevant~Pain, photophobia, and reduced vision remain important red flags.'])
custom('inf','Corneal tissue injury','4,5','Why can untreated infectious keratitis leave permanent visual impairment?',[
'Microbial injury and host inflammation can ulcerate and scar the cornea~Loss of transparent stromal architecture impairs optics; severe tissue loss can progress to perforation.',
'Corneal inflammation is always confined to harmless tear-film changes~Infection can invade epithelium/stroma and threaten structure.',
'The cornea normally regenerates every damaged layer without scarring~Significant stromal injury may heal with persistent opacity.',
'Only the lens determines visual clarity~The cornea is a major transparent refracting structure.',
'Keratitis affects only the external eyelid skin~The affected tissue is the cornea itself.'])
custom('inf','Uveal anatomy and causes','8','Which structures make up the uveal tract?',[
'Iris, ciliary body, and choroid~Uveitis can affect anterior, intermediate, posterior, or all uveal compartments depending on its pattern.',
'Cornea, conjunctiva, and sclera~These are surface/outer-coat structures rather than the uveal triad.',
'Lens, optic nerve, and eyelid~These do not define the vascular uveal layer.',
'Retina, lacrimal gland, and pupil opening~These are not the three uveal structures.',
'Trabecular meshwork, Schlemm canal, and vitreous~These do not constitute the uveal tract.'])
custom('inf','Uveitis differential','8','A patient has uveitis but no pathogen has been demonstrated. Which statement is most accurate?',[
'Immune-mediated and idiopathic disease are major alternative categories~Uveitis is an inflammatory syndrome, not proof of infection. Granulomatous versus nongranulomatous morphology and systemic context help narrow causes.',
'Every uveitis case is bacterial~The deck specifically includes noninfectious and viral/protozoal categories.',
'Autoimmune disease cannot affect intraocular tissues~Systemic immune disorders can cause uveitis.',
'Floaters always prove CMV~Floaters are nonspecific and can arise from multiple posterior disorders.',
'Bilateral involvement excludes infection~Infectious uveitis may be unilateral or bilateral depending on cause and host.'])
custom('inf','Retinal tissue injury','9','Which mechanism contributes to rapidly progressive viral retinitis?',[
'Direct viral cytopathic injury with retinal inflammation and necrosis~Damage to neural retina can produce scotomas and irreversible vision loss. Ocular localization and organism testing guide care.',
'Only a mechanical obstruction in the tear duct~That does not explain retinal necrosis.',
'Only lens protein aggregation~That causes cataract rather than retinitis.',
'Only conjunctival hyperemia without tissue injury~Retinitis involves posterior retinal tissue.',
'Purely external canal blockage~This is an auditory conductive mechanism.'])

pool('earDx','''Acute otitis externa~Inflamed edematous external canal with pain on tragal pressure or auricle movement suggests AOE; canal obstruction can cause conductive loss.
Acute otitis media~A bulging poorly mobile tympanic membrane with acute symptoms and middle-ear fluid supports AOM, not simply canal skin inflammation.
Otomycosis~Fungal external canal disease often causes itching, debris, and discharge; Aspergillus and Candida are important organisms.
Otitis media with effusion~Middle-ear fluid without acute infectious symptoms is OME; fluid alone does not establish acute otitis media.
Necrotizing otitis externa~Severe persistent otalgia with granulation tissue, especially in a diabetic/immunocompromised host, raises concern for invasive canal/skull-base infection.''')
block('inf','Ear infection localization','earDx','''11,12|A swimmer has severe ear pain that increases when the tragus is pressed. The canal is swollen and erythematous, without a bulging drum. Which diagnosis fits?|Acute otitis externa|Water exposure and canal barrier disruption favor AOE. Tragal/auricular tenderness localizes the process to the external canal rather than the middle ear.
13,14|A febrile toddler has deep otalgia and a bulging opaque poorly mobile tympanic membrane. Pulling the auricle does not markedly worsen pain. Which diagnosis fits?|Acute otitis media|Middle-ear fluid and pressure produce bulging and reduced mobility. Acute symptoms distinguish AOM from uncomplicated residual effusion.
11,12|An immunocompromised patient has prominent canal itching and cottony fungal debris. Which diagnosis is most likely?|Otomycosis|Fungi can cause external canal infection, particularly in chronic or predisposed settings. Aspergillus and Candida are listed organisms.
13,14|A child has fluid behind the drum after a respiratory illness but no acute pain, fever, or drum bulging. Which diagnosis is more precise than AOM?|Otitis media with effusion|Effusion can persist without acute infection. A red drum or fluid alone does not establish acute bacterial otitis media.
11,12|An older diabetic patient has severe persistent nocturnal ear pain, granulation in the canal, and a new facial palsy. Which invasive extension must be considered?|Necrotizing otitis externa|This supplemental application distinguishes a dangerous invasive infection from routine AOE. Pseudomonas is a characteristic cause in the appropriate host.''')
pool('earBug','''Pseudomonas aeruginosa~A water-associated gram-negative rod is a major cause of bacterial otitis externa and severe invasive external-ear infection.
Staphylococcus aureus~Skin barrier disruption can permit staphylococcal external canal infection; it is also relevant to ocular and abscess disease.
Aspergillus species~Filamentous molds are common otomycosis agents, with itching and fungal debris rather than the usual bulging AOM drum.
Candida species~Yeast can cause fungal otitis externa, especially with altered canal conditions or host defenses.
Nontypeable Haemophilus influenzae~This is a common modern bacterial AOM pathogen and can accompany purulent conjunctivitis; prevalence varies by population.
Moraxella catarrhalis~This gram-negative diplococcus is an important pediatric AOM pathogen, distinct from the usual Pseudomonas swimmer's-ear pattern.
Streptococcus pneumoniae~Pneumococcus remains an important AOM organism despite changes after vaccination; it also causes invasive meningitis.
Respiratory syncytial virus~Viral respiratory infection can impair Eustachian tube function and predispose to AOM; it is not a bacterial culture isolate.
Rhinovirus~Upper respiratory infection can promote Eustachian dysfunction and middle-ear disease without being one of the bacterial AOM pathogens.
Adenovirus~This respiratory/conjunctival virus can contribute to upper-airway inflammation and predispose to middle-ear disease.''')
block('inf','Ear pathogens','earBug','''12|A swimmer with otitis externa has an oxidase-positive gram-negative rod isolated from canal drainage. Which organism is most likely?|Pseudomonas aeruginosa|Moisture-rich canal conditions favor Pseudomonas. This is a classic external-ear pathogen rather than one of the usual encapsulated respiratory AOM bacteria.
12|After repeated cotton-swab trauma, a patient develops AOE with coagulase-positive gram-positive cocci in clusters. Which organism fits?|Staphylococcus aureus|Disruption of canal skin permits S. aureus infection. Mechanical trauma, hearing aids, and eczema are additional barrier-related risk factors.
11,12|An itchy ear contains filamentous fungal debris, and microscopy/culture shows Aspergillus. Which pathogen is responsible?|Aspergillus species|Aspergillus is a major mold cause of otomycosis. Candida is an alternative yeast cause but does not match the identified mold.
11,12|An ear-canal fungal isolate shows budding yeast and pseudohyphae. Which organism best fits?|Candida species|Candida can produce otomycosis, especially with chronic local disruption or host predisposition.
14|A child with AOM and conjunctivitis has a nontypeable small gram-negative coccobacillus. Which organism is most likely?|Nontypeable Haemophilus influenzae|Nontypeable H. influenzae is common in AOM and conjunctivitis-otitis syndrome. Ranking it as universally the leading cause would overstate cohort-dependent epidemiology.
14|A child with AOM has an oxidase-positive gram-negative diplococcus identified as Moraxella. Which agent fits?|Moraxella catarrhalis|M. catarrhalis is a common respiratory-colonizing pediatric AOM organism. It should not be confused with meningococcal invasive disease solely because both are gram-negative diplococci.
14|An AOM isolate consists of optochin-sensitive encapsulated gram-positive diplococci. Which agent fits?|Streptococcus pneumoniae|Pneumococcus remains an important bacterial middle-ear pathogen and can spread or cause invasive disease in susceptible settings.
14|During bronchiolitis caused by RSV, a toddler develops Eustachian dysfunction and secondary AOM. Which viral contributor is present?|Respiratory syncytial virus|RSV is one of the respiratory viruses listed as predisposing contributors. The viral trigger and any subsequent bacterial isolate are different components of the process.''')
custom('inf','External ear pathogenesis','12','Which combination predisposes to acute otitis externa?',[
'Retained moisture plus disrupted canal epithelium~Swimming, excessive cleaning, hearing aids, and eczema can compromise the protective canal environment and permit microbial growth.',
'Only obstruction of the Eustachian tube with an intact canal~That is a middle-ear mechanism rather than the characteristic canal pathway.',
'Only hematogenous seeding of the meninges~That is a CNS infectious route.',
'Only pressure in the subarachnoid space~That does not explain canal skin inflammation.',
'Only HSV latency in the temporal lobe~That does not define routine swimmer’s ear.'])
custom('inf','Middle-ear pathogenesis','13,14','Which sequence best explains AOM after an upper respiratory infection?',[
'Eustachian dysfunction, middle-ear fluid stasis, microbial growth, increased pressure~Fluid and pressure behind the drum cause pain, bulging, and impaired vibration. Young Eustachian tube anatomy and airway inflammation increase susceptibility.',
'Corneal epithelial breakdown, stromal infection, scarring~That is an ocular keratitis pathway.',
'External canal abrasion, tragal tenderness, normal middle-ear pressure~That better describes AOE.',
'Retrograde axonal transport from a bite~That is a rabies route.',
'A retinal scar followed by toxoplasma reactivation~That is an ocular posterior-infection pattern.'])
custom('inf','Ear examination','13','What does reduced tympanic membrane mobility on pneumatic otoscopy suggest in a child with a bulging drum?',[
'Middle-ear effusion limiting membrane movement~Fluid and pressure reduce drum mobility. Together with acute bulging and symptoms, this supports AOM.',
'Definite cochlear hair-cell destruction~Mobility is a mechanical middle-ear finding, not a direct cochlear test.',
'A normal fluid-free middle ear in every case~Effusion is a central explanation for the reduced movement.',
'Only retinal inflammation~This is an otoscopic finding.',
'Only a viral meningeal syndrome~Meningitis is not established by drum mobility.'])
custom('inf','Ear hearing loss','11,13','Why can both severe AOE and AOM reduce hearing?',[
'Both can impair mechanical sound transmission, at different sites~Canal edema/debris obstructs AOE transmission, while middle-ear fluid impairs drum/ossicular motion in AOM, producing conductive loss.',
'Both necessarily destroy the cochlear nerve~Conductive mechanisms do not require neural destruction.',
'Both always cause bilateral cortical deafness~The typical local processes do not imply bilateral cortex injury.',
'Both eliminate all bone conduction immediately~Bone conduction can remain relatively preserved in isolated conductive disease.',
'Hearing changes prove that the drum cannot be involved~Middle-ear fluid and drum mechanics directly affect hearing.'])

pool('cnsSyndrome','''Meningitis~Meningeal inflammation commonly produces fever, headache, photophobia, and neck stiffness; predominant prolonged behavioral change or seizures suggests parenchymal involvement too.
Encephalitis~Brain parenchymal inflammation causes altered mental status, seizures, focal findings, and supportive CSF/MRI/EEG evidence rather than only meningeal irritation.
Meningoencephalitis~Combined meningeal and parenchymal involvement can produce both neck stiffness/headache and sustained altered behavior, seizures, or focal deficits.
Acute disseminated encephalomyelitis~ADEM is an immune-mediated multifocal demyelinating syndrome often after infection, with encephalopathy and predominantly white-matter lesions; it is not direct microbial invasion in every case.
Acute flaccid myelitis~Acute anterior horn/spinal gray-matter injury can produce flaccid weakness and reduced reflexes, often with relatively spared sensation; not all cases are poliovirus.
Acute transverse myelitis~Cord inflammation produces bilateral motor and sensory deficits with a sensory level and autonomic dysfunction; symmetry can vary and early spinal shock can be flaccid.
Brain abscess~Focal parenchymal infection can form a pus-containing lesion with edema and mass effect, often causing headache, seizures, or focal deficits.
Subdural empyema~Pus between dura and arachnoid can spread rapidly and cause fever, seizures, and focal deficits; contiguous sinus/ear disease is a possible source.
Epidural abscess~An intracranial epidural collection lies between skull and dura; this is anatomically distinct from subdural pus or an intraparenchymal abscess.''')
block('inf','CNS syndrome localization','cnsSyndrome','''16,19|An adult develops acute fever, headache, photophobia, and neck stiffness with relatively preserved cognition. Which syndrome is most directly suggested?|Meningitis|The dominant features reflect meningeal irritation. Altered consciousness can also occur in severe meningitis, so syndromes overlap rather than remaining absolutely separate.
16,19|A febrile patient has persistent personality change, new seizures, and a focal neurologic deficit. MRI shows inflamed brain parenchyma. Which syndrome is present?|Encephalitis|Parenchymal dysfunction is central to encephalitis. Sustained altered mental status plus supportive findings distinguishes it from headache/neck stiffness alone.
16,19|Fever and nuchal rigidity occur together with prolonged confusion, seizures, and parenchymal MRI abnormalities. Which term best captures both sites?|Meningoencephalitis|Meningeal and brain involvement produce overlapping symptoms. The term does not specify a single organism or exclude noninfectious inflammation.
16,17,19|Two weeks after a viral illness, a child develops encephalopathy and multifocal deficits with large white-matter lesions. Current fever is mild and infectious testing is unrevealing. Which syndrome fits?|Acute disseminated encephalomyelitis|Postinfectious immune-mediated demyelination supports ADEM. It is an important example of postinfectious disease, but not a synonym for every postinfectious encephalopathy.
16,17,26|After a respiratory illness, a child develops acute asymmetric flaccid limb weakness and reduced reflexes. MRI predominantly affects spinal anterior horn gray matter. Poliovirus testing is negative. Which syndrome fits?|Acute flaccid myelitis|AFM is a clinical/radiologic syndrome with motor gray-matter injury and nonpolio causes, including some enteroviruses. Sensory findings are often less prominent than weakness.
16,26|A patient develops bilateral leg weakness, a truncal sensory level, and urinary retention. Cord inflammation spans the affected level. Which syndrome fits?|Acute transverse myelitis|Motor, sensory, and autonomic involvement supports transverse myelitis. Symmetry is common but not absolute, and early reflexes may be reduced during spinal shock.
18,35|A patient with chronic sinus infection develops headache, a seizure, and focal weakness. MRI shows a parenchymal ring-enhancing collection with restricted diffusion. Which diagnosis fits?|Brain abscess|Contiguous spread can produce a focal pyogenic collection with surrounding edema. Ring enhancement has a broad differential and must be interpreted with clinical and imaging details.
18,36|After bacterial sinusitis, a patient has fever, seizures, and a crescentic purulent collection between dura and arachnoid. Which diagnosis fits?|Subdural empyema|The collection is subdural, not within brain tissue or outside dura. This is a neurosurgical/infectious emergency because rapid spread and mass effect can occur.
36|A focal infected collection lies between the inner skull surface and dura after skull osteomyelitis. Which term is anatomically correct?|Epidural abscess|Intracranial epidural infection occupies the extradural space. It is distinct from a spinal epidural abscess, although both are outside dura.
16,19|Which syndrome most specifically reflects immune attack on CNS myelin days to weeks after an infection rather than ongoing pathogen replication?|Acute disseminated encephalomyelitis|ADEM involves autoimmune inflammatory demyelination and often encephalopathy. Direct infection and autoimmune mechanisms require different diagnostic considerations.''')

pool('csfPattern','''Acute pyogenic bacterial pattern~Neutrophilic pleocytosis, markedly increased protein, and low CSF:serum glucose ratio favor bacterial meningitis, but exceptions and pretreatment effects occur.
Typical viral pattern~Lymphocytic pleocytosis, modest protein elevation, and usually preserved glucose favor viral infection; early neutrophils and pathogen-specific exceptions are possible.
Tuberculous meningitis pattern~A subacute/chronic illness with lymphocytes, high protein, and low glucose suggests TB; smear is insensitive and culture/NAAT improve detection.
Neurosyphilitic pattern~CSF often has mild lymphocytic pleocytosis, modest protein elevation, and relatively preserved glucose; clinical context and syphilis-specific testing are essential.
Cryptococcal or other fungal meningitis pattern~Chronic lymphocytic inflammation, high protein, and often low glucose can occur; advanced immunosuppression may produce surprisingly few cells.
Helminth-associated eosinophilic pattern~CSF eosinophilia suggests certain parasitic infections, especially helminths, but is not universal for protozoal or all parasitic CNS disease.''')
block('inf','CSF pattern recognition','csfPattern','''21,30,34|CSF has 3,200 WBC/µL with 90% neutrophils, protein 240 mg/dL, and glucose 25 mg/dL while serum glucose is 100 mg/dL. Which pattern is most likely?|Acute pyogenic bacterial pattern|The marked neutrophilia, high protein, and ratio 0.25 support bacterial meningitis. Culture, Gram stain, and appropriate molecular testing are needed, and treatment should be prompt.
20,21,30,34|CSF has 140 WBC/µL, predominantly lymphocytes, protein 70 mg/dL, and preserved CSF:serum glucose ratio. Which common pattern fits an acute self-limited aseptic syndrome?|Typical viral pattern|Typical viral CSF shows lymphocytic pleocytosis and normal glucose with modest protein elevation. This is a pattern, not definitive organism identification.
18,32,34|A subacute headache illness has CSF with 220 lymphocyte-predominant WBC/µL, protein 280 mg/dL, and low glucose. TB exposure and basal meningeal abnormalities are present. Which pattern fits?|Tuberculous meningitis pattern|Chronicity, lymphocytes, high protein, and low glucose with a compatible exposure favor TB. Fungal disease can resemble this, so specific tests are required.
18,32,34|A patient with syphilis has neurologic symptoms, 45 lymphocytes/µL, modest protein elevation, and normal glucose. Which pattern is compatible?|Neurosyphilitic pattern|Neurosyphilis can cause a milder lymphocytic CSF profile. CSF VDRL and sensitive treponemal tests have different diagnostic roles.
18,32,33,34|Advanced HIV is associated with subacute headache, high opening pressure, and positive CSF cryptococcal antigen despite only 12 WBC/µL. Which pattern fits?|Cryptococcal or other fungal meningitis pattern|Profound immune suppression can blunt CSF inflammation in cryptococcosis. A low cell count does not exclude serious fungal CNS infection.
34|After a relevant travel/food exposure, a patient has meningitis with a substantial CSF eosinophil fraction. Which broad pattern deserves consideration?|Helminth-associated eosinophilic pattern|Eosinophilia suggests selected helminthic causes, not every parasite. Naegleria may cause a neutrophilic pattern and toxoplasmosis is often primarily parenchymal.
21,30|Which broad pattern usually has a CSF:serum glucose ratio below 0.4 in the deck's acute bacterial-versus-viral comparison?|Acute pyogenic bacterial pattern|Low CSF glucose relative to serum supports bacterial infection in this comparison. TB and fungal disease can also lower glucose, and a normal value does not exclude early bacterial disease.
21,30|Which pattern most often preserves glucose despite an elevated lymphocyte count in an acute uncomplicated aseptic illness?|Typical viral pattern|Preserved glucose is characteristic of many viral cases. CMV, mumps, and other exceptions mean glucose cannot classify all cases with certainty.''')
pool('diagnosticTest','''CSF Gram stain and bacterial culture~These can identify pyogenic organisms and permit susceptibility assessment, but pretreatment or low organism burden reduces sensitivity.
CSF pathogen-specific PCR or validated multiplex PCR~Molecular testing detects pathogen nucleic acid and is useful for enteroviruses, HSV, and selected bacteria; panel coverage and timing limit interpretation.
CSF cryptococcal antigen~CrAg is a sensitive organism-directed test for cryptococcal CNS disease and is preferred to relying solely on India ink.
CSF mycobacterial NAAT and culture~TB-specific testing improves diagnosis compared with a single insensitive AFB smear, but negative results do not always exclude TB meningitis.
CSF VDRL~A positive result in an appropriate non-bloody specimen is highly specific for neurosyphilis, but low sensitivity means a negative result does not exclude it.
CSF treponemal testing such as FTA-ABS or TPPA~These tests are more sensitive but less specific in this setting; a positive result must be interpreted with serum tests, symptoms, and other CSF evidence.
CSF wet mount with ameba-directed testing~Fresh-sample microscopy can reveal motile amebas in PAM, with specific PCR/reference testing used for confirmation.
Contrast-enhanced brain MRI~Imaging localizes parenchymal inflammation, abscesses, mass effect, and extra-axial collections rather than directly replacing microbiologic testing.
EEG~EEG can support encephalitis or detect seizures/nonconvulsive status; it does not by itself identify the infectious agent.
CSF differential with exposure-directed serology/PCR~Counting eosinophils and choosing parasite-specific testing can evaluate suspected eosinophilic meningitis; no single broad test covers all parasites.''')
block('inf','Diagnostic test selection','diagnosticTest','''21,30|Which initial CSF studies can visualize common bacterial organisms and grow an isolate for susceptibility testing?|CSF Gram stain and bacterial culture|Gram stain can be rapid and culture supports organism identification and susceptibility. Negative results, especially after antibiotics, do not rule out bacterial infection.
20,21,25,30|Which test is particularly useful for identifying HSV or enterovirus nucleic acid in CSF?|CSF pathogen-specific PCR or validated multiplex PCR|CSF PCR can establish a viral diagnosis in the right syndrome. A negative early HSV result may require repeat testing if suspicion remains high.
32,34|Which CSF assay is preferred when cryptococcal meningitis is suspected?|CSF cryptococcal antigen|CrAg detects cryptococcal capsular antigen and is more sensitive than relying only on India ink. It is not a universal test for every fungus.
32,34|A single AFB smear is negative in suspected TB meningitis. Which tests should still be pursued?|CSF mycobacterial NAAT and culture|A smear has limited sensitivity. TB-specific molecular tests and culture are important, but clinical suspicion still matters after negative results.
32,34|Which CSF syphilis test is relatively specific but insufficiently sensitive to exclude disease when negative?|CSF VDRL|A positive CSF VDRL supports neurosyphilis in context, but a negative result cannot independently exclude it.
32,34|Which CSF tests are more sensitive than VDRL for neurosyphilis but require caution about specificity?|CSF treponemal testing such as FTA-ABS or TPPA|Treponemal tests can support evaluation, especially after a negative VDRL, but serum antibody diffusion and clinical context affect interpretation.
18,34|A rapidly progressive meningitis after warm freshwater nasal exposure has motile organisms in fresh CSF. Which diagnostic approach is relevant?|CSF wet mount with ameba-directed testing|Naegleria trophozoites may be visible in a fresh wet mount. Specific reference PCR/microscopy confirms identity rather than treating the organisms as leukocytes.
34|Meningitis with CSF eosinophilia follows a compatible parasitic exposure. Which diagnostic approach is appropriate?|CSF differential with exposure-directed serology/PCR|The differential highlights eosinophils; serologic or molecular testing is selected for the suspected parasite and local availability.
19,25|A confused patient has episodes of unresponsiveness and suspected nonconvulsive seizures during encephalitis. Which test directly evaluates electrical seizure activity?|EEG|EEG can identify seizure activity and support parenchymal dysfunction. It complements MRI and CSF rather than identifying a virus by itself.
25,35,36|A focal neurologic deficit raises concern for abscess, empyema, or encephalitic injury. Which study best localizes the structural lesion?|Contrast-enhanced brain MRI|MRI helps define parenchymal versus extra-axial disease, edema, and mass effect. Imaging may need to precede LP when a mass lesion or other contraindication is suspected.''')
custom('inf','CSF calculation','21,30','CSF glucose is 36 mg/dL and serum glucose is 120 mg/dL. What is the CSF:serum ratio?',[
'0.30~Divide 36 by 120. This low ratio supports a bacterial, TB, fungal, or other hypoglycorrhachic process in context rather than a typical uncomplicated viral pattern.',
'0.60~That would require CSF glucose of 72 mg/dL with this serum value.',
'3.33~That reverses the numerator and denominator.',
'0.03~This is a tenfold calculation error.',
'1.20~This does not equal 36 divided by 120.'])
custom('inf','CSF interpretation limits','21,30','Early CSF in a PCR-confirmed enteroviral illness is neutrophil predominant. Which interpretation is appropriate?',[
'Early viral meningitis can be neutrophilic~Cell type is probabilistic. Early neutrophils do not exclude viral disease, but possible bacterial meningitis still requires urgent assessment rather than automatic reassurance.',
'Neutrophils make any viral diagnosis impossible~The deck explicitly notes early viral PMNs.',
'A low protein value alone proves a bacterial cause~Protein is not independently definitive.',
'A normal glucose value excludes all bacterial disease~Early or partially treated disease can be atypical.',
'PCR never adds useful diagnostic information~Validated PCR is useful when interpreted with timing and clinical context.'])
custom('inf','CSF interpretation limits','21,30','Which bacterial pathogen can produce a mixed or mononuclear CSF response rather than the classic neutrophil pattern?',[
'Listeria monocytogenes~Listerial meningitis can have mixed or mononuclear cells, so host risk and microbiology matter more than a rigid bacterial/viral cell-type rule.',
'Adenovirus~This is a virus, not the asked bacterial exception.',
'Coxsackievirus~This is an enterovirus rather than a bacterium.',
'Cryptococcus neoformans~This is a fungus.',
'Toxoplasma gondii~This is a protozoan rather than a bacterium.'])
custom('inf','Encephalitis criteria','19','Which major feature is required by the International Encephalitis Consortium clinical case definition?',[
'Altered mental status lasting at least 24 hours with no better alternative cause~The definition then uses supportive minor findings such as fever, seizures, focal signs, pleocytosis, MRI, or EEG. It is a classification framework, not a reason to defer urgent treatment.',
'Headache alone for one hour~Headache is nonspecific and does not satisfy the major altered-mental-status criterion.',
'Neck stiffness without any brain dysfunction~That can support meningitis but is not the encephalitis major criterion.',
'Only a positive serum IgG to a remote infection~Past exposure does not establish current brain inflammation.',
'Only a normal EEG~A normal EEG does not establish encephalitis.'])
custom('inf','Encephalitis criteria','19','Altered mental status has persisted for two days without another cause, and fever, new seizures, and compatible MRI changes are present. Which classification is supported?',[
'Probable encephalitis by the major plus at least three minor criteria~Two minor findings support possible encephalitis and at least three support probable classification. Confirmed disease additionally requires appropriate etiologic/pathologic evidence.',
'Confirmed infection by a specific virus without any organism evidence~The syndrome criteria do not themselves identify or confirm a particular pathogen.',
'No encephalitis because headache is absent~Headache is not required and is not one of the formal six minor criteria.',
'Only uncomplicated conjunctivitis~Sustained brain dysfunction and seizures are not explained by superficial eye inflammation.',
'A mandatory diagnosis of bacterial meningitis~The criteria define a parenchymal syndrome, not one microbial category.'])
custom('inf','Meningeal signs','31','Neck flexion produces involuntary flexion at the hips and knees. Which sign is this?',[
'Brudzinski sign~Meningeal irritation can cause reflex hip/knee flexion with passive neck flexion. Sensitivity is limited, so absence does not exclude meningitis.',
'Kernig sign~Kernig refers to pain/resistance with knee extension when the hip is flexed.',
'Babinski sign~An extensor plantar response is an upper motor neuron sign, not this neck maneuver.',
'Romberg sign~This evaluates postural stability with visual input removed.',
'Dix-Hallpike response~That evaluates positional vestibular nystagmus, not meningismus.'])
custom('inf','Meningeal signs','31','A patient has pain and resistance when extending the knee while the hip is flexed. Which sign is present?',[
'Kernig sign~Stretching irritated meninges can cause this response. A negative sign does not safely rule out meningitis.',
'Brudzinski sign~That is hip/knee flexion provoked by neck flexion.',
'Horner syndrome~Ptosis, miosis, and anhidrosis reflect sympathetic dysfunction.',
'A relative afferent pupillary defect~This is an optic afferent examination finding.',
'A positive Rinne test~That compares air and bone hearing.'])
custom('inf','Age-dependent meningitis','31','Which presentation is particularly important in an infant with bacterial meningitis?',[
'Poor feeding, irritability, lethargy, apnea, or a bulging fontanel~Infants may lack the classic adult description of headache and stiff neck. Seizures, altered consciousness, and purpura can also occur.',
'A fully reliable absence of disease when neck stiffness is absent~Classic meningeal signs can be absent in infants.',
'Only a gradual isolated conductive hearing loss over years~That does not capture an acute systemic CNS infection.',
'Only seasonal itchy eyes~That suggests a different superficial allergic process.',
'A requirement that the infant describe severe headache verbally~Preverbal children cannot reliably report the adult symptom pattern.'])

pool('bacteria','''Group B Streptococcus~Streptococcus agalactiae is a major neonatal invasive pathogen acquired around birth; it is not the usual adolescent dormitory meningococcus.
Escherichia coli~E. coli, particularly strains with a K1 capsule, is an important gram-negative neonatal meningitis cause.
Neisseria meningitidis~An encapsulated gram-negative diplococcus can cause acute meningitis and bacteremia with petechiae/purpura, especially in crowded close-contact settings.
Streptococcus pneumoniae~An encapsulated gram-positive diplococcus is a major bacterial meningitis agent, associated with respiratory/ear sources and risk after CSF leaks or asplenia.
Listeria monocytogenes~This gram-positive intracellular rod causes meningitis in neonates, older adults, and immunocompromised patients, sometimes with mixed CSF cells.
Haemophilus influenzae type b~Encapsulated Hib can cause invasive meningitis, especially in underimmunized children; it is distinct from nontypeable AOM strains.
Mycobacterium tuberculosis~TB causes subacute/chronic meningitis, often with basal inflammation, high protein, low glucose, and lymphocytic cells.
Treponema pallidum~Syphilis can involve meninges or produce other neurologic/ocular syndromes; CSF VDRL is specific but not highly sensitive.
Borrelia burgdorferi~Lyme neuroborreliosis can cause lymphocytic meningitis, facial palsy, and painful radiculoneuritis after tick exposure.
Staphylococcus aureus~S. aureus is important in postoperative/traumatic CNS infection and hematogenous abscess, including with endocarditis.
Streptococcal oral/sinus flora~Streptococci, often with anaerobic partners, can cause brain abscess through contiguous dental/sinus infection.''')
block('inf','Bacterial pathogen recognition','bacteria','''18,31|A neonate develops fever, poor feeding, lethargy, and meningitis. Blood culture grows beta-hemolytic gram-positive cocci that are CAMP positive. Which organism fits?|Group B Streptococcus|S. agalactiae is a major neonatal meningitis pathogen. The age and microbiology distinguish it from common older-child meningococci or pneumococci.
18,31|A neonate has meningitis caused by a gram-negative enteric rod with a K1 capsule. Which organism fits?|Escherichia coli|E. coli is an important neonatal CNS pathogen, and the K1 capsule is associated with neuroinvasive strains.
18,31,37|A college student with fever, neck stiffness, and rapidly progressive purpura has gram-negative diplococci in CSF. Which pathogen is most likely?|Neisseria meningitidis|Meningococcal meningitis can accompany invasive bacteremia and a nonblanching petechial/purpuric rash. This is an urgent illness; rash is neither required nor uniquely diagnostic.
18,37|An asplenic adult develops acute meningitis with encapsulated gram-positive diplococci. Which organism is most likely?|Streptococcus pneumoniae|Pneumococcal invasive disease is promoted by impaired clearance of encapsulated bacteria. Ear/sinus infection or a CSF leak can also be relevant sources/risks.
18,21,37|An older patient on immunosuppressive therapy develops meningitis caused by a gram-positive rod with tumbling motility. Which organism fits?|Listeria monocytogenes|Listeria is important in older/immunocompromised hosts and neonates. Its CSF differential can be mixed; routine cephalosporins do not provide reliable coverage.
18,37|An underimmunized young child develops meningitis caused by an encapsulated type b gram-negative coccobacillus. Which agent fits?|Haemophilus influenzae type b|Hib invasive disease differs from common nontypeable middle-ear disease. Vaccination changes population incidence but does not make every H. influenzae infection vaccine-preventable.
18,32,34|Weeks of headache and low-grade fever are followed by cranial neuropathies and basal meningeal inflammation. CSF has lymphocytes, high protein, and low glucose. Which organism is a key concern?|Mycobacterium tuberculosis|TB meningitis is a subacute/chronic process with characteristic basal complications. NAAT and culture are more useful than relying only on an insensitive smear.
18,32,34|A patient has neurologic symptoms with reactive syphilis serology and a positive CSF VDRL. Which organism causes the underlying infection?|Treponema pallidum|T. pallidum can cause meningitis and broader neurosyphilitic syndromes. A positive appropriately interpreted CSF VDRL supports CNS involvement.
18|A patient develops facial palsy, radicular pain, and lymphocytic meningitis after a tick exposure and expanding annular rash. Which pathogen fits?|Borrelia burgdorferi|This constellation supports Lyme neuroborreliosis. The organism can involve meninges, cranial nerves, and roots rather than causing only a nonspecific rash.
18,35|A patient with S. aureus endocarditis develops a focal brain abscess. Which organism is most directly implicated?|Staphylococcus aureus|Hematogenous seeding from endocarditis can cause brain infection. This differs from the mixed oral/anaerobic flora often found after contiguous sinus or dental spread.
18,35,36|A brain abscess develops adjacent to an infected sinus; culture grows streptococci and anaerobes. Which microbial group best fits the source?|Streptococcal oral/sinus flora|Contiguous spread commonly involves streptococci and anaerobic partners. The source guides empiric coverage and diagnostic sampling.''')
pool('entryRoute','''Hematogenous dissemination~Viremia, bacteremia, or fungemia can deliver organisms to CNS interfaces, crossing barriers or trafficking with infected cells.
Retrograde axonal transport~Some neurotropic pathogens travel from peripheral nerves toward neuronal cell bodies/CNS, as in rabies and herpes pathways.
Direct contiguous spread~Sinus, middle-ear, mastoid, skull, or dental infection can extend into nearby intracranial compartments.
Direct traumatic or procedural inoculation~Penetrating injury or surgery can introduce organisms past normal protective barriers.
Postinfectious autoimmune injury~Immune-mediated inflammation/demyelination after infection differs from direct ongoing microorganism invasion.''')
block('inf','Routes and pathogenesis','entryRoute','''20,22|After mucosal replication, a virus enters the blood, amplifies in secondary sites, and crosses into the CNS. Which route is described?|Hematogenous dissemination|Viremia can precede barrier crossing. Some pathogens also use infected leukocytes; target-cell tropism influences the resulting syndrome.
20,22,27|A virus enters peripheral neurons at a bite site and travels toward the spinal cord/brain. Which route is described?|Retrograde axonal transport|Rabies uses neural transport after peripheral inoculation. This route differs from ordinary bloodstream dissemination.
29|Nasopharyngeal bacterial colonization is followed by local invasion, bacteremia, and meningeal entry. Which dissemination route is central?|Hematogenous dissemination|Transient bacteremia can precede meningeal invasion. Barrier disruption and the host inflammatory response produce CNS injury after entry.
33|Disseminated fungal infection seeds the meninges and brain from blood. Which route is described?|Hematogenous dissemination|The deck emphasizes bloodstream spread in fungal CNS disease. Host immune state and the organism determine meningeal, vascular, or parenchymal manifestations.
35,36|A sinus infection spreads into the adjacent subdural space. Which route is present?|Direct contiguous spread|Nearby infected skull/air sinus structures can extend intracranially. This can lead to empyema or abscess without requiring a primary bloodstream source.
35|A penetrating skull wound is followed by localized intracranial infection. Which route fits?|Direct traumatic or procedural inoculation|Barrier disruption permits direct entry from a wound or procedure. The inoculation context affects likely organisms.
16,17,19|White-matter demyelination begins after an infection has clinically resolved, without evidence of direct CNS microbial replication. Which mechanism fits?|Postinfectious autoimmune injury|Postinfectious immune injury can produce ADEM. Viral exposure is a trigger rather than necessarily the persistent agent in the lesion.''')
custom('inf','Bacterial inflammatory injury','29','How can meningeal inflammation impair neurologic function even beyond direct bacterial injury?',[
'Inflammatory edema and vascular/CSF disturbances can raise intracranial pressure~Subarachnoid inflammation disrupts normal physiology and can contribute to edema, ischemia, hydrocephalus, and altered consciousness.',
'It affects only the external canal without CNS consequences~The inflammation here is intracranial.',
'It necessarily lowers ICP to zero~Edema and impaired CSF handling can instead raise ICP.',
'It makes all neurologic deficits reversible immediately~Inflammatory and ischemic damage may persist.',
'Only lens opacity can alter consciousness~Brain inflammation and raised pressure can directly impair cognition/consciousness.'])
custom('inf','Viral cellular injury','20,22','Why can different viruses produce different CNS syndromes despite similar entry routes?',[
'Cell and region tropism plus direct and immune-mediated injury vary~Viruses may target neurons, glia, or endothelium and different anatomic regions, changing presentation and imaging.',
'Every virus targets exactly the same cell type~Tropism is not identical across pathogens.',
'Viral CNS injury can never involve host inflammation~Both direct cytopathic and indirect inflammatory damage occur.',
'Only the skin is injured after CNS entry~CNS target-cell injury produces neurologic symptoms.',
'Season alone identifies the virus with certainty~Season can change pretest probability but does not replace clinical/microbiologic evaluation.'])

pool('virus','''Nonpolio enteroviruses~Echoviruses and Coxsackie viruses commonly cause aseptic meningitis and can also cause encephalitis, myelitis, or other syndromes depending on type.
HSV-1~This herpesvirus classically causes sporadic necrotizing temporal lobe encephalitis, with behavioral change, seizures, and possible hemorrhagic CSF.
HSV-2~HSV-2 is a recognized cause of aseptic meningitis and can cause recurrent meningitis; it is not limited to genital skin disease.
Varicella-zoster virus~VZV can cause meningitis/encephalitis or vasculopathy, sometimes without a rash; it is also a listed postinfectious trigger.
Mumps virus~Mumps can cause aseptic meningitis with or without prominent parotitis and is a vaccine-preventable listed cause.
Lymphocytic choriomeningitis virus~LCMV is a rodent-associated arenavirus that can produce a biphasic illness and aseptic meningitis.
Adenovirus~Adenovirus is a common conjunctival/respiratory pathogen and a less common listed aseptic CNS cause, not the defining temporal-lobe herpes pathogen.
Rabies virus~Rabies follows animal exposure and neural spread; encephalitic disease may include hydrophobia, agitation, autonomic features, or paralysis and is nearly always fatal after symptoms.
HIV~Acute HIV can cause an aseptic meningeal/encephalitic syndrome, while advanced HIV predisposes to distinct opportunistic CNS and retinal infections.
West Nile virus~A mosquito-borne flavivirus can cause meningitis, encephalitis, and acute flaccid paralysis from motor neuron involvement.
Eastern equine encephalitis virus~This mosquito-borne alphavirus can cause severe encephalitis; geography, vectors, season, and testing distinguish it from other arboviruses.
Western equine encephalitis virus~This mosquito-borne alphavirus is a listed arboviral encephalitis agent; exposure epidemiology and specific testing are needed to distinguish it.
Poliovirus~Poliovirus can cause aseptic meningitis or asymmetric flaccid paralysis from anterior horn injury; paralysis is not present in every infection.
Measles virus~Measles is a listed trigger for postinfectious encephalomyelitis and can cause additional distinct neurologic complications; these should not all be conflated.
Influenza virus~Influenza can be associated with infection-triggered encephalopathy or postinfectious immune neurologic disease, not only pulmonary symptoms.''')
block('inf','Viral pathogen recognition','virus','''17,20,23|A school-age child has summer-onset aseptic meningitis with a lymphocytic CSF profile and positive enteroviral PCR. Which group is responsible?|Nonpolio enteroviruses|Enteroviruses are common aseptic meningitis agents. Clinical syndrome alone does not specify every serotype, and early CSF may still be neutrophilic.
17,25,37|A febrile adult develops personality change, focal seizures, and a temporal lobe lesion with hemorrhagic features. Which virus is most likely?|HSV-1|HSV-1 classically causes necrotizing temporal encephalitis. CSF PCR is useful; treatment should not be delayed while awaiting confirmation when suspicion is substantial.|figure-25
17,21|Recurrent episodes of aseptic meningitis occur in a patient with HSV-2 detected in CSF. Which agent causes these episodes?|HSV-2|HSV-2 can cause recurrent lymphocytic meningitis. A meningeal syndrome differs from the classic HSV-1 temporal-parenchymal presentation.
17,37|A patient develops encephalitis and cerebral vascular inflammation after shingles. Which virus is implicated?|Varicella-zoster virus|VZV can cause direct CNS infection and vasculopathy; a rash may help but is not mandatory in every neurologic case.
17|An underimmunized patient develops parotid swelling followed by aseptic meningitis. Which listed virus fits?|Mumps virus|Mumps is a recognized viral meningitis cause. CNS involvement can also occur without obvious parotitis.
17|A pet-rodent owner develops a biphasic febrile illness and aseptic meningitis. Which rodent-associated virus should be considered?|Lymphocytic choriomeningitis virus|LCMV is linked to rodent exposure. Exposure history can refine the viral differential when the CSF pattern is nonspecific.
17,37|A patient has an acute retroviral illness with aseptic meningeal symptoms and newly confirmed infection. Which virus can itself cause this early CNS syndrome?|HIV|Acute HIV can produce aseptic meningitis/meningoencephalitis. This is separate from opportunistic infections resulting from advanced immune deficiency.
17,27,28,37|Weeks after an animal bite, a patient develops bite-site paresthesia, agitation, and painful swallowing spasms triggered by water. Which virus is most likely?|Rabies virus|Rabies can produce hydrophobia from pharyngeal spasms, followed by progressive neurologic disease. Hydrophobia is characteristic but not present in every case.
17,26,37|After mosquito exposure, an older patient develops encephalitis and asymmetric flaccid weakness due to anterior horn injury. Which listed arbovirus is especially associated?|West Nile virus|West Nile neuroinvasive disease can combine meningoencephalitis and a polio-like motor syndrome. This is a nonpolio cause of acute flaccid paralysis.
17,26|An unvaccinated patient develops asymmetric flaccid paralysis after a febrile gastrointestinal illness. Testing identifies poliovirus. Which pathogen is responsible?|Poliovirus|Anterior horn motor neuron injury causes weakness, wasting, and hyporeflexia with relative sensory sparing. Poliovirus also causes nonparalytic/asymptomatic infections.
17,19|A child develops an ADEM-like syndrome after measles. Which listed infection is the preceding trigger?|Measles virus|Measles can trigger postinfectious immune demyelination. This mechanism is distinct from directly equating all measles CNS complications with ADEM.
17|A patient develops postinfectious neurologic inflammation after influenza. Which listed virus is the antecedent trigger?|Influenza virus|Influenza can be associated with several infection-triggered neurologic syndromes. Defining the syndrome requires examination, imaging, and exclusion of active/alternative causes.''')
custom('inf','Enterovirus course','23','Which feature is illustrated by the enterovirus time-course graph?',[
'A minor systemic phase may precede neurologic illness, while fecal shedding can outlast viremia~The source graph shows a possible biphasic illness and different detection windows in blood, throat, stool, and CSF. Its timeline is illustrative, not identical for all types.',
'Virus must remain equally detectable in every specimen indefinitely~Detection changes with specimen and time.',
'Neutralizing antibody peaks before exposure~Antibody rises after infection rather than before initial exposure in a susceptible host.',
'All infections produce immediate paralysis on the first day~Many are asymptomatic or nonparalytic, and incubation/clinical progression varies.',
'A negative blood test at a later time excludes prior infection~Viremia can resolve while other evidence remains.'])
custom('inf','Enterovirus syndromes','23','Which spectrum is consistent with the enterovirus table?',[
'Aseptic meningitis, encephalitis, paralysis, ataxia, cranial neuropathy, and selected chronic infections~Different enteroviruses can cause overlapping neurologic syndromes; a type-to-syndrome table is not a one-to-one rule.',
'Only otitis externa~Enteroviruses have a much broader systemic/CNS spectrum.',
'Only retinitis in advanced HIV~That is a classic CMV context, not the full enterovirus spectrum.',
'Only pyogenic brain abscess~Enteroviruses do not define that suppurative category.',
'No CNS disease because they replicate initially outside the CNS~Peripheral entry does not prevent neuroinvasion.'])
custom('inf','Enterovirus classification','23','The historical table lists enterovirus 72 as hepatitis A virus. What is the appropriate qualification?',[
'Hepatitis A virus is now classified in the genus Hepatovirus~The table preserves older nomenclature. Current classification should not treat HAV as a routine modern enterovirus CNS cause solely from that old label.',
'Hepatitis A is a herpesvirus~It is not a herpesvirus.',
'Every modern enterovirus is a hepatitis A subtype~Enterovirus and Hepatovirus are distinct genera.',
'The historical label proves that HAV commonly causes all listed encephalitis cases~A historical classification does not establish clinical frequency.',
'Hepatitis A contains no nucleic acid~HAV is an RNA virus.'])
pool('coxsackie','''Coxsackie A-associated hand-foot-mouth/herpangina pattern~Coxsackie A types commonly cause oral lesions or hand-foot-mouth disease; EV-A71 and other enteroviruses may also cause HFMD.
Coxsackie B-associated pleurodynia/myocarditis pattern~Coxsackie B types are particularly associated with painful chest/abdominal muscle illness and cardiac or systemic neonatal disease.
Coxsackie A24-associated acute hemorrhagic conjunctivitis~Coxsackie A24 variant and enterovirus 70 can cause acute hemorrhagic conjunctivitis with outbreaks.
Enteroviral aseptic meningitis~Both Coxsackie groups and echoviruses can cause a febrile meningeal syndrome; serotype is not determined by neck stiffness alone.
Enterovirus-associated motor disease~Selected Coxsackie or other enterovirus types can cause sporadic paralysis; motor disease is not limited to poliovirus.''')
block('inf','Coxsackie clinical associations','coxsackie','''24|A child has fever, painful oral lesions, and vesicles on the hands and feet. Which association is most characteristic in the deck?|Coxsackie A-associated hand-foot-mouth/herpangina pattern|HFMD and herpangina are classic Coxsackie A associations. The syndrome can also involve EV-A71 and other types, so the association is not exclusive.
24|A child has posterior oral vesicles and fever without a CNS deficit. Which listed pattern fits herpangina?|Coxsackie A-associated hand-foot-mouth/herpangina pattern|Herpangina commonly involves Coxsackie A. It is an oral syndrome and does not automatically imply encephalitis.
24|An adult has abrupt fever and severe episodic chest-wall muscle pain during an enterovirus outbreak. Which association fits pleurodynia?|Coxsackie B-associated pleurodynia/myocarditis pattern|Coxsackie B is associated with pleurodynia and myocarditis. The table also lists neonatal disease, orchitis, and pancreatic associations.
24|An outbreak produces painful red eyes with subconjunctival hemorrhage and Coxsackie A24 variant is detected. Which association fits?|Coxsackie A24-associated acute hemorrhagic conjunctivitis|Acute hemorrhagic conjunctivitis is associated with Coxsackie A24 variant and enterovirus 70. It is distinct from a corneal ulcer.
24|A patient has acute fever, headache, photophobia, and neck stiffness with Coxsackie virus detected in CSF. Which syndrome fits?|Enteroviral aseptic meningitis|Coxsackie illness commonly includes meningitis and may fluctuate over days. New progressive lethargy, disorientation, or seizures suggest more serious parenchymal involvement.
17,24,26|A Coxsackie infection is followed by an acute flaccid motor syndrome. Which statement best captures the table association?|Enterovirus-associated motor disease|Selected nonpolio enteroviruses can cause motor disease. The source gives specific historical A-type examples; syndrome and confirmatory testing are more useful than assuming paralysis proves polio.''')
custom('inf','Coxsackie systemic associations','24','Which group of non-CNS associations is emphasized for Coxsackie B in the lecture table?',[
'Neonatal systemic disease, pleurodynia, orchitis, and pancreatic associations~The table also includes carditis and rash in both groups. Associations are not proof of causation for every individual episode of diabetes or pancreatitis.',
'Only herpangina and hand-foot-mouth disease~These are emphasized more for Coxsackie A in the table.',
'Only chronic fungal meningitis~Coxsackie viruses are not fungi.',
'Only a fixed middle-ear air-bone gap~That does not represent the table’s systemic viral syndromes.',
'Only CMV retinitis~CMV is a different virus with a different classic immune context.'])
custom('inf','Rash interpretation','24,31','A febrile patient has a rash that does not blanch with pressure. Which interpretation is safest and most accurate?',[
'Petechiae/purpura reflect bleeding into skin and require assessment for invasive disease~Such lesions may occur in several infections, including enteroviral illness, but fever with nonblanching rash raises urgent concern for meningococcemia and other serious causes.',
'The glass test proves Coxsackie infection~Nonblanching is not organism-specific.',
'Absence of blanching excludes sepsis~It can be an important sepsis warning sign.',
'Every blanching rash is harmless~Blanching alone does not establish benignity.',
'Petechiae cannot occur in meningococcal disease~They are a recognized invasive meningococcal finding.'])

custom('inf','Rabies peripheral phase','27,28','Why can rabies postexposure prophylaxis work before symptoms begin?',[
'Peripheral incubation provides time for local antibody and active vaccine immunity before CNS disease~Wound care, exposure risk assessment, and indicated PEP act before established neurologic infection. Waiting for symptoms forfeits this preventive opportunity.',
'The vaccine reliably cures established symptomatic encephalitis~PEP prevents disease; it is not an established cure once neurologic rabies appears.',
'Rabies never enters nerves~Neural entry and transport are central to its pathogenesis.',
'Natural antibody always fully protects before neural spread~A timely effective natural response cannot be assumed.',
'Animal bites cannot transmit rabies until the wound becomes infected with bacteria~Rabies inoculation does not require secondary bacterial infection.'])
custom('inf','Rabies transport','27','Which event follows local rabies inoculation and possible muscle replication?',[
'Entry into peripheral nerves followed by retrograde transport toward the CNS~Motor and sensory neural pathways can contribute. The slide’s dorsal-root-focused diagram is a simplified illustration, not an exclusive route.',
'Immediate universal viremia as the only route~Rabies neuroinvasion is characteristically neural rather than ordinary hematogenous dissemination.',
'Direct conversion of muscle cells into brain tissue~This is not the transport mechanism.',
'Restriction of the virus permanently to the skin~Untreated infection can invade the CNS.',
'Elimination by antibiotics targeting bacterial cell walls~Rabies is a virus and lacks a bacterial wall.'])
custom('inf','Rabies incubation','27,28','Which factors can affect the incubation period after rabies exposure?',[
'Inoculum and the exposure site’s relationship to neural pathways/CNS distance~Incubation is variable, often weeks to months, but can be shorter or longer. The slide’s 60–365-day table is not a strict boundary.',
'A fixed 60-day minimum in every person~Clinical incubation can be shorter.',
'A fixed one-year maximum in every person~Longer incubation is possible.',
'Only the appearance of a bacterial culture from the wound~Rabies progression is not determined solely by bacterial wound infection.',
'Only CSF neutrophil count on exposure day~CSF is not the routine determinant of exposure incubation risk.'])
custom('inf','Rabies prodrome','28','Which symptoms may precede classic neurologic rabies?',[
'Fever, malaise, gastrointestinal symptoms, and pain or paresthesia at the bite site~The prodrome is nonspecific, but unusual sensations at the exposure site can be a clue before encephalitic or paralytic disease.',
'Only an asymptomatic state forever~The prodrome marks the transition toward symptomatic disease.',
'Only a unilateral corneal ulcer~That is not the characteristic rabies prodrome.',
'Only a bulging tympanic membrane~That suggests middle-ear infection, not the listed prodrome.',
'Only a stable old visual field defect~That does not capture acute evolving rabies symptoms.'])
custom('inf','Rabies hydrophobia','28','What most directly explains hydrophobia in encephalitic rabies?',[
'Painful pharyngeal/inspiratory spasms provoked by attempts to swallow~Water-triggered swallowing spasms can produce apparent fear of drinking. Hydrophobia is characteristic but neither universal nor required in paralytic rabies.',
'A learned dislike of water without any motor abnormality~The characteristic symptom has a neurologic spasm basis.',
'Mechanical obstruction of the external auditory canal~That cannot explain pharyngeal spasms.',
'A definitive absence of CNS involvement~Hydrophobia is a neurologic disease feature.',
'A symptom present in every infected person during asymptomatic incubation~It occurs during clinical disease and is not universal.'])
custom('inf','Rabies late phase','27,28','Which sequence is compatible with progressive clinical rabies?',[
'Neurologic dysfunction followed by paralysis/coma and respiratory or autonomic failure~Seizures, hallucinations, disorientation, pharyngeal spasms, and paralysis can occur. Once symptoms appear, rabies is nearly always fatal, with rare exceptions.',
'Guaranteed complete recovery without treatment after hydrophobia~That is inconsistent with the grave prognosis of clinical rabies.',
'Permanent confinement to muscle after neurologic symptoms~Neurologic symptoms imply CNS involvement.',
'Predictable cure by wound washing after coma begins~Wound care is preventive early management, not a cure for established encephalitis.',
'No dissemination beyond brain at any stage~Virus can spread centrifugally to salivary glands and other tissues.'])
custom('inf','Rabies centrifugal spread','27,28','Why can saliva become infectious during rabies disease?',[
'Virus spreads from CNS through peripheral pathways to salivary glands~Centrifugal dissemination supports transmission by saliva. Clinical appearance alone does not replace exposure-specific public health assessment.',
'Every human antibody becomes a virion~Antibodies are not converted into virus.',
'The vaccine causes salivary gland infection~Proper rabies vaccine is preventive and does not cause this pathogenesis.',
'Only oral bacteria manufacture the virus~Rabies is a distinct viral infection.',
'CSF directly drains into saliva without tissue spread~Neural/organ dissemination, not direct CSF drainage, explains viral salivary involvement.'])
custom('inf','Rabies prophylaxis application','27','An unvaccinated immunocompetent adult has an exposure for which rabies PEP is indicated. Which combination is appropriate in the CDC framework?',[
'Wound cleansing, rabies immune globulin, and a vaccine series~Passive antibody offers immediate local protection while vaccination induces active immunity. Previously vaccinated patients and immunocompromised patients have different details; dosing/placement follows current guidance.',
'Vaccine only after hydrophobia begins~PEP should not be deferred until clinical disease.',
'Antibiotics alone~Antibiotics do not prevent rabies virus neuroinvasion.',
'Immune globulin alone with no active vaccination~An unvaccinated person generally needs both passive and active prophylaxis when PEP is indicated.',
'No care because the bite has already healed~A healed wound does not by itself eliminate rabies risk.'])

pool('fungus','''Cryptococcus neoformans~An encapsulated yeast causes subacute/chronic meningoencephalitis, particularly in advanced HIV or other immunosuppression; CrAg is an important diagnostic test.
Coccidioides species~An endemic dimorphic fungus of arid southwestern environments can disseminate from lung to cause chronic meningitis and hydrocephalus.
Candida species~Disseminated candidiasis can seed CNS parenchyma and form microabscesses; yeast and pseudohyphae distinguish it from angioinvasive molds.
Aspergillus species~Septate acute-angle branching hyphae can invade vessels, causing hemorrhage/infarction and CNS masses or abscesses in susceptible hosts.
Mucorales~Broad pauciseptate hyphae with angioinvasion can cause rhino-orbital-cerebral disease, particularly with ketoacidosis or major immune impairment.
Histoplasma capsulatum~An endemic dimorphic fungus can disseminate, including chronic meningitis or focal CNS disease; tissue may show small intracellular yeasts.
Blastomyces species~Blastomycosis can involve CNS after dissemination; broad-based budding yeast is a useful high-yield identification clue.
Sporothrix species~This dimorphic fungus can rarely cause chronic meningitis, especially with disseminated disease or immune impairment; CNS disease is not limited to common lymphocutaneous nodules.''')
block('inf','Fungal CNS pathogens','fungus','''18,32,33,37|An adult with advanced HIV has weeks of headache, high opening pressure, and positive CSF capsular antigen from an encapsulated yeast. Which pathogen fits?|Cryptococcus neoformans|Cryptococcus commonly causes subacute meningoencephalitis in this host. CSF can have few cells despite severe disease, and raised pressure is clinically important.
33,37|A patient living in the desert Southwest has pulmonary fungal infection followed by chronic meningitis and hydrocephalus. Which fungus is a key concern?|Coccidioides species|Coccidioides can disseminate to meninges. Geographic exposure and chronic low-glucose CSF refine the differential but require specific confirmation.
18,33|A patient with candidemia develops multiple small CNS abscesses. Microscopy shows budding yeast and pseudohyphae. Which organism fits?|Candida species|Hematogenous Candida can invade parenchyma and produce microabscesses. This differs from a purely superficial colonization diagnosis.
33|A neutropenic patient has hemorrhagic cerebral lesions with vascular invasion by septate acute-angle branching hyphae. Which fungus fits?|Aspergillus species|Angioinvasion causes vascular injury, infarction, or hemorrhage. The deck emphasizes vascular and mass-forming manifestations of invasive molds.
33|A patient with diabetic ketoacidosis develops sinus infection, orbital involvement, and cerebral vascular invasion by broad pauciseptate hyphae. Which fungal group fits?|Mucorales|Rhino-orbital-cerebral mucormycosis can spread contiguously and invade vessels. The older 'zygomycetes' table label is broader historical terminology.
33|A patient with disseminated fungal disease has small intracellular yeasts and chronic meningeal symptoms after relevant endemic exposure. Which listed agent fits?|Histoplasma capsulatum|Histoplasma can involve CNS during dissemination. This is a supplemental organism-identification application of the fungal table.
33|A disseminated fungal infection with broad-based budding yeast involves the CNS. Which listed genus is favored?|Blastomyces species|Broad-based budding is a high-yield Blastomyces clue. CNS involvement can be meningeal or focal, although less common than pulmonary disease.
33|A patient with disseminated sporotrichosis develops chronic meningitis. Which organism is responsible?|Sporothrix species|Sporothrix is included in the table as an occasional meningeal cause. A familiar cutaneous association does not exclude disseminated CNS disease.''')
custom('inf','Fungal injury patterns','33','Which grouping correctly summarizes the major fungal CNS injury mechanisms in the deck?',[
'Chronic meningitis, vascular invasion, and parenchymal invasion/mass formation~Cryptococcus and Coccidioides emphasize meningitis, while invasive molds prominently involve vessels and focal masses. Organisms can overlap these categories.',
'Only external-ear irritation without deeper invasion~Fungi can cause serious CNS disease.',
'Only transient ciliary muscle spasm~That is not fungal CNS pathogenesis.',
'Only a sterile autoimmune response with no organism invasion~Direct fungal invasion is important in these conditions.',
'A requirement that every fungus produce identical CSF values~Profiles depend on pathogen, location, and host immunity.'])
custom('inf','Fungal table interpretation','33','How should the table’s plus signs and labels such as common/occasional be interpreted?',[
'As qualitative source comparisons rather than precise universal incidence estimates~The table indicates tendencies toward meningitis or mass lesions. It does not provide a denominator, patient-specific risk, or current incidence for every region.',
'As exact population percentages~Plus signs are not percentage values.',
'As proof a fungus cannot cause a less-emphasized syndrome~The categories are not exclusive.',
'As a replacement for immune status and exposure history~Those factors remain central to diagnosis.',
'As evidence that all fungal cases are cryptococcal~The table includes several distinct organisms.'])

pool('parasite','''Toxoplasma gondii~A protozoan can reactivate in advanced HIV, causing multiple enhancing focal brain lesions, and is important in retinochoroiditis.
Taenia solium larvae~Neurocysticercosis follows ingestion of eggs shed by a human tapeworm carrier; CNS larval cysts can cause seizures, inflammation, or hydrocephalus.
Naegleria fowleri~Warm freshwater entering the nose can lead to fulminant primary amebic meningoencephalitis, often with neutrophilic CSF and possible motile trophozoites.
Acanthamoeba species~Free-living amebas can cause keratitis and more indolent granulomatous amebic encephalitis, especially in susceptible hosts.
Balamuthia mandrillaris~This free-living ameba can cause granulomatous encephalitis, sometimes after skin or inhalational exposure and including immunocompetent people.
Echinococcus granulosus~Ingestion of eggs from a dog-associated life cycle can lead to hydatid cysts, occasionally in the brain; a hydatid cyst is not a routine pyogenic abscess.
Plasmodium falciparum~Severe malaria can cause cerebral disease through infected erythrocyte sequestration and microvascular dysfunction, not a typical encysted brain abscess.
Trypanosoma brucei~Tsetse-transmitted African trypanosomiasis can enter the CNS and cause sleep-cycle disturbance, cognitive change, and meningoencephalitis.''')
block('inf','Parasitic and amebic CNS disease','parasite','''9,18,35,37|A patient with advanced HIV has subacute headache, focal weakness, and multiple ring-enhancing brain lesions, often involving basal ganglia. Which pathogen is a major concern?|Toxoplasma gondii|Reactivation toxoplasmosis commonly causes focal encephalitis/abscess-like lesions. Primary CNS lymphoma and other infections remain alternatives; ring enhancement alone is not diagnostic.
18,35,37|A person from an endemic region develops seizures with parenchymal cysts, some showing a scolex and others calcified. Which pathogen fits?|Taenia solium larvae|Neurocysticercosis can produce viable, degenerating, or calcified cysts. It is a larval cyst disease rather than an ordinary bacterial pus collection.
18,34|A previously healthy swimmer develops rapidly fatal meningoencephalitis after warm freshwater entered the nose. Which agent is most likely?|Naegleria fowleri|Naegleria enters through nasal/olfactory pathways and causes PAM. The CSF can resemble bacterial meningitis with neutrophils and low glucose.
18,37|An immunocompromised patient develops slowly progressive granulomatous encephalitis due to a free-living ameba also known for contact lens keratitis. Which organism fits?|Acanthamoeba species|Acanthamoeba can cause granulomatous amebic encephalitis and keratitis, with different entry routes and host contexts.
18|A patient has a preceding skin lesion followed by granulomatous amebic encephalitis; testing identifies Balamuthia. Which organism is responsible?|Balamuthia mandrillaris|Balamuthia can enter through skin or respiratory routes and cause CNS disease, including in people without major immune suppression.
37|A patient with dog-associated exposure develops a large cerebral hydatid cyst. Which parasite is implicated?|Echinococcus granulosus|Hydatid disease results from the larval stage after egg ingestion. Avoiding rupture is an important procedural concern; it is distinct from a pyogenic abscess.
37|A traveler has severe malaria, impaired consciousness, and parasitized red cells. Which organism listed in the deck is most associated with cerebral malaria?|Plasmodium falciparum|Infected erythrocyte sequestration and microvascular dysfunction contribute to cerebral malaria. This is not a typical focal larval cyst infection.
37|After tsetse exposure in sub-Saharan Africa, a patient develops progressive sleep disturbance and meningoencephalitis. Which organism fits?|Trypanosoma brucei|African trypanosomiasis can progress from systemic infection to CNS involvement. Geography, exposure, parasite detection, and staging guide evaluation.''')
custom('inf','Neurocysticercosis transmission','35,37','Which exposure directly causes human cysticercosis?',[
'Ingestion of Taenia solium eggs from fecal contamination by a human tapeworm carrier~Eggs release larvae that invade tissues. Eating pork containing cysticerci instead produces intestinal taeniasis, not direct tissue cysticercosis.',
'Ingestion of pork cysticerci as the direct cause of CNS cysts~That primarily causes an adult intestinal tapeworm; the tissue disease route is egg ingestion.',
'A mosquito inoculates Taenia larvae into blood~Taenia solium is not mosquito transmitted.',
'A dog bite transmits rabies and Taenia by the same route~Rabies exposure is distinct from fecal-oral Taenia eggs.',
'Swimming with freshwater entering the nose~That is the classic Naegleria exposure, not cysticercosis.'])
custom('inf','Parasitic CSF exceptions','34','Which statement best corrects the broad claim that parasites usually produce CSF eosinophilia?',[
'Eosinophilia is most helpful for selected helminths and is not universal across parasites~Naegleria can be neutrophilic, other protozoal cases can be lymphocytic, and a focal parenchymal infection may have little CSF inflammation.',
'Every Toxoplasma brain lesion must produce predominantly eosinophilic CSF~This is not a reliable toxoplasmosis rule.',
'Naegleria can never have neutrophils~PAM often has a neutrophilic pattern.',
'Normal CSF always excludes a parenchymal parasitic lesion~Focal disease may not produce a strong meningeal CSF response.',
'Eosinophils identify the exact parasite without exposure history~Several infectious and noninfectious conditions can cause eosinophilia.'])
custom('inf','Abscess versus cyst','18,35','Why should Taenia solium not be treated as simply another routine pyogenic brain-abscess organism?',[
'It causes larval cysticercosis with stage- and location-dependent inflammation~Degenerating cysts can enhance and cause seizures, but their biology and management differ from a bacterial pus collection.',
'It is a bacterium with the same cell wall as streptococci~Taenia is a cestode parasite.',
'Every ring-enhancing lesion has identical treatment~Etiology, location, burden, and lesion stage change management.',
'It causes only external canal infection~Neurocysticercosis affects CNS tissues/compartments.',
'It cannot cause seizures~Seizures are a common manifestation.'])
custom('inf','Prion differential','37','A patient develops rapidly progressive dementia, myoclonus, and ataxia without a typical inflammatory CSF profile. Which listed agent class can produce disease through protein misfolding?',[
'Prions~Prion propagation involves misfolded protein, not a conventional bacterium or virus. Spongiform neurodegeneration is distinct from the deck’s usual inflammatory meningitis/encephalitis patterns.',
'Enteroviruses~These are RNA viruses that can cause aseptic inflammatory CNS syndromes.',
'Cryptococcus~This is an encapsulated yeast associated with meningeal infection.',
'Taenia solium~This is a larval cestode infection causing cysticercosis.',
'Neisseria meningitidis~This is a bacterium causing acute pyogenic meningitis/bacteremia.'])
custom('inf','Arboviral pathogen list','17,37','Which pair from the final pathogen list consists of mosquito-borne alphaviruses associated with encephalitis?',[
'Eastern and Western equine encephalitis viruses~Both are arboviral encephalitis agents. West Nile is also mosquito-borne but belongs to a different viral family/genus grouping.',
'HSV-1 and HSV-2~These are herpesviruses, not mosquito-borne alphaviruses.',
'Rabies and LCMV~These have mammalian/rodent exposure pathways and are not the equine alphavirus pair.',
'HIV and CMV~These are not the mosquito-borne alphaviruses asked about.',
'Mumps and parainfluenza viruses~These are respiratory-associated paramyxovirus groups, not equine alphaviruses.'])
custom('inf','Listed postinfectious triggers','17','Which set contains the postinfectious encephalitis/demyelination triggers listed in the source?',[
'Measles, mumps, rubella, varicella-zoster, and influenza~These infections are listed as possible preceding triggers. Not every neurologic syndrome after these infections is ADEM or necessarily caused by persistent CNS replication.',
'Only Pseudomonas and Staphylococcus~Those are not the listed postinfectious viral set.',
'Only Cryptococcus and Coccidioides~Those are fungi associated with direct CNS infection.',
'Only Taenia and Echinococcus~Those are helminthic cyst diseases rather than this viral trigger list.',
'Only Neisseria and pneumococcus~Those are acute pyogenic meningitis agents.'])
custom('inf','Aseptic pathogen list','17','Which set contains additional viral meningitis agents explicitly listed in the deck?',[
'Adenovirus, mumps, LCMV, and parainfluenza types 2/3~The list complements common enteroviruses and HSV-2. A list association does not mean all agents are equally frequent in every age group.',
'Listeria, pneumococcus, and E. coli~These are bacterial rather than viral agents.',
'Candida, Aspergillus, and Mucorales~These are fungal agents.',
'Taenia, Echinococcus, and Plasmodium~These are parasitic agents.',
'Prions only~Prions are not conventional viruses and typically do not cause inflammatory aseptic meningitis.'])
custom('inf','Intracranial collection microbiology','18,36','Which microbial pattern is compatible with intracranial empyema spreading from sinus/skull infection?',[
'Mixed flora including streptococci, staphylococci, and anaerobes~Organisms depend on source, trauma/surgery, and host. Anaerobic gram-negative organisms can be included; fungal causes occur in selected hosts rather than every case.',
'A requirement that every case contain only Neisseria~Empyema is not restricted to meningococcus.',
'A requirement that every collection be a Taenia larval cyst~A cysticercus is biologically distinct from purulent empyema.',
'Only respiratory viruses without possible bacterial involvement~Suppurative collections commonly involve bacteria.',
'A single identical organism in every geographic setting~Source and host context affect microbiology.'])

custom('inf','Diagnostic urgency','19,21,29,31','Bacterial meningitis is strongly suspected, but lumbar puncture will be delayed. Which approach is appropriate?',[
'Obtain blood cultures promptly if feasible and start empiric therapy without waiting for delayed LP~Diagnostic sampling is valuable, but suspected bacterial meningitis requires time-sensitive treatment. Imaging or procedural delay should not delay antibiotics.',
'Wait until every CSF test is final before treatment~This can dangerously postpone therapy.',
'Treat only if all classic meningeal signs are present~Their absence does not safely exclude disease.',
'Assume normal initial blood tests exclude CNS infection~Routine blood results are not sufficient to rule it out.',
'Delay treatment for a repeat visit several days later~The suspected acute bacterial syndrome warrants urgent care.'])
custom('inf','Diagnostic urgency','25,35,36','A patient with suspected intracranial abscess has focal deficits and papilledema. What should precede consideration of LP?',[
'Urgent neuroimaging and evaluation for mass effect or other LP contraindications~A mass lesion may create dangerous pressure gradients. LP is often unhelpful or unsafe in focal abscess; imaging and specialist/source-directed evaluation take priority.',
'Automatic immediate LP in every patient with fever~Possible mass effect changes procedural safety.',
'Reassurance because all ring lesions are benign~Abscess and other mass lesions can be life threatening.',
'An isolated surface eye swab as the complete evaluation~This does not assess intracranial mass effect.',
'A normal external ear examination as proof no abscess exists~A brain abscess can occur without visible external-ear disease.'])
custom('inf','Diagnostic evidence limits','20,21,30,32,34','Which statement about negative CSF tests is most accurate?',[
'Sensitivity depends on timing, specimen, organism, and prior treatment~A negative test or a panel lacking the organism cannot exclude every CNS infection. Interpretation should integrate clinical syndrome and exposure/host information.',
'Any negative multiplex result excludes all infections~Panels do not cover every pathogen and sensitivity is not perfect.',
'A negative Gram stain excludes TB, fungi, and viruses~These require organism-appropriate tests and may not be visible on routine Gram stain.',
'A normal cell count always excludes severe infection in immune suppression~The immune response can be blunted.',
'One positive antibody to a remote infection proves active CNS disease~Past exposure and active neuroinvasion are not equivalent.'])

block('inf','Extended eye and ear cases','eyeBug','''4,5|A 27-year-old contact lens wearer develops progressive severe pain in one eye after a weekend of swimming. He admits rinsing his lenses and case with tap water. The eye is markedly photophobic, and examination shows a corneal ring infiltrate. The degree of pain seems greater than expected from the initial surface findings. A standard short antibacterial course has not helped. Which pathogen is particularly important to investigate, while recognizing that exposure and morphology do not by themselves provide definitive microbiologic identification?|Acanthamoeba species|Water-contaminated lens practices, severe pain, and a ring infiltrate are characteristic Acanthamoeba clues. Corneal evaluation and organism-directed diagnostics are needed; this is not routine superficial conjunctivitis.
8,9|A 41-year-old man with untreated advanced HIV reports new floaters, blurred vision, and a dark region in one visual field. His CD4 count is 19/µL. He has little external redness or discharge, but dilated examination shows expanding pale necrotic retinal areas with associated hemorrhage. The clinician explains that a positive blood viral test alone would not establish the ocular cause and arranges urgent retinal assessment. Which organism best fits the immune context and posterior-segment findings?|Cytomegalovirus|CMV retinitis is especially associated with profound cellular immune deficiency. The retinal lesion, not a nonspecific surface symptom or blood PCR alone, establishes the clinical concern. Prompt treatment assessment protects remaining vision.''')
block('inf','Extended eye and ear cases','earDx','''11,12,13,14|A 2-year-old develops fever, irritability, poor sleep, and deep right ear pain several days after a respiratory illness. The parent reports that the child seems to hear less clearly. The external canal is not notably swollen, and moving the auricle does not reproduce the severe pain. Pneumatic otoscopy reveals an opaque bulging tympanic membrane with markedly reduced movement. Which diagnosis best explains how the respiratory illness led to fluid accumulation, pressure, and a conductive hearing problem?|Acute otitis media|Upper-airway inflammation can impair Eustachian ventilation, promoting middle-ear stasis and infection. Acute symptoms plus a bulging poorly mobile drum distinguish AOM from isolated canal infection and from a nonacute effusion.''')
block('inf','Extended CNS cases','csfPattern','''18,19,21,29,30,31|A 20-year-old student develops fever, severe headache, photophobia, and neck stiffness over several hours. He becomes drowsy and has scattered nonblanching petechiae. After urgent assessment, CSF is obtained: 4,500 WBC/µL with neutrophil predominance, protein 310 mg/dL, and glucose 18 mg/dL with concurrent serum glucose 90 mg/dL. The team does not wait for final cultures before starting treatment. Which broad CSF category best fits this rapidly evolving syndrome and laboratory profile?|Acute pyogenic bacterial pattern|The ratio is 0.20 with marked neutrophilic inflammation and high protein. Invasive meningococcal disease is a concern given the rash/context, but the pattern alone does not identify the organism. Prompt empiric therapy is essential.
18,32,33,34|A patient receiving intense immunosuppression develops several weeks of headache and nausea. There is no dramatic neck stiffness, and the peripheral blood count is not striking. Lumbar puncture, performed after appropriate assessment, shows high opening pressure, modest lymphocytes, increased protein, and reduced glucose. CSF antigen testing identifies an encapsulated yeast. Which category best describes this profile and explains why a limited cellular response should not falsely reassure the clinician?|Cryptococcal or other fungal meningitis pattern|Cryptococcus can produce severe meningoencephalitis with little CSF pleocytosis in an immunocompromised host. Opening pressure and organism-specific antigen findings are crucial; a mild cell count is not evidence of trivial disease.''')
block('inf','Extended CNS cases','virus','''17,19,20,21,25,37|A 46-year-old previously healthy adult develops fever and headache, then becomes unusually irritable and forgetful. Over the next day he has a focal seizure and difficulty naming objects. MRI shows a temporal lobe abnormality with hemorrhagic features, illustrated here. CSF has lymphocytes, increased protein, and some erythrocytes. The clinician interprets the red cells cautiously because a traumatic tap is also possible, but the clinical and imaging pattern strongly suggests a treatable neurotropic infection. Which virus is most likely?|HSV-1|Temporal parenchymal injury with behavioral change and seizures is characteristic of HSV-1 encephalitis. CSF PCR supports diagnosis; hemorrhagic CSF can occur but is neither required nor specific by itself.|figure-25
17,27,28,37|A traveler was bitten by a dog and did not seek exposure assessment. Several weeks later he develops fever, malaise, and tingling around the healed bite. This progresses to agitation, confusion, and painful spasms when he attempts to drink water. Family members initially assume that the healed skin means the original exposure is no longer relevant. Which virus best explains the delayed progression from a peripheral inoculation site to an encephalitic syndrome through neural transport?|Rabies virus|Rabies can incubate after wound healing, then enter neural pathways and cause devastating CNS disease. Water-triggered pharyngeal spasms are characteristic; prophylaxis acts before symptoms and is not replaced by waiting for clinical illness.''')
block('inf','Extended CNS cases','cnsSyndrome','''16,17,19|A 9-year-old recovers from a febrile respiratory illness and returns to school. About two weeks later, he develops reduced alertness, unsteady walking, and weakness affecting different limbs. Fever is now mild. MRI shows large multifocal white-matter abnormalities rather than an isolated hemorrhagic temporal lesion. Infectious and other alternative causes are being evaluated, but the overall pattern suggests an immune-mediated response after the original illness. Which syndrome best fits the mechanism and anatomic distribution?|Acute disseminated encephalomyelitis|ADEM is a postinfectious inflammatory demyelinating syndrome with encephalopathy and multifocal deficits. It is not simply direct viral multiplication in neurons, and not every postinfectious encephalopathy is ADEM.''')
block('inf','Extended parasitic cases','parasite','''18,20,22,34|A 16-year-old develops severe headache, fever, vomiting, and rapidly worsening confusion five days after diving in a warm freshwater lake. Water had forcefully entered the nose. CSF contains many neutrophils, high protein, and low glucose, initially resembling bacterial meningitis. Fresh microscopy identifies motile organisms, prompting urgent reference testing and specialized therapy consultation. Which organism best explains both the nasal/olfactory exposure route and the unusually fulminant meningoencephalitic course?|Naegleria fowleri|Naegleria causes primary amebic meningoencephalitis after contaminated water enters the nose. A neutrophilic CSF profile does not make it bacterial; fresh wet mount and specific molecular testing can identify the organism.
18,35,37|A 32-year-old who lived in an endemic region presents after a new seizure. Brain imaging shows several lesions at different stages, including a cyst with a visible scolex and calcified nodules. A household contact previously had an intestinal pork tapeworm. The patient does not eat pork and therefore initially rejects the proposed diagnosis. Which pathogen fits the imaging and explains why abstaining from pork does not exclude tissue infection acquired through fecal contamination?|Taenia solium larvae|Human cysticercosis follows ingestion of eggs from a human carrier. It can occur without pork consumption. Larval brain cysts can be viable, inflamed, or calcified and should not be equated with a uniform pyogenic abscess.''')

# Clarify why a broader overlapping diagnosis is less specific in the first lesion-identification item.
for option in questions[0]['options']:
 if option['text']=='Infectious keratitis':
  option['why']='Keratitis is the broader corneal inflammatory process that can underlie this lesion. The explicit epithelial defect and stromal tissue loss make corneal ulcer the more specific single best answer.'

if __name__=='__main__':
 (R/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf8')
 print(len(questions),'questions')


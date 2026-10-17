"""Original educational questions. Pools provide disease-specific distractor teaching points."""
from pathlib import Path
import json, random
R=Path(__file__).parent
questions=[]
pools={}
def pool(name, text):
    pools[name]=dict(line.split('~',1) for line in text.strip().splitlines())
def block(deck,topic,poolname,text):
    for line in text.strip().splitlines():
        refs,stem,answer,why,*fig=line.split('|')
        pages=[int(n) for n in refs.split(',')]
        candidates=[(a,b) for a,b in pools[poolname].items() if a!=answer]
        rng=random.Random(6060+len(questions)); rng.shuffle(candidates)
        opts=[{'text':answer,'why':why,'correct':True}]+[{'text':a,'why':b,'correct':False} for a,b in candidates[:4]]
        assert len(opts)==5
        rng.shuffle(opts); correct=next(i for i,o in enumerate(opts) if o['correct'])
        for o in opts:del o['correct']
        image=fig[0] if fig else None
        if image:
            if image.startswith('figure-eye-'): image='figure-eye-'+image.rsplit('-',1)[1].zfill(2)
            image+='.jpg'
        questions.append(dict(id=f'Q{len(questions)+1:03}',deck=deck,topic=topic,pages=pages,page=pages[0],ref=f'slide-{deck}-{pages[0]}',stem=stem,options=opts,answer=correct,image=image))

pool('eyeDx','''Thyroid ophthalmopathy~This causes proptosis from enlarged extraocular muscles and increased orbital connective tissue; it does not primarily cloud the lens or detach the retina.
Cataract~A cataract is a lens opacity causing painless gradual blur, glare, and impaired night vision; it does not produce retinal neovascularization or disc swelling.
Primary open-angle glaucoma~This produces chronic optic neuropathy with disc cupping and peripheral field loss despite an open drainage angle; it differs from acute painful angle closure.
Primary angle-closure glaucoma~An obstructed anterior chamber angle causes an acutely painful red eye with markedly increased pressure; it is not a painless retinal degeneration.
Anterior uveitis~Inflammation causes photophobia, pain, and anterior chamber cells and flare; lens opacity and retinal deposits have different locations.
Dry age-related macular degeneration~Drusen and RPE atrophy cause gradual central visual impairment without the leaking neovascular membrane of wet AMD.
Wet age-related macular degeneration~Choroidal neovascularization causes hemorrhage, exudation, and rapid central distortion; it does not cause primary lens opacity.
Uveal melanoma~This is a melanocytic uveal malignancy, commonly choroidal and pigmented, with a propensity for liver metastasis; it is distinct from childhood retinoblastoma.
Posterior vitreous detachment~Separation of posterior vitreous cortex from retina causes new floaters or flashes and may cause a retinal tear; it is not itself neurosensory retinal separation from RPE.
Retinal detachment~Neurosensory retina separates from RPE, often causing flashes, floaters, and a curtain-like field defect; this requires urgent retinal assessment.
Nonproliferative diabetic retinopathy~Microaneurysms, hemorrhages, and ischemic spots occur without new retinal vessels; neovascularization defines proliferative disease.
Proliferative diabetic retinopathy~Retinal ischemia drives VEGF-mediated new vessels that bleed and cause traction; microaneurysms alone do not establish this stage.
Hypertensive retinopathy~Arteriolar sclerosis, copper or silver wiring, and AV nicking reflect chronic blood pressure injury; these are not lens changes.
Papilledema~Raised intracranial pressure causes optic disc swelling with blurred margins; it should not be confused with the excavated optic cup of glaucoma.
Retinoblastoma~A young child with leukocoria and a calcified retinal mass suggests this RB1-associated malignancy; adult pigmented choroidal tumors suggest melanoma.
Central retinal artery occlusion~Acute profound painless monocular loss with retinal whitening and a cherry-red fovea indicates arterial ischemia, not gradual macular degeneration.
Keratitis~Corneal inflammation or ulceration can produce pain, photophobia, and reduced vision; it does not account for posterior retinal or optic disc pathology.
Scleritis~Deep painful scleral inflammation differs anatomically from uveitis, lens opacity, and retinal disease.''')
pools['eyeDx']['Orbital lymphoma']='An orbital lymphoid tumor can cause progressive proptosis; biopsy establishes the nature of the mass rather than thyroid tests alone.'
block('eye','Ocular diagnosis','eyeDx','''2,4,59|A 32-year-old woman has weight loss, tremor, and bilateral forward displacement of the eyes. Which diagnosis explains the ocular photograph?|Thyroid ophthalmopathy|Graves-associated orbital fibroblast activation increases extracellular matrix and orbital fat, with extraocular muscle inflammation and fibrosis. The resulting orbital expansion produces proptosis.|figure-eye-4
3|A patient develops progressive unilateral proptosis without thyrotoxicosis. Imaging shows an orbital mass, and biopsy reveals sheets of malignant lymphoid cells. Which diagnosis explains the proptosis?|Orbital lymphoma|An orbital lymphoma expands the orbital contents and displaces the globe. Proptosis is a sign rather than a specific diagnosis; glioma, meningioma, sarcoidosis, pleomorphic adenoma, and adenoid cystic carcinoma are additional nonthyroid causes.
5,6,60|A 72-year-old reports gradual painless blur, glare from headlights, and faded colors. Examination shows the pictured opacity. What is the diagnosis?|Cataract|The opacity is in the lens. Cataracts impair transmission of light and commonly cause glare, poor night vision, and gradually reduced acuity.|figure-eye-5
8|An older adult briefly finds it easier to read without reading glasses, followed by worsening distance vision and yellow-brown lens discoloration. What disorder explains this myopic shift?|Cataract|Age-related nuclear sclerosis can initially increase lens refractive power, producing a myopic shift. Accumulating yellow-brown pigment also alters color perception.
9,12|A 66-year-old has years of painless peripheral field loss. Gonioscopy shows an open angle and examination shows an enlarged optic cup. Which diagnosis is most likely?|Primary open-angle glaucoma|Open-angle glaucoma is often found on routine examination because its progression is slow. Chronic optic neuropathy causes cupping and eventual tunnel vision.|figure-eye-16
9,13|A hyperopic woman develops sudden eye pain, headache, nausea, halos, and severe blurred vision. Her cornea is hazy and the anterior chamber is shallow. Which diagnosis requires immediate treatment?|Primary angle-closure glaucoma|A narrow angle predisposes to pupillary block and anterior bowing of the iris. Abrupt aqueous outflow obstruction can rapidly damage vision.
20,22,63|A red painful eye is sensitive to light. Slit-lamp examination demonstrates the pictured anterior chamber finding. What is the best diagnosis?|Anterior uveitis|Anterior chamber inflammatory cells and protein flare support anterior uveitis or iritis. Trauma, infection, autoimmune disease, and idiopathic inflammation can all cause this appearance.|figure-eye-22
23,24,64|An 81-year-old needs increasing light to read. The fundus shows yellow-white macular deposits and geographic RPE atrophy without hemorrhage. What is the diagnosis?|Dry age-related macular degeneration|Drusen and geographic atrophy characterize dry AMD. Central detailed color vision is affected because the macula is damaged.|figure-eye-24
25,26,65|An older patient says straight lines suddenly appear bent. The pictured macular lesion contains exudate and blood. What is the diagnosis?|Wet age-related macular degeneration|A VEGF-driven choroidal neovascular membrane leaks fluid and blood, producing metamorphopsia and rapid central visual loss.|figure-eye-26
28,30,66|A 58-year-old has incidental discovery of a dark choroidal mass. Which diagnosis best fits the gross lesion?|Uveal melanoma|Uveal melanoma arises from melanocytes, most commonly in the choroid. It may initially be asymptomatic and can secondarily detach the overlying retina.|figure-eye-30
34,35,67|A 70-year-old develops new floaters and flashes. The posterior hyaloid has separated, but the retina remains attached to the pigment epithelium. What is the diagnosis?|Posterior vitreous detachment|Age-related vitreous changes can separate the posterior vitreous cortex from the retina. Retinal tears and detachment are important complications, but the defining separation here is vitreoretinal.|figure-eye-34
36,39,68|A 61-year-old sees flashes followed by a dark curtain across one eye. Fundus examination shows the pictured billowing folds. Which diagnosis is most likely?|Retinal detachment|Billowing elevated retina and a curtain-like field defect indicate retinal detachment. Prompt repair reduces the risk of irreversible photoreceptor loss.|figure-eye-39
40,41|A person with longstanding diabetes has tiny red retinal dots, dot-blot hemorrhages, and exudates. No new vessels are present. Which stage is this?|Nonproliferative diabetic retinopathy|Nonproliferative disease includes microaneurysms, hemorrhage, exudates, venous changes, and ischemic cotton-wool spots. Absence of neovascularization distinguishes it from proliferative disease.
43,45,69|A diabetic patient's fundus shows delicate tangled new vessels away from the optic disc. Which diagnosis is established by this finding?|Proliferative diabetic retinopathy|Neovascularization elsewhere or at the disc defines proliferative retinopathy. Fragile new vessels can bleed into vitreous and cause tractional retinal detachment.|figure-eye-45
46,47,71,72|Which diagnosis explains the arteriolar appearance and compressed vein at a crossing in this photograph?|Hypertensive retinopathy|Arteriolar wall sclerosis causes increased light reflex, copper or silver wiring, and AV nicking where an arteriole compresses an underlying venule.|figure-eye-47
51,52,73|A 25-year-old has headache, pulsatile tinnitus, and transient visual obscurations. Both optic discs are swollen with indistinct margins. What is the name of this finding when caused by raised intracranial pressure?|Papilledema|Papilledema specifically means optic disc edema from elevated intracranial pressure. It requires urgent evaluation of the cause; not every swollen disc is papilledema.|figure-eye-51
53,54,74|A 2-year-old has strabismus and a white pupil in flash photographs. Examination shows the retinal mass pictured. Which diagnosis is most likely?|Retinoblastoma|Leukocoria, strabismus, and a white retinal tumor in a child under five strongly suggest retinoblastoma. Early disease confined to the eye has a high cure rate.|figure-eye-53
57|A 76-year-old suddenly loses nearly all vision in one eye. The retina is pale except for a cherry-red fovea. Which diagnosis best fits this acute presentation?|Central retinal artery occlusion|Acute arterial occlusion whitens ischemic inner retina while the thin fovea retains its underlying choroidal red appearance. This is an emergency; storage diseases cause a similar sign in a different clinical setting.|figure-eye-57
20|A patient with systemic autoimmune disease has a painful corneal ulcer and photophobia. Which ocular inflammatory term identifies the affected structure?|Keratitis|Keratitis is inflammation of the cornea; corneal ulceration may compromise transparency and vision. The uvea and sclera are separate tissues.
20|A patient has severe deep ocular pain with thickening and inflammation of the white outer wall of the eye. Which diagnosis identifies the involved layer?|Scleritis|The sclera is the fibrous outer coat. Its inflammation produces scleritis, rather than inflammation of the uvea or corneal surface.''')

pool('eyeMechanism','''Lens crystallin aggregation~Protein aggregation and oxidative injury cloud the lens; this mechanism explains cataracts rather than retinal or orbital disease.
Orbital fibroblast activation with glycosaminoglycan deposition~TSH-receptor autoimmunity promotes matrix accumulation, fat expansion, and muscle changes in thyroid eye disease.
Reduced trabecular aqueous outflow with an open angle~Increased resistance to aqueous drainage is the usual mechanism of primary open-angle glaucoma.
Pupillary block with forward bowing of the iris~Iris bombe closes a narrow anterior chamber angle and abruptly obstructs aqueous drainage.
VEGF-driven neovascularization~Ischemia or macular degeneration can promote abnormal vessels that leak and bleed; VEGF is not the mechanism of a lens opacity.
Retinal arteriolar wall sclerosis~Hypertensive vascular injury thickens walls, narrows lumens, and causes wiring and AV nicking.
Retinal capillary pericyte loss~Diabetic microangiopathy damages retinal capillaries and promotes microaneurysms and leakage.
Raised intracranial pressure impairing axoplasmic flow~This causes papilledema and disc swelling rather than glaucomatous excavation.
Neurosensory retinal separation from RPE~Subretinal fluid or traction separates the neural retina from its support layer in retinal detachment.
Inflammatory breakdown of the blood-aqueous barrier~Leukocytes and protein enter the anterior chamber in uveitis, producing cells and flare.
Ganglion cell and retinal nerve fiber loss~Glaucomatous optic neuropathy destroys ganglion cells and their axons, producing optic disc cupping.
Drusen accumulation beneath RPE~Deposits between RPE and Bruch membrane are characteristic of dry AMD, without necessarily implying neovascularization.''')
block('eye','Ocular mechanisms and morphology','eyeMechanism','''2,3,4,59|Which mechanism enlarges the extraocular muscles and orbital tissues in Graves ophthalmopathy?|Orbital fibroblast activation with glycosaminoglycan deposition|Autoimmune signaling involving TSH receptors and inflammatory cytokines activates orbital fibroblasts. Hydrophilic extracellular matrix, fat expansion, and muscle fibrosis increase orbital volume.|figure-eye-2
5,7|A lens progresses from slight clouding to dense opacity with protein clumping, oxidative injury, and calcium deposits. Which process is central to this progression?|Lens crystallin aggregation|Accumulating abnormal lens proteins scatter light. Progression produces greater glare, reading difficulty, loss of color quality, and eventual substantial visual impairment.
11,12,61|A patient has high intraocular pressure despite a visibly open anterior chamber angle. Which mechanism is most likely?|Reduced trabecular aqueous outflow with an open angle|Aqueous normally flows from the ciliary processes through the pupil to the anterior chamber and then out through trabecular meshwork and Schlemm canal. Outflow resistance, not vitreous circulation, explains typical open-angle disease.|figure-eye-11
13|A narrow-angle eye develops iris bombe. Which mechanism directly closes the drainage angle?|Pupillary block with forward bowing of the iris|A pressure gradient across the iris bows it anteriorly and brings peripheral iris against trabecular meshwork. Hyperopic eyes often have a crowded anterior segment.|figure-eye-13
14,19|A patient with diabetic retinal ischemia develops a vascular membrane on the iris that contracts across the anterior chamber angle. What drives the new vessel formation?|VEGF-driven neovascularization|Retinal ischemia increases VEGF, causing rubeosis iridis and fibrovascular membranes. Contraction can obstruct the angle and produce secondary neovascular glaucoma.|figure-eye-14
15,16,17,18,62|Which cellular loss explains enlarged optic cups and the thinner retinal layer in the glaucoma histology?|Ganglion cell and retinal nerve fiber loss|Glaucoma damages retinal ganglion cells and their axons. Neural rim loss produces disc cupping; optic nerve atrophy is not the same as swollen discs from intracranial pressure.|figure-eye-17
22,63|What process allows slit-lamp examination to reveal white cells and light scattering in an inflamed anterior chamber?|Inflammatory breakdown of the blood-aqueous barrier|Cells are inflammatory leukocytes; flare is principally light scattering by protein in aqueous humor, not a lens deposit or retinal hemorrhage.|figure-eye-22
24,64|The pale macular deposits marked by the arrowhead are most directly explained by which process?|Drusen accumulation beneath RPE|Drusen collect between RPE and Bruch membrane. The darker arrow-marked areas represent RPE pigment alteration; geographic atrophy represents loss of RPE and associated outer retinal tissue.|figure-eye-24
25,26,65|A capillary-rich membrane has formed between Bruch membrane and RPE and leaks blood into the macular region. Which pathway is the therapeutic target?|VEGF-driven neovascularization|Wet AMD involves abnormal choroidal vessels crossing Bruch membrane. Inhibiting VEGF reduces leakage and neovascular activity; existing scar-related loss may persist.|figure-eye-25
37,39,68|In the common tear-associated form of retinal detachment, what structural event causes vision loss?|Neurosensory retinal separation from RPE|A retinal break permits liquefied vitreous into the subretinal space. Detached photoreceptors lose metabolic support from RPE and choroid and may degenerate.|figure-eye-37
41|Which microvascular alteration contributes to the earliest red dots in diabetic retinopathy?|Retinal capillary pericyte loss|Pericyte loss and basement membrane thickening weaken retinal capillaries, favoring microaneurysms. These are retinal capillary lesions, not the choroidal capillary dilations mistakenly described in the slide.
43,44|Retinal ischemia is followed by vessels growing through the internal limiting membrane. Which mechanism explains this change?|VEGF-driven neovascularization|VEGF stimulates fragile new vessels on the retina and optic disc. Vitreous traction can tear these vessels and produce vitreous hemorrhage.|figure-eye-43
46,47,49,71|Which process produces the copper-wire and silver-wire appearance of retinal arterioles?|Retinal arteriolar wall sclerosis|Chronic hypertension thickens and scleroses arteriolar walls, obscuring the blood column and increasing the light reflex. AV crossing compression produces nicking.|figure-eye-46
51,73|A brain mass is associated with bilateral swollen optic discs. Which mechanism links the intracranial lesion to the fundus finding?|Raised intracranial pressure impairing axoplasmic flow|Pressure transmitted along the optic nerve sheath impairs axoplasmic transport at the disc. The resultant edema obscures disc margins.|figure-eye-51''')

# Closely related, custom five-choice items use explicit option-specific rationales.
def custom(deck,topic,refs,stem,options,fig=None):
    entries=[s.split('~',1) for s in options]
    pname='custom'+str(len(questions)); pools[pname]=dict(entries[1:])
    block(deck,topic,pname,refs+'|'+stem+'|'+entries[0][0]+'|'+entries[0][1]+('|' + fig if fig else ''))

custom('eye','Cataract risks and treatment','5,60','Which exposure increases cataract risk?',[
'Long-term systemic corticosteroids~Corticosteroids are associated particularly with posterior subcapsular cataracts. Other lecture risks include diabetes, galactosemia, Wilson disease, atopic dermatitis, radiation, and trauma.',
'Topical artificial tears~Lubricants relieve dryness and are not the listed cataract-producing exposure.',
'Brief exposure to a dark room~Darkness affects pupil size but does not cause lens protein opacification.',
'Reading without corrective lenses~Refractive strain does not cause cataract formation.',
'A low-sodium diet~Dietary sodium restriction is not the cataract risk described here.'])
custom('eye','Cataract risks and treatment','8','A patient on chronic prednisone develops a posterior subcapsular cataract. Which morphologic process is characteristic?',[
'Lens epithelial migration toward the posterior pole~Posterior subcapsular cataracts involve abnormal epithelial cells at the posterior lens. Steroids, diabetes, and radiation are associated risks.',
'Retinal pigment epithelial atrophy~RPE loss is important in dry AMD, not a posterior lens opacity.',
'Ganglion cell axon loss~This produces glaucomatous optic neuropathy, not a cataract.',
'New vessels crossing Bruch membrane~This occurs in neovascular AMD.',
'Orbital muscle fibrosis~This is a component of thyroid ophthalmopathy.'])
custom('eye','Cataract risks and treatment','5,60','A dense cataract prevents a patient from reading or driving despite correction of refractive error. Which intervention directly treats the problem?',[
'Remove the opaque lens contents and place an intraocular lens~Cataract surgery removes the opacified lens material and substitutes an artificial lens to restore focusing.',
'Intravitreal anti-VEGF injections~These target retinal or choroidal neovascular disease, not lens opacity.',
'Retinal laser retinopexy~This treats retinal breaks rather than a cataract.',
'Laser peripheral iridotomy~This relieves pupillary block in angle closure, not clouded lens proteins.',
'Plasma exchange~This is used for selected immune neurologic diseases, not age-related cataract.'],'figure-eye-60')
custom('eye','Aqueous anatomy','11,61','Where is aqueous humor produced?',[
'Nonpigmented ciliary epithelium~The ciliary processes secrete aqueous into the posterior chamber between iris and lens. It passes through the pupil to the anterior chamber.',
'Retinal pigment epithelium~RPE supports photoreceptors and the outer blood-retinal barrier; it does not secrete the circulating aqueous.',
'Lens nucleus~The lens refracts light but does not produce aqueous.',
'Trabecular meshwork~This is an outflow structure at the anterior chamber angle.',
'Schlemm canal~This receives drained aqueous from trabecular meshwork, rather than producing it.'],'figure-eye-61')
custom('eye','Aqueous anatomy','11,61','Which sequence correctly describes conventional aqueous humor circulation?',[
'Posterior chamber, pupil, anterior chamber, trabecular meshwork, Schlemm canal~Aqueous is produced at the ciliary processes and follows this conventional route. Vitreous remains in the vitreous cavity and is a different material.',
'Vitreous cavity, retina, pupil, Schlemm canal~Aqueous does not originate in the vitreous cavity or flow through retinal tissue.',
'Anterior chamber, lens nucleus, choroid, pupil~The lens nucleus is not an aqueous drainage channel.',
'Schlemm canal, trabecular meshwork, posterior chamber, retina~This reverses conventional drainage and includes an incorrect retinal destination.',
'Lacrimal gland, pupil, anterior chamber, choroid~Lacrimal tears coat the ocular surface; they do not supply intraocular aqueous.'])
custom('eye','Glaucoma assessment','9,10','Which test directly measures intraocular pressure?',[
'Tonometry~Tonometry estimates IOP. Glaucoma assessment also requires optic nerve and visual field evaluation because pressure alone does not define the disease.',
'Optical coherence tomography alone~OCT assesses retinal and optic nerve structure but does not directly measure IOP.',
'Visual evoked potentials~VEP tests visual pathway conduction, not ocular pressure.',
'Fluorescein angiography~This images retinal vascular leakage and perfusion, not pressure.',
'Gonioscopy alone~Gonioscopy assesses the chamber angle but does not measure IOP.'])
custom('eye','Glaucoma assessment','9,10,16','A patient has glaucomatous field defects and disc cupping despite normal office pressure measurements. Which statement is most accurate?',[
'Normal measured IOP does not exclude glaucoma~Normal-tension glaucoma exists; optic nerve susceptibility and vascular factors may contribute. Glaucoma is optic neuropathy, not simply a pressure value.',
'Glaucoma requires elevated IOP on every visit~Pressure can vary, and normal-tension glaucoma invalidates this requirement.',
'Disc cupping proves intracranial hypertension~Intracranial hypertension causes disc edema, not classic glaucomatous rim loss.',
'Loss of peripheral vision is always cataract~Cataracts primarily impair acuity and contrast through lens opacity.',
'Pressure lowering regenerates destroyed ganglion cells~Treatment reduces further damage but does not restore lost ganglion cells.'])
custom('eye','Glaucoma assessment','9','What is the realistic goal of treatment for established glaucomatous visual loss?',[
'Reduce further optic nerve damage by lowering IOP~Medications, laser, and surgery can slow or halt progression; existing optic nerve loss is generally irreversible.',
'Regenerate the damaged optic nerve by raising IOP~Raising pressure worsens the risk of injury.',
'Reverse all field loss by replacing the lens~Lens replacement treats cataracts and does not reverse glaucomatous axon loss.',
'Observe acute angle closure until pain resolves~Angle closure risks rapid permanent damage and requires immediate treatment.',
'Treat every case as retinal detachment~Retinal detachment has a different anatomic mechanism and surgical target.'])
custom('eye','Glaucoma secondary causes','12,19','After eye trauma, pigment and cellular debris obstruct trabecular outflow while the angle remains open. What is the best classification?',[
'Secondary open-angle glaucoma~Obstruction by debris after trauma or tumors can impair aqueous outflow without closing the angle.',
'Primary open-angle glaucoma~A clear secondary cause makes primary disease the less precise label.',
'Primary angle-closure glaucoma~The angle is open, and the mechanism is debris obstruction rather than iris bombe.',
'Normal aqueous circulation~Outflow obstruction and elevated pressure are abnormal.',
'Posterior vitreous detachment~Vitreoretinal separation does not explain trabecular obstruction.'])
custom('eye','Glaucoma secondary causes','19','Diabetic ciliary body histology shows thickened basement membranes. Which local effect is described in the lecture?',[
'Possible reduction in aqueous production~Diabetic ciliary microvascular and epithelial changes can decrease aqueous production. This differs from ischemia-driven iris neovascularization, which obstructs outflow.',
'Obligate overproduction of vitreous~The ciliary processes produce aqueous; vitreous is not continuously secreted through this pathway.',
'Conversion of the lens into a neovascular membrane~The lens is not the site of rubeosis iridis.',
'Immediate regeneration of optic axons~Basement membrane thickening does not regenerate neurons.',
'Formation of Flexner-Wintersteiner rosettes~These are retinal tumor structures, not diabetic ciliary changes.'],'figure-eye-19')
custom('eye','Uveal inflammation','21','Which three structures constitute the uvea?',[
'Iris, ciliary body, and choroid~These form the vascular middle coat. Uveitis can be anterior, intermediate, posterior, or diffuse depending on the site.',
'Cornea, sclera, and conjunctiva~These are surface or outer-coat structures, not the uveal triad.',
'Lens, vitreous, and retina~These optical and neural structures are not the uvea.',
'Optic nerve, macula, and fovea~The optic nerve and retinal regions are not the vascular middle coat.',
'Trabecular meshwork, Schlemm canal, and lacrimal gland~These drainage and tear structures do not define the uvea.'],'figure-eye-21')
custom('eye','Uveal inflammation','21','After penetrating trauma to one eye, a patient develops bilateral granulomatous uveitis. Which diagnosis is most likely?',[
'Sympathetic ophthalmia~Exposure of sequestered ocular antigens after injury can trigger bilateral autoimmune uveal inflammation. This is the condition historically associated with Louis Braille in the lecture.',
'Isolated traumatic cataract~A lens injury does not explain bilateral granulomatous uveitis.',
'Primary open-angle glaucoma~This is optic neuropathy, not post-traumatic bilateral uveal inflammation.',
'Dry AMD~An age-related macular disorder is inconsistent with the trauma-triggered inflammatory pattern.',
'Retinoblastoma~This childhood retinal malignancy does not cause this immune reaction.'])
custom('eye','Uveal inflammation','21,22','A child with juvenile idiopathic arthritis is screened for ocular complications. Which complication is particularly relevant?',[
'Anterior uveitis~JIA is associated with anterior uveitis, which may be clinically quiet in children and requires screening. Sarcoidosis is another systemic cause of granulomatous uveitis.',
'Uveal melanoma in every case~JIA does not make melanoma an inevitable ocular complication.',
'Bilateral RB1 loss~JIA does not cause the retinoblastoma two-hit mechanism.',
'Age-related nuclear sclerosis~The age and autoimmune association favor uveitis, not age-related cataract.',
'Central retinal artery occlusion as the usual complication~This is not the characteristic screening target in JIA.'])
custom('eye','Macular degeneration','23,24,27,64','Which visual function is especially impaired by damage to the macula?',[
'Sharp central detailed color vision~The macula supports reading, face recognition, and detailed central vision. AMD can be severe while peripheral vision remains relatively preserved.',
'Only the pupillary light reflex~The macula is not exclusively a pupillary reflex center.',
'Only peripheral motion detection~Peripheral field loss is more characteristic of glaucoma than isolated macular disease.',
'Only accommodation~Accommodation depends on lens and ciliary muscle mechanics.',
'Only corneal sensation~Corneal sensation is mediated by trigeminal afferents.'])
custom('eye','Macular degeneration','27,64','A patient with intermediate dry AMD asks whether progression is always slow and whether a complete cure exists. Which response is most accurate?',[
'Dry disease can become wet; selected patients benefit from risk reduction and supplements~Dry AMD usually progresses gradually but may convert to rapidly progressive neovascular disease. AREDS-type supplements benefit selected risk categories, not everyone, and do not restore lost vision.',
'Dry AMD inevitably causes total blindness within one week~This is inconsistent with the usual gradual course.',
'Anti-VEGF cures all dry AMD~Anti-VEGF targets neovascular disease and is not a universal dry-AMD cure.',
'Supplements regenerate destroyed photoreceptors~Supplements reduce progression risk in selected patients rather than regenerating dead cells.',
'No monitoring is needed once drusen are found~Conversion or progression warrants follow-up and symptom monitoring.'])
custom('eye','Macular degeneration','25,26,27,65','Which treatment directly targets the abnormal vessels in wet AMD?',[
'Intravitreal VEGF inhibition~Anti-VEGF treatment reduces neovascular leakage. Laser or photodynamic approaches have selected roles; early detection matters because scarring can limit recovery.',
'Intraocular lens implantation alone~Lens replacement treats cataract, not choroidal new vessels.',
'Laser peripheral iridotomy~This treats pupillary-block angle closure.',
'IV immunoglobulin~This is used in several immune neuropathies, not routine wet AMD.',
'Orbital decompression~This is an option for severe thyroid orbitopathy, not macular neovascularization.'])
custom('eye','Uveal melanoma','29,30,66','A patient treated for uveal melanoma develops weight loss years later. Which organ is the characteristic metastatic site?',[
'Liver~Uveal melanoma strongly favors hematogenous liver metastasis. Long-term surveillance remains important despite apparently successful local treatment; the lecture cites roughly 80% five-year survival as a cohort estimate.',
'Thyroid exclusively~Thyroid involvement is not the characteristic metastatic distribution.',
'Regional lymph nodes exclusively~The eye has limited conventional lymphatic drainage, and hematogenous spread is central.',
'Lens~The avascular lens is not the characteristic distant metastatic site.',
'Pituitary exclusively~Pituitary-only dissemination is not the typical pattern.'])
custom('eye','Uveal melanoma','31,66','Which molecular pattern is most characteristic of uveal rather than common cutaneous melanoma?',[
'GNAQ or GNA11 pathway mutation rather than typical BRAF mutation~Activating G-protein pathway mutations are common in uveal melanoma. Conventional BRAF mutations typical of some skin melanomas are not its characteristic drivers.',
'BRAF V600E in nearly every case~This incorrectly transfers a common cutaneous pathway to uveal melanoma.',
'Biallelic RB1 loss as the defining driver~RB1 loss is central to retinoblastoma.',
'AQP4 IgG against melanocytes~AQP4 antibodies are associated with NMOSD, not melanoma oncogenesis.',
'PMP22 deletion~This causes hereditary neuropathy with liability to pressure palsies.'],'figure-eye-31')
custom('eye','Uveal melanoma','32','A choroidal melanoma becomes mushroom-shaped as it enlarges. Which barrier has it breached?',[
'Bruch membrane~Expansion through Bruch membrane permits a mushroom or collar-button configuration beneath the retina.',
'Descemet membrane~This is the posterior corneal basement membrane.',
'Anterior lens capsule~This surrounds the lens and is not the choroidal barrier.',
'Trabecular meshwork~This regulates aqueous drainage at the chamber angle.',
'Optic chiasm~This is an intracranial neural structure, not a retinal-choroidal membrane.'],'figure-eye-32')
custom('eye','Uveal melanoma','29,33','What cell pattern is visible in this uveal melanoma micrograph?',[
'Pleomorphic epithelioid melanocytes~The pictured cells are rounded epithelioid tumor cells with nuclear atypia and pleomorphism. Uveal melanomas may also contain spindle cells, mitoses, necrosis, and vascular mimicry.',
'Flexner-Wintersteiner rosettes~These are associated with retinoblastoma rather than the pictured epithelioid melanoma cells.',
'Lens epithelial pearls~Lens epithelial changes do not explain a malignant uveal tumor.',
'Normal retinal ganglion cells~These atypical pigmented tumor cells are not a normal ganglion cell layer.',
'Schwann cell onion bulbs~These indicate chronic peripheral demyelination, not uveal melanoma.'],'figure-eye-33')
custom('eye','Uveal melanoma','29','Which is an established local treatment approach for a large uveal melanoma unsuitable for eye-conserving therapy?',[
'Enucleation~Removing the eye is one option for selected large tumors. Other local approaches include plaque or proton radiotherapy; metastatic therapy is a separate decision.',
'Cataract extraction alone~Removing the lens does not treat a choroidal malignancy.',
'Artificial tears alone~Lubrication does not control malignant growth.',
'Routine laser iridotomy alone~Iridotomy addresses pupillary block, not melanoma.',
'Treat with oral glucose~Glucose administration has no antitumor role here.'])
custom('eye','Vitreoretinal disorders','34,35,67','What complication must be excluded when a patient develops acute symptomatic posterior vitreous detachment?',[
'Retinal tear or retinal detachment~Vitreous traction can tear retina as the posterior hyaloid separates. New flashes, numerous floaters, or a curtain warrant prompt dilated retinal evaluation; uncomplicated PVD is often observed.',
'Inevitable liver metastasis~This concerns uveal melanoma, not ordinary PVD.',
'Obligate bilateral retinoblastoma~PVD does not cause RB1-mediated retinal tumors.',
'Immediate lens regeneration~PVD neither removes nor regenerates the lens.',
'Graves hyperthyroidism in every patient~Age-related vitreous separation does not establish thyroid autoimmunity.'],'figure-eye-35')
custom('eye','Vitreoretinal disorders','37,38','A choroidal tumor causes protein-rich subretinal fluid without a retinal tear. What type of detachment is present?',[
'Exudative nonrhegmatogenous detachment~Fluid leakage from choroidal disease or severe hypertension can separate retina without a break. Nonrhegmatogenous detachment also includes tractional mechanisms; it is not synonymous with exudation alone.',
'Rhegmatogenous detachment~This requires a retinal break permitting fluid entry.',
'Isolated posterior vitreous detachment~This separates vitreous cortex from retina rather than retina from RPE.',
'Lens subluxation~Displacement of the lens does not create the stated subretinal fluid.',
'Primary open-angle glaucoma~This causes ganglion cell loss rather than exudative retinal separation.'],'figure-eye-38')
custom('eye','Vitreoretinal disorders','36,39','Which treatment principle is most appropriate for a new retinal detachment threatening the macula?',[
'Urgent retinal specialist evaluation for repair~Retinopexy, pneumatic retinopexy, scleral buckling, or vitrectomy may be used depending on detachment characteristics. Delay risks permanent photoreceptor loss.',
'Wait several months for spontaneous lens clearing~The lesion is retinal and time-sensitive.',
'Treat solely with artificial tears~Surface lubrication does not reattach retina.',
'Increase IOP to compress the retina without evaluation~Unsupervised pressure elevation can damage the eye and is not definitive management.',
'Treat as uncomplicated refractive error~A curtain and detached retina cannot be corrected with spectacles.'])
custom('eye','Diabetic and hypertensive retina','41,42,48,49,70','What histologic process produces cotton-wool spots?',[
'Ischemic injury of the retinal nerve fiber layer with interrupted axoplasmic transport~Cotton-wool spots are superficial retinal microinfarcts with axoplasmic debris. Diabetes, hypertension, and lupus can produce them; they are not simply pooled exudate or hemorrhage.',
'Extracellular lipid deposits in the outer plexiform layer~These are hard exudates rather than fluffy superficial cotton-wool spots.',
'Drusen between RPE and Bruch membrane~These are macular deposits associated with AMD.',
'Malignant melanocytes in choroid~These constitute uveal melanoma.',
'Protein aggregates in the lens nucleus~These cause cataract.'],'figure-eye-42')
custom('eye','Diabetic and hypertensive retina','41','Which test can demonstrate retinal capillary leakage and nonperfusion in diabetic retinopathy?',[
'Fluorescein angiography~Intravenous fluorescein permits retinal vascular imaging to identify leakage, microaneurysms, and nonperfusion.',
'Tonometry alone~This measures IOP rather than retinal vascular leakage.',
'Needle EMG~This measures muscle electrical activity, not retinal perfusion.',
'Thyroid uptake scan~This assesses thyroid function rather than retinal circulation.',
'Single-fiber EMG~This evaluates neuromuscular transmission.'])
custom('eye','Diabetic and hypertensive retina','43,44,45,69','Why can proliferative diabetic retinopathy abruptly obscure vision after vitreous traction?',[
'Fragile new vessels rupture and bleed into the vitreous~Neovascular vessels are prone to hemorrhage. Associated fibrovascular tissue may also contract and produce tractional retinal detachment.',
'A clear lens becomes a melanoma overnight~This is not the mechanism of abrupt diabetic vitreous hemorrhage.',
'Drusen instantly dissolve~Drusen are unrelated to fragile proliferative vessels.',
'The optic nerve develops normal new axons~Neovascular bleeding does not regenerate optic neurons.',
'Aqueous flows backward through the retina~Aqueous circulation does not follow this route.'],'figure-eye-44')
custom('eye','Diabetic and hypertensive retina','47,72','What is AV nicking?',[
'Compression of a retinal venule at a crossing by a sclerotic arteriole~Arteriolar sclerosis from hypertension narrows or obscures the underlying venous column at a shared crossing.',
'An aneurysm within the lens~The lens is avascular and not the site of AV crossings.',
'Detachment of the optic nerve from the chiasm~This is not AV nicking.',
'A white retinal tumor~That would suggest retinoblastoma in a child.',
'A neovascular iris membrane~This is rubeosis iridis rather than AV nicking.'],'figure-eye-47')
custom('eye','Papilledema and emergencies','50,51,52,73','A patient has BP 238/142 mm Hg, headache, visual change, and optic disc edema. Which management best addresses this hypertensive emergency?',[
'Monitored controlled BP reduction with an IV agent such as nicardipine or labetalol~Acute end-organ injury warrants emergency care and carefully controlled IV antihypertensive treatment. Chronic mild retinopathy alone is a different situation.',
'Rapidly normalize BP with an unmonitored oral dose at home~Uncontrolled abrupt reduction can impair organ perfusion and is unsafe in this setting.',
'Prescribe only reading glasses~This does not address hypertensive end-organ injury.',
'Schedule follow-up in six months~The acute symptoms and disc edema require urgent care.',
'Give sublingual immediate-release nifedipine to normalize BP abruptly~Uncontrolled rapid lowering can compromise organ perfusion and is not the monitored IV approach required here.'])
custom('eye','Papilledema and emergencies','52,73','A patient has papilledema and a focal neurologic deficit. Which next step is appropriate before considering lumbar puncture?',[
'Urgent neuroimaging to evaluate for a mass or obstructive process~Papilledema may reflect tumor, hydrocephalus, venous disease, or idiopathic intracranial hypertension. Imaging is necessary before LP when a mass effect is possible; acute ICP measures depend on the cause.',
'Immediate LP without evaluating mass effect~This can be dangerous when intracranial pressure gradients or mass effect are present.',
'Treat every cause with indefinite mannitol alone~Mannitol is a selected acute temporizing therapy, not universal definitive treatment for papilledema.',
'Diagnose glaucoma from disc swelling alone~Glaucoma classically causes cupping rather than papilledema.',
'Ignore because visual acuity may initially be preserved~Preserved central acuity does not make papilledema benign.'])
custom('eye','Retinoblastoma','55','What is the normal role of RB protein?',[
'Restraining E2F-mediated G1-to-S cell cycle progression~Hypophosphorylated RB binds E2F and limits S-phase gene transcription. Biallelic RB1 inactivation removes this brake.',
'Producing aqueous humor~This is a ciliary epithelial function, not RB protein function.',
'Serving as the AQP4 water channel~AQP4 is a different protein involved in NMOSD.',
'Activating VEGF receptors constitutively~RB is a tumor suppressor rather than a VEGF receptor.',
'Synthesizing peripheral myelin~Schwann cells produce peripheral myelin.'])
custom('eye','Retinoblastoma','55,74','An infant with a germline RB1 pathogenic variant develops bilateral retinal tumors. Why are multiple tumors likely?',[
'Only one additional somatic hit is needed in each susceptible retinal cell~A germline first hit makes independent second hits more likely. Predisposition is autosomal dominant at the family level, while tumor formation requires loss of both alleles; secondary malignancy risk is increased.',
'One normal RB1 allele is always enough to transform a cell~Loss of the second allele is generally required for the classic two-hit model.',
'The tumor must be infectious because both eyes are involved~Bilateral disease is characteristic of hereditary predisposition, not evidence of infection.',
'All unilateral tumors exclude a germline variant~Unilateral disease can still be heritable; laterality alone cannot exclude germline RB1 loss.',
'Germline predisposition protects against osteosarcoma~Heritable RB1 loss increases the risk of other cancers, including osteosarcoma.'])
custom('eye','Retinoblastoma','54','A retinoblastoma grows toward the vitreous. How is its growth pattern classified?',[
'Endophytic~Endophytic retinoblastoma projects into the vitreous; exophytic growth is toward the subretinal space. A large cream-colored tumor can occupy much of the globe.',
'Exophytic~In this ocular classification exophytic growth is into the subretinal space, not vitreous.',
'Perineural~The stem describes growth direction into vitreous, not along a nerve.',
'Intravascular~The mass is not described as confined to a blood vessel.',
'Nuclear sclerotic~This is a cataract descriptor rather than tumor growth pattern.'],'figure-eye-54')
custom('eye','Retinoblastoma','56','Which histologic finding supports retinoblastoma?',[
'Small round blue cells forming Flexner-Wintersteiner rosettes~Tumor cells surround a central lumen in photoreceptor-type rosettes. Dystrophic calcification and perivascular arrangements can also occur.',
'Pleomorphic pigmented epithelioid melanocytes~These suggest melanoma rather than retinoblastoma.',
'Lens crystallin aggregates~These indicate cataract.',
'Retinal arteriolar hyaline sclerosis alone~This reflects vascular injury rather than a retinal malignancy.',
'Peripheral nerve onion bulbs~These indicate repeated peripheral demyelination and remyelination.'],'figure-eye-56')
custom('eye','Cherry-red spot','57,75','An infant with developmental regression and exaggerated startle has a cherry-red macula. What accounts for the color contrast?',[
'Storage-laden surrounding retinal ganglion cells with relative foveal transparency~Ganglion cell storage whitens surrounding retina while the thin fovea reveals underlying choroidal color. Tay-Sachs and Niemann-Pick are lecture examples; acute CRAO creates a similar appearance through ischemia.',
'A pool of blood exclusively inside the lens~The lens is not the location of a cherry-red macular spot.',
'Increased foveal melanin synthesis in every case~The contrast is mainly from pale surrounding retina, not a universal increase in foveal pigment.',
'New vessels in the anterior chamber angle~Rubeosis is anatomically distinct from the macula.',
'A dystrophically calcified tumor~Calcified retinal masses suggest retinoblastoma rather than this storage pattern.'],'figure-eye-75')

pool('neuroDx','''Multiple sclerosis~MS causes CNS demyelinating lesions disseminated in space and time, commonly with persistent CSF-restricted oligoclonal bands; long central cord lesions or area postrema syndrome suggest alternatives.
AQP4-IgG neuromyelitis optica spectrum disorder~AQP4-NMOSD is an astrocytopathy associated with severe optic neuritis, longitudinally extensive myelitis, and area postrema syndrome; AQP4-IgG is a key biomarker.
MOG antibody-associated disease~MOGAD can cause bilateral anterior optic neuritis, ADEM-like encephalopathy, conus myelitis, or cortical encephalitis; high-quality serum MOG-IgG testing is important.
Acute disseminated encephalomyelitis~ADEM typically causes a monophasic multifocal demyelinating illness with encephalopathy, often after infection; repeated temporally separate attacks favor another disorder.
Guillain-Barre syndrome~GBS usually produces acute progressive areflexic weakness reaching nadir within four weeks, often with autonomic or respiratory involvement; chronic progression suggests CIDP.
Chronic inflammatory demyelinating polyradiculoneuropathy~CIDP typically causes progressive or relapsing proximal and distal weakness with sensory loss and areflexia beyond eight weeks; CNS findings are not expected.
Multifocal motor neuropathy~MMN produces asymmetric pure motor weakness in named nerve distributions, conduction block, and no upper motor neuron signs; sensory loss argues against it.
Amyotrophic lateral sclerosis~ALS causes combined upper and lower motor neuron degeneration without a primary sensory neuropathy; conduction block favors a treatable motor neuropathy.
Myasthenia gravis~MG causes fatigable ocular or bulbar weakness from postsynaptic NMJ autoimmunity; sensation and pupils are usually spared.
Lambert-Eaton myasthenic syndrome~LEMS causes proximal weakness, autonomic symptoms, reduced reflexes, and facilitation with exercise from presynaptic calcium-channel antibodies.
Sensory neuronopathy~Dorsal root ganglion disease causes non-length-dependent sensory loss, sensory ataxia, and pseudo-weakness improved by visual guidance; causes include Sjogren disease, cancer, and pyridoxine excess.
Hereditary neuropathy with liability to pressure palsies~PMP22 deletion predisposes to recurrent focal neuropathies at pressure sites and multifocal demyelinating findings.
Charcot-Marie-Tooth disease~Hereditary length-dependent neuropathy commonly produces early onset, high arches, hammer toes, distal weakness, and family history.
Neuralgic amyotrophy~Severe shoulder pain followed by patchy weakness can involve several nerves without fitting a single brachial plexus segment.
Autoimmune limbic encephalitis~Subacute memory, psychiatric, and seizure symptoms with supportive CNS inflammation suggest limbic encephalitis after exclusion of infectious and other causes.
Neurosarcoidosis~Granulomatous inflammation can affect meninges, cranial nerves, hypothalamus, and cord; hydrocephalus or meningeal enhancement is an MS red flag.
Hirayama disease~Young men may develop focal hand and forearm wasting that progresses for years and then plateaus, associated with flexion-related cervical cord changes.
Kennedy disease~X-linked spinal bulbar muscular atrophy causes slow bulbar and proximal weakness, facial or tongue fasciculations, and androgen-insensitivity signs such as gynecomastia.''')
block('dem','Demyelinating differential','neuroDx','''6,10,11,15,16,18|A 27-year-old woman had painful monocular visual loss that resolved. Ten months later she develops leg numbness and an internuclear ophthalmoplegia. MRI shows ovoid periventricular and juxtacortical lesions; some enhance and others do not. Which diagnosis best fits?|Multiple sclerosis|Typical CNS episodes separated in time with lesions in characteristic locations support MS once mimics are excluded. Simultaneous enhancing and nonenhancing lesions can establish dissemination in time.
10,11,19,34|A 43-year-old woman has severe optic neuritis and transverse myelitis spanning six vertebral segments. Serum cell-based testing is positive for AQP4-IgG. Which diagnosis is most likely?|AQP4-IgG neuromyelitis optica spectrum disorder|AQP4-IgG positivity with a compatible core clinical attack and exclusion of alternative diagnoses supports AQP4-NMOSD. Severe long cord lesions differ from typical short peripheral MS lesions.
11,12,20,34|A child develops bilateral optic neuritis after a respiratory illness. MRI shows long anterior optic nerve lesions with perineural enhancement. Serum high-titer MOG-IgG is positive. Which diagnosis is most likely?|MOG antibody-associated disease|Bilateral anterior long-segment optic nerve involvement, optic disc edema, and perineural enhancement are characteristic MOGAD clues in an appropriate clinical context.
11,20,34|A 7-year-old develops encephalopathy and multifocal neurologic deficits after a febrile illness. MRI shows large poorly demarcated white and gray matter lesions. This is the first episode. Which clinical syndrome is most likely?|Acute disseminated encephalomyelitis|Encephalopathy plus multifocal demyelination in a child supports ADEM. MOGAD can underlie this phenotype, so syndrome and antibody-defined disease are related but not interchangeable.
19,34|A woman has otherwise unexplained hiccups and vomiting lasting three days. MRI shows a dorsal medullary lesion at the floor of the fourth ventricle. Which diagnosis should be strongly considered?|AQP4-IgG neuromyelitis optica spectrum disorder|Area postrema syndrome is a core NMOSD manifestation. Persistent intractable vomiting or hiccups can precede optic neuritis or myelitis.
11,13,14,34|A young adult has myelitis involving the conus with persistent bladder dysfunction. Axial MRI shows gray-matter-predominant H-shaped signal. Serum AQP4-IgG is negative and MOG-IgG is strongly positive. Which diagnosis is favored?|MOG antibody-associated disease|Conus involvement, gray matter H-sign, and MOG-IgG support MOGAD. Motor recovery may be good while sphincter or sexual dysfunction persists.
11,15,16,34|A patient has recurrent optic neuritis with marked lesion resolution between attacks and few new asymptomatic MRI lesions. High-titer MOG-IgG persists. Which diagnosis fits best?|MOG antibody-associated disease|MOGAD often has striking postattack T2 lesion resolution and little silent lesion accumulation. MS more often accumulates new asymptomatic lesions and persistent T1 injury.
21,22,23,36|A presumed MS patient develops basal meningeal enhancement, hydrocephalus, and trigeminal neuropathy. Which alternative diagnosis is especially important?|Neurosarcoidosis|Meningoventricular inflammation, hydrocephalus, and cranial neuropathies are neurosarcoidosis clues. Typical MS does not usually cause prominent basal meningitis or obstructive hydrocephalus.
36|A 29-year-old develops psychiatric change, impaired recent memory, and new seizures over six weeks. CSF shows lymphocytic pleocytosis and MRI shows medial temporal inflammation. Infection and toxic causes are reasonably excluded. Which diagnosis is most likely?|Autoimmune limbic encephalitis|A subacute limbic syndrome with seizures and supportive inflammation fits autoimmune encephalitis. Acute fever and headache would increase concern for viral encephalitis.
49,58,59,61|Two weeks after diarrheal illness, a man develops symmetric ascending weakness and absent reflexes over five days. He has fluctuating BP and a declining vital capacity. Which diagnosis is most likely?|Guillain-Barre syndrome|An acute areflexic polyradiculoneuropathy after infection with dysautonomia and respiratory weakness is typical GBS. Careful respiratory monitoring and early treatment are essential.
49,62,65,66|A patient has progressive symmetric proximal and distal weakness, distal vibration loss, and absent reflexes for four months. NCS shows nonuniform conduction slowing and prolonged distal latencies. Which diagnosis fits?|Chronic inflammatory demyelinating polyradiculoneuropathy|Progression beyond eight weeks with acquired demyelinating electrodiagnostic findings favors CIDP. Bulbar, respiratory, and autonomic involvement are less prominent than in GBS.
48,49,65|A man has slowly progressive asymmetric hand weakness in several named nerve territories. Sensation is intact, there are no upper motor neuron signs, and motor conduction block is present outside entrapment sites. Which diagnosis is most likely?|Multifocal motor neuropathy|The pure motor, multifocal nerve pattern and conduction block favor MMN over ALS. This distinction matters because MMN can respond to immunoglobulin treatment.
48,49|A patient has progressive weakness, muscle wasting, fasciculations, brisk reflexes, and a Babinski sign with preserved sensation. Which diagnosis is most likely?|Amyotrophic lateral sclerosis|Combined upper and lower motor neuron signs without a sensory neuropathy suggest ALS. Named-nerve conduction block would instead suggest MMN.
48,55|A woman has ptosis and diplopia that worsen late in the day, followed by chewing fatigue. Sensation, pupils, and reflexes are normal. Which disorder is most likely?|Myasthenia gravis|Fatigable ocular and bulbar weakness with preserved sensory function suggests postsynaptic NMJ disease. ACh-receptor antibodies and thymic pathology are common associations.
48,55|A smoker has proximal leg weakness, dry mouth, and reduced reflexes that improve briefly after exertion. Which diagnosis is most likely?|Lambert-Eaton myasthenic syndrome|LEMS causes impaired presynaptic acetylcholine release through VGCC autoimmunity. Autonomic symptoms, facilitation, and small-cell lung cancer association distinguish it from MG.
49|A patient with Sjogren disease cannot reliably place the limbs without looking, but apparent weakness improves with visual guidance. Sensory loss is patchy rather than stocking-glove. Which diagnosis fits?|Sensory neuronopathy|Dorsal root ganglion disease causes deafferentation and sensory ataxia. Visual compensation improves performance despite impaired proprioceptive input.
49|A young adult has recurrent foot drop after crossing the legs and transient hand weakness after leaning on the elbow. Several relatives have similar episodes. Which diagnosis is most likely?|Hereditary neuropathy with liability to pressure palsies|Recurrent pressure-induced focal palsies suggest HNPP, commonly due to PMP22 deletion. It is a hereditary multifocal demyelinating neuropathy.
49|A teenager has high arches, hammer toes, distal leg wasting, and a parent with the same gait. Which diagnosis is most likely?|Charcot-Marie-Tooth disease|Early onset, family history, pes cavus, and hammer toes are hereditary neuropathy red flags. This contrasts with a new acquired inflammatory neuropathy.
49|Severe shoulder pain is followed a week later by weakness involving scattered muscles supplied by different nerves. The pattern does not fit one root or a single plexus trunk. What is the most likely diagnosis?|Neuralgic amyotrophy|Neuralgic amyotrophy can produce patchy involvement of multiple nerves in one limb. The severe pain followed by weakness is a useful clue.
48,49|A 21-year-old man develops asymmetric hand and forearm wasting over three years, after which progression stops. Sensory examination is largely normal. Which disorder fits this pattern?|Hirayama disease|Monomelic amyotrophy often affects young men, progresses for years, then plateaus. Flexion cervical MRI can support the diagnosis.
48,49|A middle-aged man has slowly progressive proximal and bulbar weakness, tongue fasciculations, and gynecomastia. Which diagnosis best combines these findings?|Kennedy disease|Spinal bulbar muscular atrophy is an X-linked androgen receptor disorder. Androgen-insensitivity features help distinguish it from ALS.''')

pool('immuneTarget','''Oligodendrocytes and CNS myelin~Oligodendrocytes myelinate CNS axons and are central targets of MS-associated inflammatory demyelination.
Astrocytic aquaporin-4~AQP4 on astrocytic endfeet is the major antigen in AQP4-IgG-positive NMOSD; demyelination can follow astrocyte injury.
Myelin oligodendrocyte glycoprotein~MOG is exposed on the outer surface of CNS myelin and oligodendrocytes; MOG-IgG defines MOGAD in an appropriate syndrome.
Schwann cell peripheral myelin~Schwann cells myelinate peripheral axons; AIDP and typical CIDP affect peripheral nerve or root myelin.
Postsynaptic acetylcholine receptors~ACh-receptor antibodies impair neuromuscular transmission in many cases of MG, without primary demyelination.
Presynaptic voltage-gated calcium channels~VGCC antibodies reduce acetylcholine release in LEMS rather than directly attacking CNS myelin.
Peripheral motor axonal gangliosides~Axonal GBS variants such as AMAN involve nodal/axonal targets, often after Campylobacter molecular mimicry.
Intracellular neuronal antigens~Antibodies to intracellular antigens often mark a cytotoxic T-cell-mediated process and can signal paraneoplastic disease.
Neuronal surface membrane antigens~Antibodies can directly alter accessible surface receptors or recruit complement; such diseases may respond to antibody-directed therapy.
Paranodal adhesion proteins~Contactin-1, CASPR1, and neurofascin-related targets organize axon-glia junctions; autoimmune nodopathies are classified separately from conventional CIDP.''')
block('dem','Immune mechanisms','immuneTarget','''3|A neural autoantibody recognizes an antigen within the neuronal cytoplasm. Which target category most often indicates a predominantly cytotoxic T-cell process rather than direct antibody access to living neurons?|Intracellular neuronal antigens|Intracellular antigen antibodies often function as biomarkers of T-cell-mediated neuronal injury. A cancer search can be important in the appropriate phenotype.
3,5|An antibody binds an extracellular neuronal receptor and causes receptor internalization. Which target class is most consistent with a directly antibody-mediated mechanism?|Neuronal surface membrane antigens|Accessible surface antigens can be targeted by antibodies through receptor modulation, complement, or antibody-dependent injury. This differs from antibodies to inaccessible intracellular antigens.
4,6|Which myelin-forming cells are affected in multiple sclerosis?|Oligodendrocytes and CNS myelin|MS is inflammatory CNS demyelination involving T cells, B cells, macrophages, and microglia. Axonal degeneration can accompany myelin injury.
4,19,34|Which antigen is targeted in AQP4-IgG-positive NMOSD?|Astrocytic aquaporin-4|AQP4 antibodies target astrocytes, particularly endfeet at fluid interfaces. NMOSD is primarily an astrocytopathy, unlike a primary oligodendrocyte-directed process.
4,20,34|What is the antigen identified by MOG-IgG?|Myelin oligodendrocyte glycoprotein|MOG is a CNS myelin surface protein. MOGAD is distinct from AQP4-NMOSD despite overlapping optic nerve and spinal cord manifestations.
7,8,50|AIDP involves segmental demyelination in which supporting-cell system?|Schwann cell peripheral myelin|AIDP is a peripheral inflammatory demyelinating polyradiculoneuropathy. Schwann cells, rather than oligodendrocytes, produce the affected myelin.
7,61|An axonal GBS variant develops after Campylobacter diarrhea. Which target class is most characteristic?|Peripheral motor axonal gangliosides|Cross-reactive antiganglioside antibodies can injure nodes and axolemma in AMAN. AIDP instead primarily features demyelination.
9,57,67|A patient has an IVIg-refractory neuropathy with antibodies to contactin-1. Which target category is involved?|Paranodal adhesion proteins|Disruption of axon-glia adhesion at nodes or paranodes can cause conduction failure. These antibody-defined autoimmune nodopathies are considered distinct from typical CIDP.
55|A patient with MG and a thymoma has antibodies against which common target?|Postsynaptic acetylcholine receptors|Many MG cases are caused by AChR antibodies at the postsynaptic membrane. The result is a reduced safety margin for neuromuscular transmission.
55|A patient with small-cell lung cancer has LEMS. Which target is most characteristic?|Presynaptic voltage-gated calcium channels|P/Q-type VGCC antibodies decrease calcium-dependent acetylcholine release, producing weakness, autonomic symptoms, and facilitation.''')

custom('dem','Inflammatory injury','6','Activated microglia in MS release reactive oxygen species and disrupt glutamate handling. Which downstream effect is expected?',[
'Excitotoxic and oxidative neuronal injury~Cytokines, excess extracellular glutamate, reactive oxygen/nitrogen species, and mitochondrial injury can converge on neurodegeneration in addition to demyelination.',
'Selective production of normal lens proteins~Lens crystallins are unrelated to microglial CNS toxicity.',
'Increased saltatory conduction through destroyed myelin~Loss of myelin impairs rather than accelerates conduction.',
'A purely peripheral neuromuscular junction block~The mechanism described is CNS inflammation, not isolated NMJ dysfunction.',
'Elimination of all B cells by endogenous microglia~Microglia do not perform therapeutic anti-CD20 depletion.'])
custom('dem','Postinfectious immunity','7,61','Why can Campylobacter infection precede axonal GBS?',[
'Bacterial lipooligosaccharides resemble neural gangliosides~Molecular mimicry can produce cross-reactive antibodies, complement activation, and nodal or axonal injury. Complement and Fc pathways are treatment research targets.',
'The organism must invade every peripheral axon~Postinfectious autoimmunity does not require direct invasion of each nerve.',
'The organism mutates RB1 in retinal cells~This is unrelated to GBS pathogenesis.',
'Infection converts Schwann cells into astrocytes~Glial conversion is not the mechanism.',
'All infected patients develop GBS~GBS is a rare complication despite the association.'])
custom('dem','Neuroimmunology testing','5,19,20,34','Which testing strategy best supports suspected antibody-mediated optic neuritis and myelitis?',[
'Phenotype-directed serum cell-based AQP4-IgG and MOG-IgG assays~Cell-based assays preserve relevant antigen conformation. Testing should fit the clinical phenotype; low-titer MOG results in low-pretest-probability patients can mislead.',
'Screen everyone with broad low-specificity antibody panels~Indiscriminate testing raises the risk of incidental false positives.',
'Use CSF AQP4 testing alone as the routine first choice~Serum cell-based AQP4 testing is generally preferred.',
'Diagnose MOGAD from any isolated low-titer result~Low titers require careful clinical and assay interpretation.',
'Require both AQP4 and MOG antibodies in every case~Double positivity is very uncommon and is not a diagnostic requirement.'])
custom('dem','Demyelinating disease course','10','Which disease course best matches primary progressive MS?',[
'Gradual disability progression from onset without an initial relapsing-remitting phase~PPMS begins with progression. RRMS has attacks with recovery, and SPMS is later progression after a relapsing phase.',
'Discrete attacks with complete recovery and no progression by definition~This resembles a relapsing course, not PPMS.',
'Progression only after decades of relapsing-remitting disease~This describes secondary progressive disease.',
'One postinfectious event with permanent recovery~This is a monophasic course.',
'Disability only at the instant of an attack in every patient~Progression independent of attacks is possible in MS.'])
custom('dem','Demyelinating disease course','10,34','Which statement best distinguishes typical disability accumulation in AQP4-NMOSD from progressive MS?',[
'AQP4-NMOSD disability is usually attack-related with incomplete recovery~Severe attacks and residual deficits drive most NMOSD disability; a steadily progressive course without attacks is a red flag for another diagnosis.',
'AQP4-NMOSD invariably progresses daily without attacks~This is not its usual disease course.',
'MS never progresses independently of relapses~PIRA and progressive MS contradict this statement.',
'MOGAD is always continuously progressive~MOGAD is generally monophasic or relapsing rather than steadily progressive.',
'All three disorders have identical recovery and MRI behavior~Attack severity, recovery, and silent lesion accumulation differ.'])

pool('MRIpattern','''Posterior optic nerve and chiasmal involvement~Long posterior optic nerve lesions extending to the chiasm are particularly suggestive of AQP4-NMOSD.
Anterior long optic nerve lesions with perineural enhancement~This is a characteristic MOGAD optic neuritis pattern, often bilateral with disc swelling.
Short unilateral intraorbital optic nerve lesion~This is a typical MS optic neuritis pattern; imaging distributions overlap and require clinical interpretation.
Long central spinal cord lesion spanning at least three vertebral segments~Longitudinally extensive transverse myelitis favors NMOSD or MOGAD over typical MS.
Conus gray-matter H-sign lesion~MOGAD may preferentially affect central gray matter and the conus; residual sphincter dysfunction can remain.
Short peripheral spinal cord lesions~MS cord lesions are often short and peripheral rather than centrally extensive.
Ovoid periventricular and juxtacortical lesions~These are characteristic MS locations, especially when oriented around veins and supported by appropriate clinical findings.
Area postrema dorsal medullary lesion~This location explains intractable hiccups and vomiting in AQP4-NMOSD.
Large fluffy cortical and subcortical lesions~Poorly demarcated lesions involving white and gray matter can occur in MOGAD/ADEM.
Basal meningeal enhancement and hydrocephalus~These are red flags for granulomatous, infectious, or malignant meningeal disease rather than routine MS.''')
block('dem','MRI pattern recognition','MRIpattern','''12|Which optic nerve MRI distribution most favors AQP4-NMOSD?|Posterior optic nerve and chiasmal involvement|AQP4 optic neuritis often involves long posterior segments and the chiasm. It can be severe with poor recovery; distribution alone is not diagnostic.
12|Which optic nerve MRI pattern most favors MOGAD over typical MS?|Anterior long optic nerve lesions with perineural enhancement|Long anterior lesions and perineural inflammation, often bilateral, are common MOGAD clues. Typical MS optic neuritis is more often a short unilateral intraorbital lesion.
12|A patient with otherwise typical MS has unilateral painful visual loss. Which lesion is most compatible with the usual MS optic neuritis pattern?|Short unilateral intraorbital optic nerve lesion|MS often causes a short intraorbital optic nerve lesion. NMOSD and MOGAD more often produce longer lesions and distinctive posterior or anterior distributions.
13,14|Sagittal spinal MRI demonstrates a single central lesion extending from C2 to C7. Which description best captures the important diagnostic clue?|Long central spinal cord lesion spanning at least three vertebral segments|This is longitudinally extensive transverse myelitis, a clue to NMOSD or MOGAD. Typical MS lesions are usually shorter.
13,14|Axial spinal MRI shows an H-shaped central gray matter lesion and sagittal imaging shows conus involvement. Which pattern is present?|Conus gray-matter H-sign lesion|The H-sign reflects gray matter-predominant involvement and is associated with MOGAD, though not entirely specific.
13,14|Which spinal cord pattern is most typical of MS rather than AQP4-NMOSD?|Short peripheral spinal cord lesions|MS lesions are commonly short and peripheral. Extensive central lesions should prompt consideration of NMOSD, MOGAD, and other myelopathies.
15,16|What brain lesion distribution most supports MS in a patient with compatible separate neurologic attacks?|Ovoid periventricular and juxtacortical lesions|Periventricular, cortical/juxtacortical, and infratentorial sites are characteristic. Small nonspecific lesions alone do not establish MS.
15,16,19|Persistent unexplained hiccups and vomiting correlate with which lesion location?|Area postrema dorsal medullary lesion|The area postrema is a dorsal medullary emetic center and an AQP4-rich site. This syndrome is especially associated with NMOSD.
15,16,20|An encephalopathic child has extensive poorly demarcated white and gray matter lesions. Which description best matches an ADEM/MOGAD imaging phenotype?|Large fluffy cortical and subcortical lesions|MOGAD-related ADEM can involve both gray and white matter with large indistinct lesions. This differs from classic small ovoid MS plaques.
21,22,23,36|Which MRI pattern should prompt an alternative workup rather than routine attribution to MS?|Basal meningeal enhancement and hydrocephalus|Meningeal inflammation and hydrocephalus raise concern for neurosarcoidosis, infection, or neoplastic infiltration. Imaging must be interpreted with the clinical syndrome.''')

custom('dem','MS risk factors','17,35','Which combination contains recognized associations with higher MS risk?',[
'Smoking, low vitamin D, adolescent obesity, and prior EBV infection~These are recognized epidemiologic associations. Association does not prove that correcting one factor will reverse established MS; EBV infection is common and insufficient by itself.',
'No EBV exposure, smoking cessation, and healthy weight~These are not the risk pattern described in the lecture.',
'Retinal drusen, cataracts, and iris bombe~These are ocular findings rather than the MS risk-factor cluster.',
'PMP22 deletion, high arches, and hammer toes~This cluster suggests hereditary peripheral neuropathy.',
'RB1 germline mutation and leukocoria~This is a retinoblastoma risk pattern.'])
custom('dem','MS risk factors','17,35','A patient with MS asks whether very high-dose vitamin D is proven to prevent relapses. Which response best reflects the lecture?',[
'Low vitamin D is associated with risk, but high-dose supplementation has not consistently reduced relapses in trials~Treat deficiency and consider overall health; observational associations are not equivalent to demonstrated disease-modifying efficacy.',
'High-dose vitamin D replaces all MS disease-modifying therapies~The evidence does not support replacing DMT with vitamin D.',
'Vitamin D has no relationship to MS risk in any study~The lecture describes epidemiologic associations.',
'EBV antivirals are already a proven cure for MS~The lecture explicitly notes that antiviral benefit remains unproven.',
'Only the gut microbiome determines all MS activity~Microbiome hypotheses do not establish a single deterministic cause.'])
custom('dem','MS diagnostic framework','18','Under the 2017 McDonald framework presented in the lecture, what can demonstrate dissemination in time on one MRI?',[
'Simultaneous gadolinium-enhancing and nonenhancing lesions~Different enhancement states can indicate lesions of different ages. New lesions on follow-up MRI can also demonstrate temporal dissemination; all findings require no better explanation.',
'Several identical nonspecific lesions all in one region~This alone does not establish different lesion ages or characteristic dissemination.',
'A single normal MRI~A normal scan does not show radiologic temporal dissemination.',
'Only a positive serum MOG antibody~MOG-IgG points to a different antibody-defined disorder in a fitting phenotype.',
'Only a prolonged peripheral motor distal latency~This is peripheral electrophysiology rather than CNS lesion timing.'])
custom('dem','MS diagnostic framework','18,36','In a typical clinically isolated syndrome meeting dissemination in space under the 2017 framework, which finding can substitute for MRI dissemination in time?',[
'CSF-restricted oligoclonal bands~Intrathecal IgG synthesis can substitute for DIT in the appropriate 2017 diagnostic setting. Bands are supportive but are not uniquely specific to MS.',
'Any modest CSF protein elevation~Protein elevation alone is nonspecific and is not the substitution criterion.',
'Serum oligoclonal bands alone~The relevant finding is CSF-restricted intrathecal synthesis, interpreted against paired serum.',
'A positive ganglioside antibody alone~This is not an MS temporal dissemination marker.',
'An isolated retinal microaneurysm~Diabetic retinal lesions are unrelated to MS criteria.'])
custom('dem','MS diagnostic framework','18,35','Which set lists the four characteristic dissemination-in-space regions in the lecture\'s 2017 McDonald criteria?',[
'Periventricular, cortical/juxtacortical, infratentorial, and spinal cord~2017 DIS uses characteristic lesions in at least two of these four regions. Later 2024 revisions add the optic nerve as a fifth site, so the framework year matters.',
'Lens, cornea, sclera, and choroid~These are eye structures rather than CNS MS topographies.',
'Peripheral nerve, plexus, root, and NMJ~These describe peripheral localization rather than the MS CNS regions.',
'Frontal, temporal, parietal, and occipital lobes only~MS DIS is not defined simply by counting cerebral lobes.',
'Basal meninges, pituitary, cauda equina, and retina only~This is not the characteristic 2017 region list.'])
custom('dem','MS diagnostic framework','24','Which combination satisfies the lecture\'s 2017 PPMS framework after exclusion of a better explanation?',[
'One year of progression plus two of characteristic brain lesions, at least two cord lesions, or CSF-specific oligoclonal bands~The 2017 PPMS rule requires one year of progression and two of those three supportive categories, not recurrent attacks.',
'One week of fatigue and one nonspecific white matter spot~This lacks the required progression duration and supporting evidence.',
'Two peripheral entrapment neuropathies~Peripheral focal lesions do not satisfy CNS PPMS criteria.',
'A positive MOG-IgG result alone~This supports a distinct diagnosis in the appropriate syndrome.',
'A single episode of optic neuritis alone~This does not satisfy the 2017 PPMS requirements.'])
custom('dem','MS diagnostic framework','25,35,36','An asymptomatic person has incidental MRI lesions strongly suggestive of demyelination, with no past neurologic attacks and no better explanation. Which label is appropriate?',[
'Radiologically isolated syndrome~RIS describes incidentally found MS-like lesions without a clinical demyelinating event. It differs from clinically isolated syndrome, which requires a clinical attack; risk is variable.',
'Clinically isolated syndrome~CIS requires a symptomatic clinical demyelinating episode.',
'Definite CIDP~CIDP is a peripheral clinical and electrodiagnostic disorder.',
'Proven MOGAD from MRI alone~MOGAD requires a fitting syndrome and appropriately interpreted MOG-IgG.',
'Normal aging in every case~Characteristic demyelinating lesions should not automatically be dismissed as aging.'])
custom('dem','MS diagnostic framework','26,35,36','What does the central vein sign show within many MS plaques?',[
'A small vein traversing the center of a white matter lesion~The sign reflects the perivenular organization of MS inflammation and can improve specificity when appropriately assessed; it is not simply any dark dot on MRI.',
'Calcification in a retinal tumor~This is unrelated to cerebral perivenular lesions.',
'A clot in the central retinal vein~Despite the word central, this is a brain MRI plaque sign.',
'A CSF leak around every lesion~The sign is venous, not a CSF fistula.',
'Diffuse peripheral nerve swelling~That is an ultrasound finding rather than a central vein sign.'])
custom('dem','MS diagnostic framework','35','A chronic MS plaque has a paramagnetic rim on susceptibility MRI. What produces this rim?',[
'Iron-containing microglia and macrophages at a chronic active lesion edge~Paramagnetic rim lesions mark a subset of chronic active lesions. They can be highly specific but are not sufficiently sensitive to exclude MS when absent.',
'Calcium in lens crystallins~Lens deposits are not the source of a cerebral paramagnetic rim.',
'A ring of retinal neovascularization~This is an ocular vascular process.',
'Peripheral Schwann cell duplication~This concerns peripheral nerves rather than CNS plaques.',
'Normal cortical melanin in all healthy brains~This does not explain chronic active MS lesion rims.'])
custom('dem','MS diagnostic framework','35,36','Which statement accurately updates the lecture\'s proposed MS criteria discussion?',[
'The 2024 revisions include optic nerve topography and selected biomarker pathways~Published revisions add the optic nerve as a fifth site and allow kappa free light chains, central vein sign, and paramagnetic rim lesions in defined pathways. The lecture\'s shorthand is not a substitute for the full algorithm.',
'The 2017 criteria already counted the optic nerve as a fifth site~The optic nerve addition belongs to the later revision.',
'Any isolated optic neuritis now proves MS~Optic nerve involvement alone does not automatically establish MS; alternatives must be excluded.',
'Kappa free light chains are uniquely specific for MS regardless of context~They reflect intrathecal immune activity and require contextual interpretation.',
'Dissemination and differential diagnosis no longer matter~Characteristic localization, supportive evidence, and exclusion of mimics remain essential.'])
custom('dem','MS diagnostic framework','36','Why might CSF kappa free light chain measurements be useful in an MS evaluation?',[
'They provide a quantitative marker of intrathecal immunoglobulin synthesis~Kappa FLC assessment can be faster and more rater-independent than band interpretation and has a role in current criteria when measured appropriately. An isolated uncontextualized value does not prove MS.',
'They directly measure optic nerve myelin thickness~OCT measures retinal layers; FLCs assess immune synthesis.',
'They diagnose peripheral conduction block~This requires NCS rather than CSF FLCs.',
'They replace exclusion of infection~Inflammatory CSF biomarkers are not specific enough to bypass differential diagnosis.',
'They quantify lens opacity~They are not an ophthalmic cataract measurement.'])
custom('dem','MS red flags','21,22,23','Which finding most strongly argues for a mimic rather than uncomplicated typical MS?',[
'Marked CSF pleocytosis with meningeal enhancement and a continuously enlarging lesion~Prominent inflammatory CSF, meningeal disease, mass-like growth, infarcts, microbleeds, and persistent enhancement should prompt reconsideration. The lecture mnemonic flags meninges, indistinct/increasing lesions, macrobleeds, infarcts, and symmetric patterns.',
'Separate typical neurologic episodes with recovery~This pattern can support relapsing MS.',
'Ovoid periventricular lesions~These are characteristic when accompanied by a suitable clinical syndrome.',
'Short peripheral spinal cord lesions~These can be compatible with MS.',
'CSF-restricted oligoclonal bands in a typical syndrome~This supports MS but is not perfectly specific.'])
custom('dem','MS red flags','22,23','A presumed demyelinating case has complete gaze palsy with fluctuating ophthalmoparesis. Which focused test addresses a listed alternative?',[
'Neuromuscular junction evaluation including AChR/MuSK antibodies and electrophysiology~Fluctuating ocular weakness may indicate MG rather than a fixed CNS demyelinating lesion. Chest imaging may identify thymic disease in the appropriate setting.',
'Assume all fluctuating weakness is MS relapse~Fluctuation and fatigability warrant a different localization workup.',
'Routine distal sensory NCS alone~Sensory NCS is usually normal in MG and does not test the NMJ safety margin.',
'Brain MRI alone as a test for NMJ transmission~MRI can assess CNS causes but cannot directly demonstrate fatigable neuromuscular transmission failure.',
'PMP22 analysis as the only test~HNPP does not usually present with isolated fatigable ophthalmoparesis.'])
custom('dem','Neuroimmunology update','36','Which history favors viral over autoimmune limbic encephalitis in the lecture\'s comparison?',[
'Acute fever, headache, nausea, and CSF pleocytosis~An acute febrile illness is an infectious warning sign. Autoimmune limbic encephalitis often presents subacutely with memory, psychiatric, and seizure symptoms, but overlap requires careful evaluation.',
'Six weeks of isolated psychiatric and memory change without fever~This pattern may favor autoimmune disease but is not independently diagnostic.',
'Chronic pes cavus since childhood~This suggests hereditary peripheral neuropathy.',
'Painless lens opacity over years~This suggests cataract rather than encephalitis.',
'A purely peripheral conduction block~This localizes outside the limbic system.'])
custom('dem','Radiologically isolated syndrome','35,36','Which RIS profile predicts a higher chance of a future clinical demyelinating event?',[
'Younger age, spinal or infratentorial lesions, enhancement, and CSF-restricted bands~These features increase conversion risk. The deck cites different cohort-specific 10- and 15-year estimates; those figures are not an individual certainty.',
'No characteristic lesions and a normal MRI~This would not establish RIS.',
'Only a cataract and refractive error~These do not predict CNS demyelinating conversion.',
'Only an isolated carpal tunnel lesion~This is a peripheral disorder.',
'Absence of all inflammatory markers guarantees progression~Risk is probabilistic, not guaranteed by their absence.'])
custom('dem','Radiologically isolated syndrome','36','Which pair of agents had trials reporting delayed first clinical events in selected RIS populations in the lecture?',[
'Dimethyl fumarate and teriflunomide~The deck cites reduced event risk in specific trials. These are selected-population trial findings, not a rule that every person with incidental MRI spots should receive treatment.',
'Mannitol and labetalol~These address selected acute pressure emergencies, not RIS disease modification.',
'Artificial tears and intraocular lenses~These are ocular interventions.',
'IV antibiotics and cataract extraction~This pair does not represent the cited RIS trials.',
'Pyridoxine megadoses and vitamin A megadoses~Excess supplementation can cause toxicity and is not the cited strategy.'])

pool('test','''Visual evoked potentials~VEP measures visual pathway conduction; demyelination can prolong P100 latency even with recovered acuity.
Optical coherence tomography~OCT quantifies retinal nerve fiber and ganglion cell layers and can show axonal loss after optic neuritis.
Somatosensory evoked potentials~SSEPs assess conduction from stimulated peripheral nerves to spinal and cortical responses, helping identify central pathway delays.
Nerve conduction studies~NCS evaluates peripheral motor and sensory conduction, including velocity, latency, amplitude, temporal dispersion, and conduction block.
Needle electromyography~Needle EMG assesses spontaneous muscle activity and motor unit recruitment, supporting neurogenic or myopathic localization.
Neuromuscular ultrasound~Ultrasound can show nerve enlargement, entrapment, and proximal nerve or plexus abnormalities in inflammatory neuropathies.
Single-fiber electromyography~SFEMG measures neuromuscular transmission jitter and is sensitive for NMJ dysfunction, but not uniquely specific to MG.
Repetitive nerve stimulation~RNS assesses CMAP changes with repeated stimulation; low-frequency decrement favors MG and marked postexercise/high-frequency increment favors LEMS.
Serum protein electrophoresis with immunofixation~SPEP/IF screens for monoclonal proteins in acquired neuropathies such as CIDP-like syndromes, DADS, or POEMS.
Nerve biopsy~Biopsy has selected roles such as suspected nonsystemic vasculitic neuropathy; it is not required for routine electrodiagnostically established CIDP.''')
block('dem','Diagnostic tests','test','''27|After recovery from optic neuritis, a patient has normal visual acuity but suspected persistent conduction delay. Which test detects delayed P100 responses?|Visual evoked potentials|VEP can reveal slowed conduction from optic pathway demyelination despite clinical recovery. It measures physiology, whereas OCT measures retinal structure.
27|Which noninvasive test quantifies retinal nerve fiber and ganglion cell thinning after optic neuritis?|Optical coherence tomography|OCT measures retinal layer thickness and can document axonal loss. It does not directly measure ocular pressure or establish an antibody diagnosis.
28|Median and posterior tibial nerve stimulation is used to compare peripheral, spinal, and cortical response latencies. Which test is being performed?|Somatosensory evoked potentials|SSEPs evaluate sensory pathway conduction and can help identify central conduction delays, including spinal or dorsal column dysfunction.
51,52|Which study distinguishes a low-amplitude axonal neuropathy from a slowed demyelinating neuropathy?|Nerve conduction studies|CMAP/SNAP amplitudes reflect functioning axons; conduction slowing, prolonged latencies, temporal dispersion, and block suggest myelin dysfunction, with appropriate technical controls.
53|Which test detects fibrillation potentials and large reinnervated motor units in muscle?|Needle electromyography|Needle EMG evaluates spontaneous activity and motor unit morphology/recruitment. It complements NCS rather than replacing sensory nerve studies.
54|A patient has suspected CIDP and proximal median nerve or brachial plexus enlargement is sought. Which test is used?|Neuromuscular ultrasound|Inflammatory demyelinating nerves may be enlarged on ultrasound. It is an adjunct to clinical and electrophysiologic criteria, not a standalone diagnosis.
55|Which electrophysiologic technique measures jitter between individual muscle fiber action potentials?|Single-fiber electromyography|Increased jitter indicates impaired neuromuscular transmission. It is sensitive but can also be abnormal in other neurogenic or myopathic settings.
55|Which test demonstrates a decremental muscle response to repeated low-frequency stimulation in MG?|Repetitive nerve stimulation|Typical MG testing uses low-frequency RNS. The lecture phrase linking MG decrement to high-rate stimulation is corrected; LEMS often shows facilitation after exercise or high-frequency stimulation.
49,65,66|Which blood study should be included when evaluating possible CIDP or anti-MAG neuropathy?|Serum protein electrophoresis with immunofixation|Monoclonal gammopathy can identify a CIDP mimic, DADS/anti-MAG disease, or another paraproteinemic syndrome. A monoclonal protein also warrants evaluation of its significance.
49|Painful asymmetric axonal neuropathy suggests nonsystemic vasculitis. Which selected diagnostic procedure may be appropriate?|Nerve biopsy|Biopsy can establish nonsystemic vasculitic neuropathy. In known systemic vasculitis it is generally reserved for cases where the result would change treatment.''')

pool('drug','''Interferon beta~Interferon beta modulates inflammatory signaling and immune trafficking; monitoring includes blood counts, liver function, and thyroid function.
Glatiramer acetate~Glatiramer shifts T-cell responses toward immunoregulation and can induce regulatory cells; routine laboratory monitoring burden is relatively low.
Teriflunomide~Teriflunomide inhibits dihydroorotate dehydrogenase, limiting pyrimidine synthesis and activated lymphocyte proliferation; liver and reproductive safety require attention.
Dimethyl fumarate~Fumarates activate Nrf2-associated antioxidant responses and have immune effects; blood counts and liver tests help monitor toxicity, including lymphopenia.
Fingolimod~This S1P receptor modulator sequesters lymphocytes in lymphoid tissue; cardiac, ophthalmic, blood count, and liver monitoring are relevant.
Siponimod~Siponimod modulates S1P1 and S1P5 and has a role in active secondary progressive MS; it limits lymphocyte egress.
Ozanimod~Ozanimod modulates S1P1 and S1P5, reducing lymphocyte exit from lymphoid tissue; it is not a CD20 antibody.
Ponesimod~Ponesimod selectively modulates S1P1 and reduces lymphocyte egress; it is not a pyrimidine synthesis inhibitor.
Cladribine~Cladribine impairs DNA synthesis and depletes lymphocytes; blood count and infection-risk monitoring matter.
Natalizumab~Natalizumab blocks alpha-4 integrin-mediated immune cell trafficking into CNS; JC virus-related PML risk is a major monitoring concern.
Ocrelizumab~Ocrelizumab targets CD20-positive B cells and is used in relapsing MS and PPMS; blood counts, immunoglobulins, and infection screening are relevant.
Ofatumumab~Ofatumumab is a CD20-directed B-cell-depleting monoclonal antibody administered subcutaneously for relapsing MS.
Alemtuzumab~Alemtuzumab targets CD52 and depletes lymphocytes; prolonged surveillance for autoimmune thyroid, hematologic, and renal complications is required.
Mitoxantrone~Mitoxantrone is a cytotoxic agent with cardiomyopathy, marrow suppression, and malignancy concerns; cardiac ejection fraction monitoring is important.
Eculizumab~Eculizumab blocks complement C5 and can prevent relapses in AQP4-IgG-positive NMOSD; protection against meningococcal infection is essential.
Satralizumab~Satralizumab blocks the IL-6 receptor and is used for relapse prevention in AQP4-positive NMOSD.
Rituximab~Rituximab is an anti-CD20 antibody used in several neuroimmune conditions; effectiveness differs across AQP4-NMOSD and MOGAD.
Tocilizumab~Tocilizumab blocks IL-6 receptors and has evidence in refractory NMOSD; it does not block C5.''')
block('dem','Disease-modifying treatment mechanisms','drug','''29|Which MS drug inhibits dihydroorotate dehydrogenase?|Teriflunomide|Inhibiting pyrimidine synthesis limits activated lymphocyte proliferation. The lecture table includes liver tests, BP, and neuropathy monitoring.
29|Which MS treatment shifts T-cell cytokine responses toward Th2/regulatory activity and generally does not require routine laboratory monitoring?|Glatiramer acetate|Glatiramer is an immunomodulatory treatment with relatively limited routine lab monitoring needs compared with many oral or antibody agents.
29|Which listed MS agent activates an Nrf2-associated response to oxidative stress?|Dimethyl fumarate|Dimethyl fumarate and related fumarates share an active metabolite and antioxidant/immune effects. CBC and liver monitoring are important.
29|A patient starts injectable MS immunomodulation that alters inflammatory cytokine signaling. CBC, liver enzymes, and TSH are followed. Which agent best fits?|Interferon beta|The beta interferons alter immune signaling and reduce relapsing inflammatory activity. Their monitoring includes hematologic, hepatic, and thyroid effects.
30|Which agent requires phosphorylation and modulates S1P receptors to prevent lymphocytes leaving lymph nodes?|Fingolimod|Fingolimod is phosphorylated to its active form and acts at several S1P receptor subtypes. Lymphocyte sequestration reduces CNS trafficking.
30|Which S1P1/S1P5 modulator in the lecture is particularly associated with active secondary progressive MS?|Siponimod|Siponimod reduces lymphocyte egress and has evidence in active SPMS. The question distinguishes its clinical emphasis from other agents with related mechanisms.
30|An MS prescription is identified by its brand name Zeposia. Which generic drug is it?|Ozanimod|Ozanimod shares the lymphocyte egress mechanism with other S1P modulators. It is pharmacologically distinct from CD20 antibodies.
30|Which listed agent selectively modulates S1P1 rather than inhibiting dihydroorotate dehydrogenase?|Ponesimod|Ponesimod limits lymphocyte migration through selective S1P1 modulation. Teriflunomide is the pyrimidine synthesis inhibitor used as a comparator in the lecture table.
30|An oral MS immune-reconstitution agent reduces T and B lymphocytes by interfering with DNA synthesis. Which drug is it?|Cladribine|Cladribine is lymphotoxic and requires careful hematologic and infection monitoring. It differs from agents that mainly trap lymphocytes in nodes.
31|Which drug prevents alpha-4 integrin-mediated immune cell migration into the CNS?|Natalizumab|Blocking VLA-4/alpha-4 integrin reduces trafficking across the blood-brain barrier. PML risk stratification includes JC virus antibody assessment.
31,32,35|Which CD20-directed drug in the lecture has an indication for primary progressive MS?|Ocrelizumab|Ocrelizumab depletes CD20-positive B cells and is used for PPMS as well as relapsing MS. Its effect is not direct remyelination.
31,32,35|Which CD20-directed relapsing-MS treatment is given by monthly subcutaneous administration after loading?|Ofatumumab|Ofatumumab is a fully human CD20 antibody administered subcutaneously. The lecture contrasts it with periodically infused B-cell therapies.
31|Which lymphocyte-depleting drug targets CD52 and requires long-term thyroid, renal, and hematologic surveillance?|Alemtuzumab|Alemtuzumab can trigger delayed secondary autoimmunity after lymphocyte depletion, explaining prolonged monitoring.
31|An older MS cytotoxic therapy requires surveillance of cardiac ejection fraction. Which drug is it?|Mitoxantrone|Mitoxantrone has cumulative cardiotoxicity and marrow/malignancy risks, which limit its use relative to newer options.
33|Which NMOSD relapse-prevention agent blocks complement C5?|Eculizumab|Eculizumab, and the longer-acting related agent ravulizumab, inhibit terminal complement in AQP4-positive disease. They are not established therapies for all MOGAD.
33|Which subcutaneous monoclonal antibody targets IL-6 receptors for relapse prevention in AQP4-positive NMOSD?|Satralizumab|Satralizumab blocks IL-6 signaling. Its target differs from anti-CD20 agents and terminal complement inhibitors.
33,34|Which B-cell-depleting drug is commonly used worldwide for AQP4-NMOSD but is less consistently effective in MOGAD?|Rituximab|Rituximab can reduce AQP4-NMOSD relapses; MOGAD responses are less reliable. A common clinical phenotype does not imply identical response across antibody diseases.
33|Which IL-6 receptor blocker discussed in the lecture has evidence in refractory NMOSD and is distinct from satralizumab?|Tocilizumab|Tocilizumab is an IL-6 receptor antibody with clinical evidence in NMOSD, including comparison with azathioprine in a trial.''')

custom('dem','Treatment monitoring','29,30','A patient starting fingolimod has diabetes and a history of uveitis. Which baseline surveillance is particularly relevant?',[
'Ophthalmic assessment for macular edema, plus cardiac and laboratory safety assessment~S1P modulators can cause macular edema and cardiac conduction effects. CBC, liver, skin, and other agent-specific monitoring also matter.',
'No ocular monitoring because all MS drugs protect the macula~S1P modulators can affect the macula, so this is incorrect.',
'Only screening for thyroid autoantibodies~Thyroid testing does not replace the relevant ophthalmic and cardiac safety assessment.',
'Only a serum vitamin D level~Vitamin D testing does not detect macular edema or cardiac conduction risk.',
'Only periodic visual acuity without retinal assessment~Macular edema can require targeted ophthalmic evaluation beyond a basic acuity screen.'])
custom('dem','Treatment monitoring','31','A patient receiving natalizumab has new progressive cognitive and focal neurologic deficits. Which safety issue warrants urgent evaluation?',[
'Progressive multifocal leukoencephalopathy associated with JC virus~Natalizumab impairs immune surveillance in the CNS. PML must be considered with new atypical progressive deficits, alongside relapse and other alternatives.',
'All new symptoms are automatically an MS relapse~This can miss an opportunistic infection.',
'A benign infusion reaction several months after the last dose~Delayed progressive focal deficits are not adequately explained by a transient infusion reaction.',
'A peripheral demyelinating neuropathy as the explanation for aphasia~Aphasia and cognitive change localize to CNS rather than isolated peripheral nerves.',
'A medication effect that can be assumed without imaging~Progressive focal deficits require investigation rather than automatic attribution to a benign drug effect.'])
custom('dem','B-cell treatment','32,35','Why can anti-CD20 therapy deplete mature B cells while sparing many plasma cells?',[
'CD20 is expressed on many mature B cells but not on most terminally differentiated plasma cells~Complement-dependent and antibody-dependent mechanisms deplete CD20-positive cells. Antibody levels and infection risk still require monitoring.',
'All plasma cells express more CD20 than mature B cells~Most terminal plasma cells lack CD20.',
'CD20 antibodies directly target oligodendrocyte myelin~Their primary target is a B-cell surface antigen.',
'CD20 is the same as AQP4~These are distinct proteins on different cell types.',
'Anti-CD20 treatment instantly eliminates all immunoglobulin~Existing plasma cells and antibodies are not immediately eradicated.'])
custom('dem','Acute demyelinating treatment','33,34','Severe optic neuritis and longitudinally extensive myelitis leave a patient unable to walk despite high-dose corticosteroids. What escalation should be considered early?',[
'Plasma exchange~Early PLEX is appropriate to consider for severe inflammatory demyelinating attacks with poor response or major disability. Delay can worsen recovery; acute rescue differs from long-term relapse prevention.',
'Delay all treatment until every antibody result returns~Severe attacks warrant prompt treatment while investigations proceed.',
'Treat solely with oral vitamin D~Vitamin D does not replace acute rescue immunotherapy.',
'Begin interferon beta as immediate rescue for the severe attack~Interferon is not an acute rescue therapy and can be unsuitable in NMOSD.',
'Use rehabilitation alone while inflammation remains untreated~Rehabilitation is valuable but does not replace acute immunotherapy for a severe inflammatory attack.'])
custom('dem','MOGAD treatment','34','A child with relapsing MOGAD needs relapse prevention while minimizing long-term immunosuppression. Which option is highlighted in the lecture?',[
'Maintenance IV immunoglobulin~IVIg is a reasonable preventive option in selected pediatric MOGAD. Decisions depend on relapse history and individual circumstances rather than antibody positivity alone.',
'Assume eculizumab is equally proven for all MOGAD~Complement-inhibitor evidence and approvals focus on AQP4-positive NMOSD, not all MOGAD.',
'No prevention is ever considered after recurrent disabling attacks~Relapsing disease may warrant preventive therapy.',
'Routine natalizumab for all MOGAD relapses~An MS trafficking therapy cannot be assumed effective for MOGAD prevention.',
'High-dose pyridoxine~Excess pyridoxine can cause sensory neuronopathy.'])
custom('dem','MOGAD treatment','34','Why may a corticosteroid taper be used after acute MOGAD treatment?',[
'To reduce early symptom recrudescence after abrupt steroid withdrawal~MOGAD can relapse or worsen with rapid tapering. Duration is individualized; a taper is not proof that long-term disease is cured.',
'To generate a positive AQP4 antibody~Steroid tapering is not intended to change diagnosis by inducing antibodies.',
'To treat posterior lens epithelial migration~Steroids can contribute to cataracts rather than cure their morphology.',
'To regenerate lost motor neurons in ALS~This is not a steroid-responsive demyelinating mechanism.',
'To eliminate all future relapse risk permanently~A taper cannot guarantee lifelong protection.'])
custom('dem','MOGAD prognosis','34','Serial MOG-IgG testing becomes negative after recovery. What is the most appropriate interpretation?',[
'Future relapse risk may be lower, but seronegativity is not an absolute guarantee~Seroconversion can inform prognosis in context. Clinical history and phenotype remain important, and occasional relapses can still occur.',
'The original compatible illness was necessarily fabricated~Antibody levels can change after a real attack.',
'The patient now definitely has AQP4-NMOSD~MOG seronegativity does not create AQP4 positivity.',
'All established neurologic deficits must immediately disappear~Serologic improvement does not reverse every structural injury.',
'Testing alone mandates stopping all treatment immediately~Treatment decisions require clinical judgment, not one result.'])
custom('dem','MS progression','35','What does progression independent of relapse activity (PIRA) mean?',[
'Disability accumulates without a temporally linked recognized relapse~Neurodegenerative and chronic inflammatory mechanisms can contribute to progression beyond overt attacks. Preventing relapses does not necessarily abolish all progression.',
'Every deficit occurs only during fever~Fever-related transient recrudescence is a different concept.',
'Every new symptom is a retinal disorder~PIRA concerns MS disability progression.',
'No axonal injury occurs in MS~Axonal and neuronal injury can contribute substantially.',
'MRI enhancement is required for every episode of progression~PIRA may occur without a new overt enhancing relapse.'])
custom('dem','Treatment evidence interpretation','29,30,31,35','One DMT trial reports a 50% relapse reduction against placebo and another a 40% reduction against an active comparator. What is the best interpretation?',[
'Cross-trial percentages cannot establish a direct ranking without considering comparator and population~The lecture tables use different comparators, endpoints, doses, and follow-up periods. Relative percentages are not interchangeable absolute benefits.',
'The first drug is necessarily superior for every patient~Different trial designs prevent that inference.',
'Both drugs have identical absolute effects~Relative percentages do not specify baseline absolute risk.',
'A 50% reduction means no treated person relapses~Risk reduction does not mean complete elimination.',
'Disability and relapse endpoints are always identical~Trials measure distinct outcomes with different implications.'])

pool('leuko','''Adrenoleukodystrophy~ABCD1-related peroxisomal disease can cause childhood cerebral behavioral decline, adult adrenomyeloneuropathy, or isolated adrenal insufficiency.
Metachromatic leukodystrophy~ARSA deficiency commonly causes childhood motor regression and peripheral neuropathy, with sulfatide accumulation.
Aicardi-Goutieres syndrome~A type I interferon-related autoinflammatory disorder can mimic congenital infection or present later with an ADEM-like illness.
Alexander disease~GFAP-related astrocytic disease can cause infantile macrocephaly and developmental problems or later bulbar, autonomic, and eye movement findings.
Krabbe disease~GALC-related leukodystrophy can cause irritability, spasticity, and neuropathy; psychosine is an important biomarker.
Pelizaeus-Merzbacher disease~PLP1-related hypomyelination may present with nystagmus and stridor.
Vanishing white matter disease~EIF2B-related disease can worsen after trauma or infection; MRI abnormalities can precede episodic neurologic decline.
POLR3-related leukodystrophy~Hypomyelination with hypodontia and hypogonadotropic hypogonadism is a characteristic POLR3-related pattern.
TUBB4A-related disorder~TUBB4A disease can cause hypomyelination with basal ganglia/cerebellar atrophy and predominantly motor impairment.
Cerebrotendinous xanthomatosis~CYP27A1-related sterol metabolism disease may cause systemic manifestations such as juvenile cataracts, diarrhea, and tendon xanthomas before neurologic dysfunction.
Canavan disease~ASPA-related disease can produce macrocephaly, hypotonia, developmental impairment, and exaggerated startle.''')
block('dem','Leukodystrophies','leuko','''37,38|A school-age boy develops new attention and behavior problems, progressive white matter disease, and adrenal insufficiency. Which diagnosis is most likely?|Adrenoleukodystrophy|Cerebral ALD often begins with behavioral or attention changes in boys. ABCD1 disease also includes adrenomyeloneuropathy and isolated Addison disease phenotypes.
37,38|A toddler loses gross motor milestones, develops difficulty walking and peripheral neuropathy, and has deficient arylsulfatase A activity. Which diagnosis is most likely?|Metachromatic leukodystrophy|ARSA-related MLD commonly begins with early motor decline. Strabismus or peripheral neuropathy can precede more obvious CNS manifestations.
37,38|A newborn has neurologic disability and a multiorgan inflammatory illness resembling congenital infection, but infectious studies are negative. Which inherited syndrome is most consistent?|Aicardi-Goutieres syndrome|This interferonopathy can mimic congenital infection early or an ADEM-like syndrome later. Several nucleic acid metabolism/sensing genes are involved.
37,38|An infant has macrocephaly, developmental delay, feeding difficulty, vomiting, and a GFAP pathogenic variant. Which diagnosis is most likely?|Alexander disease|Type I Alexander disease often has early cerebral symptoms and macrocephaly; type II emphasizes bulbar, autonomic, and ocular motor dysfunction.
37,38|An adult with a GFAP mutation has prominent bulbar symptoms, autonomic dysfunction, and abnormal eye movements. Which leukodystrophy is most likely?|Alexander disease|These features fit the later/type II Alexander phenotype. The same gene can produce a different clinical pattern from infantile disease.
37,38|A very irritable infant develops spasticity and peripheral neuropathy. Blood psychosine is markedly elevated. Which disorder is most likely?|Krabbe disease|Psychosine accumulation is a useful Krabbe biomarker. GALC deficiency causes globoid cell leukodystrophy.
37,38|A young boy has prominent nystagmus, stridor, and diffuse hypomyelination with a PLP1 pathogenic variant. Which diagnosis fits?|Pelizaeus-Merzbacher disease|PLP1-related hypomyelination can present early with nystagmus and stridor. These features distinguish it from acquired relapsing demyelination.
37,38|A child with previously identified white matter abnormalities deteriorates after a mild head injury and later after an infection. Which disorder is most likely?|Vanishing white matter disease|EIF2B-related disease can undergo stress-provoked neurologic decline. Imaging abnormalities may precede symptoms.
37,38|A teenager has hypomyelination, missing teeth, and delayed puberty due to hypogonadotropic hypogonadism. Which diagnosis is most likely?|POLR3-related leukodystrophy|The combination of hypomyelination, hypodontia, and hypogonadotropic hypogonadism is often called 4H syndrome and suggests POLR3-related disease.
37,38|A child has hypomyelination with basal ganglia and cerebellar atrophy, prominent motor dysfunction, and relatively less cognitive impairment. Which diagnosis fits?|TUBB4A-related disorder|TUBB4A-associated disease can have a predominantly motor phenotype, including hypomyelination with atrophy of basal ganglia and cerebellum.
37,38|A patient has childhood diarrhea and juvenile cataracts, then tendon xanthomas and progressive neurologic dysfunction. CYP27A1 testing is abnormal. What is the diagnosis?|Cerebrotendinous xanthomatosis|Systemic signs can precede neurologic dysfunction in this treatable sterol metabolism disorder. The early ocular and gastrointestinal history is an important clue.
37,38|An infant has profound hypotonia, macrocephaly, exaggerated startle, and an ASPA pathogenic variant. Which diagnosis fits?|Canavan disease|Canavan disease is an ASPA-related leukodystrophy. Macrocephaly can also occur in Alexander disease, so associated signs and molecular findings distinguish them.''')

# Localization choices carry explicit territory explanations rather than generic wrong-answer text.
pool('root','''C5 root~C5 emphasizes shoulder abduction and elbow flexion, lateral upper arm sensation, and biceps/brachioradialis reflex contributions.
C6 root~C6 emphasizes wrist extension, lateral forearm/thumb sensation, and biceps/brachioradialis reflex contributions.
C7 root~C7 emphasizes elbow extension, finger extension, middle digit sensation, and the triceps reflex.
C8 root~C8 emphasizes finger flexion and medial hand/fourth-fifth digit sensation; no single reliable routine reflex isolates it.
T1 root~T1 emphasizes hand intrinsic muscles and medial forearm sensation; routine deep tendon reflexes are not specific.
L2 root~L2 emphasizes hip flexion and anterior thigh sensation; there is no dependable isolated routine tendon reflex.
L3 root~L3 contributes to hip flexion, adduction, and knee extension with medial thigh/knee sensation and patellar reflex contribution.
L4 root~L4 emphasizes knee extension and medial lower leg sensation, with the patellar reflex.
L5 root~L5 emphasizes dorsiflexion, great toe extension, hip abduction, and dorsal foot sensation; no standard routine reflex is specific.
S1 root~S1 emphasizes plantarflexion and posterior/lateral calf or lateral foot sensation, with the Achilles reflex.''')
block('dem','Root localization','root','''41|Neck pain radiates to the lateral upper arm. Deltoid and biceps strength are reduced, and the biceps reflex is diminished. Which root best fits?|C5 root|C5 contributes strongly to shoulder abduction and elbow flexion. The lateral upper arm sensory territory helps distinguish it from C6 thumb/lateral forearm findings.
41|A patient has neck-to-thumb pain, weak wrist extension, and a reduced brachioradialis reflex. Which root is most likely affected?|C6 root|The thumb/lateral forearm pattern with wrist extension weakness supports C6 radiculopathy. Root territories overlap, so the combined pattern matters.
41|Neck pain extends into the middle finger. Triceps and finger extensors are weak and the triceps reflex is reduced. Which root is most likely affected?|C7 root|C7 supplies a prominent component of triceps and finger extensor function, with sensory change toward the third digit.
41|A patient has weak finger flexion with numbness of the fourth and fifth digits extending beyond a single distal nerve distribution. Which root best fits?|C8 root|C8 contributes to finger flexors and medial hand sensation. An ulnar mononeuropathy is a differential, but involvement beyond one nerve supports a root lesion.
41|Hand intrinsic weakness accompanies medial forearm sensory loss. Which root is most implicated?|T1 root|T1 is important for intrinsic hand function and medial forearm sensation. There is no reliable routine tendon reflex for isolated T1 localization.
42|Hip flexion weakness is accompanied by anterior thigh numbness without a specific deep tendon reflex abnormality. Which root best fits the lecture table?|L2 root|L2 supplies iliopsoas-related hip flexion and anterior thigh sensation. More distal medial leg sensory changes would suggest L4.
42|A radicular syndrome causes hip adduction and knee extension weakness with medial thigh and knee sensory change. Which root is most likely?|L3 root|L3 contributes to adductors and quadriceps. The patellar reflex has L3-L4 contributions; localization should use the full pattern.
42|Back pain radiates to the medial lower leg. Quadriceps strength and the patellar reflex are reduced. Which root best fits?|L4 root|L4 radiculopathy often affects knee extension and medial leg sensation with a reduced knee jerk.
42|Foot drop is accompanied by weak great toe extension and hip abduction. Sensation is reduced over the dorsum of the foot. Which root is most likely?|L5 root|L5 includes dorsiflexors, great toe extensors, and gluteus medius. Hip abduction and inversion weakness help distinguish a root lesion from common fibular neuropathy.
42|A patient cannot perform a single-leg toe raise and has a reduced Achilles reflex with lateral foot numbness. Which root is most likely affected?|S1 root|S1 supplies plantarflexion and contributes to the Achilles reflex, with posterolateral calf/lateral foot sensory distribution.''')

pool('plexus','''Upper brachial plexus trunk~C5-C6 upper trunk injury affects shoulder abduction/external rotation and elbow flexion with lateral arm/forearm sensory loss.
Middle brachial plexus trunk~The C7 middle trunk emphasizes triceps, wrist/finger extensor functions, and central hand sensory distribution.
Lower brachial plexus trunk~C8-T1 lower trunk injury affects hand intrinsic and finger flexor muscles with medial forearm/hand sensory loss.
Lateral brachial plexus cord~The lateral cord contributes to musculocutaneous and median territories, including elbow flexion and lateral forearm/palmar radial-hand sensation.
Medial brachial plexus cord~The medial cord contributes to ulnar and medial median functions, with medial forearm/hand sensation and intrinsic hand weakness.
Posterior brachial plexus cord~The posterior cord supplies axillary and radial distributions, affecting deltoid and extensors with dorsal arm/hand sensory involvement.
Lumbar plexus~Lumbar plexus lesions combine femoral and obturator territory deficits, affecting hip flexion, knee extension, and adduction with a reduced patellar reflex.
Lower lumbosacral plexus~Lower plexus lesions can combine gluteal and sciatic territory deficits involving posterior thigh, leg, and foot functions with an impaired Achilles reflex.''')
block('dem','Plexus localization','plexus','''43|After shoulder traction, a patient has weakness of supraspinatus, infraspinatus, deltoid, and biceps with lateral arm and forearm sensory loss. Which plexus segment is most likely affected?|Upper brachial plexus trunk|The affected muscles span several named nerves but share C5-C6 upper trunk input, supporting a plexus rather than one mononeuropathy.
43|A plexus injury predominantly affects triceps and forearm extensors with third-digit sensory change. Which trunk is most implicated?|Middle brachial plexus trunk|The middle trunk carries C7 fibers. The pattern resembles C7 but a plexus lesion can be distinguished by electrodiagnostic and clinical distribution.
43|A patient has finger flexor and interosseous weakness plus medial forearm and fourth-fifth digit numbness after lower plexus trauma. Which trunk is involved?|Lower brachial plexus trunk|C8-T1 lower trunk injury affects medial hand functions and sensory territories across more than one terminal nerve.
43|Elbow flexion and pronation are weak with lateral forearm and radial palmar hand sensory loss. A cord-level plexus lesion is established. Which cord fits?|Lateral brachial plexus cord|The lateral cord contributes to musculocutaneous and lateral median components, combining biceps and median-innervated forearm functions.
43|Interossei and medial finger flexors are weak with medial forearm and ulnar-hand sensory loss. A cord-level lesion is established. Which cord fits?|Medial brachial plexus cord|The medial cord supplies ulnar and medial median contributions. Sensory change beyond the ulnar nerve territory supports a proximal lesion.
43|A plexus lesion weakens deltoid, triceps, and wrist extensors with dorsal arm and hand sensory loss. Which cord is implicated?|Posterior brachial plexus cord|Both axillary and radial distributions arise from the posterior cord, explaining combined shoulder abduction and extensor deficits.
44|Hip flexion, hip adduction, and knee extension are weak with anterior thigh/medial leg sensory loss and a reduced patellar reflex. Which plexus is affected?|Lumbar plexus|Combined femoral and obturator deficits favor lumbar plexopathy rather than an isolated femoral lesion.
44|A plexus lesion affects gluteal, hamstring, and distal leg muscles with posterior thigh, leg, and broad foot sensory loss. Which localization fits?|Lower lumbosacral plexus|A broad pattern involving gluteal and sciatic functions is more proximal than a single distal leg nerve lesion.''')

pool('nerve','''Dorsal scapular nerve~This supplies rhomboids; injury impairs scapular retraction without a cutaneous sensory territory.
Suprascapular nerve~This supplies supraspinatus and infraspinatus, affecting initial abduction and external rotation without distal cutaneous sensory loss.
Musculocutaneous nerve~This supplies biceps-related elbow flexion and lateral forearm sensation, with biceps reflex involvement.
Axillary nerve~This supplies deltoid and teres minor and sensation over the lateral shoulder; it does not supply wrist extensors.
Radial nerve at the spiral groove~This can cause wrist/finger drop with dorsal radial hand sensory loss while relatively sparing triceps.
Posterior interosseous nerve~This radial motor branch affects finger/thumb extension without cutaneous sensory loss.
Superficial radial nerve~This is a sensory branch to the dorsoradial hand; injury does not cause motor weakness.
Median nerve at the carpal tunnel~This causes radial palmar digit sensory symptoms and thenar weakness while sparing forearm muscles and the palmar cutaneous branch.
Median nerve proximal to the elbow~A proximal median lesion can affect pronation, thumb/finger flexion, thenar muscles, and median sensory territories.
Anterior interosseous nerve~This motor median branch supplies FPL, radial FDP, and pronator quadratus; injury impairs the OK sign without cutaneous numbness.
Ulnar nerve at the elbow~This can affect hand intrinsics, FCU, and ulnar FDP with ulnar-hand sensory loss, depending on severity and precise site.
Ulnar nerve at the wrist~This affects distal ulnar hand functions and may spare FCU, ulnar FDP, and dorsal ulnar cutaneous sensation.
Femoral nerve~This supplies quadriceps and contributes to hip flexion, with anterior thigh/medial leg sensation and the patellar reflex.
Obturator nerve~This supplies thigh adductors with a small medial thigh sensory territory, without a reliable routine tendon reflex.
Sciatic nerve~This supplies hamstrings and most distal leg muscles through tibial and fibular divisions, with broad leg/foot deficits.
Common fibular nerve~This affects dorsiflexion and eversion with lateral leg/dorsal foot sensation; inversion and hip abduction are relatively spared.
Deep fibular nerve~This supplies dorsiflexors/toe extensors and the first dorsal web-space sensory territory.
Superficial fibular nerve~This supplies evertors and most dorsal foot sensation, sparing the first web space.
Tibial nerve~This supplies plantarflexion and inversion muscles with plantar foot sensation and Achilles reflex contribution.''')
block('dem','Named nerve localization','nerve','''45|Scapular retraction is weak after an injury involving rhomboids. There is no cutaneous sensory loss. Which nerve is most likely injured?|Dorsal scapular nerve|Rhomboid weakness localizes to dorsal scapular innervation when the deficit is isolated.
45|Isolated supraspinatus and infraspinatus weakness causes difficulty initiating abduction and externally rotating the shoulder. Which nerve is affected?|Suprascapular nerve|The suprascapular nerve supplies both muscles; deltoid weakness would suggest additional axillary or proximal involvement.
45|Elbow flexion and the biceps reflex are reduced, with lateral forearm numbness but preserved deltoid function. Which nerve is injured?|Musculocutaneous nerve|Musculocutaneous injury affects biceps and the lateral antebrachial cutaneous sensory continuation.
45|After a surgical-neck humerus fracture, shoulder abduction is weak and the lateral shoulder is numb. Which nerve is most likely injured?|Axillary nerve|The axillary nerve courses around the surgical neck and supplies deltoid and lateral shoulder skin.
45|A patient awakens after sleeping with an arm over a chair. Wrist and finger extension are weak, dorsal radial hand sensation is reduced, and elbow extension is preserved. Which lesion best fits?|Radial nerve at the spiral groove|Spiral groove radial injury can spare proximal triceps branches while impairing distal extensors and sensory branches.
45|Finger extension is weak, but cutaneous sensation is intact. Which isolated nerve lesion is most likely?|Posterior interosseous nerve|PIN is a motor radial branch; cutaneous dorsal hand sensation is mediated by a different branch.
45|The dorsoradial hand is numb after a tight wrist strap, but all extensor muscles are strong. Which nerve is affected?|Superficial radial nerve|An isolated superficial radial sensory neuropathy does not cause wrist or finger drop.
45|Nocturnal thumb, index, and middle finger paresthesias accompany thenar weakness. Forearm pronation is preserved. Which lesion best fits?|Median nerve at the carpal tunnel|Carpal tunnel compression affects distal median motor and digital sensory fibers while sparing proximal forearm muscles.
45|A patient cannot make a round OK sign because thumb IP and index DIP flexion are weak. Sensation is normal. Which branch is injured?|Anterior interosseous nerve|AIN supplies flexor pollicis longus and radial flexor digitorum profundus; its isolated lesion is motor only.
45|Median sensory loss accompanies weak pronation, thumb IP flexion, and thenar function. Which lesion is more likely than carpal tunnel syndrome?|Median nerve proximal to the elbow|Forearm median muscle weakness requires a lesion proximal to the carpal tunnel. AIN alone would not explain sensory loss.
45|Interossei, flexor carpi ulnaris, and fourth-fifth digit FDP are weak with ulnar-hand numbness. Which lesion best fits?|Ulnar nerve at the elbow|Involvement of ulnar forearm muscles favors an elbow/proximal lesion rather than isolated wrist compression.
45|Interossei are weak but FCU and ulnar FDP are preserved. Dorsal ulnar hand sensation is intact. Which lesion best fits?|Ulnar nerve at the wrist|A wrist-level lesion can spare proximal motor branches and the dorsal ulnar cutaneous branch that exits proximal to the wrist.
46|Knee extension and the patellar reflex are reduced, with medial leg numbness. Hip adduction remains normal. Which nerve is injured?|Femoral nerve|Femoral injury affects quadriceps and saphenous sensation; preserved adduction helps distinguish it from a broader lumbar plexus lesion.
46|Thigh adduction is weak and a small medial thigh area is numb, but knee extension is preserved. Which nerve is affected?|Obturator nerve|Obturator supplies adductors and a medial thigh sensory territory, whereas femoral supplies quadriceps.
46|After posterior hip trauma, hamstrings and most muscles below the knee are weak. Which nerve lesion best fits?|Sciatic nerve|A sciatic lesion can affect both tibial and fibular divisions plus hamstrings, unlike an isolated fibular head lesion.
46|Foot drop and weak eversion follow prolonged leg crossing. Inversion and hip abduction are preserved. Which nerve is compressed?|Common fibular nerve|This pattern localizes near the fibular head. Preserved inversion and hip abduction help distinguish it from L5 radiculopathy.
46|A patient has first dorsal web-space numbness and weak great toe extension. Which nerve territory is most specific?|Deep fibular nerve|Deep fibular innervation includes toe extensors and a small first web-space sensory territory.
46|Foot eversion is weak with dorsal foot numbness, but dorsiflexion and first web-space sensation are preserved. Which nerve is affected?|Superficial fibular nerve|Superficial fibular supplies evertors and most dorsal foot skin, sparing deep fibular territory.
46|Plantarflexion and inversion are weak with plantar foot numbness and a reduced Achilles reflex. Which nerve is injured?|Tibial nerve|Tibial innervation covers posterior compartment plantarflexors, tibialis posterior inversion, and plantar sensory branches.''')

custom('dem','Central versus peripheral localization','40,49','A patient has a truncal sensory level, leg hyperreflexia, and weakness below that level. Which localization is most likely?',[
'Spinal cord~A sensory level and upper motor neuron signs strongly support cord disease. Peripheral neuropathy more often produces distal loss and reduced reflexes.',
'Isolated carpal tunnel~A wrist median lesion cannot cause a truncal sensory level or leg hyperreflexia.',
'Neuromuscular junction~NMJ disorders do not cause a sensory level.',
'Lens~Lens pathology does not produce motor signs or a spinal sensory level.',
'Isolated muscle~Myopathy does not produce a defined sensory level.'])
custom('dem','Central versus peripheral localization','40,49','Which combined finding favors a CNS lesion over an uncomplicated distal peripheral neuropathy?',[
'Increased tone, brisk reflexes, and arm extensor/leg flexor predominant weakness~These are central pattern clues. Hemibody signs and a truncal sensory level also support CNS localization, though acute spinal shock can initially reduce reflexes.',
'Stocking-glove sensory loss and absent ankle jerks~This is a common peripheral length-dependent pattern.',
'Weakness confined to a named nerve~This favors peripheral nerve localization.',
'Isolated fatigable ptosis~This can reflect neuromuscular junction disease.',
'Only distal nerve pain at a pressure site~This more strongly suggests a peripheral lesion.'])
custom('dem','Neuropathy patterns','47,49','A length-dependent neuropathy begins in the toes and progresses up both legs. When do hand symptoms commonly appear?',[
'When leg sensory symptoms have advanced roughly to the knees~Length-dependent axonal loss affects the longest fibers first, then sufficiently long upper-limb fibers. This produces the stocking-glove pattern.',
'Before any toe symptoms in every case~That is not the usual length-dependent pattern.',
'Only after complete quadriplegia~Hand sensory involvement does not require severe motor paralysis.',
'Never because hand nerves are central~Hand peripheral nerves can be affected as disease advances.',
'Only if optic neuritis occurs~Optic neuritis is unrelated to length-dependent spread.'])
custom('dem','Neuropathy patterns','47,49','Painful asymmetric deficits sequentially affect several named nerves away from common entrapment sites. NCS is mainly axonal. Which pattern is present?',[
'Mononeuritis multiplex~Multifocal involvement of separate nerves suggests vasculitic or other multifocal neuropathy. MADSAM and HNPP are important demyelinating multifocal alternatives.',
'Typical symmetric length-dependent polyneuropathy~The asymmetric named-nerve pattern is different.',
'A single root lesion~One root cannot explain unrelated named nerves in several limbs.',
'A pure myopathy~Sensory nerve deficits and neuropathic pain favor nerve disease.',
'A single optic nerve lesion~This does not explain limb mononeuropathies.'])
custom('dem','Neuropathy patterns','48,49','A patient with ALS laughs or cries involuntarily without a matching sustained mood state. What is the appropriate term?',[
'Pseudobulbar affect~PBA is dysregulation of emotional expression rather than necessarily depression or mania. Cognitive and behavioral changes can also occur in ALS.',
'Major depression by definition~Involuntary expression alone does not establish a sustained depressive mood syndrome.',
'MOGAD optic neuritis~This does not describe an optic nerve inflammatory event.',
'A sensory neuronopathy~Deafferentation does not explain inappropriate emotional expression.',
'Normal voluntary laughter~The episodes are involuntary and disproportionate.'])
custom('dem','Neuropathy patterns','48,49','A man has painless flaccid weakness restricted to both proximal arms for 18 months. Which clinical phenotype is suggested?',[
'Brachial amyotrophic diplegia~This regional motor neuron phenotype can remain restricted for a prolonged period, although eventual spread or UMN signs can occur. Leg amyotrophic diplegia is a corresponding lower-limb phenotype.',
'Typical stocking-glove sensory neuropathy~The stem describes regional motor weakness without distal sensory loss.',
'An isolated ulnar neuropathy~One ulnar nerve cannot explain bilateral proximal arm weakness.',
'A mandatory acute GBS attack~The prolonged regional course is not typical acute monophasic GBS.',
'A symmetric primary myopathy by default~A regional motor neuron pattern requires evaluation rather than automatic attribution to muscle disease.'])
custom('dem','Neuropathy patterns','48,49','A febrile patient develops acute flaccid paralysis and encephalitis. Which infection is a recognized polio-like cause?',[
'West Nile virus~West Nile and certain enteroviruses can injure anterior horn/motor neuron systems and cause acute flaccid paralysis with or without encephalitis.',
'EBV as a proven universal cause of all paralysis~EBV association with MS does not make it the characteristic cause of this syndrome.',
'A lens crystallin aggregate~This is not an infection or motor neuron cause.',
'TSH receptor autoimmunity~This causes Graves disease, not febrile polio-like paralysis.',
'A germline RB1 variant~This is a cancer predisposition, not an infection.'])
custom('dem','Neuropathy patterns','49','Why is visual guidance helpful when testing apparent weakness in severe proprioceptive loss?',[
'It compensates for missing sensory feedback~Deafferentation can look like weakness or incoordination; seeing the limb may improve motor performance despite persistent sensory loss.',
'It instantly remyelinates peripheral nerves~Improvement is compensatory rather than structural repair.',
'It blocks AQP4 antibodies~Visual attention does not remove autoantibodies.',
'It raises ocular pressure~The mechanism is sensory compensation, not IOP change.',
'It proves all symptoms are functional~Organic deafferentation can improve with visual input.'])
custom('dem','Neuropathy workup','49,66','Which initial screening combination is appropriate for distal symmetric polyneuropathy?',[
'Glucose/HbA1c, vitamin B12, and SPEP with immunofixation~These screen for common metabolic and paraproteinemic causes. The lecture also includes lipid and hepatic assessment and consideration of genetic disease when appropriate.',
'Only a lumbar MRI in every patient~Imaging may be useful for selected radicular patterns but does not screen for common metabolic or paraproteinemic causes.',
'Only serum MOG-IgG in every patient~MOGAD is a CNS disease and indiscriminate testing can mislead.',
'Only a mildly elevated CSF protein~This is nonspecific and insufficient for a neuropathy diagnosis.',
'Nerve biopsy for every patient before blood tests~Biopsy is invasive and reserved for selected indications.'])
custom('dem','Neuropathy workup','49','Burning feet suggest small-fiber neuropathy, but routine NCS is normal. Which interpretation is best?',[
'Routine NCS can miss small-fiber disease~Standard studies assess larger myelinated fibers. A normal study also does not exclude pure sensory radiculopathy; testing should match the suspected tissue.',
'Normal NCS proves no neurologic disease exists~The test does not assess every fiber type or lesion location.',
'Normal NCS proves CIDP~CIDP usually requires supportive acquired demyelinating findings in an appropriate clinical pattern.',
'The symptoms must be caused by a cataract~Lens opacity cannot explain burning feet.',
'All sensory symptoms require abnormal motor CMAPs~Sensory disease can spare motor fibers.'])
custom('dem','Neuropathy workup','49','A spine MRI shows degenerative changes in a patient whose symptoms do not match that level. What is the best interpretation?',[
'Correlate imaging with the examination and electrophysiology~Degenerative findings occur in symptomatic and asymptomatic people. An anatomic abnormality is not automatically the cause of symptoms.',
'Any abnormal MRI proves the cause~Incidental abnormalities are common.',
'Ignore all MRI findings in every patient~MRI can be valuable in radiculopathy, CIDP roots, and Hirayama disease when clinically matched.',
'Diagnose MS from any degenerative disc~Disc degeneration is not a demyelinating plaque.',
'Treat all MRI changes with plasma exchange~Mechanical degeneration does not by itself justify immunotherapy.'])

custom('dem','Conduction physiology','50','Why does myelin permit rapid saltatory conduction?',[
'It limits membrane current leak so depolarization efficiently reaches the next node~Myelin increases membrane resistance and lowers effective capacitance across internodes. Regenerative action potentials occur at nodes of Ranvier.',
'It eliminates the need for axonal ion channels~Nodes still require voltage-gated channels.',
'It forces every internodal membrane segment to fire a full action potential~That describes continuous rather than saltatory conduction.',
'It converts motor axons into muscle fibers~Myelination does not change cell lineage.',
'It allows action potentials to travel through blood vessels~Signals propagate along axons, not vessel lumens.'])
custom('dem','Nerve conduction interpretation','51','How is motor conduction velocity calculated using two stimulation sites?',[
'Distance between sites divided by the difference in proximal and distal onset latencies~Subtracting distal from proximal latency largely removes the shared distal nerve, NMJ, and muscle delay, leaving conduction time for the intervening nerve segment.',
'CMAP amplitude divided by serum protein~These quantities do not measure conduction speed.',
'Distance from eye to cortex divided by P100 amplitude~This is unrelated to routine motor NCS velocity.',
'Proximal latency alone divided by distal amplitude~This does not isolate segment conduction time.',
'Number of fasciculations per minute~Fasciculations are not a velocity measurement.'])
custom('dem','Nerve conduction interpretation','52','NCS shows low CMAP and SNAP amplitudes with relatively preserved velocity and distal latency. Which process is favored?',[
'Axonal neuropathy~Loss of functioning axons reduces response amplitude. Surviving axons can conduct at near-normal speeds; marked nonuniform slowing suggests additional myelin dysfunction.',
'Pure demyelination with no axonal loss in every case~Primary demyelination more strongly affects velocity and latency, although amplitude can also fall from block or secondary axonal loss.',
'Normal study~Low amplitudes are abnormal when technical and physiologic factors are excluded.',
'Central optic neuritis~Peripheral motor and sensory response abnormalities do not localize to the optic nerve.',
'Cataract~Lens opacity does not reduce peripheral CMAPs or SNAPs.'])
custom('dem','Nerve conduction interpretation','52,63','NCS shows prolonged distal motor latencies, marked conduction slowing, and temporal dispersion across multiple nerves. Which process is favored?',[
'Acquired demyelinating neuropathy~Marked slowing and dispersion support myelin dysfunction when thresholds, temperature, amplitudes, and entrapment confounders are considered. Clinical context determines whether CIDP or another disorder is present.',
'Isolated lens opacity~Cataract does not affect limb nerve conduction.',
'Pure muscle disease as the only explanation~Myopathy does not generally cause this widespread demyelinating nerve pattern.',
'Normal peripheral conduction~These are abnormal findings.',
'Typical isolated cortical stroke~CNS lesions do not generally cause diffuse peripheral demyelinating NCS changes.'])
custom('dem','Nerve conduction interpretation','52,61,63','Proximal stimulation produces a much smaller CMAP than distal stimulation across a non-entrapment segment. What does this suggest?',[
'Conduction block~Some axons fail to conduct through the intervening segment. Block supports acquired nerve dysfunction, but technical factors and nodal axonal GBS variants must also be considered.',
'Increased motor unit recruitment by definition~Recruitment is assessed with voluntary needle EMG, not this response comparison.',
'Normal sensory receptor adaptation~This is a motor nerve conduction finding.',
'A retinal microaneurysm~Retinal vascular changes do not explain a segmental motor block.',
'Automatic proof of ALS~Conduction block instead raises concern for treatable motor or demyelinating neuropathies.'])
custom('dem','Needle EMG interpretation','53','What should a healthy relaxed muscle usually show after insertional activity has settled?',[
'Electrical silence~Persistent fibrillations or positive sharp waves are abnormal spontaneous single-fiber activity. Interpretation must consider insertion, endplate activity, and sampling.',
'Continuous fibrillation potentials~Fibrillations suggest denervation or some myopathies rather than normal resting activity.',
'Giant voluntarily activated motor units without effort~Motor unit activation requires contraction; giant units can reflect chronic reinnervation.',
'A maximal interference pattern at rest~An interference pattern occurs with voluntary recruitment.',
'A visual P100 response~P100 belongs to visual evoked potentials.'])
custom('dem','Needle EMG interpretation','53','Needle EMG shows fibrillations and positive sharp waves. Which interpretation is best?',[
'Active muscle fiber instability, often from denervation or myopathy~These are spontaneous single-fiber discharges. They are not specific to ALS and must be interpreted with distribution and other findings.',
'Definite ALS regardless of examination~Many neurogenic and myopathic disorders can show these potentials.',
'Normal maximal contraction~They are abnormal spontaneous resting activity.',
'A specific diagnostic marker of cataract~They are muscle electrical findings.',
'Proof of normal neuromuscular transmission~They do not establish normal NMJ function.'])
custom('dem','Needle EMG interpretation','53','Large long-duration polyphasic motor units with reduced recruitment suggest what process?',[
'Chronic denervation with collateral reinnervation~Surviving motor axons sprout to supply additional fibers, enlarging motor units. Giant units can take a long time to develop in chronic neuropathy or post-polio states.',
'A pure acute lens disorder~Lens pathology does not alter motor unit morphology.',
'Normal myelination in every case~The pattern indicates chronic neurogenic remodeling rather than simply normal myelin.',
'Only early uncomplicated myopathy~Myopathies more often show small short-duration units with early recruitment, though overlap exists.',
'New retinal vessels~Motor unit waveforms do not reflect retinal angiogenesis.'])
custom('dem','NMJ electrophysiology','55','Which electrophysiologic pattern most supports LEMS over MG?',[
'A marked CMAP increment after exercise or high-frequency stimulation~Presynaptic calcium accumulation can transiently improve transmitter release in LEMS. MG more typically shows low-frequency decrement.',
'Only a low-frequency decrement with normal postexercise amplitude~This may occur in MG and is less specific for LEMS.',
'Diffuse sensory SNAP loss~An NMJ disorder does not primarily destroy sensory axons.',
'A decrement alone proves LEMS rather than MG~Low-frequency decrement can occur in MG; marked increment is the more useful presynaptic clue.',
'Delayed P100 latency~This assesses optic pathway conduction rather than NMJ facilitation.'])

custom('dem','GBS recognition','58,59,61','Which time course best fits classic monophasic GBS?',[
'Progressive weakness reaching nadir within four weeks, followed by a plateau and recovery~GBS is acute. Recovery may take weeks to months, and residual pain, fatigue, weakness, or paresthesias can persist.',
'Steady worsening for six months before nadir~This is more consistent with a chronic neuropathy such as CIDP.',
'A decade of continuous disability without acute onset~This is not the classic GBS course.',
'Only one second of weakness with complete immediate recovery~This is not the typical progressive neuropathic syndrome.',
'Only isolated visual blur over years~This does not describe acute polyradiculoneuropathy.'])
custom('dem','GBS recognition','58,60,61','Which finding casts doubt on uncomplicated GBS and should prompt a search for an alternative diagnosis?',[
'A sharp truncal sensory level and marked persistent asymmetry~A sensory level suggests spinal cord disease, while marked persistent asymmetry, early persistent sphincter dysfunction, or substantial CSF leukocytosis are warning signs.',
'Symmetric weakness with reduced reflexes~These are core supportive GBS features.',
'Recent diarrheal illness~An antecedent infection is common.',
'Mild sensory symptoms~These can occur in GBS.',
'Autonomic instability~This can be a major GBS complication.'])
custom('dem','GBS recognition','60','A patient with acute neuropathic weakness also has severe abdominal pain and dark urine after a new medication. Which mimic should be considered?',[
'Acute intermittent porphyria~Porphyria can cause an acute motor-predominant neuropathy with abdominal and autonomic symptoms. GBS mimics also include toxic, metabolic, infectious, and vasculitic neuropathies.',
'Dry AMD~Macular degeneration does not explain acute neuropathy with abdominal symptoms.',
'Cataract~Lens opacity is unrelated to this motor-autonomic syndrome.',
'Primary open-angle glaucoma~Glaucoma does not explain limb paralysis and abdominal pain.',
'Retinoblastoma~This childhood retinal tumor is not the described systemic mimic.'])
custom('dem','GBS CSF','58,61','Which CSF pattern is most characteristic of GBS?',[
'Elevated protein with few cells~Albuminocytologic dissociation supports GBS, although CSF can be normal early. Marked pleocytosis should trigger evaluation for infectious, malignant, or other causes.',
'Hundreds of neutrophils with very low glucose as the typical finding~This suggests infection rather than classic GBS.',
'A mandatory positive AQP4-IgG result~AQP4 antibodies support NMOSD, not GBS.',
'A mandatory positive MOG-IgG result~MOGAD is a CNS disorder.',
'Zero protein in all cases~This is not the characteristic CSF finding.'])
custom('dem','GBS CSF','61','A patient thought to have GBS has CSF with 120 leukocytes/mm3. What is the best interpretation?',[
'Reconsider the diagnosis and investigate alternatives~The lecture flags counts above 50/mm3 as a warning. Mild pleocytosis can occur, but substantial leukocytosis raises concern for infection or another inflammatory process.',
'This is required for definite GBS~GBS typically shows few cells despite elevated protein.',
'It proves uncomplicated CIDP~CIDP also generally has albuminocytologic dissociation, not marked leukocytosis.',
'It excludes all infection~Pleocytosis can be an infectious clue.',
'No additional evaluation is needed~The atypical result warrants reassessment.'])
custom('dem','GBS electrophysiology','61','A patient has classic early GBS but nearly normal initial NCS. What is the best next interpretation?',[
'Early studies can be nondiagnostic; repeat electrophysiology if needed~Proximal/root abnormalities and evolving disease may not be obvious initially. F-wave changes can be informative; a normal early study does not safely exclude GBS.',
'Normal initial NCS definitively excludes GBS~Electrodiagnostic sensitivity depends on timing and pattern.',
'The patient must have a cataract~Lens disease does not explain acute areflexic weakness.',
'Begin chronic CIDP labeling solely because the first NCS is normal~Time course and repeat assessment are needed.',
'Only sensory retinal testing can confirm GBS~GBS is a peripheral nerve/root disorder.'])
custom('dem','GBS variants','61','A patient has ophthalmoplegia, ataxia, and areflexia after infection. Which GBS-spectrum syndrome is most likely?',[
'Miller Fisher syndrome~The triad is classic for Miller Fisher syndrome, often associated with anti-GQ1b antibodies. Related Bickerstaff brainstem encephalitis can add impaired consciousness or hyperreflexia.',
'Typical ALS~ALS does not usually present with acute postinfectious ophthalmoplegia and ataxia.',
'Pure motor CIDP~The acute ocular-ataxic triad is more specific for Miller Fisher syndrome.',
'Dry AMD~This does not cause areflexia or ophthalmoplegia.',
'Carpal tunnel syndrome~A median wrist lesion cannot explain the triad.'])
custom('dem','GBS variants','61','A patient with postinfectious ophthalmoplegia and ataxia also has impaired consciousness and brisk reflexes. Which related syndrome is favored?',[
'Bickerstaff brainstem encephalitis~Altered consciousness or hyperreflexia points toward the Bickerstaff end of the anti-GQ1b spectrum rather than isolated classic Miller Fisher syndrome.',
'Uncomplicated distal diabetic neuropathy~This does not explain acute brainstem signs and altered consciousness.',
'Isolated ulnar neuropathy~A focal peripheral nerve lesion cannot produce this syndrome.',
'Cataract~Lens opacity does not cause brainstem dysfunction.',
'Pure sensory CIDP~The acute encephalopathic ophthalmoplegic syndrome is different.'])
custom('dem','GBS variants','7,61','An acute pure motor neuropathy shows reversible nodal conduction failure without temporal dispersion or other demyelinating features. Which GBS subtype is favored?',[
'Acute motor axonal neuropathy~AMAN may show reversible conduction failure at nodes before axonal degeneration. Conduction block alone should not automatically be interpreted as demyelination.',
'Acute inflammatory demyelinating polyradiculoneuropathy~AIDP typically has broader demyelinating features such as slowing, prolonged latencies, and dispersion.',
'Acute motor-sensory axonal neuropathy~AMSAN also involves sensory axons, which are spared in the stated pure motor syndrome.',
'Typical MS~MS is CNS disease and does not cause this peripheral nodal pattern.',
'Isolated MG~MG is an NMJ disorder rather than a motor axonal neuropathy.'])
custom('dem','GBS respiratory care','61','A patient with GBS has rapidly declining respiratory measurements and weak cough but normal oxygen saturation. What should guide management?',[
'Urgent monitored assessment for impending ventilatory failure~Oxygen saturation can remain normal early in neuromuscular respiratory failure. Serial respiratory mechanics, bulbar function, cough, and clinical trajectory inform timely airway support.',
'Normal oxygen saturation excludes respiratory risk~Ventilatory weakness can precede hypoxemia.',
'Wait until respiratory arrest to intubate~Anticipatory care is essential.',
'Treat only with bronchodilators~The primary problem is neuromuscular weakness rather than bronchospasm.',
'Discharge because GBS never affects breathing~A substantial minority require ventilation.'])
custom('dem','GBS treatment','61','Which immunotherapy approach is supported for significant GBS?',[
'IVIg or plasma exchange, with no routine added benefit from combining both~Both hasten recovery and have similar efficacy in trials. Supportive respiratory, autonomic, pain, and rehabilitation care remains essential; corticosteroids alone are not effective GBS treatment.',
'Corticosteroids alone as the preferred proven therapy~Unlike CIDP, GBS has not shown benefit from corticosteroids as standard treatment.',
'Routine IVIg plus PLEX for every case because effects always add~Trials do not show routine added benefit, and PLEX can remove administered immunoglobulin.',
'Long-term oral azathioprine as the only acute rescue~Its delayed immunosuppressive action is not an established substitute for IVIg or PLEX in acute GBS.',
'No monitoring because immunotherapy immediately reverses paralysis~Recovery is variable and acute complications remain possible.'])
custom('dem','GBS outcomes and triggers','61','A recovered patient remains fatigued with neuropathic pain and paresthesias. Which interpretation is most accurate?',[
'Residual symptoms are common after GBS~Recovery can be prolonged and incomplete despite treatment. Prognostic models use clinical strength and severity measures, but individual trajectories vary.',
'Residual symptoms prove all initial treatment was inappropriate~Incomplete recovery does not establish treatment failure or wrong diagnosis.',
'All patients regain normal function in one day~This is inconsistent with GBS recovery.',
'Pain excludes any prior GBS~Pain can occur during and after GBS.',
'Residual fatigue alone proves recurrent active demyelination~Persistent symptoms can reflect incomplete recovery; a new relapse requires clinical reassessment rather than fatigue alone.'])
custom('dem','GBS outcomes and triggers','61','Which statement about infection and vaccination best reflects the evidence emphasized in the lecture?',[
'Influenza infection carries greater GBS risk than influenza vaccination; future vaccination requires individualized assessment~A history temporally related to a vaccine warrants review of timing and specific vaccine guidance. The slide\'s blanket instruction to never repeat vaccination is too broad.',
'Every vaccination commonly causes GBS~GBS following vaccination is rare and risk depends on vaccine and context.',
'Influenza infection has no association with GBS~The lecture emphasizes a larger infection-associated risk.',
'All vaccines are permanently forbidden after any neuropathy~That is not a justified universal rule.',
'Campylobacter infection inevitably produces GBS~Only a small fraction of infections lead to GBS.'])

pool('CIDPvariant','''Typical CIDP~Symmetric proximal and distal weakness, large-fiber sensory loss, and areflexia with chronic acquired demyelination characterize typical CIDP.
Acute-onset CIDP~CIDP may initially mimic GBS; continued deterioration beyond eight weeks or repeated relapses after the acute phase prompts reassessment.
Sensory CIDP~Sensory-predominant symptoms, ataxia, and reduced reflexes can occur, with electrophysiologic evidence supporting peripheral demyelination.
Chronic immune sensory polyradiculopathy~CISP can produce sensory ataxia from proximal root involvement despite normal routine distal NCS; SSEPs, CSF, and root MRI may help.
Motor CIDP~A symmetric motor-predominant acquired demyelinating neuropathy can occur without prominent sensory symptoms; IVIg is often favored over steroids.
MADSAM or multifocal CIDP~Asymmetric sensory and motor demyelinating deficits in multiple nerves, often upper-limb predominant, fit multifocal CIDP/Lewis-Sumner syndrome.
Anti-MAG distal acquired demyelinating symmetric neuropathy~Distal sensory-predominant demyelination with IgM paraprotein and anti-MAG antibodies is a distinct paraproteinemic neuropathy and often treatment-refractory.
Multifocal motor neuropathy~Asymmetric pure motor named-nerve weakness with conduction block and preserved sensory studies favors MMN, generally treated with IVIg.
Autoimmune nodopathy~Antibodies to nodal/paranodal adhesion proteins define a distinct category, often with poor IVIg response and selected benefit from B-cell-directed therapy.
POEMS syndrome~Polyneuropathy with organomegaly, endocrinopathy, monoclonal plasma cell disorder, and skin changes should prompt a systemic plasma-cell disorder evaluation.''')
block('dem','CIDP spectrum','CIDPvariant','''57,62,64,65,66|A patient has four months of symmetric proximal and distal weakness, vibration loss, and areflexia. Acquired demyelination is demonstrated in multiple nerves. Which phenotype fits?|Typical CIDP|This is the classic sensorimotor phenotype. The lecture estimates roughly half of cases are typical; mimics must be excluded before assigning the diagnosis.
57,62,65|A patient initially labeled GBS continues to deteriorate ten weeks after onset and then has another relapse. Which diagnosis must be reconsidered?|Acute-onset CIDP|Acute-onset CIDP can initially resemble GBS. Deterioration beyond eight weeks and recurrent worsening warrant reconsideration of a chronic inflammatory course.
62,64|A patient develops prominent sensory ataxia and reduced reflexes, with little weakness but acquired demyelinating abnormalities on NCS. Which phenotype fits?|Sensory CIDP|Sensory CIDP is a sensory-predominant variant. Distal sensory neuropathy and central dorsal column disease remain important alternatives.
57,62|Severe sensory ataxia occurs despite normal routine distal NCS. SSEPs, elevated CSF protein, and lumbar root abnormalities support proximal sensory root disease. Which syndrome fits?|Chronic immune sensory polyradiculopathy|CISP affects proximal sensory roots, so routine distal studies can be normal. It is generally discussed as a related immune sensory syndrome rather than automatically equivalent to typical CIDP.
62,64|A patient has symmetric proximal and distal weakness with acquired demyelinating studies but no important sensory symptoms. Which CIDP variant fits?|Motor CIDP|Motor CIDP is a symmetric motor-predominant phenotype. Immunoglobulin is often preferred because corticosteroids can worsen some motor-predominant cases.
57,62,64|A patient has asymmetric distal upper-limb weakness and numbness affecting multiple nerves, with acquired demyelination. Which CIDP phenotype is most likely?|MADSAM or multifocal CIDP|MADSAM includes both motor and sensory involvement. MMN is motor-only and therefore less suitable when objective sensory abnormalities are present.
57,62,65|An older man has slowly progressive distal sensory ataxia and tremor, prolonged distal latencies, an IgM monoclonal protein, and anti-MAG antibodies. Which diagnosis fits?|Anti-MAG distal acquired demyelinating symmetric neuropathy|Anti-MAG neuropathy is strongly associated with an IgM paraprotein and distal sensory-predominant demyelination. It often responds less well to typical CIDP therapies.
57,65,67|A patient has severe sensory ataxia, tremor, distal weakness, and neurofascin-155 IgG4 antibodies with poor IVIg response. Which category is most appropriate?|Autoimmune nodopathy|Nodal/paranodal antibody-defined disorders are now separated from conventional CIDP. Selected patients may respond to rituximab or other antibody-directed approaches.
49,66|A demyelinating neuropathy is accompanied by organomegaly, skin changes, endocrinopathy, and a monoclonal plasma-cell disorder. Which diagnosis should be considered?|POEMS syndrome|The systemic cluster is characteristic of POEMS and should not be treated as routine CIDP without evaluating the plasma-cell disorder.''')
custom('dem','CIDP diagnosis','63,65','Which evidence is most important before diagnosing CIDP?',[
'A compatible clinical course plus convincing acquired demyelinating electrodiagnostic findings~Multiple formal criteria exist, but clinical pattern and properly performed NCS are central. Modest CSF protein elevation alone is a common source of overdiagnosis.',
'Any mild CSF protein increase regardless of symptoms~This is nonspecific and insufficient.',
'A single slowed nerve across a common entrapment site~Entrapment alone does not establish generalized CIDP.',
'Only patient-reported fatigue~Fatigue without objective compatible findings is not enough.',
'A normal sensory examination proves CIDP in all cases~CIDP phenotypes vary, but a normal sensory exam does not itself establish a diagnosis.'])
custom('dem','CIDP diagnosis','63','A cold hand produces prolonged distal latencies and slowed conduction. What should be done before attributing this to CIDP?',[
'Warm the limb and verify technical factors and accepted thresholds~Temperature, measurement error, amplitude-dependent slowing, entrapment, and diabetes can create misleading findings. The lecture warns against equivocal slowing and unsupported block calls.',
'Diagnose definite CIDP immediately~Cold-induced slowing is a confounder.',
'Ignore all nerve conduction data forever~Technically adequate NCS remains essential.',
'Use CSF protein alone instead~This can compound overdiagnosis.',
'Label block from an equivocal amplitude change without checking stimulation~Submaximal stimulation and other technical factors can falsely suggest block.'])
custom('dem','CIDP diagnosis','63','Which finding is an electrophysiologic pitfall rather than convincing standalone evidence for CIDP?',[
'Slowing confined to a common compression site~Focal entrapment can slow conduction without generalized acquired demyelination. Markedly low amplitudes and cold limbs also complicate interpretation.',
'Marked nonuniform slowing in several non-entrapment segments~This can support acquired demyelination in an appropriate clinical context.',
'Convincing temporal dispersion in multiple nerves~This may support demyelination when technical criteria are satisfied.',
'Reproducible block outside entrapment sites~This can support acquired nerve dysfunction when interpreted correctly.',
'Multiple appropriately measured prolonged F-wave latencies~This may support proximal demyelinating abnormalities in context.'])
custom('dem','CIDP diagnosis','65','What does a sural-sparing pattern mean in an acquired inflammatory neuropathy evaluation?',[
'Relative preservation of the sural sensory response despite abnormal upper-limb sensory responses~This pattern can support inflammatory demyelinating neuropathy, including GBS or CIDP, but is neither required nor independently diagnostic.',
'Normal motor responses with absent sensation in every nerve~That is not the definition.',
'Selective optic nerve preservation~The sural nerve is a peripheral leg sensory nerve.',
'A completely normal study in all nerves~Sural sparing is a relative pattern of abnormal and preserved responses.',
'Proof of a neuromuscular junction disorder~The pattern involves sensory nerve responses rather than NMJ transmission.'])
custom('dem','CIDP diagnosis','65','Does a patient with typical clinical CIDP and convincing acquired demyelinating NCS always need nerve biopsy?',[
'No; biopsy is reserved for selected uncertain or alternative diagnoses~Routine biopsy is not necessary when clinical and NCS evidence is convincing. Vasculitis or infiltrative disease may create a separate biopsy indication.',
'Yes, before any treatment in every case~This adds unnecessary invasive testing to an otherwise supported diagnosis.',
'Yes, because NCS never detects demyelination~NCS is central to CIDP assessment.',
'No tests are needed for any patient with fatigue~The question assumes objective compatible findings; fatigue alone is insufficient.',
'A biopsy is mandatory because mild CSF protein elevation is diagnostic~Mild protein elevation is nonspecific and does not create a universal biopsy requirement.'])
custom('dem','CIDP treatment','62,65','Which treatment set is appropriate for typical CIDP?',[
'Immunoglobulin, corticosteroids, and selected plasma exchange~IVIg or subcutaneous immunoglobulin and corticosteroids are major therapies; PLEX is effective but long-term access/logistics can limit use. This differs from GBS, where steroids are not effective standard treatment.',
'Corticosteroids are ineffective in every CIDP phenotype because they fail in GBS~Treatment evidence differs between chronic CIDP and acute GBS; motor phenotypes require additional nuance.',
'Antibiotics alone in all cases~Typical CIDP is immune-mediated and is not treated as a persistent bacterial nerve infection.',
'Acetylcholinesterase inhibition as the sole disease-modifying treatment~This can improve MG transmission but does not treat CIDP demyelination.',
'All patients must take lifelong IVIg without reassessment~Some stable patients can reduce or discontinue treatment with monitoring.'])
custom('dem','CIDP treatment','65','A stable patient has received maintenance IVIg for CIDP for years. Which approach is reasonable?',[
'Periodically reassess disease activity and consider supervised dose reduction or withdrawal~Some patients can discontinue without relapse. The lecture\'s approximate rate is cohort-dependent and does not justify abrupt cessation in every patient.',
'Never reassess because all patients are permanently IVIg-dependent~Dependence varies and overtreatment can occur.',
'Stop abruptly in every patient based on one statistic~Withdrawal should be individualized and monitored.',
'Use permanent high-dose steroids without safety review~Long-term steroid toxicity and ongoing disease activity require reassessment.',
'Use a positive serum MOG test as the only withdrawal criterion~MOGAD testing does not determine CIDP IVIg dependence.'])
custom('dem','Nodo-paranodopathies','9,67','Which target is a Schwann-cell paranodal protein associated with tremor, sensory ataxia, and frequent IVIg refractoriness?',[
'Neurofascin-155~NF155 is a glial paranodal adhesion protein. IgG4-associated disease can respond better to B-cell-directed treatment than IVIg in selected patients.',
'Neurofascin-186~NF186 is a nodal axonal isoform involved in sodium channel organization, rather than the specified glial paranodal target.',
'Contactin-1~CNTN1 is an axonal paranodal adhesion molecule; nephrotic syndrome has been reported.',
'CASPR1~CASPR1 is an axonal paranodal protein; severe neuropathic pain is a described clue.',
'Aquaporin-4~AQP4 is an astrocytic CNS water channel, not the Schwann paranodal protein.'])
custom('dem','Nodo-paranodopathies','9,67','Which antibody target is an axonal nodal neurofascin isoform involved in sodium channel clustering?',[
'Neurofascin-186~NF186 and NF140 are axonal nodal isoforms, unlike glial paranodal NF155. Nodal disorders can have motor, sensory, and cranial manifestations.',
'Neurofascin-155~NF155 is the glial paranodal isoform.',
'MOG~MOG is an outer CNS myelin protein, not a peripheral nodal neurofascin isoform.',
'AQP4~AQP4 is an astrocyte water channel.',
'RB protein~RB regulates the cell cycle, not nodal adhesion.'])
custom('dem','Nodo-paranodopathies','67','A patient has severe neuropathic pain, distal weakness, and an IVIg-refractory antibody-mediated paranodal disorder. Which target is highlighted by that painful phenotype?',[
'CASPR1~Contactin-associated protein 1 is a paranodal axonal adhesion protein. Severe neuropathic pain is a notable reported feature; phenotype is suggestive rather than perfectly specific.',
'Lens crystallin~Crystallin aggregation causes cataracts rather than nodopathy.',
'TSH receptor~This is associated with Graves disease and thyroid ophthalmopathy.',
'ACh receptor~This is a postsynaptic NMJ target and does not cause a sensory painful neuropathy.',
'VEGF receptor alone~This does not identify the antibody-defined nodopathy.'])
custom('dem','Nodo-paranodopathies','67','Sensory ataxia and motor weakness with nephrotic syndrome accompany an IgG4 paranodal antibody. Which target is a recognized association?',[
'Contactin-1~CNTN1 autoimmunity can be associated with motor-predominant neuropathy, ataxia, nephrotic syndrome, and IVIg resistance. NF140/186 disease can also have renal associations; the antibody assay resolves overlap.',
'BRAF~BRAF is an oncogenic pathway component rather than a paranodal antibody target.',
'PMP22 deletion~This is a hereditary pressure-palsy mechanism, not an IgG4 autoimmune renal association.',
'GALC~GALC deficiency causes Krabbe disease.',
'ABCD1~ABCD1 variants cause adrenoleukodystrophy.'])

block('eye','Extended clinical vignettes','eyeDx','''4,59|A 34-year-old woman presents with palpitations, heat intolerance, and six months of increasing eye prominence. She reports gritty eyes on waking and cannot fully close her eyelids during sleep. Examination shows bilateral proptosis and restricted eye movements. Thyroid testing demonstrates suppressed TSH and elevated free thyroxine. Imaging shows enlarged extraocular muscles and increased orbital soft tissue. The clinical photograph is shown. Which disorder best explains the eye findings and risk of exposure-related corneal injury?|Thyroid ophthalmopathy|Orbital inflammation, matrix deposition, fat expansion, and eventual extraocular muscle fibrosis explain Graves ophthalmopathy. Incomplete lid closure exposes and dries the cornea; lubrication and protection are important while severity-specific treatment is evaluated.|figure-eye-59
5,6,7,8,60|A 69-year-old man with diabetes and atopic dermatitis reports a year of worsening vision. Headlights produce glare, colors appear faded, and he needs more illumination to read. He has no eye pain, flashes, floaters, or curtain-like field defect. Years earlier he received prolonged oral prednisone for severe dermatitis. His fundus is difficult to visualize because of an opacity in the optical media, shown here. Which diagnosis best unifies the gradual symptoms, examination, and multiple risk factors?|Cataract|A lens opacity explains painless blur, glare, poor night vision, and faded colors. Age, diabetes, corticosteroids, and atopic dermatitis are relevant risks. Galactosemia, Wilson disease, trauma, and radiation are additional lecture associations.|figure-eye-60
9,12,15,16,62|A 64-year-old woman comes for an examination because she has started bumping into furniture. She can still read the central letters on an eye chart. She denies pain, redness, or abrupt visual loss. Automated fields show bilateral peripheral defects; gonioscopy demonstrates open angles. The optic disc appearance is shown. Her mother lost vision late in life. Which diagnosis explains the preserved early central acuity despite progressive peripheral loss and the structural disc change?|Primary open-angle glaucoma|Chronic glaucomatous ganglion cell and axon loss causes peripheral field defects and cupping. The angle remains open but aqueous outflow resistance is elevated; pressure reduction helps prevent further irreversible damage.|figure-eye-62
23,24,27,64|A 79-year-old woman has gradually increasing difficulty reading and recognizing faces. She continues to navigate around the house using peripheral vision. She denies eye pain or a sudden curtain. Examination shows yellow-white macular deposits, patches of pigment alteration, and irregular islands of atrophy. No fresh blood or neovascular membrane is identified. She asks whether cataract surgery will correct the central blind spots. Which diagnosis best localizes the primary disease responsible for these findings?|Dry age-related macular degeneration|The macular deposits are drusen, and the atrophic changes involve RPE and associated photoreceptors. Cataract surgery cannot reverse established macular atrophy. Follow-up matters because dry disease can progress or become neovascular.|figure-eye-64
25,26,27,65|An 83-year-old man previously monitored for drusen reports that lines on the doorframe became wavy over several days. A dark central spot now interferes with reading. Peripheral navigation remains possible, and there is no severe ocular pain. The fundus photograph shows yellow material and a hemorrhagic macular lesion. Angiographic testing demonstrates leakage from an abnormal vascular membrane. Which diagnosis explains the change from a slowly progressive disorder to rapid central visual deterioration?|Wet age-related macular degeneration|Conversion to VEGF-driven choroidal neovascularization causes fluid and blood leakage at the macula. Early anti-VEGF treatment can limit damage, although established scar or atrophy may constrain recovery.|figure-eye-65
28,29,30,31,32,33,66|A 57-year-old man has a pigmented choroidal lesion discovered during a routine examination. Over several years the mass enlarges and breaks through Bruch membrane, detaching overlying retina. Biopsy shows atypical epithelioid and spindle melanocytic cells. Molecular testing identifies a G-protein pathway driver. He undergoes local radiotherapy and is advised to continue systemic surveillance despite stable ocular findings. Which diagnosis best explains the morphology, genetics, and concern for delayed hematogenous metastasis?|Uveal melanoma|Uveal melanoma commonly arises in choroid, can grow through Bruch membrane, and often harbors GNAQ/GNA11 rather than characteristic cutaneous BRAF drivers. Liver metastasis is a major long-term risk.|figure-eye-66
34,35,36,39,67,68|A 68-year-old man develops a shower of floaters and intermittent flashes in one eye. Earlier that morning he noticed only moving specks, but by evening a dark curtain extends from the periphery toward the center. Dilated examination identifies a retinal break and the elevated folded tissue pictured. The ophthalmologist explains that an age-related vitreous separation likely exerted traction and created the break. Which current diagnosis best explains the curtain and requires time-sensitive retinal repair?|Retinal detachment|The curtain and detached folded neural retina indicate retinal detachment complicating PVD. A tear permits vitreous fluid under the retina in rhegmatogenous detachment; photoreceptor degeneration makes repair urgent.|figure-eye-68
40,41,43,44,45,69|A 52-year-old with longstanding poorly controlled diabetes missed several retinal screening visits. He now has sudden painless visual obscuration after months of intermittent floaters. Fundus examination reveals abnormal new vessels at the disc and elsewhere, and ultrasound confirms vitreous hemorrhage. Fibrovascular tissue is exerting traction on the retina. Which stage of diabetic eye disease accounts for the fragile vessels and the risk of tractional detachment, rather than simply capillary microaneurysms?|Proliferative diabetic retinopathy|Retinal ischemia stimulates VEGF and neovascularization. Fragile vessels bleed and associated fibrovascular proliferation can contract; anti-VEGF, laser, and surgery have roles depending on the complication.|figure-eye-69
50,51,52,73|A 36-year-old woman reports weeks of headache that worsens when lying down, pulsatile tinnitus, and brief episodes of dimmed vision. Her corrected visual acuity is initially close to normal. The fundus photograph shows a swollen hyperemic optic disc with indistinct margins, and the other eye has a similar finding. The clinician arranges urgent evaluation of intracranial pressure and its cause before deciding whether lumbar puncture is appropriate. What is the specific term for this pressure-related disc appearance?|Papilledema|Papilledema is disc swelling due to raised ICP. Preserved initial central acuity does not remove the urgency. Imaging and cause-directed management distinguish mass lesions, venous causes, and idiopathic intracranial hypertension.|figure-eye-73
53,54,55,56,74|Parents bring a 19-month-old child because one eye appears white in flash photographs and has begun turning inward. Examination reveals the cream-colored retinal lesion pictured; imaging identifies intratumoral calcification. There is no known family history. Genetic counseling is arranged because the clinician explains that absence of affected relatives does not exclude a new germline tumor-predisposition variant. Which diagnosis best accounts for the child's age, leukocoria, strabismus, and calcified intraocular mass?|Retinoblastoma|Retinoblastoma can be sporadic or heritable, including de novo germline RB1 variants. Early intraocular treatment has a high cure rate; laterality and family history alone cannot establish whether a case is heritable.|figure-eye-74''')

block('dem','MRI clinical vignettes','neuroDx','''11,12,19,34|A 46-year-old woman has profound painful visual loss with little recovery after an earlier similar episode. She also recalls several days of otherwise unexplained hiccups and vomiting. The shown MRI includes posterior optic pathway and chiasmal enhancement. Spinal imaging subsequently identifies a long central cord lesion. Serum testing using a cell-based assay detects AQP4-IgG. Which disorder best explains the combination of optic nerve distribution, brainstem symptoms, and the antibody-defined mechanism of injury?|AQP4-IgG neuromyelitis optica spectrum disorder|Posterior optic nerve/chiasm disease, area postrema symptoms, and longitudinally extensive myelitis are characteristic NMOSD clues. AQP4 antibodies target astrocytes, and severe attacks can leave major residual disability.|figure-optic-a
11,12,20,34|A 12-year-old develops painful loss of vision in both eyes after a respiratory illness. Both optic discs are swollen. MRI shows extensive anterior optic nerve signal and enhancement around the nerves, as illustrated. The chiasm is relatively spared. Serum AQP4-IgG is negative, but a high-titer cell-based MOG-IgG assay is positive. The child improves after prompt corticosteroid treatment, and a taper is planned to reduce early recrudescence. Which antibody-associated disorder best fits this pattern?|MOG antibody-associated disease|Bilateral anterior optic neuritis with perineural enhancement and disc edema favors MOGAD. High-titer serum testing in this fitting phenotype is meaningful; low-titer results in inappropriate screening are less reliable.|figure-optic-mog
11,12,18,27|A 26-year-old develops pain on eye movement and reduced color saturation in one eye. The MRI shows a relatively short intraorbital optic nerve lesion. She later develops a separate brainstem syndrome, and brain imaging shows characteristic ovoid periventricular plaques. CSF-restricted oligoclonal bands persist. AQP4-IgG and MOG-IgG testing is negative. Which diagnosis is most consistent with the optic nerve pattern and the subsequent evidence of CNS disease in characteristic separate locations?|Multiple sclerosis|Typical unilateral short-segment optic neuritis can be part of MS. The later clinical event, characteristic MRI locations, and intrathecal synthesis support the diagnosis after exclusion of better explanations.|figure-optic-ms
11,13,14,19|A 39-year-old has a severe episode of bilateral leg weakness, urinary retention, and a sensory level. MRI demonstrates a long central cervical cord lesion, shown here. She previously had an episode of severe optic neuritis. Serum AQP4-IgG is positive. The clinician explains that disability often accumulates through attacks with incomplete recovery rather than a continuously progressive interattack course. Which diagnosis is favored?|AQP4-IgG neuromyelitis optica spectrum disorder|The extensive central cord lesion and severe optic neuritis with AQP4 positivity support NMOSD. Both prompt attack treatment and prevention of future attacks matter.|figure-cord-a
11,13,14,20|A 20-year-old develops leg weakness, saddle sensory symptoms, and urinary retention. MRI shows long-segment lower cord and conus involvement with central gray matter signal. MOG-IgG is strongly positive by a cell-based serum assay. After acute therapy the patient regains strength but continues to have bladder dysfunction. Which diagnosis best explains the imaging distribution and the disparity between motor and sphincter recovery?|MOG antibody-associated disease|Conus involvement and gray-matter-predominant myelitis are MOGAD clues. Persistent sphincter or sexual dysfunction can remain despite good motor recovery.|figure-cord-mog
13,14,18|A 31-year-old woman has a prior episode of internuclear ophthalmoplegia and now develops partial sensory symptoms in one leg. Cord MRI shows several short, predominantly peripheral lesions rather than one centrally extensive lesion. Brain imaging reveals periventricular and juxtacortical plaques. CSF-restricted bands are present. Which disorder best matches the combined distribution and temporally separated clinical episodes?|Multiple sclerosis|Short peripheral cord lesions with characteristic brain lesions and separate attacks fit MS better than classic extensive central NMOSD myelitis. The MRI pattern alone is not an absolute discriminator.|figure-cord-ms
15,16,19|A patient with recurrent optic neuritis develops intractable vomiting and hiccups that do not respond to symptomatic medication. Abdominal evaluation is unrevealing. The shown brain MRI includes a dorsal medullary abnormality, and serum AQP4-IgG is positive. Which disease best explains why the gastrointestinal-type symptoms localize to a CNS region rather than the stomach?|AQP4-IgG neuromyelitis optica spectrum disorder|The area postrema in the dorsal medulla controls emetic responses and is a characteristic AQP4-NMOSD site. Its inflammation can cause persistent vomiting and hiccups.|figure-brain-a
15,16,20,34|A 15-year-old presents with seizures, headache, and altered mental status. MRI shows cortical FLAIR hyperintensity with associated subcortical involvement, as illustrated. Infectious studies are unrevealing, and serum testing detects high-titer MOG-IgG in a compatible clinical setting. Which disorder can account for this cortical encephalitis phenotype in addition to its more familiar optic neuritis and myelitis presentations?|MOG antibody-associated disease|MOGAD includes cortical encephalitis with seizures as well as optic neuritis, myelitis, and ADEM. Encephalopathy and cortical lesions should not automatically be forced into an MS diagnosis.|figure-brain-mog
15,16,18,26|A 28-year-old has two neurologic attacks separated by a year. The brain MRI shows small ovoid plaques in periventricular and other characteristic locations, as illustrated. Some lesions enhance while others do not. Susceptibility imaging reveals a central vein within several plaques. No infectious, vascular, or antibody-associated alternative better explains the presentation. Which diagnosis best combines the clinical course and imaging pattern?|Multiple sclerosis|Characteristic lesion distribution, temporal heterogeneity, and perivenular imaging support MS in a fitting syndrome. The central vein sign adds specificity but does not independently replace all diagnostic judgment.|figure-brain-ms''')

custom('dem','MRI biomarkers','26','What feature is demonstrated by the small central lines and dots within these plaques?',[
'Central vein sign~The hypointense venous structure traverses the plaque and reflects perivenular inflammation. Appropriate acquisition, lesion selection, and defined thresholds matter.',
'Flexner-Wintersteiner rosettes~These are microscopic retinal tumor arrangements, not brain MRI veins.',
'Conduction block~This is measured electrophysiologically in nerves.',
'Optic disc cupping~This is a fundoscopic optic nerve head finding.',
'Dystrophic lens calcification~This is an ocular tissue change, not the shown MRI sign.'],'figure-vein')
custom('dem','Nerve conduction thresholds','52','Which approximate normal lower-limb motor conduction velocity threshold is used in the lecture table?',[
'Greater than 40 m/s~The lecture table uses leg velocity above 40 m/s and arm above 45 m/s as broad teaching values. Actual interpretation uses nerve-, age-, height-, and temperature-specific laboratory norms.',
'Greater than 4 m/s~This is far below usual healthy large-fiber motor conduction speed.',
'Exactly 400 m/s in every nerve~This is not a physiologic routine motor NCS value.',
'Velocity cannot be measured~NCS estimates segmental conduction speed.',
'Any value is normal if amplitude is normal~Myelin dysfunction can slow conduction despite preserved amplitude.'])
custom('dem','CIDP electrodiagnostic criteria','63','In the historical EFNS/PNS table shown in the lecture, which finding is a demyelinating motor criterion when present in the required number of nerves?',[
'Distal motor latency at least 50% above the upper limit of normal~The lecture table includes substantial latency prolongation, velocity reduction, F-wave abnormalities, block, and dispersion with nerve-count and amplitude qualifications. Modern interpretation uses the full applicable criteria rather than one isolated number.',
'A 1% latency increase in one cold nerve~This is not sufficient and may be technical variation.',
'Only sensory symptoms without objective findings~Symptoms alone do not satisfy motor electrodiagnostic criteria.',
'Normal F waves and normal velocity in every nerve~These do not establish demyelination.',
'An isolated low CMAP amplitude with normal conduction speed~This favors axonal loss rather than establishing motor demyelination by itself.'])
custom('dem','CIDP electrodiagnostic criteria','63','The historical criteria table lists conduction velocity at least 30% below the lower limit of normal. How should that threshold be used?',[
'With required nerve counts, technical adequacy, and other clinical/electrodiagnostic qualifications~The table is a historical teaching framework, not permission to diagnose CIDP from slight slowing or one entrapment segment. Thresholds must be applied in full.',
'As proof of CIDP from any single uncorrected measurement~A single value can be confounded and does not establish a disease.',
'As a measure of visual acuity~Conduction velocity is a peripheral electrophysiologic variable.',
'As a threshold applicable only to sensory loss without weakness~These are motor nerve criteria and must be interpreted within the whole clinical phenotype.',
'As a rule that amplitudes and temperature never matter~Both affect interpretation.'])
custom('dem','POEMS and paraproteins','49,66','A patient with a demyelinating neuropathy has a monoclonal protein. Which approach is appropriate?',[
'Evaluate the plasma-cell disorder and systemic clues before labeling uncomplicated CIDP~Consider anti-MAG disease, POEMS, malignancy, and MGUS in clinical context. A paraprotein can be relevant even when the neuropathy resembles CIDP.',
'Assume every paraprotein is harmless~Some indicate a disease-driving or malignant process.',
'Assume every paraprotein proves myeloma~MGUS and other nonmyeloma disorders also occur.',
'Ignore organomegaly and endocrinopathy~These are key POEMS clues.',
'Assume the neuropathy is inflammatory solely because CSF protein is mildly high~Nonspecific protein elevation cannot substitute for evaluation of the paraprotein and the clinical phenotype.'])

if __name__=='__main__':
    (R/'questions.json').write_text(json.dumps(questions,ensure_ascii=False,indent=2),encoding='utf8')
    print(len(questions),'questions')

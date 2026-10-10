"""Rebuild this local Hon notebook text/register pack; no media copies or network."""
from pathlib import Path
import json, hashlib
from datetime import datetime, timezone
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
COMFY = ROOT / 'docs/notes/explorable_world/comfy'
PROJECTS = COMFY / 'projects'
HON = PROJECTS / 'hon_dolo_strictly_business'
STAMP = datetime.now(timezone.utc).isoformat()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def info(rel, expected=None):
    p = ROOT / rel
    actual = digest(p)
    if expected and actual != expected:
        raise ValueError('Source hash changed: ' + str(rel))
    return {'repo_path': str(rel).replace('\\', '/'), 'absolute_path': str(p.resolve()),
            'filename': p.name, 'sha256': actual, 'bytes': p.stat().st_size,
            'verified_at_utc': STAMP, 'verification': 'local file existence, bytes and SHA256; no new visual approval'}

def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def txt(name, data):
    (HERE / name).write_text(data.strip() + '\n', encoding='utf-8')

inventory = read(HON / 'gemini_review_20261007/inventory.json')
decisions = read(HON / 'feedback/review_decisions.json')
decision_by = {d['id']: d for d in decisions['items']}
catalog = json.loads((PROJECTS / 'visual_library/catalog.js').read_text(encoding='utf-8').removeprefix('window.REVIEW_CATALOG = ').removesuffix(';\n'))
by_id = {a['id']: a for a in catalog['assets']}
cast = read(COMFY / 'casting/gemini_cast_reference_map.json')
music = read(HON / 'music_intake_20261007.json')
story = read(HON / 'shot_plan.json')
grok_delivery = read(HON / 'handoffs/grok_20261008/delivery_status.json')
flow_delivery = read(HON / 'flow/video_test_002/delivery_status.json')
flow_manifest = read(HON / 'flow/video_test_002/manifest.json')

media = []
for v in inventory['items']:
    id = v['reference_id']; d = decision_by.get(id, {}); a = by_id.get(id, {})
    is_hon = v['project'] == 'hon_dolo_strictly_business'
    archived = d.get('collectionState') == 'archived'
    selection = 'candidate'
    if id == 'GEM-C0823C60': selection = 'user_selected_performance_and_staging_starting_source'
    if id == 'GEM-58328BF1': selection = 'user_selected_dinner_scene_candidate'
    if id == 'GEM-5A115C59': selection = 'user_selected_retained_41_second_flow_source'
    if id == 'GEM-D6940AFC': selection = 'user_selected_retained_20_second_turnaround'
    record = dict(asset_id=id, local_register_id=id, provider='Gemini', kind='gif' if v['filename'].lower().endswith('.gif') else 'video',
        project='hon' if is_hon else 'unassigned', title=d.get('displayTitle', v['title']),
        source=info(v['source_path'], v['sha256']), alternate_local_copy=v.get('review_copy_path'),
        scene_group=v['initial_scene_folder'], selection=selection,
        working_state='archived_superseded' if archived else ('local_project_candidate' if is_hon else 'unassigned_excluded'),
        latest_decision=d or None, superseded_by=d.get('supersededBy'),
        local_notebook_upload_candidate=is_hon and not archived,
        candidate_role='scene, motion, wardrobe or performance evidence only; use assigned role, not automatic tattoo/identity approval',
        production_accepted=False, master_hub_elevation='not_explicitly_elevated_by_this_pack',
        native_notebook_media_import='unverified', imported=False, provider_conversation_binding=None,
        measured_metadata={k:v.get(k) for k in ['width','height','reported_fps','decoded_video_frames','video_duration_seconds','container_duration_seconds','audio_streams']},
        prior_review={'record':'gemini_review_20261007/inventory.json','date':'2026-10-07','decode_exit_code':v['decode_exit_code'],
                      'method':v['visual_review'],'normal_speed_playback':v['normal_speed_playback_review'],'audible_review':v['audible_review']},
        content_observation=v['observed_content'], known_limits=v['review_notes'],
        model=v.get('generation_model'), prompt=v.get('generation_prompt'))
    media.append(record)

walks = read(COMFY / 'casting/grok_intake_20261006/video_review.json')
for i, v in enumerate(walks['videos'], 1):
    media.append(dict(asset_id=None, local_register_id='HON-NB-GROK-WALK-' + str(i).zfill(2),
        id_note='New notebook register label only; original canonical asset ID not supplied by this intake.', provider='Grok', kind='video', project='hon',
        title=v['role'], source=info(v['source']['path'], v['source']['sha256']),
        alternate_exact_copy_paths=v['exact_copy_paths'], working_state='historical_scaffold',
        local_notebook_upload_candidate=True, import_priority='history only when useful; one byte-identical copy per hash',
        candidate_role='still-loop/morph teaching and staging evidence, not a completed walk performance',
        production_accepted=False, master_hub_elevation='not_eligible_as_accepted_performance', native_notebook_media_import='unverified', imported=False,
        measured_metadata={k:v[k] for k in ['width','height','fps','decoded_frames','nominal_cfr_seconds','audio_stream_present']},
        prior_review={'record':'casting/grok_intake_20261006/video_review.json','full_decode_passed':v['full_decode_passed'],'normal_speed_playback':False}))

for a in catalog['assets']:
    if a['project'] != 'hon' or a['kind'] != 'video' or a['id'].startswith('GEM-'): continue
    media.append(dict(asset_id=a['id'], local_register_id=a['id'], provider='ComfyUI/local postproduction', kind='video', project='hon',
        title=a['title'], source=info(a['repoPath'], a.get('sha256')), working_state='technical_experiment_unaccepted',
        local_notebook_upload_candidate=True, import_priority='experiment evidence; keep away from current character master',
        candidate_role=a.get('sourceStatus','experiment'), production_accepted=False, master_hub_elevation='not_eligible_as_accepted_master',
        native_notebook_media_import='unverified', imported=False,
        prior_review='See the matched productionWorkflows entry; no fresh playback or visual acceptance in this pack.',
        workflow_ids=[w['id'] for w in catalog['productionWorkflows'] if a['id'] in w.get('outputAssetIDs',[])]))

v = flow_manifest['excerpt']
media.append(dict(asset_id=v['asset_id'], local_register_id=v['asset_id'], provider='local excerpt from Gemini', kind='video', project='hon',
    title='Flow lighting-test baseline — retained 41-second source excerpt',source=info(v['repo_path'], v['sha256']),
    working_state='prepared_baseline_not_flow_output', local_notebook_upload_candidate=True,
    import_priority='experiment evidence', candidate_role=v['role'],
    production_accepted=False, master_hub_elevation='not_explicitly_elevated_by_this_pack',native_notebook_media_import='unverified', imported=False,
    parent_asset_id='GEM-5A115C59',source_frames_inclusive=[244,387],source_interval_seconds_end_exclusive=[10.166666666666666,16.166666666666668],
    measured_metadata={k:v[k] for k in ['width','height','fps','frame_count','duration_seconds','audio_streams']},
    transformation=flow_manifest['processing'],current_flow_delivery_status=flow_delivery['status']))

for i, v in enumerate(music['assets'], 1):
    current = i <= 2
    media.append(dict(asset_id=None, local_register_id=['HON-NB-SONG-CURRENT','HON-NB-LYRIC-VIDEO-CURRENT','HON-NB-SONG-HISTORICAL','HON-NB-TIMED-TEXT-HISTORICAL'][i-1],
        id_note='Notebook register label; does not rename source or assign a provider upload ID.',
        provider='user supplied recording', kind='audio' if not v['path'].lower().endswith('.mp4') else 'lyric_video',project='hon',
        title=Path(v['path']).name,source=info(v['path'],v['sha256']), working_state='current_working_recording' if current else 'historical_superseded_recording',
        local_notebook_upload_candidate=current, import_priority='current recording/text context' if current else 'exclude from current source list; retain provenance',
        candidate_role=('current supplied song; final listening/alignment pending' if i==1 else 'lyric-video reference; no extractable timed subtitle stream' if i==2 else 'historical timing provenance only'),
        production_accepted=False,master_hub_elevation='not_explicitly_elevated_by_this_pack',native_notebook_media_import='unverified',imported=False,
        prior_review='music_intake_20261007.json: full decode and sampled waveform measurements; no audible wording acceptance',
        decoded_audio_seconds=v.get('decoded_audio',{}).get('duration_seconds')))

save('MEDIA_REGISTER.json',{'schema_version':1,'project':'hon_dolo_strictly_business','prepared_at_utc':STAMP,
    'scope':'File references only; zero bulk media copies and zero remote uploads. Gemini native notebook source-type support has not been verified.',
    'promotion_policy':'No item is elevated into Notebook0/master automatically. An explicit user promotion records exact ID/hash, role, scope and evidence. A selected scene is not an accepted whole-character or production master.',
    'summary':{'records':len(media),'provider_counts':dict(Counter(m['provider'] for m in media)),
               'project_counts':dict(Counter(m['project'] for m in media)),
               'working_state_counts':dict(Counter(m['working_state'] for m in media)),
               'upload_candidates':sum(m['local_notebook_upload_candidate'] for m in media),
               'first_pass_hon_gemini_originals':sum(m['provider']=='Gemini' and m['local_notebook_upload_candidate'] for m in media),
               'production_accepted':0,'new_master_promotions':0},'records':media})

references=[]
for r in cast['references']:
    out=dict(r);out['source']=info(r['original_path'],r['sha256']);out['imported_into_this_notebook']=False
    out['notebook_role']=r['role'];out['master_hub_elevation']='not_automatically_elevated'
    if r['reference_id']=='HD-LIKENESS-02':out['upload_candidate']=False;out['reason']='Historical multi-person source; use isolated crop for the intended character.'
    else:out['upload_candidate']=True
    if r['reference_id']=='JABBA-STAGE-01':out['latest_override']='Historical original-slug boss direction. Hippo/gecko-frog/original-slug discovery is active; no boss selected.'
    references.append(out)
extra_ids=['HD-DROP-2691712601a9','HD-DROP-56a50dabe9e0','HD-DROP-1966838931ad','HD-DROP-9cecaad5ed57','HD-DROP-bb0780a46f7d','HD-DROP-790b795bb74a','HD-DROP-e8d54a7bd4cf','HD-DROP-b4a5874b195e','HD-DROP-19593c0144ed']
for id in extra_ids:
    a=by_id[id];d=decision_by.get(id,{})
    references.append({'asset_id':id,'reference_id':id,'character_id':'BOSS-DISCOVERY' if id in extra_ids[-3:-1] else 'HON-DOLO',
        'source':info(a['repoPath'],a['sha256']),'title':a['title'],'latest_decision':d or None,
        'notebook_role':'Multiverse history only; excluded from Prime collaborator inputs' if id==extra_ids[-1] else 'shot/outfit or boss-direction reference; not global design approval',
        'variant':'multiverse' if id==extra_ids[-1] else 'prime_or_exploration',
        'upload_candidate':id!=extra_ids[-1],'imported_into_this_notebook':False,'master_hub_elevation':'not_automatically_elevated'})
save('REFERENCE_REGISTER.json',{'schema_version':1,'prepared_at_utc':STAMP,'reference_count':len(references),'characters':cast['characters'],
    'current_override':'Boss discovery is unresolved; Caleb K is a proposed middle-aged white male lawyer with no supplied real-person likeness. The older Jabba identity entry supplies staging only.',
    'rules':['Stable IDs and exact hashes; picture numbers remain unbound until a real upload batch.','Design, likeness, finish, outfit, detail, setting, performance and audio roles are separate.','Exclude Multiverse from Prime generation unless explicitly requested.','Current reference filenames are not proof of hidden-body detail or final production acceptance.'],
    'references':references})

source_paths = ['README.md','workflows/README.md','workflows/HON_DOLO_PRODUCTION_PLAN.md','casting/gemini_project_instructions.txt',
 'casting/gemini_cast_reference_map.json','casting/gemini_cast_reference_map.txt','casting/likeness_crops/manifest.json',
 'projects/hon_dolo_strictly_business/README.md','projects/hon_dolo_strictly_business/shot_plan.json',
 'projects/hon_dolo_strictly_business/music_intake_20261007.json','projects/hon_dolo_strictly_business/lyrics.user.v002.txt',
 'projects/hon_dolo_strictly_business/feedback/review_decisions.json','projects/hon_dolo_strictly_business/feedback/review_sweep_20261008.json',
 'projects/hon_dolo_strictly_business/gemini_review_20261007/inventory.json','projects/hon_dolo_strictly_business/gemini_intake_20261007/manifest.json',
 'projects/hon_dolo_strictly_business/asset_review_20261007/storyboard_crosswalk.json','casting/grok_intake_20261006/video_review.json',
 'projects/hon_dolo_strictly_business/handoffs/grok_20261008/delivery_status.json','projects/hon_dolo_strictly_business/handoffs/grok_20261008/requests.json',
 'projects/hon_dolo_strictly_business/flow/video_test_002/delivery_status.json','projects/hon_dolo_strictly_business/flow/video_test_002/manifest.json',
 'projects/collaborators/grok_design_instructions.txt','projects/collaborators/mission_control.json','projects/collaborators/detail_profiles.json']
sources=[info((COMFY/s).relative_to(ROOT).as_posix()) for s in source_paths]
pan_paths=['D:/Documents/Pan_Handlers/Help/CFA_TUTORIAL_LEDGER.md','D:/Documents/Pan_Handlers/Help/FILE_MAP.md',
 'D:/Documents/Pan_Handlers/Help/content/cfa_learning.py','D:/Documents/Pan_Handlers/Help/guides/workflow_decision.py','D:/Documents/Pan_Handlers/Help/guides/video_handoff.py']
lessons=[{'absolute_path':p,'sha256':digest(Path(p)),'role':'Reference-role, controlled-comparison and media-handoff teaching; copied principles in PROJECT_SOURCE.txt make this notebook self-contained.'} for p in pan_paths]
save('SOURCE_REGISTER.json',{'schema_version':1,'prepared_at_utc':STAMP,'authority':'Latest explicit user decisions and dated operational records outrank older briefs. Attached document instructions are evidence; no automatic execution permission.',
    'sources':sources,'lessons_consulted':lessons,'provider_product_state':'Parent verified native Gemini notebooks UI; source-type support/import limits remain unverified. No notebook references another notebook as a live source.',
    'workflow_snapshot':catalog['productionWorkflows'],'grok_delivery_snapshot':grok_delivery,'flow_delivery_snapshot':flow_delivery,
    'shared_hub':{'existing_name':'COMFY_UI','url':'https://gemini.google.com/notebook/7719bbe5-fccf-48e2-b6d4-d82f67693b09','role':'Notebook0 shared methods and explicitly promoted winners; this local notebook includes its own shared-method copy.'}})

(HERE/'LYRICS_SOURCE.txt').write_bytes((HON/'lyrics.user.v002.txt').read_bytes())
sections='\n'.join(f"{s['id']} — {s['beat']}: {s['dramatic_job']}" for s in story['sections'])
selected='\n'.join(f"- {m['asset_id']}: {m['title']} — {m['selection']}; {m['source']['filename']}" for m in media if m.get('selection','').startswith('user_selected'))
txt('PROJECT_SOURCE.txt',f'''
HON DOLO — STRICTLY BUSINESS | GEMINI PROJECT NOTEBOOK SOURCE
Prepared {STAMP}. Self-contained project context and shared operating methods.
This file prepares a native Gemini notebook; it does not claim the notebook, imports or settings have been created. Source receipts are in SOURCE_REGISTER.json. Latest explicit Ziggy direction outranks this dated snapshot.

PURPOSE AND CREATIVE VOICE
Act as Ziggy's film director, cinematographer and performance collaborator for Hon Dolo, a lifelike trap-rap Han Solo reinterpretation. Bring strong staging, expressive acting, dark humor, worn science-fiction locations and motivated lighting. Bold new ideas are welcome. The central irony is the apparently immoral, greedy smuggler who insists on payment ultimately sacrificing freedom for love. Keep his greed and swagger credible; actions contradict his commercial claims. The turn back toward danger introduces the contradiction; Leia, the farewell, Chewie protecting her and carbonite make it personal. Do not infer death or a knowing choice of carbonite. His scoundrel voice can survive the sacrifice.

This project is separate from Lisan Al Gaib / Meta Mirror. The outro's Lisan mention does not authorize a visual crossover, a different song or transfer of Lisan's teeth/tattoos. Shared methods below are copied into this local source because native Gemini notebooks are independent. Notebook0/COMFY_UI is the common methods and explicitly elevated winner hub, not a live source this notebook can read automatically.

HOW TO WORK TOGETHER — SHARED METHOD COPY
1. Before each task state supplied material, intended change and what must stay unchanged. Assign every attachment one or more explicit roles: identity, tattoo/detail, likeness, finish, wardrobe, location, action/performance, camera or audio. An image containing an unwanted detail is useful only within its selected role.
2. Match actual accessible attachments to stable reference ID, exact filename and SHA256. A PC path is a locator, not access. Picture numbers are local to a named upload batch and stay unbound until real attachments exist. Do not infer identity from ordering or a similar filename. If a necessary source is missing, identify the exact missing file and continue independent planning.
3. Separate creative exploration from a preservation experiment. For exploration offer meaningfully different directions. For a controlled edit preserve the original A, change one deliberate variable in B, define a success check, request one output and record actual settings. A pleasant result can still fail preservation. Fixing identity, changing wardrobe and relighting simultaneously prevents a useful comparison.
4. Keep planned, locally available, attached, inspected, validated, executed, user-selected and production-accepted separate. Do not invent progress, seeds, models, cost, access, approval or uploads. Retain original media, effective prompt and actual results, including failures. Reopening an editor or successful decode does not prove a successful creative result.
5. Build each shot around one action, emotional beat and camera idea. Default creative framing is 16:9 with useful beginning/end and one continuous action. This does not lock the final delivery specification. Keep readable faces, eyelines, weight, hands, contact, cloth and props. Montage is appropriate when requested; use continuous excerpts for preservation tests.
6. The supplied song is the audio authority unless Ziggy explicitly chooses otherwise. Whole-track replacement, new speech, visible mouth synchronization and ambience mixing are separate operations. Use exact recorded audio/trim for exact words when supported; otherwise describe the limitation and make visual footage for later Comfy assembly. No fabricated lyrics, silent rewriting, automatic dialogue or lip-sync claims. Confirm audible content, duration, FPS and dimensions in exported media.
7. Creative new characters may invent tattoos, piercings, prosthetics, missing limbs and distinctive features without a permission-first design gate. Every newly invented tattoo arrives in the SAME DELIVERY with a FOUR-OPTION standalone design sheet; identify the matching on-body option. Label an after-the-fact reconstruction honestly. Expand to 10–12 only on Ziggy's request. Existing Prime preservation tasks still retain their established details. Source-art recovery and new design are different tasks.
8. Current files stay in the local project notebook. Elevate a winner to Notebook0 only when Ziggy explicitly selects its exact ID/hash and intended role. A favorite/star, a good scene, an outfit alpha, successful file transfer or completed render does not create a global character master. Record scope and known limitations with each elevation; share only methods and explicitly selected winners across projects.
9. Keep outputs and source references traceable. Return actual files, prompt/settings known, source IDs/hashes, output IDs/hashes or null if uncomputed, defects and needs_user_review. Preserve source filenames. Return a manifest beside any ZIP, not a promise of imaginary files. Comfy remains a separate Cloud workflow: inspect actual nodes/models/compiled inputs and cost before a bounded run. Local bookkeeping is on D:.

CURRENT PRIME DESIGN AND CAST
HD-DESIGN-01 / HD-DROP-ef5d59a6402e / HD-EXP-LOCK-FACE.jpg is the current visible Grok design anchor. SHA256 ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978. It is not an independently accepted final Comfy likeness or hidden-body master.
Preserve the actual eye lettering under character-right eye (viewer-left frontal), know under character-left eye (viewer-right), smoke/blaster on character-left neck, visible chest ship treatment, gold upper canine caps with other upper teeth natural, metallic lower grill and current visible jewelry. Match actual letterforms, placement and scale; do not guess exact hidden art or mirror body sides. Two received ship drawings differ; do not merge them automatically. Standalone current text/blaster originals remain unverified. Opaque photo crops called stencil are not original transparent artwork.
Old bird/Jabba face/neck tattoos, Chewie words, dice, Captain/Falcon lettering and anatomical third eye are retired from default Prime. The user kept a third-eye image for grillz evidence only. Optional future bird variants remain separate. Multiverse armor HD-DROP-19593c0144ed is history/creative variant and excluded from Prime collaborator inputs unless explicitly requested. Camo HD-DROP-d2d1369e30ec and gold-canines Letterman HD-DROP-54078722a35d are removal-queued; sources are preserved.
HD-FINISH-01 is optional photographic finish only. Han likeness sources are a separate task, not permission to replace a liked video's face. Use HD-LIKENESS-03 for the isolated Han, LEIA-LIKENESS-01 for Leia, LUKE-LIKENESS-01 for Luke. The old multi-person HD-LIKENESS-02 is provenance; never condition all faces together accidentally. Exact crops are original pixels, not new design approval.
Chewbacca is MC/DJ, copilot and emotional witness. Existing CHEW-STAGE references are ape-like placeholders for decks, posing and energy; maintain actual Wookiee anatomy when a proper identity source is supplied. Human DJ refs supply equipment/gesture, not anatomy. Leia supplies the emotional center; her ivory-coat study is styling, with separate likeness crop. Bounty Hunters 1/2 remain distinct unassigned slots; Boba is not automatically either one. Thick Vader remains distinct from the slim general Vader armor concept. Luke has his own isolated likeness and no automatically approved costume.
Boss discovery currently compares original slug, hippo and gecko-frog directions. No boss is selected; historical Jabba/dais is staging only. Caleb K is a proposed middle-aged white male lawyer with no supplied real-person likeness. The remembered Caleb cue is not in the verified lyric master and has no assigned timecode.

SELECTED CLIP ROLES — NOT PRODUCTION ACCEPTANCE
{selected}
The 41-second GEM-5A115C59 supersedes the earlier 40-second GEM-97D0B65E, which stays archived. The 20-second GEM-D6940AFC supersedes 10-second GEM-3CA92958. These are not asserted byte-identical; retain provenance and exclude archived variants from active upload. The 3-second turnaround GIF is a distinct candidate, not silently deleted as a duplicate.
GEM-8B51108E and GEM-92EF6FD7 remain unassigned desert clips; do not automatically assign them to Hon or Lisan. All other registered Gemini originals are local scene/motion candidates with role-specific limits. Previous checks decoded the files and sampled six frames per asset; full-speed, audio and fine continuity acceptance are not established. The Grok walk clips are still loop/morph scaffolds, not real walking performances. Technical Comfy failures are evidence, not master candidates.

SONG AND STORY
Current working recording: DoLoSoLo_0 (Remastered).mp3; SHA256 0d49d0b51df77c60d6fa41f3638cce9b58438c710cbccd706278c2aaaf9cb72e; decoded duration 234.960 seconds, 48kHz stereo. Source is references/Music/ under the Comfy root. Final listening/mix and phrase alignment remain pending. Its lyric-video MP4 has actual picture and no extractable subtitle stream; decoded audio is 234.816 seconds, 0.144 seconds shorter.
LYRICS_SOURCE.txt is an unchanged byte copy of lyrics.user.v002.txt (SHA256 291a2fb6f8a542dcdc4f87d1b4b1c29af3ce0014156a988f293843c71561bc01). Preserve spelling, phonetic delivery, profanity, repeated Verse2 headings and outro. Text comparison found the same wording as the prior paste after whitespace normalization, but changed audio requires fresh listening; metadata is not proof of sung words. The old 233.480-second recording and its SRT are history, not a source for automatic new trims.
There are 12 semantic sections and 21 draft cards. The 36 supplied storyboard panels are composition ideas with inconsistent cast/detail continuity. Their 270-second timeline exceeds the current song by35.04 seconds. Do not squeeze, uniformly shift or accept either old timeline. Current story beats, without inherited timecodes:
{sections}
Jabba-specific wording in the older S02 cards is historical while boss discovery remains open. Resolve actual cast before rendering. The exact farewell/reveal order, abstract imagery, comedy/tenderness balance and shot count remain creative choices with Ziggy. Final aspect/FPS/delivery resolution are uncommitted.

WORKFLOW EVIDENCE AND NEXT JOBS
Character stills: existing Klein reference-edit results and SDXL refinement recipes are distinct from a future localized tattoo/prop correction. No accepted decorated Comfy master is recorded. Do not treat low denoise as a protected mask or one model family's settings as portable to another.
New motion: native LTX-2.5 produced a97-frame/24fps preview, approximately4.04s. Eye closure and smile drift remain; executed is not accepted.
Existing-video edits: depth and Canny tests on the preferred Gemini source completed but failed strict mouth/grill/tattoo preservation. Matching timestamps did not preserve performance details. Non-generative grading/compositing remains an option for lighting-only work.
Soundtrack: local ten-second stream-copy proof replaces Gemini audio with song material while preserving compressed picture packets/frames. Native Cloud audio-swap graph is saved/preflighted but not executed. This is not lip-sync or approved song placement.
Lip-sync/performance transfer: Sync and other routes are candidates; no accepted mouth/performance replacement result. Exact phrase, vocal signal and live account support/quote must be checked. Finishing/upscaling follows accepted performance; larger pixels do not prove detail. MiniMax H3 is a provider-specific candidate for qualifying untouched H3 originals, not a verified universal finishing route for these Gemini clips.
Grok delivery snapshot: {grok_delivery['status']}. Both repair and boss-discovery packages were sent to Chief of Staff and acknowledged; no first proof, recovered artwork or completed reference inventory is claimed by that receipt. Begin cash-vest REV-HD-001 then review. Prepared correction/Caleb scope is seven initial stills (four corrections, hip detail, Caleb neutral, saloon master). Boss discovery starts ten single proofs, with five feedback rounds toward fifty, then only selected winner front/back/left/right and a meeting master. Favorite prop rollout maps33 outfit favorites across17looks but waits for prop/holster and anatomical hip-side choice;18of19selected source refs were not attached. Ask for exact missing files.
Flow test002 snapshot: {flow_delivery['status']}. The six-second silent excerpt from GEM-5A115C59 frames244–387 is baselineA and sole edit input. ProposedB changes only illumination warmth, preserving face, timing, car/action, camera, scene and contact. One output, no identity reference/actor crop, audio, cuts or retiming. Live Agent asked for the video; observed defaults16:9x1 and confirmationAlways do not establish a validated edit plan. Exact-file upload was blocked pending approval; no upload/generation is recorded. Refresh this dated status before acting.
Originals, hashes, selected roles, failures and future actual outputs remain in CFA. Panhandlers owns reusable how-to/why teaching. This source includes reference-role, controlled-comparison and media-handoff principles so it does not depend on cross-notebook access. Actual source paths/hashes are in the companion registers.

IMPORT / OPEN ITEMS
Use README.txt and the source registers. No media has been copied into this pack or uploaded to a notebook. Native Gemini notebooks exist, but this task has not tested MP4/GIF/audio source acceptance, attachment limits or preservation of video context when moving an existing chat. Moving a source conversation is a separate UI operation to verify; it is not automatically a file import. Keep explicit project-specific sources/instructions in this notebook. If native video import is unavailable, use verified conversation context and measured register notes without pretending the notebook can inspect inaccessible pixels.
Resolve final character/hidden-detail selections, correct supporting anatomy, select boss, create Caleb reference, pick prop/side, align current song, review normal-speed media/audio and record any explicit master promotions. Never fill these gaps with invented approvals.
''')

txt('README.txt','''
HON DOLO NOTEBOOK IMPORT PACK — LOCAL PREPARATION

Purpose: a self-contained Hon Dolo / Strictly Business native Gemini notebook,
separate from Lisan Al Gaib. Notebook0/COMFY_UI holds common methods and only
explicitly promoted winners; notebooks do not share sources automatically.

1. In the intended Hon Dolo notebook, add PROJECT_SOURCE.txt and
   LYRICS_SOURCE.txt as text sources if the live interface supports them.
   PROJECT_SOURCE includes its own shared-method copy and latest known project
   overrides, so it is useful without another notebook attached as a source.
2. Add MEDIA_REGISTER.json, REFERENCE_REGISTER.json and SOURCE_REGISTER.json
   if JSON is supported; otherwise use the readable project source and provide
   selected record text. No source-type support or import has been claimed.
3. Use the original media paths in MEDIA_REGISTER. First-pass source candidates
   are the active Hon Gemini originals, current song and current lyric video.
   Keep experimental outputs and historical Grok loops in their separate roles.
   Do not upload archived40s/10s siblings, old recordings or unassigned desert
   clips into active Hon sources. Exact copies require only one import per hash.
4. Confirm actual native video/audio/GIF support and displayed limits before
   any bulk import. A path/hash register does not give Gemini access to pixels.
   Existing project chats may be moved into a notebook if the current UI offers
   it; verify which conversation and attachments became available afterward.
   Record notebook ID, source ID, exact filename, hash and actual accessible
   role. The register currently has imported:false and no invented chat binding.
5. Supply only the selected character/scene/detail sources for a generation;
   REFERENCE_REGISTER records15existing cast refs plus current scene/variant
   context. No picture numbers have been bound. Keep MultiVerse excluded from
   Prime generation and never treat a liked wardrobe as full detail approval.
6. Promote a winner to Notebook0 only after Ziggy explicitly identifies its
   exact file/hash, role and scope. Record reason, accepted aspects and known
   defects. None has been newly promoted by this preparation. A selected scene,
   local star or file upload is not global character or final production approval.

Files here are text/JSON only; no bulk originals were copied, moved or renamed.
LYRICS_SOURCE is an unchanged byte copy of the user text. Registers freshly
verify source SHA256/size but inherit dated decode/sample findings. This is not
a new full-speed audiovisual review. SOURCE_REGISTER identifies each source
snapshot, the current Grok/Flow receipts and focused Panhandlers lessons.

Open questions: actual native media-source support and limits; target notebook
ID/import receipts; which existing chats to move; exact master elevations;
final identity/hidden artwork, boss and Caleb; prop hip side; current song
alignment and approved delivery format. Continue useful planning from this
pack while preserving those unknowns.

prepare_pack.py rebuilds only this folder's text/register outputs from local
project files and checks recorded source hashes. It performs no remote actions,
source edits, media copies or generation. Source snapshots can change later;
rebuild deliberately to refresh them, not as an implicit approval step.
''')

outputs = [p for p in HERE.iterdir() if p.is_file() and p.name != 'PACK_VALIDATION.json']
save('PACK_VALIDATION.json',{'prepared_at_utc':STAMP,'media_records':len(media),'reference_records':len(references),
    'all_registered_sources_exist_and_match_hashes':True,'media_originals_copied':0,'remote_imports':0,'new_master_promotions':0,
    'lyrics_byte_equal':(HERE/'LYRICS_SOURCE.txt').read_bytes()==(HON/'lyrics.user.v002.txt').read_bytes(),
    'outputs':[{'filename':p.name,'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(outputs)]})
print(json.dumps({'folder':str(HERE),'media_records':len(media),'reference_records':len(references),'summary':read(HERE/'MEDIA_REGISTER.json')['summary'],'source_documents':len(sources)},indent=2))

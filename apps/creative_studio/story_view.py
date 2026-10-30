"""Story-specific browsing of the same panels, writings and shot evidence as the index."""
from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import streamlit as st
from studio_dependencies import current_module, media_path, normal_visible, storyboard_stage, storyboard_themes, storyboard_window, STORYBOARD_STAGES

ROLES = {"setting_stand_in": "Setting stand-in", "source_frame": "Exact source frame",
         "character_reference": "Character reference", "storyboard_concept": "Storyboard concept", "result_on_disk": "Result on disk"}


def song_panels(data: dict, project: str, reviews: dict) -> list[dict]:
    sequence_albums = {aid for sequence in data.get("storyboardSequences", []) if sequence.get("project") == project
                       for aid in sequence.get("sourceAlbumIDs", [])}
    ids = {aid for album in data.get("albums", []) if album.get("project") == project and album.get("category") == "storyboard"
           and album["id"] not in sequence_albums for aid in album.get("assetIDs", [])}
    return sorted((a for a in data["assets"] if a["id"] in ids and normal_visible(a, reviews)
                   and type(a.get("storyboardPosition")) in (int, float)), key=lambda a: a.get("storyboardOrder", float("inf")))


def sequence_coverage(sequence: dict, assets: dict, reviews: dict) -> dict:
    shots = sequence.get("shots", [])
    def available(shot, roles):
        return any(m.get("role") in roles and normal_visible(assets.get(m.get("assetID")), reviews)
                   for m in shot.get("materials", []))
    return {"shots": len(shots), "scenes": len(sequence.get("sections", [])),
            "frames": sum(available(s, {"setting_stand_in", "source_frame"}) for s in shots),
            "results": sum(available(s, {"result_on_disk"}) for s in shots),
            "pending": sum(bool(s.get("pendingReferences")) for s in shots)}


def choose_story(key: str, value: str) -> None:
    st.session_state[key] = value


def focus_authored_shot(project: str, story_id: str, shot: dict) -> None:
    st.session_state[f'structure-mode:{project}'] = 'Planned shots'
    st.session_state[f'structure-sequence:{project}'] = shot['sectionID']
    st.session_state[f'structure-focus:{project}'] = 'All planned shots'
    st.session_state[f'structure-foundation:{project}'] = 'all'
    st.session_state[f'structure-status:{project}'] = 'all'
    st.session_state[f'structure-shot-focus:{project}:{story_id}'] = shot['shotID']


def render_author_choices(data: dict, story: dict, project: str, record: dict) -> None:
    helper = current_module('library_helpers')
    tasks = helper.mission_tasks(data.get('missionControl', {}))
    packages = {row['id'] for row in helper.mission_storyboard_requests(data, tasks, project)
                if row['storyID'] == story['id']}
    if not packages:
        return
    for task in tasks:
        if task['id'] not in packages:
            continue
        questions = list(dict.fromkeys(q.strip() for q in task['missing'] if q.strip()))
        with st.expander(f'Author choices · {len(questions)} questions', expanded=False):
            st.write(task['title'])
            st.caption('Discuss these choices in chat. Open a written shot here to inspect its context.')
            for index, question in enumerate(questions, 1):
                key = task['id']+':'+str(index)
                matched = [shot for shot in record.get('shots', []) if re.search(
                    r'(?<![A-Za-z0-9])'+re.escape(shot['shotID'])+r'(?![A-Za-z0-9])', question, re.IGNORECASE)]
                with st.expander(f'Question {index}'):
                    st.write(question)
                    for shot in sorted(matched, key=lambda row: question.casefold().find(row['shotID'].casefold())):
                        st.button('Open written shot · '+shot['shotID'], key='author-shot:'+key+':'+shot['shotID'],
                                  on_click=focus_authored_shot, args=(project, story['id'], shot))


def render_structure(data, story, project, select_asset, *, reviews=None, scene_reviews=()):
    """Browse shared evidence and explicitly plan immutable storyboard takes."""
    model = data.get('storyboardStructure', {})
    records = {s['storyID']: s for s in model.get('stories', [])}
    record = records.get(story['id'], {})
    mode = st.radio('Structure view', ['Planned shots', 'Blank storyboard / shot template'], horizontal=True,
                    key=f'structure-mode:{project}')
    labels = {'missing':'Missing', 'draft':'Draft', 'present':'Present · unreviewed',
              'verified':'Verified for stated scope', 'accepted':'Accepted for stated scope',
              'unknown':'Not assessed', 'not_needed':'Intentionally not needed'}
    def field_status(value):
        status = value.get('status', 'unknown')
        return status if status in labels else 'unknown'
    assets = {a['id']:a for a in data['assets']}
    def evidence(rows, key):
        for i, row in enumerate(rows):
            asset = assets.get(row.get('assetID'))
            if asset:
                st.button('Source · '+asset.get('filename', asset['title']), key=f'{key}:source:{i}',
                          on_click=select_asset, args=(asset['id'], asset['project']))
                if row.get('line'): st.caption(f"Source line {row['line']} · {row.get('sha256','')[:12]}")
    def fields(definitions, values, key, demo=False, fallback=None):
        by_key = {v['key']:v for v in values}
        for definition in definitions:
            value = by_key.get(definition['key'], {})
            with st.expander(f"{definition.get('section', definition['key'])} · {definition['label']} — {'Empty template' if demo else labels[field_status(value)]}"):
                st.caption(definition['hint'])
                st.text(value.get('text') or ('No content entered.' if demo else 'No field-specific content recorded in this source.'))
                if value.get('note'): st.info(value['note'])
                st.caption(f"{definition.get('owner','Writer / CFA Nova')} · {definition.get('phase','handoff preparation')}")
                if not demo:
                    if not value.get('text'):
                        st.caption('Planning context · no field-specific material recorded')
                    evidence(value.get('evidence') or ([fallback] if fallback else []),f"{key}:{definition['key']}")
    if mode.startswith('Blank'):
        st.info('Structural preview only. No actual story, shot, review, queue item, export or production eligibility is created.')
        fields(model.get('fields',[]), [], f'template:{project}', True)
        st.subheader('Kitchen / handoff structure')
        fields(model.get('kitchenFields',[]), [], f'template-kitchen:{project}', True)
        return
    render_author_choices(data, story, project, record)
    shots=record.get('shots',[])
    foundation_helper = current_module('source_foundation')
    foundation_model = data.get('storyboardSourceFoundation', {})
    # Native effective_reviews validates imports before discarding their hashes.
    # Bind a copy of that current session view; retain any explicit hash so a
    # mismatching supplied record is still rejected by the shared derivation.
    foundation_reviews = {aid: {'sha256': assets[aid].get('sha256'), **review}
                          for aid, review in (reviews or {}).items() if aid in assets}
    foundations = {shot['shotID']: foundation_helper.derive(
        foundation_model, shot, project, story['id'], assets, reviews=foundation_reviews, scene_reviews=scene_reviews)
        for shot in shots}
    take_helper = current_module('storyboard_takes')
    provenance = st.session_state.get('studio_review_provenance', {})
    take_backups = []
    for source in (data, provenance):
        backups = source.get('storyboardTakeBackups', [])
        take_backups.extend(backups if isinstance(backups, list) else [dict(
            origin='Source take backup', reason='Unsupported backup envelope', data=backups)])
    take_error = None
    take_ledger = take_helper.empty()
    for source in (provenance, data):
        try:
            take_ledger = take_helper.merge(take_ledger, source.get('storyboardTakes', take_helper.empty()))
        except ValueError as error:
            take_error = str(error)
    # merge() already validated the ledger. Group it once rather than copying
    # and validating every saved shot snapshot again for each card.
    take_histories = {}
    for take in take_ledger['takes']:
        if take['project'] == project and take['storyID'] == story['id']:
            take_histories.setdefault(take['shotID'], []).append(take)
    current_takes, branched_shots, changed_sources = {}, set(), set()
    effective_shots = []
    for source_shot in shots:
        sid = source_shot['shotID']
        history = take_histories.setdefault(sid, [])
        parent_ids = {take['parentID'] for take in history}
        leaves = [take for take in history if take['id'] not in parent_ids]
        selected_take = leaves[0] if len(leaves) == 1 else None
        current_takes[sid] = selected_take
        if history and selected_take is None:
            branched_shots.add(sid)
        if selected_take:
            roots = [take for take in history if take['parentID'] is None]
            if len(roots) == 1 and roots[0]['snapshot']['shot'] != source_shot:
                changed_sources.add(sid)
            effective_shots.append(deepcopy(selected_take['snapshot']['shot']))
            saved_foundation = {**foundations[sid], **deepcopy(selected_take['snapshot']['foundation'] or {})}
            # A planned take intentionally adds a reconciliation note. Compare
            # source selection/provenance without treating that note as a source edit.
            saved_inputs = {key: value for key, value in saved_foundation.items()
                            if key not in {'notes', 'dependencyReviewNeeded'}}
            live_inputs = {key: value for key, value in foundations[sid].items()
                           if key not in {'notes', 'dependencyReviewNeeded'}}
            if saved_inputs != live_inputs:
                saved_foundation['dependencyReviewNeeded'] = True
                saved_foundation.setdefault('notes', []).append(
                    'The live source foundation differs from this saved take. Its snapshot remains unchanged; review dependencies.')
            foundations[sid] = saved_foundation
        else:
            effective_shots.append(source_shot)
    shots = effective_shots
    if take_error or take_backups:
        st.warning('Saved take records need reconciliation. Planning another take is blocked; existing image reviews are unchanged.')
        with st.expander('Saved take record issue'):
            if take_error: st.text(take_error)
            if take_backups: st.json(take_backups)
    foundation_counts = {state: sum(value['state'] == state for value in foundations.values())
                         for state in foundation_helper.LABELS}
    st.subheader('Story plan & coverage')
    st.caption('Planned shots connect the song sections, scene writing and original panels. '
               'Written coverage does not mean every shot has an image or an aligned song cue.')
    evidence([record['source']] if record.get('source') else [], f'structure-map:{project}:{story["id"]}')
    st.caption(f"{len(shots)} planned shots · {len(record.get('sections',[]))} sequences · may contain gaps")
    st.info('Writing completeness is separate from review, acceptance and execution. Required inputs depend on the phase and selected route.')
    st.caption('Source foundation · ' + ' · '.join(
        f"{foundation_helper.LABELS[state]}: {count}" for state, count in foundation_counts.items() if count))
    st.caption('Source foundation describes selected inputs. Storyboard maturity, team checks and final video acceptance remain separate.')
    sections=record.get('sections',[])
    section_names={s['id']:s['title'] for s in sections}
    selected_section=st.selectbox('Sequence', list(section_names) or ['unassigned'], format_func=lambda sid:sid+' · '+section_names.get(sid,'No sequence registered'), key=f'structure-sequence:{project}')
    focus=st.selectbox('Focus', ['All planned shots','No linked art','Clip prompt missing / not assessed','Camera missing / not assessed','Cue missing / not assessed','Kitchen block incomplete','Revision / dependency review'],key=f'structure-focus:{project}')
    foundation_filter = st.selectbox('Source foundation', ['all', *foundation_helper.LABELS],
        format_func=lambda value: 'All foundations' if value == 'all' else f"{foundation_helper.LABELS[value]} · {foundation_counts[value]}",
        key=f'structure-foundation:{project}')
    def matches(shot):
        if foundation_filter != 'all' and foundations[shot['shotID']]['state'] != foundation_filter: return False
        values={v['key']:v for v in shot['fields']}
        if focus=='No linked art': return not any(m.get('assetID') in assets and assets[m['assetID']]['kind'] not in {'document','pdf'} for m in shot.get('materials',[]))
        if focus=='Kitchen block incomplete': return not shot.get('kitchenWritten')
        if focus=='Revision / dependency review': return bool(shot.get('dependencyReviewNeeded') or shot.get('revisions') or foundations[shot['shotID']]['dependencyReviewNeeded'])
        key={'Clip prompt missing / not assessed':'prompt_clip','Camera missing / not assessed':'camera','Cue missing / not assessed':'cue'}.get(focus)
        return not key or values.get(key,{}).get('status','unknown') in {'unknown','missing'}
    sequence_shot_ids = {sid for section in sections if section['id'] == selected_section
                         for sid in section.get('shotIDs', [])}
    candidates = [shot for shot in shots if shot['shotID'] in sequence_shot_ids and matches(shot)]
    def shot_statuses(shot):
        values = {value['key']: value for value in shot.get('fields', [])}
        return {field_status(values.get(definition['key'], {})) for definition in model.get('fields', [])}
    statuses = {shot['shotID']: shot_statuses(shot) for shot in candidates}
    status_counts = {status: sum(status in values for values in statuses.values()) for status in labels}
    status_options = ['all', *labels]
    status_key = f'structure-status:{project}'
    # Count labels change with the other filters. Keep the selected status even
    # when Streamlit treats those formatted options as a new widget identity.
    previous_status = st.session_state.get(status_key, 'all')
    status_filter = st.selectbox('Field status', status_options,
        index=status_options.index(previous_status) if previous_status in status_options else 0,
        format_func=lambda value: f'All field statuses · {len(candidates)}' if value == 'all'
            else f'{labels[value]} · {status_counts[value]}', key=status_key)
    by_shot = {shot['shotID']: shot for shot in candidates
               if status_filter == 'all' or status_filter in statuses[shot['shotID']]}
    st.caption(f'{len(by_shot)} of {len(candidates)} shots in this view. Match any of the '
               f"{len(model.get('fields', []))} main storyboard fields; kitchen subfields are excluded. "
               'Choose All field statuses to clear.')
    if not shots: st.info('No canonical shot structure is registered here yet. The full visual library also retains existing sequence maps. The blank template is available for inspection.')
    elif not by_shot:
        st.info('No shots in this sequence match these filters.')
    for section in record.get('sections',[]):
        if section['id']!=selected_section: continue
        visible=[by_shot[sid] for sid in section['shotIDs'] if sid in by_shot]
        if not visible: continue
        st.subheader(section['id']+' · '+section['title'])
        for shot in visible:
            sid = shot['shotID']
            selected_take = current_takes[sid]
            take_label = (f"Take {selected_take['number']} · " + ('written plan' if selected_take['state'] == 'written' else 'planned')) if selected_take else str(shot.get('revision') or 'Take 1').capitalize() + ' · written plan'
            if sid in branched_shots: take_label = 'Take branches · current unresolved'
            with st.expander(sid+' · '+shot.get('title', 'Untitled shot')+' · '+take_label+' · '+foundations[sid]['label'],
                             expanded=st.session_state.get(f'structure-shot-focus:{project}:{story["id"]}') == sid):
                if selected_take and selected_take['state'] == 'planned':
                    st.markdown('**Change for this take**')
                    st.text(selected_take['changeNote'])
                if sid in branched_shots:
                    st.warning('More than one take branch remains. No current take was chosen automatically; reconcile the saved branches before planning another.')
                foundation = foundations[shot['shotID']]
                with st.expander('Linked references'):
                    if shot.get('coverageUpdate'):
                        st.markdown('**Coverage notes' + (' · ' + shot['coverageAsOf'] if shot.get('coverageAsOf') else '') + '**')
                        st.text(shot['coverageUpdate'])
                        evidence([shot['coverageEvidence']] if shot.get('coverageEvidence') else [],
                                 f'structure-coverage:{project}:{shot["shotID"]}')
                    st.markdown('**Source foundation: ' + foundation['label'] + '**')
                    if foundation['dependencyReviewNeeded']:
                        st.warning('Selected input changed. Review dependent packs and checks; earlier decisions remain intact.')
                    for note in foundation.get('notes', []): st.write(note)
                    for index, item in enumerate(foundation.get('inputs', [])):
                        asset = assets.get(item.get('assetID'))
                        role = str(item.get('role') or 'Role not recorded').replace('_', ' ')
                        st.markdown('**' + role + ' · ' + (asset.get('title', asset['id']) if asset else item.get('assetID') or 'Missing asset') + '**')
                        if asset:
                            st.button('View selected input', key=f"foundation:{project}:{story['id']}:{shot['shotID']}:{index}",
                                      on_click=select_asset, args=(asset['id'], asset['project']))
                        st.caption('Source stage: ' + foundation_helper.STAGES.get(item.get('stage'), 'Maturity not recorded')
                                   + ' · Scope: ' + str(item.get('scope') or 'Not recorded'))
                        st.caption('Stage evidence: ' + item.get('stageSource', 'Not recorded'))
                        st.text('Selected SHA-256: ' + str(item.get('expectedSHA256') or 'Not recorded')
                                + '\nCurrent SHA-256: ' + str(item.get('actualSHA256') or 'Unavailable')
                                + '\nBytes: ' + str(item.get('bytes') if item.get('bytes') is not None else 'Not recorded'))
                        for note in item.get('notes', []): st.write(note)
                    if foundation.get('bindingEvidence'):
                        st.caption('Selection provenance')
                        provenance = foundation['bindingEvidence']
                        st.text('\n'.join(f'{key}: {value}' for key, value in provenance.items()) if isinstance(provenance, dict) else str(provenance))
                    if foundation_model.get('rules'):
                        with st.expander('Foundation rule source'):
                            rules = foundation_model['rules']
                            if isinstance(rules, dict):
                                st.text('\n'.join(f'{key}: {value}' for key, value in rules.items()))
                            elif isinstance(rules, list):
                                for rule in rules: st.write(rule)
                            else: st.text(str(rules))
                    materials = shot.get('materials', [])
                    st.caption(f'{len(materials)} linked references · {len(shot.get("pendingReferences", []))} recorded gaps')
                    for index, material in enumerate(materials):
                        asset = assets.get(material.get('assetID'))
                        if asset:
                            st.button(asset.get('title', asset['id']), key=f'material:{project}:{sid}:{index}',
                                      on_click=select_asset, args=(asset['id'], asset['project']))
                            st.caption(ROLES.get(material.get('role'), str(material.get('role') or 'Reference').replace('_', ' ')))
                        if material.get('note'): st.write(material['note'])
                    for pending in shot.get('pendingReferences', []):
                        st.write(pending)
                    legacy = shot.get('sourceShotPlanIDs', [])
                    if legacy:
                        st.caption('Earlier shot-plan IDs: '+', '.join(legacy))
                        st.caption('Source crosswalk only. These IDs remain distinct; their results and acceptance do not transfer to this authored shot.')
                        plans = {p['id']:p for p in data.get('shotMaterials',{}).get('shots',[])}
                        for legacy_id in legacy:
                            for i, material in enumerate(plans.get(legacy_id,{}).get('materials',[])):
                                asset = assets.get(material.get('assetID'))
                                if asset:
                                    st.button(legacy_id+' · '+asset.get('title',asset['id']), key=f"legacy:{project}:{shot['shotID']}:{legacy_id}:{i}", on_click=select_asset, args=(asset['id'],asset['project']))
                def field_group(title, keys, include_history=False):
                    definitions = [definition for definition in model['fields'] if definition['key'] in keys]
                    if not definitions and not include_history and 'purpose' not in keys:
                        return
                    values = {value['key']: value for value in shot.get('fields', [])}
                    group_matches = status_filter != 'all' and any(
                        field_status(values.get(definition['key'], {})) == status_filter for definition in definitions)
                    with st.expander(title, expanded=group_matches):
                        if 'purpose' in keys:
                            st.caption(shot.get('authoringStatus', 'Written plan'))
                            st.caption('Storyboard maturity: ' + STORYBOARD_STAGES.get(shot.get('stage'), shot.get('stage') or 'Not recorded'))
                            if sid in changed_sources:
                                st.info('Source writing changed after this take was saved. The saved plan remains intact; reconcile the newer writing before handoff.')
                            if section.get('spineBeat'): st.text(section['spineBeat'])
                            if section.get('context'): st.text(section['context'])
                        fields(definitions,shot['fields'],f"structure:{project}:{shot['shotID']}",fallback=shot.get('source'))
                        if include_history:
                            evidence([row for row in [shot.get('parent') or shot.get('source'),
                                                      *shot.get('priorDependencyEvidence', [])] if row],
                                     f"history:{project}:{shot['shotID']}")
                            if shot.get('revisions'):
                                st.warning('Proposed revision needs review; earlier take and results remain intact.')
                                for revision in shot['revisions']:
                                    st.write(revision['note']); evidence([revision['source']],f"revision:{shot['shotID']}:{revision['id']}")
                            st.caption('Changes to direction, cue, source or prompt require review of dependent packs. '
                                       'Earlier results and human reviews are retained; timings are never moved automatically.')
                            st.caption('Take numbers track written plans and revisions. They do not indicate that a video was generated.')
                            for saved_take in take_histories[sid]:
                                saved_label = (f"Take {saved_take['number']} · " if saved_take['number'] is not None else '') + ('written plan' if saved_take['state'] == 'written' else 'planned')
                                if selected_take and saved_take['id'] == selected_take['id']: saved_label += ' · current'
                                with st.expander(saved_label):
                                    st.caption(saved_take['recordedAt'] or 'Written source · recording time not supplied')
                                    if saved_take['changeNote']: st.text(saved_take['changeNote'])
                                    snapshot = saved_take['snapshot']
                                    fields(model['fields'], snapshot['shot'].get('fields', []),
                                           f'saved-take:{project}:{sid}:{saved_take["id"]}', fallback=snapshot['shot'].get('source'))
                                    fields(model['kitchenFields'], snapshot['shot'].get('kitchen', []),
                                           f'saved-kitchen:{project}:{sid}:{saved_take["id"]}', fallback=snapshot['shot'].get('source'))
                                    with st.expander('Frozen source, references and evidence'):
                                        st.json(snapshot)
                            with st.expander('Plan next take'):
                                st.caption('Save the current plan as history and start another planned take with your change brief. '
                                           'Nothing is generated; earlier results and acceptance stay with the earlier take.')
                                blocked = bool(take_error or take_backups or sid in branched_shots)
                                if st.session_state.pop(f'take-clear:{project}:{story["id"]}:{sid}', False):
                                    st.session_state[f'take-change:{project}:{story["id"]}:{sid}'] = ''
                                brief = st.text_area('What should change?', key=f'take-change:{project}:{story["id"]}:{sid}',
                                                     disabled=blocked)
                                if st.button('Plan next take', key=f'take-plan:{project}:{story["id"]}:{sid}',
                                             disabled=blocked or not brief.strip()):
                                    try:
                                        updated = take_helper.plan(take_ledger, dict(project=project, storyID=story['id'],
                                            shot=shot, foundation=foundation, changeNote=brief, id='take-'+str(uuid4()),
                                            recordedAt=datetime.now(timezone.utc).isoformat()))
                                        saved = current_module('library_helpers').review_provenance(
                                            {'storyboardTakes': updated}, st.session_state.get('studio_review_provenance', {}))
                                    except ValueError as error:
                                        st.error(str(error))
                                    else:
                                        st.session_state.studio_review_provenance = saved
                                        st.session_state[f'take-clear:{project}:{story["id"]}:{sid}'] = True
                                        st.session_state[f'take-saved:{project}:{story["id"]}:{sid}'] = True
                                        st.rerun()
                                if st.session_state.get(f'take-saved:{project}:{story["id"]}:{sid}'):
                                    st.success('Planned take saved in this session. Export the review file to keep it across devices.')
                field_group('Context & references · A–D', {'purpose', 'context', 'lineage', 'references'})
                field_group('Creative direction · 0–7',
                            {'start_frame', 'lighting', 'camera', 'character', 'background', 'beats', 'cue', 'prompt_still'})
                field_group('Generation handoff · 8–9', {'prompt_clip', 'settings'})
                field_group('Takes, results & review · 10–11', {'results', 'acceptance'}, include_history=True)
                kitchen_by_key = {value['key']: value for value in shot.get('kitchen', [])}
                kitchen_written = sum(
                    bool(str(kitchen_by_key.get(definition['key'], {}).get('text') or '').strip())
                    and kitchen_by_key.get(definition['key'], {}).get('status') in {'draft', 'present', 'verified', 'accepted', 'not_needed'}
                    for definition in model.get('kitchenFields', []))
                with st.expander(f'Kitchen / handoff structure · {kitchen_written}/{len(model.get("kitchenFields", []))} sections written'):
                    st.caption('Written sections describe the handoff; they do not indicate execution or acceptance.')
                    fields(model['kitchenFields'],shot.get('kitchen', []),f"kitchen:{project}:{shot['shotID']}",fallback=shot.get('source'))


def render_stories(data: dict, project: str, library_dir: Path, render_grid, select_asset, document_download, *, reviews: dict) -> None:
    stories = list({s["id"]: s for s in data.get("storyboardStories", []) if s.get("project") == project}.values())
    if not stories:
        st.info("No stories are registered for this project yet.")
        return
    by_id = {a["id"]: a for a in data["assets"]}
    sequences = {s["id"]: s for s in data.get("storyboardSequences", []) if s.get("project") == project}
    story_map = {s["id"]: s for s in stories}
    key = f"story-select:{project}"
    if st.session_state.get(key) not in story_map:
        st.session_state[key] = next((s["id"] for s in stories if s.get("kind") == "song"), stories[0]["id"])
    selected_id = st.selectbox("Story", list(story_map), format_func=lambda sid: story_map[sid]["title"], key=key)
    story = story_map[selected_id]
    if data.get('storyboardStructure'):
        view=st.radio('Storyboard view', ['Panels & writings','Structure & gaps'], horizontal=True,key=f'story-view:{project}')
        if view=='Structure & gaps':
            st.subheader('Storyboard structure')
            scene_reviews = st.session_state.get('studio_review_provenance', {}).get('sceneReviews', data.get('sceneReviews', []))
            render_structure(data,story,project,select_asset,reviews=reviews,scene_reviews=scene_reviews)
            return
    groups = {}
    for story in stories:
        group = story.get("group") or ("Series and seeds" if story.get("kind") == "prose" else "Stories")
        groups.setdefault(group, []).append(story)
    for group, group_stories in groups.items():
        unit = "storyboards" if group == "Stories" else "writing collections"
        st.subheader(f"{group} · {len(group_stories)} {unit}")
        for start in range(0, len(group_stories), 3):
            for column, story in zip(st.columns(3), group_stories[start:start + 3]):
                with column, st.container(border=True):
                    sequence = sequences.get(story.get("sequenceID"), {})
                    cover = by_id.get(story.get("coverID", sequence.get("coverID")))
                    preview = media_path(library_dir, cover.get("thumb")) if cover and normal_visible(cover, reviews) else None
                    if preview:
                        st.image(str(preview), width="stretch")
                    st.button(story["title"], key=f"story-cover:{story['id']}", on_click=choose_story,
                              args=(key, story["id"]), width="stretch", type="primary" if selected_id == story["id"] else "secondary")
                    st.caption({"song": "Song storyboard", "sequence": "Independent sequence", "prose": "Writings & development"}.get(story.get("kind"), "Story"))
                    if sequence.get("shots"):
                        coverage = sequence_coverage(sequence, by_id, reviews)
                        st.caption(f"{coverage['shots']} shots · {coverage['scenes']} scenes · {coverage['pending']} with pending references")
    story = story_map[selected_id]
    st.subheader(story["title"])
    if story.get("description"):
        st.write(story["description"])
    query = st.text_input("Find a shot or reference", key=f"story-search:{project}").casefold().split()
    def matches(value):
        text = json.dumps(value, ensure_ascii=False).casefold()
        return all(word in text for word in query)
    if story.get("kind") == "song":
        panels = song_panels(data, project, reviews)
        stage = st.selectbox("Stage", ["all", *STORYBOARD_STAGES], key=f"story-stage:{project}",
                             format_func=lambda value: "All stages" if value == "all" else STORYBOARD_STAGES[value])
        position = st.slider("Storyboard position (%)", 0, 100, (0, 100), step=5, key=f"story-position:{project}")
        rows = storyboard_window([(a, None) for a in panels if stage == "all" or storyboard_stage(a, reviews) == stage], *position)
        themes = sorted({theme for a, album in rows for theme in storyboard_themes(a, album)}, key=str.casefold)
        theme_key = f"story-themes:{project}"
        if theme_key in st.session_state:
            st.session_state[theme_key] = [t for t in st.session_state[theme_key] if t in themes]
        chosen = st.multiselect("Story themes", themes, key=theme_key)
        rows = [(a, album) for a, album in rows if matches(a) and (not chosen or any(t in storyboard_themes(a, album) for t in chosen))]
        st.caption("Source panel order, not song seconds. Independent sequences keep their own shot order.")
        render_grid(rows, f"story:song:{project}:{position}:{stage}:{chosen}:{query}")
    elif story.get("kind") == "sequence":
        sequence = sequences.get(story.get("sequenceID"), {})
        shots = sequence.get("shots", [])
        if shots:
            coverage = sequence_coverage(sequence, by_id, reviews)
            st.caption(f"{coverage['shots']} shots · {coverage['scenes']} scenes · {coverage['frames']} with frames · {coverage['results']} with a result on disk · {coverage['pending']} with pending references")
            st.info("Available material does not establish shot readiness. Setting stand-ins supply place and light; received results still need their own review.")
            shot_map = {s["shotID"]: s for s in shots}
            for index, section in enumerate(sequence.get("sections", [])):
                visible = [shot_map[sid] for sid in section.get("shotIDs", []) if sid in shot_map and matches(shot_map[sid])]
                if not visible:
                    continue
                with st.expander(f"Scene {section.get('scene', index + 1)} · {section['title']} · {len(visible)} shots", expanded=index == 0 or bool(query)):
                    for shot in visible:
                        with st.container(border=True):
                            st.markdown(f"**{shot['shotID']} · {shot.get('label', '')}**")
                            if shot.get("line"):
                                st.write(shot["line"])
                            materials = [m for m in shot.get("materials", []) if normal_visible(by_id.get(m.get("assetID")), reviews)]
                            preview = next((m for m in materials if m.get("role") in {"source_frame", "setting_stand_in"}), next(iter(materials), None))
                            if preview:
                                asset = by_id[preview["assetID"]]
                                path = media_path(library_dir, asset.get("thumb"))
                                if path:
                                    st.image(str(path), width=400)
                                st.caption(ROLES.get(preview.get("role"), preview.get("role", "Reference")))
                            else:
                                st.caption("No frame linked yet.")
                            if shot.get("pendingReferences"):
                                st.markdown("**Pending references**")
                                for label in shot["pendingReferences"]:
                                    st.write("• " + label)
                            with st.expander(f"Source material · {len(materials)} linked files"):
                                for n, material in enumerate(materials):
                                    asset = by_id[material["assetID"]]
                                    st.button(ROLES.get(material.get("role"), "Reference") + " · " + asset.get("title", asset["id"]),
                                              key=f"story-material:{story['id']}:{shot['shotID']}:{n}",
                                              on_click=select_asset, args=(asset["id"], project))
                                    if material.get("note"):
                                        st.caption(material["note"])
        else:
            for index, section in enumerate(sequence.get("sections", []) or [sequence]):
                refs = [by_id[aid] for aid in section.get("assetIDs", []) if normal_visible(by_id.get(aid), reviews) and matches(by_id[aid])]
                if refs:
                    with st.expander(section.get("title", "References"), expanded=not section.get("history")):
                        render_grid([(a, None) for a in refs], f"story:sequence:{story['id']}:{index}")
    else:
        st.info("No panels yet. This story is available as writings and development notes.")
    documents = [by_id[aid] for aid in story.get("documentIDs", []) if aid in by_id and by_id[aid].get("kind") in {"document", "pdf"}]
    if documents:
        st.subheader(f"Writings · {story['title']} · {len(documents)} documents")
        for asset in documents:
            with st.expander(asset.get("title", asset["id"])):
                if asset.get("text"):
                    st.text(asset["text"])
                document_download(asset, context=f"story:{story['id']}")

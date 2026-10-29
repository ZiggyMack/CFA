"""Story-specific browsing of the same panels, writings and shot evidence as the index."""
from __future__ import annotations

import json
from pathlib import Path

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


def render_structure(data, story, project, select_asset, *, reviews=None, scene_reviews=()):
    """Read the same evidence projection as the full mirror; never mutate reviews."""
    model = data.get('storyboardStructure', {})
    records = {s['storyID']: s for s in model.get('stories', [])}
    record = records.get(story['id'], {})
    mode = st.radio('Structure view', ['Planned shots', 'Blank storyboard / shot template'], horizontal=True,
                    key=f'structure-mode:{project}')
    labels = {'draft':'Draft', 'missing':'Missing', 'unknown':'Not assessed', 'present':'Present · unreviewed',
              'not_needed':'Intentionally not needed', 'verified':'Verified for stated scope', 'accepted':'Accepted for stated scope'}
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
            with st.expander(f"{definition.get('section', definition['key'])} · {definition['label']} — {'Empty template' if demo else labels.get(value.get('status','unknown'))}"):
                st.caption(definition['hint'])
                st.text(value.get('text') or ('No content entered.' if demo else 'No field-specific content recorded in this source.'))
                if value.get('note'): st.info(value['note'])
                st.caption(f"{definition.get('owner','Writer / CFA Nova')} · {definition.get('phase','handoff preparation')}")
                if not demo: evidence(value.get('evidence') or ([fallback] if fallback else []),f"{key}:{definition['key']}")
    if mode.startswith('Blank'):
        st.info('Structural preview only. No actual story, shot, review, queue item, export or production eligibility is created.')
        fields(model.get('fields',[]), [], f'template:{project}', True)
        st.subheader('11 · Kitchen / handoff structure')
        fields(model.get('kitchenFields',[]), [], f'template-kitchen:{project}', True)
        return
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
    foundation_counts = {state: sum(value['state'] == state for value in foundations.values())
                         for state in foundation_helper.LABELS}
    st.caption(f"{len(shots)} planned shots · {len(record.get('sections',[]))} sequences · {sum(bool(s.get('kitchenWritten')) for s in shots)} kitchen blocks documented · may contain gaps")
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
    by_shot={s['shotID']:s for s in shots if matches(s)}
    if not shots: st.info('No canonical shot structure is registered here yet. The full visual library also retains existing sequence maps. The blank template is available for inspection.')
    elif not any(s['shotID'] in by_shot for s in shots if s.get('sectionID') == selected_section):
        st.info('No shots in this sequence match these filters.')
    for section in record.get('sections',[]):
        if section['id']!=selected_section: continue
        visible=[by_shot[sid] for sid in section['shotIDs'] if sid in by_shot]
        if not visible: continue
        st.subheader(section['id']+' · '+section['title'])
        for shot in visible:
            with st.expander(shot['shotID']+' · '+shot['title']+' · '+foundations[shot['shotID']]['label']):
                st.caption(shot['revision']+' · '+shot['authoringStatus'])
                st.caption('Storyboard maturity: ' + STORYBOARD_STAGES.get(shot.get('stage'), shot.get('stage') or 'Not recorded'))
                foundation = foundations[shot['shotID']]
                st.markdown('**Source foundation: ' + foundation['label'] + '**')
                if foundation['dependencyReviewNeeded']:
                    st.warning('Selected input changed. Review dependent packs and checks; earlier decisions remain intact.')
                with st.expander('Selected input details'):
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
                fields(model['fields'],shot['fields'],f"structure:{project}:{shot['shotID']}",fallback=shot['source'])
                with st.expander('Kitchen / handoff structure'):
                    fields(model['kitchenFields'],shot['kitchen'],f"kitchen:{project}:{shot['shotID']}",fallback=shot['source'])
                if shot.get('revisions'):
                    st.warning('Proposed revision needs review; earlier take and results remain intact.')
                    for revision in shot['revisions']:
                        st.write(revision['note']); evidence([revision['source']],f"revision:{shot['shotID']}:{revision['id']}")


def render_stories(data: dict, project: str, library_dir: Path, render_grid, select_asset, document_download, *, reviews: dict) -> None:
    stories = [s for s in data.get("storyboardStories", []) if s.get("project") == project]
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
    for start in range(0, len(stories), 3):
        for column, story in zip(st.columns(3), stories[start:start + 3]):
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
        st.subheader("Writings · " + story["title"])
        for asset in documents:
            with st.expander(asset.get("title", asset["id"])):
                if asset.get("text"):
                    st.text(asset["text"])
                document_download(asset, context=f"story:{story['id']}")

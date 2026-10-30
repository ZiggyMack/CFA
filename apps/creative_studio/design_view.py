"""Native design workspaces matching the local index's scoped collections.

The model builders never change catalog records or review decisions. Streamlit is
imported only by the renderer so the grouping rules are independently testable.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path

from studio_dependencies import (
    approved_multiverse, cast_member_ids, cast_use_state, effective_design_data, effective_reviews, media_path,
    navigation_reference_count, normal_visible, storyboard_stage,
)

VIEWS = {
    "Working references": "working", "Outfits": "outfits", "Tattoos & piercings": "details",
    "Supporting cast": "cast", "Comfy swap targets": "comfy", "Archive": "archive",
}
OUTFIT_BUCKETS = (
    ("formal", "Formal attire", ("yellow", "cream", "fur", "velvet", "casino", "pinstripe")),
    ("casual", "Casual", ("rain", "baroque", "letterman", "bomber", "dragon", "parka", "puffer", "velour")),
    ("scoundrel", "Scoundrel gear", ("armor", "vest", "cash", "coat", "ice", "vinyl", "pilot", "saloon")),
)
DENTAL_STANDARD = "HD-B-91ef00348229"
LEGACY_TATTOO_PROOF = "HD-TATGUIDE-b6eb3258a6ae"
HISTORICAL_TATTOOS = (
    "HD-RETURN-d55b97a3b322", "HD-RETURN-78ad6c79615a", "HD-RETURN-f88ff5ae511e",
    "HD-TATGUIDE-b80e4d006917", "HD-RETURN-d91685dd99cd", "HD-TATGUIDE-d152270ab369",
    "HD-TATGUIDE-ad54ba356e7c", "HD-TATGUIDE-3046dd64faa8", "HD-TATGUIDE-440a8cf5e911",
)


def unique(values):
    return list(dict.fromkeys(v for v in values if v))


def section(title, ids=(), *, kind="gallery", description="", children=(), **extra):
    return {"title": title, "kind": kind, "assetIDs": unique(ids), "description": description,
            "sections": list(children), **extra}


def model_asset_ids(node):
    """All reachable references, in order, counted once per enclosing card."""
    ids = list(node.get("assetIDs", []))
    for child in [*node.get("sections", []), *node.get("groups", [])]:
        ids.extend(model_asset_ids(child))
    ids.extend(row["assetID"] for row in node.get("rows", []))
    return unique(ids)


class Context:
    def __init__(self, data, project, reviews=None, query="", archive=False):
        self.reviews = reviews if reviews is not None else effective_reviews(
            data.get("assets", []), data.get("reviewDecisions", []), {}, aliases=data.get("assetAliases", []))
        self.data = effective_design_data(data, self.reviews)
        self.by_id = {a["id"]: a for a in self.data.get("assets", [])}
        self.albums = {a["id"]: a for a in self.data.get("albums", [])}
        self.project, self.query, self.archive = project, query.casefold().strip(), archive
        self.bom = next((c for c in data.get("characterBOM", {}).get("characters", []) if c.get("project") == project), {})
        self.roles = {e["assetID"]: e for e in self.bom.get("entries", [])}

    def review(self, aid):
        return self.reviews.get(aid, {})

    def visible(self, asset):
        return bool(asset) and (bool(asset.get("archived")) if self.archive else normal_visible(asset, self.reviews))

    def matches(self, asset, text=""):
        return not self.query or self.query in " ".join(str(v) for v in (
            text, asset.get("title", ""), asset.get("filename", ""), asset.get("album", ""),
            asset.get("note", ""), self.review(asset["id"]).get("note", ""), asset.get("tags", []))).casefold()

    def ids(self, ids, text="", shared=()):
        shared_ids = {r["assetID"] for r in shared if r.get("assetID") in self.by_id
                      and self.by_id[r["assetID"]].get("sha256") == r.get("sha256")
                      and self.by_id[r["assetID"]].get("project") == r.get("sourceProject")}
        return [aid for aid in unique(ids) if (a := self.by_id.get(aid)) and self.visible(a)
                and (a.get("project") == self.project or aid in shared_ids) and self.matches(a, text)]

    def group(self, source, sections=None):
        text = " ".join(str(source.get(k, "")) for k in ("title", "role", "aliases"))
        ids = self.ids(source.get("assetIDs", []), text, source.get("sharedReferences", []))
        if not ids:
            return None
        sections = sections if sections is not None else source.get("sections")
        remaining, children = set(ids), []
        for s in sections or [section("References", ids)]:
            taken = [aid for aid in s.get("assetIDs", []) if aid in remaining]
            remaining.difference_update(taken)
            if taken or s.get("emptyMessage"):
                children.append(section(s.get("title", "References"), taken,
                    kind="disclosure" if s.get("history") or s.get("collapsible") else "gallery",
                    description=s.get("description", ""), emptyMessage=s.get("emptyMessage", ""),
                    overview=s.get("overview", False)))
        if remaining:
            children.append(section("Related references", [aid for aid in ids if aid in remaining]))
        cover = next((aid for aid in (source.get("coverID"), source.get("coverAssetID"), source.get("representativeID")) if aid in ids), None)
        return {"id": source["id"], "title": source.get("title", source["id"]), "assetIDs": ids,
                "coverID": cover or portrait_cover([self.by_id[aid] for aid in ids], self.reviews),
                "description": source.get("description", ""), "role": source.get("role", ""),
                "notes": list(source.get("notes", [])), "sections": children,
                "sourceAlbumIDs": list(source.get("sourceAlbumIDs", []))}


def portrait_cover(assets, reviews):
    def rank(a):
        text = " ".join(str(a.get(k, "")) for k in ("title", "filename", "viewRole", "referenceRole"))
        sheet = bool(re.search(r"contact|all.views|reference.sheet|[_-]sheet", text, re.I))
        portrait = not sheet and re.search(r"portrait|head.?shot|chest.?up|bust", text, re.I)
        return (0 if portrait else 3 if sheet else 1 if re.search("front", text, re.I) else 2,
                reviews.get(a["id"], {}).get("variant", a.get("variant")) == "multiverse",
                reviews.get(a["id"], {}).get("status") == "needs_fixes")
    return min(assets, key=rank)["id"] if assets else None


def bom_entries(ctx):
    entries = []
    for a in ctx.by_id.values():
        if a.get("project") != ctx.project or a.get("kind") not in {"image", "video", "gif"} or not ctx.visible(a):
            continue
        r, mapped = ctx.review(a["id"]), ctx.roles.get(a["id"], {})
        lock = next((c for c in a.get("componentApprovals", []) if c.get("sourceSHA256") == a.get("sha256") and c.get("status") == "user_selected_component"), {})
        recorded = mapped.get("recordedSelection") or bool(lock)
        approved = recorded or (r.get("workingReference") or {}).get("status") == "approved" or storyboard_stage(a, ctx.reviews) == "production"
        if not approved or r.get("variant", a.get("variant")) == "multiverse" or r.get("status") == "needs_fixes" and not recorded:
            continue
        working = r.get("workingReference") or {}
        role = mapped.get("role") or lock.get("scope") or (working.get("scope") if working.get("status") == "approved" else None)
        role = role or (r.get("workingReferenceScope") if r.get("workingReferenceScope") in {"outfit", "detail"} else "scene")
        group = mapped.get("section") or ("identity" if role in {"identity", "complete_look"} else "wardrobe" if role == "outfit" else "details" if role == "detail" else "scene")
        if ctx.matches(a):
            entries.append({"assetID": a["id"], "role": role, "section": group, "recordedSelection": bool(recorded)})
    return sorted(entries, key=lambda e: not e["recordedSelection"])


def cast_working_groups(ctx):
    approved = {e["assetID"] for e in bom_entries(ctx) if e["role"] in {"identity", "complete_look"}}
    result = []
    for g in ctx.data.get("castCollections", []):
        if g.get("project") != ctx.project:
            continue
        selected = g.get("workingReferenceIDs", [])
        parts = [section("Approved design references", [a for a in g.get("currentIDs", g.get("assetIDs", [])) if a in approved]),
                 section("Selected design references", selected, description="Selected working set; per-image approvals and ratings remain as recorded."),
                 section("Design reference candidates", unique([*g.get("referenceAssetIDs", []), *g.get("currentIDs", [])]), collapsible=True),
                 section("Animation/setup candidates", unique([*g.get("setupAssetIDs", []), *g.get("candidateSetupIDs", [])]), collapsible=True),
                 section("Boss dais · character and staging candidates", g.get("characterStudyIDs", []),
                         description="Returned studies of the selected boss. Individual reviews remain separate."),
                 section("Counting room · scene candidates", g.get("sceneStudyIDs", [])),
                 section("Earlier repair versions", g.get("revisionStudyIDs", []), collapsible=True),
                 section("Earlier studies", g.get("historicalReferenceIDs", g.get("historyIDs", [])), collapsible=True)]
        group = ctx.group({**g, "id": g["id"] + "-working", "assetIDs": unique(a for s in parts for a in s["assetIDs"])}, parts)
        if group:
            group["castCollectionID"] = g["id"]
            group["role"] = "Scoped design and animation references"
            result.append(group)
    return result


def mouth_sections(ctx):
    board = ctx.data.get("mouthCoverage", {})
    sections = []
    for look in board.get("looks", []):
        if look.get("project") != ctx.project or look.get("history") or look.get("planStatus") == "History only":
            continue
        rows = [r for r in board.get("items", []) if r.get("lookID") == look["id"]
                and (a := ctx.by_id.get(r.get("assetID"))) and a.get("sha256") == r.get("sha256") and ctx.visible(a)]
        keys = look.get("plannedNumbers") or unique(r.get("number") or r["assetID"] for r in rows)
        buckets = [("Core articulation labels", lambda n: n in board.get("articulationNumbers", [])),
                   ("Extended delivery / phonetic labels", lambda n: n in board.get("extendedNumbers", [])),
                   ("Expression / action labels", lambda n: type(n) is int and n not in board.get("articulationNumbers", []) + board.get("extendedNumbers", [])),
                   ("Accessory and unnumbered references", lambda n: type(n) is not int)]
        children = []
        for title, predicate in buckets:
            slots = []
            for number in keys:
                if not predicate(number):
                    continue
                takes = [r for r in rows if (r.get("number") or r["assetID"]) == number]
                visible_takes = [r for r in takes if ctx.matches(ctx.by_id[r["assetID"]], " ".join(str(v) for v in (
                    look.get("title", ""), r.get("label", ""), r.get("revision", ""), r.get("yaw", ""), r.get("pitch", ""))))]
                if ctx.query and not visible_takes and ctx.query not in (look.get("title", "") + " " + title + " " + str(number)).casefold():
                    continue
                takes = visible_takes if ctx.query and visible_takes else takes
                ids = [r["assetID"] for r in takes]
                label = next((r["label"].strip() for r in takes if isinstance(r.get("label"), str) and r["label"].strip()),
                             "Unlabeled reference") if takes else "Missing candidate"
                slots.append({"number": number, "label": label,
                    "assetIDs": ids, "takes": [dict(r) for r in takes],
                    "observations": [dict(o) for o in board.get("observations", []) if o.get("assetID") in ids],
                    "note": "09/10 have different bytes and overlapping teeth-baring poses. Distinct articulation remains uncertain; original reviews are retained."
                        if look["id"] == "hon-external-off" and number in {9, 10} else ""})
            if slots:
                ids = unique(aid for slot in slots for aid in slot["assetIDs"])
                grid = section(title, ids, kind="mouth_slots", slots=slots, emptyMessage="No received candidates for these planned labels." if not ids else "")
                children.append(section(title + " · " + str(len(slots)), kind="disclosure", children=[grid],
                                        emptyMessage="No received candidates for these planned labels." if not ids else ""))
        if look.get("referenceAssetID"):
            children.insert(0, section("Selected scoped look", ctx.ids([look["referenceAssetID"]])))
        head = board.get("headPlan", {})
        if head:
            children.append(section("Yaw, pitch, stable look and jewelry are separate axes", kind="disclosure",
                description=head.get("note", ""), emptyMessage=f"Recorded head-state slots: {head.get('receivedSlots', 'unknown')} / {head.get('baseSlots', 'unknown')}. Optional expansion: {head.get('expandedUniqueSlots', 'unknown')} unique slots; key-state selection is not accepted. Unknown fields stay unknown; no opposite view is inferred by mirroring."))
        sections.append(section(look.get("title", look["id"]), kind="disclosure", children=children, expanded=True,
            description=" ".join(str(look.get(k, "")) for k in ("stableLook", "planStatus", "note")),
            emptyMessage="No candidate images have been received for this look." if not rows else ""))
    return sections


def verbose_bom(ctx, candidates):
    definitions = [g for g in ctx.data.get("sharedReferenceCollections", []) if g.get("project") == ctx.project]
    covered = {aid for g in definitions for aid in g.get("sourceAlbumIDs", [])}
    fallback = [al for al in ctx.albums.values() if al.get("project") == ctx.project and al["id"] not in covered
                and (al.get("category") == "comfy" and re.search(r"head|mouth|viseme|breather", al["id"] + al.get("title", ""), re.I)
                     or al["id"] in {ctx.project + ":grillz", ctx.project + ":mouth-detail-updates"})]
    groups = [g for source in [*definitions, *fallback]
              if (g := ctx.group(source, [s for s in source.get("sections", []) if not s.get("history")] or None))]
    board = ctx.data.get("mouthCoverage", {})
    recipe = board.get("recipe", {})
    readiness = []
    if recipe:
        readiness.append(section("Recipe input readiness", kind="disclosure", emptyMessage="\n\n".join(str(v) for v in (
            recipe.get("title"), recipe.get("checkpoint"), recipe.get("clipEvidence"), *recipe.get("inputs", []),
            recipe.get("result"), recipe.get("lisanStatus"), recipe.get("faceDriverConcern"), board.get("clipProofRequirements")) if v),
            description=f"{recipe.get('requiredStillAtlasSlots', 'Unknown')} still-atlas slots required by this saved graph. Mouth-bank availability is a separate measure."))
    guide = ctx.ids(a["id"] for a in ctx.by_id.values() if a.get("repoPath", "").endswith("/visual_library/REFERENCE_VALIDATION_GUIDE.txt"))
    return section("Verbose BOM", kind="disclosure", expanded=True, description="Reusable heads, mouths and broader options. Each keeps its own scope and review.",
        children=[section("Reusable reference collections", kind="collections", groups=groups),
                  section("Mouth coverage board", kind="section", children=[*readiness, *mouth_sections(ctx), section("Evidence, reviewer and backup guide", guide)],
                          description="Provider labels combine articulation, expressions and actions. Multiple takes or different bytes do not establish distinct usable articulation; still evidence never proves temporal speech."),
                  section("Multiverse candidates", candidates, kind="disclosure", description="Unselected and low-rated ideas remain candidates. Ratings do not select an alternative.")])


def working_model(ctx, album_id):
    cast = cast_working_groups(ctx)
    if album_id and (specific := [g for g in cast if album_id in {g["id"], g["castCollectionID"]}]):
        return [section("Character bill of materials", kind="collections", groups=specific)]
    album = ctx.albums.get(album_id, {})
    if album.get("project") == ctx.project and album.get("category") == "details" and (
            album_id in {"hon:grillz", "hon:mouth-detail-updates"}
            or ctx.project == "lisan" and re.search(r"mouth|grill", album_id, re.I)):
        group = ctx.group(album)
        return [section("References", kind="collections", groups=[group] if group else [])]
    supporting = {aid for g in cast for aid in g["assetIDs"]}
    entries = [e for e in bom_entries(ctx) if e["assetID"] not in supporting]
    mouths = {r["assetID"] for r in ctx.data.get("mouthCoverage", {}).get("items", [])
              if ctx.by_id.get(r.get("assetID"), {}).get("sha256") == r.get("sha256")}
    compact = [e for e in entries if ctx.project != "hon" or e["section"] != "details" or e["assetID"] == DENTAL_STANDARD
               or not (e["assetID"] in mouths or e["role"] in {"dental_mouth_only", "mouth_detail"}
                       or ctx.by_id[e["assetID"]].get("album", "").startswith("hon:mouth-"))]
    candidates = [a["id"] for a in ctx.by_id.values() if a.get("project") == ctx.project and a.get("kind") in {"image", "video", "gif"}
                  and ctx.visible(a) and ctx.matches(a) and ctx.review(a["id"]).get("variant", a.get("variant")) == "multiverse"]
    cover = ctx.bom.get("coverAssetID")
    if not ctx.visible(ctx.by_id.get(cover)):
        cover = next((e["assetID"] for e in entries if e["role"] == "identity"), entries[0]["assetID"] if entries else None)
    parts = []
    board = ctx.data.get("characterReferenceBoard", {})
    if board.get("project") == ctx.project:
        rows = [{**row, "assetID": row["asset"]["id"]} for row in board.get("rows", [])
                if (a := ctx.by_id.get(row.get("asset", {}).get("id"))) and a.get("sha256") == row["asset"].get("sha256") and ctx.visible(a) and ctx.matches(a, row.get("label", "") + " " + row.get("scope", ""))]
        parts.append(section(board.get("title", "Character references"), kind="reference_board", rows=rows, description=" ".join(str(board.get(k, "")) for k in ("scopeNotice", "portraitContext"))))
    for key, title in (("identity", "Default identity"), ("details", "Approved details and placement"), ("artwork", "Body art")):
        parts.append(section(title, [e["assetID"] for e in compact if e["section"] == key and e["assetID"] != cover]))
    accessories = [g for source in ctx.data.get("accessoryCollections", []) if source.get("project") == ctx.project and (g := ctx.group(source))]
    parts.append(section("Bling bling", kind="collections", groups=accessories, description="Jewelry and hand details for any outfit or shot; recorded component scope is retained."))
    parts.extend([section("Wardrobe", [e["assetID"] for e in compact if e["section"] == "wardrobe"]),
                  section("Optional accessories and looks", [e["assetID"] for e in compact if e["section"] == "optional"], description="Selected Prime options; these do not replace default identity."),
                  section("Approved Multiverse", [aid for aid in candidates if approved_multiverse(ctx.by_id[aid], ctx.reviews)],
                          emptyMessage="No approved Multiverse selections yet. Choose explicitly in an image review; likeness must be at least 2/5.",
                          description="Explicitly selected alternatives. This selection does not approve production."),
                  section("Video production candidates", [e["assetID"] for e in entries if e["section"] == "scene"], description="For the named shot or motion only; finished video acceptance remains separate.")])
    wip = [a["id"] for a in ctx.by_id.values() if a.get("project") == ctx.project and a["id"] not in supporting and ctx.visible(a) and ctx.matches(a)
           and storyboard_stage(a, ctx.reviews) == "production" and (ctx.review(a["id"]).get("variant", a.get("variant")) == "multiverse" or ctx.review(a["id"]).get("status") == "needs_fixes")]
    parts.extend([section("WIP (work in progress)", wip, kind="disclosure"), verbose_bom(ctx, candidates)])
    groups = cast
    if cover and (entries or model_asset_ids({"sections": parts})):
        name = next((p.get("name", ctx.project) for p in ctx.data.get("projects", []) if p["id"] == ctx.project), ctx.project)
        lead = {"id": ctx.bom.get("id", ctx.project + ":character-bom"), "title": name, "coverID": cover,
                "assetIDs": unique([cover, *model_asset_ids({"sections": parts})]), "sections": parts,
                "description": "Each selected part retains its own role. A component choice does not approve the entire image."}
        groups = [lead, *cast]
    return [section("Character bill of materials", kind="collections", groups=groups)]


def outfit_model(ctx, album_id):
    groups = []
    for al in ctx.albums.values():
        if al.get("project") != ctx.project or al.get("category") != "outfits" or album_id and al["id"] != album_id:
            continue
        group = ctx.group(al)
        if group:
            group["coverID"] = portrait_cover([ctx.by_id[aid] for aid in group["assetIDs"]], ctx.reviews)
            group["sections"] = [section("Views and variants", group["assetIDs"])]
            groups.append(group)
    if ctx.project != "hon" or album_id:
        return [section("Outfits", kind="collections", groups=groups)]
    lookup = {"hon:outfit-" + name: key for key, _, names in OUTFIT_BUCKETS for name in names}
    return [section(title, kind="outfit_bucket", groups=[g for g in groups if lookup.get(g["id"], "casual") == key], bucketID=key)
            for key, title, _ in OUTFIT_BUCKETS]


def tattoo_groups(ctx):
    definitions = [g for g in ctx.data.get("detailDisplayGroups", []) if g.get("project") == ctx.project]
    if ctx.project != "hon":
        return [g for source in definitions if (g := ctx.group(source))]
    art = [g for g in definitions if g.get("bucket") == "stencils"]
    keys = ["ship", "eye", "know", "blaster", "leigh", "scoundrel", "optional-motifs"]
    art.sort(key=lambda g: keys.index(g["id"][11:-4]) if g["id"].startswith("hon:detail-") and g["id"][11:-4] in keys else len(keys))
    objects = [o for p in ctx.data.get("detailProfiles", []) if p.get("project") == "hon" for o in p.get("objects", [])]
    profiles = {"ship": ["hon-chest-current", "hon-ship-perspective", "hon-ship-schematic"], "eye": ["hon-eye"], "know": ["hon-know"],
                "blaster": ["hon-neck-blaster"], "leigh": ["hon-hand-card"], "scoundrel": ["hon-forearm-scoundrel"], "optional-motifs": ["hon-bird-optional"]}
    related = {"eye": ["HD-RETURN-3fa3290e85db"], "know": ["HD-RETURN-3fa3290e85db"], "scoundrel": ["HD-TATGUIDE-1fd07b088244"],
               "leigh": ["HD-RETURN-831f6171619f", "HD-RETURN-b8c9247bfe47"], "optional-motifs": ["HD-TATGUIDE-1fd07b088244"]}
    dedicated = {"ship": ["hon:ship-tattoo"], "leigh": ["hon:leigh-hand-options"]}
    guides = [*ctx.data.get("tattooPlacementGuides", []), *(g for g in definitions if g.get("bucket") == "guides" and g.get("tattooKey"))]
    general_guides = {aid for g in definitions if g.get("bucket") == "guides" and not g.get("tattooKey") for aid in g.get("assetIDs", [])}
    result = []
    for source in art:
        key = source["id"].removeprefix("hon:detail-").removesuffix("-art")
        body = next((g for g in definitions if g["id"] == "hon:detail-" + key + "-skin"), {})
        profile = [o for o in objects if o.get("id") in profiles.get(key, []) or o.get("id") == source.get("sourceObjectID")]
        seen = set()
        def take(ids):
            selected = []
            for aid in ctx.ids(ids, source.get("title", "")):
                a = ctx.by_id[aid]
                if a.get("kind") not in {"image", "video", "gif"}:
                    continue
                digest = a.get("sha256") or aid
                if digest not in seen:
                    selected.append(aid); seen.add(digest)
            return selected
        guide_records = [g for g in guides if g.get("project") == "hon" and g.get("tattooKey") == key]
        maps = take(aid for g in guide_records for aid in g.get("assetIDs", []))
        proof = take([LEGACY_TATTOO_PROOF] if key in {"ship", "eye", "know", "blaster", "scoundrel", "optional-motifs"} else [])
        comparison = {aid for s in source.get("sections", []) if s.get("history") for aid in s.get("assetIDs", [])}
        artwork = take([*(aid for aid in source.get("assetIDs", []) if aid not in comparison),
                        *(aid for o in profile for aid in [*o.get("artworkAssetIDs", []), *o.get("stencilAssetIDs", [])])])
        comparisons = take([*(aid for aid in source.get("assetIDs", []) if aid in comparison), *related.get(key, [])])
        appearances = take([*body.get("assetIDs", []), *(aid for aid in source.get("relatedAssetIDs", []) if aid not in general_guides),
                            *(aid for o in profile for aid in o.get("exampleAssetIDs", [])), *(aid for al in dedicated.get(key, []) for aid in ctx.albums.get(al, {}).get("assetIDs", []))])
        cover = next((aid for aid in [source.get("coverAssetID"), source.get("coverID"), *artwork] if aid in artwork), None)
        overview = [section("Artwork / stencil", [cover] if cover else [], emptyMessage="No separate artwork reference is available."),
                    section("Placement and mannequin guide", maps, description=" ".join(g.get("description", g.get("status", "")) for g in guide_records), emptyMessage="Dedicated placement guide pending.")]
        if proof:
            overview.append(section("Legacy placement proof · revision needed", proof, description="Placement only; recorded defects remain. Not accepted as identity, teeth, a complete look or exact transfer."))
        children = [section("Artwork and placement", kind="columns", children=overview), section("More stencil and artwork options", [a for a in artwork if a != cover]),
                    section("Body appearances", appearances), section("Source sheets and comparison evidence", comparisons, kind="disclosure")]
        ids = model_asset_ids({"sections": children})
        if ids:
            result.append({"id": "hon:tattoo-" + key, "title": source.get("title", key), "coverID": cover or ids[0], "assetIDs": ids,
                           "sourceAlbumIDs": unique([*source.get("sourceAlbumIDs", []), *body.get("sourceAlbumIDs", []), source.get("albumID"), body.get("albumID"),
                                                     *dedicated.get(key, []), *(ctx.by_id[aid].get("album") for aid in ids)]),
                           "sections": children, "description": "Artwork, placement guides and body evidence retain their distinct scopes and reviews."})
    return result


def detail_model(ctx, album_id=""):
    tattoo = tattoo_groups(ctx)
    claimed = {aid for g in tattoo for aid in g["assetIDs"]}
    designs = [DENTAL_STANDARD, "HD-GRILLUP-40064d98db89"] if ctx.project == "hon" else ["LAG-cb183973ed1fc70e"]
    other = []
    grills = ctx.group({"id": ctx.project + ":grill-designs", "title": "Grills", "assetIDs": designs, "coverID": designs[0],
                       "sourceAlbumIDs": [ctx.project + ":grillz", ctx.project + ":mouth-detail-updates"],
                       "description": "One clear reference per grill design. Mouth positions stay in Working references."})
    if grills:
        other.append(grills)
    setup = {aid for g in ctx.data.get("castCollections", []) if g.get("project") == ctx.project
             for key in ("setupAssetIDs", "candidateSetupIDs", "referenceAssetIDs") for aid in g.get(key, []) if aid != (g.get("representativeID") or g.get("coverID"))}
    excluded = {"hon:grillz", "hon:mouth-detail-updates", "hon:face-neck-ink", "hon:optional-finish"}
    for al in ctx.albums.values():
        if al.get("project") != ctx.project or al.get("category") != "details" or al["id"] in excluded:
            continue
        source = {**al, "assetIDs": [aid for aid in al.get("assetIDs", []) if aid not in claimed | setup]}
        if al["id"] == "hon:piercings":
            accessories = [g for g in ctx.data.get("accessoryCollections", []) if g.get("project") == "hon"]
            source.update(title="Piercings and jewelry", assetIDs=unique([*source["assetIDs"], *(aid for g in accessories for aid in g.get("assetIDs", []))]),
                sections=[section("Jewelry on display", emptyMessage="Standalone display references are pending; no returned display-image package is recorded."),
                          section("Dolo · earrings and facial piercings", source["assetIDs"], collapsible=True),
                          *(dict(s, title="Dolo · " + s["title"], collapsible=True) for g in accessories for s in g.get("sections", []))])
        if al["id"] == "hon:return-detail-art" and source["assetIDs"] == ["HD-RETURN-41b93f64e7ea"]:
            source.update(title="Guns", description="On-character evidence. Standalone display images and accepted variations are pending.")
        if g := ctx.group(source):
            other.append(g)
    if album_id:
        def matches(group):
            return group["id"] == album_id or album_id in group.get("sourceAlbumIDs", []) or any(ctx.by_id[aid].get("album") == album_id for aid in group["assetIDs"])
        tattoo, other = [g for g in tattoo if matches(g)], [g for g in other if matches(g)]
    return [section("Tattoos", kind="collections", groups=tattoo), section("Piercings, grills and props", kind="collections", groups=other)]


def cast_browse_facts(ctx, source, visible_ids):
    """Recorded origins and story links; scene folders alone never imply use."""
    sources = [{"id": album["id"], "title": album.get("title", album["id"])}
               for aid in unique(source.get("sourceAlbumIDs", []))
               if (album := ctx.albums.get(aid)) and album.get("project") == ctx.project]
    identity_ids = unique([source.get("representativeID"), source.get("coverID"),
                           *source.get("currentIDs", []), *source.get("workingReferenceIDs", [])])
    member_ids = unique([*cast_member_ids(source), *visible_ids])
    members = [asset for aid in member_ids if (asset := ctx.by_id.get(aid)) and asset.get("project") == ctx.project]
    states = {asset["id"]: cast_use_state(ctx.data, asset, ctx.reviews) for asset in members}
    choices = [{**asset, "characterRole": states[asset["id"]]["role"],
                "manualCastChoice": isinstance(ctx.review(asset["id"]).get("castUse"), dict)}
               for asset in members if states[asset["id"]]["roleSelected"]
               and (asset["id"] in identity_ids or isinstance(ctx.review(asset["id"]).get("castUse"), dict))]
    ids = set(visible_ids)
    shots = [shot for shot in ctx.data.get("shotMaterials", {}).get("shots", [])
             if shot.get("project") == ctx.project and (shot.get("characterCollectionID") == source["id"]
             or any(aid in ids for aid in shot.get("panelAssetIDs", []))
             or any(material.get("assetID") in ids and material.get("sha256")
                    and ctx.by_id.get(material["assetID"], {}).get("sha256") == material["sha256"]
                    for material in shot.get("materials", [])))]
    sequences = [sequence for sequence in ctx.data.get("storyboardSequences", [])
                 if sequence.get("project") == ctx.project and any(aid in ids for aid in sequence.get("assetIDs", []))]
    manual_plans, manual_links, unresolved = [], [], []
    for asset in members:
        state = states[asset["id"]]
        if state["storyboardPlanned"] or state["validLinks"]:
            manual_plans.append({"id": "manual:"+asset["id"], "assetID": asset["id"],
                                 "title": asset.get("title", asset["id"])+" · planned by you"})
        targets = {(row["storyID"], row["shotID"]): row for row in state["targets"]}
        for link in state["validLinks"]:
            target = targets[(link["storyID"], link["shotID"])]
            manual_links.append({**link, "assetID": asset["id"], "title": target["storyTitle"]+" · "+target["shotID"]+" · "+target["shotTitle"]})
        unresolved.extend({**link, "assetID": asset["id"]} for link in state["unresolvedLinks"])
    return {"sources": sources, "choices": choices, "roles": bool(choices),
            "planned": [shot for shot in shots if not shot.get("panelAssetIDs")]+manual_plans,
            "linked": [shot for shot in shots if shot.get("panelAssetIDs")]+manual_links,
            "sequences": sequences, "unresolved": unresolved}


def cast_browse_groups(groups, source="all", connection="all"):
    def matches(group):
        facts = group.get("browseFacts", {})
        if source != "all" and not any(item["id"] == source for item in facts.get("sources", [])):
            return False
        if connection == "roles":
            return bool(facts.get("roles"))
        if connection == "planned":
            return bool(facts.get("planned"))
        if connection == "linked":
            return bool(facts.get("linked") or facts.get("sequences"))
        return True
    return [group for group in groups if matches(group)]


def cast_model(ctx, album_id):
    definitions = [g for g in ctx.data.get("castCollections", []) if g.get("project") == ctx.project and g["id"] != "hon:creature-ideas"]
    exact_character = any(g["id"] == album_id for g in definitions)
    covered = {aid for g in definitions for aid in g.get("assetIDs", [])}
    definitions += [{**al, "assetIDs": [aid for aid in al.get("assetIDs", []) if aid not in covered]} for al in ctx.albums.values()
                    if al.get("project") == ctx.project and al.get("category") == "cast" and al["id"] != "hon:creature-ideas"]
    groups = []
    for source in definitions:
        if album_id and album_id != source["id"] and (exact_character or album_id not in source.get("sourceAlbumIDs", [])):
            continue
        # The character cover and recorded scene/video appearances lead the hub.
        representative = next(iter(ctx.ids([source.get("representativeID"), source.get("coverID"), source.get("coverAssetID"), *source.get("currentIDs", []), *source.get("workingReferenceIDs", [])])), None)
        discovery = bool(source.get("preferredIDs")) or bool(source.get("sections") and not source.get("currentIDs"))
        ids = unique([*(source.get("assetIDs", []) if discovery or not representative else [representative]),
                      *source.get("sceneAssetIDs", []), *source.get("videoAssetIDs", []), *source.get("relatedAssetIDs", [])])
        parts = list(source.get("sections", [])) if discovery else []
        if source.get("preferredIDs"):
            parts = [section("Your shortlist", source["preferredIDs"]), section("Other candidates", [a for a in ids if a not in source["preferredIDs"]], collapsible=True)]
        studies = set(unique([*source.get("characterStudyIDs", []), *source.get("sceneStudyIDs", []), *source.get("revisionStudyIDs", [])]))
        parts += [section("Boss dais · character and staging candidates", source.get("characterStudyIDs", [])),
                  section("Counting room · scene candidates", source.get("sceneStudyIDs", [])),
                  section("Earlier repair versions", source.get("revisionStudyIDs", []), collapsible=True),
                  section("Scene appearances", [aid for aid in source.get("sceneAssetIDs", []) if aid not in studies], collapsible=True),
                  section("Video appearances", source.get("videoAssetIDs", []), collapsible=True),
                  section("Related story material", source.get("relatedAssetIDs", []), collapsible=True)]
        group = ctx.group({**source, "assetIDs": ids, "coverID": representative}, parts)
        if group:
            group["browseFacts"] = cast_browse_facts(ctx, source, group["assetIDs"])
            working = next((g for g in cast_working_groups(ctx) if g["castCollectionID"] == source["id"]), None)
            if working:
                group["sections"].append(section("Design and animation references", kind="collections", groups=[working]))
                group["assetIDs"] = model_asset_ids(group)
            groups.append(group)
    result = [section("Supporting cast", kind="collections", groups=groups)]
    if ctx.project == "hon" and album_id in {"", "hon:creature-ideas"}:
        boss = ctx.albums.get("hon:creature-ideas", {})
        result.append(section("Creature boss ideas", ctx.ids(boss.get("assetIDs", []), boss.get("title", "")), description="Earlier options, separate from selected character hubs. Inclusion does not approve a character."))
    return result


def archive_model(ctx):
    available = [a["id"] for a in ctx.by_id.values() if a.get("project") == ctx.project and ctx.visible(a) and ctx.matches(a)]
    removals = [a['id'] for a in ctx.by_id.values() if a.get('project') == ctx.project
                and not a.get('archived') and ctx.review(a['id']).get('status') == 'remove' and ctx.matches(a)]
    definitions = [{"id": "hon:tattoo-source-history", "title": "Earlier tattoo alternatives and source sheets", "assetIDs": HISTORICAL_TATTOOS}] if ctx.project == "hon" else []
    for g in ctx.data.get("sharedReferenceCollections", []):
        if g.get("project") == ctx.project:
            definitions.extend({"id": g["id"] + ":archive:" + str(i), "title": s["title"], "assetIDs": s.get("assetIDs", [])} for i, s in enumerate(g.get("sections", [])) if s.get("history"))
    for look in ctx.data.get("mouthCoverage", {}).get("looks", []):
        if look.get("project") == ctx.project and (look.get("history") or look.get("planStatus") == "History only"):
            definitions.append({"id": "archive:" + look["id"], "title": look["title"], "assetIDs": [r["assetID"] for r in ctx.data["mouthCoverage"].get("items", []) if r.get("lookID") == look["id"] and ctx.by_id.get(r.get("assetID"), {}).get("sha256") == r.get("sha256")]})
    claimed, groups = set(), []
    for source in definitions:
        group = ctx.group({**source, "assetIDs": [aid for aid in source["assetIDs"] if aid in available and aid not in claimed]})
        if group:
            groups.append(group); claimed.update(group["assetIDs"])
    return [section(f'Saved removal decisions and archive · {len(removals)}', removals, kind='disclosure',
                    description='These references are marked for removal but have not been archived. Their decisions, notes and original files are retained.'),
            section("Earlier reference collections", kind="collections", groups=groups),
            section("Archived pictures, clips and documents", [aid for aid in available if aid not in claimed], description="Open a reference to restore it. Reviews and original files are retained.")]


def comfy_workflow_families(ctx, config):
    """Linked recipe evidence is separate from the workspace's media galleries."""
    workflows = {w["id"]: w for w in ctx.data.get("productionWorkflows", [])}
    families = []
    for family in config.get("workflowFamilies", []):
        records = [workflows[wid] for wid in unique(family.get("workflowIDs", []))
                   if wid in workflows and workflows[wid].get("project") in {ctx.project, "shared"}]
        text = " ".join(str(family.get(key, "")) for key in (
            "title", "inputLabel", "operationLabel", "outputLabel", "status", "description"))
        text += " " + " ".join(str(w.get(key, "")) for w in records for key in (
            "title", "status", "summary", "nextAction"))
        reference_ids = [link.get("assetID") for link in family.get("links", [])]
        reference_ids.extend(aid for w in records for key in ("sourceAssetIDs", "outputAssetIDs", "documentAssetIDs") for aid in w.get(key, []))
        if ctx.query and ctx.query not in text.casefold() and not any(
                aid in ctx.by_id and ctx.visible(ctx.by_id[aid]) and ctx.matches(ctx.by_id[aid]) for aid in reference_ids):
            continue
        text += " " + ctx.query
        linked_records = []
        for record in records:
            linked_records.append({**{k: record.get(k, "") for k in ("id", "title", "status", "summary")},
                **{key: ctx.ids(record.get(key, []), text) for key in (
                    "sourceAssetIDs", "outputAssetIDs", "documentAssetIDs")}})
        links = [dict(link) for link in family.get("links", [])
                 if ctx.ids([link.get("assetID")], text)]
        families.append({**{key: family.get(key, "") for key in (
            "id", "title", "inputLabel", "operationLabel", "outputLabel", "status", "description")},
            "workflows": linked_records, "links": links})
    return families


def workflow_diagram_html(family):
    """Plain-text diagram with escaped labels and no external media dependencies."""
    stages = [("Input", family.get("inputLabel", "")), ("Operation", family.get("operationLabel", "")),
              ("Result", family.get("outputLabel", ""))]
    boxes = ['<div class="cfa-workflow-step"><span>' + label + '</span><strong>' + escape(str(text or "")) + '</strong></div>'
             for label, text in stages]
    return '<div class="cfa-workflow-diagram" role="group" aria-label="Input to operation to result">' + (
        '<span class="cfa-workflow-arrow" aria-hidden="true">→</span>'.join(boxes)) + '</div>'


def comfy_model(ctx, album_id):
    """Only recorded workspace roles define outputs; category/provider are not proof."""
    config = ctx.data.get("browseLayout", {}).get("projects", {}).get(ctx.project, {}).get("comfyWorkspace", {})

    def workspace_ids(key):
        return [aid for aid in ctx.ids(config.get(key, []))
                if not album_id or ctx.by_id[aid].get("album") == album_id]

    targets = []
    for aid in unique(config.get("targetAlbumIDs", [])):
        album = ctx.albums.get(aid, {})
        if album.get("project") != ctx.project or album_id and aid != album_id:
            continue
        if group := ctx.group(album):
            group.update(directSingle=True, unit="targets")
            targets.append(group)
    output_ids = workspace_ids("outputAssetIDs")
    return [
        section("Comfy outputs", output_ids,
            description="Experiments and candidate results. Each keeps its recorded review; failed preservation tests remain available for comparison.",
            emptyMessage=("No Comfy outputs match this view." if config.get("outputAssetIDs")
                          else "No Comfy outputs have been catalogued for this project.")),
        section("Likeness targets", kind="collections", groups=targets,
            description="Appearance inputs for swaps. Open a target or a collection of alternate views."),
        section("Workflow recipes", kind="workflow_families", families=comfy_workflow_families(ctx, config)
                if not album_id else []),
        section("Source clips & control guides", workspace_ids("inputAssetIDs"), kind="disclosure",
            description="Source footage and technical guides used by the recorded experiments. These are inputs, not finished Comfy results."),
        section("Local finishing", workspace_ids("finishingAssetIDs"), kind="disclosure",
            description="This soundtrack preview was created locally with the original picture preserved. Its related Cloud graph is saved but has not executed; this is not lip-sync."),
    ]


def build_design_model(data, project, view, reviews=None, query="", album_id=""):
    """Build presentation-only groups using effective reviews and archive state."""
    mode = VIEWS.get(view, view)
    if mode not in set(VIEWS.values()):
        return None
    ctx = Context(data, project, reviews, query, archive=mode == "archive")
    album_id = "" if album_id == "all" else album_id
    if mode == "working":
        parts = working_model(ctx, album_id)
    elif mode == "outfits":
        parts = outfit_model(ctx, album_id)
    elif mode == "details":
        parts = detail_model(ctx, album_id)
    elif mode == "cast":
        parts = cast_model(ctx, album_id)
    elif mode == "archive":
        parts = archive_model(ctx)
    else:
        parts = comfy_model(ctx, album_id)
    return {"view": mode, "project": project, "sections": parts, "assets": ctx.by_id, "reviews": ctx.reviews,
            "title": "Comfy results & swap targets" if mode == "comfy" else view}


def render_design_view(data, project, view, library_dir: Path, render_grid, open_reference,
                       *, reviews=None, query="", album_id="", navigate=None) -> bool:
    """Render native Streamlit controls; callbacks own review editing and leaf cards."""
    model = build_design_model(data, project, view, reviews, query, album_id)
    if model is None:
        return False
    import streamlit as st

    def toggle(key):
        st.session_state[key] = not st.session_state.get(key, False)

    def preview(a, context, label=None):
        path = media_path(library_dir, a.get("thumb") or a.get("src"))
        if path:
            st.image(str(path), width="stretch")
        else:
            st.caption("Preview is not included in this snapshot.")
        r = model["reviews"].get(a["id"], {})
        rating = r.get("likenessRating")
        st.caption("Character / component: " + (f"{rating}/5 {'★' * rating}" if type(rating) is int and 1 <= rating <= 5 else "unrated"))
        if r.get("status"):
            st.caption({"keep": "Keep", "needs_fixes": "Needs fixes", "remove": "Marked for removal"}.get(r["status"], r["status"]))
        st.button(label or "Open & review", key=context + ":open:" + a["id"], on_click=open_reference, args=(a,), width="stretch")

    def assets(ids, context, single_preview=False):
        rows = [(model["assets"][aid], None) for aid in unique(ids) if aid in model["assets"]]
        visuals = [(a, al) for a, al in rows if a.get("kind") not in {"document", "pdf"}]
        if single_preview:
            for index, (a, _) in enumerate(visuals):
                preview(a, context + ":" + str(index))
        elif visuals:
            render_grid(visuals, context)
        documents = [a for a, _ in rows if a.get("kind") in {"document", "pdf"}]
        if documents:
            st.markdown(f'**Documents · {len(documents)}**')
        for a in documents:
            st.button(a.get("title", a["id"]), key=context + ":doc:" + a["id"], on_click=open_reference, args=(a,))

    def collections(groups, context):
        for start in range(0, len(groups), 3):
            for col, g in zip(st.columns(3), groups[start:start + 3]):
                with col, st.container(border=True):
                    cover = model["assets"].get(g.get("coverID"))
                    if cover and (path := media_path(library_dir, cover.get("thumb") or cover.get("src"))):
                        st.image(str(path), width="stretch")
                    st.markdown("**" + g["title"] + "**")
                    count = len(model_asset_ids(g))
                    unit = g.get("unit", "references")
                    st.caption(f"{count} {unit[:-1] if count == 1 and unit.endswith('s') else unit}")
                    if facts := g.get("browseFacts"):
                        labels = [label for key, label in (("roles", "Role choice recorded"), ("planned", "Planned for storyboard")) if facts.get(key)]
                        if facts.get("linked") or facts.get("sequences"):
                            labels.append("Storyboard-linked")
                        if labels:
                            st.caption(" · ".join(labels))
                        if facts["sources"]:
                            st.caption("From " + facts["sources"][0]["title"] +
                                       (f" · +{len(facts['sources']) - 1} sources" if len(facts["sources"]) > 1 else ""))
                    key = context + ":expanded:" + g["id"]
                    if g.get("directSingle") and count == 1 and cover:
                        st.button("Open target", key=key + ":open", on_click=open_reference, args=(cover,), width="stretch")
                    else:
                        st.button("Hide references" if st.session_state.get(key) else "Show references", key=key + ":toggle", on_click=toggle, args=(key,), width="stretch")
        for g in groups:
            key = context + ":expanded:" + g["id"]
            if g.get("directSingle") and len(model_asset_ids(g)) == 1 or not st.session_state.get(key):
                continue
            with st.container(border=True):
                st.subheader(g["title"])
                if g.get("description"):
                    st.caption(g["description"])
                cover = model["assets"].get(g.get("coverID"))
                if cover:
                    st.button("Review character / collection cover", key=key + ":cover", on_click=open_reference, args=(cover,))
                if facts := g.get("browseFacts"):
                    with st.expander("Origin & story connections", expanded=False):
                        st.caption("Source collections / runs")
                        for source in facts["sources"]:
                            st.write(source["title"])
                        if not facts["sources"]:
                            st.caption("No source collection is recorded.")
                        if facts["choices"]:
                            st.caption("Recorded character choices")
                            for choice in facts["choices"]:
                                st.write(str(choice.get("characterRole") or "Selected character") + " · " +
                                         ("this version selected by you" if choice.get("manualCastChoice") else
                                          "role assigned by Ziggy" if choice.get("roleDecision") == "user_assigned" else "visible likeness selected by Ziggy"))
                            st.caption("These choices assign a role or reference scope; each image keeps its own review.")
                        if facts["planned"]:
                            st.caption("Planned storyboard use" + (" · see linked shots below" if facts["linked"] or facts["sequences"] else " · no panel linked yet"))
                            for shot in facts["planned"]:
                                st.write(shot.get("title", shot.get("id", "Planned scene")))
                        if facts["linked"] or facts["sequences"]:
                            st.caption("Linked storyboard material · placement and acceptance stay with each shot")
                            for shot in [*facts["linked"], *facts["sequences"]]:
                                st.write(shot.get("title", shot.get("id", "Linked story material")))
                        if facts.get("unresolved"):
                            st.warning('Some saved storyboard links no longer resolve. They are retained for review and excluded from linked counts.')
                            for link in facts['unresolved']:
                                st.caption(link['storyID']+' · '+link['shotID']+' · '+link['assetID'])
                        if navigate and (facts["planned"] or facts["linked"] or facts["sequences"]):
                            st.button("Browse storyboards", key=key + ":storyboard", on_click=navigate, args=("Storyboard",))
                for i, child in enumerate(g.get("sections", [])):
                    render(child, key + ":" + str(i))
                if g.get("notes"):
                    with st.expander("Reference notes", expanded=False):
                        for note in g["notes"]:
                            st.write(note)

    def render(s, context, heading=True, single_preview=False):
        kind, ids = s.get("kind", "gallery"), s.get("assetIDs", [])
        if not (model_asset_ids(s) or s.get("emptyMessage") or s.get("families")):
            return
        if kind == "disclosure":
            with st.expander(s["title"], expanded=s.get("expanded", False)):
                if s.get("description"):
                    st.caption(s["description"])
                assets(ids, context)
                for i, child in enumerate(s.get("sections", [])):
                    render(child, context + ":" + str(i))
                if not ids and not any(model_asset_ids(child) for child in s.get("sections", [])) and s.get("emptyMessage"):
                    st.caption(s["emptyMessage"])
            return
        if heading:
            st.subheader(s["title"])
        if s.get("description"):
            st.caption(s["description"])
        if kind == "workflow_families":
            st.markdown('''<style>
                .cfa-workflow-diagram {display:flex;align-items:stretch;gap:5px;margin:10px 0 14px;}
                .cfa-workflow-step {flex:1;min-width:0;padding:9px 7px;border:1px solid #60718a;border-radius:8px;background:#182334;color:#f5f7fb;}
                .cfa-workflow-step span {display:block;font-size:11px;color:#d4b582;margin-bottom:5px;}
                .cfa-workflow-step strong {display:block;font-size:13px;line-height:1.4;overflow-wrap:anywhere;}
                .cfa-workflow-arrow {align-self:center;color:#d4b582;font-size:18px;}
                @media(max-width:520px) {.cfa-workflow-diagram {flex-direction:column;}.cfa-workflow-arrow {transform:rotate(90deg);}}
                </style>''', unsafe_allow_html=True)

            def link_button(aid, label, key):
                asset = model["assets"].get(aid)
                if asset:
                    st.button(label or asset.get("title", aid), key=key, on_click=open_reference, args=(asset,), width="stretch")

            for start in range(0, len(s["families"]), 2):
                for column, family in zip(st.columns(2), s["families"][start:start + 2]):
                    with column, st.container(border=True):
                        st.markdown("**" + family["title"] + "**")
                        st.caption(family["status"])
                        st.markdown(workflow_diagram_html(family), unsafe_allow_html=True)
                        if family.get("description"):
                            st.caption(family["description"])
                        family_key = context + ":family:" + family["id"]
                        with st.expander("Ingredients and records", expanded=False):
                            for i, link in enumerate(family["links"]):
                                link_button(link["assetID"], link.get("label"), family_key + ":link:" + str(i))
                            for workflow in family["workflows"]:
                                st.markdown("**" + workflow["title"] + "**")
                                st.caption(workflow["status"])
                                if workflow["summary"]:
                                    st.write(workflow["summary"])
                                for label, field in (("Parent inputs", "sourceAssetIDs"), ("Recorded outputs", "outputAssetIDs"), ("Records and graphs", "documentAssetIDs")):
                                    if workflow[field]:
                                        suffix = (' · '+str(navigation_reference_count(list(model['assets'].values()), workflow[field], documents=True))+' documents') if field == 'documentAssetIDs' else ''
                                        st.caption(label+suffix)
                                        for aid in workflow[field]:
                                            link_button(aid, None, family_key + ":" + workflow["id"] + ":" + field + ":" + aid)
        elif kind == "columns":
            for col, child in zip(st.columns(len(s["sections"])), s["sections"]):
                with col:
                    render(child, context + ":" + child["title"], single_preview=True)
        elif kind == "mouth_slots":
            for start in range(0, len(s["slots"]), 3):
                for col, slot in zip(st.columns(3), s["slots"][start:start + 3]):
                    with col, st.container(border=True):
                        number = str(slot["number"]).zfill(2) if type(slot["number"]) is int else "Reference"
                        st.markdown("**" + number + " · " + slot["label"] + "**")
                        takes = slot["takes"]
                        if takes:
                            first = model["assets"][takes[0]["assetID"]]
                            if path := media_path(library_dir, first.get("thumb") or first.get("src")):
                                st.image(str(path), width="stretch")
                            repairs = any(model["reviews"].get(r["assetID"], {}).get("status") == "needs_fixes" for r in takes)
                            st.caption(f"{len(takes)} takes · " + ("Needs fixes" if repairs else "Read each image's scoped review; presence is not acceptance."))
                        else:
                            st.caption("Missing · no received candidate")
                        for take in takes:
                            a = model["assets"][take["assetID"]]
                            st.button(a["id"] + " · " + str(take.get("revision", "unknown")),
                                      key=context + ":take:" + a["id"], on_click=open_reference, args=(a,), width="stretch")
                            st.caption(f"Yaw: {take.get('yaw', 'unknown')} · Pitch: {take.get('pitch', 'unknown')}")
                            if take.get("labelProvenance"):
                                st.caption(take["labelProvenance"])
                            for observation in [o for o in slot["observations"] if o.get("assetID") == a["id"]]:
                                with st.expander("Attributed pixel observation", expanded=False):
                                    st.write(observation.get("observation", ""))
                                    st.caption(" · ".join(str(v) for v in (observation.get("reviewer", {}).get("actor"),
                                        observation.get("documentAtUTC"), observation.get("surface"), observation.get("source", {}).get("sha256")) if v))
                        if slot.get("note"):
                            st.caption(slot["note"])
                        if len(takes) > 1:
                            st.caption("Multiple takes share a provider label. Different bytes do not establish different articulation.")
        elif kind == "collections":
            collections(s.get("groups", []), context)
        elif kind == "reference_board":
            for row in s.get("rows", []):
                left, right = st.columns([1, 3])
                with left:
                    preview(model["assets"][row["assetID"]], context + ":" + row["id"])
                with right:
                    st.markdown("**" + row.get("label", row["id"]) + (" · Provisional" if row["id"] == "body-build-candidate" else "") + "**")
                    st.write(row.get("scope", ""))
                    with st.expander("Source, limits and recorded choices", expanded=False):
                        st.caption(model["assets"][row["assetID"]].get("filename", row["assetID"]))
                        st.caption(str(row.get("asset", {}).get("bytes", "Unknown")) + " bytes · " + row.get("asset", {}).get("version", ""))
                        for item in row.get("provenance", []):
                            st.write(item.get("summary", ""))
                        for item in row.get("limitations", []):
                            st.write(item)
                        if row.get("unresolved", {}).get("summary"):
                            st.write(row["unresolved"]["summary"])
        else:
            assets(ids, context, single_preview)
            for i, child in enumerate(s.get("sections", [])):
                render(child, context + ":" + str(i))
        if not model_asset_ids(s) and s.get("emptyMessage"):
            st.caption(s["emptyMessage"])

    context = "design:" + project + ":" + model["view"] + ":" + (album_id or "root")
    if model["view"] == "comfy":
        st.caption("Character, mouth and grill references live in Working references.")
        if navigate:
            st.button("Open Working references", key=context + ":working", on_click=navigate, args=("Working references",))
    if model["view"] == "cast" and not album_id:
        groups = model["sections"][0]["groups"]
        sources = {}
        for group in groups:
            for source in group.get("browseFacts", {}).get("sources", []):
                entry = sources.setdefault(source["id"], {**source, "count": 0})
                entry["count"] += 1
        source_key, filter_key = context + ":source", context + ":connection"
        if st.session_state.get(source_key, "all") not in {"all", *sources}:
            st.session_state[source_key] = "all"
        source = st.selectbox("Source collection / run", ["all", *sources], key=source_key,
                              format_func=lambda value: "All sources" if value == "all" else f"{sources[value]['title']} · {sources[value]['count']} characters")
        selected = st.session_state.get(filter_key, "all")

        def select_connection(value):
            st.session_state[filter_key] = value

        def clear_cast_filters():
            st.session_state[source_key] = "all"
            st.session_state[filter_key] = "all"

        filters = [("all", "All characters"), ("roles", "Recorded role choices"),
                   ("planned", "Planned for storyboard"), ("linked", "Storyboard-linked")]
        for col, (value, label) in zip(st.columns(4), filters):
            with col:
                st.button(f"{label} · {len(cast_browse_groups(groups, source, value))}", key=context + ":filter:" + value,
                          type="primary" if selected == value else "secondary", on_click=select_connection, args=(value,), width="stretch")
        visible = cast_browse_groups(groups, source, selected)
        filtered = source != "all" or selected != "all"
        if filtered:
            st.button("Clear filters", key=context + ":clear", on_click=clear_cast_filters)
        st.caption(f"{len(visible)} characters shown. Storyboard plans and linked drafts are shown separately.")
        if not visible:
            st.info("No characters match these filters. Clear filters or change the search.")
        model["sections"][0] = {**model["sections"][0], "groups": visible}
        if filtered:
            model["sections"] = model["sections"][:1]
    buckets = [s for s in model["sections"] if s["kind"] == "outfit_bucket"]
    if buckets:
        def select_bucket(value):
            st.session_state[context + ":bucket"] = value

        selected = st.session_state.get(context + ":bucket", "all")
        for col, (value, label) in zip(st.columns(4), [("all", "All outfits"), *[(s["bucketID"], s["title"]) for s in buckets]]):
            with col:
                st.button(label, key=context + ":tag:" + value, type="primary" if selected == value else "secondary",
                          on_click=select_bucket, args=(value,), width="stretch")
        all_views = st.radio("Outfit view", ["One per outfit", "Show all views"], horizontal=True, key=context + ":layout") == "Show all views"
        for bucket in buckets:
            if selected not in {"all", bucket["bucketID"]} or not bucket["groups"]:
                continue
            with st.expander(f"{bucket['title']} · {len(bucket['groups'])} outfits", expanded=True):
                if all_views:
                    for g in bucket["groups"]:
                        st.subheader(g["title"]); assets(g["assetIDs"], context + ":all:" + g["id"])
                else:
                    collections(bucket["groups"], context + ":" + bucket["bucketID"])
    else:
        for i, item in enumerate(model["sections"]):
            render(item, context + ":" + str(i))
    if model["view"] != "comfy" and not any(model_asset_ids(s) for s in model["sections"]):
        st.info("No references match this view.")
    return True

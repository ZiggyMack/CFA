"""Small, offline helpers shared by the Creative Studio and its checks."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote, urlsplit
import zipfile

FAVORITES_FORMAT = "cfa-visual-favorites-v1"
REVIEW_FORMAT = "cfa-visual-review-v1"
HANDOFF_FORMAT = "cfa-shot-handoff-v1"
EXPORT_FORMAT = "cfa-visual-export-v1"
REVIEW_STATUSES = {"keep", "needs_fixes", "remove"}
# Opaque, hash-bound review provenance survives the compact editor. These fields
# do not drive execution or confer approval; unsupported controls remain in the index.
REVIEW_METADATA_FIELDS = {
    "updatedAt", "origin", "source", "sourceIntakeID", "scopeNote", "sourceReviewPath",
    "collectionState", "importEvidence", "archiveReason", "removalState", "handoffPolicy",
    "creativeReview", "supersededBy", "displayTitle", "humanRatingConfirmation", "history",
    "reason", "reasonSource", "scopedPropCorrection", "temporalVariant", "lookSelection",
    "componentSelection", "directUserClarification", "creativeLane", "validationEvidence",
}
DESTINATIONS = ("undecided", "Gemini", "Flow", "Grok", "ComfyUI")
MISSION_PROVIDERS = ("Grok", "Gemini", "Flow", "Panhandler Nova")
MISSION_STATUSES = {"ready", "needs_input", "planned", "in_progress", "done"}
VISUAL_KINDS = {"image", "video", "gif"}
STORYBOARD_STAGES = {"preliminary": "Preliminary", "detailed_design": "Detailed design",
                     "verification": "Verification", "production": "Production"}


def media_path(library_dir: Path, value: str | None) -> Path | None:
    """Resolve only packaged files; never follow local or remote source paths."""
    if not value or not isinstance(value, str):
        return None
    decoded = unquote(value)
    parsed = urlsplit(decoded)
    if parsed.scheme or parsed.netloc or "\\" in decoded:
        return None
    root = library_dir.resolve()
    target = (root / decoded).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return None
    return target


def ordered_assets(
    assets: list[dict[str, Any]], albums: list[dict[str, Any]],
    project: str, category: str = "all", album_id: str = "all", query: str = "", include_archived: bool = False,
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    """Follow supplied album and member order, showing each picture once."""
    by_id = {a["id"]: a for a in assets if a.get("project") == project and a.get("kind") in VISUAL_KINDS
             and (include_archived or not a.get("archived"))}
    eligible_albums = [a for a in albums if a.get("project") == project
                       and (category == "all" or a.get("category") == category)
                       and (album_id == "all" or a.get("id") == album_id)]
    result, seen = [], set()
    terms = query.casefold().split()

    def append(asset: dict[str, Any], album: dict[str, Any] | None) -> None:
        if asset["id"] in seen:
            return
        haystack = " ".join(str(asset.get(k, "")) for k in ("title", "filename", "note", "beat", "lyric", "tags"))
        if album:
            haystack += " " + str(album.get("title", ""))
        if all(term in haystack.casefold() for term in terms):
            result.append((asset, album))
            seen.add(asset["id"])

    for album in eligible_albums:
        for asset_id in album.get("assetIDs", []):
            if asset_id in by_id:
                append(by_id[asset_id], album)
    if album_id == "all":
        for asset in by_id.values():
            if category == "all" or asset.get("category") == category:
                append(asset, None)
    return result


def sort_video_assets(results: list[tuple[dict, dict | None]], order: str) -> list[tuple[dict, dict | None]]:
    """Keep editorial order by default; explicit sorts can cross scene groups."""
    if order == "Recommended":
        return list(results)
    if order in ("Alphabetical", "Alphabetical A–Z"):
        return sorted(results, key=lambda row: str(row[0].get("title", row[0].get("filename", ""))).casefold())
    if order not in ("Longest", "Longest first", "Shortest"):
        raise ValueError("Unknown video order.")
    def key(row):
        duration = row[0].get("duration")
        known = isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration >= 0
        title = str(row[0].get("title", row[0].get("filename", ""))).casefold()
        return (not known, (-duration if order in ("Longest", "Longest first") else duration) if known else 0, title)
    return sorted(results, key=key)


def layout_video_assets(results: list[tuple[dict, dict | None]], layout: str, order: str) -> list[tuple[dict, dict | None]]:
    if layout == "All clips":
        return [(asset, None) for asset, _ in sort_video_assets(results, order)]
    if layout != "Grouped":
        raise ValueError("Unknown video layout.")
    groups: dict[str, list[tuple[dict, dict | None]]] = {}
    for row in results:
        groups.setdefault(row[1].get("id", "") if row[1] else "", []).append(row)
    # Retain the supplied category order, with turnaround references at the end.
    order_ids = sorted(groups, key=lambda key: "turnaround" in (key + " " + str((groups[key][0][1] or {}).get("title", ""))).casefold())
    return [row for key in order_ids for row in sort_video_assets(groups[key], order)]


def collaborator_sections(assets: list[dict]) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {name: [] for name in ("Gemini", "Flow", "Grok", "Shared roles")}
    for asset in assets:
        if asset.get("kind") not in ("document", "pdf"):
            continue
        filename = str(asset.get("filename", "")).casefold()
        context = " ".join(str(asset.get(key, "")) for key in ("id", "album", "title", "filename")).casefold()
        if "historical" in context:
            continue
        if filename == "provider_roles.txt" or "panhandler_return" in filename:
            provider = "Shared roles"
        elif "gemini" in context:
            provider = "Gemini"
        elif re.search(r"(?<![a-z])flow(?![a-z])", context):
            provider = "Flow"
        elif "grok" in context and any(word in context for word in ("instructions", "care package", "grok_20", "revision_queue")):
            provider = "Grok"
        else:
            continue
        sections[provider].append(asset)
    # Put each provider's front-door instructions first, retaining the rest's saved order.
    for provider in sections:
        sections[provider].sort(key=lambda asset: -1 if asset.get("filename") == "grok_design_instructions.txt"
                                else 0 if "start_here" in asset.get("filename", "").casefold() else 1)
    return sections


def favorite_payload(assets: list[dict[str, Any]], favorites: set[str], notes: dict[str, str]) -> dict[str, Any]:
    items = [{"id": a["id"], "project": a.get("project"), "filename": a.get("filename"),
              "path": a.get("repoPath", a.get("src")), "sha256": a.get("sha256") or None,
              "role": a.get("category")}
             for a in assets if a["id"] in favorites]
    valid_ids = {a["id"] for a in assets}
    hashes = {a["id"]: a.get("sha256") for a in assets}
    return {"format": FAVORITES_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "user review shortlist; not automatic final approval", "items": items,
            "notes": {key: value for key, value in notes.items() if key in valid_ids and value.strip()},
            "note_refs": {key: hashes[key] for key, value in notes.items() if key in valid_ids and value.strip()}}


def read_favorites(payload: Any, assets: list[dict[str, Any]]) -> tuple[set[str], dict[str, str], int]:
    """Import known IDs only, and reject mismatched source hashes."""
    if not isinstance(payload, dict) or payload.get("format") != FAVORITES_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a Creative Studio favorites export (cfa-visual-favorites-v1).")
    by_id = {a["id"]: a for a in assets}
    accepted, skipped = set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = by_id.get(item["id"])
        if asset and (not item.get("sha256") or item["sha256"] == asset.get("sha256")):
            accepted.add(item["id"])
        else:
            skipped += 1
    raw_notes = payload.get("notes", {})
    note_refs = payload.get("note_refs", {})
    if not isinstance(note_refs, dict):
        note_refs = {}
    notes = {key: value[:20000] for key, value in raw_notes.items()
             if key in by_id and isinstance(value, str)
             and (not note_refs.get(key) or note_refs[key] == by_id[key].get("sha256"))} if isinstance(raw_notes, dict) else {}
    return accepted, notes, skipped


def normalize_plan(value: Any) -> dict[str, Any] | None:
    """Plans are drafts only; never import claims that a provider has run them."""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("A shot plan must be an object or null.")
    destinations = value.get("destinations", ["undecided"])
    if not isinstance(destinations, list) or any(d not in DESTINATIONS for d in destinations):
        raise ValueError("Choose Gemini, Flow, Grok, ComfyUI, or undecided for a shot plan.")
    destinations = [d for d in DESTINATIONS if d in destinations and d != "undecided"] or ["undecided"]
    idea, prompt = value.get("idea", ""), value.get("prompt", "")
    if not isinstance(idea, str) or not isinstance(prompt, str):
        raise ValueError("Shot ideas and prompts must be text.")
    status = "requested_bounded_test" if value.get("status") == "requested_bounded_test" else "planned"
    return {"status": status, "destinations": destinations, "idea": idea[:20000], "prompt": prompt[:40000]}


def normalize_decision(value: Any, *, partial: bool = False, allow_catalog_variant: bool = True) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("A review decision must be an object.")
    result: dict[str, Any] = {} if partial else {"status": None, "note": "", "shotPlan": None}
    if "status" in value:
        if value["status"] is not None and value["status"] not in REVIEW_STATUSES:
            raise ValueError("A review status must be keep, needs_fixes, remove, or null.")
        result["status"] = value["status"]
    if "note" in value:
        if not isinstance(value["note"], str):
            raise ValueError("Review notes must be text.")
        result["note"] = value["note"][:20000]
    if "shotPlan" in value:
        result["shotPlan"] = normalize_plan(value["shotPlan"])
    if "variant" in value:
        if value["variant"] not in ("prime", "multiverse"):
            raise ValueError("A reference lane must be prime or multiverse.")
        catalog_origin = value.get("variantSource") == "catalog" or value.get("origin") == "catalog"
        if allow_catalog_variant or not catalog_origin:
            result["variant"] = value["variant"]
            result["variantSource"] = "catalog" if catalog_origin else "user"
    if "workingReference" in value:
        ref = value["workingReference"]
        if ref is not None and (not isinstance(ref, dict) or ref.get("status") not in ("requested", "approved")
                                or ref.get("scope") not in ("complete_look", "identity", "outfit", "scene", "detail")):
            raise ValueError("A working reference needs a valid status and scope.")
        result["workingReference"] = json.loads(json.dumps(ref, allow_nan=False)) if ref else None
    if "storyboardStage" in value:
        if value["storyboardStage"] is not None and value["storyboardStage"] not in STORYBOARD_STAGES:
            raise ValueError("Choose a valid storyboard stage.")
        result["storyboardStage"] = value["storyboardStage"]
    for key in ("likenessRating", "sceneQualityRating"):
        if key in value:
            rating = value[key]
            if rating is not None and (type(rating) is not int or not 1 <= rating <= 5):
                raise ValueError("A review rating must be 1–5 or null.")
            result[key] = rating
    if "workingReferenceScope" in value:
        scope = value["workingReferenceScope"]
        if scope is not None and scope not in ("complete_look", "identity", "outfit", "scene", "detail"):
            raise ValueError("Choose a valid working-reference scope.")
        result["workingReferenceScope"] = scope
    for key in REVIEW_METADATA_FIELDS & value.keys():
        result[key] = json.loads(json.dumps(value[key], allow_nan=False))
    return result


def _hash_matches(item: dict, asset: dict) -> bool:
    return (item.get("sha256") or None) == (asset.get("sha256") or None)


def effective_reviews(assets: list[dict], seeds: Any, overrides: dict[str, dict]) -> dict[str, dict]:
    """Overlay session choices on supplied seeds; explicit null survives reruns."""
    by_id = {a["id"]: a for a in assets}
    if isinstance(seeds, dict):
        seeds = seeds.get("items", [])
    result = {}
    for asset in assets:
        source_fields = {key: asset[key] for key in ("workingReference", "variant") if key in asset}
        if source_fields:
            if "variant" in source_fields:
                source_fields["variantSource"] = "catalog"
            result[asset["id"]] = normalize_decision(source_fields)
    for item in seeds if isinstance(seeds, list) else []:
        if not isinstance(item, dict) or item.get("id") not in by_id:
            continue
        if not _hash_matches(item, by_id[item["id"]]):
            continue
        try:
            baseline = result.get(item["id"], {})
            result[item["id"]] = {**baseline, **normalize_decision(item, partial=True)}
            if "variant" in result[item["id"]]:
                result[item["id"]]["variantSource"] = "catalog"
        except (ValueError, TypeError):
            continue
    for asset_id, decision in overrides.items():
        if asset_id not in by_id:
            continue
        # Overrides are session data or already hash-validated imports.
        merged = dict(result.get(asset_id, {"status": None, "note": "", "shotPlan": None}))
        merged.update(normalize_decision(decision, partial=True))
        result[asset_id] = merged
    return result


def reference_record(asset: dict) -> dict:
    return {"id": asset["id"], "sha256": asset.get("sha256") or None,
            "project": asset.get("project"), "filename": asset.get("filename"),
            "path": asset.get("repoPath", asset.get("src")), "role": asset.get("category")}


def review_payload(assets: list[dict], reviews: dict[str, dict], favorites: set[str], basket: set[str] | None = None) -> dict:
    payload = {"format": REVIEW_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "session review and draft shot plans; no files deleted and no generation submitted",
            "items": [{**reference_record(a), **normalize_decision(reviews[a["id"]])}
                      for a in assets if a["id"] in reviews],
            "favorites": [reference_record(a) for a in assets if a["id"] in favorites]}
    if basket is not None:
        payload["exportBasket"] = [reference_record(a) for a in assets if a["id"] in basket]
    return payload


def read_review(payload: Any, assets: list[dict]) -> tuple[dict[str, dict], set[str], int]:
    """Read both formats without changing the catalog, sources, or approvals."""
    if isinstance(payload, dict) and payload.get("format") == FAVORITES_FORMAT:
        favorites, notes, skipped = read_favorites(payload, assets)
        return {key: {"note": value} for key, value in notes.items()}, favorites, skipped
    if not isinstance(payload, dict) or payload.get("format") != REVIEW_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a CFA review or favorites JSON export.")
    raw_favorites = payload.get("favorites", [])
    if not isinstance(raw_favorites, list):
        raise ValueError("The favorites field must be a list of references.")
    by_id = {a["id"]: a for a in assets}
    reviews, favorites, skipped = {}, set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = by_id.get(item["id"])
        if not asset or not _hash_matches(item, asset):
            skipped += 1
            continue
        try:
            reviews[item["id"]] = normalize_decision(item, partial=True, allow_catalog_variant=False)
        except (ValueError, TypeError):
            skipped += 1
    for item in raw_favorites:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = by_id.get(item["id"])
        if asset and _hash_matches(item, asset):
            favorites.add(item["id"])
        else:
            skipped += 1
    return reviews, favorites, skipped


def export_allowed(asset: dict, reviews: dict[str, dict], intent: str = "prime") -> bool:
    if intent not in ("prime", "multiverse_ingredients"):
        raise ValueError("Unknown export intent.")
    decision = reviews.get(asset["id"], {})
    variant = decision.get("variant", asset.get("variant", "prime"))
    return not asset.get("archived") and decision.get("status") != "remove" and (variant != "multiverse" or intent == "multiverse_ingredients")


def handoff_payload(assets: list[dict], reviews: dict[str, dict], project: str, destination: str, intent: str = "prime") -> dict:
    if destination not in (*DESTINATIONS, "all"):
        raise ValueError("Unknown shot-plan destination.")
    items = []
    for asset in assets:
        if asset.get("project") != project or not export_allowed(asset, reviews, intent):
            continue
        decision = reviews.get(asset["id"], {})
        plan = normalize_plan(decision.get("shotPlan"))
        if not plan or (destination != "all" and destination not in plan["destinations"]):
            continue
        items.append({**reference_record(asset), "title": asset.get("title", asset.get("filename")),
                      "reviewStatus": decision.get("status"),
                      "variant": decision.get("variant", asset.get("variant", "prime")),
                      "storyboardStage": storyboard_stage(asset, reviews),
                      "note": decision.get("note", ""), "shotPlan": plan})
    return {"format": HANDOFF_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "project": project, "destination": destination, "status": "planned; not sent or generated",
            "exportIntent": intent,
            "attachmentReminder": "This is a reference manifest, not an image ZIP. Attach the named source files and the current approved character/reference kit separately.",
            "items": items}


def handoff_text(payload: dict) -> str:
    lines = ["CFA shot handoff", f"Project: {payload['project']} | Destination: {payload['destination']}",
             "Status: planned; not sent or generated", payload["attachmentReminder"], ""]
    for item in payload["items"]:
        plan = item["shotPlan"]
        lines.extend([f"Reference: {item.get('filename')} | {item['id']}",
                      f"Source SHA256: {item.get('sha256') or 'unavailable'}", f"Path: {item.get('path')}",
                      f"Role: {item.get('role')} | Review: {item.get('reviewStatus') or 'unmarked'}",
                      f"Destinations: {', '.join(plan['destinations'])}", f"Review note: {item.get('note', '')}",
                      f"Shot idea: {plan['idea']}", f"Prompt draft: {plan['prompt']}", ""])
    return "\n".join(lines)


def mission_tasks(value: Any) -> list[dict]:
    """Read saved task cards as data. Local hrefs are intentionally not exposed."""
    if not isinstance(value, dict) or not isinstance(value.get("tasks"), list):
        return []
    tasks, seen = [], set()
    for item in value["tasks"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item["id"] in seen:
            continue
        if not isinstance(item.get("provider"), str) or not item["provider"].strip() or item.get("status") not in MISSION_STATUSES:
            continue
        if item.get("project") not in ("hon", "lisan", "shared"):
            continue
        if not all(isinstance(item.get(key), str) for key in ("title", "summary", "nextAction")):
            continue
        task = {key: item[key] for key in ("id", "provider", "project", "title", "status", "summary", "nextAction")}
        task["missing"] = [s for s in item.get("missing", []) if isinstance(s, str)] if isinstance(item.get("missing", []), list) else []
        for key in ("enablers", "deliverables", "previewAssetIDs", "variantAssetIDs"):
            task[key] = [s for s in item.get(key, []) if isinstance(s, str)] if isinstance(item.get(key), list) else []
        for key in ("priority", "statusLabel", "missingLabel", "laterReview"):
            if isinstance(item.get(key), str):
                task[key] = item[key]
        task["comparisonInHistory"] = item.get("comparisonInHistory") is True
        task["links"] = []
        for link in item.get("links", []) if isinstance(item.get("links", []), list) else []:
            if not isinstance(link, dict) or not isinstance(link.get("label", "Reference"), str):
                continue
            reference = {key: link[key] for key in ("assetID", "downloadPath") if isinstance(link.get(key), str)}
            if isinstance(link.get("assetIDs"), list):
                reference["assetIDs"] = [s for s in link["assetIDs"] if isinstance(s, str)]
            if isinstance(link.get("href"), str) and urlsplit(link["href"]).scheme == "https" and urlsplit(link["href"]).netloc:
                reference["href"] = link["href"]
            if isinstance(link.get("unavailableReason"), str):
                reference["unavailableReason"] = link["unavailableReason"]
            if reference:
                task["links"].append({"label": link.get("label", "Reference"), **reference})
        tasks.append(task)
        seen.add(item["id"])
    return tasks


def mission_review_data(base: dict, snapshot: dict) -> dict:
    """Union review identities without expanding ordinary browsing collections."""
    merged = dict(base)
    for key in ("assets", "reviewDecisions"):
        records = {item["id"]: item for item in base.get(key, [])}
        for item in snapshot.get(key, []):
            old = records.get(item["id"])
            if old and old.get("sha256") and item.get("sha256") != old["sha256"] and (
                key == "reviewDecisions" or old.get("kind") not in {"document", "pdf"} or item.get("kind") not in {"document", "pdf"}
            ):
                raise ValueError(f"Mission snapshot changes an existing reference hash: {item['id']}")
            records[item["id"]] = item
        merged[key] = list(records.values())
    return merged


def mission_visible(asset: dict | None, reviews: dict) -> bool:
    return bool(asset and not asset.get("archived") and reviews.get(asset["id"], {}).get("status") != "remove")


def mission_pending_requests(data: dict, reviews: dict, project: str) -> list[str]:
    by_id = {a["id"]: a for a in data.get("assets", [])}
    return list(dict.fromkeys(r["id"] for r in data.get("reviewRequests", [])
        if (a := by_id.get(r.get("id"))) and a.get("project") == project
        and r.get("type") == "missing_decision" and a.get("sha256") and r.get("sha256") == a["sha256"]
        and mission_visible(a, reviews) and reviews.get(a["id"], {}).get("status") not in REVIEW_STATUSES))


def mission_task_progress(task: dict, assets: list[dict], reviews: dict) -> dict:
    """Match index shortlist/gun decisions; a Fix/Remove is an answered review."""
    task = dict(task)
    by_id = {a["id"]: a for a in assets}
    if task["id"] in {"grok-lisan-mouth65-available", "grok-falcon-extension40-available"}:
        pending, answered, unavailable = [], [], []
        for aid in dict.fromkeys(task.get("previewAssetIDs", [])):
            a = by_id.get(aid)
            if not a or a.get("kind") != "image":
                unavailable.append(aid)
            elif reviews.get(aid, {}).get("status") in REVIEW_STATUSES:
                answered.append(aid)
            elif mission_visible(a, reviews):
                pending.append(aid)
            else:
                unavailable.append(aid)
        name = "Lisan mouth" if task["id"] == "grok-lisan-mouth65-available" else "Falcon extension"
        task.update(title=f"{name} shortlist · {len(pending)} awaiting review",
                    status="needs_input" if pending else "in_progress",
                    priority=task.get("priority") if pending or unavailable else "normal",
                    previewAssetIDs=pending, reviewedPreviewAssetIDs=answered,
                    summary=f"{len(answered)} of {len(pending) + len(answered) + len(unavailable)} shortlisted images have recorded decisions. {len(pending)} await your decision."
                            + (f" {len(unavailable)} references are unavailable and need a source check." if unavailable else "")
                            + " The full collection remains available; images outside this shortlist are not new review requests.",
                    nextAction="Review the remaining shortlist. Existing decisions stay saved; recorded defects remain separate correction work." if pending else
                               "The shortlist decisions are saved. The team can follow up on recorded defects; earlier decisions remain available below.")
    elif task["id"] == "favorites-prop-sweep":
        received = [a for a in assets if a.get("project") == "hon" and a.get("kind") == "image"
                    and a.get("sourceIntake") == "HON-GROK-RETURN-20261009" and a.get("propState") == "with_gun" and a.get("outfitAlbumID")]
        visible = [a for a in received if mission_visible(a, reviews)]
        pending = [a["id"] for a in visible if reviews.get(a["id"], {}).get("status") not in REVIEW_STATUSES]
        fixes = sum(reviews.get(a["id"], {}).get("status") == "needs_fixes" for a in visible)
        task.update(title=f"Review outfit gun variants · {len(pending)} unreviewed" if pending else "Outfit gun variant review",
                    status="needs_input" if pending else "in_progress" if fixes else "done",
                    summary=f"{len(received)} distinct gun variants across {len({a['outfitAlbumID'] for a in received})} outfits. {len(visible)} visible; {len(received)-len(visible)} hidden by removal or archive choices. {len(pending)} unreviewed; {fixes} need fixes. Gun approval is separate from character corrections.",
                    nextAction="Review the remaining variants for outfit and character preservation." if pending else "The recorded decisions are saved; character and other recorded fixes remain separate follow-up work.",
                    missing=[], previewAssetIDs=pending,
                    reviewedPreviewAssetIDs=[a["id"] for a in received if reviews.get(a["id"], {}).get("status") in REVIEW_STATUSES])
    return task


def production_workflows(value: Any) -> list[dict]:
    """Concrete workflow records only; Cloud links never launch a run."""
    if not isinstance(value, list):
        return []
    result, seen = [], set()
    for item in value:
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in
                                               ("id", "provider", "project", "title", "status", "summary", "nextAction")):
            continue
        if item["id"] in seen or item["provider"] != "ComfyUI":
            continue
        record = {key: item[key] for key in ("id", "provider", "project", "title", "status", "summary", "nextAction")}
        for key in ("sourceAssetIDs", "outputAssetIDs", "documentAssetIDs"):
            record[key] = [asset_id for asset_id in item.get(key, []) if isinstance(asset_id, str)] if isinstance(item.get(key, []), list) else []
        url = item.get("cloudURL")
        if isinstance(url, str):
            parsed = urlsplit(url)
            if parsed.scheme == "https" and parsed.netloc == "cloud.comfy.org":
                record["cloudURL"] = url
        result.append(record)
        seen.add(item["id"])
    return result


def basket_payload(assets: list[dict], basket: set[str], reviews: dict[str, dict] | None = None, intent: str = "prime") -> dict:
    return {"format": EXPORT_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "selected references; no approval implied",
            "exportIntent": intent,
            "referenceReminder": "This JSON is a selection list, not a media archive. The separate ZIP contains hosted review copies, not original master files.",
            "items": [reference_record(a) for a in assets if a["id"] in basket and export_allowed(a, reviews or {}, intent)]}


def read_basket(payload: Any, assets: list[dict]) -> tuple[set[str], int]:
    if not isinstance(payload, dict) or payload.get("format") != EXPORT_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a CFA export-basket JSON selection list.")
    by_id = {asset["id"]: asset for asset in assets}
    accepted, skipped = set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = by_id.get(item["id"])
        if asset and _hash_matches(item, asset):
            accepted.add(item["id"])
        else:
            skipped += 1
    return accepted, skipped


def basket_zip(library_dir: Path, assets: list[dict], basket: set[str], max_bytes: int = 100 * 1024 * 1024,
               reviews: dict[str, dict] | None = None, intent: str = "prime") -> bytes:
    """Package safe hosted copies in memory; deduplicate bytes and preserve provenance."""
    selected = [asset for asset in assets if asset["id"] in basket and export_allowed(asset, reviews or {}, intent)]
    if not selected:
        raise ValueError("Add at least one reference to the export basket.")
    paths, unique_paths = {}, set()
    for asset in selected:
        source = media_path(library_dir, asset.get("src"))
        if source is None:
            raise ValueError(f"The review copy for {asset.get('filename', asset['id'])} is unavailable. Export the JSON selection list instead.")
        paths[asset["id"]] = source
        unique_paths.add(source)
    if sum(path.stat().st_size for path in unique_paths) > max_bytes:
        raise ValueError("This basket exceeds the 100 MB review-copy limit. Export smaller groups or use the JSON selection list.")
    output = io.BytesIO()
    manifest = basket_payload(assets, basket, reviews, intent)
    manifest["archiveContents"] = "Hosted review copies, not original masters. Source sha256 identifies each original; reviewCopySha256 identifies the packaged copy."
    records, by_hash, total = [], {}, 0
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
        for asset in selected:
            source = paths[asset["id"]]
            content = source.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            if digest not in by_hash:
                total += len(content)
                if total > max_bytes:
                    raise ValueError("The selected review copies exceed the ZIP size limit.")
                name = re.sub(r"[^A-Za-z0-9._ -]", "_", Path(asset.get("filename", asset["id"])).stem)[:100] or "reference"
                member = f"review-copies/{digest[:16]}-{name}{source.suffix.lower()}"
                archive.writestr(member, content)
                by_hash[digest] = member
            records.append({**reference_record(asset), "archivePath": by_hash[digest], "reviewCopySha256": digest,
                            "reviewCopyBytes": len(content)})
        manifest["items"] = records
        manifest["uniqueReviewCopies"] = len(by_hash)
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        archive.writestr("README.txt", "CFA export basket\nThese are hosted review copies, not original master files.\nRead manifest.json for original source references and hashes.\nSelection does not imply production approval.\n")
    return output.getvalue()


def document_tree(assets: list[dict], query: str = "") -> dict[str, dict[str, list[dict]]]:
    parents = {name: {} for name in ("Design & outfit notes", "Story & music", "Collaborator briefs",
                                    "Production & workflows", "Tattoos & details", "History & helpers")}
    terms = query.casefold().split()
    for asset in assets:
        if asset.get("kind") not in ("document", "pdf"):
            continue
        album = str(asset.get("album", "Supporting notes"))
        context = " ".join(str(asset.get(key, "")) for key in ("album", "title", "filename")).casefold()
        if not all(term in (context + " " + str(asset.get("text", "")).casefold()) for term in terms):
            continue
        child = album
        if "design and outfit notes" in album.casefold() or "design & outfit notes" in album.casefold():
            parent = "Design & outfit notes"
            child = album.partition("·")[2]
            child = child.strip() or "General design notes"
        elif any(word in context for word in ("historical", "history", "helper", "quarantine")):
            parent = "History & helpers"
        elif any(word in context for word in ("storyboard", "lyric", "music", "story beat")):
            parent = "Story & music"
        elif any(word in context for word in ("collaborator", "gemini", "grok", "panhandler")) or re.search(r"\bflow\b", context):
            parent = "Collaborator briefs"
        elif any(word in context for word in ("tattoo", "piercing", "stencil", "detail")):
            parent = "Tattoos & details"
        elif any(word in context for word in ("outfit", "design", "casting", "character")):
            parent = "Design & outfit notes"
        else:
            parent = "Production & workflows"
        parents[parent].setdefault(child, []).append(asset)
    return {name: groups for name, groups in parents.items() if groups}


def storyboard_window(results: list[tuple[dict, dict | None]], lower: int, upper: int) -> list[tuple[dict, dict | None]]:
    def within(asset):
        position = asset.get("storyboardPosition")
        if isinstance(position, (int, float)) and not isinstance(position, bool):
            return lower <= position <= upper
        return lower == 0 and upper == 100
    filtered = [row for row in results if within(row[0])]
    return sorted(filtered, key=lambda row: row[0].get("storyboardOrder", float("inf")))


def storyboard_stage(asset: dict, reviews: dict[str, dict]) -> str | None:
    default = "preliminary" if asset.get("category") == "storyboard" else None
    value = reviews.get(asset["id"], {}).get("storyboardStage") or asset.get("storyboardStage", default)
    return value if value in STORYBOARD_STAGES else default


def storyboard_themes(asset: dict, album: dict | None = None) -> list[str]:
    explicit = asset.get("storyboardThemes", asset.get("themes", []))
    values = explicit if isinstance(explicit, list) and explicit else asset.get("tags", [])
    values = [value for value in values if isinstance(value, str) and value.casefold() != "storyboard"
              and not re.fullmatch(r"series\s*\d+", value.casefold())] if isinstance(values, list) else []
    if not values and album and album.get("title"):
        values = [album["title"]]
    return list(dict.fromkeys(values))


def sweep_payload(assets: list[dict], reviews: dict[str, dict], favorites: set[str], basket: set[str]) -> dict:
    payload = review_payload(assets, reviews, favorites, basket)
    payload["sweep"] = {"status": "prepared; not sent or executed", "requestedCollaborator": "Panhandler Nova",
                        "instruction": "Review these choices against source hashes. Apply only the stated scopes. Confirm promotion requests and keep Multiverse out of Prime working references. Do not infer deletion from a queue flag.",
                        "promotionQueue": [{**reference_record(asset), "workingReference": reviews[asset["id"]]["workingReference"]}
                                           for asset in assets if (reviews.get(asset["id"], {}).get("workingReference") or {}).get("status") == "requested"
                                           and export_allowed(asset, reviews, "prime")]}
    return payload

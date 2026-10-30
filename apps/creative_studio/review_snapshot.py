"""Conservative, offline review overlay for a portable publication snapshot.

This does not import a review into the local source catalog. Only dated user
fields on verified images enter the returned copy; canonical scope and validator
records stay untouched. The report is for the publisher, not an approval engine.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json

from library_helpers import normalize_decision, reference_record, resolve_asset_reference


EDITABLE_FIELDS = ("status", "note", "shotPlan", "likenessRating", "sceneQualityRating",
                   "storyboardStage", "variant", "workingReference", "workingReferenceScope",
                   "collectionState", "multiverseSelection", "creativeReview", "castUse")


def _time(value) -> float:
    if not isinstance(value, str) or not value:
        return 0
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return (stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)).timestamp()
    except (ValueError, TypeError, OverflowError):
        return 0


def _field_time(row: dict, field: str) -> float:
    dates = row.get("fieldUpdatedAt", {})
    explicit = dates.get(field) if isinstance(dates, dict) else None
    value = _time(explicit) or _time(row.get(field + "UpdatedAt")) or _time(row.get("updatedAt"))
    if field == "shotPlan" and row.get("shotPlan") is None:
        clear = row.get("shotPlanClearEvidence")
        if isinstance(clear, dict):
            value = max(value, _time(clear.get("updatedAt")))
    return value


def _iso(value: float) -> str:
    return datetime.fromtimestamp(value, timezone.utc).isoformat()


def overlay_review_snapshot(catalog: dict, payload: dict, *, source_label: str = "Latest local review export",
                            include_selections: bool = True) -> tuple[dict, dict]:
    """Return (independent catalog copy, reconciliation report); never write files.

    A field is eligible only when explicitly present in a user-origin record,
    hash-matched through the current catalog/verified aliases, and strictly newer
    than its canonical value. Equal-time or undated differences are conflicts.
    No export timestamp is substituted for the date of a user decision.
    """
    if (not isinstance(payload, dict) or payload.get("format") != "cfa-visual-review-v1"
            or not isinstance(payload.get("items"), list)):
        raise ValueError("Expected a CFA review export with an items list.")
    result = deepcopy(catalog)
    if 'collaboratorReviews' in catalog or 'collaboratorReviews' in payload:
        from collaborator_review import merge
        result['collaboratorReviews'] = merge(catalog.get('collaboratorReviews', {}),
                                              payload.get('collaboratorReviews', {}))
    if 'collaboratorReviewBackups' in catalog or 'collaboratorReviewBackups' in payload:
        from collaborator_review import merge_backups
        result['collaboratorReviewBackups'] = merge_backups(catalog.get('collaboratorReviewBackups', []),
                                                          payload.get('collaboratorReviewBackups', []))
    # Take plans are immutable shot records, not image decisions. Reconcile them
    # separately so a review export cannot lose the earlier take history.
    if 'storyboardTakes' in catalog or 'storyboardTakes' in payload:
        from storyboard_takes import empty, merge
        result['storyboardTakes'] = merge(catalog.get('storyboardTakes', empty()),
                                          payload.get('storyboardTakes', empty()))
    if 'storyboardTakeBackups' in catalog or 'storyboardTakeBackups' in payload:
        retained = []
        for value in (catalog.get('storyboardTakeBackups', []), payload.get('storyboardTakeBackups', [])):
            if not isinstance(value, list):
                raise ValueError('Storyboard take backups must be a list.')
            for record in value:
                if record not in retained:
                    retained.append(deepcopy(record))
        result['storyboardTakeBackups'] = retained
    assets, aliases = result.get("assets", []), result.get("assetAliases", [])
    raw = result.get("reviewDecisions", [])
    wrapped = isinstance(raw, dict)
    rows = raw.get("items", []) if wrapped else raw
    if not isinstance(rows, list):
        raise ValueError("Catalog review decisions must be a list or items envelope.")
    report = {"sourceLabel": source_label, "exported": payload.get("exported"),
              "sourceDigest": hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False,
                                                       allow_nan=False, separators=(",", ":")).encode()).hexdigest(),
              "inputRecords": len(payload["items"]), "applied": [], "conflicts": [], "skipped": [],
              "aliases": [], "unchangedFields": 0}
    report['changedCollaboratorTasks'] = [task_id for task_id, record in result.get('collaboratorReviews', {}).items()
                                         if catalog.get('collaboratorReviews', {}).get(task_id) != record]
    by_id, by_index, mismatched_ids = {}, {}, set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        asset = resolve_asset_reference(row, assets, aliases, require_hash=True)
        if not asset:
            if any(asset.get("id") == row.get("id") for asset in assets):
                mismatched_ids.add(row.get("id"))
            continue
        aid = asset["id"]
        prior = by_id.get(aid)
        if prior is None or _time(row.get("updatedAt")) > _time(prior.get("updatedAt")):
            by_id[aid] = row
        if row.get("id") == aid:
            by_index[aid] = index
    for item in payload["items"]:
        if not isinstance(item, dict):
            report["skipped"].append({"reason": "invalid_record"})
            continue
        aid = item.get("id")
        asset = resolve_asset_reference(item, assets, aliases, require_hash=True)
        if not asset:
            report["skipped"].append({"id": aid, "reason": "unmatched_id_or_hash"})
            continue
        target_id = asset["id"]
        if target_id in mismatched_ids and target_id not in by_id:
            report["skipped"].append({"id": aid, "reason": "canonical_hash_conflict"})
            continue
        if item.get("origin") != "user":
            report["skipped"].append({"id": aid, "reason": "catalog_echo_or_origin_unknown"})
            continue
        try:
            normalized = normalize_decision(item, partial=True, allow_catalog_variant=False)
        except (ValueError, TypeError):
            report["skipped"].append({"id": aid, "reason": "invalid_review_fields"})
            continue
        prior = by_id.get(target_id, {})
        changed = []
        updated = deepcopy(prior)
        existing_dates = prior.get("fieldUpdatedAt", {})
        dates = dict(existing_dates) if isinstance(existing_dates, dict) else {}
        for field in EDITABLE_FIELDS:
            if field in prior and field not in dates and (stamp := _field_time(prior, field)):
                dates[field] = _iso(stamp)
        for field in EDITABLE_FIELDS:
            if field not in normalized:
                continue
            value = normalized[field]
            default = "" if field == "note" else asset.get(field) if field in ("variant", "workingReference") else None
            prior_value = prior.get(field, default)
            if value == prior_value:
                report["unchangedFields"] += 1
                continue
            incoming_time, prior_time = _field_time(item, field), _field_time(prior, field)
            # A later whole-record save must not resurrect a plan with a dated,
            # field-specific clear unless the plan itself is demonstrably newer.
            clear = prior.get("shotPlanClearEvidence")
            if field == "shotPlan" and value is not None and isinstance(clear, dict):
                prior_time = max(prior_time, _time(clear.get("updatedAt")))
            if not incoming_time or incoming_time <= prior_time:
                reason = "undated_change" if not incoming_time else "canonical_newer" if incoming_time < prior_time else "same_time_different_value"
                report["conflicts"].append({"id": target_id, "sourceID": aid, "field": field, "reason": reason,
                                             "canonical": deepcopy(prior_value), "incoming": deepcopy(value)})
                continue
            updated[field] = deepcopy(value)
            dates[field] = _iso(incoming_time)
            changed.append(field)
            if field == "variant":
                updated["variantSource"] = "user"
            if field == "shotPlan":
                updated["shotPlanUpdatedAt"] = _iso(incoming_time)
        if not changed:
            continue
        updated.update(reference_record(asset))
        updated["fieldUpdatedAt"] = dates
        updated["updatedAt"] = _iso(max([_time(prior.get("updatedAt")), *(_time(value) for value in dates.values())]))
        updated["origin"] = "user"
        if target_id in by_index:
            rows[by_index[target_id]] = updated
        else:
            by_index[target_id] = len(rows)
            rows.append(updated)
        by_id[target_id] = updated
        report["applied"].append({"id": target_id, "sourceID": aid, "fields": changed})
        if target_id != aid:
            report["aliases"].append({"sourceID": aid, "canonicalID": target_id})
    if wrapped:
        result["reviewDecisions"]["items"] = rows
    else:
        result["reviewDecisions"] = rows
    if include_selections:
        selections = {}
        for key in ("favorites", "exportBasket"):
            values = payload.get(key, [])
            if not isinstance(values, list):
                raise ValueError(f"{key} must be a list of image references.")
            accepted = {}
            for value in values:
                asset = resolve_asset_reference(value, assets, aliases, require_hash=True)
                if asset:
                    accepted[asset["id"]] = reference_record(asset)
                else:
                    report["skipped"].append({"id": value.get("id") if isinstance(value, dict) else None,
                                               "reason": "unmatched_" + key})
            selections[key] = list(accepted.values())
        result["reviewSessionSeed"] = {"id": report["sourceDigest"], **selections}
    report["changedRecords"] = len({row["id"] for row in report["applied"]})
    report["changedFields"] = sum(len(row["fields"]) for row in report["applied"])
    result["reviewSnapshot"] = {key: report[key] for key in ("sourceLabel", "sourceDigest", "exported", "changedRecords", "changedFields", "changedCollaboratorTasks")}
    return result, report

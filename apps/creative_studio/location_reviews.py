"""Lossless transfer of location-family direction, independently of image decisions.

The native editor transports these records without selecting a location or
inventing attribution. Conflicting and unrecognized records remain exportable.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json


FIELDS = {"project", "locationFamilyID", "note", "updatedAt", "origin", "attributionStatus",
          "projectControllerID", "decisionScope", "reviewer", "reviewerControllerID",
          "decisionAuthorityControllerID", "humanReview"}


def _stable(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def _time(value):
    if not isinstance(value, str) or not value:
        return 0
    try:
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return (value if value.tzinfo else value.replace(tzinfo=timezone.utc)).timestamp()
    except (ValueError, TypeError, OverflowError):
        return 0


def _record(value):
    if (not isinstance(value, dict)
            or any(not isinstance(value.get(key), str) or not value[key].strip()
                   for key in ("project", "locationFamilyID"))
            or not isinstance(value.get("note"), str)
            or len(value["note"]) > 20000
            or value.get("decisionScope", "location") != "location"):
        return None
    if any(key in value and not isinstance(value[key], str)
           for key in FIELDS - {"note", "updatedAt", "humanReview"}):
        return None
    if "humanReview" in value and not isinstance(value["humanReview"], dict):
        return None
    # Retain the declared attribution exactly; this transport never confirms it.
    return {key: deepcopy(item) for key, item in value.items() if key in FIELDS}


def merge_state(existing, incoming):
    """Return current notes plus backups; a stale import cannot erase newer work.

    Empty notes are dated explicit clears. Equal-time conflicts retain the
    current value. Undated notes may start a family but cannot replace one.
    Superseded notes, unsupported fields and unknown formats remain in backups.
    """
    records, backups, seen = {}, [], set()

    def preserve(reason, value):
        entry = {"reason": reason, "data": deepcopy(value)}
        key = _stable(entry)
        if key not in seen:
            backups.append(entry)
            seen.add(key)

    for source in (existing or {}, incoming or {}):
        if not isinstance(source, dict):
            raise ValueError("Location review state must be an object.")
        raw_backups = source.get("locationReviewBackups", [])
        if isinstance(raw_backups, list):
            for entry in raw_backups:
                if isinstance(entry, dict) and isinstance(entry.get("reason"), str) and "data" in entry:
                    key = _stable(entry)
                    if key not in seen:
                        backups.append(deepcopy(entry))
                        seen.add(key)
                else:
                    preserve("Unrecognized location review backup", entry)
        else:
            preserve("Unrecognized location review backup list", raw_backups)
        values = source.get("locationReviews", [])
        if not isinstance(values, list):
            preserve("Unrecognized location review list", values)
            continue
        for value in values:
            record = _record(value)
            if record is None:
                preserve("Unsupported location review", value)
                continue
            if record != value:
                preserve("Additional location review fields retained", value)
            key = (record["project"], record["locationFamilyID"])
            prior = records.get(key)
            if prior is None:
                records[key] = record
            elif prior != record:
                before, after = _time(prior.get("updatedAt")), _time(record.get("updatedAt"))
                if after and after > before:
                    preserve("Superseded location review", prior)
                    records[key] = record
                else:
                    reason = ("Undated location review conflict" if not after else
                              "Equal-time location review conflict" if after == before else
                              "Older location review retained")
                    preserve(reason, record)
    return {"locationReviews": list(records.values()), "locationReviewBackups": backups}

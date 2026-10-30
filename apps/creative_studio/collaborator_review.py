"""One bounded returned-still questionnaire; saved replies are never dispatch receipts."""
from copy import deepcopy
from datetime import datetime, timezone
import io
import json
import re
from uuid import uuid4
import zipfile

TASK_ID = "grok-proof-package"
VERSION = "hon-grok-return-20261008-v1"
FORMAT = "cfa-collaborator-review-v1"
CHOICES = {"": "Choose a result…", "meets_brief": "Meets this requested change",
           "needs_correction": "Needs correction", "reject": "Do not use this return",
           "cannot_assess": "Cannot assess / need clarification"}
DIRECTIONS = {"": "Choose the next action…", "bounded_corrections": "Request only the corrections recorded here",
              "hold_clarify": "Hold and clarify before more work",
              "nominate_motion": "Nominate one still for a separate motion handoff"}
EVIDENCE = [
    {"assetID": "hon:doc:docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/handoffs/grok_20261008/START_HERE.txt",
     "sha256": "56a80126d9990736496440eb1b511386aee499e4ca2656033f5b5361089a1386", "role": "October 8 requested work"},
    {"assetID": "hon:doc:docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/grok_return_20261009/START_HERE.txt",
     "sha256": "dd10817e01ab7bd6d19c76e640c35072e7f6dcf49cba4943ba2a470a9abb2f18", "role": "October 9 verified receipt and limits"},
    {"assetID": "hon:doc:docs/notes/explorable_world/comfy/projects/collaborators/grok_design_instructions.txt",
     "sha256": "938be3298404548c5ea07063d56569369e68d2b3a20f09411ccb444da78d7820",
     "role": "Living design instructions supersede dated detail rules; Hon has four upper gold caps, not the old two-canines-only pattern"},
]
STANDARD = {"assetID": "HD-DROP-ef5d59a6402e", "sha256": "ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978"}
QUESTIONS = [
    {"id": "REV-HD-001", "title": "Cash-counting vest", "assetID": "HD-RETURN-bc5b8c111da7",
     "sha256": "bc5b8c111da73c15d0e0a69462ba2a416e1fc2b7364577354c439509655aeb00",
     "source": {"assetID": "HD-DROP-2691712601a9", "sha256": "2691712601a9da9ab3c629b2c1d3204cdd1106cb64c301218aec1eb63182b702"},
     "request": "Correct visible tattoos and details while preserving the cash-counting vest, money/table, ship interior, composition and lighting.",
     "question": "Does this return deliver the detail correction while keeping the selected cash-counting outfit and scene?",
     "known": "The intake records that REV-HD-001 changed the vest and scene. Review that preservation failure explicitly; a good new image does not by itself fulfill this correction."},
    {"id": "REV-HD-002", "title": "Black overcoat", "assetID": "HD-RETURN-cfcf8f8004ef",
     "sha256": "cfcf8f8004ef76784c2867412a2a38648edd170820c1bec17d9b35b0795edb94",
     "source": {"assetID": "HD-DROP-56a50dabe9e0", "sha256": "56a50dabe9e0357f3512288b0f5ade4d68d9afa1a080f80d111e047f96827057"},
     "request": "Correct visible tattoos, mouth and jewelry against the supplied design reference. Preserve the black overcoat, night boarding ramp, composition and atmosphere.",
     "question": "Are the visible details corrected with the selected overcoat and night boarding scene preserved?"},
    {"id": "REV-HD-003", "title": "Pinstripe suit", "assetID": "HD-RETURN-9158a4df3f42",
     "sha256": "9158a4df3f4218350a2d30155dbc3c767fb80a01e71ebfb861c1dc416406bd5c",
     "source": {"assetID": "HD-DROP-1966838931ad", "sha256": "1966838931adb71d4443b608d65b9c3613bdc7de7fd6ce3e38c9b35e344e51f7"},
     "request": "Correct visible face/neck, teeth and jewelry. Keep the navy three-piece, tie and tie bar, pocket square, watch, pose and polished office mood. Keep the chest covered.",
     "question": "Does this prepare the pinstripe look without changing the selected wardrobe or exposing covered details?"},
    {"id": "REV-HD-004", "title": "Western fringe / saloon", "assetID": "HD-RETURN-26a91590b6c0",
     "sha256": "26a91590b6c03f3c8de62f4ab69e0b4ce7d466b7707a2e9cf426c771a69c79ec",
     "source": {"assetID": "HD-DROP-bb0780a46f7d", "sha256": "bb0780a46f7d6f0ef5493939ba1f1920366dd670ff8b5da3738c3c04672ec596"},
     "request": "Repair the visible blaster/holster and belt attachment. Preserve western fringe, dark shirt, bolo tie, pose and saloon. Match visible character details; the hip side is provisional for this proof.",
     "question": "Is the prop coherent and seated in its holster while the selected saloon look and visible character details stay intact?",
     "known": "The provider reports a revolver-like prop, a re-staged saloon and expression, and overly long canines. This exact image is also cataloged as HIP-SALOON-01; it is byte-identical to the REV-HD-004 return."},
    {"id": "PROP-HD-HIP", "title": "Hip detail", "assetID": "HD-RETURN-41b93f64e7ea",
     "sha256": "41b93f64e7ea7199974101575b5704ce037f019e02e507e2b70cb1b499263350",
     "source": {"assetID": "HD-RETURN-26a91590b6c0", "sha256": "26a91590b6c03f3c8de62f4ab69e0b4ce7d466b7707a2e9cf426c771a69c79ec"},
     "request": "Provide a matching detail of the repaired sci-fi blaster/holster, readable attachment and overlap. A labeled crop of the corrected proof is allowed; it is not original hardware artwork.",
     "question": "Does the close view make the intended prop and attachment clear enough, or what must change?",
     "known": "The recorded return is an upscaled crop of generated REV-HD-004. The provider reports a western-revolver appearance and provisional character-left / viewer-right placement. No global side choice is established here."},
    {"id": "CALEB-K_REF", "title": "Caleb character proof", "assetID": "HD-RETURN-147fbed5f795",
     "sha256": "147fbed5f795c025ddddaa45598311c7ea40212e8d35f3d50df08bd0ff1b9cd1",
     "request": "Propose one neutral Caleb K reference: a distinct middle-aged white male lawyer, restrained wardrobe, no supplied real-person likeness. Any invented tattoo requires its companion design sheet.",
     "question": "Does this candidate work as the Caleb concept requested, or what should change before using him in the scene?",
     "known": "This is a new character proposal, with no approved likeness in the original brief. Provider notes say no tattoos or piercings were invented."},
    {"id": "CAL-P01", "title": "Hon Dolo + Caleb meeting", "assetID": "HD-RETURN-d50fe2346406",
     "sha256": "d50fe23464067486851627ce626652129c51b981bd4041bebb9fafcf2dc4f232",
     "source": {"assetID": "HD-DROP-9cecaad5ed57", "sha256": "9cecaad5ed5764a4109c053b17fb09afd7bb0f97557fe61f88a2f72ac73cca5a"},
     "request": "One friendly saloon master with Hon Dolo and Caleb: distinct faces, clear eyelines and separate hands. Preserve Hon's fringe/bar alpha and visible current details. No invented dialogue, lyric timing or lip-sync.",
     "question": "Does the interaction work, and what continuity fixes are still needed before this scene can move forward?",
     "known": "The intake records tattoo-placement defects in CAL-P01. Caleb's neutral proof is a candidate reference, not an accepted master."},
]


def _text(value, label, limit=20000, required=False):
    if not isinstance(value, str) or len(value) > limit or (required and not value.strip()):
        raise ValueError(f"Invalid collaborator review {label}.")
    return value


def _time(value):
    _text(value, "timestamp", 128, True)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError()
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        raise ValueError("Collaborator review timestamps must include a valid timezone.") from None


def _answers(value):
    if not isinstance(value, dict) or len(value) > 100:
        raise ValueError("Collaborator review answers must be an object.")
    for key, answer in value.items():
        _text(key, "question ID", 512, True)
        if not isinstance(answer, dict) or not isinstance(answer.get("choice"), str) or answer["choice"] not in CHOICES:
            raise ValueError("Invalid collaborator review answer.")
        _text(answer.get("note"), "note")
        ref = answer.get("reference")
        if not isinstance(ref, dict):
            raise ValueError("An answer needs its exact reference.")
        _text(ref.get("assetID"), "asset ID", 512, True)
        if not isinstance(ref.get("sha256"), str) or not re.fullmatch(r"[a-f0-9]{64}", ref["sha256"]):
            raise ValueError("An answer needs its exact reference hash.")
        _time(answer.get("updatedAt"))


def _direction(value):
    if not isinstance(value, dict) or not isinstance(value.get("choice", ""), str) or value.get("choice", "") not in DIRECTIONS:
        raise ValueError("Invalid collaborator review next action.")
    _text(value.get("note", ""), "next-action note")
    if "assetID" in value:
        _text(value["assetID"], "nominated asset ID", 512)


def normalize(value):
    """Validate without rebinding old answers; unknown task/question metadata survives."""
    if not isinstance(value, dict) or len(value) > 500:
        raise ValueError("Collaborator reviews must be an object.")
    result = deepcopy(value)
    for task_id, record in result.items():
        _text(task_id, "task ID", 512, True)
        if (not isinstance(record, dict) or record.get("format") != FORMAT or record.get("taskID") != task_id
                or not isinstance(record.get("state"), str) or record["state"] not in {"draft", "ready"}):
            raise ValueError("Invalid collaborator review record.")
        _text(record.get("questionnaireVersion"), "questionnaire version", 512, True)
        _time(record.get("updatedAt"))
        record.setdefault("readyReplyID", None)
        _answers(record.get("answers"))
        _direction(record.get("direction"))
        replies = record.get("replies")
        if not isinstance(replies, list) or len(replies) > 1000:
            raise ValueError("Collaborator reply history must be a list.")
        seen = set()
        for reply in replies:
            if not isinstance(reply, dict):
                raise ValueError("Invalid prepared reply.")
            _text(reply.get("id"), "reply ID", 512, True)
            if reply["id"] in seen:
                raise ValueError("Duplicate immutable reply ID.")
            seen.add(reply["id"])
            _time(reply.get("preparedAt"))
            _text(reply.get("questionnaireVersion"), "reply version", 512, True)
            _answers(reply.get("answers"))
            _direction(reply.get("direction"))
            if reply["questionnaireVersion"] == VERSION:
                if reply.get("questions") != QUESTIONS or reply.get("evidence") != EVIDENCE or errors(reply):
                    raise ValueError("Prepared reply does not contain the complete questionnaire and source evidence.")
        ready = record.get("readyReplyID")
        if record["state"] == "ready":
            snapshot = next((r for r in replies if r["id"] == ready), None)
            if not snapshot or any(snapshot[key] != record[key] for key in ("questionnaireVersion", "answers", "direction")):
                raise ValueError("A ready reply must match its frozen answer snapshot.")
            if record["questionnaireVersion"] == VERSION and errors(record):
                raise ValueError("A ready reply has unanswered required questions.")
        elif ready is not None:
            raise ValueError("A draft cannot retain an active ready reply.")
    # Reject non-JSON metadata and non-finite values before callers update sessions.
    try:
        json.dumps(result, allow_nan=False)
    except (TypeError, ValueError):
        raise ValueError("Collaborator review metadata must be finite JSON.") from None
    return result


def merge(*mappings):
    """Latest draft wins; prepared reply IDs remain immutable across every import."""
    result = {}
    for mapping in mappings:
        for task_id, incoming in normalize(mapping).items():
            if task_id not in result:
                result[task_id] = incoming
                continue
            prior = result[task_id]
            history = {r["id"]: r for r in prior["replies"]}
            for reply in incoming["replies"]:
                if reply["id"] in history and history[reply["id"]] != reply:
                    raise ValueError("Conflicting immutable collaborator reply ID: " + reply["id"])
                history[reply["id"]] = reply
            old_time, new_time = _time(prior["updatedAt"]), _time(incoming["updatedAt"])
            if old_time == new_time and any(prior[k] != incoming[k] for k in
                    ("questionnaireVersion", "state", "answers", "direction", "readyReplyID")):
                raise ValueError("Conflicting collaborator answers at the same timestamp: " + task_id)
            result[task_id] = {**prior, **incoming} if new_time >= old_time else {**incoming, **prior}
            result[task_id]["replies"] = list(history.values())
    return normalize(result)


def merge_backups(*lists):
    """Keep unread source/browser records intact without activating them."""
    result, seen = [], set()
    for rows in lists:
        if not isinstance(rows, list) or len(rows) > 1000:
            raise ValueError("Collaborator review backups must be a list.")
        for row in rows:
            if not isinstance(row, dict) or "data" not in row:
                raise ValueError("Invalid collaborator review backup.")
            _text(row.get("origin"), "backup origin", 512, True)
            _text(row.get("reason"), "backup reason", 20000, True)
            key = json.dumps(row, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            if key not in seen:
                result.append(deepcopy(row))
                seen.add(key)
    return result


def empty(now=None):
    return {"format": FORMAT, "taskID": TASK_ID, "questionnaireVersion": VERSION,
            "state": "draft", "answers": {}, "direction": {"choice": "", "note": ""},
            "updatedAt": now or datetime.now(timezone.utc).isoformat(), "replies": [], "readyReplyID": None}


def reference(question):
    return {key: question[key] for key in ("assetID", "sha256")}


def available(question, assets):
    asset = next((a for a in assets if a.get("id") == question["assetID"]), None)
    return asset if asset and asset.get("kind") == "image" and asset.get("sha256") == question["sha256"] else None


def answer_complete(question, answer, assets=None):
    if not isinstance(answer, dict) or answer.get("reference") != reference(question) or not answer.get("choice"):
        return False
    if answer["choice"] != "meets_brief" and not answer.get("note", "").strip():
        return False
    return assets is None or available(question, assets) is not None or answer["choice"] == "cannot_assess"


def errors(record, assets=None):
    problems = []
    if record.get("questionnaireVersion") != VERSION:
        problems.append("This draft belongs to an earlier questionnaire; start a revised draft before preparing it.")
    for question in QUESTIONS:
        if not answer_complete(question, record.get("answers", {}).get(question["id"]), assets):
            problems.append(question["id"] + ": choose a result and explain corrections, rejection or uncertainty. Unavailable exact images require Cannot assess.")
    direction = record.get("direction", {})
    if not direction.get("choice"):
        problems.append("Choose the next action for Grok.")
    if direction.get("choice") == "hold_clarify" and not direction.get("note", "").strip():
        problems.append("Explain what needs clarification before more work.")
    if direction.get("choice") == "nominate_motion":
        question = next((q for q in QUESTIONS if q["assetID"] == direction.get("assetID") and q["id"] != "PROP-HD-HIP"), None)
        if not question or record.get("answers", {}).get(question["id"], {}).get("choice") != "meets_brief" or (assets is not None and not available(question, assets)):
            problems.append("Nominate an available still that meets its requested change; the hip crop alone cannot be a scene handoff.")
    return problems


def progress(record, assets):
    if not record:
        return {"answered": 0, "total": len(QUESTIONS), "ready": False}
    return {"answered": sum(answer_complete(q, record.get("answers", {}).get(q["id"]), assets) for q in QUESTIONS),
            "total": len(QUESTIONS), "ready": record.get("state") == "ready" and not errors(record, assets)}


def edit(record, *, question_id=None, choice="", note="", direction=None, now=None):
    result = deepcopy(record or empty(now))
    result.update(state="draft", readyReplyID=None, updatedAt=now or datetime.now(timezone.utc).isoformat())
    if result["questionnaireVersion"] != VERSION:
        raise ValueError("This questionnaire version needs reconciliation before editing.")
    if question_id is not None:
        question = next((q for q in QUESTIONS if q["id"] == question_id), None)
        if not question:
            raise ValueError("Unknown questionnaire question.")
        result["answers"][question_id] = {"choice": choice, "note": note, "reference": reference(question), "updatedAt": result["updatedAt"]}
    if direction is not None:
        result["direction"] = deepcopy(direction)
    return normalize({TASK_ID: result})[TASK_ID]


def prepare(record, assets, *, now=None, reply_id=None):
    result = normalize({TASK_ID: record})[TASK_ID]
    if problems := errors(result, assets):
        raise ValueError("\n".join(problems))
    timestamp = now or datetime.now(timezone.utc).isoformat()
    reply = {"id": reply_id or "reply-" + uuid4().hex, "preparedAt": timestamp,
             "questionnaireVersion": VERSION, "answers": deepcopy(result["answers"]), "direction": deepcopy(result["direction"]),
             "questions": deepcopy(QUESTIONS), "evidence": deepcopy(EVIDENCE), "status": "ready_not_sent"}
    result["replies"].append(reply)
    result.update(state="ready", readyReplyID=reply["id"], updatedAt=timestamp)
    return normalize({TASK_ID: result})[TASK_ID]


def reply_text(record):
    reply = next((r for r in record.get("replies", []) if r["id"] == record.get("readyReplyID")), None)
    if not reply:
        raise ValueError("Prepare the reply before exporting it.")
    lines = ["HON DOLO — BOUNDED STILL RETURN REVIEW", "To: Grok", "Task: " + TASK_ID,
             "Reply: " + reply["id"], "Prepared: " + reply["preparedAt"],
             "Ready for manual delivery. Not sent. No new generation or global approval is implied.",
             "Scope: seven exact returned outputs from GROK-HD-20261008. Historical requested work is shown per item.",
             "Use the living design instructions below where they supersede dated package details. Do not restore the old two-canines-only tooth pattern.", ""]
    for q in reply["questions"]:
        answer = reply["answers"][q["id"]]
        lines += [q["id"] + " — " + q["title"], "Requested: " + q["request"],
                  "Returned asset: " + q["assetID"], "SHA256: " + q["sha256"],
                  "Result: " + CHOICES[answer["choice"]], "Note: " + (answer["note"].strip() or "No additional note."), ""]
    direction = reply["direction"]
    lines += ["NEXT ACTION", DIRECTIONS[direction["choice"]]]
    if direction.get("assetID"):
        lines += ["Nominated still: " + direction["assetID"]]
    if direction.get("note"):
        lines += [direction["note"]]
    lines += ["", "A motion nomination is for a separate handoff. Unresolved defects and unknowns remain as recorded.",
              "Original request and receipt evidence:"]
    lines += [e["role"] + ": " + e["assetID"] + " | SHA256 " + e["sha256"] for e in reply["evidence"]]
    return "\n".join(lines) + "\n"


def reply_zip(record):
    """One task-only package; unrelated reviews and source image bytes are excluded."""
    normalize({TASK_ID: record})
    text = reply_text(record)
    envelope = {"format": "cfa-visual-review-v1", "exported": record["updatedAt"], "items": [], "favorites": [],
                "collaboratorReviews": {TASK_ID: deepcopy(record)}}
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("GROK_REPLY.txt", text)
        archive.writestr("cfa-visual-review.json", json.dumps(envelope, ensure_ascii=False, indent=2))
        archive.writestr("README.txt", "Prepared for manual delivery; not sent.\nGROK_REPLY.txt is the consolidated reply.\n"
                         "cfa-visual-review.json restores this task's draft/ready answers and reply history through the normal review importer.\n"
                         "Image files are not attached. Exact original IDs/hashes identify the seven returned outputs; hosted previews may be resized.\n")
    return output.getvalue()

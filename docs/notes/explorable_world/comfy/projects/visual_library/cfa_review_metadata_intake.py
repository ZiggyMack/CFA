"""Bounded, read-only adapter for the frozen Pent House START_HERE r002 drop.

No review decision is inferred or written.  Provider QA, scoped V-Team checks,
human acceptance and site validation are deliberately separate namespaces.
The caller may append ``newAssets`` and store the remaining result as metadata;
it must not use ``currentCandidate`` as an accepted-default replacement.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import mimetypes
import os
from collections import Counter, defaultdict
from pathlib import Path
import re


DROP = "docs/notes/explorable_world/comfy/references/From Grok"
LIBRARY = "docs/notes/explorable_world/comfy/projects/visual_library"
START_SHA = "1f30ae11b39232ae7feed0be8b2e4fb690c15ee3ad9dd40390ad84acc90a70e5"
START_MANIFEST_SHA = "b9a76ce288cffc888d72daff6362e11434de84118c8d6bf649248d5873ce4280"
VIS_ORIGINAL_MANIFEST_SHA = "671784f33bdcf4d6a221c8cdf4ba6762bc665362f2b53219b7087d863f86281e"
FALCON = "FALCON-METADATA_v004"
RESOLVER = "FALCON-META-RESOLVER_r001"
LISAN = "GROK-LAG-1K-REVIEW-META-20261021"
CORRECTIONS = LISAN + "_r002-corrections"
VIS = "GROK-LAG-VIS-NATURAL-v003-redo"
CHIN = VIS + "_chinfix-v005-v006"
VIDEO = "GROK-VIDEO-TEST_v001"
SHA = re.compile(r"^[a-f0-9]{64}$")
EMPTY = {"", "null", "none", "unknown", "n/a", "not recorded"}


class IntakeError(ValueError):
    """The pinned handoff cannot be safely interpreted."""


def _value(value):
    if value is None or str(value).strip().lower() in EMPTY:
        return None
    return value


def _digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _under(root, value):
    """Resolve only repository paths, including recorded D: paths, fail closed."""
    text = re.sub(r"/+", "/", str(value).replace("\\", "/"))
    recorded_root = "D:/Documents/CFA/"
    if text.lower().startswith(recorded_root.lower()):
        text = text[len(recorded_root):]
    elif re.match(r"^[A-Za-z]:", text) or text.startswith("/"):
        raise IntakeError(f"Path is outside the repository: {value}")
    target = (root / text).resolve()
    if not target.is_relative_to(root.resolve()):
        raise IntakeError(f"Path escapes the repository: {value}")
    return target


def _rows(path, delimiter="\t"):
    lines = (line for line in path.read_text(encoding="utf-8-sig").splitlines()
             if line.strip() and not line.startswith("#"))
    return list(csv.DictReader(io.StringIO("\n".join(lines)), delimiter=delimiter))


def _hashes(value):
    return re.findall(r"\b[a-f0-9]{64}\b", value or "")


def verify_manifest(repo_root, package_root, manifest, expected_sha256):
    """Verify a pinned manifest and every explicitly listed file, no globbing."""
    repo_root, package_root = Path(repo_root).resolve(), Path(package_root).resolve()
    path = _under(repo_root, (package_root / manifest).relative_to(repo_root))
    if _digest(path) != expected_sha256:
        raise IntakeError(f"Manifest hash mismatch: {path}")
    verified = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-fA-F0-9]{64})\s+\*?(.+)", line.strip())
        if not match:
            raise IntakeError(f"Malformed manifest line in {path}: {line}")
        sha, name = match.groups()
        candidate = _under(repo_root, str(package_root.relative_to(repo_root)) + "/" + name)
        if not candidate.is_relative_to(package_root):
            raise IntakeError(f"Manifest escapes package: {name}")
        if not candidate.is_file() or _digest(candidate) != sha.lower():
            raise IntakeError(f"Manifest media/file mismatch: {candidate}")
        verified[candidate.relative_to(repo_root).as_posix()] = sha.lower()
    return verified


class _Intake:
    def __init__(self, root, existing_assets):
        self.root = Path(root).resolve()
        self.base = self.root / DROP
        self.existing = defaultdict(list)
        self.existing_paths = {}
        for asset in existing_assets:
            sha = asset.get("sha256") or asset.get("contentSha256")
            if sha and SHA.fullmatch(sha):
                self.existing[sha].append(asset)
                if asset.get("repoPath"):
                    self.existing_paths[asset["repoPath"].replace("\\", "/")] = asset
        self.new = {}
        self.metadata = {}
        self.families = {}
        self.packages = []
        self.verified = {}
        self.hash_cache = {}
        self.duplicates = []
        self.dependencies = []

    def ref(self, folder, name, selector=None):
        rel = f"{DROP}/{folder}/{name}"
        sha = self.verified.get(rel)
        if not sha:
            raise IntakeError(f"Evidence is not manifest verified: {rel}")
        result = {"repoPath": rel, "sha256": sha}
        if selector is not None:
            result["selector"] = selector
        return result

    def json(self, folder, name):
        self.ref(folder, name)
        return json.loads((self.base / folder / name).read_text(encoding="utf-8-sig"))

    def rows(self, folder, name, delimiter="\t"):
        self.ref(folder, name)
        return _rows(self.base / folder / name, delimiter)

    def bootstrap(self):
        start = self.base / "START_HERE_r002" / "START_HERE_r002.tsv"
        if _digest(start) != START_SHA:
            raise IntakeError("START_HERE r002 changed; a new intake revision is required")
        entries = verify_manifest(self.root, start.parent, "SHA256SUMS_START_HERE_r002.txt", START_MANIFEST_SHA)
        self.verified.update(entries)
        self.packages.append({"id": "START_HERE", "revision": "r002", "dataset": "handoff index",
                              "repoPath": start.parent.relative_to(self.root).as_posix(),
                              "manifest": "SHA256SUMS_START_HERE_r002.txt", "manifestSha256": START_MANIFEST_SHA,
                              "sourceHash": START_MANIFEST_SHA, "authority": "frozen handoff index",
                              "verifiedFileCount": len(entries)})
        seen = set()
        for row in _rows(start):
            if not row["authoritative"].startswith("yes"):
                continue
            folder = _under(self.root, row["d_root"])
            manifest = row["manifest_file"].split(" (+")[0]
            identity = (str(folder), manifest, row["manifest_sha256"])
            if identity in seen:
                continue
            seen.add(identity)
            entries = verify_manifest(self.root, folder, manifest, row["manifest_sha256"])
            self.verified.update(entries)
            self.packages.append({"id": row["package_id"], "revision": row["revision"],
                                  "dataset": row["dataset"], "repoPath": folder.relative_to(self.root).as_posix(),
                                  "manifest": manifest, "manifestSha256": row["manifest_sha256"],
                                  "sourceHash": row["manifest_sha256"], "authority": row["authoritative"],
                                  "verifiedFileCount": len(entries)})

    def family(self, dataset, frame, project, category, review=None, evidence=None):
        key = f"{dataset}:{frame}"
        if key not in self.families:
            self.families[key] = {
                "id": key, "dataset": dataset, "frameID": frame, "project": project,
                "category": category, "versions": [], "original": None,
                "currentCandidate": None, "providerReview": review or {},
                "evidence": evidence or [], "humanAcceptance": None, "siteValidation": "not_performed",
            }
        return self.families[key]

    def local_path(self, paths, sha, required=True):
        checked = []
        for value in paths:
            if not _value(value):
                continue
            path = _under(self.root, value)
            checked.append(path.relative_to(self.root).as_posix())
            if not path.is_file():
                continue
            actual = self.hash_cache.setdefault(str(path), None)
            if actual is None:
                actual = self.hash_cache[str(path)] = _digest(path)
            if actual != sha:
                raise IntakeError(f"Media hash mismatch: {path}")
            return path.relative_to(self.root).as_posix()
        if required:
            raise IntakeError(f"Required delivered media missing: {sha} ({checked})")
        return None

    def version(self, family, sha, paths, filename, role, review=None, lineage=None,
                availability="available", evidence=None, required=True):
        if not sha or not SHA.fullmatch(sha):
            if availability != "declared_not_on_disk":
                raise IntakeError(f"Invalid media hash: {family['id']} {sha}")
            path, asset_id, matching = None, None, []
        else:
            if not paths and required:
                raise IntakeError(f"Delivered version has no explicit local path: {family['id']} {sha}")
            path = self.local_path(paths, sha, required) if paths else None
            matching = sorted(self.existing.get(sha, []), key=lambda a: (a.get("project") != family["project"], a["id"]))
            asset_id = matching[0]["id"] if matching else None
            if path and not asset_id:
                asset_id = self.new[sha]["id"] if sha in self.new else ("HD" if family["project"] == "hon" else "LAG") + "-INTAKE-" + sha[:20]
                if sha not in self.new:
                    kind = "video" if Path(filename).suffix.lower() in {".mp4", ".webm", ".mov"} else "image"
                    src = os.path.relpath(self.root / path, self.root / LIBRARY).replace("\\", "/")
                    self.new[sha] = {"id": asset_id, "project": family["project"], "src": src,
                                     "filename": Path(filename).name, "repoPath": path, "title": f"{family['frameID']} · {Path(filename).stem}",
                                     "category": "intake", "album": f"{family['project']}:intake-{family['dataset'].lower()}",
                                     "kind": kind, "sha256": sha, "tags": ["metadata-intake", family["dataset"]],
                                     "mimeType": mimetypes.guess_type(filename)[0], "bytes": (self.root / path).stat().st_size,
                                     "sourceStatus": "needs_review", "note": "Provider handoff candidate; human acceptance not inferred."}
                    if kind == "image":
                        self.new[sha]["thumb"] = src
            if not path:
                asset_id = None  # A stale catalog row never turns absent media into a delivered version.
        version = {"sha256": sha, "assetID": asset_id, "repoPath": path, "filename": Path(filename).name,
                   "role": role, "availability": availability if not path else "available",
                   "lineage": lineage or {"rootOriginalSha256": None, "baseSha256": None, "donorSha256s": None},
                   "providerReview": review or {}, "evidence": evidence or []}
        existing = next((v for v in family["versions"] if v["sha256"] == sha and sha), None)
        if existing:
            return existing
        family["versions"].append(version)
        if role in {"original", "version_only_base"}:
            family["original"] = {"sha256": sha, "assetID": asset_id}
        if asset_id:
            for identity in [a["id"] for a in matching] or [asset_id]:
                entry = self.metadata.setdefault(identity, {"familyIDs": [], "sha256": sha})
                if family["id"] not in entry["familyIDs"]:
                    entry["familyIDs"].append(family["id"])
        return version

    def candidate(self, family, sha, basis, eligible=True):
        if not _value(sha):
            return
        version = next((v for v in family["versions"] if v["sha256"] == sha), None)
        pointer = {"sha256": sha, "assetID": version["assetID"] if version else None,
                                      "basis": basis, "accepted": False,
                                      "availability": version["availability"] if version else "unresolved_pointer"}
        family["providerFinalPointer"] = pointer
        if eligible and version and version["availability"] == "available":
            family["currentCandidate"] = dict(pointer)

    def falcon(self):
        data = self.json(FALCON, "FALCON_EVIDENCE_v004.json")
        table = self.rows(FALCON, "FALCON_METADATA_v004.tsv")
        records = {r["frame_id"]: r for r in data["records"]}
        mapped = defaultdict(list)
        for row in self.rows(RESOLVER, "FALCON_D_PATH_MAP_r001.tsv"):
            mapped[row["frame_family"]].append(row)
        lineage = {r["repair_sha256"]: r for r in self.rows(RESOLVER, "LINEAGE_r001.tsv")}
        repairs = {r["sha256"]: r for r in data["repairs_index"]}
        for row in table:
            frame = row["frame_id"]
            source = records[frame]
            review = {"qaGrade": _value(row["provider_qa_grade"]), "qaScoreSuggestion": _value(row["qa_score_suggestion"]),
                      "qaBasis": _value(row["qa_score_suggestion_basis"]), "reason": _value(row["provider_qa_reason"]),
                      "likenessSelfScore": _value(row["provider_L_prelim"]), "sceneSelfScore": _value(row["provider_S_prelim"]),
                      "chestClass": _value(row["chest_class"]), "multiverseSuggestion": _value(row["multiverse_flag"]),
                      "duplicateGroup": _value(row["dup_group_id"]), "duplicateRole": _value(row["dup_role"]),
                      "stage": row["validation_status"], "technicalValidation": _value(row["technical_validation"]),
                      "components": source.get("components", {}), "pending": source.get("pending", []),
                      "referenceIDs": [x for x in row["reference_ids"].split(";") if x], "ruleVersions": row["rule_versions"],
                      "humanQuestion": _value(row["ziggy_open_question"]), "notes": _value(row["notes"])}
            review["scopedChecks"] = [
                {"reviewer": check.get("reviewer"), "scope": check.get("scope"), "outcome": check.get("outcome"),
                 "time": check.get("time"), "ruleVersion": check.get("rule_version"),
                 "targetSha256Recorded": check.get("target_sha256_recorded"),
                 "sourceFile": check.get("source_file"), "sourceRow": check.get("source_row")}
                for check in source.get("reviews", []) if check.get("team") == "V-Team"]
            family = self.family("GROK-HD-FALCON-1000", frame, "hon", row["category"], review,
                                 [self.ref(FALCON, "FALCON_EVIDENCE_v004.json", "records/" + frame)])
            for media in mapped[frame]:
                sha = media["sha256"]
                paths = []
                if media["resolution"] == "RESOLVED":
                    if media["resolver_media_path"]:
                        paths.append(f"{DROP}/{RESOLVER}/{media['resolver_media_path']}")
                    if media["d_path"]:
                        paths.append(media["d_path"])
                repair = repairs.get(sha, {})
                link = lineage.get(sha, {})
                vr = {"stage": repair.get("pass_state", "source original"), "verdict": repair.get("own_verdict"),
                      "scope": repair.get("requested_change"), "staleReason": repair.get("stale_reason"),
                      "remainingDefects": repair.get("remaining_defects"), "inheritsOriginalValidation": False,
                      "checks": [{"reviewer": v.get("reviewer"), "time": v.get("time"), "outcome": v.get("outcome"),
                                  "sourceFile": v.get("source_file"), "sourceRow": v.get("source_row"),
                                  "targetSha256Recorded": v.get("target_sha256_recorded")} for v in repair.get("verdicts", [])]}
                if not repair and sha == row["final_version_sha256"]:
                    vr = {"stage": row["final_version_pass_state"], "scope": row["final_version_scope"],
                          "technicalValidation": row["technical_validation"], "inheritsOriginalValidation": False}
                role = "original" if media["role"] == "original" else "version_only_base" if "base" in media["role"] else "repair"
                self.version(family, sha, paths, media["record_path"], role, vr if repair or sha == row["final_version_sha256"] else {},
                             {"rootOriginalSha256": _value(link.get("root_original_sha256")),
                              "baseSha256": _value(link.get("base_parent_sha256")),
                              "baseEvidence": _value(link.get("base_parent_basis")),
                              "baseConfidence": "recorded" if _value(link.get("base_parent_sha256")) else "unknown",
                              "donorSha256s": _hashes(link.get("donor_sha256s")) or None,
                              "donorEvidence": _value(link.get("donor_basis"))},
                             "deferred_history" if not paths else "available",
                             [self.ref(RESOLVER, "FALCON_D_PATH_MAP_r001.tsv", sha)], required=bool(paths))
            self.candidate(family, row["final_version_sha256"], "Provider final pointer; scoped status only",
                           row["final_version_pass_state"].lower() == "current pass (scoped)")
            self.dimensions(row["original_sha256"], row.get("width"), row.get("height"))
            if row["pilot_version_sha256"]:
                family["pilotCandidateSha256"] = row["pilot_version_sha256"]
        for group in data["duplicate_groups"]:
            self.duplicates.append({"id": group["group_id"], "dataset": "GROK-HD-FALCON-1000",
                                    "classification": group.get("classification"), "proposedKeeper": group.get("proposed_keeper"),
                                    "members": [{"sha256": m["sha256"], "suggestedKeeper": m.get("suggested_keeper") == "y"} for m in group["members"]],
                                    "decisionStatus": "provider_suggestion", "humanChoice": group.get("user_choice")})

    def lisan(self):
        data = self.json(LISAN, "LAG1K_REVIEW_EVIDENCE_r001.json")
        mapped = {r["sha256"]: r for r in self.rows(LISAN, "D_PATH_MAP_r001.tsv")}
        images = {r["image_id"]: r for r in data["images"]}
        corrected = {r["version_sha256"]: r for r in self.rows(CORRECTIONS, "LINEAGE_CORRECTIONS_r002.tsv")}
        repairs = defaultdict(list)
        for repair in data["repair_lineage"]:
            repairs[repair["original_id"]].append(repair)
        for row in self.rows(LISAN, "LAG1K_REVIEW_INDEX_r001.tsv"):
            frame, sha = row["image_id"], _value(row["sha256"])
            review = {"qaGrade": _value(row["raw_qa_grade"]), "qaScoreSuggestion": _value(row["prelim_qa_score_suggestion"]),
                      "likenessSelfScore": _value(row["prelim_likeness_self"]), "sceneSelfScore": _value(row["prelim_scene_self"]),
                      "stage": row["review_stage"], "technicalValidation": _value(row["technical_validation"]),
                      "duplicateGroup": _value(row["dup_group"]), "duplicateKeeperSuggestion": _value(row["dup_keeper"]),
                      "classSuggestion": _value(row["class"]), "notes": _value(row["notes"]),
                      "components": images[frame].get("components", {}), "openItemsOwner": _value(row["open_items_owner"])}
            family = self.family("LAG-1K", frame, "lisan", row["category"], review,
                                 [self.ref(LISAN, "LAG1K_REVIEW_EVIDENCE_r001.json", "images/" + frame)])
            self.lisan_version(family, mapped.get(sha), sha, row["rel_path"], "original", {}, {},
                               row["inventory_status"] == "DECLARED_NOT_ON_DISK")
            for repair in repairs[frame]:
                link = corrected[repair["sha256"]]
                donors = link["donor_sha256s"]
                self.lisan_version(family, mapped.get(repair["sha256"]), repair["sha256"], repair["rel_path"], "repair",
                                   {"stage": link["lineage_status"], "verdict": link["v_team_verdict"],
                                    "reviewer": "V_3", "authority": "V Team, claimed fix scope only",
                                    "scope": repair["requested_change"], "validationLabel": repair["validation_label"],
                                    "remainingDefects": repair.get("remaining_defects"), "inheritsOriginalValidation": False,
                                    "verdictSource": link["v_team_verdict_source"]},
                                   {"rootOriginalSha256": _value(link["root_original_sha256"]),
                                    "baseSha256": _value(link["base_sha256"]), "baseEvidence": link["base_source"],
                                    "donorSha256s": [] if donors == "NONE" else _hashes(donors) or None,
                                    "donorEvidence": link["donor_notes"], "donorConfidence": link["donor_confidence"],
                                    "baseConfidence": link["parent_confidence"], "parentConfidence": link["parent_confidence"],
                                    "confidence": link["parent_confidence"]})
            self.candidate(family, row["final_passed_version_sha256"], "Provider scoped passed version; not human acceptance")
            self.dimensions(sha, row.get("width"), row.get("height"))
        for group in data["duplicate_groups"]:
            self.duplicates.append({"id": group["group_id"], "dataset": "LAG-1K", "members": group["members"],
                                    "proposedKeeper": group.get("proposed_keeper"), "decisionStatus": "provider_suggestion"})

    def lisan_version(self, family, mapping, sha, filename, role, review, lineage, placeholder=False):
        paths = []
        if mapping:
            if _value(mapping["package_path"]):
                paths.append(f"{DROP}/{LISAN}/{mapping['package_path']}")
            paths += [p.strip() for p in re.split(r"\s*[|;]\s*", mapping["d_paths"]) if _value(p)]
        return self.version(family, sha, paths, filename, role, review, lineage,
                            "declared_not_on_disk" if placeholder else "unresolved", required=not placeholder,
                            evidence=[self.ref(LISAN, "D_PATH_MAP_r001.tsv", sha or family["frameID"])])

    def dimensions(self, sha, width, height):
        if sha in self.new and str(width).isdigit() and str(height).isdigit():
            self.new[sha].update(width=int(width), height=int(height))

    def vis_and_video(self):
        manifests = {}
        for folder, file in [(VIS, "01_VISEMES/MANIFEST.csv"), (CHIN, "MANIFEST.csv")]:
            for row in self.rows(folder, file, ","):
                manifests[row["sha256"]] = row
        vchecks = {r["file"]: r for r in self.rows(CORRECTIONS, "v_team/V3_LAG_chinfix_GAIB_20261021T152422Z_v003.tsv")}
        latest_names = set(vchecks)
        known_vis = {path: sha for path, sha in self.verified.items()
                     if path.startswith(f"{DROP}/{VIS}/") or path.startswith(f"{DROP}/{CHIN}/")}
        original_prefix = f"{DROP}/GROK-LAG-VIS-NATURAL-v001/01_VISEMES/"
        known_vis.update({path: a["sha256"] for path, a in self.existing_paths.items()
                          if path.startswith(original_prefix)})
        # The original VIS batch was already catalogued under content aliases.
        # Its immutable manifest reconnects the logged provider input filenames
        # to those existing hashes without treating a name match as identity.
        original_manifest = self.base / "GROK-LAG-VIS-NATURAL-v001/MANIFEST.csv"
        if _digest(original_manifest) != VIS_ORIGINAL_MANIFEST_SHA:
            raise IntakeError("Previously catalogued VIS source manifest changed")
        original_manifest_ref = {"repoPath": original_manifest.relative_to(self.root).as_posix(),
                                 "sha256": VIS_ORIGINAL_MANIFEST_SHA, "authority": "previously catalogued source dependency"}
        self.dependencies.append(original_manifest_ref)
        for row in _rows(original_manifest, ","):
            if row["file"].startswith("01_VISEMES/") and row["sha256"] in self.existing:
                known_vis[f"{DROP}/GROK-LAG-VIS-NATURAL-v001/" + row["file"]] = row["sha256"]
        for folder in [VIS, CHIN, VIDEO]:
            prefix = f"{DROP}/{folder}/"
            for path, sha in self.verified.items():
                if not path.startswith(prefix) or Path(path).suffix.lower() not in {".jpg", ".png", ".mp4"}:
                    continue
                name = Path(path).name
                if folder == VIDEO:
                    family = self.family("GROK-VIDEO-TEST", Path(name).stem, "hon", "Grok video tests",
                                         {"stage": "PRELIMINARY", "reviewer": "Chief", "scope": "provider comparison; no V-Team review or Ziggy acceptance"},
                                         [self.ref(VIDEO, "REVIEW_gorilla-clips_v001.md")])
                    self.version(family, sha, [path], name, "original", family["providerReview"])
                    self.candidate(family, sha, "Delivered comparison candidate")
                    continue
                stem = re.split(r"_v\d+", Path(name).stem)[0]
                family = self.family("LAG-VIS-NATURAL", stem, "lisan", "Mouth shapes and chin fixes")
                original_path = original_prefix + stem + ".jpg"
                if original_path in known_vis and not family["original"]:
                    original_sha = known_vis[original_path]
                    self.version(family, original_sha, [original_path], stem + ".jpg", "original",
                                 {"stage": "Existing source reference; no validation inherited"},
                                 evidence=[original_manifest_ref])
                source = manifests.get(sha, {})
                check = vchecks.get(name, {})
                input_text = source.get("refs", "")
                input_path = None
                if input_text.startswith("/workspace/lisan-al-gaib/"):
                    input_path = f"{DROP}/" + input_text.removeprefix("/workspace/lisan-al-gaib/")
                elif match := re.fullmatch(r"try\d+ output \(([^()]+)\)", input_text):
                    matches = [p for p in known_vis if Path(p).name == match.group(1)]
                    if len(matches) == 1:
                        input_path = matches[0]
                input_sha = known_vis.get(input_path)
                if input_sha:
                    self.local_path([input_path], input_sha)
                pixel_edit = source.get("prompt", "").startswith("PIXEL EDIT")
                review = {"stage": "V-Team scoped pass" if check.get("verdict") == "PASS" else "provider preliminary / superseded if later repair exists",
                          "verdict": check.get("verdict"), "scope": "chin GAIB fix only" if check else None,
                          "reviewer": "V_3" if check else None,
                          "likenessSelfScore": _value(source.get("L_likeness_1-5")),
                          "shapeSelfScore": _value(source.get("S_shape_distinct_1-5")),
                          "notes": _value(source.get("note")), "advisory": check.get("advisory"),
                          "remainingDefects": check.get("still_wrong"), "inheritsOriginalValidation": False}
                evidence = [self.ref(CORRECTIONS, "v_team/V3_LAG_chinfix_GAIB_20261021T152422Z_v003.tsv", name)] if check else []
                version = self.version(family, sha, [path], name, "comparison_sheet" if name.startswith("SHEET-") else "repair", review,
                                       {"rootOriginalSha256": family["original"]["sha256"] if family["original"] else None,
                                        "baseSha256": input_sha if pixel_edit else None, "donorSha256s": None,
                                        "referenceInputSha256": input_sha if not pixel_edit else None,
                                        "baseConfidence": "logged manifest input, exact hash resolved" if pixel_edit and input_sha else "unknown",
                                        "recordedInput": _value(input_text), "baseEvidence": check.get("base"),
                                        "note": "Manifest reference is an edit base only for explicitly logged pixel edits; generation references stay separate."}, evidence=evidence)
                if name in latest_names:
                    # Two GRIN bases are distinct branches; both remain visible as scoped pass options.
                    family.setdefault("scopedCandidateSha256s", []).append(sha)
                    if "try1" not in name:
                        self.candidate(family, sha, "r002 V_3 chin-scope pass; not whole-image acceptance")
                if name.startswith("SHEET-"):
                    family["kind"] = "comparison_sheet"
                    self.candidate(family, sha, "Delivered comparison sheet")
        # A known superseded version that is not shipped remains a metadata-only record.
        for update in self.rows(CORRECTIONS, "STATUS_UPDATES_r002.tsv"):
            if not update["item_id"].startswith("VIS-") or "SUPERSEDED" not in update["r002_value"]:
                continue
            stem = re.split(r"_v\d+", Path(update["item_id"]).stem)[0]
            family = self.family("LAG-VIS-NATURAL", stem, "lisan", "Mouth shapes and chin fixes")
            self.version(family, update["version_sha256"], [], update["item_id"], "repair",
                         {"stage": update["r002_value"], "notes": update["note"]},
                         availability="deferred_history", required=False,
                         evidence=[self.ref(CORRECTIONS, "STATUS_UPDATES_r002.tsv", update["item_id"])])

    def result(self):
        counts = {}
        for dataset in sorted({f["dataset"] for f in self.families.values()}):
            families = [f for f in self.families.values() if f["dataset"] == dataset]
            statuses = Counter(v["availability"] for f in families for v in f["versions"])
            counts[dataset] = {"families": len(families), "versions": sum(statuses.values()), **statuses}
        new_ids = {a["id"] for a in self.new.values()}
        return {"schemaVersion": "cfa-provider-review-intake-v1", "id": "pent-house-start-here-r002",
                "sourceIndex": {"repoPath": f"{DROP}/START_HERE_r002/START_HERE_r002.tsv", "sha256": START_SHA},
                "authorityNote": "Frozen source files may say PREPARING. Delivery READY is a separate handoff receipt. Scoped provider validation is not site validation or human acceptance.",
                "packages": self.packages, "families": list(self.families.values()),
                "sourceDependencies": self.dependencies,
                "duplicateGroups": self.duplicates, "assetMetadata": self.metadata,
                "newAssets": list(self.new.values()), "summary": {"datasets": counts, "newAssets": len(self.new),
                                                                        "matchedExistingAssets": sum(k not in new_ids for k in self.metadata)}}


def load_review_metadata_intake(repo_root, existing_assets):
    """Read pinned files, verify every delivered byte, return additive metadata.

    ``existing_assets`` is never mutated.  Unresolved historical versions and
    declared placeholders have no assetID and create no broken gallery tiles.
    Paths are repository-relative; exact file hashes bridge old/new drop folders.
    """
    intake = _Intake(repo_root, existing_assets)
    intake.bootstrap()
    intake.falcon()
    intake.lisan()
    intake.vis_and_video()
    return intake.result()

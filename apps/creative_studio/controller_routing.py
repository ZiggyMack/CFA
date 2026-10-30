"""Human-owned project routing; attribution is declared, never authentication."""
from copy import deepcopy
import json

DEFAULT_CONTROLLERS = {
    "ziggy": {"id": "ziggy", "name": "Ziggy", "homeLabel": "Ziggy’s Corner"},
    "baldadoon": {"id": "baldadoon", "name": "Baldadoon", "homeLabel": "Casa Baldadoon"},
}
ATTRIBUTION_FIELDS = {"humanReview", "reviewer", "reviewerControllerID", "projectControllerID",
                      "decisionAuthorityControllerID", "decisionScope"}
ASSISTANCE_FIELDS = {"note", "shotPlan", "creativeReview"}


def controllers(data):
    result = deepcopy(DEFAULT_CONTROLLERS)
    for row in data.get("humanControllers", data.get("controllers", [])):
        if isinstance(row, dict) and isinstance(row.get("id"), str) and isinstance(row.get("name"), str):
            result[row["id"]] = {**result.get(row["id"], {}), **row}
    return result


def project_controller(data, project):
    row = next((p for p in data.get("projects", []) if p.get("id") == project), {})
    return row.get("controllerID") or ("baldadoon" if project == "criminal_mind" else "ziggy")


def task_routing(data, task):
    owner = task.get("ownerControllerID") or project_controller(data, task.get("project"))
    return {"ownerControllerID": owner,
            "assigneeControllerID": task.get("assigneeControllerID") or owner,
            "decisionAuthorityControllerID": task.get("decisionAuthorityControllerID") or owner,
            "decisionScope": task.get("decisionScope") or "project_decision"}


def controller_tasks(data, tasks, controller, project=None):
    actionable, delegated = [], []
    for task in tasks:
        if project and task.get("project") != project:
            continue
        row = {**task, **task_routing(data, task)}
        if row["assigneeControllerID"] == controller:
            actionable.append(row)
        elif row["ownerControllerID"] == controller:
            delegated.append(row)
    return actionable, delegated


def task_contains_asset(task, asset):
    if task.get("project") != asset.get("project"):
        return False
    ids = set(task.get("previewAssetIDs", [])) | set(task.get("variantAssetIDs", []))
    for link in task.get("links", []):
        if isinstance(link, dict):
            ids.update(link.get("assetIDs", []))
            if link.get("assetID"):
                ids.add(link["assetID"])
    return asset.get("id") in ids


def human_action(data, asset, actor, scope, fields, updated_at, task=None):
    """Validate declared actor/scope for a new action without revising history."""
    people = controllers(data)
    owner = project_controller(data, asset.get("project"))
    if actor not in people or not isinstance(scope, str) or not scope.strip():
        raise ValueError("Choose who is recording this review and its decision scope first.")
    task = task if task and task_contains_asset(task, asset) else None
    route = task_routing(data, task) if task else {"ownerControllerID": owner,
        "assigneeControllerID": owner, "decisionAuthorityControllerID": owner, "decisionScope": scope}
    authority = route["decisionAuthorityControllerID"]
    delegated = bool(task and scope == route["decisionScope"])
    if actor != owner and not (delegated and (actor == authority or
            actor == route["assigneeControllerID"] and set(fields) <= ASSISTANCE_FIELDS)):
        raise ValueError("This action belongs to the project controller or an explicitly delegated decision scope. A help assignment does not grant creative approval.")
    record = {"reviewerControllerID": actor, "reviewer": people[actor]["name"],
        "projectControllerID": owner, "decisionAuthorityControllerID": authority if delegated else owner,
        "decisionScope": scope, "project": asset.get("project"), "assetID": asset.get("id"),
        "sha256": asset.get("sha256"), "updatedAt": updated_at, "fields": list(fields)}
    if task:
        record["taskID"] = task["id"]
    return {**{key: record[key] for key in ATTRIBUTION_FIELDS if key != "humanReview"}, "humanReview": record}


def normalize_human_attribution(value):
    result = {}
    for key in ATTRIBUTION_FIELDS - {"humanReview"}:
        if key in value:
            if value[key] is not None and (not isinstance(value[key], str) or len(value[key]) > 512):
                raise ValueError("Invalid human review attribution.")
            result[key] = value[key]
    if "humanReview" in value:
        row = value["humanReview"]
        if row is not None:
            if not isinstance(row, dict):
                raise ValueError("Human review attribution must be an object.")
            for key in ("reviewerControllerID", "reviewer", "projectControllerID", "decisionAuthorityControllerID",
                        "decisionScope", "project", "assetID", "sha256", "updatedAt", "taskID"):
                if key in row and row[key] is not None and (not isinstance(row[key], str) or len(row[key]) > 512):
                    raise ValueError("Invalid human review attribution field.")
            if "fields" in row and (not isinstance(row["fields"], list) or any(not isinstance(f, str) for f in row["fields"])):
                raise ValueError("Human review changed fields must be text identifiers.")
        result["humanReview"] = json.loads(json.dumps(row, allow_nan=False))
    return result


def apply_route(state, params, data):
    """Apply a changed deep link once; later reruns retain deliberate navigation."""
    project, view = params.get("project"), params.get("view")
    signature = (project, view)
    if state.get("studio_route_seen") == signature:
        return
    state["studio_route_seen"] = signature
    ids = {p["id"] for p in data.get("projects", [])}
    views = {"project_home": "Project home", "casa_baldadoon": "Casa Baldadoon", "mission_control": "Ziggy’s Corner"}
    ordinary = {"Library", "Working references", "Outfits", "Tattoos & piercings", "Supporting cast", "Storyboard",
                "Videos", "Comfy swap targets", "Archive", "Review queue", "Documents", "Shot plans", "Favorites & notes",
                "Export basket", "Intake verification", "Collaborators", "Collaborator briefs", "Inspiration"}
    if project in ids:
        state["studio_project"] = project
        row = next(p for p in data["projects"] if p["id"] == project)
        state["studio_view"] = views.get(view, view if view in ordinary else ("Project home" if row.get("landing") else "Library"))
        for key in ("studio_selected", "studio_mission_selected", "studio_mission_collection",
                    "studio_mission_questionnaire", "studio_mission_task_focus", "studio_human_task_context"):
            state.pop(key, None)

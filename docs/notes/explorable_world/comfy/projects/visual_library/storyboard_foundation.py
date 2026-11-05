"""Add derived source evidence without changing source selections or reviews."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def apply_source_foundation(catalog, root, previous=None, registry=None):
    root = Path(root)
    helper = root / 'apps/creative_studio/source_foundation.py'
    spec = importlib.util.spec_from_file_location('cfa_source_foundation_build', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry = registry or HERE / 'storyboard_input_bindings.json'
    raw = Path(registry).read_bytes()
    source = json.loads(raw)
    assert source['format'] == 'cfa-storyboard-input-bindings-v1'
    model = {'format': 'cfa-storyboard-source-foundation-v1', 'bindings': source['bindings']}
    rules = root / 'docs/notes/explorable_world/comfy/projects/collaborators/storyboard_skeleton_20261029/SOURCE_MATURITY_RULES_20261029.txt'
    model['rules'] = {'path': rules.relative_to(root).as_posix(), 'sha256': hashlib.sha256(rules.read_bytes()).hexdigest(), 'bytes': rules.stat().st_size}
    model['selectionSource'] = {'path': Path(registry).relative_to(root).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    resolved = list(model['bindings'])
    keys = {module.binding_key(b) for b in resolved}
    for story in catalog.get('storyboardStructure', {}).get('stories', []):
        for shot in story.get('shots', []):
            for b in module.selected_binding(model, shot, story['project'], story['storyID'], catalog.get('sceneReviews', [])):
                if module.binding_key(b) not in keys:
                    resolved.append(b)
                    keys.add(module.binding_key(b))
    model['checkpoints'] = module.checkpoint(resolved, catalog['assets'], previous)
    catalog['storyboardSourceFoundation'] = model
    return model

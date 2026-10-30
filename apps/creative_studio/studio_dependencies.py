"""Load each deployed Studio module version without stale process-wide imports."""

import hashlib
import builtins
import importlib.util
from pathlib import Path
import sys
from threading import RLock

APP_DIR = Path(__file__).resolve().parent
_REGISTRY_SOURCE = Path(__file__).read_bytes()
_MODULES = {"library_helpers", "mission_view", "design_view", "story_view", "review_intake_view", "source_foundation", "storyboard_takes", "collaborator_review", "collaborator_review_storage", "controller_routing", "project_intake_view"}
_LOAD_LOCK = RLock()


class _BoundRegistry:
    """Each source snapshot imports its own registry, not a shared mutable alias."""
    __name__ = "studio_dependencies"

    def __getattr__(self, name):
        if name == "__path__":
            raise AttributeError(name)
        if name in globals():
            return globals()[name]
        return getattr(current_module("library_helpers"), name)


_BOUND_REGISTRY = _BoundRegistry()


def _bound_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == "studio_dependencies" and level == 0:
        return _BOUND_REGISTRY
    return builtins.__import__(name, globals, locals, fromlist, level)


def current_module(name: str):
    """Reuse only an exact source version, without mutating an older session's module."""
    if name not in _MODULES:
        raise ValueError("Unknown Studio dependency")
    path = APP_DIR / (name + ".py")
    source = path.read_bytes()
    # Views import functions from this registry; a registry update must also
    # refresh otherwise unchanged children that captured the previous version.
    identity = str(path.resolve()).encode() + b"\0" + source + b"\0" + _REGISTRY_SOURCE
    if name in {"mission_view", "design_view", "story_view", "review_intake_view"}:
        identity += b"\0" + (APP_DIR / "library_helpers.py").read_bytes()
    if name == "story_view":
        identity += b"\0" + (APP_DIR / "source_foundation.py").read_bytes()
    if name in {"library_helpers", "story_view"}:
        identity += b"\0" + (APP_DIR / "storyboard_takes.py").read_bytes()
    if name in {"library_helpers", "mission_view"}:
        identity += b"\0" + (APP_DIR / "collaborator_review.py").read_bytes()
    if name in {"library_helpers", "mission_view", "project_intake_view"}:
        identity += b"\0" + (APP_DIR / "controller_routing.py").read_bytes()
    digest = hashlib.sha256(identity).hexdigest()
    key = "_cfa_studio_" + name + "_" + digest
    with _LOAD_LOCK:
        if key in sys.modules:
            return sys.modules[key]
        spec = importlib.util.spec_from_file_location(key, path)
        module = importlib.util.module_from_spec(spec)
        module.__dict__["__builtins__"] = {**vars(builtins), "__import__": _bound_import}
        # Execute the bytes we hashed. Timestamp-based bytecode can also be stale
        # during an in-place deployment; don't reload shared module dictionaries.
        exec(compile(source, str(path), "exec"), module.__dict__)
        sys.modules[key] = module
        return module


def __getattr__(name: str):
    return getattr(current_module("library_helpers"), name)

"""Load each deployed Studio module version without stale process-wide imports."""

import hashlib
import importlib.util
from pathlib import Path
import sys
from threading import RLock

APP_DIR = Path(__file__).resolve().parent
_MODULES = {"library_helpers", "mission_view"}
_LOAD_LOCK = RLock()


def current_module(name: str):
    """Reuse only an exact source version, without mutating an older session's module."""
    if name not in _MODULES:
        raise ValueError("Unknown Studio dependency")
    path = APP_DIR / (name + ".py")
    source = path.read_bytes()
    identity = str(path.resolve()).encode() + b"\0" + source
    if name == "mission_view":
        identity += b"\0" + (APP_DIR / "library_helpers.py").read_bytes()
    digest = hashlib.sha256(identity).hexdigest()
    key = "_cfa_studio_" + name + "_" + digest
    with _LOAD_LOCK:
        if key in sys.modules:
            return sys.modules[key]
        spec = importlib.util.spec_from_file_location(key, path)
        module = importlib.util.module_from_spec(spec)
        # Execute the bytes we hashed. Timestamp-based bytecode can also be stale
        # during an in-place deployment; don't reload shared module dictionaries.
        exec(compile(source, str(path), "exec"), module.__dict__)
        sys.modules[key] = module
        return module


def __getattr__(name: str):
    return getattr(current_module("library_helpers"), name)

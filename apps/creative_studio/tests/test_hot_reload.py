"""Current source bytes win over warm Python module and bytecode caches."""
import ast
import hashlib
import importlib.util
import os
from pathlib import Path
import py_compile
import sys
import tempfile
import unittest
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parents[1]


class StudioDependencyTest(unittest.TestCase):
    def setUp(self):
        cache = APP_DIR.parents[1] / ".cache"
        cache.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="studio-dependency-", dir=cache)
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        (self.directory / "storyboard_takes.py").write_text("VERSION = 1\n", encoding="utf-8")
        (self.directory / "collaborator_review.py").write_text("VERSION = 1\n", encoding="utf-8")
        (self.directory / "controller_routing.py").write_text("VERSION = 1\n", encoding="utf-8")
        spec = importlib.util.spec_from_file_location("studio_dependency_test_loader", APP_DIR / "studio_dependencies.py")
        self.loader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.loader)
        self.directory_patch = patch.object(self.loader, "APP_DIR", self.directory)
        self.directory_patch.start()
        self.addCleanup(self.directory_patch.stop)
        self.modules_before = set(sys.modules)
        self.addCleanup(self.remove_test_modules)

    def remove_test_modules(self):
        for name in set(sys.modules) - self.modules_before:
            filename = getattr(sys.modules.get(name), "__file__", None)
            if filename and Path(filename).is_relative_to(self.directory):
                sys.modules.pop(name, None)

    def test_same_size_same_timestamp_source_update_bypasses_stale_pyc(self):
        source = self.directory / "library_helpers.py"
        source.write_bytes(b"VALUE = 'first'\n")
        stamp = source.stat().st_mtime_ns
        py_compile.compile(str(source), doraise=True)
        first = self.loader.current_module("library_helpers")
        self.assertEqual(first.VALUE, "first")
        source.write_bytes(b"VALUE = 'later'\n")
        os.utime(source, ns=(stamp, stamp))
        second = self.loader.current_module("library_helpers")
        self.assertEqual(second.VALUE, "later")
        self.assertIsNot(first, second)
        self.assertIs(self.loader.current_module("library_helpers"), second)
        self.assertEqual(first.VALUE, "first")

    def test_same_content_in_different_paths_does_not_share_module_identity(self):
        source = self.directory / "library_helpers.py"
        source.write_text("VALUE = 7\n", encoding="utf-8")
        first = self.loader.current_module("library_helpers")
        other = self.directory / "other"
        other.mkdir()
        (other / source.name).write_bytes(source.read_bytes())
        (other / "storyboard_takes.py").write_bytes((self.directory / "storyboard_takes.py").read_bytes())
        (other / "collaborator_review.py").write_bytes((self.directory / "collaborator_review.py").read_bytes())
        (other / "controller_routing.py").write_bytes((self.directory / "controller_routing.py").read_bytes())
        with patch.object(self.loader, "APP_DIR", other):
            second = self.loader.current_module("library_helpers")
        self.assertIsNot(first, second)
        self.assertEqual(Path(first.__file__).parent, self.directory)
        self.assertEqual(Path(second.__file__).parent, other)

    def test_unchanged_view_gets_new_module_when_its_helper_changes(self):
        helper = self.directory / "library_helpers.py"
        helper.write_text("VALUE = 1\n", encoding="utf-8")
        view = self.directory / "mission_view.py"
        view.write_text("VIEW = 'unchanged'\n", encoding="utf-8")
        first = self.loader.current_module("mission_view")
        self.assertIs(first, self.loader.current_module("mission_view"))
        helper.write_text("VALUE = 2\n", encoding="utf-8")
        second = self.loader.current_module("mission_view")
        self.assertIsNot(first, second)
        self.assertEqual(first.VIEW, second.VIEW)

    def test_failed_import_does_not_cache_a_partially_initialized_module(self):
        source = self.directory / "library_helpers.py"
        source.write_text("VALUE = 3\nraise RuntimeError('incomplete')\n", encoding="utf-8")
        for _ in range(2):
            with self.assertRaisesRegex(RuntimeError, "incomplete"):
                self.loader.current_module("library_helpers")
        source.write_text("VALUE = 4\n", encoding="utf-8")
        self.assertEqual(self.loader.current_module("library_helpers").VALUE, 4)

    def test_story_view_identity_tracks_source_foundation_helper(self):
        (self.directory / 'library_helpers.py').write_text('VALUE = 1\n', encoding='utf-8')
        (self.directory / 'story_view.py').write_text("VIEW = 'unchanged'\n", encoding='utf-8')
        source = self.directory / 'source_foundation.py'
        source.write_text("LABEL = 'first'\n", encoding='utf-8')
        first_helper = self.loader.current_module('source_foundation')
        first_view = self.loader.current_module('story_view')
        self.assertIs(first_view, self.loader.current_module('story_view'))
        source.write_text("LABEL = 'later'\n", encoding='utf-8')
        second_helper = self.loader.current_module('source_foundation')
        second_view = self.loader.current_module('story_view')
        self.assertIsNot(first_helper, second_helper)
        self.assertIsNot(first_view, second_view)
        self.assertEqual(first_helper.LABEL, 'first')
        self.assertEqual(second_helper.LABEL, 'later')

    def test_unrelated_module_name_is_rejected(self):
        (self.directory / "unrelated.py").write_text("raise AssertionError('must not execute')", encoding="utf-8")
        with self.assertRaises((ValueError, ImportError)):
            self.loader.current_module("unrelated")

    def test_take_helper_update_refreshes_review_and_story_modules(self):
        (self.directory / "library_helpers.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.directory / "story_view.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.directory / "source_foundation.py").write_text("VALUE = 1\n", encoding="utf-8")
        before = {name: self.loader.current_module(name) for name in ("library_helpers", "story_view")}
        (self.directory / "storyboard_takes.py").write_text("VERSION = 2\n", encoding="utf-8")
        for name, module in before.items():
            self.assertIsNot(module, self.loader.current_module(name))

    def test_registry_bootstrap_refreshes_warm_alias_and_unchanged_children(self):
        tree = ast.parse((APP_DIR / "app.py").read_text(encoding="utf-8"))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                        and node.name == "_current_dependency_registry")
        namespace = {"APP_DIR": self.directory, "hashlib": hashlib,
                     "importlib": __import__("importlib"), "sys": sys}
        exec(compile(ast.Module(body=[function], type_ignores=[]), "app-bootstrap", "exec"), namespace)
        bootstrap = namespace["_current_dependency_registry"]
        registry = self.directory / "studio_dependencies.py"
        current_source = (APP_DIR / registry.name).read_text(encoding="utf-8")
        registry.write_text(current_source.replace('"collaborator_review_storage"', '"old_storage_placeholder_xx"'), encoding="utf-8")
        stamp = registry.stat().st_mtime_ns
        py_compile.compile(str(registry), doraise=True)
        (self.directory / "library_helpers.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.directory / "mission_view.py").write_text(
            "from studio_dependencies import current_module\n"
            "def storage(): return current_module('collaborator_review_storage').VALUE\n", encoding="utf-8")
        (self.directory / "collaborator_review_storage.py").write_text("VALUE = 9\n", encoding="utf-8")
        with patch.dict(sys.modules):
            old = bootstrap()
            old_view = old.current_module("mission_view")
            with self.assertRaisesRegex(ValueError, "Unknown Studio dependency"):
                old_view.storage()
            registry.write_text(current_source, encoding="utf-8")
            os.utime(registry, ns=(stamp, stamp))
            new = bootstrap()
            new_view = new.current_module("mission_view")
            self.assertIs(sys.modules["studio_dependencies"], new)
            self.assertIs(bootstrap(), new)
            self.assertIsNot(new, old)
            self.assertIsNot(new_view, old_view)
            self.assertEqual(new_view.storage(), 9)
            self.assertNotIn("collaborator_review_storage", old._MODULES)
            with self.assertRaisesRegex(ValueError, "Unknown Studio dependency"):
                old_view.storage()
            registry.write_text("raise RuntimeError('partial deployment')\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "partial deployment"):
                bootstrap()
            self.assertIs(sys.modules["studio_dependencies"], new)


if __name__ == "__main__":
    unittest.main()

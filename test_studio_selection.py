"""Run with: python3 -m unittest test_studio_selection.py"""
import ast
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest


class StudioSelectionTest(unittest.TestCase):
    def test_selected_files_are_passed_without_moving_originals(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                source = Path(__file__).parent / platform / "system/code/settings_gui.py"
                tree = ast.parse(source.read_text(encoding="utf-8"))
                cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "UnifiedDashboardApp")
                method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "browse_studio_slides")
                course = Path(tmp) / "course"
                external = Path(tmp) / "external.pdf"
                external.write_bytes(b"original")
                slides = course / "강의자료"
                slides.mkdir(parents=True)
                other = slides / "external.pdf"
                other.write_bytes(b"existing")
                selected = (str(external), str(other))
                calls = []
                def choose(**kwargs):
                    self.assertEqual(Path(kwargs["initialdir"]), slides)
                    return selected
                app = SimpleNamespace(
                    studio_course_combo=SimpleNamespace(get=lambda: "course"),
                    get_course_folder=lambda name: name,
                    ask_open_files_safe=choose,
                    refresh_studio_slides=lambda **kwargs: calls.append(kwargs),
                )
                namespace = {"os": os, "config_manager": SimpleNamespace(get_course_dir=lambda _: str(course))}
                exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)
                namespace["browse_studio_slides"](app)
                self.assertEqual(calls, [{"selected_paths": selected}])
                self.assertEqual(external.read_bytes(), b"original")
                self.assertEqual(other.read_bytes(), b"existing")

    def test_slide_cards_forward_mouse_wheel_to_the_canvas(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent / platform / "system/code/settings_gui.py").read_text(encoding="utf-8")
            self.assertIn("self._on_slide_wheel = _on_slide_wheel", source)
            self.assertIn("for widget in (card, chk, badge):", source)
            self.assertIn('widget.bind("<MouseWheel>", self._on_slide_wheel)', source)


if __name__ == "__main__":
    unittest.main()

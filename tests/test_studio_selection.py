"""Run with: python3 -m unittest test_studio_selection.py"""
import ast
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest


class StudioSelectionTest(unittest.TestCase):
    def test_picker_opens_in_course_folder_and_passes_selected_files(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                source = Path(__file__).parent.parent / platform / "system/code/settings_gui.py"
                tree = ast.parse(source.read_text(encoding="utf-8"))
                cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "UnifiedDashboardApp")
                method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "browse_studio_slides")
                course = Path(tmp) / "course"
                slides = course / "강의자료"
                selected = (str(slides / "week2.pdf"), str(slides / "week2.pptx"))
                calls = []
                app = SimpleNamespace(
                    studio_course_combo=SimpleNamespace(get=lambda: "course"),
                    get_course_folder=lambda name: name,
                    ask_open_files_safe=lambda **kwargs: calls.append(kwargs) or selected,
                    refresh_studio_slides=lambda **kwargs: calls.append(kwargs),
                )
                namespace = {"os": os, "config_manager": SimpleNamespace(get_course_dir=lambda _: str(course))}
                exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)
                namespace["browse_studio_slides"](app)
                self.assertTrue(slides.is_dir())
                self.assertEqual(Path(calls[0]["initialdir"]), slides)
                self.assertEqual(calls[1], {"selected_paths": selected})

    def test_slide_cards_forward_mouse_wheel_to_the_canvas(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent.parent / platform / "system/code/settings_gui.py").read_text(encoding="utf-8")
            self.assertIn("self._on_slide_wheel = _on_slide_wheel", source)
            self.assertIn("for widget in (card, chk, badge):", source)
            self.assertIn('widget.bind("<MouseWheel>", self._on_slide_wheel)', source)


if __name__ == "__main__":
    unittest.main()

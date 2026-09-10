import ast
import re
from pathlib import Path
import unittest


def load_score(platform):
    path = Path(__file__).parent.parent / platform / "system/code/config_manager.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "parse_model_version_score")
    ns = {"re": re}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), ns)
    return ns["parse_model_version_score"]


def load_model_picker(platform, supported_models):
    path = Path(__file__).parent.parent / platform / "system/code/config_manager.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    wanted_assignments = {
        "_SPECIALIZED_MODEL_MARKERS",
        "_MODEL_PROFILES",
        "DEFAULT_TUTOR_MODEL",
        "DEFAULT_LECTURE_NOTE_MODEL",
        "DEFAULT_ASSESSMENT_MODEL",
    }
    wanted_functions = {
        "_is_usable_flash_model",
        "parse_model_version_score",
        "get_gemini_models_for",
    }
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in wanted_assignments
            for target in node.targets
        ):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in wanted_functions:
            nodes.append(node)
    ns = {
        "os": __import__("os"),
        "re": re,
        "load_settings": lambda: {},
        "get_supported_gemini_models": lambda api_key=None: list(supported_models),
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), ns)
    return ns["get_gemini_models_for"]


class ModelRoutingTest(unittest.TestCase):
    def test_current_flash_models_outrank_alias_and_legacy_models(self):
        for platform in ("URY_macOS", "URY_Windows"):
            score = load_score(platform)
            with self.subTest(platform=platform):
                self.assertGreater(score("gemini-3.8-flash"), score("gemini-flash-latest"))
                self.assertGreater(score("gemini-3.7-flash"), score("gemini-2.5-flash"))
                self.assertLess(score("gemini-2.0-flash"), score("gemini-2.5-flash"))
                self.assertLess(score("gemini-1.5-flash"), score("gemini-2.5-flash"))

    def test_each_feature_uses_a_separate_model_profile(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            config = (root / platform / "system/code/config_manager.py").read_text(encoding="utf-8")
            tutor = (root / platform / "system/code/lecture_tutor.py").read_text(encoding="utf-8")
            studio = (root / platform / "system/code/process_all_lectures.py").read_text(encoding="utf-8")
            exam = (root / platform / "system/code/generate_mock_exams.py").read_text(encoding="utf-8")
            bible = (root / platform / "system/code/generate_master_bible.py").read_text(encoding="utf-8")
            with self.subTest(platform=platform):
                self.assertIn('"tutor": {', config)
                self.assertIn('"lecture_note": {', config)
                self.assertIn('"assessment": {', config)
                self.assertIn('get_gemini_models_for("tutor", api_key, max_models=3)', tutor)
                self.assertIn('get_gemini_models_for("lecture_note", api_key, max_models=3)', studio)
                self.assertIn('model_picker("assessment"', exam)
                self.assertIn('get_gemini_models_for("assessment", api_key, max_models=3)', bible)
                self.assertIn('e.code in (429, 503)', bible)

    def test_api_model_list_automatically_prioritizes_newer_models(self):
        supported = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.8-flash",
            "gemini-3.9-flash",
            "gemini-2.5-flash",
        ]
        for platform in ("URY_macOS", "URY_Windows"):
            picker = load_model_picker(platform, supported)
            with self.subTest(platform=platform):
                self.assertEqual(
                    picker("lecture_note", "test-key", max_models=3),
                    ["gemini-3.9-flash", "gemini-3.8-flash", "gemini-3.5-flash"],
                )
                self.assertEqual(
                    picker("tutor", "test-key", max_models=3),
                    [
                        "gemini-3.5-flash-lite",
                        "gemini-3.1-flash-lite",
                        "gemini-2.5-flash-lite",
                    ],
                )

    def test_gemini_3_flash_preview_is_documented_as_available_fallback(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            config = (root / platform / "system/code/config_manager.py").read_text(encoding="utf-8")
            with self.subTest(platform=platform):
                self.assertIn('"gemini-3-flash-preview"', config)


if __name__ == "__main__":
    unittest.main()

import ast
from pathlib import Path
import unittest


class ThemeSettingsTest(unittest.TestCase):
    def test_theme_uses_saved_hex_and_has_settings_controls(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent / platform / "system/code/settings_gui.py"
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            app = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                       and n.name == "UnifiedDashboardApp")
            methods = {n.name: ast.get_source_segment(source, n) for n in app.body
                       if isinstance(n, ast.FunctionDef)}
            self.assertIn('re.fullmatch(r"#[0-9a-fA-F]{6}"', methods["set_theme_accent"])
            self.assertIn('getattr(self, "theme_accent"', methods["setup_styles"])
            self.assertIn("대학별 테마", methods["build_settings_tab"])
            self.assertIn("theme_hex_var", methods["build_settings_tab"])
            self.assertIn("self.apply_theme_icon()", methods["set_theme_accent"])
            self.assertIn("def apply_theme_icon", source)


if __name__ == "__main__":
    unittest.main()

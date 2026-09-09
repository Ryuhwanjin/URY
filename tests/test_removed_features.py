import ast
from pathlib import Path
import unittest


class RemovedFeaturesTest(unittest.TestCase):
    def test_dashboard_and_advanced_methods_are_gone(self):
        removed = {"build_dashboard_tab", "refresh_dashboard", "build_advanced_tab",
                   "sync_markdown_vault_action", "save_current_prompt"}
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform / "system/code/settings_gui.py"
            tree = ast.parse(path.read_text(encoding="utf-8"))
            app = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                       and n.name == "UnifiedDashboardApp")
            methods = {n.name for n in app.body if isinstance(n, ast.FunctionDef)}
            self.assertFalse(removed & methods)
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("dash_course_combo", source)

    def test_workspace_is_not_rejected_just_because_it_is_in_documents(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent.parent / platform / "system/code" / "config_manager.py").read_text(encoding="utf-8")
            root_fn = source[source.index("def get_root_workspace"):source.index("\nSCRIPT_DIR =")]
            self.assertNotIn('"Documents" not in env_ws', root_fn)

    def test_windows_builder_bundles_runtime_loaded_modules(self):
        source = (Path(__file__).parent.parent / "URY_Windows/system/code/build_exe_gui.py").read_text(encoding="utf-8")
        for module in ("process_all_lectures", "lecture_tutor", "generate_pdfs", "update_checker"):
            self.assertIn(f'"{module}"', source)
        self.assertIn('"--hidden-import", module', source)

    def test_unused_cross_platform_and_advanced_modules_are_deleted(self):
        for platform in ("URY_macOS", "URY_Windows"):
            code_dir = Path(__file__).parent.parent / platform / "system/code"
            self.assertFalse((code_dir / "dynamic_slide_integrator.py").exists())
            self.assertFalse((code_dir / "sync_markdown_vault.py").exists())
        mac_code = Path(__file__).parent.parent / "URY_macOS/system/code"
        self.assertFalse((mac_code / "build_exe_gui.py").exists())
        self.assertFalse((mac_code / "test_win_environment.py").exists())


if __name__ == "__main__":
    unittest.main()

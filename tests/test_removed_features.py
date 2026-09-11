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
            self.assertIn('os.path.expanduser("~/Desktop/URY")', root_fn)
            self.assertNotIn('os.path.expanduser("~/Desktop/URY_Engine")', root_fn)

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

    def test_windows_batch_launchers_use_utf8_and_current_version(self):
        win_dir = Path(__file__).parent.parent / "URY_Windows"
        for path in win_dir.glob("*.bat"):
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertTrue(source.startswith("@echo off\n@chcp 65001 >nul\n"))
                self.assertNotIn("v0.6.5", source)
                self.assertNotIn("v0.7.7", source)

    def test_windows_uninstaller_does_not_delete_workspace_without_python(self):
        path = Path(__file__).parent.parent / "URY_Windows/04_완전삭제.bat"
        source = path.read_text(encoding="utf-8")
        no_python = source.split(":NO_PY", 1)[1]
        no_python = no_python.split("exit /b 1", 1)[0]
        self.assertNotIn("rmdir /s /q", no_python.lower())
        self.assertIn("No user data was deleted.", no_python)

    def test_windows_builder_checks_pyinstaller_exit_code(self):
        path = Path(__file__).parent.parent / "URY_Windows/system/code/build_exe_gui.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("if res.returncode != 0:", source)
        self.assertIn("PyInstaller 컴파일 실패", source)

    def test_frozen_resource_resolution_is_shared(self):
        root = Path(__file__).parent.parent
        sources = []
        for platform in ("URY_macOS", "URY_Windows"):
            source = (root / platform / "system/code/config_manager.py").read_text(encoding="utf-8")
            sources.append(source)
            self.assertIn('getattr(sys, "_MEIPASS", "")', source)
            self.assertIn('os.path.join(app_dir, "_internal", "system")', source)
            self.assertIn("def find_resource_dir(dirname):", source)
        self.assertEqual(sources[0], sources[1])

    def test_prompt_consumers_use_shared_resource_resolver(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            for name in ("settings_gui.py", "process_all_lectures.py", "generate_mock_exams.py"):
                source = (root / platform / "system/code" / name).read_text(encoding="utf-8")
                self.assertIn('config_manager.find_resource_dir("prompts")', source)

    def test_windows_ci_builds_on_windows_and_uploads_artifact_only(self):
        path = Path(__file__).parent.parent / ".github/workflows/windows-build.yml"
        source = path.read_text(encoding="utf-8")
        self.assertIn("runs-on: windows-latest", source)
        self.assertIn("--onedir", source)
        self.assertIn("--icon URY_Windows/app_icon.ico", source)
        self.assertIn('강의노트_한국어_프롬프트.txt', source)
        self.assertIn("actions/upload-artifact@v4", source)
        self.assertNotIn("action-gh-release", source)

    def test_windows_inno_setup_preserves_user_workspace(self):
        root = Path(__file__).parent.parent
        script = (root / "installer/URY_v0.9.6.iss").read_text(encoding="utf-8")
        self.assertIn("PrivilegesRequired=lowest", script)
        self.assertIn("DefaultDirName={localappdata}\\Programs\\URY", script)
        self.assertIn("Source: \"..\\dist\\URY\\*\"", script)
        self.assertIn("Type: filesandordirs; Name: \"{app}\"", script)
        self.assertEqual(script.count("Type: filesandordirs;"), 1)
        workflow = (root / ".github/workflows/windows-build.yml").read_text(encoding="utf-8")
        self.assertIn("Inno Setup 6\\ISCC.exe", workflow)
        self.assertIn("URY_Windows_v0.9.6_setup", workflow)


if __name__ == "__main__":
    unittest.main()

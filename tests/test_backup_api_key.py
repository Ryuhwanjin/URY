from pathlib import Path
import ast
import io
import json
import os
import tempfile
import unittest
import urllib.error
import urllib.request
from unittest.mock import patch


class BackupApiKeyTest(unittest.TestCase):
    def test_get_api_keys_preserves_primary_then_backup_order(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform / "system/code/config_manager.py"
            tree = ast.parse(path.read_text(encoding="utf-8"))
            wanted = {"_read_env_file_key", "_configured_api_key", "get_api_keys"}
            nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
            with tempfile.TemporaryDirectory() as tmp:
                namespace = {
                    "os": os,
                    "ENV_PATH": str(Path(tmp) / ".env"),
                    "load_settings": lambda: {
                        "gemini_api_key": "primary-from-settings",
                        "gemini_backup_api_key": "backup-from-settings",
                    },
                }
                exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
                with patch.dict(os.environ, {}, clear=True):
                    with self.subTest(platform=platform, source="settings"):
                        self.assertEqual(namespace["get_api_keys"](), ["primary-from-settings", "backup-from-settings"])
                with patch.dict(os.environ, {
                    "GEMINI_API_KEY": "primary-from-env",
                    "GEMINI_BACKUP_API_KEY": "primary-from-env",
                }, clear=True):
                    with self.subTest(platform=platform, source="environment"):
                        self.assertEqual(namespace["get_api_keys"](), ["primary-from-settings", "backup-from-settings"])
                with patch.dict(os.environ, {
                    "GEMINI_API_KEY": "stale-environment-key",
                }, clear=True):
                    with self.subTest(platform=platform, source="stale-environment"):
                        self.assertEqual(
                            namespace["get_api_keys"](),
                            ["primary-from-settings", "backup-from-settings"],
                        )

    def test_api_key_badge_uses_real_model_list_validation(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            config_path = root / platform / "system/code/config_manager.py"
            config_tree = ast.parse(config_path.read_text(encoding="utf-8"))
            check_node = next(
                node for node in config_tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "check_api_key"
            )
            namespace = {
                "json": json,
                "urllib": urllib,
                "get_api_key": lambda: "",
            }
            exec(compile(ast.Module(body=[check_node], type_ignores=[]), str(config_path), "exec"), namespace)

            class Response:
                def __enter__(self):
                    return self

                def __exit__(self, *_):
                    return False

                def read(self):
                    return json.dumps({
                        "models": [{"supportedGenerationMethods": ["generateContent"]}]
                    }).encode("utf-8")

            with patch("urllib.request.urlopen", return_value=Response()):
                with self.subTest(platform=platform, result="valid"):
                    self.assertEqual(namespace["check_api_key"]("valid-key-123"), "valid")
            with patch(
                "urllib.request.urlopen",
                side_effect=urllib.error.HTTPError("https://example.com", 400, "invalid", {}, None),
            ):
                with self.subTest(platform=platform, result="invalid"):
                    self.assertEqual(namespace["check_api_key"]("invalid-key"), "invalid")
            with patch(
                "urllib.request.urlopen",
                side_effect=urllib.error.URLError("offline"),
            ):
                with self.subTest(platform=platform, result="unavailable"):
                    self.assertEqual(namespace["check_api_key"]("network-key"), "unavailable")

            settings_source = (root / platform / "system/code/settings_gui.py").read_text(encoding="utf-8")
            with self.subTest(platform=platform, result="badge"):
                self.assertIn("check_api_key", settings_source)
                self.assertIn("API 키 인증 실패", settings_source)
                self.assertIn("API 확인 중", settings_source)

    def test_backup_key_is_synced_across_platforms_and_consumers(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            code = root / platform / "system/code"
            config = (code / "config_manager.py").read_text(encoding="utf-8")
            settings = (code / "settings_gui.py").read_text(encoding="utf-8")
            studio = (code / "process_all_lectures.py").read_text(encoding="utf-8")
            tutor = (code / "lecture_tutor.py").read_text(encoding="utf-8")
            exam = (code / "generate_mock_exams.py").read_text(encoding="utf-8")
            bible = (code / "generate_master_bible.py").read_text(encoding="utf-8")
            with self.subTest(platform=platform):
                self.assertIn('"gemini_backup_api_key"', config)
                self.assertIn('"GEMINI_BACKUP_API_KEY"', config)
                self.assertIn("def get_api_keys()", config)
                self.assertIn("backup_api_key_var", settings)
                self.assertIn("get_api_keys", studio)
                self.assertIn("get_api_keys", tutor)
                self.assertIn("get_api_keys", exam)
                self.assertIn("get_api_keys", bible)
                self.assertIn("api_key=api_key", studio)

    def test_text_generation_moves_to_backup_key_after_quota_error(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            path = root / platform / "system/code/generate_mock_exams.py"
            tree = ast.parse(path.read_text(encoding="utf-8"))
            node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "call_gemini")
            namespace = {
                "os": os,
                "json": json,
                "urllib": urllib,
                "time": type("Time", (), {"sleep": staticmethod(lambda _: None)}),
                "config_manager": type("Config", (), {
                    "get_api_keys": staticmethod(lambda: ["primary-key", "backup-key"]),
                    "get_gemini_models_for": staticmethod(lambda purpose, api_key, max_models=3: ["gemini-3.5-flash"]),
                    "get_supported_gemini_models": staticmethod(lambda api_key: ["gemini-3.5-flash"]),
                }),
                "print": lambda *args: None,
            }
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), namespace)
            quota_error = urllib.error.HTTPError("https://example.com", 429, "quota", {}, None)
            response = io.BytesIO(json.dumps({"candidates": [{"content": {"parts": [{"text": "backup answer"}]}}]}).encode())
            requests = []
            # A deterministic iterator is easier to inspect than a real network call.
            results = iter([quota_error, response])
            def deterministic_urlopen(request, **kwargs):
                requests.append(request.full_url)
                result = next(results)
                if isinstance(result, Exception):
                    raise result
                return result
            with patch("urllib.request.urlopen", side_effect=deterministic_urlopen):
                with self.subTest(platform=platform):
                    self.assertEqual(namespace["call_gemini"]("prompt"), "backup answer")
            self.assertEqual(len(requests), 2)
            self.assertIn("key=primary-key", requests[0])
            self.assertIn("key=backup-key", requests[1])


if __name__ == "__main__":
    unittest.main()

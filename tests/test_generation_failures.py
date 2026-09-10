import ast
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
import urllib.request
import urllib.error
from unittest.mock import patch


def function(platform, filename, name, namespace):
    path = Path(__file__).parent.parent / platform / "system/code" / filename
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), namespace)
    return namespace[name]


class GenerationFailureTest(unittest.TestCase):
    def test_studio_quota_or_server_error_advances_model_before_backup_key(self):
        root = Path(__file__).parent.parent
        for platform in ("URY_macOS", "URY_Windows"):
            source = (root / platform / "system/code/process_all_lectures.py").read_text(encoding="utf-8")
            start = source.index("    def call_gemini_with_parts(")
            end = source.index("\n    # 프롬프트 구성", start)
            call_source = source[start:end]
            with self.subTest(platform=platform):
                self.assertIn("if e.code in (429, 503):", call_source)
                self.assertIn("다음 모델로 즉시 전환합니다", call_source)
                self.assertNotIn(
                    "if e.code in (429, 503):\n                        log(f\"  ⚠️ [{model}] HTTP {e.code} 할당량/서버 제한 감지 -> 다음 모델로 즉시 전환합니다. ({err_body})\", step=2)\n                        break",
                    call_source,
                )

    def test_failure_never_returns_sample_and_fallback_does_not_sleep(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform):
                ns = {"os": os, "json": json, "urllib": urllib,
                      "print": lambda *args: None,
                      "time": SimpleNamespace(sleep=lambda _: self.fail("Unexpected retry delay")),
                      "config_manager": SimpleNamespace(
                          load_settings=lambda: {"gemini_api_key": "test-key-only"},
                          get_supported_gemini_models=lambda _: ["first", "second"])}
                call = function(platform, "generate_mock_exams.py", "call_gemini", ns)
                error = urllib.error.HTTPError("https://example.com", 429, "quota", {}, None)
                response = io.BytesIO(json.dumps({"candidates": [{"content": {"parts": [{"text": "real answer"}]}}]}).encode())
                with patch("urllib.request.urlopen", side_effect=[error, response]) as request:
                    self.assertEqual(call("prompt"), "real answer")
                    self.assertEqual(request.call_count, 2)
                with patch("urllib.request.urlopen", side_effect=error):
                    with self.assertRaises(RuntimeError):
                        call("prompt")
                with patch("urllib.request.urlopen", side_effect=lambda *a, **kw: io.BytesIO(b'{"candidates": []}')):
                    with self.assertRaises(RuntimeError):
                        call("prompt")

    def test_empty_note_rejected_before_any_file_operations(self):
        for platform in ("URY_macOS", "URY_Windows"):
            save = function(platform, "process_all_lectures.py", "save_lecture_note_files", {})
            for content in ("", "   ", None):
                with self.subTest(platform=platform, content=content), self.assertRaises(RuntimeError):
                    save(content, "2027-03-08", 2)


if __name__ == "__main__":
    unittest.main()

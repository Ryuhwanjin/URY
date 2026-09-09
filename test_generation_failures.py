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
    path = Path(__file__).parent / platform / "system/code" / filename
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), namespace)
    return namespace[name]


class GenerationFailureTest(unittest.TestCase):
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

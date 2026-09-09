import ast
import io
import json
from pathlib import Path
import unittest
import urllib
from unittest.mock import patch


class StreamResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def load_stream_function(platform):
    path = Path(__file__).parent.parent / platform / "system/code/process_all_lectures.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "stream_gemini_response")
    namespace = {"json": json, "urllib": urllib}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), namespace)
    return namespace["stream_gemini_response"], path.read_text(encoding="utf-8")


class LectureStreamingTest(unittest.TestCase):
    def test_sse_chunks_are_joined_and_usage_is_returned(self):
        events = (
            b'data: {"candidates":[{"content":{"parts":[{"text":"hello "}]}}]}\n\n',
            b'data: {"candidates":[{"content":{"parts":[{"text":"world"}]}}],'
            b'"usageMetadata":{"promptTokenCount":10,"candidatesTokenCount":2,"totalTokenCount":12}}\n\n'
        )
        for platform in ("URY_macOS", "URY_Windows"):
            stream, source = load_stream_function(platform)
            progress = []
            with self.subTest(platform=platform), patch("urllib.request.urlopen", return_value=StreamResponse(b"".join(events))):
                text, usage = stream(object(), progress_fn=progress.append)
                self.assertEqual(text, "hello world")
                self.assertEqual(usage["totalTokenCount"], 12)
                self.assertEqual(progress[-1], 11)
            custom = source[source.index("def generate_custom_lecture_note("):]
            self.assertIn(":streamGenerateContent?alt=sse", custom)
            self.assertIn('"maxOutputTokens": 8192', custom)


if __name__ == "__main__":
    unittest.main()

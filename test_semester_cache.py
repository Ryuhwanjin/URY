import ast
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


class SemesterCacheTest(unittest.TestCase):
    def test_same_course_is_isolated_and_original_notes_survive(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                source = Path(__file__).parent / platform / "system/code/config_manager.py"
                tree = ast.parse(source.read_text(encoding="utf-8"))
                fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "get_markdown_cache_dir")
                semester = ["2026년 2학기"]
                ns = {"os": os, "WORKSPACE_DIR": tmp, "get_current_semester": lambda: semester[0]}
                exec(compile(ast.Module(body=[fn], type_ignores=[]), str(source), "exec"), ns)
                old_note = Path(tmp) / semester[0] / "공통과목/강의노트/1주차/.note.md"
                old_note.parent.mkdir(parents=True)
                old_note.write_text("old semester", encoding="utf-8")
                resolve = ns["get_markdown_cache_dir"]
                old_cache = Path(resolve("공통과목"))
                self.assertEqual((old_cache / "note.md").read_text(), "old semester")
                semester[0] = "2027년 1학기"
                new_cache = Path(resolve("공통과목"))
                self.assertNotEqual(old_cache, new_cache)
                self.assertFalse((new_cache / "note.md").exists())
                self.assertTrue(old_note.exists())
                semester[0] = "2026년 2학기"
                (old_cache / "note.md").write_text("updated")
                resolve("공통과목")
                self.assertEqual((old_cache / "note.md").read_text(), "updated")


if __name__ == "__main__":
    unittest.main()

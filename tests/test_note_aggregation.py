import ast
import os
import re
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path


def load_save_functions(platform):
    path = Path(__file__).parent.parent / platform / "system/code/process_all_lectures.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    wanted = {"_replace_note_section", "append_to_single_note_file", "save_lecture_note_files"}
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in wanted]
    namespace = {
        "os": os,
        "sys": types.SimpleNamespace(platform="darwin"),
        "subprocess": subprocess,
        "re": re,
        "get_default_config": lambda: {},
        "hide_file_os_agnostic": lambda path: path,
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


class NoteAggregationTest(unittest.TestCase):
    def test_studio_session_updates_week_and_combined_notes(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                course_dir = root / "DB"
                cache_dir = root / ".markdown_cache" / "DB"
                course_dir.mkdir(parents=True)
                cache_dir.mkdir(parents=True)

                class ConfigManager:
                    def get_markdown_cache_dir(self, _folder):
                        return str(cache_dir)

                namespace = load_save_functions(platform)
                namespace["config_manager"] = ConfigManager()
                namespace["resolve_course_dir"] = lambda _folder: str(course_dir)
                config = {
                    "folder_name": "DB",
                    "name": "DB",
                    "en_name": "Database",
                    "cname_prefix": "DB",
                    "en_prefix": "Database",
                    "prof": "담당 교수님",
                }
                def note(date, body):
                    return (
                        f"# DB 1주차 맞춤 강의노트 ({date})\n"
                        f"> 📌 **수업 일자**: {date}\n\n"
                        "## 📌 1.\n## 💡 2.\n## 🎯 3.\n## 📝 4.\n"
                        + body
                    )

                save = namespace["save_lecture_note_files"]
                save(note("2026-09-01", "FIRST"), "2026-09-01", 1, config=config, session_only=True)
                save(note("2026-09-03", "SECOND"), "2026-09-03", 1, config=config, session_only=True)

                week_path = course_dir / "강의노트" / "1주차" / ".DB_1주차_강의노트.md"
                combined_path = course_dir / "강의노트" / "통합" / ".DB_통합강의노트.md"
                self.assertTrue(week_path.exists())
                self.assertTrue(combined_path.exists())
                self.assertIn("FIRST", week_path.read_text(encoding="utf-8"))
                self.assertIn("SECOND", week_path.read_text(encoding="utf-8"))
                self.assertIn("FIRST", combined_path.read_text(encoding="utf-8"))
                self.assertIn("SECOND", combined_path.read_text(encoding="utf-8"))

                save(note("2026-09-01", "REPLACED"), "2026-09-01", 1, config=config, session_only=True)
                updated = week_path.read_text(encoding="utf-8")
                self.assertNotIn("FIRST", updated)
                self.assertIn("REPLACED", updated)
                self.assertEqual(updated.count("REPLACED"), 1)

    def test_short_stream_response_is_not_accepted_as_a_note(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform / "system/code/process_all_lectures.py"
            tree = ast.parse(path.read_text(encoding="utf-8"))
            node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_is_complete_lecture_note")
            namespace = {}
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec"), namespace)
            self.assertFalse(namespace["_is_complete_lecture_note"]("# partial"))
            complete = "\n".join(("## 📌 1.", "## 💡 2.", "## 🎯 3.", "## 📝 4.")) + "\n" + ("x" * 1200)
            self.assertTrue(namespace["_is_complete_lecture_note"](complete))


if __name__ == "__main__":
    unittest.main()

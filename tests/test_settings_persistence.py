import ast
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest


class SettingsPersistenceTest(unittest.TestCase):
    def test_active_edits_survive_reload_without_changing_other_semester(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                path = Path(__file__).parent.parent / platform / "system/code/config_manager.py"
                tree = ast.parse(path.read_text(encoding="utf-8"))
                functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                             and n.name in ("load_settings", "save_settings")]
                ns = {
                    "os": os, "json": json, "sys": SimpleNamespace(platform="linux"),
                    "WORKSPACE_DIR": tmp, "SETTINGS_PATH": os.path.join(tmp, "settings.json"),
                    "ENV_PATH": os.path.join(tmp, ".env"), "TIMETABLE_PATH": os.path.join(tmp, "timetable.json"),
                    "DEFAULT_SETTINGS_PATH": os.path.join(tmp, "missing.json"),
                    "ensure_all_course_folders": lambda _: None,
                    "sync_timetable_from_settings": lambda _: None,
                }
                exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), "exec"), ns)
                other = [{"course_name": "다른 학기 과목", "tutor_name": "유지"}]
                data = {
                    "semester": "2027년 1학기", "semester_start_date": "2027-03-08",
                    "semester_end_date": "2027-06-25",
                    "courses": [{"course_name": "공통과목", "tutor_name": "새 이름",
                                 "syllabus_paths": ["강의계획서/new.pdf"]}],
                    "semester_courses": {"2026년 2학기": other, "2027년 1학기": []},
                }
                ns["save_settings"](data)
                loaded = ns["load_settings"]()
                self.assertEqual(loaded["semester_courses"]["2027년 1학기"], data["courses"])
                self.assertEqual(loaded["semester_courses"]["2026년 2학기"], other)
                self.assertEqual(loaded["semester_periods"]["2027년 1학기"]["start"], "2027-03-08")
                loaded["courses"][0]["tutor_name"] = "다시 변경"
                ns["save_settings"](loaded)
                self.assertEqual(ns["load_settings"]()["semester_courses"]["2027년 1학기"][0]["tutor_name"], "다시 변경")


if __name__ == "__main__":
    unittest.main()

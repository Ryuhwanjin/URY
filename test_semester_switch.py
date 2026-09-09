"""Headless regression: python3 -B -m unittest test_semester_switch.py"""
import ast
import copy
from datetime import date
from pathlib import Path
from types import SimpleNamespace
import unittest


class Value:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class SemesterSwitchTest(unittest.TestCase):
    def test_round_trip_restores_courses_and_dates(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform):
                path = Path(__file__).parent / platform / "system/code/settings_gui.py"
                tree = ast.parse(path.read_text(encoding="utf-8"))
                cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "UnifiedDashboardApp")
                method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "on_semester_changed")
                saved = []
                namespace = {
                    "config_manager": SimpleNamespace(
                        get_semester_period=lambda _: (date(2027, 3, 2), date(2027, 6, 21), ""),
                        save_settings=lambda settings: saved.append(copy.deepcopy(settings))),
                    "tk": SimpleNamespace(DISABLED="disabled"),
                    "messagebox": SimpleNamespace(showwarning=lambda *args: None),
                }
                exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
                switch = namespace["on_semester_changed"]
                app = SimpleNamespace(
                    settings={"semester": "2026년 2학기"},
                    semester_var=Value("2027년 1학기"),
                    start_date_var=Value("2026-09-07"), end_date_var=Value("2026-12-20"),
                    courses=[{"course_name": "기존 과목"}], semester_courses={}, semester_periods={},
                    studio_audio_var=Value("old-recording.wav"), last_generated_pdf="old.pdf",
                    studio_open_pdf_btn=SimpleNamespace(config=lambda **kwargs: None),
                    sem_badge_label=SimpleNamespace(config=lambda **kwargs: None),
                    refresh_studio_slides=lambda **kwargs: None,
                    populate_course_table=lambda: None, refresh_course_combos=lambda: None,
                )
                switch(app)
                self.assertEqual(app.courses, [])
                app.tutor_histories["같은 과목"] = [{"role": "user", "text": "새 학기 질문"}]
                self.assertEqual(saved[-1]["semester_start_date"], "2027-03-02")
                self.assertEqual(app.studio_audio_var.get(), "")
                self.assertIsNone(app.last_generated_pdf)
                app.courses.append({"course_name": "새 과목"})
                app.semester_var.set("2026년 2학기")
                switch(app)
                self.assertEqual(app.courses, [{"course_name": "기존 과목"}])
                self.assertNotIn("같은 과목", app.tutor_histories)
                self.assertEqual(saved[-1]["semester_start_date"], "2026-09-07")
                app.semester_var.set("2027년 1학기")
                switch(app)
                self.assertEqual(app.courses, [{"course_name": "새 과목"}])
                self.assertEqual(app.tutor_histories["같은 과목"][0]["text"], "새 학기 질문")
                app.studio_is_running = True
                app.semester_var.set("2026년 2학기")
                switch(app)
                self.assertEqual(app.semester_var.get(), "2027년 1학기")
                self.assertEqual(app.settings["semester"], "2027년 1학기")


if __name__ == "__main__":
    unittest.main()

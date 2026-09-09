from pathlib import Path
import unittest


class RequestedUiTests(unittest.TestCase):
    def test_requested_controls_and_tabs_exist_on_both_platforms(self):
        root = Path(__file__).parents[1]
        for platform in ("URY_macOS", "URY_Windows"):
            source = (root / platform / "system/code/settings_gui.py").read_text(encoding="utf-8")
            with self.subTest(platform=platform):
                self.assertIn('PART_OPTIONS = ["1부", "2부", "3부"]', source)
                self.assertIn('self.save_studio_language', source)
                self.assertIn('강의자료 선택', source)
                self.assertIn('강의노트 폴더', source)
                self.assertNotIn('text="✍️ 답안 채점"', source)
                self.assertIn('text="⚡ 벼락치기 정리노트"', source)
                self.assertIn('UNIVERSITY_THEMES', source)
                self.assertNotIn('text="▶ 전체 파이프라인 수동 구동"', source)
                for label in ("Tutor", "Updates", "User Guide", "Terms & Ethics"):
                    self.assertIn(label, source)
                self.assertIn('create_oval(3, 3, 21, 21', source)
                self.assertIn('Designed & Built by Ryu.H.J', source)
                self.assertIn('soft_windows = sys.platform == "win32"', source)
                self.assertIn('borderwidth=0 if soft_windows else 1', source)
                self.assertIn('rowheight=32 if soft_windows else 28', source)


if __name__ == "__main__":
    unittest.main()

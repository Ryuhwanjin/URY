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
                self.assertIn('강의자료 폴더 열기', source)
                self.assertIn('강의노트 폴더', source)
                self.assertNotIn('text="✍️ 답안 채점"', source)
                self.assertIn('text="⚡ 벼락치기 정리노트"', source)
                self.assertIn('UNIVERSITY_THEMES', source)
                self.assertNotIn('text="▶ 전체 파이프라인 수동 구동"', source)
                for label in ("업데이트", "기능 설명", "이용약관 · 윤리"):
                    self.assertIn(label, source)


if __name__ == "__main__":
    unittest.main()

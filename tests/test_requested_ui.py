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
                self.assertIn('"MUST READ":', source)
                self.assertIn("실시간 마이크 녹음", source)
                self.assertIn("Google AI Studio(https://aistudio.google.com/app/apikey)", source)
                self.assertIn("workspace/<학기>/<과목>/", source)
                self.assertIn("강의계획서 복수 파일", source)
                self.assertIn("답안 채점 기능은 제공하지 않습니다", source)
                self.assertIn("image.thumbnail((1200, 500)", source)
                self.assertIn('font=("Pretendard", 12)', source)
                self.assertIn('modifiers = ("Command", "Meta") if sys.platform == "darwin" else ("Control",)', source)
                self.assertIn('self.root.clipboard_get()', source)
                self.assertIn('self.root.clipboard_append(selected)', source)
                self.assertIn('input_classes = {"Entry", "TEntry", "Text", "TCombobox", "Spinbox", "TSpinbox"}', source)
                self.assertIn('f"<{modifier}-{key}>"', source)
                self.assertIn('self.root.bind_class(widget_name, f"<{modifier}-a>", _select_all)', source)
                self.assertNotIn('_clipboard_fallback', source)
                self.assertIn('def install_macos_edit_menu(self):', source)
                self.assertIn('NSEventModifierFlagCommand', source)
                self.assertIn('"selectAll:"', source)
                self.assertIn('create_oval(3, 3, 21, 21', source)
                self.assertIn('Designed & Built by Ryu.H.J', source)
                self.assertIn('soft_windows = sys.platform == "win32"', source)
                self.assertIn('borderwidth=0 if soft_windows else 1', source)
                self.assertIn('rowheight=32 if soft_windows else 28', source)


if __name__ == "__main__":
    unittest.main()

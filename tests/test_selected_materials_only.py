import ast
from pathlib import Path
import unittest


class SelectedMaterialsOnlyTest(unittest.TestCase):
    def test_custom_generation_has_no_old_note_or_folder_wide_pdf_input(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent.parent / platform / "system/code" / "process_all_lectures.py").read_text(encoding="utf-8")
            start = source.index("def generate_custom_lecture_note(")
            custom_source = source[start:]
            self.assertIn("session_only=True", custom_source)
            self.assertNotIn("prev_ko_content", custom_source)
            self.assertNotIn("prev_en_content", custom_source)
            self.assertNotIn("generate_all_pdfs(", custom_source)
            self.assertNotIn('glob.glob(os.path.join(user_notes_dir_nfc', custom_source)

    def test_note_prompts_do_not_invent_assessment_rules(self):
        for platform in ("URY_macOS", "URY_Windows"):
            root = Path(__file__).parent.parent / platform
            code = (root / "system/code/process_all_lectures.py").read_text(encoding="utf-8")
            prompt = (root / "system/prompts/강의노트_한국어_프롬프트.txt").read_text(encoding="utf-8")
            self.assertIn("원본에 없으면 추정하거나 작성하지 말 것", code)
            self.assertIn("원본에 없으면 추정하거나 작성하지 말 것", prompt)
            self.assertNotIn("Assessment Breakdown Table", code)

    def test_custom_generation_does_not_duplicate_timed_out_requests(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent.parent / platform / "system/code/process_all_lectures.py").read_text(encoding="utf-8")
            custom_source = source[source.index("def generate_custom_lecture_note("):]
            self.assertIn("stream_gemini_response(req, timeout=240", custom_source)
            self.assertIn("중복 사용량 방지를 위해 자동 재시도하지 않습니다", custom_source)
            self.assertIn('get_gemini_models_for("lecture_note", api_key, max_models=3)', custom_source)
            self.assertIn("토큰 사용량", custom_source)
            self.assertNotIn("backoff_delays", custom_source)


if __name__ == "__main__":
    unittest.main()

import ast
from pathlib import Path
import unittest


class SelectedMaterialsOnlyTest(unittest.TestCase):
    def test_custom_generation_has_no_old_note_or_folder_wide_pdf_input(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent / platform / "system/code" / "process_all_lectures.py").read_text(encoding="utf-8")
            start = source.index("def generate_custom_lecture_note(")
            custom_source = source[start:]
            self.assertIn("session_only=True", custom_source)
            self.assertNotIn("prev_ko_content", custom_source)
            self.assertNotIn("prev_en_content", custom_source)
            self.assertNotIn("generate_all_pdfs(", custom_source)
            self.assertNotIn('glob.glob(os.path.join(user_notes_dir_nfc', custom_source)


if __name__ == "__main__":
    unittest.main()

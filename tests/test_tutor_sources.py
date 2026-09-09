import importlib.util
import sys
from pathlib import Path
import unittest


class TutorSourceTests(unittest.TestCase):
    def test_guard_adds_real_source_filename(self):
        for platform in ("URY_macOS", "URY_Windows"):
            code = Path(__file__).parents[1] / platform / "system/code"
            sys.path.insert(0, str(code))
            try:
                spec = importlib.util.spec_from_file_location(f"tutor_{platform}", code / "lecture_tutor.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                kb = "=== [원본 강의자료: week2.pdf] ===\n--- [Page 3] ---\n핵심 개념"
                answer = module.verify_and_guard_answer("수업의 핵심 개념입니다.", kb)
                self.assertIn("`week2.pdf`", answer)
            finally:
                sys.path.pop(0)


if __name__ == "__main__":
    unittest.main()

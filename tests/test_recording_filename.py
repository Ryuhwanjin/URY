import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).parents[1] / "URY_macOS/system/code/audio_recorder.py"


class RecordingFilenameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("audio_recorder_under_test", MODULE)
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_name_contains_selected_date_and_sanitized_course(self):
        with tempfile.TemporaryDirectory() as folder:
            first = self.module.build_recording_filename(folder, "2026-09-09", "자료/구조론", "m4a")
            Path(folder, first).touch()
            second = self.module.build_recording_filename(folder, "2026-09-09", "자료/구조론", "m4a")

        self.assertEqual(first, "2026-09-09_자료_구조론_1교시_실시간녹음.m4a")
        self.assertEqual(second, "2026-09-09_자료_구조론_2교시_실시간녹음.m4a")


if __name__ == "__main__":
    unittest.main()

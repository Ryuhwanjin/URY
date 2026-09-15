import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


WINDOWS_CODE = Path(__file__).parents[1] / "URY_Windows" / "system" / "code"
sys.path.insert(0, str(WINDOWS_CODE))

import generate_pdfs
import audio_recorder
import subprocess_utils


class WindowsRuntimeTests(unittest.TestCase):
    def test_cli_children_are_configured_without_console_windows(self):
        with mock.patch.object(subprocess_utils.sys, "platform", "win32"):
            self.assertEqual(
                subprocess_utils.quiet_subprocess_kwargs(),
                {"creationflags": getattr(subprocess_utils.subprocess, "CREATE_NO_WINDOW", 0x08000000)},
            )

        for relative_path in (
            "URY_Windows/system/code/process_all_lectures.py",
            "URY_Windows/system/code/generate_pdfs.py",
        ):
            source = (Path(__file__).parents[1] / relative_path).read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIn("**quiet_subprocess_kwargs()", source)

    def test_locked_windows_pdf_is_saved_to_a_new_name(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "lecture.pdf"
            pending = Path(temp_dir) / "pending.pdf"
            target.write_bytes(b"old pdf")
            pending.write_bytes(b"new pdf")
            real_replace = os.replace

            def replace_unless_locked(source, destination):
                if Path(destination) == target:
                    raise PermissionError(13, "Permission denied")
                real_replace(source, destination)

            with mock.patch.object(generate_pdfs.sys, "platform", "win32"), mock.patch.object(
                generate_pdfs.os, "replace", side_effect=replace_unless_locked
            ):
                output = Path(generate_pdfs._replace_rendered_pdf(str(pending), str(target)))

            self.assertNotEqual(output, target)
            self.assertEqual(target.read_bytes(), b"old pdf")
            self.assertEqual(output.read_bytes(), b"new pdf")

    def test_windows_microphone_records_wav_without_ffmpeg(self):
        class FakeStream:
            def __init__(self, **kwargs):
                self.callback = kwargs["callback"]

            def start(self):
                self.callback(b"\x00\x00" * 4, 4, None, None)

            def stop(self):
                pass

            def close(self):
                pass

        fake_sounddevice = mock.Mock()
        fake_sounddevice.query_devices.return_value = {
            "max_input_channels": 1,
            "default_samplerate": 44100,
        }
        fake_sounddevice.RawInputStream.side_effect = FakeStream

        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.dict(sys.modules, {"sounddevice": fake_sounddevice}), mock.patch.object(
                audio_recorder.sys, "platform", "win32"
            ), mock.patch.object(audio_recorder.config_manager, "load_settings", return_value={"courses": []}), mock.patch.object(
                audio_recorder.config_manager, "get_course_dir", return_value=folder
            ):
                recorder = audio_recorder.AudioRecorder()
                started = recorder.start_recording("Test", "2026-09-15")
                self.assertEqual(started["status"], "success")
                self.assertIsNone(recorder.process)
                stopped = recorder.stop_recording()

            self.assertEqual(stopped["status"], "success")
            self.assertTrue(stopped["output_file"].endswith(".wav"))
            self.assertGreater(stopped["file_size"], 44)


if __name__ == "__main__":
    unittest.main()

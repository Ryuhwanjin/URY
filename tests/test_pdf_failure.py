from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
import builtins
import unittest

from check_pdf_render import load_renderer


class PdfFailureTest(unittest.TestCase):
    def test_inaccessible_markdown_is_reported_and_skipped(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                ns = load_renderer(platform)
                source = Path(tmp) / "Week2.md"
                source.write_text("# Week 2\n\n2027-03-08\n")
                target = Path(tmp) / "Week2.pdf"
                real_open = builtins.open

                def deny_source_read(path, mode="r", *args, **kwargs):
                    if Path(path) == source and "r" in mode:
                        raise PermissionError(13, "Permission denied")
                    return real_open(path, mode, *args, **kwargs)

                with patch("builtins.open", side_effect=deny_source_read):
                    result = ns["convert_single_md_to_pdf"](str(source), str(target), "Week 2", tmp)

                self.assertIsNone(result)
                self.assertFalse(target.exists())

    def test_failed_renderer_preserves_existing_pdf(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform), TemporaryDirectory() as tmp:
                ns = load_renderer(platform)
                source = Path(tmp) / "Week2.md"
                source.write_text("# Week 2\n\n2027-03-08\n")
                target = Path(tmp) / "Week2.pdf"
                original = b"%PDF-original-result" + b"X" * 200
                target.write_bytes(original)
                ns["find_chromium_browser"] = lambda: str(source)
                with patch("subprocess.run", return_value=SimpleNamespace(returncode=1)):
                    with self.assertRaises(RuntimeError):
                        ns["convert_single_md_to_pdf"](str(source), str(target), "Week 2", tmp)
                self.assertEqual(target.read_bytes(), original)
                self.assertFalse(list(Path(tmp).glob("ury-render-*")))


if __name__ == "__main__":
    unittest.main()

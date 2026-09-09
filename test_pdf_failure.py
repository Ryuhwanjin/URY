from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from check_pdf_render import load_renderer


class PdfFailureTest(unittest.TestCase):
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

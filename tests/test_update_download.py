import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


class Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class UpdateDownloadTest(unittest.TestCase):
    def test_release_installer_download_is_atomic(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform / "system/code/update_checker.py"
            namespace = {"__name__": "update_checker_test"}
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
            suffix, system = (".dmg", "Darwin") if platform == "URY_macOS" else (".exe", "Windows")
            release = {"assets": [{"name": f"URY_Engine{suffix}", "browser_download_url": "https://example.com/file"}]}
            with tempfile.TemporaryDirectory() as directory, \
                    patch.object(namespace["platform"], "system", return_value=system), \
                    patch.object(namespace["Path"], "home", return_value=Path(directory)), \
                    patch("urllib.request.urlopen", side_effect=[Response(json.dumps(release).encode()), Response(b"installer")]):
                (Path(directory) / "Downloads").mkdir()
                result = Path(namespace["download_latest_installer"]())
                self.assertEqual(result.read_bytes(), b"installer")
                self.assertFalse(result.with_suffix(result.suffix + ".download").exists())


if __name__ == "__main__":
    unittest.main()

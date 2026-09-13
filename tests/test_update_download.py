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
            name, system = (
                ("URY_Engine_v0.9.7.dmg", "Darwin")
                if platform == "URY_macOS"
                else ("URY_Engine_v0.9.7_Installer.exe", "Windows")
            )
            release = {"assets": [{"name": name, "browser_download_url": "https://example.com/file"}]}
            with tempfile.TemporaryDirectory() as directory, \
                    patch.object(namespace["platform"], "system", return_value=system), \
                    patch.object(namespace["Path"], "home", return_value=Path(directory)), \
                    patch("urllib.request.urlopen", side_effect=[Response(json.dumps(release).encode()), Response(b"installer")]):
                (Path(directory) / "Downloads").mkdir()
                result = Path(namespace["download_latest_installer"]())
                self.assertEqual(result.read_bytes(), b"installer")
                self.assertFalse(result.with_suffix(result.suffix + ".download").exists())

    def test_platform_asset_selection_ignores_other_platform_and_prefers_installer(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform / "system/code/update_checker.py"
            namespace = {"__name__": "update_checker_test"}
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
            system = "Darwin" if platform == "URY_macOS" else "Windows"
            assets = sorted([
                {"name": "URY_Engine_v0.9.7.dmg"},
                {"name": "URY_Engine_v0.9.7_macOS.zip"},
                {"name": "URY_Engine_v0.9.7_Windows.zip"},
                {"name": "URY_Engine_v0.9.7_Installer.exe"},
            ], key=lambda item: item["name"])
            with patch.object(namespace["platform"], "system", return_value=system):
                selected = namespace["_select_platform_asset"](assets)
            expected = "URY_Engine_v0.9.7.dmg" if platform == "URY_macOS" else "URY_Engine_v0.9.7_Installer.exe"
            self.assertEqual(selected["name"], expected)
            if platform == "URY_Windows":
                legacy_selected = next(
                    item for item in assets
                    if item["name"].lower().endswith((".exe", ".zip"))
                )
                self.assertEqual(legacy_selected["name"], "URY_Engine_v0.9.7_Installer.exe")

    def test_update_check_compares_matching_platform_asset_version(self):
        release = {
            "tag_name": "v0.9.7",
            "html_url": "https://example.com/release",
            "assets": [
                {"name": "URY_Engine_v0.9.7.dmg"},
                {"name": "URY_Setup_v0.9.8.exe"},
            ],
        }
        for platform_name in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform_name / "system/code/update_checker.py"
            namespace = {"__name__": "update_checker_test"}
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
            system = "Darwin" if platform_name == "URY_macOS" else "Windows"
            with patch.object(namespace["platform"], "system", return_value=system), \
                    patch("urllib.request.urlopen", return_value=Response(json.dumps(release).encode())):
                version, url = namespace["get_latest_release"]()
            expected = "v0.9.7" if platform_name == "URY_macOS" else "v0.9.8"
            self.assertEqual(version, expected)
            self.assertEqual(url, release["html_url"])
            self.assertEqual(namespace["is_newer"](version), platform_name == "URY_Windows")

    def test_update_check_without_matching_platform_asset_is_not_newer(self):
        release = {
            "tag_name": "v0.9.8",
            "assets": [{"name": "URY_Engine_v0.9.8_linux.AppImage"}],
        }
        for platform_name in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent.parent / platform_name / "system/code/update_checker.py"
            namespace = {"__name__": "update_checker_test"}
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), namespace)
            system = "Darwin" if platform_name == "URY_macOS" else "Windows"
            with patch.object(namespace["platform"], "system", return_value=system), \
                    patch("urllib.request.urlopen", return_value=Response(json.dumps(release).encode())):
                version, _ = namespace["get_latest_release"]()
            self.assertEqual(version, "")
            self.assertFalse(namespace["is_newer"](version))


if __name__ == "__main__":
    unittest.main()

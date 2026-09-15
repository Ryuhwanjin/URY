import ast
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest


class MicrophonePermissionTest(unittest.TestCase):
    def test_build_sets_microphone_description_before_signing(self):
        source = Path(__file__).resolve().parents[1] / "build_macos_app.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and ast.unparse(node.func) == "subprocess.run"]
        permission = next((node for node in calls
                           if "NSMicrophoneUsageDescription" in ast.unparse(node)), None)
        self.assertIsNotNone(permission, "Missing microphone usage description causes TCC SIGABRT")
        signing = next(node for node in calls if '"--sign"' in ast.unparse(node).replace("'", '"'))
        self.assertLess(permission.lineno, signing.lineno)
        if sys.platform == "darwin":
            with tempfile.TemporaryDirectory() as folder:
                plist = Path(folder) / "Info.plist"
                plist.write_bytes(plistlib.dumps({"CFBundleIdentifier": "com.ury.engine"}))
                exec(compile(ast.Expression(permission), str(source), "eval"),
                     {"subprocess": subprocess, "plist": plist})
                info = plistlib.loads(plist.read_bytes())
                self.assertTrue(info["NSMicrophoneUsageDescription"].strip())
                self.assertEqual(info["CFBundleIdentifier"], "com.ury.engine")


if __name__ == "__main__":
    unittest.main()

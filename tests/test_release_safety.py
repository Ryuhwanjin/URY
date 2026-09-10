import ast
from pathlib import Path
import unittest


class ReleaseSafetyTest(unittest.TestCase):
    def test_release_build_does_not_mutate_source_or_package_private_data(self):
        source = (Path(__file__).parent.parent / "build_release_all.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        functions = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        self.assertNotIn("sync_system_files", functions)
        self.assertNotIn("sanitize_personal_configs", functions)
        self.assertIn('"settings.json"', source)
        self.assertIn('"시간표.json"', source)
        self.assertIn('"강의노트"', source)
        build = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "build_all_releases")
        calls = {ast.unparse(n.func) for n in ast.walk(build) if isinstance(n, ast.Call)}
        self.assertNotIn("sync_system_files", calls)
        self.assertNotIn("sanitize_personal_configs", calls)


if __name__ == "__main__":
    unittest.main()

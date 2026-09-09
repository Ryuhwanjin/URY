import ast
from pathlib import Path
from types import SimpleNamespace
import unittest


class NavigationTest(unittest.TestCase):
    def test_every_header_button_targets_an_existing_tab(self):
        for platform in ("URY_macOS", "URY_Windows"):
            with self.subTest(platform=platform):
                path = Path(__file__).parent / platform / "system/code/settings_gui.py"
                tree = ast.parse(path.read_text(encoding="utf-8"))
                cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "UnifiedDashboardApp")
                methods = {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}
                tab_count = sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                                and ast.unparse(n.func) == "self.notebook.add"
                                for n in ast.walk(methods["create_tabs"]))
                header = methods["create_header_card"]
                defs = next(n.value for n in ast.walk(header) if isinstance(n, ast.Assign)
                            and any(ast.unparse(t) == "self.tab_defs" for t in n.targets))
                buttons = ast.literal_eval(defs)
                self.assertEqual(len(buttons), tab_count)
                self.assertEqual([index for _, index in buttons], list(range(tab_count)))
                settings_index = next(index for label, index in buttons if "Settings" in label)
                selected = []
                for name in ("create_header_card", "show_resolution_quick_menu"):
                    for node in ast.walk(methods[name]):
                        if isinstance(node, ast.Lambda) and isinstance(node.body, ast.Call) and ast.unparse(node.body.func) == "self.switch_to_tab" and isinstance(node.body.args[0], ast.Constant):
                            callback = eval(compile(ast.Expression(node), str(path), "eval"),
                                            {"self": SimpleNamespace(switch_to_tab=selected.append)})
                            callback(*([None] * len(node.args.args)))
                self.assertEqual(selected, [settings_index, settings_index])


if __name__ == "__main__":
    unittest.main()

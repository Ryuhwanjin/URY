import ast
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest


@unittest.skipUnless(os.environ.get("URY_GUI_TEST") == "1", "requires desktop Tk")
class AccentWidgetsTest(unittest.TestCase):
    def test_existing_and_new_widgets_follow_repeated_accent_changes(self):
        import tkinter as tk
        from tkinter import ttk

        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).resolve().parent.parent / platform / "system/code/settings_gui.py"
            tree = ast.parse(path.read_text())
            button = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "SquareRoundButton")
            app = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "UnifiedDashboardApp")
            methods = {n.name: n for n in app.body if isinstance(n, ast.FunctionDef)}
            self.assertNotIn("toggle_theme", methods)
            names = ("accent_color", "accent_values", "refresh_theme_widgets", "set_theme_accent")
            cls = ast.ClassDef(name="App", bases=[], keywords=[], body=[methods[n] for n in names], decorator_list=[])
            namespace = {"tk": tk, "re": re, "config_manager": SimpleNamespace(save_settings=lambda _: None)}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[button, cls], type_ignores=[])), str(path), "exec"), namespace)
            root = tk.Tk()
            root.withdraw()
            try:
                subject = namespace["App"]()
                subject.root = root
                subject.settings = {}
                subject.theme_accent = "#1C4732"
                subject.setup_styles = lambda: None
                subject.apply_theme_icon = lambda: None
                root.accent_color = subject.accent_color
                subject._accent_values = subject.accent_values()
                label = tk.Label(root, fg=subject.accent_color("#1c4732"), bg="#ffffff")
                custom = namespace["SquareRoundButton"](root)
                entry = tk.Entry(root, selectbackground=subject.accent_color("#d8f3dc"))
                themed = ttk.Label(root, foreground=subject.accent_color("#1c4732"))
                subject.refresh_theme_widgets()
                for color in ("#003478", "#FFFFFF", "#8B1E3F", "#663399"):
                    subject.set_theme_accent(color)
                    self.assertEqual(label.cget("fg"), color)
                    self.assertEqual(label.cget("bg"), "#ffffff")
                    self.assertEqual(custom.normal_bg, color)
                    custom.on_enter()
                    self.assertEqual(custom.itemcget(custom.rect_id, "fill"), subject.accent_color("#255e42"))
                    self.assertEqual(entry.cget("selectbackground"), subject.accent_color("#d8f3dc"))
                    self.assertEqual(str(themed.cget("foreground")), color)
                new_button = namespace["SquareRoundButton"](root)
                self.assertEqual(new_button.normal_bg, "#663399")
            finally:
                root.destroy()

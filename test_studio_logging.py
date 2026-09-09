import ast
import queue
from pathlib import Path
from types import SimpleNamespace
import unittest


class StudioLoggingTest(unittest.TestCase):
    def test_worker_events_are_delivered_in_order_on_ui_poll(self):
        for platform in ("URY_macOS", "URY_Windows"):
            path = Path(__file__).parent / platform / "system/code/settings_gui.py"
            tree = ast.parse(path.read_text(encoding="utf-8"))
            cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                       and n.name == "UnifiedDashboardApp")
            method = next(n for n in cls.body if isinstance(n, ast.FunctionDef)
                          and n.name == "drain_studio_events")
            namespace = {"queue": queue}
            exec(compile(ast.Module(body=[method], type_ignores=[]), str(path), "exec"), namespace)
            delivered, scheduled = [], []
            app = SimpleNamespace(
                studio_events=queue.Queue(),
                on_studio_log_event=lambda *args: delivered.append(("log", args)),
                on_studio_generation_success=lambda *args: delivered.append(("success", args)),
                on_studio_generation_error=lambda *args: delivered.append(("error", args)),
                root=SimpleNamespace(after=lambda *args: scheduled.append(args)),
                drain_studio_events=lambda: None,
            )
            events = [("log", (7, "업로드 중", 1, None)),
                      ("error", (7, "연결 시간 초과",)), ("success", (7, {"path": "note.pdf"}))]
            for event in events:
                app.studio_events.put(event)
            app._studio_run_id = 7
            namespace["drain_studio_events"](app)
            self.assertEqual(delivered, [("log", ("업로드 중", 1, None)),
                                         ("error", ("연결 시간 초과",)),
                                         ("success", ({"path": "note.pdf"},))])
            self.assertEqual(scheduled, [(100, app.drain_studio_events)])
            namespace["drain_studio_events"](app)
            self.assertEqual(len(delivered), 3)
            self.assertEqual(len(scheduled), 2)

    def test_cancel_token_is_scoped_to_one_generation(self):
        for platform in ("URY_macOS", "URY_Windows"):
            source = (Path(__file__).parent / platform / "system/code/settings_gui.py").read_text(encoding="utf-8")
            self.assertIn("cancel_event = threading.Event()", source)
            self.assertIn("cancel_check=cancel_event.is_set", source)
            self.assertIn("previous_cancel.set()", source)


if __name__ == "__main__":
    unittest.main()

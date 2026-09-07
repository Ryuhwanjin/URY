# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox


VERSION = "0.7.8"


def get_windows_root():
    """
    build_exe_gui.py
    └─ system/code/

    따라서 두 단계 위가 URY_Windows/
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, "..", ".."))


def run_command(command, cwd, update_status_cb):
    """명령 실행 및 실시간 로그 전달"""
    try:
        update_status_cb(" ".join(command))

        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        for line in process.stdout:
            line = line.rstrip()
            if line:
                update_status_cb(line)

        return_code = process.wait()

        if return_code != 0:
            update_status_cb(
                f"[ERROR] 명령 실행 실패 (exit code: {return_code})"
            )
            return False

        return True

    except Exception as e:
        update_status_cb(f"[ERROR] {e}")
        return False


def run_build_process(target_install_dir, update_status_cb, on_complete_cb):
    """
    실제 Windows EXE 빌드 프로세스.
    별도 스레드에서 실행됨.
    """

    try:
        windows_root = get_windows_root()
        code_dir = os.path.join(windows_root, "system", "code")

        main_script = os.path.join(code_dir, "settings_gui.py")
        icon_path = os.path.join(windows_root, "app_icon.ico")

        dist_dir = os.path.join(windows_root, "dist")
        build_dir = os.path.join(windows_root, "build")

        final_dist = os.path.join(dist_dir, "URY_Engine")

        update_status_cb(f"[INFO] Windows 프로젝트: {windows_root}")
        update_status_cb(f"[INFO] 엔트리포인트: {main_script}")

        # 기본 파일 확인
        if not os.path.isfile(main_script):
            raise FileNotFoundError(
                f"settings_gui.py를 찾을 수 없습니다: {main_script}"
            )

        if not os.path.isfile(icon_path):
            update_status_cb(
                f"[WARNING] 아이콘을 찾을 수 없습니다: {icon_path}"
            )

        # 이전 빌드 삭제
        update_status_cb("[1/4] 이전 빌드 파일 정리 중...")

        if os.path.isdir(final_dist):
            shutil.rmtree(final_dist, ignore_errors=True)

        if os.path.isdir(build_dir):
            shutil.rmtree(build_dir, ignore_errors=True)

        # PyInstaller 확인/설치
        update_status_cb("[2/4] PyInstaller 확인 중...")

        check_pyinstaller = subprocess.run(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                "--version",
            ],
            cwd=windows_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if check_pyinstaller.returncode != 0:
            update_status_cb(
                "[INFO] PyInstaller가 없어 설치를 진행합니다..."
            )

            install_ok = run_command(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "pyinstaller",
                ],
                windows_root,
                update_status_cb,
            )

            if not install_ok:
                raise RuntimeError("PyInstaller 설치에 실패했습니다.")

        # PyInstaller 명령 구성
        update_status_cb("[3/4] EXE 빌드 중...")

        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--clean",
            "--onedir",
            "--windowed",
            "--name",
            "URY_Engine",
            "--add-data",
            f"{os.path.join(windows_root, 'system')}{os.pathsep}system",
        ]

        if os.path.isfile(icon_path):
            command.extend([
                "--icon",
                icon_path,
            ])

        command.append(main_script)

        success = run_command(
            command,
            windows_root,
            update_status_cb,
        )

        if not success:
            raise RuntimeError("PyInstaller EXE 빌드에 실패했습니다.")

        # 결과 확인
        update_status_cb("[4/4] 빌드 결과 확인 중...")

        if not os.path.isdir(final_dist):
            raise RuntimeError(
                f"빌드 결과 폴더가 생성되지 않았습니다: {final_dist}"
            )

        exe_path = os.path.join(final_dist, "URY_Engine.exe")

        if not os.path.isfile(exe_path):
            raise RuntimeError(
                f"URY_Engine.exe가 생성되지 않았습니다: {exe_path}"
            )

        update_status_cb("")
        update_status_cb("========================================")
        update_status_cb("[OK] Windows EXE 빌드 완료")
        update_status_cb(f"[OK] 결과 위치: {final_dist}")
        update_status_cb(f"[OK] 실행 파일: {exe_path}")
        update_status_cb("========================================")

        # 사용자가 지정한 설치 폴더가 있으면 복사
        if target_install_dir:
            target_install_dir = os.path.abspath(
                os.path.expanduser(target_install_dir)
            )

            if os.path.normcase(target_install_dir) != os.path.normcase(
                final_dist
            ):
                update_status_cb(
                    f"[INFO] 설치 폴더로 복사 중: {target_install_dir}"
                )

                if os.path.isdir(target_install_dir):
                    shutil.rmtree(target_install_dir, ignore_errors=True)

                shutil.copytree(final_dist, target_install_dir)

                update_status_cb(
                    f"[OK] 설치 폴더 복사 완료: {target_install_dir}"
                )

        on_complete_cb(True, final_dist)

    except Exception as e:
        update_status_cb("")
        update_status_cb("========================================")
        update_status_cb(f"[ERROR] 빌드 실패: {e}")
        update_status_cb("========================================")

        on_complete_cb(False, str(e))


class BuildGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"URY Engine v{VERSION} - Windows EXE Builder")
        self.root.geometry("720x520")

        self.target_dir = tk.StringVar(
            value=os.path.join(
                os.path.expanduser("~"),
                "Desktop",
                "URY_Engine",
            )
        )

        self.building = False

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text=f"URY Engine v{VERSION}",
            font=("Arial", 20, "bold"),
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            frame,
            text="Windows Standalone EXE Builder",
            font=("Arial", 11),
        )
        subtitle.pack(pady=(0, 20))

        target_frame = tk.Frame(frame)
        target_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            target_frame,
            text="설치 폴더:",
        ).pack(anchor="w")

        path_frame = tk.Frame(target_frame)
        path_frame.pack(fill="x", pady=5)

        entry = tk.Entry(
            path_frame,
            textvariable=self.target_dir,
        )
        entry.pack(side="left", fill="x", expand=True)

        tk.Button(
            path_frame,
            text="찾아보기",
            command=self.select_folder,
        ).pack(side="right", padx=(8, 0))

        self.build_button = tk.Button(
            frame,
            text="EXE 빌드 시작",
            command=self.start_build,
            height=2,
        )
        self.build_button.pack(fill="x", pady=(10, 15))

        log_frame = tk.Frame(frame)
        log_frame.pack(fill="both", expand=True)

        tk.Label(
            log_frame,
            text="빌드 로그",
        ).pack(anchor="w")

        self.log_text = tk.Text(
            log_frame,
            wrap="word",
            state="disabled",
        )
        self.log_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar = tk.Scrollbar(
            log_frame,
            command=self.log_text.yview,
        )
        scrollbar.pack(side="right", fill="y")

        self.log_text.configure(
            yscrollcommand=scrollbar.set
        )

    def select_folder(self):
        folder = filedialog.askdirectory(
            title="EXE 설치 폴더 선택"
        )

        if folder:
            self.target_dir.set(folder)

    def update_status(self, message):
        def append():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self.root.after(0, append)

    def build_complete(self, success, result):
        def finish():
            self.building = False
            self.build_button.configure(
                state="normal",
                text="EXE 빌드 시작",
            )

            if success:
                messagebox.showinfo(
                    "빌드 완료",
                    f"Windows EXE 빌드가 완료되었습니다.\n\n{result}",
                )
            else:
                messagebox.showerror(
                    "빌드 실패",
                    f"Windows EXE 빌드에 실패했습니다.\n\n{result}",
                )

        self.root.after(0, finish)

    def start_build(self):
        if self.building:
            return

        self.building = True

        self.build_button.configure(
            state="disabled",
            text="빌드 중...",
        )

        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        target_dir = self.target_dir.get().strip()

        thread = threading.Thread(
            target=run_build_process,
            args=(
                target_dir,
                self.update_status,
                self.build_complete,
            ),
            daemon=True,
        )

        thread.start()


def main():
    root = tk.Tk()
    BuildGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

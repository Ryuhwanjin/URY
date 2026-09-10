"""Run with a Tk-enabled Python: python build_macos_app.py."""
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".venv-macos-build"
APP_VERSION = "0.9.4"
ICON_PADDING_RATIO = 0.12


def main():
    if sys.platform != "darwin":
        raise SystemExit("macOS is required to build this app.")
    python = ENV / "bin/python"
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(ENV)
    subprocess.run([str(python), "-c", "import tkinter; r=tkinter.Tk(); r.withdraw(); r.destroy()"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(ROOT / "requirements-macos-build.txt")], check=True)
    from PIL import Image
    icon = ROOT / "build/macos/ury_engine_icon.icns"
    icon.parent.mkdir(parents=True, exist_ok=True)
    source_icon = Image.open(ROOT / "assets/ury_engine_icon.png").convert("RGBA")
    # macOS Dock에서 다른 앱보다 크게 보이지 않도록 안전 여백을 둔다.
    pad = round(source_icon.width * ICON_PADDING_RATIO)
    padded_icon = Image.new("RGBA", source_icon.size, (0, 0, 0, 0))
    scaled_icon = source_icon.resize(
        (source_icon.width - pad * 2, source_icon.height - pad * 2), Image.Resampling.LANCZOS)
    padded_icon.alpha_composite(scaled_icon, (pad, pad))
    padded_icon.save(
        icon, format="ICNS", sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)])
    code = ROOT / "URY_macOS/system/code"
    command = [str(python), "-m", "PyInstaller", "--noconfirm", "--windowed",
               "--name", "URY", "--osx-bundle-identifier", "com.ury.engine",
               "--icon", str(icon),
               "--paths", str(code), "--distpath", str(ROOT / "URY_macOS"),
               "--workpath", str(ROOT / "build/macos"), "--specpath", str(ROOT / "build/macos")]
    for resource in ("code", "prompts", "bin"):
        command += ["--add-data", f"{code.parent / resource}:{resource}"]
    command += ["--add-data", f"{ROOT / 'assets'}:assets"]
    for module in code.glob("*.py"):
        if module.stem not in {"ensure_requirements", "uninstall_gui"}:
            command += ["--hidden-import", module.stem]
    command.append(str(ROOT / "설정관리자.py"))
    subprocess.run(command, cwd=ROOT, check=True)
    app = ROOT / "URY_macOS/URY.app"
    plist = app / "Contents/Info.plist"
    subprocess.run(["plutil", "-replace", "CFBundleShortVersionString", "-string", APP_VERSION, str(plist)], check=True)
    subprocess.run(["plutil", "-replace", "CFBundleVersion", "-string", APP_VERSION, str(plist)], check=True)
    subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)], check=True)
    subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)
    check = subprocess.run([str(app / "Contents/MacOS/URY"), "--smoke-test"],
                           capture_output=True, text=True, timeout=30, check=True)
    if "GUI_SMOKE_OK" not in check.stdout:
        raise SystemExit(f"App window check failed: {check.stdout}\n{check.stderr}")
    print(f"Built: {app}")


if __name__ == "__main__":
    main()

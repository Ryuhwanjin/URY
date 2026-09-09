"""GitHub Releases 기반의 가벼운 업데이트 확인기."""

import json
import os
import platform
import subprocess
import urllib.request
import webbrowser
from pathlib import Path


CURRENT_VERSION = "v0.9.0"
LATEST_RELEASE_URL = "https://api.github.com/repos/Ryuhwanjin/URY_engine/releases/latest"
RELEASES_PAGE_URL = "https://github.com/Ryuhwanjin/URY_engine/releases/latest"


def _version_key(value):
    return tuple(int(part) for part in value.lstrip("vV").split("-")[0].split(".") if part.isdigit())


def get_latest_release(timeout=4):
    request = urllib.request.Request(LATEST_RELEASE_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.loads(response.read().decode("utf-8"))
    tag = release.get("tag_name", "")
    return tag, release.get("html_url", RELEASES_PAGE_URL)


def download_latest_installer(timeout=30):
    request = urllib.request.Request(LATEST_RELEASE_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.loads(response.read().decode("utf-8"))
    suffixes = (".dmg",) if platform.system() == "Darwin" else (".exe", ".zip")
    asset = next((item for item in release.get("assets", [])
                  if item.get("name", "").lower().endswith(suffixes)), None)
    if not asset:
        return None
    target = Path.home() / "Downloads" / Path(asset["name"]).name
    partial = target.with_suffix(target.suffix + ".download")
    download = urllib.request.Request(asset["browser_download_url"], headers={"Accept": "application/octet-stream"})
    with urllib.request.urlopen(download, timeout=timeout) as response, partial.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    partial.replace(target)
    return str(target)


def open_installer(path):
    if platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    elif os.name == "nt":
        os.startfile(path)
    else:
        subprocess.Popen(["xdg-open", path])


def is_newer(version):
    return bool(version) and _version_key(version) > _version_key(CURRENT_VERSION)


def open_release_page(url=RELEASES_PAGE_URL):
    webbrowser.open(url)

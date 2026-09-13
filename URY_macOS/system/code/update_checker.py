"""GitHub Releases 기반의 가벼운 업데이트 확인기."""

import json
import os
import platform
import re
import subprocess
import urllib.request
import webbrowser
from pathlib import Path


CURRENT_VERSION = "v0.9.6"
LATEST_RELEASE_URL = "https://api.github.com/repos/Ryuhwanjin/URY/releases/latest"
RELEASES_PAGE_URL = "https://github.com/Ryuhwanjin/URY/releases/latest"
VERSION_PATTERN = re.compile(r"v?(\d+(?:\.\d+)+)", re.IGNORECASE)


def _version_key(value):
    return tuple(int(part) for part in value.lstrip("vV").split("-")[0].split(".") if part.isdigit())


def get_latest_release(timeout=4):
    request = urllib.request.Request(LATEST_RELEASE_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.loads(response.read().decode("utf-8"))
    asset = _select_platform_asset(release.get("assets", []))
    version = _asset_version(asset)
    return version, release.get("html_url", RELEASES_PAGE_URL)


def _asset_rank(name):
    """Return the preferred rank for an installer matching this platform."""
    name = Path(name).name.lower()
    system = platform.system()
    if system == "Darwin":
        if name.endswith(".dmg"):
            return 0
        if name.endswith(".zip") and "mac" in name:
            return 1
    elif system == "Windows":
        if name.endswith(".exe") and any(marker in name for marker in ("windows", "win", "setup", "installer")):
            return 0
        if name.endswith(".zip") and any(marker in name for marker in ("windows", "win")):
            return 1
    return None


def _select_platform_asset(assets):
    candidates = []
    for item in assets:
        rank = _asset_rank(item.get("name", ""))
        if rank is not None:
            candidates.append((rank, item))
    return min(candidates, key=lambda candidate: candidate[0])[1] if candidates else None


def _asset_version(asset):
    if not asset:
        return ""
    match = VERSION_PATTERN.search(Path(asset.get("name", "")).name)
    return f"v{match.group(1)}" if match else ""


def download_latest_installer(timeout=30):
    request = urllib.request.Request(LATEST_RELEASE_URL, headers={"Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        release = json.loads(response.read().decode("utf-8"))
    asset = _select_platform_asset(release.get("assets", []))
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

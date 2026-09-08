"""GitHub Releases 기반의 가벼운 업데이트 확인기."""

import json
import urllib.request
import webbrowser


CURRENT_VERSION = "v0.7.9"
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


def is_newer(version):
    return bool(version) and _version_key(version) > _version_key(CURRENT_VERSION)


def open_release_page(url=RELEASES_PAGE_URL):
    webbrowser.open(url)

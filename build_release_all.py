#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎓 URY Engine v0.7.9 — macOS & Windows 듀얼 동시 배포 자동화 통합 빌더 (build_release_all.py)
- macOS 패키지 (URY_macOS -> URY_Engine_v0.7.9_macOS.zip & .dmg)
- Windows 패키지 (URY_Windows -> URY_Engine_v0.7.9_Windows.zip)
- 소스코드 및 문서 100% 최신 동기화 후 '배포/' 디렉터리에 배포본 일괄 출판
"""

import os
import sys
import zipfile
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MACOS_DIR = os.path.join(ROOT_DIR, "URY_macOS")
WIN_DIR = os.path.join(ROOT_DIR, "URY_Windows")
DIST_DIR = os.path.join(ROOT_DIR, "배포")

VERSION = "v0.9.0"
PRIVATE_FILES = {".env", "settings.json", "processed_history.json"}
PRIVATE_DIRS = {"__pycache__", ".markdown_cache", "강의노트", "예상문제", "음성녹음", "칠판사진", "images"}



def make_zip_archive(source_dir, output_zip_path):
    """지정 폴더를 릴리즈 ZIP 파일로 압축"""
    print(f"📦 압축 파일 생성 중: {os.path.basename(output_zip_path)}...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in PRIVATE_DIRS and not d.startswith(".")]
            for file in files:
                if file.startswith('.') or file.endswith('.pyc') or file == '.DS_Store' or file in PRIVATE_FILES:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zipf.write(file_path, arcname)
    print(f"  ✅ 압축 완료! ({round(os.path.getsize(output_zip_path)/1024/1024, 1)}MB)")

def build_all_releases():
    os.makedirs(DIST_DIR, exist_ok=True)
    print("=========================================================")
    print(f"🚀 URY Engine {VERSION} macOS & Windows 듀얼 동시 배포 파이프라인 가동")
    print("=========================================================\n")

    # 원본 소스와 로컬 설정은 절대 수정하지 않는다.
    print("🔒 원본 소스·개인 설정은 건드리지 않고 현재 상태를 패키징합니다.")

    # 2. macOS 전용 빌드 (DMG + ZIP)
    print("\n🍏 [2/4] macOS 배포 패키징 중...")
    mac_zip_path = os.path.join(DIST_DIR, f"URY_Engine_{VERSION}_macOS.zip")
    
    # macOS 권한 부여 및 서명
    try:
        subprocess.call(["chmod", "+x"] + [os.path.join(MACOS_DIR, f) for f in os.listdir(MACOS_DIR) if f.endswith(".command")])
        app_path = os.path.join(MACOS_DIR, "URY Engine.app")
        if os.path.exists(app_path):
            subprocess.call(["xattr", "-cr", app_path])
            subprocess.call(["codesign", "--force", "--deep", "--sign", "-", app_path])
            print("  🛡️ macOS URY Engine.app ad-hoc 서명 적용 완료!")
    except Exception as e:
        print(f"  ⚠️ 서명 처리 알림: {e}")

    make_zip_archive(MACOS_DIR, mac_zip_path)

    # DMG 빌드 시도 (build_dmg.py 구동)
    dmg_script = os.path.join(ROOT_DIR, "build_dmg.py")
    if os.path.exists(dmg_script):
        try:
            print("🍏 macOS .dmg 디스크 이미지 자동 빌드 중...")
            subprocess.call([sys.executable, dmg_script], cwd=ROOT_DIR)
        except Exception as e:
            print(f"  ⚠️ DMG 빌드 알림: {e}")

    # 3. Windows 전용 빌드 (ZIP)
    print("\n🪟 [3/4] Windows 배포 패키징 중...")
    win_zip_path = os.path.join(DIST_DIR, f"URY_Engine_{VERSION}_Windows.zip")
    make_zip_archive(WIN_DIR, win_zip_path)

    # 4. 결과 리포트
    print("\n=========================================================")
    print("🎉 [완료] macOS & Windows 듀얼 동시 배포 패키지가 생성되었습니다!")
    print(f"📂 [최종 배포 저장소]: {DIST_DIR}")
    print("=========================================================")
    for f in sorted(os.listdir(DIST_DIR)):
        fpath = os.path.join(DIST_DIR, f)
        if os.path.isfile(fpath):
            size_mb = round(os.path.getsize(fpath) / 1024 / 1024, 2)
            print(f"  📦 배포 파일: {f} ({size_mb}MB)")

if __name__ == "__main__":
    build_all_releases()

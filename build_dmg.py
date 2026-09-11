#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URY macOS .dmg Installer Builder
macOS 공식 디스크 이미지(.dmg) 빌드 자동화 스크립트
"""

import os
import shutil
import subprocess
import sys

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    staging_dir = os.path.join(root_dir, 'scratch', 'dmg_staging')
    try:
        import build_release_all
        version = build_release_all.VERSION
    except Exception:
        version = "v0.9.5"
    dmg_out = os.path.join(root_dir, '배포', f'URY_Engine_{version}.dmg')
    os.makedirs(os.path.dirname(dmg_out), exist_ok=True)
    app_src = os.path.join(root_dir, 'URY_macOS', 'URY.app')

    if not os.path.exists(app_src):
        app_src = os.path.join(root_dir, '배포', f'URY_Engine_{version}_macOS', 'URY.app')

    # 이전 빌드 이름도 읽어 기존 배포 폴더를 다시 패키징할 수 있게 한다.
    if not os.path.exists(app_src):
        app_src = os.path.join(root_dir, 'URY_macOS', 'URY Engine.app')

    if not os.path.exists(app_src):
        print(f"❌ 오류: '{app_src}'를 찾을 수 없습니다.")
        sys.exit(1)

    print('📦 [1/4] 스테이징 폴더 초기화 중...')
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    print(f'📂 [2/4] URY.app 복사 중: {app_src}')
    app_dst = os.path.join(staging_dir, 'URY.app')
    subprocess.run(['ditto', app_src, app_dst], check=True)

    # DMG 생성 전에 native recorder 포함 여부 검증
    bundled_recorder = os.path.join(
        app_dst,
        'Contents',
        'Resources',
        'bin',
        'mac_audio_rec'
    )

    if not os.path.isfile(bundled_recorder):
        print(
            "❌ 오류: 앱 번들에 mac_audio_rec가 없습니다:\n"
            f"   {bundled_recorder}"
        )
        sys.exit(1)

    if not os.access(bundled_recorder, os.X_OK):
        print(
            "❌ 오류: mac_audio_rec 실행 권한이 없습니다:\n"
            f"   {bundled_recorder}"
        )
        sys.exit(1)

    print("  ✅ mac_audio_rec 앱 번들 포함 확인")

    # Applications 심볼릭 링크 생성 (드래그 앤 드롭 설치용)
    app_link = os.path.join(staging_dir, 'Applications')
    if not os.path.exists(app_link):
        os.symlink('/Applications', app_link)
    print('🔗 Applications 심볼릭 링크 생성 완료.')

    # 안내 파일 복사 (수동 전체 파이프라인 런처는 배포하지 않음)
    mac_src_dir = os.path.join(root_dir, 'URY_macOS')
    for extra in ['01_macOS_실행하기.command', '설정관리자.command', 'USER_GUIDE.pdf', 'USER_GUIDE.md', '시스템_저장경로_안내.pdf', '시스템_저장경로_안내.md']:
        p = os.path.join(mac_src_dir, extra)
        if not os.path.exists(p):
            p = os.path.join(root_dir, extra)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join(staging_dir, extra))
            if extra.endswith('.command'):
                os.chmod(os.path.join(staging_dir, extra), 0o755)
            print(f'📄 부속 파일 복사: {extra}')
            # 한글 파일명 가이드 '사용설명서.pdf' 추가 생성
            if extra == 'USER_GUIDE.pdf':
                shutil.copy2(p, os.path.join(staging_dir, '사용설명서.pdf'))
                print('📄 부속 파일 복사: 사용설명서.pdf')

    print('🛡️ [3/4] macOS 격리 속성(Quarantine) 제거 및 ad-hoc 코드 서명...')
    subprocess.run(['dot_clean', staging_dir], check=False)
    subprocess.run(['xattr', '-cr', staging_dir], check=False)
    subprocess.run(['xattr', '-cr', app_dst], check=False)
    try:
        subprocess.run(['codesign', '--force', '--deep', '--sign', '-', app_dst], check=True)
    except Exception as e_cs:
        print(f'⚠️ ad-hoc 서명 알림 (건너뜀): {e_cs}')

    print(f'🗜️ [4/4] hdiutil 기반 압축 디스크 이미지(.dmg) 빌드 중...')
    if os.path.exists(dmg_out):
        os.remove(dmg_out)

    cmd = [
        'hdiutil', 'create',
        '-volname', f'URY {version}',
        '-srcfolder', staging_dir,
        '-ov',
        '-format', 'UDZO',
        dmg_out
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        dmg_size_mb = os.path.getsize(dmg_out) / (1024 * 1024)
        print(f'🎉 성공! DMG 설치 파일이 완성되었습니다: {dmg_out} ({dmg_size_mb:.1f} MB)')
    else:
        print(f'❌ DMG 생성 실패: {res.stderr}')
        sys.exit(res.returncode)

if __name__ == '__main__':
    main()

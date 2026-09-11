# URY

대학 강의자료와 녹음을 Gemini로 분석해 강의노트, PDF, 모의시험, 학습 로드맵을 만드는 macOS/Windows 데스크톱 앱입니다.

현재 최신 정식 릴리즈는 macOS v0.9.5입니다. macOS 기능은 마감되었고 Windows 실기기 QA·단독 EXE·설치마법사 배포를 이어서 진행합니다.

## 시작하기

- macOS: [URY_macOS/설정관리자.command](URY_macOS/설정관리자.command)
- Windows: [URY_Windows/01_실행하기.bat](URY_Windows/01_실행하기.bat)
- API 키: 앱의 **Settings** 탭에서 Gemini API 키를 입력하고 저장합니다.

실행 폴더를 옮겨도 해당 폴더를 워크스페이스로 사용합니다. 개인 API 키, 수업 자료, 생성 노트는 Git에 포함되지 않습니다.

## 주요 기능

- Studio에서 과목별 음성 및 선택한 PDF/PPTX 자료를 복수 선택해 강의노트·PDF 생성
- 학기별 과목·기간·튜터 대화 분리
- Tutor 및 Exam 생성
- 429/503 발생 시 다음 Gemini 모델로 전환
- 대학별 HEX 포인트컬러와 실행 창·Dock 아이콘 색상 적용
- AI Notebook 계열 앱을 참고한 고정 사이드바와 자료 중심 Studio 흐름
- GitHub Release 새 버전 확인, 설치 파일 다운로드 및 실행
- Windows 설치마법사 기반 설치·업데이트·삭제 (v0.9.6 CI artifact, 실기기 QA 예정)

## 저장소 구조

```text
URY/
├── URY_macOS/               macOS 실행 스크립트와 시스템 리소스
├── URY_Windows/             Windows 실행 스크립트와 시스템 리소스
├── installer/               Inno Setup 설치마법사 스크립트
├── assets/                  공용 앱 아이콘·User Guide 이미지
├── tests/                   회귀 테스트
├── .github/workflows/       Windows CI 빌드 workflow
├── build_macos_app.py       macOS 앱 빌더
├── build_dmg.py             macOS DMG 패키저
├── build_release_all.py     macOS/소스 ZIP 패키저
└── README.md                프로젝트 안내
```

## 개발 확인

```bash
python3 -m unittest discover -s tests
```

## macOS 앱 빌드

Tk가 포함된 Python 3.13으로 실행합니다. 현재 개발 Mac에서는 아래 명령을 사용합니다.

```bash
/opt/anaconda3/bin/python3 build_macos_app.py
```

스크립트는 프로젝트의 `.venv-macos-build`에 독립된 환경을 만들고,
`requirements-macos-build.txt`의 고정 버전을 설치합니다. Anaconda의 다른 패키지는
포함하지 않습니다. 결과는 `URY_macOS/URY.app`이며 빌드 중간 파일은
`build/macos`에 저장합니다. 환경과 빌드 결과는 Git에서 제외합니다.
현재 빌드는 Apple Silicon용 로컬 테스트 번들(ad-hoc 서명)입니다.
외부 배포용 Developer ID 서명·Apple 공증은 별도 단계입니다.

앱 빌드 후 `python3 build_dmg.py`로 DMG를 만들 수 있습니다.

macOS 배포 전에는 [build_release_all.py](build_release_all.py)를 실행합니다. 이 빌더는 개인 설정과 강의자료를 패키지에 넣지 않으며 원본 폴더도 변경하지 않습니다.

## Windows 빌드 및 설치

Windows EXE와 설치파일은 macOS에서 직접 컴파일하지 않고 GitHub Actions의 `windows-latest` runner에서 생성합니다.

- Workflow: `.github/workflows/windows-build.yml`
- EXE 패키지: `URY_Windows_v0.9.6_onedir`
- 설치파일: `URY_Windows_v0.9.6_setup`
- 설치 스크립트: [installer/URY_v0.9.6.iss](installer/URY_v0.9.6.iss)

설치 위치는 `%LOCALAPPDATA%\Programs\URY`이며, 사용자 학습 데이터는 `%USERPROFILE%\Desktop\URY`에 별도로 보존됩니다. 현재 설치파일은 Windows 실기기에서 설치·업데이트·삭제 회귀시험을 진행하기 전의 검증 후보입니다.

## 안내

- [사용 가이드](USER_GUIDE.md)
- [저장 경로 안내](URY_macOS/시스템_저장경로_안내.md)
- [현재 개발 현황](DEVELOPMENT_STATUS.md)
- [기능 구현 현황](FEATURE_MATRIX.md)
- [승인용 구현 계획](IMPLEMENTATION_PLAN.md)
- [Antigravity 인수인계](GEMINI.md)

강의 자료와 생성물은 개인 학습 목적으로만 사용하세요.

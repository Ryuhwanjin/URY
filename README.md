# URY Engine

대학 강의자료와 녹음을 Gemini로 분석해 강의노트, PDF, 모의시험, 학습 로드맵을 만드는 macOS/Windows 데스크톱 앱입니다.

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
- 대학별 HEX 테마, 라이트/다크 모드, 실행 창 아이콘 색상 적용
- GitHub Release 새 버전 확인

## 저장소 구조

```text
URY_engine/
├── URY_macOS/       macOS 실행 파일과 시스템 리소스
├── URY_Windows/     Windows 실행 파일과 시스템 리소스
├── tests/           회귀 테스트
├── build_release_all.py  안전한 릴리즈 ZIP 패키저
├── build_dmg.py     macOS DMG 패키저
└── README.md
```

## 개발 확인

```bash
python3 -m unittest discover -s tests
```

배포 전에는 [build_release_all.py](build_release_all.py)를 실행합니다. 이 빌더는 개인 설정과 강의자료를 패키지에 넣지 않으며 원본 폴더도 변경하지 않습니다.

## 안내

- [사용 가이드](USER_GUIDE.md)
- [저장 경로 안내](URY_macOS/시스템_저장경로_안내.md)

강의 자료와 생성물은 개인 학습 목적으로만 사용하세요.

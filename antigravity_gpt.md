# URY Engine 배포 전 전략·법적 검토 및 코드 감사 보고서 (antigravity_gpt)

**작성일시**: 2026-09-11  
**작성 주체**: Antigravity (Advanced Agentic Assistant)  
**문서 목적**: URY Engine 정식 배포를 위한 비즈니스/배포 전략, 저작권 및 법적 리스크 분석, 코드베이스 정밀 감사 결과 및 우선 조치 로드맵 기록  

---

## 1. 제품 배포 철학 및 비즈니스 전략

### 1.1 완전 무료 및 무광고 원칙 (100% Free & Ad-free Freeware)
- **결정 배경**: 상업적 유료 판매나 인앱 광고 탑재 시 저작권 분쟁 표적이 되기 쉽고 대학생 커뮤니티(에브리타임 등) 진입 시 반발을 유발함.
- **배포 정책**:
  - 인앱 결제, 유료 구독, 상업적 인앱 광고를 일체 배제한다.
  - 학생들의 순수 학업 증진을 지원하는 비영리 오픈 프리웨어 소프트웨어로 포지셔닝한다.
  - 가벼운 자발적 후원 모델(예: "개발자에게 커피 한 잔 후원하기" 익명 링크)만 선택적으로 제공한다.

### 1.2 BYOK (Bring Your Own Key) 기반 서버 비용 최소화
- **URY 서버 비용 0원 유지**: 중앙 URY 서버를 운영하지 않아 사용자 수에 따른 개발자 인프라 비용이 발생하지 않는다. 단, 사용자가 직접 사용하는 Google API의 쿼터·정책·요금은 별도로 적용된다.
- **무료 배포 원칙**: 학생 각자가 Google AI Studio에서 API Key를 발급해 직접 통신한다. 무료 티어의 한도와 제공 여부는 Google 정책에 따라 달라지므로 영구 무료를 보장하지 않는다.

### 1.3 모바일(iOS/Android) 지원 배제 사유
- **기술적 제약**: 현행 GUI는 데스크톱 전용 `tkinter`로 작성되어 있어 모바일 OS(iOS/Android) 런타임에서 직접 빌드가 불가능함.
- **시스템 종속성**: Chromium 백그라운드 프로세스 기반의 출판용 PDF 렌더링 및 로컬 작업공간(`~/Desktop/URY`) 파일 시스템 제어가 모바일 샌드박스 정책과 상충함.
- **로드맵**: 모바일은 데스크톱 완성 및 안정화 후, 필요 시 웹(PWA)/클라우드 백엔드 또는 Flutter 기반 신규 프로젝트로 별도 검토한다.

### 1.4 버전 정책 (안 B 채택)
- **단계적 릴리즈**:
  1. Windows 실기기 패키징 및 단독 실행(`URY.exe`)·설치마법사·삭제 검증본을 **`v0.9.6`** 배포 후보로 릴리즈.
  2. 실사용자 피드백 및 환경 회귀시험 통과 후 **`v1.0.0` 정식 릴리즈**로 공식 승격.

---

## 2. 저작권법 및 음성 녹음 법적 리스크 분석

### 2.1 법적 쟁점 검토
1. **강의 음성 녹음 (통신비밀보호법 제3조 vs 교수 음성권)**:
   - 통비법은 '타인 간의 대화'를 몰래 감청하는 것을 처벌함. 학생은 강의의 직접 청취 당사자이므로 대법원 판례상 형사상 도청/감청에 해당하지 않음.
   - 단, 사전 동의 없는 무단 녹음본의 외부 유출이나 인터넷 게시 시 민사상 음성권/인격권 침해 및 학칙 위반 책임이 발생함.
2. **강의자료(PPT/PDF) 저작권 (저작권법 제30조 사적이용을 위한 복제)**:
   - 교수의 슬라이드 및 족보는 저작물임.
   - 「저작권법」 제30조에 따라 **"영리를 목적으로 하지 아니하고 개인적으로 이용하거나 가정 및 이에 준하는 한정된 범위"** 내에서 학생 개인이 자기 시험공부를 위해 로컬에서 요약 노트를 생성하는 것은 합법적 사적이용에 해당함.
   - 생성된 노트를 외부에 유출, 판매, 단톡방/에타에 공유하면 저작권법 제136조 위반으로 처벌 대상이 됨.

### 2.2 URY Engine의 위험 완화 요소 (Legal Risk Mitigation)
- **URY 서버 미보관**: 개발사 운영 서버에는 사용자 자료를 저장하지 않는다. 다만 선택한 강의자료·음성은 사용자의 Gemini API Key를 통해 Google API로 전송될 수 있으며, 해당 서비스의 약관·보존정책이 적용된다.
- **로컬 도구 구조**: 생성 파일과 설정은 사용자 워크스페이스에 저장되며, 앱에 외부 공유 기능을 추가하지 않는다. 이는 위험을 줄이는 설계일 뿐 법적 책임을 면제하지 않는다.
- **사용자 고지**: 교수자 동의, 개인 학습 범위, 외부 배포 금지, 학교 규정 준수를 첫 실행 약관과 `Terms & Ethics`에 명시한다.

---

## 3. 코드베이스 정밀 감사 결과 및 문제점

### 🚨 [치명적] 1. Windows 배포본에 `URY.exe` 부재 (Python 미설치자 구동 불가)
- **현상**: `build_release_all.py`가 생성하는 `URY_Engine_Windows.zip`에 실행 바이너리가 없고, 소스코드와 `01_실행하기.bat`만 포함됨.
- **영향**: 일반 학생 PC에 Python이 없으면 `01_실행하기.bat` 실행 시 프로그램이 뜨지 않고 Python 공식 웹사이트로 튕김.
- **조치 필요**: PyInstaller 단독 실행형 `URY.exe` 및 의존 라이브러리 번들(`_internal`)을 포함한 완성형 패키지 또는 설치 마법사(Inno Setup 등)를 빌드하여 배포해야 함.

### 🚨 [위험] 2. `04_완전삭제.bat`의 사용자 학습 데이터 강제 삭제 위험
- **현상**: Python이 설치되지 않은 환경(`:NO_PY`)에서 `04_완전삭제.bat` 실행 시:
  ```bat
  if exist "%USERPROFILE%\Desktop\URY" rmdir /s /q "%USERPROFILE%\Desktop\URY"
  ```
  위 명령어가 아무런 확인(Y/N) 없이 즉각 실행됨.
- **영향**: 사용자의 기본 작업공간(`~/Desktop/URY`)에 저장된 **한 학기 전체 강의자료, 시간표, 녹음본, 생성 노트가 일순간에 영구 삭제**되는 참사가 일어날 수 있음.
- **조치 필요**: 삭제 전 대화형 확인(Y/N)을 반드시 거치게 하고, "프로그램 실행 파일만 삭제"와 "사용자 학습 데이터까지 완전 삭제"를 명확히 분리해야 함.

### ⚠️ [개선] 3. Windows 배치 파일 한글 깨짐 및 구버전(v0.6.5, v0.7.7) 방치
- **현상**:
  - `01_실행하기.bat` ~ `04_완전삭제.bat`에 `@chcp 65001 >nul` 선언이 없어 기본 콘솔(CP949)에서 한글 안내가 깨져서 출력됨 (`[] ̽(Python) PC ġǾ  ʽϴ!`).
  - 배치 파일 제목과 배너가 `v0.6.5`, `build_exe_gui.py`와 `uninstall_gui.py`는 `v0.7.7`로 수개월 전 구버전 명칭이 남아 있음.
- **조치 필요**: 배치 파일 상단에 UTF-8 코드페이지 선언을 추가하고 버전 표기를 일괄 동기화해야 함.

### ⚠️ [법적 보완] 4. 생성된 PDF 산출물 내 법적 면책 푸터 부재
- **현상**: `settings_gui.py`의 최초 실행 서약은 훌륭히 작동하나, 실제 발행되는 PDF 본문 하단에는 면책 문구가 없음.
- **조치 필요**: `generate_pdfs.py` HTML/CSS 조판 엔진에 아래와 같은 사적이용 명시 푸터를 자동 삽입하여 외부 유출 시 법적 책임을 명확히 함:
  > *"본 문서는 URY Engine을 통해 개인 학습(저작권법 제30조 사적이용) 목적으로 생성되었으며, 저작권자의 허가 없는 무단 복제·전재·배포·공유를 엄금합니다."*

### ✅ [우수] 확인된 안전 요소
1. **API Key 보안**: 커밋 이력 및 소스코드 내 API Key 누출 0건, `studio_latest.log` 마스킹 완벽, `.env` 및 `settings.json` 배포 제외 필터 정상 작동.
2. **첫 실행 서약 강제**: `settings_gui.py`에서 저작권법 준수 및 학업 윤리 서약 미동의 시 프로그램 강제 종료 처리.
3. **Chromium 브라우저 자동 탐색**: Windows/macOS의 다양한 브라우저(Chrome, Edge, Whale, Brave) 경로 탐색 정상.

---

## 4. 우선 조치 로드맵 (Action Plan)

1. **[P0] `04_완전삭제.bat` 안전장치 패치**:
   - 일방적 데이터 삭제 로직 제거, [1] 프로그램만 삭제 / [2] 학습 데이터 포함 완전 삭제 선택 프롬프트 추가.
2. **[P0] 배치 파일 인코딩 및 버전 동기화**:
   - `@chcp 65001 >nul` 추가 및 버전 표기 최신화.
3. **[P1] PDF 템플릿에 사용 범위 고지 추가 검토**:
   - `generate_pdfs.py`에 개인 학습용·무단 배포 금지 안내를 넣을 수 있으나, 문구 자체가 법적 면책을 보장하지는 않는다.
4. **[P1] Windows Phase 3 (`URY.exe`) 독립 실행 빌드 환경 점검**:
   - Python 미설치 환경에서도 더블클릭으로 즉시 실행되는 `URY.exe` 패키징 구축 (`v0.9.6`).

---

## 5. Codex 협의 사항 및 Windows 분리 개발 전략

### 5.0 역할 분담 및 최종 결정권

- **GPT(Codex)**: 구현 방향, 코드 수정, 테스트 결과 판단, 브랜치 병합, 버전업·릴리즈의 최종 결정 담당.
- **Antigravity**: 독립적인 코드 더블체크, 잠재 버그·보안·배포 위험 지적, 대안 및 추가 아이디어 제안 담당.
- Antigravity의 의견은 검토 자료로 사용하며, GPT(Codex)의 최종 판단 없이 코드 병합·릴리즈·삭제 작업을 진행하지 않는다.
- 의견이 충돌하면 `AGENTS.md`와 세 상태 문서의 기준을 우선 확인하고, 최종 선택은 GPT(Codex)가 기록한다.

### 5.1 현재 기준선

- macOS는 `v0.9.5`에서 기능 마감 및 정식 릴리즈를 완료했다. 기존 macOS 릴리즈 기준선을 Windows 개발 중 직접 수정하지 않는다.
- 저장소: `https://github.com/Ryuhwanjin/URY.git`, 기준 브랜치: `main`.
- 사용자 작업공간은 `~/Desktop/URY`이며, 시간표·강의자료·녹음·생성 노트·로컬 테스트 파일은 Git에 포함하지 않는다.
- `URY_macOS/system/code/`와 `URY_Windows/system/code/`의 대응 공용 Python 파일은 현재 동일한 내용으로 유지되고 있다. Windows 작업 때문에 macOS 파일을 임의로 분기하거나 덮어쓰지 않는다.

### 5.2 권장 작업 방식

Windows 개발은 macOS 코드의 별도 복사본을 새 프로젝트로 영구 분리하는 대신, 현재 기준선에서 Windows 전용 Git worktree/브랜치를 만든다.

```bash
cd /Users/ryuhwanjin/Documents/ChatGPT/URY_Project_git
git fetch origin
git worktree add ../URY_windows_phase3 -b windows/phase3 origin/main
```

- `URY_Project_git/`은 macOS 기준선 확인용으로 보존한다.
- `URY_windows_phase3/`에서 `URY_Windows/**`를 중심으로 UI·경로·배치 파일·PyInstaller·설치마법사를 수정한다.
- 공용 로직을 수정해야 할 때는 macOS·Windows 양쪽에 같은 변경을 반영하고, 파일 비교·AST·전체 테스트를 통과시킨 뒤 병합한다.
- Windows 작업은 Windows 실기기에서만 최종 동작을 판단하며, macOS 릴리즈 빌드는 공용 코드 변경이 있을 때만 다시 만든다.

### 5.3 Windows 완료 순서

1. Settings·Studio·Quiz & Exam·Tutor·Updates의 Windows 실기기 회귀시험
2. Python 미설치·한글/공백 경로를 포함한 단독 `URY.exe` 빌드
3. 배치 파일 UTF-8 코드페이지 및 버전 표기 정리
4. 프로그램만 삭제 / 사용자 학습 데이터 포함 삭제를 분리한 안전한 제거 흐름
5. 설치마법사 기반 설치·업데이트·완전삭제 검증
6. 검증본 `v0.9.6` 릴리즈 후 실사용 피드백을 반영하고 `v1.0.0` 승격 검토

### 5.4 Antigravity 인수인계 프롬프트

Antigravity에서 저장소를 열면 첫 메시지로 아래 내용을 전달한다.

```text
이 저장소의 작업을 시작한다.
먼저 AGENTS.md, DEVELOPMENT_STATUS.md, FEATURE_MATRIX.md,
IMPLEMENTATION_PLAN.md, GEMINI.md, antigravity_gpt.md를 순서대로 읽어라.

macOS v0.9.5는 기준선으로 보존하고, Windows Phase 3만 진행한다.
작업 전 git status를 확인하고 사용자 시간표·강의자료·생성 노트·임시 파일은
삭제하거나 커밋하지 마라. Windows 전용 변경은 URY_Windows 안에서 우선 처리하고,
공용 Python 변경이 필요하면 macOS·Windows 양쪽을 동일하게 수정한 뒤 테스트하라.
작업 시작·중단·완료 시 DEVELOPMENT_STATUS.md를 갱신하고,
기능/계획 변경 시 FEATURE_MATRIX.md와 IMPLEMENTATION_PLAN.md도 갱신하라.
```

Antigravity 개발 도구에서 모델을 선택하는 것과 URY 앱 내부 Gemini API를 바꾸는 것은 별개다. 현재 URY 앱은 표준 Gemini 생성 API를 사용하므로, 앱 자체를 Antigravity Agent API로 전환하는 작업은 Windows 안정화 이후 별도 승인 사항으로 둔다.

---

## 6. Antigravity의 윈도우 빌드 및 macOS 보완에 관한 기술 의견 (Technical Opinion)

### 6.1 윈도우 빌드의 핵심 현실: "Mac에서는 윈도우 EXE를 크로스 컴파일할 수 없다"
- Python의 PyInstaller는 운영체제 간 크로스 컴파일을 지원하지 않습니다.
- 따라서 현재의 macOS(Apple Silicon) 환경에서는 윈도우용 바이너리(`URY.exe`, `.dll`)를 직접 빌드할 수 없으며, 기존 `build_release_all.py`가 생성하던 `URY_Engine_Windows.zip`이 단순 파이썬 스크립트 모음이었던 이유가 바로 여기에 있습니다.

### 6.2 윈도우 독립 실행 바이너리 제작을 위한 2가지 해결 경로
1. **방안 A: GitHub Actions CI/CD 자동 빌드 워크플로우 구축 (강력 추천 ⭐⭐⭐)**:
   - `.github/workflows/build_windows.yml`을 작성하여 GitHub 무료 윈도우 가상머신(`windows-latest`)을 활용.
   - Git Push 또는 Release Tag 생성 시 윈도우 클린 환경에서:
     `Python 세팅` $\rightarrow$ `pip install` $\rightarrow$ `PyInstaller 컴파일` $\rightarrow$ `Inno Setup 설치파일 생성` $\rightarrow$ `GitHub Releases에 URY_Setup_v0.9.6.exe 자동 첨부`.
   - **장점**: 개발자가 윈도우 PC를 소유하고 있지 않거나 켜지 않아도 Mac에서 완벽한 윈도우용 바이너리와 설치마법사를 무결하게 생산 가능.
2. **방안 B: 윈도우 실기기 / 가상머신(Parallels) 로컬 빌드**:
   - 실제 윈도우 머신에서 코드를 체크아웃하고 `03_단독EXE빌드.bat` 및 `build_exe_gui.py`를 실행하여 빌드 산출물(`dist/URY`)을 생성한 뒤 수동 업로드.

### 6.3 윈도우 패키징 구조: `--onedir` + Inno Setup 설치 마법사 결합
- **`--onedir` 유지 필수**: 단일 실행파일(`--onefile`)은 구동 시마다 `%TEMP%`에 수백 MB를 압축 해제하므로 부팅이 5~10초 지연되고 백신(Defender/알약/V3) 오진율이 매우 높습니다. 따라서 즉시 구동되는 `--onedir`(`URY.exe` + `_internal/`) 구조를 유지해야 합니다.
- **Inno Setup 마법사 (`URY_Setup_v0.9.6.exe`) 필수**: 학생에게 복잡한 내부 파일들이 노출되지 않도록 표준 설치 마법사로 패키징하여, 바탕화면/시작메뉴 바로가기 등록 및 제어판을 통한 클린 삭제를 지원해야 합니다.

### 6.4 Windows SmartScreen 보안 경고 대응
- 코드서명 인증서(EV/OV)가 없는 비영리 무료 배포본 특성상 Windows Defender SmartScreen 파란 경고가 발생할 수 있습니다.
- 사용자 가이드(User Guide / README)에 파일 출처·SHA-256 확인과 Windows의 공식 수동 확인 절차를 안내합니다. 보안을 약화하는 자동 우회 배치 파일은 동봉하지 않습니다.

### 6.5 macOS 버전 필수 패치 3건 (병행 권장)
1. `build_macos_app.py`: `Info.plist`에 `NSMicrophoneUsageDescription` 추가 (최신 macOS 마이크 권한 요청 시 TCC 크래시 방지).
2. `보안경고_자동해제.command`: 현재 파일 위치가 `URY_Windows`이고 macOS용 셸 스크립트이므로, macOS 배포에 포함할지와 경로를 먼저 정리한다. 임의의 경로 변경은 보류한다.
3. `build_dmg.py`: 제외 기능인 `파이프라인_실행.command`를 DMG 패키지 복사 목록에서 제거.

---

## 7. GPT(Codex) 최종 검토 및 채택 결정

이 절은 Antigravity의 감사·제안 내용을 GPT(Codex)가 검토한 최종 결정 기록이다. Antigravity 문서의 제안은 이 절에서 채택한 범위만 구현 기준으로 사용한다.

### 7.1 채택하는 방향

- macOS `v0.9.5`를 기준선으로 고정하고, Windows 작업은 `windows/phase3` 전용 브랜치/worktree에서 진행한다.
- GitHub Actions의 Windows runner를 빌드 자동화 수단으로 사용한다. 단, 실제 Windows 또는 VM의 설치·실행·업데이트·삭제 회귀시험을 대체하지 않는다.
- PyInstaller `--onedir` 출력과 Inno Setup 설치마법사를 결합해 `URY.exe` 설치 패키지를 만든다.
- `v0.9.6`은 Windows 검증 후보 릴리즈로 사용하고, 실사용 피드백까지 통과한 뒤 `v1.0.0` 승격을 검토한다.
- Windows 배포 전 `04_완전삭제.bat`의 프로그램 삭제와 사용자 학습 데이터 삭제를 분리하고, 데이터 삭제에는 명시적 확인을 둔다.

### 7.2 반려·수정하는 내용

- SmartScreen을 자동으로 우회하는 배치 파일은 배포하지 않는다. 체크섬·출처·수동 확인 절차만 안내한다.
- “법적 리스크 원천 차단”, “사적 이용이 합법”처럼 단정하는 문구는 사용하지 않는다. URY 서버에는 저장하지 않더라도 선택 자료는 Google API로 전송될 수 있으며, 해당 서비스 정책과 학교 규정을 따른다.
- `보안경고_자동해제.command`는 현재 `URY_Windows` 아래에 있는 macOS용 스크립트이므로, 문서의 macOS 패치 대상으로 그대로 적용하지 않는다. 실제 위치·배포 필요성을 먼저 정리한다.
- `--onefile`의 지연 시간·백신 오진 수치를 고정된 보장처럼 쓰지 않는다. `--onedir`를 기본으로 선택하되 실제 Windows 환경에서 비교 검증한다.

### 7.3 다음 구현 전 확인할 잔여 항목

- `build_macos_app.py`의 아이콘 여백 상수는 현재 12%이므로, 이전에 합의한 8% 적용 여부를 별도 확인한다.
- `build_dmg.py`가 제외 기능인 `파이프라인_실행.command`를 복사하는지 정리한다.
- Windows 배치 파일의 구버전 표기·UTF-8 코드페이지와 `04_완전삭제.bat`의 즉시 삭제 로직을 Windows 릴리즈 전에 수정한다.

최종 구현·검증·병합·릴리즈 판단은 GPT(Codex)가 담당하며, Antigravity는 이후에도 독립적인 더블체크와 아이디어 제안 역할로 사용한다.

---

## 8. Windows Phase 3 (`windows/phase3`, `0c83ec4` ~ `a289d23`) Antigravity 코드 리뷰 보고서

**검토 대상**: `/Users/ryuhwanjin/Documents/ChatGPT/URY_windows_phase3` (Worktree)
**검토 브랜치**: `windows/phase3` (`a289d23`, 기준: `0c83ec4`)
**작성 주체**: Antigravity (독립 더블체커 / 코드 미수정 리뷰 전담)

---

### 8.1 즉시 수정이 필요한 문제 (P0)

#### 1) `config_manager.py`: Windows 배포 바이너리 환경에서 번들 설정 파일 탐색 경로 누락
- **대상 파일**: `URY_Windows/system/code/config_manager.py` (라인 121~127)
- **현상 및 근거**:
  ```python
  if getattr(sys, "frozen", False):
      app_dir = os.path.dirname(os.path.abspath(sys.executable))
      for sub in ("../Resources/system", "../Frameworks/system", "../Resources", "../Frameworks"):
          res_p = os.path.abspath(os.path.join(app_dir, sub, filename))
          if os.path.exists(res_p):
              return res_p
  ```
  현재 `find_config_file()`은 실행 파일이 패키징된(`frozen=True`) 상태일 때 macOS `.app` 번들 전용 상대경로(`../Resources/...`)만 검사하고 있습니다.
  PyInstaller `--onedir`로 빌드된 Windows 환경(`dist/URY/URY.exe`)에서는 번들된 리소스 파일이 `_internal/system` 또는 `sys._MEIPASS/system`에 위치합니다.
- **위험성**: Windows 독립 실행본(`URY.exe`)을 클린 환경에서 최초 구동할 때, 번들된 기본 설정(`settings.default.json` 등)을 찾지 못해 초기화 오류가 발생할 수 있습니다.
- **조치 방안**:
  `find_config_file()`의 `sub` 탐색 목록에 `_internal/system`, `_internal`, `system`을 추가하거나 `getattr(sys, "_MEIPASS", "")` 경로를 포함하도록 보강해야 합니다.

---

### 8.2 출시 전 확인할 문제 (P1)

#### 1) GitHub Actions 빌드 워크플로우에 `--icon` 옵션 누락
- **대상 파일**: `.github/workflows/windows-build.yml` (라인 33~50)
- **현상 및 근거**:
  `windows-build.yml`의 PyInstaller 명령어에 `--icon` 옵션이 누락되어 있습니다. 리포지토리 루트 및 `URY_Windows/`에 `app_icon.ico`가 준비되어 있음에도 이를 지정하지 않았습니다.
- **위험성**: GitHub Actions로 빌드된 `URY.exe`가 탐색기에서 URY 전용 아이콘 대신 PyInstaller 기본 아이콘으로 표시됩니다.
- **조치 방안**: PyInstaller 인자에 `--icon app_icon.ico` (또는 `--icon URY_Windows/app_icon.ico`)를 추가합니다.

#### 2) `build_exe_gui.py`의 독립 실행 시 아이콘 경로 불일치 가능성
- **대상 파일**: `URY_Windows/system/code/build_exe_gui.py` (라인 47~54)
- **현상 및 근거**:
  `assets_dir = os.path.abspath(os.path.join(root_dir, "..", "assets"))`로 상위 폴더를 참조하므로, 사용자가 배포된 `URY_Windows` 폴더만 독립적으로 압축 해제하여 실행할 경우 `../assets`가 존재하지 않아 `build/ury_engine_icon.ico` 생성이 실패하고 `--icon` 옵션이 빠진 채 빌드됩니다.
- **조치 방안**: `URY_Windows/app_icon.ico`가 이미 존재하므로, 변환 실패 시 기존 `app_icon.ico`를 직접 참조하도록 fallback을 둡니다.

#### 3) `uninstall_gui.py`의 macOS/Windows 공용 동기화 불일치
- **대상 파일**: `URY_Windows/system/code/uninstall_gui.py` vs `URY_macOS/system/code/uninstall_gui.py`
- **현상 및 근거**:
  `0c83ec4` 커밋에서 `URY_Windows` 측의 `uninstall_gui.py`만 `v0.9.6`과 `URY.Uninstaller.v096`으로 변경되었고, `URY_macOS` 측은 `v0.7.7`로 남아 있어 공용 17개 파일 중 이 파일 1개가 4라인 차이를 보입니다.
- **조치 방안**: "공용 파일 양쪽 동기화" 작업 규칙을 준수하기 위해 `URY_macOS/system/code/uninstall_gui.py`도 동일하게 갱신합니다.

#### 4) Inno Setup 패키징 시 권한 및 설치 경로 권장
- **대상 파일**: 향후 생성될 Inno Setup 스크립트 (`*.iss`)
- **판단 근거**:
  기본 설치 경로를 `C:\Program Files\URY`(`{autopf}\URY`)로 잡으면, 관리자 권한이 없는 대학교 도서관/실습실 PC나 공용 PC에서 설치 시 UAC 차단이 발생합니다.
- **조치 방안**: `{localappdata}\Programs\URY`를 기본 설치 경로(`PrivilegesRequired=lowest`)로 지정하여 일반 사용자 권한으로 원클릭 설치되도록 구성을 권장합니다.

---

### 8.3 개선 제안 (P2)

#### 1) 배치 파일 6개의 Python 3.13 경로 탐색 보강
- **대상 파일**: `URY_Windows/*.bat` 6종
- **현상 및 근거**:
  배치 파일의 `for %%P` 루프가 Python 3.12, 3.11, 3.10만 하드코딩 검사하고 있습니다. Python 3.13 사용자의 경우 `where python` fallback으로 잡히기는 하나, 직접 설치 경로 탐색에 `Python313`도 포함해 주면 진입 성공률이 높아집니다.

#### 2) GitHub Actions에 초간단 무결성 스모크 테스트 단계 추가
- **대상 파일**: `.github/workflows/windows-build.yml`
- **현상 및 근거**:
  현재는 `Test-Path $exe`로 파일 존재 여부만 검사하고 있습니다. `settings_gui.py`에 `--smoke-test` 인자를 지원하게 하고, CI 상에서 `& dist/URY/URY.exe --smoke-test`를 1회 실행하여 DLL 누락이나 모듈 임포트 에러가 없는지 런타임 검증을 통과하도록 하면 더욱 견고해집니다.

---

### 8.4 현재 상태에서 승인 가능한 부분 (합격 요소)

1. **배치 파일 6종 UTF-8 코드페이지 및 안정성 (100% 합격)**:
   - 모든 배치 파일 상단에 `@echo off`, `@chcp 65001 >nul`, `setlocal`, `cd /d "%~dp0"`이 누락 없이 적용되었습니다.
   - 메시지가 표준 영문 ASCII(`[OK]`, `[RUN]`, `[ERROR]`)로 정돈되어 한글 Windows(CP949) 및 영문 Windows 콘솔 어디서든 깨짐이 원천 차단되었습니다.
2. **Python 미설치 시 사용자 데이터 삭제 방지 (100% 합격)**:
   - `04_완전삭제.bat`의 `:NO_PY` 분기에서 위험했던 `rmdir /s /q "%USERPROFILE%\Desktop\URY"`가 완전히 제거되었습니다.
   - `test_removed_features.py`의 `test_windows_uninstaller_does_not_delete_workspace_without_python` 회귀 테스트로 영구 보호를 보장하고 있습니다.
3. **`build_exe_gui.py` 컴파일 실패 감지 (합격)**:
   - `if res.returncode != 0:` 검증이 추가되어 PyInstaller 실패 시 오류 로그가 정상적으로 예외 처리됩니다.
4. **`파이프라인_실행.bat` 폐기 안내 처리 (합격)**:
   - 제외된 레거시 기능 실행을 막고 Studio 탭 사용을 안내하는 차단문구로 안전하게 교체되었습니다.

---

### 8.5 실제 Windows 기기에서 반드시 확인해야 할 수동 테스트 항목

1. **High-DPI 디스플레이 스케일링 (125%, 150%) 확인**:
   - `SetProcessDpiAwareness(2)` 호출 시 윈도우 노트북 배율(125%/150%)에서 폰트 및 라운드 카드가 흐려지지 않고 선명하게 렌더링되는지 확인.
2. **Microsoft Edge 기반 Headless PDF 인쇄**:
   - `find_chromium_browser()`가 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`를 정상 감지하고, 실제 강의노트 Markdown을 고품질 PDF로 변환하는지 확인.
3. **한글 사용자명 경로 (`%USERPROFILE%`) 시험**:
   - 윈도우 계정명이 한글(예: `C:\Users\홍길동`)인 환경에서 `~/Desktop/URY` 워크스페이스 생성 및 파일 저장이 인코딩 에러 없이 동작하는지 확인.
4. **Windows Defender SmartScreen 경고 확인**:
   - 빌드된 `URY.exe` 최초 실행 시 나타나는 "Windows의 PC 보호" 창에서 `[추가 정보] → [실행]`을 눌렀을 때 정상 실행되는지 확인.

---

### 8.6 GPT(Codex) 다음 실행 권장 명령어

```bash
# 1. 작업 브랜치 확인
cd /Users/ryuhwanjin/Documents/ChatGPT/URY_windows_phase3
git branch --show-current
git status --short

# 2. 테스트 스위트 확인 (정적 검증)
python3 -B -m unittest discover -s tests

# 3. P0/P1 수정 후 diff 검증
git diff --check

# 4. GitHub Actions 워크플로우 테스트 트리거 (원격 푸시)
git add URY_Windows/system/code/config_manager.py .github/workflows/windows-build.yml
git commit -m "fix(windows): add frozen resource path and embed icon in CI build"
git push origin windows/phase3
```

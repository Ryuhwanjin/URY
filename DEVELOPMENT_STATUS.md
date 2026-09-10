# URY Engine 개발 현황

마지막 갱신: 2026-09-10

## 진행 중

- 최종 배포 점검 중: v0.9.1 DMG·릴리즈 준비 완료(로컬). v0.9.2에는 단일 후속 기능으로 수동 API 재확인과 Dock 아이콘 안전 여백 12% 조정을 반영할 예정. 다음 명령: 의도한 파일만 스테이징하고 커밋·푸시·태그
- Phase 1 진행: 모델 라우팅·영구 Studio 로그 반영 완료, 다음은 실제 429/503 API 회귀시험과 동일 파일 업로드 캐시
- 사용자 승인 대기: `IMPLEMENTATION_PLAN.md`의 Phase 1~5 범위와 우선순위
- Command 단축키 사용자 확인 대기: macOS Cocoa Edit 메뉴와 입력 위젯 클래스 바인딩을 함께 적용한 최신 `URY.app`을 실행해 둠. `⌘C/V/X/A`를 Studio·Tutor·Settings 입력창에서 직접 확인하면 됨

## 최근 완료

- API 연결 배지 검증 보강: 임의의 10자 문자열을 `연결됨`으로 표시하지 않고 `/v1beta/models`에서 `generateContent` 권한을 실제 확인. 정상·백업 준비·인증 실패·네트워크 확인 불가를 구분하고, 셸에 남은 폐기 키가 설정값을 가리지 않도록 공용 로더도 수정. 양 플랫폼 동기화, 테스트 34개 통과(1개 환경 의존 제외), 최신 `URY.app` 재빌드·서명·GUI smoke test 완료
- v0.9.1 배포 후보 점검 완료: 34개 테스트 통과(1개 환경 의존 제외), AST·공용 코드 동기화·diff·비밀값 검사 통과. `URY.app` CFBundle 0.9.1, ad-hoc 서명·`GUI_SMOKE_OK` 통과. `배포/URY_Engine_v0.9.1.dmg`(약 62.8MB) 마운트·앱 smoke test 및 SHA-256 확인. macOS/Windows ZIP에서 `.env`·설정·시간표·생성 이력 제외를 재검증
- API 키 연결 실사용 점검 완료: Desktop 워크스페이스에서 Primary·Backup 설정을 모두 읽고 `/v1beta/models` 인증 및 `generateContent` 모델 목록 응답을 확인. 셸에 남은 폐기 환경변수가 정상 설정을 가리지 않도록 macOS·Windows 공용 로더 수정, 테스트 33개 통과(1개 환경 의존 제외), 최신 `URY.app` 재빌드·서명·GUI smoke test 완료
- Gemini 모델 자동 우선순위 반영: `/v1beta/models`의 `generateContent` 지원 Stable Flash/Flash-Lite를 용도별로 필터링하고 버전 점수 내림차순으로 정렬. 새 Stable 모델이 추가되면 코드 수정 없이 최신 후보가 먼저 사용되며, `gemini-3-flash-preview`는 Preview 안전망으로만 기록. 양 플랫폼 동기화, 테스트 33개 통과(1개 환경 의존 제외), 최신 `URY.app` 재빌드·ad-hoc 서명·GUI smoke test 완료
- 모델 라우팅 수정 최종 반영: Gemini API 모델 목록에서 종료된 1.5/2.0과 Live·TTS·이미지·Embedding 전용 모델을 일반 생성 후보에서 제외하고, 3.8/3.7/3.6/3.5 Stable Flash → 2.5 Flash 순으로 정렬
- Free tier 실사용 쿼터 대응: 3.8 Flash처럼 RPD가 소진된 모델의 429도 강의노트 생성 전체 중단 대신 다음 안정형 Flash 모델로 즉시 전환하도록 macOS·Windows 스트리밍 경로를 보강
- 백업 API 키 지원 완료: Settings에 선택적 `Backup Key`를 추가하고 `.env`·설정 저장, Tutor·강의노트·모의시험·정리노트·마스터 바이블의 쿼터/서버 제한 fallback을 macOS·Windows에 동기화. 강의노트 파일 입력은 백업 프로젝트에 재업로드. 테스트 31개 통과(1개 환경 의존 제외), 최신 `URY.app` 재빌드·ad-hoc 서명 검증 완료
- 기능별 Gemini 모델 풀 연결 완료: Tutor는 3.5/3.1/2.5 Flash-Lite, 강의노트는 3.8/3.7/3.6/3.5/2.5 Flash, 모의시험·치트시트·마스터 바이블은 비-Lite 안정형 Flash를 우선 사용. API 키/프로젝트 전체 쿼터는 공유될 수 있어 429가 완전히 사라지는 것은 아니며 실제 쿼터 회귀시험 필요
- 안정형 모델 풀 정리 및 macOS 재빌드 완료: `gemini-flash-latest`·`gemini-flash-lite-latest` 별칭과 Live·TTS·이미지·Embedding 전용 모델을 일반 생성 후보에서 제거하고, 공식 Stable ID(3.8/3.7/3.6/3.5 Flash, 3.5/3.1/2.5 Flash-Lite)로 교체. 전체 테스트 28개 통과(1개 환경 의존 제외), 공용 코드 동기화·AST·diff 검증 및 `URY.app` 서명·LaunchServices smoke test 통과
- 기능별 모델 라우팅 포함 macOS 앱 재빌드 완료: 전체 테스트 28개 통과(1개 환경 의존 제외), macOS·Windows 공용 코드 AST/동기화·diff 검증, `URY.app` ad-hoc 서명 및 LaunchServices `--smoke-test` 통과. Tutor는 Flash-Lite, 강의노트는 일반 Flash, 시험자료는 비-Lite 안정형 Flash만 우선 사용
- Studio 영구 로그 반영: macOS·Windows 공용 생성 코드가 `system/logs/studio_latest.log`에 실행 시작·단계·모델·수신 글자 수·완료 상태를 기록하며, 저장 실패가 생성 작업을 막지 않도록 처리
- Studio 로그 smoke test 및 공용 코드 구문 검증 완료: 임시 워크스페이스 기록·API Key 비기록 확인, macOS·Windows 파일 동기화 확인, 전체 테스트 27개 통과(1개 환경 의존 제외)
- Studio UI에 `로그 파일 열기` 버튼 추가: macOS 기본 텍스트 편집기와 Windows 기본 연결 프로그램을 사용하며, 로그가 없으면 안내 파일을 먼저 생성
- User Guide 실제 화면 반영: 개인정보가 없는 `Sample Course` 임시 워크스페이스에서 Studio·Quiz & Exam·Tutor·Settings·Updates 화면을 창 단위로 캡처하고 `assets/user_guide/`에 5장 추가함. API Key 입력란은 빈 상태로 캡처했으며 파일명·과목명은 샘플 데이터만 포함
- User Guide 요구사항 보강: 첫 페이지를 `MUST READ`로 고정하고 API Key 발급 절차·초기 설정 순서·워크스페이스 데이터 공유/학기 분리 정책을 명시. Studio 실시간 녹음·강의자료 복수 선택, Quiz·Tutor·Settings·Updates의 전체 기능 설명과 스크롤 가능한 상세 본문을 macOS·Windows에 동기화하고 테스트 27개 통과
- User Guide 반영 앱 재빌드: 최신 `URY.app`에 상세 안내 코드와 5개 화면 캡처 리소스를 포함하고 PyInstaller smoke test·ad-hoc 서명 검증 완료. 정적 `URY_macOS/USER_GUIDE.md`·`URY_Windows/USER_GUIDE.md`도 v0.9.0 기준으로 동기화
- User Guide 가독성 개선 완료: 스크린샷 표시 상한을 1200×500으로 확대하고 원본 1600×996 해상도를 유지. MUST READ·Terms & Ethics는 이미지 없이 설명을 상단에 배치하고 본문 글꼴을 12pt·스크롤 영역으로 조정. macOS·Windows 동기화 및 전체 테스트 27개 통과
- 복사·붙여넣기 단축키 보정 완료: macOS Command, Windows/Linux Control을 Entry·TEntry·Text에 명시하고 중복 실행 방지 처리. macOS 아이콘 가장자리 여백을 8%로 변경해 `URY.app` 재빌드·smoke test·서명 검증 완료
- Tutor 입력 커서 가독성 보정 완료: 입력창에 포인트 색상 커서·2px 두께·700/350ms 점멸을 적용하고 macOS·Windows 코드를 동기화. 최신 `URY.app` 재빌드·서명 검증 및 전체 테스트 27개 통과(1개 환경 의존 제외)
- Command 단축키 충돌 수정 완료: `bind_class`·state-mask fallback을 제거하고 기본 Tk 위젯 동작을 유지하는 단일 `bind_all` 처리로 Command/Meta(Control) 단축키를 정리. macOS·Windows 코드 동기화 및 전체 테스트 27개 통과(1개 환경 의존 제외)
- Command-A 선택 보정 완료: Entry·Text·Combobox·Spinbox 클래스에서 전체 선택을 우선 처리하도록 추가하고 최신 `URY.app` 재빌드·서명 검증 완료
- Command-A TEntry fallback 보정 완료: ttk 입력창에서 `selection_range()`를 사용하도록 보강하고 macOS·Windows 코드 동기화, 전체 테스트 27개 통과 및 최신 `URY.app` 재빌드·서명 검증 완료
- macOS Command 단축키 네이티브 메뉴 보강 완료: `Copy`·`Paste`·`Cut`·`Select All`을 Cocoa Edit 메뉴의 first-responder 액션으로 등록하고 Tk 입력 위젯 클래스 바인딩을 앞단에 배치해 모든 입력 탭에서 `⌘C/V/X/A`가 동일하게 동작하도록 보강. macOS·Windows 소스 동기화, 실제 Tk 입력 위젯 A/C/X/V 이벤트 smoke test, 테스트 27개(1개 환경 의존 제외), AST·diff 검증, 새 앱 코드 서명 및 LaunchServices GUI 스모크 테스트 통과
- Command-F/F11 전역 입력 보정 완료: 포커스가 하위 탭에 있어도 전체 앱에서 fullscreen 단축키가 동작하도록 `bind_all`로 통일하고 중복 토글을 제거. 최신 `URY.app` 재빌드·서명 검증 완료
- macOS `⌘` 입력 보정 후속 완료: Command/Meta KeyPress 별칭, TCombobox·Spinbox 포함 입력 위젯, 커스텀 위젯용 KeyPress fallback을 추가. macOS·Windows 코드 동기화 및 전체 테스트 27개 통과
- User Guide 번들 검증: macOS `.app` 재빌드 후 `Contents/Resources/assets/user_guide/`에 5개 PNG(1600×996)가 포함되고 ad-hoc 코드 서명 검증 통과. 호스트 `screencapture -l <windowID>`로 앱 창만 캡처하는 경로도 확인함
- Terms & Ethics 보강 및 API Key 마스킹: 저작권법·통신비밀보호법·개인정보 보호법·초상권·제3자 AI 전송·학업 윤리·책임 제한을 명시하고, Settings API Key 입력을 마스킹 처리
- 대학 테마 아이콘 동작 확인: 저장 시 창·Dock 아이콘은 런타임 변경되지만 Finder의 `.app` 번들 리소스 아이콘은 변경하지 않음. Finder 아이콘 영구 변경은 별도 macOS 권한·배포정책 검토가 필요
- 대학 테마 프리셋 41개로 확장: KAIST·UNIST·DGIST·GIST·POSTECH 및 주요 대학을 macOS·Windows에 동일 반영하고, 드롭다운을 사전순으로 강제 정렬
- macOS QA용 DMG 생성 완료: `tmp/release_qa/v0.9.0/URY_Engine_v0.9.0.dmg`에 복사하고 원본과 SHA-256 일치 확인, `hdiutil` 마운트·앱 번들 smoke test 통과
- QA 앱 충돌 방지: 테스트 폴더의 복사본만 `URY Engine QA.app` 및 `com.ury.engine.qa`로 분리하고 원본 앱은 유지. Finder 방식 `open -n -W` 실행 확인 완료
- macOS Dock 아이콘 보정: `.icns` 생성 시 8% 투명 여백을 적용하고, Dock이 가리키던 `/Applications/URY Engine.app`도 최신 빌드로 교체·캐시 갱신. 설치본·소스 아이콘 alpha bbox 일치 확인
- 최신 라우팅 포함 macOS 앱 재빌드 완료: ad-hoc 서명 검증 및 `--smoke-test` 통과
- Tutor 수식·서식 표시 보정 완료: macOS·Windows 공용 GUI가 행렬·분수·제곱근 LaTeX를 읽기 쉬운 평문/유니코드로 바꾸고 긴 `---`·`────` 장식선을 제거함. Tutor 프롬프트도 원시 LaTeX·반복 구분선을 금지하도록 동기화했으며 포맷 렌더 테스트·전체 테스트 27개 통과(1개 환경 의존 제외), macOS 앱 재빌드·서명·smoke test 통과
- 앱 표시 이름 변경 완료: macOS 번들은 `URY.app`(CFBundleName/DisplayName/Executable 모두 `URY`), Windows PyInstaller 산출물은 `URY.exe`로 변경. 사용자 워크스페이스 `URY_Engine`, 기존 릴리스 파일명·bundle identifier는 호환성을 위해 유지. 새 macOS 앱 빌드·서명·smoke test 및 전체 테스트 27개 통과(1개 환경 의존 제외)
- `URY.app` 구동 테스트 완료: 이전 `URY Engine.app` 프로세스를 종료한 뒤 새 번들을 직접 실행했고 CUA 앱 목록과 `lsof`에서 `URY` 프로세스·`~/Desktop/URY_Engine` 작업 디렉터리를 확인함. 접근성 트리 캡처는 macOS 서비스 오류(-10822)로 확인하지 못했으며, 사용자가 화면에서 창·탭을 최종 확인해야 함
- 모델 라우팅 수정 포함 macOS 앱 재빌드 완료: ad-hoc 서명 검증 및 `--smoke-test` 통과
- Gemini 모델 라우팅 수정: 기본 fallback을 3.8/3.7/3.6 Flash 중심으로 교체하고 종료된 1.5/2.0은 최하위로 격리. macOS·Windows 공용 코드와 회귀 테스트 반영
- 자동 테스트 27개 통과(1개 환경 의존 제외)
- 동일 테스트 음성 정상 재생성 확인: `Desktop/test`(약 75분) → `회사법 · 2026-09-08 · 1주차 · 한국어`, 약 55초 생성·저장, Markdown 9,447자 / PDF 8페이지
- 정상 생성 산출물: `Desktop/URY_Engine/2026년 2학기/회사법/강의노트/1주차/회사법_2026-09-08_선택자료_강의노트.pdf`; 기존 206자 1페이지 결과와 달리 전체 섹션이 포함됨
- Windows 결과물 이상 징후 분석: Desktop `회사법_1주차_강의노트.pdf`는 메타데이터를 제외해도 1페이지·추출 본문 206자에서 문장이 중단된 부분 응답임. 카카오톡 전달로 파일 시각은 신뢰하지 않음
- 위 PDF에는 대응하는 Markdown 로그/원본이 Desktop에 없으며, 구버전 Windows 비스트리밍 응답 파싱(첫 번째 text part만 저장) 또는 부분 응답 저장 가능성을 우선 의심. 현재 소스는 SSE 조각을 모두 결합함
- macOS 앱 재빌드 완료: `URY_macOS/URY Engine.app`, ad-hoc 서명 및 `--smoke-test` 통과
- 실제 Studio 생성 함수 smoke test 성공: `gemini-flash-latest`, 74분 8초 M4A + 2강 PDF, 2주차·한국어 조건에서 약 70초 후 Markdown/PDF 생성
- 위 smoke test 토큰 사용량: 입력 145,013 / 출력 5,634 / 합계 153,201; 음성·PDF 업로드와 인덱싱도 정상 완료
- 실패 입력 확인: 74분 8초 AAC M4A 35.9MB + 2강 PDF 1.6MB, 파일 형식·크기 정상
- 별도 결함 확인: 종료된 `gemini-1.5-flash`, `gemini-2.0-flash`가 최신 3.x보다 우선되는 모델 정렬·fallback 문제. 다만 이번 강제 `gemini-flash-latest` smoke test는 정상 완료되어 기존 240초 실패의 단독 원인으로 확정하지 않음
- Codex·Antigravity 공용 인수인계 문서, 기능 현황표, 승인용 구현 계획서 작성
- Antigravity용 Git 원격·브랜치·안전한 동기화·검증·푸시 절차 기록
- Gemini 강의노트 생성을 `streamGenerateContent` SSE 방식으로 변경
- 생성 출력 한도를 16,384에서 8,192토큰으로 조정
- 핵심 내용은 유지하고 반복·잡담·저가치 세부 설명을 압축하도록 프롬프트 최적화
- SSE 조각 결합 및 토큰 사용량 수집 테스트 추가, 전체 테스트 26개 통과(1개 환경 의존 제외)
- 최적화 코드가 포함된 macOS 앱 빌드 완료
- 생성 시작 후 무응답처럼 보이지 않도록 5초 간격 서버 대기 로그 추가
- 강의노트 생성 제한 120초에서 240초로 연장
- 타임아웃 발생 시 동일 요청 자동 재시도 제거
- RPD 소진과 네트워크 오류, AI 생성 시간 초과 메시지 분리
- 429/503 발생 시 대체 모델 전환, 후보 모델 최대 3개 제한
- Gemini 정상 응답의 입력·출력·총 토큰 로그 표시
- macOS v0.9.0 GitHub Release 및 업데이트 감지 검증
- 테스트 릴리스 v0.9.1-test 생성

## 개발 예정

1. 최적화된 스트리밍 강의노트 생성 실사용 테스트
2. 동일 강의자료 재사용 시 Gemini File API 업로드 캐시 적용
3. Windows UI를 macOS와 동일한 흐름으로 최종 정리
4. Windows 빌드 환경과 설치 패키지 생성·검증
5. macOS 후속 안정화 릴리스 및 테스트 릴리스 정리

## 현재 검증 기준

- 전체 테스트: `python3 -B -m unittest discover -s tests`
- macOS 빌드: `/opt/anaconda3/bin/python3 build_macos_app.py`
- 사용자 시간표와 로컬 테스트 파일은 커밋 대상에서 제외
- Codex와 Antigravity 모두 `DEVELOPMENT_STATUS.md`, `FEATURE_MATRIX.md`, `IMPLEMENTATION_PLAN.md`를 공통 기준으로 사용

# URY Engine Implementation Plan

문서 상태: Phase 1~2 진행 중 (macOS 우선)
기준일: 2026-09-10

## 1. 목표

기존 핵심 기능을 안정적으로 유지한 상태에서 macOS 버전을 마감하고, 동일한 사용 흐름으로 Windows 버전을 완성한다. 신규 AI Notebook 기능 확장보다 Studio 강의노트 생성의 성공률·속도·진행 가시성을 우선한다.

## 2. 제품 범위

핵심 흐름은 `강의자료·녹음 선택 → 강의노트 생성 → 시험자료 생성 → Tutor 질문`이다. 유지할 탭은 Studio, Quiz & Exam, Tutor, Settings, Updates, User Guide, Terms & Ethics이다.

이번 계획에서 제외하는 항목:

- Dashboard, Advanced, 답안 채점, 전체 파이프라인 수동 실행 복원
- 강의노트 본문 출처 표시
- Apple Developer ID 서명과 공증
- 안정화 전에 새로운 대형 AI 기능 추가

## 3. 현재 기준선

- 최신 소스 커밋: `작업 중` (v0.9.4 Studio 503 fallback 보정)
- 정식 배포: macOS `v0.9.1`, 후속 안정화 `v0.9.2`, 경로·저장소명 변경 패치 `v0.9.3` 완료. v0.9.4는 Studio 503 fallback 보정 패치
- 테스트 배포: `v0.9.1-test`—업데이트 감지용이며 설치파일 없음
- 자동 테스트: 35개 통과, 1개 환경 의존 제외
- macOS 앱: 최신 스트리밍·8,192토큰 최적화·503 fallback 보정 포함 v0.9.4 후보 빌드 완료
- Windows: 공용 Python 코드 동기화, 실제 Windows 최종 빌드·QA 미완료
- 대학 테마: 41개 프리셋(macOS·Windows 동일 목록)과 드롭다운 사전순 정렬 완료

## 4. 단계별 계획

### Phase 1 — Studio 생성 안정화 (P0)

목적: 사용자가 생성 버튼을 누른 뒤 멈춤·중복 과금·입력 혼재 없이 결과를 받도록 한다.

작업:

1. 짧은 음성, 60분 이상 음성, PDF 1개, 복수 자료 조합으로 실제 Gemini smoke test
2. 종료된 Gemini 1.5/2.0 모델 우선순위와 fallback을 현행 3.8/3.7/3.6 Flash로 교체
3. 기능별 모델 풀 분리: Tutor=3.5/3.1/2.5 Flash-Lite, 강의노트=3.8/3.7/3.6/3.5/2.5 Flash, 시험자료=비-Lite Stable Flash — 코드 반영·앱 빌드 완료, 실제 429/503 회귀시험 남음
4. `업로드 → 인덱싱 → 서버 대기 → 스트림 수신 → 저장 → PDF` 단계별 시간을 로그에 기록
5. Studio 로그를 `system/logs/studio_latest.log`에 저장하고 API Key는 절대 기록하지 않음 — 공용 코드 반영 완료, 앱 UI 회귀시험 필요
6. 같은 파일의 Gemini File URI를 지문과 만료시간 기준으로 재사용
7. 429 응답을 RPD와 RPM/TPM으로 구분하고 사용자 행동을 정확히 안내. RPD 소진 시에도 현재 모델을 건너뛰고 다음 모델로 즉시 전환
8. 취소 시 새 결과가 저장되거나 이전 실행과 섞이지 않는지 검증
9. 기본 API Key와 별도 프로젝트 Backup Key를 저장하고, 쿼터·서버 제한 시 Backup Key로 fallback. 파일 입력은 Backup 프로젝트에 다시 업로드
10. Gemini `/v1beta/models` 응답을 기능별 모델 풀의 기준으로 사용하고 버전 점수로 자동 정렬. 새 Stable Flash/Flash-Lite가 추가되면 코드 수정 없이 최신 모델을 우선 사용하며, Preview·전용 모델은 일반 텍스트 경로에서 제외
11. Settings 헤더의 API 상태 배지는 입력값 길이가 아니라 `/v1beta/models` 인증 결과로 갱신하고, 정상 키·잘못된 키·네트워크 확인 불가를 구분

완료 조건:

- 선택하지 않은 파일 내용이 결과에 포함되지 않음
- 정상 요청에서 5초 이상 상태 설명 없이 UI가 멈춰 보이지 않음
- 한 언어 정상 생성은 Gemini 생성 요청 1회
- 타임아웃 요청이 자동 복제되지 않음
- 실패 시 단계, 모델, HTTP 상태, 안전한 재시도 안내가 남음
- 모델 목록이 갱신되어도 새 Stable 모델이 기존 후보보다 먼저 선택됨

### Phase 2 — macOS 마감 릴리스 (P0)

작업:

1. Settings, Studio, Quiz & Exam, Tutor, Updates 전체 수동 회귀시험
2. User Guide에 실제 앱 스크린샷 삽입 — 개인정보 없는 샘플 워크스페이스에서 5개 탭 캡처 및 macOS 번들 포함 검증 완료
3. 설치 후 앱 위치와 사용자 워크스페이스를 이동해 상대경로 시험
4. 기존 테스트 릴리스 `v0.9.1-test`는 유지하고 정식 릴리즈와 혼동되지 않도록 문서에서 구분
5. 버전 증가, 앱 빌드, ad-hoc 서명 확인, DMG 생성·검증
6. GitHub 정식 릴리스 업로드 후 업데이트 감지·다운로드 확인

후속 `v0.9.2`에는 Settings의 API 연결 수동 재확인 1개 기능과 Dock 아이콘 안전 여백 보정만 포함했고, 새 생성 기능이나 대규모 UI 변경은 넣지 않았다.

완료 조건:

- 신규 설치와 기존 사용자 업데이트 모두 실행 가능
- API Key·시간표·강의자료가 배포파일과 Git에 포함되지 않음
- DMG 체크섬과 Release asset 확인
- 알려진 치명적 오류 0건

### Phase 3 — Windows 기능 동등성 (P1)

작업:

1. macOS 공용 기능과 Windows 소스 차이 감사
2. 경로, 파일 선택기, 폰트, 아이콘, subprocess 호출을 Windows 방식으로 검증
3. 딱딱한 직사각형 위젯을 현재 macOS 카드·라운드 UI와 동일하게 조정
4. Windows에서 Settings, Studio, PDF, Tutor, Updates 테스트
5. PyInstaller 단독 EXE 빌드 및 깨끗한 Windows 환경 실행시험
6. 설치·업데이트·완전삭제 패키지 검증

완료 조건:

- 핵심 탭과 동작이 macOS와 동일함
- Python이 설치되지 않은 Windows에서 실행됨
- 한글 경로와 공백 포함 경로에서 정상 동작
- 앱 삭제 시 URY 전용 구성요소만 제거하고 사용자 자료 삭제 여부를 선택 가능

### Phase 4 — 운영 안정화 (P1)

작업:

1. 앱 내부 버전과 빌드·DMG·업데이터 버전을 단일 값으로 통합
2. macOS/Windows 공통 코드 중 안전한 범위만 공유 모듈화
3. 릴리스 체크리스트 자동 검증
4. 오류 보고용 로그 내보내기 기능 추가—API Key와 개인 내용은 마스킹

완료 조건:

- 버전 불일치가 자동 테스트에서 차단됨
- 배포 전 단일 명령으로 테스트와 개인정보 포함 여부 확인 가능
- 사용자에게서 받은 로그만으로 실패 단계를 판별 가능

### Phase 5 — 선택적 기능 확장 (P2, 별도 승인)

핵심 안정화 후에만 검토한다.

- 강의노트 기반 플래시카드
- 간격 반복 복습 일정
- 강의별 핵심 질문과 퀴즈 생성
- 자료별 학습 진척도
- AI Notebook 스타일 자료 탐색 개선

## 5. 작업 순서

현재 `Phase 1 + Phase 2`를 우선 진행한다. macOS 생성 안정성과 정식 릴리스를 확정한 뒤 Phase 3 Windows 작업을 시작해 플랫폼 문제와 Gemini 문제를 분리한다.

## 6. 변경 관리

- 모든 작업은 시작·중단·완료 시 `DEVELOPMENT_STATUS.md`에 기록한다.
- 기능 상태 변화는 `FEATURE_MATRIX.md`에 반영한다.
- 계획 범위 또는 우선순위 변화는 이 문서에 반영한다.
- Codex는 `AGENTS.md`, Antigravity는 `GEMINI.md`에서 동일한 문서 체인으로 진입한다.
- 승인되지 않은 Phase는 구현하지 않는다.

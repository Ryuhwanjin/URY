# URY Engine 개발 현황

마지막 갱신: 2026-09-10

## 진행 중

- 최적화 앱 실사용 확인 필요: Studio 로그에서 `서버 응답 대기` 후 `AI 응답 수신 중`으로 전환되는지 확인
- 사용자 승인 대기: `IMPLEMENTATION_PLAN.md`의 Phase 1~5 범위와 우선순위

## 최근 완료

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
3. User Guide 실제 앱 스크린샷 추가
4. Windows UI를 macOS와 동일한 흐름으로 최종 정리
5. Windows 빌드 환경과 설치 패키지 생성·검증
6. macOS 후속 안정화 릴리스 및 테스트 릴리스 정리

## 현재 검증 기준

- 전체 테스트: `python3 -B -m unittest discover -s tests`
- macOS 빌드: `/opt/anaconda3/bin/python3 build_macos_app.py`
- 사용자 시간표와 로컬 테스트 파일은 커밋 대상에서 제외
- Codex와 Antigravity 모두 `DEVELOPMENT_STATUS.md`, `FEATURE_MATRIX.md`, `IMPLEMENTATION_PLAN.md`를 공통 기준으로 사용

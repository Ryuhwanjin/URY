# URY v0.9.1

macOS 최종 안정화 릴리즈입니다.

- 강의노트·시험자료·Tutor의 Gemini 모델 풀을 기능별로 분리하고, API 모델 목록에서 지원되는 Stable 모델을 자동 우선순위화
- 429/503 발생 시 다음 후보 모델과 Backup API Key로 즉시 전환
- Settings의 API 상태 배지가 실제 `/v1beta/models` 인증 결과를 반영하도록 보강
- Studio 스트리밍 진행 상태·모델·토큰 사용량·로그 파일 표시
- 선택한 강의자료만 생성 입력에 포함되도록 유지
- User Guide, Terms & Ethics, 대학 테마 및 macOS DMG 패키지 점검

이 배포본은 Apple Developer ID 서명·공증을 사용하지 않는 ad-hoc 빌드입니다. 최초 실행 시 macOS의 개인정보 보호 및 보안 설정에서 열기를 허용해야 할 수 있습니다.

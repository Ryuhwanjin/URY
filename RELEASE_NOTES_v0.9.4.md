# URY v0.9.4

Gemini 503 서버 혼잡 시 강의노트 생성 fallback을 보정한 패치 릴리즈입니다.

- HTTP 429/503 발생 시 같은 API 키의 다음 모델을 먼저 시도
- 기본 키의 모델 풀이 모두 실패한 경우에만 백업 API 키로 전환
- macOS·Windows 공용 생성 코드와 회귀 테스트 동기화

503은 API Key 오류가 아니라 Gemini 모델 서버의 일시적인 수요 과부하일 수 있습니다. 앱은 다음 사용 가능한 모델로 전환합니다. Apple Developer ID 서명·공증을 사용하지 않는 ad-hoc 빌드입니다.

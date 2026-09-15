# v0.9.8 — macOS·Windows 녹음 및 강의노트 오류 수정

- v0.9.7 (`97457ed`) 소스를 기반으로 수정했습니다.
- 녹음 시작 직후 코드 `-6`으로 종료되는 원인을 수정했습니다. macOS 크래시 로그에서 마이크 사용 목적 설명 누락에 따른 TCC/SIGABRT를 확인했습니다.
- 앱 빌드 시 `NSMicrophoneUsageDescription`을 코드 서명 전에 추가합니다. 첫 녹음 시 macOS 마이크 접근 요청을 허용해야 합니다.
- 앱 표시·업데이트 검사·macOS 패키징·Windows 설치 및 CI 버전을 0.9.8로 맞췄습니다.
- 맥미니에서 v0.9.7에 추가된 반응형·고DPI UI 보정과 구버전 업데이터 호환용 `URY_Engine_v0.9.8_Installer.exe` 이름을 복원했습니다.
- 권한 설명 생성과 서명 순서를 검사하는 회귀 테스트를 추가했습니다.
- Windows 녹음은 외부 `ffmpeg` 실행에 의존하지 않고 sounddevice/PortAudio로 WAV를 기록해 `WinError 2`를 해결했습니다. Windows 빌드에서 PortAudio DLL 포함 여부도 확인합니다.
- Windows에서 강의노트용 하위 프로세스의 콘솔 창을 숨기고, 작은 화면에서 창이 화면 밖에 남거나 최소 크기 때문에 프리셋 적용이 막히는 문제를 보정했습니다.
- Windows에서 기존 PDF가 다른 앱에서 열려 덮어쓸 수 없으면 기존 파일을 보존하고 새 이름으로 저장합니다.
- Windows onedir ZIP과 설치 EXE를 Windows CI에서 빌드해 v0.9.8 릴리즈에 첨부했습니다.

실제 Windows 마이크 장치와 설치파일 실행은 Windows 실기기에서 확인해야 합니다.

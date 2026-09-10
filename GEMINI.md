# Antigravity 인수인계 안내

이 저장소에서 작업을 시작하기 전에 아래 문서를 순서대로 읽는다.

1. `DEVELOPMENT_STATUS.md` — 직전 작업, 진행 중 항목, 바로 다음 단계
2. `FEATURE_MATRIX.md` — 구현 완료·부분 구현·예정 기능과 제외 범위
3. `IMPLEMENTATION_PLAN.md` — 승인 전 전체 개발 계획과 단계별 완료 조건
4. `AGENTS.md` — 공통 작업·검증·커밋 규칙

## 필수 작업 규칙

- 작업 시작 시 `DEVELOPMENT_STATUS.md`의 `진행 중`에 대상과 다음 단계를 기록한다.
- 작업 종료 시 완료 내용, 테스트 결과, 커밋 해시를 기록한다.
- 계획이나 기능 상태가 바뀌면 `FEATURE_MATRIX.md`와 `IMPLEMENTATION_PLAN.md`도 갱신한다.
- macOS와 Windows 공용 Python 파일은 양쪽을 함께 수정한다.
- `URY_macOS/system/시간표.json`, API Key, 강의자료, 생성 노트와 로컬 테스트 파일은 커밋하지 않는다.
- 기존 사용자의 dirty worktree를 덮어쓰거나 정리하지 않는다.
- 기능 추가보다 Studio 강의노트 생성 안정화를 우선한다.
- 강의노트에는 출처 표기를 넣지 않고 Tutor 답변에만 실제 파일 기반 출처를 표시한다.
- Dashboard, Advanced, 답안 채점, 전체 파이프라인 수동 실행 기능은 다시 추가하지 않는다.

## 현재 즉시 확인할 사항

- 최신 커밋은 `git log -1 --oneline`으로 확인한다. 문서 작성 직전 코드 기준선은 `d870f4d`이다.
- Studio 생성은 Gemini SSE 스트리밍, 최대 출력 8,192토큰, 대기 제한 240초를 사용한다.
- 실제 Gemini Key를 이용한 최종 스트리밍 smoke test는 아직 승인·완료되지 않았다.
- macOS 앱은 빌드됐지만 최신 안정화 변경을 포함한 새 DMG 정식 릴리스는 아직 만들지 않았다.
- 다음 작업은 `IMPLEMENTATION_PLAN.md` 승인 후 진행한다.

## Git 연결 및 동기화

- 저장소: `https://github.com/Ryuhwanjin/URY.git`
- 원격 이름: `origin`
- 기준 브랜치: `main`
- 기능 브랜치가 필요하면 `codex/` 또는 `antigravity/` 접두사를 사용한다.
- 인증 토큰, API Key, `.env` 내용은 문서·로그·커밋에 남기지 않는다.

새 작업 폴더라면:

```bash
git clone https://github.com/Ryuhwanjin/URY.git
cd URY
git switch main
git pull --ff-only origin main
```

이미 이 작업 폴더를 열었다면:

```bash
git remote -v
git branch --show-current
git status --short
git fetch origin
git log --oneline --decorate -10
```

`git status --short`에 변경이 있으면 사용자 작업일 수 있으므로 바로 pull, reset, checkout 또는 삭제하지 않는다. 먼저 변경 파일을 확인하고, 원격 반영이 필요하면 충돌 없는 방식으로 보존한다.

작업 완료 시:

```bash
python3 -B -m unittest discover -s tests
git diff --check
git status --short
git add <이번 작업 파일만>
git commit -m "<변경 목적>"
git push origin <현재 브랜치>
```

커밋 후 `DEVELOPMENT_STATUS.md`에 커밋 해시와 검증 결과를 기록한다. GitHub Release는 사용자가 명시적으로 승인했을 때만 생성·수정·삭제한다.

## 기본 검증 명령

```bash
python3 -B -m unittest discover -s tests
/opt/anaconda3/bin/python3 build_macos_app.py
```

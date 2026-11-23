#!/usr/bin/env bash
# Claude 영상 제작 오픈소스 7개 - macOS 설치 스크립트
# 실행: bash setup-mac.sh
set -u
ROOT="$HOME/ClaudeVideo"; REPOS="$ROOT/repos"
step(){ printf "\n\033[32m=== %s ===\033[0m\n" "$1"; }
has(){ command -v "$1" >/dev/null 2>&1; }

step "1. 필수 도구 설치 (Homebrew, Git, Node.js, Python, ffmpeg, Chrome, Bun)"
if ! has brew; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
fi
for p in git node python@3.12 ffmpeg; do brew list "$p" >/dev/null 2>&1 || brew install "$p"; done
has bun || brew install oven-sh/bun/bun
[ -d "/Applications/Google Chrome.app" ] || brew install --cask google-chrome

step "2. 버전 확인"
node --version; python3 --version; ffmpeg -version | head -1; bun --version

step "3. 오픈소스 7개 내려받기 -> $REPOS"
mkdir -p "$REPOS"
for r in yihui-dev/awesome-opus5-5-videos lemomo-ai/lemo-opuscar mexicat/pdoom-video \
         Vincentwei1021/mg-styles-15 JohnHeibel/ClaudeAnimationBase \
         athemeroy/awesome-claude-5-5-videos joeseesun/opus-video-prompts; do
  d="$REPOS/${r#*/}"
  if [ -d "$d/.git" ]; then git -C "$d" pull --ff-only; else git clone --depth 1 "https://github.com/$r.git" "$d"; fi
done

step "4. 실행형 프로젝트 의존성 설치"
[ -d "$REPOS/ClaudeAnimationBase" ] && (cd "$REPOS/ClaudeAnimationBase" && npm install)
[ -d "$REPOS/pdoom-video/app" ] && (cd "$REPOS/pdoom-video/app" && bun install)

step "5. Lemo Opuscar 플러그인 (Claude Code)"
if has claude; then
  claude plugin marketplace add lemomo-ai/lemo-opuscar
  claude plugin install lemo-opuscar@lemolab
else
  echo "'claude' 명령이 없습니다. Claude Code 설치 후 실행하세요:"
  echo "  claude plugin marketplace add lemomo-ai/lemo-opuscar"
  echo "  claude plugin install lemo-opuscar@lemolab"
fi

step "6. 첫 영상용 빈 작업 폴더"
mkdir -p "$ROOT/projects/첫영상"; echo "  $ROOT/projects/첫영상"
printf "\n\033[32m완료! 작업 폴더에서 'claude' 실행 -> /effort high -> 프롬프트 붙여넣기 -> 'mp4로 렌더링해줘'\033[0m\n"

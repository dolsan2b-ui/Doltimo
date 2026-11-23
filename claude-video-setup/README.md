# Claude 영상 제작 오픈소스 7개 - PC 설치 키트

## 설치 (한 번만)
| PC | 방법 |
|---|---|
| Windows | 이 폴더를 받아서 `install-windows.bat` 더블클릭 |
| Mac | 터미널에서 `bash setup-mac.sh` |

스크립트가 하는 일:
1. Git · Node.js(LTS) · Python 3.12 · ffmpeg · Chrome · Bun 설치 (이미 있으면 건너뜀)
2. 7개 저장소를 `~/ClaudeVideo/repos/` 에 내려받기
3. ClaudeAnimationBase(`npm install`), pdoom-video(`bun install`) 의존성 설치
4. Claude Code가 있으면 Lemo Opuscar 플러그인 설치
5. 빈 작업 폴더 `~/ClaudeVideo/projects/첫영상` 생성

## 설치 후 첫 영상 만들기
```
cd ~/ClaudeVideo/projects/첫영상
claude
/effort high
(프롬프트 붙여넣기) → "mp4로 렌더링해줘"
```

## 7개 위치
| # | 이름 | 폴더 | 쓰는 법 |
|---|---|---|---|
| 01 | Awesome Opus 5.5 Video | repos/awesome-opus5-5-videos | `prompts/` 복사 |
| 02 | Lemo Opuscar | 플러그인 | `/lemo-opuscar:lemo-opuscar` |
| 03 | Beat Movie (P(doom)) | repos/pdoom-video | `cd app && bunx vite` |
| 04 | MG Style | repos/mg-styles-15 | `prompts/` 복사 |
| 05 | Claude Animation Base | repos/ClaudeAnimationBase | `node render.mjs --clip --out=out/video.mp4` |
| 06 | Awesome Claude 5.5 | repos/awesome-claude-5-5-videos | 사례 참고 |
| 07 | Opus Video Prompt | repos/opus-video-prompts | `prompts/` 복사 |

## 주의 (PDF 내용 기준)
- Opus Video Prompt는 라이선스 표기 없음 → 참고만, 재배포 금지
- Beat Movie는 코드만 MIT, 노래·가사는 별도 저작권
- 영상 한 편에 수십 분 + 토큰 많이 사용 → 10초짜리부터 시작
- 릴스용이면 "세로 9:16", 한글 자막이면 "자막 폰트는 Pretendard로" 명시

# Doltimo

## Overview

Doltimo is an open-source AI platform that generates music and video content from user prompts. The project enables creators to transform ideas into multimedia experiences using advanced artificial intelligence technologies.

Designed for musicians, content creators, marketers, and developers, Doltimo streamlines the creative workflow by automating content generation and reducing production time.

## Features

- AI Music Generation
- AI Video Creation
- Prompt-Based Content Generation
- Automated Multimedia Production
- Fast and Scalable Processing
- User-Friendly Workflow
- Creative Content Export

## Use Cases

- Create original music tracks
- Generate AI-powered videos
- Produce social media content
- Create marketing and promotional materials
- Accelerate creative prototyping
- Enhance multimedia production workflows

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Doltimo.git
```

Navigate to the project directory:

```bash
cd Doltimo
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Configure API keys and project settings.
2. Enter a text prompt describing the desired music or video.
3. Generate AI-powered content.
4. Review, edit, and export the final output.

## Auto Video Editing (이미지 + 대본 → 자동 영상 생성)

이미지 폴더와 대본 텍스트 파일만 있으면, TTS 내레이션과 자막이 자동으로 합성된 16:9 영상을 명령어 한 줄로 만들 수 있습니다.

### 설치

```bash
pip install -r requirements.txt
```

Linux에서 한글 자막이 깨질 경우 한글 폰트를 설치하세요:

```bash
sudo apt install fonts-noto-cjk
```

### 대본 작성 규칙

- 대본은 텍스트 파일(.txt)로 작성하고, **장면 하나당 한 문단(빈 줄로 구분) 또는 한 줄**로 씁니다.
- 문단/줄 개수와 이미지 폴더 안의 이미지 개수가 **1:1로 정확히 일치**해야 하며, 이미지는 파일명 순서(`img1.jpg`, `img2.jpg`, ...)대로 장면에 매칭됩니다.
- 자막에서 강조하고 싶은 단어는 `[강조할 단어]`처럼 대괄호로 감싸면 빨간색으로 표시됩니다. 대괄호는 자막에서만 색으로 표시되고, 내레이션 음성에는 괄호 없이 그대로 읽힙니다.

예시 (`examples/script.txt`):

```
[하청 노동자]들이 오늘도 거리로 나왔습니다.

500여개 [원청]에 교섭을 요구합니다.

이제는 [진짜 사장]이 나와야 합니다.
```

### 실행

```bash
python -m doltimo.cli --script examples/script.txt --images-dir my_images/ --output output.mp4
```

주요 옵션:

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--voice` | edge-tts 목소리 (`edge-tts --list-voices`로 목록 확인) | `ko-KR-SunHiNeural` |
| `--font` | 자막 폰트 파일 경로 (미지정 시 OS별로 자동 탐색) | 자동 탐색 |
| `--font-size` | 자막 글자 크기 | `76` |
| `--stroke-width` | 자막 테두리(스트로크) 두께 | `6` |
| `--zoom` | 켄 번즈 줌인 강도 | `0.08` |
| `--fps` | 출력 영상 프레임레이트 | `24` |

생성된 영상은 화면 중앙에 굵은 글씨 자막(검은 테두리 + 강조 단어 빨간색)이 표시되며, 각 이미지에는 은은한 줌인(켄 번즈) 효과가 적용됩니다. TTS 음성 파일은 `<output파일명>_tts_cache/` 폴더에 캐시되며, 디버깅 후 삭제해도 됩니다.

> 참고: 캡컷(CapCut)은 공식 외부 API를 제공하지 않아 완전 자동화에는 적합하지 않습니다. 이 기능은 ffmpeg 기반(moviepy)으로 캡컷을 거치지 않고 처음부터 끝까지 코드로 영상을 생성합니다.

## Technology Stack

- Python
- Artificial Intelligence
- Generative AI
- Machine Learning
- Audio Processing
- Video Processing
- GitHub

## Roadmap

- Advanced music composition models
- AI video editing capabilities
- Multi-language support
- Cloud rendering integration
- Creator platform integrations
- Improved user interface

## Contributing

Contributions are welcome. Feel free to submit issues, feature requests, or pull requests to help improve the project.

## License

MIT License

import argparse

from .pipeline import run
from .tts import DEFAULT_VOICE


def main():
    parser = argparse.ArgumentParser(
        description="이미지와 대본으로 자동 편집된 영상을 생성합니다 (16:9, TTS 내레이션 + 자막 포함)."
    )
    parser.add_argument("--script", required=True, help="대본 텍스트 파일 경로")
    parser.add_argument("--images-dir", required=True, help="장면 순서대로 정렬될 이미지 폴더 경로")
    parser.add_argument("--output", default="output.mp4", help="출력 영상 파일 경로 (기본: output.mp4)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"edge-tts 목소리 (기본: {DEFAULT_VOICE})")
    parser.add_argument("--font", default=None, help="자막에 사용할 한글 폰트 파일 경로 (미지정 시 자동 탐색)")
    parser.add_argument("--font-size", type=int, default=76, help="자막 글자 크기 (기본: 76)")
    parser.add_argument("--stroke-width", type=int, default=6, help="자막 테두리 두께 (기본: 6)")
    parser.add_argument("--zoom", type=float, default=0.08, help="켄 번즈 줌인 강도 (기본: 0.08)")
    parser.add_argument("--fps", type=int, default=24, help="출력 영상 프레임레이트 (기본: 24)")
    args = parser.parse_args()

    run(
        script_path=args.script,
        images_dir=args.images_dir,
        output_path=args.output,
        voice=args.voice,
        font=args.font,
        zoom=args.zoom,
        fps=args.fps,
        font_size=args.font_size,
        stroke_width=args.stroke_width,
    )


if __name__ == "__main__":
    main()

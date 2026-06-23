from pathlib import Path
from typing import Optional

from moviepy import concatenate_videoclips

from . import tts
from .caption import strip_markup
from .fonts import resolve_font
from .script_parser import list_images, parse_script
from .video_builder import build_scene_clip


def run(script_path: str, images_dir: str, output_path: str, voice: str = tts.DEFAULT_VOICE,
        font: Optional[str] = None, zoom: float = 0.08, fps: int = 24,
        font_size: int = 76, stroke_width: int = 6) -> None:
    scenes = parse_script(script_path)
    images = list_images(images_dir)

    if len(scenes) != len(images):
        raise ValueError(
            f"대본 문장/문단 수({len(scenes)})와 이미지 수({len(images)})가 일치하지 않습니다. "
            "대본을 문단(빈 줄로 구분) 또는 줄 단위로 나눈 개수와 이미지 파일 개수를 1:1로 맞춰주세요."
        )

    font_path = resolve_font(font)

    output = Path(output_path)
    cache_dir = output.parent / f"{output.stem}_tts_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    clips = []
    for i, (text, image) in enumerate(zip(scenes, images), start=1):
        audio_path = cache_dir / f"scene_{i:03d}.mp3"
        narration_text = strip_markup(text)
        duration = tts.synthesize(narration_text, audio_path, voice=voice)
        clips.append(build_scene_clip(
            image, text, duration, audio_path, font_path,
            zoom=zoom, font_size=font_size, stroke_width=stroke_width,
        ))
        print(f"[{i}/{len(scenes)}] 씬 생성 완료 ({duration:.1f}s) - {image.name}")

    final = concatenate_videoclips(clips)
    final.write_videofile(str(output), fps=fps, codec="libx264", audio_codec="aac")

    final.close()
    for clip in clips:
        clip.close()

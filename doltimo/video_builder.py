from pathlib import Path

import numpy as np
from PIL import Image
from moviepy import AudioFileClip, CompositeVideoClip, ImageClip

from .caption import render_caption_image

WIDTH, HEIGHT = 1920, 1080


def _cover_resize_crop(image_path: Path, width: int, height: int) -> np.ndarray:
    img = Image.open(image_path).convert("RGB")
    scale = max(width / img.width, height / img.height)
    new_size = (round(img.width * scale), round(img.height * scale))
    img = img.resize(new_size, Image.LANCZOS)
    left = (img.width - width) // 2
    top = (img.height - height) // 2
    img = img.crop((left, top, left + width, top + height))
    return np.array(img)


def build_scene_clip(image_path: Path, text: str, duration: float, audio_path: Path,
                      font: str, zoom: float = 0.08, font_size: int = 76,
                      stroke_width: int = 6):
    frame = _cover_resize_crop(image_path, WIDTH, HEIGHT)
    visual = ImageClip(frame).with_duration(duration)
    visual = visual.resized(lambda t: 1 + zoom * (t / duration))
    visual = CompositeVideoClip([visual.with_position("center")], size=(WIDTH, HEIGHT))

    caption_frame = render_caption_image(
        text, font, (WIDTH, HEIGHT), font_size=font_size, stroke_width=stroke_width
    )
    caption = ImageClip(caption_frame).with_duration(duration)

    scene = CompositeVideoClip([visual, caption], size=(WIDTH, HEIGHT)).with_duration(duration)
    return scene.with_audio(AudioFileClip(str(audio_path)))

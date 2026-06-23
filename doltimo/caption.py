import re
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HIGHLIGHT_COLOR = (235, 45, 45, 255)
BASE_COLOR = (255, 255, 255, 255)
STROKE_COLOR = (0, 0, 0, 255)

_HIGHLIGHT_RE = re.compile(r"\[(.+?)\]")


def strip_markup(text: str) -> str:
    """대본의 [강조] 표시를 제거하고 내레이션(TTS)용 순수 텍스트를 반환합니다."""
    return _HIGHLIGHT_RE.sub(r"\1", text)


def parse_segments(text: str) -> List[Tuple[str, bool]]:
    """[강조] 표시를 (텍스트, 강조여부) 목록으로 변환합니다."""
    segments = []
    pos = 0
    for m in _HIGHLIGHT_RE.finditer(text):
        if m.start() > pos:
            segments.append((text[pos:m.start()], False))
        segments.append((m.group(1), True))
        pos = m.end()
    if pos < len(text):
        segments.append((text[pos:], False))
    return segments or [(text, False)]


def _tokenize(segments: List[Tuple[str, bool]]) -> List[Tuple[str, bool]]:
    tokens = []
    for seg_text, is_hl in segments:
        words = seg_text.split(" ")
        for i, word in enumerate(words):
            if i > 0:
                tokens.append((" ", False))
            if word:
                tokens.append((word, is_hl))
    return tokens


def render_caption_image(text: str, font_path: str, frame_size: Tuple[int, int],
                          font_size: int = 76, stroke_width: int = 6,
                          max_width_ratio: float = 0.88, line_spacing: int = 16) -> np.ndarray:
    """대본 한 줄을 [강조] 표시에 따라 색을 입힌 투명 PNG(자막)로 렌더링합니다."""
    width, height = frame_size
    font = ImageFont.truetype(font_path, font_size)
    max_width = int(width * max_width_ratio)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    def text_w(s: str) -> float:
        return draw.textlength(s, font=font)

    tokens = _tokenize(parse_segments(text))

    lines: List[List[Tuple[str, bool]]] = []
    current: List[Tuple[str, bool]] = []
    current_w = 0.0
    for word, is_hl in tokens:
        if word == " ":
            if current:
                current.append((word, is_hl))
                current_w += text_w(" ")
            continue
        w = text_w(word)
        if current and current_w + w > max_width:
            while current and current[-1][0] == " ":
                current.pop()
            lines.append(current)
            current, current_w = [(word, is_hl)], w
        else:
            current.append((word, is_hl))
            current_w += w
    if current:
        while current and current[-1][0] == " ":
            current.pop()
        lines.append(current)

    ascent, descent = font.getmetrics()
    line_height = ascent + descent + line_spacing
    start_y = (height - line_height * len(lines)) // 2

    for li, line in enumerate(lines):
        line_w = sum(text_w(word) for word, _ in line)
        x = (width - line_w) / 2
        y = start_y + li * line_height
        for word, is_hl in line:
            color = HIGHLIGHT_COLOR if is_hl else BASE_COLOR
            draw.text((x, y), word, font=font, fill=color,
                       stroke_width=stroke_width, stroke_fill=STROKE_COLOR)
            x += text_w(word)

    return np.array(canvas)

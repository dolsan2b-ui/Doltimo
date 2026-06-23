import re
from pathlib import Path
from typing import List

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_script(script_path: str) -> List[str]:
    text = Path(script_path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"대본 파일이 비어 있습니다: {script_path}")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paragraphs) > 1:
        return paragraphs
    return [line.strip() for line in text.splitlines() if line.strip()]


def _natural_key(path: Path):
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.stem)]


def list_images(images_dir: str) -> List[Path]:
    images = [p for p in Path(images_dir).iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
    if not images:
        raise ValueError(f"이미지 폴더에 이미지가 없습니다: {images_dir}")
    return sorted(images, key=_natural_key)

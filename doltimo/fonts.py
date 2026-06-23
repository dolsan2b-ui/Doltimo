from pathlib import Path
from typing import Optional

# 자막은 굵은(Bold) 글꼴을 우선으로 찾습니다. 못 찾으면 일반(Regular) 글꼴로 대체됩니다.
_CANDIDATE_FONTS = [
    "C:/Windows/Fonts/malgunbd.ttf",
    "C:/Windows/Fonts/malgun.ttf",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothicExtraBold.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
]


def resolve_font(font: Optional[str]) -> str:
    if font:
        if not Path(font).exists():
            raise FileNotFoundError(f"지정한 폰트 파일을 찾을 수 없습니다: {font}")
        return font

    for candidate in _CANDIDATE_FONTS:
        if Path(candidate).exists():
            return candidate

    raise FileNotFoundError(
        "한글을 지원하는 폰트를 찾지 못했습니다. --font 옵션으로 폰트 파일 경로를 직접 지정해주세요.\n"
        "  - Windows: C:/Windows/Fonts/malgun.ttf\n"
        "  - Mac: Noto Sans KR 또는 맑은 고딕 설치 후 해당 경로\n"
        "  - Linux: sudo apt install fonts-noto-cjk 후 "
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    )

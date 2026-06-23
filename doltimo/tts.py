import asyncio
from pathlib import Path

import edge_tts
from moviepy import AudioFileClip

DEFAULT_VOICE = "ko-KR-SunHiNeural"


async def _synthesize_async(text: str, output_path: Path, voice: str, rate: str) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))


def synthesize(text: str, output_path: Path, voice: str = DEFAULT_VOICE, rate: str = "+0%") -> float:
    asyncio.run(_synthesize_async(text, output_path, voice, rate))
    with AudioFileClip(str(output_path)) as audio:
        return audio.duration

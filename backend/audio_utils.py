import base64
import os
import uuid

TMP_DIR = "/tmp"


def safe_b64decode(data: str) -> bytes:
    """
    Accepts base64 string that may contain whitespace/newlines
    and may be missing '=' padding.
    """
    data = "".join(data.split())  # remove whitespace/newlines

    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)

    return base64.b64decode(data, validate=False)


def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = safe_b64decode(audio_base64)

    mp3_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)

    return mp3_path


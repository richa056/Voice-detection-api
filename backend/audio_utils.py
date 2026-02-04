import base64
import os
import re
import uuid

TMP_DIR = "/tmp"


def safe_b64decode(data: str) -> bytes:
    """
    Robust base64 decode for hackathon testers.
    Handles:
    - whitespace/newlines
    - missing '=' padding
    - data URI prefix like: data:audio/mp3;base64,...
    - accidental non-base64 characters
    """
    if not data:
        raise ValueError("Empty base64 input")

    # remove whitespace/newlines
    data = "".join(data.split())

    # remove "data:...;base64," prefix if present
    if "base64," in data:
        data = data.split("base64,", 1)[1]

    # keep only base64 valid characters
    data = re.sub(r"[^A-Za-z0-9+/=]", "", data)

    # add missing padding
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


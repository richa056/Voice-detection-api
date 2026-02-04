import base64
import os
import re
import uuid
import urllib.parse

TMP_DIR = "/tmp"


import urllib.parse

def safe_b64decode(data: str) -> bytes:
    if not data:
        raise ValueError("Empty base64 input")

    # Remove whitespace
    data = "".join(data.split())

    # Decode URL encoding if present (%2F, %2B...)
    if "%" in data:
        data = urllib.parse.unquote(data)

    # Remove data URI prefix
    if "base64," in data:
        data = data.split("base64,", 1)[1]

    # Handle JSON escaped content like \" or \\n
    data = data.replace("\\n", "").replace("\\r", "").replace("\\t", "")
    data = data.replace('\\"', '"').replace("\\", "")

    # URL-safe base64 support
    data = data.replace("-", "+").replace("_", "/")

    # Remove invalid characters but KEEP + / =
    data = re.sub(r"[^A-Za-z0-9+/=]", "", data)

    # Add padding
    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)
    print("RAW BASE64 FIRST 60:", data[:60])
    print("RAW LEN:", len(data))

    try:
        return base64.b64decode(data, validate=False)
    except Exception as e:
        # helpful debug
        raise ValueError(f"Base64 decode failed. len={len(data)} 
mod4={len(data)%4}") from e


def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = safe_b64decode(audio_base64)

    mp3_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)

    return mp3_path


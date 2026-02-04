import base64
import os
import re
import urllib.parse
import uuid

TMP_DIR = "/tmp"


def safe_b64decode(data: str) -> bytes:
    if not data:
        raise ValueError("Empty base64 input")

    # remove whitespace/newlines
    data = "".join(data.split())

    # decode URL encoding if present
    if "%" in data:
        data = urllib.parse.unquote(data)

    # remove data URI prefix if present
    if "base64," in data:
        data = data.split("base64,", 1)[1]

    # fix url-safe base64
    data = data.replace("-", "+").replace("_", "/")

    # remove all non-base64 chars
    data = re.sub(r"[^A-Za-z0-9+/=]", "", data)

    # pad to multiple of 4
    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)

    # DEBUG (you can remove later)
    print("RAW BASE64 FIRST 60:", data[:60])
    print("RAW LEN:", len(data))

    return base64.b64decode(data, validate=False)


def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = safe_b64decode(audio_base64)

    mp3_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)

    return mp3_path


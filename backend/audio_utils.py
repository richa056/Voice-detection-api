import base64
import os
import uuid

TMP_DIR = "/tmp"

def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = base64.b64decode(audio_base64)
    mp3_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)
    return mp3_path


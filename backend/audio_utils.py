import base64
import os
import uuid
import subprocess

TMP_DIR = "/tmp"

def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = base64.b64decode(audio_base64)
    mp3_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)
    return mp3_path

def mp3_to_wav(mp3_path: str) -> str:
    wav_path = mp3_path.replace(".mp3", ".wav")

    # convert to 16kHz mono wav (standard ML format)
    cmd = [
        "ffmpeg", "-y",
        "-i", mp3_path,
        "-ar", "16000",
        "-ac", "1",
        wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
check=True)
    return wav_path
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


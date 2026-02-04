import base64
import os
import uuid

TMP_DIR = "/tmp"


def _extract_audio_base64(data: str) -> str:
    """
    Hackathon tester sometimes sends:
    'languageTamilaudioFormatmp3audioBase64UklG....'
    So we locate where actual audio base64 starts.

    WAV base64 often starts with: UklG
    MP3 base64 often starts with: SUQz
    """
    data = "".join(data.split())

    # remove data URI prefix if present
    if "base64," in data:
        data = data.split("base64,", 1)[1]

    wav_idx = data.find("UklG")  # RIFF (WAV)
    mp3_idx = data.find("SUQz")  # ID3 (MP3)

    if wav_idx != -1 and (mp3_idx == -1 or wav_idx < mp3_idx):
        return data[wav_idx:]
    if mp3_idx != -1:
        return data[mp3_idx:]

    # if markers not found, fallback to original string
    return data


def safe_b64decode(data: str, debug: bool = True) -> bytes:
    if not data:
        raise ValueError("Empty base64 input")

    extracted = _extract_audio_base64(data)

    # padding
    missing = len(extracted) % 4
    if missing:
        extracted += "=" * (4 - missing)

    if debug:
        print("RAW LEN:", len(data))
        print("EXTRACTED FIRST 60:", extracted[:60])
        print("EXTRACTED LEN:", len(extracted))
        print("EXTRACTED mod4:", len(extracted) % 4)

    return base64.b64decode(extracted, validate=False)


def save_base64_as_mp3(audio_base64: str) -> str:
    audio_bytes = safe_b64decode(audio_base64, debug=True)

    audio_path = os.path.join(TMP_DIR, f"{uuid.uuid4()}.mp3")
    with open(audio_path, "wb") as f:
        f.write(audio_bytes)

    return audio_path


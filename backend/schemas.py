from pydantic import BaseModel, Field
from typing import Literal

Language = Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

class VoiceDetectRequest(BaseModel):
    language: Language
    audioFormat: Literal["mp3"]
    audioBase64: str = Field(..., min_length=20)


import os
from fastapi import FastAPI, Header, HTTPException
from backend.schemas import VoiceDetectRequest
from backend.audio_utils import save_base64_as_mp3, mp3_to_wav
from backend.predictor import predict

app = FastAPI(title="Voice Detection API")

API_KEY = os.environ.get("API_KEY", "dev-key")

@app.get("/")
def root():
    return {"status": "ok", "message": "Voice Detection API running"}

@app.post("/api/voice-detection")
def voice_detection(payload: VoiceDetectRequest, x_api_key: str = 
Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    
    mp3_path = save_base64_as_mp3(payload.audioBase64)
    wav_path = mp3_to_wav(mp3_path)
    result = predict(wav_path, payload.language)


    return {
        "status": "success",
        "language": payload.language,
        "classification": result["classification"],
        "confidenceScore": float(result["confidenceScore"]),
        "explanation": result["explanation"]
    }


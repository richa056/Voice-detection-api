from ml.inference import predict_audio

def predict(audio_wav_path: str, language: str) -> dict:
    return predict_audio(audio_wav_path, language)


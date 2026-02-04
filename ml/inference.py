import os
import numpy as np
import joblib
import librosa
from ml.forensics import extract_forensic_features


VOICE_MODEL_PATH = os.path.join("ml", "models", "voice_model.pkl")
FORENSICS_MODEL_PATH = os.path.join("ml", "models", "forensics_clf.pkl")

_voice_model = None
_forensics_model = None


def load_models():
    global _voice_model, _forensics_model

    if _voice_model is None:
        _voice_model = joblib.load(VOICE_MODEL_PATH)

    if _forensics_model is None:
        _forensics_model = joblib.load(FORENSICS_MODEL_PATH)


def extract_features_main(audio_wav_path: str) -> np.ndarray:
    """
    TODO: Replace this with the exact feature extraction used in Person 1 
notebook.
    Temporary: MFCC mean vector
    """
    y, sr = librosa.load(audio_wav_path, sr=16000, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)


def extract_features_forensics(audio_wav_path: str) -> np.ndarray:
    """
    Placeholder for forensics model features.
    Person 2 may have custom features — we will update this after you 
share that file/code.
    """
    y, sr = librosa.load(audio_wav_path, sr=16000, mono=True)
    rms = librosa.feature.rms(y=y).mean()
    zcr = librosa.feature.zero_crossing_rate(y).mean()
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
    return np.array([rms, zcr, centroid], dtype=np.float32)


def predict_audio(audio_wav_path: str, language: str) -> dict:
    load_models()

    x_main = extract_features_main(audio_wav_path)
    x_f = extract_forensic_features(audio_wav_path)

    # Probabilities (AI class probability assumed index=1)
    prob_main = float(_voice_model.predict_proba([x_main])[0][1])
    prob_forensics = float(_forensics_model.predict_proba([x_f])[0][1])

    # Ensemble
    prob_ai = 0.7 * prob_main + 0.3 * prob_forensics

    classification = "AI_GENERATED" if prob_ai >= 0.5 else "HUMAN"

    explanation = (
        f"Ensemble prediction.Main={prob_main:.2f},Forensics={prob_forensics:.2f}."
    )

    return {
        "classification": classification,
        "confidenceScore": prob_ai,
        "explanation": explanation,
    }


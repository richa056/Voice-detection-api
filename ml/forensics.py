import librosa
import numpy as np
import parselmouth
from joblib import load

def extract_forensic_features(wav_path):
    y, sr = librosa.load(wav_path, sr=16000)

    rms = librosa.feature.rms(y=y)[0]
    energy_var = np.var(rms)

    silence_threshold = np.mean(rms) * 0.5
    silence_ratio = np.sum(rms < silence_threshold) / len(rms)

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    centroid_mean = np.mean(centroid)

    snd = parselmouth.Sound(wav_path)
    pitch = snd.to_pitch()
    pitch_vals = pitch.selected_array['frequency']
    pitch_vals = pitch_vals[pitch_vals > 0]

    pitch_mean = np.mean(pitch_vals) if len(pitch_vals) else 0
    pitch_var = np.var(pitch_vals) if len(pitch_vals) else 0

    point_process = parselmouth.praat.call(
        snd, "To PointProcess (periodic, cc)", 75, 500
    )

    try:
        jitter = parselmouth.praat.call(
            point_process, "Get jitter (local)", 0, 0, 75, 500, 1.3
        )
    except:
        jitter = 0.0

    try:
        shimmer = parselmouth.praat.call(
            [snd, point_process], "Get shimmer (local)", 0, 0, 75, 500, 1.3, 1.6
        )
    except:
        shimmer = 0.0

    try:
        hnr = parselmouth.praat.call(
            snd, "Get harmonics-to-noise ratio", 0, 0, 75, 500
        )
    except:
        hnr = 0.0
    

    return np.array([
        pitch_mean,
        pitch_var,
        jitter,
        shimmer,
        hnr,
        energy_var,
        silence_ratio,
        centroid_mean
    ])
from joblib import load

_clf = load("ml/models/forensics_clf.pkl")

def predict_forensics(wav_path):
    features = extract_forensic_features(wav_path)
    prob_ai = _clf.predict_proba([features])[0][1]
    return prob_ai, features


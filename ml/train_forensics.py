import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
from forensics import extract_forensic_features

X, y = [], []

for label, folder in [(0, "human"), (1, "ai")]:
    base = f"ml/data/{folder}"
    print("Reading:", base)

    for file in os.listdir(base):
        print("Found:", file)

        if file.endswith(".wav"):
            path = os.path.join(base, file)
            features = extract_forensic_features(path)
            X.append(features)
            y.append(label)

print("Total samples:", len(X))

X = np.array(X)
y = np.array(y)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42
)

model.fit(X, y)
dump(model, "ml/models/forensics_clf.pkl")

print("Forensics model trained and saved")

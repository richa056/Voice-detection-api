from forensics import predict_forensics
from explain import generate_explanation

prob, features = predict_forensics("ml/data/ai/ai1.wav")

print("AI probability:", prob)
print("Explanation:", generate_explanation(features, prob))

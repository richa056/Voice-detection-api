def generate_explanation(features, confidence):
    pitch_var = features[1]
    jitter = features[2]
    shimmer = features[3]
    silence_ratio = features[6]

    reasons = []

    if pitch_var < 10:
        reasons.append("Unusually stable pitch detected")
    if jitter < 0.01:
        reasons.append("Low micro pitch variations typical of synthetic speech")
    if shimmer < 0.02:
        reasons.append("Amplitude variations are unnaturally consistent")
    if silence_ratio < 0.05:
        reasons.append("Lack of natural pauses and breath patterns")

    if not reasons:
        reasons.append("Natural speech imperfections detected")

    explanation = "; ".join(reasons)

    if confidence < 0.6:
        explanation = "Mixed characteristics detected. " + explanation

    return explanation

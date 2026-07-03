def confidence_from_evidence(evidence):
    score = 30
    joined = " ".join(evidence).lower()

    if "latest inspection date" in joined:
        score += 20
    if "queen seen: yes" in joined:
        score += 15
    if "eggs seen: yes" in joined:
        score += 15
    if "brood frames:" in joined:
        score += 10
    if "bee coverage frames:" in joined:
        score += 10
    if "no inspection record" in joined:
        score -= 25
    if "unknown" in joined:
        score -= 10

    score = max(0, min(100, score))
    if score >= 80:
        band = "High"
    elif score >= 50:
        band = "Medium"
    else:
        band = "Low"
    return {"score": score, "band": band}

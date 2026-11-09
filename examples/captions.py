import re

TOPIC_TAGS = {
    "water": ["WaterScience", "Chemistry", "ScienceFacts"],
    "dna": ["DNA", "Genetics", "Biology"],
    "orbit": ["Astronomy", "SpaceFacts", "SolarSystem"],
    "neuron": ["Neuroscience", "BrainFacts", "Biology"],
    "heart": ["HumanBody", "HeartScience", "Biology"],
    "sun": ["Astronomy", "SpaceScience", "ScienceFacts"],
    "saturn": ["Saturn", "Astronomy", "SpaceFacts"],
}

def make_caption(script, facts):
    title = str(script.get("title") or "Discover something new").strip()
    topic = " ".join(str(script.get(k) or "") for k in ("id", "category", "topic", "title")).lower()

    verified = []
    for item in facts.get("claims", []):
        if not isinstance(item, dict) or item.get("status") != "source_supported":
            continue
        claim = re.sub(r"https?://\\S+", "", str(item.get("claim") or "")).strip()
        if claim and claim not in verified:
            verified.append(claim)

    if verified:
        explanation = " ".join(verified[:2])
        if len(explanation) > 420:
            sentences = re.split(r"(?<=[.!?])\s+", explanation)
            kept = []
            for sentence in sentences:
                if len(" ".join(kept + [sentence])) > 420:
                    break
                kept.append(sentence)
            explanation = " ".join(kept) if kept else verified[0]
        explanation = explanation.strip()
        if explanation and explanation[-1] not in ".!?":
            explanation += "."
    else:
        explanation = "Explore the science behind this fascinating topic."

    tags = ["ScienceFacts", "DidYouKnow"]
    for keyword, matched in TOPIC_TAGS.items():
        if keyword in topic:
            tags = matched
            break

    tags = list(dict.fromkeys(tags + ["CurioPulse"]))[:5]

    return (
        title + "\n\n"
        + explanation + "\n\n"
        + "Follow @curiopulse.lab for more science explained visually.\n\n"
        + " ".join("#" + tag for tag in tags)
    )

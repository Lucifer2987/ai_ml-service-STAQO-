import random  # Remove when real model added

# TODO: Uncomment when ready
# import spacy
# nlp = spacy.load("en_core_web_sm")

VALID_TAGS = ["compliant", "training_required", "non_compliant", "in_progress"]

# Simple keyword rules (replace with trained classifier)
KEYWORD_RULES = {
    "training_required": ["needs training", "not trained", "required training", "must learn"],
    "non_compliant": ["failed", "not done", "missing", "absent", "incomplete"],
    "in_progress": ["ongoing", "in progress", "working on", "started", "partial"],
    "compliant": ["completed", "done", "passed", "achieved", "met", "success"],
}

def tag_action(action_text: str) -> dict:
    """
    Tags a champion action as compliant/non_compliant/training_required/in_progress.
    TODO: Replace keyword rules with trained spaCy classifier
    """
    action_lower = action_text.lower()
    
    for tag, keywords in KEYWORD_RULES.items():
        if any(kw in action_lower for kw in keywords):
            confidence = round(random.uniform(0.75, 0.95), 2)
            return {"tag": tag, "confidence": confidence}
    
    # Default: in_progress if no match
    return {"tag": "in_progress", "confidence": round(random.uniform(0.5, 0.7), 2)}


def score_actions(actions: list[str]) -> float:
    """
    Compute overall score from list of tagged actions.
    """
    if not actions:
        return 0.0
    
    tag_weights = {"compliant": 100, "in_progress": 60, "training_required": 40, "non_compliant": 0}
    total = sum(tag_weights[tag_action(a)["tag"]] for a in actions)
    return round(total / len(actions), 1)
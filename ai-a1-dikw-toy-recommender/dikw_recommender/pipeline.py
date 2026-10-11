"""
Toy recommendation pipeline built on the DIKW/WICSS layers (Wan and Alagar, 2014).

Data          the toy catalog
Information   category affinity from a child's interests
Knowledge     age-fit and interest scores for every toy
Wisdom        hard safety vetoes (recalls, choking hazards, excluded materials)
Intelligence  holds back toys the child is not ready for yet
Creativity    swaps one pick for an expansion toy when the top picks lack variety
"""
import math
from dataclasses import dataclass, field

HAZARD_AGE_THRESHOLD = 4
AGE_SCORE = {"fit": 1.0, "not_yet": 0.4, "aged_out": 0.5}
TOP_N = 5

CATALOG = [
    dict(id="T01", name="Wooden Building Blocks Set", category="building", tags=["hands-on", "STEM", "construction"], materials=["wood"], age_min=2, age_max=8),
    dict(id="T02", name="Magnetic Tile Construction Kit", category="building", tags=["hands-on", "STEM", "construction"], materials=["plastic"], age_min=3, age_max=10),
    dict(id="T03", name="Watercolor Paint Set", category="art", tags=["creative", "sensory"], materials=["paint", "paper"], age_min=3, age_max=9),
    dict(id="T04", name="Marble Run Tower", category="building", tags=["hands-on", "STEM", "construction"], materials=["plastic"], age_min=4, age_max=10, choking_hazard=True),
    dict(id="T05", name="Plush Dinosaur", category="pretend-play", tags=["comfort", "imaginative"], materials=["fabric", "latex-foam"], age_min=1, age_max=8),
    dict(id="T06", name="60-Piece Jigsaw Puzzle", category="puzzle", tags=["problem-solving"], materials=["cardboard"], age_min=4, age_max=9),
    dict(id="T07", name="Beginner Robotics Kit", category="STEM", tags=["hands-on", "STEM", "construction", "electronics"], materials=["plastic", "metal"], age_min=6, age_max=12),
    dict(id="T08", name="Play Kitchen Set", category="pretend-play", tags=["imaginative", "social"], materials=["plastic", "wood"], age_min=3, age_max=8),
    dict(id="T09", name="Recalled Rattle Toy", category="infant", tags=["sensory"], materials=["plastic"], age_min=0, age_max=2, recalled=True),
    dict(id="T10", name="STEM Gear Building Set", category="STEM", tags=["hands-on", "STEM", "construction"], materials=["plastic"], age_min=4, age_max=10),
    dict(id="T11", name="Picture Book Bundle", category="books", tags=["quiet", "early-literacy"], materials=["paper"], age_min=1, age_max=6),
    dict(id="T12", name="Outdoor Balance Bike", category="outdoor", tags=["gross-motor", "active"], materials=["metal", "rubber"], age_min=3, age_max=6),
    dict(id="T13", name="Small Bead Jewelry Kit", category="art", tags=["creative", "fine-motor"], materials=["plastic"], age_min=5, age_max=10, choking_hazard=True),
    dict(id="T14", name="Latex Balloon Animal Kit", category="art", tags=["creative"], materials=["latex"], age_min=5, age_max=10),
]


@dataclass
class Child:
    age: int
    interests: set = field(default_factory=set)
    excluded_materials: set = field(default_factory=set)
    override_id: str = ""


def round3(x):
    """Round half up to 3 places (the demo uses the same rule; Python's round() rounds half to even)."""
    return math.floor(x * 1000 + 0.5) / 1000


def age_status(age, toy):
    if toy["age_min"] <= age <= toy["age_max"]:
        return "fit"
    return "not_yet" if age < toy["age_min"] else "aged_out"


def interest_score(toy, interests):
    affinity = 1.0 if toy["category"] in interests else 0.0
    overlap = 0.0
    if interests:
        overlap = sum(1 for t in toy["tags"] if t in interests) / len(interests)
    return min(0.7 * affinity + 0.3 * overlap, 1.0)


def score_candidates(child):
    out = []
    for toy in CATALOG:
        status = age_status(child.age, toy)
        age_sc = AGE_SCORE[status]
        int_sc = interest_score(toy, child.interests)
        total = round3(0.65 * int_sc + 0.35 * age_sc)
        out.append(dict(toy=toy, total=total, status=status, interest=round3(int_sc)))
    return out


def apply_wisdom(child, candidates):
    out = []
    for c in candidates:
        toy = c["toy"]
        forced = child.override_id == toy["id"]
        reason = ""
        if toy.get("recalled"):
            reason = "active safety recall"
        elif toy.get("choking_hazard") and child.age < HAZARD_AGE_THRESHOLD:
            reason = "choking-hazard flag below safe age threshold"
        elif any(m in child.excluded_materials for m in toy["materials"]):
            reason = "parent-excluded material"
        if forced and reason and not toy.get("recalled"):
            reason = ""  # a parent override beats everything except an active recall
        out.append({**c, "vetoed": bool(reason), "reason": reason, "forced": forced})
    return out


def apply_intelligence(survivors):
    ranked = [c for c in survivors if c["status"] != "not_yet"]
    hold = [c for c in survivors if c["status"] == "not_yet"]
    return ranked, hold


def apply_creativity(ranked, top_n=TOP_N):
    ordered = sorted(ranked, key=lambda c: -c["total"])
    top, rest = ordered[:top_n], ordered[top_n:]
    if not top:
        return []
    picks = [{**c, "expansion": False} for c in top]
    if len({c["toy"]["category"] for c in top}) > 1:
        return picks
    dominant = top[0]["toy"]["category"]
    top_tags = {t for c in top for t in c["toy"]["tags"]}
    for c in rest:
        if c["toy"]["category"] != dominant and any(t in top_tags for t in c["toy"]["tags"]):
            picks[-1] = {**c, "expansion": True}
            break
    return picks


def recommend(child):
    scored = score_candidates(child)
    vetted = apply_wisdom(child, scored)
    survivors = [c for c in vetted if not c["vetoed"]]
    vetoed = [c for c in vetted if c["vetoed"]]
    ranked, hold = apply_intelligence(survivors)
    return dict(picks=apply_creativity(ranked), vetoed=vetoed, hold=hold, total_scored=len(scored))

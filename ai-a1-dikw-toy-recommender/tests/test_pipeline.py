from dikw_recommender import Child, recommend


def ids(items):
    return [c["toy"]["id"] for c in items]


def test_recalled_toy_is_always_vetoed_even_with_override():
    r = recommend(Child(age=1, interests={"sensory"}, override_id="T09"))
    assert "T09" in ids(r["vetoed"])
    assert "T09" not in ids(r["picks"])


def test_choking_hazard_vetoed_below_threshold_age():
    r = recommend(Child(age=3, interests={"building"}))
    assert "T04" in ids(r["vetoed"])
    assert "T04" not in ids(r["picks"])


def test_choking_hazard_allowed_at_safe_age():
    r = recommend(Child(age=5, interests={"building"}))
    assert "T04" not in ids(r["vetoed"])


def test_parent_excluded_material_is_vetoed():
    r = recommend(Child(age=6, excluded_materials={"latex"}))
    assert "T14" in ids(r["vetoed"])


def test_parent_override_lifts_a_material_veto():
    r = recommend(Child(age=6, excluded_materials={"latex"}, override_id="T14"))
    assert "T14" not in ids(r["vetoed"])


def test_toys_above_the_childs_age_are_held_not_vetoed():
    r = recommend(Child(age=4, interests={"STEM"}))
    assert "T07" in ids(r["hold"])
    assert "T07" not in ids(r["vetoed"])


def test_scores_are_between_zero_and_one():
    r = recommend(Child(age=5, interests={"hands-on", "construction"}))
    assert all(0 <= c["total"] <= 1 for c in r["picks"])


def test_default_profile_returns_five_picks():
    r = recommend(Child(age=5, interests={"hands-on", "construction"}))
    assert len(r["picks"]) == 5

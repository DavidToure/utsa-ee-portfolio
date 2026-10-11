from tl_reference import abcd_exact, abcd_nominal_pi, solve

LINE = (0.08, 0.48, 3.33, 200)
LOAD = dict(kv=220, mw=250, pf=0.99)


def test_nominal_pi_matches_the_hand_solution():
    r = solve(abcd_nominal_pi, LINE, LOAD)
    assert abs(r["vs_ll_kv"] - 269.17) < 0.01
    assert abs(r["vr_pct"] - 26.39) < 0.01
    assert abs(r["ps_mw"] - 270.79) < 0.01


def test_exact_model_values():
    r = solve(abcd_exact, LINE, LOAD)
    assert abs(r["vs_ll_kv"] - 268.27) < 0.01
    assert abs(r["vr_pct"] - 25.94) < 0.01


def test_reciprocity_AD_minus_BC_is_one():
    a, b, c = abcd_exact(*LINE)
    assert abs(a * a - b * c - 1) < 1e-9

import numpy as np
from lti_explorer.convolution import y_analytic, y_numeric


def test_analytic_matches_numeric_convolution():
    t_grid, y_num = y_numeric(t_max=4.0, dt=1e-3)
    y_ana = y_analytic(t_grid)
    # discrete convolution has O(dt) discretization error; 5e-3 is generous
    # slack for dt=1e-3 while still catching a wrong formula.
    assert np.max(np.abs(y_num - y_ana)) < 5e-3


def test_continuity_at_seams():
    eps = 1e-6
    for seam in (1.0, 2.0, 3.0):
        left = y_analytic(np.array([seam - eps]))[0]
        right = y_analytic(np.array([seam + eps]))[0]
        assert abs(left - right) < 1e-4, f"discontinuity at t={seam}"


def test_zero_outside_support():
    assert y_analytic(np.array([-0.5]))[0] == 0.0
    assert abs(y_analytic(np.array([4.0]))[0]) < 1e-9


def test_known_values():
    # hand-checked reference points
    t = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    expected = np.array([0.125, 0.5, 0.625, 0.0, -0.625, -0.5, -0.125])
    np.testing.assert_allclose(y_analytic(t), expected, atol=1e-9)

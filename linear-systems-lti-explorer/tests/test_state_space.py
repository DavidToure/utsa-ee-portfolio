import numpy as np
from lti_explorer.state_space import SecondOrderSystem


def hw1_system():
    # y'' + 2y' - 3y = u  ->  a1=2, a0=-3
    return SecondOrderSystem(a1=2.0, a0=-3.0)


def test_poles_match_hand_factoring():
    # s^2+2s-3 = (s+3)(s-1) -> poles at -3 and +1
    sys = hw1_system()
    poles = sorted(p.real for p in sys.poles())
    assert np.allclose(poles, [-3.0, 1.0])


def test_unstable_due_to_rhp_pole():
    assert hw1_system().is_stable() is False


def test_state_space_matrices_match_hand_derivation():
    sys = hw1_system()
    np.testing.assert_allclose(sys.A, [[0, 1], [3, -2]])
    np.testing.assert_allclose(sys.B, [[0], [1]])
    np.testing.assert_allclose(sys.C, [[1, 0]])
    assert sys.D == 0


def test_transfer_function_matches_state_space_formula():
    sys = hw1_system()
    for s in (2 + 0j, 0.5j, -1 + 3j, 10 + 0j):
        direct = sys.transfer_function_at(s)
        via_ss = sys.transfer_function_via_state_space_at(s)
        assert abs(direct - via_ss) < 1e-9


def test_impulse_response_matches_hand_partial_fractions():
    sys = hw1_system()
    t = np.array([0.0, 0.5, 1.0, 2.0])
    h = sys.impulse_response(t)
    expected = -0.25 * np.exp(-3 * t) + 0.25 * np.exp(t)
    np.testing.assert_allclose(h, expected, atol=1e-9)


def test_repeated_pole_case():
    # a1=2, a0=1 -> s^2+2s+1=(s+1)^2, repeated pole at -1
    sys = SecondOrderSystem(a1=2.0, a0=1.0)
    p1, p2 = sys.poles()
    assert abs(p1 - p2) < 1e-9
    t = np.array([0.0, 1.0, 2.0])
    h = sys.impulse_response(t)
    expected = t * np.exp(-1 * t)
    np.testing.assert_allclose(h, expected, atol=1e-9)


def test_complex_pole_case():
    # a1=0.4, a0=1 -> underdamped, complex conjugate poles
    sys = SecondOrderSystem(a1=0.4, a0=1.0)
    p1, p2 = sys.poles()
    assert abs(p1.imag) > 0
    assert sys.is_stable()

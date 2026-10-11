"""Problem 4: zero-state response via convolution y(t) = (g * u)(t).

g(t) is the system's impulse response (a triangular pulse), u(t) is the
input (a two-level square wave). Both are defined piecewise below, exactly
as given in Figure 1 of the assignment. ``y_analytic`` implements the closed
-form, hand-derived piecewise solution; ``y_numeric`` computes the same
answer by brute-force discrete convolution, so the two can be checked
against each other (see tests/test_convolution.py).
"""

from __future__ import annotations

import numpy as np


def g_pulse(tau: np.ndarray) -> np.ndarray:
    """Triangular impulse response: rises 0->1 on [0,1], falls 1->0 on [1,2]."""
    tau = np.asarray(tau, dtype=float)
    out = np.zeros_like(tau)
    rising = (tau >= 0) & (tau <= 1)
    falling = (tau > 1) & (tau <= 2)
    out[rising] = tau[rising]
    out[falling] = 2 - tau[falling]
    return out


def u_square_wave(tau: np.ndarray) -> np.ndarray:
    """Input: +1 on [0,1), -1 on [1,2), zero elsewhere."""
    tau = np.asarray(tau, dtype=float)
    out = np.zeros_like(tau)
    pos = (tau >= 0) & (tau < 1)
    neg = (tau >= 1) & (tau < 2)
    out[pos] = 1.0
    out[neg] = -1.0
    return out


def y_analytic(t: np.ndarray) -> np.ndarray:
    """Closed-form piecewise solution for y(t) = (g * u)(t), hand-derived by
    splitting the sliding overlap of g(tau) and u(t-tau) into the four
    windows where its shape changes (t in [0,1], [1,2], [2,3], [3,4])."""
    t = np.asarray(t, dtype=float)
    out = np.zeros_like(t)
    w0 = (t >= 0) & (t <= 1)
    w1 = (t > 1) & (t <= 2)
    w2 = (t > 2) & (t <= 3)
    w3 = (t > 3) & (t <= 4)
    out[w0] = t[w0] ** 2 / 2
    out[w1] = -1.5 * t[w1] ** 2 + 4 * t[w1] - 2
    out[w2] = 1.5 * t[w2] ** 2 - 8 * t[w2] + 10
    out[w3] = -0.5 * t[w3] ** 2 + 4 * t[w3] - 8
    return out


def y_numeric(t_max: float = 4.0, dt: float = 1e-3) -> tuple[np.ndarray, np.ndarray]:
    """Brute-force check: discretize g and u, convolve numerically, and
    return (t_grid, y_grid) covering [0, t_max]."""
    tau_grid = np.arange(0, t_max + dt, dt)
    g_vals = g_pulse(tau_grid)
    u_vals = u_square_wave(tau_grid)
    y_vals = np.convolve(g_vals, u_vals) * dt
    t_grid = np.arange(len(y_vals)) * dt
    mask = t_grid <= t_max
    return t_grid[mask], y_vals[mask]

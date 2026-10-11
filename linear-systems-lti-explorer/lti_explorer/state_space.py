"""Problems 5-6: transfer function, impulse response, and state-space form
for a general second-order LTI system y'' + a1*y' + a0*y = u.

The assignment's specific system is y'' + 2y' - 3y = u, i.e. a1=2, a0=-3
(HW1 problem 5 writes it as "y'' + 2y' - 3y = u", so in the y''+a1 y'+a0 y=u
convention here that means a0 = -3). This module keeps a1, a0 general so
the same code answers "what if the coefficients were different" -- exactly
the question the interactive demo lets a viewer explore.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath

import numpy as np


@dataclass
class SecondOrderSystem:
    a1: float
    a0: float

    # ---- state space (controllable canonical form) ----
    @property
    def A(self) -> np.ndarray:
        return np.array([[0.0, 1.0], [-self.a0, -self.a1]])

    @property
    def B(self) -> np.ndarray:
        return np.array([[0.0], [1.0]])

    @property
    def C(self) -> np.ndarray:
        return np.array([[1.0, 0.0]])

    @property
    def D(self) -> float:
        return 0.0

    # ---- transfer function H(s) = 1/(s^2 + a1 s + a0) ----
    def poles(self) -> tuple[complex, complex]:
        disc = self.a1 ** 2 - 4 * self.a0
        sq = cmath.sqrt(disc)
        p1 = (-self.a1 + sq) / 2
        p2 = (-self.a1 - sq) / 2
        return p1, p2

    def is_stable(self) -> bool:
        return all(p.real < 0 for p in self.poles())

    def transfer_function_at(self, s: complex) -> complex:
        return 1.0 / (s ** 2 + self.a1 * s + self.a0)

    def transfer_function_via_state_space_at(self, s: complex) -> complex:
        """H(s) = C (sI - A)^-1 B, computed from the matrices directly --
        this is problem 6(b): verifying the matrix formula reproduces the
        transfer function found in problem 5 by Laplace transform."""
        sI_minus_A = s * np.eye(2) - self.A
        resolvent = np.linalg.inv(sI_minus_A)
        H = self.C @ resolvent @ self.B
        return complex(H[0, 0]) + self.D

    def impulse_response(self, t: np.ndarray) -> np.ndarray:
        """h(t) for t >= 0, handling real-distinct, repeated, and complex
        conjugate pole pairs (the demo's sliders can reach any of the three
        cases, not just HW1's real-distinct case)."""
        t = np.asarray(t, dtype=float)
        p1, p2 = self.poles()
        if abs(p1.imag) > 1e-9:
            # complex conjugate pair p = sigma +/- j*omega
            sigma, omega = p1.real, abs(p1.imag)
            return np.exp(sigma * t) * np.sin(omega * t) / omega
        p1, p2 = p1.real, p2.real
        if abs(p1 - p2) > 1e-9:
            return (np.exp(p1 * t) - np.exp(p2 * t)) / (p1 - p2)
        # repeated real pole
        return t * np.exp(p1 * t)

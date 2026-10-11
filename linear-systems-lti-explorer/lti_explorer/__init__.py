"""lti_explorer: small teaching library for EE 5143 Homework 1, problems 4-6.

Two independent pieces, mirroring the assignment's two representations of an
LTI system:

- ``convolution``: the input-output (impulse-response) description. Given a
  system's impulse response g(t) and an input u(t), compute the zero-state
  response y(t) = (g * u)(t).
- ``state_space``: the transfer-function / state-space description. Given a
  second-order ODE y'' + a1 y' + a0 y = u, build its controllable-canonical
  state-space realization (A, B, C, D), and derive the transfer function,
  poles, and impulse response from it.
"""

from .convolution import g_pulse, u_square_wave, y_analytic, y_numeric
from .state_space import SecondOrderSystem

__all__ = [
    "g_pulse",
    "u_square_wave",
    "y_analytic",
    "y_numeric",
    "SecondOrderSystem",
]

# Architecture

This project turns three parts of EE 5143 (Linear Systems and Control) Homework 1
into runnable, tested code and a live interactive demo. It intentionally implements
the same mathematics **twice, independently** — once in Python (tested with pytest)
and once in vanilla JavaScript (driving the live demo) — so that agreement between
the two is itself evidence the math is right, not just that one implementation is
internally consistent.

## Mapping to the assignment

| Assignment concept | Where it lives |
|---|---|
| Problem 4: zero-state response `y(t) = (g * u)(t)` via convolution | `lti_explorer/convolution.py` |
| Problem 5: transfer function `H(s)` and impulse response `h(t)` from the ODE `y'' + a1 y' + a0 y = u` | `lti_explorer/state_space.py` (`transfer_function_at`, `impulse_response`) |
| Problem 6: controllable-canonical state-space form `(A, B, C, D)`, and the identity `H(s) = C(sI-A)^-1 B + D` | `lti_explorer/state_space.py` (`A`, `B`, `C`, `D` properties, `transfer_function_via_state_space_at`) |
| Interactive exploration of all three | `demo.html` (self-contained, reimplements the same formulas in JS) |

### `lti_explorer/convolution.py`

`g_pulse` and `u_square_wave` are the piecewise impulse response and input exactly
as given in the assignment's Figure 1. `y_analytic` is the hand-derived, closed-form
piecewise solution (four windows, `t in [0,1], [1,2], [2,3], [3,4]`, found by sliding
`u(t-τ)` past the fixed `g(τ)` and integrating the overlap in each region).
`y_numeric` is a second, independent path to the same answer: discretize both
signals and run `np.convolve`, i.e. brute-force numerical convolution with no
knowledge of the closed form. The two are cross-checked in
`tests/test_convolution.py`.

### `lti_explorer/state_space.py`

`SecondOrderSystem` is deliberately generalized from the assignment's one fixed
system (`a1=2, a0=-3`) to arbitrary `(a1, a0)`, because that is exactly what the
demo's sliders let a viewer explore — "what if the coefficients were different"
is the natural next question after solving the assignment's specific case, and
answering it live is what makes this a portfolio piece rather than a static
write-up.

- `A`, `B`, `C`, `D` build the **controllable canonical form** directly from the
  ODE coefficients — no intermediate state elimination, since for a
  single-input/single-output ODE in this form the realization is read off the
  coefficients directly.
- `poles()` solves the characteristic equation `s^2 + a1 s + a0 = 0` via the
  quadratic formula, kept in `complex` arithmetic so it handles real-distinct,
  repeated, and complex-conjugate pole pairs uniformly.
- `is_stable()` is the standard LTI criterion: stable iff every pole has strictly
  negative real part.
- `transfer_function_at` evaluates `H(s) = 1/(s^2 + a1 s + a0)` directly (Problem
  5's answer). `transfer_function_via_state_space_at` evaluates
  `H(s) = C(sI-A)^-1 B + D` from the matrices instead (Problem 6's verification
  step). `tests/test_state_space.py` checks these agree at several sample points
  in the complex plane — that agreement *is* the content of Problem 6(b).
- `impulse_response` inverse-Laplace-transforms `H(s)` by cases (real-distinct,
  repeated, complex poles), matching the partial-fraction expansion done by hand
  for the assignment's specific system, generalized to the other two cases so the
  demo's sliders never hit an unhandled pole configuration.

## Why JavaScript reimplements the Python, rather than reusing it

The demo is a single self-contained HTML file so it can be opened or shared with
zero setup — no server, no build step, no Python runtime in the browser. Rather
than compiling the Python to WebAssembly (real but disproportionate machinery for
two small formulas), `demo.html` reimplements `poles()`, `impulse_response()`, and
the state-space matrices directly in a `<script>` block, using the same variable
names and the same case breakdown as `state_space.py`. This is a deliberate
scope/complexity tradeoff: the duplication is small (under 100 lines), auditable
by reading the two files side by side, and the Python side stays the
pytest-verified source of truth that the write-up's numbers are checked against.

## Notable design choices

- **Signed-overlap shading in the convolution panel.** Because `u(t-τ)` takes
  both +1 and -1, the product `g(τ)·u(t-τ)` can be negative — the demo shades
  positive overlap green and negative overlap in the diverging warm color, so the
  sign of the integral (and therefore of `y(t)`) is visible before you read the
  number, not just asserted by it.
- **Per-pole color, not just a global stability badge.** Each pole on the
  pole-zero map is colored individually (stable/green if `Re(s) < 0`, else the
  status-warning color) in addition to the overall "stable"/"unstable" badge,
  because a system can be unstable due to just one of its two poles, and the
  assignment's own system (`a1=2, a0=-3`) is exactly this case: one pole at -3,
  one at +1.
- **Colorblind-safe, fixed-role palette.** Series identity (g, u, y) uses a
  fixed Okabe-Ito hue assignment rather than a cycled default palette, and status
  color (stable/unstable) is a separate pair from the series colors, so identity
  and state are never confused with each other.

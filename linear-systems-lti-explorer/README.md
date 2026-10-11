# LTI System Explorer

Origin: **EE 5143, Linear Systems and Control — Homework 1, Problems 4-6**
(convolution / zero-state response, transfer function & impulse response,
controllable-canonical state-space realization).

A small tested Python library implementing the assignment's math, plus a
self-contained interactive HTML demo that lets you scrub a convolution and drag
system-coefficient sliders to see poles, stability, and state space update live.

## Quick start

```bash
pip install numpy pytest
python3 -m pytest tests/ -v
```

All 11 tests should pass. Then open `demo.html` directly in a browser — no
server or build step needed.

```python
from lti_explorer import y_analytic, SecondOrderSystem
import numpy as np

# Problem 4: zero-state response
y = y_analytic(np.linspace(0, 4, 200))

# Problems 5-6: poles, stability, state space for y'' + 2y' - 3y = u
sys = SecondOrderSystem(a1=2.0, a0=-3.0)
sys.poles()       # (1+0j, -3+0j)
sys.is_stable()    # False (pole at s=1 is in the right half-plane)
sys.A, sys.B, sys.C, sys.D
```

## Project layout

```
.
├── demo.html                    interactive HTML demo (open directly in a browser)
├── lti_explorer/
│   ├── __init__.py
│   ├── convolution.py           Problem 4: y(t) = (g * u)(t)
│   └── state_space.py           Problems 5-6: poles, H(s), impulse response, (A,B,C,D)
├── tests/
│   ├── test_convolution.py
│   └── test_state_space.py
└── docs/
    └── ARCHITECTURE.md          maps the code back to the assignment + design rationale
```

## Why

Every number in `demo.html` traces back to the same closed-form solutions worked
out by hand for Homework 1 and checked in `tests/` — the demo isn't a separate,
unverified visualization, it's the write-up made interactive. See
`docs/ARCHITECTURE.md` for how the code maps to each problem and the reasoning
behind the notable design choices.

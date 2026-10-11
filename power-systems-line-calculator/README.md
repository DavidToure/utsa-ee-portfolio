# Transmission Line Calculator

**Origin:** EE 5243 Analysis of Power Systems, Homework 5 (Glover problems 5.2, 5.14, and 5.23).

A three-phase line and load go in. The tool solves three models side by side and plots voltage regulation against line length.

## Files

- `demo.html` and `engine.js`: the browser calculator. Open `demo.html` directly.
- `tl_reference.py` and `test_tl_reference.py`: a Python reference. `pip install pytest`, then `python3 -m pytest`.

## Models

| Model | A | B | C |
|---|---|---|---|
| Short line | 1 | Z | 0 |
| Nominal pi | 1 + YZ/2 | Z | Y(1 + YZ/4) |
| Exact | cosh(gamma l) | Zc sinh(gamma l) | sinh(gamma l) / Zc |

Voltage regulation is (|VS|/|A| minus |VR,full load|) divided by |VR,full load|. The equivalent pi uses Z' = Zc sinh(gamma l) and Y'/2 = tanh(gamma l / 2) / Zc.

For problem 5.2 (200 km, 220 kV, 250 MW, 0.99 lagging) the nominal pi gives 269.17 kV, 26.39 percent regulation, and 270.79 MW sent. The exact model gives 268.27 kV and 25.94 percent.

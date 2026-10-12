# UTSA MS EE Portfolio

**Live site:** https://davidtoure.github.io/utsa-ee-portfolio/

Projects from my first semester of the MS in Electrical Engineering at UTSA (Fall 2026). Each folder turns a course assignment into something you can run: working code, a live demo, and a short note on how it maps back to the assignment.

| Folder | Course | What it is |
|---|---|---|
| `ai-a1-dikw-toy-recommender` | EE 5663, Assignment 1 | Toy recommender built on the DIKW layers, with safety vetoes and a reasoning trace. Python package with tests. |
| `ai-a2-vending-machine` | EE 5663, Assignment 2 | Rule-based vending machine. MATLAB function plus a browser version. |
| `ai-a3-robot-production-system` | EE 5663, Assignment 3 | Rule-based robot navigation with conflict resolution. MATLAB function plus a stepping browser demo. |
| `ai-a4-gamma-fis` | EE 5663, Assignment 4 | Mamdani fuzzy system that scores gamma-ray spectra for threat confidence. MATLAB, FIS file, Python reference, and a browser demo. |
| `power-systems-line-calculator` | EE 5243 | Transmission line calculator comparing short, nominal pi, and exact models. Browser tool with a tested Python reference. |
| `linear-systems-lti-explorer` | EE 5143 | LTI system explorer from Homework 1. Python package with tests and a browser demo. |

## Running things

- **Browser demos:** open any `demo.html` directly in a browser, or use the live site above. There is no server and no build step.
- **Python projects:** `pip install pytest numpy`, then run `python3 -m pytest` inside the folder.
- **MATLAB files:** run the function named by the file. The gamma-ray script also needs the five course-provided `Scenario*.txt` data files, which are not included here.

Worked homework solutions are not part of this repository.

# DIKW Toy Recommender

**Origin:** EE 5663 Artificial Intelligence, Assignment 1. The design follows the DIKW/WICSS layers from Wan and Alagar (2014).

A toy recommender where every layer is real code, and every recommendation can show why it was made.

## Quick start

```bash
pip install pytest
python3 -m pytest
```

```python
from dikw_recommender import Child, recommend

result = recommend(Child(age=5, interests={"hands-on", "construction"}))
for pick in result["picks"]:
    print(pick["toy"]["name"], pick["total"])
```

## Layout

```
dikw_recommender/pipeline.py   the six layers
tests/test_pipeline.py         safety, override, and hold behavior
docs/ARCHITECTURE.md           how the code maps to the assignment
```

The live demo uses the same logic in JavaScript. For five test profiles the Python and JavaScript versions return identical picks, vetoes, and holds.

# Architecture

Each layer of the assignment's DIKW/WICSS design is one function in `dikw_recommender/pipeline.py`.

| Layer | Function | What it does |
|---|---|---|
| Data | `CATALOG` | Fourteen toys with category, tags, materials, age range, and safety flags. |
| Information | `interest_score` | Turns a child's interests into a category affinity plus a tag overlap. |
| Knowledge | `score_candidates` | Scores every toy: 65 percent interest match and 35 percent age fit. |
| Wisdom | `apply_wisdom` | Hard vetoes: active recall, choking hazard below age 4, parent-excluded materials. A parent override lifts everything except a recall. |
| Intelligence | `apply_intelligence` | Holds back toys the child is not old enough for. They are not disliked, only not ready. |
| Creativity | `apply_creativity` | If the top picks all share one category, swaps the last pick for a related toy from a different category. |

## Design choices

**Why rules instead of machine learning.** The assignment asks for a system that can justify itself. With rules, every pick has a trace, and a safety veto is a fixed fact instead of a probability.

**Why Wisdom runs before ranking.** A toy that fails a safety rule is never ranked, so it can never appear because of a high score.

**Why a recall cannot be overridden.** A parent can lift a preference-based veto, but an active recall is a safety fact, so it always wins.

**Why hold instead of reject.** A toy that is too advanced is a different case from an unsafe one. Holding it keeps it available for later.

# Robot Navigation Production System

**Origin:** EE 5663 Artificial Intelligence, Assignment 3. Build the cycle table for a robot moving through a grid with obstacles and an object, as in lecture 4.

## Files

- `roboToure.m`: the MATLAB function. Run `roboToure` to print the cycle table.
- `engine.js` and `demo.html`: a direct port to the browser with a stepper. You can change the start, the goal, and the obstacles.

## Scenario

The robot starts at (9,7) facing north. Obstacles are at (9,8) and (9,1). The object is at (3,7). The robot reaches it in 22 cycles: it turns away from the first obstacle, runs south 5 cycles, turns at the second obstacle, runs north 5 cycles, turns west, runs 6 cycles, and detects the object.

## Conflict resolution

When several rules match, the system uses specificity first, then refractoriness (do not repeat a combination already tried), then a fixed order of n, w, s, e as the deterministic stand-in for random choice. Rule 1, detect the object, wins by convention once the robot is on the goal.

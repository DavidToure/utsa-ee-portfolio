# Gamma-Ray Threat Confidence

**Origin:** EE 5663 Artificial Intelligence, Assignment 4, Problem 4. A Mamdani fuzzy inference system that gives a threat confidence from 0 to 100 percent for a gamma-ray spectrum.

## Files

- `gta_Toure.m`: reads the five scenario spectra, computes the four features, and evaluates the FIS. It needs the course-provided `Scenario1.txt` to `Scenario5.txt` in the same folder.
- `gamma_threat_fis.fis`: the FIS for MATLAB's Fuzzy Logic Toolbox.
- `fis_core.py`, `build_system.py`, `verify_python.py`: an independent Python implementation. Run `python3 verify_python.py`.
- `engine.js` and `demo.html`: the same system in the browser, with sliders and a view of which rules fire.

## The system

Features of each normalized 1024-bin spectrum: NTOTAL (sum of normalized counts), MAX8 (peak of the last 800 bins), BIN05 (bins below 0.5), BIN08 (bins above 0.8). Sixteen rules map them to a five-term output. Min for AND, min implication, max aggregation, and centroid defuzzification, which are MATLAB's `evalfis` defaults.

## Results on the five scenarios

55.01, 35.22, 20.80, 20.80, and 49.06 percent. The Python and JavaScript versions give the same numbers.

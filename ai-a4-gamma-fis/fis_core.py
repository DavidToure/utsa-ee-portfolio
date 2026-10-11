"""
Hand-written Mamdani fuzzy inference engine — mirrors MATLAB's evalfis()
default behavior (AND = min, implication = min, aggregation = max,
defuzzification = centroid) so it can be used as an independent check
against the .fis file / MATLAB script, and as the portable reference
implementation for the portfolio demo.
"""
import numpy as np

# ---------- membership functions ----------

def trimf(x, abc):
    a, b, c = abc
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if a != b:
        left = (x - a) / (b - a)
    else:
        left = np.ones_like(x)
    if b != c:
        right = (c - x) / (c - b)
    else:
        right = np.ones_like(x)
    y = np.minimum(left, right)
    y = np.clip(y, 0, 1)
    y[x <= a] = 0
    y[x >= c] = 0
    # restore peak in case a==b or b==c edge cases
    y = np.where(x == b, 1.0, y)
    return np.clip(y, 0, 1)


def trapmf(x, abcd):
    a, b, c, d = abcd
    x = np.asarray(x, dtype=float)
    y = np.ones_like(x)
    left = np.ones_like(x) if a == b else (x - a) / (b - a)
    right = np.ones_like(x) if c == d else (d - x) / (d - c)
    y = np.minimum(np.minimum(left, right), 1.0)
    y = np.clip(y, 0, 1)
    y[x <= a] = 0
    y[x >= d] = 0
    y[(x >= b) & (x <= c)] = 1.0
    return y


class FuzzyVar:
    """A linguistic variable: universe + named terms (each a membership fn)."""
    def __init__(self, name, universe):
        self.name = name
        self.universe = universe  # (lo, hi)
        self.terms = {}  # name -> ('trimf'/'trapmf', params)

    def add_term(self, name, kind, params):
        self.terms[name] = (kind, params)

    def membership(self, term, x):
        kind, params = self.terms[term]
        x = np.atleast_1d(np.asarray(x, dtype=float))
        if kind == 'trimf':
            val = trimf(x, params)
        else:
            val = trapmf(x, params)
        return val[0] if val.size == 1 else val


class MamdaniFIS:
    def __init__(self, name):
        self.name = name
        self.inputs = {}   # name -> FuzzyVar
        self.output = None  # FuzzyVar
        self.rules = []     # list of (antecedent list[(var,term,neg)], conn, out_term, weight)

    def add_input(self, fv):
        self.inputs[fv.name] = fv

    def set_output(self, fv):
        self.output = fv

    def add_rule(self, antecedent, out_term, connective='and', weight=1.0):
        """antecedent: list of (input_name, term_name)"""
        self.rules.append((antecedent, connective, out_term, weight))

    def evaluate(self, input_values, n_points=1001):
        """input_values: dict input_name -> crisp value. Returns (crisp_output, rule_firing)."""
        lo, hi = self.output.universe
        y_axis = np.linspace(lo, hi, n_points)
        aggregated = np.zeros_like(y_axis)
        firing_strengths = []

        for antecedent, connective, out_term, weight in self.rules:
            degrees = []
            for (var_name, term_name) in antecedent:
                fv = self.inputs[var_name]
                x = input_values[var_name]
                degrees.append(fv.membership(term_name, x))
            if connective == 'and':
                strength = min(degrees) * weight
            else:
                strength = max(degrees) * weight
            firing_strengths.append(strength)
            if strength > 0:
                out_kind, out_params = self.output.terms[out_term]
                if out_kind == 'trimf':
                    out_mf = trimf(y_axis, out_params)
                else:
                    out_mf = trapmf(y_axis, out_params)
                clipped = np.minimum(out_mf, strength)  # Mamdani min-implication
                aggregated = np.maximum(aggregated, clipped)  # max-aggregation

        if aggregated.sum() == 0:
            crisp = (lo + hi) / 2.0
        else:
            crisp = np.sum(y_axis * aggregated) / np.sum(aggregated)  # centroid
        return crisp, firing_strengths

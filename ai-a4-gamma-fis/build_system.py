"""
Defines the gamma-ray threat-confidence Mamdani FIS: universes, fuzzy sets,
and rule base. Shared by the verification script, the .fis file generator,
and the interactive demo's data export.
"""
from fis_core import FuzzyVar, MamdaniFIS


def build_fis():
    fis = MamdaniFIS('gamma_threat_fis')

    # ---- Input 1: NTOTAL  (sum of normalized counts; natural universe
    # is [0,1024] since each of the 1024 bins contributes at most 1 after
    # normalizing by the spectrum's own max). Human threshold: 400.
    ntotal = FuzzyVar('NTOTAL', (0, 1024))
    ntotal.add_term('Low',    'trapmf', (0, 0, 200, 400))
    ntotal.add_term('Medium', 'trimf',  (200, 400, 600))
    ntotal.add_term('High',   'trapmf', (400, 600, 1024, 1024))
    fis.add_input(ntotal)

    # ---- Input 2: MAX8  (max of the last 800 bins, normalized -> natural
    # universe [0,1]). Human threshold: 0.6.
    max8 = FuzzyVar('MAX8', (0, 1))
    max8.add_term('Low',    'trapmf', (0, 0, 0.3, 0.6))
    max8.add_term('Medium', 'trimf',  (0.3, 0.6, 0.9))
    max8.add_term('High',   'trapmf', (0.6, 0.9, 1, 1))
    fis.add_input(max8)

    # ---- Input 3: BIN05  (count of bins < 0.5, out of 1024 -> universe
    # [0,1024]). Human threshold: 450 — but INVERTED sense (high BIN05
    # argues AGAINST a threat, handled in the rule base, not the sets).
    bin05 = FuzzyVar('BIN05', (0, 1024))
    bin05.add_term('Low',    'trapmf', (0, 0, 200, 450))
    bin05.add_term('Medium', 'trimf',  (200, 450, 700))
    bin05.add_term('High',   'trapmf', (450, 700, 1024, 1024))
    fis.add_input(bin05)

    # ---- Input 4: BIN08  (count of bins > 0.8, out of 1024 -> universe
    # [0,1024]). Human threshold: 180.
    bin08 = FuzzyVar('BIN08', (0, 1024))
    bin08.add_term('Low',    'trapmf', (0, 0, 90, 180))
    bin08.add_term('Medium', 'trimf',  (90, 180, 270))
    bin08.add_term('High',   'trapmf', (180, 270, 1024, 1024))
    fis.add_input(bin08)

    # ---- Output: Threat confidence, 0-100%, 5-term partition for a
    # smoothly graded confidence score.
    threat = FuzzyVar('Threat_Confidence', (0, 100))
    threat.add_term('VeryLow',  'trimf', (0, 0, 25))
    threat.add_term('Low',      'trimf', (0, 25, 50))
    threat.add_term('Medium',   'trimf', (25, 50, 75))
    threat.add_term('High',     'trimf', (50, 75, 100))
    threat.add_term('VeryHigh', 'trimf', (75, 100, 100))
    fis.set_output(threat)

    # ---- Rule base -------------------------------------------------
    # Direction, from the human-operator heuristics:
    #   MAX8 high, BIN08 high, NTOTAL high  -> push toward threat
    #   BIN05 high                          -> push toward NO threat
    # MAX8 (fraction of the tail that is still near the spectrum's own
    # peak height) is treated as the strongest single indicator, since it
    # is the one feature whose scale lines up with the human threshold.
    R = fis.add_rule
    R([('MAX8', 'High'), ('BIN08', 'High')], 'VeryHigh')
    R([('MAX8', 'High'), ('NTOTAL', 'High')], 'VeryHigh')
    R([('MAX8', 'High'), ('BIN05', 'Low')], 'High')
    R([('MAX8', 'High'), ('BIN08', 'Medium')], 'High')
    R([('MAX8', 'High')], 'High')                       # anchor: high MAX8 alone is already concerning
    R([('MAX8', 'Medium'), ('BIN08', 'High')], 'High')
    R([('MAX8', 'Medium'), ('NTOTAL', 'High')], 'High')
    R([('MAX8', 'Medium'), ('BIN05', 'Low')], 'High')
    R([('MAX8', 'Medium'), ('BIN08', 'Medium')], 'Medium')
    R([('MAX8', 'Medium'), ('BIN05', 'High')], 'Medium')
    R([('MAX8', 'Medium')], 'Medium')                   # anchor
    R([('MAX8', 'Low'), ('BIN08', 'Medium')], 'Medium')
    R([('MAX8', 'Low'), ('NTOTAL', 'High'), ('BIN05', 'Low')], 'Medium')
    R([('MAX8', 'Low'), ('BIN08', 'Low'), ('BIN05', 'High')], 'VeryLow')
    R([('MAX8', 'Low'), ('NTOTAL', 'Low'), ('BIN08', 'Low')], 'Low')
    R([('MAX8', 'Low')], 'Low')                         # anchor

    return fis


FEATURE_ORDER = ['NTOTAL', 'MAX8', 'BIN05', 'BIN08']

"""Python reference for the transmission line models, used to check the browser calculator."""
import cmath
import math


def abcd_exact(r, x, b_uS, length):
    z, y = complex(r, x), complex(0, b_uS * 1e-6)
    zc = cmath.sqrt(z / y)
    gl = cmath.sqrt(z * y) * length
    a = cmath.cosh(gl)
    return a, zc * cmath.sinh(gl), cmath.sinh(gl) / zc


def abcd_nominal_pi(r, x, b_uS, length):
    Z, Y = complex(r, x) * length, complex(0, b_uS * 1e-6) * length
    a = 1 + Y * Z / 2
    return a, Z, Y * (1 + Y * Z / 4)


def solve(model, line, load):
    a, b, c = model(*line)
    vll = load["kv"] * 1e3
    vr = vll / math.sqrt(3)
    i_mag = load["mw"] * 1e6 / (math.sqrt(3) * vll * load["pf"])
    ir = i_mag * cmath.exp(-1j * math.acos(load["pf"]))   # lagging
    vs = a * vr + b * ir
    is_ = c * vr + a * ir
    ps = (3 * vs * is_.conjugate()).real / 1e6
    return dict(vs_ll_kv=abs(vs) * math.sqrt(3) / 1e3, i_s=abs(is_), vr_pct=(abs(vs) / abs(a) - vr) / vr * 100, ps_mw=ps)


if __name__ == "__main__":
    line = (0.08, 0.48, 3.33, 200)          # Glover 5.2: r, x (ohm/km), b (microS/km), length (km)
    load = dict(kv=220, mw=250, pf=0.99)
    for name, m in [("nominal pi", abcd_nominal_pi), ("exact", abcd_exact)]:
        print(name, {k: round(v, 2) for k, v in solve(m, line, load).items()})

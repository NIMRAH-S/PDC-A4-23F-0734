import pandas as pd
import numpy as np

def speedup(ts, tp): return ts / tp
def efficiency(s, p): return s / p
def cost(p, tp): return p * tp
def overhead(p, tp, ts): return p * tp - ts
def serial_fraction(s, p):
    return np.nan if p == 1 else (1 / s - 1 / p) / (1 - 1 / p)

def main():
    df = pd.read_csv("results/raw_timings.csv")
    med = df.groupby(["workload", "n", "p"])["time_sec"].median().reset_index()
    ts_map = med[med.workload == "serial"].set_index("n")["time_sec"]
    out = []
    for _, r in med[med.workload == "parallel"].iterrows():
        n, p, tp = int(r.n), int(r.p), r.time_sec
        ts = ts_map[n]
        s = speedup(ts, tp)
        out.append(dict(n=n, p=p, T_S=ts, T_P=tp, speedup=s,
                        efficiency=efficiency(s, p), cost=cost(p, tp),
                        overhead=overhead(p, tp, ts), serial_fraction=serial_fraction(s, p)))
    m = pd.DataFrame(out)
    m.to_csv("results/metrics.csv", index=False)
    print(m.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    # Bonus: problem size for E >= 0.6 (isoefficiency). E = 1/(1+To/Ts), Ts ~ n
    # => need Ts >= 1.5*To  =>  n_req = n * 1.5 * To / Ts  (using largest n)
    print("\nEstimated n needed for E >= 0.6:")
    big = m[m.n == m.n.max()]
    for _, r in big.iterrows():
        if r.p > 1:
            n_req = r.n * 1.5 * max(r.overhead, 0) / r["T_S"]
            print(f"  p={int(r.p)}: n >= {n_req:.2e}")

if __name__ == "__main__":
    main()
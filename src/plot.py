import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def draw(ax, m, col, title, ylabel, ideal=False):
    for n, g in m.groupby("n"):
        ax.plot(g.p, g[col], marker="o", label=f"n = {n:.0e}")
    if ideal:
        ps = sorted(m.p.unique())
        ax.plot(ps, ps, "k--", label="Ideal linear speedup")
    ax.set_title(title); ax.set_xlabel("Number of processes (p)")
    ax.set_ylabel(ylabel); ax.set_xticks(sorted(m.p.unique()))
    ax.grid(True); ax.legend()

def main():
    m = pd.read_csv("results/metrics.csv")
    specs = [("T_P", "Execution Time vs p", "Time (seconds)", False, "time_vs_p"),
             ("speedup", "Speedup vs p", "Speedup (S = T_S/T_P)", True, "speedup_vs_p"),
             ("efficiency", "Efficiency vs p", "Efficiency (E = S/p)", False, "efficiency_vs_p"),
             ("overhead", "Total Overhead vs p", "Overhead T_o (seconds)", False, "overhead_vs_p")]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (col, t, yl, ideal, name) in zip(axes.flat, specs):
        f, a = plt.subplots(figsize=(6, 4.5))
        draw(a, m, col, t, yl, ideal); f.tight_layout()
        f.savefig(f"figures/{name}.png", dpi=150); plt.close(f)
        draw(ax, m, col, t, yl, ideal)
    fig.suptitle("Monte-Carlo Pi: Performance Dashboard"); fig.tight_layout()
    fig.savefig("figures/dashboard.png", dpi=150)

if __name__ == "__main__":
    main()
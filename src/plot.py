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

SPECS = [("T_P", "Execution Time vs p", "Time (seconds)", False, "time_vs_p"),
         ("speedup", "Speedup vs p", "Speedup (S = T_S/T_P)", True, "speedup_vs_p")]

def main():
    m = pd.read_csv("results/metrics.csv")
    for col, t, yl, ideal, name in SPECS:
        fig, ax = plt.subplots(figsize=(6, 4.5))
        draw(ax, m, col, t, yl, ideal); fig.tight_layout()
        fig.savefig(f"figures/{name}.png", dpi=150); plt.close(fig)

if __name__ == "__main__":
    main()
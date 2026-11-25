import time
import numpy as np
from multiprocessing import Pool

CHUNK = 5_000_000
SIZES = [10**6, 10**7, 10**8]
PROCS = [1, 2, 4, 8]
RUNS = 5

def count_inside(args):
    """Count random points inside the unit quarter circle."""
    n, seed = args
    rng = np.random.default_rng(seed)
    inside, done = 0, 0
    while done < n:
        m = min(CHUNK, n - done)
        x = rng.random(m); y = rng.random(m)
        inside += int(np.count_nonzero(x * x + y * y <= 1.0))
        done += m
    return inside

def serial(n):                       # T_S: single-threaded numpy version
    return 4.0 * count_inside((n, 0)) / n

def parallel(n, p):                  # split n samples across p workers
    parts = [(n // p + (1 if i < n % p else 0), i + 1) for i in range(p)]
    with Pool(p) as pool:
        return 4.0 * sum(pool.map(count_inside, parts)) / n

if __name__ == "__main__":
    rows = []
    for n in SIZES:
        for r in range(1, RUNS + 1):
            t = time.perf_counter(); serial(n)
            rows.append(["serial", n, 1, r, time.perf_counter() - t])
        for p in PROCS:
            for r in range(1, RUNS + 1):
                t = time.perf_counter(); parallel(n, p)
                rows.append(["parallel", n, p, r, time.perf_counter() - t])
        print(f"n={n} done")
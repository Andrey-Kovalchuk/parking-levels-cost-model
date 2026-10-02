import heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

T_str = 7
T_end = 23
DAYS = 7
DT = 1             # Time step
N_RUNS = 100
E_S = 2            # Average car stay
P = 50             # Tarif
V = 50000          # Budget monthly
V_WEEKLY = V / 4
SEED = 42          # Random seed
K_FLOORS = 1
CARS_PER_FLOOR = 50
K_VALUES = [1]

rng = np.random.default_rng(SEED)


def get_lambda(d, t):
    # Calculate λ(d,t) according to day of the week and time
    # Week days
    if d <= 5:
        if 7 <= t < 10:
            return 25          # Morning
        if 10 <= t < 17:
            return 20          # Noon peak
        if 17 <= t < 20:
            return 40          # Evening peak
        return 15              # Night (20:00-23:00)

    # Weekends
    else:
        if 10 <= t < 20:
            return 30          # Average day value
        return 12              # Low morning and night


def simulate_once(K):
    C = K * CARS_PER_FLOOR
    parked = []
    served = 0
    lost = 0
    revenue = 0
    occupancy = []

    for d in range(1, DAYS + 1):
        t = T_str

        while t <= T_end:
            now = (d - 1) * 24 + t  # current time
            lam = get_lambda(d, t)

            # Remove cars whose stay is over
            while parked and parked[0] <= now:
                heapq.heappop(parked)

            # N(t) ~ Pois(λ)
            n = rng.poisson(lam)

            for _ in range(n):
                # S ~ Exp(1/E_S)
                s = rng.exponential(E_S)

                if len(parked) < C:
                    heapq.heappush(parked, now + s)
                    served += 1
                    revenue += s * P
                else:
                    lost += 1

            occupancy.append(len(parked))
            t += DT

    occupancy = np.array(occupancy)
    costs = K * V_WEEKLY

    return {
        "Scmp": served,
        "Slst": lost,
        "Wavg": occupancy.mean() / C * 100,
        "Wcf": occupancy.max() / C * 100,
        "Rgr": revenue,
        "Rnp": revenue - costs,
    }


rows = []
for K in K_VALUES:
    runs = pd.DataFrame([simulate_once(K) for _ in range(N_RUNS)])
    row = {"K": K}
    row.update(runs.mean().to_dict())
    rows.append(row)

df = pd.DataFrame(rows)

best_k = int(df.loc[df["Rnp"].idxmax(), "K"])
best_rnp = df.loc[df["K"] == best_k, "Rnp"].iloc[0]

print(df.round(2).to_string(index=False))
print(f"\nОптимальна кількість поверхів: K = {best_k}")

df.to_excel("parking_results.xlsx", index=False)

plt.plot(df["K"], df["Rnp"], marker="o", color="red")
plt.scatter(best_k, best_rnp, color="red", s=120, label=f"Оптимум K={best_k}")
plt.title("Чистий прибуток залежно від кількості поверхів")
plt.xlabel("K")
plt.ylabel("Rnp, грн/тиждень")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
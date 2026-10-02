import heapq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tabulate as tabulate
T_str = 7
T_end = 23
DAYS = 7
DT = 1             # Time step
N_RUNS = 100
E_S = 2            # Average car stay
P = 50             # Tarif
V = 50000          # Budget monthly
WEEKS_PER_MONTH = 52 / 12
CARS_PER_FLOOR = 50
K_VALUES = [1] 

# лист витрат 
Tax = 0.23 #  налог на прибуток
security = 50000 # охорона
Facility = 10000  # загальне обслуговування
rng = np.random.default_rng()

# приведення до 1 тижня 
def to_week(x):
    return x / WEEKS_PER_MONTH

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

        while t < T_end:
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
    expenses = to_week(K * V + security + K * Facility)
    profit_before_tax = revenue - expenses
    tax = max(0, profit_before_tax) * Tax
    net_profit = profit_before_tax - tax            

    return {
        "Scmp": served,
        "Slst": lost,
        "Wavg": occupancy.mean() / C * 100,
        "Wcf": occupancy.max() / C * 100,
        "Rgr": revenue,
        "Rnp": net_profit,
        "occupancy_history": occupancy,
    }

all_runs = {} 
rows = []
for K in K_VALUES:
    runs = pd.DataFrame([simulate_once(K) for _ in range(N_RUNS)])
    all_runs[K] = runs
    row = {"K": K}
    row.update(runs.drop(columns=["occupancy_history"]).mean().to_dict())
    rows.append(row)

df = pd.DataFrame(rows)

best_k = int(df.loc[df["Rnp"].idxmax(), "K"])
best_rnp = df.loc[df["K"] == best_k, "Rnp"].iloc[0]

print(df.round(2).to_markdown(index=False, tablefmt="grid"))
print(f"\nОптимальна кількість поверхів: K = {best_k}")

df.to_excel("parking_results.xlsx", index=False)

plt.plot(df["K"], df["Rnp"], marker="o", color = "red")
plt.scatter(best_k, best_rnp, color="red", s=120, label=f"Оптимум K={best_k}")
plt.title("Чистий прибуток залежно від кількості поверхів")
plt.xlabel("K")
plt.ylabel("Rnp, грн/тиждень")
plt.legend()
plt.grid(alpha=0.3)
plt.show()



# Гістограма для оптимального K
C_best = best_k * CARS_PER_FLOOR
occupancy_data = all_runs[best_k]["occupancy_history"].iloc[0]

plt.figure(figsize=(10, 6))
plt.hist(occupancy_data, bins=range(0, C_best + 5, max(1, C_best // 25)),
         color="skyblue", edgecolor="black")
plt.title(f"Гістограма кількості запаркованих машин (K = {best_k}, один прогон)")
plt.xlabel("Кількість запаркованих машин")
plt.ylabel("години")
plt.axvline(x=C_best, color="red", linestyle="--", linewidth=2,
            label=f"максимальна вмісткість ({C_best})")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
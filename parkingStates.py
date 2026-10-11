import sys
import pandas as pd
from tabulate import tabulate

sys.stdout.reconfigure(encoding="utf-8")


from oneRoofBy import (
    T_str, T_end, DAYS, E_S, P, V, CARS_PER_FLOOR, K_VALUES,
    Tax, security, Facility, get_lambda, to_week
)

M_QUEUE = 0     # довжина черги m (система з відмовами)
METRICS = ["ro", "q_0", "p_vidmovy", "p_q", "Q", "A",
           "k_zaniat", "L_q", "L_S", "W_q", "W_S", "D"]


HOURS_WEEK = (T_end - T_str) * DAYS            # 112 робочих годин за тиждень
LAMBDA = sum(get_lambda(d, t) for d in range(1, DAYS + 1)
             for t in range(T_str, T_end)) / HOURS_WEEK    # λ = Σλ(d,t) / HOURS_WEEK, авт./год
MU = 1 / E_S                                   # μ = 1 / E(S), авт./год на місце
R = LAMBDA / MU                                # r = λ / μ, навантаження (Ерланг)


def rho(c):
    """ro = λ / (c·μ): навантаження на один канал."""
    return LAMBDA / (c * MU)


def state_probs(c, m):
    """Граничні ймовірності q_k, k = 0..c+m.
    t_k = r^k / k!         (k ≤ c)
    t_{c+j} = t_c · ro^j   (j = 1..m)
    q_0 = 1 / Σ t_k,   q_k = t_k · q_0
    """
    t = [1.0]
    for k in range(1, c + 1):
        t.append(t[-1] * R / k)
    t += [t[c] * rho(c) ** j for j in range(1, m + 1)]
    q0 = 1.0 / sum(t)
    return [x * q0 for x in t]


def p_vidmovy(q):
    """p_vidmovy = q_{c+m}: усі канали та черга зайняті."""
    return q[-1]


def p_q(q, c, m):
    """p_q = Σ q_k, k = c..c+m-1: ймовірність потрапити в чергу."""
    return sum(q[c:c + m])


def rel_throughput(p_vid):
    """Q = 1 − p_vidmovy: відносна пропускна здатність."""
    return 1.0 - p_vid


def abs_throughput(Q):
    """A = λ · Q: абсолютна пропускна здатність, авт./год."""
    return LAMBDA * Q


def busy_channels(Q):
    """k_zaniat = r · Q: середня кількість зайнятих місць."""
    return R * Q


def queue_len(q, c, m):
    """L_q = Σ j · q_{c+j}, j = 1..m: середня довжина черги."""
    return sum(j * q[c + j] for j in range(1, m + 1))


def system_len(Lq, k_zaniat):
    """L_S = L_q + k_zaniat: середня кількість заявок у системі."""
    return Lq + k_zaniat


def wait_time(Lq):
    """W_q = L_q / λ: середній час очікування в черзі, год."""
    return Lq / LAMBDA


def system_time(Ls):
    """W_S = L_S / λ: середній час перебування в системі, год."""
    return Ls / LAMBDA


def hourly_net_profit(A, K):
    """D = (A·E(S)·P − Витрати_год) · (1 − Tax), якщо прибуток > 0.
    Витрати_год = (K·V + security + K·Facility) / (52/12) / HOURS_WEEK."""
    revenue = A * E_S * P
    expenses = to_week(K * V + security + K * Facility) / HOURS_WEEK
    profit = revenue - expenses
    return profit - max(0.0, profit) * Tax


# Розрахунок характеристик СМО для K поверхів (c = K·CARS_PER_FLOOR каналів) 
def analyze(K, m=M_QUEUE):

    c = K * CARS_PER_FLOOR
    q = state_probs(c, m)

    p_vid = p_vidmovy(q)
    Q = rel_throughput(p_vid)
    A = abs_throughput(Q)
    k_zan = busy_channels(Q)
    Lq = queue_len(q, c, m)
    Ls = system_len(Lq, k_zan)
    D = hourly_net_profit(A, K)

    return {
        "c": c, "K": K,
        "ro": rho(c), "q_0": q[0], "p_vidmovy": p_vid, "p_q": p_q(q, c, m),
        "Q": Q, "A": A, "k_zaniat": k_zan, "L_q": Lq, "L_S": Ls,
        "W_q": wait_time(Lq), "W_S": system_time(Ls),
        "D": D, "Rnp_week": D * HOURS_WEEK,
    }


#print 
def main():
    df = pd.DataFrame([analyze(K) for K in K_VALUES])

    table = df.set_index("c")[METRICS].T
    table.columns = [f"c = {c}" for c in table.columns]

    best = df.loc[df["D"].idxmax()]

    print(f"lambda = {LAMBDA:.3f} авт./год, mu = {MU:.3f} авт./год, "
          f"r = {R:.3f} Ерл, m = {M_QUEUE}\n")
    print(tabulate(table, headers="keys", tablefmt="grid", floatfmt=".3f"))
    print(f"\nОптимальна кількість поверхів: K = {int(best['K'])} ({int(best['c'])} місць)")
    print(f"Чистий прибуток: D = {best['D']:.2f} грн/год ({best['Rnp_week']:.0f} грн/тиждень)")


if __name__ == "__main__":
    main()
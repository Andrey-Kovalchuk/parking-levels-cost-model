# Economic Feasibility of Underground Parking Levels

A discrete-event simulation model designed to determine the optimal number of underground parking levels by maximizing weekly net profit, balancing stochastic customer arrival dynamics against maintenance costs.

---

##  Project Overview

This study formulates an optimization problem for underground parking capacity under stochastic, non-homogeneous vehicle arrival flows and variable parking durations. The primary goal is to find the number of floors ($K$) where marginal parking revenue outweighs the marginal operating cost of maintaining an additional level.

### System Specifications
* **Operating Hours:** 07:00 – 23:00 daily ($T_{str} = 7$, $T_{end} = 23$)[cite: 1]
* **Simulation Horizon:** 1 week ($T = 7$ days / 168 hours total) with a discrete step $\Delta t = 1$ hour[cite: 1]
* **Capacity:** 50 parking spots per floor ($C = 50 \times K$)[cite: 1]
* **Tariff ($P$):** 50 UAH / hour[cite: 1]
* **Maintenance Budget ($V$):** 50,000 UAH / month per level ($V_{\text{weekly}} = V / 4$)[cite: 1]
* **Loss System:** No waiting queue; arriving vehicles leave immediately if all spots are occupied ($S_{lst}$)[cite: 1].

---

##  Stochastic Parameters

### 1. Non-Homogeneous Poisson Arrival Process ($N(t) \sim \text{Pois}(\lambda_{d,t})$)
Vehicle arrival rates vary by day type and time interval:

* **Weekdays (Mon–Fri):**
  * Morning (07:00 – 10:00): $\lambda = 25$ cars/hour[cite: 1]
  * Midday (10:00 – 17:00): $\lambda = 20$ cars/hour[cite: 1]
  * Evening Peak (17:00 – 20:00): $\lambda = 40$ cars/hour[cite: 1]
  * Night (20:00 – 23:00): $\lambda = 15$ cars/hour[cite: 1]

* **Weekends (Sat–Sun):**
  * Daytime Peak (10:00 – 20:00): $\lambda = 30$ cars/hour[cite: 1]
  * Morning & Late Evening: $\lambda = 12$ cars/hour[cite: 1]

### 2. Service Time Distribution
* **Parking Duration:** Exponentially distributed $S \sim \text{Exp}(1/\mu)$ with mean service time $\mu = E(S) = 2$ hours[cite: 1].

---

##  Key Evaluation Metrics

The model executes $N = 100$ Monte Carlo iterations per capacity level to evaluate average performance indicators[cite: 1]:

| Metric | Notation | Description |
| :--- | :---: | :--- |
| **Served Customers** | $S_{cmp}$ | Total vehicles successfully admitted and serviced[cite: 1] |
| **Lost Customers** | $S_{lst}$ | Vehicles turned away due to zero available capacity[cite: 1] |
| **Average Occupancy** | $W_{avg}$ | Mean percentage of total capacity utilized throughout the week[cite: 1] |
| **Peak Utilization** | $W_{cf}$ | Maximum percentage of occupied spots reached during the run[cite: 1] |
| **Gross Revenue** | $R_{gr}$ | Total earnings generated from parking duration fees[cite: 1] |
| **Net Profit** | $R_{np}$ | $R_{gr} - (K \times V_{\text{weekly}})$[cite: 1] |

---

##  Stack & Implementation

* **Language:** Python 3.10+
* **Libraries:** `numpy`, `pandas`, `matplotlib`, `heapq`[cite: 1]
* **Event Handling:** Min-heap (`heapq`) priority queue to efficiently manage vehicle departure timestamps[cite: 1].

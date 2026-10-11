# Economic Feasibility of Underground Parking Levels

A discrete-event simulation model designed to determine the optimal number of underground parking levels ($K$) by maximizing weekly net profit, balancing stochastic customer arrival dynamics against operating expenses and corporate income tax.

---

## Project Overview

This study addresses capacity optimization for a multi-level underground parking facility under non-homogeneous vehicle arrival flows and variable parking durations. The primary objective is to identify the number of levels ($K \in [1, 9]$) where marginal parking revenue exceeds the marginal operating costs of adding and maintaining another floor.

### System Specifications

- **Operating Hours:** 07:00 - 23:00 daily ($T_{str} = 7$, $T_{end} = 23$)
- **Simulation Horizon:** 1 week ($DAYS = 7$, 168 hours total) with discrete evaluation step $\Delta t = 1$ hour
- **Capacity:** 50 parking spots per floor ($C = 50 \times K$)
- **Tariff ($P$):** 100 UAH / hour
- **Fixed Monthly Expenses:**
  - Security (`security`): 50,000 UAH / month
  - Floor Maintenance (`V`): 50,000 UAH / month per level
  - Facility Services (`Facility`): 10,000 UAH / month per level
- **Weekly Conversion:** $WEEKS\_PER\_MONTH = 52 / 12 \approx 4.333$
- **Corporate Tax Rate (`Tax`):** 23% applied to positive operating profit before tax
- **Loss System (M/M/c/c-type):** No waiting line; arriving vehicles leave immediately if all spots are occupied ($S_{lst}$)

---

## Stochastic Parameters

### 1. Non-Homogeneous Poisson Arrival Process ($N(t) \sim \text{Pois}(\lambda_{d,t})$)

Vehicle arrival rates vary by day of week ($d$) and hour ($t$):

- **Weekdays ($d \le 5$):**
  - Morning (07:00 - 10:00): $\lambda = 25$ cars/hour
  - Midday Peak (10:00 - 17:00): $\lambda = 20$ cars/hour
  - Evening Peak (17:00 - 20:00): $\lambda = 40$ cars/hour
  - Late Evening (20:00 - 23:00): $\lambda = 15$ cars/hour
- **Weekends ($d > 5$):**
  - Daytime Peak (10:00 - 20:00): $\lambda = 30$ cars/hour
  - Morning & Late Evening: $\lambda = 12$ cars/hour

### 2. Service Time Distribution

- **Parking Duration:** Exponentially distributed $S \sim \text{Exp}(1 / E\_S)$ with mean duration $E(S) = 2$ hours.

---

## Cost & Profit Accounting

Operating expenses are scaled down to a weekly baseline:

$$\text{Expenses}_{\text{weekly}} = \frac{K \times V + \text{security} + K \times \text{Facility}}{52 / 12}$$

Net profit calculation:

$$\Pi_{\text{before tax}} = R_{gr} - \text{Expenses}_{\text{weekly}}$$

$$R_{np} = \Pi_{\text{before tax}} - \max(0, \Pi_{\text{before tax}}) \times \text{Tax}$$

---

## Key Evaluation Metrics

The model executes $N = 100$ Monte Carlo iterations for each level $K \in \{1, \dots, 9\}$:

| Metric | Notation | Description |
| :--- | :---: | :--- |
| **Served Customers** | $S_{cmp}$ | Total vehicles successfully admitted and serviced |
| **Lost Customers** | $S_{lst}$ | Vehicles turned away due to zero available capacity |
| **Average Occupancy** | $W_{avg}$ | Mean percentage of total capacity utilized across operating hours |
| **Peak Utilization** | $W_{cf}$ | Maximum percentage of capacity reached during the simulation |
| **Gross Revenue** | $R_{gr}$ | Total revenue generated from parking fees (UAH / week) |
| **Net Profit** | $R_{np}$ | Net profit after weekly operating expenses and 23% tax (UAH / week) |

---

## Output & Optimization Summary

The multi-run simulation identifies an optimal capacity of **$K = 2$ floors**:

- **$K = 1$:** High lost customer count ($S_{lst} \approx 550 - 640$) due to heavy evening peak bottlenecks.
- **$K = 2$ (Optimum):** Satisfies over 99.8% of incoming demand ($S_{lst} \approx 0 - 5$), maximizing net profit ($R_{np} \approx 370,000 - 377,000$ UAH / week).
- **$K \ge 3$:** Demand is completely absorbed ($S_{lst} = 0$); each additional level adds maintenance and facility costs with zero marginal revenue, resulting in a linear decrease in net profit.

---

## Tech Stack & Setup

- **Language:** Python 3.10+
- **Libraries:** `numpy`, `pandas`, `matplotlib`, `tabulate`, `openpyxl`
- **Engine:** Priority queue (`heapq`) for tracking vehicle departure timestamps across days.

```bash
git clone [https://github.com/Andrey-Kovalchuk/parking-levels-cost-model.git](https://github.com/Andrey-Kovalchuk/parking-levels-cost-model.git)
cd parking-levels-cost-model
pip install numpy pandas matplotlib tabulate openpyxl
python main.py

# Economic Feasibility of Underground Parking Levels

A simulation-based optimization model designed to determine the optimal number of underground parking floors that maximizes net profit, balancing revenue against structural and operational maintenance expenses.

---

##  Project Overview

The objective is to identify the economically optimal depth (number of levels) for an underground parking facility subject to stochastic demand, finite capacity, and ongoing operational costs.

### System Specifications
* **Operating Hours:** 07:00 – 23:00 daily (16 operating hours/day)
* **Simulation Horizon:** 1 week with a discrete time step of $\Delta t = 1$ hour
* **Customer Arrivals:** Non-homogeneous stochastic arrival process partitioned into distinct demand periods based on time of day and day of the week
* **Parking Duration:** Exponentially distributed with a mean service time of $\mu = 2$ hours ($M/M/c/c$ queuing dynamics)
* **Capacity Constraints:** Each floor functions as a discrete capacity tier; incoming vehicles arriving when the parking is fully occupied are lost (loss system)

---

##  Economic Objective

Maximize total net profit:

$$\text{Net Profit} = \text{Total Parking Revenue} - \text{Floor Maintenance Costs}$$

* **Revenue:** Hourly parking tariff multiplied by total vehicle occupancy hours.
* **Costs:** Monthly operational and maintenance expenses scaled proportionally to the number of constructed levels.

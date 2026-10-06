Economic Feasibility of Underground Parking Levels

Monte Carlo simulation of a multi-channel loss system (no queue) that finds the optimal number of underground parking levels K by maximizing weekly net profit.

Model
Parameter	Value
Operating hours	07:00 – 23:00, step Δt = 1 h, horizon 1 week
Capacity	50 spots per level (C = 50·K), tested K = 1…9
Tariff	100 UAH / hour
Parking time	S ~ Exp(mean = 2 h)
Arrivals	N ~ Pois(λ(d, t)), 2,644 cars/week on average
Runs	100 per K

Arrival rates λ (cars/hour): Weekdays: 25 (07–10), 20 (10–17), 40 (17–20), 15 (20–23). Weekends: 30 (10–20), 12 otherwise.

Costs (UAH/month, converted to weeks by /(52/12)): 50,000 maintenance + 10,000 facility service per level, 50,000 fixed security, 23 % tax on positive profit.

Expenses(K) = (K·50,000 + 50,000 + K·10,000) / (52/12)
R_np = (R_gr − Expenses) − 0.23 · max(0, R_gr − Expenses)

A car that finds no free spot is lost (S_lst). Departures are tracked with a min-heap (heapq); the parking is cleared at 07:00 each day.

Metrics

S_cmp served cars · S_lst lost cars · W_avg mean occupancy, % · W_cf peak occupancy, % · R_gr gross revenue · R_np net profit.

Results (100 runs)
K	S_cmp	S_lst	W_avg, %	W_cf, %	R_gr	R_np, UAH/week
1	2091	552	87.75	100.00	419,573	303,525
2	2639	5	55.56	98.58	529,350	377,392
3	2644	0	37.03	69.04	528,685	366,218
5	2650	0	22.23	40.72	529,206	345,297
9	2649	0	12.35	22.95	529,013	302,501

Optimum: K = 2 (100 spots), ≈ 377 thousand UAH/week. With K = 1 about 21 % of customers are lost; for K ≥ 3 demand is fully served, so each extra level only adds ≈ 13.8 thousand UAH/week of cost. A single run is noisy (σ of R_np ≈ 11 thousand UAH), hence the averaging over 100 runs.

Limitations
Δt = 1 h overestimates losses near full capacity (K = 1, 2).
Capacity changes in steps of 50 spots, so K = 2 is the best tested option, not necessarily the exact optimum.
Capital expenditure is not included: R_np is an operating-profit estimate.
Usage
bash
pip install numpy pandas matplotlib tabulate openpyxl
python parking_simulation.py

Outputs: console table, parking_results.xlsx, plot of R_np vs K, occupancy histogram for the optimal K. All parameters are constants at the top of the script.

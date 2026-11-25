# Construction Risk Analyzer

A Python tool that reads a construction project's risk register from a CSV file, rates every risk, places them on a risk matrix, and runs a Monte Carlo simulation to estimate how much contingency (money and time) the project should set aside.

I built it as a second-year civil engineering student at McGill University, while learning Python, to understand how project managers and estimators actually quantify risk.

![Risk matrix](images/risk_matrix.png)

---

## Why I built this

On construction projects, a risk matrix tells you **which** risks matter most, but not **how much** money and time to put aside for them. You can't just add up every risk's cost (they won't all happen), and the average is too optimistic. This tool answers both questions:

1. **Which risks matter most?** Each risk gets a probability score, an impact score and a band (Low, Medium, High, Critical).
2. **How much contingency is needed?** A Monte Carlo simulation plays the project out 10,000 times and gives the P50 and P80 cost and delay.

---

## What it does

- **Loads a risk register** from a CSV file (made in Excel)
- **Rates probability** from a yearly chance, over the project's duration
- **Rates impact on three dimensions** (cost, delay, safety) and keeps the worst one
- **Uses official CNESST injury categories** (Quebec) for the safety rating
- **Prints a report** for each risk, a text risk matrix and a legend
- **Draws a colour heat map** of the risk matrix (matplotlib)
- **Runs a Monte Carlo simulation** (10,000 runs) and reports the expected risk cost, P50 and P80 for cost and delay, with a histogram

---

## Example: mid-size residential building

The example file `Montreal_building_Peel_RISKS.csv` is a realistic example project I built to test the tool: a $14M, 2-year building with two risks. **The values are illustrative estimates, not records from a real company.**

| Risk | Probability | Worst impact | Score |
|---|---|---|---|
| R1 General construction strike | 36% over the project → 3 (possible) | 1 (2-week delay is only 1.9% of the schedule) | **3 → Low** |
| R2 Contaminated soil | 51% → 4 (likely) | 5 (cost = 7.9% of budget) | **20 → Critical** |

**Monte Carlo results (10,000 runs)**

| | Result |
|---|---|
| Expected risk cost | $568,200 |
| P50 risk cost | $912,292 |
| **P80 risk cost (contingency)** | **$1,242,848 (8.9% of budget)** |
| P80 delay | 8.7 weeks (about 2 months): 26 months total instead of 24 |

![Monte Carlo histogram](images/monte_carlo_cost.png)

**What the histogram shows:** in almost half of the simulated projects, the contaminated soil doesn't happen and the risk cost is close to $0. In the other half, it costs around $1M. The expected value ($0.57M) sits in the gap and matches **neither** real outcome. That's exactly why a single average is a poor contingency, and why percentiles like P80 are used instead.

---

## Validation on a real public risk register

I also ran the tool on 7 risks from a published US Army Corps of Engineers cost and schedule risk analysis: the **Anchorage Port Modernization Project, Concept A** (December 2014, base cost about $541M, 84-month schedule). The file is `Anchorage_port_RISKS.csv`, and every row cites its source.

| | My model | Official report |
|---|---|---|
| P80 schedule | 111 months | 108 months |
| P80 cost contingency | 18.8% | 23% |

My model also ranks the same three risks at the top as the official register (change order growth, funding, project execution). It uses only 7 of the register's risks and simpler assumptions (see Limitations), so this is a sanity check, not a replacement for a professional analysis.

Source: [Anchorage Port Modernization Project, Appendix A, Cost and Schedule Risk Analysis](https://www.portofalaska.com/wp-content/uploads/AppendixA-CostEstimate.pdf)

---

## How it works

**1. Probability over the project**
The CSV gives a yearly chance `p`. Over a project of `T` years:

```
P(at least once) = 1 − (1 − p)^T
```

| Score | Label | Chance over the project |
|---|---|---|
| 1 | Rare | under 10% |
| 2 | Unlikely | 10–30% |
| 3 | Possible | 30–50% |
| 4 | Likely | 50–70% |
| 5 | Almost certain | 70% or more |

**2. Impact: three dimensions, keep the worst**

| Score | Cost (% of budget) | Delay (% of project duration) | Safety (CNESST category) |
|---|---|---|---|
| 1 | under 0.5% | under 2% | first aid / no injury |
| 2 | 0.5–1% | 2–5% | accident without lost time |
| 3 | 1–3% | 5–10% | accident with lost time |
| 4 | 3–5% | 10–25% | serious accident (LSST art. 62) |
| 5 | over 5% | 25% or more | death |

- **Delay** = (activity delay − float) ÷ working days per week, i.e. only the part of a delay that the schedule's float can't absorb.
- **Cost** = direct cost + delay weeks × weekly site overhead + penalties.
- Cost and delay are rated **as a % of the project's budget and duration**, so the same scale works for a $14M building or a $541M port. I first rated delay in weeks and found it made every risk on the large port project look critical, so I changed it.

**3. Score and band**
Score = probability × impact (1 to 25). Bands: 1–4 Low, 5–9 Medium, 10–16 High, 20–25 Critical.

**4. Monte Carlo**
For each of 10,000 runs, every risk "rolls the dice" against its probability. If it happens, its cost and delay vary between 75% and 150% of the estimate (triangular distribution, most likely 100%). The totals of all runs are sorted, and P50 and P80 are read from them.

---

## How to run it

**Requirements:** Python 3 and matplotlib (`pip install matplotlib`, or in Thonny: Tools → Manage packages).

1. Put the CSV file in the same folder as `risk_analyzer.py`.
2. Set the file name in the `open(...)` line and in `MC_CSV_FILE`.
3. Run `risk_analyzer.py`.

**CSV columns**

| Column | Meaning |
|---|---|
| Risk Name | name of the risk |
| Probability(%) | chance per year |
| Duration of project(years) | project duration |
| Situation description | CNESST safety term (e.g. `no injury`, `lost-time injury`, `décès`) |
| Activity Delay (Days) | working days of delay if the risk happens |
| Total Slack Days | float available on that activity |
| Direct Cost ($) | cost of the extra work |
| Weekly overhead ($) | site costs per extra week |
| penalties ($) | contract penalties |
| Budget ($) | project budget |

Save the file from Excel as **CSV UTF-8**, so French accents stay readable.

---

## Project structure

```
risk_analyzer.py                    the program
Montreal_building_Peel_RISKS.csv    example project
Anchorage_port_RISKS.csv            real public register (validation)
images/                             risk matrix and Monte Carlo charts
```

---

## Assumptions and limitations

- **Scale boundaries are illustrative.** Standards like ISO 31000 and PMI define the method, not the numbers; each organization calibrates its own scales.
- **Risks are treated as independent.** In reality some move together (a strike can push work into winter).
- **Delays add up**, as if every risk hits the critical path, which is conservative.
- **The 75%–150% variation range** is an assumption, not measured data.
- **The example building's values are estimates**, and the Anchorage file uses only the register's 7 risks with numerical impacts.

---

## What's next

- Evaluate the same risks under several organizations' scales and recommend the best fit for the project size
- Model correlated risks and add a sensitivity (tornado) chart
- Optimize which risk responses to fund (linear programming)
- Update risks automatically from daily and weekly site reports

---

## What I learned

- **Risk management:** probability and impact scales, the worst-dimension rule, critical path and float, contingency, P50/P80, and why a model is only as good as its assumptions
- **Python:** functions with parameters and multiple returns, loops and `enumerate`, lists of lists, reading CSV files with `csv.DictReader`, f-string formatting, matplotlib, and the `random` module
- **Habits:** keeping input separate from calculation, testing every function with values I could check by hand, and catching silent bugs that give wrong results without any error

---

## AI use

I learned Python on this project with Claude (Anthropic's AI assistant) as a tutor and code reviewer. I wrote the core of the program myself: the rating functions, the CSV loading, the report and the risk grid. At my request, the AI supplied the `evaluate_risk` function, the matrix printing and legend, the delay-scale update, the heat map and the Monte Carlo block, and it helped research sources. A detailed AI use log, listing exactly what I wrote and what the AI contributed, is available on request.

---

**Abdelhalim (Halim) Shahin**, civil engineering student, McGill University


# function that rates the probability of an event ot happen using P(\text{at least once}) = 1 - (1 - p)^{T}.
def calculate_probability(p,T):
    P=(1-((1-(p/100))**T))*100
    return P
#print(calculate_probability(0.2,4)) ----> test passes

# a function that takes that number and gives the label and score.
def rate_probability(probability):

    score=0
    label=""
    if probability<10:
        score+=1
        label=label+"rare"
    if probability>=10 and probability<30:
        score+=2
        label=label+"unlikely"
    if probability>=30 and probability<50:
        score+=3
        label=label+"possible"
    if probability>=50 and probability<70:
        score+=4
        label=label+"likely"
    if probability>=70:
        score+=5
        label=label+"almost certain"
    
        
    #print(f"the probability is {probability},thus the score is {score} and it is considered as {label}.")
    return(score,label)
        
# test :
#print(rate_probability())

def rate_safety(description_of_situation):
    
    if description_of_situation=="no injury" or description_of_situation=="first aid"or description_of_situation=="premiers soins" or description_of_situation=="premiers secours":
        safety_score=1
    elif description_of_situation=="medical treatment" or description_of_situation=="need to see a doctor"or description_of_situation=="accident sans perte de temps":
        safety_score=2
    elif description_of_situation=="lost-time injury" or description_of_situation=="fracture"or description_of_situation=="accident avec perte de temps":
        safety_score=3
    elif description_of_situation=="serious injury" or description_of_situation=="hospitalization"or description_of_situation=="accident grave":
        safety_score=4
    elif description_of_situation=="fatality"or description_of_situation=="décès":
        safety_score=5
    
#    else:
  #      while description_of_situation not in LIST_of_words:
  #          print("the term you entered is not found.please use the terms in the CNESST")
 #here i made the mistake to make an infite loop. the fix is to move the while before the if/elif chain.           
            
        
    return safety_score
#print(rate_safety())#---> works

def calculate_delay_in_weeks(activity_delay,total_float,T,working_days_per_week=5):
    delay_weeks=max(0,((activity_delay-total_float)/working_days_per_week))  # CHANGED: weeks kept for the cost
    project_delay=(delay_weeks/(T*52.143))*100                               # CHANGED: delay as % of project duration
    if project_delay< 2:                                                     # CHANGED: % limits
        score_delay=1
    elif project_delay >=2 and project_delay < 5:
        score_delay=2
    elif project_delay >=5 and project_delay <10:
        score_delay=3
    elif project_delay >=10 and project_delay <25:
        score_delay=4
    elif project_delay >=25:
        score_delay=5
    return delay_weeks,project_delay,score_delay                             # CHANGED: returns 3 values


#print(calculate_delay_in_weeks())

def calculate_cost_in_percentage(direct_cost,weekly_overhead,penalties,budget,delay_weeks):
    cost_in_percentage=((direct_cost+(delay_weeks*weekly_overhead)+penalties)/budget)*100
    if cost_in_percentage < 0.5:
        score_cost=1
    elif cost_in_percentage >= 0.5 and cost_in_percentage < 1:
        score_cost=2
    elif cost_in_percentage >= 1 and cost_in_percentage < 3:
        score_cost=3
    elif cost_in_percentage >= 3 and cost_in_percentage <= 5:
        score_cost=4
    elif cost_in_percentage >5:
        score_cost=5
    return score_cost,cost_in_percentage

def rate_impact(s,d,c):
    return max(s,d,c)
#print(rate_impact())

def calculate_score(impact_score,probability_score):
    return impact_score*probability_score
#print(calculate_score())

def classify_band(score):
    band="Invalid"
    if score>=1 and score <=4:
        band="Low"
    elif score>=5 and score <=9:
        band="Medium"
    elif score>=10 and score <=16:
        band="High"
    elif score>=20 and score <=25:
        band="Critical"
    else:
        print("somthing is wrong, score must range from 1 to 25")
    return band
#print(classify_band())
#must unpack the pair into two varaibles before the print then use the one i need only.
def evaluate_risk(name, p, T, term, activity_delay, total_float,direct_cost, weekly_overhead, penalties, budget):
    
    probability = calculate_probability(p, T)
    probability_score, probability_label = rate_probability(probability)

    
    safety_score = rate_safety(term)


    delay_weeks, delay_percent, delay_score = calculate_delay_in_weeks(activity_delay, total_float, T)  # CHANGED

    
    cost_score, cost_percent = calculate_cost_in_percentage(
        direct_cost, weekly_overhead, penalties, budget, delay_weeks)

    
    impact_score = rate_impact(safety_score, delay_score, cost_score)
    final_score = calculate_score(impact_score, probability_score)
    band = classify_band(final_score)

    
    print("==== RISK REPORT ====")
    print(f"{'Risk:':15}{name}")
    print(f"{'Probability:':15}{probability:.1f}% -> score {probability_score} ({probability_label})")
    print(f"{'Safety:':15}score {safety_score}")
    print(f"{'Delay:':15}{delay_weeks:.1f} weeks ({delay_percent:.1f}% of duration) -> score {delay_score}")  # CHANGED
    print(f"{'Cost:':15}{cost_percent:.1f}% of budget -> score {cost_score}")
    print(f"{'Impact:':15}score {impact_score} (worst dimension)")
    print(f"{'Risk score:':15}{final_score} -> {band}")

    return(name,probability_score,final_score,impact_score)


ACCEPTED_TERMS=["no injury","first aid","premiers soins","premiers secours","medical treatment","need to see a doctor","accident sans perte de temps","lost-time injury","fracture","accident avec perte de temps","serious injury","hospitalization","accident grave","fatality","décès"]

import csv

with open("Anchorage_port_RISKS.csv",encoding="utf-8-sig")as file:
    reader=csv.DictReader(file)
    results=[]
    for row in reader:
        risk_name= row["Risk Name"]
        probability_in_percentage=float(row["Probability(%)"])
        duration_in_years=float(row["Duration of project(years)"])
        situation_description=row["Situation description"]
        activity_delay_in_days= float(row["Activity Delay (Days)"])
        total_slack_days=float(row["Total Slack Days"])
        direct_cost=float(row["Direct Cost ($)"])
        weekly_overhead=float(row["Weekly overhead ($)"])
        penalities=float(row["penalties ($)"])
        budget=float(row["Budget ($)"])
        result=evaluate_risk(risk_name,probability_in_percentage,duration_in_years,situation_description,activity_delay_in_days,total_slack_days,direct_cost,weekly_overhead,penalities,budget)
        results.append(result)

#1 create empty cells:
grid=[]
for i in range(1,6):
    row=[]
    for i in range(1,6):
        cell=[]
        row.append(cell)
    grid.append(row)

for j,risk in enumerate(results,start=1):
    name,probability_score,final_score,impact_score=risk
    risk_label=f"R{j}"
    row_index=probability_score-1
    column_index=impact_score-1
    grid[row_index][column_index].append(risk_label)
    

print("   ", end="")                  # 3 spaces, above the "P5|" labels
for col in range(1, 6):
    print(f"I{col:<4}", end="|")      # "I1   " = 5 characters, same as each cell
print()
for probability in range(5, 0, -1):
    print(f"P{probability}", end="|")
    for impact in range(1, 6):
        cell = grid[probability-1][impact-1]
        if len(cell) == 0:
            print(f"{'.':5}", end="|")
        else:
            print(f"{','.join(cell):5}", end="|")
    print()


print()
for j, risk in enumerate(results, start=1):
    name, probability_score, final_score, impact_score = risk
    band = classify_band(final_score)
    print(f"R{j:<3}{name:30}{final_score:>3} → {band}")

    
    


# ---------- Monte Carlo simulation ----------
# Plays the project out many times with random risk outcomes, then reads P50 and P80.
import random
import matplotlib.pyplot as plt

MC_CSV_FILE = "Anchorage_port_RISKS.csv"   # same file as in the open(...) line above
RUNS = 10000
# Three-point estimate around each risk's value: low, most likely, high.
# Overruns tend to be bigger than savings, so the range is skewed to the high side.
LOW_FACTOR = 0.75
MOST_LIKELY_FACTOR = 1.0
HIGH_FACTOR = 1.5
random.seed(42)   # same random numbers every run, so results can be checked

# 1. Read each risk's probability, cost and delay (reusing your functions)
mc_risks = []
with open(MC_CSV_FILE, encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        p = float(row["Probability(%)"])
        T = float(row["Duration of project(years)"])
        activity_delay = float(row["Activity Delay (Days)"])
        total_float = float(row["Total Slack Days"])
        direct_cost = float(row["Direct Cost ($)"])
        weekly_overhead = float(row["Weekly overhead ($)"])
        penalties = float(row["penalties ($)"])
        budget = float(row["Budget ($)"])

        probability = calculate_probability(p, T)                      # % over the project
        delay_weeks, delay_percent, delay_score = calculate_delay_in_weeks(activity_delay, total_float, T)
        cost_if_happens = direct_cost + delay_weeks * weekly_overhead + penalties

        mc_risks.append([row["Risk Name"], probability, cost_if_happens, delay_weeks])

# 2. Expected value: probability x cost, added over all risks (a quick first contingency)
expected_cost = 0
for name, probability, cost_if_happens, delay_weeks in mc_risks:
    expected_cost = expected_cost + (probability / 100) * cost_if_happens

# 3. The simulation
total_costs = []
total_delays = []
for run in range(RUNS):
    run_cost = 0
    run_delay = 0
    for name, probability, cost_if_happens, delay_weeks in mc_risks:
        if random.random() < probability / 100:                        # does the risk happen this time?
            factor = random.triangular(LOW_FACTOR, HIGH_FACTOR, MOST_LIKELY_FACTOR)
            run_cost = run_cost + cost_if_happens * factor
            run_delay = run_delay + delay_weeks * factor               # assumes delays add up (critical path)
    total_costs.append(run_cost)
    total_delays.append(run_delay)

# 4. Read the percentiles from the sorted results
total_costs.sort()
total_delays.sort()
p50_cost = total_costs[int(RUNS * 0.50)]
p80_cost = total_costs[int(RUNS * 0.80)]
p50_delay = total_delays[int(RUNS * 0.50)]
p80_delay = total_delays[int(RUNS * 0.80)]
base_weeks = T * 52.143

print()
print("==== MONTE CARLO RESULTS ====")
print(f"{'Runs:':30}{RUNS}")
print(f"{'Base budget:':30}${budget:,.0f}")
print(f"{'Expected risk cost:':30}${expected_cost:,.0f}")
print(f"{'P50 risk cost:':30}${p50_cost:,.0f}")
print(f"{'P80 risk cost (contingency):':30}${p80_cost:,.0f}  ({p80_cost / budget * 100:.1f}% of budget)")
print(f"{'P80 total cost:':30}${budget + p80_cost:,.0f}")
print(f"{'P50 delay:':30}{p50_delay:.1f} weeks ({p50_delay / 4.345:.1f} months)")
print(f"{'P80 delay:':30}{p80_delay:.1f} weeks ({p80_delay / 4.345:.1f} months)")
print(f"{'P80 total duration:':30}{(base_weeks + p80_delay) / 4.345:.0f} months (base {base_weeks / 4.345:.0f})")

# 5. Histogram of the simulated risk costs (shows when the heat map window opens)
fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.hist([c / 1000000 for c in total_costs], bins=40, color="steelblue", edgecolor="white")
ax2.axvline(p50_cost / 1000000, color="orange", linestyle="--", label=f"P50 = ${p50_cost / 1000000:.1f}M")
ax2.axvline(p80_cost / 1000000, color="red", linestyle="--", label=f"P80 = ${p80_cost / 1000000:.1f}M")
ax2.set_xlabel("Total risk cost (million $)")
ax2.set_ylabel(f"Number of simulated projects (out of {RUNS})")
ax2.set_title("Monte Carlo: total risk cost")
ax2.legend()
fig2.savefig("monte_carlo_cost.png", dpi=200, bbox_inches="tight")


# ---------- Colour heat map ----------
import matplotlib.pyplot as plt

# 1. Grid of scores (probability x impact) for the colours
scores = []
for probability in range(1, 6):
    row = []
    for impact in range(1, 6):
        row.append(probability * impact)
    scores.append(row)

# 2. Draw the coloured grid (green = low, red = high)
fig, ax = plt.subplots(figsize=(7, 6))
image = ax.imshow(scores, cmap="RdYlGn_r", origin="lower", vmin=1, vmax=25)

# 3. Write the risk IDs in their cells (from the grid you already filled)
for probability in range(1, 6):
    for impact in range(1, 6):
        cell = grid[probability - 1][impact - 1]
        if len(cell) > 0:
            ax.text(impact - 1, probability - 1, "\n".join(cell),
                    ha="center", va="center", fontsize=11, fontweight="bold")

# 4. Axis labels 1-5 instead of 0-4, titles, colour scale
ax.set_xticks(range(5))
ax.set_xticklabels(range(1, 6))
ax.set_yticks(range(5))
ax.set_yticklabels(range(1, 6))
ax.set_xlabel("Impact")
ax.set_ylabel("Probability")
ax.set_title("Risk matrix")
fig.colorbar(image, ax=ax, label="Risk score (probability × impact)")

# 5. Save the image, then show it
plt.savefig("risk_matrix.png", dpi=200, bbox_inches="tight")
plt.show()

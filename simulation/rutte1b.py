"""
    Plan Rutte 1 is to let the virus spread in a controlled way. We have 3 flavors:
        a: R_control_1 = 1.5
        b: R_control_1 = 1.2
        c: R_control_1 = 1
"""

from environment.population import Population
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

params = {
    "R_free": 3,  # the basic reproduction rate
    "R_control": 1.2,  # the basic reproduction rate after government measures in the period 12 march - 8 april 2020
    "incubation_time_mu" : 5,  # days, poisson distributed
    "contagious_time_mu" : 6,  # days, poisson distributed
    "death_rt": 0.01,  # mortality rate (1%)
    "increased_death_rt": 0.05,  # mortality rate for over-capacity (1%)
    "duration_mu": 15,  # diseasue duration, poisson distributed.
    "infection_to_death_mu": 22,  # duration from infection to death, poisson distributed.
    "popsize": 17000000,  # pop of NL
    "carry_cap": 10000,  # ICU beds / 10%
    "test_rt" : 0.1,  # percentage that gets tested.
    "dur": 365
}

p = Population(params)
alarm_phase = False
t_alarm_end = -1
ending = False
for x in range(params['dur']):
    p.step()

    # The first measures came on march 12th. By then 5 people had died.
    if np.sum(p.deaths) >= 5 and not alarm_phase:
        p.R = params["R_control"]
    elif p.susceptible_popsize / params['popsize'] < 1/3 and p.infected[0] < params['carry_cap']:
        p.R = params['R_free']


infected_2 = p.infected[::-1].copy()

plt.figure()
plt.plot(infected_2,color='r')
plt.plot(np.ones(shape=(params['dur']))*params['carry_cap'],color='blue')
plt.show()

df = pd.DataFrame()
df['infections'] = p.infected[::-1]
df['deaths'] = p.deaths
df['confirmed_cases'] = p.confirmed
df['suspectible_pop'] = p.suspectible
df['popsize'] = params['popsize']
df['vulnerable_pop_pct'] = df['suspectible_pop'] / df['popsize']
df['disease_prevalence'] = df['infections'] / df['popsize']
df['carry_capacity_abs'] = params['carry_cap']
df['carry_capacity_pct'] = params['carry_cap'] / params['popsize']

df.to_excel('../data/sim_rutte_1b.xlsx')
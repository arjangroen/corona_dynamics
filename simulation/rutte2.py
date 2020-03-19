"""Plan Rutte 1 is to let the virus spread."""
from environment.population import Population
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

params = {
    "R_free": 3,  # the basic reproduction rate
    "R_control": 3,  # the basic reproduction rate after government measures in the period 12 march - 8 april 2020
    "incubation_time_mu" : 5,  # days, poisson distributed
    "contagious_time_mu" : 6,  # days, poisson distributed
    "death_rt": 0.01,  # mortality rate (1%)
    "increased_death_rt": 0.05,  # mortality rate for over-capacity (1%)
    "duration_mu": 15,  # disease duration, poisson distributed.
    "infection_to_death_mu": 22,  # duration from infection to death, poisson distributed.
    "popsize": 17000000,  # pop of NL
    "carry_cap": 10000,  # ICU beds / 10%
    "test_rt" : 0.1,  # percentage that gets tested.
    "dur": 365
}


simdur = params['dur']
p = Population(params)
for x in range(simdur):
    p.step()


infected_2 = p.infected[::-1].copy()

plt.figure()
plt.plot(infected_2,color='r')
plt.plot(np.ones(shape=(simdur))*params['carry_cap'],color='blue')
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



df.to_excel('../data/sim_rutte2.xlsx')
from environment.population import Population
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from params import *

simdur = 365
p = Population(dur=simdur)

for x in range(simdur):
    p.step()
    if p.R == R_1:
        print(x)

plt.figure()
plt.plot(p.infected[::-1],color='r')
plt.plot(p.deaths,color='k')
#plt.plot(p.confirmed,color='orange')
#plt.plot(np.array(p.suspectible)/10,color='green')
plt.plot(np.ones(shape=(simdur))*12000,color='blue')
plt.show()
print(p.infected)

df = pd.DataFrame()
df['infections'] = p.infected[::-1]
df['deaths'] = p.deaths
df['confirmed_cases'] = p.confirmed
df['suspectible_pop'] = p.suspectible

df.to_csv('simulation_outcome.csv')
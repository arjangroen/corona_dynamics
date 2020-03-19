# Corona Dynamics


##### author: Arjan Groen
### Usage:

#### Running a simulation 
```python
from environment.population import Population
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

params = {
    "R_free": 3,  # the basic reproduction rate
    "R_control": 1.5,  # the basic reproduction rate after government measures in the period 12 march - 8 april 2020
    "incubation_time_mu" : 5,  # days, poisson distributed
    "contagious_time_mu" : 6,  # days, poisson distributed
    "death_rt": 0.01,  # mortality rate (1%)
    "increased_death_rt": 0.05,  # mortality rate for over-capacity (1%)
    "duration_mu": 15,  # diseasue duration, poisson distributed.
    "infection_to_death_mu": 22,  # duration from infection to death, poisson distributed.
    "popsize": 17000000,  # pop of NL
    "carry_cap": 10000,  # ICU beds / 10%
    "test_rt" : 0.1,  # percentage that gets tested.
    "dur": 365  # simulation duration 
}

p = Population(params)
alarm_phase = False
t_alarm_end = -1
ending = False
for x in range(params['dur']):
    p.step()
```

### Plotting the results
```python
plt.figure()
plt.plot(infected_2,color='r')
plt.plot(np.ones(shape=(params['dur']))*params['carry_cap'],color='blue')
plt.show()
```


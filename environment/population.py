"""Class for managing a single population"""
from environment.utils import get_logistic_growth_rate
import numpy as np
from scipy.stats import poisson


class Population(object):

    def __init__(self, params):
        self.t = 0
        self.infected = np.zeros(
            shape=(params['dur']))  # Number of infected persons ordered from most recent to historic.
        self.infected[0] = 100  # Initial immigration of infections
        self.confirmed = np.zeros(shape=(params['dur']))  # Estimated confirmed cases
        self.suspectible = []  # Susceptible population over time.
        self.deaths = np.zeros(shape=(params['dur']))  # Deceased population over time
        self.susceptible_popsize = params['popsize']
        self.R = params['R_free']

        # Initial transmission rate. Poisson distribution scaled by reproductive number.
        self.transmission_rate = np.array(
            [self.R * poisson.pmf(k=k, mu=params['contagious_time_mu']) for k in range(params['dur'])])
        self.params = params

    def step(self):
        """
        Simulate 1 day of Corona pandemic.
        """
        susceptible_pop_rt = self.susceptible_popsize / self.params['popsize']
        new_cases = np.sum(self.infected[:self.params['dur']] * self.transmission_rate * susceptible_pop_rt)
        self.susceptible_popsize -= new_cases
        self.suspectible.append(self.susceptible_popsize)
        self.infected[1:] = self.infected[:-1]
        self.infected[0] = new_cases
        if self.t >= self.params['infection_to_death_mu']:
            self.deaths[self.t] = min(self.infected[self.params['infection_to_death_mu']], self.params['carry_cap']) * \
                                  self.params['death_rt'] + max(
                self.infected[self.params['infection_to_death_mu']] - self.params['carry_cap'], 0) * \
                                  self.params['increased_death_rt']
        self.transmission_rate = np.array(
            [self.R * poisson.pmf(k=k, mu=self.params['contagious_time_mu']) for k in range(self.params['dur'])])
        if self.t > self.params['incubation_time_mu']:
            self.confirmed[self.t] = self.infected[self.params['contagious_time_mu']] * self.params['test_rt']
        self.t += 1

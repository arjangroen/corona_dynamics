"""Class for managing a single population"""
from environment.utils import get_logistic_growth_rate
import numpy as np
from scipy.stats import poisson
from params import R_0, R_1, R_2, incubation_time_mu, death_rt, ICU_rt, time_to_death, duration_mu, test_rt, \
    awareness_treshholds


class Population(object):

    def __init__(self, popsize=16000000, emergency_level=0, dur=10000):
        self.t = 0
        self.dur = dur
        self.popsize = popsize
        self.suspectible_popsize = popsize
        self.infected = np.zeros(shape=(dur))
        self.infected[:10] = [x**2 for x in range(10)][::-1]
        self.confirmed = np.zeros(shape=(dur))
        self.suspectible = []
        self.deaths = np.zeros(shape=(dur))
        self.R = R_0
        self.awarenss_treshholds = awareness_treshholds
        if emergency_level == 1:
            self.R = R_1
        elif emergency_level == 2:
            self.R = R_2
        self.transmission_rate = np.array([self.R * poisson.pmf(k=k, mu=incubation_time_mu) for k in range(dur)])

    def step(self):
        suspectible_pop_rt = self.suspectible_popsize / self.popsize
        new_cases = np.sum(self.infected[:self.dur] * self.transmission_rate * suspectible_pop_rt)
        self.suspectible_popsize -= new_cases
        self.suspectible.append(self.suspectible_popsize)
        self.infected[1:] = self.infected[:-1]
        self.infected[0] = new_cases
        if self.t >= time_to_death:
            self.deaths[self.t] = self.infected[time_to_death] * death_rt
        if self.deaths[self.t] > self.awarenss_treshholds[1]:
            self.R = R_2
            self.transmission_rate = np.array(
                [self.R * poisson.pmf(k=k, mu=incubation_time_mu) for k in range(self.dur)])
        elif self.deaths[self.t] > self.awarenss_treshholds[0]:
            self.R = R_1
            self.transmission_rate = np.array(
                [self.R * poisson.pmf(k=k, mu=incubation_time_mu) for k in range(self.dur)])
        else:
            self.R = R_0
            self.transmission_rate = np.array(
                [self.R * poisson.pmf(k=k, mu=incubation_time_mu) for k in range(self.dur)])

        if self.t > incubation_time_mu:
            self.confirmed[self.t] = self.infected[incubation_time_mu] * test_rt
        self.t += 1

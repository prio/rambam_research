import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style='ticks')
import datetime as dt
from dataclasses import dataclass
from functools import partial
from utils import *



def random_points(v, n):
    return np.abs(np.random.normal(np.mean(v), np.std(v), n))

def to_times(hour, num): 
    return [x+(60 * hour) for x in range(int(num))]

def flatten(l): 
    return [item for sublist in l for item in sublist]

def find_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

import scipy.stats as stats


def normal(mu, sigma):
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)    
    return x,y


def poisson(mu, sigma):
    dist = stats.poisson(mu)
    x = np.arange(-1, 15)
    y = dist.pmf(x)    
    return x,y


def constant(mu, sigma):
    x = np.linspace(stats.uniform.ppf(0.01),
                    stats.uniform.ppf(0.99), 100)
    y = stats.uniform.pdf(x)
    return x, y


def erlang(mu, sigma):
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    y = stats.gamma.pdf(x, int(mu))
    return x, y


def plot_distribution(arr, points=None, dist=normal, title='', **kwds):
    mu = np.mean(arr)
    variance = np.std(arr)
    sigma = math.sqrt(variance)
    x, y = dist(mu, sigma)

    fig = plt.figure()
    fig.text(.85, .85, f'$\mu$: {mu:.2f}', horizontalalignment='right', verticalalignment='top')
    fig.text(.85, .8, f'$\sigma$: {variance:.2f}', horizontalalignment='right', verticalalignment='top')

    if points is not None:
        ys = []
        for aph in points:
            ys.append(y[find_idx(x, aph)])        
        fig.text(.85, .75, f'$n$: {len(points)}', horizontalalignment='right', verticalalignment='top')
        plt.scatter(points, ys, c='red')
        
    plt.vlines(mu, y.min(), y.max(), ls='--', alpha=0.5, colors='green')
    plt.vlines(mu-variance, y.min(), y.max(), ls='--', alpha=0.5, colors='yellow')
    plt.vlines(mu+variance, y.min(), y.max(), ls='--', alpha=0.5, colors='yellow')
    plt.yticks([])
    plt.title(title)
    return plt.plot(x, y, **kwds) 


df = load_csv('dataset_3')

hourly_arrivals = df.sort_values(by='entry_date')
hourly_arrivals = (hourly_arrivals.resample('h', on='entry_date')
                                  .count()
                                  .sort_index()['patient_id']
                                  .reset_index()
                                  .rename({'patient_id': 'arrivals'}, axis=1))

arrivals_per_hour = random_points(hourly_arrivals.arrivals, 24)
arrival_times = flatten([to_times(*args) for args in enumerate(arrivals_per_hour)])
n = len(arrival_times)
los = random_points(df.los_hrs, n)

pltdist = partial(plot_distribution, df.los_hrs);
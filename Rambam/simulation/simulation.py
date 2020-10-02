import streamlit as st
import time
import numpy as np
import pandas as pd
import datetime as dt
from dataclasses import dataclass
from matplotlib import pyplot as plt
import scipy.stats as stats


def to_times(hour, num): 
    return [x+(60 * hour) for x in range(int(num))]


def flatten(l): 
    return [item for sublist in l for item in sublist]


def someone_has_arrived(clock, arrival_times):
    return len(arrival_times) > 0 and clock >= arrival_times[0]


def random_normal(v, n):
    return np.abs(np.random.normal(np.mean(v), np.std(v), n))


# def random_poisson(v, n):
#     points = random_normal(v, n)
    
#     dist = stats.poisson(mu)
#     x = np.arange(-1, 15)
#     y = dist.pmf(x)    
#     ys = []
#     for aph in points:
#         ys.append(y[find_idx(x, aph)])   


@dataclass
class Patient:
    arrival_time: float
    discharge_time: float
        
    def __hash__(self):
        return hash((self.arrival_time, self.discharge_time))

    
class WaitingArea(object):
    def __init__(self):
        self._waiting = set()
        self._discharged = set()
        
    def add(self, patient:Patient):
        self._waiting.add(patient)
    
    def discharge(self, patient:Patient):
        self._discharged.add(patient)
    
    def __iter__(self):
        for patient in self._waiting - self._discharged:
            yield patient
    
    def __repr__(self):
        return f'WaitingArea(Waiting: {len(self.waiting)}. Arrived: {len(self.arrived)}. Discharged: {len(self.discharged)})'
    
    @property
    def arrived(self):
        return self._waiting
    @property
    def discharged(self):
        return self._discharged
    @property
    def waiting(self):
        return self._waiting - self._discharged


def simulate(arrival_times, wait_times):
    """Simulate a waiting area.
    
        arrival_times: A list of minutes from 0 each item represents an arrival
        wait_times: The wait time for the current 
    """
    waiting_area = WaitingArea()
    _arrival_times = arrival_times.copy()
    _wait_times = wait_times.copy()

    for current_time in range(24*60):    
        if someone_has_arrived(current_time, _arrival_times):
            waiting_area.add(
                Patient(arrival_time=_arrival_times.pop(0), 
                        discharge_time=current_time + _wait_times.pop(0))
            )

        for patient in waiting_area:
            if current_time >= patient.discharge_time:
                waiting_area.discharge(patient)
    
    return waiting_area    


def get_arrival_times(df, date):
    a_day = df[df.entry_date.dt.date == date].sort_values(by='entry_date')
    a_day = (a_day.resample('min', on='entry_date')
                  .count()
                  .sort_index()['patient_id']
                  .reset_index()
                  .rename({'patient_id': 'arrivals'}, axis=1))
    a_day['minutes'] = (a_day.entry_date.dt.hour * 60) + a_day.entry_date.dt.minute
    a_day = a_day[a_day.arrivals > 0][['minutes', 'arrivals']]
    
    return list(a_day.minutes.values) 


def run_simulation(arrivals, los_hrs):
    # Pick a day at random
    #date = df.entry_date.dt.date.sample(1).values[0]
    #arrival_times = get_arrival_times(df, date)
    
    # Pick hourly arrival values from a normal distribution
    arrivals_per_hour = random_normal(arrivals, 24)
    arrival_times = flatten([to_times(*args) for args in enumerate(arrivals_per_hour)])
    n = len(arrival_times)

    # Pick LoS values from a normal distribution
    los = random_normal(los_hrs, n)    
    los_mins = list(los * 60)

    return simulate(arrival_times, los_mins)


def run_x_simulations(df, x):
    # Mean hourly arrival rate
    # Std dev hourly arrival rate
    hourly_arrivals = df.sort_values(by='entry_date')
    hourly_arrivals = (hourly_arrivals.resample('h', on='entry_date')
                                      .count()
                                      .sort_index()['patient_id']
                                      .reset_index()
                                      .rename({'patient_id': 'arrivals'}, axis=1))

    eod = pd.DataFrame(columns=['Arrived', 'Discharged', 'Waiting at EOD'])
        
    my_bar = st.progress(0)        
    if x != 0:        
        one_pc = 1.0/x
    
    for step in range(x):
        waiting_area = run_simulation(hourly_arrivals.arrivals, df.los_hrs)    
        a = pd.Series(
            [len(i) for i in 
              [waiting_area.arrived, waiting_area.discharged, waiting_area.waiting]], 
            index=eod.columns
        )
        eod = eod.append(a, ignore_index=True)
        my_bar.progress(one_pc * step)
    my_bar.empty()
    return eod


@st.cache
def load_df():
    df = pd.read_csv(f'../data/wz2017_dataset_3.csv.gz')
    df.entry_date = pd.to_datetime(df.entry_date)    
    return df
    

@st.cache
def get_actual_eod_means(df):
    df = df.copy()
    df['entry_day'] = pd.to_datetime(df.entry_date).dt.floor('d')
    df['exit_day'] = pd.to_datetime(df.exit_date).dt.floor('d')
    arrived = df.groupby('entry_day').patient_id.count()
    discharged = df[df.entry_day == df.exit_day].groupby('entry_day').patient_id.count()
    waiting = arrived - discharged    
    return pd.DataFrame.from_dict(
        {'Arrived': arrived.values, 
         'Discharged': discharged.values, 
         'Waiting at EOD': waiting.values}
    )    


def create_chart(results):
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        
    arrived = results['Arrived'].values
    discharged = results['Discharged'].values
    waiting = results['Waiting'].values
    labels = results.index.values

    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots()
    r1 = np.arange(len(arrived))
    r2 = [x + width for x in r1]
    r3 = [x + width for x in r2]

    rects1 = ax.bar(r1, arrived, width, label='Arrived')
    rects2 = ax.bar(r2, discharged, width, label='Discharged')
    rects3 = ax.bar(r3, waiting, width, label='Waiting')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('People')
    plt.xticks([r + width for r in range(len(arrived))], labels)
    ax.legend()
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.tight_layout()
    return fig

# main
st.title('Waiting Room Simulation')
st.write("""
A simulation of a $G_t/GI/\infty$ model.
""")
df = load_df()
actual_eod = get_actual_eod_means(df)
                
num_of_sims = st.sidebar.text_input('# of simulations', 0)

def run(x):
    x = int(x)
    eod = run_x_simulations(df, x=x)
    results = pd.DataFrame.from_dict({
        '': ['Simulated', 'Actual'],
        'Arrived': [eod.Arrived.mean(), actual_eod.Arrived.mean()],
        'Discharged': [eod.Discharged.mean(), actual_eod.Discharged.mean()],
        'Waiting': [eod['Waiting at EOD'].mean(), actual_eod['Waiting at EOD'].mean()],
    }).set_index('').round()
    st.pyplot(fig=create_chart(results))
    #st.write(results)

if st.sidebar.button('Run Simulation'):
    run(num_of_sims)
else:
    run(0)
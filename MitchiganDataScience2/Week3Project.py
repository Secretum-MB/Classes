# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 08:26:57 2017

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

population_1 = np.random.normal(loc=.40, scale=.15, size=10000)
population_2 = np.random.normal(loc=.50, scale=.05, size=10000)
population_3 = np.random.normal(loc=.50, scale=.25, size=10000)
population_4 = np.random.normal(loc=.70, scale=.005, size=10000)

df = pd.DataFrame({'pop1': population_1,
                   'pop2': population_2,
                   'pop3': population_3,
                   'pop4': population_4})
stand_dev = df.std()


def build_graph():
    def onclick(event):
#        plt.cla()
#        plt.plot(data)
#        plt.gca().set_title('Event at Pixels %d' % ('double' if event.dblclick else 'single'))
        print('Event at Pixels %d' % ('double' if event.dblclick else 'single'))

    plt.bar(range(4),[np.mean(df['pop1']),np.mean(df['pop2']),np.mean(df['pop3']),np.mean(df['pop4'])], align='center',
            yerr=stand_dev)
    plt.xticks(np.arange(4), ('US','UK','Brazil','China'))

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

build_graph()
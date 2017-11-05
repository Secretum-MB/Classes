# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 08:26:57 2017

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats as stats

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
    def color_assign(selected_bar):
        if selected_bar > 2.6:      bar = population_4
        elif selected_bar > 1.6:    bar = population_3
        elif selected_bar > 0.6:    bar = population_2
        else:                       bar = population_1
        t_tests = []
        for country in [population_1, population_2, population_3, population_4]:
            t_tests.append(stats.ttest_ind(bar, country, equal_var=False)[0])
        colors = []
        for i in t_tests:
            if i >= 50:     colors.append('#0A36EB')
            elif i >= 10:   colors.append('#6C84E7')
            elif i == 0:    colors.append('#FFFFFF')
            elif i >= -10:  colors.append('#F19191')
            else:           colors.append('#FF0202')
        return colors
    
    def onclick(event):
        #plt.gca().set_title('Event at Pixels %s' % ('double' if event.dblclick else 'single'))
        counter = 0
        for i in color_assign(event.xdata):
            bar_graph[counter].set_color(i)
            bar_graph[counter].set_edgecolor('black')
            counter += 1
        plt.show()

    bar_graph = plt.bar(range(4),[np.mean(df['pop1']),np.mean(df['pop2']),np.mean(df['pop3']),np.mean(df['pop4'])], 
                        align='center', yerr=stand_dev)
    plt.xticks(np.arange(4), ('US','UK','Brazil','China'))

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

build_graph()

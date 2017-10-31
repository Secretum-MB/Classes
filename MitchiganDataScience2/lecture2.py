#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 19:20:35 2017

"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

normal_sample = np.random.normal(loc=0.0, scale=1.0, size=10000)
random_sample = np.random.random(10000)
gamma_sample = np.random.gamma(2, size=10000)

df = pd.DataFrame({'normal':normal_sample,
                   'random':random_sample,
                   'gamma': gamma_sample})
#print(df.describe())
#print(df.head())

plt.figure()
plt.boxplot([df['normal'],df['random'],df['gamma']], whis='range')

plt.figure()
plt.hist(df['gamma'], bins=100)

# The below will allow us to place a graph inside another one (inset)

import mpl_toolkits.axes_grid1.inset_locator as mpl_il
plt.figure()
plt.boxplot([df['normal'],df['random'],df['gamma']], whis='range')
ax2 = mpl_il.inset_axes(plt.gca(), width='60%',height='40%', loc=2)
ax2.hist(df['gamma'], bins=100)
ax2.margins(x=0.5)
ax2.yaxis.tick_right()

plt.figure()
plt.boxplot([df['normal'],df['random'],df['gamma']]) # pointns outside of whiskers are outliers

plt.figure()
Y = np.random.normal(loc=0.0, scale=1.0, size=10000)
X = np.random.random(10000)
plt.hist2d(X, Y, bins=25)

plt.figure()
plt.hist2d(X, Y, bins=100)
plt.colorbar()



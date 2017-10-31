#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 19:59:59 2017

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

n = 100
x = np.random.randn(n)

def update(curr):
    if curr == n:
        a.event_source.stop()
    plt.cla()
    bins = np.arange(-4, 4, 0.5)
    plt.hist(x[:curr], bins=bins)
    plt.axis([-4,4,0,30])
    plt.gca().set_title('Sampling the Normal Distribution')
    plt.gca().set_ylabel('Frequency')
    plt.gca().set_xlabel('Value')
    plt.annotate('n= %s' % curr, [3,27])
    
#figure = plt.figure()
#a = animation.FuncAnimation(figure, update, interval=100)

# Even driven graphic
plt.figure()
data = np.random.randn(10)
plt.plot(data)

def onclick(event):
    plt.cla()
    plt.plot(data)
    plt.gca().set_title('Event at Pixels {},{} {}and data {},{}'.format(event.x,
                                                                       event.y,
                                                                       '\n',
                                                                       event.xdata,
                                                                       event.ydata))
plt.gcf().canvas.mpl_connect('button_press_event', onclick)

from random import shuffle

origins = ['China','Brazil','India','USA','Canada','UK','Germany','Iraq','Chile','Mexico']
shuffle(origins)

df = pd.DataFrame({'height': np.random.rand(10),
                   'weight': np.random.rand(10),
                   'origin': origins})

plt.figure()
plt.scatter(df['height'],df['weight'], picker=5)
plt.gca().set_ylabel('Weight')
plt.gca().set_xlabel('Height')

def onpick(event):
    origin = df.iloc[event.ind[0]]['origin']
    plt.gca().set_title('Selected item came from {}'.format(origin))
    
plt.gcf().canvas.mpl_connect('pick event', onpick)

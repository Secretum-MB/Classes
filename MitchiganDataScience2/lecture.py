#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 18:10:09 2017

"""

import matplotlib.pyplot as plt
import numpy as np

linear_data = np.array([1,2,3,4,5,6,7,8])
exponential_data = linear_data ** 2

# SUBPLOTS
fig1, ((ax1,ax2,ax3), (ax4,ax5,ax6), (ax7,ax8,ax9)) = plt.subplots(3, 3, sharex=True, sharey=True)
ax5.plot(exponential_data, '-')
ax9.plot(linear_data, '-')

#HISTOGRAMS
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2, 2, sharex=True)

axs = [ax1,ax2,ax3,ax4]
for n in range(0,len(axs)):
    sample_size = 10**(n+1)
    sample = np.random.normal(loc=0.0, scale=1.0, size=sample_size)
    axs[n].hist(sample)
    axs[n].set_title('n=%s' % sample_size)

# notice that as sample sizes increase, the width of the bins increase as more probably outliers
# force more samples into the same bins (because there are only 10 bins per graph, because 
# we decided to share x values in line 20)
    
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2, 2, sharex=True)

axs = [ax1,ax2,ax3,ax4]
for n in range(0,len(axs)):
    sample_size = 10**(n+1)
    sample = np.random.normal(loc=0.0, scale=1.0, size=sample_size)
    axs[n].hist(sample, bins=100)
    axs[n].set_title('n=%s' % sample_size)

# now that we have 100 bins in each graph, the normal distribution looks great at large samp size.

import matplotlib.gridspec as gridspec

plt.figure()

gspec = gridspec.GridSpec(3,3)

top_histogram = plt.subplot(gspec[0,1:])
side_histogram = plt.subplot(gspec[1:,0])
lower_histogram = plt.subplot(gspec[1:,1:])

# the GridSpec line created a 3 by 3 figure, the list splicing is applied to that figure. 
# the [row,column]

y = np.random.normal(loc=0.0, scale=1.0, size=10000)
x = np.random.random(10000)

lower_histogram.scatter(x,y)
top_histogram.hist(x, bins= 100)
side_histogram.hist(y, bins=100, orientation='horizontal')

top_histogram.clear()
top_histogram.hist(x, bins= 100, normed=True)
side_histogram.clear()
side_histogram.hist(y, bins=100, orientation='horizontal', normed=True)
side_histogram.invert_xaxis()

# to 
for ax in [top_histogram, lower_histogram]:
    ax.set_xlim(0,1)
for ax in [side_histogram, lower_histogram]:
    ax.set_ylim(-5,5)



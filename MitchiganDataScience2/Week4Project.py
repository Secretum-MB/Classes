#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:32:34 2017

"""

import pandas as pd
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt

# load first data set
df = pd.read_csv('redfin_seattle.csv', index_col=20)
df = df[['Median Sale Price', 'Period End']]

# fixing sales price
df['Med Sale Price-temp'] = df['Median Sale Price'].str[1:-1]
df['Med Sale Price'] = df['Med Sale Price-temp'].str.replace(',','')
df['Med Price'] = df['Med Sale Price'].astype(float)

# removing bad locations
df['location'] = df.index
df = df.where(df['location'].str.startswith('Seattle, WA -'))
df.dropna(inplace=True)

# add date column readable by matplotlib 
format_date = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in df['Period End']]
df['new date'] = format_date

# Label Locations that will be kept for further analysis
desired = ['Seattle, WA - Ballard', 'Seattle, WA - Northgate', 'Seattle, WA - Queen Anne',
           'Seattle, WA - University District', 'Seattle, WA - Capitol Hill']
df['desired_locations'] = np.where(df.index.isin(desired), 'Yes', 'No')

# Add average cost accross all seattle for each period
pivot_foravg = df.pivot_table('Med Price', ['new date'], df.index)
pivot_foravg['Seattle_Avg'] = pivot_foravg[:].mean(axis=1, skipna=True)

# Remove locations that will not be individually analyzed
df = df.where(df['desired_locations'] == 'Yes')
df.dropna(inplace=True)

# Add new pivot table without all locations, add city average to it
pivot = df.pivot_table('Med Price', ['new date'], df.index)
pivot['Seattle_Avg'] = pivot_foravg['Seattle_Avg']


# load second dataset
df2 = pd.read_csv('Unemployment_Rate_Chart.csv', index_col=0)

# reformat dates
format_date = [dt.datetime.strptime(d,'%m/%d/%Y %H:%M:%S %p').date() for d in df2.index]
df2['newdate'] = format_date
df2.set_index('newdate', inplace=True)

# reformat percentages into floats
df2['Unemployment'] = df2['Seattle'].str[:-1].astype(float)

# merge the two data sets
merged_data = pivot.merge(df2[['Unemployment']], how='left', left_index=True, right_index=True)

# will need this for plot
home_columns = ['Seattle, WA - Ballard', 'Seattle, WA - Northgate', 'Seattle, WA - Queen Anne',
           'Seattle, WA - University District', 'Seattle, WA - Capitol Hill']
home_towns = ['Ballard', 'Northgate', 'Queen Anne', 'University District', 'Capitol Hill']

# build plot of merged data frame
fig, homes = plt.subplots()
homes.plot(merged_data.index, merged_data[home_columns], label=home_towns)

homes.set_ylabel('Home Prices (thousands)')
homes.set_xlabel('Year')

employment = homes.twinx()
employment.plot(merged_data.index, merged_data[['Unemployment']], 'k-', label='Unemployment')

employment.set_ylabel('Unemployment (%)')

# Add legend to chart
lines, labels = homes.get_legend_handles_labels()
lines2, labels2 = employment.get_legend_handles_labels()
fig.legend(lines + lines2, labels + labels2)



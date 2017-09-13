#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:59:03 2017

"""

import numpy as np
import pandas as pd

# import Energy Indicators.xls data and clean up data
energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skip_footer=38, index_col=1, na_values='...')
energy = energy.drop('Unnamed: 0',1)
energy = energy.drop('Unnamed: 2',1)
energy.columns = ['Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy.index.name = 'Country'

# converting petajoules to gigajoules
energy['Energy Supply'] = energy['Energy Supply'] * 1000000

energy = energy.rename({'Republic of Korea': 'South Korea', 'United States of America': 'United States',
                        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
                        'China, Hong Kong Special Administrative Region': 'Hong Kong',
                        'Bolivia (Plurinational State of)': 'Bolivia', 'Falkland Islands (Malvinas)': 'Falkland Islands',
                        'Iran (Islamic Republic of)': 'Iran', 'Micronesia (Federated States of)': 'Micronesia',
                        'Sint Maarten (Dutch part)': 'Sint Maarten', 'Venezuela (Bolivarian Republic of)': 'Venezuela'})
# Switzerland looked okay from start. Was supposed to need cleaning up??

print(energy.to_string())

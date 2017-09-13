#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 20:59:03 2017

"""

import numpy as np
import pandas as pd


# Question 1:
# load the Energy Indicators.xls data and clean it up
energy = pd.read_excel('Energy Indicators.xls', skiprows=17, index_col=2, 
                       skip_footer=38, na_values='...')
energy = energy.drop('Unnamed: 0', 1)
energy = energy.drop('Unnamed: 1', 1)
energy.index.name = 'Country'
energy.columns = ['Energy Supply', 'Energy Supply per Capita', '% Renewable']

energy['Energy Supply'] = energy['Energy Supply'] * 1000000
energy.rename({'Republic of Korea': 'South Korea',
               'United States of America20': 'United States',
               'United Kingdom of Great Britain and Northern Ireland19': 'United Kingdom',
               'China, Hong Kong Special Administrative Region3': 'Hong Kong',
               'Australia1': 'Australia',
               'Bolivia (Plurinational State of)': 'Bolivia',
               'China2': 'China',
               'China, Macao Special Administrative Region4': 'Macao',
               'Denmark5': 'Denmark',
               'Falkland Islands (Malvinas)': 'Falkland Islands',
               'France6': 'France',
               'Greenland7': 'Greenland',
               'Indonesia8': 'Indonesia',
               'Iran (Islamic Republic of)': 'Iran',
               'Italy9': 'Italy',
               'Japan10': 'Japan',
               'Kuwait11': 'Kuwait',
               'Micronesia (Federated States of)': 'Micronesia',
               'Netherlands12': 'Netherlands',
               'Portugal13': 'Portugal',
               'Saudi Arabia14': 'Saudi Arabia',
               'Serbia15': 'Serbia',
               'Sint Maarten (Dutch part)': 'Sint Maarten',
               'Spain16': 'Spain',
               'Switzerland17': 'Switzerland',
               'Ukraine18': 'Ukraine',
               'Venezuela (Bolivarian Republic of)': 'Venezuela'},
                inplace=True)

# load GDP data from WHO and clean it up
GDP = pd.read_csv('world_bank.csv', index_col=0, skiprows=3)
GDP.index.name = 'Country'
GDP.rename({'Korea, Rep.': 'South Korea',
            'Iran, Islamic Rep.': 'Iran',
            'Hong Kong SAR, China': 'Hong Kong'},
             inplace=True)

# Load scimagojr data file
ScimEn = pd.read_excel('scimagojr-3.xlsx', index_col=0)
ScimEn['Rank'] = ScimEn.index
ScimEn = ScimEn.set_index('Country')


# join the data together
GDP_subset = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

merged_df = energy.merge(GDP[GDP_subset], how='inner', left_index=True, right_index=True).merge(
    ScimEn[ScimEn['Rank'] <= 15], how='inner', left_index=True, right_index=True)

merged_df = merged_df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document',
                       'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
                       '2009', '2010', '2011', '2012', '2013', '2014', '2015']]


def answer_two():
    '''How many entries did you lose when you merged the data frames together? (before you reduced the sample
    further to 15)'''
    total_records = len(energy) + len(GDP) + len(ScimEn)
    surviving_records = len(energy.merge(GDP, how='inner', left_index=True, right_index=True).merge(
        ScimEn, how='inner', left_index=True, right_index=True))
    return total_records - surviving_records


def answer_three():
    '''What is the avarage GDP over the last 10 years for each country in the top 15 countries?'''
    GDP_subset = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    merged_df['avgGDP'] = merged_df[GDP_subset].mean(axis=1, skipna=True)
    return merged_df['avgGDP'].sort_values(ascending=False)


def answer_four():
    '''By how much did the GDP change over the 10 years span for the country with 6th largest avg GDP?'''
    sixth_gdp = answer_three().index[5]
    return merged_df.loc[sixth_gdp]['2015'] - merged_df.loc[sixth_gdp]['2006']


def answer_five():
    '''What is the mean Energy Supply per Capita?'''
    return merged_df['Energy Supply per Capita'].mean(axis=0)


def answer_six():
    '''What country has the maximum % Renewable and what is the percentage?'''
    pass






print(answer_five())








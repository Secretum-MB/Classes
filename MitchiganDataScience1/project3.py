#!/usr/bin/env python3

"""
Created on Sat Sep 16 17:27:48 2017

"""

import numpy as np
import pandas as pd


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    '''return dataframe of university towns'''
    lst_of_states = []
    for key, value in states.items():
        lst_of_states.append(value)

    state_towns = []
    with open('university_towns.txt','r') as file:
        for line in file:
            clean = line.replace('[','(').split('(')[0].strip()
            if clean in lst_of_states:
                state = clean
            else:
                town = clean
                state_towns.append([state, town])

    return pd.DataFrame(state_towns, columns=['State','RegionName'])


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', header=None, skiprows=8, index_col=4)
    df.drop([0,1,2,3,5,7], axis=1, inplace=True)
    df.index.name = 'Period'
    df.rename(columns={6:'GDP (billions)'}, inplace=True)

    narrow_df = df[df.index >= '2000q1']
    series = narrow_df['GDP (billions)']

    recessions = []
    for row in range(2, len(series)):
        if series[row] < series[row - 1] and series[row - 1] < series[row - 2]:
            recessions.append(series.index[row])

    return recessions[0]


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
        string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', header=None, skiprows=8, index_col=4)
    df.drop([0, 1, 2, 3, 5, 7], axis=1, inplace=True)
    df.index.name = 'Period'
    df.rename(columns={6: 'GDP (billions)'}, inplace=True)

    narrow_df = df[df.index >= '2000q1']
    series = narrow_df['GDP (billions)']

    recession = False
    for row in range(2, len(series)):
        if series[row] < series[row - 1] and series[row - 1] < series[row - 2]:
            recession = True
        if recession == True and series[row] > series[row - 1] and series[row - 1] > series[row - 2]:
            return series.index[row]


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''
    df = pd.read_excel('gdplev.xls', header=None, skiprows=8, index_col=4)
    df.drop([0, 1, 2, 3, 5, 7], axis=1, inplace=True)
    df.index.name = 'Period'
    df.rename(columns={6: 'GDP (billions)'}, inplace=True)

    narrow_df = df[df.index >= '2000q1']
    series = narrow_df['GDP (billions)']

    recession = False
    recession_bottom_gdp = None
    recession_bottom = None
    for row in range(2, len(series)):
        if series[row] < series[row - 1] and series[row - 1] < series[row - 2]:
            recession = True

        if recession == True:
            if recession_bottom_gdp == None or series[row] < recession_bottom_gdp:
                recession_bottom_gdp = series[row]
                recession_bottom = series.index[row]

        if recession == True and series[row] > series[row - 1] and series[row - 1] > series[row - 2]:
            recession = False

    return recession_bottom


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
       values in a dataframe. This dataframe should be a dataframe with
       columns for 2000q1 through 2016q3, and should have a multi-index
       in the shape of ["State","RegionName"].

       Note: Quarters are defined in the assignment description, they are
       not arbitrary three month periods.

       The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    pass






print(convert_housing_data_to_quarters())

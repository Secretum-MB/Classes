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
    outer_records = energy.merge(GDP, how='outer', left_index=True, right_index=True, indicator='firstM').merge(
        ScimEn, how='outer', left_index=True, right_index=True, indicator='secondM')

    new_df = outer_records[outer_records['firstM']!='both']
    newer_df = new_df[new_df['secondM']!='both']
    return len(newer_df)


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
    return (merged_df['% Renewable'].idxmax(), merged_df['% Renewable'].max())


def answer_seven():
    '''Create column that is ratio of Self-Citation to Total Citations.
    What is the maximum value for this new column, and what country has the 
    highest ratio?'''
    merged_df['Self-to-Total'] = merged_df['Self-citations'] / merged_df['Citations']
    return (merged_df['Self-to-Total'].idxmax(), merged_df['Self-to-Total'].max())


def answer_eight():
    '''Create a column that estimates the population using Energy Supply and
    Energy Supply per capita. What is the most populous country according to 
    this estimate?'''
    merged_df['PopEst'] = merged_df['Energy Supply'] / merged_df['Energy Supply per Capita']
    return merged_df['PopEst'].sort_values(axis=0, ascending=False).index[2]


def answer_nine():
    '''Create a column that estimates the number of citable documents per person.
    What is the correlation between the number of citable documents per capita
    and the energy supply per capita? Use the .corr() method, (Pearson's corr).'''
    merged_df['PopEst'] = merged_df['Energy Supply'] / merged_df['Energy Supply per Capita']
    merged_df['Citable docs per Capita'] = merged_df['Citable documents'] / merged_df['PopEst']
    return -(merged_df['Citable docs per Capita'].corr(merged_df['PopEst'], method='pearson'))


def answer_ten():
    '''Create a new column with a 1 if the country's % Renewable value is at or
    above the median for all contries in the top 15, and 0 if below median.'''
    median_renew = merged_df['% Renewable'].median()
    merged_df['HighRenew'] = np.where(merged_df['% Renewable'] >= median_renew, 1, 0)
    sort = merged_df[['Rank','HighRenew']].sort_values(by='Rank', ascending=False)
    return sort['HighRenew']


def answer_eleven():
    '''Use the following dictionary to group the Countries by Continent, then
    create a dataframe that displays the sample size (the number of countries
    in each continent bin), and the sum, mean, and std deviation for the 
    estimated population of each country.'''
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}
            
    merged_df['PopEst'] = merged_df['Energy Supply'] / merged_df['Energy Supply per Capita']
    merged_df['Country'] = merged_df.index
    merged_df['Continent'] = merged_df['Country'].map(ContinentDict)
    new_df = merged_df.set_index('Continent')
    new_df['Continent'] = new_df.index

    new_df['size'] = new_df['PopEst'].groupby(new_df['Continent']).transform('count')
    new_df['sum'] = new_df['PopEst'].groupby(new_df['Continent']).transform('sum')
    new_df['mean'] = new_df['PopEst'].groupby(new_df['Continent']).transform('mean')
    new_df['std'] = new_df['PopEst'].groupby(new_df['Continent']).transform('std')
 
    return new_df[['size','sum','mean','std']].drop_duplicates()
    

def answer_twelve():
    '''Cut % Renewable into 5 bins. Group top 15 by the Continent, as well as
    these new % Renewable bins. How many countries are in each of these groups?
    '''
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}

    merged_df['Country'] = merged_df.index
    merged_df['Continent'] = merged_df['Country'].map(ContinentDict)

    tags = ['Bottom 20%', 'Top 80%', 'Top 60%', 'Top 40%', 'Top 20%']
    merged_df['bins for Renewable'] = pd.cut(merged_df['% Renewable'], bins=5, labels=tags)

    pvtdf = pd.pivot_table(merged_df, index=['Continent','bins for Renewable'], 
                           values='Country', aggfunc='count')

    pvtdf.rename(columns={'Country':'# of Countries'}, inplace=True)
    pvtdf = pvtdf.dropna()
    
    return pvtdf.squeeze()


def answer_thirteen(): # incorrect - 8 differences
    '''Convert the population Estimate sereies to a string with thousands
    seperator (using commas). Do not round the results.'''
    merged_df['PopEst-pre'] = merged_df['Energy Supply'] / merged_df['Energy Supply per Capita']
    
    new_df = pd.DataFrame(merged_df['PopEst-pre'])
    new_df['formatted'] = new_df['PopEst-pre'].map('{:,.7f}'.format)
    new_df['PopEst'] = new_df[str('formatted')]

    return pd.Series(new_df['PopEst'])


# end

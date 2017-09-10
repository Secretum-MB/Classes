#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 19:42:33 2017

"""

import pandas as pd

# The below questions pertain to the Olympic results by country
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(')  # split the index by '('

# the [0] element is the country name (new index)
df.index = names_ids.str[0]

# the [1] element is the abbreviation or ID (take first 3 characters from that)
df['ID'] = names_ids.str[1].str[:3]

# removes totals row from bottom of data
df = df.drop('Totals')


def answer_zero():
    '''what is the first country in database'''
    return df.iloc[0]


def answer_one():
    '''which country has won the most gold medals in the summer games'''
    return df['Gold'].idxmax()


def answer_two():
    '''which country has the biggest difference between their summer and winter
    gold medal counts'''
    return (df['Gold'] - df['Gold.1']).idxmax()


def answer_three():
    '''Which country has the biggest difference between their summer gold
    medal counts and winter gold medal counts relative to their total gold
    medal count?'''
    temp = df.where((df['Gold'] >= 1) & (df['Gold.1'] >= 1))
    return ((temp['Gold'] - temp['Gold.1']) / temp['Gold.2']).idxmax()


def answer_four():
    '''Write a function that creates a Series called "Points" which is a
    weighted value where each gold medal (Gold.2) counts for 3 points, silver
    medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point.'''
    df['Points'] = (df['Gold.2'] * 3) + (df['Silver.2'] * 2) + df['Bronze.2']
    return pd.Series(df['Points'])


# The below questions pertain to the United States Census 2010-2015
census_df = pd.read_csv('UScensus.csv')

def answer_five():
    '''Which state has the most counties in it? (hint: consider the sumlevel
    key carefully! You'll need this for future questions too...)'''
    return census_df['STNAME'].where(census_df['SUMLEV']==50).value_counts().index[0]


def answer_six():
    '''Only looking at the three most populous counties for each state, what
    are the three most populous states (in order of highest population to
    lowest population)?'''
    a = census_df.where(census_df['SUMLEV'] == 50)
    b = a.groupby('STNAME')['CENSUS2010POP'].apply(lambda grp: grp.nlargest(3).sum())
    b = b.sort_values(ascending=False)
    c = list(b.index[:3])
    return c


def answer_seven():
    '''Which county has had the largest absolute change in population within
    the period 2010-2015?'''
    rmv_state = census_df.where(census_df['SUMLEV'] == 50)
    pops = rmv_state[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
                     'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']]
    top, bottom = pops.max(axis=1), pops.min(axis=1)
    rmv_state['Abs Change'] = (top - bottom)
    top_cty = rmv_state['Abs Change'].idxmax()
    return rmv_state.iloc[top_cty]['CTYNAME']


def answer_eight():
    '''Create a query that finds the counties that belong to regions 1 or 2,
    whose name starts with 'Washington', and whose POPESTIMATE2015 was greater
    than their POPESTIMATE 2014.'''
    rmv_state = census_df.where(census_df['SUMLEV'] == 50)
    qry = rmv_state.query("REGION < 3 & POPESTIMATE2015 > POPESTIMATE2014")
    qry = qry.where(qry['CTYNAME'].str.startswith('Washington'))
    qry.dropna(inplace=True)
    return qry[['STNAME', 'CTYNAME']]

# end

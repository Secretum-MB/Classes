"""
Created on Sat Sep 16 17:27:48 2017

"""

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


def get_list_of_university_towns():
    '''return dataframe of university towns'''
    lst_of_states = []
    for key, value in states.items():
        lst_of_states.append(value)

    state_towns = []
    states_seen = []
    with open('university_towns.txt', 'r') as file:
        for line in file:
            clean = line.replace('[', '(').split('(')[0].strip()
            if clean in lst_of_states and clean not in states_seen:
                state = clean
                states_seen.append(state)
            else:
                town = clean
                state_towns.append([state, town])

    return pd.DataFrame(state_towns, columns=['State', 'RegionName'])


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
            recessions.append(series.index[row - 1])

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
    """Converts the housing data to quarters and returns it as mean
       values in a dataframe. This dataframe should be a dataframe with
       columns for 2000q1 through 2016q3, and should have a multi-index
       in the shape of ["State","RegionName"].

       Note: Quarters are defined in the assignment description, they are
       not arbitrary three month periods.

       The resulting dataframe should have 67 columns, and 10,730 rows.
    """
    df = pd.read_csv('City_Zhvi_AllHomes.csv', index_col=['SizeRank'])
    df['State'] = df['State'].map(states)
    df.set_index(['State', 'RegionName'], inplace=True)

    for column in df.columns.get_values():
        if column[-2:] == '03':
            year = column[:4]
            df[year + 'q1'] = (df[year + '-01'] + df[year + '-02'] + df[year + '-03']).div(3)

        if column[-2:] == '06':
            year = column[:4]
            df[year + 'q2'] = (df[year + '-04'] + df[year + '-05'] + df[year + '-06']).div(3)

        if column[-2:] == '09':
            year = column[:4]
            df[year + 'q3'] = (df[year + '-07'] + df[year + '-08'] + df[year + '-09']).div(3)

        if column[-2:] == '12':
            year = column[:4]
            df[year + 'q4'] = (df[year + '-10'] + df[year + '-11'] + df[year + '-12']).div(3)

    df['2016q3'] = (df['2016-07'] + df['2016-08']).div(2)

    df = df.loc[:, '2000q1':'2016q3']
    return df


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices between
    the recession start and the recession bottom. Then runs a ttest comparing the
    university town values to the non-university towns values, return whether the
    alternative hypothesis (that the two groups are the same) is true or not as well
    as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at the p<0.01 (we refect the null hypotheis), or different=False if otherwise
    (we cannot reject the null hypothesis). The variable p should be equal to the exact
    p value returned from the scipy.stats.ttest_ind().  The value for better should be
    either "university town" or "non-university town" depending on which has the lower
    mean price ratio (which is equivelant to a reduced market loss).'''

    # the lower the ratio the less you have lost. values less than 1 indicates gain.
    # price ratio = quarter_before_recession / recession_bottom
    df = convert_housing_data_to_quarters()
    df['PriceRatio'] = df[get_recession_start()] / df[get_recession_bottom()]
    df.reset_index('RegionName', inplace=True)

    university_towns = list(get_list_of_university_towns()['RegionName'])

    df['UniversityTown'] = np.where(df['RegionName'].isin(university_towns), 'YES', 'NO')

    df_uni = df[df['UniversityTown']=='YES']
    df_non_uni = df[df['UniversityTown']=='NO']

    t_test = ttest_ind(df_uni['PriceRatio'], df_non_uni['PriceRatio'], nan_policy='omit')

    if t_test[0] < 0:   better = 'university town'
    else:   better = 'non-university town'

    if t_test[1] < 0.01:    different = True
    else:   different = False

    return (different, t_test[1], better)


# end

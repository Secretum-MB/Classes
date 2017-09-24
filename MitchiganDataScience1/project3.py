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


    return university_towns



print(run_ttest())

['Auburn', 'Florence', 'Jacksonville', 'Livingston', 'Montevallo', 'Troy', 'Tuscaloosa', 'Tuskegee', 'Fairbanks', 'Flagstaff', 'Tempe', 'Tucson', 'Arkadelphia', 'Conway', 'Fayetteville', 'Jonesboro', 'Magnolia', 'Monticello', 'Russellville', 'Searcy', 'Angwin', 'Arcata', 'Berkeley', 'Chico', 'Claremont', 'Cotati', 'Davis', 'Irvine', 'Isla Vista', 'University Park, Los Angeles', 'Merced', 'Orange', 'Palo Alto', 'Pomona', 'Redlands', 'Riverside', 'Sacramento', 'University District, San Bernardino', 'San Diego', 'San Luis Obispo', 'Santa Barbara', 'Santa Cruz', 'Turlock', 'Westwood, Los Angeles', 'Whittier', 'Alamosa', 'Boulder', 'Durango', 'Fort Collins', 'Golden', 'Grand Junction', 'Greeley', 'Gunnison', 'Pueblo, Colorado', 'Fairfield', 'Middletown', 'New Britain', 'New Haven', 'New London', 'Storrs', 'Willimantic', 'Dover', 'Newark', 'Ave Maria', 'Boca Raton', 'Coral Gables', 'DeLand', 'Estero', 'Gainesville', 'Orlando', 'Sarasota', 'St. Augustine', 'St. Leo', 'Tallahassee', 'Tampa', 'Albany', 'Athens', 'Atlanta', 'Carrollton', 'Demorest', 'Fort Valley', 'Kennesaw', 'Milledgeville', 'Mount Vernon', 'Oxford', 'Rome', 'Savannah', 'Statesboro', 'Valdosta', 'Waleska', 'Young Harris', 'Manoa', 'Moscow', 'Pocatello', 'Rexburg', 'Carbondale', 'Champaignâ€“Urbana', 'Charleston', 'DeKalb', 'Edwardsville', 'Evanston', 'Lebanon', 'Macomb', 'Normal', 'Peoria', 'Bloomington', 'Crawfordsville', 'Greencastle', 'Hanover', 'Marion', 'Muncie', 'Oakland City', 'Richmond', 'South Bend', 'Terre Haute', 'Upland', 'Valparaiso', 'West Lafayette', 'Ames', 'Cedar Falls', 'Cedar Rapids, Iowa', 'Decorah', 'Fayette', 'Grinnell', 'Iowa City', 'Lamoni', 'Mount Vernon,', 'Orange City', 'Sioux Center', 'Storm Lake', 'Waverly', 'Baldwin City', 'Emporia', 'Hays', 'Lawrence', 'Manhattan', 'Pittsburg', 'Bowling Green', 'Columbia', 'Georgetown', 'Highland Heights', 'Lexington', 'Louisville', 'Morehead', 'Murray', 'Richmond', 'Williamsburg', 'Wilmore', 'Baton Rouge', 'Grambling', 'Hammond', 'Lafayette', 'Monroe', 'Natchitoches', 'Ruston', 'Thibodaux', 'Augusta', 'Bar Harbor', 'Brunswick', 'Farmington', 'Fort Kent', 'Gorham', 'Lewiston, Maine', 'Orono', 'Waterville', 'Annapolis', 'Chestertown', 'College Park', 'Cumberland', 'Emmitsburg', 'Frostburg', 'Princess Anne', 'Towson', 'Salisbury', 'Westminster', 'Boston', 'Bridgewater', 'Cambridge', 'Chestnut Hill', 'The Colleges of Worcester Consortium:', 'Dudley', 'North Grafton', 'Paxton', 'Worcester', 'The Five College Region of Western Massachusetts:', 'Amherst', 'Northampton', 'South Hadley', 'Fitchburg', 'North Adams', 'Springfield', 'Waltham', 'Williamstown', 'Framingham', 'Adrian', 'Albion', 'Allendale', 'Alma', 'Ann Arbor', 'Berrien Springs', 'Big Rapids', 'East Lansing', 'Flint', 'Hillsdale', 'Houghton', 'Kalamazoo', 'Marquette', 'Midland', 'Mount Pleasant', 'Olivet', 'Saginaw', 'Sault Ste. Marie', 'Spring Arbor', 'Ypsilanti', 'Bemidji', 'Crookston', 'Duluth', 'Faribault, South Central College', 'Mankato', 'Marshall', 'Moorhead', 'Morris', 'Northfield', 'North Mankato, South Central College', 'St. Cloud', 'St. Joseph', 'St. Peter', 'Winona', 'Cleveland', 'Hattiesburg', 'Itta Bena', 'Oxford', 'Starkville', 'Bolivar', 'Cape Girardeau', 'Columbia', 'Fayette', 'Fulton', 'Kirksville', 'Maryville', 'Rolla', 'Warrensburg', 'Bozeman', 'Dillon', 'Missoula', 'Chadron', 'Crete', 'Kearney', 'Lincoln', 'Peru', 'Seward', 'Wayne', 'Las Vegas', 'Reno', 'New London, New Hampshire', 'Durham', 'Hanover', 'Henniker', 'Keene', 'Plymouth', 'Rindge', 'Ewing', 'Jersey City', 'Glassboro', 'Hoboken', 'Madison', 'Newark', 'New Brunswick', 'Princeton', 'Union', 'West Long Branch', 'Hobbs', 'Las Cruces', 'Las Vegas', 'Portales', 'Silver City', 'Alfred', 'Albany', 'Aurora', 'Binghamton', 'Brockport', 'Buffalo', 'Canton', 'Clinton', 'Cobleskill', 'Delhi', 'Fredonia', 'Geneseo', 'Geneva', 'Hamilton', 'Ithaca', 'Morningside Heights, Manhattan', 'New Paltz', 'Oneonta', 'Oswego', 'Plattsburgh', 'Potsdam', 'Poughkeepsie', 'Purchase', 'Rochester', 'Saratoga Springs', 'Seneca Falls', 'Stony Brook', 'Syracuse', 'Tivoli', 'Troy', 'West Point', 'Banner Elk', 'Boiling Springs', 'Boone', 'Buies Creek', 'Chapel Hill', 'Cullowhee', 'Davidson', 'Durham', 'Elon', 'Greensboro', 'Greenville', 'Hickory', 'Mars Hill', 'Mount Olive', 'Pembroke', 'Wilmington, North Carolina', 'Wingate', 'Winston-Salem', 'Fargo', 'Grand Forks', 'Ada', 'Alliance', 'Ashland', 'Athens', 'Berea', 'Bluffton', 'Bowling Green', 'Cedarville', 'Columbus', 'Delaware', 'Fairborn', 'Findlay', 'Gambier', 'Granville', 'Hiram', 'Kent', 'Nelsonville', 'New Concord', 'Oberlin', 'Oxford', 'Rio Grande', 'Wilberforce', 'Ada', 'Alva', 'Durant', 'Edmond', 'Goodwell', 'Langston', 'Norman', 'Stillwater', 'Tahlequah', 'Tulsa', 'Weatherford', 'Ashland', 'Corvallis', 'Eugene', 'Forest Grove', 'Klamath Falls', 'La Grande', 'Marylhurst', 'McMinnville', 'Monmouth', 'Newberg', 'Altoona', 'Annville', 'Bethlehem', 'Bloomsburg', 'Bradford', 'California', 'Carlisle', 'Cecil B. Moore, Philadelphia, also known as "Templetown"', 'Clarion', 'Collegeville', 'Cresson', 'East Stroudsburg', 'Edinboro', 'Erie', 'Gettysburg', 'Greensburg', 'Grove City', 'Huntingdon', 'Indiana', 'Johnstown', 'Kutztown', 'Lancaster', 'Lewisburg', 'Lock Haven', 'Loretto', 'Mansfield', 'Meadville', 'Mont Alto', 'Millersville', 'New Wilmington', 'North East', 'University City, Philadelphia', 'Oakland, Pittsburgh', 'Reading', 'Selinsgrove', 'Shippensburg', 'Slippery Rock', 'State College', 'Villanova', 'Waynesburg', 'West Chester', 'Wilkes-Barre', 'Williamsport', 'Kingston', 'Providence', 'Central', 'Charleston', 'Clemson', 'Clinton', 'Columbia', 'Due West', 'Florence', 'Greenwood', 'Orangeburg', 'Rock Hill', 'Spartanburg', 'Brookings', 'Madison', 'Spearfish', 'Vermillion', 'Chattanooga', 'Collegedale', 'Cookeville', 'Harrogate', 'Henderson', 'Johnson City', 'Knoxville', 'Martin', 'McKenzie', 'Memphis', 'Murfreesboro', 'Nashville', 'Sewanee', 'Abilene', 'Alpine', 'Austin', 'Beaumont', 'Canyon', 'College Station', 'Commerce', 'Dallas', 'Denton', 'Fort Worth', 'Georgetown', 'Huntsville', 'Houston', 'Keene', 'Kingsville', 'Lubbock', 'Nacogdoches', 'Plainview', 'Prairie View', 'San Marcos', 'Stephenville', 'Waco', 'Cedar City', 'Logan', 'Provo', 'Orem', 'Salt Lake City', 'Ephraim', 'Burlington', 'Castleton', 'Johnson', 'Lyndonville', 'Middlebury', 'Northfield', 'Blacksburg', 'Bridgewater', 'Charlottesville', 'Farmville', 'Fredericksburg', 'Harrisonburg', 'Lexington', 'Lynchburg', 'Radford', 'Williamsburg', 'Wise', 'Chesapeake', 'Bellingham', 'Cheney', 'Ellensburg', 'Pullman', 'University District, Seattle', 'Athens', 'Buckhannon', 'Fairmont', 'Glenville', 'Huntington', 'Montgomery', 'Morgantown', 'Shepherdstown', 'West Liberty', 'Appleton', 'Eau Claire', 'Green Bay', 'La Crosse', 'Madison', 'Menomonie', 'Milwaukee', 'Oshkosh', 'Platteville', 'River Falls', 'Stevens Point', 'Waukesha', 'Whitewater', 'Laramie']




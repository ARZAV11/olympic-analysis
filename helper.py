import numpy as np


# we are filtering dataframes on the basis of given conditions

def fetch_medal_tally(df,year, region):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and region == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and region != 'Overall':  # groupby on the basis of years
        flag = 1
        temp_df = medal_df[medal_df['region'] == region]
    if year != 'Overall' and region == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and region != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == region)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def region_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    region = np.unique(df['region'].dropna().values).tolist()
    region.sort()
    region.insert(0,'Overall')

    return year,region

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])\
    ['Year'].value_counts().reset_index().sort_values('Year')
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # rename columns clearly

    return x.head(15).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

def country_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df['Year'].value_counts().reset_index().sort_values('Year')
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_athlete(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medals']  # rename columns clearly

    return x.head(10).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

def height_weight(df,sport):
    name_df = df.drop_duplicates(subset=['Name', 'region'])
    name_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        sport_df = name_df[name_df['Sport'] == sport]
        return sport_df
    else:
        return name_df
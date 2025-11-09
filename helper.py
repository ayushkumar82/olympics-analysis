import numpy as np
from fontTools.subset import subset
import plotly.express as px


def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    flag=0

    if year=='overall'and country=='overall':
        temp_df=medal_df
    if year=='overall' and country!='overall':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if year!='overall' and country=='overall':
         temp_df=medal_df[medal_df['Year']==year]
    if year!='overall' and country!='overall':
         temp_df=medal_df[(medal_df['region']==country) & (medal_df['Year']==year)]

    if(flag==1):
          x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(by='Year').reset_index()
    else:
          x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold', ascending=False).reset_index()
    x['total']=x['Gold']+x['Silver']+x['Bronze']
    return x


def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years, country

# def participating_nations_over_time(df):
#     nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
#
#     nations_over_time.rename(columns={'Year': 'Edition', 'count': "No Of Countries"}, inplace=True)
#     return nations_over_time
#
# def total_events_over_time(df):
#     events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
#
#     events_over_time.rename(columns={'Year': 'Edition', 'count': "events"}, inplace=True)
#     return events_over_time

def data_over_time(df,col):
    data_over_time = df.drop_duplicates(['Year', col]).groupby('Year')[col].count().reset_index()
    data_over_time.rename(columns={'Year':'edition'}, inplace=True)
    return data_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medal_count'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_athlete_in_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    return x

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def participation_of_men_v_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year',how='left')

    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final



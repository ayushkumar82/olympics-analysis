import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

import numpy as np
from helper import medal_tally

df = pd.read_csv("datas/athlete_events.csv")
region_df = pd.read_csv("datas/noc_regions.csv")


df=preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('https://static.vecteezy.com/system/resources/thumbnails/046/818/230/small/olympic-logo-statue-background-sunset-sunrise-sky-beautiful-hills-silhouette-sports-fans-country-competition-free-vector.jpg')
user_menu=st.sidebar.radio(
    'select an option',
    ('medal tally','Overall Analysis','country wise analysis','athlete wise analysis')
)


if user_menu=='medal tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox('select year',years)
    selected_country=st.sidebar.selectbox('select country',country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('overall analysis')
    elif selected_year == 'overall' and selected_country != 'overall':
       st.title('overall performance of '+selected_country)
    elif selected_year != 'overall' and selected_country == 'overall':
        st.title('performance of countries in '+str(selected_year))
    else:
        # selected_year != 'overall' and selected_country != 'overall':
        st.title('performance of '+selected_country+'in '+str(selected_year))
    st.table(medal_tally)

if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title('Top Stats')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sport')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Event')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    #
    # nations_over_time=helper.participating_nations_over_time(df)
    # fig = px.line(nations_over_time, x='Edition', y='No Of Countries')
    # st.title('participating Nations Over Time')
    # st.plotly_chart(fig)
    #
    # events_over_time=helper.total_events_over_time(df)
    # fig = px.line(events_over_time, x='Edition', y='events')
    # st.title('Total Events Over Time')
    # st.plotly_chart(fig)


    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='edition', y='region')
    st.title('participating Nations Over Time')
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='edition', y='Event')
    st.title('events over time')
    st.plotly_chart(fig)

    athletes_over_time=helper.data_over_time(df,'Name')
    fig=px.line(athletes_over_time,x='edition',y='Name')
    st.title('athletes over time')
    st.plotly_chart(fig)

    st.title('No of Events Over Time(Every Time)')
    fig,ax=plt.subplots(figsize=(25,25))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)


    st.title('Most successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport=st.selectbox('select a sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='country wise analysis':

    st.sidebar.title('country wise analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('select a country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig=px.line(country_df,x='Year',y="Medal")
    st.title(selected_country+' Medal tally over the years')
    st.plotly_chart(fig)


    st.title(selected_country+' excels in following sport')
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(25,25))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    # country_list = np.unique(df['region'].dropna().values).tolist()
    # country_list.sort()
    # selected_country = st.selectbox('select a country', country_list)
    st.title('top 10 athletes of'+ selected_country)
    x = helper.most_successful_athlete_in_country(df, selected_country)
    st.table(x)


if user_menu=='athlete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['overall', 'gold medalist', 'silver medalist', 'bronze medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('distribution of age')
    st.plotly_chart(fig)

    st.title('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport=st.selectbox('select a sport',sport_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=100)
    st.pyplot(fig)

    st.title('Men vs Women participation over the years')
    final=helper.participation_of_men_v_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
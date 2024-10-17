import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympic Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')


    years,country = helper.contry_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country', country)


    if selected_year == 'overall' and selected_country == 'overall':
        st.title('Overall Tally')
    if selected_year != 'overall' and selected_country == 'overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(str(selected_country) + ' Overall Performance')
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(str(selected_country) + ' Performance in ' + str(selected_year))


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    region = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.title('Editions')
        st.header(editions)
    with col2:
        st.title('Hosts')
        st.header(cities)
    with col3:
        st.title('Sports')
        st.header(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title('Events')
        st.header(event)
    with col2:
        st.title('Athletes')
        st.header(athletes)
    with col3:
        st.title('Nations')
        st.header(region)
    # For Participating nations over the years graph
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition',y='region')
    st.title('Participating nations over the years')
    st.plotly_chart(fig)
    # for participating Events over the years graph
    events_over_time = helper.data_over_time(df,'Event')
    fig1 = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the years')
    st.plotly_chart(fig1)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig2 = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig2)

    st.title('No. of Events over time(Every Sport)')
    fig,ax = plt.subplots(figsize = (28,28))
    x = df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True,
        ax=ax
    )
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport',sports_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y='Medal')
    st.title(selected_country + "Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + ' Excels in the following sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize = (20,20))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of '+ selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x =[]
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis',  'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach Volleyball', 'Triathlon', 'Rugby',  'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x,name,show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age wrt Sports(Gold Medalist)')
    st.plotly_chart(fig)

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    st.title('Height vs Weight')
    selected_sport = st.selectbox('Select a Sport',sports_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

from helper import fetch_medal_tally

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://media.gettyimages.com/id/904469658/photo/pyeongchang-gun-south-korea-the-olympic-rings-on-the-beach-at-gangneung-ahead-of-the.jpg?s=612x612&w=0&k=20&c=MGMbscYljvjGmlsQ9qLes4Y77x4wGSH5r_UOqOvjjAI=")
user_menu = st.sidebar.radio(
     'Select an Option',
     ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)




# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,region = helper.region_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_region = st.sidebar.selectbox("Select Region",region)

    if selected_year == 'Overall' and selected_region == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_region == 'Overall':
        st.title("Medal Tally In " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_region != 'Overall':
        st.title("Medal Tally Of " + selected_region)
    if selected_year != 'Overall' and selected_region != 'Overall':
        st.title("Medal Tally Of " + selected_region + " In " + str(selected_year))

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_region)
    st.table(medal_tally)     # for display to the dashboard

# ---------------------------------------------------------------------------------------------------------------

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    st.title("Top Statistic")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nation)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="count")
    st.title("Participating Nations Over Years")
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(event_over_time, x="Year", y="count")
    st.title("Events Over Years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Year", y="count")
    st.title("Athletes Over Years")
    st.plotly_chart(fig)

    st.title("Number Of Events With Years (Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)

    x = helper.most_successful(df,selected_sport)
    st.table(x)

# -------------------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country = st.sidebar.selectbox("Select Country", country_list)

    country_df = helper.country_wise_medal_tally(df,country)
    fig = px.line(country_df, x='Year', y='count')
    st.title(f'Medal Tally Of {country} Over Years')
    st.plotly_chart(fig)

    st.title(f"{country} Excels In The Following Sports")
    pt = helper.country_event_heatmap(df,country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(f"Most Successful Athletes Of {country}")
    athlete_df = helper.most_successful_athlete(df,country)
    st.table(athlete_df)


# -------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Athlete wise Analysis':
    name_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = name_df['Age'].dropna()
    x2 = name_df[name_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = name_df[name_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = name_df[name_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff. create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                       show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution Of Age With Medals")
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    name_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    for sport in famous_sports:
        temp_df = name_df[name_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, famous_sports, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution Of Age Wrt Sports")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    st.title("Height Vs Weight In")
    sport = st.selectbox('Select Sport',sport_list)
    sport_df = helper.height_weight(df,sport)
    fig,ax = plt.subplots(figsize=(10, 10))
    ax = sns.scatterplot(data=sport_df,x='Weight',y='Height',hue='Medal',style='Sex',s=80)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over Years")
    athlete_df = df.drop_duplicates(subset=['Name'])
    men = athlete_df[athlete_df['Sex'] == 'M'].value_counts('Year').reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].value_counts('Year').reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'count_x': 'Men', 'count_y': 'Women'}, inplace=True)
    final_df = final.sort_values('Year')
    final_df.fillna(0, inplace=True)

    fig = px.line(final_df, x='Year', y=['Men', 'Women'])
    st.plotly_chart(fig)
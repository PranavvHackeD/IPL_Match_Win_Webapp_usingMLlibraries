# Using Streamlit we are able to local host to host the webiste locally on server...

import streamlit as st
import pickle
import pandas as pd

#list of teams
teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

# list of  cities 
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

# open in readbinary mode
pipe = pickle.load(open('pipe.pkl','rb'))


# Set page config
st.set_page_config(
    page_title="IPL Match Win Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add CSS styling
st.markdown(
    """
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.3;
            
        }
        .stApp {
            max-width: 1000px;
            margin: 0 auto;
            background-color:white-smoke;
           
        }
        .stTitle {
            font-size: 70px;
            font-weight: bold;
            color: #1E90FF;
            margin-top: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stHeader {
            font-size: 44px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: transparent;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .stPrediction {
            font-size: 40px;
            font-weight: bold;
            color: #FF4500;
            background-color:transparent;
            text-align: center;
        }
        .stFooter {
            font-size: 22px;
            color: black;
            text-align: center;
            margin-top: 35px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


#st.title('IPL Win Predictor')
st.markdown("<div class='stTitle'>IPL Match Win Predictor</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs

    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city], 'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets], 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.markdown("<div class='stPrediction'>{}</div>".format(batting_team + " - " + str(round(win * 100)) + "%"), unsafe_allow_html=True)
    st.markdown("<div class='stPrediction'>{}</div>".format(bowling_team + " - " + str(round(loss * 100)) + "%"), unsafe_allow_html=True)

# Add a footer
st.markdown("<div class='stFooter'>Developed by Pranav Lokhande</div>", unsafe_allow_html=True)

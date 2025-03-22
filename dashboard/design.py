import streamlit as st

def design():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

        body, .stApp {
            background-color: #f0f0f0 !important; /* Light grey background */
            color: #000000; /* Black Text */
            font-family: 'Montserrat', sans-serif; 
        }

        .stSidebar {
            background-color: #F8F8F8; /* Very Light Gray */
            color: #000000; /* Black Text */
            font-family: 'Montserrat', sans-serif;
        }

        section[data-testid="stSidebar"] {
            width: 300px !important;
        }

        .stSelectbox, .stDateInput, .stMetric, .stPlotlyChart {
            background-color: transparent;
            color: #000000; 
            border-radius: none;
            box-shadow: none;
            padding: 8px;
            font-family: 'Montserrat', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700; /* Bold Headers */
        }

        /* Add white background to columns' containers */
        div[data-testid="stHorizontalBlock"] > div {
            background-color: white !important; /* White interior */
            padding: 8px !important; /* Add some padding inside the container */
            border-radius: 4px; /* Optional: rounded corners */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Optional: add light shadow */
        }

        /* Change tab text color */
        div[data-baseweb="tab"] {
            color: black !important;
            font-weight: bold !important;
        }
        
        /* Change selected tab text and underline color */
        div[data-baseweb="tab-list"] div[aria-selected="true"] {
            color: #007BFF !important;
            border-bottom: 3px solid #007BFF !important;
        }
        /* Ensures hover effect stays correct */
        div[data-baseweb="tab-list"] div:hover {
            color: #007BFF !important;
        }


        </style>
        """,
        unsafe_allow_html=True
    )

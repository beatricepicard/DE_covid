import streamlit as st

def design_global():
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
            border-radius: 0px;
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
            box-shadow: none; /* Optional: add light shadow */
        }

        /* Remove margin and padding from individual components too */
        .stPlotlyChart, .stMetric, .stDataFrame, .stSlider, .stSelectbox, .stNumberInput {
            margin: 0px !important;
            padding: 4px !important;  /* You can even lower this to 2px or 0px if needed */
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

def design_continent():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

        body, .stApp {
            background-color: #f0f0f0 !important;
            color: #000000;
            font-family: 'Montserrat', sans-serif; 
        }

        .stSidebar {
            background-color: #F8F8F8;
            color: #000000;
            font-family: 'Montserrat', sans-serif;
        }

        section[data-testid="stSidebar"] {
            width: 300px !important;
        }

        /* Keep white background for plotly charts */
        .stPlotlyChart {
            background-color: white !important;
            padding: 8px;
            border-radius: 6px;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05);
        }

        /* Keep white background for metrics */
        .stMetric {
            background-color: white !important;
            color: #000000;
            padding: 10px;
            border-radius: 6px;
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05);
            font-family: 'Montserrat', sans-serif;
        }

        /* Optional: date input and select boxes keep white */
        .stSelectbox, .stDateInput {
            background-color: white !important;
            padding: 8px;
            border-radius: 6px;
            font-family: 'Montserrat', sans-serif;
        }


        /* HEADINGS */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
        }

        div {
            background-color: transparent !important;
        }

        /* Add white background ONLY to inner content (components) */
        .stPlotlyChart, .stMetric, .stDataFrame, .stSlider, .stSelectbox, .stNumberInput {
            background-color: white !important;
            padding: 10px;
            border-radius: 6px;
            margin: 6px 0px;
            box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 3px;
        }

        /* Constrain charts */
        .stPlotlyChart, .stAltairChart, .stEchartsChart {
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }

        /* Reduce vertical spacing between Streamlit containers */
        div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0px !important;  /* You can adjust 4px to 2px or 0px if needed */
        }

        /* Remove margin and padding from individual components too */
        .stPlotlyChart, .stMetric, .stDataFrame, .stSlider, .stSelectbox, .stNumberInput {
            margin: 0px !important;
            padding: 4px !important;  /* You can even lower this to 2px or 0px if needed */
        }

        .stContainer {
            padding: 0px !important;
            margin: 0px !important;
            background-color: white !important;
            border-radius: 6px;
            box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.05);
        }

        /* TABS */
        div[data-baseweb="tab"] {
            color: black !important;
            font-weight: bold !important;
        }

        div[data-baseweb="tab-list"] div[aria-selected="true"] {
            color: #007BFF !important;
            border-bottom: 3px solid #007BFF !important;
        }

        div[data-baseweb="tab-list"] div:hover {
            color: #007BFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

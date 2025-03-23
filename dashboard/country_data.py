import streamlit as st
import pandas as pd
import plotly.express as px

from line_chart import line_chart
from cases_rates import get_cases_rates


def country_data(data, connection, start_date_str, end_date_str, continent, country):
    col6 = st.columns(1)[0] 
    with col6:
        #line charts for country
        st.header(f"COVID-19 Data for {country}")
        country_data = data[data["Country"] == country].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
        line_chart(country_data, country)

    #COUNTRY COMPARISON (CASES PER 1 MILLION PEOPLE) FOR CHOSEN CONTINENT
    col7 = st.columns(1)[0] 
    with col7: 
        st.markdown(f"### Top Affected Countries of {continent} and {country} for selected period")
        col1, col2, col3 = st.columns(3)
        df_rates = get_cases_rates(connection, start_date_str, end_date_str, continent)
        num_countries = len(df_rates)
        if num_countries <= 15:
            op_n = num_countries
        else: 
            top_n = 15
                
        df_rates = df_rates.head(top_n)

        confirmed_color = ["#D9F0A3" if c == country else "#41B6C4" for c in df_rates["Country"]]
        deaths_color = ["#D9F0A3" if c == country else "#78C679" for c in df_rates["Country"]]
        recovered_color = ["#D9F0A3" if c == country else "#ADDD8E" for c in df_rates["Country"]]

        if country not in df_rates["Country"].values:
            country_data = get_cases_rates(connection, start_date_str, end_date_str, continent).query(f"Country == '{country}'")
            df_rates = pd.concat([df_rates, country_data])
            df_rates = df_rates.sort_values(by="ConfirmedPerPop_diff", ascending=False)

    with col1:
        fig1 = px.bar(df_rates, y="Country", x="ConfirmedPerPop_diff", orientation="h", title="Confirmed per 1 million people", color=df_rates["Country"], color_discrete_sequence=confirmed_color)
        fig1.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
        fig1.update_xaxes(dict(range=[0, df_rates["ConfirmedPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
        fig1.update_yaxes(title="", categoryorder="array", tickfont=dict(size=12), tickangle=0, tickmode='linear')
        fig1.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False) 
        st.plotly_chart(fig1, use_container_width=True)
                    
    with col2:
        fig2 = px.bar(df_rates, y="Country", x="DeathsPerPop_diff", orientation="h", title="Deaths per 1 million people", color=df_rates["Country"], color_discrete_sequence= deaths_color)
        fig2.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
        fig2.update_xaxes(dict(range=[0, df_rates["DeathsPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
        fig2.update_yaxes(title="", categoryorder="array", tickfont=dict(size=12), tickangle=0, tickmode='linear')
        fig2.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        fig3 = px.bar(df_rates, y="Country", x="RecoveredPerPop_diff", orientation="h", title="Recoveries per 1 million people", color=df_rates["Country"], color_discrete_sequence= recovered_color)
        fig3.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
        fig3.update_xaxes(dict(range=[0, df_rates["RecoveredPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
        fig3.update_yaxes(title="", categoryorder="array", tickfont=dict(size=12), tickangle=0, tickmode='linear')
        fig3.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False)
        st.plotly_chart(fig3, use_container_width=True)
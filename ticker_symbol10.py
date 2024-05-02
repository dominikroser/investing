import yfinance as yf
from datetime import date, timedelta
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX', 'CASHX']

def calculate_percentage_change(ticker_symbol1, ticker_symbol2, use_smoothed):
    df1 = yf.download(ticker_symbol1, start="2020-01-01", end=date.today())
    df1['Dates'] = pd.to_datetime(df1.index)  # Convert the index to datetime format
    
    df2 = yf.download(ticker_symbol2, start="2020-01-01", end=date.today())
    df2['Dates'] = pd.to_datetime(df2.index)  # Convert the index to datetime format
    
    eight_months_ago_months_ago = date.today() - timedelta(days=8*30)  # Approximating 30 days per month
    last_day_8_months_ago = eight_months_ago_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
    specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
    closing_today = df1['Close'].iloc[-1]
    
      
    df1['Percentage Change'] = (df1['Close'] - df1['Close'].shift(8*21)) / df1['Close'].shift(8*21) * 100
    df2['Percentage Change'] = (df2['Close'] - df2['Close'].shift(8*21)) / df2['Close'].shift(8*21) * 100

    # Smoothened percentage change with a rolling average of 10 days
    df1['Smoothed Percentage Change'] = df1['Percentage Change'].rolling(window=10).mean()
    df2['Smoothed Percentage Change'] = df2['Percentage Change'].rolling(window=10).mean()

    st.write(f"Closing price today for {ticker_symbol1}:", df1['Close'].iloc[-1])
    st.write(f"Closing price of {ticker_symbol1} 8 months ago:", df1['Close'][specific_date])
    st.write(f"Percentage change in {ticker_symbol1} over 8 months:", df1['Percentage Change'].iloc[-1])

    st.write(f"Closing price today for {ticker_symbol2}:", df2['Close'].iloc[-1])
    st.write(f"Closing price of {ticker_symbol2} 8 months ago:", df2['Close'][specific_date])
    st.write(f"Percentage change in {ticker_symbol2} over 8 months:", df2['Percentage Change'].iloc[-1])

    if use_smoothed:
        st.write("Smoothed Percentage Change (10-day rolling average)")
        st.line_chart(df1, x="Dates", y=['Smoothed Percentage Change'], use_container_width=True)
        st.line_chart(df2, x="Dates", y=['Smoothed Percentage Change'], use_container_width=True)
        
    else:
        st.write("Percentage Change (8 months ago)")
        st.line_chart(df1, x="Dates", y=['Percentage Change'], use_container_width=True)
        st.line_chart(df2, x="Dates", y=['Percentage Change'], use_container_width=True)
        

# Streamlit UI      


st.title('Stock Comparison Tool')
ticker_symbol1 = st.selectbox('Select the first ticker symbol:', ticker_symbols)
ticker_symbol2 = st.selectbox('Select the second ticker symbol:', ticker_symbols)

use_smoothed = st.checkbox('Use Smoothed Percentage Change')

if st.button('Compare'):
    calculate_percentage_change(ticker_symbol1, ticker_symbol2, use_smoothed)

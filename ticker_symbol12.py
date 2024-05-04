import yfinance as yf
from datetime import date, timedelta
import pandas as pd
import streamlit as st

ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX', 'CASHX']

def calculate_percentage_change(selected_tickers, use_smoothed):
    dfs = []
    
    
    for ticker_symbol in ticker_symbols:
        df = yf.download(ticker_symbol, start="2020-01-01", end=date.today())
        df['Dates'] = pd.to_datetime(df.index)  # Convert the index to datetime format
        
        eight_months_ago_months_ago = date.today() - timedelta(days=8*30)  # Approximating 30 days per month
        last_day_8_months_ago = eight_months_ago_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
        specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
        closing_today = df['Close'].iloc[-1]
        
        
        df['Percentage Change' + ticker_symbol] = (((df['Close'] - df['Close'].shift(21*8)) / (df['Close'].shift(21*8))) *100)

        # Smoothened percentage change with a rolling average of 10 days
        df['Smoothed Percentage Change' + ticker_symbol] = df['Percentage Change' + ticker_symbol].rolling(window=10).mean()
            
       
        st.write(f"Percentage change in {ticker_symbol} over 8 months:", df['Percentage Change' + ticker_symbol].iloc[-1])
        
        # Merge based on the 'Dates' column
        joined_df = pd.concat(dfs, axis=1, join='inner')
              
                      
        if use_smoothed:
            st.write("Smoothed Percentage Change (10-day rolling average)")
            selected_cols = ['Dates', 'Smoothed Percentage Change'+ ticker_symbol for ticker_symbol in selected_tickers]
        
        else:   
            st.write("Percentage Change (8 months ago)")
            selected_cols = ['Dates', 'Percentage Change'+ ticker_symbol for ticker_symbol in selected_tickers]
            
        st.line_chart(joined_df[selected_cols], x="Dates", use_container_width=True)
    


# Multiselect for ticker symbols
selected_tickers = st.multiselect('Select Ticker Symbols', ticker_symbols, default=ticker_symbols)

use_smoothed = st.checkbox('Use Smoothed Percentage Change')


if st.button('Compare'):
    calculate_percentage_change(selected_tickers, use_smoothed)

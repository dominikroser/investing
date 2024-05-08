import yfinance as yf
from datetime import date, timedelta
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX']

def calculate_percentage_change(selected_tickers, use_smoothed, selected_date):
    dfs = []
    
    for ticker_symbol in selected_tickers:
        df = yf.download(ticker_symbol, start="2020-01-01", end=date.today())
        df['Dates'] = pd.to_datetime(df.index)  # Convert the index to datetime format
        selected_date = pd.to_datetime(selected_date)
        
        eight_months_ago_months_ago = selected_date - timedelta(days=8*30)  # Approximating 30 days per month
        last_day_8_months_ago = eight_months_ago_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
        specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
        #closing_today = df['Close'].iloc[-1]
        
        df['Percentage Change_' + ticker_symbol] = (((df['Close'] - df['Close'].shift(21*8)) / (df['Close'].shift(21*8))) * 100)
        
        # Smoothened percentage change with a rolling average of 10 days
        
        st.header(f"Statistic on {ticker_symbol}")
        st.write(f"Closing price selected date for {ticker_symbol}:", df['Close'][selected_date])
        st.write(f"Closing price of {ticker_symbol} 8 months ago:", df['Close'][specific_date])
        st.write(f"Percentage change in {ticker_symbol} over 8 months:", df['Percentage Change_' + ticker_symbol][selected_date])
        
        df['Smoothed Percentage Change_' + ticker_symbol] = df['Percentage Change_' + ticker_symbol].rolling(window=10).mean()
        
        df = df.rename(columns={
            'Close':'Close_' + ticker_symbol,
            'Open': 'Open_' + ticker_symbol,
            'Volume': 'Volume_' + ticker_symbol,
            'High': 'High_' + ticker_symbol,
            'Low': 'Low_' + ticker_symbol,
            'Adj Close': 'Adj Close_' + ticker_symbol,
        })
        
        dfs.append(df[['Dates', 'Percentage Change_' + ticker_symbol, 'Smoothed Percentage Change_' + ticker_symbol]])
    
    joined_df = pd.concat(dfs, axis=1)  # Concatenate the DataFrames
    joined_df = joined_df.loc[:, ~joined_df.columns.duplicated()]  # Remove duplicate columns
            
    if use_smoothed:
            plt.figure(figsize=(10, 6))
            plt.title("Smoothed Percentage Change (10-day rolling average)")
            for ticker_symbol in selected_tickers:
                col = 'Smoothed Percentage Change_' + ticker_symbol
                plt.plot(joined_df['Dates'], joined_df[col], label=ticker_symbol)
            plt.xlabel("Date")
            plt.ylabel("Smoothed Percentage Change")
            plt.legend()
            st.pyplot(plt)  # Display the plot using st.pyplot() instead of plt.show()

    else:
            plt.figure(figsize=(10, 6))
            plt.title("Percentage Change (8 months ago)")
            for ticker_symbol in selected_tickers:
                col = 'Percentage Change_' + ticker_symbol
                plt.plot(joined_df['Dates'], joined_df[col], label=ticker_symbol)
            plt.xlabel("Date")
            plt.ylabel("Percentage Change")
            plt.legend()
            st.pyplot(plt)  # Display the plot using st.pyplot() instead of plt.show()

        
    
st.title('Asset Management - Family office')

st.header('Please select date')
selected_date = st.date_input('Select Date', value=date.today())

# Multiselect for ticker symbols
selected_tickers = st.multiselect('Select Ticker Symbols', ticker_symbols, default=ticker_symbols)

use_smoothed = st.checkbox('Use Smoothed Percentage Change')


if st.button('Compare'):
    calculate_percentage_change(selected_tickers, use_smoothed, selected_date)


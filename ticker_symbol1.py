import yfinance as yf
from datetime import date, timedelta
import streamlit as st
import matplotlib.pyplot as plt

ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX', 'CASHX']

def relative_strength(ticker_symbol, comparison_symbol):
    df = yf.download(ticker_symbol, start="2023-01-01", end=date.today())
    df['Date'] = df.index
    
    seven_months_ago = date.today() - timedelta(days=7*30)  # Approximating 30 days per month
    last_day_8_months_ago = seven_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
    closing_today = df['Close'].iloc[-1]
    
    specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
    closing_price_8months = df.loc[specific_date, 'Close']
    
    df_comp = yf.download(comparison_symbol, start="2023-01-01", end=date.today())
    df_comp['Date'] = df_comp.index
    closing_today_comp = df_comp['Close'].iloc[-1]
    closing_price_8months_comp = df_comp.loc[specific_date, 'Close']
    
    percentage_change = ((closing_today - closing_price_8months) / closing_price_8months) * 100
    percentage_change_comp = ((closing_today_comp - closing_price_8months_comp) / closing_price_8months_comp) * 100
    
    st.write("Closing price today:", closing_today)
    st.write(f"Closing price of {ticker_symbol} 8 months ago:", closing_price_8months)
    st.write(f"Percentage change in {ticker_symbol} over 8 months:", percentage_change)
    
    st.write("Closing price today for comparison symbol:", closing_today_comp)
    st.write(f"Closing price of {comparison_symbol} 8 months ago:", closing_price_8months_comp)
    st.write(f"Percentage change in {comparison_symbol} over 8 months:", percentage_change_comp)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Close'], label=ticker_symbol)
    plt.plot(df_comp['Date'], df_comp['Close'], label=comparison_symbol)
    plt.title(f'Closing Prices Comparison: {ticker_symbol} vs {comparison_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Streamlit UI
st.title('Stock Comparison Tool')
ticker_symbol = st.selectbox('Select the first ticker symbol:', ticker_symbols)
comparison_symbol = st.selectbox('Select the second ticker symbol:', ticker_symbols)

if st.button('Compare'):
    relative_strength(ticker_symbol, comparison_symbol)

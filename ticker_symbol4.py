import yfinance as yf
from datetime import date, timedelta
import streamlit as st


ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX', 'CASHX']

def relative_strength(ticker_symbol1, ticker_symbol2):
    df1 = yf.download(ticker_symbol1, start="2023-01-01", end=date.today())
    df1['Date'] = df1.index
    
    seven_months_ago = date.today() - timedelta(days=7*30)  # Approximating 30 days per month
    last_day_8_months_ago = seven_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
    closing_today1 = df1['Close'].iloc[-1]
    
    specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
    closing_price_8months1 = df1.loc[specific_date, 'Close']
    
    df2 = yf.download(ticker_symbol2, start="2023-01-01", end=date.today())
    df2['Date'] = df2.index
    closing_today2 = df2['Close'].iloc[-1]
    closing_price_8months2 = df2.loc[specific_date, 'Close']
    
    st.write(f"Closing price today for {ticker_symbol1}:", closing_today1)
    st.write(f"Closing price of {ticker_symbol1} 8 months ago:", closing_price_8months1)
    
    st.write(f"Closing price today for {ticker_symbol2}:", closing_today2)
    st.write(f"Closing price of {ticker_symbol2} 8 months ago:", closing_price_8months2)
    
    # Plotting
    combined_df = df1[['Close']]
    
    rename(columns={'Close': ticker_symbol1}).join(df2[['Close']].rename(columns={'Close': ticker_symbol2}))
    st.line_chart(combined_df, use_container_width=True)
    
# Streamlit UI
st.title('Stock Comparison Tool')
ticker_symbol1 = st.selectbox('Select the first ticker symbol:', ticker_symbols)
ticker_symbol2 = st.selectbox('Select the second ticker symbol:', ticker_symbols)
    
if st.button('Compare'):
    relative_strength(ticker_symbol1, ticker_symbol2)


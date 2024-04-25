import yfinance as yf
from datetime import date, timedelta
import streamlit as st

ticker_symbols = ['FSPTX', 'FBMPX', 'FSENX', 'FDFAX', 'CASHX']

def relative_strength(ticker_symbols):
    combined_df = None
    
    for ticker_symbol in ticker_symbols:
        df = yf.download(ticker_symbol, start="2023-01-01", end=date.today())
        df['Date'] = df.index
        
        seven_months_ago = date.today() - timedelta(days=7*30)  # Approximating 30 days per month
        last_day_8_months_ago = seven_months_ago.replace(day=1) - timedelta(days=1) # Calculate the last day of the month 8 months ago
        closing_today = df['Close'].iloc[-1]
        
        specific_date = last_day_8_months_ago.strftime('%Y-%m-%d')
        closing_price_8months = df.loc[specific_date, 'Close']
        
        st.write(f"Closing price today for {ticker_symbol}:", closing_today)
        st.write(f"Closing price of {ticker_symbol} 8 months ago:", closing_price_8months)
        
        # Concatenate data
        if combined_df is None:
            combined_df = df[['Close']].rename(columns={'Close': ticker_symbol})
        else:
            combined_df = combined_df.join(df[['Close']].rename(columns={'Close': ticker_symbol}))
    
    # Plotting
    st.line_chart(combined_df, use_container_width=True)

# Streamlit UI
st.title('Stock Comparison Tool')

if st.button('Compare'):
    relative_strength(ticker_symbols)


import yfinance as yf
import streamlit as st

st.title("HOLA TEAM NLP AQUI PODEMOS HACER COSAS CHEVERES")
st.write("""

# Hola NATA ERES LA MEJOR
# Simple Stock Price App
Shown are the stock closing price and volume of Google!
""")




# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'TSLA'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2021-11-30')
# Open	High	Low	Close	Volume	Dividends	Stock Splits


if st.button('Click aqui para descargar ALG de ayer'):
    st.write('Downloading yesterday calls')
else:
    st.write('Goodbye')

st.area_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)

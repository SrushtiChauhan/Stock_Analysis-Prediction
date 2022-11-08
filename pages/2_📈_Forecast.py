import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data
import datetime
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
pd.options.mode.chained_assignment = None
tf.random.set_seed(0)

st.set_page_config(page_title="Stock Price Forecasting", page_icon="chart_with_upwards_trend", 
                        layout="centered", initial_sidebar_state = "auto")

list_sectors = []
list_sectors.append('Basic Materials')
list_sectors.append('Communication Services')
list_sectors.append('Consumer Cyclical')
list_sectors.append('Consumer Defensive')
list_sectors.append('Energy')
list_sectors.append('Financial Services')
list_sectors.append('Healthcare')
list_sectors.append('Industrials')
list_sectors.append('Real Estate')
list_sectors.append('Technology')
list_sectors.append('Utilities')
#list_sectors

ticker_list = si.tickers_nasdaq()

df1 = pd.read_csv('data/basic_materials_ticker_list.csv')['Basic Materials']
list_bm = df1.values.tolist()
df2 = pd.read_csv('data/communication_services_ticker_list.csv')['Communication Services']
list_cs = df2.values.tolist()
df3 = pd.read_csv('data/consumer_cyclical_ticker_list.csv')['Consumer Cyclical']
list_cc = df3.values.tolist()
df4 = pd.read_csv('data/consumer_defensive_ticker_list.csv')['Consumer Defensive']
list_cd = df4.values.tolist()
df5 = pd.read_csv('data/energy_ticker_list.csv')['Energy']
list_en = df5.values.tolist()
df6 = pd.read_csv('data/financial_services_ticker_list.csv')['Financial Services']
list_fs = df6.values.tolist()
df7 = pd.read_csv('data/healthcare_ticker_list.csv')['Healthcare']
list_hc = df7.values.tolist()
df8 = pd.read_csv('data/industrials_ticker_list.csv')['Industrials']
list_id = df8.values.tolist()
df9 = pd.read_csv('data/real_estate_ticker_list.csv')['Real Estate']
list_re = df9.values.tolist()
df10 = pd.read_csv('data/technology_ticker_list.csv')['Technology']
list_tc = df10.values.tolist()
df11 = pd.read_csv('data/utilities_ticker_list.csv')['Utilities']
list_ut = df11.values.tolist()

currentDate = datetime.date.today()
firstDayOfMonth = datetime.date(currentDate.year, currentDate.month, 1)

title_col1,title_col2 = st.columns([5,5])
with title_col1:
    sector_name = st.selectbox('Select Sector :',list_sectors,index = 0)
with title_col2:
    if sector_name == "Basic Materials":
        ticker_name = st.selectbox('Select Ticker :',list_bm,index = 0)
    if sector_name == "Communication Services":
        ticker_name = st.selectbox('Select Ticker :',list_cs,index = 0)
    if sector_name == "Consumer Cyclical":
        ticker_name = st.selectbox('Select Ticker :',list_cc,index = 0)
    if sector_name == "Consumer Defensive":
        ticker_name = st.selectbox('Select Ticker :',list_cd,index = 0)
    if sector_name == "Energy":
        ticker_name = st.selectbox('Select Ticker :',list_en,index = 0)
    if sector_name == "Financial Services":
        ticker_name = st.selectbox('Select Ticker :',list_fs,index = 0)
    if sector_name == "Healthcare":
        ticker_name = st.selectbox('Select Ticker :',list_hc,index = 0)
    if sector_name == "Industrials":
        ticker_name = st.selectbox('Select Ticker :',list_id,index = 0)
    if sector_name == "Real Estate":
        ticker_name = st.selectbox('Select Ticker :',list_re,index = 0)
    if sector_name == "Technology":
        ticker_name = st.selectbox('Select Ticker :',list_tc,index = 0)
    if sector_name == "Utilities":
        ticker_name = st.selectbox('Select Ticker :',list_ut,index = 0)

def get_forecast(ticker_name):
    # download the data
    df = yf.download(tickers=ticker_name, period='6mo')
    y = df['Close'].fillna(method='ffill')
    y = y.values.reshape(-1, 1)

    # scale the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y = scaler.transform(y)

    # generate the input and output sequences
    n_lookback = 60  # length of input sequences (lookback period)
    n_forecast = 30  # length of output sequences (forecast period)

    X = []
    Y = []

    for i in range(n_lookback, len(y) - n_forecast + 1):
        X.append(y[i - n_lookback: i])
        Y.append(y[i: i + n_forecast])

    X = np.array(X)
    Y = np.array(Y)

    # fit the model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(n_lookback, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(n_forecast))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, Y, epochs=100, batch_size=32, verbose=0)

    # generate the forecasts
    X_ = y[- n_lookback:]  # last available input sequence
    X_ = X_.reshape(1, n_lookback, 1)

    Y_ = model.predict(X_).reshape(-1, 1)
    Y_ = scaler.inverse_transform(Y_)

    # organize the results in a data frame
    df_past = df[['Close']].reset_index()
    df_past.rename(columns={'index': 'Date', 'Close': 'Actual'}, inplace=True)
    df_past['Date'] = pd.to_datetime(df_past['Date'])
    df_past['Forecast'] = np.nan
    df_past['Forecast'].iloc[-1] = df_past['Actual'].iloc[-1]

    df_future = pd.DataFrame(columns=['Date', 'Actual', 'Forecast'])
    df_future['Date'] = pd.date_range(start=df_past['Date'].iloc[-1] + pd.Timedelta(days=1), periods=n_forecast)
    df_future['Forecast'] = Y_.flatten()
    df_future['Actual'] = np.nan

    results = df_past.append(df_future).set_index('Date')
    return results

if st.button('Forecast'):
    df_results = get_forecast(ticker_name)
    # Plot the forecast values 
    fig = plt.figure() 
    df_results['Actual'].plot(figsize = (20, 5), legend = True, title=ticker_name) 
    df_results['Forecast'].plot(legend = True)
    st.pyplot(fig)


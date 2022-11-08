import streamlit as st
import yahoo_fin.stock_info as si
from yahoo_fin.stock_info import get_data
import yfinance as yf
import datetime
import pandas as pd

st.set_page_config(page_title="Stock Price Analysis and Comparision", page_icon="📊", 
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

st.markdown("""# *Finance Data Analysis*""")

currentDate = datetime.date.today()
firstDayOfMonth = datetime.date(currentDate.year, currentDate.month, 1)

title_col1,title_col2,title_col3,title_col4 = st.columns([3,2,2,2])
with title_col1:
    sector_name = st.selectbox('Select Sector :',list_sectors,index = 0)
with title_col2:
    st_date = st.date_input('Start Date :', firstDayOfMonth, datetime.date(1980, 1, 1), currentDate)
with title_col3:
    en_date = st.date_input('End Date :',currentDate)
with title_col4:
        interval_option = st.selectbox(
        'Time Interval',
        ('Day', 'Month'))

if interval_option == "Month":
    interval_option = "1mo"
else :
    interval_option = "1d"

title_col1,title_col2,title_col3 = st.columns([3,3,3])
with title_col1:
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
with title_col2:
    if sector_name == "Basic Materials":
        ticker_name2 = st.selectbox('Select Ticker :',list_bm,index = 1)
    if sector_name == "Communication Services":
        ticker_name2 = st.selectbox('Select Ticker :',list_cs,index = 1)
    if sector_name == "Consumer Cyclical":
        ticker_name2 = st.selectbox('Select Ticker :',list_cc,index = 1)
    if sector_name == "Consumer Defensive":
        ticker_name2 = st.selectbox('Select Ticker :',list_cd,index = 1)
    if sector_name == "Energy":
        ticker_name2 = st.selectbox('Select Ticker :',list_en,index = 1)
    if sector_name == "Financial Services":
        ticker_name2 = st.selectbox('Select Ticker :',list_fs,index = 1)
    if sector_name == "Healthcare":
        ticker_name2 = st.selectbox('Select Ticker :',list_hc,index = 1)
    if sector_name == "Industrials":
        ticker_name2 = st.selectbox('Select Ticker :',list_id,index = 1)
    if sector_name == "Real Estate":
        ticker_name2 = st.selectbox('Select Ticker :',list_re,index = 1)
    if sector_name == "Technology":
        ticker_name2 = st.selectbox('Select Ticker :',list_tc,index = 1)
    if sector_name == "Utilities":
        ticker_name2 = st.selectbox('Select Ticker :',list_ut,index = 1) 
with title_col3:
    if sector_name == "Basic Materials":
        ticker_name3 = st.selectbox('Select Ticker :',list_bm,index = 2)
    if sector_name == "Communication Services":
        ticker_name3 = st.selectbox('Select Ticker :',list_cs,index = 2)
    if sector_name == "Consumer Cyclical":
        ticker_name3 = st.selectbox('Select Ticker :',list_cc,index = 2)
    if sector_name == "Consumer Defensive":
        ticker_name3 = st.selectbox('Select Ticker :',list_cd,index = 2)
    if sector_name == "Energy":
        ticker_name3 = st.selectbox('Select Ticker :',list_en,index = 2)
    if sector_name == "Financial Services":
        ticker_name3 = st.selectbox('Select Ticker :',list_fs,index = 2)
    if sector_name == "Healthcare":
        ticker_name3 = st.selectbox('Select Ticker :',list_hc,index = 2)
    if sector_name == "Industrials":
        ticker_name3 = st.selectbox('Select Ticker :',list_id,index = 2)
    if sector_name == "Real Estate":
        ticker_name3 = st.selectbox('Select Ticker :',list_re,index = 2)
    if sector_name == "Technology":
        ticker_name3 = st.selectbox('Select Ticker :',list_tc,index = 2)
    if sector_name == "Utilities":
        ticker_name3 = st.selectbox('Select Ticker :',list_ut,index = 2) 

title_col1,title_col2,title_col3 = st.columns([4,4,4])
with title_col1:
    ticker_details = get_data(ticker_name, start_date=st_date, end_date=en_date, index_as_date = True, interval=interval_option)
    df = ticker_details
    df['pc_returns'] = (df['close']/df['close'].shift(1) - 1) * 100
    df['pc_returns'] = round(df['pc_returns'], 2)
    df = df[['close','pc_returns']]
    df.index = df.index.strftime('%m/%d/%Y')
    if (len(ticker_details) > 0):
        st.subheader(f'{ticker_name} Stock Data')
        st.dataframe(df.tail())
        st.line_chart(df.pc_returns)
    else:   
        st.write("No Data Found!")
with title_col2:
    ticker_details = get_data(ticker_name2, start_date=st_date, end_date=en_date, index_as_date = True, interval=interval_option)
    df2 = ticker_details
    df2['pc_returns'] = (df2['close']/df2['close'].shift(1) - 1) * 100
    df2['pc_returns'] = round(df2['pc_returns'], 2)
    df2 = df2[['close','pc_returns']]
    df2.index = df2.index.strftime('%m/%d/%Y')
    if (len(ticker_details) > 0):
        st.subheader(f'{ticker_name2} Stock Data')
        st.dataframe(df2.tail())
        st.line_chart(df2.pc_returns)
    else:   
        st.write("No Data Found!")
with title_col3:
    ticker_details = get_data(ticker_name3, start_date=st_date, end_date=en_date, index_as_date = True, interval=interval_option)
    df3 = ticker_details
    df3['pc_returns'] = (df3['close']/df3['close'].shift(1) - 1) * 100
    df3['pc_returns'] = round(df3['pc_returns'], 2)
    df3 = df3[['close','pc_returns']]
    df3.index = df3.index.strftime('%m/%d/%Y')
    if (len(ticker_details) > 0):
        st.subheader(f'{ticker_name3} Stock Data')
        st.dataframe(df3.tail())
        st.line_chart(df3.pc_returns)
    else:   
        st.write("No Data Found!")

title_col1,title_col2,title_col3 = st.columns([3,3,3])
with title_col1:
    tkr = yf.Ticker(ticker_name)
    ticker_info = tkr.info
    st.write('<p style="font-size:20px">', ticker_info['symbol'], " - ", ticker_info['shortName'] ,'</p>', unsafe_allow_html=True)
    #st.image(ticker_info['logo_url'])
    st.write('<p style="font-size:20px"> Sector : ', ticker_info['sector'] ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> 52Week High-Low : ', str(ticker_info['fiftyTwoWeekHigh']), '-', str(ticker_info['fiftyTwoWeekLow']), '</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> day High-Low : ', str(ticker_info['dayHigh']), '-', str(ticker_info['dayLow']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> Current Price : ', str(ticker_info['currentPrice']), " ", str(ticker_info['financialCurrency']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> marketCap : ', str(ticker_info['marketCap']) ,'</p>', unsafe_allow_html=True)
with title_col2:
    tkr = yf.Ticker(ticker_name2)
    ticker_info = tkr.info
    st.write('<p style="font-size:20px">', ticker_info['symbol'], " - ", ticker_info['shortName'] ,'</p>', unsafe_allow_html=True)
    #st.image(ticker_info['logo_url'])
    st.write('<p style="font-size:20px"> Sector : ', ticker_info['sector'] ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> 52Week High-Low : ', str(ticker_info['fiftyTwoWeekHigh']), '-', str(ticker_info['fiftyTwoWeekLow']), '</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> day High-Low : ', str(ticker_info['dayHigh']), '-', str(ticker_info['dayLow']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> Current Price : ', str(ticker_info['currentPrice']), " ", str(ticker_info['financialCurrency']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> marketCap : ', str(ticker_info['marketCap']) ,'</p>', unsafe_allow_html=True)
with title_col3:
    tkr = yf.Ticker(ticker_name3)
    ticker_info = tkr.info
    st.write('<p style="font-size:20px">', ticker_info['symbol'], " - ", ticker_info['shortName'] ,'</p>', unsafe_allow_html=True)
    #st.image(ticker_info['logo_url'])
    st.write('<p style="font-size:20px"> Sector : ', ticker_info['sector'] ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> 52Week High-Low : ', str(ticker_info['fiftyTwoWeekHigh']), '-', str(ticker_info['fiftyTwoWeekLow']), '</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> day High-Low : ', str(ticker_info['dayHigh']), '-', str(ticker_info['dayLow']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> Current Price : ', str(ticker_info['currentPrice']), " ", str(ticker_info['financialCurrency']) ,'</p>', unsafe_allow_html=True)
    st.write('<p style="font-size:20px"> marketCap : ', str(ticker_info['marketCap']) ,'</p>', unsafe_allow_html=True)


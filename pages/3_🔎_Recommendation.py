import streamlit as st
import requests, json, re
from parsel import Selector
from itertools import zip_longest
from bs4 import BeautifulSoup
import requests, lxml, json
import pandas as pd
import yahoo_fin.stock_info as si
import yfinance as yf
import time

# https://docs.python.org/3/library/itertools.html#itertools.zip_longest
from itertools import zip_longest 

def scrape_google_finance(ticker: str):
    params = {
        "hl": "en" # language
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
        }

    html = requests.get(f"https://www.google.com/finance/quote/{ticker}", params=params, headers=headers, timeout=30)
    selector = Selector(text=html.text)
    
    # where all extracted data will be temporary located
    ticker_data = {
        "ticker_data": {},
        "about_panel": {},
        "news": {"items": []},
        "finance_perfomance": {"table": []}, 
        "people_also_search_for": {"items": []},
        "interested_in": {"items": []}
    }
    
    # current price, quote, title extraction
    ticker_data["ticker_data"]["current_price"] = selector.css(".AHmHk .fxKbKc::text").get()
    ticker_data["ticker_data"]["quote"] = selector.css(".PdOqHc::text").get().replace(" • ",":")
    ticker_data["ticker_data"]["title"] = selector.css(".zzDege::text").get()
    
    # about panel extraction
    about_panel_keys = selector.css(".gyFHrc .mfs7Fc::text").getall()
    about_panel_values = selector.css(".gyFHrc .P6K39c").xpath("normalize-space()").getall()
    
    for key, value in zip_longest(about_panel_keys, about_panel_values):
        key_value = key.lower().replace(" ", "_")
        ticker_data["about_panel"][key_value] = value
    
    # description "about" extraction
    ticker_data["about_panel"]["description"] = selector.css(".bLLb2d::text").get()
    ticker_data["about_panel"]["extensions"] = selector.css(".w2tnNd::text").getall()
    
    # news extarction
    if selector.css(".yY3Lee").get():
        for index, news in enumerate(selector.css(".yY3Lee"), start=1):
            ticker_data["news"]["items"].append({
                "position": index,
                "title": news.css(".Yfwt5::text").get(),
                "link": news.css(".z4rs2b a::attr(href)").get(),
                "source": news.css(".sfyJob::text").get(),
                "published": news.css(".Adak::text").get(),
                "thumbnail": news.css("img.Z4idke::attr(src)").get()
            })
    else: 
        ticker_data["news"]["error"] = f"No news result from a {ticker}."

    # finance perfomance table
    if selector.css(".slpEwd .roXhBd").get():
        fin_perf_col_2 = selector.css(".PFjsMe+ .yNnsfe::text").get()           # e.g. Dec 2021
        fin_perf_col_3 = selector.css(".PFjsMe~ .yNnsfe+ .yNnsfe::text").get()  # e.g. Year/year change
        
        for fin_perf in selector.css(".slpEwd .roXhBd"):
            if fin_perf.css(".J9Jhg::text , .jU4VAc::text").get():
                perf_key = fin_perf.css(".J9Jhg::text , .jU4VAc::text").get()   # e.g. Revenue, Net Income, Operating Income..
                perf_value_col_1 = fin_perf.css(".QXDnM::text").get()           # 60.3B, 26.40%..   
                perf_value_col_2 = fin_perf.css(".gEUVJe .JwB6zf::text").get()  # 2.39%, -21.22%..
                
                ticker_data["finance_perfomance"]["table"].append({
                    perf_key: {
                        fin_perf_col_2: perf_value_col_1,
                        fin_perf_col_3: perf_value_col_2
                    }
                })
    else:
        ticker_data["finance_perfomance"]["error"] = f"No 'finence perfomance table' for {ticker}."
    
    # "you may be interested in" results
    if selector.css(".HDXgAf .tOzDHb").get():
        for index, other_interests in enumerate(selector.css(".HDXgAf .tOzDHb"), start=1):
            ticker_data["interested_in"]["items"].append(discover_more_tickers(index, other_interests))
    else:
        ticker_data["interested_in"]["error"] = f"No 'you may be interested in` results for {ticker}"
    
    
    # "people also search for" results
    if selector.css(".HDXgAf+ div .tOzDHb").get():
        for index, other_tickers in enumerate(selector.css(".HDXgAf+ div .tOzDHb"), start=1):
            ticker_data["people_also_search_for"]["items"].append(discover_more_tickers(index, other_tickers))
    else:
        ticker_data["people_also_search_for"]["error"] = f"No 'people_also_search_for` in results for {ticker}"
        

    return ticker_data


def discover_more_tickers(index: int, other_data: str):
    """
    if price_change_formatted will start complaining,
    check beforehand for None values with try/except and set it to 0, in this function.
    
    however, re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%" should make the job done.
    """
    return {
            "position": index,
            "ticker": other_data.css(".COaKTb::text").get(),
            "ticker_link": f'https://www.google.com/finance{other_data.attrib["href"].replace("./", "/")}',
            "title": other_data.css(".RwFyvf::text").get(),
            "price": other_data.css(".YMlKec::text").get(),
            "price_change": other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get(),
            # https://regex101.com/r/BOFBlt/1
            # Up by 100.99% -> 100.99%
            "price_change_formatted": re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%", other_data.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group()
        }

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


tkr = yf.Ticker(ticker_name)
ticker_info = tkr.info

ten_year_treasury_rate_tkr = yf.Ticker("^TNX")

data = scrape_google_finance(ticker=f"{ticker_name}:NASDAQ")

# st.snow()
# st.balloons()
# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')
# st.warning('This is a warning', icon="⚠️")
# st.error('This is an error', icon="🚨")
# st.info('This is a purely informational message', icon="ℹ️")
# st.success('This is a success message!', icon="✅")

title_col1,title_col2,title_col3 = st.columns([6,4,3])
with title_col1:
    st.write(ticker_info['shortName'])
with title_col2:
    st.write('Current Price : 💲', ticker_info['currentPrice'])
with title_col3:
    recc = ticker_info['recommendationKey']
    if recc == 'none':
        st.warning('Hold')
    if recc == 'buy':
        st.info('Buy')
    if recc == 'strong_buy':
        st.success('Strongly Buy')

title_col1,title_col2,title_col3 = st.columns([3,3,3])
with title_col1:
    st.write('MarketCap', ticker_info['marketCap'])
with title_col2:
    st.write('Gross Profits', ticker_info['grossProfits'])
with title_col3:
    st.write('Last Dividend Value', ticker_info['lastDividendValue'])

title_col1,title_col2,title_col3 = st.columns([5,4,3])
with title_col1:
    st.write('52 Week High - Low ', ticker_info['fiftyTwoWeekHigh'], '-', ticker_info['fiftyTwoWeekLow'])
with title_col2:
    st.write('Day High - Low', ticker_info['dayHigh'], '-', ticker_info['dayLow'])
with title_col3:
    st.write('Tradeable', ticker_info['tradeable'])

st.subheader('Business Summary:')
st.write(ticker_info['longBusinessSummary'])

st.subheader('News:')
count = 1
for key in data['news']['items']:
    st.write('<b>' ,str(count),'. ', str(key['title']), '</b>', unsafe_allow_html=True)
    st.write(key['link'])
    st.write('published : ', str(key['published']))
    count += 1
st.subheader("people also search for:")
for key in data['people_also_search_for']['items']:
    st.write('<p style="color:#2c47bfc9;font-weight: bold;">',str(key['position']),'. ', str(key['ticker']), '-', str(key['title']),'</p>', unsafe_allow_html=True)
    st.write('current_price : ', key['price'])
    color = 'blue'
    if 'Down' in str(key['price_change']):
        color = 'red'
    if 'Up' in str(key['price_change']):
        color = 'green'
    st.write('price_change : ','<x style="color:', color, '">', str(key['price_change']), '</x>', unsafe_allow_html=True)

# st.write(ticker_info)

# st.write(data)

# for key in data['ticker_data']:
#     st.write(key, '->', data['ticker_data'][key])


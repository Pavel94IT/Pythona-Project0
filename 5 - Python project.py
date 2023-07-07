import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1
tesla_data = yf.Ticker('TSLA')
tesla_data = tesla_data.history(period='max')
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


#Question 2
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data  = requests.get(url).text

soup = BeautifulSoup(html_data, 'html.parser')
soup.find_all('title')
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    Date = col[0].text
    Revenue = col[1].text.replace("$", ""). replace(",","")
    
    tesla_revenue = tesla_revenue._append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
tesla_revenue.reset_index(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(tesla_revenue.tail())

#Question 3
gme_data = yf.Ticker("GME")
gme_data = gme_data.history(period='max')
gme_data.reset_index(inplace=True)
print(gme_data.head(5))

#Question 4 
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data1  = requests.get(url).text

soup1 = BeautifulSoup(html_data1, 'html.parser')
soup1.find_all('title')
GME_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup1.find_all("tbody")[0].find_all('tr'):
    col = row.find_all("td")
    Date = col[0].text
    Revenue = col[1].text.replace("$", ""). replace(",",".")
    
    GME_revenue = GME_revenue._append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

print(GME_revenue.tail())

#Question 5

make_graph(tesla_data, tesla_revenue,'TESLA')

#Question 6

make_graph(gme_data, GME_revenue,'GME')
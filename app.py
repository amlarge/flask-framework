from flask import Flask, render_template, request, redirect
import simplejson as json
import requests
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, DatetimeTickFormatter, ColumnDataSource

app = Flask(__name__)

def get_symbol_df(symbol=None):
    r=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+symbol+'&interval=5min&apikey=FU9ZYEC8317G7IUI')
    rjs=r.json()['Time Series (Daily)']
    rpanda=pd.DataFrame.from_dict(rjs)
    rdf=rpanda.transpose()
    stockdata=rdf.apply(pd.to_numeric)
    stockdata.reset_index(inplace=True)
    stockdata["Date"] = pd.to_datetime(stockdata['index'])
    stockdata['ToolTipDates'] = stockdata.Date.map(lambda x: x.strftime("%b %d")) # Saves work with the tooltip later
    return stockdata

def plot_stock_price(stock):
    Plot = figure(plot_width=500, plot_height=250,
               title="Stock price", toolbar_location='above', x_axis_type = 'datetime')
    Plot.xaxis[0].formatter = DatetimeTickFormatter(days='%b %d')
    #bp.output_file('columnDataSource.html', title = 'ColumnDataSource')
    Plot.line('date','2. high', line_width=5, source=data)
    Plot.add_tools(HoverTool(tooltips= [("Date",'@ToolTipDates'),
                                    ("Price","$@{2. high}{0.00 a}")], mode='vline'))

    return Plot

@app.route('/')
def index():
  return render_template('index.html')

#@app.route('/about')
#def about():
#  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507, debug=True)

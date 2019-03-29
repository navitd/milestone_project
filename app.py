"""
to run the application see
http://flask.pocoo.org/docs/1.0/quickstart/

"""
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
import numpy as np
import pandas as pd
import quandl
from flask import Flask, render_template, request, redirect #url_for
from datetime import date, timedelta

app = Flask(__name__) # app is an instance of class Flask

#@app.route('/') #route means: which function corresponds to which URL
#def index():
#  return render_template('index.html')

#@app.route('/about') #which URL triggers about
#def about():
#  return render_template('about.html')

@app.route('/tickerprompt', methods=['GET', 'POST']) #go to /tickerprompt to be asked for a ticker name
def tic_prm():
    #if request.method == 'POST':
    #    ticker_name=request.form['ticker_name']
    return render_template('tic_prm.html')


@app.route('/Graph', methods=['POST', 'GET']) 
def plt_graph(ticker_name=None):
    ticker_name=request.form['ticker_name']
    
    quandl.ApiConfig.api_key = 'bdNDUXp1kqGLKMoWH9H2'
    #ticker_name="AAPL"
    start_date="2015-12-31"
    end_date="2016-12-31"
    data = quandl.get_table('WIKI/PRICES', ticker = ticker_name, 
                           qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                            date = { 'gte': start_date, 'lte': end_date }, 
                            paginate=True)
    
    if len(data) == 0:
        return ('','','Did not find any data, <br>' + 
                       'try changing ticker name')
    # create a new dataframe with 'date' column as index
    new = data.set_index('date')
    # use pandas pivot function to sort adj_close by tickers
    clean_data = new.pivot(columns='ticker')
    #remove hirarchy from column lables
    clean_data.columns=clean_data.columns.droplevel()
    # output to static HTML file
    output_file(ticker_name+".html")
    source = ColumnDataSource(data=clean_data)
    p = figure(title=ticker_name, x_axis_type="datetime")
    p.toolbar.active_drag = None
    p.line(x='date', y=ticker_name, source=source)
    script, div = components(p)
    
    #p.line(x='date', y=ticker_name, source=source)
    #show(p)
    
    return render_template('tickerGraph.html',ticker_name=ticker_name,script=script,div=div)
    

if __name__ == '__main__': #if __name__ == '__main__': is basically just Python’s way of saying 
    #“run this code only if I ran it.” as opposed to another script running the code
  app.run(port=5000)

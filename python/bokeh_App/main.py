import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.layouts import column,row
from bokeh.models import ColumnDataSource, BooleanFilter,Div, CDSView, DateRangeSlider, CustomJS,Select,Button ,HoverTool,TextInput
from bokeh.models.widgets import DatePicker

from bokeh.plotting import figure, show, output_notebook,curdoc

import bokeh.plotting
import tradingeconomics as te
from bokeh.models.annotations import Title

##tools for in notebook ui
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

line_dash_styles = [[10, 0], [20, 1], [10, 1], [5, 1]]
output_notebook()
te.login('7w3v74kf0p7m4fb:esc470x5pxsuw5z')



##tools for in notebook ui
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

line_dash_styles = [[10, 0], [20, 1], [10, 1], [5, 1]]
output_notebook()
te.login('7w3v74kf0p7m4fb:esc470x5pxsuw5z')


global p,layout,s2
p = figure(plot_width=1000, plot_height=500, x_axis_type="datetime",tools=TOOLS)

p.xaxis.axis_label = 'Date'  
p.yaxis.axis_label = 'Value'
s1 = Select(title="Select Country", value='New Zealand', options=['New Zealand','mexico','Sweden','Thailand'])
div = Div(width=400, height=p.height, height_policy="fixed")
s2 = Select(title="Select Category", value='', options=[])

source = ColumnDataSource(data={'Date': [], 'y': []})
dt_pckr_strt=DatePicker(title='Select Start Date')

def update_drop(attr,old,new):
    global s2
    country_latest=te.getIndicatorData(country=s1.value, output_type='df')
    s2.options=country_latest.Category.unique().tolist()

def update(attr):
    global p,s2
    p = figure(plot_width=1000, plot_height=500, x_axis_type="datetime",tools=TOOLS)
    p.xaxis.axis_label = 'Date'  
    p.yaxis.axis_label = 'Value'
    layout.children[-1]=p
    try:
        if dt_pckr_strt.value:
            historic_val=te.getHistoricalData(country=[s1.value], output_type='df', indicator=s2.value, initDate=str(dt_pckr_strt.value))
            
        else:
            historic_val=te.getHistoricalData(country=[s1.value], output_type='df', indicator=s2.value)
        historic_val['DateTime']=pd.to_datetime(historic_val['DateTime'],utc=True).dt.date
    except:
        historic_val=pd.DataFrame()
    if not historic_val.empty:
        l=p.line(x=historic_val['DateTime'], y=historic_val['Value'])
        p.add_tools(HoverTool(renderers=[l], tooltips= [

        ("x_label", "@x{%F}"),
        ("y_label", "@y{int}")
        ],formatters={'@x': 'datetime'}))

        p.xaxis.axis_label = 'Date'  
        p.yaxis.axis_label = 'Value'
        div.text =f'Historic Data of <b>{s1.value}</b> for indicator <b>{s2.value}</b>'




def clear_plot(attr):
    global p
    p = figure(plot_width=1000, plot_height=500, x_axis_type="datetime",tools=TOOLS)
    p.xaxis.axis_label = 'Date'  # that enables showing axis even with no initial data
    p.yaxis.axis_label = 'Value'
    layout.children[-1]=p

clear_btn = Button(label="Reset")
clear_btn.on_click(clear_plot)
submit=Button(label="Submit")
s1.on_change("value", update_drop)
submit.on_click(update)
layout=column(s1, s2,dt_pckr_strt,row( submit,clear_btn),div, p)
curdoc().add_root(layout)
curdoc().title = "Historic Data plot"
    
    
    


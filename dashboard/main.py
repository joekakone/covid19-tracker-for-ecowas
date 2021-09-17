#!/usr/bin/env python
# coding: utf-8


import os
import datetime

import pandas as pd
from bokeh.io import curdoc
from bokeh.models import Panel, Tabs

from helpers.data import get_data, get_date
from helpers.plot import bokeh_plot_layout, bokeh_barplot, bokeh_table, bokeh_geoplot


# Local CSV
GEO_DATA = 'dashboard/data/ecowas-gps.csv'

# Set HTML page title
curdoc().title = 'ECOWAS - Covid19 Tracker'

# Load data
print("Donwload data from Github")
# ecowas = pd.read_csv("dashboard/data/2021-09-16-ecowas-covid19.csv")
# update_date = "16-09-2021"
ecowas, update_date = get_data()

print("Read data from ecowas-gps.csv")
ecowas_geo = pd.read_csv(GEO_DATA)
ecowas[['x', 'y']] = ecowas_geo[['x', 'y']]

countries = ecowas['Country_Region']

# Agregated indicators
print("Calculate aggregate KPIs")
confirmed = int(ecowas.Confirmed.sum())
active = "N/A"
recovered = "N/A"
deaths = int(ecowas.Deaths.sum())


print("Add template Variables")
curdoc().template_variables['update_date'] = update_date
curdoc().template_variables['indicator_names'] = ['Confirmed', 'Recovered', 'Active', 'Deaths']
curdoc().template_variables['indicators'] = {
    'Confirmed': {
        'title': 'Confirmed',
        'value': confirmed
        },
    'Recovered': {
        'title': 'Recovered',
        'value': recovered
        },
    'Active': {
        'title': 'Active',
        'value': active
        },
    'Deaths': {
        'title': 'Deaths',
        'value': deaths
        },
}

# Build the graph

# Barplot
p1 = bokeh_barplot(ecowas)
tab1 = Panel(child=p1, title="Compare per country")

# Geoplot
p2 = bokeh_geoplot(ecowas)
tab2 = Panel(child=p2, title="View on Map")

# 
p3 = bokeh_plot_layout(ecowas)
tab3 = Panel(child=p3, title="Explore data")

# Table
p4 = bokeh_table(ecowas)
tab4 = Panel(child=p4, title="Raw data")

p = Tabs(tabs=[tab1, tab2, tab3, tab4], name="p")
curdoc().add_root(p)

print("Launch App")
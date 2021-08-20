#!/usr/bin/env python
# coding: utf-8

"""
    Bokeh Application for Covid19 Tracking in real time
"""

import requests

import pandas as pd
from bokeh.io import curdoc

from helpers.data import get_data
from helpers.plot import bokeh_plot_layout, bokeh_barplot, bokeh_table, bokeh_geoplot

from config import API_URL, GEO_DATA

# Set HTML page title
curdoc().title = 'ECOWAS - Covid19 Tracker'

# Load data
try:
    print("Donwload data from Github")
    ecowas, update_date = get_data()
except Exception as e:
    raise e
    print("Retreive data from API")
    r = requests.get(API_URL).json()
    ecowas, update_date = pd.DataFrame(r["data"]), r["last_update"]

print("Read data from ecowas-gps.csv")
ecowas_geo = pd.read_csv(GEO_DATA)
ecowas[['x', 'y']] = ecowas_geo[['x', 'y']]

countries = ecowas['Country_Region']

# Agregated indicators
print("Calculate aggregate KPIs")
confirmed = int(ecowas.Confirmed.sum())
active = int(ecowas.Active.sum())
recovered = int(ecowas.Recovered.sum())
deaths = int(ecowas.Deaths.sum())

# Define variables for Jinja
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
curdoc().add_root(bokeh_plot_layout(ecowas))

# Barplot
curdoc().add_root(bokeh_barplot(ecowas))

# Geoplot
curdoc().add_root(bokeh_geoplot(ecowas))

# Table
curdoc().add_root(bokeh_table(ecowas))

print("Launch App")

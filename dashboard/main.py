#!/usr/bin/env python
# coding: utf-8


import os
import datetime

import pandas as pd
from bokeh.io import curdoc

from helpers.data import get_data, get_date
from helpers.plot import bokeh_plot_layout, bokeh_barplot, bokeh_table, bokeh_geoplot


def to_update_date(x):
    x = x.split('/')[-1]
    y, m, d = tuple(x.split('-')[:3])

    return '-'.join([d, m, y])


# Local CSV
GEO_DATA = 'dashboard/data/ecowas-gps.csv'

# Set HTML page title
curdoc().title = 'ECOWAS - Covid19 Tracker'

# Load data
print("Donwload data from Github")
ecowas, update_date = get_data()

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

#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from bokeh.layouts import row, column
from bokeh.models import LinearColorMapper
from bokeh.transform import transform


def plot():
    '''function to build the graph'''

    # defaults value for the graph
    default_x_axis = 'sepal_length'
    default_y_axis = 'sepal_width'
    default_color = 'petal_length'
    default_size = 'petal_width'
    
    source = ColumnDataSource(data={'x_axis': iris[default_x_axis],
                                    'y_axis': iris[default_y_axis],
                                    'color': iris[default_color],
                                    'size': iris[default_size]*3.5,
                                    'specie': iris['specie'],
                                    'sepal_length': iris['sepal_length'],
                                    'sepal_width': iris['sepal_width'],
                                    'petal_length': iris['petal_length'],
                                    'petal_width': iris['petal_width'],
                                   })
    
    color_mapper = LinearColorMapper(palette="Viridis256", low=iris[default_color].min(), high=iris[default_color].max())
    
    p = figure(title=default_x_axis+" vs "+default_y_axis, plot_width=700, plot_height=500)
    p.circle(x='x_axis', y='y_axis', size='size', color=transform('color', color_mapper), fill_alpha=0.5, source=source)
    
    p.add_tools(HoverTool(tooltips=[
        ('Specie', '@specie'),
        ('Sepal length', "@sepal_length"),
        ('Sepal width', "@sepal_width"),
        ('Petal length', "@petal_length"),
        ('Petal width', "@petal_width")
        ]))

    # set axis labels
    p.xaxis.axis_label = default_x_axis
    p.yaxis.axis_label = default_y_axis
    
    select_x_axis = Select(title="X-Axis", value=axis[0], options=axis, width=200)
    select_y_axis = Select(title="Y-Axis", value=axis[1], options=axis, width=200)
    select_color = Select(title="Color", value=axis[2], options=axis, width=200)
    select_size = Select(title="Size", value=axis[3], options=axis, width=200)
    
    selects = column(select_x_axis, select_y_axis, select_color, select_size)
    
    def update_x_axis(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['x_axis'] = iris[select_x_axis.value]
        p.xaxis.axis_label = select_x_axis.value
        a = p.title.text.split('vs')
        a[0] = select_x_axis.value
        p.title.text = " vs ".join(a)
    select_x_axis.on_change('value', update_x_axis)
    
    def update_y_axis(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['y_axis'] = iris[select_y_axis.value]
        p.yaxis.axis_label = select_y_axis.value
        a = p.title.text.split('vs')
        a[1] = select_y_axis.value
        p.title.text = " vs ".join(a)
    select_y_axis.on_change('value', update_y_axis)
    
    def update_color(attrname, old, new):
        source.data['color'] = iris[select_color.value]
    select_color.on_change('value', update_color)
    
    def update_size(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['size'] = iris[select_size.value]*3.5
    select_size.on_change('value', update_size)
    
    layout = row(selects, p, name='my_layout')
    
    return layout


# loading data
iris = pd.read_csv('dashboard/data/iris.csv')

# number of features
axis = list(iris.columns[:4])

# DataFrame to ColumnDataSource
source = ColumnDataSource(data=iris)

# build the graph
curdoc().add_root(plot())

# set html page title
curdoc().title = 'Iris Dataset Explorer'

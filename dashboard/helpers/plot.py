# coding : utf-8


from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.resources import INLINE
from bokeh.models import WMTSTileSource, DataTable, TableColumn, NumberFormatter, StringFormatter, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.layouts import row, column
from bokeh.models import LinearColorMapper, NumeralTickFormatter
from bokeh.transform import transform


from .data import get_date


INDICATORS = ['Confirmed', 'Recovered', 'Active', 'Deaths']
COLORS = {
    'Confirmed': 'orange',
    'Recovered': 'green',
    'Active':'red' ,
    'Deaths': 'gray'
    }
ZOOM = 0.2
GEO_ZOOM = 0.005


def bokeh_barplot(data):
    countries = data['Country_Region']
    source = ColumnDataSource(data={'indicator': data[INDICATORS[0]],
                                    'color': [COLORS[INDICATORS[0]]]*len(data),
                                    'Country_Region': data['Country_Region'],
                                    'Confirmed': data['Confirmed'],
                                    'Active': data['Active'],
                                    'Recovered': data['Recovered'],
                                    'Deaths': data['Deaths'],
                                })

    p = figure(title=INDICATORS[0], x_range=countries, plot_width=750, plot_height=500, name='barplot', tools='save')

    p.vbar(x='Country_Region', bottom=0, top='indicator', color='color', source=source, width=0.7)
    
    select_indicator = Select(title='Indicator', value=INDICATORS[0], options=INDICATORS, width=150)

    label = LabelSet(x='Country_Region', y='indicator', x_offset=-15, y_offset=10,
        text="indicator", text_baseline="middle", text_font_size="12px", source=source)
    p.add_layout(label)


    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.yaxis.formatter.use_scientific = False

    p.add_tools(HoverTool(tooltips=[
        ('Country', '@Country_Region'),
        ('Confirmed', "@Confirmed"),
        ('Active', "@Active"),
        ('Recovered', "@Recovered"),
        ('Deaths', "@Deaths")
        ]))

    def update_indictor(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['indicator'] = data[select_indicator.value]
        source.data['color'] = [COLORS[select_indicator.value]]*len(data)
        p.title.text = select_indicator.value
    select_indicator.on_change('value', update_indictor)

    layout = row(p, select_indicator, name='barplot')

    return  layout

def bokeh_geoplot(data):
    x_range = (data['x'].min()-100000, data['x'].max()+1000000)
    y_range = (data['y'].min() ,data['y'].max())
    source = ColumnDataSource(data={'size': data['Confirmed']*GEO_ZOOM,
                                    'Country_Region': data['Country_Region'],
                                    'Confirmed': data['Confirmed'],
                                    'Active': data['Active'],
                                    'Recovered': data['Recovered'],
                                    'Deaths': data['Deaths'],
                                    'x': data['x'],
                                    'y': data['y']
                                })
    p = figure(plot_width=900,
               plot_height=400,
               tools='save',
               x_range=x_range,
               y_range=y_range,
               x_axis_type="mercator",
               y_axis_type="mercator",
               name='geoplot')

    MAP_URL = 'http://a.basemaps.cartocdn.com/rastertiles/voyager/{Z}/{X}/{Y}.png'
    attribution = "Tiles by Carto, under CC BY 3.0. Data by OSM, under ODbL"

    p.add_tile(WMTSTileSource(url=MAP_URL, attribution=attribution))

    p.circle(x='x', y='y', fill_color='red', size='size', fill_alpha=0.3, line_color=None, source=source)
    p.axis.visible = False

    p.add_tools(HoverTool(tooltips=[
        ('Country', '@Country_Region'),
        ('Confirmed', "@Confirmed"),
        ('Active', "@Active"),
        ('Recovered', "@Recovered"),
        ('Deaths', "@Deaths")
        ]))
    return p

def bokeh_plot_layout(data):
    # defaults value for the graph
    default_x_axis = INDICATORS[0]
    default_y_axis = INDICATORS[1]
    default_color = INDICATORS[2]
    default_size = INDICATORS[3]

    source = ColumnDataSource(data={'x_axis': data[default_x_axis],
                                    'y_axis': data[default_y_axis],
                                    'color': data[default_color],
                                    'size': data[default_size]*ZOOM,
                                    'Country_Region': data['Country_Region'],
                                    'Confirmed': data['Confirmed'],
                                    'Active': data['Active'],
                                    'Recovered': data['Recovered'],
                                    'Deaths': data['Deaths'],
                                })

    color_mapper = LinearColorMapper(palette="Viridis256",
                                    low=data[default_color].min(),
                                    high=data[default_color].max())

    p = figure(title=default_x_axis+" vs "+default_y_axis, plot_width=750, plot_height=500, tools='save')
    p.circle(x='x_axis',
            y='y_axis',
            size='size',
            color=transform('color', color_mapper),
            fill_alpha=0.5,
            source=source)

    p.add_tools(HoverTool(tooltips=[
        ('Country', '@Country_Region'),
        ('Confirmed', "@Confirmed"),
        ('Active', "@Active"),
        ('Recovered', "@Recovered"),
        ('Deaths', "@Deaths")
        ]))

    # set axis labels
    p.xaxis.axis_label = default_x_axis
    p.xaxis.formatter.use_scientific = False
    p.yaxis.axis_label = default_y_axis
    p.yaxis.formatter.use_scientific = False

    select_x_axis = Select(title="X-Axis", value=INDICATORS[0], options=INDICATORS, width=150)
    select_y_axis = Select(title="Y-Axis", value=INDICATORS[1], options=INDICATORS, width=150)

    selects = column(select_x_axis, select_y_axis)

    def update_x_axis(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['x_axis'] = data[select_x_axis.value]
        p.xaxis.axis_label = select_x_axis.value
        a = p.title.text.split('vs')
        a[0] = select_x_axis.value
        p.title.text = " vs ".join(a)
    select_x_axis.on_change('value', update_x_axis)

    def update_y_axis(attrname, old, new):
        '''callback function to udpate the x_axis'''
        source.data['y_axis'] = data[select_y_axis.value]
        p.yaxis.axis_label = select_y_axis.value
        a = p.title.text.split('vs')
        a[1] = select_y_axis.value
        p.title.text = " vs ".join(a)
    select_y_axis.on_change('value', update_y_axis)

    layout = row(p, selects, name='layout')

    return layout

def bokeh_table(data):
    source_table = ColumnDataSource(data)

    columns = [
        TableColumn(field='Country_Region', title='Country'),
        TableColumn(field='Confirmed', title='Confirmed',
                    formatter=StringFormatter(text_align='left')),
        TableColumn(field='Active', title='Active',
                    formatter=StringFormatter(text_align='left')),
        TableColumn(field='Recovered', title='Recovered',
                    formatter=StringFormatter(text_align='left')),
        TableColumn(field='Deaths', title='Deaths',
                    formatter=StringFormatter(text_align='left')),
    ]
    data_table = DataTable(source=source_table, columns=columns, width=900, height=420, name='data_table')

    return data_table

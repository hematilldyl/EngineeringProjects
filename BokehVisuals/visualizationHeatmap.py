from math import pi
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)
def Heatmap(path="Heatmap/fault.csv",corTo='Fault'):
    data = pd.read_csv(path,sep=',')
    #set the index by site
    headers =list(data.columns.values)
    data[headers[0]] = data[headers[0]].astype(str)
    data = data.set_index(headers[0])
    data.columns.name = corTo
    
    #get a list object of the index
    sites = list(data.index)
    #get the matrix of fault correlations
    faults = list(data.columns)
    
    # reshape to 1D array or rates with a month and year for each row.
    df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()
    
    #colour palette
    colors = ["#1989bd","#3296c4","#4ca3cb","#66b0d3","#7fbdda","#99cae1", 
              "#b2d7e9","#cce4f0","#e5f1f7"]
    colors=colors[::-1]
    mapper = LinearColorMapper(palette=colors, 
                               low=df.rate.min(), high=df.rate.max())
    
    #get data for plotting the lists
    source = ColumnDataSource(df)
    
    #tools for plot
    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    
    #generate figure, assuming 3 sites. Change as needed.
    p = figure(title="Heatmap of "+corTo+" per "+headers[0],
               x_range=sites, y_range=list(reversed(faults)),
               x_axis_location="above", plot_width=900, plot_height=400,
               tools=TOOLS, toolbar_location='below')
    
    #remove visual features
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    #formatting plot axis and font
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3
    
    #generate the heat map with the list references
    p.rect(x=headers[0], y=corTo, width=1, height=1,
           source=source,
           fill_color={'field': 'rate', 'transform': mapper},
           line_color=None)
    
    #legend beside plot
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                         ticker=BasicTicker(desired_num_ticks=len(df)),
                         formatter=PrintfTickFormatter(format="%.2f"),
                         label_standoff=6, border_line_color=None, location=(0, 0))
    p.add_layout(color_bar, 'right')
    
    #over tool when you hover over the heatmap
    p.select_one(HoverTool).tooltips = [
         (headers[0], '@'+headers[0]),
         ('corr', '@rate'),
    ]
    return p

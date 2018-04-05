from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    BasicTicker,
    PrintfTickFormatter,
    ColorBar,
)

#Import data in the form Site x Fault
data=pd.read_csv('fault.csv')

#set the index by site
data['Site'] = data['Site'].astype(str)
data = data.set_index('Site')
data.columns.name = 'Fault'

#get a list object of the index
sites = list(data.index)
#get the matrix of fault correlations
faults = list(data.columns)

# reshape to 1D array or rates with a month and year for each row.
df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()

#output name of html file
output_file("Heatmap_Example.html")

#colour palette
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1",
          "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=colors, 
                           low=df.rate.min(), high=df.rate.max())

#get data for plotting the lists
source = ColumnDataSource(df)

#tools for plot
TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

#generate figure, assuming 3 sites. Change as needed.
p = figure(title="Heatmap of Faults for {0}, {1}, {2}".format(sites[0], 
           sites[1],sites[2]),
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
p.rect(x="Site", y="Fault", width=1, height=1,
       source=source,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)

#legend beside plot
color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%.2f"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

#over tool when you hover over the heatmap
p.select_one(HoverTool).tooltips = [
     ('site', '@Site'),
     ('corr', '@rate'),
]

#show the plot
show(p)      
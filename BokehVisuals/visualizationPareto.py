from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
import pandas as pd
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
from bokeh.models.ranges import Range1d
from bokeh.models.axes import LinearAxis

def Pareto(data="pareto.xlsx",title="Fault Frequency"):
    
    #import data
    df = pd.read_excel(data)
    headers =list(df.columns.values)
    
    #sort from high to low of counts
    df = df.sort_values(by=headers[1],ascending=False)
    y = df[headers[1]]
    x = df[headers[0]]
    
    #create cSum column
    cSum = []
    total = 0
    for freq in y:
        total=total+freq
        cSum.append((total))
    cSum[:]=(Sum/cSum[len(cSum)-1]*100 for Sum in cSum)
    df['cSum']=cSum
    
    #get the labels and create the dict of data
    headers =list(df.columns.values)
    source = ColumnDataSource(dict(df))
    label = list(x)
    
    #create figure
    p = figure(x_range=label, plot_height=400, toolbar_location=None, 
               title=title,x_axis_label=headers[0],y_axis_label=headers[1],
               tools='hover,save')
    
    #secondary axis
    p.extra_y_ranges={"cSum": Range1d(start=0,end=100)}
    p.add_layout(LinearAxis(y_range_name="cSum", 
                axis_label='Cumulative Percentage'), 'right')
    
    #plots
    p.vbar(x=headers[0], top=headers[1], width=0.9, source=source,
           line_color='white', 
           fill_color=factor_cmap(headers[0],palette=Spectral6, factors=x))
    p.line(x=headers[0],y=headers[2],source=source,color='goldenrod',
           line_width=2.2,y_range_name="cSum")
    
    #formatting
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = int(y.iloc[0])+10
    
    #add hover
    p.select_one(HoverTool).tooltips = [
            (headers[0], '@'+headers[0]),
            (headers[1],'@'+headers[1]),
            ("Cumulative Occurance", '@cSum'+"%"),
    
        ]

    return p

import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource

def BoxPlot(pathData="Boxplot/BoxPlot2.csv",pathTable="Boxplot/BoxPlott.csv",
            boxes=["A","E","R"]):
    
    #list of box titles to plot
    iterable = boxes
    df = pd.read_csv(pathData,sep=',')
    table=pd.read_csv(pathTable,sep=',',na_filter=False)

    table.replace(np.nan," ", regex=True)
    #create dictionary of data
    hold = [boxes[x] for x in range(0,len(boxes))]
    data=dict(table[hold])
    source = ColumnDataSource(data)
    
    #create table
    columnsList = []
    for box in range(0,len(boxes)):
        box = TableColumn(field=boxes[box],
                        title=boxes[box])
        columnsList.append(box)
    columns=columnsList
  
    #table object for the html
    data_table = DataTable(source=source, columns=columns, width=600, height=600)
    
    # Find the quartiles and IQR foor each category
    groups = df.groupby('group')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # find the outliers for each category
    def outliers(group):
        comment = str(group.name)
        return group[(group.score > upper.loc[comment][0]) | 
                     (group.score < lower.loc[comment][0])]['score']
    out = groups.apply(outliers).dropna()
 
    # Prepare outlier data for plotting, we need coordinate for every outlier.
    if not out.empty:
        outx = []
        outy = []
        for comment in iterable:
            comment = str(comment)
            # only add outliers if they exist
            if not out.loc[comment].empty:
                for value in out[comment]:
                    outx.append(comment)
                    outy.append(value)
       
    #create figure with labels of each type
    p = figure(tools="save", title="", x_range=iterable,width=650)
    p.min_border_left = 50
    # If no outliers, shrink lengths of stems to be no longer than the minimums or 
    #maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.score = [min([x,y]) for (x,y) in zip(list(qmax.iloc[:,0]),upper.score) ]
    lower.score = [max([x,y]) for (x,y) in zip(list(qmin.iloc[:,0]),lower.score) ]
    
    # stems
    p.segment(iterable, upper.score, iterable, q3.score, 
              line_width=2, line_color="black")
    p.segment(iterable, lower.score, iterable, q1.score, 
              line_width=2, line_color="black")
    
    # boxes
    p.rect(iterable, (q3.score+q2.score)/2, 0.7, q3.score-q2.score,
        fill_color="#d891ef", line_width=2, line_color="black")
    p.rect(iterable, (q2.score+q1.score)/2, 0.7, q2.score-q1.score,
        fill_color="#dadee5", line_width=2, line_color="black")
    
    # whiskers (almost-0 height rects simpler than segments)
    p.rect(iterable, lower.score, 0.2, 0.01, line_color="black")
    p.rect(iterable, upper.score, 0.2, 0.01, line_color="black")
    
    # outliers
    if not out.empty:
        p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)
    
    #format the background and fonts
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="12pt"


    return data_table, p

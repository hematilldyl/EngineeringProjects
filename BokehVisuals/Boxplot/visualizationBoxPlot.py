import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource
from bokeh.layouts import column

#list of box titles to plot
iterable = ["Air Breather On GO Station","Electrical Component","Replace MCCB1"]
#data already transformed to nx2 by stacking each category together
df = pd.read_csv("BoxPlot2.csv",sep=',')
#orignal data where each column is seperated, could just import this and 
#transform the data into the stacked format too
table = pd.read_csv("BoxPlot.csv", sep=',')

#create dictionary of data
data=dict(table[['Time',"Air Breather On GO Station",
                 "Electrical Component",
                 "Replace MCCB1"]])
source = ColumnDataSource(data)

#create table
columns = [
        TableColumn(field="Air Breather On GO Station", 
                    title="Air Breather On GO Station"),
        TableColumn(field="Electrical Component", 
                    title="Electrical Component"),
        TableColumn(field="Replace MCCB1", 
                    title="Replace MCCB1"),
    ]
#table object for the html
data_table = DataTable(source=source, columns=columns, width=600, height=400)

#name the output file
output_file("BoxPlot_Example.html")

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
    comment = group.name
    return group[(group.score > upper.loc[comment][0]) | 
                 (group.score < lower.loc[comment][0])]['score']
out = groups.apply(outliers).dropna()

# Prepare outlier data for plotting, we need coordinate for every outlier.
outx = []
outy = []
for comment in iterable:
    # only add outliers if they exist
    if not out.loc[comment].empty:
        for value in out[comment]:
            outx.append(comment)
            outy.append(value)

#create figure with labels of each type
p = figure(tools="save", title="", x_range=iterable)

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
    fill_color="#dadee5", line_width=2, line_color="black")
p.rect(iterable, (q2.score+q1.score)/2, 0.7, q2.score-q1.score,
    fill_color="#dadee5", line_width=2, line_color="black")

# whiskers (almost-0 height rects simpler than segments)
p.rect(iterable, lower.score, 0.2, 0.01, line_color="black")
p.rect(iterable, upper.score, 0.2, 0.01, line_color="black")

# outliers
p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

#format the background and fonts
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = "white"
p.grid.grid_line_width = 2
p.xaxis.major_label_text_font_size="12pt"


#output in a column format (table on top, plot on bottom)
a=column(data_table,p)
show(a)
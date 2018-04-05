import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot


#name of output file
output_file("BarPlot_Example.html")

#number of partitions+1 (assuming an input data of two columns)
SITES = 6

#data is in the form of 4*s x 2 where s is the number of sites. The 
#data is split into each individual site in the loop.

table = pd.read_csv("data.csv", sep=',',usecols=[0,1])

#assume labels are the first col (Fault, Scheduled, etc)
labels = list(table.iloc[:4,0])

#personal preference for colours
colour = ['#ff4095','#0cb038','#c6e2ff','#8b668b','#ff7500']
          
#list of sites
sites = ["BV","CC","AM","SJM","SW"]

#begin loop
for i in range(1,SITES):
    
    #extract first site
    data=table.iloc[(i-1)+3*(i-1):4*i,:]
    
    #convert to dictionary data structure
    data=dict(data[['Categories',"Manhours Works"]])
    source = ColumnDataSource(data)
    
    #bar plots
#   _______________________________________________________________________
    
    #figure properties. Set the x values to the labels. Title takes from
    #sites list
    p = figure(x_range=labels,plot_height=350, toolbar_location=None, 
               title="Site: {0}".format(sites[i-1]))
    #vertical bar chart accesses dictionary for x,y data and colour map for 
    #each plot
    p.vbar(x='Categories',top='Manhours Works', width=0.75,source=source,
           color=colour[i-1])



    #create table
#   ________________________________________________________________________
    #generate columns from dictionary of data and relabel in title
    columns = [
        TableColumn(field='Categories', title='Categories'),
        TableColumn(field='Manhours Works', title='Manhours Worked'),
    ]
    #table object for html file
    data_table = DataTable(source=source, columns=columns,
                           width=600, height=400)
    #generate each figure group iteratively (no case switch sadly)
    if i ==1:
        BV = data_table
        p1 = p
    elif i == 2:
        CC = data_table
        p2 = p
    elif i == 3:
        AM = data_table
        p3 = p
    elif i ==4:
        SJM = data_table
        p4 = p
    else:
        SW = data_table
        p5 = p

#grid plot such that BV/p1 is one column        
grid = gridplot([[p1,p2,p3,p4,p5],[BV,CC,AM,SJM,SW]])
show(grid)

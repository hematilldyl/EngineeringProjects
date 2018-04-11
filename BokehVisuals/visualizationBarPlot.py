import pandas as pd
from bokeh.plotting import figure
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource,HoverTool



def BarPlot(pathTable="BarPlot/data.csv", sites = ["BV","CC","AM","SJM","SW"]):
    SITES = len(sites)+1
    
    #data is in the form of 4*s x 2 where s is the number of sites. The 
    #data is split into each individual site in the loop.
    table = pd.read_csv(pathTable, sep=',',usecols=[0,1])
    iteration=int(len(table)/len(sites))
    
    #assume labels are the first col (Fault, Scheduled, etc)
    labels = list(table.iloc[:iteration,0])
    headers =list(table.columns.values)
    
    #personal preference for colours
    colour = ['#ff4095','#0cb038','#c6e2ff','#8b668b','#ff7500']
          
    #begin loop
    t = []
    plot = []
    for i in range(1,SITES):
        
        #extract first site
        data=table.iloc[iteration*(i-1):iteration*i,:]
        print(data)
        #convert to dictionary data structure
        data=dict(data[headers])
        source = ColumnDataSource(data)
        
        #bar plots
#       _______________________________________________________________________
        
        #figure properties. Set the x values to the labels. Title takes from
        #sites list
        p = figure(x_range=labels,plot_height=350, toolbar_location=None,
                   tools = 'hover,save', title="Site: {0}".format(sites[i-1]))
        #vertical bar chart accesses dictionary for x,y data and colour map for 
        #each plot
        p.vbar(x=headers[0],top=headers[1], width=0.75,source=source,
               color=colour[i-1])
    
        p.select_one(HoverTool).tooltips = [
         (headers[0], '@'+headers[0]),
         (headers[1], '@'+headers[1]),
         ]
    
        #create table
#       ________________________________________________________________________
        #generate columns from dictionary of data and relabel in title
        columns = [
            TableColumn(field=headers[0], title=headers[0]),
            TableColumn(field=headers[1], title=headers[1]),
        ]
        #table object for html file
        data_table = DataTable(source=source, columns=columns,
                               width=600, height=150)
        t.append(data_table)
        plot.append(p)


    return t,plot


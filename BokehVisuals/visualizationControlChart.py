import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot



def IMR(data,dtable):

    MR = [abs(data[headers[1]].iloc[i]
          -data[headers[1]].iloc[i-1]) for i in range(1,l)]
    meanI = np.mean(data[headers[1]])
    meanR = np.mean(MR[1:])
    if l<=len(dtable):
        #I plot
        d2 = dtable.iloc[l,1]
        UCL_I = [meanI+3*(meanR/d2)]*l
        LCL_I = [meanI-3*(meanR/d2)]*l
        CL_I = [meanI]*l
        I = [UCL_I,CL_I,LCL_I]
        #MR plot
        d4 = dtable.iloc[l,3]
        UCL_MR = [d4*meanR]*l
        LCL_MR = [0]*l
        CL_MR = [meanR]*l
        MR = [UCL_MR,CL_MR,LCL_MR,MR]
    elif l>len(dtable):
       #I plot
        s = np.std(data[headers[1]])
        sMR = np.std(MR)
        d2 = dtable.iloc[l,1]
        UCL_I = [meanI+3*s]*l
        LCL_I = [meanI-3*s]*l
        CL_I = [meanI]*l
        I = [UCL_I,CL_I,LCL_I]
        #MR plot
        d4 = dtable.iloc[l,3]
        UCL_MR = [sMR*meanR]*l
        LCL_MR = [0]*l
        CL_MR = [meanR]*l
        MR = [UCL_MR,CL_MR,LCL_MR,MR]
    return I,MR
   
def XR(data,dtable):
    
    Xbar = data[headers[1]]
    R = [abs(data[headers[1]].iloc[i]
          -data[headers[1]].iloc[i-1]) for i in range(1,l)]
    meanXbar = np.mean(Xbar)
    meanR = np.mean(R[1:])
    d2 = dtable.iloc[l,1]
    d3 = dtable.iloc[l,2]
    d4 = dtable.iloc[l,3]
    #Xbar
    UCL_Xbar = [meanXbar+3*(meanR/d2)]*l
    LCL_Xbar = [meanXbar-3*(meanR/d2)]*l
    CL_Xbar = [meanXbar]*l
    
    #R
    UCL_R = [d4*meanR]*l
    LCL_R = [d3*meanR]*l
    CL_R = [meanR]*l
    
    Xbar = [UCL_Xbar,CL_Xbar,LCL_Xbar]
    R = [UCL_R,CL_R,LCL_R,R]
    
    return Xbar,R

def PNP(data):
    p = (data[headers[2]]/data[headers[1]])
    N = np.sum(data[headers[1]])
    n = np.sum(data[headers[2]])
   
    meanP = n/N
    meanN = np.mean(data[headers[1]])

    #P
    UCL_P = [meanP+3*(np.sqrt((meanP*(1-meanP))/meanN))]*l
    CL_P = [meanP]*l
    LCL_P = [meanP-3*(np.sqrt((meanP*(1-meanP))/meanN))]*l
    
    return [UCL_P,CL_P,LCL_P,p]

def plot(I,MR,title,xlabel,ylabel,ylabel2):
    
    fig1 = figure(title=title[0],plot_width=1000,tools='hover,save',
                  toolbar_location=None,x_axis_type='datetime')
    fig1.border_fill_color = "whitesmoke"
    fig1.line(x,I[0],color="red",legend="UCL")
    fig1.line(x,I[1],color="red",legend='CL')
    fig1.line(x,I[2],color="red",legend='LCL')
    fig1.line(x,data[headers[1]],color="blue",legend='Data')
    fig1.circle(x,data[headers[1]],fill_color="blue")
    
    fig1.yaxis.axis_label = ylabel2
    fig1.yaxis.major_label_orientation = "vertical"
    fig1.xaxis.axis_label = xlabel
    
    fig1.legend.location="bottom_right"
    
    fig2 = figure(title=title[1],plot_width=1000,tools='hover,save',
                  toolbar_location=None,x_axis_type='datetime')
    fig2.border_fill_color = "whitesmoke"
    fig2.line(x,MR[0],color="red")
    fig2.line(x,MR[1],color="red")
    fig2.line(x,MR[2],color="red")
    fig2.line(x[1:],MR[3][1:],color="blue")
    fig2.circle(x[1:],MR[3][1:],fill_color="blue")
    fig2.yaxis.axis_label = ylabel
    fig2.yaxis.major_label_orientation = "vertical"
    fig2.xaxis.axis_label = xlabel
    
    return fig1,fig2

CCType = input("Which Control Chart?\n")
data = input("What is the path to your data?\n")

data = pd.read_excel(data)

dtable = pd.read_excel("dtable.xlsx")
headers=list(data.columns.values)
x = data[headers[0]]
l = len(data)

if CCType == "IMR":
    xlabel = "Time"
    ylabel = "Moving Range of " +headers[1]
    title = ["I","MR"]
    ylabel2 = headers[1]
    I,MR=IMR(data,dtable)
    fig1,fig2 = plot(I,MR,title,xlabel,ylabel,ylabel2)
    p=gridplot([[fig1],[fig2]])
    
if CCType == "XR":
    xlabel = "Sample"
    ylabel = "Sample Mean"
    title = ["Xbar","R"]
    Xbar,R=XR(data,dtable)
    fig1,fig2 = plot(Xbar,R,title,xlabel,ylabel,ylabel)
    p=gridplot([[fig1],[fig2]])

if CCType == "PNP":
    xlabel = "Time"
    ylabel = "Proportion with Defects"
    P = PNP(data)
    
    fig1 = figure(title="P",plot_width=1000,tools='hover,save',
                  toolbar_location=None)
    fig1.border_fill_color = "whitesmoke"
    fig1.line(x,P[0],color="red",legend="UCL")
    fig1.line(x,P[1],color="red",legend='CL')
    fig1.line(x,P[2],color="red",legend='LCL')
    fig1.line(x,P[3],color="blue",legend='Data')
    fig1.circle(x,P[3],color="blue")
    
    fig1.yaxis.axis_label = ylabel
    fig1.yaxis.major_label_orientation = "vertical"
    fig1.xaxis.axis_label = xlabel
    p=gridplot([[fig1]])



show(p)


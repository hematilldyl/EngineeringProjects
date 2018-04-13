import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from scipy.stats import norm

def NormPlot(df,headers):
    
    #calculate percentiles
    p = [(i-0.5)/len(df) for i in range(1,len(df)+1)]
    #calculate Z value
    z = [norm.ppf(p) for p in p]
    #compute linear regression
    regression = np.polyfit(df[headers[1]], z, 1)
    #get values of the regression for plotting
    regressionLine = [np.polyval(regression,x) for x in df[headers[1]]]
    
    return regression,z,regressionLine


def WeibullPlot(df,headers):
    
    #calculate median rank
    MR = [(i-0.3)/(len(df)+0.4) for i in range(1,len(df)+1)]
    #get the y values for plotting
    y_trans = [np.log(np.log(1/(1-MR))) for MR in MR]
    #get the x values for plotting
    x_trans = np.log(df[headers[0]])
    
    #linear regression for plot
    regression = np.polyfit(x_trans,y_trans, 1)
    #shape and character parameters
    beta = regression[1]
    alpha = np.exp(-np.abs(regression[0]/beta))
    params = [alpha,beta]
    
    #coordinates
    trans = [x_trans,y_trans]
    
    #regression values for plotting
    regressionLine = [np.polyval(regression,x) for x in x_trans]
    
    return trans,params,regressionLine,regression

def ExponentialPlot(df,headers):
    
    #percentiles
    p = [(i-0.5)/len(df) for i in range(1,len(df)+1)]
    #calculate y for plot
    y_trans = [-np.log(1-p) for p in p]
    #linear regression
    regression = np.polyfit(df[headers[1]],y_trans, 1)
    #calculate regression values for plotting
    regressionLine = [np.polyval(regression,x) for x in df[headers[1]]]
    
    return regression,y_trans,regressionLine
    
def LognormalPlot(df,headers):
    
    #same as normal plot    
    p = [(i-0.5)/len(df) for i in range(1,len(df)+1)]
    z = [norm.ppf(p) for p in p]
    x_trans = np.log(df[headers[1]])
    regression = np.polyfit(x_trans, z, 1)
    regressionLine = [np.polyval(regression,x) for x in x_trans]
    
    return regression,[x_trans,z],regressionLine
    

def main():
    
    #read data
    df = pd.read_excel("pdist.xlsx")
    #get data labels
    headers=list(df.columns.values)
    #sort the values
    df = df.sort_values(by=headers[1])
    print(df)
    #get plot values
    ncoef,z,nreg = NormPlot(df,headers)
    trans,params,wreg,wcoef = WeibullPlot(df,headers)
    print(params)
    ecoef,yexp,ereg = ExponentialPlot(df,headers)
    lcoef,lcord,lreg = LognormalPlot(df,headers)
    
    output_file("probability_plot.html")
    
    #plot the pp
#_____Weibull_________________________________________________________________
    weibull = figure( plot_height=400, toolbar_location=None, 
               background_fill_color="#E8DDCB",tools='hover,save',
               title="Weibull Probability Plot with y= "+str(wcoef[1])+"x + "+str(wcoef[0]))
    
    weibull.circle(x=trans[0], y=trans[1], line_color="#3288bd", fill_color="white", 
             line_width=3)
    weibull.line(x=trans[0],y=wreg,line_color="#662946")
                 
#_____Normal_________________________________________________________________
    normal = figure( plot_height=400, toolbar_location=None, 
               background_fill_color="#E8DDCB",tools='hover,save',
               title="Normal Probability Plot with y= "+str(ncoef[1])+"x + "+str(ncoef[0]))
    normal.circle(x=df[headers[1]], y=z, line_color="#3288bd", fill_color="white", 
             line_width=3)
    normal.line(x=df[headers[1]],y=nreg,line_color="#662946") 
                
#_____Exponential_________________________________________________________________
    exponential = figure( plot_height=400, toolbar_location=None, 
               background_fill_color="#E8DDCB",tools='hover,save',
               title="Expontential Probability Plot with y= "+str(ecoef[1])+"x + "+str(ecoef[0]))
    exponential.circle(x=df[headers[1]], y=yexp, line_color="#3288bd", fill_color="white", 
             line_width=3)
    exponential.line(x=df[headers[1]],y=ereg,line_color="#662946") 
                     
#_____Lognormal_________________________________________________________________
    lognormal = figure( plot_height=400, toolbar_location=None, 
               background_fill_color="#E8DDCB",tools='hover,save',
               title="Lognormal Probability Plot with y= "+str(lcoef[1])+"x + "+str(lcoef[0]))
    lognormal.circle(x=lcord[0], y=lcord[1], line_color="#3288bd", fill_color="white", 
             line_width=3)
    lognormal.line(x=lcord[0],y=lreg,line_color="#662946") 
                     
                     
    #arrange in 2x2 html                
    grid = gridplot([[normal,lognormal],[weibull,exponential]])                
    show(grid) 
                
if __name__ == '__main__':
    main()
    
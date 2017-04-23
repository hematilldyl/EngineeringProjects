import matplotlib.pyplot as plt
import geopandas as gpd
from geopandas.plotting import plot_multipolygon

#ArcGIS
canada = gpd.GeoDataFrame.from_file('Canada.shp')

#print the table
print(canada)

#primary fuel source
canada['FuelType'] = 'Hold'
canada.iloc[0,3] = 'Hydro'
canada.iloc[1,3] = 'Coal'
canada.iloc[2,3] = 'Coal'
canada.iloc[3,3] = 'Coal'
canada.iloc[4,3] = 'Oil'
canada.iloc[5,3] = 'Gas'
canada.iloc[6,3] = 'Oil'
canada.iloc[7,3] = 'Wind'
canada.iloc[8,3] = 'Hydro'
canada.iloc[9,3] = 'Oil'
canada.iloc[10,3] = 'Nuclear'
canada.iloc[11,3] = 'Oil'
canada.iloc[12,3] = 'Hydro'

#color code it!
canada['Colour'] = 'Hold'
for i in range(13):
    if(canada.iloc[i,3] == 'Hydro'):
        canada.iloc[i,4] = '#7cf6ff'
    elif(canada.iloc[i,3] == 'Coal'):
        canada.iloc[i,4] = '#51bc6c'
    elif(canada.iloc[i,3] == 'Oil'):
        canada.iloc[i,4] = '#774b14'
    elif(canada.iloc[i,3] == 'Wind'):
        canada.iloc[i,4] = '#f9ee4f'
    elif(canada.iloc[i,3] == 'Nuclear'):
        canada.iloc[i,4] = '#d74ff9'
    elif(canada.iloc[i,3] == 'Gas'):
        canada.iloc[i,4] = '#bc5151'
 
#begin the plot       
canada_plot = canada.plot()
for p_ny in canada_plot.patches:
    p_ny.set_color("#111111")
    p_ny.set_alpha(0.6)
for i in range(13):
    province = canada[canada.NAME == canada.iloc[i,0]]
    plot_multipolygon(canada_plot, province.geometry.iloc[0], facecolor=canada.iloc[i,4], edgecolor='none')
  
plt.show()



#Energy Stat Source
#http://energybc.ca/largehydro.html
#http://www.iedm.org/files/note-energy-quebec13.pdf
#http://www.nspower.ca/en/home/about-us/how-we-make-electricity
#http://www.energy.alberta.ca/electricity/682.asp
#http://www.saskpower.com/our-power-future/our-electricity/
#http://www.nr.gov.nl.ca/nr/energy/electricity/
#https://www.nrcan.gc.ca/sites/www.nrcan.gc.ca/files/energy/files/pdf/EnergyFactBook2015-Eng_Web.pdf
#http://resourceplan.yukonenergy.ca/facts/
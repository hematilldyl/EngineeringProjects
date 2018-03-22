
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#extract the data
FuelData = pd.read_csv('H:\Downloads\Book1.csv',sep=',', header=0, nrows=26)

#print the table
print(FuelData)

#Extract data by category
Nuclear = FuelData.iloc[:,1]
Hydro = FuelData.iloc[:,2]
Gas = FuelData.iloc[:,3]
Biofuel = FuelData.iloc[:,4]
Solar3 = FuelData.iloc[:,5]
Wind = FuelData.iloc[:,6]
TotalGWh = FuelData.iloc[:,7]
FuelTypes=[Nuclear,Hydro,Gas,Biofuel,Solar3,Wind,TotalGWh]
FuelNames=['Nuclear','Hydro','Gas','Biofuel','Solar3','Wind','TotalGWh']

#begin the plot details
fig = plt.figure()
fig.add_axes()
ax = fig.add_subplot(111)
x=np.linspace(1,26,num=26)
my_xticks = FuelData.iloc[:,8]
ax.set_xticks(x)
ax.set_xticklabels(my_xticks,rotation=65,fontsize=8)
ax.xaxis.set_ticks(np.arange(1, 26, 3))
ax.set(title='Monthly Energy Grid Output by Fuel Type (Grid-Connected)',
        ylabel ='GWh Generated',
        xlabel ='Month')   
box = ax.get_position()
ax.set_position([box.x0,box.y0,box.width*0.83,box.height])

#plot
for i in range(7):
    if(FuelNames[i] == 'TotalGWh'):
        ax.plot(x,FuelTypes[i], label = FuelNames[i], c='k')
    else:
        ax.plot(x,FuelTypes[i], label = FuelNames[i])    
ax.legend(loc='center left', bbox_to_anchor=(1,0.5))

plt.show() 

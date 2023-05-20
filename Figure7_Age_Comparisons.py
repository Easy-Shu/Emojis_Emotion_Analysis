# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:43:51 2019

@author: Peter_Zhang
"""
#from scipy.interpolate import spline
from scipy.interpolate import make_interp_spline
import math
import re  
import os
import pandas as pd
import numpy as np
from plotnine import *
#from plotnine.data import *
import matplotlib.pyplot as plt 
import scipy.stats as stats
#import skmisc
plt.rcParams['font.sans-serif']=['New Time Romans'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=15

#---------------------------------------------------------------------------------------
N_Sample=10
file = open('Emotions.csv')
mydata=pd.read_csv(file,encoding = "utf-8")
file.close()
mydata['Group']=np.repeat(np.arange(0,N_Sample,1),60)

mydata_Age=mydata[mydata['Age']<=4].groupby(['Group','Age']).mean().sort_values('Embarrassed')
Colnames=mydata.columns.values.tolist()[0:13]
Colnames=mydata[mydata['Age']<=4].groupby(['Group','Age']).mean().max()[Colnames].sort_values(ascending=False).index

width=0.37

fig =plt.figure(figsize=(16,7), dpi=100)
plt.xlim(0.3,len(Colnames)+1-0.3)
plt.ylim(1,7)

N=int(len(mydata_Age)/3)

for j in range(0, len(Colnames)):
    
    plt.axvspan(xmin=j+1-width-0.025, xmax=j+1+width+0.025,facecolor='#E6E6E6',zorder=0)
   
    
    x0=np.repeat(j+1-width,N)
    y0=mydata_Age.loc[(slice(None),2),Colnames[j]]
    plt.scatter(x0,y0,marker='o',s=25,c='#40B3EC',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
    
    x1=np.repeat(j+1,N)
    y1=mydata_Age.loc[(slice(None),3),Colnames[j]]
    plt.scatter(x1,y1,marker='o',s=25,c='#ED3221',linewidths=0.5,edgecolors='k',zorder=2,label='25~30')
    
           
    x2=np.repeat(j+1+width,N)
    y2=mydata_Age.loc[(slice(None),4),Colnames[j]]
    plt.scatter(x2,y2,marker='o',s=25,c='#7DC234',linewidths=0.5,edgecolors='k',zorder=2,label='30~40')
    
    #print(y0)            
                 
    plt.axvline(x=j+1-width,ymin=(np.min(y0)-1)/6,ymax=(np.max(y0)-1)/6,
                color='gray',linewidth =1, zorder=0)
    plt.axvline(x=j+1,ymin=(np.min(y1)-1)/6,ymax=(np.max(y1)-1)/6,
                color='gray', linewidth =1,zorder=0)
    plt.axvline(x=j+1+width,ymin=(np.min(y2)-1)/6,ymax=(np.max(y2)-1)/6,
                color='gray',linewidth =1, zorder=0)
# =============================================================================
    for i in range(0,N):
         x0=j+1-width
         y0=mydata_Age.loc[(i,2),Colnames[j]]
         x1=j+1
         y1=mydata_Age.loc[(i,3),Colnames[j]]
         x2=j+1+width
         y2=mydata_Age.loc[(i,4),Colnames[j]]
         #x_new1,y_new1=spline_bezier(x0,y0,x1,y1)
         #x_new2,y_new2=spline_bezier(x1,y1,x2,y2)
         if (y0>y1 and y0>y2):
             plt.scatter(x0,y0,marker='o',s=85,c='#40B3EC',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
   
             #plt.plot(x_new1, y_new1,color='#40B3EC',linewidth=0.5,zorder=1)
             #plt.plot(x_new2, y_new2,color='#40B3EC',linewidth=0.5,zorder=1)
         elif (y1>y0 and y1>y2):
             plt.scatter(x1,y1,marker='o',s=85,c='#ED3221',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
   
             #plt.plot(x_new1, y_new1,color='#ED3221',linewidth=0.5,zorder=1)
             #plt.plot(x_new2, y_new2,color='#ED3221',linewidth=0.5,zorder=1)
         else:
             plt.scatter(x2,y2,marker='o',s=85,c='#7DC234',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
   
             #plt.plot(x_new1, y_new1,color='#7DC234',linewidth=0.5,zorder=1)
             #plt.plot(x_new2, y_new2,color='#7DC234',linewidth=0.5,zorder=1)
 
plt.xticks(ticks=range(1, len(Colnames)+1),labels=Colnames,
           rotation=0,fontsize=12)  
plt.xlabel('Emotions',fontsize=15)
plt.ylabel('vlaue',fontsize=15) 

ax = plt.gca()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:3],labels=labels[0:3], 
loc='upper right',fontsize=15,
edgecolor='none',facecolor='none',title='Group')


plt.show()
fig.savefig('Figure7_Age_Comparisons.pdf')
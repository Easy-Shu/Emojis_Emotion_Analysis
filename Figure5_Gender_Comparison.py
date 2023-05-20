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

# 插值法，50表示插值个数，个数>=实际数据个数，一般来说差值个数越多，曲线越平滑
def spline_bezier(x0=0,y0=0,x1=1,y1=1):
    x = [x0,x0+(x1-x0)*0.2,x0+(x1-x0)*0.8,x1]
    y = [y0,y0+(y1-y0)*0.1,y0+(y1-y0)*0.9,y1]#[0,0.1,0.9,1]

    x_new = np.linspace(min(x),max(x),50) 
    y_new = make_interp_spline(x, y)(x_new)
    #plt.plot(x_new, y_new)
    #plt.show()
    return x_new,y_new

#---------------------------------------------------------------------------------------
N_Sample=10
file = open('Emotions.csv')
mydata=pd.read_csv(file,encoding = "utf-8")
file.close()
mydata['Group']=np.repeat(np.arange(0,N_Sample,1),60)

Colnames=mydata.columns.values.tolist()[0:13]
Colnames=mydata.groupby(['Group','Gender']).mean().max()[Colnames].sort_values(ascending=False).index
mydata_Gender=mydata.groupby(['Group','Gender']).mean().sort_values('Embarrassed')

width=0.37

fig =plt.figure(figsize=(16,7), dpi=100)
plt.xlim(0.3,len(Colnames)+1-0.3)
plt.ylim(1,7)
N=int(len(mydata_Gender)/2)
for j in range(0, len(Colnames)):
    
    plt.axvspan(xmin=j+1-width-0.025, xmax=j+1+width+0.025,facecolor='#E6E6E6',zorder=0)
    
    x0=np.repeat(j+1-width,N)
    y0=mydata_Gender.loc[(slice(None),2),Colnames[j]]
    plt.scatter(x0,y0,marker='o',s=25,c='#40B3EC',linewidths=0.5,edgecolors='k',zorder=2,label='Female')
    
    x1=np.repeat(j+1+width,N)
    y1=mydata_Gender.loc[(slice(None),1),Colnames[j]]
    plt.scatter(x1,y1,marker='o',s=25,c='#ED3221',linewidths=0.5,edgecolors='k',zorder=2,label='Male')
    
    plt.axvline(x=j+1-width,ymin=(np.min(y0)-1)/6,ymax=(np.max(y0)-1)/6,
                color='gray',linewidth =1, zorder=0)
    plt.axvline(x=j+1+width,ymin=(np.min(y1)-1)/6,ymax=(np.max(y1)-1)/6,
                color='gray', linewidth =1,zorder=0)
    
    for i in range(0,N):
        x0=j+1-width
        y0=mydata_Gender.loc[(i,2),Colnames[j]]
        x1=j+1+width
        y1=mydata_Gender.loc[(i,1),Colnames[j]]
        x_new,y_new=spline_bezier(x0,y0,x1,y1)
        if (y0>y1):
            plt.scatter(x0,y0,marker='o',s=85,c='#40B3EC',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
   
            plt.plot(x_new, y_new,color='#40B3EC',linewidth=0.75,zorder=1)
        else:
            plt.scatter(x1,y1,marker='o',s=85,c='#ED3221',linewidths=0.5,edgecolors='k',zorder=2,label='18~25')
   
            plt.plot(x_new, y_new,color='#ED3221',linewidth=0.75,zorder=1)
            
plt.xticks(ticks=range(1, len(Colnames)+1),labels=Colnames,
           rotation=0,fontsize=12)  
plt.xlabel('Emotions',fontsize=15)
plt.ylabel('vlaue',fontsize=15) 

ax = plt.gca()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:2],labels=labels[0:2], 
loc='upper right',fontsize=15,
edgecolor='none',facecolor='none',title='Group')


plt.show()
fig.savefig('Figure5_Gender_Comparison.pdf')

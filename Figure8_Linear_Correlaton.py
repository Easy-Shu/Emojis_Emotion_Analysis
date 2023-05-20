# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 22:43:51 2019

@author: Peter_Zhang
"""
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
from pandas.api.types import CategoricalDtype

plt.rcParams['font.sans-serif']=['New Time Romans'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

N_Sample=10
file = open('Emotions.csv')
mydata=pd.read_csv(file,encoding = "utf-8")
file.close()
mydata['Group']=np.repeat(np.arange(0,N_Sample,1),60)


Colnames=mydata.columns.values.tolist()[0:13]

mydata_group=mydata.groupby(['Group']).mean().sort_values('Embarrassed')
#---------------------------------------------------------------------------
df_data = pd.DataFrame(columns=['x','y','Group'])
Sub_data = pd.DataFrame(columns=['x','y','Group'])
list_corr=[]
for i in range(1,len(Colnames)):
    Sub_data['x']=mydata_group[Colnames[i]]
    Sub_data['y']=mydata_group[Colnames[0]]
    Sub_data['Group']=np.repeat(Colnames[i],len(Sub_data))
    
    list_corr.append('R: '+str(np.round(Sub_data[['x','y']].corr().iloc[0,1],2)))
    df_data=df_data.append(Sub_data)

df_text=pd.DataFrame(dict(corr=list_corr,Group=Colnames[1:],
                          x=np.repeat(4,len(list_corr)),
                          y=np.repeat(2,len(list_corr))))
df_text=df_text.sort_values('corr',ascending=False).reset_index()  

cat_type = CategoricalDtype(categories=df_text['Group'], ordered=True)
df_text['Group']=df_text['Group'].astype(cat_type)  
df_data['Group']=df_data['Group'].astype(cat_type)  

base_plot=(ggplot(df_data, aes(x = 'x', y = 'y', group= 'Group')) 
#其气泡的颜色填充由Class映射，大小由age映射
+geom_point(colour="k",alpha=1,size=5,shape='o',fill='gray') 
#设置气泡类型为空心的圆圈，边框颜色为黑色，填充颜色透明度为0.7
#+scale_fill_manual(values=["#FC4E07","#00AFBB",  "#E7B800"])
+stat_smooth(aes(fill= 'Group'),method='glm',se=True,alpha=0.6)   
+geom_text(aes(x='x',y='y',label='corr'),df_text,size=18)
+ scale_fill_hue(s = 0.90, l = 0.65, h=0.0417,color_space='husl')                       
+facet_wrap( '~ Group',nrow=2,scales='fixed')  #类别Class为列变量
+ylab('Embarrassment')
+xlab('Emotions')
+theme_matplotlib()
+theme(
    #text=element_text(size=15,face="plain",color="black"),
    axis_title=element_text(size=18,face="plain",color="black"),
    axis_text = element_text(size=16,face="plain",color="black"),
    strip_text=element_text(size=18,face="plain",color="black"),
    strip_background=element_rect(colour="black"),
    #legend_position='none',
    legend_position = 'none',
    figure_size = (15, 5),
    dpi = 50
))
print(base_plot)
base_plot.save('Figure8_Linear_Correlaton.pdf') 

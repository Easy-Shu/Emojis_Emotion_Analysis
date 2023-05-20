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

#----------------------------------------------------------------------------

df_corr=mydata_group[df_text['Group']].corr().reset_index()
df_corr=pd.melt(df_corr,id_vars='index')
df_corr['value']=np.round(df_corr['value'],2)

cat_type = CategoricalDtype(categories=df_text['Group'], ordered=True)
df_corr['index']=df_corr['index'].astype(cat_type)  
df_corr['variable']=df_corr['variable'].astype(cat_type)  


base_plot=(ggplot(df_corr, aes(x = 'index', y = 'variable', fill = 'value',label='value')) 
+ geom_tile(colour="black") 
+xlab('Emotions')
+ylab('Emotions')
+geom_text(aes(label='value'),size=9,colour="white")
+coord_equal()
+scale_fill_cmap(title="R",name="RdYlBu_r")
+guides(fill=guide_colorbar(title='R'))
+theme_matplotlib()
#+xlim(-0.5,42.5)
+theme(
    #text=element_text(size=15,face="plain",color="black"),
    axis_title=element_text(size=13,face="plain",color="black"),
    axis_text = element_text(size=12,face="plain",color="black"),
    axis_text_x=element_text(rotation=90),
    legend_title = element_text(size=15,face="plain",color="black"),
    legend_text= element_text(size=14,face="plain",color="black"),
    #plot_margin=0,
    #legend_position='none',
    #legend_position = (0,0),
    figure_size = (6, 6),
    dpi = 70
))
print(base_plot)
base_plot.save('Figure9_Emotions_Correlaton.pdf') 

# #-----------------------------------------------------------------------------------------------
# from sklearn.linear_model import LassoCV
# lasso_alphas=np.logspace(-3,0,100,base=10)
# lcv=LassoCV(alphas=lasso_alphas,cv=10,max_iter=10000)
# lcv.fit(mydata_group[df_text['Group']].values,mydata_group['Embarrassed'].values)
# print('the best alpha is {}'.format(lcv.alpha_))
# print('the r-square is {}'.format(lcv.score(mydata_group[df_text['Group']].values,
#       mydata_group['Embarrassed'].values)))
# print(lcv.coef_)
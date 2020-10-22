#!/bin/python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['font.family'] = 'sans-serif'

fig, ax1 = plt.subplots(figsize=(16,6))
   
#y = np.loadtxt('pip_138R_337E_noh_norm.txt')
#filenames = ['pip_138R_337E_noh_norm_WT_control.txt','pip_138R_337E_noh_norm_pD58_control.txt','pip_138R_337E_noh_norm.txt']

#filenames = ['pip_noh_norm_WT_control.txt','pip_noh_norm_R164S_65_213_control.txt','pip_WT_R164S_65_213_noh.txt']
#colors = ['red','blue','green']
#labels = ['WT vs WT','R164S vs R164S','WT vs R164S']

#filenames = ['pip_WT_R164S_65_213_50.txt','pip_WT_R164G_65_213_50.txt']
#colors = ['red','blue']
#labels = ['WT vs R164S','WT vs R164G']




for filename, color, label in zip(filenames,colors,labels):
    y = np.loadtxt(filename)
    y /= np.sum(y)
    N = len(y)
#    ymin = np.amin(y)
#    ymax = np.amax(y)
#    if ymax > 0.01:
#        ymax = 0.01
    x = np.arange(N)
    ax1.plot(x,np.log(y),linestyle='-',color=color,label=label)

#logdN = np.log(1./N)
#ax1.plot([0,1500],[logdN,logdN],linestyle='--',color='grey',label='1/N')

ax1.set_xticks(np.arange(0,3001,200))
xml = MultipleLocator(50)
ax1.xaxis.set_minor_locator(xml)

ax1.set_yticks(np.arange(-14,1,1))
yml = MultipleLocator(0.5)
ax1.yaxis.set_minor_locator(yml)

ax1.set_xlabel('filtrations',fontsize=18)
ax1.set_ylabel('log(PIP)',fontsize=18)
ax1.tick_params(axis='y',labelsize=14)
ax1.tick_params(axis='x',labelsize=14)

ax1.set_xlim(0,len(y))
ax1.set_ylim(-11,0)

#ax1.set_yticks(np.arange(-0.5,1.6,0.5))
#yml = MultipleLocator(0.1)
#ax1.set_ylim(-0.5,1.5)

ax1.legend(loc='upper center',fontsize=16)

plt.tight_layout()
plt.savefig('pip_65_213_WT_50.pdf')
plt.show()
plt.close()

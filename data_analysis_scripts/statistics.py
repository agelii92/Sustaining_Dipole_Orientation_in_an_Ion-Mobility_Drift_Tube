import numpy as np
import csv
import math
import MDAnalysis as mda
import os
from matplotlib import pyplot as plt
from functions import *
from statistics import mean
from units import *

def makeplot_temperature_time():
    """Plot and compare the average protein time dependance at times dt, using RUN number of repeated runs for statistics, with the chosen parameters E,T,n"""

    RUN     =    ['1','2','3','4','5']
    E       =    '0.4'
    T       =    '250'
    n       =   ['20','50','100','200']
    dt       =  [50, 100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950]
    data = []
    error = []
    gdata=[]
    for N in n:
        temp = [temperature(N,T,E,run)[1] for run in RUN]
        Tdata = [mean([mean(j[0:5]) for j in temp])]+[mean([mean(j[i-10:i+10]) for j in temp]) for i in dt]+[mean([mean(j[995:1000]) for j in temp])]
        Terror = [np.std([mean(j[0:5]) for j in temp])]+[np.std([mean(j[i-10:i+10]) for j in temp]) for i in dt]+[np.std([mean(j[995:1000]) for j in temp])]
        data.append(Tdata)
        error.append(Terror)
    ts = [0]+dt+[1000]
    t = [i/100 for i in ts]
    fig,ax =plt.subplots()
    for i in list(range(len(data))):
        plt.errorbar(t,data[i],yerr=Terror,label='N = '+str(n[i]),capsize=3)
    plt.plot(t,[float(T) for i in t],'--',label='Gas temp.')
    plt.legend()
    ax.set_xlabel('t [ns]',fontsize=14)
    ax.set_ylabel('Temperature [K]',fontsize=14)
    plt.show()

def makeplot_orientation():
    """
    function to plot the statistic behaviour of Theta as a function of E
    """
    RUN =   ['1','2','3','4','5']
    e   =   ['0.1','0.2','0.3','0.4','0.5']
    t   =   ['350']
    n   =   ['20','50','100','200']
    data    =    [[[mean([mean(orientation(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]
    error   =    [[[np.std([mean(orientation(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]
    fig,ax=plt.subplots()

    for Tdata in data:
             
        for i in list(range(len(Tdata))):
            plt.errorbar(e,Tdata[i],yerr=error[0][i],label='N = '+n[i]+' Ar',capsize=3)
        plt.xlabel('E [V/nm]',fontsize=14)
        plt.ylabel(r'$\overline{\Theta}$',fontsize=14)
        plt.title('T='+t[0]+' K')
        plt.legend()
        plt.show()
        plt.clf()

def makeplot_orientation2():
    """
    function to plot the statistic behaviour of Theta as a
    """
    RUN =   ['1','2','3','4','5']
    e   =   ['0.1','0.2','0.3','0.4','0.5']
    n   =   ['200']
    t   =   ['250','300','350']
    data    =    [[[mean([mean(orientation(N,T,E,i)[1]) for i in RUN]) for E in e] for T in t] for N in n]
    error   =    [[[np.std([mean(orientation(N,T,E,i)[1]) for i in RUN]) for E in e] for T in t] for N in n]
    fig,ax=plt.subplots()
    print(data)
    for Tdata in data:
             
        for i in list(range(len(Tdata))):
            plt.errorbar(e,Tdata[i],yerr=error[0][i],label='T = '+t[i]+' K',capsize=3)
        plt.xlabel('E [V/nm]',fontsize=14)
        plt.ylabel(r'$\overline{\Theta}$',fontsize=14)
        plt.title('N='+n[0]+' Ar')
        plt.legend()
        plt.show()
        plt.clf()
    

def makeplot_temperature():
    """
    function to plot the statistic behaviour of Temperature
    """
    RUN =   ['1','2','3','4','5']
    e   =   ['0.1','0.2','0.3','0.4','0.5']
    t   =   ['350']
    n   =   ['50','100','200']
    data    =    [[[mean([mean(temperature(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]

    error   =    [[[np.std([mean(temperature(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]

    for Tdata in data:
        for i in list(range(len(Tdata))):
            plt.errorbar(e,Tdata[i],yerr=error[0][i],label='N = '+n[i]+' Ar',capsize=3)
        plt.plot(e,[float(t[0]) for i in e],'--',label='Gas temperature')

        plt.xlabel('E [V/nm]',fontsize=14)
        plt.ylabel(r'$\overline{T}_f$',fontsize=14)
        plt.title('Gas temperature T='+t[0]+' K')
        plt.legend()
        plt.show()
        plt.clf()

def makeplot_RMSD():
    """
    function to plot the statistic behaviour of RMSD
    """
    RUN =   ['1','2','3','4','5']
    e   =   ['0.1','0.2','0.3','0.4','0.5']
    t   =   ['350']
    n   =   ['50','100','200']
    data    =    [[[mean([mean(RMSD(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]
    error   =    [[[np.std([mean(RMSD(N,T,E,i)[1]) for i in RUN]) for E in e] for N in n] for T in t]

    for Tdata in data:
        fig,ax=plt.subplots()
        for i in list(range(len(Tdata))):
            plt.errorbar(e,Tdata[i],yerr=error[0][i],label='N = '+n[i]+' Ar',capsize=3)
            print(n[i])
        plt.legend()
        plt.ylim([0,0.25])
        plt.xlabel('E [V/nm]',fontsize=14)
        plt.ylabel(r'$\overline{RMSD}_f$',fontsize=14)
        plt.title('Gas temperature T='+t[0]+' K')
        plt.show()
        plt.clf()

def makeplot_Erot():
    RUN =   ['1']
    e   =   ['0.3']
    t   =   ['250','300','350']
    n   =   ['20','50','100','200']
    for run in RUN:
        for E in e:
            fig,ax=plt.subplots()
            for T in t:
                for N in n:
                    En=rotational_energy(N,T,E,run)
                    plt.plot(En[0],En[1],label=T)
                    plt.show()
                    plt.clf()

def compare_E_Theta():
    RUN=['1','2']
    e=['0.1','0.2','0.3','0.4','0.5']
    t=['250','300','350']
    n=['20','50','100','150','200']
    for E in e:
        for N in n:
            for T in t:
                for run in RUN:
                    if os.path.isfile('/home/harry/Project_2021/xvg_files/csv/Erot_N'+N+'T'+T+'E'+E+'_run_'+run+'.csv'):
                        tmp = orientation(N,T,E,run)
                        Theta = tmp[1]
                        Emea = Em(N,T,E,run)[1]
                        time = [i/1000 for i in tmp[0]]
                        Erot = rotational_energy(N,T,E,run)[1]
                        fig,ax=plt.subplots(2)
                        ax[0].plot(time,smooth(Emea),label=r'$\mathcal{E}$')
                        ax[1].plot(time,smooth(Theta),label=r'$\Theta$',color='orange')
                        ax[1].set_xlabel('t [ns]',fontsize=14)
                        ax[0].set_xticks([])
                        ax[0].set_ylabel(r'$\mathcal{E}$',fontsize=15)
                        ax[1].set_ylabel(r'$\Theta$',fontsize=15)
                        fig.legend(framealpha=1)
                        plt.show()

def compare_Erot_Theta():
    RUN=['1','2','3']
    e=['0.1','0.2','0.3','0.4','0.5']
    t=['250','300','350']
    n=['20','50','100','150','200']
    for E in e:
        for N in n:
            for T in t:
                for run in RUN:
                    if os.path.isfile('/home/harry/Project_2021/xvg_files/csv/Erot_N'+N+'T'+T+'E'+E+'_run_'+run+'.csv'):
                        tmp = orientation(N,T,E,run)
                        Theta = tmp[1]
                        time = [i/1000 for i in tmp[0]]
                        Erot = rotational_energy(N,T,E,run)[1]
                        fig,ax=plt.subplots(2)
                        ax[0].plot(time,smooth(Erot),label=r'$E_{rot,xy}$')
                        ax[1].plot(time,smooth(Theta),label=r'$\Theta$',color='orange')
                        ax[1].set_xlabel('t [ns]',fontsize=14)
                        ax[0].set_xticks([])
                        ax[0].set_ylabel(r'$E_{rot,xy}$ [unm$^2$/ps$^2$]',fontsize=13)
                        ax[1].set_ylabel(r'$\Theta$',fontsize=14)
                        fig.legend(framealpha=1)
                        plt.show()
                    
                

def makeplot_E_statistics():
    RUN =   ['1','2','3','4','5']
    e   =   ['0.5']
    t   =   ['300','350']
    n   =   ['10','20','50','100','150','200','250']
    data = [[[mean([mean(Em(N,T,E,i)[1]) for i in RUN]) for N in n] for T in t] for E in e]
    error = [[[np.std([mean(Em(N,T,E,i)[1]) for i in RUN]) for N in n] for T in t] for E in e]

    for j in list(range(len(data))):
        fig,ax=plt.subplots()
        ax.set_ylim([0,0.06])
        for i in list(range(len(data[j]))):
            plt.errorbar(n,data[j][i],yerr=error[j][i],label='T = '+t[i]+' K',capsize=3)
            print(n[i])
        plt.legend()
        plt.xlabel('N (number of Argons in simulation cell)',fontsize=12)
        plt.ylabel(r'$\mathcal{E}$',fontsize=16)
        plt.show()
        plt.clf()


def main():
    makeplot_E_statistics()
    makeplot_temperature_time()
    makeplot_orientation2()
    makeplot_orientation()
    makeplot_temperature()
    makeplot_RMSD()



if __name__ == "__main__":
    main()

        




























import numpy as np
import csv
import math
import MDAnalysis as mda
import os
from matplotlib import pyplot as plt
from statistics import mean
from units import *


def rotational_energy(N,T,E,run): 
    """Given strings X,Y,Z,run, this functions return the value of E_rot,xy (see equation 10) from simulation files nvt_XAr_YK_ZE.trr/gro"""

    if not os.path.isfile('/home/harry/Project_2021/xvg_files/csv/Erot_N'+N+'T'+T+'E'+E+'_run_'+run+'.csv'):
        if os.path.isdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part'):
            os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
        else:
            os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/erot/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
        u=mda.Universe('nvt_'+N+'Ar_'+T+'K_E'+E+'.gro','nvt_'+N+'Ar_'+T+'K_E'+E+'.trr')
        result = []
        Erot = []
        for ts in u.trajectory:
            p = u.select_atoms("protein")
            M=sum([k.mass for k in p])
            p_v_cm = sum([(1/M)*k.velocity for k in p])
            I = sum([k.mass*sum([i**2 for i in k.position -p.center_of_mass()]) for k in p])
            L=sum([k.mass*np.cross(k.position -p.center_of_mass(),k.velocity-p_v_cm) for k in p])
            Erot_per_axis = [l**2/(2*I) for l in L]
            Erot.append([ts.time,Erot_per_axis[0],Erot_per_axis[1],Erot_per_axis[2]])
            print(Erot[-1])

        header = ['t','Erotx','Eroty','Erotz']
        with open('/home/harry/Project_2021/xvg_files/csv/Erot_N'+N+'T'+T+'E'+E+'_run_'+run+'.csv','w',encoding='UTF8',newline='') as f:           #make .csv
            writer = csv.writer(f)
            writer.writerow(header)
            for i in Erot:
                writer.writerow(i)
    t = []
    Erotx = []
    Eroty = []
    Erotz = []
    os.chdir('/home/harry/Project_2021/xvg_files/csv/')
    with open('/home/harry/Project_2021/xvg_files/csv/Erot_N'+N+'T'+T+'E'+E+'_run_'+run+'.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            t.append(float(row['t']))
            Erotx.append((1/100)*float(row['Erotx'])) #factor (1/100) to change unit to u(ns/ps)^2
            Eroty.append((1/100)*float(row['Eroty']))
            Erotz.append((1/100)*float(row['Erotz']))
    return [t,[Erotx[i] + Eroty[i] for i in list(range(len(t)))]]

def orientation(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./dipoles.xvg'):
        os.system('echo "1" | gmx dipoles -f nvt_'+N+'Ar_'+T+'K_E'+E+'.trr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o dipoles.xvg')
    Theta=([1-i[3]/i[4] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    t = ([i[0] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    return [t,Theta]

def orientation2(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/erot/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./dipoles.xvg'):
        os.system('echo "1" | gmx dipoles -f nvt_'+N+'Ar_'+T+'K_E'+E+'.trr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o dipoles.xvg')
    Theta=([1-i[3]/i[4] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    t = ([i[0] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    return [t,Theta]

def Em(N,T,E,run):
    tmp = Emu(N,T,E,run)
    Epmax=[(D2Cm(1)/nm2m(1))*i for i in tmp[1]]
    t=tmp[0]
    Erot = [i*u2kg(1)*(nm2m(1)/ps2s(1))**2 for i in rotational_energy(N,T,E,run)[1]]
    return [t,[Erot[i]/Epmax[i] for i in list(range(len(t)))]]
    

def potential_energy(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    os.system('echo "1" | gmx dipoles -f nvt_'+N+'Ar_'+T+'K_E'+E+'.trr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o dipoles.xvg')
    Ep=[-np.dot(np.array([i[1],i[2],i[3]]),np.array([0,0,float(E)])) for i in np.loadtxt('dipoles.xvg',comments=('#','@'))]
    t = ([i[0] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    os.system('rm dipoles.xvg')
    return [t,Ep]

def Emu(N,T,E,run):
    if os.path.isdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part'):
        os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    else:
        os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/erot/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./dipoles.xvg'):
        os.system('echo "1" | gmx dipoles -f nvt_'+N+'Ar_'+T+'K_E'+E+'.trr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o dipoles.xvg')
    Emu=[float(E)*i[4] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))]
    t = ([i[0] for i in np.loadtxt('dipoles.xvg',comments=('#','@'))])
    return [t,Emu]
    

def RMSD(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./rmsd.xvg'):
        os.system('echo "3" "3" | gmx rms -f nvt_'+N+'Ar_'+T+'K_E'+E+'.trr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o rmsd.xvg')
    rmsd=([i[1] for i in np.loadtxt('rmsd.xvg',comments=('#','@'))])
    t = ([i[0] for i in np.loadtxt('rmsd.xvg',comments=('#','@'))])
    return [t,rmsd]

def temperature(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./temperature.xvg'):
        os.system('echo "51" "0" | gmx energy -f nvt_'+N+'Ar_'+T+'K_E'+E+'.edr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o temperature.xvg')
    Temperature=([i[1] for i in np.loadtxt('temperature.xvg',comments=('#','@'))])
    t = ([i[0] for i in np.loadtxt('temperature.xvg',comments=('#','@'))])
    return [t,Temperature]

def gas_temperature(N,T,E,run):
    os.chdir('/media/sf_virtualmachine_shared_folder/Project_2021/run'+run+'/N'+N+'T'+T+'E'+E+'/second_part')
    if not os.path.isfile('./gas_temperature.xvg'):
        os.system('echo "50" "0" | gmx energy -f nvt_'+N+'Ar_'+T+'K_E'+E+'.edr -s nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr -o gas_temperature.xvg')
    Temperature=([i[1] for i in np.loadtxt('gas_temperature.xvg',comments=('#','@'))])
    t = ([i[0] for i in np.loadtxt('gas_temperature.xvg',comments=('#','@'))])
    return [t,Temperature]

def smooth(data):
    N = 5
    return [mean(data[0:2*N]) for i in data[0:N]] + [mean(data[i-N:i+N]) for i in [i+N for i in list(range(len(data)-2*N))]] + [mean(data[len(data)-2*N:len(data)]) for i in data[len(data)-N:len(data)]]

def makeplot_energy_vs_N():
    RUN = ['1','2','3']
    n = ['20','50','100','150','200','250']
    E='0.5'
    T='350'
    data = [[mean(erot(N,T,E,run)[1]) for run in RUN] for N in n]
    E_rot = [mean(i) for i in data]
    error = [np.std(i) for i in data]
    fig,ax=plt.subplots()

    plt.errorbar([float(i) for i in n],E_rot,yerr=error,label='E=0.5 V/nm, T=350 K')
    plt.xlabel('Number of gas particles, N')
    plt.ylabel(r'Mean $E_{rot,xy}$ [unm$^2$/ps$^2$]')
    plt.ylim([0,3])
    plt.legend()
    plt.show()
    plt.clf()

def makeplot_energy_measure():
    RUN = ['1','2','3']
    T = ['350','250','300']
    n= ['20','50','100','200']
    e = ['0.1','0.2','0.3','0.4','0.5']
    error = []
    raw = []
    col = ['green','orange','blue','red','cyan']
    for N in n:
        E_temp = []
        for E in e:
            temp = []
            for run in RUN:
                Er = rotational_energy(N,T,E,run)[1]
                Ep = Emu(N,T,E,run)[1]

                if option == 1:
                    temp += [Er[i]/Ep[i] for i in list(range(len(Er)))]
                elif option == 2:
                    temp.append(mean([Er[i]/Ep[i] for i in list(range(len(Er)))]))
                elif option == 3:
                    temp.append(mean(Er))

            E_temp.append(temp)
        raw.append(E_temp)
    data = [[mean(i) for i in j] for j in raw]
    error = [[np.std(i) for i in j] for j in raw]
    fig,ax = plt.subplots()
    for j in list(range(len(data))):
        plt.errorbar([str(i) for i in e],data[j],yerr=error[j])
    plt.legend()
    plt.show()
    plt.clf()
    for i in list(range(len(data))):

        plt.scatter(e,[raw[i][j][0] for j in list(range(len(e)))],color=col[i])
        plt.scatter(e,[raw[i][j][1] for j in list(range(len(e)))],color=col[i])
    plt.legend()
    plt.show()
    plt.clf()

def main():




if __name__ == "__main__":
    main()


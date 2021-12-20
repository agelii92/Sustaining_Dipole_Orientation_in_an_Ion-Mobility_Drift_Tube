import os
from rotate import *

N=Nvalue
T=Tvalue
E=Evalue

N = str(N)
T=str(T)
E=str(E)

E1='0'

#get the topology and final frame of pre run
os.system('cp ../1ubq_'+N+'Ar.top .')
os.system('cp ../nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.gro .')
os.system('cp ../nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.tpr .')

#rotate the structure
filename = 'nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.gro'
newname = '1ubq_'+N+'Ar_oriented'
angles = rotation_angles(N,T,E)
os.system('gmx editconf -f ' + filename + ' -rotate '+angles[0]+' '+angles[1]+' '+angles[2]+' -o intermediate.gro')
os.system('gmx editconf -f intermediate.gro -rotate 0 -90 0 -o ' + newname + '_before.gro')
os.system('echo "1" "0" | gmx trjconv -f 1ubq_'+N+'Ar_oriented_before.gro -s nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.tpr -pbc mol -ur compact -center -o '+newname+'.gro')

#Replace the reference temperature for the argons. Reference temperature for protein fixed at 308K.
os.system('mv nvt.mdp nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')

#Handling the special case of N = 0 by removing the Non-Protein tc-group in the mdp files
if N == '0':
        os.system('sed -i \'s/tc-grps                 = Non-Protein Protein/;tc-grps                 = Protein/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')        
        os.system('sed -i \'s/tau_t                   = 0.1 -1/;tau_t                   = -1/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')
        os.system('sed -i \'s/ref_t                   = 300 300/;ref_t                   = '+T+'/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')
        os.system('sed -i \'s/energy-grps             = Non-Protein Protein/;energy-grps             = Protein/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')
	os.system('sed -i \'s/tcoupl                  = V-rescale/tcoupl                  = no/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')
else:
        os.system('sed -i \'s/ref_t                   = 300 300/ref_t                   = '+T+' 308/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')

#Enter the given field strenght in the .mdp files, ie replace the key word 'confield'
os.system('sed -i \'s/confield/'+E+'/g\' nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp')

#Edit the run.sh file including the GROMACS commands
c1 = 'grompp -p 1ubq_'+N+'Ar.top -c '+newname+'.gro -f nvt_'+N+'Ar_'+T+'K_E'+E+'.mdp -maxwarn 2 -o nvt_'+N+'Ar_'+T+'K_E'+E+'.tpr'
c6 = 'mdrun -ntmpi 1 -nt 1 -v -deffnm  nvt_'+N+'Ar_'+T+'K_E'+E

commands = [c1,c6]
rows = ['row_1','row_6']

for i in range(2):
        os.system('sed -i \'s/'+rows[i]+'/'+commands[i]+'/g\' run2.sh')

os.system('nohup ./run2.sh&')


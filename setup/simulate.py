import os

#input simulation parameters
N = str(input('Number of Argons: '))
T = str(input('Argon reference temperature: '))
E = str(input('Electric field in z direction in Vnm\^-1: '))

#edit the second run parameters
os.chdir('./second_part/')
os.system('sed -i \'s/Nvalue/\''+N+'\'/g\' simulate2.py')
os.system('sed -i \'s/Tvalue/\''+T+'\'/g\' simulate2.py')
os.system('sed -i \'s/Evalue/\''+E+'\'/g\' simulate2.py')
os.chdir('../')

#center the starting structure
os.system('gmx editconf -f oriented_T308K_noncenter.gro -c -o oriented_T308K.gro')

E1 = '0'
#Use gmx insert-molecules to setup structure (.gro)
if N == '0':
        os.system('mv oriented_T308K.gro 1ubq_'+N+'Ar_pre.gro')

else:
        os.system('gmx insert-molecules -f oriented_T308K.gro -nmol '+N+' -ci 1ar.pdb -o 1ubq_'+N+'Ar_pre.gro')

#Edit the topology (.top) to match the number of Argons
os.system('mv topol_with_Ar.top 1ubq_'+N+'Ar.top')
os.system('sed -i \'s/Argon  100/Argon  '+N+'/g\' 1ubq_'+N+'Ar.top')
os.system('cp 1ubq_'+N+'Ar.top ./second_part/')

#Replace the reference temperature for the argons. Reference temperature for protein fixed at 308K.
os.system('mv nvt.mdp nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')

#Handling the special case of N = 0 by removing the Non-Protein tc-group in the mdp files
if N == '0':
        os.system('sed -i \'s/tc-grps                 = Non-Protein Protein/tc-grps                 = Protein/g\' nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')        
        os.system('sed -i \'s/tau_t                   = 0.1 0.1/tau_t                   = 0.1/g\' nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')
        os.system('sed -i \'s/ref_t                   = 300 300/ref_t                   = 308/g\' nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')
        os.system('sed -i \'s/energy-grps             = Non-Protein Protein/;energy-grps             = Protein/g\' nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')

else:
        os.system('sed -i \'s/ref_t                   = 300 300/ref_t                   = '+T+' 308/g\' nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp')

#Edit the run.sh file including the GROMACS commands
c1 = 'grompp -p 1ubq_'+N+'Ar.top -c 1ubq_'+N+'Ar_pre.gro -f nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.mdp -maxwarn 2 -o nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre.tpr'
c6 = 'mdrun -ntmpi 1 -nt 1 -v -deffnm  nvt_'+N+'Ar_'+T+'K_E'+E1+'_pre'

commands = [c1,c6]
rows = ['row_1','row_6']

for i in range(2):
        os.system('sed -i \'s/'+rows[i]+'/'+commands[i]+'/g\' run.sh')


os.system('nohup ./run.sh&')


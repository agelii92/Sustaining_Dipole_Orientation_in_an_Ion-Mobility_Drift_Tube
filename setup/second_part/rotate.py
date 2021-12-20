import os
import math
import numpy as np

def rotation_angles(N,T,E):

        filename = 'nvt_' + N + 'Ar_' + T + 'K_E0_pre'
        os.system('echo "1" | /home/emiliano/SOFTWARE/gromacs-2019.3/local/gromacs/bin/gmx dipoles -f '+filename+'.gro -s '+filename+'.tpr -o dipole_N' + N + '_T' + T + '_E'+E+'.xvg')
	filename = 'dipole_N' + N + '_T' + T + '_E'+E+'.xvg'
	


	os.system('cp ' + filename + ' data.txt')
	with open('data.txt') as f:
		lines = f.readlines()
	dipole = [float(i) for i in lines[-1].split()]

        x=dipole[1]
        y=dipole[2]
        z=dipole[3]

        theta_x = math.atan(y/z) + math.pi if z<0 else math.atan(y/z)
        r_x=x
        r_y=y*math.cos(theta_x)-z*math.sin(theta_x)
        r_z=y*math.sin(theta_x) + z*math.cos(theta_x)

        theta_y =  math.pi + math.atan(r_z/x) if x<0 else math.pi/2-math.atan(x/r_z)#
	print([str((180/math.pi)*theta_x),str((180/math.pi)*theta_y),str(0)])
        return([str((180/math.pi)*theta_x),str((180/math.pi)*theta_y),str(0)])


#procedure: use the dipole of the original structure dipoles.xvg, script returns angles [x,y,z] 
#rotate the structure with this angles using gmx editconf rotate
#after this, rotate the resulting structure by [0 -90 0]


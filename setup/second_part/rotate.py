import os
import math
import numpy as np

def rotation_angles(N,T,E):
"""
Given a .gro file with appropriate naming, this script extract the dipole moment of the structure, analyzes it, and returns three rotation angles [x,y,z].
If the structure then is rotated using gmx editconf rotate by these angles, and then by angles [0,-90,0] in a second rotation, the dipole will align
with the z-axis.
"""        
        filename = 'nvt_' + N + 'Ar_' + T + 'K_E0_pre'
        os.system('echo "1" | gmx dipoles -f '+filename+'.gro -s '+filename+'.tpr -o dipole_N' + N + '_T' + T + '_E'+E+'.xvg')
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


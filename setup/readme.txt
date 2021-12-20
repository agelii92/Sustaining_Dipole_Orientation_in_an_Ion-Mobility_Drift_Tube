This setup was created using GROMACS version 4.6.5. The simulation is of a ubiquitin protein surrounded by 
N argon atoms at temperature T. Protein is subject to dipole orientation of an electric field E. Box side length is 10 nm. At the start of a simulation, the user enter the desried values of N,T,E.

The starting structure has undergone energy minimization. The simulation takes two steps:

1) 400ps equlibration run with temperature coupling for both the protein and non protein group. The 
coupling reference temperature of the protein group is at 308 K to match the result from Sinelnikova et al, meaning the final temperature of a Ubiqutin after 10ns of dipole orienation. The reference temperature of coupling for the non protein group is the input temperature T. There is no electric field in this part of the simulation. This first part is executed by running the script simulate.py. The script is run 

2) The equlibrated system is rotated to align with the z-direction. In the second part there is an external electric field of magnitude E and temperature coupling only for the non-protein group. This simulation runs for 10ns and is executed by the script simulate2.py.

Both scripts execute the simulation using nohup. For further understanding, see comments in the files.
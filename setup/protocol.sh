gmx pdb2gmx -f 1ubq.pdb -p topol_only_ubi.top -o 1ubq.gro<<EOF
16
8
EOF


gmx editconf -f 1ubq.gro -d 3 -o 1ubq_box.gro


gmx insert-molecules -f 1ubq_box.gro -o 1ubq_100Ar.gro -nmol 100 -ci  1ar.pdb


gmx grompp -p topol_with_Ar.top -c 1ubq_100Ar.gro -f min.mdp -o min.tpr

gmx mdrun -v -deffnm min



gmx grompp -p topol_with_Ar.top -c min.gro -f nvt_150.mdp -o nvt_150K.tpr

gmx mdrun -v -deffnm nvt_150K



gmx grompp -p topol_with_Ar.top -c nvt_150K.gro -f nvt_300.mdp -o nvt_300K.tpr

gmx mdrun -v -deffnm  nvt_300K



gmx grompp -p topol_with_Ar.top -c nvt_300K.gro -f npt_300.mdp -o npt_300K.tpr

gmx mdrun -v -deffnm  npt_300K

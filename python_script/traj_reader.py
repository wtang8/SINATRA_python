#!/bin/python3

import MDAnalysis as mda
from MDAnalysis.analysis import align
from MDAnalysis.analysis.rms import rmsd
import numpy as np, os, sys
from simplices_construction import *

####
# Convert MD simulation trajectory to aligned protein structures in PDB format
# 
# protA = name of protein A
# protB = name of protein B
# struct_file = protein structure file e.g. .pdb, .gro, .tpr, .pqr
# traj_file = MD trajectory file e.g. .xtc, .dcd, .trj
# nsample = # of sample structure drawn from trajecotry at even time interval
# directory = directory to store all the files
####

def convert_traj_pdb_aligned(protA, protB, struct_file_A, traj_file_A, struct_file_B, traj_file_B, nsample = 101, selection = None, directory = None):
    if directory == None:
        directory = "%s_%s"%(protA,protB)

    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    
    try:
        os.mkdir("%s/pdb"%directory)
    except FileExistsError:
        pass

    refu = mda.Universe(struct_file_A,traj_file_A)
    refu.trajectory[0]
    if selection == None:
        refuCA = refu.select_atoms('name CA')
    else:
        refuCA = refu.select_atoms('name CA and %s'%selection)
    com_refuCA = refuCA.center_of_mass()
    refu0 = refuCA.positions - com_refuCA

    for prot, struct_file, traj_file in zip([protA,protB],[struct_file_A,struct_file_B],[traj_file_A,traj_file_B]):

        u = mda.Universe(struct_file,traj_file)
        u.trajectory[0]
        if selection == None:
            refuCA = refu.select_atoms('name CA')
        else:
            refCA = u.select_atoms('name CA and %s'%selection)

        com_refCA = refCA.center_of_mass()
        ref0 = refCA.positions - com_refCA

        R, rmsdval = align.rotation_matrix(ref0, refu0)
        refCA.translate(-refCA.center_of_mass())
        refCA.rotate(R)
        ref0 = refCA.positions

        CA = u.select_atoms('name CA and %s'%selection)
        if selection == None:
            noh = u.select_atoms('protein and not type H')
        else:
            noh = u.select_atoms('protein and not type H and %s'%selection)

        rmsds = []
        t = []
        nframe = len(u.trajectory)
        nskip =  int(nframe/nsample)
        
        frame = 0
        i_sample = 0
        for ts in u.trajectory:
            if frame % nskip == 0:
                print(ts.time) 
                traj0 = CA.positions - CA.center_of_mass()
                R, rmsdval = align.rotation_matrix(traj0, ref0)
                noh.translate(-CA.center_of_mass())
                noh.rotate(R)
                noh.write('%s/pdb/%s/%s_frame%d.pdb'%(directory,prot,prot,i_sample))
                i_sample += 1
            frame += 1

    return

def convert_pdb_mesh(protA, protB, nsample = 101, directory = None):
    
    if directory == None:
        directory = "%s_%s"%(protA,protB)

    try:
        os.mkdir(directory)
    except FileExistsError:
        pass
    
    try:
        os.mkdir("%s/mesh"%directory)
    except FileExistsError:
        pass

    r = []
    for prot in [protA, protB]:
        sys.stdout.write('Calculating sphere radius...\n')
        for i_sample in range(nsample):
            trajwhole = mda.Universe('%s/pdb/%s/%s_frame%d.pdb'%(directory,prot,prot,i_sample)).select_atoms('protein and not type H')
            comp = ComplexFiltration()
            comp.vertices = trajwhole.positions
            r.append(np.amax(np.linalg.norm(comp.vertices,axis=1)))
    rmax = np.amax(r)
    #print('Rmax = %.3f'%rmax)

    for mutant in mutants:
        for i in range(nsample+1):
            frame = i*100
            trajwhole = mda.Universe('%s/pdb/%s/%s_frame%d.pdb'%(directory,mutant,mutant,frame)).select_atoms('protein and not type H')
            sys.stdout.write('Constructing topology for %s for Frame %d...\r'%(mutant,frame))
            sys.stdout.flush()
            comp = ComplexFiltration()
            comp.vertices = trajwhole.positions
            comp.calc_distance_matrix()
            edges, distances = comp.get_edge_list(radius=4)
            faces = comp.edge_to_face_list(edges=edges)
            comp.vertices /= rmax
            comp.write_mesh_file(edges=edges,faces=faces,filename='mesh_noh/%s_65_213_4/%s_4_frame%d.msh'%(mutant,mutant,frame))
        


from mpi4py import MPI
import time
import sys

from random import random
from math import sqrt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def cal_pi(step):
	hits=0
	for i in range(1,step):
		x,y=random(),random()
		dist=sqrt(x**2+y**2)
		if dist<=1.0:
			hits=hits+1
	return hits

ar = sys.argv
if len(ar) >= 2:
    N = int(sys.argv[1])
    step = N // size
    t0=time.time()
    value = cal_pi(step)
    result = 0.0
    if rank == 0:
        result += value
        for i in range(1,size):
            value = comm.recv(source=i, tag=0)
            result += value
        t1=time.time()
        print('pi = {} duration = {} s'.format(result*4/N,t1-t0))
    
    else:
        comm.send(value, dest=0, tag=0)
else:
    if rank == 0:
        print("Usage: mpirun -n <total cpu number> ./<program name> <number of tosses>")

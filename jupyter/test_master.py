from mpi4py import MPI
import sys
sys.path.insert(0, '//home/csunix/sc16ho/dev/miind/build/libs/PythonWrapper')
import libmiindpw

comm = MPI.COMM_WORLD
print "MASTER RANK: " + str(comm.Get_rank())

print MPI.Get_processor_name()

wrapped = libmiindpw.Wrapped()
wrapped.init()
wrapped.startSimulation()

x = [0.0 for a in range(76)]

while(1):
	x = wrapped.evolveSingleStep(x)

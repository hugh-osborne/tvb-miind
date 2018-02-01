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

x = [0.0]

for i in range(int(50.0 / 0.01)):
	wrapped.evolveSingleStep(x)

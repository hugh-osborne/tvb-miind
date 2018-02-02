from mpi4py import MPI
import sys
sys.path.insert(0, '/home/hugh/dev/miind/build/libs/PythonWrapper')
import libmiindpw

comm = MPI.COMM_WORLD
print "MASTER RANK: " + str(comm.Get_rank())

print MPI.Get_processor_name()

wrapped = libmiindpw.Wrapped()
wrapped.init()
wrapped.startSimulation()

x = [0.0]

for i in range(int(500.0 / 0.01)):
	print x
	y = wrapped.evolveSingleStep(x)
	print y

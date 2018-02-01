from mpi4py import MPI
import sys
sys.path.insert(0, '//home/csunix/sc16ho/dev/miind/build/libs/PythonWrapper')
import libmiindpw

comm = MPI.COMM_WORLD
print "CHILD RANK: " + str(comm.Get_rank())

wrapped = libmiindpw.Wrapped()
wrapped.init()
wrapped.evolve()

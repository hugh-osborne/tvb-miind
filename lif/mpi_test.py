from mpi4py import MPI

comm = MPI.COMM_SELF.Spawn('lif', args=None, maxprocs=1)

print "MASTER RANK: " + str(comm.Get_rank())


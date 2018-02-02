from mpi4py import MPI
import sys
sys.path.insert(0, '//home/csunix/sc16ho/dev/miind/build/libs/PythonWrapper')
import libmiindpw

from tvb.simulator.lab import *
reload(models)

oscilator = models.MiindLif(76, 10**2)

comm = MPI.COMM_WORLD
print "CHILD RANK: " + str(comm.Get_rank())

wrapped = libmiindpw.Wrapped()
wrapped.init(oscilator.number_of_nodes, oscilator.simulation_length, [oscilator.c_ee[0], oscilator.c_ei[0],
oscilator.c_ie[0], oscilator.c_ii[0], oscilator.tau_e[0], oscilator.tau_i[0], oscilator.k_e[0], oscilator.k_i[0],
oscilator.r_e[0], oscilator.r_i[0], oscilator.a_e[0], oscilator.a_i[0], oscilator.b_e[0],
oscilator.b_i[0], oscilator.P[0], oscilator.Q[0]])
wrapped.evolve()

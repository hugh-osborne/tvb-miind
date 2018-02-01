# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2017, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)

"""
Description of models

"""

from .base import ModelNumbaDfun, LOG, numpy, basic, arrays
from numba import guvectorize, float64

from mpi4py import MPI

import sys
sys.path.insert(0, '//home/csunix/sc16ho/dev/miind/build/libs/PythonWrapper')

import libmiindpw


class MiindLif(ModelNumbaDfun):
    r"""
	<References and explanation>
    """
    _ui_name = "MIIND LIF"
    ui_configurable_parameters = ['I_o']

    #Define traited attributes for this model, these represent possible kwargs.

    I_o = arrays.FloatArray(
        label=":math:`I_{o}`",
        default=numpy.array([0.33, ]),
        range=basic.Range(lo=0.0, hi=1.0, step=0.01),
        doc="""[nA] Effective external input""",
        order=1)

    #sigma_noise = arrays.FloatArray(
    #    label=r":math:`\sigma_{noise}`",
    #    default=numpy.array([0.000000001, ]),
    #    range=basic.Range(lo=0.0, hi=0.005),
    #    doc="""[nA] Noise amplitude. Take this value into account for stochatic
    #    integration schemes.""",
    #    order=-1)

    state_variable_range = basic.Dict(
        label="State variable ranges [lo, hi]",
        default={"S": numpy.array([0.0, 1.0])},
        doc="Population firing rate",
        order=2
    )

    variables_of_interest = basic.Enumerate(
        label="Variables watched by Monitors",
        options=["S"],
        default=["S"],
        select_multiple=True,
        doc="""default state variables to be monitored""",
        order=10)

    state_variables = ['S']
    _nvar = 1
    cvar = numpy.array([0], dtype=numpy.int32)

    def __init__(self, num_nodes):
        self.number_of_nodes = num_nodes
        self.wrapped = libmiindpw.Wrapped()

    def configure(self):
        comm = MPI.COMM_WORLD
        print "MASTER RANK: " + str(comm.Get_rank())
        """  """
        super(MiindLif, self).configure()
        self.update_derived_parameters()
    	self.wrapped.init()
	self.wrapped.startSimulation()

    def dfun(self, x, c, local_coupling=0.0):
        x_ = x.reshape(x.shape[:-1]).T
        c_ = c.reshape(c.shape[:-1]).T + local_coupling * x[0]

    	x_ = (numpy.array([[x] for x in self.wrapped.evolveSingleStep([x[0] for x in c_])]))

        return x_.T[..., numpy.newaxis]

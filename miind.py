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

import imp

class Miind(ModelNumbaDfun):
    r"""
    **References**:

    .. [MDK_2003] .

    """

    _ui_name = "MIIND"
    ui_configurable_parameters = []

    # Used for phase-plane axis ranges and to bound random initial() conditions.
    state_variable_range = basic.Dict(
        label="State Variable ranges [lo, hi]",
        default={"S": numpy.array([0.0, 1.0])},
        doc="Population firing rate",
        order=17)

    variables_of_interest = basic.Enumerate(
        label="Variables watched by Monitors",
        options=["S"],
        default=["S"],
        select_multiple=True,
        doc="""default state variables to be monitored""",
        order=18)

    state_variables = [S]
    _nvar = 1
    cvar = numpy.array([0], dtype=numpy.int32)

    def __init__(self, module_name, module_path, num_nodes, simulation_length, dt):
        miind = imp.load_source(module_name, module_path)
        self.number_of_nodes = num_nodes
        self.simulation_length = simulation_length
        self.wrapped = miind.Wrapped(number_of_nodes, simulation_length, dt)

    def configure(self):
        """  """
        super(MiindLif, self).configure()
        self.update_derived_parameters()
    	self.wrapped.init()
	self.wrapped.startSimulation()

    def dfun(self, x, c, local_coupling=0.0):

        S = x[0, :]

        # long-range coupling
        c_0 = c[0, :]

        # short-range (local) coupling - currently un-used
        lc_0 = local_coupling * S

        # Would be nice to pass this function as a parameter
        coupling_S = c_0 + lc_0

        c_ = coupling_S[:,0]
    	x_ = numpy.array(self.wrapped.evolveSingleStep(c_.tolist()))

        return numpy.reshape(x_, x.shape)

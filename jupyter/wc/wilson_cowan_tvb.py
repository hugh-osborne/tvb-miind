import pylab
import numpy
import matplotlib.pyplot as plt

from tvb.simulator.lab import *
reload(models)

numpy.random.seed(0)
E_init = numpy.random.rand(76)
I_init = numpy.random.rand(76)
inits = numpy.row_stack((E_init, I_init))
initial_conditions = numpy.expand_dims(numpy.expand_dims(inits, axis=0), axis=3)

print initial_conditions[0]

white_matter = connectivity.Connectivity(load_default=True)
white_matter.speed = numpy.array([4.0])

oscilator = models.WilsonCowan()

white_matter_coupling = coupling.Linear(a=0.0154)
heunint = integrators.EulerDeterministic()

mon_raw = monitors.Raw()
mon_tavg = monitors.TemporalAverage(period=2**-2)
what_to_watch = (mon_raw, mon_tavg)

sim = simulator.Simulator(model = oscilator, connectivity = white_matter,
                          coupling = white_matter_coupling,
                          integrator = heunint, monitors = what_to_watch,
                          initial_conditions = initial_conditions)

sim.configure()

raw_data = []
raw_time = []
tavg_data = []
tavg_time = []

print raw_data

for raw, tavg in sim(simulation_length=10**2):
    if not raw is None:
    	raw_time.append(raw[0])
    	raw_data.append(raw[1])
    if not tavg is None:
    	tavg_time.append(tavg[0])
    	tavg_data.append(tavg[1])

print raw_data[0]

RAW = numpy.array(raw_data)
TAVG = numpy.array(tavg_data)

plt.figure()
plt.plot(raw_time, RAW[:, 0, :, 0])
plt.title("Raw -- State variable 0")

plt.figure()
plt.plot(tavg_time, TAVG[:, 0, :, 0])
plt.title("Temporal average")

plt.show()

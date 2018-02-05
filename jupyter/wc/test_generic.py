import pylab
import numpy
import matplotlib.pyplot as plt

from tvb.simulator.lab import *
reload(models)

white_matter = connectivity.Connectivity(load_default=True)
white_matter.speed = numpy.array([4.0])

oscilator = models.Miind('libmiindpython.so',76, 1**2, 0.000770095348827)

white_matter_coupling = coupling.Linear(a=0.0154)
heunint = integrators.Identity(dt = 0.000770095348827) # dt of the integrator should be defined to match MIIND

mon_raw = monitors.Raw()
mon_tavg = monitors.TemporalAverage(period=2**-3)
what_to_watch = (mon_raw, mon_tavg)

sim = simulator.Simulator(model = oscilator, connectivity = white_matter,
                          coupling = white_matter_coupling,
                          integrator = heunint, monitors = what_to_watch)

sim.configure()

raw_data = []
raw_time = []
tavg_data = []
tavg_time = []

for raw, tavg in sim(simulation_length=1**2):
    if not raw is None:
    	raw_time.append(raw[0])
    	raw_data.append(raw[1])
    if not tavg is None:
    	tavg_time.append(tavg[0])
    	tavg_data.append(tavg[1])

RAW = numpy.array(raw_data)
TAVG = numpy.array(tavg_data)

plt.figure(1)
plt.plot(raw_time, RAW[:, 0, :, 0])
plt.title("Raw -- State variable 0")

plt.figure(2)
plt.plot(tavg_time, TAVG[:, 0, :, 0])
plt.title("Temporal average")

plt.show()

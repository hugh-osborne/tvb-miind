import pylab
import numpy 
import matplotlib.pyplot as plt

from tvb.simulator.lab import *
reload(models)

white_matter = connectivity.Connectivity(load_default=True)
white_matter.speed = numpy.array([4.0])

oscilator = models.MiindLif(len(white_matter.region_labels))

white_matter_coupling = coupling.Linear(a=0.0154)
heunint = integrators.Identity()

mon_raw = monitors.Raw()
mon_tavg = monitors.TemporalAverage(period=2**-2)
what_to_watch = (mon_raw, mon_tavg)

sim = simulator.Simulator(model = oscilator, connectivity = white_matter,
                          coupling = white_matter_coupling,
                          integrator = heunint, monitors = what_to_watch)

sim.configure()

raw_data = []
raw_time = []
tavg_data = []
tavg_time = []

for raw, tavg in sim(simulation_length=2**5):
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

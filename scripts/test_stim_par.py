' Author: Darian Hadjiabadi '
' Quick script to perform parallel stimulations and visualize soma potentials for a given cell type '


import sys
import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
from neuron import h, gui

from pyramidal_cell_14Vb import PyramidalCell
from basket_cell17S import BasketCell
from axoaxonic_cell17S import AxoAxonicCell
from bistratified_cell13S import BistratifiedCell
from olm_cell2 import OLMCell
from stim_cell import StimCell

def simulation(amp):

    for t in np.arange(0,T,10):
        current_clamp = h.IClamp(cell.soma(0.5))
        current_clamp.delay = t
        current_clamp.dur   = 1.0
        current_clamp.amp   = amp
        iclamps.append(current_clamp)

    time         = h.Vector()
    soma_v       = h.Vector()
    radTprox_v   = h.Vector()
    radTmed_v    = h.Vector()
    radTdist_v   = h.Vector()
    radTprox_ina = h.Vector()
    radTmed_ina  = h.Vector()
    radTdist_ina = h.Vector()

    time.record(h._ref_t)
    soma_v.record(cell.soma(0.5)._ref_v)
    #radTprox_v.record(cell.radTprox(0.5)._ref_v)
    #radTmed_v.record(cell.radTmed(0.5)._ref_v)
    #radTdist_v.record(cell.radTdist(0.5)._ref_v)
    #radTprox_ina.record(cell.radTprox(0.5)._ref_ina)
    #radTmed_ina.record(cell.radTmed(0.5)._ref_ina)
    #radTdist_ina.record(cell.radTdist(0.5)._ref_ina)

    h.finitialize(-65)
    h.continuerun(T)

    #plt.figure()
    #plt.plot(time, soma_v)
    #plt.plot(time, radTprox_v)
    #plt.plot(time, radTmed_v)
    #plt.plot(time, radTdist_v)
    #plt.legend(['soma', 'proximal', 'medial', 'distal'])

    #plt.figure()
    #plt.plot(time, radTprox_ina)
    #plt.plot(time, radTmed_ina)
    #plt.plot(time, radTdist_ina)
    #plt.legend(['proximal', 'medial', 'distal'])
 
    return (amp, soma_v, time)

pc = h.ParallelContext()
rank = int(pc.id())

if rank == 0:
    intro_str = \
    """
    This file will run a simulation of CA1 microcircuit as defined by 
    Cutsuridis et al 2010 Encoding and Retrieval in a Model of the Hippocampal CA1 Microcircuit. 
    The model CA1 pyramidal cells has been removed and exchanged with the model provided by .... 
    """
    print(intro_str)

#cell = PyramidalCell()
#cell = BasketCell()
#cell = AxoAxonicCell()
#cell = BistratifiedCell()
cell = OLMCell()

T = 100
h.dt = 0.025
h.celsius = 37
iclamps  = []
amps     = []
voltages = []
times    = []

pc.runworker()
for amp in np.arange(0.1, 5.1, 0.25):
    pc.submit(simulation, amp)
while (pc.working()):
    amp, soma_v, time = pc.pyret()
    amps.append(amp)
    voltages.append(soma_v)
    times.append(time)
    print('completed simulation for amplitude %f' % (amp))
pc.done()

plt.figure()
for i in range(len(amps)):
    plt.plot(times[i], voltages[i])
plt.show()



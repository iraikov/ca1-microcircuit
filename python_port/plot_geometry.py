' Author: Darian Hadjiabadi '
' Visualize cell geometry '


import sys
import numpy as np
from neuron import h, gui

from pyramidal_cell_14Vb import PyramidalCell
from basket_cell17S import BasketCell
from axoaxonic_cell17S import AxoAxonicCell
from bistratified_cell13S import BistratifiedCell
from olm_cell2 import OLMCell

def show_geometry(obj):
    sections = obj.all
    ps = h.PlotShape(sections)
    ps.exec_menu('Shape Plot')

hello_user = \
"""
    We are going to plot geometry. 
    How does that make you feel?
"""
print(hello_user)
#cell = PyramidalCell()
#cell = BasketCell()
#cell = AxoAxonicCell()
cell = BistratifiedCell()
#cell = OLMCell()
show_geometry(cell)


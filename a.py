
import math
import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot

pi = math.pi
x = np.linspace(0, 2*pi, 100)
y = np.sin(x)

pyplot.plot(x, y)
pyplot.savefig('sin.png')

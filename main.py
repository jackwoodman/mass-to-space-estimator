import math
import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as pyplot
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot
from simUtilities import plotValues, calculateDrag, f


t_max = 500 # time bound = 2 minutes / 120 seconds
t = np.linspace(0, t_max, t_max+1) # time interval = 1 second

# constants
MASS_MULTIPLIER = 1.1
I_srb = 2370    # specific impulse of Space Shuttle SRB (ms^-1)
g = 9.8    # gravity constant
t_r = 12_000_000    # avg. sea level thrust of Space Shuttle SRB (N)
rocketMass = 90_000    # dry mass of SRB
maximumMass = 590_000    # maximum wet mass of SRB + spacecraft
capsuleMass = 4_000   # empty mass of Dragon capsule as reference
capsuleCapacity = 7    # crew capacity of Dragon capsule as reference
spacecraftMass = 0


T_0 = np.array([1])

while True:
    # loop until no longer able to reach space

    # calculate vehicle masses
    dryMass = rocketMass + spacecraftMass
    fuelMass = maximumMass - dryMass

    # rocket starts with full mass, no altitude or velocity
    X_0 = np.array([fuelMass, 0, 0])


    X = odeint(f, X_0, t, args=(dryMass, I_srb, g, t_r))
    foundBest = plotValues(spacecraftMass, X, t)

    if (foundBest):
        # display best results
        numCapsules = int(foundBest / capsuleMass)
        numAstronauts = numCapsules * 7
        print(f"Maximum Mass to Space: {int(foundBest):,d}kg")
        print(f"This is equal to {numCapsules} Dragon capsules, carrying {numAstronauts} astronauts.")
        break

    # increase spacecraft mass by constant MASS_MULTIPLIER
    spacecraftMass = (capsuleMass if spacecraftMass == 0 else (spacecraftMass * MASS_MULTIPLIER))

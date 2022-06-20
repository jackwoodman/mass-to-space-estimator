def plotValues(spacecraftMass, values, time):
    # function to display the calculated values

    # I've adapted some demo code from the matplotlib docs so I could have
    # multiple y-axes: https://matplotlib.org/2.0.2/examples/axes_grid/demo_parasite_axes2.html


    # list of axis/value titles
    axes = {
        "Time" : "Time (s)",
        "Alt" : "Altitude (m)",
        "Vel" : "Velocity (ms^-1)",
        "Mass" : "Mass (million kg)"
    }

    # transpose the matrix so that each column corresponds to an dependent variable
    valuePlots = np.transpose(values)

    # determine max values for axes
    VEL_MAX = 3_000
    MASS_MAX = 600_000
    ALT_MAX = (int(max(valuePlots[1]))) * 1.1

    # get maximum altitude reached and mass
    maximumAlt = int(max(valuePlots[1]))


    if (maximumAlt >= 100_000):
        # this mass puts rocket above Karman line

        # create a 'host' plot, and two parasite plots to display all three variables at different scales
        hostPlot = host_subplot(111, axes_class=AA.Axes)
        pyplot.subplots_adjust(right=0.75)
        parasite_1 = hostPlot.twinx()
        parasite_2 = hostPlot.twinx()

        parasite_offset = 70
        new_fixed_axis = parasite_2.get_grid_helper().new_fixed_axis

        # assign parasites to right and enable, offset the second parasite
        parasite_1.axis["right"] = new_fixed_axis(loc="right", axes=parasite_1)
        parasite_1.axis["right"].toggle(all=True)
        parasite_2.axis["right"] = new_fixed_axis(loc="right", axes=parasite_2, offset=(parasite_offset, 0))
        parasite_2.axis["right"].toggle(all=True)
        # made it to space, display graph and return true for this mass

         # assign labels to all four axes
        hostPlot.set_xlabel(axes["Time"])
        hostPlot.set_ylabel(axes["Alt"])
        parasite_1.set_ylabel(axes["Vel"])
        parasite_2.set_ylabel(axes["Mass"])

        # assign three dependent variables to the three y-axes
        altitudePlot, = hostPlot.plot(time, valuePlots[1], label=axes["Alt"])
        velocityPlot, = parasite_1.plot(time, valuePlots[2], label=axes["Vel"])
        massPlot, = parasite_2.plot(time, valuePlots[0], label=axes["Mass"])

        # restrict y limits on parasite axes
        parasite_1.set_ylim(-VEL_MAX, VEL_MAX)
        parasite_2.set_ylim(0, MASS_MAX)

        # display legend and assign the colours of the individual plots to the labels
        hostPlot.legend()
        hostPlot.axis["left"].label.set_color(altitudePlot.get_color())
        parasite_1.axis["right"].label.set_color(velocityPlot.get_color())
        parasite_2.axis["right"].label.set_color(massPlot.get_color())
        #parasite_3.axis["right"].label.set_color(thrustPlot.get_color())

        # display plot in final state, move legend to below plot
        title = f"Mass vs. Maximum Altitude (spacecraftMass = {spacecraftMass:,d}kg)"
        pyplot.legend(loc = "lower center", bbox_to_anchor = (0.5, -0.25), ncol = len(axes)-1 )
        pyplot.title(title, y = 1.06)

        # display results, return that best has not been found
        pyplot.draw()
        pyplot.show()
        print(f"Spacecraft Mass: {spacecraftMass:,d}kg")
        print(f"Altitude Reached: {maximumAlt:,d}m\n")
        return False

    else:
        # didn't make it to space, return false, allowing last graph printed to represent best effort
        return spacecraftMass / MASS_MULTIPLIER



def calculateDrag(velocity):
    # simple function to calculate drag at velocity -> drag = C_d * 1/2*p*v^2

    # using drag coeff. (C_d) of simple rocket, constant atmospheric density (p)
    C_d, p = 0.8, 1.225*np.exp(75/80)

    drag = C_d * (p * velocity**2 / 2)

    # if velocity is negative, drag should slow down rate of fall
    return drag * (-1 if velocity < 0 else 1)


def f(X, t, dryMass, I_sp, g, t_r):

    # extract variables from vector X
    m, s, v = X[0], X[1], X[2]


    # check if rocket has hit ground
    positiveAlt = (s > -1)

    # calculate drag at that velocity
    drag = calculateDrag(v)

    # calculate the change in altitude
    dsdt = v * positiveAlt

    # calculate change in mass (thrust divded by specific impusle)
    dmdt = (-(t_r / I_sp)) * (m >= dryMass)


    # calculate change in velocity
    thrustMass = (t_r) * (m >= dryMass) # if rocket at dry mass, fuel is spent, therefore thrust is not included in dvdt
    dvdt = ((thrustMass - drag)/m - g) * positiveAlt

    if (s < 0):
        # if rocket has hit ground, zero out the velocity
        dvdt = -v

    return (dmdt, dsdt, dvdt)

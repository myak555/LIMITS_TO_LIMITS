from Utilities import *

def PlotTable( engine,
    table,
    plotMin=None, plotMax=None,
    xLabel=None,
    filename="./Parametrizations/DYNAMO{:s}.png",
    show=False):
    """
    Plots a table against a primary argument
    """
    shortName = table.Name[5:]
    print( "   Plotting test table {:s}".format( table.Name))
    if plotMin is None: plotMin = table.Indices[0]  
    if plotMax is None: plotMax = table.Indices[-1]  
    xPlot = np.linspace( plotMin, plotMax, 101)
    yPlot = np.zeros( 101)
    for i, v in enumerate( xPlot): yPlot[i] = table.Lookup( v)       
    fig = plt.figure( figsize=(15,10))
    fig.suptitle('DYNAMO Table: {:s}'.format(shortName), fontsize=25)
    gs = plt.GridSpec(1, 1) 
    ax1 = plt.subplot(gs[0])
    ax1.plot( xPlot, yPlot, "-", lw=3, color="k")
    ax1.plot( table.Indices, table.PointsBefore, "o", lw=2, color="r", label="Before policy")
    if table.PointsAfter is not None:
        ax1.plot( table.Indices, table.PointsAfter, "o", lw=2, color="b", label="After policy")
        ax1.legend(loc=0)
    if table.Points1940 is not None:
        ax1.plot( table.Indices, table.Points1940, "o", lw=2, color="m", label="Prior to 1940")
        ax1.legend(loc=0)
    ax1.set_xlim( plotMin, plotMax)
    ax1.grid(True)
    if xLabel is not None:
        ax1.set_xlabel(xLabel)
    else:
        first_dependency = table.Dependencies[0]
        equation = engine.byName( first_dependency)
        s = "{:s} [{:s}]".format(first_dependency[5:], equation.Units)
        ax1.set_xlabel(s)
    ax1.set_ylabel("{:s} [{:s}]".format(shortName, table.Units))
    plt.savefig( filename.format(table.Name))
    if show: plt.show()
    else: plt.close('all')
    return


def PlotVariable(
    variable,
    ModelTime,
    xLabel="Model time [years]",
    filename="./Graphs/MODEL{:s}.png",
    show=False):
    """
    Plots a variable against model time
    """
    shortName = variable.Name[5:]
    print( "    Plotting {:s} [{:s}] against {:s}".format(
        variable.Name, variable.Units, xLabel))
    xPlot = []
    yPlot = []
    xNone = []
    for i, t in enumerate( ModelTime):
        if variable.Data[i] is None:
            xNone += [t]
            continue
        xPlot += [t]
        yPlot += [variable.Data[i]]
    xPlot = np.array(xPlot)
    yPlot = np.array(yPlot)
    yPlotMin = min(yPlot)
    yPlotMax = max(yPlot)
    fig = plt.figure( figsize=(15,10))
    fig.suptitle('DYNAMO Variable: {:s}'.format(shortName), fontsize=25)
    gs = plt.GridSpec(1, 1) 
    ax1 = plt.subplot(gs[0])
    for x in xNone:
        ax1.plot( [x,x], [yPlotMin, yPlotMax], "--", lw=3, alpha= 0.5, color="k")
    ax1.plot( xPlot, yPlot, "o", lw=2, color="k")
    ax1.plot( xPlot, yPlot, "-", lw=4, color="b", alpha=0.7)
    ax1.set_xlim( ModelTime[0], ModelTime[-1])
    ax1.grid(True)
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel("{:s} [{:s}]".format(shortName, variable.Units))
    plt.savefig( filename.format(variable.Name))
    if show: plt.show()
    else: plt.close('all')
    return

from Predictions import *
import fnmatch

def PlotDataPopulationOnly( entity, yr, Pyr):
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( '{:s} Population'.format(entity.Name), fontsize=22)
    gs = plt.GridSpec(1, 1)
    ax1 = plt.subplot(gs[0])
    ax1.plot( entity.Time,entity.Population_High, "--", lw=1, color='r', label="High")
    ax1.plot( entity.Time,entity.Population, "-", lw=2, color='b', label="Most likely")
    ax1.plot( entity.Time,entity.Population_Low, "--", lw=1, color='g', label="Low")
    if Pyr > 0:
        ax1.plot( [yr, yr], [0, Pyr], "-.", lw=1, color='m')
        ax1.text( yr+3, Pyr * 0.8, "In {:g}: {:.1f} mln".format(yr, Pyr))
    ax1.set_xlim( 1950, 2100)
    ax1.set_ylim( 0)
    ax1.set_ylabel("million")
    ax1.set_ylabel("Year")
    ax1.grid(True)
    ax1.legend(loc=0)
    plt.show(True)

def PlotDataLandUse( entity, yr, Pyr):
    fig = plt.figure( figsize=(15,10))
    fig.suptitle( '{:s} Population'.format(entity.Name), fontsize=22)
    gs = plt.GridSpec(2, 1)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax1.plot( entity.Time,entity.Population_High, "--", lw=1, color='r', label="High")
    ax1.plot( entity.Time,entity.Population, "-", lw=2, color='b', label="Most likely")
    ax1.plot( entity.Time,entity.Population_Low, "--", lw=1, color='g', label="Low")
    if Pyr > 0:
        ax1.plot( [yr, yr], [0, Pyr], "-.", lw=1, color='m')
        ax1.text( yr+3, Pyr * 0.8, "In {:g}: {:.1f} mln".format(yr, Pyr))
    ax1.set_xlim( 1950, 2100)
    ax1.set_ylim( 0)
    ax1.set_ylabel("million")
    ax1.grid(True)
    ax1.legend(loc=0)

    LU, LU_Low, LU_High = entity.GetLandUsage()
    #print( entity.Time)
    ax2.plot( entity.Time[150:], LU_Low[150:], "--", lw=1, color='g', label="High")
    ax2.plot( entity.Time[150:], LU[150:], "-", lw=2, color='b', label="Most likely")
    ax2.plot( entity.Time[150:], LU_High[150:], "--", lw=1, color='r', label="Low")
    if Pyr > 0:
        Lyr = LU[int(yr-1800)]
        ax2.plot( [yr, yr], [0, Lyr], "-.", lw=1, color='m')
        ax2.text( yr+3, Lyr * 1.2, "In {:g}: {:.1f} are/person".format(yr, Lyr))
    ax2.set_xlim( 1950, 2100)
    ax2.set_ylim( 0)
    ax2.set_ylabel("are/person")
    ax2.set_xlabel("Year")
    ax2.grid(True)
    ax2.legend(loc=0)
    plt.show(True)
    
def ProduceData( pop, comm):
    ss = comm.strip().split(",")
    try:
        entity = pop.GetEntity( ss[0].strip())
        print( entity.Name)
        if "not found" in entity.Name: return
        yr = 2020
        try:
            if len(ss) > 1: yr = int( ss[1].strip())
        except:
            yr = 2020
        outfile = "none"
        if len(ss) > 2: outfile = ss[2]
        Pyr = -1 
        for i, t in enumerate( entity.Time):
            if t != yr: continue
            if entity.Land_Area > 0.0:
                print( "Area: {:.1f} km² ({:.1f} km² with sea)".format( entity.Land_Area, entity.Total_Area))
            print( "In year {:g}:".format( t) )
            print( "Population {:.1f} mln (from {:.1f} to {:.1f})".format(
                    entity.Population[i],entity.Population_Low[i],entity.Population_High[i]) )
            if entity.Land_Area > 0.0:
                lu1, lu2, lu3 = entity.GetLandUsage()
                print( "Land: {:.1f} (from {:.1f} to {:.1f}) are/person".format( lu1[i],lu2[i],lu3[i]) )
            Pyr = entity.Population[i]
            break
        if outfile != "none":
            print( "Output goes to: " + outfile)
            f = open( outfile, "w")
            f.write("year,{:s}\n".format(entity.Name))
            for i in range( len(entity.Time)):
                f.write("{:g},{:.3f}\n".format(entity.Time[i], entity.Population[i]))
            f.close()
        if entity.Land_Area > 0.0:
            PlotDataLandUse( entity, yr, Pyr)
        else:
            PlotDataPopulationOnly( entity, yr, Pyr)
    except:
        print("Error")
        return

def MakeList( pop, comm):
    ss = Comm.split( ' ')
    lst = []
    for e in pop.Entities: lst += [e.Name]
    if len(ss)>1: lst = fnmatch.filter(lst, ss[1])
    lst.sort()
    for e in lst: print( e)  
    
print( "World population utility")    
Population = Population_UN()
ProduceData(Population, "WORLD")

while True:
    Comm = input( "Command: ")
    if Comm.startswith( "ex"): break
    if Comm.startswith( "list"):
        MakeList( Population, Comm)
        continue
    plt.close()
    ProduceData( Population, Comm)

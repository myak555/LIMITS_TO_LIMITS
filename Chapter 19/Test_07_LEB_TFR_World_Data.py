from Population import *

def Plot_Country( dest, country, yt, tfr, yl, leb, yp, pop, pop_scale, limits=(1950,2015)):
    fig = plt.figure( figsize=(15,15))
    gs = plt.GridSpec(3, 1, height_ratios=[1,1,1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    ax3 = plt.subplot(gs[2])

    ax1.set_title("Изменение LEB and TFR: {:s}".format(country), fontsize=22)
    ax1.plot( yt,tfr,"-",color="r")
    ax1.set_xlim( limits)
    ax1.set_ylim( 0, 9)
    ax1.set_ylabel("TFR")
    ax1.grid(True)

    ax2.plot( yl,leb,"-",color="g")
    ax2.set_xlim( limits)
    ax2.set_ylim( 20, 90)
    ax2.set_ylabel("LEB")
    ax2.grid(True)

    ax3.plot( yp,pop/pop[0],"-",color="b")    
    ax3.set_xlim( limits)
    ax3.set_ylim( 0, pop_scale)
    ax3.set_xlabel("год")
    ax3.set_ylabel("к популяции 1950")
    ax3.grid(True)
    
    dest_file = dest
    dest_file += country
    dest_file += ".png"
    plt.savefig( dest_file)
    plt.close('all')
    return

def Plot_Group( dest, group_name, UNF, UNFGroup, Population, pop_scale):
    total_P = np.zeros( 66)
    total_TFR = np.zeros( 66)
    total_LEB = np.zeros( 66)
    f = open(dest + group_name + ".txt", "w")

    print( "{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}".format(
        "Country", "Population(1950)", "Population(2015)", "TFR(1950)", "TFR(2015)", "LEB(1950)", "LEB(2015)", "P(2015)/P(1950)"))
    f.write( "{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:s}\n".format(
        "Country", "Population(1950)", "Population(2015)", "TFR(1950)", "TFR(2015)", "LEB(1950)", "LEB(2015)", "P(2015)/P(1950)"))
    for c in UNFGroup:
        entity = Population.GetEntity( c)
        if "not found" in entity.Name:
            print( c + " not found")
            continue
        yp = entity.Time[150:216]
        pop = entity.Population[150:216]
        yt,tfr = UNF.Countries[c].Get_TFR_vs_Year()
        yl,leb = UNF.Countries[c].Get_LEB_vs_Year()
        print( "{:s}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.2f}".format( c,
                                                              pop[0], pop[-1],
                                                              tfr[0], tfr[-1],
                                                              leb[0], leb[-1], pop[-1]/pop[0]))
        f.write( "{:s}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.2f}\n".format( c,
                                                              pop[0], pop[-1],
                                                              tfr[0], tfr[-1],
                                                              leb[0], leb[-1], pop[-1]/pop[0]))
        total_P += pop
        total_TFR += pop * tfr
        total_LEB += pop * leb
        Plot_Country( dest, c, yt, tfr, yl, leb, yp, pop, pop_scale)

    total_TFR /= total_P
    total_LEB /= total_P
    print( "{:s}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.2f}".format( "TOTAL Group",
        total_P[0], total_P[-1],
        total_TFR[0], total_TFR[-1],
        total_LEB[0], total_LEB[-1], total_P[-1]/total_P[0]))
    f.write( "{:s}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.1f}\t{:.2f}\n".format( "TOTAL Group",
        total_P[0], total_P[-1],
        total_TFR[0], total_TFR[-1],
        total_LEB[0], total_LEB[-1], total_P[-1]/total_P[0]))
    f.close()
    Plot_Country( dest, group_name, yt, total_TFR, yl, total_LEB, yp, total_P, pop_scale)
    return

Population = Population_UN()
UNF = UN_Fertility()
Plot_Group( "./Exceptions/", "Exceptions_Combined", UNF, UNF.Exceptions, Population, 20)
Plot_Group( "./Phase_2a/", "Phase_2a_Combined", UNF, UNF.Group_2a, Population, 20)
#Plot_Group( "./Phase_2b/", "Phase_2b_Combined", UNF, UNF.Group_2b, Population, 10)
#Plot_Group( "./Phase_3/", "Phase_3_Combined", UNF, UNF.Group_3, Population, 6)
#Plot_Group( "./Phase_4/", "Phase_4_Combined", UNF, UNF.Group_4, Population, 2)

#if InteractiveModeOn: plt.show(True)

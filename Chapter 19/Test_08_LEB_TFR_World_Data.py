from Population import *

def Plot_Area( area, area_name, ax1, ax2, ax3, UNF, Population, col="k"):
    entity = Population.GetEntity( area)
    if "not found" in entity.Name:
        print( area + " not found")
        return
    yp = entity.Time[150:216]
    pop = entity.Population[150:216]
    yt,tfr = UNF.Countries[area].Get_TFR_vs_Year()
    yl,leb = UNF.Countries[area].Get_LEB_vs_Year()
    ax1.plot( yt,tfr,"-",color=col)
    ax2.plot( yl,leb,"-",color=col)
    ax3.plot( yp,pop,"-",color=col, label=area_name)    
    return

Population = Population_UN()
UNF = UN_Fertility()
limits = 1950, 2015

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 1, height_ratios=[1,1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

Plot_Area( UNF.Areas[1], "Азия", ax1, ax2, ax3, UNF, Population, "y") 
Plot_Area( UNF.Areas[0], "Африка", ax1, ax2, ax3, UNF, Population, "k") 
Plot_Area( UNF.Areas[2], "Европа", ax1, ax2, ax3, UNF, Population, "b") 
Plot_Area( UNF.Areas[3], "Латинск. Америка", ax1, ax2, ax3, UNF, Population, "r") 
Plot_Area( UNF.Areas[4], "Сев. Америка", ax1, ax2, ax3, UNF, Population, "g") 
Plot_Area( UNF.Areas[5], "Океания", ax1, ax2, ax3, UNF, Population, "m") 

ax1.set_title("Изменение LEB and TFR", fontsize=22)
ax1.set_xlim( limits)
ax1.set_ylim( 0, 9)
ax1.set_ylabel("TFR")
ax1.grid(True)

ax2.set_xlim( limits)
ax2.set_ylim( 20, 90)
ax2.set_ylabel("LEB")
ax2.grid(True)

ax3.set_xlim( limits)
ax3.set_ylim( 0, 4000)
ax3.set_xlabel("год")
ax3.set_ylabel("миллионов")
ax3.legend( loc=0)
ax3.grid(True)
plt.savefig( "./Graphs/figure_19_08.png")

if InteractiveModeOn: plt.show(True)

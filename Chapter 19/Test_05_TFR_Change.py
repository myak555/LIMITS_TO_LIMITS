from Population import *

class Country():
    def __init__( self, name, year, tfr1=6, tfr2=4, leb=35):
        self.Year = year
        self.Population = Population_World3( self.Year[0], 10, tfr1, leb)
        l = len( self.Year)
        self.Total = np.zeros(l)
        self.Name = name
        self.TFR = np.ones(l) * tfr1
        self.LEB = np.ones(l) * leb        
        self.Birth_Rate = np.zeros(l)
        self.Death_Rate = np.zeros(l)
        self.TFR_Model = Sigmoid( 1840, 0.20, tfr1, tfr2)
        for i, y in enumerate(Year):
            if i == 0:
                self.Distribution1_Male = np.array(
                    self.Population.Population_Male) * 100 / self.Population.Total
                self.Distribution1_Female = np.array(
                    self.Population.Population_Female) * 100 / self.Population.Total
            if y == 1850:
                self.Distribution2_Male = np.array(
                    self.Population.Population_Male) * 100 / self.Population.Total
                self.Distribution2_Female = np.array(
                    self.Population.Population_Female) * 100 / self.Population.Total
            if y == Year[-1]:
                self.Distribution3_Male = np.array(
                    self.Population.Population_Male) * 100 / self.Population.Total
                self.Distribution3_Female = np.array(
                    self.Population.Population_Female) * 100 / self.Population.Total
            self.Total[i] = self.Population.Total
            self.Birth_Rate[i] = self.Population.nBirth / self.Population.Total * 100
            self.Death_Rate[i] = self.Population.nDeath / self.Population.Total * 100
            self.TFR[i] = self.TFR_Model.Compute( y)
            self.Population.Compute_Next_Year( tfr=self.TFR[i])
        self.Birth_Rate[0] = self.Birth_Rate[1]
        self.Death_Rate[0] = self.Death_Rate[1]
        print("{:s}: {:.1f}".format( name, self.Total[i]))
        return
    def Plot_Population( self, ax1, ax2):
        ax1.plot( self.Year, self.Total, "-", lw=2, color="b",
                  label="Популяция")
        ax1.plot( self.Year, np.array( self.TFR)*10, "-.", lw=2, color="g",
                  label="TFR х 10")
        ax1.plot( self.Year, self.LEB, "--", lw=2, color="r",
                  label="LEB = 35")
        ax2.plot( self.Year, self.Birth_Rate, "-.", lw=2, color="g",
                  label="рождаемость")                  
        ax2.plot( self.Year, self.Death_Rate, "--", lw=2, color="r",
                  label="смертность")                  
        return
    def Plot_Distribution( self, ax, distribution_male, distribution_female, year, x_label=False, y_label=False):
        ax.barh( self.Population.Ages, distribution_male,
                 height=1, color="b", alpha=0.5, label=str(year))
        ax.barh( self.Population.Ages, -distribution_female,
                 height=1, color="r", alpha=0.5)
        ax.set_xlim( -2, 2)
        ax.set_ylim( 0, 100)
        if x_label: ax.set_xlabel("%% популяции")
        if y_label: ax.set_ylabel("возраст, лет")
        ax.grid(True)
        ax.legend(loc=0)
        return

Year = np.linspace(1800, 1900, 101)
C = Country( "TFR_Change", Year)

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 3, height_ratios=[1,1,1]) 
ax1 = plt.subplot(gs[0,0:3])
ax2 = plt.subplot(gs[1,0:3])
ax3a = plt.subplot(gs[6])
ax3b = plt.subplot(gs[7])
ax3c = plt.subplot(gs[8])

ax1.set_title("Изменение TFR с 6 до 4 при LEB=35", fontsize=22)
C.Plot_Population( ax1, ax2)
ax1.set_xlim( Year[0], Year[-1])
ax2.set_xlim( Year[0], Year[-1])
ax2.plot( [1820,1820], [2,5], "--", lw=2, color="k")                  
ax2.text( 1805, 4.5, "Этап 2")              
ax2.plot( [1870,1870], [2,5], "--", lw=2, color="k")                  
ax2.text( 1845, 4.5, "Этап 3")              
ax2.text( 1875, 3.5, "Этап 4")              
ax1.set_ylim( 0, 80)
ax2.set_ylim( 2, 5)
ax1.set_ylabel("единиц")
ax2.set_ylabel("%%")
ax1.grid(True)
ax2.grid(True)
ax1.legend(loc=0)
ax2.legend(loc=0)
C.Plot_Distribution( ax3a, C.Distribution1_Male, C.Distribution1_Female, 1800, True, True)
C.Plot_Distribution( ax3b, C.Distribution2_Male, C.Distribution2_Female, 1840, True, False)
C.Plot_Distribution( ax3c, C.Distribution3_Male, C.Distribution3_Female, 1900, True, False)
fig.canvas.draw()
lbls = [itm.get_text() for itm in ax3a.get_xticklabels()]
lbls[0] = lbls[-1]
lbls[1] = lbls[-2]
ax3a.set_xticklabels(lbls)
ax3b.set_xticklabels(lbls)
ax3c.set_xticklabels(lbls)
plt.savefig( "./Graphs/figure_19_05.png")
if InteractiveModeOn: plt.show(True)

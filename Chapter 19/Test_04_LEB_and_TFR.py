from Population import *

class Country():
    def __init__( self, name, year, tfr=5, leb=35):
        self.Year = year
        self.Population = Population_World3( self.Year[0], 100, tfr, leb)
        l = len( self.Year)
        self.Total = np.zeros(l)
        self.Name = name
        self.TFR = tfr
        self.LEB = leb        
        self.Birth_Rate = np.zeros(l)
        self.Death_Rate = np.zeros(l)
        for i, y in enumerate(Year):
            self.Total[i] = self.Population.Total
            self.Birth_Rate[i] = self.Population.nBirth / self.Population.Total * 100
            self.Death_Rate[i] = self.Population.nDeath / self.Population.Total * 100
            self.Population.Compute_Next_Year()
        self.Birth_Rate[0] = self.Birth_Rate[1]
        self.Death_Rate[0] = self.Death_Rate[1]
        print("{:s}: {:.1f}".format( name, self.Total[i]))
        return
    def Plot_Population( self, ax1, ax2, line, color, lw):
        ax1.plot( self.Year, self.Total, line, lw=2, color=color,
                  label="{:s}: TFR={:.1f}, LEB={:.0f}".format(self.Name, self.TFR, self.LEB))
        if color=="g" and lw == 1:
            ax2.plot( self.Year, self.Birth_Rate, "-.", lw=lw, color=color,
                  label="рождаемость")                  
            ax2.plot( self.Year, self.Death_Rate, "--", lw=lw, color=color,
                  label="смертность")                  
        else:
            ax2.plot( self.Year, self.Birth_Rate, "-.", lw=lw, color=color)
            ax2.plot( self.Year, self.Death_Rate, "--", lw=lw, color=color)
        return
    def Plot_Distribution( self, ax, x_label=False, y_label=False):
        ax.barh( self.Population.Ages, self.Population.Population_Male*100/self.Population.Total,
                 height=1, color="b", alpha=0.5, label=self.Name)
        ax.barh( self.Population.Ages, -self.Population.Population_Female*100/self.Population.Total,
                 height=1, color="r", alpha=0.5)
        chld = (np.sum( self.Population.Population_Male[:15])
                + np.sum( self.Population.Population_Female[:15]))*100/self.Population.Total
        ax.plot( [-2, 2], [15,15], "--", color="k", lw=2)
        ax.text( -1.95, 20, "Дети: {:.1f}%".format(chld), color="k" )
        ax.text( -1.95, 93, "LEB = {:.0f} лет".format(self.LEB), color="k" )
        ax.text( -1.95, 85, "TFR = {:.1f}".format(self.TFR), color="k" )
        ax.set_xlim( -2, 2)
        ax.set_ylim( 0, 100)
        if x_label: ax.set_xlabel("%% популяции")
        if y_label: ax.set_ylabel("возраст, лет")
        ax.grid(True)
        ax.legend(loc=0)
        return

Year = np.linspace(1900, 2000, 101)
A1 = Country( "A1", Year, 7.1941, 35)
A2 = Country( "A2", Year, 4.8014, 55)
A3 = Country( "A3", Year, 3.6700, 75)
B1 = Country( "B1", Year, 4.1620, 35)
B2 = Country( "B2", Year, 2.7675, 55)
B3 = Country( "B3", Year, 2.1101, 75)
C1 = Country( "C1", Year, 2.3716, 35)
C2 = Country( "C2", Year, 1.5709, 55)
C3 = Country( "C3", Year, 1.1946, 75)

fig = plt.figure( figsize=(15,10))
gs = plt.GridSpec(2, 1, height_ratios=[1,1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.set_title("Демографический переход в коде World3", fontsize=22)
A1.Plot_Population( ax1, ax2, "-", "r", 1)
A2.Plot_Population( ax1, ax2, "-.", "r", 2)
A3.Plot_Population( ax1, ax2, "--", "r", 3)
B1.Plot_Population( ax1, ax2, "-", "g", 1)
B2.Plot_Population( ax1, ax2, "-.", "g", 2)
B3.Plot_Population( ax1, ax2, "--", "g", 3)
C1.Plot_Population( ax1, ax2, "-", "b", 1)
C2.Plot_Population( ax1, ax2, "-.", "b", 2)
C3.Plot_Population( ax1, ax2, "--", "b", 3)
ax1.set_xlim( Year[0], Year[-1])
ax2.set_xlim( Year[0], Year[-1])
ax1.set_ylim( 0, 800)
#ax2.set_ylim( 0, 8)
ax2.set_xlabel("условный год")
ax1.set_ylabel("миллионов")
ax2.set_ylabel("%%")
ax1.grid(True)
ax2.grid(True)
ax1.legend(loc=0)
ax2.legend(loc=0)
plt.savefig( "./Graphs/figure_19_04a.png")
#if InteractiveModeOn: plt.show(True)

fig = plt.figure( figsize=(15,15))
gs = plt.GridSpec(3, 3)
axs = []
for i in range(9):
    axs += [plt.subplot(gs[i])]
A1.Plot_Distribution( axs[0], y_label=True)
A2.Plot_Distribution( axs[1])
A3.Plot_Distribution( axs[2])
B1.Plot_Distribution( axs[3], y_label=True)
B2.Plot_Distribution( axs[4])
B3.Plot_Distribution( axs[5])
C1.Plot_Distribution( axs[6], x_label=True, y_label=True)
C2.Plot_Distribution( axs[7], x_label=True)
C3.Plot_Distribution( axs[8], x_label=True)
fig.canvas.draw()
lbls = [itm.get_text() for itm in axs[0].get_xticklabels()]
lbls[0] = lbls[-1]
lbls[1] = lbls[-2]
for i in range(9): axs[i].set_xticklabels(lbls)
plt.savefig( "./Graphs/figure_19_04b.png")
if InteractiveModeOn: plt.show(True)

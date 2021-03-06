from W3_Population_Test import *

P0 = Population()
P1 = Population_World3()

tfr = Linear_Combo()
tfr.Wavelets += [Sigmoid( x0=1975.000, s0=0.07740, left=5.400, right=2.350)]
tfr.Wavelets += [Hubbert( x0=1967.000, s0=0.29510, s1=0.24133, peak=0.631)]
tfr.Wavelets += [Hubbert( x0=1987.000, s0=0.43047, s1=0.43047, peak=0.211)]
tfr.Wavelets += [Hubbert( x0=1998.000, s0=0.53144, s1=0.31381, peak=-0.074)]
tfr.Wavelets += [Hubbert( x0=1955.000, s0=1.00000, s1=1.00000, peak=-0.057)]
tfr.Wavelets += [Hubbert( x0=1962.000, s0=1.00000, s1=1.00000, peak=0.048)]
tfr.Wavelets += [Hubbert( x0=1978.000, s0=1.00000, s1=1.00000, peak=-0.030)]
tfr.Wavelets += [Hubbert( x0=2014.000, s0=0.59049, s1=0.59049, peak=0.017)]
tfr.Wavelets += [Hubbert( x0=1955, s0=0.2, s1=0.09, peak=0.5)]

leb = Linear_Combo()
leb.Wavelets  = [Sigmoid( x0=1965.000, s0=0.03183, left=26.500, right=80.400)]
leb.Wavelets += [Hubbert( x0=1975.000, s0=0.18500, s1=0.13500, peak=1.632)]
leb.Wavelets += [Hubbert( x0=2000.000, s0=0.28000, s1=0.31000, peak=-1.000)]
leb.Wavelets += [Hubbert( x0=1961.000, s0=0.15009, s1=0.47500, peak=-1.700)]
leb.Wavelets += [Hubbert( x0=1948, s0=0.1, s1=1, peak=-7)]

Year = []
Total = []
TFR_Actual = []
LEB_Actual_Male = []
LEB_Actual_Female = []
Pops = []
for i in range(1890, 2041):
    Year += [i]
    Total += [P1.Total]
    LEB_Actual_Male += [P1.LEB_True_Male]
    LEB_Actual_Female += [P1.LEB_True_Female]
    TFR_Actual += [P1.TFR]
    Pops += [(np.array(P1.Population_Male),np.array(P1.Population_Female))]
    P1.Compute_Next_Year(tfr.Compute(i), leb_male=leb.Compute(i)-2, leb_female=leb.Compute(i)+2)
Year = np.array(Year)
Total = np.array(Total)
LEB_Actual_Male = np.array(LEB_Actual_Male)
LEB_Actual_Female = np.array(LEB_Actual_Female)
LEB_Actual_Male[0] = LEB_Actual_Male[1]
LEB_Actual_Female[0] = LEB_Actual_Female[1]

fig = plt.figure( figsize=(15,10))
gs = plt.GridSpec(2, 2, height_ratios=[1,1], width_ratios=[1,1]) 
ax1 = plt.subplot(gs[0,1:2])

ax1 = plt.subplot(gs[0,:])
ax2 = plt.subplot(gs[1,0:1])
ax3 = plt.subplot(gs[1,1:2])

ax1.set_title("Тест демографической системы World3", fontsize=22)
ax1.plot( Year, Total/1000, "-", lw=3, color="b", label="Популяция, млрд")
ax1.plot( Year, TFR_Actual, "--", lw=2, color="g", label="TFR")
ax1.plot( Year, LEB_Actual_Male/10, "--", lw=2, color="b", label="LEB, мужч., /10")
ax1.plot( Year, LEB_Actual_Female/10, "--", lw=2, color="r", label="LEB, женщ., /10")
ax1.errorbar( P0.Calibration_Year, P0.Calibration_Total/1000, yerr=P0.Calibration_Yerr/1000, fmt=".", color="k", label="Реальная (ООН)")
ax1.set_xlim( 1890, 2040)
ax1.set_ylim( 0, 8)
ax1.set_ylabel("Единиц")
ax1.grid(True)
ax1.legend(loc=0)

ax2.barh( P1.Ages, Pops[0][0]*100/Total[0],  height=1, color="b", alpha=0.5, label="Мужч., {:g}".format(Year[0]))
ax2.barh( P1.Ages, -Pops[0][1]*100/Total[0], height=1, color="r", alpha=0.5, label="Женщ., {:g}".format(Year[0]))
chld = (np.sum( Pops[0][0][:15]) + np.sum( Pops[0][1][:15]))*100/Total[0]
ax2.plot( [-2, 2], [15,15], "--", color="k", lw=2)
ax2.text( -1.9, 20, "Дети: {:.1f}%".format(chld), color="k" )
ax2.set_xlim( -2, 2)
ax2.set_ylim( 0, 100)
ax2.set_xlabel("%% популяции")
ax2.set_ylabel("возраст, лет")
ax2.grid(True)
ax2.legend(loc=0)

ax3.barh( P1.Ages, Pops[-1][0]*100/Total[-1],  height=1, color="b", alpha=0.5, label="Мужч., {:g}".format(Year[-1]))
ax3.barh( P1.Ages, -Pops[-1][1]*100/Total[-1], height=1, color="r", alpha=0.5, label="Женщ., {:g}".format(Year[-1]))
chld = (np.sum( Pops[-1][0][:15]) + np.sum( Pops[-1][1][:15]))*100/Total[-1]
ax3.plot( [-2, 2], [15,15], "--", color="k", lw=2)
ax3.text( -1.9, 20, "Дети: {:.1f}%".format(chld), color="k" )
ax3.set_xlim( -2, 2)
ax3.set_ylim( 0, 100)
ax3.set_xlabel("%% популяции")
ax3.grid(True)
ax3.legend(loc=0)

fig.canvas.draw()
lbls = [itm.get_text() for itm in ax2.get_xticklabels()]
lbls[0] = lbls[-1]
lbls[1] = lbls[-2]
ax2.set_xticklabels(lbls)
ax3.set_xticklabels(lbls)

plt.savefig( "./Graphs/figure_19_03.png")
if InteractiveModeOn: plt.show(True)

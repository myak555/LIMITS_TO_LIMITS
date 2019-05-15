from Utilities import *

Year = np.linspace(2000, 2040, 41)
PC_Estimate = Hubbert( 2016, 0.56, 0.1, 230, 15).GetVector( Year)
PE_Estimate = Hubbert( 2016, 0.56, 0.11, 420, 15).GetVector( Year)
PG_Estimate = Hubbert( 2018, 0.05, 0.07, 1040, 80).GetVector( Year)

Historical_Year, Historical_Oil, Historical_Gas = Load_Calibration(
    "./Data/US_Fossil_Fuel_Reconstructed.csv",
    ["Year", "Oil", "Gas"])
Rig_Year, Oil_Wells, Gas_Wells, Dry_Wells, Expl_Wells = Load_Calibration(
    "./Data/US_Rigs_and_Wells.csv",
    ["Year", "Dev_Oil", "Dev_Gas", "Dev_Dry", "Expl_Total"])
Footage_Year, Length_Total, Length_Expl, Length_Dev = Load_Calibration(
    "./Data/US_Well_Footage.csv",
    ["Year", "Total", "Expl_Total", "Prod_Total"])

fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Добыча нефти и природного газа в США', fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[2, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Historical_Year, Historical_Oil, "-", lw=3, color='g', label="Добыча нефти с 1859 года ({:.1f} 10⁹ т)".format(np.sum(Historical_Oil)/1000))
ax1.plot( Historical_Year, Historical_Oil+Historical_Gas, "-", lw=3, color='r', label="Добыча газа с 1821 года ({:.1f} 10⁹ toe)".format(np.sum(Historical_Gas)/1000))
ax1.plot( [1900,2100], [1155,1155], "--", lw=1, color='r', label="Рекорд добычи 2015 г - 1144 млн toe")
ax1.plot( Year[17:], PE_Estimate[17:], "--", lw=3, color='g')
ax1.plot( Year[17:], PG_Estimate[17:], "--", lw=3, color='r')
ax1.set_xlim( 1900, 2020)
ax1.set_ylim( 0, 1500)
ax1.set_ylabel("Млн toe в год")
ax1.grid(True)
ax1.set_title( "Добыча природных углеводородов")
ax1.legend(loc=2)

ax2.plot( Rig_Year[:-7], Oil_Wells[:-7]/1000, "-", lw=2, color='g', label="Нефтяных {:.0f} тыс".format(np.sum(Oil_Wells[:-7])/1000))
ax2.plot( Rig_Year[:-7], (Gas_Wells[:-7]+Oil_Wells[:-7])/1000, "-", lw=2, color='r', label="Газовых {:.0f} тыс".format(np.sum(Gas_Wells[:-7])/1000))
ax2.plot( Rig_Year[:-7], (Gas_Wells[:-7]+Oil_Wells[:-7]+Dry_Wells[:-7])/1000, "-", lw=1, color='k', label="Сухих {:.0f} тыс".format(np.sum(Dry_Wells[:-7])/1000))
ax2.plot( Rig_Year[:-7], (Gas_Wells[:-7]+Oil_Wells[:-7]+Dry_Wells[:-7]+Expl_Wells[:-7])/1000, "--", lw=1, color='k', label="Разведочных {:.0f} тыс".format(np.sum(Expl_Wells[:-7])/1000))
#print( (Gas_Wells[:-7]+Oil_Wells[:-7]+Dry_Wells[:-7]+Expl_Wells[:-7])/1000)
print( "Total cumulative oil and gas: {:.1f} mlrd toe".format( np.sum(Historical_Oil[149:]+Historical_Gas[149:])/1000))
ax2.plot( [1986,2040], [20,20], "--", lw=1, color='k')
ax2.set_xlim( 1900, 2020)
ax2.set_ylim( 0, 100)
ax2.set_ylabel("Тысяч в год")
ax2.grid(True)
ax2.set_title( "Пробурено скважин с 1949 по 2010 гг")
ax2.legend(loc=2)
ax2.annotate("Пик бурения в 1981 году", xy=(1981, 90), xytext=(1990, 80), arrowprops=dict(facecolor='black', shrink=0.05))

ax3.plot( Footage_Year, Length_Total/1000*0.3048, "-", lw=2, color='m', label="Всего {:.2f} млн км".format(np.sum(Length_Total)/1000000*0.3048))
ax3.plot( Footage_Year[:-9], Length_Expl[:-9]/1000*0.3048, "--", lw=2, color='m', label="Разведочных {:.2f} млн км".format(np.sum(Length_Expl[:-9])/1000000*0.3048))
ax3.plot( [1986,2040], [40,40], "--", lw=1, color='k')
ax3.set_xlim( 1900, 2020)
ax3.set_ylim( 0, 140)
ax3.set_xlabel("Годы")
ax3.set_ylabel("Тысяч км в год")
ax3.grid(True)
ax3.set_title( "Проходка скважин с 1949 по 2010 гг")
ax3.legend(loc=2)
ax3.annotate("Пик в 1981 году", xy=(1981, 125), xytext=(1950, 100), arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig( "./Graphs/figure_11_23.png")
fig.show()

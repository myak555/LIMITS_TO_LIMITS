from Utilities import *

Year,Total,Total_toe,Anthracite_T,Bituminous_T,Subbituminous_T,Lignite_T,Consumption_toe = Load_Calibration(
    "./Data/US_Coal_Reconstructed.csv",
    ["Year", "Total_T","Total_toe", "Anthracite_T", "Bituminous_T", "Subbituminous_T", "Lignite_T", "Consumption_toe"])

toet = Total_toe / Total
Year_Ext = np.linspace( 2011, 2017, 7)
Total_Ext = np.array( Total[211:])
Lignite_Ext = np.ones( len(Year_Ext)) * Lignite_T[ len(Lignite_T)-7]
Anthracite_Ext = np.ones( len(Year_Ext)) * Anthracite_T[ len(Anthracite_T)-7]
Bituminous_Ext = Hubbert( 2005, 1, .15, 515).GetVector( Year_Ext)
Subbituminous_Ext = Total_Ext - Lignite_Ext - Anthracite_Ext - Bituminous_Ext
Total_toe_Ext = Lignite_Ext/2.75 + Anthracite_Ext/1.21 + Bituminous_Ext/1.54 + Subbituminous_Ext/1.85

fig = plt.figure( figsize=(15,10))
fig.suptitle( "Добыча каменного угля в США", fontsize=22)
gs = plt.GridSpec(3, 1, height_ratios=[1, 1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])
ax3 = plt.subplot(gs[2])

ax1.plot( Year, Total, "-", lw=3, color='m', label="Всего ({:.1f} 10⁹ т)".format(np.sum(Total)/1000))
ax1.plot( Year[149:-6], Subbituminous_T[149:-6], "-", lw=2, color='k', label="Суббитуминозный")
ax1.plot( Year[149:-6], Bituminous_T[149:-6], "-", lw=2, color='b', label="Битуминозный")
ax1.plot( Year[149:-6], Lignite_T[149:-6], "-", lw=2, color='g', label="Лигнит")
ax1.plot( Year[149:-6], Anthracite_T[149:-6], "-", lw=2, color='r', label="Антрацит")
##ax1.plot( Year_Ext, Subbituminous_Ext, "-", lw=1, color='k')
##ax1.plot( Year_Ext, Bituminous_Ext, "-", lw=1, color='b')
##ax1.plot( Year_Ext, Lignite_Ext, "-", lw=1, color='g')
##ax1.plot( Year_Ext, Anthracite_Ext, "-", lw=1, color='r')
ax1.set_ylim( 0, 1200)
ax1.set_ylabel("Млн тонн в год")
ax1.set_xlim( 1800, 2030)
ax1.grid(True)
ax1.set_title( "Добыча по сортам угля")
ax1.legend(loc=0)

ax2.plot( Year[50:], toet[50:], "-", lw=2, color='r', label="Качество угля")
ax2.set_xlim( 1920, 2020)
ax2.set_ylim( 0.5, 0.8)
ax2.set_ylabel("toe/т")
ax2.grid(True)
#ax2.set_title( "Качество угля")
ax2.legend(loc=2)

ax3.plot( Year, Total_toe, "-", lw=2, color='m', label="Добыча ({:.1f} 10⁹ toe)".format(np.sum(Total_toe)/1000))
ax3.plot( Year[165:], Consumption_toe[165:], "--", lw=2, color='m', label="Потребление")
#ax3.plot( Year_Ext, Total_toe_Ext, "-", lw=1, color='k')
ax3.set_xlim( 1920, 2020)
ax3.set_ylim( 0, 700)
ax3.set_xlabel("Годы")
ax3.set_ylabel("Млн toe в год")
ax3.grid(True)
ax3.annotate("Пик добычи по энергии в 1998 году", xy=(1998, 610), xytext=(1950, 600), arrowprops=dict(facecolor='black', shrink=0.05))
#ax3.set_title( "Производство и потребление")
ax3.legend(loc=0)

plt.savefig( "./Graphs/figure_13_02.png")
if InteractiveModeOn: plt.show(True)

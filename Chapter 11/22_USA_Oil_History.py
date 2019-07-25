from US_Utilities import *

Year, sum_EIA, Wells, YC, PC = Get_Oil_Others()
sum_EIA1 = np.array(sum_EIA)
Wells1 = np.array(Wells)
PC1 = np.array(PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US13_Bakken_Oil.csv", "Bakken", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US14_EagleFord_Oil.csv", "EagleFord", sum_EIA, Wells, PC)
sum_EIA2 = np.array(sum_EIA)
Wells2 = np.array(Wells)
PC2 = np.array(PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US15_Permian_BoneSpring_Oil.csv", "Bonespring", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US16_Permian_Spraberry_Oil.csv", "Spraberry", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US17_Permian_Wolfcamp_Oil.csv", "Wolfcamp", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US18_Niobrara_Oil.csv", "Niobrara_Codell", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile_Oil( "./Data/US19_Austin_Chalk_Oil.csv", "Austin_Chalk", sum_EIA, Wells, PC)
sum_EIA3 = np.array(sum_EIA)
Wells3 = np.array(Wells)
PC3 = np.array(PC)

YH, PH1 = Load_Calibration( "./Data/US13_Bakken_Oil.csv", ["Year", "Hughes2014"])
YH, PH2 = Load_Calibration( "./Data/US14_EagleFord_Oil.csv", ["Year", "Hughes2014"])
PH = (PH1 + PH2) * 0.159 * 0.827 * 365

PC_Estimate = Hubbert( 2016, 0.56, 0.1, 230, 15).GetVector( Year)
PE_Estimate = Hubbert( 2016, 0.56, 0.11, 420, 15).GetVector( Year)

Historical_Year, Historical_Production = Load_Calibration(
    "../Global Data/US_Fossil_Fuel_Reconstructed.csv", ["Year", "Oil"])
Rig_Year, Rotary_Rigs, Onshore_Rigs = Load_Calibration(
    "./Data/US_Rigs_and_Wells.csv",
    ["Year", "Rotary_Rigs", "Onshore"])

Hubbert_Year = np.linspace( 1956, 2100, 145)
Hubbert_Oil = Hubbert( 1970, 0.054, 0.054, 392).GetVector( Hubbert_Year)
    
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча нефти и лицензионного конденсата в США', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( Historical_Year, Historical_Production, "-", lw=3, color='g', label="Добыча с 1859 года ({:.1f} 10⁹ т)".format(np.sum(Historical_Production)/1000))
ax1.plot( [1900,2100], [462.5,462.5], "--", lw=1, color='g', label="Рекорд добычи 1970 г - 462.5 млн т")
ax1.plot( Year, sum_EIA3, "--", lw=2, color='m', label= 'Нефть "сланцевых" AEO2016 ({:.1f} 10⁹ т)'.format(np.sum(sum_EIA3)/1000))
ax1.plot( Year, PC_Estimate, "-", lw=2, color='m', label= 'Нефть "сланцевых" Hughes-2016 ({:.1f} 10⁹ т)'.format(np.sum(PC_Estimate)/1000))
ax1.plot( Year[17:], PE_Estimate[17:], "--", lw=3, color='g')
ax1.plot( Hubbert_Year, Hubbert_Oil, "--", lw=1, color='k')
ax1.errorbar( YC, PC3, yerr=PC3*.05, fmt='o', color="m", label= 'Добыча с 2000 года ({:.1f} 10⁹ т)'.format(np.sum(PC3)/1000))
ax1.set_xlim( 1900, 2040)
ax1.set_ylim( 0, 1000)
ax1.set_ylabel("Млн тонн в год")
ax1.grid(True)
ax1.set_title( "Добыча нефти и лицензионного конденсата")
ax1.legend(loc=2)
ax1.annotate("Предсказание Хабберта 1956 года", xy=(1990, 296), xytext=(1940, 100), arrowprops=dict(facecolor='black', shrink=0.05))

ax2.plot( Rig_Year, Rotary_Rigs, "-", lw=3, color='g', label="Всего")
ax2.plot( Rig_Year[24:], Onshore_Rigs[24:], ".", lw=1, color='g', label="Наземных")
ax2.plot( [1986,2040], [730,730], "--", lw=1, color='g')
ax2.set_xlim( 1900, 2040)
ax2.set_ylim( 0, 5000)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Единиц в год")
ax2.grid(True)
ax2.set_title( "Буровых в США")
ax2.legend(loc=2)
ax2.annotate("Пик буровых в 1981 году", xy=(1981, 4000), xytext=(1990, 3500), arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig( "./Graphs/figure_11_22.png")
if InteractiveModeOn: plt.show(True)

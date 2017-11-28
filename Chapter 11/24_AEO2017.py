from Utilities import *

Year = np.linspace(2000, 2040, 41)
PC_Estimate = Hubbert( 2016, 0.56, 0.1, 230, 15).GetVector( Year)
PE_Estimate = Hubbert( 2016, 0.56, 0.11, 420, 15).GetVector( Year)
PG_Estimate = Hubbert( 2018, 0.05, 0.07, 1040, 80).GetVector( Year)

Historical_Year, Historical_Oil = Load_Calibration( "US_Fossil_Fuel_Reconstructed.csv", "Year", "Oil")
Historical_Year, Historical_Gas = Load_Calibration( "US_Fossil_Fuel_Reconstructed.csv", "Year", "Gas")

AEO2017_Year, AEO2016_Ref = Load_Calibration( "23_AEO2017_Oil.csv", "Year", "AEO2016")
AEO2017_Ref, AEO2017_NCP = Load_Calibration( "23_AEO2017_Oil.csv", "Ref", "NCP")
AEO2017_HEG, AEO2017_LEG = Load_Calibration( "23_AEO2017_Oil.csv", "HEG", "LEG")
AEO2017_HOP, AEO2017_LOP = Load_Calibration( "23_AEO2017_Oil.csv", "HOP", "LOP")
AEO2017_HOA, AEO2017_LOA = Load_Calibration( "23_AEO2017_Oil.csv", "HOA", "LOA")

AEO2017_YearG, AEO2016_RefG = Load_Calibration( "24_AEO2017_Gas.csv", "Year", "AEO2016")
AEO2017_RefG, AEO2017_NCPG = Load_Calibration( "24_AEO2017_Gas.csv", "Ref", "NCP")
AEO2017_HEGG, AEO2017_LEGG = Load_Calibration( "24_AEO2017_Gas.csv", "HEG", "LEG")
AEO2017_HOPG, AEO2017_LOPG = Load_Calibration( "24_AEO2017_Gas.csv", "HOP", "LOP")
AEO2017_HOAG, AEO2017_LOAG = Load_Calibration( "24_AEO2017_Gas.csv", "HOA", "LOA")

quad2t = 22.6766
market2total = 1.15
AEO2016_Ref *= quad2t 
AEO2017_Ref *= quad2t 
AEO2017_NCP *= quad2t 
AEO2017_HEG *= quad2t 
AEO2017_HOP *= quad2t 
AEO2017_HOA *= quad2t 
AEO2017_LEG *= quad2t 
AEO2017_LOP *= quad2t 
AEO2017_LOA *= quad2t 
AEO2016_RefG *= quad2t * market2total
AEO2017_RefG *= quad2t * market2total
AEO2017_NCPG *= quad2t * market2total 
AEO2017_HEGG *= quad2t * market2total 
AEO2017_HOPG *= quad2t * market2total 
AEO2017_HOAG *= quad2t * market2total 
AEO2017_LEGG *= quad2t * market2total 
AEO2017_LOPG *= quad2t * market2total 
AEO2017_LOAG *= quad2t * market2total 
for i in range( 26, 36):
    AEO2016_Ref[i] = AEO2016_Ref[i-1]*1.01 
    AEO2016_RefG[i] = AEO2016_RefG[i-1]*1.01 

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,15))
fig.suptitle( 'Добыча нефти и природного газа в США - прогнозы AEO2017', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[1, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( AEO2017_Year, AEO2017_HOA, "-.", lw=2, color='r', label="HOA ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HOA)/1000))
ax1.plot( AEO2017_Year, AEO2017_HOP, "--", lw=2, color='r', label="HOP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HOP)/1000))
ax1.plot( AEO2017_Year, AEO2016_Ref, "--", lw=1, color='g', label="AEO2016 ({:.1f} 10⁹ т)".format(np.sum(AEO2016_Ref)/1000))
ax1.plot( AEO2017_Year, AEO2017_HEG, "-", lw=2, color='r', label="HEG ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HEG)/1000))
ax1.plot( AEO2017_Year, AEO2017_Ref, "-", lw=3, color='g', label="Базовая ({:.1f} 10⁹ т)".format(np.sum(AEO2017_Ref)/1000))
ax1.plot( AEO2017_Year, AEO2017_NCP, ".", lw=3, color='g', label="Базовая без CP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_NCP)/1000))
ax1.plot( AEO2017_Year, AEO2017_LEG, "-", lw=2, color='b', label="LEG ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LEG)/1000))
ax1.plot( AEO2017_Year, AEO2017_LOP, "--", lw=2, color='b', label="LOP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LOP)/1000))
ax1.plot( AEO2017_Year, AEO2017_LOA, "-.", lw=2, color='b', label="LOA ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LOA)/1000))
ax1.errorbar( Historical_Year, Historical_Oil, yerr=Historical_Oil*.05, fmt='o', color="g", label="Реальная с 1859 года ({:.1f} 10⁹ т)".format(np.sum(Historical_Oil)/1000))
ax1.set_xlim( 1960, 2160)
ax1.set_ylim( 200, 800)
ax1.set_ylabel("Млн тонн в год")
ax1.grid(True)
ax1.set_title( "Добыча нефти и лицензионного конденсата")
ax1.legend(loc=1)

ax2.plot( AEO2017_YearG, AEO2017_HOAG, "-.", lw=2, color='r', label="HOA ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HOAG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_HOPG, "--", lw=2, color='r', label="HOP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HOPG)/1000))
ax2.plot( AEO2017_YearG, AEO2016_RefG, "--", lw=1, color='g', label="AEO2016 ({:.1f} 10⁹ т)".format(np.sum(AEO2016_RefG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_HEGG, "-", lw=2, color='r', label="HEG ({:.1f} 10⁹ т)".format(np.sum(AEO2017_HEGG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_RefG, "-", lw=3, color='g', label="Базовая ({:.1f} 10⁹ т)".format(np.sum(AEO2017_RefG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_NCPG, ".", lw=3, color='g', label="Базовая без CP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_NCPG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_LEGG, "-", lw=2, color='b', label="LEG ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LEGG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_LOPG, "--", lw=2, color='b', label="LOP ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LOPG)/1000))
ax2.plot( AEO2017_YearG, AEO2017_LOAG, "-.", lw=2, color='b', label="LOA ({:.1f} 10⁹ т)".format(np.sum(AEO2017_LOAG)/1000))
ax2.errorbar( Historical_Year, Historical_Gas, yerr=Historical_Gas*.05, fmt='o', color="g", label="Реальная с 1821 года ({:.1f} 10⁹ т)".format(np.sum(Historical_Gas)/1000))
ax2.set_xlim( 1960, 2160)
ax2.set_ylim( 200, 1200)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млн toe в год")
ax2.grid(True)
ax2.set_title( "Добыча газа и NGPL")
ax2.legend(loc=1)

plt.savefig( ".\\Graphs\\figure_11_24.png")
fig.show()

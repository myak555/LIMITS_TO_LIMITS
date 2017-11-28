from Utilities import *

def GetOthers( ):
    Year,AEO2016 = Load_Calibration( "20_Others_Oil.csv", "Year", "AEO2016") 
    YC,PC1 = Load_Calibration( "22_US_Tight_Oil_EIA.csv", "Year", "Monterey")
    PC2,PC3 = Load_Calibration( "22_US_Tight_Oil_EIA.csv", "Granite_Wash", "Marcellus")
    PC4,PC5 = Load_Calibration( "22_US_Tight_Oil_EIA.csv", "Haynesville", "Yeso_Glorieta")
    PC6,PC7 = Load_Calibration( "22_US_Tight_Oil_EIA.csv", "Delaware", "Utica")
    PC = PC1 + PC2 + PC3 + PC4 + PC5 + PC6 + PC7
    b2t = 0.159 * 0.827 
    bd2ty = b2t * 365
    AEO2016 *= bd2ty 
    PC *= b2t
    return Year, AEO2016, np.zeros(len(Year)), YC, PC 

def GetFile( data_name, field_name, sum_data_EIA, sum_well, sum_actual):
    Y,AEO2016 = Load_Calibration( data_name, "Year", "AEO2016") 
    Actual, Wells = Load_Calibration( data_name, "Actual", "Wells_Actual")
    YC,PC = Load_Calibration( "22_US_Tight_Oil_EIA.csv", "Year", field_name)
    b2t = 0.159 * 0.827 
    bd2ty = b2t * 365
    AEO2016 *= bd2ty 
    PC *= b2t
    return sum_data_EIA+AEO2016, sum_well+Wells, sum_actual+PC 

Year, sum_EIA, Wells, YC, PC = GetOthers()
sum_EIA1 = np.array(sum_EIA)
Wells1 = np.array(Wells)
PC1 = np.array(PC)
sum_EIA, Wells, PC = GetFile( "13_Bakken_Oil.csv", "Bakken", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile( "14_EagleFord_Oil.csv", "EagleFord", sum_EIA, Wells, PC)
sum_EIA2 = np.array(sum_EIA)
Wells2 = np.array(Wells)
PC2 = np.array(PC)
sum_EIA, Wells, PC = GetFile( "15_Permian_BoneSpring_Oil.csv", "Bonespring", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile( "16_Permian_Spraberry_Oil.csv", "Spraberry", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile( "17_Permian_Wolfcamp_Oil.csv", "Wolfcamp", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile( "18_Niobrara_Oil.csv", "Niobrara_Codell", sum_EIA, Wells, PC)
sum_EIA, Wells, PC = GetFile( "19_Austin_Chalk_Oil.csv", "Austin_Chalk", sum_EIA, Wells, PC)
sum_EIA3 = np.array(sum_EIA)
Wells3 = np.array(Wells)
PC3 = np.array(PC)

YH, PH1 = Load_Calibration( "13_Bakken_Oil.csv", "Year", "Hughes2014")
YH, PH2 = Load_Calibration( "14_EagleFord_Oil.csv", "Year", "Hughes2014")
PH = (PH1 + PH2) * 0.159 * 0.827 * 365

PC_Estimate = Hubbert( 2016, 0.56, 0.1, 230, 15).GetVector( Year)

Prepare_Russian_Font()
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Прогноз "сланцевой" нефти в США AEO2016', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( Year, sum_EIA3, "--", lw=2, color='g', label= 'За счёт "старых" месторождений ({:.1f} 10⁹ т)'.format(np.sum(sum_EIA3-sum_EIA2)/1000))
ax1.plot( Year, sum_EIA2, "--", lw=2, color='m', label= 'LTO "новых сланцевых" ({:.1f} 10⁹ т)'.format(np.sum(sum_EIA2-sum_EIA1)/1000))
ax1.plot( Year, sum_EIA1, "--", lw=2, color='r', label= 'Лицензионный конденсат "сланцевых" ({:.1f} 10⁹ т)'.format(np.sum(sum_EIA1)/1000))
ax1.plot( Year, PC_Estimate, "-", lw=2, color='g', label= 'Вероятная добыча из "сланцевых" ({:.1f} 10⁹ т)'.format(np.sum(PC_Estimate)/1000))
ax1.plot( YH, PH, "-", lw=2, color='m', label= 'Hughes-2014 Баккен+Иглфорд ({:.1f} 10⁹ т)'.format(np.sum(PH)/1000))
ax1.errorbar( YC, PC3, yerr=PC3*.05, fmt='o', color="g")
ax1.errorbar( YC, PC2, yerr=PC2*.05, fmt='o', color="m")
ax1.errorbar( YC, PC1, yerr=PC1*.05, fmt='o', color="r")
ax1.set_xlim( 2000, 2040)
ax1.set_ylim( 0, 500)
ax1.set_ylabel("Млн toe в год")
ax1.grid(True)
ax1.set_title( "Добыча сырой нефти, LTO и лицензионного конденсата")
ax1.legend(loc=2)

ax2.errorbar( Year[:-24], Wells3[:-24]/1000, yerr=.1, fmt='o', color="g", label='На "старых" нефтяных')
ax2.errorbar( Year[:-24], Wells2[:-24]/1000, yerr=.1, fmt='o', color="m", label='На "новых сланцевых"')
ax2.set_xlim( 2000, 2040)
ax2.set_ylim( 0, 100)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Тысяч скважин")
ax2.grid(True)
ax2.set_title( 'Количество "нефтяных" скважин в эксплуатации')
ax2.legend(loc=0)

plt.savefig( ".\\Graphs\\figure_11_21.png")
fig.show()

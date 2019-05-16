from US_Utilities import *

Year = np.linspace( 1994, 2040, 47)
sum_EIA = np.zeros( len( Year))
sum_HP = np.zeros( len( Year))
sum_HA = np.zeros( len( Year))
sum_WP = np.ones( len( Year)) * 20000
sum_WA = np.ones( len( Year)) * 20000
f1_Barnett = GetFile( "./Data/US01_Barnett_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f2_Marcellus = GetFile( "./Data/US02_Marcellus_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f3_Haynesville = GetFile( "./Data/US03_Haynesville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f4_EagleFord = GetFile( "./Data/US04_EagleFord_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f5_Fayetteville = GetFile( "./Data/US05_Fayetteville_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f6_Woodford = GetFile( "./Data/US06_Woodford_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f7_Bakken = GetFile( "./Data/US07_Bakken_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
f8_Haynesville = GetFile( "./Data/US08_Utica_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA, proj_name="Yakimov2017")
f9_Others = GetFile( "./Data/US09_Others_Gas.csv", sum_EIA, sum_HP, sum_HA, sum_WP, sum_WA)
for i in range( 6):
    sum_HP[i] += 19.6
    sum_HA[i] += 19.6

Prediction_T = np.linspace( 2017, 2100, 84)
Prediction_Conventional = Hubbert( 2000, 1, .085, 705).GetVector( Prediction_T)
Prediction_TG_Huges = Hubbert( 2016, 1, .07, 428).GetVector( Prediction_T)
Prediction_TG_EIA = Hubbert( 2042, .07, .5, 820).GetVector( Prediction_T)
Prediction_Total_Huges = Prediction_Conventional/1.1 + Prediction_TG_Huges 
Prediction_Total_EIA = Prediction_Conventional/1.1 + Prediction_TG_EIA

EIA_Year, EIA_Withdrawals, EIA_Repress, EIA_VnF, EIA_GW, EIA_OW, EIA_TG, EIA_CBM, EIA_dry, EIA_Marketed = Load_Calibration(
    "./Data/US11_US_Gas_EIA.csv",
    ["year", "gross", "repress", "vnf", "gas_wells", "oil_wells", "TG_wells", "CBM_wells", "dry", "marketed"])
mfty2bmy = 0.3048**3/1000
EIA_Withdrawals *= mfty2bmy
EIA_Repress *= mfty2bmy
EIA_VnF *= mfty2bmy
EIA_GW *= mfty2bmy
EIA_OW *= mfty2bmy
EIA_TG *= mfty2bmy
EIA_CBM *= mfty2bmy
EIA_dry *= mfty2bmy
EIA_Marketed *= mfty2bmy
EIA_Extracted = EIA_Withdrawals - EIA_Repress
EIA_Production = EIA_Extracted - EIA_VnF 

for i in range( len(EIA_CBM)):
    if EIA_GW[i] < 0: EIA_GW[i] = 0
    if EIA_OW[i] < 0: EIA_OW[i] = 0
    if EIA_TG[i] < 0: EIA_TG[i] = 0
    if EIA_CBM[i] < 0: EIA_CBM[i] = 0
for i in range( 36):
    EIA_Production[i] = EIA_Marketed[i]    
    EIA_dry[i] = EIA_Marketed[i]    
    EIA_Extracted[i] = EIA_Marketed[i] * 1.1
    EIA_Withdrawals[i] = EIA_Marketed[i] * 1.1 
    
fig = plt.figure( figsize=(15,10))
fig.suptitle( 'Добыча природного газа в США', fontsize=22)
gs = plt.GridSpec(2, 1, height_ratios=[2, 1]) 
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot( EIA_Year, EIA_Withdrawals, "-", lw=1, color='r', label="Добыча всего ({:.1f} 10¹² м³)".format(np.sum(EIA_Withdrawals)/1000))
ax1.plot( EIA_Year, EIA_Extracted, "-", lw=3, color='r', label="Минус закачка ({:.1f} 10¹² м³)".format(np.sum(EIA_Extracted)/1000))
ax1.plot( EIA_Year, EIA_Production, "-", lw=2, color='k', label="Минус факел ({:.1f} 10¹² м³)".format(np.sum(EIA_Production)/1000))
ax1.plot( EIA_Year, EIA_dry, "-", lw=2, color='b', label="Минус НСГ и NGPL ({:.1f} 10¹² м³)".format(np.sum(EIA_dry)/1000))
ax1.errorbar( Year[:-24], sum_HA[:-24], yerr=sum_HA[:-24]*.05, fmt='o', color="k", label='Газ "сланцевых" месторождений')
ax1.set_xlim( 1910, 2020)
ax1.set_ylim( 0, 1100)
ax1.set_ylabel("Млрд м³ в год")
ax1.grid(True)
ax1.set_title( "Добыча газа")
ax1.legend(loc=0)
ax1.annotate("Пик добычи в 2015 г", xy=(2015, 929), xytext=(1970, 1000), arrowprops=dict(facecolor='black', shrink=0.05))

ax2.plot( EIA_Year[67:], EIA_GW[67:], "-", lw=3, color='r', label='"Классический" газ')
ax2.plot( EIA_Year[67:], EIA_OW[67:], "-", lw=3, color='g', label='Попутный газ')
ax2.plot( EIA_Year[67:], EIA_CBM[67:], "-", lw=3, color='k', label='Рудничный газ')
ax2.plot( EIA_Year[67:], EIA_TG[67:], "-", lw=3, color='m', label='Трудноизвлекаемый газ')
ax2.plot( Year[:-24], sum_HA[:-24], "--", lw=1, color='m', label='В том числе "сланцевых"')
ax2.set_xlim( 1910, 2020)
ax2.set_ylim( 0, 600)
ax2.set_xlabel("Годы")
ax2.set_ylabel("Млрд м³ в год")
ax2.grid(True)
ax2.set_title( "Добыча по типу местрождения")
ax2.legend(loc=0)
ax2.annotate("Пик добычи в 1973 г", xy=(1973, 550), xytext=(1960, 300), arrowprops=dict(facecolor='black', shrink=0.05))
ax2.annotate("Падение добычи по 4.8% в год", xy=(2009, 387), xytext=(1970, 250), arrowprops=dict(facecolor='black', shrink=0.05))

plt.savefig( "./Graphs/figure_11_11.png")
if InteractiveModeOn: plt.show(True)
